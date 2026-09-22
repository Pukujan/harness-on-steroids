"""Thin CLI adapters used by the controller replay pilot."""

from __future__ import annotations

import json
import os
import shlex
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from shutil import which


@dataclass(frozen=True)
class HarnessRun:
    adapter: str
    status: str
    returncode: int | None
    duration_ms: float
    events_path: Path
    stderr_path: Path


def extract_tool_seq(path: Path) -> list[str]:
    """Extract tool names from JSON or JSON-lines output without retaining bodies."""

    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    result: list[str] = []
    parsed_lines = 0
    for line in text.splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        parsed_lines += 1
        if isinstance(value, dict):
            _collect_tool_names(value, result)
    if parsed_lines == 0:
        try:
            value = json.loads(text)
        except json.JSONDecodeError:
            return result
        _collect_tool_names(value, result)
    return result


def _collect_tool_names(value: object, result: list[str]) -> None:
    if not isinstance(value, dict):
        return
    for key in ("tool", "tool_name", "toolName", "function"):
        item = value.get(key)
        if isinstance(item, str) and item and key != "function":
            result.append(item.lower())
        elif isinstance(item, dict):
            _collect_tool_names(item, result)
    part = value.get("part")
    if isinstance(part, dict):
        _collect_tool_names(part, result)
    tool_call = value.get("tool_call")
    if isinstance(tool_call, dict):
        _collect_tool_names(tool_call, result)
    function = value.get("function")
    if isinstance(function, dict):
        name = function.get("name")
        if isinstance(name, str) and name:
            result.append(name.lower())
    tool_call = value.get("toolCall")
    if isinstance(tool_call, dict):
        _collect_tool_names(tool_call, result)


class HarnessAdapter:
    name = "harness"

    def available(self) -> bool:
        raise NotImplementedError

    def command(self, *, prompt_file: Path, workdir: Path, title: str) -> list[str]:
        raise NotImplementedError

    def prepare_workdir(self, workdir: Path) -> None:
        """Write adapter-local ignored configuration when a harness needs it."""

        return None

    def run(
        self,
        *,
        prompt: str,
        prompt_file: Path,
        workdir: Path,
        events_path: Path,
        stderr_path: Path,
        timeout: float,
        title: str,
    ) -> HarnessRun:
        prompt_file.write_text(prompt, encoding="utf-8")
        self.prepare_workdir(workdir)
        command = self.command(prompt_file=prompt_file, workdir=workdir, title=title)
        started = time.perf_counter()
        try:
            with events_path.open("w", encoding="utf-8") as events, stderr_path.open(
                "w", encoding="utf-8"
            ) as errors:
                process = subprocess.Popen(
                    command,
                    cwd=str(workdir),
                    stdout=events,
                    stderr=errors,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                )
                try:
                    process.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
                    return HarnessRun(
                        self.name,
                        "timeout",
                        None,
                        (time.perf_counter() - started) * 1000,
                        events_path,
                        stderr_path,
                    )
        except OSError as exc:
            stderr_path.write_text(type(exc).__name__, encoding="utf-8")
            return HarnessRun(
                self.name,
                "launch_error",
                None,
                (time.perf_counter() - started) * 1000,
                events_path,
                stderr_path,
            )
        stderr_text = stderr_path.read_text(encoding="utf-8", errors="replace")
        status = "ok" if process.returncode == 0 else f"fail_{process.returncode}"
        if process.returncode != 0 and "max turns reached" in stderr_text.lower():
            status = "partial"
        return HarnessRun(
            self.name,
            status,
            process.returncode,
            (time.perf_counter() - started) * 1000,
            events_path,
            stderr_path,
        )


def _resolve(command: str, fallback: str) -> str:
    configured = os.environ.get(command, "")
    return configured or which(fallback) or fallback


def _windows_node_command(name: str, fallback: str) -> str:
    configured = os.environ.get(f"{name.upper()}_COMMAND", "")
    if configured:
        return configured
    if os.name == "nt":
        candidates = (
            (Path(r"C:\nvm4w\nodejs\node_modules\opencode-ai\bin\opencode.exe"),)
            if name == "opencode"
            else (Path(rf"C:\nvm4w\nodejs\{name}.cmd"),)
        )
        for candidate in candidates:
            if candidate.is_file():
                return str(candidate)
    return which(fallback) or fallback


class OpenCodeAdapter(HarnessAdapter):
    name = "opencode"

    def __init__(self, executable: str | None = None, model: str | None = None) -> None:
        self.executable = executable or _windows_node_command("opencode", "opencode")
        self.model = model or os.environ.get("OPENCODE_MODEL", "")

    def available(self) -> bool:
        return Path(self.executable).is_file() or which(self.executable) is not None

    def prepare_workdir(self, workdir: Path) -> None:
        if not self.model.startswith("local-bonsai/"):
            return
        base_url = os.environ.get("LOCAL_MODEL_BASE_URL", "http://127.0.0.1:8080/v1")
        model_key = self.model.split("/", 1)[1] or "bonsai"
        config = {
            "$schema": "https://opencode.ai/config.json",
            "provider": {
                "local-bonsai": {
                    "npm": "@ai-sdk/openai-compatible",
                    "name": "Local Bonsai",
                    "options": {
                        "baseURL": base_url,
                        "apiKey": "none",
                        "timeout": 180000,
                        "chunkTimeout": 60000,
                    },
                    "models": {
                        model_key: {
                            "name": "Ternary Bonsai local endpoint",
                            "tool_call": True,
                            "reasoning": True,
                            "limit": {"context": 8192, "output": 2048},
                        }
                    },
                }
            },
        }
        (workdir / "opencode.json").write_text(
            json.dumps(config, indent=2) + "\n", encoding="utf-8"
        )

    def command(self, *, prompt_file: Path, workdir: Path, title: str) -> list[str]:
        prompt = prompt_file.read_text(encoding="utf-8")
        command = [
            self.executable,
            "run",
            "--agent",
            "codex",
            "--format",
            "json",
            "--dir",
            str(workdir),
            "--title",
            title,
            "--auto",
        ]
        if self.model:
            command.extend(["--model", self.model])
        command.append(prompt)
        return command


class GrokBuildAdapter(HarnessAdapter):
    name = "grok-build"

    def __init__(self, executable: str | None = None, model: str | None = None) -> None:
        self.executable = executable or _windows_node_command("grok", "grok")
        self.model = model or os.environ.get("GROK_BUILD_MODEL", "")
        self.max_turns = os.environ.get("GROK_BUILD_MAX_TURNS", "4")

    def available(self) -> bool:
        return Path(self.executable).is_file() or which(self.executable) is not None

    def command(self, *, prompt_file: Path, workdir: Path, title: str) -> list[str]:
        command = [
            self.executable,
            "--cwd",
            str(workdir),
            "--output-format",
            "json",
            "--always-approve",
            "--max-turns",
            self.max_turns,
            "--prompt-file",
            str(prompt_file),
        ]
        if self.model:
            command.extend(["--model", self.model])
        return command


class PiAdapter(HarnessAdapter):
    name = "pi"

    def __init__(self, executable: str | None = None) -> None:
        self.executable = executable or _resolve("PI_COMMAND", "pi")
        self.model = os.environ.get("PI_MODEL", "")
        self.extra_args = shlex.split(os.environ.get("PI_ARGS", ""))

    def available(self) -> bool:
        return Path(self.executable).is_file() or which(self.executable) is not None

    def prepare_workdir(self, workdir: Path) -> None:
        if not self.model.startswith("yolo-auto/"):
            return
        model_id = self.model.split("/", 1)[1] or "qwen3.8-flash"
        config_dir = workdir / ".pi" / "agent"
        config_dir.mkdir(parents=True, exist_ok=True)
        config = {
            "providers": {
                "yolo-auto": {
                    "baseUrl": os.environ.get("QWEN_API_URL", "https://yolo-auto.com/v1"),
                    "api": "openai-completions",
                    "apiKey": "$QWEN_API_KEY",
                    "compat": {
                        "supportsDeveloperRole": False,
                        "supportsReasoningEffort": False,
                    },
                    "models": [
                        {
                            "id": model_id,
                            "name": "Qwen Flash (YOLO Auto)",
                            "reasoning": True,
                            "input": ["text"],
                            "contextWindow": 131072,
                            "maxTokens": 16384,
                        }
                    ],
                }
            }
        }
        (config_dir / "models.json").write_text(
            json.dumps(config, indent=2) + "\n", encoding="utf-8"
        )
        os.environ["PI_CODING_AGENT_DIR"] = str(config_dir)

    def command(self, *, prompt_file: Path, workdir: Path, title: str) -> list[str]:
        command = [self.executable, *self.extra_args]
        if self.model:
            command.extend(["--model", self.model])
        command.extend(
            [
                "--mode",
                "json",
                "--print",
                "--no-session",
                "--approve",
                prompt_file.read_text(encoding="utf-8"),
            ]
        )
        return command


__all__ = [
    "GrokBuildAdapter",
    "HarnessAdapter",
    "HarnessRun",
    "OpenCodeAdapter",
    "PiAdapter",
    "extract_tool_seq",
]

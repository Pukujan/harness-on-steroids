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

HARNESS_INACTIVITY_TIMEOUT_SECONDS = 20 * 60
HARNESS_MAX_RUNTIME_SECONDS = 2 * 60 * 60
STREAM_POLL_SECONDS = 0.25


@dataclass(frozen=True)
class HarnessRun:
    adapter: str
    status: str
    returncode: int | None
    duration_ms: float
    events_path: Path
    stderr_path: Path
    timeout_reason: str | None = None


@dataclass(frozen=True)
class AdapterEvent:
    """Normalized event metadata; raw CLI bodies remain in ignored artifacts."""

    event_kind: str
    tool_name: str | None = None
    status: str = "observed"
    summary: str = ""

    def to_payload(self) -> dict[str, str]:
        payload = {
            "event_kind": self.event_kind,
            "status": self.status,
            "summary": self.summary,
        }
        if self.tool_name:
            payload["tool_name"] = self.tool_name
        return payload


def extract_event_seq(path: Path) -> list[AdapterEvent]:
    """Read JSON/NDJSON event metadata for all three CLI adapters."""

    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    values: list[object] = []
    for line in text.splitlines():
        try:
            values.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    if not values:
        try:
            values = [json.loads(text)]
        except json.JSONDecodeError:
            return []
    result: list[AdapterEvent] = []
    for value in values:
        if not isinstance(value, dict):
            continue
        event_kind = next(
            (
                str(value[key]).strip()
                for key in ("event", "event_type", "type", "kind", "name")
                if value.get(key) not in (None, "") and isinstance(value.get(key), (str, int))
            ),
            "json_event",
        )
        tool_names: list[str] = []
        _collect_tool_names(value, tool_names)
        status_value = value.get("status")
        status = str(status_value).strip() if status_value not in (None, "") else "observed"
        summary_value = value.get("summary")
        summary = str(summary_value).strip()[:500] if summary_value not in (None, "") else ""
        result.append(
            AdapterEvent(
                event_kind=event_kind,
                tool_name=tool_names[0] if tool_names else None,
                status=status,
                summary=summary,
            )
        )
    return result


def extract_session_id(path: Path) -> str | None:
    """Return a session identifier only when the adapter emitted one."""

    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    values: list[object] = []
    for line in text.splitlines():
        try:
            values.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    if not values:
        try:
            values = [json.loads(text)]
        except json.JSONDecodeError:
            return None

    def find(value: object) -> str | None:
        if isinstance(value, dict):
            for key in ("session_id", "sessionId", "sessionID"):
                candidate = value.get(key)
                if isinstance(candidate, str) and candidate.strip():
                    return candidate.strip()
            for nested in value.values():
                found = find(nested)
                if found:
                    return found
        elif isinstance(value, list):
            for nested in value:
                found = find(nested)
                if found:
                    return found
        return None

    for value in values:
        found = find(value)
        if found:
            return found
    return None


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

    #: When True the prompt is delivered over stdin and must NOT appear in argv
    #: (Windows truncates the command line and the harness never launches).
    prompt_via_stdin = False

    def available(self) -> bool:
        raise NotImplementedError

    def command(self, *, prompt_file: Path, workdir: Path, title: str) -> list[str]:
        raise NotImplementedError

    def prepare_workdir(self, workdir: Path) -> None:
        """Write adapter-local ignored configuration when a harness needs it."""

        return None

    def stream_events(self, events_path: Path) -> list[AdapterEvent]:
        """Return normalized event metadata without exposing raw event bodies."""

        return extract_event_seq(events_path)

    @staticmethod
    def _stream_signature(paths: tuple[Path, ...]) -> tuple[tuple[bool, int, int], ...]:
        signature: list[tuple[bool, int, int]] = []
        for path in paths:
            try:
                stat = path.stat()
            except OSError:
                signature.append((False, 0, 0))
            else:
                signature.append((True, stat.st_size, stat.st_mtime_ns))
        return tuple(signature)

    @classmethod
    def _wait_for_process(
        cls,
        process: subprocess.Popen[str],
        *,
        progress_paths: tuple[Path, ...],
        inactivity_timeout: float,
        max_runtime: float,
    ) -> str | None:
        """Wait while resetting the inactivity timer when stream files advance."""

        started = time.monotonic()
        last_activity = started
        previous = cls._stream_signature(progress_paths)
        while process.poll() is None:
            now = time.monotonic()
            current = cls._stream_signature(progress_paths)
            if current != previous:
                previous = current
                last_activity = now
            if now - started >= max_runtime:
                return "max_runtime"
            if now - last_activity >= inactivity_timeout:
                return "inactivity"
            time.sleep(STREAM_POLL_SECONDS)
        process.wait()
        return None

    def run(
        self,
        *,
        prompt: str,
        prompt_file: Path,
        workdir: Path,
        events_path: Path,
        stderr_path: Path,
        title: str,
        timeout: float = HARNESS_INACTIVITY_TIMEOUT_SECONDS,
        max_runtime: float = HARNESS_MAX_RUNTIME_SECONDS,
    ) -> HarnessRun:
        prompt_file.write_text(prompt, encoding="utf-8")
        self.prepare_workdir(workdir)
        command = self.command(prompt_file=prompt_file, workdir=workdir, title=title)
        started = time.perf_counter()
        use_stdin = self.prompt_via_stdin
        stdin_stream = subprocess.DEVNULL
        try:
            with events_path.open("w", encoding="utf-8") as events, stderr_path.open(
                "w", encoding="utf-8"
            ) as errors:
                process = subprocess.Popen(
                    command,
                    cwd=str(workdir),
                    stdin=subprocess.PIPE if use_stdin else stdin_stream,
                    stdout=events,
                    stderr=errors,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                )
                if use_stdin:
                    assert process.stdin is not None
                    try:
                        process.stdin.write(prompt)
                        process.stdin.close()
                    except (BrokenPipeError, ValueError):
                        # The harness exited before draining stdin; let the exit
                        # status below report the real failure instead.
                        pass
                timeout_reason = self._wait_for_process(
                    process,
                    progress_paths=(events_path, stderr_path),
                    inactivity_timeout=timeout,
                    max_runtime=max_runtime,
                )
                if timeout_reason is not None:
                    process.kill()
                    process.wait()
                    return HarnessRun(
                        self.name,
                        "timeout",
                        None,
                        (time.perf_counter() - started) * 1000,
                        events_path,
                        stderr_path,
                        timeout_reason,
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

    prompt_via_stdin = True

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
                        # Keep the provider's total request ceiling aligned with
                        # the host absolute cap; silence is governed separately
                        # by header/chunk timeouts.
                        "timeout": HARNESS_MAX_RUNTIME_SECONDS * 1000,
                        "headerTimeout": 1200000,
                        "chunkTimeout": 1200000,
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
        # Prompt is delivered over stdin (see prompt_via_stdin) to avoid the
        # Windows command-line length limit that silently aborted every arm.
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

    prompt_via_stdin = True

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
        settings = {
            "httpIdleTimeoutMs": 1200000,
            "retry": {
                "enabled": True,
                # This is a total provider request ceiling.  The idle boundary
                # remains 20 minutes, while an actively streaming request may
                # continue until the host's two-hour cap.
                "provider": {
                    "timeoutMs": HARNESS_MAX_RUNTIME_SECONDS * 1000,
                    "maxRetries": 0,
                },
            },
        }
        (config_dir / "settings.json").write_text(
            json.dumps(settings, indent=2) + "\n", encoding="utf-8"
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
            ]
        )
        # Prompt is delivered over stdin (see prompt_via_stdin); pi merges piped
        # stdin into the initial prompt in print mode. Passing it as argv blew the
        # Windows command-line limit ("The command line is too long") so the
        # harness never started and every replay turn recorded fail_1/0 tools.
        return command


__all__ = [
    "AdapterEvent",
    "GrokBuildAdapter",
    "HARNESS_MAX_RUNTIME_SECONDS",
    "HARNESS_INACTIVITY_TIMEOUT_SECONDS",
    "HarnessAdapter",
    "HarnessRun",
    "OpenCodeAdapter",
    "PiAdapter",
    "extract_event_seq",
    "extract_session_id",
    "extract_tool_seq",
]

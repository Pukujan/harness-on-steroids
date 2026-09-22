"""Bounded, local tool loop for the CKFF-backed Sol model.

The model never receives filesystem access directly.  It requests one of the
small tools below; this module validates and executes the request locally,
then sends the result back in the next streamed Chat Completions turn.
"""

from __future__ import annotations

import difflib
import json
import os
import re
import subprocess
import time
import urllib.error
import urllib.request
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[1]


class SolBridgeError(RuntimeError):
    """Raised when the Sol provider or local tool loop cannot continue."""


def _read_env_file(path: Path) -> dict[str, str]:
    """Read a minimal dotenv file without printing or mutating process env."""

    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        if key:
            values[key] = value
    return values


def _setting(env: Mapping[str, str], *names: str, default: str = "") -> str:
    for name in names:
        value = env.get(name, "").strip()
        if value:
            return value
    return default


@dataclass(frozen=True)
class SolConfig:
    """Non-secret provider settings plus the selected CC credential."""

    api_key: str
    base_url: str = "https://ckffai.com/v1"
    backup_base_url: str = "https://aws.ckffai.com/v1"
    model: str = "gpt-5.6-sol"
    timeout_seconds: float = 600.0
    max_rounds: int = 8

    @classmethod
    def from_env(cls, env_path: Path | None = None) -> "SolConfig":
        path = env_path or ROOT / ".env"
        values = _read_env_file(path)
        merged = dict(values)
        for key, value in os.environ.items():
            if value:
                merged[key] = value
        api_key = _setting(merged, "CKFF_CODEX_CC_API_KEY")
        if not api_key:
            raise SolBridgeError(
                "No CKFF CC credential found. Set CKFF_CODEX_CC_API_KEY in the ignored .env."
            )
        try:
            timeout = float(
                _setting(
                    merged,
                    "CKFF_PRIMARY_TIMEOUT_SECONDS",
                    "CKFF_TIMEOUT_SECONDS",
                    default="600",
                )
            )
        except ValueError as exc:
            raise SolBridgeError("CKFF timeout must be numeric") from exc
        try:
            rounds = int(_setting(merged, "SOL_MAX_ROUNDS", default="8"))
        except ValueError as exc:
            raise SolBridgeError("SOL_MAX_ROUNDS must be an integer") from exc
        return cls(
            api_key=api_key,
            base_url=_setting(merged, "CKFF_PRIMARY_BASE_URL", default=cls.base_url),
            backup_base_url=_setting(
                merged, "CKFF_BACKUP_BASE_URL", default=cls.backup_base_url
            ),
            model=_setting(merged, "CKFF_CODEX_MODEL", default=cls.model),
            timeout_seconds=max(1.0, timeout),
            max_rounds=max(1, rounds),
        )


def _sse_data(lines: Iterable[bytes]) -> Iterator[str]:
    data: list[str] = []
    for raw in lines:
        line = raw.decode("utf-8", errors="replace").rstrip("\r\n")
        if not line:
            if data:
                yield "\n".join(data)
                data = []
            continue
        if line.startswith("data:"):
            data.append(line[5:].lstrip())
    if data:
        yield "\n".join(data)


class ChatCompletionsClient:
    """Small streaming client for CKFF's HTTP Chat Completions endpoint."""

    def __init__(self, config: SolConfig) -> None:
        self.config = config
        self.model = config.model

    def stream(
        self, messages: Sequence[Mapping[str, Any]], tools: Sequence[Mapping[str, Any]]
    ) -> Iterator[dict[str, Any]]:
        payload = {
            "model": self.config.model,
            "messages": list(messages),
            "tools": list(tools),
            "tool_choice": "auto",
            "stream": True,
            "reasoning_effort": "xhigh",
        }
        errors: list[str] = []
        for base_url in (self.config.base_url, self.config.backup_base_url):
            yielded = False
            try:
                for chunk in self._stream_once(base_url, payload):
                    yielded = True
                    yield chunk
                return
            except Exception as exc:
                if yielded:
                    raise SolBridgeError(f"CKFF stream failed after data arrived: {exc}") from exc
                errors.append(f"{base_url}: {type(exc).__name__}: {exc}")
        raise SolBridgeError("All CKFF endpoints failed: " + " | ".join(errors))

    def _stream_once(
        self, base_url: str, payload: Mapping[str, Any]
    ) -> Iterator[dict[str, Any]]:
        endpoint = base_url.rstrip("/") + "/chat/completions"
        request = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Accept": "text/event-stream",
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            response = urllib.request.urlopen(request, timeout=self.config.timeout_seconds)
        except urllib.error.HTTPError as exc:
            body = exc.read(2000).decode("utf-8", errors="replace")
            raise SolBridgeError(f"HTTP {exc.code} from {endpoint}: {body}") from exc
        except urllib.error.URLError as exc:
            raise SolBridgeError(f"request failed for {endpoint}: {exc.reason}") from exc

        deadline = time.monotonic() + self.config.timeout_seconds
        try:
            for data in _sse_data(response):
                if time.monotonic() > deadline:
                    raise SolBridgeError("stream exceeded its bounded timeout")
                if data == "[DONE]":
                    return
                try:
                    value = json.loads(data)
                except json.JSONDecodeError as exc:
                    raise SolBridgeError(f"CKFF returned non-JSON SSE data: {data[:300]}") from exc
                if isinstance(value, dict):
                    yield value
        finally:
            response.close()


_PROTECTED_DIRS = {
    ".git",
    ".sol",
    ".venv",
    "__pycache__",
    "data",
    "session_diff",
    "session_share",
}
_PROTECTED_SUFFIXES = {".sqlite", ".db", ".jsonl"}


class RepoTools:
    """Validated repository tools exposed to Sol."""

    def __init__(self, root: Path, *, dry_run: bool = False) -> None:
        self.root = root.resolve()
        self.dry_run = dry_run

    def _path(self, value: str, *, allow_missing: bool = False) -> Path:
        if not value or Path(value).is_absolute():
            raise SolBridgeError("tool path must be a non-empty repository-relative path")
        candidate = (self.root / value).resolve()
        try:
            candidate.relative_to(self.root)
        except ValueError as exc:
            raise SolBridgeError("tool path escapes the repository root") from exc
        relative_parts = candidate.relative_to(self.root).parts
        if any(part in _PROTECTED_DIRS for part in relative_parts):
            raise SolBridgeError("tool path is inside protected local state")
        if candidate.name.startswith(".env") or candidate.suffix.lower() in _PROTECTED_SUFFIXES:
            raise SolBridgeError("tool path is protected from transcript or secret access")
        if not allow_missing and not candidate.is_file():
            raise SolBridgeError(f"file does not exist: {value}")
        return candidate

    def _visible(self, path: Path) -> bool:
        try:
            relative = path.resolve().relative_to(self.root)
        except ValueError:
            return False
        if any(part in _PROTECTED_DIRS for part in relative.parts):
            return False
        return not path.name.startswith(".env") and path.suffix.lower() not in _PROTECTED_SUFFIXES

    def list_files(self, pattern: str = "**/*", limit: int = 200) -> dict[str, Any]:
        limit = max(1, min(limit, 500))
        matches: list[str] = []
        for path in self.root.glob(pattern):
            if path.is_file() and self._visible(path):
                matches.append(path.relative_to(self.root).as_posix())
                if len(matches) >= limit:
                    break
        return {"ok": True, "files": sorted(matches), "truncated": len(matches) >= limit}

    def search(self, query: str, pattern: str = "**/*", regex: bool = False) -> dict[str, Any]:
        if not query or len(query) > 500:
            raise SolBridgeError("search query must be between 1 and 500 characters")
        matcher = re.compile(query) if regex else None
        matches: list[str] = []
        for path in self.root.glob(pattern):
            if not path.is_file() or not self._visible(path):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for line_no, line in enumerate(text.splitlines(), 1):
                found = bool(matcher.search(line)) if matcher else query in line
                if found:
                    rel = path.relative_to(self.root).as_posix()
                    matches.append(f"{rel}:{line_no}:{line[:300]}")
                    if len(matches) >= 100:
                        return {"ok": True, "matches": matches, "truncated": True}
        return {"ok": True, "matches": matches, "truncated": False}

    def read_file(self, path: str, max_bytes: int = 40000) -> dict[str, Any]:
        target = self._path(path)
        max_bytes = max(1, min(max_bytes, 100000))
        raw = target.read_bytes()
        truncated = len(raw) > max_bytes
        return {
            "ok": True,
            "path": path,
            "content": raw[:max_bytes].decode("utf-8", errors="replace"),
            "truncated": truncated,
        }

    def apply_patch(self, patch: str) -> dict[str, Any]:
        if not patch.strip():
            raise SolBridgeError("patch cannot be empty")
        if patch.lstrip().startswith("*** Begin Patch"):
            return self._apply_codex_patch(patch)
        touched: set[str] = set()
        for line in patch.splitlines():
            if line.startswith(("--- ", "+++ ")):
                value = line[4:].split("\t", 1)[0].strip()
                if value not in {"/dev/null", "a/dev/null", "b/dev/null"}:
                    if value.startswith(("a/", "b/")):
                        value = value[2:]
                    self._path(value, allow_missing=True)
                    touched.add(value)
        if not touched:
            raise SolBridgeError("patch did not identify a repository file")
        return self._apply_unified_patch(patch, touched)

    def _apply_codex_patch(self, patch: str) -> dict[str, Any]:
        """Translate the common Codex patch envelope into a git patch."""

        lines = patch.splitlines()
        if not lines or lines[0].strip() != "*** Begin Patch":
            raise SolBridgeError("invalid Codex patch envelope")
        changes: list[tuple[str, str, str]] = []
        index = 1
        while index < len(lines):
            header = lines[index]
            if header.strip() == "*** End Patch":
                break
            match = re.fullmatch(r"\*\*\* (Update|Add|Delete) File: (.+)", header)
            if not match:
                raise SolBridgeError(f"unsupported Codex patch header: {header}")
            operation, raw_path = match.groups()
            target = self._path(raw_path.strip(), allow_missing=True)
            if operation == "Add" and target.exists():
                raise SolBridgeError(f"Codex Add File already exists: {raw_path.strip()}")
            relative = target.relative_to(self.root).as_posix()
            original = target.read_text(encoding="utf-8") if target.is_file() else ""
            index += 1
            body: list[str] = []
            while index < len(lines) and not lines[index].startswith("*** "):
                body.append(lines[index])
                index += 1
            if operation == "Add":
                new_text = "\n".join(line[1:] for line in body if line.startswith("+"))
                if body and new_text:
                    new_text += "\n"
            elif operation == "Delete":
                new_text = ""
            else:
                new_text = self._apply_codex_hunks(original, body, relative)
            changes.append((relative, original, new_text))
        if not changes:
            raise SolBridgeError("Codex patch contained no file operation")
        unified: list[str] = []
        for relative, original, new_text in changes:
            old_lines = original.splitlines()
            new_lines = new_text.splitlines()
            from_name = f"a/{relative}" if original else "/dev/null"
            to_name = f"b/{relative}" if new_text else "/dev/null"
            unified.extend(
                difflib.unified_diff(
                    old_lines,
                    new_lines,
                    fromfile=from_name,
                    tofile=to_name,
                    n=max(len(old_lines), len(new_lines), 1),
                    lineterm="",
                )
            )
        return self._apply_unified_patch(
            "\n".join(unified) + "\n", {c[0] for c in changes}, changes
        )

    @staticmethod
    def _apply_codex_hunks(original: str, body: list[str], relative: str) -> str:
        lines = original.splitlines()
        had_final_newline = original.endswith(("\n", "\r"))
        hunks: list[list[str]] = []
        current: list[str] = []
        for line in body:
            if line.startswith("@@"):
                if current:
                    hunks.append(current)
                    current = []
                continue
            if line.startswith((" ", "+", "-")):
                current.append(line)
            elif line:
                raise SolBridgeError(f"unsupported Codex patch line for {relative}: {line}")
        if current:
            hunks.append(current)
        if not hunks:
            raise SolBridgeError(f"Codex update has no hunk for {relative}")
        for hunk in hunks:
            old = [line[1:] for line in hunk if line.startswith((" ", "-"))]
            new = [line[1:] for line in hunk if line.startswith((" ", "+"))]
            if not old:
                lines[0:0] = new
                continue
            start = next(
                (
                    position
                    for position in range(len(lines) - len(old) + 1)
                    if lines[position : position + len(old)] == old
                ),
                -1,
            )
            if start < 0:
                raise SolBridgeError(f"Codex hunk did not match {relative}")
            lines[start : start + len(old)] = new
        result = "\n".join(lines)
        return result + ("\n" if had_final_newline else "")

    def _apply_unified_patch(
        self,
        patch: str,
        touched: set[str],
        changes: list[tuple[str, str, str]] | None = None,
    ) -> dict[str, Any]:
        if self.dry_run:
            return {"ok": True, "dry_run": True, "would_touch": sorted(touched)}
        checked = subprocess.run(
            ["git", "apply", "--check", "--whitespace=nowarn", "-"],
            cwd=self.root,
            input=patch,
            text=True,
            capture_output=True,
            timeout=60,
            check=False,
        )
        if checked.returncode:
            if changes and all(not self._is_tracked(relative) for relative, _, _ in changes):
                return self._apply_untracked_changes(changes)
            return {
                "ok": False,
                "stage": "check",
                "output": (checked.stderr or checked.stdout)[-4000:],
            }
        applied = subprocess.run(
            ["git", "apply", "--whitespace=nowarn", "-"],
            cwd=self.root,
            input=patch,
            text=True,
            capture_output=True,
            timeout=60,
            check=False,
        )
        return {
            "ok": applied.returncode == 0,
            "stage": "apply",
            "touched": sorted(touched),
            "output": (applied.stderr or applied.stdout)[-4000:],
        }

    def _is_tracked(self, relative: str) -> bool:
        result = subprocess.run(
            ["git", "ls-files", "--error-unmatch", "--", relative],
            cwd=self.root,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        return result.returncode == 0

    def _apply_untracked_changes(
        self, changes: list[tuple[str, str, str]]
    ) -> dict[str, Any]:
        for relative, original, _ in changes:
            target = self._path(relative, allow_missing=True)
            current = target.read_text(encoding="utf-8") if target.is_file() else ""
            if current != original:
                return {
                    "ok": False,
                    "stage": "untracked-check",
                    "output": f"file changed after inspection: {relative}",
                }
        for relative, _, new_text in changes:
            target = self._path(relative, allow_missing=True)
            if not new_text:
                if target.exists():
                    target.unlink()
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(new_text, encoding="utf-8")
        return {
            "ok": True,
            "stage": "untracked-direct",
            "touched": sorted(relative for relative, _, _ in changes),
        }

    def git_diff(self, path: str = "") -> dict[str, Any]:
        args = ["git", "diff", "--stat", "--"]
        if path:
            safe = self._path(path, allow_missing=True)
            args.append(str(safe.relative_to(self.root)))
        proc = subprocess.run(
            args, cwd=self.root, capture_output=True, text=True, timeout=60, check=False
        )
        return {"ok": proc.returncode == 0, "output": (proc.stdout or proc.stderr)[-12000:]}

    def run_checks(self, commands: list[list[str]] | None = None) -> dict[str, Any]:
        requested = commands or [["python", "-m", "pytest", "-q"]]
        results: list[dict[str, Any]] = []
        for command in requested[:4]:
            self._validate_check(command)
            if self.dry_run:
                results.append({"ok": True, "dry_run": True, "command": command})
                continue
            try:
                proc = subprocess.run(
                    command,
                    cwd=self.root,
                    capture_output=True,
                    text=True,
                    timeout=120,
                    check=False,
                )
                results.append(
                    {
                        "ok": proc.returncode == 0,
                        "command": command,
                        "returncode": proc.returncode,
                        "output": ((proc.stdout or "") + (proc.stderr or ""))[-6000:],
                    }
                )
            except subprocess.TimeoutExpired:
                results.append({"ok": False, "command": command, "error": "check timed out"})
        return {"ok": all(result["ok"] for result in results), "results": results}

    @staticmethod
    def _validate_check(command: list[str]) -> None:
        if not command:
            raise SolBridgeError("check command cannot be empty")
        executable = Path(command[0]).name.lower()
        if executable in {"python", "python.exe", "py", "py.exe"}:
            if len(command) < 3 or command[1:3] != ["-m", "pytest"]:
                raise SolBridgeError("Python checks are limited to python -m pytest")
        elif executable not in {"ruff", "ruff.exe", "mypy", "mypy.exe"}:
            raise SolBridgeError("check executable is not allow-listed")


TOOL_DEFINITIONS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List visible repository files matching a glob.",
            "parameters": {
                "type": "object",
                "properties": {"pattern": {"type": "string"}, "limit": {"type": "integer"}},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "Search visible text files for a literal or regular expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "pattern": {"type": "string"},
                    "regex": {"type": "boolean"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a bounded UTF-8 text file by repository-relative path.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}, "max_bytes": {"type": "integer"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "apply_patch",
            "description": (
                "Apply a unified git patch to visible repository files after validation."
            ),
            "parameters": {
                "type": "object",
                "properties": {"patch": {"type": "string"}},
                "required": ["patch"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "git_diff",
            "description": "Show a bounded summary of current repository changes.",
            "parameters": {"type": "object", "properties": {"path": {"type": "string"}}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_checks",
            "description": "Run allow-listed repository checks, each with a hard local timeout.",
            "parameters": {
                "type": "object",
                "properties": {
                    "commands": {
                        "type": "array",
                        "items": {"type": "array", "items": {"type": "string"}},
                    }
                },
            },
        },
    },
]


SYSTEM_PROMPT = """You are Sol, the project's bounded reasoning and verification partner.
Work on exactly the user task supplied in this run. Inspect before proposing changes.
Use small tool calls and keep the task granular. Never claim an edit succeeded until
you inspect the resulting diff and run an appropriate check. Use apply_patch for edits.
Do not request secrets, raw transcripts, databases, or files outside the repository.
Finish with a concise evidence-based report of changes, checks, and any remaining risk.
"""


class RunRecorder:
    """Append-only local record; the directory is ignored and never committed."""

    def __init__(self, root: Path, run_id: str | None = None) -> None:
        self.run_id = run_id or uuid.uuid4().hex[:12]
        self.path = root / ".sol" / "runs" / f"{self.run_id}.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def add(self, event: str, **data: Any) -> None:
        record = {"time": time.time(), "event": event, **data}
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


@dataclass(frozen=True)
class SolResult:
    run_id: str
    rounds: int
    final_text: str
    tool_calls: int
    record_path: Path


class SolBridge:
    """Run Sol with a local, bounded tool executor."""

    def __init__(
        self,
        root: Path,
        client: Any,
        *,
        max_rounds: int = 8,
        dry_run: bool = False,
        recorder: RunRecorder | None = None,
    ) -> None:
        self.root = root.resolve()
        self.client = client
        self.max_rounds = max(1, max_rounds)
        self.tools = RepoTools(self.root, dry_run=dry_run)
        self.recorder = recorder or RunRecorder(self.root)

    def run(self, task: str) -> SolResult:
        if not task.strip():
            raise SolBridgeError("task cannot be empty")
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": task.strip()},
        ]
        calls = 0
        self.recorder.add(
            "run_started", task=task.strip(), model=getattr(self.client, "model", None)
        )
        for round_number in range(1, self.max_rounds + 1):
            assistant, tool_calls = self._collect_assistant(messages)
            messages.append(assistant)
            self.recorder.add("assistant_turn", round=round_number, assistant=assistant)
            if not tool_calls:
                final = str(assistant.get("content") or "").strip()
                self.recorder.add("run_finished", round=round_number, tool_calls=calls)
                return SolResult(
                    self.recorder.run_id, round_number, final, calls, self.recorder.path
                )
            for call in tool_calls:
                calls += 1
                result = self._dispatch(call["name"], call["arguments"])
                self.recorder.add(
                    "tool_result",
                    round=round_number,
                    name=call["name"],
                    arguments=call["arguments"],
                    result=result,
                )
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call["id"],
                        "content": json.dumps(result, ensure_ascii=False),
                    }
                )
        self.recorder.add(
            "run_stopped", reason="round_limit", rounds=self.max_rounds, tool_calls=calls
        )
        raise SolBridgeError(f"Sol reached the {self.max_rounds}-round limit before finishing")

    def _collect_assistant(
        self, messages: Sequence[Mapping[str, Any]]
    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        content: list[str] = []
        calls: dict[int, dict[str, str]] = {}
        for chunk in self.client.stream(messages, TOOL_DEFINITIONS):
            choice = (chunk.get("choices") or [{}])[0]
            delta = choice.get("delta") or choice.get("message") or {}
            if isinstance(delta.get("content"), str):
                content.append(delta["content"])
            for raw_call in delta.get("tool_calls") or []:
                index = int(raw_call.get("index", 0))
                item = calls.setdefault(index, {"id": "", "name": "", "arguments": ""})
                item["id"] += str(raw_call.get("id") or "")
                function = raw_call.get("function") or {}
                item["name"] += str(function.get("name") or "")
                item["arguments"] += str(function.get("arguments") or "")
        tool_calls = []
        encoded_calls = []
        for index in sorted(calls):
            item = calls[index]
            try:
                arguments = json.loads(item["arguments"] or "{}")
            except json.JSONDecodeError as exc:
                arguments = {"_parse_error": f"invalid tool arguments: {exc}"}
            tool_calls.append(
                {
                    "id": item["id"] or f"sol-call-{index}",
                    "name": item["name"],
                    "arguments": arguments,
                }
            )
            encoded_calls.append(
                {
                    "id": item["id"] or f"sol-call-{index}",
                    "type": "function",
                    "function": {"name": item["name"], "arguments": item["arguments"] or "{}"},
                }
            )
        assistant: dict[str, Any] = {"role": "assistant", "content": "".join(content) or None}
        if encoded_calls:
            assistant["tool_calls"] = encoded_calls
        return assistant, tool_calls

    def _dispatch(self, name: str, arguments: Any) -> dict[str, Any]:
        if not isinstance(arguments, dict):
            return {"ok": False, "error": "tool arguments must be an object"}
        if "_parse_error" in arguments:
            return {"ok": False, "error": arguments["_parse_error"]}
        method: Callable[..., dict[str, Any]] | None = getattr(self.tools, name, None)
        if method is None or name.startswith("_"):
            return {"ok": False, "error": f"unknown tool: {name}"}
        try:
            return method(**arguments)
        except (OSError, SolBridgeError, subprocess.SubprocessError) as exc:
            return {"ok": False, "error": str(exc)}


def run_task(
    task: str,
    *,
    root: Path = ROOT,
    env_path: Path | None = None,
    max_rounds: int | None = None,
    dry_run: bool = False,
) -> SolResult:
    config = SolConfig.from_env(env_path)
    client = ChatCompletionsClient(config)
    bridge = SolBridge(
        root,
        client,
        max_rounds=max_rounds or config.max_rounds,
        dry_run=dry_run,
    )
    return bridge.run(task)

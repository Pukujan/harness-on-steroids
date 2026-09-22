"""Source adapters for the two currently imported transcript families."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from .model import CanonicalEvent, stable_id

TOOL_ALIASES = {
    "exec_command": "execute",
    "shell_command": "execute",
    "run": "execute",
    "read_file": "inspect",
    "search": "inspect",
    "grep": "inspect",
    "glob": "inspect",
    "list_files": "inspect",
    "apply_patch": "mutate",
    "write_file": "mutate",
    "edit": "mutate",
    "pytest": "verify",
    "run_checks": "verify",
    "test": "verify",
    "spawn_agent": "delegate",
    "send_message": "delegate",
    "wait_agent": "wait",
    "wait": "wait",
    "web_search": "research",
    "web_search_call": "research",
}


def tool_family(name: str | None) -> str | None:
    if not name:
        return None
    normalized = name.lower().strip()
    if normalized in TOOL_ALIASES:
        return TOOL_ALIASES[normalized]
    if any(token in normalized for token in ("read", "search", "grep", "glob", "list", "inspect")):
        return "inspect"
    if any(token in normalized for token in ("patch", "write", "edit", "delete", "move")):
        return "mutate"
    if any(token in normalized for token in ("test", "check", "lint", "format", "diff")):
        return "verify"
    if any(token in normalized for token in ("agent", "task", "thread", "delegate")):
        return "delegate"
    if any(token in normalized for token in ("wait", "sleep", "background")):
        return "wait"
    return "other"


def _scalar_attributes(**values: Any) -> dict[str, str | int | float | bool | None]:
    """Keep only bounded scalar metadata; never copy text or nested payloads."""

    result: dict[str, str | int | float | bool | None] = {}
    for key, value in values.items():
        if isinstance(value, (str, int, float, bool)) or value is None:
            result[key] = value
    return result


def _content_length(value: Any) -> int | None:
    if isinstance(value, str):
        return len(value)
    if isinstance(value, list):
        lengths = [_content_length(item.get("text")) for item in value if isinstance(item, dict)]
        known = [length for length in lengths if length is not None]
        return sum(known) if known else None
    if isinstance(value, dict):
        return _content_length(value.get("text"))
    return None


def _chat_episode(path: Path) -> str:
    parts = list(path.parts)
    if "conversations" in parts:
        index = parts.index("conversations")
        if index + 1 < len(parts):
            return stable_id("chat", parts[index + 1])
    return stable_id("chat-file", path.as_posix())


def _codex_episode(path: Path, payload: dict[str, Any]) -> str:
    session_id = payload.get("session_id") or payload.get("id")
    return stable_id("codex", session_id or path.stem)


def _chat_event(
    record: dict[str, Any], path: Path, line_no: int, source_id: str, episode_id: str
) -> CanonicalEvent:
    event_class = str(record.get("class") or record.get("event_class") or "unknown")
    if event_class == "message.user":
        kind, subtype, actor = "message", "user", "user"
    elif event_class == "message.assistant":
        kind, subtype, actor = "message", "assistant", "assistant"
    elif event_class == "citation":
        kind, subtype, actor = "citation", "citation", "assistant"
    elif event_class == "tool.call":
        kind, subtype, actor = (
            "tool_call",
            "tool_call",
            str(record.get("author_role") or "assistant"),
        )
    elif event_class == "tool.result":
        kind, subtype, actor = "tool_result", "tool_result", "tool"
    else:
        kind, subtype, actor = "unknown", event_class, str(record.get("author_role") or "unknown")
    metadata_raw = record.get("metadata")
    metadata: dict[str, Any] = metadata_raw if isinstance(metadata_raw, dict) else {}
    content_raw = record.get("content")
    content: dict[str, Any] = content_raw if isinstance(content_raw, dict) else {}
    tool_name = (
        metadata.get("invoked_plugin")
        or metadata.get("invoked_resource")
        or record.get("recipient")
    )
    if not isinstance(tool_name, str):
        tool_name = None
    record_key = record.get("message_id") or record.get("node_id") or f"{event_class}:{line_no}"
    return CanonicalEvent(
        event_id=stable_id(source_id, record_key, event_class),
        source_id=source_id,
        episode_id=episode_id,
        lane="chatgpt_chat",
        ordinal=line_no,
        kind=kind,
        actor=actor,
        timestamp=str(record.get("create_time")) if record.get("create_time") is not None else None,
        subtype=subtype,
        tool_name=tool_name,
        tool_family=tool_family(tool_name),
        status=str(record.get("status")) if record.get("status") is not None else None,
        observation="observed",
        source_pointer=f"{path.as_posix()}:{line_no}",
        attributes=_scalar_attributes(
            content_type=record.get("content_type") or content.get("content_type"),
            content_chars=_content_length(content),
            has_citation=event_class == "citation",
        ),
    )


def _codex_event(
    record: dict[str, Any], path: Path, line_no: int, source_id: str, episode_id: str
) -> CanonicalEvent:
    record_type = str(record.get("type") or "unknown")
    payload_raw = record.get("payload")
    payload: dict[str, Any] = payload_raw if isinstance(payload_raw, dict) else {}
    payload_type = str(payload.get("type") or record_type)
    kind = "unknown"
    actor = str(payload.get("role") or "system")
    subtype = payload_type
    tool_name: str | None = None
    observation = "observed"
    if record_type == "session_meta":
        kind, subtype = "lifecycle", "session_meta"
    elif record_type == "turn_context":
        kind, subtype = "context", "turn_context"
    elif record_type == "compacted":
        kind, subtype = "compaction", "compacted"
    elif record_type == "event_msg":
        kind, subtype = "lifecycle", payload_type
    elif record_type == "response_item":
        if payload_type == "message":
            kind = "message"
        elif payload_type == "reasoning":
            kind = "reasoning"
        elif payload_type in {"function_call", "custom_tool_call"}:
            kind, observation = "tool_call", "not_observed"
            tool_name = str(payload.get("name")) if payload.get("name") is not None else None
        elif payload_type in {"function_call_output", "custom_tool_call_output"}:
            kind = "tool_result"
            tool_name = str(payload.get("name")) if payload.get("name") is not None else None
        elif payload_type == "web_search_call":
            kind = "research"
        else:
            kind = "response_item"
    record_key = payload.get("id") or payload.get("call_id") or record.get("ordinal") or line_no
    return CanonicalEvent(
        event_id=stable_id(source_id, record_key, record_type, payload_type),
        source_id=source_id,
        episode_id=episode_id,
        lane="codex",
        ordinal=int(record.get("ordinal", line_no)),
        kind=kind,
        actor=actor,
        timestamp=str(record.get("timestamp")) if record.get("timestamp") is not None else None,
        subtype=subtype,
        tool_name=tool_name,
        tool_family=tool_family(tool_name),
        status=str(payload.get("status")) if payload.get("status") is not None else None,
        observation=observation,
        source_pointer=f"{path.as_posix()}:{line_no}",
        attributes=_scalar_attributes(
            record_type=record_type,
            content_chars=_content_length(payload.get("content")),
            has_output=payload_type.endswith("_output"),
            call_id=payload.get("call_id"),
        ),
    )


def normalize_jsonl(
    path: Path, *, lane: str = "auto", source_id: str | None = None
) -> list[CanonicalEvent]:
    """Normalize one JSONL file without retaining body text."""

    resolved_lane = lane
    if resolved_lane == "auto":
        resolved_lane = (
            "chatgpt_chat"
            if path.name in {"messages.jsonl", "tool-events.jsonl"}
            else "codex"
        )
    source = source_id or stable_id("source", path.as_posix())
    events: list[CanonicalEvent] = []
    episode = _chat_episode(path) if resolved_lane == "chatgpt_chat" else None
    with path.open(encoding="utf-8", errors="replace") as handle:
        for line_no, line in enumerate(handle, 1):
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                events.append(
                    CanonicalEvent(
                        event_id=stable_id(source, line_no, "parse_error"),
                        source_id=source,
                        episode_id=episode or stable_id("codex-file", path.stem),
                        lane=resolved_lane,
                        ordinal=line_no,
                        kind="parse_error",
                        actor="system",
                        subtype="invalid_json",
                        observation="unknown",
                        source_pointer=f"{path.as_posix()}:{line_no}",
                    )
                )
                continue
            if not isinstance(record, dict):
                continue
            if resolved_lane == "chatgpt_chat":
                events.append(_chat_event(record, path, line_no, source, episode or source))
            else:
                payload_raw = record.get("payload")
                payload: dict[str, Any] = (
                    payload_raw if isinstance(payload_raw, dict) else {}
                )
                events.append(
                    _codex_event(record, path, line_no, source, _codex_episode(path, payload))
                )
    return events


def jsonl_paths(inputs: Iterable[Path]) -> list[Path]:
    """Expand files/directories deterministically to JSONL inputs."""

    paths: list[Path] = []
    for value in inputs:
        if value.is_file() and value.suffix.lower() == ".jsonl":
            paths.append(value)
        elif value.is_dir():
            paths.extend(path for path in value.rglob("*.jsonl") if path.is_file())
    return sorted(set(paths), key=lambda item: item.as_posix())

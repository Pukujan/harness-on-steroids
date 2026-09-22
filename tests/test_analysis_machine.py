from __future__ import annotations

import json
from pathlib import Path

from src.hos.analysis_machine import (
    analyze_events,
    export_stream,
    iter_normalized_jsonl,
    normalize_jsonl,
    validate_event,
)
from src.hos.analysis_machine.model import CanonicalEvent


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8"
    )


def test_normalizes_both_lanes_without_body_text(tmp_path: Path) -> None:
    codex = tmp_path / "codex.jsonl"
    _write_jsonl(
        codex,
        [
            {"type": "session_meta", "ordinal": 0, "payload": {"session_id": "s1"}},
            {
                "type": "response_item",
                "ordinal": 1,
                "payload": {"type": "function_call", "name": "read_file", "call_id": "c1"},
            },
            {
                "type": "response_item",
                "ordinal": 2,
                "payload": {"type": "function_call_output", "call_id": "c1", "output": "secret"},
            },
            {
                "type": "response_item",
                "ordinal": 3,
                "payload": {"type": "function_call", "name": "apply_patch", "call_id": "c2"},
            },
        ],
    )
    chat = tmp_path / "messages.jsonl"
    _write_jsonl(
        chat,
        [
            {
                "class": "message.user",
                "message_id": "m1",
                "author_role": "user",
                "content": {"content_type": "text", "text": "private ask"},
            },
            {
                "class": "message.assistant",
                "message_id": "m2",
                "author_role": "assistant",
                "content": {"content_type": "text", "text": "private answer"},
            },
        ],
    )

    codex_events = normalize_jsonl(codex, lane="codex", source_id="codex-source")
    chat_events = normalize_jsonl(chat, lane="chatgpt_chat", source_id="chat-source")
    assert all("secret" not in json.dumps(event.to_dict()) for event in codex_events)
    summary = analyze_events([*codex_events, *chat_events])
    assert summary["lane_counts"] == {"chatgpt_chat": 2, "codex": 4}
    assert summary["lanes"]["codex"]["inspection_before_mutation_rate"] == 1.0
    assert summary["lanes"]["chatgpt_chat"]["assistant_messages"] == 1


def test_summary_is_independent_of_event_input_order() -> None:
    events = [
        CanonicalEvent("a", "source", "episode", "codex", 2, "tool_result", "tool"),
        CanonicalEvent(
            "b",
            "source",
            "episode",
            "codex",
            1,
            "tool_call",
            "assistant",
            tool_name="read_file",
            tool_family="inspect",
        ),
    ]
    assert analyze_events(events) == analyze_events(reversed(events))


def test_unknown_fields_and_tool_aliases_do_not_change_structural_summary(tmp_path: Path) -> None:
    first = tmp_path / "first.jsonl"
    second = tmp_path / "second.jsonl"
    base = {
        "type": "response_item",
        "ordinal": 1,
        "payload": {"type": "function_call", "name": "exec_command", "call_id": "c1"},
    }
    changed = {
        **base,
        "future_field": {"private": "body"},
        "payload": {**base["payload"], "future_payload_field": "ignored"},
    }
    _write_jsonl(first, [base])
    _write_jsonl(second, [changed])
    left = analyze_events(normalize_jsonl(first, lane="codex", source_id="same"))
    right = analyze_events(normalize_jsonl(second, lane="codex", source_id="same"))
    assert left["kind_counts"] == right["kind_counts"]
    assert left["lanes"]["codex"]["first_tool_family"] == {"execute": 1}
    assert right["lanes"]["codex"]["first_tool_family"] == {"execute": 1}


def test_contract_rejects_invalid_event() -> None:
    event = CanonicalEvent("", "", "", "bad", -1, "tool_call", "assistant")
    codes = {issue.code for issue in validate_event(event)}
    assert {
        "missing_id",
        "missing_source",
        "missing_episode",
        "invalid_lane",
        "negative_ordinal",
    } <= codes


def test_streaming_export_matches_materialized_summary(tmp_path: Path) -> None:
    source = tmp_path / "source.jsonl"
    _write_jsonl(
        source,
        [
            {
                "type": "response_item",
                "ordinal": 1,
                "payload": {"type": "function_call", "name": "read_file", "call_id": "c1"},
            },
            {
                "type": "response_item",
                "ordinal": 2,
                "payload": {"type": "function_call", "name": "apply_patch", "call_id": "c2"},
            },
        ],
    )
    materialized = normalize_jsonl(source, lane="codex", source_id="same")
    streamed = list(iter_normalized_jsonl(source, lane="codex", source_id="same"))
    assert analyze_events(materialized) == analyze_events(streamed)
    summary = export_stream(iter(streamed), tmp_path / "export", source_count=1)
    assert summary["event_count"] == 2
    manifest = json.loads((tmp_path / "export" / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["streaming"] is True
    assert manifest["events_exported"] is True
    assert manifest["codebook_version"] == "analysis-codebook/0.1.0"


def test_streaming_summary_only_does_not_write_events(tmp_path: Path) -> None:
    event = CanonicalEvent("a", "source", "episode", "codex", 1, "context", "system")
    output = tmp_path / "summary-only"
    (output).mkdir()
    (output / "events.jsonl").write_text("stale\n", encoding="utf-8")
    export_stream(iter((event,)), output, source_count=1, write_events=False)
    assert not (output / "events.jsonl").exists()
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["events_exported"] is False


def test_codex_session_id_carries_across_records(tmp_path: Path) -> None:
    source = tmp_path / "session.jsonl"
    _write_jsonl(
        source,
        [
            {"type": "session_meta", "payload": {"session_id": "s1"}},
            {
                "type": "response_item",
                "ordinal": 1,
                "payload": {"type": "function_call", "name": "read_file", "call_id": "c1"},
            },
            {
                "type": "response_item",
                "ordinal": 2,
                "payload": {"type": "function_call", "name": "apply_patch", "call_id": "c2"},
            },
        ],
    )
    events = normalize_jsonl(source, lane="codex", source_id="stable-source")
    assert len({event.episode_id for event in events}) == 1
    assert analyze_events(events)["lanes"]["codex"]["inspection_before_mutation_rate"] == 1.0


def test_malformed_jsonl_records_become_bounded_parse_events(tmp_path: Path) -> None:
    source = tmp_path / "malformed.jsonl"
    source.write_text(
        "null\n"
        + json.dumps({"type": "response_item", "ordinal": "not-a-number"})
        + "\n",
        encoding="utf-8",
    )
    events = normalize_jsonl(source, lane="codex", source_id="stable-source")
    assert [event.kind for event in events] == ["parse_error", "parse_error"]
    assert {event.subtype for event in events} == {"invalid_record", "invalid_ordinal"}


def test_analysis_run_id_includes_event_fingerprint(tmp_path: Path) -> None:
    first = CanonicalEvent("first", "source", "episode", "codex", 1, "context", "system")
    second = CanonicalEvent("second", "source", "episode", "codex", 1, "context", "system")
    first_dir = tmp_path / "first"
    second_dir = tmp_path / "second"
    export_stream(iter((first,)), first_dir, source_count=1)
    export_stream(iter((second,)), second_dir, source_count=1)
    first_manifest = json.loads((first_dir / "manifest.json").read_text(encoding="utf-8"))
    second_manifest = json.loads((second_dir / "manifest.json").read_text(encoding="utf-8"))
    assert first_manifest["analysis_run_id"] != second_manifest["analysis_run_id"]
    assert first_manifest["event_fingerprint"] != second_manifest["event_fingerprint"]


def test_chat_episode_count_and_citation_denominator_are_explicit(tmp_path: Path) -> None:
    source = tmp_path / "messages.jsonl"
    _write_jsonl(
        source,
        [
            {"class": "message.user", "message_id": "u1"},
            {"class": "message.assistant", "message_id": "a1"},
            {"class": "citation", "message_id": "c1", "field": "citations"},
            {"class": "citation", "message_id": "c1", "field": "content_references"},
        ],
    )
    summary = analyze_events(normalize_jsonl(source, lane="chatgpt_chat", source_id="chat"))
    chat = summary["lanes"]["chatgpt_chat"]
    assert chat["episode_count"] == 1
    assert chat["assistant_episode_count"] == 1
    assert chat["citation_presence_denominator"] == 1
    assert chat["citation_presence_rate"] == 1.0
    assert summary["validation_issue_count"] == 0

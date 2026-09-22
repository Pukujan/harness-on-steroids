"""Deterministic lane analyzers and export format."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from .model import CONTRACT_VERSION, ONTOLOGY_VERSION, CanonicalEvent, event_sort_key
from .validate import validate_events

ANALYZER_VERSION = "analysis-machine/0.1.0"


def _rate(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def _episodes(events: Iterable[CanonicalEvent]) -> dict[str, list[CanonicalEvent]]:
    grouped: dict[str, list[CanonicalEvent]] = defaultdict(list)
    for event in sorted(events, key=event_sort_key):
        grouped[event.episode_id].append(event)
    return dict(grouped)


def _codex_summary(events: list[CanonicalEvent]) -> dict[str, Any]:
    episodes = _episodes(event for event in events if event.lane == "codex")
    first_tools: Counter[str] = Counter()
    inspection_before_mutation = 0
    verification_after_mutation = 0
    mutation_episodes = 0
    tool_calls = 0
    tool_results = 0
    delegation_events = 0
    compactions = 0
    for sequence in episodes.values():
        calls = [event for event in sequence if event.kind == "tool_call"]
        results = [event for event in sequence if event.kind == "tool_result"]
        tool_calls += len(calls)
        tool_results += len(results)
        if calls:
            first_tools[calls[0].tool_family or "unknown"] += 1
        mutation_indexes = [
            index for index, event in enumerate(sequence) if event.tool_family == "mutate"
        ]
        inspect_indexes = [
            index for index, event in enumerate(sequence) if event.tool_family == "inspect"
        ]
        verify_indexes = [
            index for index, event in enumerate(sequence) if event.tool_family == "verify"
        ]
        if mutation_indexes:
            mutation_episodes += 1
            if inspect_indexes and min(inspect_indexes) < min(mutation_indexes):
                inspection_before_mutation += 1
            if verify_indexes and max(verify_indexes) > min(mutation_indexes):
                verification_after_mutation += 1
        delegation_events += sum(event.tool_family == "delegate" for event in sequence)
        compactions += sum(event.kind == "compaction" for event in sequence)
    return {
        "episode_count": len(episodes),
        "tool_calls": tool_calls,
        "tool_results": tool_results,
        "tool_result_rate": _rate(tool_results, tool_calls),
        "first_tool_family": dict(sorted(first_tools.items())),
        "mutation_episodes": mutation_episodes,
        "inspection_before_mutation": inspection_before_mutation,
        "inspection_before_mutation_rate": _rate(inspection_before_mutation, mutation_episodes),
        "verification_after_mutation": verification_after_mutation,
        "verification_after_mutation_rate": _rate(verification_after_mutation, mutation_episodes),
        "delegation_events": delegation_events,
        "compactions": compactions,
    }


def _chat_summary(events: list[CanonicalEvent]) -> dict[str, Any]:
    chat_events = [event for event in events if event.lane == "chatgpt_chat"]
    episodes = _episodes(chat_events)
    counts = Counter(event.kind for event in chat_events)
    assistant_episodes = {
        episode_id
        for episode_id, sequence in episodes.items()
        if any(event.kind == "message" and event.actor == "assistant" for event in sequence)
    }
    citation_episodes = {
        event.episode_id for event in chat_events if event.kind == "citation"
    }
    return {
        "episode_count": len(episodes),
        "user_messages": sum(
            event.kind == "message" and event.actor == "user" for event in chat_events
        ),
        "assistant_messages": sum(
            event.kind == "message" and event.actor == "assistant" for event in chat_events
        ),
        "tool_calls": counts["tool_call"],
        "tool_results": counts["tool_result"],
        "citations": counts["citation"],
        "research_events": counts["research"],
        "execution_output_events": sum(
            event.attributes.get("content_type") == "execution_output" for event in chat_events
        ),
        "code_events": sum(event.attributes.get("content_type") == "code" for event in chat_events),
        "citation_presence_rate": _rate(len(citation_episodes), len(assistant_episodes)),
        "known_message_or_tool_rate": _rate(
            sum(
                event.kind in {"message", "tool_call", "tool_result", "citation"}
                for event in chat_events
            ),
            len(chat_events),
        ),
    }


def analyze_events(events: Iterable[CanonicalEvent]) -> dict[str, Any]:
    """Return a versioned, body-free summary for both lanes."""

    materialized = list(events)
    issues = validate_events(materialized)
    lane_counts = Counter(event.lane for event in materialized)
    kind_counts = Counter(event.kind for event in materialized)
    issue_counts = Counter(issue.code for issue in issues)
    known = sum(event.kind not in {"unknown", "parse_error"} for event in materialized)
    return {
        "contract_version": CONTRACT_VERSION,
        "ontology_version": ONTOLOGY_VERSION,
        "analyzer_version": ANALYZER_VERSION,
        "event_count": len(materialized),
        "episode_count": len({event.episode_id for event in materialized}),
        "lane_counts": dict(sorted(lane_counts.items())),
        "kind_counts": dict(sorted(kind_counts.items())),
        "unknown_or_parse_error_count": len(materialized) - known,
        "known_event_rate": _rate(known, len(materialized)),
        "validation_issue_count": len(issues),
        "validation_issue_counts": dict(sorted(issue_counts.items())),
        "lanes": {
            "codex": _codex_summary(materialized),
            "chatgpt_chat": _chat_summary(materialized),
        },
    }


def export_bundle(
    events: Iterable[CanonicalEvent], output_dir: Path, *, source_count: int | None = None
) -> dict[str, Any]:
    """Write a reproducible local export: manifest, normalized events, and summary."""

    materialized = sorted(list(events), key=event_sort_key)
    summary = analyze_events(materialized)
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "events.jsonl").open("w", encoding="utf-8", newline="\n") as handle:
        for event in materialized:
            handle.write(json.dumps(event.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    manifest = {
        "contract_version": CONTRACT_VERSION,
        "ontology_version": ONTOLOGY_VERSION,
        "analyzer_version": ANALYZER_VERSION,
        "event_count": len(materialized),
        "source_count": source_count,
        "body_policy": "no transcript bodies are written",
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return summary

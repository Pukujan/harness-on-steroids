"""Deterministic lane analyzers and export format."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from .model import (
    CODEBOOK_VERSION,
    CONTRACT_VERSION,
    ONTOLOGY_VERSION,
    CanonicalEvent,
    event_sort_key,
    stable_id,
)
from .validate import validate_events

ANALYZER_VERSION = "analysis-machine/0.2.0"


def _rate(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


class StreamingAnalyzer:
    """Bounded-state analyzer for large exports.

    It keeps per-episode counters and first/last ordinal markers, never the
    transcript body or the complete event list.
    """

    def __init__(self, *, duplicate_tracking_limit: int = 250_000) -> None:
        self.event_count = 0
        self.episode_ids: set[str] = set()
        self.lane_counts: Counter[str] = Counter()
        self.kind_counts: Counter[str] = Counter()
        self.unknown_subtypes: Counter[str] = Counter()
        self.issue_counts: Counter[str] = Counter()
        self.seen_ids: set[str] = set()
        self.duplicate_tracking_limit = max(0, duplicate_tracking_limit)
        self.duplicate_tracking_complete = True
        self.duplicate_checks_skipped = 0
        self.known_count = 0
        self.codex: dict[str, dict[str, Any]] = {}
        self.chat_assistant_episodes: set[str] = set()
        self.chat_episode_ids: set[str] = set()
        self.chat_citation_episodes: set[str] = set()
        self.chat_counts: Counter[str] = Counter()
        # XOR of per-event digests keeps the dataset fingerprint order
        # independent while remaining bounded for streaming inputs.  The
        # event count is mixed in at summary time so repeated events matter.
        self.event_fingerprint = bytearray(32)

    def add(self, event: CanonicalEvent) -> None:
        self.event_count += 1
        encoded = json.dumps(
            event.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        digest = hashlib.sha256(encoded).digest()
        for index, value in enumerate(digest):
            self.event_fingerprint[index] ^= value
        self.episode_ids.add(event.episode_id)
        self.lane_counts[event.lane] += 1
        self.kind_counts[event.kind] += 1
        if event.kind in {"unknown", "parse_error"}:
            self.unknown_subtypes[event.subtype or event.kind] += 1
        for issue in validate_events((event,)):
            self.issue_counts[issue.code] += 1
        if event.event_id in self.seen_ids:
            self.issue_counts["duplicate_event_id"] += 1
        elif len(self.seen_ids) < self.duplicate_tracking_limit:
            self.seen_ids.add(event.event_id)
        else:
            self.duplicate_tracking_complete = False
            self.duplicate_checks_skipped += 1
        if event.kind not in {"unknown", "parse_error"}:
            self.known_count += 1
        if event.lane == "codex":
            self._add_codex(event)
        elif event.lane == "chatgpt_chat":
            self._add_chat(event)

    def _add_codex(self, event: CanonicalEvent) -> None:
        state = self.codex.setdefault(
            event.episode_id,
            {
                "tool_calls": 0,
                "tool_results": 0,
                "first_tool": None,
                "first_inspect": None,
                "first_mutate": None,
                "verify_after_mutate": False,
                "delegation_events": 0,
                "compactions": 0,
            },
        )
        marker = (event.ordinal, event.event_id)
        if event.kind == "tool_call":
            state["tool_calls"] += 1
            if state["first_tool"] is None or marker < state["first_tool"][0]:
                state["first_tool"] = (marker, event.tool_family or "unknown")
        elif event.kind == "tool_result":
            state["tool_results"] += 1
        if event.tool_family == "inspect":
            if state["first_inspect"] is None or marker < state["first_inspect"]:
                state["first_inspect"] = marker
        elif event.tool_family == "mutate":
            if state["first_mutate"] is None or marker < state["first_mutate"]:
                state["first_mutate"] = marker
        elif event.tool_family == "verify":
            if state["first_mutate"] is not None and marker > state["first_mutate"]:
                state["verify_after_mutate"] = True
        if event.tool_family == "delegate":
            state["delegation_events"] += 1
        if event.kind == "compaction":
            state["compactions"] += 1

    def _add_chat(self, event: CanonicalEvent) -> None:
        self.chat_episode_ids.add(event.episode_id)
        self.chat_counts[event.kind] += 1
        if event.kind == "message" and event.actor == "assistant":
            self.chat_assistant_episodes.add(event.episode_id)
            self.chat_counts["assistant_message"] += 1
        elif event.kind == "message" and event.actor == "user":
            self.chat_counts["user_message"] += 1
        if event.kind == "citation":
            self.chat_citation_episodes.add(event.episode_id)
        if event.kind == "research" or event.tool_family == "research":
            self.chat_counts["research"] += 1
        if event.attributes.get("content_type") == "execution_output":
            self.chat_counts["execution_output"] += 1
        if event.attributes.get("content_type") == "code":
            self.chat_counts["code"] += 1

    def summary(self) -> dict[str, Any]:
        first_tools: Counter[str] = Counter()
        inspection_action_before_mutation_action = 0
        mutation_action_episodes = 0
        verification_action_after_mutation_action = 0
        tool_calls = 0
        tool_results = 0
        delegation_events = 0
        compactions = 0
        for state in self.codex.values():
            tool_calls += state["tool_calls"]
            tool_results += state["tool_results"]
            delegation_events += state["delegation_events"]
            compactions += state["compactions"]
            if state["first_tool"] is not None:
                first_tools[state["first_tool"][1]] += 1
            if state["first_mutate"] is not None:
                mutation_action_episodes += 1
                if (
                    state["first_inspect"] is not None
                    and state["first_inspect"] < state["first_mutate"]
                ):
                    inspection_action_before_mutation_action += 1
                if state["verify_after_mutate"]:
                    verification_action_after_mutation_action += 1
        chat_event_count = self.lane_counts.get("chatgpt_chat", 0)
        chat_known = sum(
            self.chat_counts[k] for k in ("message", "tool_call", "tool_result", "citation")
        )
        issues = dict(sorted(self.issue_counts.items()))
        fingerprint = hashlib.sha256(
            bytes(self.event_fingerprint) + str(self.event_count).encode("ascii")
        ).hexdigest()
        return {
            "contract_version": CONTRACT_VERSION,
            "ontology_version": ONTOLOGY_VERSION,
            "codebook_version": CODEBOOK_VERSION,
            "analyzer_version": ANALYZER_VERSION,
            "event_count": self.event_count,
            "episode_count": len(self.episode_ids),
            "lane_counts": dict(sorted(self.lane_counts.items())),
            "kind_counts": dict(sorted(self.kind_counts.items())),
            "unknown_event_count": self.kind_counts.get("unknown", 0),
            "parse_error_count": self.kind_counts.get("parse_error", 0),
            "unknown_or_parse_error_count": self.event_count - self.known_count,
            "unknown_or_parse_error_subtypes": dict(sorted(self.unknown_subtypes.items())),
            "known_event_rate": _rate(self.known_count, self.event_count),
            "validation_issue_count": sum(issues.values()),
            "validation_issue_counts": issues,
            "duplicate_tracking_complete": self.duplicate_tracking_complete,
            "duplicate_tracking_limit": self.duplicate_tracking_limit,
            "duplicate_checks_skipped": self.duplicate_checks_skipped,
            "event_fingerprint": fingerprint,
            "lanes": {
                "codex": {
                    "episode_count": len(self.codex),
                    "tool_calls": tool_calls,
                    "tool_results": tool_results,
                    "tool_results_per_call": _rate(tool_results, tool_calls),
                    "first_tool_family": dict(sorted(first_tools.items())),
                    "mutation_action_episodes": mutation_action_episodes,
                    "inspection_action_before_mutation_action": (
                        inspection_action_before_mutation_action
                    ),
                    "inspection_action_before_mutation_action_rate": _rate(
                        inspection_action_before_mutation_action, mutation_action_episodes
                    ),
                    "verification_action_after_mutation_action": (
                        verification_action_after_mutation_action
                    ),
                    "verification_action_after_mutation_action_rate": _rate(
                        verification_action_after_mutation_action, mutation_action_episodes
                    ),
                    "delegation_events": delegation_events,
                    "compactions": compactions,
                },
                "chatgpt_chat": {
                    "episode_count": len(self.chat_episode_ids),
                    "assistant_episode_count": len(self.chat_assistant_episodes),
                    "user_messages": self.chat_counts["user_message"],
                    "assistant_messages": self.chat_counts.get("assistant_message", 0),
                    "tool_calls": self.chat_counts["tool_call"],
                    "tool_results": self.chat_counts["tool_result"],
                    "citations": self.chat_counts["citation"],
                    "research_events": self.chat_counts["research"],
                    "execution_output_events": self.chat_counts["execution_output"],
                    "code_events": self.chat_counts["code"],
                    "citation_presence_rate": _rate(
                        len(self.chat_citation_episodes), len(self.chat_episode_ids)
                    ),
                    "citation_presence_numerator": len(self.chat_citation_episodes),
                    "citation_presence_denominator": len(self.chat_episode_ids),
                    "known_message_or_tool_rate": _rate(chat_known, chat_event_count),
                    "known_message_or_tool_numerator": chat_known,
                    "known_message_or_tool_denominator": chat_event_count,
                },
            },
        }


def analyze_stream(
    events: Iterable[CanonicalEvent], *, duplicate_tracking_limit: int = 250_000
) -> dict[str, Any]:
    analyzer = StreamingAnalyzer(duplicate_tracking_limit=duplicate_tracking_limit)
    for event in events:
        analyzer.add(event)
    return analyzer.summary()


def analyze_events(events: Iterable[CanonicalEvent]) -> dict[str, Any]:
    """Return a versioned, body-free summary for both lanes."""
    return analyze_stream(events)


def export_bundle(
    events: Iterable[CanonicalEvent], output_dir: Path, *, source_count: int | None = None
) -> dict[str, Any]:
    """Write a reproducible local export: manifest, normalized events, and summary."""

    materialized = sorted(list(events), key=event_sort_key)
    analyzer = StreamingAnalyzer()
    for event in materialized:
        analyzer.add(event)
    summary = analyzer.summary()
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "events.jsonl").open("w", encoding="utf-8", newline="\n") as handle:
        for event in materialized:
            handle.write(json.dumps(event.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")
    run_id = stable_id(
        "analysis-run",
        CONTRACT_VERSION,
        ONTOLOGY_VERSION,
        CODEBOOK_VERSION,
        ANALYZER_VERSION,
        summary["event_count"],
        source_count,
        summary["event_fingerprint"],
    )
    summary["analysis_run_id"] = run_id
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    manifest = {
        "analysis_run_id": run_id,
        "contract_version": CONTRACT_VERSION,
        "ontology_version": ONTOLOGY_VERSION,
        "codebook_version": CODEBOOK_VERSION,
        "analyzer_version": ANALYZER_VERSION,
        "event_count": len(materialized),
        "source_count": source_count,
        "body_policy": "no transcript bodies are written",
        "streaming": False,
        "events_exported": True,
        "event_fingerprint": summary["event_fingerprint"],
        "ordering_policy": "sorted by event_sort_key",
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return summary


def export_stream(
    events: Iterable[CanonicalEvent],
    output_dir: Path,
    *,
    source_count: int | None = None,
    write_events: bool = True,
    duplicate_tracking_limit: int = 250_000,
) -> dict[str, Any]:
    """Export a deterministic input stream without retaining all events."""

    output_dir.mkdir(parents=True, exist_ok=True)
    analyzer = StreamingAnalyzer(duplicate_tracking_limit=duplicate_tracking_limit)
    event_path = output_dir / "events.jsonl"
    if not write_events and event_path.exists():
        event_path.unlink()
    handle = (
        event_path.open("w", encoding="utf-8", newline="\n") if write_events else None
    )
    try:
        for event in events:
            analyzer.add(event)
            if handle is not None:
                handle.write(json.dumps(event.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")
    finally:
        if handle is not None:
            handle.close()
    summary = analyzer.summary()
    run_id = stable_id(
        "analysis-run",
        CONTRACT_VERSION,
        ONTOLOGY_VERSION,
        CODEBOOK_VERSION,
        ANALYZER_VERSION,
        summary["event_count"],
        source_count,
        summary["event_fingerprint"],
    )
    summary["analysis_run_id"] = run_id
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    manifest = {
        "analysis_run_id": run_id,
        "contract_version": CONTRACT_VERSION,
        "ontology_version": ONTOLOGY_VERSION,
        "codebook_version": CODEBOOK_VERSION,
        "analyzer_version": ANALYZER_VERSION,
        "event_count": summary["event_count"],
        "source_count": source_count,
        "body_policy": "no transcript bodies are written",
        "streaming": True,
        "events_exported": write_events,
        "event_fingerprint": summary["event_fingerprint"],
        "ordering_policy": "caller-supplied deterministic event order",
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return summary

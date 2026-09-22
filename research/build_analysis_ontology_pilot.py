"""Build a deterministic, body-free ontology pilot and sealed holdout.

This is intentionally a small research runner, not an annotation platform. It
selects episodes using normalized structural features, writes local ignored
JSONL, and records enough metadata to reproduce the split without copying
transcript bodies into Git.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

# Permit both `python -m research.build_analysis_ontology_pilot` and direct
# execution from the repository root.
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.hos.analysis_machine.model import (  # noqa: E402
    CODEBOOK_VERSION,
    ONTOLOGY_VERSION,
    CanonicalEvent,
    stable_id,
)
from src.hos.analysis_machine.normalize import iter_normalized_paths, jsonl_paths  # noqa: E402

CODEX_FEATURES = frozenset(
    {"inspect", "mutate", "verify", "delegate", "compaction", "unknown"}
)
CHAT_FEATURES = frozenset(
    {
        "user_message",
        "assistant_message",
        "citation",
        "research",
        "tool",
        "code",
        "execution_output",
        "unknown",
    }
)


def _features(event: CanonicalEvent) -> set[str]:
    if event.lane == "codex":
        result: set[str] = set()
        if event.tool_family in CODEX_FEATURES:
            result.add(event.tool_family or "unknown")
        if event.kind == "compaction":
            result.add("compaction")
        if event.kind == "unknown":
            result.add("unknown")
        return result
    if event.lane == "chatgpt_chat":
        result = set()
        if event.kind == "message" and event.actor == "user":
            result.add("user_message")
        if event.kind == "message" and event.actor == "assistant":
            result.add("assistant_message")
        if event.kind in {"tool_call", "tool_result"}:
            result.add("tool")
        if event.kind == "citation":
            result.add("citation")
        if event.kind == "research":
            result.add("research")
        if event.tool_family == "research":
            result.add("research")
        if event.attributes.get("content_type") == "code":
            result.add("code")
        if event.attributes.get("content_type") == "execution_output":
            result.add("execution_output")
        if event.kind == "unknown":
            result.add("unknown")
        return result
    return {"unknown"}


def _episode_stats(events: Iterable[CanonicalEvent]) -> dict[str, dict[str, Any]]:
    stats: dict[str, dict[str, Any]] = {}
    for event in events:
        state = stats.setdefault(
            event.episode_id,
            {
                "episode_id": event.episode_id,
                "lane": event.lane,
                "event_count": 0,
                "features": set(),
            },
        )
        state["event_count"] += 1
        state["features"].update(_features(event))
    return stats


def _select(
    stats: dict[str, dict[str, Any]],
    *,
    lane: str,
    count: int,
    holdout: bool,
    salt: str,
) -> list[str]:
    candidates = []
    for state in stats.values():
        if state["lane"] != lane:
            continue
        bucket = int(stable_id("ontology-pilot-bucket", salt, state["episode_id"]), 16) % 5
        if (bucket == 0) != holdout:
            candidates.append(state)
    selected: list[str] = []
    covered: set[str] = set()
    while candidates and len(selected) < count:
        choice = max(
            candidates,
            key=lambda state: (
                len(set(state["features"]) - covered),
                -abs(int(state["event_count"]) - 80),
                -int(state["event_count"]),
                state["episode_id"],
            ),
        )
        candidates.remove(choice)
        selected.append(choice["episode_id"])
        covered.update(choice["features"])
    return sorted(selected)


def build_pilot(
    inputs: Iterable[Path],
    output_dir: Path,
    *,
    pilot_per_lane: int = 4,
    holdout_per_lane: int = 2,
) -> dict[str, Any]:
    paths = jsonl_paths(inputs)
    stats = _episode_stats(iter_normalized_paths(paths))
    pilot_ids = {
        lane: _select(
            stats,
            lane=lane,
            count=pilot_per_lane,
            holdout=False,
            salt="split",
        )
        for lane in ("codex", "chatgpt_chat")
    }
    holdout_ids = {
        lane: _select(
            stats,
            lane=lane,
            count=holdout_per_lane,
            holdout=True,
            salt="split",
        )
        for lane in ("codex", "chatgpt_chat")
    }
    selected = {
        "pilot": set(pilot_ids["codex"] + pilot_ids["chatgpt_chat"]),
        "holdout": set(holdout_ids["codex"] + holdout_ids["chatgpt_chat"]),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    pilot_path = output_dir / "pilot-events.jsonl"
    holdout_path = output_dir / "holdout-events.jsonl"
    event_counts = {"pilot": 0, "holdout": 0}
    with (
        pilot_path.open("w", encoding="utf-8", newline="\n") as pilot_handle,
        holdout_path.open("w", encoding="utf-8", newline="\n") as holdout_handle,
    ):
        handles = {"pilot": pilot_handle, "holdout": holdout_handle}
        for event in iter_normalized_paths(paths):
            split = "pilot" if event.episode_id in selected["pilot"] else "holdout"
            if event.episode_id not in selected[split]:
                continue
            row = {
                "sample_id": stable_id("ontology-pilot", split, event.event_id),
                "split": split,
                "event": event.to_dict(),
            }
            handles[split].write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            event_counts[split] += 1
    manifest = {
        "schema": "analysis-ontology-pilot/0.1.0",
        "ontology_version": ONTOLOGY_VERSION,
        "codebook_version": CODEBOOK_VERSION,
        "source_count": len(paths),
        "selection_policy": {
            "bucket_count": 5,
            "pilot_bucket": "nonzero",
            "holdout_bucket": "zero",
            "greedy_feature_coverage": True,
            "event_target_size": 80,
            "features": {
            "codex": sorted(CODEX_FEATURES),
                "chatgpt_chat": sorted(CHAT_FEATURES),
            },
        },
        "episodes": {
            "pilot": pilot_ids,
            "holdout": holdout_ids,
        },
        "event_counts": event_counts,
        "body_policy": "canonical events only; transcript bodies are not written",
        "holdout_policy": "do not open or annotate until pilot adjudication is frozen",
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(prog="build-analysis-ontology-pilot")
    parser.add_argument("--input", action="append", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--pilot-per-lane", type=int, default=4)
    parser.add_argument("--holdout-per-lane", type=int, default=2)
    args = parser.parse_args()
    manifest = build_pilot(
        (Path(value) for value in args.input),
        Path(args.output),
        pilot_per_lane=args.pilot_per_lane,
        holdout_per_lane=args.holdout_per_lane,
    )
    print(json.dumps(manifest, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

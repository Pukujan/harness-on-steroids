"""Build a deterministic, body-free human review packet.

This is deliberately a packet builder, not an annotation service. It turns a
frozen canonical-event sample into one episode record per line with structural
event evidence and empty adjudication fields. The packet stays in the ignored
local evidence plane; it never copies transcript bodies into Git.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

REVIEW_PACKET_VERSION = "analysis-review-packet/0.1.0"


def _jsonl_paths(inputs: Iterable[Path]) -> list[Path]:
    paths: list[Path] = []
    for value in inputs:
        if value.is_file() and value.suffix.lower() == ".jsonl":
            paths.append(value)
        elif value.is_dir():
            paths.extend(path for path in value.rglob("*.jsonl") if path.is_file())
    return sorted(set(paths), key=lambda item: item.as_posix())


def _event_for_packet(row: dict[str, Any]) -> dict[str, Any]:
    event = row.get("event")
    if not isinstance(event, dict):
        raise ValueError("review input row must contain an event object")
    forbidden = {
        "body",
        "content",
        "text",
        "prompt",
        "raw",
        "stderr",
        "stdout",
        "arguments",
        "result_body",
    }
    leaked = forbidden.intersection(event)
    if leaked:
        raise ValueError(f"body-bearing fields are not allowed: {sorted(leaked)}")
    allowed = {
        "contract_version",
        "event_id",
        "source_id",
        "episode_id",
        "lane",
        "ordinal",
        "kind",
        "actor",
        "timestamp",
        "subtype",
        "tool_name",
        "tool_family",
        "status",
        "observation",
        "source_pointer",
        "source_record_id",
        "body_status",
        "analysis_run_id",
        "parent_event_id",
        "supersedes_event_id",
        "attributes",
    }
    return {key: event[key] for key in sorted(allowed.intersection(event))}


def build_review_packet(inputs: Iterable[Path], output_dir: Path) -> dict[str, Any]:
    paths = _jsonl_paths(inputs)
    episodes: dict[str, list[dict[str, Any]]] = defaultdict(list)
    input_hash = hashlib.sha256()
    row_count = 0
    for path in paths:
        for line in path.read_bytes().splitlines(keepends=True):
            input_hash.update(line)
            if not line.strip():
                continue
            row = json.loads(line)
            event = _event_for_packet(row)
            if row.get("split") not in {None, "pilot"}:
                raise ValueError("review packet input must be a pilot, not a holdout")
            episode_id = str(event.get("episode_id", "")).strip()
            if not episode_id:
                raise ValueError("review packet event is missing episode_id")
            episodes[episode_id].append(
                {
                    "sample_id": row.get("sample_id"),
                    "event": event,
                }
            )
            row_count += 1

    output_dir.mkdir(parents=True, exist_ok=True)
    packet_path = output_dir / "episodes.jsonl"
    with packet_path.open("w", encoding="utf-8", newline="\n") as handle:
        for episode_id in sorted(episodes):
            rows = sorted(
                episodes[episode_id],
                key=lambda row: (
                    int(row["event"].get("ordinal", 0)),
                    str(row["event"].get("event_id", "")),
                ),
            )
            first = rows[0]["event"]
            handle.write(
                json.dumps(
                    {
                        "episode_id": episode_id,
                        "lane": first.get("lane", "unknown"),
                        "event_count": len(rows),
                        "events": rows,
                        "adjudication": {
                            "reviewer": None,
                            "labels": {},
                            "abstentions": [],
                            "notes": "",
                        },
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                )
                + "\n"
            )

    manifest = {
        "schema": REVIEW_PACKET_VERSION,
        "body_policy": "canonical events only; transcript bodies are not written",
        "source_count": len(paths),
        "episode_count": len(episodes),
        "event_count": row_count,
        "input_fingerprint": input_hash.hexdigest(),
        "adjudication_policy": (
            "empty fields require owner/human review; model annotations are advisory"
        ),
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(prog="build-analysis-review-packet")
    parser.add_argument("--input", action="append", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    manifest = build_review_packet(
        (Path(value) for value in args.input),
        Path(args.output),
    )
    print(json.dumps(manifest, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

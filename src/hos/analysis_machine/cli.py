"""Command-line export for the reusable analysis machine."""

from __future__ import annotations

import argparse
from pathlib import Path

from .analyze import export_stream
from .normalize import iter_normalized_paths, jsonl_paths


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="analysis-machine")
    parser.add_argument(
        "--input", action="append", required=True, help="JSONL file or directory; repeatable"
    )
    parser.add_argument("--output", required=True, help="ignored local export directory")
    parser.add_argument("--lane", choices=("auto", "codex", "chatgpt_chat"), default="auto")
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="do not write the potentially large normalized events.jsonl",
    )
    parser.add_argument(
        "--duplicate-tracking-limit",
        type=int,
        default=250_000,
        help="maximum event IDs retained for exact duplicate checks",
    )
    args = parser.parse_args(argv)
    paths = jsonl_paths(Path(value) for value in args.input)
    summary = export_stream(
        iter_normalized_paths(paths, lane=args.lane),
        Path(args.output),
        source_count=len(paths),
        write_events=not args.summary_only,
        duplicate_tracking_limit=args.duplicate_tracking_limit,
    )
    print(
        f"analysis-machine: {summary['event_count']} events, "
        f"{summary['episode_count']} episodes, output={args.output}"
    )
    return 0

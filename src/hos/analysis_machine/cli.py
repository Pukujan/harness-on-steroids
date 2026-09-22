"""Command-line export for the reusable analysis machine."""

from __future__ import annotations

import argparse
from pathlib import Path

from .analyze import export_bundle
from .normalize import jsonl_paths, normalize_jsonl


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="analysis-machine")
    parser.add_argument(
        "--input", action="append", required=True, help="JSONL file or directory; repeatable"
    )
    parser.add_argument("--output", required=True, help="ignored local export directory")
    parser.add_argument("--lane", choices=("auto", "codex", "chatgpt_chat"), default="auto")
    args = parser.parse_args(argv)
    paths = jsonl_paths(Path(value) for value in args.input)
    events = []
    for path in paths:
        events.extend(normalize_jsonl(path, lane=args.lane))
    summary = export_bundle(events, Path(args.output), source_count=len(paths))
    print(
        f"analysis-machine: {summary['event_count']} events, "
        f"{summary['episode_count']} episodes, output={args.output}"
    )
    return 0

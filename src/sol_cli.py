"""CLI for a bounded CKFF Sol tool-loop run."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.sol_bridge import ROOT, SolBridgeError, run_task


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(prog="sol-worker")
    parser.add_argument("task", nargs="?", help="one bounded task for Sol")
    parser.add_argument("--task-file", default="", help="read the task from a UTF-8 file")
    parser.add_argument("--root", default=str(ROOT), help="repository root")
    parser.add_argument("--env-file", default="", help="ignored dotenv file to load")
    parser.add_argument("--max-rounds", type=int, default=0)
    parser.add_argument("--dry-run", action="store_true", help="preview edits and checks")
    args = parser.parse_args(argv)
    try:
        if bool(args.task) == bool(args.task_file):
            parser.error("provide exactly one of TASK or --task-file")
        task = (
            Path(args.task_file).read_text(encoding="utf-8") if args.task_file else str(args.task)
        )
        result = run_task(
            task,
            root=Path(args.root),
            env_path=Path(args.env_file) if args.env_file else None,
            max_rounds=args.max_rounds or None,
            dry_run=args.dry_run,
        )
    except (OSError, SolBridgeError) as exc:
        parser.exit(1, f"sol-worker: {exc}\n")
    print(result.final_text)
    print(f"\nRun record: {result.record_path}")
    print(f"Rounds: {result.rounds}; tool calls: {result.tool_calls}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

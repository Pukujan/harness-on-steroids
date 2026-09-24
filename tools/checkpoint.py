"""Command-line entry point for issue-backed checkpoint publishing."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.hos.checkpoint_publisher import (  # noqa: E402
    DEFAULT_WORKTREE_ROOT,
    CheckpointError,
    CheckpointPublisher,
    PublishResult,
    ReconcileResult,
    find_repository_root,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Publish and reconcile HOS checkpoints.")
    commands = parser.add_subparsers(dest="command", required=True)

    publish = commands.add_parser("publish", help="validate and publish an issue checkpoint")
    publish.add_argument("--issue", type=int, required=True)
    publish.add_argument(
        "--include",
        action="append",
        default=[],
        metavar="PATH",
        help="explicit changed path to include (repeat for each path)",
    )
    publish.add_argument("--base", default="main")
    publish.add_argument("--dry-run", action="store_true")

    reconcile = commands.add_parser(
        "reconcile", help="update canonical checkout and retire a merged clean worktree"
    )
    reconcile.add_argument("--pr", type=int, required=True)
    reconcile.add_argument("--worktree-path", type=Path, required=True)
    reconcile.add_argument("--worktree-root", type=Path, default=DEFAULT_WORKTREE_ROOT)
    reconcile.add_argument("--base", default="main")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        root = find_repository_root(Path.cwd())
        publisher = CheckpointPublisher(
            root,
            worktree_root=getattr(args, "worktree_root", DEFAULT_WORKTREE_ROOT),
        )
        result: PublishResult | ReconcileResult
        if args.command == "publish":
            result = publisher.publish(args.issue, args.include, args.dry_run, args.base)
        else:
            result = publisher.reconcile(args.pr, args.worktree_path, args.base)
        print(json.dumps(result.as_dict(), sort_keys=True))
        return 0
    except CheckpointError as exc:
        print(json.dumps({"state": "blocked", "reason": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

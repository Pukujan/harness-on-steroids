"""CLI: python -m src.goal_cli set|tick|status|pause|resume|clear|gate|subgoal"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from src.goal_loop import GoalEngine


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="goal")
    p.add_argument("--state", default="", help="state json path")
    sub = p.add_subparsers(dest="action", required=True)
    s = sub.add_parser("set")
    s.add_argument("text")
    s.add_argument("--max-turns", type=int, default=20)
    sub.add_parser("status")
    sub.add_parser("pause")
    sub.add_parser("resume")
    sub.add_parser("clear")
    g = sub.add_parser("gate")
    g.add_argument("--cmd", required=True, help="shell command (quote it)")
    sg = sub.add_parser("subgoal")
    sg.add_argument("text")
    t = sub.add_parser("tick")
    t.add_argument("--response", default="")
    t.add_argument("--response-file", default="")
    args = p.parse_args(argv)
    path = Path(args.state) if args.state else None
    eng = GoalEngine(path=path)
    if args.action == "set":
        eng.set_goal(args.text, max_turns=args.max_turns)
    elif args.action == "status":
        pass
    elif args.action == "pause":
        eng.pause()
    elif args.action == "resume":
        eng.resume()
    elif args.action == "clear":
        eng.clear()
    elif args.action == "gate":
        eng.add_gate(args.cmd)
    elif args.action == "subgoal":
        eng.add_subgoal(args.text)
    elif args.action == "tick":
        resp = args.response
        if args.response_file:
            resp = Path(args.response_file).read_text(encoding="utf-8")
        out = eng.tick(resp)
        print(json.dumps(out, indent=2))
        return 0 if not out["continue"] else 10
    print(json.dumps(eng.state.__dict__, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

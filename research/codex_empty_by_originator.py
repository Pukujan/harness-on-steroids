#!/usr/bin/env python3
"""Hashed files with no tool calls, by originator. Counts only."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "data" / "raw" / "codex"
OUT = ROOT / "reports" / "codex-empty-by-originator.md"
CALL_TYPES = {"custom_tool_call", "function_call"}


def main() -> None:
    files: Counter = Counter()
    empty: Counter = Counter()
    for path in sorted(CODEX.glob("*.jsonl")):
        orig = "unknown"
        has = False
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                payload = obj.get("payload") if isinstance(obj.get("payload"), dict) else {}
                if obj.get("type") == "session_meta":
                    o = payload.get("originator")
                    if isinstance(o, str):
                        orig = o
                    continue
                name = payload.get("name")
                pt = payload.get("type")
                if isinstance(name, str) and pt in CALL_TYPES:
                    has = True
        files[orig] += 1
        if not has:
            empty[orig] += 1
    n = sum(files.values())
    ne = sum(empty.values())
    lines = [
        "# Files with no tool calls, by originator",
        "",
        "One originator per file. Calls = custom_tool_call / function_call. v33.",
        "",
        f"Hashed files: **{n}** with no calls: **{ne}**",
        "",
        "| originator | files | no calls |",
        "| --- | --- | --- |",
    ]
    for orig, nf in files.most_common():
        lines.append(f"| {orig} | {nf} | {empty.get(orig, 0)} |")
    lines += [
        "",
        "## interpretation",
        "",
        "`codex_exec` is mostly empty of calls (210/315). That is not Work gold.",
        "Work no-call files stay **4/87**. vscode 3/16. Desktop 109/1103.",
        "Do not average empty-exec into Work imitate mode.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} empty={ne}/{n}")


if __name__ == "__main__":
    main()

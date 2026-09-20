#!/usr/bin/env python3
"""Tool mix by originator. No bodies."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "data" / "raw" / "codex"
OUT = ROOT / "reports" / "codex-by-originator.md"


def main() -> None:
    files = sorted(CODEX.glob("*.jsonl"))
    tools: dict[str, Counter] = defaultdict(Counter)
    first: dict[str, Counter] = defaultdict(Counter)
    n_files: Counter = Counter()
    for path in files:
        orig = "unknown"
        saw_first = False
        n_files["files"] += 1
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                payload = obj.get("payload") if isinstance(obj.get("payload"), dict) else {}
                if obj.get("type") == "session_meta":
                    o = payload.get("originator")
                    if isinstance(o, str) and o:
                        orig = o
                    n_files[orig] += 1
                    continue
                name = payload.get("name")
                if not isinstance(name, str):
                    continue
                tools[orig][name] += 1
                if not saw_first:
                    first[orig][name] += 1
                    saw_first = True

    lines = [
        "# Codex tool mix by originator",
        "",
        f"Files scanned: **{n_files['files']}**",
        "",
        "## sessions (session_meta originator)",
        "",
        "| originator | files |",
        "| --- | --- |",
    ]
    for k, v in n_files.most_common():
        if k == "files":
            continue
        lines.append(f"| {k} | {v} |")
    for orig in sorted(tools):
        lines += ["", f"## `{orig}` tools", "", "| tool | count |", "| --- | --- |"]
        for t, c in tools[orig].most_common(12):
            lines.append(f"| {t} | {c} |")
        lines += ["", f"### `{orig}` first tool", "", "| tool | sessions |", "| --- | --- |"]
        for t, c in first[orig].most_common(8):
            lines.append(f"| {t} | {c} |")
    lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()

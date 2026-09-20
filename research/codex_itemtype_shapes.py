#!/usr/bin/env python3
"""Codex thread_items shapes (task split proxy). No JSON bodies."""

from __future__ import annotations

import sqlite3
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "raw" / "sqlite" / "codex_thread_history.sqlite"
OUT = ROOT / "reports" / "codex-itemtype-shapes.md"

MUTATE = {"fileChange"}
LOOK = {"webSearch", "imageView"}
DECOMP = {"subAgentActivity", "plan", "collabAgentToolCall"}


def md_table(rows, headers, limit=30) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows[:limit]:
        lines.append("| " + " | ".join(str(x) for x in row) + " |")
    return "\n".join(lines)


def main() -> None:
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    cur = con.execute(
        "SELECT thread_id, item_type FROM thread_items ORDER BY thread_id, rollout_ordinal"
    )
    first = Counter()
    compact_shapes = Counter()
    n = 0
    n_look_before_fc = 0
    n_fc = 0
    n_decomp = 0
    current = None
    seq: list[str] = []

    def flush(s: list[str]) -> None:
        nonlocal n, n_look_before_fc, n_fc, n_decomp
        if not s:
            return
        n += 1
        first[s[0]] += 1
        compact = [s[0]]
        for x in s[1:]:
            if x != compact[-1]:
                compact.append(x)
        compact_shapes[" → ".join(compact[:10])] += 1
        if "fileChange" in s:
            n_fc += 1
            i = s.index("fileChange")
            if any(x in LOOK or x == "commandExecution" for x in s[:i]):
                n_look_before_fc += 1
        if any(x in DECOMP for x in s):
            n_decomp += 1

    for tid, t in cur:
        if tid != current:
            flush(seq)
            current = tid
            seq = []
        seq.append(t or "null")
    flush(seq)
    con.close()
    OUT.write_text(
        "\n".join(
            [
                "# Codex item_type shapes (sqlite projection)",
                "",
                "Not finished gold. Complements JSONL tool names.",
                "",
                f"- threads: **{n}**",
                f"- with fileChange: **{n_fc}**",
                f"- commandExecution/webSearch/imageView before first fileChange: **{n_look_before_fc}**",
                f"- with plan/subagent/collab tools: **{n_decomp}**",
                "",
                "## first item_type",
                "",
                md_table(first.most_common(), ["first", "threads"]),
                "",
                "## collapsed shapes (top 25)",
                "",
                md_table(compact_shapes.most_common(25), ["shape", "threads"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

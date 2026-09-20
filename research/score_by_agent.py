#!/usr/bin/env python3
"""work_match by session.agent. No bodies."""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.score_session import _agents, _tools, score_seq

OUT = ROOT / "reports" / "work-match-by-agent.md"
SKIP_PREFIXES = ("study-os",)


def rollup(db: Path) -> list[tuple[str, int, int]]:
    seqs = _tools(db)
    agents = _agents(db)
    n: Counter = Counter()
    match: Counter = Counter()
    for sid, seq in seqs.items():
        if not seq:
            continue
        if any(any(x.startswith(p) for p in SKIP_PREFIXES) for x in seq):
            continue
        ag = agents.get(sid) or "<null>"
        n[ag] += 1
        if score_seq(seq)["work_match"]:
            match[ag] += 1
    rows = []
    for ag, nn in n.most_common():
        rows.append((ag, match[ag], nn))
    return rows


def main() -> None:
    lines = [
        "# work_match by session.agent",
        "",
        "v55. Skip study-os tool prefix. No bodies. There is no `codex` slug.",
        "",
    ]
    for label, db in (
        ("kilo.db", ROOT / "data" / "raw" / "sqlite" / "kilo.db"),
        ("opencode.db", ROOT / "data" / "raw" / "sqlite" / "opencode.db"),
    ):
        lines += [f"## {label}", "", "| agent | work_match | sessions |", "| --- | --- | --- |"]
        if not db.exists():
            lines.append("| (missing) | 0 | 0 |")
            lines.append("")
            continue
        for ag, m, n in rollup(db):
            lines.append(f"| {ag} | {m}/{n} | {n} |")
        lines.append("")
    lines += [
        "## interpretation",
        "",
        "Neither product has agent=`codex`. Score `code`/`build` as the coding copies. luna is not Work gold.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

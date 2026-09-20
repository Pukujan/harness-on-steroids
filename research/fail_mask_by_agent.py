#!/usr/bin/env python3
"""fail_mask for coding agents (kilo code, opencode build). No bodies."""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.score_session import _agents, _tools, score_seq

OUT = ROOT / "reports" / "fail-mask-by-agent.md"
SKIP_PREFIXES = ("study-os",)
KEEP = {
    "kilo.db": {"code"},
    "opencode.db": {"build"},
}


def main() -> None:
    lines = [
        "# fail_mask for coding agents",
        "",
        "v56. Kilo `code`, OpenCode `build`. Skip study-os. No bodies.",
        "",
    ]
    for label, keep in KEEP.items():
        db = ROOT / "data" / "raw" / "sqlite" / label
        lines += [f"## {label} agent={','.join(sorted(keep))}", "", "| fail_mask | n |", "| --- | --- |"]
        if not db.exists():
            lines.append("| missing | 0 |")
            lines.append("")
            continue
        seqs = _tools(db)
        agents = _agents(db)
        masks: Counter = Counter()
        for sid, seq in seqs.items():
            if not seq:
                continue
            if agents.get(sid) not in keep:
                continue
            if any(any(x.startswith(p) for p in SKIP_PREFIXES) for x in seq):
                continue
            masks[score_seq(seq)["fail_mask"]] += 1
        for k, v in masks.most_common(12):
            lines.append(f"| {k} | {v} |")
        lines.append("")
    lines += [
        "## interpretation",
        "",
        "Coding copies still fail R2+R4+R5 (write + todowrite after look) and OpenCode R3 (bash-first).",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

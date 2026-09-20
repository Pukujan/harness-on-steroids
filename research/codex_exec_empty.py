#!/usr/bin/env python3
"""Empty-of-calls codex_exec files. Type counts only. No bodies."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "data" / "raw" / "codex"
OUT = ROOT / "reports" / "codex-exec-empty.md"
WANT = "codex_exec"
CALL_TYPES = {"custom_tool_call", "function_call"}


def main() -> None:
    n = 0
    empty = 0
    top_types: Counter = Counter()
    payload_types: Counter = Counter()
    lines_per: list[int] = []
    for path in sorted(CODEX.glob("*.jsonl")):
        orig = None
        has = False
        types: Counter = Counter()
        ptypes: Counter = Counter()
        nlines = 0
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                nlines += 1
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                payload = obj.get("payload") if isinstance(obj.get("payload"), dict) else {}
                t = obj.get("type")
                if isinstance(t, str):
                    types[t] += 1
                if t == "session_meta":
                    o = payload.get("originator")
                    if isinstance(o, str):
                        orig = o
                    continue
                if orig != WANT:
                    continue
                pt = payload.get("type")
                if isinstance(pt, str):
                    ptypes[pt] += 1
                name = payload.get("name")
                if isinstance(name, str) and pt in CALL_TYPES:
                    has = True
        if orig != WANT:
            continue
        n += 1
        if has:
            continue
        empty += 1
        lines_per.append(nlines)
        top_types.update(types)
        payload_types.update(ptypes)
    lines_per.sort()
    med = lines_per[len(lines_per) // 2] if lines_per else 0
    lines = [
        "# Empty `codex_exec` files (no tool calls)",
        "",
        "Counts only. No bodies. v34.",
        "",
        f"codex_exec files: **{n}** empty of calls: **{empty}**",
        f"- line counts: n={len(lines_per)} min={lines_per[0] if lines_per else 0} median={med} max={lines_per[-1] if lines_per else 0}",
        "",
        "## top-level types (empty files)",
        "",
        "| type | count |",
        "| --- | --- |",
    ]
    for k, v in top_types.most_common(10):
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## payload.type (empty files)",
        "",
        "| type | count |",
        "| --- | --- |",
    ]
    for k, v in payload_types.most_common(10):
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## interpretation",
        "",
        "`codex_exec` empty files are not Work gold. Work empty is 4/87 and short.",
        "Do not copy exec-originator no-call threads into the imitate mode.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} empty={empty}/{n}")


if __name__ == "__main__":
    main()

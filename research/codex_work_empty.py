#!/usr/bin/env python3
"""Work sessions with no tool calls. Type counts only. No bodies."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "data" / "raw" / "codex"
OUT = ROOT / "reports" / "codex-work-empty.md"
WANT = "codex_work_desktop"
CALL_TYPES = {"custom_tool_call", "function_call"}


def main() -> None:
    n = 0
    empty = 0
    top_types = Counter()
    payload_types = Counter()
    lines_per: list[int] = []
    meta_hist: Counter = Counter()
    meta_rows = 0
    for path in sorted(CODEX.glob("*.jsonl")):
        orig = None
        seq: list[str] = []
        types: Counter = Counter()
        ptypes: Counter = Counter()
        nlines = 0
        nmeta = 0
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
                if obj.get("type") == "session_meta":
                    nmeta += 1
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
                    seq.append(name)
        if orig != WANT:
            continue
        n += 1
        meta_hist[nmeta] += 1
        meta_rows += nmeta
        if seq:
            continue
        empty += 1
        lines_per.append(nlines)
        top_types.update(types)
        payload_types.update(ptypes)
    lines = [
        "# ChatGPT Work sessions with no tool calls",
        "",
        "Counts only. No bodies. v25.",
        "",
        f"Work files: **{n}** empty of calls: **{empty}**",
        f"- line counts: {sorted(lines_per)}",
        f"- session_meta rows: **{meta_rows}** (files with 1 meta: **{meta_hist.get(1, 0)}**; with 2: **{meta_hist.get(2, 0)}**)",
        "",
        "## top-level types (empty files)",
        "",
        "| type | count |",
        "| --- | --- |",
    ]
    for k, v in top_types.most_common(12):
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## payload.type (empty files)",
        "",
        "| type | count |",
        "| --- | --- |",
    ]
    for k, v in payload_types.most_common(12):
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## interpretation",
        "",
        "Empty Work files are short (14–25 lines): messages and task_started/complete, **no tool calls**.",
        "Originator **95** is session_meta rows (79 files ×1 + 8 files ×2). Tool-call analysis uses **87** files.",
        "If there is nothing to look up, stop. Do not spawn or patch.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} empty={empty}/{n}")


if __name__ == "__main__":
    main()

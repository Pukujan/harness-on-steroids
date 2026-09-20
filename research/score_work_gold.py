#!/usr/bin/env python3
"""Self-score Work JSONL with R1–R6 mapping. Counts only. No bodies."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.score_session import map_work_seq, score_seq

CODEX = ROOT / "data" / "raw" / "codex"
OUT = ROOT / "reports" / "work-gold-self-score.md"
WANT = "codex_work_desktop"
CALL_TYPES = {"custom_tool_call", "function_call"}


def main() -> None:
    n = 0
    scored = 0
    match = 0
    bits = Counter()
    firsts = Counter()
    for path in sorted(CODEX.glob("*.jsonl")):
        orig = None
        seq: list[str] = []
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
                if orig != WANT:
                    continue
                name = payload.get("name")
                pt = payload.get("type")
                if isinstance(name, str) and pt in CALL_TYPES:
                    seq.append(name)
        if orig != WANT:
            continue
        n += 1
        mapped = map_work_seq(seq)
        if not mapped:
            continue
        scored += 1
        s = score_seq(mapped)
        firsts[s["first"]] += 1
        if s["work_match"]:
            match += 1
        for k in (
            "r1_look_first",
            "r2_no_write",
            "r3_read_first",
            "r4_no_todowrite",
            "r5_no_write_after_look_run",
            "r6_decompose_not_first",
        ):
            if s[k]:
                bits[k] += 1
    lines = [
        "# Work gold self-score (mapped onto R1–R6)",
        "",
        "No bodies. v17. `exec`→read, `shell_command`→bash, `apply_patch`→edit, `send_message`→task, `update_plan`→todowrite.",
        "",
        f"Work sessions: **{n}** with mapped calls: **{scored}**",
        f"- **work_match: {match} / {scored}** ({(match / scored) if scored else 0:.2f})",
        "",
        "## relations on Work itself",
        "",
        "| relation | pass |",
        "| --- | --- |",
    ]
    for k, v in bits.most_common():
        lines.append(f"| {k} | {v} / {scored} |")
    lines += [
        "",
        "## mapped first tool",
        "",
        "| first | n |",
        "| --- | --- |",
    ]
    for k, v in firsts.most_common():
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## interpretation",
        "",
        "If Work itself does not mostly work_match, the scorer is the wrong exam.",
        "Kilo/OpenCode should move toward this rate, not toward SWE-bench.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} match={match}/{scored}")


if __name__ == "__main__":
    main()

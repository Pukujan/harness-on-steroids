#!/usr/bin/env python3
"""Process-score Work JSONL for develop+holdout hashes. No bodies."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.score_session import map_work_seq, score_seq

CODEX = ROOT / "data" / "raw" / "codex"
OUT = ROOT / "reports" / "replay-scores.md"
WANT = "codex_work_desktop"
CALL_TYPES = {"custom_tool_call", "function_call"}
HOLD = ROOT / "reports" / "work-long-holdout.md"


def hashes_from(md: Path, heading: str) -> list[str]:
    text = md.read_text(encoding="utf-8")
    chunk = text.split(heading, 1)[-1].split("## ", 1)[0]
    found: list[str] = []
    for tok in chunk.replace("`", " ").split():
        if len(tok) == 12 and all(c in "0123456789abcdef" for c in tok):
            found.append(tok)
    return found


def main() -> None:
    develop = hashes_from(HOLD, "## Develop")
    holdout = hashes_from(HOLD, "## Hidden holdout")
    want = set(develop + holdout)
    by_hash: dict[str, list[str]] = {}
    for path in sorted(CODEX.glob("*.jsonl")):
        h = path.stem[:12]
        if h not in want:
            continue
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
        by_hash[h] = seq

    def rows(label: str, hs: list[str]) -> list[str]:
        out = [
            f"## {label}",
            "",
            "| hash12 | work_match | fail_mask | kilo | opencode | morph |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
        for h in hs:
            s = score_seq(map_work_seq(by_hash.get(h, [])))
            wm = "yes" if s.get("work_match") else "no"
            mask = s.get("fail_mask") or "empty"
            out.append(f"| {h} | {wm} | {mask} | pending | pending | pending |")
        out.append("")
        return out

    lines = [
        "# Replay scores (hashes only)",
        "",
        "v64. Work process from JSONL. Kilo/OpenCode/morph columns **pending** (not replayed). No bodies.",
        "",
    ]
    lines += rows("develop (16)", develop)
    lines += rows("holdout (6)", holdout)
    lines += [
        "Kilo and OpenCode live replay of these threads is **not done**.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} develop={len(develop)} holdout={len(holdout)}")


if __name__ == "__main__":
    main()

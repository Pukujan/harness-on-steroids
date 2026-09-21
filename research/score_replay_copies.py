#!/usr/bin/env python3
"""Fill OpenCode/morph columns from gitignored copies. Keep Kilo cells. No bodies."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from research.replay_lib import (  # noqa: E402
    REPLAY,
    SCORES,
    cell,
    develop_hashes,
    holdout_hashes,
    parse_score_row,
    tool_seq,
)


def existing_rows() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    if not SCORES.is_file():
        return out
    for line in SCORES.read_text(encoding="utf-8").splitlines():
        row = parse_score_row(line)
        if row:
            out[row["hash12"]] = row
    return out


def opencode_cell(h: str) -> str:
    dest = REPLAY / h
    err = dest / "opencode.err"
    nd = dest / "opencode.ndjson"
    seq = tool_seq(nd)
    if seq:
        return cell(seq)
    timed = err.is_file() and "timeout" in err.read_text(encoding="utf-8", errors="replace").lower()
    if timed and (not nd.is_file() or nd.stat().st_size < 500):
        return "timeout"
    if nd.is_file() and nd.stat().st_size > 0:
        return "no/empty/no"
    if timed:
        return "timeout"
    return "pending"


def morph_cell(h: str, prev: str) -> str:
    dest = REPLAY / h
    morph_nd = dest / "opencode-morph.ndjson"
    seq = tool_seq(morph_nd)
    if seq:
        return "yes"
    # Keep previously recorded tool-replays. File-only or error ndjson is not yes.
    if prev == "yes":
        return "yes"
    if morph_nd.is_file() and morph_nd.stat().st_size > 0 and not seq:
        return "empty-tools"
    return "pending"


def section(label: str, hs: list[str], prev: dict[str, dict[str, str]]) -> list[str]:
    lines = [
        f"## {label}",
        "",
        "| hash12 | work_match | fail_mask | kilo | opencode | morph |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for h in hs:
        old = prev.get(h, {})
        kilo = old.get("kilo", "pending")
        wm = old.get("work_match", "pending")
        mask = old.get("fail_mask", "pending")
        oc = opencode_cell(h)
        morph = morph_cell(h, old.get("morph", "pending"))
        lines.append(f"| {h} | {wm} | {mask} | {kilo} | {oc} | {morph} |")
    lines.append("")
    return lines


def main() -> None:
    prev = existing_rows()
    develop = develop_hashes()
    holdout = holdout_hashes()
    lines = [
        "# Replay scores (hashes only)",
        "",
        "v65. Work process from JSONL. OpenCode cells from gitignored ndjson copies. Kilo cells kept. No bodies.",
        "",
    ]
    lines += section("develop (16)", develop, prev)
    lines += section("holdout (6)", holdout, prev)
    lines += [
        "Kilo and OpenCode live replay of these threads is **not done**.",
        "",
    ]
    SCORES.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {SCORES} develop={len(develop)} holdout={len(holdout)}")


if __name__ == "__main__":
    main()

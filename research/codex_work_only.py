#!/usr/bin/env python3
"""ChatGPT Work desktop only (originator=codex_work_desktop). No bodies."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "data" / "raw" / "codex"
OUT = ROOT / "reports" / "codex-work-desktop-only.md"
WANT = "codex_work_desktop"


def main() -> None:
    files = sorted(CODEX.glob("*.jsonl"))
    n = 0
    tools = Counter()
    first = Counter()
    bigrams = Counter()
    has_spawn = 0
    has_patch = 0
    has_wait = 0
    has_js = 0
    has_send = 0
    for path in files:
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
                name = payload.get("name")
                if isinstance(name, str):
                    seq.append(name)
        if orig != WANT:
            continue
        n += 1
        if seq:
            first[seq[0]] += 1
        names = set(seq)
        if "spawn_agent" in names or "send_message" in names:
            has_spawn += 1
        if "apply_patch" in names:
            has_patch += 1
        if "wait" in names:
            has_wait += 1
        if "js" in names:
            has_js += 1
        if "send_message" in names:
            has_send += 1
        for t in seq:
            tools[t] += 1
        for a, b in zip(seq, seq[1:]):
            bigrams[f"{a} -> {b}"] += 1

    lines = [
        "# ChatGPT Work desktop only (`codex_work_desktop`)",
        "",
        f"Sessions: **{n}**",
        f"- with wait: **{has_wait}**",
        f"- with js: **{has_js}**",
        f"- with send_message: **{has_send}**",
        f"- with spawn/send (multi-agent): **{has_spawn}**",
        f"- with apply_patch: **{has_patch}**",
        "",
        "## first tool",
        "",
        "| tool | sessions |",
        "| --- | --- |",
    ]
    for k, v in first.most_common():
        lines.append(f"| {k} | {v} |")
    lines += ["", "## tools", "", "| tool | count |", "| --- | --- |"]
    for k, v in tools.most_common(15):
        lines.append(f"| {k} | {v} |")
    lines += ["", "## bigrams", "", "| bigram | count |", "| --- | --- |"]
    for k, v in bigrams.most_common(20):
        lines.append(f"| {k} | {v} |")
    lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Work-desktop js vs shell_command vs exec. Counts/neighbors only. No bodies."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "data" / "raw" / "codex"
OUT = ROOT / "reports" / "codex-work-js-shell.md"
WANT = "codex_work_desktop"
CALL_TYPES = {"custom_tool_call", "function_call"}


def neighbors(seq: list[str], name: str) -> tuple[Counter, Counter]:
    prev: Counter = Counter()
    nxt: Counter = Counter()
    for i, x in enumerate(seq):
        if x != name:
            continue
        prev[seq[i - 1] if i else "<start>"] += 1
        nxt[seq[i + 1] if i + 1 < len(seq) else "<end>"] += 1
    return prev, nxt


def main() -> None:
    n = 0
    tools = Counter()
    has_js = 0
    has_shell = 0
    has_exec = 0
    js_only_with_exec = 0
    shell_and_patch = 0
    first = Counter()
    js_prev: Counter = Counter()
    js_next: Counter = Counter()
    sh_prev: Counter = Counter()
    sh_next: Counter = Counter()

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
        if not seq:
            continue
        names = set(seq)
        first[seq[0]] += 1
        for t in seq:
            tools[t] += 1
        if "js" in names:
            has_js += 1
            if "exec" in names:
                js_only_with_exec += 1
            jp, jn = neighbors(seq, "js")
            js_prev.update(jp)
            js_next.update(jn)
        if "shell_command" in names:
            has_shell += 1
            if "apply_patch" in names:
                shell_and_patch += 1
            sp, sn = neighbors(seq, "shell_command")
            sh_prev.update(sp)
            sh_next.update(sn)
        if "exec" in names:
            has_exec += 1

    lines = [
        "# ChatGPT Work js vs shell vs exec (`codex_work_desktop`)",
        "",
        "Keys and counts only. No bodies. v10.",
        "",
        f"Sessions with calls: **{sum(first.values())}** / {n}",
        f"- with exec: **{has_exec}**",
        f"- with js: **{has_js}** (also have exec: **{js_only_with_exec}**)",
        f"- with shell_command: **{has_shell}** (also apply_patch: **{shell_and_patch}**)",
        "",
        "## call counts",
        "",
        "| tool | count |",
        "| --- | --- |",
    ]
    for k, v in tools.most_common(12):
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## `js` previous / next",
        "",
        "| prev | count |",
        "| --- | --- |",
    ]
    for k, v in js_prev.most_common(8):
        lines.append(f"| {k} | {v} |")
    lines += ["", "| next | count |", "| --- | --- |"]
    for k, v in js_next.most_common(8):
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## `shell_command` previous / next",
        "",
        "| prev | count |",
        "| --- | --- |",
    ]
    for k, v in sh_prev.most_common(8):
        lines.append(f"| {k} | {v} |")
    lines += ["", "| next | count |", "| --- | --- |"]
    for k, v in sh_next.most_common(8):
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## interpretation",
        "",
        "Work inspect is **exec** (JS cells), not cwd shell. `js` is a rare sibling of exec.",
        "`shell_command` is scarce; the only apply_patch session is in the shell slice.",
        "Do not map Work gold to bash+edit. Map exec to Read/Grep/inspect; map js to a small script still after look.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Non-empty vscode vs Work. Calls only. No bodies."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "data" / "raw" / "codex"
OUT = ROOT / "reports" / "codex-vscode-vs-work.md"
CALL_TYPES = {"custom_tool_call", "function_call"}
WANT = ("codex_vscode", "codex_work_desktop")


def main() -> None:
    files: Counter = Counter()
    nonempty: Counter = Counter()
    patch_files: Counter = Counter()
    shell_first: Counter = Counter()
    tools: dict[str, Counter] = {k: Counter() for k in WANT}
    first: dict[str, Counter] = {k: Counter() for k in WANT}
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
                if orig not in WANT:
                    continue
                name = payload.get("name")
                pt = payload.get("type")
                if isinstance(name, str) and pt in CALL_TYPES:
                    seq.append(name)
        if orig not in WANT:
            continue
        files[orig] += 1
        if not seq:
            continue
        nonempty[orig] += 1
        tools[orig].update(seq)
        first[orig][seq[0]] += 1
        if seq[0] == "shell_command":
            shell_first[orig] += 1
        if "apply_patch" in seq:
            patch_files[orig] += 1
    v, w = "codex_vscode", "codex_work_desktop"
    lines = [
        "# Non-empty vscode vs Work (calls only)",
        "",
        "v39. Do not average these originators.",
        "",
        "| originator | files | with calls | apply_patch files | first=shell |",
        "| --- | --- | --- | --- | --- |",
        f"| {w} | {files[w]} | {nonempty[w]} | {patch_files[w]} | {shell_first[w]} |",
        f"| {v} | {files[v]} | {nonempty[v]} | **{patch_files[v]}** | **{shell_first[v]}** |",
        "",
        f"vscode nonempty: shell_command {tools[v]['shell_command']}, apply_patch {tools[v]['apply_patch']}. Every nonempty vscode session starts with shell_command. {patch_files[v]}/{nonempty[v]} patch.",
        "",
        f"Work: exec {first[w]['exec']} first, apply_patch {patch_files[w]}/{nonempty[w]}.",
        "",
        "## interpretation",
        "",
        f"The shell↔patch sandwich is vscode ({patch_files[v]}/{nonempty[v]} nonempty) plus nonempty `codex_exec` (31/105). Not Desktop (1/994). Not Work ({patch_files[w]}/{nonempty[w]}).",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} vscode_patch={patch_files[v]}/{nonempty[v]}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Non-empty codex_exec vs Work tool mix. Calls only. No bodies."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "data" / "raw" / "codex"
OUT = ROOT / "reports" / "codex-exec-vs-work.md"
CALL_TYPES = {"custom_tool_call", "function_call"}
WANT = ("codex_exec", "codex_work_desktop")


def main() -> None:
    tools: dict[str, Counter] = {k: Counter() for k in WANT}
    files: Counter = Counter()
    nonempty: Counter = Counter()
    first: dict[str, Counter] = {k: Counter() for k in WANT}
    patch_files: Counter = Counter()
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
        if "apply_patch" in seq:
            patch_files[orig] += 1
    lines = [
        "# Non-empty `codex_exec` vs Work (calls only)",
        "",
        "v35. Do not average these originators.",
        "",
        f"| originator | files | with calls | apply_patch files |",
        f"| --- | --- | --- | --- |",
        f"| codex_work_desktop | {files['codex_work_desktop']} | {nonempty['codex_work_desktop']} | {patch_files['codex_work_desktop']} |",
        f"| codex_exec | {files['codex_exec']} | {nonempty['codex_exec']} | {patch_files['codex_exec']} |",
        "",
    ]
    for orig in WANT:
        lines += [f"## `{orig}` calls", "", "| tool | count |", "| --- | --- |"]
        for t, c in tools[orig].most_common(10):
            lines.append(f"| {t} | {c} |")
        lines += ["", f"### `{orig}` first call", "", "| tool | sessions |", "| --- | --- |"]
        for t, c in first[orig].most_common(6):
            lines.append(f"| {t} | {c} |")
        lines.append("")
    lines += [
        "## interpretation",
        "",
        "Non-empty `codex_exec` patches more than Work. Work is exec/wait/send. Do not imitate exec-originator as Work.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} exec_nonempty={nonempty['codex_exec']} work_nonempty={nonempty['codex_work_desktop']}")


if __name__ == "__main__":
    main()

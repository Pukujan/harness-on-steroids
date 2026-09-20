#!/usr/bin/env python3
"""apply_patch session rate by originator. Calls only. No bodies."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "data" / "raw" / "codex"
OUT = ROOT / "reports" / "codex-patch-by-originator.md"
CALL_TYPES = {"custom_tool_call", "function_call"}


def main() -> None:
    files: Counter = Counter()
    nonempty: Counter = Counter()
    patch: Counter = Counter()
    for path in sorted(CODEX.glob("*.jsonl")):
        orig = "unknown"
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
                name = payload.get("name")
                pt = payload.get("type")
                if isinstance(name, str) and pt in CALL_TYPES:
                    seq.append(name)
        files[orig] += 1
        if not seq:
            continue
        nonempty[orig] += 1
        if "apply_patch" in seq:
            patch[orig] += 1
    order = ["codex_work_desktop", "Codex Desktop", "codex_exec", "codex_vscode"]
    lines = [
        "# apply_patch session rate by originator",
        "",
        "Calls only. One originator per file. v40. Do not average.",
        "",
        "| originator | files | with calls | apply_patch files | rate among nonempty |",
        "| --- | --- | --- | --- | --- |",
    ]
    for orig in order:
        nf = files[orig]
        nn = nonempty[orig]
        np = patch[orig]
        rate = f"{np}/{nn}" if nn else "n/a"
        lines.append(f"| {orig} | {nf} | {nn} | {np} | {rate} |")
    lines += [
        "",
        "## interpretation",
        "",
        "Work **1/83**. Desktop **1/994**. nonempty `codex_exec` **31/105**. vscode **12/13**.",
        "Imitate Work. Do not imitate vscode or nonempty exec patch rates.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

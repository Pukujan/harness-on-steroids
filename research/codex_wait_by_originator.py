#!/usr/bin/env python3
"""wait session rate by originator. Calls only. No bodies."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "data" / "raw" / "codex"
OUT = ROOT / "reports" / "codex-wait-by-originator.md"
CALL_TYPES = {"custom_tool_call", "function_call"}


def main() -> None:
    files: Counter = Counter()
    nonempty: Counter = Counter()
    wait: Counter = Counter()
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
        if "wait" in seq:
            wait[orig] += 1
    order = ["codex_work_desktop", "Codex Desktop", "codex_exec", "codex_vscode"]
    lines = [
        "# wait session rate by originator",
        "",
        "Calls only. One originator per file. v42. Do not average.",
        "",
        "| originator | files | with calls | wait files | rate among nonempty |",
        "| --- | --- | --- | --- | --- |",
    ]
    for orig in order:
        nf, nn, nw = files[orig], nonempty[orig], wait[orig]
        rate = f"{nw}/{nn}" if nn else "n/a"
        lines.append(f"| {orig} | {nf} | {nn} | {nw} | {rate} |")
    lines += [
        "",
        "## interpretation",
        "",
        "Work and Desktop wait on cells. vscode almost never waits (shell↔patch instead).",
        "Imitate Work wait-after-exec, not vscode.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

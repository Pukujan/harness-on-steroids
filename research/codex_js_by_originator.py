#!/usr/bin/env python3
"""js session rate by originator. Calls only. No bodies."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "data" / "raw" / "codex"
OUT = ROOT / "reports" / "codex-js-by-originator.md"
CALL_TYPES = {"custom_tool_call", "function_call"}


def main() -> None:
    files: Counter = Counter()
    nonempty: Counter = Counter()
    js: Counter = Counter()
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
        if "js" in seq:
            js[orig] += 1
    order = ["codex_work_desktop", "Codex Desktop", "codex_exec", "codex_vscode"]
    lines = [
        "# js session rate by originator",
        "",
        "Calls only. One originator per file. v50. Do not average.",
        "",
        "| originator | files | with calls | js files | rate among nonempty |",
        "| --- | --- | --- | --- | --- |",
    ]
    for orig in order:
        nf, nn, nj = files[orig], nonempty[orig], js[orig]
        rate = f"{nj}/{nn}" if nn else "n/a"
        lines.append(f"| {orig} | {nf} | {nn} | {nj} | {rate} |")
    lines += [
        "",
        "## interpretation",
        "",
        "Work `js` is rare (5/83) and sits next to exec. vscode is 1/13 js vs 13/13 cwd shell. Do not map Work inspect to bash.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

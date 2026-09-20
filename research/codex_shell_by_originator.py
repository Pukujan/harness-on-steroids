#!/usr/bin/env python3
"""shell_command session rate by originator. Calls only. No bodies."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "data" / "raw" / "codex"
OUT = ROOT / "reports" / "codex-shell-by-originator.md"
CALL_TYPES = {"custom_tool_call", "function_call"}


def main() -> None:
    files: Counter = Counter()
    nonempty: Counter = Counter()
    shell: Counter = Counter()
    shell_first: Counter = Counter()
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
        if "shell_command" in seq:
            shell[orig] += 1
        if seq[0] == "shell_command":
            shell_first[orig] += 1
    order = ["codex_work_desktop", "Codex Desktop", "codex_exec", "codex_vscode"]
    lines = [
        "# shell_command session rate by originator",
        "",
        "Calls only. One originator per file. v48. Do not average.",
        "",
        "| originator | files | with calls | shell_command files | shell first |",
        "| --- | --- | --- | --- | --- |",
    ]
    for orig in order:
        lines.append(
            f"| {orig} | {files[orig]} | {nonempty[orig]} | {shell[orig]} | {shell_first[orig]} |"
        )
    lines += [
        "",
        "## interpretation",
        "",
        "Work almost never cwd-shells. vscode always starts with shell. Do not bash as tool 1.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exec raw-string PREFIX classes only. Never write the rest of the command."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "data" / "raw" / "codex"
OUT = ROOT / "reports" / "codex-exec-prefix.md"


def prefix_class(s: str) -> str:
    t = s.lstrip()
    if not t:
        return "empty"
    if t.startswith("{"):
        return "json_object"
    low = t[:40].lower()
    if t.startswith(("const ", "let ", "await ", "import ", "async ", "function ", "(()", "/*")):
        return "js_source"
    if t.startswith("$"):
        return "ps_var"
    if low.startswith(("get-", "set-", "select-", "test-", "write-", "new-", "remove-", "copy-", "move-", "start-", "stop-", "invoke-")):
        return "ps_cmdlet"
    if low.startswith("git "):
        return "git"
    if low.startswith(("rg ", "grep ", "findstr ")):
        return "search"
    if low.startswith(("python", "py ", "node ", "npm ", "npx ", "cargo ", "pytest")):
        return "runtime"
    if low.startswith(("dir ", "ls ", "cat ", "type ", "head ")):
        return "fs_read"
    if t.startswith("***"):
        return "redacted"
    return "other"


def main() -> None:
    files = sorted(CODEX.glob("*.jsonl"))
    ctr = Counter()
    n = 0
    for path in files:
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                payload = obj.get("payload") if isinstance(obj.get("payload"), dict) else {}
                if payload.get("name") != "exec":
                    continue
                inp = payload.get("input")
                if not isinstance(inp, str):
                    ctr["non_string"] += 1
                    n += 1
                    continue
                ctr[prefix_class(inp)] += 1
                n += 1
    lines = [
        "# Codex `exec` prefix classes (no bodies)",
        "",
        f"exec string inputs classified: **{n}**",
        "",
        "| class | count |",
        "| --- | --- |",
    ]
    for k, v in ctr.most_common():
        lines.append(f"| {k} | {v} |")
    lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()

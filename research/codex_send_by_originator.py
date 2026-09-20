#!/usr/bin/env python3
"""send_message session rate by originator. Calls only. No bodies."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "data" / "raw" / "codex"
OUT = ROOT / "reports" / "codex-send-by-originator.md"
CALL_TYPES = {"custom_tool_call", "function_call"}


def main() -> None:
    files: Counter = Counter()
    nonempty: Counter = Counter()
    send: Counter = Counter()
    spawn: Counter = Counter()
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
        names = set(seq)
        if "send_message" in names:
            send[orig] += 1
        if "spawn_agent" in names:
            spawn[orig] += 1
    order = ["codex_work_desktop", "Codex Desktop", "codex_exec", "codex_vscode"]
    lines = [
        "# send_message / spawn_agent session rate by originator",
        "",
        "Calls only. One originator per file. v43. Do not average.",
        "",
        "| originator | files | with calls | send_message | spawn_agent |",
        "| --- | --- | --- | --- | --- |",
    ]
    for orig in order:
        lines.append(
            f"| {orig} | {files[orig]} | {nonempty[orig]} | {send[orig]} | {spawn[orig]} |"
        )
    lines += [
        "",
        "## interpretation",
        "",
        "Work splits with send_message, not vscode (0). spawn_agent is rare on Work.",
        "Imitate send-after-look. Do not imitate vscode (no send, all patch).",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

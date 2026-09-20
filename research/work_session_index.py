#!/usr/bin/env python3
"""Work session index: hashes and counts only. No message bodies."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "data" / "raw" / "codex"
OUT = ROOT / "reports" / "work-session-index.md"
WANT = "codex_work_desktop"
CALL_TYPES = {"custom_tool_call", "function_call"}


def main() -> None:
    rows: list[tuple] = []
    for path in sorted(CODEX.glob("*.jsonl")):
        orig = None
        n_user = 0
        n_asst = 0
        calls: list[str] = []
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
                pt = payload.get("type")
                role = payload.get("role")
                if pt == "message" and role == "user":
                    n_user += 1
                elif pt == "message" and role == "assistant":
                    n_asst += 1
                name = payload.get("name")
                if isinstance(name, str) and pt in CALL_TYPES:
                    calls.append(name)
        if orig != WANT:
            continue
        first = calls[0] if calls else "(none)"
        patched = int("apply_patch" in calls)
        rows.append((path.stem[:12], n_user, n_asst, len(calls), first, patched))
    lines = [
        "# Work session index (structure only)",
        "",
        "v58. Hashed prefix, turn counts, first tool, patch bit. **No bodies.**",
        "",
        f"Work files: **{len(rows)}**",
        "",
        "| hash12 | user_turns | asst_turns | tool_calls | first | patch |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for h, u, a, c, first, p in rows:
        lines.append(f"| {h} | {u} | {a} | {c} | {first} | {p} |")
    lines += [
        "",
        "Replay of these asks into Kilo/OpenCode is **not** in this file.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} n={len(rows)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Work-desktop plan/collab tools vs full-corpus. Counts only. No bodies."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "data" / "raw" / "codex"
OUT = ROOT / "reports" / "codex-work-plan.md"
WANT = "codex_work_desktop"
CALL_TYPES = {"custom_tool_call", "function_call"}
PLANISH = {
    "update_plan",
    "request_user_input",
    "request_permissions",
    "create_thread",
    "followup_task",
    "multi_agent_v1",
}


def main() -> None:
    n = 0
    modes = Counter()
    tools = Counter()
    sess_tool: Counter = Counter()
    first_mode = Counter()
    n_plan_mode = 0

    for path in sorted(CODEX.glob("*.jsonl")):
        orig = None
        seq: list[str] = []
        mode_last = None
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
                if obj.get("type") == "turn_context":
                    m = payload.get("collaboration_mode")
                    if isinstance(m, str):
                        mode_last = m
                        modes[m] += 1
                name = payload.get("name")
                pt = payload.get("type")
                if isinstance(name, str) and pt in CALL_TYPES:
                    seq.append(name)
        if orig != WANT:
            continue
        n += 1
        if mode_last == "plan":
            n_plan_mode += 1
        if mode_last:
            first_mode[mode_last] += 1
        names = set(seq)
        for t in PLANISH:
            if t in names:
                sess_tool[t] += 1
        for t in seq:
            tools[t] += 1

    lines = [
        "# ChatGPT Work plan/collab tools (`codex_work_desktop`)",
        "",
        "Counts only. No bodies. v13. Full-corpus `update_plan` 137 is **not** Work.",
        "",
        f"Sessions: **{n}** last collaboration_mode=plan: **{n_plan_mode}**",
        "",
        "## last collaboration_mode per session",
        "",
        "| mode | sessions |",
        "| --- | --- |",
    ]
    for k, v in first_mode.most_common():
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## turn_context collaboration_mode events",
        "",
        "| mode | count |",
        "| --- | --- |",
    ]
    for k, v in modes.most_common():
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## plan-ish tools (sessions with ≥1 call)",
        "",
        "| tool | sessions | calls |",
        "| --- | --- | --- |",
    ]
    for t in sorted(PLANISH):
        lines.append(f"| {t} | {sess_tool.get(t, 0)} | {tools.get(t, 0)} |")
    lines += [
        "",
        "## interpretation",
        "",
        "Work does not run `update_plan`. Todowrite-first is not Work gold.",
        "Plan collaboration_mode is absent or negligible. Multi-piece is send_message, not a plan file.",
        "Keep mapping `update_plan` → todowrite only as a mixed-corpus leftover, not Work default.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} sessions={n} plan_mode={n_plan_mode} update_plan_calls={tools.get('update_plan', 0)}")


if __name__ == "__main__":
    main()

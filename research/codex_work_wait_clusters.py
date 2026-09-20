#!/usr/bin/env python3
"""Work-desktop consecutive wait / wait_agent cluster lengths. Counts only."""

from __future__ import annotations

import json
import statistics
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "data" / "raw" / "codex"
OUT = ROOT / "reports" / "codex-work-wait-clusters.md"
WANT = "codex_work_desktop"
CALL_TYPES = {"custom_tool_call", "function_call"}


def run_lengths(seq: list[str], name: str) -> list[int]:
    runs: list[int] = []
    n = 0
    for x in seq:
        if x == name:
            n += 1
        elif n:
            runs.append(n)
            n = 0
    if n:
        runs.append(n)
    return runs


def after_runs(seq: list[str], name: str) -> Counter:
    nxt: Counter = Counter()
    n = 0
    for x in seq:
        if x == name:
            n += 1
            continue
        if n:
            nxt[x] += 1
            n = 0
    if n:
        nxt["<end>"] += 1
    return nxt


def bucket(n: int) -> str:
    if n <= 5:
        return str(n)
    if n <= 10:
        return "6-10"
    return "11+"


def median(xs: list[int]) -> str:
    if not xs:
        return "n/a"
    return str(int(statistics.median(xs)))


def main() -> None:
    n = 0
    wait_runs: list[int] = []
    agent_runs: list[int] = []
    wait_buckets: Counter = Counter()
    agent_buckets: Counter = Counter()
    after_wait = Counter()
    after_agent = Counter()
    sess_wait_ge2 = 0
    sess_wait = 0

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
                if orig != WANT:
                    continue
                name = payload.get("name")
                pt = payload.get("type")
                if isinstance(name, str) and pt in CALL_TYPES:
                    seq.append(name)
        if orig != WANT:
            continue
        n += 1
        wr = run_lengths(seq, "wait")
        ar = run_lengths(seq, "wait_agent")
        if wr:
            sess_wait += 1
            if any(x >= 2 for x in wr):
                sess_wait_ge2 += 1
        wait_runs.extend(wr)
        agent_runs.extend(ar)
        for r in wr:
            wait_buckets[bucket(r)] += 1
        for r in ar:
            agent_buckets[bucket(r)] += 1
        after_wait.update(after_runs(seq, "wait"))
        after_agent.update(after_runs(seq, "wait_agent"))

    lines = [
        "# ChatGPT Work wait clusters (`codex_work_desktop`)",
        "",
        "Counts only. No bodies. v11.",
        "",
        f"Sessions: **{n}** with wait: **{sess_wait}** with wait-run length ≥2: **{sess_wait_ge2}**",
        f"- wait-runs: **{len(wait_runs)}** median **{median(wait_runs)}**",
        f"- wait_agent-runs: **{len(agent_runs)}** median **{median(agent_runs)}**",
        "",
        "## wait-run length buckets",
        "",
        "| length | runs |",
        "| --- | --- |",
    ]
    for k in ("1", "2", "3", "4", "5", "6-10", "11+"):
        lines.append(f"| {k} | {wait_buckets.get(k, 0)} |")
    lines += [
        "",
        "## wait_agent-run length buckets",
        "",
        "| length | runs |",
        "| --- | --- |",
    ]
    for k in ("1", "2", "3", "4", "5", "6-10", "11+"):
        lines.append(f"| {k} | {agent_buckets.get(k, 0)} |")
    lines += [
        "",
        "## next after a wait-run",
        "",
        "| next | count |",
        "| --- | --- |",
    ]
    for k, v in after_wait.most_common(8):
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## next after a wait_agent-run",
        "",
        "| next | count |",
        "| --- | --- |",
    ]
    for k, v in after_agent.most_common(8):
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## interpretation",
        "",
        "Work often **waits more than once** before looking again. After a wait-run, next is usually exec.",
        "After wait_agent, next is list_agents / send_message / exec, not apply_patch.",
        "Imitate: if you wait on a cell or child, you may wait again. Do not patch when the wait ends.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} wait_runs={len(wait_runs)} agent_runs={len(agent_runs)}")


if __name__ == "__main__":
    main()

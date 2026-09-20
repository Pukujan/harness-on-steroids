#!/usr/bin/env python3
"""Work-desktop exec-run lengths and wait/send insertion. Keys/counts only."""

from __future__ import annotations

import json
import statistics
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "data" / "raw" / "codex"
OUT = ROOT / "reports" / "codex-work-wait.md"
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
    for i, x in enumerate(seq):
        if x == name:
            n += 1
            continue
        if n:
            nxt[x] += 1
            n = 0
    if n:
        nxt["<end>"] += 1
    return nxt


def neighbors(seq: list[str], name: str) -> tuple[Counter, Counter]:
    prev: Counter = Counter()
    nxt: Counter = Counter()
    for i, x in enumerate(seq):
        if x != name:
            continue
        prev[seq[i - 1] if i else "<start>"] += 1
        nxt[seq[i + 1] if i + 1 < len(seq) else "<end>"] += 1
    return prev, nxt


def bucket(n: int) -> str:
    if n <= 5:
        return str(n)
    if n <= 10:
        return "6-10"
    if n <= 20:
        return "11-20"
    if n <= 50:
        return "21-50"
    return "51+"


def median(xs: list[int]) -> str:
    if not xs:
        return "n/a"
    return str(int(statistics.median(xs)))


def main() -> None:
    n = 0
    exec_runs: list[int] = []
    after_exec = Counter()
    wait_prev: Counter = Counter()
    wait_next: Counter = Counter()
    send_prev: Counter = Counter()
    send_next: Counter = Counter()
    wait_after_exec_run = 0
    patch_after_exec_run = 0
    send_after_exec_run = 0
    end_after_exec_run = 0
    run_buckets: Counter = Counter()
    sess_with_wait = 0
    wait_then_exec = 0
    wait_then_wait = 0

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
        if not seq:
            continue
        runs = run_lengths(seq, "exec")
        exec_runs.extend(runs)
        for r in runs:
            run_buckets[bucket(r)] += 1
        ae = after_runs(seq, "exec")
        after_exec.update(ae)
        wait_after_exec_run += ae.get("wait", 0)
        patch_after_exec_run += ae.get("apply_patch", 0)
        send_after_exec_run += ae.get("send_message", 0)
        end_after_exec_run += ae.get("<end>", 0)
        if "wait" in seq:
            sess_with_wait += 1
            wp, wn = neighbors(seq, "wait")
            wait_prev.update(wp)
            wait_next.update(wn)
            wait_then_exec += wn.get("exec", 0)
            wait_then_wait += wn.get("wait", 0)
        if "send_message" in seq:
            sp, sn = neighbors(seq, "send_message")
            send_prev.update(sp)
            send_next.update(sn)

    lines = [
        "# ChatGPT Work wait / exec-run insertion (`codex_work_desktop`)",
        "",
        "Keys and counts only. No bodies. v9.",
        "",
        f"Sessions: **{n}** with wait: **{sess_with_wait}**",
        f"- exec-runs: **{len(exec_runs)}** median length **{median(exec_runs)}**",
        f"- after an exec-run: wait **{wait_after_exec_run}**, send_message **{send_after_exec_run}**, apply_patch **{patch_after_exec_run}**, end **{end_after_exec_run}**",
        "",
        "## exec-run length buckets",
        "",
        "| length | runs |",
        "| --- | --- |",
    ]
    for k in ("1", "2", "3", "4", "5", "6-10", "11-20", "21-50", "51+"):
        lines.append(f"| {k} | {run_buckets.get(k, 0)} |")
    lines += [
        "",
        "## next tool after an exec-run",
        "",
        "| next | count |",
        "| --- | --- |",
    ]
    for k, v in after_exec.most_common(12):
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## `wait` previous / next",
        "",
        "| prev | count |",
        "| --- | --- |",
    ]
    for k, v in wait_prev.most_common(8):
        lines.append(f"| {k} | {v} |")
    lines += ["", "| next | count |", "| --- | --- |"]
    for k, v in wait_next.most_common(8):
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## `send_message` previous / next",
        "",
        "| prev | count |",
        "| --- | --- |",
    ]
    for k, v in send_prev.most_common(8):
        lines.append(f"| {k} | {v} |")
    lines += ["", "| next | count |", "| --- | --- |"]
    for k, v in send_next.most_common(8):
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## interpretation",
        "",
        "After a short exec burst, Work **waits or sends**, almost never patches.",
        "wait is usually exec → wait → exec (or wait → wait). send_message sits between exec bursts.",
        "Do not treat a long look-then-patch sandwich as Work gold.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} sessions={n} runs={len(exec_runs)}")


if __name__ == "__main__":
    main()

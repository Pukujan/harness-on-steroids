#!/usr/bin/env python3
"""Work-desktop send_message / spawn task-split. Counts only. No bodies."""

from __future__ import annotations

import json
import statistics
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "data" / "raw" / "codex"
OUT = ROOT / "reports" / "codex-work-send.md"
WANT = "codex_work_desktop"
CALL_TYPES = {"custom_tool_call", "function_call"}


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
    n_send = 0
    n_spawn = 0
    n_both = 0
    n_list = 0
    n_wait_agent = 0
    n_send_and_patch = 0
    sends_per: list[int] = []
    send_buckets: Counter = Counter()
    idx_first_send: list[int] = []
    after_last_send: Counter = Counter()
    between_sends: Counter = Counter()
    spawn_also_send = 0

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
        names = set(seq)
        sc = seq.count("send_message")
        if sc:
            n_send += 1
            sends_per.append(sc)
            send_buckets[bucket(sc)] += 1
            idx_first_send.append(seq.index("send_message"))
            last = max(i for i, t in enumerate(seq) if t == "send_message")
            after_last_send[seq[last + 1] if last + 1 < len(seq) else "<end>"] += 1
            idxs = [i for i, t in enumerate(seq) if t == "send_message"]
            for a, b in zip(idxs, idxs[1:]):
                mid = seq[a + 1 : b]
                if not mid:
                    between_sends["<adjacent>"] += 1
                elif all(x == "exec" for x in mid):
                    between_sends["exec-only"] += 1
                elif "wait_agent" in mid:
                    between_sends["has-wait_agent"] += 1
                elif "wait" in mid:
                    between_sends["has-wait"] += 1
                else:
                    between_sends["other"] += 1
        if "spawn_agent" in names:
            n_spawn += 1
            if sc:
                n_both += 1
                spawn_also_send += 1
        if "list_agents" in names:
            n_list += 1
        if "wait_agent" in names:
            n_wait_agent += 1
        if sc and "apply_patch" in names:
            n_send_and_patch += 1

    lines = [
        "# ChatGPT Work send_message task split (`codex_work_desktop`)",
        "",
        "Counts only. No bodies. v12.",
        "",
        f"Sessions: **{n}**",
        f"- send_message: **{n_send}**",
        f"- spawn_agent: **{n_spawn}**",
        f"- both send and spawn: **{n_both}**",
        f"- list_agents: **{n_list}**",
        f"- wait_agent: **{n_wait_agent}**",
        f"- send and apply_patch: **{n_send_and_patch}**",
        f"- median sends/session (among senders): **{median(sends_per)}**",
        f"- median index of first send: **{median(idx_first_send)}**",
        "",
        "## sends per sending session",
        "",
        "| sends | sessions |",
        "| --- | --- |",
    ]
    for k in ("1", "2", "3", "4", "5", "6-10", "11+"):
        lines.append(f"| {k} | {send_buckets.get(k, 0)} |")
    lines += [
        "",
        "## after last send_message",
        "",
        "| next | sessions |",
        "| --- | --- |",
    ]
    for k, v in after_last_send.most_common():
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## between consecutive sends",
        "",
        "| gap | count |",
        "| --- | --- |",
    ]
    for k, v in between_sends.most_common():
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## interpretation",
        "",
        "Work splits multi-piece work with **repeated send_message**, not spawn_agent.",
        "spawn_agent is 2 sessions. send+patch is 0. After the last send, look (exec) or stop.",
        "Between sends, look (exec-only) or wait. Do not insert apply_patch.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} send_sessions={n_send} spawn={n_spawn}")


if __name__ == "__main__":
    main()

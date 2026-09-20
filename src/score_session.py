"""Score Kilo/OpenCode sqlite sessions against Work-gold relations. No bodies."""

from __future__ import annotations

import json
import sqlite3
import statistics
from collections import Counter
from pathlib import Path

WRITE = {"edit", "write", "patch"}
LOOK = {
    "read",
    "grep",
    "glob",
    "webfetch",
    "websearch",
    "semantic_search",
    "kilo_local_recall",
    "skill",
}
LOOKISH = LOOK | {"bash"}
DECOMPOSE = {"task", "todowrite", "agent_manager"}


def _first_index(seq: list[str], names: set[str]) -> int | None:
    for i, x in enumerate(seq):
        if x in names:
            return i
    return None


def start_look_burst(seq: list[str]) -> int:
    n = 0
    for x in seq:
        if x in LOOKISH:
            n += 1
        else:
            break
    return n


def write_after_look_run(seq: list[str]) -> bool:
    """Work: apply_patch after an exec-run is 0. Look-run then edit fails R5."""
    n = 0
    for x in seq:
        if x in LOOKISH:
            n += 1
            continue
        if n and x in WRITE:
            return True
        n = 0
    return False


def _tools(db: Path) -> dict[str, list[str]]:
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    by: dict[str, list[str]] = {}
    for sid, _ts, raw in con.execute(
        "SELECT session_id, time_created, data FROM part ORDER BY session_id, time_created"
    ):
        obj = json.loads(raw)
        t = obj.get("type")
        name = None
        if t == "patch":
            name = "patch"
        elif t == "tool":
            tool = obj.get("tool")
            if isinstance(tool, str):
                name = tool
        if name:
            by.setdefault(sid, []).append(name)
    con.close()
    return by


def score_seq(seq: list[str]) -> dict:
    if not seq:
        return {
            "r1": None,
            "r5_wait": False,
            "wrote": False,
            "r2_no_write": True,
            "r6_decompose_not_first": True,
            "r5_no_write_after_look_run": True,
            "r4_no_todowrite": True,
            "wrote_without_task": False,
            "start_look_burst": 0,
            "tools_before_write": None,
            "tools_before_decompose": None,
        }
    first = seq[0]
    r1 = first not in WRITE
    wrote = any(x in WRITE for x in seq)
    has_todo = "todowrite" in seq
    has_task = "task" in seq
    waitish = any(x in {"task", "schedule_wakeup", "background_process"} for x in seq)
    look_after = False
    wi = _first_index(seq, WRITE)
    if wrote and wi is not None:
        look_after = any(x in LOOKISH for x in seq[wi + 1 :])
    di = _first_index(seq, DECOMPOSE)
    return {
        "first": first,
        "r1_look_first": r1,
        "r2_no_write": not wrote,
        "r6_decompose_not_first": first not in DECOMPOSE,
        "r5_no_write_after_look_run": not write_after_look_run(seq),
        "r4_no_todowrite": not has_todo,
        "wrote_without_task": wrote and not has_task,
        "wrote": wrote,
        "look_after_write": look_after,
        "multi_piece": waitish or has_task,
        "start_look_burst": start_look_burst(seq),
        "tools_before_write": wi,
        "tools_before_decompose": di,
    }


def summarize(db: Path, skip_prefixes: tuple[str, ...] = ("study-os",)) -> dict:
    seqs = _tools(db)
    n = 0
    r1_ok = 0
    r2_ok = 0
    r6_ok = 0
    r5_ok = 0
    r4_ok = 0
    write_first = 0
    wrote_without_task_n = 0
    todo_n = 0
    decompose_first = 0
    wrote_n = 0
    sandwich = 0
    skipped = 0
    firsts = Counter()
    bursts: list[int] = []
    before_write: list[int] = []
    before_decomp: list[int] = []
    for seq in seqs.values():
        if not seq:
            continue
        if any(any(x.startswith(p) for p in skip_prefixes) for x in seq):
            skipped += 1
            continue
        n += 1
        s = score_seq(seq)
        firsts[s["first"]] += 1
        bursts.append(int(s["start_look_burst"]))
        if s["r1_look_first"]:
            r1_ok += 1
        else:
            write_first += 1
        if s["r2_no_write"]:
            r2_ok += 1
        if s["r6_decompose_not_first"]:
            r6_ok += 1
        else:
            decompose_first += 1
        if s["r5_no_write_after_look_run"]:
            r5_ok += 1
        if s["r4_no_todowrite"]:
            r4_ok += 1
        else:
            todo_n += 1
        if s["wrote_without_task"]:
            wrote_without_task_n += 1
        if s["wrote"]:
            wrote_n += 1
            if s["look_after_write"]:
                sandwich += 1
            if s["tools_before_write"] is not None:
                before_write.append(int(s["tools_before_write"]))
        if s["tools_before_decompose"] is not None:
            before_decomp.append(int(s["tools_before_decompose"]))
    return {
        "db": db.name,
        "sessions_with_tools": n,
        "skipped_study_os": skipped,
        "r1_look_first": r1_ok,
        "r2_no_write": r2_ok,
        "r6_decompose_not_first": r6_ok,
        "r5_no_write_after_look_run": r5_ok,
        "r4_no_todowrite": r4_ok,
        "todowrite_sessions": todo_n,
        "wrote_without_task": wrote_without_task_n,
        "decompose_first": decompose_first,
        "write_rate": (wrote_n / n) if n else 0.0,
        "write_first": write_first,
        "wrote": wrote_n,
        "sandwich_look_after_write": sandwich,
        "median_start_look_burst": int(statistics.median(bursts)) if bursts else None,
        "median_tools_before_write": int(statistics.median(before_write)) if before_write else None,
        "median_tools_before_decompose": int(statistics.median(before_decomp)) if before_decomp else None,
        "multi_piece": sum(
            1
            for seq in seqs.values()
            if seq
            and not any(any(x.startswith(p) for p in skip_prefixes) for x in seq)
            and score_seq(seq)["multi_piece"]
        ),
        "firsts": firsts.most_common(8),
    }

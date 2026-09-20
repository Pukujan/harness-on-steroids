"""Score Kilo/OpenCode sqlite sessions against Work-gold relations. No bodies."""

from __future__ import annotations

import json
import sqlite3
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
        return {"r1": None, "r5_wait": False, "wrote": False}
    first = seq[0]
    r1 = first not in WRITE
    wrote = any(x in WRITE for x in seq)
    waitish = any(x in {"task", "todowrite", "schedule_wakeup", "background_process"} for x in seq)
    look_after = False
    if wrote:
        wi = next(i for i, x in enumerate(seq) if x in WRITE)
        look_after = any(x in LOOK or x == "bash" for x in seq[wi + 1 :])
    return {
        "first": first,
        "r1_look_first": r1,
        "wrote": wrote,
        "look_after_write": look_after,
        "multi_piece": waitish or seq.count("task") > 0,
    }


def summarize(db: Path, skip_prefixes: tuple[str, ...] = ("study-os",)) -> dict:
    seqs = _tools(db)
    n = 0
    r1_ok = 0
    write_first = 0
    wrote_n = 0
    sandwich = 0
    skipped = 0
    firsts = Counter()
    for seq in seqs.values():
        if not seq:
            continue
        if any(any(x.startswith(p) for p in skip_prefixes) for x in seq):
            skipped += 1
            continue
        n += 1
        s = score_seq(seq)
        firsts[s["first"]] += 1
        if s["r1_look_first"]:
            r1_ok += 1
        else:
            write_first += 1
        if s["wrote"]:
            wrote_n += 1
            if s["look_after_write"]:
                sandwich += 1
    return {
        "db": db.name,
        "sessions_with_tools": n,
        "skipped_study_os": skipped,
        "r1_look_first": r1_ok,
        "write_first": write_first,
        "wrote": wrote_n,
        "sandwich_look_after_write": sandwich,
        "multi_piece": sum(
            1
            for seq in seqs.values()
            if seq
            and not any(any(x.startswith(p) for p in skip_prefixes) for x in seq)
            and score_seq(seq)["multi_piece"]
        ),
        "firsts": firsts.most_common(8),
    }

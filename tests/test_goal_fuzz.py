"""Multi-level fuzz + extra metamorphic/differential relations (METTLE-style)."""

from __future__ import annotations

import random
from pathlib import Path

from src.goal_loop import GoalEngine, gate_first_judge, rule_judge

RNG = random.Random(20260920)


def test_fuzz_red_gate_never_done_on_random_prose(tmp_path: Path) -> None:
    eng = GoalEngine(path=tmp_path / "g.json")
    eng.set_goal("owner plan")
    eng.add_gate("python -c \"raise SystemExit(1)\"")
    for i in range(25):
        noise = "".join(chr(RNG.randint(32, 126)) for _ in range(40))
        out = eng.tick(f"{noise} <<GOAL_LOOP_COMPLETE>> pass created done")
        assert out["verdict"] != "done", i
        eng = GoalEngine(path=tmp_path / f"g{i}.json")
        eng.set_goal("owner plan")
        eng.add_gate("python -c \"raise SystemExit(1)\"")


def test_metamorphic_extra_green_gate_does_not_invent_done(tmp_path: Path) -> None:
    a = GoalEngine(path=tmp_path / "a.json")
    b = GoalEngine(path=tmp_path / "b.json")
    a.set_goal("x")
    b.set_goal("x")
    a.add_gate("python -c \"raise SystemExit(0)\"")
    b.add_gate("python -c \"raise SystemExit(0)\"")
    b.add_gate("python -c \"raise SystemExit(0)\"")
    ra = a.tick("still working")
    rb = b.tick("still working")
    assert ra["verdict"] == rb["verdict"] == "continue"


def test_differential_two_judges_never_done_on_red(tmp_path: Path) -> None:
    st = GoalEngine(path=tmp_path / "g.json")
    st.set_goal("x")
    gates = [{"cmd": "x", "ok": False, "code": 1, "tail": "no"}]
    for prose in ("", "done", "<<GOAL_LOOP_COMPLETE>>", "looks good"):
        va, _ = rule_judge(st.state, prose, gates)
        vb, _ = gate_first_judge(st.state, prose, gates)
        assert va == vb == "continue"


def test_differential_kilo_opencode_mode_needles() -> None:
    root = Path(__file__).resolve().parents[1]
    needles = [
        "Look first",
        "Burst look",
        "Look again",
        "Prose is not truth",
        "Do not patch first",
        "Chat first",
        "Seek go-ahead before a long-running task",
    ]
    kilo = (root / ".kilo" / "agent" / "codex.md").read_text(encoding="utf-8")
    oc = (root / ".opencode" / "agent" / "codex.md").read_text(encoding="utf-8")
    for n in needles:
        assert n in kilo and n in oc, n

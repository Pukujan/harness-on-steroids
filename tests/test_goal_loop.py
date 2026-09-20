from __future__ import annotations

import json
from pathlib import Path

from src.goal_loop import GoalEngine, gate_first_judge, load_state, rule_judge


def test_cli_gate_accepts_pytest_flags(tmp_path: Path) -> None:
    from src.goal_cli import main

    state = tmp_path / "g.json"
    assert main(["--state", str(state), "set", "x"]) == 0
    assert main(["--state", str(state), "gate", "--cmd", "python -m pytest -q"]) == 0
    st = json.loads(state.read_text(encoding="utf-8"))
    assert "pytest" in st["gates"][0]


def test_spec_exists() -> None:
    spec = json.loads(Path("spec/goal-loop.v1.json").read_text(encoding="utf-8"))
    assert "done" in spec["verdicts"]
    assert spec["defaults"]["max_turns"] == 20


def test_set_tick_continue_then_done(tmp_path: Path) -> None:
    eng = GoalEngine(path=tmp_path / "g.json")
    eng.set_goal("create notes", max_turns=5)
    r1 = eng.tick("working on it")
    assert r1["verdict"] == "continue" and r1["continue"] is True
    r2 = eng.tick("<<GOAL_LOOP_COMPLETE>>")
    assert r2["verdict"] == "done"
    assert load_state(tmp_path / "g.json").status == "done"


def test_property_green_gate_without_done_marker_continues(tmp_path: Path) -> None:
    eng = GoalEngine(path=tmp_path / "g.json")
    eng.set_goal("x")
    eng.add_gate("python -c \"raise SystemExit(0)\"")
    out = eng.tick("pytest tests pass, still working")
    assert out["verdict"] == "continue"


def test_property_red_gate_never_done(tmp_path: Path) -> None:
    eng = GoalEngine(path=tmp_path / "g.json")
    eng.set_goal("x")
    eng.add_gate("python -c \"raise SystemExit(1)\"")
    out = eng.tick("<<GOAL_LOOP_COMPLETE>>")
    assert out["verdict"] != "done"


def test_property_budget_pauses(tmp_path: Path) -> None:
    eng = GoalEngine(path=tmp_path / "g.json")
    eng.set_goal("x", max_turns=2)
    eng.tick("still going")
    eng.tick("still going")
    assert eng.state.status == "paused"
    assert eng.state.turns >= 2


def test_property_judge_error_fail_open(tmp_path: Path) -> None:
    def boom(*_a, **_k):
        raise RuntimeError("judge down")

    eng = GoalEngine(path=tmp_path / "g.json", judge=boom)
    eng.set_goal("x", max_turns=5)
    out = eng.tick("hello")
    assert out["verdict"] == "continue"
    assert "fail-open" in out["reason"]


def test_property_new_goal_clears_subgoals(tmp_path: Path) -> None:
    eng = GoalEngine(path=tmp_path / "g.json")
    eng.set_goal("a")
    eng.add_subgoal("also b")
    eng.set_goal("c")
    assert eng.state.subgoals == []
    assert eng.state.text == "c"


def test_differential_judges_agree_on_red_gate(tmp_path: Path) -> None:
    eng = GoalEngine(path=tmp_path / "g.json")
    eng.set_goal("x")
    eng.add_gate("python -c \"raise SystemExit(2)\"")
    gates = [{"cmd": "x", "ok": False, "code": 2, "tail": "fail"}]
    a, _ = rule_judge(eng.state, "<<GOAL_LOOP_COMPLETE>>", gates)
    b, _ = gate_first_judge(eng.state, "<<GOAL_LOOP_COMPLETE>>", gates)
    assert a == b == "continue"


def test_metamorphic_whitespace_goal_same_done(tmp_path: Path) -> None:
    e1 = GoalEngine(path=tmp_path / "a.json")
    e2 = GoalEngine(path=tmp_path / "b.json")
    e1.set_goal("fix tests")
    e2.set_goal("  fix tests  \n")
    r1 = e1.tick("<<GOAL_LOOP_COMPLETE>>")
    r2 = e2.tick("<<GOAL_LOOP_COMPLETE>>")
    assert r1["verdict"] == r2["verdict"] == "done"


def test_live_fake_agent_with_gate(tmp_path: Path) -> None:
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    n = {"i": 0}

    def agent() -> str:
        n["i"] += 1
        (scratch / f"note_{n['i']}.txt").write_text(str(n["i"]), encoding="utf-8")
        left = 4 - n["i"]
        if left <= 0:
            return "created all four files. <<GOAL_LOOP_COMPLETE>>"
        return f"created note_{n['i']}.txt, {left} remain"

    gate_py = tmp_path / "gate.py"
    gate_py.write_text(
        "import pathlib, sys\n"
        f"p = pathlib.Path(r'{scratch}')\n"
        "sys.exit(0 if len(list(p.glob('note_*.txt'))) >= 4 else 1)\n",
        encoding="utf-8",
    )
    eng = GoalEngine(path=tmp_path / "g.json")
    eng.set_goal("create four note files", max_turns=10)
    eng.add_gate(f'python "{gate_py}"')
    last = "start"
    for _ in range(10):
        last = agent()
        out = eng.tick(last, cwd=scratch)
        if out["verdict"] == "done":
            break
    assert out["verdict"] == "done"
    assert n["i"] == 4

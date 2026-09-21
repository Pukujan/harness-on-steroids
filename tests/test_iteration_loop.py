from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_iteration_loop_spec_exists() -> None:
    text = (ROOT / "spec" / "iteration-loop.md").read_text(encoding="utf-8")
    for needle in (
        "Measure Codex gold",
        "Kilo mode",
        "OpenCode mode",
        "Differential check",
        "Gap report",
        "work_match",
        "Do not start coding first",
        "Decompose into tasks",
    ):
        assert needle in text, needle


def test_plan_requires_repeat_until_modes_exist() -> None:
    plan = (ROOT / "PLAN.md").read_text(encoding="utf-8")
    assert "### C — Kilo mode" in plan
    assert "### D — OpenCode mode" in plan
    assert "### G — Work research, planning, provenance" in plan
    assert "### H — Durable evidence" in plan
    assert "### I — Portable Codex pack" in plan
    issues = (ROOT / "ISSUES.md").read_text(encoding="utf-8")
    assert "12. Iteration loop until behavior matches" in issues
    assert "Iteration loop until behavior matches" in issues

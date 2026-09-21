from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_iteration_loop_spec_is_small_empirical_loop() -> None:
    text = (ROOT / "spec" / "iteration-loop.md").read_text(encoding="utf-8")
    for needle in (
        "one hypothesis",
        "Pi + OpenCode + Grok Build",
        "complete observable trajectory",
        "prompt/context first",
        "Same model across harnesses is useful but not required",
        "A runtime state machine is **not required**",
        "No substantial architecture-only slice",
        "sealed holdout",
    ):
        assert needle in text, needle


def test_plan_and_current_name_active_baseline() -> None:
    plan = (ROOT / "PLAN.md").read_text(encoding="utf-8")
    for needle in (
        "Large destination, tiny verified steps.",
        "### M0 - Governance reset - DONE",
        "### M1 - Multi-harness baseline - ACTIVE",
        "### M5 - Runtime enforcement only if earned",
        "GitHub issue #2",
    ):
        assert needle in plan, needle

    current = (ROOT / "checkpoints" / "CURRENT.md").read_text(encoding="utf-8")
    assert "Do not change prompts/control before this baseline." in current
    assert "Do not build a general state machine or protocol framework in this slice." in current

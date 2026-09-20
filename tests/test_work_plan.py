from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_work_plan_report_locks_v13() -> None:
    text = (ROOT / "reports" / "codex-work-plan.md").read_text(encoding="utf-8")
    for n in (
        "last collaboration_mode=plan: **0**",
        "| update_plan | 0 | 0 |",
        "| request_user_input | 0 | 0 |",
        "Work does not run `update_plan`",
    ):
        assert n in text, n


def test_modes_and_spec_drop_todowrite_as_work_gold() -> None:
    spec = (ROOT / "spec" / "codex-imitate-mode.md").read_text(encoding="utf-8")
    kilo = (ROOT / ".kilo" / "agent" / "codex.md").read_text(encoding="utf-8")
    oc = (ROOT / ".opencode" / "agent" / "codex.md").read_text(encoding="utf-8")
    assert "Work `update_plan` is **0**" in spec
    assert "Do not Todowrite — Work `update_plan` is 0" in kilo
    assert "Do not Todowrite — Work `update_plan` is 0" in oc

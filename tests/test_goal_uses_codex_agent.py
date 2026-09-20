from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_kilo_and_opencode_goal_commands_select_codex_agent() -> None:
    kilo = (ROOT / ".kilo" / "command" / "goal.md").read_text(encoding="utf-8")
    oc = (ROOT / ".opencode" / "command" / "goal.md").read_text(encoding="utf-8")
    assert "agent: codex" in kilo
    assert "agent: codex" in oc

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_kilo_does_not_shadow_reserved_goal_command() -> None:
    """Kilo's product /goal 500s if a custom command/goal.md exists."""
    kilo = ROOT / ".kilo" / "command" / "goal.md"
    assert not kilo.is_file(), "do not add .kilo/command/goal.md; it shadows reserved /goal"


def test_opencode_goal_command_selects_codex_agent() -> None:
    oc = (ROOT / ".opencode" / "command" / "goal.md").read_text(encoding="utf-8")
    assert "agent: codex" in oc

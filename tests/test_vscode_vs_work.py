from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_vscode_nonempty_is_the_sandwich() -> None:
    text = (ROOT / "reports" / "codex-vscode-vs-work.md").read_text(encoding="utf-8")
    for n in (
        "| codex_work_desktop | 87 | 83 | 1 | 2 |",
        "| codex_vscode | 16 | 13 | **12** | **13** |",
        "12/13 patch",
        "Every nonempty vscode session starts with shell_command",
    ):
        assert n in text, n

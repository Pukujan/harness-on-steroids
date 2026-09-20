from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_send_is_work_not_vscode() -> None:
    text = (ROOT / "reports" / "codex-send-by-originator.md").read_text(encoding="utf-8")
    for n in (
        "| codex_work_desktop | 87 | 83 | 25 | 2 |",
        "| Codex Desktop | 1103 | 994 | 17 | 3 |",
        "| codex_exec | 315 | 105 | 0 | 0 |",
        "| codex_vscode | 16 | 13 | 0 | 0 |",
        "Work splits with send_message, not vscode (0)",
    ):
        assert n in text, n

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_work_almost_never_cwd_shells() -> None:
    text = (ROOT / "reports" / "codex-shell-by-originator.md").read_text(encoding="utf-8")
    for n in (
        "| codex_work_desktop | 87 | 83 | 2 | 2 |",
        "| Codex Desktop | 1103 | 994 | 4 | 1 |",
        "| codex_exec | 315 | 105 | 45 | 37 |",
        "| codex_vscode | 16 | 13 | 13 | 13 |",
        "Do not bash as tool 1",
    ):
        assert n in text, n

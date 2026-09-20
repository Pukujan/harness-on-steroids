from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_work_js_is_rare_not_vscode_shell() -> None:
    text = (ROOT / "reports" / "codex-js-by-originator.md").read_text(encoding="utf-8")
    for n in (
        "| codex_work_desktop | 87 | 83 | 5 | 5/83 |",
        "| Codex Desktop | 1103 | 994 | 17 | 17/994 |",
        "| codex_exec | 315 | 105 | 1 | 1/105 |",
        "| codex_vscode | 16 | 13 | 1 | 1/13 |",
        "Do not map Work inspect to bash",
    ):
        assert n in text, n

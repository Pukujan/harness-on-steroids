from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_wait_rates_contrast_work_and_vscode() -> None:
    text = (ROOT / "reports" / "codex-wait-by-originator.md").read_text(encoding="utf-8")
    for n in (
        "| codex_work_desktop | 87 | 83 | 31 | 31/83 |",
        "| Codex Desktop | 1103 | 994 | 88 | 88/994 |",
        "| codex_exec | 315 | 105 | 16 | 16/105 |",
        "| codex_vscode | 16 | 13 | 0 | 0/13 |",
        "vscode almost never waits",
    ):
        assert n in text, n

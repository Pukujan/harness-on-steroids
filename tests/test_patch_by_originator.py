from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_patch_rates_do_not_average() -> None:
    text = (ROOT / "reports" / "codex-patch-by-originator.md").read_text(encoding="utf-8")
    for n in (
        "| codex_work_desktop | 87 | 83 | 1 | 1/83 |",
        "| Codex Desktop | 1103 | 994 | 1 | 1/994 |",
        "| codex_exec | 315 | 105 | 31 | 31/105 |",
        "| codex_vscode | 16 | 13 | 12 | 12/13 |",
        "Do not imitate vscode or nonempty exec patch rates",
    ):
        assert n in text, n

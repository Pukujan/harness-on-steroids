from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_work_has_zero_update_plan() -> None:
    text = (ROOT / "reports" / "codex-plan-by-originator.md").read_text(encoding="utf-8")
    for n in (
        "| codex_work_desktop | 87 | 83 | 0 | 0 |",
        "| Codex Desktop | 1103 | 994 | 2 | 1 |",
        "| codex_exec | 315 | 105 | 11 | 8 |",
        "| codex_vscode | 16 | 13 | 6 | 0 |",
        "Work **update_plan 0**",
    ):
        assert n in text, n

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_empty_by_originator_locks_v33() -> None:
    text = (ROOT / "reports" / "codex-empty-by-originator.md").read_text(encoding="utf-8")
    for n in (
        "Hashed files: **1521** with no calls: **326**",
        "| codex_exec | 315 | 210 |",
        "| Codex Desktop | 1103 | 109 |",
        "| codex_work_desktop | 87 | 4 |",
        "| codex_vscode | 16 | 3 |",
        "not Work gold",
    ):
        assert n in text, n

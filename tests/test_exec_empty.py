from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_exec_empty_is_not_work_gold() -> None:
    text = (ROOT / "reports" / "codex-exec-empty.md").read_text(encoding="utf-8")
    for n in (
        "codex_exec files: **315** empty of calls: **210**",
        "median=9",
        "max=24",
        "| message | 746 |",
        "not Work gold",
    ):
        assert n in text, n

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_work_empty_sessions_are_short_no_calls() -> None:
    text = (ROOT / "reports" / "codex-work-empty.md").read_text(encoding="utf-8")
    for n in (
        "Work files: **87** empty of calls: **4**",
        "[14, 14, 24, 25]",
        "| message | 21 |",
        "| task_started | 7 |",
        "no tool calls",
    ):
        assert n in text, n

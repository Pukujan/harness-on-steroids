from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_modes_stop_when_nothing_to_look_up() -> None:
    kilo = (ROOT / ".kilo" / "agent" / "codex.md").read_text(encoding="utf-8")
    oc = (ROOT / ".opencode" / "agent" / "codex.md").read_text(encoding="utf-8")
    needle = "If there is nothing to look up, stop"
    assert needle in kilo and needle in oc


def test_work_empty_sessions_are_short_no_calls() -> None:
    text = (ROOT / "reports" / "codex-work-empty.md").read_text(encoding="utf-8")
    for n in (
        "Work files: **87** empty of calls: **4**",
        "[14, 14, 24, 25]",
        "| message | 21 |",
        "| task_started | 7 |",
        "no tool calls",
        "session_meta rows: **95**",
        "with 1 meta: **79**",
        "with 2: **8**",
    ):
        assert n in text, n

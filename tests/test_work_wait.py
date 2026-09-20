from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_work_wait_report_locks_v9() -> None:
    text = (ROOT / "reports" / "codex-work-wait.md").read_text(encoding="utf-8")
    for n in (
        "Sessions: **87** with wait: **31**",
        "median length **3**",
        "apply_patch **0**",
        "wait **218**",
        "send_message **53**",
        "| wait | 218 |",
        "| send_message | 53 |",
    ):
        assert n in text, n


def test_modes_forbid_edit_after_look_burst() -> None:
    kilo = (ROOT / ".kilo" / "agent" / "codex.md").read_text(encoding="utf-8")
    oc = (ROOT / ".opencode" / "agent" / "codex.md").read_text(encoding="utf-8")
    needle = "do not Edit as the next tool"
    assert needle in kilo and needle in oc

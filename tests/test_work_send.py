from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_work_send_report_locks_v12() -> None:
    text = (ROOT / "reports" / "codex-work-send.md").read_text(encoding="utf-8")
    for n in (
        "send_message: **25**",
        "spawn_agent: **2**",
        "both send and spawn: **1**",
        "send and apply_patch: **0**",
        "median sends/session (among senders): **2**",
        "median index of first send: **15**",
        "| <end> | 18 |",
        "| exec-only | 26 |",
    ):
        assert n in text, n


def test_spec_and_modes_prefer_send_not_spawn() -> None:
    spec = (ROOT / "spec" / "codex-imitate-mode.md").read_text(encoding="utf-8")
    kilo = (ROOT / ".kilo" / "agent" / "codex.md").read_text(encoding="utf-8")
    oc = (ROOT / ".opencode" / "agent" / "codex.md").read_text(encoding="utf-8")
    assert "repeated `send_message(target, message)`" in spec
    assert "send+patch 0" in kilo and "send+patch 0" in oc
    assert "Median 2 sends" in kilo and "Median 2 sends" in oc

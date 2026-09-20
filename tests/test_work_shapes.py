from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_work_shapes_report_locks_v7() -> None:
    text = (ROOT / "reports" / "codex-work-shapes.md").read_text(encoding="utf-8")
    for n in (
        "Sessions: **85**",
        "| exec_only | 33 |",
        "| multi_agent | 27 |",
        "| patch | 1 |",
        "send_message sessions: **25**",
        "spawn_agent sessions: **2**",
        "first tool is not send_message: **81** / 81",
        "median tools before first send_message: **15**",
        "`message,target`",
        "`cell_id,max_tokens,yield_time_ms`",
    ):
        assert n in text, n


def test_spec_and_modes_encode_send_after_look() -> None:
    spec = (ROOT / "spec" / "codex-imitate-mode.md").read_text(encoding="utf-8")
    kilo = (ROOT / ".kilo" / "agent" / "codex.md").read_text(encoding="utf-8")
    oc = (ROOT / ".opencode" / "agent" / "codex.md").read_text(encoding="utf-8")
    assert "send_message(target, message)" in spec
    assert "Never Task as tool 1" in kilo
    assert "Never Task as tool 1" in oc
    assert "Never Todowrite as tool 1" in kilo
    assert "Never Todowrite as tool 1" in oc
    assert "exec_only 33" in kilo and "exec_only 33" in oc

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_future_agent_pattern_has_work_relations() -> None:
    text = (ROOT / "spec" / "future-agent-pattern.md").read_text(encoding="utf-8")
    for n in (
        "Do not write first",
        "Burst look",
        "Wait on slow",
        "send_message",
        "After failure",
        "Prose is not truth",
        "score_session.py",
    ):
        assert n in text, n

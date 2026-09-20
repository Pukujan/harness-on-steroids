from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_no_codex_slug_in_agent_rollup() -> None:
    text = (ROOT / "reports" / "work-match-by-agent.md").read_text(encoding="utf-8")
    for n in (
        "| code | 1/13 | 13 |",
        "| plan | 0/7 | 7 |",
        "| build | 3/19 | 19 |",
        "There is no `codex` slug",
        "luna is not Work gold",
    ):
        assert n in text, n
    assert "| codex |" not in text

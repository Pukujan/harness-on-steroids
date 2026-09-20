from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_coding_agents_fail_r2_r4_r5_and_opencode_r3() -> None:
    text = (ROOT / "reports" / "fail-mask-by-agent.md").read_text(encoding="utf-8")
    for n in (
        "## kilo.db agent=code",
        "| R2+R4+R5 | 5 |",
        "| none | 1 |",
        "## opencode.db agent=build",
        "| R2+R3+R4+R5 | 6 |",
        "OpenCode R3 (bash-first)",
    ):
        assert n in text, n

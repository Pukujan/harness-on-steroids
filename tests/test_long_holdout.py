from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_holdout_is_the_six_longest() -> None:
    text = (ROOT / "reports" / "work-long-holdout.md").read_text(encoding="utf-8")
    assert "Develop (n=16" in text
    assert "Hidden holdout (n=6" in text
    for h in (
        "0aecd1eabdf2",
        "1442d08cf2d3",
        "3a749176fae1",
        "45ca341b6f6c",
        "555f9c94ba8e",
        "55fd1ef9b613",
    ):
        assert h in text
    kilo = (ROOT / ".kilo" / "agent" / "codex.md").read_text(encoding="utf-8")
    oc = (ROOT / ".opencode" / "agent" / "codex.md").read_text(encoding="utf-8")
    for h in ("0aecd1eabdf2", "1442d08cf2d3"):
        assert h not in kilo and h not in oc


def test_modes_say_multi_turn_not_oneshot() -> None:
    kilo = (ROOT / ".kilo" / "agent" / "codex.md").read_text(encoding="utf-8")
    oc = (ROOT / ".opencode" / "agent" / "codex.md").read_text(encoding="utf-8")
    assert "Do not overfit one-shot asks" in kilo
    assert "Do not overfit one-shot asks" in oc

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_dashboard_keeps_originators_unmixed() -> None:
    text = (ROOT / "reports" / "codex-originator-dashboard.md").read_text(encoding="utf-8")
    for n in (
        "| Work | 83 | **1/83** | **31/83** | **25** | 2 | **0** | **2** | **5** |",
        "| Desktop | 994 | 1/994 | 88/994 | 17 | 3 | 2 | 4 | 17 |",
        "| `codex_exec` | 105 | **31/105** | 16/105 | 0 | 0 | 11 | **45** | 1 |",
        "| vscode | 13 | **12/13** | **0/13** | **0** | 0 | 6 | **13** | 1 |",
        "Do not imitate vscode",
        "Do not imitate nonempty exec",
    ):
        assert n in text, n
    spec = (ROOT / "spec" / "codex-imitate-mode.md").read_text(encoding="utf-8")
    handoff = (ROOT / "HANDOFF.md").read_text(encoding="utf-8")
    assert "codex-originator-dashboard.md" in spec
    assert "codex-originator-dashboard.md" in handoff
    assert "do not average" in handoff.lower()
    assert "| Work | **1/83** | **31/83** | **25** | **0** | **2** |" in spec

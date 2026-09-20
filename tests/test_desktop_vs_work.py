from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_spec_says_sandwich_is_vscode_plus_exec_not_desktop() -> None:
    spec = (ROOT / "spec" / "codex-imitate-mode.md").read_text(encoding="utf-8")
    assert "31/105" in spec
    assert "1/994" in spec
    assert "do not treat Desktop as the sandwich" in spec


def test_desktop_session_patch_rate_is_not_vscode() -> None:
    text = (ROOT / "reports" / "codex-desktop-vs-work.md").read_text(encoding="utf-8")
    for n in (
        "| codex_work_desktop | 87 | 83 | 1 | 0 |",
        "| Codex Desktop | 1103 | 994 | 1 | 1 |",
        "| apply_patch | 186 |",
        "| exec | 990 |",
        "Do not imitate Desktop as Work",
    ):
        assert n in text, n

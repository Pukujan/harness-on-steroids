from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


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

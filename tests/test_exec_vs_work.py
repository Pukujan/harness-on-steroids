from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_exec_vs_work_does_not_average() -> None:
    text = (ROOT / "reports" / "codex-exec-vs-work.md").read_text(encoding="utf-8")
    for n in (
        "| codex_work_desktop | 87 | 83 | 1 |",
        "| codex_exec | 315 | 105 | 31 |",
        "| apply_patch | 61 |",
        "| update_plan | 8 |",
        "Do not imitate exec-originator as Work",
    ):
        assert n in text, n

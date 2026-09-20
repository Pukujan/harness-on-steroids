from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_matched_task_spec_forbids_swebench_and_bodies() -> None:
    spec = (ROOT / "spec" / "matched-task-eval.md").read_text(encoding="utf-8")
    for n in (
        "not only who called which tool",
        "Never commit message bodies",
        "Do not stand up SWE-bench",
        "Replay not run yet",
    ):
        assert n in spec, n


def test_work_index_is_counts_only() -> None:
    text = (ROOT / "reports" / "work-session-index.md").read_text(encoding="utf-8")
    assert "Work files: **87**" in text
    assert "**No bodies.**" in text
    assert "Replay of these asks" in text
    for line in text.splitlines():
        if line.startswith("| ") and "hash12" not in line and "---" not in line:
            assert len(line) < 120, line

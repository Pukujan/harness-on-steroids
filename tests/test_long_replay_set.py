from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_long_set_is_22_hashes_no_bodies() -> None:
    text = (ROOT / "reports" / "work-long-replay-set.md").read_text(encoding="utf-8")
    assert "Primary n=**22**" in text
    assert "8 singles are smoke only" in text
    assert "| 0aecd1eabdf2 | 33 | 769 | exec |" in text
    assert "| 1442d08cf2d3 | 52 | 2936 | exec |" in text
    assert "Do not SWE-bench" in text
    for line in text.splitlines():
        if line.startswith("| ") and "hash12" not in line and "---" not in line:
            assert len(line) < 80, line


def test_goal_is_long_not_singles() -> None:
    g = (ROOT / "spec" / "matched-task-goal.md").read_text(encoding="utf-8")
    assert "long Work threads" in g
    assert "8 singles are optional smoke" in g
    assert "test_metamorphic.py" in g

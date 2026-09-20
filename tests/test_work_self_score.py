from src.score_session import map_work_seq, score_seq
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_map_work_exec_matches() -> None:
    s = score_seq(map_work_seq(["exec", "exec", "wait", "exec"]))
    assert s["work_match"] is True
    assert s["r3_read_first"] is True


def test_map_work_shell_patch_fails() -> None:
    s = score_seq(map_work_seq(["shell_command", "apply_patch"]))
    assert s["r3_read_first"] is False
    assert s["r2_no_write"] is False
    assert s["work_match"] is False


def test_work_self_score_report_locks_v17() -> None:
    text = (ROOT / "reports" / "work-gold-self-score.md").read_text(encoding="utf-8")
    for n in (
        "work_match: 81 / 83",
        "r1_look_first | 83 / 83",
        "r4_no_todowrite | 83 / 83",
        "| read | 81 |",
        "| bash | 2 |",
    ):
        assert n in text, n

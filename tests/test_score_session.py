from src.score_session import score_seq, summarize
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_r1_write_first_fails() -> None:
    s = score_seq(["write", "read"])
    assert s["r1_look_first"] is False


def test_r1_read_first_passes() -> None:
    s = score_seq(["read", "grep", "edit", "read"])
    assert s["r1_look_first"] is True
    assert s["look_after_write"] is True
    assert s["r2_no_write"] is False


def test_fail_mask_names_missing_relations() -> None:
    assert score_seq(["read", "grep"])["fail_mask"] == "none"
    assert "R2" in score_seq(["read", "edit"])["fail_mask"]
    assert "R3" in score_seq(["bash", "read"])["fail_mask"]
    assert score_seq([])["fail_mask"] == "empty"


def test_work_match_requires_all_relations() -> None:
    assert score_seq(["read", "grep", "glob"])["work_match"] is True
    assert score_seq(["bash", "read"])["work_match"] is False
    assert score_seq(["read", "edit"])["work_match"] is False
    assert score_seq(["read", "todowrite"])["work_match"] is False
    assert score_seq(["todowrite", "read"])["work_match"] is False
    assert score_seq([])["work_match"] is False


def test_r3_bash_first_fails_read_first() -> None:
    assert score_seq(["read", "bash"])["r3_read_first"] is True
    assert score_seq(["bash", "read"])["r3_read_first"] is False
    assert score_seq(["bash", "read"])["r1_look_first"] is True


def test_r2_look_only_matches_work_default() -> None:
    s = score_seq(["read", "grep", "bash"])
    assert s["r1_look_first"] is True
    assert s["r2_no_write"] is True
    assert s["wrote"] is False
    assert s["r6_decompose_not_first"] is True
    assert s["start_look_burst"] == 3


def test_r5_write_after_look_run_fails() -> None:
    assert score_seq(["read", "grep", "edit"])["r5_no_write_after_look_run"] is False
    assert score_seq(["read", "grep", "task"])["r5_no_write_after_look_run"] is True
    assert score_seq(["read", "bash", "read"])["r5_no_write_after_look_run"] is True


def test_r6_todowrite_first_fails() -> None:
    s = score_seq(["todowrite", "read", "edit"])
    assert s["r6_decompose_not_first"] is False
    assert s["r1_look_first"] is True
    assert score_seq(["task", "read"])["r6_decompose_not_first"] is False
    assert score_seq(["read", "grep", "task"])["r6_decompose_not_first"] is True
    assert score_seq(["read", "grep", "task"])["tools_before_decompose"] == 2


def test_metamorphic_prefix_look_preserves_r1() -> None:
    base = ["read", "edit"]
    padded = ["grep", "read", "edit"]
    assert score_seq(base)["r1_look_first"] == score_seq(padded)["r1_look_first"] is True


def test_differential_empty_vs_write() -> None:
    assert score_seq([])["r1"] is None
    assert score_seq(["patch"])["r1_look_first"] is False


def test_multi_piece_task_counts() -> None:
    s = score_seq(["read", "task", "read"])
    assert s["multi_piece"] is True
    assert score_seq(["read", "edit"])["multi_piece"] is False
    assert score_seq(["read", "todowrite"])["multi_piece"] is False


def test_r4_todowrite_fails_work() -> None:
    assert score_seq(["read", "grep"])["r4_no_todowrite"] is True
    assert score_seq(["read", "todowrite", "task"])["r4_no_todowrite"] is False
    assert score_seq(["read", "edit"])["wrote_without_task"] is True
    assert score_seq(["read", "task", "edit"])["wrote_without_task"] is False


def test_skip_study_os_prefix() -> None:
    from src.score_session import summarize
    from unittest.mock import patch

    fake = {
        "a": ["read", "edit"],
        "b": ["study-os-replay_status", "bash"],
    }
    with patch("src.score_session._tools", return_value=fake):
        out = summarize(Path("x.db"))
    assert out["skipped_study_os"] == 1
    assert out["sessions_with_tools"] == 1
    assert out["r1_look_first"] == 1


def test_kilo_copy_look_first_if_present() -> None:
    db = ROOT / "data" / "raw" / "sqlite" / "kilo.db"
    if not db.is_file():
        return
    out = summarize(db)
    assert out["write_first"] == 0

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


def test_metamorphic_prefix_look_preserves_r1() -> None:
    base = ["read", "edit"]
    padded = ["grep", "read", "edit"]
    assert score_seq(base)["r1_look_first"] == score_seq(padded)["r1_look_first"] is True


def test_differential_empty_vs_write() -> None:
    assert score_seq([])["r1"] is None
    assert score_seq(["patch"])["r1_look_first"] is False


def test_kilo_copy_look_first_if_present() -> None:
    db = ROOT / "data" / "raw" / "sqlite" / "kilo.db"
    if not db.is_file():
        return
    out = summarize(db)
    assert out["write_first"] == 0

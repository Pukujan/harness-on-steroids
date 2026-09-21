from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_replay_scores_work_column_only() -> None:
    text = (ROOT / "reports" / "replay-scores.md").read_text(encoding="utf-8")
    assert "## develop (16)" in text
    assert "## holdout (6)" in text
    assert "| pending |" in text
    assert "| 0d6ca4607eaf | yes | none | yes/none/partial | no/R2+R4+R5/partial | yes |" in text
    assert "| 2bde00530ddd | yes | none | yes/none/partial | no/R4/partial | yes |" in text
    assert "| 6eb8631b71ff | yes | none | no/R2+R5/partial | yes/none/partial | pending |" in text
    assert "| 0aecd1eabdf2 | yes | none | no/R2+R5/yes | no/R2+R3+R5/partial | pending |" in text
    assert "| 1442d08cf2d3 | yes | none | yes/none/yes | no/R2+R4+R5/partial | pending |" in text
    assert "not done" in text
    assert text.count("| yes |") >= 20
    assert "| 1b09f49da9b9 | no | R3 |" in text

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_work_wait_clusters_locks_v11() -> None:
    text = (ROOT / "reports" / "codex-work-wait-clusters.md").read_text(encoding="utf-8")
    for n in (
        "Sessions: **85** with wait: **31** with wait-run length ≥2: **18**",
        "wait-runs: **222** median **1**",
        "| exec | 211 |",
        "| 3 | 73 |",
    ):
        assert n in text, n


def test_modes_allow_repeat_wait() -> None:
    kilo = (ROOT / ".kilo" / "agent" / "codex.md").read_text(encoding="utf-8")
    oc = (ROOT / ".opencode" / "agent" / "codex.md").read_text(encoding="utf-8")
    needle = "You may wait more than once"
    assert needle in kilo and needle in oc

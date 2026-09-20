from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_replay_buckets_have_no_prompts() -> None:
    text = (ROOT / "reports" / "work-replay-buckets.md").read_text(encoding="utf-8")
    for n in (
        "| 1 | 8 |",
        "| 2–5 | 52 |",
        "| 6–20 | 16 |",
        "| 21+ | 6 |",
        "Prompts are **not** extracted",
        "Do not SWE-bench",
    ):
        assert n in text, n

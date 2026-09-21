from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOLDOUT = ROOT / "tests" / "holdout" / "holdout_sha256.json"


def _corpus() -> str:
    return "\n".join(
        (ROOT / name).read_text(encoding="utf-8")
        for name in (
            "AGENTS.md",
            "PLAN.md",
            "HANDOFF.md",
            "checkpoints/CURRENT.md",
        )
    )


def _all_hashes(text: str) -> set[str]:
    found: set[str] = set()
    n = len(text)
    for width in range(12, 161):
        for i in range(0, n - width + 1):
            found.add(hashlib.sha256(text[i : i + width].encode("utf-8")).hexdigest())
    return found


def test_holdout_file_exists() -> None:
    assert HOLDOUT.is_file()


def test_every_holdout_hash_is_present() -> None:
    data = json.loads(HOLDOUT.read_text(encoding="utf-8"))
    needles = data["needles_sha256"]
    assert len(needles) >= 10
    found = _all_hashes(_corpus())
    missing = [h for h in needles if h not in found]
    assert missing == [], f"holdout unmatched (owner text removed): {missing}"

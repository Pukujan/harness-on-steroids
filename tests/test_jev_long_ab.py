from __future__ import annotations

from collections import Counter

from research.replay_lib import develop_hashes
from research.run_jev_long_ab import _fixture_turns


def test_long_ab_fixture_plan_has_60_turns_and_covers_every_develop_hash() -> None:
    hashes = develop_hashes()
    turns = _fixture_turns(hashes, 60)
    counts = Counter(turn.task_hash for turn in turns)

    assert len(turns) == 60
    assert set(counts) == set(hashes)
    assert all(count >= 3 for count in counts.values())
    assert all(turn.turn_index >= 1 for turn in turns)
    assert all(turn.ask for turn in turns)

from __future__ import annotations

from collections import Counter
from pathlib import Path

import pytest
from research.replay_lib import develop_hashes
from research.run_jev_long_ab import _fixture_turns, _should_run_advisory_baseline
from src.hos.controller import ControllerAction, DecisionValidation, JevDecision


def test_long_ab_fixture_plan_has_60_turns_and_covers_every_develop_hash() -> None:
    hashes = develop_hashes()
    replay_root = Path(__file__).resolve().parents[1] / "data" / "replay"
    missing = [
        task_hash
        for task_hash in hashes
        if not (replay_root / task_hash / "user.md").is_file()
    ]
    if missing:
        pytest.skip("requires the ignored local data/replay corpus")

    turns = _fixture_turns(hashes, 60)
    counts = Counter(turn.task_hash for turn in turns)

    assert len(turns) == 60
    assert set(counts) == set(hashes)
    assert all(count >= 3 for count in counts.values())
    assert all(turn.turn_index >= 1 for turn in turns)
    assert all(turn.ask for turn in turns)


def test_only_low_confidence_can_use_advisory_baseline() -> None:
    decision = JevDecision(
        task_class="inspect",
        next_action=ControllerAction.INSPECT_REPO,
        next_bead=None,
        confidence=0.2,
        status="ok",
        source="jev",
    )
    low = DecisionValidation(False, decision, "low_confidence")
    invalid = DecisionValidation(False, decision, "illegal_action_for_phase")
    assert _should_run_advisory_baseline(low, enabled=True)
    assert not _should_run_advisory_baseline(low, enabled=False)
    assert not _should_run_advisory_baseline(invalid, enabled=True)

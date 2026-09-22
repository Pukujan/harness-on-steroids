"""Replay prompts must carry the owner ask, never harness context boilerplate.

Work transcripts prepend `<recommended_plugins>` / `<environment_context>` blocks
to the first user turn. For a third of the pool that turn holds *nothing else*, so
feeding `turns[0]` to a harness sends a prompt with no task in it. These tests keep
that from coming back, and assert only on lengths and flags, never on bodies.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from research.replay_lib import (
    REPLAY,
    ROOT,
    ask_turns,
    develop_hashes,
    first_ask,
    holdout_hashes,
    strip_context_blocks,
    user_turns,
)
from src.hos.controller import ControllerPhase, build_initial_state

BOILER = (
    "<recommended_plugins>\nHere is a list of plugins that are available but not "
    "installed.\n- Slack (slack@openai-curated-remote)\n</recommended_plugins>"
    "<environment_context>\n  <cwd>C:\\Users\\someone\\Documents\\Codex\\im</cwd>\n"
    "  <shell>powershell</shell>\n</environment_context>"
)

# data/replay/ is gitignored, so corpus-dependent checks only run locally.
NEEDS_CORPUS = pytest.mark.skipif(not REPLAY.is_dir(), reason="gitignored replay corpus absent")


def test_strip_drops_context_blocks(tmp_path: Path) -> None:
    assert strip_context_blocks(BOILER) == ""


def test_strip_keeps_ask_between_blocks() -> None:
    text = BOILER.replace(
        "</recommended_plugins><environment_context>",
        "</recommended_plugins>\nsynthetic ask goes here\n<environment_context>",
    )
    assert strip_context_blocks(text) == "synthetic ask goes here"


def test_first_ask_skips_a_boilerplate_only_turn(tmp_path: Path) -> None:
    md = tmp_path / "user.md"
    md.write_text(
        f"{BOILER}\n\n---\n\nsynthetic ask goes here\n\n---\n\nsynthetic follow-up",
        encoding="utf-8",
    )

    ask, shifted = first_ask(md)

    assert ask == "synthetic ask goes here"
    assert shifted is True
    # raw shape is preserved for counting; ask shape is what a harness should run.
    assert len(user_turns(md)) == 3
    assert ask_turns(md) == ["synthetic ask goes here", "synthetic follow-up"]


def test_first_ask_reports_no_task_at_all(tmp_path: Path) -> None:
    md = tmp_path / "user.md"
    md.write_text(f"{BOILER}\n\n---\n\n{BOILER}", encoding="utf-8")

    assert first_ask(md) == ("", False)


def test_controller_state_does_not_claim_a_missing_request() -> None:
    honest = build_initial_state("abc123def456").to_payload()
    missing = build_initial_state("abc123def456", ask_present=False, ask_shifted=True).to_payload()

    assert "user_request_received" in honest["observed_facts"]
    assert honest["user_input_required"] is False
    assert "user_request_received" not in missing["observed_facts"]
    assert "user_request_missing" in missing["observed_facts"]
    assert "first_turn_was_harness_context_only" in missing["observed_facts"]
    assert "do_not_infer_the_task_from_boilerplate" in missing["constraints"]
    assert missing["user_input_required"] is True
    assert build_initial_state("abc123def456", ask_present=False).phase is ControllerPhase.INTAKE


@NEEDS_CORPUS
def test_every_pool_task_yields_a_real_ask() -> None:
    pool = develop_hashes() + holdout_hashes()

    assert pool, "pool must not be empty"
    for hash12 in pool:
        source = REPLAY / hash12 / "user.md"
        if not source.is_file():
            continue
        ask, _shifted = first_ask(source)
        assert ask, f"{hash12} produced no ask after stripping context blocks"
        assert "<recommended_plugins>" not in ask
        assert "<environment_context>" not in ask


@NEEDS_CORPUS
def test_replay_scores_flags_contaminated_opencode_cells() -> None:
    text = (ROOT / "reports" / "replay-scores.md").read_text(encoding="utf-8")

    assert "prompt-contaminated" in text
    contaminated = [
        hash12
        for hash12 in develop_hashes() + holdout_hashes()
        if (REPLAY / hash12 / "user.md").is_file()
        and first_ask(REPLAY / hash12 / "user.md")[1]
    ]
    assert contaminated, "expected context-only hashes to flag"
    section = text.split("prompt-contaminated", 1)[1]
    for hash12 in contaminated:
        assert hash12 in section, f"{hash12} contaminated but not flagged"


def test_replay_scores_pinned_rows_are_still_pinned() -> None:
    text = (ROOT / "reports" / "replay-scores.md").read_text(encoding="utf-8")

    # Pinned rows stay pinned: the annotation is additive, gate tests are not rewritten.
    assert "| 0d6ca4607eaf | yes | none | yes/none/partial | no/R2+R4+R5/partial | yes |" in text


@NEEDS_CORPUS
def test_morph_prompts_are_never_task_free() -> None:
    """Morphs may embed the context preamble, but must still contain an ask.

    That is why the develop morph replays are not invalidated by the first-turn bug
    and should not be re-run just to drop the preamble.
    """

    checked = 0
    for hash12 in develop_hashes() + holdout_hashes():
        morph = REPLAY / hash12 / "morphs" / "m1.md"
        if not morph.is_file():
            continue
        checked += 1
        text = morph.read_text(encoding="utf-8", errors="replace")
        assert strip_context_blocks(text), f"{hash12} morph has no ask outside context blocks"
    assert checked, "expected morph files to check"

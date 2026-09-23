from __future__ import annotations

from pathlib import Path

from src.owner_invariants import (
    check_active_harnesses,
    check_control_policy,
    check_forbidden_as_project,
    check_snippets_contains,
    load_spec,
)

ROOT = Path(__file__).resolve().parents[1]


def _real(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def test_dropping_reference_evidence_snippet_is_caught(tmp_path: Path, monkeypatch) -> None:
    spec = load_spec()
    agents = _real("AGENTS.md")
    mutated = agents.replace(
        "ChatGPT Work / Codex transcripts are reference evidence",
        "ChatGPT Work / Codex transcripts are optional background",
    )
    fake_agents = tmp_path / "AGENTS.md"
    fake_agents.write_text(mutated, encoding="utf-8")
    monkeypatch.setattr(
        "src.owner_invariants.read_doc",
        lambda name: (
            fake_agents.read_text(encoding="utf-8") if name == "AGENTS.md" else _real(name)
        ),
    )
    assert check_snippets_contains(spec), "removing reference-evidence clause must fail"


def test_swebench_as_goal_is_caught(monkeypatch) -> None:
    plan = _real("PLAN.md")
    poisoned = plan.replace(
        "## Long-term goal",
        "## Long-term goal\n\nRun SWE-bench Verified as the exam.\n",
    )
    monkeypatch.setattr(
        "src.owner_invariants.read_doc",
        lambda name, _p=poisoned: _p if name == "PLAN.md" else _real(name),
    )
    assert check_forbidden_as_project(), "installing SWE-bench as the goal must fail"


def test_dropping_grok_build_is_caught(monkeypatch) -> None:
    agents = _real("AGENTS.md").replace("Grok Build", "Other Harness")
    plan = _real("PLAN.md").replace("Grok Build", "Other Harness")
    current = _real("checkpoints/CURRENT.md").replace("Grok Build", "Other Harness")
    monkeypatch.setattr(
        "src.owner_invariants.read_doc",
        lambda name, _a=agents, _p=plan, _c=current: (
            _a if name == "AGENTS.md"
            else _p if name == "PLAN.md"
            else _c if name == "checkpoints/CURRENT.md"
            else _real(name)
        ),
    )
    assert check_active_harnesses(), "dropping an active harness must fail"


def test_forcing_general_state_machine_is_caught(monkeypatch) -> None:
    plan = _real("PLAN.md").replace(
        "There is no requirement to build a general runtime state machine.",
        "Build a general runtime state machine first.",
    )
    monkeypatch.setattr(
        "src.owner_invariants.read_doc",
        lambda name, _p=plan: _p if name == "PLAN.md" else _real(name),
    )
    assert check_control_policy(), "making a general state machine mandatory must fail"

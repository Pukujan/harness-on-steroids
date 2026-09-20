from __future__ import annotations

import json
from pathlib import Path

from src.owner_invariants import (
    check_forbidden_as_project,
    check_imitate_both_products,
    check_snippets_contains,
    load_spec,
)

ROOT = Path(__file__).resolve().parents[1]


def test_dropping_gold_snippet_is_caught(tmp_path: Path, monkeypatch) -> None:
    spec = load_spec()
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    mutated = agents.replace("transcripts are the **gold behavior**", "transcripts are optional")
    fake_agents = tmp_path / "AGENTS.md"
    fake_agents.write_text(mutated, encoding="utf-8")
    monkeypatch.setattr(
        "src.owner_invariants.read_doc",
        lambda name: fake_agents.read_text(encoding="utf-8") if name == "AGENTS.md" else (ROOT / name).read_text(encoding="utf-8"),
    )
    failures = check_snippets_contains(spec)
    assert failures, "mutation of gold clause must fail properties"


def test_swebench_as_goal_is_caught(monkeypatch) -> None:
    plan = (ROOT / "PLAN.md").read_text(encoding="utf-8")
    poisoned = plan.replace("## Goal", "## Goal\n\nRun SWE-bench Verified as the exam.\n")
    monkeypatch.setattr(
        "src.owner_invariants.read_doc",
        lambda name, _p=poisoned: _p if name == "PLAN.md" else (ROOT / name).read_text(encoding="utf-8"),
    )
    failures = check_forbidden_as_project()
    assert failures, "installing SWE-bench as the goal must fail"


def test_dropping_opencode_is_caught(monkeypatch) -> None:
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8").replace("OpenCode", "OtherCLI")
    plan = (ROOT / "PLAN.md").read_text(encoding="utf-8").replace("OpenCode", "OtherCLI")
    monkeypatch.setattr(
        "src.owner_invariants.read_doc",
        lambda name, _a=agents, _p=plan: _a if name == "AGENTS.md" else _p if name == "PLAN.md" else (ROOT / name).read_text(encoding="utf-8"),
    )
    failures = check_imitate_both_products()
    assert failures, "dropping OpenCode must fail"

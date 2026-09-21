from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_plan_preserves_richer_work_research_as_active_signal() -> None:
    plan = (ROOT / "PLAN.md").read_text(encoding="utf-8")
    for n in (
        "interaction",
        "Research/inspection",
        "Verification/provenance",
        "Output behavior",
        "Continuity",
        "Variance",
        "account-wide provenance exporter",
        "Tool order is diagnostic",
    ):
        assert n in plan, n


def test_current_baseline_uses_existing_develop_replay_without_tuning() -> None:
    current = (ROOT / "checkpoints" / "CURRENT.md").read_text(encoding="utf-8")
    for n in (
        "existing **development** replay set",
        "Pi",
        "OpenCode",
        "Grok Build",
        "Do not change prompts/control before this baseline.",
    ):
        assert n in current, n


def test_v0_research_gate_spec_remains_as_historical_evidence() -> None:
    spec = (ROOT / "spec" / "work-research-gates.md").read_text(encoding="utf-8")
    for n in (
        "Not complete",
        "Do not treat the chat as the project",
        "not observed",
        "Synthesize late",
        "compacted",
        "Not SWE-bench",
        "JOURNAL is not fact",
    ):
        assert n in spec, n


def test_issues_preserve_old_research_lineage_without_making_it_active_roadmap() -> None:
    issues = (ROOT / "ISSUES.md").read_text(encoding="utf-8")
    assert "v0 historical lineage - issues 1-18" in issues
    assert "GitHub issue #2 - Baseline multi-harness Work behavior replay" in issues
    assert "Do not replace 8-18" in issues

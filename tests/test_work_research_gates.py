from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_plan_has_research_provenance_steps() -> None:
    plan = (ROOT / "PLAN.md").read_text(encoding="utf-8")
    for n in (
        "### G — Work research, planning, provenance",
        "Do not treat the chat as the project",
        "Synthesize late",
        "compacted",
        "### H — Durable evidence",
        "### I — Portable Codex pack",
        "not the exam",
    ):
        assert n in plan, n


def test_issues_queue_14_to_17() -> None:
    issues = (ROOT / "ISSUES.md").read_text(encoding="utf-8")
    for n in (
        "14. Work research / planning / compacted",
        "15. Provenance and research gates in Codex mode",
        "16. Durable checkpoints",
        "17. Portable Codex pack",
        "18. Repo modules, lint, types",
        "Do not replace 8–18",
    ):
        assert n in issues, n


def test_work_research_gates_spec() -> None:
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

"""Owner invariant checkers for owner spec v2."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "spec" / "owner.v2.json"


def load_spec() -> dict:
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))


def read_doc(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def check_snippets_contains(spec: dict | None = None) -> list[str]:
    spec = spec or load_spec()
    failures: list[str] = []
    required = spec.get("required_snippets") or {}
    for doc, needles in required.items():
        text = read_doc(doc)
        for needle in needles:
            if needle not in text:
                failures.append(f"{doc} missing {needle!r}")
    return failures


def check_snippets_regex(spec: dict | None = None) -> list[str]:
    """Second checker: same needles as regex-escaped search."""
    spec = spec or load_spec()
    failures: list[str] = []
    required = spec.get("required_snippets") or {}
    for doc, needles in required.items():
        text = read_doc(doc)
        for needle in needles:
            if re.search(re.escape(needle), text) is None:
                failures.append(f"{doc} regex-miss {needle!r}")
    return failures


def check_read_order() -> list[str]:
    agents = read_doc("AGENTS.md")
    failures: list[str] = []
    for name in ("AGENTS.md", "PLAN.md", "checkpoints/CURRENT.md", "HANDOFF.md", "ISSUES.md"):
        if name not in agents:
            failures.append(f"AGENTS.md does not name {name!r} in continuity order")
    if "checkpoints/CURRENT.md" not in read_doc("HANDOFF.md"):
        failures.append("HANDOFF.md does not point at checkpoints/CURRENT.md")
    return failures


def check_forbidden_as_project() -> list[str]:
    """Public benchmarks may be comparison context, never the project definition."""
    failures: list[str] = []
    agents = read_doc("AGENTS.md")
    plan = read_doc("PLAN.md")
    if "Do not invent a new public exam" not in agents:
        failures.append("AGENTS.md dropped no-public-exam")
    if "public benchmark replacement" not in plan:
        failures.append("PLAN.md dropped public-benchmark boundary")
    goal = plan.split("## Reference evidence")[0] if "## Reference evidence" in plan else plan
    if re.search(r"(?i)run SWE-bench|SWE-bench Verified as the exam|use Harbor as the exam", goal):
        failures.append("PLAN.md installs a public benchmark as the project")
    return failures


def check_active_harnesses() -> list[str]:
    failures: list[str] = []
    blob = (
        read_doc("AGENTS.md")
        + "\n"
        + read_doc("PLAN.md")
        + "\n"
        + read_doc("checkpoints/CURRENT.md")
    )
    for word in ("Pi", "OpenCode", "Grok Build"):
        if word not in blob:
            failures.append(f"active docs dropped harness {word}")
    if "Kilo Codex v0" not in blob:
        failures.append("active docs dropped Kilo Codex v0 baseline")
    return failures


def check_control_policy() -> list[str]:
    failures: list[str] = []
    agents = read_doc("AGENTS.md")
    plan = read_doc("PLAN.md")
    spec = load_spec()
    if "Prompt/context control is the first intervention." not in agents:
        failures.append("AGENTS.md dropped prompt/context-first control")
    if "There is no requirement to build a general runtime state machine." not in plan:
        failures.append("PLAN.md made runtime state machine ambiguous")
    if spec["control"]["general_runtime_state_machine_required"] is not False:
        failures.append("owner spec requires a general runtime state machine")
    return failures


def all_failures() -> list[str]:
    return (
        check_snippets_contains()
        + check_read_order()
        + check_forbidden_as_project()
        + check_active_harnesses()
        + check_control_policy()
    )


def docs_ok() -> bool:
    return not all_failures()

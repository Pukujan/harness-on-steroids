"""Owner invariant checkers (spec-driven). Two implementations for differential tests."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "spec" / "owner.v1.json"


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
    """Second checker: same needles as regex-escaped search (differential pair)."""
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
    for name in ("AGENTS.md", "PLAN.md", "HANDOFF.md"):
        if name not in agents:
            failures.append(f"AGENTS.md does not name {name} in read order")
    if "PLAN.md" not in read_doc("HANDOFF.md"):
        failures.append("HANDOFF.md does not point at PLAN.md")
    return failures


def check_forbidden_as_project() -> list[str]:
    """SWE-bench etc. may appear only as forbidden, not as the goal."""
    failures: list[str] = []
    plan = read_doc("PLAN.md")
    goal = plan.split("## Gold standard")[0] if "## Gold standard" in plan else plan
    if re.search(r"(?i)run SWE-bench|SWE-bench Verified as the", goal):
        failures.append("PLAN.md goal section installs SWE-bench as the project")
    if "No public coding exam" not in plan:
        failures.append("PLAN.md dropped no-public-exam")
    agents = read_doc("AGENTS.md")
    if "Do not invent a new exam" not in agents:
        failures.append("AGENTS.md dropped no-new-exam")
    return failures


def check_imitate_both_products() -> list[str]:
    failures: list[str] = []
    blob = read_doc("AGENTS.md") + "\n" + read_doc("PLAN.md")
    for word in ("Kilo", "OpenCode"):
        if word not in blob:
            failures.append(f"docs dropped product {word}")
    if "free" not in read_doc("AGENTS.md") or "build mode" not in read_doc("AGENTS.md"):
        failures.append("AGENTS.md dropped free OpenCode build mode")
    return failures


def all_failures() -> list[str]:
    return (
        check_snippets_contains()
        + check_read_order()
        + check_forbidden_as_project()
        + check_imitate_both_products()
    )


def docs_ok() -> bool:
    return not all_failures()

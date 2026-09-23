from __future__ import annotations

import re
from pathlib import Path

from src.owner_invariants import all_failures, check_snippets_contains, load_spec, read_doc

ROOT = Path(__file__).resolve().parents[1]


def test_extra_blank_lines_still_pass(monkeypatch) -> None:
    """Metamorphic: padding whitespace must not break owner properties."""
    spec = load_spec()

    def padded(name: str) -> str:
        return re.sub(r"\n", "\n\n", read_doc(name))

    monkeypatch.setattr("src.owner_invariants.read_doc", padded)
    assert check_snippets_contains(spec) == []


def test_current_docs_pass_untransformed() -> None:
    assert all_failures() == []


def test_kilo_and_opencode_modes_stay_paired() -> None:
    """Once one imitate-mode exists, the other must exist (metamorphic pair)."""
    kilo = (
        list((ROOT / ".kilo" / "agent").glob("*.md"))
        if (ROOT / ".kilo" / "agent").is_dir()
        else []
    )
    oc = list((ROOT / ".opencode").glob("**/*")) if (ROOT / ".opencode").is_dir() else []
    kilo_mode = [p for p in kilo if "codex" in p.name.lower() or "imitate" in p.name.lower()]
    if kilo_mode and not oc:
        raise AssertionError("Kilo imitate mode exists without OpenCode counterpart")

from __future__ import annotations

import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEEDLES = ["Look first", "Burst look", "Look again", "Prose is not truth", "Do not patch first"]
RNG = random.Random(42)


def test_kilo_json_loads_owner_docs() -> None:
    cfg = json.loads((ROOT / "kilo.json").read_text(encoding="utf-8"))
    inst = cfg.get("instructions") or []
    assert "AGENTS.md" in inst and "PLAN.md" in inst


def test_prompt_stack_doc_names_layers() -> None:
    text = (ROOT / "spec" / "prompt-stack.md").read_text(encoding="utf-8")
    for n in ("AGENTS.md", "codex.md", "goal_loop.py", "owner.v1.json"):
        assert n in text, n


def test_fuzz_mode_delete_look_first_is_detectable() -> None:
    original = (ROOT / ".kilo" / "agent" / "codex.md").read_text(encoding="utf-8")
    assert "Look first" in original
    broken = original.replace("Look first", "Skip look")
    assert "Look first" not in broken
    # live files must still be intact
    assert "Look first" in original


def test_fuzz_random_erasure_of_needles_from_copy() -> None:
    original = (ROOT / ".opencode" / "agent" / "codex.md").read_text(encoding="utf-8")
    for needle in NEEDLES:
        copy = original.replace(needle, "")
        assert needle not in copy
        assert needle in original


def test_metamorphic_mode_files_share_needles() -> None:
    kilo = (ROOT / ".kilo" / "agent" / "codex.md").read_text(encoding="utf-8")
    oc = (ROOT / ".opencode" / "agent" / "codex.md").read_text(encoding="utf-8")
    for n in NEEDLES:
        assert (n in kilo) == (n in oc)

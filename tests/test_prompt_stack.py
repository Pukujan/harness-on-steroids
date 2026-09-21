from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V0_NEEDLES = [
    "Look first",
    "Burst look",
    "Look again",
    "Prose is not truth",
    "Do not patch first",
    "Chat first",
    "Seek go-ahead before a long-running task",
]


def test_kilo_json_loads_owner_docs() -> None:
    cfg = json.loads((ROOT / "kilo.json").read_text(encoding="utf-8"))
    inst = cfg.get("instructions") or []
    assert "AGENTS.md" in inst and "PLAN.md" in inst


def test_prompt_stack_doc_names_new_layers() -> None:
    text = (ROOT / "spec" / "prompt-stack.md").read_text(encoding="utf-8")
    for n in ("AGENTS.md", "checkpoints/CURRENT.md", "owner.v2.json", "Pi + OpenCode + Grok Build"):
        assert n in text, n
    assert "A full state machine is not a required layer." in text
    assert "CONTINUE.md is dormant" in text


def test_continue_is_post_goal_only() -> None:
    cont = (ROOT / "CONTINUE.md").read_text(encoding="utf-8")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "dormant unless explicitly activated" in cont
    assert "Seek go-ahead before starting a long-running task" in agents
    assert "A status question is not a standing goal" in agents


def test_v0_kilo_mode_remains_intact_as_baseline() -> None:
    original = (ROOT / ".kilo" / "agent" / "codex.md").read_text(encoding="utf-8")
    for needle in V0_NEEDLES:
        assert needle in original


def test_v0_opencode_mode_remains_intact_as_baseline() -> None:
    original = (ROOT / ".opencode" / "agent" / "codex.md").read_text(encoding="utf-8")
    for needle in V0_NEEDLES:
        assert needle in original


def test_v0_mode_files_still_share_behavior_needles() -> None:
    kilo = (ROOT / ".kilo" / "agent" / "codex.md").read_text(encoding="utf-8")
    oc = (ROOT / ".opencode" / "agent" / "codex.md").read_text(encoding="utf-8")
    for n in V0_NEEDLES:
        assert (n in kilo) == (n in oc)

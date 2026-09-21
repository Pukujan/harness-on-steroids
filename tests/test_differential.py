from src.owner_invariants import check_snippets_contains, check_snippets_regex, load_spec, read_doc


def test_two_checkers_agree_on_current_docs() -> None:
    spec = load_spec()
    a = check_snippets_contains(spec)
    b = check_snippets_regex(spec)
    assert a == [] and b == []


def test_two_checkers_agree_on_failure(monkeypatch) -> None:
    spec = load_spec()
    monkeypatch.setattr("src.owner_invariants.read_doc", lambda name: "not the owner docs")
    a = check_snippets_contains(spec)
    b = check_snippets_regex(spec)
    assert a and b
    assert len(a) == len(b)


def test_owner_docs_share_new_direction() -> None:
    blob = "\n".join(
        read_doc(name)
        for name in ("AGENTS.md", "PLAN.md", "checkpoints/CURRENT.md")
    )
    for needle in ("Pi", "OpenCode", "Grok Build", "Kilo Codex v0"):
        assert needle in blob
    assert "model- and harness-agnostic" in blob
    assert "Do not invent a new public exam" in read_doc("AGENTS.md")

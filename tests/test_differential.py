from src.owner_invariants import check_snippets_contains, check_snippets_regex, load_spec, read_doc


def test_two_checkers_agree_on_current_docs() -> None:
    spec = load_spec()
    a = check_snippets_contains(spec)
    b = check_snippets_regex(spec)
    assert a == [] and b == []


def test_two_checkers_agree_on_failure(monkeypatch) -> None:
    spec = load_spec()
    monkeypatch.setattr(
        "src.owner_invariants.read_doc",
        lambda name: "not the owner docs",
    )
    a = check_snippets_contains(spec)
    b = check_snippets_regex(spec)
    assert a and b
    assert len(a) == len(b)


def test_agents_and_plan_do_not_contradict_gold() -> None:
    agents = read_doc("AGENTS.md")
    plan = read_doc("PLAN.md")
    assert "gold" in agents.lower() and "gold" in plan.lower()
    assert "Kilo" in agents and "Kilo" in plan
    assert "OpenCode" in agents and "OpenCode" in plan
    assert "Do not invent a new exam" in agents
    assert "No public coding exam" in plan

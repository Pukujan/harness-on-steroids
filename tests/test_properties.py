from src.owner_invariants import all_failures, load_spec


def test_spec_loads_and_forbids_exam_substitute() -> None:
    spec = load_spec()
    assert spec["no_exception"] is True
    assert spec["gold"]["invent_new_exam"] is False
    assert spec["gold"]["retest_codex_on_public_benchmarks"] is False
    assert "kilo" in spec["products"] and "opencode" in spec["products"]


def test_owner_docs_satisfy_all_properties() -> None:
    failures = all_failures()
    assert failures == [], failures

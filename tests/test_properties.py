from src.owner_invariants import all_failures, load_spec


def test_spec_loads_new_owner_contract() -> None:
    spec = load_spec()
    assert spec["schema"].endswith("/2.0.0")
    assert spec["no_exception"] is True
    assert spec["goal"]["public_benchmark_substitute"] is False
    assert spec["models"]["model_agnostic"] is True
    assert spec["harnesses"]["active_development"] == ["pi", "opencode", "grok-build"]
    assert spec["control"]["general_runtime_state_machine_required"] is False
    assert spec["iteration"]["one_main_behavior_hypothesis_per_slice"] is True


def test_owner_docs_satisfy_all_properties() -> None:
    failures = all_failures()
    assert failures == [], failures

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WF = ROOT / ".github" / "workflows" / "owner-gate.yml"


def test_workflow_exists_and_is_not_a_noop() -> None:
    assert WF.is_file()
    text = WF.read_text(encoding="utf-8")
    assert "continue-on-error" not in text
    assert "pytest" in text
    for name in (
        "test_properties.py",
        "test_hidden_holdout.py",
        "test_mutations.py",
        "test_metamorphic.py",
        "test_differential.py",
        "test_ci_contract.py",
        "test_iteration_loop.py",
        "test_imitate_modes.py",
        "test_goal_loop.py",
        "test_goal_fuzz.py",
        "test_prompt_stack.py",
        "test_score_session.py",
        "test_future_agent_pattern.py",
        "test_work_vs_vscode.py",
        "test_work_shapes.py",
        "test_work_wait.py",
        "test_work_js_shell.py",
        "test_work_wait_clusters.py",
        "test_work_send.py",
        "test_work_plan.py",
        "test_work_self_score.py",
        "test_work_empty.py",
    ):
        assert name in text, name

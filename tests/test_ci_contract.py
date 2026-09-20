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
        "test_goal_uses_codex_agent.py",
        "test_empty_by_originator.py",
        "test_exec_empty.py",
        "test_exec_vs_work.py",
        "test_desktop_vs_work.py",
        "test_vscode_vs_work.py",
        "test_patch_by_originator.py",
        "test_wait_by_originator.py",
        "test_send_by_originator.py",
        "test_plan_by_originator.py",
        "test_originator_dashboard.py",
        "test_shell_by_originator.py",
        "test_js_by_originator.py",
        "test_work_match_by_agent.py",
        "test_fail_mask_by_agent.py",
        "test_matched_task_eval.py",
        "test_work_replay_buckets.py",
    ):
        assert name in text, name

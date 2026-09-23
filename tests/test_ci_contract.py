from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WF = ROOT / ".github" / "workflows" / "owner-gate.yml"


def test_workflow_runs_required_quality_and_checkpoint_gates() -> None:
    assert WF.is_file()
    text = WF.read_text(encoding="utf-8")
    assert "continue-on-error" not in text
    assert "pull_request:" in text
    assert "ruff check src tests" in text
    assert "mypy src" in text
    assert "run: pytest -q" in text
    assert 'github.event_name == \'pull_request\'' in text
    assert "checkpoints/CURRENT.md" in text
    for job in ("lint", "typecheck", "tests", "windows-tests", "checkpoint-record"):
        assert f"name: {job}" in text
    assert (ROOT / ".github" / "pull_request_template.md").is_file()

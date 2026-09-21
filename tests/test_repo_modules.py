from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_repo_modules_map_exists() -> None:
    text = (ROOT / "spec" / "repo-modules.md").read_text(encoding="utf-8")
    for n in (
        "Layers (MVC-shaped)",
        "Contract",
        "Measure",
        "Adapt",
        "Lib",
        "Gate",
        "src/hos/",
        "Lint and types",
        "New analysis scripts in the repo root",
    ):
        assert n in text, n


def test_work_ux_gaps_doc_exists() -> None:
    text = (ROOT / "research" / "work-ux-gaps.md").read_text(encoding="utf-8")
    for n in (
        "Measurement not run",
        "send_message",
        "compacted",
        "Do not treat the chat as the project",
        "PCM vs imitate pack",
        "Isolated `oc-sandbox`",
    ):
        assert n in text, n


def test_combined_slices_goal_is_not_started() -> None:
    text = (ROOT / "spec" / "combined-slices-goal.md").read_text(encoding="utf-8")
    assert "Not started" in text
    assert "Do not SWE-bench" in text
    assert "issue 18" in text


def test_pyproject_declares_ruff_and_mypy() -> None:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "[tool.ruff]" in text
    assert "[tool.mypy]" in text
    assert "ruff" in text
    assert "mypy" in text


def test_hos_facade_imports() -> None:
    from src.hos import GoalEngine, load_spec, score_seq

    assert callable(score_seq)
    assert callable(load_spec)
    assert GoalEngine is not None


def test_issues_include_foundation() -> None:
    issues = (ROOT / "ISSUES.md").read_text(encoding="utf-8")
    assert "18. Repo modules, lint, types" in issues
    assert "Do not replace 8–18" in issues

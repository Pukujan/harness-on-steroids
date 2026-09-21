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
        "State",
        "owner.v2.json",
        "checkpoints/CURRENT.md",
        "No substantial architecture-only slice",
        "New analysis scripts in the repo root",
    ):
        assert n in text, n


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


def test_issues_preserve_v0_history_and_map_active_work() -> None:
    issues = (ROOT / "ISSUES.md").read_text(encoding="utf-8")
    for needle in (
        "v0 historical lineage - issues 1-18",
        "18. Repo modules, lint, types",
        "20. Governance switch / owner spec v2",
        "GitHub issue #2 - Baseline multi-harness Work behavior replay",
        "Do not replace 8-18",
    ):
        assert needle in issues, needle

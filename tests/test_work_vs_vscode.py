"""Differential: Work gold vs vscode sandwich must not be averaged away."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_work_almost_never_patches() -> None:
    work = (ROOT / "reports" / "codex-work-desktop-only.md").read_text(encoding="utf-8")
    assert "with apply_patch: **1**" in work
    assert "| apply_patch | 2 |" in work


def test_vscode_is_the_patch_sandwich() -> None:
    by = (ROOT / "reports" / "codex-by-originator.md").read_text(encoding="utf-8")
    assert "| apply_patch | 718 |" in by
    assert "| shell_command | 5562 |" in by
    assert "codex_vscode" in by


def test_spec_prefers_work_over_vscode() -> None:
    spec = (ROOT / "spec" / "codex-imitate-mode.md").read_text(encoding="utf-8")
    assert "codex_work_desktop" in spec
    work_i = spec.find("codex_work_desktop")
    vs_i = spec.lower().find("vs code")
    assert work_i != -1 and vs_i != -1

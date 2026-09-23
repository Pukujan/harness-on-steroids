from __future__ import annotations

import os
from pathlib import Path

from research.run_jev_long_ab import _clone_workspace
from src.hos.controller.adapters import OpenCodeAdapter


def test_task_workspace_clone_excludes_reproducible_runtime_state(tmp_path: Path) -> None:
    seed = tmp_path / "seed"
    destination = tmp_path / "run" / "workspace"
    (seed / ".opencode" / "agent").mkdir(parents=True)
    (seed / ".opencode" / "agent" / "codex.md").write_text("control", encoding="utf-8")
    (seed / ".opencode" / "node_modules" / "pkg").mkdir(parents=True)
    (seed / "node_modules" / "pkg").mkdir(parents=True)
    (seed / ".venv" / "Scripts").mkdir(parents=True)
    (seed / "src").mkdir()
    (seed / "src" / "main.py").write_text("print('ok')", encoding="utf-8")

    _clone_workspace(destination, seed)

    assert (destination / "src" / "main.py").read_text(encoding="utf-8") == "print('ok')"
    assert not (destination / ".opencode").exists()
    assert not (destination / "node_modules").exists()
    assert not (destination / ".venv").exists()


def test_opencode_stages_only_shared_control_files(tmp_path: Path) -> None:
    source = tmp_path / "source-config"
    (source / "agent").mkdir(parents=True)
    (source / "command").mkdir()
    (source / "node_modules" / "package").mkdir(parents=True)
    (source / "agent" / "codex.md").write_text("agent", encoding="utf-8")
    (source / "command" / "goal.md").write_text("command", encoding="utf-8")
    runtime_root = tmp_path / "shared-runtime"
    adapter = OpenCodeAdapter(
        executable="opencode-test",
        runtime_root=runtime_root,
        config_source=source,
    )

    adapter.prepare_runtime()

    assert (adapter.config_dir / "agent" / "codex.md").read_text(encoding="utf-8") == "agent"
    assert (adapter.config_dir / "command" / "goal.md").read_text(encoding="utf-8") == "command"
    assert not (adapter.config_dir / "node_modules").exists()


def test_opencode_process_paths_are_shared_and_inherited_secrets_are_untouched(
    tmp_path: Path, monkeypatch
) -> None:
    xdg_config = tmp_path / "user-config"
    user_config_dir = xdg_config / "opencode"
    user_config_dir.mkdir(parents=True)
    user_config = user_config_dir / "opencode.jsonc"
    user_config.write_text("{}", encoding="utf-8")
    monkeypatch.setenv("XDG_CONFIG_HOME", str(xdg_config))
    monkeypatch.setenv("QWEN_API_KEY", "test-secret-not-printed")
    runtime_root = tmp_path / "shared-runtime"
    adapter = OpenCodeAdapter(executable="opencode-test", runtime_root=runtime_root)

    overrides = adapter.process_environment(tmp_path / "workspace")

    assert Path(overrides["OPENCODE_CONFIG_DIR"]) == runtime_root / "config"
    for key in (
        "XDG_CONFIG_HOME",
        "XDG_DATA_HOME",
        "XDG_CACHE_HOME",
        "XDG_STATE_HOME",
        "OPENCODE_TEST_HOME",
        "TEMP",
        "TMP",
        "TMPDIR",
    ):
        assert Path(overrides[key]).is_relative_to(runtime_root)
    assert overrides["OPENCODE_DISABLE_PROJECT_CONFIG"] == "1"
    assert overrides["OPENCODE_CONFIG"] == str(user_config)
    assert "QWEN_API_KEY" not in overrides
    assert os.environ["QWEN_API_KEY"] == "test-secret-not-printed"


def test_windows_opencode_default_is_repo_owned_not_nvm() -> None:
    if os.name != "nt":
        return

    adapter = OpenCodeAdapter()
    assert Path(adapter.executable) == (
        Path(__file__).resolve().parents[1] / ".tools" / "opencode" / "opencode.exe"
    )

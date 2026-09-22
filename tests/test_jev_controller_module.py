from __future__ import annotations

import json
from pathlib import Path

from src.hos.controller import (
    ControllerAction,
    ControllerPhase,
    JevController,
    OpenCodeAdapter,
    PiAdapter,
    build_initial_state,
    controller_directive,
)
from src.hos.controller.adapters import extract_tool_seq


def test_initial_state_is_compact_and_does_not_include_prompt() -> None:
    state = build_initial_state("abc123def456")

    payload = state.to_payload()

    assert state.phase is ControllerPhase.INTAKE
    assert payload["intent_class"] == "existing_codex_work_replay"
    assert "abc123def456" not in json.dumps(payload)
    assert payload["constraints"]


def test_jev_nested_response_and_probabilities_are_normalized() -> None:
    decision = JevController._parse_decision(
        {
            "answers": {
                "next_action": {
                    "choice": "INSPECT_REPO",
                    "probabilities": {"INSPECT_REPO": 0.6, "READ_DOCS": 0.4},
                }
            }
        },
        ControllerPhase.INTAKE,
    )

    assert decision.status == "ok"
    assert decision.action is ControllerAction.INSPECT_REPO
    assert decision.confidence == 0.6


def test_unavailable_controller_produces_safe_directive(monkeypatch) -> None:
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    decision = JevController(api_key="").decide(build_initial_state("abc123def456"))

    assert decision.status == "unavailable"
    assert "inspect before acting" in controller_directive(decision)


def test_adapter_command_builders_keep_harnesses_distinct(tmp_path: Path) -> None:
    prompt = tmp_path / "prompt.txt"
    prompt.write_text("inspect the repository", encoding="utf-8")
    workdir = tmp_path / "work"
    workdir.mkdir()

    opencode = OpenCodeAdapter(executable="opencode-test")
    pi = PiAdapter(executable="pi-test")

    assert opencode.command(prompt_file=prompt, workdir=workdir, title="t")[1] == "run"
    pi_command = pi.command(prompt_file=prompt, workdir=workdir, title="t")
    assert "--mode" in pi_command
    assert "--print" in pi_command
    assert "grok" not in opencode.name
    assert pi.name == "pi"


def test_pi_model_is_explicit_and_configurable(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("PI_MODEL", "yolo-auto/qwen3.8-flash")
    adapter = PiAdapter(executable="pi-test")
    prompt = tmp_path / "prompt.txt"
    prompt.write_text("inspect", encoding="utf-8")

    command = adapter.command(prompt_file=prompt, workdir=tmp_path, title="t")

    assert command[1:3] == ["--model", "yolo-auto/qwen3.8-flash"]


def test_pi_yolo_model_writes_project_local_provider_config(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("PI_MODEL", "yolo-auto/qwen3.8-flash")
    monkeypatch.setenv("QWEN_API_URL", "https://yolo-auto.com/v1")
    adapter = PiAdapter(executable="pi-test")

    adapter.prepare_workdir(tmp_path)

    config = json.loads(
        (tmp_path / ".pi" / "agent" / "models.json").read_text(encoding="utf-8")
    )
    provider = config["providers"]["yolo-auto"]
    assert provider["baseUrl"] == "https://yolo-auto.com/v1"
    assert provider["apiKey"] == "$QWEN_API_KEY"
    assert provider["apiKey"] == "$QWEN_API_KEY"


def test_opencode_local_model_writes_isolated_provider_config(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("LOCAL_MODEL_BASE_URL", "http://100.79.248.88:8080/v1")
    adapter = OpenCodeAdapter(executable="opencode-test", model="local-bonsai/bonsai")

    adapter.prepare_workdir(tmp_path)

    config = json.loads((tmp_path / "opencode.json").read_text(encoding="utf-8"))
    assert config["provider"]["local-bonsai"]["options"]["baseURL"].endswith("/v1")
    assert "apiKey" not in json.dumps(config) or "none" in json.dumps(config)


def test_event_parser_accepts_nested_tool_calls(tmp_path: Path) -> None:
    events = tmp_path / "events.ndjson"
    events.write_text(
        "\n".join(
            [
                json.dumps({"part": {"tool": "read"}}),
                json.dumps({"tool_call": {"function": {"name": "bash"}}}),
            ]
        ),
        encoding="utf-8",
    )

    assert extract_tool_seq(events) == ["read", "bash"]

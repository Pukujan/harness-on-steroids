from __future__ import annotations

import json
import sys
from pathlib import Path

from src.hos.controller import (
    ControllerAction,
    ControllerPhase,
    GrokBuildAdapter,
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


def test_prompt_is_not_passed_in_argv(tmp_path: Path) -> None:
    """Regression: a prompt-sized argv blew the Windows command-line limit.

    Every replay turn recorded ``fail_1`` ("The command line is too long") and
    the harness never launched, so 0-tool / no-outcome cells measured nothing.
    Pi/OpenCode must feed the prompt over stdin; Grok uses --prompt-file. No
    adapter may place the prompt body in argv.
    """
    prompt_file = tmp_path / "prompt.txt"
    prompt = "x" * 40000  # larger than the ~32K Windows command-line limit
    prompt_file.write_text(prompt, encoding="utf-8")
    workdir = tmp_path / "work"
    workdir.mkdir()

    opencode = OpenCodeAdapter(executable="opencode-test")
    pi = PiAdapter(executable="pi-test")
    grok = GrokBuildAdapter(executable="grok-test")

    assert opencode.prompt_via_stdin is True
    assert pi.prompt_via_stdin is True
    assert grok.prompt_via_stdin is False

    for adapter in (opencode, pi, grok):
        command = adapter.command(prompt_file=prompt_file, workdir=workdir, title="t")
        joined = " ".join(command)
        assert prompt not in joined
        assert prompt[:64] not in joined

    # Grok still references the prompt by file path, not by value.
    grok_command = grok.command(prompt_file=prompt_file, workdir=workdir, title="t")
    assert str(prompt_file) in grok_command


def test_stdin_prompt_delivers_over_pipe_not_argv(tmp_path: Path) -> None:
    """Prove the run() plumbing feeds a large prompt over stdin to the harness."""
    echo = tmp_path / "echo_stdin.py"
    echo.write_text(
        "import sys\n"
        "data = sys.stdin.read()\n"
        "print(len(data), len(sys.argv[1:]))\n",
        encoding="utf-8",
    )

    class _StdinHarness(PiAdapter):
        def command(self, *, prompt_file: Path, workdir: Path, title: str) -> list[str]:
            return [sys.executable, str(echo)]

    prompt_file = tmp_path / "prompt.txt"
    events = tmp_path / "events.ndjson"
    errors = tmp_path / "stderr.txt"
    workdir = tmp_path / "work"
    workdir.mkdir()
    big_prompt = "y" * 40000  # larger than the Windows command-line limit

    run = _StdinHarness(executable=sys.executable).run(
        prompt=big_prompt,
        prompt_file=prompt_file,
        workdir=workdir,
        events_path=events,
        stderr_path=errors,
        timeout=30,
        title="t",
    )

    assert run.status == "ok"
    delivered, argv_args = events.read_text(encoding="utf-8").split()
    assert delivered == str(len(big_prompt))
    assert argv_args == "0"


def test_streaming_progress_resets_inactivity_timeout(tmp_path: Path) -> None:
    """A live stream must not be killed by a short inactivity window."""
    stream = tmp_path / "stream.py"
    stream.write_text(
        "import sys, time\n"
        "for index in range(8):\n"
        "    print(index, flush=True)\n"
        "    time.sleep(0.08)\n",
        encoding="utf-8",
    )

    class _StreamingHarness(PiAdapter):
        def command(self, *, prompt_file: Path, workdir: Path, title: str) -> list[str]:
            return [sys.executable, str(stream)]

    adapter = _StreamingHarness(executable=sys.executable)
    workdir = tmp_path / "work"
    workdir.mkdir()
    run = adapter.run(
        prompt="stream",
        prompt_file=tmp_path / "prompt.txt",
        workdir=workdir,
        events_path=tmp_path / "events.ndjson",
        stderr_path=tmp_path / "stderr.txt",
        timeout=0.12,
        max_runtime=2.0,
        title="streaming",
    )

    assert run.status == "ok"
    assert run.timeout_reason is None


def test_silent_harness_hits_inactivity_timeout(tmp_path: Path) -> None:
    silent = tmp_path / "silent.py"
    silent.write_text("import time\ntime.sleep(0.5)\n", encoding="utf-8")

    class _SilentHarness(PiAdapter):
        def command(self, *, prompt_file: Path, workdir: Path, title: str) -> list[str]:
            return [sys.executable, str(silent)]

    adapter = _SilentHarness(executable=sys.executable)
    workdir = tmp_path / "work"
    workdir.mkdir()
    run = adapter.run(
        prompt="silent",
        prompt_file=tmp_path / "prompt.txt",
        workdir=workdir,
        events_path=tmp_path / "events.ndjson",
        stderr_path=tmp_path / "stderr.txt",
        timeout=0.1,
        max_runtime=1.0,
        title="silent",
    )

    assert run.status == "timeout"
    assert run.timeout_reason == "inactivity"


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
    settings = json.loads((tmp_path / ".pi" / "agent" / "settings.json").read_text())
    assert settings["httpIdleTimeoutMs"] == 1200000
    assert settings["retry"]["provider"]["timeoutMs"] == 1200000
    assert provider["apiKey"] == "$QWEN_API_KEY"


def test_opencode_local_model_writes_isolated_provider_config(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("LOCAL_MODEL_BASE_URL", "http://100.79.248.88:8080/v1")
    adapter = OpenCodeAdapter(executable="opencode-test", model="local-bonsai/bonsai")

    adapter.prepare_workdir(tmp_path)

    config = json.loads((tmp_path / "opencode.json").read_text(encoding="utf-8"))
    assert config["provider"]["local-bonsai"]["options"]["baseURL"].endswith("/v1")
    assert config["provider"]["local-bonsai"]["options"]["timeout"] == 1200000
    assert config["provider"]["local-bonsai"]["options"]["chunkTimeout"] == 1200000
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

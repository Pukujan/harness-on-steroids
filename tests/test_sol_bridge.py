from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest
from src.sol_bridge import (
    ChatCompletionsClient,
    RepoTools,
    RunRecorder,
    SolBridge,
    SolBridgeError,
    SolConfig,
    _sse_data,
)


class FakeResponse:
    def __init__(self, events: list[dict]) -> None:
        self.lines = []
        for event in events:
            self.lines.extend(
                [
                    b"event: message\n",
                    f"data: {json.dumps(event)}\n".encode(),
                    b"\n",
                ]
            )
        self.lines.append(b"data: [DONE]\n\n")

    def __iter__(self):
        return iter(self.lines)

    def close(self) -> None:
        pass


def test_sse_data_joins_multiline_events() -> None:
    assert list(_sse_data([b"data: one\n", b"data: two\n", b"\n"])) == ["one\ntwo"]


def test_streaming_client_posts_to_chat_completions(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: dict[str, object] = {}

    def fake_urlopen(request, timeout):
        seen["url"] = request.full_url
        seen["timeout"] = timeout
        return FakeResponse([{"choices": [{"delta": {"content": "ok"}}]}])

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    config = SolConfig(api_key="test", timeout_seconds=12)
    chunks = list(ChatCompletionsClient(config).stream([], []))
    assert chunks[0]["choices"][0]["delta"]["content"] == "ok"
    assert seen == {"url": "https://ckffai.com/v1/chat/completions", "timeout": 12}


def test_tool_loop_inspects_then_finishes(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("hello", encoding="utf-8")

    class FakeClient:
        model = "fake-sol"

        def __init__(self) -> None:
            self.turn = 0

        def stream(self, messages, tools):
            self.turn += 1
            if self.turn == 1:
                yield {
                    "choices": [
                        {
                            "delta": {
                                "tool_calls": [
                                    {
                                        "index": 0,
                                        "id": "call-1",
                                        "function": {
                                            "name": "list_files",
                                            "arguments": '{"pattern":"*.md"}',
                                        },
                                    }
                                ]
                            }
                        }
                    ]
                }
            else:
                yield {"choices": [{"delta": {"content": "Inspected README.md."}}]}

    result = SolBridge(
        tmp_path,
        FakeClient(),
        recorder=RunRecorder(tmp_path, "test-run"),
    ).run("Inspect the repository.")
    assert result.final_text == "Inspected README.md."
    assert result.rounds == 2
    assert result.tool_calls == 1
    assert result.record_path.is_file()
    assert '"event": "tool_result"' in result.record_path.read_text(encoding="utf-8")


def test_repo_tools_block_secrets_and_escape(tmp_path: Path) -> None:
    tools = RepoTools(tmp_path)
    (tmp_path / ".env").write_text("secret", encoding="utf-8")
    with pytest.raises(SolBridgeError):
        tools.read_file(".env")
    with pytest.raises(SolBridgeError):
        tools.read_file("../outside.txt")


def test_dry_run_does_not_apply_patch(tmp_path: Path) -> None:
    path = tmp_path / "note.txt"
    path.write_text("before\n", encoding="utf-8")
    patch = """diff --git a/note.txt b/note.txt
--- a/note.txt
+++ b/note.txt
@@ -1 +1 @@
-before
+after
"""
    result = RepoTools(tmp_path, dry_run=True).apply_patch(patch)
    assert result["dry_run"] is True
    assert path.read_text(encoding="utf-8") == "before\n"


def test_codex_patch_updates_untracked_file(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    path = tmp_path / "note.md"
    path.write_text("before", encoding="utf-8")
    patch = """*** Begin Patch
*** Update File: note.md
@@
-before
+after
*** End Patch
"""
    result = RepoTools(tmp_path).apply_patch(patch)
    assert result["ok"] is True
    assert result["stage"] == "untracked-direct"
    assert path.read_text(encoding="utf-8") == "after"

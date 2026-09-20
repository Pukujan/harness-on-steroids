import json
from pathlib import Path

from research.extract_replay import user_text_from_payload, write_session


def test_user_text_from_payload_string_and_list() -> None:
    assert user_text_from_payload({"type": "message", "role": "user", "content": "  hi  "}) == "hi"
    assert (
        user_text_from_payload(
            {
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": "a"}, {"text": "b"}],
            }
        )
        == "a\nb"
    )
    assert user_text_from_payload({"type": "message", "role": "assistant", "content": "no"}) == ""


def test_write_session_does_not_belong_in_git(tmp_path: Path, monkeypatch) -> None:
    import research.extract_replay as er

    monkeypatch.setattr(er, "OUT", tmp_path)
    dest = er.write_session("abc123def456", ["hello task"], ["exec", "wait"])
    assert dest.name == "abc123def456"
    assert (dest / "user.md").read_text(encoding="utf-8") == "hello task"
    meta = json.loads((dest / "meta.json").read_text(encoding="utf-8"))
    assert meta["user_turns"] == 1
    assert meta["first"] == "exec"
    assert meta["patch"] is False
    gitignore = Path(__file__).resolve().parents[1].joinpath(".gitignore").read_text(encoding="utf-8")
    assert "data/" in gitignore

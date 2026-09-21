import json
from pathlib import Path

from research.replay_lib import cell, outcome_label, tool_seq


def test_tool_seq_reads_utf16_and_utf8(tmp_path: Path) -> None:
    events = [
        {"type": "tool_use", "part": {"tool": "glob"}},
        {"type": "tool_use", "part": {"tool": "read"}},
    ]
    utf8 = tmp_path / "a.ndjson"
    utf8.write_text("\n".join(json.dumps(e) for e in events) + "\n", encoding="utf-8")
    utf16 = tmp_path / "b.ndjson"
    utf16.write_bytes(("\n".join(json.dumps(e) for e in events) + "\n").encode("utf-16"))
    assert tool_seq(utf8) == ["glob", "read"]
    assert tool_seq(utf16) == ["glob", "read"]
    assert outcome_label(["glob", "read"]) == "partial"
    assert cell(["glob", "grep", "read"]).startswith("yes/none/")


def test_empty_ndjson_is_empty_list(tmp_path: Path) -> None:
    p = tmp_path / "empty.ndjson"
    p.write_text("", encoding="utf-8")
    assert tool_seq(p) == []


def test_tool_seq_utf16_then_utf8_append(tmp_path: Path) -> None:
    p = tmp_path / "mix.ndjson"
    first = json.dumps({"type": "tool_use", "part": {"tool": "glob"}}) + "\n"
    second = json.dumps({"type": "tool_use", "part": {"tool": "read"}}) + "\n"
    p.write_bytes(first.encode("utf-16") + second.encode("utf-8"))
    seq = tool_seq(p)
    assert "glob" in seq

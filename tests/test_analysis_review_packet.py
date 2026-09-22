from __future__ import annotations

import json
from pathlib import Path

import pytest
from research.build_analysis_review_packet import build_review_packet


def _row(episode: str, ordinal: int, event_id: str, **extra: object) -> dict[str, object]:
    event: dict[str, object] = {
        "episode_id": episode,
        "event_id": event_id,
        "lane": "codex",
        "ordinal": ordinal,
        "kind": "tool_call",
        "actor": "assistant",
        "observation": "observed",
        "attributes": {},
        **extra,
    }
    return {"sample_id": f"sample-{event_id}", "split": "pilot", "event": event}


def test_review_packet_is_sorted_and_body_free(tmp_path: Path) -> None:
    source = tmp_path / "pilot-events.jsonl"
    source.write_text(
        "\n".join(
            json.dumps(row)
            for row in (
                _row("episode-b", 2, "b2"),
                _row("episode-a", 2, "a2"),
                _row("episode-a", 1, "a1"),
            )
        )
        + "\n",
        encoding="utf-8",
    )
    output = tmp_path / "packet"

    manifest = build_review_packet((source,), output)

    assert manifest["episode_count"] == 2
    assert manifest["event_count"] == 3
    rows = [json.loads(line) for line in (output / "episodes.jsonl").read_text().splitlines()]
    assert [row["episode_id"] for row in rows] == ["episode-a", "episode-b"]
    assert [item["event"]["event_id"] for item in rows[0]["events"]] == ["a1", "a2"]
    assert "adjudication" in rows[0]
    assert "body" not in json.dumps(rows)


def test_review_packet_rejects_holdout_and_body_fields(tmp_path: Path) -> None:
    source = tmp_path / "events.jsonl"
    source.write_text(
        json.dumps({"split": "holdout", "event": _row("e", 1, "x")["event"]}) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="pilot"):
        build_review_packet((source,), tmp_path / "packet")

    source.write_text(
        json.dumps({"split": "pilot", "event": _row("e", 1, "x", text="secret")["event"]})
        + "\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="body-bearing"):
        build_review_packet((source,), tmp_path / "packet")

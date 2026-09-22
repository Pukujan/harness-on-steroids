from __future__ import annotations

from research.run_jev_shadow_annotation import expected_labels, parse_answers, select_events


def _event(event_id: str, **values: object) -> dict[str, object]:
    event = {
        "event_id": event_id,
        "episode_id": "episode",
        "lane": "chatgpt_chat",
        "kind": "message",
        "actor": "assistant",
        "tool_family": None,
        "attributes": {},
    }
    event.update(values)
    return {"event": event, "split": "pilot"}


def test_expected_labels_are_structural() -> None:
    row = _event("x", kind="citation", attributes={"content_type": "code"})
    labels = expected_labels(row["event"])
    assert labels["citation_event_present"] is True
    assert labels["code_event"] is True
    assert labels["research_observed"] is False


def test_selection_is_deterministic_and_covers_predicates() -> None:
    rows = [
        _event("a", kind="citation"),
        _event("b", kind="unknown"),
        _event("c", kind="research", tool_family="research"),
        _event("d", kind="tool_call", tool_family="inspect"),
        _event("e", kind="tool_call", tool_family="mutate"),
        _event("f", kind="tool_call", tool_family="verify"),
        _event("g", kind="message", attributes={"content_type": "code"}),
        _event("h", kind="message", attributes={"content_type": "execution_output"}),
    ]
    first = select_events(rows, 8)
    second = select_events(list(reversed(rows)), 8)
    assert [row["event"]["event_id"] for row in first] == [
        row["event"]["event_id"] for row in second
    ]
    assert len(first) == 8


def test_selection_fills_requested_budget_after_coverage() -> None:
    rows = [
        _event(event_id, kind="message")
        for event_id in ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j")
    ]
    rows.extend(
        [
            _event("k", kind="citation"),
            _event("l", kind="unknown"),
            _event("m", kind="research", tool_family="research"),
            _event("n", kind="tool_call", tool_family="inspect"),
            _event("o", kind="tool_call", tool_family="mutate"),
            _event("p", kind="tool_call", tool_family="verify"),
            _event("q", kind="message", attributes={"content_type": "code"}),
            _event("r", kind="message", attributes={"content_type": "execution_output"}),
        ]
    )
    selected = select_events(rows, 12)
    assert len(selected) == 12
    selected_ids = {row["event"]["event_id"] for row in selected}
    assert {"k", "l", "m", "n", "o", "p", "q", "r"}.issubset(selected_ids)
    assert len(selected_ids) == 12


def test_parse_answers_accepts_noul_probabilities() -> None:
    payload = {
        "answers": {
            "shadow__citation_event_present": {"noul": 0.91, "confidence": 0.91},
            "shadow__research_observed": {"probability": 0.2},
        }
    }
    parsed = parse_answers(payload)
    assert parsed["citation_event_present"]["probability"] == 0.91
    assert parsed["research_observed"]["probability"] == 0.2
    assert parsed["code_event"]["valid"] is False

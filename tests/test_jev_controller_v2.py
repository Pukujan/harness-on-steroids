from __future__ import annotations

import json
from pathlib import Path

import pytest
from src.hos.controller import (
    AdapterObservation,
    AdapterStepResult,
    ControllerAction,
    ControllerPhase,
    DecisionBead,
    DecisionContext,
    GrokBuildAdapter,
    JevController,
    JevDecision,
    JevDecisionLoop,
    OpenCodeAdapter,
    PiAdapter,
    build_typed_questions,
    validate_jev_decision,
)
from src.hos.controller.adapters import extract_event_seq, extract_session_id


def make_context() -> DecisionContext:
    bead = DecisionBead(
        "bead-1",
        "Implement the bounded change",
        acceptance_criteria=("targeted checks pass",),
    )
    context = DecisionContext.from_ask(
        "task-hash",
        "Implement the bounded change and verify it.",
        constraints=("inspect before write", "verify after change"),
        timeout_budget_s=60,
    )
    context.open_beads = (bead,)
    context.candidate_beads = (bead,)
    return context


def decision(action: ControllerAction, *, confidence: float = 0.95) -> JevDecision:
    return JevDecision(
        task_class="implement",
        next_bead="bead-1",
        next_action=action,
        verification_level="targeted",
        evidence_sufficient=True,
        should_continue=True,
        readiness="ready",
        risk="low",
        confidence=confidence,
    )


def test_context_contains_full_relevant_decision_inputs() -> None:
    context = make_context()
    context.add_conversation("Owner corrected the target file.")
    context.record_observation(
        AdapterObservation(
            "tool_result",
            tool_name="read",
            status="ok",
            summary="The target file exists.",
        )
    )
    payload = context.to_payload()

    assert payload["original_ask"].startswith("Implement")
    assert payload["candidate_beads"][0]["id"] == "bead-1"
    assert payload["adapter_observations"][0]["tool_name"] == "read"
    assert "The target file exists." in payload["evidence"]
    assert "INSPECT_REPO" in payload["allowed_actions"]
    assert "raw" not in json.dumps(payload).lower()


def test_typed_questions_use_choice_score_and_noul() -> None:
    questions = build_typed_questions(make_context())

    assert len(questions) == 9
    assert questions["task-hash__task_class"]["type"] == "choice"
    assert questions["task-hash__next_action"]["criteria"]["INSPECT_REPO"]
    assert any(
        option == "INSPECT_REPO"
        for option in questions["task-hash__next_action"]["criteria"]
    )
    assert questions["task-hash__evidence_sufficient"]["type"] == "noul"
    assert questions["task-hash__evidence_sufficient"]["true_when"]
    assert questions["task-hash__readiness"]["type"] == "score"
    assert len(questions["task-hash__readiness"]["criteria"]) == 5


def test_jev_typed_response_is_parsed_into_structured_answers() -> None:
    parsed = JevController._parse_jev_decision(
        {
            "answers": {
                "task-hash__task_class": {"choice": "implement", "confidence": 0.99},
                "task-hash__next_bead": {"choice": "bead-1", "confidence": 0.9},
                "task-hash__next_action": {
                    "choice": "INSPECT_REPO",
                    "confidence": 0.8,
                    "probabilities": {"INSPECT_REPO": 0.8, "READ_DOCS": 0.2},
                },
                "task-hash__delegate_target": {"choice": "local"},
                "task-hash__verification_level": {"choice": "targeted"},
                "task-hash__evidence_sufficient": {"probability": 0.7},
                "task-hash__should_continue": {"value": True},
                "task-hash__readiness": {"score": "ready"},
                "task-hash__risk": {"score": "low"},
            }
        }
    )

    assert parsed.next_action is ControllerAction.INSPECT_REPO
    assert parsed.next_bead == "bead-1"
    assert parsed.evidence_sufficient is True
    assert parsed.should_continue is True
    assert parsed.confidence == 0.8
    assert parsed.probabilities["INSPECT_REPO"] == 0.8


def test_jev_native_noul_and_score_answers_are_reduced_safely() -> None:
    parsed = JevController._parse_jev_decision(
        {
            "answers": {
                "task-hash__task_class": {
                    "type": "choice",
                    "choice": "implement",
                    "confidence": 0.8,
                },
                "task-hash__next_bead": {"type": "choice", "choice": "bead-1"},
                "task-hash__next_action": {
                    "type": "choice",
                    "choice": "INSPECT_REPO",
                    "confidence": 0.7,
                },
                "task-hash__delegate_target": {"choice": "local"},
                "task-hash__verification_level": {"choice": "targeted"},
                "task-hash__evidence_sufficient": {"type": "noul", "noul": 0.7},
                "task-hash__should_continue": {"type": "noul", "noul": 0.8},
                "task-hash__readiness": {
                    "type": "score",
                    "score": 1.8,
                    "legend": {"0": "blocked", "1": "proposed", "2": "ready"},
                },
                "task-hash__risk": {
                    "type": "score",
                    "score": 0.2,
                    "legend": {"0": "low", "1": "high"},
                },
            }
        }
    )

    assert parsed.evidence_sufficient is True
    assert parsed.should_continue is True
    assert parsed.readiness == "ready"
    assert parsed.risk == "low"
    assert parsed.confidence == 0.7


def test_invalid_and_low_confidence_decisions_are_rejected() -> None:
    context = make_context()

    illegal = validate_jev_decision(decision(ControllerAction.WRITE_FILE), context)
    low = validate_jev_decision(decision(ControllerAction.INSPECT_REPO, confidence=0.2), context)

    assert not illegal.accepted
    assert illegal.reason == "illegal_action_for_phase"
    assert not low.accepted
    assert low.reason == "low_confidence"


class FakeController:
    def __init__(self) -> None:
        self.seen: list[dict[str, object]] = []
        self.responses = [
            decision(ControllerAction.INSPECT_REPO),
            decision(ControllerAction.DECOMPOSE),
            decision(ControllerAction.APPLY_PATCH),
        ]

    def decide_context(self, context: DecisionContext) -> JevDecision:
        self.seen.append(context.to_payload())
        return self.responses[len(self.seen) - 1]


class FakeAdapter:
    def __init__(self) -> None:
        self.calls: list[ControllerAction] = []

    def run_step(self, context: DecisionContext, decision: JevDecision) -> AdapterStepResult:
        self.calls.append(decision.next_action)
        return AdapterStepResult(
            status="ok",
            observations=(
                AdapterObservation(
                    event_kind=f"{decision.next_action.value.lower()}_result",
                    status="ok",
                    summary=f"completed {decision.next_action.value}",
                ),
            ),
            changed_paths=("src/target.py",)
            if decision.next_action is ControllerAction.APPLY_PATCH
            else (),
        )


def test_loop_accumulates_context_across_three_bounded_steps() -> None:
    controller = FakeController()
    adapter = FakeAdapter()
    result = JevDecisionLoop(controller, adapter, max_steps=3).run(make_context())

    assert result.status == "budget_exhausted"
    assert result.steps == 3
    assert adapter.calls == [
        ControllerAction.INSPECT_REPO,
        ControllerAction.DECOMPOSE,
        ControllerAction.APPLY_PATCH,
    ]
    assert len(controller.seen[0]["adapter_observations"]) == 0
    assert len(controller.seen[1]["adapter_observations"]) == 1
    assert len(controller.seen[2]["adapter_observations"]) == 2
    assert controller.seen[1]["phase"] == ControllerPhase.OBSERVE.value
    assert controller.seen[2]["phase"] == ControllerPhase.PLAN.value
    assert result.context.changed_paths == ("src/target.py",)


def test_unavailable_controller_falls_back_without_running_adapter() -> None:
    class UnavailableController:
        def decide_context(self, context: DecisionContext) -> JevDecision:
            return JevDecision.unavailable("missing_api_key")

    adapter = FakeAdapter()
    result = JevDecisionLoop(UnavailableController(), adapter).run(make_context())

    assert result.status == "fallback"
    assert result.decisions[0].source == "fallback"
    assert result.decisions[0].next_action is ControllerAction.ESCALATE
    assert adapter.calls == []


@pytest.mark.parametrize("adapter_type", [OpenCodeAdapter, GrokBuildAdapter, PiAdapter])
def test_each_cli_adapter_reduces_structured_events_without_raw_body(
    tmp_path: Path, adapter_type
) -> None:
    events = tmp_path / f"{adapter_type.__name__}.ndjson"
    events.write_text(
        json.dumps(
            {
                "type": "tool_result",
                "session_id": "native-session-123",
                "part": {"tool": "read"},
                "status": "ok",
                "summary": "read completed",
                "body": "PRIVATE RAW EVENT BODY",
            }
        ),
        encoding="utf-8",
    )

    adapter = adapter_type(executable="missing-test-executable")
    reduced = adapter.stream_events(events)

    assert reduced[0].event_kind == "tool_result"
    assert reduced[0].tool_name == "read"
    assert "PRIVATE" not in json.dumps([event.to_payload() for event in reduced])
    assert extract_event_seq(events) == reduced
    assert extract_session_id(events) == "native-session-123"


def test_v2_request_payload_pins_model_and_context_questions() -> None:
    controller = JevController(api_key="test-key")
    request = controller._context_request_payload(make_context())

    assert request["model"] == "typesafe/jev-1.13"
    assert request["state"]["records"][0]["record"]["original_ask"].startswith("Implement")
    assert len(request["questions"]) == 9
    assert "stream" not in request

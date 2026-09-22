"""Bounded Jev routing for the harness.

Jev proposes one next action from compact state. Deterministic guards and the
selected harness still own legality, tools, and side effects.
"""

from __future__ import annotations

import json
import math
import os
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Protocol, Sequence
from urllib.parse import urlsplit


class ControllerPhase(str, Enum):
    INTAKE = "intake"
    OBSERVE = "observe"
    UNDERSTAND = "understand"
    PLAN = "plan"
    DELEGATE = "delegate"
    EXECUTE = "execute"
    VERIFY = "verify"
    RECOVER = "recover"
    COMMUNICATE = "communicate"
    COMPLETE = "complete"


class ControllerAction(str, Enum):
    CLASSIFY_REQUEST = "CLASSIFY_REQUEST"
    INSPECT_REPO = "INSPECT_REPO"
    INSPECT_TASK_STATE = "INSPECT_TASK_STATE"
    INSPECT_ENV = "INSPECT_ENV"
    SEARCH_LOCAL = "SEARCH_LOCAL"
    READ_SOURCE = "READ_SOURCE"
    READ_DOCS = "READ_DOCS"
    CHECK_HISTORY = "CHECK_HISTORY"
    REPRODUCE = "REPRODUCE"
    BUILD_CONTEXT_PACK = "BUILD_CONTEXT_PACK"
    RESEARCH_EXTERNAL = "RESEARCH_EXTERNAL"
    DECOMPOSE = "DECOMPOSE"
    CREATE_TASK = "CREATE_TASK"
    CREATE_BEAD = "CREATE_BEAD"
    UPDATE_BEAD = "UPDATE_BEAD"
    CLOSE_BEAD = "CLOSE_BEAD"
    DELEGATE_TO_SOL = "DELEGATE_TO_SOL"
    DELEGATE_TO_SPECIALIST = "DELEGATE_TO_SPECIALIST"
    WAIT_FOR_WORK = "WAIT_FOR_WORK"
    RESUME_WORK = "RESUME_WORK"
    APPLY_PATCH = "APPLY_PATCH"
    WRITE_FILE = "WRITE_FILE"
    RUN_TARGETED_TESTS = "RUN_TARGETED_TESTS"
    RUN_BROAD_TESTS = "RUN_BROAD_TESTS"
    RUN_CONTRACT_CHECK = "RUN_CONTRACT_CHECK"
    CHECK_GIT_DIFF = "CHECK_GIT_DIFF"
    CHECK_STATUS = "CHECK_STATUS"
    REVIEW_RESULT = "REVIEW_RESULT"
    RETRY_TRANSIENT_FAILURE = "RETRY_TRANSIENT_FAILURE"
    RECOVER_AFTER_FAILURE = "RECOVER_AFTER_FAILURE"
    REVERT_CHANGE = "REVERT_CHANGE"
    ASK_USER = "ASK_USER"
    UPDATE_USER = "UPDATE_USER"
    FINALIZE = "FINALIZE"
    ESCALATE = "ESCALATE"


ACTION_DESCRIPTIONS: dict[str, str] = {
    action.value: action.value.replace("_", " ").lower() for action in ControllerAction
}
ACTION_DESCRIPTIONS.update(
    {
        "INSPECT_REPO": (
            "Inspect repository structure and current files before deciding on a change."
        ),
        "BUILD_CONTEXT_PACK": "Assemble a compact evidence pack for a bounded reasoning task.",
        "DELEGATE_TO_SOL": "Delegate a bounded hard-reasoning slice to the configured Sol worker.",
        "CREATE_BEAD": "Create a durable bead for a long-horizon work unit or dependency.",
        "UPDATE_BEAD": "Update an existing bead with evidence, status, or dependency changes.",
        "CLOSE_BEAD": "Close a bead only after its acceptance evidence is recorded.",
        "APPLY_PATCH": "Apply an approved patch to an existing file after inspection.",
        "RUN_TARGETED_TESTS": "Run the smallest checks that cover the changed behavior.",
        "RUN_BROAD_TESTS": "Run broader repository checks after targeted checks pass.",
        "ASK_USER": "Ask the owner for missing input, authorization, or a decision.",
        "FINALIZE": "Deliver the requested result after completion evidence and verification.",
        "ESCALATE": (
            "Stop autonomous routing and escalate an unsafe or repeatedly blocked situation."
        ),
    }
)


LEGAL_ACTIONS_BY_PHASE: dict[ControllerPhase, frozenset[ControllerAction]] = {
    ControllerPhase.INTAKE: frozenset(
        {
            ControllerAction.CLASSIFY_REQUEST,
            ControllerAction.INSPECT_REPO,
            ControllerAction.INSPECT_TASK_STATE,
            ControllerAction.INSPECT_ENV,
            ControllerAction.SEARCH_LOCAL,
            ControllerAction.READ_DOCS,
            ControllerAction.BUILD_CONTEXT_PACK,
            ControllerAction.ASK_USER,
            ControllerAction.ESCALATE,
        }
    ),
    ControllerPhase.OBSERVE: frozenset(
        {
            ControllerAction.INSPECT_REPO,
            ControllerAction.INSPECT_TASK_STATE,
            ControllerAction.INSPECT_ENV,
            ControllerAction.SEARCH_LOCAL,
            ControllerAction.READ_SOURCE,
            ControllerAction.READ_DOCS,
            ControllerAction.CHECK_HISTORY,
            ControllerAction.REPRODUCE,
            ControllerAction.BUILD_CONTEXT_PACK,
            ControllerAction.CLASSIFY_REQUEST,
            ControllerAction.DECOMPOSE,
            ControllerAction.ASK_USER,
            ControllerAction.ESCALATE,
        }
    ),
    ControllerPhase.UNDERSTAND: frozenset(
        {
            ControllerAction.INSPECT_REPO,
            ControllerAction.SEARCH_LOCAL,
            ControllerAction.READ_SOURCE,
            ControllerAction.READ_DOCS,
            ControllerAction.CHECK_HISTORY,
            ControllerAction.BUILD_CONTEXT_PACK,
            ControllerAction.DECOMPOSE,
            ControllerAction.CREATE_BEAD,
            ControllerAction.DELEGATE_TO_SOL,
            ControllerAction.DELEGATE_TO_SPECIALIST,
            ControllerAction.ASK_USER,
            ControllerAction.ESCALATE,
        }
    ),
    ControllerPhase.PLAN: frozenset(
        {
            ControllerAction.CREATE_BEAD,
            ControllerAction.UPDATE_BEAD,
            ControllerAction.CLOSE_BEAD,
            ControllerAction.DECOMPOSE,
            ControllerAction.BUILD_CONTEXT_PACK,
            ControllerAction.DELEGATE_TO_SOL,
            ControllerAction.DELEGATE_TO_SPECIALIST,
            ControllerAction.APPLY_PATCH,
            ControllerAction.WRITE_FILE,
            ControllerAction.ASK_USER,
            ControllerAction.ESCALATE,
        }
    ),
    ControllerPhase.DELEGATE: frozenset(
        {
            ControllerAction.DELEGATE_TO_SOL,
            ControllerAction.DELEGATE_TO_SPECIALIST,
            ControllerAction.WAIT_FOR_WORK,
            ControllerAction.RESUME_WORK,
            ControllerAction.CHECK_STATUS,
            ControllerAction.UPDATE_BEAD,
            ControllerAction.ASK_USER,
            ControllerAction.ESCALATE,
        }
    ),
    ControllerPhase.EXECUTE: frozenset(
        {
            ControllerAction.APPLY_PATCH,
            ControllerAction.WRITE_FILE,
            ControllerAction.RUN_TARGETED_TESTS,
            ControllerAction.CHECK_GIT_DIFF,
            ControllerAction.CHECK_STATUS,
            ControllerAction.WAIT_FOR_WORK,
            ControllerAction.RESUME_WORK,
            ControllerAction.RETRY_TRANSIENT_FAILURE,
            ControllerAction.RECOVER_AFTER_FAILURE,
            ControllerAction.ASK_USER,
            ControllerAction.ESCALATE,
        }
    ),
    ControllerPhase.VERIFY: frozenset(
        {
            ControllerAction.RUN_TARGETED_TESTS,
            ControllerAction.RUN_BROAD_TESTS,
            ControllerAction.RUN_CONTRACT_CHECK,
            ControllerAction.CHECK_GIT_DIFF,
            ControllerAction.CHECK_STATUS,
            ControllerAction.REVIEW_RESULT,
            ControllerAction.UPDATE_BEAD,
            ControllerAction.CLOSE_BEAD,
            ControllerAction.FINALIZE,
            ControllerAction.RETRY_TRANSIENT_FAILURE,
            ControllerAction.RECOVER_AFTER_FAILURE,
            ControllerAction.REVERT_CHANGE,
            ControllerAction.ASK_USER,
            ControllerAction.ESCALATE,
        }
    ),
    ControllerPhase.RECOVER: frozenset(
        {
            ControllerAction.INSPECT_REPO,
            ControllerAction.INSPECT_TASK_STATE,
            ControllerAction.CHECK_STATUS,
            ControllerAction.RETRY_TRANSIENT_FAILURE,
            ControllerAction.RECOVER_AFTER_FAILURE,
            ControllerAction.REVERT_CHANGE,
            ControllerAction.RUN_TARGETED_TESTS,
            ControllerAction.ASK_USER,
            ControllerAction.ESCALATE,
        }
    ),
    ControllerPhase.COMMUNICATE: frozenset(
        {
            ControllerAction.UPDATE_USER,
            ControllerAction.FINALIZE,
            ControllerAction.ASK_USER,
            ControllerAction.ESCALATE,
        }
    ),
    ControllerPhase.COMPLETE: frozenset(
        {ControllerAction.FINALIZE, ControllerAction.UPDATE_USER}
    ),
}


TASK_CLASS_CHOICES = (
    "inspect",
    "research",
    "reproduce",
    "plan",
    "implement",
    "test",
    "verify",
    "recover",
    "communicate",
    "escalate",
)
DELEGATE_TARGET_CHOICES = ("local", "sol", "specialist", "owner")
VERIFICATION_CHOICES = ("none", "targeted", "broad", "acceptance")
READINESS_CHOICES = ("blocked", "proposed", "ready", "partial", "complete")
RISK_CHOICES = ("low", "medium", "high", "unknown")


@dataclass(frozen=True)
class ControllerState:
    """Non-sensitive state exposed to Jev."""

    task_hash: str
    phase: ControllerPhase
    intent_class: str
    observed_facts: tuple[str, ...] = ()
    recent_event_kinds: tuple[str, ...] = ()
    constraints: tuple[str, ...] = ()
    verification_fresh: bool = False
    work_running: bool = False
    user_input_required: bool = False

    def to_payload(self) -> dict[str, Any]:
        return {
            "intent_class": self.intent_class,
            "phase": self.phase.value,
            "observed_facts": list(self.observed_facts),
            "recent_event_kinds": list(self.recent_event_kinds),
            "constraints": list(self.constraints),
            "verification_fresh": self.verification_fresh,
            "work_running": self.work_running,
            "user_input_required": self.user_input_required,
        }


@dataclass(frozen=True)
class ControllerDecision:
    action: ControllerAction
    phase: ControllerPhase
    confidence: float | None
    status: str
    source: str = "jev"
    probabilities: dict[str, float] = field(default_factory=dict)
    error_type: str | None = None


@dataclass(frozen=True)
class DecisionBead:
    """A small durable work unit that Jev may select, without owning it."""

    bead_id: str
    description: str
    dependencies: tuple[str, ...] = ()
    acceptance_criteria: tuple[str, ...] = ()
    status: str = "open"

    def to_payload(self) -> dict[str, Any]:
        return {
            "id": self.bead_id,
            "description": self.description,
            "dependencies": list(self.dependencies),
            "acceptance_criteria": list(self.acceptance_criteria),
            "status": self.status,
        }


# The more explicit name is useful to adapter authors; retain a short alias
# for callers that already use the contract's "candidate bead" terminology.
CandidateBead = DecisionBead


@dataclass(frozen=True)
class AdapterObservation:
    """A privacy-safe, normalized observation folded back into Jev context."""

    event_kind: str
    tool_name: str | None = None
    status: str = "observed"
    summary: str = ""
    failure: str | None = None
    changed_paths: tuple[str, ...] = ()

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "event_kind": self.event_kind,
            "status": self.status,
            "summary": self.summary,
        }
        if self.tool_name:
            payload["tool_name"] = self.tool_name
        if self.failure:
            payload["failure"] = self.failure
        if self.changed_paths:
            payload["changed_paths"] = list(self.changed_paths)
        return payload


@dataclass
class DecisionContext:
    """The bounded, evolving state sent to Jev on every decision round."""

    task_hash: str
    original_ask: str
    relevant_conversation: tuple[str, ...] = ()
    open_beads: tuple[DecisionBead, ...] = ()
    candidate_beads: tuple[DecisionBead, ...] = ()
    adapter_observations: tuple[AdapterObservation, ...] = ()
    evidence: tuple[str, ...] = ()
    repo_facts: tuple[str, ...] = ()
    changed_paths: tuple[str, ...] = ()
    test_results: tuple[str, ...] = ()
    constraints: tuple[str, ...] = ()
    phase: ControllerPhase = ControllerPhase.INTAKE
    allowed_actions: tuple[str, ...] = ()
    timeout_budget_s: float | None = None
    retry_count: int = 0
    user_input_status: str = "not_required"
    current_bead_id: str | None = None

    @classmethod
    def from_ask(
        cls,
        task_hash: str,
        original_ask: str,
        *,
        constraints: Sequence[str] = (),
        timeout_budget_s: float | None = None,
    ) -> "DecisionContext":
        return cls(
            task_hash=task_hash,
            original_ask=original_ask,
            constraints=tuple(constraints),
            timeout_budget_s=timeout_budget_s,
        )

    def legal_actions(self) -> tuple[str, ...]:
        if self.allowed_actions:
            return tuple(self.allowed_actions)
        allowed = LEGAL_ACTIONS_BY_PHASE[self.phase]
        return tuple(action.value for action in ControllerAction if action in allowed)

    def add_conversation(self, turn: str) -> None:
        if turn:
            self.relevant_conversation += (turn,)

    def add_evidence(self, *items: str) -> None:
        self.evidence += tuple(item for item in items if item)

    def record_observation(self, observation: AdapterObservation) -> None:
        self.adapter_observations += (observation,)
        self.changed_paths += tuple(
            path for path in observation.changed_paths if path not in self.changed_paths
        )
        if observation.failure:
            self.add_evidence(f"adapter_failure:{observation.failure}")
        if observation.summary:
            self.add_evidence(observation.summary)

    def set_phase(self, phase: ControllerPhase) -> None:
        self.phase = phase

    def to_payload(self, *, max_chars: int = 32_000) -> dict[str, Any]:
        """Serialize context while retaining the ask and newest observations.

        Jev receives derived event summaries rather than raw adapter bodies. If
        the request budget is exceeded, older conversation/event detail is
        compacted deterministically before the request is sent.
        """

        payload: dict[str, Any] = {
            "task_hash": self.task_hash,
            "original_ask": self.original_ask,
            "relevant_conversation": list(self.relevant_conversation),
            "phase": self.phase.value,
            "allowed_actions": list(self.legal_actions()),
            "open_beads": [bead.to_payload() for bead in self.open_beads],
            "candidate_beads": [bead.to_payload() for bead in self.candidate_beads],
            "adapter_observations": [
                observation.to_payload() for observation in self.adapter_observations
            ],
            "evidence": list(self.evidence),
            "repo_facts": list(self.repo_facts),
            "changed_paths": list(self.changed_paths),
            "test_results": list(self.test_results),
            "constraints": list(self.constraints),
            "timeout_budget_s": self.timeout_budget_s,
            "retry_count": self.retry_count,
            "user_input_status": self.user_input_status,
            "current_bead_id": self.current_bead_id,
        }
        if max_chars <= 0:
            raise ValueError("max_chars must be positive")

        def encoded_size() -> int:
            return len(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))

        # Preserve the original ask, current phase, candidates, and newest
        # observations first. Older narrative is the least decision-critical.
        while encoded_size() > max_chars and payload["relevant_conversation"]:
            payload["relevant_conversation"].pop(0)
        while encoded_size() > max_chars and len(payload["adapter_observations"]) > 1:
            payload["adapter_observations"].pop(0)
        while encoded_size() > max_chars and payload["evidence"]:
            payload["evidence"].pop(0)
        while encoded_size() > max_chars and payload["repo_facts"]:
            payload["repo_facts"].pop(0)
        if encoded_size() > max_chars:
            payload["original_ask"] = payload["original_ask"][: max(0, max_chars // 2)]
        return payload

    def to_json(self, *, max_chars: int = 32_000) -> str:
        return json.dumps(self.to_payload(max_chars=max_chars), ensure_ascii=False)


@dataclass(frozen=True)
class TypedQuestion:
    key: str
    question_type: str
    instructions: str
    criteria: Mapping[str, Any] | Sequence[str] | None = None
    true_when: str | None = None
    false_when: str | None = None

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "type": self.question_type,
            "instructions": self.instructions,
        }
        if self.criteria is not None:
            if isinstance(self.criteria, Mapping):
                payload["criteria"] = {
                    str(name): str(description) for name, description in self.criteria.items()
                }
            else:
                payload["criteria"] = [str(level) for level in self.criteria]
        elif self.question_type == "noul":
            payload["true_when"] = self.true_when or "The statement is supported by the context."
            payload["false_when"] = (
                self.false_when or "The statement is not supported by the context."
            )
        return payload


def build_typed_questions(context: DecisionContext) -> dict[str, dict[str, Any]]:
    """Build the independent v2 Choice, Score, and Noul questions."""

    prefix = f"{context.task_hash}__"
    candidate_choices: dict[str, str] = {
        bead.bead_id: bead.description for bead in context.candidate_beads
    }
    if not candidate_choices:
        candidate_choices = {"NONE": "No candidate bead is currently available."}
    action_choices = {
        action: ACTION_DESCRIPTIONS.get(action, action.replace("_", " ").lower())
        for action in context.legal_actions()
    }
    questions = (
        TypedQuestion(
            prefix + "task_class",
            "choice",
            "Classify the owner request and current bounded work step.",
            {choice: choice for choice in TASK_CLASS_CHOICES},
        ),
        TypedQuestion(
            prefix + "next_bead",
            "choice",
            "Choose one currently available candidate bead, or NONE.",
            candidate_choices,
        ),
        TypedQuestion(
            prefix + "next_action",
            "choice",
            "Choose exactly one legal, bounded next harness action.",
            action_choices,
        ),
        TypedQuestion(
            prefix + "delegate_target",
            "choice",
            "Choose the target only if delegation is needed for this bounded step.",
            {choice: choice for choice in DELEGATE_TARGET_CHOICES},
        ),
        TypedQuestion(
            prefix + "verification_level",
            "choice",
            "Choose the verification level supported by the current evidence.",
            {choice: choice for choice in VERIFICATION_CHOICES},
        ),
        TypedQuestion(
            prefix + "evidence_sufficient",
            "noul",
            "Is the current evidence sufficient to take the proposed bounded action?",
            true_when="The current evidence supports taking the proposed action.",
            false_when="The evidence is missing, contradictory, or insufficient.",
        ),
        TypedQuestion(
            prefix + "should_continue",
            "noul",
            "Should the controller continue with another bounded step after this one?",
            true_when="Another bounded step is appropriate and safe.",
            false_when="The loop should stop for completion, escalation, or owner input.",
        ),
        TypedQuestion(
            prefix + "readiness",
            "score",
            "Score the bead's readiness for the proposed next step.",
            READINESS_CHOICES,
        ),
        TypedQuestion(
            prefix + "risk",
            "score",
            "Score the risk of taking the proposed next step.",
            RISK_CHOICES,
        ),
    )
    return {question.key: question.to_payload() for question in questions}


@dataclass(frozen=True)
class JevDecision:
    """Structured answers from one v2 Jev round."""

    task_class: str
    next_bead: str | None
    next_action: ControllerAction
    delegate_target: str = "local"
    verification_level: str = "none"
    evidence_sufficient: bool | None = None
    should_continue: bool | None = True
    readiness: str = "proposed"
    risk: str = "unknown"
    confidence: float | None = None
    status: str = "ok"
    source: str = "jev"
    probabilities: dict[str, float] = field(default_factory=dict)
    error_type: str | None = None
    answer_confidences: dict[str, float] = field(default_factory=dict)

    @property
    def action(self) -> ControllerAction:
        """Compatibility alias matching the v1 ControllerDecision field."""

        return self.next_action

    @classmethod
    def unavailable(cls, error_type: str) -> "JevDecision":
        return cls(
            task_class="escalate",
            next_bead=None,
            next_action=ControllerAction.ESCALATE,
            status="unavailable",
            source="fallback",
            error_type=error_type,
        )


@dataclass(frozen=True)
class DecisionValidation:
    accepted: bool
    decision: JevDecision
    reason: str | None = None


def validate_jev_decision(
    decision: JevDecision,
    context: DecisionContext,
    *,
    min_confidence: float = 0.55,
) -> DecisionValidation:
    """Validate an answer against the current context before execution."""

    if decision.status != "ok":
        return DecisionValidation(False, decision, decision.error_type or decision.status)
    if not isinstance(decision.next_action, ControllerAction):
        return DecisionValidation(False, decision, "unknown_action")
    if decision.confidence is not None and decision.confidence < min_confidence:
        return DecisionValidation(False, decision, "low_confidence")
    if decision.next_action.value not in context.legal_actions():
        return DecisionValidation(False, decision, "illegal_action_for_phase")
    if decision.next_bead:
        available = {
            bead.bead_id
            for bead in (*context.open_beads, *context.candidate_beads)
            if bead.status not in {"closed", "complete"}
        }
        if decision.next_bead not in available:
            return DecisionValidation(False, decision, "unavailable_bead")
    if decision.delegate_target not in DELEGATE_TARGET_CHOICES:
        return DecisionValidation(False, decision, "unknown_delegate_target")
    if decision.verification_level not in VERIFICATION_CHOICES:
        return DecisionValidation(False, decision, "unknown_verification_level")
    if decision.readiness not in READINESS_CHOICES:
        return DecisionValidation(False, decision, "unknown_readiness")
    if decision.risk not in RISK_CHOICES:
        return DecisionValidation(False, decision, "unknown_risk")
    return DecisionValidation(True, decision)


def fallback_jev_decision(context: DecisionContext, reason: str) -> JevDecision:
    """Return an explicit non-executing safety fallback for bad Jev output."""

    action = (
        ControllerAction.ASK_USER
        if context.user_input_status in {"required", "waiting"}
        else ControllerAction.ESCALATE
    )
    return JevDecision(
        task_class="escalate",
        next_bead=None,
        next_action=action,
        status="fallback",
        source="fallback",
        error_type=reason,
    )


@dataclass(frozen=True)
class AdapterStepResult:
    """Result of exactly one bounded adapter action."""

    status: str
    observations: tuple[AdapterObservation, ...] = ()
    evidence: tuple[str, ...] = ()
    test_results: tuple[str, ...] = ()
    changed_paths: tuple[str, ...] = ()
    phase: ControllerPhase | None = None
    completed: bool = False
    stop_reason: str | None = None


class BoundedAdapter(Protocol):
    def run_step(self, context: DecisionContext, decision: JevDecision) -> AdapterStepResult:
        """Execute one validated action and return derived observations only."""


@dataclass(frozen=True)
class JevLoopResult:
    status: str
    context: DecisionContext
    decisions: tuple[JevDecision, ...]
    validations: tuple[DecisionValidation, ...]
    steps: int
    stop_reason: str | None = None


def phase_after_action(
    phase: ControllerPhase,
    action: ControllerAction,
    result_status: str,
) -> ControllerPhase:
    """Apply a narrow deterministic phase transition after one adapter step."""

    if result_status not in {"ok", "partial", "complete"}:
        return ControllerPhase.RECOVER
    if action is ControllerAction.FINALIZE:
        return ControllerPhase.COMPLETE
    if action in {
        ControllerAction.CLASSIFY_REQUEST,
        ControllerAction.INSPECT_REPO,
        ControllerAction.INSPECT_TASK_STATE,
        ControllerAction.INSPECT_ENV,
        ControllerAction.SEARCH_LOCAL,
        ControllerAction.READ_SOURCE,
        ControllerAction.READ_DOCS,
        ControllerAction.CHECK_HISTORY,
        ControllerAction.REPRODUCE,
        ControllerAction.BUILD_CONTEXT_PACK,
    }:
        return ControllerPhase.OBSERVE if phase is ControllerPhase.INTAKE else phase
    if action in {ControllerAction.DECOMPOSE, ControllerAction.CREATE_BEAD}:
        return ControllerPhase.PLAN
    if action in {
        ControllerAction.DELEGATE_TO_SOL,
        ControllerAction.DELEGATE_TO_SPECIALIST,
        ControllerAction.WAIT_FOR_WORK,
        ControllerAction.RESUME_WORK,
    }:
        return ControllerPhase.DELEGATE
    if action in {ControllerAction.APPLY_PATCH, ControllerAction.WRITE_FILE}:
        return ControllerPhase.VERIFY
    if action in {
        ControllerAction.RUN_TARGETED_TESTS,
        ControllerAction.RUN_BROAD_TESTS,
        ControllerAction.RUN_CONTRACT_CHECK,
        ControllerAction.CHECK_GIT_DIFF,
        ControllerAction.REVIEW_RESULT,
        ControllerAction.UPDATE_BEAD,
        ControllerAction.CLOSE_BEAD,
    }:
        return ControllerPhase.VERIFY
    if action in {ControllerAction.RETRY_TRANSIENT_FAILURE, ControllerAction.RECOVER_AFTER_FAILURE}:
        return ControllerPhase.RECOVER
    if action is ControllerAction.UPDATE_USER:
        return ControllerPhase.COMMUNICATE
    return phase


class JevDecisionLoop:
    """Repeated Jev -> validation -> one bounded adapter step controller."""

    def __init__(
        self,
        controller: Any,
        adapter: BoundedAdapter,
        *,
        max_steps: int = 8,
        min_confidence: float = 0.55,
    ) -> None:
        if max_steps <= 0:
            raise ValueError("max_steps must be positive")
        self.controller = controller
        self.adapter = adapter
        self.max_steps = max_steps
        self.min_confidence = min_confidence

    def run(self, context: DecisionContext) -> JevLoopResult:
        decisions: list[JevDecision] = []
        validations: list[DecisionValidation] = []
        for step in range(self.max_steps):
            decision = self.controller.decide_context(context)
            decisions.append(decision)
            validation = validate_jev_decision(
                decision, context, min_confidence=self.min_confidence
            )
            validations.append(validation)
            if not validation.accepted:
                fallback = fallback_jev_decision(context, validation.reason or "invalid_decision")
                decisions[-1] = fallback
                context.add_evidence(f"jev_fallback:{validation.reason or 'invalid_decision'}")
                return JevLoopResult(
                    "fallback",
                    context,
                    tuple(decisions),
                    tuple(validations),
                    step,
                    validation.reason,
                )

            if validation.decision.next_action in {
                ControllerAction.FINALIZE,
                ControllerAction.ESCALATE,
                ControllerAction.ASK_USER,
            }:
                return JevLoopResult(
                    "stopped",
                    context,
                    tuple(decisions),
                    tuple(validations),
                    step,
                    validation.decision.next_action.value,
                )

            result = self.adapter.run_step(context, validation.decision)
            for observation in result.observations:
                context.record_observation(observation)
            context.add_evidence(*result.evidence)
            context.test_results += tuple(result.test_results)
            context.changed_paths += tuple(
                path for path in result.changed_paths if path not in context.changed_paths
            )
            context.set_phase(
                result.phase
                or phase_after_action(
                    context.phase, validation.decision.next_action, result.status
                )
            )
            if result.status not in {"ok", "partial", "complete"}:
                context.retry_count += 1
            if result.completed or result.stop_reason:
                return JevLoopResult(
                    "complete" if result.completed else "stopped",
                    context,
                    tuple(decisions),
                    tuple(validations),
                    step + 1,
                    result.stop_reason,
                )
            if validation.decision.next_action in {
                ControllerAction.FINALIZE,
                ControllerAction.ESCALATE,
                ControllerAction.ASK_USER,
            }:
                return JevLoopResult(
                    "stopped",
                    context,
                    tuple(decisions),
                    tuple(validations),
                    step + 1,
                    validation.decision.next_action.value,
                )
            if validation.decision.should_continue is False:
                return JevLoopResult(
                    "stopped",
                    context,
                    tuple(decisions),
                    tuple(validations),
                    step + 1,
                    "jev_should_continue_false",
                )
        return JevLoopResult(
            "budget_exhausted",
            context,
            tuple(decisions),
            tuple(validations),
            self.max_steps,
            "max_steps",
        )


def build_initial_state(
    task_hash: str,
    *,
    ask_present: bool = True,
    ask_shifted: bool = False,
) -> ControllerState:
    """Create the compact intake state used for a replay pilot.

    `ask_present` records whether the replay actually yielded an owner ask once
    harness context blocks are stripped. Jev must not be told a request was
    received when the extracted turn contained only `<recommended_plugins>` /
    `<environment_context>` boilerplate.
    """

    facts = ["prior_codex_task_selected", "isolated_replay_workspace_available"]
    facts.insert(0, "user_request_received" if ask_present else "user_request_missing")
    if ask_shifted:
        facts.append("first_turn_was_harness_context_only")
    constraints = [
        "look_before_write",
        "verify_after_change",
        "do_not_print_prompt_or_secret_values",
    ]
    if not ask_present:
        constraints.append("do_not_infer_the_task_from_boilerplate")
    return ControllerState(
        task_hash=task_hash,
        phase=ControllerPhase.INTAKE,
        intent_class="existing_codex_work_replay",
        observed_facts=tuple(facts),
        recent_event_kinds=("task_started",),
        constraints=tuple(constraints),
        user_input_required=not ask_present,
    )


class JevController:
    """Small synchronous Jev client with no tool or filesystem authority."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.api_key = (
            os.environ.get("OPENROUTER_API_KEY", "") if api_key is None else api_key
        )
        configured_url = base_url or os.environ.get(
            "OPENROUTER_API_URL", "https://openrouter.ai/api/v1"
        )
        self.base_url = self._openrouter_decisions_url(configured_url)
        self.model = model or os.environ.get("JEV_OPENROUTER_MODEL", "typesafe/jev-1.13")
        self.timeout = timeout
        if "jev" not in self.model.lower() or "typesafe" not in self.model.lower():
            raise ValueError("JevController only permits a Typesafe Jev model")

    def decide(self, state: ControllerState) -> ControllerDecision:
        if not self.api_key:
            return self._unavailable("missing_api_key")
        request = self._request_payload(state)
        try:
            body = json.dumps(request, separators=(",", ":")).encode("utf-8")
            req = urllib.request.Request(
                self.base_url,
                data=body,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/harness-on-steroids",
                    "X-OpenRouter-Title": "harness-on-steroids Jev controller",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
            return self._parse_decision(payload, state.phase)
        except urllib.error.HTTPError as exc:
            return self._unavailable(f"http_{exc.code}")
        except (urllib.error.URLError, TimeoutError, OSError):
            return self._unavailable("provider_error")
        except (json.JSONDecodeError, TypeError, ValueError):
            return self._unavailable("parse_error")

    def decide_context(self, context: DecisionContext) -> JevDecision:
        """Ask the typed v2 question set for the next bounded decision."""

        if not self.api_key:
            return JevDecision.unavailable("missing_api_key")
        request = self._context_request_payload(context)
        try:
            body = json.dumps(request, separators=(",", ":")).encode("utf-8")
            req = urllib.request.Request(
                self.base_url,
                data=body,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/harness-on-steroids",
                    "X-OpenRouter-Title": "harness-on-steroids Jev controller v2",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
            return self._parse_jev_decision(payload)
        except urllib.error.HTTPError as exc:
            return JevDecision.unavailable(f"http_{exc.code}")
        except (urllib.error.URLError, TimeoutError, OSError):
            return JevDecision.unavailable("provider_error")
        except (json.JSONDecodeError, TypeError, ValueError, KeyError):
            return JevDecision.unavailable("parse_error")

    def _request_payload(self, state: ControllerState) -> dict[str, Any]:
        return {
            "model": self.model,
            "state": {
                "description": "One non-sensitive harness routing state.",
                "records": [
                    {
                        "id": state.task_hash,
                        "record": state.to_payload(),
                    }
                ],
            },
            "questions": {
                f"{state.task_hash}__next_action": {
                    "type": "choice",
                    "instructions": (
                        "Choose exactly one safest next harness action. Return one action label."
                    ),
                    "criteria": ACTION_DESCRIPTIONS,
                }
            },
        }

    def _context_request_payload(self, context: DecisionContext) -> dict[str, Any]:
        return {
            "model": self.model,
            "state": {
                "description": (
                    "The complete relevant, non-sensitive decision context for one "
                    "bounded harness step."
                ),
                "records": [
                    {
                        "id": context.task_hash,
                        "record": context.to_payload(),
                    }
                ],
            },
            "questions": build_typed_questions(context),
        }

    @staticmethod
    def _openrouter_decisions_url(configured_url: str) -> str:
        parts = urlsplit(configured_url)
        if parts.scheme != "https" or parts.hostname != "openrouter.ai":
            raise ValueError("JevController only permits the OpenRouter HTTPS API")
        return "https://openrouter.ai/api/alpha/decisions"

    @staticmethod
    def _nested_values(payload: Mapping[str, Any]) -> list[Mapping[str, Any]]:
        values = [payload]
        for key in ("result", "data", "output", "response", "answer", "answers", "next_action"):
            value = payload.get(key)
            if isinstance(value, Mapping):
                values.extend(JevController._nested_values(value))
        return values

    @classmethod
    def _find_first(cls, payload: Mapping[str, Any], keys: Sequence[str]) -> Any:
        for candidate in cls._nested_values(payload):
            for key in keys:
                if key in candidate:
                    return candidate[key]
        return None

    @classmethod
    def _parse_decision(
        cls, payload: Mapping[str, Any], phase: ControllerPhase
    ) -> ControllerDecision:
        answers = payload.get("answers")
        answer_payload: Mapping[str, Any] = payload
        if isinstance(answers, Mapping):
            answer_payload = next(
                (value for value in answers.values() if isinstance(value, Mapping)), answers
            )
        raw_action = cls._find_first(
            answer_payload, ("choice", "action", "label", "class", "value")
        )
        action_text = str(raw_action).strip().upper().replace("-", "_").replace(" ", "_")
        if action_text not in ACTION_DESCRIPTIONS:
            raise ValueError("jev_unknown_action")
        raw_probs = cls._find_first(
            answer_payload, ("probabilities", "probability_map", "probs")
        )
        probabilities: dict[str, float] = {}
        if isinstance(raw_probs, Mapping):
            for key, value in raw_probs.items():
                label = str(key).strip().upper().replace("-", "_").replace(" ", "_")
                if label in ACTION_DESCRIPTIONS:
                    probabilities[label] = float(value)
            total = sum(probabilities.values())
            if total > 0 and math.isfinite(total):
                probabilities = {key: value / total for key, value in probabilities.items()}
        confidence = probabilities.get(action_text)
        return ControllerDecision(
            action=ControllerAction(action_text),
            phase=phase,
            confidence=confidence,
            status="ok",
            probabilities=probabilities,
        )

    @classmethod
    def _parse_jev_decision(cls, payload: Mapping[str, Any]) -> JevDecision:
        answers = payload.get("answers")
        answer_values: Mapping[str, Any] = answers if isinstance(answers, Mapping) else payload

        def answer(field: str) -> Any:
            suffix = f"__{field}"
            for key, value in answer_values.items():
                if str(key) == field or str(key).endswith(suffix):
                    return value
            return None

        def raw(value: Any, *keys: str) -> Any:
            if isinstance(value, Mapping):
                for key in keys:
                    if key in value:
                        return value[key]
            return value

        def text(field: str, default: str) -> str:
            value = raw(answer(field), "choice", "score", "value", "label", "class")
            return str(value).strip() if value is not None else default

        def normalized(field: str, default: str) -> str:
            return text(field, default).lower().replace("-", "_").replace(" ", "_")

        def score_label(field: str, default: str) -> str:
            value = answer(field)
            if isinstance(value, Mapping):
                legend = value.get("legend")
                score = value.get("score")
                if isinstance(legend, Mapping) and isinstance(score, (int, float)):
                    nearest = str(round(float(score)))
                    label = legend.get(nearest)
                    if label is not None:
                        return str(label).strip().lower().replace("-", "_").replace(" ", "_")
            return normalized(field, default)

        def boolean(field: str) -> bool | None:
            value = raw(answer(field), "value", "probability", "prob", "noul", "score")
            if isinstance(value, bool):
                return value
            if isinstance(value, (int, float)):
                return float(value) >= 0.5
            if isinstance(value, str):
                lowered = value.strip().lower()
                if lowered in {"true", "yes", "1", "y"}:
                    return True
                if lowered in {"false", "no", "0", "n"}:
                    return False
            return None

        confidences: dict[str, float] = {}
        for field_name in (
            "task_class",
            "next_bead",
            "next_action",
            "delegate_target",
            "verification_level",
            "evidence_sufficient",
            "should_continue",
            "readiness",
            "risk",
        ):
            value = answer(field_name)
            confidence = raw(value, "confidence", "probability_of_choice", "prob")
            if isinstance(confidence, (int, float)) and math.isfinite(float(confidence)):
                confidences[field_name] = float(confidence)
        overall = raw(payload, "confidence")
        if not isinstance(overall, (int, float)):
            # The selected action is the executable choice. Score/Noul
            # confidence is retained per answer but does not make an otherwise
            # legal action unusable merely because the rubric is uncertain.
            overall = confidences.get("next_action")
        if overall is not None:
            overall = float(overall)

        action_text = normalized("next_action", "ESCALATE").upper()
        try:
            action = ControllerAction(action_text)
        except ValueError as exc:
            raise ValueError("jev_unknown_action") from exc
        bead_text = text("next_bead", "NONE")
        bead: str | None = (
            None
            if bead_text.upper() in {"NONE", "NO_BEAD", "NULL", ""}
            else bead_text
        )
        action_probabilities: dict[str, float] = {}
        raw_action_probabilities = raw(answer("next_action"), "probabilities", "probs")
        if isinstance(raw_action_probabilities, Mapping):
            for key, value in raw_action_probabilities.items():
                if isinstance(value, (int, float)) and math.isfinite(float(value)):
                    action_probabilities[
                        str(key).strip().upper().replace("-", "_").replace(" ", "_")
                    ] = float(value)
        return JevDecision(
            task_class=normalized("task_class", "escalate"),
            next_bead=bead,
            next_action=action,
            delegate_target=normalized("delegate_target", "local"),
            verification_level=normalized("verification_level", "none"),
            evidence_sufficient=boolean("evidence_sufficient"),
            should_continue=boolean("should_continue"),
            readiness=score_label("readiness", "proposed"),
            risk=score_label("risk", "unknown"),
            confidence=overall,
            probabilities=action_probabilities,
            answer_confidences=confidences,
        )

    @staticmethod
    def _unavailable(error_type: str) -> ControllerDecision:
        return ControllerDecision(
            action=ControllerAction.ESCALATE,
            phase=ControllerPhase.INTAKE,
            confidence=None,
            status="unavailable",
            error_type=error_type,
        )


def controller_directive(decision: ControllerDecision) -> str:
    """Turn a Jev proposal into a bounded prompt hint without granting authority."""

    if decision.status != "ok":
        return (
            "Controller unavailable; follow the repository instructions and inspect before acting."
        )
    return (
        f"Controller proposal: {decision.action.value}. Treat this as a routing hint only. "
        "Use repository instructions and your own evidence to confirm legality, "
        "then continue through verification."
    )


__all__ = [
    "ACTION_DESCRIPTIONS",
    "LEGAL_ACTIONS_BY_PHASE",
    "AdapterObservation",
    "AdapterStepResult",
    "BoundedAdapter",
    "CandidateBead",
    "ControllerAction",
    "ControllerDecision",
    "ControllerPhase",
    "ControllerState",
    "DecisionBead",
    "DecisionContext",
    "DecisionValidation",
    "JevController",
    "JevDecision",
    "JevDecisionLoop",
    "JevLoopResult",
    "RISK_CHOICES",
    "READINESS_CHOICES",
    "TASK_CLASS_CHOICES",
    "VERIFICATION_CHOICES",
    "build_initial_state",
    "build_typed_questions",
    "controller_directive",
    "fallback_jev_decision",
    "phase_after_action",
    "validate_jev_decision",
]

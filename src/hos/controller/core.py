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
from typing import Any, Mapping, Sequence
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
    "ControllerAction",
    "ControllerDecision",
    "ControllerPhase",
    "ControllerState",
    "JevController",
    "build_initial_state",
    "controller_directive",
]

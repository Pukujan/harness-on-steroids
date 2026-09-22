"""Versioned, body-minimized evidence contract for transcript analysis."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Mapping

CONTRACT_VERSION = "analysis-event/0.1.0"
ONTOLOGY_VERSION = "analysis-ontology/0.1.0"
CODEBOOK_VERSION = "analysis-codebook/0.1.0"

LANES = frozenset({"codex", "chatgpt_chat", "unknown"})
OBSERVATION_STATES = frozenset(
    {
        "observed",
        "inferred",
        "user_provided",
        "externally_sourced",
        "not_observed",
        "unknown",
        "not_applicable",
    }
)
BODY_STATES = frozenset(
    {"not_retained", "redacted", "available_local", "unknown", "not_applicable"}
)


def stable_id(*parts: object, length: int = 24) -> str:
    """Return a stable non-reversible identifier for a tuple of local keys."""

    encoded = json.dumps(parts, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()[:length]


Scalar = str | int | float | bool | None


@dataclass(frozen=True, slots=True)
class CanonicalEvent:
    """A normalized observable event with no transcript body."""

    event_id: str
    source_id: str
    episode_id: str
    lane: str
    ordinal: int
    kind: str
    actor: str
    timestamp: str | None = None
    subtype: str | None = None
    tool_name: str | None = None
    tool_family: str | None = None
    status: str | None = None
    observation: str = "unknown"
    source_pointer: str = ""
    source_record_id: str = ""
    body_status: str = "not_retained"
    analysis_run_id: str | None = None
    parent_event_id: str | None = None
    supersedes_event_id: str | None = None
    attributes: Mapping[str, Scalar] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize in a stable key order without exposing content bodies."""

        return {
            "contract_version": CONTRACT_VERSION,
            "event_id": self.event_id,
            "source_id": self.source_id,
            "episode_id": self.episode_id,
            "lane": self.lane,
            "ordinal": self.ordinal,
            "kind": self.kind,
            "actor": self.actor,
            "timestamp": self.timestamp,
            "subtype": self.subtype,
            "tool_name": self.tool_name,
            "tool_family": self.tool_family,
            "status": self.status,
            "observation": self.observation,
            "source_pointer": self.source_pointer,
            "source_record_id": self.source_record_id,
            "body_status": self.body_status,
            "analysis_run_id": self.analysis_run_id,
            "parent_event_id": self.parent_event_id,
            "supersedes_event_id": self.supersedes_event_id,
            "attributes": dict(sorted(self.attributes.items())),
        }


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """A deterministic validation finding; never contains a source body."""

    code: str
    field: str
    message: str
    event_id: str | None = None


def event_sort_key(event: CanonicalEvent) -> tuple[str, int, str]:
    """Use explicit episode/ordinal/id tie-breaking instead of filesystem order."""

    return (event.episode_id, event.ordinal, event.event_id)

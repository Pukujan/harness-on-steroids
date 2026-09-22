"""Contract validation for normalized events and exported summaries."""

from __future__ import annotations

from collections.abc import Iterable

from .model import LANES, OBSERVATION_STATES, CanonicalEvent, ValidationIssue


def validate_event(event: CanonicalEvent) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if not event.event_id:
        issues.append(ValidationIssue("missing_id", "event_id", "event_id is required"))
    if not event.source_id:
        issues.append(
            ValidationIssue("missing_source", "source_id", "source_id is required", event.event_id)
        )
    if not event.episode_id:
        issues.append(
            ValidationIssue(
                "missing_episode", "episode_id", "episode_id is required", event.event_id
            )
        )
    if event.lane not in LANES:
        issues.append(
            ValidationIssue("invalid_lane", "lane", "lane is not in the contract", event.event_id)
        )
    if event.ordinal < 0:
        issues.append(
            ValidationIssue(
                "negative_ordinal", "ordinal", "ordinal must be non-negative", event.event_id
            )
        )
    if not event.kind:
        issues.append(ValidationIssue("missing_kind", "kind", "kind is required", event.event_id))
    if event.observation not in OBSERVATION_STATES:
        issues.append(
            ValidationIssue(
                "invalid_observation",
                "observation",
                "observation is not in the contract",
                event.event_id,
            )
        )
    if event.kind == "tool_call" and not event.tool_name:
        issues.append(
            ValidationIssue(
                "missing_tool_name", "tool_name", "tool events need a tool name", event.event_id
            )
        )
    return issues


def validate_events(events: Iterable[CanonicalEvent]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    seen: set[str] = set()
    for event in events:
        issues.extend(validate_event(event))
        if event.event_id in seen:
            issues.append(
                ValidationIssue(
                    "duplicate_event_id", "event_id", "event_id is duplicated", event.event_id
                )
            )
        seen.add(event.event_id)
    return issues

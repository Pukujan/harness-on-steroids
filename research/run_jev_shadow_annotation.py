"""Probe Jev as a bounded, body-free structural annotator.

This is a research runner, not a replacement for the deterministic analysis
machine. It sends a small deterministic sample of canonical events to Jev as
independent Noul questions, compares only against labels defined directly by
canonical fields, and writes hash-only local results.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data/derived/analysis-machine/ontology-pilot-20260922-v3/pilot-events.jsonl"
DEFAULT_OUTPUT = ROOT / "data/derived/analysis-machine/jev-shadow-annotation-20260922-v1"
DEFAULT_MODEL = "typesafe/jev-1.13"

LABELS = (
    "inspection_action",
    "mutation_action",
    "verification_action",
    "research_observed",
    "citation_event_present",
    "code_event",
    "execution_output_event",
    "unclassified_event_present",
)


def _load_env(path: Path) -> None:
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        if key in {"OPENROUTER_API_KEY", "OPENROUTER_API_URL", "JEV_OPENROUTER_MODEL"}:
            os.environ.setdefault(key, value.strip().strip("\"").strip("'"))


def _event_features(event: dict[str, Any]) -> dict[str, Any]:
    attributes = event.get("attributes")
    if not isinstance(attributes, dict):
        attributes = {}
    return {
        "lane": event.get("lane"),
        "kind": event.get("kind"),
        "actor": event.get("actor"),
        "tool_family": event.get("tool_family"),
        "tool_name": event.get("tool_name"),
        "observation": event.get("observation"),
        "status": event.get("status"),
        "subtype": event.get("subtype"),
        "content_type": attributes.get("content_type"),
        "has_citation": attributes.get("has_citation"),
    }


def expected_labels(event: dict[str, Any]) -> dict[str, bool]:
    kind = event.get("kind")
    family = event.get("tool_family")
    attributes = event.get("attributes")
    if not isinstance(attributes, dict):
        attributes = {}
    return {
        "inspection_action": kind == "tool_call" and family == "inspect",
        "mutation_action": kind == "tool_call" and family == "mutate",
        "verification_action": kind == "tool_call" and family == "verify",
        "research_observed": kind == "research" or family == "research",
        "citation_event_present": kind == "citation",
        "code_event": attributes.get("content_type") == "code",
        "execution_output_event": attributes.get("content_type") == "execution_output",
        "unclassified_event_present": kind == "unknown",
    }


def _coverage(event: dict[str, Any]) -> set[tuple[str, bool]]:
    return {(label, value) for label, value in expected_labels(event).items()}


def select_events(rows: Iterable[dict[str, Any]], max_events: int) -> list[dict[str, Any]]:
    """Select a deterministic sample covering predicates, then fill the budget."""

    if max_events <= 0:
        raise ValueError("max_events must be positive")
    candidates = sorted(rows, key=lambda row: str(row["event"].get("event_id", "")))
    target = {(label, value) for label in LABELS for value in (False, True)}
    selected: list[dict[str, Any]] = []
    remaining = list(candidates)
    covered: set[tuple[str, bool]] = set()
    while remaining and len(selected) < max_events and covered != target:
        choice = max(
            remaining,
            key=lambda row: (
                len(_coverage(row["event"]) - covered),
                str(row["event"].get("event_id", "")),
            ),
        )
        remaining.remove(choice)
        selected.append(choice)
        covered.update(_coverage(choice["event"]))
    # Coverage is a minimum requirement, not a reason to silently ignore a
    # caller's larger sample budget.  The remaining candidates are already in
    # stable event-id order, so filling from the front preserves repeatability.
    while remaining and len(selected) < max_events:
        selected.append(remaining.pop(0))
    return selected


def _questions() -> dict[str, dict[str, Any]]:
    descriptions = {
        "inspection_action": "The event is an observed inspect-family action request.",
        "mutation_action": "The event is an observed mutate-family action request.",
        "verification_action": "The event is an observed verify-family action request.",
        "research_observed": "The event is an explicit research or source-retrieval event.",
        "citation_event_present": "The event is a normalized citation event.",
        "code_event": "The canonical content_type attribute is exactly code.",
        "execution_output_event": (
            "The canonical content_type attribute is exactly execution_output."
        ),
        "unclassified_event_present": "The canonical event kind is unknown.",
    }
    return {
        f"shadow__{label}": {
            "type": "noul",
            "instructions": (
                "Is this predicate true for the supplied canonical event? "
                f"{description}"
            ),
            "true_when": description,
            "false_when": "The supplied canonical event does not satisfy the predicate.",
        }
        for label, description in descriptions.items()
    }


def _decisions_url(configured: str) -> str:
    if not configured.startswith("https://openrouter.ai/"):
        raise ValueError("shadow runner only permits the OpenRouter HTTPS API")
    return "https://openrouter.ai/api/alpha/decisions"


def _parse_probability(value: Any) -> float | None:
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if isinstance(value, (int, float)) and math.isfinite(float(value)):
        number = float(value)
        if 0.0 <= number <= 1.0:
            return number
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "1"}:
            return 1.0
        if lowered in {"false", "no", "0"}:
            return 0.0
    return None


def parse_answers(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    answers = payload.get("answers")
    if not isinstance(answers, dict):
        raise ValueError("jev response has no answers object")
    parsed: dict[str, dict[str, Any]] = {}
    for label in LABELS:
        key = f"shadow__{label}"
        raw = answers.get(key)
        if not isinstance(raw, dict):
            parsed[label] = {"probability": None, "confidence": None, "valid": False}
            continue
        probability = None
        for candidate in ("noul", "probability", "prob", "value", "score"):
            if candidate in raw:
                probability = _parse_probability(raw[candidate])
                if probability is not None:
                    break
        confidence = _parse_probability(raw.get("confidence"))
        parsed[label] = {
            "probability": probability,
            "confidence": confidence,
            "valid": probability is not None,
        }
    return parsed


def _request(
    event: dict[str, Any], *, api_key: str, model: str, timeout: float
) -> tuple[str, dict[str, Any] | None]:
    event_id = str(event["event"].get("event_id", ""))
    payload = {
        "model": model,
        "state": {
            "description": (
                "One canonical body-free transcript event. Classify only the supplied "
                "structural fields; do not infer omitted body content."
            ),
            "records": [
                {
                    "id": event_id,
                    "record": {
                        "event": _event_features(event["event"]),
                        "body_policy": "not_retained",
                    },
                }
            ],
        },
        "questions": _questions(),
    }
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    request = urllib.request.Request(
        _decisions_url(os.environ.get("OPENROUTER_API_URL", "https://openrouter.ai/api/v1")),
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/harness-on-steroids",
            "X-OpenRouter-Title": "harness-on-steroids Jev shadow annotation",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return "ok", json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return f"http_{exc.code}", None
    except (urllib.error.URLError, TimeoutError, OSError):
        return "provider_error", None
    except (json.JSONDecodeError, TypeError, ValueError):
        return "parse_error", None


def run(
    input_path: Path, output_dir: Path, *, max_events: int, timeout: float
) -> dict[str, Any]:
    _load_env(ROOT / ".env")
    rows = [
        json.loads(line)
        for line in input_path.read_text(encoding="utf-8").splitlines()
        if line
    ]
    selected = select_events(rows, max_events)
    input_fingerprint = hashlib.sha256(
        json.dumps(
            [_event_features(row["event"]) for row in selected],
            ensure_ascii=False,
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()
    output_dir.mkdir(parents=True, exist_ok=True)
    result_path = output_dir / "results.jsonl"
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    model = os.environ.get("JEV_OPENROUTER_MODEL", DEFAULT_MODEL)
    rows_out: list[dict[str, Any]] = []
    counts = {"questions": 0, "valid": 0, "correct": 0}
    for row in selected:
        event = row["event"]
        expected = expected_labels(event)
        if not api_key:
            status, parsed = "missing_api_key", None
        else:
            status, payload = _request(event=row, api_key=api_key, model=model, timeout=timeout)
            parsed = parse_answers(payload) if payload is not None else None
        labels: dict[str, Any] = {}
        for label in LABELS:
            default_answer: dict[str, Any] = {
                "probability": None,
                "confidence": None,
                "valid": False,
            }
            answer = (
                dict(parsed.get(label) or default_answer)
                if parsed is not None
                else default_answer
            )
            probability = answer["probability"]
            predicted = probability >= 0.5 if isinstance(probability, float) else None
            correct = predicted == expected[label] if predicted is not None else None
            labels[label] = {
                "expected": expected[label],
                "predicted": predicted,
                "probability_true": probability,
                "confidence": answer["confidence"],
                "correct": correct,
                "valid": answer["valid"],
            }
            counts["questions"] += 1
            counts["valid"] += int(answer["valid"])
            counts["correct"] += int(correct is True)
        rows_out.append(
            {
                "event_id": event.get("event_id"),
                "episode_id": event.get("episode_id"),
                "lane": event.get("lane"),
                "status": status,
                "labels": labels,
            }
        )
    with result_path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows_out:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    manifest = {
        "schema": "jev-shadow-annotation/0.1.0",
        "model": model,
        "input": str(input_path),
        "input_fingerprint": input_fingerprint,
        "selected_events": len(selected),
        "labels_per_event": len(LABELS),
        "timeout_seconds": timeout,
        "counts": counts,
        "body_policy": "body-free canonical event features only; no raw response is written",
        "created_at_epoch": int(time.time()),
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(prog="run-jev-shadow-annotation")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--max-events", type=int, default=16)
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args()
    print(
        json.dumps(
            run(args.input, args.output, max_events=args.max_events, timeout=args.timeout),
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

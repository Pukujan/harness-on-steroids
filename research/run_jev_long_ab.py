#!/usr/bin/env python3
"""Run the frozen long-horizon Jev A/B experiment.

Arm A and arm B use the same Work-derived user-turn fixtures, isolated
repository snapshot, deterministic context feeder, adapter, model, and
timeouts. Arm B adds only one validated Jev decision before each bounded
harness invocation. Raw prompts and events remain below ignored
``.controller-runs``; committed output is hash-only.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import shutil
import statistics
import subprocess
import sys
import tarfile
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from research.replay_lib import REPLAY, ask_turns, develop_hashes, outcome_label  # noqa: E402
from src.hos.controller import (  # noqa: E402
    AdapterObservation,
    ControllerAction,
    DecisionContext,
    DecisionValidation,
    GrokBuildAdapter,
    HarnessAdapter,
    JevController,
    JevDecision,
    OpenCodeAdapter,
    PiAdapter,
    RepositoryContextFeeder,
    phase_after_action,
    validate_jev_decision,
)
from src.hos.controller.adapters import (  # noqa: E402
    HARNESS_MAX_RUNTIME_SECONDS,
    HARNESS_INACTIVITY_TIMEOUT_SECONDS,
    extract_session_id,
    extract_tool_seq,
)
from src.score_session import score_seq  # noqa: E402

ENV_KEYS = {
    "OPENROUTER_API_KEY",
    "OPENROUTER_API_URL",
    "JEV_OPENROUTER_MODEL",
    "OPENCODE_MODEL",
    "GROK_BUILD_MODEL",
    "PI_MODEL",
    "GROK_BUILD_MAX_TURNS",
    "QWEN_API_URL",
    "QWEN_API_KEY",
}


@dataclass(frozen=True)
class ReplayTurn:
    task_hash: str
    turn_index: int
    task_turn_count: int
    ask: str


@dataclass
class ArmTaskResult:
    task_hash: str
    adapter: HarnessAdapter
    mode: str
    workspace: Path
    rows: list[dict[str, Any]]
    tool_seq: list[str]
    decisions: list[JevDecision]
    validation_reasons: list[str]
    session_ids: list[str]
    context_pack_digests: list[str]
    statuses: list[str]


def _should_run_advisory_baseline(
    validation: DecisionValidation | None, *, enabled: bool
) -> bool:
    """Return whether a low-confidence answer should remain advisory only."""

    return bool(
        enabled
        and validation is not None
        and not validation.accepted
        and validation.reason == "low_confidence"
    )


def _load_env(path: Path) -> None:
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        if key.strip() in ENV_KEYS:
            os.environ[key.strip()] = value.strip().strip('"').strip("'")


def _adapter(name: str) -> HarnessAdapter:
    if name == "opencode":
        return OpenCodeAdapter()
    if name == "grok-build":
        return GrokBuildAdapter()
    if name == "pi":
        return PiAdapter()
    raise ValueError(f"unknown adapter: {name}")


def _scoreable_tool_seq(seq: Sequence[str]) -> list[str]:
    aliases = {
        "apply_patch": "edit",
        "edit_file": "edit",
        "write_file": "write",
        "patch": "patch",
        "shell": "bash",
        "terminal": "bash",
        "exec": "bash",
        "run_command": "bash",
        "todo": "todowrite",
        "todo_write": "todowrite",
        "spawn_agent": "task",
        "delegate": "task",
    }
    return [aliases.get(tool, tool) for tool in seq]


def _status_for_context(status: str) -> str:
    if status == "ok":
        return "ok"
    if status == "partial":
        return "partial"
    return "failed"


def _fixture_turns(task_hashes: Sequence[str], limit: int) -> list[ReplayTurn]:
    """Allocate at least three turns per development task, then fill in order."""

    if limit <= 0:
        raise ValueError("turn limit must be positive")
    all_turns: dict[str, list[str]] = {
        task_hash: ask_turns(REPLAY / task_hash / "user.md") for task_hash in task_hashes
    }
    available = sum(len(turns) for turns in all_turns.values())
    if available < limit:
        raise ValueError(f"only {available} usable Work turns available; need {limit}")
    selected: list[ReplayTurn] = []
    for task_hash in task_hashes:
        turns = all_turns[task_hash]
        for index, ask in enumerate(turns[:3], start=1):
            selected.append(ReplayTurn(task_hash, index, len(turns), ask))
    if len(selected) > limit:
        raise ValueError("turn limit must leave at least three turns per task")
    next_index = {task_hash: 3 for task_hash in task_hashes}
    while len(selected) < limit:
        added = False
        for task_hash in task_hashes:
            turns = all_turns[task_hash]
            index = next_index[task_hash]
            if index < len(turns):
                selected.append(ReplayTurn(task_hash, index + 1, len(turns), turns[index]))
                next_index[task_hash] += 1
                added = True
                if len(selected) == limit:
                    break
        if not added:
            raise ValueError("could not fill the requested turn budget")
    return selected


def _materialize_seed(seed: Path) -> None:
    seed.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["git", "archive", "--format=tar", "HEAD"],
        cwd=ROOT,
        capture_output=True,
        timeout=60,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError("workspace_seed_failed")
    seed.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(result.stdout), mode="r:") as archive:
        try:
            archive.extractall(seed, filter="data")
        except TypeError:  # Python 3.11 has no tarfile filter argument.
            archive.extractall(seed)
    commands = (
        ["git", "init", "--quiet", "--initial-branch=main"],
        ["git", "config", "user.email", "fixture@example.invalid"],
        ["git", "config", "user.name", "Fixture Workspace"],
        ["git", "add", "-A"],
        ["git", "commit", "--quiet", "-m", "fixture snapshot"],
    )
    for command in commands:
        initialized = subprocess.run(
            command,
            cwd=seed,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=180,
            check=False,
        )
        if initialized.returncode != 0:
            raise RuntimeError("workspace_seed_init_failed")


def _clone_workspace(destination: Path, seed: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(seed, destination)


def _new_context(
    task_hash: str, first_ask: str, turn_budget: int, *, timeout_budget_s: float
) -> DecisionContext:
    return DecisionContext.from_ask(
        task_hash,
        first_ask,
        constraints=(
            "look_before_write",
            "verify_after_change",
            "do_not_print_prompt_or_secret_values",
            "bounded_action_per_replay_turn",
        ),
        timeout_budget_s=timeout_budget_s,
        turn_budget=turn_budget,
    )


def _context_prompt(context: DecisionContext, current_ask: str) -> str:
    payload = json.dumps(context.to_payload(max_chars=14_000), ensure_ascii=False, indent=2)
    return (
        "You are continuing one bounded turn of a long-running coding task. Follow the "
        "repository instructions and inspect before writes. Use the current owner turn "
        "as the immediate request, while preserving the accumulated context. Verify any "
        "material change before stopping.\n\n"
        f"Current owner turn:\n{current_ask}\n\n"
        "Shared derived context pack (facts and summaries, not raw event bodies):\n"
        f"{payload}\n\n"
        "Work only on this current turn. Leave observable evidence for the next turn."
    )


def _jev_prompt(context: DecisionContext, decision: JevDecision, current_ask: str) -> str:
    payload = json.dumps(context.to_payload(max_chars=14_000), ensure_ascii=False, indent=2)
    return (
        "You are continuing one bounded turn of a long-running coding task. A separate "
        "typed controller selected the action below from the supplied live context. "
        "The controller has no tools or filesystem authority. Follow repository "
        "instructions, inspect before writes, and verify material changes.\n\n"
        f"Current owner turn:\n{current_ask}\n\n"
        f"Validated controller action: {decision.next_action.value}\n"
        f"Validated controller bead: {decision.next_bead or 'NONE'}\n\n"
        "Decision context:\n"
        f"{payload}\n\n"
        "Perform only this bounded step and leave concise observable evidence for the "
        "next context-feeder update."
    )


def _fold_run(
    context: DecisionContext,
    adapter: HarnessAdapter,
    run: Any,
    tool_seq: list[str],
    session_ids: list[str],
) -> list[str]:
    events = adapter.stream_events(run.events_path)
    tools = extract_tool_seq(run.events_path)
    tool_seq.extend(tools)
    session_id = extract_session_id(run.events_path)
    if session_id and session_id not in session_ids:
        session_ids.append(session_id)
    for event in events[-40:]:
        context.record_observation(
            AdapterObservation(
                event_kind=event.event_kind,
                tool_name=event.tool_name,
                status=event.status,
                summary=event.summary,
            )
        )
    failed = run.status not in {"ok", "partial"}
    context.record_observation(
        AdapterObservation(
            event_kind="harness_run",
            status=run.status,
            summary=f"{len(events)} normalized events; {len(tools)} tool observations",
            failure=run.status if failed else None,
        )
    )
    context.add_evidence(f"adapter_status:{run.status}")
    return tools


def _turn_row(
    *,
    turn: ReplayTurn,
    mode: str,
    run: Any | None,
    decision: JevDecision | None,
    validation: DecisionValidation | None,
    context_digest: str,
    tool_seq: Sequence[str],
) -> dict[str, Any]:
    status = run.status if run is not None else (decision.status if decision else "not_run")
    return {
        "task_hash": turn.task_hash,
        "turn_index": turn.turn_index,
        "task_turn_count": turn.task_turn_count,
        "mode": mode,
        "harness_status": status,
        "executed": run is not None,
        "duration_ms": round(float(run.duration_ms), 1) if run is not None else 0.0,
        "timeout": bool(run is not None and run.status == "timeout"),
        "timeout_reason": run.timeout_reason if run is not None else None,
        "tool_count": len(tool_seq),
        "context_pack_digest": context_digest,
        "decision_action": decision.next_action.value if decision else None,
        "decision_confidence": decision.confidence if decision else None,
        "decision_source": decision.source if decision else None,
        "validation_reason": validation.reason if validation and not validation.accepted else None,
    }


def _run_arm_task(
    *,
    adapter: HarnessAdapter,
    mode: str,
    task_hash: str,
    turns: Sequence[ReplayTurn],
    root: Path,
    timeout: float,
    jev_timeout: float,
    min_confidence: float,
    low_confidence_advisory: bool,
    seed: Path,
) -> ArmTaskResult:
    workspace = root / adapter.name / mode / task_hash / "workspace"
    _clone_workspace(workspace, seed)
    feeder = RepositoryContextFeeder()
    context = _new_context(
        task_hash, turns[0].ask, len(turns), timeout_budget_s=timeout
    )
    controller = JevController(timeout=jev_timeout) if mode == "jev" else None
    rows: list[dict[str, Any]] = []
    tool_seq: list[str] = []
    decisions: list[JevDecision] = []
    validation_reasons: list[str] = []
    session_ids: list[str] = []
    context_pack_digests: list[str] = []
    statuses: list[str] = []

    for turn in turns:
        snapshot = feeder.update(
            context,
            workspace,
            user_turn=turn.ask,
            turn_index=turn.turn_index,
        )
        context_pack_digests.append(snapshot.digest)
        turn_dir = root / adapter.name / mode / task_hash / f"turn-{turn.turn_index:03d}"
        turn_dir.mkdir(parents=True, exist_ok=True)
        run: Any | None = None
        decision: JevDecision | None = None
        validation: DecisionValidation | None = None
        if controller is not None:
            decision = controller.decide_context(context)
            validation = validate_jev_decision(decision, context, min_confidence=min_confidence)
            decisions.append(decision)
            if not validation.accepted:
                validation_reasons.append(validation.reason or "invalid_decision")
                advisory_baseline = _should_run_advisory_baseline(
                    validation, enabled=low_confidence_advisory
                )
                if not advisory_baseline:
                    context.add_evidence(f"jev_fallback:{validation.reason or 'invalid_decision'}")
                # Do not add an advisory Jev answer to the feeder context:
                # the execution prompt must remain equivalent in shape to Arm
                # A. The decision and reason are retained in the hash-only row
                # as advisory metadata.
                if advisory_baseline:
                    prompt = _context_prompt(context, turn.ask)
                    run = adapter.run(
                        prompt=prompt,
                        prompt_file=turn_dir / "prompt.txt",
                        workdir=workspace,
                        events_path=turn_dir / "events.ndjson",
                        stderr_path=turn_dir / "stderr.txt",
                        timeout=timeout,
                        title=f"jev-long-{task_hash}-{mode}-{turn.turn_index}",
                    )
                    _fold_run(context, adapter, run, tool_seq, session_ids)
            elif decision.next_action in {
                ControllerAction.FINALIZE,
                ControllerAction.ESCALATE,
                ControllerAction.ASK_USER,
            }:
                validation_reasons.append(decision.next_action.value)
                context.add_evidence(f"jev_stop:{decision.next_action.value}")
            else:
                prompt = _jev_prompt(context, decision, turn.ask)
                run = adapter.run(
                    prompt=prompt,
                    prompt_file=turn_dir / "prompt.txt",
                    workdir=workspace,
                    events_path=turn_dir / "events.ndjson",
                    stderr_path=turn_dir / "stderr.txt",
                    timeout=timeout,
                    title=f"jev-long-{task_hash}-{mode}-{turn.turn_index}",
                )
                _fold_run(context, adapter, run, tool_seq, session_ids)
                context.set_phase(
                    phase_after_action(
                        context.phase,
                        decision.next_action,
                        _status_for_context(run.status),
                    )
                )
        else:
            prompt = _context_prompt(context, turn.ask)
            run = adapter.run(
                prompt=prompt,
                prompt_file=turn_dir / "prompt.txt",
                workdir=workspace,
                events_path=turn_dir / "events.ndjson",
                stderr_path=turn_dir / "stderr.txt",
                timeout=timeout,
                title=f"jev-long-{task_hash}-{mode}-{turn.turn_index}",
            )
            _fold_run(context, adapter, run, tool_seq, session_ids)
        if run is not None:
            statuses.append(run.status)
        else:
            statuses.append("not_executed")
        rows.append(
            _turn_row(
                turn=turn,
                mode=mode,
                run=run,
                decision=decision,
                validation=validation,
                context_digest=snapshot.digest,
                tool_seq=tool_seq,
            )
        )
        context.turn_index = turn.turn_index

    return ArmTaskResult(
        task_hash=task_hash,
        adapter=adapter,
        mode=mode,
        workspace=workspace,
        rows=rows,
        tool_seq=tool_seq,
        decisions=decisions,
        validation_reasons=validation_reasons,
        session_ids=session_ids,
        context_pack_digests=context_pack_digests,
        statuses=statuses,
    )


def _task_summary(result: ArmTaskResult) -> dict[str, Any]:
    scoreable = _scoreable_tool_seq(result.tool_seq)
    scored = score_seq(scoreable)
    advisory_executions = sum(
        bool(row["executed"]) and row.get("validation_reason") == "low_confidence"
        for row in result.rows
    )
    timeout_reasons = Counter(
        str(row["timeout_reason"])
        for row in result.rows
        if row.get("timeout_reason")
    )
    return {
        "task_hash": result.task_hash,
        "adapter": result.adapter.name,
        "mode": result.mode,
        "turns": len(result.rows),
        "executed_turns": sum(bool(row["executed"]) for row in result.rows),
        "statuses": dict(sorted(Counter(result.statuses).items())),
        "timeouts": sum(status == "timeout" for status in result.statuses),
        "tool_count": len(scoreable),
        "tool_seq": scoreable,
        "work_match": bool(scored.get("work_match")),
        "fail_mask": scored.get("fail_mask"),
        "outcome": outcome_label(scoreable),
        "decision_count": len(result.decisions),
        "fallback_count": len(result.validation_reasons),
        "advisory_executions": advisory_executions,
        "timeout_reasons": dict(sorted(timeout_reasons.items())),
        "decision_actions": [decision.next_action.value for decision in result.decisions],
        "decision_confidences": [decision.confidence for decision in result.decisions],
        "validation_reasons": result.validation_reasons,
        "native_session_ids_observed": len(result.session_ids),
        "context_pack_count": len(result.context_pack_digests),
    }


def _model_config() -> dict[str, str]:
    return {
        "jev_model": os.environ.get("JEV_OPENROUTER_MODEL", "typesafe/jev-1.13"),
        "opencode_model": os.environ.get("OPENCODE_MODEL", "configured-default"),
        "pi_model": os.environ.get("PI_MODEL", "configured-default"),
        "grok_build_model": os.environ.get("GROK_BUILD_MODEL", "configured-default"),
        "grok_build_max_turns": os.environ.get("GROK_BUILD_MAX_TURNS", "configured-default"),
    }


def _aggregate(summaries: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for summary in summaries:
        groups[(summary["adapter"], summary["mode"])].append(summary)
    output: list[dict[str, Any]] = []
    for (adapter, mode), group in sorted(groups.items()):
        output.append(
            {
                "adapter": adapter,
                "mode": mode,
                "tasks": len(group),
                "turns": sum(int(row["turns"]) for row in group),
                "executed_turns": sum(int(row["executed_turns"]) for row in group),
                "timeouts": sum(int(row["timeouts"]) for row in group),
                "work_match": sum(bool(row["work_match"]) for row in group),
                "outcomes": dict(sorted(Counter(row["outcome"] for row in group).items())),
                "mean_tools_per_task": round(
                    statistics.mean(row["tool_count"] for row in group), 1
                ),
                "decisions": sum(int(row["decision_count"]) for row in group),
                "fallbacks": sum(int(row["fallback_count"]) for row in group),
                "advisory_executions": sum(
                    int(row.get("advisory_executions", 0)) for row in group
                ),
                "timeout_reasons": dict(
                    sorted(
                        Counter(
                            reason
                            for row in group
                            for reason, count in row.get("timeout_reasons", {}).items()
                            for _ in range(int(count))
                        ).items()
                    )
                ),
            }
        )
    return output


def _write_report(result: dict[str, Any], path: Path) -> None:
    low_confidence_policy = (
        "advisory baseline execution"
        if result["low_confidence_advisory"]
        else "non-executing fallback"
    )
    lines = [
        f"# Jev long-horizon matched A/B — {result['date']}",
        "",
        "Hash-only comparison of a shared context-fed baseline (A) and a Jev-"
        "validated bounded-action arm (B). The six holdout hashes were not used.",
        "",
        "## Frozen slice",
        "",
        f"- Development hashes: {', '.join(result['task_hashes'])}",
        f"- Matched replay turns per arm/harness: {result['turn_budget']}",
        f"- Adapters requested: {', '.join(result['adapters'])}",
        f"- Per bounded invocation timeout: {result['timeout_seconds']} seconds",
        f"- Jev timeout: {result['jev_timeout_seconds']} seconds",
        f"- Jev model: `{result['models']['jev_model']}` via OpenRouter Decisions API",
        f"- OpenCode model: `{result['models']['opencode_model']}`",
        f"- Pi model: `{result['models']['pi_model']}`",
        f"- Grok Build model: `{result['models']['grok_build_model']}`",
        f"- Grok Build configured max turns: `{result['models']['grok_build_max_turns']}`",
        f"- Low-confidence Jev policy: {low_confidence_policy}.",
        f"- Harness timeout policy: {result['timeout_seconds']}s inactivity timeout with "
        f"{result['max_runtime_seconds']}s absolute safety cap; stream progress resets inactivity.",
        "- Gold/reference: local ChatGPT Work/Codex development evidence; R1-R6 are diagnostic.",
        "- Raw prompts, event bodies, transcript bodies, and credentials remain ignored/local.",
        "",
        "## Aggregate results",
        "",
        "| Adapter | Mode | Tasks | Turns | Executed | Timeouts | Work-match | Outcomes | "
        "Mean tools/task | Jev decisions | Fallbacks | Advisory executions | Timeout reasons |",
        "|---|---|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---|",
    ]
    for row in result["aggregate"]:
        outcomes = ", ".join(f"{key}={value}" for key, value in row["outcomes"].items())
        lines.append(
            f"| {row['adapter']} | {row['mode']} | {row['tasks']} | {row['turns']} | "
            f"{row['executed_turns']} | {row['timeouts']} | {row['work_match']}/{row['tasks']} | "
            f"{outcomes} | {row['mean_tools_per_task']} | {row['decisions']} | "
            f"{row['fallbacks']} | {row['advisory_executions']} | "
            f"{row['timeout_reasons']} |"
        )
    lines.extend(
        [
            "",
            "## Per-task summaries",
            "",
            "| Adapter | Hash | Mode | Turns | Executed | Statuses | Work-match | Outcome | "
            "Tools | Decisions | Fallbacks | R1-R6 fail mask |",
            "|---|---|---|---:|---:|---|---:|---|---:|---:|---:|---|",
        ]
    )
    for row in result["task_summaries"]:
        statuses = ", ".join(f"{key}={value}" for key, value in row["statuses"].items())
        lines.append(
            f"| {row['adapter']} | `{row['task_hash']}` | {row['mode']} | {row['turns']} | "
            f"{row['executed_turns']} | {statuses} | {'yes' if row['work_match'] else 'no'} | "
            f"{row['outcome']} | {row['tool_count']} | {row['decision_count']} | "
            f"{row['fallback_count']} | {row['fail_mask']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "This report uses a synthetic clean snapshot of this repository as the "
            "isolated execution workspace because the original Work worktrees are "
            "not part of the committed corpus. It therefore measures transfer of "
            "observable control behavior, not reproduction of every original file "
            "outcome. A/B cells are comparable only within the recorded harness, "
            "model, fixture, workspace, and turn budget.",
            "",
            f"Source run id: `{result['run_id']}`",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def run_experiment(
    *,
    task_hashes: Sequence[str],
    adapter_names: Sequence[str],
    turn_budget: int,
    timeout: float,
    jev_timeout: float,
    min_confidence: float,
    low_confidence_advisory: bool,
    run_id: str,
    report_path: Path | None = None,
) -> dict[str, Any]:
    _load_env(ROOT / ".env")
    turns = _fixture_turns(task_hashes, turn_budget)
    by_task: dict[str, list[ReplayTurn]] = defaultdict(list)
    for turn in turns:
        by_task[turn.task_hash].append(turn)
    output_root = ROOT / ".controller-runs" / run_id
    seed = output_root / "_seed"
    _materialize_seed(seed)
    task_summaries: list[dict[str, Any]] = []
    turn_rows: list[dict[str, Any]] = []
    for adapter_name in adapter_names:
        adapter = _adapter(adapter_name)
        for task_hash in task_hashes:
            if not by_task[task_hash]:
                continue
            if not adapter.available():
                for mode in ("baseline", "jev"):
                    task_summaries.append(
                        {
                            "task_hash": task_hash,
                            "adapter": adapter_name,
                            "mode": mode,
                            "turns": len(by_task[task_hash]),
                            "executed_turns": 0,
                            "statuses": {"unavailable": len(by_task[task_hash])},
                            "timeouts": 0,
                            "tool_count": 0,
                            "tool_seq": [],
                            "work_match": False,
                            "fail_mask": "empty",
                            "outcome": "no",
                            "decision_count": 0,
                            "fallback_count": len(by_task[task_hash]) if mode == "jev" else 0,
                            "advisory_executions": 0,
                            "timeout_reasons": {},
                            "decision_actions": [],
                            "decision_confidences": [],
                            "validation_reasons": ["adapter_unavailable"],
                            "native_session_ids_observed": 0,
                            "context_pack_count": len(by_task[task_hash]),
                        }
                    )
                    turn_rows.extend(
                        {
                            "task_hash": task_hash,
                            "turn_index": turn.turn_index,
                            "mode": mode,
                            "harness_status": "unavailable",
                            "executed": False,
                        }
                        for turn in by_task[task_hash]
                    )
                continue
            for mode in ("baseline", "jev"):
                arm = _run_arm_task(
                    adapter=adapter,
                    mode=mode,
                    task_hash=task_hash,
                    turns=by_task[task_hash],
                    root=output_root,
                    timeout=timeout,
                    jev_timeout=jev_timeout,
                    min_confidence=min_confidence,
                    low_confidence_advisory=low_confidence_advisory,
                    seed=seed,
                )
                task_summaries.append(_task_summary(arm))
                turn_rows.extend(arm.rows)
    result = {
        "run_id": run_id,
        "date": time.strftime("%Y-%m-%d"),
        "task_hashes": list(task_hashes),
        "adapters": list(adapter_names),
        "turn_budget": turn_budget,
        "timeout_seconds": timeout,
        "max_runtime_seconds": HARNESS_MAX_RUNTIME_SECONDS,
        "jev_timeout_seconds": jev_timeout,
        "min_confidence": min_confidence,
        "low_confidence_advisory": low_confidence_advisory,
        "models": _model_config(),
        "rows": turn_rows,
        "task_summaries": task_summaries,
        "aggregate": _aggregate(task_summaries),
        "notes": [
            "Fixtures are the first real owner asks after stripping harness-only context blocks.",
            "The same deterministic context feeder is used by baseline and Jev arms.",
            "Each task/mode/harness has a fresh equivalent cloned workspace and persistent "
            "context within its selected turns.",
            "The six hidden holdout hashes were not selected or scored.",
        ],
    }
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "results.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if report_path:
        _write_report(result, report_path)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("hashes", nargs="*", help="development Work hash12 values")
    parser.add_argument("--turns", type=int, default=60)
    parser.add_argument("--adapters", default="opencode,grok-build,pi")
    parser.add_argument(
        "--timeout",
        type=float,
        default=HARNESS_INACTIVITY_TIMEOUT_SECONDS,
        help="inactivity timeout; active stdout/stderr progress resets it",
    )
    parser.add_argument("--jev-timeout", type=float, default=30.0)
    parser.add_argument("--min-confidence", type=float, default=0.55)
    parser.add_argument(
        "--low-confidence-advisory",
        action="store_true",
        help="execute the baseline feeder prompt for low-confidence Jev answers",
    )
    parser.add_argument("--run-id", default=f"jev-long-ab-{time.strftime('%Y%m%d-%H%M%S')}")
    parser.add_argument(
        "--report",
        type=Path,
        default=ROOT / "reports" / "jev-long-ab-latest.md",
    )
    args = parser.parse_args()
    task_hashes = args.hashes or develop_hashes()
    adapters = [name.strip() for name in args.adapters.split(",") if name.strip()]
    result = run_experiment(
        task_hashes=task_hashes,
        adapter_names=adapters,
        turn_budget=args.turns,
        timeout=args.timeout,
        jev_timeout=args.jev_timeout,
        min_confidence=args.min_confidence,
        low_confidence_advisory=args.low_confidence_advisory,
        run_id=args.run_id,
        report_path=args.report,
    )
    print(
        json.dumps(
            {
                "run_id": result["run_id"],
                "turns": result["turn_budget"],
                "adapters": result["adapters"],
                "aggregate": result["aggregate"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

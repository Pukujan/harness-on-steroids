#!/usr/bin/env python3
"""Run a hash-only Jev v2 loop against the existing develop replay hashes.

Baseline launches one bounded harness invocation. The Jev arm launches one
explicit-context invocation per validated Jev decision and folds normalized
adapter observations back into the next decision context. Raw prompts and
events stay below the ignored ``.controller-runs`` directory.
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from research.replay_lib import REPLAY, develop_hashes, first_ask, outcome_label  # noqa: E402
from src.hos.controller import (  # noqa: E402
    AdapterObservation,
    AdapterStepResult,
    DecisionBead,
    DecisionContext,
    GrokBuildAdapter,
    HarnessAdapter,
    JevController,
    JevDecision,
    JevDecisionLoop,
    OpenCodeAdapter,
    PiAdapter,
    extract_session_id,
)
from src.hos.controller.adapters import extract_tool_seq  # noqa: E402
from src.score_session import score_seq  # noqa: E402

ENV_KEYS = {
    "OPENROUTER_API_KEY",
    "OPENROUTER_API_URL",
    "JEV_OPENROUTER_MODEL",
    "OPENCODE_MODEL",
    "GROK_BUILD_MODEL",
    "PI_MODEL",
    "QWEN_API_URL",
    "QWEN_API_KEY",
}


def _load_env(path: Path, allowed: set[str] | None = None) -> None:
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        if key and (allowed is None or key in allowed):
            os.environ[key] = value.strip().strip('"').strip("'")


def _adapter(name: str) -> HarnessAdapter:
    if name == "opencode":
        return OpenCodeAdapter()
    if name == "grok-build":
        return GrokBuildAdapter()
    if name == "pi":
        return PiAdapter()
    raise ValueError(f"unknown adapter: {name}")


def _scoreable_tool_seq(seq: list[str]) -> list[str]:
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


def _status_for_step(status: str) -> str:
    if status == "ok":
        return "ok"
    if status == "partial":
        return "partial"
    return "failed"


def _step_prompt(context: DecisionContext, decision: JevDecision) -> str:
    state = json.dumps(context.to_payload(max_chars=12_000), ensure_ascii=False, indent=2)
    return (
        "You are executing one bounded step selected by a separate typed controller.\n"
        "The controller has no tools or filesystem authority. Follow the repository's "
        "instructions, inspect before writes, and verify any material change.\n\n"
        f"Selected action: {decision.next_action.value}\n"
        f"Selected bead: {decision.next_bead or 'NONE'}\n"
        "Current decision context (derived facts and summaries only):\n"
        f"{state}\n\n"
        "Perform only this bounded step. Stop after the step and leave concise observable "
        "evidence for the next controller round."
    )


class ReplayStepAdapter:
    """Adapt one existing CLI adapter to the v2 bounded-step protocol."""

    def __init__(
        self,
        adapter: HarnessAdapter,
        *,
        task_hash: str,
        root: Path,
        timeout: float,
        title: str,
    ) -> None:
        self.adapter = adapter
        self.task_hash = task_hash
        self.root = root
        self.timeout = timeout
        self.title = title
        self.step_index = 0
        self.runs: list[Any] = []
        self.tool_seq: list[str] = []
        self.session_ids: list[str] = []

    def run_step(self, context: DecisionContext, decision: JevDecision) -> AdapterStepResult:
        self.step_index += 1
        step_dir = self.root / f"step-{self.step_index:02d}"
        workdir = step_dir / "workspace"
        workdir.mkdir(parents=True, exist_ok=True)
        readme = workdir / "README.md"
        if not readme.exists():
            readme.write_text(
                f"Isolated Jev v2 replay workspace for {self.task_hash}.\n",
                encoding="utf-8",
            )
        run = self.adapter.run(
            prompt=_step_prompt(context, decision),
            prompt_file=step_dir / "prompt.txt",
            workdir=workdir,
            events_path=step_dir / "events.ndjson",
            stderr_path=step_dir / "stderr.txt",
            timeout=self.timeout,
            title=f"{self.title}-step-{self.step_index}",
        )
        self.runs.append(run)
        tools = extract_tool_seq(run.events_path)
        self.tool_seq.extend(tools)
        session_id = extract_session_id(run.events_path)
        if session_id and session_id not in self.session_ids:
            self.session_ids.append(session_id)
        events = self.adapter.stream_events(run.events_path)
        failed = run.status not in {"ok", "partial"}
        observation = AdapterObservation(
            event_kind="adapter_run",
            status=run.status,
            summary=f"{len(events)} normalized events; {len(tools)} tool observations",
            failure=run.status if failed else None,
        )
        return AdapterStepResult(
            status=_status_for_step(run.status),
            observations=(observation,),
            evidence=(f"adapter_status:{run.status}",),
        )


def _context(task_hash: str, ask: str, ask_shifted: bool) -> DecisionContext:
    bead = DecisionBead(
        "task-main",
        "Complete the existing owner request in bounded steps.",
        acceptance_criteria=("owner request satisfied", "material result verified"),
    )
    context = DecisionContext.from_ask(
        task_hash,
        ask,
        constraints=(
            "look_before_write",
            "verify_after_change",
            "do_not_print_prompt_or_secret_values",
        ),
    )
    context.open_beads = (bead,)
    context.candidate_beads = (bead,)
    if ask_shifted:
        context.add_evidence("first_stored_turn_was_harness_context_only")
    return context


def _base_row(
    *,
    task_hash: str,
    adapter: HarnessAdapter,
    mode: str,
    runs: list[Any],
    tool_seq: list[str],
    decisions: list[JevDecision],
    loop_status: str | None,
    loop_stop_reason: str | None,
    ask_shifted: bool,
    session_ids: list[str],
) -> dict[str, Any]:
    scoreable = _scoreable_tool_seq(tool_seq)
    scored = score_seq(scoreable)
    statuses = [run.status for run in runs]
    return {
        "task_hash": task_hash,
        "adapter": adapter.name,
        "mode": mode,
        "ask_present": True,
        "ask_shifted": ask_shifted,
        "controller_status": decisions[-1].status if decisions else "disabled",
        "controller_actions": [decision.next_action.value for decision in decisions],
        "controller_confidences": [decision.confidence for decision in decisions],
        "controller_errors": [decision.error_type for decision in decisions if decision.error_type],
        "decision_count": len(decisions),
        "loop_status": loop_status,
        "loop_stop_reason": loop_stop_reason,
        "harness_statuses": statuses,
        "harness_status": statuses[-1] if statuses else (loop_status or "not_run"),
        "returncodes": [run.returncode for run in runs],
        "duration_ms": round(sum(run.duration_ms for run in runs), 1),
        "timeout_count": sum(status == "timeout" for status in statuses),
        "tool_seq": scoreable,
        "tool_count": len(scoreable),
        "work_match": bool(scored.get("work_match")),
        "fail_mask": scored.get("fail_mask"),
        "outcome": outcome_label(scoreable),
        "native_session_ids_observed": len(session_ids),
        "session_reuse": "none_explicit_context_replay",
    }


def _run_baseline(
    adapter: HarnessAdapter,
    task_hash: str,
    ask: str,
    ask_shifted: bool,
    root: Path,
    timeout: float,
) -> dict[str, Any]:
    run_dir = root / adapter.name / "baseline" / task_hash
    workdir = run_dir / "workspace"
    workdir.mkdir(parents=True, exist_ok=True)
    (workdir / "README.md").write_text(
        f"Isolated Jev v2 baseline replay workspace for {task_hash}.\n", encoding="utf-8"
    )
    run = adapter.run(
        prompt=ask,
        prompt_file=run_dir / "prompt.txt",
        workdir=workdir,
        events_path=run_dir / "events.ndjson",
        stderr_path=run_dir / "stderr.txt",
        timeout=timeout,
        title=f"jev-v2-{task_hash}-baseline",
    )
    return _base_row(
        task_hash=task_hash,
        adapter=adapter,
        mode="baseline",
        runs=[run],
        tool_seq=extract_tool_seq(run.events_path),
        decisions=[],
        loop_status=None,
        loop_stop_reason=None,
        ask_shifted=ask_shifted,
        session_ids=[extract_session_id(run.events_path)]
        if extract_session_id(run.events_path)
        else [],
    )


def _run_loop(
    adapter: HarnessAdapter,
    task_hash: str,
    ask: str,
    ask_shifted: bool,
    root: Path,
    timeout: float,
    max_steps: int,
) -> dict[str, Any]:
    context = _context(task_hash, ask, ask_shifted)
    step_adapter = ReplayStepAdapter(
        adapter,
        task_hash=task_hash,
        root=root / adapter.name / "jev-loop" / task_hash,
        timeout=timeout,
        title=f"jev-v2-{task_hash}-loop",
    )
    result = JevDecisionLoop(JevController(), step_adapter, max_steps=max_steps).run(context)
    return _base_row(
        task_hash=task_hash,
        adapter=adapter,
        mode="jev-loop",
        runs=step_adapter.runs,
        tool_seq=step_adapter.tool_seq,
        decisions=list(result.decisions),
        loop_status=result.status,
        loop_stop_reason=result.stop_reason,
        ask_shifted=ask_shifted,
        session_ids=step_adapter.session_ids,
    )


def _model_config() -> dict[str, str]:
    return {
        "jev_model": os.environ.get("JEV_OPENROUTER_MODEL", "typesafe/jev-1.13"),
        "opencode_model": os.environ.get("OPENCODE_MODEL", "configured-default"),
        "grok_build_model": os.environ.get("GROK_BUILD_MODEL", "configured-default"),
        "pi_model": os.environ.get("PI_MODEL", "configured-default"),
    }


def _aggregate(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[(row["adapter"], row["mode"])].append(row)
    output: list[dict[str, Any]] = []
    for (adapter, mode), group in sorted(groups.items()):
        status_counts = Counter(row["harness_status"] for row in group)
        outcomes = Counter(row["outcome"] for row in group)
        tool_sequences = {tuple(row["tool_seq"]) for row in group}
        action_sequences = {tuple(row["controller_actions"]) for row in group}
        output.append(
            {
                "adapter": adapter,
                "mode": mode,
                "n": len(group),
                "status_counts": dict(sorted(status_counts.items())),
                "timeouts": sum(row["timeout_count"] for row in group),
                "work_match": sum(bool(row["work_match"]) for row in group),
                "outcomes": dict(sorted(outcomes.items())),
                "mean_tools": round(statistics.mean(row["tool_count"] for row in group), 1),
                "mean_decisions": round(statistics.mean(row["decision_count"] for row in group), 1),
                "distinct_tool_sequences": len(tool_sequences),
                "distinct_decision_sequences": len(action_sequences),
                # This slice has one attempt per task. Different hashes are
                # fixtures, not repeated generations, so they cannot prove
                # run-to-run variance.
                "variance_available": False,
                "native_session_observations": sum(
                    row["native_session_ids_observed"] for row in group
                ),
            }
        )
    return output


def _write_report(result: dict[str, Any], path: Path) -> None:
    lines = [
        f"# Jev controller v2 matched replay — {result['date']}",
        "",
        "This hash-only report compares one baseline invocation with a repeated Jev "
        "decision loop over the same existing development Work hashes.",
        "",
        "## Frozen slice",
        "",
        f"- Work hashes: {', '.join(result['task_hashes'])}",
        f"- Adapters: {', '.join(result['adapters'])}",
        f"- Per bounded invocation timeout: {result['timeout_seconds']} seconds",
        f"- Jev model: `{result['models']['jev_model']}` via OpenRouter Decisions API",
        f"- Adapter models: OpenCode `{result['models']['opencode_model']}`, "
        f"Grok Build `{result['models']['grok_build_model']}`, "
        f"Pi `{result['models']['pi_model']}`",
        "- Loop context mode: explicit accumulated context; no session identifier was "
        "invented or reused",
        "",
        "## Aggregate results",
        "",
        "| Adapter | Mode | n | statuses | timeouts | work-match | outcomes | mean tools | "
        "mean Jev decisions | variance |",
        "|---|---|---:|---|---:|---:|---|---:|---:|---|",
    ]
    for row in result["aggregate"]:
        status = ", ".join(f"{key}={value}" for key, value in row["status_counts"].items())
        outcomes = ", ".join(f"{key}={value}" for key, value in row["outcomes"].items())
        variance = (
            f"tools={row['distinct_tool_sequences']}, "
            f"decisions={row['distinct_decision_sequences']}"
            if row["variance_available"]
            else "not available (single run)"
        )
        lines.append(
            f"| {row['adapter']} | {row['mode']} | {row['n']} | {status} | "
            f"{row['timeouts']} | {row['work_match']}/{row['n']} | {outcomes} | "
            f"{row['mean_tools']} | {row['mean_decisions']} | {variance} |"
        )
    lines.extend(
        [
            "",
            "## Per-task observations",
            "",
            "| Adapter | Hash | Mode | status | decisions | tools | R1-R6 fail mask | "
            "work-match | outcome | actions | sessions observed |",
            "|---|---|---|---|---:|---:|---|---:|---|---|---:|",
        ]
    )
    for row in result["rows"]:
        actions = ", ".join(row["controller_actions"]) or "disabled"
        lines.append(
            f"| {row['adapter']} | `{row['task_hash']}` | {row['mode']} | "
            f"{row['harness_status']} | {row['decision_count']} | {row['tool_count']} | "
            f"{row['fail_mask']} | {'yes' if row['work_match'] else 'no'} | {row['outcome']} | "
            f"{actions} | {row['native_session_ids_observed']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "This is the smallest v2 implementation slice. A single repetition does not "
            "support a repeated-run variance claim; the report records that limitation "
            "instead of treating one run as variance evidence. Native session identifiers "
            "are recorded only when emitted by an adapter. The loop therefore uses explicit "
            "context replay, which is the documented fallback for adapters whose continuation "
            "semantics are not yet proven.",
            "",
            f"Source run id: `{result['run_id']}`",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def run_slice(
    *,
    task_hashes: list[str],
    adapter_names: list[str],
    timeout: float,
    max_steps: int,
    run_id: str,
    report_path: Path | None = None,
) -> dict[str, Any]:
    _load_env(ROOT / ".env", ENV_KEYS)
    rows: list[dict[str, Any]] = []
    output_root = ROOT / ".controller-runs" / run_id
    for name in adapter_names:
        adapter = _adapter(name)
        for task_hash in task_hashes:
            source = REPLAY / task_hash / "user.md"
            ask, ask_shifted = first_ask(source)
            if not ask:
                continue
            if not adapter.available():
                rows.extend(
                    [
                        {
                            "task_hash": task_hash,
                            "adapter": adapter.name,
                            "mode": mode,
                            "ask_present": True,
                            "ask_shifted": ask_shifted,
                            "controller_status": "not_run",
                            "controller_actions": [],
                            "controller_confidences": [],
                            "controller_errors": ["adapter_unavailable"],
                            "decision_count": 0,
                            "loop_status": None,
                            "loop_stop_reason": None,
                            "harness_statuses": ["unavailable"],
                            "harness_status": "unavailable",
                            "returncodes": [],
                            "duration_ms": 0.0,
                            "timeout_count": 0,
                            "tool_seq": [],
                            "tool_count": 0,
                            "work_match": False,
                            "fail_mask": "empty",
                            "outcome": "no",
                            "native_session_ids_observed": 0,
                            "session_reuse": "none_explicit_context_replay",
                        }
                        for mode in ("baseline", "jev-loop")
                    ]
                )
                continue
            rows.append(_run_baseline(adapter, task_hash, ask, ask_shifted, output_root, timeout))
            rows.append(
                _run_loop(
                    adapter,
                    task_hash,
                    ask,
                    ask_shifted,
                    output_root,
                    timeout,
                    max_steps,
                )
            )
    result = {
        "run_id": run_id,
        "date": time.strftime("%Y-%m-%d"),
        "task_hashes": task_hashes,
        "adapters": adapter_names,
        "timeout_seconds": timeout,
        "max_steps": max_steps,
        "repetitions": 1,
        "models": _model_config(),
        "rows": rows,
        "aggregate": _aggregate(rows),
        "notes": [
            "The input is the first real owner ask after stripping context-only harness blocks.",
            "Baseline and Jev-loop arms use fresh run directories.",
            "Raw prompts, stderr, and adapter events are ignored and are not in this result.",
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
    parser.add_argument("hashes", nargs="*", help="existing Work hash12 values")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--adapters", default="opencode,grok-build,pi")
    parser.add_argument("--timeout", type=float, default=90.0)
    parser.add_argument("--max-steps", type=int, default=3)
    parser.add_argument("--run-id", default=f"jev-v2-{time.strftime('%Y%m%d-%H%M%S')}")
    parser.add_argument("--report", type=Path, default=None)
    args = parser.parse_args()
    hashes = args.hashes or develop_hashes()[: args.limit]
    result = run_slice(
        task_hashes=hashes,
        adapter_names=[item.strip() for item in args.adapters.split(",") if item.strip()],
        timeout=args.timeout,
        max_steps=args.max_steps,
        run_id=args.run_id,
        report_path=args.report,
    )
    compact = [
        {
            "task_hash": row["task_hash"],
            "adapter": row["adapter"],
            "mode": row["mode"],
            "status": row["harness_status"],
            "decisions": row["decision_count"],
            "tools": row["tool_count"],
            "work_match": row["work_match"],
            "outcome": row["outcome"],
        }
        for row in result["rows"]
    ]
    print(json.dumps(compact, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

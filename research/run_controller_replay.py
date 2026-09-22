#!/usr/bin/env python3
"""Run a bounded baseline-versus-Jev replay pilot using existing Work hashes.

The script reads the first user turn from each selected, already archived replay
task, but writes only hashes, controller labels, tool names, and scorer cells.
Raw prompts and CLI events stay under the ignored .controller-runs directory.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from research.replay_lib import (  # noqa: E402
    REPLAY,
    develop_hashes,
    first_ask,
    outcome_label,
)
from src.hos.controller import (  # noqa: E402
    GrokBuildAdapter,
    HarnessAdapter,
    JevController,
    OpenCodeAdapter,
    PiAdapter,
    build_initial_state,
    controller_directive,
)
from src.hos.controller.adapters import extract_tool_seq  # noqa: E402
from src.score_session import score_seq  # noqa: E402


def _load_env(path: Path, allowed: set[str] | None = None) -> None:
    """Load ignored dotenv values into this process without printing them."""

    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"").strip("'")
        if key and (allowed is None or key in allowed):
            os.environ[key] = value


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


def _record(
    *,
    task_hash: str,
    adapter: HarnessAdapter,
    mode: str,
    decision: Any,
    run: Any,
    tools: list[str],
    ask_present: bool = True,
    ask_shifted: bool = False,
) -> dict[str, Any]:
    scoreable = _scoreable_tool_seq(tools)
    scored = score_seq(scoreable)
    return {
        "task_hash": task_hash,
        "adapter": adapter.name,
        "mode": mode,
        "ask_present": ask_present,
        "ask_shifted": ask_shifted,
        "controller_status": decision.status if decision else "disabled",
        "controller_action": decision.action.value if decision else None,
        "controller_confidence": decision.confidence if decision else None,
        "controller_error": decision.error_type if decision else None,
        "harness_status": run.status,
        "returncode": run.returncode,
        "duration_ms": round(run.duration_ms, 1),
        "tool_seq": scoreable,
        "tool_count": len(scoreable),
        "work_match": bool(scored.get("work_match")),
        "fail_mask": scored.get("fail_mask"),
        "outcome": outcome_label(scoreable),
        "events_path": str(run.events_path.relative_to(ROOT)),
        "stderr_path": str(run.stderr_path.relative_to(ROOT)),
    }


def run_pilot(
    *,
    task_hashes: list[str],
    adapter_names: list[str],
    timeout: float,
    run_id: str,
) -> dict[str, Any]:
    _load_env(ROOT / ".env")
    _load_env(
        Path(r"C:\Users\pujan\OneDrive\Desktop\configs\.env"),
        {"OPENROUTER_API_KEY", "OPENROUTER_API_URL", "JEV_OPENROUTER_MODEL"},
    )
    output_root = ROOT / ".controller-runs" / run_id
    rows: list[dict[str, Any]] = []
    for name in adapter_names:
        adapter = _adapter(name)
        if not adapter.available():
            for task_hash in task_hashes:
                for mode in ("baseline", "jev"):
                    rows.append(
                        {
                            "task_hash": task_hash,
                            "adapter": adapter.name,
                            "mode": mode,
                            "controller_status": "not_run",
                            "controller_action": None,
                            "controller_confidence": None,
                            "controller_error": "adapter_unavailable",
                            "harness_status": "unavailable",
                            "returncode": None,
                            "duration_ms": 0.0,
                            "tool_seq": [],
                            "tool_count": 0,
                            "work_match": False,
                            "fail_mask": "empty",
                            "outcome": "no",
                        }
                    )
            continue
        for task_hash in task_hashes:
            source = REPLAY / task_hash / "user.md"
            base_prompt, ask_shifted = first_ask(source)
            if not base_prompt:
                continue
            ask_present = bool(base_prompt)
            for mode in ("baseline", "jev"):
                decision = None
                prompt = base_prompt
                if mode == "jev":
                    decision = JevController().decide(
                        build_initial_state(
                            task_hash,
                            ask_present=ask_present,
                            ask_shifted=ask_shifted,
                        )
                    )
                    prompt = f"{controller_directive(decision)}\n\n{base_prompt}"
                run_dir = output_root / adapter.name / mode / task_hash
                workdir = run_dir / "workspace"
                workdir.mkdir(parents=True, exist_ok=True)
                (workdir / "README.md").write_text(
                    f"Isolated controller replay workspace for {task_hash}.\n", encoding="utf-8"
                )
                run = adapter.run(
                    prompt=prompt,
                    prompt_file=run_dir / "prompt.txt",
                    workdir=workdir,
                    events_path=run_dir / "events.ndjson",
                    stderr_path=run_dir / "stderr.txt",
                    timeout=timeout,
                    title=f"controller-{task_hash}-{mode}",
                )
                tools = extract_tool_seq(run.events_path)
                rows.append(
                    _record(
                        task_hash=task_hash,
                        adapter=adapter,
                        mode=mode,
                        decision=decision,
                        run=run,
                        tools=tools,
                        ask_present=ask_present,
                        ask_shifted=ask_shifted,
                    )
                )
    result = {
        "run_id": run_id,
        "task_hashes": task_hashes,
        "adapters": adapter_names,
        "timeout_seconds": timeout,
        "rows": rows,
        "notes": [
            "Pilot uses the first owner ask from each existing develop Work replay, with the "
            "prepended <recommended_plugins>/<environment_context> blocks stripped.",
            "ask_shifted marks tasks whose raw turn 1 was harness context only, so the earlier "
            "context-only runs are not comparable to these.",
            "Jev sees compact state only and supplies a routing hint; it never receives tools "
            "or filesystem authority.",
            "Raw prompts and CLI events are ignored and are not included in this result.",
        ],
    }
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "results.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("hashes", nargs="*", help="existing Work hash12 values")
    parser.add_argument("--limit", type=int, default=2)
    parser.add_argument("--adapters", default="opencode,grok-build,pi")
    parser.add_argument("--timeout", type=float, default=90.0)
    parser.add_argument("--run-id", default=f"pilot-{time.strftime('%Y%m%d-%H%M%S')}")
    args = parser.parse_args()
    hashes = args.hashes or develop_hashes()[: args.limit]
    result = run_pilot(
        task_hashes=hashes,
        adapter_names=[item.strip() for item in args.adapters.split(",") if item.strip()],
        timeout=args.timeout,
        run_id=args.run_id,
    )
    compact = []
    for row in result["rows"]:
        compact.append(
            {
                "task_hash": row["task_hash"],
                "adapter": row["adapter"],
                "mode": row["mode"],
                "controller_status": row["controller_status"],
                "controller_action": row["controller_action"],
                "harness_status": row["harness_status"],
                "tool_count": row["tool_count"],
                "work_match": row["work_match"],
                "fail_mask": row["fail_mask"],
                "outcome": row["outcome"],
            }
        )
    print(json.dumps(compact, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

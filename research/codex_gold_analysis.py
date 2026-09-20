#!/usr/bin/env python3
"""Full-corpus Codex gold analysis. Counts and sequences only. No bodies."""

from __future__ import annotations

import json
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "data" / "raw" / "codex"
REPORTS = ROOT / "reports"
STATUS = ROOT / "research" / "STATUS.md"

DECOMPOSE = {
    "spawn_agent",
    "wait_agent",
    "list_agents",
    "followup_task",
    "update_plan",
    "interrupt_agent",
}
MUTATE_TOOLS = {"apply_patch", "_create_file", "_update_file"}
EXEC_TOOLS = {"exec", "shell_command", "run"}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_status(phase: str, **extra: object) -> None:
    lines = ["# Status", "", f"- updated: {utc_now()}", f"- phase: {phase}"]
    for k, v in extra.items():
        lines.append(f"- {k}: {v}")
    lines += [
        "",
        "CONTINUE.md: do not stop. Owner plan. No SWE-bench substitute.",
        "",
    ]
    STATUS.write_text("\n".join(lines) + "\n", encoding="utf-8")


def tool_name(payload: dict) -> str | None:
    n = payload.get("name")
    if isinstance(n, str) and 0 < len(n) < 80:
        return n
    t = payload.get("type")
    if t in {"custom_tool_call", "function_call"}:
        n = payload.get("name")
        if isinstance(n, str):
            return n
    return None


def md_table(rows: list[tuple], headers: list[str], limit: int = 40) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows[:limit]:
        lines.append("| " + " | ".join("" if x is None else str(x) for x in row) + " |")
    return "\n".join(lines)


def main() -> int:
    files = sorted(CODEX.glob("*.jsonl"))
    write_status("gold_analysis_start", files=len(files))
    t0 = time.time()
    top_types: Counter[str] = Counter()
    tools: Counter[str] = Counter()
    collab: Counter[str] = Counter()
    models: Counter[str] = Counter()
    originators: Counter[str] = Counter()
    first_tools: Counter[str] = Counter()
    bigrams: Counter[str] = Counter()
    trigrams: Counter[str] = Counter()
    decompose_sessions = 0
    mutate_sessions = 0
    exec_sessions = 0
    n_ok = 0
    n_bad = 0
    n_lines = 0
    for i, path in enumerate(files, 1):
        if i % 50 == 0:
            write_status("gold_analysis", progress=f"{i}/{len(files)}", lines=n_lines)
        seq: list[str] = []
        saw_decomp = False
        saw_mut = False
        saw_exec = False
        try:
            with path.open("r", encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        n_bad += 1
                        continue
                    n_lines += 1
                    t = obj.get("type")
                    if isinstance(t, str):
                        top_types[t] += 1
                    payload = obj.get("payload") if isinstance(obj.get("payload"), dict) else {}
                    if t == "session_meta":
                        orig = payload.get("originator")
                        if isinstance(orig, str):
                            originators[orig] += 1
                    if t == "turn_context":
                        cm = payload.get("collaboration_mode")
                        if isinstance(cm, dict):
                            mode = cm.get("mode")
                            if isinstance(mode, str):
                                collab[mode] += 1
                        model = payload.get("model")
                        if isinstance(model, str) and len(model) < 80:
                            models[model] += 1
                    name = tool_name(payload)
                    if name:
                        tools[name] += 1
                        seq.append(name)
                        if name in DECOMPOSE:
                            saw_decomp = True
                        if name in MUTATE_TOOLS:
                            saw_mut = True
                        if name in EXEC_TOOLS:
                            saw_exec = True
        except OSError:
            continue
        n_ok += 1
        if seq:
            first_tools[seq[0]] += 1
            for a, b in zip(seq, seq[1:]):
                bigrams[f"{a} -> {b}"] += 1
            for a, b, c in zip(seq, seq[1:], seq[2:]):
                trigrams[f"{a} -> {b} -> {c}"] += 1
        if saw_decomp:
            decompose_sessions += 1
        if saw_mut:
            mutate_sessions += 1
        if saw_exec:
            exec_sessions += 1

    REPORTS.mkdir(parents=True, exist_ok=True)
    parts = [
        "# Codex gold behavior (full hashed corpus)",
        "",
        f"Generated: {utc_now()}",
        "",
        "Local Codex/ChatGPT Work transcripts are gold. No message bodies.",
        "",
        f"- hashed files: **{n_ok}** / {len(files)}",
        f"- lines: **{n_lines}**",
        f"- bad json lines: **{n_bad}**",
        f"- sessions with decompose tools (spawn/plan/wait/list/followup): **{decompose_sessions}**",
        f"- sessions with exec/shell: **{exec_sessions}**",
        f"- sessions with apply_patch/file tools: **{mutate_sessions}**",
        "",
        "## originator",
        "",
        md_table(originators.most_common(), ["originator", "count"]),
        "",
        "## collaboration_mode",
        "",
        md_table(collab.most_common(), ["mode", "count"]),
        "",
        "## models (turn_context)",
        "",
        md_table(models.most_common(20), ["model", "count"]),
        "",
        "## top-level JSONL type",
        "",
        md_table(top_types.most_common(), ["type", "count"]),
        "",
        "## tool names",
        "",
        md_table(tools.most_common(50), ["tool", "count"]),
        "",
        "## first tool in session",
        "",
        md_table(first_tools.most_common(20), ["first_tool", "sessions"]),
        "",
        "## tool bigrams (top 40)",
        "",
        md_table(bigrams.most_common(40), ["bigram", "count"]),
        "",
        "## tool trigrams (top 30)",
        "",
        md_table(trigrams.most_common(30), ["trigram", "count"]),
        "",
        "## How this feeds the imitate mode",
        "",
        "Kilo and OpenCode must copy **these** chains (task split + tool order), not a public exam.",
        "",
        f"Elapsed s: {int(time.time() - t0)}",
        "",
    ]
    out = REPORTS / "codex-gold-behavior.md"
    out.write_text("\n".join(parts), encoding="utf-8")
    write_status("gold_analysis_done", files=n_ok, lines=n_lines, report=str(out.name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

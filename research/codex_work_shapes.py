#!/usr/bin/env python3
"""Work-desktop session archetypes, burst lengths, send/spawn position.

Keys and counts only. No message bodies, command text, or paths.
"""

from __future__ import annotations

import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "data" / "raw" / "codex"
OUT = ROOT / "reports" / "codex-work-shapes.md"
WANT = "codex_work_desktop"
CALL_TYPES = {"custom_tool_call", "function_call"}
DECOMPOSE = {
    "send_message",
    "spawn_agent",
    "create_thread",
    "followup_task",
    "wait_agent",
    "list_agents",
    "interrupt_agent",
    "send_message_to_thread",
    "multi_agent_v1",
}


def input_obj(payload: dict):
    inp = payload.get("input") or payload.get("arguments")
    if isinstance(inp, dict):
        return inp
    if isinstance(inp, str):
        s = inp.strip()
        if s.startswith("{") or s.startswith("["):
            try:
                o = json.loads(s)
            except json.JSONDecodeError:
                return None
            return o if isinstance(o, dict) else None
    return None


def keyset(d: dict) -> str:
    return ",".join(sorted(d.keys())[:12])


def collapse(seq: list[str], limit: int = 8) -> str:
    if not seq:
        return "(empty)"
    out = [seq[0]]
    for x in seq[1:]:
        if x != out[-1]:
            out.append(x)
        if len(out) >= limit:
            break
    return " → ".join(out)


def run_lengths(seq: list[str], name: str) -> list[int]:
    runs: list[int] = []
    n = 0
    for x in seq:
        if x == name:
            n += 1
        elif n:
            runs.append(n)
            n = 0
    if n:
        runs.append(n)
    return runs


def archetype(names: set[str]) -> str:
    if "apply_patch" in names:
        return "patch"
    if names & {
        "send_message",
        "spawn_agent",
        "create_thread",
        "followup_task",
        "send_message_to_thread",
        "multi_agent_v1",
    }:
        return "multi_agent"
    if "js" in names:
        return "js"
    if "wait" in names:
        return "exec_wait"
    if "shell_command" in names:
        return "shell"
    if "exec" in names:
        return "exec_only"
    return "other"


def median(xs: list[int]) -> str:
    if not xs:
        return "n/a"
    return str(int(statistics.median(xs)))


def main() -> None:
    n = 0
    empty = 0
    arch = Counter()
    first = Counter()
    first_decomp = Counter()
    collapsed = Counter()
    keysets: dict[str, Counter] = defaultdict(Counter)
    tools_before_send: list[int] = []
    tools_before_wait: list[int] = []
    tools_before_decomp: list[int] = []
    session_len: list[int] = []
    exec_runs: list[int] = []
    send_never_first = 0
    send_sessions = 0
    spawn_sessions = 0
    wait_sessions = 0
    patch_sessions = 0

    for path in sorted(CODEX.glob("*.jsonl")):
        orig = None
        seq: list[str] = []
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                payload = obj.get("payload") if isinstance(obj.get("payload"), dict) else {}
                if obj.get("type") == "session_meta":
                    o = payload.get("originator")
                    if isinstance(o, str):
                        orig = o
                    continue
                if orig != WANT:
                    continue
                name = payload.get("name")
                pt = payload.get("type")
                if not isinstance(name, str) or pt not in CALL_TYPES:
                    continue
                seq.append(name)
                d = input_obj(payload)
                if d is not None:
                    keysets[name][keyset(d)] += 1
                elif payload.get("input") is not None:
                    keysets[name]["<non-json-or-empty>"] += 1
        if orig != WANT:
            continue
        n += 1
        if not seq:
            empty += 1
            arch["empty"] += 1
            continue
        names = set(seq)
        a = archetype(names)
        arch[a] += 1
        first[seq[0]] += 1
        collapsed[collapse(seq)] += 1
        session_len.append(len(seq))
        exec_runs.extend(run_lengths(seq, "exec"))
        if seq[0] != "send_message":
            send_never_first += 1
        if "send_message" in names:
            send_sessions += 1
            tools_before_send.append(seq.index("send_message"))
        if "spawn_agent" in names:
            spawn_sessions += 1
        if "wait" in names:
            wait_sessions += 1
            tools_before_wait.append(seq.index("wait"))
        if "apply_patch" in names:
            patch_sessions += 1
        decomp_i = next((i for i, t in enumerate(seq) if t in DECOMPOSE), None)
        if decomp_i is not None:
            tools_before_decomp.append(decomp_i)
            first_decomp[seq[decomp_i]] += 1

    lines = [
        "# ChatGPT Work session shapes (`codex_work_desktop`)",
        "",
        "Keys and counts only. No bodies. v7 interpretation.",
        "",
        f"Sessions: **{n}** (empty: **{empty}**)",
        f"- send_message sessions: **{send_sessions}**",
        f"- spawn_agent sessions: **{spawn_sessions}**",
        f"- wait sessions: **{wait_sessions}**",
        f"- apply_patch sessions: **{patch_sessions}**",
        f"- first tool is not send_message: **{send_never_first}** / {n - empty}",
        f"- median tools/session: **{median(session_len)}**",
        f"- median consecutive exec-run: **{median(exec_runs)}**",
        f"- median tools before first send_message: **{median(tools_before_send)}**",
        f"- median tools before first wait: **{median(tools_before_wait)}**",
        f"- median tools before first decompose: **{median(tools_before_decomp)}**",
        "First-tool counts are **calls only** (`custom_tool_call` / `function_call`), not outputs.",
        "",
        "## exclusive archetype",
        "",
        "| archetype | sessions |",
        "| --- | --- |",
    ]
    for k, v in arch.most_common():
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "Priority: patch > multi_agent > js > exec_wait > shell > exec_only.",
        "multi_agent = send_message / spawn_agent / create_thread / followup / thread.",
        "",
        "## first tool",
        "",
        "| tool | sessions |",
        "| --- | --- |",
    ]
    for k, v in first.most_common():
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## first decompose tool",
        "",
        "| tool | sessions |",
        "| --- | --- |",
    ]
    for k, v in first_decomp.most_common():
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## collapsed shapes (top 20)",
        "",
        "| shape | sessions |",
        "| --- | --- |",
    ]
    for k, v in collapsed.most_common(20):
        lines.append(f"| {k} | {v} |")
    for name in (
        "wait",
        "send_message",
        "spawn_agent",
        "wait_agent",
        "js",
        "shell_command",
        "followup_task",
        "exec",
        "apply_patch",
    ):
        ctr = keysets.get(name)
        if not ctr:
            continue
        lines += ["", f"## `{name}` input keysets", "", "| keys | count |", "| --- | --- |"]
        for ks, c in ctr.most_common(8):
            lines.append(f"| `{ks}` | {c} |")
    lines += [
        "",
        "## interpretation",
        "",
        "Work default is an **exec burst**, then optional **wait(cell_id)**, then more exec.",
        "Multi-piece work is **send_message(target, message)** after a look burst, not extra apply_patch.",
        "spawn_agent is rare. apply_patch is almost absent.",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} sessions={n}")


if __name__ == "__main__":
    main()

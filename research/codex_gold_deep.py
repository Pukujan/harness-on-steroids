#!/usr/bin/env python3
"""Deeper Codex gold: exec bins, per-session shapes, decompose graphs. No bodies."""

from __future__ import annotations

import json
import re
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "data" / "raw" / "codex"
STATUS = ROOT / "research" / "STATUS.md"
OUT = ROOT / "reports" / "codex-gold-behavior.md"

LOOK = {
    "get-content",
    "get-childitem",
    "rg",
    "select-string",
    "git",
    "test-path",
    "type",
    "cat",
    "head",
    "dir",
    "ls",
    "findstr",
    "get-item",
    "get-childitem",
}
CHECK = {"pytest", "npm", "cargo", "go", "dotnet", "vitest", "jest", "python"}
WRITEISH = {
    "set-content",
    "out-file",
    "new-item",
    "remove-item",
    "mkdir",
    "ni",
    "echo",
    "copy-item",
    "move-item",
    "git",
}
DECOMPOSE = {
    "spawn_agent",
    "wait_agent",
    "list_agents",
    "followup_task",
    "update_plan",
    "interrupt_agent",
    "create_thread",
    "send_message",
    "send_message_to_thread",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_status(phase: str, **extra: object) -> None:
    lines = ["# Status", "", f"- updated: {utc_now()}", f"- phase: {phase}"]
    for k, v in extra.items():
        lines.append(f"- {k}: {v}")
    lines += ["", "CONTINUE.md: do not stop. Analysis is NOT finished.", ""]
    STATUS.write_text("\n".join(lines) + "\n", encoding="utf-8")


def extract_command(inp) -> str | None:
    if isinstance(inp, dict):
        for k in ("command", "cmd", "shell", "script"):
            if isinstance(inp.get(k), str):
                return inp[k]
        return None
    if isinstance(inp, str):
        s = inp.strip()
        if s.startswith("{") or s.startswith("["):
            try:
                obj = json.loads(s)
            except json.JSONDecodeError:
                return s[:200]
            return extract_command(obj) or s[:200]
        return s
    return None


def first_tok(cmd: str) -> str:
    s = cmd.strip().strip("'\"")
    if not s:
        return ""
    # skip env prefixes
    s = re.sub(r"^\$env:[^=]+=[^;]+;\s*", "", s, flags=re.I)
    parts = s.replace("\n", " ").split()
    if not parts:
        return ""
    tok = parts[0].strip("&(").split("\\")[-1].split("/")[-1].lower()
    return tok[:40]


def git_second(cmd: str) -> str:
    parts = cmd.replace("\n", " ").split()
    if len(parts) >= 2 and parts[0].lower().endswith("git"):
        return parts[1].lower()[:20]
    return ""


def bin_exec(cmd: str) -> str:
    tok = first_tok(cmd)
    if tok == "git":
        sub = git_second(cmd)
        if sub in {"status", "log", "diff", "show", "rev-parse", "ls-files", "blame", "branch"}:
            return "look"
        if sub in {"add", "commit", "checkout", "switch", "merge", "rebase", "reset", "stash", "push", "pull", "mv", "rm"}:
            return "write"
        return "git_other"
    if tok in LOOK:
        return "look"
    if tok in WRITEISH and tok != "git":
        return "write"
    if tok in CHECK or "pytest" in cmd.lower() or " -m pytest" in cmd.lower():
        return "check"
    if tok in {"python", "py", "node", "pwsh", "powershell"}:
        return "script"
    if tok in {"const", "let", "await"} or tok.startswith('{"code"') or tok.startswith('{"cell'):
        return "js_cell"
    if tok == "***" or not tok:
        return "redacted"
    return "other:" + (tok or "?")


def md_table(rows, headers, limit=40) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows[:limit]:
        lines.append("| " + " | ".join("" if x is None else str(x) for x in row) + " |")
    if len(rows) > limit:
        lines.append(f"| … | {len(rows) - limit} more |")
    return "\n".join(lines)


def main() -> int:
    files = sorted(CODEX.glob("*.jsonl"))
    write_status("gold_deep_start", files=len(files))
    t0 = time.time()
    exec_bins: Counter[str] = Counter()
    first_bin: Counter[str] = Counter()
    shape: Counter[str] = Counter()
    n_look_then_write = 0
    n_write_first = 0
    n_with_exec = 0
    n_decomp = 0
    decomp_first: Counter[str] = Counter()
    seq_to_write: list[int] = []
    n_ok = 0
    n_lines = 0
    for i, path in enumerate(files, 1):
        if i % 40 == 0:
            write_status("gold_deep", progress=f"{i}/{len(files)}")
        bins: list[str] = []
        tools: list[str] = []
        try:
            with path.open("r", encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    n_lines += 1
                    payload = obj.get("payload") if isinstance(obj.get("payload"), dict) else {}
                    name = payload.get("name") if isinstance(payload.get("name"), str) else None
                    pt = payload.get("type")
                    if name:
                        tools.append(name)
                    if name in {"exec", "shell_command", "run"} or pt in {"custom_tool_call", "function_call"}:
                        if name in {"exec", "shell_command", "run"}:
                            cmd = extract_command(payload.get("input") or payload.get("arguments"))
                            if cmd:
                                b = bin_exec(cmd)
                                exec_bins[b] += 1
                                bins.append(b)
                    if name == "apply_patch":
                        bins.append("write")
        except OSError:
            continue
        n_ok += 1
        if bins:
            n_with_exec += 1
            first_bin[bins[0]] += 1
            # collapse consecutive
            compact = [bins[0]]
            for b in bins[1:]:
                if b != compact[-1]:
                    compact.append(b)
            shape["|".join(compact[:8])] += 1
            try:
                wi = next(i for i, b in enumerate(bins) if b == "write")
            except StopIteration:
                wi = None
            if wi == 0:
                n_write_first += 1
            elif wi is not None:
                if any(b == "look" for b in bins[:wi]):
                    n_look_then_write += 1
                seq_to_write.append(wi)
        if any(t in DECOMPOSE for t in tools):
            n_decomp += 1
            decomp_first[next(t for t in tools if t in DECOMPOSE)] += 1

    def med(xs: list[int]) -> int:
        if not xs:
            return 0
        s = sorted(xs)
        return s[len(s) // 2]

    existing = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
    extra = [
        "",
        "## Deep pass (exec bins, no command text)",
        "",
        f"Generated: {utc_now()} elapsed_s={int(time.time()-t0)} files={n_ok} lines={n_lines}",
        "",
        "### exec/shell first-token bins",
        "",
        md_table(exec_bins.most_common(40), ["bin", "count"]),
        "",
        "### first exec bin in a session",
        "",
        md_table(first_bin.most_common(), ["first_bin", "sessions"]),
        "",
        f"- sessions with exec bins: **{n_with_exec}**",
        f"- look before first write (among those with a write bin): **{n_look_then_write}**",
        f"- write as first exec bin: **{n_write_first}**",
        f"- median exec-steps to first write bin: **{med(seq_to_write)}**",
        f"- sessions with decompose tools: **{n_decomp}**",
        "",
        "### first decompose tool",
        "",
        md_table(decomp_first.most_common(), ["tool", "sessions"]),
        "",
        "### collapsed look/write/check shapes (top 25)",
        "",
        md_table(shape.most_common(25), ["shape", "sessions"]),
        "",
        "NOT DONE. Next: per-turn task graphs, error-then-look, plan-mode subset.",
        "",
    ]
    # append deep section; keep first pass
    if "## Deep pass" in existing:
        head = existing.split("## Deep pass")[0].rstrip()
        OUT.write_text(head + "\n" + "\n".join(extra), encoding="utf-8")
    else:
        OUT.write_text(existing.rstrip() + "\n" + "\n".join(extra), encoding="utf-8")
    write_status("gold_deep_done", files=n_ok, look_then_write=n_look_then_write, write_first=n_write_first)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Classify exec/js/shell input SHAPE only. No command/code bodies in output."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "data" / "raw" / "codex"
OUT = ROOT / "reports" / "codex-exec-shape.md"


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


def main() -> None:
    files = sorted(CODEX.glob("*.jsonl"))
    by_name_keys: dict[str, Counter] = {}
    exec_has_command = 0
    exec_has_code = 0
    js_has_code = 0
    n_named = Counter()
    n_files = 0
    for path in files:
        n_files += 1
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                payload = obj.get("payload") if isinstance(obj.get("payload"), dict) else {}
                name = payload.get("name")
                if not isinstance(name, str):
                    continue
                if payload.get("type") not in {"custom_tool_call", "function_call", None}:
                    # still count names we care about
                    pass
                if name not in {
                    "exec",
                    "shell_command",
                    "js",
                    "run",
                    "apply_patch",
                    "spawn_agent",
                    "update_plan",
                    "wait",
                }:
                    continue
                n_named[name] += 1
                d = input_obj(payload)
                if d is None:
                    by_name_keys.setdefault(name, Counter())["<non-json-or-empty>"] += 1
                    continue
                by_name_keys.setdefault(name, Counter())[keyset(d)] += 1
                if name == "exec":
                    if "command" in d:
                        exec_has_command += 1
                    if "code" in d or "source" in d:
                        exec_has_code += 1
                if name == "js" and ("code" in d or "source" in d or "script" in d):
                    js_has_code += 1

    lines = [
        "# Codex exec/js/shell input shapes (keys only)",
        "",
        f"Files scanned: **{n_files}**",
        "",
        f"- exec inputs with `command` key: **{exec_has_command}**",
        f"- exec inputs with `code`/`source`: **{exec_has_code}**",
        f"- js inputs with code-like key: **{js_has_code}**",
        "",
        "## call counts (this pass)",
        "",
        "| name | count |",
        "| --- | --- |",
    ]
    for k, v in n_named.most_common():
        lines.append(f"| {k} | {v} |")
    for name, ctr in sorted(by_name_keys.items()):
        lines += ["", f"## `{name}` input keysets", "", "| keys | count |", "| --- | --- |"]
        for ks, c in ctr.most_common(15):
            lines.append(f"| `{ks}` | {c} |")
    lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()

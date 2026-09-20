#!/usr/bin/env python3
"""Plan-mode mix + error-then-next-tool. No command/message bodies."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "data" / "raw" / "codex"
OUT = ROOT / "reports" / "codex-plan-and-errors.md"

EXIT_RE = re.compile(r"^Exit code:\s*(-?\d+)", re.I)


def parse_exit(out) -> int | None:
    if isinstance(out, str):
        m = EXIT_RE.match(out.lstrip())
        return int(m.group(1)) if m else None
    if isinstance(out, list) and out and isinstance(out[0], dict):
        t = out[0].get("text")
        if isinstance(t, str):
            m = EXIT_RE.match(t.lstrip())
            return int(m.group(1)) if m else None
    return None


def main() -> None:
    files = sorted(CODEX.glob("*.jsonl"))
    mode_tools: dict[str, Counter] = defaultdict(Counter)
    mode_first: dict[str, Counter] = defaultdict(Counter)
    after_fail: Counter = Counter()
    n_fail = 0
    spawn_forks: Counter = Counter()
    spawn_has_model = 0
    spawn_n = 0
    n_files = 0
    for path in files:
        n_files += 1
        last_mode = "unknown"
        last_fail = False
        first_tool_this = True
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                t = obj.get("type")
                payload = obj.get("payload") if isinstance(obj.get("payload"), dict) else {}
                if t == "turn_context":
                    cm = payload.get("collaboration_mode")
                    if isinstance(cm, dict) and isinstance(cm.get("mode"), str):
                        last_mode = cm["mode"]
                    continue
                name = payload.get("name") if isinstance(payload.get("name"), str) else None
                pt = payload.get("type")
                if name:
                    mode_tools[last_mode][name] += 1
                    if first_tool_this:
                        mode_first[last_mode][name] += 1
                        first_tool_this = False
                    if last_fail:
                        after_fail[name] += 1
                        last_fail = False
                    if name == "spawn_agent":
                        spawn_n += 1
                        inp = payload.get("input")
                        d = inp if isinstance(inp, dict) else None
                        if isinstance(inp, str) and inp.strip().startswith("{"):
                            try:
                                d = json.loads(inp)
                            except json.JSONDecodeError:
                                d = None
                        if isinstance(d, dict):
                            ft = d.get("fork_turns")
                            spawn_forks[str(ft)] += 1
                            if d.get("model"):
                                spawn_has_model += 1
                if pt in {"custom_tool_call_output", "function_call_output"}:
                    code = parse_exit(payload.get("output"))
                    if code is not None and code != 0:
                        n_fail += 1
                        last_fail = True
                    else:
                        last_fail = False

    def table(ctr: Counter, n=20) -> str:
        rows = ["| name | count |", "| --- | --- |"]
        for k, v in ctr.most_common(n):
            rows.append(f"| {k} | {v} |")
        return "\n".join(rows)

    lines = [
        "# Codex plan-mode vs default, and after failed exec",
        "",
        f"Files: **{n_files}**",
        "",
        f"- failed tool outputs (nonzero Exit code prefix): **{n_fail}**",
        f"- spawn_agent calls: **{spawn_n}** (with model field: **{spawn_has_model}**)",
        "",
        "## first tool by collaboration_mode (approx, last mode on file)",
        "",
    ]
    for mode, ctr in sorted(mode_first.items()):
        lines += [f"### first tool, mode={mode}", "", table(ctr, 10), ""]
    lines += ["## tools by last collaboration_mode", ""]
    for mode, ctr in sorted(mode_tools.items()):
        lines += [f"### tools, mode={mode}", "", table(ctr, 12), ""]
    lines += [
        "## next tool after nonzero exit",
        "",
        table(after_fail, 15),
        "",
        "## spawn_agent fork_turns (values only)",
        "",
        table(spawn_forks, 15),
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()

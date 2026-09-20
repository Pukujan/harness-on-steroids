#!/usr/bin/env python3
"""Work-desktop only: next tool after nonzero Exit code. No bodies."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "data" / "raw" / "codex"
OUT = ROOT / "reports" / "codex-work-errors.md"
WANT = "codex_work_desktop"
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
    after = Counter()
    n_fail = 0
    n_sess = 0
    for path in sorted(CODEX.glob("*.jsonl")):
        orig = None
        last_fail = False
        in_work = False
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                payload = obj.get("payload") if isinstance(obj.get("payload"), dict) else {}
                if obj.get("type") == "session_meta":
                    o = payload.get("originator")
                    in_work = o == WANT
                    orig = o
                    continue
                if not in_work:
                    continue
                name = payload.get("name") if isinstance(payload.get("name"), str) else None
                pt = payload.get("type")
                if last_fail and name:
                    after[name] += 1
                    last_fail = False
                if pt in {"custom_tool_call_output", "function_call_output"}:
                    code = parse_exit(payload.get("output"))
                    if code is not None and code != 0:
                        n_fail += 1
                        last_fail = True
                    else:
                        last_fail = False
        if orig == WANT:
            n_sess += 1
    lines = [
        "# ChatGPT Work only — after nonzero exit",
        "",
        f"Work files: **{n_sess}** failed outputs: **{n_fail}**",
        "",
        "| next tool | count |",
        "| --- | --- |",
    ]
    for k, v in after.most_common(15):
        lines.append(f"| {k} | {v} |")
    lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()

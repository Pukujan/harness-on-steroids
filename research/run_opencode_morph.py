#!/usr/bin/env python3
"""Replay gitignored morphs/m1.md into opencode-morph.ndjson. Prints hash+status only."""

from __future__ import annotations

import subprocess
import sys
import threading
from pathlib import Path
from shutil import which

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from research.replay_lib import REPLAY, tool_seq  # noqa: E402

_EXE = Path(r"C:\nvm4w\nodejs\node_modules\opencode-ai\bin\opencode.exe")
_CMD = Path(r"C:\nvm4w\nodejs\opencode.cmd")
OPENCODE = (
    str(_EXE)
    if _EXE.is_file()
    else (str(_CMD) if _CMD.is_file() else (which("opencode") or "opencode"))
)


def run_morph(h: str) -> str:
    dest = REPLAY / h
    m1 = dest / "morphs" / "m1.md"
    nd = dest / "opencode-morph.ndjson"
    if not m1.is_file():
        return "no-m1"
    if tool_seq(nd):
        return "skip"
    prompt = m1.read_text(encoding="utf-8", errors="replace")
    if not prompt.strip():
        return "empty-m1"
    sandbox = dest / "oc-morph-sandbox"
    sandbox.mkdir(parents=True, exist_ok=True)
    (sandbox / "README.md").write_text(f"Morph sandbox {h}\n", encoding="utf-8")
    cmd = [
        OPENCODE,
        "run",
        "--agent",
        "codex",
        "--format",
        "json",
        "--dir",
        str(sandbox),
        "--title",
        f"morph-{h}",
        "--auto",
        prompt,
    ]
    proc = subprocess.Popen(
        cmd,
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    err_box: list[str] = []

    def pump() -> None:
        assert proc.stdout is not None
        with nd.open("w", encoding="utf-8") as out:
            for line in proc.stdout:
                out.write(line)
                out.flush()
        if proc.stderr:
            err_box.append(proc.stderr.read())

    t = threading.Thread(target=pump, daemon=True)
    t.start()
    t.join(180)
    if t.is_alive():
        proc.kill()
        (dest / "opencode-morph.err").write_text("timeout\n", encoding="utf-8")
        return "timeout"
    proc.wait()
    if tool_seq(nd):
        return "ok"
    return "empty-tools"


def main() -> None:
    hashes = sys.argv[1:] or ["74841f3cc419"]
    for h in hashes:
        print(h, run_morph(h))


if __name__ == "__main__":
    main()

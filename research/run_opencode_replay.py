#!/usr/bin/env python3
"""Idempotent OpenCode develop replay. Skip hashes that already have tools. No stdout bodies."""

from __future__ import annotations

import argparse
import subprocess
import sys
import threading
from pathlib import Path
from shutil import which

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from research.replay_lib import (  # noqa: E402
    REPLAY,
    ask_turns,
    develop_hashes,
    strip_context_blocks,
    tool_seq,
    user_turns,
)

_EXE = Path(r"C:\nvm4w\nodejs\node_modules\opencode-ai\bin\opencode.exe")
_CMD = Path(r"C:\nvm4w\nodejs\opencode.cmd")
OPENCODE = (
    str(_EXE)
    if _EXE.is_file()
    else (str(_CMD) if _CMD.is_file() else (which("opencode") or "opencode"))
)


def already_done(dest: Path) -> bool:
    return bool(tool_seq(dest / "opencode.ndjson"))


def run_hash(
    h: str,
    max_turns: int,
    model: str = "",
    extra: bool = False,
    turn: int = 0,
) -> str:
    dest = REPLAY / h
    user = dest / "user.md"
    if not user.is_file():
        return "no-user"
    if already_done(dest) and not extra and turn <= 0:
        return "skip"
    turns = user_turns(user)
    if turn:
        if turn < 1 or turn > len(turns):
            return "bad-turn"
        extra = turn > 1
        # --turn keeps raw transcript indices so earlier notes stay reproducible,
        # but a raw turn is never sent while it is only harness context blocks.
        ask = strip_context_blocks(turns[turn - 1])
        if not ask:
            return "empty-ask"
        turns = [ask]
        max_turns = 1
    elif extra:
        asks = ask_turns(user)
        fallback = "Continue the same task. Look first, then verify with tools."
        nxt = asks[1] if len(asks) > 1 else fallback
        turns = [nxt]
        max_turns = 1
    else:
        # Sequential path: drop the context-only turn so turn 1 is the owner's ask.
        turns = ask_turns(user)
    if not turns:
        return "empty"
    sandbox = dest / "oc-sandbox"
    sandbox.mkdir(parents=True, exist_ok=True)
    (sandbox / "README.md").write_text(
        f"Isolated OpenCode replay sandbox for {h}. Gitignored.\n", encoding="utf-8"
    )
    nd = dest / "opencode.ndjson"
    err = dest / "opencode.err"
    # One process per user turn. Stream JSON events to disk as they arrive.
    for i, turn in enumerate(turns[:max_turns]):
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
            f"replay-{h}",
            "--auto",
        ]
        if model:
            cmd.extend(["--model", model])
        if extra or i:
            cmd.append("-c")
        cmd.append(turn)
        mode = "a" if extra or (i and nd.is_file()) else "w"
        proc = subprocess.Popen(
            cmd,
            cwd=str(ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        assert proc.stdout is not None
        stderr_box: list[str] = []

        def pump() -> None:
            with nd.open(mode, encoding="utf-8") as out:
                for line in proc.stdout:
                    out.write(line)
                    out.flush()
            if proc.stderr:
                stderr_box.append(proc.stderr.read())

        t = threading.Thread(target=pump, daemon=True)
        t.start()
        t.join(180)
        if t.is_alive():
            proc.kill()
            err.write_text("timeout\n", encoding="utf-8")
            return "timeout"
        rc = proc.wait()
        stderr = stderr_box[0] if stderr_box else ""
        if rc != 0:
            if stderr:
                err.write_text(stderr[-4000:], encoding="utf-8")
            return f"fail-{rc}"
    if already_done(dest):
        return "ok"
    if nd.is_file() and nd.stat().st_size > 0:
        return "empty-tools"
    return "no-output"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("hashes", nargs="*", help="hash12 list; default = pending develop")
    p.add_argument("--max-turns", type=int, default=1)
    p.add_argument("--model", default="", help="opencode --model override, e.g. openrouter/inclusionai/ling-3.0-flash-fin:free")
    p.add_argument("--extra", action="store_true", help="one more -c turn even if tools already exist")
    p.add_argument("--turn", type=int, default=0, help="1-based user turn; implies -c when >1")
    args = p.parse_args()
    want = args.hashes or develop_hashes()
    for h in want:
        if already_done(REPLAY / h) and not args.extra and args.turn <= 0:
            print(f"{h} skip")
            continue
        try:
            status = run_hash(
                h, args.max_turns, model=args.model, extra=args.extra, turn=args.turn
            )
        except subprocess.TimeoutExpired:
            status = "timeout"
            (REPLAY / h / "opencode.err").write_text("timeout\n", encoding="utf-8")
        print(f"{h} {status}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Write Work user asks to gitignored data/replay/. Never print bodies."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "data" / "raw" / "codex"
OUT = ROOT / "data" / "replay"
WANT = "codex_work_desktop"
CALL_TYPES = {"custom_tool_call", "function_call"}


def user_text_from_payload(payload: dict) -> str:
    if payload.get("type") != "message" or payload.get("role") != "user":
        return ""
    content = payload.get("content")
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                t = item.get("text") or item.get("input_text")
                if isinstance(t, str):
                    parts.append(t)
        return "\n".join(p.strip() for p in parts if p.strip())
    return ""


def extract_one(path: Path) -> dict:
    orig = None
    users: list[str] = []
    calls: list[str] = []
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
            t = user_text_from_payload(payload)
            if t:
                users.append(t)
            name = payload.get("name")
            pt = payload.get("type")
            if isinstance(name, str) and pt in CALL_TYPES:
                calls.append(name)
    return {"orig": orig, "users": users, "calls": calls}


def write_session(hash12: str, users: list[str], calls: list[str]) -> Path:
    dest = OUT / hash12
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "user.md").write_text("\n\n---\n\n".join(users), encoding="utf-8")
    meta = {
        "hash12": hash12,
        "user_turns": len(users),
        "tool_calls": len(calls),
        "first": calls[0] if calls else None,
        "patch": "apply_patch" in calls,
    }
    (dest / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return dest


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    n = 0
    n_with_user = 0
    for path in sorted(CODEX.glob("*.jsonl")):
        got = extract_one(path)
        if got["orig"] != WANT:
            continue
        n += 1
        if not got["users"]:
            continue
        n_with_user += 1
        write_session(path.stem[:12], got["users"], got["calls"])
    (OUT / "README.md").write_text(
        f"Gitignored Work replay prompts. sessions_with_user={n_with_user} of {n}. Do not commit.\n",
        encoding="utf-8",
    )
    print(f"extract_replay sessions={n} with_user={n_with_user} dest=data/replay")


if __name__ == "__main__":
    main()

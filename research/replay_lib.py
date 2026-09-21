"""Shared replay helpers. Hashes and tool names only. Never print bodies."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPLAY = ROOT / "data" / "replay"
HOLD = ROOT / "reports" / "work-long-holdout.md"
SCORES = ROOT / "reports" / "replay-scores.md"

LOOK = {"read", "grep", "glob", "webfetch", "websearch", "semantic_search", "list"}
WRITE = {"edit", "write", "patch"}


def hashes_from(md: Path, heading: str) -> list[str]:
    text = md.read_text(encoding="utf-8")
    chunk = text.split(heading, 1)[-1].split("## ", 1)[0]
    found: list[str] = []
    for tok in chunk.replace("`", " ").split():
        if len(tok) == 12 and all(c in "0123456789abcdef" for c in tok):
            found.append(tok)
    return found


def develop_hashes() -> list[str]:
    return hashes_from(HOLD, "## Develop")


def holdout_hashes() -> list[str]:
    return hashes_from(HOLD, "## Hidden holdout")


def load_text(path: Path) -> str:
    raw = path.read_bytes()
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        u16 = raw.decode("utf-16", errors="replace")
        u8 = raw.decode("utf-8", errors="ignore")
        return u16 + "\n" + u8
    return raw.decode("utf-8", errors="replace")


def tool_seq(path: Path) -> list[str]:
    if not path.is_file() or path.stat().st_size == 0:
        return []
    seq: list[str] = []
    for line in load_text(path).splitlines():
        s = line.strip()
        if not s:
            continue
        try:
            obj = json.loads(s)
        except json.JSONDecodeError:
            continue
        part = obj.get("part") if isinstance(obj.get("part"), dict) else {}
        name = obj.get("tool") or obj.get("name") or part.get("tool") or part.get("name")
        if isinstance(name, str) and name:
            seq.append(name.lower())
    return seq


def outcome_label(seq: list[str]) -> str:
    if not seq:
        return "no"
    research = any(t in LOOK for t in seq)
    wrote = any(t in WRITE for t in seq)
    verify = any(t in {"bash", "task"} for t in seq)
    if research and (verify or wrote):
        return "partial"
    if research:
        return "partial"
    return "no"


def cell(seq: list[str], empty: str = "pending") -> str:
    if not seq:
        return empty
    from src.score_session import score_seq

    s = score_seq(seq)
    wm = "yes" if s.get("work_match") else "no"
    mask = s.get("fail_mask") or "empty"
    return f"{wm}/{mask}/{outcome_label(seq)}"


def process_cell(seq: list[str], empty: str = "pending") -> str:
    """Match older table shape: work_match/fail_mask without outcome suffix."""
    if not seq:
        return empty
    from src.score_session import score_seq

    s = score_seq(seq)
    wm = "yes" if s.get("work_match") else "no"
    mask = s.get("fail_mask") or "empty"
    return f"{wm}/{mask}"


def user_turns(user_md: Path) -> list[str]:
    text = user_md.read_text(encoding="utf-8")
    parts = [p.strip() for p in text.split("\n\n---\n\n") if p.strip()]
    return parts


def parse_score_row(line: str) -> dict[str, str] | None:
    if not line.startswith("| ") or "hash12" in line or line.startswith("| ---"):
        return None
    cols = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cols) < 6:
        return None
    return {
        "hash12": cols[0],
        "work_match": cols[1],
        "fail_mask": cols[2],
        "kilo": cols[3],
        "opencode": cols[4],
        "morph": cols[5],
    }

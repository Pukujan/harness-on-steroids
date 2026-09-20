#!/usr/bin/env python3
"""Resumable overnight corpus pipeline.

Copy then hash before parse. Counts and type histograms only. Never writes
message bodies, titles, previews, prompts, or file contents to reports.
"""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import sys
import time
import traceback
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw"
REPORTS = ROOT / "reports"
STATUS = ROOT / "research" / "STATUS.md"
MANIFEST = DATA / "manifest.jsonl"

CODEX_SESSIONS = Path(r"C:\Users\pujan\.codex\sessions")
CODEX_ARCHIVED = Path(r"C:\Users\pujan\.codex\archived_sessions")
SQLITE_SOURCES = {
    "codex_thread_history": Path(r"C:\Users\pujan\.codex\thread_history_1.sqlite"),
    "codex_state": Path(r"C:\Users\pujan\.codex\state_5.sqlite"),
    "kilo": Path(r"C:\Users\pujan\.local\share\kilo\kilo.db"),
    "opencode": Path(r"C:\Users\pujan\.local\share\opencode\opencode.db"),
}

SKIP_KEYS = {
    "content",
    "text",
    "body",
    "encrypted_content",
    "base_instructions",
    "message",
    "preview",
    "first_user_message",
    "title",
    "prompt",
    "summary",
    "replacement_history",
    "cwd",
    "path",
    "directory",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_status(phase: str, **extra: object) -> None:
    STATUS.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Overnight status",
        "",
        f"- updated: {utc_now()}",
        f"- phase: {phase}",
    ]
    for key, value in extra.items():
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("Watchdog: if this file is stale >20 min and the runner is not alive, restart `python research/overnight_runner.py`.")
    lines.append("")
    lines.append("Do not start Milestone A issues. Do not patch Kilo/OpenCode. Do not commit `data/`.")
    lines.append("")
    STATUS.write_text("\n".join(lines) + "\n", encoding="utf-8")


def sha256_copy(src: Path, dest: Path) -> tuple[str, int]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    h = hashlib.sha256()
    size = 0
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    with src.open("rb") as inf, tmp.open("wb") as out:
        while True:
            chunk = inf.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
            out.write(chunk)
            size += len(chunk)
    digest = h.hexdigest()
    final = dest.parent / f"{digest}{src.suffix}"
    if dest != final:
        tmp.replace(final)
        return digest, size
    tmp.replace(dest)
    return digest, size


def load_copied_hashes() -> set[str]:
    seen: set[str] = set()
    if not MANIFEST.exists():
        return seen
    with MANIFEST.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            digest = row.get("sha256")
            if isinstance(digest, str):
                seen.add(digest)
    return seen


def append_manifest(row: dict) -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, sort_keys=True) + "\n")


def copy_hash_jsonl() -> dict:
    files: list[tuple[str, Path]] = []
    if CODEX_SESSIONS.exists():
        files.extend(("sessions", p) for p in CODEX_SESSIONS.rglob("rollout-*.jsonl"))
    if CODEX_ARCHIVED.exists():
        files.extend(("archived", p) for p in CODEX_ARCHIVED.rglob("rollout-*.jsonl"))
    files.sort(key=lambda item: str(item[1]))
    seen = load_copied_hashes()
    copied = 0
    skipped = 0
    errors = 0
    dest_dir = DATA / "codex"
    dest_dir.mkdir(parents=True, exist_ok=True)
    total = len(files)
    for i, (kind, src) in enumerate(files, 1):
        try:
            st = src.stat()
            # Fast skip: if a dest with matching size already hashed this exact file
            # we still hash unless manifest already has source_rel+mtime+bytes.
        except OSError:
            errors += 1
            continue
        rel = str(src).replace(str(Path(r"C:\Users\pujan\.codex")) + os.sep, "").replace("\\", "/")
        already = False
        if MANIFEST.exists():
            # cheap in-memory skip uses sha only; check by rel+mtime+bytes via a sidecar index later
            pass
        write_status(
            "copy_hash_jsonl",
            progress=f"{i}/{total}",
            copied=copied,
            skipped=skipped,
            errors=errors,
            current_rel=rel,
        )
        try:
            digest, size = sha256_copy(src, dest_dir / "pending.jsonl")
            if digest in seen:
                skipped += 1
                pending_final = dest_dir / f"{digest}.jsonl"
                if pending_final.exists():
                    pass
            else:
                append_manifest(
                    {
                        "kind": kind,
                        "source_rel": rel,
                        "mtime": int(st.st_mtime),
                        "bytes": size,
                        "sha256": digest,
                        "copied_at": utc_now(),
                    }
                )
                seen.add(digest)
                copied += 1
        except Exception as exc:
            errors += 1
            append_manifest(
                {
                    "kind": kind,
                    "source_rel": rel,
                    "error": type(exc).__name__,
                    "copied_at": utc_now(),
                }
            )
        if i % 25 == 0:
            write_status(
                "copy_hash_jsonl",
                progress=f"{i}/{total}",
                copied=copied,
                skipped=skipped,
                errors=errors,
            )
    return {"total": total, "copied": copied, "skipped": skipped, "errors": errors}


def backup_sqlite(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        dest.unlink()
    src_con = sqlite3.connect(f"file:{src}?mode=ro", uri=True)
    dest_con = sqlite3.connect(dest)
    try:
        src_con.backup(dest_con)
    finally:
        dest_con.close()
        src_con.close()


def copy_sqlites() -> dict:
    out: dict[str, object] = {}
    dest_dir = DATA / "sqlite"
    dest_dir.mkdir(parents=True, exist_ok=True)
    for label, src in SQLITE_SOURCES.items():
        write_status("copy_sqlite", current=label)
        dest = dest_dir / f"{label}{src.suffix}"
        try:
            backup_sqlite(src, dest)
            out[label] = {"bytes": dest.stat().st_size, "ok": True}
        except Exception as exc:
            out[label] = {"ok": False, "error": type(exc).__name__}
    return out


def connect(path: Path) -> sqlite3.Connection:
    return sqlite3.connect(f"file:{path}?mode=ro", uri=True)


def hist(con: sqlite3.Connection, sql: str) -> list[tuple]:
    return list(con.execute(sql))


def md_table(rows: list[tuple], headers: list[str], limit: int = 30) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows[:limit]:
        lines.append("| " + " | ".join("" if v is None else str(v) for v in row) + " |")
    if len(rows) > limit:
        lines.append(f"| … | {len(rows) - limit} more |")
    return "\n".join(lines)


def sqlite_metrics() -> None:
    write_status("sqlite_metrics")
    REPORTS.mkdir(parents=True, exist_ok=True)
    thread_db = DATA / "sqlite" / "codex_thread_history.sqlite"
    state_db = DATA / "sqlite" / "codex_state.sqlite"
    kilo_db = DATA / "sqlite" / "kilo.db"
    oc_db = DATA / "sqlite" / "opencode.db"

    parts: list[str] = [
        "# Local corpus stats (counts only)",
        "",
        f"Generated: {utc_now()}",
        "",
        "No message bodies, titles, previews, or paths with file contents.",
        "",
        "## Codex Work / Desktop",
        "",
        "Primary transcripts are local `rollout-*.jsonl`. ChatGPT.com Cloud is not this corpus.",
        "",
    ]

    if state_db.exists():
        con = connect(state_db)
        n = con.execute("SELECT COUNT(*) FROM threads").fetchone()[0]
        parts.append(f"Threads in `state_5` copy: **{n}**")
        parts.append("")
        parts.append("### Originator")
        parts.append("")
        parts.append(
            md_table(
                hist(
                    con,
                    "SELECT COALESCE(originator,'(null)'), COUNT(*) FROM threads GROUP BY 1 ORDER BY 2 DESC",
                ),
                ["originator", "count"],
            )
        )
        parts.append("")
        parts.append("### thread_source")
        parts.append("")
        parts.append(
            md_table(
                hist(
                    con,
                    "SELECT COALESCE(thread_source,'(null)'), COUNT(*) FROM threads GROUP BY 1 ORDER BY 2 DESC",
                ),
                ["thread_source", "count"],
            )
        )
        parts.append("")
        parts.append("### model")
        parts.append("")
        parts.append(
            md_table(
                hist(
                    con,
                    "SELECT COALESCE(model,'(null)'), COUNT(*) FROM threads GROUP BY 1 ORDER BY 2 DESC",
                ),
                ["model", "count"],
            )
        )
        parts.append("")
        parts.append("### archived")
        parts.append("")
        parts.append(
            md_table(
                hist(con, "SELECT COALESCE(archived,0), COUNT(*) FROM threads GROUP BY 1"),
                ["archived", "count"],
            )
        )
        con.close()

    if thread_db.exists():
        con = connect(thread_db)
        parts.append("")
        parts.append("### item_type histogram")
        parts.append("")
        parts.append(
            md_table(
                hist(
                    con,
                    "SELECT COALESCE(item_type,'(null)'), COUNT(*) FROM thread_items GROUP BY 1 ORDER BY 2 DESC",
                ),
                ["item_type", "count"],
            )
        )

        # Per-thread first mutate / observe-prefix using item_type only.
        first_kinds: Counter[str] = Counter()
        first10: Counter[str] = Counter()
        seq_to_filechange: list[int] = []
        seq_to_command: list[int] = []
        seq_to_search: list[int] = []
        observe_before_filechange = 0
        plan_before_filechange = 0
        threads_with_filechange = 0
        threads_with_search = 0
        threads_with_plan = 0
        n_threads = 0
        cur = con.execute(
            "SELECT thread_id, item_type FROM thread_items ORDER BY thread_id, rollout_ordinal"
        )
        current_id = None
        types: list[str] = []

        def flush(seq: list[str]) -> None:
            nonlocal observe_before_filechange, plan_before_filechange
            nonlocal threads_with_filechange, threads_with_search, threads_with_plan, n_threads
            if not seq:
                return
            n_threads += 1
            first_kinds[seq[0]] += 1
            first10["|".join(seq[:10])] += 1
            def first_idx(name: str) -> int | None:
                try:
                    return seq.index(name)
                except ValueError:
                    return None

            fc = first_idx("fileChange")
            cmd = first_idx("commandExecution")
            search = first_idx("webSearch")
            plan = first_idx("plan")
            if fc is not None:
                threads_with_filechange += 1
                seq_to_filechange.append(fc)
                prefix = seq[:fc]
                if "webSearch" in prefix or "imageView" in prefix:
                    observe_before_filechange += 1
                if "plan" in prefix:
                    plan_before_filechange += 1
            if cmd is not None:
                seq_to_command.append(cmd)
            if search is not None:
                threads_with_search += 1
                seq_to_search.append(search)
            if plan is not None:
                threads_with_plan += 1

        for thread_id, item_type in cur:
            if thread_id != current_id:
                flush(types)
                current_id = thread_id
                types = []
            types.append(item_type or "null")
        flush(types)

        def median(xs: list[int]) -> float:
            if not xs:
                return 0.0
            s = sorted(xs)
            return s[len(s) // 2]

        parts.append("")
        parts.append("### loop proxies (item_type sequence, no bodies)")
        parts.append("")
        parts.append(f"- threads with item rows: **{n_threads}**")
        parts.append(f"- threads with fileChange: **{threads_with_filechange}**")
        parts.append(f"- threads with webSearch: **{threads_with_search}**")
        parts.append(f"- threads with plan: **{threads_with_plan}**")
        if threads_with_filechange:
            parts.append(
                f"- webSearch/imageView before first fileChange: **{observe_before_filechange}** "
                f"({observe_before_filechange / threads_with_filechange:.1%})"
            )
            parts.append(
                f"- plan before first fileChange: **{plan_before_filechange}** "
                f"({plan_before_filechange / threads_with_filechange:.1%})"
            )
            parts.append(f"- median seq to first fileChange: **{median(seq_to_filechange)}**")
        if seq_to_command:
            parts.append(f"- median seq to first commandExecution: **{median(seq_to_command)}**")
        if seq_to_search:
            parts.append(f"- median seq to first webSearch: **{median(seq_to_search)}**")
        parts.append("")
        parts.append("### first item_type")
        parts.append("")
        parts.append(
            md_table([(k, v) for k, v in first_kinds.most_common()], ["first_item_type", "threads"])
        )
        parts.append("")
        parts.append("### first-10 item_type signatures (top 20)")
        parts.append("")
        parts.append(
            md_table(
                [(k, v) for k, v in first10.most_common(20)],
                ["first10", "threads"],
            )
        )
        con.close()

    def json_type_hist(db: Path, table: str, label: str) -> None:
        if not db.exists():
            parts.append(f"- missing {label}")
            return
        con = connect(db)
        n_sess = con.execute("SELECT COUNT(*) FROM session").fetchone()[0]
        n_msg = con.execute("SELECT COUNT(*) FROM message").fetchone()[0]
        n_part = con.execute("SELECT COUNT(*) FROM part").fetchone()[0]
        parts.append(f"### {label}")
        parts.append("")
        parts.append(f"- sessions: **{n_sess}**")
        parts.append(f"- messages: **{n_msg}**")
        parts.append(f"- parts: **{n_part}**")
        parts.append("")
        parts.append("part `json_extract(data,'$.type')`")
        parts.append("")
        try:
            rows = hist(
                con,
                "SELECT COALESCE(json_extract(data,'$.type'),'(null)'), COUNT(*) FROM part GROUP BY 1 ORDER BY 2 DESC",
            )
            parts.append(md_table(rows, ["part_type", "count"]))
        except Exception as exc:
            parts.append(f"(part type hist failed: {type(exc).__name__})")
        parts.append("")
        try:
            rows = hist(
                con,
                "SELECT COALESCE(json_extract(data,'$.role'), json_extract(data,'$.info.role'), '(null)'), COUNT(*) FROM message GROUP BY 1 ORDER BY 2 DESC",
            )
            parts.append("message role/type extract")
            parts.append("")
            parts.append(md_table(rows, ["role_or_type", "count"]))
        except Exception as exc:
            parts.append(f"(message role hist failed: {type(exc).__name__})")
        parts.append("")
        con.close()

    parts.append("")
    parts.append("## Kilo (this product CLI db)")
    parts.append("")
    json_type_hist(kilo_db, "part", "kilo.db")
    parts.append("## OpenCode")
    parts.append("")
    json_type_hist(oc_db, "part", "opencode.db")

    (REPORTS / "local-corpus.md").write_text("\n".join(parts) + "\n", encoding="utf-8")


WALK_TOOL_TYPES = {
    "custom_tool_call",
    "function_call",
    "tool_call",
    "mcp_tool_call",
    "custom_tool_call_output",
}


def walk_tools(obj: object, names: Counter[str], types: Counter[str], depth: int = 0) -> None:
    if depth > 12:
        return
    if isinstance(obj, dict):
        t = obj.get("type")
        if isinstance(t, str):
            types[t] += 1
            if t in WALK_TOOL_TYPES or "tool" in t.lower():
                name = obj.get("name")
                if isinstance(name, str) and 0 < len(name) < 80:
                    names[name] += 1
        for key, val in obj.items():
            if key in SKIP_KEYS:
                continue
            walk_tools(val, names, types, depth + 1)
    elif isinstance(obj, list):
        for item in obj[:200]:
            walk_tools(item, names, types, depth + 1)


def jsonl_histograms(limit_files: int | None = None) -> None:
    write_status("jsonl_histograms")
    dest_dir = DATA / "codex"
    files = sorted(dest_dir.glob("*.jsonl"))
    if limit_files:
        files = files[:limit_files]
    type_counts: Counter[str] = Counter()
    nested_types: Counter[str] = Counter()
    tool_names: Counter[str] = Counter()
    unknown_types: Counter[str] = Counter()
    bad_json = 0
    files_ok = 0
    lines_ok = 0
    known = {
        "session_meta",
        "event_msg",
        "response_item",
        "turn_context",
        "compacted",
        "world_state",
        "custom_tool_call",
        "event",
    }
    total = len(files)
    for i, path in enumerate(files, 1):
        write_status("jsonl_histograms", progress=f"{i}/{total}", files_ok=files_ok, lines_ok=lines_ok)
        try:
            with path.open("r", encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        bad_json += 1
                        continue
                    lines_ok += 1
                    t = obj.get("type") if isinstance(obj, dict) else None
                    if isinstance(t, str):
                        type_counts[t] += 1
                        if t not in known:
                            unknown_types[t] += 1
                    if isinstance(obj, dict):
                        payload = obj.get("payload")
                        walk_tools(payload if payload is not None else obj, tool_names, nested_types)
            files_ok += 1
        except OSError:
            continue
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Codex JSONL type/tool histograms",
        "",
        f"Generated: {utc_now()}",
        "",
        f"- hashed files scanned: **{files_ok}** / {total}",
        f"- lines parsed: **{lines_ok}**",
        f"- bad json lines: **{bad_json}**",
        "",
        "## top-level `type`",
        "",
        md_table([(k, v) for k, v in type_counts.most_common()], ["type", "count"]),
        "",
        "## unknown top-level types",
        "",
        md_table([(k, v) for k, v in unknown_types.most_common()], ["type", "count"])
        if unknown_types
        else "_none_",
        "",
        "## nested `type` (payload walk, skip body keys)",
        "",
        md_table([(k, v) for k, v in nested_types.most_common(40)], ["nested_type", "count"]),
        "",
        "## tool `name` (only when type looks like a tool call)",
        "",
        md_table([(k, v) for k, v in tool_names.most_common(60)], ["tool_name", "count"])
        if tool_names
        else "_none found in walk_",
        "",
    ]
    (REPORTS / "codex-jsonl-types.md").write_text("\n".join(lines), encoding="utf-8")


def contrast_stub() -> None:
    write_status("contrast_stub")
    src = REPORTS / "local-corpus.md"
    extra = REPORTS / "codex-jsonl-types.md"
    lines = [
        "# Contrast draft (Codex Work vs Kilo vs OpenCode)",
        "",
        f"Generated: {utc_now()}",
        "",
        "This is a measurement draft, not a claim that Kilo equals ChatGPT.",
        "",
        "See `reports/local-corpus.md` and `reports/codex-jsonl-types.md`.",
        "",
        "## What exists locally",
        "",
        "- **Codex/Work desktop** local rollouts + sqlite projections: large, classifiable without Cloud.",
        "- **OpenCode** `opencode.db`: real session/message/part corpus.",
        "- **Kilo (this product)** `kilo.db`: small but complete CLI sessions; `session_diff` is not the transcript.",
        "- **Kilo Code VS Code** `kilocode.kilo-code`: empty folder, not a corpus.",
        "- **ChatGPT.com Cloud**: not on disk. `thread_source=chatgpt_handoff` is rare. Official ZIP adapter stays dormant.",
        "- **Chromium / Brave / Store LocalState**: out of corpus.",
        "",
        "## How classification works (v0)",
        "",
        "Codex sqlite `thread_items.item_type` is the cheapest observe/plan/mutate proxy:",
        "",
        "| item_type | proxy |",
        "| --- | --- |",
        "| webSearch, imageView | observe |",
        "| plan | plan |",
        "| fileChange | mutate |",
        "| commandExecution | mixed (read vs write; needs later hashed-arg rules, not bodies in git) |",
        "| mcpToolCall, dynamicToolCall, collabAgentToolCall | skill/tool |",
        "| agentMessage, userMessage, reasoning | talk / think |",
        "",
        "Kilo/OpenCode: classify `part.data.type` from sqlite copies, not `session_diff` JSON.",
        "",
        "## Out of this campaign",
        "",
        "Harness patches that try to make Kilo/OpenCode as rigorous as Codex wait until a reviewed contrast exists.",
        "",
    ]
    if src.exists():
        lines.append("_local-corpus.md exists._")
    if extra.exists():
        lines.append("_codex-jsonl-types.md exists._")
    lines.append("")
    (REPORTS / "contrast-draft.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    started = time.time()
    write_status("start", argv=" ".join(sys.argv[1:]))
    try:
        DATA.mkdir(parents=True, exist_ok=True)
        REPORTS.mkdir(parents=True, exist_ok=True)
        result_copy = copy_hash_jsonl()
        write_status("copy_hash_done", **result_copy)
        sqlite_result = copy_sqlites()
        write_status("copy_sqlite_done", **{k: v.get("ok") if isinstance(v, dict) else v for k, v in sqlite_result.items()})
        sqlite_metrics()
        write_status("sqlite_metrics_done")
        jsonl_histograms()
        write_status("jsonl_histograms_done")
        contrast_stub()
        write_status(
            "complete",
            elapsed_s=int(time.time() - started),
            jsonl=result_copy,
        )
        return 0
    except Exception:
        STATUS.parent.mkdir(parents=True, exist_ok=True)
        err = traceback.format_exc()
        (ROOT / "research" / "overnight_error.txt").write_text(err, encoding="utf-8")
        write_status("error", error=err.splitlines()[-1] if err else "unknown")
        raise


if __name__ == "__main__":
    raise SystemExit(main())

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.score_session import summarize

lines = ["# Session scores vs Work-gold R1/R2/R5/R6", "", "No bodies. Work: never send first; apply_patch after exec-run 0; write-rate 0.01.", ""]
for name in ("kilo.db", "opencode.db"):
    db = ROOT / "data" / "raw" / "sqlite" / name
    if not db.is_file():
        lines.append(f"- missing {name}")
        continue
    out = summarize(db)
    lines.append(f"## {name}")
    lines.append("")
    lines.append(f"- sessions_with_tools: **{out['sessions_with_tools']}**")
    lines.append(f"- **Work-match (R1∧R2∧R3∧R4∧R5∧R6): {out.get('work_match', 0)}** / {out['sessions_with_tools']} ({out.get('work_match_rate', 0):.2f})")
    lines.append(f"- R1 look-first: **{out['r1_look_first']}**")
    lines.append(f"- R3 read-first (not bash): **{out.get('r3_read_first', 0)}** (Work first=exec 79, shell 2)")
    lines.append(f"- bash-first: **{out.get('bash_first', 0)}**")
    lines.append(f"- R2 no-write: **{out.get('r2_no_write', 0)}**")
    lines.append(f"- R5 no-write-after-look-run: **{out.get('r5_no_write_after_look_run', 0)}** (Work apply_patch after exec-run 0)")
    lines.append(f"- R4 no-todowrite: **{out.get('r4_no_todowrite', 0)}** (Work update_plan 0)")
    lines.append(f"- todowrite sessions: **{out.get('todowrite_sessions', 0)}**")
    lines.append(f"- wrote-without-task: **{out.get('wrote_without_task', 0)}**")
    lines.append(f"- R6 decompose-not-first: **{out.get('r6_decompose_not_first', 0)}**")
    lines.append(f"- decompose-first: **{out.get('decompose_first', 0)}**")
    lines.append(f"- write-rate: **{out.get('write_rate', 0):.2f}** (Work gold 1/87 ≈ 0.01)")
    lines.append(f"- write-first: **{out['write_first']}**")
    lines.append(f"- median start look-burst: **{out.get('median_start_look_burst')}** (Work exec-run median 3)")
    lines.append(f"- median tools before write: **{out.get('median_tools_before_write')}**")
    lines.append(f"- median tools before task/todo: **{out.get('median_tools_before_decompose')}** (Work send median 15)")
    lines.append(f"- skipped_study_os: **{out.get('skipped_study_os', 0)}**")
    lines.append(f"- wrote: **{out.get('wrote', 0)}**")
    lines.append(f"- sandwich look-after-write: **{out.get('sandwich_look_after_write', 0)}**")
    lines.append(f"- multi_piece (task/wait-ish, not todowrite): **{out.get('multi_piece', 0)}**")
    lines.append("")
    lines.append("| first | n |")
    lines.append("| --- | --- |")
    for k, v in out["firsts"]:
        lines.append(f"| {k} | {v} |")
    lines.append("")
    lines.append("| fail_mask | n |")
    lines.append("| --- | --- |")
    for k, v in out.get("fail_masks") or []:
        lines.append(f"| {k} | {v} |")
    lines.append("")
(ROOT / "reports" / "session-scores.md").write_text("\n".join(lines), encoding="utf-8")
print("wrote reports/session-scores.md")

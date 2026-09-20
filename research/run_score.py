import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.score_session import summarize

lines = ["# Session scores vs Work-gold R1 (look first)", "", "No bodies.", ""]
for name in ("kilo.db", "opencode.db"):
    db = ROOT / "data" / "raw" / "sqlite" / name
    if not db.is_file():
        lines.append(f"- missing {name}")
        continue
    out = summarize(db)
    lines.append(f"## {name}")
    lines.append("")
    lines.append(f"- sessions_with_tools: **{out['sessions_with_tools']}**")
    lines.append(f"- R1 look-first: **{out['r1_look_first']}**")
    lines.append(f"- write-first: **{out['write_first']}**")
    lines.append(f"- skipped_study_os: **{out.get('skipped_study_os', 0)}**")
    lines.append(f"- wrote: **{out.get('wrote', 0)}**")
    lines.append(f"- sandwich look-after-write: **{out.get('sandwich_look_after_write', 0)}**")
    lines.append(f"- multi_piece (task/todo/wait-ish): **{out.get('multi_piece', 0)}**")
    lines.append("")
    lines.append("| first | n |")
    lines.append("| --- | --- |")
    for k, v in out["firsts"]:
        lines.append(f"| {k} | {v} |")
    lines.append("")
(ROOT / "reports" / "session-scores.md").write_text("\n".join(lines), encoding="utf-8")
print("wrote reports/session-scores.md")

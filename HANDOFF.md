# Handoff

**Owner wins:** `AGENTS.md` → `PLAN.md` → `ISSUES.md` → `CONTINUE.md`.

## 48-hour no-stop

Until **2026-09-22T05:58:00Z**. Do not wait. Do not self-stop. Do not SWE-bench.

## Current

Gold loop on 1518 files: **`exec` is JS cells** (30044/30373), **`wait` is `cell_id`**, **`shell_command` is cwd shell**, edits sandwiched, spawn rare and named.

Spec + `.kilo/agent/codex.md` + `.opencode/agent/codex.md` updated so both products **imitate** that gold. Pytest must stay green.

Still open: error-then-look, plan-mode subset, measure live Kilo/OpenCode against the new mapping. `/goal` engine standing, not complete.

## Do not

Commit `data/` or bodies. Restart `codex_gold_analysis.py` only if the gold report is missing.

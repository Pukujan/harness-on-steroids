# 48-hour no-stop (owner)

Deadline: **2026-09-22T05:58:00Z** (48 hours from 2026-09-20T05:58:00Z).

**20-hour analysis floor:** do not stop the gold-analysis / imitate iteration before **2026-09-21T12:05:00Z** (20h from 2026-09-20T16:05Z). Fuzz, metamorphic, and differential tests must stay in CI. Recode interpretations into `reports/versions/`, do not only overwrite.

The owner ordered continuous work. Agents do not stop, wait for approval, ask for a “continue” message, or pause because a watchdog prompt is stale.

## If you would stop

You are wrong. Continue. Read `AGENTS.md` → `PLAN.md` → `ISSUES.md` → `HANDOFF.md`. Do the next open issue. Do not invent a new project.

## Allowed stop

Only the owner saying stop, or the clock past the deadline **and** issues 8–11 have modes + gold analysis. Until then: keep going.

## Work

Issue log order: finish gates 1–7 green, then 8 full Codex analysis, 9 spec, 10 Kilo mode, 11 OpenCode mode, 12 iteration loop. Codex transcripts are gold. Kilo and OpenCode imitate. No SWE-bench substitute.

After each slice: append `research/JOURNAL.md` (what/why/evidence). Occasional git commit+push of allowed files only (`data/` never).

## Wakeups

If fewer than two wakeups remain before the deadline, schedule more. Restart dead runners. Do not wait.

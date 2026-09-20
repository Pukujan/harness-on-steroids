# Activity journal

How this project actually proceeds. Append-only. No message bodies.

## Rules

- After a real slice of work: append a dated note here (what, why, evidence path).
- Occasional `git push` of specs, tests, reports, modes — never `data/` or transcripts.
- Standing `/goal` stays on the owner plan. Do not mark complete without `<<GOAL_LOOP_COMPLETE>>`.

## 2026-09-20

- Owner restated gold: local Codex/Work JSONL. Kilo + OpenCode imitate. No SWE-bench substitute. Durable in `AGENTS.md` / `PLAN.md`.
- Copy-hash 1518 jsonl into gitignored `data/raw/`. Counts-only reports under `reports/`.
- Gold interpretation v2/v3: `exec` is JS cells; `wait` is `cell_id`; `shell_command` is cwd shell; after fail look 446 vs patch 59. Snapshots in `reports/versions/v3/`.
- Owner-gate: properties, holdout, mutation, metamorphic, differential, CI contract, imitate modes, goal-loop, fuzz (`tests/test_goal_fuzz.py`).
- `/goal` engine `src/goal_loop.py` (Hermes/Codex semantics, rule judge + gates). CLI dest bug fixed. Done token `<<GOAL_LOOP_COMPLETE>>`.
- Modes: `.kilo/agent/codex.md`, `.opencode/agent/codex.md`.
- 20h analysis floor 2026-09-21T02:35Z plus 48h CONTINUE deadline 2026-09-22T05:58Z.
- Methods notes: `research/GOAL-MODE.md`, `research/PROVENANCE-METHODS.md`, `research/EXTERNAL-METHODS.md` (latter must not override owner gold).

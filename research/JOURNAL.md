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
- First push: `b3b7cd2` to `origin/main` (no `data/`). Journal + occasional push now part of CONTINUE/ISSUES.
- Prompt/context stack spec + tests (`spec/prompt-stack.md`, `tests/test_prompt_stack.py`). Spec snapshot `spec/versions/v3-codex-imitate-mode.md`. W3C PROV noted in PROVENANCE-METHODS (versioning/derivation, not RDF busywork).
- Originator split (`reports/codex-by-originator.md`): ChatGPT Work (`codex_work_desktop`, 93) is exec+wait+js+spawn, almost no apply_patch. `codex_vscode` (16) is the shell↔patch sandwich. Modes/spec now treat **Work as primary gold**. Snapshot `reports/versions/v4/`.
- Methods notes: `research/GOAL-MODE.md`, `research/PROVENANCE-METHODS.md`, `research/EXTERNAL-METHODS.md` (latter must not override owner gold).

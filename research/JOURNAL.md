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
- Work-only slice (`reports/codex-work-desktop-only.md`, v5): 85 sessions, apply_patch in 1, exec→exec 6998, multi-agent 26. Spec/tests lock this.
- Work-gold relations + scorer (`spec/work-gold-relations.md`, `src/score_session.py`). Kilo copy: 17/17 R1 look-first, 0 write-first. OpenCode: 76/77 look-first (Study OS noise).
- 20h loop reset to **2026-09-21T12:05Z**, goal max_turns 40, wakeups 4h/8h/20h. Scorer skips study-os: OpenCode 24 coding sessions, sandwich 12/13; Kilo sandwich 15/15.
- 10m wakeup chain. Work-only error-then-next scan running (`research/codex_work_errors.py`).
- Work-only errors: 5 fails, next=`shell_command` 4, no patch (`reports/codex-work-errors.md`). Stronger look-after-fail than mixed corpus.
- Methods notes: `research/GOAL-MODE.md`, `research/PROVENANCE-METHODS.md`, `research/EXTERNAL-METHODS.md` (latter must not override owner gold).
- v7 Work shapes (`research/codex_work_shapes.py`, `reports/codex-work-shapes.md`): 85 sessions, exec_only 33, multi_agent 27, exec_wait 16, patch 1. send_message never first (81/81). Median 15 tools before send. spawn_agent sessions 2. Scorer R2 no-write. Modes: never Task as tool 1; default look-only. Snapshot `reports/versions/v7/`.
- v8 R6 scorer: decompose-not-first (task/todowrite/agent_manager). Kilo 16/17 R6, write-rate still 0.88. OpenCode 16/24 R6, median tools before todo **0**. Modes: never Todowrite as tool 1. Snapshot `reports/versions/v8/`.
- v9 wait insertion (`research/codex_work_wait.py`): 361 exec-runs, median 3; after run wait 218 / send 53 / apply_patch **0**. Scorer R5 no-write-after-look-run. Kilo 2/17, OpenCode 12/24. Modes: do not Edit as next tool after look burst. Snapshot `reports/versions/v9/`.
- v10 js vs shell (`research/codex_work_js_shell.py`): exec 79 sessions / 7345 calls; js 5; shell_command **2** (1 with patch). Modes prefer Read/Grep/Glob. Synced global Kilo+OpenCode codex agents. Snapshot `reports/versions/v10/`.
- v11 wait clusters (`research/codex_work_wait_clusters.py`): 222 wait-runs, 18/31 sessions cluster ≥2; after wait-run exec 211. Modes: you may wait more than once. Snapshot `reports/versions/v11/`.
- v12 send topology (`research/codex_work_send.py`): send 25/85, median 2, first index 15; spawn 2; send+patch 0; after last send end 18. Spec task-split now Work send, not mixed-corpus spawn. Snapshot `reports/versions/v12/`.
- v13 Work plan (`research/codex_work_plan.py`): update_plan 0, request_user_input 0, plan-mode 0. Modes: do not Todowrite. Snapshot `reports/versions/v13/`.
- v14 R4 scorer `r4_no_todowrite`; todowrite dropped from multi_piece. Kilo 7/17 R4 (10 todo sessions), OpenCode 11/24. Snapshot `reports/versions/v14/`.
- v15 R3 read-first (not bash). Kilo 15/17, OpenCode 5/24 bash-first 10. Modes: do not bash as tool 1. Snapshot `reports/versions/v15/`.
- v16 work_match = R1∧R2∧R3∧R4∧R5∧R6. Kilo 1/17 (0.06), OpenCode 4/24 (0.17). Iteration loop metric. Snapshot `reports/versions/v16/`.
- v17 Work self-score (`research/score_work_gold.py`): mapped R1–R6 **79/81 (0.98)**. Confirms scorer. Snapshot `reports/versions/v17/`.
- v18 fail_mask on live copies. Kilo 10/17 R2+R4+R5. OpenCode bash-first stacks. Snapshot `reports/versions/v18/`.
- v19 corpus delta: 3 new hashed rollouts (2 Work exec-only, 1 Codex Desktop). Work 87. Self-score 81/83. Spec sandwich marked vscode. Snapshot `reports/versions/v19/`. Do not commit `data/`.
- v20 refreshed kilo/opencode sqlite copies. Kilo 20 sessions, work_match 1/20. Fail still R2+R4+R5. Codex mode not the scored agent. Snapshot `reports/versions/v20/`.
- v21 originator recount on 1521. Desktop 1106, work 95 files, vscode 16 (patch 718 unchanged). Snapshot `reports/versions/v21/`.
- v22 regenerated `codex-gold-behavior.md` on 1521 (lines 355679). 1518 snapshot kept. Explicit do-not-average-originators. Snapshot `reports/versions/v22/`.
- v23 deep pass restored: js_cell 29231 / 1521 files. Work still primary. Snapshot `reports/versions/v23/`.
- v24 empty Work sessions: 4/87, 14–25 lines, no calls. 95 originator rows ≠ 87 files. Snapshot `reports/versions/v24/`.
- v25 session_meta: 79×1 + 8×2 = 95. Modes: stop if nothing to look up. Snapshot `reports/versions/v25/`.

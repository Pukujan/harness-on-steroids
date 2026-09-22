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
- **2026-09-21T12:06Z** 20h floor elapsed. Gaps: `reports/20h-floor-gaps.md`. Issue 13 live replay + morphs still open. 48h continues.
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
- v26 originator files counted once: Work 87, Desktop 1103. Snapshot `reports/versions/v26/`.
- v27 gold-behavior originator table aligned to one-file-once (Work 87). Snapshot `reports/versions/v27/`.
- v28 ISSUES 8–11 done (analysis, spec, both modes). 12 in_progress: owner has not said match. Snapshot `reports/versions/v28/`.
- v29 `.kilo/command/goal.md` `agent: codex` like OpenCode. Snapshot `reports/versions/v29/`.
- v30 skip session.agent=plan. Kilo 7 skipped, 13 remain, work_match 1/13. No codex slug in sqlite yet. Snapshot `reports/versions/v30/`.
- v31 originator first-tool is call types only. Work first exec 81 / shell 2. Snapshot `reports/versions/v31/`.
- v32 mixed-corpus first-tool calls only: exec 1131, no create_thread. gold_analysis tool_name requires call types. Snapshot `reports/versions/v32/`.
- v33 empty-by-originator: 326/1521 no calls; codex_exec 210/315 empty; Work 4/87. Snapshot `reports/versions/v33/`.
- v34 empty codex_exec: 210/315, median 9 lines, messages+task_started. Not Work. Snapshot `reports/versions/v34/`.
- v35 nonempty exec vs Work: exec 31/105 patch vs Work 1/83. Snapshot `reports/versions/v35/`.
- v36 Desktop vs Work: Desktop patch in 1/994 nonempty files (186 calls in that one). Sandwich is vscode/exec, not Desktop. Snapshot `reports/versions/v36/`.
- v37 spec: sandwich is vscode + nonempty exec (31/105), not Desktop (1/994). Snapshot `reports/versions/v37/`.
- v38 live captions: Work first exec 81 / shell 2; R6 83/83. Snapshot `reports/versions/v38/`.
- v39 vscode vs Work: 12/13 nonempty vscode patch, all shell-first. Snapshot `reports/versions/v39/`.
- v40 patch-by-originator table: Work 1/83, Desktop 1/994, exec 31/105, vscode 12/13. Snapshot `reports/versions/v40/`.
- v41 spec table of those four rates. Snapshot `reports/versions/v41/`.
- v42 wait-by-originator: Work 31/83, vscode 0/13. Snapshot `reports/versions/v42/`.
- v43 send-by-originator: Work 25 send / 2 spawn; vscode 0/0. Snapshot `reports/versions/v43/`.
- v44 plan-by-originator: Work update_plan 0; exec 11; vscode 6. Snapshot `reports/versions/v44/`.
- v45 originator dashboard one-pager. Snapshot `reports/versions/v45/`.
- v46 HANDOFF/spec point at the dashboard as current gold. Compacted v-list. Snapshot `reports/versions/v46/`.
- v47 spec table expanded to patch/wait/send/plan. Full pytest green. Snapshot `reports/versions/v47/`.
- v48 shell-by-originator: Work 2/83, vscode 13/13, exec 45/105 (37 first). Snapshot `reports/versions/v48/`.
- v49 spec cwd-shell column. Snapshot `reports/versions/v49/`.
- v50 js-by-originator: Work 5/83, vscode 1/13. Snapshot `reports/versions/v50/`.
- v51 dashboard js column. Snapshot `reports/versions/v51/`.
- v52 spec js column. Snapshot `reports/versions/v52/`.
- v53 kilo.db refresh: still code/plan, no codex slug. Issue 12 notes updated. Snapshot `reports/versions/v53/`.
- v54 opencode.db: 153 sessions, no codex slug (build/luna/…). Snapshot `reports/versions/v54/`.
- v55 work_match by agent: kilo code 1/13; opencode build 3/19. Snapshot `reports/versions/v55/`.
- v56 fail_mask by coding agent. Kilo code R2+R4+R5=5. OpenCode build R2+R3+R4+R5=6. Snapshot `reports/versions/v56/`.
- v57 full pytest 90 green. ISSUES 12 points at agent rollups. Snapshot `reports/versions/v57/`.
- v58 matched-task eval spec + Work session index (87 hashes, counts only, no bodies). Replay not run. Snapshot `reports/versions/v58/`.
- v59 replay buckets from user_turn counts: 8 single-ask, 16 in 6–20, 6 long. No prompts. Snapshot `reports/versions/v59/`.
- v60 PLAN F + AGENTS: matched-task outcome is owner goal; process tests stay; replay not run. Snapshot `reports/versions/v60/`.
- v61 extract_replay.py + spec/matched-task-goal.md for owner `/goal`. Snapshot `reports/versions/v61/`.
- v62 primary exam is 22 long Work threads + morphs, not 8 singles. Snapshot `reports/versions/v62/`.
- v63 morph = stretch eval; 16 develop / 6 holdout; mutation+doc-holdout stay; modes say multi-turn. Snapshot `reports/versions/v63/`.
- v64 Work process scores for 22 hashes; kilo/opencode/morph pending. Snapshot `reports/versions/v64/`.
- Live develop Kilo replays in this worktree: most look-first fail_mask none; 6eb8 wrote (R2+R5). OpenCode scored on a few hashes. Morph files on several. Holdout not scored on copies yet.
- Human README: problem framing (harness not model), what we copied from Work, reproducibility, components, status, related research without SWE-bench-as-project.
- Kilo `/goal` 500: removed `.kilo/command/goal.md` (shadows reserved `/goal`). Fresh `GET /command` 200; live VS Code kilo still needs a window reload. Tests now forbid that file. CLI goal set to matched-task outcome (PLAN F / issue 13).
- v65 replay scorer from gitignored ndjson (utf-16/utf-8). Develop OpenCode copies: 1b09+b7e6 ran; 74841 scored; 633c timeout; morph files on all 16 develop. Morph *replays* still short. Holdout still pending. pytest replay tests green.
- OpenCode runner now streams JSON events to disk, one user turn per process, 180s cap. a584 one-turn ok (yes/none/partial). Develop OpenCode: 14/16 cells, 2 timeout. Do not bundle four hashes in one 30min tool call.
- Kept going: Zen/DeepSeek 402 no funds; OpenRouter glm-5.2:free has no tools; qwen3.8-27b:free scored 633c (10 tools) then rate-limit. 6eb8 text-only no/empty/no. Develop OpenCode 16/16 notes. Holdout started: 555f no/R3/partial, 45ca yes/none/partial, 55fd empty. 0aecd/1442/3a74 still pending. pytest replay-scores green.
- Holdout OpenCode one-turn notes: 55fd yes/none/partial, 3a74 yes/none/partial, 0aecd no/R3/partial, 1442 no/empty/no. Stop-when notes now present for 16+6 and ≥3 morph replays. Verification pytest green. Full original-workspace multi-turn still not done.
- Owner extend 20h + 10m wakeups. `.kilo/command/goal.md` stays deleted (Kilo reserved `/goal` 500). Zen `deepseek-v4-flash` was 402 no funds. OpenRouter free+tools ping: north-mini-code, dots-3-note, ling-3.0-flash-fin/sante/vl, lfm-2.5 (200 tools). Gemma free 429. Zen HTTP 403/1010 with .env key; CLI auth.json is separate. Used `openrouter/inclusionai/ling-3.0-flash-fin:free`: 1442 102 tools; 6eb8 39 tools look-first. reports/free-models-tools.md. Do not use glm-5.2:free for tools.
- Owner asked to run remaining matched-task. Blockers: 180s cap; isolated empty sandbox vs live original cwd (all 22 develop+holdout cwds still exist — do not `--auto` mutate them); Kilo CLI not on PATH. Runner gained `--turn`. Extra OpenCode turns (`ling-3.0-flash-fin:free`): 1a415 turn2+3 timeout 21→84 tools still yes/none/partial; 74841 turn2 timeout 24→26 still yes/none/partial; 8d42 turn2 **ok** 26→33 then write, cell no/R2+R5/partial. Rescored copies; pytest replay/matched/holdout green. Do not extra-turn pinned 6eb8/0d6c/2bde/0aecd/1442/1b09 rows.
- Chat-first vs no-stop: owner clarified CONTINUE is post-`/goal` only. Wrote it into project AGENTS.md / CONTINUE.md / HANDOFF.md / ISSUES.md, both Codex modes, spec, owner.v1 snippets, tests. Kilo global AGENTS.md + kilo.jsonc agent prompts (code/build/plan/general) override default personality. Synced global kilo/opencode codex agents. Restored accidental dirty `reports/codex-gold-behavior.md`. Owner-gate pytest green.
- Owner: put research/planning/provenance/compacted/checkpoints into the plan, not chat. PLAN G–I, ISSUES 14–17, `spec/work-research-gates.md`, CI test. Measurement not run. Do not treat the chat as the project.
- Foundation: `spec/repo-modules.md`, `research/work-ux-gaps.md`, `spec/combined-slices-goal.md` (not started), `src/hos/` facade, ruff+mypy in pyproject, issue 18, tests/test_repo_modules.py. Combined `/goal` not launched.
- Issue 13 stop-when notes rechecked from copies (no bodies): develop 16 and holdout 6 all have OpenCode tool seqs. Morph *replays with tools* now 3: `0d6ca4607eaf` (12, timeout, todowrite+bash), `2bde00530ddd` (29), `6e412585c223` (29). File-only morphs are not extra evidence. Rescored copies; replay-scores table unchanged. Verification pytest green. Did not `--auto` original Work cwds. Did not start combined-slices. Issues 14–18 still queued. Full original-cwd multi-turn still not done.

## 2026-09-21 — harness-agnostic planning reset

- Read the issue log, owner plan, handoff, research status/journal, UX gaps, research/provenance gates, module map, matched-task specs/reports, source scorer/goal code, and test contracts.
- Added the proposal package under `spec/harness-agnostic/`. It treats Kilo/OpenCode as adapters and expands the target to Pi and future harnesses through a portable behavior protocol, evidence/lineage plane, UX and behavior research, action-plan/execution/verification, recovery/continuity, capability negotiation, and outcome gates.
- No implementation, prompt rewrite, replay execution, cleanup, or raw transcript/body export was performed. Existing code and issues remain preserved as historical/prototype state pending owner review.

- Reviewed the full harness-agnostic package against AGENTS/PLAN/ISSUES/HANDOFF, UX/research gates, module map, matched-task eval, and current replay state. Added `spec/harness-agnostic/11-owner-review.md` and resolved all ten owner decision questions into recommended planning defaults in `10-owner-decisions-and-handoff.md`.
- Planning amendments only: protocol now requires run/task-graph/attempt hierarchy and explicit terminal states; adapters require persisted capability negotiation; evaluation freezes acceptance/environment/model strata before tuning; new derived identifiers get a privacy-safe rule. No prompts, adapters, replay, cleanup, or runtime code changed.
- Issue 19 moved to in_progress: architecture review is complete, but owner acceptance and the source-of-truth governance switch remain pending before any implementation or `/goal`.

## 2026-09-21 — owner accepts model/harness-agnostic fast-loop direction

- Owner accepted the architecture reset with a simpler operating contract: rich Work/Codex observable behavior is reference evidence; the project is model- and harness-agnostic.
- Normal development surfaces are Pi + OpenCode + Grok Build in the same slice where technically possible. Exact model/provider/harness/control versions are recorded; same-model parity is useful but optional.
- Kilo Codex v0, R1–R6, 22-thread replay/morph work, and existing reports remain positive-control/history rather than the active product boundary.
- Prompt/context/capability/checkpoint control comes first. A general runtime state machine is not required; narrow enforcement must be earned by repeated measured failure and a successful experiment.
- Fast-loop invariant: one main behavior hypothesis, smallest intervention, automatic multi-harness rerun, visible result, keep/revert/refine. No substantial architecture-only slice.
- GitHub/repository continuity is authoritative. Created GitHub issue #2 for the first baseline and checkpoints/CURRENT.md for exact next action.
- Governance switch targets owner spec v2; v1 remains historical. Raw/private transcript/account data remains local.


- v66 replay prompt hygiene: runners fed `user_turns()[0]`, which in Work transcripts is the `<recommended_plugins>`/`<environment_context>` preamble. Over 22 develop+holdout hashes, 19 turn-1s carry a context block and **11 are context-only**, so those replays ran with **no owner ask**. Consequence: every prior baseline-vs-Jev cell is confounded — baseline got boilerplate (0 tool calls on all three adapters) while the Jev arm's directive was its only actionable text (Pi up to 306 calls). That measures instruction-present vs absent, not routing. Fix: `strip_context_blocks`/`first_ask`/`ask_turns` in `research/replay_lib.py` (`user_turns` keeps raw shape for counts/old tables), both runners use the real ask and record `ask_present`/`ask_shifted`; `--turn N` keeps raw indices and returns `empty-ask` rather than running boilerplate; `build_initial_state` reports `user_request_missing` + `user_input_required` instead of claiming a request. New gate `tests/test_replay_prompt_hygiene.py`; also wired `test_jev_controller_module.py` into owner-gate (it existed but was never in CI) and fixed `src/hos/__init__.py` import order that broke `ruff check src`. Banner added to `reports/jev-controller-pilot.md`; snapshot `reports/versions/v66/`. Full pytest green. **Set not re-run yet: no valid controller comparison exists.** Did not commit `data/` or bodies.
- v66 re-run (first valid controller rows): `replay-fix-20260922` OpenCode/Qwen, 150s, real ask in both arms. `0d6ca4607eaf` (ask_shifted, previously boilerplate-only) baseline **ok/6 tools** where the pre-fix arm logged 0 — the signature of the fixed prompt, not of routing. Control `1a415bc257e5` baseline ok/0, Jev 14. Both Jev rows timed out at the cap; one raised tool count, one did not; no work-match gain established. Two tasks = smoke test only. Table added to `reports/jev-controller-pilot.md` under "First valid comparison"; pre-fix cells stay under the invalid banner. Gates green (pytest 134, ruff/mypy `src`). No bodies or prompts committed.
- v66 blast radius beyond the controller: the same first-turn bug is in the long-running OpenCode replay path, so `reports/replay-scores.md`'s **opencode column is prompt-contaminated for 11 of 22 hashes** (`0d6ca4607eaf`, `28372e365066`, `2bde00530ddd`, `6e412585c223`, `8d42bc26b8ea`, `b7e6393f4c14`, `bd179678f540`, `f37de8488162`, `1442d08cf2d3`, `555f9c94ba8e`, `55fd1ef9b613`) — all 11 have ndjson with 2–102 calls, so cells look healthy but the prompt had no ask; extra `-c` turns can carry a real ask later, which masks it. Rows **not** rewritten: `tests/test_replay_scores.py` pins those exact cells and mandatory owner-gate tests are not edited to hide a defect. Additive "prompt-contaminated" section + `test_replay_scores_flags_contaminated_opencode_cells` fails if a context-only hash goes unflagged. Work column (own JSONL) and Kilo column (sqlite copies) unaffected. Issue 13's OpenCode evidence stays **open** for those 11. Gates green.

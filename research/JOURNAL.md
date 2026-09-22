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

## 2026-09-21 — Jev Controller v2 approved for implementation

- Researched TypeSafe's official System One documentation and OpenRouter's Jev
  integration. Jev evaluates supplied state against typed Choice, Score, and
  Noul questions; it does not replace the coding-agent LLM, call tools, write
  code, or hold a conversational session.
- Corrected the controller hypothesis: Jev should receive the full relevant
  decision context, including the owner ask, relevant conversation, adapter
  events, repository facts, open beads, candidate work, and verification
  evidence. The harness owns the repeated context-update loop.
- Durable records added: `research/jev-controller-v2-research.md`,
  `spec/jev-controller-v2.md`, `docs/jev-controller-v2-runbook.md`, and
  Issue 21 in `ISSUES.md`. `HANDOFF.md` and `checkpoints/CURRENT.md` now point
  the next session at v2 implementation.
- The old three-harness Jev run remains v1 smoke evidence only. The next code
  slice is a fake-adapter-tested `DecisionContext`/`JevDecisionLoop`, followed
  by OpenCode, Grok Build, and Pi adapter audits and a fresh matched replay.
- v66 re-run (first valid controller rows): `replay-fix-20260922` OpenCode/Qwen, 150s, real ask in both arms. `0d6ca4607eaf` (ask_shifted, previously boilerplate-only) baseline **ok/6 tools** where the pre-fix arm logged 0 — the signature of the fixed prompt, not of routing. Control `1a415bc257e5` baseline ok/0, Jev 14. Both Jev rows timed out at the cap; one raised tool count, one did not; no work-match gain established. Two tasks = smoke test only. Table added to `reports/jev-controller-pilot.md` under "First valid comparison"; pre-fix cells stay under the invalid banner. Gates green (pytest 134, ruff/mypy `src`). No bodies or prompts committed.
- v66 blast radius beyond the controller: the same first-turn bug is in the long-running OpenCode replay path, so `reports/replay-scores.md`'s **opencode column is prompt-contaminated for 11 of 22 hashes** (`0d6ca4607eaf`, `28372e365066`, `2bde00530ddd`, `6e412585c223`, `8d42bc26b8ea`, `b7e6393f4c14`, `bd179678f540`, `f37de8488162`, `1442d08cf2d3`, `555f9c94ba8e`, `55fd1ef9b613`) — all 11 have ndjson with 2–102 calls, so cells look healthy but the prompt had no ask; extra `-c` turns can carry a real ask later, which masks it. Rows **not** rewritten: `tests/test_replay_scores.py` pins those exact cells and mandatory owner-gate tests are not edited to hide a defect. Additive "prompt-contaminated" section + `test_replay_scores_flags_contaminated_opencode_cells` fails if a context-only hash goes unflagged. Work column (own JSONL) and Kilo column (sqlite copies) unaffected. OpenCode evidence stays **open** for those 11. Gates green. NOTE (post-rebase): the owner's harness-agnostic reset renumbered ISSUES.md, so the local '### 19' added here was dropped during conflict resolution and the blocker now lives under active GitHub issue #2; the v0 no-stop governance block was deliberately NOT re-added over the owner's rewritten chat-first section.

## 2026-09-21 — Jev v2 first implementation and matched slice

- Added `DecisionContext`, typed Choice/Score/Noul request construction and
  parsing, phase/action legality checks, explicit fallback, and the bounded
  repeated `JevDecisionLoop` while preserving the v1 pilot APIs.
- Added normalized adapter event/session metadata extraction and fake tests
  proving three context-aware decisions, observation folding, and no adapter
  execution after an unavailable or low-confidence decision.
- The live OpenRouter probe initially returned schema errors; the provider
  response identified `criteria` as the required question field, and Score/Noul
  answer shapes were captured and tested. No provider credentials or response
  bodies were committed.
- Fresh three-development-hash replay across OpenCode, Grok Build, and Pi:
  baseline timed out 7/9 arms; Jev stopped 6/9 arms on low action confidence;
  the remaining three adapter loops made two decisions each but timed out, and
  no arm reached a Work match. OpenCode emitted a native session identifier;
  Grok Build and Pi did not. This single repetition does not establish
  variance. Report: `reports/matched-replay-jev-v2-20260921.md`.
- At the time of the first implementation slice, the selected next hypothesis
  was to remove `CLASSIFY_REQUEST` from the intake next-action choices and
  prefer evidence-producing inspection. The later public-OSS review below
  supersedes that as the immediate next experiment because the feeder context
  was not populated.

## 2026-09-21 — public Jev ecosystem evidence corrects the feeder boundary

- Reviewed public Jev integrations rather than inferring behavior from our
  prototype. The strongest live-agent example found was
  `browser-use/jev-ultrafast` (16.0k GitHub stars when checked): a host turns
  browser observations into an indexed element table and recent-action state,
  sends compatible operation/target choices to Jev, executes the validated
  result, and observes again.
- TypeSafe's public browser-agent and tool-router examples show the same
  contract: the host supplies live state and a closed permitted candidate set;
  Jev chooses within that set; the host validates, executes, and feeds the next
  observation back. Jev has no file-system, browser, tool, or subagent
  authority.
- Our v2 replay supplied the owner ask, one synthetic `task-main` bead, the
  intake action catalog, generic constraints, and mostly empty context fields.
  It did not run a context-producing inspection worker or supply real file
  excerpts, repository facts, candidate beads, or test evidence before the
  first decision. The loop mechanics were tested, but not live
  observation-derived action selection.
- Durable detail is in `research/jev-ecosystem-evidence.md` and the expanded
  `research/jev-controller-v2-research.md`. The next experiment is revised to
  add the smallest bounded context-feeder preflight while holding Jev schema,
  threshold, and adapters constant; the earlier `CLASSIFY_REQUEST` choice-set
  change is paused until that feeder exists.

## 2026-09-21 — owner authorizes 60-turn matched Jev A/B

- The next experiment is now Issue 22, not another context-poor Jev smoke
  run: 60 matched Work-derived development user turns per arm and available
  harness, preserving per-hash long-running context.
- Arm A receives the shared context-feeder pack and no Jev decision. Arm B
  receives the identical pack, then one validated Jev action choice. OpenCode
  and Pi currently use `yolo-auto/qwen3.8-flash`; Grok Build uses `grok-4.7`;
  Jev remains a separate `typesafe/jev-1.13` OpenRouter call.
- The local ChatGPT Work/Codex corpus remains the behavioral gold/reference;
  the 16 development hashes are tunable fixtures and the six holdout hashes
  remain sealed. R1-R6 and the existing taxonomy are diagnostic signals,
  supplemented by verification, provenance, continuity, outcome, and honest
  reporting measures.

## 2026-09-22 — long A/B launch blocker: prompt must not travel in argv

The first context-fed long A/B runs (`jev-long-smoke-seed-20260922`,
`jev-long-ab-20260922-pi`) showed many `fail_1` cells at 0 tools with empty
events. Diagnosis: the Pi and OpenCode adapters passed the whole context-pack
prompt as a command-line argument, and Windows aborted the process with "The
command line is too long" before the harness started. Dead cells therefore
measured a launch failure, not model behavior — the same contamination class as
the pre-v66 task-free prompts. The `git archive` seed materialization itself
worked, and turns that did launch showed the harness working (33-68 tools/task,
including a real baseline Work-match).

Control-layer fix, held the decision loop/schema/fixtures constant: adapters now
deliver the prompt over stdin (Pi/OpenCode) and keep Grok on `--prompt-file`;
the prompt no longer appears in argv, and a harness that dies before draining
stdin no longer raises a spurious launch_error. Two regression tests pin that the
prompt is absent from argv and that a 40k-char prompt is delivered over a pipe
with zero positional args. All 152 tests and ruff pass; a real Pi call with a
40k-char prompt returns status ok with events and no "too long". Both affected
reports are flagged launch-blocked. Next action: one fresh matched A/B slice on
the frozen development hashes under a new run_id; do not compare new cells to the
launch-blocked runs.

## 2026-09-22 — clean Jev long-horizon A/B result

- Completed the frozen Issue 22 matrix after fixing the Windows prompt transport
  blocker. OpenCode, Grok Build, and Pi each received 60 matched
  Work-derived development turns per arm across the same 16 development
  hashes; the six holdout hashes stayed sealed. The shared deterministic
  repository feeder, isolated seed, harness timeout, and model were held
  constant between arms.
- Recorded model/config provenance: OpenCode and Pi used
  `yolo-auto/qwen3.8-flash`, Grok Build used `grok-4.7`, and Jev used
  `typesafe/jev-1.13` through OpenRouter Decisions API. Each result has 60
  turns, 16 hashes, 120 rows, and zero `fail_1` transport rows.
- Aggregate Work-match: OpenCode baseline 8/16 versus Jev 4/16; Grok Build
  baseline 0/16 versus Jev 0/16; Pi baseline 0/16 versus Jev 0/16. Jev
  executed only 13, 13, and 12 turns respectively because 47, 47, and 48
  decisions failed the 0.55 confidence gate. Mean Jev confidence was 0.419,
  0.409, and 0.390.
- This is a negative promotion result for the current policy, not evidence
  that Jev can never help. The feeder supplied bounded repository facts,
  changed paths, redacted excerpts, and candidate beads; Jev still had no
  filesystem, shell, tool, or subagent authority. The strongest observed
  failure is confidence-gate under-execution, which makes the Jev arm
  incomparable as a coding-capability intervention unless low-confidence
  fallback remains executable.
- Durable report: `reports/jev-long-ab-20260922.md`, with detailed
  hash-only reports for each harness. Exactly one next hypothesis is retained:
  keep the feeder/choices/models/fixtures/timeouts fixed, execute the
  baseline-equivalent feeder prompt on low-confidence Jev decisions while
  recording Jev as advisory, and rerun one fresh 60-turn development slice.

## 2026-09-22 — Jev OSS architecture deep dive

- Inspected source and architecture documentation for Jev Ultrafast,
  Stanley, JevWire, pi-jev, pi-typesafe, pi-jev-tools, TypeSafe Router, and
  the TypeSafe playground. Upstream `main` commit hashes and direct source
  links are recorded in `research/jev-oss-architecture-deep-dive-20260922.md`.
- The common architecture is host observation -> bounded evidence and closed
  candidates -> typed Jev decision -> host validation/policy -> execution or
  abstention -> independent verification -> refreshed observation. Jev does
  not read files, discover project direction, or execute actions by itself.
- Stanley is the closest coding-agent reference: deterministic workflow
  registry and availability gates, exact checks before Jev, bounded hunk-level
  questions, code-owned thresholds, `cannot_tell`/`notChecked`, and an
  explicitly unverified Pi fallback for unsupported requests.
- Jev Ultrafast contributes the strongest freshness pattern: code-owned
  candidate IDs, state fingerprints, revalidation immediately before action,
  and independent verification of `DONE`. JevWire contributes a provider-
  neutral decision contract and whole-response validation. pi-jev-tools shows
  local retrieval and provenance before Jev ranking. pi-jev shows how an
  explicit state can route to a separate worker/scout/reviewer workflow.
- This comparison exposed the exact remaining context gap in our own slice:
  the feeder does not automatically read `CURRENT.md`, `HANDOFF.md`,
  `ISSUES.md`, or the active issue body; its four candidate beads are generic
  placeholders. That is a research finding, not an implementation change.
- Reuse decision: port patterns first, and only copy code from confirmed MIT
  repositories after commit/dependency/license review. Do not add a general
  orchestration framework. Keep the authorized next experiment unchanged:
  make low-confidence Jev advisory and rerun the matched slice.

## 2026-09-22 — Jev classification versus data capture

- A source-backed follow-up separates Jev's useful role from the host's capture
  role. TypeSafe's System One documentation and public Jev integrations show
  Jev evaluating host-supplied state and returning typed choices/scores; the
  host observes files or browser state, bounds candidates, validates freshness
  and policy, executes, verifies, and records the trajectory.
- Jev therefore remains a candidate for bounded classification, scoring, and
  routing, including advisory post-hoc labeling of a frozen event sample. It
  is not suitable as the source of truth for transcript capture, repository
  observation, provenance, authorization, execution, or verification.
- Our Issue 22 A/B confirms that the feeder, not Jev, captured repository
  context. It also shows that the current controller policy is not promoted:
  Jev executed only 13/13/12 of 60 turns after 47/47/48 low-confidence
  fallbacks, and OpenCode Work-match fell from 8/16 to 4/16. The report
  `research/jev-classification-capture-20260922.md` records the distinction
  and keeps the controller follow-up separate from the analytical-machine
  annotation work.

## 2026-09-22 — analytical machine v0 begins

- The corpus is now treated as two analysis lanes: Codex execution and
  ChatGPT chat/research. They share a body-minimized evidence contract but
  use separate analyzers and quality dimensions.
- Added `src/hos/analysis_machine/` and its durable plan
  `docs/analytical-machine-v0-plan.md`. The first slice normalizes imported
  Codex envelope JSONL and existing ChatGPT provenance message/tool-event
  JSONL, then exports versioned events and summaries without transcript bodies.
- Sol reviewed the proposed slice through the local bounded CKFF worker. Its
  main warning is durable: deterministic output can still be misleading unless
  source identity, duplicate policy, missing-data status, provenance coverage,
  ontology version, analyzer version, and alias-map behavior are explicit.
- Focused tests passed for both lanes, contract validation, event-order
  invariance, unknown-field resistance, tool-alias invariance, and body
  minimization. The first real pilot used one Codex session and one ChatGPT
  provenance conversation: 5,525 events across three episodes, zero parse
  errors, zero validation issues, and 100% known-event coverage. A repeat run
  produced byte-identical export hashes.

## 2026-09-22 — analytical machine full structural pass and provider boundary

- The streaming machine (`analysis-machine/0.2.0`, codebook
  `analysis-codebook/0.1.1`) processed 2,173 local JSONL sources into 556,241
  body-minimized events across 1,499 episodes: 419,893 Codex events in 1,387
  episodes and 136,348 ChatGPT events in 112 episodes.
- The corrected adapter carries Codex session identity across records, keeps
  repeated citation rows distinct using structural field/pointer identity,
  emits bounded parse-error events for malformed records, and includes a
  dataset fingerprint in run identity. Exact duplicate tracking with a
  600,000-ID cap found zero duplicate IDs and zero validation issues. 28,565
  events remained unknown and zero parse errors were observed.
- Structural observations include 53,183 Codex tool calls, 53,190 tool
  results, 45 mutation-action episodes, 3 inspection-action-before-mutation-
  action episodes, zero qualifying verification-action-after-mutation-action
  episodes, 285 delegation events, and
  318 compactions. ChatGPT includes 2,430 user messages, 7,144 assistant
  messages, 30,084 citation rows, 100/112 citation-presence episodes, 34,584
  code events, and 2,163 execution-output events. These are adapter-defined
  observations, not quality or intent judgments; the corrected adapter now
  reports 5,244 research-family events from explicit source-retrieval tool
  names such as `web.run`, while citation presence remains separate.
- Three native Luna subagents performed independent read-only reviews of the
  aggregate, ontology/codebook, and streaming implementation. They exposed
  the session-carry, citation-identity, malformed-record, run-ID, and
  denominator issues that were fixed before the final v6/v7 pass. Their suggestions remain
  advisory and are not gold annotations.
- Provider routing is explicit and durable: Sol is allowed only through the
  CKFF Sol worker; Luna is allowed only through native Codex/ChatGPT subagent
  spawning and is never allowed through CKFF. An unavailable provider arm must
  be recorded, not silently replaced.
- The committed interpretations are
  `reports/analysis-machine-full-corpus-20260922.md` and
  `research/analysis-ontology-pilot-20260922.md`. The pilot is now frozen and
  adjudicated with two independent native Luna reviews; no category is
  promoted to accepted. Two fresh native Luna holdout reviews agreed on
  citation, research, unclassified-event, and abstention labels; one
  action-versus-evidence disagreement was adjudicated as `not_applicable`.
  The next action is a larger lane-balanced sample for owner/human
  adjudication before accepting quality, UX, provenance-correctness, planning,
  or outcome labels.

## 2026-09-22 — larger ontology pilot and advisory review

- The deterministic selector produced a new 24-episode pilot (12 Codex, 12
  ChatGPT; 8,930 body-free events) and an eight-episode sealed holdout (3,231
  events). Four independent native Luna reviews covered the pilot only, two
  per lane, with no CKFF/Sol, raw corpus, web, or repository edits.
- The canonical reference counts are 2,559 Codex events and 6,371 ChatGPT
  events. Structural pilot observations are 2 Codex episodes with an observed
  inspect action, 1 with 17 mutation actions, 0 with verification actions,
  10/12 ChatGPT episodes with citations, 9/12 with explicit research-family
  events, 5/12 with code attributes, and 1/12 with execution-output
  attributes.
- The reviews were useful but not gold: one reviewer misreported the ChatGPT
  total as 4,371 and reviewers inconsistently treated explicit code/output
  attributes and research-family events. The durable adjudication is in
  `research/analysis-ontology-pilot-v3-review-20260922.md`; no quality,
  planning, UX, provenance-correctness, or outcome labels were promoted.
- Added `research/build_analysis_review_packet.py`, a deterministic packet
  builder that emits one body-free source-linked episode record per line with
  empty owner-adjudication fields. It rejects holdout input and body-bearing
  fields; the v3 packet was generated locally with 24 episodes and 8,930
  events. This is a review aid, not an annotation platform or gold-label
  generator.

## 2026-09-22 — first live Jev structural annotation probe

- `research/run_jev_shadow_annotation.py` sent a deterministic eight-event
  sample from the v3 pilot to `typesafe/jev-1.13` through the OpenRouter
  Decisions API. It asked eight independent binary structural questions per
  event using canonical body-free fields; the holdout remained sealed and no
  raw response was written.
- All 64 probabilities were valid. At `p >= 0.50`, Jev matched direct
  canonical-field labels 62/64 (96.875%) with one research false positive and
  one mutation false negative. At a two-sided 0.75 acceptance band, 59/64
  predictions were accepted with zero errors and five abstentions.
- This supports a fast bounded annotation sidecar, not a quality claim. Noul
  returned probability values but no separate confidence field in this run,
  so probability was treated as the score. The durable report is
  `reports/jev-shadow-annotation-20260922.md`; owner/human semantic
  adjudication and a larger repeated study remain required.

# harness-on-steroids - owner instructions

**The user owns this project. Agents do not.** If an older plan, proposal, mode prompt, issue note, or prior agent disagrees with this file or PLAN.md, this file and PLAN.md win.

Read in this order:

1. AGENTS.md
2. PLAN.md
3. checkpoints/CURRENT.md
4. the active GitHub issue named by CURRENT.md
5. HANDOFF.md
6. ISSUES.md

Before changing README, marketing, UX, image, or HTML content, also read .content-system/system-version.json and the relevant .content-system files.

## What this project is

ChatGPT Work / Codex transcripts are reference evidence for observable agent behavior. The long-term target is **model- and harness-agnostic** control: learn useful observable behavior from that corpus and transfer it across coding-agent harnesses without requiring the same model, tool names, prose, or exact trajectory.

The reference is richer than tool order. Measure interaction shape, inspection and research, waits, delegation, tool calls and results, verification, provenance, output behavior, corrections, continuity/context management, terminal status, task outcome, and repeated-run variance when those signals are observable.

Do not infer hidden chain-of-thought. Do not turn an unobserved signal into a fact.

## Active development surfaces

Pi, OpenCode, and Grok Build run in the same development slice when technically possible. Record the exact harness version, model/provider, control version, environment fidelity, and run attempt.

The project is model-agnostic. Using the same model across harnesses is a useful isolation test when convenient, not a requirement for normal iteration.

Kilo Codex v0 is a positive-control baseline. The existing Kilo/OpenCode Codex prompts, R1-R6 scorer, 22-thread replay work, morphs, and reports are valuable historical/prototype evidence. They do not define the future product boundary.

## Control-layer rule

Prompt/context control is the first intervention. Prefer the smallest change to behavior instructions, context composition, capability/tool presentation, continuation/checkpoint context, or adapter lowering that tests one hypothesis.

State-machine enforcement is earned, not assumed. Semantic phase/state labels are useful for normalization and scoring. Add runtime state or guards only when repeated evidence across tasks/harnesses shows that prompt/context control is insufficient, and keep the guard only if measured behavior or outcomes improve.

Do not pre-build a general orchestration framework, event platform, graph database, or full protocol implementation merely because a proposal names one.

## Fast empirical loop - mandatory

Every active implementation slice should normally contain one main behavior hypothesis:

1. choose a small set of existing representative Work-derived tasks;
2. run Pi + OpenCode + Grok Build in the same slice where possible;
3. capture the complete observable trajectory and outcome;
4. compare automatically against reference evidence and the previous control version;
5. make the smallest control-layer change;
6. rerun;
7. keep, revert, or refine from the measured result.

A substantial slice must produce a measured reference signal, an automated evaluation capability, or an observable behavior/outcome result. Architecture-only progress is not enough.

Use repeated generations and morphs when they answer a concrete robustness question. Behavioral variance is itself a signal: a strong control layer should make desirable behavior more stable across models, harnesses, and reruns.

## Evaluation

Tool order is diagnostic, not the goal. R1-R6 remain a historical/cheap process layer.

Evaluate the complete observable trajectory where available:

- interaction and user-turn handling;
- inspect/research sufficiency;
- native actions, waits, failures, retries, and delegation;
- verification after material changes or uncertain results;
- provenance/evidence supporting consequential claims;
- output behavior, uncertainty, partial/blocked/complete honesty;
- continuity across long tasks, corrections, interruption, or compaction;
- observable task outcome and forbidden side effects;
- repeated-run deviation.

Equivalent tools, wording, decomposition, and implementations may pass when they satisfy the same task and behavioral obligations.

## Scope control

Large destination, tiny verified steps.

- GitHub Issues are the active work graph. Keep only a small number of active experimental issues.
- Do not pre-create a speculative 50-step implementation backlog.
- Do not change the evaluator to rescue a disappointing candidate result.
- Freeze task fixtures/acceptance criteria before tuning on them.
- Holdout/morph boundaries stay sealed during tuning.
- Do not promote a process improvement that harms outcome, verification, safety, or truthful reporting.
- Preserve the working prompt-only baseline so added machinery must demonstrate value beyond it.

## Durable continuity

Do not treat the chat as project memory. GitHub and the repository are authoritative.

checkpoints/CURRENT.md names the active issue, current hypothesis/baseline, last verified result, and exact next action. Update it after a real slice. GitHub Issues hold executable experiments and their acceptance criteria. research/JOURNAL.md remains an append-only research trail; it is not source-of-truth state.

## Windows workspace, runtime, and cleanup policy

- On this host, `D:\claude\harness-on-steroids` is the canonical checkout and stays on D:. Use that checkout for routine work; do not create Codex-managed C: worktrees for this repository. Codex's managed-worktree root is app/user-level, not configurable by this repository's instructions, so select **current checkout** in Codex unless a verified D:-resident isolation path is available.
- Create an isolated worktree only for a concrete safety or parallelism need, and only when its actual location is on D:. Keep at most one temporary HOS worktree per active task. After verification, publish durable non-private changes, update the canonical D: checkout after merge, and retire the temporary worktree. Preserve or archive every dirty/unpushed change before retiring it; never clean another repository's worktrees under this rule.
- HOS Windows experiments use the single pinned portable OpenCode executable installed by `tools/install-opencode.ps1` at `.tools/opencode/opencode.exe`. Do not use an NVM/PATH OpenCode fallback, install OpenCode globally, or install it separately in a task workspace.
- OpenCode config, its generated plugin dependency tree, data, cache, state, and temporary files for HOS runs belong in the single ignored `.harness-cache/opencode/` directory on D:. The adapter stages tracked `.opencode/agent` and `.opencode/command` there. Per-task workspaces must exclude `.opencode`, `node_modules`, and `.venv`; do not copy or recreate these dependencies per task/run.
- Controller-run outputs default to the ignored `.controller-runs/` directory in the D: checkout. Raw prompts, traces, account data, credentials, and reproducible dependency trees are not committed. Only the shared plugin dependency tree may be regenerated, once, for the pinned runtime; remove it when reclaiming space, and do not remove shared runtimes owned by other projects.
- A pushed-but-unmerged branch is still durable work, not grounds to discard its checkout; retire a task worktree only after its changes are merged or explicitly archived. The checkpoint policy below governs when publishable changes must be pushed.

## Checkpoint publication and merge gate

- A checkpoint is a verified implementation or research slice with an issue-linked result and an updated `checkpoints/CURRENT.md`. Commit and push each completed, publishable checkpoint to its issue branch and open/update its pull request in the same work session. Do not accumulate multiple completed checkpoints locally; publish before pausing, handing off, or retiring a worktree, and at least once per active workday when publishable changes exist.
- Every checkpoint intended for the project must merge to `main` through a pull request before the next independent slice begins. `main` is protected: direct pushes and force pushes are disabled, and admin bypass is disabled. The merge is blocked until the branch is current and the required `lint`, `typecheck`, `tests`, `windows-tests`, and `checkpoint-record` checks pass.
- The required `checkpoint-record` check rejects a pull request unless it changes `checkpoints/CURRENT.md`. Keep the GitHub issue and PR aligned with the checkpoint; the PR template records the issue and verification.
- Never publish raw transcripts, prompts, account data, credentials, `.env` files, or private/reversible identifiers to satisfy cadence. Record only a safe redacted status when an artifact cannot be committed.

## Existing code and history

The old code is disposable; evidence and lessons are not.

Do not mass-delete or move v0 files merely for cleanliness. Git history already preserves them. Keep the current Codex-mode implementation and replay/scoring artifacts available as v0 baseline/history until a measured replacement exists. Relocate/delete only with an audit mapping and replacement evidence.

## Evidence and privacy

The primary reference population remains the versioned local ChatGPT Work/Codex evidence, with originators/clients kept separate. The account-wide provenance exporter may enrich the local evidence plane; Harness on Steroids should consume approved redacted/derived interfaces rather than copy private bodies into Git.

Raw JSONL, SQLite, prompts/transcript bodies, credentials, private account exports, user artifacts, raw account identifiers, and unsafe reversible identifiers stay local. Git may contain specs, structural/aggregate findings, approved hashes/aliases, tests, reports, and redacted examples.

## Do not

- Do not invent a new public exam or replace the project with SWE-bench, Terminal-Bench, Harbor, or another leaderboard.
- Do not re-test Codex merely to create a public benchmark.
- Do not build a standalone Codex clone.
- Do not make a particular model or harness the product boundary.
- Do not require exact Work tool sequences or exact prose as universal correctness.
- Do not claim private reasoning was observed.
- Do not commit private corpus bodies or secrets.

## Chat first, then explicit long-run authorization

Before /goal and an explicit go-ahead, conversation is the job. Answer questions and status requests. **Seek go-ahead before starting a long-running task.** A status question is not a standing goal.

After a /goal is explicitly set and the owner says go, CONTINUE.md governs autonomous continuation. The presence of PLAN.md, CURRENT.md, or an open GitHub issue does not itself authorize a long-running loop.

## Local CKFF Codex CLI

When using the local CKFF-backed Codex CLI, read [`docs/local-ckff-codex.md`](docs/local-ckff-codex.md) before selecting a key, model, endpoint, or request mode. Load the ignored `.env` explicitly; never print or commit its values. The active Codex CLI route uses the CKFF CC credential and streamed Responses requests. The CKFF default credential is intentionally excluded from active GPT use because it is expensive.

For agentic Sol work, use the repository's `src.sol_bridge` worker route: it uses streamed Chat Completions and executes only its validated local tools. Do not assume the native Codex CLI transport and the CKFF endpoint are interchangeable.

## Hosted comparison arms

For bounded matched-harness experiments, load the ignored repository `.env` and
keep the execution arms explicit. OpenCode uses `OPENCODE_MODEL` with the
configured YOLO Auto provider; the current low-cost arm is
`yolo-auto/qwen3.8-flash`. Pi uses `PI_MODEL` and its adapter writes a
project-local ignored provider file that references `QWEN_API_KEY` without
copying the secret into that file. Grok Build uses the authenticated CLI with
`GROK_BUILD_MODEL=grok-4.7`. Never print these credentials or place them in a
report. Jev remains OpenRouter Decisions API only and is a separate controller
call, not an execution model.

## Stop rewriting the goal

If you think SWE-bench is “better science,” **do not substitute it**. Do the analysis and the imitate-Codex modes. The owner already decided.


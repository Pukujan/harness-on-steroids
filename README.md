# Harness on steroids

**Learn reliable agent behavior from real Work/Codex traces, then transfer it across harnesses and models with fast measurable iterations.**

A capable model can still behave badly when its harness edits too early, skips research, guesses through asynchronous work, loses task state, or claims success without verification. This project studies those failures at the **control layer**.

<p align="center">
  <img src="docs/content-system-assets/hero.png" alt="A coding agent researches first, acts carefully, and verifies the result" width="100%">
</p>

## The reference

The project starts from a large local ChatGPT Work/Codex transcript corpus and an increasingly rich account-wide provenance export.

The useful signal is not just:

```text
exec -> wait -> exec
```

It is the complete observable trajectory where the source exposes it:

- how the assistant responds before acting;
- what it inspects and researches;
- when it waits, delegates, retries, or changes direction;
- tool inputs, results, failures, and mutations;
- whether it verifies the result;
- what evidence supports the final claims;
- how it handles corrections and long-running context;
- final output behavior and terminal status;
- whether the requested task actually succeeded;
- how much behavior varies across repeated runs of the same task.

Private transcript bodies, credentials, account exports, and raw local data stay out of Git.

## The goal

Harness on Steroids is **model- and harness-agnostic**.

The aim is not to reproduce exact Codex tool names or prose. It is to transfer useful supported behavioral properties to other coding-agent harnesses even when their models, tools, and native interfaces differ.

Normal development uses:

```text
same Work-derived task slice
        |
   +----+----+
   |    |    |
  Pi OpenCode Grok Build
   |    |    |
   +----+----+
        |
complete observable traces
        |
automatic comparison
        |
smallest next control change
```

The exact model/provider/config is recorded for every run. Using the same model across harnesses is useful for isolating harness effects, but it is not a requirement: model robustness is part of the problem.

## What already worked

The original project phase analyzed Work tool behavior, produced paired Kilo/OpenCode Codex-mode prompts, built an R1-R6 process scorer, and started matched replay on **22 long Work threads** (16 development, 6 holdout) with morph testing.

The prompt-only **Kilo Codex v0** result is especially useful: changing the behavior/control prompt produced a substantial qualitative improvement without changing the underlying model.

That work is not discarded. It is now the **v0 positive-control baseline and historical evidence**.

Tool-order scores such as R1-R6 remain useful diagnostics. They are no longer the definition of success.

## How development works now

**Large destination, tiny verified steps.**

Each normal slice should look like:

```text
reference evidence
      |
one behavioral deviation
      |
one hypothesis
      |
baseline on Pi + OpenCode + Grok Build
      |
smallest control change
      |
rerun same fixtures
      |
automatic comparison
      |
keep / revert / refine
```

The first knobs are deliberately cheap:

1. behavior prompt/instructions;
2. context selection and composition;
3. tool/capability presentation and adapter lowering;
4. checkpoint/continuation context;
5. only then a narrow runtime guard if repeated evidence proves it is needed.

A general runtime state machine is **not** a prerequisite.

Semantic labels such as inspect, research, execute, observe, verify, or complete can help normalize traces. Runtime enforcement is added only when a recurring measured failure survives prompt/context control and a small experiment shows the guard helps.

## What gets scored

The evaluator grows from the evidence rather than from a prebuilt framework.

Useful dimensions include:

| Dimension | Example question |
| --- | --- |
| Interaction | Did it orient, ask, update, and respond to corrections appropriately? |
| Research | Did it inspect the relevant target before consequential action? |
| Execution | Did it wait, retry, delegate, and mutate sensibly? |
| Verification | Did it actually check the result after material change or uncertainty? |
| Provenance | Can consequential claims be tied to observed evidence? |
| Output behavior | Did it distinguish observed, uncertain, partial, blocked, and complete? |
| Continuity | Did it preserve the important task state across a long run or interruption? |
| Outcome | Did the requested artifact/state/tests actually satisfy the task? |
| Variance | Does the desired behavior remain stable across repeated generations/morphs? |

Exact wording and exact tool sequences are not pass criteria.

## Current evidence

The repository currently records roughly **1,500 hashed Codex rollout files**. The primary Work slice is `codex_work_desktop`: 87 sessions, 83 with calls. Existing reports record, among other diagnostics, wait in 31/83, send in 25, spawn in 2, `update_plan` in 0, and patch in 1/83.

Those numbers are calibration evidence, not universal rules.

## Current active slice

The owner accepted the new operating direction on **2026-09-21**.

The first active experiment is GitHub issue **#2 — Baseline multi-harness Work behavior replay**.

It intentionally changes **nothing** first. It selects 3-5 existing development replay tasks and runs Pi, OpenCode, and Grok Build, capturing the richest comparable observable traces available. The result should identify the largest recurring deviations from Work evidence and exactly one smallest next control-layer hypothesis.

No general protocol/state-machine framework is being built before that result.

## Durable project memory

A new agent should be able to continue without this chat.

Read:

1. `AGENTS.md` — owner constitution;
2. `PLAN.md` — accepted long-term direction and operating method;
3. `checkpoints/CURRENT.md` — exact active state and next action;
4. the active GitHub issue — executable experiment scope and stop condition;
5. `HANDOFF.md` — concise evidence/handoff context.

`research/JOURNAL.md` is the append-only research trail, not the current state.

## Existing code policy

The old code is disposable; the evidence and lessons are not.

The current Kilo/OpenCode modes, scorer, replay utilities, and reports remain available as v0 baseline/history. Git history is the primary archive. Old implementation can be replaced when a measured replacement exists; backward compatibility is not a goal if it obstructs the behavioral-control objective.

## Boundaries

This project does not:

- replace the local Work/Codex reference with SWE-bench, Terminal-Bench, Harbor, or another public exam;
- build a standalone Codex clone;
- optimize for one particular model as the project goal;
- require exact Work prose or tool sequences;
- infer hidden chain-of-thought;
- count architecture completion as progress without a measured signal or behavior result;
- commit raw private transcript/account data.

## Repository map

| Path | Role |
| --- | --- |
| `AGENTS.md`, `PLAN.md` | authoritative owner contract |
| `spec/owner.v2.json` | machine-enforced owner invariants |
| `checkpoints/CURRENT.md` | current experiment and exact next action |
| GitHub Issues | active experimental work graph |
| `reports/`, `research/` | evidence, measurements, replay results, journal |
| `spec/harness-agnostic/` | architecture discussion + accepted operating refinement |
| `.kilo/agent/codex.md`, `.opencode/agent/codex.md` | v0 prompt-control baselines |
| `src/`, `tests/` | current reusable utilities and regression gates |

The active plan is intentionally empirical: **measure, change one thing, rerun, and let the behavior earn the architecture.**

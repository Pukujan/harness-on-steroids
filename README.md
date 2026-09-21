# Harness on steroids

**A research-led way to make agent harnesses behave reliably across products.**

A capable model can still do brittle work when its surrounding loop edits too soon, skips research, guesses while a job is running, loses state during handoff, or claims success without checking. Harness on Steroids studies that loop as a system.

<p align="center">
  <img src="docs/content-system-assets/hero.png" alt="A coding agent researches first, acts carefully, and verifies the result" width="100%">
</p>

## The problem

The model is only one part of an agent. The harness decides how the model receives context, sees tools, waits, asks for authority, splits work, recovers from failure, preserves state, and reports what actually happened.

That is why the same class of model can feel careful in ChatGPT Work and careless in another environment. The useful question is not “which tool did it call first?” It is:

> Given the task, available evidence, capabilities, authority, failures, and user corrections, did the harness make the right kind of decision—and can we prove the result?

## What this project is becoming

This is **not** a new coding agent or a second Codex. It is a portable behavior system with four parts:

1. **Evidence plane** — capture and normalize observable events with source pointers, integrity, context, and provenance.
2. **Behavior research** — study task topology, UX, research gates, action choices, verification, recovery, delegation, compaction, and handoff.
3. **Work Behavior Protocol** — express the useful behavior as semantic phases and obligations rather than product-specific tool names or prompt phrases.
4. **Adapters and verifiers** — project the protocol onto Kilo, OpenCode, Pi, and future harnesses, then check semantic traces and observable outcomes.

```text
local Work/Codex evidence
        |
        v
events -> context -> annotations -> behavior protocol
                                      |
                 +--------------------+--------------------+
                 v                    v                    v
             Kilo adapter        OpenCode adapter       Pi adapter
                 |                    |                    |
                 +--------- conformance + outcomes --------+
```

ChatGPT Work/Codex is the reference evidence source. It is not a literal script that every harness must reproduce. The host harness still owns its model, tools, permissions, UI, and native persistence; the portable layer defines the semantic contract between them.

## The behavior we want to preserve

The target is a conditional loop, not a fixed sequence:

```text
orient -> inspect -> research -> model -> plan -> authorize
  -> execute -> observe -> verify
  -> revise / recover / handoff / compact
  -> synthesize -> complete or blocked
```

The important obligations are:

- **Research before consequential action.** Inspect the target and distinguish observed facts from inference, uncertainty, and absence.
- **Evidence into action.** Connect a source observation to a decision, an authorized plan item, a native action, its observed result, and verification.
- **Honest waiting.** Wait for asynchronous work instead of guessing that it succeeded.
- **Useful decomposition.** Split multi-piece work after understanding the task, and preserve the brief and ownership of each slice.
- **Verification after change.** Check the relevant artifact, state, or test after mutation or failure.
- **Continuity.** Preserve objectives, constraints, evidence, pending approvals, failures, and the exact next action across compaction, interruption, and handoff.
- **Truthful UX.** Show the difference between observed, inferred, blocked, partial, and complete.

Planning is semantic. It does not require an `update_plan` tool or a long plan document; it may be represented by an evidence-backed action sequence, child brief, or checkpoint.

## What the local evidence says

The repository starts from a counts-only, hashed local corpus of about **1,500 Codex rollout files**. The primary reference slice is ChatGPT Work (`codex_work_desktop`): **87 sessions**, **83 with calls**, with wait in 31/83, send in 25, spawn in 2, and `update_plan` in 0. Work’s mapped process self-score is 81/83.

Those numbers are useful calibration, not the definition of good behavior. They show correlations in one originator. They do not explain the available alternatives, user intent, UX quality, research sufficiency, verification quality, or task outcome. Tool counts remain diagnostics.

The matched-task scaffold contains **22 long Work threads**: 16 for development and 6 held out. Replay is still incomplete, so the project does not claim that Kilo or OpenCode matches Work yet.

Raw JSONL, SQLite, prompts, transcript bodies, credentials, and user artifacts stay local. Git contains specs, reports, hashes, structural measurements, and tests only.

## What exists today

- A full-corpus, originator-separated Work/Codex analysis and versioned reports.
- Paired Kilo and OpenCode Codex-mode prototypes.
- A process scorer for look-first, wait/send order, mutation timing, and post-action inspection.
- Matched-task replay scaffolding with develop, holdout, and morph concepts.
- Property, hidden-holdout, mutation, metamorphic, differential, and CI gates.
- An issue log that records incomplete research instead of hiding it.
- A planning package under [`spec/harness-agnostic/`](spec/harness-agnostic/) that broadens the target to UX research, provenance, action planning, verification, continuity, Pi, and future adapters.

## What is not built yet

The durable protocol is still a proposal. The repository does not yet have:

- a canonical cross-harness event model and normalizer;
- a first-class evidence/claim/action/verification ledger;
- measured UX and user-turn research for the Work corpus;
- verified compaction and handoff preservation;
- capability manifests and explicit degraded paths;
- a Pi adapter or a capability-contrast adapter;
- semantic conformance verifiers that replace the process scorer as the main quality gate;
- completed matched-task outcome evaluation.

The current modes and scorer remain useful prototypes and historical evidence. They are not being presented as the finished architecture.

## How the project will be evaluated

Success is a vector, not a tool histogram:

| Layer | Question |
| --- | --- |
| Evidence integrity | Did the normalized trace conserve its source and preserve unknowns? |
| Behavior | Did the harness choose appropriate phases and transitions? |
| UX | Did it ask, update, wait, hand off, and report honestly? |
| Provenance | Can every consequential claim and action point to evidence? |
| Verification | Did it check the result against acceptance criteria? |
| Continuity | Did it survive failure, interruption, compaction, or handoff? |
| Outcome | Did the requested work actually complete within scope? |
| Safety | Did it avoid unauthorized actions, silent uncertainty, and overreach? |

The test strategy includes property, mutation, metamorphic, differential, recovery, UX, and sealed-holdout tests. Exact prose or exact vendor tool names should not be required when the semantic behavior and outcome are equivalent.

## Repository map

| Path | Role |
| --- | --- |
| `AGENTS.md`, `PLAN.md`, `ISSUES.md`, `HANDOFF.md` | Owner contract, current work, durable issue state, and handoff |
| `spec/harness-agnostic/` | Proposed harness-neutral behavior architecture and next decisions |
| `spec/codex-imitate-mode.md` | Current Work/Codex prototype specification |
| `spec/work-research-gates.md` | Research validity, sufficiency, provenance, and continuity gaps |
| `reports/` | Counts-only evidence, snapshots, replay indices, and score tables |
| `research/` | Corpus measurements, replay utilities, and append-only journal |
| `.kilo/agent/codex.md` | Kilo prototype projection |
| `.opencode/agent/codex.md` | OpenCode prototype projection |
| `src/` | Current scorer, goal loop, and owner-invariant library |
| `tests/` | Governance, process, replay, and evaluation gates |
| `.content-system/` | Pinned content-generation adapter and evidence map |

## Boundaries

This project does not:

- turn SWE-bench, Terminal-Bench, Harbor, or a public leaderboard into the exam;
- build a standalone Codex clone or generic “AI-powered harness”;
- infer or require hidden chain-of-thought;
- treat a summarizer as the answer to continuity before compaction is measured;
- claim completion from a process score alone;
- commit raw local transcript or account-export data.

The current implementation is disposable if it blocks the long-term protocol. The evidence, tests, and audit trail are not.

## Current status and next step

The repository is in an **architecture-reset planning phase**. The proposal package is committed under `spec/harness-agnostic/`, and issue 19 records the owner-review gate. No protocol implementation, prompt rewrite, Pi adapter, cleanup, or long-running `/goal` loop has started from that proposal.

The next authorized slice is read-only: agree on the evidence interface, measure the missing UX/research/compaction dimensions, define annotation and decision-point rules, and return with a protocol draft before building adapters.

## Content and visual contract

This README follows the pinned [`content-generation-modules` v0.1.2](https://github.com/Pukujan/content-generation-modules/releases/tag/v0.1.2) adapter in [`.content-system/`](.content-system/). Claims are marked by their repository evidence and status; the visual assets remain narrative orientation aids rather than proof of behavior. The longer review artifacts live in [`docs/content-system-preview.md`](docs/content-system-preview.md) and [`docs/content-system-preview.html`](docs/content-system-preview.html).

## Read next

Start with [`AGENTS.md`](AGENTS.md) → [`PLAN.md`](PLAN.md) → [`HANDOFF.md`](HANDOFF.md) → [`ISSUES.md`](ISSUES.md). Then read the [harness-agnostic planning package](spec/harness-agnostic/README.md).

Do not commit `data/`, private exports, or chat bodies.

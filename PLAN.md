# Plan (owner) - harness- and model-agnostic behavioral control

Owner: Pujan. Agents execute this plan; they do not replace it.

Status: **accepted and authoritative as of 2026-09-21**.

## Long-term goal

Build a model- and harness-agnostic control layer that transfers useful **observable** behavior found in local ChatGPT Work/Codex transcripts to different coding-agent harnesses.

The project is not "copy Codex tool names." It is to learn and reproduce supported behavioral properties across the whole observable trajectory: conversation handling, inspection/research, action choice, waiting, delegation, verification, provenance, context/continuity, output behavior, and task outcome.

**Large destination, tiny verified steps.**

## Reference evidence

Primary evidence is the local, versioned ChatGPT Work/Codex corpus. Keep originators/clients separate. The custom account-wide provenance exporter may enrich the source with additional observable structure, but raw account/transcript bodies remain local.

The existing corpus/tool research is v0 evidence, not discarded work:

- full-corpus originator-separated analysis;
- spec/codex-imitate-mode.md;
- Kilo/OpenCode Codex-mode prompts;
- R1-R6 process scorer;
- 22 long Work replay threads (16 develop, 6 holdout);
- morph/replay scaffolding and reports.

Tool order is diagnostic, not the final target.

## Development surfaces

Every normal development slice should run the candidate on **Pi + OpenCode + Grok Build** in the same slice when technically possible.

Record exact harness/version, model/provider/version or model ID, control version/config, task fixture/environment fidelity, and run attempt/repetition.

The system is model-agnostic. The same model across harnesses is useful but not required. When a common model is available, it can isolate harness effects; normal iteration may use different models and still contribute evidence when identity is recorded.

**Kilo Codex v0 is the positive-control baseline.** Kilo already showed that a stronger behavior prompt can materially improve a harness. Keep that result available as a baseline instead of making Kilo the main development target.

## Control mechanisms - cheapest first

Use the smallest mechanism that can fix an observed deviation:

1. prompt / behavior instructions;
2. context selection and composition;
3. tool/capability descriptions and adapter lowering;
4. checkpoint / continuation context;
5. a narrow runtime guard or state only when repeated evidence shows 1-4 are insufficient.

There is no requirement to build a general runtime state machine.

Semantic states/phases may be used by the evaluator to normalize different native traces, for example inspect, research, execute, observe, verify, complete. Runtime enforcement is added only when an observed persistent failure justifies it and a measured slice shows improvement.

## Fast development loop

spec/iteration-loop.md is the normative loop:

reference evidence -> one behavior hypothesis -> baseline on Pi + OpenCode + Grok Build -> smallest control change -> rerun the same fixtures -> automatic multi-signal comparison -> keep / revert / refine

Each slice should normally change **one behavior hypothesis**.

A substantial slice must end with at least one of:
- a new measured reference signal;
- a new automated evaluator capability;
- an observable behavior/outcome result.

Do not spend multiple slices building architecture before seeing behavioral evidence.

## What gets measured

Score observable dimensions separately rather than collapsing everything into one early number:

1. Interaction - pre-tool/post-tool response shape, questions, corrections, authorization, useful updates.
2. Research/inspection - target inspected, evidence gathered, research sufficiency, response to new evidence.
3. Execution - native tool/action topology, waits, failures, retries, delegation, mutations.
4. Verification/provenance - result observed, post-change checks, claims supported by evidence.
5. Output behavior - uncertainty, partial/blocked/complete honesty, concise evidence-backed synthesis, repetition/noise.
6. Continuity - long-task state preservation, corrections, compaction/interruption/rehydration where observable.
7. Outcome - requested artifact/state/checks, side effects, task acceptance.
8. Variance - deviation across repeated generations and morph-equivalent requests.

Exact wording and exact tool names are not pass criteria.

## Repeated runs and morphs

Use the same input over multiple generations when it helps measure stability. A strong control layer should reduce undesirable behavioral variance even when model quality differs.

Keep the existing morph principle: paraphrase, split/merge turns, add irrelevant context, or inject corrections without changing the semantic task. Do not tune on sealed holdout tasks or their derived variants.

## Project continuity

The repository and GitHub are project memory.

- AGENTS.md - constitutional owner rules.
- PLAN.md - durable destination and operating method.
- spec/owner.v2.json and spec/owner.v2.md - machine/human governance contract.
- checkpoints/CURRENT.md - exact current state and next action.
- GitHub Issues are the active work graph; avoid speculative backlog.
- HANDOFF.md - concise handoff/current evidence summary.
- ISSUES.md - durable historical issue ledger and mapping.
- research/JOURNAL.md - append-only research history, not current state.

A new agent should not need this chat to continue correctly.

## Existing repository / v0 policy

Do not wipe the evidence trail.

The old code is disposable; evidence and lessons are not.

Keep v0 prototype files in place while they remain useful baselines. Git history is the primary archive. Move/delete old implementation only after a measured replacement exists, current tests/evidence are mapped or intentionally retired, and an audit note explains what moved and why.

Backward compatibility with the current implementation is **not** a product requirement if it obstructs the goal.

## Current milestones - evidence-driven, not waterfall

### M0 - Governance reset - DONE

Make this plan, owner spec v2, continuity checkpoint, tests, and issue tracking authoritative. Preserve v0 as baseline/history.

### M1 - Multi-harness baseline - ACTIVE

GitHub issue #2.

Use 3-5 existing representative long Work-derived development tasks. Run Pi + OpenCode + Grok Build in the same slice with no new control intervention first.

Capture the complete observable trajectory that each harness exposes. Produce a comparison identifying the largest recurring deviations from Work reference behavior and one smallest next hypothesis.

This milestone must produce visible results before adding architecture.

### M2 - Enrich only the signals the baseline needs

Use the Work/Codex corpus and account-wide exporter to add missing measurable signals such as assistant-turn shape, user-turn class, verification/provenance, output behavior, continuity/compaction, and child brief structure.

Do not build a general annotation platform first. Add the smallest extractor/scorer needed to answer an observed evaluation question.

### M3 - Iterative control improvement

For each measured deviation: state one hypothesis, make one small prompt/context/capability/checkpoint change, run all three active harnesses, compare automatically, keep/revert, and record the result.

### M4 - Promotion loop

Periodically test surviving changes on broader develop tasks, repeated runs, morphs, multiple models where useful, and sealed holdout.

Promotion requires no regression in outcome, verification, scope/safety, or honest reporting.

### M5 - Runtime enforcement only if earned

If a failure persists across prompts/context, tasks, models, and harnesses, test the smallest runtime state/guard that directly addresses it. Do not build a general state-machine framework in advance.

## Explicitly out of scope

- public benchmark replacement of the local Work/Codex evidence;
- a standalone Codex clone;
- a framework-completion milestone with no behavioral result;
- model-specific optimization as the project goal;
- exact prose/tool-sequence cloning;
- private reasoning inference;
- transcript bodies, secrets, or private exports in Git;
- a speculative giant adapter/protocol implementation before experiments demand it.

## Quality gates

Keep the existing property, hidden-holdout, mutation, metamorphic, differential, replay, and CI gates as historical and regression protection, but update governance gates to owner spec v2.

Do not delete v0 replay/process tests just because they are no longer the primary objective. They remain useful evidence until deliberately retired with an audit mapping.

## Long-running execution

This plan being accepted does **not** itself start an autonomous /goal loop. CONTINUE.md applies only after a specific /goal plus explicit owner go-ahead.

The immediate authorized continuity target is GitHub issue #2; execution of that long-running experiment still follows the chat-first/go-ahead rule.

# Behavior and UX research plan

## Research question

Do not ask only “which tool came next?” Ask:

> Given the task, available evidence, capabilities, authority, prior outcomes, and user interaction state, which semantic phase and decision were appropriate, which were chosen, and what evidence shows that the choice worked?

## Annotation ontology

Annotate spans or event groups with versioned labels:

- `intake`, `orient`, `inspect`, `decompose`, `research`, `compare_sources`;
- `form_hypothesis`, `plan_action`, `request_authority`;
- `execute`, `observe_result`, `verify`, `revise`, `recover`;
- `synthesize`, `handoff`, `wait`, `compact`, `rehydrate`;
- `blocked`, `complete`.

Each annotation records the event span, entry trigger, target object, intended result, supporting evidence IDs, available alternatives if observable, exit condition, downstream effect, confidence, ambiguity, competing label, annotation version, and whether later evidence contradicted it.

Do not infer hidden chain-of-thought. Observable thoughts or reasoning recaps are content classes, not privileged ground truth.

## UX research dimensions

The existing `research/work-ux-gaps.md` correctly identifies UX as unmeasured. The next study must measure:

- whether and when the harness speaks before first tool use;
- timing and usefulness of updates around inspection, mutation, waits, errors, and completion;
- user-turn classes: question, status request, correction, authorization, new scope, stop, and go-ahead;
- when the harness asks versus assumes;
- progress reporting during long or asynchronous work;
- permission and authority explanations;
- child-task naming, briefing, waiting, and synthesis;
- blocker and partial-completion language;
- reaction to user corrections;
- repeated updates that add no new information;
- completion claims relative to actual evidence and unfinished obligations;
- behavior before/after compaction, interruption, restart, and handoff.

## Research gates

Treat these as testable semantic gates, not slogans:

| Gate | Required evidence |
| --- | --- |
| Research valid | Claim cites an observed result/source or is explicitly `not_observed` |
| Research enough | The target of the next consequential action was actually inspected |
| Action reliable | No material write/send before prerequisites and authority are satisfied |
| Verify after action | The relevant result is observed and checked after mutation |
| Synthesize late | State is handed off through a brief, checkpoint, or user answer rather than an unbounded chat |
| UX honest | Observed, inferred, blocked, partial, and complete are visibly distinct |

## Sampling and reliability

Stratify by task family, thread length, model, originator, harness, failure mode, compaction, delegation, and outcome. Double-annotate a sample and adjudicate disagreements. If annotators cannot agree on phase boundaries, task topology, or outcome labels, do not encode the disputed rule as a hard protocol invariant.

## What existing counts cannot establish

The current Work figures show rare patching, wait clusters, sends, and no `update_plan` calls. They do not prove that planning is absent: planning may be represented by a child brief, checkpoint, action sequence, or implicit evidence-backed next step. A semantic `plan_action` state must therefore be independent of any particular tool name.

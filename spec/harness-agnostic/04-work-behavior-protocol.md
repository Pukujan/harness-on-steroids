# Work Behavior Protocol (proposal)

## Purpose

The protocol is a declarative semantic contract consumed by a host harness. It is not a replacement model loop, a transcript replay engine, or a Codex clone.

## Lifecycle

```text
intake -> orient -> inspect -> research -> model -> plan
  -> authorize -> execute -> observe -> verify
  -> {revise | recover | handoff | compact/rehydrate | synthesize}
  -> {complete | blocked}
```

Transitions are conditional. A simple question may stop after orientation; a multi-repository change may traverse the full lifecycle. A harness must be allowed to take semantically equivalent paths when evidence and outcome are equivalent.

## State obligations

| State | Entry condition | Obligation | Exit evidence |
| --- | --- | --- | --- |
| `orient` | Request received | Identify objective, scope, authority, and ambiguity | Task context record |
| `inspect` | Target or environment unknown | Read/search/inspect relevant state | Source pointers or explicit absence |
| `research` | Claim/action depends on external or repository facts | Gather and compare sources | Evidence ledger entries |
| `model` | Facts are sufficient enough to act | Separate facts, inferences, uncertainty, conflicts | Decision context |
| `plan` | Consequential work has dependencies | Define semantic actions, prerequisites, expected results, acceptance | Action-plan graph |
| `authorize` | Action crosses a material authority boundary | Ask, confirm, or use recorded authority | Authority record |
| `execute` | Plan item is actionable | Invoke a native capability exactly within scope | Action event |
| `observe` | Action returned or is asynchronous | Wait/poll/receive result; do not assume success | Result event |
| `verify` | Result may satisfy an obligation | Check artifact/state/claim against criteria | Verification record |
| `revise` | Evidence changes understanding | Update plan and affected lineage | New plan revision |
| `recover` | Failure, stale evidence, conflict, or missing capability | Change premise, method, input, or environment | Recovery outcome or precise blocker |
| `synthesize` | User-facing response or handoff required | Summarize evidence, outcome, residuals, and next action | Auditable response/handoff |
| `complete` | Acceptance criteria verified | Claim completion only within verified scope | Completion record |
| `blocked` | Progress requires missing authority/evidence/capability/external state | Name blocker and exact unblock condition | Blocker record |

## Normative behavior

- Inspectable targets are inspected before consequential mutation.
- A missing observation is not a negative observation.
- Tool output and source evidence outrank model prose.
- Writes, sends, delegation, and authority changes require appropriate prerequisites.
- Long-running or asynchronous work is waited on and then observed.
- Material mutations receive relevant verification.
- A retry must change a premise, method, input, or environment; identical repetition is not recovery.
- Completion is gated by evidence, not by an attempted action or confident prose.
- Semantic plan state is not tied to `update_plan`; the current Work data reports zero of that tool.
- The protocol never requires private reasoning or exact wording.

## UX contract

Adapters must render or approximate these semantics:

- concise orientation before nontrivial work;
- meaningful progress at phase boundaries or after long waits;
- explicit authority requests;
- distinct observed, inferred, uncertain, blocked, partial, and complete states;
- evidence-backed completion with residual risks;
- no conversion of an ordinary question/status request into a standing autonomous goal;
- no repetitive narration of unchanged state.

## Capability-degraded behavior

If a host lacks a capability, the protocol must choose an explicit degraded path. A harness without child agents serializes slices; it must not claim delegation. A harness without structured verification hooks may expose advisory status, but the adapter must declare that limitation and the evaluator must not score the invariant as enforced.

# Work Behavior Protocol (proposal)

## Purpose

The protocol is a declarative semantic contract consumed by a host harness. It is not a replacement model loop, a transcript replay engine, or a Codex clone.

The v1 protocol uses three scopes rather than one flat state machine:

1. **run** — the user-visible job and its terminal status;
2. **task graph** — one or more dependent or concurrent tasks/plan items;
3. **attempt** — a single task attempt moving through semantic phases.

This matters because delegation, waits, retries, and verification may be active for different tasks at the same time.

## Lifecycle

A run begins at `intake`, constructs or updates a task graph, and terminates only at `complete`, `partial`, `blocked`, `failed`, or `interrupted`.

Each task attempt may traverse:

```text
orient -> inspect -> research -> assess -> plan -> authorize
  -> execute -> observe -> verify
  -> {revise | recover | handoff | compact/rehydrate | synthesize}
```

Transitions are conditional and phases may be skipped when their obligation is already satisfied by current evidence. Independent tasks may proceed concurrently when dependency, authority, and capability constraints allow it. A simple question may stop after orientation or inspection; a multi-repository change may contain several task attempts, waits, child tasks, and recoveries.

A parent task cannot be considered complete while a required child/dependency is unresolved. A wait belongs to the task or external condition being awaited, not to the whole run by default.

## Normative terms

- **Consequential action:** an action that can change durable state, communicate externally, spend material resources, broaden authority, or create a result that the user may rely on.
- **Material mutation:** a consequential write/change whose failure or incorrectness could alter the requested outcome.
- **Authority boundary:** a point where user approval, host permission, credential scope, or explicit project policy is required before proceeding.
- **Verified scope:** the subset of requested outcome claims for which post-action evidence satisfies the declared acceptance criteria.

These definitions are adapter-independent. Harnesses may add stricter local definitions but may not weaken them while claiming full conformance.

## State obligations

| State | Entry condition | Obligation | Exit evidence |
| --- | --- | --- | --- |
| `orient` | Request/task received | Identify objective, scope, authority, ambiguity, and dependencies | Task context record |
| `inspect` | Target or environment unknown/stale | Read/search/inspect relevant state | Source pointers or explicit absence |
| `research` | Claim/action depends on repository or external facts | Gather and compare sources | Evidence ledger entries |
| `assess` | Evidence is sufficient to choose a path | Separate observations, inferences, uncertainty, and conflicts | Decision context |
| `plan` | Consequential work has dependencies or multiple obligations | Define semantic actions, prerequisites, expected results, acceptance | Action-plan graph/revision |
| `authorize` | Action crosses an authority boundary | Ask, confirm, or use recorded authority | Authority record |
| `execute` | Plan item is actionable | Invoke a native capability exactly within scope | Action event |
| `observe` | Action returned or is asynchronous | Receive/wait/poll/cancel as appropriate; do not assume success | Result/lifecycle event |
| `verify` | Result may satisfy an obligation | Check artifact/state/claim against criteria | Verification record |
| `revise` | Evidence changes understanding | Update affected task/plan lineage | New plan revision |
| `recover` | Failure, stale evidence, conflict, or missing capability | Change premise, method, input, actor, or environment | Recovery outcome or precise blocker |
| `handoff` | Work changes actor/harness | Transfer bounded state, authority, evidence, and next action | Handoff record |
| `compact` | Context/state must be reduced | Produce checkpoint projection without destroying source history | Checkpoint + source links |
| `rehydrate` | Work resumes from compacted/restarted state | Revalidate critical constraints, pending authority, evidence links, and next action | Rehydration record |
| `synthesize` | User-facing response or task-level summary required | State evidence, outcome, residuals, and next action | Auditable response/handoff |

## Run terminal states

- `complete`: all required acceptance criteria are verified within authorized scope.
- `partial`: a useful subset is verified and the unresolved remainder is named.
- `blocked`: progress requires a specific missing authority, capability, evidence item, dependency, or external state; the unblock condition is explicit.
- `failed`: an attempted required path failed and no acceptable recovery remains within current scope.
- `interrupted`: execution stopped before a terminal outcome but a resumable checkpoint exists or the missing state is identified.

Confident prose or a successful tool return cannot by itself create `complete`.

## Normative behavior

- Inspectable targets are inspected before consequential mutation unless current evidence is explicitly fresh and sufficient.
- A missing observation is not a negative observation.
- Tool/source evidence outranks unsupported model prose.
- Writes, sends, delegation, authority changes, and other consequential actions require their prerequisites and authority.
- Long-running or asynchronous work is observed to a terminal or explicitly deferred state.
- Material mutations receive relevant verification.
- A retry must change a premise, method, input, actor, or environment; identical repetition is not recovery.
- Completion is gated by verification evidence and dependency closure.
- Semantic planning is not tied to `update_plan` or any product-specific tool.
- The protocol never requires private reasoning, hidden chain-of-thought, or exact wording.

## UX contract

Adapters must render or approximate these semantics:

- concise orientation before nontrivial work;
- meaningful progress at phase boundaries, material changes, or after long waits;
- explicit authority requests;
- visibly distinct observed, inferred, uncertain, blocked, partial, failed, interrupted, and complete states;
- evidence-backed completion with residual risks;
- no conversion of an ordinary question/status request into a standing autonomous goal;
- no repetitive narration of unchanged state.

## Capability-degraded behavior

If a host lacks a capability, the negotiated protocol profile must choose an explicit degraded path. A harness without child agents serializes or locally decomposes slices; it must not claim delegation. A harness without enforceable verification hooks may expose an advisory verifier, but the adapter must declare that limitation and may not claim the affected invariant as runtime-enforced.

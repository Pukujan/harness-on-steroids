# Continuity, wait, compaction, and handoff

## Three-layer state model

Continuity should use three separate layers:

1. immutable local event history;
2. derived current-state model;
3. compact checkpoint projection for restart, handoff, or user-visible status.

`CURRENT.md` can be a readable projection, but it must not become the sole source of truth.

## Portable checkpoint

A checkpoint must preserve:

- objective, success criteria, constraints, and user corrections;
- authority boundaries and pending approvals;
- current lifecycle phase and task/dependency graph;
- observed facts, claims, uncertainty, and source pointers;
- action-plan revisions and decisions/rejected alternatives;
- actions taken, results, failures, and recovery state;
- artifacts, versions, and verification completed/still required;
- active waits, child tasks, handoffs, and compaction boundaries;
- exact next action and blocker/unblock condition.

## Wait semantics

Waiting is a lifecycle operation, not a timing preference. The adapter must distinguish:

- an in-process asynchronous cell or job;
- a child-task wait;
- a user/authority wait;
- an external-state wait;
- a periodic scheduler wakeup.

The current Work evidence shows same-thread wait behavior around long-running cells. The project’s scheduler wakeups are continuity machinery, not evidence that the target harness uses the same interaction pattern.

## Handoff packet

A child brief or cross-harness handoff should include the objective, scope, authority, current phase, dependency graph, observed facts, evidence pointers, actions/results, verification state, failed approaches, artifacts, exact next action, open questions, and blockers. A short prompt without this state is not a durable handoff.

## Compaction contract

Measure existing `compacted` events before choosing a compression algorithm. Compaction is successful only if rehydration preserves the obligations above. A rehydrated run must verify critical constraints, pending approvals, evidence links, and next action before resuming.

Do not build a summarizer as the first response to context loss. First establish the event/checkpoint contract and test semantic preservation.

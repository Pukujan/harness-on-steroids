# Owner decisions and handoff

## Decisions required before implementation

1. Priority order: task outcome, research discipline, verification, safety/scope, continuity, delegation, latency/cost, and interaction style.
2. Reference population: which Work/Codex originators, models, clients, time ranges, and empty sessions are in scope, and how coverage is explained.
3. Environment fidelity: what workspace, tools, permissions, external resources, and starting state must be reconstructed for a matched task.
4. Outcome identity: which artifact/state/test/acceptance rubric defines “the same job succeeded.”
5. Model matrix: which model and version strata are required for every adapter.
6. Enforcement budget: which protocol invariants must be runtime-enforced versus advisory per harness.
7. Variation tolerance: which semantically equivalent paths are accepted and which safety/process differences are disqualifying.
8. Annotation authority: who adjudicates ambiguous phases, UX, and outcomes, and how adjudication becomes reproducible.
9. Privacy boundary: confirm that public GitHub receives only aggregate/structural evidence and no raw account exports.
10. Repository reset policy: which current modules are retained, wrapped, or replaced after the protocol is accepted.

## Proposed next authorized slice

After approval, do **not** start with a prompt rewrite. Start with a read-only contract/evidence slice:

1. map the current repo claims to this package;
2. inventory the upstream exporter schema and the local Work corpus without copying bodies;
3. propose versioned event/context/index schemas;
4. run the missing UX/research/compaction measurements;
5. return with an annotation sample, disagreement report, and protocol draft for approval.

Only then should a `/goal` or long-running implementation loop be considered.

## Current handoff state

- Current branch before this package: `main` at the existing replay/test snapshot.
- Package branch: `planning/harness-agnostic-context`.
- Existing implementation: preserved and untouched by this proposal.
- Existing issues 13–18: still open/in progress as recorded in `ISSUES.md`.
- No adapter implementation, prompt rewrite, replay run, or cleanup is authorized by this package.

## Completion definition for this planning task

This planning task is complete when the package is reviewed, committed, pushed, and linked from the issue log. Project implementation remains intentionally incomplete.

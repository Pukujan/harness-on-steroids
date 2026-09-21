# Verification and evaluation plan

## Verifier layers

Use separate verdicts; do not collapse them into a single tool-order score.

1. **Evidence integrity** — source conservation, valid graph links, deterministic hashes, parser/reconciliation status, and explicit unknowns.
2. **Coverage** — every corpus item is included, excluded, or unresolved with a reason.
3. **Annotation reliability** — agreement on phase, task boundary, decision point, UX class, and outcome.
4. **Protocol conformance** — valid state transitions, evidence obligations, authority, waits, recovery, and completion gates.
5. **UX conformance** — honest progress, ask/assume behavior, blocker visibility, correction handling, and non-repetitive updates.
6. **Action provenance** — evidence-to-plan-to-action-to-result-to-verification lineage.
7. **Outcome** — requested artifacts/state/tests and user-visible acceptance criteria.
8. **Safety/scope** — no unauthorized action, skipped verification, silent uncertainty, or overreach.

R1–R6 remain a cheap historical process layer. They must not decide whether a harness behaves well or completes the task.

## Test families

- Property: inspect before mutation; support claims or mark `not_observed`; verify after mutation; completion requires evidence.
- Mutation: remove verification, corrupt a result, deny permission, delay a job, stale a source, remove a capability, or inject false success.
- Metamorphic: paraphrase requests, rename paths, reorder irrelevant context, add distractors, substitute equivalent tools, split/merge user turns, and vary harmless formatting.
- Differential: compare adapters under equivalent capabilities, against native modes, and against semantic Work reference traces.
- Holdout: sealed long threads across task families, dates, workspaces, failures, compaction, model classes, and capability patterns.
- Recovery: force transient errors, missing tools, stale evidence, child failure, interruption, and rehydration.
- UX: evaluate progress, authority, blocker, correction, and completion behavior at the phase boundary rather than by prose similarity.

## Outcome rubric

Define the rubric before running adapters. Score observable criteria such as:

- task intent and scope were addressed;
- research was sufficient for consequential claims/actions;
- expected artifacts or state changes exist;
- tests/checks were relevant and passed or failures were surfaced;
- verification was performed and linked;
- no unauthorized or unrelated changes occurred;
- uncertainty, partial completion, and blockers were honest;
- continuity survived the injected interruption or compaction.

Exact wording, exact tool names, latency, and one valid alternative sequence should not fail a semantically equivalent run.

## Split and leakage rules

Freeze task families, model/version strata, environment reconstruction, and train/development/holdout boundaries before tuning. Keep complete threads, paraphrases, related workspaces, sibling tasks, and derived answers in the same leakage group. Score the sealed holdout once after development is frozen.

If process scores rise while outcome or safety falls, stop implementation and return to diagnosis.

## Promotion gates

Promote a protocol/adapter version only when evidence integrity, coverage, annotation reliability, semantic conformance, paired-adapter parity, outcome thresholds, repeated-run stability, and safety gates all pass. “The modes exist” is not completion.

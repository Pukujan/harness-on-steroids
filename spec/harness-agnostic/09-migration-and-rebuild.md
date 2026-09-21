# Migration and rebuild strategy

## Principle

The current code is disposable; the evidence and lessons are not. Rebuild around the new boundary instead of layering more prompt exceptions onto a scorer that cannot represent the desired behavior.

## Phase 0 — proposal freeze

- owner reviews this package;
- resolve the decisions in `10-owner-decisions-and-handoff.md`;
- preserve the current branch and reports;
- declare which existing claims are historical, diagnostic, or normative;
- freeze privacy and leakage rules.

No implementation begins in this phase.

## Phase 1 — evidence interface

- agree on the exporter-to-harness event schema;
- verify raw-before-parse preservation, source pointers, hashes, and reconciliation;
- add context/capability/index records;
- produce coverage and unknown-state reports;
- keep all raw material local.

## Phase 2 — research and annotation

- measure UX and user-turn classes;
- measure research gates, child briefs, waits, compaction, and continuity;
- publish an annotation handbook and adjudicated sample;
- derive conditional decision points and counterexamples.

## Phase 3 — protocol and verifiers

- write versioned state/transition and action-plan schemas;
- implement semantic trace validation and provenance checks;
- build mutation, recovery, continuity, and UX fixtures;
- keep R1–R6 as a compatibility view only.

## Phase 4 — adapters

- implement thin Kilo, OpenCode, and Pi mappings;
- add one capability-contrast adapter;
- declare degraded guarantees rather than faking unsupported behavior;
- test paired semantics before optimizing prompts or model settings.

## Phase 5 — outcomes

- reconstruct comparable environments;
- run development matched tasks and morphs;
- compare native mode versus adapter mode;
- open the sealed holdout only after the development gate;
- record outcome, safety, UX, and continuity deltas.

## File disposition

Do not delete the existing reports, modes, scorer, or issue history during the reset. Move them under explicit version/history labels only after new tests reference the replacement. A clean rebuild is acceptable later, but it must preserve an audit path from every retired claim to the evidence that replaced it.

## Stop conditions

Return to evidence work when context or environment cannot be reconstructed, annotation disagreement stays high, rules are supported mainly by tool counts, leakage is found, holdout degrades sharply, improvements depend on memorized wording, or an adapter cannot enforce a claimed invariant.

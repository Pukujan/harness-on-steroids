# Current-state audit and disposition

## Confirmed strengths

The repository already has valuable foundations:

- owner governance and anti-substitution gates;
- a hashed local corpus and originator separation;
- explicit Work/Codex gold selection rather than averaging incompatible originators;
- structural reports for task splits, wait, send, spawn, patch, shell, JavaScript, and empty sessions;
- versioned historical reports under `reports/versions/`;
- paired Kilo/OpenCode prototype modes;
- process relations R1–R6, property, holdout, mutation, metamorphic, differential, and CI tests;
- long-thread develop/holdout lists and hash-only replay score tables;
- a stated research/provenance/checkpoint queue;
- a module map that separates contract, measurement, adaptation, library, gates, and state.

These are assets to preserve, not evidence that the final architecture is complete.

## Current evidence and its limit

The current gold snapshot says ChatGPT Work is `codex_work_desktop`, with 87 files, 83 containing calls, patch in 1/83, wait in 31/83, send in 25, spawn in 2, `update_plan` in 0, and first call mostly `exec`. The Work self-score is 81/83. Kilo and OpenCode replay rows remain uneven, and the full multi-turn matched-task evaluation is not complete.

These counts establish observable correlations. They do not establish why a decision was made, what alternatives were available, whether the target was understood, whether a final claim was verified, or whether the same behavior transfers to another harness.

The repository's own open queue confirms the gap:

- issue 13: matched-task outcome replay is not complete;
- issue 14: Work research, planning, user-turn classes, child briefs, and compaction measurement is not complete;
- issue 15: provenance and research gates are not fully encoded;
- issue 16: durable checkpoints are not implemented as a verified continuity layer;
- issue 17: the portable pack remains queued;
- issue 18: module/lint/type foundation work remains in progress.

## Keep, demote, replace

| Existing artifact | Disposition under this proposal |
| --- | --- |
| `AGENTS.md`, owner gates, privacy rules | Keep as governance and safety boundary |
| Hashed corpus and aggregate reports | Keep as evidence snapshots with coverage caveats |
| `reports/versions/` and current issue log | Keep as historical audit trail |
| R1–R6 | Keep as cheap process diagnostics, not the success definition |
| Kilo/OpenCode prompt files | Keep as prototype adapters; do not call them the protocol |
| `spec/codex-imitate-mode.md` | Freeze as protocol v0/history, then supersede through an approved version |
| `src/score_session.py` | Keep as legacy scorer until semantic verifiers exist |
| `research/replay_lib.py` | Keep as replay evidence utility; do not make it the behavior model |
| Tool histograms and phrase needles | Governance/descriptive layer only |
| One-turn or sandbox replay rows | Smoke evidence only; not full outcome parity |
| Direct prompt patching from counts | Replace with evidence-backed protocol and adapter conformance |
| Existing implementation structure | Disposable if it prevents the protocol/evidence boundary |

## Main architectural diagnosis

The project currently has strong measurement discipline around tool traces but weak modeling of conditional decisions. The missing objects are:

1. context and capability availability at each decision point;
2. semantic episode and phase labels;
3. UX obligations and user-turn classes;
4. research claim/source records;
5. action-plan items with authority and acceptance criteria;
6. result and verification links;
7. failure/recovery and continuity state;
8. adapter capability manifests;
9. semantic conformance and outcome verifiers.

The reset should build those objects before tuning any harness mode.

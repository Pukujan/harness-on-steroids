# Handoff

**Owner precedence:** AGENTS.md -> PLAN.md -> checkpoints/CURRENT.md -> active GitHub issue -> HANDOFF.md -> ISSUES.md.

## Current direction

The owner accepted the model- and harness-agnostic behavioral-control reset on **2026-09-21**.

The project now learns from the complete observable behavior in local ChatGPT Work/Codex transcripts and transfers those supported behaviors through the smallest effective control-layer changes. Prompt/context engineering remains the first intervention. A general runtime state machine is not pre-authorized; runtime guards are added only when repeated evidence earns them.

Normal development runs **Pi + OpenCode + Grok Build in the same slice** where technically possible. Record exact model/provider/harness/config, but do not make any model the product boundary.

Kilo Codex v0 remains a positive-control baseline and historical proof that behavior prompting can materially improve a harness.

## Active issue

Local issue **22 - Jev long-horizon matched A/B**. The durable research
and contract are `research/jev-controller-v2-research.md`,
`research/jev-ecosystem-evidence.md`, `research/jev-long-horizon-ab.md`, and
`spec/jev-controller-v2.md`;
`ISSUES.md` contains the issue mapping.

The old three-adapter Jev run is complete as a v1 routing smoke test. It used
one compact decision and one prompt hint per task. Do not treat it as evidence
that Jev can decompose tasks or control a long horizon.

The clean Issue 22 long-horizon A/B is now complete. OpenCode, Grok Build, and
Pi each ran 60 matched Work-derived development turns per arm across 16
development hashes with the shared feeder and sealed six-hash holdout. The
current Jev policy did not win: Jev executed only 13, 13, and 12 turns after
47, 47, and 48 low-confidence fallbacks respectively. OpenCode fell from
8/16 to 4/16 Work-match; Grok Build and Pi were 0/16 in both arms. See
`reports/jev-long-ab-20260922.md` and its three per-harness reports.

Historical active issue label: GitHub issue **#2 - Baseline multi-harness Work behavior replay**.

The completed implementation was the long-horizon matched A/B: the shared
context feeder ran 60 Work-derived development turns with and without the
validated Jev decision on each available harness. The follow-up is limited to
the low-confidence fallback hypothesis below.

The next session should:

1. Read `AGENTS.md`, `PLAN.md`, `HANDOFF.md`,
   `research/jev-controller-v2-research.md`,
   `research/jev-ecosystem-evidence.md`,
   `research/jev-long-horizon-ab.md`, and `spec/jev-controller-v2.md`.
2. Read the combined result `reports/jev-long-ab-20260922.md` and the three
   per-harness reports before changing code.
3. Implement only the one follow-up hypothesis in `checkpoints/CURRENT.md`:
   low-confidence Jev handling should execute the baseline-equivalent feeder
   prompt while recording the Jev answer as advisory.
4. Rerun one fresh matched 60-turn development A/B slice under a new `run_id`;
   keep the six holdout hashes sealed and compare only with the Work reference.
5. Update `checkpoints/CURRENT.md` with the measured result and one next action.

## v2 implementation checkpoint — 2026-09-21

The first reusable v2 slice is now implemented. `src/hos/controller/core.py`
contains `DecisionContext`, typed question construction and parsing, legal
phase/action validation, deterministic fallback, and `JevDecisionLoop`;
`src/hos/controller/adapters.py` contains normalized event and native-session
metadata extraction. The v1 APIs and pilot remain intact.

Focused tests cover the fake three-round loop, context accumulation, provider
answer parsing, fallback safety, and independent OpenCode/Grok Build/Pi event
handling. A fresh matched three-hash run is recorded in
`reports/matched-replay-jev-v2-20260921.md`; it found 6/9 low-confidence Jev
fallbacks, 7/9 baseline timeouts, no Work matches, and repeated two-decision
loops on one hash per adapter. Variance is explicitly unclaimed because this
was one repetition. The exact next hypothesis is in `checkpoints/CURRENT.md`.

Jev remains OpenRouter-only. It receives no tool authority. The adapters own
CLI execution, event capture, and normalized tool observations.

## External Jev evidence checkpoint — 2026-09-21 (historical finding)

Public OSS examples confirm that Jev does not read files or discover live
state. The host or a worker must feed Jev the current observations and closed
candidate set. Our first v2 runner did not have that context-feeder preflight:
it sent the owner ask, a synthetic bead, generic constraints, and mostly empty
state fields, then folded back adapter metadata after execution. The prior
`CLASSIFY_REQUEST`-only hypothesis was therefore paused. Issue 22 subsequently
added the smallest bounded feeder and reran the full matched slice; its result
and the one remaining hypothesis are recorded above and in `CURRENT.md`.

## Reference evidence

Primary reference: local ChatGPT Work codex_work_desktop, originators kept separate.

One-pager: reports/codex-originator-dashboard.md. Keep originators separate; **do not average** Work with vscode, codex_exec, or Desktop.

Existing v0 evidence remains valuable:
- hashed corpus ~1521 files;
- Work 87 sessions / 83 with calls;
- wait 31/83, send 25, spawn 2, update_plan 0, patch 1/83;
- Kilo/OpenCode Codex-mode prompts;
- R1-R6 scorer;
- 22 long Work replay threads (16 develop, 6 holdout);
- morph/replay reports.

Those counts are diagnostics, not the full definition of good behavior.

The richer target includes interaction shape, research, observation, waits, verification, provenance, output behavior, corrections, context/continuity, outcome, and repeated-run variance.

## Continuity

Read checkpoints/CURRENT.md for the exact next action. GitHub Issues hold executable experiment scope and pass conditions. Do not recover project state from chat history if repository state exists.

Update CURRENT after real experimental work, not after discussion-only turns.

## Historical planning package

spec/harness-agnostic remains useful architecture/research thinking, but the final owner-approved operating contract is spec/harness-agnostic/12-owner-accepted-operating-contract.md.

Where earlier package text requires a large prebuilt protocol/state-machine architecture, owner spec v2 and file 12 win: start with the empirical multi-harness loop and earn additional machinery from observed failures.

## Existing files

Do not wipe v0 for cleanliness. Git history is the archive. Existing modes/scorers/replays remain baseline/history until a measured replacement plus audit mapping exists.

## Privacy

Never commit raw JSONL, SQLite, replay prompt bodies, credentials, private account exports, user artifacts, or unsafe identifiers.

## Long-running mode

This accepted plan does not automatically start /goal. CONTINUE.md applies only after a specific goal and explicit owner go-ahead. Ordinary status/conversation still answers first.

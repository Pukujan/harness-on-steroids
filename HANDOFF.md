# Handoff

**Owner precedence:** AGENTS.md -> PLAN.md -> checkpoints/CURRENT.md -> active GitHub issue -> HANDOFF.md -> ISSUES.md.

## Current direction

The owner accepted the model- and harness-agnostic behavioral-control reset on **2026-09-21**.

The project now learns from the complete observable behavior in local ChatGPT Work/Codex transcripts and transfers those supported behaviors through the smallest effective control-layer changes. Prompt/context engineering remains the first intervention. A general runtime state machine is not pre-authorized; runtime guards are added only when repeated evidence earns them.

Normal development runs **Pi + OpenCode + Grok Build in the same slice** where technically possible. Record exact model/provider/harness/config, but do not make any model the product boundary.

Kilo Codex v0 remains a positive-control baseline and historical proof that behavior prompting can materially improve a harness.

## Analytical machine checkpoint — 2026-09-22

The current bounded implementation slice is Issue 23, documented in
`docs/analytical-machine-v0-plan.md` and tracked in `ISSUES.md`. The reusable
module is `src/hos/analysis_machine/`.

It normalizes the imported Codex envelope JSONL and existing ChatGPT
provenance normalized views into body-minimized, versioned `CanonicalEvent`
records, then computes separate Codex execution and ChatGPT chat/research
summaries. Normalization and aggregation are streamable; summary-only runs
write only local `manifest.json` and `summary.json`, while event exports remain
optional. Raw transcript bodies, SQLite, and credentials remain ignored.

AM-01 through AM-05 are complete with focused tests and a real bounded pilot.
One Codex session plus one ChatGPT provenance conversation produced 5,525
events across three episodes, with zero parse errors, zero validation issues,
100% known-event coverage, and byte-identical repeat exports. This proves
repeatability and contract behavior, not agent quality. A corrected full
structural pass over 2,173 local JSONL sources produced 556,241 events across
1,499 episodes: 419,893 Codex events in 1,387 episodes and 136,348 ChatGPT
events in 112 episodes. Exact duplicate tracking with a 600,000-ID cap found
zero duplicate IDs and zero validation issues; 28,565 events remained unknown
and zero parse errors were observed. See
`reports/analysis-machine-full-corpus-20260922.md`. AM-06's pilot and sealed
holdout checks are now recorded in
`research/analysis-ontology-pilot-20260922.md`; no quality or outcome labels
were promoted. AM-06b's larger pilot and advisory review are recorded in
`research/analysis-ontology-pilot-v3-review-20260922.md`; the exact next action
is owner/human adjudication of that source-linked structural batch. Do not
build a graph database/dashboard yet.

Sol reviewed the design through the repository's bounded CKFF worker. The
useful warning was that deterministic output is not automatically valid:
contract, source identity, duplicate policy, missing-data status, provenance
coverage, ontology version, analyzer version, and alias-map version must all
be visible in the export. Provider routing is explicit: Sol is CKFF-only; Luna
is native Codex/ChatGPT subagent-only and never CKFF. The AM-06 pilot used two
independent native Luna annotation passes plus two fresh holdout passes;
they remain advisory/read-only checks, not human gold annotation.

## External Jev OSS architecture deep dive — 2026-09-22

`research/jev-oss-architecture-deep-dive-20260922.md` is the durable source-
backed comparison of Jev Ultrafast, Stanley, JevWire, pi-jev, pi-typesafe,
pi-jev-tools, TypeSafe Router, and the TypeSafe playground examples. It
inspected actual source/architecture files and pinned the observed upstream
`main` commits, rather than relying on assumptions about Jev.

The shared finding is that Jev does not read files, discover project direction,
or execute actions. A host observer or subagent must supply bounded state and a
closed candidate set; host code validates the response, applies policy, and
executes or abstains. Stanley is the closest coding-agent pattern: deterministic
workflow eligibility and evidence collection around small Jev questions, with a
general coding agent only as an explicitly unverified fallback.

The deep dive recommends reusing patterns first: a bounded workflow registry,
provider-neutral response validation, local evidence retrieval, freshness
checks, independent verification, and advisory/shadow modes. It does not
authorize a general orchestration framework or change the current next action.

The focused classification/capture verdict is recorded in
`research/jev-classification-capture-20260922.md`: use Jev only as a bounded
classifier/selector or advisory shadow annotator; keep complete data capture,
provenance, execution, and verification deterministic and host-owned. Public
Jev Ultrafast and TypeSafe playground implementations follow this same
boundary. Our matched A/B did not show an outcome gain and was heavily
under-executed by the confidence gate.

The first live Jev shadow-classification probe is recorded in
`reports/jev-shadow-annotation-20260922.md`. It used eight body-free pilot
events and eight independent Noul predicates (64 valid probabilities): 62/64
matched direct canonical-field labels at a 0.50 threshold; a 0.75 acceptance
band accepted 59/64 with zero errors and five abstentions. This is a small
structural wire/behavior probe, not semantic-quality evidence. The v3 holdout
remained sealed, and the next annotation step still requires owner/human
adjudication plus a larger repeated semantic-label study. Two additional
repeats produced the same thresholded predictions for all 64 questions, while
probabilities varied modestly (mean range 0.0112, maximum 0.08).

The selector was then fixed to fill a requested sample budget beyond the
minimum coverage set. Three fresh 32-event structural repeats returned
256/256 valid probabilities and 254/256 direct-label matches each; all
thresholded predictions were identical across runs. Mean probability range
was 0.0100 and maximum 0.11. At a 0.75 acceptance band the first run accepted
243/256 with 13 abstentions; each repeat accepted 240/256 with 16 abstentions.
No accepted label was wrong in any run. This remains structural sidecar
evidence; semantic labels still require owner/human adjudication and the
holdout remains sealed.

## Harness timeout reliability policy — 2026-09-22

The attempted advisory A/B was stopped before interpretation when the owner
identified the old 60-second hard process timeout as unsuitable for active
streaming. The adapter policy is now a configurable 20-minute default
inactivity timeout reset by stdout/stderr progress plus a two-hour absolute
safety cap. An actively streaming one-hour task is allowed; elapsed task time
alone is not a kill reason. OpenCode and Pi
provider-side idle/header/chunk settings use the 20-minute boundary while
total request ceilings use the two-hour cap, so active streams are not cut off
at the idle threshold. Timeout reasons are typed and reported; see
`docs/harness-timeout-policy.md`. The advisory A/B must be rerun under this
policy with a fresh run ID.

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
   `research/jev-ecosystem-evidence.md`, `research/jev-long-horizon-ab.md`,
   `research/jev-oss-architecture-deep-dive-20260922.md`, and
   `spec/jev-controller-v2.md`.
2. Read the combined result `reports/jev-long-ab-20260922.md` and the three
   per-harness reports before changing code.
3. Implement only the one follow-up hypothesis in `checkpoints/CURRENT.md`:
   low-confidence Jev handling should execute the baseline-equivalent feeder
   prompt while recording the Jev answer as advisory.
4. The fresh matched 60-turn development A/B slice is currently running as
   `jev-long-ab-advisory-20260922-v2`; keep the six holdout hashes sealed and
   compare only with the Work reference. Do not restart or interpret partial
   turn directories as final evidence.
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

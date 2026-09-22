# Issue log - durable history and active mapping

Active executable work now lives in GitHub Issues. This file preserves repository issue history and maps the current owner direction.

Read AGENTS.md -> PLAN.md -> checkpoints/CURRENT.md -> active GitHub issue first.

## v0 historical lineage - issues 1-18

Issues 1-18 belong to the original "Kilo/OpenCode imitate Work" phase. Their detailed wording is preserved in Git history through commit 9e01f8a and the related reports/specs.

They produced durable evidence that remains useful:
- owner/property/holdout/mutation/metamorphic/differential CI gates;
- full Work/Codex corpus analysis;
- spec/codex-imitate-mode.md;
- Kilo and OpenCode Codex-mode prompts;
- R1-R6 scorer and gap reports;
- matched-task 22-thread develop/holdout scaffold and morphs;
- research/provenance/continuity questions;
- src/hos foundation/lint/type work.

Their incomplete status does **not** make them the active roadmap after owner spec v2. They are v0 baseline/history unless a current GitHub issue explicitly reuses them.

Historical needle retained for old regression tests: 18. Repo modules, lint, types. Do not replace 8-18 by deleting their evidence/tests.

## 19. Harness-agnostic reset proposal

- **Status:** done
- **Result:** architecture proposal reviewed, then accepted by owner with a simpler operating refinement.
- **Files:** spec/harness-agnostic, especially 12-owner-accepted-operating-contract.md
- **Important refinement:** prompt/context-first empirical iteration; Pi/OpenCode/Grok Build together; model-agnostic; no pre-required runtime state machine.

## 20. Governance switch / owner spec v2

- **Status:** done
- **Goal:** make the accepted direction authoritative and remove the old Kilo/OpenCode-only governance conflict.
- **Files:** AGENTS.md, PLAN.md, spec/owner.v2.*, HANDOFF.md, CONTINUE.md, checkpoints/CURRENT.md, governance tests.
- **Pass:** owner docs/tests point to v2; v1 remains history; active work is GitHub issue #2.

## Active GitHub work

### Issue 21 - Jev persistent decision controller

- **Status:** open; owner approved implementation on 2026-09-21.
- **Research:** `research/jev-controller-v2-research.md`.
- **External evidence:** `research/jev-ecosystem-evidence.md` records public
  Jev integrations and the required context-feeder boundary.
- **OSS architecture deep dive:**
  `research/jev-oss-architecture-deep-dive-20260922.md` inspects Jev
  Ultrafast, Stanley, JevWire, pi-jev, pi-typesafe, pi-jev-tools, TypeSafe
  Router, and the TypeSafe playground at pinned upstream commits. It confirms
  that Jev is decision-only and identifies MIT-licensed patterns we can port
  after review: bounded workflow registries, evidence retrieval, response
  validation, freshness checks, and independent verification.
- **Contract:** `spec/jev-controller-v2.md`.
- **Problem:** the first Jev replay used one compact state request and one
  prompt hint per task. It did not test Jev as a context-aware classifier,
  bead selector, or repeated decision controller.
- **Intervention:** add a persistent context accumulator, typed Jev questions,
  candidate bead selection, legal transition validation, repeated decisions,
  and adapter event feedback. Keep the old pilot as v1 smoke evidence.
- **Fixtures:** existing develop Work hashes; Pi, OpenCode, and Grok Build in
  the same matched slices where technically possible.
- **Pass condition:** the v2 runner makes repeated decisions from updated
  context, passes fake-adapter and adapter-stream tests, and produces a
  hash-only baseline-versus-Jev report with R1-R6, work-match, outcome, and
  timeout measurements.
- **Stop condition:** stop after the smallest working loop and one matched
  replay; do not expand into a general protocol framework without a measured
  failure that requires it.

The research and contract are the durable issue record for this slice. A
future session should begin with them and `checkpoints/CURRENT.md`.

**First implementation slice (2026-09-21):** the reusable context/loop,
provider schema parser, legal-action fallback, and independent adapter event
normalizers are implemented and tested. Fresh replay
`jev-v2-matched-20260921` covers three development hashes across OpenCode,
Grok Build, and Pi. Six of nine Jev arms stopped at the low-confidence gate;
the three executed arms made two decisions each but timed out, and no arm
reached a Work match. Baselines timed out 7/9 times. The result is recorded in
`reports/matched-replay-jev-v2-20260921.md`; variance is not claimed because
the slice has one repetition. The first replay tested loop mechanics with
mostly empty decision context; it did not test observation-derived candidate
selection. Public OSS evidence shows that the host must feed Jev live state
and a closed candidate set. The next controlled hypothesis is therefore the
bounded context-feeder preflight recorded in `checkpoints/CURRENT.md`; the
`CLASSIFY_REQUEST` choice-set change is paused until that feeder is present.

### Issue 22 - Jev long-horizon matched A/B

- **Status:** active; first 60-turn A/B slice complete, follow-up hypothesis
  retained below.
- **Research contract:** `research/jev-long-horizon-ab.md`.
- **Question:** does Jev improve observable Work-aligned behavior and outcome
  when the no-Jev and Jev arms receive the same context, harness, model,
  workspace, and user turns?
- **Gold/reference:** local ChatGPT Work/Codex transcripts; 16 development
  hashes for tuning and six hidden holdout hashes sealed. Work-derived
  taxonomy and R1-R6 remain diagnostic signals, not exact tool-order rules.
- **Matrix:** OpenCode + Pi use the configured `yolo-auto/qwen3.8-flash`;
  Grok Build uses configured `grok-4.7`; Jev is the separate
  `typesafe/jev-1.13` OpenRouter Decisions call.
- **Scale:** exactly 60 matched development user turns per arm and available
  harness, preserving per-hash long-running context. At least three turns are
  allocated to every development hash before filling the remaining budget in
  frozen order.
- **Intervention:** add only the validated Jev decision between the shared
  context feeder and the harness invocation. Baseline gets the same feeder
  pack without the Jev answer.
- **Pass/stop:** produce comparable hash-only aggregates for all available
  harnesses, then retain Jev only if outcome/behavior improves without harming
  verification, safety, continuity, scope, or truthful reporting.
- **Privacy:** raw prompts, transcript bodies, event bodies, credentials, and
  private files remain ignored/local.

**Measured result (2026-09-22):** the clean slice completed on all three
available harnesses. Each arm had 60 matched turns over all 16 development
hashes, with 120 hash-only rows per harness and no `fail_1` launch rows. The
baseline/Jev Work-match counts were OpenCode 8/16 vs 4/16, Grok Build 0/16
vs 0/16, and Pi 0/16 vs 0/16. Jev executed only 13, 13, and 12 turns after
47, 47, and 48 low-confidence fallbacks. The current policy is therefore not
promoted; see `reports/jev-long-ab-20260922.md`.

**Next hypothesis:** keep the feeder, choices, models, fixtures, and timeouts
fixed, but make a low-confidence Jev result advisory while executing the same
feeder prompt as baseline. Rerun one fresh matched 60-turn development slice
to separate action-selection value from confidence-gate under-execution.

**Timeout policy correction (2026-09-22):** the first advisory rerun was
stopped before interpretation because the runner still imposed a 60-second
hard wall-clock kill. The adapter now uses a 3-minute default inactivity
timeout reset by stream progress plus a two-hour absolute cap; timeout reasons
are retained.
The advisory slice `jev-long-ab-advisory-20260922-v2` was later stopped before
interpretation when the owner shortened the default inactivity boundary to
3 minutes. Its partial folders are not evidence; a fresh run ID is required.
Fresh run `jev-long-ab-advisory-20260922-v3` is now running under the 180-second
policy with the same matched fixtures; its partial run was stopped before
interpretation when Windows process-tree cleanup was tightened. Start a fresh
run after that correction; do not mix v3 artifacts into its aggregate. Fresh
run `jev-long-ab-advisory-20260922-v4` is now active under the corrected policy
and is the only run eligible for interpretation.

### Issue 23 - Reusable analytical machine v0

- **Status:** active; implementation, full structural pass, and the larger
  advisory ontology pilot/holdout review are complete; owner/human
  adjudication is next.
- **Goal:** create a repeatable and exportable analysis machine that can be
  reused for future agent datasets, with separate Codex execution and
  ChatGPT chat/research analyzers over one body-minimized evidence contract.
- **Contract:** `docs/analytical-machine-v0-plan.md`.
- **Implementation:** `src/hos/analysis_machine/` provides versioned canonical
  events, Codex/ChatGPT JSONL adapters, streaming lane summaries, local
  manifest/optional-events/summary export, body-free fingerprints, and
  validation issues.
- **Beads:** AM-01 through AM-05 are complete; AM-06 advisory ontology
  pilot/holdout review is complete with no category promotion; AM-06b's larger
  deterministic sample and four native Luna advisory reviews are complete,
  while owner/human adjudication remains. The deterministic review packet
  builder is `research/build_analysis_review_packet.py`; AM-07 graph projection
  and AM-08 dashboard are explicitly deferred.
- **Validation:** contract, golden fixture, order invariance, unknown-field,
  alias, body-minimization, mutation, and differential checks. Existing
  `score_seq` is a compatibility diagnostic, not objective gold.
- **Measured first slice:** one Codex session plus one ChatGPT provenance
  conversation produced 5,525 events across three episodes, zero parse errors,
  zero validation issues, 100% known-event coverage, and byte-identical repeat
  exports. This is contract/repeatability evidence, not an agent-quality claim.
- **Measured full structural pass:** 2,173 local JSONL sources produced
  556,241 events across 1,499 episodes: 419,893 Codex events / 1,387 episodes
  and 136,348 ChatGPT events / 112 episodes. Exact duplicate tracking with a
  600,000-ID cap found zero duplicate IDs and zero validation issues; 28,565
  events remained unknown and zero parse errors were observed. This is adapter/coverage
  evidence, not a quality claim. See
  `reports/analysis-machine-full-corpus-20260922.md`.
- **Next pass:** owner/human-adjudicate the v3 source-linked structural batch
  recorded in `research/analysis-ontology-pilot-v3-review-20260922.md`, with
  quality/UX/outcome/planning labels remaining abstained until their evidence
  surface is defined.
- **Jev sidecar probe:** a separate eight-event structural Noul probe is
  recorded in `reports/jev-shadow-annotation-20260922.md`; it is not gold or a
  controller result. Keep the holdout sealed and benchmark semantic Jev labels
  only after owner/human adjudication. The selector now honors larger sample
  budgets; three fresh 32-event repeats produced 254/256 direct structural
  matches each with identical thresholded predictions. This strengthens the
  mechanical sidecar result but does not promote semantic labels.
- **Stop:** do not promote ontology terms, add a graph database, or build
  Power BI views before the bounded pilot is annotated and inspected.
- **Privacy:** raw JSONL/SQLite and local derived exports remain ignored;
  committed artifacts contain only code, contracts, tests, and aggregate
  evidence.

### GitHub issue #2 - Baseline multi-harness Work behavior replay

- **Status:** open
- **Goal:** baseline 3-5 existing development tasks across Pi, OpenCode, and Grok Build before changing control.
- **Intervention:** none initially.
- **Pass:** comparable traces or explicit non-comparable reasons; largest recurring deviations identified; exactly one smallest next control hypothesis selected.
- **Scope:** do not turn this into a general state-machine/protocol framework.
- **Blocking defect found (v66):** the replay runners sent the raw first user turn, which
  in these Work transcripts is the `<recommended_plugins>` / `<environment_context>`
  preamble. For **11 of the 22** develop+holdout hashes that turn contains no ask at all,
  so any baseline trace on those hashes measures behaviour on a **task-free prompt**,
  and a controller/hint arm that adds a directive would look effective purely because it
  supplied the only instruction. Extraction is fixed (`research/replay_lib.py`
  `strip_context_blocks` / `first_ask` / `ask_turns`, gate
  `tests/test_replay_prompt_hygiene.py`). Before this issue's baseline is trusted: move
  the old `data/replay/<hash>/opencode.ndjson` aside per hash (the runner **appends**, so
  re-running in place mixes old and new evidence) and regenerate
  `reports/replay-scores.md`, whose OpenCode column is flagged contaminated for those 11
  in `reports/versions/v66/README.md`.

## Rules for future issues

- Keep only a small number of active issues.
- One main behavior hypothesis per normal implementation issue.
- Each issue must name its baseline, intervention, fixtures, measurable pass/stop condition, and privacy/scope boundaries.
- Do not pre-create a speculative large backlog.
- Preserve v0 evidence/tests unless deliberately retired with an audit mapping.
- Never commit data/, transcript bodies, credentials, or private exports.

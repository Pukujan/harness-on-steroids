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

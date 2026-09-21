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

### GitHub issue #2 - Baseline multi-harness Work behavior replay

- **Status:** open
- **Goal:** baseline 3-5 existing development tasks across Pi, OpenCode, and Grok Build before changing control.
- **Intervention:** none initially.
- **Pass:** comparable traces or explicit non-comparable reasons; largest recurring deviations identified; exactly one smallest next control hypothesis selected.
- **Scope:** do not turn this into a general state-machine/protocol framework.

## Rules for future issues

- Keep only a small number of active issues.
- One main behavior hypothesis per normal implementation issue.
- Each issue must name its baseline, intervention, fixtures, measurable pass/stop condition, and privacy/scope boundaries.
- Do not pre-create a speculative large backlog.
- Preserve v0 evidence/tests unless deliberately retired with an audit mapping.
- Never commit data/, transcript bodies, credentials, or private exports.

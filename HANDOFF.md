# Handoff

**Owner precedence:** AGENTS.md -> PLAN.md -> checkpoints/CURRENT.md -> active GitHub issue -> HANDOFF.md -> ISSUES.md.

## Current direction

The owner accepted the model- and harness-agnostic behavioral-control reset on **2026-09-21**.

The project now learns from the complete observable behavior in local ChatGPT Work/Codex transcripts and transfers those supported behaviors through the smallest effective control-layer changes. Prompt/context engineering remains the first intervention. A general runtime state machine is not pre-authorized; runtime guards are added only when repeated evidence earns them.

Normal development runs **Pi + OpenCode + Grok Build in the same slice** where technically possible. Record exact model/provider/harness/config, but do not make any model the product boundary.

Kilo Codex v0 remains a positive-control baseline and historical proof that behavior prompting can materially improve a harness.

## Active issue

Local issue **21 - Jev persistent decision controller**. The durable research
and contract are `research/jev-controller-v2-research.md` and
`spec/jev-controller-v2.md`; `ISSUES.md` contains the issue mapping.

The old three-adapter Jev run is complete as a v1 routing smoke test. It used
one compact decision and one prompt hint per task. Do not treat it as evidence
that Jev can decompose tasks or control a long horizon.

Historical active issue label: GitHub issue **#2 - Baseline multi-harness Work behavior replay**.

The next implementation is Jev Controller v2: assemble the full relevant
decision context, ask typed Choice/Score/Noul questions, validate the selected
bead/action against legal transitions, execute one bounded adapter step, fold
the resulting events back into context, and ask Jev again.

The next session should:

1. Read `AGENTS.md`, `PLAN.md`, `HANDOFF.md`,
   `research/jev-controller-v2-research.md`, and `spec/jev-controller-v2.md`.
2. Inspect the current `src/hos/controller` module and preserve the v1 pilot.
3. Add the reusable `DecisionContext` and repeated `JevDecisionLoop` with fake
   adapter tests before live calls.
4. Audit OpenCode, Grok Build, and Pi event streaming/session behavior.
5. Run one OpenCode smoke task, then a matched baseline-versus-loop slice on
   existing develop Work hashes.
6. Update `checkpoints/CURRENT.md` with measured results and one next action.

Jev remains OpenRouter-only. It receives no tool authority. The adapters own
CLI execution, event capture, and normalized tool observations.

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

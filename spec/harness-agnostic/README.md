# Harness-agnostic behavior system — planning package

Status: **proposal only**. This package changes the planning target; it does not authorize implementation, replay execution, prompt tuning, deletion, or repository cleanup.

The durable goal is a repeatable, harness-agnostic system that can project the observable strengths of ChatGPT Work/Codex onto Pi, Kilo, OpenCode, and future harnesses. Kilo and OpenCode are examples of adapters, not the product boundary.

This package is intentionally separate from the current owner plan. `PLAN.md`, `AGENTS.md`, and the existing issue gates remain authoritative until the owner accepts or edits this proposal.

## Package map

| File | Purpose |
| --- | --- |
| `00-executive-brief.md` | New target, scope, non-goals, and acceptance shape |
| `01-current-state-audit.md` | What the repository has proved, what is incomplete, and what becomes historical |
| `02-evidence-and-provenance.md` | Evidence plane, lineage, context, and repository-safe data contract |
| `03-behavior-and-ux-research.md` | Research design for behavior, UX, decisions, and ambiguity |
| `04-work-behavior-protocol.md` | Harness-neutral lifecycle and semantic obligations |
| `05-action-plan-and-execution.md` | Research-to-action planning, execution, verification, and recovery |
| `06-continuity-and-handoff.md` | Compaction, restart, delegation, wait, and handoff contracts |
| `07-adapter-and-capability-contract.md` | Host responsibilities, capability negotiation, and adapter shape |
| `08-verification-and-evaluation.md` | Verifiers, properties, outcome rubrics, splits, and promotion gates |
| `09-migration-and-rebuild.md` | How to preserve evidence while treating current code as disposable |
| `10-owner-decisions-and-handoff.md` | Resolved planning defaults and the approval handoff |\n| `11-owner-review.md` | Architecture review, amendments, risks, and acceptance recommendation |

## Reading order for a future planner

Read `AGENTS.md`, `PLAN.md`, `ISSUES.md`, then this package. Read the package in numeric order. Do not infer approval from its presence in GitHub.

## Evidence boundary

The package contains only aggregate counts, schemas, labels, hashes, and structural findings. Raw JSONL, SQLite, prompts, transcript bodies, credentials, and user artifacts remain local and are not part of this package.

The companion provenance-exporter work demonstrated that a richer source can preserve raw nodes before parsing, normalized records, rendered views, reconciliation, and hashes. That is an upstream evidence-plane concern. Harness on Steroids should consume a versioned, redacted event interface instead of growing a second transcript parser.

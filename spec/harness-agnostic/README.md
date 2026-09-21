# Harness-agnostic behavior system - planning package

Status: **owner accepted with operating-contract refinement on 2026-09-21**.

This directory records the architecture reset discussion and the research areas it exposed. The final owner-approved operating contract is 12-owner-accepted-operating-contract.md plus the authoritative AGENTS.md / PLAN.md.

The durable goal is model- and harness-agnostic behavioral control learned from observable ChatGPT Work/Codex evidence. Pi, OpenCode, and Grok Build are the normal concurrent development surfaces; Kilo Codex v0 is preserved as a positive-control baseline/history.

The owner deliberately simplified the original proposal: do **not** pre-build the whole semantic protocol/runtime/state-machine architecture. Start with the existing fast empirical loop, enrich the observable reference signals, use prompt/context/capability control first, and add runtime enforcement only when repeated measured failures earn it.

## Package map

00-executive-brief.md through 11-owner-review.md preserve the original proposal/review context.

12-owner-accepted-operating-contract.md is the **final accepted refinement and wins inside this package on conflict**.

## Reading order

Read AGENTS.md -> PLAN.md -> checkpoints/CURRENT.md -> active GitHub issue. Use this package for research/architecture context, not as a license to implement every proposed subsystem.

## Evidence boundary

Raw JSONL, SQLite, prompts/transcript bodies, credentials, private account exports, and user artifacts remain local.

The companion provenance-exporter work may enrich the source evidence. Harness on Steroids should consume approved redacted/derived interfaces rather than growing a second private-data copy.

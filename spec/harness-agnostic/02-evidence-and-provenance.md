# Evidence and provenance contract

## Boundary

The provenance exporter is the evidence plane. It owns lossless source capture, raw preservation, parsing, normalization, rendered views, reconciliation, and integrity. Harness on Steroids consumes a versioned evidence interface and owns annotations, behavior hypotheses, protocol rules, adapters, and evaluation.

No second parser should be grown inside the harness project merely to access a convenient field.

## Canonical event shape

The future evidence interface should expose an append-only event stream. Exact field names can be decided during implementation, but every event needs these semantic fields:

- schema and extractor version;
- stable event ID, ordinal, timestamp, and source pointer;
- source digest and integrity status;
- hashed conversation, thread, turn, exchange, request, work, and run identifiers;
- parent/child and call/result relationships;
- actor, role, channel, lifecycle status, end-turn state, and weight;
- observed harness/originator, model, client, plugin, connector, and capability metadata;
- event kind: message, content, tool call, tool result, lifecycle, wait, compaction, citation, artifact, handoff, permission, or error;
- content kind: text, code, multimodal text, execution output, thoughts, reasoning recap, or unknown;
- tool identity, semantic capability, arguments/result shape, asynchronous state, duration, and error class;
- observation state: `observed`, `not_observed`, `unknown`, `inaccessible`, or `not_applicable`.

Missing data must never silently become a negative fact.

## First-class context

A trace is uninterpretable without its operating context. Export or reconstruct a redacted context record containing:

- original user request and later corrections, approvals, scope changes, and stop signals;
- starting workspace/repository identity and relevant state summary;
- available tools, skills, permissions, models, plugins, and UI surfaces;
- harness instructions and collaboration mode;
- ancestry, resumption, compaction, and handoff boundaries;
- child tasks and delegated ownership;
- expected artifacts, produced artifacts, and verification status;
- terminal state: complete, partial, blocked, failed, or interrupted.

## Required indexes

The evidence plane should make these relationships queryable without re-reading raw message bodies:

1. tool call/result and asynchronous lifecycle index;
2. claim/source/citation index;
3. artifact producer/consumer/verifier index;
4. parent/child task and handoff index;
5. failure/retry/recovery/revision index;
6. conversation/turn/episode/decision-point index;
7. compaction/rehydration index;
8. user correction/approval/authority index.

## Research-to-action lineage

The durable chain is:

```text
source event
  -> observation or claim
  -> decision-point evidence set
  -> plan item
  -> authorized native action
  -> observed result
  -> verification evidence
  -> accepted, revised, recovered, or blocked outcome
```

Every normative behavior rule must point to supporting observations and known counterexamples. Every final claim in an evaluated run must point to verification evidence, not only to the action that was attempted.

## Identifier and ordering rules

Stable identifiers must not create a new privacy leak. Source-native opaque IDs may remain local. New derived identifiers should be deterministic only within the local evidence domain, preferably keyed/HMAC-derived when their input could be guessed. Public reports may contain only explicitly approved structural identifiers or redacted aliases; they must not expose raw paths, account IDs, user names, prompt text, or reversible content-derived IDs.

Event order is defined primarily by source ordinal and explicit parent/call/result relations. Wall-clock timestamps are supporting evidence, not the sole ordering authority, because clocks can be absent, duplicated, skewed, or reconstructed. Unknown ordering must remain unknown rather than being guessed.

## Repository-safe data policy

Git may contain schemas, aggregate counts, structural labels, versioned hashes, redacted examples, and reproducible check definitions. Git must not contain raw JSONL, SQLite, prompt bodies, transcript bodies, credentials, private account exports, or user artifacts.

The local provenance-exporter inspection found that complete bundles can preserve raw-before-parse data, normalized records, rendered turns, reconciliation, and hashes, while partial account captures can still be validated at the raw/derived conservation layer. That supports this boundary; it does not authorize copying those captures into this repository.

# Owner review — harness-agnostic reset

Date: 2026-09-21

## Disposition

**Recommend acceptance with the amendments recorded in this review.**

The proposal fixes the central architectural problem in the current repository: behavior is presently represented too strongly by prompt text and tool-order diagnostics. The new package correctly moves the durable product boundary to a harness-neutral semantic protocol backed by evidence lineage, capability negotiation, semantic verification, continuity, and outcome evaluation.

The proposal should not be implemented exactly as first drafted, however. Two issues are architectural rather than editorial: the lifecycle must support nested/concurrent task state, and capability negotiation must produce a persisted run-specific result rather than stopping at a static manifest. Those amendments are incorporated into the package by this review.

## What is strong enough to keep

- ChatGPT Work/Codex remains the reference evidence population rather than being replaced by a public benchmark.
- Kilo and OpenCode become adapters instead of defining the architecture.
- Pi and future harnesses are included at the protocol boundary without requiring them to share tool names.
- Evidence/provenance and research-to-action lineage are first-class.
- Missing observations are represented explicitly rather than converted into negative facts.
- Verification and user-visible outcomes replace raw tool-order scores as promotion gates.
- Compaction, restart, handoff, wait, recovery, permission, and partial completion are modeled as semantics.
- Existing reports, scorers, modes, and replay work are preserved as historical/prototype evidence rather than deleted.

## Required corrections made by this review

### 1. Flat lifecycle -> hierarchical task protocol

A run can contain concurrent children, blocked dependencies, asynchronous waits, retries, and separate verification states. A single sequence of run-level phases cannot represent that faithfully. Protocol v1 therefore distinguishes:

`run -> task graph -> attempt phases`

with run terminal states `complete`, `partial`, `blocked`, `failed`, and `interrupted`.

### 2. Manifest -> negotiation handshake

A capability manifest describes what a harness claims to support; it does not say what a particular protocol run can actually guarantee. Each run therefore needs a persisted negotiated profile mapping required semantic capabilities to native/emulated operations and declaring enforced, advisory, degraded, or incompatible guarantees.

### 3. Ambiguous normative terms -> protocol definitions

Terms such as “consequential,” “material,” “authority,” and “verified” must mean the same thing across Pi, Kilo, OpenCode, and future adapters. Product-specific tool names cannot define them.

### 4. Outcome comparison -> predeclared acceptance contract

Matched-task evaluation must freeze the user-visible acceptance criteria and environment fidelity before adapter tuning. Otherwise exact Work artifacts or late-selected metrics can become accidental answer keys.

### 5. Model confounding -> explicit strata

Harness effects and model effects must not be silently mixed. Use a common model across harnesses where available, plus realistic native/default-model runs. Keep unmatched model strata separate.

### 6. Public hashes -> privacy review

A hash is not automatically safe. Newly derived public identifiers must be explicitly approved as non-reversible/non-sensitive; keyed local identifiers are preferred when inputs could be guessed.

### 7. Proposal acceptance -> atomic governance transition

The current `AGENTS.md` and `PLAN.md` still define the two-adapter imitate-Codex plan. If this reset is accepted, update governance and its invariants/tests deliberately in one change. Do not allow the implementation to operate under two contradictory sources of truth.

## Risk register

| Risk | Required control |
| --- | --- |
| Protocol becomes another hidden agent loop | Keep model invocation/tool scheduling in host; protocol only defines semantics/state/verifiers |
| “Work-like” becomes exact transcript imitation | Score semantic obligations/outcome; exact tool names and prose are diagnostic only |
| Capability gaps are papered over | Persist negotiated profile and degraded/incompatible guarantees |
| Research labels smuggle in hidden reasoning | Annotate only observable events/results/recaps; record ambiguity and counterexamples |
| Evaluation overfits 22 replay threads | Freeze leakage groups, acceptance contracts, thresholds, and holdout before tuning |
| Environment mismatch looks like harness failure | Tier environment fidelity; mark essential unreconstructable cases non-comparable |
| Runtime claims exceed enforcement | Separate enforced/advisory/emulated guarantees and test them independently |
| New provenance IDs leak private inputs | Keep raw/source IDs local; approve only safe aliases/hashes for Git |
| Reset destroys useful historical evidence | Retire only behind versioned replacements and audit mappings |
| Adapter optimization harms outcomes | Stop when process improves while outcome/safety regresses |

## Decision resolutions

The ten owner questions are resolved as recommended defaults in `10-owner-decisions-and-handoff.md`. The key ordering is: hard safety/authority/privacy/evidence constraints first; then verified task outcome; research sufficiency; continuity/recovery; honest UX; delegation; cost/latency; stylistic similarity.

## Acceptance gate

This document records the architectural review and recommended resolution. It **does not impersonate owner acceptance**. Until the owner explicitly accepts the reset, `AGENTS.md` and `PLAN.md` remain authoritative and no implementation, replay expansion, prompt rewrite, or cleanup begins.

After owner acceptance, the first authorized work is the read-only evidence/contract slice in `10-owner-decisions-and-handoff.md`, followed by another approval gate before runtime/adapters.

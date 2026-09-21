# Adapter and capability contract

## Host/protocol split

### Portable protocol owns

- semantic lifecycle and valid transitions;
- evidence obligations and observation states;
- task/dependency and action-plan representation;
- verification, retry, recovery, escalation, and stop rules;
- handoff, checkpoint, compaction, and rehydration requirements;
- UX obligations;
- conformance fixtures and semantic trace schema.

### Host harness owns

- model selection and invocation;
- native tools, permissions, and approval UI;
- scheduling and cancellation;
- native session persistence;
- rendering messages/progress;
- translation between native events and protocol events;
- lowering semantic actions to available operations.

The portable layer may maintain protocol state but must not become an independent general-purpose model/tool loop.

## Version contract

Protocol, event schema, capability manifest, and adapter each have explicit versions. An adapter declares the protocol/schema versions it supports. Breaking invariant or schema changes require a new major version; backward-compatible fields/capabilities may advance a minor version; documentary/test clarifications may advance a patch version. Evaluations always record the exact versions used.

## Capability manifest

Every adapter publishes a versioned manifest covering:

- read/search/inspect;
- edit/write/execute/test;
- browser/research/connectors;
- asynchronous wait/resume/cancel;
- child-agent spawn/message/wait/interrupt;
- permission and approval hooks;
- durable state and restart;
- structured tool results;
- artifact/citation support;
- compaction visibility;
- progress, blocker, partial, failure, and completion UI surfaces.

Each capability declares:

- status: `enforced`, `advisory`, `emulated`, `unavailable`, or `unknown`;
- native mechanism or lowering target;
- constraints/limits relevant to behavior;
- evidence emitted on success, failure, wait, cancel, and permission denial.

## Capability negotiation

Before a protocol run, the adapter performs an explicit negotiation between protocol requirements and the host manifest. The result is persisted as a **negotiated profile** containing:

- protocol/schema/adapter/manifest versions;
- required and optional semantic capabilities;
- the selected native/emulated lowering for each capability;
- which invariants are runtime-enforced versus advisory;
- degraded guarantees and their reason;
- incompatible requirements that prevent full conformance.

No run may silently pretend an unavailable capability exists. If a required invariant cannot be enforced, the run is either rejected as incompatible or labeled with the declared degraded guarantee before evaluation.

## Semantic mapping

Adapters map native operations to semantic capabilities such as `inspect`, `research`, `plan`, `authorize`, `execute`, `wait`, `delegate`, `observe`, `verify`, `handoff`, and `recover`. The same semantic action may be implemented by different tools in Pi, Kilo, OpenCode, ChatGPT Work, or a future harness.

No adapter may rely on a product-specific tool name as a universal rule. Tool histograms remain useful for diagnosing an adapter, not for defining portability.

## Initial adapter set

The architecture should be exercised against:

- ChatGPT Work/Codex as reference evidence, not an adapter to be reimplemented;
- Kilo;
- OpenCode;
- Pi;
- at least one additional harness chosen after the capability matrix exposes a useful contrast (for example, no child agents, no structured wait, or weak persistence).

The contrast harness is a design test, not a product commitment. If the protocol cannot represent capability degradation without product-specific exceptions, the protocol boundary is too coupled.

## Adapter conformance

An adapter passes conformance only when it can emit a valid semantic trace, persist its negotiated profile, declare unavailable guarantees, preserve provenance links, honor authority boundaries, and pass the applicable property/mutation/differential tests. Prompt text alone cannot satisfy a runtime-enforced invariant.

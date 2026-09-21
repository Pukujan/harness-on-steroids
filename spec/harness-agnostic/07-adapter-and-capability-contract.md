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

## Capability manifest

Every adapter publishes a versioned manifest covering:

- read/search/inspect;
- edit/write/execute/test;
- browser/research/connectors;
- asynchronous wait/resume;
- child-agent spawn/message/wait/interrupt;
- permission and approval hooks;
- durable state and restart;
- structured tool results;
- artifact/citation support;
- compaction visibility;
- progress, blocker, and completion UI surfaces.

Each capability declares whether it is enforced, advisory, emulated, unavailable, or unknown.

## Semantic mapping

Adapters map native operations to semantic capabilities such as `inspect`, `research`, `plan`, `execute`, `wait`, `delegate`, `observe`, `verify`, `handoff`, and `recover`. The same semantic action may be implemented by different tools in Pi, Kilo, OpenCode, ChatGPT Work, or a future harness.

No adapter may rely on a product-specific tool name as a universal rule. Tool histograms remain useful for diagnosing an adapter, not for defining portability.

## Initial adapter set

The architecture should be exercised against:

- ChatGPT Work/Codex as reference evidence, not an adapter to be reimplemented;
- Kilo;
- OpenCode;
- Pi;
- at least one additional harness chosen for capability contrast, such as a harness with no child agents or no structured wait.

The fourth harness is a design test: if the protocol cannot describe capability degradation cleanly, it is too coupled to Kilo/OpenCode.

## Adapter conformance

An adapter passes conformance only when it can emit a valid semantic trace, declare unavailable guarantees, preserve provenance links, honor authority boundaries, and pass the relevant property/mutation/differential tests. Prompt text alone cannot pass a runtime-enforced invariant.

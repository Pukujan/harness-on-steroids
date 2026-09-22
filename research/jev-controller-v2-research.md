# Jev Controller v2 research record

Updated: 2026-09-21
Status: owner-approved for implementation

## Finding

The first Jev replay was a routing smoke test, not a real Jev controller. It
made one request per task with a compact state record, selected one action, and
prepended one directive to the downstream harness prompt. It did not carry the
coding agent's evolving context back into Jev, classify candidate beads, or
make a second decision after an observed execution step.

## Verified model behavior

TypeSafe documents Jev as a System One decision model. The application sends a
`state` plus typed questions and receives structured answers, probabilities, and
confidence. The available primitives are:

- `Choice`: choose one item from a defined set;
- `Score`: place the state on a defined rubric;
- `Noul`: return a probability for a true/false question.

Jev accepts text, JSON objects, and arrays of text. It does not write code,
generate explanations, call tools, or maintain a conversational session. The
conversation and execution loop therefore belong to the harness. The harness
must build the next state from the original ask, relevant conversation,
coding-agent events, repository facts, active beads, candidate tasks, and
verification evidence before asking the next typed questions.

Sources checked:

- https://docs.typesafe.ai/concepts/system-one
- https://docs.typesafe.ai/introduction
- https://docs.typesafe.ai/introduction/coding-agents
- https://openrouter.ai/typesafe/jev-1.13/
- https://openrouter.ai/labs/jev/compile

## External ecosystem evidence: Jev needs a context feeder

The public OSS evidence resolved an important ambiguity in the v2 design. The
companion note [`research/jev-ecosystem-evidence.md`](jev-ecosystem-evidence.md)
records the source review and exact comparison. In short, Jev is a typed,
decision-only endpoint: the host supplies the current state and a closed set
of legal choices; the host validates and executes the answer. Jev does not
open repository files, inspect a browser, call tools, run a subagent, or
invent the next prompt.

The clearest live-agent example is
[`browser-use/jev-ultrafast`](https://github.com/browser-use/jev-ultrafast).
Its host turns a live browser observation into an indexed element table and
recent-action context, offers only compatible operations and targets to Jev,
executes the validated selection, and observes the page again. The
[TypeSafe playground browser-agent notes](https://github.com/TypeSafeAI/typesafe-playground/blob/main/docs/jev-browser-agent.md)
and [tool-router notes](https://github.com/TypeSafeAI/typesafe-playground/blob/main/docs/tool-router.md)
show the same boundary: the host constructs the live state and permitted
candidate set, while Jev chooses within it.

This means a coding controller requires a context-feeder boundary before the
Jev call. Deterministic collectors can provide git status, file tree,
changed paths, command results, session metadata, and test results. A coding
worker or subagent may be needed to inspect relevant files, interpret an
open-ended owner request, or propose candidate beads. That worker is not
optional in every design, but some feeder fields do not require an LLM. The
important point is that Jev cannot collect either kind of context itself.

## What the first v2 replay actually supplied

The first v2 runner supplied the owner ask, `intake` phase, one synthetic
`task-main` bead, generic constraints, and initially empty conversation,
repository-fact, event, changed-path, and test-result fields. It offered an
action set derived from the existing `ControllerAction` enum. After an
adapter step, it folded back normalized event metadata and status summaries.
It did not first run an inspection worker, derive real candidate beads, or
provide file excerpts, repository facts, or test evidence before the first
Jev decision.

Therefore that replay proved request construction, typed-answer parsing,
legal-action validation, fallback, and repeated-loop mechanics. It did not
prove observation-derived coding-task classification or bead selection. The
low-confidence fallbacks and repeated `CLASSIFY_REQUEST` choices are
consistent with an under-populated decision context; they are not evidence
that Jev cannot route a properly prepared coding state.

## Revised next experiment

The next primary hypothesis is now a bounded context-feeder preflight: collect
deterministic repository facts and, where needed, have the coding worker
propose real candidate beads and acceptance criteria before the first Jev
call. Keep the Jev schema, confidence threshold, and adapters constant, then
rerun the same frozen hashes. The earlier idea of removing
`CLASSIFY_REQUEST` from the intake choice set is paused until the missing
context is populated; otherwise the two interventions would be confounded.

## Correct use in this project

The generative coding model proposes candidate beads or decomposes an open
request. Jev then makes the bounded decisions that software can consume:

- classify the request and current phase;
- choose the next bead from the candidate set;
- choose the next legal harness action;
- score readiness, risk, or verification sufficiency;
- decide whether to delegate to Sol, continue, retry, ask the owner, or
  escalate;
- decide whether a bead has enough acceptance evidence to close.

Jev should receive the full relevant decision context, not merely the current
phase. The controller should still avoid sending irrelevant history forever:
the context builder owns the 32K request budget and can preserve the complete
task record while compacting old event detail into typed facts and summaries.

## Streaming and back-and-forth

OpenRouter documents normal chat streaming separately from Jev's structured
Decisions interface. The Jev example uses a Decisions request and receives
typed `answers`; it is not a text-generation stream. The harness must still
stream adapter events and run a repeated decision loop:

```text
state/context -> Jev decision -> one bounded harness step
       ^                                  |
       +------ observed events/results ---+
```

The implementation must probe the configured OpenRouter Jev route for any
supported streaming flag rather than pretending a response is streamed. A
structured request/response at each event boundary is acceptable; the
long-running behavior comes from the repeated context-update cycle.

## What the old pilot means

The old result in `reports/matched-replay-20260921.md` measures whether one
Jev hint changes downstream harness behavior. It is retained as v1 smoke-test
evidence. It must not be presented as evidence that Jev's task decomposition,
classification, or long-horizon control is correct.

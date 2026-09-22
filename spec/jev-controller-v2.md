# Jev Controller v2 contract

Status: owner-approved for implementation on 2026-09-21.

## Roles

Jev is the typed classifier and decision selector. It never owns tools,
filesystem access, prompts, subprocesses, or side effects.

The generative coding harness proposes or executes work. The bead store holds
durable work units, dependencies, evidence, and completion state. The runtime
controller enforces legal phase transitions and delegates one bounded action
at a time.

## Decision context

Every Jev round receives a `DecisionContext` containing:

- task identity and original owner request;
- relevant conversation turns and corrections;
- current phase and allowed actions;
- open beads, dependencies, candidate next beads, and acceptance criteria;
- recent adapter events, tool names, return status, and failures;
- repository facts, changed paths, test results, and verification evidence;
- active constraints, timeout budget, retry count, and user-input status.

The context is serialized as text/JSON state for the OpenRouter Jev Decisions
API. Raw event bodies remain in ignored run artifacts; committed reports keep
hashes and derived measurements only.

## Typed question set

The first v2 schema uses several independent questions in one Jev request:

1. `task_class` — `inspect`, `research`, `reproduce`, `plan`, `implement`,
   `test`, `verify`, `recover`, `communicate`, or `escalate`.
2. `next_bead` — one of the currently open candidate bead identifiers.
3. `next_action` — one of the currently legal `ControllerAction` values.
4. `delegate_target` — `local`, `sol`, `specialist`, or `owner`.
5. `verification_level` — `none`, `targeted`, `broad`, or `acceptance`.
6. `evidence_sufficient` — Noul for whether the proposed action is supported.
7. `should_continue` — Noul for whether another bounded step is appropriate.
8. `readiness` — Score over blocked, proposed, ready, partial, and complete.
9. `risk` — Score over low, medium, high, and unknown.

The deterministic controller combines these answers. A low-confidence or
schema-invalid result follows the configured fallback and never silently
becomes an executable action.

## Runtime loop

1. Build the initial context from the owner ask and durable task state.
2. Ask the generative harness or Sol worker to propose candidate beads when
   decomposition is missing.
3. Ask Jev the typed question set.
4. Validate Jev's choices against the current phase and available beads.
5. Execute exactly one bounded adapter action.
6. Stream and reduce adapter events into facts, bead evidence, and outcomes.
7. Append the result to the context and ask Jev again.
8. Stop on verified completion, owner input, escalation, exhausted budget, or
   repeated failure.

## Harness adapters

The existing adapters remain separate execution backends:

- OpenCode launches its JSON event mode with the configured agent/model.
- Grok Build launches the authenticated CLI with JSON output and bounded turns.
- Pi launches headless JSON mode and uses its project-local provider config.

Adapters do not interpret Jev. They execute controller-approved prompts or
bounded actions, stream observable output, and return normalized events. The
OpenCode and Grok continuation behavior must be verified from real CLI session
identifiers; the runner must never invent a session identifier. Explicit
context replay is the fallback when a CLI cannot continue a session.

## Acceptance criteria

- Jev calls remain OpenRouter-only and are pinned to a Typesafe Jev model.
- The v2 runner makes more than one Jev decision when the task has more than
  one bounded execution step.
- Each decision sees the updated context from the previous step.
- Jev cannot directly call tools or mutate files.
- Illegal, unknown, low-confidence, and unavailable decisions have tested
  fallback behavior.
- OpenCode, Grok Build, and Pi adapters have independent streaming/event tests.
- A fake-adapter test proves context accumulation and legal transitions.
- A real matched replay compares baseline and Jev-loop modes on the same
  existing Work hashes using R1-R6, work-match, outcome, timeout, and variance
  measurements.

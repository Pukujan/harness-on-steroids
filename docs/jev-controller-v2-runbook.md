# Jev Controller v2 next-session runbook

This runbook is the executable continuation point after the v2 plan is
approved. The repository root is `D:\claude\harness-on-steroids`.

## Read first

1. `AGENTS.md`
2. `PLAN.md`
3. `HANDOFF.md`
4. `checkpoints/CURRENT.md`
5. `research/jev-controller-v2-research.md`
6. `spec/jev-controller-v2.md`

## Current implementation boundary

The tracked controller is v1. `src/hos/controller/core.py` has the phase and
action taxonomy, OpenRouter-only Jev client, compact `ControllerState`, and
one-shot `ControllerDecision`. `research/run_controller_replay.py` is the v1
baseline-versus-hint runner. Keep both available for comparison.

The v2 implementation should add, in small slices:

1. `DecisionContext` with original ask, relevant conversation, candidate beads,
   adapter observations, evidence, constraints, and current phase.
2. Typed question construction for task class, bead selection, next action,
   delegation, verification, readiness, risk, and continuation.
3. Legal-action validation and deterministic fallback for bad or low-confidence
   Jev decisions.
4. `JevDecisionLoop` that executes one bounded step, updates context, and asks
   Jev again.
5. Fake-controller and fake-adapter tests proving multi-round context flow.

## Adapter checks

- OpenCode: verify JSON event streaming and whether a real session identifier
  can be captured and reused. Never invent a session identifier.
- Grok Build: verify the CLI's actual structured output mode and why the v1
  parser observed zero tool events.
- Pi: preserve headless JSON mode, project-local provider configuration, and
  the configured Qwen Flash model.

If a CLI cannot continue a native session, use explicit accumulated context for
the next bounded invocation and record that limitation in the run report.

## Validation sequence

1. Unit tests for state serialization, question schemas, parser behavior,
   legal transitions, and fallback.
2. Fake multi-step loop test with at least three decisions.
3. One OpenCode smoke task with ignored raw artifacts.
4. One matched baseline/JeV-loop task on each available adapter.
5. Expand to the frozen develop slice only after the smoke results are valid.
6. Write a hash-only report and update `checkpoints/CURRENT.md`.

Jev calls must stay on OpenRouter. Do not print or commit credentials, raw
transcript bodies, or raw CLI event bodies.

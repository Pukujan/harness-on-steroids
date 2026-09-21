# Owner-accepted operating contract

Date accepted: 2026-09-21
Status: **authoritative refinement of this planning package**

This file records the owner's final decision after reviewing the harness-agnostic proposal and the existing Codex-mode experiments. Where this file conflicts with earlier files in this package, this file wins. Repository-wide precedence remains AGENTS.md and PLAN.md.

## Goal

Build a **model- and harness-agnostic control layer** that transfers supported observable behavior from the local ChatGPT Work/Codex corpus to other coding-agent harnesses.

Do not reduce the reference to tool-call order. Use every reliable observable signal the corpus/exporter can provide: interaction shape, inspection/research, waits, delegation, tool inputs/results, verification, provenance, final-output behavior, corrections, context/continuity, terminal outcome, and repeated-run variance.

## Development topology

Normal development runs **Pi, OpenCode, and Grok Build in the same slice** when technically possible.

Record the exact model/provider/version and harness/config for every run. Same-model cross-harness comparisons are useful isolation tests, but the project is model-agnostic and does not require model parity for every iteration.

Kilo Codex v0 remains a positive-control baseline and evidence that behavior prompting can produce large immediate improvements.

## Mechanism

Start with the cheapest control mechanisms:
1. behavior prompt/instructions;
2. context selection/composition;
3. capability/tool presentation and adapter lowering;
4. checkpoint/continuation context;
5. narrow runtime state/guard only after repeated measured failures justify it.

A full state machine is **not** a prerequisite.

Semantic phases/states may be inferred/annotated for comparison. Runtime enforcement is introduced only when prompt/context control repeatedly fails and a small controlled experiment shows the guard improves behavior or outcomes.

## Fast-loop invariant

Do not turn this into a long infrastructure build.

Each normal slice:
- one main behavioral deviation/hypothesis;
- small fixed set of existing Work-derived tasks;
- baseline/candidate run across all three active harnesses;
- automatic capture and comparison;
- visible measured result;
- keep/revert/refine.

No substantial architecture-only slice counts as progress.

## Evaluation

Tool matching and R1-R6 remain diagnostics. Primary evaluation expands to the complete observable trajectory and outcome.

Repeated generations of the same/equivalent input are valuable: deviation and variance are themselves signals of control-layer quality.

Morphs, long tasks, corrections, and continuity failures are used to test robustness. Holdout remains sealed during tuning.

## Continuity and repository policy

GitHub/repository state is authoritative project memory:
- owner contract in AGENTS.md / PLAN.md / owner spec v2;
- exact current state in checkpoints/CURRENT.md;
- executable work in GitHub Issues;
- evidence/history in reports/specs/JOURNAL/git history.

The old implementation may be replaced freely if it obstructs the goal, but evidence, tests, lessons, and audit history are preserved. Do not wipe v0 merely for cleanliness.

## Immediate next slice

GitHub issue #2: baseline 3-5 existing development tasks across Pi, OpenCode, and Grok Build **before changing the control layer**. Capture available full-trajectory signals, identify the largest recurring deviations, then select exactly one smallest next intervention.

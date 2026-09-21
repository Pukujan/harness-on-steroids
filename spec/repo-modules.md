# Repo modules (boundaries)

This is a research/software project, not a dump. New work goes in the smallest layer that owns the active experiment. Do not pre-build a framework because a future architecture might need it.

## Layers (MVC-shaped)

| Layer | Owns | Must not own |
| --- | --- | --- |
| **Contract** AGENTS.md, PLAN.md, spec/owner.v2.*, spec/ | Owner rules, experimental contracts, versioned interpretations | Private transcript bodies |
| **Measure** research/ + reports/ | Reference extraction, replay runners, normalized traces, comparisons, JOURNAL | Product prompt text as truth |
| **Adapt** harness configs/adapters | Pi/OpenCode/Grok Build control surfaces; Kilo v0 baseline | Corpus interpretation |
| **Lib** src/ | Reusable scorers, owner invariants, goal/checkpoint helpers | Speculative framework without a measured caller |
| **Gate** tests/ + .github/workflows/ | Properties, holdout, mutation, metamorphic, differential, replay regression | Implementing the experiment itself |
| **State** checkpoints/CURRENT.md, GitHub Issues, HANDOFF.md, ISSUES.md | Current work and durable continuity | Long chat transcripts as memory |

Routing rule: prefer an existing module. A new abstraction should normally have a current measured use in the active issue.

## src/ policy

Current v0 modules remain valid historical/regression utilities:
- src/owner_invariants.py
- src/score_session.py
- src/goal_loop.py / src/goal_cli.py
- existing src/hos facade

Do not expand src/hos into a generalized protocol runtime until an experiment requires reusable code.

If repeated experiments need the same normalizer/scorer/runner, extract that minimal shared unit then.

## Versionable artifacts

| Kind | Where |
| --- | --- |
| Reference interpretations | reports/versions/vN/ |
| Historical imitate spec | spec/codex-imitate-mode.md, spec/versions/ |
| Owner spec | spec/owner.v2.json |
| Active continuity | checkpoints/CURRENT.md + GitHub issue |
| v0 implementation history | Git history; relocate only after replacement + audit mapping |

## Fast-loop rule

No substantial architecture-only slice. New code should support a measured reference signal, an automated evaluator capability, or an observable behavior/outcome experiment immediately.

## Lint and types

pyproject.toml ruff/mypy settings apply to src/. CI keeps the owner/replay regression gates.

## Out of bounds

- SWE-bench or another public benchmark as the project
- summarizer/compressor as the project
- exact tool/prose cloning as the success definition
- model-specific optimization as the project goal
- New analysis scripts in the repo root
- giant protocol/state-machine implementation before evidence requires it

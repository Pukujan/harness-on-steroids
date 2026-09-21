# Prompt / context / harness stack

Layers, top wins on conflict. The current owner contract is spec/owner.v2.json.

| Layer | File | Job |
| --- | --- | --- |
| Owner | AGENTS.md, PLAN.md | Model/harness-agnostic goal, scope, fast-loop rules |
| Current state | checkpoints/CURRENT.md, active GitHub issue | Exact experiment, hypothesis/baseline, next action, stop condition |
| Loop | spec/iteration-loop.md, CONTINUE.md when explicitly activated | Small empirical iteration; autonomous continuation only after owner go |
| Machine spec | spec/owner.v2.json | Testable governance claims |
| Reference | reports/, research/, spec/codex-imitate-mode.md | Work/Codex evidence plus v0 historical interpretation |
| Control | harness prompt/context/config/adapter surfaces | Smallest intervention; prompt/context first |
| Proof | tests/, .github/workflows/owner-gate.yml | Governance and regression gates |
| Modules | spec/repo-modules.md | Contract / measure / adapt / lib / gate / state boundaries |

## Precedence

If a v0 mode prompt or older proposal disagrees with AGENTS.md / PLAN.md, the owner docs win.

The current Kilo/OpenCode Codex prompts are v0 positive-control/history. They remain useful baselines, not owner-level source of truth.

## Active development

Pi + OpenCode + Grok Build run in the same development slice where technically possible. Record exact harness/model/config. Same-model cross-harness runs are useful isolation checks, not a requirement.

## Control order

Prefer:
1. prompt/behavior instruction;
2. context composition;
3. tool/capability presentation/lowering;
4. checkpoint/continuation context;
5. narrow runtime state/guard only after repeated evidence earns it.

A full state machine is not a required layer.

## Chat vs no-stop

Ordinary chat answers first and seeks go-ahead. CONTINUE.md is dormant until a concrete /goal and explicit owner go. An open issue does not activate it.

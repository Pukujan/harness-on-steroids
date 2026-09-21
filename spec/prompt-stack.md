# Prompt / context / harness stack

Layers, top wins on conflict. Codex gold is the behavior layer, not a public exam.

| Layer | File | Job |
| --- | --- | --- |
| Owner | `AGENTS.md`, `PLAN.md` | Gold = local Codex transcripts; imitate in Kilo+OpenCode; no SWE-bench substitute |
| Loop | `CONTINUE.md`, `ISSUES.md`, `research/JOURNAL.md` | 20h/48h, document, occasional push |
| Machine spec | `spec/owner.v1.json`, `spec/codex-imitate-mode.md`, `spec/goal-loop.v1.json`, `spec/work-research-gates.md` | Testable claims |
| Product context | `kilo.json` `instructions` | Load AGENTS.md then PLAN.md |
| Behavior | `.kilo/agent/codex.md`, `.opencode/agent/codex.md` | Look first, burst, wait, sandwich, look-after-fail |
| /goal | Kilo product `/goal` (do not add `.kilo/command/goal.md`); OpenCode `.opencode/command/goal.md` | OpenCode routes to `agent: codex`. Kilo reserved `/goal` 500s if shadowed |
| Engine | `src/goal_loop.py` | Standing goal, gates before done, persist |
| Proof | `tests/`, `.github/workflows/owner-gate.yml` | Properties, holdout, mutation, metamorphic, differential, fuzz |
| Modules | `spec/repo-modules.md` | Contract / measure / adapt / lib / gate |

If a mode prompt disagrees with `AGENTS.md`, **AGENTS.md wins**. Recode behavior from new gold reports into `reports/versions/` then the mode files, not the other way around.

Chat vs no-stop: ordinary chat answers first and seeks go-ahead. `CONTINUE.md` no-stop applies only after `/goal` + owner go. Kilo default personality (accomplish, do not chat) does not override that.

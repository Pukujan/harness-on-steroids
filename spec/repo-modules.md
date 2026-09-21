# Repo modules (boundaries)

This is a software project, not a dump. New work goes in the module that owns it. Version interpretations in `reports/versions/` and `spec/versions/`, not by overwriting history.

## Layers (MVC-shaped)

| Layer | Owns | Must not own |
| --- | --- | --- |
| **Contract** `spec/` | Owner gold, imitate states, research gates, this map | Chat bodies, live replay prompts |
| **Measure** `research/` + `reports/` | JSONL counts, replay runners, JOURNAL | Product mode text as source of truth |
| **Adapt** `.kilo/agent/` `.opencode/agent/` | Codex mode prompts (paired) | Corpus parsing |
| **Lib** `src/` | Scorer, goal engine, owner invariants | One-off analysis scripts |
| **Gate** `tests/` + `.github/workflows/` | Properties, holdout, CI | Implementing replay |
| **State** `AGENTS.md` `PLAN.md` `ISSUES.md` `HANDOFF.md` | What to do next | Tool histograms as the exam |

Routing: a new file answers “which layer?” If it is a count from JSONL → `research/` script + `reports/`. If it is a required behavior → `spec/` then both modes. If it is a check → `tests/` and CI. If it is session memory → checkpoint (issue 16), not a longer chat.

## `src/` packages (current + target)

Current library modules (keep import paths until issue 18 moves them):

| Module | Job |
| --- | --- |
| `src/owner_invariants.py` | Owner-spec checkers |
| `src/score_session.py` | R1–R6 process score |
| `src/goal_loop.py` `src/goal_cli.py` | Standing `/goal` engine |

Target packages (do not dump new CLIs at repo root):

- `src/hos/score/` — process score
- `src/hos/goal/` — goal engine
- `src/hos/replay/` — replay_lib (today `research/replay_lib.py`)
- `src/hos/gold/` — hashed JSONL counters (today `research/codex_*.py`)

Facades: `src/hos/` re-exports. Tests may keep old imports until a dedicated move PR.

## Versionable artifacts

| Kind | Where |
| --- | --- |
| Gold interpretation | `reports/versions/vN/` |
| Imitate spec | `spec/versions/` |
| Owner spec | `spec/owner.v1.json` |
| Continuity protocol | PCM later; do not clobber `HANDOFF.md` |

## Lint and types

`pyproject.toml` `[tool.ruff]` and `[tool.mypy]` apply to `src/`. CI must keep pytest owner-gate. Ruff/mypy on `src/` join CI when issue 18 is green. `research/` scripts stay ruff-clean-enough; they are not the public API.

## Out of bounds

- SWE-bench as the project
- Summarizer as the memory
- Unpaired Kilo vs OpenCode mode edits
- New analysis scripts in the repo root

# How to keep this from being half-baked (external + local)

Not a substitute for Codex gold. Methods for **20h+ iteration**: measure, version, fuzz, judge, do not ship vibe.

## External

| Source | What to copy | What not to copy |
| --- | --- | --- |
| METTLE / metamorphic testing (Xie et al., arXiv:1807.10453) | Relations that must hold under transforms (whitespace, extra passing gate, paraphrase of goal text) because there is **no labeled “correct transcript”** | Treating clustering papers as the product |
| Codex CLI `/goal` + Hermes Persistent Goals | Standing objective, **judge after every turn**, gates before done, budget then pause, persist | Pretending a markdown `/goal` is that engine |
| SWE-bench Verified (OpenAI) | Hidden tests are for **public** tasks; eval quality matters | Using it as this project’s gold |
| FOSSIL / PAM decision lineage (this machine, internal) | Record *why* a spec version won (counts + hashes), not only the file | Mixing hades product into this repo |

There is no oracle for “did the agent behave like Codex” except **process relations** on traces (look-first, wait-on-cell, sandwich edit, look-after-fail) plus **mechanical gates**. That is why metamorphic + differential + fuzz belong here.

## Local versions (recode, compare, keep)

Keep numbered snapshots under `reports/versions/` when the gold *interpretation* changes (v1 histograms, v2 JS-cell+wait, v3 error-then-look). Do not overwrite away the argument.

## 20-hour floor

Analysis/iteration does not stop before **2026-09-21T02:35:00Z** (20h from 2026-09-20T06:35Z) and still respects the 48h `CONTINUE.md` deadline. Wakeups are the clock. `/goal` max_turns is per-process, not hours.

## Harness vs prompt

Prompt/mode text (`.kilo/agent/codex.md`) is one layer. Harness layer is: goal engine, pytest gates, fuzz that a red gate cannot be “done”, owner-invariant holdout. Both required. Coding without a new measurement or a new relation is not progress.

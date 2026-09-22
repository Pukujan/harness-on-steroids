# Jev long-horizon matched A/B — combined result — 2026-09-22

Hash-only result for Issue 22. Arm A is the shared deterministic repository
context feeder plus the harness. Arm B receives the identical feeder pack,
then one Jev Decisions API call, typed validation, and a bounded action hint.
The six holdout hashes were not selected or scored.

## Frozen matrix

- 16 Work-derived development hashes; at least three user turns per hash.
- 60 matched user turns per arm and harness; 120 rows per harness.
- OpenCode and Pi: `yolo-auto/qwen3.8-flash` through Yolo Auto.
- Grok Build: `grok-4.7`.
- Jev: `typesafe/jev-1.13` through the OpenRouter Decisions API.
- Harness invocation timeout: 60 seconds; Jev timeout: 30 seconds; minimum
  accepted Jev confidence: 0.55.
- Gold/reference: local ChatGPT Work/Codex development evidence. The existing
  Work-derived taxonomy and R1-R6 are diagnostic, not exact tool-order rules.
- Raw prompts, transcript bodies, event bodies, credentials, and private
  files remain ignored/local. The per-harness reports contain hashes only.

## Aggregate result

| Harness | Arm | Turns | Executed | Timeouts | Work-match | Outcomes | Mean tools/task | Jev decisions | Low-confidence fallbacks |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| OpenCode | A baseline | 60 | 60 | 57 | 8/16 | no=5, partial=11 | 8.3 | 0 | 0 |
| OpenCode | B Jev | 60 | 13 | 12 | 4/16 | no=9, partial=7 | 3.6 | 60 | 47 |
| Grok Build | A baseline | 60 | 60 | 58 | 0/16 | no=16 | 0.0 | 0 | 0 |
| Grok Build | B Jev | 60 | 13 | 12 | 0/16 | no=16 | 0.0 | 60 | 47 |
| Pi | A baseline | 60 | 60 | 49 | 0/16 | no=12, partial=4 | 36.2 | 0 | 0 |
| Pi | B Jev | 60 | 12 | 10 | 0/16 | no=15, partial=1 | 9.1 | 60 | 48 |

The per-harness hash-level tables are in:

- `reports/jev-long-ab-final-20260922-opencode.md`
- `reports/jev-long-ab-final-20260922-grok.md`
- `reports/jev-long-ab-final-20260922-pi.md`

## Decision observations

Every Jev arm made 60 typed decisions. Mean decision confidence was 0.419
(OpenCode), 0.409 (Grok Build), and 0.390 (Pi), below the 0.55 acceptance
gate. Consequently 47, 47, and 48 decisions respectively fell back for
`low_confidence`; the accepted decisions executed only 13, 13, and 12
bounded harness turns. The most common proposed action was `INSPECT_REPO`:
36 OpenCode, 52 Grok Build, and 33 Pi decisions. The remaining decisions were
mostly `RECOVER_AFTER_FAILURE` or `ASK_USER`, with one `SEARCH_LOCAL` in each
adapter and one OpenCode `READ_DOCS` decision.

## Interpretation

This slice does not support promoting the current Jev controller policy. It
did not improve Work-match or outcome, and on OpenCode the match rate fell
from 8/16 to 4/16. On Grok Build and Pi neither arm reached a Work-match;
the Jev arm additionally reduced execution and worsened the observed Pi
outcome distribution.

The strongest measured failure is under-execution caused by the confidence
gate, not proof that Jev cannot reason over repository context. The feeder
did provide live bounded facts, changed paths, candidate beads, and redacted
excerpts to both arms; Jev itself still had no file, shell, or subagent
authority. Low-confidence decisions were recorded and safely prevented a
harness call, which is appropriate safety behavior but not a useful coding
control policy in this benchmark.

## One next hypothesis

Keep the feeder, candidate choices, models, fixtures, and timeouts fixed, but
make low-confidence fallback execute the same shared feeder prompt as Arm A
while recording the Jev answer as advisory. A fresh matched 60-turn slice can
then test whether Jev's accepted action hints add value without allowing the
confidence gate to turn the Jev arm into a mostly unexecuted arm.

## Provenance

- OpenCode run: `jev-long-ab-final-20260922-opencode`
- Grok Build run: `jev-long-ab-final-20260922-grok`
- Pi run: `jev-long-ab-final-20260922-pi`
- Each run audited at 60 turns, 16 development hashes, 32 task summaries,
  and zero `fail_1` rows. No holdout hash was selected.

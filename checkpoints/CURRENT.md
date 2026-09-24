# Current

Updated: 2026-09-24
Plan status: **owner accepted / frozen operating direction**
Owner spec: spec/owner.v2.json

## Repository durability checkpoint — Issue #3

The storage/worktree remediation is tracked separately from GitHub
issue #7, which is now complete. `main` previously had no branch protection;
the prior CI ran a
manually maintained subset of tests, and its latest run failed because the
handoff omitted the Issue #2 owner-contract reference. The replacement CI
defines separate lint, type-check, complete Linux and Windows test-suite, and
checkpoint-record checks. Pull requests to `main` must update this file;
branch protection must require all five checks and a current base before
merge. Verified, publishable checkpoints are to be pushed as issue branches
and merged before advancing to the next independent slice. Raw/private
artifacts remain local.

The storage/runtime remediation is complete and merged as PR #4 and follow-up
PR #5 on 2026-09-23. All nine registered HOS worktrees on C: were retired
after preserving and hash-verifying unique dirty work on D:. All 74 generated
per-run OpenCode plugin dependency trees were pruned while retaining controller
run records and results; D: free space increased by 46.59 GiB during this
cleanup. PR #5 routed both legacy replay scripts through the same pinned
repo-owned OpenCode executable and passed `lint`, `typecheck`, `tests`,
`windows-tests`, and `checkpoint-record`. Main's required PR checks and
no-bypass protection are active. The existing user-level NVM installation was
left untouched; HOS no longer selects it. No storage/runtime work remains.

The canonical D: checkout is reconciled to PR #8's merge commit
`cd8abd0a92514ed2d6ec8275e5874b9ac4c23e79`. The merged issue #7 task worktree
was clean and has been retired. Pre-existing owner changes were archived
locally before reconciliation and remain outside the repository.

## Completed checkpoint automation — GitHub issue #7

GitHub issue #7, **Automate issue-backed checkpoint publishing and worktree
closeout**, is complete. PR #8 merged on 2026-09-24 as
`cd8abd0a92514ed2d6ec8275e5874b9ac4c23e79`; all five required checks passed.
Repository auto-merge is enabled, `main` requires an up-to-date branch, and
administrators are subject to branch protection. The publisher/reconciler
confirmed the merge, fast-forwarded the canonical D: checkout, removed the
clean merged task worktree, and marked PR #8's durable closeout state
`complete`.

The implementation is in `src/hos/checkpoint_publisher.py`,
`tools/checkpoint.py`, and `docs/checkpoint-publisher.md`. The publisher commits
only explicitly selected safe paths on an issue branch, creates or updates
the linked PR, queues auto-merge, and reports pending CI asynchronously. The
local reconciler updates the canonical checkout only after GitHub confirms a
protected merge and retires only a clean, merged D: task worktree. Owner-local
changes were preserved separately and were not included in PR #8.

## Next experiment — GitHub issue #2

Baseline 3–5 representative existing development tasks through Pi, OpenCode,
and Grok Build with no control intervention. Capture comparable observable
trajectories or explicit non-comparable reasons, identify the largest recurring
deviations from Work references, and select exactly one smallest next control
hypothesis. Keep the behavioral holdout sealed.

## Last verified Issue #7 implementation result

`src/hos/checkpoint_publisher.py` and `tools/checkpoint.py` implement the local
publish/reconcile path. Publication validates the issue and required branch
protection, freezes the issue body by digest, stages only explicit paths,
rejects private/generated artifacts and common credential formats, and opens
or updates the linked PR. An eligible PR is queued for GitHub auto-merge and
returns `pending_ci_merge` while checks run. Reconciliation verifies the
confirmed merge and validates the exact clean worktree before fast-forwarding
or cleanup; dirty or ambiguous work is preserved.

The focused publisher/CI-contract suites passed (52 checks). The complete
Windows suite passed (225 passed, 4 skipped because ignored local replay data
was absent); repository-wide Ruff and mypy passed. A GitHub-backed dry-run
returned `would_publish`. PR #8 then passed `lint`, `typecheck`, `tests`,
`windows-tests`, and `checkpoint-record` and merged through auto-merge. Local
reconciliation completed after the owner changes were safely archived.

## Last verified analytical-machine result — 2026-09-22

The completed local research track formerly labeled “Issue 23” is implemented
in `src/hos/analysis_machine/` with Codex and ChatGPT JSONL adapters, body-free
canonical events, separate lane summaries, deterministic export, contract
validation, and focused tests. The durable plan and bead ledger are
`docs/analytical-machine-v0-plan.md`.

The first bounded pilot used one Codex session and one ChatGPT provenance
conversation: 5,525 events across three episodes, zero parse errors, zero
validation issues, and 100% known-event coverage. A repeat export produced
byte-identical hashes for all three artifacts. This proves repeatability and
contract behavior, not agent quality or lane comparability.

The final corrected full structural pass (`analysis-machine/0.2.0`,
`analysis-codebook/0.1.1`) then consumed 2,173 local JSONL sources and
produced 556,241 events across 1,499 episodes: 419,893 Codex events in 1,387
episodes and 136,348 ChatGPT events in 112 episodes. Exact duplicate tracking
used a 600,000-ID cap and found zero duplicate IDs and zero validation issues.
28,565 events remained unknown and zero parse errors were observed. The summary-only output
is local and ignored; its committed aggregate interpretation is
`reports/analysis-machine-full-corpus-20260922.md`.

The owner approved the structural packet and operating rules on 2026-09-22;
this did not promote an ontology category. The former local “Issue 22” Jev
advisory follow-up is paused: the later attempts have no valid aggregate and
are not behavioral evidence. These two labels are historical local research
tracks, not GitHub issues. GitHub #2 remains open for the multi-harness
baseline and is queued behind the issue #7 merge/reconciliation gate.

The current provider boundary is explicit: Sol is CKFF-only through the local
Sol worker, while Luna is native Codex/ChatGPT subagent-only and never CKFF.
Three read-only native Luna reviews were used as advisory engineering review;
they did not supply gold labels or change files.

AM-06's frozen ontology pilot is now complete as an advisory measurement:
eight pilot episodes (four per lane, 2,671 body-free events) received two
independent native Luna annotations, followed by adjudication. Four sealed
holdout episodes (two per lane, 2,909 events) then received two fresh
independent reviews. The codebook is now `analysis-codebook/0.1.1`; the
adapter is `analysis-machine/0.2.0`. Research-family aliases, action-versus-
evidence distinctions, and `unknown`/`not_observed`/`not_applicable` rules are
explicit. No quality, UX, outcome, or planning category was promoted.

The larger AM-06b pilot is also complete as an advisory review: 24 pilot
episodes (12 per lane, 8,930 body-free events) and eight sealed holdout
episodes (3,231 events) were selected deterministically. Four independent
native Luna reviews (two per lane) exposed useful schema ambiguities but also
made material counting/field-recognition errors, confirming that model labels
cannot become gold without owner/human adjudication. The canonical comparison
and rules are recorded in
`research/analysis-ontology-pilot-v3-review-20260922.md`. The deterministic
owner-review packet is generated by
`research/build_analysis_review_packet.py` and was exercised locally as
`data/derived/analysis-machine/ontology-review-packet-v3/`.
On resume, the packet was revalidated: 24 pilot episodes remain balanced at
12 Codex / 12 ChatGPT, with 2,559 and 6,371 events respectively (8,930 total);
the packet contains no body-bearing keys or holdout rows. Focused analysis and
packet tests pass (13 tests), and Ruff is clean.

## Completed local research-track 22 baseline

Issue 22's clean matched A/B is complete. Its Jev policy was not promoted;
the result remains preserved below as historical controller evidence.

## Last verified v2 result — 2026-09-22

Issue 22's clean matched A/B is complete. Each of OpenCode, Grok Build, and
Pi received 60 Work-derived development turns in each arm across the same 16
development hashes, with the same deterministic repository context feeder,
isolated workspace, model, and timeout. The six holdout hashes remained sealed.

- OpenCode: baseline 8/16 Work-match and Jev 4/16; Jev executed 13/60 turns
  after 47 low-confidence fallbacks.
- Grok Build: baseline and Jev 0/16 Work-match; Jev executed 13/60 turns
  after 47 low-confidence fallbacks.
- Pi: baseline and Jev 0/16 Work-match; Jev executed 12/60 turns after 48
  low-confidence fallbacks, with fewer partial outcomes than baseline.
- No run had the prior Windows argv launch contamination: all three reports
  have 60 turns, 16 hashes, 120 rows, and zero `fail_1` rows.

The current Jev policy is not promoted. The clearest failure is that the
0.55 confidence gate converted the Jev arms into mostly unexecuted arms. The
combined hash-only report is `reports/jev-long-ab-20260922.md`; the detailed
per-harness reports are adjacent to it.

## External Jev OSS architecture deep dive — 2026-09-22

The source-backed report is `research/jev-oss-architecture-deep-dive-20260922.md`.
It confirms across Jev Ultrafast, Stanley, JevWire, pi-jev, pi-typesafe,
pi-jev-tools, TypeSafe Router, and the TypeSafe playground that Jev is
decision-only: a host observer or subagent must read live state and construct
the bounded candidate set. The current feeder is narrower than those examples:
it supplies bounded repository facts and excerpts, but does not automatically
include `CURRENT.md`, `HANDOFF.md`, `ISSUES.md`, the active issue body, a full
diff, or a context-producing scout. Its four candidate beads are synthetic
`inspect-context`, `plan-change`, `execute-change`, and `verify-result`.

The report recommends porting patterns, not adding a generic state-machine
framework: deterministic workflow eligibility, bounded evidence retrieval,
closed-set validation, freshness checks, independent verification, and
advisory/shadow measurement. This research does not change the exact next
action below.

## Jev classification/capture verdict — 2026-09-22

The focused source-backed result is
`research/jev-classification-capture-20260922.md`. Jev is suitable only for
bounded classification, scoring, routing, or an advisory shadow label over
host-supplied state. It is not the capture layer: the host must read live
files/events, preserve identity/order/provenance, construct the closed
candidate or label set, validate the answer, execute or abstain, and
independently verify. The analytical machine therefore remains deterministic
for capture and structural metrics; any Jev annotation lane must be separate
and compared with human adjudication.

## Jev shadow classification probe — 2026-09-22

The first live, body-free Jev annotation probe is recorded in
`reports/jev-shadow-annotation-20260922.md`. It sent eight deterministic pilot
events through eight independent Noul predicates (64 valid probabilities):
62/64 matched direct canonical-field labels at threshold 0.50; at a 0.75
acceptance band, 59/64 were accepted with zero errors and five abstentions.
Three repeats of the same sample produced the same 62/64 result and identical
thresholded predictions; probability ranges varied slightly (mean 0.0112,
maximum 0.08). This is a tiny structural wire/behavior probe, not
semantic-quality evidence. The v3 holdout remained sealed and no raw response
was written. The next Jev annotation step still requires owner/human
adjudication and a larger repeated semantic-label study. Before that semantic
step, the selector was corrected to honor a larger requested sample budget.
Three fresh 32-event structural repeats returned 256 valid probabilities and
254/256 direct-label matches each, with identical thresholded predictions;
mean probability range was 0.0100 and maximum 0.11. At a 0.75 acceptance band
the first run accepted 243 and abstained on 13; each repeat accepted 240 and
abstained on 16. Zero accepted labels were wrong in any run. This is still not
semantic-quality evidence and does not open the holdout.

## Baselines to preserve

- ChatGPT Work/Codex local transcript evidence = behavioral reference.
- Kilo Codex v0 = positive-control prompt baseline.
- Existing Kilo/OpenCode R1-R6, 22-thread replay, morph, and outcome notes = v0 historical/prototype evidence.

## Previous verified v2 result — 2026-09-21

Implemented and tested the smallest reusable v2 loop:

- `DecisionContext` carries the owner ask, relevant conversation, beads,
  adapter observations, evidence, repository facts, changes, test results,
  constraints, phase, retries, and user-input status with deterministic
  32K-budget compaction.
- Jev receives nine typed Choice/Score/Noul questions through the OpenRouter
  Decisions API. The live schema was probed and corrected to the provider's
  `criteria` shape; native Noul and Score answers are parsed into booleans and
  legend labels.
- `JevDecisionLoop` validates phase-legal actions, rejects low-confidence,
  unknown, unavailable, or unavailable-bead decisions, executes one bounded
  adapter step, folds normalized observations back into context, and asks Jev
  again. Fake tests prove three-round context accumulation and no adapter call
  on fallback.
- OpenCode, Grok Build, and Pi each have normalized event/session extraction
  tests. Native session IDs are recorded only when emitted; the runner uses
  explicit context replay and does not invent continuation IDs.
- Fresh matched run: `reports/matched-replay-jev-v2-20260921.md`, run id
  `jev-v2-matched-20260921`, three development hashes across all three
  available adapters. It produced repeated decisions on one hash per adapter
  (two decisions each), while 6/9 Jev arms stopped on low confidence. Baseline
  arms timed out 7/9 times; none of the 18 arms reached a Work match. A single
  repetition does not establish variance.

All focused tests and ruff checks pass. Raw prompts, stderr, and adapter event
bodies remain in ignored `.controller-runs/` artifacts only.

## External Jev evidence update — 2026-09-21

Public Jev integrations confirm that Jev is decision-only. The host must
construct the live state and closed candidate set, then validate and execute
the selected option. See `research/jev-ecosystem-evidence.md` and
`research/jev-controller-v2-research.md` for the source-backed comparison.

The first v2 replay did not yet have that feeder: it supplied the owner ask,
one synthetic `task-main` bead, generic constraints, the intake action set,
and mostly empty conversation/repository/event/test context. It therefore
tested loop mechanics and fallback, not observation-derived coding decisions.

## Next action

Merge the documentation-only handoff correction tracked by issue #9 through
the five required checks. Then begin GitHub issue **#2**: freeze 3–5 representative
development fixtures and their acceptance/environment notes, keeping the Work
holdout sealed. Before trusting the baseline, follow issue #2's replay hygiene
precondition for the contaminated pre-v66 OpenCode traces. Run the unchanged
current configuration through Pi, OpenCode, and Grok Build in the same slice
where possible; capture comparable observable trajectories and outcomes, then
select exactly one smallest next control hypothesis. Make no control
intervention during the baseline.

## Harness timeout reliability policy — 2026-09-22

The previous long-horizon runner used a 60-second hard wall-clock kill. That
was rejected as unreliable for an actively streaming TUI/CLI agent. The adapter
now uses a 120-second default inactivity timeout that resets when stdout or
stderr advances, plus a 7,200-second absolute safety cap. OpenCode provider
request/header/chunk settings and Pi HTTP/provider settings use 120,000 ms for
idle/header/chunk silence, while total request ceilings remain 7,200,000 ms.
Timeout reason is recorded as `inactivity` or `max_runtime`; active streaming
within the idle boundary is not timed out by the watchdog. See
`docs/harness-timeout-policy.md`.

## Historical Jev next action

**Launch blocker found and fixed first (2026-09-22).** The first
context-fed long A/B smoke (`run_id jev-long-smoke-seed-20260922`,
`reports/jev-long-ab-smoke-seed-20260922.md`) showed every arm at `0 tools /
outcome no` with `fail_1` and **empty events**. Root cause: the Pi and OpenCode
adapters passed the whole context-pack prompt as a command-line argument and
Windows aborted the process with `The command line is too long`, so the harness
never launched — those cells measure a launch failure, not model behavior (same
contamination class as the pre-v66 traces). The `git archive` seed
materialization itself worked. Fix (control-layer only, all 152 tests + ruff
pass): `src/hos/controller/adapters.py` now delivers the prompt over stdin for
Pi/OpenCode (`prompt_via_stdin`) and keeps Grok on `--prompt-file`; the prompt no
longer appears in argv, pinned by two new regression tests. Verified end-to-end:
a real Pi call with a 40k-char prompt returns `ok` with events and `OK-PIPE`, no
`too long`.

The launch blocker is cleared and the clean matched A/B is now recorded. The
earlier `CLASSIFY_REQUEST` choice-set hypothesis stays paused. The planned
next action was to keep the feeder, choices, models, fixtures, and timeouts
fixed, change only low-confidence handling so the Jev arm executes the same
feeder prompt as baseline while recording the Jev answer as advisory, and run
one fresh matched 60-turn slice under a new `run_id`. That slice is now
`jev-long-ab-advisory-20260922-v5`; its aggregate is pending.

The prior rerun `jev-long-ab-advisory-20260922-v2` was intentionally stopped
before interpretation after the owner shortened the default inactivity policy
from 20 minutes to 2 minutes. It had produced liveness evidence only, no
aggregate report, and its partial turn folders remain ignored diagnostics.
The stopped run is not combined with the current v5 slice.

Fresh run `jev-long-ab-advisory-20260922-v3` was launched at 17:37 with the
same 60-turn matched configuration, but it was stopped before interpretation
after the Windows process-tree cleanup path was tightened. Fresh run
`jev-long-ab-advisory-20260922-v4` was also stopped before interpretation after
its first end-to-end handoff still included excess cleanup overhead. The
default is now 120 seconds so observed handoffs stay within the owner's 2–3
minute maximum; both partial runs remain excluded.

Fresh run `jev-long-ab-advisory-20260922-v5` was launched at 18:20 with the
same 60-turn matched configuration. It was the only run eligible for later
interpretation, but the owner paused this stale session at approximately 20:11
before its aggregate report was written. Its first silent baseline child
transitioned to baseline turn 2 at 18:25 under the 120-second policy, an
approximately 2:38 end-to-end handoff.
During baseline turn 4, the child became silent after 18:29:20 and was gone by
18:31:28 while the experiment parent remained alive. This verifies the final
inactivity kill-and-continue path. A second silent baseline handoff, from turn
1 at 18:40:38 to turn 2 at 18:43:18, took approximately 2:40 end-to-end and
also stayed within the owner's 2–3 minute boundary. The aggregate is still
pending and v5 must not be interpreted as a completed A/B.

The last observed v5 child was `633c140546c0` Jev turn 4, started at 20:09:16;
the owner then stopped the complete process tree at approximately 20:11 to
avoid carrying this long session forward. No v5 report exists. The raw ignored
run directory remains local for diagnostics, but it is not evidence and must
not be mixed into a future aggregate. This local research track is paused;
these historical run notes do not authorize a new run. GitHub issue #7 is the
completed work item, with issue #2 next after the issue #9 handoff-correction
PR merges.

## Long-horizon A/B contract

The executable contract is `research/jev-long-horizon-ab.md`. The completed
slice used the shared deterministic context feeder and a 60-turn matched
runner. A and B used the same Work-derived development turn fixtures,
fresh equivalent workspaces, feeder pack, timeout, and harness/model. B adds
only the Jev decision, typed validation, and bounded action hint. OpenCode and
Pi currently use `yolo-auto/qwen3.8-flash`; Grok Build uses `grok-4.7`; Jev is
the separate `typesafe/jev-1.13` OpenRouter call. The ChatGPT Work corpus
remains the behavioral reference and holdout remains sealed.

**Historical baseline note:** a blocking defect was found and fixed first
(2026-09-22, `reports/versions/v66/README.md`).
The replay runners passed the raw first user turn to the harness. In these Work
transcripts that turn is the prepended `<recommended_plugins>` / `<environment_context>`
block, and for **11 of the 22** develop+holdout hashes it contains no ask at all, so a
baseline on those hashes measures behaviour on a **task-free prompt**. Any hint/control
arm that adds a directive would appear to help only because it supplied the sole
instruction — this is exactly what the pre-fix Pi/OpenCode/Grok controller rows show
(baseline 0 tool calls vs a hint arm up to 306). Do **not** reuse pre-v66 traces as a
baseline, and do not compare new cells to them.

Fix is in: `research/replay_lib.py` (`strip_context_blocks` / `first_ask` / `ask_turns`),
both runners now send the real ask and record `ask_present` / `ask_shifted`, plus gate
`tests/test_replay_prompt_hygiene.py`. The `reports/replay-scores.md` OpenCode column is
flagged contaminated for those 11 hashes (rows kept because `tests/test_replay_scores.py`
pins them).

The v1 pilot is already recorded in `reports/matched-replay-20260921.md`.
Before a new matched run, move old per-run artifacts aside or use a fresh
`run_id`; do not append fresh traces to an old evidence directory.

Then proceed as planned: select 3-5 representative tasks from the existing **development** replay set, not holdout. Freeze their acceptance/environment notes, then run the current configuration through:

1. Pi
2. OpenCode
3. Grok Build

in the same slice where technically possible.

Record exact model/provider/harness/control version and capture all observable interaction, tool/result, wait/failure, verification/provenance, output, continuity, and outcome signals that each harness exposes.

Historical v2 plan: the next slice was authorized by the measured local
research-track 22 result. The later advisory attempts produced no valid
aggregate, so this is not current run authorization. GitHub issue #7 is
complete; issue #2 is next after the issue #9 checkpoint PR merges and the
owner starts that experiment.

Historical v1 baseline: **Baseline multi-harness Work behavior replay**.
Historical v1 baseline contract: **Do not change prompts/control before this baseline.**
The old slice also stated: **Do not build a general state machine or protocol framework in this slice.** Those sentences remain here as the
preserved v1 baseline boundary; the research track formerly labeled 21 was a
separate v2 experiment and is not current authorization.

## Stop condition for this slice

Return with:
- comparable traces or explicit non-comparable reasons for all three harnesses;
- a compact automatic/structural comparison against Work reference evidence;
- the largest recurring behavioral deviations;
- exactly one smallest next control-layer hypothesis.

Do not build a general protocol framework in this slice. The v2 loop may use a
narrow runtime phase/transition gate because the owner explicitly approved
this controller experiment; expand it only if the measured replay requires it.

## Continuity rule

After real work, update this file to the measured result and exact next action. Do not use chat history as the project checkpoint.

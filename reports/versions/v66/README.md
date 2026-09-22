# v66 — replay prompts must carry the owner ask

Counts and flags only. No message bodies, no prompts.

## Defect

`run_controller_replay.py` and `run_opencode_replay.py` fed the harness
`user_turns(user.md)[0]`. In these Work transcripts the first stored turn is the
harness context preamble, not the ask. Measured over the 22 develop+holdout hashes:

| fact | count |
| --- | --- |
| pool tasks | 22 |
| turn 1 contains a context block | 19 |
| turn 1 is **context only** (no ask at all) | 11 |
| task found in a later turn after the fix | 11 |

Context-only hashes (shifted): `0d6ca4607eaf`, `28372e365066`, `2bde00530ddd`,
`6e412585c223`, `8d42bc26b8ea`, `b7e6393f4c14`, `bd179678f540`, `f37de8488162`,
`1442d08cf2d3`, `555f9c94ba8e`, `55fd1ef9b613`.

## Effect on the controller pilot

For every `replay-*-3-20260921` and `pilot-*` run, the baseline arm received
boilerplate only, and the Jev arm additionally received the controller directive —
the only actionable sentence in its prompt.

| arm | tool calls observed |
| --- | --- |
| baseline (all three adapters) | 0 |
| Jev (Pi, one hash) | up to 306 |
| Jev (OpenCode) | 5–13 |

So the recorded claim that the routing hint "increased tool activity and caused one
timeout" measures **instruction-present vs instruction-absent**, not routing quality.
Those cells are invalid as a comparison; see the banner in
`reports/jev-controller-pilot.md`. Do not recompute or re-quote them as evidence.

## Fix

- `research/replay_lib.py`: `strip_context_blocks`, `ask_text`, `ask_turns`,
  `first_ask`. `user_turns` keeps the raw transcript shape for counting and the
  older score tables.
- `research/run_controller_replay.py`: sends `first_ask`, passes `ask_present` /
  `ask_shifted` into controller state, and records both flags per row.
- `research/run_opencode_replay.py`: sequential and `--extra` paths use `ask_turns`;
  `--turn N` keeps raw indices so earlier notes stay reproducible, and returns
  `empty-ask` instead of running a boilerplate-only turn.
- `src/hos/controller/core.py`: `build_initial_state` no longer asserts
  `user_request_received` when no ask was extracted; it reports
  `user_request_missing`, sets `user_input_required`, and adds
  `do_not_infer_the_task_from_boilerplate`.
- `tests/test_replay_prompt_hygiene.py`: new gate. Registered in owner-gate together
  with `tests/test_jev_controller_module.py`, which existed but was never in CI.
- `src/hos/__init__.py`: import order fixed — it failed `ruff check src`, which the
  owner-gate runs.

## Wider blast radius: the headline OpenCode column

The same first-turn bug sits in the long-running OpenCode replay path, so the
`opencode` column of `reports/replay-scores.md` was earned partly on task-free
prompts. Of the 22 pool tasks, **11 are context-only in turn 1 and all 11 have an
`opencode.ndjson`** (2–102 tool calls each, so the cells look healthy — extra `-c`
turns can carry a real ask later in the thread). Those 11 cells describe behaviour
on a prompt with no ask, not imitation of Work on that ask.

The table rows were **not** rewritten: `tests/test_replay_scores.py` pins those exact
cells and mandatory owner-gate tests are not edited to hide a defect. The annotation
section is additive and `test_replay_scores_flags_contaminated_opencode_cells` now
fails if a context-only hash is missing from it. Work and Kilo columns are unaffected
(Work is scored from its own JSONL; Kilo cells come from sqlite copies).

## First valid rows (post-fix)

`replay-fix-20260922` (OpenCode / Qwen Flash, 150s, real ask in both arms):
`0d6ca4607eaf` baseline ok / 6 tool calls — the same arm logged 0 before the fix —
and `1a415bc257e5` baseline ok / 0 vs Jev 14. Both Jev rows hit the cap and no
work-match gain appeared, so this is a smoke test, not a controller result. See the
table in `reports/jev-controller-pilot.md`.

## Morph prompts: polluted but still valid

7 develop morphs (`0d6ca4607eaf`, `1a415bc257e5`, `1b09f49da9b9`, `28372e365066`,
`2bde00530ddd`, `6e412585c223`, `6eb8631b71ff`) embed the same context block, but
**every** morph still yields a non-empty ask after stripping. `run_opencode_morph.py`
reads the whole morph file as the prompt, so those runs carried the ask plus noise.
That is a cleanliness issue, not the empty-prompt defect: the "develop morphs 16/16"
result is **not** invalidated, and it should not be re-run just to drop the preamble.
If morphs are regenerated later, strip the blocks then — and change
`tests/test_replay_scores.py` pins in the same commit.

## Not done

The 11 contaminated OpenCode replay cells have **not** been re-run with the fixed
runner, so the OpenCode evidence for those hashes is still open (tracked under active
GitHub issue #2; v0 issue 13 is history). The larger
matched set (develop 16, fixed adapters, per-step state) has still not been re-run,
so there is no valid baseline-vs-Jev conclusion yet. Never compare new cells to the
pre-v66 numbers.

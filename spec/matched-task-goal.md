# /goal — matched-task outcome (copy-paste)

Paste this into Kilo `/goal` (Codex agent) when you want the run.

```
Outcome: Extract Work user asks into gitignored data/replay/ (never git). Replay each selected ask into Kilo Codex mode and OpenCode Codex/build (current models). Score process (R1–R6) and observable outcome (research, verification, whether the ask was addressed). Do not commit bodies. Do not SWE-bench.

Verification: pytest tests/test_matched_task_eval.py tests/test_extract_replay.py tests/test_work_replay_buckets.py -q stays green. data/replay/<hash12>/user.md exists locally and is gitignored. A scores table under data/replay/scores.md (gitignored) or reports/replay-scores.md with hashes only.

Constraints: ChatGPT Work sessions only (codex_work_desktop). Start with the 8 single-user-turn sessions, then 16 with 6–20 turns. Privacy: no message bodies in git. Keep existing owner-gate tests.

Boundaries: Not vscode. Not Harbor. Not re-testing Codex on a public bench. Do not print user.md in chat.

Stop when: extract done for the 8 singles; at least one Kilo and one OpenCode replay scored on process+outcome notes; owner can run the rest.
```

CLI equivalent:

```
python -m src.goal_cli set "PLAN F matched-task: extract Work asks to data/replay (gitignored), replay 8 singles in Kilo Codex + OpenCode, score process+outcome, no bodies in git, no SWE-bench"
python -m src.goal_cli gate --cmd "pytest tests/test_matched_task_eval.py tests/test_extract_replay.py -q"
```

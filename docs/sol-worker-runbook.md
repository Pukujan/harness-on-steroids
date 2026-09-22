# Sol worker runbook

This is the repeatable procedure for using the inexpensive CKFF Sol route as a
bounded reasoning agent in this repository or another local repository.

## What gets installed

The reusable part is deliberately small and dependency-free:

- `src/sol_bridge.py` — provider client, streamed tool loop, repository tools,
  path policy, and append-only run recorder.
- `src/sol_cli.py` — command-line entry point.
- `.env.example` — non-secret configuration shape.

To reuse it elsewhere, copy those three files into the target repository. The
bridge derives the repository root from the file location when run normally; the
CLI also accepts `--root` for an explicit root. The target repository should
keep its credential in an ignored `.env` and add `.sol/` to `.gitignore`.

## Configuration

Create `.env` from `.env.example` and set only the CC credential. The worker
reads `CKFF_CODEX_CC_API_KEY`, uses `gpt-5.6-sol`, streams every request, and
uses the CKFF primary endpoint before the backup endpoint. It never falls back
to `ckff-cortex-default`.

The request is intentionally bounded in two ways:

- one user task is sent per run;
- the model may take only `SOL_MAX_ROUNDS` tool-loop rounds, with a default of 8.

Each local check has its own 120-second limit. The provider request uses the
configured CKFF network timeout, while streaming keeps the connection active.

## Running a task

From the target repository:

```text
python -m src.sol_cli "Inspect the prompt stack and identify one smallest verified improvement. Do not edit until you have inspected the relevant files."
```

For a longer task description, keep the task text in a local ignored file:

```text
python -m src.sol_cli --task-file .sol/task.txt --max-rounds 6
```

Use `--dry-run` to exercise inspection, patch validation, and check planning
without writing files or running checks:

```text
python -m src.sol_cli --task-file .sol/task.txt --dry-run
```

The final response is printed, and the full local event record is written to
`.sol/runs/<run-id>.jsonl`. These records can contain task context and tool
results, so they are intentionally ignored and must not be committed.

## Tool-loop contract

Sol can request only these local operations:

1. `list_files` to discover visible repository files;
2. `search` to find relevant text;
3. `read_file` for bounded file reads;
4. `apply_patch` for unified patches or the Codex `*** Begin Patch` envelope;
5. `git_diff` to inspect the resulting change;
6. `run_checks` for allow-listed pytest, ruff, or mypy commands.

The worker validates every path against the repository root and blocks secrets,
raw JSONL transcripts, databases, corpus data, session directories, and local
run records. It applies patches through `git apply --check` first. It does not
execute arbitrary shell text. Codex-format edits to existing untracked files
use a guarded direct-write fallback only after the worker confirms that the
file is still byte-for-byte equal to the inspected version.

The expected cycle is:

```text
inspect -> propose -> patch -> diff -> check -> verify -> report
```

This is a small runtime lifecycle, not a general workflow language. The worker
owns execution and evidence; Sol owns bounded reasoning and verification.

## Reusing it with Beads

Beads can wrap this worker later, but it is not required for the tool loop. A
Beads task should represent one bounded worker run or one dependency unit. Put
the task ID in the task file and run record, then let the worker report the
patch and checks back to the task. Do not make Beads the canonical transcript,
prompt, or policy store, and do not run `bd init` in a target repository without
checking that repository's existing agent instructions and hooks.

## Recovery and handoff

If a provider call times out, rerun the same task with the same repository
state. The prior `.sol/runs` record shows the last assistant turn and tool
result. If a patch was applied but verification stopped, start with `git_diff`
and the relevant checks rather than repeating the patch. A future coordinator
can use the run ID as the handoff reference without needing the provider's
hidden conversation state.

## Portability boundary

The bridge is portable because it depends only on Python 3.11+ and the standard
library. The CKFF-specific pieces are the environment names, endpoints, model,
and streamed Chat Completions request. A different OpenAI-compatible provider
can reuse the local tool executor by replacing `ChatCompletionsClient`; the
path policy and tool loop do not depend on CKFF.

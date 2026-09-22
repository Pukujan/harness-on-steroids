# Jev controller module

The harness has a separate `src.hos.controller` module. The original v1 pilot
treated Jev as a bounded routing adviser: it received compact structured state
and proposed one next action from the shared 35-action taxonomy. That pilot is
preserved as smoke evidence only. The approved v2 design is documented in
`research/jev-controller-v2-research.md` and `spec/jev-controller-v2.md`.

In v2, Jev receives the full relevant decision context, including conversation
turns, coding-agent events, repository facts, open beads, candidate tasks, and
verification evidence. It answers typed Choice/Score/Noul questions. The
controller validates the answer, executes one bounded adapter step, folds the
observed result back into context, and asks Jev again. Jev never owns tools,
filesystem writes, subprocesses, or side effects.

Jev is hard-wired to the OpenRouter Decisions API and a Typesafe Jev model;
OpenCode Zen, CKFF, and generic chat models are rejected by configuration. The
selected harness still owns tool execution, filesystem writes, verification,
and escalation.

The module includes adapters for OpenCode, Grok Build, and Pi. OpenCode uses
the existing `codex` agent, Grok Build uses its JSON output mode and isolated
working directory, and Pi is configurable through `PI_COMMAND` and `PI_ARGS`.
The adapter reports unavailable when a CLI is not installed instead of
silently substituting another harness.

## Hosted execution arms

The current bounded comparison uses Grok Build’s authenticated xAI CLI with
`GROK_BUILD_MODEL=grok-4.7` and YOLO Auto’s Qwen Flash through the existing
OpenCode provider. Set `OPENCODE_MODEL=yolo-auto/qwen3.8-flash` and
`PI_MODEL=yolo-auto/qwen3.8-flash` when Pi is installed. The Qwen credential is
loaded from the ignored `.env`; it is never written into reports or command
output. The runner preserves the distinction between an unavailable Pi CLI and
a failed Pi model request.

Pi is run headlessly with `--print --mode json --no-session --approve`; its
adapter creates an ignored project-local `models.json` so the Qwen endpoint and
API-key environment reference do not modify the user’s global Pi setup.

## Bounded replay pilot

Run the first two existing develop hashes in baseline and Jev-controlled modes:

```powershell
python research/run_controller_replay.py --limit 2
```

The script loads the ignored repository `.env` in-process, reads only the first
user turn from each existing replay, and stores raw prompt/event files below
`.controller-runs/`. The committed result is intended to contain hashes,
controller labels, tool names, scorer cells, and adapter status only. Do not
copy prompts, message bodies, or secret values into reports.

This first pilot tested Jev as an initial routing hint. It does not claim that
a single hint is a full closed-loop controller. The next experiment is the v2
loop described above.

## Next-session implementation entrypoint

Start from `HANDOFF.md` and `checkpoints/CURRENT.md`. The first code slice is
the reusable context/decision loop plus fake-adapter tests. Do not delete or
rewrite the v1 pilot while the v2 behavior is being measured.

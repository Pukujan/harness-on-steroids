# Jev controller module

The harness now has a separate `src.hos.controller` module. It treats Jev as a
bounded routing adviser: Jev receives compact structured state and proposes one
next action from the shared 35-action taxonomy. Jev is hard-wired to the
OpenRouter Decisions API and a Typesafe Jev model; OpenCode Zen, CKFF, and
generic chat models are rejected by configuration. The selected harness still
owns tool execution, filesystem writes, verification, and escalation. This
keeps a state machine useful without granting a classifier authority over side
effects.

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

This first pilot tests Jev as an initial routing hint. It does not claim that a
single hint is a full closed-loop state machine. The next experiment should
feed verified post-step state back into Jev and compare the same matched tasks
with and without that additional decision point.

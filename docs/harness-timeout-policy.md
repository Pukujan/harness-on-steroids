# Harness execution timeout policy

Status: owner-requested reliability policy, 2026-09-22.

The harness runner must not kill an agent merely because one model response or
tool step takes longer than a short fixed wall-clock interval. A live stream is
evidence that the process is still working.

## Policy

- The default harness inactivity timeout is **1,200 seconds (20 minutes)**.
- Progress is observed from bytes arriving in the harness event or stderr
  stream files. Any progress resets the inactivity timer.
- A separate **7,200-second (two-hour)** absolute safety cap prevents a
  genuinely hung process from living forever.
- A timeout is recorded as either `inactivity` or `max_runtime`; both remain
  distinct from launch failures and model exit failures.
- The host kills a process only after one of those limits is reached. It does
  not impose a 60-second per-chunk or per-turn kill while output is advancing.

The timeout is a liveness boundary, not a task-completion policy. Harnesses
may finish earlier, return a partial result, or stop because their own task
budget is exhausted.

## Provider alignment

The adapters also configure the provider-side stream boundaries where the
harness supports project-local settings:

- OpenCode local-provider configuration uses 1,200,000 ms for request,
  header, and streamed-chunk timeouts.
- Pi project-local settings use 1,200,000 ms for HTTP idle and provider
  request timeouts, with agent-level retries enabled and provider retries kept
  at zero.

These settings match the host watchdog. The host watchdog remains authoritative
because not every provider or CLI exposes the same configuration surface.

## Why this matches TUI-agent behavior

OpenCode documents separate request, header, and streamed-chunk timeouts; the
chunk timer is specifically about a period with no streamed response, not the
total duration of an active streamed run:

https://opencode.ai/docs/config/

Pi exposes an HTTP header/body idle timeout, provider request timeout, and
agent-level retry policy. Its default configuration is likewise based on
inactivity and recovery rather than a one-minute total kill:

https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/settings.md

Our adapters now implement the same essential boundary independently of which
CLI is installed: active output keeps the run alive; prolonged silence is
recoverable; a long absolute cap remains for safety.

## Verification

`tests/test_jev_controller_module.py` proves both sides of the contract:

1. a child that emits output continuously beyond a short test inactivity
   window completes successfully;
2. a silent child receives a typed `inactivity` timeout.

The long-horizon Jev runner defaults to this policy and reports both timeout
settings and timeout reasons in its hash-only aggregate.

# Executive brief

## Decision in one sentence

Stop treating “behave like Codex” as two prompt files and a tool-order score; plan a portable behavior system that learns observable process policies from evidence and projects them through adapters without replacing the host harness.

## Durable objective

Given a task, available context, tools, permissions, failures, delays, user corrections, and accumulated evidence, a compatible harness should make the same *kind* of sound decisions as successful ChatGPT Work/Codex sessions:

- orient before consequential action;
- inspect and research the target rather than guessing;
- separate observation, inference, uncertainty, and absence;
- choose a task topology and split work only when useful;
- form an evidence-backed action plan;
- execute through available native capabilities;
- wait for asynchronous work and observe results;
- verify the requested outcome and the claims made about it;
- revise or recover after failures;
- preserve state across compaction, interruption, delegation, and restart;
- communicate progress, authority needs, blockers, and completion clearly;
- stop when the acceptance conditions are met or name exactly what is blocked.

This is a conditional process contract, not a fixed transcript, exact tool sequence, hidden-reasoning clone, or new standalone agent product.

## Product boundary

```text
Provenance exporter
  lossless capture -> canonical events -> indexes -> integrity
                                      |
                                      v
Harness on Steroids
  annotations -> behavior model -> portable protocol -> verifiers
                                      |
             +------------------------+-----------------------+
             v                        v                       v
       Pi adapter              Kilo adapter            OpenCode adapter
             |                        |                       |
             +----------- matched-task outcomes ---------------+
```

The host harness remains responsible for model selection, native tools, permissions, scheduling, UI rendering, and session persistence. The portable layer specifies semantic obligations and verifies conformance.

## What this proposal changes

1. The current Kilo/OpenCode modes become prototype adapters and historical evidence.
2. `update_plan` frequency, exact prose, and raw tool counts become descriptive diagnostics, not the behavior definition.
3. UX policy, research validity, provenance, action planning, verification, recovery, handoff, and compaction become first-class.
4. Pi and future harnesses are in scope from the protocol boundary, even if their adapters are implemented later.
5. Outcome evaluation becomes the promotion gate; process traces remain necessary diagnostics.

## What this proposal does not authorize

- no implementation or prompt rewrite;
- no deletion or cleanup of the current repository;
- no replay against private workspaces;
- no new Codex clone, summarizer, or public benchmark project;
- no raw transcript or account export committed to Git;
- no claim that existing Work research is complete;
- no `/goal` no-stop loop until the owner explicitly accepts the plan and gives go-ahead.

## First approval gate

The owner should accept the architecture and resolve the decisions in `10-owner-decisions-and-handoff.md` before any adapter or runtime work starts.

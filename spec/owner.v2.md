# Owner spec v2 - behavioral-control research contract

Normative machine copy: spec/owner.v2.json.

Status: **accepted by owner on 2026-09-21**. This supersedes owner spec v1 for active project direction. v1 remains historical evidence of the prompt-mode phase.

## Frozen claims

1. The user owns the project; agents do not replace the owner goal.
2. Local ChatGPT Work/Codex transcripts are the primary reference evidence for observable behavior. Tool calls are only one signal.
3. The project is model- and harness-agnostic.
4. Pi, OpenCode, and Grok Build are the concurrent normal development surfaces. Kilo Codex v0 is a positive-control baseline/history.
5. Prompt/context control is the first intervention. A runtime state machine is not required; enforcement must be earned by repeated measured failure.
6. Evaluate complete observable trajectories: interaction, research/inspection, execution/waits/failures, verification, provenance, output behavior, continuity, outcome, and repeated-run variance.
7. Every normal implementation slice is one behavior hypothesis, smallest intervention, automatic run/compare, then keep/revert/refine.
8. GitHub/repository state is durable project memory; chat is not.
9. Existing v0 modes/scorers/replays are preserved as evidence/baseline but may be replaced when measured replacements exist.
10. No public benchmark substitutes for the local reference corpus; no private transcript/account bodies or secrets enter Git.

## Unfrozen implementation details

Do not treat these as constitutional commitments:
- a full runtime state machine;
- a particular module layout;
- a particular model;
- one universal scoring weight;
- exact Work tool names or prose;
- a giant predeclared adapter/protocol framework.

Those choices are earned from experiments.

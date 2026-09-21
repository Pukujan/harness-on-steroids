# Action-plan and execution contract

## Why a separate action-plan phase exists

Research produces understanding; execution changes state. The bridge must be explicit so that a later verifier can answer why an action was selected, what authority it had, what result was expected, and whether the result was accepted.

The plan is semantic. It may be rendered as a child brief, structured checkpoint, native task list, or concise internal state. It is not required to be an `update_plan` call or a long plan document.

## Action-plan item

Each consequential item should carry:

- goal and authorized scope;
- current-state evidence and source pointers;
- task identity and dependency edges;
- target harness/actor and required capability;
- intended semantic action;
- prerequisites, authority, and approval state;
- expected artifact or state transition;
- acceptance criteria;
- verification method and owner;
- timeout, wait, retry, and escalation policy;
- recovery/rollback option;
- status, revision, and provenance links.

## Execution ledger

Every action should be traceable through this chain:

```text
evidence -> hypothesis/intent -> plan item -> native action
        -> observed result -> verification -> accepted/revised/recovered/blocked
```

The ledger should distinguish attempted versus completed, tool returned versus state changed, generated artifact versus validated artifact, local verification versus user-visible acceptance, current evidence versus stale evidence, and user-authorized scope versus incidental side effect.

## Research-to-action verifier

For each accepted plan item, the verifier should be able to answer:

1. What observation justified this action?
2. What alternative or uncertainty was known?
3. What authority allowed the action?
4. What native capability performed it?
5. What result was actually observed?
6. What verification was run afterward?
7. What final claim depends on this result?

If any answer is unavailable, the result is `unknown` or `not_observed`, not an inferred pass.

## Recovery policy

Classify failure before retrying: transient execution, invalid assumption, stale evidence, missing capability, permission boundary, dependency failure, verification failure, conflicting source, child-task failure, or context loss. Set a retry budget and escalation threshold. A blocked state must name the missing evidence, capability, authority, or external state precisely.

## Safety boundary

The system must not improve a process score by skipping verification, widening authority, making unauthorized writes, hiding uncertainty, or converting a partial result into completion.

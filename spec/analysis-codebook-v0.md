# Analysis codebook v0

Status: pilot. Ontology: `analysis-ontology/0.1.0`. Codebook:
`analysis-codebook/0.1.1`.

This codebook describes how observable evidence is labeled. It is separate
from the ontology because definitions can remain stable while annotation rules
or examples improve.

## Label rules

Use the narrowest label supported by an observable event or an explicit
artifact. Do not infer private reasoning, intent, project direction, or quality
from silence. `not_observed` means the predicate applies, the relevant evidence
surface is complete, and no qualifying event is present. `unknown` means the
evidence surface is incomplete, body-minimized, sampled, or ambiguously
ordered. `not_applicable` means the predicate's precondition is not evidenced;
`abstained` means a reviewer declines a body-dependent judgment.

| Label | Include when | Exclude when |
| --- | --- | --- |
| `inspection` | A file, repository, source, or observed tool result is explicitly observed | An inspect-classified call has no observed result; the agent merely says it inspected something |
| `inspection_action` | An inspect-family tool action is observed as an action request | Treating the action request as proof that file/source contents were observed |
| `mutation` | A file or external state is explicitly changed | A proposed patch is only described |
| `mutation_action` | A mutate-family tool action is observed as an action request | Treating the request or an unexamined result as proof that state changed |
| `verification` | An explicit verification-family action/result or independent evidence is observed after a material action | Generic execution, or a final answer that merely claims success |
| `citation_event_present` | A source/citation event is present in normalized evidence | Treating presence as citation correctness, claim support, or source quality |
| `research_observed` | An explicit research-family event or source-retrieval tool action is present | Citation presence alone, or an unclassified generic tool call |
| `unclassified_event_present` | A normalized event has an unknown canonical kind | Treating source telemetry gaps as agent uncertainty |
| `agent_uncertainty_observed` | An explicit agent/user uncertainty, abstention, or limitation event is observed | Inferring uncertainty from an unknown adapter kind or silence |
| `overplanned` | Planning is disproportionate, speculative, or delays useful inspection/action for the task | The plan is long but necessary and evidence-grounded |
| `unsupported_assumption` | A claim about state or direction lacks an observable supporting source | The user explicitly supplied the fact |
| `late_verification` | Verification occurs only after a material sequence that could have been checked earlier | No material change occurred |
| `emerging` | A repeated observable pattern does not fit an accepted category | A known label merely feels imperfect |

## Lane rules

Codex execution labels require tool/action/result evidence and are evaluated at
the episode/task level. Action-order metrics must be named explicitly as
`*_action_*_action`; a recognized action request is not the same as an
observed state change or result. ChatGPT chat/research labels use turn, citation, source,
answer, and UX evidence; research requires an explicit research/source-
retrieval event and citation presence is a separate label. A ChatGPT coding
conversation is still in the ChatGPT lane; `task_family=coding` is an
orthogonal field.

## Promotion requirements

A proposed category needs a definition, inclusion and exclusion rules,
positive examples, counterexamples, known confusions, source event IDs, lane,
and a proposed analytic use. Promotion requires a frozen pilot, an adjudicated
sample, disagreement reporting, and a migration map. A model proposal alone is
never gold.

## Provider boundary

The provider boundary is asymmetric and intentional:

- Sol is allowed only through the repository's CKFF route (`src.sol_bridge`)
  with the ignored `CKFF_CODEX_CC_API_KEY`. Sol is not allowed through native
  Codex spawning or a spawned subagent.
- Luna is allowed only through native Codex/ChatGPT subagent spawning. Luna is
  never allowed through CKFF, YOLO Auto, OpenRouter, a direct model endpoint, or
  a silently substituted provider.
- If the requested provider/model is unavailable in its allowed route, record
  the unavailable/error outcome and stop that arm. Do not cross the boundary to
  make the run appear complete.

Record requested model, returned model when available, execution surface,
configuration version, and provider error status without recording secrets.

# Analysis codebook v0

Status: pilot. Ontology: `analysis-ontology/0.1.0`.

This codebook describes how observable evidence is labeled. It is separate
from the ontology because definitions can remain stable while annotation rules
or examples improve.

## Label rules

Use the narrowest label supported by an observable event or an explicit
artifact. Do not infer private reasoning, intent, project direction, or quality
from silence. Record `unknown`, `not_observed`, or `abstained` when evidence is
missing.

| Label | Include when | Exclude when |
| --- | --- | --- |
| `inspection` | A file, repository, source, or tool result is explicitly observed | The agent merely says it inspected something |
| `mutation` | A file or external state is explicitly changed | A proposed patch is only described |
| `verification` | A test, check, diff, or independent evidence is observed after a material action | The final answer merely claims success |
| `citation` | A source or citation event is present in the normalized evidence | A factual sentence has no linked source |
| `overplanned` | Planning is disproportionate, speculative, or delays useful inspection/action for the task | The plan is long but necessary and evidence-grounded |
| `unsupported_assumption` | A claim about state or direction lacks an observable supporting source | The user explicitly supplied the fact |
| `late_verification` | Verification occurs only after a material sequence that could have been checked earlier | No material change occurred |
| `emerging` | A repeated observable pattern does not fit an accepted category | A known label merely feels imperfect |

## Lane rules

Codex execution labels require tool/action/result evidence and are evaluated at
the episode/task level. ChatGPT chat/research labels use turn, citation,
source, answer, and UX evidence. A ChatGPT coding conversation is still in the
ChatGPT lane; `task_family=coding` is an orthogonal field.

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

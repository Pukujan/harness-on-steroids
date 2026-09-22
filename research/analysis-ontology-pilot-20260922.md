# Analysis ontology pilot report

Date: 2026-09-22  
Ontology: `analysis-ontology/0.1.0`  
Codebook: `analysis-codebook/0.1.1`
Status: pilot adjudicated; no labels promoted to accepted

## Why this report exists

The full-corpus pass proves that the analysis machine can produce stable,
body-minimized structural evidence. It does not provide enough source-linked
examples to turn every useful idea into a reliable annotation category. This
report separates what can be reported directly from the current event tables
from what needs a human-reviewed sample.

## Frozen pilot and independent review

The deterministic selector froze eight pilot episodes (four Codex and four
ChatGPT) containing 2,671 body-free events, plus four sealed holdout episodes
(two Codex and two ChatGPT) containing 2,909 body-free events. The local
manifest and event files are ignored under
`data/derived/analysis-machine/ontology-pilot-20260922-v2/`; the split is
disjoint and reproducible from the committed selector
`research/build_analysis_ontology_pilot.py`.

Two independent native Luna reviewers read only the codebook, ontology,
manifest, and pilot event file. They did not receive the holdout or raw corpus.
Their outputs were advisory annotations, not hidden reasoning or gold truth. One
reviewer attempted an unrelated issue lookup during its run; no external
content was used in the labels or adjudication, which relied only on the local
pilot artifacts.

## Adjudication

The initial disagreement was useful because it exposed adapter/codebook
ambiguity:

| Question | Reviewer disagreement | Adjudicated rule/result |
| --- | --- | --- |
| `research_observed` in four ChatGPT episodes | One reviewer counted explicit `web.run` tool calls; the other required canonical kind `research` | The final adapter maps research/source-retrieval tool names to `tool_family=research`; all four pilot ChatGPT episodes are `observed` |
| `inspection_before_mutation` in three Codex episodes with no mutation | `unknown` versus `not_applicable` | `not_applicable`: the mutation predicate is not evidenced |
| `inspection_before_mutation` in the Codex mutation episode | `observed` from an inspect call versus `unknown` because the call had no observed result | `unknown`: an inspect action request is not proof that contents were observed |
| `verification_after_mutation` in no-mutation episodes | `unknown` versus `not_applicable` | `not_applicable` |
| `verification_after_mutation` in the mutation episode | Both reviewers returned `unknown` | `unknown`: no explicit verification-family result/evidence was present |
| Unknown telemetry | Both observed unknown events | Rename the annotation label to `unclassified_event_present`; it is not agent uncertainty |

All eight reviewers abstained on `overplanned`, `unsupported_assumption`,
`late_verification`, and `outcome_quality`, as required by the body-free
evidence boundary. Citation presence was consistently observable, but it is
now named `citation_event_present` in the codebook and is not citation
correctness or claim support.

The codebook was bumped to `analysis-codebook/0.1.1` to record these
non-breaking operational clarifications. No category is promoted to
`accepted`: the pilot demonstrates that structural presence labels are
reviewable, while body-dependent quality labels require a richer evidence
surface and a separate adjudicated sample.

## Reportable now as structural observations

These labels are narrow descriptions of normalized evidence, not judgments of
quality:

- `event_observed`: a canonical event with a valid adapter classification;
- `unknown`: an event whose kind or source shape is outside current coverage;
- `mutation_episode`: an episode containing a mutation-family event;
- `inspection_action_before_mutation_action`: a qualifying inspect-family
  action precedes the first mutate-family action in an episode;
- `verification_action_after_mutation_action`: a qualifying verify-family
  action follows a mutate-family action;
- `delegation_observed`: a delegation-family event is present;
- `compaction_observed`: a normalized compaction event is present;
- `citation_event_present`: a citation event is present in a ChatGPT episode;
- `research_observed`: an explicit research-family event or source-retrieval
  tool action is present;
- `unclassified_event_present`: a normalized event has an unknown canonical
  kind; this is not agent uncertainty;
- `code_event` and `execution_output_event`: the source adapter exposes the
  corresponding content type.

Every rate must publish its numerator, denominator, lane, adapter definition,
ontology version, and missingness coverage. Citation presence is not citation
validity or claim support.

## Categories that require annotation before use

The following cannot be promoted from the summary-only aggregate or this
body-free pilot:

- `overplanned`, `underplanned`, or proportionate planning;
- `unsupported_assumption` and `late_verification` as quality judgments;
- user intent, task family, answer quality, UX quality, or response quality;
- complete, partial, blocked, failed, or successful outcome;
- citation correctness, source quality, claim support, or research sufficiency;
- corrections, handoffs, continuity quality, and context sufficiency;
- whether a verification was substantively adequate;
- any inference about private reasoning, motivation, or project direction.

An action request can support `inspection_action` or `mutation_action` and the
two action-order metrics above, but `inspection`, `mutation`, and
`verification` require the corresponding observed result/evidence. Generic
`execute` calls stay `unknown` for semantic labels.

These labels need a source-linked, body-minimized event sample plus the
minimum content or artifact view required by their definition. They must be
double-reviewed independently, adjudicated, and tested on a sealed holdout.
Native Luna proposals can help identify candidate definitions or confusions,
but they are advisory and never the gold annotation by themselves.

## Missingness policy

- `unknown`: the adapter or event shape cannot support the label.
- `not_observed`: the predicate applies, the evidence surface is complete, and
  no qualifying event is present.
- `not_applicable`: the task or denominator does not apply.
- `abstained`: a reviewer declines because the judgment is body-dependent or
  evidence is insufficient.
- `emerging`: a repeated observable pattern does not yet fit a promoted term.

Never convert `unknown` or `abstained` into zero. A zero event count must be
reported as an observed zero only when the adapter coverage and denominator
support that claim. Research-family tool names such as `web.run` are now
explicitly normalized; citation presence alone still does not establish
research sufficiency.

## Pilot protocol

1. Freeze a small sample separately for Codex execution and ChatGPT
   chat/research. Keep source pointers and stable event IDs, but retain no raw
   bodies in Git.
2. Write inclusion/exclusion rules, positive examples, counterexamples, and
   known confusions before annotation.
3. Have two reviewers label independently; record agreement by label and lane.
4. Adjudicate disagreements without changing the frozen sample silently.
5. Promote only categories that answer a stated analysis question and have a
   migration map from the pilot vocabulary.
6. Rerun the old and new ontology versions on the same frozen pilot and a
   sealed holdout. Treat changed scores as new results, never as historical
   rewrites.

The planned verification step was to apply the adjudicated codebook to the
four sealed holdout episodes with fresh independent reviewers, then compare
agreement without tuning the selector or adapter on holdout labels; that check
is recorded below.

## Sealed holdout check

After the pilot adjudication, two fresh native Luna reviewers independently
read only the four holdout episodes. They agreed on all citation, research,
unclassified-event, and body-dependent-abstention labels. One Codex episode
contained a mutation action request marked `not_observed` plus a body-free
result; reviewers differed between `unknown` and `not_applicable` for the
inspection/verification relations. Under the final rule that `mutation`
requires an observed state change, the adjudicated result is
`not_applicable`; an action request alone cannot establish a mutation.

The holdout therefore confirms that the final missingness rule is mechanically
usable across unseen episodes, but it does not justify promoting quality or
outcome categories. The structural citation/research/unclassified labels stay
in pilot status until a larger lane-balanced sample and a human-adjudicated
agreement study answer a concrete analysis question.

## Provider provenance rule

Sol is permitted only through the local CKFF Sol worker. Luna is permitted only
through native Codex/ChatGPT subagent spawning and is never permitted through
CKFF. Provider/model, execution surface, configuration version, and unavailable
or error outcomes belong in the analysis run metadata without secrets.

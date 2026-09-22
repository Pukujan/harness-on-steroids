# Analysis ontology pilot report

Date: 2026-09-22  
Ontology: `analysis-ontology/0.1.0`  
Codebook: `analysis-codebook/0.1.0`  
Status: pilot; no labels promoted to accepted

## Why this report exists

The full-corpus pass proves that the analysis machine can produce stable,
body-minimized structural evidence. It does not provide enough source-linked
examples to turn every useful idea into a reliable annotation category. This
report separates what can be reported directly from the current event tables
from what needs a human-reviewed sample.

## Reportable now as structural observations

These labels are narrow descriptions of normalized evidence, not judgments of
quality:

- `event_observed`: a canonical event with a valid adapter classification;
- `unknown`: an event whose kind or source shape is outside current coverage;
- `mutation_episode`: an episode containing a mutation-family event;
- `inspection_before_mutation`: a qualifying inspection-family event precedes
  the first mutation-family event in an episode;
- `verification_after_mutation`: a qualifying verification-family event follows
  a mutation-family event;
- `delegation_observed`: a delegation-family event is present;
- `compaction_observed`: a normalized compaction event is present;
- `citation_present`: a citation event is present in a ChatGPT episode;
- `code_event` and `execution_output_event`: the source adapter exposes the
  corresponding content type.

Every rate must publish its numerator, denominator, lane, adapter definition,
ontology version, and missingness coverage. Citation presence is not citation
validity or claim support.

## Categories that require annotation before use

The following cannot be promoted from the summary-only aggregate:

- `overplanned`, `underplanned`, or proportionate planning;
- `unsupported_assumption` and `late_verification` as quality judgments;
- user intent, task family, answer quality, UX quality, or response quality;
- complete, partial, blocked, failed, or successful outcome;
- citation correctness, source quality, claim support, or research sufficiency;
- corrections, handoffs, continuity quality, and context sufficiency;
- whether a verification was substantively adequate;
- any inference about private reasoning, motivation, or project direction.

These labels need a source-linked, body-minimized event sample plus the
minimum content or artifact view required by their definition. They must be
double-reviewed independently, adjudicated, and tested on a sealed holdout.
Native Luna proposals can help identify candidate definitions or confusions,
but they are advisory and never the gold annotation by themselves.

## Missingness policy

- `unknown`: the adapter or event shape cannot support the label.
- `not_observed`: the searched-for qualifying event was absent from the known
  evidence.
- `not_applicable`: the task or denominator does not apply.
- `abstained`: a reviewer declines because evidence is insufficient.
- `emerging`: a repeated observable pattern does not yet fit a promoted term.

Never convert `unknown` or `abstained` into zero. A zero event count must be
reported as an observed zero only when the adapter coverage and denominator
support that claim. The current ChatGPT `research_events: 0` is therefore
`not_observed`/unavailable for this adapter view, not evidence that research did
not occur.

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

## Provider provenance rule

Sol is permitted only through the local CKFF Sol worker. Luna is permitted only
through native Codex/ChatGPT subagent spawning and is never permitted through
CKFF. Provider/model, execution surface, configuration version, and unavailable
or error outcomes belong in the analysis run metadata without secrets.

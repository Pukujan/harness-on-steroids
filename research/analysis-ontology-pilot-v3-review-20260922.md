# Analysis ontology pilot v3 review

Date: 2026-09-22  
Ontology: `analysis-ontology/0.1.0`  
Codebook: `analysis-codebook/0.1.1`  
Status: advisory review complete; no labels promoted to accepted

## Frozen sample

The deterministic selector produced a new pilot under the ignored local
evidence plane:

`data/derived/analysis-machine/ontology-pilot-20260922-v3/`

- Pilot: 24 episodes, 12 Codex and 12 ChatGPT, 8,930 canonical body-free
  events.
- Sealed holdout: 8 episodes, 4 Codex and 4 ChatGPT, 3,231 events.
- The pilot and holdout are disjoint. The holdout was not opened by reviewers.
- Source identity and event pointers remain in the local evidence plane; raw
  transcript bodies were not exported.

Four independent native Luna reviews were used as advisory annotations: two
for Codex and two for ChatGPT. They received the codebook, ontology, manifest,
and pilot events only. They did not use CKFF/Sol, browse externally, edit the
repository, or inspect raw corpus files.

## Deterministic reference counts

The canonical event fields are the authoritative reference for structural
presence labels. The pilot contains:

| Lane | Events | Structural result |
| --- | ---: | --- |
| Codex | 2,559 | 2 episodes with an observed inspect-family action; 1 episode with 17 observed mutation actions; 0 observed verification actions; 9 delegation actions; 1 compaction; 166 unknown events |
| ChatGPT | 6,371 | 10/12 episodes with citation events; 9/12 with explicit research-family events; 5/12 with `content_type=code`; 1/12 with `content_type=execution_output`; 14 unknown events |

These are structural observations. They do not establish quality, correctness,
intent, completion, research sufficiency, or successful mutation.

## Review agreement and disagreement

### Codex lane

The two reviewers agreed on the main boundary: an observed action request is
not automatically observed state change, and generic execution cannot be
called verification without a qualifying event/result. They agreed that
body-dependent labels must be abstained.

The main ambiguity was an `inspect` family on an observed `create_thread`
result. The result is observable metadata, but it is not evidence that a file,
source, or repository state was inspected. Under the current narrow codebook,
that case remains unknown/not applicable for inspection evidence. Only an
observed inspect-family `tool_call` supports `inspection_action`; a qualifying
observed source/file result is needed for `inspection`.

Both reviewers also surfaced an ontology gap: lifecycle events such as
`task_complete` and `turn_aborted` are present in the canonical stream but are
not yet accepted outcome labels. They remain `emerging`, not completion or
quality judgments.

### ChatGPT lane

The reviewers agreed on the major citation/research distinction and abstained
from overplanning, unsupported assumptions, late verification, UX, outcome,
and citation correctness. They identified rendered-turn-only and
provenance-only episodes as evidence-surface limitations rather than failures.

There were material review errors and inconsistencies:

- One reviewer reported 4,371 ChatGPT events; the deterministic event file
  contains 6,371. The error was arithmetic/reporting, not a corpus change.
- One reviewer treated all code and execution-output labels as unknown even
  though `content_type=code` and `content_type=execution_output` are explicit
  canonical attributes. Those are valid structural observations without
  retaining body text.
- Research-family counts were reported as 8/12 or 9/12 by different reviews;
  the canonical rule is explicit `kind=research` or `tool_family=research`,
  which yields 9/12 in this pilot.
- `source_linked` was used by one review as a convenient label, but it is not
  by itself evidence that a citation is correct or that a claim is supported.

These errors are exactly why model annotations remain advisory. They cannot
replace deterministic event accounting or an adjudicated reference set.

## Adjudicated operational rules

The v0 codebook remains the governing interpretation for this pilot:

1. `code_event` and `execution_output_event` are observed when the canonical
   `content_type` attribute explicitly carries those values. Body text is not
   required for this structural label.
2. `research_observed` requires an explicit research-family event or
   source-retrieval tool action. `citation_event_present` is separate and does
   not prove research sufficiency or claim support.
3. `inspection_action` requires an observed inspect-family action request.
   An inspect-family result without a corresponding action is not enough to
   establish the action.
4. `inspection`, `mutation`, and `verification` require the corresponding
   observed evidence/result. A patch request, generic shell command, or
   unexamined result is not state-change or verification proof.
5. Lifecycle events are retained as observable events but are not promoted to
   `complete`, `partial`, `failed`, or outcome quality without a defined
   outcome evidence surface.
6. `unknown`, `not_observed`, `not_applicable`, and `abstained` remain distinct;
   none is converted into a zero merely to make a rate look complete.

## What this teaches us about Jev

This review supports a fast Jev annotation lane only as a bounded, separate
sidecar. Jev could receive one canonical event or checkpoint, the ontology
definition, and a closed label set, then return a label and confidence. The
host must still validate the label, preserve the original event, record the
request/answer/configuration, and compare Jev against deterministic rules and
human adjudication.

The review also shows why Jev should not be used to capture or aggregate the
dataset: even human-readable model reviews can miscount events or overlook
explicit structured fields. Capture and aggregation remain deterministic.

## Decision and next step

No quality, UX, planning, provenance-correctness, or outcome category is
promoted from this pilot. The sealed holdout remains closed. The next required
step is owner/human adjudication of a source-linked structural batch, followed
by a separate Jev shadow-label experiment. The controller A/B follow-up for
low-confidence advisory fallback remains a different experiment and must not
be combined with ontology tuning. The deterministic packet for that review is
generated by `research/build_analysis_review_packet.py` and currently lives in
the ignored local evidence plane at
`data/derived/analysis-machine/ontology-review-packet-v3/`.

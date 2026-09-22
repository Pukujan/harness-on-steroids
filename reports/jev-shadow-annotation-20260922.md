# Jev shadow structural annotation probe — 2026-09-22

Status: bounded live probe; not a quality benchmark and not a promoted
annotation lane

## Contract

The runner was `research/run_jev_shadow_annotation.py`, using the OpenRouter
Decisions API and `typesafe/jev-1.13`. It selected a deterministic sample from
the v3 pilot only:

- 8 canonical events across Codex and ChatGPT;
- 8 independent Noul questions per event;
- 64 typed probabilities returned;
- body-free canonical fields only;
- no raw response or transcript body written;
- the v3 holdout was not opened or sent;
- no execution or repository mutation was authorized.

The local run manifest and results remain ignored under
`data/derived/analysis-machine/jev-shadow-annotation-20260922-v1/`.

Jev's official model contract describes typed answers and probabilities for
host-supplied state, while the host retains capture and validation:

- https://docs.typesafe.ai/concepts/system-one
- https://github.com/TypeSafeAI/typesafe-playground/blob/main/docs/jev-browser-agent.md

## Result

At a binary threshold of `0.50`, 62 of 64 predictions matched the
deterministic canonical-field label: **96.875% on this tiny structural probe**.
All 64 answers were valid probabilities. The two errors were:

- one false-positive `research_observed` prediction at `p(true)=0.58`;
- one false-negative `mutation_action` prediction at `p(true)=0.38`.

The exact same sample and schema were run three times (`v1`, `v2`, and `v3`).
Each run returned 64 valid probabilities and 62/64 correct labels. Every one
of the 64 thresholded predictions was identical across all three runs. The
mean per-question probability range across runs was 0.0112 and the maximum
range was 0.08. This is a useful stability signal for this tiny probe, not a
general variance estimate.

| Predicate | Questions | Expected positives | Correct | Accuracy |
| --- | ---: | ---: | ---: | ---: |
| `citation_event_present` | 8 | 1 | 8 | 100% |
| `code_event` | 8 | 2 | 8 | 100% |
| `execution_output_event` | 8 | 1 | 8 | 100% |
| `inspection_action` | 8 | 1 | 8 | 100% |
| `mutation_action` | 8 | 1 | 7 | 87.5% |
| `research_observed` | 8 | 1 | 7 | 87.5% |
| `unclassified_event_present` | 8 | 1 | 8 | 100% |
| `verification_action` | 8 | 1 | 8 | 100% |

The Noul responses did not include a separate confidence field in this run;
the returned probability of `true` was used as the classification score. That
is distinct from assuming that every Jev response will expose a universal
confidence field.

## Threshold sensitivity

The following is descriptive for this eight-event sample only. A result was
accepted when either `p(true)` or `p(false)` met the threshold; otherwise it
was treated as abstained.

| Acceptance threshold | Accepted | Abstained | Accepted accuracy | Wrong accepted |
| ---: | ---: | ---: | ---: | ---: |
| 0.50 | 64 | 0 | 96.9% | 2 |
| 0.60 | 63 | 1 | 98.4% | 1 |
| 0.75 | 59 | 5 | 100% | 0 |
| 0.85 | 54 | 10 | 100% | 0 |
| 0.90 | 46 | 18 | 100% | 0 |

This is the desired fast-classification tradeoff in miniature: Jev can provide
a quick score, while host policy chooses whether to accept or abstain. It does
not establish that `0.75` is the correct production threshold; threshold and
calibration must be measured on a larger adjudicated sample.

The repeated-run result also separates two properties that should not be
collapsed: thresholded label stability was perfect on this sample, while
probability values varied slightly. Both should be measured in future runs.

## Interpretation

This probe supports Jev as a potentially useful **semantic annotation
sidecar** for bounded questions. It does not replace deterministic capture,
normalization, provenance, or aggregation. The direct structural predicates
were intentionally easy and mechanically defined; the probe says nothing yet
about `overplanned`, UX, answer quality, research sufficiency, unsupported
assumptions, or outcome quality.

The correct production shape remains:

```text
capture event deterministically
  -> apply mechanical labels in code
  -> queue only semantic/ambiguous questions for Jev
  -> validate typed probability and ontology version
  -> accept, abstain, or send to review
  -> retain the original event and aggregate separately
```

## Next experiment

Do not tune the ontology or controller from this probe. First obtain owner/
human adjudication from the v3 review packet. Then run a larger repeated Jev
shadow study with:

1. stratified Codex and ChatGPT samples;
2. semantic labels with explicit abstention;
3. repeated calls for variance;
4. per-label precision, recall, coverage, and calibration;
5. request/configuration digests and provider/model metadata;
6. the holdout sealed until the annotation policy is frozen.

This remains separate from the Jev controller A/B and its low-confidence
advisory-fallback hypothesis.

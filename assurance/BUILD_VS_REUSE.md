# Build vs reuse (draft, not reviewed)

Assessment status: **draft**. PAM `build-vs-reuse@0.2.0` REUSE_008 is not satisfied. Do not treat this as `build_new` authorization.

Capability under comparison: **measure research/verify/plan/mutate loops from local agent transcripts, counts-only, privacy-preserving.**

This is **not** the capability “make Kilo behave like ChatGPT.” That capability is out of scope.

## Decision criteria

- Concrete locators, not abstract categories
- No message bodies in git
- Copy-then-hash
- Cheap probe preferred over prose rejection
- Internal systems count (Codex sqlite, Kilo/OpenCode dbs, hades stats script)

## Candidates

| ID | Name | Locator | Origin | Coverage | Disposition |
| --- | --- | --- | --- | --- | --- |
| C1 | hades counts-only stats | `Pukujan/hades-product` `tools/transcript_stats.py` | internal | partial (privacy pattern only; wrong schema) | **wrap / extend pattern** |
| C2 | Codex item_type projection | local `~\.codex\thread_history_1.sqlite` | internal | full for Codex loop proxies | **reuse** as first metrics surface |
| C3 | Codex JSONL rollouts | local `~\.codex\sessions` + `archived_sessions` | internal | full source of truth | **reuse** via copy-hash + stream |
| C4 | OpenCode session db | local `~\.local\share\opencode\opencode.db` | internal | full for OpenCode | **reuse** via sqlite copy |
| C5 | Kilo CLI db | local `~\.local\share\kilo\kilo.db` | internal | full for this Kilo | **reuse** via sqlite copy |
| C6 | FOSSIL | `Pukujan/fossil-core` (and sibling pack repos) | internal | lineage later, not live tracker | **defer** until contrast |
| C7 | PAM | `Pukujan/project-assurance-modules` | n/a | methodology only | **not a product candidate** (PAM forbids counting itself) |
| C8 | Hermes / hades gateway conversations schema | hades-v2 memories export | internal | wrong corpus | **reject** as event model |
| C9 | New events.v1 + 26-issue campaign product | this repo as designed in the plan | proposed bespoke | full if built | **not earned yet** (`more_research` / compose first) |

## Probes

- Inventory glob + sqlite table/row counts: **run** (this session). Evidence: `reports/` overnight + this file.
- `item_type` sequence proxies without bodies: **run** overnight against a sqlite backup.
- JSONL stream type/tool-name walk skipping body keys: **run** overnight against hashed copies.
- events.v1 goldens product: **not_run** — disproportionate until C2/C3 histograms exist.

## Disposition

**compose** existing stores and the hades counts-only pattern.

**more_research** on whether a dedicated events.v1 adapter is still needed after sqlite+JSONL histograms.

**not** `build_new` of the 26-issue software campaign.

Reconsider if: hashed JSONL types cannot map to observe/mutate; or sqlite `item_json` is required for tool names and we still need a streaming adapter (still counts-only).

Human review: pending. User asked to re-run PAM and lead with analysis; overnight pipeline is the cheap probe, not projectization.

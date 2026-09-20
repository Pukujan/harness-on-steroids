# Scope boundary (draft)

Not frozen. Human still owns admission of new work.

## Current goal

Lead with **data analysis** of local Codex/Work transcripts, compared to local OpenCode and Kilo sessions. Produce counts-only inventory, classification rules, and a contrast draft.

## Current claims

- Local Codex/Work JSONL + sqlite exist and are the ChatGPT-app-adjacent corpus on this PC.
- OpenCode and Kilo CLI databases exist and can be inventoried without Cloud.
- ChatGPT.com Cloud is not available as local transcripts (except two `chatgpt_handoff` threads).
- Classification can start from Codex `thread_items.item_type` without putting bodies in git.

## Explicit non-goals (now)

- Making Kilo/OpenCode “as reliable as ChatGPT” in this campaign (that is the **next** campaign after contrast).
- Creating the 26 GitHub issues / Milestone A bootstrap.
- Freezing `PROJECT_ASSURANCE` without human review.
- Patching Kilo, OpenCode, Pi, Beads, MCP, or hades.
- Scraping Brave or Chromium cache.
- Treating unofficial Cloud APIs as a corpus.
- Committing message bodies, raw JSONL, sqlite, or `session_diff`.

## Deferred

| Item | Trigger to reconsider |
| --- | --- |
| events.v1 adapters + goldens as a software product | Reviewed reuse assessment says compose/wrap is not enough |
| GitHub issue catalog | Human accepts projectization facts (`software=true`, `projectization=true`) |
| FOSSIL pack v1 | Contrast draft exists and lineage is worth pinning |
| Cloud ZIP adapter | A ZIP actually appears in `data/incoming/` |
| Harness behavior changes | Milestone F-style contrast exists and is reviewed |
| Empirical “Codex is more rigorous” claim | Then `benchmark.integrity` becomes required |

## Rejected

- Chromium cache as transcripts
- Brave scrape
- Kilo-only analysis labeled “ChatGPT analysis”
- `build_new` of a quiz-style abstract “generic transcript framework”

## Scope-admission rule

New work enters the **current** horizon only if it is required to measure, copy-hash, or classify local corpora without leaking bodies. Product/harness changes need a new reviewed scope.

## Repository boundary

This repo (`Pukujan/harness-on-steroids`) may hold research artifacts, gitignored copies, counts-only reports, and later schemas. It must not own Kilo product, OpenCode product, hades, or `colorful-income`.

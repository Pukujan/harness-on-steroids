# Night notes — 2026-09-20 05:24Z

Pipeline **complete**. Copy-hash 1518/1518, 0 errors, ~1.42 GB hashed JSONL. Sqlite backups present. No bodies in reports.

## Findings worth keeping

1. ChatGPT.com is not local. Codex/Work JSONL is the corpus.
2. Codex does **not** look like “plan then search then patch” in `item_type`. Plan is almost unused. Search-before-fileChange is 30% of mutating threads. Exec is the bulk tool.
3. OpenCode local db is polluted by Study OS replay. Filter before contrast claims.
4. Kilo n=18, but those sessions are long and read-heavy (94% observe-before-mutate in-sample).
5. PAM research facts still hold: do not projectize tonight.

## Files

- `reports/local-corpus.md`
- `reports/codex-jsonl-types.md`
- `reports/kilo-opencode-tools.md`
- `reports/contrast-draft.md`

## Next (still research)

Optional: hashed-arg exec classifier; OpenCode coding-only subset. Not GitHub issues. Not harness patches.

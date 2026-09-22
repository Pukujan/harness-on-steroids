# Local CKFF Codex CLI

This repository has local CKF AI TECH credentials for bounded Codex CLI and compatible model calls. The secret values live only in the ignored `.env` files. Do not print, commit, paste, or send them to another service.

## Active credentials

- `CKFF_CODEX_CC_API_KEY` is the Codex CLI default. Its `gpt-5.6-sol` probe returned streamed Responses successfully.
- `CKFF_CODEX_PRO_API_KEY` is available for OpenAI-compatible Chat Completions callers. Its `gpt-5.6-sol` probe returned streamed Chat Completions successfully. Its streamed Responses path was not confirmed within the bounded probe, so do not assume it works with Codex CLI.
- The source credential named `ckff-cortex-default` is intentionally not active. It exposes many models but is the expensive route for GPT models and is excluded from local Codex selection.

The source env has no literal `cortex-codex-2` variable. The prior default-like credential is the one deliberately excluded above.

## CKFF endpoints and timeouts

The CKFF website identifies these OpenAI-compatible base URLs:

- Primary: `https://ckffai.com/v1` — 600-second network timeout; preferred.
- Backup: `https://aws.ckffai.com/v1` — 180-second network timeout; use only as fallback.

The service warns that non-streaming requests can fail at the shorter timeout. Use streaming for every long or reasoning-heavy request. Keep work granular and bounded so one request represents one meaningful task or verification step; preserve the endpoint timeout appropriate to the selected route.

The preferred Codex CLI model is `gpt-5.6-sol`. The credential-specific model list is authoritative; query `/v1/models` before changing the model.

## Local Sol worker

This repository's `src.sol_bridge` uses the CC credential with streamed HTTP Chat Completions. It is the local agent route for Sol: the model requests bounded tools, while the worker validates and executes them in the repository. It supports visible file listing, search, bounded reads, unified patches, diffs, and allow-listed checks. Run records are written under the ignored `.sol/runs/` directory.

The native Codex CLI path is not the worker implementation. During the initial probe, that CLI attempted CKFF's `/v1/responses` WebSocket transport and received `404`; therefore do not silently switch this worker to the expensive default credential or assume the native CLI transport is compatible. The worker stays on the streamed CC Chat Completions route until a separate compatibility probe proves otherwise.

## Codex CLI usage

`.env` is ignored and is not automatically loaded by every shell or agent. Load it only into the process that needs it, set `CODEX_API_KEY` from `CKFF_CODEX_CC_API_KEY`, and point Codex's OpenAI provider at the primary CKFF base URL. Codex custom provider configuration uses an environment key and a base URL; its streamed provider path is the relevant one here.

Do not use `ckff-cortex-default` as a fallback for GPT work. If CC is unavailable, stop and report the credential or endpoint failure rather than silently switching to the expensive default route.

## Sources

- CKFF setup and endpoint guidance: <https://ckff.dev/>
- Codex manual: <https://developers.openai.com/codex/codex-manual.md>

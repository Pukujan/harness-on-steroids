# Free models that advertise tools

No secrets. OpenRouter rows: price 0 and `tools` in supported_parameters.

## Tried earlier (do not repeat blindly)

- `openrouter/z-ai/glm-5.2:free` — 400 no tool endpoints
- `openrouter/qwen/qwen3.8-27b:free` — tools then 429 rate-limit
- `openrouter/google/gemma-4-31b-it:free` — 429
- `opencode/glm-5.3-flash` — fail
- `opencode/deepseek-v4-flash` — **402 insufficient funds**
- `opencode/ling-3.0-flash-fin-free` — timeout/empty
- `yolo-auto/qwen3.8-flash` — tools when it ran

## OpenRouter free + tools advertised

- host: `openrouter.ai` HTTP 200 count **20**

- `cohere/north-mini-code:free`
- `dots-studio/dots-3-note-preview:free`
- `google/gemma-4-26b-a4b-it:free`
- `google/gemma-4-31b-it:free`
- `inclusionai/ling-3.0-flash-fin:free`
- `inclusionai/ling-3.0-flash-sante:free`
- `inclusionai/ling-3.0-flash-vl:free`
- `liquid/lfm-2.5-2.6b:free`
- `nex-agi/nex-n2.5-mini:free`
- `nex-agi/nex-n2.5-pro:free`
- `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free`
- `nvidia/nemotron-3-super-120b-a12b:free`
- `nvidia/nemotron-3-ultra-550b-a55b:free`
- `nvidia/nemotron-3.5-lightning:free`
- `openrouter/free`
- `poolside/laguna-s-2.1:free`
- `poolside/laguna-xs-2.1:free`
- `qwen/qwen3.8-27b:free`
- `thinkingmachines/inkling-small:free`
- `thinkingmachines/inkling:free`

## OpenRouter tool ping (status only)

- `cohere/north-mini-code:free` → 200 tools
- `dots-studio/dots-3-note-preview:free` → 200 tools
- `google/gemma-4-26b-a4b-it:free` → 429 {"error":{"message":"Provider returned error","code":429,"metadata":{"raw":"goog
- `google/gemma-4-31b-it:free` → 429 {"error":{"message":"Provider returned error","code":429,"metadata":{"raw":"goog
- `inclusionai/ling-3.0-flash-fin:free` → 200 tools
- `inclusionai/ling-3.0-flash-sante:free` → 200 tools
- `inclusionai/ling-3.0-flash-vl:free` → 200 tools
- `liquid/lfm-2.5-2.6b:free` → 200 tools

## OpenCode Zen ids containing free

- host: `opencode.ai` HTTP 200 count **7**

- `jev-1.13-free`
- `ling-3.0-flash-fin-free`
- `mimo-v2.5-free`
- `muse-spark-1.2-contributor-free`
- `muse-spark-1.3-contributor-free`
- `nemotron-3-ultra-free`
- `nemotron-3.5-lightning-free`

## Zen free tool ping

- `jev-1.13-free` → 403 error code: 1010 
- `ling-3.0-flash-fin-free` → 403 error code: 1010 
- `mimo-v2.5-free` → 403 error code: 1010 
- `muse-spark-1.2-contributor-free` → 403 error code: 1010 
- `muse-spark-1.3-contributor-free` → 403 error code: 1010 
- `nemotron-3-ultra-free` → 403 error code: 1010 
- `nemotron-3.5-lightning-free` → 403 error code: 1010 

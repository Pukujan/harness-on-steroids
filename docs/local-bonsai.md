# Local Bonsai inference path

The harness can use a locally served OpenAI-compatible model as its execution
backend while Jev remains the state, bead, and mini-task routing controller.
The recommended model for the current experiment is Prism ML’s Ternary Bonsai
2 27B GGUF. The model card describes Metal support, a 262K context window, a
separate vision pack, and PTQ1_0/PQ2_0 ternary packings. Use Prism’s patched
llama.cpp fork; stock llama.cpp does not support these formats correctly.

On the MacBook Pro, clone Prism’s demo repository and run its setup script with
the optional web UI and code interpreter disabled. The current working host is
`teresas-macbook-pro` at Tailscale address `100.79.248.88`. Download the
smaller PTQ1_0 file and the Q8 vision projector, then serve them with the
repository’s patched binary:

```bash
git clone https://github.com/PrismML-Eng/Bonsai-demo ~/Bonsai-demo
cd ~/Bonsai-demo
BONSAI_SKIP_GGUF=1 BONSAI_SKIP_MLX=1 BONSAI_OPENWEBUI=0 \
  BONSAI_CODE_INTERPRETER=0 ./setup.sh
.venv/bin/hf download prism-ml/Ternary-Bonsai-2-27B-gguf \
  Ternary-Bonsai-2-27B-PTQ1_0.gguf \
  Ternary-Bonsai-2-27B-mmproj-Q8_0.gguf \
  --local-dir models/bonsai2-gguf/27B
BONSAI_HOST=100.79.248.88 PORT=8080 \
  BONSAI_GGUF=models/bonsai2-gguf/27B/Ternary-Bonsai-2-27B-PTQ1_0.gguf \
  BONSAI_MMPROJ=models/bonsai2-gguf/27B/Ternary-Bonsai-2-27B-mmproj-Q8_0.gguf \
  BONSAI_FAMILY=bonsai2 BONSAI_MODEL=27B BONSAI_CTX=16384 \
  ./scripts/start_llama_server.sh -np 1
```

The exact binary flags should follow the model card and the current Prism demo
repository. Expose the service only on the Tailscale
interface, then set these ignored local variables in the Windows worktree:

```text
LOCAL_MODEL_BASE_URL=http://100.79.248.88:8080/v1
LOCAL_MODEL_ID=/Users/teresaguajardo/Bonsai-demo/models/bonsai2-gguf/27B/Ternary-Bonsai-2-27B-PTQ1_0.gguf
LOCAL_MODEL_API_KEY=none
```

The server advertises the exact model identifier at `/v1/models`; use that
identifier when a CLI requires a model name. A bounded connectivity and chat
smoke test is repeatable from the Windows worktree:

```powershell
python research/probe_local_model.py
```

The adapters use the local endpoint through each CLI’s own model configuration;
they do not send the corpus or prompts to the model host during inventory. Pi
can point directly at the endpoint using its `models.json` provider entry. For
OpenCode and Grok Build, keep the local model configuration in their ignored
user configuration and select it through `OPENCODE_MODEL` or
`GROK_BUILD_MODEL` when the CLI supports that route.

The replay adapter can create an isolated OpenCode provider file inside each
ignored run workspace, which avoids changing the user’s global OpenCode setup:

```powershell
$env:OPENCODE_MODEL = "local-bonsai/bonsai"
python research/run_controller_replay.py --limit 1 --adapters opencode --timeout 180
```

The `local-bonsai/bonsai` name is an adapter alias. The server’s advertised
model identifier remains available through `probe_local_model.py` for direct
OpenAI-compatible clients.

A remote endpoint is not assumed to be ready just because the Mac is online.
The pilot records `unavailable` until `/v1/models` and one bounded chat
completion both succeed.

On the 16 GiB MacBook Pro, the tested stable profile is 16,384 context tokens
with one inference slot. A 32,768-token one-slot launch reached the server
startup path but logged Metal insufficient-memory errors and returned HTTP 500
for a bounded request, so it is not the default. Exact die temperature was not
available through the non-root SSH account; `memory_pressure`, process RSS, and
`pmset -g therm` warning state were available.

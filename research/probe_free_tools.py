"""List OpenRouter/Zen free models that advertise tools. No secrets."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
ENV = ROOT / ".env"
OUT = ROOT / "reports" / "free-models-tools.md"


def load_env() -> dict[str, str]:
    vals: dict[str, str] = {}
    for line in ENV.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, v = s.split("=", 1)
        vals[k.strip()] = v.strip()
    return vals


def host_of(url: str) -> str:
    try:
        return urlparse(url).netloc or "(bad-url)"
    except Exception:
        return "(bad-url)"


def get_json(url: str, key: str | None, timeout: int = 30) -> tuple[int, object]:
    req = urllib.request.Request(url, headers={"User-Agent": "harness-probe"})
    if key:
        req.add_header("Authorization", f"Bearer {key}")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")[:180]
    except Exception as e:
        return 0, type(e).__name__


def post_tools(url: str, key: str, model: str) -> tuple[int, str]:
    body = json.dumps(
        {
            "model": model,
            "messages": [{"role": "user", "content": "Call the ping tool."}],
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": "ping",
                        "description": "Health check",
                        "parameters": {"type": "object", "properties": {}},
                    },
                }
            ],
            "max_tokens": 64,
        }
    ).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Authorization", f"Bearer {key}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
            msg = ((data.get("choices") or [{}])[0].get("message") or {})
            tools = msg.get("tool_calls") or []
            return resp.status, "tools" if tools else "text"
    except urllib.error.HTTPError as e:
        snippet = e.read().decode("utf-8", errors="replace")[:120]
        return e.code, snippet.replace("\n", " ")
    except Exception as e:
        return 0, type(e).__name__


def main() -> None:
    env = load_env()
    lines = [
        "# Free models that advertise tools",
        "",
        "No secrets. OpenRouter rows: price 0 and `tools` in supported_parameters.",
        "",
        "## Tried earlier (do not repeat blindly)",
        "",
        "- `openrouter/z-ai/glm-5.2:free` — 400 no tool endpoints",
        "- `openrouter/qwen/qwen3.8-27b:free` — tools then 429 rate-limit",
        "- `openrouter/google/gemma-4-31b-it:free` — 429",
        "- `opencode/glm-5.3-flash` — fail",
        "- `opencode/deepseek-v4-flash` — **402 insufficient funds**",
        "- `opencode/ling-3.0-flash-fin-free` — timeout/empty",
        "- `yolo-auto/qwen3.8-flash` — tools when it ran",
        "",
    ]
    or_base = (env.get("OPENROUTER_API_URL") or "https://openrouter.ai/api/v1").rstrip("/")
    models_url = or_base if or_base.endswith("/models") else (
        or_base + "/models" if or_base.endswith("/v1") else or_base + "/v1/models"
    )
    st, payload = get_json(models_url, env.get("OPENROUTER_API_KEY"))
    tool_free: list[str] = []
    if st == 200 and isinstance(payload, dict):
        for row in payload.get("data") or []:
            if not isinstance(row, dict):
                continue
            mid = row.get("id")
            if not isinstance(mid, str):
                continue
            pricing = row.get("pricing") if isinstance(row.get("pricing"), dict) else {}
            prompt = str(pricing.get("prompt") or "1")
            completion = str(pricing.get("completion") or "1")
            params = row.get("supported_parameters") or []
            if not isinstance(params, list):
                params = []
            free = mid.endswith(":free") or (prompt in {"0", "0.0"} and completion in {"0", "0.0"})
            if free and "tools" in params:
                tool_free.append(mid)
    tool_free = sorted(set(tool_free))
    lines += [
        "## OpenRouter free + tools advertised",
        "",
        f"- host: `{host_of(or_base)}` HTTP {st} count **{len(tool_free)}**",
        "",
    ]
    for mid in tool_free:
        lines.append(f"- `{mid}`")
    lines.append("")

    chat = or_base if or_base.endswith("/chat/completions") else (
        or_base + "/chat/completions" if or_base.endswith("/v1") else or_base + "/v1/chat/completions"
    )
    lines += ["## OpenRouter tool ping (status only)", ""]
    key = env.get("OPENROUTER_API_KEY") or ""
    for mid in tool_free[:8]:
        code, note = post_tools(chat, key, mid)
        lines.append(f"- `{mid}` → {code} {note[:80]}")
    lines.append("")

    zen = (env.get("OPENCODE_ZEN_API_URL") or "").rstrip("/")
    zkey = env.get("OPENCODE_API_KEY") or ""
    if zen:
        mu = zen if zen.endswith("/models") else (
            zen + "/models" if zen.endswith("/v1") else zen + "/v1/models"
        )
        st, payload = get_json(mu, zkey)
        ids: list[str] = []
        if st == 200 and isinstance(payload, dict):
            data = payload.get("data") or payload.get("models") or []
            if isinstance(data, list):
                for row in data:
                    if isinstance(row, str) and "free" in row.lower():
                        ids.append(row)
                    elif isinstance(row, dict):
                        mid = str(row.get("id") or row.get("name") or "")
                        if "free" in mid.lower():
                            ids.append(mid)
        ids = sorted(set(ids))
        lines += [
            "## OpenCode Zen ids containing free",
            "",
            f"- host: `{host_of(zen)}` HTTP {st} count **{len(ids)}**",
            "",
        ]
        for mid in ids:
            lines.append(f"- `{mid}`")
        lines.append("")
        zchat = zen if zen.endswith("/chat/completions") else (
            zen + "/chat/completions" if zen.endswith("/v1") else zen + "/v1/chat/completions"
        )
        lines += ["## Zen free tool ping", ""]
        for mid in ids[:8]:
            code, note = post_tools(zchat, zkey, mid)
            lines.append(f"- `{mid}` → {code} {note[:80]}")
        lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} openrouter_tool_free={len(tool_free)}")


if __name__ == "__main__":
    main()

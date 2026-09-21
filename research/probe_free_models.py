"""Probe OpenRouter / Zen / OpenCode keys without printing secrets."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
ENV = ROOT / ".env"
OUT = ROOT / "reports" / "free-models.md"


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
        p = urlparse(url)
        return p.netloc or "(bad-url)"
    except Exception:
        return "(bad-url)"


def get_json(url: str, key: str | None, timeout: int = 25) -> tuple[int, object]:
    req = urllib.request.Request(url, headers={"User-Agent": "harness-on-steroids-probe"})
    if key:
        req.add_header("Authorization", f"Bearer {key}")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return resp.status, json.loads(body)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")[:200]
    except Exception as e:
        return 0, type(e).__name__


def or_free(payload: object) -> list[str]:
    data = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(data, list):
        return []
    ids: list[str] = []
    for row in data:
        if not isinstance(row, dict):
            continue
        mid = row.get("id")
        if not isinstance(mid, str):
            continue
        pricing = row.get("pricing") if isinstance(row.get("pricing"), dict) else {}
        prompt = str(pricing.get("prompt") or "1")
        completion = str(pricing.get("completion") or "1")
        free = mid.endswith(":free") or (prompt in {"0", "0.0"} and completion in {"0", "0.0"})
        if free:
            ids.append(mid)
    return sorted(set(ids))


def ids_from(payload: object) -> list[str]:
    if isinstance(payload, dict):
        data = payload.get("data") or payload.get("models") or payload.get("id")
        if isinstance(data, list):
            out = []
            for row in data:
                if isinstance(row, str):
                    out.append(row)
                elif isinstance(row, dict):
                    mid = row.get("id") or row.get("name")
                    if isinstance(mid, str):
                        out.append(mid)
            return sorted(set(out))[:80]
    if isinstance(payload, list):
        return [str(x)[:80] for x in payload[:80]]
    return []


def main() -> None:
    env = load_env()
    lines = [
        "# Free / cheap models probe",
        "",
        "No secrets. Hosts and model ids only. `.env` is gitignored.",
        "",
    ]
    or_url = (env.get("OPENROUTER_API_URL") or "https://openrouter.ai/api/v1").rstrip("/")
    if not or_url.endswith("/models"):
        models_url = or_url + "/models" if or_url.endswith("/v1") else or_url.rstrip("/") + "/v1/models"
    else:
        models_url = or_url
    st, payload = get_json(models_url, env.get("OPENROUTER_API_KEY"))
    free = or_free(payload) if st == 200 else []
    lines += [
        "## OpenRouter",
        "",
        f"- host: `{host_of(or_url)}`",
        f"- models HTTP: **{st}**",
        f"- default env model: `{env.get('OPENROUTER_MODEL', '')}`",
        f"- free ids: **{len(free)}**",
        "",
    ]
    for mid in free[:40]:
        lines.append(f"- `{mid}`")
    if len(free) > 40:
        lines.append(f"- … {len(free) - 40} more")
    lines.append("")

    for label, url_key, key_key in (
        ("OpenCode", "OPENCODE_API_URL", "OPENCODE_API_KEY"),
        ("OpenCode2", "OPENCODE2_API_URL", "OPENCODE2_API_KEY"),
        ("OpenCode Zen", "OPENCODE_ZEN_API_URL", "OPENCODE_API_KEY"),
        ("OpenCode Zen2", "OPENCODE_ZEN2_API_URL", "OPENCODE_API_KEY"),
    ):
        url = (env.get(url_key) or "").rstrip("/")
        if not url:
            lines += [f"## {label}", "", "- url missing", ""]
            continue
        mu = url if url.endswith("/models") else url + ("/models" if url.endswith("/v1") else "/v1/models")
        st, payload = get_json(mu, env.get(key_key))
        ids = ids_from(payload) if st == 200 else []
        lines += [
            f"## {label}",
            "",
            f"- host: `{host_of(url)}`",
            f"- models HTTP: **{st}**",
            f"- ids listed: **{len(ids)}**",
            "",
        ]
        for mid in ids[:25]:
            lines.append(f"- `{mid}`")
        if st != 200:
            lines.append(f"- error class/snippet: `{str(payload)[:120]}`")
        lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} openrouter_free={len(free)}")


if __name__ == "__main__":
    main()

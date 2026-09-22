#!/usr/bin/env python3
"""Probe an OpenAI-compatible local model without retaining its response text."""

from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from typing import Any


def _request(
    url: str,
    *,
    method: str = "GET",
    body: dict[str, Any] | None = None,
    timeout: float,
) -> Any:
    data = None
    headers = {"Accept": "application/json"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default=os.environ.get("LOCAL_MODEL_BASE_URL", "http://127.0.0.1:8080/v1"))
    parser.add_argument("--model", default=os.environ.get("LOCAL_MODEL_ID", ""))
    parser.add_argument("--timeout", type=float, default=180.0)
    args = parser.parse_args()
    base_url = args.base_url.rstrip("/")

    try:
        models = _request(f"{base_url}/models", timeout=args.timeout)
        model_ids = [row.get("id") for row in models.get("data", []) if isinstance(row, dict)]
        model = args.model or (model_ids[0] if model_ids else "")
        if not model:
            raise RuntimeError("/models returned no model id")
        result = _request(
            f"{base_url}/chat/completions",
            method="POST",
            body={
                "model": model,
                "messages": [{"role": "user", "content": "Reply with exactly OK."}],
                "max_tokens": 8,
                "temperature": 0,
                "stream": False,
            },
            timeout=args.timeout,
        )
        choice = (result.get("choices") or [{}])[0]
        usage = result.get("usage") or {}
        print(
            json.dumps(
                {
                    "status": "ok",
                    "model": result.get("model", model),
                    "available_models": model_ids,
                    "finish_reason": choice.get("finish_reason"),
                    "prompt_tokens": usage.get("prompt_tokens"),
                    "completion_tokens": usage.get("completion_tokens"),
                    "response_chars": len(str((choice.get("message") or {}).get("content", ""))),
                },
                sort_keys=True,
            )
        )
        return 0
    except (OSError, RuntimeError, ValueError, urllib.error.HTTPError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

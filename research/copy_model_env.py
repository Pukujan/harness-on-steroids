"""Copy model-provider keys into gitignored .env. Never print secrets."""

from __future__ import annotations

from pathlib import Path

SRC = Path(r"C:\Users\pujan\OneDrive\Desktop\configs\.env")
DST = Path(__file__).resolve().parents[1] / ".env"
WANT = [
    "OPENROUTER_API_URL",
    "OPENROUTER_API_KEY",
    "OPENROUTER_MODEL",
    "OPENCODE_API_URL",
    "OPENCODE_API_KEY",
    "OPENCODE_MODEL",
    "OPENCODE2_API_URL",
    "OPENCODE2_API_KEY",
    "OPENCODE2_MODEL",
    "OPENCODE_ZEN_API_URL",
    "OPENCODE_ZEN_MODEL",
    "OPENCODE_ZEN2_API_URL",
    "OPENCODE_ZEN2_MODEL",
    "QWEN_API_URL",
    "QWEN_API_KEY",
    "QWEN_MODEL",
    "GLM_API_URL",
    "GLM_API_KEY",
    "GLM_MODEL",
    "NINEROUTER_API_URL",
    "NINEROUTER_API_KEY",
]


def main() -> None:
    vals: dict[str, str] = {}
    for line in SRC.read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        key, raw = s.split("=", 1)
        key = key.strip()
        if key not in WANT:
            continue
        val = raw.strip().strip('"').strip("'")
        if val:
            vals[key] = val
    lines = ["# Subset from OneDrive Desktop configs/.env — gitignored", ""]
    got = [k for k in WANT if k in vals]
    missing = [k in WANT and k not in vals for k in WANT]
    for key in got:
        lines.append(f"{key}={vals[key]}")
    DST.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wrote", DST.name, "keys", len(got))
    print("present", ",".join(got))
    print("missing", ",".join(k for k in WANT if k not in vals) or "none")
    for name in ("OPENROUTER_API_KEY", "OPENCODE_API_KEY", "QWEN_API_KEY", "NINEROUTER_API_KEY"):
        print(f"{name}_len", len(vals.get(name, "")))
    print("zen_url", "yes" if vals.get("OPENCODE_ZEN_API_URL") else "no")


if __name__ == "__main__":
    main()

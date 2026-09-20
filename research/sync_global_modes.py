#!/usr/bin/env python3
"""Copy project Codex-imitate modes into this machine's Kilo/OpenCode agent dirs."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = Path(os.environ.get("USERPROFILE") or os.environ.get("HOME") or "")


def main() -> None:
    pairs = [
        (ROOT / ".kilo" / "agent" / "codex.md", HOME / ".config" / "kilo" / "agent" / "codex.md"),
        (ROOT / ".opencode" / "agent" / "codex.md", HOME / ".config" / "opencode" / "agent" / "codex.md"),
    ]
    for src, dst in pairs:
        if not src.is_file():
            raise SystemExit(f"missing {src}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"synced {dst}")


if __name__ == "__main__":
    main()

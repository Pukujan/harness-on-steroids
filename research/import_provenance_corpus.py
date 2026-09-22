#!/usr/bin/env python3
"""Hash and summarize a local ChatGPT export without retaining message bodies.

The source corpus stays outside Git. The generated manifest contains file hashes,
sizes, and structural counts only. The report is suitable for deriving a newer
gold-behavior ontology without copying conversation text into the repository.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterator


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _iter_json_values(path: Path) -> Iterator[Any]:
    if path.suffix.lower() == ".jsonl":
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.strip():
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    yield None
        return
    try:
        yield json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except json.JSONDecodeError:
        yield None


def _walk(value: Any, *, depth: int = 0) -> Iterator[tuple[str, Any, int]]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield key, child, depth
            yield from _walk(child, depth=depth + 1)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child, depth=depth + 1)


_CATEGORICAL_KEYS = {
    "content_type",
    "default_model_slug",
    "message_type",
    "model_slug",
    "recipient",
    "resolved_model_slug",
    "status",
    "thinking_effort",
}


def _analyze_file(
    path: Path,
) -> tuple[dict[str, Any], Counter[str], Counter[str], Counter[str], dict[str, Counter[str]]]:
    keys: Counter[str] = Counter()
    roles: Counter[str] = Counter()
    content_types: Counter[str] = Counter()
    categorical: dict[str, Counter[str]] = {
        key: Counter() for key in sorted(_CATEGORICAL_KEYS)
    }
    roots: Counter[str] = Counter()
    records = 0
    parse_errors = 0
    for value in _iter_json_values(path):
        records += 1
        if value is None:
            parse_errors += 1
            roots["invalid"] += 1
            continue
        roots[type(value).__name__] += 1
        for key, child, _depth in _walk(value):
            keys[key] += 1
            if key == "role" and isinstance(child, str):
                roles[child] += 1
            if key == "type" and isinstance(child, str) and child in {
                "message",
                "tool_call",
                "tool_result",
                "function",
                "compacted",
                "reasoning",
            }:
                content_types[child] += 1
            if key in categorical and isinstance(child, str) and len(child) <= 200:
                categorical[key][child] += 1
    meta = {
        "sha256": _sha256(path),
        "bytes": path.stat().st_size,
        "suffix": path.suffix.lower(),
        "records": records,
        "parse_errors": parse_errors,
        "root_types": dict(sorted(roots.items())),
    }
    return meta, keys, roles, content_types, categorical


def build_inventory(source: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    files = sorted(path for path in source.rglob("*") if path.is_file())
    key_counts: Counter[str] = Counter()
    role_counts: Counter[str] = Counter()
    type_counts: Counter[str] = Counter()
    categorical_counts: dict[str, Counter[str]] = {
        key: Counter() for key in sorted(_CATEGORICAL_KEYS)
    }
    suffix_counts: Counter[str] = Counter()
    roots: Counter[str] = Counter()
    manifest: list[dict[str, Any]] = []
    parse_errors = 0
    for path in files:
        meta, keys, roles, content_types, categorical = _analyze_file(path)
        manifest.append(meta)
        suffix_counts[meta["suffix"]] += 1
        key_counts.update(keys)
        role_counts.update(roles)
        type_counts.update(content_types)
        for key, values in categorical.items():
            categorical_counts[key].update(values)
        roots.update(meta["root_types"])
        parse_errors += int(meta["parse_errors"])
    return (
        {
            "source_label": "chatgpt-provenance-account",
            "source_file_count": len(files),
            "source_bytes": sum(int(row["bytes"]) for row in manifest),
            "suffix_counts": dict(sorted(suffix_counts.items())),
            "root_type_counts": dict(sorted(roots.items())),
            "top_keys": dict(key_counts.most_common(40)),
            "role_counts": dict(sorted(role_counts.items())),
            "event_type_counts": dict(sorted(type_counts.items())),
            "categorical_value_counts": {
                key: dict(values.most_common(40))
                for key, values in categorical_counts.items()
                if values
            },
            "parse_error_records": parse_errors,
            "privacy": "No message bodies, titles, paths, or raw JSON are retained.",
        },
        manifest,
    )


def write_outputs(source: Path, output_dir: Path, report_path: Path) -> dict[str, Any]:
    summary, manifest = build_inventory(source)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "source-manifest.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in manifest), encoding="utf-8"
    )
    (output_dir / "inventory.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    report_lines = [
        "# Imported provenance corpus inventory",
        "",
        "This report is structure-only. The source export remains outside Git; the ignored "
        "manifest stores hashes and file sizes before parsing.",
        "",
        f"- Files: **{summary['source_file_count']}**",
        f"- Bytes: **{summary['source_bytes']}**",
        f"- Parse-error records: **{summary['parse_error_records']}**",
        f"- File types: `{json.dumps(summary['suffix_counts'], sort_keys=True)}`",
        f"- Roles: `{json.dumps(summary['role_counts'], sort_keys=True)}`",
        f"- Event-like types: `{json.dumps(summary['event_type_counts'], sort_keys=True)}`",
        "- Categorical fields: "
        f"`{json.dumps(summary['categorical_value_counts'], sort_keys=True)}`",
        "",
        "## Use in the harness",
        "",
        "The corpus is a newer provenance source for ontology and long-horizon task "
        "calibration. It is kept separate from the existing local Work gold until origin, "
        "export shape, and matched-task eligibility are verified. Derived samples must carry "
        "a source hash and must not include message bodies.",
        "",
    ]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("data/provenance"))
    parser.add_argument(
        "--report", type=Path, default=Path("reports/provenance-corpus-inventory.md")
    )
    args = parser.parse_args()
    summary = write_outputs(args.source, args.output_dir, args.report)
    print(
        json.dumps(
            {
                "files": summary["source_file_count"],
                "bytes": summary["source_bytes"],
                "parse_error_records": summary["parse_error_records"],
                "report": str(args.report),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

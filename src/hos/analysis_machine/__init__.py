"""Small, repeatable transcript-analysis machine.

The package deliberately owns only normalization, deterministic lane summaries,
and export.  Raw transcript bodies remain outside the package's outputs.
"""

from .analyze import ANALYZER_VERSION, analyze_events, analyze_stream, export_bundle, export_stream
from .model import (
    CODEBOOK_VERSION,
    CONTRACT_VERSION,
    ONTOLOGY_VERSION,
    CanonicalEvent,
    ValidationIssue,
)
from .normalize import iter_normalized_jsonl, iter_normalized_paths, normalize_jsonl
from .validate import validate_event

__all__ = [
    "ANALYZER_VERSION",
    "CODEBOOK_VERSION",
    "CONTRACT_VERSION",
    "ONTOLOGY_VERSION",
    "CanonicalEvent",
    "ValidationIssue",
    "analyze_events",
    "analyze_stream",
    "export_bundle",
    "export_stream",
    "normalize_jsonl",
    "iter_normalized_jsonl",
    "iter_normalized_paths",
    "validate_event",
]

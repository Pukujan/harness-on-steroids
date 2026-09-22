"""Small, repeatable transcript-analysis machine.

The package deliberately owns only normalization, deterministic lane summaries,
and export.  Raw transcript bodies remain outside the package's outputs.
"""

from .analyze import ANALYZER_VERSION, analyze_events, export_bundle
from .model import CONTRACT_VERSION, ONTOLOGY_VERSION, CanonicalEvent, ValidationIssue
from .normalize import normalize_jsonl
from .validate import validate_event

__all__ = [
    "ANALYZER_VERSION",
    "CONTRACT_VERSION",
    "ONTOLOGY_VERSION",
    "CanonicalEvent",
    "ValidationIssue",
    "analyze_events",
    "export_bundle",
    "normalize_jsonl",
    "validate_event",
]

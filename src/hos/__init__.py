"""Managed library facade. Import paths under src.* stay until issue 18 moves them."""

from src.goal_loop import GoalEngine
from src.hos.analysis_machine import CanonicalEvent, analyze_events, export_bundle, normalize_jsonl
from src.hos.controller import (
    ControllerAction,
    ControllerDecision,
    ControllerPhase,
    ControllerState,
    JevController,
)
from src.owner_invariants import all_failures, load_spec
from src.score_session import score_seq
from src.sol_bridge import SolBridge, SolConfig, SolResult, run_task

__all__ = [
    "GoalEngine",
    "CanonicalEvent",
    "ControllerAction",
    "ControllerDecision",
    "ControllerPhase",
    "ControllerState",
    "JevController",
    "SolBridge",
    "SolConfig",
    "SolResult",
    "all_failures",
    "analyze_events",
    "export_bundle",
    "load_spec",
    "normalize_jsonl",
    "run_task",
    "score_seq",
]

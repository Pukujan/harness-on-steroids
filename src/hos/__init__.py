"""Managed library facade. Import paths under src.* stay until issue 18 moves them."""

from src.goal_loop import GoalEngine
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
    "ControllerAction",
    "ControllerDecision",
    "ControllerPhase",
    "ControllerState",
    "JevController",
    "SolBridge",
    "SolConfig",
    "SolResult",
    "all_failures",
    "load_spec",
    "run_task",
    "score_seq",
]

"""Core package for chaotic billiards simulations."""

from .types import BallState, CollisionEvent, RunResult, SimulationConfig

__all__ = [
    "BallState",
    "CollisionEvent",
    "RunResult",
    "SimulationConfig",
]

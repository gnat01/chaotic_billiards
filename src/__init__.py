"""Core package namespace for the first chaotic billiards slice."""

from model import BallState, CollisionEvent, RunResult, SimulationConfig

__all__ = [
    "BallState",
    "CollisionEvent",
    "RunResult",
    "SimulationConfig",
]

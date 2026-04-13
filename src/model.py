from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

Vec2 = tuple[float, float]


@dataclass(frozen=True)
class BallState:
    """Translational state for a finite-radius billiard ball."""

    position: Vec2
    velocity: Vec2
    radius: float
    time: float = 0.0
    collision_count: int = 0
    active: bool = True


@dataclass(frozen=True)
class CollisionEvent:
    """Next ball-boundary contact for the ball center trajectory."""

    time_to_contact: float
    center_at_contact: Vec2
    contact_point: Vec2
    normal: Vec2
    boundary_label: str | None = None


@dataclass(frozen=True)
class SimulationConfig:
    max_time: float = 10.0
    max_collisions: int = 100
    min_speed: float = 1e-9
    epsilon: float = 1e-9
    reflection_mode: Literal["elastic", "inelastic"] = "elastic"
    restitution: float = 1.0


@dataclass(frozen=True)
class RunResult:
    states: list[BallState] = field(default_factory=list)
    collisions: list[CollisionEvent] = field(default_factory=list)
    termination_reason: Literal[
        "max_time",
        "max_collisions",
        "min_speed",
        "no_collision",
        "invalid_event",
    ] = "no_collision"

    @property
    def final_state(self) -> BallState:
        return self.states[-1]

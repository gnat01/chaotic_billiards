from __future__ import annotations

from model import BallState, SimulationConfig


def speed(velocity: tuple[float, float]) -> float:
    return ((velocity[0] ** 2) + (velocity[1] ** 2)) ** 0.5


def should_stop(state: BallState, config: SimulationConfig) -> str | None:
    if speed(state.velocity) <= config.min_speed:
        return "min_speed"
    if state.collision_count >= config.max_collisions:
        return "max_collisions"
    if state.time >= config.max_time:
        return "max_time"
    return None

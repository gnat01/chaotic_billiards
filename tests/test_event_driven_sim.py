from __future__ import annotations

import math

from engine import run_simulation
from geometry import Geometry
from model import BallState, CollisionEvent, SimulationConfig


class OneDimensionalCorridor(Geometry):
    """Simple vertical-wall corridor used only to validate the event loop."""

    def __init__(self, left: float, right: float) -> None:
        self.left = left
        self.right = right

    @property
    def name(self) -> str:
        return "one_dimensional_corridor"

    def contains_ball(self, center: tuple[float, float], radius: float) -> bool:
        return (self.left + radius) <= center[0] <= (self.right - radius)

    def first_contact(
        self,
        center: tuple[float, float],
        velocity: tuple[float, float],
        radius: float,
        epsilon: float = 1e-9,
    ) -> CollisionEvent | None:
        vx, vy = velocity
        if abs(vx) <= epsilon:
            return None

        if vx > 0.0:
            wall_x = self.right
            center_x = wall_x - radius
            dt = (center_x - center[0]) / vx
            normal = (-1.0, 0.0)
        else:
            wall_x = self.left
            center_x = wall_x + radius
            dt = (center_x - center[0]) / vx
            normal = (1.0, 0.0)

        if dt <= epsilon:
            return None

        center_at_contact = (center_x, center[1] + (vy * dt))
        contact_point = (wall_x, center_at_contact[1])
        return CollisionEvent(
            time_to_contact=dt,
            center_at_contact=center_at_contact,
            contact_point=contact_point,
            normal=normal,
            boundary_label="vertical_wall",
        )


def test_event_driven_engine_reflects_between_vertical_walls() -> None:
    geometry = OneDimensionalCorridor(left=0.0, right=10.0)
    initial_state = BallState(position=(5.0, 0.0), velocity=(2.0, 0.5), radius=1.0)
    config = SimulationConfig(max_time=8.0, max_collisions=10)

    result = run_simulation(initial_state=initial_state, geometry=geometry, config=config)

    assert result.termination_reason == "max_time"
    assert len(result.collisions) == 2
    assert result.final_state.collision_count == 2
    assert result.states[1].position == (9.0, 1.0)
    assert result.states[1].velocity == (-2.0, 0.5)
    assert result.states[2].position == (1.0, 3.0)
    assert result.states[2].velocity == (2.0, 0.5)
    assert result.final_state.position == (5.0, 4.0)


def test_event_driven_engine_rejects_invalid_initial_state() -> None:
    geometry = OneDimensionalCorridor(left=0.0, right=10.0)
    initial_state = BallState(position=(0.5, 0.0), velocity=(1.0, 0.0), radius=1.0)

    try:
        run_simulation(initial_state=initial_state, geometry=geometry)
    except ValueError as exc:
        assert "not valid" in str(exc)
    else:
        raise AssertionError("Expected invalid initial state to raise ValueError")


def test_event_driven_engine_preserves_speed_under_specular_reflection() -> None:
    geometry = OneDimensionalCorridor(left=0.0, right=10.0)
    initial_state = BallState(position=(5.0, 1.0), velocity=(3.0, 4.0), radius=1.0)
    result = run_simulation(
        initial_state=initial_state,
        geometry=geometry,
        config=SimulationConfig(max_time=2.0, max_collisions=1),
    )

    initial_speed = math.hypot(*initial_state.velocity)
    reflected_speed = math.hypot(*result.final_state.velocity)
    assert math.isclose(initial_speed, reflected_speed)

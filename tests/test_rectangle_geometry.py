from __future__ import annotations

import math

from engine import run_simulation
from geometry import Rectangle, Square
from model import BallState, SimulationConfig


def test_rectangle_contains_ball_uses_ball_radius() -> None:
    geometry = Rectangle(width=10.0, height=6.0)

    assert geometry.contains_ball((1.0, 1.0), radius=1.0)
    assert not geometry.contains_ball((0.99, 1.0), radius=1.0)
    assert not geometry.contains_ball((9.01, 2.0), radius=1.0)
    assert not geometry.contains_ball((4.0, 5.1), radius=1.0)


def test_rectangle_first_contact_hits_right_wall_exactly() -> None:
    geometry = Rectangle(width=10.0, height=6.0)

    event = geometry.first_contact(center=(2.0, 2.0), velocity=(2.0, 0.5), radius=1.0)

    assert event is not None
    assert math.isclose(event.time_to_contact, 3.5)
    assert event.center_at_contact == (9.0, 3.75)
    assert event.contact_point == (10.0, 3.75)
    assert event.normal == (-1.0, 0.0)
    assert event.boundary_label == "right_wall"


def test_rectangle_first_contact_picks_earliest_wall() -> None:
    geometry = Rectangle(width=10.0, height=6.0)

    event = geometry.first_contact(center=(5.0, 2.0), velocity=(1.0, 2.0), radius=1.0)

    assert event is not None
    assert math.isclose(event.time_to_contact, 1.5)
    assert event.center_at_contact == (6.5, 5.0)
    assert event.contact_point == (6.5, 6.0)
    assert event.normal == (0.0, -1.0)
    assert event.boundary_label == "top_wall"


def test_square_runs_inside_event_driven_engine() -> None:
    geometry = Square(side_length=10.0)
    initial_state = BallState(position=(5.0, 5.0), velocity=(2.0, 1.0), radius=1.0)
    result = run_simulation(
        initial_state=initial_state,
        geometry=geometry,
        config=SimulationConfig(max_time=4.0, max_collisions=10),
    )

    assert result.termination_reason == "max_time"
    assert len(result.collisions) == 2
    assert result.collisions[0].boundary_label == "right_wall"
    assert result.collisions[1].boundary_label == "top_wall"
    assert result.states[1].position == (9.0, 7.0)
    assert result.states[1].velocity == (-2.0, 1.0)
    assert result.final_state.position == (5.0, 9.0)
    assert result.final_state.velocity == (-2.0, -1.0)

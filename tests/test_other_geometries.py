from __future__ import annotations

import math

from engine import run_simulation
from geometry import CircleTable, SinaiTable, StadiumTable, Triangle, build_geometry
from model import BallState, SimulationConfig


def test_circle_contains_ball_and_hits_circular_wall() -> None:
    geometry = CircleTable(radius=5.0, center=(5.0, 5.0))

    assert geometry.contains_ball((5.0, 5.0), radius=0.5)
    assert not geometry.contains_ball((9.8, 5.0), radius=0.5)

    event = geometry.first_contact(center=(5.0, 5.0), velocity=(2.0, 0.0), radius=1.0)

    assert event is not None
    assert math.isclose(event.time_to_contact, 2.0)
    assert event.center_at_contact == (9.0, 5.0)
    assert event.contact_point == (10.0, 5.0)
    assert event.normal == (-1.0, 0.0)
    assert event.boundary_label == "circular_wall"


def test_triangle_contains_ball_and_hits_base() -> None:
    geometry = Triangle(width=10.0, height=8.0)

    assert geometry.contains_ball((5.0, 2.0), radius=0.5)
    assert not geometry.contains_ball((1.0, 7.5), radius=0.5)

    event = geometry.first_contact(center=(5.0, 3.0), velocity=(0.0, -2.0), radius=0.5)

    assert event is not None
    assert math.isclose(event.time_to_contact, 1.25)
    assert event.center_at_contact == (5.0, 0.5)
    assert event.contact_point == (5.0, 0.0)
    assert event.normal == (0.0, 1.0)
    assert event.boundary_label == "base"


def test_triangle_symmetry_axis_apex_hit_reflects_off_both_slopes() -> None:
    geometry = Triangle(width=10.0, height=8.0)
    initial_state = BallState(position=(5.0, 2.0), velocity=(0.0, 2.5), radius=0.25)

    result = run_simulation(
        initial_state=initial_state,
        geometry=geometry,
        config=SimulationConfig(max_time=6.0, max_collisions=4),
    )

    assert result.collisions
    first_collision = result.collisions[0]
    assert first_collision.boundary_label == "left_slope+right_slope"
    assert math.isclose(first_collision.center_at_contact[0], 5.0)
    assert math.isclose(first_collision.center_at_contact[1], 7.52830094339717, rel_tol=1e-9)
    assert math.isclose(result.states[1].velocity[0], 0.0, abs_tol=1e-9)
    assert result.states[1].velocity[1] < 0.0
    assert geometry.contains_ball(result.final_state.position, initial_state.radius)


def test_sinai_excludes_obstacle_and_detects_obstacle_contact() -> None:
    geometry = SinaiTable(width=10.0, height=6.0, obstacle_radius=1.0, obstacle_center=(5.0, 3.0))

    assert geometry.contains_ball((2.0, 2.0), radius=0.4)
    assert not geometry.contains_ball((5.0, 3.0), radius=0.4)

    event = geometry.first_contact(center=(2.0, 3.0), velocity=(1.0, 0.0), radius=0.5)

    assert event is not None
    assert math.isclose(event.time_to_contact, 1.5)
    assert event.center_at_contact == (3.5, 3.0)
    assert event.contact_point == (4.0, 3.0)
    assert event.normal == (-1.0, 0.0)
    assert event.boundary_label == "obstacle"


def test_circle_runs_inside_event_driven_engine() -> None:
    geometry = build_geometry("circle", circle_radius=5.0)
    initial_state = BallState(position=(5.0, 5.0), velocity=(2.0, 0.0), radius=1.0)

    result = run_simulation(
        initial_state=initial_state,
        geometry=geometry,
        config=SimulationConfig(max_time=5.0, max_collisions=4),
    )

    assert result.collisions
    assert result.collisions[0].boundary_label == "circular_wall"


def test_stadium_contains_ball_and_hits_right_cap() -> None:
    geometry = StadiumTable(width=12.0, height=6.0)

    assert geometry.contains_ball((6.0, 3.0), radius=0.5)
    assert not geometry.contains_ball((0.4, 3.0), radius=0.5)

    event = geometry.first_contact(center=(6.0, 3.0), velocity=(2.0, 0.0), radius=1.0)

    assert event is not None
    assert math.isclose(event.time_to_contact, 2.5)
    assert event.center_at_contact == (11.0, 3.0)
    assert event.contact_point == (12.0, 3.0)
    assert event.normal == (-1.0, 0.0)
    assert event.boundary_label == "right_cap"


def test_stadium_runs_inside_event_driven_engine() -> None:
    geometry = build_geometry("stadium", width=12.0, height=6.0)
    initial_state = BallState(position=(6.0, 3.0), velocity=(2.0, 1.0), radius=0.5)

    result = run_simulation(
        initial_state=initial_state,
        geometry=geometry,
        config=SimulationConfig(max_time=6.0, max_collisions=6),
    )

    assert result.collisions
    assert result.collisions[0].boundary_label in {"top_wall", "right_cap"}

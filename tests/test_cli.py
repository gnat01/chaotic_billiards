from __future__ import annotations

import math

from cli import resolve_velocity


def test_resolve_velocity_uses_cartesian_components_when_no_angle() -> None:
    assert resolve_velocity(3.0, 4.0, None, None) == (3.0, 4.0)


def test_resolve_velocity_uses_angle_and_explicit_speed() -> None:
    vx, vy = resolve_velocity(0.0, 0.0, 90.0, 5.0)

    assert math.isclose(vx, 0.0, abs_tol=1e-9)
    assert math.isclose(vy, 5.0, abs_tol=1e-9)


def test_resolve_velocity_uses_angle_and_infers_speed_from_vx_vy() -> None:
    vx, vy = resolve_velocity(3.0, 4.0, 180.0, None)

    assert math.isclose(vx, -5.0, abs_tol=1e-9)
    assert math.isclose(vy, 0.0, abs_tol=1e-9)


def test_resolve_velocity_rejects_out_of_range_angle() -> None:
    try:
        resolve_velocity(1.0, 0.0, 360.0, 1.0)
    except ValueError as exc:
        assert "between 0 and 359" in str(exc)
    else:
        raise AssertionError("Expected out-of-range angle to raise ValueError")

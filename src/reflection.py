from __future__ import annotations

from model import Vec2


def dot(a: Vec2, b: Vec2) -> float:
    return (a[0] * b[0]) + (a[1] * b[1])


def norm(a: Vec2) -> float:
    return dot(a, a) ** 0.5


def normalize(a: Vec2) -> Vec2:
    magnitude = norm(a)
    if magnitude == 0.0:
        raise ValueError("Cannot normalize a zero vector")
    return (a[0] / magnitude, a[1] / magnitude)


def reflect_specular(velocity: Vec2, normal: Vec2) -> Vec2:
    """Reflect a translational velocity across a wall normal."""

    unit_normal = normalize(normal)
    normal_component = dot(velocity, unit_normal)
    return (
        velocity[0] - (2.0 * normal_component * unit_normal[0]),
        velocity[1] - (2.0 * normal_component * unit_normal[1]),
    )

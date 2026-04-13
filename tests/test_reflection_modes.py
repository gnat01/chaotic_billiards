from __future__ import annotations

import math

from reflection import reflect_inelastic, reflect_specular


def test_inelastic_reflection_reduces_normal_component_only() -> None:
    velocity = (3.0, -4.0)
    normal = (0.0, 1.0)

    reflected = reflect_inelastic(velocity, normal, restitution=0.5)

    assert reflected == (3.0, 2.0)


def test_elastic_and_inelastic_match_at_restitution_one() -> None:
    velocity = (2.0, -5.0)
    normal = (0.0, 1.0)

    elastic = reflect_specular(velocity, normal)
    inelastic = reflect_inelastic(velocity, normal, restitution=1.0)

    assert elastic == inelastic


def test_inelastic_reflection_reduces_speed() -> None:
    velocity = (1.0, -3.0)
    normal = (0.0, 1.0)

    reflected = reflect_inelastic(velocity, normal, restitution=0.25)

    assert math.hypot(*reflected) < math.hypot(*velocity)

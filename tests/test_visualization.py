from __future__ import annotations

from geometry import Rectangle
from model import BallState, RunResult
from visualization import sample_run


def test_sample_run_interpolates_positions_between_event_states() -> None:
    result = RunResult(
        states=[
            BallState(position=(1.0, 1.0), velocity=(2.0, 0.0), radius=0.5, time=0.0),
            BallState(position=(3.0, 1.0), velocity=(-2.0, 0.0), radius=0.5, time=1.0, collision_count=1),
            BallState(position=(1.0, 1.0), velocity=(-2.0, 0.0), radius=0.5, time=2.0, collision_count=1),
        ],
        collisions=[],
        termination_reason="max_time",
    )

    sampled = sample_run(result, fps=2)

    assert sampled.times == [0.0, 0.5, 1.0, 1.5, 2.0]
    assert sampled.positions == [
        (1.0, 1.0),
        (2.0, 1.0),
        (3.0, 1.0),
        (2.0, 1.0),
        (1.0, 1.0),
    ]


def test_rectangle_renderer_sampling_contract_uses_geometry() -> None:
    geometry = Rectangle(width=8.0, height=4.0)
    assert geometry.left == 0.0
    assert geometry.right == 8.0

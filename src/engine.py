from __future__ import annotations

from dataclasses import replace

from geometry import Geometry
from model import BallState, CollisionEvent, RunResult, SimulationConfig
from recorder import SimulationRecorder
from reflection import reflect_specular
from stopping import should_stop


def _advance_without_collision(state: BallState, delta_t: float) -> BallState:
    return replace(
        state,
        position=(
            state.position[0] + (state.velocity[0] * delta_t),
            state.position[1] + (state.velocity[1] * delta_t),
        ),
        time=state.time + delta_t,
    )


def _state_at_contact(state: BallState, event: CollisionEvent) -> BallState:
    return replace(
        state,
        position=event.center_at_contact,
        time=state.time + event.time_to_contact,
    )


def run_simulation(
    initial_state: BallState,
    geometry: Geometry,
    config: SimulationConfig | None = None,
) -> RunResult:
    config = config or SimulationConfig()
    if not geometry.contains_ball(initial_state.position, initial_state.radius):
        raise ValueError("Initial ball state is not valid for the geometry")

    recorder = SimulationRecorder(initial_state)
    state = initial_state

    while True:
        reason = should_stop(state, config)
        if reason is not None:
            return recorder.build_result(reason)

        event = geometry.first_contact(
            center=state.position,
            velocity=state.velocity,
            radius=state.radius,
            epsilon=config.epsilon,
        )

        if event is None:
            remaining_time = config.max_time - state.time
            if remaining_time > config.epsilon:
                state = _advance_without_collision(state, remaining_time)
                recorder.record_state(state)
                return recorder.build_result("max_time")
            return recorder.build_result("no_collision")

        if event.time_to_contact <= config.epsilon:
            return recorder.build_result("invalid_event")

        if state.time + event.time_to_contact > config.max_time:
            remaining_time = config.max_time - state.time
            state = _advance_without_collision(state, remaining_time)
            recorder.record_state(state)
            return recorder.build_result("max_time")

        contact_state = _state_at_contact(state, event)
        reflected_velocity = reflect_specular(contact_state.velocity, event.normal)
        state = replace(
            contact_state,
            velocity=reflected_velocity,
            collision_count=contact_state.collision_count + 1,
        )
        recorder.record_collision(event)
        recorder.record_state(state)

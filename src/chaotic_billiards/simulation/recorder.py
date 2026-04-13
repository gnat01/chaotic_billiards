from __future__ import annotations

from chaotic_billiards.types import BallState, CollisionEvent, RunResult


class SimulationRecorder:
    def __init__(self, initial_state: BallState) -> None:
        self._states: list[BallState] = [initial_state]
        self._collisions: list[CollisionEvent] = []

    def record_collision(self, event: CollisionEvent) -> None:
        self._collisions.append(event)

    def record_state(self, state: BallState) -> None:
        self._states.append(state)

    def build_result(self, termination_reason: str) -> RunResult:
        return RunResult(
            states=list(self._states),
            collisions=list(self._collisions),
            termination_reason=termination_reason,
        )

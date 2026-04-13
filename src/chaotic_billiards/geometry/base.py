from __future__ import annotations

from abc import ABC, abstractmethod

from chaotic_billiards.types import CollisionEvent, Vec2


class Geometry(ABC):
    """Boundary interface for finite-radius billiard ball motion."""

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def contains_ball(self, center: Vec2, radius: float) -> bool:
        raise NotImplementedError

    @abstractmethod
    def first_contact(
        self,
        center: Vec2,
        velocity: Vec2,
        radius: float,
        epsilon: float = 1e-9,
    ) -> CollisionEvent | None:
        raise NotImplementedError

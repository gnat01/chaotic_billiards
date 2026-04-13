from __future__ import annotations

from abc import ABC, abstractmethod

from model import CollisionEvent, Vec2


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


class Rectangle(Geometry):
    """Axis-aligned rectangular table."""

    def __init__(self, width: float, height: float, origin: Vec2 = (0.0, 0.0)) -> None:
        if width <= 0.0 or height <= 0.0:
            raise ValueError("Rectangle dimensions must be positive")
        self.width = width
        self.height = height
        self.origin = origin

    @property
    def name(self) -> str:
        return "rectangle"

    @property
    def left(self) -> float:
        return self.origin[0]

    @property
    def right(self) -> float:
        return self.origin[0] + self.width

    @property
    def bottom(self) -> float:
        return self.origin[1]

    @property
    def top(self) -> float:
        return self.origin[1] + self.height

    def contains_ball(self, center: Vec2, radius: float) -> bool:
        if radius < 0.0:
            return False
        return (
            (self.left + radius) <= center[0] <= (self.right - radius)
            and (self.bottom + radius) <= center[1] <= (self.top - radius)
        )

    def first_contact(
        self,
        center: Vec2,
        velocity: Vec2,
        radius: float,
        epsilon: float = 1e-9,
    ) -> CollisionEvent | None:
        candidates: list[CollisionEvent] = []
        vx, vy = velocity

        if vx > epsilon:
            center_x = self.right - radius
            dt = (center_x - center[0]) / vx
            if dt > epsilon:
                center_y = center[1] + (vy * dt)
                if (self.bottom + radius - epsilon) <= center_y <= (self.top - radius + epsilon):
                    candidates.append(
                        CollisionEvent(
                            time_to_contact=dt,
                            center_at_contact=(center_x, center_y),
                            contact_point=(self.right, center_y),
                            normal=(-1.0, 0.0),
                            boundary_label="right_wall",
                        )
                    )

        if vx < -epsilon:
            center_x = self.left + radius
            dt = (center_x - center[0]) / vx
            if dt > epsilon:
                center_y = center[1] + (vy * dt)
                if (self.bottom + radius - epsilon) <= center_y <= (self.top - radius + epsilon):
                    candidates.append(
                        CollisionEvent(
                            time_to_contact=dt,
                            center_at_contact=(center_x, center_y),
                            contact_point=(self.left, center_y),
                            normal=(1.0, 0.0),
                            boundary_label="left_wall",
                        )
                    )

        if vy > epsilon:
            center_y = self.top - radius
            dt = (center_y - center[1]) / vy
            if dt > epsilon:
                center_x = center[0] + (vx * dt)
                if (self.left + radius - epsilon) <= center_x <= (self.right - radius + epsilon):
                    candidates.append(
                        CollisionEvent(
                            time_to_contact=dt,
                            center_at_contact=(center_x, center_y),
                            contact_point=(center_x, self.top),
                            normal=(0.0, -1.0),
                            boundary_label="top_wall",
                        )
                    )

        if vy < -epsilon:
            center_y = self.bottom + radius
            dt = (center_y - center[1]) / vy
            if dt > epsilon:
                center_x = center[0] + (vx * dt)
                if (self.left + radius - epsilon) <= center_x <= (self.right - radius + epsilon):
                    candidates.append(
                        CollisionEvent(
                            time_to_contact=dt,
                            center_at_contact=(center_x, center_y),
                            contact_point=(center_x, self.bottom),
                            normal=(0.0, 1.0),
                            boundary_label="bottom_wall",
                        )
                    )

        if not candidates:
            return None

        return min(candidates, key=lambda event: event.time_to_contact)


class Square(Rectangle):
    def __init__(self, side_length: float, origin: Vec2 = (0.0, 0.0)) -> None:
        super().__init__(width=side_length, height=side_length, origin=origin)

    @property
    def name(self) -> str:
        return "square"


SUPPORTED_GEOMETRIES = (
    "square",
    "rectangle",
    "circle",
    "sinai",
    "triangle",
    "stadium",
)


def build_geometry(
    geometry_name: str,
    *,
    width: float = 10.0,
    height: float = 6.0,
    side_length: float = 10.0,
    origin: Vec2 = (0.0, 0.0),
) -> Geometry:
    if geometry_name == "rectangle":
        return Rectangle(width=width, height=height, origin=origin)
    if geometry_name == "square":
        return Square(side_length=side_length, origin=origin)
    if geometry_name in {"circle", "sinai", "triangle", "stadium"}:
        raise NotImplementedError(f"Geometry '{geometry_name}' is planned but not implemented yet")
    raise ValueError(f"Unknown geometry: {geometry_name}")

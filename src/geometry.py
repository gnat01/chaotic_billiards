from __future__ import annotations

from abc import ABC, abstractmethod
import math

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


def _dot(a: Vec2, b: Vec2) -> float:
    return (a[0] * b[0]) + (a[1] * b[1])


def _sub(a: Vec2, b: Vec2) -> Vec2:
    return (a[0] - b[0], a[1] - b[1])


def _add(a: Vec2, b: Vec2) -> Vec2:
    return (a[0] + b[0], a[1] + b[1])


def _scale(a: Vec2, scalar: float) -> Vec2:
    return (a[0] * scalar, a[1] * scalar)


def _norm(a: Vec2) -> float:
    return math.hypot(a[0], a[1])


def _normalize(a: Vec2) -> Vec2:
    magnitude = _norm(a)
    if magnitude == 0.0:
        raise ValueError("Cannot normalize a zero vector")
    return (a[0] / magnitude, a[1] / magnitude)


def _cross(a: Vec2, b: Vec2) -> float:
    return (a[0] * b[1]) - (a[1] * b[0])


def _polygon_area(vertices: tuple[Vec2, ...]) -> float:
    area = 0.0
    for index, point in enumerate(vertices):
        next_point = vertices[(index + 1) % len(vertices)]
        area += (point[0] * next_point[1]) - (point[1] * next_point[0])
    return 0.5 * area


def _ensure_ccw(vertices: tuple[Vec2, ...]) -> tuple[Vec2, ...]:
    if _polygon_area(vertices) < 0.0:
        return tuple(reversed(vertices))
    return vertices


def _edge_inward_normal(start: Vec2, end: Vec2) -> Vec2:
    edge = _sub(end, start)
    return _normalize((-edge[1], edge[0]))


def _project_onto_segment(point: Vec2, start: Vec2, end: Vec2) -> float:
    edge = _sub(end, start)
    edge_sq = _dot(edge, edge)
    if edge_sq == 0.0:
        return 0.0
    return _dot(_sub(point, start), edge) / edge_sq


def _first_polygon_contact(
    vertices: tuple[Vec2, ...],
    center: Vec2,
    velocity: Vec2,
    radius: float,
    epsilon: float = 1e-9,
    labels: tuple[str, ...] | None = None,
) -> CollisionEvent | None:
    candidates: list[CollisionEvent] = []

    for index, start in enumerate(vertices):
        end = vertices[(index + 1) % len(vertices)]
        inward_normal = _edge_inward_normal(start, end)
        inward_distance = _dot(_sub(center, start), inward_normal)
        velocity_along_normal = _dot(velocity, inward_normal)
        if velocity_along_normal >= -epsilon:
            continue

        dt = (radius - inward_distance) / velocity_along_normal
        if dt <= epsilon:
            continue

        center_at_contact = _add(center, _scale(velocity, dt))
        wall_contact = _sub(center_at_contact, _scale(inward_normal, radius))
        edge_fraction = _project_onto_segment(wall_contact, start, end)
        if not (-epsilon <= edge_fraction <= 1.0 + epsilon):
            continue

        candidates.append(
            CollisionEvent(
                time_to_contact=dt,
                center_at_contact=center_at_contact,
                contact_point=wall_contact,
                normal=inward_normal,
                boundary_label=labels[index] if labels is not None else f"edge_{index}",
            )
        )

    if not candidates:
        return None

    return min(candidates, key=lambda event: event.time_to_contact)


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


class CircleTable(Geometry):
    def __init__(self, radius: float, center: Vec2 = (5.0, 5.0)) -> None:
        if radius <= 0.0:
            raise ValueError("Circle radius must be positive")
        self.radius = radius
        self.center = center

    @property
    def name(self) -> str:
        return "circle"

    @property
    def left(self) -> float:
        return self.center[0] - self.radius

    @property
    def right(self) -> float:
        return self.center[0] + self.radius

    @property
    def bottom(self) -> float:
        return self.center[1] - self.radius

    @property
    def top(self) -> float:
        return self.center[1] + self.radius

    def contains_ball(self, center: Vec2, radius: float) -> bool:
        return _norm(_sub(center, self.center)) <= (self.radius - radius)

    def first_contact(
        self,
        center: Vec2,
        velocity: Vec2,
        radius: float,
        epsilon: float = 1e-9,
    ) -> CollisionEvent | None:
        effective_radius = self.radius - radius
        relative_center = _sub(center, self.center)
        speed_sq = _dot(velocity, velocity)
        if speed_sq <= epsilon:
            return None

        quadratic_a = speed_sq
        quadratic_b = 2.0 * _dot(relative_center, velocity)
        quadratic_c = _dot(relative_center, relative_center) - (effective_radius * effective_radius)
        discriminant = (quadratic_b * quadratic_b) - (4.0 * quadratic_a * quadratic_c)
        if discriminant < 0.0:
            return None

        sqrt_discriminant = math.sqrt(max(discriminant, 0.0))
        roots = (
            (-quadratic_b - sqrt_discriminant) / (2.0 * quadratic_a),
            (-quadratic_b + sqrt_discriminant) / (2.0 * quadratic_a),
        )
        dt = min((root for root in roots if root > epsilon), default=None)
        if dt is None:
            return None

        center_at_contact = _add(center, _scale(velocity, dt))
        inward_normal = _normalize(_sub(self.center, center_at_contact))
        contact_point = _sub(center_at_contact, _scale(inward_normal, radius))
        return CollisionEvent(
            time_to_contact=dt,
            center_at_contact=center_at_contact,
            contact_point=contact_point,
            normal=inward_normal,
            boundary_label="circular_wall",
        )


class Triangle(Geometry):
    def __init__(self, width: float, height: float, origin: Vec2 = (0.0, 0.0)) -> None:
        if width <= 0.0 or height <= 0.0:
            raise ValueError("Triangle dimensions must be positive")
        self.width = width
        self.height = height
        self.origin = origin
        self.vertices = _ensure_ccw(
            (
                origin,
                (origin[0] + width, origin[1]),
                (origin[0] + (0.5 * width), origin[1] + height),
            )
        )
        self.edge_labels = ("base", "right_slope", "left_slope")

    @property
    def name(self) -> str:
        return "triangle"

    @property
    def left(self) -> float:
        return min(vertex[0] for vertex in self.vertices)

    @property
    def right(self) -> float:
        return max(vertex[0] for vertex in self.vertices)

    @property
    def bottom(self) -> float:
        return min(vertex[1] for vertex in self.vertices)

    @property
    def top(self) -> float:
        return max(vertex[1] for vertex in self.vertices)

    def contains_ball(self, center: Vec2, radius: float) -> bool:
        if radius < 0.0:
            return False
        for index, start in enumerate(self.vertices):
            end = self.vertices[(index + 1) % len(self.vertices)]
            inward_normal = _edge_inward_normal(start, end)
            if _dot(_sub(center, start), inward_normal) < (radius - 1e-9):
                return False
        return True

    def first_contact(
        self,
        center: Vec2,
        velocity: Vec2,
        radius: float,
        epsilon: float = 1e-9,
    ) -> CollisionEvent | None:
        return _first_polygon_contact(
            self.vertices,
            center=center,
            velocity=velocity,
            radius=radius,
            epsilon=epsilon,
            labels=self.edge_labels,
        )


class SinaiTable(Geometry):
    def __init__(
        self,
        width: float,
        height: float,
        obstacle_radius: float,
        obstacle_center: Vec2 | None = None,
        origin: Vec2 = (0.0, 0.0),
    ) -> None:
        if obstacle_radius <= 0.0:
            raise ValueError("Sinai obstacle radius must be positive")
        self.outer = Rectangle(width=width, height=height, origin=origin)
        self.obstacle_radius = obstacle_radius
        self.obstacle_center = obstacle_center or (
            origin[0] + (0.5 * width),
            origin[1] + (0.5 * height),
        )

    @property
    def name(self) -> str:
        return "sinai"

    @property
    def left(self) -> float:
        return self.outer.left

    @property
    def right(self) -> float:
        return self.outer.right

    @property
    def bottom(self) -> float:
        return self.outer.bottom

    @property
    def top(self) -> float:
        return self.outer.top

    @property
    def width(self) -> float:
        return self.outer.width

    @property
    def height(self) -> float:
        return self.outer.height

    @property
    def origin(self) -> Vec2:
        return self.outer.origin

    def contains_ball(self, center: Vec2, radius: float) -> bool:
        if not self.outer.contains_ball(center, radius):
            return False
        return _norm(_sub(center, self.obstacle_center)) >= (self.obstacle_radius + radius)

    def _obstacle_contact(
        self,
        center: Vec2,
        velocity: Vec2,
        radius: float,
        epsilon: float = 1e-9,
    ) -> CollisionEvent | None:
        inflated_radius = self.obstacle_radius + radius
        relative_center = _sub(center, self.obstacle_center)
        speed_sq = _dot(velocity, velocity)
        if speed_sq <= epsilon:
            return None

        quadratic_a = speed_sq
        quadratic_b = 2.0 * _dot(relative_center, velocity)
        quadratic_c = _dot(relative_center, relative_center) - (inflated_radius * inflated_radius)
        discriminant = (quadratic_b * quadratic_b) - (4.0 * quadratic_a * quadratic_c)
        if discriminant < 0.0:
            return None

        sqrt_discriminant = math.sqrt(max(discriminant, 0.0))
        roots = (
            (-quadratic_b - sqrt_discriminant) / (2.0 * quadratic_a),
            (-quadratic_b + sqrt_discriminant) / (2.0 * quadratic_a),
        )
        dt = min((root for root in roots if root > epsilon), default=None)
        if dt is None:
            return None

        center_at_contact = _add(center, _scale(velocity, dt))
        inward_normal = _normalize(_sub(center_at_contact, self.obstacle_center))
        contact_point = _sub(center_at_contact, _scale(inward_normal, radius))
        return CollisionEvent(
            time_to_contact=dt,
            center_at_contact=center_at_contact,
            contact_point=contact_point,
            normal=inward_normal,
            boundary_label="obstacle",
        )

    def first_contact(
        self,
        center: Vec2,
        velocity: Vec2,
        radius: float,
        epsilon: float = 1e-9,
    ) -> CollisionEvent | None:
        candidates = []
        outer_event = self.outer.first_contact(center, velocity, radius, epsilon)
        if outer_event is not None:
            candidates.append(outer_event)
        obstacle_event = self._obstacle_contact(center, velocity, radius, epsilon)
        if obstacle_event is not None:
            candidates.append(obstacle_event)
        if not candidates:
            return None
        return min(candidates, key=lambda event: event.time_to_contact)


class StadiumTable(Geometry):
    """Horizontal Bunimovich stadium with semicircular endcaps."""

    def __init__(self, width: float, height: float, origin: Vec2 = (0.0, 0.0)) -> None:
        if width <= 0.0 or height <= 0.0:
            raise ValueError("Stadium dimensions must be positive")
        if width < height:
            raise ValueError("Stadium currently requires width >= height")
        self.width = width
        self.height = height
        self.origin = origin
        self.cap_radius = 0.5 * height
        self.left_cap_center = (origin[0] + self.cap_radius, origin[1] + self.cap_radius)
        self.right_cap_center = (
            origin[0] + width - self.cap_radius,
            origin[1] + self.cap_radius,
        )

    @property
    def name(self) -> str:
        return "stadium"

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
        effective_radius = self.cap_radius - radius
        if effective_radius < 0.0:
            return False
        clamped_x = min(max(center[0], self.left_cap_center[0]), self.right_cap_center[0])
        closest_point = (clamped_x, self.left_cap_center[1])
        return _norm(_sub(center, closest_point)) <= (effective_radius + 1e-9)

    def _circle_contact(
        self,
        circle_center: Vec2,
        center: Vec2,
        velocity: Vec2,
        effective_radius: float,
        boundary_label: str,
        x_predicate,
        epsilon: float,
    ) -> CollisionEvent | None:
        relative_center = _sub(center, circle_center)
        speed_sq = _dot(velocity, velocity)
        if speed_sq <= epsilon:
            return None

        quadratic_a = speed_sq
        quadratic_b = 2.0 * _dot(relative_center, velocity)
        quadratic_c = _dot(relative_center, relative_center) - (effective_radius * effective_radius)
        discriminant = (quadratic_b * quadratic_b) - (4.0 * quadratic_a * quadratic_c)
        if discriminant < 0.0:
            return None

        sqrt_discriminant = math.sqrt(max(discriminant, 0.0))
        roots = (
            (-quadratic_b - sqrt_discriminant) / (2.0 * quadratic_a),
            (-quadratic_b + sqrt_discriminant) / (2.0 * quadratic_a),
        )
        for dt in sorted(root for root in roots if root > epsilon):
            center_at_contact = _add(center, _scale(velocity, dt))
            if not x_predicate(center_at_contact[0]):
                continue
            inward_normal = _normalize(_sub(circle_center, center_at_contact))
            return CollisionEvent(
                time_to_contact=dt,
                center_at_contact=center_at_contact,
                contact_point=center_at_contact,
                normal=inward_normal,
                boundary_label=boundary_label,
            )
        return None

    def first_contact(
        self,
        center: Vec2,
        velocity: Vec2,
        radius: float,
        epsilon: float = 1e-9,
    ) -> CollisionEvent | None:
        effective_radius = self.cap_radius - radius
        if effective_radius < 0.0:
            return None

        candidates: list[CollisionEvent] = []
        vx, vy = velocity

        if vy > epsilon:
            center_y = self.top - radius
            dt = (center_y - center[1]) / vy
            if dt > epsilon:
                center_x = center[0] + (vx * dt)
                if self.left_cap_center[0] - epsilon <= center_x <= self.right_cap_center[0] + epsilon:
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
                if self.left_cap_center[0] - epsilon <= center_x <= self.right_cap_center[0] + epsilon:
                    candidates.append(
                        CollisionEvent(
                            time_to_contact=dt,
                            center_at_contact=(center_x, center_y),
                            contact_point=(center_x, self.bottom),
                            normal=(0.0, 1.0),
                            boundary_label="bottom_wall",
                        )
                    )

        left_event = self._circle_contact(
            self.left_cap_center,
            center,
            velocity,
            effective_radius,
            "left_cap",
            lambda x: x <= self.left_cap_center[0] + epsilon,
            epsilon,
        )
        if left_event is not None:
            left_normal = _normalize(_sub(self.left_cap_center, left_event.center_at_contact))
            candidates.append(
                CollisionEvent(
                    time_to_contact=left_event.time_to_contact,
                    center_at_contact=left_event.center_at_contact,
                    contact_point=_sub(left_event.center_at_contact, _scale(left_normal, radius)),
                    normal=left_normal,
                    boundary_label=left_event.boundary_label,
                )
            )

        right_event = self._circle_contact(
            self.right_cap_center,
            center,
            velocity,
            effective_radius,
            "right_cap",
            lambda x: x >= self.right_cap_center[0] - epsilon,
            epsilon,
        )
        if right_event is not None:
            right_normal = _normalize(_sub(self.right_cap_center, right_event.center_at_contact))
            candidates.append(
                CollisionEvent(
                    time_to_contact=right_event.time_to_contact,
                    center_at_contact=right_event.center_at_contact,
                    contact_point=_sub(right_event.center_at_contact, _scale(right_normal, radius)),
                    normal=right_normal,
                    boundary_label=right_event.boundary_label,
                )
            )

        if not candidates:
            return None
        return min(candidates, key=lambda event: event.time_to_contact)


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
    circle_radius: float = 5.0,
    obstacle_radius: float | None = None,
    obstacle_center: Vec2 | None = None,
    origin: Vec2 = (0.0, 0.0),
) -> Geometry:
    if geometry_name == "rectangle":
        return Rectangle(width=width, height=height, origin=origin)
    if geometry_name == "square":
        return Square(side_length=side_length, origin=origin)
    if geometry_name == "circle":
        return CircleTable(radius=circle_radius, center=(origin[0] + circle_radius, origin[1] + circle_radius))
    if geometry_name == "triangle":
        return Triangle(width=width, height=height, origin=origin)
    if geometry_name == "sinai":
        actual_obstacle_radius = obstacle_radius if obstacle_radius is not None else (0.18 * min(width, height))
        return SinaiTable(
            width=width,
            height=height,
            obstacle_radius=actual_obstacle_radius,
            obstacle_center=obstacle_center,
            origin=origin,
        )
    if geometry_name == "stadium":
        return StadiumTable(width=width, height=height, origin=origin)
    raise ValueError(f"Unknown geometry: {geometry_name}")

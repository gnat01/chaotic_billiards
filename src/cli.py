from __future__ import annotations

import argparse
import math

from engine import run_simulation
from geometry import SUPPORTED_GEOMETRIES, build_geometry
from model import BallState, SimulationConfig
from visualization import show_animation


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run and visualize chaotic billiards demos")
    parser.add_argument("--geometry", choices=SUPPORTED_GEOMETRIES, default="rectangle")
    parser.add_argument("--width", type=float, default=10.0)
    parser.add_argument("--height", type=float, default=6.0)
    parser.add_argument("--side-length", type=float, default=10.0)
    parser.add_argument("--circle-radius", type=float, default=5.0)
    parser.add_argument("--obstacle-radius", type=float, default=None)
    parser.add_argument("--obstacle-x", type=float, default=None)
    parser.add_argument("--obstacle-y", type=float, default=None)
    parser.add_argument("--ball-radius", type=float, default=0.35)
    parser.add_argument("--start-x", type=float, default=2.0)
    parser.add_argument("--start-y", type=float, default=2.0)
    parser.add_argument("--vx", type=float, default=3.0)
    parser.add_argument("--vy", type=float, default=1.75)
    parser.add_argument("--launch-angle-deg", type=float, default=None)
    parser.add_argument("--speed", type=float, default=None)
    parser.add_argument("--max-time", type=float, default=12.0)
    parser.add_argument("--max-collisions", type=int, default=500)
    parser.add_argument("--reflection-mode", choices=("elastic", "inelastic"), default="elastic")
    parser.add_argument("--restitution", type=float, default=0.9)
    parser.add_argument("--fps", type=int, default=60)
    parser.add_argument("--hide-path", action="store_true")
    parser.add_argument("--save", type=str, default=None)
    return parser


def resolve_velocity(
    vx: float,
    vy: float,
    launch_angle_deg: float | None,
    speed: float | None,
) -> tuple[float, float]:
    if launch_angle_deg is None:
        return (vx, vy)

    if not 0.0 <= launch_angle_deg <= 359.0:
        raise ValueError("launch angle must be between 0 and 359 degrees")

    resolved_speed = speed if speed is not None else math.hypot(vx, vy)
    if resolved_speed <= 0.0:
        raise ValueError("speed must be positive when launch angle is used")

    angle_radians = math.radians(launch_angle_deg)
    return (
        resolved_speed * math.cos(angle_radians),
        resolved_speed * math.sin(angle_radians),
    )


def main() -> None:
    args = build_parser().parse_args()
    geometry = build_geometry(
        args.geometry,
        width=args.width,
        height=args.height,
        side_length=args.side_length,
        circle_radius=args.circle_radius,
        obstacle_radius=args.obstacle_radius,
        obstacle_center=(
            (args.obstacle_x, args.obstacle_y)
            if args.obstacle_x is not None and args.obstacle_y is not None
            else None
        ),
    )

    if not 0.0 < args.ball_radius:
        raise ValueError("ball radius must be positive")
    if not 0.0 <= args.restitution <= 1.0:
        raise ValueError("restitution must be between 0 and 1")
    if args.speed is not None and args.speed <= 0.0:
        raise ValueError("speed must be positive")

    initial_velocity = resolve_velocity(
        vx=args.vx,
        vy=args.vy,
        launch_angle_deg=args.launch_angle_deg,
        speed=args.speed,
    )

    initial_state = BallState(
        position=(args.start_x, args.start_y),
        velocity=initial_velocity,
        radius=args.ball_radius,
    )
    config = SimulationConfig(
        max_time=args.max_time,
        max_collisions=args.max_collisions,
        reflection_mode=args.reflection_mode,
        restitution=args.restitution,
    )

    result = run_simulation(initial_state=initial_state, geometry=geometry, config=config)
    title = (
        f"{geometry.name} | mode={args.reflection_mode} | "
        f"T={args.max_time:g} | r={args.ball_radius:g}"
    )
    print(f"geometry={geometry.name}")
    if hasattr(geometry, "width") and hasattr(geometry, "height"):
        print(f"table={getattr(geometry, 'width')} x {getattr(geometry, 'height')}")
    if hasattr(geometry, "radius"):
        print(f"table_radius={getattr(geometry, 'radius')}")
    if hasattr(geometry, "obstacle_radius"):
        print(f"obstacle_radius={getattr(geometry, 'obstacle_radius')}")
        print(f"obstacle_center={getattr(geometry, 'obstacle_center')}")
    print(f"ball_radius={args.ball_radius}")
    print(f"start=({args.start_x}, {args.start_y})")
    if args.launch_angle_deg is not None:
        print(f"launch_angle_deg={args.launch_angle_deg}")
        print(f"speed={math.hypot(*initial_velocity)}")
    print(f"velocity={initial_velocity}")
    print(f"max_time={args.max_time}")
    print(f"max_collisions={args.max_collisions}")
    print(f"reflection_mode={args.reflection_mode}")
    if args.reflection_mode == "inelastic":
        print(f"restitution={args.restitution}")
    print(f"fps={args.fps}")

    animation_handle = show_animation(
        result=result,
        geometry=geometry,
        fps=args.fps,
        show_path=not args.hide_path,
        title=title,
        save_path=args.save,
    )
    _ = animation_handle


if __name__ == "__main__":
    main()

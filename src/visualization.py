from __future__ import annotations

from dataclasses import dataclass

import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle as RectanglePatch

from geometry import Rectangle, Square
from model import RunResult, Vec2


@dataclass(frozen=True)
class SampledTrajectory:
    times: list[float]
    positions: list[Vec2]


def sample_run(result: RunResult, fps: int = 60) -> SampledTrajectory:
    if fps <= 0:
        raise ValueError("fps must be positive")

    states = result.states
    if not states:
        return SampledTrajectory(times=[], positions=[])

    sample_dt = 1.0 / fps
    sampled_times: list[float] = []
    sampled_positions: list[Vec2] = []

    for index, state in enumerate(states[:-1]):
        next_state = states[index + 1]
        segment_duration = next_state.time - state.time
        if segment_duration < 0.0:
            raise ValueError("RunResult states must be time-ordered")
        if segment_duration == 0.0:
            continue

        t = state.time
        while t < next_state.time:
            dt = t - state.time
            sampled_times.append(t)
            sampled_positions.append(
                (
                    state.position[0] + (state.velocity[0] * dt),
                    state.position[1] + (state.velocity[1] * dt),
                )
            )
            t += sample_dt

    sampled_times.append(states[-1].time)
    sampled_positions.append(states[-1].position)
    return SampledTrajectory(times=sampled_times, positions=sampled_positions)


def _add_geometry_patch(ax: plt.Axes, geometry: object) -> None:
    if isinstance(geometry, Rectangle):
        patch = RectanglePatch(
            geometry.origin,
            geometry.width,
            geometry.height,
            fill=False,
            linewidth=2.0,
            edgecolor="black",
        )
        ax.add_patch(patch)
        return
    if isinstance(geometry, Square):
        patch = RectanglePatch(
            geometry.origin,
            geometry.width,
            geometry.height,
            fill=False,
            linewidth=2.0,
            edgecolor="black",
        )
        ax.add_patch(patch)
        return
    raise NotImplementedError(f"No renderer for geometry type: {type(geometry).__name__}")


def _set_axes_limits(ax: plt.Axes, geometry: object, padding: float = 0.5) -> None:
    if isinstance(geometry, Rectangle):
        ax.set_xlim(geometry.left - padding, geometry.right + padding)
        ax.set_ylim(geometry.bottom - padding, geometry.top + padding)
        ax.set_aspect("equal", adjustable="box")
        return
    raise NotImplementedError(f"No axis setup for geometry type: {type(geometry).__name__}")


def animate_run(
    result: RunResult,
    geometry: object,
    *,
    fps: int = 60,
    show_path: bool = True,
    title: str | None = None,
    save_path: str | None = None,
) -> animation.FuncAnimation:
    sampled = sample_run(result, fps=fps)

    fig, ax = plt.subplots(figsize=(8, 5))
    _add_geometry_patch(ax, geometry)
    _set_axes_limits(ax, geometry, padding=result.final_state.radius + 0.5)
    ax.set_title(title or f"{geometry.name} billiard")
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    ball = Circle(
        result.states[0].position,
        result.states[0].radius,
        facecolor="#d1495b",
        edgecolor="#5f0f40",
        linewidth=1.5,
    )
    ax.add_patch(ball)
    path_line, = ax.plot([], [], color="#00798c", linewidth=1.5, alpha=0.9)
    time_text = ax.text(0.02, 0.98, "", transform=ax.transAxes, va="top")

    path_x: list[float] = []
    path_y: list[float] = []

    def update(frame_index: int):
        position = sampled.positions[frame_index]
        ball.center = position
        if show_path:
            path_x.append(position[0])
            path_y.append(position[1])
            path_line.set_data(path_x, path_y)
        time_text.set_text(f"t = {sampled.times[frame_index]:.2f}")
        return ball, path_line, time_text

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=len(sampled.positions),
        interval=1000 / fps,
        blit=True,
        repeat=False,
    )

    if save_path is not None:
        ani.save(save_path)

    return ani


def show_animation(
    result: RunResult,
    geometry: object,
    *,
    fps: int = 60,
    show_path: bool = True,
    title: str | None = None,
    save_path: str | None = None,
) -> animation.FuncAnimation:
    ani = animate_run(
        result=result,
        geometry=geometry,
        fps=fps,
        show_path=show_path,
        title=title,
        save_path=save_path,
    )
    plt.show()
    return ani

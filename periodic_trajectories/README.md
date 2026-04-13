# Periodic Trajectories

This directory collects reproducible periodic or near-periodic launch setups for the current billiards simulator.

Each example includes:

- geometry
- table parameters
- ball radius
- starting position
- launch angle in degrees
- speed
- a ready-to-run CLI command

These are intended as educational presets, not formal proofs of periodicity under every numerical setting.

## Files

- [square_horizontal_two_cycle.json](/Users/gn/work/learn/python/chaotic_billiards/periodic_trajectories/square_horizontal_two_cycle.json)
- [square_diagonal_four_cycle.json](/Users/gn/work/learn/python/chaotic_billiards/periodic_trajectories/square_diagonal_four_cycle.json)
- [rectangle_rational_slope.json](/Users/gn/work/learn/python/chaotic_billiards/periodic_trajectories/rectangle_rational_slope.json)
- [circle_diameter_two_cycle.json](/Users/gn/work/learn/python/chaotic_billiards/periodic_trajectories/circle_diameter_two_cycle.json)
- [triangle_symmetry_axis.json](/Users/gn/work/learn/python/chaotic_billiards/periodic_trajectories/triangle_symmetry_axis.json)
- [stadium_centerline_two_cycle.json](/Users/gn/work/learn/python/chaotic_billiards/periodic_trajectories/stadium_centerline_two_cycle.json)

## Notes

- `launch_angle_deg` uses the CLI convention:
  - `0` means due right
  - `90` means straight up
  - `180` means due left
  - `270` means straight down
- If you use `--launch-angle-deg`, the CLI computes `vx, vy` from angle and speed.
- These examples are intended for `--reflection-mode elastic`.

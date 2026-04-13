# How To Run

This file documents the current CLI runner for `chaotic_billiards`.

The CLI lives at [src/cli.py](/Users/gn/work/learn/python/chaotic_billiards/src/cli.py).

## Basic Run

From the repository root:

```bash
PYTHONPATH=src python src/cli.py
```

That launches the default animation:

- geometry: `rectangle`
- width: `10`
- height: `6`
- ball radius: `0.35`
- start position: `(2.0, 2.0)`
- velocity: `(3.0, 1.75)`
- max time: `12`
- reflection mode: `elastic`

## Common Examples

Rectangle, elastic:

```bash
PYTHONPATH=src python src/cli.py \
  --geometry rectangle \
  --width 12 \
  --height 7 \
  --ball-radius 0.35 \
  --start-x 2.0 \
  --start-y 2.0 \
  --vx 3.0 \
  --vy 1.75 \
  --max-time 12 \
  --reflection-mode elastic
```

Square, inelastic:

```bash
PYTHONPATH=src python src/cli.py \
  --geometry square \
  --side-length 10 \
  --ball-radius 0.4 \
  --start-x 3 \
  --start-y 3 \
  --vx 4 \
  --vy 2.5 \
  --max-time 20 \
  --reflection-mode inelastic \
  --restitution 0.85
```

Save output instead of only showing it:

```bash
PYTHONPATH=src python src/cli.py \
  --geometry rectangle \
  --width 10 \
  --height 6 \
  --save output.mp4
```

Hide the traced path:

```bash
PYTHONPATH=src python src/cli.py --hide-path
```

## All Flags

### `--geometry`

Type: string

Accepted values:

- `rectangle`
- `square`
- `circle`
- `sinai`
- `triangle`
- `stadium`

Current status:

- implemented: `rectangle`, `square`
- planned but not implemented yet: `circle`, `sinai`, `triangle`, `stadium`

Hard constraint:

- must be one of the listed values

Recommended usage:

- use `rectangle` or `square` right now

### `--width`

Type: float

Default:

- `10.0`

Used by:

- `rectangle`

Hard constraint:

- must be `> 0`

Recommended range:

- `4` to `30`

Notes:

- ignored for `square`
- larger values make horizontal travel longer and reduce apparent bounce frequency for the same velocity

### `--height`

Type: float

Default:

- `6.0`

Used by:

- `rectangle`

Hard constraint:

- must be `> 0`

Recommended range:

- `4` to `20`

Notes:

- ignored for `square`

### `--side-length`

Type: float

Default:

- `10.0`

Used by:

- `square`

Hard constraint:

- must be `> 0`

Recommended range:

- `4` to `20`

Notes:

- ignored for `rectangle`

### `--ball-radius`

Type: float

Default:

- `0.35`

Hard constraint:

- must be `> 0`
- must also fit inside the chosen geometry together with the chosen start position

Practical range:

- `0.1` to `1.5` for the current default table sizes

Recommended range:

- rectangle `10 x 6`: `0.15` to `0.75`
- square `10 x 10`: `0.15` to `1.0`

Notes:

- larger radius makes the ball feel more physical on screen
- very large radius sharply reduces the accessible region and makes invalid starts more likely

### `--start-x`

Type: float

Default:

- `2.0`

Hard constraint:

- must satisfy `left + radius <= start_x <= right - radius`

For the default rectangle:

- valid range is `[0.35, 9.65]`

For the default square:

- valid range is `[0.35, 9.65]`

Notes:

- if this is outside the allowed center region, the program raises a `ValueError`

### `--start-y`

Type: float

Default:

- `2.0`

Hard constraint:

- must satisfy `bottom + radius <= start_y <= top - radius`

For the default rectangle:

- valid range is `[0.35, 5.65]`

For the default square:

- valid range is `[0.35, 9.65]`

Notes:

- if this is outside the allowed center region, the program raises a `ValueError`

### `--vx`

Type: float

Default:

- `3.0`

Hard constraint:

- any float is accepted

Practical range:

- `-10` to `10`

Recommended range:

- `-6` to `6`

Notes:

- `0` is allowed
- if both `vx` and `vy` are `0`, the run will stop immediately on min-speed logic
- larger magnitudes make the animation feel faster, but can make runs visually busy

### `--vy`

Type: float

Default:

- `1.75`

Hard constraint:

- any float is accepted

Practical range:

- `-10` to `10`

Recommended range:

- `-6` to `6`

Notes:

- same considerations as `--vx`

### `--max-time`

Type: float

Default:

- `12.0`

Hard constraint:

- should be `> 0`

Recommended range:

- `3` to `60`

Notes:

- this is the total simulation time horizon
- larger values mean more travel and more bounces
- very large values can make the animation long and the traced path dense

### `--max-collisions`

Type: integer

Default:

- `500`

Hard constraint:

- should be `>= 1`

Recommended range:

- `10` to `5000`

Notes:

- this is a safety cap on the number of wall collisions
- whichever limit is hit first ends the run: `max-time` or `max-collisions`

### `--reflection-mode`

Type: string

Accepted values:

- `elastic`
- `inelastic`

Default:

- `elastic`

Meaning:

- `elastic`: preserve speed at wall reflection
- `inelastic`: reduce the wall-normal component using `--restitution`

Recommended usage:

- start with `elastic`
- use `inelastic` when you want the ball to settle into slower motion over time

### `--restitution`

Type: float

Default:

- `0.9`

Hard constraint:

- must be between `0` and `1`, inclusive

Meaning:

- `1.0`: fully elastic on the wall-normal component
- `0.0`: completely removes the outgoing wall-normal component

Recommended range:

- `0.7` to `1.0`

Useful values:

- `1.0`: effectively elastic
- `0.95`: very light loss
- `0.85`: noticeable loss
- `0.5`: strong loss

Notes:

- this only matters when `--reflection-mode inelastic`

### `--fps`

Type: integer

Default:

- `60`

Hard constraint:

- must be `> 0`

Recommended range:

- `24` to `120`

Useful values:

- `24`: coarse but lightweight
- `30`: standard preview
- `60`: good default
- `120`: very smooth, if you want dense playback

### `--hide-path`

Type: flag

Default:

- off

Meaning:

- if provided, the traced center-path line is hidden

Use it when:

- you want to focus on the ball motion itself
- the path becomes too visually dense

### `--save`

Type: string path

Default:

- `None`

Meaning:

- save the animation to the given file path

Examples:

- `--save output.mp4`
- `--save run.gif`

Notes:

- whether a particular save target works depends on your local matplotlib animation writer support

## Important Parameter Interactions

These matter more than the individual flags by themselves.

### Ball radius and start position

The center of the ball must start inside the valid eroded table:

- rectangle: `radius <= x <= width - radius`
- rectangle: `radius <= y <= height - radius`
- square: same rule using `side-length`

If you make the radius larger, you usually need to move `start-x` and `start-y` inward.

### Ball radius and geometry size

These combinations are bad:

- very large radius in a small table
- radius close to half the smaller table dimension

Practical rule:

- keep `ball-radius < min(width, height) / 4` for a comfortable first pass

### Velocity and max time

If speed is high and `max-time` is large:

- the run will produce many bounces
- the path may become visually crowded

Good starting combinations:

- moderate speed `sqrt(vx^2 + vy^2)` around `2` to `6`
- `max-time` around `8` to `20`

### Inelastic mode and restitution

If `reflection-mode` is `inelastic` and `restitution` is low:

- the ball loses speed faster
- long runs may feel visually dead after a while

Good starting values:

- `0.9`
- `0.95`

## Best Starting Settings

If you just want something that feels good on screen, start here:

### Rectangle

```bash
PYTHONPATH=src python src/cli.py \
  --geometry rectangle \
  --width 12 \
  --height 7 \
  --ball-radius 0.35 \
  --start-x 2.0 \
  --start-y 2.0 \
  --vx 3.2 \
  --vy 1.9 \
  --max-time 14 \
  --max-collisions 800 \
  --reflection-mode elastic \
  --fps 60
```

### Square

```bash
PYTHONPATH=src python src/cli.py \
  --geometry square \
  --side-length 10 \
  --ball-radius 0.4 \
  --start-x 3.0 \
  --start-y 3.0 \
  --vx 4.0 \
  --vy 2.5 \
  --max-time 16 \
  --max-collisions 800 \
  --reflection-mode elastic \
  --fps 60
```

## Current Gaps

The CLI already exposes the geometry names you said you want to support long term, but right now only these are runnable:

- `rectangle`
- `square`

These are registered but not yet implemented:

- `circle`
- `sinai`
- `triangle`
- `stadium`

If you pass one of those today, the program will raise `NotImplementedError`.

## Current Missing Knobs

These are not exposed yet, but are obvious next additions:

- table origin
- background and visual styling
- line thickness and ball color
- drag during free motion
- random initial conditions
- preset trajectories
- separate playback speed versus simulation duration

## Quick Reference

```bash
PYTHONPATH=src python src/cli.py \
  --geometry rectangle|square \
  --width FLOAT \
  --height FLOAT \
  --side-length FLOAT \
  --ball-radius FLOAT \
  --start-x FLOAT \
  --start-y FLOAT \
  --vx FLOAT \
  --vy FLOAT \
  --max-time FLOAT \
  --max-collisions INT \
  --reflection-mode elastic|inelastic \
  --restitution FLOAT \
  --fps INT \
  --hide-path \
  --save PATH
```

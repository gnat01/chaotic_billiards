# Periodic Trajectories

This file lists exact CLI commands for the current periodic or near-periodic example trajectories.

Run all commands from the repository root:

```bash
cd /Users/gn/work/learn/python/chaotic_billiards
```

## Square: Horizontal Two-Cycle

The ball runs along the horizontal centerline and bounces back and forth between the left and right walls.

```bash
PYTHONPATH=src python src/cli.py \
  --geometry square \
  --side-length 10 \
  --ball-radius 0.35 \
  --start-x 5 \
  --start-y 5 \
  --launch-angle-deg 0 \
  --speed 3 \
  --max-time 12 \
  --reflection-mode elastic
```

## Square: Diagonal Four-Cycle

The classic 45-degree square orbit.

```bash
PYTHONPATH=src python src/cli.py \
  --geometry square \
  --side-length 10 \
  --ball-radius 0.35 \
  --start-x 5 \
  --start-y 5 \
  --launch-angle-deg 45 \
  --speed 3 \
  --max-time 12 \
  --reflection-mode elastic
```
### Square : long cycle

```bash
PYTHONPATH=src python src/cli.py \
  --geometry square \
  --side-length 10 \
  --ball-radius 0.35 \
  --start-x 5 \
  --start-y 5 \
  --launch-angle-deg 60 \
  --speed 10 \
  --max-time 50 \
  --reflection-mode elastic 
```

### Square : gated complex!

```bash
PYTHONPATH=src python src/cli.py \
  --geometry square \
  --side-length 10 \
  --ball-radius 0.35 \
  --start-x 5 \
  --start-y 5 \
  --launch-angle-deg 80 \
  --speed 17 \
  --max-time 50 \
  --reflection-mode elastic 
```

## Rectangle: Rational-Slope Orbit

A repeating rectangular orbit using a rational slope.

```bash
PYTHONPATH=src python src/cli.py \
  --geometry rectangle \
  --width 12 \
  --height 8 \
  --ball-radius 0.3 \
  --start-x 3 \
  --start-y 3 \
  --launch-angle-deg 53.1301023542 \
  --speed 2.5 \
  --max-time 18 \
  --reflection-mode elastic
```

## Circle: Diameter Two-Cycle

The ball travels through the center of the circle along a diameter.

```bash
PYTHONPATH=src python src/cli.py \
  --geometry circle \
  --circle-radius 5 \
  --ball-radius 0.35 \
  --start-x 5 \
  --start-y 5 \
  --launch-angle-deg 0 \
  --speed 3 \
  --max-time 12 \
  --reflection-mode elastic
```

## Triangle: Symmetry-Axis Orbit

An up-down launch along the isosceles triangle symmetry axis.

```bash
PYTHONPATH=src python src/cli.py \
  --geometry triangle \
  --width 10 \
  --height 8 \
  --ball-radius 0.25 \
  --start-x 5 \
  --start-y 2 \
  --launch-angle-deg 90 \
  --speed 2.5 \
  --max-time 12 \
  --reflection-mode elastic
```

## Stadium: Centerline Two-Cycle

A centerline launch between the stadium endcaps. This one is periodic but unstable under perturbation.

```bash
PYTHONPATH=src python src/cli.py \
  --geometry stadium \
  --width 12 \
  --height 6 \
  --ball-radius 0.35 \
  --start-x 6 \
  --start-y 3 \
  --launch-angle-deg 0 \
  --speed 3 \
  --max-time 12 \
  --reflection-mode elastic
```

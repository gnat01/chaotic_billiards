# Chaotic Billiards: Project Scaffolding

## Purpose

This document defines the repository scaffold for building the chaotic billiards project described in `notes.md`. It is intentionally implementation-facing: directories, files, module boundaries, data contracts, and the order in which the scaffold should be filled in.

## Repository Layout

```text
chaotic_billiards/
  README.md
  pyproject.toml
  notes.md
  scaffold.md
  .gitignore
  src/
    chaotic_billiards/
      __init__.py
      config.py
      types.py
      geometry/
        __init__.py
        base.py
        polygon.py
        circle.py
        stadium.py
        sinai.py
        irregular.py
      physics/
        __init__.py
        state.py
        collision.py
        reflection.py
        dissipation.py
        propagation.py
      simulation/
        __init__.py
        engine.py
        recorder.py
        sampler.py
        stopping.py
      metrics/
        __init__.py
        basic.py
        divergence.py
        sections.py
        occupancy.py
      visualization/
        __init__.py
        trajectories.py
        comparisons.py
        energy.py
        animation.py
      presets/
        __init__.py
        regular.py
        chaotic.py
        dissipative.py
      experiments/
        __init__.py
        periodic_orbits.py
        sensitivity.py
        geometry_comparison.py
        dissipation_comparison.py
      cli.py
  tests/
    test_polygon_reflection.py
    test_circle_reflection.py
    test_energy_conservation.py
    test_dissipation.py
    test_stadium_runs.py
    test_sinai_runs.py
    test_presets.py
  outputs/
    plots/
    animations/
    data/
  notebooks/
    01_baseline_geometries.ipynb
    02_chaotic_examples.ipynb
    03_dissipation.ipynb
```

## Top-Level Files

### `README.md`

Should contain:

- project purpose
- setup instructions
- how to run a named preset
- how to generate plots and animations
- explanation that some geometries are controls, not chaotic exemplars

### `pyproject.toml`

Should define:

- package metadata
- Python version
- dependencies
- optional dev dependencies
- CLI entry point

Minimal dependency target:

- `numpy`
- `matplotlib`
- `pytest`

Optional later:

- `scipy`
- `pandas`
- `imageio`
- `jupyter`

### `.gitignore`

Should ignore:

- `__pycache__/`
- `.pytest_cache/`
- `.venv/`
- `outputs/`
- notebook checkpoints

## Package Structure

Use `src/chaotic_billiards/` as the import root.

### `config.py`

Central location for:

- numerical tolerances
- default output directories
- default plotting parameters
- max collision counts
- default simulation horizon

### `types.py`

Shared dataclasses and aliases for:

- `Vec2`
- `BallState`
- `CollisionEvent`
- `SimulationConfig`
- `DissipationConfig`
- `RunResult`
- `MetricSeries`

Keep these light and stable so the rest of the package shares one vocabulary.

Do not include angular position, spin, or angular velocity in the first version.

## Geometry Layer

This layer answers:

- is the ball center in a valid position for a given radius?
- where is the next ball-boundary contact?
- what is the outward normal at the contact point?

### `geometry/base.py`

Define abstract interfaces:

- `contains_ball(center, radius) -> bool`
- `first_contact(center, velocity, radius) -> CollisionEvent | None`
- `normal_at(contact_point) -> Vec2`
- `bounding_box() -> tuple[float, float, float, float]`
- `name` property

The geometry layer should treat the rendered table boundary and the valid center-path boundary as related but distinct concepts.

### `geometry/polygon.py`

Responsible for:

- generic convex polygon support first
- line-segment boundary storage
- inward offset support for finite ball radius
- center-path contact against edges and corners
- flat-wall normals

Use this to implement:

- square
- rectangle
- triangle
- diamond
- irregular polygon

### `geometry/circle.py`

Responsible for:

- circle contact for a finite-radius ball
- radial normal computation

### `geometry/stadium.py`

Responsible for:

- Bunimovich stadium boundary model
- segment plus semicircle composition
- dispatching intersection queries to sub-boundaries

### `geometry/sinai.py`

Responsible for:

- outer polygon boundary
- circular obstacle
- choosing the earliest valid ball contact across outer and inner boundaries

### `geometry/irregular.py`

Initially support:

- one irregular polygon preset

Later support:

- smooth parametric boundaries if needed

## Physics Layer

This layer handles motion and collision updates.

### `physics/state.py`

Should define the particle state object:

- position
- radius
- velocity
- time
- collision count
- alive or active flag

Do not store:

- angular velocity
- orientation
- rotational energy

### `physics/collision.py`

Responsible for:

- asking the current geometry for the next ball contact
- filtering numerical self-collisions
- returning a normalized collision event

The event should distinguish:

- center position at impact time
- geometric contact point on the wall or obstacle
- boundary normal

### `physics/reflection.py`

Responsible for:

- elastic specular reflection
- inelastic wall reflection
- restitution parameters

Keep reflection math isolated so it can be tested independently.

With a rigid disk and fixed-orientation walls, translational reflection is still straightforward. Spin, rolling, and rotational dynamics should remain out of scope unless explicitly added later.

### `physics/dissipation.py`

Responsible for:

- drag during free flight
- kinetic energy helpers
- velocity updates between collisions

This file should not know about geometry details.

### `physics/propagation.py`

Responsible for:

- advancing state to a target event time
- optionally sampling intermediate centers for visualization
- applying drag during free motion

## Simulation Layer

This layer turns geometry and physics into reproducible runs.

### `simulation/engine.py`

Main event loop:

- initialize state
- find next collision
- advance to that collision
- apply reflection
- record outputs
- stop on configured conditions

### `simulation/recorder.py`

Responsible for collecting:

- states over time
- collision events
- sampled center positions
- rendered ball outlines only when needed by visualization
- summary metadata

### `simulation/sampler.py`

Responsible for:

- resampling event-based motion into evenly spaced visualization samples
- decoupling display frames from physics events

### `simulation/stopping.py`

Provide stopping rules such as:

- max simulation time
- max collisions
- min speed threshold
- escaped domain for future open billiards

## Metrics Layer

This layer computes analysis outputs from a completed run.

### `metrics/basic.py`

Compute:

- speed series
- kinetic energy series
- path length
- collisions per unit time
- summary statistics

### `metrics/divergence.py`

Compute:

- pairwise trajectory separation
- log separation
- finite-time Lyapunov estimate

Keep the API explicit that this is a finite-time estimate, not a proof of chaos.

### `metrics/sections.py`

Compute:

- return-map samples
- Poincare-like section data for selected boundaries or surfaces

### `metrics/occupancy.py`

Compute:

- spatial occupancy grid
- coarse-grained entropy
- optional exploratory box-counting support

## Visualization Layer

This layer turns runs and metrics into figures.

### `visualization/trajectories.py`

Produce:

- single-run path plots
- geometry outlines
- finite-radius ball overlays
- periodic trajectory figures

### `visualization/comparisons.py`

Produce:

- overlaid nearby trajectories
- regular vs chaotic side-by-side figures
- multi-geometry comparisons

### `visualization/energy.py`

Produce:

- energy versus time
- speed versus time
- collision rate summaries

### `visualization/animation.py`

Produce:

- animated path renderings
- visible moving billiard ball render
- optional side-by-side animation for trajectory divergence

Keep animation code separate from physics so rendering complexity does not leak into the core engine.

## Presets Layer

This layer defines named scenarios that users can run without assembling components manually.

### `presets/regular.py`

Should include:

- square periodic orbit
- rectangle rational-slope orbit
- circle symmetric orbit

### `presets/chaotic.py`

Should include:

- stadium nearby-initial-condition divergence
- Sinai benchmark run

### `presets/dissipative.py`

Should include:

- square with drag
- stadium with inelastic walls
- one direct elastic vs dissipative comparison

Each preset should return:

- geometry
- initial ball state
- simulation config
- plotting hints

Presets should set a radius explicitly rather than relying on a hidden default.

## Experiments Layer

This layer contains higher-level scripts that produce end-user outputs.

### `experiments/periodic_orbits.py`

Runs and saves:

- regular geometry demos
- periodic trajectory plots

### `experiments/sensitivity.py`

Runs and saves:

- paired nearby trajectories
- divergence plots
- regular vs chaotic comparison figures

### `experiments/geometry_comparison.py`

Runs and saves:

- same initial-speed comparisons across multiple geometries
- summary tables or figure panels

### `experiments/dissipation_comparison.py`

Runs and saves:

- elastic vs drag
- elastic vs inelastic-wall
- combined dissipation comparison plots

## CLI

### `cli.py`

Provide a minimal command-line interface like:

```text
python -m chaotic_billiards.cli run --preset square_periodic
python -m chaotic_billiards.cli run --preset stadium_divergence
python -m chaotic_billiards.cli experiment sensitivity
```

Initial commands:

- `run --preset <name>`
- `experiment <name>`
- `list-presets`

The CLI should write plots and data to `outputs/`.

## Test Scaffold

Tests should be in place early, even before all geometry variants exist.

### `test_polygon_reflection.py`

Validate:

- angle of incidence equals angle of reflection on flat walls
- square and rectangle collisions preserve speed in elastic mode
- the finite-radius ball does not cross the wall boundary
- no hidden rotational state is required anywhere in the simulation path

### `test_circle_reflection.py`

Validate:

- radial normal use
- symmetric circle examples behave as expected
- changing radius shifts contact timing correctly

### `test_energy_conservation.py`

Validate:

- elastic no-drag runs conserve energy within tolerance

### `test_dissipation.py`

Validate:

- drag reduces speed monotonically when configured
- inelastic collisions reduce energy at impacts

### `test_stadium_runs.py`

Validate:

- stadium runs complete without invalid geometry or collision errors

### `test_sinai_runs.py`

Validate:

- obstacle collisions are detected correctly
- outer and inner boundaries are both active

### `test_presets.py`

Validate:

- every named preset is runnable
- every preset produces a consistent config object

## Data Flow

Use this end-to-end flow:

1. A preset or experiment constructs a geometry, initial state, and config.
2. The simulation engine advances the billiard ball event by event.
3. The recorder stores trajectory and collision history.
4. Metric modules compute summaries from the recorded run.
5. Visualization modules generate figures or animations.
6. The CLI or notebook saves outputs into `outputs/`.

## Fill Order

Implement the scaffold in this order:

1. `types.py`, `config.py`, `geometry/base.py`, `physics/state.py`
2. `geometry/polygon.py`, `physics/reflection.py`, `physics/collision.py`
3. `physics/propagation.py`, `simulation/engine.py`, `simulation/recorder.py`
4. `metrics/basic.py`, `visualization/trajectories.py`
5. `presets/regular.py`, `cli.py`, baseline tests
6. `geometry/circle.py`, `geometry/stadium.py`, `geometry/sinai.py`
7. `metrics/divergence.py`, `visualization/comparisons.py`
8. `physics/dissipation.py`, `visualization/energy.py`, dissipative presets
9. `experiments/*.py`, animation support, notebooks

## Minimum First Cut

If the goal is to stand up a usable skeleton quickly, create these files first:

- `pyproject.toml`
- `src/chaotic_billiards/types.py`
- `src/chaotic_billiards/geometry/base.py`
- `src/chaotic_billiards/geometry/polygon.py`
- `src/chaotic_billiards/physics/state.py`
- `src/chaotic_billiards/physics/reflection.py`
- `src/chaotic_billiards/physics/collision.py`
- `src/chaotic_billiards/simulation/engine.py`
- `src/chaotic_billiards/simulation/recorder.py`
- `src/chaotic_billiards/metrics/basic.py`
- `src/chaotic_billiards/visualization/trajectories.py`
- `src/chaotic_billiards/presets/regular.py`
- `src/chaotic_billiards/cli.py`
- `tests/test_polygon_reflection.py`
- `tests/test_energy_conservation.py`

That is enough to support square and rectangle trajectories with elastic collisions and basic plotting.

Even in the first cut, treat the moving object as a finite-radius ball so the collision API and plots do not need to be redesigned later.

## Non-Goals For The Scaffold

Do not bake these into the first scaffold:

- over-general smooth-boundary geometry abstractions
- open billiards or escape-time machinery
- fractal-dimension analysis as a first-class required module
- optimization for very large parameter sweeps
- UI complexity beyond a small CLI and notebooks

## Summary

This scaffold keeps the project split into:

- geometry definition
- physical update rules
- event-driven simulation
- metrics
- visualization
- presets and experiments

That separation is enough to build the simple regular cases first, then extend into chaotic and dissipative regimes without rewriting the core engine.

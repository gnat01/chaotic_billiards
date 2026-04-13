# Chaotic Billiards: End-to-End Scope

## Goal

Build an end-to-end chaotic billiards project that can:

- simulate billiard motion inside multiple table geometries
- visualize trajectories, including periodic and chaotic-looking behavior
- compare nearby initial conditions to show sensitive dependence
- support both conservative and dissipative variants
- track a useful set of dynamical metrics
- provide a clear progression from simple baseline systems to genuinely chaotic ones

The project should not treat every geometry as chaotic. Some shapes are controls or baselines and are useful precisely because they are regular or integrable.

## Core Questions

The project should answer these questions:

- How do trajectories differ across geometries?
- Which setups produce periodic or quasi-periodic motion?
- Which setups exhibit strong sensitivity to initial conditions?
- How does dissipation change long-run behavior?
- Which metrics are robust enough to compute and visualize well?

## System Definition

Model a finite-radius billiard ball moving in straight lines inside a closed 2D domain.

Use a ball radius `r > 0`, not a point-mass idealization. This is the better choice here for two reasons:

- it is closer to the actual billiards intuition
- it produces much better visual output because the moving object and its near-wall behavior read clearly on screen

Numerically, this means the simulated center of the ball moves inside the geometry eroded inward by radius `r`, or equivalently the collision system must compute contact between the finite ball and the original table boundary.

For now, treat the ball as a translating disk only:

- no spin
- no rolling
- no angular momentum
- no rotational kinetic energy

That keeps the model simpler and is enough for the visual and dynamical goals of this project.

At boundary collision:

- `elastic` mode: specular reflection, speed preserved
- `inelastic_wall` mode: specular reflection with reduced normal/tangential speed according to a restitution rule

During free motion:

- `no_drag` mode: speed constant between collisions
- `drag` mode: speed decays continuously over time or distance

These should be configurable independently. "Inelastic scattering" and "energy loss while moving" are different mechanisms and should not be merged into one vague setting.

## Geometry Set

Include the geometries from the original note, but classify them by purpose.

### Baseline / regular cases

- square
- rectangle
- circle
- equilateral or isosceles triangle
- diamond / rhombus

These are useful for:

- validating collision handling
- showing periodic trajectories
- contrasting regular motion against chaotic motion

### Chaotic or more interesting cases

- stadium billiard
- Sinai billiard (square or rectangle with circular obstacle)
- Bunimovich-style deformations
- irregular polygon
- smooth irregular boundary

The original note mentioned "irregular"; this should be made concrete as at least one polygonal irregular table and one smooth nontrivial table.

## Minimum Viable Physics

Start with the simplest defensible model:

- finite-radius rigid disk in 2D
- translation only, no rotational state
- 2D position and velocity
- fixed ball radius as a first step
- exact or numerically stable wall intersection
- specular reflection for elastic collisions
- fixed time step only for visualization, not for collision detection if avoidable

Preferred approach:

- use event-based collision handling where possible
- compute the next ball-boundary contact event
- advance directly to the collision
- then update velocity

This avoids major artifacts from naive time stepping.

For polygons, the simplest robust approach is to evolve the center against an inward-offset table boundary. For circles and curved boundaries, compute contact using the ball radius explicitly.

## Dissipative Variants

Support these variants explicitly:

1. `elastic + no_drag`
2. `elastic + drag`
3. `inelastic_wall + no_drag`
4. `inelastic_wall + drag`

Expected outcomes:

- elastic systems preserve kinetic energy
- drag collapses long-run motion toward rest
- inelastic wall collisions reduce energy at impacts
- combined dissipation may produce rapid settling or attractor-like path concentration

All of these statements refer only to translational kinetic energy in the current scope.

## Metrics

Track the original metrics, but tighten definitions.

### Required metrics

- position over time
- velocity over time
- speed over time
- kinetic energy over time
- collision count
- collisions per unit time
- path length

### Recommended chaos-related metrics

- separation between two nearby trajectories
- finite-time Lyapunov estimate
- recurrence or return-map statistics
- distribution of incidence/reflection angles

### Optional advanced metrics

- Poincare section samples
- escape time, if open billiards are later added
- occupancy heatmap
- coarse-grained entropy

### De-scope or treat carefully

- "fractal dimension of trajectory traced"

This should not be a default headline metric. If included, define it narrowly as a box-counting dimension estimate of the visited set under a specific sampling rule, and present it as exploratory rather than canonical.

## Demonstrations To Include

The project should produce these concrete demos.

### 1. Periodic trajectories

Show periodic or nearly periodic paths in:

- square
- rectangle
- circle

Examples:

- rational-slope orbit in a square
- symmetric orbit in a circle

### 2. Sensitive dependence to initial conditions

Launch two particles with nearly identical initial conditions and plot:

- both trajectories overlaid
- distance between states over time
- log separation versus time when meaningful

Do this in:

- a baseline regular geometry
- a chaotic geometry such as stadium or Sinai

The contrast is the goal.

### 3. Geometry comparison

Hold initial speed and comparable initial conditions fixed and compare:

- qualitative path structure
- collision frequency
- energy behavior
- finite-time instability indicators

### 4. Dissipation comparison

For the same geometry and initial condition, compare:

- elastic vs inelastic wall collisions
- no drag vs drag

Show:

- energy decay curves
- number of bounces before settling
- final resting behavior

## Numerical and Modeling Constraints

To keep the project credible:

- separate simulation time from visualization frame rate
- validate reflection laws against known simple cases
- avoid calling a system chaotic based only on a tangled-looking path
- state clearly when a metric is heuristic

For regular polygonal geometries, expect many trajectories to be periodic or structured. Do not oversell them as chaotic examples.

## Suggested Architecture

Use a modular structure like this:

```text
chaotic_billiards/
  src/
    geometry.py
    dynamics.py
    collision.py
    metrics.py
    simulation.py
    visualization.py
    experiments.py
    presets.py
  outputs/
    plots/
    animations/
    data/
  notes.md
```

### Module responsibilities

- `geometry.py`: boundary definitions, normals, intersection helpers
- `collision.py`: next-hit computation and reflection updates
- `dynamics.py`: drag and inelastic rules
- `simulation.py`: main integrator / event loop
- `metrics.py`: Lyapunov estimate, collision stats, energy stats
- `visualization.py`: trajectory plots, overlays, animations, heatmaps
- `experiments.py`: reproducible runs and parameter sweeps
- `presets.py`: named scenarios for demos

## Milestones

### Phase 1: Baseline simulator

- implement square and rectangle
- support elastic collisions
- verify periodic trajectories
- output simple trajectory plots

Success criterion:

- trajectories reflect correctly and preserve speed up to numerical tolerance

### Phase 2: More geometries

- add circle, triangle, diamond
- validate collisions in each geometry
- build preset initial conditions that show structured motion

Success criterion:

- each geometry has at least one reproducible demo trajectory

### Phase 3: Chaotic exemplars

- add stadium billiard
- add Sinai billiard
- add one irregular polygon or smooth irregular boundary
- implement nearby-trajectory comparison

Success criterion:

- clear visual contrast between regular and chaotic cases

### Phase 4: Dissipation

- add wall inelasticity
- add drag during free motion
- compare decay behavior across regimes

Success criterion:

- energy decay plots and trajectory changes are reproducible and interpretable

### Phase 5: Metrics and analysis

- finite-time Lyapunov estimate
- bounce rate statistics
- occupancy heatmaps
- Poincare-style sections where applicable

Success criterion:

- metrics are stable enough to compare across runs

### Phase 6: Presentation layer

- notebook or CLI presets
- exportable figures
- optional animation rendering
- concise write-up explaining which cases are regular vs chaotic

Success criterion:

- a new user can run named demos and reproduce the main figures

## Deliverables

The end-to-end project should produce:

- a reusable simulator
- a small set of named geometry presets
- plots of trajectories and energy curves
- side-by-side comparisons of nearby initial conditions
- at least one animation for a regular case and one for a chaotic case
- a short technical note explaining model assumptions and metric definitions

## Validation Plan

Use these checks:

- speed conservation in elastic no-drag runs
- correct reflection angles on flat walls for the ball center trajectory
- known symmetric or periodic trajectories in square/circle
- monotone energy decrease in dissipative runs
- stable qualitative behavior under smaller plotting step sizes

Add ball-specific checks:

- the ball never visually penetrates the boundary
- corner and curved-wall contacts remain numerically stable
- changing ball radius changes accessible motion in expected ways

## Risks

- naive time stepping may miss collisions or create fake chaos
- finite-radius corner handling can be trickier than point-particle geometry
- poorly defined irregular boundaries may make collision handling brittle
- Lyapunov estimates can be noisy and misleading if renormalization is not handled carefully
- fractal-dimension claims can become hand-wavy unless tightly specified

## Recommended Initial Scope

If this needs to be scoped tightly for a first version, build:

- square
- circle
- stadium
- Sinai
- elastic mode
- optional drag
- trajectory plots
- ball-rendered trajectory and animation output
- nearby-trajectory divergence plot
- energy and bounce-rate metrics

Leave these for later:

- fractal dimension estimates
- highly general smooth irregular boundaries
- heavy parameter sweeps
- advanced statistical analysis

## Summary

This project should be framed as a progression:

- start from regular billiards
- use a visible finite-radius ball, not an invisible point abstraction
- add reliable geometry handling
- introduce chaotic benchmark geometries
- compare nearby initial conditions
- then add dissipation and analysis metrics

That gives a defensible chaotic billiards project instead of a loose collection of visual ideas.

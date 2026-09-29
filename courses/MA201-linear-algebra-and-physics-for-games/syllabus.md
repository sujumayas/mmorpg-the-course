# MA201 — Linear Algebra and Physics for Games

Year 2, semester 3 · 4 credits · Prerequisites: MA101

Vectors, matrices, transforms and Newtonian motion — the math under 3D worlds and movement.

## Learning outcomes

- Use matrices for transforms between spaces
- Implement integration for motion and understand its errors
- Build collision detection and response for simple shapes

## Schedule

| Week | Topic | Lecture | Example |
|---|---|---|---|
| 1 | Vectors in 3D, cross product | [lecture](lectures/w01-vectors-in-3d-and-the-cross-product.md) | [walkable-slope](examples/w01-walkable-slope.html) |
| 2 | Matrices and linear transformations | [lecture](lectures/w02-matrices-and-linear-transformations.md) | [isometric-basis](examples/w02-isometric-basis.html) |
| 3 | Transform hierarchies: local and world space | [lecture](lectures/w03-transform-hierarchies-local-and-world-space.md) | [parent-scale-shear](examples/w03-parent-scale-shear.html) |
| 4 | Homogeneous coordinates and projection | [lecture](lectures/w04-homogeneous-coordinates-and-projection.md) | [fov-frustum](examples/w04-fov-frustum.html) |
| 5 | Quaternions for rotation (intuition first) | [lecture](lectures/w05-quaternions-for-rotation.md) | [slerp-long-way](examples/w05-slerp-long-way.html) |
| 6 | Kinematics: position, velocity, acceleration | [lecture](lectures/w06-kinematics-position-velocity-acceleration.md) | [moving-platform](examples/w06-moving-platform.html) |
| 7 | Numerical integration: Euler vs semi-implicit vs Verlet | [lecture](lectures/w07-numerical-integration-euler-semi-implicit-verlet.md) | [orbit-integrators](examples/w07-orbit-integrators.html) |
| 8 | Forces, mass, drag | [lecture](lectures/w08-forces-mass-and-drag.md) | [terminal-velocity](examples/w08-terminal-velocity.html) |
| 9 | Collision detection: spheres, AABB, SAT | [lecture](lectures/w09-collision-detection-spheres-aabb-sat.md) | [sat-projections](examples/w09-sat-projections.html) |
| 10 | Collision response and impulses | [lecture](lectures/w10-collision-response-and-impulses.md) | [impulse-bounce](examples/w10-impulse-bounce.html) |
| 11 | Spatial partitioning: grids and quadtrees | [lecture](lectures/w11-spatial-partitioning-grids-and-quadtrees.md) | [cell-size-tradeoff](examples/w11-cell-size-tradeoff.html) |
| 12 | Raycasting | [lecture](lectures/w12-raycasting.md) | [grid-raycaster](examples/w12-grid-raycaster.html) |
| 13 | Projectile motion and aiming at moving targets | [lecture](lectures/w13-projectile-motion-and-aiming-at-moving-targets.md) | [lead-the-target](examples/w13-lead-the-target.html) |
| 14 | Determinism and floating point | [lecture](lectures/w14-determinism-and-floating-point.md) | [far-from-origin](examples/w14-far-from-origin.html) |
| 15 | Final exam + physics sandbox | [assessments](#assessment-materials) | — |

## Signature worked examples

- Explicit Euler orbit spirals outward; semi-implicit stays stable — side-by-side
- Lead-the-target: solve the intercept quadratic for a moving archer target

## Labs

- [MA201 · Lab 01: Floor, wall or ceiling](labs/lab01.md)
- [MA201 · Lab 02: The isometric picker](labs/lab02.md)
- [MA201 · Lab 03: Local and world space](labs/lab03.md)
- [MA201 · Lab 04: A software camera](labs/lab04.md)
- [MA201 · Lab 05: A quaternion toolkit](labs/lab05.md)
- [MA201 · Lab 06: Moving frames](labs/lab06.md)
- [MA201 · Lab 07: Three integrators and an energy meter](labs/lab07.md)
- [MA201 · Lab 08: A force accumulator and three drag models](labs/lab08.md)
- [MA201 · Lab 09: A narrow phase with contacts](labs/lab09.md)
- [MA201 · Lab 10: An impulse resolver](labs/lab10.md)
- [MA201 · Lab 11: Grids, quadtrees and a world boss](labs/lab11.md)
- [MA201 · Lab 12: A grid raycaster and a hitscan check](labs/lab12.md)
- [MA201 · Lab 13: The archer's aim](labs/lab13.md)
- [MA201 · Lab 14: Precision budget and a determinism harness](labs/lab14.md)

## Assessment materials

- [MA201 exam bank](assessments/exam-bank.md)
- [MA201 final exam brief](assessments/final-exam-brief.md)
- [MA201 problem sets brief](assessments/problem-sets-brief.md)
- [MA201 physics sandbox brief](assessments/sandbox-brief.md)

## Readings

- Millington — Game Physics Engine Development (selected)
- Dunn & Parberry — 3D Math Primer, ch. 3-8

## Assessment

Problem sets (40%), sandbox (30%), final (30%)

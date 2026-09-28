# MA101 — Mathematics for Games I: Algebra, Functions & Trigonometry

Year 1, semester 1 · 4 credits · Prerequisites: none

The math that sits inside every stat sheet and every movement script: functions, curves, trig and vectors.

## Learning outcomes

- Model game quantities with linear, polynomial, exponential, logarithmic and rational functions
- Choose a curve shape to produce a desired feel (growth, diminishing returns, caps)
- Use trigonometry for rotation, aiming and circular motion
- Use 2D vectors for movement, direction and distance

## Schedule

| Week | Topic | Lecture | Example |
|---|---|---|---|
| 1 | Functions as machines: input stat, output effect | [lecture](lectures/w01-functions-as-machines.md) | [stat-machine](examples/w01-stat-machine.html) |
| 2 | Linear functions and rates (damage per level) | [lecture](lectures/w02-linear-functions-and-rates.md) | [flat-growth](examples/w02-flat-growth.html) |
| 3 | Polynomials and quadratic curves (jump arcs) | [lecture](lectures/w03-polynomials-and-quadratic-curves.md) | [jump-designer](examples/w03-jump-designer.html) |
| 4 | Exponentials: growth and the XP curve | [lecture](lectures/w04-exponentials-and-the-xp-curve.md) | [xp-curve](examples/w04-xp-curve.html) |
| 5 | Logarithms: 'how many levels until…' | [lecture](lectures/w05-logarithms-how-many-levels-until.md) | [afford-curve](examples/w05-afford-curve.html) |
| 6 | Rational functions and asymptotes: A/(A+K) | [lecture](lectures/w06-rational-functions-and-asymptotes.md) | [armor-curve](examples/w06-armor-curve.html) |
| 7 | Piecewise functions, caps and floors | [lecture](lectures/w07-piecewise-caps-and-floors.md) | [soft-cap-curve](examples/w07-soft-cap-curve.html) |
| 8 | Interpolation: lerp, inverse lerp, remap | [lecture](lectures/w08-interpolation-lerp-inverse-lerp-remap.md) | [remap-squash](examples/w08-remap-squash.html) |
| 9 | Easing curves for animation feel | [lecture](lectures/w09-easing-curves-for-animation-feel.md) | [easing-race](examples/w09-easing-race.html) |
| 10 | Angles, radians, sin/cos — orbiting and aiming | [lecture](lectures/w10-angles-radians-sin-cos.md) | [orbit-and-waves](examples/w10-orbit-and-waves.html) |
| 11 | atan2 and turning toward a target | [lecture](lectures/w11-atan2-turning-toward-a-target.md) | [turn-toward-target](examples/w11-turn-toward-target.html) |
| 12 | 2D vectors: add, scale, magnitude, normalize | [lecture](lectures/w12-2d-vectors.md) | [diagonal-movement](examples/w12-diagonal-movement.html) |
| 13 | Dot product: facing, field of view cones | [lecture](lectures/w13-dot-product-facing-and-vision-cones.md) | [vision-cone](examples/w13-vision-cone.html) |
| 14 | Distances and ranges: circles, squared distance trick | [lecture](lectures/w14-distances-ranges-and-squared-distance.md) | [range-rings](examples/w14-range-rings.html) |
| 15 | Final exam + curve-design mini project | [assessments](#assessment-materials) | — |

## Signature worked examples

- Armor / (Armor + K): mitigation curve vs effective HP line (League of Legends K=100, WoW K=400+85·level) — the course's anchor example
- RuneScape XP curve: why level 92 is halfway to 99 (verified: 6,517,253 of 13,034,431 XP)
- Diagonal movement bug: why un-normalized WASD is ~41% faster
- Dot product vision cone: stealth guard that 'sees' 60° ahead

## Labs

- [MA101 · Lab 01: Build a stat machine](labs/lab01.md)
- [MA101 · Lab 02: Fit, compare and cross](labs/lab02.md)
- [MA101 · Lab 03: Jump designer](labs/lab03.md)
- [MA101 · Lab 04: Build and tune an XP curve](labs/lab04.md)
- [MA101 · Lab 05: The "how many until" calculator](labs/lab05.md)
- [MA101 · Lab 06: Asymptote audit](labs/lab06.md)
- [MA101 · Lab 07: Stat curves with caps and floors](labs/lab07.md)
- [MA101 · Lab 08: Remap everything](labs/lab08.md)
- [MA101 · Lab 09: An easing library and a juicy menu](labs/lab09.md)
- [MA101 · Lab 10: Orbits and bursts](labs/lab10.md)
- [MA101 · Lab 11: Turrets that turn](labs/lab11.md)
- [MA101 · Lab 12: A movement controller you can trust](labs/lab12.md)
- [MA101 · Lab 13: Guard vision](labs/lab13.md)
- [MA101 · Lab 14: Range queries](labs/lab14.md)

## Assessment materials

- [MA101 exam bank](assessments/exam-bank.md)
- [MA101 curve-design project brief](assessments/curve-design-project-brief.md)
- [MA101 midterm and final brief](assessments/midterm-and-final-brief.md)
- [MA101 problem sets brief](assessments/problem-sets-brief.md)
- [MA101 · Lab grading key (labs 13 and 14)](assessments/lab-grading-key.md)

## Readings

- Dunn & Parberry — 3D Math Primer for Graphics and Game Development, ch. 1-2
- Freya Holmér — Math for Game Devs lecture series (video)

## Assessment

Problem sets (40%), curve-design project (20%), midterm (15%), final (25%)

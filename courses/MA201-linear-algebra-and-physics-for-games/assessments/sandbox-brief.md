# MA201 physics sandbox brief

**Weight:** 30% of the course grade.
**Work:** pairs. One mark for the pair, except the individual viva (5 points) and any adjustment from the contribution statement.
**When:** weeks 10 to 15. Milestones at the end of weeks 10 and 12, final submission 48 hours before the week 15 session, showcase in that session.
**Related:** [problem sets](problem-sets-brief.md), [exam bank](exam-bank.md), [final exam](final-exam-brief.md).

## What you build

A small 2D physics sandbox in Python that puts the whole course in one program. Bodies fall, collide, bounce, slide and stack. A player can cast rays into the scene. A turret aims at moving targets. The simulation replays bit for bit from a seed and an input log. A design document explains every number you chose.

Most of the code already exists in your labs. The sandbox is where those pieces meet, and where you find out which of them you trusted too early.

| Piece | Comes from | Lecture |
|---|---|---|
| Transforms for oriented boxes, local and world space | [Lab 03](../labs/lab03.md) | [week 3](../lectures/w03-transform-hierarchies-local-and-world-space.md) |
| Fixed-timestep integrator (semi-implicit Euler, or Verlet with a reason) | [Lab 07](../labs/lab07.md) | [week 7](../lectures/w07-numerical-integration-euler-semi-implicit-verlet.md) |
| `Body`, force accumulator, drag as a coefficient in 1/s | [Lab 08](../labs/lab08.md) | [week 8](../lectures/w08-forces-mass-and-drag.md) |
| Narrow phase with normal and depth (circles, oriented boxes, SAT) | [Lab 09](../labs/lab09.md) | [week 9](../lectures/w09-collision-detection-spheres-aabb-sat.md) |
| Impulse resolver, restitution threshold, friction clamp, positional correction | [Lab 10](../labs/lab10.md) | [week 10](../lectures/w10-collision-response-and-impulses.md) |
| Broad phase (grid or quadtree) | [Lab 11](../labs/lab11.md) | [week 11](../lectures/w11-spatial-partitioning-grids-and-quadtrees.md) |
| Raycasts (grid walk, sphere, slab) | [Lab 12](../labs/lab12.md) | [week 12](../lectures/w12-raycasting.md) |
| Intercept aim and dodge budget | [Lab 13](../labs/lab13.md) | [week 13](../lectures/w13-projectile-motion-and-aiming-at-moving-targets.md) |
| Precision budget and per-tick state hash | [Lab 14](../labs/lab14.md) | [week 14](../lectures/w14-determinism-and-floating-point.md) |

### Technical rules

- Python 3.13 with the standard library only, run with the course interpreter `.venv/bin/python`. Draw with `tkinter` (part of the standard library) or write frames to an SVG or HTML file. `matplotlib` is allowed for plots in the design document, not in the sandbox.
- The sandbox must run headless. Markers run `sandbox.py --check` on a clean copy of your folder. Code that only runs on your machine (an absolute path, a missing file) counts as failing.
- Physics runs on a fixed timestep with an accumulator (CS101 week 9), whatever the drawing frame rate. State the tick rate in the README.
- Dynamic bodies are circles and oriented boxes. Static geometry may also use boxes and line segments.
- Rotation from impulses is optional. The core grade needs boxes that can be placed at any angle and kinematic bodies that rotate at a set rate. Dynamic bodies may keep a fixed orientation, the choice Minecraft makes for its entities. If you add spin, use the week 10 section 6 denominator and say so.
- Contact points. Week 9 section 4 describes Box2D's reference-face and incident-face clipping. You do not have to write it, and you are not expected to link Box2D itself. One contact point at the deepest vertex along the MTV is enough for the core grade. The two-point clip is an extension.

### Required checks

`sandbox.py --check` prints PASS or FAIL for each check below, with the measured number, and exits with status 1 if any fails. The expected values come from the lectures.

| Check | Scene | Passes when |
|---|---|---|
| `orbit` | Body at (1, 0), velocity (0, 1), inverse-square gravity with GM = 1 (week 7), 60 steps per orbit, 10 orbits | Largest energy error below 0.01 (the week 7 table gives 0.0055 for semi-implicit) |
| `stop_shot` | Two 0.17 kg circles, 2 m/s into rest, `e = 0.95` | Final velocities 0.050 and 1.950 m/s to within 0.001 |
| `momentum` | 200 random two-body collisions, random masses, normals and `e` | Total momentum unchanged to 1e-9, energy lost matches `½ μ (1 − e²) v_n²` to 1e-9 |
| `sat` | Week 9 cases 1 and 2 | Case 1 separated, case 2 normal (0.7071, 0.7071) and depth 0.1515 to 1e-4 |
| `drop` | Ball dropped 1 m, `e = 0.8`, threshold 1 m/s | Bounce count within one of the week 10 model's 7, and the README explains any difference |
| `stack` | Five 1 m boxes stacked on a static floor, 10 s | Top box drifts less than 2 cm, every box ends slower than 0.01 m/s |
| `broadphase` | 500 random circles, your broad phase plus narrow phase | Same overlapping pairs as brute force |
| `raycast` | Week 12 sphere and box cases | `t` of 9.6 and 5.657 to 1e-3, a miss where the lecture has one |
| `aim` | Week 13 TF2 scout row | Flight time 0.9759 s and aim point (1000.0, 390.4) |
| `replay` | Your busiest scene, 60 s from a seed and a recorded input log, run twice | Identical per-tick hashes of the full state for all ticks |

### Required scenes

Three scenes at least, selectable with `--scene NAME` and drawable in the window.

1. **A collision scene with rotated boxes.** For example a crate tower knocked over by a ball, or a pinball table. It must show the contact normal and depth as a debug overlay.
2. **A raycast interaction.** For example mouse picking, a line-of-sight check between guards and a player, or a hitscan tool that pushes what it hits.
3. **An aiming agent.** A turret or archer that uses the intercept quadratic against moving targets, with a switch between body aim, the one-step estimate and the exact solve, and a hit-rate readout.

Every scene has an overlay with total kinetic energy, total momentum, the tick number and the current state hash. Engines you will work with ship this kind of overlay, and the energy line catches the wrong integrator in seconds (week 7 section 5).

### Extensions

Extensions are marked under the criterion they belong to and cannot lift a criterion above full marks. Good choices are angular response with spin, the two-point contact clip, a quadtree with a live world-boss style crowd, a floating origin demonstrated 600 km from the origin with the float32 staircase from week 14, drag with mass (quadratic drag as a force), and swept tests for fast bullets.

## Deliverables

Submitted as one folder named `sandbox-<surname1>-<surname2>`:

- `sandbox.py` and its modules, and a `README.md` of at most one page. The README gives the run commands, the tick rate, the controls, and the output of `--check` pasted in.
- `replays/`, with the input log and seed used by the `replay` check.
- A design document of at most six pages (PDF), with the sections below.
- A screen recording of at most two minutes showing the three required scenes.
- A contribution statement of at most 150 words, signed by both partners, saying who wrote which parts.

### Design document sections

1. **World and units.** World size, units, tick rate, largest speed and slowest mover.
2. **Integrator and stability.** Your integrator, why, and the stiffest spring or strongest drag your tick rate can hold, with the `ω·dt < 2` and `c·h < 1` numbers from labs 07 and 08.
3. **Drag and materials.** Drag coefficients in 1/s with terminal speeds and 90% times, your combine rule, a material table, and the bounce counts and first bounce heights it gives (lab 10's method).
4. **Collision pipeline.** Shapes, the number of SAT axes per pair type, the broad phase with its cell size or capacity, and measured candidate pairs per tick against brute force (lab 11's method).
5. **Precision and determinism.** The lab 14 precision budget for your world, the representation you chose for positions and time, the rules you follow for replay, and the result of the `replay` check.
6. **What is still wrong.** At least two behaviors you know are wrong or fragile, each with a measured number and the fix you would make with another week. Honest entries here earn marks.

## Milestones

| Milestone | Due | What you hand in | Marks |
|---|---|---|---|
| M1, proposal | end of week 10 | One page: the pair, the three scenes, which lab code you will reuse, world size and tick rate, and the two risks you expect | 2 |
| M2, vertical slice | end of week 12 | Headless run of circles and boxes falling onto a floor with the lab 10 resolver on a fixed timestep, and `--check` passing `orbit`, `stop_shot`, `momentum` and `sat` | 3 |
| Final | 48 hours before the week 15 session | Everything in Deliverables | 90 |
| Viva | week 15 session | Individual, see below | 5 |

Milestones get written feedback within a week. A milestone handed in late earns 0 of its marks but still gets feedback.

## Showcase and viva

In the week 15 session each pair demos its sandbox for five minutes, live from the submitted folder. Then each student answers questions alone for five minutes. The questions point at your own code and your own design document, in the style of the [exam bank](exam-bank.md). Typical questions:

- "Show the line where velocity is updated. Which integrator is this, and what happens to the orbit if I swap these two lines?"
- "Your mud has `c = 60` per second. What does your damping formula do at 20 Hz?"
- "Drop this ball from 2 m. Before you run it, how many bounces does your material table predict?"
- "The `replay` check passed. Name one change to this code that would make it fail on another machine."

## Rubric

Each criterion is scored in bands. A criterion earns its full points in the Excellent band, 60 to 80% of them in Adequate, and 0 to 40% in Weak, at the marker's judgment within the band.

| Criterion | Points | Excellent | Adequate | Weak |
|---|---|---|---|---|
| Automated checks | 20 | All ten checks pass on a clean copy with `.venv/bin/python` | Seven to nine pass | Six or fewer pass, or `--check` does not run |
| Collision pipeline | 15 | Contacts, response and broad phase work together in the scenes; debug overlay shows normals and depths; measured pair counts in the document | Works in the scenes with visible jitter or sinking the document does not explain | Bodies tunnel, stick or explode in a required scene |
| Motion and forces | 10 | Fixed timestep with accumulator; force accumulator with drag in 1/s; energy overlay behaves as week 7 predicts | Motion correct, drag or timestep handled ad hoc | Frame-rate dependent motion or energy that climbs without explanation |
| Queries and agents | 10 | Raycast interaction and aiming agent both work, with three aim modes and a hit-rate readout | One of the two complete | Both missing or broken |
| Determinism and precision | 10 | `replay` passes; the state hash covers every value the next tick reads; precision budget applied to the world with a chosen representation | Replay passes with gaps in the hash, or the budget is generic | Replay fails or is missing |
| Design document | 20 | All six sections, every choice backed by a number the pair measured or computed, honest "still wrong" section | Complete but some choices unsupported | Sections missing, or claims without numbers |
| Showcase demo | 5 | Runs live from the submitted folder, the three scenes shown, clear narration | Runs with a restart or a missing scene | Does not run |
| Milestones | 5 | M1 (2) and M2 (3) on time and complete | One late or incomplete | Both missing |
| Individual viva | 5 | Explains own code and numbers, predicts a result before running it | Explains the code, cannot predict | Cannot explain the submitted work |
| **Total** | **100** | | | |

## Late work, integrity and adjustments

- The final submission may be up to 48 hours late with 10 points off. After that it is marked for feedback only and scores 0, because the showcase needs it.
- You may reuse any lecture code, lab starter code and your own lab solutions. Code from other pairs, or from a physics library, is not allowed in the sandbox. You may read Box2D's source to understand a technique and must cite what you read in the design document.
- You may use documentation, forums and AI assistants to understand an error or an idea, and you must list that help in one line in the README. You may not submit code you cannot explain in the viva.
- If the contribution statement or the viva shows a clearly uneven split, the instructor may move up to 20 points between the partners' marks after talking to both.

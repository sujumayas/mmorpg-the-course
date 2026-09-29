# MA201 · Week 09 — Collision Detection: Spheres, AABB and SAT

**Why this matters:** In CS101 your hitboxes never turned. The moment a crate tumbles, a door swings or a sword rotates, the four-comparison box test gives wrong answers, and the fix every physics engine uses is one idea: look for a line that separates the two shapes. This week you learn that idea, the separating axis test, well enough to write it, to read it in an engine's source, and to hand week 10 the two numbers response needs, the contact normal and the penetration depth.

**You will be able to:**
- Compute sphere-sphere and AABB-AABB overlap in 3D, including the contact normal and penetration depth.
- Compute the projection radius of a rotated box onto any axis, and use it to run the separating axis test (SAT) for two oriented rectangles by hand.
- Derive the minimum translation vector from a SAT result and state which way it must point.
- List the candidate axes SAT needs for two boxes in 3D (15) and for two convex polygons, and explain why SAT does not work on concave shapes.

**Before class:** Dunn & Parberry, *3D Math Primer for Graphics and Game Development* (2nd ed.), chapter 9, the sections on bounding volumes and intersection tests (spheres and AABBs). Ericson, C. *Real-Time Collision Detection* (2005), chapter 4, section 4.4 on oriented bounding boxes, if your library has it. Reread CS101 week 10, sections 2 and 3.

**Prerequisites from earlier courses:** [CS101 week 10, collision basics](../../CS101-programming-for-games-i/lectures/w10-collision-basics-aabb-and-circles.md) (the four-comparison AABB test as two interval tests, circles with squared distance, circle-versus-box by clamping, minimum push-out, tunneling). This lecture assumes all of it. [MA101 week 13, the dot product](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w13-dot-product-facing-and-vision-cones.md) (`v · û` as the length of `v`'s shadow on a unit direction). [MA101 week 14, squared distance](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w14-distances-ranges-and-squared-distance.md). [MA201 week 1, the cross product](w01-vectors-in-3d-and-the-cross-product.md) (a vector perpendicular to two others), used in section 5. [MA201 week 3, local and world space](w03-transform-hierarchies-local-and-world-space.md), for a box's axes written in world coordinates.

**Interactive:** [`examples/w09-sat-projections.html`](../examples/w09-sat-projections.html). Keep it open during section 3.

---

## 1. What detection has to hand over

A collision system works in two phases. The **broad phase** finds pairs of objects that *might* touch, cheaply, using a grid or a tree. That is week 11. The **narrow phase** takes each candidate pair and answers exactly. This week is the narrow phase.

In CS101 the narrow phase answered yes or no, and then pushed the player out along the shallower axis. Week 10 of this course needs more. For each overlapping pair it needs:

- the **contact normal** `n`, a unit vector pointing from shape A toward shape B, along the direction that separates them with the least movement;
- the **penetration depth** `d`, how far they overlap along `n`;
- a **contact point** where they touch, for spin.

The pair `(n, d)` together is the **minimum translation vector** (MTV): move B by `d·n` (or A by `−d·n`, or each by half) and they stop overlapping. Every test in this lecture returns an MTV, not just a boolean.

Two terms you will need. A shape is **convex** if the straight segment between any two of its points stays inside it. Circles, spheres, boxes, capsules and triangles are convex. An L-shaped room or a star is **concave**: some segments between its points leave the shape. Everything in this lecture works only on convex shapes. Section 6 says what engines do about the rest.

## 2. Spheres and axis-aligned boxes in 3D

These are CS101's tests with a third coordinate. The only new work is producing the MTV.

### Sphere against sphere

Two spheres with centers `c_A`, `c_B` and radii `r_A`, `r_B` overlap when `|c_B − c_A|² < (r_A + r_B)²`, exactly as for circles. On a hit, and only on a hit, take one square root to build the MTV:

```
d_vec  = c_B − c_A
normal = d_vec / |d_vec|
depth  = r_A + r_B − |d_vec|
```

```python
import math

def spheres(ca, ra, cb, rb):
    d = [cb[i] - ca[i] for i in range(3)]
    dist2 = sum(x * x for x in d)
    if dist2 >= (ra + rb) ** 2:
        return None
    dist = math.sqrt(dist2)                 # one square root, only on a hit
    normal = [x / dist for x in d]
    return [round(x, 4) for x in normal], round(ra + rb - dist, 4)

print(spheres((0, 0, 0), 1.0, (1.2, 0.9, 0.0), 0.8))
print(spheres((0, 0, 0), 1.0, (1.2, 0.9, 0.8), 0.8))
```

```
([0.8, 0.6, 0.0], 0.3)
([0.7059, 0.5294, 0.4706], 0.1)
```

Check the first line. The offset is `(1.2, 0.9, 0)`, its squared length is `1.44 + 0.81 = 2.25`, so the distance is 1.5. The radii sum to 1.8, so the depth is 0.3 and the normal is `(1.2, 0.9, 0) / 1.5 = (0.8, 0.6, 0)`. In the second line the offset `(1.2, 0.9, 0.8)` has squared length 2.89, distance 1.7, depth 0.1.

One trap. If the two centers coincide, `dist` is 0 and the normal is undefined. Engines pick an arbitrary fixed direction (often straight up) for that case. Your code must too, or it divides by zero on the first frame two objects spawn in the same place.

### AABB against AABB

In 3D, an **axis-aligned bounding box** is a center `c` and three half-extents `(h_x, h_y, h_z)`. CS101 showed that two boxes overlap exactly when their intervals overlap on x **and** on y. Add z and you are done: three interval tests. Written with centers and half-extents, each axis becomes one comparison:

```
overlap on axis i   ⇔   |c_B,i − c_A,i| < h_A,i + h_B,i
depth on axis i     =   h_A,i + h_B,i − |c_B,i − c_A,i|
```

The MTV is the axis with the smallest depth, pointed from A toward B by the sign of `c_B,i − c_A,i`. That is CS101's "push along the shallower axis", now with a third axis.

### Sphere against AABB

Clamp the sphere's center into the box, one coordinate at a time, to get the closest point `p`. The sphere overlaps if `|c − p|² < r²`. The normal is `(c − p) / |c − p|`, pointing from the box toward the sphere, and the depth is `r − |c − p|`. This is CS101's circle-against-box test with one more clamp. For a box that is rotated, first move the sphere's center into the box's local space (week 3), clamp there, and move the result back.

## 3. Worked example: when a rotated crate gets a false hit

### The hook

Minecraft never rotates an entity's bounding box, as you saw in CS101 week 10. A mob turns, its box doesn't. That choice is what makes four comparisons enough. Physics games cannot make it. A crate knocked off a shelf tumbles, a plank lands at an angle, a car rolls. So what does a general-purpose engine do when two boxes are rotated?

Godot 4's built-in 2D physics answers in a file called `godot_collision_solver_2d_sat.cpp`. For two rectangles it tests exactly four directions, two from each box, and stops at the first one that shows a gap. Before those four, it retries whichever direction separated the pair on the previous frame. The idea behind those four directions is the separating axis test, and the rest of this section is that idea.

First, why not just keep using AABBs? Take a 2 × 2 crate rotated 45°. Its tightest axis-aligned box is 2.83 × 2.83, twice the area of the crate. Put it near a wall and the AABB test reports a hit while the player sees a clear gap. That is the false hit this example fixes.

### The model

**The separating axis theorem.** Two convex shapes do not overlap if and only if there is some direction such that, when both shapes are projected onto a line in that direction, their shadows do not overlap. Such a direction is a **separating axis**.

"Projected onto a line" means flattening each shape into an interval, exactly the step CS101 used for AABBs on x and y. You already know how to compute one point's shadow on a unit direction `n`: it is the dot product `p · n`. The theorem turns one 2D question into several 1D ones.

The theorem would be useless if you had to try every direction. You don't. For two convex polygons in 2D, if any separating axis exists, then one of the polygons' **edge normals** is a separating axis. A rectangle has four edges but only two different normal directions, so two rectangles need at most **four** axis tests. That is Godot's four.

**The projection of a box.** A rotated box has a center `c`, two unit axes `u` and `v` (its local x and y written in world coordinates, week 3), and half-extents `h_u`, `h_v`. Its shadow on a unit axis `n` is an interval centered at `c · n` with half-width

```
r = h_u · |u · n| + h_v · |v · n|
```

Each half-extent contributes the length of its shadow on `n`. The absolute values are there because a shadow length is never negative. When `n` is the world x axis and the box is unrotated, this gives `r = h_u`, the CS101 case.

**The test on one axis.** With `d = c_B − c_A`, the two intervals overlap on axis `n` when

```
|d · n|  <  r_A(n) + r_B(n)
overlap on n  =  r_A(n) + r_B(n) − |d · n|
```

If the overlap is zero or negative on any candidate axis, that axis separates the shapes: stop, there is no collision. If all candidate axes show positive overlap, the shapes collide, and the axis with the **smallest** overlap gives the MTV. Its depth is that overlap. Its normal is that axis, flipped if needed so that it points from A toward B, that is, so that `d · n > 0`.

That is the whole algorithm. For two rectangles, four dot products for `d · n`, a few more for the radii, four comparisons.

### Numbers you can check

Box A is axis-aligned at the origin with half-extents `(2, 1)`, so its axes are `u_A = (1, 0)` and `v_A = (0, 1)`. Box B is a 2 × 2 square (half-extents `(1, 1)`) rotated 45°, so `u_B = (0.7071, 0.7071)` and `v_B = (−0.7071, 0.7071)`, where `0.7071 = √2/2`.

The four radii, which don't depend on where B is:

| Axis `n` | `r_A(n)` | `r_B(n)` | Sum |
|---|---|---|---|
| `(1, 0)` | 2 | `0.7071 + 0.7071 = 1.4142` | 3.4142 |
| `(0, 1)` | 1 | 1.4142 | 2.4142 |
| `(0.7071, 0.7071)` | `2 × 0.7071 + 1 × 0.7071 = 2.1213` | 1 | 3.1213 |
| `(−0.7071, 0.7071)` | 2.1213 | 1 | 3.1213 |

**Case 1: B centered at `(3.0, 1.5)`.** First the AABB check. B's axis-aligned box has half-extents 1.4142 on both axes, so it spans x from 1.586 to 4.414 and y from 0.086 to 2.914. A spans x from −2 to 2 and y from −1 to 1. The intervals overlap on both axes, so an AABB test says **hit**.

Now SAT, with `d = (3.0, 1.5)`:

| Axis `n` | `|d · n|` | `r_A + r_B` | Overlap |
|---|---|---|---|
| `(1, 0)` | 3.0000 | 3.4142 | +0.4142 |
| `(0, 1)` | 1.5000 | 2.4142 | +0.9142 |
| `(0.7071, 0.7071)` | `4.5 × 0.7071 = 3.1820` | 3.1213 | **−0.0607** |

The third axis separates them by 0.0607. The gap sits between B's lower-left face and A's top-right corner `(2, 1)`: that corner projects to `3 × 0.7071 = 2.1213` on the axis, and B's face sits at `3.1820 − 1 = 2.1820`. SAT stops here: **no collision**. The false hit is gone.

**Case 2: B centered at `(2.8, 1.4)`.** Now `d = (2.8, 1.4)`:

| Axis `n` | `|d · n|` | `r_A + r_B` | Overlap |
|---|---|---|---|
| `(1, 0)` | 2.8000 | 3.4142 | +0.6142 |
| `(0, 1)` | 1.4000 | 2.4142 | +1.0142 |
| `(0.7071, 0.7071)` | `4.2 × 0.7071 = 2.9698` | 3.1213 | **+0.1515** |
| `(−0.7071, 0.7071)` | `1.4 × 0.7071 = 0.9899` | 3.1213 | +2.1314 |

All four overlap, so the boxes collide. The smallest overlap is 0.1515 on `(0.7071, 0.7071)`, and `d · n` is positive, so the MTV is normal `(0.7071, 0.7071)`, depth 0.1515. Pushing B 0.1515 along that diagonal separates them. Note what CS101's push-out rule would have done with the same boxes treated as AABBs: its smallest overlap is on x, so it shoves B sideways by a larger amount, in a direction that has nothing to do with the face that is actually touching.

The code below runs as shown and prints both cases:

```python
import math

def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]

def box(center, half_w, half_h, angle_deg):
    t = math.radians(angle_deg)
    u = (math.cos(t), math.sin(t))      # the box's local x axis, in world space
    v = (-math.sin(t), math.cos(t))     # the box's local y axis
    return {"c": center, "h": (half_w, half_h), "axes": (u, v)}

def radius_on(b, n):
    (u, v), (hw, hh) = b["axes"], b["h"]
    return hw * abs(dot(u, n)) + hh * abs(dot(v, n))

def sat(a, b):
    d = (b["c"][0] - a["c"][0], b["c"][1] - a["c"][1])
    best = None
    for n in a["axes"] + b["axes"]:
        dist = abs(dot(d, n))
        overlap = radius_on(a, n) + radius_on(b, n) - dist
        print(f"  axis ({n[0] + 0:+.4f}, {n[1] + 0:+.4f})  |d.n|={dist:.4f}  "
              f"rA+rB={radius_on(a, n) + radius_on(b, n):.4f}  overlap={overlap:+.4f}")
        if overlap <= 0:
            return "separated"
        if best is None or overlap < best[0]:
            sign = 1 if dot(d, n) >= 0 else -1          # point the normal from A to B
            best = (overlap, (sign * n[0], sign * n[1]))
    depth, normal = best
    return f"overlap: normal ({normal[0]:.4f}, {normal[1]:.4f}), depth {depth:.4f}"

a = box((0, 0), 2, 1, 0)
for center in ((3.0, 1.5), (2.8, 1.4)):
    print(f"B at {center}:")
    print(" ", sat(a, box(center, 1, 1, 45)))
```

```
B at (3.0, 1.5):
  axis (+1.0000, +0.0000)  |d.n|=3.0000  rA+rB=3.4142  overlap=+0.4142
  axis (+0.0000, +1.0000)  |d.n|=1.5000  rA+rB=2.4142  overlap=+0.9142
  axis (+0.7071, +0.7071)  |d.n|=3.1820  rA+rB=3.1213  overlap=-0.0607
  separated
B at (2.8, 1.4):
  axis (+1.0000, +0.0000)  |d.n|=2.8000  rA+rB=3.4142  overlap=+0.6142
  axis (+0.0000, +1.0000)  |d.n|=1.4000  rA+rB=2.4142  overlap=+1.0142
  axis (+0.7071, +0.7071)  |d.n|=2.9698  rA+rB=3.1213  overlap=+0.1515
  axis (-0.7071, +0.7071)  |d.n|=0.9899  rA+rB=3.1213  overlap=+2.1314
  overlap: normal (0.7071, 0.7071), depth 0.1515
```

(The `+ 0` in the print turns Python's `−0.0` into `0.0` so the table reads cleanly.)

### The visual

Open the interactive. Two rectangles sit on a canvas: A in one color, B in another. Around the canvas, four axis lines are drawn, one per candidate direction, each with the two shapes' shadows as colored bars and their shared part highlighted. Beside each axis is its row from the table: `|d · n|`, the radius sum and the overlap.

Load the "Case 1" preset. The shapes look like they touch. The AABB toggle draws B's axis-aligned box, which clearly overlaps A. Now look at the diagonal axis: its two bars have a visible gap, and its row is red. Drag B slowly down and left along the diagonal. The gap closes at exactly the moment the corner of A touches B's face, and the MTV arrow appears on the diagonal. Rotate B with the slider (or the Q and E keys) and watch the four axis lines turn with it. The axis that holds the smallest overlap jumps from one to another as you rotate, and the MTV arrow jumps with it.

The one thing to take away: a collision is the absence of any gap on every candidate axis. One gap anywhere is enough to say no.

### Cross-game recognition

**Godot 4 (built-in 2D physics, `modules/godot_physics_2d/godot_collision_solver_2d_sat.cpp`, master branch, 4.x, checked September 2026).** `_collision_rectangle_rectangle` calls `test_axis` on the two columns of A's transform (its local x and y axes in world space), then on B's two columns, and returns as soon as one of them separates. `test_axis` projects both shapes, checks for a gap, and otherwise keeps the axis with the smallest depth as `best_axis`, flipping its sign to keep it pointing consistently. That is our algorithm line for line. Two engine details go beyond it. First, `test_previous_axis` tries the axis that separated the pair last frame before anything else. Objects move a little per frame, so last frame's gap is usually still a gap, and the test exits after one axis. This is called **frame coherence**. Second, `test_axis` handles a zero-length axis by substituting an upward one, the same trap as the coincident sphere centers in section 2.

**Box2D (version 3.1.1, `src/manifold.c`).** `b2CollidePolygons` computes "edge separation using the separating axis test (SAT)", in the words of its own comment. `b2FindMaxSeparation` loops over every edge normal of one polygon, finds the other polygon's deepest vertex along it, and keeps the largest separation. It is called twice, once in each direction. Box2D polygons must be convex, with at most 8 vertices (`B2_MAX_POLYGON_VERTICES`). Box2D does not stop when a gap appears. It reports small positive separations too, as "speculative" contacts, so the solver can prepare for a hit that is about to happen.

**3D oriented boxes (Gottschalk, Lin and Manocha, "OBBTree", SIGGRAPH 1996).** In 3D, face normals are not enough. Two boxes can also be separated by a plane that runs along one edge of each. The paper counts the candidates: 3 face directions from each box plus the 3 × 3 cross products of one box's edge directions with the other's, **15 axes** in total. It reports that the whole test takes fewer than 200 operations in practice, and that most disjoint pairs exit after only a few axes.

**CS101's four comparisons.** The AABB test from CS101 week 10 is SAT with the axes fixed to x and y. Because neither box rotates, both boxes share the same two axes, and each test reduces to one comparison of intervals. Minecraft's choice not to rotate boxes is really a choice to run SAT with two free axes instead of four in 2D (or three instead of 15 in 3D).

Four implementations, one idea: project both shapes on a short list of directions, and a single gap means no collision.

### Eyes-open design judgment

- **Pick the cheapest shape that fits.** A sphere or capsule test is one distance, an AABB test is three comparisons, a 3D box test is up to 15 axes, and a general convex hull more. Use spheres for things that roll or should feel fair from every angle, boxes for crates and buildings, hulls only when a player can see and feel the difference.
- **SAT needs convex shapes.** A concave shape, such as an L-shaped wall, can have no separating axis among its edge normals and still not overlap. Engines split concave shapes into convex pieces (Godot's `CollisionPolygon2D` does this in its default `BUILD_SOLIDS` mode) or use triangle meshes for static level geometry. Budget for the decomposition, because more pieces mean more pairs.
- **The MTV answers "shortest way out", not "the way it came in".** For a fast object that sank deep into a thin wall, the shortest way out can be through the far side. That is tunneling's cousin from CS101 week 10. Keep steps small relative to thickness, or use a swept test.
- **Exit early, and remember the last separating axis.** Order candidate axes so the likeliest separator comes first, and cache the separating axis per pair as Godot does. In a scene where most pairs are close but not touching, that turns four or 15 tests into one.
- **Tolerance is a design decision.** Should touching count? Box2D reports contacts slightly *before* they touch. CS101 used strict comparisons so tiles don't snag. Decide, and use the same rule in every test.

## 4. From SAT to a contact for week 10

Week 10's impulse formula takes the normal and depth straight from SAT. Two details matter when you hand them over.

**Direction.** The normal must point from A to B. Our code flips the axis so that `d · n > 0`. Get this backwards and week 10's response pulls the bodies together instead of apart. A cheap test: after computing the MTV, move B by `depth · n` and run SAT again. It should report an overlap of about zero on that axis.

**The contact point.** For spin, response also needs where the shapes touch. For a box against a box, the usual method finds the **reference face** (the face on the MTV axis belonging to the box that owns that axis) and the **incident face** (the face of the other box most opposite to the normal), then clips the incident face against the sides of the reference face. Box2D's `b2ClipPolygons` does exactly this and returns up to two points in 2D. The [physics sandbox](../assessments/sandbox-brief.md) does not ask you to write the clipper or to link Box2D. For the core grade, one contact point is enough: the vertex of the incident box that pushes deepest into the reference box along the MTV normal. In case 2 the diagonal axis belongs to B, so A is the incident box, and its deepest vertex is the corner `(2, 1)`, the A vertex with the largest `p · n`. The two-point clip is an extension. Either way, the point comes from the SAT axis, not from separate math.

## 5. SAT in 3D: 15 axes and where they come from

Moving from 2D to 3D adds one new kind of candidate axis, and it comes from the cross product (week 1).

For two convex polyhedra, SAT's candidate axes are:

1. every face normal of A,
2. every face normal of B,
3. the cross product of every edge direction of A with every edge direction of B.

The third group handles the edge-on-edge case. Picture two boxes that approach each other with one edge crossing another, like a plus sign seen from the side. No face of either box faces the other, yet the plane through both edges separates them. Its normal is perpendicular to both edges, which is the definition of their cross product.

A box has 3 distinct face directions and 3 distinct edge directions, which happen to be the same three axes. So two boxes need `3 + 3 + 3 × 3 = 15` axes. The projection radius generalizes the 2D one with a third term, `r = h_u·|u · n| + h_v·|v · n| + h_w·|w · n|`.

**The parallel-edge trap.** If an edge of A is parallel to an edge of B, their cross product is the zero vector. Normalizing it divides by zero, and even an almost-parallel pair gives a tiny vector whose direction is mostly rounding error. Skip any cross-product axis whose length is below a small tolerance (Ericson suggests adding a small epsilon to the radius terms for the same reason). A face axis already covers the parallel case, so nothing is lost.

| Pair | Candidate axes |
|---|---|
| Sphere, sphere | 1 (the line between centers) |
| AABB, AABB (3D) | 3 |
| Box, box (3D) | 15 |
| Convex polygons with `m` and `k` edges (2D) | up to `m + k` |
| Convex polyhedra with `F_A`, `F_B` faces and `E_A`, `E_B` edge directions | `F_A + F_B + E_A·E_B` |

The last row explains why engines avoid general convex hulls in bulk. Two hulls with 20 edge directions each need 400 cross-product axes before face axes. Engines switch to other algorithms for those (GJK, which Box2D uses for its distance queries, is the usual one, and a later course covers it).

## 6. Choosing shapes for a game

Detection is where performance and fairness meet. A few rules of thumb:

- **Characters:** capsules or boxes that don't rotate. They slide along walls cleanly and the test is cheap. Characters rarely need to tip over.
- **Projectiles:** spheres or rays (week 12). If they are fast, sweep them.
- **Props that tumble:** boxes and convex hulls with SAT, since rotation is the point.
- **Level geometry:** static triangle meshes or convex pieces, tested only against nearby objects thanks to the broad phase.
- **Hitboxes for combat:** several small spheres or capsules along a limb or blade, not one rotated box. Each sphere test is one squared distance, and a sphere looks the same at every angle, so the limb can rotate freely at no extra cost.

## In-class activity (25 minutes)

Work in pairs with paper, a calculator and the interactive.

1. (8 min) Box A: center `(0, 0)`, half-extents `(3, 1)`, not rotated. Box B: center `(3.5, 1.8)`, half-extents `(1, 0.5)`, rotated 30° (`u_B = (0.8660, 0.5)`, `v_B = (−0.5, 0.8660)`). Compute all four projection radii for both boxes, then `|d · n|` on each axis. Do they collide? If yes, give the MTV.
2. (7 min) Load your boxes into the interactive's custom preset and check every number. Then rotate B, first toward 0° and then toward 90°, until the result flips. Record both angles and which axis separates at each.
3. (10 min) A designer wants a spinning saw blade (a 12-pointed star) as a hazard. Propose two collision representations, one cheap and one accurate, count the SAT axes each needs against a player box, and name one gameplay consequence of choosing the cheap one.

Expected output: the four-row table with the verdict and MTV, the flip angle, and the two proposals with axis counts.

## Common misconceptions

- **"If the AABBs overlap, the objects overlap."** An AABB around a rotated object can double its area. AABB overlap is a broad-phase filter, not a verdict.
- **"SAT has to try every direction."** For convex polygons, the edge normals are enough. For 3D boxes, 15 axes are enough.
- **"The smallest overlap is always the right push."** It is the shortest push. For deep or fast penetrations, it can point out of the wrong side. Keep penetrations shallow.
- **"SAT works for any shape."** Only for convex ones. A concave shape must be split into convex pieces first.

## Check yourself

1. Sphere A at `(1, 2, 2)` with radius 1.5, sphere B at `(3, 3, 4)` with radius 1.7. Do they overlap? If yes, give the normal and depth.
2. A 4 × 2 box (half-extents `(2, 1)`) is rotated 30°. What is its projection radius on the world x axis, and on the world y axis? What are the half-extents of its AABB?
3. In case 2 of the worked example, a teammate's code returns the normal `(−0.7071, −0.7071)`. What went wrong, and what happens in week 10's response if nobody notices?
4. How many SAT axes are needed for a box against a triangular prism in 3D? (A triangular prism has 5 faces with 4 distinct face directions, and 9 edges with 4 distinct edge directions.)

<details>
<summary>Answers</summary>

1. `d = (2, 1, 2)`, `|d|² = 9`, so `|d| = 3`. The radii sum to 3.2 and `9 < 10.24`, so they overlap. Normal `(2, 1, 2)/3 = (0.667, 0.333, 0.667)`, depth `3.2 − 3 = 0.2`.
2. `u = (0.8660, 0.5)`, `v = (−0.5, 0.8660)`. On x: `2 × 0.8660 + 1 × 0.5 = 2.232`. On y: `2 × 0.5 + 1 × 0.8660 = 1.866`. Those are the AABB half-extents, so the AABB is 4.46 × 3.73.
3. The sign flip was skipped or reversed: the normal must satisfy `d · n > 0`, and `d = (2.8, 1.4)`. With the reversed normal, week 10 treats the bodies as approaching when they are separating and vice versa, so the impulse pulls them further into each other or sticks them together.
4. Face directions: 3 for the box plus 4 for the prism = 7. Edge cross products: 3 × 4 = 12. Total 19 axes, minus any that come out parallel (skip zero-length cross products).

</details>

## Lab / assignment hook

[Lab 09, a narrow phase with contacts](../labs/lab09.md). You implement sphere-sphere, AABB-AABB and oriented-box SAT tests in Python, each returning a normal and depth, pass tests built from this lecture's tables, then measure how often an AABB-only test gives false hits for boxes at random angles. Deliverable: passing code, a false-hit chart and a 250-word shape recommendation for a named game object. The contacts feed week 10's impulse lab.

## Sources

- Godot Engine source, `modules/godot_physics_2d/godot_collision_solver_2d_sat.cpp` (master branch, version 4.8-dev, checked September 2026). `_collision_rectangle_rectangle` tests the two transform columns of each rectangle; `test_axis` projects, returns on a gap, keeps the smallest depth as `best_axis`, and substitutes an upward axis for a zero-length one; `test_previous_axis` retries the last separating axis. https://github.com/godotengine/godot/blob/master/modules/godot_physics_2d/godot_collision_solver_2d_sat.cpp
- Box2D, version 3.1.1 (June 2025), `src/manifold.c` (`b2FindMaxSeparation`, `b2CollidePolygons` with its SAT comment and speculative distance, `b2ClipPolygons`) and `include/box2d/collision.h` (convex polygons, `B2_MAX_POLYGON_VERTICES` 8). https://github.com/erincatto/box2d
- Gottschalk, S., Lin, M. C. & Manocha, D. (1996). "OBBTree: A Hierarchical Structure for Rapid Interference Detection". *Proceedings of SIGGRAPH 96*. The 15 candidate axes for two OBBs; fewer than 200 operations per test. http://gamma.cs.unc.edu/SSV/obb.pdf
- Minecraft Wiki, "Hitbox" (Java Edition), as cited in CS101 week 10: entity boxes keep a fixed orientation.
- Ericson, C. (2005). *Real-Time Collision Detection*. Morgan Kaufmann. Chapter 4 (OBB tests, robustness epsilon for parallel edges).
- Godot Engine class reference, `CollisionPolygon2D`, `build_mode` default `BUILD_SOLIDS` (convex decomposition), master branch 2026. https://github.com/godotengine/godot/blob/master/doc/classes/CollisionPolygon2D.xml
- Box2D 3.1.1, `src/distance.c`: GJK for distance between convex shapes.
- Dunn, F. & Parberry, I. (2011). *3D Math Primer for Graphics and Game Development* (2nd ed.). CRC Press. Chapter 9.

## Interactive spec: examples/w09-sat-projections.html

**Purpose.** Show that two convex shapes collide exactly when every candidate axis shows overlapping shadows, and that one gap on one axis is enough to say no. The insight made obvious: the AABB view says "hit" in case 1 while the diagonal axis shows a visible gap. Two linked views: the shapes (look like they touch) and the projection strips (reveal the gap).

**Layout.** Mobile-first. Main canvas: world −6 to 6 on x, −4 to 4 on y, y up, light grid every 1 unit. Box A (accent color) and box B (second color) drawn filled at 30% opacity with solid outlines, centers marked. Below the canvas on narrow screens, to the right on wide: four projection strips, one per candidate axis, in the order A's u, A's v, B's u, B's v. Each strip is a horizontal number line labelled with its axis vector to 4 decimals, showing A's interval and B's interval as colored bars (center `c·n`, half-width `r`), the shared part highlighted, or the gap shaded red with its width printed. Also, on the canvas itself, draw each axis as a faint line through the origin in its direction, with the shadows as thick bars on it (toggle "draw axes on canvas", default on for wide screens, off for narrow).

**Table.** Under the strips, a four-row table: axis, `|d · n|`, `r_A`, `r_B`, `r_A + r_B`, overlap (signed, 4 decimals). The row with the first non-positive overlap is marked "separating axis"; if none, the row with the smallest overlap is marked "MTV". A result line reads either "No collision: separated on axis (…) by g" or "Collision: normal (nx, ny), depth d".

**Model.** Box: center `c`, half-extents `(hw, hh)`, angle `θ`. `u = (cos θ, sin θ)`, `v = (−sin θ, cos θ)`. `r(n) = hw·|u·n| + hh·|v·n|`. `d = c_B − c_A`. Overlap on `n` = `r_A(n) + r_B(n) − |d·n|`. MTV normal = smallest-overlap axis, sign chosen so `d·n > 0`. Test all four axes for the table even after a gap is found (the table is for learning), but show which axis an early-exit implementation would stop at.

**Controls.**
- Drag either box by its body; drag a small handle on each box to rotate it. Keyboard: Tab selects a box, arrows move 0.1 (Shift 0.01), Q and E rotate by 5° (Shift 1°).
- Sliders for the selected box: angle −90° to 90°, half-width 0.25 to 3, half-height 0.25 to 3.
- "Show AABB of B" toggle: draws B's axis-aligned box (half-extents `r_B((1,0))`, `r_B((0,1))`) dashed, and a badge "AABB test: hit / no hit" beside the SAT result, with a warning "AABB false hit" when they disagree.
- "Show MTV" toggle: draws the arrow `depth·n` from B's center; a "Resolve" button moves B by it (animated over 300 ms, instant under `prefers-reduced-motion`), after which the table shows overlap 0.0000 on that axis.
- Presets: "Case 1" (A: `(0,0)`, `(2,1)`, 0°; B: `(3.0,1.5)`, `(1,1)`, 45°), "Case 2" (B at `(2.8,1.4)`), "Activity" (A: `(0,0)`, `(3,1)`, 0°; B: `(3.5,1.8)`, `(1,0.5)`, 30°; expected result "Collision: normal (0.0000, 1.0000), depth 0.1330"; turning B below about 20° separates them), "Plus sign" (A: `(0,0)`, `(3,0.4)`, 0°; B: `(0,0)`, `(0.4,3)`, 0°), "Custom".

**Test values (must match to 4 decimals).**
- Case 1: rows `(1,0)` 3.0000 / 3.4142 / +0.4142; `(0,1)` 1.5000 / 2.4142 / +0.9142; `(0.7071,0.7071)` 3.1820 / 3.1213 / −0.0607; result "No collision"; AABB badge "hit", warning shown.
- Case 2: overlaps +0.6142, +1.0142, +0.1515, +2.1314; result "Collision: normal (0.7071, 0.7071), depth 0.1515". After Resolve, B's center is `(2.9071, 1.5071)` and the diagonal row shows 0.0000.
- Radii for B at 45°: `r_B` on `(1,0)` and `(0,1)` is 1.4142; `r_A` on the diagonals is 2.1213.

**First screen.** Case 1 loaded, AABB toggle on, the red gap on the diagonal strip and the "AABB false hit" warning visible without any interaction.

**Accessibility and style.** Everything operable by keyboard with visible focus; a live region announces the result line on change. Pass/fail shown by text and icon as well as color. Respect `prefers-color-scheme` and `prefers-reduced-motion`. Use the shared tokens from `templates/interactive-tokens.css`, inlined. No game art: rectangles, lines and labels only.

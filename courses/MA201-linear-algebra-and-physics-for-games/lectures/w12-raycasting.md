# MA201 · Week 12 — Raycasting

**Why this matters:** "What is in that direction, and how far away?" is the question behind every hitscan gun, every line-of-sight check, every mouse click on a 3D object, every foot that finds the ground and every camera that stops before a wall. A raycast answers it. This week you write the three raycasts engines use most (against a grid, a sphere and a box), learn why they fail at the edges, and see how one shipped game drew its entire 3D view with nothing else.

**You will be able to:**
- Write a ray as `p(t) = o + t d` and compute the first hit against a grid, a sphere and an axis-aligned box.
- Trace a ray through a grid cell by cell by hand, and explain why its cost depends on distance travelled rather than on the number of walls.
- Derive the perpendicular-distance correction for a raycast renderer and predict the fisheye distortion without it.
- Diagnose the standard raycast failures (starting inside, parallel rays, grazing hits, sampled walks that skip corners) and choose a fix.

**Before class:** Dunn & Parberry, *3D Math Primer for Graphics and Game Development* (2nd ed.), chapter 9 section on rays, and Appendix A, the sections on ray against sphere and ray against AABB (free at gamemath.com). Amanatides, J. & Woo, A. (1987), "A Fast Voxel Traversal Algorithm for Ray Tracing", *Eurographics '87*, sections 1 to 3 (four pages).

**Prerequisites from earlier courses:** [MA101 week 3, polynomials and quadratics](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w03-polynomials-and-quadratic-curves.md) (the quadratic formula and the discriminant). [MA101 week 13, the dot product](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w13-dot-product-facing-and-vision-cones.md) (projection onto a direction). [MA201 week 1, vectors in 3D](w01-vectors-in-3d-and-the-cross-product.md). [MA201 week 4, projection](w04-homogeneous-coordinates-and-projection.md) (on-screen size is proportional to one over depth). [MA201 week 11, spatial partitioning](w11-spatial-partitioning-grids-and-quadtrees.md) (the grid this week's ray walks through). [MA201 week 9, collision detection](w09-collision-detection-spheres-aabb-sat.md) (AABB overlap).

**Interactive:** [`examples/w12-grid-raycaster.html`](../examples/w12-grid-raycaster.html). Keep it open during section 2.

---

## 1. A ray is a line with a start and a direction

A **ray** is every point you reach by starting at an **origin** `o` and moving some distance along a **direction** `d`:

```
p(t) = o + t d,    t ≥ 0
```

- `o` is a point (the gun barrel, the eye, the character's feet).
- `d` is a direction. We keep it a **unit vector**, so `t` is a distance in world units.
- `t` is the **ray parameter**. `t = 0` is the origin. Negative `t` is behind the origin and is not part of the ray.

A **raycast** asks for the smallest `t ≥ 0` at which `p(t)` touches some shape, and usually also returns the hit point `p(t)`, the surface normal there, and which object was hit. Often it takes a maximum distance too, so the question becomes "the first hit within 50 m". That turns the ray into a **segment**, `0 ≤ t ≤ t_max`, which is what a line-of-sight check really is.

Every ray test in this lecture has the same three steps. Substitute `p(t)` into the shape's equation. Solve for `t`. Keep the smallest solution that is not negative. The shapes differ only in how hard step 2 is.

## 2. Worked example: Wolfenstein 3D's 320 rays

### The hook

Wolfenstein 3D (id Software, MS-DOS, May 1992) put players in corridors that looked 3D on PCs with no 3D hardware at all. It did not transform or project any polygons. Its levels are grids of tiles, at most 64 × 64, and each frame the renderer cast **one ray per column of the view**, up to 320 of them. Each ray walks through the grid until it hits a wall tile, and the distance to that wall sets how tall to draw that column of wall. Nothing else. id released the source code in 1995, so you can read exactly how.

Two questions come out of that. How does a ray walk through a grid without missing any tile, and without testing all 4,096 of them? And why does a straight wall, drawn from true ray distances, come out curved?

### The model

Put the grid on unit cells, cell `(cx, cy)` covering `cx ≤ x < cx + 1` and `cy ≤ y < cy + 1`. A ray crosses cell boundaries of two kinds, vertical lines `x = integer` and horizontal lines `y = integer`. The **grid walk** (Amanatides and Woo's traversal, also called a DDA, for digital differential analyzer) keeps two numbers:

```
t_max_x  = t at which the ray next crosses a vertical line
t_max_y  = t at which the ray next crosses a horizontal line

t_delta_x = 1 / |d_x|    t between one vertical line and the next
t_delta_y = 1 / |d_y|    t between one horizontal line and the next
```

At each step, cross whichever line comes first. If `t_max_x < t_max_y`, move one cell in x and add `t_delta_x` to `t_max_x`. Otherwise move one cell in y and add `t_delta_y` to `t_max_y`. Test the new cell. Stop at the first wall. The `t` of the crossing you just made is the distance to the wall.

The walk visits exactly the cells the ray passes through, in order, with one comparison and one addition per cell. Its cost is proportional to how far the ray travels, measured in cells, not to how many walls exist.

For drawing, a column's wall height on screen is

```
height = H / t_perp,     t_perp = t × cos(ray angle − view angle)
```

where `H` is a constant set by the screen size and field of view, and `t_perp` is the hit's distance measured **along the view direction**, not along the ray. You met this in MA201 week 4. Size on screen is proportional to one over **depth**, the distance along the camera's forward axis. The ray length `t` is not depth. For a ray pointing off to the side, `t` is longer than the depth by `1 / cos` of the angle.

### Numbers you can check

Here is the whole renderer's core in Python, on an 8 × 8 map. As in Wolfenstein 3D's map files, row index `y` grows downward. The player stands at `(2.5, 4.5)` and looks along +x, at a straight wall that fills column `x = 6`.

```python
import math

MAP = [
    "########",
    "#.....##",
    "#.....##",
    "#.....##",
    "#.....##",
    "#.....##",
    "#.....##",
    "########",
]


def is_wall(cx, cy):
    return MAP[cy][cx] == "#"


def grid_walk(ox, oy, angle_deg, trace=False):
    """Walk unit cells along the ray from (ox, oy). Return (t, cell) of the first wall."""
    dx, dy = math.cos(math.radians(angle_deg)), math.sin(math.radians(angle_deg))
    cx, cy = int(ox), int(oy)
    step_x, step_y = (1 if dx > 0 else -1), (1 if dy > 0 else -1)
    t_delta_x = abs(1 / dx) if dx else math.inf      # t to cross one whole cell in x
    t_delta_y = abs(1 / dy) if dy else math.inf
    t_max_x = ((cx + (dx > 0)) - ox) / dx if dx else math.inf   # t to the first x line
    t_max_y = ((cy + (dy > 0)) - oy) / dy if dy else math.inf
    while True:
        if t_max_x < t_max_y:
            t, cx, t_max_x = t_max_x, cx + step_x, t_max_x + t_delta_x
        else:
            t, cy, t_max_y = t_max_y, cy + step_y, t_max_y + t_delta_y
        if trace:
            print(f"  t = {t:.3f}  enter cell ({cx}, {cy})")
        if is_wall(cx, cy):
            return t, (cx, cy)


print("ray at 20 degrees from (2.5, 4.5):")
grid_walk(2.5, 4.5, 20, trace=True)

print("\nangle   t (along ray)   perpendicular   height from t   height from perp")
for a in (-30, -20, -10, 0, 10, 20, 30):
    t, _ = grid_walk(2.5, 4.5, a)
    perp = t * math.cos(math.radians(a))          # view direction is 0 degrees
    print(f"{a:+4d}    {t:9.3f}      {perp:9.3f}      {240 / t:9.1f}      {240 / perp:9.1f}")
```

It prints:

```
ray at 20 degrees from (2.5, 4.5):
  t = 0.532  enter cell (3, 4)
  t = 1.462  enter cell (3, 5)
  t = 1.596  enter cell (4, 5)
  t = 2.660  enter cell (5, 5)
  t = 3.725  enter cell (6, 5)

angle   t (along ray)   perpendicular   height from t   height from perp
 -30        4.041          3.500           59.4           68.6
 -20        3.725          3.500           64.4           68.6
 -10        3.554          3.500           67.5           68.6
  +0        3.500          3.500           68.6           68.6
 +10        3.554          3.500           67.5           68.6
 +20        3.725          3.500           64.4           68.6
 +30        4.041          3.500           59.4           68.6
```

Check the trace by hand. At 20°, `d = (0.940, 0.342)`. The first vertical line is `x = 3`, half a cell away, so `t_max_x = 0.5 / 0.940 = 0.532`. The first horizontal line is `y = 5`, also half a cell away, so `t_max_y = 0.5 / 0.342 = 1.462`. The x crossing comes first, so the ray enters `(3, 4)` at `t = 0.532`, and `t_max_x` becomes `0.532 + 1 / 0.940 = 1.596`. Now `1.462 < 1.596`, so the next crossing is in y, into `(3, 5)`. Three more x crossings reach the wall at `(6, 5)`, at `t = 3.725`. Five cells, five comparisons, and the other 59 cells of the map are never looked at.

Check the wall distance another way. The wall face is the line `x = 6`, 3.5 units in front of the player. A ray at angle `a` reaches it after `3.5 / cos(a)`, and `3.5 / cos 20° = 3.725`. The walk found the exact distance, not an approximation.

Now read the table's last two columns. The wall is straight and square to the player, so every column of it should be drawn the same height. With the true ray distance, the center column is 68.6 units tall and the edges at ±30° shrink to 59.4, a 13% bulge in the middle. That is the **fisheye** effect. Multiply by `cos(a)` to get depth, and every column is 68.6. The ray distance is right about how far the wall is. It is wrong about how big it looks, because a flat screen measures depth, not distance.

### A visual you can move

Open [`examples/w12-grid-raycaster.html`](../examples/w12-grid-raycaster.html). The left view is the map from above. The player is a dot with a view cone, and a fan of rays is drawn out to their hits, with the cells each ray visited lightly shaded. The right view is the rendered first-person strip, one vertical bar per ray. It opens on this lecture's scene with the correction turned off, so the flat wall in front of you bulges.

Tick "perpendicular distance". The bulge snaps flat and nothing on the map changes. The rays and their hits are identical. Only the number used for height changed. Then turn the player with the arrow keys so the wall is at an angle, and toggle the correction again. Without it, walls bow outward like the view through a door peephole. Last, drag the ray count from 8 to 320 and watch the cells-visited counter. It grows with rays times distance, and adding walls to the map (click a cell to toggle it) makes rays stop sooner and the count go down.

### Cross-game recognition

**Wolfenstein 3D's own code (1992, source released 1995).** In `WL_DRAW.C`, each column's ray is stepped from tile boundary to tile boundary, with the crossing points held in `xintercept` and `yintercept`. The function `CalcHeight` then rotates the hit point into the view's frame, computing `gx × cos(view) − gy × sin(view)`, which is the distance along the view direction, and divides a height constant by it. That is the model above, with the fisheye correction built in. The positions are 16.16 fixed-point numbers, with one tile equal to 65,536 units (`TILESHIFT` 16 in `WL_DEF.H`), because floating point was too slow on the PCs of the time. MA201 week 14 returns to why a game might still choose integers today.

**Line of sight in a level blockout.** [GD201 week 12](../../GD201-level-and-world-design/lectures/w12-spawn-design-and-contested-resources.md) tests line of sight on a grid by sampling the segment every quarter of a cell and checking the cell under each sample. That is simple and nearly right. The grid walk is exactly right, and here is the difference on a segment from `(0.5, 0.5)` to `(4.2, 3.0)`:

```python
import math

def dda_cells(ax, ay, bx, by):
    """Every unit cell the segment from a to b passes through, in order."""
    dx, dy = bx - ax, by - ay
    cx, cy, end = int(ax), int(ay), (int(bx), int(by))
    sx, sy = (1 if dx > 0 else -1), (1 if dy > 0 else -1)
    tdx = abs(1 / dx) if dx else math.inf
    tdy = abs(1 / dy) if dy else math.inf
    tmx = ((cx + (dx > 0)) - ax) / dx if dx else math.inf
    tmy = ((cy + (dy > 0)) - ay) / dy if dy else math.inf
    cells = [(cx, cy)]
    while (cx, cy) != end:
        if tmx < tmy:
            cx, tmx = cx + sx, tmx + tdx
        else:
            cy, tmy = cy + sy, tmy + tdy
        cells.append((cx, cy))
    return cells

def sampled_cells(ax, ay, bx, by, per_cell=4):
    """Cells hit by samples every 1/per_cell of a cell along the segment."""
    n = max(1, math.ceil(per_cell * max(abs(bx - ax), abs(by - ay))))
    return list(dict.fromkeys((int(ax + (bx - ax) * i / n), int(ay + (by - ay) * i / n))
                              for i in range(n + 1)))

a, b = (0.5, 0.5), (4.2, 3.0)
walk, samp = dda_cells(*a, *b), sampled_cells(*a, *b)
print("grid walk:", walk)
print("sampled:  ", samp)
print("missed by sampling:", [c for c in walk if c not in samp])
```

```
grid walk: [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2), (4, 2), (4, 3)]
sampled:   [(0, 0), (1, 1), (2, 1), (2, 2), (3, 2), (4, 3)]
missed by sampling: [(1, 0), (4, 2)]
```

Sampling stepped over two cells, `(1, 0)` and `(4, 2)`, which the segment clips across their corners. The samples are about 0.3 units apart along the segment, so any corner piece shorter than that can fall between two of them. Put a pillar in either cell and the sampled check reports a clear line of sight through it. Players find exactly these gaps, a sniper who can see through the corner of a crate. For a blockout the error is harmless. For a shipped server check it is a bug.

**Engine raycasts.** Unity's `Physics.Raycast` (Unity 6) takes an origin, a direction and a maximum distance, and returns whether anything was hit, with an optional hit record. Godot 4's `intersect_ray` takes a from and a to point and returns a dictionary with the hit `position`, surface `normal` and `collider`, or an empty dictionary on a miss. Both walk a broad-phase structure first (week 11), exactly as the grid walk does, and only run the exact shape tests of section 3 on the objects the ray's path passes near. Box2D's dynamic tree (v2.4.1) has a `RayCast` query for the same purpose.

Rewrite all three into the model's form and they are one algorithm. Walk a spatial structure along the ray in order of `t`, test what you meet, stop at the first hit.

### Eyes-open design judgment

- **Walk, don't scan.** A ray that tests every object in the level is `O(n)` per ray, and a renderer or perception system casts thousands. The grid walk and the tree query make the cost depend on the distance travelled. Wolfenstein 3D's frame was 320 short walks, not 320 × 4,096 tests.
- **Cap the distance.** An uncapped ray over open terrain walks until it leaves the world. Every raycast in gameplay code should have a `t_max` from the design (weapon range, sight range).
- **Distance and depth answer different questions.** Use the ray length `t` for gameplay (range, damage falloff, sound delay). Use depth `t_perp` for anything drawn on a flat screen. Mixing them up is the fisheye bug. The reverse mistake is just as easy to write. Measure damage falloff by view depth instead of ray length, and a target at the edge of the screen takes more damage than the same target at the center.
- **Grids are cheap because the world agreed to be a grid.** Wolfenstein 3D's walls are all full tiles at right angles, which is why the renderer is so simple. The moment you want a diagonal wall or a floor of varying height, you need the shape tests below or a different renderer.

## 3. Rays against shapes

### Sphere: a quadratic

A sphere of center `c` and radius `R` is every point with `|p − c|² = R²`. Substitute the ray and let `m = o − c`, the vector from the center to the origin. With `d` a unit vector:

```
|m + t d|² = R²
t² + 2 (m · d) t + (m · m − R²) = 0
```

That is a quadratic in `t`, the one from MA101 week 3, with `a = 1`. Write `b = m · d` and `k = m · m − R²`:

```
disc = b² − k
t = −b ± √disc
```

- `disc < 0`: the line misses the sphere.
- `disc = 0`: the ray grazes it at one point.
- `disc > 0`: two hits, entering at `−b − √disc` and leaving at `−b + √disc`.

Two early exits save most of the work. If `k > 0`, the origin is outside the sphere. If also `b > 0`, the sphere is behind the ray, so there is nothing to hit. And if `k < 0`, the origin is inside the sphere, the smaller root is negative, and you must decide what "hit" means (section 4).

### Box: three slabs

An axis-aligned box is the overlap of three **slabs**: `lo_x ≤ x ≤ hi_x`, and the same for y and z. The ray is inside the x slab for `t` between `(lo_x − o_x) / d_x` and `(hi_x − o_x) / d_x`, in whichever order makes the interval run forward. It is inside the box where all three intervals overlap. So the entry `t` is the **largest** of the three slab entries, and the exit is the **smallest** of the three exits. If the entry comes after the exit, the ray misses.

```python
import math


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def ray_sphere(o, d, c, radius):
    """First t >= 0 where o + t d (d unit) meets the sphere, or None."""
    m = (o[0] - c[0], o[1] - c[1], o[2] - c[2])
    b = dot(m, d)
    k = dot(m, m) - radius * radius       # > 0 means the origin is outside
    if k > 0 and b > 0:
        return None                       # outside and pointing away
    disc = b * b - k
    if disc < 0:
        return None                       # the line misses the sphere
    t = -b - math.sqrt(disc)
    return max(t, 0.0)                    # t < 0: we started inside


def ray_aabb(o, d, lo, hi):
    """Slab test: first t >= 0 where o + t d enters the box [lo, hi], or None."""
    t_near, t_far = 0.0, math.inf
    for axis in range(3):
        if d[axis] == 0:
            if not lo[axis] <= o[axis] <= hi[axis]:
                return None               # parallel to this slab and outside it
            continue
        t1 = (lo[axis] - o[axis]) / d[axis]
        t2 = (hi[axis] - o[axis]) / d[axis]
        t_near = max(t_near, min(t1, t2))
        t_far = min(t_far, max(t1, t2))
        if t_near > t_far:
            return None                   # slabs don't overlap along the ray
    return t_near


o, d = (0, 0, 0), (1, 0, 0)
for y in (0.0, 0.3, 0.5, 0.6):
    hit = ray_sphere(o, d, (10, y, 0), 0.5)
    print(f"sphere at (10, {y}, 0), r 0.5:", None if hit is None else round(hit, 3))
print("inside the sphere:", ray_sphere((10, 0, 0), d, (10, 0, 0), 0.5))

s = 1 / math.sqrt(2)
print("box, straight:", ray_aabb(o, d, (4, -1, -1), (6, 1, 1)))
print("box, 45 deg:  ", round(ray_aabb(o, (s, s, 0), (4, 3, -1), (6, 5, 1)), 3))
print("box, 45 deg, miss:", ray_aabb(o, (s, s, 0), (4, 0, -1), (6, 2, 1)))
```

```
sphere at (10, 0.0, 0), r 0.5: 9.5
sphere at (10, 0.3, 0), r 0.5: 9.6
sphere at (10, 0.5, 0), r 0.5: 10.0
sphere at (10, 0.6, 0), r 0.5: None
inside the sphere: 0.0
box, straight: 4.0
box, 45 deg:   5.657
box, 45 deg, miss: None
```

Check the second sphere line by hand. `m = (−10, −0.3, 0)`, `b = −10`, `k = 100.09 − 0.25 = 99.84`, `disc = 100 − 99.84 = 0.16`, so `t = 10 − 0.4 = 9.6`. The sphere at height 0.5 is grazed at exactly `t = 10`, and at 0.6 it is missed. A hitscan shot hits a sphere exactly when the sphere's center is within `R` of the line, whatever the distance. That is why hitscan hitboxes feel the same at every range, and why a designer who wants long shots to be harder must change something else (spread, or a projectile, next week).

For the 45° box, the ray enters the x slab at `4 / 0.707 = 5.657` and the y slab at `3 / 0.707 = 4.243`. The later entry wins, 5.657. In the miss case, the ray leaves the y slab at `t = 2.83` before it enters the x slab at 5.657, so the intervals never overlap.

### Other shapes

A **plane** `n · p = h` gives a linear equation, `t = (h − n · o) / (n · d)`, with no hit when `n · d = 0` (the ray runs parallel). A **triangle** is a plane hit followed by an inside-the-triangle test, and a mesh is thousands of triangles behind a tree (week 11) so that only a few are tested. Capsules, the usual shape for characters, combine a cylinder and two sphere caps. Dunn and Parberry's Appendix A and Ericson chapter 5 give all of them. They all follow the same three steps as the sphere.

## 4. Where raycasts go wrong

**Starting inside.** When the origin is inside a shape, the first root is negative. Is that a hit at `t = 0`, a hit at the exit, or nothing? Engines choose differently, so read the documentation. Unity's documentation for `Physics.Raycast` states that it does not detect colliders that contain the ray's origin. That is why a ground check cast from a character's center, which sits inside its own capsule, needs its own collider excluded by a layer mask. Our `ray_sphere` returns 0, which is the right answer for "am I already touching this?" and the wrong one for "what is in front of me?".

**Hitting yourself.** A ray cast from a surface you just hit (a bouncing laser, a ricochet, a reflection) can hit the same surface at `t ≈ 0` because of rounding. The standard fix is to start the new ray a small distance `ε` along the normal, or to ignore hits with `t < ε`. The right `ε` depends on your world's scale. 0.001 m is typical for a human-scale game, and far too small at 10 km from the origin, which is week 14's subject.

**Parallel rays.** Dividing by `d_x = 0` is a crash in Python and an infinity in most engines' float math. Both our functions handle it explicitly. The slab test with IEEE infinities almost works on its own, until the origin lies exactly on a slab boundary, where `0 × ∞` gives NaN and every comparison with NaN is false.

**Grazing and edges.** A ray exactly through a grid corner, or exactly tangent to a sphere, lands on a tie. The grid walk above breaks ties toward y, so a ray through a corner visits one of the two side cells and not the other. For rendering that is invisible. For a line-of-sight rule, decide whether a corner blocks sight and test for that case, or players will find the one diagonal that sees through a wall.

**Sampling instead of walking.** As the GD201 comparison in section 2 showed, stepping along a ray in fixed increments can skip thin walls and corners. The same bug, in time instead of space, is CS101's tunnelling. A bullet moved in steps passes through thin walls. Casting a ray along each step's path, from the old position to the new one, is the standard fix for fast projectiles, and it is exactly what the server-side movement check in [MMO302 week 6](../../MMO302-mmo-server-architecture/lectures/w06-simulation-authority-and-anti-cheat-by-design.md) does.

## In-class activity (25 minutes)

In pairs, on grid paper.

1. Draw a 10 × 10 map with a wall layout of your choice, including one diagonal gap between two wall cells that touch only at a corner. (5 min)
2. Place a guard and a player so that the straight segment between them passes exactly through that corner. Trace the grid walk by hand, writing `t_max_x`, `t_max_y` and the cell at each step. Does the guard see the player? Would the quarter-cell sampler agree? (12 min)
3. Decide whether a diagonal gap like this should block sight in your game. Write the rule in one sentence, and the one-line change to `grid_walk` that enforces it. (8 min)

Expected output: the traced table, the two verdicts, and your rule with its code change.

## Common misconceptions

- **"The raycast distance is how far away it looks."** On a flat screen, apparent size follows depth along the view axis. Distance along the ray is longer by `1 / cos` of the off-axis angle. Use it for gameplay, not for drawing.
- **"Stepping along the ray in small steps is the same as a raycast."** It is an approximation that skips anything thinner than a step, and corners. The grid walk visits every cell crossed. Shape tests solve for the exact `t`.
- **"A negative root means a miss."** It means the hit is behind the origin. If only one root is negative, the origin is inside the shape, which is often the case you most need to handle.
- **"More walls make raycasting slower."** For a grid walk, more walls make rays stop sooner. The cost is cells crossed before the first hit.

## Check yourself

1. A ray starts at `(1.5, 1.5)` in a unit grid with direction exactly `(0.7071, 0.7071)`, the same number in both components. List the first four cells it enters (breaking exact ties toward y, as in the lecture's code) and the `t` at each. Then explain why `grid_walk(1.5, 1.5, 45)` may visit different cells.
2. In the lecture's scene, the player turns to face 10°. The wall is still the line `x = 6`. What are the ray distance and the perpendicular distance for the ray at 30° (20° right of the view direction)?
3. A hitscan ray from the origin along `(1, 0, 0)` meets a sphere of radius 0.3 centred at `(20, 0.2, 0)`. Find `t`. Would it hit with the center at `(20, 0.35, 0)`?
4. A ray from `(0, 0, 0)` with direction `(0.6, 0.8, 0)` meets the box from `(3, 2, −1)` to `(5, 6, 1)`. Find the entry and exit `t`.

<details>
<summary>Answers</summary>

1. `d = (0.707, 0.707)`, `t_delta = 1.414` on both axes, and both first crossings are at `t = 0.707`. With ties going to y: `(1, 2)` at 0.707, then x at 0.707 into `(2, 2)`, then y at 2.121 into `(2, 3)`, then x at 2.121 into `(3, 3)`. The ray passes exactly through the corners, and the tie rule decides which side cell it visits. In Python, `math.cos(math.radians(45))` is 0.7071067811865476 and `math.sin` of the same angle is 0.7071067811865475. They differ in the last digit, so `t_max_x` is slightly smaller than `t_max_y`, the "tie" is not a tie, and the walk goes x first. Rounding decides the corner. Week 14 is about exactly this.
2. The ray at 30° reaches `x = 6` at `t = 3.5 / cos 30° = 4.041`. Its angle to the view direction is 20°, so `t_perp = 4.041 × cos 20° = 3.798`. Depth is measured along the new view direction, which is why the wall now slants on screen.
3. `m = (−20, −0.2, 0)`, `b = −20`, `k = 400.04 − 0.09 = 399.95`, `disc = 400 − 399.95 = 0.05`, `t = 20 − 0.224 = 19.776`. At 0.35 the center is farther than 0.3 from the line, so `disc = 400 − (400.1225 − 0.09) < 0`, a miss.
4. x slab: `t` from `3 / 0.6 = 5` to `5 / 0.6 = 8.333`. y slab: `2 / 0.8 = 2.5` to `6 / 0.8 = 7.5`. z: `d_z = 0` and `0` lies inside `[−1, 1]`, so no limit. Entry `max(5, 2.5) = 5`, exit `min(8.333, 7.5) = 7.5`. Hit, entering at `t = 5`, point `(3, 4, 0)`.

</details>

## Lab / assignment hook

[Lab 12, a grid raycaster and a hitscan check](../labs/lab12.md). You implement the grid walk, the perpendicular-distance column heights, and the sphere and slab tests, render a map as text columns in the terminal, and then find and fix a planted line-of-sight exploit on a server map by replacing a sampled check with a grid walk.

## Sources

- id Software, *Wolfenstein 3D* source code (GitHub `id-Software/wolf3d`, originally released 1995). `WOLFSRC/WL_DEF.H` (`MAPSIZE` 64, `MAXVIEWWIDTH` 320, `TILESHIFT` 16 and `GLOBAL1 = 1 << 16` fixed point); `WOLFSRC/WL_DRAW.C` (per-column ray stepping with `xintercept` and `yintercept`; `CalcHeight` computes distance along the view direction with `viewcos` and `viewsin`).
- Wikipedia, "Wolfenstein 3D" (accessed September 2026). MS-DOS release on 5 May 1992; ray-casting renderer; source code released in 1995.
- Amanatides, J. & Woo, A. (1987). "A Fast Voxel Traversal Algorithm for Ray Tracing." *Eurographics '87*, pp. 3-10.
- Unity Technologies. Unity 6.6 Scripting API, `Physics.Raycast`: parameters, boolean result, and the note that raycasts do not detect colliders containing the origin.
- Godot Engine. Godot 4.7 documentation, "Ray-casting": `PhysicsRayQueryParameters2D/3D.create`, `intersect_ray` result dictionary, empty dictionary on a miss.
- Catto, E. Box2D v2.4.1, `b2_dynamic_tree.h` (tree used for volume queries and ray casts).
- Dunn, F. & Parberry, I. *3D Math Primer for Graphics and Game Development*, 2nd ed., chapter 9 and Appendix A (gamemath.com).
- Ericson, C. (2005). *Real-Time Collision Detection*. Morgan Kaufmann. Chapter 5.

## Interactive spec: examples/w12-grid-raycaster.html

**The one insight:** a raycast renderer that uses the true ray length draws straight walls curved, because apparent size follows depth along the view direction, not distance along the ray. The rays and their hits don't change when you fix it. Only the number used for height does. A secondary insight: the grid walk's cost is cells crossed, so more walls make it cheaper.

**Layout.** Two linked views, side by side at 1280 px, stacked at 390 px (map on top).

- **Left, "Map":** the lecture's 8 × 8 map by default (row strings given in the lecture, `#` wall), drawn with y growing downward. Player dot at `(2.5, 4.5)`, facing 0° (+x), with a translucent view cone of the current field of view. A fan of `N` rays from the player to their hits. Cells visited by the currently highlighted ray are shaded; others outlined faintly. A "trace" panel lists, for the highlighted ray, each step's `t` and entered cell, exactly as in the lecture's printed trace. Clicking or pressing Enter on a cell toggles it between wall and floor (the outer border stays wall). A "Load 16 × 16 map" button swaps in a larger maze.
- **Right, "View":** the first-person strip, `N` vertical bars, bar `i` centered, height `H / dist` with `H = 240` in the same units as the lecture's table, clipped to the strip. Bars shaded darker for hits on horizontal grid lines (y crossings) than vertical ones, so wall faces read clearly. A thin horizon line. Under the strip, a small line plot of bar height against column, which makes the bulge measurable.

**Controls (labelled, keyboard accessible):**

1. "Perpendicular distance" checkbox, default off on first load.
2. Ray count `N`: 8, 16, 32, 64, 160, 320. Default 7 on first load, cast at −30°, −20°, …, +30° so the bars match the lecture's table exactly; the selector also offers "7 (table)".
3. Field of view 30° to 120°, default 60°.
4. Turn left/right (arrow keys when the map has focus, 5° per press) and move forward/back (W/S, 0.1 cells), with collision against wall cells.
5. Highlighted ray selector (a slider over ray indices), default the +20° ray.
6. Readouts: cells visited by all rays this frame, and by the highlighted ray; highlighted ray's `t`, `t_perp`, and both heights.

**Formulas.** Ray `i` of `N` at angle `view + fov × (i/(N − 1) − 0.5)` (for `N = 7` and fov 60 this gives −30 … +30 in 10° steps). Direction `(cos a, sin a)`. Grid walk exactly as in the lecture's `grid_walk`: `t_delta = |1/d|`, `t_max = ((c + (d > 0)) − o) / d`, step the smaller, ties go to y. `t_perp = t × cos(a − view)`. Height `= 240 / (perp ? t_perp : t)`.

**Test values (must match the lecture).**

- Highlighted ray at +20° from `(2.5, 4.5)`: trace `t` = 0.532 (3, 4), 1.462 (3, 5), 1.596 (4, 5), 2.660 (5, 5), 3.725 (6, 5).
- Seven-ray table, correction off: heights 59.4, 64.4, 67.5, 68.6, 67.5, 64.4, 59.4. On: all 68.6.
- Check yourself 2: view at 10°, the ray at 30°: `t = 4.041`, `t_perp = 3.798`.
- Corner example: segment from `(0.5, 0.5)` to `(4.2, 3.0)` visits (0,0), (1,0), (1,1), (2,1), (2,2), (3,2), (4,2), (4,3). Provide a "compare with sampling" toggle that draws the quarter-cell samples as dots on this segment on a blank 6 × 5 grid and marks cells (1, 0) and (4, 2) as missed.

**First screen.** Lecture scene, 7 rays, correction off, the bulging wall visible in the strip and in the height plot. Caption: "Same rays, same hits. Tick the box: only the number used for height changes."

**Accessibility.** All controls reachable by Tab with visible focus. A live region announces the highlighted ray's `t`, `t_perp` and heights after each change. `prefers-reduced-motion`: movement keys jump without animation. `prefers-color-scheme` via `templates/interactive-tokens.css`. Flat colored bars and grid squares only, no textures or game art.

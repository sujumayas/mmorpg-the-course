# CS101 · Week 10 — Collision basics: AABB and circles

**Why this matters:** Every pickup, wall, bullet and enemy in your arcade game asks one question each frame. Do these two things touch? This week you write that test yourself, in four comparisons for boxes and one for circles, and you learn the three ways it goes wrong in shipped games.

**You will be able to:**
- Write an axis-aligned box overlap test as four comparisons and trace it by hand for any pair of boxes.
- Write a circle overlap test with squared distances and no square root.
- Compute the overlap depth on each axis and use the smaller one to push a player out of a wall.
- Predict when a fast object will tunnel through a thin wall, given its speed, the frame rate and the wall's thickness.

**Before class:** Nystrom, *Game Programming Patterns*, the "Update Method" chapter (free online), for where collision checks sit in the loop. Godot 4 documentation, "Physics introduction", the sections on collision shapes and Area2D. Reread your week 9 notes on delta time.

**Prerequisites from earlier courses:** Section 3 explains the distance formula and the squared-distance trick it needs; [MA101 week 12, 2D vectors](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w12-2d-vectors.md) and [MA101 week 14, distances and the squared-distance trick](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w14-distances-ranges-and-squared-distance.md) cover both in depth at the end of this semester. [CS101 week 8, input handling and movement](w08-input-handling-and-movement.md) (moving a box with the keyboard). [CS101 week 9, delta time and frame-rate independence](w09-delta-time-and-frame-rate-independence.md) (step size per frame and the fixed-timestep accumulator, both used in section 5).

**Interactive:** [AABB overlap](../examples/w10-aabb-overlap.html). Keep it open during section 2.

---

## 1. What a collision check answers

A game draws a sprite, but it does not collide with the sprite. It collides with a simpler shape that stands in for the sprite. That shape is the **collider**, and when it decides whether something got hit, players call it the **hitbox**. The sprite can be a knight with a flowing cape. The collider is usually a rectangle or a circle.

Why the simplification? Because the check runs constantly. If your game has 40 bullets and 20 enemies, testing every bullet against every enemy is 800 checks per frame. At 60 frames per second that is 48,000 checks per second, before you add walls and pickups. Each check has to be cheap, and a rectangle test costs four comparisons.

Three words you will use all week:

- A **collision test** (or overlap test) takes two shapes and returns `True` or `False`. It does nothing else.
- **Collision response** is what your code does after a `True`. Destroy the bullet, subtract health, push the player out of the wall. Response is a design decision. The test is math.
- A **discrete** check looks at where things are this frame and ignores the path they took to get there. Almost everything you write in this course is discrete. Section 5 shows the price.

### Coordinates, once more

In Godot 2D and in most 2D engines, `x` grows to the right and `y` grows **downward**. The top-left corner of the screen is `(0, 0)`. A box is stored as its top-left corner plus its size:

```python
player = {"x": 100, "y": 100, "w": 32, "h": 48}
```

From that you can read its four edges:

```python
left   = box["x"]
right  = box["x"] + box["w"]
top    = box["y"]
bottom = box["y"] + box["h"]
```

For the player above, left is 100, right is 132, top is 100 and bottom is 148. Because `y` points down, "bottom" is the larger `y` value. If you mix this up, every vertical test flips, so write the four lines above into a helper function once and never retype them.

A box whose edges run parallel to the screen's x and y axes is **axis-aligned**. It never rotates. That is the "AA" in **AABB**, an axis-aligned bounding box.

## 2. Worked example: the AABB test as four comparisons

### The hook

Open Minecraft Java Edition and press F3 + B. White boxes appear around every creature and around your own character. Now spin around. The creature models turn, but the white boxes don't. The Minecraft Wiki describes the entity bounding box as one that moves with the entity but keeps a fixed orientation. A standing player is a box 0.6 blocks wide and 1.8 blocks tall. Sneak, and the game swaps it for a box 1.5 blocks tall. Swim or glide and it becomes 0.6 by 0.6.

So Minecraft treats you, for collision purposes, as a box that cannot turn. You might expect that to feel wrong. It doesn't, and the reason is the subject of this section: a box that never rotates can be tested against another one with four comparisons, and a test that cheap can run for every entity, every tick.

### The model

Two axis-aligned boxes `a` and `b` overlap if and only if all four of these are true:

```
1.  a.left   < b.right      a starts before b ends, horizontally
2.  a.right  > b.left       a ends after b starts, horizontally
3.  a.top    < b.bottom     a starts before b ends, vertically
4.  a.bottom > b.top        a ends after b starts, vertically
```

Read each comparison as ruling out one way of being apart. If comparison 1 is false, `a` sits entirely to the right of `b`. If 2 is false, `a` sits entirely to the left. If 3 is false, `a` is entirely below `b`, and if 4 is false, `a` is entirely above. Those are the only four ways two non-rotating boxes can miss each other. Rule all four out and they must overlap.

There is a second way to see the same thing, and the interactive draws it. Squash each box flat onto the x axis. Each becomes an interval, `[left, right]`. Do the same on the y axis. Two boxes overlap exactly when their x intervals overlap **and** their y intervals overlap. Comparisons 1 and 2 are the x-interval test. Comparisons 3 and 4 are the y-interval test. One 2D question becomes two 1D questions.

In Python, with the helper from section 1:

```python
def edges(box):
    return box["x"], box["x"] + box["w"], box["y"], box["y"] + box["h"]

def aabb_overlap(a, b):
    a_left, a_right, a_top, a_bottom = edges(a)
    b_left, b_right, b_top, b_bottom = edges(b)
    return (a_left < b_right and
            a_right > b_left and
            a_top < b_bottom and
            a_bottom > b_top)
```

Python's `and` stops at the first `False`, so a pair of boxes that are far apart costs one or two comparisons, not four. That early exit is why the test order barely matters for speed. It matters for reading the code, so keep the order above everywhere.

The same test in GDScript, if you store boxes as Godot's built-in `Rect2`:

```gdscript
func aabb_overlap(a: Rect2, b: Rect2) -> bool:
    return (a.position.x < b.end.x and a.end.x > b.position.x
        and a.position.y < b.end.y and a.end.y > b.position.y)
```

You would normally call `a.intersects(b)` instead. You write it by hand once so you know what that call does.

### Numbers you can check

Take the player box `(x=100, y=100, w=32, h=48)`, so its edges are left 100, right 132, top 100, bottom 148. Test it against five other boxes. Each cell shows the comparison with numbers filled in.

| Other box `(x, y, w, h)` | 1. `a.left < b.right` | 2. `a.right > b.left` | 3. `a.top < b.bottom` | 4. `a.bottom > b.top` | Overlap? |
|---|---|---|---|---|---|
| A `(120, 130, 32, 32)` | 100 < 152 ✓ | 132 > 120 ✓ | 100 < 162 ✓ | 148 > 130 ✓ | yes |
| B `(140, 110, 32, 32)` | 100 < 172 ✓ | 132 > 140 ✗ | 100 < 142 ✓ | 148 > 110 ✓ | no |
| C `(132, 100, 32, 32)` | 100 < 164 ✓ | 132 > 132 ✗ | 100 < 132 ✓ | 148 > 100 ✓ | no, touching |
| D `(60, 60, 32, 32)` | 100 < 92 ✗ | 132 > 60 ✓ | 100 < 92 ✗ | 148 > 60 ✓ | no |
| E `(90, 140, 60, 8)` | 100 < 150 ✓ | 132 > 90 ✓ | 100 < 148 ✓ | 148 > 140 ✓ | yes |

Look at what each miss tells you. Box B fails only comparison 2, so it lies to the right of the player with a gap of 8 pixels (140 minus 132). Box D fails two comparisons, 1 and 3, so it lies up and to the left, diagonally away. Box C is the interesting one. Its left edge sits exactly on the player's right edge. They share a line but no area, and with strict `<` and `>` the test says no overlap. Box E is a thin platform whose top edge is 8 pixels above the player's feet. The player has sunk into it, and the test says so.

### The visual

Open the interactive. Two boxes sit on a canvas, and beside them four rows light up green or red, one per comparison, with the live numbers. Drag either box. Below the canvas the same two boxes are drawn again as intervals on the x axis and on the y axis.

Press preset B, then drag it slowly to the left until it touches the player. Watch row 2 flip exactly when the x intervals start to share more than a point. Then press the "Plus sign" preset, a tall thin box across a wide flat one. No corner of either box is inside the other, yet all four rows are green. The "Show the corner test" toggle runs the common beginner version, "is any corner of `a` inside `b`?", and you will see it answer no while the boxes plainly overlap. The interval view shows why the four comparisons are right: both projections overlap, so the boxes do.

### Cross-game recognition

**Godot 4 (engine source, `core/math/rect2.h`).** `Rect2.intersects` is our test written as four early returns. It returns `false` if `position.x >= p_rect.position.x + p_rect.size.width`, then the same for the other three sides, and `true` if none fired. Each line is the negation of one of our comparisons. It also takes an `include_borders` flag, default `false`. With the default, touching boxes like C do not intersect. Pass `true` and the `>=` becomes `>`, so touching counts.

**pygame (current documentation for `Rect.colliderect`).** The docs say two rectangles collide if any portion overlaps, except the top and bottom or left and right edges. That is the same strict rule as Godot's default. pygame also says a point on the right or bottom edge of a rectangle is not inside it, which is the same rule applied to points. Two engines, one convention. The reason is tiling: if touching counted as overlapping, a player standing on a row of floor tiles would be "inside" the floor every frame.

**Minecraft (Java Edition, current versions).** Entity bounding boxes never rotate, which is why the four-comparison test is enough for them. The game changes the box's *size* instead of its angle. Sneaking shortens the player box from 1.8 to 1.5 blocks, and crawling or swimming shrinks it to 0.6. A shape change is a design tool here, and a cheap one, because the test does not care.

**Celeste (2018).** Maddy Thorson's article "Celeste & Forgiveness" lists corner correction among the game's assists. If you bump your head on the corner of a ceiling during a jump, the game tries to wiggle you sideways around it instead of stopping you. That behavior starts with exactly the test in this section. The overlap test reports a hit, and the response code checks whether a small sideways shift would clear it. The test is plain arithmetic. The generosity lives in the response.

Four products, one idea. Whenever you see a hitbox that does not turn, expect four comparisons underneath.

### Eyes-open design judgment

Boxes are the default for good reasons. They are cheap, they tile, and they match level geometry built from tiles. They also have costs you should choose to pay:

- **Corners stick out.** A box around a round character has corners the character doesn't. Enemies clip the empty corner and players feel cheated. Shrink the hitbox a few pixels inside the sprite, or use a circle.
- **Touching versus overlapping is a rule, and you have to pick it.** Strict comparisons stop a player from snagging on the seam between two floor tiles. Inclusive comparisons make pickups easier to grab. Decide once, write it in your design notes, and use the same rule everywhere.
- **A box can't turn.** A long rotated sword swing doesn't fit a non-rotating box. You either use a stack of small boxes along the blade, or you move to oriented boxes and a heavier test ([MA201 week 9](../../MA201-linear-algebra-and-physics-for-games/lectures/w09-collision-detection-spheres-aabb-sat.md) covers the separating axis test that generalizes this one).
- **The hitbox is part of the game feel.** A hitbox smaller than the sprite makes the player feel lucky. A bigger one makes enemies feel unfair. That's a tuning knob, and Celeste shows a studio turning it on purpose.

## 3. Circles: one comparison and no square root

A circle collider is a center `(cx, cy)` and a radius `r`. Two circles overlap when the distance between their centers is less than the sum of their radii. The horizontal gap `dx` and the vertical gap `dy` between the centers are the two short sides of a right triangle, so by Pythagoras the distance is `√(dx² + dy²)`. The square root is slow and also unnecessary. Both the distance and the sum of radii are non-negative, and for non-negative numbers `a < b` is true exactly when `a² < b²` (try 3 < 4 and 9 < 16). So you can square both sides and the answer never changes:

```
overlap  if and only if  dx² + dy² < (r1 + r2)²
where    dx = c2.x − c1.x,   dy = c2.y − c1.y
```

```python
def circle_overlap(a, b):
    dx = b["cx"] - a["cx"]
    dy = b["cy"] - a["cy"]
    reach = a["r"] + b["r"]
    return dx * dx + dy * dy < reach * reach
```

A worked check. A player circle with radius 16 stands at `(180, 115)`. A coin with radius 8 sits at `(200, 100)`.

| Player center | `dx` | `dy` | `dx² + dy²` | `(16 + 8)²` | Overlap? |
|---|---|---|---|---|---|
| (180, 115) | 20 | −15 | 625 | 576 | no, 1 pixel short |
| (182, 114) | 18 | −14 | 520 | 576 | yes |
| (176, 118) | 24 | −18 | 900 | 576 | no |

In the first row the true distance is 25 and the reach is 24, so the player misses the coin by one pixel. You never computed 25. You compared 625 with 576.

Circles suit things that are round or that should feel fair from every direction: coins, bullets, explosions, the "pickup radius" around a player. A circle has no corners to snag on, and rotating it changes nothing. Its weakness is the reverse of the box's. A circle fits a wall or a doorway badly, so most games use boxes for the world and circles for small moving things.

### Circle against box

Mixed pairs come up constantly, for example a round bullet against a rectangular wall. The trick is to find the point on the box nearest the circle's center, then do a point-in-circle test on that point. The nearest point is the center, clamped into the box on each axis:

```python
def clamp(v, lo, hi):
    return max(lo, min(v, hi))

def circle_box_overlap(c, box):
    left, right, top, bottom = edges(box)
    nx = clamp(c["cx"], left, right)
    ny = clamp(c["cy"], top, bottom)
    dx = c["cx"] - nx
    dy = c["cy"] - ny
    return dx * dx + dy * dy < c["r"] * c["r"]
```

Try a bullet of radius 4 at `(135, 151)` against the player box (left 100, right 132, top 100, bottom 148). The nearest point is `(132, 148)`, the bottom-right corner. The offset is `(3, 3)`, so the squared distance is 18. That is more than 16, so the bullet misses. A box test around the bullet's own bounding square would have said hit, because the square's corner pokes into the player. This is the corner problem from section 2, viewed from the bullet's side.

## 4. Response: getting the player out of the wall

The test tells you the player is inside a wall. Now you have to move them out, and "back to where they were last frame" is a poor answer because it also cancels the sideways part of their motion. The standard beginner response is **minimum push-out**. Measure how deep the overlap is on each axis and push along the shallower one.

```python
def overlap_depth(a, b):
    a_left, a_right, a_top, a_bottom = edges(a)
    b_left, b_right, b_top, b_bottom = edges(b)
    ox = min(a_right, b_right) - max(a_left, b_left)
    oy = min(a_bottom, b_bottom) - max(a_top, b_top)
    return ox, oy   # both positive only when the boxes overlap
```

For player and box A from the table, `ox = min(132, 152) − max(100, 120) = 12` and `oy = min(148, 162) − max(100, 130) = 18`. The x overlap is smaller, so push on x. The player's center (x = 116) is left of A's center (x = 136), so push left by 12. The player's `x` becomes 88, its right edge becomes 120, and that equals A's left edge. With the strict rule the boxes now touch without overlapping, which is exactly where you want them.

For box E, the thin platform, `ox = min(132, 150) − max(100, 90) = 32` and `oy = min(148, 148) − max(100, 140) = 8`. Push on y, upward by 8, and the player stands on the platform.

The rule works because the shallow axis is almost always the one the player entered from. A player running right into a wall has only a few pixels of x overlap but a whole body height of y overlap. It fails when the player moves fast diagonally into a corner, where both depths are similar and the push can pick the wrong side. The fix most platformers use is to move and resolve one axis at a time, x first, then y. Godot's `CharacterBody2D.move_and_slide()` does this work for you, and you will use it in your mini-game. Writing it yourself once is how you learn what it is guarding against.

## 5. Tunneling: when fast objects skip the wall

Discrete checks look at positions, never at paths. A bullet that moves 30 pixels per frame is tested at pixel 0, then pixel 30, then 60. If the wall lies entirely between two of those samples, the bullet never overlaps it and passes straight through. This is **tunneling**.

Here is the condition. An object of size `s` moving `v` pixels per second, stepped at `f` frames per second, moves `v / f` pixels per step. It can skip a wall of thickness `t` when

```
v / f  >  t + s
```

Take a 4-pixel bullet at 900 pixels per second against a 16-pixel wall, so the threshold is 20 pixels per step.

| Frame rate | Step per frame | Can it tunnel? |
|---|---|---|
| 120 fps | 7.5 px | no |
| 60 fps | 15 px | no |
| 30 fps | 30 px | yes |
| 20 fps | 45 px | yes, through two walls in a row |

Now connect this to week 9. You made movement frame-rate independent by multiplying by `delta`, so the bullet crosses the screen in the same time on any machine. But the collision check still runs once per frame. On a slow laptop the same bullet takes bigger steps, and suddenly it can fly through walls that stop it on your desktop. Delta time fixed the speed and quietly broke the collision. This is one of the strongest arguments for the fixed timestep from week 9. If physics always steps at 60 Hz, the step size is always 15 pixels and your table has one row.

Three fixes, cheapest first:

1. **Design around it.** Keep walls thicker than the fastest object's step, `t > v / f − s`. Free, and often enough for an arcade game.
2. **Substep.** Move fast objects in several small steps per frame and test after each. Four substeps at 30 fps give 7.5-pixel steps.
3. **Sweep.** Test the whole path segment instead of its endpoints. Godot calls this continuous collision detection. `RigidBody2D.continuous_cd` offers a ray-cast mode and a slower, more precise shape-cast mode. The documentation warns that the default, disabled mode can miss small, fast objects.

## 6. How many checks? A first look at cost

If you test every object against every other, `n` objects need `n × (n − 1) / 2` checks.

| Objects | Pair checks per frame |
|---|---|
| 10 | 45 |
| 100 | 4,950 |
| 1,000 | 499,500 |

A few hundred objects is fine in this course. A bullet-hell screen or an MMO town square is not, which is why engines split the world into a grid or tree and only test nearby pairs (the **broad phase**) before running the four comparisons (the **narrow phase**). You'll build a grid broad phase in [CS102 week 4](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w04-big-o-intuition-for-game-developers.md). For now, a simple habit keeps you safe. Don't test pairs that can never matter. Bullets from the player never need testing against the player, and pickups never need testing against walls. Godot's collision layers and masks exist for exactly this.

## In-class activity (25 minutes)

Work in pairs with the interactive and a copy of the section 2 code.

1. (5 min) Each partner writes three boxes on paper. Swap. Fill in the four-comparison table for all nine pairs without the computer, then check in the interactive.
2. (10 min) Find a pair of boxes where the corner test says "no" and the four-comparison test says "yes". Write down the coordinates. Then find one where the corner test gives a false "yes", or argue that none exists.
3. (10 min) Your game's bullets are 6 pixels wide and fly at 1,200 pixels per second. Walls are 16 pixels thick. At what frame rate does tunneling start? How many substeps do you need at 30 fps to be safe?

Expected output: the nine-row table, one counterexample pair, and the two numbers from step 3 with the working shown.

## Common misconceptions

- **"Two boxes overlap if a corner of one is inside the other."** A plus-sign overlap has no corner inside either box. Use the four interval comparisons.
- **"Touching counts as colliding."** Only if you choose inclusive comparisons. Godot's default and pygame both treat shared edges as not overlapping, so tiles don't snag.
- **"Circle tests need a square root."** Compare squared distance against the squared sum of radii. Squaring two non-negative numbers keeps their order, so the answer is the same.
- **"Delta time makes everything frame-rate independent."** It makes speed independent. Collision is still sampled per frame, so low frame rates tunnel.

## Check yourself

1. Box `a = (10, 10, 20, 20)` and box `b = (25, 28, 10, 10)`. Evaluate all four comparisons. Do they overlap? What is `(ox, oy)`, and which way should `a` be pushed?
2. Two circles of radius 10 and 14 have centers `(0, 0)` and `(18, 16)`. Overlap or not? Show the squared numbers.
3. A 2-pixel bullet flies at 1,500 pixels per second. The thinnest wall is 12 pixels. Below what frame rate can it tunnel?
4. A teammate writes `a_right >= b_left` for comparison 2 and leaves the others strict. Describe a bug players could see.

<details>
<summary>Answers</summary>

1. Edges of `a`: left 10, right 30, top 10, bottom 30. Edges of `b`: left 25, right 35, top 28, bottom 38. Comparisons: `10 < 35` ✓, `30 > 25` ✓, `10 < 38` ✓, `30 > 28` ✓, so they overlap. `ox = min(30, 35) − max(10, 25) = 5`, `oy = min(30, 38) − max(10, 28) = 2`. Push on y by 2. `a`'s center y (20) is above `b`'s (33), so push `a` up by 2.
2. `dx² + dy² = 324 + 256 = 580`. `(10 + 14)² = 576`. 580 is not less than 576, so they do not overlap (distance about 24.08 against a reach of 24).
3. It tunnels when `1500 / f > 12 + 2 = 14`, so when `f < 107.1` fps. At 60 fps it moves 25 pixels per frame and can skip the wall.
4. The rule is now inclusive on one side only. A player standing with their right edge exactly on a wall's left edge counts as colliding, but the mirror case on the left does not. Players would snag when walking right along seams between tiles, or trigger a pickup from one side and not the other.

</details>

## Lab / assignment hook

[Lab 10, collision toolkit](../labs/lab10.md). You implement `aabb_overlap`, `circle_overlap`, `circle_box_overlap`, `overlap_depth` and `push_out` in Python, run the provided tests, and measure tunneling in a small bullet simulation at four frame rates. Deliverable: the completed starter file and a 250-word note recommending a wall thickness for your mini-game.

## Sources

- Minecraft Wiki, "Hitbox" (Java Edition, page as of September 2026). F3 + B shows hitboxes; entity bounding boxes keep a static orientation without rotating; player box 0.6 × 1.8 standing, 1.5 tall sneaking, 0.6 × 0.6 swimming or gliding. https://minecraft.wiki/w/Hitbox
- Godot Engine source, `core/math/rect2.h`, `Rect2::intersects` and `Rect2::has_point` (master branch, Godot 4.x, checked September 2026). Four early-return comparisons, `include_borders` default `false`. https://github.com/godotengine/godot/blob/master/core/math/rect2.h
- pygame documentation, "pygame.Rect", `colliderect` and `collidepoint` (pygame 2.x). Shared edges are not a collision; right and bottom edges are outside. https://www.pygame.org/docs/ref/rect.html
- Thorson, M. "Celeste & Forgiveness" (maddymakesgames.com, undated article about Celeste, released 2018). Jump corner correction and the other positioning assists. https://maddymakesgames.com/articles/celeste_and_forgiveness/index.html
- Godot Engine documentation, "RigidBody2D", property `continuous_cd` and enum `CCDMode` (Godot 4 stable). https://docs.godotengine.org/en/stable/classes/class_rigidbody2d.html
- Nystrom, R. (2014). *Game Programming Patterns*, "Update Method". https://gameprogrammingpatterns.com/update-method.html

## Interactive spec: examples/w10-aabb-overlap.html

**Purpose.** Make the four comparisons visible. The one insight: two boxes overlap exactly when their x intervals overlap and their y intervals overlap, and each of the four comparisons is one way of being apart. The corner test is shown failing on a plus-sign overlap.

**Layout.** Mobile-first. Top: a canvas (logical size 320 × 240 world units, scaled to fit, y down, a light 16-unit grid). Below it on narrow screens, beside it on wide screens: the comparison panel. Under the canvas: the projection strip, two horizontal number lines labelled "x" and "y" (the y line drawn horizontally too, with a label saying it is the vertical axis laid flat).

**Objects.** Box `a` (the player, accent color) starts at `(100, 100, 32, 48)`. Box `b` (second color) starts at `(120, 130, 32, 32)`, box A from the lecture table. Both are draggable with mouse and touch. Keyboard: Tab focuses a box; arrow keys move it 1 unit, Shift + arrow moves 8. Positions snap to integers.

**Comparison panel.** Four rows, always in this order, each showing the formula, the live numbers and a pass or fail badge (text plus color, never color alone):
1. `a.left < b.right` e.g. `100 < 152 ✓`
2. `a.right > b.left`
3. `a.top < b.bottom`
4. `a.bottom > b.top`
A fifth row shows the result "Overlap: yes/no". When a row fails, draw a short arrow on the canvas on that side of `a` showing the gap, labelled with its size in units (for B in the table, "gap 8").

**Projection strip.** Each box drawn as a colored interval on the x line `[left, right]` and on the y line `[top, bottom]`. The shared part of each pair of intervals is highlighted. The overlap is "yes" exactly when both lines show a highlighted shared segment. Show `ox` and `oy` numerically (`ox = min(a.right, b.right) − max(a.left, b.left)`, same for y), left blank when not positive.

**Controls.**
- Edge rule toggle: "strict (Godot default, pygame)" versus "inclusive (touching counts)". Inclusive uses `<=` and `>=`. Box C `(132, 100, 32, 32)` must flip from no to yes when toggled.
- "Corner test" toggle: overlays the result of `any corner of a inside b or any corner of b inside a` (point inside uses the strict rule) as a separate badge. Where it disagrees with the four comparisons, show a warning line "corner test disagrees".
- Presets menu that loads box `b` as the table's A, B, C, D, E, plus "plus sign" which sets `a = (110, 80, 10, 90)` and `b = (90, 110, 60, 20)`.
- "Push out" button: applies minimum push-out to `a` along the smaller overlap axis, away from `b`'s center, and animates the move (instant if `prefers-reduced-motion`).
- Tab 2, "Circles": two draggable circles, `r1 = 16` at `(180, 115)` and `r2 = 8` at `(200, 100)`, sliders for both radii (4 to 48). Panel shows `dx`, `dy`, `dx² + dy²`, `(r1 + r2)²` and the result. A faint dashed circle of radius `r1 + r2` around circle 2 shows where circle 1's center must be to touch.

**Test values (must match exactly).**
- Presets A, B, C, D, E against `a = (100, 100, 32, 48)` give the pass or fail pattern in the lecture table: A ✓✓✓✓, B ✓✗✓✓, C ✓✗✓✓ strict and ✓✓✓✓ inclusive, D ✗✓✗✓, E ✓✓✓✓.
- Preset A: `ox = 12`, `oy = 18`; Push out moves `a` to `x = 88`.
- Preset E: `ox = 32`, `oy = 8`; Push out moves `a` to `y = 92`.
- Plus sign: four comparisons say yes; corner test says no.
- Circles tab: `(180, 115)` vs `(200, 100)` shows 625 vs 576, no; moving circle 1 to `(182, 114)` shows 520 vs 576, yes.

**Accessibility.** All controls reachable by keyboard with visible focus. A live region announces "Overlap: yes/no" on change. Respect `prefers-color-scheme` and `prefers-reduced-motion`. Use the shared tokens from `templates/interactive-tokens.css`. No game art; boxes and circles only.

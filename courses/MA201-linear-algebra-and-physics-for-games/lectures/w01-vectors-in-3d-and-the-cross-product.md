# MA201 · Week 01 — Vectors in 3D and the Cross Product

**Why this matters:** Every 3D game asks the same questions many times per frame. Which way does this surface face? Can the player stand on it? Is the enemy to my left or my right? Should the renderer bother drawing this triangle? One operation answers all four, the cross product, and three engines you will use disagree about what its answer looks like on screen.

**You will be able to:**
- Compute the cross product of two 3D vectors by hand and in code, and check the result with two dot products.
- Derive a triangle's normal and area from its three corners, and predict how swapping two corners changes both.
- Decide whether a surface is floor, wall or ceiling with a one-line test, and convert any engine's slope setting into that test.
- Explain why the same cross-product code gives opposite left/right answers in Godot and Unity, and write the test correctly for each.

**Before class:** Dunn & Parberry, *3D Math Primer for Graphics and Game Development* (2nd ed., 2011), chapter 1 on 3D coordinate spaces and left- versus right-handed conventions, and chapter 2, the sections on the cross product. Millington, *Game Physics Engine Development* (2nd ed., 2010), chapter 2, the sections on the vector product.

**Prerequisites from earlier courses:** [MA101 week 12, 2D vectors](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w12-2d-vectors.md) (add, scale, magnitude, normalize). [MA101 week 13, the dot product](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w13-dot-product-facing-and-vision-cones.md) (the threshold test `â · b̂ ≥ cos(h)` and the left-or-right perpendicular trick in 2D). [MA101 week 14, distances](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w14-distances-ranges-and-squared-distance.md) (3D distance and squared distance).

**Interactive:** [examples/w01-walkable-slope.html](../examples/w01-walkable-slope.html). Keep it open during section 3.

---

## 1. What carries over from 2D, and what does not

Everything you did with 2D vectors in MA101 works in 3D with one more component. A 3D vector is three numbers `(x, y, z)`. You add and subtract component by component, scale by multiplying each component, and measure length with Pythagoras extended by one term:

```
|v| = sqrt(x² + y² + z²)
a · b = a.x b.x + a.y b.y + a.z b.z
```

Normalizing still means dividing by the length, and the zero-vector guard from MA101 week 12 still applies. The dot product still equals `|a| |b| cos(θ)`, so every threshold test from MA101 week 13 (vision cones, "is it in front of me") works unchanged in 3D. None of that needs re-teaching. If any of it feels shaky, reread those two lectures before going on.

Two things are new in 3D.

The first is a new question. In 2D there is exactly one direction perpendicular to a line, up to sign. In 3D there is a whole plane of directions perpendicular to a single vector, but only one direction (up to sign) perpendicular to *two* vectors at once. Surfaces in games are made of triangles, and a triangle gives you two edge vectors. The direction perpendicular to both edges is the direction the surface faces. Finding it needs a new operation.

The second is a convention problem. Once you have three axes, you must decide which way each one points, and engines decided differently.

| Engine | Up axis | Forward | Handedness |
|---|---|---|---|
| Godot 4.x | +Y | −Z (`Vector3.FORWARD = (0, 0, −1)`) | right-handed |
| Unity 6 | +Y | +Z | left-handed |
| Unreal Engine 5 | +Z | +X | left-handed |
| glTF 2.0 file format | +Y | (not fixed) | right-handed |

**Handedness** describes how the three axes sit relative to each other. Point the thumb of your right hand along +X and your index finger along +Y. If +Z runs along your bent middle finger, the axes are right-handed. If it runs the other way, they are left-handed and your left hand fits instead. No rotation turns one into the other. They are mirror images.

Hold on to this table. Section 4 shows that it changes the meaning, but never the arithmetic, of the operation you are about to learn.

## 2. The cross product

The **cross product** takes two 3D vectors and returns a third vector:

```
a × b = ( a.y b.z − a.z b.y,
          a.z b.x − a.x b.z,
          a.x b.y − a.y b.x )
```

A way to remember the pattern: the x-component uses only y and z, the y-component uses only z and x, the z-component uses only x and y. Each follows the cycle x → y → z → x. The first product in each line follows the cycle forward, and the subtracted product is the same pair swapped.

Try the simplest case by hand. `(1, 0, 0) × (0, 1, 0)`:

- x: `0·0 − 0·1 = 0`
- y: `0·0 − 1·0 = 0`
- z: `1·1 − 0·0 = 1`

The result is `(0, 0, 1)`. The x-axis crossed with the y-axis gives the z-axis. The same cycle gives `y × z = x` and `z × x = y`.

### Four properties you will use every week

**It is perpendicular to both inputs.** Dot the result with `a` and you get 0. Dot it with `b` and you get 0. This is the reason the operation exists, and it is also your debugging check. If `(a × b) · a` is not zero (within float tolerance), your formula has a typo.

**Its length is the area of the parallelogram.** Draw `a` and `b` from the same point and complete the parallelogram. Then

```
|a × b| = |a| |b| sin(θ)  =  area of the parallelogram
```

where `θ` is the angle between them. A triangle is half a parallelogram, so a triangle's area is `|a × b| / 2`. Parallel vectors (θ = 0° or 180°) give a zero-length result, because the parallelogram is flat. That also means a degenerate triangle, three points on a line, has no normal. Your code has to handle that case.

**Order flips the sign.** `b × a = −(a × b)`. Swapping the inputs points the result the opposite way. This is called **anti-commutativity**, and it is the source of most cross-product bugs in games.

**It compares directions the way `sin` does, while the dot product uses `cos`.** The dot product is largest when the vectors agree. The cross product's length is largest when they are perpendicular and zero when they agree. Use the dot product to ask "how aligned?" and the cross product to ask "which way round, and how far from aligned?"

Here is the operation in code, with the perpendicularity check:

```python
def cross(a, b):
    return (a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0])

def dot(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

a, b = (2, 1, 0), (1, 3, 2)
c = cross(a, b)
print(c, dot(c, a), dot(c, b))   # (2, -4, 5) 0 0
print(cross(b, a))               # (-2, 4, -5)
```

Check the first component by hand. `a.y b.z − a.z b.y = 1·2 − 0·3 = 2`. The two zeros on the first line confirm that `c` is perpendicular to both inputs.

## 3. Worked example: the 45° ramp that some characters cannot climb

### The hook

Build a ramp that rises one meter for every meter it runs. That is a 45° slope, the most natural "steep but walkable" number a level designer can pick. Now drop three characters on it.

- A character using Godot 4.7's `CharacterBody3D` with default settings walks up it.
- A pawn in Unreal Engine 3 with the stock `WalkableFloorZ` walks up it.
- A character using Unreal Engine 5's `CharacterMovementComponent` with default settings cannot. The ramp counts as a wall, and the character slides back down.

Unreal 5's editor shows the reason if you look. The default "Walkable Floor Angle" is 44.765°, not 45°. Where does a number like 44.765 come from? From a cross product, a dot product and a cosine. Once you see the model, you can read any engine's slope setting, predict which ramps work, and stop filing bug reports about "random" sliding.

### The model

A surface in a game is a mesh of triangles. Each triangle has three corners `a`, `b`, `c`. To decide whether a character may stand on it, the engine needs three things.

1. **Two edges from one corner.** `e1 = b − a` and `e2 = c − a`.
2. **The normal.** `n = e1 × e2`. The **normal** is the direction the surface faces. Normalize it: `n̂ = n / |n|`. The corner order `a → b → c` decides which of the two possible directions you get (section 4 returns to this).
3. **The walkable test.** With `û` as the world's unit up vector and `θmax` the steepest walkable slope,

```
walkable  ⇔  n̂ · û ≥ cos(θmax)
```

The slope angle of a surface is the angle between its normal and straight up. A flat floor's normal points straight up, so the angle is 0° and `n̂ · û = 1`. A vertical wall's normal is horizontal, so the angle is 90° and `n̂ · û = 0`. This is the MA101 week 13 cone test turned upside down. The "guard" is the up vector, the "cone" is the set of walkable normals, and `cos(θmax)` is the threshold.

Engines store this threshold in one of two forms. Some store the angle and compute the cosine. Some store the cosine directly. Unreal's source keeps both, `WalkableFloorAngle` in degrees and `WalkableFloorZ` as the cosine. In a Z-up engine, `n̂ · û` is just the normal's z-component, which is why Unreal calls the threshold a "Z".

Now the 44.765° is no mystery. In the Unreal Engine 5.3 source (read from a public mirror, see Sources), the character movement component's constructor sets `WalkableFloorZ` to 0.71, and the angle is derived from it as `acos(0.71)`:

```
acos(0.71) = 44.765°
```

Someone picked a round cosine, not a round angle. The cosine of 45° is `1/√2 = 0.70711`, which is just below 0.71. So a perfect 45° ramp fails the default test by 0.0029.

Unreal Engine 3 made the opposite rounding. Its base `Pawn` class, in a third-party copy of the UDK-era source, sets `WalkableFloorZ=0.7`, with a source comment calling it roughly a 45 degree angle. `acos(0.7) = 45.573°`, so the 45° ramp passes. Godot stores an angle, 45° by default, and allows a tolerance of 0.01 radians (0.573°) when it classifies a collision, giving an effective limit of 45.573°. Godot and UE3 land on almost the same number from opposite directions.

### Numbers you can check

Use a Y-up world, `û = (0, 1, 0)`. Build each ramp as one triangle with `a = (0, 0, 0)`, `b = (0, 0, 1)` and `c = (run, rise, 0)`. Then `e1 = (0, 0, 1)`, `e2 = (run, rise, 0)`, and the cross product works out to `n = (−rise, run, 0)`. Check that by hand once with the formula from section 2. It is the fastest way to trust the rest of the table.

Because `û` is the y-axis, `n̂ · û` is just `run / |n|`.

| Ramp (rise : run) | n | \|n\| | n̂ · û | Slope angle | UE5 default (≥ 0.71) | UE3 Pawn (≥ 0.70) | Godot 4.7 (≤ 45.573°) |
|---|---|---|---|---|---|---|---|
| 1 : 4 | (−1, 4, 0) | 4.123 | 0.970 | 14.04° | floor | floor | floor |
| 1 : 2 | (−1, 2, 0) | 2.236 | 0.894 | 26.57° | floor | floor | floor |
| 3 : 4 | (−3, 4, 0) | 5.000 | 0.800 | 36.87° | floor | floor | floor |
| 1 : 1 | (−1, 1, 0) | 1.414 | 0.7071 | 45.00° | **wall** | floor | floor |
| 1.01 : 1 | (−1.01, 1, 0) | 1.421 | 0.7036 | 45.29° | **wall** | floor | floor |
| 6 : 5 | (−6, 5, 0) | 7.810 | 0.640 | 50.19° | wall | wall | wall |
| 1 : 0 (vertical) | (−1, 0, 0) | 1.000 | 0.000 | 90.00° | wall | wall | wall |

Three things to notice.

The two bold rows are the whole story of the hook. Any ramp between 44.765° and 45.573° is walkable in Godot and UE3 and not in UE5. That window is less than one degree wide, and a designer's "45°" ramp sits in it.

The slope angle column is there so you can read the table. The engine never needs it. Unreal compares the normal's z-component with 0.71 directly, no `acos` needed. (Godot does call `acos` in this code path, which costs a little more and changes nothing about the result.)

The triangle's area is `|n| / 2`. The 3 : 4 ramp triangle has area 2.5 square meters. You will use this in the lab to weight surfaces by area.

Here is the same computation as code. It prints the 1 : 1 row.

```python
import math

def cross(a, b):
    return (a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0])

def sub(a, b):
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def normal(a, b, c):
    n = cross(sub(b, a), sub(c, a))
    length = math.sqrt(n[0]**2 + n[1]**2 + n[2]**2)
    return (n[0]/length, n[1]/length, n[2]/length)

UP = (0.0, 1.0, 0.0)
n = normal((0, 0, 0), (0, 0, 1), (1, 1, 0))
up_dot = n[0]*UP[0] + n[1]*UP[1] + n[2]*UP[2]
print(round(up_dot, 4))                           # 0.7071
print("UE5 floor:", up_dot >= 0.71)               # UE5 floor: False
print("UE3 floor:", up_dot >= 0.70)               # UE3 floor: True
print(round(math.degrees(math.acos(0.71)), 3))    # 44.765
```

### Flip two corners

Now list the same 1 : 1 ramp's corners as `a, c, b` instead of `a, b, c`. The edges swap, the cross product flips sign, and `n = (1, −1, 0)`. The normal points down into the ground. `n̂ · û = −0.707`, far below any threshold.

Godot's classifier has a third answer for this case. It first checks the angle to `û`, then the angle to `−û`. A normal within 45.573° of straight *down* is a **ceiling**. So the same geometry, with two corners swapped, turns a floor into a ceiling. In a real engine the physics collider usually supplies the normal and this does not happen by accident. In your own tools and in the lab, it will. Section 4 explains how engines decide which order is "correct".

### The visual

Open [examples/w01-walkable-slope.html](../examples/w01-walkable-slope.html). The left view draws the ramp triangle in 3D with its two edge vectors, the parallelogram they span, and the normal arrow. The right view plots `n̂ · û` against the slope angle from 0° to 180°. It is a cosine curve, with three horizontal lines, one per engine preset.

Drag the rise slider. On the left the ramp tilts and the normal leans. On the right the marker slides along the curve. The test is a horizontal line cut across a cosine, exactly like the vision cone in MA101 week 13. Now zoom the right view to 44° to 46°. The UE5 line separates from the other two, and a 1 : 1 ramp sits between them. The UE3 and Godot lines still overlap, because 0.70 and `cos(45° + 0.01 rad) = 0.7000005` differ only in the seventh decimal, so the Godot line is drawn dashed on top. Press "swap b and c". The normal arrow flips through the ramp, the parallelogram's shading changes to its back-face colour, and the marker jumps to 135° on the curve, where Godot's ceiling band is shaded.

### Cross-game recognition

The same test hides behind every engine's slope setting. The skill is to rewrite each one as `n̂ · û ≥ c` and read off `c`.

**Unreal Engine 5 (5.3 source).** `UCharacterMovementComponent::IsWalkable` rotates the hit normal into gravity space and returns false when its z-component is below `WalkableFloorZ`. The constructor sets `WalkableFloorZ` to 0.71. Here `c = 0.71` is stored directly, and `SetWalkableFloorAngle` converts an angle to it with `cos`. Individual meshes may override the threshold through a "walkable slope override", which is the same test with a per-surface `c`.

**Unreal Engine 3 (UDK-era source, for example as released with Renegade X).** `Pawn.uc` sets `WalkableFloorZ=0.7`. Same model, `c = 0.70`.

**Godot 4.7.** `CharacterBody3D` has `floor_max_angle`, in radians, defaulting to 45°, and `up_direction`, defaulting to `Vector3.UP`. The classifier compares the collision's angle to `up_direction` with `floor_max_angle + 0.01`. This is the angle form of the same test, with `c = cos(45.573°) = 0.700`. Because `up_direction` is a parameter, you can build a game where "up" rotates (walking on the inside of a space station) without touching the test.

**Unity 6.** The `CharacterController` component has a Slope Limit in degrees, and the manual describes it as the steepest slope the collider will climb. That is `θmax` in angle form. The manual does not document the internal comparison, so you cannot tell from it whether a slope exactly at the limit counts. Test it in the engine before you build a level around it.

Four engines, four names (`WalkableFloorZ`, `floor_max_angle`, Slope Limit, and the UE3 version of the same field), one test. When a new engine hands you a slope setting, ask whether it is stored as an angle or a cosine and whether the comparison includes the boundary.

### Eyes-open design judgment

A threshold on `n̂ · û` is the right default for "can I stand here?" It is one dot product per contact, it has no special cases, and you can tune it per surface. Decide these on purpose:

- **Never build geometry on the threshold.** The table shows that "45°" means floor in one engine and wall in another. Pick a limit, then author ramps at least 2° to 3° inside it and cliffs at least 2° to 3° outside it. Players forgive a rule they can learn and hate one that works on Tuesday's build and not Wednesday's.
- **Choose the form that avoids surprises.** Storing the cosine (Unreal) skips `acos` at runtime but gives designers a number like 44.765 in the editor. Storing the angle (Godot) is readable but invites "45 exactly" ramps. Whichever you pick, show both numbers in your tools.
- **Walkable is a design verb.** A slope limit decides where players can go, so it is level design. Steep-but-climbable slopes open shortcuts and sequence breaks. A lower limit makes terrain more of a barrier and puts more weight on paths and stairs. Tune it with the level designers, not after them.
- **Per-surface overrides beat a global change.** If one ice slope must be unclimbable, give that surface its own threshold (Unreal's walkable slope override) instead of lowering the global limit and breaking every other ramp.

### Check yourself (worked example)

1. A studio wants its Unreal 5 characters to climb exactly 50° and no more. What should `WalkableFloorZ` be?
2. A triangle has corners `a = (0, 0, 0)`, `b = (0, 0, 2)`, `c = (3, 4, 0)` in a Y-up world. Compute its unit normal and slope angle. Is it a floor in UE5 and in Godot 4.7 defaults?
3. Your tool reports a floor triangle as a ceiling. Name the most likely cause and a one-line fix.

<details>
<summary>Answers</summary>

1. `cos(50°) = 0.643`. Any walkable surface has `n̂ · û ≥ 0.643`.
2. `e1 = (0, 0, 2)`, `e2 = (3, 4, 0)`, `n = (0·0 − 2·4, 2·3 − 0·0, 0·4 − 0·3) = (−8, 6, 0)`, `|n| = 10`, `n̂ = (−0.8, 0.6, 0)`. `n̂ · û = 0.6`, slope angle `acos(0.6) = 53.13°`. A wall in both.
3. The corners are in the opposite winding order from the one your code assumes, so the cross product points down. Swap the operands (`(c − a) × (b − a)`), or swap two corners when you load the mesh, to match your engine's convention.

</details>

## 4. Handedness and winding: same arithmetic, different pictures

### Winding order decides the front

The **winding order** of a triangle is the order its corners appear in, clockwise or counter-clockwise, as seen from a given side. The cross product turns winding into a direction. In a right-handed coordinate system, if the corners appear counter-clockwise from where you stand, `(b − a) × (c − a)` points toward you.

Renderers use this to skip work. A closed mesh, such as a character or a crate, shows you only its outside. Triangles facing away from the camera are hidden behind the ones facing it, so the GPU can drop them before drawing. This is **back-face culling**, and it needs a rule for which winding counts as the front:

| System | Front face by default |
|---|---|
| OpenGL (`glFrontFace`) | counter-clockwise |
| Direct3D 11 (`FrontCounterClockwise = FALSE`) | clockwise |
| Unity 6 | clockwise |
| Godot 4.x (`ArrayMesh`, `SurfaceTool`) | clockwise |
| glTF 2.0 files | counter-clockwise, unless the node's transform mirrors the mesh |

When you import a mesh and see the inside of it (faces missing on the near side, visible on the far side), the winding convention is wrong for that engine. Every triangle's normal points inward, and culling removes exactly the faces you wanted.

Godot shows how carefully engines track this. Its vector maths tutorial computes a triangle normal as `(b − a).cross(c − a)`. Its own `Plane` constructor, which the docs say takes three points "given in clockwise order", computes the normal with the operands the other way round, `(a − c).cross(a − b)`, which equals `(c − a) × (b − a)`. The engine is right-handed and treats clockwise as front, so it needs the reversed order to make normals point out of the front face. Neither snippet is wrong. They answer different questions, and you have to know which one you are asking.

### Left or right of me, in 3D

MA101 week 13 showed a 2D left-or-right test using a perpendicular dot product. The 3D version uses the cross product. With `f` as your forward direction, `d` as the direction to the target and `û` as up, compute

```
side = (f × d) · û
```

The sign tells you the side. The size is `|f| |d| sin(θ)` times how vertical `f × d` is, so for level ground and unit vectors it is the sine of the turn angle. This is how a turret in 3D knows whether to yaw left or right before it uses the `atan2` method from MA101 week 11 to get the exact angle.

But which sign means "right"? Put a target directly to the character's right and compute:

| Engine | f (forward) | d (to the right) | f × d | side | Positive means |
|---|---|---|---|---|---|
| Godot 4.x | (0, 0, −1) | (1, 0, 0) | (0, −1, 0) | −1 | left |
| Unity 6 | (0, 0, 1) | (1, 0, 0) | (0, 1, 0) | +1 | right |
| Unreal 5 | (1, 0, 0) | (0, 1, 0) | (0, 0, 1) | +1 | right |

The formula did the same arithmetic three times. What changed is where each engine puts "forward" and "right". In both left-handed engines, positive means right. In right-handed Godot, positive means left. Unity's own documentation for `Vector3.Cross` tells you to find the result's direction with the "left hand rule". The documentation is telling you the picture, not changing the formula.

So when you port steering code from one engine to another ([CS203 week 2](../../CS203-artificial-intelligence-for-games/lectures/w02-steering-behaviors.md) blends turn requests from several behaviors), the cross product will not raise an error. It will quietly turn your enemies the wrong way. Write one test with a known target on the right, run it in each engine, and keep it.

### The cross product builds coordinate frames

One more job, which week 3 depends on. Given a forward direction `f` and a rough up `û`, you can build three perpendicular axes for a camera or a character:

```
right = normalize(f × û)        (right-handed convention; swap for left-handed)
up'   = right × f
```

The first cross product gives a direction perpendicular to both forward and world up, which is sideways. The second gives a true up that is perpendicular to forward, even if forward tilts. This is what "look at" functions do inside every engine. It fails when `f` is parallel to `û` (looking straight up or down), because the cross product has zero length. That is why cameras in many games stop just short of vertical. You will build these frames into matrices next week.

## 5. Cost and precision

The cross product costs six multiplications and three subtractions. A normalize adds a square root and three divisions. Two practical consequences follow.

**Precompute normals for static geometry.** A level's floor does not move, so its triangle normals are computed once, at import or load time, and stored. The per-frame walkable test is then one dot product and one comparison. Engines store normals in the mesh for exactly this reason.

**Compare before you normalize when you can.** If you only need the sign of `n · û` (for example, "does this face point up at all?"), skip the normalize. The sign does not depend on length. If you need the threshold test without a square root, square both sides with care. For `c > 0`, `n̂ · û ≥ c` is the same as `n · û ≥ 0` and `(n · û)² ≥ c² |n|²`. This is the squared-distance idea from MA101 week 14, applied to angles.

**Watch tiny triangles.** A sliver triangle has two nearly parallel edges, so `|n|` is close to 0. Dividing by it amplifies float error, and the normal can point anywhere. Real meshes contain such triangles. Guard the normalize (return "no normal" below a small length) and skip those triangles in floor checks. The lab's test mesh contains one.

## In-class activity (25 minutes)

Work in pairs with the interactive and paper.

1. Your team's game uses Godot 4.7 defaults. A level designer sends you six ramps as rise : run pairs: 1 : 3, 5 : 6, 1 : 1, 21 : 20, 7 : 6, 3 : 2. For each, compute `n̂ · û` and the slope angle, and classify it as floor or wall.
2. The team is moving to Unreal 5. Which of the six ramps change class? Propose one `WalkableFloorZ` that keeps every ramp's class the same as in Godot, or explain why none exists.
3. Write a one-paragraph rule for the level designers ("ramps must be at most ..., cliffs at least ..."). Include one number in degrees and one in rise : run.
4. Swap rules with another pair. Find one ramp that satisfies their rule and still behaves differently in the two engines, or confirm there is none.

Expected output: a six-row table, the proposed `WalkableFloorZ` with its angle, and the one-paragraph rule.

## Common misconceptions

- **"`a × b` and `b × a` are the same, like multiplication."** They point in opposite directions. Swapping operands flips normals, flips culling, and flips left and right.
- **"Left-handed engines use a different cross product formula."** Every engine uses the same component formula. Handedness changes how the axes are drawn, so the same numbers look like a left-hand-rule result on screen. Your code does not change. Your interpretation of the sign does.
- **"The slope limit is an angle, so the engine computes an angle."** Many engines store and compare the cosine (Unreal's `WalkableFloorZ`). The angle in the editor is a display value derived from it, which is why it can read 44.765.
- **"The cross product's length does not matter, only its direction."** Its length is twice the triangle's area. That is useful (area weighting, spotting degenerate triangles) and dangerous (a near-zero length means an unreliable direction).

## Check yourself

1. Compute `(1, 2, 3) × (4, 5, 6)` and verify your answer with two dot products.
2. A triangle has corners `(1, 0, 0)`, `(0, 1, 0)` and `(0, 0, 1)`. Find its area and its unit normal for the order given. Is this face a floor in UE5 with Z as up?
3. In Unity, an enemy faces `f = (0, 0, 1)`. The player is at relative position `d = (−3, 0, 4)`. Compute `(f × d) · û` with `û = (0, 1, 0)`. Should the enemy turn left or right?
4. An engine stores the walkable threshold as a cosine, 0.8. A designer asks for "about 5° steeper". What new value do you give them?
5. A mirrored copy of a statue (scale −1 on x) renders inside-out. Using winding order, explain why.

<details>
<summary>Answers</summary>

1. `(2·6 − 3·5, 3·4 − 1·6, 1·5 − 2·4) = (−3, 6, −3)`. Check: `(−3, 6, −3) · (1, 2, 3) = −3 + 12 − 9 = 0` and `(−3, 6, −3) · (4, 5, 6) = −12 + 30 − 18 = 0`.
2. `e1 = (−1, 1, 0)`, `e2 = (−1, 0, 1)`, `n = (1·1 − 0·0, 0·(−1) − (−1)·1, (−1)·0 − 1·(−1)) = (1, 1, 1)`. `|n| = √3 = 1.732`, area `0.866`. `n̂ = (0.577, 0.577, 0.577)`. With Z up, `n̂ · û = 0.577 < 0.71`, slope 54.7°, so it is a wall.
3. `f × d = (0·4 − 1·0, 1·(−3) − 0·4, 0·0 − 0·(−3)) = (0, −3, 0)`, so `side = −3`. In Unity (left-handed) positive means right, so negative means turn left. The player is 36.9° to the left, and `side / |d| = −0.6 = −sin(36.9°)`.
4. `acos(0.8) = 36.87°`. Add 5° for 41.87°, and `cos(41.87°) = 0.745`. Lowering the cosine allows steeper slopes.
5. Mirroring reverses the apparent order of every triangle's corners, so counter-clockwise becomes clockwise as seen from outside. The cross product of each face now points inward, and back-face culling removes the outside faces. Engines fix this by flipping the front-face rule when a transform mirrors (glTF 2.0 does it by the sign of the transform's determinant, which you meet next week).

</details>

## Lab / assignment hook

[Lab 01, floor, wall or ceiling](../labs/lab01.md). Implement a small 3D vector module with cross product, triangle normal and area, then classify every triangle of a test level mesh as floor, wall or ceiling under three engine presets. Report the total walkable area under each preset and find the triangles that change class. Deliverable: the completed Python file passing the tests, and a 250-word memo recommending a slope limit to your level designers.

## Sources

- Godot Engine documentation and source, version 4.7 (stable 4.7.2, accessed September 2026). `CharacterBody3D.floor_max_angle` defaults to 45 degrees, `up_direction` defaults to `Vector3.UP`; `scene/3d/physics/character_body_3d.cpp` classifies a collision as floor when its angle to `up_direction` is at most `floor_max_angle + FLOOR_ANGLE_THRESHOLD`, with the threshold defined as 0.01, and as ceiling by the same test against `-up_direction`. `Vector3.FORWARD = (0, 0, -1)`, `UP = (0, 1, 0)`. "Introduction to 3D": right-handed coordinate system with Y up. "Vector math" tutorial: triangle normal as `(b - a).cross(c - a)`. `ArrayMesh` and `SurfaceTool` notes: clockwise winding for front faces. `Plane(point1, point2, point3)`: points in clockwise order; `core/math/plane.h` computes `(p1 - p3).cross(p1 - p2)` for clockwise.
- Unreal Engine 5.3.2 source (Engine/Source/Runtime/Engine, `CharacterMovementComponent.cpp` and `.h`). Read from a public third-party mirror of the source on GitHub, not from Epic's own repository or documentation, which require an account; accessed September 2026. Constructor calls `SetWalkableFloorZ(0.71f)`; `SetWalkableFloorZ` sets the angle to `acos` of the value; `IsWalkable` rejects hits whose gravity-relative normal Z is below `WalkableFloorZ`; per-component walkable slope overrides. Engine source comments in the GLTF importer and Datasmith describe Unreal as left-handed with Z up.
- Unreal Engine 3 script source, `Engine/Classes/Pawn.uc` (UDK era). Read from the copy in the Renegade X source release by Totem Arts, a third-party mirror, not from an Epic publication; accessed September 2026. `WalkableFloorZ=0.7` with a comment that 0.7 is about a 45 degree angle.
- Unity documentation, Unity 6.6 (accessed September 2026). Scripting reference `Vector3.Cross` (direction by the left hand rule; magnitude is the product of magnitudes times the sine of the angle; triangle-normal example). Manual "Character Controller component" (Slope Limit in degrees). Manual "Mesh index data" (clockwise winding is front facing; back faces culled by default).
- Khronos, OpenGL 4 reference page `glFrontFace` (initial value `GL_CCW`).
- Microsoft Learn, `D3D11_RASTERIZER_DESC` (default `FrontCounterClockwise` is FALSE, so clockwise triangles are front-facing).
- Khronos, glTF 2.0 Specification (right-handed coordinate system; the sign of the node's global transform determinant selects counterclockwise or clockwise front faces).
- Dunn, F. & Parberry, I. (2011). *3D Math Primer for Graphics and Game Development*, 2nd ed. CRC Press.
- Millington, I. (2010). *Game Physics Engine Development*, 2nd ed. Morgan Kaufmann.
- The ramp triangles and the activity's designer requests are invented for teaching.

## Interactive spec: examples/w01-walkable-slope.html

**The one insight:** a walkable-slope rule is a horizontal line across a cosine curve of `n̂ · û`, and three engines draw that line less than one degree apart, so a "45°" ramp is a floor in one and a wall in another. Flipping the triangle's winding flips the normal and sends the same ramp to the ceiling band.

**Layout.** Two linked views side by side at 1280 px, stacked at 390 px (3D view on top).

- **Left, "Ramp":** an oblique 3D drawing (fixed camera, simple orthographic projection, no WebGL required; draw with 2D canvas or SVG). Y is up. Draw a ground grid on the XZ plane from −1 to 3 on x and −1 to 2 on z. Draw the triangle with corners `a = (0, 0, 0)`, `b = (0, 0, 1)`, `c = (run, rise, 0)`. Draw `e1 = b − a` and `e2 = c − a` as arrows from `a`, and shade the parallelogram `a, b, b + e2, c` at 15% opacity. Draw the unit normal `n̂` as an arrow of length 1 from the triangle's centroid. Front face (normal toward the camera side of the plane) uses the accent colour, back face uses a muted hatch colour. Label each corner.
- **Right, "Up-dot curve":** x-axis slope angle 0° to 180°, y-axis `n̂ · û` from −1 to 1, plotting `cos(angle)`. Draw three horizontal threshold lines: UE5 default at 0.71, UE3 Pawn at 0.70, Godot 4.7 at `cos(45° + 0.01 rad) = 0.7000005` (label it "Godot 4.7, 45° + 0.01 rad"). The UE3 and Godot lines coincide at any zoom, so draw the Godot line dashed on top of the solid UE3 line and label the pair as overlapping. Shade the floor band (`y ≥` the selected engine's threshold) in one colour and the ceiling band (`y ≤ −threshold`) in another, walls neutral. A marker shows the current triangle. A "zoom 44° to 46°" toggle rescales the x-axis to that window and the y-axis to 0.69 to 0.72 so the UE5 line separates visibly from the UE3 and Godot pair.

**Readouts (copyable text):** `e1`, `e2`, `n = e1 × e2` (3 decimals), `|n|`, triangle area `|n|/2`, `n̂`, `n̂ · û` (4 decimals), slope angle (2 decimals), and a three-cell verdict row: UE5 / UE3 / Godot 4.7 each showing "floor", "wall" or "ceiling". UE rules: floor if `n̂ · û ≥ Z`, else wall (UE does not report ceilings from this test; show "wall"). Godot rule: floor if angle to up ≤ 45.573°, else ceiling if angle to down ≤ 45.573°, else wall.

**Controls (keyboard accessible, labelled):**

1. Rise: slider 0 to 6, step 0.01, default 1. The range must reach the 6 : 5 preset.
2. Run: slider 0 to 6, step 0.01, default 1. The range must reach the 3 : 4 preset. If rise and run are both 0, show "degenerate triangle: no normal" and hide the marker.
3. Preset buttons for rise : run: 1:4, 1:2, 3:4, 1:1, 1.01:1, 6:5, vertical (run 0, rise 1).
4. "Swap b and c" toggle (winding flip). When on, `n = (c − a) × (b − a)`.
5. Selected engine for band shading: UE5, UE3, Godot 4.7, Custom. Custom shows an angle slider 0° to 90° step 0.1° that sets the threshold to `cos(angle)`.
6. Zoom toggle (see above).

**Test values (must match):** 1:1 → `n = (−1, 1, 0)`, `n̂ · û = 0.7071`, angle 45.00°, verdict UE5 wall, UE3 floor, Godot floor. 1.01:1 → `0.7036`, 45.29°, same verdicts. 3:4 → `n = (−3, 4, 0)`, `|n| = 5`, area 2.5, `0.8000`, 36.87°, all floor. 6:5 → `0.6402`, 50.19°, all wall. Vertical → `0.0000`, 90.00°, all wall. 1:1 with swap → `n = (1, −1, 0)`, `−0.7071`, 135.00°, UE5 wall, UE3 wall, Godot ceiling.

**First screen.** Load at 1:1 with zoom on, so the marker is visibly between the UE5 line and the other two, and the verdict row already reads "wall / floor / floor". Caption above the views: "Same ramp, three engines. Move the slope, then swap two corners."

**Accessibility and motion.** Arrow keys adjust sliders; all readouts update on input. No animation needed; under `prefers-reduced-motion` do not tween the marker.

# MA201 · Week 05 — Quaternions for Rotation (Intuition First)

**Why this matters:** Every 3D engine you will use stores rotations as four numbers called a quaternion, while its editor shows you three angles. When a turret spins the long way round, a camera flips at the top of a look, or an imported animation twists a wrist through 360°, the bug lives in the gap between those two views. You do not need the abstract algebra to close that gap. You need three facts and one sign check.

**You will be able to:**
- Build the quaternion for a rotation of any angle about any axis, and read the angle and axis back out of a quaternion an engine prints.
- Rotate a vector with a quaternion and compose two rotations in the right order, checking the result against a rotation matrix from week 2.
- Explain gimbal lock with a numerical example in a named Euler order, and decide when Euler angles are still the right tool.
- Compute a slerp between two orientations, detect the "long way round" from the sign of a dot product, and fix it.

**Before class:** Dunn & Parberry, *3D Math Primer for Graphics and Game Development* (2nd ed., 2011), chapter 8, sections 8.3 (Euler angles, including gimbal lock) and 8.5 (quaternions) up to and including slerp. Skip the proofs on a first read. Re-read MA201 week 2 on rotation matrices.

**Prerequisites from earlier courses:** [MA101 week 11, atan2 and turning toward a target](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w11-atan2-turning-toward-a-target.md) (the shortest signed angle difference, which this week lifts into 3D). [MA101 week 13, the dot product](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w13-dot-product-facing-and-vision-cones.md) (dot product as cosine of an angle). [MA101 week 8, lerp](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w08-interpolation-lerp-inverse-lerp-remap.md). MA201 [week 1](w01-vectors-in-3d-and-the-cross-product.md) (cross product), [week 2](w02-matrices-and-linear-transformations.md) (rotation matrices) and [week 4](w04-homogeneous-coordinates-and-projection.md) (the column-vector convention used here).

**Interactive:** [`examples/w05-slerp-long-way.html`](../examples/w05-slerp-long-way.html). Keep it open during section 4.

---

## 1. Three ways to store a rotation

A rotation in 3D has three degrees of freedom. Two numbers say which way the thing points, and one more says how it is rolled around that direction. Games store it in one of three forms.

**Euler angles.** Three angles, usually called yaw (turn left or right, about the up axis), pitch (look up or down, about the side axis) and roll (tilt, about the forward axis). They are what a designer types into an inspector. Their weakness is that "rotate by yaw, pitch and roll" is incomplete. You must also say **in what order** and **about which axes** (the object's own axes or the world's). Engines disagree:

- Unity's documentation for `Transform.eulerAngles` says rotations are performed around the Z axis, then the X axis, then the Y axis, in that order.
- Godot's `Node3D.rotation_order` defaults to YXZ, and its documentation says the rotations are intrinsic, about the object's local axes.

Copy three numbers from one engine to the other and you can get a different orientation.

**Rotation matrices.** Nine numbers, the 3×3 block from week 4. They are exact and fast to apply to a vector, and composing two rotations is one matrix product. But nine numbers for three degrees of freedom leaves room for error. After thousands of multiplications, rounding makes the matrix slightly non-rotational (columns no longer exactly unit length or perpendicular), and fixing that needs a re-orthogonalization step. Interpolating two matrices entry by entry also gives something that is not a rotation.

**Quaternions.** Four numbers. Unity's `Quaternion` reference states that Unity uses quaternions internally for all rotations. Godot's `Node3D` keeps a basis matrix and offers `Quaternion` for rotation math. glTF, the standard 3D interchange format, stores every node rotation and every animated rotation as a unit quaternion. Four numbers for three freedoms leaves one extra, and that extra is easy to fix: scale the four numbers so their squares sum to 1.

### Gimbal lock, with numbers

Euler angles have one more problem that no choice of order removes. Take Godot's YXZ order, where the orientation is `R = R_y(yaw) · R_x(pitch) · R_z(roll)` with column vectors. Set pitch to exactly 90°, so the object looks straight up. Now compare two settings:

| Yaw | Pitch | Roll | Resulting quaternion (w, x, y, z) |
|---|---|---|---|
| 30° | 90° | 0° | (0.6830, 0.6830, 0.1830, −0.1830) |
| 0° | 90° | −30° | (0.6830, 0.6830, 0.1830, −0.1830) |

Different angles, identical orientation. With the object pitched straight up, its local forward axis (the roll axis) lies along the world up axis (the yaw axis). Yaw and roll now turn it about the same line, so one of the three degrees of freedom has disappeared. That is **gimbal lock**. The name comes from mechanical gimbals, three nested rings on pivots, where two rings line up and jam one direction of motion.

Gimbal lock is not a bug in the numbers. It is a property of every three-angle description. Near the locked pitch, a small change in orientation can need a huge change in yaw and roll. That is why an animation curve that passes near pitch 90° suddenly spins, and why a flight game that stores Euler angles cannot fly a loop smoothly.

## 2. What the four numbers mean

Forget the algebra for a moment. Any rotation, however complicated, is a single turn by some angle `θ` about some axis `n̂` (a unit vector). This is **Euler's rotation theorem**. A quaternion is that axis and angle, packed like this:

```
q = (w, x, y, z) = ( cos(θ/2),  sin(θ/2)·n̂ )
```

- `w` is the **scalar part**, `cos(θ/2)`.
- `(x, y, z)` is the **vector part**, the axis scaled by `sin(θ/2)`.
- Because `cos² + sin² = 1` and `n̂` has length 1, `w² + x² + y² + z² = 1`. Rotations are **unit quaternions**.

Three facts carry you through almost everything in a game.

**Fact 1: the angle is halved.** A 90° turn about the up axis `(0, 1, 0)` is `(cos 45°, 0, sin 45°, 0) = (0.7071, 0, 0.7071, 0)`. Print the rotation of a Unity or Godot object you turned 90° in the inspector and you will see those 0.7071s. Read them backwards: `θ = 2·acos(w)` and `n̂ = (x, y, z) / sin(θ/2)`.

**Fact 2: q and −q are the same rotation.** Negate all four numbers of `(0.7071, 0, 0.7071, 0)` and you get `(−0.7071, 0, −0.7071, 0)`. That is `θ = 2·acos(−0.7071) = 270°` about the axis `(0, −1, 0)`, which is a 90° turn about `(0, 1, 0)` again. Every orientation has exactly two quaternions, one the negative of the other. This is called the **double cover**. It is harmless when you apply a rotation and causes the main bug of section 4 when you interpolate.

**Fact 3: the dot product measures the turn between two orientations.** For unit quaternions `a` and `b`, `a · b = aw·bw + ax·bx + ay·by + az·bz`, and

```
|a · b| = cos(φ / 2)
```

where `φ` is the angle of the single rotation that takes orientation `a` to orientation `b`. It is the MA101 week 13 dot product again, one dimension up, with the half angle.

The table shows yaw turns about `(0, 1, 0)` against the identity `(1, 0, 0, 0)`:

| Turn | q = (w, x, y, z) | Dot with identity |
|---|---|---|
| 0° | (1.0000, 0, 0.0000, 0) | 1.0000 |
| 20° | (0.9848, 0, 0.1736, 0) | 0.9848 |
| 90° | (0.7071, 0, 0.7071, 0) | 0.7071 |
| 180° | (0.0000, 0, 1.0000, 0) | 0.0000 |
| 270° | (−0.7071, 0, 0.7071, 0) | −0.7071 |
| 340° | (−0.9848, 0, 0.1736, 0) | −0.9848 |
| 360° | (−1.0000, 0, 0.0000, 0) | −1.0000 |

A full 360° turn gives `−1`, not `+1`. It is the same orientation as no turn at all, stored with the other sign. And 340° and 20° have dot products of opposite sign and equal size: the same pair of orientations, 20° apart, reached two different ways.

### Why half? A picture instead of a proof

The formula that rotates a vector `v` by `q` uses `q` twice:

```
v' = q · (0, v) · q*        where q* = (w, −x, −y, −z) is the conjugate
```

Here `·` is the **quaternion product** (written out in code below), and `(0, v)` is the vector written as a quaternion with zero scalar part. Each of the two multiplications turns `v` by half the angle, so the pair gives the full `θ`. You do not need to derive this. You need to remember that the stored angle is half the visible one, and that multiplying twice is why.

### Composing rotations

The quaternion product composes rotations, like the matrix product in week 2. With the same column-vector convention, `q2 · q1` means "apply `q1` first, then `q2`", and order matters. Here is the whole toolkit in about twenty lines. Engines add speed and conveniences, but this is the arithmetic.

```python
import math

def from_axis_angle(axis, deg):
    h = math.radians(deg) / 2
    s = math.sin(h)
    return (math.cos(h), axis[0] * s, axis[1] * s, axis[2] * s)

def mul(a, b):
    w1, x1, y1, z1 = a
    w2, x2, y2, z2 = b
    return (w1*w2 - x1*x2 - y1*y2 - z1*z2,
            w1*x2 + x1*w2 + y1*z2 - z1*y2,
            w1*y2 - x1*z2 + y1*w2 + z1*x2,
            w1*z2 + x1*y2 - y1*x2 + z1*w2)

def conj(q):
    return (q[0], -q[1], -q[2], -q[3])

def rotate(q, v):
    return mul(mul(q, (0.0, *v)), conj(q))[1:]

def r(t):
    return tuple(round(x, 4) + 0.0 for x in t)

UP, RIGHT = (0, 1, 0), (1, 0, 0)
yaw90 = from_axis_angle(UP, 90)
pitch90 = from_axis_angle(RIGHT, 90)
print("yaw90       ", r(yaw90))
print("turn x axis ", r(rotate(yaw90, (1, 0, 0))))
print("pitch then yaw, forward ->", r(rotate(mul(yaw90, pitch90), (0, 0, -1))))
print("yaw then pitch, forward ->", r(rotate(mul(pitch90, yaw90), (0, 0, -1))))
```

Output:

```
yaw90        (0.7071, 0.0, 0.7071, 0.0)
turn x axis  (0.0, 0.0, -1.0)
pitch then yaw, forward -> (0.0, 1.0, 0.0)
yaw then pitch, forward -> (-1.0, 0.0, 0.0)
```

The second line matches week 4, where `rot_y(90)` sent `(1, 0, 0)` to `(0, 0, −1)`. The last two lines show order at work. Pitch the forward vector `(0, 0, −1)` up first and it points at the sky, where a yaw about the up axis leaves it alone. Yaw first and it points along −x, where a pitch about the world x axis leaves it alone.

## 3. From three angles to four numbers and back

Engines convert constantly. The inspector shows Euler angles, the transform stores a quaternion or matrix, and the conversion follows the engine's order. For Godot's YXZ it is exactly the composition above:

```
q = q_y(yaw) · q_x(pitch) · q_z(roll)
```

Converting back from a quaternion to Euler angles has no unique answer near gimbal lock (section 1 showed two answers for one orientation). Engines pick one, which is why an inspector sometimes shows `(180, 0, 180)` for an object you rotated to `(0, 180, 0)`. Both describe the same orientation. If your gameplay code reads Euler angles back out of a transform and compares them with a number, it will break when the engine picks the other triple. Read orientation as vectors (the object's forward and up) or as quaternions, and compare those.

## 4. Worked example: the turret that spins the long way

### The hook

A defense turret in a third-person game has two keyframes in its animation. At the start it faces yaw 170°. A moment later it faces yaw −170°. Those two directions are 20° apart. Played back, the turret swings 340° through the wrong side, sweeping its barrel across the room.

This is not a hypothetical. Godot ships two quaternion interpolation functions, `slerp` and `slerpni`, and the only difference its documentation lists is that `slerpni` does not check whether the rotation path is smaller than 90 degrees. The glTF 2.0 specification, which every engine's animation importer follows, writes the fix into the standard, and explains that it keeps interpolation on the short path. Someone shipped the long way often enough that the standard has to rule it out.

### The model

**Slerp** (spherical linear interpolation) blends two unit quaternions `a` and `b` so the orientation turns at a constant angular speed along the shortest arc between them. Let `Ω` be the angle between them in 4D, with `cos Ω = a · b`. Then

```
slerp(a, b, t) = [ sin((1 − t)·Ω) · a  +  sin(t·Ω) · b ] / sin Ω
```

for `t` from 0 to 1. At `t = 0` it returns `a`, at `t = 1` it returns `b`, and the resulting rotation angle grows linearly with `t`. That is the whole formula, and it is the same as the lerp of MA101 week 8 with the weights bent onto a circle.

The trap is Fact 2. Orientation `b` has two quaternions, `b` and `−b`. Slerp travels the 4D arc to whichever one you hand it. The arc to one of them is `Ω`, the arc to the other is `180° − Ω`, and in 3D these become turns of `2Ω` and `360° − 2Ω`. One is the short way round and one is the long way.

The rule is one line: **if `a · b < 0`, replace `b` with `−b` before interpolating.** A negative dot product means `Ω > 90°` in 4D, which means a turn of more than 180° in 3D. Flipping the sign picks the other arc, which is always 180° or less. Godot's `slerpni` warning about "90 degrees" is this 4D angle.

### Numbers you can check

Yaw 170° about the up axis `(0, 1, 0)`:

```
a = (cos 85°, 0, sin 85°, 0)    = (0.08716, 0, 0.99619, 0)
```

Yaw −170°:

```
b = (cos(−85°), 0, sin(−85°), 0) = (0.08716, 0, −0.99619, 0)
```

The dot product is `0.08716² − 0.99619² = 0.00760 − 0.99240 = −0.9848`. It is negative, so this pair would take the long way. Check with Fact 3: `|a · b| = 0.9848 = cos 10°`, so the true turn between them is `φ = 20°`. Without the flip, slerp travels `Ω = acos(−0.9848) = 170°` in 4D, a 340° turn in 3D.

The turret's yaw at five points of the animation:

| t | Naive slerp (no sign check) | Slerp with sign check |
|---|---|---|
| 0.00 | 170° | 170° |
| 0.25 | 85° | 175° |
| 0.50 | 0° | 180° |
| 0.75 | −85° | −175° |
| 1.00 | −170° | −170° |

The naive column sweeps through 85°, 0° and −85°, the full back of the room. The corrected column moves 5° per quarter, steady and short. Check the corrected midpoint by hand: with `−b = (−0.08716, 0, 0.99619, 0)`, the halfway quaternion is proportional to `a + (−b) = (0, 0, 1.99238, 0)`, which normalizes to `(0, 0, 1, 0)`, a 180° yaw. Exactly halfway between 170° and 190°.

### The visual

Open [`examples/w05-slerp-long-way.html`](../examples/w05-slerp-long-way.html). The left panel is a top-down turret with two ghost barrels at the start and end yaws and a live barrel animating between them. The right panel is the **quaternion circle**. For turns about a single axis, `q = (cos(θ/2), sin(θ/2))` is a point on a unit circle, so you can draw quaternions directly. It shows `a`, `b` and `−b` as dots, and the arc slerp travels.

Drag the end yaw from −170° toward 170°. In the left panel, the two barrels are always close together. In the right panel, `b` slides around the circle and crosses to the far side of `a` once the turn passes 180°. When the sign check is off, the arc on the right follows `b` the long way and the barrel on the left sweeps the room. Turn the check on and the arc jumps to `−b`, which is always within a quarter circle of `a`. On the turret, 170° and −170° look like neighbours. On the circle, one of the two quaternions for −170° is nearly opposite `a`. Both pictures are right, and the right-hand one is the one slerp sees.

### Cross-game recognition

**Godot 4 (class reference and `core/math/quaternion.cpp`).** `Quaternion.slerp` computes the dot product first and negates the target when it is negative, exactly the rule above. `slerpni` skips that check, for the rare case where you want the literal arc between two stored values.

**glTF 2.0 (Khronos specification, 2.0.1).** For `LINEAR` rotation animation, the spec defines `a = arccos(|v_k · v_{k+1}|)` and multiplies the second keyframe by the sign of the dot product. Its implementation note says this keeps interpolation on the short path along the great circle. Every compliant importer, in every engine, applies the rule. So an exporter that writes `q` for one key and `−q` for the next is safe in glTF, while the same keys played by a naive interpolator spin.

**MA101 week 11, Dota 2's turn rate.** The shortest signed angle difference wraps a 2D angle difference into `[−180°, 180°]` so a hero turns the short way. That is the same decision in one dimension. In 2D you wrap the angle. In 3D you flip the quaternion's sign. Both answer "which of the two ways round is shorter?".

**Networked snapshots, CS202 week 10.** The [entity interpolation lecture](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w10-entity-interpolation.md) cites Fiedler's recommendation to use slerp for orientation between snapshots. A server that sends orientations as quaternions will send `q` and `−q` for nearly identical rotations depending on rounding, so the client must apply the sign check or remote players will spin between packets.

### Eyes-open design judgment

- **Always use the checked slerp for gameplay and animation, unless you mean to spin.** A 360° spinning attack cannot be keyed with two keyframes of the same orientation, because the short path between identical orientations is no turn at all. Key it with three or four intermediate orientations, or animate an angle directly.
- **Nlerp is often good enough.** Normalized lerp, `normalize((1 − t)·a + t·b)` with the same sign check, follows the same path but with uneven speed. For a 120° turn it reaches 27.8° at `t = 0.25` where slerp reaches 30°. For turns under about 30° per frame or keyframe the difference is invisible, and nlerp is cheaper. Blend trees that mix many poses per frame often use it.
- **Keep Euler angles where they are the better model.** A first-person camera needs yaw and pitch, never roll, and pitch clamped to about ±89°. Two floats describe it exactly, stay far from gimbal lock, and let you apply a turn-rate cap per axis. Build the quaternion from them each frame. Quaternions win when orientation is free, as in flight, space, physics bodies and animation.
- **Normalize after you accumulate.** Multiplying a quaternion by small rotations every frame lets rounding push its length off 1, and a non-unit quaternion scales the object as it rotates. Renormalize every frame or every few hundred multiplications. It costs one square root.

## 5. Quaternions in the rest of the pipeline

**To a matrix.** Rendering needs the 4×4 matrix of week 4. A unit quaternion converts to its 3×3 rotation block with a fixed formula of products (Dunn and Parberry give it in chapter 8, in the section on converting between representations). Engines compose parent and child rotations as quaternions and convert once per object for the GPU.

**Look rotations.** "Turn to face the target" is usually written as a quaternion built from a forward direction and an up direction (Unity calls it `Quaternion.LookRotation`). It is the 3D version of MA101 week 11's `atan2`, and it has the same weak spot as gimbal lock: when forward is parallel to up, the up direction no longer fixes the roll, and the result can flip. A turret looking straight up needs a fallback up vector.

**Turn-rate caps.** To turn at most `ω` degrees per second toward a target orientation `b`, compute the remaining angle `φ = 2·acos(|a · b|)`, and slerp with `t = min(1, ω·Δt / φ)`. This is MA101 week 11's capped turning, with the dot product giving the angle for free.

## In-class activity (25 minutes)

Pairs, one laptop, the interactive and a calculator.

1. For each pair of yaws, compute both quaternions, their dot product, the true turn `φ`, and whether naive slerp would take the long way: (10°, 80°), (−100°, 100°), (0°, 190°), (45°, 45° + 360°).
2. Explain the last case to your partner: why is the dot product −1, and what does a naive slerp do?
3. Now a 3D case. Orientation `a` is yaw 30° then pitch 40°, `b` is yaw 30° then pitch −40°, in YXZ order. Compute `a` and `b` with the composition rule and find `φ`. Predict the turn before you compute it, and explain any difference.
4. Write a three-line code review comment for a teammate whose camera interpolates Euler angles component by component with `lerp`. Name one orientation pair where it fails and say what the player sees.

Expected output: a table for step 1, one sentence for step 2, the number for step 3, and the review comment.

## Common misconceptions

- **"The quaternion's w is the angle."** It is `cos(θ/2)`. A w of 0.7071 is a 90° turn, and a w of 0 is a 180° turn.
- **"Quaternions fix gimbal lock, so I never have to think about order."** They fix it for storage and interpolation. The moment you convert to or from Euler angles, you must know the engine's order, and near pitch 90° the angles you get back are not unique.
- **"If two quaternions are different, the orientations are different."** `q` and `−q` are the same orientation. Compare orientations with `|a · b|` close to 1, not by comparing components.
- **"Slerp always takes the shortest path."** Only the checked version does. Raw slerp on `a` and `b` with a negative dot product takes the long way.

## Check yourself

1. Write the quaternion for a 60° turn about the x axis. What is the quaternion for a −300° turn about the same axis?
2. An engine prints the rotation `(0.9239, 0, 0, 0.3827)` as `(w, x, y, z)`. What turn is it, about which axis?
3. Two orientations have quaternions with dot product −0.8660. What is the turn between them, and which way does naive slerp go?
4. In YXZ order, a character has yaw 0°, pitch 90°, roll 50°. Give a different yaw and roll, with pitch still 90°, that produce the same orientation.
5. A turret turns at 120° per second. It is at yaw 170° and must face yaw −170°. How long does the turn take with the checked slerp, and how long would it take the long way?

<details>
<summary>Answers</summary>

1. `(cos 30°, sin 30°, 0, 0) = (0.8660, 0.5, 0, 0)`. For −300°: `(cos(−150°), sin(−150°), 0, 0) = (−0.8660, −0.5, 0, 0)`, which is the negative of the first, so the same orientation.
2. `θ = 2·acos(0.9239) = 45°`. Axis `(0, 0, 0.3827) / sin(22.5°) = (0, 0, 1)`. A 45° turn about z (roll).
3. `|a · b| = 0.8660 = cos 30°`, so `φ = 60°`. The dot is negative, so naive slerp takes the long way, a 300° turn.
4. With pitch 90°, yaw and roll turn about the same line, so `(yaw, roll) = (Y, R)` gives the same orientation as `(Y + k, R + k)` for any `k`. With `k = −50`, yaw −50° and roll 0° is one answer. Section 1's table is the same rule with `k = −30`. Check it with the code by building both quaternions: both come out as `(0.6409, 0.6409, −0.2988, 0.2988)`.
5. The short turn is 20°, so `20 / 120 = 0.167` s. The long way is 340°, which takes 2.83 s.

</details>

## Lab / assignment hook

[Lab 05, a quaternion toolkit](../labs/lab05.md). You implement axis-angle construction, the product, vector rotation, Euler conversion in YXZ order, checked and unchecked slerp and nlerp, then replay a recorded turret animation and count the frames that take the long way. Deliverable: your `quat.py` passing the tests and a one-page bug report for the animation team.

## Sources

- Unity Technologies, Scripting API, `Quaternion` and `Transform.eulerAngles` (Unity 6 documentation, accessed September 2026). Quaternions stored as `{x, y, z, w}` and used internally for all rotations; Euler rotations applied about Z, then X, then Y.
- Godot Engine class reference, `Quaternion`, `Node3D` and `@GlobalScope` (master branch, 4.8-dev, September 2026; unchanged in the 4.x series). `slerp` requires normalized inputs; `slerpni` does not check whether the path is under 90 degrees; `rotation_order` default `EULER_ORDER_YXZ`, applied as intrinsic rotations.
- Godot Engine source, `core/math/quaternion.cpp`, `Quaternion::slerp` (master branch, September 2026). Negates the target when the dot product is negative, then falls back to linear interpolation when the quaternions are very close.
- Khronos Group, glTF 2.0 Specification (2.0.1, 2021). Node rotation as a unit quaternion in XYZW order; spherical linear interpolation for rotation channels using the absolute value and sign of the keyframe dot product, with the note that this follows the short path; interpolated result normalized.
- Dunn, F. & Parberry, I. (2011). *3D Math Primer for Graphics and Game Development*, 2nd ed. CRC Press. Chapter 8.

## Interactive spec: examples/w05-slerp-long-way.html

**Purpose.** Show that two yaws that look close on a turret can have quaternions that are far apart, and that the sign check picks the short arc. Two linked views: the turret (what the player sees) and the quaternion circle (what slerp sees).

**Layout.** Two panels side by side at 1280 px, stacked at 390 px.

- **Left, turret view.** Top-down circle for the room, a turret at the center. Draw a faint ghost barrel at the start yaw `A` and at the end yaw `B`, and a solid barrel at the current interpolated yaw. Leave a fading trail of the barrel tip for the last full animation so the swept path is visible as an arc. Yaw 0 points up the page, positive yaw turns counter-clockwise (right-handed about +y seen from above).
- **Right, quaternion circle.** A unit circle with horizontal axis `w` and vertical axis `y` (the quaternion components for a turn about the up axis). Plot `a = (cos(A/2), sin(A/2))`, `b = (cos(B/2), sin(B/2))` and `−b` as labelled dots. Draw the arc slerp travels from `a` to the chosen target (`b` or `−b`) as a thick stroke, and a moving dot for the current quaternion.

**Controls (keyboard accessible).**
1. Start yaw `A` slider, −180° to 180°, step 1, default 170.
2. End yaw `B` slider, −540° to 540°, step 1, default −170. Allowing values beyond ±180 lets students see `B` and `B + 360°` give opposite quaternions.
3. Toggle "Sign check (flip b when a · b < 0)", default off on first load so the long way is visible immediately.
4. Method select: slerp, nlerp.
5. Play/pause button and a `t` scrubber 0 to 1, step 0.01. The animation loops over 2 seconds when playing. With `prefers-reduced-motion`, start paused at `t = 0.5`.

**Formulas.** `a = (cos(A/2), 0, sin(A/2), 0)`, `b = (cos(B/2), 0, sin(B/2), 0)` in (w, x, y, z). `d = a · b`. If the check is on and `d < 0`, set `b ← −b`, `d ← −d`. `Ω = acos(clamp(d, −1, 1))`. Slerp: `q(t) = (sin((1−t)Ω)·a + sin(tΩ)·b) / sin Ω`, with plain lerp plus normalize when `sin Ω < 1e-6`. Nlerp: `normalize((1−t)·a + t·b)`. Displayed yaw `= 2·atan2(q_y, q_w)` wrapped to (−180°, 180°].

**Readouts (monospaced).** `a`, `b` (after any flip) to 4 decimals, `a · b`, 4D angle `Ω`, 3D turn traveled `2Ω`, the true shortest turn `φ = 2·acos(|a·b|)`, and the current yaw. Show "LONG WAY" in a warning style when the traveled turn exceeds 180°.

**The one insight.** On load (170°, −170°, check off), the barrel sweeps 340° through the back of the room while the readout shows the true turn is 20°, and on the circle `b` sits almost opposite `a`. Turning the check on moves the arc to `−b` next to `a` and the barrel moves 20°.

**Test values.**
- A = 170, B = −170: `a = (0.0872, 0, 0.9962, 0)`, `b = (0.0872, 0, −0.9962, 0)`, `a · b = −0.9848`, `φ = 20.00°`. Check off: yaw at t = 0.25, 0.5, 0.75 is 85.0°, 0.0°, −85.0°. Check on: 175.0°, 180.0°, −175.0°.
- A = 0, B = 120, nlerp at t = 0.25: yaw 27.80°. Slerp at t = 0.25: 30.00°.
- A = 45, B = 405: `a · b = −1.0000`, `φ = 0.00°`. Check on: the barrel does not move.

**Style.** Shared palette from `templates/interactive-tokens.css`, inline. The long-way arc and the short-way arc differ in dash pattern as well as color. No game art.

# MA101 · Week 13 — Dot product: facing, field of view cones

**Why this matters:** Every guard that fails to notice you behind its back, every "Target needs to be in front of you" message and every backstab bonus is one multiplication-and-add followed by one comparison. Once you can read the dot product, you can build, debug and tune all of them, and you stop calling `acos` sixty times a second for no reason.

**You will be able to:**
- Compute the dot product of two 2D vectors by components and interpret its sign and size.
- Derive the vision-cone test `f̂ · d̂ ≥ cos(h)` and convert any "the guard sees N degrees" spec into a threshold number.
- Diagnose the two most common cone bugs (unnormalized direction, half-angle versus full-angle confusion) from their symptoms.
- Design a graded detection rule that uses the dot product as an input to a remap.

**Before class:** Dunn & Parberry, *3D Math Primer for Graphics and Game Development* (2nd ed.), chapter 2, the sections on the dot product and its geometric interpretation. Freya Holmér, *Math for Game Devs* (2022), part 1, the segments on direction to a point and the dot product (roughly the last third of the video).

**Prerequisites from earlier courses:** [MA101 week 10](w10-angles-radians-sin-cos.md) (sine, cosine and radians), [week 11](w11-atan2-turning-toward-a-target.md) (atan2 and turning toward a target) and [week 12](w12-2d-vectors.md) (vector addition, magnitude and normalization, including the diagonal-movement bug). Week 8's inverse lerp comes back in section 4.

**Interactive:** [examples/w13-vision-cone.html](../examples/w13-vision-cone.html). Keep it open during section 2.

---

## 1. Two numbers in, one number out

Last week you learned to treat a position or a movement as a vector, a pair of numbers `(x, y)` with a length and a direction. You can add vectors, scale them, measure their length with `|v| = sqrt(x² + y²)` and normalize them into unit vectors of length 1. A unit vector is written with a hat, `v̂`, and it carries direction only.

This week adds one operation. The **dot product** takes two vectors and returns a single number:

```
a · b = a.x × b.x + a.y × b.y
```

Multiply matching components, add the results. That is the whole computation. In 3D you add a third term, `a.z × b.z`, and nothing else changes.

Try a few by hand:

| a | b | a · b |
|---|---|---|
| (1, 0) | (1, 0) | 1 |
| (1, 0) | (0, 1) | 0 |
| (1, 0) | (−1, 0) | −1 |
| (3, 4) | (4, −3) | 12 − 12 = 0 |
| (2, 1) | (3, 5) | 6 + 5 = 11 |

The first three rows are unit vectors, and the pattern is already visible. Same direction gives 1. At right angles gives 0. Opposite gives −1. The fourth row shows that "right angles gives 0" holds for vectors of any length. The fifth row shows that the result can be bigger than 1 when the vectors are long.

### What the number means

The component formula is easy to compute and hard to interpret. The second form of the dot product is the opposite:

```
a · b = |a| × |b| × cos(θ)
```

Here `θ` (theta) is the angle between the two vectors, measured the short way round, so it runs from 0° to 180°. You met cosine in week 10. It is 1 at 0°, 0 at 90° and −1 at 180°, and it is symmetric, so `cos(30°) = cos(−30°)`. That symmetry is why the dot product cannot tell left from right. Keep that in mind for section 3.

If both vectors are unit vectors, their lengths are 1 and the formula collapses:

```
â · b̂ = cos(θ)
```

That line is the reason the dot product is everywhere in games. You have two directions. You want to know how closely they agree. You multiply and add, and you get the cosine of the angle between them without ever computing the angle.

### Why the two forms agree

You do not need to memorize this derivation, but you should see it once so the formula is not magic. Draw `a` and `b` from the same point. The third side of that triangle is `a − b`. The law of cosines (the general form of Pythagoras) says:

```
|a − b|² = |a|² + |b|² − 2|a||b|cos(θ)
```

Now expand the left side by components. `(a.x − b.x)² + (a.y − b.y)²` becomes `a.x² + a.y² + b.x² + b.y² − 2(a.x b.x + a.y b.y)`. The first four terms are `|a|² + |b|²`. Match the two expansions and the leftover pieces must be equal:

```
a.x b.x + a.y b.y = |a||b|cos(θ)
```

The component form and the angle form are the same number.

### Reading the sign

Before you compute anything precise, the sign alone answers a useful question.

| Sign of a · b | Angle between them | Plain reading |
|---|---|---|
| positive | less than 90° | roughly the same way |
| zero | exactly 90° | perpendicular |
| negative | more than 90° | roughly opposite ways |

A guard's forward direction dotted with the direction to the player tells you whether the player is in front of or behind the guard. That is one multiply-add per axis and a sign check.

## 2. Worked example: the stealth guard who sees 60° ahead

### The hook

Anyone who has played a stealth game knows the rule without being told. You can creep to within arm's reach of a guard's back and stay hidden. Step into view ten meters in front of the same guard and you are caught at once. Guards have a cone of vision, and the game is about staying out of it.

Here is the puzzle a new programmer runs into. The design document says "the guard sees 60° ahead, up to 20 meters." The obvious code computes the angle to the player with `atan2`, subtracts the guard's facing angle, wraps the result into −180° to 180°, and compares. That works, but the wrapping step is easy to get wrong (week 11 showed how a turn toward a target at 350° can spin the long way round). There is a shorter test that never computes an angle at all, has no wraparound, and runs in a handful of multiplications. It also exposes a question the design document forgot to answer.

### The model

Name every quantity:

- `g` is the guard's position.
- `p` is the player's position.
- `f̂` is the guard's forward direction, a unit vector.
- `d = p − g` is the vector from the guard to the player.
- `d̂ = d / |d|` is that direction as a unit vector.
- `h` is the cone's **half-angle**, the angle from the forward direction to the edge of the cone.
- `R` is the sight range.

The player is seen when both of these hold:

```
|d| ≤ R                   (close enough)
f̂ · d̂ ≥ cos(h)            (inside the cone)
```

Why does the second line work? Because `f̂ · d̂ = cos(θ)`, where θ is the angle between where the guard looks and where the player stands. The player is inside the cone when `θ ≤ h`. Cosine gets smaller as the angle grows from 0° to 180°, so `θ ≤ h` is the same statement as `cos(θ) ≥ cos(h)`. The inequality flips direction because cosine runs downhill.

Call `c = cos(h)` the **threshold**. You compute it once, when the guard is created or when the designer changes the spec. At runtime the test is one dot product and one comparison.

Now the question the design document forgot. Does "sees 60° ahead" mean a 60° cone in total, or 60° to each side of forward? Those are different guards:

| Reading of "60° ahead" | Half-angle h | Full cone | Threshold c = cos(h) |
|---|---|---|---|
| 60° in total | 30° | 60° | 0.866 |
| 60° to each side | 60° | 120° | 0.500 |

The second guard covers twice the angle of the first. This lecture uses the first reading, a 60° total cone with `h = 30°` and `c ≈ 0.866`, because it produces a guard you can sneak past. Your job as a designer is to write "half-angle 30°" in the spec so no one has to guess.

### Numbers you can check

Put the guard at the origin, `g = (0, 0)`, facing along the positive x-axis, so `f̂ = (1, 0)`. Set `R = 20` meters and `c = 0.866`. Because `f̂ = (1, 0)`, the dot product `f̂ · d̂` is simply the x-component of `d̂`. That makes every row easy to verify by hand.

| Player p | d | \|d\| | d̂ | f̂ · d̂ | Angle θ (display only) | In range? | Seen? |
|---|---|---|---|---|---|---|---|
| (10, 0) | (10, 0) | 10.00 | (1.000, 0.000) | 1.000 | 0° | yes | yes |
| (3, 1) | (3, 1) | 3.16 | (0.949, 0.316) | 0.949 | 18.4° | yes | yes |
| (10, 5) | (10, 5) | 11.18 | (0.894, 0.447) | 0.894 | 26.6° | yes | yes |
| (10, 6) | (10, 6) | 11.66 | (0.857, 0.514) | 0.857 | 31.0° | yes | no |
| (5, 5) | (5, 5) | 7.07 | (0.707, 0.707) | 0.707 | 45.0° | yes | no |
| (0, 8) | (0, 8) | 8.00 | (0.000, 1.000) | 0.000 | 90.0° | yes | no |
| (−6, 0) | (−6, 0) | 6.00 | (−1.000, 0.000) | −1.000 | 180.0° | yes | no |
| (18, 9) | (18, 9) | 20.12 | (0.894, 0.447) | 0.894 | 26.6° | no | no |
| (25, 0) | (25, 0) | 25.00 | (1.000, 0.000) | 1.000 | 0° | no | no |

Three rows deserve a second look.

Rows (10, 5) and (10, 6) sit one meter apart and land on opposite sides of the cone's edge. The dot product drops from 0.894 to 0.857, crossing 0.866. The angle column confirms it (26.6° is inside 30°, 31.0° is outside), but the code never needed that column. It exists only so you can check the table.

Row (−6, 0) is the player standing six meters directly behind the guard. The dot product is −1, as far from the threshold as it can get. That is the "arm's reach of the guard's back" from the hook.

Rows (10, 5) and (18, 9) point in exactly the same direction and have identical dot products. Only the range test separates them. The cone test and the range test answer different questions, and you need both.

Now turn the guard. Set its facing to 45°, so `f̂ = (cos 45°, sin 45°) = (0.707, 0.707)`. The player at (5, 5) now has `d̂ = (0.707, 0.707)` and `f̂ · d̂ = 0.707 × 0.707 + 0.707 × 0.707 = 1.000`. Seen, dead center. The player at (10, 0) has `f̂ · d̂ = 0.707`, so is now outside the cone. Nothing about the test changed. You only changed `f̂`.

### The visual

Open [`examples/w13-vision-cone.html`](../examples/w13-vision-cone.html). The left view is a top-down map with the guard, its cone and a player you can drag. The right view plots `f̂ · d̂` against the angle θ from −180° to 180°. It is a cosine hump, with a flat horizontal line at the threshold `c`.

Drag the player around the guard and watch the marker ride along the hump. The player is seen exactly when the marker is above the flat line and within range. Now move the half-angle slider. On the map the cone widens. On the plot the flat line drops. That is the picture to keep: **a vision cone is a horizontal line cut across a cosine curve.** Widening the cone means lowering one number.

Then switch on the "forget to normalize" toggle. The test becomes `f̂ · d ≥ c` with the raw, unnormalized `d`. On the map the cone vanishes and is replaced by a half-plane. For the guard facing +x, `f̂ · d` is just `d.x`, so the test becomes `d.x ≥ 0.866`. Every point more than 0.866 meters in front of the guard passes, at any angle up to 90°. The player at (5, 5), 45° off to the side, is now "seen." The player at (1, 15), 86° off, is seen too. This is the classic bug. Guards seem to see out of the sides of their heads, but only once you are far enough away, which makes it maddening to reproduce. The fix is either to normalize `d`, or to use the equivalent no-division form covered in section 5.

### Cross-game recognition

The same one-line test hides behind many rules that are not described as dot products. The skill is to rewrite each rule as `f̂ · d̂ ≥ c` and read off `c`.

**World of Warcraft, facing.** Most attacks and offensive spells in World of Warcraft require the target to be in front of the attacker, and the game shows "Target needs to be in front of you" when it is not. Warcraft Wiki describes "in front" as 90° to either side of the character's exact front. That is a half-angle of 90°, so `c = cos(90°) = 0`. The rule is `f̂ · d̂ ≥ 0`, which is the sign test from section 1. Note what the source tells you. The wiki describes the observable behavior. It does not show Blizzard's code, which may compute an angle rather than a dot product. The two are mathematically equivalent, and the dot form is how you would write it.

**World of Warcraft, Backstab.** In classic-era World of Warcraft (1.x, and the Classic re-release), the rogue ability Backstab has the tooltip requirement "Must be behind the target." This flips the question around. Now you use the *target's* forward vector, and the direction from the target to the attacker. With `t̂` as the target's forward and `â` as the unit direction from the target to the attacker, "behind" means `t̂ · â < 0`, a threshold of `c = 0` with the inequality reversed. In the current retail game the ability no longer requires being behind. Warcraft Wiki's current tooltip instead gives 20% more damage from behind. That is the same test driving a multiplier instead of a gate: `damage × (1.2 if t̂ · â < 0 else 1.0)`.

**Unreal Engine, AI Perception.** Unreal's sight sense for AI characters (`UAISenseConfig_Sight`, Unreal Engine 5.3 documentation) has a property named `PeripheralVisionAngleDegrees`. Its documentation says the value is measured from the forward vector and is not the whole range. In other words, it is our `h`. Set it to 30 and you get this lecture's guard, with `c = cos(30°) = 0.866`. Set it to 60, believing you asked for a 60° cone, and you get the 120° guard from the ambiguity table. The documentation spells this out, so read it before you tune.

**Unity, `Vector3.Dot`.** Unity's scripting reference for `Vector3.Dot` says that for normalized vectors the result is 1 for the same direction, −1 for opposite directions and 0 for perpendicular. That is the sign table from section 1, stated by an engine vendor. Notice the qualifier "for normalized vectors." The documentation is warning you about the bug you just saw in the interactive.

Four sources, four vocabularies (facing arc, "must be behind," peripheral angle, normalized dot). All four are `f̂ · d̂` compared against `cos(h)`.

### Eyes-open design judgment

The dot-product cone is the right default for "can this character see, target or hit that one?" It is cheap, has no angle wraparound, and every engine has the function built in. That does not settle the design questions. Decide these on purpose:

- **Write the half-angle, not "the cone."** The ambiguity in "60° ahead" costs teams real time. Specify `h` in degrees and store `c = cos(h)` in data. If a designer tunes the cone in a spreadsheet, have the spreadsheet show both.
- **The cone only answers direction.** It says nothing about walls. A real guard also needs a line-of-sight check, usually a raycast (MA201 covers raycasting). Raycasts are expensive compared with a dot product. So run the cheapest test first. Check range, then the cone, and raycast only for the few players who pass both. Order matters for performance, not for correctness.
- **A hard edge feels unfair at the boundary.** The table showed a one-meter step flipping the result. Many stealth designs soften this with a detection meter that fills faster near the center of the cone and slower at the edge. Section 4 shows how to build that from the same dot product.
- **Readability beats realism.** Players cannot see an invisible cone. If your game punishes being seen, show the player where the cone is, or make guards' heads and lights point clearly along `f̂`. A 60° cone that players can read is fairer than a realistic 180° cone they cannot.
- **One cone may not be enough.** A narrow, long "focus" cone plus a wide, short "peripheral" cone is a common pattern. Each is the same test with a different `c` and `R`.

### Check yourself on the guard

1. The guard faces `f̂ = (0, 1)`. The player is at `p = (4, 7)` with the guard at the origin. Is the player seen with `h = 30°` and `R = 20`?
2. A designer wants a cone where the threshold is exactly 0.5. What is the full cone angle?
3. A bug report says "guards spot me at the edge of the screen but not when I'm close and slightly off-center." Which bug from this section fits, and why?

<details>
<summary>Answers</summary>

1. `|d| = sqrt(16 + 49) = 8.06`, so in range. `d̂ = (0.496, 0.868)`. `f̂ · d̂ = 0.868`, which is just above 0.866. Seen, barely. The angle is about 29.7°.
2. `cos(h) = 0.5` gives `h = 60°`, so the full cone is 120°.
3. The unnormalized `d`. The test becomes "the forward distance `f̂ · d` is at least 0.866 m." A far player at the edge of the screen, even 80° off-center, has a large forward distance and passes. A close player at (0.5, 0.2), only 22° off-center, has a forward distance of 0.5 m and fails. Normalize `d` or use the squared form in section 5.

</details>

## 3. Left or right? The perpendicular dot product

The dot product cannot tell left from right, because `cos(30°) = cos(−30°)`. A turret that knows the target is 30° off-axis still needs to know which way to turn. Week 11 solved this with `atan2`. Here is the dot-product way.

Rotate the forward vector 90° counterclockwise. In 2D, the rotation of `(x, y)` by 90° counterclockwise is `(−y, x)`. Call that the guard's **left vector**, `l̂ = (−f.y, f.x)`. Then:

```
l̂ · d > 0   →  target is to the left
l̂ · d < 0   →  target is to the right
l̂ · d = 0   →  target is dead ahead or dead behind
```

For the guard facing `(1, 0)`, the left vector is `(0, 1)`. The player at (10, 5) gives `l̂ · d = 5`, so left. The player at (10, −5) gives −5, so right. Expanded, `l̂ · d = f.x × d.y − f.y × d.x`. Many engines call this quantity the 2D cross product or "perp dot." MA201 generalizes it to the 3D cross product.

A turning rule now needs no angles at all:

```
if f̂ · d̂ ≥ c_aim:       fire
else if l̂ · d > 0:      turn left
else:                    turn right
```

Notice that the aiming threshold `c_aim` can be much tighter than a vision threshold. A turret that fires when `f̂ · d̂ ≥ 0.999` fires within about 2.6° of perfect aim, since `acos(0.999) ≈ 2.56°`.

## 4. From yes-or-no to how-much

A hard cone says "seen" or "not seen." Most stealth designs want something in between. The dot product is already a number that grows smoothly from the cone's edge to its center, so you can feed it into the inverse lerp from week 8.

Inverse lerp maps a value in the range `[a, b]` to `[0, 1]`:

```
invlerp(a, b, v) = (v − a) / (b − a)
```

Use `a = c` (the edge of the cone) and `b = 1` (dead center), then clamp:

```
focus = clamp(invlerp(c, 1, f̂ · d̂), 0, 1)
```

For our 30° guard, `c = 0.866`:

| Player at angle θ | f̂ · d̂ | focus |
|---|---|---|
| 0° | 1.000 | 1.00 |
| 10° | 0.985 | 0.89 |
| 20° | 0.940 | 0.55 |
| 26.6° | 0.894 | 0.21 |
| 30° | 0.866 | 0.00 |
| 45° | 0.707 | 0.00 (clamped) |

A detection meter that fills at `focus × base_rate` per second gives the player a warning band near the edge. Look at the shape of the column, though. Focus drops slowly near the center and quickly near the edge, because cosine is flat near 0°. If you want detection to fall off evenly with angle, you would need the angle itself, `acos(f̂ · d̂)`, and that costs more. Often the cosine shape is what you want anyway. Players standing near the center get caught fast, and the edge is a narrow danger zone. Decide which shape you want. Do not inherit one by accident.

Distance can be folded in the same way. `range_factor = clamp(invlerp(R, R_near, |d|), 0, 1)` is 1 when the player is closer than `R_near` and falls to 0 at `R`. Multiply the two factors and you have a two-input detection rate. This is the start of the perception systems CS203 builds on (see the [CS203 syllabus](../../CS203-artificial-intelligence-for-games/syllabus.md), week 10, perception systems).

## 5. Making it cheap: skip the normalize

Normalizing `d` costs a square root and a division. A guard that checks thirty players every frame does thirty of each. You can remove both.

Start from the test and multiply both sides by `|d|`, which is positive:

```
f̂ · (d / |d|) ≥ c
f̂ · d ≥ c × |d|
```

If `c ≥ 0` (any cone of 180° or narrower), the left side must be non-negative for the test to pass, so you can square both sides without changing the answer:

```
f̂ · d ≥ 0   and   (f̂ · d)² ≥ c² × (d · d)
```

`d · d` is `d.x² + d.y²`, the squared length. There is no square root left and no division. `c²` is a constant you store alongside `c`. For `h = 30°`, `c² = 0.75`.

Check it on the player at (10, 6). `f̂ · d = 10`. `(f̂ · d)² = 100`. `d · d = 136`. `0.75 × 136 = 102`. Since 100 < 102, not seen, which matches the table.

The first condition (`f̂ · d ≥ 0`) is easy to forget, and forgetting it makes the guard see a mirror-image cone behind its head, because squaring erases the sign. Next week develops the same squared-length idea for range checks, where it is even more common.

A word of caution. This trick saves a square root per check. On modern hardware that is a small saving, and clarity may matter more. Profile first. Use the squared form in hot loops over many entities, and the readable form elsewhere.

## 6. Other places the dot product appears

You will meet the same operation in many systems that look unrelated. Recognizing it saves you from re-deriving it each time.

- **Projection: how much of a vector points along a direction.** `v · û` is the length of `v`'s shadow on the direction `û`. A character's forward speed is `velocity · f̂`. A car game's "sideways slip" is `velocity · l̂`. When MA201 handles collision response, the part of a velocity going into a wall is `velocity · n̂`, with `n̂` the wall's normal.
- **Lighting.** The simplest diffuse lighting model makes a surface brighter the more directly it faces the light. Brightness is proportional to `max(0, n̂ · l̂)`, the dot product of the surface normal with the direction to the light. That is Lambert's cosine law, the same cosine you used for the guard.
- **Similarity of directions in general.** "Is the player moving toward the objective?" is the unit velocity dotted with the unit direction to the objective, compared against a threshold such as 0.7. "Is the camera looking at the painting?" is the vision-cone test run from the camera.

## In-class activity (25 minutes)

In pairs, design the vision for two guard types in a small top-down stealth level. You need graph paper, a calculator and the interactive.

1. **Sentry.** Stands still, long focused sight. Choose `h` and `R`. Write the threshold `c` and `c²` to three decimals.
2. **Patroller.** Walks a route, wide short sight. Choose `h` and `R`. Write `c` and `c²`.
3. On graph paper, place each guard at (0, 0) facing (1, 0). Mark five player positions you think are interesting edge cases, including at least one that the sentry sees and the patroller does not, and one the reverse.
4. For each position, compute `f̂ · d̂` and the range test by hand. Then check your five points in the interactive.
5. Write one sentence for the level designer explaining how a player can tell the two guard types apart on screen.

**Expected output:** a half-page sheet with both guards' specs, a 5-row table per guard, and the one-sentence readability note. Swap sheets with another pair and check one of their rows.

## Common misconceptions

- **"The dot product gives the angle."** It gives the cosine of the angle, and only when both vectors are unit length. To get degrees you need `acos`, and you almost never need degrees at runtime. Compare cosines directly.
- **"Wider cone means bigger threshold."** Backwards. A wider cone has a larger `h`, so a smaller `cos(h)`. Widening the cone lowers the line on the cosine plot.
- **"Normalizing is optional if the numbers look fine."** The test looks fine when the player is about one unit away and fails everywhere else. Unity's own documentation qualifies its sign rules with "for normalized vectors." Either normalize or use the squared form with the sign check.
- **"The dot product tells me left or right."** It cannot, because cosine is symmetric. Use the perpendicular dot product `l̂ · d` for side.

## Check yourself

1. Compute `(3, −2) · (4, 5)`. Is the angle between the vectors more or less than 90°?
2. A guard at (2, 3) faces `f̂ = (0.6, 0.8)`. The player is at (8, 11). With `h = 30°` and `R = 15`, is the player seen? Show the dot product.
3. Unreal's `PeripheralVisionAngleDegrees` is set to 45. A designer says the guard has "a 45° cone." What is the full cone, and what is `c`?
4. Using the squared form from section 5 with `h = 30°`, test the player at (5, 5) against the guard facing (1, 0). What do the two sides of the inequality equal?
5. You want a detection meter that fills at full rate inside 10° of center and at zero rate at 40°. Write the focus formula using `f̂ · d̂`.

<details>
<summary>Answers</summary>

1. `12 − 10 = 2`. Positive, so less than 90°.
2. `d = (6, 8)`, `|d| = 10`, in range. `d̂ = (0.6, 0.8)`. `f̂ · d̂ = 0.36 + 0.64 = 1.0`. Seen, dead center.
3. The value is a half-angle, so the full cone is 90°. `c = cos(45°) ≈ 0.707`.
4. `f̂ · d = 5`, which is non-negative. `(f̂ · d)² = 25`. `d · d = 50`, and `0.75 × 50 = 37.5`. Since 25 < 37.5, not seen. That matches the 45° row of the table.
5. `focus = clamp(invlerp(cos 40°, cos 10°, f̂ · d̂), 0, 1) = clamp((f̂ · d̂ − 0.766) / (0.985 − 0.766), 0, 1)`.

</details>

## Lab hook

**Lab 13, Guard vision.** In [`labs/lab13.md`](../labs/lab13.md) you implement the cone test, the left/right test and the graded detection meter for a set of guards and a recorded player path, then find and fix a planted unnormalized-vector bug. The results feed the problem set and the curve-design project, where your detection falloff is one of the curves you may choose to design.

## Sources

- Warcraft Wiki, "Facing" (retrieved September 2026). Describes "in front" as 90° to either side of a unit's exact front, the "Target needs to be in front of you" error, and Backstab and Ambush as behind-only abilities. Describes observable behavior, not source code.
- Warcraft Wiki, "Backstab" (retrieved September 2026). Classic-era tooltip requires being behind the target; the current retail tooltip gives 20% more damage from behind instead.
- Epic Games, Unreal Engine 5.3 API documentation, `UAISenseConfig_Sight::PeripheralVisionAngleDegrees`. States that the angle is measured relative to the forward vector and is not the whole range.
- Unity Technologies, Scripting API, `Vector3.Dot` (current documentation, retrieved September 2026). States the 1, −1 and 0 results for normalized vectors.
- Dunn, F. & Parberry, I. (2011). *3D Math Primer for Graphics and Game Development*, 2nd ed. CRC Press. Chapter 2.
- Holmér, F. (2022). *Math for Game Devs [2022, part 1]: Numbers, Vectors and Dot Product*. YouTube lecture recorded for Futuregames students.

## Interactive spec: examples/w13-vision-cone.html

**The one insight the visual must make obvious:** a vision cone is a horizontal threshold line cut across a cosine curve. The code compares one number, `f̂ · d̂`, against one constant, `c = cos(h)`. Widening the cone lowers the line. Forgetting to normalize turns the cone into a half-plane.

**Layout.** Two linked views side by side on desktop (map left, plot right), stacked on mobile (map on top). Readout panel under both.

**View A, top-down map.**
- World coordinates from −25 to 25 meters on both axes, y up. Light grid every 5 m, axis labels every 10 m.
- Guard drawn as a generic circle with a short forward arrow at the origin. Do not draw any game character.
- Cone drawn as a filled wedge from the guard, half-angle `h`, radius `R`, semi-transparent accent color.
- Region shading: shade every map cell (render at 2 px per cell or use a canvas pass) where the *currently active test* passes. With normalize on this matches the wedge. With normalize off it shows the half-plane `f̂ · d ≥ c` clipped to the range circle, so students see the wedge replaced by a stripe.
- Player drawn as a generic diamond. Draggable with pointer. Keyboard: when focused, arrow keys move it 0.5 m, Shift + arrow moves it 5 m.
- Draw `d` as a thin line from guard to player. Draw `d̂` as a unit-length arrow (scaled for visibility, with a label "d̂, length 1").
- Player color: "seen" color when both tests pass, neutral otherwise. The word SEEN or HIDDEN appears next to the player so color is not the only signal.

**View B, plot.**
- x-axis: angle θ from −180° to 180°, ticks every 30°. y-axis: from −1.2 to 1.2 with normalize on.
- Plot `y = cos(θ)` as a solid curve.
- Horizontal line at `y = c`, labeled "threshold c = cos(h)". Shade the band where `cos(θ) ≥ c`.
- Vertical dashed lines at θ = ±h.
- Player marker at `(θ_player, f̂ · d̂)`, where θ_player is the signed angle from `f̂` to `d` (use atan2 for display only).
- With normalize off, replace the curve with `y = |d| × cos(θ)` for the current `|d|`, rescale the y-axis to fit, and keep the threshold line at `c`. The curve grows taller as the player moves away, so the band above `c` widens toward ±90°. Caption: "Unnormalized: the test now depends on distance."

**Controls.**
- Guard facing slider: 0° to 359°, step 1°, default 0°. `f̂ = (cos φ, sin φ)`.
- Half-angle `h` slider: 5° to 90°, step 1°, default 30°.
- Range `R` slider: 5 m to 25 m, step 0.5 m, default 20 m.
- Preset buttons: "60° total (h = 30°)" and "60° each side (h = 60°)". These set `h` and show the matching row of the ambiguity table.
- Toggle "Forget to normalize d" (default off).
- Toggle "Graded detection" (default off). When on, the map shading becomes a gradient using `focus = clamp((f̂ · d̂ − c) / (1 − c), 0, 1)` inside range, and the readout adds a focus value.
- Button "Snap to test positions" cycles the player through (10, 0), (3, 1), (10, 5), (10, 6), (5, 5), (0, 8), (−6, 0), (18, 9), (25, 0).

**Readouts (monospace, 3 decimals, updated live):** `f̂`, `d`, `|d|`, `d̂`, `f̂ · d̂` (or `f̂ · d` when unnormalized), `c`, `c²`, `l̂ · d` with the word LEFT or RIGHT, angle θ in degrees labeled "display only", range test pass/fail, cone test pass/fail, final SEEN/HIDDEN.

**Exact formulas.**
- `d = p − g`, `|d| = sqrt(d.x² + d.y²)`, `d̂ = d / |d|` (if `|d| < 1e-6`, treat as seen and show "player on guard").
- Cone test (normalized): `f̂ · d̂ ≥ cos(h)`.
- Cone test (bug mode): `f̂ · d ≥ cos(h)`.
- Range test: `|d| ≤ R`.
- Left vector `l̂ = (−f.y, f.x)`.

**Test values (guard at origin, facing 0°, h = 30°, R = 20, normalize on).** The readout must match the lecture's table to 3 decimals.

| Player | f̂ · d̂ | Seen |
|---|---|---|
| (10, 0) | 1.000 | yes |
| (3, 1) | 0.949 | yes |
| (10, 5) | 0.894 | yes |
| (10, 6) | 0.857 | no |
| (5, 5) | 0.707 | no |
| (0, 8) | 0.000 | no |
| (−6, 0) | −1.000 | no |
| (18, 9) | 0.894 | no (range) |
| (25, 0) | 1.000 | no (range) |

Extra checks. Facing 45°, player (5, 5) gives 1.000, seen. Facing 45°, player (10, 0) gives 0.707, not seen. Bug mode, facing 0°, player (5, 5) gives `f̂ · d = 5.000`, seen. Bug mode, player (1, 15) gives 1.000, seen, even though the angle is 86.2°.

**First screen.** Guard facing 0°, `h = 30°`, player at (10, 6) just outside the cone edge with the marker just under the threshold line on the plot. Caption: "One meter from being seen. Drag the player up or down."

**Accessibility and motion.** All sliders and toggles are native inputs with labels. No animation except when "Snap to test positions" moves the player; under `prefers-reduced-motion` the player jumps. Palette from `templates/interactive-tokens.css`, light and dark.

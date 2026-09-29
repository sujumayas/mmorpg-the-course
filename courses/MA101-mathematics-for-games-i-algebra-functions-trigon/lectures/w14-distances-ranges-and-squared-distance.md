# MA101 · Week 14 — Distances and ranges: circles, squared distance trick

**Why this matters:** "Is it in range?" is probably the most frequently asked question in a running game. Aggro, pickups, spell range, despawning, audio falloff and network relevance all ask it, for thousands of pairs of things, every frame. Getting the answer right is Pythagoras. Getting it cheaply, and choosing which kind of distance your game uses, are design decisions.

**You will be able to:**
- Compute Euclidean distance in 2D and 3D and test whether a point is inside a circle, a ring or a sphere.
- Apply the squared-distance trick and prove that it never changes the answer of a comparison.
- Compare Euclidean, Manhattan, Chebyshev and alternating-diagonal distance, and predict the shape each makes as a "range circle."
- Design a two-radius (hysteresis) range rule and explain what problem it prevents.

**Before class:** Dunn & Parberry, *3D Math Primer for Graphics and Game Development* (2nd ed.), chapter 2, the sections on vector magnitude and the distance formula. Freya Holmér, *Math for Game Devs* (2022), part 1, the segments on length, distance and the radial trigger.

**Prerequisites from earlier courses:** [MA101 week 12](w12-2d-vectors.md) (vectors, magnitude, normalization and the diagonal-movement bug) and week 13 ([dot product and vision cones](w13-dot-product-facing-and-vision-cones.md)), which introduced `d · d` as the squared length. Week 7's piecewise rules and week 8's inverse lerp reappear in sections 4 and 5.

**Interactive:** [examples/w14-range-rings.html](../examples/w14-range-rings.html). Keep it open during section 2.

---

## 1. Distance is Pythagoras with a subtraction in front

Two things stand at positions `a` and `b`. The vector from one to the other is `d = b − a`. The distance between them is the length of that vector:

```
dist(a, b) = |b − a| = sqrt(dx² + dy²)          (2D)
dist(a, b) = sqrt(dx² + dy² + dz²)              (3D)
```

Here `dx = b.x − a.x`, and so on. This is the right triangle from school. `dx` and `dy` are the two short sides, and the distance is the long side. Last week you saw the same sum written as `d · d`, the dot product of a vector with itself. So `|d|² = d · d`. Keep that identity in your pocket. It is the whole trick in this lecture.

The sign of `dx` does not matter, because squaring removes it. Distance from `a` to `b` equals distance from `b` to `a`.

A **circle** of radius `r` around a center `c` is every point at distance exactly `r` from `c`. The **inside** of the circle, called a disk, is every point at distance `r` or less. In 3D the same words give a sphere and a ball. When game code says a mob "has a 10-meter aggro radius," it means: the mob notices players inside a disk (or ball) of radius 10 around it.

So the basic range test is:

```
in_range = dist(a, b) ≤ r
```

A **ring** (mathematicians say annulus) is the region between two radii:

```
in_ring = r_min ≤ dist(a, b) ≤ r_max
```

You will see rings often. A ranged attack that cannot be used point-blank has a minimum range. A spawner that places monsters "near but not on top of" the player uses a ring. The worked example below has two rings stacked.

## 2. Worked example: Minecraft's despawn rings and the squared-distance trick

### The hook

In Minecraft: Java Edition, hostile mobs do not live forever. Walk away from a zombie and at some point it disappears. The Minecraft Wiki documents the rules as two distances. A mob with no player within 32 blocks for long enough starts rolling a small random chance to despawn every game tick. A mob with no player within 128 blocks despawns instantly.

Here is the surprise. The wiki gives a pair of examples. A mob stands at the origin. You walk to 65 blocks east and 65 blocks south. The mob survives. You walk to 91 east and 91 south. It vanishes, even though you are well under 128 blocks along each axis. Players who think of distance as "how many blocks along each axis" get this wrong, and so do programmers who write the check as `abs(dx) ≤ 128 and abs(dz) ≤ 128`. The wiki spells out that the check is a true Euclidean sphere, not a box and not a diamond.

The second puzzle is for the programmer. A busy Minecraft server checks many mobs against many players, over and over. Each check as written needs a square root. You can remove every one of them and get exactly the same answers.

### The model

Name the quantities. The mob is at `m`, the nearest player at `p`, and `d = p − m`. Two radii come from the rules: `r_near = 32` and `r_far = 128`, both in blocks.

```
D = |d| = sqrt(dx² + dy² + dz²)

D ≤ 32            → safe: no despawn, inactivity timer resets
32 < D ≤ 128      → random zone: may despawn by chance after a delay
D > 128           → despawns instantly
```

That is a piecewise rule (week 7) over a distance. Now the trick. For numbers that are zero or positive, squaring preserves order:

```
if D ≥ 0 and r ≥ 0:    D ≤ r   exactly when   D² ≤ r²
```

Why? The function `x ↦ x²` is increasing for `x ≥ 0`. If `D` is smaller than `r`, then `D²` is smaller than `r²`, and the other way round. Distances and radii are never negative, so the condition always holds.

`D²` needs no square root. It is `dx² + dy² + dz²`, which is `d · d`. The radii are constants, so you square them once: `32² = 1,024` and `128² = 16,384`. The despawn rule becomes:

```
S = dx² + dy² + dz²          (squared distance)

S ≤ 1,024          → safe
1,024 < S ≤ 16,384 → random zone
S > 16,384         → despawn now
```

Same decisions, no square roots. Unity's scripting reference for `sqrMagnitude` recommends exactly this. It says that skipping the square root is faster and that comparing squared magnitudes against a squared distance gives the same result.

We cannot see Mojang's source code through the wiki, so we cannot say whether Minecraft uses this form internally. It does not matter for the rule. The two forms give identical answers, and the wiki's description tells us the rule is Euclidean.

### Numbers you can check

The mob is at the origin. The player moves on the same height, so `dy = 0` and only the two horizontal axes matter. Every number here can be checked with a calculator in under a minute.

| Player (x, z) | S = x² + z² | D = sqrt(S) | Largest single axis | Zone |
|---|---|---|---|---|
| (20, 20) | 800 | 28.28 | 20 | safe |
| (30, 10) | 1,000 | 31.62 | 30 | safe |
| (30, 30) | 1,800 | 42.43 | 30 | random |
| (65, 65) | 8,450 | 91.92 | 65 | random |
| (90, 90) | 16,200 | 127.28 | 90 | random |
| (100, 80) | 16,400 | 128.06 | 100 | despawn |
| (91, 91) | 16,562 | 128.69 | 91 | despawn |
| (120, 50) | 16,900 | 130.00 | 120 | despawn |

Read the table with the squared thresholds in mind. Row (90, 90) has `S = 16,200`, which is under 16,384. Row (91, 91) has `S = 16,562`, which is over. One block along each axis moves the player across the despawn boundary. The wiki's two examples, (65, 65) and (91, 91), come out as 91.9 and 128.7, matching its figures.

Row (120, 50) is the one that surprises the "per axis" reader. Neither coordinate reaches 128, but the straight-line distance is exactly 130. It is a 5-12-13 right triangle scaled by 10.

Now look at the column you did not need. Every zone decision can be made from the `S` column and the two constants 1,024 and 16,384. The `D` column is there only for humans.

### The visual

Open [`examples/w14-range-rings.html`](../examples/w14-range-rings.html). The left view is a top-down map with the mob at the center, the 32-block ring and the 128-block ring, and a player you can drag. The right view shows two number lines, one for distance `D` and one for squared distance `S`, stacked with connecting lines between matching values. The marks 32 and 1,024 are joined. So are 128 and 16,384.

Drag the player. The player's marker moves along both number lines at once. The connecting lines never cross, which is the visual proof that squaring preserves order. The squared line stretches the far end enormously (16,384 is sixteen times 1,024, although 128 is only four times 32), but nothing ever swaps sides of a threshold. That is the insight to take away. **Squaring bends the ruler but keeps the order, so every "closer than" answer stays the same.**

Then switch on the "forgot to square the radius" toggle. The code now compares `S ≤ 128`, squared distance against an unsquared radius. The outer ring on the map shrinks to `sqrt(128) ≈ 11.3` blocks, and the inner ring shrinks to `sqrt(32) ≈ 5.7`. Mobs would vanish when you step twelve blocks away. This bug is common because the code still "looks right." Both sides of the comparison are named after distance.

Finally, try the metric menu. It swaps Euclidean distance for three alternatives covered in section 3, and the rings change shape into a diamond, a square or an octagon.

### Cross-game recognition

The same question, "is `D ≤ r`?", appears in every engine and many rulebooks. What changes is how `D` is computed and whether the square root is paid for.

**Minecraft: Bedrock Edition.** Bedrock uses different radii for the same idea. The Minecraft Wiki lists instant despawn beyond 128 blocks at simulation distances of 6 or more, 44 blocks at simulation distance 4, and 40 blocks for fish, with a 1-in-800 chance per tick beyond 32 blocks. Java Edition uses 64 blocks for fish. Same model, different constants per edition and per setting. In squared form Bedrock's small-world rule is `S > 1,936`.

**Unity.** Unity exposes both `magnitude` and `sqrMagnitude` on its vector types, and its documentation for `sqrMagnitude` recommends the squared version for comparisons. Engine teams provide the squared version as a first-class function because range checks are that common.

**Dungeons & Dragons 3.5 (tabletop).** The d20 System Reference Document measures distance on a square grid of 5-foot squares, but not with Pythagoras. The first diagonal step counts as 1 square, the second as 2, the third as 1, and so on. A spell with 30-foot range reaches targets within 6 squares under this rule. The "circle" of reachable squares is an octagon. It is the same test, `D ≤ r`, with a different `D`. Section 3 shows why the alternating rule is a clever approximation of `sqrt(2)`.

**Chess.** A king moves one square in any direction, including diagonally. The number of king moves between two squares is `max(|dx|, |dy|)`, called Chebyshev distance. The squares a king can reach in `n` moves form a square, not a circle. Any grid game that lets diagonal steps cost the same as straight ones has chess-king distance, whether its designers noticed or not.

Four settings. Each is `D ≤ r`. Minecraft and Unity use Euclidean `D` and can square both sides. D&D 3.5 and chess use grid rules that are already integer arithmetic, so there is no square root to remove.

### Eyes-open design judgment

- **Use squared distance for comparisons, real distance for amounts.** Whenever the question is yes or no ("in range?", "which enemy is closest?"), compare squared values. Whenever you need a quantity that scales with distance (damage falloff, sound volume, a number shown to the player), you need the real `D`. A falloff written as `1 − S / r²` is a different curve from `1 − D / r`. It is flatter near the center and steeper near the edge. That may be fine, but choose it on purpose.
- **Square the constants in one place.** Store `r` in data, the way designers think about it, and compute `r²` once in code. Never ask a designer to type 16,384.
- **Watch integer overflow.** In a 32-bit signed integer, the largest value is 2,147,483,647. Its square root is about 46,341. If your positions are integers in millimeters, two objects 47 meters apart overflow the squared-distance calculation and wrap to a negative number, which then passes every "in range" test. Use 64-bit integers or floating point for `S`.
- **Pick the metric for feel as well as speed.** Euclidean distance matches what players see on a continuous map. On a grid, Chebyshev distance is simpler to explain ("any direction costs 1") but lets a unit travel about 41% farther on a diagonal than on a straight line for the same cost, the same `sqrt(2)` factor as the diagonal-movement bug from week 12. Players find the diagonals and exploit them.
- **Two radii are better than one.** Minecraft's rule has a safe zone and an instant zone with a random band between them. Section 4 shows why a band between two radii is a good pattern in general.

### Check yourself on the despawn rings

1. A mob is at (10, 64, −20) and the nearest player at (70, 70, 60). Compute `S`, then decide the zone without taking a square root.
2. A programmer writes `if (dx*dx + dz*dz > 128) despawn();`. At what distance do mobs actually despawn?
3. Why is `abs(dx) ≤ 128 && abs(dz) ≤ 128` wrong for Minecraft's rule, and which direction does it get wrong?

<details>
<summary>Answers</summary>

1. `dx = 60`, `dy = 6`, `dz = 80`. `S = 3,600 + 36 + 6,400 = 10,036`. That is between 1,024 and 16,384, so the random zone. (`D ≈ 100.2`.)
2. At `sqrt(128) ≈ 11.3` blocks. The radius was not squared.
3. It tests a square of side 256, which contains the circle. The corners of that square reach out to `128 × sqrt(2) ≈ 181` blocks. Mobs at (91, 91) would survive with this check but despawn in the real game. The check keeps mobs too long, diagonally.

</details>

## 3. Four ways to measure distance

Section 2 used ordinary straight-line distance. Games, especially grid games, often use others. Each is a rule for turning `(dx, dy)` into one number. Write `ax = |dx|` and `ay = |dy|`.

| Name | Formula | "Circle" shape | Where you see it |
|---|---|---|---|
| Euclidean | `sqrt(ax² + ay²)` | circle | continuous worlds, physics |
| Manhattan (taxicab) | `ax + ay` | diamond | 4-direction grid movement |
| Chebyshev (king) | `max(ax, ay)` | square | 8-direction grids, chess king |
| Alternating diagonal (D&D 3.5) | `max + floor(min / 2)` | octagon | tabletop grids |

The alternating rule needs a line of explanation. You take `min(ax, ay)` diagonal steps and `max − min` straight steps. Every second diagonal costs one extra square, so the total is `(max − min) + min + floor(min / 2)`, which simplifies to `max + floor(min / 2)`.

Compute all four for three offsets:

| Offset (dx, dy) | Euclidean | Manhattan | Chebyshev | Alternating |
|---|---|---|---|---|
| (10, 0) | 10.00 | 10 | 10 | 10 |
| (3, 4) | 5.00 | 7 | 4 | 5 |
| (6, 6) | 8.49 | 12 | 6 | 9 |

Along an axis, all four agree. On diagonals they disagree, and the pattern is always the same. Manhattan overestimates, Chebyshev underestimates, and the alternating rule lands close to Euclidean. For a pure diagonal of `n` steps, Euclidean gives `n × 1.414`, and the alternating rule gives about `n × 1.5`. That is why the rule exists. It approximates `sqrt(2)` with integers a person can count at a table.

A design consequence. Suppose a grid game uses Chebyshev distance for movement ("move 6 squares in any direction"). A unit moving diagonally covers `6 × 1.414 ≈ 8.5` squares of real, straight-line distance. That is the week-12 diagonal bug in a new form. On a square grid, fixing it means either the alternating rule, a Euclidean check, or accepting the fast diagonals as a known quirk. Any of the three can be right. Leaving it undecided is the mistake.

## 4. Two radii: hysteresis for aggro and leash

Picture a mob with an aggro radius of 10 meters that stops chasing when the player is farther than 10 meters. A player standing at 9.9 meters is chased. The player steps back to 10.1 and the mob gives up. Steps forward, chased again. Near the boundary the mob flickers between states every few frames. The numbers in this example are invented for teaching, not taken from a particular game.

The standard fix is **hysteresis**, meaning the rule for entering a state is different from the rule for leaving it. Use two radii:

```
state IDLE:   if S ≤ r_aggro²  → state CHASE
state CHASE:  if S > r_leash²  → state RETURN
```

With `r_aggro = 10` and `r_leash = 30`, the mob starts chasing at 10 meters and does not give up until the player is 30 meters away. The 20-meter band between them is where the mob's current state decides the answer. Here is a player walking in and back out:

| Player distance | Mob state before | Rule checked | Mob state after |
|---|---|---|---|
| 25 | IDLE | 625 ≤ 100? no | IDLE |
| 12 | IDLE | 144 ≤ 100? no | IDLE |
| 9 | IDLE | 81 ≤ 100? yes | CHASE |
| 12 | CHASE | 144 > 900? no | CHASE |
| 25 | CHASE | 625 > 900? no | CHASE |
| 31 | CHASE | 961 > 900? yes | RETURN |

The player stood at 12 meters twice, and at 25 meters twice, and got a different mob state each time. That is hysteresis working. The squared thresholds 100 and 900 are what the code stores.

Minecraft's despawn rule has the same two-radius shape, used for a different reason. The 32-to-128 band stops mobs from vanishing the instant you look away, while the 128 boundary puts a hard limit on how many far-away mobs the game must keep. CS203 builds full aggro, leash and threat systems on this idea (see [CS203 week 12, MMO mob AI](../../CS203-artificial-intelligence-for-games/lectures/w12-mmo-mob-ai-leashing-aggro-threat-tables.md)). MMO302 uses the same two-radius pattern to decide which players a server sends updates about (see [MMO302 week 3, area of interest with hysteresis](../../MMO302-mmo-server-architecture/lectures/w03-area-of-interest-grids-radius-hysteresis.md)).

## 5. Range checks at scale

The squared-distance trick removes a square root per check. The number of checks is often the bigger problem.

If `n` objects each check every other object, that is `n × (n − 1) / 2` pairs. For 100 objects, 4,950 pairs. For 1,000 objects, 499,500 pairs. For 10,000, almost 50 million, every tick. The cost grows with the square of the population. Removing a square root makes each check a little cheaper. It does not change how many checks there are.

The standard remedy is to avoid checking pairs that cannot possibly be close. Divide the world into a grid of cells at least as wide as the largest range you care about. An object only needs to check objects in its own cell and the neighboring cells. If objects are spread out, each cell holds a handful, and the work grows roughly in proportion to `n` instead of `n²`. MA201 covers grids and quadtrees in detail (see [MA201 week 11, spatial partitioning](../../MA201-linear-algebra-and-physics-for-games/lectures/w11-spatial-partitioning-grids-and-quadtrees.md)).

Two more range tests you will use constantly, both in squared form:

- **Two circles overlap** when the distance between centers is at most the sum of the radii: `S ≤ (r1 + r2)²`. Square the sum, not each radius. `(3 + 4)² = 49`, while `3² + 4² = 25`. Mixing these up shrinks every hitbox.
- **Nearest of several targets.** Keep the candidate with the smallest `S`. Because squaring preserves order, the smallest `S` belongs to the smallest `D`. Take a square root only at the end, and only if you need the actual distance.

## 6. When you do need the real distance

Some systems need `D` itself. An ordering is not enough for them.

- **Falloff.** Sound volume, explosion damage and light intensity usually fade with distance. A linear fade is `clamp(invlerp(r, r_full, D), 0, 1)`, the week-8 inverse lerp. You need `D` for that shape.
- **Displayed numbers.** If the UI says "34 m to objective," compute `D`.
- **Movement by a fixed amount.** To move 5 meters toward a target you need the unit direction `d / D`, which needs `D` (week 12's normalize).

A useful habit is to compute `S` first, reject everything outside the largest relevant radius, and then take `sqrt(S)` only for the few survivors that need a real distance. That is the same "cheapest test first" ordering you used for the guard last week, with range before cone before raycast.

## In-class activity (25 minutes)

In groups of three, design the range rules for one monster camp in an open-world game. You need the interactive, a calculator and a sheet of graph paper.

1. Choose an aggro radius and a leash radius. Write both, and both squared.
2. Choose a despawn rule for the camp's monsters when no player is nearby, with a safe radius and an instant radius. Write all four numbers (two radii, two squares).
3. Pick a metric. If your game uses a grid, pick one of the grid metrics from section 3 and say why.
4. Draw your rings on graph paper at a scale where one square is 5 meters. Place five player positions that test each boundary, including at least one diagonal case where your metric and Euclidean distance disagree.
5. For each position, compute `S` by hand and write the monster's state.

**Expected output:** one page with the radii and their squares, the drawing, a 5-row table, and two sentences on what problem your leash band prevents.

## Common misconceptions

- **"Squared distance is an approximation."** It is exact for comparisons. `D ≤ r` and `D² ≤ r²` are the same statement when both sides are non-negative. It is only wrong when you use `S` as if it were a distance, for example in a falloff or a UI label.
- **"Checking each axis separately is the same as checking distance."** `abs(dx) ≤ r and abs(dy) ≤ r` tests a square, which reaches `r × sqrt(2)` on the diagonals. It is a fine cheap first filter, but it is not a circle.
- **"To compare with squared distance, square everything."** Square the threshold and compare it with `dx² + dy²`. For overlapping circles, square the sum of the radii, not each radius.
- **"Removing the square root fixes performance."** It trims each check. The number of pairs, which grows with `n²`, usually dominates. Spatial partitioning fixes that.

## Check yourself

1. A pickup has a 1.5 m radius. The player is at (3.2, 0.9) and the pickup at (2.0, 1.8). Is the pickup collected? Use squared distance only.
2. Two circular hitboxes have radii 0.4 and 0.6 and centers 0.95 apart along x. Do they overlap? What squared threshold does the code store?
3. On a D&D 3.5 grid, is a target 5 squares east and 4 squares north within a 30-foot (6-square) range? What would Chebyshev and Euclidean say?
4. A mob with aggro radius 8 m and leash radius 20 m is chasing. The player is at 15 m. Is the mob still chasing? What would a single-radius rule at 8 m have done?
5. Positions are stored as 32-bit integers in centimeters. Beyond what distance does `dx² + dy²` overflow on a single axis difference?

<details>
<summary>Answers</summary>

1. `dx = 1.2`, `dy = −0.9`. `S = 1.44 + 0.81 = 2.25`. `r² = 2.25`. `S ≤ r²`, so yes, exactly on the edge (`D = 1.5`). In floating point, a case this close can round either way, so do not build puzzles that depend on exact edges.
2. The threshold is `(0.4 + 0.6)² = 1.0`. `S = 0.9025`, which is less than 1.0, so they overlap.
3. Alternating: `max + floor(min/2) = 5 + 2 = 7` squares, out of range. Chebyshev: `max(5, 4) = 5`, in range. Euclidean: `sqrt(41) ≈ 6.40`, out of range.
4. Yes. `S = 225`, which is not greater than `20² = 400`, so it keeps chasing. A single 8 m radius would have dropped the chase as soon as the player passed 8 m.
5. `sqrt(2,147,483,647) ≈ 46,341` cm, about 463 m. With two axes both contributing, the sum can overflow sooner, at about 46,341 / 1.414 ≈ 32,768 cm per axis on a diagonal.

</details>

## Lab hook

**Lab 14, Range queries.** In [`labs/lab14.md`](../labs/lab14.md) you classify a data set of mob and player positions into Minecraft-style despawn zones using squared distance, verify that the results match a square-root version exactly, reproduce an overflow bug, and implement an aggro and leash state machine. The lab's metric comparison is a candidate topic for the curve-design mini project in week 15.

## Sources

- Minecraft Wiki, "Mob spawning," section "Despawning" (retrieved September 2026; describes current Java and Bedrock editions). Java: 1-in-800 chance per tick when no player is within 32 blocks after the inactivity delay, instant despawn beyond 128 blocks (64 for fish), Euclidean sphere with the (65, 65) and (91, 91) examples. Bedrock: 128 blocks at simulation distance 6 and up, 44 at simulation distance 4, 40 for fish. The wiki describes behavior; this lecture does not claim how Mojang's code computes it.
- Unity Technologies, Scripting API, `Vector3.sqrMagnitude` (current documentation, retrieved September 2026). Recommends squared magnitude for comparisons because it skips the square root.
- d20 System Reference Document (D&D 3.5), "Movement, Position, and Distance." The alternating 1-2-1 cost for diagonal moves on a grid.
- Dunn, F. & Parberry, I. (2011). *3D Math Primer for Graphics and Game Development*, 2nd ed. CRC Press. Chapter 2.
- Holmér, F. (2022). *Math for Game Devs [2022, part 1]: Numbers, Vectors and Dot Product*. YouTube lecture recorded for Futuregames students.

## Interactive spec: examples/w14-range-rings.html

**The one insight the visual must make obvious:** squaring bends the ruler but keeps the order. Every "closer than r" answer computed with `D` is identical when computed with `S = D²` against `r²`. The bug to show is comparing `S` with an unsquared `r`.

**Layout.** Map left and number lines right on desktop, stacked on mobile (map first). Readouts under both.

**View A, top-down map.**
- World from −160 to 160 blocks on both axes (x right, z down is fine, label axes "x" and "z"). Grid lines every 16 blocks, labels every 32.
- Mob drawn as a generic circle at the origin. No Minecraft art, textures or characters.
- Ring 1 (inner, `r_near`, default 32) and ring 2 (outer, `r_far`, default 128), drawn as the true set `metric(dx, dz) = r` for the chosen metric. For Euclidean they are circles; Manhattan diamonds; Chebyshev squares; Alternating octagons (draw by marching over integer cells and outlining the region).
- Zone shading: safe (inside inner), random (between), despawn (outside outer), three distinct palette tones plus text labels.
- Player drawn as a generic diamond, draggable with pointer. Keyboard: arrows move 1 block, Shift + arrows move 10 blocks. Coordinates snap to integers.
- Dashed line from mob to player, labeled with `D`.

**View B, linked number lines.**
- Top line: distance `D` from 0 to 200, ticks every 25, with marks at `r_near` and `r_far`.
- Bottom line: squared distance `S` from 0 to 40,000 (linear scale), ticks every 5,000, with marks at `r_near²` and `r_far²`.
- Thin connector lines join `D = k` to `S = k²` for k = 0, 16, 32, 48, ..., 192, and bold connectors for the two radii. Connectors never cross.
- Player marker on both lines with a connector between them.
- With the bug toggle on, the bottom-line threshold marks move to `S = r_near` and `S = r_far` (32 and 128). Draw their connectors back up to `D = sqrt(32) ≈ 5.66` and `D = sqrt(128) ≈ 11.31` in the warning color, and redraw the map rings at those radii. Caption: "Compared S with r instead of r²."

**Controls.**
- Inner radius slider: 8 to 64, step 1, default 32.
- Outer radius slider: 32 to 160, step 1, default 128. Enforce outer ≥ inner.
- Metric select: Euclidean (default), Manhattan, Chebyshev, Alternating diagonal (D&D 3.5). In non-Euclidean modes, `S` readout shows "n/a (integer metric)" and the number lines show the metric value on the top line only, with a note that grid metrics need no square root.
- Toggle "Forgot to square the radius" (default off, Euclidean only).
- Toggle "Per-axis box check" (default off): shades the square `|dx| ≤ r_far and |dz| ≤ r_far` outline in dashed style over the circle, so the corners outside the circle are visible.
- Button "Snap to test positions" cycles the player through the table below.

**Readouts (monospace):** `dx`, `dz`, `S` (integer), `D` (2 decimals), `r_near²`, `r_far²`, the comparison lines written out (for example `16,562 > 16,384 → despawn`), Manhattan, Chebyshev and Alternating values for the current offset, and zone name.

**Exact formulas.**
- `S = dx² + dz²`, `D = sqrt(S)`.
- Zone (Euclidean): `S ≤ r_near²` safe, `S ≤ r_far²` random, else despawn.
- Manhattan `|dx| + |dz|`. Chebyshev `max(|dx|, |dz|)`. Alternating `max + floor(min / 2)`. Zones compare these directly against the radii.

**Test values (defaults, Euclidean, mob at origin).** Readouts must match:

| Player (x, z) | S | D | Zone |
|---|---|---|---|
| (20, 20) | 800 | 28.28 | safe |
| (30, 10) | 1,000 | 31.62 | safe |
| (30, 30) | 1,800 | 42.43 | random |
| (65, 65) | 8,450 | 91.92 | random |
| (90, 90) | 16,200 | 127.28 | random |
| (100, 80) | 16,400 | 128.06 | despawn |
| (91, 91) | 16,562 | 128.69 | despawn |
| (120, 50) | 16,900 | 130.00 | despawn |

Metric checks at offset (6, 6): Euclidean 8.49, Manhattan 12, Chebyshev 6, Alternating 9. At (3, 4): 5.00, 7, 4, 5. Bug mode: player at (10, 5), `S = 125`, shows random zone (should be safe); player at (12, 0), `S = 144`, shows despawn.

**First screen.** Player at (90, 90), random zone, with the marker just under the `r_far²` mark on the S line. Caption: "One block further on each axis and this mob is gone. Drag the player."

**Accessibility and motion.** Native labeled inputs; zone shown by text as well as color. Snap animation disabled under `prefers-reduced-motion`. Palette from `templates/interactive-tokens.css`, light and dark.

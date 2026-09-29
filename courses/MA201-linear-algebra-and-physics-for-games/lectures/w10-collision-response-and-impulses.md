# MA201 · Week 10 — Collision Response and Impulses

**Why this matters:** Last week your code learned to say "these two things overlap." That answer is useless until something happens next. The ball has to bounce, the crate has to slide, the barrel has to roll away at the right speed. One formula, the collision impulse, decides all of it, and every engine you will use computes it for you with settings you choose. If you don't know what those settings do, you get balls that bounce forever, crates that stick to walls, and a bouncy mushroom that works on grass and dies on stone.

**You will be able to:**
- Compute the impulse for a collision between two bodies from their masses, velocities, the contact normal and the coefficient of restitution.
- Predict the speeds after a collision for equal masses, unequal masses and immovable walls, and check the answer with momentum and kinetic energy.
- Explain what a restitution threshold, a combine rule and a friction clamp do, and choose values for a design goal.
- Correct overlap after a collision without adding energy or jitter.

**Before class:** Dunn & Parberry, *3D Math Primer for Graphics and Game Development* (2nd ed.), section 12.4, "Impulsive forces and collisions" (free at gamemath.com). Millington, *Game Physics Engine Development* (2nd ed., 2010), chapter 7, "Hard constraints", up to the contact resolver algorithm. Optional: Chris Hecker, "Physics, Part 3: Collision Response" (*Game Developer*, Feb/Mar 1997, free on chrishecker.com).

**Prerequisites from earlier courses:** [MA101 week 12, 2D vectors](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w12-2d-vectors.md) (normalize, scale, add). [MA101 week 13, the dot product](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w13-dot-product-facing-and-vision-cones.md) (projecting a vector onto a direction). [CS101 week 10, collision basics](../../CS101-programming-for-games-i/lectures/w10-collision-basics-aabb-and-circles.md), section 4 (minimum push-out). [MA201 week 7, numerical integration](w07-numerical-integration-euler-semi-implicit-verlet.md) (semi-implicit Euler, used in the lab's drop test). [MA201 week 8, forces, mass and drag](w08-forces-mass-and-drag.md) (inverse mass, and why an impulse is not a force). [MA201 week 9, collision detection](w09-collision-detection-spheres-aabb-sat.md) (which hands you the contact normal and depth).

**Interactive:** [`examples/w10-impulse-bounce.html`](../examples/w10-impulse-bounce.html). Keep it open during sections 2 and 3.

---

## 1. What detection hands you, and the two jobs of response

Week 9's detection step answers three questions for a pair of shapes A and B that overlap:

- the **contact normal** `n`, a unit vector pointing from A toward B along the direction that separates them fastest;
- the **penetration depth** `d`, how far they overlap along `n`;
- a **contact point**, where they touch. You need it for spin, which this lecture mostly sets aside.

Response then has two separate jobs. Beginners mix them up, and most collision bugs come from that.

1. **Fix the velocities** so the bodies stop moving into each other. A ball that hits the floor must now move up, or at least stop moving down.
2. **Fix the positions** so the bodies stop overlapping. A ball that sank 3 cm into the floor during the last step must come back out.

In CS101 week 10 you did only job 2. The player's box was pushed out of the wall along the shallower axis, and its velocity was left alone. That works for a character controller, because the next frame's input sets a new velocity anyway. It fails for anything that moves on its own momentum. A ball pushed out of the floor but still carrying its downward velocity sinks straight back in on the next step, gets pushed out again, and sits there buzzing. Job 1 is this lecture's main subject. Job 2 comes back in section 5.

### The quantity that matters: velocity along the normal

Only one number decides whether a collision needs a velocity fix. Take the velocity of B relative to A and project it onto the normal with the dot product from MA101 week 13:

```
v_n = (v_B − v_A) · n
```

- `v_n < 0`: B is moving toward A along the normal. They are **approaching**, and you must act.
- `v_n > 0`: they are already separating. Do nothing, even though they overlap. Applying an impulse here would pull them back together.
- `v_n = 0`: they are resting or sliding along each other.

The sideways part of the relative velocity, the part along the surface, is the **tangential velocity**. It matters for friction (section 4) and not for bouncing.

## 2. Worked example: the stop shot, and one impulse for every bounce

### The hook

Anyone who has played a pool game, from a phone app to a full simulator, has seen the stop shot. Hit an object ball dead center with a cue ball that is sliding rather than rolling, and the cue ball stops on the spot while the object ball carries on at almost the same speed. It looks like the cue ball handed over its motion and kept nothing.

Now throw the same ball at the cushion. It comes back. Roll a light ball into a heavy one and the light ball bounces back while the heavy one creeps forward. Let a heavy ball hit a light one and the light one shoots away faster than the heavy one was ever moving.

Four different outcomes. One formula produces all of them, with only the masses and one "bounciness" number changing.

### The model

An **impulse** is a large force applied for a very short time. Physics engines treat a collision as instantaneous, so they skip the force and apply its total effect, the impulse `J`, which changes momentum directly. A body of mass `m` hit by impulse `J` changes velocity by `J / m`.

The collision impulse acts along the normal, equal and opposite on the two bodies (Newton's third law). Its size `j` is chosen so that after the collision the normal velocity obeys **Newton's law of restitution**:

```
v_n' = −e × v_n
```

`e` is the **coefficient of restitution**. `e = 1` means the bodies separate as fast as they approached (perfectly elastic). `e = 0` means they stop approaching and do not separate at all (perfectly inelastic). Real pool balls sit between 0.92 and 0.98. A ball against a cushion is 0.6 to 0.9.

Solving for `j` gives the model, stated once:

```
v_n  = (v_B − v_A) · n                       only act if v_n < 0
j    = −(1 + e) × v_n / (1/m_A + 1/m_B)
v_A' = v_A − (j / m_A) × n
v_B' = v_B + (j / m_B) × n
```

- `v_A`, `v_B` are velocities before the collision; primes mark velocities after.
- `n` is the unit contact normal from A to B.
- `m_A`, `m_B` are masses. Engines store the **inverse mass** `1/m`, because an immovable object (a wall, the floor, a kinematic platform) then has inverse mass 0 and needs no special case.
- `e` is the restitution for this pair.
- `j` is the impulse size, in newton-seconds (kg·m/s). It is always positive when the bodies approach.

Two facts follow directly, and they are your checks on every answer.

- **Momentum is conserved.** A loses `j × n` of momentum and B gains exactly `j × n`. Total momentum `m_A v_A + m_B v_B` is the same before and after, whatever `e` is. (A wall is the exception, because its infinite mass soaks up momentum without moving.)
- **Kinetic energy drops by a fixed share.** The energy lost is `½ μ (1 − e²) v_n²`, where `μ = 1 / (1/m_A + 1/m_B)` is the **reduced mass**. With `e = 1` nothing is lost. With `e = 0` the most is lost that momentum conservation allows.

### Numbers you can check

Put everything on one line so vectors become plain numbers. The normal is `n = +1` (pointing right), A moves right at 2 m/s, B is at rest. This code is the model for that 1D case.

```python
def collide_1d(m_a, v_a, m_b, v_b, e):
    """Head-on collision along +x. A mass of None means immovable (a wall)."""
    inv_a = 0.0 if m_a is None else 1.0 / m_a
    inv_b = 0.0 if m_b is None else 1.0 / m_b
    v_n = v_b - v_a                    # relative velocity along n = +x
    if v_n >= 0:                       # separating or resting: no impulse
        return v_a, v_b, 0.0
    j = -(1 + e) * v_n / (inv_a + inv_b)
    return v_a - j * inv_a, v_b + j * inv_b, j

cases = [
    ("pool, e = 0.95",        0.17, 2.0, 0.17, 0.0, 0.95),
    ("pool, e = 1",           0.17, 2.0, 0.17, 0.0, 1.0),
    ("ball into rail, e=0.75",0.17, 2.0, None, 0.0, 0.75),
    ("heavy hits light",      10.0, 2.0, 1.0,  0.0, 1.0),
    ("light hits heavy",      1.0,  2.0, 10.0, 0.0, 1.0),
    ("equal, e = 0 (stick)",  1.0,  2.0, 1.0,  0.0, 0.0),
]
for name, ma, va, mb, vb, e in cases:
    va2, vb2, j = collide_1d(ma, va, mb, vb, e)
    print(f"{name:24s} j={j:6.3f}  v_a'={va2:+.3f}  v_b'={vb2:+.3f}")
```

It prints:

```
pool, e = 0.95           j= 0.332  v_a'=+0.050  v_b'=+1.950
pool, e = 1              j= 0.340  v_a'=+0.000  v_b'=+2.000
ball into rail, e=0.75   j= 0.595  v_a'=-1.500  v_b'=+0.000
heavy hits light         j= 3.636  v_a'=+1.636  v_b'=+3.636
light hits heavy         j= 3.636  v_a'=-1.636  v_b'=+0.364
equal, e = 0 (stick)     j= 1.000  v_a'=+1.000  v_b'=+1.000
```

The pool balls are 0.17 kg, a standard 6 oz ball. Work the first row by hand. `v_n = 0 − 2 = −2`. The inverse masses sum to `2 / 0.17 = 11.76`. So `j = 1.95 × 2 / 11.76 = 0.3315`. The cue ball loses `0.3315 / 0.17 = 1.95` m/s and keeps 0.05 m/s. The object ball gains 1.95 m/s. That is the stop shot, give or take a creep of 5 cm per second.

Now check the two conservation facts on the same rows.

| Case | Momentum before | Momentum after | KE before (J) | KE after (J) | KE lost |
|---|---|---|---|---|---|
| Pool, e = 0.95 | 0.340 | 0.340 | 0.340 | 0.323 | 4.9% |
| Ball into rail, e = 0.75 | 0.340 | −0.255 | 0.340 | 0.191 | 43.8% |
| Heavy hits light, e = 1 | 20.0 | 20.0 | 20.0 | 20.0 | 0% |
| Light hits heavy, e = 1 | 2.0 | 2.0 | 2.0 | 2.0 | 0% |
| Equal, e = 0 | 2.0 | 2.0 | 2.0 | 1.0 | 50% |

Momentum holds in every row except the rail, where the immovable cushion takes the difference. The rail row also shows the wall case of the energy rule. With an infinite mass, `μ` is just the ball's mass, and the ball keeps `e² = 0.5625` of its energy.

Read the mass rows again. When a 10 kg body at 2 m/s hits a 1 kg body with `e = 1`, the light one leaves at 3.64 m/s, 1.8 times the heavy one's speed. As the mass ratio grows, that factor approaches 2, the speed of a ping-pong ball hit by a bat. When the light one does the hitting, it bounces back at almost its full speed and the heavy one barely moves. Those are the outcomes you have seen in every physics sandbox. They come from the same line of code.

### A visual you can move

Open [`examples/w10-impulse-bounce.html`](../examples/w10-impulse-bounce.html). The left view is a track with two blocks sliding toward each other, sized by mass. The right view shows two pairs of bars, momentum before and after and kinetic energy before and after. It opens on the pool case at `e = 0.95`.

Drag `e` from 1 down to 0. The blocks' exit speeds change, and so does the energy bar. The momentum bars do not move at all. Now drag the mass of B from 0.17 kg up to 10 kg. The cue ball stops stopping, turns around and bounces back, and the momentum bars still match. The one thing the view makes obvious is that `e` decides how much energy survives, and nothing you set can change the total momentum. Finally switch B to "wall" and watch the momentum bars stop matching, because the wall is now part of the system.

### Cross-game recognition

Every rigid-body engine you will meet solves this impulse, extended with spin (section 6). What they differ on is how a pair of materials becomes one `e`, and when to ignore it.

**Box2D (v2.4.1).** Box2D is the 2D engine behind *Angry Birds*, *Limbo* and *Shovel Knight*, among others. Each fixture has a `restitution`, default 0, and a contact takes the **larger** of the two (`b2MixRestitution` returns the max). Friction mixes as the square root of the product. A bouncy ball on a dead floor therefore bounces fully. The contact solver applies restitution only when the approach speed exceeds a `restitutionThreshold`, which defaults to 1 m/s. Below that, `e` is treated as 0.

**Unity (PhysX, Unity 6).** A Physics Material has a `Bounciness` from 0 to 1, default 0, and a `Bounce Combine` mode. The default is Average. The other modes are Minimum, Multiply and Maximum, and when two materials disagree, Unity uses the one higher in the order Maximum, Multiply, Minimum, Average. The same bouncy ball (`e = 0.9`) on a dead floor (`e = 0`) gets 0.45 by default. The global `Physics.bounceThreshold` defaults to 2. Two objects approaching slower than that do not bounce.

**Godot (built-in physics, Godot 4).** A `PhysicsMaterial` has `bounce` from 0 to 1. Godot's own 3D solver **adds** the two bounces and clamps the sum to 1, so two half-bouncy objects give a perfectly elastic collision. Setting `absorbent` on one material subtracts its bounce instead.

Rewrite all three in this lecture's form and they are the same line, `j = −(1 + e) v_n / (1/m_A + 1/m_B)`, with a different function choosing `e`:

| Engine | `e` for ball (0.9) on floor (0) | `e` for two 0.5 materials | Bounce only if approach speed ≥ |
|---|---|---|---|
| Box2D v2.4.1 | max = 0.9 | 0.5 | 1 m/s (per fixture) |
| Unity 6, default Average | 0.45 | 0.5 | 2 (project setting) |
| Godot 4, built-in 3D | sum, clamped = 0.9 | 1.0 | none in this rule |

The pool table is the fourth context. The billiards numbers (ball-ball 0.92 to 0.98, ball-cushion 0.6 to 0.9) are measurements of the same `e`.

### Eyes-open design judgment

- **Decide the combine rule before you tune materials.** Under max, the bounciest surface in a pair wins, so one bouncy prop bounces off everything. Under average, a bouncy mushroom loses half its bounce on dead ground. Under add, two moderately bouncy objects become perfectly elastic. None is wrong, but a designer who tunes values without knowing the rule will be surprised in playtest.
- **`e` above 1 adds energy.** The formula accepts it, and some games want it for jump pads and bumpers. Pinball bumpers are the classic case. Give such objects infinite mass (inverse mass 0) so the extra energy goes into the player, and cap the result, or two bumpers facing each other become a perpetual-motion machine.
- **Don't simulate what you can script.** If a jump pad must always launch the player to exactly the same ledge, set the velocity directly. Restitution makes the result depend on how fast the player arrived, which is realistic and often not what the level needs.
- **Momentum is a promise to the player.** A heavy boss that gets knocked back by a light arrow breaks the mass rows of the table above, and players notice. If you want that for game feel, apply it as a scripted knockback, not by lying about mass.

## 3. Why balls stop: the restitution threshold

Drop a ball from height `h` onto a static floor. It hits at speed `v₀ = √(2gh)`, leaves at `e v₀`, and rises to `e² h`. Every bounce keeps `e²` of the height. With `e = 0.8` the heights go 64%, 41%, 26%, 17% of the drop, and so on forever.

Forever is the problem. The bounces get shorter as well as lower. The total time is a geometric series, and it is finite:

```
t_total = t₀ × (1 + e) / (1 − e),   t₀ = √(2h / g)
```

For `h = 1` m and `e = 0.8`, `t₀ = 0.452` s and the ball comes to rest after 4.06 s, having bounced infinitely often. A real ball does this (until the bounces are smaller than the dimples in the floor). A simulator stepping at 60 Hz cannot. Once a bounce lasts less than one step, the ball spends every step either inside the floor or barely above it, and each impulse sends it up by a fraction of a millimetre. On screen that looks like a ball that vibrates on the ground and never settles. The fix engines use is the threshold from the table above. Below a certain approach speed, set `e = 0`.

```python
import math

G = 9.81

def drop(h, e, threshold):
    """Drop from height h onto a static floor. Return (bounces, heights, time to rest)."""
    v = math.sqrt(2 * G * h)          # speed at first impact
    t = v / G                         # time of the fall
    heights = []
    while v * e > 0 and v >= threshold:   # engine bounces only above the threshold
        v *= e                        # Newton's law: rebound = e x impact speed
        heights.append(v * v / (2 * G))
        t += 2 * v / G                # up and back down
    return len(heights), heights, t

for thr in (0.0001, 1.0, 2.0):
    n, hs, t = drop(1.0, 0.8, thr)
    print(f"threshold {thr:>6} m/s: {n:2d} bounces, rest at {t:.2f} s, "
          f"first heights {[round(x, 3) for x in hs[:4]]}, last {hs[-1]:.3f} m")

t0 = math.sqrt(2 * 1.0 / G)
print(f"exact limit: {t0 * (1 + 0.8) / (1 - 0.8):.2f} s")
```

```
threshold 0.0001 m/s: 48 bounces, rest at 4.06 s, first heights [0.64, 0.41, 0.262, 0.168], last 0.000 m
threshold    1.0 m/s:  7 bounces, rest at 3.31 s, first heights [0.64, 0.41, 0.262, 0.168], last 0.044 m
threshold    2.0 m/s:  4 bounces, rest at 2.58 s, first heights [0.64, 0.41, 0.262, 0.168], last 0.168 m
exact limit: 4.06 s
```

Read the last column. With Box2D's default of 1 m/s the ball makes a 4.4 cm hop and then stops dead, which few players notice. With Unity's default of 2, the last bounce is 17 cm high and the next impact just stops, which players can see. The threshold that fixes jitter also clips the tail of every bounce. If your game is about bouncing balls, lower the threshold and accept a little more solver work. If it is about crates, raise it.

Open the interactive's "Drop test" tab. It plots height against time for the three thresholds on the same axes. They agree exactly until each one's cutoff, and then the higher threshold drops to a flat line early.

## 4. Friction: an impulse along the surface, with a clamp

The normal impulse stops bodies moving into each other. Friction resists them sliding along each other. It is a second impulse, along the **tangent** `t`, the unit direction of the sliding velocity.

The **Coulomb friction** rule says friction can push back at most `μ` times as hard as the surfaces press together, where `μ` is the **coefficient of friction**. In impulse form:

```
v_t   = (v_B − v_A) · t                     sliding speed along the tangent
j_t   = −v_t / (1/m_A + 1/m_B)              impulse that would stop the sliding
j_t   = clamp(j_t, −μ j, +μ j)              friction can't exceed μ × normal impulse
```

The clamp is the whole idea. If the impulse needed to stop sliding is small, friction stops it and the bodies grip. If it is large, friction gives the most it can and the bodies keep sliding, slower.

Take a 10 kg crate landing on the floor at `v = (3, −2)` m/s with `e = 0` and `μ = 0.5`. The normal impulse is `j = 2 / 0.1 = 20` N·s, which kills the vertical speed. Stopping the 3 m/s slide would take `10 × 3 = 30` N·s, but friction may give only `0.5 × 20 = 10`. So the crate keeps `3 − 10 / 10 = 2` m/s of slide. With `μ = 1.5` the limit is 30 N·s and the crate stops dead on landing.

Notice that the friction limit comes from `j`. A crate that lands hard gets more grip on that step than one that lands gently. Engines apply friction every step for resting bodies as well, using the impulse that holds them up against gravity, which gives the everyday "heavier things are harder to push" behavior. The combine rules differ here too. Box2D uses `√(μ_A μ_B)`, Unity defaults to the average, and Godot's built-in solver takes the smaller value unless a material is marked `rough`.

## 5. Fixing the position without adding energy

The velocity fix makes the bodies separate from now on. It does nothing about the 3 cm the ball already sank into the floor. Three ways to deal with that, from worst to best.

**Teleport out fully.** Move each body out along `n`, splitting the distance by inverse mass so a wall doesn't move and two equal crates move half each:

```
move_A = −d × (1/m_A) / (1/m_A + 1/m_B) × n
move_B = +d × (1/m_B) / (1/m_A + 1/m_B) × n
```

This is CS101's push-out, weighted by mass. It works for one contact. In a stack of boxes each push-out creates a new overlap with the next box, and fully correcting every one each step makes the stack jitter.

**Push by velocity.** Add extra separating velocity proportional to the depth. It removes the overlap, but the extra velocity stays after the overlap is gone, so the body leaves the contact faster than it arrived. Deep overlaps turn into launches. This is the "objects explode apart when spawned inside each other" bug.

**Correct a fraction, leave a little slop.** Correct only part of the overlap each step and ignore a tiny amount. Box2D v2.4.1 does this with a separate position pass. Each step it removes `0.2 × (d − 0.005)` metres of overlap (its `b2_baumgarte` factor and `b2_linearSlop`), capped at 0.2 m per step, without touching velocity. The 5 mm of slop is left deliberately. A box resting on the floor stays in contact, which keeps the contact alive for the next step instead of flickering between touching and not touching.

For a 5 cm overlap, the excess over slop shrinks by a factor of 0.8 per step. After 5 steps it is `0.045 × 0.8⁵ = 1.5` cm over slop, and after 10 steps under 5 mm. At 60 Hz, that is 1/6 of a second of gradual correction, too fast to see and slow enough not to add energy. Because the correction never writes to velocity, the next step of the week 7 integrator starts from the impulse's velocity alone, and no energy leaks in.

## 6. What changes with spin

Everything above treats bodies as points. Real contacts happen away from the center of mass, so an impulse also makes the body spin. In 2D, with `r_A` and `r_B` the vectors from each center of mass to the contact point and `I` the moment of inertia, the denominator gains two terms:

```
j = −(1 + e) × v_n / (1/m_A + 1/m_B + (r_A × n)² / I_A + (r_B × n)² / I_B)
```

Here `r × n` is the 2D cross product, a single number, and `v_n` uses the velocity of the contact point, including spin. The structure is unchanged. The denominator is the "how hard is this contact to move" term, and hitting a body off-center makes it easier to move, because part of the impulse goes into rotation. Millington chapter 14 and Hecker's part 3 derive it fully. Box2D's `b2_contact_solver.cpp` computes exactly this denominator, which it calls the effective mass.

The other change is that real scenes have many contacts at once, such as a box resting on two corners or a stack of ten crates. Engines solve them by **sequential impulses**. They apply each contact's impulse in turn, loop over all contacts several times per step, and let the corrections settle. [MMO404 week 11, physics in MMOs](../../MMO404-advanced-networked-simulation/lectures/w11-physics-in-mmos.md), shows what that costs on a server.

## In-class activity (25 minutes)

In pairs, you are tuning the physics materials for a 2D platformer built on an engine with Unity's defaults (Average combine, bounce threshold 2).

1. The level designer wants a rubber ball that, dropped from 3 m onto normal ground (`e = 0`), bounces at least 5 times. Using `e² h` for heights and the threshold rule, find the ball's bounciness and the combine mode you need. Is the default threshold a problem?
2. The same ball must bounce at most twice on a mud material. Choose mud's bounciness and combine mode. Check both rules at once, keeping Unity's priority order in mind.
3. A spring pad must launch any player to 4 m regardless of fall height. Explain in two sentences why restitution cannot do this, and what you would do instead.
4. Swap answers with another pair and verify one of their numbers with the drop-test tab of the interactive.

Expected output: a small table of materials (bounciness, combine mode), the bounce counts they give, and the spring-pad paragraph.

## Common misconceptions

- **"Restitution is the fraction of speed each body keeps."** It is the fraction of *relative normal* speed that survives. In the pool shot the cue ball keeps 2.5% of its speed and the pair keeps 95% of its closing speed. Both are consistent with `e = 0.95`.
- **"An inelastic collision loses momentum."** It loses kinetic energy. Momentum is conserved for every `e`, unless one body is immovable and absorbs it.
- **"If they overlap, apply the impulse."** Apply it only when `v_n < 0`. Overlapping bodies that are already separating must be left alone, or the impulse pulls them back together and they stick.
- **"Fix overlap by pushing them apart faster."** Extra velocity outlives the overlap and launches bodies. Correct positions directly and gradually, with slop.

## Check yourself

1. A 2 kg body at 3 m/s hits a 1 kg body at rest, head on, with `e = 0.5`. Compute `j` and both final velocities. Verify momentum.
2. In the same collision, what fraction of kinetic energy is lost? Use the reduced-mass formula, then check it against the before-and-after speeds.
3. A ball with bounciness 0.6 lands on a floor with bounciness 0.2. What `e` does each engine in the cross-game table use? Under which engine does the ball bounce highest?
4. With `e = 0.9` and Box2D's 1 m/s threshold, how many bounces does a ball dropped from 2 m make?
5. A 5 kg crate lands at `(4, −3)` m/s on a static floor with `e = 0` and `μ = 0.4`. What is its horizontal speed after the landing step?

<details>
<summary>Answers</summary>

1. `v_n = 0 − 3 = −3`. Inverse masses sum to `0.5 + 1 = 1.5`. `j = 1.5 × 3 / 1.5 = 3` N·s. `v_A' = 3 − 3/2 = 1.5` m/s, `v_B' = 0 + 3/1 = 3` m/s. Momentum: `2 × 3 = 6` before, `2 × 1.5 + 1 × 3 = 6` after. The relative speed after is 1.5, half of 3, as `e = 0.5` requires.
2. `μ = 1 / 1.5 = 2/3` kg. Loss `= ½ × (2/3) × (1 − 0.25) × 9 = 2.25` J. Before: `½ × 2 × 9 = 9` J. After: `½ × 2 × 2.25 + ½ × 1 × 9 = 2.25 + 4.5 = 6.75` J. Lost 2.25 J, which is 25%.
3. Box2D max: 0.6. Unity average: 0.4. Godot sum: 0.8. The ball bounces highest under Godot.
4. Impact speed `√(2 × 9.81 × 2) = 6.26` m/s. Bounce `k` happens while `6.26 × 0.9^(k−1) ≥ 1`, so `0.9^(k−1) ≥ 0.1597`. That gives `k − 1 ≤ 17.4`, so 18 bounces.
5. Normal impulse `j = 5 × 3 = 15` N·s. Friction limit `0.4 × 15 = 6` N·s. Stopping the slide would need `5 × 4 = 20` N·s, so friction is clamped at 6 and the crate keeps `4 − 6/5 = 2.8` m/s.

</details>

## Lab / assignment hook

[Lab 10, an impulse resolver](../labs/lab10.md). You implement the normal impulse, friction clamp and positional correction for 2D circles and walls, check them against this lecture's tables, then tune one material table so that three design targets hold under a combine rule you choose. The resolver feeds the physics sandbox in the final assessment.

## Sources

- Alciatore, D. G. "Pool and billiards physics resources: physical properties" (Colorado State University, billiards.colostate.edu, accessed September 2026). Ball mass 6 oz; ball-ball restitution 0.92 to 0.98; ball-rail restitution 0.6 to 0.9.
- Catto, E. Box2D v2.4.1 source (GitHub `erincatto/box2d`, tag `v2.4.1`, 2020). `b2_contact.h` (`b2MixRestitution` takes the max, `b2MixFriction` the square root of the product); `b2_fixture.h` (default restitution 0, friction 0.2, `restitutionThreshold` 1 m/s); `b2_contact_solver.cpp` (restitution applied only when the approach speed exceeds the threshold; position correction with `b2_baumgarte` 0.2); `b2_common.h` (`b2_linearSlop` 0.005 m, `b2_maxLinearCorrection` 0.2 m).
- Wikipedia, "Box2D" (accessed September 2026). Games that used Box2D, including *Angry Birds*, *Limbo* and *Shovel Knight*.
- Unity Technologies. Unity 6.6 Manual, "Physics Material asset reference" and "How collider surface values combine"; Scripting API, `Physics.bounceThreshold` (default 2). Bounciness default 0, combine modes and their priority order. All checked 29 September 2026.
- Godot Engine. Godot 4.7 class reference, `PhysicsMaterial` (`bounce`, `absorbent`, `friction`, `rough`). Godot source, `modules/godot_physics_3d/godot_body_pair_3d.cpp` (master branch, 2026): `combine_bounce` clamps the sum of the two bounces to [0, 1]; `combine_friction` takes the smaller value.
- Dunn, F. & Parberry, I. *3D Math Primer for Graphics and Game Development*, 2nd ed., section 12.4 (gamemath.com).
- Millington, I. (2010). *Game Physics Engine Development*, 2nd ed. Morgan Kaufmann. Chapters 7, 14 and 15.
- Hecker, C. (1997). "Physics, Part 3: Collision Response." *Game Developer*, Feb/Mar 1997.

## Interactive spec: examples/w10-impulse-bounce.html

**The one insight:** the restitution coefficient decides how much kinetic energy survives a collision, and nothing you set changes total momentum. A second tab shows why engines need a bounce threshold: a finite drop contains infinitely many bounces, and the threshold cuts the tail off at a visible height.

**Layout.** Two tabs, "Collision" (default) and "Drop test". Tab bar is keyboard operable (arrow keys switch, Enter selects).

*Collision tab*: two linked views, side by side at 1280 px, stacked at 390 px (track on top).

- **Left, "Track":** a horizontal 1D track 4 m long. Block A starts at x = 0.8 m, block B at x = 2.4 m (centers). Block widths scale with the cube root of mass (0.1 m at 0.17 kg, clamp 0.08 to 0.4 m) so heavy blocks look heavy. A "wall" option draws B as a hatched fixed barrier at x = 3.0 m. Velocity arrows above each block, labelled with the value in m/s. The animation runs the approach, applies the impulse at contact (use the model, not an integrator), then runs 1.5 s after, and loops. After contact the "before" arrows stay as faint ghosts.
- **Right, "Conservation":** two grouped bar pairs. Momentum before and after (signed, axis through zero, kg·m/s). Kinetic energy before and after (J), with the lost share labelled as a percentage. Below, a readout block: `v_n`, `j`, `v_A'`, `v_B'`, reduced mass `μ`, energy lost, and "momentum conserved: yes" (or "no, the wall absorbed Δp = …" in wall mode).

**Controls (labelled, keyboard accessible):**

1. `e` slider 0 to 1.2, step 0.01, default 0.95. Values above 1 show a note: "adds energy".
2. Mass of A, log slider 0.05 to 20 kg, default 0.17.
3. Mass of B, same range, default 0.17. A checkbox "B is a wall (inverse mass 0)".
4. Velocity of A, −3 to 3 m/s, step 0.1, default 2. Velocity of B, same, default 0.
5. Preset buttons matching the lecture's table: "Pool 0.95", "Pool 1.0", "Rail 0.75", "Heavy hits light", "Light hits heavy", "Stick (e = 0)".
6. Play/Pause and Replay.

If `v_n ≥ 0` (not approaching), show "no collision: already separating" and draw no impulse.

*Drop test tab*: one plot, height (m) against time (s), 0 to 5 s, with three curves on the same axes: threshold "none" (use 0.0001 m/s), "1 m/s (Box2D default)", "2 (Unity default)". Parabolic arcs drawn analytically between impacts. Controls: drop height 0.5 to 5 m (default 1), `e` 0.1 to 0.99 (default 0.8). A table under the plot lists, per threshold, bounce count, last bounce height and time to rest. A horizontal dashed line marks the height of each threshold's last bounce.

**Formulas.** `v_n = v_B − v_A` (n = +x). If `v_n < 0`: `j = −(1 + e) v_n / (1/m_A + 1/m_B)` with `1/m_B = 0` in wall mode; `v_A' = v_A − j/m_A`, `v_B' = v_B + j/m_B`. `μ = 1/(1/m_A + 1/m_B)`; energy lost `= ½ μ (1 − e²) v_n²`. Drop: `g = 9.81`, `v = √(2gh)`, `t = v/g`; while `v ≥ threshold` and `e > 0`: `v ← e v`, record height `v²/(2g)`, `t += 2v/g`.

**Test values (must match the lecture).**

- Pool, `e = 0.95`, 0.17 kg each, 2 m/s into rest: `j = 0.332`, `v_A' = 0.050`, `v_B' = 1.950`, KE 0.340 → 0.323 J (4.9% lost).
- Pool, `e = 1`: `j = 0.340`, `v_A' = 0`, `v_B' = 2`.
- Rail (wall), `e = 0.75`, 0.17 kg at 2 m/s: `j = 0.595`, `v_A' = −1.5`, momentum 0.340 → −0.255, KE lost 43.8%.
- Heavy hits light (10 kg, 1 kg, `e = 1`): `j = 3.636`, `v_A' = 1.636`, `v_B' = 3.636`.
- Light hits heavy (1 kg, 10 kg, `e = 1`): `v_A' = −1.636`, `v_B' = 0.364`.
- Equal 1 kg, `e = 0`: both 1.000 m/s, 50% KE lost.
- Check yourself 1: 2 kg at 3 m/s into 1 kg, `e = 0.5`: `j = 3`, `v_A' = 1.5`, `v_B' = 3`, 25% KE lost.
- Drop test, `h = 1`, `e = 0.8`: none → 48 bounces, rest 4.06 s; 1 m/s → 7 bounces, last 0.044 m, rest 3.31 s; 2 → 4 bounces, last 0.168 m, rest 2.58 s.

**First screen.** Collision tab, pool preset at `e = 0.95`, animation playing, cue ball visibly stopping. Caption: "Same formula for every bounce. Drag e: the energy bar moves, the momentum bar never does."

**Accessibility.** All controls reachable by Tab with visible focus. A live region announces the readout after each collision ("j 0.332, A leaves at 0.05 m/s, B at 1.95 m/s"). `prefers-reduced-motion`: no looping animation, show a static before/after diagram. `prefers-color-scheme` via the shared tokens from `templates/interactive-tokens.css`. Plain rectangles and circles only, no game art.

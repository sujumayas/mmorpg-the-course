# MA201 · Week 13 — Projectile Motion and Aiming at Moving Targets

**Why this matters:** Every archer mob, turret, companion and auto-aim assist in your game has to answer one question many times a second. Where do I point so the shot and the target arrive at the same place at the same time? Get it wrong and your archers shoot at where players used to be. Get it perfectly right and your archers never miss, which is its own design problem. This week you learn to solve the question exactly, to know when it has no answer, and to decide how good your aim should be.

**You will be able to:**
- Derive the intercept quadratic `(u·u − s²)t² + 2(D·u)t + D·D = 0` for a straight-line projectile and a target at constant velocity, and pick the right root, or report that none exists.
- Compute the launch angles that hit a fixed point under gravity, and the aim vector that hits a moving target under gravity by solving for flight time numerically.
- Extend the aim to include a cast delay or network latency, and compute how much extra lead it needs.
- Design a projectile's speed, cast time and hit radius from a dodge budget, and critique an enemy archer whose aim is too good.

**Before class:** Millington, *Game Physics Engine Development* (2nd ed., 2010), chapter 3, the ballistics demo (projectile types with different speeds, gravity and damping). Dunn & Parberry, *3D Math Primer* (2nd ed., 2011), chapter 2, the dot product sections, as a reminder that `v·v = |v|²`. Reread section 3 of CS203 week 2 on pursuit.

**Prerequisites from earlier courses:** [MA101 week 3, quadratic curves](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w03-polynomials-and-quadratic-curves.md) (the quadratic formula, the discriminant and "does the jump reach?"). [MA101 week 11, atan2](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w11-atan2-turning-toward-a-target.md) (turning a direction vector into an angle). [MA101 week 13, the dot product](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w13-dot-product-facing-and-vision-cones.md). Looking ahead, [CS203 week 2, steering behaviors](../../CS203-artificial-intelligence-for-games/lectures/w02-steering-behaviors.md) (next semester) uses pursuit with a rough prediction time `T = D / max_speed`, and this week makes that estimate exact. [CS202 week 11, lag compensation](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w11-lag-compensation-rewind-hit-detection.md), also next semester, shows which projectiles still need a lead online. MA201 [week 6](w06-kinematics-position-velocity-acceleration.md) (constant acceleration, one axis at a time), [week 7](w07-numerical-integration-euler-semi-implicit-verlet.md) (integrators), [week 8](w08-forces-mass-and-drag.md) (drag) and [week 12](w12-raycasting.md) (raycasting, which hitscan weapons use).

**Interactive:** [`examples/w13-lead-the-target.html`](../examples/w13-lead-the-target.html). Keep it open during section 2.

---

## 1. Hitscan, projectiles and the time the world keeps moving

Games fire two kinds of shot. A **hitscan** shot resolves instantly. The game casts a ray from the muzzle (week 12) and whatever the ray touches this tick is hit. There is no flight time, so aiming at a moving target means pointing at it. A **projectile** is an object with a position and a velocity that the physics step moves every tick, like any other body from weeks 6 to 8. It takes time to arrive, and the target keeps moving during that time.

A projectile under constant acceleration is week 6's formula with a new name for the start velocity:

```
p(t) = p₀ + v·t + ½·g·t²
```

- `p₀` is the launch point, usually the muzzle or the archer's hand.
- `v` is the launch velocity. Its length `s = |v|` is the **projectile speed**, which the weapon's data sets. Its direction is the one thing the shooter controls.
- `g` is the gravity vector, for example `(0, −9.81, 0)` m/s² with y up. For rockets, magic bolts and most skillshots, designers set `g = 0` and the projectile flies in a straight line at constant speed.

Drag (week 8) bends the path further. Most game projectiles either ignore drag or apply a small per-tick factor. We ignore it until section 5.

The **aiming problem** reverses the formula. You know `p₀`, `s`, `g`, and where the target is and how it moves. You want the direction of `v`. This is harder than it looks, because where the target will be depends on when the shot arrives, and when the shot arrives depends on where you aim. The quantity that breaks the loop is the **flight time** `t`. Find `t` and everything else follows.

## 2. Worked example: the intercept quadratic

### The hook

In Team Fortress 2, the Soldier's rocket launcher fires rockets at 1,100 Hammer units per second (the Source engine's length unit). The Scout runs at 400 Hammer units per second. Fire at a Scout 1,000 units away who is running sideways, aimed straight at his body, and the rocket passes about 340 units behind him. That is several body widths. Players learn to "lead" by feel, aiming ahead of the target, and good Soldiers do it without thinking.

An enemy archer in your game has no feel. It has a position, a target position, a target velocity and an arrow speed, and it must produce a direction. CS203's pursuit guessed a prediction time with `T = distance / speed`. That guess is close but not exact, and this week you will see how close and why. The exact answer is a quadratic, and the quadratic also tells you when no aim will ever hit.

### The model

Put the shooter at the origin. Let the target start at relative position `D` and move at constant velocity `u`. The projectile flies in a straight line at speed `s` (no gravity for now), in a direction you choose.

After `t` seconds the target is at `D + u·t`. The projectile, whatever its direction, is somewhere on a circle (a sphere in 3D) of radius `s·t` around the shooter. The shot can hit at time `t` exactly when the target is on that circle:

```
|D + u·t| = s·t
```

Square both sides and expand with the dot product, using `|w|² = w·w`:

```
(D + u·t)·(D + u·t) = s²·t²
D·D + 2(D·u)·t + (u·u)·t² = s²·t²
(u·u − s²)·t² + 2(D·u)·t + D·D = 0
```

This is the **intercept quadratic**, `a·t² + b·t + c = 0` with

```
a = u·u − s²      (target speed squared minus shot speed squared)
b = 2·(D·u)       (negative if the target is closing, positive if it is leaving)
c = D·D           (distance squared, always positive)
```

Solve it with MA101 week 3's formula `t = (−b ± √(b² − 4ac)) / (2a)`, keep the smallest positive root, and aim at the **intercept point**

```
P = D + u·t          aim direction = P / |P|,  launch velocity v = P / t
```

The signs tell you which roots exist before you compute anything.

- **Shot faster than target** (`s > |u|`, the usual case). Then `a < 0` and `c > 0`, so the product of the roots `c / a` is negative. One root is positive and one negative. **There is always exactly one intercept**, whatever the target does.
- **Shot as fast as target** (`a = 0`). The equation is linear, `t = −c / b`. It has a positive answer only if `b < 0`, meaning the target is closing.
- **Shot slower than target** (`a > 0`). Both roots have the same sign. If the target is leaving (`b > 0`), both are negative and no aim works. If it is closing, there may be two intercepts or none, depending on the discriminant.

The geometry is worth a picture, and the interactive draws it. The target slides along a straight line. The shot's reach is a circle growing at speed `s`. The intercept is the first moment the growing circle touches the moving dot.

### Numbers you can check

Put the Soldier at the origin and the Scout at `D = (1000, 0)` Hammer units, with rocket speed `s = 1100`. Here is the solver in code. It handles the `a = 0` case and returns `None` when no root is positive.

```python
import math

def intercept_time(D, u, s):
    """Smallest t > 0 with |D + u t| = s t, or None."""
    a = u[0]**2 + u[1]**2 - s * s
    b = 2 * (D[0] * u[0] + D[1] * u[1])
    c = D[0]**2 + D[1]**2
    if abs(a) < 1e-9:                      # target as fast as the shot
        return -c / b if b < 0 else None
    disc = b * b - 4 * a * c
    if disc < 0:
        return None
    r = math.sqrt(disc)
    roots = sorted(((-b - r) / (2 * a), (-b + r) / (2 * a)))
    return next((t for t in roots if t > 0), None)

D, s = (1000.0, 0.0), 1100.0            # Scout 1,000 HU away, rocket 1,100 HU/s
for name, u in [("toward", (-400, 0)), ("across", (0, 400)),
                ("away", (400, 0)), ("Heavy across", (0, 230))]:
    t = intercept_time(D, u, s)
    aim = (D[0] + u[0] * t, D[1] + u[1] * t)
    lead = math.degrees(math.atan2(aim[1], aim[0]))
    print(f"{name:12} t = {t:.4f} s  aim ({aim[0]:7.1f}, {aim[1]:6.1f})  lead {lead:5.1f} deg")
```

Output:

```
toward       t = 0.6667 s  aim (  733.3,    0.0)  lead   0.0 deg
across       t = 0.9759 s  aim ( 1000.0,  390.4)  lead  21.3 deg
away         t = 1.4286 s  aim ( 1571.4,    0.0)  lead   0.0 deg
Heavy across t = 0.9296 s  aim ( 1000.0,  213.8)  lead  12.1 deg
```

Check the first and third rows by hand. Running straight toward the shooter, `|1000 − 400t| = 1100t` gives `t = 1000 / 1500 = 0.667` s. Running away, `1000 + 400t = 1100t` gives `t = 1000 / 700 = 1.429` s. In both cases the lead angle is zero, because the target moves along the line of fire. The Scout running across is the hard case. Here `b = 0`, so `t = √(c / −a) = √(1,000,000 / 1,050,000) = 0.976` s, and the rocket must be aimed 390 units ahead of him, 21.3° off his body. The Heavy (230 units per second in the game's class data) needs 12.1°.

Now compare with CS203's estimator. Pursuit predicted `T = distance / speed`, which is the time the shot would need to reach where the target is now. Aim there, and ask again how long the shot takes to reach *that* point. Repeating this is a **fixed-point iteration**, `t_next = |D + u·t| / s`:

| Guess | Assumed flight time | Actual flight time to that point | Target is this far from the aim point on arrival |
|---|---|---|---|
| 0 (aim at the body) | 0 | 0.9091 s | 363.6 HU |
| 1 (CS203's estimate) | 0.9091 s | 0.9673 s | 23.3 HU |
| 2 | 0.9673 s | 0.9748 s | 3.0 HU |
| 3 | 0.9748 s | 0.9758 s | 0.4 HU |
| Exact root | 0.9759 s | 0.9759 s | 0 |

The distances in the last column are `400 × (actual − assumed)`, how far the Scout travels between the time you assumed and the time the rocket gets there. (The closest the unled rocket ever gets to the Scout's body is 341.7 units, a little less than the 363.6 in row 0, because the rocket passes near him slightly before reaching the aim point.) CS203's estimate is the first step of this iteration. It removes 94% of the error in one step, which is why it works well for steering. Each further step cuts the error by roughly a factor of eight here. The quadratic jumps straight to the end.

The iteration converges only when the shot is faster than the target, and slowly when the two speeds are close. The quadratic has no such limit, and it tells you when to give up.

### A visual you can move

Open `examples/w13-lead-the-target.html`. The left view is top-down. The shooter sits at the left, the target moves along a dashed line, and a faint circle of radius `s·t` grows from the shooter as a scrubber moves `t`. Three aim modes fire three coloured shots at once: at the body, CS203's one-step estimate, and the exact intercept. The right view plots `g(t) = |D + u·t| − s·t` against `t`, the gap between where the target is and how far the shot can reach. The exact intercept is where that curve crosses zero, and the estimate's `T` is marked on the same axis.

Drag the target speed up toward the shot speed. On the left the lead point runs away along the target's path. On the right the curve flattens and its zero crossing slides out to large `t`. Push the target speed past the shot speed with the target moving away and the curve never crosses zero. The readout says "no intercept", and the left view shows the circle chasing a dot it can never touch. Set the heading straight toward the shooter and all three shots hit, which is the case your intuition tends to forget.

### Cross-game recognition

The same equation hides behind every "lead" in games. Each case below has a shot speed, a target speed and a delay, and the rewrite is the same.

**League of Legends (current patches), Ezreal's Mystic Shot.** The League of Legends Wiki lists a missile speed of 2,000 units per second, a range of 1,200, a listed width of 120 and a cast time of 0.25 s. Champion base movement speeds on the same wiki run from 325 to 355. The cast time is a **delay** `τ` before the missile exists. During it the target moves `u·τ`, so the missile starts from a shifted problem with `D' = D + u·τ`. For a target 1,000 units away moving across at 345 units per second, without the cast time you would lead by 175 units (flight 0.508 s). With it, `D' = (1000, 86.25)`, the flight is 0.517 s, and you must lead by 265 units, half as much again. The intercept point is 1,034 units away, inside the 1,200 range. The target has moved about twice the listed width before the bolt arrives, which is why the skill rewards prediction.

**Online play of any projectile weapon.** Latency is another delay. CS202 week 11 showed that many games, following Half-Life, do not lag-compensate projectiles. A player with 100 ms of latency is aiming at where the target was 100 ms ago, on top of the flight time, so the lead they need grows by `|u| × 0.1` s. That is the Mystic Shot correction with `τ` equal to the latency. Games that spawn fast projectiles further along their path are subtracting that delay back out.

**Guild Wars 2 (current), projectile skills.** The Guild Wars 2 Wiki defines a projectile as an attack that must travel to its target before dealing damage, and notes that most can be dodged, blocked or reflected, while a few auto-track a moving target. Auto-tracking is the designer choosing to solve the aiming problem for the player. A homing projectile re-aims every tick (MA101 week 11's turn toward a target), so the intercept quadratic stops mattering and dodging becomes the only defence. The same wiki notes projectiles travel further when fired from a height. That is gravity, and it is section 3.

**Steering AI (CS203 week 2).** Pursuit's `T = D / max_speed` is guess 1 in the table above. A pursuer that re-predicts every frame runs the fixed-point iteration one step per frame, spread over time, which is why it converges on moving quarry even with a crude estimate.

Four contexts, one model. Write down the shot speed, the target velocity and every delay before the shot exists, then solve `|D' + u·t| = s·t`.

### Eyes-open design judgment

An exact solver is easy to write, and that is the danger. Decide these on purpose.

- **Perfect lead is unfair lead.** An archer with an exact solver hits every target that moves in a straight line. Players experience that as cheating, because a human archer can't do it. Add an error you control. Use a reaction delay (the archer reads the target's velocity from 0.2 s ago, as CS203 suggested for pursuers), a random angular spread, or aim at the estimate instead of the exact root.
- **Straight-line prediction is wrong by design.** The model assumes the target keeps its velocity. A player who changes direction after you fire makes any lead wrong. Section 4 turns this into a number, the dodge budget, and that number is your real design knob.
- **Choose which cases get no answer.** When the shot is slower than a fleeing target the quadratic has no positive root. Your AI needs a fallback such as not firing, aiming at the body anyway, or moving closer. Returning `None` without handling it is a crash waiting for the first fast player.
- **Homing is a different game.** Homing projectiles remove aiming skill and make movement the only answer. Tab-target MMOs often want that, action combat rarely does. Pick one on purpose per skill.

### Check this example

1. A turret fires bolts at 30 m/s at a runner 24 m away moving straight across at 6 m/s. Compute the flight time and the lead angle.
2. Same turret, runner moving straight away at 6 m/s. Flight time? What lead angle?
3. A slime moves at 12 m/s toward a player whose slow spell travels at 10 m/s. The slime starts 20 m away, heading straight at the player. Can the spell hit? When?

<details>
<summary>Answers</summary>

1. `b = 0`, so `t = √(24² / (30² − 6²)) = √(576 / 864) = 0.816` s. Aim point `(24, 4.90)`, lead angle `atan(4.90 / 24) = 11.5°`.
2. `24 + 6t = 30t`, so `t = 1.0` s. Lead angle 0°, because the runner moves along the line of fire.
3. `a = 144 − 100 = 44`, `b = 2 × (20 × −12) = −480`, `c = 400`. Discriminant `230,400 − 70,400 = 160,000`, root 400. `t = (480 − 400) / 88 = 0.909` s or `(480 + 400) / 88 = 10` s. The spell hits at 0.909 s. A slower shot can hit a faster target that is coming toward you. The second root is not a real second chance, because by 10 s the slime has passed the player.

</details>

## 3. Gravity: two ways to hit a fixed point

Arrows, grenades and catapult stones fall. Start with a target that stands still at horizontal distance `x` and height `y` above the launch point. The shooter picks an elevation angle `θ`, and the launch velocity is `(s·cos θ, s·sin θ)`. Each axis moves on its own (week 6):

```
horizontal:  x = s·cos θ · t
vertical:    y = s·sin θ · t − ½·g·t²
```

Eliminate `t` from the first line, write `1 / cos²θ = 1 + tan²θ`, and you get a quadratic in `tan θ`. Its solution is the standard **launch angle formula**

```
tan θ = ( s² ± √( s⁴ − g·(g·x² + 2·y·s²) ) ) / (g·x)
```

- The minus sign gives the **low arc**, fast and flat.
- The plus sign gives the **high arc**, a lob that takes much longer.
- If the square root's argument is negative, the target is out of reach at this speed. On flat ground (`y = 0`) the maximum range is `s² / g`, reached at 45°.

Take an archer whose arrows leave at `s = 40` m/s under `g = 9.81` m/s², a real-world value your game is free to change.

| Target | Low arc | Flight time | High arc | Flight time |
|---|---|---|---|---|
| 60 m away, same height | 10.79° | 1.53 s | 79.21° | 8.01 s |
| 60 m away, 10 m higher | 20.64° | 1.60 s | 78.82° | 7.74 s |
| Maximum range on flat ground | 163.1 m at 45° | | | |

Check the first row. `s² = 1,600`, `s⁴ = 2,560,000`, `g²x² = 346,448`, so the root is `√2,213,552 = 1,487.8`. Then `tan θ = (1,600 − 1,487.8) / 588.6 = 0.1906`, giving 10.79°. Flight time is `60 / (40 × cos 10.79°) = 1.53` s.

The high arc spends 8 seconds in the air. Against a player who can walk 5 m/s, that is 40 m of movement, so a lob is useless against anything that moves. That is why mortar-style attacks in games are area denial rather than aimed shots. The telegraphed landing circle is honest about the flight time.

## 4. A moving target under gravity

Now combine sections 2 and 3. The projectile's position is `v·t + ½·g·t²` and the target's is `D + u·t`. Setting them equal and solving for the launch velocity gives

```
v = (D + u·t) / t − ½·g·t
```

Read it as two corrections to aiming at the target's body. Aim at where the target will be (the lead), then aim *above* that point by `½·|g|·t²`, the distance gravity will pull the shot down during its flight. The constraint is still `|v| = s`, and squaring it gives

```
|D + u·t − ½·g·t²|² = s²·t²
```

The `t²` inside the bracket makes this a **quartic** (degree 4) in `t`. Quartics have a closed-form solution, but it is long and numerically fragile. Games don't use it. They find the root numerically. The function `f(t) = |D + u·t − ½·g·t²| − s·t` starts positive at small `t` (the shot hasn't reached anything yet) and turns negative once the shot can outrun the gap. Scan forward for the first sign change, then **bisect** (halve the bracket until it is tiny). The first root is the low arc. A later sign change back, if there is one, is the high arc.

```python
import math

def ballistic_intercept(D, u, s, g=9.81, t_max=20.0, n=2000):
    """Earliest t with |D + u t - 0.5 g t^2 (up)| = s t. Returns (t, v) or None.
    D, u are (x, y, z) with y up. Scans for a sign change, then bisects."""
    def miss(t):
        px = D[0] + u[0] * t
        py = D[1] + u[1] * t + 0.5 * g * t * t     # aim above to cancel the drop
        pz = D[2] + u[2] * t
        return math.sqrt(px * px + py * py + pz * pz) - s * t
    prev_t, prev_f = 1e-6, miss(1e-6)
    for i in range(1, n + 1):
        t = t_max * i / n
        f = miss(t)
        if prev_f > 0 >= f:                        # the shot has caught up
            lo, hi = prev_t, t
            for _ in range(60):
                mid = (lo + hi) / 2
                lo, hi = (mid, hi) if miss(mid) > 0 else (lo, mid)
            t = hi
            v = ((D[0] + u[0] * t) / t, (D[1] + u[1] * t) / t + 0.5 * g * t,
                 (D[2] + u[2] * t) / t)
            return t, v
        prev_t, prev_f = t, f
    return None

s = 40.0                                           # arrow speed, m/s
for label, u in [("standing", (0, 0, 0)), ("running across", (0, 0, 5.0)),
                 ("running away", (5.0, 0, 0))]:
    t, v = ballistic_intercept((60.0, 0.0, 0.0), u, s)
    elev = math.degrees(math.atan2(v[1], math.hypot(v[0], v[2])))
    yaw = math.degrees(math.atan2(v[2], v[0]))
    print(f"{label:15} t = {t:.3f} s  elevation {elev:5.2f} deg  yaw {yaw:5.2f} deg")
```

Output:

```
standing        t = 1.527 s  elevation 10.79 deg  yaw  0.00 deg
running across  t = 1.540 s  elevation 10.89 deg  yaw  7.31 deg
running away    t = 1.762 s  elevation 12.48 deg  yaw  0.00 deg
```

The standing row matches section 3's low arc exactly, which is your first test that the solver is right. Running across needs 7.31° of sideways lead and a tiny bit more elevation, because the intercept point is slightly further away. Running away needs no sideways lead, but the arrow must fly 8.8 m further, so it climbs to 12.48°. The target's motion changes the elevation too, because elevation depends on distance.

With `g = 0` the `miss` function becomes section 2's `|D + u·t| − s·t`, and the scan finds the same root as the quadratic. Keep the quadratic for straight shots. It is exact, fast, and tells you when no answer exists. Keep the scan for arcs.

### Dodging is the design, and it has a budget

Every lead assumes the target keeps going straight. A target that sees the shot and changes course can be anywhere in a disc of radius `|u|·t_left` around where it was, where `t_left` is the time it has to react. Call the shot's **hit radius** `R` (projectile radius plus target radius, the distance at which the collision test from week 9 reports a hit). Then the rule is

```
the shot can be dodged by reaction if   |u| · (τ + t − t_react) > R
```

where `τ` is any cast delay the target can see, `t` the flight time and `t_react` the player's reaction time. The left side is the **dodge budget**, how far the target can move after noticing. As long as it exceeds the hit radius, a skilled player can always sidestep. Below it, the shot is a guaranteed hit once aimed well.

Take the Mystic Shot case from section 2, with a reaction time of 0.25 s. The target has `0.25 + 0.517 − 0.25 = 0.517` s to move, and at 345 units per second covers 178 units. Compare that with the hit radius you choose. A 120-unit radius leaves the dodge easy at this range. At 400 units range the flight time drops to 0.22 s, the budget falls to about 74 units, and the same bolt becomes nearly undodgeable. That is the whole feel of a skillshot, set by three numbers. As a designer you choose `s`, `τ` and `R` so the budget crosses `R` at the range you want. Past that range the shot is a read of the player's movement. Inside it the shot is a reflex check for the shooter.

## 5. What the models leave out

**Drag.** With week 8's per-tick drag the projectile slows during flight. There is no closed form for the flight time, but `f(t)` still works if you replace `s·t` with the distance a dragged projectile covers in time `t`. Precompute that as a table once per projectile type. Minecraft's thrown projectiles, for example, use per-tick gravity and drag factors listed in week 8's sources, so an exact aim for them is a table lookup plus a bisection.

**Integration error.** Your game doesn't move projectiles along the exact parabola. It steps them with week 7's integrator. Semi-implicit Euler at 60 Hz drops a projectile further than the exact `½·g·t²`, by about `½·g·t·dt` after flight time `t`. For our 1.53 s arrow that is `0.5 × 9.81 × 1.53 × (1/60) = 0.125` m low. That is small, but it is a systematic miss at every range, and it grows with flight time. Either aim with the same integrator you fly with (simulate the shot forward in the solver), or fly projectiles with the exact formula from launch time instead of stepping them.

**Acceleration of the target.** If the target is accelerating, `D + u·t + ½·a·t²` gives another quartic and the same scan solves it. In practice target acceleration measured from positions is noisy (week 6), and predicting it usually makes aim worse.

## In-class activity (25 minutes)

Groups of three. Each group gets one printed top-down grid with a tower at the origin and a target path, plus a projectile card (speed, cast delay, hit radius).

1. **Solve (8 min).** Compute the intercept time and aim point for the target at the moment shown, using the quadratic. Mark the aim point on the grid. One member checks with the interactive.
2. **Dodge budget (7 min).** With a reaction time of 0.25 s, compute the dodge budget at 5 m, 15 m and 30 m. Mark the range at which the budget equals the hit radius.
3. **Tune (10 min).** Your designer wants this tower to "reliably hit anyone standing still, and hit a running player about half the time at 20 m." Change exactly one of speed, cast delay or hit radius to get there, and justify it with your budget numbers.

Expected output: an annotated grid, a three-row budget table, and one sentence naming the parameter you changed and its new value.

## Common misconceptions

- **"Aiming at the body always misses a moving target."** Only the part of the motion across the line of fire needs a lead. A target running straight toward or away from you is hit by aiming at it, just later or sooner.
- **"If the shot is slower than the target, it can never hit."** A slow shot can still hit a faster target that is coming toward you (Check this example, question 3). The sign of `b` decides.
- **"The prediction `T = distance / speed` is the flight time."** It is the flight time to where the target is now. The true flight time differs by the target's motion along the line of fire, and one or two iterations or the quadratic fix it.
- **"Gravity only changes elevation, so solve the lead first, then add the drop."** The drop depends on the flight time, and the flight time depends on the aim. Solve both together, as in section 4.

## Check yourself

1. A wizard casts a bolt at 18 m/s with a 0.4 s cast time at a target 12 m away moving across at 4 m/s. Compute the shifted start `D'`, the flight time, and the total time from the start of the cast to the hit.
2. Show that when the target moves straight across (`D·u = 0`) and `s > |u|`, the flight time is `|D| / √(s² − |u|²)`.
3. An arrow at 40 m/s must hit a crow perched 30 m away horizontally and 30 m up. Is it reachable? If so, compute the low-arc angle.
4. A designer doubles projectile speed to "make the archer better." What happens to the dodge budget at 20 m, and to the lead angle against a runner crossing at right angles?
5. Your intercept solver returns `None` for a fleeing player on a horse. List two things the archer AI could do instead, and the effect of each on the player.

<details>
<summary>Answers</summary>

1. `D' = (12, 1.6)`. `a = 16 − 324 = −308`, `b = 2 × 1.6 × 4 = 12.8`, `c = 146.56`. The discriminant is `163.84 + 180,561.9 = 180,725.8`, root 425.1. The positive root is `(−12.8 − 425.1) / (−616) = 0.711` s. Total time from the start of the cast is `0.4 + 0.711 = 1.111` s.
2. With `b = 0`, `a·t² + c = 0`, so `t² = −c / a = |D|² / (s² − |u|²)`. Take the positive square root.
3. `s⁴ − g(g x² + 2 y s²) = 2,560,000 − 9.81 × (9.81 × 900 + 2 × 30 × 1,600) = 2,560,000 − 9.81 × 104,829 = 1,531,628`. That is positive, so it is reachable. The root is 1,237.6, and `tan θ = (1,600 − 1,237.6) / (9.81 × 30) = 1.231`, so `θ = 50.9°`.
4. The flight time halves, so the dodge budget `|u|(τ + t − t_react)` shrinks. If `τ` is small it may drop below zero, and the shot becomes undodgeable at that range. For a runner crossing at right angles, the lead angle is `atan(|u|·t / |D|) = atan(|u| / √(s² − |u|²))`, which roughly halves too.
5. Examples. Hold fire until the player turns or slows, which tells the player "outrun it and you're safe." Aim at the body anyway for a guaranteed miss that still looks like an attack. Switch to a faster attack or a homing one, which removes the counterplay. Each choice should be deliberate.

</details>

## Lab / assignment hook

[Lab 13, the archer's aim](../labs/lab13.md). Implement the intercept quadratic with its edge cases, the launch angle formula and the ballistic intercept scan in Python, pass the tests, and then run a seeded duel simulation in which a target jinks at random. Measure the hit rate of body aim, the one-step estimate and the exact solve against projectile speed, and use the dodge budget to tune an archer to a hit rate the designer asks for.

## Sources

- Team Fortress Wiki, "Projectiles" (current, page as of September 2026). Rocket Launcher rockets at 1,100 Hammer units per second; Huntsman arrows 1,800 to 2,600 per second and affected by gravity. https://wiki.teamfortress.com/wiki/Projectiles
- Team Fortress Wiki, template "Metrics/Base speed", used on the "Classes" page (current). Base speeds in Hammer units per second: Scout 400, Soldier 240, Heavy 230. https://wiki.teamfortress.com/wiki/Classes
- League of Legends Wiki, "Ezreal", ability data for Mystic Shot (current patches, September 2026). Target range 1,200, speed 2,000, width 120, cast time 0.25 s. https://wiki.leagueoflegends.com/en-us/Ezreal
- League of Legends Wiki, "Movement speed" and "List of champions/Movement speed" (current patches). Base movement speeds from 325 to 355. https://wiki.leagueoflegends.com/en-us/Movement_speed
- Guild Wars 2 Wiki, "Projectile" (current). Projectiles must travel before dealing damage; most can be dodged, blocked or reflected; a few auto-track the target; projectiles travel further when fired from a height. https://wiki.guildwars2.com/wiki/Projectile
- Bernier, Y. (2001). "Latency Compensating Methods in Client/Server In-game Protocol Design and Optimization." Game Developers Conference 2001. Projectiles in Half-Life were not lag compensated. Cited through CS202 week 11.
- Reynolds, C. (1999). "Steering Behaviors for Autonomous Characters." Game Developers Conference 1999. Pursuit's prediction interval proportional to distance. Cited through CS203 week 2.
- Millington, I. (2010). *Game Physics Engine Development* (2nd ed.). Morgan Kaufmann. Chapter 3, ballistic projectiles.

## Interactive spec: examples/w13-lead-the-target.html

**The one insight the visual must make obvious:** the intercept is the first moment the shot's growing reach circle `|p| = s·t` touches the moving target, which is the zero of `g(t) = |D + u·t| − s·t`. Aiming at the body misses by the target's sideways motion, the one-step estimate nearly hits, and the exact root always hits while `s > |u|`.

**Layout.** Two linked views side by side at 1280 px, stacked at 390 px (top-down first).

- **Left, top-down world.** Units are metres. Shooter at the origin, drawn as a small circle. Target drawn as a circle of radius `R` (hit radius, default 0.5 m) at `D + u·t`, with its path as a dashed line and an arrow for `u`. A faint circle of radius `s·t` centred on the shooter shows the shot's reach at the current scrub time. Three shots are drawn as small dots moving along straight lines. Grey is aimed at the body, amber at the one-step estimate (aim at `D + u·T₁` with `T₁ = |D| / s`), and the program's accent colour at the exact intercept. Mark the exact intercept point with a cross and the estimate's aim point with a hollow cross. After a shot reaches its aim point (or at the closest approach, if it misses), draw its miss distance as a label.
- **Right, the gap function.** Plot `g(t) = |D + u·t| − s·t` for `t` from 0 to `max(2 × t*, 3)` s, where `t*` is the exact root (or 3 s if there is none). Draw the zero line, mark `t*` with a filled dot, mark `T₁` with a hollow dot, and draw a vertical cursor at the current scrub time that moves with the left view.

**Controls** (all keyboard accessible, each with a visible numeric value):

- Distance `|D|`: 5 to 60 m, default 30. `D` points along +x.
- Target speed `|u|`: 0 to 30 m/s, default 6.
- Target heading: 0° to 359°, default 90° (straight across). 0° means moving away along +x.
- Shot speed `s`: 5 to 60 m/s, default 25.
- Cast delay `τ`: 0 to 1 s, default 0. With `τ > 0`, the solver uses `D' = D + u·τ` and the shot leaves at `t = τ`. Show both `D` and `D'`.
- Time scrubber `t` from 0 to the plot's right edge, plus a Play/Pause button that animates it in real time (disabled under `prefers-reduced-motion`, where the scrubber still works).
- Preset buttons: "TF2 Scout" (scale the view to Hammer units: `|D| = 1000`, `|u| = 400`, heading 90°, `s = 1100`, `R = 50`), "Mystic Shot" (`|D| = 1000`, `|u| = 345`, heading 90°, `s = 2000`, `τ = 0.25`, `R = 120`, units), "Fleeing and faster" (`|D| = 20`, `|u| = 12`, heading 0°, `s = 10`).

**Readouts** next to the views: `a`, `b`, `c`, discriminant, both roots, chosen `t*`, aim point, lead angle `atan2`, the one-step estimate `T₁` and its miss distance, the body-aim miss (closest approach), and the dodge budget `|u|·(τ + t* − 0.25)` compared with `R` as "dodgeable" or "not dodgeable at this range". When no positive root exists, show "no intercept" in place of `t*` and grey the exact shot.

**Formulas.** `a = u·u − s²`, `b = 2(D'·u)`, `c = D'·D'`. If `|a| < 1e-9`, `t = −c / b` when `b < 0`, else none. Otherwise take the smallest positive root of the quadratic. Body-aim miss: the shot's velocity is `s·D'/|D'|`, and the miss is the minimum over `t ≥ 0` of `|D' + (u − v)·t|`.

**Test values** (must match to the shown digits, with `τ = 0`):

| `|D|` | `|u|` | Heading | `s` | `t*` | Aim point | Lead angle | One-step miss | Body-aim miss |
|---|---|---|---|---|---|---|---|---|
| 1000 | 400 | 90° | 1100 | 0.9759 s | (1000.0, 390.4) | 21.3° | 23.3 | 341.7 |
| 1000 | 400 | 180° | 1100 | 0.6667 s | (733.3, 0.0) | 0.0° | 0.0 | 0.0 |
| 1000 | 400 | 0° | 1100 | 1.4286 s | (1571.4, 0.0) | 0.0° | 0.0 | 0.0 |
| 1000 | 230 | 90° | 1100 | 0.9296 s | (1000.0, 213.8) | 12.1° | 4.5 | 204.7 |
| 20 | 12 | 180° | 10 | 0.9091 s | (9.09, 0.0) | 0.0° | 0.0 (at 10.0 s) | 0.0 |
| 20 | 12 | 0° | 10 | none | — | — | 20.0 (at 0 s) | 20.0 (at 0 s) |

With the Mystic Shot preset (`τ = 0.25`): `D' = (1000, 86.25)`, `t* = 0.5172` s after release, aim point `(1000.0, 264.7)`, intercept distance 1034.4.

"One-step miss" and "body-aim miss" are both closest approaches, computed the same way: fire at speed `s` toward the aim point (`D' + u·T₁` for the one-step shot, `D'` for body aim) and take the minimum over flight time `t ≥ 0` of the distance between shot and target centres, `|D' + (u − v)·t|`. For the crossing rows this equals the lecture's `400 × (actual − assumed)` column to the digits shown (23.3). For headings 0° and 180° it is 0, because the shot flies along the target's path and meets it on the way; the section 2 formula `|u| × |t(T₁) − T₁|` would give 132.2 there, so do not use it. In the slime row the one-step shot is aimed at `D + u·T₁ = (−4, 0)`, behind the shooter, and meets the slime only at 10.0 s, long after it has passed. In the fleeing row nothing is ever closer than at release, so both misses are 20.0 at 0 s. Show the time of closest approach next to each miss.

**Style.** Use the shared tokens from `templates/interactive-tokens.css`, inline. No game art. Draw shooter and target as plain shapes and name the games only in the preset labels.

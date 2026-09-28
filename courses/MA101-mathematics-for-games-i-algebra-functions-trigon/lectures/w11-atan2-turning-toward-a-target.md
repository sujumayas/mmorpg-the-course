# MA101 · Week 11 — atan2 and Turning Toward a Target

**Why this matters:** Every enemy that looks at you, every turret that tracks you and every homing missile that chases you has to answer one question each frame: which way is the target, and how far do I have to turn? Get the answer slightly wrong and your turret spins the long way round or your missile circles its target forever.

**You will be able to:**
- Compute the angle from one point to another with `atan2`, and explain why `atan(y/x)` gives wrong answers in half the plane.
- Compute the shortest signed difference between two angles, handling the wrap at ±180°.
- Implement turning at a capped rate and compute how long a turn takes, using Dota 2's turn-rate rule as the test case.
- Compute a homing missile's turning radius and predict when it will orbit instead of hit.

**Before class:** Dunn & Parberry, *3D Math Primer for Graphics and Game Development* (2nd ed., 2011), chapter 1 trigonometry review, the part on inverse trigonometric functions. Re-read MA101 week 10 sections 2 and 3 (radians and the unit circle).

**Prerequisites from earlier courses:** [MA101 week 10, angles, radians, sin and cos](w10-angles-radians-sin-cos.md). [MA101 week 7, piecewise functions, caps and floors](w07-piecewise-caps-and-floors.md) and [MA101 week 8, lerp, inverse lerp and remap](w08-interpolation-lerp-inverse-lerp-remap.md).

**Interactive:** [examples/w11-turn-toward-target.html](../examples/w11-turn-toward-target.html). Keep it open during sections 4 and 5.

---

## 1. The reverse question

Last week you went from an angle to a point: given `θ`, the point on the unit circle is `(cos θ, sin θ)`. This week you go the other way. You have two points, a turret at `(tx, ty)` and a player at `(px, py)`, and you want the angle the turret should face.

Step one is always the same. Subtract to get the **displacement**, the arrow from the turret to the player:

```
dx = px − tx
dy = py − ty
```

Order matters. Target minus self gives the arrow pointing *from* self *to* the target. Self minus target points the other way, and your turret will face directly away from the player. If you ever see an enemy that walks backwards away from you in a perfectly straight line, check this subtraction first.

Step two is to turn that arrow into an angle. The arrow `(dx, dy)` points in some direction, and the angle `θ` of that direction satisfies `dx = d cos θ` and `dy = d sin θ`, where `d` is the arrow's length. Divide the second by the first and the length cancels:

```
tan θ = dy / dx
```

So it looks like `θ = atan(dy / dx)` is the answer. It is not, and the reason is worth five minutes.

## 2. Why atan(y/x) fails, and what atan2 does instead

### Half the plane goes missing

Put the turret at the origin and the player at `(−300, 100)`, up and to the left. The true direction is about 161.6°, a little above straight left.

Now compute `atan(100 / −300) = atan(−0.333) = −18.4°`. That is down and to the right, almost exactly the opposite direction. The turret shoots away from the player.

The problem is the division. `100 / −300` and `−100 / 300` are both `−0.333`, so `atan` cannot tell "up-left" from "down-right". Dividing throws away the signs of `dx` and `dy` separately and keeps only whether they match. `atan` returns angles only between −90° and 90°, the right half of the circle, so every target on the left half gets reflected through the origin.

Two more failures come for free.

- If `dx = 0` (the target is straight above or below), `dy / dx` divides by zero.
- If the target sits exactly on top of the turret, both are zero and no direction exists at all.

### atan2 keeps both signs

The function `atan2(y, x)` takes the two components separately instead of their ratio. Because it sees both signs, it knows which quadrant the arrow is in and returns the full angle, in the range from −π to π radians (−180° to 180°). It also handles `x = 0` correctly.

| Target offset (dx, dy) | atan(dy/dx) | atan2(dy, dx) | Correct? |
|---|---|---|---|
| (300, 0) | 0.0° | 0.0° | both |
| (200, 200) | 45.0° | 45.0° | both |
| (0, 300) | divide by zero | 90.0° | atan2 only |
| (−300, 100) | −18.4° | 161.6° | atan2 only |
| (−300, 0) | 0.0° | 180.0° | atan2 only |
| (100, −300) | −71.6° | −71.6° | both |
| (−200, −200) | 45.0° | −135.0° | atan2 only |

Notice the last row. `atan` says 45°, the same as for `(200, 200)`, because both components flipped sign and the ratio stayed at 1. The target is directly behind the first one.

### Argument order and conventions

The argument order is `atan2(y, x)`, y first. This matches the mathematical definition, and it trips up almost everyone at least once because every other function you write takes x first. Unity's `Mathf.Atan2(y, x)` and Godot's global `atan2(y, x)` both put y first, and both return radians in the range −π to π. Excel's `ATAN2` takes x first, which is a good reason to label your spreadsheet columns clearly.

Two conventions from last week still apply:

- In a y-down screen space, a positive `atan2` result is clockwise on screen. The math is unchanged.
- If your sprite's artwork faces up instead of right, the angle that points the sprite at the target is `atan2(dy, dx) + π/2` or `− π/2`, depending on your y direction. Decide once, test with a target straight to the right, and write the offset down.

Finally, guard the zero case. If `dx` and `dy` are both zero, most libraries return 0, which means "face right". That is harmless for a turret but can make a homing missile that reaches its target spin to face east for one frame. Check the distance first and skip the update when it is tiny.

## 3. How far to turn: angle differences and the wrap

### The long way round

Knowing where the target is does not tell you how to get there. A turret faces 170° and the target is at −170°. The subtraction `target − current = −340°` tells the turret to swing 340° clockwise. But −170° is the same direction as 190°, only 20° further counterclockwise. Any player watching a turret take the 340° route will call it a bug, and they will be right.

The reason is that angles wrap. 170° and −190° are the same direction, and so are 190° and −170°. A difference of −340° and a difference of +20° describe the same final facing. We want the one with the smallest size.

### The shortest signed difference

The rule: take the raw difference and wrap it into the range (−180°, 180°].

```
raw   = target − current
delta = raw − 360 × round(raw / 360)          (degrees)
delta = raw − 2π × round(raw / 2π)            (radians)
```

Or with a floor-based modulo:

```
delta = ((raw + 180) mod 360) − 180
```

Be careful with that second version in C, C#, C++, Java and JavaScript. Their `%` operator keeps the sign of the left-hand side, so `−340 % 360` is `−340`, not `20`. Python's `%` floors, so it works there. The first version with `round` avoids the problem in every language.

| Current | Target | Raw difference | Shortest delta |
|---|---|---|---|
| 170° | −170° | −340° | +20° |
| −170° | 170° | +340° | −20° |
| 10° | 350° | +340° | −20° |
| 90° | −90° | −180° | ±180° (tie) |
| 45° | 135° | +90° | +90° |

The tie row matters. When the target is exactly behind you, both directions are equally short. Your code picks one, and it must pick consistently or a unit facing exactly away from its target will jitter between the two. Unity's `Mathf.DeltaAngle` returns values from just above −180 up to and including 180, so a tie resolves to +180. Godot's `angle_difference` does the same job in radians.

The sign of `delta` tells you which way to turn: positive means increase the angle, negative means decrease it. The size tells you how far.

## 4. Worked example: Dota 2's turn rate

### The hook

In Dota 2, a hero cannot act in a direction until it is facing close to it. Order a hero to walk away from an enemy and it first has to turn around, and that turn takes real time. The community wiki measures the difference between a quick-turning hero and a slow one in hundredths of a second. In a fight, those hundredths decide whether you escape or get stunned.

The surprising detail is the unit. Dota 2 does not express turn rate in degrees per second. It uses **radians per 0.03 seconds**. Most heroes sit between 0.5 and 0.6. What does 0.5 mean in a unit you can feel, and how long does a hero spend turning around?

### The model

Three pieces, each from an earlier section.

1. **Where is the target?** `goal = atan2(dy, dx)`.
2. **How far must I turn?** `delta = wrap(goal − facing)`, the shortest signed difference.
3. **How fast can I turn?** Each tick, change `facing` by at most `ω × dt` toward the goal:

```
step   = clamp(delta, −ω × dt, +ω × dt)
facing = facing + step
```

`ω` is the turn rate in radians per second. The clamp is the piecewise function from MA101 week 7: turn the full remaining amount if it is small, otherwise turn the maximum allowed.

Dota 2 adds one rule. The wiki reports that a unit starts moving, or casting at a point, once the target direction is within 11.5° of its facing. So the hero does not need to finish the turn, only to get within 11.5° (0.2007 radians).

Putting it together, the time before a hero can act after being ordered toward a direction `|delta|` away is:

```
ω (rad/s)   = turn_rate / 0.03
time to act = (|delta| − 0.2007) / ω      if |delta| > 0.2007, else 0
            = 0.03 × (|delta| − 0.2007) / turn_rate
```

This treats the turn as continuous. The wiki's own formula for a 180° turn, `0.03π / turn_rate`, does the same.

### Numbers you can check

First convert the unit. A turn rate of 0.5 radians per 0.03 s is `0.5 / 0.03 = 16.7` radians per second, which is about 955° per second. A full 180° turn therefore takes `π / 16.7 = 0.188` seconds, matching the wiki's "between 0.15 and 0.19 seconds" for the common range.

| Turn rate | ω (rad/s) | ω (deg/s) | Full 180° turn | Time to act on a 180° order (within 11.5°) |
|---|---|---|---|---|
| 0.5 | 16.7 | 955 | 0.188 s | 0.176 s |
| 0.6 | 20.0 | 1,146 | 0.157 s | 0.147 s |
| 1.0 | 33.3 | 1,910 | 0.094 s | 0.088 s |

Now a concrete scene. A hero stands at the origin facing east (0°). Enemies appear at different offsets. For each, compute `atan2`, then the time before the hero can act toward it.

| Target offset | atan2 angle | Time to act, turn rate 0.5 | Time to act, turn rate 0.6 |
|---|---|---|---|
| (300, 0) | 0.0° | 0.000 s | 0.000 s |
| (200, 200) | 45.0° | 0.035 s | 0.029 s |
| (0, 300) | 90.0° | 0.082 s | 0.069 s |
| (100, −300) | −71.6° | 0.063 s | 0.052 s |
| (−200, −200) | −135.0° | 0.129 s | 0.108 s |
| (−300, 100) | 161.6° | 0.157 s | 0.131 s |

Check the (0, 300) row by hand. The angle is 90°, which is `π/2 = 1.5708` rad. Subtract the 0.2007 leeway to get 1.3701 rad. Multiply by 0.03 and divide by 0.5 to get 0.0822 s.

The difference between turn rate 0.5 and 0.6 on a full turnaround is about 0.03 seconds. That sounds like nothing, but it is one whole 0.03 s turn step of extra delay every time a slow hero reverses direction. The table also shows why a hero caught from behind loses more than one caught from the side. The cost grows linearly with the angle.

### Move it yourself

Open [`examples/w11-turn-toward-target.html`](../examples/w11-turn-toward-target.html). The top-down view shows a unit at the center with a facing arrow and a draggable target. A shaded wedge shows the 11.5° "can act" cone around the facing arrow.

Drag the target in a circle around the unit. The readouts show `atan(dy/dx)` and `atan2(dy, dx)` side by side. On the right half they agree. Cross into the left half and the `atan` readout jumps to the mirror direction; a ghost arrow shows where a turret using it would aim.

Now click "Order" to make the unit turn toward the target at the chosen turn rate. A timer shows the seconds until the target enters the wedge. Switch the difference mode from "shortest (wrapped)" to "naive (raw)" and put the target just across the ±180° line behind the unit. The naive unit swings the long way round, and the timer shows how much longer it takes.

### Cross-game recognition

**Doom (1993), monsters.** id Software's released source shows that ordinary Doom monsters do not turn at a rate at all. The function `A_FaceTarget` sets the monster's angle straight to the value returned by `R_PointToAngle2`, Doom's own version of `atan2` built from a lookup table of arctangents. The turn is instant, so it is our model with `ω = ∞`. The code then adds a random offset of up to about 45° either way if the player is partly invisible, which is how the invisibility power-up makes monsters miss. It works on the angle, not the position, because the angle is the thing the monster aims with.

**Doom (1993), homing missiles.** The Revenant's homing missile, in the function `A_Tracer`, is the rate-limited version. It computes the exact angle to its target with `R_PointToAngle2`, then turns toward it by a fixed step of `0xC000000` angle units, which is 16.875°, snapping to the exact angle if the step would overshoot. It decides which way to turn by subtracting the two angles as unsigned 32-bit integers and checking whether the result is more than half a turn (`0x80000000`). Because Doom's angles wrap at 2³², that single comparison is the shortest-signed-difference test from section 3, done with integer overflow instead of `round`. The adjustment runs only on game tics that are multiples of 4, at 35 tics per second, so a homing missile turns about 148° per second.

**Unity and Godot.** Both engines ship the model as library functions. Unity's `Mathf.DeltaAngle` gives the shortest difference in degrees and `Mathf.MoveTowardsAngle` turns by at most a given step, wrapping correctly. Godot's `angle_difference` and `rotate_toward` are the radian versions. Read their documentation after this lecture and you should recognize every line: wrap, clamp, add.

Three different presentations, one algorithm: `atan2` to find the goal, wrap to find the short way, clamp to respect the turn rate.

### Eyes-open design judgment

A turn rate is a design lever. Treat it as a stat, not an animation detail.

- **Instant turning (Doom's monsters) is readable and fair to the attacker.** Enemies always face you, and the only way to dodge is to move. It makes flanking worthless.
- **Rate-limited turning rewards position.** In Dota 2 a slow-turning hero is punished for changing its mind, and getting behind an enemy has a measurable value in seconds. That is depth, but players only feel it if the turn is visible. A 0.03 s difference is invisible on its own. It matters because it stacks across a fight.
- **The action cone is a second lever.** Dota 2's 11.5° leeway shaves time off every turn. A wider cone makes turn rate matter less. A zero cone makes the last few degrees, where the unit is already almost facing, cost time for nothing a player can see.
- **Match the unit to the designer.** Radians per 0.03 s is a fine engine unit and a poor tuning unit. Show designers degrees per second, or better "seconds to turn around", and convert in code.

## 5. Homing missiles and the turning circle

A missile that flies at speed `v` and turns at most `ω` radians per second cannot turn more tightly than a circle of radius:

```
R = v / ω
```

This comes straight from last week's orbit model: a point moving around a circle of radius `R` at angular speed `ω` has linear speed `ωR`. Set that equal to `v` and solve for `R`.

The consequence is the classic homing-missile bug. If the target is inside one of the two circles of radius `R` that touch the missile's path on its left and right, the missile cannot reach it by turning. It turns as hard as it can, overshoots, and circles. If the target stays still, the missile orbits it until its lifetime runs out.

| Speed v | Turn rate ω | Turning radius R |
|---|---|---|
| 350 units/s | 2.58 rad/s (147.7°/s) | 135.8 units |
| 400 px/s | π rad/s (180°/s) | 127.3 px |
| 400 px/s | 2π rad/s (360°/s) | 63.7 px |
| 600 px/s | π rad/s (180°/s) | 191.0 px |

The first row uses the Doom Revenant missile's numbers from the source: speed 10 map units per tic at 35 tics per second is 350 units per second, and 16.875° every 4 tics is 147.7° per second. Its turning circle has a radius of about 136 map units, more than eight times the player's 16-unit collision radius. That is one reason a player who sidesteps late can make it swing past.

Fixes, each with a cost:

- **Raise `ω` as the missile gets close.** The circle shrinks and the missile connects, but it can look like it bends unnaturally.
- **Lower `v` when turning hard.** Real aircraft do this. The missile feels heavier and more readable.
- **Give it a lifetime or a maximum turn total.** Orbiting stops, but the missile may simply fizzle next to the target.
- **Aim at a predicted point, not the current one.** That is interception, which you meet in CS203 (see the [CS203 syllabus](../../CS203-artificial-intelligence-for-games/syllabus.md)).

## 6. Smooth turning versus capped turning

The clamp model turns at a constant rate and stops dead. Some games want a turn that starts fast and eases into the target instead. The common trick is to cover a fixed *fraction* of the remaining difference each frame:

```
facing = facing + delta × (1 − e^(−k × dt))
```

`k` is a sharpness constant. With `k = 10`, the facing covers about 63% of the remaining angle in the first 0.1 s. This is the exponential approach you met with lerp in MA101 week 8, applied to an angle. Using `e^(−k dt)` instead of a plain fraction like 0.1 makes it independent of frame rate.

Two rules keep it correct.

1. **Always lerp the wrapped delta, never the raw angles.** Lerping from 170° to −170° with raw numbers passes through 0° and spins the long way. Godot's `lerp_angle` exists for exactly this reason.
2. **Know that it never quite arrives.** An exponential approach gets closer forever. If a game rule depends on "facing the target", use a tolerance cone like Dota 2's, or switch to a clamp when the remainder is small.

Which feels better is a design call. Constant-rate turning reads as mechanical: tanks, turrets, heavy units. Exponential turning reads as organic: cameras, creatures, a character's head tracking you. A lot of good-feeling games use both, clamped for the body and eased for the head.

## In-class activity (25 minutes)

Pairs, with a spreadsheet or a calculator.

1. **Tabulate (8 min).** A turret at (400, 300) in a y-down screen faces 0 radians (right). Compute `atan2` angles, in degrees, to targets at (600, 300), (400, 100), (200, 320) and (380, 500). For each, say where it is on the screen in words, and check that your words match the y-down convention.
2. **Turn times (7 min).** The turret turns at 120° per second and fires once the target is within 5°. For each target, compute the shortest delta and the time until it can fire.
3. **Break it (5 min).** Replace the shortest delta with the raw difference. Which targets now take longer, and by how much? Start the turret at 170° and repeat for the target at (200, 320).
4. **Missile (5 min).** Your turret fires missiles at 500 px/s. Choose a turn rate so that a missile fired straight right can still hit a target 150 px directly below the turret after first flying past it. Justify with `R = v/ω`.

Expected output: a table with four rows (angle, delta, time), a sentence on the naive bug, and a turn rate with the radius it gives.

## Common misconceptions

- **"`atan(dy/dx)` gives the direction to the target."** It gives the right answer only when the target is to the right (`dx > 0`). On the left half it returns the mirror image, and at `dx = 0` it divides by zero. Use `atan2(dy, dx)`.
- **"`atan2` takes x first."** In Unity, Godot, C, JavaScript and Python it takes y first. Excel is the common exception.
- **"To turn toward a target, subtract the angles."** The raw difference can be up to 360°. Wrap it into (−180°, 180°] first or your unit will sometimes turn the long way.
- **"A homing missile will always hit a stationary target eventually."** Not if the target is inside its turning circle `R = v/ω`. It will circle.

## Check yourself

1. A turret at (100, 100) aims at a player at (40, 180) in a math-convention (y-up) world. What angle does `atan2` return, in degrees? What would `atan(dy/dx)` return?
2. A unit faces −150°. Its target is at 120°. What is the shortest signed turn, and which way is it?
3. A hero has a Dota 2 turn rate of 0.7. How long does it take to act on a target directly behind it? Give the answer in seconds and compare it with turn rate 0.5.
4. A missile flies at 450 px/s. A designer wants it to be able to turn inside a circle of radius 100 px. What minimum turn rate is needed, in degrees per second?
5. Doom's Revenant missile turns 16.875° per adjustment. What is that in Doom's integer angle units, as a fraction of `0x80000000` (half a turn)?

<details>
<summary>Answers</summary>

1. `dx = −60`, `dy = 80`. `atan2(80, −60) = 126.9°` (up and to the left). `atan(80 / −60) = atan(−1.333) = −53.1°`, which points down and to the right, the exact opposite.
2. Raw `120 − (−150) = 270°`. Wrapped: `270 − 360 = −90°`. Turn 90° in the negative direction (clockwise in math convention).
3. Target behind means `|delta| = π`. Time `= 0.03 × (π − 0.2007) / 0.7 = 0.126 s`. At turn rate 0.5 it is 0.176 s, so the faster hero acts 0.05 s sooner.
4. `ω = v / R = 450 / 100 = 4.5 rad/s`, which is `4.5 × 180/π = 257.8°/s`.
5. 16.875° is 16.875/180 of half a turn, which is 0.09375, that is 3/32. `0x80000000 × 3/32 = 0xC000000`, the value in the source.

</details>

## Lab hook

**Lab 11: Turrets that turn.** You build a turret with a capped turn rate and a homing missile, measure turn times against the formula from section 4, and find the missile's orbit condition experimentally. The brief is in [Lab 11](../labs/lab11.md).

## Sources

- Dota 2 Wiki (Fandom), "Turn rate", accessed September 2026. Turn rate in radians per 0.03 seconds; the 180° time formula `0.03π / turn rate`; most heroes between 0.5 and 0.6 (0.15 to 0.19 s for 180°); units move or cast once the target is within 11.5°. Rules as described for the current patch at time of access. Individual hero values change across patches and are not used here.
- Liquipedia Dota 2 Wiki, "Turn Rate", retrieved September 2026. Confirms the unit (radians per 0.03 s), `t = 0.03π / T`, most heroes between 0.5 and 0.6 (0.15 to 0.19 s for 180°), and the 11.5° facing rule, which it sources to Valve's Dota 2 blog post "Various Pathfinding Fixes" (March 2015). It also notes that a turn ramps up to full rate, so the formula gives the maximum rate, not an exact frame count.
- id Software, DOOM source code (linuxdoom-1.10, released 1997), github.com/id-Software/DOOM. `p_enemy.c`: `A_FaceTarget` (instant facing via `R_PointToAngle2`, random offset for shadowed targets), `A_Tracer` (`TRACEANGLE = 0xc000000`, unsigned half-turn comparison, runs when `gametic & 3` is 0). `info.c`: `MT_TRACER` speed `10*FRACUNIT`, tracer states lasting 2 tics, `MT_PLAYER` radius `16*FRACUNIT`. `p_inter.c`: the partial invisibility power-up sets `MF_SHADOW` on the player. `doomdef.h`: `TICRATE 35`. `tables.h`: angle constants. `r_main.c`: `R_PointToAngle`.
- Unity Technologies, Scripting API, `Mathf.Atan2` (y first, radians, range −π to π), `Mathf.DeltaAngle` (shortest difference in degrees), `Mathf.MoveTowardsAngle`. Unity 6 documentation, accessed September 2026.
- Godot Engine documentation, `@GlobalScope`: `atan2(y, x)`, `angle_difference`, `rotate_toward`, `lerp_angle`. Godot 4.x stable docs, accessed September 2026.
- Microsoft Support, "ATAN2 function" (Excel), argument order `ATAN2(x_num, y_num)`, accessed September 2026.
- Dunn, F. & Parberry, I. (2011). *3D Math Primer for Graphics and Game Development* (2nd ed.). CRC Press. Chapter 1.

## Interactive spec: examples/w11-turn-toward-target.html

**The one insight:** `atan2` finds the right direction everywhere while `atan(dy/dx)` mirrors the whole left half, and turning must use the wrapped shortest difference, or a unit near the ±180° line turns the long way.

**Layout.** One main top-down canvas (y-up math convention, labeled) plus a readout panel beside it on desktop and below it on mobile. A mode switch at the top chooses "Turret" or "Homing missile".

**Turret mode.**

- Unit at the center, drawn as a circle with a facing arrow. A shaded wedge of ±11.5° around the facing (width adjustable).
- A draggable target (mouse, touch, and arrow keys to nudge by 10 units when focused).
- A solid line to the target at the `atan2` angle. A dashed ghost arrow at the `atan(dy/dx)` angle, drawn in a warning color whenever it differs from `atan2` by more than 0.5°.
- An arc showing the planned turn: from facing to goal, drawn along the shortest delta in "wrapped" mode or along the raw difference in "naive" mode.
- Controls: turn rate as Dota-style "radians per 0.03 s" slider 0.2 to 1.2, step 0.05, default 0.5 (show converted rad/s and deg/s next to it); cone half-width slider 0° to 30°, default 11.5°; difference mode toggle "shortest (wrapped)" / "naive (raw)"; "Order" button that animates the turn at `ω = rate/0.03` rad/s and stops a timer when `|delta| ≤ cone`; "Reset facing" with a numeric facing input in degrees, default 0.
- Readouts: `dx, dy`; `atan(dy/dx)` in degrees (or "undefined" when `dx = 0`); `atan2(dy, dx)` in degrees and radians; raw difference; wrapped delta; predicted time to act `0.03 × max(0, |delta| − cone_rad) / rate`; measured time from the animation.

**Homing missile mode.**

- A missile starts at the left edge moving right at speed `v`, turning toward a stationary draggable target with `step = clamp(delta, −ω dt, ω dt)`, `dt = 1/60`.
- Controls: `v` 100 to 800 px/s, default 400; `ω` 30 to 720 °/s, default 180; lifetime 2 to 10 s, default 6.
- Draw the two turning circles of radius `R = v/ω` tangent to the missile's current heading. Shade them. Draw the missile's trail.
- Readouts: `R`, whether the target is currently inside either circle, and hit/orbit result.

**Test values.**

- Target (−300, 100): `atan` −18.4°, `atan2` 161.6°. Target (−200, −200): `atan` 45.0°, `atan2` −135.0°. Target (0, 300): `atan` undefined, `atan2` 90.0°.
- Facing 0°, target (−300, 100), rate 0.5, cone 11.5°: predicted 0.157 s; rate 0.6: 0.131 s.
- Facing 170°, target direction −170°: wrapped delta +20.0°, raw −340.0°.
- Full turn (target directly behind), rate 0.5, cone 0°: 0.188 s. Cone 11.5°: 0.176 s.
- Missile `v = 400`, `ω = 180°/s`: `R = 127.3`. `v = 350`, `ω = 147.65625°/s`: `R = 135.8`.

**Accessibility.** All numbers as live text. Target draggable by keyboard. `prefers-reduced-motion`: turns and missile flights jump to the end state and show the computed times. Palette from `templates/interactive-tokens.css`; ghost arrow uses dash pattern as well as color.

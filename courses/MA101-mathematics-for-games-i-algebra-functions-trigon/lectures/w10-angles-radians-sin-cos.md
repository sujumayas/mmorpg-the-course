# MA101 · Week 10 — Angles, radians, sin and cos: orbiting and aiming

**Why this matters:** Every turret that aims, every shield that circles the player and every bullet fired at an angle runs on two functions, `sin` and `cos`. If you know what they return and what unit they expect, you can build all of those in a few lines and debug them in seconds when they go wrong.

**You will be able to:**
- Convert between degrees and radians and explain why engines use radians.
- Compute the position of a point orbiting a center at radius `r`, angular speed `ω` and phase offset, by hand and in code.
- Place `N` objects evenly on a circle and compute the gap between them.
- Turn an aim angle and a speed into a velocity vector, and design a radial bullet burst.

**Before class:** Dunn & Parberry, *3D Math Primer for Graphics and Game Development* (2nd ed., 2011), chapter 1, sections on angles and trigonometry (the "Math Review" material at the end of chapter 1). Freya Holmér, *Math for Game Devs*, part 1, the segment on the unit circle and trigonometry.

**Prerequisites from earlier courses:** [MA101 week 1, functions as machines](w01-functions-as-machines.md) and [MA101 week 8, lerp, inverse lerp and remap](w08-interpolation-lerp-inverse-lerp-remap.md). No earlier course is required.

**Interactive:** [examples/w10-orbit-and-waves.html](../examples/w10-orbit-and-waves.html). Keep it open during section 4.

---

## 1. Three jobs, one circle

Look at almost any action game and you will find three jobs that involve angles.

1. **Facing.** A character, a turret or a camera points somewhere. That direction is stored as an angle.
2. **Circling.** Something moves around a center point. Shields, orbiting familiars, a planet in a space sim, a spinning saw blade.
3. **Aiming.** Something leaves a point at an angle and travels in a straight line. Bullets, arrows, thrown grenades seen from above.

All three rest on the same picture: a circle with its center at the origin, a radius drawn out from it, and the angle that radius makes with the positive x-axis. This week you learn to read that picture in both directions. Given an angle, where is the point on the circle? That is `cos` and `sin`, and it is the subject of this lecture. Given a point, what is the angle? That is `atan2`, and it is next week.

Before the math, one habit. When you see an angle in game code, ask two questions right away. What unit is it in? Which way is positive? Most angle bugs in student projects come from getting one of these wrong, and neither one produces an error message. The game runs. The turret just points at the wrong thing.

## 2. Degrees, radians and why engines chose radians

### Two units for one quantity

You already know degrees: a full turn is 360°. The number 360 is a historical choice. It divides evenly by 2, 3, 4, 5, 6, 8, 9, 10 and 12, which made it convenient for ancient astronomers. It has nothing to do with the geometry of a circle.

A **radian** is defined by the circle itself. Take a circle of radius `r`. Walk along its edge a distance equal to `r`. The angle you swept out, measured from the center, is one radian. Since the full circumference is `2πr`, a full turn is `2π` radians, about 6.283.

That definition gives you the most useful formula in this lecture:

```
arc length  s = r × θ      (θ in radians)
```

With degrees you would need `s = r × θ × π / 180`. The radian is the unit that makes that conversion factor disappear. It is also the unit in which the calculus of `sin` and `cos` is cleanest, which is why every math library uses it.

### Converting

```
radians = degrees × π / 180
degrees = radians × 180 / π
```

Learn these landmarks by heart. You will use them every week for the rest of the course.

| Degrees | Radians (exact) | Radians (decimal) | Direction on screen (x right) |
|---|---|---|---|
| 0° | 0 | 0.000 | right |
| 45° | π/4 | 0.785 | diagonal |
| 90° | π/2 | 1.571 | a quarter turn |
| 180° | π | 3.142 | left |
| 270° | 3π/2 | 4.712 | three quarters |
| 360° | 2π | 6.283 | back to the start |
| 1 rad | 1 | 1.000 | about 57.3° |

### What your engine expects

Every mainstream math library takes radians. Unity's `Mathf.Sin` documents its input as an angle in radians, and Unity gives you `Mathf.Deg2Rad` and `Mathf.Rad2Deg` constants to convert. Godot's global `sin` names its parameter `angle_rad`, and Godot has `deg_to_rad` and `rad_to_deg`. JavaScript's `Math.sin`, C's `sin` and Python's `math.sin` all take radians too.

Engines often *display* degrees in the editor because designers read them more easily. Unity's inspector shows a Transform's rotation in degrees. Godot's inspector shows `rotation_degrees` while the script-side `rotation` property is in radians. So the number you typed into the editor may not be the number your script sees.

### The bug everyone writes once

Suppose you want a shield at the top of a circle and you write `sin(90)`. You expect 1. You get 0.894. And `cos(90)` gives −0.448 instead of 0.

What happened is that the library read 90 as 90 radians. That is 14 full turns plus about 2.035 radians (116.6°), so the point lands up and to the left instead of straight up. Nothing crashes. The shield is simply in the wrong place, and for other inputs it looks almost random.

The fix is a conversion at the boundary. Store angles in radians everywhere inside your code. Convert once, where a human types or reads a value. If you must keep degrees in a variable, put the unit in the name, such as `aimDeg`, so that `sin(aimDeg)` looks wrong when you read it.

## 3. Sin and cos are coordinates

### The unit circle

Draw a circle of radius 1 around the origin. This is the **unit circle**. Pick an angle `θ`, measured counterclockwise from the positive x-axis in the usual math convention. Walk out from the center at that angle until you hit the circle. The point you hit is:

```
(cos θ, sin θ)
```

That is the whole definition you need. `cos θ` is the x-coordinate of the point at angle `θ` on the unit circle, and `sin θ` is its y-coordinate. Everything else follows from it.

- At `θ = 0` the point is (1, 0), so `cos 0 = 1` and `sin 0 = 0`.
- At `θ = π/2` the point is (0, 1).
- At `θ = π` the point is (−1, 0).
- Both values always stay between −1 and 1, because the point is on a circle of radius 1.
- Since the point is on the unit circle, `cos²θ + sin²θ = 1` for every angle. That is Pythagoras applied to the triangle from the origin to the point.
- Adding `2π` to the angle brings you back to the same point, so both functions repeat every `2π`. We say they are **periodic** with period `2π`.

### Scaling and moving the circle

A circle of radius `r` centered at `(cx, cy)` is the unit circle stretched by `r` and then moved. So the point at angle `θ` on it is:

```
x = cx + r × cos θ
y = cy + r × sin θ
```

Read that as a recipe. `cos θ` and `sin θ` give you a direction of length 1. Multiplying by `r` makes it the right length. Adding the center moves it to the right place. In week 12 you will see the same recipe written with vectors: position equals center plus radius times a unit direction.

### Screen coordinates flip the picture

In math class, y points up and a positive angle turns counterclockwise. On most 2D screens and in many 2D engines, y points *down*: row 0 is the top of the window. The formulas above stay the same, but the picture flips. With y down, increasing `θ` makes a point move *clockwise* on screen.

This is not a bug, and you should not "fix" it by negating things at random. Decide once which convention your project uses, write it in a comment at the top of your math helpers, and test with the four landmark angles 0, π/2, π and 3π/2. If `θ = π/2` puts the point at the bottom of the screen, you are in a y-down world.

### The wave is the shadow of the circle

Now let the angle grow with time: `θ = ωt`, where `t` is time in seconds and `ω` (omega) is the **angular speed** in radians per second. The point goes around the circle at a steady rate.

Watch only its x-coordinate. It slides right, slows, stops at the edge, slides left, stops, and comes back. Plot that x-coordinate against time and you get the cosine wave. The y-coordinate gives the sine wave, the same shape shifted by a quarter turn. The waves are not a separate topic. They are what circular motion looks like when you only watch one axis.

This is the single most useful idea to take from this week. It explains why the same function drives both an orbiting shield and a gently bobbing pickup: the pickup is a point going around a circle that you only let move up and down.

## 4. Worked example: the orbiting shield

### The hook

In Vampire Survivors, the King Bible weapon is a set of books that spin around the player and damage any enemy they touch. The Amount stat adds more books, which join the circle spaced evenly. The Area stat pushes the books further from the player and makes them bigger.

Here is the surprising part. The community wiki warns that more Area can make the King Bible *worse*, because the books end up further apart and enemies slip through. How can a bigger shield protect you less? The answer is one line of trigonometry.

### The model

Place `N` orbs on a circle of radius `r` around a center `(cx, cy)`. The circle rotates at angular speed `ω` (radians per second). Orb number `k` (counting from 0 to `N − 1`) is at angle:

```
θ_k(t) = θ0 + ω × t + 2π × k / N
x_k(t) = cx + r × cos(θ_k(t))
y_k(t) = cy + r × sin(θ_k(t))
```

- `θ0` is the starting angle of orb 0.
- `ω t` is how far the whole ring has turned after `t` seconds.
- `2πk/N` is orb `k`'s fixed offset. Dividing a full turn into `N` equal slices is what "spaced evenly" means.

From this model three quantities fall out, and they are the ones a designer cares about.

```
gap along the arc between neighbors   = 2π r / N
straight-line gap (chord)             = 2 r sin(π / N)
speed of each orb                     = ω r
hits per second on a fixed spot of the ring = N ω / (2π)
```

The arc gap is just arc length `s = rθ` with `θ = 2π/N`. The chord is the straight distance between two neighbors, which is what an enemy has to squeeze through. The orb speed comes from the same arc-length formula: in one second the ring turns `ω` radians, so each orb travels `ω r`. The last line counts how often an orb passes a fixed spot: the ring makes `ω / 2π` full turns per second, and each turn carries `N` orbs past that spot.

### Numbers you can check

Take `N = 3`, `r = 100` pixels, `ω = π` rad/s (half a turn per second, 180°/s), `θ0 = 0`, center at the origin. The orb offsets are 0, 2π/3 and 4π/3 (0°, 120°, 240°).

| Orb k | Angle at t = 0 | Position at t = 0 | Angle at t = 0.25 s | Position at t = 0.25 s |
|---|---|---|---|---|
| 0 | 0° | (100.0, 0.0) | 45° | (70.7, 70.7) |
| 1 | 120° | (−50.0, 86.6) | 165° | (−96.6, 25.9) |
| 2 | 240° | (−50.0, −86.6) | 285° | (25.9, −96.6) |

Check one row by hand. For orb 1 at `t = 0.25`, the angle is `0 + π × 0.25 + 2π/3 = π/4 + 2π/3 = 11π/12`, which is 165°. `cos 165° = −0.966` and `sin 165° = 0.259`, times 100 gives (−96.6, 25.9).

Now the design numbers. Keep `ω = π` and vary `r` and `N`.

| N | r (px) | Arc gap 2πr/N | Chord gap 2r sin(π/N) | Orb speed ωr (px/s) | Hits/s on one spot |
|---|---|---|---|---|---|
| 3 | 100 | 209.4 | 173.2 | 314.2 | 1.5 |
| 3 | 150 | 314.2 | 259.8 | 471.2 | 1.5 |
| 4 | 100 | 157.1 | 141.4 | 314.2 | 2.0 |
| 4 | 150 | 235.6 | 212.1 | 471.2 | 2.0 |
| 6 | 100 | 104.7 | 100.0 | 314.2 | 3.0 |

Read the table as the King Bible puzzle solved. Raising the radius from 100 to 150 with 3 orbs grows the chord gap from 173 to 260 pixels, a 50% increase. The gap scales with `r`, so any enemy narrower than the gap minus the orb size can walk through between passes. The hit rate on a spot of the ring does not change with `r` at all, because it depends only on `N` and `ω`. So a bigger radius covers a larger area, but covers every part of it more thinly, and it does not hit any more often.

The fix a player reaches for is Amount. Going from 3 to 6 orbs at `r = 100` halves the arc gap and doubles the hit rate. In the model, `N` and `r` pull the gap in opposite directions, and the ratio `r / N` is what sets it.

### Move it yourself

Open [`examples/w10-orbit-and-waves.html`](../examples/w10-orbit-and-waves.html). The left panel shows the ring of orbs around a player dot, with the chord gap drawn between two neighbors and labeled in pixels. The right panel shows the x-coordinate of orb 0 over time as a scrolling cosine wave, with the y-coordinate as a second, fainter sine wave.

Drag the radius slider from 100 to 150. The ring grows, the gap label climbs from 173 to 260, and the "hits per second" readout stays at 1.5. Then drag the orb count slider to 6 and watch the gap shrink and the hit rate double. Finally switch on "Degrees bug" mode, which feeds the angle into `cos` and `sin` as if it were in degrees but without conversion. The orbs jump around the ring in a pattern that looks random. That is what the `sin(90)` bug looks like in motion.

### Cross-game recognition

**The Binding of Isaac: Rebirth.** A whole family of items, called orbitals on the community wiki, are familiars that circle Isaac at a set distance and block enemy shots or deal contact damage. Their job is the same as the King Bible's, and the same trade-off holds: an orbital that circles further out covers a bigger ring with the same number of bodies, so the gaps between blocking passes grow with the radius.

**Doom (1993).** Doom's source code, released by id Software, stores angles in neither degrees nor radians. An angle is a 32-bit unsigned integer where a full turn is 2³², so 90° is the hexadecimal constant `0x40000000` and 180° is `0x80000000`. Sine and cosine come from a lookup table of 8,192 entries per turn, which gives a resolution of about 0.044°. When a homing missile in Doom sets its velocity, the code multiplies its speed by the table's cosine for x and sine for y. That is `v = s × (cos θ, sin θ)`, the formula in section 5, written in a different unit. A nice side effect of the integer angle is that wraparound is free. Adding a quarter turn to three quarters overflows the integer and lands back at zero, with no `mod 360` needed.

**Your engine.** Unity's documentation for `Mathf.Sin` shows how to find the corners of a regular polygon by stepping the angle in increments of `2π / numSides`. That is the `2πk/N` term from our model, used to place vertices instead of shields.

Three different settings, one formula: center plus radius times `(cos θ, sin θ)`, with the angle split into `N` equal slices when you need `N` things.

### Eyes-open design judgment

Orbiting defenses are popular because the player can read them at a glance and they need no aiming. The math says what you actually control, and it is worth deciding each part on purpose.

- **Coverage is set by `r / N`, not by `r`.** If a stat grows the radius, pair it with something that grows `N` or the orb size, or players will discover, as Vampire Survivors players did, that the "upgrade" opens holes. Or embrace it: a radius stat that trades density for reach is a real choice, and a skilled player can make it.
- **Hit rate is set by `N ω`, not by `r`.** If you want a bigger ring to hit more, you must raise `ω` or `N`. Raising `ω` also raises the orb's linear speed `ωr`, which can make fast outer orbs hard to see. At `r = 150` and `ω = π`, each orb moves at 471 pixels per second, fast enough to blur at 60 frames per second (about 8 pixels per frame).
- **Discrete steps can tunnel.** At 60 frames per second, an orb at `r = 150` with `ω = 2π` moves about 16 pixels per frame. A small enemy can sit in the gap between two frames and never overlap the orb. The trig is exact. The collision check samples it.
- **Evenly spaced is a choice.** Clustered orbs (all offsets inside a 90° wedge) make a sweeping blade instead of a ring. The only change is the offset term.

### Check yourself

Questions 1 to 3 in the Check yourself section use this model directly.

## 5. Aiming: from an angle to a velocity

### One formula

A bullet fired from a point at angle `θ` with speed `s` (pixels per second) has velocity:

```
vx = s × cos θ
vy = s × sin θ
```

Each frame, you move it by velocity times the frame time: `x += vx × dt`, `y += vy × dt`. The `cos` and `sin` give the direction, the speed gives the length. This is the orbit recipe again, except the radius grows with time instead of the angle.

| Speed s | Angle | vx | vy | Where after 0.5 s (from origin) |
|---|---|---|---|---|
| 600 | 0° | 600.0 | 0.0 | (300.0, 0.0) |
| 600 | 30° | 519.6 | 300.0 | (259.8, 150.0) |
| 600 | 90° | 0.0 | 600.0 | (0.0, 300.0) |
| 600 | 135° | −424.3 | 424.3 | (−212.1, 212.1) |

Check the 30° row: `cos 30° = 0.866` and `sin 30° = 0.5`. The speed along the diagonal is still 600, since `519.6² + 300² = 360,000 = 600²`. Direction changes, speed does not. That property is the whole reason we use `cos` and `sin` here instead of, say, `(1, 0.5)`, and week 12 will show what goes wrong when a game forgets it.

### Radial bursts and spread

A radial burst, the ring of bullets a boss fires in a bullet-hell shooter, is the orbit model with time taken out. Fire `N` bullets at angles `θ0 + 2πk/N`. Eight bullets land at 0°, 45°, 90° and so on. Add a small `θ0` each wave, say 10°, and the rings rotate into a spiral, because each wave starts where the last one left off plus a little.

A shotgun spread is the same idea over a smaller arc. Five pellets across a 20° cone centered on your aim angle `a` go at `a − 10°, a − 5°, a, a + 5°, a + 10°`. The general form is `a − spread/2 + spread × k / (N − 1)` for `k = 0 … N − 1`. Note the `N − 1`. A cone has two edges and a ring has none, which is why the ring divides by `N` and the cone by `N − 1`.

Randomized spread uses the same formula with a random offset. Doom (1993) does this when a monster aims at a partly invisible player: it adds a random amount to the monster's facing angle, up to about 45° either way. Next week we look at that code in detail.

## 6. Waves over time: bobbing, pulsing, breathing

The shadow-of-a-circle idea from section 3 gives you a tool for anything that should move back and forth smoothly.

```
offset(t) = A × sin(2π × f × t + φ)
```

- `A` is the **amplitude**, how far it moves from the center (pixels, scale units, brightness).
- `f` is the **frequency** in cycles per second (hertz). One full cycle takes `1/f` seconds, the **period**.
- `φ` (phi) is the **phase**, a starting angle that shifts the wave in time.

The link to orbiting is `ω = 2πf`. A pickup that bobs once per second (`f = 1`) is the shadow of a point circling at `ω = 2π` rad/s.

Some uses with numbers:

- A coin bobbing 6 pixels up and down once every 1.5 seconds: `A = 6`, `f = 1/1.5 = 0.667` Hz.
- A "breathing" idle scale on a slime: `scale = 1 + 0.05 × sin(2π × 0.5 × t)`, so it grows and shrinks by 5% every 2 seconds.
- A row of 10 coins that should ripple like a wave instead of bobbing together: give coin `k` the phase `φ = 2πk/10`. That is the `2πk/N` offset from the orbit model, applied in time instead of space.

Two warnings. First, a sine wave spends most of its time near its peaks and moves fastest through the middle. That is what makes it look natural. It is also where the sine eases in Monocle's list from [MA101 week 9](w09-easing-curves-for-animation-feel.md) get their gentle starts and stops. `SineInOut(t) = (1 − cos(πt)) / 2` is half a turn of this circle's shadow, rescaled to run from 0 to 1, and like smoothstep it starts and ends at speed 0. Second, if you drive the wave with the real clock `t` but spawn objects at different times, they will all be in step. If you want each to start at the bottom of its bob, measure `t` from its own spawn time or set `φ` so that `sin(φ) = −1`, that is `φ = 3π/2`.

## In-class activity (25 minutes)

Work in pairs with a calculator or a spreadsheet and graph paper.

1. **Design a guardian ring (10 min).** A boss is surrounded by rotating fireballs. The player's hitbox is 24 pixels wide. Each fireball is 20 pixels across. You want the ring at `r = 120` pixels and you want a *skilled* player to be able to slip through, but only just. Find the number of fireballs `N` so that the chord gap minus one fireball diameter is between 30 and 40 pixels. Show the calculation for your chosen `N` and one neighbor value.
2. **Timing (5 min).** With your `N`, pick `ω` so that a fireball passes any point of the ring every 0.4 seconds. Give `ω` in rad/s and in degrees per second.
3. **Plot it (5 min).** Compute the positions of all fireballs at `t = 0` and `t = 0.1` s with `θ0 = 0` and the center at the origin. Sketch them on graph paper in a y-down frame, so you can see which way the ring turns on screen.
4. **Swap and attack (5 min).** Give your numbers to another pair. They must find the best moment to cross (how long the gap stays open at a given spot) and report it in seconds.

Expected output: one page with `N`, `ω`, two tables of positions, a sketch, and the other pair's crossing-window estimate. For step 1, `N = 5` gives a chord of 141.1 and a clearance of 121, which is too easy. Keep going.

## Common misconceptions

- **"`sin(90)` is 1."** Only if the function takes degrees, and almost none do. `sin(90)` in any standard library is 0.894 because 90 is read as radians. Convert with `× π/180` at the point where the human-readable value enters your code.
- **"Positive angles always turn counterclockwise."** Only when y points up. In a y-down screen space the same formulas turn clockwise on screen. Test with `θ = π/2` and see where the point goes.
- **"A bigger orbit radius gives a better shield."** It gives a bigger ring with the same number of orbs, so the gaps grow in proportion to `r` and the hit rate at any spot stays the same. Coverage depends on `r/N`.
- **"Sine waves and circles are different topics."** The sine wave is the y-coordinate of a point moving around a circle at constant speed. Bobbing, orbiting and aiming all use the same two functions for the same reason.

## Check yourself

1. Four shield orbs circle a player at `r = 80` px, `ω = 3π/2` rad/s, `θ0 = 0`. Where is orb 2 at `t = 0.5` s (center at the origin, math convention)?
2. A designer wants a ring of orbs at `r = 200` px with a chord gap of at most 100 px. What is the smallest `N` that works?
3. An upgrade increases orbit radius by 25% and angular speed by 25%. By what percentage do the chord gap, the orb's linear speed and the hits per second on a fixed spot change?
4. A turret fires at 45° with speed 400 px/s. Give the velocity components. The code accidentally passes 45 to `cos` and `sin` without converting. Give the components it actually uses and the angle in degrees the bullet actually travels.
5. You want 12 coins in a row to ripple so that the wave travels exactly once along the row. What phase do you give coin `k`?

<details>
<summary>Answers</summary>

1. `θ_2 = 0 + (3π/2)(0.5) + 2π(2)/4 = 3π/4 + π = 7π/4`, which is 315°. Position `(80 cos 315°, 80 sin 315°) = (56.6, −56.6)`.
2. Need `2 × 200 × sin(π/N) ≤ 100`, so `sin(π/N) ≤ 0.25`, so `π/N ≤ 0.2527`, so `N ≥ 12.43`. The smallest whole number is `N = 13` (chord 95.7 px). `N = 12` gives 103.5 px, which is too wide.
3. Chord gap is proportional to `r`, so +25%. Linear speed `ωr` changes by `1.25 × 1.25 = 1.5625`, so +56.25%. Hits per second `Nω/2π` depend only on `ω`, so +25%.
4. Intended: `(400 cos 45°, 400 sin 45°) = (282.8, 282.8)`. Actual: 45 radians is 7 full turns plus 1.018 rad (58.3°), so `cos 45 = 0.525` and `sin 45 = 0.851`, giving `(210.1, 340.4)`. The bullet travels at about 58.3°, still at speed 400.
5. `φ_k = 2πk/12 = πk/6`. Coin 12 would have phase `2π`, which is the same as coin 0, so the pattern repeats exactly once along the row.

</details>

## Lab hook

**Lab 10: Orbits and bursts.** You build an orbiting shield and a radial bullet pattern, then tune them against the gap and hit-rate numbers from section 4. The brief is in [Lab 10](../labs/lab10.md).

## Sources

- Vampire Survivors Wiki (community, vampire.survivors.wiki), "King Bible", accessed September 2026. Describes the books spinning around the player, extra books from Amount being spaced evenly, Area pushing them further out, and the note that bigger Area can leave larger gaps. Current game version at time of access.
- The Binding of Isaac: Rebirth Wiki (Fandom), "Familiar", accessed September 2026. Defines orbitals as familiars that circle Isaac and block shots or deal contact damage (Rebirth and its expansions).
- id Software, DOOM source code (linuxdoom-1.10, released 1997), files `tables.h` (angle type, `ANG90 = 0x40000000`, `FINEANGLES = 8192`) and `p_enemy.c` (`A_Tracer` sets momentum from speed times `finecosine` and `finesine`; `A_FaceTarget` adds random angle offset for shadowed targets). github.com/id-Software/DOOM.
- Unity Technologies, Scripting API, `Mathf.Sin` (input in radians; polygon example using `2π / numSides`), `Mathf.Deg2Rad`, `Transform.eulerAngles` (degrees). Unity 6 documentation, accessed September 2026.
- Godot Engine documentation, `@GlobalScope` (`sin(angle_rad)`, `deg_to_rad`), `Node2D.rotation` and `rotation_degrees`. Godot 4.x stable docs, accessed September 2026.
- Dunn, F. & Parberry, I. (2011). *3D Math Primer for Graphics and Game Development* (2nd ed.). CRC Press. Chapter 1.
- Holmér, F. *Math for Game Devs* (lecture series, YouTube, 2022).

## Interactive spec: examples/w10-orbit-and-waves.html

**The one insight:** an orbiting point's x and y are `cos` and `sin` of a growing angle, and the gap between `N` orbs grows with `r` while the hit rate does not. The first screen must show both at once, without any interaction.

**Layout.** Two linked panels side by side at desktop width, stacked on mobile (circle first).

- **Left panel, "Ring".** A player dot at the center. `N` orbs on a circle of radius `r`, rotating at `ω`. Draw the circle faintly. Draw a straight segment between orb 0 and orb 1 labeled with the chord length in px, and a thin arc between them labeled with the arc length. Draw a short fixed tick mark on the ring at angle 0 (the "probe spot"); flash it each time an orb passes it. Use y-down screen coordinates, so the ring turns clockwise on screen, and show a small note "y points down: positive ω turns clockwise".
- **Right panel, "Shadow".** A scrolling plot of orb 0's x-coordinate (solid) and y-coordinate (dashed, lighter) against time over the last 4 seconds, range `−r` to `+r`. Draw a horizontal dotted line from orb 0 in the left panel to the current point on the x trace, so the student sees the wave is the orb's shadow.

**Controls** (all keyboard accessible, labels with live values).

- `N` orbs: integer slider 1 to 12, default 3.
- Radius `r`: slider 40 to 200 px (in model units; scale to the canvas), step 5, default 100.
- Angular speed `ω`: slider 0 to 4π rad/s, step π/8, default π. Show value as "π rad/s = 180°/s".
- Pause/play button (respect `prefers-reduced-motion`: start paused, show a still frame with the numbers).
- Time scrub slider 0 to 4 s, active when paused, so students can set `t = 0.25` exactly.
- Toggle "Degrees bug": when on, compute `θ_k` in degrees (`θ0 + ωdeg × t + 360k/N`) and pass it straight into `Math.cos` / `Math.sin` without conversion. Show a red banner "angle passed as degrees".

**Readouts** (monospace, next to the visual): each orb's angle in degrees and radians and its (x, y) to 1 decimal; arc gap `2πr/N`; chord gap `2r sin(π/N)`; orb speed `ωr` in px/s and px/frame at 60 fps; hits per second on the probe spot `Nω/2π`.

**Formulas.** `θ_k(t) = θ0 + ωt + 2πk/N`, `θ0 = 0`. `x_k = r cos θ_k`, `y_k = r sin θ_k` (model coordinates, y-down on screen).

**Test values (must match exactly to 1 decimal).**

- `N = 3, r = 100, ω = π, t = 0`: orbs at (100.0, 0.0), (−50.0, 86.6), (−50.0, −86.6).
- Same, `t = 0.25`: (70.7, 70.7), (−96.6, 25.9), (25.9, −96.6).
- `N = 3, r = 100`: chord 173.2, arc 209.4, hits/s 1.5. `r = 150`: chord 259.8, arc 314.2, hits/s 1.5, speed 471.2 px/s.
- `N = 6, r = 100`: chord 100.0, arc 104.7, hits/s 3.0.
- Degrees bug, `N = 1`, angle 90: orb at `(r × −0.448, r × 0.894)`.

**Accessibility.** Canvas has an `aria-label` summarizing the current numbers; readouts are live text, not canvas-drawn. Colors from `templates/interactive-tokens.css`; x and y traces also differ by dash pattern, not only color.

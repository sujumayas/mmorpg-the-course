# MA101 · Week 08 — Interpolation: Lerp, Inverse Lerp and Remap

**Why this matters:** Game code is full of one move: take a number from one range and turn it into a number in another range. Fall speed becomes sprite squash, distance becomes damage, time becomes position, health becomes bar colour. Three tiny functions do all of it, and once you know them you will see them in every engine and every codebase you open.

**You will be able to:**
- Compute `lerp`, `inverseLerp` and `remap` by hand and in code, with and without clamping.
- Derive `remap` from `lerp` and `inverseLerp`, and recognise it when it is written differently.
- Design a clamped remap from a gameplay input to a visual or numeric output, and choose its ranges.
- Explain why "lerp toward a target every frame" depends on frame rate, and fix it.

**Before class:** Freya Holmér, "Lerp smoothing is broken" (article on her Substack, 2024, about 15 minutes; the talk version from Guadalindie 2024 is optional). Re-read section 3 of MA101 week 7 on `min`, `max` and `clamp`.

**Prerequisites from earlier courses:** MA101 has no prerequisite course. This week uses straight lines and slope from [MA101 week 2](w02-linear-functions-and-rates.md), exponentials from [MA101 week 4](w04-exponentials-and-the-xp-curve.md) and clamping from [MA101 week 7](w07-piecewise-caps-and-floors.md).

**Interactive:** [examples/w08-remap-squash.html](../examples/w08-remap-squash.html). Keep it open during section 2.

---

## 1. Three small functions

### Lerp: "go this fraction of the way"

**Lerp** is short for linear interpolation. Give it a start value `a`, an end value `b` and a fraction `t`, and it returns the value that is `t` of the way from `a` to `b`:

```
lerp(a, b, t) = a + (b − a) × t
```

- `a` is the value at `t = 0`.
- `b` is the value at `t = 1`.
- `t` is the **parameter**, a fraction. `t = 0.25` means a quarter of the way.

Check it. `lerp(10, 50, 0.25) = 10 + 40 × 0.25 = 20`. A quarter of the way from 10 to 50 is 20. `lerp(10, 50, 0) = 10` and `lerp(10, 50, 1) = 50`, as they should be.

You can rearrange the same formula as a weighted blend:

```
lerp(a, b, t) = (1 − t) × a + t × b
```

At `t = 0.25` this gives 75% of `a` plus 25% of `b`. That reading is handy for colours and positions: to blend red and blue, lerp each channel. Many engines and shading languages call this function `mix`, which is a good name for this second reading.

Lerp is a straight line through two points, `(0, a)` and `(1, b)`, so everything you learned about lines in week 2 applies. The slope is `b − a`. The intercept is `a`.

### Inverse lerp: "what fraction of the way am I?"

**Inverse lerp** runs the question backwards. You know the start, the end, and a value `v` somewhere along the way. What is `t`?

```
inverseLerp(a, b, v) = (v − a) / (b − a)
```

Check it. `inverseLerp(10, 50, 20) = (20 − 10) / (50 − 10) = 10 / 40 = 0.25`. It undoes the lerp above. That is what "inverse" means: `inverseLerp(a, b, lerp(a, b, t)) = t` for any `t`, as long as `a ≠ b`.

Inverse lerp turns any range into the **unit range** from 0 to 1. That is what makes it useful. Health from 0 to 350 becomes a fraction from 0 to 1. Distance from 20 m to 80 m becomes a fraction. Time from the start of an animation to its end becomes a fraction. Once everything is a fraction, everything can talk to everything else.

### Remap: "same position, new range"

**Remap** chains the two. Find where `v` sits in the input range, then go the same fraction of the way along the output range:

```
remap(v, inA, inB, outA, outB) = lerp(outA, outB, inverseLerp(inA, inB, v))
```

Written out in one line:

```
remap(v, inA, inB, outA, outB) = outA + (outB − outA) × (v − inA) / (inB − inA)
```

Check it. Map a health value of 70 out of 0 to 350 onto a bar that is 200 pixels wide: `remap(70, 0, 350, 0, 200) = 0 + 200 × 70/350 = 40` pixels. Health is 20% full, the bar is 20% full.

### Outside the range: extrapolation and clamping

Nothing in these formulas stops `t` from going below 0 or above 1. `lerp(10, 50, 1.5) = 70`. That is **extrapolation**, continuing the line past its endpoints. Sometimes you want it. Often you do not: a health bar should never draw wider than its frame.

So each function has a **clamped** version that forces `t` into `[0, 1]` first, using the clamp from week 7:

```
clampedRemap(v, inA, inB, outA, outB) = lerp(outA, outB, clamp(inverseLerp(inA, inB, v), 0, 1))
```

Engines disagree about which version is the default. Some clamp inside `lerp` and offer an "unclamped" variant. Others never clamp and expect you to do it. The Monocle engine that Celeste was built on has both a `Map` and a `ClampedMap`. The first time you use an engine's lerp, read its documentation for one thing: does it clamp?

One more trap. `inverseLerp(a, b, v)` divides by `b − a`. If a designer sets both ends of a range to the same number, you divide by zero. Guard against it.

## 2. Worked example: Celeste's landing squash

### The hook

In Celeste (Maddy Makes Games, 2018), when Madeline lands, her sprite squashes wide and short for a moment, then springs back. Watch closely and you will notice the squash is bigger when she lands from higher up. A small hop gives a small squash. A long fall gives a big one.

The developers published the player code in 2018. The landing squash is two lines of arithmetic: an inverse lerp and a lerp. No physics, no animation file.

### The model

When Madeline touches the ground with downward speed `v` (pixels per second), the published code computes:

```
squish = min(v / 240, 1)
scaleX = lerp(1, 1.6, squish)
scaleY = lerp(1, 0.4, squish)
```

- `v` is the landing speed. In this code, downward is positive.
- `240` is the constant `FastMaxFall`, the fastest Madeline falls when the player holds down. Normal maximum fall speed (`MaxFall`) is 160.
- `squish` is a fraction from 0 to 1.
- `scaleX` and `scaleY` multiply the sprite's width and height. `1` means normal size.

Read it with this week's vocabulary. `v / 240` is `inverseLerp(0, 240, v)`: what fraction of the fastest fall speed is this landing? The `min(…, 1)` clamps it from above (landings are never negative, so no floor is needed). Then two lerps turn that one fraction into two scales: width grows toward 1.6, height shrinks toward 0.4.

As one expression, `scaleX = clampedRemap(v, 0, 240, 1, 1.6)`. One input range, two output ranges, one shared `t`.

### Numbers you can check

| Landing speed v (px/s) | squish = min(v/240, 1) | scaleX = lerp(1, 1.6, squish) | scaleY = lerp(1, 0.4, squish) |
|---|---|---|---|
| 0 | 0 | 1.00 | 1.00 |
| 60 | 0.25 | 1.15 | 0.85 |
| 120 | 0.5 | 1.30 | 0.70 |
| 160 (normal max fall) | 0.667 | 1.40 | 0.60 |
| 200 | 0.833 | 1.50 | 0.50 |
| 240 (fast-fall max) | 1 | 1.60 | 0.40 |
| 300 (hypothetical) | 1 (clamped) | 1.60 | 0.40 |

Check the 160 row by hand. `160 / 240 = 2/3`. `lerp(1, 1.6, 2/3) = 1 + 0.6 × 2/3 = 1.4`. `lerp(1, 0.4, 2/3) = 1 − 0.6 × 2/3 = 0.6`.

Two things are worth noticing. First, a normal full-speed fall gives 1.4 by 0.6, and only a held fast-fall reaches the full 1.6 by 0.4. The maximum squash is saved as a reward for the more committed move. Second, the last row cannot normally happen, because Madeline's speed is limited to 240. The clamp is a guard. If a later mechanic ever pushes her faster, the sprite will not collapse to a sliver. Without the clamp, 300 px/s would give `scaleY = 0.25`.

The squash does not stay. Every frame, the code moves each scale back toward 1 by at most `1.75 × dt`, where `dt` is the frame time in seconds. So a 1.6 squash takes `0.6 / 1.75 ≈ 0.34` seconds to recover, and a 1.4 squash about `0.23` seconds. That recovery is linear in time, which you will compare with other shapes next week.

### The visual

Open [`examples/w08-remap-squash.html`](../examples/w08-remap-squash.html). On the left is a number line for landing speed from 0 to 300 px/s. Under it is a second line for `squish` from 0 to 1. On the right are the two output ranges, width from 1 to 1.6 and height from 1 to 0.4, plus a plain rectangle that squashes as you drag. Thin connector lines join the same point on every line.

Drag the speed slider. The marker slides along the input line, the `t` marker moves the same proportion along the unit line, and both output markers move the same proportion along their own lines. One of them moves right while the other moves left, because `0.4 < 1`. Then drag past 240: the input marker keeps going, but `t` stops at 1 and everything downstream freezes. That frozen moment is the clamp.

Switch off the clamp and drag past 240 again. The rectangle keeps flattening. That is extrapolation, and it shows why the clamp is there.

### Cross-game recognition

Once you know the shape `lerp(outA, outB, inverseLerp(inA, inB, v))`, you find it everywhere.

**Celeste again, wall slide.** While Madeline slides down a wall, a timer drains from 1.2 s to 0. Her maximum fall speed is `lerp(160, 20, timer / 1.2)`. Here `timer / 1.2` is an inverse lerp of the time left. At the start of the slide (timer 1.2) the cap is 20 px/s, a gentle slide. Halfway (timer 0.6) it is 90. When the timer runs out it is back to the normal 160. The same code base remaps fast-fall speed from 200 to 240 onto a vertical stretch of the sprite, from 1 to 1.5.

**Team Fortress 2 (Valve, 2007 onward), damage over distance.** The official TF2 wiki documents a distance modifier for most weapons. It is 1.5 at point blank (0 Hammer units), 1.0 at 512 units, and 0.5 at 1,024 units or further. Those three points sit exactly on the clamped remap `clampedRemap(d, 0, 1024, 1.5, 0.5) = 1.5 − d / 1024`. Check it: at 512, `1.5 − 0.5 = 1.0`. But the wiki also says the curve between them is cubic, not a straight line, and that random spread shifts the distance by about 100 units. So the ranges are a remap, and the shape between them is something else. Next week you will learn how to bend a remap on purpose.

**OpenGL linear fog (fixed-function pipeline, OpenGL 1.x and 2.x).** The classic fog formula is `f = (end − c) / (end − start)`, clamped to `[0, 1]`, where `c` is the distance to the camera and `f` is how much of the object's own colour survives. Rewrite it: `f = 1 − inverseLerp(start, end, c)`. The final colour is then `lerp(fogColour, objectColour, f)`. A whole generation of 3D games used fog that was one inverse lerp and one lerp.

**Counter-Strike: Global Offensive (2012 to 2023), for contrast.** Not every falloff is a remap. CS:GO multiplies bullet damage by `rangeModifier^(distance / 500)`, where each weapon has its own modifier, 0.98 for the AK-47. That is an exponential from week 4, not a lerp. It has no end distance and no clamp: damage keeps shrinking forever, a little less each step. Put it next to TF2 and you see a design choice. A remap gives you two distances you control exactly. An exponential gives you one rate and no endpoint.

Four contexts, one question: *what is the input range, what is the output range, and is it clamped?*

### Design judgment

A remap is the most readable tuning tool you have. Its four numbers mean something to a designer: "squash starts at 0 px/s, reaches full at 240, full is 1.6 wide." Compare that with a hand-tuned polynomial whose coefficients mean nothing. When a designer asks for a change ("make small hops squash less"), you change one number and everyone can predict the result.

That readability comes with choices you must make on purpose:

- **Where does the input range start?** Celeste starts squash at 0 px/s, so even a tiny drop squashes a little. If you started at 60 instead, every landing slower than 60 would look identical. Sometimes that is right (you may not want the sprite to twitch on every step down a staircase).
- **Clamp or extrapolate?** Clamp anything the player sees and anything that can break (sizes, colours, percentages). Extrapolate only when you want the trend to continue and you have checked the extremes.
- **Keep area or not?** At full squash Celeste's sprite is `1.6 × 0.4 = 0.64` of its normal area. That reads as a hard impact. Animators often prefer to keep area constant, `scaleY = 1 / scaleX`, so the character looks squashed rather than smaller. Neither is correct. Choose the one that matches the feel you want.
- **Is linear the right shape?** A remap is a straight line between two points. Many things feel better on a curve, which is next week's topic. Keep the remap for the ranges and add a curve for the shape.

### Check yourself (worked example)

1. Madeline lands at 90 px/s. Compute `squish`, `scaleX` and `scaleY`. How long does the squash take to recover at 1.75 per second?
2. You want an area-preserving version: keep `scaleX = lerp(1, 1.6, squish)` but set `scaleY = 1 / scaleX`. What is `scaleY` at full squash, and how does it compare with Celeste's 0.4?

<details>
<summary>Answers</summary>

1. `squish = 90/240 = 0.375`. `scaleX = 1 + 0.6 × 0.375 = 1.225`. `scaleY = 1 − 0.6 × 0.375 = 0.775`. Recovery time is `0.225 / 1.75 ≈ 0.13` s for both scales.
2. `scaleY = 1/1.6 = 0.625`. That is a much milder vertical squash than 0.4, so the landing reads as softer.

</details>

## 3. Lerping more than one number

Lerp works on anything you can add and scale, one component at a time.

- **Positions.** To move a point from `P = (2, 8)` to `Q = (10, 4)`, lerp x and y separately: `lerp(P, Q, 0.25) = (2 + 8 × 0.25, 8 − 4 × 0.25) = (4, 7)`. The result always lies on the straight segment between the two points. You will meet this again in MA101 week 12, when positions become vectors.
- **Colours.** A health bar that goes from green `(0, 200, 0)` at full health to red `(220, 0, 0)` at empty: compute `t = inverseLerp(0, maxHP, hp)`, then lerp each channel from red to green. At half health you get `(110, 100, 0)`, a muddy olive. That is a known weakness of lerping in RGB: the midpoint can look darker or duller than either end. Designers often add a yellow midpoint instead, which brings us to the next idea.

### Several keys: piecewise lerp

Suppose you want green at full health, yellow at half, and red at empty. Now you have three **keys** (value and output pairs), and between each pair you lerp. This is a piecewise function where each piece is a remap:

```
       ⎧ remap(hp, 0,   50, red,    yellow)   if hp < 50
col =  ⎨
       ⎩ remap(hp, 50, 100, yellow, green)    if hp ≥ 50
```

You have seen this before. The straight-line Elden Ring model in week 7 was exactly a piecewise lerp through four keys. Every curve editor in every engine, from animation timelines to damage-over-level tables, stores keys and interpolates between them. Linear interpolation between keys is the simplest choice. Next week you will change the shape between keys.

To evaluate a piecewise lerp in code:

1. Find the two keys the input falls between (the one just below and the one just above).
2. Inverse-lerp the input between those two keys to get a local `t`.
3. Lerp the two keys' outputs with that `t`.

If the input is below the first key or above the last, either clamp to the end value or extrapolate the first or last segment. Say which in your spec.

## 4. Lerp in a loop: smoothing and its trap

So far `t` came from a range: a speed, a distance, a health value. There is a second common use of lerp where `t` is a fixed small number and the lerp runs every frame:

```
x = lerp(x, target, k)      // every frame, e.g. k = 0.1
```

Each frame, `x` moves 10% of the remaining distance to `target`. It moves fast when far away and slows as it gets close, and it never quite arrives. This is **lerp smoothing**, and it is everywhere: cameras that trail a player, health bars that drain toward the real value, UI that glides into place.

Work out what happens. After one frame the remaining gap is `(1 − k)` of what it was. After `n` frames it is `(1 − k)^n`. That is the exponential decay from week 4, sampled once per frame.

Now the trap. The number of frames per second depends on the player's machine. Take `k = 0.1` and measure the gap left after half a second:

| Frame rate | Frames in 0.5 s | Gap left with fixed k = 0.1 | Gap left with k = 6 × dt | Gap left with k = 1 − e^(−6 dt) |
|---|---|---|---|---|
| 30 fps | 15 | 0.206 (20.6%) | 0.035 | 0.050 |
| 60 fps | 30 | 0.042 (4.2%) | 0.042 | 0.050 |
| 144 fps | 72 | 0.0005 (0.05%) | 0.047 | 0.050 |

With a fixed `k`, the camera on a 30 fps laptop is still 20% behind after half a second, and on a 144 fps monitor it has already arrived. Same code, different game.

The common patch is to scale `k` by the frame time: `k = speed × dt`. Celeste does this for Madeline's hair colour, `lerp(hairColour, usedColour, 6 × dt)`. It is much better (the middle column is close across frame rates) but not exact, and it breaks if a frame is long enough that `speed × dt > 1`.

The exact fix follows from the exponential view. You want the gap to shrink by the same fraction per second whatever the frame rate, so use:

```
k = 1 − exp(−λ × dt)
x = lerp(x, target, k)
```

where `λ` (lambda) is a decay rate in "per second" units. With `λ = 6`, the gap after 0.5 s is `e^(−3) ≈ 0.050` at every frame rate, as the last column shows. Freya Holmér's 2024 talk and article walk through this derivation in detail and are this week's reading.

One more distinction. Lerp smoothing moves toward a target that may itself move. It has no fixed duration and no end. That makes it a different tool from the timed animations you will build next week, where you know the start, the end and the duration in advance. Do not call lerp smoothing an "easing curve"; it is exponential decay.

## In-class activity (25 minutes)

Work in groups of three. You are building the feedback for a charged bow shot in a top-down action game. The player holds a button for between 0.2 s and 1.5 s.

1. Decide the input range. Is 0.2 s the "zero" of your charge, or 0? Write your choice and one reason.
2. Write clamped remaps from hold time to three outputs: arrow damage (20 to 80), arrow speed (400 to 900 px/s) and the pitch of the charge sound (1.0 to 1.5). Compute all three at hold times 0.1, 0.5, 0.85, 1.5 and 2.0 s.
3. Add a colour: the bow glows white at no charge, orange at half charge, red at full. Write it as a piecewise lerp with three keys.
4. One person argues damage should extrapolate past 1.5 s ("reward patience"). Another argues it should clamp. Decide, and write down one exploit or problem the losing option would have caused.

Expected output: a one-page sheet with the remaps, the numeric table, the colour keys and your decision.

## Common misconceptions

- **"Lerp is only for positions."** Lerp works on any quantity you can add and scale: sizes, colours, volumes, damage, time.
- **"`t` has to be between 0 and 1."** Mathematically, no. Values outside that range extrapolate. Whether your engine clamps `t` is an engine decision, so check.
- **"Inverse lerp gives a percentage, so it is always between 0 and 1."** Only if the value lies inside the range. `inverseLerp(10, 50, 70) = 1.5`.
- **"`x = lerp(x, target, 0.1)` every frame is a smooth, fixed-speed animation."** It is exponential decay, it depends on frame rate unless you use `1 − e^(−λ dt)`, and it never exactly arrives.

## Check yourself

1. Compute `lerp(−20, 30, 0.6)`, `inverseLerp(200, 50, 110)` and `remap(45, 30, 90, 1, 0)`.
2. A spell's cast time falls linearly from 2.5 s at level 1 to 1.0 s at level 20, and stays at 1.0 s after that. Write it as a clamped remap. What is the cast time at level 8 and at level 25?
3. In OpenGL linear fog, `start = 20` and `end = 100`. What fraction of an object's colour survives at distance 40 and at distance 120?
4. A camera uses `x = lerp(x, target, 0.2)` every frame at 60 fps. Your game now runs at 120 fps. What `k` per frame keeps the same behaviour? (Hint: two frames at 120 fps must shrink the gap as much as one frame at 60 fps.)

<details>
<summary>Answers</summary>

1. `−20 + 50 × 0.6 = 10`. `(110 − 200)/(50 − 200) = −90/−150 = 0.6`. `inverseLerp(30, 90, 45) = 15/60 = 0.25`, so `lerp(1, 0, 0.25) = 0.75`.
2. `castTime = clampedRemap(level, 1, 20, 2.5, 1.0)`. At level 8, `t = 7/19 ≈ 0.368`, so `2.5 − 1.5 × 0.368 ≈ 1.95` s. At level 25, `t` clamps to 1, so 1.0 s.
3. `f = (100 − 40)/(100 − 20) = 0.75`, so 75% survives. At 120, `f = −20/80 = −0.25`, which clamps to 0: the object is fully fogged.
4. At 60 fps one frame leaves `0.8` of the gap. At 120 fps two frames must leave `0.8`, so `(1 − k)^2 = 0.8`, `1 − k = √0.8 ≈ 0.894`, and `k ≈ 0.106`. Not 0.1. Halving `k` is close but not exact.

</details>

## Lab hook

**Lab 08, Remap everything.** Implement `lerp`, `inverseLerp`, `remap` and a piecewise-lerp key table in code, drive a squash-and-stretch sprite and a damage-falloff readout from them, then measure and fix frame-rate-dependent smoothing. See [labs/lab08.md](../labs/lab08.md).

## Sources

- NoelFB/Celeste repository on GitHub, `Source/Player/Player.cs` (published 2018; MIT licence covers the code files only). Landing squash `min(Speed.Y / FastMaxFall, 1)` with scales lerped to 1.6 and 0.4; constants `MaxFall = 160`, `FastMaxFall = 240`; recovery `Approach(scale, 1, 1.75 × dt)`; wall-slide `lerp(MaxFall, WallSlideStartMax, timer / WallSlideTime)` with `WallSlideStartMax = 20`, `WallSlideTime = 1.2`; fast-fall stretch; hair colour `Color.Lerp(…, 6 × dt)`.
- Monocle engine (Matt Thorson), open source and linked from the Celeste repository; GitHub mirror `monocle-engine`, file `Monocle/Util/Calc.cs`. `Map`, `ClampedMap` and `Approach`. The open-source version may differ in details from the one shipped in Celeste.
- Official TF2 Wiki, "Damage" (retrieved September 2026). Distance modifier 1.5 at 0 HU, 1.0 at 512 HU, 0.5 at 1,024 HU or further; described as cubic; random spread of about 102 HU; weapon exceptions.
- Khronos Group, OpenGL 2.1 reference page `glFog`. `GL_LINEAR` fog factor `(end − c)/(end − start)`, clamped to `[0, 1]`.
- Counter-Strike Wiki (Fandom), "Damage dropoff" and "AK-47"; Z. Virant, "A comparison of damage falloff in PvP FPSs" (Medium). CS:GO damage formula `damage × rangeModifier^(distance/500)`, AK-47 modifier 0.98.
- Holmér, F. (2024). "Lerp smoothing is broken" (Substack article; talk recorded at Guadalindie 2024). Frame-rate-independent lerp smoothing with an exponential decay factor.

## Interactive spec: examples/w08-remap-squash.html

**Insight the visual must make obvious:** remap is one shared fraction `t`. The input marker, the `t` marker and every output marker always sit at the same proportion of their own lines. When the input passes the end of its range, `t` stops at 1 and every output freezes (clamp on), or keeps going (clamp off).

**Layout.** Two linked views. Stack vertically on mobile.

- View A, "The mapping": four horizontal number lines, one above another, with thin vertical connector lines through the current marker positions. (1) Input "Landing speed (px/s)", 0 to 300, with the range 0 to 240 shaded and ticks at 160 ("normal max fall") and 240 ("fast-fall max"). (2) "t = inverseLerp(0, 240, v)", drawn from −0.25 to 1.25 with 0 to 1 shaded. (3) "scaleX", 1.0 to 1.6 shaded, drawn from 0.85 to 1.75. (4) "scaleY", drawn so that 1.0 is on the left and 0.4 on the right (the line runs backwards), shaded 1.0 to 0.4, drawn from 1.15 to 0.25. Label the backwards line clearly.
- View B, "The sprite": a plain rounded rectangle (generic, no character art) standing on a ground line, drawn at `scaleX × 40` px wide and `scaleY × 60` px tall, anchored at its bottom centre. Show a dashed outline of the unscaled 40 × 60 rectangle for reference and the area ratio `scaleX × scaleY`.

**Controls.**
- Slider "Landing speed v" (0 to 300 px/s, step 1, default 160). Arrow keys adjust by 1, Page Up and Page Down by 20.
- Toggle "Clamp t to [0, 1]" (default on).
- Toggle "Keep area constant (scaleY = 1/scaleX)" (default off). When on, line (4) shows the new scaleY and the readout says so.
- Button "Play landing": animates the rectangle from the squashed scale back to 1 using `Approach(scale, 1, 1.75 × dt)` per frame, and prints the recovery time. Respect `prefers-reduced-motion` by jumping straight to the end state and printing the time.
- Mode switch "Other remaps": (a) "Celeste wall slide": input timer 1.2 → 0 s, output max fall speed `lerp(160, 20, timer/1.2)`; (b) "TF2 distance modifier (linear version)": input distance 0 to 1,400 HU, output `clampedRemap(d, 0, 1024, 1.5, 0.5)`, with a note that the real curve between the endpoints is cubic per the TF2 wiki; (c) "Linear fog": input distance 0 to 150 with start 20 and end 100, output surviving fraction `clamp((end − c)/(end − start), 0, 1)`.

**Readout (next to the visual, copyable):** `v = …, t = …, scaleX = …, scaleY = …, area = …`.

**Exact formulas.** `t = v / 240`, clamped to `[0, 1]` when the toggle is on. `scaleX = 1 + 0.6 t`. `scaleY = 1 − 0.6 t`, or `1 / scaleX` in keep-area mode. Recovery time `= max(|scaleX − 1|, |scaleY − 1|) / 1.75` seconds.

**Test values.** v=0 → t 0, 1.00 × 1.00. v=60 → 0.25, 1.15 × 0.85. v=90 → 0.375, 1.225 × 0.775. v=160 → 0.667, 1.40 × 0.60, area 0.84. v=240 → 1, 1.60 × 0.40, area 0.64, recovery 0.343 s. v=300 clamp on → 1.60 × 0.40; clamp off → t 1.25, 1.75 × 0.25. Keep-area at v=240 → scaleY 0.625. Wall slide timer 0.6 → 90 px/s. TF2 linear d=512 → 1.0, d=1200 → 0.5 (clamped). Fog c=40 → 0.75, c=120 → 0.

**Constraints.** Generic shapes only. No Celeste character art, names on the sprite, logos or screenshots. Name the games in labels only.

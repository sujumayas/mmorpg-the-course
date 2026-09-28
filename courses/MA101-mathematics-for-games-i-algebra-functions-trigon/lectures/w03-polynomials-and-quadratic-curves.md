# MA101 · Week 03 — Polynomials and Quadratic Curves (Jump Arcs)

**Why this matters:** Every jump, thrown grenade and arrow arc in a 2D or 3D game is a quadratic, and so are many experience tables. If you can write a quadratic from the numbers a designer cares about (how high, how long), you stop tuning gravity by guesswork and start designing jumps on paper.

**You will be able to:**
- Compute gravity and launch speed for a jump from a chosen height and time to apex, and predict the whole arc.
- Detect whether a table of game data is linear, quadratic or cubic using differences.
- Solve a quadratic equation to answer "when does the arc reach this height?" and read the discriminant as "can it reach at all?"
- Critique a jump design that uses different gravity going up and coming down.

**Before class:** J. Kyle Pittman, "Math for Game Programmers: Building a Better Jump" (GDC 2016), slides or video, first half (up to "Time and space"). Dunn & Parberry, *3D Math Primer*, chapter 1, the 2D coordinate sections, for reading position graphs.

**Prerequisites from earlier courses:** [MA101 week 1](w01-functions-as-machines.md) (functions, composition, inverses) and [MA101 week 2](w02-linear-functions-and-rates.md) (slope, rates, units). No earlier courses.

**Interactive:** [`examples/w03-jump-designer.html`](../examples/w03-jump-designer.html). Keep it open during section 2.

---

## 1. Polynomials, and what degree does

A **polynomial** is a sum of terms, each a number times a whole-number power of the input:

```
f(x) = a₀ + a₁·x + a₂·x² + a₃·x³ + ...
```

The numbers `a₀, a₁, a₂ ...` are the **coefficients**. The highest power with a coefficient that is not zero is the **degree**.

- Degree 0: `f(x) = 7`. A constant. Flat line.
- Degree 1: `f(x) = 33 + 22x`. A line, [week 2](w02-linear-functions-and-rates.md).
- Degree 2: `f(x) = 15x − 18.75x²`. A **quadratic**. Its graph is a **parabola**, the U shape (or upside-down U).
- Degree 3: `f(x) = x³`. A **cubic**.

For game design one fact about degree matters most. **For large inputs, the highest-degree term wins.** Double the input and a line doubles, a quadratic roughly quadruples, a cubic roughly multiplies by eight. So the degree of your progression curve decides how much harder level 60 is than level 30. The lower terms only shape the early part of the curve, the same way intercepts did for lines last week.

### Three ways to write a quadratic

A quadratic can be written in three forms. Each one makes a different fact easy to read.

**Standard form.** `f(x) = a·x² + b·x + c`. You read `c` directly as the value at `x = 0`. The sign of `a` tells you which way it opens: positive opens upward (a valley), negative opens downward (a hill).

**Vertex form.** `f(x) = a·(x − p)² + q`. The **vertex**, the top of the hill or bottom of the valley, is at `(p, q)`. For a jump, the vertex is the apex: the highest point, reached at time `p`, at height `q`.

**Factored form.** `f(x) = a·(x − r₁)·(x − r₂)`. The **roots** `r₁` and `r₂` are where the curve crosses zero. For a jump, those are take-off and landing.

The jump in the next section, `y(t) = 15t − 18.75t²`, is the same curve in all three forms:

```
standard:  y = −18.75·t² + 15·t + 0
vertex:    y = −18.75·(t − 0.4)² + 3
factored:  y = −18.75·t·(t − 0.8)
```

Standard form says it starts at 0. Vertex form says it peaks at height 3 at time 0.4. Factored form says it leaves the ground at 0 and lands at 0.8. You will switch forms depending on which question you are asking.

## 2. Worked example: designing a jump from height and time

### The hook

Celeste (2018) is praised for how its jump feels. Its player code was published by the developers, so you can read the rules directly. Two of them break textbook physics on purpose. While you hold the jump button, Madeline's upward speed is held constant for up to 0.2 seconds. And near the top of the jump, when her vertical speed is below 40 pixels per second and you are still holding jump, **gravity is cut in half**.

Why would a designer halve gravity at the top of a jump? And how do you decide on a gravity value in the first place?

Start with the second question. The answer is that you do not pick gravity. You pick what the player sees (how high the jump goes and how long it takes to get there), and gravity falls out of the algebra.

### The model

A character that leaves the ground with upward speed `v₀` and is pulled down by constant gravity `g` has height

```
y(t) = v₀·t − ½·g·t²
v(t) = v₀ − g·t
```

- `t` is time since take-off, in seconds.
- `y` is height above the take-off point, in whatever unit your level uses. This lecture uses **tiles**.
- `v₀` is launch speed, in tiles per second, upward positive.
- `g` is gravity, in tiles per second per second (tiles/s²).
- `v(t)` is the vertical speed at time `t`.

Look at `v(t)`. It is a line from [week 2](w02-linear-functions-and-rates.md), with slope `−g`. Speed drops by the same amount every second. Height, which accumulates that speed, is a quadratic. **A quadratic is what you get when the rate of change is itself a line.**

Now flip the model around. A designer does not think "launch speed 15, gravity 37.5." They think "the jump is 3 tiles high and takes 0.4 seconds to reach the top." Call those `h` (apex height) and `t_h` (time to apex).

At the apex the character stops rising, so `v(t_h) = 0`:

```
0 = v₀ − g·t_h        →   v₀ = g·t_h
```

And the height at the apex is `h`:

```
h = v₀·t_h − ½·g·t_h²  =  g·t_h² − ½·g·t_h²  =  ½·g·t_h²
```

Solve both for the designer's numbers:

```
g  = 2h / t_h²
v₀ = 2h / t_h
```

That pair of lines is the whole worked example. Pittman's 2016 GDC talk derives exactly these two formulas and argues that jumps should be tuned this way. Pick height and time. Compute gravity and launch speed. Never guess.

### Numbers you can check

Take `h = 3` tiles and `t_h = 0.4` s.

```
g  = 2 × 3 / 0.4²  = 6 / 0.16 = 37.5 tiles/s²
v₀ = 2 × 3 / 0.4   = 15 tiles/s
y(t) = 15·t − 18.75·t²
```

Sample it every 0.1 s, the way a game samples it every frame.

| t (s) | y(t) (tiles) | First difference Δy | Second difference Δ²y | v(t) (tiles/s) |
|---|---|---|---|---|
| 0.0 | 0.0000 | — | — | 15.00 |
| 0.1 | 1.3125 | +1.3125 | — | 11.25 |
| 0.2 | 2.2500 | +0.9375 | −0.375 | 7.50 |
| 0.3 | 2.8125 | +0.5625 | −0.375 | 3.75 |
| 0.4 | 3.0000 | +0.1875 | −0.375 | 0.00 |
| 0.5 | 2.8125 | −0.1875 | −0.375 | −3.75 |
| 0.6 | 2.2500 | −0.5625 | −0.375 | −7.50 |
| 0.7 | 1.3125 | −0.9375 | −0.375 | −11.25 |
| 0.8 | 0.0000 | −1.3125 | −0.375 | −15.00 |

Check `t = 0.3`: `15 × 0.3 = 4.5`, `18.75 × 0.09 = 1.6875`, difference 2.8125.

Three things to notice.

- The heights are symmetric around `t = 0.4`. The arc up mirrors the arc down.
- The **first differences** (how far the character moved in each 0.1 s step) fall in a straight line. They are the speed, sampled.
- The **second differences** are all exactly `−0.375`. That constant is `−g·Δt² = −37.5 × 0.01`. A constant second difference is the fingerprint of a quadratic, and section 3 turns it into a tool.

### The visual

Open [`examples/w03-jump-designer.html`](../examples/w03-jump-designer.html). The top panel draws the arc as a character would trace it across the screen. The bottom panel draws vertical speed against time.

Drag the height slider. The arc grows taller and the speed line gets steeper, because `g = 2h / t_h²` grows with `h`. Now drag time-to-apex down from 0.4 to 0.25 while keeping height fixed. The arc stays the same height but gets narrower, and the speed line becomes *much* steeper. Halving `t_h` multiplies gravity by four. This is the source of the common advice that snappy platformers use "unrealistically high gravity." They do not choose high gravity. They choose short air time, and high gravity is the consequence.

The picture that matters is the pair. The arc is curved and hard to reason about. The speed line is straight and easy. Everything a designer might want to change about a jump is a change to that straight line: its starting value, its slope, or a kink in it.

### Cross-game recognition

**Celeste (2018, published player source code).** Read the hook again with the model in hand. The constants are gravity 900 px/s², jump speed 105 px/s, a 0.2 s window in which holding jump keeps the speed at 105, and half gravity (450 px/s²) while vertical speed is below 40 px/s and jump is held. On the speed-time graph that is three straight pieces instead of one: flat for 0.2 s, then a slope of −900 until the speed reaches 40, then a gentler slope of −450 through the apex. The height is three quadratic pieces joined smoothly.

You can compute the height of a fully held jump from those pieces (a simplified model that ignores moving platforms and other special cases):

| Phase | Speed change | Duration | Height gained |
|---|---|---|---|
| Hold (constant speed) | 105 → 105 | 0.200 s | 105 × 0.2 = 21.00 px |
| Full gravity | 105 → 40 | 65/900 ≈ 0.072 s | (105² − 40²) / (2 × 900) ≈ 5.24 px |
| Half gravity | 40 → 0 | 40/450 ≈ 0.089 s | 40² / (2 × 450) ≈ 1.78 px |
| **Total to apex** | | ≈ 0.361 s | ≈ 28.0 px |

Tap the button instead and the hold ends at once, half gravity never applies, and the arc is one plain parabola with apex `105² / (2 × 900) ≈ 6.1` px. Same constants, a jump more than four times higher when held. The half-gravity phase also answers the hook. It lasts about 0.09 s, twice as long as full gravity would take to stop the same 40 px/s, yet it adds less than 1 px of extra height. The designers bought hang time at the top of the arc, where players aim at a ledge or line up a dash, without making the jump noticeably taller.

**Pittman's piecewise arcs (GDC 2016).** The talk generalises Celeste's trick. Design a jump as several parabolic pieces, each with its own gravity, joined where the speed matches. The most common version uses stronger gravity after the apex ("fast falling"). With a fall multiplier `m`, the descent takes `t_h / √m` instead of `t_h`, so the jump spends less time falling than rising. It feels weighty without making the rise sluggish.

**Dungeons & Dragons 3.5 experience table (2003).** The same shape does a completely different job. The experience needed to reach level `n` is 1,000 at level 2, 3,000 at level 3, 6,000 at level 4, and 190,000 at level 20. Take differences: 1,000, 2,000, 3,000. Take differences again: 1,000, 1,000. Constant second differences, so it is a quadratic. It fits `XP(n) = 500·n·(n − 1)` exactly: `500 × 20 × 19 = 190,000`. A jump arc and a level table, one kind of curve.

Wherever something changes at a steady *rate of change* (speed that drops by the same amount each frame, cost per level that rises by the same amount each level), you get a quadratic.

### Design judgment

- **Design from what the player sees.** Height and time to apex are what a level designer can check against a gap on the grid. Gravity and launch speed are implementation details. Keep `h` and `t_h` as the tunable values in your data and compute `g` and `v₀` from them.
- **A pure parabola is symmetric, and that often feels floaty.** Rising and falling take the same time. Most action platformers break the symmetry with a fall multiplier or a variable-height jump. Decide how much, and do not stack three tricks without drawing the speed-time graph first.
- **Every extra piece is a rule players will learn.** Celeste's hold window and half-gravity apex are both discoverable by feel. Speedrunners will find every edge between pieces. Make sure the joins are where you want them.
- **Frame rate is part of the model.** The table used `Δt = 0.1` s and the formula gave exact values. Game code usually adds speed and position step by step each frame, and the simplest version of that (update position with the old speed, then update speed) drifts from the true parabola. Pittman's talk covers this. If your jump height changes when the frame rate changes, this is why.
- **Quadratic cost curves grow faster than players expect.** In the D&D table, level 20 needs 190 times the XP of level 2. That can be right for a tabletop campaign. For a game with fixed XP per monster it means grind rises like `n`. Compare it with the exponential curves of [week 4](w04-exponentials-and-the-xp-curve.md) before choosing.

### Check yourself (worked example)

1. With `h = 3` tiles, `t_h = 0.4` s and a fall multiplier of 3, how long does the descent take, and what is the total air time?
2. For the same jump without a fall multiplier, when is the character 2.5 tiles high on the way down? If it moves sideways at 8 tiles/s, how far from take-off is that?
3. A game runs at 60 frames per second. What is the second difference in height between consecutive frames for the `g = 37.5` jump?

(Answers at the end of the lecture.)

## 3. Differences: reverse-engineering a curve from data

You often meet a game curve as a table, from a wiki, a data mine or your own measurements. Differences tell you its degree without any guessing.

The rule:

- If the **first** differences are constant, the data is linear (degree 1).
- If the **second** differences are constant, it is quadratic (degree 2).
- If the **third** differences are constant, it is cubic (degree 3).

And the constant tells you the leading coefficient. For equally spaced inputs one unit apart, a quadratic `a·n² + ...` has second difference `2a`. A cubic `a·n³ + ...` has third difference `6a`.

### Example: the D&D table

| Level n | XP needed | Δ | Δ² |
|---|---|---|---|
| 1 | 0 | — | — |
| 2 | 1,000 | 1,000 | — |
| 3 | 3,000 | 2,000 | 1,000 |
| 4 | 6,000 | 3,000 | 1,000 |
| 5 | 10,000 | 4,000 | 1,000 |

Second difference 1,000, so `2a = 1,000` and `a = 500`. Now find the rest. At `n = 1` the XP is 0, and at `n = 2` it is 1,000. Try `500·n² + b·n + c`. From `n = 1`: `500 + b + c = 0`. From `n = 2`: `2,000 + 2b + c = 1,000`. Subtract: `1,500 + b = 1,000`, so `b = −500` and `c = 0`. Result: `XP(n) = 500n² − 500n = 500·n·(n − 1)`.

### Example: a cubic

Pokémon's "Medium Fast" experience group, used by many species since the first games, needs `n³` experience points for level `n`. Level 10 needs 1,000. Level 50 needs 125,000. Level 100 needs 1,000,000.

| Level n | n³ | Δ | Δ² | Δ³ |
|---|---|---|---|---|
| 1 | 1 | — | — | — |
| 2 | 8 | 7 | — | — |
| 3 | 27 | 19 | 12 | — |
| 4 | 64 | 37 | 18 | 6 |
| 5 | 125 | 61 | 24 | 6 |

Third difference 6, which is `6a` with `a = 1`. Cubic confirmed.

Now a design question you can answer. At what level is a Medium Fast Pokémon halfway to level 100 in experience? Half of 1,000,000 is 500,000, and `∛500,000 ≈ 79.4`. Level 79 needs 493,039 and level 80 needs 512,000. So the halfway point in effort is around level 80, not level 50. For a cubic, the top fifth of the levels costs half the total. Hold that thought for next week, where an exponential curve pushes the halfway point even closer to the cap.

### A warning about differences

The difference test needs equally spaced inputs. If a wiki lists levels 1, 5, 10, 20, 50, the steps are uneven and the differences mean nothing until you divide by the step sizes. Also, real tables are often rounded to nice numbers. If your second differences are 996, 1,004, 1,000, 998, the curve is a quadratic with rounding noise, not a mystery.

## 4. Solving quadratics: "does the jump reach?"

Many questions about an arc are of the form "when is the height equal to `p`?" That gives a quadratic equation:

```
v₀·t − ½·g·t² = p
½·g·t² − v₀·t + p = 0
```

Any quadratic equation `a·t² + b·t + c = 0` is solved by the **quadratic formula**:

```
t = ( −b ± √(b² − 4ac) ) / (2a)
```

The expression under the square root, `D = b² − 4ac`, is the **discriminant**. It answers the design question before you compute any times:

- `D > 0`: two times. The arc passes height `p` on the way up and again on the way down.
- `D = 0`: one time. Height `p` is exactly the apex.
- `D < 0`: no real time. The arc never reaches `p`. The ledge is too high.

### Worked case: landing on a ledge

Our jump is `y(t) = 15t − 18.75t²`. A ledge's top is 2 tiles high. Solve `18.75t² − 15t + 2 = 0`:

```
D = 15² − 4 × 18.75 × 2 = 225 − 150 = 75
√D ≈ 8.660
t = (15 ± 8.660) / 37.5    →   t ≈ 0.169 s  or  t ≈ 0.631 s
```

The character passes 2 tiles on the way up at 0.169 s and comes back down to 2 tiles at 0.631 s. With a horizontal speed of 8 tiles/s those times are 1.35 and 5.05 tiles from take-off. Between those two distances the character is at or above ledge height. A ledge whose near edge lies inside that window can be landed on. A ledge that starts beyond 5.05 tiles cannot, because the character has already dropped below its top. Level designers turn this window into a rule for gap sizes.

Now raise the ledge to 3.5 tiles:

```
D = 225 − 4 × 18.75 × 3.5 = 225 − 262.5 = −37.5
```

Negative. The jump cannot reach it, and you knew that without solving for `t`, because the apex is 3.

The discriminant is `v₀² − 2g·p`, which is zero exactly when `p = v₀² / (2g)`. That is another way of writing the apex height, `h = v₀² / (2g)`. Check: `15² / 75 = 3`. Algebra agrees with the table.

## 5. Choosing a degree on purpose

Put the three curves you now know side by side, each scaled so that level 1 needs 0 and level 20 needs 190,000 (the D&D total).

| Level | Linear `10,000·(n − 1)` | Quadratic `500·n·(n − 1)` | Cubic scaled to match at 20 |
|---|---|---|---|
| 2 | 10,000 | 1,000 | 166 |
| 5 | 40,000 | 10,000 | 2,945 |
| 10 | 90,000 | 45,000 | 23,729 |
| 15 | 140,000 | 105,000 | 80,143 |
| 20 | 190,000 | 190,000 | 190,000 |

The cubic column is `190,000 × (n³ − 1) / (20³ − 1)`, rounded. Check level 10: `190,000 × 999 / 7,999 ≈ 23,729`.

Same endpoint, very different journeys. The linear curve makes level 2 cost as much as level 19. The cubic makes the first ten levels almost free and puts seven eighths of the effort in the second half. The quadratic sits between. None is right in general. The degree is a decision about where you want players to spend their time.

## In-class activity (25 minutes)

Pairs. Graph paper or a spreadsheet, plus the interactive.

1. **Design on paper.** Draw a level segment: a 4-tile gap, then a ledge 2 tiles higher than the take-off point. Choose a jump height `h`, time to apex `t_h` and horizontal speed that clear it with a little margin.
2. **Compute.** Find `g` and `v₀`. Use the quadratic formula to find when the arc comes back down to 2 tiles, and how far sideways that is. Does the character land on the ledge?
3. **Tune the feel.** Add a fall multiplier of 2. Recompute the descent time. Does the character still clear the gap? If not, change one number and explain which.
4. **Check in the interactive.** Enter your values and screenshot the arc with your ledge marked.

Expected output: a one-page sheet with your drawing, the four numbers, the quadratic-formula working, and the screenshot.

## Common misconceptions

- **"Higher gravity makes the jump lower."** Only if you keep launch speed fixed. If you design from height and time, higher gravity comes from a shorter time to apex, and the height is whatever you chose.
- **"A curve that rises faster and faster must be exponential."** Quadratics and cubics also rise faster and faster. Take differences. Constant second differences mean quadratic. Exponential curves have constant *ratios*, next week.
- **"The quadratic formula always gives two answers."** Only when the discriminant is positive. A negative discriminant is the formula telling you the height is out of reach.
- **"Celeste's jump is a parabola."** A tapped jump is. A held jump is three parabolic pieces with different gravity. Most shipped platformers use pieces.

## Check yourself

1. Design a jump that rises 4 tiles in 0.5 s. What are `g` and `v₀`?
2. You shorten the time to apex from 0.4 s to 0.3 s and keep `h = 3`. By what factor does gravity change? What is the new launch speed?
3. If the D&D 3.5 formula `500·n·(n − 1)` were extended past level 20, what is the first level needing at least 1,000,000 XP?
4. A mystery table reads 0, 3, 12, 27, 48 for levels 1 to 5. What degree is it, and what is its formula?
5. Using the Celeste constants, what is the apex height of a tapped jump (no hold, no half gravity)? How much higher is the fully held jump, as a ratio?

<details>
<summary>Answers</summary>

Worked-example questions:

1. Descent time `0.4 / √3 ≈ 0.231` s. Total air time `0.4 + 0.231 ≈ 0.631` s.
2. Solve `18.75t² − 15t + 2.5 = 0`. `D = 225 − 187.5 = 37.5`, `√D ≈ 6.124`. On the way down, `t = (15 + 6.124) / 37.5 ≈ 0.563` s. Sideways: `8 × 0.563 ≈ 4.51` tiles.
3. `−g·Δt² = −37.5 × (1/60)² = −37.5 / 3,600 ≈ −0.0104` tiles per frame per frame.

End-of-lecture questions:

1. `g = 2 × 4 / 0.25 = 32` tiles/s². `v₀ = 2 × 4 / 0.5 = 16` tiles/s.
2. Gravity scales with `1 / t_h²`, so the factor is `(0.4 / 0.3)² ≈ 1.78`. New `g = 6 / 0.09 ≈ 66.7` tiles/s². New `v₀ = 6 / 0.3 = 20` tiles/s.
3. Need `n·(n − 1) ≥ 2,000`. `45 × 44 = 1,980` is short. `46 × 45 = 2,070` is enough. Level 46.
4. Differences 3, 9, 15, 21. Second differences 6, 6, 6. Quadratic with `2a = 6`, `a = 3`. It is 0 at level 1, which suggests `3·(n − 1)²`. Check level 5: `3 × 16 = 48`. Correct.
5. Tapped: `105² / (2 × 900) = 11,025 / 1,800 ≈ 6.1` px. Held: about 28.0 px. Ratio about 4.6.

</details>

## Lab hook

**Lab 03: Jump designer.** You implement the jump from `h` and `t_h` in a small script or spreadsheet that steps the physics frame by frame, compare the stepped heights with the exact quadratic, add a fall multiplier, and reverse-engineer the degree of three game data tables. See [`labs/lab03.md`](../labs/lab03.md).

## Sources

- Celeste player constants: Celeste source code, `Player.cs`, published by the developers on GitHub (repository NoelFB/Celeste; the game shipped in 2018). Gravity 900, MaxFall 160, JumpSpeed −105 (negative is up), VarJumpTime 0.2, HalfGravThreshold 40; gravity multiplier 0.5 while `|Speed.Y| < 40` and jump is held. The height table in section 2 is this lecture's simplified model built from those constants, not a measured value from the game.
- Pittman, J. K. (2016). "Math for Game Programmers: Building a Better Jump." Game Developers Conference. Slides on GDC Vault. Derives `g = 2h / t_h²` and `v₀ = 2h / t_h`, piecewise gravity for fast falling and variable height, and integration error.
- Dungeons & Dragons 3.5 experience table: System Reference Document 3.5 (2003), "Experience and Level-Dependent Benefits." 1,000 XP for level 2, 3,000 for level 3, 6,000 for level 4, 190,000 for level 20.
- Pokémon Medium Fast experience group: Bulbapedia, "Experience" (all main-series generations). Experience for level `n` is `n³`, 1,000,000 at level 100.
- Dunn, F. & Parberry, I. (2011). *3D Math Primer for Graphics and Game Development*, 2nd ed. CRC Press. Chapter 1.

## Interactive spec: examples/w03-jump-designer.html

**The one insight the visual must make obvious:** the curved arc is controlled entirely by a straight speed line. Designers pick height and time; gravity and launch speed follow from `g = 2h/t_h²` and `v₀ = 2h/t_h`. Shortening time to apex makes the speed line much steeper while the arc keeps its height.

**Layout.** Two linked panels stacked vertically on all widths (they share the time axis):
- Top: "Arc". Height (tiles) against horizontal distance (tiles), drawn on a tile grid (1 tile = 1 grid square), with a small generic square for the character at the current time.
- Bottom: "Vertical speed". Speed (tiles/s) against time (s). Align it with the top panel so that time `t` sits directly below horizontal distance `vx·t`. A horizontal zero line is labelled "apex".

**Controls** (keyboard operable, numeric readouts):
- Apex height `h`: slider 0.5 to 8 tiles, step 0.1, default 3.
- Time to apex `t_h`: slider 0.15 to 0.8 s, step 0.01, default 0.4.
- Fall multiplier `m`: slider 1 to 4, step 0.1, default 1.
- Horizontal speed `vx`: slider 2 to 15 tiles/s, step 0.5, default 8.
- Ledge height `p`: slider 0 to 8 tiles, step 0.1, default 2. Drawn as a horizontal dashed line on the arc panel.
- Time scrubber `t`: slider 0 to total air time, default `t_h`. Moves the character and a marker on the speed line.
- Preset button "Celeste model (px)": switches units to pixels and plots the three-piece held jump plus the tapped jump as a faint line (see below). A second click returns to the designer mode.

**Readouts:** `g`, `v₀`, rise time, fall time `t_h/√m`, total air time, horizontal distance `vx × total`, and for the ledge: discriminant `D = v₀² − 2·g·p` and the one or two crossing times and distances (use rise gravity for the crossing on the way up; for the crossing on the way down use `t = t_h + √(2(h − p)/(m·g))`). If `p > h` show "ledge out of reach (D < 0)".

**Formulas (designer mode).**
```
g  = 2*h / th^2
v0 = 2*h / th
rise (0 ≤ t ≤ th):         y = v0*t − 0.5*g*t^2         v = v0 − g*t
fall (th < t ≤ th + th/√m): y = h − 0.5*m*g*(t − th)^2    v = −m*g*(t − th)
x = vx * t
```

**Differences table** below the panels: sample `t = 0, Δt, 2Δt, ...` to landing, with columns t, y, Δy, Δ²y, v. A selector for `Δt` = 0.1 s or 1/60 s (1/60 shows only the first 12 rows plus a "show all" toggle). Values to four decimals.

**Celeste preset (px, px/s, px/s²).** Upward positive. Held jump:
```
phase 1: 0 ≤ t ≤ 0.2           v = 105, y = 105 t
phase 2: until v = 40          v = 105 − 900 (t − 0.2)          (duration 65/900 s)
phase 3: until v = 0           v = 40 − 450 (t − t2)             (duration 40/450 s)
descent after apex: full gravity 900 (not held), capped at fall speed 160
```
Tapped jump: `v = 105 − 900 t` from take-off, full gravity throughout. Label the preset "model built from published constants; the game has more rules".

**Test values.**
| Setting | Expected |
|---|---|
| h=3, th=0.4 | g = 37.5, v0 = 15 |
| h=3, th=0.4, t=0.3 | y = 2.8125, v = 3.75 |
| h=3, th=0.4, Δt=0.1 | every Δ²y = −0.3750 |
| h=3, th=0.4, m=3 | fall time 0.2309, total 0.6309 |
| h=3, th=0.4, m=1, p=2, vx=8 | D = 75; t = 0.1691 and 0.6309; x = 1.352 and 5.048 |
| h=3, th=0.4, p=3.5 | D = −37.5, "out of reach" |
| h=4, th=0.5 | g = 32, v0 = 16 |
| Celeste held | apex ≈ 28.01 px at t ≈ 0.3611 s |
| Celeste tapped | apex ≈ 6.125 px at t ≈ 0.1167 s |

No Celeste art, character sprite, fonts or logo. Draw the character as a plain rounded square. Colours: arc in ochre, speed line in steel, ledge in blood red, grid in the palette's grid token.

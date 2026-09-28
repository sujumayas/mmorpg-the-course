# MA101 · Lab 08: Remap everything

**Week:** 8 ([Interpolation: lerp, inverse lerp and remap](../lectures/w08-interpolation-lerp-inverse-lerp-remap.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** in pairs

## Objective

Write your own `lerp`, `inverseLerp`, `remap` and piecewise-lerp functions, prove them with tests, and use them to drive a landing squash and a damage-falloff readout. Then measure frame-rate-dependent smoothing and fix it.

## Starter materials

- Any programming language or game engine you know (Python with pygame, Godot, Unity or a browser page with JavaScript are all fine). Do not use the engine's built-in lerp or remap functions for Parts A to C. You may compare against them at the end.
- The Celeste landing constants from lecture section 2: `FastMaxFall = 240`, squash scales `lerp(1, 1.6, t)` and `lerp(1, 0.4, t)`, recovery rate 1.75 per second.
- The test table from lecture section 2 (landing speeds 0, 60, 120, 160, 200, 240, 300).
- A plain rectangle sprite 40 × 60 px. No game characters.

## Steps

### Part A: the functions and their tests (35 minutes)

1. Write `lerp(a, b, t)`, `inverseLerp(a, b, v)`, `remap(v, inA, inB, outA, outB)` and `clampedRemap(...)`. `remap` must call the other two, not repeat their arithmetic.
2. Make `inverseLerp` handle `a == b` without dividing by zero. Decide what it returns and write the reason in a comment.
3. Write at least ten tests, including every row of the lecture's landing table, `inverseLerp(10, 50, 70) = 1.5`, a remap with a backwards output range, and the `a == b` case.

### Part B: squash on landing (30 minutes)

4. Drop the rectangle from three heights with simple gravity, record the landing speed, and apply the Celeste squash with a clamped remap. Recover the scale toward 1 at 1.75 per second with an `approach` function built from `min` and `max`.
5. Print landing speed, `t`, both scales and the recovery time on each landing. Check one landing against the lecture's numbers by hand.
6. Add a toggle for "keep area" (`scaleY = 1 / scaleX`) and describe the difference in feel in two sentences.

### Part C: keyed curve (25 minutes)

7. Write `evaluateKeys(keys, x)` that takes a sorted list of `(x, y)` keys and returns a piecewise-lerp value, clamping outside the first and last key.
8. Use it for damage falloff with keys `(0, 1.5)`, `(512, 1.0)`, `(1024, 0.5)`. Print the multiplier at 0, 256, 512, 900 and 1,400. Then add a key of your choice to bend the curve, and state in one sentence what changed for players at mid range.

### Part D: smoothing across frame rates (at home)

9. Make a camera value follow a target that jumps from 0 to 100, with `x = lerp(x, target, 0.1)` every frame. Run a fixed-step simulation (no real rendering needed) at 30, 60 and 144 fps and record the gap after 0.25 s, 0.5 s and 1 s.
10. Repeat with `k = 6 × dt` and with `k = 1 − exp(−6 × dt)`. Put all nine results in one table.
11. Write at most 250 words explaining the table, including why the last method matches at every frame rate. Name one place in a game you know where the first method would cause a visible bug.

## Deliverable

Your source code with passing tests, a 30-second screen recording of Parts B and C running, and the Part D table and write-up as a PDF.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Core functions and tests (25%) | All four functions correct, `remap` composed from the others, zero-width range handled and justified, ten or more meaningful tests passing | Correct, a few tests thin | A function wrong or tests missing | Missing |
| Landing squash (20%) | Matches lecture numbers, clamp works above 240, recovery uses `approach`, keep-area toggle and feel described | Works, one element missing | Squash wrong or unclamped | Missing |
| Keyed curve (20%) | Correct piecewise lerp with clamped ends, printed values right, added key explained in player terms | Correct, explanation thin | Wrong segment chosen at some inputs | Missing |
| Smoothing table (20%) | All nine values correct, clear table | One method wrong | Only fixed-k measured | Missing |
| Write-up (15%) | Explains exponential decay and names a concrete bug | Explanation right, no example | Describes numbers without explaining | Missing |

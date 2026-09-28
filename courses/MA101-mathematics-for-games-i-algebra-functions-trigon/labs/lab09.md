# MA101 · Lab 09: An easing library and a juicy menu

**Week:** 9 ([Easing curves for animation feel](../lectures/w09-easing-curves-for-animation-feel.md))
**Time:** one 2-hour lab session plus up to 3 hours at home
**Work:** individually

## Objective

Build a small easing library from three rules (a power ease-in, `Invert` and `Follow`), test it against the lecture's tables, then use it to animate a four-element game menu. Tune eases and durations so the menu feels responsive, and defend every choice with the slope reasoning from lecture.

## Starter materials

- The lerp and inverse lerp functions you wrote in Lab 08. If yours are broken, rebuild them from the one-line formulas in [week 8, section 1](../lectures/w08-interpolation-lerp-inverse-lerp-remap.md): `lerp(a, b, t) = a + (b − a) × t` and `inverseLerp(a, b, v) = (v − a) / (b − a)`.
- Any engine or language that can draw rectangles and text each frame.
- Lecture tables for positions at `t = 0.1, 0.25, 0.5, 0.75` and the start, middle and end speeds.
- A menu mock-up: a title bar, three buttons and a tooltip panel, all plain rectangles. No game logos or art.

## Steps

### Part A: the library (40 minutes)

1. Write `quadIn`, `cubeIn` and `backIn(t) = t²(2.70158t − 1.70158)`.
2. Write `invert(ease)` returning `t → 1 − ease(1 − t)` and `follow(first, second)` returning the piecewise in-out from lecture section 2. Build all Out and InOut eases from these two functions, not by writing their formulas directly.
3. Add `smoothstep(t) = 3t² − 2t³` and a custom `powerOut(p)` that returns `t → 1 − (1 − t)^p`.
4. Write a test that checks every ease at `t = 0` and `t = 1`, and every value in the lecture's position table to three decimals.
5. Write `speed(ease, t)` that estimates the slope with `(ease(t + h) − ease(t − h)) / 2h`, clamping the sample points to `[0, 1]`. Check it against the lecture's speed table.

### Part B: a tween system (30 minutes)

6. Write a `Tween` that stores start value, end value, start time, duration and ease, and returns its value for any current time using `lerp(a, b, ease(clamp(inverseLerp(start, start + duration, now), 0, 1)))`.
7. Show that your tween reaches exactly the end value on the last frame at 30, 60 and 144 fps.

### Part C: the menu (at home)

8. Animate the menu opening: title drops in, buttons slide in one after another, tooltip fades in on hover. Choose an ease and duration for each element.
9. Add a "reduce motion" option that shortens every duration to at most 0.05 s. Check the final layout is identical.
10. Record two versions: your tuned menu, and the same menu with every ease set to linear and the same durations.
11. Write at most 300 words. For each element, state the ease, the duration and the fraction of the motion visible by frame 2 at 60 fps. Apply the two questions from lecture (responds to input? arriving or leaving?) and justify any exception.

## Deliverable

Source code with passing tests, the two recordings (tuned and linear, 10 seconds each) and the write-up as a PDF.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Library built from rules (25%) | All eases correct, Out and InOut built only with `invert` and `follow`, tests match lecture values | Correct, one ease written by hand | Values wrong for some eases | Missing |
| Speed estimate (15%) | Matches the lecture speed table including endpoints | Correct except at endpoints | Wrong method | Missing |
| Tween system (15%) | Exact end value at all three frame rates, time-based not frame-counted | Works at 60 fps only | Drifts or overshoots end | Missing |
| Menu feel (25%) | Clear improvement over linear in recording, player-triggered elements respond immediately, reduce-motion works | Improvement visible, one element sluggish | Little difference from linear | Missing |
| Justification (20%) | Every choice argued with numbers from the library and the two questions | Most choices argued | Taste only | Missing |

# MA101 · Week 09 — Easing Curves for Animation Feel

**Why this matters:** Two menus slide in over the same distance in the same time. One feels crisp and one feels sluggish, and the only difference is a curve you cannot see. Easing curves are that curve. They are a few lines of algebra each, and choosing the right one is most of what people mean when they say a game "feels good."

**You will be able to:**
- Compute eased positions with `lerp(a, b, E(t))` for linear, quadratic, cubic, in-out and smoothstep eases.
- Derive an ease-out from an ease-in with the invert rule, and an in-out ease as a piecewise function.
- Read start and end speed from an easing curve, and predict how an ease will feel before you run it.
- Choose and justify an ease and a duration for a given game event.

**Before class:** Robert Penner, "Motion, Tweening, and Easing," chapter 7 of *Robert Penner's Programming Macromedia Flash MX* (McGraw-Hill/Osborne, 2002), pp. 191 to 240; the chapter is free as a PDF on the author's site. Read the sections on tweening and on quadratic and cubic easing; skip the ActionScript details. Optional: watch Jonasson and Purho, "Juice it or lose it" (2012 talk, about 15 minutes).

**Prerequisites from earlier courses:** MA101 has no prerequisite course. This week uses polynomials from [MA101 week 3](w03-polynomials-and-quadratic-curves.md), piecewise functions from [MA101 week 7](w07-piecewise-caps-and-floors.md), and lerp, inverse lerp and remap from [MA101 week 8](w08-interpolation-lerp-inverse-lerp-remap.md).

**Interactive:** [examples/w09-easing-race.html](../examples/w09-easing-race.html). Keep it open during section 2.

---

## 1. From lerp to tween

Last week you moved values with `lerp(a, b, t)`. To animate something over time, you let `t` be time, turned into a fraction with inverse lerp:

```
t = clamp(inverseLerp(startTime, startTime + duration, now), 0, 1)
value = lerp(a, b, t)
```

This is a **tween** (from "in-between"): a value that goes from `a` to `b` over a fixed duration. With plain lerp, the value moves at constant speed. It starts at full speed, stops dead at the end, and covers the same distance in every frame.

Real objects do not move like that. They speed up from rest and slow down before stopping. Plain linear tweens look mechanical, and players read that as cheap even when they cannot say why.

An **easing function** fixes this by bending `t` before you lerp:

```
value = lerp(a, b, E(t))
```

`E` is a function from `[0, 1]` to numbers, with two rules:

- `E(0) = 0`, so the tween starts at `a`.
- `E(1) = 1`, so the tween ends at `b`.

Between those points, `E` can do anything. The duration and the endpoints stay exactly the same. Only the timing inside changes. That is why easing is such a cheap tool: you can change the feel of an animation without touching its start, end or length.

The simplest non-linear ease is `E(t) = t²`. At `t = 0.5` (half the time) it returns `0.25`, so the object has covered only a quarter of the distance. It starts slowly and finishes fast. That is an **ease-in**: the motion eases in from rest.

## 2. Worked example: Celeste's 0.16-second pickup

### The hook

In Celeste (Maddy Makes Games, 2018), Madeline can pick up certain objects and carry them overhead. When she grabs one, it swings from where it was to above her head. That move lasts 0.16 seconds, under ten frames at 60 frames per second. You would think nobody could see the timing inside ten frames.

The developers disagreed. The published player code creates the pickup as a tween with `Ease.CubeInOut` over `0.16` seconds, moving the object along a short curve. Someone chose a specific easing curve for a movement that lasts a sixth of a second. This section shows what that curve does, and why its effect is visible even at that length.

### The model

Celeste's engine, Monocle, builds its whole easing library from a few simple functions and two rules. The same structure appears in Penner's 2002 equations and in most tween libraries since.

**Ease-in** of power `n`:

```
In_n(t) = tⁿ          (n = 2 quad, n = 3 cubic)
```

**Ease-out** is an ease-in played backwards and upside down, which Monocle calls `Invert`:

```
Out(t) = 1 − In(1 − t)
```

**Ease-in-out** runs the ease-in for the first half of the time and the ease-out for the second half, each squeezed into half the time and half the distance. Monocle calls this `Follow`. It is a piecewise function, straight from week 7:

```
            ⎧ In(2t) / 2               if t ≤ 0.5
InOut(t) =  ⎨
            ⎩ Out(2t − 1) / 2 + 0.5    if t > 0.5
```

So for the cubic case:

- `CubeIn(t) = t³`
- `CubeOut(t) = 1 − (1 − t)³`
- `CubeInOut(t) = 4t³` for `t ≤ 0.5`, and `1 − 4(1 − t)³` for `t > 0.5`

Check the breakpoint of `CubeInOut`. At `t = 0.5` the first piece gives `4 × 0.125 = 0.5`, and the second gives `1 − 4 × 0.125 = 0.5`. Continuous.

### Reading speed from the curve

Plot `E(t)` against `t` and the **slope** of the curve is the object's speed, as a multiple of the average speed. Slope 1 means "moving at the average speed of the whole tween" (the speed linear would have). Slope 3 means three times average. Slope 0 means momentarily stopped.

You can estimate slope with two nearby samples, the rise over the run from week 2. For `t³` near the end: `E(1) − E(0.99) = 1 − 0.970299 = 0.0297`, over a run of 0.01, gives a slope of about 2.97. The exact value is 3. For `tⁿ` in general, the speed starts at 0 and ends at `n`. The invert rule swaps these: an ease-out of power `n` starts at speed `n` and ends at 0.

### Numbers you can check

Position (fraction of the distance covered) at five moments:

| t (fraction of time) | Linear | QuadIn t² | QuadOut | CubeOut | CubeInOut | Smoothstep |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 0.1 | 0.100 | 0.010 | 0.190 | 0.271 | 0.004 | 0.028 |
| 0.25 | 0.250 | 0.063 | 0.438 | 0.578 | 0.063 | 0.156 |
| 0.5 | 0.500 | 0.250 | 0.750 | 0.875 | 0.500 | 0.500 |
| 0.75 | 0.750 | 0.563 | 0.938 | 0.984 | 0.938 | 0.844 |
| 1 | 1 | 1 | 1 | 1 | 1 | 1 |

Speed (slope) at the start, middle and end:

| Ease | Start speed | Middle speed | End speed |
|---|---|---|---|
| Linear | 1 | 1 | 1 |
| QuadIn | 0 | 1 | 2 |
| QuadOut | 2 | 1 | 0 |
| CubeOut | 3 | 0.75 | 0 |
| CubeInOut | 0 | 3 | 0 |
| Smoothstep | 0 | 1.5 | 0 |

(Smoothstep is `3t² − 2t³`, a gentler in-out that you will meet again in section 4.)

Check two by hand. QuadOut at 0.25: `1 − (0.75)² = 1 − 0.5625 = 0.4375`. CubeInOut at 0.75 uses the second piece: `1 − 4 × (0.25)³ = 1 − 4 × 0.015625 = 0.9375`.

Now apply it to Celeste's 0.16 s pickup at 60 fps. Each frame advances `t` by `(1/60) / 0.16 ≈ 0.104`:

| Frame | t | CubeInOut: fraction of the path | CubeOut, for comparison |
|---|---|---|---|
| 0 | 0 | 0.000 | 0.000 |
| 1 | 0.104 | 0.005 | 0.281 |
| 2 | 0.208 | 0.036 | 0.504 |
| 3 | 0.313 | 0.122 | 0.675 |
| 4 | 0.417 | 0.289 | 0.802 |
| 5 | 0.521 | 0.560 | 0.890 |
| 6 | 0.625 | 0.789 | 0.947 |
| 7 | 0.729 | 0.921 | 0.980 |
| 8 | 0.833 | 0.981 | 0.995 |
| 9 | 0.938 | 0.999 | 1.000 |
| 10 | 1 | 1.000 | 1.000 |

(This assumes a steady 60 fps and that the tween samples at these moments. The exact frame bookkeeping inside the engine may differ by a frame.)

Read the middle column. On frames 1 and 2 the object barely moves, under 4% of the path. Frames 4, 5 and 6 together carry two thirds of the trip, from 12% to 79%. Then it settles. Even in ten frames, the eye catches that pattern as "lifted, swung, placed." The linear version would move the same 10% every frame and read as "teleported slowly."

Now read the right-hand column. A cube ease-out covers half the distance by frame 2. If the pickup used that ease, the object would seem to leap to Madeline's hands. Same duration, same path, different verb.

### The visual

Open [`examples/w09-easing-race.html`](../examples/w09-easing-race.html). The top view shows three or more dots racing across the screen, one per ease, all starting and finishing together. The bottom-left view plots each ease as `E(t)` against `t`. The bottom-right plots their speed (slope) against `t`.

Scrub the time slider. On the race track, the dots look like "different personalities." On the speed plot you see why: the ease-out dot's speed starts at 3 and falls, the ease-in dot's starts at 0 and climbs, the in-out dot's is a hill with its peak in the middle. The areas under all the speed curves are equal, because every dot covers the same distance in the same time. Easing never changes how far or how long. It only moves speed around within the tween.

Press "Frames" and the scrubber snaps to Celeste's ten frames, with the table's numbers beside each dot.

### Cross-game recognition

**Celeste, other effects.** The same player code uses `Ease.QuadOut` for the screen-distortion bursts on dashes and landings, and a sine in-out, `Ease.SineInOut`, for flying along a curve in one sequence. Monocle's full list (Sine, Quad, Cube, Quint, Expo, Back, Big Back, Elastic and Bounce, each in In, Out and InOut forms) is built from just the "In" versions plus `Invert` and `Follow`.

**Flash games and Robert Penner's equations (2001 to 2002).** Penner published a set of easing equations for Flash that spread through web and game development. His chapter names eight "flavours" (linear, quadratic, cubic, quartic, quintic, sinusoidal, exponential and circular), each with in, out and in-out forms. The names "QuadOut" and "CubeInOut" in Monocle, and in most tween libraries, trace back to this set.

**The web (CSS, used by browser games and many game launchers and store pages).** A CSS transition has a timing function. The default, called `ease`, is defined as a cubic Bézier curve with control points `(0.25, 0.1)` and `(0.25, 1)`. It starts slowly, speeds up sharply and then settles for a long time. It is an asymmetric in-out: more "out" than "in." Every browser ships this ease as the default for any transition that does not choose one.

**GLSL shaders (OpenGL Shading Language).** The built-in `smoothstep(edge0, edge1, x)` is defined as `t = clamp((x − edge0) / (edge1 − edge0), 0, 1)` followed by `t² × (3 − 2t)`. Read that with this course's vocabulary: a clamped inverse lerp (week 8) followed by an in-out easing curve. Shader programmers use it for soft edges, fades and glows, where the input is a distance or a brightness rather than time.

**Team Fortress 2 (Valve, 2007 onward).** Last week you saw that TF2's damage distance modifier passes through 1.5, 1.0 and 0.5 at 0, 512 and 1,024 units. The official wiki describes the curve between them as cubic. That is a remap from distance to damage with a non-linear shape in the middle, an easing curve with distance playing the role of time.

Five contexts, one formula: `lerp(a, b, E(inverseLerp(start, end, input)))`. Time, distance or brightness in, a shaped fraction in the middle, any output range out.

### Design judgment

The slope table is your design tool. Ask two questions of every animation:

1. **Does the motion respond to the player's input?** If yes, it needs speed at the start. Use an ease-out. A button press that triggers an ease-in feels laggy, because for the first frames almost nothing happens. That is added input latency, even if your code responds on the same frame. Jumps, dashes, menu opens and hit reactions all want motion right away.
2. **Is the object leaving or arriving?** Material Design 3, Google's interface guidelines, recommends a decelerating ease (an ease-out) for elements that enter the screen and come to rest, and an accelerating ease (an ease-in) for elements that leave the screen without stopping. Leaving at full speed reads as "gone for good." Arriving and slowing reads as "here, and staying."

Celeste's pickup uses an in-out, which breaks rule 1. Is that a mistake? No. The pickup is not the player's feedback. Madeline's grab animation plays immediately, and the object's swing is secondary motion that follows the grab. An in-out makes it look like a physical object with weight being lifted and placed. That is the trade-off to decide deliberately. **The thing the player controls should respond instantly. The things that react to it can have weight.**

Other judgments to make on purpose:

- **Duration and ease interact.** A strong ease-out makes a 0.3 s animation feel faster than a linear 0.2 s one, because most of the distance happens early. If a menu feels slow, try a stronger ease-out before shortening it.
- **Stronger is not always better.** Higher powers (quint, expo) concentrate the motion into a smaller slice of time. At short durations, that slice can become one frame, which reads as a pop, not a motion.
- **Respect players who turn motion off.** Many platforms offer a "reduce motion" setting. Honour it by shortening or removing non-essential tweens. The final state must still be correct, which it will be, since `E(1) = 1`.

### Check yourself (worked example)

1. Using `QuadOut`, what fraction of the distance does an object cover in the first 20% of the time? Using `QuadIn`?
2. A dash lasts 0.2 s and covers 96 px with `CubeOut`. How far has the character moved after 0.05 s? What is their speed at the start, in pixels per second? (Average speed is distance divided by duration.)
3. Write `QuintOut(t)` using the invert rule, and state its start and end speeds.

<details>
<summary>Answers</summary>

1. `QuadOut(0.2) = 1 − 0.8² = 0.36`, so 36% of the distance. `QuadIn(0.2) = 0.04`, so 4%.
2. `t = 0.05/0.2 = 0.25`, `CubeOut(0.25) = 0.578`, so `0.578 × 96 ≈ 55.5` px. Average speed is `96/0.2 = 480` px/s, and CubeOut starts at 3× average, so 1,440 px/s.
3. `QuintOut(t) = 1 − (1 − t)⁵`. Start speed 5, end speed 0.

</details>

## 3. Beyond 0 and 1: overshoot and bounce

The rules `E(0) = 0` and `E(1) = 1` say nothing about the values in between. An ease can go past 1 on the way and come back. That is **overshoot**, and it reads as springy or elastic.

Monocle's `BackIn` is `t² × (2.70158t − 1.70158)`. It dips below zero first, like winding up before a throw. Its lowest value is about −0.100 at `t ≈ 0.42`. The strange constant 1.70158 is chosen so that the dip is almost exactly 10% of the distance. `BackOut`, built with the invert rule, goes the other way: it overshoots to about 1.100 at `t ≈ 0.58`, then settles back to 1.

| t | 0.1 | 0.25 | 0.5 | 0.58 | 0.75 | 0.9 | 1 |
|---|---|---|---|---|---|---|---|
| BackOut(t) | 0.409 | 0.817 | 1.088 | 1.100 | 1.064 | 1.014 | 1 |

A button that pops in with `BackOut` swells 10% past its size and settles. That small overshoot is one of the cheapest bits of "juice" you can add. In their 2012 talk "Juice it or lose it," Jonasson and Purho rebuilt a plain Breakout clone live on stage, and tweened blocks with springy eases were among the first changes that made it feel alive.

Two warnings. Overshoot means values outside `[a, b]`. If you tween a colour channel, an alpha or a health bar with `BackOut`, you briefly get values past the legal range. Clamp the output, or do not use overshoot on those. And if you tween a position with overshoot next to a wall, the object will clip into the wall for a few frames.

**Bounce** eases are piecewise, like the in-out rule. Monocle's `BounceOut` is four parabola pieces joined end to end, each smaller than the last, imitating a ball dropped on the floor. It is week 3's quadratic, used four times, stitched together with week 7's piecewise definition.

## 4. Smoothstep and building your own

Sometimes you want a gentle in-out with no power to choose. **Smoothstep** is `S(t) = 3t² − 2t³`. It starts and ends at speed 0 and peaks at speed 1.5 in the middle, softer than CubeInOut's peak of 3. It is one polynomial, not piecewise, so it is cheap and has no breakpoint to get wrong.

You can design your own ease with any function that meets `E(0) = 0` and `E(1) = 1`. Three quick recipes:

- **Mix two eases.** `E(t) = lerp(Linear(t), QuadOut(t), m)` with `m` between 0 and 1 gives a "slightly eased" curve. At `m = 0.5` and `t = 0.25`, `E = 0.5 × 0.25 + 0.5 × 0.4375 = 0.344`.
- **Power as a dial.** `Out(t) = 1 − (1 − t)^p` with `p` any positive number, not only integers. Designers can tune `p = 2.5` in a data file.
- **Keys and curves.** Engine curve editors let you place keys and drag tangents (handles that set the slope at each key). Behind the scenes these are usually cubic curves like CSS's Bézier ease. The start and end speeds you set with the handles are the slopes you learned to read in section 2.

Whatever you build, test its endpoints, check whether it overshoots, and read its start speed against the "does it respond to input?" rule.

## 5. Easing is not smoothing

Last week ended with lerp smoothing, `x = lerp(x, target, k)` every frame. People often call that "easing," but it is a different tool.

| | Easing tween | Lerp smoothing |
|---|---|---|
| Knows its start, end and duration | Yes | No, only the current value and the target |
| Ends exactly at the target | Yes, at `t = 1` | Never, it approaches forever |
| Target can move mid-way | Awkward, you restart the tween | Natural, it follows |
| Shape | Any curve you pick | Always exponential decay, fastest at the start |
| Frame-rate safe | Yes, if `t` comes from real time | Only with `k = 1 − e^(−λ dt)` |

Use a tween for authored, one-off motion: a menu opening, a pickup, a card flipping. Use smoothing for following something that keeps moving: a camera, a health bar catching up with damage. Many games use both on one element, for example a smoothed camera that also plays a tweened zoom.

## In-class activity (30 minutes)

Groups of three. Each group gets a scenario card (below) and must choose an ease and a duration, then defend it.

- A. The inventory panel slides in from the right when the player presses I.
- B. A damage number floats up from an enemy and fades out.
- C. A treasure chest lid opens after the player holds a button for 1 second.
- D. The camera pans from the player to a boss door that just unlocked, then back.

For your scenario:

1. Pick an ease from sections 2 to 4 and a duration in seconds. Write `E(t)`.
2. Compute the position at frames 1, 2 and the middle frame at 60 fps. Say what fraction of the motion is visible by frame 2.
3. Apply the two questions from the design judgment: does it respond to input, and is it arriving or leaving? Does your choice follow the rules? If not, justify the exception, as Celeste's pickup does.
4. Try the interactive's "custom" mode with your ease and duration and write one sentence on whether it felt as you predicted.

Expected output: one card per group with the ease, duration, frame numbers and justification. Two groups present.

## Common misconceptions

- **"Easing changes how long an animation takes."** Duration is fixed by `inverseLerp` on time. Easing only redistributes speed inside that duration.
- **"Ease-in means the animation feels smooth at the start, so it's always the nice one."** Ease-in starts at speed 0. On anything triggered by the player, that reads as input lag.
- **"An eased value stays between a and b."** Only if `E` stays in `[0, 1]`. Back and elastic eases overshoot on purpose.
- **"`lerp(x, target, 0.1)` every frame is an ease-out."** It is exponential smoothing. It has no duration, never finishes, and depends on frame rate unless corrected. See section 5.

## Check yourself

1. Compute `CubeInOut(0.4)` and `CubeInOut(0.8)`. Which piece of the definition does each use?
2. Prove that `Out(t) = 1 − In(1 − t)` always satisfies `Out(0) = 0` and `Out(1) = 1` if `In` does.
3. A UI toast uses smoothstep over 0.4 s to slide 120 px. Where is it after 0.1 s, and after 0.2 s?
4. A designer says "the dash feels floaty." It uses QuadInOut over 0.25 s. Suggest a change that keeps the distance and duration, and use the slope table to explain why it helps.

<details>
<summary>Answers</summary>

1. `0.4 ≤ 0.5`, so the first piece: `4 × 0.4³ = 4 × 0.064 = 0.256`. `0.8 > 0.5`, so the second piece: `1 − 4 × 0.2³ = 1 − 0.032 = 0.968`.
2. `Out(0) = 1 − In(1) = 1 − 1 = 0`. `Out(1) = 1 − In(0) = 1 − 0 = 1`.
3. At 0.1 s, `t = 0.25`, `S = 3(0.0625) − 2(0.015625) = 0.15625`, so about 18.8 px. At 0.2 s, `t = 0.5`, `S = 0.5`, so 60 px.
4. Switch to QuadOut or CubeOut. QuadInOut starts at speed 0, so the dash hangs for the first frames after the press. QuadOut starts at speed 2 and CubeOut at 3, so the dash covers 44% or 58% of its distance in the first quarter of the time, and it reads as a burst.

</details>

## Lab hook

**Lab 09, An easing library and a juicy menu.** Implement In, Out (by `Invert`) and InOut (by `Follow`) for quad, cubic and back eases, test them against this lecture's tables, then tune the eases and durations of a four-element game menu and defend your choices. See [labs/lab09.md](../labs/lab09.md).

## Sources

- NoelFB/Celeste repository on GitHub, `Source/Player/Player.cs` (published 2018; MIT licence covers the code files only). Pickup tween `Tween.Create(…, Ease.CubeInOut, .16f, …)`; `Ease.QuadOut` for displacement bursts; `Ease.SineInOut` along a flight curve.
- Monocle engine (Matt Thorson), open source and linked from the Celeste repository; GitHub mirror `monocle-engine`, file `Monocle/Util/Ease.cs`. Definitions of `QuadIn`, `CubeIn`, `Invert`, `Follow`, `BackIn` with constants 2.70158 and 1.70158, and the four-piece `BounceOut`. The open-source version may differ in details from the one shipped in Celeste.
- Penner, R. (2002). "Motion, Tweening, and Easing." Chapter 7 of *Robert Penner's Programming Macromedia Flash MX*, McGraw-Hill/Osborne, pp. 191 to 240. PDF on robertpenner.com.
- MDN Web Docs, "`<easing-function>`." The CSS `ease` keyword equals `cubic-bezier(0.25, 0.1, 0.25, 1)`.
- Khronos Group, OpenGL 4 reference page `smoothstep`. Definition with a clamped inverse lerp followed by `t × t × (3 − 2t)`.
- Official TF2 Wiki, "Damage" (retrieved September 2026). Distance modifier endpoints and its cubic shape.
- Google, Material Design 3, "Easing and duration." Decelerating ease for elements entering and resting, accelerating ease for elements exiting.
- Jonasson, M. & Purho, P. (2012). "Juice it or lose it." Conference talk, recording in the GDC Vault and on YouTube. Live-juicing of a Breakout clone, including tweened blocks.

## Interactive spec: examples/w09-easing-race.html

**Insight the visual must make obvious:** every ease covers the same distance in the same time, and the difference is where the speed goes. On the race track the dots look like different personalities. On the speed plot the reason is plain: ease-out spends its speed at the start, ease-in at the end, in-out in the middle, and the area under every speed curve is the same.

**Layout.** Three views, linked by one time value `t`.

- View A, "Race": horizontal lanes, one per selected ease, each with a dot moving from x = 0 to x = 1 (scaled to the lane width). Dots start and end together. Faint tick marks under each lane show the dot's position at every frame of the current frame mode, so the spacing of frames is visible.
- View B, "Position": `E(t)` against `t` for the selected eases, 0 to 1 on both axes, y-axis extended to −0.15 and 1.15 so back eases fit. A vertical line at the current `t`.
- View C, "Speed": the slope of each ease against `t`, y-axis 0 to 5 (extend to include negative values when a back ease is selected). A vertical line at the current `t`. Label: "1 = average speed. Equal areas: same distance, same time."

On mobile, stack A above B above C.

**Controls.**
- Checkboxes for which eases race (default Linear, QuadOut, CubeInOut): Linear, QuadIn, QuadOut, CubeIn, CubeOut, CubeInOut, QuadInOut, Smoothstep, BackOut.
- Time slider `t` (0 to 1, step 0.001) and a Play button that runs the race over a duration from a "Duration (s)" input (default 0.16, range 0.05 to 2). Under `prefers-reduced-motion`, Play steps `t` in visible 0.1 jumps instead of animating smoothly.
- Toggle "Frames at 60 fps": snaps `t` to `k × (1/60) / duration` for integer `k`, clamped to 1. With duration 0.16 this gives frames 0 to 10. Left and right arrow keys step one frame.
- "Custom" row: a power slider `p` (0.5 to 6, step 0.1) and a type selector In, Out or InOut, which adds a lane for `t^p`, `1 − (1 − t)^p`, or the `Follow` form of `t^p`.
- Readout table beside the views: for each selected ease, `E(t)` to 3 decimals and speed to 2 decimals at the current `t`.

**Exact formulas.**
- Linear `t`. QuadIn `t²`. CubeIn `t³`. Out forms by `Out(t) = 1 − In(1 − t)`. InOut forms by `Follow`: `In(2t)/2` for `t ≤ 0.5`, else `Out(2t − 1)/2 + 0.5`. Smoothstep `3t² − 2t³`. BackIn `t²(2.70158t − 1.70158)`, BackOut `1 − BackIn(1 − t)`.
- Speeds, exact: Linear 1. QuadIn `2t`. QuadOut `2(1 − t)`. CubeIn `3t²`. CubeOut `3(1 − t)²`. CubeInOut `12t²` for `t ≤ 0.5`, else `12(1 − t)²`. QuadInOut `4t` for `t ≤ 0.5`, else `4(1 − t)`. Smoothstep `6t − 6t²`. BackOut `3 × 2.70158 × (1 − t)² − 2 × 1.70158 × (1 − t)`. Custom In `p t^(p−1)`, Out `p(1 − t)^(p−1)`.

**Test values.** QuadOut(0.25) = 0.438. CubeOut(0.25) = 0.578. CubeInOut(0.25) = 0.063, (0.75) = 0.938. Smoothstep(0.25) = 0.156. BackOut(0.5) = 1.088, maximum ≈ 1.100 at t ≈ 0.58. Speeds: CubeInOut at 0.5 → 3.00; Smoothstep at 0.5 → 1.50; CubeOut at 0 → 3.00. Frame mode with duration 0.16: frame 2 → t 0.208, CubeInOut 0.036, CubeOut 0.504; frame 5 → t 0.521, CubeInOut 0.560.

**Constraints.** Plain dots and lines only. No game art, characters or logos. Name games only in the caption text.

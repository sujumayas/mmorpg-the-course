# MA101 · Week 12 — 2D Vectors: Add, Scale, Magnitude, Normalize

**Why this matters:** Position, velocity, aim direction, knockback and the arrow from an enemy to you are all the same kind of object, a 2D vector. Four operations on it cover most movement code you will ever write, and forgetting one of them, normalize, has shipped a speed bug in games for over thirty years.

**You will be able to:**
- Add, subtract and scale 2D vectors, and say what each result means in a game.
- Compute a vector's magnitude and normalize it, including the zero-vector case.
- Explain and compute why un-normalized diagonal input is about 41% faster, and fix it.
- Choose between normalizing and clamping the length of analog input, and justify the choice.

**Before class:** Dunn & Parberry, *3D Math Primer for Graphics and Game Development* (2nd ed., 2011), chapter 2 (vectors), sections on vector addition, scalar multiplication, magnitude and normalization. Freya Holmér, *Math for Game Devs*, part 1, the segments on vectors and normalization.

**Prerequisites from earlier courses:** [MA101 week 10, angles, radians, sin and cos](w10-angles-radians-sin-cos.md) and [MA101 week 11, atan2 and turning toward a target](w11-atan2-turning-toward-a-target.md). [MA101 week 7, piecewise functions, caps and floors](w07-piecewise-caps-and-floors.md) for clamps.

**Interactive:** [examples/w12-diagonal-movement.html](../examples/w12-diagonal-movement.html). Keep it open during section 5.

---

## 1. One object, many jobs

A **vector** in 2D is a pair of numbers, written `v = (x, y)`. The numbers are its **components**. You can picture it as an arrow: start anywhere, move `x` to the right and `y` up (or down, in a y-down screen), and the arrow points from where you started to where you ended.

An arrow has two properties that matter: which way it points (its **direction**) and how long it is (its **magnitude**). A vector carries both at once. That is why games use vectors for so many things.

| Game quantity | As a vector | What the direction means | What the length means |
|---|---|---|---|
| Position | (320, 180) | from the world origin to the object | how far from the origin |
| Displacement | target − self | which way the target is | how far away it is |
| Velocity | (4, −3) units/s | which way the object moves | its speed |
| Aim or facing | (0.8, 0.6) | where it looks | always 1 (a unit vector) |
| Knockback impulse | (−120, 40) | which way you get shoved | how hard |

Two warnings about this table. First, a position and a displacement are both pairs of numbers, but they are not the same kind of thing. Adding two positions ("my house plus your house") means nothing. Adding a displacement to a position ("my house plus three blocks north") gives a new position. Keep track of which is which, and many bugs disappear. Second, the facing row has length 1 on purpose. Section 4 explains why.

## 2. Adding and subtracting

### Addition

Add vectors component by component:

```
(a, b) + (c, d) = (a + c, b + d)
```

As arrows: put the second arrow's tail on the first arrow's head. The sum goes from the first tail to the second head. This is how movement works every frame:

```
position = position + velocity × dt
```

It is also how you combine influences. A character walking right at `(5, 0)` on a conveyor belt pushing up at `(0, 2)` moves at `(5, 2)`. Wind, currents, knockback and input all add. Order does not matter: `u + v = v + u`.

### Subtraction

Subtract the same way:

```
(a, b) − (c, d) = (a − c, b − d)
```

You used subtraction last week. `target − self` is the displacement from self to target, the arrow you fed into `atan2`. Keep the rule "to minus from": the vector from A to B is `B − A`.

| Self | Target | target − self | Meaning |
|---|---|---|---|
| (2, 3) | (8, 3) | (6, 0) | 6 units to the right |
| (2, 3) | (2, −1) | (0, −4) | 4 units down (y-up world) |
| (2, 3) | (5, 7) | (3, 4) | up and right, 5 units away |

## 3. Scaling

Multiply a vector by a plain number, called a **scalar**, and you multiply each component:

```
k × (x, y) = (k x, k y)
```

The arrow keeps its line but gets `k` times longer. Some cases worth naming:

- `k = 2` doubles the length, same direction.
- `k = 0.5` halves it.
- `k = −1` flips it to point the other way. Knockback is often `−1 ×` the direction to the attacker, or simply `self − attacker`.
- `k = 0` gives the **zero vector** `(0, 0)`, which has length 0 and no direction at all.

Scaling is how you set a speed. If `d` is a direction of length 1 and `s` is a speed, then `s × d` is a velocity of speed `s` in direction `d`. That separation of "which way" from "how fast" is the most useful habit in movement code, and the rest of this lecture is about what happens when you skip it.

## 4. Magnitude and normalizing

### Magnitude

The length of `v = (x, y)` comes from Pythagoras. The components are the two short sides of a right triangle, and the arrow is the long side:

```
|v| = sqrt(x² + y²)
```

`|(3, 4)| = sqrt(9 + 16) = 5`. `|(1, 1)| = sqrt(2) = 1.414`. `|(0, 0)| = 0`.

The distance between two points is the magnitude of their difference, `|B − A|`. [MA101 week 14](w14-distances-ranges-and-squared-distance.md) builds on this and shows how to skip the square root when you only need to compare distances.

### Normalizing

A **unit vector** is a vector of length 1. It is a pure direction. To **normalize** a vector, divide it by its own length:

```
normalize(v) = v / |v| = (x / |v|, y / |v|)
```

The result points the same way and has length exactly 1. Check it: `normalize((3, 4)) = (0.6, 0.8)`, and `sqrt(0.36 + 0.64) = 1`.

You have already met unit vectors without the name. The point `(cos θ, sin θ)` on the unit circle from week 10 is always a unit vector, because `cos²θ + sin²θ = 1`. So there are two ways to build a direction: from an angle with `(cos θ, sin θ)`, or from any arrow by normalizing. Going from a unit vector back to an angle is `atan2(y, x)` from week 11. The three weeks form a loop.

### The zero vector trap

`normalize((0, 0))` divides by zero. Depending on the language you get `NaN` (not a number), infinity, an exception or a silent `(0, 0)`. A `NaN` is the worst case. It spreads into every value it touches, so one bad frame can turn a character's position into `NaN` and make it vanish from the world.

Always guard it:

```
len = |v|
if len > tiny: dir = v / len
else:          dir = (0, 0)       // or keep the last facing
```

In movement code the zero vector is common. It is what you get when the player presses nothing, or presses left and right together.

## 5. Worked example: the diagonal movement bug

### The hook

In Doom (1993), players discovered that holding "forward" and "strafe" together moves you faster than holding "forward" alone. The community calls it straferunning, and speedrunners use it constantly. The most extreme form, called SR50, moves you at about 141% of normal running speed.

The same bug appears in countless student projects and more than a few shipped games: press W and D together and your character crosses the room noticeably faster than pressing W alone. Where does the extra speed come from, and why is the number always close to 41%?

### The model

Most keyboard movement code reads four keys and builds an input vector:

```
input = (right − left, up − down)       each key is 0 or 1
velocity = speed × input
```

With one key held, `input` is something like `(0, 1)`, of length 1. With two perpendicular keys held, it is `(1, 1)`, of length:

```
|(1, 1)| = sqrt(1² + 1²) = sqrt(2) = 1.4142
```

So the character moves `sqrt(2)` times as fast on the diagonal. The extra is `sqrt(2) − 1 = 0.4142`, about 41%. That is where the number comes from. It is Pythagoras, and it will be the same in every game that makes this mistake, whatever its speed.

The fix is to separate direction from speed, as section 3 recommended:

```
velocity = speed × normalize(input)      (with the zero guard)
```

Now every non-zero input has length 1, and the character moves at `speed` in all eight directions.

### Numbers you can check

Let `speed = 5` units per second.

| Keys held | input | Length | Raw velocity | Raw speed | Normalized velocity | Normalized speed |
|---|---|---|---|---|---|---|
| W | (0, 1) | 1.000 | (0, 5) | 5.00 | (0, 5) | 5.00 |
| D | (1, 0) | 1.000 | (5, 0) | 5.00 | (5, 0) | 5.00 |
| W + D | (1, 1) | 1.414 | (5, 5) | 7.07 | (3.54, 3.54) | 5.00 |
| S + A | (−1, −1) | 1.414 | (−5, −5) | 7.07 | (−3.54, −3.54) | 5.00 |
| W + S | (0, 0) | 0.000 | (0, 0) | 0.00 | (0, 0) by guard | 0.00 |

Check the W + D row: `(1, 1) / 1.414 = (0.707, 0.707)`, times 5 is `(3.54, 3.54)`, and `sqrt(3.54² + 3.54²) = 5.00`.

Now feel the size of the effect. Take a square room 100 units on a side and walk from one corner to the opposite one. The diagonal is `100 × sqrt(2) = 141.4` units long.

| Route | Distance | Time, raw input | Time, normalized input |
|---|---|---|---|
| Straight along one wall | 100.0 | 20.0 s | 20.0 s |
| Corner to corner, diagonal | 141.4 | 20.0 s | 28.3 s |
| Along two walls (an L) | 200.0 | 40.0 s | 40.0 s |

With the bug, crossing the room corner to corner takes exactly as long as walking along one wall. The diagonal is "free". Every player who figures that out will zigzag through your levels, and every chase your AI designers tuned with straight-line speeds will be off by 41%.

### Move it yourself

Open [`examples/w12-diagonal-movement.html`](../examples/w12-diagonal-movement.html). On the left, two identical characters race from the same start: one uses raw input, the other normalized input. Hold two arrow keys (or tap the on-screen pad) and watch the raw one pull ahead on diagonals and stay level on straight lines. On the right is the input diagram: the eight possible input vectors drawn as arrows from the center, with a unit circle behind them. In raw mode the four diagonal arrows poke out past the circle to the corners of a square. Switch to normalized and they snap back onto the circle.

The two views show the same fact twice. The race shows the effect. The diagram shows the cause: raw keyboard input lives on a square, and speed should live on a circle.

### Cross-game recognition

**Doom (1993).** id Software's released source makes the numbers exact. Walking adds a forward component of 25 (hex `0x19`) and a sideways component of 24 (`0x18`). Running uses 50 (`0x32`) and 40 (`0x28`). The movement code then thrusts the player along their facing angle by the forward amount and along the angle 90° to the side by the sideways amount, so the two add as perpendicular vectors, exactly like `(1, 1)`. The game clamps each component separately at 50, which is a square limit, not a circle.

| Doom input | Forward | Side | Speed = sqrt(f² + s²) | Relative to forward only |
|---|---|---|---|---|
| Walk forward | 25 | 0 | 25.0 | 1.00× |
| Walk forward + strafe | 25 | 24 | 34.7 | 1.39× |
| Run forward | 50 | 0 | 50.0 | 1.00× |
| Run forward + strafe (SR40) | 50 | 40 | 64.0 | 1.28× |
| Run + two strafe inputs (SR50) | 50 | 50 (clamped) | 70.7 | 1.41× |

SR50 works because the engine adds sideways input from more than one control (the strafe key and the turn key with strafe held) before the clamp. The sideways total goes past 50 and gets clipped to 50, giving the full `sqrt(2)` diagonal.

**Quake (1996).** Quake's released source takes the opposite approach. The client sets forward speed 200 and sideways speed 350 by default (both doubled when running), then the server computes the length of the wished-for velocity and, if it is longer than `sv_maxspeed` (default 320), scales the whole vector down to length 320. That is a clamp on the magnitude, a circle limit.

| Quake input (walking) | Forward | Side | Length | After clamp to 320 |
|---|---|---|---|---|
| Forward | 200 | 0 | 200.0 | 200.0 |
| Strafe | 0 | 350 | 350.0 | 320.0 |
| Forward + strafe | 200 | 350 | 403.1 | 320.0 |

On the ground, no key combination in Quake gives you more than 320. Same formula as our fix, three years after Doom.

**Unity and Godot.** Modern engines build the fix into their input systems. In Unity's Input System, a 2D Vector composite bound to four keys defaults to the mode `DigitalNormalized`, which normalizes the resulting vector. Godot's `Input.get_vector` returns a vector whose length is limited to 1. If you read four keys yourself instead of using these helpers, you get the bug back.

Four games and engines, one idea: the length of the input vector is the speed multiplier, so decide what that length should be.

### Eyes-open design judgment

Normalizing is the right default. It is not a law.

- **Doom kept its fast diagonal, and players built a culture on it.** Straferunning is part of Doom's skill ceiling. If you ship a movement exploit and players love it, removing it later is a design change, not a bug fix. Decide early.
- **Square versus circle is the real choice.** Doom clamps each axis (a square). Quake clamps the length (a circle). A square limit always gives diagonals `sqrt(2)` more speed. A circle limit gives every direction the same top speed. There is no third option hiding here, only these two shapes and blends of them.
- **Grid and pixel-art games have a special case.** If a character moves one tile per step and a diagonal step counts as one step, diagonals cover `sqrt(2)` times the distance per step. Some games want that. If you do not, you must make diagonal steps cost more time, or disallow them.
- **Normalizing analog input is a mistake.** Section 6 explains. Use it for digital keys, clamp the length for sticks.

## 6. Analog sticks: normalize or clamp?

A gamepad stick gives you an input vector with any length from 0 to about 1, where the length tells you how far the player pushed. Half tilt should mean half speed.

If you normalize stick input, every non-zero tilt becomes length 1. A gentle push to sneak becomes a full sprint. That is the digital fix applied where it destroys information.

The right tool for analog input is to **clamp the length**, which is what Quake does to its wish velocity and what Godot's `get_vector` does:

```
len = |input|
if len > 1: input = input / len     // only shrink, never grow
```

| Stick input | Length | Normalize | Clamp length to 1 |
|---|---|---|---|
| (0.5, 0) | 0.50 | (1.00, 0) full speed | (0.50, 0) half speed |
| (0.3, 0.4) | 0.50 | (0.60, 0.80) full speed | (0.30, 0.40) half speed |
| (0.9, 0.9) | 1.27 | (0.71, 0.71) | (0.71, 0.71) |
| (1, 0) | 1.00 | (1, 0) | (1, 0) |

The third row matters. Some controllers report values near `(0.9, 0.9)` or even `(1, 1)` at a full diagonal push, because the physical gate or the driver lets the stick reach the corners of a square. Clamping catches that case and leaves every gentler input alone. For keyboards, clamping and normalizing give the same result, because digital input only has lengths 0, 1 and 1.414. So "clamp the length to 1" is the one rule that works for both.

A dead zone, the small region near the center where input is ignored, is a separate step you apply before this. It belongs to the controls work in UX201.

## In-class activity (25 minutes)

Pairs, paper or a spreadsheet.

1. **Audit (8 min).** Here is movement pseudocode from a student project:
   ```
   dir = (0, 0)
   if key(W): dir.y += 1
   if key(S): dir.y -= 1
   if key(A): dir.x -= 1
   if key(D): dir.x += 1
   if sprint: dir = dir * 1.5
   pos += dir * 4 * dt
   ```
   List every distinct speed the character can move at, with the keys that produce it. How many are there?
2. **Fix (7 min).** Rewrite it so walking is always 4 units/s, sprinting is always 6 units/s, and no key combination produces `NaN`. Show the result for W + D + sprint.
3. **Analog (5 min).** The same game adds gamepad support. Write the two-line rule you would use for stick input and compute the speed for stick `(0.2, 0.6)` while sprinting.
4. **Judgment (5 min).** A designer asks to keep the fast diagonal "because speedrunners will like it". Write three sentences: one on what it breaks in level design, one on what it adds, and your recommendation.

Expected output: a speed list (task 1 has four distinct non-zero speeds: 4, 5.66, 6 and 8.49), fixed pseudocode, one worked stick value and a three-sentence recommendation.

## Common misconceptions

- **"Pressing two keys adds their speeds, so diagonal is twice as fast."** The components add, the speeds do not. `(1, 0) + (0, 1)` has length 1.414, not 2. The extra is 41%.
- **"Normalize everything."** Normalizing analog input throws away how far the player pushed. Clamp the length to 1 instead, which leaves short vectors alone.
- **"Normalizing is always safe."** The zero vector has no direction, and dividing by its length gives `NaN` or an error. Guard it.
- **"A position plus a position is a position."** Adding two positions has no meaning. Position plus displacement is a position, and position minus position is a displacement.

## Check yourself

1. A character moves at 6 units/s using raw keyboard input. What is its speed when holding up and right? How long does it take to cover a 30-unit diagonal compared with a normalized character?
2. Normalize `(−5, 12)`. Check that your answer has length 1.
3. A game builds keyboard input as `(±1, ±1)` and then clamps each axis separately to at most 0.8. What is the diagonal speed relative to straight movement?
4. A stick reports `(0.6, 0.8)`. Give the velocity at speed 10 under raw, normalize and clamp-length rules. Which rules agree, and why?
5. In Doom, compute the speed of walking forward while strafing as a percentage increase over walking forward, from the source values 25 and 24.

<details>
<summary>Answers</summary>

1. Raw speed `6 × sqrt(2) = 8.49` units/s. 30 units take `30 / 8.49 = 3.54 s` raw and `30 / 6 = 5.00 s` normalized.
2. `|(−5, 12)| = sqrt(25 + 144) = 13`, so the unit vector is `(−5/13, 12/13) = (−0.385, 0.923)`. Check: `0.148 + 0.852 = 1.000`.
3. Straight movement is `(0.8, 0)` after the clamp, length 0.8. Diagonal is `(0.8, 0.8)`, length `0.8 × sqrt(2) = 1.131`. Ratio `1.131 / 0.8 = 1.414`. A per-axis clamp is a square limit, so the diagonal stays 41% faster.
4. `|(0.6, 0.8)| = 1`. Raw gives `(6, 8)`. Normalize gives `(6, 8)`. Clamp gives `(6, 8)`. All three agree because the input already has length 1, so none of them changes it.
5. `sqrt(25² + 24²) = sqrt(1201) = 34.66`. `34.66 / 25 = 1.386`, about 38.6% faster.

</details>

## Lab hook

**Lab 12: A movement controller you can trust.** You build a top-down character controller with keyboard and simulated stick input, log its speed in all directions, and demonstrate the bug and both fixes with a speed-by-direction plot. The brief is in [Lab 12](../labs/lab12.md). Your `Vec2` class carries into [week 13](w13-dot-product-facing-and-vision-cones.md), where the dot product turns it into a guard's vision cone.

## Sources

- id Software, DOOM source code (linuxdoom-1.10, released 1997), github.com/id-Software/DOOM. `g_game.c`: `forwardmove[2] = {0x19, 0x32}`, `sidemove[2] = {0x18, 0x28}`, per-axis clamp to `MAXPLMOVE` (`forwardmove[1]`, 50), strafe input from keys, turn keys with strafe held and mouse adding before the clamp. `p_user.c`: `P_Thrust` along the facing angle for forward and along `angle − ANG90` for sideways movement.
- Doom Wiki (doomwiki.org), "Straferunning" and "SR-50 automation", retrieved September 2026. Community names SR40 and SR50, with SR40 at 128% and SR50 at 141% of normal running speed. Both figures also follow directly from the `g_game.c` values above: `sqrt(50² + 40²) / 50 = 1.28` and `sqrt(50² + 50²) / 50 = 1.41`.
- id Software, Quake source code (WinQuake, released 1999), github.com/id-Software/Quake. `cl_input.c`: `cl_forwardspeed` 200, `cl_sidespeed` 350, `cl_movespeedkey` 2.0. `sv_user.c`: wish velocity scaled down to `sv_maxspeed` when longer. `sv_phys.c`: `sv_maxspeed` default 320.
- Unity Technologies, Input System package manual, "Action Bindings", 2D Vector composite modes (`DigitalNormalized` default). Input System 1.11, accessed September 2026.
- Godot Engine documentation, `Input.get_vector` (length limited to 1, circular dead zone). Godot 4.x stable docs, accessed September 2026.
- Dunn, F. & Parberry, I. (2011). *3D Math Primer for Graphics and Game Development* (2nd ed.). CRC Press. Chapter 2.
- Holmér, F. *Math for Game Devs* (lecture series, YouTube, 2022).

## Interactive spec: examples/w12-diagonal-movement.html

**The one insight:** raw keyboard input lives on a square, so diagonal inputs are `sqrt(2) = 1.414` long and move 41% faster; normalizing (or clamping length) puts every direction on the unit circle. Show it as two linked views: a race where the effect is visible, and an input diagram where the cause is visible.

**Layout.** Left (or top on mobile): "Race" panel. Right (or below): "Input space" panel. Readouts under both.

- **Race.** A square arena, 100 × 100 model units, drawn to fit. Two generic circles start at the bottom-left corner: A "raw" and B "normalized", in two token colors plus labels. Both follow the same input. Each leaves a trail. A "corner to corner" button runs both on input (1, 1) and shows arrival times. A "one wall" button runs input (1, 0).
- **Input space.** Axes from −1.6 to 1.6. The unit circle drawn faintly and the square `|x| ≤ 1, |y| ≤ 1` drawn faintly. The eight digital inputs drawn as arrows from the origin. The currently held input highlighted. In "raw" mode the diagonal arrows end at the square's corners; in "normalized" and "clamp length" modes they end on the circle. Label the length of the highlighted arrow.
- **Analog stick mode.** A toggle replaces the eight arrows with a draggable stick knob (pointer and arrow keys) that can reach anywhere in the square `[−1, 1]²`. Show three dots for the resulting vector under raw, normalize and clamp-length rules, each labeled with its length.

**Controls.** Arrow keys or WASD move both racers (arena must be focusable; show an on-screen 8-way pad for touch). Mode selector for the input diagram: raw / normalize / clamp length. Speed slider 1 to 10 units/s, default 5. Reset button.

**Readouts.** Current input vector, its length, raw velocity and speed, normalized velocity and speed, clamp-length velocity and speed, and the ratio raw/normalized speed. Race times to two decimals.

**Formulas.** `input = (right − left, up − down)`; `raw = s × input`; `norm = |input| > 1e-6 ? s × input / |input| : (0, 0)`; `clamp = |input| > 1 ? s × input / |input| : s × input`.

**Test values.**

- `s = 5`, input (1, 1): raw (5.00, 5.00) speed 7.07; normalized (3.54, 3.54) speed 5.00; ratio 1.414.
- Input (0, 0): all three give (0, 0); no NaN anywhere in the UI.
- Corner to corner, 141.4 units: raw 20.00 s, normalized 28.28 s. One wall, 100 units: both 20.00 s.
- Stick (0.5, 0): raw and clamp speed 2.50, normalize speed 5.00. Stick (0.9, 0.9): raw speed 6.36, normalize and clamp speed 5.00.

**Accessibility.** Keyboard-only use must work end to end. `prefers-reduced-motion`: race results appear as computed times and final trails, without animation. Palette from `templates/interactive-tokens.css`; racers differ by shape or label as well as color. Draw generic circles only, no game art.

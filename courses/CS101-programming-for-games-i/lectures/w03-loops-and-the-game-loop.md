# CS101 · Week 03 — Loops: The Game Loop Concept

**Why this matters:** Every real-time game is one loop that never stops. Read input, update the world, draw it, repeat. How often that loop runs, and how much work each pass does, sets the speed of everything in the game. In 1978 that fact turned Space Invaders' hardware limit into its difficulty curve.

**You will be able to:**
- Write `while` and `for` loops, including loops that end on a condition or a `break`, and trace them by hand.
- Build a text adventure turn loop and explain how it differs from a real-time game loop.
- Compute how fast a quantity changes when it moves a fixed amount per loop pass, given the loop rate and the work per pass.
- Critique frame-counted game logic and say when it is safe and when it breaks.

**Before class:** Robert Nystrom, *Game Programming Patterns* (2014), chapter "Game Loop" (free at gameprogrammingpatterns.com), up to and including the section on running as fast as you can. Python Tutorial, sections 4.2 "for Statements", 4.3 "The range() Function" and 4.4 "break and continue Statements".

**Prerequisites from earlier courses:** [CS101 week 1, programs, variables and types](w01-programs-variables-and-types.md) (state as variables). [CS101 week 2, conditionals](w02-conditionals-room-transitions-and-win-lose.md) (the read, change, check turn structure and win/lose chains). [MA101 week 2, linear functions and rates](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w02-linear-functions-and-rates.md) (speed as a rate) and [MA101 week 6, rational functions](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w06-rational-functions-and-asymptotes.md) comes later this semester and studies the `c / N` curve you meet in section 4. You do not need it first.

**Interactive:** [One alien per frame](../examples/w03-invaders-loop.html). Keep it open during section 4.

---

## 1. Repeating yourself on purpose

Last week's cave program read one command and stopped. To keep a game going you need the program to run the same lines again and again. That is a **loop**.

### `while`: repeat while a condition holds

```python
lamp_oil = 10

while lamp_oil > 0:
    print(f"The lamp flickers. Oil left: {lamp_oil}")
    lamp_oil = lamp_oil - 3

print("Darkness.")
```

Output:

```
The lamp flickers. Oil left: 10
The lamp flickers. Oil left: 7
The lamp flickers. Oil left: 4
The lamp flickers. Oil left: 1
Darkness.
```

Python checks the condition, runs the indented block, then goes back and checks again. When the condition is `False` it skips to the first line after the block. Each pass through the block is an **iteration**.

Trace it with a table, the most useful habit you will build this week:

| Iteration | `lamp_oil` at check | Condition | Printed |
|---|---|---|---|
| 1 | 10 | True | Oil left: 10 |
| 2 | 7 | True | Oil left: 7 |
| 3 | 4 | True | Oil left: 4 |
| 4 | 1 | True | Oil left: 1 |
| — | −2 | False | Darkness. |

Notice the condition is `> 0`, not `!= 0`. Oil goes 10, 7, 4, 1, −2. It never equals 0, so `while lamp_oil != 0` would run forever. That is last week's overkill lesson in a new place.

An **infinite loop** is a loop whose condition never becomes `False`. Sometimes that is a bug. In a game it is often the plan. Stop a runaway program with Ctrl+C.

### `for`: repeat for each item

When you know how many times to repeat, use `for` with `range`:

```python
total = 0
for level in range(1, 6):
    total = total + level * 100
print(total)   # 1500
```

`range(1, 6)` produces 1, 2, 3, 4, 5. It stops *before* 6. `range(5)` produces 0 to 4. That "stop before" rule causes the most common loop bug in every language, the **off-by-one error**, where a loop runs one time too many or too few. When you write a range, say the first and last values out loud and check them.

This loop is also an example of an **accumulator**, a variable that starts empty and collects a result across iterations. Score totals, damage over time and XP sums are all accumulators.

### `break` and `continue`

`break` leaves the loop at once. `continue` skips the rest of this iteration and goes back to the check.

```python
for turn in range(1, 101):
    if turn % 10 != 0:
        continue            # only act on every 10th turn
    print(f"Turn {turn}: a bat flies past.")
    if turn == 30:
        break               # leave early
```

This prints turns 10, 20 and 30, then stops.

## 2. The turn loop: a text adventure that keeps going

Wrap last week's read, change, check turn in a `while` loop and the cave becomes a game you can play until you win, lose or quit.

```python
room = "entrance"
has_key = False
moves = 0
playing = True

while playing:
    command = input(f"[{room}] > ").strip().lower()
    moves = moves + 1

    # Change the state
    if command == "quit":
        playing = False
    elif room == "entrance" and command == "north":
        room = "hall"
    elif room == "hall" and command == "take key":
        has_key = True
        print("You pick up a rusty key.")
    elif room == "hall" and command == "east" and has_key:
        room = "vault"
    elif room == "hall" and command == "east":
        print("The vault door is locked.")
    elif room == "hall" and command == "south":
        room = "entrance"
    else:
        print("Nothing happens.")

    # Check the outcome once per turn
    if room == "vault":
        print(f"You found the treasure in {moves} moves. You win!")
        playing = False
    elif moves >= 20:
        print("Your lamp dies. Game over.")
        playing = False
```

The variable `playing` is a **flag**, a boolean that controls the loop. Any branch can end the game by setting it to `False`. You could use `break` instead. A flag is easier to extend, because the loop still finishes its current turn before it stops.

This is a **turn loop**. The line `input(...)` **blocks**. The program stops and waits, for a second or an hour, until the player presses Enter. Nothing in the world moves while it waits. That is correct for a text adventure or a chess program. It is wrong for anything where the world moves on its own.

## 3. The game loop

Nystrom's "Game Loop" chapter describes the pattern that almost every real-time game uses:

```python
while running:
    process_input()   # look at the keyboard and controller, don't wait
    update()          # move everything one small step
    render()          # draw the new state
```

Three differences from the turn loop:

1. **Input does not block.** The loop checks whether a key is down right now, and moves on either way. Enemies keep moving while you think.
2. **Each pass is one frame.** A **frame** is one iteration of the loop, ending in one drawn picture. **Frame rate** is how many frames run per second (fps). At 60 fps, each frame has a budget of `1000 / 60 ≈ 16.7` milliseconds for input, update and drawing together.
3. **Update moves things a small amount.** The world changes a little every frame, and the illusion of motion comes from doing it many times a second.

Python's terminal cannot read keys without blocking unless you use a library, so here is a game loop without input. It moves one ship across the screen at a steady 60 frames per second.

```python
import time

FPS = 60
x = 0
frame = 0

while x < 40:
    # update
    x = x + 1
    frame = frame + 1
    # render
    print(" " * x + ">", end="\r")
    # wait for the rest of this frame's 1/60 s
    time.sleep(1 / FPS)

print(f"\nArrived after {frame} frames, about {frame / FPS:.2f} s.")
```

The ship moves 1 character per frame, so its speed is `1 × 60 = 60` characters per second. The rule hiding in that sentence is today's model:

```
speed = distance per frame × frames per second
```

If the loop runs faster, the ship moves faster. In week 7 Godot runs the loop for you and calls your update code once per frame. In [week 9](w09-delta-time-and-frame-rate-independence.md) you learn to make movement independent of frame rate with delta time. This week you see why that is needed.

## 4. Worked example: why Space Invaders speeds up

### The hook

In Taito's *Space Invaders* (1978), a formation of aliens marches side to side and steps down toward you. At the start it crawls. As you shoot them, the survivors get faster, and the last one races across the screen. The acceleration is the difficulty curve of the whole game.

Nobody wrote a line saying "speed up as aliens die". Wikipedia's account of the game, based on designer Tomohiro Nishikado's recollections, says the hardware could draw the aliens faster when fewer were on screen, and Nishikado kept the effect rather than compensating for it. Computer Archeology's annotated disassembly of the arcade code shows the loop that produces it. The routine that advances the aliens runs from the interrupt the hardware raises in the middle of each screen refresh, 60 times a second, and each time it moves **one** alien. When it has gone through every living alien, the whole formation has taken one step.

### The model

- `F` is the number of loop passes per second. For Space Invaders, `F = 60`, one per screen refresh.
- `N` is the number of living aliens.
- `d` is how far the formation moves in one step. The disassembly uses 2 pixels sideways.

Each pass moves one alien, so a full formation step takes `N` frames. That gives

```
formation steps per second = F / N
formation speed            = d × F / N   pixels per second
time for one step          = N / F       seconds
```

The work per frame is constant. The work per *formation step* is proportional to `N`. Remove aliens and each step needs fewer frames, so steps come more often.

(The disassembly also has a special case for the very last alien's step size. We leave it out. The model without it explains the curve.)

### Numbers you can check

With `F = 60` and `d = 2`:

| Aliens alive `N` | Frames per step | Steps per second `60/N` | Speed `2 × 60/N` (px/s) | Time per step (s) |
|---|---|---|---|---|
| 55 (5 rows of 11) | 55 | 1.09 | 2.18 | 0.917 |
| 44 | 44 | 1.36 | 2.73 | 0.733 |
| 28 | 28 | 2.14 | 4.29 | 0.467 |
| 11 | 11 | 5.45 | 10.91 | 0.183 |
| 5 | 5 | 12 | 24 | 0.083 |
| 2 | 2 | 30 | 60 | 0.033 |
| 1 | 1 | 60 | 120 | 0.017 |

Killing the first 27 aliens (55 to 28) doubles the speed. Killing the last one of two doubles it again, in a single shot. The curve is `c / N`, a rational function, which is why it is flat at first and then shoots upward. MA101 week 6 studies that shape in depth.

You can reproduce the frame counts with a loop that does what the arcade did, one alien per frame:

```python
FPS = 60
alive = 11          # try 55, 28, 1
cursor = 0          # which alien moves this frame
frame = 0
steps_done = 0

while steps_done < 3:
    # update: move the alien under the cursor, then advance the cursor
    cursor = cursor + 1
    if cursor == alive:
        cursor = 0
        steps_done = steps_done + 1
    frame = frame + 1

print(f"{alive} aliens: {frame} frames for 3 steps = {frame / FPS:.2f} s")
```

With 11 aliens it prints `33 frames for 3 steps = 0.55 s`. Three steps at 0.183 s each is 0.55 s, matching the table.

### The visual

Open `examples/w03-invaders-loop.html`. The left view is the loop. It shows a formation of generic blocks with a highlight on the one alien being moved this frame, a frame counter, and a bar showing the constant work per frame (one alien). The right view is the result. It plots formation speed against aliens alive, from 55 down to 1, with a dot for the current value.

Click aliens to remove them, or drag the "aliens alive" slider. In the left view nothing about a single frame changes. The highlight still moves one alien, the work bar stays the same height. In the right view the dot climbs the `120 / N` curve. The loop looks identical every frame, yet the game gets faster. The "Loop rate F" buttons switch `F` between 30, 60 and 120 passes per second to show that the same code on a faster loop speeds up the whole curve.

### Cross-game recognition

**IBM PC games and the turbo button (mid-1980s to mid-1990s).** Many early PC programs timed themselves by the speed of the processor, tuned for the original 4.77 MHz Intel 8088. Their loops did a fixed amount of work per pass and assumed a pass took a fixed time. On faster 286, 386 and 486 machines the loop ran more passes per second, and by our model everything moved faster in proportion, often too fast to play. Many PCs of that era had a front-panel "turbo" button whose off position slowed the machine to near original speed so those programs stayed playable. Same model, with `F` changing instead of `N`. Nystrom mentions the button in his Game Loop chapter for this reason.

**Godot 4 (the engine you use from week 7).** Godot runs two loops for you. The docs say `_process()` is called every drawn frame, as often as possible, and `_physics_process()` is called at a fixed rate, 60 times per second by default (set under Physics > Common in Project Settings). Code that moves a sprite 2 pixels in `_process()` without further care is Space Invaders on a turbo PC. It moves at `2 × F` pixels per second, and `F` is whatever the player's machine manages. Code in `_physics_process()` gets a steady `F = 60` on any machine that can keep up. Engines build a fixed-rate loop because of exactly the problem in this section.

**Your text adventure from section 2.** Its loop rate is set by the player's typing, one pass per command. The lamp in that code runs out after 20 *moves*, not 20 seconds. A fast player and a slow player get the same game. Turn-based games are immune to loop-rate problems because their loop rate is the player's own decision rate.

### Design judgment

Frame-counted logic (move `d` per frame, count frames for timers) is not wrong. It is a trade-off you should choose with open eyes.

- **Safe when `F` is fixed and guaranteed.** An arcade board refreshes at the same rate every time. Space Invaders could count frames because every machine was identical. Fighting games that measure attacks in frames rely on the same guarantee.
- **Deterministic.** The same inputs on the same frames give the same result every time. Replays, rollback netcode and speedrun routes all depend on that property. You meet it again in [CS202 week 12](../../CS202-networking-fundamentals-for-multiplayer-games/syllabus.md), deterministic lockstep.
- **Breaks when `F` varies.** On PCs and phones the frame rate depends on the hardware, the monitor and what else is on screen. Frame-counted speed then varies with it. The fixes are delta time and a fixed-timestep loop, [weeks 9 and after](w09-delta-time-and-frame-rate-independence.md), following Glenn Fiedler's "Fix Your Timestep!" (2004).
- **Emergent difficulty is still a design decision.** Nishikado kept an accidental curve because it played well. If you want that curve on purpose, write it explicitly, for example `speed = 120 / alive`, so it survives a port to faster hardware. Otherwise the next machine changes your difficulty for you.
- **Watch the budget.** Work that grows with `N` inside a frame (drawing every alien, checking every bullet against every alien) makes frames slower as `N` grows, which is the opposite of the Space Invaders effect. At 60 fps you have 16.7 ms. Keep per-frame work bounded or you drop frames.

### Check yourself (worked example)

1. A tribute game moves one alien per frame at 60 fps, but starts with 40 aliens. How long does one formation step take at the start, and how many aliens must be left before the formation steps at least 10 times per second?
2. The same code runs on a board that refreshes at 50 Hz. How fast (in px/s, with `d = 2`) does a formation of 20 aliens move? How much slower is that than at 60 Hz?
3. A designer wants the formation's speed to rise linearly from 2 px/s at 55 aliens to 120 px/s at 1 alien instead of following `120 / N`. Write the formula. At 28 aliens, is the new game harder or easier than Space Invaders?

<details>
<summary>Answers</summary>

1. `N / F = 40 / 60 ≈ 0.667` s per step. Steps per second `60 / N ≥ 10` needs `N ≤ 6`. So 6 or fewer aliens.
2. `2 × 50 / 20 = 5` px/s, against `2 × 60 / 20 = 6` px/s at 60 Hz. It is one sixth slower (about 17%).
3. Speed falls linearly from 120 at `N = 1` to 2 at `N = 55`, a slope of `−118 / 54` per alien. So `speed = 120 − (N − 1) × 118 / 54`. At `N = 28`, speed is `120 − 27 × 2.185 ≈ 61` px/s, far above the 4.29 px/s of Space Invaders. It is much harder in the middle of the wave.

</details>

## 5. Loop patterns you will reuse all semester

Most game loops are built from a small set of patterns:

| Pattern | Shape | Game example |
|---|---|---|
| Count | `for i in range(n):` | Spawn 5 enemies, animate 12 frames |
| Accumulate | `total = total + x` inside a loop | Sum damage over a poison's 6 ticks |
| Search | loop, `if` found, `break` | First free slot, first enemy in range |
| Run until | `while not done:` with a flag | The game loop, a menu, a turn loop |
| Every k-th | `if frame % k == 0:` | Fire every 30 frames, blink every 15 |

The last pattern uses `%` again. `frame % 30 == 0` is `True` on frames 0, 30, 60 and so on. At 60 fps that is twice per second, and at 120 fps it is four times per second. Frame-counted again, with the same trade-off.

### Tracing tips

- Before running a loop, predict how many iterations it will make and write it down.
- If it misbehaves, print the loop variables at the top of the block. `print(f"frame={frame} x={x}")` beats guessing.
- For infinite loops, add a safety counter while developing: `if frame > 10_000: break`.

## In-class activity (25 min)

In pairs, on paper first, then in Python.

1. **Trace (8 min).** Trace the section 2 turn loop for the commands `north`, `east`, `take key`, `east`. Fill a table with iteration, command, room, `has_key`, `moves` and message.
2. **Rate (10 min).** Take the invaders frame-count program. Change it so it moves **two** aliens per frame. Predict the new table row for 55, 11 and 1 aliens before running it. Then run it and check.
3. **Decide (7 min).** You are porting a frame-counted game to a phone that might run at 30, 60 or 120 fps. List two values in the game that would change with frame rate and say, for each, whether you would count frames or measure seconds.

Expected output: a trace table, the three predicted and measured rows from step 2 (the model gives `N / 2`, so 27.5, 5.5 and 0.5 frames per step; code that moves two aliens per frame measures 28, 6 and 1, because a frame cannot be split), and a short list from step 3.

## Common misconceptions

- **"`range(1, 10)` includes 10."** It stops before 10. It gives nine values, 1 to 9.
- **"A game loop waits for the player."** A turn loop does. A real-time game loop checks input and moves on, so the world keeps running.
- **"If the code does the same thing every frame, the game runs at the same speed everywhere."** Speed is distance per frame times frames per second. The same per-frame code runs faster on a faster loop, and faster when each step needs fewer frames, as Space Invaders shows.
- **"`while x != target` is fine for moving objects."** If `x` moves in steps larger than 1 it can jump over the target. Use `<` or `>=`.

## Check yourself

1. How many times does `for i in range(3, 15, 4): print(i)` print, and what values?
2. What is wrong with this loop, and how would you fix it? `hp = 10`, then `while hp != 0: hp = hp - 3`.
3. A game loop runs at 60 fps. A power-up timer counts 300 frames. How long does it last at 60 fps, and at 144 fps?
4. A loop moves a missile 4 pixels per frame at 30 fps. Another moves 2 pixels per frame at 60 fps. Which is faster, and which looks smoother?
5. Write a `for` loop that prints a countdown `3`, `2`, `1`, then `Go!`.

<details>
<summary>Answers</summary>

1. Three times: 3, 7, 11. The next value, 15, is not included.
2. `hp` goes 10, 7, 4, 1, −2, and never equals 0, so the loop never ends. Use `while hp > 0:`.
3. `300 / 60 = 5` s at 60 fps. At 144 fps the same count lasts `300 / 144 ≈ 2.08` s. Frame-counted timers shrink on fast machines.
4. Both move `4 × 30 = 2 × 60 = 120` px/s, so neither is faster. The 60 fps missile moves in smaller steps, twice as often, so it looks smoother.
5. `for n in range(3, 0, -1): print(n)` then `print("Go!")`.

</details>

## Lab / assignment hook

[Lab 03, loop it](../labs/lab03.md). You turn a one-turn cave into a full turn loop with a move limit and a win check, then write a frame loop that reproduces the invaders speed table and measures it. A checker script runs both parts. Part of the weekly exercises (40%). Mini-game 1, a platformer built in weeks 7 to 9, reuses the read, change, check order from this loop for its win and loss checks.

## Sources

- Wikipedia, "Space Invaders". Taito, 1978, Intel 8080; Nishikado's account that the hardware drew the aliens faster when fewer remained, and that he kept the speed-up as a gameplay feature.
- Computer Archeology, "Space Invaders" code disassembly (computerarcheology.com/Arcade/SpaceInvaders). 5 rows of 11 aliens; 60 Hz screen with mid-screen and end-of-screen interrupts; the routine that advances one alien per mid-screen interrupt and moves the rack a step when the cursor passes the last alien; rack delta of 2 pixels and the special case for a single alien.
- Wikipedia, "Turbo button". Programs timed by the CPU speed of the 4.77 MHz 8088 ran too fast on faster machines; turbo buttons were common on 286, 386 and 486 PCs from the mid-1980s to mid-1990s.
- Nystrom, R. (2014). *Game Programming Patterns*, chapter "Game Loop". gameprogrammingpatterns.com. The process input, update, render structure, non-blocking input, and the turbo button example.
- Godot Engine documentation (stable, Godot 4), "Idle and physics processing". `_process()` every frame, `_physics_process()` at a fixed 60 times per second by default.
- Fiedler, G. (2004). "Fix Your Timestep!". gafferongames.com. Referenced for week 9.
- Python Software Foundation, *The Python Tutorial*, sections 4.2 to 4.4 (Python 3.13).

## Interactive spec: examples/w03-invaders-loop.html

**Purpose.** Show that a loop doing constant work per frame can still produce a speed that depends on how much work a step needs. The first screen shows 55 aliens marching slowly with the speed readout at 2.18 px/s and the curve dot at the far left.

**Layout.** Two linked views. Left: the loop (formation plus frame instrumentation). Right: the speed curve. Stacked on mobile (loop first).

**Left view, the loop.**
- A 5 × 11 formation of plain rounded rectangles (no Space Invaders sprites). Each frame, exactly one living alien moves by `d = 2` px (scaled for display), in reading order; a highlight outlines the alien moved this frame. When the cursor passes the last living alien, increment the "formation steps" counter and reverse direction at the play-field edges (step down 8 px on a reversal).
- The simulation runs at the chosen loop rate `F` using a fixed-step accumulator on `requestAnimationFrame`, so display rate does not change the model. Under `prefers-reduced-motion`, pause by default and offer a "step 1 frame" and "step 1 formation step" button.
- Instrumentation beside the formation: frame counter, "aliens moved this frame: 1" with a bar of constant height, "frames per formation step: N".
- Controls: slider "aliens alive" 1 to 55 (removes aliens from the bottom-right, in reverse reading order); click or Enter on an alien to remove it; segmented control `F` ∈ {30, 60, 120} (default 60); play/pause; reset to 55.

**Right view, the curve.**
- Plot speed `s(N) = d × F / N` in px/s for N from 1 to 55 (x-axis reversed so it reads left to right as aliens die, 55 on the left). Draw curves for the current `F` solid and the other two `F` values faint.
- A dot at the current `N`; readouts: `N`, frames per step `N`, steps per second `F / N` (2 decimals), speed `2F / N` px/s (2 decimals), time per step `N / F` s (3 decimals).
- Optional "measured" readout: frames counted in the left view divided by formation steps completed over the last few steps; must equal `N`.

**The one insight.** Every frame does the same work, yet the formation speeds up as `F / N` because each step needs fewer frames. Changing `F` scales the whole curve, which is the turbo-button problem.

**Test values (F = 60, d = 2; must match the lecture table).**
- N = 55 → 1.09 steps/s, 2.18 px/s, 0.917 s.
- N = 28 → 2.14 steps/s, 4.29 px/s, 0.467 s.
- N = 11 → 5.45 steps/s, 10.91 px/s, 0.183 s.
- N = 1 → 60 steps/s, 120 px/s, 0.017 s.
- F = 50 is not offered, but F = 30 with N = 20 → 3 px/s, and F = 120 with N = 20 → 12 px/s.

**Accessibility.** All controls keyboard reachable; aliens focusable in a grid with arrow-key navigation; readouts in an `aria-live="polite"` region, throttled to at most once per second.

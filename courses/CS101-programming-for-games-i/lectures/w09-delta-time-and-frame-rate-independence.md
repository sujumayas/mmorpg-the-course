# CS101 · Week 09 — Delta Time and Frame-Rate Independence

**Why this matters:** Your game will run on a 30 fps school laptop, a 60 Hz office monitor and a 144 Hz gaming screen, often on the same day. If your code counts frames instead of seconds, it is three different games, and the fastest machine gets the fastest (or broken) one. This week you learn the one multiplication that fixes most of it, and the loop structure that fixes the rest.

**You will be able to:**
- Compute how fast an object moves per second when its code moves it a fixed amount per frame, at any frame rate.
- Convert per-frame movement, timers and damping into per-second code using `delta`, and check the result with numbers.
- Explain why `position += velocity × dt` still gives different jump heights at different frame rates, and compute the difference.
- Trace a fixed-timestep accumulator loop frame by frame, including the number of simulation steps, the leftover time and the interpolation factor.

**Before class:** Fiedler, G. "Fix Your Timestep!" (gafferongames.com, 2004), the whole article, about 20 minutes. Nystrom, *Game Programming Patterns* (2014), "Game Loop", from "Take a little nap" to the end.

**Prerequisites from earlier courses:** [CS101 week 3, loops and the game loop](w03-loops-and-the-game-loop.md) (the loop itself). [CS101 week 7, scenes, nodes and scripts](w07-engine-intro-scenes-nodes-scripts.md) (`_process(delta)` and `_physics_process(delta)`). [CS101 week 8, input handling and movement](w08-input-handling-and-movement.md) (timers in seconds, the "6 frames" bug). [MA101 week 2, linear functions and rates](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w02-linear-functions-and-rates.md) (distance = rate × time). [MA101 week 8, interpolation](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w08-interpolation-lerp-inverse-lerp-remap.md) (lerp, and why "lerp toward a target every frame" depends on frame rate). [GS101 week 3, the arcade era](../../GS101-history-and-critical-study-of-games/lectures/w03-arcade-era-and-the-coin-op-business-model.md) (Space Invaders as a business and design story).

**Interactive:** [Refresh-rate race](../examples/w09-refresh-rate-race.html) for section 2 and [fixed-timestep accumulator](../examples/w09-fixed-timestep-accumulator.html) for section 4.

---

## 1. What a frame is

A **frame** is one pass through the game loop: read input, update the world, draw the picture. The **frame rate** is how many frames run per second (fps). The **frame time**, written `dt` for "delta time" (delta is the Greek letter mathematicians use for "change in"), is how long one frame takes, in seconds.

```
dt = 1 / fps        fps = 1 / dt
```

| Frame rate | Frame time `dt` | Where you meet it |
|---|---|---|
| 30 fps | 33.3 ms | Older laptops, some console games |
| 60 fps | 16.7 ms | Most office and laptop screens |
| 120 fps | 8.33 ms | Newer phones and TVs, many gaming monitors |
| 144 fps | 6.94 ms | Common gaming monitor refresh rate |
| 240 fps | 4.17 ms | High-end esports monitors |

Two facts make this a problem. First, you do not choose the frame rate. With **vsync** on (Godot's default), the engine waits for the monitor to finish showing each picture, so the frame rate usually matches the monitor's refresh rate. Buy a 144 Hz monitor and your game runs 144 frames a second. Second, frame time is not constant. A frame that loads a texture, spawns fifty enemies or loses the CPU to another program takes longer. `dt` jumps around from frame to frame, even on one machine.

## 2. Worked example: why speed doubles on a 120 Hz monitor

### The hook

Space Invaders (Taito, 1978) is famous for aliens that march faster and faster as you shoot them. According to Wikipedia's account of its development, designer Tomohiro Nishikado found that his hardware could draw each frame faster when fewer aliens remained on screen. The aliens moved a fixed step each frame, so fewer aliens meant more frames per second, which meant faster aliens. He kept the effect, and it became the game's tension curve. (GS101 week 3 discusses it as a design decision.)

That time it was a happy accident. Here is one that wasn't. In Dark Souls II (2014), weapon durability loss was tied to the frame rate, so weapons wore out faster in versions that ran at 60 frames per second, such as the PC release. The bug survived patch 1.10 in February 2015 and the April 2015 re-release, Scholar of the First Sin, which ran at 60 fps on PC, PlayStation 4 and Xbox One. A patch later that April finally fixed it. For about a year, players on better hardware had worse weapons.

Both games have one cause. Code that says "per frame" when the designer meant "per second".

### The model

Suppose your code moves the player a fixed `s` pixels each frame:

```
x = x + s                       (runs once per frame)
speed = s × fps                 (pixels per second)
```

Speed is proportional to frame rate. Double the frame rate and you double the speed.

The fix is to state speeds in units per *second*, called `v`, and multiply by the frame time:

```
x = x + v × dt                  (runs once per frame)
distance in one second = v × dt × fps = v × (1/fps) × fps = v
```

The `fps` cancels. The player covers `v` pixels per second at any frame rate. This multiplication is what `delta` in `_process(delta)` is for.

### Code you can run

```python
def naive(fps, seconds=1.0, step=5):
    x = 0
    for _ in range(round(fps * seconds)):
        x += step                 # 5 px per frame, tuned on a 60 Hz screen
    return x

def with_dt(fps, seconds=1.0, speed=300):
    x, dt = 0.0, 1 / fps
    for _ in range(round(fps * seconds)):
        x += speed * dt           # 300 px per second, whatever the frame rate
    return x

for fps in (30, 60, 120, 144):
    print(fps, naive(fps), round(with_dt(fps), 6))
```

The same thing in Godot is one line inside `_process`:

```gdscript
func _process(delta: float) -> void:
    position.x += 300.0 * delta     # not: position.x += 5
```

### Numbers you can check

The naive version was tuned at 60 fps, where 5 px per frame is 300 px/s. Crossing a 1,920 px wide screen takes `1920 / (5 × fps)` seconds.

| Frame rate | Naive: px moved in 1 s | Naive: time to cross 1,920 px | With `dt`: px moved in 1 s |
|---|---|---|---|
| 30 fps | 150 | 12.80 s | 300 |
| 60 fps | 300 | 6.40 s | 300 |
| 120 fps | 600 | 3.20 s | 300 |
| 144 fps | 720 | 2.67 s | 300 |

On a 120 Hz monitor the naive player is exactly twice as fast as the one you tested. On a 30 fps laptop it is half as fast. Everything else counted per frame moves with it: enemy patrols, bullet speeds, animation timers, cooldowns, and (as Dark Souls II shows) any stat that ticks once per frame.

### A visual you can move

Open `examples/w09-refresh-rate-race.html`. Two lanes, two runners, one piece of code. The top lane is a simulated 60 Hz monitor and the bottom lane a simulated 120 Hz monitor (use the selector to try 30, 144 or 240 Hz). Each runner is drawn only on its own lane's frames, so you can see the 120 Hz runner update twice as often. With the "use delta time" switch off, the 120 Hz runner reaches the finish flag in half the time. Flip it on and the two runners move side by side, even though one is still drawn twice as often. A frame counter and a distance readout under each lane show the numbers from the table.

The insight is in the gap between the two views. Both lanes run the same code. Only the number of times per second it runs is different, and `dt` is the only thing that tells the code what that number is.

### Cross-game recognition

- **Space Invaders (1978).** Fixed step per frame, frame rate rising as aliens die. Speed rose with it. Written in our model, `speed = s × fps`, with fps growing through the wave.
- **Dark Souls II (2014 to April 2015).** Durability loss tied to the frame rate. Same model with "durability" in place of `x`. A 60 fps build loses durability faster than a 30 fps one, for the same play.
- **Early PC games and the turbo button.** Nystrom notes that games written for one CPU ran too fast on faster machines, which is why old PCs had a "turbo" button to slow the computer down. Here the loop had no wait at all, so `fps` was simply "as fast as the CPU allows".
- **Celeste (2018).** The fix, visible in the published `Player.cs`. Movement is applied as `MoveH(Speed.X * Engine.DeltaTime)`, and every timer, including the coyote timer from week 8, counts down with `timer -= Engine.DeltaTime`.

Four games, one rule: *anything that should happen per second must be multiplied by `dt`, or it happens per frame.*

### Eyes-open design judgment

`dt` fixes additions. It does not automatically fix everything else, and multiplying by `dt` in the wrong place creates new bugs.

**Multiplications per frame.** A common way to slow something down is `velocity *= 0.9` every frame. That loses 10% per *frame*. After one second at 60 fps, `0.9^60 = 0.0018` of the speed is left. At 144 fps, `0.9^144 ≈ 0.00000026`. Multiplying the 0.9 by `dt` makes nonsense. The correct fix is a power: `velocity *= 0.9 ** (dt * 60)`, which loses exactly as much per second as the original did at 60 fps. Celeste's camera does this. It moves toward its target by `1 − 0.01^dt` of the remaining gap each frame, which closes 99% of the gap per second at any frame rate. MA101 week 8 derives the general form, `1 − e^(−λ dt)`.

| Frame rate | `0.9` per frame: left after 1 s | `0.9^(dt × 60)` per frame: left after 1 s | Celeste camera: fraction of gap closed per frame |
|---|---|---|---|
| 30 fps | 0.042 | 0.0018 | 0.142 |
| 60 fps | 0.0018 | 0.0018 | 0.074 |
| 144 fps | 0.00000026 | 0.0018 | 0.031 |

**Huge frames.** When the player drags the window or the OS pauses your game, the next `dt` can be two seconds. `x += v × dt` then teleports the player 600 px in one step, possibly through a wall. Clamp `dt` (for example to 0.1 s) before using it. The game then runs in slow motion for that one frame, which is better than skipping through geometry.

**When per-frame is fine.** A menu animation or a particle flicker that runs 20% faster on some machines harms nobody. Spend care where it touches gameplay, fairness or anything two players compare.

**The part `dt` cannot fix.** Section 3 shows it.

### Check yourself (worked example)

1. A bullet moves 12 px per frame. How fast does it travel at 60, 120 and 240 fps, in px/s?
2. Rewrite `timer -= 1` (run per frame, with `timer = 90` meaning "1.5 seconds at 60 fps") so it lasts 1.5 seconds at any frame rate.
3. A skid applies `speed *= 0.8` per frame and was tuned at 60 fps. Write the frame-rate-independent version.

<details>
<summary>Answers</summary>

1. `12 × fps`: 720, 1,440 and 2,880 px/s.
2. Start with `timer = 1.5` and subtract `dt` each frame (`timer -= dt`). It ends when `timer <= 0`.
3. `speed *= 0.8 ** (dt * 60)`. At 60 fps, `dt × 60 = 1`, which gives back the original.

</details>

## 3. Where `dt` is not enough: the jump that depends on your monitor

Try a jump. Initial upward speed `v0 = 400` px/s, gravity `g = 1000` px/s². Physics gives an exact apex height of `v0² / (2g) = 80` px. A game updates it like this each frame:

```python
def jump_apex(fps, v0=400.0, g=1000.0):
    dt, y, v, best = 1 / fps, 0.0, v0, 0.0
    while v > -v0:
        v -= g * dt        # gravity changes velocity...
        y += v * dt        # ...then velocity changes position
        best = max(best, y)
    return best
```

This is called **semi-implicit Euler** integration. It updates velocity first, then position, and it is what most game code does (Godot's `CharacterBody2D` examples add gravity to `velocity`, then call `move_and_slide`). Every line uses `dt` correctly. Here is what it gives:

| Frame rate | Semi-implicit Euler apex | Swap the two lines (explicit Euler) apex | Exact |
|---|---|---|---|
| 30 fps | 73.33 px | 86.67 px | 80 px |
| 60 fps | 76.67 px | 83.33 px | 80 px |
| 120 fps | 78.33 px | 81.67 px | 80 px |
| 144 fps | 78.62 px | 81.39 px | 80 px |

The code is frame-rate *aware* but not frame-rate *independent*. Stepping in chunks of `dt` approximates a smooth curve, and the error is about `v0 × dt / 2` (6.67 px at 30 fps, 1.39 px at 144 fps). If a ledge is 78 px high, the 144 Hz player makes the jump and the 60 Hz player never can. Variable `dt` also means variable results from the same inputs, so replays drift and networked players disagree. Nystrom lists exactly these problems for variable time steps: non-determinism, and physics tuned for one step size becoming unstable at another.

You could chase ever-better integration formulas. The standard solution is simpler. Stop letting the frame rate choose `dt`.

## 4. Worked example: the fixed-timestep accumulator

### The hook

Open any Godot project and look at *Project Settings → Physics → Common*. `physics_ticks_per_second` is 60, and `max_physics_steps_per_frame` is 8. Your `_physics_process` is called 60 times a second whether the screen runs at 30, 60 or 144 Hz. At 144 Hz, most frames get no physics call at all. At 30 Hz, every frame gets two. The jump in section 3 would come out at 76.67 px on every machine. Not exactly 80, but *the same* for every player, every replay and every run.

How does an engine run a 60 Hz simulation inside a 144 Hz loop? With a few lines Glenn Fiedler published in 2004 as "Fix Your Timestep!".

### The model

Keep a bank of real time that has passed but not yet been simulated, called the **accumulator**. Each frame, deposit the frame's real duration. Then withdraw in fixed chunks of `SIM_DT` (for example 1/60 s), running one simulation step per chunk, until less than one chunk remains.

```
each frame:
    frame_time = min(real time since last frame, 0.25)
    accumulator += frame_time
    while accumulator >= SIM_DT:
        previous = current
        current = step(current, SIM_DT)          # always the same dt
        accumulator -= SIM_DT
    alpha = accumulator / SIM_DT                 # 0 ≤ alpha < 1
    draw(lerp(previous, current, alpha))
```

- `SIM_DT` is the fixed simulation step. The simulation never sees any other `dt`, so it gives identical results on every machine.
- The **leftover** in the accumulator is real time that is not yet worth a whole step. It carries into the next frame, so no time is lost.
- `alpha` says how far we are between the last two simulated states. Drawing `lerp(previous, current, alpha)` (MA101 week 8) keeps motion smooth on screens faster than the simulation. Fiedler calls this "the final touch".
- The `min(…, 0.25)` clamp prevents the **spiral of death**. If one frame takes very long, the loop would need many steps to catch up. If steps are slow, catching up takes even longer, and the next frame needs even more steps. The clamp gives up on the lost time instead, so the game slows down briefly rather than freezing.

### Code you can run

```python
SIM_DT = 1 / 60
EPS = 1e-9                                 # float tolerance (week 1: never compare floats exactly)

def run_accumulator(frame_times, sim_dt=SIM_DT, max_frame=0.25):
    acc, rows = 0.0, []
    for i, ft in enumerate(frame_times, 1):
        ft = min(ft, max_frame)            # avoid the spiral of death after a hitch
        acc += ft
        steps = 0
        while acc >= sim_dt - EPS:
            acc -= sim_dt                  # one fixed simulation step runs here
            steps += 1
        if abs(acc) < EPS:
            acc = 0.0                      # snap rounding dust to exactly zero
        rows.append((i, ft * 1000, steps, acc * 1000, acc / sim_dt))
    return rows

for row in run_accumulator([1 / 144] * 12):
    print("%2d  %.2f ms  %d steps  leftover %.2f ms  alpha %.3f" % row)
```

### Numbers you can check

**A 144 Hz screen, 60 Hz simulation.** Each frame deposits 6.94 ms. Each step withdraws 16.67 ms.

| Frame | Deposit | Steps run | Leftover | alpha |
|---|---|---|---|---|
| 1 | 6.94 ms | 0 | 6.94 ms | 0.417 |
| 2 | 6.94 ms | 0 | 13.89 ms | 0.833 |
| 3 | 6.94 ms | 1 | 4.17 ms | 0.250 |
| 4 | 6.94 ms | 0 | 11.11 ms | 0.667 |
| 5 | 6.94 ms | 1 | 1.39 ms | 0.083 |
| 6 | 6.94 ms | 0 | 8.33 ms | 0.500 |
| 7 | 6.94 ms | 0 | 15.28 ms | 0.917 |
| 8 | 6.94 ms | 1 | 5.56 ms | 0.333 |
| 9 | 6.94 ms | 0 | 12.50 ms | 0.750 |
| 10 | 6.94 ms | 1 | 2.78 ms | 0.167 |
| 11 | 6.94 ms | 0 | 9.72 ms | 0.583 |
| 12 | 6.94 ms | 1 | 0.00 ms | 0.000 |

Twelve frames, five steps: `12 / 144 = 5 / 60 = 0.0833` s, so real time and simulated time agree exactly. Check frame 3 by hand: `13.89 + 6.94 = 20.83`, one step leaves `20.83 − 16.67 = 4.17`. Frame 12 is why the code has `EPS`. Twelve deposits of 1/144 should equal five steps of 1/60 exactly, but floats can't store either fraction exactly, so the accumulator ends a hair below 16.67 ms. Without the tolerance, `acc >= sim_dt` is false on frame 12, the table shows 0 steps and alpha 1.000, and the step slips to frame 13. That is week 1's rule again. Never compare floats exactly. The tolerance of one nanosecond is far smaller than any real frame, so it only absorbs rounding.

**A 50 fps laptop.** Each frame deposits 20 ms. The pattern is 1, 1, 1, 1, 2 steps, with leftovers 3.33, 6.67, 10.00, 13.33, 0.00 ms. Six steps per five frames, which is 60 per 50.

**A hitch.** Frames of 16.67 ms, then 300 ms (the player alt-tabbed), then 16.67 ms. The clamp cuts 300 to 250 ms, so the long frame runs 15 steps instead of 18. The game loses 50 ms of simulated time and stays responsive.

### A visual you can move

Open `examples/w09-fixed-timestep-accumulator.html`. The top view is a timeline. Render frames are drawn as ticks above the line, simulation steps as ticks below, and a bar on the side fills with real time and drains in `SIM_DT` chunks. The bottom view is a ball thrown on the same jump as section 3, drawn three ways side by side: variable `dt`, fixed step without interpolation, and fixed step with interpolation. Sliders set the display rate (30 to 240 fps), the simulation rate (10 to 120 Hz) and a "hitch" button inserts a 300 ms frame.

Set the simulation to 10 Hz to see the idea at its most obvious. Without interpolation the ball jumps in visible steps. With it the ball moves smoothly, and the peak height readout stays exactly the same across every display rate, while the variable-`dt` ball's peak changes each time you move the display slider.

### Cross-game recognition

- **Godot 4.x.** `_physics_process` runs at `physics_ticks_per_second` (60 by default), independent of the frame rate. `max_physics_steps_per_frame` (8 by default) caps catch-up, the same job as Fiedler's 0.25 s clamp. An optional physics interpolation setting draws between ticks, Fiedler's final touch.
- **Unity.** `FixedUpdate` runs at the interval set by `Time.fixedDeltaTime`. The Time settings' "Maximum Allowed Timestep" caps the worst case when frame rate is low. Same three parts: fixed step, accumulator, clamp.
- **Nystrom's game loop.** His version keeps a `lag` variable (our accumulator), runs `update()` in fixed `MS_PER_UPDATE` steps while lag is large enough, and calls `render(lag / MS_PER_UPDATE)`, which is our `alpha`.
- **Celeste (2018), as a contrast.** The published player code scales everything by `Engine.DeltaTime` rather than showing an accumulator. That is a legitimate choice for a single-player game whose developers control the target frame rate. It shows the fixed-step loop is a decision, not a law.

### Eyes-open design judgment

- **Pick the tick rate deliberately.** 60 Hz is a sensible default. A lower rate (30 Hz) halves CPU cost but adds latency and needs interpolation to look smooth. A higher rate (120 Hz) makes fast collisions more reliable and costs twice the CPU. Competitive online games choose their server tick rate with great care. You will meet that in [CS202 week 13](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w13-tick-rate-and-bandwidth-budgets.md).
- **Interpolation costs latency.** Drawing between `previous` and `current` means the screen shows a state up to one step old. At 60 Hz that is at most 16.7 ms. Usually worth it, but know you're paying it.
- **Know what goes where.** Gameplay physics, movement, collisions and anything that must match across machines go in the fixed step (`_physics_process`). Pure visuals such as camera smoothing, particles and UI can use variable `dt` in `_process`.
- **Input still arrives per frame.** A button pressed during a frame with 0 physics steps must survive until the next step. That is why week 8 warned against clearing input flags in `_process`.
- **Keep steps cheaper than `SIM_DT`.** If one simulation step takes longer to compute than the time it represents (more than 16.7 ms of CPU for a 60 Hz step), no clamp can save you. The game will always fall behind. Profile before you raise the tick rate.

### Check yourself (worked example)

1. Display 90 fps, simulation 60 Hz. Trace three frames from an empty accumulator: steps and leftover in each.
2. Display 30 fps, simulation 60 Hz. How many steps run each frame? What is alpha after each frame?
3. With a 0.25 s clamp and 60 Hz steps, what is the most steps a single frame can run? What is it in Godot with the default settings?

<details>
<summary>Answers</summary>

1. Deposit 11.11 ms per frame. Frame 1: 0 steps, leftover 11.11. Frame 2: 22.22, 1 step, leftover 5.56. Frame 3: 16.67, 1 step, leftover 0.00. Two steps per three frames, which is 60 per 90.
2. Deposit 33.33 ms. Two steps every frame, leftover 0, alpha 0.
3. `0.25 × 60 = 15` steps. Godot caps it at 8 by default, so at most `8 / 60 = 0.133` s of game time per frame.

</details>

## In-class activity (25 minutes)

Pairs. One laptop with Godot, one with Python.

1. **Break it (Godot).** Make a `Node2D` that moves `position.x += 5` in `_process`. Set *Application → Run → Max FPS* to 30, then 60, then 144 (turn off vsync under *Display → Window* to go above your monitor's rate). Time how long it takes to cross the window at each setting with a stopwatch.
2. **Fix it.** Change to `300 * delta` and repeat. Record the three times again.
3. **Jump it (Python).** Run `jump_apex` at 30, 60 and 144 fps. Then write a version that runs the same jump inside `run_accumulator` with `SIM_DT = 1/60`, feeding it frame times for 30, 60 and 144 fps. Record the six apex heights.
4. **Explain it.** Write three sentences for a teammate who says "I already use delta, so we don't need a fixed timestep".

Expected output: two rows of three crossing times (the first row roughly 12.8, 6.4 and 2.7 s for a 1,920 px window, the second row all equal), six apex heights (three different, three identical at 76.67 px), and the three sentences.

## Common misconceptions

- **"Higher frame rate just means smoother."** Only if the code is frame-rate independent. Otherwise it also means faster, or a different jump.
- **"Multiply everything by `dt`."** Additions yes. Multiplicative decay needs a power (`k ** (dt × 60)`). Constants such as jump impulses, which happen once, need no `dt`.
- **"Using `delta` makes physics identical on all machines."** It makes speeds right. Integration error still depends on `dt`, so jump heights and collisions still vary. A fixed timestep makes results identical.
- **"A fixed timestep means the game runs at 60 fps."** The *simulation* runs at 60 Hz. The display can run at any rate, and interpolation keeps it smooth.

## Check yourself

1. A platformer's enemy patrol turns around every 120 frames. How long is its patrol at 60 fps and at 144 fps? Fix it.
2. Using the semi-implicit Euler model, estimate the apex error at 240 fps for `v0 = 400`. Is a 79 px ledge reachable?
3. Your game uses a 50 Hz simulation. The screen runs at 60 fps. Trace five frames: steps and alpha each frame.
4. A student removes the clamp from the accumulator, and a 3-second loading stall occurs. With 60 Hz steps that each take 2 ms of CPU, how many steps run in the next frame, and how long does that frame take to compute?

<details>
<summary>Answers</summary>

1. 2 s at 60 fps, 0.83 s at 144 fps. Use a timer in seconds: `turn_timer -= dt`, turn around when it reaches 0 and reset it to 2.0.
2. `400 × (1/240) / 2 ≈ 0.83` px, so the apex is about 79.17 px (the model gives 79.17). Just reachable. At 60 fps (76.67) it is not, which is exactly the unfairness a fixed step removes.
3. `SIM_DT` = 20 ms, deposit 16.67 ms. Frame 1: 0 steps, leftover 16.67, alpha 0.833. Frame 2: 33.33, 1 step, leftover 13.33, alpha 0.667. Frame 3: 30.00, 1 step, 10.00, alpha 0.500. Frame 4: 26.67, 1 step, 6.67, alpha 0.333. Frame 5: 23.33, 1 step, 3.33, alpha 0.167. Four steps in five frames, which is 50 per 60.
4. `3 × 60 = 180` steps, `180 × 2 ms = 360` ms of computing in one frame, during which the game is frozen and more time piles up. With a 0.25 s clamp it would be 15 steps and 30 ms.

</details>

## Lab / assignment hook

[Lab 09, one game, every frame rate](../labs/lab09.md). You build a small Python simulation harness that runs the same movement, damping and jump code at 30, 60, 144 and 240 fps, find the frame-rate-dependent lines in a deliberately broken game script, fix them with `dt`, powers and a fixed-timestep accumulator, and prove the fixes with tests.

## Sources

- Fiedler, G. (2004, June 10). "Fix Your Timestep!". gafferongames.com. Fixed, variable and semi-fixed steps; the accumulator loop; the spiral of death; clamping frame time at 0.25 s; interpolation with `alpha = accumulator / dt`. https://gafferongames.com/post/fix_your_timestep/
- Nystrom, R. (2014). *Game Programming Patterns*, "Game Loop". Old games running too fast on faster PCs and the turbo button; problems with variable time steps (non-determinism, physics instability); the `lag` and `MS_PER_UPDATE` loop with `render(lag / MS_PER_UPDATE)`. https://gameprogrammingpatterns.com/game-loop.html
- Wikipedia, "Space Invaders" (accessed September 2026), development section, citing *Game Informer* 177 (2008) and *IEEE Spectrum*. The hardware rendered frames faster with fewer aliens and positions updated per frame, so aliens sped up as they were destroyed.
- Wikipedia, "Dark Souls II" (accessed September 2026), citing Klepek, P., "Annoying Dark Souls 2 Glitch Has Gone Unfixed For Nearly A Year", Kotaku (15 April 2015), and the Steam announcement of the durability update. Frame-rate-dependent weapon degradation; Scholar of the First Sin at 60 fps on PC, PS4 and Xbox One; patch 1.10 on 5 February 2015 did not fix it; fixed in an April 2015 patch.
- NoelFB, `Celeste` repository, `Source/Player/Player.cs` (file history from March 2019; code from Celeste, 2018). `MoveH(Speed.X * Engine.DeltaTime)`; timers decremented by `Engine.DeltaTime`; camera update `from + (target − from) × (1 − Math.Pow(0.01 / multiplier, Engine.DeltaTime))` with `multiplier = 1` in normal play. https://github.com/NoelFB/Celeste
- Godot Engine documentation 4.7 (stable), "ProjectSettings". `physics/common/physics_ticks_per_second` default 60; `physics/common/max_physics_steps_per_frame` default 8; `application/run/max_fps` 0 means unlimited. https://docs.godotengine.org/en/stable/classes/class_projectsettings.html
- Godot Engine documentation 4.7, "Idle and physics processing" and "Introduction to physics interpolation". `_physics_process` at a fixed rate independent of frame rate; interpolation between ticks to avoid visible jumps. https://docs.godotengine.org/en/stable/tutorials/scripting/idle_and_physics_processing.html
- Unity documentation, `Time.fixedDeltaTime` and "Time" settings (current manual). Fixed update interval; Maximum Allowed Timestep caps the worst case at low frame rates. https://docs.unity3d.com/Manual/class-TimeManager.html

## Interactive spec: examples/w09-refresh-rate-race.html

**Purpose.** Signature example. Make obvious that per-frame movement makes speed proportional to refresh rate, and that `dt` removes the dependence even though one screen still draws more often.

**Layout.** Two horizontal lanes stacked, each 100% width, 80 px tall on mobile and 120 px on desktop. Each lane has a start line at 5% and a finish flag at 95% of its width, representing 1,920 logical px. A readout panel under the lanes.

**Controls.**
- Top lane refresh rate: fixed 60 Hz label. Bottom lane refresh rate selector: 30, 120 (default), 144, 240 Hz.
- Switch "Use delta time" (default off).
- Buttons: Race (reset and start), Pause, Step (advance simulated wall-clock by 1/240 s).
- Speed field: per-frame step `s` (default 5 px) when off; per-second speed `v` (default 300 px/s) when on. Show both, greyed as appropriate.

**Simulation.** Drive both lanes from one simulated wall clock advancing in 1/240 s ticks (so every listed rate divides evenly, except 144, which uses a per-lane accumulator: a lane "frames" whenever its own accumulated time reaches `1/rate`). On each lane's frame: off: `x += s`; on: `x += v × (1/rate)`. Draw each runner only at its lane's frame times (hold the position between frames, so the 30 Hz lane looks visibly steppy). Stop a lane when `x ≥ 1920` and record its finish time.

**Readouts per lane (exact, copyable).** Frames so far, `x` in px to 2 decimals, px per second (`s × rate` or `v`), finish time to 2 decimals.

**Insight the first screen must show.** On load, auto-run once with delta time off: the 120 Hz runner finishes at 3.20 s while the 60 Hz runner is at the middle of its lane (960 px), with a caption "Same code. Twice the frames, twice the speed." Toggling "Use delta time" and pressing Race makes both finish together at 6.40 s.

**Test values.**
- Off, 60 Hz: 300 px/s, finish 6.40 s. Off, 120 Hz: 600 px/s, 3.20 s. Off, 144 Hz: 720 px/s, 2.67 s. Off, 30 Hz: 150 px/s, 12.80 s. Off, 240 Hz: 1,200 px/s, 1.60 s.
- On, any rate: 300 px/s, finish 6.40 s (±1 frame of the slower lane).

**Accessibility.** Keyboard operable controls; readouts in a polite live region at finish; reduced motion shows final positions and the table without animation; light and dark themes from the shared tokens; no game art.

## Interactive spec: examples/w09-fixed-timestep-accumulator.html

**Purpose.** Signature example. Visualise Fiedler's accumulator: render frames and simulation steps on one timeline, the accumulator filling and draining, and interpolation smoothing the picture, while fixed-step results stay identical across display rates.

**Layout.** Two linked views, stacked.

- **Timeline view.** A horizontal time axis showing the last 250 ms of real time. Render frames as ticks above the axis (labelled with the frame number), simulation steps as ticks below it. To the right, a vertical bar labelled "accumulator" with a line at `SIM_DT`; it fills by each frame's deposit and drops by `SIM_DT` per step. Show the current `alpha` as a marker between the last two simulation ticks.
- **Jump view.** Three columns, each with a ball thrown up with `v0 = 400` px/s under `g = 1000` px/s² (semi-implicit Euler: `v −= g·dt; y += v·dt`), repeating. Column A: variable timestep (`dt` = display frame time). Column B: fixed step, drawn at the latest simulated state. Column C: fixed step, drawn at `lerp(previous, current, alpha)`. A dashed line at the exact apex 80 px. Under each, "peak height" to 2 decimals, taken from the highest simulated state (not the interpolated drawing), so B and C always report the same value.

**Controls.**
- Display rate slider: 30 to 240 fps (steps 30, 50, 60, 90, 120, 144, 240), default 144.
- Simulation rate slider: 10 to 120 Hz (10, 20, 30, 50, 60, 120), default 60.
- Toggle "Clamp frame time at 0.25 s" (default on).
- Button "Hitch": makes the next display frame last 300 ms.
- Pause and Step (one display frame).
- A table below listing the last 12 frames: frame, deposit (ms), steps, leftover (ms), alpha, matching the lecture's columns.

**Model (must match exactly).** Per display frame: `ft = frame time`; if clamp on, `ft = min(ft, 0.25)`; `acc += ft`; while `acc ≥ SIM_DT − 1e-9`: `prev = cur; cur = step(cur, SIM_DT); acc −= SIM_DT`; `alpha = acc / SIM_DT`. Use the 1e-9 tolerance so the lecture's 144 Hz table reproduces exactly with a step on frame 12.

**Insight the first screen must show.** Load at display 144, simulation 60, running: the table fills with the lecture's 0,0,1,0,1,0,0,1,0,1,0,1 step pattern, column B and C peaks both read 76.67 px, column A reads 78.62 px. Dragging the display slider changes column A's peak (73.33 at 30 fps, 76.67 at 60, 78.62 at 144) while B and C stay at 76.67. Dropping the simulation rate to 10 Hz makes column B visibly steppy and C smooth.

**Test values.**
- Display 144, sim 60, empty start: steps per frame 0,0,1,0,1,0,0,1,0,1,0,1; leftovers (ms) 6.94, 13.89, 4.17, 11.11, 1.39, 8.33, 15.28, 5.56, 12.50, 2.78, 9.72, 0.00; alpha 0.417, 0.833, 0.250, 0.667, 0.083, 0.500, 0.917, 0.333, 0.750, 0.167, 0.583, 0.000.
- Display 50, sim 60: steps 1,1,1,1,2 repeating; leftovers 3.33, 6.67, 10.00, 13.33, 0.00 ms.
- Display 90, sim 60: steps 0,1,1 repeating; leftovers 11.11, 5.56, 0.00 ms.
- Hitch with clamp on at sim 60: 15 steps in the hitch frame. Clamp off: 18 steps.
- Peak heights with sim 60 (B and C): 76.67 px at any display rate. Column A peaks: 73.33 (30), 76.67 (60), 78.33 (120), 78.62 (144).

**Accessibility.** Keyboard operable sliders and buttons with visible values; the frame table is a real `<table>`; reduced motion starts paused with Step; light and dark themes from the shared tokens.

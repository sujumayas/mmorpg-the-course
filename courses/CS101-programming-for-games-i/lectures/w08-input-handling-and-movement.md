# CS101 · Week 08 — Input Handling and Movement

**Why this matters:** Players judge your game by what happens in the tenth of a second after they press a button. "I pressed jump and nothing happened" is the complaint that ends a demo, and most of the time the player is half right: they pressed a little late, and your code was stricter than it needed to be. This week you learn to read input exactly, and then to forgive it on purpose.

**You will be able to:**
- Choose between event-driven and polled input for a given action, and write both in Godot.
- Derive "just pressed" and "just released" from a stream of held/not-held states, and trace it frame by frame.
- Implement coyote time and a jump buffer with two timers, and compute how many frames each window lasts at a given frame rate.
- Turn a direction input into smooth movement with acceleration, and compute the time to reach top speed.

**Before class:** Godot Engine documentation (stable, 4.x), "Using InputEvent" and "Input examples" (about 20 minutes together). Browse `Source/Player/Player.cs` in the NoelFB/Celeste repository on GitHub, only the constants at the top of the file (the first 90 lines) and the "Jump Grace" block in `Update`. Nystrom, *Game Programming Patterns* (2014), "Game Loop", the section on processing input.

**Prerequisites from earlier courses:** [CS101 week 7, scenes, nodes and scripts](w07-engine-intro-scenes-nodes-scripts.md) (callbacks, `_process`, `_physics_process`). [CS101 week 3, loops and the game loop](w03-loops-and-the-game-loop.md) (the input step of the loop). Later this semester, [MA101 week 7, piecewise functions, caps and floors](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w07-piecewise-caps-and-floors.md) covers the clamps inside `move_toward`, and [MA101 week 12, 2D vectors](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w12-2d-vectors.md) covers vector length in full. This lecture explains the parts it uses.

**Interactive:** [w08-jump-forgiveness.html](../examples/w08-jump-forgiveness.html). Use it during section 3.

---

## 1. Two ways to hear the player

A keyboard, mouse or gamepad does not talk to your game directly. The operating system reads the device and hands the engine a stream of **input events**: "key Space went down", "key Space went up", "left stick moved to (0.42, −0.10)". The engine can give you those events in two ways.

**Events (push).** The engine calls a function on your node each time something happens. In Godot the gameplay one is `_unhandled_input(event)`. It is called only for events that no menu or button already used, which is why the documentation recommends it for gameplay over `_input`.

```gdscript
func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("pause"):
        get_tree().paused = not get_tree().paused
```

**Polling (pull).** Once per frame, you ask the engine what state the controls are in right now. Godot keeps a table of every action's state for you.

```gdscript
func _physics_process(delta: float) -> void:
    if Input.is_action_pressed("move_right"):
        velocity.x = 90.0
```

Neither is better. They answer different questions. Events answer "did something happen?" and fit one-off actions such as pausing, opening a menu or typing a name. Polling answers "what is the state now?" and fits anything continuous, such as movement, aiming or holding a charge.

### Actions, not keys

Both examples use **action names** (`"pause"`, `"move_right"`), not keys. You set these up in *Project Settings → Input Map*, where each action can be bound to several keys, buttons and stick directions. Your code asks about `"jump"` and never needs to know whether that is Space, W, or the A button on a pad. This is the same idea as the item database in week 6: the code looks things up by a name, and the data decides what the name means. It also makes remapping controls possible later, which players with disabilities rely on.

### The key-repeat trap

Hold a key in a text editor and after a moment it starts typing the letter again and again. The operating system does this by sending repeated "pressed" events, called **echo** events. Godot's documentation says they typically arrive about 20 times a second after the key has been held for roughly half a second, and that players can change or disable the rate in their system settings. Godot's `event.is_action_pressed()` ignores echoes by default. If you read raw key events instead and forget about echoes, a held jump key will fire twenty jumps a second on one player's machine and none on another's. Never let gameplay depend on the operating system's repeat rate.

## 2. Held, just pressed, just released

Polling tells you whether a button is **held** this frame. Many actions need something different, the *moment* it changed. Jumping should happen once per press, not every frame the key is down. Godot gives you three questions:

| Function | True when |
|---|---|
| `Input.is_action_pressed("jump")` | the action is held this frame |
| `Input.is_action_just_pressed("jump")` | the action started being pressed in the current frame or physics tick |
| `Input.is_action_just_released("jump")` | the action stopped being pressed in the current frame or physics tick |

You can compute the last two yourself from the first. Keep last frame's state and compare. Detecting a change between two samples like this is called **edge detection**, a term borrowed from electronics, where the "edge" is the jump in a signal from low to high.

```python
class Button:
    def __init__(self):
        self.held = False
        self.was_held = False

    def update(self, held_now):
        self.was_held = self.held
        self.held = held_now

    def just_pressed(self):
        return self.held and not self.was_held

    def just_released(self):
        return self.was_held and not self.held
```

Trace it. The top row is what the player's finger does, one column per frame.

| Frame | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| held | no | yes | yes | yes | no | no | yes |
| just_pressed | no | **yes** | no | no | no | no | **yes** |
| just_released | no | no | no | no | **yes** | no | no |

Two presses, two `just_pressed` frames, one release. Two classic bugs come from picking the wrong column:

- **Jump on `held`.** The character jumps on frame 2, lands, and jumps again on the first grounded frame while the key is still down. The player holding Space bunny-hops forever.
- **Move on `just_pressed`.** The character moves for one frame per press, so walking requires hammering the key.

Rule of thumb: continuous actions read `held`, one-shot actions read `just_pressed`, and "charge and release" actions (a bow, a variable-height jump) use `just_released` to end the charge.

## 3. Worked example: coyote time and the jump buffer

### The hook

Celeste (2018) is a platformer known for precise, fair-feeling jumps. Its developers published the player code on GitHub, and the top of `Player.cs` contains the line `JumpGraceTime = 0.1f`. Further down, a block labelled "Jump Grace" resets a timer to that value on every frame the player stands on ground, and counts it down by the frame time while airborne. The jump code then checks whether the timer is still above zero. In plain words: in Celeste you can jump for a tenth of a second *after* running off a ledge. Most players never notice. They just feel that the game "didn't eat" a jump they pressed a moment too late.

Designers call this **coyote time**, after the cartoon coyote who runs off a cliff and hangs in the air until he looks down. Its twin is the **jump buffer**: if you press jump a moment *before* you land, the game remembers the press and jumps on the landing frame instead of throwing it away. Celeste calls `Input.Jump.ConsumeBuffer()` when it performs a jump, which shows the jump press is buffered and then used up. The released file does not include the buffer's length, so this lecture treats the buffer length as your design choice.

### The model

Two timers, both measured in **seconds**, plus edge detection:

```
since_ground  = 0 on any grounded frame, otherwise since_ground + dt
since_press   = 0 on a just_pressed frame, otherwise since_press + dt

can_jump   = since_ground ≤ C        (C = coyote window, seconds)
wants_jump = since_press  ≤ B        (B = buffer window, seconds)

jump if can_jump and wants_jump, then reset both timers so the press is used once
```

`dt` is the frame time from week 7. With `C = 0` and `B = 0`, this reduces to the strict rule "jump only if you press on a grounded frame". Every extra millisecond in `C` or `B` is forgiveness you chose to give.

The same rule in Python, runnable:

```python
class JumpInput:
    """Edge detection plus two forgiveness timers, all in seconds."""
    def __init__(self, coyote=0.1, buffer=0.1):
        self.coyote = coyote          # how long after leaving ground you may still jump
        self.buffer = buffer          # how long an early press is remembered
        self.was_held = False
        self.since_ground = 999.0     # seconds since we last stood on ground
        self.since_press = 999.0      # seconds since jump was last pressed

    def update(self, held, grounded, dt):
        just_pressed = held and not self.was_held       # edge detection
        self.was_held = held
        self.since_ground = 0.0 if grounded else self.since_ground + dt
        self.since_press = 0.0 if just_pressed else self.since_press + dt
        if self.since_ground <= self.coyote and self.since_press <= self.buffer:
            self.since_press = 999.0                    # consume the press
            self.since_ground = 999.0                   # one jump per ledge
            return True
        return False
```

Celeste writes the coyote half as a countdown (`timer = 0.1` on ground, `timer -= dt` in the air, jump if `timer > 0`). A countdown and our count-up with `≤` are the same rule. They can differ by one frame at the exact boundary, because of how each comparison treats "exactly equal".

### Numbers you can check

**Coyote window.** Run off a ledge at Celeste's top running speed, `MaxRun = 90` px/s. The last airborne frame on which jumping still works is the largest whole `k` with `k × dt ≤ C`. How far past the edge are you then? `distance = 90 × k × dt`.

| Frame rate | dt | Last allowed airborne frame | Time after edge | Distance past edge |
|---|---|---|---|---|
| 30 fps | 33.3 ms | 3 | 0.100 s | 9.00 px |
| 60 fps | 16.7 ms | 6 | 0.100 s | 9.00 px |
| 144 fps | 6.9 ms | 14 | 0.097 s | 8.75 px |

Check the 144 row: `0.1 × 144 = 14.4`, so frame 14 is the last whole frame, at `14 / 144 = 0.0972` s, and `90 × 0.0972 = 8.75` px. The window is the same *time* at every frame rate. That is exactly what the seconds-based timer buys you.

Now suppose a programmer "simplifies" the window to **6 frames**, because 6 frames is 0.1 s at 60 fps:

| Frame rate | 6 frames lasts | Distance past edge |
|---|---|---|
| 30 fps | 0.200 s | 18.00 px |
| 60 fps | 0.100 s | 9.00 px |
| 144 fps | 0.042 s | 3.75 px |

On a 144 Hz monitor the forgiveness shrinks to less than half. On a 30 fps laptop it doubles, and players can jump off thin air. Same code, three different games. Week 9 is about this whole family of bugs.

**Jump buffer.** At 60 fps with `B = 0.1` s, the running Python model gives:

| Pressed | Buffer 0 s | Buffer 0.1 s |
|---|---|---|
| 0.05 s before landing | no jump (the press happened in the air and was lost) | jump on the landing frame |
| 0.15 s before landing | no jump | no jump (outside the window) |

Notice what "no jump" means in the first row. The player *did* press jump. Your code saw a `just_pressed` edge on an airborne frame, found `can_jump` false, and forgot about it. On landing, the key is still held but `just_pressed` is false, so nothing happens. From the player's side, the game ignored a button press. That is the complaint in the "Why this matters" line.

### A visual you can move

Open the interactive. The top view is a side-on platform with a ledge, and a square character running right at 90 px/s. The bottom view is a timeline of frames, one tick per frame, with the "left the ground" moment at zero. Drag the press marker along the timeline, or press Space while the animation plays, to choose when jump is pressed. Sliders set `C` and `B` from 0 to 0.25 s, and a selector switches the frame rate (30, 60, 144) and the timer unit (seconds or frames).

The two views together show the idea. The top view shows a character who is clearly past the edge, yet jumps. The timeline shows why. The press landed inside the shaded coyote window. Switch the unit to "frames", set 6, and change the frame rate. The shaded window stretches and shrinks while the top view's jump succeeds or fails for the same press time.

### Cross-game recognition

The rule "accept an input that arrives a little early or a little late" appears far outside platformers. Look for two timers.

- **Celeste (2018).** Coyote time as a 0.1 s countdown reset on ground, decremented with the frame time. The jump press is buffered and consumed on use.
- **Godot's own input table.** `is_action_just_pressed` returns true "in the current frame or physics tick". That is a buffer of exactly one frame. If you check it in a node that doesn't run this frame, or twice in one frame, you get surprising results. Your own `since_press` timer is the same idea with a longer, chosen window.
- **Your text adventure from weeks 1 to 6.** The command line is an extreme buffer. The player types while the game prints, and the whole line waits until the game is ready to read it. Nothing is lost, however early it arrives. A real-time game can't wait forever, so it keeps the press for `B` seconds and then drops it.
- **Operating-system key repeat.** The mirror image. Instead of remembering one early press, it *invents* extra presses from a long hold. Games switch it off for gameplay for the same reason they add buffers: the game, not the OS, should decide how input maps to actions.

### Eyes-open design judgment

Forgiveness is a dial, not a feature you either have or don't.

- **Too small and the game feels broken.** Human reaction and timing are not frame-exact. With `C = B = 0`, a press one frame late fails. At 144 fps, one frame is under 7 ms.
- **Too large and the game feels floaty or wrong.** With `C = 0.25` s at 90 px/s, the player can jump from 22.5 px past the edge, visibly standing on air. A large buffer can fire a jump the player has already changed their mind about, for example pressing jump, then deciding to drop down.
- **Always consume.** Reset the buffer when it fires. Otherwise one press can trigger a jump on landing, and again on the next landing.
- **Measure in seconds.** Frame counts change meaning with frame rate, as the table shows.
- **Coyote time interacts with double jumps.** If the character has a double jump, decide whether a coyote-time jump counts as the ground jump or spends the air jump. Either is fine. Leaving it to chance is not, because players will find the case where they get three jumps.

Game feel is invisible when it works. Nobody writes "nice buffer" in a review. They write "tight controls".

### Check yourself (worked example)

1. At 120 fps with `C = 0.08` s, what is the last airborne frame on which a coyote jump works, and how far past the edge is a 90 px/s runner then?
2. A player presses jump 0.07 s before landing, at 60 fps. Does the jump fire with `B = 0.05`? With `B = 0.1`?
3. A programmer codes coyote time as "5 frames". At what frame rate does that equal Celeste's 0.1 s?

<details>
<summary>Answers</summary>

1. `0.08 × 120 = 9.6`, so frame 9, at `9 / 120 = 0.075` s. Distance `90 × 0.075 = 6.75` px.
2. No with `B = 0.05` (0.07 > 0.05). Yes with `B = 0.1`, on the landing frame.
3. `5 / fps = 0.1`, so 50 fps.

</details>

## 4. From input to movement

### Direction first

For a top-down or twin-stick game, read four actions into one vector:

```gdscript
var dir := Input.get_vector("move_left", "move_right", "move_up", "move_down")
```

Godot's documentation says the result has its length limited to 1 and a circular deadzone. That single call fixes the diagonal speed bug. Pressing right and down at once would naively give the direction `(1, 1)`. By Pythagoras its length is `√(1² + 1²) = √2 ≈ 1.41`, so a character moving along it goes 41% faster than one moving straight right. `get_vector` gives `(0.707, 0.707)` instead, whose length is 1, so diagonals are not 41% faster. (MA101 week 12 covers vector length properly.) A gamepad stick pushed halfway still gives a length near 0.5, so slow walking survives. If you build the vector yourself from four `is_action_pressed` calls, you must clamp it yourself. For a side-scroller, `Input.get_axis("move_left", "move_right")` gives one number from −1 to 1.

### Speed with acceleration

The simplest movement sets velocity straight from input: `velocity.x = dir.x * MAX_SPEED`. It feels stiff, because you go from 0 to full speed in one frame and stop just as fast. Most games instead move velocity *toward* a target by at most a fixed amount per second.

Celeste does exactly this. With `MaxRun = 90` and `RunAccel = 1000` (px/s²), its running code sets the horizontal speed to `Approach(Speed.X, max * moveX, RunAccel * mult * Engine.DeltaTime)`, where `mult` is 1 on the ground and `AirMult = 0.65` in the air. `Approach` moves a value toward a target by at most a given step and never overshoots. Godot has the same function built in as `move_toward`.

```gdscript
extends CharacterBody2D

const MAX_RUN := 90.0
const RUN_ACCEL := 1000.0
const AIR_MULT := 0.65

func _physics_process(delta: float) -> void:
    var move_x := Input.get_axis("move_left", "move_right")
    var mult := 1.0 if is_on_floor() else AIR_MULT
    velocity.x = move_toward(velocity.x, move_x * MAX_RUN, RUN_ACCEL * mult * delta)
    move_and_slide()
```

In Python, so you can test it:

```python
def approach(value, target, max_step):
    if value < target:
        return min(value + max_step, target)
    return max(value - max_step, target)
```

Time to reach top speed from standing is `MAX_RUN / (RUN_ACCEL × mult)`:

| Where | Acceleration | Time to 90 px/s | Frames at 60 fps |
|---|---|---|---|
| Ground | 1,000 px/s² | 0.090 s | 6 (5.4 rounded up) |
| Air | 650 px/s² | 0.138 s | 9 (8.3 rounded up) |

Six frames is fast enough to feel instant and slow enough to read as weight. The lower air value gives the player slightly less steering in the air, which is a design statement about commitment. Try `RUN_ACCEL = 300` (0.3 s to top speed) and the character feels like it is on ice. Both are valid, for different games. The point is that acceleration is a number you tune, and `delta` in the step keeps the feel identical at any frame rate.

### Where to read input

Read input in the same callback that uses it. Movement and jumping that use physics belong in `_physics_process`, so read them there. A pause toggle belongs in `_unhandled_input`. Mixing them causes subtle bugs. For example, calling `is_action_just_pressed` in `_process` to trigger something that `_physics_process` performs can miss or double a press when the two run at different rates, a problem week 9 explains fully.

## In-class activity (25 minutes)

Pairs, Godot open, starting from any `CharacterBody2D` with a floor and a ledge.

1. Implement the strict jump: `if is_on_floor() and Input.is_action_just_pressed("jump")`. One partner plays, and the other counts failed jumps off the ledge's edge in 20 attempts at "jump as late as possible".
2. Add coyote time and a buffer in seconds, using the two-timer model. Start with `C = B = 0.1`. Repeat the 20 attempts. Record the failure count.
3. Set `C = 0.3`. Play for one minute. Write one sentence on how it feels.
4. Replace your seconds timer with a 6-frame counter. Set *Project Settings → Application → Run → Max FPS* to 30, play, then set it to 144 (or as high as your screen allows) and play again. Describe the difference.

Expected output: two failure counts from steps 1 and 2, one sentence from step 3, and a two-sentence comparison from step 4 that uses the phrase "frames per second" and a number.

## Common misconceptions

- **"Players who miss jumps just need to get better."** Players press within a spread of tens of milliseconds. A game with no forgiveness punishes normal human timing, not a lack of skill.
- **"`is_action_pressed` and `is_action_just_pressed` are interchangeable."** One reports a state, the other a change. Jump on the state and you bunny-hop. Walk on the change and you stutter.
- **"Coyote time is a cheat."** It is a design parameter. Its size decides how precise your game feels, and it should be tuned like any other number.
- **"Six frames is 0.1 seconds."** Only at 60 fps. Store windows in seconds and compare against accumulated `delta`.

## Check yourself

1. Fill in the `just_pressed` and `just_released` rows for held states `no, yes, no, yes, yes, no`.
2. A shooter fires when `Input.is_action_pressed("fire")` and the weapon's cooldown has expired. Is `held` the right choice here? What changes if you switch to `just_pressed`?
3. Using Celeste's constants, how long does it take to stop from full speed on the ground if there is no input (target 0, same `RUN_ACCEL`)? In the air?
4. A game runs input and jumping in `_physics_process` at 60 ticks per second but draws at 144 fps. A student moves the `is_action_just_pressed("jump")` check into `_process` and sets a flag that `_physics_process` reads. What goes wrong if the flag is never cleared, and what if it is cleared in `_process` every frame?

<details>
<summary>Answers</summary>

1. `just_pressed`: no, yes, no, yes, no, no. `just_released`: no, no, yes, no, no, yes.
2. Yes for an automatic weapon: holding means keep firing, and the cooldown sets the rate. With `just_pressed` it becomes semi-automatic, one shot per press, which is a different design (and a different feel).
3. `90 / 1000 = 0.09` s on the ground. In the air `90 / 650 ≈ 0.138` s.
4. Never cleared: the flag stays true and the character jumps again on every landing, like jumping on `held`. Cleared every render frame: `_process` runs about 2.4 times per physics tick, so the flag is often cleared before any physics tick reads it, and presses are lost. Read the input where you use it, or clear the flag only when the physics code consumes it.

</details>

## Lab / assignment hook

[Lab 08, input you can trust](../labs/lab08.md). You replay recorded input logs through an edge detector and the two-timer jump model in Python, measure how many presses a strict jump drops, compare seconds and frames at three frame rates, and tune `C`, `B` and acceleration for a short Godot level.

## Sources

- NoelFB, `Celeste` repository, `Source/Player/Player.cs` (file history from March 2019; code from the released game, Celeste, 2018). `JumpGraceTime = 0.1f`; the "Jump Grace" block resetting the timer on ground and subtracting `Engine.DeltaTime` in the air; jump when `jumpGraceTimer > 0`; `Input.Jump.ConsumeBuffer()`; `MaxRun = 90f`, `RunAccel = 1000f`, `AirMult = .65f`; horizontal speed set with `Calc.Approach(Speed.X, max * moveX, RunAccel * mult * Engine.DeltaTime)`. https://github.com/NoelFB/Celeste
- Godot Engine documentation 4.7 (stable), class reference "Input". `is_action_pressed`, `is_action_just_pressed` and `is_action_just_released` ("in the current frame or physics tick"); `get_vector` length limited to 1 with a circular deadzone; `get_axis`. https://docs.godotengine.org/en/stable/classes/class_input.html
- Godot Engine documentation 4.7, class reference "InputEvent". `is_echo`: repeated key events, typically about 20 per second after roughly half a second of holding, configurable by the user; `is_action_pressed` ignores echoes unless `allow_echo` is true. https://docs.godotengine.org/en/stable/classes/class_inputevent.html
- Godot Engine documentation 4.7, "Using InputEvent". Event propagation order; `_unhandled_input` recommended for gameplay input so the GUI can intercept events. https://docs.godotengine.org/en/stable/tutorials/inputs/inputevent.html
- Nystrom, R. (2014). *Game Programming Patterns*, "Game Loop". Processing input as one step of the loop. https://gameprogrammingpatterns.com/game-loop.html

## Interactive spec: examples/w08-jump-forgiveness.html

**Purpose.** Show that a jump pressed after leaving a ledge (or before landing) succeeds or fails because of two timer windows, and that windows measured in frames change size with frame rate while windows measured in seconds do not.

**Layout.** Two linked views, stacked (world on top, timeline below) at all widths.

- **World view.** Canvas 640 × 200 logical px. Ground from x = 0 to x = 320 (the ledge edge), a pit after it, and a landing platform from x = 370 to 640 at the same height. A 16 × 16 square character runs right at 90 px/s starting at x = 230, so it reaches the edge at t = 1.0 s from start. Once past the edge it falls under gravity 900 px/s² (Celeste's `Gravity`, for look only). If a jump fires, apply an upward velocity of 300 px/s and continue the 90 px/s horizontal run so the character clears the pit when the jump fires within the coyote window. Draw a ghost marker at the x where jump was pressed and a second marker where it fired, with the distance past the edge in px.
- **Timeline view.** Horizontal axis from −0.3 s to +0.3 s around the event (left the ground in coyote mode; landing in buffer mode). One tick per simulated frame. Shade the coyote window `[0, C]` after the edge (coyote mode) or the buffer window `[−B, 0]` before landing (buffer mode). A draggable press marker (also movable with arrow keys, 1 ms per press, 10 ms with Shift). The frame on which the press is registered is highlighted. The frame on which the jump fires, if any, is marked with a filled dot, or the label "press lost" appears.

**Controls.**
- Mode toggle: "Late press (coyote)" / "Early press (buffer)". In buffer mode, the world view starts the character falling onto the landing platform, landing at t = 0.
- `C` slider 0 to 0.25 s, step 0.01, default 0.10. `B` slider 0 to 0.25 s, step 0.01, default 0.10.
- Frame rate selector: 30, 60, 144.
- Unit toggle: "seconds" / "frames". In frames mode, the sliders become integer frame counts 0 to 15 (default 6) and the window's time length is `frames / fps`.
- Play/replay button, and Space to press jump live during playback.

**Model (must match exactly).** Per frame `k` with `dt = 1/fps`: `just_pressed = held_k and not held_{k-1}`; `since_ground = 0 if grounded else since_ground + dt`; `since_press = 0 if just_pressed else since_press + dt`; jump if `since_ground ≤ C_seconds and since_press ≤ B_seconds`, then reset both timers to a large number. In frames mode, compare frame counters against integer windows instead, with `≤`. A press at time `p` is registered on the first frame with `k × dt ≥ p`.

**Readouts.** Press time, registered frame and its time, fire frame (or "lost"), distance past edge at fire time `90 × t_fire` to 2 decimals, window length in seconds and in frames.

**Insight the first screen must show.** Load in coyote mode, 60 fps, seconds, `C = 0.10`, press marker at +0.08 s: the world shows the character jumping from 7.5 px past the edge and clearing the pit, and a line of text reads "Pressed 0.08 s late. Jumped anyway." Setting `C = 0` makes the character fall.

**Test values.**
- Coyote, seconds, `C = 0.10`, press +0.05 s: 30 fps fires on frame 2 (t = 0.067, 6.00 px); 60 fps frame 3 (0.050 s, 4.50 px); 144 fps frame 8 (0.056 s, 5.00 px).
- Coyote, seconds, `C = 0.10`, press +0.15 s: falls at all three frame rates.
- Coyote, seconds, `C = 0.10`: last successful press frame is 3 at 30 fps (9.00 px), 6 at 60 fps (9.00 px), 14 at 144 fps (8.75 px).
- Coyote, frames, window 6: window lasts 0.200 s at 30 fps, 0.100 s at 60, 0.042 s at 144. Press +0.08 s succeeds at 30 and 60 fps and fails at 144 fps.
- Buffer, seconds, 60 fps, `B = 0.10`, press −0.05 s: fires on the landing frame (frame 0). With `B = 0`: "press lost". Press −0.15 s with `B = 0.10`: "press lost".

**Accessibility.** Every control is keyboard operable; the press marker has an `aria-valuetext` like "press at 0.08 seconds after the edge"; results are announced in a polite live region; reduced motion shows the final frame of each attempt without animation; light and dark themes from the shared tokens.

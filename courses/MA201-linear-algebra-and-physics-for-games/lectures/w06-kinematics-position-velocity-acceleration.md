# MA201 · Week 06 — Kinematics: Position, Velocity, Acceleration

**Why this matters:** Every moving thing in a game is described by three vectors that are rates of each other. Position changes at the velocity, velocity changes at the acceleration. Once you can move between them, and between the frames of reference they are measured in, you can answer design questions that otherwise take a day of playtesting: will the player land back on the moving platform, why does the elevator jump feel short, how fast is that player really running.

**You will be able to:**
- Compute velocity and acceleration vectors from sampled positions with forward and central differences, and estimate their error and their sensitivity to noise.
- Predict position and velocity under constant acceleration in 2D or 3D by treating each axis separately.
- Derive relative velocity and acceleration between two frames of reference, and use them to compute where a player lands after jumping from a moving platform under each of Godot's three `platform_on_leave` modes.
- Compute the velocity and centripetal acceleration of a point on a rotating platform, and critique a moving-platform design against those numbers.

**Before class:** Millington, *Game Physics Engine Development* (2nd ed., 2010), chapter 2, the section on calculus (differential and integral calculus for vectors), and chapter 3 up to the first-law discussion. Dunn & Parberry, *3D Math Primer* (2nd ed., 2011), chapter 3 on multiple coordinate spaces, the part on nested spaces. Re-read your MA201 week 1 notes on the cross product.

**Prerequisites from earlier courses:** [MA101 week 2, linear functions and rates](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w02-linear-functions-and-rates.md) (rate of change as slope). [MA101 week 3, quadratic curves](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w03-polynomials-and-quadratic-curves.md) (designing a jump from height and time, including Celeste's jump; not repeated here). [CS101 week 9, delta time](../../CS101-programming-for-games-i/lectures/w09-delta-time-and-frame-rate-independence.md) (per-second rates in code, the fixed timestep). Looking ahead, [CS203 week 2, steering behaviors](../../CS203-artificial-intelligence-for-games/lectures/w02-steering-behaviors.md) (next semester) uses the braking distance `v²/(2a)`. MA201 [week 1](w01-vectors-in-3d-and-the-cross-product.md) (cross product) and [week 3](w03-transform-hierarchies-local-and-world-space.md) (local and world space).

**Interactive:** [`examples/w06-moving-platform.html`](../examples/w06-moving-platform.html). Keep it open during section 3.

---

## 1. Three vectors that are rates of each other

**Kinematics** is the description of motion without asking what causes it. Forces and mass come in week 8. This week you only need three quantities, each a vector in 2D or 3D:

- **Position** `r(t)`, where the object is at time `t`.
- **Velocity** `v(t)`, how fast position is changing, and in which direction. Its length `|v|` is the **speed**. Velocity is a vector and speed is a number. A character running in a circle at constant speed has a velocity that changes every frame.
- **Acceleration** `a(t)`, how fast velocity is changing. It can change speed (pressing the stick harder), direction (turning), or both.

"How fast something changes" has a precise meaning. Over a short time `Δt`, the position changes by `Δr = r(t + Δt) − r(t)`, and the **average velocity** over that interval is `Δr / Δt`. Shrink `Δt` toward zero and the average settles on one value, the **instantaneous velocity**, called the **derivative** of position:

```
v(t) = dr/dt = lim (Δt → 0) of [ r(t + Δt) − r(t) ] / Δt
a(t) = dv/dt
```

In MA101 week 2 you met rate of change as the slope of a line. The derivative is the slope of a curve at one point, the slope of the line that just touches it there. For a vector, take the derivative of each component separately. If `r(t) = (x(t), y(t), z(t))`, then `v(t) = (x′(t), y′(t), z′(t))`.

Going the other way, position is the running total of velocity, and velocity is the running total of acceleration. On a graph of velocity against time, the **area under the curve** between two times is the change in position. In MA101 week 3 you used exactly this, reading jump height off the area of a velocity graph made of straight pieces. That running total is called the **integral**. Week 7 is about computing it step by step in a game loop, and what goes wrong when you do. This week stays with cases where you can write the answer exactly.

### Derivatives from samples

A game never has `r(t)` as a formula for a player. It has samples, one per physics tick or one per network packet. You estimate the derivative from them with **finite differences**:

```
forward difference:   v ≈ [ r(t + h) − r(t) ] / h
central difference:   v ≈ [ r(t + h) − r(t − h) ] / (2h)
second difference:    a ≈ [ r(t + h) − 2·r(t) + r(t − h) ] / h²
```

Here `h` is the time between samples. The central difference is the slope across a window centered on `t`, and it is usually far more accurate for the same `h`. Try it on a platform that slides back and forth along `x(t) = 200 · sin(πt/2)` pixels, sampled every `h = 0.1` s. Near `t = 0.5` the samples are 117.56, 141.42 and 161.80 px.

```python
import math

def x(t):
    return 200 * math.sin(math.pi * t / 2)

t, h = 0.5, 0.1
forward = (x(t + h) - x(t)) / h
central = (x(t + h) - x(t - h)) / (2 * h)
second = (x(t + h) - 2 * x(t) + x(t - h)) / h**2
true_v = 200 * (math.pi / 2) * math.cos(math.pi * t / 2)
true_a = -200 * (math.pi / 2) ** 2 * math.sin(math.pi * t / 2)
print(f"forward {forward:7.2f}  central {central:7.2f}  true v {true_v:7.2f} px/s")
print(f"second difference {second:8.2f}  true a {true_a:8.2f} px/s^2")
```

Output:

```
forward  203.82  central  221.23  true v  222.14 px/s
second difference  -348.23  true a  -348.94 px/s^2
```

The forward difference is 8% low. It measures the average velocity over the next 0.1 s, and the platform is slowing down. The central difference is within 0.4%. Its error shrinks with `h²` instead of `h`, so halving the sampling interval cuts it by four.

### Differences amplify noise

There is a catch you will meet in any real log. Suppose each recorded position can be off by up to `e = 0.5` px, from rounding or network compression. A difference of two such samples can be off by `2e`, and dividing by a small `h` magnifies it. At 60 samples per second (`h = 1/60`), the forward-difference velocity can be off by up to `2e / h = 60` px/s. The second difference can be off by `4e / h² = 7,200` px/s², which is more than seven times the gravity of Godot's 2D default.

So velocity estimated from positions is usable, and acceleration estimated from positions is mostly noise unless you smooth first or sample more coarsely. When a game needs acceleration (to detect a speed hack's impossible burst, or to drive an animation's lean), it should send or record velocity directly, or average over several ticks. CS202's [server authority lecture](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w04-server-authority-never-trust-the-client.md) checks movement against a maximum speed for exactly this reason. Speed is one difference away from the data. Acceleration is two.

## 2. Constant acceleration, one axis at a time

When acceleration is constant, the running totals have exact formulas. In vector form:

```
v(t) = v₀ + a·t
r(t) = r₀ + v₀·t + ½·a·t²
```

- `r₀` and `v₀` are the position and velocity at `t = 0`.
- `a` is the constant acceleration vector, for example gravity `(0, −980)` px/s² in a y-up 2D game.

The formula is the one-dimensional jump of MA101 week 3, written with vectors. The useful fact is that **each axis is independent**. With gravity pointing straight down, the horizontal velocity never changes, and the vertical motion is the same parabola whether or not the object is moving sideways. You can solve the vertical problem for air time, then multiply by horizontal speed for distance.

Two consequences you will use repeatedly:

```
time to apex     t_apex = v₀y / g
air time         T = 2·v₀y / g         (landing at take-off height)
apex height      h = v₀y² / (2g)
```

Godot's 2D character template uses a jump velocity of 400 px/s (written −400, because Godot's 2D y axis points down) and a default gravity of 980 px/s². So `T = 800 / 980 = 0.816` s and `h = 160,000 / 1,960 = 81.6` px. Those two numbers are the baseline for the worked example.

## 3. Worked example: jumping off a moving platform

### The hook

Stand on a moving platform in Celeste, jump, and you carry the platform's speed with you. The published player code calls this a **lift boost**. When Madeline jumps, the game adds the platform's velocity to hers, capped at 250 px/s sideways and 130 px/s upward. A platform moving down adds nothing. Walk off a platform that is rising and she keeps its upward speed.

Godot 4 exposes the same choice as a property on every `CharacterBody2D` and `CharacterBody3D`, `platform_on_leave`, with three options: add the platform's velocity, add only its upward part, or do nothing.

Why would a game designer and an engine both need a rule for this, and why would Celeste throw away the downward part? The answer is a kinematics fact about frames of reference.

### The model

A **frame of reference** is the viewpoint you measure positions from. The world is one frame. A moving platform is another. Let `r_p(t)` be the platform's position in the world, and `r_rel(t)` the player's position measured from the platform (its local space from week 3, with no rotation for now). Then

```
r(t)  = r_p(t) + r_rel(t)
v(t)  = v_p(t) + v_rel(t)
a(t)  = a_p(t) + a_rel(t)
```

The first line is the local-to-world rule. The other two follow by taking the derivative of each side. The player's world velocity is the platform's velocity plus the velocity relative to the platform. Velocities of frames add. This is **relative motion**, and it is the whole model.

Now read a jump through it. While the player stands on the platform, `v_rel = 0`, so the player's world velocity is `v_p`. The jump adds `v_jump = (0, 400)` relative to whatever the player was already doing. At the instant of leaving, the engine chooses the player's new world velocity. Godot's three modes are three choices:

```
ADD_VELOCITY           v = v_jump + v_p
ADD_UPWARD_VELOCITY    v = v_jump + (v_p.x, max(v_p.y, 0))
DO_NOTHING             v = v_jump
```

After take-off, the player feels gravity only, and the platform keeps doing whatever it does. Whether the player comes down in the same spot on the platform depends on the relative motion. Subtract the platform's motion from the player's, and in the platform's frame

```
r_rel(t) = r_rel(0) + (v(0) − v_p(0))·t + ½·(g − a_p)·t²
```

Two terms decide everything. The **inherited velocity mismatch** `v(0) − v_p(0) − v_jump`, and the **platform's acceleration** `a_p`. If the engine inherits the full velocity and the platform moves at constant velocity (`a_p = 0`), then in the platform's frame the jump is exactly an ordinary jump. The player lands where they took off. That is why Godot's documentation calls adding the velocity the physically accurate default.

### Numbers you can check

Use Godot's template values: jump 400 px/s, gravity 980 px/s², baseline air time 0.816 s and apex 81.6 px. The player stands still on the platform and presses jump.

**A platform moving sideways at 150 px/s.** During 0.816 s the platform travels `150 × 0.816 = 122.4` px.

| Mode | Player's world vx | Player moves | Lands relative to take-off spot on the platform |
|---|---|---|---|
| ADD_VELOCITY | 150 | 122.4 px | 0 px |
| ADD_UPWARD_VELOCITY | 150 | 122.4 px | 0 px |
| DO_NOTHING | 0 | 0 px | 122.4 px behind |

With `DO_NOTHING`, a platform 100 px wide slides out from under a player who jumps from its center.

**An elevator moving vertically at 100 px/s.** Now the modes differ. "Apex" is the height gained, measured in whichever frame the column says.

| Elevator | Mode | World launch speed | Apex in world | Launch speed relative to elevator | Apex above elevator floor | Time until landing on elevator |
|---|---|---|---|---|---|---|
| Up 100 | ADD_VELOCITY | 500 | 127.6 px | 400 | 81.6 px | 0.816 s |
| Up 100 | DO_NOTHING | 400 | 81.6 px | 300 | 45.9 px | 0.612 s |
| Down 100 | ADD_VELOCITY | 300 | 45.9 px | 400 | 81.6 px | 0.816 s |
| Down 100 | ADD_UPWARD_VELOCITY | 400 | 81.6 px | 500 | 127.6 px | 1.020 s |

Check one row. Descending elevator, `ADD_UPWARD_VELOCITY`: the downward platform velocity is dropped, so the world launch speed is 400. Relative to the elevator, which is moving at −100, that is `400 − (−100) = 500`. Relative apex `500² / 1,960 = 127.6` px, relative air time `2 × 500 / 980 = 1.020` s.

The table explains Celeste's rule. With full inheritance on a descending elevator, the jump looks right relative to the elevator but reaches only 45.9 px of world height. If the next ledge is fixed to the world, the player cannot reach it. Dropping the downward part keeps the world jump at its designed 81.6 px. Rising platforms add height, which is a reward rather than a problem, so Celeste keeps that part and caps it.

**An accelerating platform.** A mine cart speeds up at a constant `a_p = 200` px/s² while the player is in the air. Full velocity inheritance matches the cart's velocity at take-off, but the cart keeps accelerating. In the cart's frame the player drifts back by `½ · a_p · T² = ½ × 200 × 0.816² = 66.6` px. No choice of inherited velocity fixes this. The only kinematic fix is to keep the player attached to the cart's frame while airborne, and that is a design decision rather than physics.

Here is the whole table as code:

```python
g, jump, T = 980.0, 400.0, 800.0 / 980.0

def launch(mode, vp):
    vx, vy = vp
    if mode == "add":
        return vx, jump + vy
    if mode == "upward":
        return vx, jump + max(vy, 0.0)
    return 0.0, jump

for vp in [(150.0, 0.0), (0.0, 100.0), (0.0, -100.0)]:
    for mode in ["add", "upward", "nothing"]:
        vx, vy = launch(mode, vp)
        rel_vy = vy - vp[1]
        air = 2 * rel_vy / g                      # time until landing on the platform
        drift = (vx - vp[0]) * air                # sideways miss, relative to the platform
        print(f"vp={vp!s:13} {mode:8} world apex {vy**2/(2*g):6.1f}  "
              f"rel apex {rel_vy**2/(2*g):6.1f}  air {air:.3f}  drift {drift:6.1f}")
print(f"cart drift {0.5 * 200 * T**2:.1f} px")
```

Output:

```
vp=(150.0, 0.0)  add      world apex   81.6  rel apex   81.6  air 0.816  drift    0.0
vp=(150.0, 0.0)  upward   world apex   81.6  rel apex   81.6  air 0.816  drift    0.0
vp=(150.0, 0.0)  nothing  world apex   81.6  rel apex   81.6  air 0.816  drift -122.4
vp=(0.0, 100.0)  add      world apex  127.6  rel apex   81.6  air 0.816  drift    0.0
vp=(0.0, 100.0)  upward   world apex  127.6  rel apex   81.6  air 0.816  drift    0.0
vp=(0.0, 100.0)  nothing  world apex   81.6  rel apex   45.9  air 0.612  drift    0.0
vp=(0.0, -100.0) add      world apex   45.9  rel apex   81.6  air 0.816  drift    0.0
vp=(0.0, -100.0) upward   world apex   81.6  rel apex  127.6  air 1.020  drift    0.0
vp=(0.0, -100.0) nothing  world apex   81.6  rel apex  127.6  air 1.020  drift    0.0
cart drift 66.6 px
```

### The visual

Open [`examples/w06-moving-platform.html`](../examples/w06-moving-platform.html). The top panel shows the jump in the world frame, with a platform sliding right and the player's arc. The bottom panel shows the same jump drawn in the platform's frame, with the platform fixed in place.

Set the mode to "add velocity" and the platform to a constant 150 px/s. The top arc is a long, lopsided-looking parabola, and it lands on the platform. The bottom panel shows a plain vertical jump, straight up and down, identical to jumping on solid ground. Switch to "do nothing" and the bottom panel shows the truth: relative to the platform, the player was thrown backwards at 150 px/s. Now choose the "accelerating cart" motion with "add velocity". The world arc still looks reasonable, but the platform-frame arc curls backwards. That curl is `−½ · a_p · t²`, and it is why your players fall off accelerating carts.

### Cross-game recognition

**Celeste (2018, published player source, `Player.cs`).** The `LiftBoost` property caps the platform speed at 250 horizontally and 130 upward, and zeroes any downward component. `Jump()` adds it to Madeline's speed. When she walks off a rising platform without jumping, the game also sets her vertical speed to the lift's upward speed. In the model's terms, Celeste chose `ADD_UPWARD_VELOCITY` with caps.

**Godot 4 (class reference, `CharacterBody2D.platform_on_leave`).** Three documented modes, with `ADD_VELOCITY` the default, described as physically accurate, and `ADD_UPWARD_VELOCITY` recommended for keeping full jump height when the platform moves down. That is Celeste's reasoning written into an engine. A subtle trap is in Godot's own starter template. Its air control does `velocity.x = move_toward(velocity.x, 0, SPEED)` when no direction is held, with `SPEED = 300` subtracted per physics tick. Any inherited platform velocity under 300 px/s is erased on the first tick in the air, so a player who jumps without holding a direction behaves as if the mode were `DO_NOTHING`. The flag and the movement code must agree.

**World of Warcraft transports (Wrath of the Lich King 3.3.5a, as reconstructed by the TrinityCore server emulator).** Boats and zeppelins carry players across the sea. TrinityCore's movement record for a unit includes a transport GUID and a position offset relative to the transport, and the server computes the passenger's world position from the transport's position and orientation plus that offset. This is the first line of the model, `r = r_p + r_rel`, with a rotation added. Storing the relative position is the "keep the player attached to the moving frame" fix from the mine-cart case. A player walking on a deck stays on the deck however the ship moves, because their position is never stored in the world frame at all. This describes the emulator's reconstruction of the protocol, not Blizzard's own server code.

Three products, one equation. When you meet a moving platform, ask: *which frame is the player's position stored in, and what velocity does the player get when the frames separate?*

### Eyes-open design judgment

- **Inherit velocity by default, and decide the vertical part deliberately.** Full inheritance makes constant-velocity platforms behave exactly like the ground, which is what players expect. Dropping the downward part protects world-fixed jump heights. Dropping everything (`DO_NOTHING`) makes every fast platform a trap.
- **Cap what you inherit.** A platform moving at 600 px/s would launch a player across the level. Celeste's caps (250 and 130) keep lift boosts useful without breaking the level's geometry. Choose caps from the gaps you want reachable, using the air-time formula.
- **Accelerating platforms break velocity inheritance.** If a platform speeds up, slows down, or reverses during a jump, the player lands `½ · a_p · T²` from where they expect. Either keep the jump short compared to the platform's rhythm, keep players attached to the platform's frame while airborne, or give players a visible cue to jump at the constant-speed part of the path.
- **Test with the input released.** Many "inheritance is broken" reports are the air-control code erasing the inherited velocity, as in Godot's template. Write a test that jumps without holding a direction.

## 4. Rotating platforms: velocity without speed change

Platforms also spin. Think of a turntable, a rotating log, or the deck of a turning ship. A point fixed on a platform rotating at angular velocity `ω` (a vector along the rotation axis, length in radians per second) has velocity

```
v = ω × r_rel
```

where `r_rel` runs from the rotation center to the point. You met the cross product in [week 1](w01-vectors-in-3d-and-the-cross-product.md). Its direction is perpendicular to both the axis and the radius, so the point moves along the circle, and its size is `|ω| · |r_rel|` when the radius is perpendicular to the axis.

That point moves at constant speed, yet it accelerates the whole time, because its velocity keeps turning. The acceleration points to the center and has size

```
|a| = ω² · r = v² / r
```

This is **centripetal acceleration**. A carousel turning at 1 rad/s carries a player standing 3 m out at 3 m/s, with 3 m/s² of acceleration toward the middle. The player's character controller must supply that acceleration, usually by being attached to the platform's frame. The moment it lets go (a jump), the player leaves along the tangent at 3 m/s, not along the radius. Players often expect to be thrown straight outward. The kinematics says sideways.

It connects to MA101 week 11, where a homing missile turning at a capped rate `ω` and speed `v` flies a circle of radius `v / ω`. Its centripetal acceleration is `v · ω`, which is how much sideways grip it needs. The same numbers describe how hard a car's tyres or a character's feet must push to hold a turn.

## In-class activity (25 minutes)

Groups of three. You are designing a moving-platform section for a 2D platformer using Godot's template jump (400 px/s, 980 px/s², run speed 300 px/s).

1. Choose a `platform_on_leave` mode and caps for inherited velocity. Justify both in two sentences.
2. Design three platforms: one moving horizontally at a constant speed, one elevator, one that moves back and forth on a smooth path. For each, give the speed or path and the width.
3. For each platform, compute where a player standing at its center lands after a jump with no input held, in the platform frame. Use the model, then check in the interactive. Mark any case where the player lands off the platform.
4. Choose one fix for the worst case from the design judgment list and recompute.

Expected output: a mode choice with caps, a table of three platforms with landing offsets, and one fixed design with its new number.

## Common misconceptions

- **"Constant speed means no acceleration."** Constant velocity means no acceleration. A point on a turntable has constant speed and an acceleration of `v²/r` toward the center.
- **"If the player keeps the platform's velocity, they always land on the platform."** Only if the platform's velocity stays constant during the jump. Any platform acceleration gives a drift of `½ · a_p · T²`.
- **"Velocity from positions is as good as the positions."** Each difference divides the sample error by `h`. Velocity is usable, acceleration from raw positions is mostly noise at 60 Hz.
- **"Leaving a spinning platform throws you straight outward."** You leave along the tangent, at the speed of the point you stood on.

## Check yourself

1. A drone's samples at `t = 0.9`, `1.0` and `1.1` s are `(10.0, 4.0)`, `(12.0, 4.5)` and `(14.4, 4.8)` m. Estimate its velocity at `t = 1.0` with a central difference and its acceleration with a second difference.
2. With Godot's template jump, a platform moves right at 250 px/s and the mode is `DO_NOTHING`. How far from the take-off spot on the platform does the player land? How wide must the platform be for a player at its center to land on it?
3. An elevator descends at 150 px/s. Compute the world apex and the apex above the floor under `ADD_VELOCITY` and `ADD_UPWARD_VELOCITY`.
4. A player stands 4 m from the center of a platform rotating at 0.5 rad/s and jumps. What is their horizontal speed at take-off, relative to the world, and in which direction?
5. Positions are logged with error up to 0.25 m at 20 samples per second. What is the worst-case error of a forward-difference speed? Would a speed check with a limit of 7 m/s and a tolerance of 1 m/s produce false positives?

<details>
<summary>Answers</summary>

1. Velocity `((14.4 − 10.0) / 0.2, (4.8 − 4.0) / 0.2) = (22, 4)` m/s. Acceleration `((14.4 − 24 + 10) / 0.01, (4.8 − 9 + 4) / 0.01) = (40, −20)` m/s².
2. `250 × 0.816 = 204.1` px behind the take-off spot. The platform would need to be more than 408 px wide.
3. `ADD_VELOCITY`: world launch 250, world apex `250² / 1,960 = 31.9` px, relative launch 400, apex above floor 81.6 px. `ADD_UPWARD_VELOCITY`: world launch 400, world apex 81.6 px, relative launch 550, apex above floor `550² / 1,960 = 154.3` px.
4. `v = ω · r = 0.5 × 4 = 2` m/s, along the tangent of the circle at that point (perpendicular to the radius, in the direction of rotation).
5. `2e / h = 2 × 0.25 × 20 = 10` m/s. A player running at exactly 7 m/s can appear to run at up to 17 m/s for one sample, so a 1 m/s tolerance would flag honest players. Use a central difference over a longer window, or check distance over a second instead of per sample.

</details>

## Lab / assignment hook

[Lab 06, moving frames](../labs/lab06.md). You implement finite differences, the three leave modes and the platform-frame landing prediction in Python, test them against this lecture's tables, then analyse a recorded log of a player riding a back-and-forth platform to find the jump that went wrong. Deliverable: your `kinematics.py` passing the tests and a one-page design note choosing a leave mode and caps for your game.

## Sources

- NoelFB/Celeste repository on GitHub, `Source/Player/Player.cs` (published 2018; MIT licence covers the code files only). `LiftXCap = 250f`, `LiftYCap = -130f` (Celeste's y axis points down, so this is 130 upward); the `LiftBoost` property zeroes downward lift and clamps both components; `Jump()` adds `LiftBoost` to the speed; walking off a rising platform sets the vertical speed to the lift speed.
- Godot Engine class reference, `CharacterBody2D` (master branch, 4.8-dev, September 2026; present in the 4.x series). `platform_on_leave` with `PLATFORM_ON_LEAVE_ADD_VELOCITY` (default, described as physically accurate), `PLATFORM_ON_LEAVE_ADD_UPWARD_VELOCITY` (keeps full jump height when the platform moves down) and `PLATFORM_ON_LEAVE_DO_NOTHING`.
- Godot Engine source, `modules/gdscript/editor/script_templates/CharacterBody2D/basic_movement.gd` (master branch, September 2026). `SPEED = 300.0`, `JUMP_VELOCITY = -400.0`, gravity added from `get_gravity()`, and `move_toward(velocity.x, 0, SPEED)` when no direction is held.
- Godot Engine class reference, `ProjectSettings` (master branch, September 2026). `physics/2d/default_gravity` default 980 px/s².
- TrinityCore, branch 3.3.5, `src/server/game/Entities/Object/MovementInfo.h`, `Object.h` and `Transport/Transport.h` (accessed September 2026). Movement info holds a transport GUID and a transport-relative position; `CalculatePassengerPosition` derives a passenger's world position from the transport's position and orientation. TrinityCore is a community server emulator for World of Warcraft: Wrath of the Lich King (client 3.3.5a), not Blizzard code.
- Millington, I. (2010). *Game Physics Engine Development*, 2nd ed. CRC Press. Chapters 2 and 3.
- Dunn, F. & Parberry, I. (2011). *3D Math Primer for Graphics and Game Development*, 2nd ed. CRC Press. Chapter 3.

## Interactive spec: examples/w06-moving-platform.html

**Purpose.** Make relative motion visible. The same jump drawn in the world frame and in the platform's frame, so students see that inheriting velocity turns a moving platform into still ground, and that platform acceleration bends the jump backwards however velocity is inherited.

**Layout.** Two stacked panels sharing one time axis, full width at both breakpoints. Top: world frame. Bottom: platform frame (platform drawn fixed at the center, the world scrolls). y up in both panels, 1 px of drawing per game pixel at 1280 width, scaled to fit at 390.

**Simulation.** Exact kinematics, no numerical integration. Gravity `g = 980` px/s² down. Jump velocity relative to the platform `(0, 400)`. The player stands at the platform's center until the jump at `t = 0`. Platform motions (select):
1. "Constant slide": `x_p(t) = 150·t`, `y_p = 0`. Speed slider 0 to 400 px/s, default 150.
2. "Elevator": `x_p = 0`, `y_p(t) = v_e·t`, `v_e` slider −200 to 200 px/s, default 100.
3. "Accelerating cart": `x_p(t) = v_c·t + ½·a_c·t²`, `v_c` default 100, `a_c` slider −400 to 400 px/s², default 200.
4. "Back and forth": `x_p(t) = 200·sin(ω(t + t₀))`, `ω = π/2`, a phase slider `t₀` from 0 to 4 s, default 1.0 (the turnaround point).
Launch velocity by mode, with `v_p` the platform velocity at `t = 0`: add velocity `v = (0, 400) + v_p`; add upward velocity `v = (0, 400) + (v_p.x, max(v_p.y, 0))`; do nothing `v = (0, 400)`. Optional caps: a checkbox "Celeste caps" that clamps `v_p.x` to ±250 and the upward part of `v_p.y` to 130 before adding. Player world position `r(t) = r_p(0) + v·t + ½·(0, −980)·t²`. Platform-frame position `r(t) − r_p(t)`. Landing: the first `t > 0` where the player's relative y returns to 0 while moving down; find it numerically on the exact formulas by stepping `t` in 0.001 s increments until the relative y changes sign, then refining inside that step by bisection (the example halves the bracket 60 times). Plain stepping without the refinement stops up to 0.001 s late and reads 122.5 and 143.3 instead of the test values 122.4 and 143.1. For the constant-velocity motions the landing time also has the closed form `2·(v.y − v_p.y)/g`, which you can use as a check.

**Controls (keyboard accessible).** Mode radio group (add, upward, nothing), platform-motion select, the sliders for the selected motion, "Celeste caps" checkbox, play/pause, and a time scrubber from 0 to the landing time. With `prefers-reduced-motion`, show the full arcs statically.

**Readouts (monospaced, 1 decimal).** Launch velocity (world), world apex height, apex above the platform, air time until landing on the platform, and horizontal landing offset relative to the take-off spot. Highlight the offset in a warning style when its size exceeds 50 px (the platform's half-width).

**The one insight.** On load (constant slide 150, mode add), the top panel shows a long slanted arc and the bottom panel a straight vertical jump that lands at offset 0.0. Switching the mode to "do nothing" turns the bottom arc into a backwards throw that lands at −122.4. Switching the motion to "accelerating cart" with mode add shows a backward curl in the bottom panel landing at −66.6 even though velocity was inherited.

**Test values.**
- Constant slide 150, add: air 0.8 s (0.816), offset 0.0. Do nothing: offset −122.4.
- Elevator +100, add: world apex 127.6, relative apex 81.6, air 0.8 (0.816). Do nothing: relative apex 45.9, air 0.6 (0.612).
- Elevator −100, add: world apex 45.9. Upward: world apex 81.6, relative apex 127.6, air 1.0 (1.020).
- Accelerating cart `v_c = 100`, `a_c = 200`, add: offset −66.6.
- Back and forth, `t₀ = 1.0`, add: launch x velocity 0.0, offset +143.1 (the platform has swung back toward the center by 143.1 px while the player stayed put).

**Style.** Shared palette from `templates/interactive-tokens.css`, inline. Player and platform as plain shapes, arcs as strokes with distinct dash patterns for the world and relative paths. No game art.

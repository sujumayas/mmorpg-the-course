# CS203 · Week 02 — Steering Behaviors

**Why this matters:** Movement is the first thing a player reads about an NPC, long before any decision. A guard who circles his post like a moth, or a zombie that stops dead and then lurches, looks stupid whatever its brain is doing. Steering behaviors are the small formulas that turn "go there" into motion that looks alive, and one line of physics tells you how to tune them.

**You will be able to:**
- Compute the steering request for seek, flee, arrive and pursue from positions, velocities and limits, and apply it with a frame-rate independent update.
- Derive the braking distance `v² / (2a)` and use it to predict seek's overshoot and to choose arrive's slowing radius.
- Implement seek, arrive and pursue in Python and measure overshoot, settle time and time to catch.
- Critique a blended steering system, name the stalemate it can fall into, and decide when steering is the wrong tool.

**Before class:** Craig Reynolds, "Steering Behaviors for Autonomous Characters" (Game Developers Conference 1999), free at red3d.com/cwr/steer/gdc99, sections on the vehicle model, seek and flee, pursuit and evasion, arrival and wander. Millington, *AI for Games* (3rd ed., 2019), chapter 3, the sections on kinematic movement and steering behaviors. Skim Andrew Fray, "Context Steering", *Game AI Pro 2* (2015), chapter 18, sections 18.1 and 18.2, free online.

**Prerequisites from earlier courses:** [CS203 week 1](w01-game-ai-vs-academic-ai.md) (artificial stupidity and the five tests). [MA101 week 12, 2D vectors](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w12-2d-vectors.md) (subtract, scale, normalize, clamp a length). [MA101 week 11, atan2 and turning](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w11-atan2-turning-toward-a-target.md) (homing missiles and the turning circle). [MA101 week 8, lerp and remap](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w08-interpolation-lerp-inverse-lerp-remap.md) (arrive's speed ramp is a remap). [CS101 week 9, delta time](../../CS101-programming-for-games-i/lectures/w09-delta-time-and-frame-rate-independence.md) (why every rate is multiplied by `dt`). [GD102 week 12, emergent behavior](../../GD102-systems-design-and-game-mechanics/lectures/w12-emergent-behavior-from-simple-rules.md) (Reynolds's boids and their three rules).

**Interactive:** [`examples/w02-seek-vs-arrive.html`](../examples/w02-seek-vs-arrive.html). Keep it open during section 2.

---

## 1. The vehicle model

Reynolds split character motion into three layers. **Action selection** decides the goal ("go to the door", "chase the player"). **Steering** turns that goal into a desired change of motion. **Locomotion** is the body that carries it out: legs, wheels, an animation system. This week is about the middle layer. Weeks 6 to 9 cover action selection. Locomotion belongs to your engine and animators.

Steering works on a simple body, a **point mass** with four numbers.

- `position`, a vector (MA101 week 12).
- `velocity`, a vector. Its length is the current speed.
- `max_speed`, the fastest the character can go.
- `max_accel`, the largest change in velocity per second the body can produce. Reynolds calls the equivalent limit `max_force` and divides by mass. We fold mass in and talk about acceleration directly, in m/s².

Every steering behavior answers one question. **What velocity would I like to have right now?** Call it the **desired velocity**. The steering request is the difference between what you want and what you have:

```
steering = desired_velocity − velocity
```

The body cannot deliver any request instantly, so each frame the request is **truncated** (clamped in length) to what `max_accel` allows in one frame, and then applied:

```
dv       = truncate(steering, max_accel × dt)
velocity = truncate(velocity + dv, max_speed)
position = position + velocity × dt
```

Here `dt` is the frame time, 1/60 s at 60 Hz. Multiplying by `dt` is what makes the motion the same on a 60 Hz and a 144 Hz screen (CS101 week 9). Updating the velocity first and then moving with the new velocity is called semi-implicit Euler, and it is the standard choice for games.

That is the whole machine. The behaviors differ only in how they compute `desired_velocity`.

- **Seek:** `desired = normalize(target − position) × max_speed`. Full speed straight at the target.
- **Flee:** the same vector, reversed. Full speed straight away.

A warning for readers of the original paper. The HTML version of Reynolds's paper writes seek as `normalize(position − target)`. That vector points away from the target, which is flee. Write `target − position`, and if your seeker runs away on its first test, check that line first.

Why a velocity *difference* and not simply "set velocity to desired"? Because the difference respects the body. A character running east who suddenly wants to go north cannot turn on the spot. With `max_accel` limiting the change per frame, it curves around, and the curve tightens or widens with the character's weight. A cat and a cargo truck can run the same seek code with different limits and look like a cat and a truck.

## 2. Worked example: why the guard circles his post

### The hook

Left 4 Dead (Valve, 2008) moves hundreds of infected through cluttered streets, and they pour around cars and each other rather than walking in straight lines between waypoints. In his 2009 talk on the game's AI, Michael Booth explains why. Following a computed path directly "looks robotic", so every actor in the game uses **reactive path following**. It moves toward a look-ahead point farther down the path and lets local obstacle avoidance handle props, corners and other bots. Booth notes that this combines well with the mob's flocking and gives fluid motion. In other words, the whole horde is seeking a point that keeps moving ahead of it.

Seek is perfect for a point that keeps moving away. It is terrible for a point that stops. Unity's documentation for its navigation agent says as much. Its `autoBraking` setting exists because an agent that needs to land close to its destination must brake, or it will overshoot and end up endlessly "orbiting" the target zone. The same page's component reference advises turning auto braking *off* for a guard on patrol, so the guard moves smoothly through waypoints instead of slowing at each one.

So when should an NPC brake, and how early? That is a number, and you can compute it.

### The model

**Braking distance.** A body moving at speed `v` that decelerates at its maximum `a` stops after

```
b = v² / (2a)
```

This is the same kinematics as a car's stopping distance. Every seek-based overshoot in this lecture comes from this one line.

**Seek overshoots by `b`.** A seeker runs at `max_speed` until it reaches the target. Only once it is *past* the target does its desired velocity flip, so only then does it start to brake. It travels `b` beyond the target before stopping, and then seeks back and passes through again at speed. Along a straight line the result is an oscillation of amplitude `b` that never dies out. Reynolds compares it to a moth buzzing around a light bulb. In two dimensions, any sideways velocity turns the oscillation into the orbit Unity's documentation describes.

**Arrive ramps the desired speed down.** Arrive is seek with a **slowing radius** `r`. Outside `r` it seeks at full speed. Inside, the desired speed falls in proportion to the distance `d` that is left:

```
desired_speed = max_speed × min(1, d / r)
```

That is a remap (MA101 week 8) of distance in `[0, r]` to speed in `[0, max_speed]`.

**Choosing `r`.** Two thresholds come from comparing the ramp with what the body can do.

1. If `r < b`, the agent cannot stop in time. Even braking at full strength from the moment it enters the radius, it needs `b` to stop, so it overshoots by about `b − r`.
2. If `r ≥ b`, it stops without overshooting. It may brake at full strength for a while, then join the ramp and follow it in.
3. If `r ≥ v² / a = 2b`, the agent can follow the ramp exactly from the moment it enters. On the ramp the deceleration needed is `(max_speed / r) × speed`, largest at the edge where speed is `max_speed`, so the condition is `max_speed² / r ≤ a`.

So the useful range for the slowing radius is **`b ≤ r ≤ 2b` and a little beyond**. Below `b` the NPC overshoots. Far above `2b` it arrives safely but slowly, for a reason the numbers will show.

### Numbers you can check

Take a soldier with `max_speed = 6` m/s and `max_accel = 12` m/s². The braking distance is `b = 6² / (2 × 12) = 1.5` m, and `2b = 3` m. Here is a one-dimensional simulation at 60 Hz. The soldier starts at rest at `x = 0` and heads for a target at `x = 20`.

```python
DT = 1 / 60                               # one frame at 60 Hz

def step(x, v, desired_v, max_accel):
    """One frame: steer velocity toward desired_v, limited by max_accel."""
    dv = desired_v - v                    # the steering request
    limit = max_accel * DT
    dv = max(-limit, min(limit, dv))      # truncate to what the body can do
    v += dv
    return x + v * DT, v                  # new position uses the new velocity

def seek(x, target, max_speed, slow_radius=0):
    return max_speed if target > x else -max_speed

def arrive(x, target, max_speed, slow_radius):
    d = target - x
    speed = max_speed * min(1.0, abs(d) / slow_radius)
    return speed if d > 0 else -speed

def run(behavior, slow_radius=0, max_speed=6.0, max_accel=12.0, target=20.0):
    x, v, furthest, settled = 0.0, 0.0, 0.0, None
    for frame in range(8 * 60):           # 8 seconds
        x, v = step(x, v, behavior(x, target, max_speed, slow_radius), max_accel)
        furthest = max(furthest, x)
        near = abs(target - x) < 0.05 and abs(v) < 0.05
        if not near:
            settled = None
        elif settled is None:
            settled = (frame + 1) * DT
    return max(0.0, furthest - target), settled

b = 6.0 ** 2 / (2 * 12.0)
print(f"braking distance b = {b} m")
print("seek        overshoot %.2f m, settled %s" % run(seek))
for r in [0.75, 1.0, 1.25, 1.5, 2.0, 3.0, 6.0]:
    over, t = run(arrive, r)
    print(f"arrive r={r:<4} predicted {max(0, b - r):.2f}  overshoot {over:.2f} m, settled {t:.2f} s")
```

Output:

```
braking distance b = 1.5 m
seek        overshoot 1.50 m, settled None
arrive r=0.75 predicted 0.75  overshoot 0.80 m, settled 4.78 s
arrive r=1.0  predicted 0.50  overshoot 0.50 m, settled 4.68 s
arrive r=1.25 predicted 0.25  overshoot 0.30 m, settled 4.63 s
arrive r=1.5  predicted 0.00  overshoot 0.00 m, settled 3.83 s
arrive r=2.0  predicted 0.00  overshoot 0.00 m, settled 4.78 s
arrive r=3.0  predicted 0.00  overshoot 0.00 m, settled 5.45 s
arrive r=6.0  predicted 0.00  overshoot 0.00 m, settled 7.35 s
```

"Settled" means the soldier is within 5 cm of the target, moving slower than 5 cm/s, and stays that way until the 8 seconds end. As a table:

| Behavior | Slowing radius `r` | Predicted overshoot `max(0, b − r)` | Simulated overshoot | Settled at |
|---|---|---|---|---|
| Seek | — | 1.50 m | 1.50 m | never |
| Arrive | 0.75 m | 0.75 m | 0.80 m | 4.78 s |
| Arrive | 1.0 m | 0.50 m | 0.50 m | 4.68 s |
| Arrive | 1.25 m | 0.25 m | 0.30 m | 4.63 s |
| Arrive | 1.5 m (= `b`) | 0 | 0.00 m | 3.83 s |
| Arrive | 2.0 m | 0 | 0.00 m | 4.78 s |
| Arrive | 3.0 m (= `2b`) | 0 | 0.00 m | 5.45 s |
| Arrive | 6.0 m | 0 | 0.00 m | 7.35 s |

Check the first rows by hand. Seek overshoots by exactly `b = 1.5` m and never settles. Below `r = b`, the overshoot tracks `b − r` to within 5 cm. The small extra comes from the 60 Hz steps, since the soldier moves 10 cm per frame at full speed and the braking decision is made once per frame.

The settle column holds the surprise. The fastest clean arrival is at `r = b`, 3.83 s for a 20 m trip that would take 3.33 s at full speed plus 0.25 s to accelerate. Every bigger radius is *slower*. Inside the ramp, speed is proportional to remaining distance, so the distance shrinks by the same fraction every moment, an exponential decay with time constant `r / max_speed`. At `r = 6` that is a full second per factor of `e`, and the soldier creeps the last half meter. Players read that creep as hesitation. This is why engines add a **stopping distance**: Unity's agent simply stops once it is that close, which cuts off the tail.

### Move it yourself

Open [the interactive](../examples/w02-seek-vs-arrive.html). The top view is the 20 m track with the soldier's trail marked every quarter second. The bottom view plots the soldier's speed against the distance left, with two reference curves: the arrive ramp (a straight line from `(r, max_speed)` down to the origin) and the maximum-braking curve `speed = √(2ad)`, which is the fastest you can be going at distance `d` and still stop in time. Drag the radius slider down past `b` and watch the soldier's trace cross above the braking curve. At that moment overshoot becomes unavoidable. Drag it up past `2b` and watch the trace lie flat on the ramp, and the settle time grow.

The two views show the same run. The track shows the symptom, a soldier stepping past his post. The phase plot shows the cause, a ramp steeper than the body's braking curve.

### Cross-game recognition

**Left 4 Dead (2008).** Reactive path following is seek aimed at a moving look-ahead point. Because the point is always ahead, the overshoot problem never appears mid-path. It only appears where the path ends. Booth's slides list the trade-off plainly. Re-pathing is cheap and motion is fluid, but local avoidance can push an actor far enough off the path that it has to re-path.

**Unity's NavMeshAgent (AI Navigation package 2.0, current documentation).** Three settings map onto this lecture's model. Acceleration is `max_accel`. Auto braking switches arrive on and off. Stopping distance cuts off the exponential tail. The documentation's advice to turn auto braking off for patrols is the seek-for-waypoints, arrive-for-destinations rule, stated as a checkbox. Any game made with Unity's navigation inherits these three knobs.

**Pac-Man (1980), Pinky.** Last week's pink ghost targets the tile four ahead of Pac-Man. That is Reynolds's **pursuit** (section 3) with a fixed look-ahead measured in tiles instead of seconds. Same idea, forty years apart. Aim where the target is going, not where it is.

### Eyes-open design judgment

- **Pick seek or arrive per goal, not per character.** Waypoints the NPC passes through want seek. Places it must stop at (a door, a conversation spot, a cover point) want arrive. Most characters need both.
- **Derive `r` from the body, then adjust.** Start at `r = b = max_speed² / (2 max_accel)`, which is the fastest clean stop. Increase it toward `2b` if the full-strength braking looks harsh for the character. A heavy ogre has a small `max_accel`, a big `b` and so a big slowing radius. It should look like it needs room to stop.
- **Don't fix overshoot by raising `max_accel`.** It works, and it makes a heavy character stop like a hummingbird. The acceleration limit is part of how the character reads.
- **Always add a stopping distance.** A proportional ramp never quite reaches zero. Choose a stop threshold small enough that the snap is invisible, a few centimeters for a human-sized NPC.
- **Match the animation.** A steering body that decelerates at 12 m/s² while the animation plays a jog produces foot sliding. Give the animators the numbers, or read `max_accel` from their stop animation.

## 3. Pursuit and evasion

Seek aims at where the target *is*. Against a moving target that means chasing its tail. **Pursuit** aims at where the target *will be* after a prediction time `T`, assuming it keeps its current velocity:

```
predicted = target_position + target_velocity × T
desired   = seek(predicted)
```

The whole design problem is choosing `T`. With `T = 0` pursuit is seek. Reynolds suggests a simple estimator, `T = D × c`, where `D` is the distance to the quarry and `c` is a tuning constant. Far away, predict far ahead. Close in, predict a little. A natural choice of `c` is `1 / max_speed`, so `T` is roughly the time the pursuer needs to cover the gap. Reynolds also warns that the prediction is recomputed every frame, so it only has to be right for one frame at a time.

```python
import math

DT = 1 / 60

def clamp_length(x, y, limit):
    n = math.hypot(x, y)
    return (x, y) if n <= limit else (x * limit / n, y * limit / n)

def chase(quarry_speed, predict, max_speed=6.0, max_accel=12.0):
    p, v = (0.0, 0.0), (0.0, 0.0)
    q, qv = (10.0, 0.0), (0.0, quarry_speed)       # quarry runs along +y
    for frame in range(1, 20 * 60):
        T = math.dist(p, q) / max_speed if predict else 0.0   # T = D * c
        aim = (q[0] + qv[0] * T, q[1] + qv[1] * T)
        dx, dy = aim[0] - p[0], aim[1] - p[1]
        n = math.hypot(dx, dy)
        want = (dx / n * max_speed, dy / n * max_speed)       # seek the aim point
        dv = clamp_length(want[0] - v[0], want[1] - v[1], max_accel * DT)
        v = clamp_length(v[0] + dv[0], v[1] + dv[1], max_speed)
        p = (p[0] + v[0] * DT, p[1] + v[1] * DT)
        q = (q[0] + qv[0] * DT, q[1] + qv[1] * DT)
        if math.dist(p, q) < 0.5:
            return frame * DT

for s in [3.0, 4.5]:
    print(f"quarry {s} m/s: seek {chase(s, False):.2f} s, pursue {chase(s, True):.2f} s")
```

Output:

```
quarry 3.0 m/s: seek 2.40 s, pursue 2.15 s
quarry 4.5 m/s: seek 4.10 s, pursue 3.05 s
```

The pursuer starts 10 m from a quarry running at right angles to the line between them. Against a slow quarry, prediction saves 10%. Against a quarry at three quarters of the pursuer's speed it saves 26%, over a second. The faster the target relative to the pursuer, the more prediction matters, because a seeker ends up running behind the target along a curve while the pursuer cuts the corner.

**Evade** is the mirror image. It flees from the predicted position. A fleeing rabbit that evades rather than flees dodges sideways out of the pursuer's path instead of running straight ahead of it.

For design, prediction is where fairness enters movement. A pursuer with perfect prediction and a speed advantage cannot be escaped by any dodge. Week 1's five tests apply. If the player is supposed to be able to shake a pursuer, cap `T`, add a reaction delay to the quarry velocity the pursuer uses (Rabin's 0.2 s), or give the pursuer a turning limit so a sharp cut beats it.

## 4. Wander, groups and blending

### Wander

Random steering each frame produces twitching. Reynolds's **wander** keeps state. Imagine a circle a little way in front of the character. A target point sits on that circle, and each frame it moves a small random step along it. The character seeks that point. Because the point moves only a little per frame, the character's turns are smooth and sustained, like an animal idly sniffing around. Two numbers tune it: the circle's radius (how sharp the turns can be) and the random step (how often the direction changes).

### Groups

GD102 week 12 introduced Reynolds's boids, three local rules that make a flock. They are steering behaviors. **Separation** steers away from nearby neighbors, weighted by closeness. **Alignment** steers toward the neighbors' average velocity. **Cohesion** seeks the neighbors' average position. Week 11 of this course builds formations on the same foundation. Left 4 Dead's hordes are a working example of path following plus separation.

### Blending, and where it fails

Real NPCs run several behaviors at once. The simplest way to combine them is a **weighted sum** of their steering requests, truncated as usual. It works most of the time, and Fray explains why it sometimes fails badly. Picture a bot with a chase behavior pointing east at a target and an avoid behavior pointing west away from an obstacle between them. Average the two and the result is close to zero. The bot stops in front of the obstacle, a textbook case of artificial stupidity. Adjusting weights only moves the point where the two cancel.

Fray, who worked on Codemasters' F1 racing games, reports that in F1 2010 the avoidance behavior grew into a large set of special cases to cope with this. For F1 2011 the team replaced steering behaviors with **context steering**. Each behavior writes into small arrays of "interest" and "danger" per heading, and one final step picks the most interesting heading that is not dangerous. He reports that the codebase shrank by 4,000 lines while the AI avoided collisions and overtook better.

His diagnosis is the design lesson. Steering behaviors are statistical. They give mostly the right direction most of the time. In a flock watched from a distance, the odd wrong move of one bird disappears in the crowd. In a racing game, where the player is wheel to wheel with each AI car, every wrong move is visible. Use steering where individuals blur into a group, and reach for something with more context where the player watches one agent closely.

## In-class activity (25 minutes)

Groups of three, one laptop with the interactive.

1. **Three bodies (10 min).** Tune arrive for three characters. A rat has `max_speed = 8` m/s and `max_accel = 40` m/s². A soldier has 6 and 12. An ogre has 4 and 3. Compute `b` and `2b` for each. Set each in the interactive, find the smallest `r` with no overshoot, and record the settle time at `r = b` and at `r = 2b`.
2. **Choose (5 min).** Pick a final `r` and a stopping distance for each character. Justify each in one sentence in terms of how the character should look.
3. **Break it (7 min).** Using the pursue mode, find a quarry speed at which pursuit and seek differ by more than 1 s. Then find a quarry maneuver (a sharp turn) that makes pursuit worse than seek for a moment. Describe why.
4. **Report (3 min).** One group presents the ogre.

Expected output: a table of `b`, `2b`, chosen `r`, stopping distance and settle times for three characters, and two sentences on the pursuit failure.

## Common misconceptions

- **"Steering sets the velocity."** Steering *requests a change* in velocity, and the body grants only what `max_accel` allows. That limit is what makes a truck curve and a cat pivot.
- **"A bigger slowing radius is always safer."** It removes overshoot only up to `r = b`. Beyond `2b` it adds nothing but a slow, hesitant creep at the end.
- **"Seek eventually settles."** Along a line it oscillates forever with amplitude `v² / (2a)`. In two dimensions it orbits. Seek has no notion of stopping.
- **"Pursuit needs to know where the player will go."** It assumes the target keeps its current velocity for `T` seconds and re-predicts every frame. It is wrong about the future constantly, and it is still better than seek.

## Check yourself

1. A wolf has `max_speed = 8` m/s and `max_accel = 16` m/s². What is its braking distance? Roughly how far will it overshoot with arrive and `r = 1.2` m? What `r` lets it follow the ramp exactly?
2. The soldier from section 2 uses arrive with `r = 6` m. Why is it slower to settle than with `r = 1.5` m, even though both arrive without overshoot?
3. A pursuer at `(0, 0)` with `max_speed = 10` m/s uses `T = D / max_speed`. The quarry is at `(20, 0)` moving at `(0, 5)` m/s. What point does the pursuer aim at this frame?
4. A bot's chase behavior requests `(4, 0)` and its avoid behavior requests `(−4, 0.5)`. With equal weights of 0.5, what is the blended request? What does the player see?
5. A designer fixes a soldier's overshoot by raising `max_accel` from 12 to 48 m/s². What happens to `b`, and what might a player notice about the soldier?

<details>
<summary>Answers</summary>

1. `b = 8² / (2 × 16) = 2` m. Overshoot about `2 − 1.2 = 0.8` m. Following the ramp exactly needs `r ≥ v² / a = 64 / 16 = 4` m.
2. Inside the ramp, speed is proportional to remaining distance, so the distance decays exponentially with time constant `r / max_speed`. At `r = 6` that is 1 s; at `r = 1.5`, 0.25 s. The big radius makes the last half meter a slow creep. A stopping distance would cut it short.
3. `D = 20`, `T = 20 / 10 = 2` s. Predicted position `(20, 0) + 2 × (0, 5) = (20, 10)`.
4. `0.5 × (4, 0) + 0.5 × (−4, 0.5) = (0, 0.25)`. The bot almost stops and drifts slowly sideways in front of the obstacle. It looks stuck, which is artificial stupidity.
5. `b` drops from 1.5 m to `36 / 96 = 0.375` m, so the overshoot mostly disappears. But the soldier now stops from full speed in about an eighth of a second, which reads as an unnatural jolt and will not match a jog-to-stop animation. Tuning `r` would have fixed it without changing the body.

</details>

## Lab / assignment hook

[Lab 02, a steering toolkit](../labs/lab02.md). Implement `step`, `seek`, `arrive`, `pursue` and `blend` for a 2D point mass so the provided tests pass, then tune arrive for three character bodies and write a short spec that another programmer could use to reproduce your tuning. Deliverable: the passing code, a tuning table and a 300-word movement spec.

## Sources

- Reynolds, C. W. (1999). "Steering Behaviors for Autonomous Characters." Game Developers Conference 1999 (HTML version, red3d.com/cwr/steer/gdc99, read September 2026). The three layers; the simple vehicle model with truncation by max force and max speed; steering as desired minus current velocity; seek and the moth comparison; flee; pursuit with `T = Dc`; arrival with a linearly ramped desired speed; wander on a circle; the `position − target` form printed in the seek formula.
- Booth, M. (2009). "The AI Systems of Left 4 Dead." Valve. Slides from the 2009 talk. Direct path following looks robotic; reactive path following toward a look-ahead point with local obstacle avoidance; its trade-offs; used for all actors in Left 4 Dead (2008). https://steamcdn-a.akamaihd.net/apps/valve/2009/ai_systems_of_l4d_mike_booth.pdf
- Unity Technologies. Scripting API, `AI.NavMeshAgent.autoBraking` (Unity 6.6 documentation, read September 2026): braking to avoid overshooting or endless orbiting. AI Navigation package 2.0 manual, "NavMesh Agent" component reference: acceleration, stopping distance, and the advice to disable auto braking for a guard on patrol.
- Fray, A. (2015). "Context Steering: Behavior-Driven Steering at the Macro Scale." In S. Rabin (ed.), *Game AI Pro 2*, chapter 18. CRC Press. Free at gameaipro.com. The chase and avoid stalemate; the growth of avoidance code in F1 2010; context steering in F1 2011 and the 4,000-line reduction; steering as a statistical method suited to flocks.
- Pittman, J. (2009). "The Pac-Man Dossier." Game Developer. Pinky's four-tiles-ahead target, as used in week 1.
- Millington, I. (2019). *AI for Games*, 3rd ed. CRC Press. Chapter 3, kinematic and steering behaviors.
- The soldier, wolf, rat and ogre numbers are invented for teaching.

## Interactive spec: examples/w02-seek-vs-arrive.html

**The one insight:** seek overshoots by exactly the braking distance `b = v² / (2a)`, and arrive stops cleanly once its slowing radius reaches `b`; beyond `2b` it only gets slower. The student should see the speed trace cross the maximum-braking curve at the same moment the soldier steps past the flag.

**Layout.** Two linked views stacked vertically at all widths (track on top), plus a readout panel beside them at 1280 px and below them at 390 px. A mode switch at the top: "Arrive" (default) and "Pursue".

- **Arrive mode, top view "Track":** a horizontal 1D track from −2 m to 24 m with the target flag at 20 m. The agent is a filled circle. Its trail is marked with small ticks every 0.25 s of simulated time. The slowing radius is a shaded band from `20 − r` to 20, and the braking distance `b` is a second, hatched band from `20 − b` to 20, both labelled. Overshoot beyond 20 is highlighted in the warning color with its length printed.
- **Arrive mode, bottom view "Speed vs distance left":** x axis is distance left `d = 20 − x` from 22 m down to −2 m (left to right, so motion reads left to right like the track); y axis is speed from 0 to `max_speed + 1`. Draw the ramp `max_speed × min(1, |d| / r)` (solid), the maximum-braking curve `√(2 a |d|)` (dashed), and the agent's trace as points (one per frame). Where the trace goes more than 0.15 m/s above the braking curve (with `d > 0` and the agent moving toward the target), color those points in the warning color. The 0.15 m/s tolerance absorbs the 60 Hz frame-step effect near `d = 0`.
- **Pursue mode:** a single 2D view, 24 m × 24 m, pursuer starting at `(0, 0)` at rest and quarry starting at `(10, 0)` moving at `(0, s)`. Draw both traces, and for the pursue run the current aim point as a small cross joined to the quarry by a thin line. Run seek and pursue together as two pursuers of different colors, labelled "seek" and "pursue".

**Controls (keyboard accessible, labelled, values printed):**

1. `max_speed` slider, 2 to 12 m/s, step 0.5, default 6.
2. `max_accel` slider, 2 to 40 m/s², step 1, default 12.
3. Slowing radius `r` slider, 0 to 10 m, step 0.05, default 1.5. At 0 the behavior is seek (label "seek").
4. Play/Pause, Restart, and a speed select (0.25×, 1×, 4×). Any slider change restarts the run and redraws both views immediately; the final trace is also precomputed so the plot is complete even when paused.
5. Pursue mode: quarry speed `s` slider, 0 to 5.5 m/s, step 0.5, default 4.5. Uses `max_speed` and `max_accel` from sliders 1 and 2.

**Readouts:** `b = v²/(2a)`, `2b`, predicted overshoot `max(0, b − r)`, simulated overshoot (max x − 20, floored at 0), settle time (the time after which `|d| < 0.05` and `|v| < 0.05` hold until the end of 8 s, or "never"). Pursue mode: catch time for seek and for pursue (distance under 0.5 m), or "no catch in 20 s".

**Algorithm (must match the lecture code).** `dt = 1/60`, 8 s (arrive) or 20 s (pursue). Each frame: compute desired velocity; `dv = desired − v` truncated to length `max_accel × dt`; `v = truncate(v + dv, max_speed)`; `x = x + v × dt`. Seek desired speed `max_speed` toward the target; arrive desired speed `max_speed × min(1, |d| / r)` toward the target. Pursue aims at `q + qv × T` with `T = |p − q| / max_speed`; seek aims at `q`. Use the exact loop and stopping rules from the lecture's two code blocks.

**Test values (must match to the printed precision).**

- Defaults (6, 12): `b = 1.5`, `2b = 3`. Seek (`r = 0`): overshoot 1.50 m, settle "never".
- Arrive `r` = 0.75, 1.0, 1.25, 1.5, 2.0, 3.0, 6.0: overshoot 0.80, 0.50, 0.30, 0.00, 0.00, 0.00, 0.00 m; settle 4.78, 4.68, 4.63, 3.83, 4.78, 5.45, 7.35 s.
- Pursue, `s = 3.0`: seek 2.40 s, pursue 2.15 s. `s = 4.5`: seek 4.10 s, pursue 3.05 s.
- Largest excess of speed over the braking curve `√(2a·d)` while `d > 0`: at `r = 1.0` about 3.11 m/s (18 frames more than 0.01 m/s above it, 17 of them more than 0.15 m/s and so warning-colored); at `r = 1.5` about 0.12 m/s (a frame-step effect, no warning points); at `r = 2.0` and `r = 3.0` zero.

**First screen.** Arrive mode with `r = 1.0`, run already complete, so the overshoot of 0.50 m and the red points above the braking curve are visible at once. Caption: "Slowing radius smaller than the braking distance: the soldier cannot stop in time. Drag r up to 1.5."

**Accessibility.** Tab order follows the control list, visible focus, sliders operable with arrow keys. A live region reports overshoot and settle time after each change. Respects `prefers-reduced-motion` (show the finished run without animation) and `prefers-color-scheme`. Palette from `templates/interactive-tokens.css`; the warning color is never the only cue (overshoot points are also drawn hollow). No game art.

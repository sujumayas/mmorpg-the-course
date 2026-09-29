# CS201 · Week 11 — Physics Integration Basics

**Why this matters:** You will almost never write a rigid-body solver. You will integrate one, such as Box2D, Jolt, PhysX or Godot's built-in engine, into a game whose entities, scripts and renderer also want to own positions. Most physics bugs in shipped games are integration bugs. Crates teleport, triggers fire twice, a destroyed enemy crashes the step, a pile of rubble eats the frame. This week is about the seam between your engine and the physics library.

**You will be able to:**
- Compute when a body and an island fall asleep from the sleep rule (speed threshold and still-time), and the awake cost that follows.
- Design the per-frame order of writes and reads between entities and a physics world so each transform property has exactly one owner at each point in the frame.
- Implement buffered contact events that make it safe to destroy bodies in response to collisions.
- Critique a physics setup (sleep thresholds, pile sizes, static versus kinematic bodies) for its CPU cost and its wake-up spikes.

**Before class:** Gregory, *Game Engine Architecture* (3rd ed., 2018), chapter 13 "Collision and Rigid Body Dynamics," the sections on integrating a physics engine into your game. Box2D v3.1 documentation, "Simulation," the sections on the world step, sleep, body events and contact events (about 20 minutes).

**Prerequisites from earlier courses:** [CS101 week 9, delta time and the fixed-timestep accumulator](../../CS101-programming-for-games-i/lectures/w09-delta-time-and-frame-rate-independence.md) (why physics steps at a fixed rate, semi-implicit Euler, and render interpolation with `alpha`). [CS101 week 10, collision basics](../../CS101-programming-for-games-i/lectures/w10-collision-basics-aabb-and-circles.md) (AABB tests, tunneling, broad versus narrow phase). [CS102 week 4, big-O intuition](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w04-big-o-intuition-for-game-developers.md) (the grid broad phase). [CS102 week 10, observer and events](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w10-observer-and-events.md) (the modify-while-iterating bug, and queued events). [CS201 week 4, the frame](w04-the-frame-update-render-present.md) (where physics sits in the update stage). The vector and force material is in MA201, which runs alongside this course: [week 7, numerical integration](../../MA201-linear-algebra-and-physics-for-games/lectures/w07-numerical-integration-euler-semi-implicit-verlet.md), [week 8, forces and mass](../../MA201-linear-algebra-and-physics-for-games/lectures/w08-forces-mass-and-drag.md) and [week 10, collision response and impulses](../../MA201-linear-algebra-and-physics-for-games/lectures/w10-collision-response-and-impulses.md). None of it is re-taught here.

**Interactive:** [`examples/w11-sleeping-islands.html`](../examples/w11-sleeping-islands.html). Keep it open during section 2.

---

## 1. The physics world is a second world

When you add a physics library, you add a second copy of your scene. Your engine has entities with transforms. The physics library has its own **world** that holds **bodies** (things with mass and velocity) and **shapes** attached to them (the boxes, circles and capsules that collide). The library does not know what a goblin is. It knows body 4,112 has a capsule and a velocity.

Bodies come in three kinds, and the kind decides who owns the position.

- A **static** body never moves. Walls and terrain. The physics world treats it as infinitely heavy and does not integrate it.
- A **kinematic** body moves only because your code says so, by setting its velocity or a target position. Forces and collisions do not push it. Moving platforms, doors, and often player characters.
- A **dynamic** body is moved by the solver. Gravity, forces, impulses and contacts change its velocity, and the step integrates its position. Crates, ragdolls, debris.

One call to the world's `step(dt)` runs a fixed pipeline. Library details differ, but the order is close to this:

1. **Broad phase.** Find pairs of shapes whose bounding boxes overlap, with a tree or grid (CS101 week 10, CS102 week 4).
2. **Narrow phase.** For each pair, compute exact contact points and penetration depth.
3. **Island building.** Group bodies connected by contacts or joints into **islands**, sets of bodies that affect each other.
4. **Solve.** For each awake island, compute the impulses that stop penetration and satisfy joints, then integrate velocities and positions with a fixed `dt` (CS101 week 9).
5. **Sleep and events.** Put settled islands to sleep, then record which contacts began and ended and which bodies moved.

Steps 3 and 5 are this week's worked example. They decide how much a scene costs after the action is over.

## 2. Worked example: the rubble pile that stops costing

### The hook

Blow up a wall in a physics-heavy game and a thousand chunks fly. A second later the frame rate is back to normal, although every chunk still exists and still has a body. The physics engine stopped simulating them. Box2D's documentation says that when a body or group of bodies comes to rest, it enters a sleep state with very little CPU overhead.

Box2D v2.4 put a body to sleep once it had been below 0.01 m/s (and 2 degrees per second of rotation) for 0.5 s. Box2D v3.1 uses a default speed threshold of 0.05 m/s and the same 0.5 s. Godot 4's built-in engine defaults to 0.5 s as well. Yet anyone who has built a tall stack of crates has seen it stay awake for a long time, burning CPU, because one crate near the top kept trembling. One crate's jitter kept all of them awake. Why should one body's speed decide the fate of the whole stack?

### The model

Each body keeps a **still-timer** `s`. Every step:

```
if speed < v_sleep:   s = s + dt
else:                 s = 0
island sleeps when    min(s over all bodies in the island) >= t_sleep
```

- `v_sleep` is the speed threshold (0.05 m/s in Box2D v3.1).
- `t_sleep` is how long a body must stay below it (0.5 s in Box2D and Godot).
- An **island** is a set of bodies connected through contacts or joints. Static bodies do not join islands, so two crates resting on the same floor but not touching each other are separate islands.

The island rule is the whole point. Bodies in an island push on each other through contacts. If the solver froze the bottom crate while the top crate was still sliding, the frozen crate could not respond to the pushes, and the stack would pass through itself or explode when it woke. So an island sleeps as a unit, which means **the island falls asleep at the moment its slowest-to-settle body does.**

The step cost for the physics world is roughly proportional to the awake bodies and contacts:

```
C_step ≈ a × (awake bodies) + b × (awake contacts)
```

Sleeping bodies cost almost nothing beyond their slot in the broad phase.

For a body whose speed decays smoothly as `v(t) = v0 × e^(−k t)`, the time it takes to go still is `ln(v0 / v_sleep) / k`. Its sleep time is that plus `t_sleep`.

### Numbers you can check

Take a stack of five crates after a hit, with starting speeds 4, 2, 1, 0.5 and 0.25 m/s, decaying at `k = 2` per second. Use Box2D v3.1's defaults, `v_sleep = 0.05` m/s and `t_sleep = 0.5` s, and a 60 Hz step. The code below simulates the still-timers tick by tick. It also tries one crate that never settles below 0.06 m/s, and then scales up to 200 stacks.

```python
import math

HZ = 60                                    # physics ticks per second

def speed(v0, floor, k, tick):
    """A settling body: speed decays from v0 at rate k, but never below its jitter floor."""
    return max(v0 * math.exp(-k * tick / HZ), floor)

def sleep_ticks(island, v_sleep=0.05, t_sleep=0.5, k=2.0, max_s=10):
    """Return (tick each body could sleep on its own, tick the whole island sleeps or None)."""
    need = round(t_sleep * HZ)             # ticks a body must stay below v_sleep
    timers = [0] * len(island)
    alone = [None] * len(island)
    for tick in range(1, max_s * HZ + 1):
        for i, (v0, floor) in enumerate(island):
            slow = speed(v0, floor, k, tick) < v_sleep
            timers[i] = timers[i] + 1 if slow else 0
            if timers[i] >= need and alone[i] is None:
                alone[i] = tick
        if min(timers) >= need:            # the island sleeps only when every body is ready
            return alone, tick
    return alone, None

stack = [(4.0, 0), (2.0, 0), (1.0, 0), (0.5, 0), (0.25, 0)]   # (v0 in m/s, jitter floor)
alone, together = sleep_ticks(stack)
print("each body alone (s):", [round(t / HZ, 3) for t in alone])
print("island sleeps at (s):", round(together / HZ, 3))
print("awake body-seconds, per body:", round(sum(alone) / HZ, 2))
print("awake body-seconds, island:  ", round(len(stack) * together / HZ, 2))

jittery = [(4.0, 0), (2.0, 0), (1.0, 0.06), (0.5, 0), (0.25, 0)]
print("one crate jitters at 0.06 m/s, v_sleep 0.05:", sleep_ticks(jittery)[1])
print("same crate, v_sleep 0.10 (s):", round(sleep_ticks(jittery, v_sleep=0.10)[1] / HZ, 3))

for t in (1.0, 2.0, 2.5, 3.0, 10.0):       # 200 such stacks = 1,000 crates; 20 stacks jitter
    tick = round(t * HZ)
    per_body = 200 * sum(1 for a in alone if a > tick)
    island = 1000 if together > tick else 0
    with_jitter = (180 * 5 if together > tick else 0) + 20 * 5
    print(f"t = {t:4.1f} s   awake: per body {per_body:4d}   island {island:4d}   island + 20 jittery {with_jitter:4d}")
```

```
each body alone (s): [2.683, 2.333, 1.983, 1.65, 1.3]
island sleeps at (s): 2.683
awake body-seconds, per body: 9.95
awake body-seconds, island:   13.42
one crate jitters at 0.06 m/s, v_sleep 0.05: None
same crate, v_sleep 0.10 (s): 2.333
t =  1.0 s   awake: per body 1000   island 1000   island + 20 jittery 1000
t =  2.0 s   awake: per body  400   island 1000   island + 20 jittery 1000
t =  2.5 s   awake: per body  200   island 1000   island + 20 jittery 1000
t =  3.0 s   awake: per body    0   island    0   island + 20 jittery  100
t = 10.0 s   awake: per body    0   island    0   island + 20 jittery  100
```

| Crate | `v0` (m/s) | Goes still at `ln(v0/0.05)/2` | Could sleep alone at | Sleeps in the island at |
|---|---|---|---|---|
| top | 4.0 | 2.19 s | 2.68 s | 2.68 s |
| 2 | 2.0 | 1.84 s | 2.33 s | 2.68 s |
| 3 | 1.0 | 1.50 s | 1.98 s | 2.68 s |
| 4 | 0.5 | 1.15 s | 1.65 s | 2.68 s |
| bottom | 0.25 | 0.80 s | 1.30 s | 2.68 s |

Check the top crate by hand. `ln(4 / 0.05) = ln 80 = 4.38`, divided by 2 is 2.19 s, plus 0.5 s gives 2.69 s. The tick loop reports 2.683 s because it counts in whole 1/60 s steps. The island costs 13.42 awake body-seconds against 9.95 if each crate could sleep on its own, 35% more. That is the price of correct stacking.

Now the jittery crate. Its speed never drops below 0.06 m/s, just above the 0.05 threshold, so its timer keeps resetting. The island **never** sleeps, and neither do the four calm crates on it. Scale that to the 1,000-crate scene. Twenty jittery stacks out of 200 keep 100 bodies awake forever, which is 10% of the pile's peak cost paid every frame for the rest of the level. Raise `v_sleep` to 0.10 m/s (Godot 4's 3D default) and the same stack sleeps at 2.33 s.

The insight: **a pile's idle cost is set by its worst member, not its average.** One trembling body holds its whole island awake.

### A visual you can move

Open `examples/w11-sleeping-islands.html`. The left view is a side-on scene of 20 stacks of five crates. Awake crates are drawn in the accent color, sleeping ones gray, and each crate has a thin bar showing its still-timer filling toward `t_sleep`. The right view plots awake bodies against time, with a line for per-body sleeping and a line for island sleeping.

Press "knock over" and watch the stacks go gray one whole stack at a time, never crate by crate. Then drag the "jittery crates" slider from 0 to 5. Each jittery crate turns its entire stack into a permanent block of color, and the island line on the right flattens above zero. Drag `v_sleep` above the jitter floor and those stacks go gray. Last, click any sleeping stack to bump it. The whole stack wakes at once, and a spike appears on the chart.

### Cross-game recognition

**Box2D (v2.4 and v3.1).** v2.4 hard-coded `b2_timeToSleep = 0.5` s, a linear tolerance of 0.01 m/s and an angular tolerance of 2 degrees per second. v3.1 moved the speed threshold into each body's definition (`sleepThreshold`, default 0.05 m/s) and keeps a 0.5 s time to sleep. The v3 source organizes bodies into islands and solver sets, and its documentation says a sleeping body wakes when an awake body collides with it, or when a joint or contact attached to it is destroyed. Our model, with the constants filled in.

**Godot 4.3.** The project settings `physics/2d/time_before_sleep` and `physics/3d/time_before_sleep` default to 0.5 s. The speed thresholds are `physics/2d/sleep_threshold_linear` at 2.0 (2D units are pixels, so 2 px/s) and `physics/3d/sleep_threshold_linear` at 0.1 m/s. Same rule, different units, and the same `t_sleep`.

**Unity 6 (PhysX).** Unity's per-body `Rigidbody.sleepThreshold` is a mass-normalized energy rather than a speed, but the manual describes the same behavior. A body sleeps below the threshold, and a collision or force wakes it. The manual also warns that a sleeping Rigidbody may fail to wake when a static collider is moved through its Transform instead of through physics. That is the ownership bug of section 3, and it shows that sleep and sync interact.

Three engines, three sets of units, one timer-and-island rule. When you open a new engine's physics settings, look for the threshold and the time. Then ask what counts as an island.

### Eyes-open design judgment

- **Tune `v_sleep` against your worst jitter, not your average motion.** Too low and stacks never settle. Too high and a slowly rolling ball stops dead in mid-roll, which players see. Measure the jitter floor of your tallest stack, then set the threshold just above it.
- **Keep islands small.** A 500-crate pile is one island if every crate touches a neighbor. It sleeps late, and one bump wakes all 500 in a single step, a spike you can see in the frame graph. Split set dressing into separate piles, or make background props static.
- **Static and kinematic are cheaper than asleep.** A crate that will never move in gameplay should not be dynamic at all.
- **Waking is a gameplay event.** A player walking into a sleeping pile wakes it. A player's explosion three rooms away does not, unless your code says so. Decide which game actions call a wake-up, and remember that a force applied to a sleeping body may be ignored (Box2D v3.1 documents this for forces applied without waking).
- **Disabling sleep is a valid choice.** Box2D's own documentation suggests turning sleep off if your game does not need it, since tracking sleep has a cost. A small arena game where everything moves all the time may be faster without it.

### Check yourself (worked example)

1. A crate starts at 3 m/s and decays with `k = 3` per second. With `v_sleep = 0.05` m/s and `t_sleep = 0.5` s, when can it sleep on its own?
2. An island has crates that could sleep alone at 1.2, 1.9 and 2.4 s. How many awake body-seconds does it cost, and how many would per-body sleeping cost?
3. A crate jitters at 0.03 m/s. Does it block sleep in Box2D v3.1 with default settings? In Box2D v2.4?

<details>
<summary>Answers</summary>

1. `ln(3 / 0.05) / 3 = ln 60 / 3 = 4.09 / 3 = 1.36` s to go still, plus 0.5 s, so about 1.86 s.
2. Island: `3 × 2.4 = 7.2` body-seconds. Per body: `1.2 + 1.9 + 2.4 = 5.5`.
3. v3.1 threshold is 0.05 m/s, and 0.03 is below it, so it does not block. v2.4's linear tolerance is 0.01 m/s, so 0.03 is above it, and the island never sleeps.

</details>

## 3. Who owns the transform

Your entity has a position. Its body has a position. The renderer wants a position. If more than one of them writes it in the same frame, you get the classic integration bugs. Objects snap back after you move them. Physics fights your animation. A trigger fires when nothing touched it.

The fix is a rule. **At every point in the frame, each transform property has exactly one owner, and ownership is decided by body type.**

| Body type | Who writes the position | How the game changes it | Who reads it |
|---|---|---|---|
| static | the game, at load time | rarely, and as a teleport | physics |
| kinematic | the game, before the step | set velocity or target position | physics reads it for collisions, entity keeps it |
| dynamic | physics, during the step | forces, impulses, and explicit teleports only | the game copies it to the entity after the step |

Then fix the order of a frame so the handoffs happen in one place:

1. **Gameplay writes commands.** Forces, impulses, kinematic targets, and requested teleports. Nothing touches dynamic positions directly.
2. **Physics steps** zero or more times at a fixed `dt`, driven by the accumulator from CS101 week 9.
3. **Drain events.** Contacts that began or ended, sensors entered, bodies that moved or fell asleep (section 4).
4. **Copy out.** For each dynamic body that moved, write its transform into its entity.
5. **Render** with interpolation between the last two physics states, using `alpha` from CS101 week 9.

Step 4 is where sleep pays twice. If only moved bodies are copied, sleeping bodies cost nothing in the sync either. Box2D v3.1 provides exactly this. After each step, `b2World_GetBodyEvents()` returns a contiguous array of move events, one for each body that moved, each with a flag saying whether it just fell asleep. The documentation recommends it over reading every body's transform, because most bodies may not have moved and iterating over all of them causes cache misses. You will see why contiguous arrays matter in week 6.

The teleport is the one case where the game writes a dynamic body's position. Make it an explicit command that also wakes the island. Unity's manual warns that a static collider moved through its Transform, rather than through physics, may not wake sleeping Rigidbodies near it. The body keeps sleeping in mid-air where the floor used to be. In the ownership table, that is the game writing a property that physics owns, outside the one sanctioned path.

## 4. Contact events: buffer, then act

Game logic wants to react to collisions. A bullet hits an enemy, the enemy takes damage and maybe dies, and its body should disappear. The tempting code destroys the body inside the collision callback. Box2D v2.4's documentation forbids it. The world cannot be altered inside a callback, because you might destroy objects the solver is still processing and leave it holding orphaned pointers. Its recommended practice is to buffer the contact data and process it after the step. Box2D v3.1 goes further. Contact begin and end events arrive as arrays you read after `b2World_Step()` returns, and its documentation says to process them before other game logic.

This is CS102 week 10's modify-while-iterating bug, one level down. The list being modified is inside the physics library, where you cannot see it. Here is the buffered version.

```python
class PhysicsWorld:
    def __init__(self):
        self.bodies = {}            # body id -> health of the crate it belongs to
        self.locked = False         # True while step() is running
        self.contact_events = []    # filled during the step, read after it

    def destroy(self, body_id):
        if self.locked:
            raise RuntimeError("cannot change the world during a step")
        del self.bodies[body_id]

    def step(self, touching_pairs):
        self.locked = True
        self.contact_events.clear()
        for a, b in touching_pairs:           # the solver's inner loop
            self.contact_events.append((a, b))
        self.locked = False

world = PhysicsWorld()
world.bodies = {1: 30, 2: 10, 3: 10}
world.step([(1, 2), (2, 3), (1, 3)])

to_destroy = set()                             # buffer: a body may appear in many events
for a, b in world.contact_events:
    for body in (a, b):
        world.bodies[body] -= 10
        if world.bodies[body] <= 0:
            to_destroy.add(body)
for body in sorted(to_destroy):
    world.destroy(body)                        # safe: the step is over
print("events:", world.contact_events)
print("survivors:", world.bodies)
```

```
events: [(1, 2), (2, 3), (1, 3)]
survivors: {1: 10}
```

Two details matter. First, the `locked` flag turns a silent corruption into a loud error. Real libraries do something similar. In Box2D v3.1, `b2DestroyBody` on a locked world trips an assertion in debug builds and silently does nothing in release builds. Second, destruction is buffered even *after* the step. Body 2 appears in two events. If the first event destroyed it immediately, the second event would look up a body that no longer exists. Box2D v2.4's own example for this (its "CollisionProcessing" test) buffers the bodies to destroy, sorts the buffer and skips duplicates for the same reason.

Events also give you the right shape for gameplay. "Contact began" and "contact ended" are edges, fired once. If your trigger zone reacts to "is touching" every step instead, your door plays its opening sound 60 times a second.

## 5. What to hand the physics world, and what not to

A last integration decision is what goes into the physics world at all. Every body costs broad-phase work, memory and sync. A good default:

- **Collision-only scenery** is static bodies with simple shapes. A detailed mesh is for rendering. The physics shape is a handful of boxes.
- **The player character** is usually kinematic, or a dynamic capsule with rotation locked. Designers want exact, snappy control that a real force simulation does not give. Godot's `CharacterBody2D`, which you used in CS101 week 9, is a body moved only by script, with a `move_and_slide` helper that slides along walls.
- **Pure visuals** (sparks, leaves, shell casings) often skip the physics world and use a cheap particle integrator that never collides with anything that matters.
- **Queries** such as raycasts and overlap tests do not need bodies. Line of sight for AI, ground checks and bullet hits are queries against the world's broad phase.

Every item on this list is a way to keep `awake bodies` in the section 2 cost formula small before sleep has to do it for you.

## In-class activity (25 minutes)

In pairs, plan the physics for a dungeon room in an action RPG. It has a collapsing bridge of 40 planks, 120 barrels and crates for the player to smash, 6 enemies and the player, and a portcullis that drops when a lever is pulled.

1. Assign each object a body type (static, kinematic, dynamic, or not in the physics world). Justify each in one line.
2. Group the dynamic bodies into likely islands at rest. Which island is the largest? Estimate its sleep time if its worst member settles like the top crate in section 2.
3. Write the frame order for this room, and mark where the lever, the portcullis and "barrel destroyed" happen.
4. Swap with another pair and find one place where two systems write the same transform in the same frame.

Expected output: a table of objects with body types, an island sketch with your largest island circled, and a five-line frame order.

## Common misconceptions

- **"A sleeping body is gone from the simulation."** It still collides. An awake body that touches it wakes it and its whole island. Sleep removes solving and integrating, not existence.
- **"Each body sleeps when it stops moving."** Each island does. One body still moving keeps every body connected to it awake.
- **"Setting the position of a dynamic body is how you move it."** It is a teleport. It skips collision in between, can wake nothing, and fights the solver. Use forces, impulses or velocity, and keep teleports explicit.
- **"Destroying a body in the collision callback is fine if it works in testing."** It works until two contacts involve the same body in one step. Buffer, then act.

## Check yourself

1. Your 60 Hz physics world has 800 dynamic bodies. Profiling shows `a = 4 µs` per awake body and `b = 1.5 µs` per awake contact, with about 1.5 contacts per awake body. What is the step cost with everything awake? If 90% of bodies are asleep, what is it? What share of a 16.7 ms frame is that at one step per frame?
2. A designer builds a decorative tower of 300 crates, all touching. The player's arrow grazes the top crate. Using the model, describe the frame cost before, during and after, and propose two fixes.
3. In the frame order of section 3, a script sets a dynamic crate's position directly in step 1 instead of issuing a teleport command. List two things that can go wrong.
4. A body's speed decays as `v0 × e^(−2t)`. What starting speed makes it take exactly 2.0 s to become able to sleep in Box2D v3.1 defaults?

<details>
<summary>Answers</summary>

1. All awake: `800 × 4 + 1,200 × 1.5 = 3,200 + 1,800 = 5,000 µs = 5.0 ms`, 30% of a 16.7 ms frame. With 80 awake and 120 contacts: `320 + 180 = 500 µs = 0.5 ms`, 3%.
2. Before: asleep, near zero cost. The graze wakes the whole island, so all 300 crates plus their contacts are solved from that step on (with question 1's numbers, `300 × 4 + 450 × 1.5 = 1,875 µs`, a jump of almost 1.9 ms in one frame). The island sleeps again only after its slowest crate settles and 0.5 s passes. Fixes: make most of the tower static and only the top layers dynamic, or split the tower into several separate islands, or convert crates to dynamic only when actually hit.
3. The solver can overwrite it in the step, so the crate snaps back. Or it lands overlapping another body and gets a huge separation impulse. Also its island may stay asleep, so it hangs in the air.
4. Still-time must be 1.5 s: `ln(v0 / 0.05) / 2 = 1.5`, so `v0 = 0.05 × e^3 ≈ 1.00` m/s.

</details>

## Lab / assignment hook

[Lab 11, islands, sleep and a safe event queue](../labs/lab11.md). You write the engine side of physics integration in Python: union-find islands from contact pairs, still-timers with island sleep, wake-on-touch, and a buffered event queue that makes destroying bodies safe. Then you measure awake-body counts for three pile layouts and recommend sleep settings.

## Sources

- Box2D v2.4.1, `include/box2d/b2_common.h`. `b2_timeToSleep` 0.5 s, `b2_linearSleepTolerance` 0.01 m/s, `b2_angularSleepTolerance` 2 degrees per second. https://github.com/erincatto/box2d/tree/v2.4.1
- Box2D v2.4.1 documentation, `docs/dynamics.md`, contact listener section. Altering the world inside callbacks is not allowed; buffer contact data and process it after the step; the CollisionProcessing example sorts its destroy buffer and skips duplicates.
- Box2D v3.1.0, `src/world.c`, `b2GetWorldLocked` (asserts and returns NULL when the world is locked), used by `b2DestroyBody` in `src/body.c`.
- Box2D v3.1.0, `include/box2d/types.h` (`sleepThreshold` default 0.05 m/s, `b2BodyMoveEvent` with `fellAsleep`), `src/constants.h` (`B2_TIME_TO_SLEEP` 0.5 s), `src/island.c`, and `docs/simulation.md` (sleep, waking rules, body events, contact events after the step, disabling sleep). https://github.com/erincatto/box2d/tree/v3.1.0
- Godot Engine 4.3, `doc/classes/ProjectSettings.xml`. `physics/2d/sleep_threshold_linear` 2.0, `physics/3d/sleep_threshold_linear` 0.1, `physics/2d/time_before_sleep` and `physics/3d/time_before_sleep` 0.5 s. https://github.com/godotengine/godot/blob/4.3-stable/doc/classes/ProjectSettings.xml
- Unity 6.6 Scripting Reference, `Rigidbody.sleepThreshold` (mass-normalized energy threshold). Unity 6.6 Manual, "Rigidbody physics" overview (sleep, wake on collision or force, moved static colliders may not wake sleeping bodies). https://docs.unity3d.com/Manual/RigidbodiesOverview.html
- Gregory, J. (2018). *Game Engine Architecture*, 3rd ed. CRC Press. Chapter 13.

## Interactive spec: examples/w11-sleeping-islands.html

**The one insight:** an island sleeps only when its slowest body is ready, so one jittering body keeps its whole stack awake, and one bump wakes the whole stack at once.

**Layout.** Two linked views, stacked on mobile, side by side at 1,280 px.

- **Left view, "the room".** Side-on drawing of 20 stacks of 5 crates on a floor, in 4 rows of 5 stacks (generic squares, no art). Awake crates in the accent color, sleeping crates in a muted gray. Each crate has a thin horizontal bar underneath showing its still-timer `s / t_sleep` (full = ready). Crates do not need to move physically; a small random offset proportional to current speed (capped at 3 px, and zero under `prefers-reduced-motion`) suggests motion.
- **Right view, "the cost".** Line chart of awake bodies (0 to 100) against time (0 to 10 s). Two lines, "per body" (dashed) and "island" (solid), plus a horizontal readout of the current values. A vertical cursor shows the current time.

**Model (per stack, identical to the lecture).** 60 Hz ticks. Crate `j` of 5 (top to bottom) has `v0 = [4, 2, 1, 0.5, 0.25]` m/s and speed `max(v0 × exp(−k × t_since_knock), floor)`. Jittery crates have `floor = jitter` (default 0.06 m/s); others have `floor = 0`. Timers: `s = s + 1/60` if speed `< v_sleep`, else `s = 0`. A stack (island) sleeps when all 5 timers `≥ t_sleep`; once asleep, its crates stop updating and draw gray. "Per body" line counts crates whose own timer has not yet reached `t_sleep`.

**Controls.**
- "Knock over" button: resets all timers and sets `t_since_knock = 0` for every stack.
- `v_sleep` slider: 0.01 to 0.20 m/s, step 0.01, default 0.05.
- `t_sleep` slider: 0.1 to 2.0 s, step 0.1, default 0.5.
- Decay `k` slider: 0.5 to 5 per second, step 0.5, default 2.
- "Jittery crates" slider: 0 to 5, default 0. Each unit makes the middle crate of one more stack (stacks 1, 5, 9, 13, 17) jittery.
- Jitter floor slider: 0.01 to 0.2 m/s, default 0.06.
- Clicking or pressing Enter on a sleeping stack "bumps" it: resets that stack's `t_since_knock = 0` and timers, so it wakes as a whole and the chart spikes by 5.
- Play/pause and a speed selector (0.25×, 1×, 4×). Default 1×.

**Readouts.** Current time, awake bodies (island rule), awake bodies (per-body rule), island sleep time for a normal stack, awake body-seconds so far for both rules.

**Test values (defaults, no jitter).** Per-crate sleep times alone: 2.683, 2.333, 1.983, 1.650, 1.300 s. Island sleep time: 2.683 s. Awake counts for all 20 stacks: at 2.0 s, per body 40 and island 100; at 2.5 s, per body 20 and island 100; at 3.0 s, 0 and 0. With 2 jittery crates (floor 0.06, `v_sleep` 0.05): island count stays at 10 forever. With 2 jittery crates and `v_sleep = 0.10`: island sleep time 2.333 s, count 0 after that. Awake body-seconds per stack by 10 s: per body 9.95, island 13.42.

**First screen.** The scene 1.5 s after a knock, paused, with 1 jittery crate, so the viewer sees colored stacks, partly filled timer bars and a chart with both lines already diverging. Keyboard: all controls reachable with Tab; stacks focusable in reading order. Respect `prefers-color-scheme`.

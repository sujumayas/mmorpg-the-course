# MA201 · Week 08 — Forces, Mass and Drag

**Why this matters:** Every falling player, sliding crate and coasting car in your game stops accelerating at some speed, and the rule that decides that speed is usually one multiplication per tick that nobody wrote down. Get it wrong and your game feels floaty on one machine and brick-heavy on another, ice feels like carpet, or a crate flips direction when the frame rate drops. This week you learn to read that multiplication as physics, compute the speed limit it creates, and move it between tick rates without changing the feel.

**You will be able to:**
- Build a force accumulator that sums gravity, applied forces and drag into one acceleration per step, and explain why gravity is added as an acceleration while other forces are divided by mass.
- Compute the terminal velocity and the time to reach 90% of it for a per-tick drag rule, and check your answer against a shipped game's documented numbers.
- Convert a per-tick drag factor to a drag coefficient in 1/s and back, and use it to keep the same feel at 20, 60 and 144 Hz.
- Compare linear drag, quadratic drag and a hard speed cap, and choose between them for a stated design goal.

**Before class:** Millington, *Game Physics Engine Development* (2nd ed., 2010), chapter 3 (the damping term in the particle integrator) and chapter 5, "Adding General Forces", up to the force generators for drag. NASA Glenn Research Center, *Beginner's Guide to Aeronautics*, the pages "The Drag Equation" and "Terminal Velocity" (10 minutes together).

**Prerequisites from earlier courses:** [MA201 week 7, numerical integration](w07-numerical-integration-euler-semi-implicit-verlet.md) (semi-implicit Euler and the stability limit `ω·dt < 2`, which reappears here). [CS101 week 9, delta time](../../CS101-programming-for-games-i/lectures/w09-delta-time-and-frame-rate-independence.md), the misconception about multiplicative decay (`k ** (dt × 60)`), which section 4 explains. [MA101 week 4, exponentials](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md) (repeated multiplication, `e`, and `ln`). [CS203 week 2, steering behaviors](../../CS203-artificial-intelligence-for-games/lectures/w02-steering-behaviors.md), where `max_accel` folds mass into acceleration. This week unfolds it.

**Interactive:** [`examples/w08-terminal-velocity.html`](../examples/w08-terminal-velocity.html). Keep it open during section 2.

---

## 1. Forces add, mass divides

Newton's second law says that the acceleration of a body is the total force on it divided by its mass:

```
a = F_total / m
```

- `F_total` is the vector sum of every force acting on the body this step, in newtons (N) if you use metres and kilograms.
- `m` is the body's mass in kilograms.
- `a` is the acceleration in m/s², which the integrator from week 7 turns into velocity and position.

A **force** is a push or pull with a direction and a size. Forces from different causes simply add as vectors. That gives you the most useful structure in game physics, the **force accumulator**. Each step you clear a force total, let every system (gravity, thrusters, springs, wind, drag) add its contribution, divide once by mass, and integrate once:

```python
class Body:
    def __init__(self, mass):
        self.inv_mass = 0.0 if mass == float("inf") else 1.0 / mass
        self.pos = [0.0, 0.0]
        self.vel = [0.0, 0.0]
        self.force = [0.0, 0.0]

    def add_force(self, fx, fy):
        self.force[0] += fx
        self.force[1] += fy

    def step(self, dt, gravity=(0.0, -9.81)):
        if self.inv_mass == 0.0:          # static or kinematic: forces do nothing
            self.force = [0.0, 0.0]
            return
        ax = self.force[0] * self.inv_mass + gravity[0]
        ay = self.force[1] * self.inv_mass + gravity[1]
        self.vel[0] += ax * dt            # semi-implicit Euler (week 7)
        self.vel[1] += ay * dt
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt
        self.force = [0.0, 0.0]           # forces last one step

crate = Body(2.0)
crate.add_force(10.0, 0.0)                # a 10 N push to the right
crate.step(1 / 60)
print([round(v, 4) for v in crate.vel])   # [0.0833, -0.1635]
```

Three details in that code are design decisions, and every engine makes them.

**Engines store inverse mass.** Dividing by mass is a multiplication by `1/m`, and storing `1/m` lets you represent an immovable body as `inv_mass = 0` instead of an infinite mass. A wall, a floor or a moving platform driven by animation has inverse mass 0. Week 10's impulse formula depends on this: an impulse against a body with inverse mass 0 changes nothing about that body.

**Gravity is added as an acceleration, not a force.** Near a planet's surface, the gravitational force on a body is `m·g`. Divide by `m` and every body gets the same acceleration `g`, whatever its mass. So engines skip the multiply-then-divide and add `g` straight to the acceleration. Box2D 3.1 does exactly this. Its velocity stage adds `h · invMass · force + h · gravityScale · gravity` to each body's velocity, where `h` is the step. Forces are scaled by inverse mass and gravity is not. It also sets the gravity scale to zero for bodies with zero inverse mass, so a kinematic platform never starts falling.

**Forces last one step.** The accumulator is cleared after every step. A thruster that should keep pushing must call `add_force` every step. An instant hit, such as a knockback, is not a force at all but an **impulse**, a change of momentum applied once. Week 10 covers impulses. The point for now is that mass divides both. The same 10 N push, or the same knockback impulse, moves a 2 kg crate five times as much as a 10 kg crate. If your design wants a heavy boss that barely moves when hit and a light imp that flies across the room, mass is the dial.

Check the printed numbers. The push gives `10 / 2 = 5` m/s² to the right, so `v_x = 5 / 60 = 0.0833` m/s. Gravity gives `v_y = −9.81 / 60 = −0.1635` m/s. The two directions are independent because forces add as vectors.

In CS203 week 2, a steering agent had a `max_accel` instead of a force and a mass. That is the same law with `F/m` folded into one number. It is the right simplification when every agent of one type has one mass. Unfold it when you want the same steering force to push a heavy troll and a light goblin differently.

## 2. Worked example: why Minecraft players never fall faster than 78.4 blocks per second

### The hook

Jump off a very tall pillar in Minecraft Java Edition. For the first second you speed up quickly. By the third second you are falling at about 55 blocks per second, and after that the gains get smaller and smaller. However long the fall, you never pass 78.4 blocks per second. A dropped item falls beside you at exactly half that limit, 39.2 blocks per second. There is no speed cap anywhere in the rule that produces this. The limit appears on its own, from one multiplication per tick.

### The model

The Minecraft Wiki documents the per-tick motion of every entity type as three operations: update the position, add the acceleration, apply drag. For players and other living entities in the air, in that order, each tick (1/20 s) runs:

```
y ← y + v          (position, using last tick's velocity)
v ← v − g          (gravity, g = 0.08 blocks per tick²)
v ← v · d          (drag, d = 0.98 per tick)
```

- `v` is the vertical velocity in blocks per tick. Multiply by 20 for blocks per second.
- `g` is the gravity added each tick.
- `d` is the **drag factor**, the fraction of velocity kept each tick. `d = 0.98` means 2% of the velocity is removed every tick.

Combine the last two lines into one: `v_next = (v − g) · d`. When the velocity stops changing, `v_next = v`. Call that value `v*` and solve:

```
v* = (v* − g) · d
v* · (1 − d) = −g · d
v* = −g · d / (1 − d)
```

With `g = 0.08` and `d = 0.98`: `v* = −0.08 × 0.98 / 0.02 = −3.92` blocks per tick, or **78.4 blocks per second**. That is the **terminal velocity**, the speed at which drag removes exactly as much speed per tick as gravity adds.

How fast do you approach it? Subtract `v*` from both sides of the update and the gap to terminal velocity shrinks by the factor `d` every tick. Starting from rest, the gap after `n` ticks is `d^n` of the full terminal speed:

```
v_n = v* · (1 − d^n)
```

That is an exponential approach, the same shape as the XP curves in MA101 week 4 turned upside down. To reach 90% of terminal speed you need `d^n = 0.1`, so `n = ln 0.1 / ln 0.98 ≈ 114` ticks, about 5.7 seconds.

### Numbers you can check

The following code runs as shown and checks the simulation against the closed form:

```python
G, DRAG = 0.08, 0.98            # Minecraft player: blocks per tick², per-tick drag
TERMINAL = G * DRAG / (1 - DRAG)

y, v = 0.0, 0.0                  # height fallen (negative is down), velocity per tick
for tick in range(1, 201):
    y += v                       # 1. position, with last tick's velocity
    v -= G                       # 2. acceleration
    v *= DRAG                    # 3. drag
    if tick in (1, 10, 20, 40, 60, 100, 200):
        closed = -TERMINAL * (1 - DRAG ** tick)
        print(f"tick {tick:3d}  t={tick / 20:5.2f}s  v={v * 20:7.2f} blocks/s  "
              f"closed form {closed * 20:7.2f}  fallen {abs(y):7.2f} blocks")
print(f"terminal velocity {TERMINAL:.2f} blocks/tick = {TERMINAL * 20:.1f} blocks/s")
```

```
tick   1  t= 0.05s  v=  -1.57 blocks/s  closed form   -1.57  fallen    0.00 blocks
tick  10  t= 0.50s  v= -14.34 blocks/s  closed form  -14.34  fallen    3.35 blocks
tick  20  t= 1.00s  v= -26.06 blocks/s  closed form  -26.06  fallen   13.25 blocks
tick  40  t= 2.00s  v= -43.46 blocks/s  closed form  -43.46  fallen   48.16 blocks
tick  60  t= 3.00s  v= -55.07 blocks/s  closed form  -55.07  fallen   97.52 blocks
tick 100  t= 5.00s  v= -68.00 blocks/s  closed form  -68.00  fallen  221.99 blocks
tick 200  t=10.00s  v= -77.02 blocks/s  closed form  -77.02  fallen  591.45 blocks
terminal velocity 3.92 blocks/tick = 78.4 blocks/s
```

| Time | Speed (blocks/s) | Share of terminal | Fallen (blocks) |
|---|---|---|---|
| 0.5 s | 14.34 | 18% | 3.35 |
| 1 s | 26.06 | 33% | 13.25 |
| 2 s | 43.46 | 55% | 48.16 |
| 3 s | 55.07 | 70% | 97.52 |
| 5 s | 68.00 | 87% | 221.99 |
| 10 s | 77.02 | 98% | 591.45 |

Check the first tick by hand. `v = (0 − 0.08) × 0.98 = −0.0784` blocks per tick, which is 1.568 blocks per second. The position did not move on tick 1, because the position update came first and used the old velocity of zero. That is the explicit Euler order from week 7. Under constant gravity it is harmless, as the week 7 check-yourself question showed.

Notice what the table says about game feel. Half of terminal speed arrives in under 2 seconds. Reaching 90% takes almost 6. A fall of 13 blocks (a tall building) is still in the fast-acceleration part of the curve, so for almost every fall a player makes in normal play, drag is barely noticeable. Drag matters for the rare, long falls, and there it quietly guarantees that no fall ever becomes too fast for chunks to load or collisions to catch.

### The visual

Open the interactive. The left chart plots speed against time for a falling body. The right chart plots the same fall as position against time. A dashed horizontal line on the left marks the terminal velocity `g·d/(1 − d)`, computed from the sliders, with its value printed beside it.

Start with the "Minecraft player" preset. Drag the drag slider from 0.98 toward 1.00. The terminal line rises, and at `d = 1` it vanishes: without drag the speed line is a straight ramp and the position curve is a parabola that never straightens. Move it back to 0.98 and watch the position curve bend into a straight line. That straight tail is falling at constant speed. Now switch the preset to "Item". The gravity halves and the drag stays the same, and the terminal speed halves exactly. Terminal speed is proportional to `g` when drag is fixed.

The "continuous" overlay draws `v(t) = v*·(1 − e^(−t/τ))` from section 3 on top of the tick-by-tick dots. They sit on the same curve.

### Cross-game recognition

**Minecraft's other entities (Java Edition, Minecraft Wiki, September 2026).** Every entity type follows the same three operations with its own numbers, and the wiki's terminal-velocity column is exactly our formula. Items and falling blocks have `g = 0.04` and `d = 0.98`, so `v* = 0.04 × 0.98 / 0.02 = 1.96` blocks per tick (39.2 blocks per second). Thrown snowballs, eggs and ender pearls have `g = 0.03` and `d = 0.99`, and in Java Edition 1.21.2 their order changed from "position, drag, acceleration" to "acceleration, drag, position". Drag now comes after gravity, so `v* = 0.03 × 0.99 / 0.01 = 2.97` blocks per tick. Under the old order, drag came before gravity and the fixed point was `v* = g / (1 − d) = 3.00`. The same two numbers, reordered, give a different speed limit. That is week 7's lesson about line order, measured in snowballs.

**Minecraft ground friction.** The same wiki page notes that a living entity standing on a block has horizontal drag `0.91 × friction`, with block friction 0.6 by default and 0.98 for ice. A mob sliding with no input keeps `0.91 × 0.6 = 0.546` of its speed per tick on stone and `0.91 × 0.98 = 0.8918` on ice. How far does it slide? With the position updated before the drag, the total distance is a geometric series, `v₀ · (1 + d + d² + …) = v₀ / (1 − d)` blocks. On stone that is `2.2·v₀`. On ice it is `9.2·v₀`, more than four times as far. Ice is slippery in Minecraft because a single per-tick factor moved from 0.546 to 0.892.

**Quake (id Software, 1996; WinQuake source released 1999).** Ground friction in `sv_user.c` (`SV_UserFriction`) lowers the player's horizontal speed each frame by `frametime × friction × max(speed, stopspeed)`, with `sv_friction = 4` and `sv_stopspeed = 100` units per second. Above 100 units per second that is linear drag, speed shrinking in proportion to itself at rate 4 per second. Below 100 it switches to a constant deceleration of 400 units/s², so the player actually stops instead of creeping toward zero forever. From a full run of 320 units per second, the exponential part takes `ln(3.2) / 4 ≈ 0.29` s and the constant part `100 / 400 = 0.25` s, so a Quake player stops in about half a second. Quake also clamps each velocity component to `sv_maxvelocity = 2000` in `SV_CheckVelocity`, a hard cap rather than drag.

**Box2D (version 3.1, `src/solver.c`).** Each body has a `linearDamping` coefficient `c` in 1/s. The velocity stage multiplies velocity by `1 / (1 + h·c)` every step. A comment in the source explains why: the exact solution of `dv/dt = −c·v` is `v·e^(−c·h)`, and `1/(1 + c·h)` is a cheap approximation to it that stays between 0 and 1 for any step size. Section 4 shows what happens with the other obvious approximation.

**The real world (NASA Glenn Research Center).** Air resistance on a moving object is not proportional to speed but to its square: `D = ½·ρ·v²·C_d·A`, with air density `ρ`, drag coefficient `C_d` and reference area `A`. Setting drag equal to weight `W` gives the terminal velocity `v_t = √(2W / (C_d·ρ·A))`. The shape is the same (a speed where drag balances gravity), the approach is different. Section 3 compares them.

Four games and one physics page, one model: a force that grows with speed, balanced against a constant pull, produces a speed limit. Whenever a game has a maximum fall speed, a coasting distance or a "top speed" that nothing clamps, look for the drag factor and compute `g·d/(1 − d)`.

### Eyes-open design judgment

- **Drag sets two things at once: the top speed and how quickly you reach it.** With a per-tick rule, top speed is `g·d/(1 − d)` and the time constant is about `1/(1 − d)` ticks. You cannot change one without the other unless you also change `g`. Tune both numbers together, with a target like "reach 90% of 60 blocks/s in 3 s", and solve for `g` and `d`.
- **Drag or a hard cap?** A clamp like Quake's `sv_maxvelocity` is cheap and exact, but it feels like hitting a wall: acceleration goes from full to zero in one frame. Drag gives a smooth approach and never quite reaches the limit. Many games use both, drag for feel and a clamp as a safety net for bugs, like Box2D's 400 m/s default speed limit from week 7.
- **Drag per tick is tied to the tick rate.** Minecraft's `0.98` means "per 1/20 s". Copy that number into a 60 Hz game and your players fall at a terminal speed about three times higher, reached three times more slowly. Section 4 shows the conversion.
- **Drag does not have to be physical.** Games apply different drag horizontally and vertically (Minecraft's 0.91 and 0.98), in the air and on the ground, and per material. Each is a feel dial. Name them in your design document and give each one a target number, a top speed or a stopping distance, instead of a raw factor.

## 3. Continuous drag: coefficients, time constants and mass

The per-tick rule hides a continuous law. Write drag as a force opposite to the velocity and proportional to it:

```
F_drag = −b · v        (linear drag, b in kg/s)
m · dv/dt = −m·g − b·v
```

Divide by `m` and set `c = b / m`, the **drag coefficient** in 1/s. The solution from rest is

```
v(t) = −v_t · (1 − e^(−c·t))       with   v_t = g / c   and   τ = 1 / c
```

`τ` (tau) is the **time constant**. After one `τ` the body has reached `1 − 1/e ≈ 63%` of terminal speed, after `ln 10 · τ ≈ 2.3·τ` it has reached 90%.

### Mapping a per-tick factor to a coefficient

Over one tick of length `Δt`, the exact solution multiplies the gap to terminal speed by `e^(−c·Δt)`. The per-tick rule multiplies it by `d`. Set them equal:

```
d = e^(−c·Δt)      so      c = −ln(d) / Δt
```

For Minecraft's player, `c = −ln(0.98) / 0.05 = 0.404` per second and `τ = 2.47` s. Gravity of 0.08 blocks per tick² is `0.08 × 20² = 32` blocks/s², about 3.3 times Earth's 9.81 m/s² if you read a block as a metre. So Minecraft's fall is strong gravity plus strong drag. That pairing reaches a high speed quickly and then levels off, and it makes a short hop feel snappy rather than floaty.

### Where mass enters

With linear drag, `v_t = m·g / b`. If two bodies have the same drag constant `b` (same shape and size), the one with twice the mass falls twice as fast at the end. With quadratic drag, `v_t = √(2·m·g / (ρ·C_d·A))`, and twice the mass gives only `√2 ≈ 1.41` times the speed.

Take an invented ball: mass 0.5 kg, `C_d = 0.5`, area 0.02 m², air density 1.2 kg/m³, `g = 9.81` m/s².

| Drag model | Terminal speed, 0.5 kg | Terminal speed, 1.0 kg | Time to 90% (0.5 kg) |
|---|---|---|---|
| Quadratic | 28.6 m/s | 40.4 m/s | 4.3 s |
| Linear, tuned to the same 28.6 m/s | 28.6 m/s | 57.2 m/s | 6.7 s |

Quadratic drag reaches its limit sooner because it is weak at low speed and strong near the top. It also makes heavy things only a little faster than light ones, which is what people expect from real objects.

Now the game-engine twist. Minecraft's rule has no mass at all: every entity type gets its own `g` and `d`. Box2D's `linearDamping` and similar settings in other engines are coefficients `c` in 1/s, not forces, so they slow a 1 kg body and a 1,000 kg body at the same rate. That is a sensible simplification for feel. It becomes a trap when a designer expects "heavier things fall faster" and gets identical falls. If you want mass to matter, write drag as a force `−b·v` (or `−k·|v|·v` for quadratic) into the accumulator from section 1, and let the division by mass do the rest.

## 4. Drag that survives a change of tick rate

Your game runs its physics at 60 Hz, and you want exactly Minecraft's fall. Two ways to get there.

**Convert through the coefficient.** From section 3, `c = −ln(d) / Δt`. The new per-step factor at step `h` is `d_new = e^(−c·h)`. That simplifies to `d_new = d^(h/Δt)`, the power rule from CS101 week 9. For `d = 0.98` at 20 Hz and `h = 1/60`, `d_new = 0.98^(1/3) = 0.99329`. Gravity per step must also be rescaled, because 0.08 is per tick squared: in per-second units it is 32 blocks/s², and you add `32 × h` per step.

**Use a damping formula that takes `c` and `h` directly.** Three common ones, all written as "multiply the velocity by":

```python
import math

def damp_exact(v, c, h):
    return v * math.exp(-c * h)

def damp_pade(v, c, h):          # Box2D 3.1's form
    return v / (1 + c * h)

def damp_linear(v, c, h):        # the "obvious" form
    return v * (1 - c * h)

h = 1 / 60
for c in (2, 20, 100, 150):
    print(f"c={c:3d}/s  c*h={c * h:5.3f}  exact {damp_exact(1, c, h):.4f}  "
          f"pade {damp_pade(1, c, h):.4f}  linear {damp_linear(1, c, h):+.4f}")
```

```
c=  2/s  c*h=0.033  exact 0.9672  pade 0.9677  linear +0.9667
c= 20/s  c*h=0.333  exact 0.7165  pade 0.7500  linear +0.6667
c=100/s  c*h=1.667  exact 0.1889  pade 0.3750  linear -0.6667
c=150/s  c*h=2.500  exact 0.0821  pade 0.2857  linear -1.5000
```

For gentle drag the three agree to three decimals. For strong drag they part ways. The linear form `1 − c·h` goes negative when `c·h > 1`, which means the body's velocity *reverses* each step: a crate on sticky mud jitters back and forth instead of stopping. Past `c·h > 2`, the factor is below −1 and the jitter grows every step until the crate flies off. That is the week 7 stability limit again. Drag is a "spring" acting on velocity, and the naive update of it has a stability limit just like the spring did.

The Padé form `1/(1 + c·h)`, the one Box2D uses, is always between 0 and 1. It damps too little for strong drag (0.375 instead of 0.189 at `c·h = 1.67`), but it can never reverse or explode. The exact form costs one `exp` call per body per step, which is usually affordable and makes the result independent of the tick rate.

Two takeaways. Store drag as a coefficient in 1/s in your data files, never as a per-frame factor, so the number means the same thing at any rate. And when a designer asks for "very high drag" (mud, water, a slow-motion zone), check `c·h` against 1 before you ship.

## 5. Putting it together: one step with forces

A complete step for a body now reads like this, in words:

1. Clear the force total.
2. Add every force: applied forces (thrust, wind, player input as a force), springs, and drag written as a force if mass should matter.
3. Compute `a = F_total · inv_mass + g`.
4. Semi-implicit Euler: `v += a·h`, then damping if you use a coefficient (`v *= 1/(1 + c·h)` or `e^(−c·h)`), then `x += v·h`.
5. Clamp speed to a safety cap if you have one.

Where you put the damping (step 4) is a choice with a measurable effect, as Minecraft's snowballs showed: drag before or after gravity changes the terminal speed by the factor `d`. Pick one, write it in your spec, and keep it the same for every entity type unless you want them to differ.

## In-class activity (25 minutes)

Work in groups of three with the interactive and a calculator.

1. (8 min) Your platformer runs at 60 Hz. The designer wants a falling player to reach 90% of a top speed of 20 m/s in 1.2 s. Using the per-step rule `v ← (v − g·h)·d`, find `d` and `g`. Hint: first find `n` steps for 1.2 s, then `d` from `d^n = 0.1`, then `g` from the terminal-velocity formula.
2. (7 min) Enter your `g` and `d` in the interactive's custom mode. Confirm the top speed and the 90% time. Then switch the tick rate to 30 Hz with "keep per-step numbers" on, and record the new top speed and 90% time. Switch "convert per-second" on and record them again.
3. (10 min) The same designer asks for a mud pool where the player's horizontal speed decays with `c = 90` per second. Which of the three damping formulas from section 4 are safe at 60 Hz? At 30 Hz? Write one sentence for the programmer.

Expected output: `g` and `d` with the working, the four numbers from step 2, and the verdict and sentence from step 3.

## Common misconceptions

- **"Terminal velocity is a speed cap the game enforces."** In Minecraft, nothing clamps the fall. The limit is the fixed point of `v ← (v − g)·d`. A clamp is a different tool with a different feel.
- **"Heavier objects fall faster."** Only when drag is a force. With no drag everything falls with the same `g`, and with engine damping coefficients (1/s) mass cancels out as well.
- **"A drag factor of 0.98 is a property of the object."** It is a property of the object *and the tick length*. At 60 Hz the same physics needs 0.9933.
- **"Damping can only slow things down."** The `1 − c·h` form reverses velocity when `c·h > 1` and explodes when `c·h > 2`. Use `1/(1 + c·h)` or `e^(−c·h)`.

## Check yourself

1. Minecraft experience orbs have `g = 0.03` blocks per tick² and `d = 0.98`, with acceleration applied before drag. Compute their terminal velocity in blocks per second. How many ticks do they need to reach 90% of it?
2. A player under the Slow Falling effect in Minecraft has `g = 0.01` with the player drag of 0.98. What is the terminal speed, and how does the time to reach 90% compare with a normal fall?
3. Convert a drag factor of 0.95 per tick at 20 Hz into a coefficient `c` in 1/s and into a per-step factor at 144 Hz.
4. A Quake player moving at 80 units per second releases all keys. Using the friction rule, how long until they stop, and how far do they slide? (Ignore frame rounding.)
5. A crate in a swamp level uses `v *= 1 - c*h` with `c = 70` per second. It behaves at 60 Hz. The console port runs physics at 30 Hz. What do players see?

<details>
<summary>Answers</summary>

1. `v* = 0.03 × 0.98 / 0.02 = 1.47` blocks per tick, which is 29.4 blocks per second (the wiki's value). 90% needs `0.98^n = 0.1`, `n ≈ 114` ticks, the same as players, because the time to 90% depends only on `d`.
2. `v* = 0.01 × 0.98 / 0.02 = 0.49` blocks per tick, 9.8 blocks per second. The time to 90% is still about 114 ticks (5.7 s), because `d` did not change. A slow faller reaches its lower top speed on the same schedule.
3. `c = −ln(0.95) / 0.05 ≈ 1.026` per second. At 144 Hz, `d = e^(−1.026 / 144) ≈ 0.99290`. Check: `0.95^(20/144) ≈ 0.99290`.
4. Below `stopspeed` the deceleration is constant: `friction × stopspeed = 4 × 100 = 400` units/s². Time to stop `80 / 400 = 0.2` s. Distance `80² / (2 × 400) = 8` units.
5. At 30 Hz, `c·h = 70/30 ≈ 2.33`, so the factor is `1 − 2.33 = −1.33`. The crate's velocity flips sign and grows by a third every step: it shakes and then flies out of the swamp. At 60 Hz `c·h = 1.17`, which already reverses velocity each step (factor −0.17) but shrinks it, so the jitter was too small to notice.

</details>

## Lab / assignment hook

[Lab 08, a force accumulator and three drag models](../labs/lab08.md). You complete a Python body with a force accumulator, reproduce Minecraft's documented terminal velocities from the per-tick rules, port the player fall to 60 Hz and 144 Hz without changing its feel, and break the linear damping formula on purpose. Deliverable: passing tests, one comparison plot and a one-page drag spec for a named game feel.

## Sources

- Minecraft Wiki, "Entity", section "Motion" (Java Edition, page as of September 2026). Per-tick operations and order; player gravity 0.08 and drag 0.98 (vertical), 0.91 (horizontal); ground drag `0.91 × friction` with friction 0.6 default and 0.98 for ice; items 0.04 and 0.98; experience orbs 0.03; thrown projectiles 0.03 and 0.99 with the order change in Java Edition 1.21.2; Slow Falling gravity 0.01; the terminal-velocity formulas and the table values 78.4, 39.2, 29.4, 59.4 and 9.8 blocks per second. https://minecraft.wiki/w/Entity
- id Software, Quake source code (WinQuake, GPL release 1999, game 1996), `WinQuake/sv_user.c` (`SV_UserFriction`) and `WinQuake/sv_phys.c` (`sv_friction` 4, `sv_stopspeed` 100, `sv_gravity` 800, `sv_maxvelocity` 2000, `SV_CheckVelocity`). https://github.com/id-Software/Quake
- Box2D, version 3.1.1 (June 2025), `src/solver.c`, `b2IntegrateVelocitiesTask`: damping factor `1/(1 + h·linearDamping)` with the source comment deriving it from `v·exp(−c·h)`; velocity change `h·invMass·force + h·gravityScale·gravity`; gravity scale zero for bodies with zero inverse mass. https://github.com/erincatto/box2d
- NASA Glenn Research Center, *Beginner's Guide to Aeronautics*, "The Drag Equation" and "Terminal Velocity" (pages checked September 2026). `D = Cd·ρ·V²·A/2`; `V = √(2W/(Cd·ρ·A))`. https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/drag-equation/ and https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/termvel/
- Millington, I. (2010). *Game Physics Engine Development* (2nd ed.). CRC Press. Chapters 3 and 5: damping in the integrator, force accumulators and drag force generators.

## Interactive spec: examples/w08-terminal-velocity.html

**Purpose.** Make visible that a per-tick drag multiplication creates a speed limit with no clamp, and that the limit is `g·d/(1 − d)`. The one insight: the speed curve flattens onto a line whose height the student can predict from two numbers, and the position curve straightens at the same moment. A second tab shows the damping formulas diverging when `c·h` passes 1.

**Layout.** Mobile-first. Tab 1, "Fall": two linked charts side by side on wide screens, stacked on narrow. Left: speed (blocks/s, positive downward) against time 0 to 12 s. Right: distance fallen (blocks) against the same time axis. On the left, a dashed horizontal line at the terminal speed with its value printed at the right end; a dotted vertical line at the 90% time with its value. A vertical time cursor, draggable, synchronized across both charts, with a readout of `t`, tick number, speed and distance at the cursor.

**Model, tab 1.** Per-tick simulation at rate `R` (ticks per second, default 20). Parameters `g` (blocks per tick²) and `d`. Order selector with three options:
- "Position, acceleration, drag" (Minecraft players): `y += v; v -= g; v *= d`.
- "Acceleration, position, drag" (Minecraft items): `v -= g; y += v; v *= d`.
- "Acceleration, drag, position" (Minecraft thrown projectiles since Java Edition 1.21.2): `v -= g; v *= d; y += v`.
Terminal speed shown as `g·d/(1 − d)` for the three orders above (drag after acceleration in all three), in blocks per tick and ×R in blocks per second. Plot each tick as a dot; connect with a thin line. Overlay toggle "continuous": `v(t) = v*·(1 − e^(−c·t))` with `c = −ln(d)·R`.

**Controls, tab 1.**
- Presets: "Minecraft player" (`g = 0.08`, `d = 0.98`, order 1, `R = 20`), "Item" (`0.04`, `0.98`, order 2), "Snowball, 1.21.2+" (`0.03`, `0.99`, order 3), "Slow Falling" (`0.01`, `0.98`, order 1), "Custom".
- Sliders: `g` 0.005 to 0.2 (step 0.005); `d` 0.90 to 1.00 (step 0.001). At `d = 1.00` hide the terminal line and show "no terminal velocity".
- Tick rate `R`: 20, 30, 60, 144. A switch "when changing rate: keep per-tick numbers / convert per-second". Convert mode sets `g_new = g·(20/R)²` and `d_new = d^(20/R)` (relative to the preset's 20 Hz values) so the curves overlap; keep mode leaves `g` and `d` and shows the feel changing.
- A ghost of the previous settings (thin gray curve) stays on screen after any change until "clear ghost" is pressed.

**Tab 2, "Damping formulas".** One chart: velocity against time 0 to 1 s, starting at `v = 10`, for three per-step rules at step `h = 1/R`, where `R` comes from tab 2's own step-rate buttons (20, 30, 60, 144, default 60), independent of tab 1's tick rate so that the test values below appear on first open: exact `v·e^(−c·h)`, Padé `v/(1 + c·h)`, linear `v·(1 − c·h)`. Slider `c` 0 to 200 per second, default 20. Readout of `c·h` and the three per-step factors to 4 decimals. When `c·h > 1`, show a warning "linear form reverses velocity"; when `c·h > 2`, "linear form is unstable". Clamp the y-axis to ±30 and mark points off-scale.

**Test values (must match).**
- Player preset: terminal 3.92 blocks/tick, 78.4 blocks/s; at `t = 1.00 s` (tick 20) speed 26.06 blocks/s and fallen 13.25 blocks; at tick 100 speed 68.00 and fallen 221.99; 90% time 5.70 s (tick 114).
- Item preset: terminal 1.96 blocks/tick, 39.2 blocks/s.
- Snowball preset: terminal 2.97 blocks/tick, 59.4 blocks/s.
- Slow Falling: 9.8 blocks/s.
- Tab 2 at `R = 60`: `c = 20` gives factors exact 0.7165, Padé 0.7500, linear 0.6667; `c = 100` gives 0.1889, 0.3750, −0.6667; `c = 150` gives 0.0821, 0.2857, −1.5000.

**First screen.** Player preset, both charts drawn, terminal line and 90% marker visible, no interaction needed.

**Accessibility and style.** All sliders keyboard-operable with visible focus, value text next to each. Live region announces the terminal speed when it changes. Respect `prefers-color-scheme` and `prefers-reduced-motion` (no animated drawing; charts update instantly). Use the shared tokens from `templates/interactive-tokens.css`, inlined. No game art or block textures: lines, dots and labels only.

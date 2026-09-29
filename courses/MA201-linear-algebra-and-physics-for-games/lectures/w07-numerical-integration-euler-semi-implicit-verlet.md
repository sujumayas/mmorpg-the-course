# MA201 · Week 07 — Numerical Integration: Euler vs Semi-implicit vs Verlet

**Why this matters:** Every physics object in your game moves because some loop turns forces into velocity and velocity into position, one step at a time. The order of two lines in that loop decides whether a planet keeps its orbit, whether a ragdoll lies still or explodes, and whether a stiff spring works at 60 Hz. This week you learn to pick that order on purpose and to predict what goes wrong when someone picks it by accident.

**You will be able to:**
- Compute one step of explicit Euler, semi-implicit Euler and Verlet by hand for a body under gravity, and state which one a given piece of engine code implements.
- Explain, with a drawing and with the energy formula, why explicit Euler makes a circular orbit spiral outward while semi-implicit Euler keeps it closed.
- Derive the explicit Euler growth factor `1 + ω²·dt²` for a spring and the semi-implicit stability limit `ω·dt < 2`, and use them to find the stiffest spring a 60 Hz simulation can hold.
- Choose an integrator for a given game system (projectile, orbit, cloth, character controller) and defend the choice in terms of cost, stability and accuracy.

**Before class:** Millington, *Game Physics Engine Development* (2nd ed., 2010), chapter 3, "The Laws of Motion", the sections on the integrator. Fiedler, G. "Integration Basics" (gafferongames.com, 2004), the whole article, about 15 minutes. Skim Jakobsen, T. "Advanced Character Physics" (GDC 2001), section 2 only.

**Prerequisites from earlier courses:** [CS101 week 9, delta time and frame-rate independence](../../CS101-programming-for-games-i/lectures/w09-delta-time-and-frame-rate-independence.md), section 3 (the jump whose apex depends on the frame rate, where you first met the words "semi-implicit Euler") and section 4 (the fixed-timestep accumulator). [MA101 week 12, 2D vectors](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w12-2d-vectors.md) (adding and scaling vectors). [MA201 week 6, kinematics](w06-kinematics-position-velocity-acceleration.md), for position, velocity and acceleration as rates of change.

**Interactive:** [`examples/w07-orbit-integrators.html`](../examples/w07-orbit-integrators.html). Keep it open during section 2.

---

## 1. What an integrator is

In week 6 you wrote motion as rates. Velocity is how fast position changes. Acceleration is how fast velocity changes. Newton's second law gives the acceleration from the forces, `a = F / m`. That is a description of motion, not a recipe for computing it. A game needs a recipe: given where a body is now and how fast it is going, where is it `dt` seconds later?

A few words to fix before we start:

- The **state** of a body is everything the next step needs. For a point body that is position `x` and velocity `v`, both vectors.
- The **time step** `dt` is how far forward one update jumps. In a fixed-timestep loop (CS101 week 9, section 4) it is a constant such as 1/60 s.
- An **integrator** is the rule that turns the state at time `t` into the state at time `t + dt`. The name comes from calculus, where finding position from velocity is called integration.
- The **exact solution** is the smooth curve the body would follow if `dt` were infinitely small. The integrator's output is a sequence of points that tries to stay on it.

The integrator never sees the curve. It sees one point and one slope, and it guesses. Every integrator is a different guess. The rest of this lecture is about what those guesses do after a thousand steps, because a game runs a thousand steps in about 17 seconds.

You already met the stakes in CS101. There, the same jump reached 76.67 px at 60 fps with one line order and 83.33 px with the other, against an exact 80 px. That was a small, constant error. This week you see the kind of error that grows without limit, and the kind that doesn't.

## 2. Worked example: the orbit that will not close

### The hook

Swap two lines in a physics loop and a planet that should circle forever flies off into space within a few orbits. Keep them in the other order and it circles for as long as you care to run it. Game physics engines are built around this fact. Box2D, the 2D engine behind a long list of physics games, runs its solver in stages, and the stage that updates velocities always runs before the stage that updates positions. Years before Box2D existed, IO Interactive built the ragdolls and cloth in *Hitman: Codename 47* (2000) on a third rule, Verlet integration. Its author, Thomas Jakobsen, chose it because the obvious rule let cloth particles "blow up".

Why would line order matter that much? Both orders use the same numbers, the same `dt`, the same force. Let's find out.

### The model

A body starts at `x` with velocity `v`. The force at `x` gives the acceleration `a(x)`. Three rules for one step:

```
Explicit Euler             Semi-implicit Euler        Velocity Verlet
x_new = x + v·dt           v_new = v + a(x)·dt        x_new = x + v·dt + ½·a(x)·dt²
v_new = v + a(x)·dt        x_new = x + v_new·dt       v_new = v + ½·(a(x) + a(x_new))·dt
```

- `x`, `v` are the position and velocity now, as vectors.
- `a(x)` is the acceleration the forces produce at position `x`.
- `x_new`, `v_new` are the state one step later.
- `dt` is the time step.

Read them slowly.

**Explicit Euler** moves the body with the velocity it had at the start of the step, then updates the velocity. It assumes nothing changes during the step.

**Semi-implicit Euler** (also called symplectic Euler) updates the velocity first, then moves with the *new* velocity. The only difference from explicit Euler is which velocity the position update uses. This is the "two lines swapped" from the hook.

**Velocity Verlet** moves the body using both the velocity and the acceleration, a parabola instead of a straight line. It then updates the velocity with the average of the old and new accelerations. It needs the acceleration at the new position, but that value is reused as `a(x)` in the next step, so it still costs one force evaluation per step.

Jakobsen's paper writes Verlet a different way, with no velocity at all. It stores the current position `x` and the previous one `x_prev`, and steps with `x_new = 2x − x_prev + a(x)·dt²`. The quantity `x − x_prev` is the distance moved last step, which stands in for velocity. With matching starting values the two forms produce the same positions. Games that need a velocity (for damage, sound, networking) use the velocity form. Cloth and ragdoll code often uses the position form, because moving a particle directly also changes its implied velocity, which makes constraints easy.

### The test case: a circular orbit

Put a body at `x = (1, 0)` with velocity `v = (0, 1)` and pull it toward the origin with inverse-square gravity:

```
a(x) = −x / |x|³        (gravity with GM = 1)
```

With these numbers the exact solution is a circle of radius 1, traversed once every `2π ≈ 6.28` seconds. The **total energy** of the body is

```
E = ½·|v|² − 1 / |x|
```

the kinetic energy plus the gravitational potential energy (per unit mass). On the exact circle `|v| = 1` and `|x| = 1`, so `E = 0.5 − 1 = −0.5` forever. Energy is our lie detector. An integrator that makes `E` climb is pumping energy into the system, and a body with more energy sits on a bigger orbit.

### Numbers you can check

Take one step with `dt = 0.1`. At the start, `a(x) = −(1, 0) / 1 = (−1, 0)`.

| Rule | `x_new` | `v_new` | `|x_new|` | `E` after the step |
|---|---|---|---|---|
| Exact circle | (0.99500, 0.09983) | (−0.09983, 0.99500) | 1.00000 | −0.50000 |
| Explicit Euler | (1.00000, 0.10000) | (−0.10000, 1.00000) | 1.00499 | −0.49004 |
| Semi-implicit Euler | (0.99000, 0.10000) | (−0.10000, 1.00000) | 0.99504 | −0.49999 |
| Velocity Verlet | (0.99500, 0.10000) | (−0.09975, 0.99500) | 1.00001 | −0.50000 |

Check the Euler row yourself. Position moves by `v·dt = (0, 0.1)`, so `x_new = (1, 0.1)`. Velocity changes by `a·dt = (−0.1, 0)`, so `v_new = (−0.1, 1)`. Then `|x_new| = √1.01 = 1.00499`, and `E = ½·1.01 − 1/1.00499 = 0.505 − 0.99504 = −0.49004`. One step, and explicit Euler has added about 0.01 of energy.

The semi-implicit row changes the velocity first, to `(−0.1, 1)`, then moves with it: `x_new = (1 − 0.01, 0.1) = (0.99, 0.1)`. The same numbers in a different order put the body slightly *inside* the circle instead of outside.

Now run a thousand steps. The following code runs as shown with `.venv/bin/python`:

```python
import math

def accel(x, y):
    """Gravity toward the origin with GM = 1."""
    r3 = (x * x + y * y) ** 1.5
    return -x / r3, -y / r3

def explicit_euler(x, y, vx, vy, dt):
    ax, ay = accel(x, y)
    return x + vx * dt, y + vy * dt, vx + ax * dt, vy + ay * dt

def semi_implicit(x, y, vx, vy, dt):
    ax, ay = accel(x, y)
    vx, vy = vx + ax * dt, vy + ay * dt
    return x + vx * dt, y + vy * dt, vx, vy

def velocity_verlet(x, y, vx, vy, dt):
    ax, ay = accel(x, y)
    x, y = x + vx * dt + 0.5 * ax * dt * dt, y + vy * dt + 0.5 * ay * dt * dt
    bx, by = accel(x, y)
    return x, y, vx + 0.5 * (ax + bx) * dt, vy + 0.5 * (ay + by) * dt

def energy(x, y, vx, vy):
    return 0.5 * (vx * vx + vy * vy) - 1 / math.hypot(x, y)

for step in (explicit_euler, semi_implicit, velocity_verlet):
    s = (1.0, 0.0, 0.0, 1.0)
    cells = []
    for n in range(1, 1001):
        s = step(*s, 0.1)
        if n in (1, 100, 1000):
            cells.append(f"r={math.hypot(s[0], s[1]):.4f} E={energy(*s):.4f}")
    print(f"{step.__name__:15s}", " | ".join(cells))
```

It prints:

```
explicit_euler  r=1.0050 E=-0.4900 | r=2.3039 E=-0.2607 | r=3.3949 E=-0.1095
semi_implicit   r=0.9950 E=-0.5000 | r=1.0379 E=-0.4959 | r=1.0433 E=-0.4990
velocity_verlet r=1.0000 E=-0.5000 | r=1.0046 E=-0.5000 | r=1.0005 E=-0.5000
```

In a table, with the exact answer `r = 1`, `E = −0.5` throughout:

| After | Explicit Euler `r`, `E` | Semi-implicit `r`, `E` | Velocity Verlet `r`, `E` |
|---|---|---|---|
| 1 step (t = 0.1) | 1.0050, −0.4900 | 0.9950, −0.5000 | 1.0000, −0.5000 |
| 100 steps (t = 10, about 1.6 orbits) | 2.3039, −0.2607 | 1.0379, −0.4959 | 1.0046, −0.5000 |
| 1,000 steps (t = 100, about 16 orbits) | 3.3949, −0.1095 | 1.0433, −0.4990 | 1.0005, −0.5000 |

Explicit Euler has more than doubled the orbit's size within two orbits and keeps climbing. Its energy only ever goes up. Semi-implicit Euler is not exact either: its radius wanders between about 0.955 and 1.055 over the whole run. But it wanders *around* the right answer and never drifts off. Verlet stays within half a percent.

### The visual

Open the interactive. Three panels show the same starting state stepped by the three rules, side by side, with the exact circle drawn faintly behind each. Below them, a shared graph plots energy against time for all three.

Press play at the default step, 60 steps per orbit. In the top row, the Euler planet spirals out while the others trace closed loops. In the graph, the Euler line climbs like a staircase and never comes back down. The semi-implicit line wiggles in a thin band around −0.5. The Verlet line is almost flat.

Now turn on "show one step". The panel freezes and draws a single step as arrows. Explicit Euler's arrow is the tangent to the circle at the start point, and a tangent always points outside a circle. Every step lands a little further out, and a planet further out has more energy. Semi-implicit Euler's arrow is bent toward the center before it is used, so it lands slightly inside. On the next step the body is closer to the center, gravity is stronger, and the error swings back the other way. That is the whole story: one rule makes an error that always has the same sign, the other makes an error that alternates.

Drag the step slider toward 400 steps per orbit. Euler's spiral slows but does not stop. A smaller step delays the escape, it does not prevent it.

### Cross-game recognition

**Box2D (version 3.1, source `src/solver.c`).** The solver's stage list runs `b2IntegrateVelocitiesTask` before `b2IntegratePositionsTask`. The first adds `h·invMass·force + h·gravity` to each body's velocity. The second adds `h·velocity` to the position, using the velocity the first stage just wrote. That is semi-implicit Euler, with `h` as the sub-step. Box2D also clamps each body's speed to a maximum (400 m/s by default in version 3.1) before moving it, a guard against runaway velocities.

**Hitman: Codename 47 (IO Interactive, 2000).** Jakobsen's GDC 2001 paper says the game's cloth, plants, rigid bodies and falling corpses all ran on position Verlet in the Glacier engine. His reasons match our table: the velocity is implied by two positions, so velocity and position cannot drift out of step. He also notes that Verlet can lose a little energy, and that replacing the 2 in `2x − x_prev` with something like 1.99 adds a small drag on purpose. To throw a body back when it was shot, the game moved the hit particle directly and let the integrator turn the displacement into motion.

**Minecraft (Java Edition, as documented on the Minecraft Wiki in September 2026).** Each entity type applies three operations per tick (update position, add acceleration, apply drag) in a fixed order, and the order varies by entity. Players and mobs update position first, using last tick's velocity, which is the explicit Euler order. Dropped items and falling blocks add acceleration first, then move, which is the semi-implicit order. In Java Edition 1.21.2, thrown projectiles such as snowballs and ender pearls switched from "position, drag, acceleration" to "acceleration, drag, position", from the explicit order to the semi-implicit one. Under constant gravity neither order is unstable, but the change moved where every thrown snowball lands. Week 8 uses these same entity rules to compute terminal velocity.

**The CS101 jump, revisited.** In CS101 week 9 you saw semi-implicit Euler land a 400 px/s jump at 76.67 px at 60 fps, and explicit Euler at 83.33 px, against an exact 80 px. Run the same jump with velocity Verlet and the apex sample is 80.00 px at 30, 60, 120 and 144 fps. Under constant acceleration the Verlet position update `x + v·dt + ½·a·dt²` is the exact kinematics formula from week 6, so it has no error at all at the sample points. The explicit and semi-implicit errors in that table have opposite signs for the same reason the orbits in this section err outward and inward.

Four systems, one decision. Whenever you read a physics update, find the line that changes the position and ask which velocity it uses.

### Eyes-open design judgment

- **Default to semi-implicit Euler.** It costs the same as explicit Euler, it needs one force evaluation per step, and it does not pump energy into orbits or springs. This is why Box2D uses it and why Fiedler recommends it as the default for games.
- **Reach for Verlet when positions are what you control.** Cloth, ropes, ragdolls and soft bodies are mostly constraints ("these two particles stay 0.3 m apart"). Position Verlet lets you fix a constraint by moving particles, and the velocity follows. The cost is that velocity-dependent forces such as drag need care, because there is no stored velocity to read.
- **Never ship explicit Euler for anything that oscillates.** Springs, orbits, pendulums, camera follow with overshoot, bobbing pickups. It is fine for a straight line at constant velocity, where every rule gives the same answer.
- **A smaller step is not a fix for the wrong rule.** It delays the failure and multiplies your cost. Change the rule first, then pick the step.
- **Accuracy is a design choice too.** Semi-implicit Euler's orbit wobbles 5% at 60 steps per orbit. For a decorative moon that is invisible. For a space game where players plan a landing from the predicted path, it is a bug report. If the player must predict the result, compute the prediction with the same integrator and step the game uses, or use an exact formula.

## 3. Why one rule gains energy: the spring

The orbit shows the effect. A spring shows the cause, with numbers you can derive by hand.

A body on a spring has acceleration `a = −ω²·x`, where `ω` (omega, in radians per second) sets how fast it oscillates. The spring stiffness `k` and mass `m` give `ω² = k / m`. The exact motion from `x = 1`, `v = 0` is `x = cos(ωt)`, and the quantity

```
A² = x² + (v / ω)²
```

stays exactly 1 forever. `A` is the **amplitude**, the height of the swing.

### Explicit Euler grows by a fixed factor every step

Apply explicit Euler: `x_new = x + v·dt` and `v_new = v − ω²·x·dt`. Expand `x_new² + (v_new/ω)²`:

```
x_new²        = x² + 2·x·v·dt + v²·dt²
(v_new / ω)²  = v²/ω² − 2·x·v·dt + ω²·x²·dt²
sum           = (x² + v²/ω²) · (1 + ω²·dt²)
```

The cross terms cancel exactly and what is left is the old `A²` times `1 + ω²·dt²`. Every single step, no matter where the body is in its swing, the squared amplitude grows by that factor. After `n` steps the amplitude has grown by `(1 + ω²·dt²)^(n/2)`. This is the orbit's staircase in its cleanest form. The error always has the same sign because `1 + ω²·dt²` is always bigger than 1.

For a gentle spring, `ω = 10` rad/s at 60 Hz, `ω·dt = 1/6`, the factor per step is `1 + 1/36`, and after 60 steps (one second) the amplitude is `(37/36)^30 ≈ 2.27` times bigger. A bobbing pickup that should float up and down by 10 cm is swinging by 23 cm after one second and by more than 30 m after ten.

### Semi-implicit Euler holds until `ω·dt = 2`

Semi-implicit Euler does not keep `A` exactly constant, but it keeps a slightly tilted version of it constant, so the amplitude stays bounded. The analysis (in Millington, chapter 3, and in the Fiedler article) gives one clean condition: the motion stays bounded if and only if

```
ω · dt < 2
```

Past that line, the spring explodes, exactly like explicit Euler but faster. Here is the check, which runs as shown:

```python
def peak_semi_implicit(w, dt, steps):
    """Largest |x| a semi-implicit spring reaches, starting at x = 1, v = 0."""
    x, v, peak = 1.0, 0.0, 1.0
    for _ in range(steps):
        v = v - w * w * x * dt
        x = x + v * dt
        peak = max(peak, abs(x))
        if peak > 1e6:
            return "blows up"
    return f"{peak:.3f}"

dt = 1 / 60
for w in (10, 60, 110, 119, 121):
    euler_growth = (1 + (w * dt) ** 2) ** 30      # one second = 60 steps
    print(f"w={w:3d}  w*dt={w * dt:.3f}  euler x{euler_growth:.3g} per second  "
          f"semi peak over 10 s: {peak_semi_implicit(w, dt, 600)}")
```

```
w= 10  w*dt=0.167  euler x2.27 per second  semi peak over 10 s: 1.003
w= 60  w*dt=1.000  euler x1.07e+09 per second  semi peak over 10 s: 1.000
w=110  w*dt=1.833  euler x1.54e+19 per second  semi peak over 10 s: 2.502
w=119  w*dt=1.983  euler x6.24e+20 per second  semi peak over 10 s: 7.762
w=121  w*dt=2.017  euler x1.39e+21 per second  semi peak over 10 s: blows up
```

| `ω` (rad/s) | `ω·dt` at 60 Hz | Explicit Euler amplitude growth per second | Semi-implicit peak over 10 s |
|---|---|---|---|
| 10 | 0.167 | ×2.27 | 1.003 |
| 60 | 1.000 | ×1.07 billion | 1.000 |
| 110 | 1.833 | — (already exploded) | 2.502 |
| 119 | 1.983 | — | 7.762 |
| 121 | 2.017 | — | blows up |

Two things to see. Semi-implicit Euler is bounded right up to the limit, but near it the swing is distorted: the peak is `1 / √(1 − (ω·dt/2)²)`, which is 2.50 at `ω·dt = 1.833`. A spring close to the limit is stable and still looks wrong. And the limit itself is sharp. At 60 Hz, `ω` must stay below 120 rad/s, so `k / m < 14,400`. A 1 kg ragdoll limb on a joint spring stiffer than 14,400 N/m will explode at 60 Hz no matter how carefully the rest of the code is written. Velocity Verlet has the same limit.

This is the practical reason physics engines run sub-steps (the Box2D 3.1 API notes that four sub-steps per step is usual) and use "soft" constraints instead of very stiff springs: halving `dt` doubles the stiffest `ω` you can hold, which quadruples the allowed `k / m`.

## 4. How the error shrinks when you shrink the step

Explicit Euler's orbit problem does not go away with a smaller step. The other two rules improve quickly. Here is the largest energy error over ten orbits, measured by the lab's code:

| Steps per orbit | `dt` | Explicit Euler | Semi-implicit | Velocity Verlet |
|---|---|---|---|---|
| 60 | 0.105 | 0.37 | 5.5 × 10⁻³ | 1.5 × 10⁻⁵ |
| 120 | 0.052 | 0.32 | 1.4 × 10⁻³ | 9.4 × 10⁻⁷ |
| 240 | 0.026 | 0.28 | 3.4 × 10⁻⁴ | 5.9 × 10⁻⁸ |
| 480 | 0.013 | 0.22 | 8.6 × 10⁻⁵ | 3.7 × 10⁻⁹ |

Each halving of the step divides the semi-implicit error by about 4 and the Verlet error by about 16 on this circular orbit. Explicit Euler barely moves, because its error is not a wobble that shrinks, it is a drift that accumulates over the ten orbits.

Two warnings about reading tables like this. First, the circular orbit is a friendly test: its symmetry cancels some error for the two stable rules. Start the same body with speed 1.2 instead of 1 and the orbit becomes an ellipse. Then each halving of the step only halves the semi-implicit error (0.0149, 0.0067, 0.0032, 0.0015) and quarters the Verlet error (0.00087, 0.00022, 0.000054, 0.000014). That is the textbook behavior: semi-implicit Euler is a **first-order** method, whose error scales with `dt`, and Verlet is **second-order**, scaling with `dt²`. You will reproduce both tables in the lab. Second, a smaller error per unit of time costs more steps per second. Going from 60 to 480 steps per orbit is eight times the CPU. For a game with a fixed budget per frame, the right question is "which rule gives acceptable error at the step I can afford?", not "which rule is most accurate?".

### What about fancier integrators?

You will read about fourth-order Runge-Kutta (RK4), which samples the acceleration four times per step and combines them. For smooth problems it is far more accurate per step. Fiedler's article tests it against semi-implicit Euler on a spring and finds that RK4 keeps the frequency right but slowly loses energy, while semi-implicit Euler keeps the energy but drifts in phase. For games, RK4 has two practical problems. It needs four force evaluations per step, and games often cannot evaluate forces at made-up intermediate states (collisions and contacts happen at real positions). It is common in tools and offline simulation and rare in game physics loops.

## 5. Putting it in the game loop

An integrator only behaves the way this lecture describes if `dt` is fixed. Everything in section 3 depends on `ω·dt`: a spring that is stable at 60 Hz can explode on a frame that took 1/20 s. That is one more argument for the fixed-timestep accumulator you built in CS101 week 9. The accumulator guarantees the physics always sees the same `dt`, so the stability limit you tested is the one players get. When the integrator lives inside a physics library such as Box2D, the questions change to who owns each transform, when bodies sleep and how contact events reach gameplay code. [CS201 week 11, physics integration basics](../../CS201-game-engine-architecture/lectures/w11-physics-integration-basics.md) covers that side and does not repeat the step rules taught here.

Three rules of thumb for your own code:

1. **Sum all forces first, integrate once.** Compute gravity, springs, drag and thrust into one acceleration, then run one integrator step. Mixing "add some velocity, move, add more velocity, move" silently creates a different integrator. Week 8 builds this force accumulator.
2. **Write the order down.** In a design spec or a code comment, state "semi-implicit Euler, 60 Hz, 4 sub-steps". Two programmers who assume different orders will produce two different games, as Minecraft's projectile change shows.
3. **Test with energy.** For any closed system (no drag, no thrust), total energy should stay nearly constant. A one-line energy readout in a debug overlay catches the wrong integrator in seconds.

## In-class activity (25 minutes)

Work in pairs with paper, a calculator and the interactive.

1. (8 min) Each partner hand-computes two steps of one integrator for the orbit with `dt = 0.2`, starting at `x = (1, 0)`, `v = (0, 1)`. One partner uses explicit Euler, the other semi-implicit. Compute `|x|` and `E` after each step. Compare. Whose radius went up?
2. (7 min) Set the interactive to 20 steps per orbit (close to `dt = 0.3`). Record how many orbits the explicit Euler planet completes before its radius passes 3. Then find the smallest steps-per-orbit value at which it survives 10 orbits below radius 2.
3. (10 min) Your game has a 60 Hz physics tick and a grappling hook modeled as a spring with `k = 20,000 N/m` on an 80 kg character. Is it stable with semi-implicit Euler? If not, how many sub-steps per tick do you need? Write the calculation.

Expected output: the two-step hand table for both rules, the two numbers from step 2, and the sub-step calculation with its answer.

## Common misconceptions

- **"Euler is just less accurate, so use a smaller `dt`."** Explicit Euler's error on an oscillating system has a fixed sign and grows every step. A smaller `dt` slows the growth, it does not stop it. Change the rule.
- **"Semi-implicit Euler conserves energy."** It keeps energy *bounded*, oscillating in a band around the true value. The orbit radius still wobbles by 5% at 60 steps per orbit. Bounded is not exact.
- **"Verlet can't give me a velocity."** Position Verlet stores none, but `(x − x_prev) / dt` is an estimate of it, and velocity Verlet stores it directly. Both produce the same positions.
- **"Stable means correct."** A semi-implicit spring at `ω·dt = 1.9` is stable and swings about three times too far. Stay well below the limit, not just under it.

## Check yourself

1. A body is at `x = (0, 2)` with `v = (1, 0)` under the orbit's gravity `a(x) = −x / |x|³`, and `dt = 0.1`. Compute one step of explicit Euler and one step of semi-implicit Euler. Which result is farther from the origin?
2. A bobbing pickup uses explicit Euler on a spring with `ω = 6` rad/s at 30 Hz. By what factor has its amplitude grown after 3 seconds?
3. Your cloth simulation runs semi-implicit Euler at 120 Hz. What is the largest `k / m` it can hold? If a designer drops the physics rate to 30 Hz to save CPU, what happens to cloth tuned at `k / m = 20,000`?
4. A programmer writes `position += velocity * dt` and then `velocity += gravity * dt` for a projectile under constant gravity, and argues that the order doesn't matter since nothing oscillates. Is the code stable? Is it correct? What changes if you add a spring?

<details>
<summary>Answers</summary>

1. `|x| = 2`, so `a = −(0, 2)/8 = (0, −0.25)`. Explicit: `x_new = (0.1, 2)`, `v_new = (1, −0.025)`, `|x_new| = √4.01 ≈ 2.0025`. Semi-implicit: `v_new = (1, −0.025)`, `x_new = (0.1, 1.9975)`, `|x_new| = √(0.01 + 3.990006) ≈ 2.0000`. Explicit Euler lands farther out.
2. `ω·dt = 6/30 = 0.2`, factor per step `1 + 0.04 = 1.04` on the squared amplitude. 3 s is 90 steps, so the amplitude grows by `1.04^45 ≈ 5.84`.
3. `ω·dt < 2` gives `ω < 240` rad/s, so `k / m < 57,600`. At 30 Hz the limit is `ω < 60`, `k / m < 3,600`. Cloth at 20,000 has `ω ≈ 141`, `ω·dt ≈ 4.7`, far past the limit, so it explodes.
4. Under constant gravity it is stable: velocity changes by the same amount every step, and the position error grows only as `½·g·dt·t`, the CS101 jump error. It is not exact (the jump overshoots). Add a spring and the acceleration depends on position, the explicit order starts adding energy every step, and the motion grows without bound.

</details>

## Lab / assignment hook

[Lab 07, three integrators and an energy meter](../labs/lab07.md). You implement the three step functions in a Python starter, pass tests built from this lecture's hand-computed first step and energy tables, then measure an elliptical orbit and a spring at the stability limit. Deliverable: passing code, two plots and a 300-word integrator recommendation for a named game system. Problem set 3 draws on it.

## Sources

- Box2D, version 3.1.1 (June 2025), `src/solver.c`: `b2IntegrateVelocitiesTask` runs before `b2IntegratePositionsTask`; velocity update `h·invMass·force + h·gravity`; position update `deltaPosition += h·linearVelocity`; speed clamp in the position stage. `src/types.c`: default `maximumLinearSpeed = 400 m/s` (times length units per meter). https://github.com/erincatto/box2d
- Jakobsen, T. (2001). "Advanced Character Physics". Game Developers Conference 2001, IO Interactive. Verlet scheme `x' = 2x − x* + a·dt²`, used in *Hitman: Codename 47* for cloth, plants, rigid bodies and corpses; the 1.99 drag trick; moving particles to apply hits. Copy used: https://www.cs.cmu.edu/afs/cs/academic/class/15462-s13/www/lec_slides/Jakobsen.pdf
- Minecraft Wiki, "Entity", section "Motion" (Java Edition, page as of September 2026). The three per-tick operations, per-entity ordering, and the note that thrown projectiles changed order in Java Edition 1.21.2. https://minecraft.wiki/w/Entity
- Fiedler, G. (2004, June 1). "Integration Basics". gafferongames.com. Explicit vs semi-implicit Euler on springs; RK4 compared with semi-implicit Euler; recommendation of semi-implicit Euler for games. https://gafferongames.com/post/integration_basics/
- Millington, I. (2010). *Game Physics Engine Development* (2nd ed.). CRC Press. Chapter 3, the particle integrator.
- CS101 week 9 (this program), section 3, for the jump apex values at 30 to 144 fps.

## Interactive spec: examples/w07-orbit-integrators.html

**Purpose.** The signature example for MA201. The one insight: explicit Euler's error always points outward, so the orbit spirals away and energy climbs step after step, while semi-implicit Euler's error alternates and the orbit stays closed. Two linked views: orbits (looks like "a bit off") and energy over time (reveals "one of these is broken").

**Layout.** Mobile-first. Top: three square canvases in a row on wide screens, stacked on narrow screens, titled "Explicit Euler", "Semi-implicit Euler", "Velocity Verlet". Each shows the origin (a small filled circle for the attractor), the exact circle of radius 1 as a faint dashed line, the body as a dot, and its trail (last 2,000 points). World view spans −4 to 4 on both axes; add an "auto-zoom" checkbox that fits the largest radius so far. Below: one shared line chart of energy `E` against time `t` for the three methods (three series, same colors as the panel titles, labelled directly at the line ends, not only by legend), with a dashed reference line at `E = −0.5`. Y-axis from `min(−0.6, E0 − 0.1)` rounded down to a multiple of 0.1, up to 0.1, clamped, where `E0 = ½·v0² − 1` is the starting energy. The lower limit reaches −1.0 at `v0 = 0.6` (`E0 = −0.82`), so slow starts stay on the chart. Values above 0.1 are drawn at the top edge with a marker "escaped".

**Model.** GM = 1. `a(x, y) = (−x, −y) / (x² + y²)^1.5`. Start `x = (1, 0)`, `v = (0, v0)`. Step rules exactly as in the lecture:
- Explicit: `x += v·dt` using old `v`, then `v += a(old x)·dt`.
- Semi-implicit: `v += a(x)·dt`, then `x += v·dt`.
- Velocity Verlet: `x += v·dt + ½·a(x)·dt²`, then `v += ½·(a(old x) + a(new x))·dt`.
Energy `E = ½·|v|² − 1/|x|`. Use float64 (JS numbers). If `|x| < 0.05` for any method, stop that method and show "crashed into the center".

**Controls.**
- Steps per orbit slider: 10 to 400, default 60, with `dt = 2π / stepsPerOrbit` shown to 4 decimals. The lecture's hand table uses `dt = 0.1`; add a "dt = 0.1 exactly" button that sets `dt = 0.1` (label shows "≈ 62.8 steps per orbit").
- Initial speed `v0` slider: 0.6 to 1.3, default 1.0 (1.0 is circular; other values give ellipses; for `v0 ≥ √2 ≈ 1.414` the exact orbit escapes, so cap at 1.3).
- Play/pause, "Step once", Reset. Simulation speed: steps per animation frame 1 to 20, default 4.
- "Show one step" toggle: pauses and draws, on each panel, the current position, the velocity arrow used for the position update (for explicit, the old velocity, tangent to the circle; for semi-implicit, the new velocity), and the landing point, with the exact circle so the student sees outside vs inside.
- Method checkboxes to hide any panel's series in the chart.

**Readouts.** Under each panel: step count `n`, time `t` (2 decimals), `r = |x|` (4 decimals), `E` (5 decimals), min and max `r` so far (4 decimals). These must be copyable text.

**Test values (must match to the shown decimals, `dt = 0.1` button, `v0 = 1`).**
- After 1 step: explicit `x = (1.00000, 0.10000)`, `r = 1.0050`, `E = −0.49004`; semi-implicit `x = (0.99000, 0.10000)`, `r = 0.9950`, `E = −0.49999`; Verlet `x = (0.99500, 0.10000)`, `r = 1.0000`, `E = −0.50000`.
- After 100 steps: explicit `r = 2.3039`, `E = −0.26071`; semi-implicit `r = 1.0379`, `E = −0.49590`; Verlet `r = 1.0046`, `E = −0.49999`.
- After 1,000 steps: explicit `r = 3.3949`, `E = −0.10949`; semi-implicit `r = 1.0433`, min/max `r` 0.9549 / 1.0551; Verlet `r = 1.0005`.

**First screen.** Autoplay (unless `prefers-reduced-motion`, then show the state after 300 steps, drawn statically, with a Play button) at 60 steps per orbit so the spiral and the climbing energy line are visible within 3 seconds, before the student touches anything.

**Accessibility and style.** Keyboard: all controls focusable, Space toggles play, `.` steps once. Live region announces "Explicit Euler energy now E = …" at most once per second while playing, off by default with a toggle. Respect `prefers-color-scheme`. Use the shared tokens from `templates/interactive-tokens.css`, inlined. No game art: dots, circles and lines only.

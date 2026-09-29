# MA201 · Week 14 — Determinism and Floating Point

**Why this matters:** Every position, velocity and timer in this course has been a floating-point number, and so far you have treated them as real numbers. They are not. A float has a fixed number of significant bits, so the further a value is from zero the coarser its steps. Walk far enough from the origin and characters stutter, then freeze. Leave a server running for a week and its clock stops. And two machines running the same physics code can drift apart from a single rounding difference in the last bit. This week you learn to predict each of those failures with a formula, and to choose between floats, doubles and integers on purpose.

**You will be able to:**
- Compute the spacing between neighbouring float32 and float64 values at any magnitude, and use it to predict the smallest movement, the largest safe world and the longest safe uptime of a system.
- Explain which floating-point operations IEEE 754 guarantees to give identical bits on every machine, and name the compiler, library and threading effects that break that guarantee.
- Demonstrate with code that a one-bit difference grows until two simulations disagree completely, and state what this means for lockstep and replays.
- Choose between float32, float64, a shifted origin and fixed-point integers for a given world size and precision need, and defend the choice.

**Before class:** Goldberg, D. (1991), "What Every Computer Scientist Should Know About Floating-Point Arithmetic", *ACM Computing Surveys* 23(1), sections 1.1 and 1.2 (formats and relative error, about 20 minutes). The Python tutorial chapter "Floating-Point Arithmetic: Issues and Limitations" (15 minutes). Erin Catto, "Determinism" (box2d.org, August 2024), the whole post. Skim the Godot documentation page "Large world coordinates" up to its precision table.

**Prerequisites from earlier courses:** Looking ahead, [CS202 week 12, deterministic lockstep](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w12-deterministic-lockstep-rts.md) (next semester), section 3, sets lockstep's rules (non-associative addition, seeded random numbers, iteration order, local-only state, checksums). This week goes under them to the hardware and compiler. [CS101 week 9, the fixed timestep](../../CS101-programming-for-games-i/lectures/w09-delta-time-and-frame-rate-independence.md). [CS102 week 14, unit testing gameplay rules](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w14-unit-testing-gameplay-rules.md). [MMO404 week 11, physics in MMOs](../../MMO404-advanced-networked-simulation/lectures/w11-physics-in-mmos.md) (year 4) covers body ownership and resimulation. MA201 [week 4](w04-homogeneous-coordinates-and-projection.md) (reversed-Z depth, where you met "floats are densest near zero") and [week 7](w07-numerical-integration-euler-semi-implicit-verlet.md) (integration error, which is a different error from rounding).

**Interactive:** [`examples/w14-far-from-origin.html`](../examples/w14-far-from-origin.html). Keep it open during section 2.

---

## 1. What a float can hold

A **floating-point number** stores a value as a sign, a **significand** (the significant digits) and an **exponent** (a power of two that says where the binary point goes). It is scientific notation in base 2:

```
value = ± significand × 2^exponent,    1 ≤ significand < 2
```

The IEEE 754 standard fixes two formats you will meet everywhere.

| Format | Also called | Bits | Significand bits | Relative precision |
|---|---|---|---|---|
| binary32 | `float`, float32, single | 32 | 24 | 2⁻²⁴ ≈ 6.0 × 10⁻⁸ |
| binary64 | `double`, float64 | 64 | 53 | 2⁻⁵³ ≈ 1.1 × 10⁻¹⁶ |

Python's `float` is binary64. Most engines store positions and GPU data in binary32, at half the memory.

The number of significand bits is fixed, so the **gap** between one representable value and the next depends on the exponent. Between 1 and 2, float32 has 2²³ evenly spaced values. Between 2 and 4 it has the same count, spread over twice the distance. The gap doubles every time the value doubles:

```
gap32(x) = 2^( floor(log2 |x|) − 23 )
gap64(x) = 2^( floor(log2 |x|) − 52 )
```

The gap is also called one **ulp**, a "unit in the last place". Any result that lands between two floats is **rounded to the nearest** one, so a single rounding moves a value by at most half a gap. That is the only error a correctly rounded operation makes. The relative error is always tiny. The absolute error grows with the size of the number, and absolute error is what the player sees.

Two consequences follow. First, most decimal fractions are not exact. `0.1` in float32 is really `0.100000001490116…`. Doubles have the same problem further down, which is why CS202 week 12 could show `(0.1 + 0.2) + 0.3` and `0.1 + (0.2 + 0.3)` giving different answers. Second, adding a small number to a large one can do nothing at all. At `16,777,216 = 2²⁴` the float32 gap is 2, so `16,777,216 + 1` rounds back to `16,777,216`. Hold on to that one. It is this week's worked example. [CS101 week 1](../../CS101-programming-for-games-i/lectures/w01-programs-variables-and-types.md) showed this number line. This week turns the gap into a formula for speed and freeze distance.

In week 4 you used the fact that floats are densest near zero to spend depth-buffer precision where it was needed. Here the same fact turns into a problem, because game worlds are big.

## 2. Worked example: the walk that freezes 524 km from the origin

### The hook

Minecraft: Java Edition generates terrain out to a world border 29,999,984 blocks from the centre, and stores every entity's position as three doubles (the wiki's entity format lists `Pos` as a list of three doubles, while `Rotation` is two floats). That choice is deliberate. The Minecraft Wiki keeps a page of "distance effects" in Java Edition, and many of the entries are bugs where some system converts a position to a float along the way. The positional-audio bug MC-191170 is one example, where sounds come from the wrong place at high coordinates. At 30 million blocks a float32 can only hold every second block. A sound's position there is rounded by up to a whole block.

Engines have met the same wall. Unreal Engine 4 limited worlds to a `WORLD_MAX` of 21 km. Unreal Engine 5 introduced Large World Coordinates, which move engine types to doubles, and its default `WORLD_MAX` became 88 million km. Godot 4 can be compiled with `precision=double` for the same reason, and its documentation gives a table of how precision falls with distance.

Why would a game need to care about millimetres 100 km from the origin? Because every tick adds a small step to a large position, and the step is what gets rounded.

### The model

A character at position `x` moves `v·dt` per tick. In float32 the new position is rounded to the nearest multiple of the gap at `x`. So the step it actually takes is

```
actual step  = round( v·dt / gap32(x) ) × gap32(x)
actual speed = actual step / dt
```

- `v` is the intended speed and `dt` the tick length.
- `gap32(x)` is the float32 spacing at the character's position, from section 1. In 2D or 3D each coordinate is its own float, so use the gap of the coordinate that is changing.
- `round` rounds to the nearest whole number (ties to even, which you can ignore here).

Two things follow. The speed is **quantized**. It can only be a whole number of gaps per tick, so it comes out too fast or too slow depending on how `v·dt` falls between multiples. And if `v·dt < gap/2`, the step rounds to zero. The character **freezes**. The addition cannot represent a change that small.

The freeze condition gives a distance. For a walker at 1.4 m/s on a 60 Hz tick, `v·dt = 0.0233` m, so the character freezes once `gap32(x) > 0.0467` m. The gap first exceeds that at `gap = 2⁻⁴ = 0.0625` m, which starts at `x = 2¹⁹ = 524,288` m. **Beyond 524 km, a walking character in float32 cannot move at all.**

### Numbers you can check

The code below emulates float32 in Python. `f32` rounds a double to the nearest float32 by packing it into four bytes and unpacking it. Adding two float32 values in double precision is exact at these magnitudes, so `f32(a + b)` gives the same bits as a float32 addition would.

```python
import math, struct

def f32(x):
    """Round a Python float (a double) to the nearest float32."""
    return struct.unpack("<f", struct.pack("<f", x))[0]

def gap32(x):
    """Distance from float32 x to the next float32 away from zero."""
    return 2.0 ** (math.floor(math.log2(abs(x))) - 23)

v, dt = 1.4, 1 / 60                        # walking speed m/s, 60 Hz tick
print("   distance   float32 gap   double gap   speed after 60 ticks")
for x0 in [1, 10_000, 100_000, 200_000, 300_000, 600_000, 30_000_000]:
    x = start = f32(x0)
    for _ in range(60):
        x = f32(x + f32(v * dt))           # a float32 add: exact sum, then round
    print(f"{x0:>11,} m  {gap32(x0):9.3g} m  {math.ulp(x0):9.3g} m   {x - start:6.3f} m/s")
```

Output:

```
   distance   float32 gap   double gap   speed after 60 ticks
          1 m   1.19e-07 m   2.22e-16 m    1.400 m/s
     10,000 m   0.000977 m   1.82e-12 m    1.406 m/s
    100,000 m    0.00781 m   1.46e-11 m    1.406 m/s
    200,000 m     0.0156 m   2.91e-11 m    0.938 m/s
    300,000 m     0.0312 m   5.82e-11 m    1.875 m/s
    600,000 m     0.0625 m   1.16e-10 m    0.000 m/s
 30,000,000 m          2 m   3.73e-09 m    0.000 m/s
```

Check the 200 km row by hand. 200,000 lies between 2¹⁷ and 2¹⁸, so the gap is `2^(17 − 23) = 2⁻⁶ = 0.015625` m. The step `0.02333 / 0.015625 = 1.49` rounds to 1 gap, so the walker moves 0.015625 m per tick, or `0.015625 × 60 = 0.9375` m/s. That is 33% slow. At 300 km the gap doubles to 0.03125 m, the ratio is 0.75, which rounds up to 1 gap, and the walker runs at 1.875 m/s, 34% fast. At 600 km the ratio is 0.37, which rounds to 0.

So the failure is not a smooth decline. Between 131 km and 262 km everyone walks a third too slow, and between 262 km and 524 km they walk a third too fast. Past that, nobody walks. Faster movers survive further out. A 6 m/s horse freezes only when the gap exceeds 0.2 m, beyond 2²¹ m (2,097 km).

The double column shows why doubles fix this for any world a game needs. At 30,000 km a double still resolves 4 nanometres.

### A visual you can move

Open `examples/w14-far-from-origin.html`. The left view is a zoomed strip of ground around the character, 40 float32 gaps wide but never less than half a metre (0.625 m at the 200 km default), with a tick mark at every representable float32 position. A ghost marker moves smoothly at the intended speed while the real character jumps from tick to tick. The right view plots actual speed against distance from the origin on a logarithmic axis, for the chosen speed and tick rate. It is a staircase that hugs the intended speed near the origin, starts to swing above and below it, and drops to zero at the freeze distance.

Drag the distance slider out from 1 km. On the left the tick marks spread apart until the ghost walks away from a character that can no longer follow. On the right the marker climbs the staircase. Switch the representation to double and the staircase flattens onto the intended speed across the whole axis. Press "shift origin here" and watch the character's local position reset to zero and its motion become smooth again, which is section 3's fix.

### Cross-game recognition

The same gap formula is behind each of these, written in each engine's units.

**Unreal Engine 4 and 5 (UE5 documentation, 5.8 era).** Unreal measures in centimetres. A coordinate of 21 km, 2,100,000 cm, lies just above 2²¹, so its float32 gap is `2^(21 − 23) = 0.25` cm. That is the precision at the edge of UE4's `WORLD_MAX`. UE5's Large World Coordinates add double-precision versions of the engine's core math types and raise the default `WORLD_MAX` to 88 million km. The documentation still describes Large World Coordinates as a beta feature to use with caution when shipping, because every system that touches positions has to be converted.

**Godot 4 (documentation for 4.7).** Godot's large-world page lists single-precision steps by range, for example about 0.0002 between 2,048 and 4,096 and about 0.0039 between 32,768 and 65,536. Those are `gap32` at 2¹¹ and 2¹⁵, exactly our formula. It recommends staying within 2,048 to 4,096 units for a first-person game and allows larger ranges for third-person and top-down views, because the camera is further away and small errors are harder to see. Compiling with `precision=double` fixes positions and physics, but the page lists parts that stay single precision, including 2D rendering and some shader features. The GPU mostly works in float32, so a double-precision engine still converts to a camera-relative float at the last step.

**Unity 6.6 (documentation), and time.** Time is a coordinate too. Unity's `Time.time` is a float, and the documentation adds `Time.timeAsDouble`, recommending it for more precision over long periods. Section 3 shows what the float version does after a few days of uptime.

Three engines, one formula. Find the largest coordinate and the smallest step a system must represent, and check that `step > gap(largest)` with room to spare.

### Eyes-open design judgment

- **Size the world from the formula.** Decide the smallest movement you must represent (a sneaking character, a slow platform, a physics contact tolerance) and the tick rate. Then find where `gap32` exceeds twice that step. That is your float32 world radius, and a practical one is several times smaller, so that errors stay invisible.
- **Doubles are not free.** They double the memory and bandwidth of every position, and the GPU still wants float32. Most engines that use doubles convert to camera-relative float32 for rendering. Networked games often quantize positions on the wire anyway ([CS202 week 5](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w05-serialization-and-bit-packing.md)).
- **Shifting the origin is cheap and local.** Many games keep float32 but periodically move the world so the player is near the origin. This is a **floating origin** or origin rebasing. It fixes rendering and local physics, but every system holding an absolute position must be shifted in the same frame, and a server that simulates many distant players at once cannot have one origin for all of them. Servers then use doubles, integers, or per-region local coordinates.
- **Check every conversion.** Minecraft's distance bugs sit where a double position becomes a float for audio or lighting. In code review, ask where each value gets narrowed.

### Check this example

1. A stealth game lets players creep at 0.5 m/s on a 30 Hz tick in float32. At what distance from the origin does creeping first stop? At what distance does it first run at the wrong speed by more than 10%?
2. A space game uses float32 metres and wants 1 mm precision for docking. What is the largest coordinate it can use?
3. Explain why the 10 km and 100 km rows in the table show the same speed, 1.406 m/s.

<details>
<summary>Answers</summary>

1. `v·dt = 0.5 / 30 = 0.01667` m. Freezing needs `gap > 0.0333`, first true at `gap = 2⁻⁴` from `x = 2¹⁹ = 524,288` m. For errors, check each band. From 32,768 m to 262,144 m the step rounds to 4, 2 and then 1 gap, each 6.25% short. From `2¹⁸ = 262,144` m the gap is 0.03125 and 0.53 gaps rounds to 1, which is 87.5% fast. So the first error above 10% starts at 262 km.
2. The gap must be at most 1 mm, so `2^(e − 23) ≤ 0.001`, giving `e ≤ 13`. Coordinates up to `2¹⁴ = 16,384` m have gaps of at most 0.98 mm.
3. At 10 km the step is 23.89 gaps of 0.977 mm and rounds to 24. At 100 km it is 2.99 gaps of 7.8 mm and rounds to 3. Both give a step of 0.0234375 m, which is 1.406 m/s. Different gaps can happen to round to the same step.

</details>

## 3. Time is a coordinate too

A timer that adds `dt` every tick is a walker whose position is the current time. The same formula applies, and the numbers are worse because game time only grows. Here is a float32 clock that has been running for some hours, advanced by 600 ticks of 1/60 s, ten real seconds.

```python
import struct

def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]

dt = f32(1 / 60)
print("uptime   clock gap   ten real seconds of ticks read as")
for hours in [1, 5, 20, 40, 80, 150]:
    t = start = f32(hours * 3600.0)
    for _ in range(600):                   # 600 ticks at 60 Hz
        t = f32(t + dt)
    gap = 2.0 ** (int(start).bit_length() - 24)
    print(f"{hours:>4} h   {gap:9.3g} s   {t - start:7.3f} s")
```

Output:

```
uptime   clock gap   ten real seconds of ticks read as
   1 h    0.000244 s     9.961 s
   5 h     0.00195 s    10.547 s
  20 h     0.00781 s     9.375 s
  40 h      0.0156 s     9.375 s
  80 h      0.0312 s    18.750 s
 150 h      0.0625 s     0.000 s
```

After one hour the clock is already 0.4% slow. After 80 hours of uptime it runs at almost double speed, and after 6 days (2¹⁹ s is 145.6 hours) it stops. Every cooldown and respawn timer that reads this clock goes wrong with it, and an MMO server up for a week between maintenance windows reaches the last row.

The fix is simple and worth making a rule. **Count ticks in an integer, and compute time as `tick × dt` when you need it.** A 64-bit tick counter at 60 Hz lasts about 4.9 billion years. If you need seconds as a number, compute them in double. Unity offers `Time.timeAsDouble` for exactly this. Never accumulate a float clock by repeated addition, and never store "time since server start" in float32.

## 4. Determinism: what IEEE 754 promises

A simulation is **deterministic** if the same starting state and the same inputs always produce exactly the same bits. CS202 week 12 showed why lockstep networking and replays need it, and listed four leaks in your own code: summation order, shared random generators, container iteration order and local-only information. Fix those and one question remains. Will the *hardware and compiler* give the same bits for the same code?

The IEEE 754 standard gives a strong promise here. The basic operations (add, subtract, multiply, divide and square root) must be **correctly rounded**. The result is the exact mathematical answer rounded to the nearest representable value. There is exactly one right answer, so any conforming hardware produces the same bits for the same operation on the same inputs. That is why Erin Catto could report in 2024 that modern x64 and ARM CPUs give identical rounding for basic arithmetic.

The promise covers single operations. Programs break it in four ways, and all of them are about *which* operations actually run.

**Fused multiply-add (FMA).** Many CPUs have an instruction that computes `a × b + c` with one rounding instead of two. Compilers may substitute it for a separate multiply and add when allowed to "contract" the expression, so the bits depend on whether this compiler, for this CPU, chose to fuse. Python 3.13 exposes the instruction as `math.fma`:

```python
import math
a, b, c = 0.1, 10.0, -1.0
print(a * b + c)          # multiply rounds to exactly 1.0, then add
print(math.fma(a, b, c))  # one rounding at the end keeps the tiny remainder
```

Output:

```
0.0
5.551115123125783e-17
```

The same line of source code, compiled two ways, gives zero or not-zero. Both Box2D and Jolt Physics tell you to turn contraction off (`-ffp-contract=off` on GCC and Clang) for cross-platform determinism.

**Extended precision.** The old x87 floating-point unit on 32-bit x86 computed internally with 80-bit registers and rounded to 64 or 32 bits only when a value was stored to memory. Whether an intermediate result was rounded then depended on register pressure, which depended on the optimizer. Catto calls this era "the floating point dark ages". On 64-bit platforms SSE and NEON round each operation to its declared type, so it matters only for old 32-bit targets.

**Library functions.** IEEE 754 does not require `sin`, `cos`, `exp` or `atan2` to be correctly rounded, and each platform's C library implements them differently. Catto found that `atan2f` gave different answers on different platforms and wrote his own approximations for Box2D. Jolt's documentation gives the same advice and adds standard library functions whose behaviour differs between implementations, such as `std::sort` with equal keys and `std::hash`. `sqrt` is safe because it is one of the correctly rounded basic operations.

**Unsafe optimization flags and threads.** "Fast math" compiler settings allow the optimizer to reorder and simplify floating-point expressions as if they were real numbers, which changes rounding. Multithreading reorders work by timing. Box2D v3 keeps contact lists in a deterministic order by building per-thread bit arrays and merging them, instead of letting threads append in whatever order they finish. Jolt adds the processor's rounding mode and its flush-to-zero flags for very small numbers to the list of state that must match.

Engines that commit to determinism say what it costs. Box2D v3 claims cross-platform determinism across MSVC, GCC and Clang on x64 and ARM, with no settings needed. Jolt Physics offers it behind a `CROSS_PLATFORM_DETERMINISTIC` build option, which its documentation says makes the library about 8% slower. Both are explicit that determinism holds only if your game calls the engine in the same order with the same inputs.

## 5. Why the last bit matters

If FMA changes a result by 10⁻¹⁷, why care? Because many game simulations are **chaotic**. A small difference in state produces a slightly different collision angle, which produces a larger difference after the next bounce, and the difference multiplies each time. The code below runs a ball around a square arena with a round pillar in the middle. It runs the simulation twice, identical except that the pillar bounce is written once with a separate multiply and subtract and once with `math.fma`.

```python
import math

def run(seconds, fused, dt=1 / 120):
    """Ball at speed 1 in the box [-1, 1] x [-1, 1] with a round pillar of
    radius 0.5 in the middle. `fused` picks one of two ways to write the
    same bounce. Returns the final position."""
    x, y, vx, vy = 0.1, -0.8, math.cos(0.3), math.sin(0.3)
    for _ in range(round(seconds / dt)):
        x, y = x + vx * dt, y + vy * dt
        if abs(x) > 1:                        # wall: mirror velocity and position
            vx, x = -vx, math.copysign(2, x) - x
        if abs(y) > 1:
            vy, y = -vy, math.copysign(2, y) - y
        d = math.hypot(x, y)
        if d < 0.5:                           # pillar: reflect about the normal
            nx, ny = x / d, y / d
            dot = vx * nx + vy * ny
            if fused:
                vx, vy = math.fma(-2 * dot, nx, vx), math.fma(-2 * dot, ny, vy)
            else:
                vx, vy = vx - 2 * dot * nx, vy - 2 * dot * ny
            x, y = nx * (1 - d), ny * (1 - d)
    return x, y

for s in [10, 20, 25, 30, 40, 50, 55, 60]:
    (xa, ya), (xb, yb) = run(s, False), run(s, True)
    print(f"after {s:>2} s  gap {math.hypot(xa - xb, ya - yb):.1e}")
```

Output:

```
after 10 s  gap 0.0e+00
after 20 s  gap 0.0e+00
after 25 s  gap 4.9e-14
after 30 s  gap 4.4e-12
after 40 s  gap 8.4e-09
after 50 s  gap 1.9e-05
after 55 s  gap 2.7e-03
after 60 s  gap 1.4e+00
```

The printed position gap is zero at 10 and 20 seconds, yet the runs are not identical. Hash the full state, velocity included, every tick (lab 14 does this) and the first difference appears at tick 191, the first pillar bounce, 1.6 s in. A later rounding happens to erase it at tick 613. A second difference appears at tick 1,402 (11.7 s) and never goes away. At first it lives only in the last bits of the velocity, too small to change the position it is added to. It reaches the positions at tick 2,012 (16.8 s), flickers in and out of them until tick 2,464 (20.5 s), which is why the printed gap at 20 s is still zero, and stays in them from then on. From 25 s the position gap grows by a factor of roughly 40 to 500 every 5 seconds. By 60 seconds the balls are 1.4 units apart in an arena 2 units wide. The runs are unrelated. (Tick numbers count from 0, as `first_divergence` does in the lab.)

Three lessons follow.

- **"Close enough" is not a tolerance you can use for lockstep.** Any difference, however small, will grow. Lockstep peers, rollback resimulation and replays need identical bits, and checksums (CS202 week 12) must hash the exact bits, not rounded values.
- **A desync shows up long after its cause, and only in what you hash.** The lasting difference was born at 11.7 s in a velocity and reached a millimetre at 52.9 s. A checksum of positions alone sees the first difference at tick 407 instead of 191, 1.8 s late, and the lasting one at 16.8 s instead of 11.7 s. Hash everything the next tick reads, every tick.
- **Chaos is not an integrator bug.** Week 7's integrators control drift from the true physics. Rounding decides whether two copies of the *same* simulation drift apart.

## 6. Fixed point: uniform steps, limited range

The alternative CS202 mentioned is **fixed point**. Store every position as an integer count of a small unit, such as millimetres. The spacing is then the same everywhere, 1 mm at the origin and 1 mm at the edge, and integer arithmetic is exact and identical on every machine.

| Representation | Spacing at 1 km | Spacing at 1,000 km | Largest coordinate |
|---|---|---|---|
| float32 metres | 0.061 mm | 62.5 mm | about 3.4 × 10³⁸ |
| int32 millimetres | 1 mm | 1 mm | 2,147 km (2³¹ mm) |
| float64 metres | 1.1 × 10⁻¹³ m | 1.2 × 10⁻¹⁰ m | about 1.8 × 10³⁰⁸ |

int32 millimetres beat float32 metres beyond 16,384 m, where the float gap passes 1 mm. The costs are real, though. A product of two millimetre values is in square millimetres and can overflow 32 bits, so every multiply needs a 64-bit intermediate and a rescale. Square roots and trigonometry need integer versions or tables. And the range is fixed. Catto rejected fixed point for Box2D because it would be slower, harder to write, limit world size and bring overflow bugs, once floats could be made deterministic.

Fixed point still suits data with a natural unit and a modest range, such as money, health in tenths, tile positions and tick counters. Many games mix the two, with a deterministic integer game state and floats for rendering and effects that no other machine needs to agree on.

## In-class activity (25 minutes)

Groups of three. Each group gets a world card with a world size, a tick rate, the slowest mover (with its speed), the longest session or server uptime, and whether the game uses lockstep.

1. **Precision budget (10 min).** For float32 metres, compute the gap at the world's edge, the slowest mover's step per tick, their ratio, and the float32 clock's gap after the stated uptime. Mark each as safe (step at least 20 gaps), visible (2 to 20) or broken (under 2).
2. **Choose (10 min).** Pick one representation for positions and one for time. Choose among float32, float64, float32 with a floating origin, and int32 or int64 fixed point. Write two sentences on what your choice costs.
3. **Determinism audit (5 min).** If the card says lockstep, list the three compiler or library settings from section 4 you would lock down, and one test you would run in continuous integration.

Expected output: a filled budget table, a two-sentence choice, and (for lockstep cards) the audit list.

## Common misconceptions

- **"Floating point is random, so it can't be deterministic."** Each basic operation has exactly one correct result, and conforming hardware gives it. Non-determinism comes from running different operations (FMA or not, a different `atan2`, a different order), not from the arithmetic itself.
- **"Switching to double makes the game deterministic."** Doubles fix precision, the size of the gap. They do nothing about FMA, library functions or order. A double simulation diverges just as the demo in section 5 does, only from a smaller first difference.
- **"Precision loss is gradual, so small errors far away are fine."** Movement error is a staircase that swings between too fast and too slow, then stops entirely (section 2). It shows up as broken gameplay, not as slight blur.
- **"Comparing with an epsilon fixes desyncs."** An epsilon hides a difference in one comparison, and chaos grows it back. Lockstep needs bit-identical state.

## Check yourself

1. What is the float32 gap at 5,000 m? At 70,000 m? Give both in millimetres.
2. A server stores `time_since_start` in float32 and adds `1/20` each tick at 20 Hz. After how many hours does the clock stop advancing?
3. A designer wants a 64 km × 64 km open world centred on the origin in float32, and the slowest thing that moves is a door hinge that rotates a 1 m door edge at 0.2 m/s, on a 60 Hz tick. Is that safe at the corners? Propose a fix if not.
4. Two peers run the same lockstep build, one compiled with GCC and one with Clang, and desync after 40 seconds. Name two causes from section 4 that fit, and the setting or code change that removes each.
5. Convert the float32 walker table's 300 km row into an int32 millimetre representation. What speed does the walker have there, and what is the largest distance this representation reaches?

<details>
<summary>Answers</summary>

1. 5,000 lies in [4,096, 8,192), so the gap is `2^(12 − 23) = 2⁻¹¹ = 0.488` mm. 70,000 lies in [65,536, 131,072), so the gap is `2⁻⁷ = 7.81` mm.
2. It stops when `dt = 0.05` is less than half the gap, so the gap must exceed 0.1. The first such gap is `2⁻³ = 0.125`, which starts at `2²⁰ = 1,048,576` s, or 291 hours (about 12 days). It runs at the wrong rate long before that.
3. The corners are at `x = y = 32,000` m. Each coordinate is a separate float in [16,384, 32,768), where the gap is `2⁻⁹ = 1.95` mm. The hinge edge moves `0.2 / 60 = 3.3` mm per tick, 1.71 gaps, which rounds to 2 gaps (3.9 mm). That is 17% fast, and as the edge turns, each axis's share of the step rounds differently, so the motion is visibly jerky. The fix is to simulate the door in its local frame (week 3), where positions are near zero, and convert to world space only for rendering. A floating origin also works.
4. Contraction of `a × b + c` into FMA by one compiler and not the other (fix with `-ffp-contract=off` on both, or write explicit operations). Different `sin`, `cos` or `atan2` implementations in each standard library (fix by using your own deterministic versions). Fast-math on either build is also possible.
5. The step `0.02333` m becomes 23 mm per tick after rounding to whole millimetres, which is `23 × 60 = 1.38` m/s everywhere, 1.4% slow at every distance. The error is the same at 300 km as at the origin. The range limit is `2³¹` mm, about 2,147 km. (You could store 23.33 mm steps exactly by using a smaller unit, or by carrying the remainder from tick to tick.)

</details>

## Lab / assignment hook

[Lab 14, precision budget and a determinism harness](../labs/lab14.md). Implement the float32 gap, quantized movement and clock functions and a per-tick state hash in Python, pass the tests, then run the lab's small arena simulation under two builds of the same bounce and use your hashes to find the first tick where they diverge. Finish by writing a one-page precision budget for your physics sandbox world.

## Sources

- IEEE Computer Society (2019). *IEEE Standard for Floating-Point Arithmetic*, IEEE 754-2019. Binary32 and binary64 formats (24 and 53 significand bits); correct rounding of add, subtract, multiply, divide, square root and fused multiply-add; elementary functions such as `sin` only recommended, not required, to be correctly rounded.
- Goldberg, D. (1991). "What Every Computer Scientist Should Know About Floating-Point Arithmetic." *ACM Computing Surveys* 23(1), 5-48. Relative error and ulps.
- Python Software Foundation, *Python 3.13 documentation*, `math.fma` (new in 3.13), `math.ulp`, `math.nextafter`, and the tutorial chapter "Floating-Point Arithmetic: Issues and Limitations" (accessed September 2026). All code outputs in this lecture were reproduced with Python 3.13.5.
- Minecraft Wiki, "Entity format" (Java Edition, page as of September 2026). `Pos` and `Motion` are lists of three doubles; `Rotation` is two floats. https://minecraft.wiki/w/Entity_format
- Minecraft Wiki, "Java Edition distance effects" (page as of September 2026). Vanilla bounds of ±29,999,984; effects caused by casting to float, including positional audio from the wrong location at high coordinates (bug MC-191170). https://minecraft.wiki/w/Java_Edition_distance_effects
- Epic Games, "Large World Coordinates in Unreal Engine 5" (Unreal Engine 5.8 documentation, accessed September 2026). Double-precision types; default `WORLD_MAX` of 88 million km; the UE4 `WORLD_MAX` of 21 km; described as a beta feature.
- Godot Engine documentation, "Large world coordinates" (Godot 4.7 documentation, accessed September 2026). Precision table by range; recommended ranges by camera type; the `precision=double` build option; features that remain single precision.
- Unity Technologies, Scripting API "Time.time" and "Time.timeAsDouble" (Unity 6.6 documentation, accessed September 2026). `Time.time` is a float; `timeAsDouble` is recommended for greater precision over extended periods.
- Catto, E. (2024). "Determinism." box2d.org, 27 August 2024. Algorithmic, multithreaded and cross-platform determinism in Box2D v3; x87 extended precision; fast-math; FMA disabled with `-ffp-contract=off`; custom `atan2f` because results differed across platforms; `sqrtf` deterministic; bit arrays to keep contact order; reasons for rejecting fixed point.
- Rouwé, J. Jolt Physics, `Docs/Architecture.md`, section "Deterministic Simulation" (GitHub master branch, accessed September 2026). `CROSS_PLATFORM_DETERMINISTIC` option about 8% slower; precise floating-point model; contraction off; consistent rounding and flush-to-zero flags; avoid standard trigonometry, `std::sort` and `std::hash`. https://github.com/jrouwe/JoltPhysics

## Interactive spec: examples/w14-far-from-origin.html

**The one insight the visual must make obvious:** a float's spacing doubles every time the distance from the origin doubles, so a fixed per-tick step becomes a staircase of wrong speeds and then stops. Near the origin the character follows its ghost. Far away it lags, overtakes, then freezes, while a double or a shifted origin stays smooth.

**Layout.** Two linked views side by side at 1280 px, stacked at 390 px (left view first).

- **Left, the ground strip.** A horizontal strip representing a window of width `max(40 × gap, 0.5 m)` around the character's current position. Draw a tick at every representable value of the current representation inside the window (float32 ticks at multiples of `gap32(x)`; for int32 mm, ticks every 1 mm; for float64, draw no ticks and label "gaps too small to draw"). Show a hollow ghost marker moving at exactly `v` and a filled character marker whose position is updated each tick by `x = round_repr(x + v·dt)`. Label the window's left edge with its absolute coordinate in metres. When the step rounds to zero, show a "frozen" badge.
- **Right, speed against distance.** Log-scale x axis from 1 m to 4 × 10⁷ m. Y axis from 0 to `2.2 × v`. Plot the actual speed `round(v·dt / gap(x)) × gap(x) / dt` for the chosen representation as a step function, a dashed horizontal line at `v`, and a vertical marker at the current distance. Show the float32 curve always in a muted colour for comparison when another representation is selected.

**Controls** (keyboard accessible, each with a visible value):

- Distance from origin: logarithmic slider from 1 m to 40,000 km, default 200 km. Also a numeric input.
- Speed `v`: 0.1 to 10 m/s, default 1.4.
- Tick rate: 20, 30, 60 or 120 Hz, default 60.
- Representation: float32, float64, int32 millimetres. Default float32.
- "Shift origin here" button. It stores an offset equal to the current position, so the stored local coordinate becomes 0 and the displayed world position stays the same. The strip keeps the absolute label. The right-hand marker moves to the local distance. A "reset origin" button undoes it.
- Play/Pause for the tick animation (paused and single-step button under `prefers-reduced-motion`).

**Readouts:** current gap in metres and millimetres, step `v·dt`, the ratio `v·dt / gap`, the rounded number of gaps per tick, actual speed and percent error, and the freeze distance for the current `v` and tick rate: the smallest power of two `2^e` with `2^(e − 23) > 2·v·dt` (float32). For float64 use `2^(e − 52)`. For int32 mm, freezing occurs only if `v·dt < 0.5` mm, independent of distance, and the range limit is 2,147,483.647 m. Show "out of range" past that.

**Formulas.** Use `Math.fround` for float32 rounding. Compute each tick as `x = Math.fround(x + Math.fround(v * dt))`. For float64 use plain JS numbers. For int32 mm, store `Math.round(x * 1000)` as an integer and add `Math.round(v * dt * 1000)` each tick. `gap32(x) = 2^(floor(log2|x|) − 23)`.

**Test values** (float32, `v = 1.4`, 60 Hz; speed measured over 60 ticks from the given start):

| Start distance | Gap | Speed |
|---|---|---|
| 1 m | 1.19 × 10⁻⁷ m | 1.400 m/s |
| 10,000 m | 0.000977 m | 1.406 m/s |
| 100,000 m | 0.00781 m | 1.406 m/s |
| 200,000 m | 0.0156 m | 0.938 m/s |
| 300,000 m | 0.0312 m | 1.875 m/s |
| 600,000 m | 0.0625 m | 0.000 m/s |
| 30,000,000 m | 2 m | 0.000 m/s |

Freeze distance for 1.4 m/s at 60 Hz is 524,288 m. For 6 m/s at 60 Hz it is 2,097,152 m. For int32 mm at 1.4 m/s and 60 Hz the step is 23 mm and the speed is 1.380 m/s at every distance.

**Style.** Use the shared tokens from `templates/interactive-tokens.css`, inline. No game art. Name games only in a short caption under the right view ("UE4 world edge", "Minecraft world border") as vertical reference lines at 21 km and 29,999,984 m.

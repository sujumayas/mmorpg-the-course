# CS101 · Week 14 — Polish Pass: Sound, Particles, Screen Shake

**Why this matters:** Next week you release your arcade game. The rules already work. What players notice in the first ten seconds is how a hit feels, and that comes from code you can write this week in under a hundred lines. Written carelessly, the same code shakes harder on fast monitors, eats your frame budget, and makes some players feel sick.

**You will be able to:**
- Implement trauma-based screen shake that stacks, clamps and decays at the same speed at 30, 60 and 144 frames per second.
- Compute shake strength and duration from trauma, decay rate and exponent, and predict how a small and a large hit will look.
- Write a particle emitter with an accumulator and dead-particle removal, and compute its steady-state particle count from rate and lifetime.
- Add pitch and volume variation to a sound in semitones and decibels, and design a polish pass with an accessibility setting for each effect.

**Before class:** Watch Squirrel Eiserloh, "Math for Game Programmers: Juicing Your Cameras With Math" (GDC 2016, GDC Vault or YouTube), the camera shake section (about 15 minutes). Read the Godot documentation (Godot 4) class pages for `Camera2D` (the `offset` property), `GPUParticles2D` (`amount` and `lifetime`) and `AudioStreamPlayer` (`pitch_scale` and `volume_db`).

**Prerequisites from earlier courses:** [CS101 week 9, delta time and the accumulator](w09-delta-time-and-frame-rate-independence.md) and [week 11, game states](w11-game-state-machines.md); every effect here updates with `delta`. [CS101 week 13, randomness](w13-randomness-spawning-and-procedural-variety.md) (separate generators for gameplay and effects; the no-repeat rule). [GD101 week 12, feedback, juice, clarity and readability](../../GD101-introduction-to-game-design/lectures/w12-feedback-juice-clarity-readability.md) covers when juice helps and when it hides information; this lecture covers how to code it. [MA101 week 9, easing curves](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w09-easing-curves-for-animation-feel.md) (smoothstep and ease-out) and [MA101 week 10, sin and cos](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w10-angles-radians-sin-cos.md) (turning an angle into a velocity, used for particles). Sound design itself belongs to [AU101](../../AU101-audio-for-games/syllabus.md).

**Interactive:** [examples/w14-trauma-shake.html](../examples/w14-trauma-shake.html). Keep it open during section 2.

---

## 1. Polish is code that listens

Polish (often called **juice**) is feedback that repeats and amplifies something that already happened in the rules. The enemy was already dead. The shake, the sparks and the crunch tell the player about it louder.

That gives you the structure for all of this week's code. Rules decide. Feedback listens. Keep them apart:

```python
def on_enemy_killed(enemy):
    score.add(enemy.points)              # rule
    trauma.add(0.3)                      # feedback
    sparks.burst(fx_rng, 24, enemy.x, enemy.y)
    sfx.play("pop", fx_rng)
```

In Godot you would emit a signal `enemy_killed` and connect the camera, the particle scene and the sound player to it. Either way, three habits follow:

1. **Effects never change the rules.** Removing every effect must leave the game playable and identical. That is how you test it, and it is what lets players turn effects off.
2. **Effects draw from their own random generator** (`fx_rng`), so they can never move a spawn. Week 13 section 1 explains why.
3. **Every effect updates with `delta`.** A polish pass is where frame-rate bugs from week 9 come back, because effects are short and fast and nobody times them.

The rest of this lecture builds the three effects that give the most feel per line of code: screen shake, particles and sound variation.

## 2. Worked example: screen shake that stacks, fades and behaves

### The hook

In Minecraft Java Edition 1.19.4, Mojang added an accessibility slider called "Damage Tilt." The Minecraft Wiki describes it as controlling how much the camera shakes when you get hurt, with a default of 100%. A game that barely shakes its camera still needed a dial for the one shake it has. Meanwhile Jan Willem Nijman of Vlambeer gave a whole 2013 talk, "The art of screenshake," built around a plain shooter that feels better with each small feedback change, shake included.

So shake matters a lot to how a hit feels, and players need control over it. Both facts point at the same thing. Shake should be one number your code can scale, not a tangle of `if` statements.

### The naive version and its four bugs

Here is what most first attempts look like:

```python
if just_got_hit:
    shake_timer = 0.3
if shake_timer > 0:
    camera.offset = (rng.uniform(-8, 8), rng.uniform(-8, 8))
    shake_timer -= 1 / 60
```

Four problems hide in five lines:

- **Every hit shakes the same.** A graze and a boss slam both give 8 pixels.
- **Hits don't stack, they reset.** A second hit during the shake restarts the timer. Five fast hits shake no harder than one.
- **The timer counts frames, not seconds.** `1/60` per frame lasts 0.3 s at 60 Hz, 0.125 s at 144 Hz and 0.6 s at 30 Hz.
- **The picture jitters.** A fresh random offset every frame means that at 144 Hz the camera jumps to 144 unrelated places a second. It looks like a broken video signal, not an impact.

### The model: trauma

Eiserloh's GDC 2016 talk introduced a cleaner model, and Godot tutorials have copied it since. Keep one number, **trauma** `T`, between 0 and 1. Hits add to it. Time drains it. The camera shakes by a power of it.

```
on hit:        T = min(T + amount, 1)
every frame:   T = max(T - d × dt, 0)
shake         = T ^ p
offset        = max_offset × shake × noise(t × f)
```

- `T` is trauma, 0 (calm) to 1 (maximum).
- `amount` is how much this event adds. A graze might add 0.2, a big hit 0.6.
- `d` is the decay rate in trauma per second. `dt` is the frame's delta time.
- `p` is the exponent, usually 2 or 3.
- `max_offset` is the largest shake in pixels, reached only at `T = 1`.
- `noise(x)` is a smooth random function in the range −1 to 1 (explained below), sampled at time `t` times a frequency `f`.

Each line fixes one of the four bugs. `amount` makes events differ. `min(T + amount, 1)` stacks hits and caps them. `d × dt` makes decay run in seconds. Noise instead of fresh random values stops the jitter. And `T ^ p` makes the effect feel right, which the numbers below show.

In Python this is a class with three short methods:

```python
class Trauma:
    def __init__(self, decay=0.8, power=2):
        self.value, self.decay, self.power = 0.0, decay, power

    def add(self, amount):
        self.value = min(self.value + amount, 1.0)

    def update(self, dt):
        self.value = max(self.value - self.decay * dt, 0.0)

    def shake(self):
        return self.value ** self.power
```

### Numbers you can check

Take one hit that adds `T = 0.5`, with `d = 0.8` per second, `p = 2` and `max_offset = 16` px. Trauma falls in a straight line, `T(t) = 0.5 − 0.8t`, and reaches 0 at `t = 0.5 / 0.8 = 0.625` s.

| Time (s) | Trauma `T` | Shake `T²` | Largest offset `16 × T²` (px) | Shake if `p = 1` (px) |
|---|---|---|---|---|
| 0.0 | 0.50 | 0.250 | 4.0 | 8.0 |
| 0.1 | 0.42 | 0.176 | 2.8 | 6.7 |
| 0.2 | 0.34 | 0.116 | 1.8 | 5.4 |
| 0.3 | 0.26 | 0.068 | 1.1 | 4.2 |
| 0.4 | 0.18 | 0.032 | 0.5 | 2.9 |
| 0.5 | 0.10 | 0.010 | 0.2 | 1.6 |
| 0.625 | 0 | 0 | 0 | 0 |

Look at the last two columns. With `p = 1` the shake falls in a straight line and stops dead at 0.625 s. With `p = 2` it falls fast and then trails off, dropping below one pixel after 0.31 s. That's an ease-out, the shape MA101 week 9 showed feels like a real impact settling. Trauma drains linearly. The shake you see does not.

Now compare hit sizes, still with `p = 2` and 16 px:

| Event | Trauma added | Shake `T²` | Peak offset (px) | With `p = 1` (px) |
|---|---|---|---|---|
| Graze | 0.2 | 0.04 | 0.6 | 3.2 |
| Big hit | 0.6 | 0.36 | 5.8 | 9.6 |
| Two big hits, fast | 0.6 + 0.6 → 1.0 (capped) | 1.00 | 16.0 | 16.0 |

A graze adds a third of a big hit's trauma, but with the square it gives about a tenth of the shake. Small events barely register. Big events stack into a full shake. The exponent is a contrast knob. It keeps the screen calm most of the time, so the one big moment stands out. That fits GD101 week 12's warning that when everything shakes, nothing does.

### Frame-rate independence, measured

The lab 14 tests run the decay at three frame rates. The table shows how long a 0.5 hit takes to calm down:

| Frame rate | Decay per frame `d/60` (the bug) | Decay `d × dt` (the fix) |
|---|---|---|
| 30 Hz | 1.27 s | 0.63 s |
| 60 Hz | 0.63 s | 0.63 s |
| 144 Hz | 0.26 s | 0.63 s |

With the fix, every machine calms after 0.625 s, give or take one frame. With the bug, a player on a 144 Hz monitor gets less than half the shake of a 60 Hz player. Week 9 showed the same bug in movement speed. Here it hides better, because nobody times a shake with a stopwatch.

### Noise instead of random

`rng.uniform(-1, 1)` each frame gives values with no relation to each other. **Noise** gives values that are random over long stretches but smooth over short ones. The simplest kind is **value noise**. Pick a random value at every whole number, then blend between neighbours with smoothstep:

```python
def value_noise(seed, x):
    i = math.floor(x)
    f = x - i
    s = f * f * (3 - 2 * f)                     # smoothstep
    a = random.Random(seed * 1_000_003 + i).uniform(-1, 1)
    b = random.Random(seed * 1_000_003 + i + 1).uniform(-1, 1)
    return a + (b - a) * s
```

Sample it at `t × f`. With `f = 15` the camera heads toward a new random target 15 times a second and glides between targets, whatever the frame rate. At 144 Hz, white random gives 144 jumps a second. Noise gives 15 smooth swings, drawn at 144 frames. Use a different seed for x and y so the two axes don't move together. Godot 4 has noise built in. The `FastNoiseLite` class generates Perlin, value and other noise types in the range −1 to 1.

Noise is also repeatable. The same seed and the same `t` give the same offset, so a recorded replay shakes the same way.

### See it move

Open the interactive. The left panel is a camera view of a simple scene with a crosshair at the true camera center. The right panel plots trauma (straight line) and shake (curve) over the last two seconds. Press "Graze" three times, then "Big hit" once. The trauma line jumps by the same steps you pressed. The shake curve barely moves for the grazes and spikes on the big hit. Set the exponent to 1 and the grazes suddenly rattle the screen. Switch the frame rate to 144 Hz and turn on "decay per frame (bug)". The shake cuts off early. Switch "noise" to "white random" and watch the left panel start to jitter.

### Cross-game recognition

**Godot tutorials (KidsCanCode, Godot Recipes).** The "Screen Shake" recipe embeds Eiserloh's talk and builds the same model on a `Camera2D`. It uses `decay = 0.8`, `trauma_power = 2` (the page suggests a range of 2 to 3), a maximum offset of 100 × 75 pixels plus a small maximum rotation of 0.1 radians, and gradient noise for the motion. Trauma is clamped with `min(trauma + amount, 1.0)` and drained with `max(trauma - decay * delta, 0)`. It is our model line for line. The code on that page is still in Godot 3 syntax (`export var`), so port it to `@export` when you copy the idea.

**Minecraft Java Edition (1.19.4 onward).** The Damage Tilt slider runs from 0% to 100%. In our model it is one more factor in the offset line, `max_offset × user_scale × shake × noise`. Because all shake in our code goes through that one line, adding the same setting to your game is one multiplication and one slider in the options menu.

**Vlambeer's shooter demo (INDIGO 2013).** Nijman's talk layers many small effects on each shot, and shake is one of them. Every shot adding a little and every explosion adding a lot is `trauma.add(small)` and `trauma.add(large)`, with the exponent keeping the small ones quiet.

In each case the pieces are the same: a single accumulated value, a cap, a time-based drain, a curve, and a global scale.

### Design judgment

- **Shake the view, not the world.** Move the camera's `offset` (the Godot docs name camera shake as a use of it), never the positions of the player or enemies. Collision and aim must not shake.
- **Keep UI still.** In Godot, put the HUD on a `CanvasLayer` so the camera offset does not move it. Players read health while hurt.
- **Choose the exponent deliberately.** `p = 2` is a good default. `p = 3` keeps the screen calmer and saves shake for the biggest events. `p = 1` makes every event visible, which is tiring in a game with many hits.
- **Tune `max_offset` to your resolution.** 16 px on a 320 × 180 pixel-art game is huge; on 1280 × 720 it is modest.
- **Always ship a scale setting**, 0% to 100%, and respect it everywhere. Shake can cause motion sickness. GD101 week 12 covers why. The code cost is one variable.
- **Decide what may not shake.** A shake during a precise platforming jump can cost the player a life. Some games add less trauma, or none, in states where precision matters (week 11's state machine is where you decide this).

A GDScript version for your arcade game:

```gdscript
extends Camera2D

@export var decay := 0.8
@export var power := 2.0
@export var max_offset := Vector2(16, 16)
var trauma := 0.0
var user_scale := 1.0        # from the options menu, 0.0 to 1.0
var t := 0.0
var noise := FastNoiseLite.new()

func add_trauma(amount: float) -> void:
    trauma = min(trauma + amount, 1.0)

func _process(delta: float) -> void:
    t += delta
    trauma = max(trauma - decay * delta, 0.0)
    var s := pow(trauma, power) * user_scale
    offset.x = max_offset.x * s * noise.get_noise_2d(1.0, t * 1000.0)
    offset.y = max_offset.y * s * noise.get_noise_2d(2.0, t * 1000.0)
```

The `1000.0` scales time into the noise's coordinates. FastNoiseLite's default `frequency` is 0.01, so this samples about 10 noise units per second, close to the Python version's 15. Tune it by eye in the interactive first, then match it here.

## 3. Particles: many tiny objects with a lifetime

A particle is a small, short-lived object with a position, a velocity and an age. An **emitter** creates particles and updates them. That's the whole idea. The data is a list of dictionaries (week 5 and 6):

```python
def update(self, dt, rng):
    self.to_emit += self.rate * dt              # 1. emit, with an accumulator
    while self.to_emit >= 1.0:
        self.burst(rng, 1)
        self.to_emit -= 1.0
    for p in self.particles:                    # 2. move and age
        p["vy"] += self.gravity * dt
        p["x"] += p["vx"] * dt
        p["y"] += p["vy"] * dt
        p["age"] += dt
    self.particles = [p for p in self.particles if p["age"] < self.lifetime]   # 3. remove dead
```

Two details matter.

**The accumulator.** A rate of 60 per second at 144 frames per second means 0.42 particles per frame. You can't emit 0.42 of a particle, so you keep the fraction in `to_emit` and emit whenever it passes 1. This is the same accumulator you used in week 9 for a fixed timestep: carry the leftover time (or particles) into the next frame. Without it you would emit one per frame, which is 144 per second on a fast machine and 30 on a slow one.

**Removal.** Never delete items from a list while a `for` loop walks over it. The loop skips the item after each deletion. Build a new list of survivors instead, as step 3 does.

`burst` gives each particle a random direction and speed, which is MA101 week 10's angle-to-velocity conversion:

```python
angle = rng.uniform(0, 2 * math.pi)
speed = rng.uniform(0.5, 1.0) * max_speed
vx, vy = speed * math.cos(angle), speed * math.sin(angle)
```

### The particle budget: count = rate × lifetime

How many particles are alive at once? If an emitter makes `r` particles per second and each lives `L` seconds, then after the first `L` seconds, particles die as fast as they are born, and the count settles at

```
alive = r × L
```

Godot uses this relation too. The `GPUParticles2D` docs state that the effective emission rate is `amount / lifetime` particles per second (times `amount_ratio`). So in Godot you set `amount` to the number alive at once, and the engine works out the rate. For bursts, multiply how often the burst happens by its size.

| Effect | Rate | Lifetime | Alive on average |
|---|---|---|---|
| Ship thruster | 60 per s | 1.5 s | 90 |
| Enemy death burst, 40 sparks, 5 kills per s in a busy wave | 200 per s | 0.6 s | 120 |
| Trails on 10 bullets, 30 per s each | 300 per s | 0.3 s | 90 |
| Total | | | 300 |

The lab 14 emitter, at 60 per second and 1.5 s, holds exactly 90 particles after 5 seconds, as the model predicts. The formula also tells you which knob to turn. If the busy wave drops frames, halving the sparks' lifetime cuts their count in half without changing how many appear per kill. Players notice a burst's size far more than how long the last faint sparks linger.

## 4. Sound: variation without a sound designer

The fastest sound polish is to stop playing the identical sample every time. The ear catches exact repeats, just as week 13's players caught repeated pieces. Two cheap fixes:

**Pitch variation.** Musical pitch is measured in **semitones**; 12 semitones double the frequency. To shift by `s` semitones, multiply the playback rate by `2^(s/12)`:

| Shift (semitones) | −2 | −1 | 0 | +1 | +2 | +12 |
|---|---|---|---|---|---|---|
| `pitch_scale` | 0.891 | 0.944 | 1.000 | 1.059 | 1.122 | 2.000 |

A random shift of up to ±1 or ±2 semitones per shot sounds like the same gun, never quite the same shot. In Godot, `AudioStreamPlayer.pitch_scale` is this multiplier. Its docs note that it changes pitch and tempo together, so a lower pitch also plays slightly longer.

```gdscript
func play_shot() -> void:
    $Shot.pitch_scale = pow(2.0, fx_rng.randf_range(-1.5, 1.5) / 12.0)
    $Shot.play()
```

**Volume variation.** Godot measures `volume_db` in **decibels**, a log scale. +6 dB is about double the amplitude and −6 dB about half, because `20 × log10(2) ≈ 6.02`. A random offset of ±1 to ±2 dB is enough.

Godot 4 bundles both ideas in `AudioStreamRandomizer`. Its `random_pitch` of 1.0 means no variation, and 2.0 means anywhere between half and double pitch, which is far too much for most sounds; a value of 1.12 gives about ±2 semitones. `random_volume_offset_db` of 3.0 means ±3 dB. With several recorded variants in its pool, the `PLAYBACK_RANDOM_NO_REPEATS` mode is week 13's NES-style rule for sound.

Give loud, frequent sounds a limit. Ten enemies dying in the same frame should not play ten pops at full volume. The simplest rule is "at most N copies of this sound at once." In Godot that is `max_polyphony` on the player. Its docs give a default of 1 and say that once the limit is reached, `play()` cuts off the oldest copy.

## 5. Running a polish pass

Polish is endless if you let it be. Run it as a pass with an order and a stopping rule:

1. **List the five most frequent events** in your game (shoot, hit, kill, pick up, get hurt) and the one rarest big event (boss dies, game over).
2. **Assign each a trauma amount, a particle burst and a sound**, as a table in a dictionary. Frequent events get small amounts (trauma 0.1 to 0.2). The rare event gets the most (0.6 or more).
3. **Implement one listener per event** that reads from the table. No magic numbers in gameplay code.
4. **Add the settings**: shake scale, particle amount scale, effects volume. Test the game with all three at 0. It must still play the same.
5. **Measure.** Print the particle count and frame time in the busiest wave. Compare with your `r × L` budget.
6. **Stop** when the rarest event clearly outranks the most frequent one in feel. More polish past that point starts to bury information.

## In-class activity (30 minutes)

Pairs, with the lab 14 starter and one team's arcade game from this term.

1. **Budget (8 min).** Fill in a copy of the section 3 table for your game's three busiest effects. Compute the total alive at once. Decide which effect you would cut first if you had to halve it.
2. **Tune by numbers (10 min).** Using the interactive, choose `amount` values for a graze and a big hit so that the graze peaks under 1 px and the big hit over 6 px at `max_offset = 16`. Write down your exponent. Check your choice with `amount² × 16` by hand.
3. **Bug hunt (7 min).** Run `python juice.py` on the unmodified starter. Explain from its output which two lines are wrong and what a 144 Hz player would see.
4. **Swap and critique (5 min).** Swap tables with another pair. Find one event where their shake or burst is bigger than its importance.

Expected output: a filled budget table, two `amount` values with the exponent, and a two-sentence bug explanation.

## Common misconceptions

- **"Screen shake is random offsets."** Fresh random offsets each frame jitter, and at high frame rates they jitter more. Use smooth noise sampled at a fixed frequency.
- **"A shake timer is enough."** A timer can't stack hits or vary strength. Trauma does both with one number.
- **"If it looks fine on my monitor, it's fine."** Any effect that counts frames runs at a different speed on a different display. Scale every change by `delta`, and test at 30 and 144 Hz (the lab tests do).
- **"More particles means more impact."** The count grows with `rate × lifetime`, so long-lived faint particles cost the most and add the least. Short, dense bursts read as impact.

## Check yourself

1. A hit adds 0.4 trauma. With `d = 1.0` per second, `p = 3` and `max_offset = 20` px, what is the peak offset, and after how many seconds does the camera stop shaking?
2. Trauma is 0.9 when a hit adding 0.5 lands. What is trauma right after? What would a timer-based shake have done instead?
3. You want a smoke emitter with about 150 particles alive, each living 2.5 s. What rate do you need? What would you set `amount` to in Godot's `GPUParticles2D`?
4. A gun sound plays with `pitch_scale` chosen uniformly from 0.8 to 1.25. Roughly how many semitones is that range, and is it a good choice for a gun fired ten times a second?
5. Your teammate decays trauma with `trauma *= 0.9` every frame. Is that frame-rate independent? Explain what a 144 Hz player sees compared with a 60 Hz player.

<details>
<summary>Answers</summary>

1. Shake `0.4³ = 0.064`, peak offset `20 × 0.064 = 1.28` px. Trauma reaches 0 after `0.4 / 1.0 = 0.4` s. With `p = 3` this hit barely moves the camera, which may be exactly right for a frequent event.
2. `min(0.9 + 0.5, 1) = 1.0`, the cap. The shake rises from `0.81` to `1.0` of the maximum. A timer would have restarted the same fixed shake, with no increase at all.
3. `r = alive / L = 150 / 2.5 = 60` per second. In Godot, `amount` is the number per cycle over one lifetime, so set `amount = 150` with `lifetime = 2.5`, and the docs' rate `amount / lifetime = 60` per second follows.
4. `12 × log2(0.8) ≈ −3.9` and `12 × log2(1.25) ≈ +3.9`, so about ±4 semitones, an 8-semitone spread. At ten shots a second that sounds like a melody, not a gun. A range of about ±1 to ±2 semitones is safer.
5. No. It removes 10% per frame, so at 144 Hz it removes 10% 144 times a second and the shake dies about 2.4 times faster than at 60 Hz. To keep a multiplicative fade, use `trauma *= pow(0.9, delta * 60)`, which removes the same share per second at any frame rate. (MA101 week 8 shows the same fix for lerp smoothing.)

</details>

## Lab / assignment hook

[Lab 14, headless juice](../labs/lab14.md). You fix the trauma class and particle emitter in the starter until the frame-rate tests pass at 30, 60 and 144 Hz, then port both to your Godot arcade game with a shake-scale setting in the options menu. The polish table from section 5 goes into your final release notes (week 15).

## Sources

- Eiserloh, S. (2016). "Math for Game Programmers: Juicing Your Cameras With Math." GDC 2016, GDC Vault; recording on the GDC YouTube channel. Camera shake from trauma, with noise-driven motion. https://gdcvault.com/play/1023557/Math-for-Game-Programmers-Juicing
- KidsCanCode, Godot Recipes, "Screen Shake" (4.x section; the page's code uses Godot 3 syntax). Embeds Eiserloh's talk; `decay = 0.8`, `max_offset = Vector2(100, 75)`, `max_roll = 0.1`, `trauma_power = 2` with a suggested range of 2 to 3, `min(trauma + amount, 1.0)`, `max(trauma - decay * delta, 0)`, OpenSimplex noise. https://kidscancode.org/godot_recipes/4.x/2d/screen_shake/index.html
- Minecraft Wiki, "Options" (Java Edition). Damage Tilt controls the amount of camera shake caused by being hurt, default 100%, added in 1.19.4 (snapshot 23w06a). https://minecraft.wiki/w/Options
- Nijman, J. W. (2013). "The art of screenshake." INDIGO Classes 2013, recording on the Dutch Game Garden YouTube channel.
- Godot Engine documentation (stable, Godot 4.7), `Camera2D`. The `offset` property, described as useful for camera shake.
- Godot Engine documentation (Godot 4.7), `GPUParticles2D`. `amount`, `lifetime`, and the effective emission rate `(amount × amount_ratio) / lifetime`.
- Godot Engine documentation (Godot 4.7), `AudioStreamPlayer`. `pitch_scale` as a multiplier that changes pitch and tempo; `volume_db` in decibels; `max_polyphony` (default 1) cuts off the oldest sound when the limit is reached.
- Godot Engine documentation (Godot 4.7), `AudioStreamRandomizer`. `random_pitch` (1.0 none, 2.0 between half and double), `random_volume_offset_db`, `PLAYBACK_RANDOM_NO_REPEATS`.
- Godot Engine documentation (Godot 4.7), `FastNoiseLite`. Perlin, value and other noise types, values mostly in −1 to 1, default `frequency` 0.01.
- Simulation figures in section 2 and 3: lab 14 starter with the reference solution, run with Python 3.13.5.

## Interactive spec: examples/w14-trauma-shake.html

**The one insight:** trauma drains in a straight line, but the shake you see is trauma squared, so small hits barely register, big hits dominate, and the fade is an ease-out. A second insight sits behind a toggle: decaying per frame instead of per second changes the shake with the monitor.

**Layout.** Two linked views, stacked on mobile, side by side from 900 px.

- **Left, "Camera":** a 16:9 viewport showing a generic scene (a grid floor, three rectangles as "enemies", a circle as the "player", all drawn with shapes, no art). The whole scene is drawn offset by `(dx, dy)`. A fixed crosshair marks the true camera center and a faint outline marks the unshaken frame, so the offset is visible as a gap. A HUD bar in one corner does not move (it models a `CanvasLayer`).
- **Right, "Trauma vs shake":** a scrolling time plot of the last 2 s. Line 1: trauma `T` (0 to 1). Line 2: shake `T^p` (0 to 1). Markers at each hit with the amount added. A horizontal dashed line at the shake level that equals 1 px of offset (`1 / (max_offset × user_scale)`) labelled "1 px".

**Controls.**
- Buttons: "Graze +0.2", "Big hit +0.6", "Custom +x" with a slider for x from 0.05 to 1.0. Keyboard shortcuts G, B, C.
- Exponent `p`: slider 1 to 3, step 0.5, default 2.
- Decay `d`: slider 0.2 to 2.0 per second, default 0.8.
- Max offset: slider 0 to 32 px, default 16.
- Shake scale (accessibility): slider 0% to 100%, default 100%.
- Motion: radio "Noise" (default) or "White random".
- Frame rate: radio 30, 60, 144 Hz. The simulation steps at this rate using a fixed `dt = 1 / fps` inside `requestAnimationFrame` (accumulator), independent of the real display.
- Toggle: "Decay per frame (bug)". When on, decay uses `d / 60` per simulated frame instead of `d × dt`.
- Reduced motion: when `prefers-reduced-motion` is set, the left view starts paused on a static frame showing the offset gap and the peak offset number, with a "Play shake" button; the right plot still updates.

**Readouts beside the plot (live text).** Current `T`, current shake `T^p`, current offset `dx, dy` in px, peak offset of the last hit in px, and "calm after" (seconds until `T = 0` from the last hit, computed as `T_after_hit / d`, or measured when the bug toggle is on).

**Formulas.**
- `T = min(T + amount, 1)` on a hit. Each simulated frame `T = max(T − d × dt, 0)` (or `T − d / 60` with the bug toggle).
- `shake = T^p`, `dx = max_offset × user_scale × shake × n(seed=1, t × 15)`, `dy` the same with seed 2.
- Noise `n`: 1D value noise with smoothstep, lattice values uniform in −1 to 1 from a seeded hash of the integer index, as in the lecture's `value_noise`. White random: a fresh uniform −1 to 1 value per simulated frame.

**Test values (p = 2, d = 0.8, max_offset 16, scale 100%).**
- One hit of 0.5: peak shake 0.25, peak offset bound 4.0 px, calm after 0.625 s (displayed as 0.63).
- Graze 0.2: shake 0.04, bound 0.64 px. Big hit 0.6: shake 0.36, bound 5.76 px. Two big hits in quick succession: T capped at 1.0, bound 16 px.
- p = 1, one hit of 0.5: bound 8.0 px.
- Bug toggle on, one hit of 0.5: calm after about 1.27 s at 30 Hz, 0.63 s at 60 Hz, 0.26 s at 144 Hz. Bug off: about 0.63 s at all three.
- Scale 0%: offset exactly 0 for any hit.

**Accessibility.** Every control keyboard-reachable with visible focus; all sliders labelled with their current value; the plot has a text summary updated after each hit ("Big hit: peak 5.8 px, calm in 0.75 s"). The page itself must not shake anything outside the left viewport.

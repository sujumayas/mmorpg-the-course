# AU101 · Week 06 — Middleware: FMOD and Wwise Events and Parameters

**Why this matters:** Last week every sound decision lived in game code, so changing how an engine sounds meant a programmer, a rebuild and a new test. Audio middleware moves those decisions into a tool the sound designer owns. The game sends two kinds of message, "this happened" and "this number changed", and the designer decides what that sounds like. Knowing where that line sits, and how a number becomes a sound, is most of what you need to work on a team that uses FMOD or Wwise.

**You will be able to:**
- Map the core concepts of FMOD Studio and Wwise (events, parameters or RTPCs, switches, states, banks, buses) onto each other and onto engine-only code.
- Build a parameter pipeline, from game value to normalized parameter to property curves, and compute the pitch and gain of each layer at any parameter value.
- Design an equal-power crossfade between loops and show by calculation why a linear crossfade dips by 3 dB.
- Write an event contract (names, parameters, ranges, owner, lifetime) that a programmer and a sound designer can both work from.

**Before class:** FMOD Studio User Manual (version 2.03), chapter 7 "Parameters", sections 7.1 and 7.2 (about 20 minutes), and the Modulator Reference entry "Seek Modulator". FMOD for Unity documentation (2.03), "Integration Tutorial", section 3.4 on the kart engine (skim; about 10 minutes). Optional: download the Celeste FMOD Studio project from FMOD's downloads page (free account; read the licence) and open the event named "!!!_README_FIRST".

**Prerequisites from earlier courses:** [MA101 week 8, lerp, inverse lerp and remap](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w08-interpolation-lerp-inverse-lerp-remap.md) (step 1 of the parameter pipeline is a clamped inverse lerp). [MA101 week 5, logarithms](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md) (decibels) and [MA101 week 10, sin and cos](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w10-angles-radians-sin-cos.md) (the equal-power curves). From this course, [week 4](w04-layering-and-variation.md) (variation and random modulators) and [week 5](w05-implementation-in-engine.md) (where triggers come from).

**Interactive:** [examples/w06-engine-rpm.html](../examples/w06-engine-rpm.html). Keep it open, with headphones, during section 2.

---

## 1. What middleware changes

Audio **middleware** is a separate tool plus a runtime library that your game links against. The two you'll meet most are FMOD (Firelight Technologies) and Wwise (Audiokinetic). FMOD Studio downloads with a free account, and Wwise is free for non-commercial use. Read each licence before you ship anything. Both integrate with Unity and Unreal, and Wwise also has an open-source integration for Godot.

The idea is a split of responsibility.

- **The programmer** decides *when* something happens and *what numbers* describe the game. "The kart's engine is running." "RPM is now 1,730." "The player walked onto grass." "The game is paused."
- **The sound designer** decides *what that sounds like*. Which files, how many layers, how pitch follows RPM, what grass sounds like, how the mix changes on pause.

The programmer's code never names a WAV file. It names an **event** and sets **parameters**. That's the whole interface.

### A shared vocabulary

The tools use different words for nearly the same ideas. This table is the translation you'll keep coming back to.

| Idea | FMOD Studio | Wwise | Engine only (Godot, Unity) |
|---|---|---|---|
| A named sound the game can request | Event; each playing copy is an event instance | Event, sent with `PostEvent` | A player node or source with a clip |
| A number from the game that shapes the sound | Continuous or discrete user parameter | RTPC (real-time parameter control), set with `SetRTPCValue` | Your own code changes pitch and volume |
| A choice among named options on one object | Labeled parameter | Switch, set per game object with `SetSwitch` | An `if` or a dictionary of clips |
| A game-wide mode | Global parameter, or a snapshot on the mixer | State, set game-wide with `SetState` | Global variables and bus settings |
| The files shipped to the game | Bank | SoundBank, loaded with `LoadBank` | Imported resources |
| A mixing channel | Bus (group bus, return bus) | Bus, auxiliary bus | Audio bus |

Two details are worth stressing. First, FMOD events are **instanced**. The manual's own example is a gunshot event, where every shot in the game creates a new instance, and each instance can have its own parameter values and its own random choices. Second, Wwise separates switches (per game object, so each character can stand on a different surface) from states (one value for the whole game, such as "underwater" or "paused"). You can see that split in the API. `SetSwitch` takes a game object and `SetState` does not.

### Buses and snapshots

Every event's output flows into a **bus**, and buses feed other buses until everything reaches the master bus. In FMOD a group bus makes a submix of whatever is routed into it and has its own effects, so a typical project routes weapons, footsteps and ambience into an "SFX" bus, and "SFX", "Music", "Dialogue" and "UI" into the master. One fader on "SFX" then moves every sound effect at once, and that fader is what the player's options menu controls.

A **snapshot** is a saved change to that mix which the game can start and stop like an event. The FMOD glossary describes it as an instanceable set of changes to the project mix. While it is active it overrides some mixer values, and when it stops the mix returns to what it would have been. "Paused" (music down, SFX muffled) and "Underwater" (a low-pass on everything) are typical snapshots. Wwise gets the same effect from states driving bus properties. Week 10 builds a full mix from buses, snapshots and ducking. This week you only need to know that the programmer starts and stops a snapshot by name, exactly like an event, and the designer decides what it does.

### What you get for the extra tool

- **Iteration without rebuilds.** Both tools can connect to the running game and apply changes live. FMOD calls this live update. The FMOD manual's Celeste appendix walks you through connecting FMOD Studio to a retail copy of Celeste and hearing your edits in the game as you play.
- **Behaviour the designer can see.** Curves, playlists and randomization are drawn in the tool, not buried in code.
- **Profiling.** The tool can record what played, when, and at what parameter values.

The cost is one more piece of software to license, learn, version and ship, and a boundary that both sides have to agree on. Section 4 turns that agreement into a document.

## 2. Worked example: an engine that shifts gears it doesn't have

### The hook

SuperTuxKart (the open-source kart racer, version 1.5, 2025) has no gearbox in its physics. Listen to a kart accelerate and you still hear gear changes. The engine note climbs, drops, climbs again, drops again, and climbs a third time. The source code explains it. The kart plays one looping engine sample and sets its pitch every frame from the kart's speed. The comment calls the result a "staired sawtooth" with three evenly spaced fake gears, and describes the sound as "brrrBRRRbrrrBRRR".

Here is the rule, where `f` is the kart's speed divided by its maximum speed, between 0 and 1 on the ground:

```
gears = 3 × (f mod 0.333334)
pitch = 0.6 + 0.35 × (0.9 × f + gears)
```

The `mod` makes `gears` climb from 0 to nearly 1 across each third of the speed range, then snap back to 0. That snap is the "gear change". The `0.9 × f` term makes each gear start a little higher than the last.

Every piece of that rule is a sound design decision, and it lives in C++. To try a fourth gear or a softer shift, someone edits `kart.cpp` and rebuilds the game. Middleware exists so that a sound designer can make that change by dragging a curve. The rest of this example builds the general form of what SuperTuxKart hard-coded.

### The model: the parameter pipeline

Every parameter-driven sound, in any tool, follows the same three steps.

```
1. p = clamp((x − x_min) / (x_max − x_min), 0, 1)      game value → parameter
2. y_k = f_k(p)                                         one curve per property
3. apply y_k to property k (pitch, volume, filter, layer gain, ...)
```

- `x` is a game value in its own units (speed in m/s, RPM, health, distance).
- `x_min` and `x_max` are the range the designer cares about. Step 1 is MA101 week 8's clamped inverse lerp. Some tools skip the normalization and let the parameter keep game units (an "RPM" parameter from 500 to 2,000), which is the same thing with a different axis label.
- `f_k` is a **curve** that maps the parameter to one property. FMOD calls these automation curves, and the manual describes them as a line graph giving the property's value for every value of the parameter. In Wwise the same idea is an RTPC curve.

SuperTuxKart's code is steps 1 to 3 with one curve (`f = speed / max_speed`, then the sawtooth into pitch).

A richer engine uses several loops, each recorded at a steady RPM, and crossfades between them. That needs two curves per loop, one for pitch and one for gain. For loops recorded at `r_1 < r_2 < ...` and a current RPM between neighbours `r_a` and `r_b`:

```
pitch_i = rpm / r_i                        each loop is sped up or slowed to match
t       = (rpm − r_a) / (r_b − r_a)        how far between the two loops
gain_a  = cos(t × 90°)                     equal-power crossfade
gain_b  = sin(t × 90°)
```

Why cosine and sine? The two loops are different recordings, so their waveforms are unrelated. As you saw in week 4, unrelated signals add their **power** (amplitude squared), not their amplitude. The loudness of the mix follows `gain_a² + gain_b²`, and `cos² + sin² = 1` at every `t`. The loudness stays constant through the whole fade.

The obvious alternative is a **linear crossfade**, `gain_a = 1 − t` and `gain_b = t`. The gains always add to 1, so it *looks* balanced on the curve editor. But the power is `(1 − t)² + t²`, which is only 0.5 at the midpoint, a drop of `10 × log10(0.5) = −3.0 dB`. Linear crossfades between different recordings leave a hole in the middle. You'll meet the same quarter-circle curve twice more in this course. Week 7 uses it to pan a sound between two speakers, and week 8 uses it to swap one music stem for another.

### Numbers you can check

First, SuperTuxKart's pitch at a few speeds:

| Speed fraction `f` | `gears` | Pitch multiplier | What you hear |
|---|---|---|---|
| 0 | 0 | 0.600 | Idle |
| 0.30 | 0.900 | 1.010 | Near the top of gear 1 |
| 0.3333 | 0.9999 | 1.055 | Top of gear 1 |
| 0.334 | 0.002 | 0.706 | Gear 2 starts, a drop of about 7 semitones |
| 0.6666 | 0.9998 | 1.160 | Top of gear 2 |
| 0.667 | 0.001 | 0.810 | Gear 3 starts, a drop of about 6.2 semitones |
| 1.0 | 1.000 | 1.265 | Top speed |

Check one yourself: at the shift from gear 1 to gear 2 the ratio is `1.055 / 0.706 = 1.494`, and `12 × log2(1.494) ≈ 6.95` semitones. The oddly precise `0.333334` is slightly more than a third, so at `f = 1` the sawtooth hasn't wrapped yet and top speed is the highest pitch.

Next, a three-loop engine with loops recorded at 1,000, 2,000 and 4,000 RPM:

| RPM | Lower loop: gain, pitch | Upper loop: gain, pitch | Linear fade: total level | Equal-power: total level |
|---|---|---|---|---|
| 1,000 | 1.000, +0.0 st | 0.000, −12.0 st | 0.00 dB | 0.00 dB |
| 1,250 | 0.924, +3.9 st | 0.383, −8.1 st | −2.04 dB | 0.00 dB |
| 1,500 | 0.707, +7.0 st | 0.707, −5.0 st | −3.01 dB | 0.00 dB |
| 1,750 | 0.383, +9.7 st | 0.924, −2.3 st | −2.04 dB | 0.00 dB |
| 2,000 | 0.000, +12.0 st | 1.000, +0.0 st | 0.00 dB | 0.00 dB |
| 3,000 | 0.707 (2,000 loop), +7.0 st | 0.707 (4,000 loop), −5.0 st | −3.01 dB | 0.00 dB |

The gains shown are the equal-power ones. The linear column uses `1 − t` and `t`.

Read the pitch columns too. At 1,500 RPM the lower loop is being played 7 semitones fast. Pitch-shifting a recording that far makes it sound smaller and buzzier, because the whole spectrum moves, including resonances of the engine body that should stay put. Loops an octave apart are too far apart for a realistic engine. Section 2's design judgment comes back to this.

### Code you can run

```python
import math

def stk_pitch(f):
    """SuperTuxKart's engine pitch for f = speed / max_speed (0 to 1, on the ground)."""
    gears = 3 * math.fmod(f, 0.333334)
    return 0.6 + (0.9 * f + gears) * 0.35

LOOPS = [1000, 2000, 4000]           # RPM each engine loop was recorded at

def engine_mix(rpm, equal_power=True):
    """Gain and pitch (semitones) for the two loops that bracket rpm."""
    for a, b in zip(LOOPS, LOOPS[1:]):
        if a <= rpm <= b:
            break
    t = (rpm - a) / (b - a)
    if equal_power:
        ga, gb = math.cos(t * math.pi / 2), math.sin(t * math.pi / 2)
    else:
        ga, gb = 1 - t, t
    power_db = 10 * math.log10(ga ** 2 + gb ** 2)
    return (a, ga, 12 * math.log2(rpm / a)), (b, gb, 12 * math.log2(rpm / b)), power_db

for f in (0.0, 0.3, 0.3333, 0.334, 0.6666, 0.667, 1.0):
    print(f"STK f={f:<6} pitch x{stk_pitch(f):.3f}")
for rpm in (1000, 1250, 1500, 1750, 2000, 3000):
    lo, hi, lin = engine_mix(rpm, equal_power=False)
    lo, hi, eq = engine_mix(rpm)
    print(f"{rpm} rpm: loop {lo[0]} gain {lo[1]:.3f} ({lo[2]:+.1f} st), "
          f"loop {hi[0]} gain {hi[1]:.3f} ({hi[2]:+.1f} st), "
          f"sum linear {lin:+.2f} dB, equal-power {eq:+.2f} dB")
```

Output:

```
STK f=0.0    pitch x0.600
STK f=0.3    pitch x1.010
STK f=0.3333 pitch x1.055
STK f=0.334  pitch x0.706
STK f=0.6666 pitch x1.160
STK f=0.667  pitch x0.810
STK f=1.0    pitch x1.265
1000 rpm: loop 1000 gain 1.000 (+0.0 st), loop 2000 gain 0.000 (-12.0 st), sum linear +0.00 dB, equal-power +0.00 dB
1250 rpm: loop 1000 gain 0.924 (+3.9 st), loop 2000 gain 0.383 (-8.1 st), sum linear -2.04 dB, equal-power +0.00 dB
1500 rpm: loop 1000 gain 0.707 (+7.0 st), loop 2000 gain 0.707 (-5.0 st), sum linear -3.01 dB, equal-power +0.00 dB
1750 rpm: loop 1000 gain 0.383 (+9.7 st), loop 2000 gain 0.924 (-2.3 st), sum linear -2.04 dB, equal-power +0.00 dB
2000 rpm: loop 1000 gain 0.000 (+12.0 st), loop 2000 gain 1.000 (+0.0 st), sum linear +0.00 dB, equal-power +0.00 dB
3000 rpm: loop 2000 gain 0.707 (+7.0 st), loop 4000 gain 0.707 (-5.0 st), sum linear -3.01 dB, equal-power +0.00 dB
```

### A visual you can move

Open [`examples/w06-engine-rpm.html`](../examples/w06-engine-rpm.html). Drag the RPM slider and a procedurally generated engine plays. The left view is the designer's curve editor: one gain curve per loop across the RPM range, with the current RPM as a vertical line. The right view shows what the listener gets: total loudness in dB across the whole range, and each loop's pitch shift in semitones.

In "Linear" mode, the left view looks tidy, straight lines that always add up to 1. The right view shows the truth, a 3 dB dip halfway between every pair of loops, and you can hear the engine thin out as you sweep through. Switch to "Equal power" and the loudness line goes flat. Then press "Add loop at 3,000" and "Add loop at 1,414" and watch the worst pitch shift fall. Finally, switch the source to "SuperTuxKart rule" and drive the slider as speed. The one loop's pitch traces the staired sawtooth, and you hear three gear changes that the physics never had.

### Cross-game recognition

**SuperTuxKart (1.5).** Our pipeline, written in C++. Step 1 is `f = speed / max_speed`. Step 2 is the sawtooth curve. Step 3 sends the result to OpenAL as the source's pitch. The wrapper clamps pitch to between 0.5 and 2.0, noting that OpenAL only accepts that range. That clamp is an extra curve, a flat floor and ceiling, applied after the designer's curve. One loop, one parameter, one curve, all owned by a programmer.

**FMOD for Unity, kart tutorial (2.03).** FMOD's own Unity integration tutorial builds the middleware version of the same idea, and it uses Unity's Karting Microgame. The engine is an event from the FMOD examples project called "Vehicles/Ride-on Mower", with a parameter named RPM. The tutorial's script does step 1 in C#, computing `Mathf.Lerp(minRPM, maxRPM, kartSpeed)` and sending it with `SetParameter("RPM", ...)`, and then tells you to set the range to 500 to 2,000 RPM to match the event. Everything after that number, which loops play, how they crossfade and how pitch follows, lives in the FMOD project, where a sound designer can change it without touching the script. In our model, the programmer owns step 1 and the designer owns steps 2 and 3.

**Wwise (2026.1).** The call has the same shape: `SetRTPCValue("RPM", value, gameObject)`. The curve that maps that RTPC onto a property is drawn in the Wwise authoring tool. The open-source Wwise integration for Godot wraps exactly these calls (`SetRTPCValue`, `SetSwitch`, `SetState`, `PostEvent`, `LoadBank`), which shows how thin the programmer's side of the boundary is.

**FMOD seek modulator (2.03).** Not a game, but the same pipeline with one more stage. A seek modulator makes a property ramp toward a new value at a fixed rate instead of jumping. The manual's example is a speed of "0.1 range/s" on a pitch range of −24 to 24 semitones, which gives `0.1 × 48 = 4.8` semitones per second. That's a rate limit inserted between step 2 and step 3. Section 3 does the arithmetic for our engine.

### Design judgment

- **Who owns each step?** Give step 1 to the programmer and steps 2 and 3 to the designer. If the programmer normalizes speed to 0 to 1, the designer can reuse the same event on a slow tractor and a fast kart by changing one number in code. If the parameter carries real units (RPM), the designer can reason about recordings directly. Decide once per project and write it in the contract.
- **Crossfade in the right space.** A linear `t` puts the "halfway" point at 1,500 RPM between 1,000 and 2,000, where the lower loop is shifted +7.0 semitones and the upper −5.0. Using `t = log(rpm / r_a) / log(r_b / r_a)` puts halfway at the geometric mean, about 1,414 RPM, where both loops are shifted by exactly 6 semitones in opposite directions. Pitch is heard on a log scale, so a log-spaced crossfade spreads the damage evenly.
- **More loops or more stretch?** Every extra loop is more recording time and memory (week 14). Every missing loop means more pitch shifting, which smears the character of the engine. A practical rule is to keep every *audible* loop within about ±5 semitones of its recorded pitch. With loops an octave apart, that is impossible, which is why realistic engines use many loops or other techniques (granular synthesis, which is beyond this course).
- **Equal power is for unrelated sounds.** If two layers are the *same* recording, aligned, their amplitudes add, and equal-power gains give a +3 dB bump in the middle instead of a flat line. Use linear fades between identical, aligned material, such as two versions of one music stem, and equal-power fades between different recordings. Week 8 applies this to music.
- **Stylized can beat accurate.** SuperTuxKart's single loop is not realistic, and it doesn't try to be. Three fake gears make acceleration readable and fun in a cartoon racer. The pipeline doesn't decide your style. It lets you change style without a programmer.

## 3. Smoothing parameters: seek speed

Game values can jump. A kart hits a wall and its speed goes from full to zero in one frame. If RPM follows instantly, the engine pitch drops an octave in 16 ms, which sounds like a glitch. Worse, some properties produce clicks when they change abruptly, such as a volume that steps from full to silent within one sample.

The fix is to limit how fast the parameter may move. FMOD's seek modulator ramps a property toward its new value at a fixed rate, expressed as a fraction of the property's range per second. FMOD parameters also have a separate **velocity** setting that keeps a parameter ramping on its own at a fixed number of units per second, even when the game doesn't set it. If both apply, the manual says the parameter first seeks to the new value and then resumes its velocity.

The arithmetic is short. Suppose the RPM parameter runs from 1,000 to 4,000, a range of 3,000, and the seek speed is 0.5 range/s.

```
rate = 0.5 × 3,000 = 1,500 RPM per second
time to fall from 3,500 to 2,000 = 1,500 / 1,500 = 1.0 s
```

That's a smooth, believable spin-down. But the same smoothing adds lag. If the player floors the accelerator, the sound trails the physics by up to a second. A common compromise is an asymmetric seek. FMOD's seek modulator can set separate ascending and descending speeds, fast going up (the player caused it, and should hear it now) and slower going down (engines spin down gradually).

There's a second reason to smooth. When the game sets a parameter only once per frame, each change is a small step. For pitch that's harmless. For volume, filter cutoff or pan, a large step at a low frame rate can produce **zipper noise**, a faint buzz at the frame rate. Seek speed turns steps into ramps and removes it.

## 4. The event contract

Middleware moves decisions to the designer, but it does not remove the need to agree. The programmer and the designer share a list of names and numbers, and if either side changes it alone, the game breaks quietly. The sound just doesn't play, or plays at the wrong pitch. Write the agreement down. A minimal **event contract** has one row per event:

| Field | Example | Why it matters |
|---|---|---|
| Event path | `event:/Vehicles/Kart Engine` | Code refers to this string; renaming breaks the build silently |
| Type | Persistent loop, owned by the kart | Tells the programmer to keep a handle and stop it |
| Parameters | `RPM`, continuous, 1,000-4,000, set every frame | Range and units prevent "why is it silent at 5,000?" |
| Labels | `Surface`: Asphalt, Dirt, Grass (labeled) | Code must send exactly these strings |
| Global state | `Paused` (global parameter or snapshot) | Mix changes that aren't tied to one object |
| Bank | `Vehicles` | Must be loaded before the event plays |
| Owner | Sound design: curves and content; Gameplay: RPM value | Who fixes what |

Two lifetime rules cover most bugs. A **one-shot event** is started and released straight away, and it frees itself when it finishes. A **persistent event** (an engine, a burning loop) is created once, stored, updated, and explicitly stopped and released. That's week 5's stuck-loop problem again, now with an event instance instead of a player node.

Banks add one more rule. An event's content must be in a loaded bank before the event plays, and a bank that is never unloaded stays in memory. Group banks by when they're needed (per level, per vehicle, "always loaded" for UI) and write that grouping into the contract. FMOD's master bank, which holds the mixer, buses and routing, has to stay loaded the whole time, so the manual advises against putting events in it except in very small projects. Week 14 turns bank grouping into a memory budget.

## In-class activity (25 minutes)

In pairs, write the event contract for a **spell** in a small action RPG. The spell charges while a button is held (up to 2 seconds), then releases, and its sound should change with charge and with the element (fire, ice, lightning).

1. List the events you need. Decide which are one-shots and which are persistent.
2. Define every parameter: name, type (continuous, discrete, labeled), range, units, who sets it, and how often.
3. For the charge loop, sketch two curves on paper: pitch versus charge and volume versus charge. Mark the values at 0%, 50% and 100%.
4. Choose a seek speed for charge in range/s so that releasing early drops the charge sound to silence in 0.25 s. Show the calculation.
5. Swap with another pair. Find one case their contract doesn't cover (for example, the player is stunned mid-charge).

Expected output: a contract table in the section 4 format, two curve sketches with marked values, and the seek calculation.

## Common misconceptions

- **"Middleware plays the sound, so the programmer's job is done."** The programmer still owns when events start and stop, the values sent, instance lifetimes and bank loading. Most middleware bugs are on the code side of the contract.
- **"A linear crossfade keeps the level steady because the gains add to 1."** Only for identical, aligned material. For different recordings it dips 3 dB at the midpoint. Check the power, not the gains.
- **"Switches and states are the same thing."** In Wwise a switch is set per game object and a state is game-wide. Using a state for footstep surface would make every character in the game sound like they're on the same ground.
- **"Smoothing a parameter is free."** A seek speed adds lag equal to the distance to travel divided by the rate. Asymmetric seeks keep the player's own actions responsive.

## Check yourself

1. Using SuperTuxKart's rule, compute the pitch at `f = 0.5` and `f = 0.9`. How many semitones apart are they?
2. Loops are recorded at 1,500 and 3,000 RPM. At 2,000 RPM, compute `t`, both equal-power gains, both pitch shifts in semitones, and the total level with a linear fade.
3. With a log-spaced crossfade between those same loops, at what RPM are the two gains equal, and what is each loop's pitch shift there?
4. An FMOD pitch property runs from −24 to +24 semitones with a seek modulator at 0.25 range/s. A game value jumps so that the target pitch rises by 6 semitones. How long does the property take to get there?
5. A programmer renames the event `event:/Vehicles/Kart Engine` to `event:/Vehicles/KartEngine` in code only. What does the player hear, and which part of the contract would have prevented it?

<details>
<summary>Answers</summary>

1. `f = 0.5`: `gears = 3 × (0.5 − 0.333334) ≈ 0.5`, pitch `0.6 + 0.35 × (0.45 + 0.5) ≈ 0.9325`. `f = 0.9`: `gears = 3 × (0.9 − 0.666668) ≈ 0.7`, pitch `0.6 + 0.35 × (0.81 + 0.7) ≈ 1.1285`. The ratio is about 1.210, so `12 × log2(1.210) ≈ 3.3` semitones.
2. `t = (2,000 − 1,500) / 1,500 = 0.333`. Gains `cos(30°) = 0.866` and `sin(30°) = 0.5`. Pitch shifts `12 × log2(2,000/1,500) = +4.98` and `12 × log2(2,000/3,000) = −7.02` semitones. Linear fade: `(0.667)² + (0.333)² = 0.556`, which is `−2.55 dB`.
3. Equal gains at `t = 0.5`, which in log space is the geometric mean `√(1,500 × 3,000) ≈ 2,121` RPM. Each loop is shifted by 6 semitones, +6 for the lower and −6 for the upper.
4. Rate `0.25 × 48 = 12` semitones per second, so 6 semitones take 0.5 s.
5. Nothing. The event lookup fails, so no engine sound plays, and depending on the integration there may be only a log warning. A contract with the exact event path, checked in both places (or generated from the FMOD project), would catch it.

</details>

## Lab / assignment hook

[Lab 06, an engine event and its contract](../labs/lab06.md). You'll generate engine loops procedurally, build a parameter-driven engine event in FMOD Studio, and write its event contract as a JSON file that a provided validator checks for crossfade level and pitch stretch. The same event plugs into your week 5 scene. This event also starts your practice for the **adaptive music** assignment (30%), which uses the same parameters and crossfades on music stems in weeks 8 and 9.

## Sources

- SuperTuxKart source code, `src/karts/kart.cpp` (`Kart::updateEngineSFX`) and `src/audio/sfx_openal.cpp` (`SFXOpenAL::reallySetSpeed`), release 1.5 (October 2025), GitHub `supertuxkart/stk-code`. Engine pitch `0.6 + (0.9 f + 3 × fmod(f, 0.333334)) × 0.35`, the "staired sawtooth" comment with three fake gears, and the pitch clamp to 0.5-2.0 for OpenAL.
- Firelight Technologies, FMOD Studio User Manual 2.03 (2.03.14, May 2026). Chapter 2 "FMOD Studio Concepts" (instanced events, the gunshot example), chapter 7 "Parameters" (automation curves, continuous, discrete and labeled user parameters, global parameters), "Parameters Reference" (velocity), chapter 22 "Modulator Reference" (seek modulator, the 0.1 range/s example on −24 to 24 semitones giving 4.8 semitones per second, checked 29 September 2026), and "Appendix: Celeste Getting Started Guide" (the public Celeste FMOD project by Power Up Audio and Lena Raine, notes by Kevin Regamey, live update, educational licence).
- Firelight Technologies, FMOD Studio User Manual 2.03, Glossary: "Group Bus" (submix with its own signal chain), "Snapshot" (instanceable changes to the project mix, reverting when stopped) and "Master Bank" (holds the mixer, buses and routing; must stay loaded).
- Firelight Technologies, FMOD for Unity 2.03, "Integration Tutorial", section on the kart engine. "Vehicles/Ride-on Mower" event from the examples project, the RPM parameter, `Mathf.Lerp(minRPM, maxRPM, kartSpeed)` and `SetParameter("RPM", ...)`, the 500-2,000 range.
- Fama, A., Wwise Integration for the Godot Engine, `wwise_gdextension.cpp` (release "Wwise 2026.1.3 for Godot", September 2026, GitHub `alessandrofama/wwise-godot-integration`). Wwise SDK calls `AK::SoundEngine::PostEvent`, `SetRTPCValue` (with a game object), `SetSwitch` (with a game object), `SetState` (without one) and `LoadBank`.

## Interactive spec: examples/w06-engine-rpm.html

**The one insight:** a linear crossfade looks balanced on the curve editor (gains add to 1) but leaves a 3 dB hole in the loudness between every pair of loops; an equal-power crossfade is flat. A second insight: the fewer loops you have, the further each audible loop is pitch-shifted, and SuperTuxKart's single loop with a sawtooth curve shows a stylized alternative.

**Layout.** Two linked views and a control panel. Mobile: stacked (curve editor, listener view, controls, readouts). From 900 px: the two views side by side above the controls.

- **Left view, "Curve editor":** x axis RPM from 800 to 4,200 (log scale toggle, default linear); y axis gain 0 to 1. One curve per loop, each in its own colour from the program palette, with a legend listing its recorded RPM. A vertical line at the current RPM with dots where it crosses each curve. In "SuperTuxKart rule" mode this view instead plots pitch multiplier (y from 0.5 to 1.4) against speed fraction `f` (0 to 1).
- **Right view, "What you hear":** two stacked mini-plots sharing the RPM axis. Top: total level `10 × log10(Σ gain_i²)` in dB, y from −6 to +3 dB, with a dashed line at 0 dB. Bottom: pitch shift in semitones `12 × log2(rpm / r_i)` for every loop whose gain is at least 0.1 (−20 dB), y from −12 to +12, with dashed guide lines at ±5 semitones labelled "stretch limit".

**Sound generation (Web Audio API, procedural).** Each loop is a stationary "engine" tone built at its recorded RPM `r`: the firing frequency `F = r / 60 × 2` Hz (a four-cylinder four-stroke fires twice per revolution); sum of harmonics 1 to 12 of `F` with amplitudes `1 / k` and fixed random phases (seeded), multiplied by a slow 3 Hz amplitude wobble of depth 0.1, through a low-pass at 2,500 Hz, plus band-passed noise (centre `8 × F`, Q 1) at −18 dB. Render each loop into a 2 s `AudioBuffer` whose length is a whole number of cycles of `F` so it loops cleanly. Play each with `loop = true`, `playbackRate = rpm / r`, into its own `GainNode` set to the curve's gain, then a master gain and a compressor (threshold −3 dB) before the destination. Parameter changes use `setTargetAtTime` with a 20 ms time constant to avoid zipper noise (or the seek speed control when enabled). Audio starts only after the user presses "Start engine".

**Controls.**
- RPM: slider 1,000 to 4,000, step 10, default 1,500; arrow keys move by 10, Page Up/Down by 250.
- Crossfade: radio "Linear" (default) or "Equal power".
- Crossfade spacing: radio "Linear in RPM" (default) or "Log (pitch) spaced", which uses `t = ln(rpm / r_a) / ln(r_b / r_a)`.
- Loops: checkboxes for loops at 1,000, 1,414, 2,000, 3,000 and 4,000 RPM; defaults 1,000, 2,000, 4,000 checked. Minimum two loops.
- Seek speed: slider "Instant" or 0.05 to 2 range/s (range = 3,000 RPM), default Instant; when set, the heard RPM ramps toward the slider value at `speed × 3,000` RPM per second and the vertical line shows both target (hollow) and current (filled).
- Source: radio "Multi-loop event" (default) or "SuperTuxKart rule". In the SuperTuxKart mode, the slider becomes speed fraction `f` from 0 to 1 (step 0.001), one loop recorded at 1,000 RPM plays at `playbackRate = 0.6 + 0.35 × (0.9 f + 3 × (f mod 0.333334))`, clamped to 0.5-2.0.
- Button "Sweep" (key W): moves RPM (or `f`) from minimum to maximum over 6 s and back, so students can hear the dips.

**Readouts (live text).** For each audible loop: recorded RPM, gain (3 decimals), gain in dB (1 decimal), pitch shift in semitones (1 decimal). Total level in dB (2 decimals). Worst pitch shift among audible loops. In SuperTuxKart mode: `f`, `gears`, pitch multiplier (3 decimals), and semitones relative to 1.0.

**Test values (loops 1,000, 2,000, 4,000; linear spacing).**
- 1,500 RPM, Linear: gains 0.500 / 0.500, total −3.01 dB; pitch +7.0 / −5.0 st.
- 1,500 RPM, Equal power: gains 0.707 / 0.707, total 0.00 dB.
- 1,250 RPM, Linear: total −2.04 dB. Equal power: gains 0.924 / 0.383.
- 3,000 RPM, Equal power: loops 2,000 and 4,000 at 0.707 each; pitch +7.0 / −5.0 st.
- Log spacing, 1,414 RPM: equal gains; pitch +6.0 / −6.0 st.
- Adding the 3,000 loop: at 2,500 RPM (linear spacing) the bracketing loops are 2,000 and 3,000, `t = 0.5`, pitch +3.9 / −3.2 st.
- SuperTuxKart: `f = 0` gives 0.600; `f = 0.3333` gives 1.055; `f = 0.334` gives 0.706; `f = 0.5` gives 0.932 (exactly 0.93249993, because `0.333334` is slightly more than a third); `f = 1` gives 1.265.
- Seek 0.5 range/s: moving the slider from 3,500 to 2,000 takes 1.0 s for the current value to arrive.

**Accessibility.** All controls keyboard reachable with visible focus and labelled values. A text summary under the right view updates on change ("1,500 RPM: two loops at 0.707, total 0.0 dB, worst stretch +7.0 st"). Volume slider (default 50%) and mute toggle; "Stop engine" button always visible while sound plays. Respect `prefers-color-scheme`; with `prefers-reduced-motion`, "Sweep" steps in five jumps instead of animating. No logos or game art; the SuperTuxKart mode is described in text only.

# AU101 · Week 07 — Spatial Audio and Attenuation

**Why this matters:** Every 3D sound in your game carries two pieces of information the player uses without thinking: how far away it is and which side it is on. Both come from a few lines of math that the engine runs for you, with defaults someone else chose. If you leave those defaults alone, enemy footsteps vanish at the wrong range, a campfire across the map keeps eating a voice, and players in a shooter argue about whether they "should have heard that."

**You will be able to:**
- Compute gain and level in dB at any distance for the inverse, linear and tapered attenuation curves, and find where each crosses a threshold.
- Rewrite the attenuation settings of Web Audio, FMOD, Unity and Godot into one common form and predict where each goes silent.
- Compute equal-power stereo pan gains from a listener position, a facing and a source position.
- Design an attenuation table for a game's sound list and defend each curve and range as a gameplay decision.

**Before class:** Collins, *Game Sound* (2008), chapter 7, "Gameplay, genre and the functions of game audio." Skim sections 6.3 and 6.4 ("Panning Algorithm" and "Distance Effects") of the W3C Web Audio API specification. You will not need to memorize them, but you will see the formulas from this lecture written as a standard.

**Prerequisites from earlier courses:** [MA101 week 5, logarithms](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md) (decibels, `dB = 20 · log10(amplitude ratio)`). [MA101 week 14, distances](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w14-distances-ranges-and-squared-distance.md) (distance between two points, range checks). [MA101 week 13, the dot product](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w13-dot-product-facing-and-vision-cones.md) (left or right of a facing). [AU101 week 1](w01-what-sound-does-feedback-space-emotion.md) (interaural time and level differences and the front-back confusion; this lecture builds on them and does not repeat them). [AU101 week 5, implementation in engine](w05-implementation-in-engine.md) (players, clips and the listener). [AU101 week 6, middleware events and parameters](w06-middleware-events-and-parameters.md).

**Interactive:** [examples/w07-attenuation-curves.html](../examples/w07-attenuation-curves.html). Keep it open during section 2.

---

## 1. Three questions the ear asks

When a sound plays in a 3D game, the engine answers three questions for it every frame.

1. **How far?** The engine turns the distance between the sound and the listener into a gain. Gain is an amplitude multiplier: 1 leaves the sound as authored, 0.5 is about −6 dB, 0 is silence. The function that maps distance to gain is the **attenuation curve** (FMOD and Unity call it rolloff).
2. **Which way?** The engine turns the direction of the sound into a pair of speaker gains. This is **panning**.
3. **Through what?** The engine may filter the sound to suggest walls, air, or a big room. This covers **occlusion** (a wall between you and the sound), air absorption and reverb.

Two words need pinning down first. The **emitter** (or source) is the point the sound comes from. The **listener** is the point that hears. It is usually attached to the camera or to the player character. Section 5 shows why that choice is a design decision.

This week covers the first two questions in depth and the third briefly. Week 1 explained what the ear does with timing and level differences between the two ears. This week is about the numbers you choose.

## 2. Worked example: where does a sound go silent?

### The hook

In Minecraft (Java Edition), a sound played at the default volume can be heard within a 16-block radius, and there is a gradual falloff to silence inside that sphere. Players learn this without reading anything. A mob a short walk away is faint, and past a certain point you hear nothing at all. The `/playsound` command has a surprise in it. Raise the volume above 1 and the sound does not get louder. Instead, the 16-block radius is multiplied by the volume, so volume 2 reaches 32 blocks.

Now compare real air. A small sound source outdoors obeys the inverse square law: intensity falls with the square of distance, so every doubling of distance costs about 6 dB. It never reaches zero. A gunshot at 1 km is quiet, not absent.

So Minecraft draws a hard edge that physics does not have, and it treats "volume" as a range knob. Is that a hack, or a choice? To answer, you need the curves.

### The model

An attenuation curve is a gain function `g(d)` of the distance `d` between emitter and listener. The level in decibels is

```
L(d) = 20 · log10(g(d))      (0 dB means "as authored")
```

Every engine curve you will meet is built from two shapes, each with a **reference distance** `r` (inside it, the sound plays at full gain) and, for the second, a **maximum distance** `R`:

```
inverse:  g(d) = r / max(d, r)
linear:   g(d) = 1 − (clamp(d, r, R) − r) / (R − r)
```

- `d` is the distance, in metres or any world unit.
- `r` is the reference distance (called min distance in FMOD and Unity, ref distance in Web Audio, unit size in Godot).
- `R` is the maximum distance, where the linear curve reaches 0.
- `clamp(d, r, R)` pins `d` between `r` and `R`.

Put the inverse curve into decibels and it becomes a straight line against the logarithm of distance:

```
L(d) = −20 · log10(d / r)      for d ≥ r
```

Each doubling of `d` subtracts `20 · log10(2) ≈ 6.02 dB`, whatever the starting distance. That is the inverse square law, expressed in amplitude. The linear curve has no such rule. It removes equal slices of amplitude per metre, which in decibels means almost nothing at first and everything at the end.

### Numbers you can check

Take `r = 1 m` and, for the linear curve, `R = 32 m`. This short program prints both curves. It runs as shown with `.venv/bin/python`.

```python
import math

def db(g):
    return 20 * math.log10(g) if g > 0 else float("-inf")

def inverse(d, ref=1.0):
    return ref / max(d, ref)

def linear(d, ref=1.0, max_d=32.0):
    d = min(max(d, ref), max_d)
    return 1 - (d - ref) / (max_d - ref)

for d in (1, 2, 4, 8, 16, 24, 32):
    gi, gl = inverse(d), linear(d)
    print(f"{d:>3} m  inverse {gi:.3f} ({db(gi):6.1f} dB)   linear {gl:.3f} ({db(gl):6.1f} dB)")
```

It prints:

```
  1 m  inverse 1.000 (   0.0 dB)   linear 1.000 (   0.0 dB)
  2 m  inverse 0.500 (  -6.0 dB)   linear 0.968 (  -0.3 dB)
  4 m  inverse 0.250 ( -12.0 dB)   linear 0.903 (  -0.9 dB)
  8 m  inverse 0.125 ( -18.1 dB)   linear 0.774 (  -2.2 dB)
 16 m  inverse 0.062 ( -24.1 dB)   linear 0.516 (  -5.7 dB)
 24 m  inverse 0.042 ( -27.6 dB)   linear 0.258 ( -11.8 dB)
 32 m  inverse 0.031 ( -30.1 dB)   linear 0.000 (  -inf dB)
```

(The 16 m inverse gain is exactly 1/16 = 0.0625; the program rounds it to 0.062.)

Check two rows by hand. At 8 m the inverse gain is 1/8, and `20 · log10(0.125) = −18.06 dB`, three doublings of −6.02. At 16 m the linear gain is `1 − 15/31 = 0.516`, and `20 · log10(0.516) = −5.7 dB`.

Read the table as a player would. With the inverse curve, the sound is 12 dB down by 4 m and then drifts slowly: going from 16 m to 32 m costs the same 6 dB as going from 1 m to 2 m. With the linear curve, half the distance to the edge costs less than 6 dB, and the sound is still clearly audible at 24 m. Then it drops 12 dB and more over the last few metres and disappears.

### The visual

Open the interactive. The left plot shows gain against distance on ordinary axes. On that plot the linear curve looks gentle and fair, a straight ramp, and the inverse curve looks brutal, collapsing in the first few metres. The right plot shows the same curves in decibels, with distance on a log scale. Now the inverse curve is the calm one, a straight line falling 6 dB per doubling, and the linear curve is the cliff at the end.

Drag the emitter on the top-down map and listen. With the inverse curve you hear a smooth, steady fade and you can judge distance all the way out. With the linear curve the sound barely changes for most of the walk, then collapses over the last few metres. Your ear works in something close to decibels, which is why the right plot predicts what you hear and the left one does not.

### Cross-game recognition

Engines expose these two shapes under different names. Rewrite each into the form above.

**Web Audio API (W3C specification, 2026 editor's draft).** The `PannerNode` has three distance models. Its `"inverse"` model is `ref / (ref + f · (max(d, ref) − ref))`, where `f` is the rolloff factor. With `f = 1` that simplifies to `ref / max(d, ref)`, our inverse curve. The `"linear"` model is `1 − f · (clamp(d, ref, max) − ref) / (max − ref)`, our linear curve with `f = 1`. The defaults are the inverse model, `refDistance = 1`, `maxDistance = 10000` and `rolloffFactor = 1`. So an untouched Web Audio source follows the physical curve and never goes silent in any space you are likely to build.

**FMOD Engine (Core API 2.03).** The default rolloff is inverse. Its documentation describes it as unattenuated below the min distance and then attenuating with min distance divided by distance, until the max distance, where it stops attenuating. Read that last clause carefully. Past the max distance the sound holds its level rather than going silent. FMOD also offers linear and linear-squared rolloffs, which reach silence at the max distance, and an inverse tapered mode. That mode follows the inverse curve close in and switches to the linear-squared curve when that one is quieter, so it behaves realistically near the source and still reaches silence at the max distance.

**Unity (Unity 6.6).** An `AudioSource` has Logarithmic, Linear and Custom rolloff modes. The scripting reference says that in Logarithmic mode the source ignores the max distance setting and the sound keeps attenuating indefinitely. In Linear mode the max distance is where the volume reaches zero. Unity's "logarithmic" is our inverse curve. It is named after what it looks like on the decibel plot.

**Godot (master branch, 4.8 in development, September 2026).** `AudioStreamPlayer3D` defaults to the inverse-distance model, computed as `1 / (d / unit_size)` with `unit_size = 10` by default. That is our inverse curve with `r = 10`, except that Godot does not clamp at `r`. It caps the result with `max_db`, which defaults to +3 dB. If you set `max_distance`, Godot multiplies the gain by `1 − d / max_distance`, a linear taper to silence. Godot's docs note this also lets the engine skip mixing far-away players, which saves CPU.

**Minecraft (Java Edition, September 2026).** The wiki documents a 16-block audible radius at volume 1, multiplied by volume above 1, with a falloff to silence inside. Whatever the exact shape inside, this is a curve with a guaranteed `R`, and the "volume" parameter above 1 scales `R`, not the gain.

Four engines and a game, and every one of them is a choice between two shapes. The physical one never goes silent. The other one hits zero at a range you choose. The hybrids (FMOD's inverse tapered, Godot's inverse times a linear taper) try to get both.

### Eyes-open design judgment

Neither curve is "right." Each one answers a different question.

- **The inverse curve is honest about distance.** Every doubling costs the same 6 dB, so players can judge range by ear at any distance. Its costs: without the clamp at `r`, a sound at half the reference distance would play 6 dB louder than authored, so every engine clamps or caps it. And it never reaches zero. You must pair it with a max distance or a culling rule, or every distant sound keeps running. [Week 14](w14-optimization-voices-memory-streaming.md) covers voice budgets. For now, know that "inaudible" and "not playing" are different things.
- **The linear curve is honest about range.** It guarantees silence at `R`, and players learn that edge (Minecraft players learn the 16-block rule this way). Its cost is that it carries almost no distance information for most of its range. An enemy at 8 m and one at 16 m differ by only 3.5 dB, which is hard to tell apart in a busy mix.
- **The range of a sound is a gameplay rule.** In a competitive shooter, the footstep radius is a detection radius. If you lengthen it, you reward players who listen. If you shorten it, you reward players who flank. Write it in the design document with the same care as weapon range, and make it identical for every client.
- **Per-category curves beat one global curve.** Give each category of sound its own `r`, `R` and shape: footsteps, gunfire, ambience, voices. Part B of lab 7 asks you to do exactly this for a sound list.

Decide deliberately which sounds need a guaranteed edge (gameplay information), which need a long honest tail (atmosphere and orientation), and which should be culled early to save voices.

### Check yourself on the curves

1. With the inverse curve and `r = 2 m`, at what distance is a sound 24 dB below its authored level?
2. A linear curve has `r = 1 m` and `R = 41 m`. What is the level in dB at 21 m?
3. Unity's Logarithmic mode ignores max distance. A designer sets max distance to 20 m and expects silence at 20 m. With `r = 1 m`, what level does the sound actually have at 20 m and at 40 m?

<details>
<summary>Answers</summary>

1. 24 dB is four doublings of 6.02 dB (24.08), so `d ≈ 2 × 2⁴ = 32 m`. Exactly, `d = 2 × 10^(24/20) = 31.7 m`.
2. `g = 1 − 20/40 = 0.5`, so −6.0 dB. Halfway to the edge is only 6 dB down.
3. `20 · log10(1/20) = −26.0 dB` at 20 m and `−32.0 dB` at 40 m. The sound is quiet, not silent, and it keeps playing.

</details>

## 3. Which way: equal-power panning

Distance gives you one gain. Direction splits it between two speakers. The simplest useful version works in two dimensions, looking down on the world.

### Pan position from a dot product

Let the listener stand at `P` and let `right` be the unit vector pointing to the listener's right. Let the emitter be at `S`. The unit direction to the emitter is `u = (S − P) / |S − P|`. The pan position is

```
p = u · right          (−1 = hard left, 0 = centre, +1 = hard right)
```

You met this in MA101 week 13: the dot product of two unit vectors is the cosine of the angle between them. A sound straight ahead is at 90° to `right`, so `p = 0`. A sound directly to the right gives `p = 1`.

Notice that a sound straight behind you also gives `p = 0`. Stereo panning cannot tell front from back. Week 1 showed why the ear itself struggles with this. Games handle it with other cues, such as filtering sounds behind the listener or using HRTF rendering on headphones (HRTF is a head-related transfer function, a filter measured from real ears).

### From pan position to two gains

The obvious rule is linear: `left = (1 − p) / 2`, `right = (1 + p) / 2`. It has a flaw. Two uncorrelated signals add by power, not by amplitude, and a single signal sent to two speakers is heard at roughly its combined power. At the centre, each speaker gets 0.5, and the total power is `0.5² + 0.5² = 0.5`, a 3 dB dip. A sound walking across the stereo field gets quieter in the middle.

The **equal-power pan law** fixes this with a quarter circle:

```
a = (p + 1) / 2
left  = cos(a · π/2)
right = sin(a · π/2)
```

Because `cos² + sin² = 1`, the total power is 1 at every position. At the centre each speaker gets `cos(π/4) = 0.707`, which is −3 dB per speaker and 0 dB in total. This exact formula is the Web Audio `StereoPannerNode` algorithm for mono input. Godot's class reference says its two-speaker panning uses the same standard.

```python
import math

def equal_power(p):
    a = (p + 1) / 2
    return math.cos(a * math.pi / 2), math.sin(a * math.pi / 2)

def linear_pan(p):
    return (1 - p) / 2, (1 + p) / 2

for p in (-1, -0.5, 0, 0.5, 1):
    for name, f in (("equal-power", equal_power), ("linear", linear_pan)):
        left, right = f(p)
        power_db = 10 * math.log10(left**2 + right**2)
        print(f"p={p:+.1f} {name:<11} L={left:.3f} R={right:.3f} total {power_db:+.1f} dB")
```

Output:

```
p=-1.0 equal-power L=1.000 R=0.000 total +0.0 dB
p=-1.0 linear      L=1.000 R=0.000 total +0.0 dB
p=-0.5 equal-power L=0.924 R=0.383 total +0.0 dB
p=-0.5 linear      L=0.750 R=0.250 total -2.0 dB
p=+0.0 equal-power L=0.707 R=0.707 total +0.0 dB
p=+0.0 linear      L=0.500 R=0.500 total -3.0 dB
p=+0.5 equal-power L=0.383 R=0.924 total +0.0 dB
p=+0.5 linear      L=0.250 R=0.750 total -2.0 dB
p=+1.0 equal-power L=0.000 R=1.000 total +0.0 dB
p=+1.0 linear      L=0.000 R=1.000 total +0.0 dB
```

The final speaker gains multiply the two effects: `left_out = g(d) · left(p)`, `right_out = g(d) · right(p)`. Distance and direction are independent knobs.

### How far to pan

Full panning is not always best. A sound hard-panned into one ear on headphones feels unnatural at close range, and players on a single speaker lose it entirely if it only reaches one channel. Godot exposes a panning strength that scales the effect, where 0 disables panning and 1 fully mutes one channel for a sound exactly to the side. A good rule: pan fully for small, distant, gameplay-critical sounds (where is the sniper?), and less for large or close sources (the dragon filling the screen is not "on the left").

## 4. Through what: filters as distance and occlusion cues

Loudness is not the only thing distance changes. Air absorbs high frequencies more than low ones over long distances, and walls block highs far more than lows. Games imitate both with a **low-pass filter**, which lets low frequencies through and cuts high ones.

- **Distance filtering.** Godot's `AudioStreamPlayer3D` has an attenuation filter with a default cutoff of 5,000 Hz and a strength of −24 dB, applied more strongly as the sound attenuates. A distant explosion then sounds dull and far away, where the gain alone would only make it quiet.
- **Occlusion.** When a raycast from listener to emitter hits a wall, lower the gain a few dB and lower the filter cutoff. The player hears "the fight is behind that door" rather than "the fight is quiet."
- **Reverb send.** Send more of a distant sound to the room's reverb and less of the dry signal. Close sounds are mostly dry, far sounds mostly reverberant. This is one of the strongest distance cues there is, and it costs one parameter per sound.

These cues matter more than exact loudness, because the player hears loudness relative to the whole mix, which changes all the time. [Week 10](w10-mixing-ducking-and-priority.md) deals with that mix.

## 5. Where is the listener?

In a first-person game, the listener sits at the camera, which is also the character's head. In a third-person game the camera floats several metres behind the character, and you have to choose.

- **Listener at the camera.** Panning matches the screen. Distances are wrong, though: an enemy standing next to the character is 5 m from the camera, so it sounds farther than it is.
- **Listener at the character.** Distances match gameplay. Panning can disagree with the screen when the camera orbits.
- **Split.** Compute distance (attenuation) from the character and direction (panning) from the camera. FMOD's Studio API supports this directly: `setListenerAttributes` takes an optional attenuation position that is used for distance while the listener's own position and facing are used for direction. It gives you correct gameplay ranges and panning that matches what the player sees.

For an MMO ([week 12](w12-audio-for-mmos-many-players-one-mix.md)), the choice matters more. The camera often zooms far out, and dozens of other players' spells land around your character. Attenuating from the camera would make your own fight sound distant every time you zoom out.

## In-class activity (25 minutes)

Work in pairs. You are designing the audio for a small top-down co-op dungeon game with a 40 m wide screen.

1. List six sounds: player footsteps, enemy footsteps, enemy attack wind-up, a waterfall ambience, a treasure chest's shimmer loop, and a teammate's healing spell.
2. For each, choose a curve (inverse, linear, tapered), `r` and `R`. Use the interactive's custom mode to check the level at 10 m, 20 m and 40 m.
3. Mark which two sounds carry gameplay information that must never be missed. For those, compute the level at the edge of the screen and say whether a player will hear it over the waterfall (assume the waterfall sits at −12 dB where the player stands).
4. Swap sheets with another pair. Find one sound whose range contradicts the gameplay (for example, an attack wind-up that goes silent before the attack can reach you).

Expected output: a six-row table, the two edge-of-screen levels from step 3, and one contradiction found in another pair's sheet.

## Common misconceptions

- **"Linear attenuation is the natural one, because it's a straight line."** It is straight in amplitude. Your ear hears something close to decibels, where the linear curve is a cliff at the end. The physical curve is the inverse one.
- **"Max distance means the sound goes silent there."** It depends on the engine and the mode. In FMOD's default inverse mode, the sound stops attenuating at max distance and holds its level. Unity's Logarithmic mode ignores max distance entirely. Read the mode, not the field name.
- **"If you can't hear it, it costs nothing."** A sound at −60 dB still takes a voice and still gets mixed unless the engine culls it. Pair long curves with a cull distance.
- **"Panning a sound to the centre should give each speaker half."** That is the linear pan law, which dips 3 dB at the centre. Equal-power panning gives each speaker 0.707 so the total stays constant.

## Check yourself

1. A sword clash uses the inverse curve with `r = 3 m`. At what distance is it 18 dB down? What about 30 dB down?
2. A designer wants an enemy footstep to stay above −20 dB (clearly readable) out to 20 m and to be silent from 30 m on. With `r = 1 m`, which of the three curves (inverse, linear, tapered) can meet both requirements? Give one set of parameters.
3. The listener stands at (0, 0) and faces +y, so `right = (1, 0)`. An emitter is at (3, 4). Compute the pan position `p` and both equal-power gains.
4. Using the Web Audio inverse formula with `ref = 1` and rolloff factor `f = 2`, compute the gain at `d = 5`. How does that compare with the `f = 1` gain, in dB?
5. Your third-person game attenuates from the camera, which sits 6 m behind the character. A teammate stands 2 m from the character, on the camera's side. By how many dB does the camera's listener underestimate the teammate's level, compared with a listener on the character, if the curve is inverse with `r = 1 m`? (Assume the teammate is 4 m from the camera.)

<details>
<summary>Answers</summary>

1. Every 6.02 dB is a doubling. 18 dB is three doublings, so `3 × 8 = 24 m`. For 30 dB: `3 × 10^(30/20) = 94.9 m`.
2. The inverse curve is at −20 dB by 10 m and never reaches silence, so it fails both. The tapered curve follows the inverse curve close in, so it is also at −20 dB by 10 m and fails the first requirement. Only the linear curve works. It crosses −20 dB where `g = 0.1`, at `d = 1 + 0.9 (R − 1)`. That is at least 20 m when `R ≥ 22.1`, and silence from 30 m needs `R ≤ 30`. For example, `R = 26` gives −20 dB at 23.5 m and silence at 26 m. This is the case for the linear curve: clear, then gone.
3. `|S − P| = 5`, so `u = (0.6, 0.8)` and `p = u · right = 0.6`. Then `a = 0.8`, `left = cos(0.4π) = 0.309`, `right = sin(0.4π) = 0.951`.
4. `1 / (1 + 2 × 4) = 1/9 = 0.111`, which is −19.1 dB. With `f = 1` it is `1/5`, −14.0 dB. Doubling the rolloff factor makes it 5.1 dB quieter at this distance.
5. From the character: `20 · log10(1/2) = −6.0 dB`. From the camera: `20 · log10(1/4) = −12.0 dB`. The camera listener hears the teammate 6 dB quieter than the gameplay distance suggests.

</details>

## Lab / assignment hook

[Lab 07, attenuation and panning](../labs/lab07.md). You implement the linear, tapered and equal-power functions from this lecture in Python, find the audible radius of each curve, and design an attenuation table for a twelve-sound game. The table feeds the SFX pack assessment, where every 3D sound must ship with its curve and range.

## Sources

- Minecraft Wiki, "Commands/playsound" (Java Edition, accessed September 2026). The 16-block audible radius at volume 1, multiplied by volume above 1; volume below 1 makes the sound quieter; falloff to silence within the sphere.
- W3C, *Web Audio API* (editor's draft, accessed September 2026), sections 1.27 (PannerNode), 6.3.3 (StereoPannerNode panning) and 6.4 (distance effects). The linear, inverse and exponential distance models; defaults `refDistance = 1`, `maxDistance = 10000`, `rolloffFactor = 1`, `distanceModel = "inverse"`, `panningModel = "equalpower"`; the `cos`/`sin` equal-power algorithm. https://webaudio.github.io/web-audio-api/
- Firelight Technologies, *FMOD Engine 2.03 Core API Reference*, "FMOD_MODE" (accessed September 2026). Descriptions of `FMOD_3D_INVERSEROLLOFF` (the default), `FMOD_3D_LINEARROLLOFF`, `FMOD_3D_LINEARSQUAREROLLOFF` and `FMOD_3D_INVERSETAPEREDROLLOFF`.
- Unity Technologies, *Unity 6.6 Scripting API*, `AudioSource.maxDistance` and `AudioSource.minDistance` (accessed September 2026). Logarithmic mode ignores max distance; Linear mode reaches zero at max distance.
- Godot Engine, `doc/classes/AudioStreamPlayer3D.xml` and `scene/3d/audio_stream_player_3d.cpp`, master branch (4.8 in development, September 2026). Default `unit_size = 10`, `max_db = 3`, the inverse-distance formula, the `1 − d / max_distance` taper, the attenuation filter (5,000 Hz, −24 dB), and the note on WebAudio-standard stereo panning. https://github.com/godotengine/godot
- Nave, R., *HyperPhysics*, "Inverse Square Law, Sound" (Georgia State University). Intensity from a point source falls with the square of distance in the absence of reflections.
- Collins, K. (2008). *Game Sound: An Introduction to the History, Theory, and Practice of Video Game Music and Sound Design*. MIT Press. Chapter 7.

## Interactive spec: examples/w07-attenuation-curves.html

**The one insight.** The same attenuation curve that looks gentle on a gain plot is a cliff on a decibel plot, and the one that looks brutal on the gain plot is a steady 6 dB per doubling. Your ear agrees with the decibel plot.

**Layout.** Three panels. On mobile they stack; at 1280 px wide the map is on the left and the two plots are stacked on the right.

1. **Top-down map** (square canvas, 0 to 64 m on each axis, grid every 8 m). The listener is a circle with a facing arrow at the centre (32, 32), facing up (+y). The emitter is a draggable dot, starting at (32, 40), 8 m ahead. Draw dashed circles at `r` and `R` around the listener. Keyboard: arrow keys move the emitter 1 m, shift+arrow 4 m. A second control rotates the listener's facing in 15° steps (buttons "turn left" and "turn right").
2. **Gain plot.** x axis distance 0 to 64 m (linear), y axis gain 0 to 1 (linear). Draw all selected curves. A vertical marker shows the current distance, and a dot marks each curve's gain there.
3. **Level plot.** x axis distance 0.5 to 64 m on a log2 scale (ticks at 0.5, 1, 2, 4, 8, 16, 32, 64), y axis level −60 to +3 dB. Same curves, same marker. Draw a horizontal dashed line at −40 dB labelled "about inaudible in a mix" and one at −20 dB.

**Curves (exact formulas).** `g(d)` with `r`, `R`, and rolloff `f`:

```
inverse(d)  = r / (r + f * (max(d, r) - r))
linear(d)   = max(0, 1 - f * (min(max(d, r), R) - r) / (R - r))
tapered(d)  = min(inverse(d) with f = 1, linear(d) with f = 1 squared)
godot(d)    = min(10^(3/20), r / max(d, 1e-6)) * (R > 0 ? max(0, 1 - d / R) : 1)
L(d)        = 20 * log10(g(d)), shown as "-inf" when g = 0
```

**Controls.**
- Checkboxes for which curves to draw: inverse (on), linear (on), tapered (off), godot-style (off). One radio group chooses which curve drives the audio (default inverse).
- Sliders: `r` 0.5 to 10 m (step 0.5, default 1), `R` 4 to 64 m (step 1, default 32), rolloff `f` 0.5 to 4 (step 0.1, default 1).
- Preset buttons: "physical" (inverse, r = 1, f = 1), "hard edge at 16" (linear, r = 1, R = 16), "hard edge at 32" (linear, r = 1, R = 32, mirrors a volume-2 sound in the Minecraft hook; the shape inside Minecraft's radius is not modeled), "Godot default" (godot, r = 10, R = 0 meaning no taper).
- Play/stop button for the sound.

**Readouts next to the plots.** Distance (1 decimal), pan position `p` (2 decimals), left and right gains (3 decimals), and for each drawn curve its gain (3 decimals), level in dB (1 decimal), and the distances where it crosses −20 dB and −40 dB (1 decimal, or "never" when it does not reach them within 10,000 m). Compute crossings by bisection on [0, 10000] to 0.01 m.

**Pan.** `p = dot(normalize(S - P), right)`, clamped to [-1, 1], with `right` the listener's right-hand unit vector; `p = 0` when the emitter sits on the listener. Gains `left = cos((p+1)/2 * π/2)`, `right = sin((p+1)/2 * π/2)`.

**Audio (Web Audio, procedural only).** Source: a footstep-like burst every 0.45 s, made of 60 ms of white noise through a band-pass filter at 900 Hz (Q 1.2) with an exponential decay envelope, plus an optional steady 330 Hz triangle tone (toggle "tone") for hearing smooth changes. Route source → `GainNode` (value = selected curve's `g(d)`, set with `setTargetAtTime(g, now, 0.02)`) → `StereoPannerNode` (pan = `p`) → destination. Do not use `PannerNode`, so that what students hear is exactly the model on screen. Start audio only after a user gesture.

**Test values (the page must reproduce these exactly with r = 1, R = 32, f = 1).**

| d (m) | inverse gain | inverse dB | linear gain | linear dB | tapered gain |
|---|---|---|---|---|---|
| 2 | 0.500 | −6.0 | 0.968 | −0.3 | 0.500 |
| 8 | 0.125 | −18.1 | 0.774 | −2.2 | 0.125 |
| 16 | 0.0625 | −24.1 | 0.516 | −5.7 | 0.0625 |
| 28 | 0.036 | −28.9 | 0.129 | −17.8 | 0.017 |
| 32 | 0.031 | −30.1 | 0 | −inf | 0 |

Crossings with r = 1, R = 32: inverse −20 dB at 10.0 m and −40 dB at 100.0 m; linear −20 dB at 28.9 m and −40 dB at 31.7 m. Pan with the listener at (32, 32) facing +y and the emitter at (35, 36): `p = 0.60`, left 0.309, right 0.951.

**Accessibility and states.** All controls reachable by keyboard with visible focus. Respect `prefers-reduced-motion` (no animated transitions of the plots). Light and dark themes from the shared tokens. If audio is unavailable, the plots and readouts still work and a note says so.

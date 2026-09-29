# AU101 · Week 08 — Adaptive Music: Vertical Layering

**Why this matters:** A fight can start at any moment and end at any moment. Linear music, written like a film score, cannot know when. Vertical layering is the cheapest reliable way to make music follow the game: every part of the piece plays all the time, and the game only decides how loud each part is. Most adaptive scores you have heard use it somewhere, and the assessment for this course asks you to build one.

**You will be able to:**
- Compute the gain of each stem and the total level of the mix from an intensity value, using ramp thresholds.
- Explain why layered stems stay in time when they enter, and design stems that work in every combination the game can produce.
- Compute fade times from a smoothing rate and choose different rates for rising and falling intensity.
- Critique a layering design for loudness growth, repetition and the game-state mapping that drives it.

**Before class:** Collins, *Game Sound* (2008), chapter 8, "Compositional approaches to dynamic game music." Play the first level of Super Mario World (SNES, 1990; also in Nintendo's Switch Online SNES library) or watch a recording, and listen for the moment Mario mounts Yoshi.

**Prerequisites from earlier courses:** [MA101 week 8, lerp, inverse lerp and remap](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w08-interpolation-lerp-inverse-lerp-remap.md) (the stem ramp is an inverse lerp with a clamp). [MA101 week 5, logarithms](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md) (decibels). Looking ahead, [GD201 week 3, flow, pacing and intensity graphs](../../GD201-level-and-world-design/lectures/w03-flow-pacing-and-intensity-graphs.md) (year 2) teaches the intensity curve a level designer draws, which is the curve your music follows. [CS101 week 9, delta time](../../CS101-programming-for-games-i/lectures/w09-delta-time-and-frame-rate-independence.md) (rates per second, not per frame). [AU101 week 7](w07-spatial-audio-and-attenuation.md) (the equal-power curve, which returns here as a crossfade). [AU101 week 6, middleware events and parameters](w06-middleware-events-and-parameters.md) (game parameters driving sound).

**Interactive:** [examples/w08-layer-mixer.html](../examples/w08-layer-mixer.html). Keep it open during section 2.

---

## 1. Two ways to make music adapt

Adaptive music (also called dynamic or interactive music) changes in response to what happens in the game. There are two basic moves, and every adaptive score is some mix of them.

- **Vertical:** change *what plays at the same time*. The piece is split into **stems**, separate audio files for groups of instruments (pads, drums, bass, lead), which all play together, in sync, from the same start point. The game raises and lowers each stem's volume. The piece gets thicker or thinner, but it never jumps.
- **Horizontal:** change *what plays next*. The piece is split into sections, and the game picks which section follows which, at musically sensible moments. Next week covers this.

The names come from a score on paper. Instruments are stacked vertically on the page, and time runs horizontally.

This week has one idea: in vertical layering, **nothing starts or stops; only volumes move.** Everything else follows from it.

## 2. Worked example: the combat intensity slider

### The hook

In Super Mario World (SNES, 1990), when Mario climbs onto Yoshi, a bongo part joins the level music. It lands exactly on the beat, wherever in the song you happen to be. When Mario gets knocked off, the bongos vanish and the song carries on without a hiccup.

How does a drum part enter halfway through a bar and still land on the beat? It did not enter. It was playing the whole time, at zero volume.

### The model

Split the piece into `N` stems that share one tempo, one key and one loop length, and start them all on the same sample. The game supplies an **intensity** `x`, a number from 0 (calm) to 1 (the most intense moment you designed for). Each stem `i` has an entry threshold `a_i` and a fade width `w`. Its gain is a clamped ramp:

```
g_i(x) = clamp((x − a_i) / w, 0, 1)
output(t) = Σ g_i(x) · stem_i(t)
```

- `x` is the intensity parameter, 0 to 1.
- `a_i` is the intensity at which stem `i` starts to fade in.
- `w` is the width of the fade, in intensity units. The stem reaches full gain at `a_i + w`.
- `stem_i(t)` is the stem's audio at time `t`. It keeps running whatever its gain is.

A stem with no threshold is the **bed**. It plays at gain 1 always. The ramp is MA101 week 8's inverse lerp, clamped at both ends.

How loud is the total? If the stems are about equally loud and **uncorrelated** (different instruments playing different notes, so their waveforms do not line up), their powers add, not their amplitudes. The level of the mix, relative to one stem at full gain, is

```
L(x) = 10 · log10( Σ g_i(x)² )      dB
```

Four equal stems at full gain give `10 · log10(4) = +6.02 dB`. That number will matter in the design judgment below.

### Numbers you can check

Use four stems: a pad as the bed, drums with `a = 0.2`, bass with `a = 0.45`, and a lead melody with `a = 0.7`, all with `w = 0.2`. This program prints the gains and the level. It runs as shown with `.venv/bin/python`.

```python
import math

STEMS = [("pad", None), ("drums", 0.2), ("bass", 0.45), ("lead", 0.7)]
W = 0.2

def stem_gain(x, a, w=W):
    if a is None:
        return 1.0
    return min(1.0, max(0.0, (x - a) / w))

def level_db(gains):
    return 10 * math.log10(sum(g * g for g in gains))

print("   x   pad drums  bass  lead   level")
for x in (0.0, 0.3, 0.5, 0.6, 0.8, 1.0):
    gains = [stem_gain(x, a) for _, a in STEMS]
    print(f"{x:4.1f}  " + "  ".join(f"{g:4.2f}" for g in gains) + f"  {level_db(gains):+5.2f} dB")
```

It prints:

```
   x   pad drums  bass  lead   level
 0.0  1.00  0.00  0.00  0.00  +0.00 dB
 0.3  1.00  0.50  0.00  0.00  +0.97 dB
 0.5  1.00  1.00  0.25  0.00  +3.14 dB
 0.6  1.00  1.00  0.75  0.00  +4.09 dB
 0.8  1.00  1.00  1.00  0.50  +5.12 dB
 1.0  1.00  1.00  1.00  1.00  +6.02 dB
```

Check one row by hand. At `x = 0.6`, drums are full (`0.6 ≥ 0.4`), bass is at `(0.6 − 0.45)/0.2 = 0.75`, lead is at 0. The level is `10 · log10(1 + 1 + 0.5625) = 10 · log10(2.5625) = 4.09 dB`.

Two things to notice. The thresholds overlap in time only a little: the bass starts fading in at 0.45, just after the drums are full at 0.4, so each entry is heard on its own. And the level climbs 6 dB from calm to full. Whether that is what you want is a design decision.

### The visual

Open the interactive. The main control is a combat intensity slider. As you drag it, four procedurally generated stems (a pad, a drum pattern, a bass line and a lead) fade in and out in real time. You never hear a stem start late or drift off the beat, because none of them ever restarts.

The interactive has two linked views. The top view shows the four ramp functions `g_i(x)` with a marker at the current intensity; it looks like a tidy staircase. The bottom view is a scrolling timeline of the last 20 seconds, with one lane per stem showing its actual gain. Press "fight" and the game-side intensity jumps around (calm, spotted, peak, victory). The timeline shows what the listener really gets: the ramps smoothed over time, so a jump in the game becomes a fade in the music. There is also a "restart stem on entry" switch. Turn it on and each stem starts from its own beginning when it fades in, instead of running all along. Now you hear the drums enter off the beat. That switch is the mistake the whole technique exists to avoid.

### Cross-game recognition

**Super Mario World (SNES, 1990).** Yoshi's bongos are a two-stem layering system with a binary intensity: `x = 1` when riding Yoshi, else 0, and a single stem with `a = 0` and a very small `w`. The Mario Wiki notes the bongos are added to the overworld theme and its arrangements, but not to the Ghost House and Castle themes, where Yoshi cannot go, and not to the Bonus Game theme, which already has bongos.

**Red Dead Redemption (Rockstar, 2010).** Rockstar's behind-the-scenes piece on the score shows composers Bill Elm and Woody Jackson and their session players recording "stem after emotive stem" for the interactive soundtrack. Wikipedia's article on the soundtrack, citing Rockstar's making-of video, says the music was recorded at 130 beats per minute in A minor. That shared tempo and key is the precondition in our model. Any stem can sit on top of any other only because they all agree on the beat and the harmony.

**FMOD Studio (2.03).** In middleware, the model is built directly. You create a parameter (say `intensity`, 0 to 1) and draw an automation curve on each audio track's volume against that parameter. Each curve is a `g_i(x)`, and you can bend it instead of using a straight ramp. FMOD's seek modulator then makes the parameter's value ramp toward a new value at a fixed rate instead of jumping; FMOD calls that rate the seek speed. That is the smoothing in section 3. FMOD also distributes the full FMOD Studio project for Celeste (Power Up Audio and Lena Raine) for educational use. Open it to study how a shipped game's music events and parameters are organized.

In every case the structure is the same: one clock, several parts that always play, and gains driven by a game value.

### Eyes-open design judgment

Vertical layering is fast and robust. It also constrains your composer more than any other technique.

- **Instant response, no waiting.** A gain change is heard within a few milliseconds of the game asking for it. Horizontal switching (next week) usually waits for a beat or a bar. This is layering's main strength, and it is why games often use it for moment-to-moment intensity.
- **One tempo, one key, one loop.** Every stem must work over the same harmonic structure for its whole length. The music cannot modulate, change tempo, or build to a different section, because every stem would have to do the same thing in step. Long layered loops get repetitive. Mix in horizontal changes (next week) to escape the loop.
- **Every reachable combination must sound finished.** With ordered thresholds, only `N` combinations occur (bed; bed + drums; bed + drums + bass; and so on), and the composer can check each one. If stems are driven by independent parameters, `2^N` combinations can occur. Four stems give 16 mixes to check, and eight give 256. Keep the combinations you ship to a number someone can actually listen to.
- **Intensity is louder, unless you decide otherwise.** The +6 dB from four stems is noticeable, and it lands exactly when the sound effects are busiest. You can leave the growth in on purpose (louder feels more intense), trim the stems so full intensity matches the calm level, or duck the music under important effects. [Week 10](w10-mixing-ducking-and-priority.md) covers ducking. Decide which, and write it down.
- **The mapping is the hard part.** The math above is simple. Deciding what `x` means in the game is not. The next section shows one mapping and its failure modes.
- **Cost.** Every stem is a stream that plays even at zero gain. Four stereo stems of 44.1 kHz audio are eight channels decoded all the time. [Week 14](w14-optimization-voices-memory-streaming.md) covers streaming budgets.

Use vertical layering when the game state changes often and unpredictably and the music must answer at once. Do not use it alone when the music needs to go somewhere, such as a boss's second phase, a victory, or a change of location.

### Check yourself on the layers

1. With the four stems above, at what intensity is the mix about 3 dB louder than the bed alone? (Hint: the powers must sum to about 2.)
2. You add a fifth stem, choir, with `a = 0.85` and `w = 0.15`. What is the level at `x = 1` now, and at `x = 0.9`?
3. The composer delivers a drum stem that is 4 bars long and a pad that is 6 bars long. What goes wrong after the first loop, and after how many bars do the two line up again?

<details>
<summary>Answers</summary>

1. Pad plus drums gives power `1 + g_d²`. That reaches 2 when drums are full, at `x = 0.4`, where the level is `10 · log10(2) = 3.01 dB`. So `x = 0.4`.
2. At `x = 1` five full stems give `10 · log10(5) = +6.99 dB`. At `x = 0.9` the choir is at `(0.9 − 0.85)/0.15 = 0.333`, so power is `4 + 0.111 = 4.111` and the level is `+6.14 dB`.
3. After 4 bars the drums restart while the pad is in bar 5, so the drum pattern and the harmony drift against each other. They line up again after the least common multiple of 4 and 6, which is 12 bars. Every stem must share one loop length (or divide it evenly).

</details>

## 3. Smoothing: from game events to musical fades

Game intensity jumps. An enemy spots you and `x` goes from 0.1 to 0.8 in one frame. If the stem gains jumped too, you would hear the bass and lead switch on like a light. So the music does not read `x` directly. It follows a smoothed copy that moves at a limited rate:

```
if target > x:   x = min(target, x + up_rate · dt)
else:            x = max(target, x − down_rate · dt)
```

`dt` is the frame time in seconds (CS101 week 9), and the rates are in intensity units per second. FMOD's seek speed is this rate.

Use two rates, not one. Take `up_rate = 0.5` per second and `down_rate = 0.1` per second.

- **Rising.** From calm (0.1) to peak (1.0) takes `0.9 / 0.5 = 1.8 s`. The drums reach full at `x = 0.4`, which takes `0.3 / 0.5 = 0.6 s`. The player hears the fight start almost at once.
- **Falling.** From 1.0 back to 0 takes `1.0 / 0.1 = 10 s`. The lead fades out between `x = 0.9` and `0.7` (1 to 3 s after the fight ends). The drums fade out between `x = 0.4` and `0.2` (6 to 8 s after).

The asymmetry is deliberate. A fast rise matches the jolt of being spotted. A slow fall avoids the "music gives the game away" problem. If the combat layers vanish the instant the last enemy dies, the music tells players there is nothing left to fear. If an enemy is hiding, it tells them that too. A slow release also absorbs flicker, when an enemy steps in and out of aggro range and the raw intensity bounces between two values every second.

### Driving intensity from game state

Here is one mapping for a small action game:

```
x = clamp(0.2 · enemies_engaged + 0.4 · (1 − health_fraction), 0, 1)
```

- Full health, two enemies: `x = 0.4`. Pad and drums.
- Full health, four enemies: `x = 0.8`. Lead half in.
- Half health, three enemies: `0.6 + 0.2 = 0.8`. Same music as four enemies at full health.
- Low health (10%), no enemies left: `x = 0.36`. The drums keep going after the fight.

The last line is a bug or a feature, depending on your game. It keeps tension up while the player is weak. It also means a player who stays hurt never hears calm music again. This is where GD201's intensity graph helps. Sketch the curve the level designer wants the player to feel, then check that your formula produces it on a real playthrough. Log `x` every second in a playtest and plot it next to the designer's graph.

## 4. Swapping one stem for another: the equal-power crossfade

Sometimes you want a stem to be replaced rather than added. The calm flute melody should give way to a brass melody as the fight starts, not play on top of it. That is a **crossfade** between two stems driven by one value `t` from 0 to 1.

The obvious crossfade is linear, `out = 1 − t`, `in = t`. For two uncorrelated melodies it dips in the middle, for the same reason the linear pan law dipped last week. Use the equal-power curve from week 7 instead: `out = cos(t · π/2)`, `in = sin(t · π/2)`.

```python
import math

for t in (0.0, 0.25, 0.5, 0.75, 1.0):
    lin_out, lin_in = 1 - t, t
    ep_out, ep_in = math.cos(t * math.pi / 2), math.sin(t * math.pi / 2)
    lin_db = 10 * math.log10(lin_out**2 + lin_in**2)
    ep_db = 10 * math.log10(ep_out**2 + ep_in**2)
    print(f"t={t:.2f}  linear {lin_out:.3f}/{lin_in:.3f} {lin_db:+.1f} dB   "
          f"equal-power {ep_out:.3f}/{ep_in:.3f} {ep_db:+.1f} dB")
```

Output:

```
t=0.00  linear 1.000/0.000 +0.0 dB   equal-power 1.000/0.000 +0.0 dB
t=0.25  linear 0.750/0.250 -2.0 dB   equal-power 0.924/0.383 +0.0 dB
t=0.50  linear 0.500/0.500 -3.0 dB   equal-power 0.707/0.707 +0.0 dB
t=0.75  linear 0.250/0.750 -2.0 dB   equal-power 0.383/0.924 +0.0 dB
t=1.00  linear 0.000/1.000 +0.0 dB   equal-power 0.000/1.000 +0.0 dB
```

One caution. If the two stems are the *same* recording, or strongly correlated (the same melody on two similar instruments, perfectly in phase), their amplitudes add, and the linear fade is the one that stays level. Equal-power then bulges by +3 dB in the middle. For different instruments playing different parts, which is the usual case in layering, equal-power is the right default.

## 5. Writing for layers

A few rules that composers who write for layering tend to follow. Treat them as a checklist when you review a stem set.

- **Give each stem its own frequency range.** If the bass stem and the pad both sit around 100 to 200 Hz, adding the bass makes the low end muddy instead of stronger. Pads in the middle, bass low, lead on top, percussion spread out.
- **Make the bed complete.** The bed is what players hear most. It must sound like finished music on its own, not like a backing track waiting for a melody.
- **Put identity in the early stems.** If the theme's recognizable melody is only in the top stem, most players hear it only in the biggest fights. Put a version of it in the bed or the second stem.
- **Loop points in the same place.** Every stem is cut to exactly the same length, with the loop point at the same sample. A few milliseconds of difference accumulates into audible drift over a long session.
- **Leave headroom.** Mix the stems so that the full combination peaks below full scale. Lab 8's renderer applies a fixed −6 dB trim for exactly this reason.

## In-class activity (25 minutes)

Work in groups of three. You are scoring a stealth level.

1. Define an intensity formula from three game values: guards alerted (0 to 3), whether the player is currently seen (0 or 1), and seconds since last seen. Write it as one line, like section 3's example.
2. Choose four stems for a stealth score and give each a threshold and fade width. One stem must be the bed.
3. Choose up and down rates. Compute how long the music takes to reach full intensity when the player is spotted, and how long it takes to return to the bed after the guards give up.
4. Write the three most likely game situations as rows in a table: game values, `x`, which stems are audible, and the level in dB.
5. Swap with another group. Find a situation their formula handles badly (for example, music that tells the player a guard is still searching when the game says the search is over).

Expected output: one formula, a stem table, two times from step 3, a three-row situation table, and the problem the other group found.

## Common misconceptions

- **"The drums start when the fight starts."** In vertical layering, the drums started when the music started. The fight only makes them audible. That is why they land on the beat.
- **"More layers means proportionally louder."** Uncorrelated stems add by power. Two equal stems are +3 dB, four are +6 dB, eight are +9 dB. Each doubling of stems adds 3 dB, not double the loudness.
- **"Smoothing is just to hide clicks."** Clicks come from instant gain jumps inside one audio buffer, and any short ramp (a few milliseconds) fixes them. The smoothing in section 3 works over seconds and is a musical decision about how quickly the score reacts.
- **"Linear crossfades are wrong."** They are right for identical or strongly correlated material. They dip for different material. Pick the curve for the signals you have.

## Check yourself

1. Using the four-stem set from section 2, what is `x` and which stems are audible for a player at 30% health fighting two enemies, using section 3's mapping?
2. With `up_rate = 0.5` and `down_rate = 0.1`, the intensity target goes from 0 to 0.6 at `t = 0` and back to 0 at `t = 3 s`. What is the smoothed `x` at `t = 1`, `t = 3` and `t = 5`?
3. A designer wants full intensity to be no louder than the bed alone. By what factor (and how many dB) must every stem's gain be scaled at `x = 1`? What does the player lose?
4. A crossfade between two different melodies uses `out = 1 − t` and `in = t`. At `t = 0.5`, what is the level change? What curve would you use instead, and what is its value at `t = 0.5`?

<details>
<summary>Answers</summary>

1. `x = 0.2 × 2 + 0.4 × 0.7 = 0.68`. Pad (1), drums (1), bass `(0.68 − 0.45)/0.2 = 1` (clamped from 1.15), lead 0. Three stems at full, level `10 · log10(3) = 4.77 dB`.
2. At `t = 1`: `x = min(0.6, 0.5 × 1) = 0.5`. At `t = 1.2 s` it reaches 0.6 and holds. At `t = 3` it is 0.6. At `t = 5` it has fallen for 2 s at 0.1 per second: `0.6 − 0.2 = 0.4`.
3. The power sum at `x = 1` is 4, so every gain must be scaled by `1/√4 = 0.5`, which is −6.02 dB. The player loses the loudness cue that the fight has escalated; only the texture changes. Some designers compensate partly, for example by 3 dB.
4. The power is `0.25 + 0.25 = 0.5`, a −3.0 dB dip. Use the equal-power curve `cos(t · π/2)` and `sin(t · π/2)`, both 0.707 at `t = 0.5`, total power 1, 0 dB.

</details>

## Lab / assignment hook

[Lab 08, a layered score from an intensity curve](../labs/lab08.md). You implement the stem ramp, the level formula and the asymmetric smoother, render 32 seconds of procedurally generated layered music to a WAV file, then retune thresholds and rates for a given encounter. The rendered file and your tuning notes are the first half of the adaptive music assessment; next week's lab adds the horizontal half.

## Sources

- Super Mario Wiki, "Ground BGM (Super Mario World)" (formerly "Overworld Theme", accessed September 2026). Bongo percussion added while riding Yoshi in Super Mario World (SNES, 1990) to the ground theme and its arrangements, except "Ghost House BGM", "Castle BGM", "Bonus Game BGM" and jingles.
- Rockstar Games Newswire, "Behind the Scenes of the Red Dead Redemption Soundtrack" (July 28, 2010, archived). Bill Elm and Woody Jackson and session players recording stems for the interactive soundtrack.
- Wikipedia, "Music of Red Dead Redemption" (accessed September 2026). Music recorded at 130 BPM in A minor, citing Rockstar's making-of documentary.
- Firelight Technologies, *FMOD Studio User Manual 2.03* (2.03.14, May 2026), chapter 7 "Parameters" and chapter 28 "Glossary" (entries for automation, seek modulator, seek speed). Appendix "Celeste Getting Started Guide": the Celeste FMOD Studio project by Power Up Audio and Lena Raine, released for non-commercial educational use.
- Collins, K. (2008). *Game Sound: An Introduction to the History, Theory, and Practice of Video Game Music and Sound Design*. MIT Press. Chapter 8.

## Interactive spec: examples/w08-layer-mixer.html

**The one insight.** In vertical layering every stem plays all the time and only gains move, so a layer can enter at any instant and still land on the beat. The "restart stem on entry" switch makes the alternative audible.

**Audio engine (Web Audio, all procedural, no samples).** One `AudioContext`. 120 BPM, 4/4, loop of 4 bars (8 s). A lookahead scheduler (25 ms timer, 100 ms lookahead) schedules notes for all four stems against `audioContext.currentTime`, from the same bar-0 origin. Each stem feeds its own `GainNode`; all four feed a master `GainNode` (value 0.5, the fixed −6 dB trim) and then the destination.

- **Pad (bed):** chords A minor (A3 C4 E4), F major (F3 A3 C4), G major (G3 B3 D4), E major (E3 G#3 B3), one per bar. Three sine oscillators per chord at 0.12 each, 50 ms attack and release.
- **Drums:** kick on every beat (sine sweep from 110 Hz to 50 Hz over 80 ms, exponential decay), hat on every eighth note (white noise through a high-pass at 7 kHz, 30 ms decay).
- **Bass:** eighth notes on the bar's root (A2, F2, G2, E2), every fourth eighth an octave up. Sawtooth through a low-pass at 900 Hz, decay 150 ms.
- **Lead:** one note per beat, repeating A4 C5 D5 E5 D5 C5 B4 A4. Triangle wave, 25 ms attack, 300 ms decay.

**Model (exact).**

```
g_i(x) = a_i == null ? 1 : clamp((x - a_i) / w, 0, 1)
thresholds: pad null, drums 0.2, bass 0.45, lead 0.7; w = 0.2 (slider)
smoothed x: if target > x: x = min(target, x + up * dt) else x = max(target, x - down * dt)
fade shape "equal-power": gain = sin(g_i * π/2); "linear": gain = g_i
level_dB = 10 * log10(Σ gain_i²)
compensation (toggle): multiply every gain by 1 / sqrt(Σ gain_i²)
```

Apply gains with `setTargetAtTime(gain, now, 0.015)` every animation frame, so no clicks.

**Controls.**
- Intensity slider 0 to 1, step 0.01 (the target). Keyboard: arrows ±0.01, page up/down ±0.1.
- Up rate slider 0.05 to 2 per second (default 0.5), down rate 0.02 to 2 (default 0.1). A "no smoothing" checkbox sets both to infinity.
- Fade width `w` slider 0.05 to 0.4 (default 0.2).
- Fade shape radio: linear (default), equal-power.
- Toggle "compensate loudness" (off by default).
- Toggle "restart stem on entry" (off by default). When on, a stem whose smoothed gain rises from 0 is re-scheduled from its own bar 0 at that moment, instead of following the shared clock. This is the deliberately wrong version.
- Button "fight": plays a scripted target sequence (0.1 for 4 s, 0.55 for 3 s, 1.0 for 6 s, 0 afterwards), then hands control back to the slider.
- Play/stop (audio starts only after a user gesture). Per-stem solo buttons.

**Views.**
1. **Ramp view:** x axis intensity 0 to 1, y axis gain 0 to 1. The four `g_i(x)` curves, a solid vertical line at the smoothed `x`, a dashed one at the target.
2. **Timeline view:** the last 20 s scrolling left. Top lane shows target (dashed) and smoothed (solid) intensity. Below, one lane per stem with its applied gain as a filled area. Vertical grid lines on every bar (2 s). Freeze scrolling under `prefers-reduced-motion` and redraw once per second instead.
3. **Readouts:** target and smoothed `x` (2 decimals), each stem's gain (2 decimals), `level_dB` (2 decimals, relative to one stem), current bar and beat.

**Test values (defaults, linear shape, no compensation).**

| x | pad | drums | bass | lead | level dB |
|---|---|---|---|---|---|
| 0.0 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 0.3 | 1.00 | 0.50 | 0.00 | 0.00 | 0.97 |
| 0.5 | 1.00 | 1.00 | 0.25 | 0.00 | 3.14 |
| 0.6 | 1.00 | 1.00 | 0.75 | 0.00 | 4.09 |
| 0.8 | 1.00 | 1.00 | 1.00 | 0.50 | 5.12 |
| 1.0 | 1.00 | 1.00 | 1.00 | 1.00 | 6.02 |

With compensation on at `x = 1`, each gain shows 0.50 and the level shows 0.00 dB. With the "fight" sequence and default rates, the smoothed `x` starts at 0.1, reaches 0.55 at 0.9 s after the first jump (4.9 s into the sequence), reaches 1.0 at 0.9 s after the second jump (7.9 s), and is back to 0.4 at 6 s after the target drops to 0 (19.0 s).

**Accessibility.** All controls keyboard reachable with visible focus; readouts in an `aria-live="polite"` region updated at most twice per second. Light and dark themes from the shared tokens. If audio is blocked, the views still animate from the model and a note says sound is off.

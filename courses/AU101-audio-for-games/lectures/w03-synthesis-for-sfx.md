# AU101 · Week 03 — Synthesis for SFX

**Why this matters:** A coin pickup, a jump, a laser and a hurt sound can each be built from about six numbers. Synthesis lets you make placeholder sounds in minutes and whole retro soundscapes at runtime, and it teaches you what makes any sound read as "good" or "bad" to a player. The same few controls show up in 1980s console hardware, jam tools and every browser.

**You will be able to:**
- Compute the frequency of a sliding tone at any moment from its start frequency and slide rate, and convert the change to semitones.
- Design pickup, jump, laser and hurt sounds from a waveform, a pitch contour and an amplitude envelope, and justify each choice.
- Predict when a synthesised tone will alias at a given sample rate, and name two ways to avoid it.
- Critique a synthesised sound set for readability: does each contour match the meaning of its event?

**Before class:** Collins, *Game Sound* (2008), chapter 3. As you read, note each sound chip or technique named and what it could and could not do. Try the browser port of sfxr at sfxr.me for ten minutes. Press each preset button several times and note what the results in one category have in common.

**Prerequisites from earlier courses:** [AU101 week 1](w01-what-sound-does-feedback-space-emotion.md) (frequency, the feedback jobs). [AU101 week 2](w02-recording-and-foley-basics.md) (sample rate and the Nyquist limit). [MA101 week 4, exponentials](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md) (growth by a constant factor per step). [MA101 week 8, interpolation](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w08-interpolation-lerp-inverse-lerp-remap.md) (lerp, used for envelopes). [MA101 week 10, sin and cos](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w10-angles-radians-sin-cos.md) (phase and frequency). [CS101 week 14](../../CS101-programming-for-games-i/lectures/w14-polish-pass-sound-particles-screen-shake.md) (semitones and `2^(s/12)`).

**Interactive:** [examples/w03-pitch-contour-synth.html](../examples/w03-pitch-contour-synth.html). Keep it open during section 3.

---

## 1. A synthesiser is three questions

Recording captures a sound that exists. **Synthesis** computes one from numbers. Every synthesised sound effect answers three questions, and the rest of this lecture is about each answer.

1. **What shape does one cycle have?** That is the **oscillator** and its **waveform**.
2. **How does the pitch move over time?** That is the **pitch contour**: start frequency, slide, jumps.
3. **How does the level move over time?** That is the **amplitude envelope**.

A fourth optional stage, the **filter**, removes some frequencies. It matters more for music and ambience than for short effects, so we treat it briefly in section 4.

### Oscillators and waveforms

An oscillator repeats a shape `f` times per second. The standard way to build one in code is a **phase accumulator**. Keep a number `phase` between 0 and 1 that says how far through the current cycle you are. Every sample, add `f / fs` (frequency divided by sample rate) and wrap back into 0 to 1. Then turn the phase into a sample value with one of these shapes:

| Waveform | Sample from phase `φ` | Sound | Harmonics present |
|---|---|---|---|
| Sine | `sin(2π φ)` | pure, soft, whistle-like | only the fundamental |
| Square | `+1 if φ < 0.5 else −1` | hollow, buzzy, the classic 8-bit tone | odd harmonics, level `1/k` |
| Sawtooth | `2φ − 1` | bright, brassy, aggressive | all harmonics, level `1/k` |
| Triangle | `1 − 4 × |φ − 0.5|` | soft but clearer than sine, "flute-like" | odd harmonics, level `1/k²` |
| Noise | a new random value each sample | hiss, crash, explosion | everything, no pitch |

A **harmonic** is a component at a whole-number multiple `k` of the fundamental frequency. A 400 Hz square wave contains 400, 1,200, 2,000, 2,800 Hz and so on, each weaker than the last. Harmonic content is what makes a square and a sine at the same pitch sound different. It is also the source of the aliasing problem in section 4.

Why a phase accumulator instead of `sin(2π f t)`? Because game sounds change frequency while they play. If you compute `sin(2π f(t) t)` with a changing `f`, the wave jumps whenever `f` changes and you hear clicks and wrong pitches. Accumulating phase keeps the wave continuous, so the frequency can change every sample.

### The amplitude envelope

An **envelope** is a curve that shapes level over time. Synthesisers for music use four stages, **ADSR**: attack (rise from silence), decay (fall to a held level), sustain (held level while a key is down) and release (fall to silence after the key is released). A one-shot sound effect has no key to hold, so it usually needs only two stages:

- **Attack** `A`: level rises from 0 to 1. A few milliseconds gives a crisp start without a click. Zero gives a click, which is sometimes what you want for UI.
- **Decay** `D`: level falls from 1 to 0.

The simplest version is two linear ramps, which you know from MA101 week 8 as lerps:

```
level(t) = t / A                 for 0 ≤ t < A
level(t) = 1 − (t − A) / D       for A ≤ t < A + D
level(t) = 0                     afterwards
```

Short attack and short decay make a blip. Short attack and long decay make a pluck or a bell. Long attack makes a swell, which reads as "something is coming" and is rare in feedback sounds for exactly that reason. The attack tells the player *when*, and a sluggish attack makes controls feel laggy.

## 2. Pitch contour: what the sound means

Here is the claim of this week. For short game sounds, **the direction the pitch moves carries more meaning than the waveform or the exact pitch.** Rising contours read as gain, success and upward motion. Falling contours read as loss, damage and downward motion or departure. The worked example tests that claim against three systems built decades apart.

## 3. Worked example: a pickup, a jump, a laser and a hurt from six numbers

### The hook

sfxr is a tiny sound-effect generator that Tomas Pettersson (DrPetter) wrote for the 10th Ludum Dare game jam in December 2007, so entrants could get sounds into a 48-hour game without hunting for them. Its interface is a column of buttons named for game events: pickup/coin, laser/shoot, explosion, powerup, hit/hurt, jump, blip/select. Each press rolls random parameters. Press "hit/hurt" twenty times and you get twenty different sounds, yet every one of them sounds like getting hurt. Press "powerup" and every result sounds like a reward.

How can a randomiser be that reliable? Read the preset code in the maintained browser port, jsfxr. The `hitHurt` preset picks a random start frequency but always a *negative* frequency slide. `laserShoot` also always slides down. `powerUp` and `jump` always slide *up*. `pickupCoin` adds an optional sudden jump in pitch partway through, and the jump always goes up. The randomness lives in everything except the one thing that carries the meaning.

### The model

A pitch contour with a slide and one optional jump:

```
f(t) = f0 × 2^(s × t)                      before the jump
f(t) = f0 × 2^(s × t) × 2^(n / 12)         from t_jump onward
```

- `f0` is the start frequency in Hz.
- `s` is the slide in **octaves per second**. Positive rises, negative falls. One octave is a doubling of frequency.
- `n` is the jump size in **semitones**. Twelve semitones make an octave, so a jump of `n` semitones multiplies frequency by `2^(n/12)`. You met this factor in CS101 week 14.
- `t_jump` is when the jump happens.
- `t` is time since the sound started, in seconds.

The slide is exponential, not linear. The frequency is multiplied by the same factor every second. That matches how we hear pitch, where each octave sounds like the same size of step whether it goes from 100 to 200 Hz or from 1,000 to 2,000 Hz. The total pitch change over a sound of length `T` in semitones is simply `12 × s × T + n`.

Put the contour together with a waveform and a two-stage envelope and a sound effect is six numbers: waveform, `f0`, `s`, `n` (with `t_jump`), `A` and `D`.

### Numbers you can check

Four designs, rendered at 48 kHz. The code computes the end frequency, the total change in semitones and the length. Run it with `.venv/bin/python`.

```python
import math

RATE = 48000
# name: (wave, f0 Hz, slide octaves/s, jump semitones, jump time s, attack s, decay s)
PRESETS = {
    "coin":  ("square",   1000,  0.0, 5, 0.06, 0.005, 0.25),
    "jump":  ("square",    300,  2.0, 0, 0.00, 0.010, 0.20),
    "laser": ("sawtooth", 1200, -4.0, 0, 0.00, 0.002, 0.25),
    "hurt":  ("square",    400, -3.0, 0, 0.00, 0.002, 0.20),
}

def freq_at(t, f0, slide, jump, t_jump):
    f = f0 * 2 ** (slide * t)
    return f * 2 ** (jump / 12) if jump and t >= t_jump else f

for name, (wave, f0, slide, jump, t_jump, a, d) in PRESETS.items():
    end = a + d
    f_end = freq_at(end, f0, slide, jump, t_jump)
    semis = 12 * math.log2(f_end / f0)
    print(f"{name:<5} {wave:<8} {f0:>5} Hz -> {f_end:7.1f} Hz  {semis:+5.1f} st  "
          f"{end * 1000:3.0f} ms  {round(end * RATE):5d} samples")
```

It prints:

```
coin  square    1000 Hz ->  1334.8 Hz   +5.0 st  255 ms  12240 samples
jump  square     300 Hz ->   401.4 Hz   +5.0 st  210 ms  10080 samples
laser sawtooth  1200 Hz ->   596.7 Hz  -12.1 st  252 ms  12096 samples
hurt  square     400 Hz ->   262.8 Hz   -7.3 st  202 ms   9696 samples
```

| Sound | Wave | Start | Contour | End | Change | Length |
|---|---|---|---|---|---|---|
| Coin | square | 1,000 Hz | flat, then jump +5 st at 60 ms | 1,334.8 Hz | +5.0 st | 255 ms |
| Jump | square | 300 Hz | slide +2 oct/s | 401.4 Hz | +5.0 st | 210 ms |
| Laser | sawtooth | 1,200 Hz | slide −4 oct/s | 596.7 Hz | −12.1 st | 252 ms |
| Hurt | square | 400 Hz | slide −3 oct/s | 262.8 Hz | −7.3 st | 202 ms |

Check the jump by hand. It lasts 0.21 s at +2 octaves per second, so it rises `2 × 0.21 = 0.42` octaves, which is `12 × 0.42 = 5.04` semitones. The frequency is `300 × 2^0.42 ≈ 401.4` Hz.

Notice that the coin and the jump end exactly the same pitch distance above where they started, +5 semitones, a musical interval called a **perfect fourth**. They still sound different. The coin gets there in one instant step, which sounds like a two-note chime, a discrete reward. The jump glides, which sounds like continuous motion. The shape of the contour carries the difference, not the size.

### A visual you can move

Open [`examples/w03-pitch-contour-synth.html`](../examples/w03-pitch-contour-synth.html). The left view draws the waveform you will hear, with the envelope outlined over it. The right view plots pitch in semitones against time, which turns every exponential slide into a straight line. Load "hurt" and drag the slide from −3 to +3 octaves per second without touching anything else. The left view barely changes: same wave, same envelope, same length. The right view tips from falling to rising, and the sound flips from damage to reward. Then load "coin" and set the jump to −5 semitones. The "reward" becomes a "wrong answer" buzz. The page has a blind test mode that plays two random contours and asks which is the pickup, and most people get it right from the direction alone.

### Cross-game recognition

**sfxr (2007) and jsfxr (current).** Written as parameters, sfxr's frequency slide multiplies the period by a constant factor every sample (`periodMult = 1 − ramp³ × 0.01` in jsfxr), which makes the frequency change by a constant factor per sample, an exponential slide. Its arpeggio multiplies the period once, partway through, which is our jump `n`. The presets fix the sign of the slide and jump per category and randomise the rest. That is the model's claim, turned into a tool.

**The NES audio chip (Nintendo Entertainment System, 1980s).** The console's APU has five channels: two pulse waves, a triangle, noise and a sample channel. The pulse frequency is `f = f_CPU / (16 × (t + 1))`, where `t` is an 11-bit timer value and `f_CPU` is 1.789773 MHz on NTSC machines. Each pulse channel also has a hardware **sweep unit** that repeatedly adds or subtracts a shifted copy of the period to itself. Adding `period >> S` multiplies the period by `1 + 2^−S` per step, so the frequency falls by a constant factor per step. That is the same exponential slide, built into silicon so a game could fire a falling "pew" without spending CPU time on it. With `S = 3`, each step multiplies frequency by `1 / 1.125 ≈ 0.889`, about −2 semitones per step.

The timer also shows why old hardware sounds slightly out of tune at high pitches. To play 440 Hz, `t = 1,789,773 / (16 × 440) − 1 ≈ 253.2`. The register only takes integers, so `t = 253`, which plays 440.4 Hz. At 4,000 Hz, `t` rounds to 27 and plays 3,995.0 Hz.

**Pong (Atari, 1972).** Allan Alcorn built Pong's beeps from tones he found in the game's sync generator circuit, because he had no room or knowledge for anything more elaborate. Pong has no slides at all. It separates events with different fixed pitches and lengths. That is the floor of synthesis for feedback: even without contour, distinct pitches for distinct events carry the game.

**The Web Audio API (current browsers).** `OscillatorNode.type` offers `sine`, `square`, `sawtooth` and `triangle`, the same table as section 1. `AudioParam.exponentialRampToValueAtTime` ramps a frequency exponentially, and MDN's documentation notes that exponential ramps suit frequencies because of the way the ear works. The interactive for this week, and the lab's WAV renderer, use this model directly.

Four systems across 50 years share one model. It is an oscillator whose frequency is multiplied by a constant factor per unit of time, with the direction of that factor carrying the meaning.

### Eyes-open design judgment

- **Match contour to meaning, then break the rule on purpose.** Rising for gain and falling for loss is a convention players have absorbed from decades of games. A falling pickup sound will confuse them. When you break the convention, for a cursed item that sounds like a reward and then sours, do it deliberately and with a reason you could write down.
- **Keep variation off the meaning-carrying parameter.** When you randomise a sound for variety (week 4), vary start pitch, length and waveform detail, not the sign of the slide. sfxr's presets are a good model.
- **Synthesis is a style as well as a placeholder tool.** Pure synthesised effects signal "retro" or "abstract" strongly. In a realistic game, synthesis still earns its place in UI sounds, sci-fi weapons and as layers (a synthesised sub-bass under a recorded explosion, week 4).
- **Runtime synthesis versus baked files.** Generating sounds at runtime costs almost no memory and lets parameters follow gameplay (a charge-up whose pitch tracks the charge). Baked WAVs cost memory but no CPU and are easier to review. Most games bake, and synthesise at runtime only where a sound must follow a continuous game value.
- **Harsh waveforms fatigue.** Sawtooth and square waves at high pitch are loud for their level and tiring over a long session. A sound the player hears 2,000 times an hour (a footstep, a hit marker) should be softer in tone than one heard twice an hour.

## 4. Aliasing and filters: where synthesis meets sampling

Week 2's Nyquist limit comes back here with a twist. A recording is filtered before it is sampled, so nothing above `fs / 2` gets in. A synthesised square wave computed sample by sample has no such filter. Its harmonics continue forever, and the ones above Nyquist **fold back** to wrong frequencies:

```
alias frequency = |k × f − m × fs|   for the whole number m that puts it between 0 and fs / 2
```

Take a 3,100 Hz square wave at 48 kHz. Its odd harmonics are 3,100, 9,300, 15,500 and 21,700 Hz, all below 24,000 Hz and fine. The 9th harmonic, 27,900 Hz, folds to `48,000 − 27,900 = 20,100` Hz. The 11th, 34,100 Hz, folds to 13,900 Hz. The 15th, 46,500 Hz, folds to 1,500 Hz, a tone *below* the note you asked for, at `1/15` of the fundamental's amplitude (about −23.5 dB). None of these folded frequencies are harmonics of 3,100 Hz, so they sound like a dirty, inharmonic whine, and they move in the opposite direction when the note slides.

Three practical responses:

1. **Keep harsh waveforms low.** Below about 1 kHz, the folded harmonics are weak enough that nobody notices.
2. **Use band-limited oscillators.** The Web Audio specification defines `OscillatorNode`'s basic waveforms through their Fourier series and lets browsers depart from the ideal shape to prevent aliasing. That is one reason to use it rather than writing sample values yourself in the browser. Game engines and plugins have equivalents.
3. **Oversample and filter.** Compute at a higher rate, low-pass filter, then drop back to the output rate. jsfxr computes eight sub-samples per output sample (`OVERSAMPLING = 8`) for exactly this reason.

A **low-pass filter** passes frequencies below a **cutoff** and removes those above. Sliding the cutoff down over time makes a sound "close" or muffle, which is how noise becomes an explosion that rumbles off, or how a door sound is placed in the next room. A **high-pass filter** does the opposite and thins a sound out, useful for radios and small speakers. Week 7 uses low-pass filters for distance and occlusion.

## 5. Noise: sounds without pitch

Explosions, hits, wind, rain and fire have no clear pitch. Build them from noise:

- **Explosion.** Noise, attack under 5 ms, decay 0.5 to 1.5 s, low-pass cutoff sliding from about 5 kHz down to 200 Hz across the decay.
- **Hit.** A 20 to 60 ms noise burst mixed with a short falling square or sine ("hurt" from the table) for body.
- **Footstep on gravel.** Three or four very short noise bursts 10 to 20 ms apart, band-passed. Synthesised footsteps rarely beat recorded ones, which is why week 2 recorded them.

Noise also shows that the pitch contour idea has limits. Sliding a noise filter's cutoff downward still reads as "falling" and "ending", so the direction-carries-meaning rule extends to filter cutoff as well as pitch.

## In-class activity (30 minutes)

Pairs, one laptop, headphones, the week's interactive (or sfxr.me).

1. **Build a set (15 min).** Design six sounds for a small platformer: jump, land, coin, power-up, hurt, death. Write each as its six numbers (wave, `f0`, `s`, `n` and `t_jump`, `A`, `D`), plus a noise mix or filter if you used one.
2. **Compute (5 min).** For each sound, compute the total pitch change in semitones with `12 × s × T + n`. Mark each as rising, falling or flat.
3. **Swap and guess (10 min).** Play your six sounds, in random order and unlabelled, to another pair. They name each event. Record how many they got right and which pairs they confused.

Expected output: a six-row parameter table, the rising/falling column, and the other pair's score. Confusions between sounds with the same contour direction (coin and power-up, hurt and death) are expected. Confusions across directions point to a design problem.

## Common misconceptions

- **"A slide is a straight line in hertz."** A linear slide from 200 to 1,000 Hz spends most of its time in the top octaves and sounds like it speeds up. Exponential slides sound even, which is why hardware from the NES onward implements them.
- **"Square waves are just louder sine waves."** They contain odd harmonics that sines do not, which is what makes them sound buzzy. At the same peak level a square also has 3 dB more RMS than a sine.
- **"Synthesised sounds are only for retro games."** Synthesis is how most UI, sci-fi and sub-bass layers in modern games are made, and runtime synthesis is how sounds follow continuous gameplay values.
- **"If it sounds right at one pitch, it works at every pitch."** Naive oscillators alias as pitch rises. Test synthesised sounds at the top of their pitch range.

## Check yourself

1. A laser starts at 1,600 Hz and slides at −5 octaves per second for 0.2 s. What is its end frequency, and how many semitones did it fall?
2. You want a pickup that rises exactly one octave in 150 ms by a glide rather than a jump. What slide `s` do you need? What if you want the same total change as a jump at 50 ms instead?
3. A 2,500 Hz square wave plays at 44.1 kHz. Where does its 11th harmonic fold to? Is it a harmonic of 2,500 Hz?
4. On NTSC NES hardware, what timer value `t` gets closest to 1,000 Hz, and what frequency does it actually play?
5. A designer makes the "level up" sound a long, rising sawtooth with a 400 ms attack. Players say it feels slow and the reward "arrives late". Use the envelope and contour ideas to suggest a fix.

<details>
<summary>Answers</summary>

1. `1,600 × 2^(−5 × 0.2) = 1,600 × 2^(−1) = 800` Hz. It fell one octave, 12 semitones.
2. One octave in 0.15 s means `s = 1 / 0.15 ≈ 6.67` octaves per second. For a jump instead: `s = 0`, `n = 12` semitones, `t_jump = 0.05` s.
3. `11 × 2,500 = 27,500` Hz, above Nyquist (22,050 Hz). It folds to `44,100 − 27,500 = 16,600` Hz. `16,600 / 2,500 = 6.64`, not a whole number, so it is not a harmonic and sounds inharmonic.
4. `t = 1,789,773 / (16 × 1,000) − 1 ≈ 110.9`, so `t = 111`. It plays `1,789,773 / (16 × 112) ≈ 998.8` Hz.
5. Shorten the attack to a few milliseconds so the sound starts on the event, and keep the rise in the pitch contour, which carries the "gain" meaning. A fast two-step jump (like the coin) followed by a short glide keeps the sense of growth without delaying the confirmation.

</details>

## Lab / assignment hook

[Lab 03, a tiny sound-effect synthesiser](../labs/lab03.md). Implement a phase-accumulator oscillator, the two-stage envelope and the slide-and-jump contour in standard-library Python, render your six platformer sounds to WAV, and measure them with your week 2 level functions. The six sounds go into the SFX pack as the synthesised half of your set.

## Sources

- Pettersson, T. (DrPetter), "sfxr" project page (archived copy; page last updated 14 September 2012). Written for the 10th Ludum Dare, December 2007; preset buttons for common game events; MIT licence.
- Fredricksen, E. and McCormick, C., jsfxr, `sfxr.js` (GitHub `chr15m/jsfxr`, master branch, accessed September 2026). Preset functions `pickupCoin`, `laserShoot`, `explosion`, `powerUp`, `hitHurt`, `jump`, `blipSelect`; signs of `p_freq_ramp` per preset; period multiplier `1 − ramp³ × 0.01`; `OVERSAMPLING = 8`.
- NESdev Wiki, "APU", "APU Pulse" and "APU Sweep". Five channels; `f = f_CPU / (16 × (t + 1))`, `f_CPU` = 1.789773 MHz (NTSC); sweep unit adds or subtracts the period shifted right by the shift count.
- Wikipedia, "Pong". Alcorn generated the sound effects from tones in the sync generator circuit.
- W3C, Web Audio API specification (editor's draft, accessed September 2026), section on basic waveform phase. Oscillator output may differ from the ideal waveform to prevent aliasing.
- MDN Web Docs, "OscillatorNode: type property" and "AudioParam: exponentialRampToValueAtTime() method". Waveform types; exponential ramps suit frequencies.
- Collins, K. (2008). *Game Sound*. MIT Press. Chapter 3 (course reading).

## Interactive spec: examples/w03-pitch-contour-synth.html

**Purpose.** Show that the pitch contour carries the meaning of a short sound effect. The one insight: flipping the sign of the slide (or jump) changes almost nothing in the waveform view but turns "hurt" into "reward" in the pitch view and in the ear.

**Layout.** Two linked views side by side on desktop, stacked on mobile, controls below.

- **Left, "What you hear".** The rendered waveform over the sound's length (x: time 0 to `A + D`, y: −1 to 1), drawn in `--ink-soft`, with the envelope outline `±level(t)` in `--steel`. Because the waveform is dense, draw it as a min/max band per pixel column.
- **Right, "Pitch contour".** x: time in ms, y: semitones relative to `f0` from −24 to +24 (straight lines for exponential slides). Draw the contour in `--ochre` if it ends above 0, `--blood` if below, `--ink` if flat. Label the end value, e.g. "+5.0 st".

**Model (exact).**

```
f(t) = f0 * 2^(s * t) * (t >= t_jump && n != 0 ? 2^(n / 12) : 1)
phase += f(t) / fs; phase -= floor(phase)
square: phase < 0.5 ? 1 : -1;  saw: 2*phase - 1;  triangle: 1 - 4*abs(phase - 0.5);  sine: sin(2π phase);  noise: uniform(-1, 1) from a seeded generator
level(t) = t < A ? t / A : (t < A + D ? 1 - (t - A) / D : 0)
sample = 0.5 * level(t) * wave(phase)
semitones_total = 12 * log2(f(A + D) / f0)
```

For audio playback use Web Audio `OscillatorNode` (band-limited) with `frequency.setValueAtTime(f0, t0)`, `exponentialRampToValueAtTime(f(t_jump−), t0 + t_jump)`, then `setValueAtTime(f(t_jump+), …)` and a second exponential ramp to the end; drive a `GainNode` with `linearRampToValueAtTime` for the envelope. Noise uses an `AudioBuffer` filled from the seeded generator. The waveform drawing may use the naive formulas above.

**Controls.**
- Preset buttons: coin, jump, laser, hurt (values from the lecture table).
- Waveform: segmented control sine / square / sawtooth / triangle / noise.
- `f0`: 50-4,000 Hz, logarithmic slider. `s`: −8 to +8 octaves per second, step 0.1. `n`: −12 to +12 semitones, step 1. `t_jump`: 0-300 ms. `A`: 0-200 ms. `D`: 20-1,000 ms.
- "Flip contour" button: negates `s` and `n` together.
- "Play" button (Space when focused).
- "Blind test" mode: plays two sounds with the same wave, `f0`, `A`, `D` but opposite contours, in random order, and asks "which is the pickup?". Keep a running score on the page (no storage).

**Readouts (exact).** Start and end frequency (Hz, 1 decimal), total change (semitones, 1 decimal), length (ms), samples at 48 kHz, and for square and sawtooth the number of harmonics below Nyquist at the highest frequency reached (`floor(24,000 / f_max)`).

**Test values (must match the lecture).**
- coin: 1,000 → 1,334.8 Hz, +5.0 st, 255 ms, 12,240 samples.
- jump: 300 → 401.4 Hz, +5.0 st, 210 ms, 10,080 samples.
- laser: 1,200 → 596.7 Hz, −12.1 st, 252 ms, 12,096 samples.
- hurt: 400 → 262.8 Hz, −7.3 st, 202 ms, 9,696 samples. After "flip contour": 400 → 608.8 Hz, +7.3 st.

**First screen.** The "hurt" preset loaded, with a second ghost contour in the right view showing its flipped version, captioned "Same wave, same envelope. Only the direction changed."

**Rules.** Audio starts only on user gesture; master gain capped at 0.5. Keyboard-operable controls with visible focus. Respect `prefers-reduced-motion` and `prefers-color-scheme`. Shared tokens from `templates/interactive-tokens.css`. No external audio.

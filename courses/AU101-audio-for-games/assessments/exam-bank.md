# AU101 · Exam bank: quiz, practice and crit questions

AU101 has no written exam. The grade comes from three components: the [SFX pack](sfx-pack-brief.md) (30%), the [adaptive music](adaptive-music-brief.md) assignment (30%) and the [final sound pass](final-sound-pass-brief.md) (40%). This bank has three other jobs.

- **Practice.** Work a week's questions before its lab. If you can answer them with the lecture closed, the lab will go quickly.
- **Lab quizzes.** From week 2 on, each lab opens with a 10-minute ungraded quiz of two or three questions from this bank. Usually one applies a lecture model to new numbers and one asks you to explain or critique.
- **Crit questions.** The milestone reviews and the week 15 crit of the final sound pass ask questions in this style, rewritten with the numbers from your own sounds, stems and budget sheet.

Every question is tagged with its week and one type.

- **compute**: apply a lecture model (ITD, dBFS, Nyquist, repeat chance, frame-grid timing, attenuation, stem gains, sync waits, power sums, Little's law, reading rate, memory and CPU cost) to values you have not seen before.
- **code**: say what a short piece of Python prints, and why.
- **trace**: step a system (the music director, the HDR window) through a list of events and give its log.
- **explain**: say why something behaves as it does, with a number as evidence.
- **design**: choose a technique or a value for a stated situation and justify it.
- **critique**: find what is wrong with a proposal and say how to fix it.

All numbers are invented unless a question names a game. Every game fact used here comes from the lecture of the tagged week, which cites its source and version. Every code snippet runs as shown with Python 3.13 (`.venv/bin/python`). Every number in the answers was recomputed in Python from the lectures' own models. Unless a question says otherwise, use the lectures' defaults: head radius 0.0875 m and speed of sound 343 m/s (week 1), decibels as `20 · log10` of an amplitude ratio, and `d_min = 1.0 s` for subtitles (week 13). Write your own answer before you open the solution.

---

## Week 1: What sound does in games

1. *Week 1 · compute.* Use the spherical-head model `ITD = (r / c) × (θ + sin θ)` with `θ = asin(sin a)`.
   (a) Compute the ITD in milliseconds and in samples at 48 kHz for sources at azimuth 20° and 70°.
   (b) Give the mirror azimuth behind the listener for each one.
   (c) Compare the ITD change from 0° to 20° with the change from 70° to 90°. What does the difference say about how well a listener can place a sound that is already off to the side?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 20°: 0.176 ms, 8.46 samples. 70°: 0.551 ms, 26.47 samples. (b) 160° and 110°. (c) 0° to 20° moves the ITD by 176 µs; 70° to 90° moves it by only 104 µs. The same 20° step changes the timing cue far less at the side, so direction is judged less precisely there.

(a) `r / c = 0.0875 / 343 = 0.2551 ms`. At 20°, `θ = 0.3491` rad and `sin θ = 0.3420`, so `ITD = 0.2551 × 0.6911 = 0.176 ms`, and `0.000176 × 48,000 = 8.46` samples. At 70°, `θ = 1.2217` and `sin θ = 0.9397`, so `ITD = 0.2551 × 2.1614 = 0.551 ms`, 26.47 samples.

(b) `sin 160° = sin 20°` and `sin 110° = sin 70°`, so each pair has the same lateral angle and the same ITD. That is the cone of confusion.

(c) The 90° ITD is 0.656 ms. `0.656 − 0.551 = 0.104 ms`, against `0.176 − 0 = 0.176 ms` near the front. The curve flattens toward 90° because `θ + sin θ` grows more slowly as `sin θ` levels off. A game that needs players to tell 70° from 90° should not rely on timing alone.
</details>

2. *Week 1 · code.* A programmer fakes direction on headphones by delaying the left channel by exactly 10 samples at 48 kHz. This script finds the lateral angle the spherical-head model assigns to that delay. What does it print, and at which two azimuths on the right side will a listener hear the sound?

```python
import math

R, C, RATE = 0.0875, 343.0, 48000

def itd(theta):
    return R / C * (theta + math.sin(theta))

target = 10 / RATE            # 10 samples of delay, in seconds
lo, hi = 0.0, math.pi / 2
for _ in range(60):
    mid = (lo + hi) / 2
    if itd(mid) < target:
        lo = mid
    else:
        hi = mid
print(f"ITD {target * 1000:.3f} ms, lateral angle {math.degrees(lo):.1f} deg")
```

<details>
<summary>Answer and worked solution</summary>

**Answer.** It prints `ITD 0.208 ms, lateral angle 23.7 deg`. The listener may hear the sound at about 23.7° (front right) or 156.3° (back right).

`10 / 48,000 = 0.000208 s`. The ITD grows steadily from 0 to π/2, so bisection works: each step keeps the half of the interval where the ITD crosses the target. Sixty halvings shrink the interval far below a thousandth of a degree. The mirror azimuth is `180 − 23.7 = 156.3°`. A pure delay carries no pinna cue, so the model has nothing to separate the two. The fix from the lecture is HRTF filtering, or a listener that turns with the camera so head movement breaks the tie.
</details>

3. *Week 1 · compute.* Your lab 01 audit of a horror game has 48 events. 30 rows have `job = feedback`, split into 21 confirm, 6 report and 3 forecast. 14 rows are off screen. 9 rows have mute cost 3.
   (a) Compute `off_screen_pct` and `forecast_pct_of_feedback` as the checker does (one decimal).
   (b) How many percentage points does one extra row move `off_screen_pct` in a 48-row audit, and in a 40-row one?
   (c) In one sentence each, say what the two percentages tell you about this game.

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 29.2% and 10.0%. (b) About 2.1 points at 48 rows, 2.5 at 40. (c) See below.

(a) `100 × 14 / 48 = 29.2`. The checker divides forecasts by all feedback kinds, `100 × 3 / 30 = 10.0`.

(b) One row is `100 / 48 = 2.08` points, or `100 / 40 = 2.5` at the minimum size. That is why lab 01 asks for at least 40 events: no single odd moment swings a percentage by more than a few points.

(c) Almost a third of the sounds come from things the player cannot see, so much of the game's information lives only in audio, and the 9 mute-cost-3 rows are its accessibility debt. Only one feedback sound in ten warns before something happens; for a horror game that suggests it prefers surprise to forecast, which is a design choice worth naming in the memo.
</details>

4. *Week 1 · explain.* Classify each sound by main job (feedback, space, emotion), by feedback kind where it applies, by trigger (input or state) and by diegetic or not. Then give it a mute cost from 1 to 3 with a reason.
   (a) A metallic click when you finish reloading. (b) A distant horn that sounds 5 seconds before a siege wave arrives. (c) Rain that gets muffled when you walk under a roof. (d) A low cello note under the scene when a companion dies.

<details>
<summary>Answer and worked solution</summary>

**Answer.**

(a) Feedback, confirm, input, diegetic. Mute cost 2: a muted player can watch the ammo counter, but the click tells them without looking away from the target.

(b) Feedback, forecast, state, diegetic (a horn in the world). Mute cost 3 unless there is a visual timer: it turns a surprise wave into a decision, and a muted player loses those 5 seconds.

(c) Space, state (the roof changed the acoustic), diegetic. Mute cost 1: the player can see the roof. It also confirms movement weakly.

(d) Emotion, state, non-diegetic. Mute cost 1 for information, but a muted player loses the tone of the moment. Week 13 would caption it only if the music also carries game state.
</details>

## Week 2: Recording and foley basics

5. *Week 2 · compute.* For each format give the Nyquist frequency, the dynamic range from `6.02 × N`, the bytes per second, and the size of a 90-second recording in MB (1 MB = 1,000,000 bytes).
   (a) 44,100 Hz, 16-bit, stereo. (b) 96,000 Hz, 24-bit, mono. (c) 22,050 Hz, 8-bit, mono.

<details>
<summary>Answer and worked solution</summary>

**Answer.**

| Format | Nyquist | Dynamic range | Bytes per second | 90 s |
|---|---|---|---|---|
| (a) 44.1 kHz, 16-bit, stereo | 22,050 Hz | 96.3 dB | 176,400 | 15.88 MB |
| (b) 96 kHz, 24-bit, mono | 48,000 Hz | 144.5 dB | 288,000 | 25.92 MB |
| (c) 22.05 kHz, 8-bit, mono | 11,025 Hz | 48.2 dB | 22,050 | 1.98 MB |

Bytes per second is `fs × (N / 8) × channels`. For (a), `44,100 × 2 × 2 = 176,400`, and `× 90 = 15,876,000` bytes. Format (c) is close to Doom's 11,025 Hz, 8-bit effects at twice the rate: everything above 11 kHz is gone and quiet tails carry audible hiss.
</details>

6. *Week 2 · compute.* You record a chain rattle whose content reaches 50 kHz, with a microphone specified to 30 kHz. The creature designer will play it at pitch 0.7 and 0.4.
   (a) Using `f_top_after = p × min(fs / 2, f_mic, f_source)`, give the top frequency at pitch 1.0, 0.7 and 0.4 for recordings at 48, 96 and 192 kHz.
   (b) The designer wants the full audible band (to 20 kHz) at pitch 0.5. Can any sample rate deliver that with this microphone? What would you need?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 48 kHz: 24.0, 16.8 and 9.6 kHz. 96 kHz and 192 kHz: 30.0, 21.0 and 12.0 kHz. (b) No. You need a microphone that reaches at least 40 kHz and a rate of at least 80 kHz, so 96 kHz.

(a) At 48 kHz the limit is Nyquist, 24 kHz. At 96 and 192 kHz Nyquist is 48 and 96 kHz, so the 30 kHz microphone is the limit, and 192 kHz buys nothing over 96 kHz.

(b) At pitch 0.5, 20 kHz after the shift needs `f_top ≥ 40 kHz` before it. With this microphone `f_top` is at most 30 kHz, so the best you get at pitch 0.5 is 15 kHz, at any rate. With a 40 kHz microphone, `fs / 2 ≥ 40 kHz` means `fs ≥ 80 kHz`, and the standard rate above that is 96 kHz. Spend on the microphone first.
</details>

7. *Week 2 · compute.* A creak recorded at 50 cm peaks at −30 dBFS. The room tone sits at −70 dBFS. Lab 02's spec needs peaks between −20 and −1 dBFS and at least 40 dB between the peak and the room tone floor.
   (a) What do the peak and the signal-to-noise ratio become if you move the microphone to 20 cm without touching gain?
   (b) What distance would bring the peak to −9 dBFS with no gain change? Is it a good idea?
   (c) Propose a setup that reaches a −9 dBFS peak, and say what happens to the signal-to-noise ratio.

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) Peak −22.0 dBFS, signal-to-noise ratio 48.0 dB. (b) About 4.5 cm, which is too close. (c) Work at 20 cm and add about 13 dB of input gain. The ratio stays at 48 dB.

(a) `20 × log10(50 / 20) = +7.96 dB`. The room noise does not move, so the ratio grows from 40 dB to about 48 dB. At 50 cm the take only just met the 40 dB rule.

(b) You need +21 dB: `d = 50 / 10^(21/20) = 4.46 cm`. At that range proximity effect boosts the bass, a small movement of the prop changes the level a lot, and air from the swing can thump the diaphragm.

(c) Gain amplifies the creak and the room noise by the same amount, so it does not change the acoustic signal-to-noise ratio. Only distance does. Move to a practical close distance for the ratio, then set gain for the level: `−22.0 + 13 = −9` dBFS. With 24-bit recording the converter's own noise sits far below the room's, so the gain costs nothing audible.
</details>

8. *Week 2 · critique.* A student hands in this foley session: stereo WAV at 44.1 kHz, 16-bit; footsteps recorded 1.5 m from a phone in a tiled kitchen; peaks between −3 and 0 dBFS, with three takes showing flat-topped waveforms; no room tone; files named `step1.wav` to `step14.wav`. The student plans to pitch the footsteps down an octave for a golem. List the problems in order of how hard they are to fix later, and give the fix for each.

<details>
<summary>Answer and worked solution</summary>

**Answer.** From hardest to easiest to fix later.

- **Clipping.** Three takes hit full scale with flat tops. Clipping is permanent and declipping fails on impacts. Re-record with peaks at −12 to −6 dBFS.
- **Room.** A tiled kitchen adds bright, long reflections that cannot be subtracted, and a golem in a cave will need its own reverb. Record close (15 to 40 cm) in a dead space such as a wardrobe or behind blankets.
- **Distance.** At 1.5 m the room noise is high relative to the steps. Moving to 30 cm is a factor of 5, `20 × log10(5) ≈ +14 dB` of signal-to-noise ratio for free.
- **Stereo.** A stereo footstep bakes in one position. Point sources should be mono so the engine can place them.
- **Sample rate for the pitch plan.** At 44.1 kHz and pitch 0.5, the top falls to about 11 kHz, so the golem steps sound dull. Record at 96 kHz if the microphone reaches above 20 kHz.
- **No room tone.** You cannot measure the noise floor or fill edit gaps. Record 30 seconds.
- **Names.** Use `CatID_description_initials_NN.wav`, for example `FOOTStne_golem-walk_AB_01.wav`. This is the cheapest fix and the only one that does not need a new session.
</details>

## Week 3: Synthesis for SFX

9. *Week 3 · compute.* A laser starts at 2,000 Hz and slides at −6 octaves per second. Attack is 2 ms and decay 180 ms.
   (a) What is its end frequency, and how many semitones does it fall?
   (b) At what time does it pass 1,000 Hz?
   (c) What slide would make it fall exactly one octave over its whole length?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 938.2 Hz, a fall of 13.1 semitones. (b) At 0.167 s. (c) About −5.49 octaves per second.

(a) The length is `T = 0.002 + 0.180 = 0.182 s`. `f = 2,000 × 2^(−6 × 0.182) = 2,000 × 2^(−1.092) = 938.2 Hz`. The change is `12 × s × T = 12 × (−6) × 0.182 = −13.1` semitones.

(b) 1,000 Hz is one octave down, which takes `1 / 6 = 0.167 s` at 6 octaves per second.

(c) One octave over 0.182 s: `s = −1 / 0.182 = −5.49` octaves per second. The fall still carries the "shot leaving" meaning, which is why every laser preset in jsfxr slides down.
</details>

10. *Week 3 · compute.* A naive square wave at 2,800 Hz plays at 44.1 kHz.
    (a) List its odd harmonics from the 1st to the 15th and where each one lands after folding, using `|k × f − m × fs|`.
    (b) Which folded tone lands below the fundamental, and at what level relative to it?
    (c) Is the 9th harmonic's folded tone a harmonic of 2,800 Hz?

<details>
<summary>Answer and worked solution</summary>

**Answer.**

| k | k × f (Hz) | Heard at (Hz) | Level (dB) |
|---|---|---|---|
| 1 | 2,800 | 2,800 | 0.0 |
| 3 | 8,400 | 8,400 | −9.5 |
| 5 | 14,000 | 14,000 | −14.0 |
| 7 | 19,600 | 19,600 | −16.9 |
| 9 | 25,200 | 18,900 | −19.1 |
| 11 | 30,800 | 13,300 | −20.8 |
| 13 | 36,400 | 7,700 | −22.3 |
| 15 | 42,000 | 2,100 | −23.5 |

(a) Nyquist is 22,050 Hz, so harmonics 1 to 7 are fine. From the 9th on, subtract from 44,100: `44,100 − 25,200 = 18,900`, and so on. The level of harmonic `k` is `20 × log10(1/k)`.

(b) The 15th folds to 2,100 Hz, below the 2,800 Hz note, at −23.5 dB.

(c) No. `18,900 / 2,800 = 6.75`, not a whole number, so it is inharmonic and sounds like a dirty whine. When the note slides up, the folded tones slide down. Keep harsh waveforms low, use a band-limited oscillator, or oversample and filter as jsfxr does.
</details>

11. *Week 3 · compute.* On NTSC NES hardware the pulse frequency is `f = 1,789,773 / (16 × (t + 1))` for an integer timer `t`.
    (a) What `t` comes closest to C5, 523.25 Hz? What frequency does it play, and how many cents off is it (`1200 × log2(f / 523.25)`)?
    (b) The sweep unit multiplies the period by `1 + 2^(−S)` per step. How many semitones does one step lower the pitch for `S = 1`, 2 and 4?
    (c) With `S = 2`, how many steps does a falling "pew" need to drop at least one octave?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `t = 213`, 522.71 Hz, 1.8 cents flat. (b) −7.02, −3.86 and −1.05 semitones. (c) 4 steps.

(a) `1,789,773 / (16 × 523.25) − 1 = 212.78`, which rounds to 213. Then `1,789,773 / (16 × 214) = 522.71 Hz`, and `1200 × log2(522.71 / 523.25) = −1.8` cents. That is inaudible; the error grows at high pitches, where `t` is small.

(b) The frequency factor per step is `1 / (1 + 2^(−S))`: 0.667, 0.8 and 0.941. In semitones, `12 × log2` of each: −7.02, −3.86 and −1.05.

(c) Three steps give `0.8³ = 0.512`, −11.6 semitones, just short of an octave. Four give `0.8⁴ = 0.410`, −15.5 semitones. The frequency falls by a constant factor per step, the same exponential slide as the model.
</details>

12. *Week 3 · code.* This is the lecture's contour function. What does the loop print? What sound does this contour describe?

```python
def freq_at(t, f0, slide, jump, t_jump):
    f = f0 * 2 ** (slide * t)
    return f * 2 ** (jump / 12) if jump and t >= t_jump else f

for t in (0.0, 0.05, 0.1, 0.2):
    print(t, round(freq_at(t, 500, 1.0, 7, 0.1), 1))
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
0.0 500.0
0.05 517.6
0.1 802.9
0.2 860.6
```

The slide is +1 octave per second, so before the jump `f = 500 × 2^t`: 500 Hz at 0 and `500 × 2^0.05 = 517.6` Hz at 0.05 s. At `t = 0.1` the jump applies (`t >= t_jump`), adding `2^(7/12) = 1.498`: `500 × 2^0.1 × 1.498 = 802.9` Hz. At 0.2 s, `500 × 2^0.2 × 1.498 = 860.6` Hz. A slow rise with an upward jump of a perfect fifth partway is a power-up or pickup: both parts of the contour say "gain". The condition `if jump and ...` also means a jump of 0 is skipped cleanly.
</details>

## Week 4: Layering and variation

13. *Week 4 · compute.* A footstep event has four files with weights 4, 2, 1 and 1.
    (a) What is its repeat chance `R`? Compare it with four equal weights.
    (b) What is the chance of at least one exact repeat in a run of 8 steps, for each setup?
    (c) Name a no-memory fix and a memory fix, and give `R` for each.

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `R = 22/64 = 34.4%`, against 25% for equal weights. (b) 94.8% and 86.7%. (c) Equal weights give 25%; a "never twice in a row" rule gives 0 at the file level.

(a) Probabilities 4/8, 2/8, 1/8, 1/8. `R = (16 + 4 + 1 + 1) / 64 = 0.344`.

(b) Eight steps have 7 neighbouring pairs. `1 − (1 − 0.344)^7 = 0.948` and `1 − 0.75^7 = 0.867`.

(c) The heavy file makes repeats more likely, so first flatten the weights. Then add FMOD's Shuffle or Unity's "Avoid Repeating Last", which sets the file-level repeat chance to 0. Add a small pitch range last, since pitch costs no memory.
</details>

14. *Week 4 · compute.* You may load 12 files for a sword hit. Compute `R`, the number of distinct combinations and the chance of at least one exact repeat in a 10-hit burst for: 12 whole variants; 2 layers of 6; 3 layers of 4; 4 layers of 3; 6 layers of 2. Which arrangement would you ship, and why not simply the one with the lowest `R`?

<details>
<summary>Answer and worked solution</summary>

**Answer.**

| Arrangement | Combinations | R | P(repeat in 10) |
|---|---|---|---|
| 12 whole | 12 | 8.3% | 54.3% |
| 2 × 6 | 36 | 2.8% | 22.4% |
| 3 × 4 | 64 | 1.6% | 13.2% |
| 4 × 3 | 81 | 1.2% | 10.6% |
| 6 × 2 | 64 | 1.6% | 13.2% |

Independent layers multiply: `R = Π (1 / n_i)`, and `P = 1 − (1 − R)^9`. Four layers of 3 has the lowest `R`, but it plays four voices per hit instead of three (33% more voice cost in a combo), and each extra layer is another chance of phase cancellation and mud in the low end. Going from 3 × 4 to 4 × 3 only moves the burst figure from 13.2% to 10.6%. Ship 3 × 4 with one job per layer (transient, body, tail), and add a small whole-sound pitch range if you need more.
</details>

15. *Week 4 · compute.* Doom's source gives the chainsaw a pitch offset of `8 − (random & 15)` around a normal pitch of 128. Chocolate Doom approximates the original by changing sample length by `2 − pitch / 128`.
    (a) How many outcomes does the rule have, and what is its repeat chance?
    (b) What is the pitch range in semitones? Compare with the pistol's range of about +2.3 to −1.9 semitones from the lecture.
    (c) What is the chance of at least one exact repeat in 10 chainsaw sounds?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 16 outcomes, offsets −7 to +8, `R = 1/16 = 6.25%`. (b) About +1.12 to −0.92 semitones, roughly half the pistol's 4.2-semitone spread. (c) 44.1%.

(a) `random & 15` is 0 to 15, all equally likely, so the offset runs from 8 down to −7.

(b) At pitch 136 the length factor is `2 − 136/128 = 0.9375`, so playback is `1 / 0.9375 = 1.067` times faster: `12 × log2(1.067) = +1.12` semitones. At pitch 121 the factor is `1.0547`, `12 × log2(1 / 1.0547) = −0.92` semitones.

(c) `1 − (15/16)^9 = 0.441`. The narrower range keeps the saw's identity steady, at the price of a higher repeat chance than the pistol's 1/32.
</details>

16. *Week 4 · code.* A designer invents a lopsided pitch rule: `(random & 7) − (random & 3)`. What does this print, and what is the rule's repeat chance?

```python
from collections import Counter

outcomes = Counter((a & 7) - (b & 3) for a in range(8) for b in range(4))
total = sum(outcomes.values())
r = sum((c / total) ** 2 for c in outcomes.values())
print(len(outcomes), total, max(outcomes.values()))
print(f"{r:.4f}")
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
11 32 4
0.1055
```

There are `8 × 4 = 32` equally likely pairs. The difference runs from `0 − 3 = −3` to `7 − 0 = 7`, 11 values. The counts are 1, 2, 3, 4, 4, 4, 4, 4, 3, 2, 1 for −3 to 7, a flat top with sloped sides, so the largest count is 4. `R = (1 + 4 + 9 + 16 × 5 + 9 + 4 + 1) / 1024 = 108 / 1024 = 0.1055`. The rule also skews upward: 7 of its 11 outcomes are above 0, so the sound drifts sharp on average (the mean offset is `3.5 − 1.5 = +2` steps).
</details>

17. *Week 4 · explain.* Three files play in three modes: uniform random with no memory, FMOD's Shuffle (no item twice in a row, three or more items), and Unity's Shuffle as the lecture describes it (a bag that plays every clip before any repeats, then refills without memory of the last pick).
    (a) Give the long-run file-level repeat chance for each.
    (b) Which mode allows the pattern A B A B A B, and which never can?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) Uniform: 1/3 = 33.3%. FMOD Shuffle: 0. Unity bag: 1/9 = 11.1%. (b) FMOD Shuffle allows A B A B. A bag of three can never play A B A B inside a cycle.

(a) Inside one bag of `n` items there are `n − 1` neighbouring pairs and none repeat. The boundary pair (last of one bag, first of the next) repeats with probability `1/n`, since the new bag's first item is uniform. That is one repeat chance per `n` pairs, so `R = (1/n) / n = 1/n²`, which is 1/9 for three files.

(b) "Not twice in a row" only forbids the same neighbour, so A B A B is legal and can sound like a two-step loop. Within one bag each file appears once, so A cannot return until C has played. The bag's failure is different: the last item of each bag is predictable. Pick the failure you mind least, as the lecture says.
</details>

## Week 5: Implementation in engine

18. *Week 5 · compute.* A 700 rpm weapon (one shot every 85.7 ms).
    (a) With a reset cooldown, what rate does it fire at 60, 144 and 240 fps?
    (b) With a carry cooldown at 60 fps, list the first seven gaps. Why does the pattern repeat every seven shots?
    (c) A player on a 60 Hz monitor says the weapon feels weaker than on stream. Is that plausible?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 600 rpm, 664.6 rpm and 685.7 rpm. (b) 100.0, 83.3, 83.3, 83.3, 83.3, 83.3, 83.3 ms. (c) Yes: 14% fewer shots per minute at 60 fps than designed.

(a) `T / Δ` is 5.14 frames at 60 fps, 12.34 at 144 and 20.57 at 240. Rounded up: 6, 13 and 21 frames, so gaps of 100.0, 90.3 and 87.5 ms, and `60 / gap` gives the rates. The error is 14.3%, 5.1% and 2.0%.

(b) Shot `k` fires at `ceil(k × 5.143) × 16.67 ms`: frames 0, 6, 11, 16, 21, 26, 31, 36. Seven periods are `7 × 85.71 = 600 ms`, exactly 36 frames, so the pattern of one 6-frame gap and six 5-frame gaps repeats. The average is exactly 700 rpm.

(c) Under a reset cooldown the damage per second falls with the rate. The fix is a carry cooldown for gameplay and audio-clock scheduling for the sound, so both agree.
</details>

19. *Week 5 · compute.* (a) A game runs at 30 fps, mixes in 256-sample chunks at 48 kHz, and its output latency is 20 ms. What is the worst-case delay from an event to the speaker?
    (b) A character with a 0.7 m stride walks at 3 m/s for 2 s, then sprints at 6 m/s for 1 s. How many steps does the distance method play? How many would a 0.5 s timer play?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) About 58.7 ms. (b) 17 steps with 0.1 m carried over; the timer plays 6.

(a) Up to one frame to notice the event, `1000 / 30 = 33.3 ms`; up to one chunk before the mix picks it up, `256 / 48,000 = 5.3 ms`; then 20 ms of output latency. `33.3 + 5.3 + 20 = 58.7 ms`. The frame dominates, so at 30 fps a faster audio device barely helps.

(b) Distance is `3 × 2 + 6 × 1 = 12 m`, and `12 / 0.7 = 17.14`, so 17 steps with 0.1 m left in the accumulator. The timer plays one step per 0.5 s over 3 s, 6 steps, and during the sprint the feet land 8.6 times per second while only 2 steps per second are heard.
</details>

20. *Week 5 · code.* What does each line print? Which one would make a carry cooldown invent a late shot?

```python
import math
from fractions import Fraction

print(math.ceil(3 * 0.1 / (1 / 30)))
print(3 * 0.1 / (1 / 30))
print(math.ceil(3 * Fraction(1, 10) / Fraction(1, 30)))
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
10
9.000000000000002
9
```

Shot 3 of a 600 rpm gun at 30 fps is due at exactly 9 frames. In floats, `0.1` and `1/30` are not exact, and the division comes out a hair above 9, so `ceil` returns 10 and the shot fires one frame (33.3 ms) late. With `Fraction` the division is exactly 9. This is the float trap the lecture and lab 05 test for. Integer ticks or fractions keep every frame count honest.
</details>

21. *Week 5 · compute.* A designer uses Unity's `PlayScheduled` with a lookahead `L = 0.12 s` and schedules a whole 30-round magazine of a 900 rpm weapon when the trigger is pressed at `t = 0`.
    (a) The player releases at 0.4 s. How many shots have played, and how many more will play if the code does nothing?
    (b) The code switches to a window of the next 2 shots, refilled every frame. What is the longest the sound can run on after release?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 5 played, 25 more would play. (b) At most two more shots, about 133 ms of overrun, unless the scheduled sources are stopped.

(a) `T = 60 / 900 = 66.7 ms`, so shots are at `0.12 + 0.0667k`: 0.120, 0.187, 0.253, 0.320 and 0.387 s are before 0.4 s. The sixth is at 0.453 s. That leaves 25 of 30.

(b) With a 2-shot window, at most two shots are ever scheduled ahead, so release can be followed by at most `2 × 66.7 = 133 ms` of shots. Keep handles and stop any source scheduled after the release time to bring that to zero.
</details>

## Week 6: Middleware events and parameters

22. *Week 6 · compute.* Use SuperTuxKart's rule `pitch = 0.6 + 0.35 × (0.9 f + 3 × fmod(f, 0.333334))`.
    (a) Compute the pitch at `f = 0.1` and `f = 0.95`. How many semitones apart are they?
    (b) Compute the pitch just before and just after the gear-2-to-3 shift (`f = 0.6666` and `0.667`) and the size of the drop in semitones.

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 0.7365 and 1.1967, 8.4 semitones apart. (b) 1.1599 and 0.8105, a drop of 6.2 semitones.

(a) At 0.1, `fmod = 0.1`, gears `= 0.3`, pitch `= 0.6 + 0.35 × (0.09 + 0.3) = 0.7365`. At 0.95, `fmod = 0.95 − 0.666668 = 0.283332`, gears `≈ 0.85`, pitch `= 0.6 + 0.35 × (0.855 + 0.85) = 1.1967`. `12 × log2(1.1967 / 0.7365) = 8.4`.

(b) Just before, gears ≈ 0.9998 and pitch 1.1599. Just after, gears ≈ 0.001 and pitch 0.8105. `12 × log2(1.1599 / 0.8105) = 6.2` semitones. That drop is the fake gear change the physics never had.
</details>

23. *Week 6 · compute.* Engine loops are recorded at 1,700 and 2,400 RPM.
    (a) At 2,000 RPM, compute `t`, both equal-power gains, both pitch shifts in semitones, and the total level a linear fade would give.
    (b) Where is the midpoint of a log-spaced crossfade, and what is each loop's shift there?
    (c) Would this pair pass lab 06's rule of at most ±6 semitones on any audible loop?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `t = 0.429`; gains 0.782 and 0.623; shifts +2.81 and −3.16 semitones; linear fade −2.92 dB. (b) About 2,020 RPM, ±2.98 semitones. (c) Yes.

(a) `t = (2,000 − 1,700) / 700 = 0.4286`. `cos(0.4286 × 90°) = 0.782`, `sin(...) = 0.623`. `12 × log2(2,000 / 1,700) = +2.81` and `12 × log2(2,000 / 2,400) = −3.16`. Linear gains are 0.571 and 0.429, power `0.327 + 0.184 = 0.510`, which is `10 × log10(0.510) = −2.92 dB`.

(b) `√(1,700 × 2,400) = 2,019.9` RPM. The ratio 2,400 / 1,700 is 5.97 semitones, so each loop is shifted by half, 2.98.

(c) The worst shift anywhere between the two loops is the full 5.97 semitones, at the far end of each loop's fade, where its gain is already 0. Every audible shift is under 6.
</details>

24. *Week 6 · compute.* An RPM parameter runs from 800 to 6,800. The seek modulator is asymmetric: 1.0 range/s up and 0.25 range/s down.
    (a) How long does the sound take to rise from 1,500 to 6,000 RPM? To fall back?
    (b) The player hits a wall at full speed. How long does the sound lag behind the physics? Is that acceptable here?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) Rise 0.75 s, fall 3.0 s. (b) Up to 3.0 s on the way down, which is acceptable for a spin-down and wrong for an impact.

(a) The range is 6,000 RPM. Up: `1.0 × 6,000 = 6,000` RPM per second, so 4,500 RPM take 0.75 s. Down: 1,500 RPM per second, so 3.0 s.

(b) The physics speed drops to 0 at once and the engine note takes 3 s to follow. A slow fall is believable for an engine running down, but a crash also needs an immediate cue. Play a one-shot impact event, and consider a separate fast-down seek (or a snapshot) for collisions. Seek adds lag equal to distance divided by rate.
</details>

25. *Week 6 · compute.* Two copies of the same music stem, perfectly aligned, are crossfaded.
    (a) What is the total level at `t = 0.5` with equal-power gains? With linear gains?
    (b) At `t = 0.25`?
    (c) Which curve should you use here, and which between two different recordings?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) Equal-power +3.01 dB, linear 0 dB. (b) Equal-power +2.32 dB, linear 0 dB. (c) Linear for identical aligned material, equal-power for different recordings.

(a) Identical aligned signals add in amplitude. Equal-power gives `0.707 + 0.707 = 1.414`, which is `20 × log10(1.414) = +3.01 dB`. Linear gives `0.5 + 0.5 = 1`, 0 dB.

(b) `cos(22.5°) + sin(22.5°) = 0.924 + 0.383 = 1.307`, +2.32 dB. Linear is always 1.

(c) The equal-power curve assumes powers add, which is true only for unrelated signals. For two versions of one aligned stem, the bump would be heard as a swell in the middle of every fade.
</details>

26. *Week 6 · critique.* A team's event contract for footsteps reads: "Event `event:/Player/Footstep`, one-shot. Surface is a Wwise **state** with values Stone, Grass, Wood, set by the player controller when the player changes surface. RPM: n/a. Bank: Master." Find the problems and rewrite the relevant fields.

<details>
<summary>Answer and worked solution</summary>

**Answer.** Two problems.

- **Surface as a state.** A Wwise state is game-wide, so when the player steps onto grass, every NPC's footsteps also switch to grass. Surface belongs to each game object: make it a **switch** (`SetSwitch` with the game object), or a labeled parameter per instance in FMOD. Each character sets its own surface in its step function.
- **Bank.** The master bank holds the mixer and routing and must stay loaded. The FMOD manual advises against putting events in it except in tiny projects. Put footsteps in a bank loaded with the character, for example `Characters`, and write when it loads.

A fixed contract row: event `event:/Player/Footstep`, one-shot, started and released per step; switch `Surface` = Stone, Grass or Wood, set per game object by the step function; bank `Characters`, loaded with the level; owner: sound design for content and variation, gameplay for step timing and surface.
</details>

## Week 7: Spatial audio and attenuation

27. *Week 7 · compute.* (a) An inverse curve has `r = 2 m`. Give the level at 5 m, 20 m and 50 m, and the distance where it reaches −30 dB.
    (b) Using the Web Audio inverse model `ref / (ref + f × (max(d, ref) − ref))` with `ref = 1`, compare the gain at 9 m for rolloff factor 0.5 and 1.

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) −7.96 dB, −20.0 dB, −27.96 dB; −30 dB at 63.2 m. (b) With `f = 0.5`, 0.2 (−14.0 dB). With `f = 1`, 1/9 (−19.1 dB).

(a) `L = −20 × log10(d / 2)`. At 5 m, `−20 × log10(2.5) = −7.96`. At 20 m, −20.0. At 50 m, `−20 × log10(25) = −27.96`. Solving `−30 = −20 × log10(d / 2)` gives `d = 2 × 10^1.5 = 63.2 m`.

(b) `1 / (1 + 0.5 × 8) = 0.2`, and `1 / (1 + 8) = 0.111`. Halving the rolloff factor makes the sound 5.1 dB louder at 9 m. A smaller factor stretches the curve, which suits large outdoor sounds.
</details>

28. *Week 7 · compute.* Compare a linear curve with `r = 1 m`, `R = 50 m` and an inverse curve with `r = 1 m`.
    (a) Where is each 6 dB down? Where is each 40 dB down?
    (b) Give both levels at 13 m.
    (c) Which curve would a player find easier for judging whether an enemy is at 8 m or 16 m, and why?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) Inverse: −6 dB at 2.0 m, −40 dB at 100 m. Linear: −6 dB at 25.5 m, −40 dB at 49.5 m. (b) Linear −2.4 dB, inverse −22.3 dB. (c) The inverse curve.

(a) Inverse: `g = 0.5` at `d = 2`, `g = 0.01` at `d = 100`. Linear: `g = 1 − (d − 1) / 49`, so `g = 0.5` at `d = 25.5` and `g = 0.01` at `d = 1 + 0.99 × 49 = 49.5`.

(b) Linear `1 − 12/49 = 0.755`, −2.4 dB. Inverse `1/13`, −22.3 dB.

(c) The inverse curve drops 6 dB for every doubling, so 8 m and 16 m are always 6 dB apart. The linear curve spends most of its range within a few dB of full level and then collapses. It is honest about range, not about distance.
</details>

29. *Week 7 · compute.* The listener is at the origin, facing along `(1, 1) / √2`, so its right vector is `(1, −1) / √2`. An emitter is at `(−2, 4)`.
    (a) Compute the pan position `p` and both equal-power gains.
    (b) Apply an inverse curve with `r = 1 m`. What are the final left and right gains?
    (c) Find the mirror position behind the listener that gives the same `p`.

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `p = −0.949`, left 0.999, right 0.040. (b) Left 0.223, right 0.009. (c) `(−4, 2)`.

(a) Distance `√(4 + 16) = 4.472`, so `u = (−0.447, 0.894)`. `p = u · right = (−0.447 − 0.894) / √2 = −0.949`, almost hard left. `a = (p + 1) / 2 = 0.0257`, left `cos(0.0257 × 90°) = 0.999`, right `sin(...) = 0.040`.

(b) `g = 1 / 4.472 = 0.224` (−13.0 dB). Multiply: `0.224 × 0.999 = 0.223` and `0.224 × 0.040 = 0.009`.

(c) Reflect the emitter across the listener's left-right axis. Its component along the facing is `(−2 + 4) / √2 = 1.414`; subtract twice that along the facing: `(−2, 4) − 2 × 1.414 × (0.707, 0.707) = (−4, 2)`. Its facing component is −1.414, so it is behind, yet `p` is the same −0.949. Stereo panning cannot tell them apart.
</details>

30. *Week 7 · compute.* A third-person camera sits 8 m behind the character. An enemy stands 3 m in front of the character, on the camera's line of sight. The curve is inverse with `r = 1 m`. By how many dB does a listener on the camera underestimate the enemy's level, compared with a listener on the character? What does FMOD offer to fix it?

<details>
<summary>Answer and worked solution</summary>

**Answer.** 11.3 dB. FMOD's `setListenerAttributes` takes an attenuation position, so distance can come from the character while panning comes from the camera.

From the character, `20 × log10(1/3) = −9.5 dB`. From the camera the enemy is `8 + 3 = 11 m` away, `20 × log10(1/11) = −20.8 dB`. The gap is `20 × log10(11 / 3) = 11.3 dB`. The enemy sounds almost four times as far away as it is, which breaks every range the designer tuned for gameplay.
</details>

31. *Week 7 · design.* In a stealth game, guard footsteps must stay above −30 dB out to 15 m (so the player gets warning) and be silent from 25 m (so the player cannot track guards across the level). With `r = 1 m`, which curves meet both rules? Give parameters and compare the level at 10 m.

<details>
<summary>Answer and worked solution</summary>

**Answer.** The inverse curve fails the silence rule. A linear curve with `R` between 15.5 m and 25 m works. A tapered curve with `R = 25 m` also works, and it keeps an honest distance cue up close. Prefer the tapered one.

The inverse curve reaches −30 dB at `10^1.5 = 31.6 m` and never goes silent.

Linear: −30 dB means `g = 0.0316`, which happens at `d = 1 + 0.968 (R − 1)`. That is at least 15 m when `R ≥ 15.5`, and silence from 25 m needs `R ≤ 25`. With `R = 20` the crossing is at 19.4 m, and at 10 m the level is only −5.6 dB.

Tapered (the smaller of the inverse gain and the squared linear gain) with `R = 25`: at 15 m, `min(−23.5, −15.2) = −23.5 dB`; at 20 m, −27.3 dB; silent at 25 m. At 10 m it is −20.0 dB, 14 dB below the linear curve, and it keeps the 6 dB-per-doubling cue that tells the player how close the guard is. The range is a gameplay rule; write both numbers into the design document.
</details>

## Week 8: Adaptive music: vertical layering

32. *Week 8 · compute.* Five equally loud, uncorrelated stems: a bed plus stems with thresholds 0.15, 0.4, 0.65 and 0.85, all with `w = 0.15`. Give every stem gain and the level `10 × log10(Σ g²)` at `x = 0.5`, 0.75 and 1.0.

<details>
<summary>Answer and worked solution</summary>

**Answer.**

| x | Gains (bed, 0.15, 0.4, 0.65, 0.85) | Level |
|---|---|---|
| 0.5 | 1, 1, 0.667, 0, 0 | +3.88 dB |
| 0.75 | 1, 1, 1, 0.667, 0 | +5.37 dB |
| 1.0 | 1, 1, 1, 1, 1 | +6.99 dB |

At 0.5 the second stem is full (`0.5 ≥ 0.3`), the third is at `(0.5 − 0.4) / 0.15 = 0.667`, and the power is `1 + 1 + 0.444 = 2.444`, which is +3.88 dB. At 1.0 five full stems give `10 × log10(5) = 6.99 dB`.
</details>

33. *Week 8 · compute.* Use the lecture's four stems (bed, drums `a = 0.2`, bass `a = 0.45`, lead `a = 0.7`, all `w = 0.2`). The smoother has `up_rate = 0.4` and `down_rate = 0.08` per second. The target jumps from 0 to 0.9 at `t = 0` and drops to 0.2 at `t = 4 s`.
    (a) Give the smoothed `x` at 1, 6 and 10 s, and when it reaches 0.9 and 0.2.
    (b) When does each stem start and finish fading out?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `x = 0.4` at 1 s, 0.74 at 6 s, 0.42 at 10 s. It reaches 0.9 at 2.25 s and 0.2 at 12.75 s. (b) Lead from 4.0 to 6.5 s, bass from 7.1 to 9.6 s, drums from 10.25 to 12.75 s.

(a) Rising at 0.4 per second, 0.9 takes 2.25 s. Falling from 0.9 at 0.08 per second: at 6 s, `0.9 − 0.16 = 0.74`; at 10 s, `0.9 − 0.48 = 0.42`; 0.2 is reached after `0.7 / 0.08 = 8.75 s`, at 12.75 s.

(b) Each stem is full at `a + 0.2` and silent at `a`. The lead is full at 0.9, so it starts fading at once and is silent at 0.7, `0.2 / 0.08 = 2.5 s` later. The bass fades between 0.65 and 0.45, reached at `4 + 0.25/0.08 = 7.125 s` and `4 + 0.45/0.08 = 9.625 s`. The drums fade between 0.4 and 0.2, at 10.25 s and 12.75 s. The target settles at 0.2, exactly the drums' threshold, so they end at gain 0. The combat music takes almost nine seconds to empty out, which is the slow release doing its job.
</details>

34. *Week 8 · compute.* Six equally loud, uncorrelated stems are all full at `x = 1`.
    (a) How much louder is that than the bed alone?
    (b) What gain must every stem get so full intensity matches the bed?
    (c) The designer wants full intensity to be exactly 3 dB louder than the bed. What gain now?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) +7.78 dB. (b) 0.408, which is −7.78 dB. (c) 0.577, which is −4.77 dB.

(a) `10 × log10(6) = 7.78 dB`.

(b) Power must be 1: `6 g² = 1`, `g = 1 / √6 = 0.408`.

(c) Power 2 (+3.01 dB): `6 g² = 2`, `g = √(1/3) = 0.577`. The player keeps a small loudness cue for escalation while the stems leave room for combat effects.
</details>

35. *Week 8 · critique.* A composer delivers six stems for a layered combat track. The pad and bass loop every 8 bars, the drums every 12. Each stem is driven by its own game parameter (enemies near, health, combo, boss phase, weather, time of day). What goes wrong, and how many mixes must someone listen to before shipping? What would you change?

<details>
<summary>Answer and worked solution</summary>

**Answer.** The loops drift apart harmonically and only line up every 24 bars, and six independent parameters produce 64 reachable mixes.

With an 8-bar and a 12-bar loop, after 8 bars the pad restarts while the drums are in bar 9, and the two only realign after `lcm(8, 12) = 24` bars. Every stem must share one loop length or divide it evenly. With independent parameters every on/off combination can occur: `2^6 = 64` mixes, each of which must sound finished. Drive the stems from one intensity value with ordered thresholds, which leaves 6 combinations to check. Handle weather and time of day as separate music states (week 9) or as ambience, not as stems of the combat track.
</details>

## Week 9: Horizontal re-sequencing and stingers

36. *Week 9 · compute.* Music in 3/4 at 96 BPM starts at `t = 0`.
    (a) Give the length of a beat, a bar and a 4-bar phrase.
    (b) A transition request arrives at `t = 10.0 s`. When is it served, and how long is the wait, for each unit?
    (c) For the bar unit, what are the average wait and the share of requests that wait more than 1 s?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 0.625 s, 1.875 s, 7.5 s. (b) Beat 10.0 s (wait 0), bar 11.25 s (1.25 s), phrase 15.0 s (5.0 s). (c) 0.94 s average, 46.7% over 1 s.

(a) A beat is `60 / 96 = 0.625 s`; a bar is 3 beats; a phrase is 4 bars.

(b) `10.0 / 0.625 = 16` exactly, so the beat unit serves at once (the `ceil` in `next_sync` returns 16, and the 1e-9 tolerance protects this case from float noise). `ceil(10 / 1.875) = 6`, so 11.25 s. `ceil(10 / 7.5) = 2`, so 15.0 s.

(c) Average `U / 2 = 0.9375 s`. `P(wait > 1) = 1 − 1 / 1.875 = 0.467`.
</details>

37. *Week 9 · compute.* A 16-bar explore loop at 128 BPM in 4/4 has composer-marked exit points at the ends of bars 4, 6, 12 and 16. Requests arrive at uniformly random times.
    (a) What are the gaps between exit points, the average wait and the worst wait?
    (b) Compare with a plain 4-bar phrase grid at the same tempo.

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) Gaps 7.5, 3.75, 11.25 and 7.5 s; average 4.22 s; worst 11.25 s. (b) The grid gives 3.75 s average and 7.5 s worst.

(a) A bar is `4 × 60 / 128 = 1.875 s`, and the loop is 30 s. The points sit at 7.5, 11.25, 22.5 and 30 s. A request lands in a gap of length `g` with probability `g / 30` and then waits `g / 2` on average, so the average is `Σ g² / (2 × 30) = (56.25 + 14.06 + 126.56 + 56.25) / 60 = 4.22 s`.

(b) A regular 7.5 s grid gives `7.5 / 2 = 3.75 s`. The hand-placed points cost about half a second on average and 3.75 s in the worst case, all from the one long gap between bars 6 and 12. Add a point in that stretch, or cover it with a stinger.
</details>

38. *Week 9 · trace.* Use the lecture's transition matrix (explore to combat: bar; combat to explore: phrase; explore to boss: beat; combat to boss: bar; boss to victory: beat; victory to explore: phrase; anything else: bar) at 120 BPM in 4/4, starting in explore. The director advances any due switch before it handles each event. The game sends:

```
 2.2  state combat
 2.9  state explore
 3.1  state combat
 7.6  state boss
 7.7  stinger roar
15.2  state victory
15.3  state explore
```

Give the director's log. What does the player never hear, and what should the game code change?

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
 4.00  switch   explore  combat
 8.00  stinger  roar
 8.00  switch   combat   boss
16.00  switch   boss     explore
```

The player never hears the victory music.

At 2.2 s combat is pending for the next bar, 4.0 s. At 2.9 s explore is the current state, so the pending switch is cancelled. At 3.1 s combat is pending again for 4.0 s, and it happens. At 7.6 s combat to boss uses the bar unit, 8.0 s. The roar stinger at 7.7 s lands on the next beat, also 8.0 s. At 15.2 s boss to victory uses the beat unit, 15.5 s. At 15.3 s explore arrives before that switch, and a newer request replaces the pending one: boss to explore falls back to the default bar, 16.0 s. The fanfare is thrown away.

The director did what its rules say. The game sent "explore" 0.1 s after "victory". The game should wait until the victory switch has happened (or until the fanfare ends) before it asks for explore. With explore sent at 18.0 s instead, the log shows `15.50 switch boss victory` and `24.00 switch victory explore`.
</details>

39. *Week 9 · design.* An enrage event in a 140 BPM, 4/4 boss track must be answered musically within 0.75 s for at least 90% of requests. Which sync units pass? What would you do if the composer insists the switch lands on a bar?

<details>
<summary>Answer and worked solution</summary>

**Answer.** Only the beat unit passes. With a bar-quantized switch, fire a beat-quantized enrage stinger.

`P(wait ≤ 0.75) = 0.75 / U` must be at least 0.9, so `U ≤ 0.833 s`. A beat is `60 / 140 = 0.429 s`, which passes (every request is answered within 0.43 s). A bar is 1.714 s, which answers only `0.75 / 1.714 = 43.75%` in time. A stinger on the next beat answers the event at once and lets the switch wait for the bar, where it sounds musical.
</details>

## Week 10: Mixing, ducking and priority

40. *Week 10 · compute.* Four unrelated sounds play at −12, −15, −18 and −24 dBFS.
    (a) What is the combined level, and how much headroom is left below 0 dBFS?
    (b) How much does the −24 dBFS sound add to the total? What is that effect called?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) −9.41 dBFS, 9.4 dB of headroom. (b) About 0.15 dB. The quieter sound is masked.

(a) `10 × log10(10^−1.2 + 10^−1.5 + 10^−1.8 + 10^−2.4) = 10 × log10(0.1148) = −9.41 dBFS`.

(b) Without it the sum is −9.56 dBFS, so it adds 0.15 dB. The loud sounds cover it, and the ear struggles to pick it out: masking. If it carries information, it needs priority, a duck on the others, or a higher level by importance, not hope.
</details>

41. *Week 10 · compute.* An HDR bus has `T = 0`, `W = 40 dB` and `r = 25 dB/s`. A scene holds gunfire at +15, a voice at +5, rain at −20 and insects at −28. A blast at +50 plays from 0 to 0.3 s.
    (a) Give every sound's output in dBFS before the blast. Which are culled?
    (b) After the blast ends, how long is each sound deaf, and when does the window top return to 15?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) Gunfire 0, voice −10, rain −35, insects culled (−43). (b) Gunfire never drops out; voice 0.2 s (back at 0.5 s); rain 1.2 s (back at 1.5 s); insects stay culled; the top reaches 15 at 1.7 s.

(a) The top sits on the gunfire at 15. Anything below `15 − 40 = −25` is culled. `−28 − 15 = −43`, so the insects are out before any blast.

(b) Deaf time is `(P − (L + W)) / r`. Gunfire: `50 − 55 < 0`, never. Voice: `(50 − 45) / 25 = 0.2 s`. Rain: `(50 − 20) / 25 = 1.2 s`. The formula would give the insects 1.52 s, but the window only falls to the gunfire's 15, never to the 12 the insects need, so they stay culled as long as the gunfire plays. The top falls 35 dB at 25 dB/s, `35 / 25 = 1.4 s`, and reaches 15 at 1.7 s. If the insects matter, raise their in-game level by importance.
</details>

42. *Week 10 · compute.* Dialogue ducks music by `D = 9 dB` with `t_a = 0.15 s` and `t_r = 1.2 s`, using the lecture's straight-line model.
    (a) What are the attack and release rates in dB per second?
    (b) Two lines are 0.6 s apart. How far does the music recover in the gap?
    (c) What is the shortest release time for which the music recovers no more than 2 dB in that gap?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 60 dB/s and 7.5 dB/s. (b) 4.5 dB, to −4.5 dB. (c) 2.7 s.

(a) `9 / 0.15 = 60` and `9 / 1.2 = 7.5`.

(b) `7.5 × 0.6 = 4.5 dB`, so the music climbs from −9 to −4.5 dB and is pushed down again: an audible swell between lines.

(c) The rate must be at most `2 / 0.6 = 3.33 dB/s`, so `t_r ≥ 9 / 3.33 = 2.7 s`. The alternative is to hold the key active across the whole conversation.
</details>

43. *Week 10 · compute.* Three voices remain for combat sounds. Priority falls with distance: `p_eff = p − 25 × min(d, 50) / 50`.

| Request | Base p | Distance | Started at |
|---|---|---|---|
| Boss tell | 95 | 25 m | 0.0 s |
| Your heal | 80 | 0 m | 0.4 s |
| Ally A's spell | 65 | 8 m | 0.2 s |
| Ally B's spell | 65 | 8 m | 0.5 s |
| Enemy footsteps | 70 | 30 m | 0.3 s |
| Torch loop | 30 | 2 m | 0.0 s |

(a) Compute every `p_eff`. Which three play if ties keep the oldest? If they keep the newest?
(b) This is a PvP battleground and the footsteps belong to an enemy flanking you. Critique the table.

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 82.5, 80, 61, 61, 55, 29. Boss tell, your heal and Ally A (oldest) or Ally B (newest). (b) The enemy footsteps lose to allies' spells because of the distance offset.

(a) Boss `95 − 25 × 25/50 = 82.5`. Heal 80. Allies `65 − 25 × 8/50 = 61`. Footsteps `70 − 25 × 30/50 = 55`. Torch `30 − 1 = 29`. The allies tie at 61; keep-oldest picks A (0.2 s), keep-newest picks B (0.5 s). The torch should go virtual rather than be killed, so it can resume.

(b) In PvP the flanker is the most dangerous sound in the scene, and the distance offset pushes it below cosmetic ally spells. Give enemy footsteps within a threat radius a higher base priority or no distance offset, and consider a duck on ally spells while an enemy is within footstep range. This is the Overwatch "Play by Sound" tension: importance, not loudness or distance, should decide.
</details>

## Week 11: UI sound design

44. *Week 11 · compute.* A streak ladder uses `[0, 2, 4, 7, 9, 12, 14, 16]` semitones from `f0 = 440 Hz` and resamples a 250 ms chime.
    (a) What frequency do steps 6 and 8 play, and how long does the chime last at step 8?
    (b) A streak reaches 10 events. What does step 10 play in cap mode and in wrap mode?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 880.0 Hz and 1,108.7 Hz; 99.2 ms. (b) Cap: 1,108.7 Hz. Wrap: 493.9 Hz.

(a) Step 6 is +12 semitones, `440 × 2 = 880 Hz`. Step 8 is +16, `440 × 2^(16/12) = 1,108.7 Hz`. Resampling at a ratio of `2^(16/12) = 2.52` shortens the chime to `250 / 2.52 = 99.2 ms`.

(b) Cap holds the last entry, +16. Wrap uses `(10 − 1) mod 8 = 1`, the second entry, +2 semitones: `440 × 2^(2/12) = 493.9 Hz`. The wrap drop sounds like a reset the player did not earn. Decide on purpose.
</details>

45. *Week 11 · code.* A streak should reset only when the gap is longer than 0.6 s, so a gap of exactly 0.6 s keeps the streak going. What does this print, and what did the designer intend?

```python
T_RESET = 0.6
times = [0, 0.5, 1.1, 1.4, 2.1, 2.3]

steps, n, prev = [], 0, None
for t in times:
    n = n + 1 if prev is not None and t - prev <= T_RESET else 1
    steps.append(n)
    prev = t
print(steps)
```

<details>
<summary>Answer and worked solution</summary>

**Answer.** It prints `[1, 2, 1, 2, 1, 2]`. The intended result is `[1, 2, 3, 4, 1, 2]`.

The gaps are 0.5, 0.6, 0.3, 0.7 and 0.2 s. The only real reset is the 0.7 s gap. But `1.1 − 0.5` is `0.6000000000000001` in floating point, which is greater than 0.6, so the streak breaks at the third event. That also restarts the count before the 0.3 s gap. Store times in integer milliseconds (`1100 − 500 <= 600` is exact), or compare with a tolerance (`t - prev <= T_RESET + 1e-9`). Players hear the bug as a ladder that drops for no reason, the "you lost it" message sent when they did not.
</details>

46. *Week 11 · compute.* (a) Hover sounds of 30 ms fire 45 times a minute during a 90-minute session. How many plays, and how many seconds of hover sound, per session?
    (b) A 1.5 s loot-win jingle fires 6 times a minute in a 25-minute dungeon. How many seconds of jingle per run? Propose a change.

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 4,050 plays, 121.5 s. (b) 225 s, almost four minutes.

(a) `45 × 90 = 4,050`, and `4,050 × 0.030 = 121.5 s`. That is why hovers are short, soft (around −30 dBFS) and low in high-frequency content.

(b) `6 × 25 = 150` plays, `150 × 1.5 = 225 s`. An event that frequent is not rare, so it should get a small signal: a 100 to 200 ms confirm for ordinary wins, and the full jingle only for rare quality, on the "the more often, the smaller" rule.
</details>

47. *Week 11 · compute.* A console build mixes 480-sample buffers at 48 kHz with three buffers queued. An auction-house purchase needs a server round trip of 120 ms.
    (a) What is the buffer latency in ms and in 60 fps frames?
    (b) Roughly when can "purchase confirmed" play after the click? What plays before that?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 30 ms, 1.8 frames. (b) About 150 ms after the click, plus up to a frame; a neutral click plays on press.

(a) One buffer is `1000 × 480 / 48,000 = 10 ms`; three queued are 30 ms, `30 / 16.7 = 1.8` frames.

(b) The result is known after the 120 ms round trip, then the sound waits up to 30 ms of buffering: about 150 ms. Playing "confirmed" on press would lie whenever the item was already sold. Play a neutral click on press (about 30 ms later), then confirm or error when the server answers, and a "still waiting" cue if the answer takes more than a second.
</details>

## Week 12: Audio for MMOs

48. *Week 12 · compute.* A 25-player raid: each action starts `a = 3` sounds, actions come every `g = 1.2 s`, and sounds last `W = 0.9 s`. The boss holds 5 voices. The budget is 40.
    (a) What is the average demand per player and in total?
    (b) Tiers reserve 4 for you, 6 for the boss, 10 for your party (4 other players) and 20 for the others (20 players), with spill-down. What share of each tier is kept?
    (c) Compare with a flat first-come policy in which the boss's loops, started at the pull, always hold their voices.

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 2.25 voices per player, 56.25 for the players, 61.25 with the boss. (b) You, boss and party 100%; others 52.8%. (c) Flat keeps about 62% of every player's sounds, including yours.

(a) Little's law: `3 / 1.2 × 0.9 = 2.25` per player; `25 × 2.25 = 56.25`.

(b) Demands: you 2.25, boss 5, party `4 × 2.25 = 9`, others `20 × 2.25 = 45`. Unused: `(4 − 2.25) + (6 − 5) + (10 − 9) = 3.75`. The others get `20 + 3.75 = 23.75` of 45, 52.8%. Total use is exactly 40.

(c) The boss takes 5, leaving 35 for 56.25 of player demand: `35 / 56.25 = 62%`. The flat policy keeps more of the others' sounds, and loses 38% of your own.
</details>

49. *Week 12 · compute.* A capital city keeps the nearest 8 players as individual sounds and feeds the rest into a crowd bed at `10 × log10(n)` dB above one player. How loud is the bed with 60 players present, and with 240? How much louder does quadrupling the crowd make it?

<details>
<summary>Answer and worked solution</summary>

**Answer.** +17.2 dB at 60 players, +23.7 dB at 240, a difference of 6.5 dB.

The bed counts `60 − 8 = 52` and `240 − 8 = 232` players. `10 × log10(52) = 17.2` and `10 × log10(232) = 23.7`. The difference is `10 × log10(232 / 52) = 6.5 dB`. A bed that scaled linearly with the head count would be 4.5 times the amplitude, +13 dB. Scale in decibels, and blend to a denser crowd loop for texture.
</details>

50. *Week 12 · compute.* Take the lecture's 40-player raid (`a = 2`, `g = 1.5 s`, a 32-voice budget, the boss holding 4 voices). Apply audio LOD: your sounds last 1.2 s, your party's 0.9 s and the others' 0.4 s. What is the total average demand now? Does it fit the budget without tiers? Would you drop the tiers?

<details>
<summary>Answer and worked solution</summary>

**Answer.** 29.1 voices, under 32 on average. Keep the tiers anyway.

You: `1 × 2 / 1.5 × 1.2 = 1.6`. Boss 4. Party: `4 × 2 / 1.5 × 0.9 = 4.8`. Others: `35 × 2 / 1.5 × 0.4 = 18.7`. Total 29.1. Shortening the others' sounds to a third did more than any reservation. But Little's law gives averages. On the pull everyone fires at once, and the peak is far above 29. The tiers are what protect your own sounds in exactly that moment.
</details>

51. *Week 12 · critique.* A programmer proposes "nearest first" as the only rule for a world boss: sort every request by distance and keep the closest 48. Give two failures and the fix.

<details>
<summary>Answer and worked solution</summary>

**Answer.** It protects you (distance 0) but can drop the boss, which often stands 20 m or more away and carries the most important tells. It also lets a cluster of strangers standing on top of you take every slot from your own party. Use relevance tiers (you, boss, party, others) with reservations and spill-down, and use distance only as the tie-breaker inside a tier. Add a duck on the others' tier while a boss tell plays.
</details>

## Week 13: Accessibility

52. *Week 13 · compute.* The line "Get to the boat before the tide turns!" has a 1.8 s clip and a 0.5 s gap to the next line. Use `R = 17` and `d_min = 1.0`.
    (a) Count `n`. What display time does it need, what hold, and does it fit?
    (b) What is `n_max`?
    (c) Shown voice-locked, what fraction does a 17 CPS reader miss?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `n = 38`, `d = 2.24 s`, hold 0.44 s, fits. (b) 39. (c) 19.5%.

(a) Every character counts, including spaces and the "!". `d = max(1, 38 / 17) = 2.235 s`, hold `2.235 − 1.8 = 0.435 s ≤ 0.5`.

(b) `floor(17 × (1.8 + 0.5)) = floor(39.1) = 39`.

(c) `1 − 17 × 1.8 / 38 = 1 − 30.6 / 38 = 0.195`. The reader reaches character 30.6 and loses the last 7.4 characters, most of "e turns!", the part that says why they must hurry. Hold fixes it for free.
</details>

53. *Week 13 · compute.* Classify each line at 17 CPS as fits, clash on rate, or clash on minimum time. Name a fix for each clash, and flag any line that breaks a 42-character row.

| # | Line | L (s) | Gap (s) |
|---|---|---|---|
| 1 | Down! | 0.4 | 0.4 |
| 2 | They've got a sniper on the water tower. | 1.9 | 0.3 |
| 3 | Smoke out. Move, move, move! | 1.3 | 1.5 |
| 4 | Hold here until the second squad reaches the east gate. | 2.6 | 1.0 |

<details>
<summary>Answer and worked solution</summary>

**Answer.**

| # | n | Need d | Hold | Verdict | n_max |
|---|---|---|---|---|---|
| 1 | 5 | 1.00 | 0.60 | clash on minimum time | 13 |
| 2 | 40 | 2.35 | 0.45 | clash on rate | 37 |
| 3 | 28 | 1.65 | 0.35 | fits | 47 |
| 4 | 55 | 3.24 | 0.64 | fits on time, needs two rows | 61 |

Line 1 is five characters, readable in a third of a second, but `d_min` wants 1.0 s and the gap is 0.4. Cutting text cannot help. Stack it above line 2. Line 2 needs 0.45 s of hold and has 0.3. Condense to at most 37 characters, for example "Sniper on the water tower!" (26), and ask the writers for that line in the next recording. Line 4 fits on time but is 55 characters, so it wraps onto two rows of at most 42, which uses up the stacking room if line 5 arrives quickly.
</details>

54. *Week 13 · compute.* Use compass headings (0° north, clockwise). The player faces heading 300° with a 100° field of view. Markers: none if on screen, `v` if `|rel| ≥ 135°`, otherwise `<` or `>`. Wedges: `round(rel / (360 / k)) mod k`. For each source, give bearing, relative angle, marker and the wedge for `k = 8` and `k = 16`.
    (a) `(−3, 3)`. (b) `(2, −6)`. (c) `(5, 0)`. (d) `(0, −4)`.

<details>
<summary>Answer and worked solution</summary>

**Answer.**

| Source | Bearing | rel | Marker | Wedge k=8 | Wedge k=16 |
|---|---|---|---|---|---|
| (a) (−3, 3) | −45.00° | 15.00° | none | 0 | 1 |
| (b) (2, −6) | 161.57° | −138.43° | `v` | 5 | 10 |
| (c) (5, 0) | 90.00° | 150.00° | `v` | 3 | 7 |
| (d) (0, −4) | 180.00° | −120.00° | `<` | 5 | 11 |

The bearing is `atan2(dx, dy)`. For (a), `wrap(−45 − 300) = wrap(−345) = 15°`, inside ±50°, so it is on screen. For (b), `161.57 − 300 = −138.43`, past 135°, so `v`; `round(−138.43 / 45) = −3`, and `−3 mod 8 = 5`. For (c), `wrap(90 − 300) = wrap(−210) = 150°`. For (d), `180 − 300 = −120`, off screen to the left. Note that (b) and (c) share the `v` marker, while the 8-wedge ring puts them in different wedges, 5 and 3. The ring carries more direction than the marker, which is where the fairness test starts to matter.
</details>

55. *Week 13 · critique.* A team reports: "Our subtitles are fine. The average forced rate across the script is 15 CPS, and our radial indicator shows every footstep within 40 m in one of 16 wedges, with a distance ring." Critique both claims.

<details>
<summary>Answer and worked solution</summary>

**Answer.** The average hides the lines players fail on. Players fail on the fastest lines, not the mean, so a script of slow lines with a few 25 CPS barks averages fine. Report every line's forced rate or clash verdict at the chosen `R`, and the count of lines over it.

The indicator fails the fairness test in a competitive game. Sixteen wedges and a distance ring for every footstep in 40 m are more precise than stereo headphones, which cannot even separate front from back. Every serious player would switch it on. Match the precision (8 wide wedges, no distance), show only sounds that won the week 10 priority mix, and add the fade a hearing player gets from a distant sound. Or mute effects while it is on, as Fortnite did in 2018, and state the cost to players with partial hearing.
</details>

## Week 14: Optimization: voices, memory, streaming

56. *Week 14 · compute.* A footstep set has 40 variants of 0.8 s, mono, 48 kHz, 16-bit. Use Unity's ratios (ADPCM 3.5, Vorbis 10) and 1 MB = 1,000,000 bytes.
    (a) What is its size as PCM, ADPCM (compressed in memory) and Vorbis (compressed in memory)?
    (b) What does Vorbis set to decompress on load occupy in memory?
    (c) What is the PCM size at 22,050 Hz, and what would you lose?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 3.07 MB, 0.88 MB, 0.31 MB. (b) 3.07 MB. (c) 1.41 MB; everything above 11 kHz.

(a) `40 × 0.8 × 48,000 × 2 = 3,072,000` bytes. `/ 3.5 = 877,714` and `/ 10 = 307,200`.

(b) Decompress on load turns it back into PCM, 3.07 MB, whatever the file size on disk. That is plan B's trap.

(c) `40 × 0.8 × 22,050 × 2 = 1,411,200` bytes. Nyquist is 11,025 Hz, so a thud on wood loses little and gravel or snow loses its crunch. For the shipped set, keep PCM (plan D's choice for small, frequent sounds, 3.07 MB and no decode cost) or use ADPCM compressed in memory (0.88 MB and cheap to decode, Unity's recommendation for noisy, frequent sounds). Cut the rate only after listening.
</details>

57. *Week 14 · compute.* With the lecture's invented costs (mix 0.10% per voice; decode 0 for PCM, 0.05% for ADPCM, 0.40% for Vorbis) and a 6% CPU budget:
    (a) How many real voices fit for each codec?
    (b) Ten Vorbis ambience voices are already playing. How many PCM voices are left?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 60 PCM, 40 ADPCM, 12 Vorbis. (b) 10.

(a) `N_real = floor(B / (mix + decode))`: `6 / 0.10 = 60`, `6 / 0.15 = 40`, `6 / 0.50 = 12`. (In code, add a small tolerance before `floor`, since `6 / 0.1` is not exact in floating point.)

(b) Ten Vorbis voices cost `10 × 0.50 = 5%`. The last 1% buys `1 / 0.10 = 10` PCM voices. Streaming the ambience would not help, since a streamed Vorbis file still decodes on every block; decoding it on load or dropping it to fewer voices would.
</details>

58. *Week 14 · code.* This is the lecture's cost model for one group. What does it print? Then start from plan D (5.74 MB, 5.20%) and apply both changes shown: footsteps to Vorbis compressed in memory, and ambience from compressed to stream. What are the new totals, and would you accept them on the 32 MB and 8% budget?

```python
RATIO = {"pcm": 1.0, "adpcm": 3.5, "vorbis": 10.0}
DECODE = {"pcm": 0.0, "adpcm": 0.05, "vorbis": 0.40}
MIX, STREAM_BUF = 0.10, 200_000

def group_cost(count, secs, ch, voices, codec, load):
    pcm = count * 48_000 * 2 * ch * secs
    mem = {"decompress": pcm, "compressed": pcm / RATIO[codec],
           "stream": voices * STREAM_BUF}[load]
    played = "pcm" if load == "decompress" else codec
    return mem / 1e6, voices * (MIX + DECODE[played])

for args in [(24, 0.35, 1, 6, "pcm", "decompress"),
             (24, 0.35, 1, 6, "vorbis", "compressed"),
             (3, 45, 2, 3, "vorbis", "compressed"),
             (3, 45, 2, 3, "vorbis", "stream")]:
    mem, cpu = group_cost(*args)
    print(f"{args[0]:>2} x {args[1]} s  {args[4]:<6} {args[5]:<10} {mem:6.3f} MB  {cpu:4.2f}%")
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
24 x 0.35 s  pcm    decompress  0.806 MB  0.60%
24 x 0.35 s  vorbis compressed  0.081 MB  3.00%
 3 x 45 s  vorbis compressed  2.592 MB  1.50%
 3 x 45 s  vorbis stream      0.600 MB  1.50%
```

New totals: memory `5.74 − 0.806 + 0.081 − 2.592 + 0.600 = 3.02 MB`; CPU `5.20 − 0.60 + 3.00 = 7.60%`. Both fit, but the plan is worse. Memory was never the problem at 5.74 of 32 MB, and the footstep change spends 2.4% of CPU to save 0.7 MB, leaving 0.4% for the next feature. Six footstep voices decoding Vorbis at the busiest moment is exactly what the lecture warns against. Streaming the ambience is reasonable (three long loops, few voices), but it adds 57.6 KB/s of disk reads and start delay to 3 more streams. Keep footsteps as PCM.
</details>

59. *Week 14 · compute.* A level streams two stereo music tracks at 48 kHz and two mono voice-over lines at 24 kHz, all 16-bit Vorbis at ratio 10.
    (a) What is the total read rate from disk?
    (b) How much buffer memory do the four streams hold at Unity's 200 KB each?
    (c) A teammate proposes streaming all 30 UI sounds too. Give two reasons against it.

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 48,000 bytes per second, 48 KB/s. (b) 800 KB. (c) Start delay and buffer overhead.

(a) Each stream reads `fs × (b / 8) × c / r`. Music: `48,000 × 2 × 2 / 10 = 19,200` B/s each. Voice-over: `24,000 × 2 × 1 / 10 = 4,800` B/s each. Total `2 × 19,200 + 2 × 4,800 = 48,000` B/s.

(b) `4 × 200,000 = 800,000` bytes.

(c) A stream must fill its buffer from disk before the first sample plays, so every menu click would lag (week 11). And one 200 KB buffer is larger than a 0.25 s mono UI sound as PCM (24 KB), so streaming costs more memory than it saves. Keep UI in memory, decompressed.
</details>

60. *Week 14 · critique.* A producer says: "We switched every audio file to Vorbis and the install shrank from 189 MB to 19 MB, so the audio memory problem on the phone is solved." Using the lecture's plans, explain what probably happened and what the audio team should check.

<details>
<summary>Answer and worked solution</summary>

**Answer.** The producer measured disk, not memory. If the files kept the default load type of decompress on load, every Vorbis file is decoded back into PCM when the level loads, so resident memory is still 188.73 MB (plan B). If instead they are all compressed in memory, memory falls to 18.87 MB but 21 peak voices decode Vorbis in real time, 10.5% CPU against an 8% budget (plan C), and the busiest frame stutters. Check the load type per group and profile resident memory and audio CPU at the busiest moment. Then choose per group, as plan D does: PCM for small frequent sounds, ADPCM for noisy weapons, Vorbis compressed for long loops, Vorbis streamed for music and voice-over.
</details>

# AU101 · Lab 03: A tiny sound-effect synthesiser

**Week:** 3, synthesis for SFX ([lecture](../lectures/w03-synthesis-for-sfx.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** formative, feeds the SFX pack (30%). Your six rendered sounds are the synthesised half of that pack.

## Objective

Implement the week 3 model (phase-accumulator oscillator, two-stage envelope, slide-and-jump pitch contour) in standard-library Python, render a six-sound platformer set to WAV, and test whether listeners read each contour the way you intended.

## Starter materials

All in [`lab03-starter/`](lab03-starter/). Standard-library Python, no installs.

- [`synth.py`](lab03-starter/synth.py) with an `Sfx` dataclass, the lecture's four presets, a working 24-bit `write_wav`, a JSON loader, and four functions for you to write: `freq_at`, `envelope`, `wave_value` and `render`.
- [`test_synth.py`](lab03-starter/test_synth.py). All 12 tests fail on the starter. They check the lecture's end frequencies (coin 1,334.8 Hz, jump 401.4 Hz, laser 596.7 Hz, hurt 262.8 Hz) and sample counts (12,240, 10,080, 12,096, 9,696), the envelope shape, each waveform, that a 1,200 Hz square has a 40-sample period at 48 kHz, and that a sliding sine never jumps in phase (which fails if you compute `sin(2π f(t) t)` instead of accumulating phase).
- [`my_sounds.json`](lab03-starter/my_sounds.json), a first draft of the six platformer sounds for you to redesign.
- Your `levels.py` from [lab 02](lab02.md), for measuring peaks.

Run the tests, then render, from the repository root:

```
.venv/bin/python -m unittest discover courses/AU101-audio-for-games/labs/lab03-starter
.venv/bin/python courses/AU101-audio-for-games/labs/lab03-starter/synth.py out/
.venv/bin/python courses/AU101-audio-for-games/labs/lab03-starter/synth.py out/ courses/AU101-audio-for-games/labs/lab03-starter/my_sounds.json
```

## Steps

1. **Implement** the four functions until all tests pass. Keep `render` to a single loop over samples.
2. **Listen to the presets.** Render the four lecture presets and play them. Confirm by ear that coin and jump rise, and laser and hurt fall.
3. **Redesign the six sounds** in `my_sounds.json` (jump, land, coin, power-up, hurt, death) for a platformer of your choosing. For each, record its six numbers and the total pitch change in semitones, `12 × slide × length + jump`.
4. **Measure.** Load each WAV with `levels.read_wav` and report `peak_dbfs` and `rms_dbfs`. Note which waveform gives the highest RMS at the same gain and why.
5. **Alias hunt.** Render a sawtooth at 3,100 Hz with no slide for 0.5 s. Listen, then compute where its 9th, 11th and 15th harmonics fold at 48 kHz (lecture section 4). Now add a slide of +2 octaves per second and describe what the folded tones do as the note rises.
6. **Blind test.** Play your six sounds, shuffled and unlabelled, to three people outside your group. Ask them to name each event from the list of six. Record every answer.
7. **Revise.** Change the one sound that was misread most often, re-render, and test it with two new listeners.

## Deliverable

1. Your `synth.py` with all tests passing.
2. Your final `my_sounds.json` and the six WAV files.
3. A report of at most 600 words with: a table of the six sounds (six numbers, semitone change, peak and RMS in dBFS); the alias-hunt calculation and what you heard; the blind-test confusion table (intended event against guessed event); and the revision you made and whether it worked.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Synthesiser correctness | All 12 tests pass; phase accumulator and envelope clearly written | Tests pass, code hard to follow | Tests fail | 25% |
| Sound design | Each contour matches its meaning; set is coherent in style; no clicks | One or two weak sounds | Contours contradict meanings | 25% |
| Measurement and aliasing | Peaks, RMS and three alias frequencies correct, with listening notes | Numbers correct, no listening notes | Missing or wrong | 20% |
| Blind test and revision | Confusion table from 3+ listeners, targeted revision retested | Test done, revision untested | No test | 20% |
| Report clarity | Parameters reproducible from the table alone | Partial | Missing | 10% |

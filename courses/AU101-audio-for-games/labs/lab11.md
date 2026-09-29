# AU101 · Lab 11: Render a UI family

**Week:** 11 ([lecture](../lectures/w11-ui-sound-design.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish.
**Work mode:** individual, with a partner for the blind test in Part D.
**Counts toward:** the SFX pack (30%).

## Objective

Build a tiny synthesiser that renders UI sounds to WAV, prove it against the week 11 lecture's numbers, then design, render and blind-test an eight-sound UI family with written meaning rules.

## Starter materials

All in [`lab11-starter/`](lab11-starter/). Python 3, standard library only (`math`, `struct`, `wave`).

- [`ui_sounds.py`](lab11-starter/ui_sounds.py): stubs for `semitone_ratio`, `ladder_semitones` (cap, wrap and same modes), `streak_steps` (the reset rule), `render` (a sine sweep with an attack and release envelope, normalised to an exact peak in dBFS) and `concat`. Finished tools: `peak_db`, `estimate_freq` (zero-crossing pitch estimate) and `write_wav` (mono 16-bit). A placeholder `FAMILY` dictionary shows the format for Part C.
- [`test_ui_sounds.py`](lab11-starter/test_ui_sounds.py): eight tests. They check the lecture's ladder table (523.25 to 1,046.50 Hz), cap and wrap, the streak reset (`[0, 0.3, 0.6, 1.5, 1.7]` with a 0.5 s reset gives `[1, 2, 3, 1, 2]`), exact length and peak, pitch within 1%, sweep direction, and a WAV round trip. All eight fail on the starter.
- The [streak ladder interactive](../examples/w11-streak-ladder.html) to compare your ladder by ear.
- Any audio editor that can open WAV files and show a waveform (Audacity is free), for Part C.

Run the tests with `python3 test_ui_sounds.py` inside the folder. Run `python3 ui_sounds.py` to render the placeholder family and an 8-step streak into WAV files.

## Steps

### Part A: pitch and streak logic (30 min)

1. Implement `semitone_ratio`, `ladder_semitones` and `streak_steps`. Note that a gap *equal* to the reset time keeps the streak going; only a longer gap resets it.
2. Print the lecture's ladder table from your functions and check it digit for digit.

### Part B: the renderer (40 min)

3. Implement `render`. Accumulate phase sample by sample so the sweep is smooth, apply the envelope, then scale so the peak is exactly the requested dBFS.
4. Implement `concat`. Render `streak.wav` and listen. If you hear clicks at the start or end of a tone, your envelope is wrong.

### Part C: your family (50 min)

5. Choose an interface: a game's main menu, an MMO inventory, a crafting screen, or a mobile shop. List its eight most important UI events.
6. Write a meaning rule for each parameter you use (pitch direction, interval, length, level, timbre if you layer partials). Keep them to one sentence each.
7. Fill `FAMILY` with your eight sounds and render them. Set lengths and peaks from the lecture's repetition budget, adjusted for your interface's event rates, which you must estimate and write down.
8. Add one streak ladder with a scale, cap or wrap choice and `T_reset`, and render an example streak that includes one reset.

### Part D: blind test (20 min)

9. Play your eight sounds in random order to a partner who has not seen your spec. After each, they pick the event from your list. Do three rounds. Record a confusion table (what was played against what was guessed).
10. Change the one pair that was confused most, re-render, and run one more round.

## Deliverable

- Completed `ui_sounds.py` with all eight tests passing.
- A folder of WAV files: your eight family sounds, the streak example, and the revised sound(s) from step 10.
- A two-page PDF spec: the event list with estimated rates, the meaning rules, the family table (name, trigger, start and end frequency, length, peak, bus, priority), the ladder settings, both confusion tables and a 100-word note on what you changed and why.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Code (Parts A and B) | All eight tests pass; renders are click-free | Six or seven tests pass | Five or fewer pass | 25 |
| Meaning rules | One clear rule per parameter, followed by every sound | Rules present but broken by one or two sounds | Missing | 15 |
| Family design | Eight sounds with lengths and peaks justified by estimated rates | Values given without rates | Fewer than eight sounds | 20 |
| Streak ladder | Scale, mode and reset chosen and justified; example includes a reset | Ladder present, choices not justified | Missing | 15 |
| Blind test and revision | Three rounds recorded, worst pair revised and retested with improvement shown | Test done, no retest | Missing | 20 |
| Note | Specific about what changed and what the test showed | Generic | Missing | 5 |
| **Total** | | | | **100** |

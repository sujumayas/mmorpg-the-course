# AU101 · Lab 13: Subtitle timing and directional cues

**Week:** 13, accessibility: subtitles and visual sound cues ([lecture](../lectures/w13-accessibility-subtitles-and-visual-sound-cues.md)).
**Time:** 2 hours in lab, plus about 2 hours at home.
**Weight:** formative, feeds the final sound pass (40%). The caption plan you write in Part C goes into your final submission.

## Objective

Turn the lecture's reading-rate model and direction markers into a checker you could run in a build pipeline. Use it to fix a 12-line combat script, then write a caption and visual-cue plan for your own game slice.

## Starter materials

All in [`lab13-starter/`](lab13-starter/). Python 3.10 or later, standard library only.

- [`subtitles.py`](lab13-starter/subtitles.py). CSV loading, `char_count` and the report printer are written. The functions `required_duration`, `unread_fraction`, `time_line`, `wrap`, `needs_split`, `relative_bearing`, `cue_arrow` and `sector` raise `NotImplementedError`. Their docstrings give the formulas.
- [`dialogue.csv`](lab13-starter/dialogue.csv). Twelve lines of an invented stealth scene with `id`, `speaker`, `text`, `start` and `voice_len` in seconds. Lines 1 to 6 are the lecture's example.
- [`test_subtitles.py`](lab13-starter/test_subtitles.py). Seven tests. On the untouched starter every test prints `TODO` and the script exits with status 1. Run it from the repository root:

```
.venv/bin/python courses/AU101-audio-for-games/labs/lab13-starter/test_subtitles.py
```

- The interactive [`examples/w13-subtitle-reading-race.html`](../examples/w13-subtitle-reading-race.html) for spot checks against lines 1 to 6.

## Steps

### Part A: the checker (40 min)

1. **Timing one line.** Implement `required_duration`, `unread_fraction` and `time_line`. Use a small tolerance when you compare `hold` with `gap`, because `2.82 − 2.2` is not exactly `0.62` in floating point. Run the tests until `test_required_duration`, `test_unread_fraction` and `test_time_line` pass.
2. **Layout.** Implement `wrap` as a greedy word wrap at 42 characters and `needs_split` for the two-row limit. Run until `test_wrap` passes.
3. **Report.** Run `subtitles.py` on its own. It prints the table for `dialogue.csv` at 17 CPS. Copy the table into your report. Then change the call in `__main__` to 20 CPS and copy that table too. Note which lines change verdict.

### Part B: fix the script (35 min)

4. **Classify every clash.** For each line that does not fit at 17 CPS, write down why. Is it the reading rate (`n/R` too large) or the minimum display time (`d_min` too large for the gap)? Is the line also too long for two rows?
5. **Fix each one with a named strategy.** Hold, stack, condense or pace, as in section 2 of the lecture. For condensed lines, write the new text and show that it is at most `n_max` characters. Keep the meaning. If a line can only be fixed by changing the recording, say so and write the shorter line you would give the actor.
6. **Prove it.** Save your fixed script as `dialogue_fixed.csv`, same columns. Do not change `start` or `voice_len` unless your fix is a re-record. For a stacked line, add a column `stack` set to `yes`, and count it as fitting if the two rows together are at most two rows of 42 characters. Run your checker on it and show zero unexplained clashes.

### Part C: directions and a caption plan (45 min)

7. **Markers.** Implement `relative_bearing`, `cue_arrow` and `sector`. Note that the lab uses compass headings, so the bearing is `atan2(dx, dy)`, not MA101's `atan2(dy, dx)`. Run until all seven tests pass.
8. **Your slice.** List every sound in 60 seconds of your own final-project slice, or of the sample scene your instructor provides. Apply the information test from section 3 of the lecture. For each sound that passes, write a caption key in brackets, its category (dialogue, chatter, gameplay, music) and its priority from your week 10 mix.
9. **One moment, drawn.** Pick one moment with at least three sounds that pass the information test. Give the player's position, facing and field of view, and each source's position. Use your functions to compute each marker and each 8-wedge index. Sketch the screen with the captions and the radial ring.
10. **Fairness.** In 150 words, say whether your cue design passes the fairness test from the lecture. Name one thing it shows that a hearing player could not get from stereo audio, if any, and what you changed because of it.

## Deliverable

- Your completed `subtitles.py` (renamed `lab13-<yourname>.py`) with all tests passing.
- `dialogue_fixed.csv` and the checker output on it.
- A report of up to 2 pages with: the two tables from step 3, the clash classification and fixes from steps 4 and 5, the caption plan table from step 8, the sketch and numbers from step 9, and the fairness paragraph from step 10.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Checker (steps 1-2, 7) | All seven tests pass; code follows the lecture's formulas directly and handles the tolerance and the ±180° wrap | Tests pass with hard-coded cases or special-casing | Tests fail | 25% |
| Clash diagnosis (steps 3-4) | Both tables correct; every clash classified as rate, minimum time or layout, with the numbers | Tables correct, classification partly missing | Tables missing or wrong | 15% |
| Script fixes (steps 5-6) | Every clash fixed with a named strategy; condensed lines within `n_max` and faithful to the meaning; fixed file passes the checker | Most fixed; one or two lines lose meaning or still clash | Few fixes or no evidence | 25% |
| Caption and cue plan (steps 8-9) | Information test applied to every sound with reasons; markers and wedges computed correctly and match the sketch | Plan present with gaps, or one computation wrong | Missing | 25% |
| Fairness judgment (step 10) | Names a specific advantage or gap with numbers, and a concrete change | General statement without a change | Missing | 10% |

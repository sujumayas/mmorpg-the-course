# AU101 · Lab 14: An audio budget you can defend

**Week:** 14, optimization: voices, memory, streaming ([lecture](../lectures/w14-optimization-voices-memory-streaming.md)).
**Time:** 2 hours in lab, plus about 2 hours at home.
**Weight:** formative, feeds the final sound pass (40%). The budget sheet from Part C is a required appendix of your final submission.

## Objective

Implement the lecture's memory, disk, CPU and streaming model, use it to show why the three one-setting plans fail, find a per-group plan that fits a handheld target, and write the audio budget for your own game slice.

## Starter materials

All in [`lab14-starter/`](lab14-starter/). Python 3.10 or later, standard library only.

- [`audio_budget.py`](lab14-starter/audio_budget.py). CSV loading, the constants and the report printer are written. The functions `pcm_bytes`, `group_pcm_bytes`, `disk_bytes`, `resident_bytes`, `played_codec`, `cpu_percent`, `stream_read_rate`, `max_real_voices` and `evaluate` raise `NotImplementedError`. The module docstring gives every formula.
- [`level_assets.csv`](lab14-starter/level_assets.csv). The lecture's six asset groups under plans A, B and C. Columns: `plan`, `group`, `count`, `seconds`, `channels`, `rate`, `bits`, `codec` (`pcm`, `adpcm`, `vorbis`), `load` (`decompress`, `compressed`, `stream`), `peak_voices`.
- [`test_audio_budget.py`](lab14-starter/test_audio_budget.py). Four tests. On the untouched starter every test prints `TODO` and the script exits with status 1. Run it from the repository root:

```
.venv/bin/python courses/AU101-audio-for-games/labs/lab14-starter/test_audio_budget.py
```

- The CPU costs in the starter (`MIX`, `DECODE`) are invented for an imaginary phone, as in the lecture. The ratios and the 200 KB stream buffer come from the Unity 6 manual.

## Steps

### Part A: the model (40 min)

1. **Bytes.** Implement `pcm_bytes`, `group_pcm_bytes`, `disk_bytes` and `resident_bytes`. Run until `test_pcm_bytes` and `test_disk_and_resident` pass. Check one number by hand: the music group as PCM is `4 × 48,000 × 2 × 2 × 150 = 115,200,000` bytes.
2. **CPU and streams.** Implement `played_codec`, `cpu_percent`, `stream_read_rate` and `max_real_voices`. Remember that a decompressed sound plays as PCM. Run until `test_cpu_and_streams` passes.
3. **Plans.** Implement `evaluate`, then run `audio_budget.py` on its own. It prints plans A, B and C. Copy the output. In two sentences each, say which budget each plan breaks and why.

### Part B: the handheld port (40 min)

4. **Plan D.** Add the lecture's plan D to a copy of the CSV and confirm 5.74 MB and 5.20% CPU at the 32 MB and 8% budgets.
5. **Handheld target.** Change the budgets in `main` to 8 MB and 4.5%. Plan D now fails on CPU. Write plan E in the CSV that fits both budgets. You may change codec, load type, sample rate and channels. You may not change counts, lengths or peak voices. Run the tests again to make sure nothing broke.
6. **Name the cost.** For every change from D to E, write one line on what a player could hear. Then run the lecture's interactive listening panel at your chosen sample rate for any group you downsampled, and say whether you would ship it.
7. **Emote party.** Add a group `emotes` (16 sounds, 1.0 s, stereo, 48 kHz, 10 peak voices). Find the cheapest settings that keep plan E inside the handheld budgets, or show that it can't fit and say what you would cut, with numbers.

### Part C: your slice (40 min)

8. **Inventory.** List every sound in your final-project slice, grouped as in the lecture. For each group record count, typical length, channels, source sample rate and your estimate of peak voices from playing the busiest 30 seconds.
9. **Budget sheet.** Pick a target platform and state its audio memory and CPU budget. If you have no official figure, use the handheld numbers from step 5 and say so. Write the plan as a CSV in the starter's format and run the checker on it.
10. **Measure one thing.** In your engine, open the audio profiler during the busiest 30 seconds and record the peak real voice count and the audio CPU figure it shows. Compare the voice count with your estimate from step 8. If they differ by more than 25%, update the sheet and say which sounds you missed.

## Deliverable

- Your completed `audio_budget.py` (renamed `lab14-<yourname>.py`) with all four tests passing.
- The CSV with plans D, E and E-plus-emotes, and the checker output for each.
- Your slice's budget CSV and checker output.
- A report of up to 2 pages: the plan A to C explanations (step 3), the change list with audible costs (step 6), the emote decision (step 7), your platform budget and plan (step 9), and the profiler comparison with a screenshot (step 10).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Model (steps 1-3) | All four tests pass; explanations name the decompress trap and the CPU cost of Vorbis voices with numbers | Tests pass, explanations vague | Tests fail | 25% |
| Handheld plan (steps 4-5) | Plan E fits both budgets without changing counts, lengths or voices; every change justified by group | Fits, but with changes that break the rules or without reasons | Does not fit | 20% |
| Audible cost and emotes (steps 6-7) | Each change paired with a specific audible effect; emote decision priced in both budgets | Present with gaps | Missing | 20% |
| Slice budget (steps 8-9) | Complete inventory, stated platform budget with its source, plan passes the checker | Inventory or plan incomplete | Missing | 25% |
| Measurement (step 10) | Profiler figures recorded and compared, sheet updated where the estimate was off | Figures recorded, no comparison | Missing | 10% |

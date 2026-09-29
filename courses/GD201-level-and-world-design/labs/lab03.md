# GD201 · Lab 03: Intensity graph for your blockout

**Week:** 3 · **Time:** 2 hours in the lab plus about 2 hours at home · **Weight:** part of the blockouts component (40% of the course). It revises the Lab 02 blockout.

**Lecture:** [Week 03, flow, pacing and intensity graphs](../lectures/w03-flow-pacing-and-intensity-graphs.md). **Interactive:** [w03-intensity-graph.html](../examples/w03-intensity-graph.html), for checking curves by eye.

## Objective

Implement the lecture's intensity model, its four measurements and the Director rule. Then write a beat chart and an encounter list for your Lab 02 blockout, compute its intensity graph, and revise the encounters to hit a target shape without changing the total threat. Play-test the revision and compare what testers did in the valleys with what you planned.

## Starter materials

- [`lab03-starter/intensity.py`](lab03-starter/intensity.py). The lecture's Flooded Mill beat chart as sample data, a report function, and five functions to fill in: `intensity_curve`, `measure`, `director`, `events_from_beats` and `half_life`.
- [`lab03-starter/check_lab03.py`](lab03-starter/check_lab03.py). A checker with 12 checks. Do not edit it.
- Your Lab 02 blockout and revision log.

Run from inside `lab03-starter`:

```
python intensity.py
python check_lab03.py
```

## Steps

1. **Part A, the model (25 min).** Implement `intensity_curve` and `measure`. Check against the lecture: design B has maximum 62.7, 30 s at peak, 60 s calm and 2 peaks.
2. **Part B, the Director and beats (20 min).** Implement `director`, `events_from_beats` and `half_life`. Run the checker until it prints `12/12 checks pass`. Run `intensity.py` and confirm the Flooded Mill's three fights peak at about 29, 40 and 49, rising toward the climax.
3. **Part C, your beat chart (20 min).** Write a beat chart for your Lab 02 blockout with the columns from section 3 of the lecture. Take durations from your stopwatch times, not your guesses. Choose a threat scale (for example 5 per weak enemy engaging, 15 per strong one) and write it at the top of the sheet.
4. **Part D, the curve (15 min).** Turn the chart into beats for `events_from_beats` and compute the curve with `d = 0.5`. Plot it (spreadsheet or matplotlib, if you have it) with the peak and calm bands. Record the four measurements.
5. **Part E, reshape (20 min).** Pick a target shape and write it down in one sentence (for example "three peaks, each higher than the last, at least 30 s calm after each"). Move threat between beats, or change beat durations in the blockout, until the curve meets it. The total threat must stay within 5% of the original. Record the before and after measurements.
6. **Part F, test (at home, 1 hour).** Apply the change in the engine and run one round with two new testers. Note what they do in each valley: explore, heal, look ahead, get bored, or push on. Time each valley.
7. **Sensitivity (10 min).** Recompute the curve with `d = 0.3` and `d = 0.7`. Does your revised design still meet the target? Write two sentences on what that says about how much to trust the exact numbers.
8. **Stretch (optional).** Replace one authored fight with `director` and compare the curve's shape over three different `full` values.

## Deliverable

Submit a zip with:
- Your completed `intensity.py` with your level's beats as a second list.
- The beat chart, the threat scale, and plots of the curve before and after reshaping.
- A one-page note with: the target shape sentence; before and after measurements in a table; what testers did in each valley with timings; the sensitivity result from step 7.
- The updated Lab 02 revision log with this round added.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Checker | 12/12 checks pass | 8-11 pass | 0-7 pass | 20% |
| Beat chart | Durations from measured times, threat scale stated, types and new mechanics consistent with the Lab 01 lesson matrix | Chart complete but durations guessed | Missing or no durations | 20% |
| Reshaping | Target stated in advance, met with total threat within 5%, before and after measured | Target met but total changed or target vague | No change or no measurements | 30% |
| Valley test | Tester behaviour logged and timed per valley, compared with the chart's intent | Observations present but not tied to valleys | Missing | 20% |
| Sensitivity | Both `d` values run, conclusion about how far to trust the numbers stated | One value run | Missing | 10% |

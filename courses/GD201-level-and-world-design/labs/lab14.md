# GD201 · Lab 14: Death heatmaps that don't lie

**Week:** 14 · **Time:** 2 hours in the lab plus about 3 hours at home · **Weight:** the heatmap analysis counts toward the analysis component (20% of the course). The instrumented blockout feeds the final zone.

**Lecture:** [Week 14, playtesting levels with heatmaps](../lectures/w14-playtesting-levels-with-heatmaps.md). **Interactive:** [w14-death-heatmap.html](../examples/w14-death-heatmap.html), for checking your maps.

## Objective

Turn a telemetry file into count, raw-rate and shrunk-rate heatmaps, use them to find where a simulated level is really dangerous, measure how the answer depends on `k` and cell size, and then run the same analysis on a playtest of your own blockout.

## Starter materials

- [`lab14-starter/heatmap.py`](lab14-starter/heatmap.py). Loads the telemetry and prints text maps. Six functions to fill in: `cell_of`, `count_deaths`, `count_visits`, `heat`, `heat_map` and `top_cells`. The docstrings define each one.
- [`lab14-starter/telemetry.csv`](lab14-starter/telemetry.csv). A simulated playtest of an invented 40 × 20 m level: 30 testers, 4 runs each, one position sample per second, 39 deaths.
- [`lab14-starter/make_telemetry.py`](lab14-starter/make_telemetry.py). The script that made the CSV, including the true danger of each region. Don't read `TRUE_DANGER` until step 4.
- [`lab14-starter/check_lab14.py`](lab14-starter/check_lab14.py). A checker with 11 checks. Do not edit it.
- For Part E: your Lab 02 or Lab 13 blockout, an engine that can write a text file (every engine you have used in this course can), and at least five testers.

Run from inside `lab14-starter` with the course Python:

```
python heatmap.py
python check_lab14.py
```

The starter runs and reports that the functions are not implemented. The checker prints `0/11 checks pass` until you fill them in.

## Steps

1. **Part A, counting (25 min).** Implement `cell_of`, `count_deaths` and `count_visits`. Remember that a player who leaves a cell and returns makes a new visit, and that a death row is also a position sample. The checker's tiny playtest tests both rules.
2. **Part B, heat (15 min).** Implement `heat`, `heat_map` and `top_cells`. Run the checker until it prints `11/11 checks pass`. Then run `python heatmap.py` and look at the three text maps.
3. **Part C, sensitivity (20 min).** Make a table of the top 3 cells by shrunk rate for `k` = 0, 5, 10, 20, 50 and 100 at 4 m cells, and for cell sizes 2, 4 and 8 m at `k = 20`. Mark where the top cell stops moving. Write two sentences on which `k` and which cell size you would present, and why.
4. **Part D, compare with the truth (15 min).** Now open `make_telemetry.py` and read `TRUE_DANGER`. Which region did the count map point to? Which did the shrunk map point to? Is there a region your maps under-rated? Explain it with the number of visits there. Then regenerate the data with 300 testers with `main(testers=300, path="telemetry300.csv")`, so the checker still uses the original file, and say what changed.
5. **Part E, instrument your blockout (40 min, lab or home).** Add logging to your blockout. Write a CSV row with player, run, time, kind, x and y (use the top-down plane) once per second and on every death. If your level has no deaths, log another failure event instead (falling off, failing a jump, being spotted) and say so. Use an anonymous player ID and tell testers what you record.
6. **Part F, playtest and analyse (60 min).** Run at least five testers, two runs each, without coaching. Load your CSV with `heatmap.py` (change `WIDTH` and `HEIGHT` to your level's size). Make the three maps, choose `k` and cell size using step 3's method, and pick the one cell you would change first. Watch the recording or read the observer notes for at least two failures there and write down what the players did.
7. **Stretch (optional).** Add a fourth map for position after a fixed time (the Halo 3 Jungle method): where each tester is 60 seconds into their first run. Describe what it shows that the death maps don't.

## Deliverable

Submit a zip with:
- Your completed `heatmap.py` and your blockout's telemetry CSV.
- The sensitivity table from step 3 and the half-page comparison with the truth from step 4.
- A two-page heatmap analysis of your blockout. It must contain the three maps (screenshots or text), the chosen `k` and cell size with their justification, the top cell with its `v`, `d` and shrunk rate, the observation notes for two failures there, and the change you propose with the question the next playtest should answer.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Checker | 11/11 checks pass | 7-10 pass | 0-6 pass | 20% |
| Sensitivity and truth | Full table, stable point identified, under-rated region explained with visit counts, 300-tester rerun discussed | Table present, explanation partial | Missing or no reference to visits | 20% |
| Instrumentation and playtest | Logging per second and per failure, anonymous IDs, five or more testers, two runs each | Logging works, fewer testers or runs | No usable telemetry | 20% |
| Analysis | Three maps read together, `k` and cell size justified, every rate reported with its `v`, observation explains why | Maps and rates present, justification thin or `v` missing | Count map alone, or conclusions without data | 30% |
| Proposed change | Specific change tied to the observed cause, with a testable question for the next round | Change named, link to cause weak | No change or unrelated change | 10% |

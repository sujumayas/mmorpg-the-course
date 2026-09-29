# GD201 · Lab 11: Zone population planner

**Week:** 11 · **Time:** 2 hours in the lab plus about 2 hours at home · **Weight:** part of the analysis component (20% of the course). The population plan you write here becomes a section of your final zone's design document.

**Lecture:** [Week 11, shared spaces](../lectures/w11-shared-spaces-designing-for-many-players.md). **Interactive:** [w11-crowd-capacity.html](../examples/w11-crowd-capacity.html), for checking your numbers.

## Objective

Implement the lecture's neighbour model, test it against a Monte Carlo placement of players, measure how much extra crowding appears when players choose camps at random instead of evenly, and use the model to write a population plan for your own final zone.

## Starter materials

- [`lab11-starter/crowd.py`](lab11-starter/crowd.py). The teaching zone's values, a given `toroidal_distance` helper, and five functions to fill in: `camp_neighbours`, `open_neighbours`, `capacity`, `copies_needed` and `simulate`. The docstrings define each one exactly, including how `simulate` places players.
- [`lab11-starter/check_lab11.py`](lab11-starter/check_lab11.py). A checker with 10 checks. Do not edit it.
- Your final-zone blockout or paper plan, with its camps marked.
- For the Monte Carlo part, reread [MA102 week 11, Monte Carlo simulation](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w11-monte-carlo-simulation.md) if you need a refresher on seeds and averaging over trials.

Run from inside `lab11-starter` with the course Python:

```
python crowd.py
python check_lab11.py
```

The starter runs and reports that the functions are not implemented. The checker prints `0/10 checks pass` until you fill them in.

## Steps

1. **Part A, the formulas (15 min).** Implement `camp_neighbours`, `open_neighbours`, `capacity` and `copies_needed`. Reproduce the lecture's table rows for 100, 400 and 1,000 players and the range 40 to 146.
2. **Part B, the simulation (35 min).** Implement `simulate` with `random_camps=False`. Camp players split evenly, open players scattered on a square that wraps at the edges. Confirm that the camp mean is exactly 29 at `P = 400` and that the open mean lands near the formula at `P = 1,000`.
3. **Part B, where the model breaks (10 min).** Run `simulate` at `P = 400` with `camp_radius` set to 15, 25 and 40 metres, keeping `r = 40`. Record the camp mean each time. Explain in two sentences which assumption of the model fails as the camp grows, and what that means for how big a real camp should be.
4. **Part C, uneven camps (15 min).** Run with `random_camps=True`. The camp mean should rise to about `(m − 1) / H`, where `m = round(f × P)`. Derive that value for `P = 400` and compare it with the model's `m / H − 1`. The difference is close to one extra neighbour for every player. Write three sentences on why the average *player* sees a more crowded camp than the average *camp* holds. (Hint: count how many players stand at a busy camp and how many at a quiet one.)
5. **Part C, the band (5 min).** Run the checker until it prints `10/10 checks pass`.
6. **Part D, your zone (40 min).** For your final zone, list every camp and label it competitive or cooperative, as in the in-class activity. Estimate `f`, `A` and `r` from your blockout. Choose `n_min` and `n_max` for each kind of camp and justify them in a sentence each. Compute:
   - `P_min` and `P_max` for the competitive camps;
   - `N_camp` and `N_open` at an assumed launch population of 2,000 players in your zone, with and without copies;
   - the same at 20% and at 3% of launch.
7. **Part D, one change (15 min).** Propose one layout or rule change that widens your comfortable range. Show the before and after numbers and name its cost.
8. **Stretch (optional).** Add a third group of players to `simulate`: travellers who walk the paths between camps. Place them on straight segments between neighbouring camps and measure how many neighbours they see. Compare with `N_open`.

## Deliverable

Submit a zip with:
- Your completed `crowd.py`.
- A population plan of up to two pages with: the table from step 3 and your explanation; the Part C derivation and three sentences; your camp list with labels and `n_min`, `n_max`; the Part D numbers in one table (launch, 20%, 3%, with and without copies); your proposed change with numbers and its cost.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Checker | 10/10 checks pass | 6-9 pass | 0-5 pass | 25% |
| Model limits (step 3) | Camp mean recorded for three radii; the failed assumption named and turned into a size rule | Numbers recorded, explanation vague | Missing | 15% |
| Uneven camps (step 4) | Correct derivation of `(m − 1) / H`, clear explanation of why players see more crowding than camps hold | Value correct, explanation incomplete | Missing or wrong | 15% |
| Population plan | Camps labelled, bands justified, numbers correct at all three populations, copies computed | Mostly complete, one population missing | Numbers guessed or missing | 30% |
| Design change | Change widens the range, before and after numbers shown, a real cost named | Change works but cost not named | No change or it narrows the range | 15% |

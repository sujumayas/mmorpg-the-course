# GD201 · Lab 04: Landmark legibility audit

**Week:** 4, guiding the player with landmarks, light and weenies ([lecture](../lectures/w04-guiding-the-player-landmarks-light-weenies.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** part of the blockouts assessment (40%). The zone you fix here is reused in week 9 (points of interest) and in the final greybox zone.

## Objective

Build a small tool that tells you, for every start point in a zone, which landmarks a player can actually read on screen. Then use it to fix a sample zone where one start point sees nothing, and check your numbers against a greybox in your engine.

## Starter materials

All in [`lab04-starter/`](lab04-starter/). Standard-library Python, run with `.venv/bin/python` from the repository root or any Python 3.9+.

- [`landmark.py`](lab04-starter/landmark.py), with the lecture's formulas as empty functions: `vertical_fov`, `screen_fraction`, `max_distance`, `required_height`, `relative_luminance`, `contrast_ratio` and `legibility_matrix`. A zone loader and a `report()` function are provided.
- [`zone.csv`](lab04-starter/zone.csv), a 3 km by 3 km sample zone with four landmarks (height in meters and a representative 8-bit color for each) and four start points.
- [`check_lab04.py`](lab04-starter/check_lab04.py), 18 checks built from the lecture's test values. All fail on the starter. Do not edit it.
- The [interactive](../examples/w04-landmark-range.html) for spot checks.

## Steps

1. **Formulas.** Implement the six formula functions. The checks include the lecture's table (a 50 m tower at 100 m fills 480 pixels at 1080p with a 90° horizontal view) and the lit-doorway contrast ratio of 7.02.
2. **Legibility matrix.** Implement `legibility_matrix`. Use the straight-line ground distance between a start point and a landmark, and compare it with that landmark's `max_distance`, with fog applied when given. Run `python check_lab04.py` until all 18 checks pass.
3. **Audit the sample zone.** Run `python landmark.py`. With a 90° horizontal view and `f_min = 2%`, one start point sees no landmark at all. Report which one, and how far it is from each landmark.
4. **Contrast audit.** The report also prints each landmark's contrast ratio against a daytime sky of (170, 190, 215). One landmark falls far below 3:1. Name it, explain in one sentence why its height is not the problem, and propose a color that brings it above 4.5:1 against the sky. Show the ratio.
5. **Fix the zone, three ways.** Produce three alternative edits to `zone.csv` so that every start point sees the weenie and at least one other landmark. (a) Change only landmark heights, and report the smallest total added height you found. (b) Move landmarks only, without changing heights. (c) Add one new landmark only. For each, give the new matrix and one sentence on its cost to the art team or to the zone's layout.
6. **Field of view and fog.** Rerun your preferred fix with a 110° horizontal view, then with fog at 1,500 m. Which start points lose their landmarks? Decide whether you would cap the player's field-of-view option, raise landmarks further, or accept the loss, and defend the choice in three sentences.
7. **Engine check.** Greybox your preferred fix in the course engine at true scale. From each start point, take a 1080p screenshot facing the weenie. Measure the weenie's height in pixels and compare it with `screen_fraction × 1080`. Report the error for each start. If the errors are larger than 10%, find out why (a different field of view, eye height, terrain in the way).

## Deliverable

Your completed `landmark.py` with all checks passing, the edited `zone.csv` for your preferred fix, the four screenshots from step 7 with measured and predicted pixel heights, and a report of at most 600 words covering steps 3 to 6.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Tool correctness | All 18 checks pass; code is short and readable | 14-17 checks pass | Fewer than 14 | 25% |
| Audit and contrast | Blind start point and low-contrast landmark identified with distances and ratios; proposed color reaches 4.5:1 | Identified, numbers incomplete | Missing or wrong | 20% |
| Three fixes | Three valid fixes, each with matrix and a cost judgment; minimal added height justified | Two valid fixes, or costs not discussed | One or none | 25% |
| FOV and fog decision | Losses listed, decision defended with numbers | Losses listed, decision vague | Missing | 15% |
| Engine check | Four screenshots, errors computed, large errors explained | Screenshots with partial analysis | Missing | 15% |

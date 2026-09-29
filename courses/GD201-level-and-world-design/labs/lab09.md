# GD201 · Lab 09: POI density audit

**Week:** 9 · **Time:** 2 hours in the lab plus about 2 hours at home · **Weight:** part of the analysis component (20% of the course). Your fixed layout is a starting point for the final greybox zone.

**Lecture:** [Week 09, open-world structure: POI density](../lectures/w09-open-world-structure-poi-density.md). **Interactive:** [w09-poi-gap.html](../examples/w09-poi-gap.html), for checking the density table and seeing grid, jittered and random layouts.

## Objective

Implement the lecture's gap and density model and three audit tools (a nearest-neighbour tour, a dead-zone finder and a visibility count). Use them on the Marsh, a 2 km × 2 km zone of 60 POIs that looks fine on average but hides one large empty area and one crowded cluster. Fix it for walkers at a 40-second design gap, then derive a version for players on a +60% mount with the same rhythm.

## Starter materials

- [`lab09-starter/poi_density.py`](lab09-starter/poi_density.py). The design speeds (`WALK = 6.4` m/s, `MOUNT = 1.6 × WALK`), the design gap (`TARGET = 40` s) and nine functions to fill in: `spacing_for_gap`, `density_for_gap`, `gap_for_density`, `load_zone`, `nearest_neighbour_tour`, `long_gaps`, `empty_fraction`, `largest_empty_circle` and `visible_count`. The docstrings define each one, including how to break ties.
- [`lab09-starter/zone_marsh.csv`](lab09-starter/zone_marsh.csv). The Marsh: 60 POIs as `name,x,y` in metres, origin at the south-west corner.
- [`lab09-starter/check_lab09.py`](lab09-starter/check_lab09.py). A checker with 9 checks. Do not edit it.
- For Part E: squared paper or any image editor, and the engine you used for the week 7 greybox.

Run from inside `lab09-starter` with the course Python:

```
python poi_density.py
python check_lab09.py
```

The starter runs and says the functions are not implemented. The checker prints `0/9 checks pass` until you fill them in.

## Steps

1. **Part A, the model (15 min).** Implement `spacing_for_gap`, `density_for_gap` and `gap_for_density`. Reproduce the lecture's table (192 m and 27.1 per km² for 30 s on foot).
2. **Part B, the tour (25 min).** Implement `load_zone`, `nearest_neighbour_tour` and `long_gaps`. The tour is a stand-in for a player who always heads for the closest thing they haven't done. It is not an optimal route, and it doesn't need to be.
3. **Part C, empty space and visibility (25 min).** Implement `empty_fraction`, `largest_empty_circle` and `visible_count` on a 50 m raster. Run the checker until it prints `9/9 checks pass`.
4. **Read the Marsh (15 min).** Plot the POIs (a scatter plot in any tool, or by hand on squared paper). Mark the tour's long legs and the largest empty circle. In your log, answer:
   - The Marsh's average density gives a grid gap of 40.3 s, right on target. Why do four legs take more than 80 s?
   - Where is the cluster? Compute `visible_count` within 300 m at the cluster and at the centre of the empty circle. What does each feel like to a player standing there?
   - What fraction of the Marsh is more than 250 m from any POI? Compare it with the random-layout formula `exp(−ρ π r²)` at the Marsh's density.
5. **Part D, fix it for walkers (20 min).** Move, add or remove POIs (keep the total between 58 and 64) so that no tour leg is over 80 s on foot and the largest empty circle is under 300 m. Save it as `zone_marsh_fixed.csv` and report the before and after numbers.
6. **Part E, the mounted version (at home, 45 min).** Players in the Marsh's sister zone ride at `MOUNT`. Compute the density that keeps the 40-second gap, and the POI count for a 2 km zone. Build that layout by thinning your fixed Marsh (don't start over), and check it with your tools at `MOUNT`. Then greybox 500 m × 500 m of either version in your engine at true scale, and time the walk between three neighbouring POIs with the default character controller. Compare your measured gaps with the model and explain any difference (paths around obstacles, slopes, the controller's real speed).
7. **Stretch (optional).** Replace the nearest-neighbour player with one who heads for the nearest POI *they can see* (within `r = 300` m) and wanders straight on otherwise. How does the empty circle change their tour?

## Deliverable

Submit a zip with:
- Your completed `poi_density.py`, `zone_marsh_fixed.csv` and your mounted layout CSV.
- Two plots (before and after) with long legs and the largest empty circle marked.
- A log (about 600 words) with your answers to step 4, the before and after table from step 5, the mounted-version numbers and your measured greybox gaps from step 6.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Checker | 9/9 checks pass | 5-8 checks pass | 4 or fewer pass | 30% |
| Reading the Marsh | Explains long legs by layout, not average density; visibility contrast at both spots; empty fraction compared with the random formula | Two of the three answered well | Answers restate numbers without explanation | 20% |
| Walker fix | Both targets met within the POI limit, changes justified by terrain or story | Targets met, no justification | Targets not met | 20% |
| Mounted version and greybox | Density and count computed, thinned layout checked at `MOUNT`, measured gaps compared with model and differences explained | Computed and built, comparison thin | Missing | 20% |
| Code readability | Shared distance helper, clear raster loop, ties handled as specified | Works but repetitive | Hard to follow | 10% |

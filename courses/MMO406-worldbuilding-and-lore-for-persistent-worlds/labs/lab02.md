# MMO406 · Lab 02: A map that needs its neighbours

**Week:** 2, geography and ecology ([lecture](../lectures/w02-geography-and-ecology.md)).
**Time:** 2 hours in lab, plus up to 4 hours at home.
**Weight:** exercises (40% of the course, shared across the exercise labs). The region sheet you produce here is a required section of the final world bible (60%).

## Objective

Build a small tool that measures how self-sufficient each region of a world is, then use it to design the regions of your own world. You will code the lecture's local-share formula, check real resource sets against a recipe list, find recipes that no single region can supply, and run the ten percent check on a spawn table. Your design must hit locality targets you set and justify.

## Starter materials

All in [`lab02-starter/`](lab02-starter/). Standard-library Python, run with the program's `.venv/bin/python`.

- [`regions.py`](lab02-starter/regions.py), with a finished loader and report, and five empty functions: `local_share`, `makeable_here`, `makeable_anywhere`, `combo_coverage` and `predator_ratio`.
- [`albion.json`](lab02-starter/albion.json), the five Albion Online biomes and their resources from the lecture.
- [`recipes.json`](lab02-starter/recipes.json), an invented list of 12 recipes over the same five resource types. It is a teaching list, not Albion's real crafting data.
- [`spawns.json`](lab02-starter/spawns.json), the swamp spawn table from the lecture's check-yourself question 4.
- [`test_regions.py`](lab02-starter/test_regions.py), tests built from the lecture: the `M = 5` table (60%, 30%, 10% at `r = 3`), the check-yourself values for `M = 6`, Albion's coverage (10 of 10 pairs, 5 of 10 triples), the recipes a forest region can make at home, the one recipe no biome can supply, and the swamp's predator-to-prey mass ratio of 36. The tests fail on the starter and pass once your functions are correct.
- The [interactive](../examples/w02-resource-locality.html), for spot checks.

Run the tests from inside the starter folder:

```
cd courses/MMO406-worldbuilding-and-lore-for-persistent-worlds/labs/lab02-starter
../../../../.venv/bin/python test_regions.py
```

## Steps

1. **The formula (10 min).** Implement `local_share` with `math.comb` and return a `Fraction`. `C(r, k)` is 0 when `k > r`, which `math.comb` already handles.
2. **Recipes (20 min).** Implement `makeable_here` and `makeable_anywhere`. Return sorted names so results are stable.
3. **Coverage (15 min).** Implement `combo_coverage` with `itertools.combinations`. Check by hand that Albion covers exactly the five biome triples.
4. **Spawns (10 min).** Implement `predator_ratio`. Then run `regions.py` with no arguments and write down each biome's count of home-made recipes.
5. **Explain the gap (15 min).** The model predicts each biome makes the same share of a perfectly even recipe list. The invented list gives counts from 1 to 5. In at most 150 words, explain the spread from the recipe list's composition (which types and pairs it overuses).
6. **Set your targets (at home).** For your own world, choose `M` (resource types) and the number of regions. Write three targets and one sentence of reasoning for each: the minimum home locality for two-type recipes in every region, the share of three-type combinations that must need trade, and whether any single region may be self-sufficient.
7. **Design and measure (at home).** Write `myworld.json` and `myrecipes.json` (at least 15 recipes, mixing `k = 1` to `k = 3`). Run the report. Revise until all three targets are met. Keep each version.
8. **Frame and ecology (at home).** Draw a sketch map of your regions with prevailing wind, mountains and one river system, and mark any deliberate break of the section 1 rules with its reason. Write one spawn table per region (at least three creatures), run `predator_ratio`, and for any ratio above 1 choose accept, explain or simulate. For "explain," write the reason as a tension for your lab 01 ledger.

## Deliverable

- Your completed `regions.py` with all six tests passing, and the step 5 explanation.
- `myworld.json`, `myrecipes.json`, each version's report, and the sketch map (photo or drawing).
- A region sheet of at most 900 words: your targets and reasons, the final numbers against each target, the spawn tables with their ratios and decisions, and the tensions you added to your ledger.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Correctness | All six tests pass; exact fractions | Five pass | Fewer than five pass | 25% |
| Recipe-list analysis | Explains the Albion spread from specific overused types and pairs | Correct but general | Missing or wrong | 10% |
| Targets and design | Targets reasoned from the kind of play wanted; final design meets all three with numbers shown | Targets met, reasoning thin | Targets not met or not measured | 25% |
| Physical frame | Map follows the section 1 rules; every break has a stated reason | Minor unexplained breaks | Rivers split inland, rain shadows reversed, no reasons | 15% |
| Ecology | Ratios computed; each large break handled as accept, explain or simulate, with at least one new ledger tension | Ratios computed, decisions thin | Missing | 25% |

# MMO306 · Lab 06: A flexible tier ladder

**Week:** 6, raid design and difficulty tiers ([lecture](../lectures/w06-raid-design-and-difficulty-tiers.md)).
**Time:** 2 hours in lab, plus up to 4 hours at home.
**Weight:** part of the encounter designs (40%). The ladder feeds the final dungeon brief.

## Objective

Turn one boss into a difficulty ladder you can defend with numbers. You will implement the lecture's flex model (roster, health rules, per-dealer requirement, mechanic exposure and a wipe buff), derive a neutral health rule for two roster assumptions, and fill in a four- or five-tier ladder for your own boss from lab 04.

## Starter materials

All in [`lab06-starter/`](lab06-starter/). Standard-library Python 3.10 or later.

- [`flex.py`](lab06-starter/flex.py): eight functions marked TODO: `roster`, `health_linear`, `per_dealer`, `health_neutral`, `clean_raidwide`, `clean_targeted`, `clean_fixed` and `wipes_to_clear`.
- [`test_flex.py`](lab06-starter/test_flex.py): the lecture's table (damage dealers 6, 10, 14, 18, 22; linear-rule requirements 1,750 down to 1,431.8; neutral health 2,160,000 to 7,920,000; clean pulls 82.5% to 56.2% raid-wide), the three-tank case (6,120,000 at 25 players) and the wipe-buff answers (5 wipes at 80%, 9 at 70%, never at 60%). Run it with `python test_flex.py`. Every test fails on the starter.
- [`ladder_template.csv`](lab06-starter/ladder_template.csv): the section 3 ladder with one row per tier and a `new_test` column.
- Your lab 04 `encounter.py` and boss, and your lab 05 telegraph tools.
- The [interactive](../examples/w06-flex-scaling.html) for checking curves.

## Steps

1. **Implement and test.** Fill in `flex.py` until all tests pass.
2. **Your boss at 20.** Take your lab 04 execution-check boss (boss 2) as the Normal tier at 20 players. Record `H20`, `T` and the target group's `u`.
3. **Two rosters.** Derive the neutral health rule for (a) 2 tanks at every size and (b) 3 tanks from 25 players up. Tabulate `H(N)` for `N` = 10, 15, 20, 25, 30 under the linear rule and both neutral rules, with the per-dealer requirement under each.
4. **Mechanic exposure.** For each of your boss's mechanics, decide whether its targets are raid-wide, `N // 5` or fixed. Using a telegraph from lab 05 and its per-player success `p`, tabulate the clean-pull chance (or expected misses, if it isn't a wipe) at 10, 20 and 30 players. Change one mechanic so the 10-player and 30-player clean-pull chances are within 10 points of each other, and report the change.
5. **The ladder.** Fill in `ladder_template.csv` for four or five tiers. Every tier must add one new test (write it in `new_test`). Wipe mechanics may appear only in tiers with a fixed group or at most 20 players. Use lab 04's simulator to confirm that your target group for each tier clears it with the number of deaths you allow.
6. **Catch-up.** Pick a catch-up tool for your Heroic tier once it is old (a stacking wipe buff, a flat buff or none). Using `wipes_to_clear` or a flat multiplier, say which share of groups (by effective DPS as a fraction of the requirement: 60%, 70%, 80%, 90%) it lets through.

## Deliverable

`flex.py` with all tests passing, the filled ladder CSV, and a rationale of at most 800 words: the neutral rule you chose and why, the step 4 change, what each tier tests, and your catch-up choice.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Implementation | All tests pass; roster options handled cleanly | Tests pass, roster options hard-coded | Tests fail | 20% |
| Neutral health | Both rosters derived and tabulated, linear-rule bias quantified | One roster only | Missing or wrong | 20% |
| Mechanic exposure | All mechanics classified; one change brings sizes within 10 points | Classified, no working change | Missing | 20% |
| Ladder | Every tier adds a named test; wipe rule respected; clears simulated | Ladder complete, tests vague or not simulated | Tiers differ only in health | 25% |
| Catch-up and rationale | Tool priced for four DPS fractions; choice argued | Tool chosen without pricing | Missing | 15% |

# MMO307 · Lab 06: Catch-up simulator

**Week:** 6, catch-up mechanics ([lecture](../lectures/w06-catch-up-mechanics.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** part of the progression analysis (30%). Your finish-week results can feed the lab 01 simulator if you want to turn currency into gear.

## Objective

Implement weekly and rolling caps, cap raises and cap removals as one allowance function, simulate a population of players who join a season late at different speeds, and tune a season's catch-up rules to meet two targets that pull against each other: late players should finish, and committed players should still have a reason to play in the first weeks.

## Starter materials

All in [`lab06-starter/`](lab06-starter/). Standard-library Python, run with `.venv/bin/python` or any Python 3.10+.

- [`catchup.py`](lab06-starter/catchup.py), a `Rule` dataclass (allowance `L`, rolling or weekly, head start, a raise to `L2` after week `raise_at`, removal after week `remove_at`) and six functions to write: `allowance`, `simulate`, `finish_week`, `catch_up_week`, `free_window` and `population`. Each docstring states the rule from the lecture. Running the file prints the lecture's rolling-cap example once `simulate` works.
- [`test_catchup.py`](lab06-starter/test_catchup.py), tests built from the lecture's numbers: the rolling and weekly columns of the section 2 table (finish in weeks 12 and 18); catch-up weeks 24, 12 and never; finish weeks 15, 14, 12, 12 for speeds 1,000 to 3,000; free windows 6, 9 and 8; check-yourself 5 (finish in weeks 9 and 12 after the cap comes off); the raised-cap example (week 11); Conquest-style raise from 550 to 1,100. Run `python test_catchup.py`. Every test prints `TODO` on the starter, and the script exits with status 1 until all pass.
- The [interactive](../examples/w06-rolling-cap.html) for spot checks.

## Steps

1. **Tests first.** Implement the six functions and run the tests until they all pass.
2. **Reproduce the lecture.** Print the section 2 table (weeks 6 to 18) for both rules from your simulator, and the speed table for `v` from 1,000 to 3,000.
3. **Shipped rules as data.** Encode each of these as a `Rule` and simulate a player with `j = 6` and `v = 2 L` for 20 weeks. Report their finish week and the gap to a veteran at weeks 8, 12 and 16.
   - Shadowlands Conquest: `L = 550`, rolling, raised to 1,100 per week (treat the raise as happening after week 16 of a 24-week season), removed after week 20. Use `N = 9,900`.
   - A Final Fantasy XIV style weekly cap: `L = 450`, weekly, removed after week 16 (the next rotation). Use `N = 5,010`, the Heliometry armor set from week 1.
   - A Midnight crest style cap: `L = 100`, removed after week 9. Use `N = 1,600` (16 slots, five ranks each, 20 crests per rank). Try it as rolling and as weekly, since the wiki does not say which.
4. **Population.** Generate 5,000 players with `population(5_000, seed=42, max_join=12, speeds=[0.5 L, L, 1.5 L, 2 L, 4 L])` for a 20-week season with `N = 16 L`. For each rule in step 3 (using its own `L` and a scaled `N = 16 L`), report the share of players who finish by week 20, split by join week (0 to 4, 5 to 8, 9 to 12) and by speed.
5. **Design task.** Design the catch-up rules for a 20-week season with `N = 4,800`. Choose `L`, rolling or weekly, and at most two levers from lecture section 4. Your targets:
   - at least 90% of players who join by week 8 finish by week 20 (use the step 4 population with your `L`);
   - the free lateness window for a player at `v = 4 L` is at most 4 weeks;
   - a player who plays every week at exactly `v = L` finishes no later than week 18.
   Show your rule's numbers against each target. If you cannot meet all three, say which one you gave up and why.
6. **Who pays?** For your final rule, name the player it treats worst (by join week and speed) and quantify how far behind a veteran they end the season.

## Deliverable

Your completed `catchup.py` with passing tests, a script that produces every table above, and a report of at most 700 words with the step 3 comparison, the step 4 table, the step 5 design against its three targets and the step 6 answer.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Simulator correctness | All provided tests pass; one allowance function covers every rule | Tests pass, rules special-cased | Tests fail | 25% |
| Shipped rules | All three encoded correctly, finish weeks and gaps reported, rolling vs weekly crest cap compared | Two of three correct | One or none | 20% |
| Population analysis | Shares by join week and speed for every rule, seeded and reproducible | Shares reported without the speed split | Missing | 20% |
| Design task | All three targets checked with numbers; any trade-off justified | Two targets met, third discussed | Targets not checked | 25% |
| Report | Names the worst-served player with a number, within length | Names a player without a number | Missing or over length | 10% |

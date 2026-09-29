# MMO307 · Lab 05: The squish planner

**Week:** 5, stat squish ([lecture](../lectures/w05-stat-squish-when-numbers-get-too-big.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** part of the progression analysis (30%).

## Objective

Plan a stat squish for a fictional six-era MMO. Decide whether a uniform divisor can work, choose per-era divisors that fit the readable band, build the compensation table for old content, test the game's formulas for squish safety, and estimate how long your squish will last. Then write the one-page squish plan a lead designer would sign off.

## Starter materials

All in [`lab05-starter/`](lab05-starter/). Standard-library Python, run with `.venv/bin/python` or any Python 3.10+.

- [`eras.csv`](lab05-starter/eras.csv), six eras of an invented game with a typical creature's health, a typical boss's health and a typical damage-over-time tick, before the squish. Eras are two years apart.
- [`squish.py`](lab05-starter/squish.py), a loader that works, four of the game's formulas (`armor_mitigation`, `floored_damage`, `dot_tick`, `time_to_die`) and eight functions to write: `dynamic_range`, `uniform_divisor_range`, `squish`, `compensation`, `hits_to_kill`, `power_law`, `headroom` and `scale_error`. Each docstring states the rule from the lecture.
- [`test_squish.py`](lab05-starter/test_squish.py), tests built from the lecture's numbers: dynamic range 1,000 with no uniform divisor; the four-era table (new health 1,000, 2,000, 4,000, 10,000; hits 1, 1, 1, 5 before and 1, 1, 2, 5 after; compensation 100, 20, 4, 1); the power-law curve at `p = 1/3`; headroom 6.28 years for `d = 40, R = 1.8`; the armor, floor and rounding cases from section 4. Run `python test_squish.py`. The starter fails five of six tests and exits with status 1.
- The [interactive](../examples/w05-squish-map.html) for spot checks.

## Steps

1. **Tests first.** Implement the eight functions and run the tests until they all pass.
2. **Can one divisor work?** The current player hits for 900,000. The team's readable band for creature health is 400 to 15,000 and for boss health 20,000 to 3,000,000. Compute the dynamic range of each column and whether a uniform divisor exists for each. Show the numbers.
3. **Per-era divisors.** Choose one divisor per era that puts every era's creature and boss health inside its band, with health still rising from era to era. Report a table of old values, divisors and new values. Then try `power_law` for a few values of `p` and report the `p` that comes closest to your hand-chosen divisors.
4. **Compensation.** Build `m_e` for your divisors. For creatures and bosses in every era, report hits to kill (creatures) and the number of 900,000 hits a solo player needs (bosses) before the squish, after it, and after it with compensation. Every current-era number must be unchanged, and every compensated number must equal its before value.
5. **Formula audit.** Use `scale_error` on each of the four formulas with your current-era divisor.
   - Armor: once with `k` squished, once without. Which one did your team's spreadsheet do?
   - Floored damage: find the smallest attack-minus-defense gap (before the squish) where the floor starts to distort results after it.
   - DoT ticks: squish every era's tick with that era's divisor. Which eras' ticks round to less than 5? Propose a fix (change the tick count, change the divisor, or keep more precision) and show its effect.
   - Time to die: your lead wants player health to squish by half the damage divisor, as World of Warcraft did in 2014. Report the change in time to die and one encounter it would break.
6. **Headroom.** From `eras.csv`, estimate the game's growth per year `R` (eras are two years apart; use the current and previous era's creature health). How many years will your current-era divisor last? What divisor would last six years?
7. **Squish plan.** Write a one-page plan: the divisors, the compensation table, the formula fixes, the intended balance changes (at least the health change from step 5), and the date you would plan the next squish.

## Deliverable

Your completed `squish.py` with passing tests, a script or notebook that produces every table above from `eras.csv`, and the one-page squish plan (at most 600 words plus tables).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Code correctness | All provided tests pass; tables generated from the data, not typed | Tests pass, some tables hand-made | Tests fail | 25% |
| Divisors and compensation | Every era in band, current era unchanged, compensated values equal before values, power-law comparison made | One band violated or one compensation error | Several errors | 25% |
| Formula audit | All four formulas tested, distortion thresholds found, DoT fix shown with numbers | Three formulas tested, thresholds approximate | Two or fewer | 25% |
| Headroom | `R` estimated correctly, both headroom questions answered | One answered | Missing | 10% |
| Squish plan | Clear, within length, separates squish from intended balance changes | Clear but mixes the two | Missing or hard to follow | 15% |

# GD201 · Lab 05: Signpost playtest and model

**Week:** 5, affordances and signposting ([lecture](../lectures/w05-affordances-and-signposting.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** part of the blockouts assessment (40%). The route you redesign here goes into your week 9 zone.

## Objective

Implement the lecture's two signposting models, fit them to a playtest log, and redesign a route so that at least 95% of players find it while spending as few loud signposts as you can. Then run a small playtest of your own greybox route and fit the model to your own data.

## Starter materials

All in [`lab05-starter/`](lab05-starter/). Standard-library Python, run with `.venv/bin/python` from the repository root or any Python 3.9+.

- [`signposts.py`](lab05-starter/signposts.py), with empty functions for the models (`find_chance`, `signposts_needed`, `mixture`, `route_find`, `lost_by_group`), for fitting a playtest (`signpost_rates`, `tester_rates`, `fit_two_groups`) and a Monte Carlo `simulate`. It defines a subtle signpost (scanners 0.5, tunnelers 0.05), a loud signpost (0.9 for both), the lecture's 70/30 population and a sample route of six subtle signposts.
- [`playtest_log.csv`](lab05-starter/playtest_log.csv), 12 testers by 6 signposts, one row per tester and signpost, `noticed` 1 or 0.
- [`check_lab05.py`](lab05-starter/check_lab05.py), 16 checks from the lecture's numbers and the log. All fail on the starter. Do not edit it.
- The [interactive](../examples/w05-signpost-funnel.html) for spot checks.

## Steps

1. **Models.** Implement `find_chance`, `signposts_needed`, `mixture`, `route_find` and `lost_by_group`. Watch the float trap in `signposts_needed`. With `p = 0.2` and a 36% target, the exact answer is 2 (since `1 − 0.8² = 0.36`), but the division gives 2.0000000000000004 and a naive `ceil` returns 3. Subtract a small tolerance before rounding up.
2. **Fitting.** Implement `signpost_rates`, `tester_rates` and `fit_two_groups`. Run `python check_lab05.py` until the fitting checks pass.
3. **Simulation.** Implement `simulate` and confirm it agrees with `route_find` within 1% at 50,000 players. Then run it at 12 players with ten different seeds and report the spread of results. Explain in two sentences what that spread says about a 12-person playtest.
4. **Read the log.** Plot a histogram of the 12 tester rates. Is this one group or two? Report the fitted shares and notice chances, and compare the fitted route's P(find) with the lecture's population.
5. **Redesign the sample route.** You may swap any subtle signpost for a loud one. Each loud signpost costs 1 "immersion point." Find the cheapest route that reaches 95% under (a) the lecture groups and (b) your fitted groups. Then add an escalation signpost, one that only lost players meet, with `p = 0.9` for both groups. Show where it sits in the formula and report the new P(find) with no loud signposts at all.
6. **Your own playtest.** Take the greybox route from your week 4 zone. Place at least 5 signposts. Run it with at least 4 people from outside your team, recording noticed or not per signpost, using the protocol in lecture section 4. Save the log in the same CSV format, fit the model, and predict the lost share for 1,000 players.
7. **Judgment.** In at most 300 words, argue for your final route. Say which group each signpost is for, where you spent loud signposts or escalation and why, and what a player who turns "signposting off" would face.

## Deliverable

Your completed `signposts.py` with all checks passing, your own playtest CSV, the histogram from step 4, the two redesigned routes from step 5, and a report of at most 800 words covering steps 3 to 7.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Models and fitting | All 16 checks pass; code is short and readable | 12-15 checks pass | Fewer than 12 | 25% |
| Small-sample judgment | Spread from 12-player runs reported and interpreted correctly | Spread reported, interpretation thin | Missing | 10% |
| Route redesign | Cheapest routes found for both populations; escalation modeled correctly | Valid routes, not minimal, or escalation wrong | Missing or target not met | 25% |
| Own playtest | Protocol followed, at least 4 outside testers, fit and prediction reported | Fewer testers or protocol gaps | Missing | 25% |
| Argument | Each signpost justified by group; "off" case addressed with numbers | Argument present but generic | Missing | 15% |

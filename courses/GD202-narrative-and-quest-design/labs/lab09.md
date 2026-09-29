# GD202 · Lab 09: Stranger to rival

**Week:** 9, emergent narrative ([lecture](../lectures/w09-emergent-narrative.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** part of the dialogue exercises (40%). The rival you design here can appear in your final quest chain.

## Objective

Implement the recurrence model from the lecture, confirm it with a simulation, and build a tiny nemesis system that promotes and remembers characters. Use it to tune a rival system for a zone of your own, then write the memory lines that make each rematch read as a continuing story.

## Starter materials

All in [`lab09-starter/`](lab09-starter/). Standard-library Python.

- [`rival.py`](lab09-starter/rival.py), a skeleton with six TODO functions: `p_meet`, `p_rematch_within`, `expected_wait`, `weight_for`, `simulate` and `campaign`. The docstrings fix the order of random calls so results are repeatable.
- [`test_rival.py`](lab09-starter/test_rival.py), tests built from the lecture's recurrence table, the weight targets (3 for a cast of 20 and 30 for a cast of 200, for a 50% rematch within 5), a Monte Carlo check against the formula, and rule checks for the campaign (every loss promotes exactly one character; a rematch is flagged exactly when the drawn character had beaten the player before; the same seed gives the same story).
- The [interactive](../examples/w09-rival-recurrence.html) for spot checks.

Run the tests from inside the starter folder with `../../../../.venv/bin/python test_rival.py`. They all fail on the starter. They all pass once your functions are correct.

## Steps

1. **The formulas.** Implement `p_meet`, `p_rematch_within` and `expected_wait`. Reject a cast below 1 or a weight of 0 or less with `ValueError`.
2. **Tuning by target.** Implement `weight_for(R, k, target)` by stepping `w` up from 1. Then check your answer against the closed form in the lecture.
3. **Simulation.** Implement `simulate`. Run it for three settings of your choice with 20,000 trials and report the gap between simulation and formula.
4. **The nemesis campaign.** Implement `campaign`. Run it with `R = 20`, `w = 10`, 60 encounters and a 70% player win rate, and print the log.
5. **Tests.** Run the test file until every test passes.
6. **Read the log as a story.** From one campaign log, pick the character with the most rematches. Write his story in five sentences using only what the log shows (encounters, wins, losses, rank). Then write which ingredient from lecture section 1 (cast, memory, stakes, retelling) the log was missing that you had to invent.
7. **Frustration check.** Add a rule of your own to `campaign` that stops a rival from becoming unbeatable (for example, cap the rank, decay `w` after each player win, or give the player a bonus after two losses to the same character). Run 1,000 campaigns with and without the rule and compare the largest rank any character reaches (mean and maximum).
8. **Your zone.** Choose `R` and `w` for a zone in your final project so that a player who loses to a rival has at least a 60% chance of a rematch within 8 encounters, and no more than 90% within 3. Show that your numbers meet both conditions, or explain why no whole `w` can for your `R` and what you changed.
9. **Memory lines.** Write the rival's lines for first rematch, second rematch, player wins, player loses again. Each at most 25 words, readable aloud, and valid for any encounter.

## Deliverable

Your completed `rival.py` with passing tests and your step 7 rule, and a report of at most 700 words: the simulation check (step 3), the five-sentence story and missing ingredient (step 6), the frustration comparison table (step 7), your zone numbers (step 8) and the four memory lines (step 9).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Model and campaign correctness | All provided tests pass; code is readable | Tests pass, code hard to follow | Tests fail | 25% |
| Simulation check | Gaps reported and explained (sample size, randomness) | Gaps reported without comment | Missing | 10% |
| Story from the log | Story uses only logged facts; missing ingredient named precisely | Story adds unlogged events without saying so | Missing | 15% |
| Frustration rule | Rule defined, compared over 1,000 runs with mean and max | Rule defined, weak comparison | Missing | 20% |
| Zone tuning | Both conditions met and shown, or impossibility argued | One condition shown | Missing | 15% |
| Memory lines | Lines work for any encounter and change with the rival's history | Lines generic or tied to one scene | Missing | 15% |

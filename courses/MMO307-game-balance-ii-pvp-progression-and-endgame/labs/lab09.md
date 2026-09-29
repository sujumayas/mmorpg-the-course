# MMO307 · Lab 09: Glicko and TrueSkill side by side

**Week:** 9, Glicko and uncertainty; TrueSkill for teams ([lecture](../lectures/w09-glicko-and-trueskill.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** part of the rating lab (30%), with labs 08, 10, 11 and 14 (20 of its 100 points).

## Objective

Implement Glicko-1 and a two-team TrueSkill update, check both against published numbers, rebuild the lecture's comparison of Elo and Glicko over a career, and test how TrueSkill handles a 3v3 mode where some players queue as parties.

## Starter materials

- [`lab09-starter/ratings.py`](lab09-starter/ratings.py), standard-library Python. Empty: `g`, `glicko_expected`, `glicko_update`, `rd_after_idle`, `c_for_reset`, `win_probability`, `trueskill_rate`. Provided: `career(system, seed, ...)`, the one-player simulation behind the lecture's section 3 table. With seeds 0 to 299 and a correct implementation it reproduces that table exactly.
- [`lab09-starter/test_ratings.py`](lab09-starter/test_ratings.py) with Glickman's worked example (1,464 and 151.4), his `g` values, the effective-K table rows, idle RD growth (80.6, 149.9, cap at 350), `c = 63.2` and `c = 71.0`, the library's 1v1 values (29.396 ± 7.171), the no-draw value 29.205, the team example (+0.22 and +3.76) and the win probability 0.529. All tests fail on the starter. Run from the starter folder with `../../../../.venv/bin/python test_ratings.py`, or with pytest.
- The [rating uncertainty interactive](../examples/w09-rating-uncertainty.html) for checking single updates.
- Your `elo.py` from [Lab 08](lab08.md).

## Steps

1. **Glicko-1.** Implement `g`, `glicko_expected` and `glicko_update` from the lecture. An empty period returns the inputs unchanged. (Glickman's full system still grows RD for players who sit out a period; that is step 2's job.)
2. **Idle growth.** Implement `rd_after_idle` and `c_for_reset`.
3. **TrueSkill.** Implement `win_probability` and `trueskill_rate`. All tests must pass before you continue.
4. **Career table.** Use `career` to rebuild the lecture's section 3 table for Elo K = 32, Glicko with `c = 0`, and Glicko with `c = 15`, averaging seeds 0 to 299. Then find the `c` (in steps of 5) that minimizes the sum of "games to reach 1,800 ± 30" and "games to reach 2,000 ± 30 after the jump", and report its settled wobble.
5. **Idle players.** Change `career` so the player takes a break of 20 idle periods at game 150 (no games, only RD growth) instead of improving. Compare how many games Elo and your step 4 Glicko need to recover within 30 of their true 1,800 after the break when the player comes back 150 points worse (true 1,650). Explain the difference using effective K.
6. **3v3 ladder with parties.** Build a population of 600 players with hidden true skills on TrueSkill's scale (normal, mean 25, standard deviation 4). In each round, form 100 matches of 3v3 by sorting on `μ` and taking consecutive groups of six, alternating players between teams. A team's true performance is the sum of each player's true skill plus normal noise with standard deviation `β` per player. Run 100 rounds and report the root-mean-square gap between `μ` and true skill.
7. **Add parties.** Make 20% of players members of fixed parties of three who always play together, and give a party a hidden bonus of +3 total performance for coordination. Run again. Measure the average `μ − true skill` for party members and for solo players. Then have the party members queue solo for 20 rounds and measure how their ratings move. Write down what the model assumed that was false.

## Deliverable

The completed `ratings.py` with all tests passing, your experiment scripts, the tables from steps 4, 5 and 7, and a memo of at most 400 words to a PvP systems lead. The memo must recommend Elo, Glicko or TrueSkill for a 3v3 arena mode with solo and party queues, give the parameter values you would start with, and name one measurement you would run after launch to check the choice.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Implementation and tests | All tests pass; code follows the lecture's formulas and handles edge cases | Tests pass with a noted gap | Tests fail | 25% |
| Career and idle analysis | Table reproduced; best `c` found; idle recovery explained with effective K | Numbers without explanation | Missing or wrong | 20% |
| 3v3 ladder | Working ladder with error measured over rounds | Ladder runs, measurement unclear | Missing | 20% |
| Party analysis | Party bias measured in both directions and the false assumption named | Bias measured one way | Missing | 20% |
| Memo | Clear recommendation with starting parameters and a post-launch check, within limit | Recommendation without parameters or check | Hard to act on | 15% |

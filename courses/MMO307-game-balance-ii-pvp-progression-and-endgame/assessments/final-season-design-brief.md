# MMO307 · Final season design brief: a ranked season with rating simulation

**Weight:** 40% of the course grade.
**Assigned:** week 10. **Milestone 1:** end of week 11. **Milestone 2:** end of week 13. **Final submission:** start of week 15, followed by a 20-minute presentation and viva in week 15.
**Work mode:** individual, or a pair with a contribution statement. In a pair, each partner answers the viva questions alone, and the pair must meet the pair requirements marked below.
**Lectures:** all fourteen, most directly [week 7, split tuning](../lectures/w07-pvp-vs-pve-split-tuning.md), [week 8, Elo](../lectures/w08-elo-and-expected-score.md), [week 9, Glicko and TrueSkill](../lectures/w09-glicko-and-trueskill.md), [week 10, matchmaking](../lectures/w10-matchmaking-quality-vs-queue-time.md), [week 11, seasons](../lectures/w11-seasonal-structures-and-resets.md), [week 13, patch cycles](../lectures/w13-meta-game-and-patch-cycles.md) and [week 14, measuring balance](../lectures/w14-measuring-balance-with-win-rates-and-pick-rates.md). For the reward side, [week 1](../lectures/w01-the-endgame-problem.md), [week 6](../lectures/w06-catch-up-mechanics.md) and [week 12](../lectures/w12-alternative-advancement-and-account-progression.md).

## What this component is for

Each lab tuned one number against one target. A season is where all of those numbers run at once, on the same players, on the same calendar. The reset you choose decides how misplaced players are in the weeks when your patch lands. The patch lands in a meta that takes `τ` days to settle. The matchmaker's window decides how lopsided the games are that your dashboard reads. The rating system decides whether the dashboard can see a strong class at all.

This project asks you to design one ranked PvP season for an invented MMO arena mode, and to defend it with a simulation you wrote. It assesses all three course outcomes. Your rating system and its tuning assess "implement and tune Elo/Glicko-style rating systems". Your split register and your in-season rewards assess "balance PvP separately from PvE where needed" and "design endgame progression that resists power creep". The simulation and the viva carry the most marks, because a season design that has not been run is a guess.

## The setting

Design a season for a 3v3 arena mode or a 1v1 duel ladder in an invented MMO. The pool is at least 2,000 players with hidden true skills, normal with mean 1,500 and standard deviation 200 on the Elo scale (or the TrueSkill equivalent). The mode has at least four classes, drawn from your lab 07 roster or your own. The season runs at least 12 weeks. Pick a peak arrival rate and an off-peak rate for the queue, and a distribution of games per week for casual and committed players. State every one of these inputs in your design document, because every result depends on them.

Keep the game invented. You may cite real games as precedent, as the lectures do, with the version or era and a source. No copyrighted names, art or characters in anything you build.

## What you build

### The season design document

`SEASON.md`, 2,000 to 3,000 words plus tables, with these sections.

1. **The season in one paragraph.** Length, mode, what a player chases and what they keep at the end.
2. **Rating system.** Elo, Glicko-1, Glicko-2 or TrueSkill, with every parameter and where it came from (your rating system sheet from the [rating lab](rating-lab-brief.md)). Settled wobble and games to place for a new player.
3. **Season start and end.** What resets: visible rank, hidden rating, both. The compression `α`, any provisional K or RD increase, and the visible track with its bonus rule. The misplaced share of the season for a casual and a committed player at 1,700, 1,900 and 2,100.
4. **Matchmaker.** Window rule (`w₀`, growth, `w_max`), with a wait target as a percentile and a fairness ceiling. The median and 90th-percentile wait, and mean favourite expected score, by rating band, at peak and off-peak.
5. **Class balance.** Your split register from [lab 07](../labs/lab07.md) for this mode: every PvP-only multiplier, its grain, its reason and its audit date. If the mode has a PvP item-level cap or ignores gear, say so and why (week 2).
6. **Patch calendar.** Your settling time `τ` from [lab 13](../labs/lab13.md) or a stated estimate, the patch days, each patch's judgment day (`2τ` after it), and the average `N_eff` the calendar gives. Flag every patch you must write before its predecessor is readable.
7. **Balance dashboard.** Your rule from [lab 14](../labs/lab14.md): the signal, the threshold, the sample-size condition and the day it can fire after a patch. Say why that signal suits your rating structure (`f`).
8. **Rewards.** What players earn during the season (titles, cosmetics, currency, gear), how late players catch up (week 6), and whether any of it grants power in the ranked mode. If it does, show the power gap it creates and how the split register or a cap contains it.
9. **Who pays.** The player your season serves worst, with numbers for what they experience: games spent misplaced, seconds in queue, favourite expected score, weeks behind on rewards.

### The simulation

A standard-library Python program, `season.py`, that plays your season. You may reuse your own lab code freely.

- **Population.** At least 2,000 players with hidden true skills, a main class each, and a games-per-week value drawn from your casual and committed distributions. Some players join late.
- **Rating.** Your chosen update rule, with the parameters from section 2.
- **Matchmaking.** Players enter a queue and are matched with your window rule. You may use lab 10's second-by-second queue or a round-based approximation. If you approximate, show on one scenario that its waits and fairness agree with lab 10's queue within 20%.
- **Season start.** Warm the ladder up, then apply your reset at day 0.
- **A patch.** At a day of your choice, one class gains a hidden advantage `δ` (for example +60 rating points of effective skill, as in lab 14). Later patches may remove it.
- **Outputs, per day.** Mean absolute rating error, share of lopsided games (true skill gap above 200), wait percentiles by band, visible rank progress, and each class's win rate and top-10% representation.
- **Headless and seeded.** `python season.py --seed N --days D --out results.csv` runs with `.venv/bin/python` from a clean copy and writes a CSV. The same seed gives the same file, line for line.
- **Pair requirement.** Pairs also simulate a second season end, so the report shows two consecutive seasons, and implement one catch-up rule for late joiners in the reward currency (week 6).

### The evidence report

`EVIDENCE.md` holds three experiments. Each has a question, a prediction written before the run and dated, the commands with seeds, a table over at least 5 seeds, and a paragraph comparing the prediction with the result.

1. **Reset strength.** Your chosen reset against a hard reset and against a visible-only reset. Report games to settle for players at 1,900 and above, and the total excess lopsided games in the first 4 weeks. Compare with `τ ln(e₀/ε)` from week 11.
2. **Queue at peak and off-peak.** Your window rule at both arrival rates. Report the top band's 90th-percentile wait and the population's mean favourite score against your two targets.
3. **Catching the patch.** Run with `δ = 0`, `+30` and `+60` for the patched class. Report the day your dashboard rule fires in each case, or that it does not, and the false-alarm rate at `δ = 0`. Compare the early-window win rate with `E(δ)` and the late win rate with `E((1 − f)δ)` from week 14.

## Deliverables

- A repository or zip with `season.py`, any modules it uses, and the CSV results behind every table.
- `README.md` with the commands to run the default season and to reproduce each experiment. They must work from a clean copy on the lab machines.
- `SEASON.md` and `EVIDENCE.md` as above.
- A one-page season summary for players, written as patch notes would be (MMO303 week 14's style): what resets, what is kept, how the ladder is climbed and when patches land. No numbers a player cannot check.
- Slides for the presentation, at most 8.
- Pairs only: `CONTRIBUTIONS.md`, one paragraph each, naming the files each partner wrote.

## Milestone 1: season proposal (end of week 11, 10 points)

Two pages. The mode, season length and population inputs. Your rating system choice and parameters from labs 08 and 09. Your planned reset, with the model's games to settle for a 2,100 player and the misplaced share for a casual player. A sketch of the patch calendar with the `τ` you will assume until lab 13 measures one. One risk you expect the simulation to reveal. Feedback comes back within a week. Plans may change later, but `SEASON.md` must say what changed and why.

## Milestone 2: running simulation (end of week 13, 15 points)

A 5-minute demo in the lab session. `season.py` runs headless from a seed, warms up, applies the reset and plays at least 4 weeks with matchmaking and rating updates. It prints mean rating error and lopsided share by week. Bring a one-page note comparing the simulated games to settle for the 1,900+ band with your milestone 1 prediction, and one bug you found by reading the CSV.

## Presentation and viva (week 15, 20 minutes)

Two examiners attend. Every student follows the same steps.

1. **Pitch (5 min).** Present the season from your slides. Name the player your design serves worst.
2. **Run (4 min).** An examiner picks a seed and a `δ`. You run the season headless from a clean copy and read out, from the CSV, the day the dashboard fires and the top band's 90th-percentile wait.
3. **Change a parameter (4 min).** An examiner changes one input, for example halving the off-peak arrival rate or doubling casual players' share. You predict the effect on one output with a lecture formula, then rerun and compare.
4. **Questions (7 min).** Three questions in the style of the [exam bank](exam-bank.md), rewritten with your own numbers and code. At least one is a compute question and one asks you to explain a line of your own simulation.

## Rubric

### Milestones (25 points)

| Criterion | Excellent | Good | Weak | Missing | Points |
|---|---|---|---|---|---|
| M1: inputs and rating choice | 5: all inputs stated; rating system and parameters traced to labs 08 and 09 with wobble and placement numbers | 3 to 4: one input or source missing | 1 to 2: choice without numbers | 0 | 5 |
| M1: reset and calendar plan | 5: model games to settle and misplaced share computed; calendar sketch with an assumed `τ`; one risk named | 3 to 4: one of the three thin | 1 to 2: plan without numbers | 0 | 5 |
| M2: running simulation | 10: seeded headless run; warm-up, reset and 4 weeks of matchmaking and updates; error and lopsided share by week | 6 to 9: runs, one element missing | 2 to 5: runs only partly, or not seeded | 0 to 1 | 10 |
| M2: first comparison | 5: simulated settling compared with the milestone 1 prediction, gap explained; one CSV-found bug | 3 to 4: compared, not explained | 1 to 2: numbers without comparison | 0 | 5 |

### Final submission, presentation and viva (75 points)

| Criterion | Excellent | Good | Adequate | Weak or missing | Points |
|---|---|---|---|---|---|
| Rating system and season end | 11 to 12: parameters traced to labs; reset chosen against at least two alternatives; misplaced share per band for casual and committed players; visible track climbs in a stated number of games | 8 to 10: one comparison or band missing | 5 to 7: choices stated, weakly justified | 0 to 4: defaults with no reasoning | 12 |
| Matchmaker | 9 to 10: wait percentile and fairness targets written first; results by band at peak and off-peak; off-peak rule stated as a spec | 7 to 8: one condition or band missing | 4 to 6: population averages only | 0 to 3: no targets | 10 |
| Class balance and rewards | 9 to 10: split register with grain, reason and audit date; reward track with catch-up rule; any ranked-mode power gap computed and contained | 7 to 8: one of the three thin | 4 to 6: splits or rewards listed without numbers | 0 to 3: missing | 10 |
| Patch calendar and dashboard | 9 to 10: `τ` measured or justified; judgment days and conflicts flagged; dashboard signal matched to `f`, with threshold and sample-size condition | 7 to 8: one element missing | 4 to 6: calendar or rule given without the model | 0 to 3: missing | 10 |
| Simulation quality | 11 to 12: all required outputs; seeded and reproducible; matchmaking agrees with lab 10 or the approximation is validated; code readable | 8 to 10: one output missing or one validation skipped | 5 to 7: runs but results not reproducible | 0 to 4: does not run from a clean copy | 12 |
| Evidence | 9 to 10: three experiments with dated predictions, 5 seeds, spreads, and honest comparison with the lecture formulas | 7 to 8: one experiment thin | 4 to 6: results without predictions or formulas | 0 to 3: missing | 10 |
| Presentation, player summary and viva | 10 to 11: clear pitch naming the worst-served player; live run and parameter change handled with a correct prediction; answers use your own numbers; player summary plain and accurate | 7 to 9: one step needs help | 4 to 6: two steps fail, or answers vague | 0 to 3: cannot run or explain | 11 |
| **Total** | | | | | **75** |

The final season design mark is the milestones plus the final, out of 100, multiplied by 0.40.

## Rules and advice

- **Your labs are the parts.** The rating update is lab 08 or 09, the matchmaker is lab 10, the season end is lab 11, the split register is lab 07, the calendar is lab 13 and the dashboard is lab 14. The new work is making them share one population and one calendar, and measuring what happens when they interact.
- **Write the targets before the runs.** A wait target, a fairness ceiling, a misplaced-share limit and a dashboard firing day belong in `SEASON.md` before you tune. A target chosen after seeing the results always passes.
- **Keep a control.** Every experiment needs a run with the lever off (no reset, `δ = 0`, a fixed window). Report results as differences from it, as lab 11 does.
- **Late work.** Up to 48 hours late loses 10% of the final submission mark. Later work is not accepted without an extension agreed before the deadline.

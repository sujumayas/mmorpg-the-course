# MMO305 · Lab 09: Toxicity intervention memo

**Week:** 9 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the reading responses and field observation work

## Objective

Fit the two-group toxicity model from [week 9](../lectures/w09-toxicity-research-and-interventions.md) to a month of (synthetic) match data, compare three intervention packages on toxic-match share and on wrongly punished players, and recommend one to a producer.

The model: `q = (1 − p) × r_o + p × r_h`, toxic-match share `1 − (1 − q)^n`, punishment with recall `k`, situational reduction `x`, and wrong bans `fpr × (1 − p) × M`.

## Starter materials

- [`lab09-starter/incidents.csv`](lab09-starter/incidents.csv). 5,000 rows, one per sampled player, with three columns:
  - `player_id` (P0001 to P5000),
  - `matches` (matches played last month, 10 to 40),
  - `matches_with_incident` (matches in which that player committed at least one toxic act, as confirmed by review).
- The data is synthetic. It was generated with a fixed random seed from a two-group population, and the true group of each player is hidden. Treat it as if it came from your own telemetry.
- Fixed facts about the live game: 5v5 matches (`n = 10`), a monthly active population of `M = 50,000`, and current detection recall `k = 0.4`.
- Any spreadsheet tool, or Python with pandas.

## Steps

1. **Per-player rate.** Add a column `rate = matches_with_incident / matches`. Plot a histogram of `rate` with bins 0.05 wide. Describe its shape in two sentences. Where is the gap?
2. **Draw the line.** Choose a cut-off rate above which you call a player persistent. Justify it from the histogram. Using your cut-off, estimate `p` (share of players above the line), `r_h` (total incidents over total matches for players above the line) and `r_o` (the same for players below).
3. **Where incidents come from.** Compute `q`, the persistent share of incidents, and the toxic-match share. Compare with the lecture's example. Is this game's problem more or less concentrated?
4. **Three packages.** Compute, for each package, `q` after, the share of incidents removed compared with no intervention (`k = 0`, `x = 0`), the toxic-match share, correct bans `k × p × M` and wrong bans `fpr × (1 − p) × M` per month.

   | Package | Recall `k` | Everyone-rate reduction `x` | False-positive rate `fpr` |
   |---|---|---|---|
   | Current | 0.4 | 0 | 0.3% |
   | A: better detection | 0.8 | 0 | 0.5% |
   | B: situational changes | 0.4 | 0.15 | 0.3% |
   | C: half and half | 0.6 | 0.08 | 0.4% |

5. **Sensitivity.** Move your cut-off in step 2 up and down by 0.05. Recompute the packages. Does the ranking change?
6. **Name the costs.** For package B, list the specific situational changes you would ship (at least three, drawing on Kou's contextual factors) and one cost of each for players who were never toxic.

## Deliverable

The sheet or notebook, the histogram, the package table, and a memo of about 400 words to your producer. The memo must recommend one package, cite at least three numbers from your table, state the wrong-ban count plainly, and say how you would check the result with an A/B test after launch.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Fitting the model | Cut-off justified from the histogram; `p`, `r_h`, `r_o` computed from totals, not averages of rates | Parameters computed, cut-off not justified | Parameters missing or wrong | 25% |
| Package comparison | All four rows correct for the student's parameters, wrong bans included | One package wrong or wrong bans missing | Two or more wrong | 25% |
| Sensitivity check | Shows whether the ranking survives a moved cut-off, with numbers | Done for one direction only | Missing | 15% |
| Situational design | Three concrete changes tied to Kou's factors, each with a named cost | Changes listed without costs | Missing | 15% |
| Memo | Clear recommendation argued from numbers, wrong bans faced, test plan included, about 400 words | Recommendation weakly supported | Opinion without numbers | 20% |

<details>
<summary>Instructor check values (cut-off at rate ≥ 0.20)</summary>

- 142 players above the line, so `p = 2.84%`. `r_h ≈ 0.434`, `r_o ≈ 0.0253`. 2,655 players had no incidents at all.
- `q ≈ 0.0369`, persistent share of incidents about 33%, toxic-match share about 31.3%. The problem is more concentrated than the lecture's example (25%).
- Packages (relative to `k = 0`, `x = 0`):

  | Package | `q` after | Removed | Toxic matches | Correct bans | Wrong bans |
  |---|---|---|---|---|---|
  | Current | 0.0319 | 13.4% | 27.7% | 568 | 146 |
  | A | 0.0270 | 26.7% | 23.9% | 1,136 | 243 |
  | B | 0.0271 | 26.4% | 24.1% | 568 | 146 |
  | C | 0.0271 | 26.5% | 24.0% | 852 | 194 |

- The three packages are within about 0.2 points of toxic-match share of each other. A strong memo notices the near tie and decides on the second criterion: A punishes about 100 more innocent players a month than B, while B's effect is an estimate that needs an experiment. Either choice can earn full marks if argued from these numbers.
- Cut-offs between 0.15 and 0.25 give `p` between about 2.7% and 3.6%; the packages stay within about 0.7 points of each other across that range. At a cut-off of 0.15, A pulls slightly ahead (23.6% against 24.2% for B), because more players count as persistent.

</details>

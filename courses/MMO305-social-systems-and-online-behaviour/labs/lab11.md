# MMO305 · Lab 11: Newcomer cohort analysis

**Week:** 11 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the reading responses and field observation work

## Objective

Fit the two-state newcomer model from [week 11](../lectures/w11-newcomers-and-mentoring-systems.md) to a cohort log, estimate the solo churn `a`, tied churn `b` and connection rate `p` for a control group and a mentored group, and show a studio why its day-7 dashboard undersells the mentor program.

## Starter materials

- Python 3 with numpy, pandas and matplotlib, or a spreadsheet for steps 1 and 2.
- The model from week 11, section 2:
  - `U[t+1] = U[t] × (1 − a − p)`, `A[t+1] = A[t] × (1 − b) + U[t] × p`, `R[t] = U[t] + A[t]`
  - share who ever attach `p / (a + p)`
- The data generator below. Run it once to create `mmo305_lab11_cohort.csv` (366,000 rows, about 7 MB). Each row is one player on one day: `player_id`, `group` (`control` or `mentored`), `day` (0 to 60), `active` (1 if still playing), `attached` (1 if the player has a tie by the start of that day). In a real studio the `attached` flag would come from guild membership, a repeated group partner or a friend-list entry used for play. Treat the generator as a black box until step 5: do not read the parameter values before you have estimated them.

```python
import numpy as np, csv
rng = np.random.default_rng(11)
GROUPS = {"control": (0.10, 0.02, 0.02), "mentored": (0.10, 0.02, 0.05)}
N, DAYS = 3000, 60
with open("mmo305_lab11_cohort.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["player_id", "group", "day", "active", "attached"])
    pid = 0
    for g, (a, b, p) in GROUPS.items():
        for _ in range(N):
            pid += 1
            active, attached = True, False
            for day in range(DAYS + 1):
                w.writerow([pid, g, day, int(active), int(attached)])
                if not active:
                    continue
                u = rng.random()
                if attached:
                    if u < b: active = False
                else:
                    if u < a: active = False
                    elif u < a + p: attached = True
```

## Steps

1. **Dashboard view.** For each group, compute retention (share active) at days 1, 7, 14, 30 and 60. Put them in one table. Write the one-sentence conclusion a manager who only sees day 1 and day 7 would draw.
2. **Composition.** For each group and day, compute the share of active players who are attached. Plot it for days 0 to 60. On which day does it pass 50% in each group?
3. **Estimate the parameters.** Count player-days by state. For unattached active player-days, `a` is the share followed by `active = 0` the next day and `p` the share followed by `attached = 1` the next day. For attached active player-days, `b` is the share followed by `active = 0`. Report all three for both groups, with a 95% interval for each (MA102 week 13: `±1.96 × √(x(1 − x)/n)`, where `n` is the number of player-days in that state).
4. **Model against data.** Plug your estimates into the update rule and plot the model's `R[t]` over the observed retention for both groups. Report the largest gap in percentage points.
5. **What-if.** Using your control-group estimates, compute day-7 and day-30 retention for two alternatives: a tutorial that cuts `a` by 30%, and a mentor program with your mentored-group `p`. Which one would a day-7 A/B test pick? Which one leaves more players at day 30? Now read the generator's parameters and comment on how close your estimates came.
6. **Recommendation.** Write a one-page memo to a studio that ran this test and reported "mentoring: +3 points at day 7, not worth the moderation cost."

## Deliverable

Your notebook or spreadsheet, the tables from steps 1, 3 and 5, the plots from steps 2 and 4, and the one-page memo. The memo must name the metric and horizon the studio should use, give the estimated `p` for both groups with intervals, and state one reason the estimated effect could be wrong in a real game even though it is right here (for example, who chooses to join a mentored group).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Dashboard and composition | Correct tables and plot, crossing day identified | Minor errors or unlabelled plot | Missing or wrong | 20% |
| Parameter estimates | All six estimates with correct intervals and a clear counting method | Estimates correct, intervals missing or wrong | Missing or wrong method | 25% |
| Model against data | Overlaid plot, gap reported, sensible comment on fit | Plot present, no comment | Missing | 15% |
| What-if | Both alternatives computed at both horizons, correct conclusion | Numbers correct, conclusion weak | Missing | 15% |
| Memo | Names the right horizon and metric, uses the estimates, raises a real confound | Correct horizon, weak use of numbers | Opinion without data | 25% |

<details>
<summary>Instructor check values</summary>

With seed 11 as given (numpy `default_rng`, PCG64):

- Retention, control: day 1 90.0%, day 7 50.7%, day 14 29.8%, day 30 13.7%, day 60 6.7%. Mentored: 89.5%, 53.5%, 34.9%, 21.1%, 11.7%. Day-7 gap about 3 points; day-30 gap about 7.
- Attached share of active players at day 30: control about 81%, mentored about 97%. The attached share first passes 50% on day 17 for control and day 9 for mentored.
- Estimates: control `a ≈ 0.097`, `p ≈ 0.021`, `b ≈ 0.020`. Mentored `a ≈ 0.102`, `p ≈ 0.051`, `b ≈ 0.020`. True values: `a = 0.10`, `b = 0.02`, `p = 0.02` and `0.05`.
- What-if with the true control values: tutorial (`a = 0.07`, `p = 0.02`) gives day 7 61.7%, day 30 19.8%. Mentoring (`a = 0.10`, `p = 0.05`) gives day 7 about 53.1%, day 30 about 21.4%. The day-7 test picks the tutorial; day 30 favours mentoring.

</details>

# MMO401 · Lab 02: Your first agent-based economy

**Week:** 2 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** part of the ABM labs (40%)

## Objective

Implement the random-exchange model, verify it against the exponential predictions from [week 2](../lectures/w02-agent-based-modeling-i.md), and then change one rule to see how a single design choice moves the wealth distribution. You leave with a tested model you will extend in lab 03 and in the final project.

## Starter materials

Python 3.10 or later, no packages required. Plotting with `matplotlib` is optional; a spreadsheet chart of exported CSV is fine. Save this as `mmo401_lab02.py`.

```python
"""MMO401 lab 02 starter: the random-exchange economy."""
import csv
import math
import random
import statistics


def gini(xs):
    """Gini coefficient of a list of non-negative balances."""
    xs = sorted(xs); n = len(xs); s = sum(xs)
    if s == 0:
        return 0.0
    cum = sum((k + 1) * x for k, x in enumerate(xs))
    return (2 * cum) / (n * s) - (n + 1) / n


def observe(gold):
    """The observers from week 2, section 3."""
    s = sorted(gold); n = len(s); M = sum(s); mean = M / n
    return {
        "total": M,
        "gini": gini(s),
        "below_mean": sum(1 for x in s if x < mean) / n,
        "median": statistics.median(s),
        "top10": sum(s[int(0.9 * n):]) / M,
        "broke": sum(1 for x in s if x == 0) / n,
    }


def trade(gold, rng, d):
    """One step: random payer i pays d to a random other player j, if i can afford it."""
    N = len(gold)
    i = rng.randrange(N)
    j = rng.randrange(N - 1)
    if j >= i:
        j += 1
    if gold[i] >= d:
        gold[i] -= d
        gold[j] += d


def run(N=1000, m0=100, d=5, trades=1_000_000, seed=1, every=10_000, out=None):
    rng = random.Random(seed)
    gold = [m0] * N
    rows = []
    for t in range(1, trades + 1):
        trade(gold, rng, d)
        if t % every == 0:
            row = {"trades": t, **observe(gold)}
            rows.append(row)
    assert sum(gold) == N * m0, "conservation broken"
    if out:
        with open(out, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=rows[0].keys())
            w.writeheader(); w.writerows(rows)
    return gold, rows


def exponential_predictions(T):
    return {
        "below_mean": 1 - math.exp(-1),
        "median": T * math.log(2),
        "top10": 0.1 * (1 + math.log(10)),
        "gini": 0.5,
    }


if __name__ == "__main__":
    gold, rows = run(out="lab02_seed1.csv")
    print({k: round(v, 3) for k, v in observe(gold).items()})
    print({k: round(v, 3) for k, v in exponential_predictions(100).items()})
```

## Steps

1. **Run and reproduce.** Run the starter unchanged. Your final Gini must be 0.512, median 70, and 62.0% of players below the mean. If not, find out why before going on (Python version, edited code, wrong seed).
2. **Verify.** Add two tests of your own besides the conservation `assert`. Suggestions: with `N = 2` the Gini can only take the values you can compute by hand; with `d` larger than `m0` nobody ever trades. Show each test passing.
3. **Burn-in.** Plot Gini against trades per player from the CSV. Mark where you judge the model has settled and justify the choice in two sentences.
4. **Replicate.** Run seeds 1 to 20 at 2,000 trades per player. Report the mean Gini with a 95% interval (`mean ± 1.96 × sd / sqrt(20)`). Compare with the discrete prediction 0.512 and the continuous prediction 0.5.
5. **Validate.** Plot a histogram of final balances with bin width `d` and overlay `N × d × exp(−m/T) / T`. Plot it again on a log y-axis. Describe in two sentences where the fit is good and where it is not.
6. **Change one rule.** Choose one and implement it as a new function, leaving the original untouched:
   - **Variable trade size.** `d` is drawn each step from {5, 10, 50} with probabilities {0.7, 0.25, 0.05}.
   - **Savings.** Each player keeps a reserve of 20 gold and refuses to pay if paying would drop them below it.
   - **Rich pay more.** The payer pays `max(1, round(0.05 × gold[i]))` instead of a fixed `d`.
   Predict the direction of the Gini change before running. Then run 10 seeds of both the original and your variant with the same seeds, and report both as mean ± 95% interval.
7. **Report.** Write the six-part description (agents, rules, environment, schedule, seed, observers) of your variant and one paragraph on what a designer should take from it.

## Deliverable

Your `.py` file, the CSVs you produced, and a PDF of at most three pages with: the reproduction check, your two tests, the burn-in plot, the replication result, the two histograms, the variant's prediction and results table, and the report from step 7.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Reproduction and tests (steps 1-2) | Exact reference values, two meaningful passing tests | Values reproduced, tests trivial | Values do not match and not explained | 15% |
| Burn-in and replication (steps 3-4) | Clear settling point with reason; correct interval; comparison with both predictions | Interval computed, reasoning thin | Single run only | 20% |
| Validation plots (step 5) | Both plots correct and labelled, fit described honestly including the zero bin | One plot, or no description | Missing | 15% |
| Variant (step 6) | Prediction stated first, correct implementation, same seeds, intervals for both | Implemented but no prediction or no intervals | Not working | 30% |
| Report (step 7) | All six parts, a concrete design takeaway tied to the numbers | Parts missing or takeaway generic | Missing | 20% |

<details>
<summary>Instructor check values</summary>

- Starter, seed 1, 1,000,000 trades: Gini 0.512, median 70, below mean 62.0%, top-10% share 32.5%, broke 5.8%.
- 2,000,000 trades, seed 1: Gini 0.519. Seeds 1-20 at 2,000,000 trades: mean 0.510, sd about 0.008, so the interval is about 0.510 ± 0.004.
- Seed 2 at 1,000,000 trades: Gini 0.515.
- `d = 1`, seed 1, 1,000,000 trades: Gini about 0.247 (still in burn-in, slower relaxation).
- Variants (seed 1 then seed 2, 2,000,000 trades, reference implementations): variable trade size Gini 0.498 and 0.507 (settled shape stays close to exponential); savings reserve of 20 gold 0.425 and 0.411 with no broke players (the lower tail is cut off); "rich pay more" 0.129 and 0.132 (payments shrink as a player gets poorer). Accept any direction the student's own replicated numbers support if the implementation is correct.
- Step 5: the zero bin is where the discrete model departs from the continuous curve. With 5-gold chunks the broke share settles near `1 / (T/d + 1) = 4.8%` for T = 100. Students who notice and explain this get full marks.

</details>

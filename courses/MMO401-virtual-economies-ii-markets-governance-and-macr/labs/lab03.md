# MMO401 · Lab 03: A policy experiment

**Week:** 3 · **Time:** 2 hours in lab plus about 4 hours at home · **Weight:** part of the ABM labs (40%)

## Objective

Use an agent-based model the way an in-house economist does: calibrate it from a ledger, compare balanced policies with replications and common random numbers, test how sensitive the answer is, and write a report someone else could check. This lab applies [week 3](../lectures/w03-agent-based-modeling-ii.md) and extends your lab 02 model.

## Starter materials

**1. Code.** Python 3.10 or later, no packages required. Save as `mmo401_lab03.py`. This is the code that produced the week 3 tables.

```python
"""MMO401 lab 03 starter: balanced faucet/sink policies on the random-exchange economy."""
import math
import random
import statistics


def gini(xs):
    xs = sorted(xs); n = len(xs); s = sum(xs)
    if s == 0:
        return 0.0
    cum = sum((k + 1) * x for k, x in enumerate(xs))
    return (2 * cum) / (n * s) - (n + 1) / n


def observe(gold, d):
    s = sorted(gold); n = len(s); M = sum(s)
    return {
        "money": M,
        "gini": gini(s),
        "top10": sum(s[int(0.9 * n):]) / M,
        "median": statistics.median(s),
        "under_d": sum(1 for x in s if x < d) / n,
    }


def apply_policy(policy, gold, r, f):
    N = len(gold); M = sum(gold)
    if policy == "none":
        return gold
    if policy == "A":   # flat faucet + proportional sink (sink first, then faucet)
        return [x - r * x + f for x in gold]
    if policy == "B":   # proportional faucet (budget f*N split by holdings) + proportional sink
        return [x - r * x + (f * N) * x / M for x in gold]
    if policy == "C":   # proportional faucet + flat sink, cannot go below zero
        return [max(0.0, x + r * x - f) for x in gold]
    raise ValueError(policy)


def run(policy, N=1000, m0=100.0, d=5.0, ticks=1000, r=0.02, seed=1, log_at=()):
    rng = random.Random(seed)
    f = r * m0                       # sized so the policy is balanced at M = N * m0
    gold = [m0] * N
    log = {}
    for t in range(1, ticks + 1):
        for _ in range(N):           # one tick = N trades
            i = rng.randrange(N)
            j = rng.randrange(N - 1)
            if j >= i:
                j += 1
            if gold[i] >= d:
                gold[i] -= d
                gold[j] += d
        gold = apply_policy(policy, gold, r, f)
        if t in log_at:
            log[t] = observe(gold, d)
    return gold, log


def replicate(policy, seeds=range(1, 21), **kw):
    g = [gini(run(policy, seed=s, **kw)[0]) for s in seeds]
    mean = statistics.mean(g); sd = statistics.stdev(g)
    return mean, 1.96 * sd / math.sqrt(len(g))


if __name__ == "__main__":
    # Unit test: the four-player hand case, trading switched off.
    assert [round(x, 2) for x in apply_policy("A", [100, 200, 300, 400], 0.10, 25)] == [115, 205, 295, 385]
    for p in ["none", "A", "B"]:
        _, log = run(p, log_at={1000})
        o = log[1000]
        print(p, round(o["money"]), round(o["gini"], 3), round(o["top10"], 3),
              round(o["median"], 1), round(o["under_d"], 3))
```

A full 20-seed replication of one policy takes a few minutes in plain Python. Start long runs early, or use `ticks=500` while debugging.

**2. An invented ledger to calibrate from.** A fictional MMO, "Harbor," reports one week of currency flows. Its money supply at the start of the week was 50,000,000 gold across 40,000 active characters.

| Entry | Type | Amount in the week (gold) | How it is paid or charged |
|---|---|---|---|
| Daily login chest | Faucet | 1,400,000 | 5 gold per character per day, every character |
| Monster loot gold | Faucet | 2,100,000 | Per kill; better-geared characters kill faster |
| Auction-house cut | Sink | 1,500,000 | 5% of each sale |
| Mount upkeep | Sink | 1,200,000 | 30 gold per character per week, if they can pay |
| Repair bills | Sink | 800,000 | 10% of item value per death |

## Steps

1. **Reproduce.** Run the starter. Check the three printed rows against the week 3 simulation table. Add a conservation-style test of your own: for policy A with trading on, total gold after every tick must equal `N × m0` to within `1e-6`.
2. **Calibrate.** For Harbor, compute each entry as a percentage of the money supply per week. Classify each as flat or proportional, faucet or sink, and explain each choice in one line. Compute the net weekly change in money supply as a percentage. Convert Harbor's flat faucet and flat sink to "gold per character per week" and its proportional entries to a weekly rate. State the tick length you will use and the resulting `r` and `f`.
3. **Encode Harbor.** Add a policy `"H"` to `apply_policy` that applies all five entries with the shapes you chose in step 2, scaled to the model's `N = 1,000` and `m0 = 100` so each entry keeps its share of the money supply. Explain your scaling in two sentences. Harbor's totals balance for this week. Check whether its money supply stays flat in your model, and explain what you see.
4. **Compare.** Run `none`, `A`, `B` and `H` with seeds 1 to 20 (common random numbers: every policy uses the same seed list). Report the tick-1,000 Gini, median and money supply as mean ± 95% interval in one table.
5. **Sensitivity.** Pick the Harbor entry you were least sure how to classify. Run Harbor again with that entry's shape flipped (flat to proportional or the reverse), same total. Then run a one-at-a-time sweep of one rate over at least four values. Say in one sentence per result whether it would change a recommendation.
6. **Break it.** Run policy C for 300 ticks with seeds 1 to 5. Report the tick at which the money supply first exceeds 101% of its start in each run, and explain the mechanism in three sentences.
7. **Report.** Write the four-part model report from week 3, section 5 (overview, rules, tests, results), ending with a recommendation to Harbor's designers in the week 1 memo format.

## Deliverable

Your `.py` file and a PDF report of at most five pages containing the calibration table (step 2), the comparison table (step 4), the sensitivity results (step 5), the break-it table (step 6) and the model report with its recommendation (step 7). Include your seed lists and run lengths.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Reproduction and tests (step 1) | Reference values reproduced, extra test passes and is meaningful | Values reproduced, weak test | Values do not match and not explained | 10% |
| Calibration (step 2) | Shares correct, every shape justified, tick length and parameters stated and consistent | Minor errors or unstated tick | Shares or shapes wrong without reasons | 20% |
| Harbor policy (step 3) | Implemented with correct scaling, explained clearly | Works but scaling unclear | Not working | 15% |
| Comparison (step 4) | Four policies, 20 common seeds, intervals for every value, correct reading of overlaps | Intervals missing for some values | Single runs | 20% |
| Sensitivity and break-it (steps 5-6) | Structural flip and sweep both run, decision impact stated; C mechanism explained | One of the two done well | Missing | 15% |
| Report and recommendation (step 7) | All four parts, recommendation with a reversal condition, uncertainty stated | Parts missing or no reversal condition | Opinion without results | 20% |

<details>
<summary>Instructor check values</summary>

- Starter output, seed 1, tick 1,000: `none 100000 0.512 0.325 70.0 0.058`; `A 100000 0.195 0.163 99.3 0.0`; `B 100000 0.512 0.325 70.0 0.058`.
- Replications (seeds 1-20, tick 1,000): A Gini 0.195 ± 0.002; B 0.498 ± 0.004.
- Sweep of policy A with `f = 100r` (seeds 1-5, tick 1,000): r = 0.5% gives 0.331, 1% 0.263, 2% 0.195, 5% 0.122, 10% 0.083.
- Policy C, seed 1: money supply 100,000 at tick 10, 100,823 at tick 50, 112,088 at tick 100, 298,250 at tick 200.
- Harbor shares of the 50,000,000 supply per week: login chest 2.8%, loot 4.2%, auction cut 3.0%, mount upkeep 2.4%, repairs 1.6%. Faucets 7.0%, sinks 7.0%, net 0%. Harbor is balanced in total, so any drift students see comes from the flat upkeep sink leaking when poor characters cannot pay, and from the proportional loot faucet compounding on the rich. A good step 3 answer names both.
- Expected classification: login chest flat faucet (5 × 7 = 35 gold per character per week, 1,400,000 / 40,000 = 35, consistent); loot proportional faucet (activity scales with gear); auction cut proportional sink (on trade, approximated as on holdings); mount upkeep flat sink (30 gold per week; 1,200,000 / 40,000 = 30, consistent, so everyone paid this week); repairs proportional sink (to item value). Accept reasoned alternatives for repairs and the auction cut.
- Direction: Harbor combines both compressing shapes (flat faucet, proportional sinks) and both spreading shapes (proportional loot, flat upkeep). Expect a Gini between A's and C's, with the result sensitive to how loot is modeled. That sensitivity is the finding step 5 should surface.

</details>

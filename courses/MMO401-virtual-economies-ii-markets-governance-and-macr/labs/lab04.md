# MMO401 · Lab 04: The policy desk

**Week:** 4 ([lecture](../lectures/w04-monetary-policy-tools-in-games.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs.
**Counts toward:** ABM labs (40% of the course grade). The final agent-based economy reuses the policy rule you write here.

## Objective

Build the day-by-day money model from week 4, add a tax feedback rule with a data lag, and find the fastest rule that brings an overheated server to its target without undershooting by more than 5%. Then test your rule against a faucet shock it was not tuned for.

## Starter materials

Everything you need is below. Use Python 3 (standard library) or a spreadsheet with one row per day.

The model, from lecture sections 2 and 3:

```
m[0] = m0
on day t = 1..T:
    if (t - 1) mod R == 0:
        obs = m[max(0, t - 1 - L)]
        tau = clamp(tau_n + k * (obs / target - 1), 0, 0.30)
    m[t] = m[t-1] + g - tau * v * m[t-1]
with tau_n = g / (v * target)
```

A minimal Python starting point (copy it into `lab04.py`):

```python
def run(k, L, R=30, m0=20000, target=16000, g=40, v=0.05, T=1095, cap=0.30, g_of_day=None):
    tau_n = g / (v * target)
    m, taus, tau = [m0], [], tau_n
    for t in range(1, T + 1):
        if (t - 1) % R == 0:
            obs = m[max(0, t - 1 - L)]
            tau = min(cap, max(0.0, tau_n + k * (obs / target - 1)))
        gt = g_of_day(t) if g_of_day else g
        m.append(m[-1] + gt - tau * v * m[-1])
        taus.append(tau)
    return m, taus

def settle_day(m, target, band=0.02):
    for i in range(len(m)):
        if all(abs(x / target - 1) < band for x in m[i:]):
            return i
    return None
```

Fixed inputs for everyone: `m0 = 20,000`, target 16,000, `g = 40`, `v = 5%`, tax clamp 0% to 30%, horizon 1,095 days. Each pair is assigned a data lag `L` of 30, 60 or 90 days and a review period `R` of 7 or 30 days.

## Steps

1. **Reproduce the lecture.** Run `k = 0.2` with `L` = 0, 60 and 90 at `R = 30`. Your lowest `m` and settle day must match the lecture table (16,000 and day 156; 14,856 and day 235; 13,992 and day 670).
2. **Map the rule.** For your assigned `L` and `R`, sweep `k` from 0 to 1 in steps of 0.05. For each `k` record the lowest `m`, the highest tax, and the settle day. Plot settle day and lowest `m` against `k` on one chart with two axes.
3. **Pick a rule.** Choose the `k` with the earliest settle day whose lowest `m` stays at or above 15,200 (5% below target) and whose highest tax stays at or below 15%.
4. **Shock it.** Keep your chosen rule. On day 400, a new zone raises `g` from 40 to 55 for good (use `g_of_day`). Record the peak `m` after the shock, the highest tax, and the day the server settles again. Note that the rule's `tau_n` still assumes `g = 40`, so the rule must work harder to compensate.
5. **Fix the neutral rate.** Change the rule so that `tau_n` is recomputed each review from an estimate of `g` measured over the previous `R` days (you may read `g_of_day` directly as your "telemetry", delayed by `L` days). Rerun step 4 and compare.
6. **Patch notes.** Write the two-sentence patch note you would publish on day 400 to explain what players will see over the next six months.

## Deliverable

`lab04.py` (or the spreadsheet) and a report of at most two pages: the step 1 check, the step 2 chart, your chosen `k` with its three numbers, a before/after table for steps 4 and 5, and the patch note.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Lecture reproduction | All three rows match to the gold piece and day | One row off, with the cause found | Not matching and not explained | 15 |
| Sweep and chart | Full sweep, both measures on one legible chart, constraints marked | Sweep done, chart unclear | Partial sweep | 25 |
| Rule choice | Choice follows the stated constraints and is justified from the chart | Reasonable choice, weak justification | Arbitrary | 15 |
| Shock and fix | Steps 4 and 5 both run, effect of the neutral-rate estimate explained with numbers | One step run | Missing | 30 |
| Patch note | Honest about timing, uses a number from the model | Present, vague about timing | Missing | 15 |

<details>
<summary>Instructor check values</summary>

- `k = 0.2`, `R = 30`: `L = 0` gives lowest 16,000, settle day 156. `L = 30` gives lowest 15,835, settle day 82. `L = 60` gives lowest 14,856, settle day 235. `L = 90` gives lowest 13,992, settle day 670.
- `k = 0.1`, `L = 60`, `R = 30`: lowest 15,958, settle day 160. This is a good answer for the `L = 60` pairs.
- `k = 0.5`, `L = 60`, `R = 30`: lowest 11,567, never settles; tax swings between 0% and 17.5%.
- After the step 4 shock with `k = 0.1`, `L = 60`, `R = 30`, `m` peaks near 17,900 and ends day 1,095 at about 17,856, 11.6% above target. A rule with a fixed `tau_n = 5%` settles above target because a proportional rule with a wrong neutral rate leaves a steady error. With `g = 55` the new neutral rate is `55 / (0.05 × 16,000) = 6.875%`. Students who find this in step 5 have understood the lecture.

</details>

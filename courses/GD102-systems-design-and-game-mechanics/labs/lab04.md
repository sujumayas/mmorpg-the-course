# GD102 · Lab 04: Rubber-band tuning

**Assigned:** week 4. **Due:** start of week 5. **Weight:** part of the Machinations models component (30% of the course).
**Lecture:** [Week 4, negative feedback loops](../lectures/w04-negative-feedback-loops-rubber-banding.md). **Interactive:** [w04-kart-rubber-band.html](../examples/w04-kart-rubber-band.html), for checking your numbers.

## Objective

Build the two-racer catch-up recurrence in a spreadsheet, then run the eight-racer simulation from the lecture, reproduce two of its table rows, and tune a catch-up rule for a design target of your own. By the end you should be able to state a feedback strength as a number and defend it with two measurements, closeness and early-lead value.

## Starter materials

**Part A, spreadsheet.** Create a sheet with these named inputs on an Inputs tab. No other numbers may be typed into formulas.

| Name | Value | Meaning |
|---|---|---|
| `d` | 2 | leader's edge, m per second |
| `k` | 0.25 | fraction of the gap recovered per second |
| `g0` | 0 | starting gap |
| `steps` | 30 | seconds to model |

**Part B, simulation script.** Save the following as `kart_sim.py`. It uses only the Python standard library and matches the lecture's model and the interactive spec.

```python
import random

N, T, V, SIGMA, CAP = 8, 120, 10.0, 1.5, 60.0
SKILL = [0.35 - 0.1 * i for i in range(N)]   # kart 0 is the best driver

def race(mode, f, rng):
    x = [0.0] * N
    leader_prev, changes, half_leader = -1, 0, None
    for t in range(T):
        lead = max(x)
        if mode == "distance":
            bonus = [0.1 * f * min(lead - xi, CAP) for xi in x]
        else:  # "position"
            order = sorted(range(N), key=lambda i: -x[i])
            rank = [0] * N
            for r, i in enumerate(order):
                rank[i] = r
            bonus = [2.0 * f * rank[i] / (N - 1) for i in range(N)]
        x = [x[i] + V + SKILL[i] + rng.gauss(0, SIGMA) + bonus[i] for i in range(N)]
        leader = max(range(N), key=lambda i: x[i])
        if leader_prev >= 0 and leader != leader_prev:
            changes += 1
        leader_prev = leader
        if t == T // 2 - 1:
            half_leader = leader
    winner = max(range(N), key=lambda i: x[i])
    return winner, half_leader, max(x) - min(x), changes

def measure(mode, f, races=2000, seed=1):
    rng = random.Random(seed)
    half = best = spread = changes = 0
    for _ in range(races):
        w, h, s, c = race(mode, f, rng)
        half += (w == h)
        best += (w == 0)
        spread += s
        changes += c
    return {"halfway_leader_wins": half / races, "best_wins": best / races,
            "spread": spread / races, "lead_changes": changes / races}

if __name__ == "__main__":
    for mode in ("distance", "position"):
        for f in (0.0, 0.5):
            print(mode, f, measure(mode, f))
```

**Design brief (from the lead designer).** "Our kart game is for friends of mixed skill. The best driver in a lobby should still win at least 40% of races, and the halfway leader should win between 30% and 40%. Races should finish with a spread under 30 m."

## Steps

1. **Recurrence.** On a Model tab, compute `g_t` for `t = 0..steps` with `g_(t+1) = g_t + d − k × g_t`. Add a column with the closed form `(d / k) × (1 − (1 − k)^t)` and a column with the difference. Check yourself: `g_3 = 4.625` and the difference column is zero to rounding.
2. **Chart.** Plot `g_t` for `k = 0, 0.25, 0.5, 1.5`. Use a data table or four copies of the column. Label the steady state `d / k` as a horizontal line for the three positive cases that have one.
3. **Overshoot.** Find the smallest `k` at which the gap first becomes negative (the chaser passes the leader) with `d = 2` and `g0 = 10`. Explain in two sentences why the answer is tied to the sign of `1 − k`.
4. **Reproduce.** Run `kart_sim.py`. Your distance 50% and position 50% rows must match the lecture table within 3 percentage points. If they do not, find the bug before going on. Record your numbers.
5. **Sweep.** Extend the script to run strength `f = 0, 0.1, ..., 1.0` in both modes. Save the results as a CSV and chart halfway-leader wins and best-driver wins against `f`, with a 12.5% reference line.
6. **Tune.** Find every setting (mode and `f`) that meets all three conditions in the design brief. If none does, find the setting that comes closest and say which condition fails.
7. **Change one rule.** Propose one change to the model (a different cap, bonus only when more than 20 m behind, a bonus that fades in the last 20 seconds, or your own idea). Implement it, rerun the sweep, and report whether it widens the range of settings that meet the brief.

## Deliverable

The spreadsheet, the modified script and its CSV output, and a recommendation memo of about 300 words. The memo names your chosen mode and strength, reports all four measurements for it, explains the trade-off between closeness and early-lead value in your own words, and states the result of step 7.

## Rubric

| Criterion | Points | Full marks | Partial | Minimal |
|---|---|---|---|---|
| Recurrence and closed form | 15 | Both columns correct and agree; inputs named, none typed into formulas | Minor errors or hard-coded values | Recurrence missing or wrong |
| Chart and overshoot | 15 | Four curves with steady-state lines; overshoot threshold correct with sign explanation | Chart or explanation incomplete | Missing |
| Reproduction | 15 | Both rows within tolerance, numbers recorded | One row within tolerance | Script not run |
| Sweep and chart | 20 | Both modes swept, CSV saved, chart labelled with reference line | One mode or unlabelled chart | No sweep |
| Tuning against the brief | 15 | All qualifying settings found, or closest setting with the failing condition named | Some settings checked | Guess without data |
| Rule change and memo | 20 | Change implemented and measured; memo backs every claim with a number | Change proposed, not measured, or memo vague | Missing |

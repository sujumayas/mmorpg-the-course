# MMO304 · Lab 13: Market reach and the upgrade drought

**Assigned:** week 13. **Due:** start of week 14. **Weight:** part of the Models component (30%).
**Lecture:** [Week 13, case studies](../lectures/w13-case-studies-eve-diablo-runescape-grand-exchange.md).

## Objective

Test the week 13 model by simulation. You will confirm that a market with reach `m` divides the rate of upgrades found by playing by about `1 + m`, then break the model's simplifying assumptions one at a time and see which conclusions survive. The result is the market section of your final economy spec.

## Starter materials

You need Python 3 with the standard library only. A spreadsheet version is allowed (see step 6), but the Python route is faster for 10,000 runs.

Save this as `upgrade_drought.py`:

```python
import random, statistics

def run(d=20, m=99, hours=100, quality=None, destroy_per_hour=0.0, seed=None):
    """Simulate one player. Returns (upgrades_from_play, final_gear_quality).

    d                 own drops per hour
    m                 market reach: each own drop is matched by m drops on sale
    quality           function of an RNG returning one item's quality
                      (default: uniform 0..1)
    destroy_per_hour  chance per hour that worn gear is destroyed (reset to 0)
    """
    rng = random.Random(seed)
    if quality is None:
        quality = lambda r: r.random()
    best = 0.0
    upgrades = 0
    for hour in range(hours):
        if rng.random() < destroy_per_hour:
            best = 0.0
        for _ in range(d):
            # market first: the best of m items from other players is on sale
            if m > 0:
                market_best = max(quality(rng) for _ in range(m))
                if market_best > best:
                    best = market_best   # bought, not found: not counted
            q = quality(rng)
            if q > best:            # an upgrade found by playing
                best = q
                upgrades += 1
    return upgrades, best

def summary(n_runs=2000, **kw):
    # run i uses seed i, so every result can be reproduced exactly
    ups, gear = zip(*(run(seed=i, **kw) for i in range(n_runs)))
    return statistics.mean(ups), statistics.mean(gear)

if __name__ == "__main__":
    for m in (0, 9, 99):
        u, g = summary(n_runs=500, m=m, hours=10)
        print(f"m={m:3d}  upgrades from play={u:6.3f}  gear quality={g:.5f}")
```

Expected output at `d = 20`, `hours = 10` (200 own drops), give or take simulation noise: with `m = 0`, about 5.9 upgrades from play (the harmonic number `H_200 = 5.878`) and gear quality near 0.995. With `m = 99`, about 0.06 upgrades from play and gear quality near 0.99995.

Runtime note: each hour draws `d × (m + 1)` items, so `m = 199` at `hours = 50` is 200,000 draws per run. Use `n_runs=200` for the sweep in step 3 if 2,000 is too slow. For uniform quality only, you may replace the market line with `market_best = rng.random() ** (1 / m)`, which has the same distribution as the maximum of `m` uniform draws; do not use that shortcut in step 4.

Create a results file, `lab13_results.csv`, with this header row, one row per run you report:

```
scenario,d,m,hours,distribution,destroy_per_hour,upgrades_from_play,gear_quality,predicted_upgrades,notes
```

## Steps

1. **Run the baseline.** Run the script. Record the three rows in the CSV. For `m = 0`, compute the prediction `H_n` by hand or with a one-line sum and put it in `predicted_upgrades`.
2. **Check the `1/(K+1)` rule.** In the script the market is checked before each own drop, so own drop number `i` competes with `K = 100·i − 1` earlier items and upgrades with chance `1/(100·i)`. For `m = 99`, predict upgrades from play over 200 own drops as `sum over i = 1..200 of 1/(100·i)`, which equals `H_200 / 100 ≈ 0.059`. Compare with the simulation. Explain any gap of more than 10% in `notes`.
3. **Sweep reach.** Run `m` in {0, 1, 4, 9, 19, 49, 99, 199} at `hours = 50`. Plot upgrades from play against `1 + m` on log-log axes. The slope should be close to −1 once `m` is large. Report the fitted slope.
4. **Change the distribution.** Replace uniform quality with a skewed one, for example `quality=lambda r: r.random() ** 3` (most items are poor). Repeat step 3. Does the `1/(1 + m)` shape survive? Explain why using the fact that "beats the best of K" depends only on ranks, not on the values.
5. **Add destruction.** Set `m = 99` and try `destroy_per_hour` in {0, 0.05, 0.2, 0.5}. How much destruction does it take for the market player's upgrades from play to reach the self-found player's baseline from step 1? Relate this to EVE in two sentences.
6. **(Spreadsheet option.)** If you work in a spreadsheet instead, simulate 200 own drops in rows with `=RAND()`, a running maximum column, and a market column that uses `=MAX` over `m` random cells. Run at least 200 recalculations with a data table and report the mean.
7. **Write the memo.** 400 words, addressed to a producer who wants a global auction house for your final-project game. Name your core reward, give the `m` you recommend for it, quote one number from your simulation, and propose one mitigation (binding, destruction, regional markets or a tax).

## Deliverable

A zip with `upgrade_drought.py` (with your changes), `lab13_results.csv`, the log-log plot from step 3 (PNG), and the memo (PDF or Markdown).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) |
|---|---|---|---|
| Baseline and prediction (steps 1-2) | Simulated and predicted values agree within noise; gaps explained with the model | Values present, explanation thin | Values missing or prediction wrong |
| Reach sweep (step 3) | Clean log-log plot, slope reported and interpreted | Plot present, slope not interpreted | No sweep |
| Assumption tests (steps 4-5) | Correctly explains why ranks make the result distribution-free; destruction threshold found and linked to EVE | One of the two tests done well | Tests missing or conclusions contradict the data |
| Memo (step 7) | Names the core reward, recommends a specific `m`, cites a simulated number, gives a mitigation with a trade-off | Recommendation present but vague | No recommendation or no numbers |
| Reproducibility | Seeds or run counts stated; CSV complete | Some rows incomplete | Results cannot be reproduced |

Total 20 points, scaled to the lab weight.

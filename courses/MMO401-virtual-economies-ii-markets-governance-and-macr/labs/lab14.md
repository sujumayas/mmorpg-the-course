# MMO401 · Lab 14: Sizing an intervention

**Assigned:** week 14. **Due:** start of week 15 (it becomes a draft of your final policy memo). **Weight:** part of the ABM labs component (40%).
**Lecture:** [Week 14, intervention design](../lectures/w14-intervention-design.md). Uses your results from [Lab 13](lab13.md).

## Objective

Turn the Lab 13 diagnosis into a sized, predicted and reversible intervention. You calibrate the week 14 stock-flow model to the Lab 13 economy, forecast the producer's planned tax rise under three behavioural elasticities, compare it with a faucet cut, and write a one-page intervention spec.

## Starter materials

Python 3 with the standard library (a spreadsheet works too). The model runs in monthly steps so it matches the Lab 13 data. Save as `intervene.py`:

```python
import math

def simulate(M0, F, V0, tau0, tau, eps, months=12):
    """Monthly stock-flow model with a proportional sales tax.

    M0    money stock at the start (billions of crowns)
    F     net faucet per month after all non-tax sinks
    V0    monthly velocity at the old tax rate
    tau0  old tax rate, tau  new tax rate
    eps   elasticity of velocity to the tax rate
    Returns a list of dicts, one per month, from month 0.
    """
    V = V0 * (tau / tau0) ** (-eps)
    r = tau * V
    M = M0
    rows = []
    for m in range(months + 1):
        rows.append({
            "month": m, "M": M, "trade": V * M, "tax_sink": r * M,
            "price_index": M / M0, "volume_index": V / V0,
        })
        M = M + F - r * M
    return rows, F / r, -math.log(2) / math.log(1 - r)

if __name__ == "__main__":
    rows, M_star, half = simulate(M0=1271.4, F=114, V0=4.2, tau0=0.02, tau=0.04, eps=0)
    print(f"M* = {M_star:.1f}, half-life = {half:.2f} months")
    for r in rows:
        print(f"{r['month']:2d}  M={r['M']:8.1f}  sink={r['tax_sink']:6.1f}  "
              f"P={r['price_index']:.3f}  Q={r['volume_index']:.3f}")
```

Calibration values from Lab 13, month 12: `M0 = 1,271.4`, `F = 149 − 22 − 13 = 114` (faucets minus repairs and other sinks), `V0 = 4.2`, `τ0 = 2%`. With monthly steps, use the exact discrete half-life `−ln 2 / ln(1 − r)`, which the script already does. The `ln 2 / r` shortcut from the lecture drifts once `r` is above about 0.05.

Checkpoints: at `τ = 2%`, `M* ≈ 1,357` and money is still rising slowly. At `τ = 4%` and `ε = 0`, `M* ≈ 679`, half-life ≈ 3.8 months, `M` after 6 months ≈ 875. At `ε = 0.5`, `M* ≈ 960`, half-life ≈ 5.5 months.

## Steps

1. **Baseline.** Run the model at `τ = τ0` for 12 months. Report `M*` and where money per player will settle if active players stay at 54,000.
2. **Forecast the planned rise.** Run `τ = 4%` for `ε` in {0, 0.5, 1}. For each, report `M*`, half-life, the month-1 tax sink, and `M`, price index and volume index at months 1, 3, 6 and 12. Plot all three money paths on one chart and the price and volume indices on a second.
3. **Compare a faucet cut.** Find the net faucet `F` that gives the same `M*` as step 2's `ε = 0` case while keeping `τ = 2%`. Say which faucet line from Lab 13 you would cut and by what percentage. Explain why this option's result does not depend on `ε`.
4. **Add the announcement.** The rise was announced in month 10. Using your Lab 13 month 11 result, estimate the velocity drop that happened before the change. Rerun step 2 with `V0` lowered by that amount for the first two months only (edit the loop). Does it change your 12-month forecast by more than 5%?
5. **Incidence.** Fill the four-row incidence table from the lecture (new players, gatherers, traders, richest 1%) for the tax rise and for your faucet cut.
6. **Kill criteria.** Write two kill criteria as numbers with dates, one of which must separate `ε ≈ 0` from `ε ≈ 1` using the price and volume indices.
7. **Write the spec.** One page in the lecture's seven-part format. Recommend the tax rise, the faucet cut, a smaller staged rise, or no action. Cite at least three numbers from your runs.

## Deliverable

`intervene.py` with your edits, the two plots from step 2 (PNG), a CSV of every run, and the one-page spec (Markdown or PDF).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) |
|---|---|---|---|
| Calibration and forecasts (steps 1-2) | Correct `M*` and half-lives for all runs; clear plots; results match checkpoints | Minor errors or one run missing | Model not calibrated to Lab 13 or results far from checkpoints |
| Faucet comparison (step 3) | Correct `F`, a named faucet line with a percentage, and a sound explanation of why `ε` drops out | Right `F`, weak explanation | Missing or wrong |
| Announcement effect (step 4) | Velocity drop estimated from Lab 13 data; rerun done; effect sized | Estimate made, rerun missing | Missing |
| Incidence and kill criteria (steps 5-6) | Both tables complete; kill criteria numeric, dated, and one distinguishes elasticities | Criteria present but not numeric | Missing |
| Spec (step 7) | All seven parts; recommendation follows from the numbers; alternatives rejected with reasons | Spec present, some parts thin | No recommendation or no numbers |

Total 20 points, scaled to the lab weight.

<details>
<summary>Instructor key (remove before handing out)</summary>

- Step 1: `r = 0.084`, `M* = 1,357.1`, money per player at equilibrium about 25.1 million crowns.
- Step 2: `ε = 0` gives `r = 0.168`, `M* = 678.6`, half-life 3.77 months, month-1 sink 213.6, `M` at months 1, 3, 6, 12 = 1,171.8, 1,020.0, 875.2, 743.8. `ε = 0.5` gives `V = 2.970`, `r = 0.1188`, `M* = 959.6`, half-life 5.48 months, `M` = 1,234.4, 1,173.0, 1,105.6, 1,028.0. `ε = 1` gives `r = 0.084`, identical to the baseline path; volume index 0.5 from month 0.
- Step 3: `F = 678.6 × 0.084 ≈ 57`, a cut of 57 from 114 net, for example about 63% of the 90 in bounties. That is a very large faucet cut, which is itself an argument for a mixed or staged plan. `ε` drops out because the tax rate and velocity do not change.
- Step 4: Lab 13 month 11 velocity fell about 9%. A two-month 9% dip changes the 12-month `M` by well under 5%.

</details>

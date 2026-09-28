# MMO304 · Lab 10: Search cost and market design

**Week:** 10 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** part of the models assessment (30%)

## Objective

Check the search-cost model from [week 10](../lectures/w10-market-design-auction-houses-vendors-barter.md) by simulation, watch sellers undercut when buyers can see every ask, and then use the model to write a market design for a small MMO with numbers attached.

## Starter materials

- Python 3 with numpy and matplotlib (the program's reference stack), or a spreadsheet if you prefer. The Python route is expected for steps 3 and 4.
- The three formulas from week 10, section 2:
  - expected price after `k` checks, `L + (H − L) / (k + 1)`
  - total cost, `L + (H − L) / (k + 1) + k × c`
  - chance an ask `p` wins, `((H − p) / (H − L)) ^ (k − 1)`
- Fixed inputs for everyone: `L = 80`, `H = 120`, `N = 40` sellers, seed 10.
- The starter script below. Copy it into `lab10.py`.

```python
import numpy as np

L, H, N = 80.0, 120.0, 40
rng = np.random.default_rng(10)

def expected_min(k):
    return L + (H - L) / (k + 1)

def best_k(c, kmax=N):
    costs = [expected_min(k) + k * c for k in range(1, kmax + 1)]
    return int(np.argmin(costs)) + 1

def simulate_buyers(asks, k, n_buyers):
    """Each buyer checks k random sellers and buys the cheapest.
    Returns the prices paid and how many sales each seller made."""
    paid = np.empty(n_buyers)
    sales = np.zeros(len(asks), dtype=int)
    for b in range(n_buyers):
        idx = rng.choice(len(asks), size=k, replace=False)
        winner = idx[np.argmin(asks[idx])]
        paid[b] = asks[winner]
        sales[winner] += 1
    return paid, sales

def sellers_respond(asks, sales):
    """TODO (step 4): sellers with zero sales cut their ask.
    Rule from the week 10 interactive spec:
    new ask = max(L, ask - 0.25 * (ask - L) - 1)."""
    raise NotImplementedError

asks = rng.uniform(L, H, size=N)
```

## Steps

1. **Formula table.** Compute the expected price for `k = 1` to `20` and the best `k` for `c = 0.5, 1, 2, 3, 4, 6, 10`. Check three of your values against the tables in the lecture.
2. **Simulation check.** With fresh uniform asks each time, simulate 10,000 buyers for `k = 1, 3, 10`. Report the mean price paid and its 95% margin of error (MA102 week 11). Does the formula value fall inside the margin? If not, find your bug before going on.
3. **Seller win chances.** Using the simulation from step 2 with `k = 3`, bin sellers by ask (80-90, 90-100, 100-110, 110-120) and compute the share of buyers who checked a seller in each bin and bought from them. Compare with the formula at each bin's midpoint.
4. **Undercutting.** Implement `sellers_respond`. Run 10 rounds of 200 buyers each for `c = 6` (use `best_k`), then repeat for `c = 0` with `k = N`. Plot the lowest ask, median ask and highest ask per round for both cases on one chart.
5. **Fees.** Add a sale fee `f` to the auction case. A seller now nets `p × (1 − f)`, and a seller whose net would fall below a production cost of 78 refuses to cut further. Run `f = 0.02, 0.05, 0.15` and record where asks settle.
6. **Design brief.** Read the brief below and write your market design.

**Brief:** *Harbor Lights* is a small sailing MMO with about 3,000 players online on one server. It has four port towns a 10-minute voyage apart. Tradable goods are 12 commodities (fish, timber, spices and so on) and about 400 kinds of ship parts. The designers want a "trader captain" play style that earns money by knowing prices and carrying goods, and they want new players to buy ship parts at fair prices.

## Deliverable

`lab10.py` (or the spreadsheet), the chart from step 4, the table from step 5, and a design memo of 500-700 words. The memo must state, for commodities and for ship parts separately: scope (per port or whole server), search cost, visibility (asks only, or bids too), fees and where they are charged. It must predict the price spread for one commodity between ports using a number from your simulation, and name one way players could break your design.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Formula table and simulation check | All values correct, margins of error reported, formula inside the margin | Values correct, no margins or one mismatch unexplained | Wrong or missing | 20% |
| Seller win chances | Binned shares match the formula within noise, with a sentence on any gap | Computed but not compared | Missing | 15% |
| Undercutting chart | Both cases plotted and labelled, the collapse at `c = 0` visible and described | Plotted but hard to read or not described | Missing | 20% |
| Fees | Settling prices for all three fees with a correct explanation of the cost floor | Numbers given, explanation weak | Missing | 15% |
| Design memo | Separate, justified choices for both good types, a predicted spread with numbers, a credible exploit | Choices made but not tied to numbers | Opinion without the model | 30% |

<details>
<summary>Instructor check values</summary>

- Expected price: `k = 1` 100.00, `k = 3` 90.00, `k = 10` 83.64.
- Best `k`: `c = 0.5` gives 8, `c = 1` gives 5, `c = 2` gives 3 (gain 3 to 4 is exactly 2.0; the first minimum is at 3 under `argmin`), `c = 3` gives 3, `c = 4` gives 2, `c = 6` gives 2, `c = 10` gives 1.
- Simulated means with 10,000 buyers should land within about ±0.25 of the formula for `k = 3` (SD of the minimum of 3 uniforms on a width of 40 is about 7.7).
- Win chance at `k = 3`, bin midpoints: 85 → 76.6%, 95 → 39.1%, 105 → 14.1%, 115 → 1.6%.
- At `c = 0`, the highest ask should fall below about 90 within 10 rounds. At `c = 6` (`k = 2`), high asks still sell often and the spread shrinks much more slowly.
- With fees, asks cannot fall below `78 / (1 − f)`: 79.59 at 2%, 82.11 at 5%, 91.76 at 15%.

</details>

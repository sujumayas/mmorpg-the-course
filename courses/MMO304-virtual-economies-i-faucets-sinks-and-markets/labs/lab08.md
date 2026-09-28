# MMO304 · Lab 08: Item lifecycle simulation

**Week:** 8 (extended in week 9) · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the Models assignment (30%)

## Objective

Simulate the stock and price of three item types over one year, design a destruction rate for each that holds it at a target coverage, and price the gold that a repair rule removes. In week 9 you add a money item and watch a duplication exploit echo through a year of prices.

This lab uses [week 8](../lectures/w08-item-decay-durability-and-destruction-as-sinks.md): `S(t + 1) = S + F − d × S`, `S* = F / d`, `d = F / (c × N)`, `P ≈ max(floor, P_max × (1 − S / N))`, and the two repair-sink formulas. Part D uses [week 9](../lectures/w09-commodity-money-when-an-item-becomes-currency.md).

## Starter materials

- A blank spreadsheet with 366 rows (day 0 to day 365).
- Three item types from an invented game. All start at `S(0) = 0`.

| Item | New copies per day `F` | Players who want one `N` | `P_max` (gold) | Vendor floor | Target coverage `c` |
|---|---|---|---|---|---|
| Breastplate | 100 | 10,000 | 1,000 | 50 | 50% |
| Rare mount | 5 | 20,000 | 40,000 | 500 | 10% |
| Shield | 60 | 4,000 | 600 | 20 | 40% |

- Repair data. A time-decay helmet has a full repair cost of 90,000 gold over a 12-hour lifespan; a repair discount of `(1 − skill / 200)` applies for players with the Armoursmith skill. A death-decay armour set loses 10% durability per death and costs 400 gold to repair from zero.
- Week 9 extension. A money item with `F = 40` per day, `d = 0.2%` per day and `S(0) = 20,000`. A duplication exploit adds 60 extra copies per day on days 100 to 129.

## Steps

**Part A: no destruction.**
1. For each item, simulate `S(t)` and `P(t)` with `d = 0`. Record the day each item's price first reaches its floor, if it does within a year.

**Part B: designed destruction.**
2. For each item, derive `d` from the target coverage. Simulate `S(t)` and `P(t)` with that `d`.
3. For each item, report `S*`, mean lifetime `1/d`, days to half of `S*`, `S(365)` and `P(365)`. Which item is far from its steady state after a year, and why?
4. Plot stock and price for each item, with and without destruction, on linked charts (same time axis).

**Part C: repair sinks.**
5. For the time-decay helmet, compute the gold sink per hour of use for skill levels 0, 50 and 100.
6. For the death-decay set, compute the gold sink per hour for players dying 1, 3 and 10 times per hour. Who pays most?

**Part D (week 9): a money item.**
7. Simulate the money item with and without the exploit. Plot the difference between the two stocks from day 100 to day 365.
8. Taking prices quoted in the money item as proportional to its stock, how much higher are prices on day 130 and day 365 than without the exploit?

## Deliverable

The spreadsheet and a design note of about 400 words. It must recommend a destruction rule for each item in player-facing terms (for example, a per-death chance), cite `S*` and `P(365)` for each, compare the two repair sinks, and state how long the exploit's effect lasts.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Part A simulation | All three items correct, floor days identified | One item wrong | Two or more wrong | 15% |
| Part B design | `d`, `S*`, lifetime, half time, day-365 values correct; slow item explained | Values right, explanation missing | Values wrong | 25% |
| Linked charts | Stock and price on shared axis, with and without `d`, labelled | Charts present but hard to read | Missing | 15% |
| Part C repair sinks | All six values correct, the question of who pays answered | Values right, no discussion | Wrong | 15% |
| Part D money item | Both runs and the price gap at days 130 and 365 correct | One run wrong | Missing | 10% |
| Design note | Player-facing rules, numbers cited, trade-offs named | Rules given, numbers thin | No note or no numbers | 20% |

<details>
<summary>Instructor check values</summary>

- Part A floor days (`P_max × (1 − F t / N) ≤ floor`): breastplate day 95. Mount day 3,950, so not within a year (price on day 365 is `40,000 × (1 − 1,825/20,000) = 36,350`). Shield `t ≥ 64.4`, so day 65 in a daily sheet.
- Part B: breastplate `d = 2%`, `S* = 5,000`, lifetime 50 days, half at 34.3 days, `S(365) ≈ 4,997`, `P(365) ≈ 500`. Mount `d = 0.25%`, `S* = 2,000`, lifetime 400 days, half at 276.9 days, `S(365) ≈ 1,198`, `P(365) ≈ 37,600`. The mount is the slow one: small `d` means a long approach. Shield `d = 3.75%`, `S* = 1,600`, lifetime about 27 days, half at 18.1 days, `S(365) ≈ 1,600`, `P(365) ≈ 360`.
- Part C time-decay: 7,500 gold per hour at skill 0, 5,625 at 50, 3,750 at 100. Death-decay: 40, 120 and 400 gold per hour.
- Part D: without the exploit, the stock stays at 20,000. With `S(t + 1) = S(t) + F + extra(t) − d × S(t)` and `extra = 60` on days 100 to 129, the stock is about 21,749 on day 130 (an excess near 1,750, so prices about 8.7% higher), falling to about 21,092 on day 365 (still about 5.5% above). Students who count a day's extra copies on the same day get the same values one day earlier; accept either convention if stated.

</details>

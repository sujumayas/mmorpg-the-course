# MMO304 · Lab 01: Pricing scarcity in hours

**Week:** 1 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the Models assignment (30%)

## Objective

Turn a loot table into hours and gold before it ships. You will compute each item's expected farming time and long-run price, simulate 1,000 farmers to see how unevenly that cost falls, and redesign three drop rules to hit target prices with an acceptable dry tail.

This lab uses [week 1](../lectures/w01-why-virtual-economies-exist-artificial-scarcity.md): `T = t / p` and `P ≈ w × T`, with the median and 95th-percentile waits from [MA102 week 7](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md).

## Starter materials

- A spreadsheet (Google Sheets, Excel or LibreOffice Calc), or Python 3 with only the standard library.
- The loot table below. Copy it into your sheet as-is. It describes an invented game with a farming wage of `w = 450` gold per hour.

| Item | Source | Time per attempt | Drop chance | Tradeable | Target price (gold) |
|---|---|---|---|---|---|
| Linen scrap | Humanoid, level 10 | 25 s | 40% | Yes | 10 |
| Iron ore | Gathering node | 40 s | 100% (1 per node) | Yes | 6 |
| Wolf-fang charm | Wolf pack leader | 75 s | 4% | Yes | 600 |
| Ember staff | Dungeon end boss | 25 min | 8% | Yes | 3,000 |
| Stormglass ring | World boss, once per day | 15 min | 2% | Yes | 20,000 |
| Warden's crest | Raid boss, once per week | 3 h | 15% | No (soulbound) | — |

- Spreadsheet random draws for the simulation: `=RAND()` (Sheets, Excel, Calc). The number of attempts until a drop for one farmer is `=CEILING(LN(RAND()) / LN(1 - p), 1)`, which samples the geometric distribution directly. In Python, `math.ceil(math.log(random.random()) / math.log(1 - p))`, with `random.seed(304)` so results repeat.

## Steps

1. **Hours and price.** For each tradeable item, compute mean attempts `1/p`, expected hours `T = t / p` (convert `t` to hours first) and price `P = w × T`. For the Warden's crest compute `T` only, and write one sentence on why `P` does not apply.
2. **Tail.** For each item compute median attempts `ceil(ln 0.5 / ln(1 − p))` and 95th-percentile attempts `ceil(ln 0.05 / ln(1 − p))`, and convert both to hours. For the two rate-limited items (Stormglass ring and Warden's crest), also convert attempts into calendar days or weeks.
3. **Simulate.** For the Ember staff, draw 1,000 farmers' attempt counts. Report the sample mean, median and 95th percentile, and compare them with step 2. Plot a histogram with 30 bins.
4. **Compare to targets.** Put your computed price next to the target price. Mark each item as "too cheap", "on target" (within 20%) or "too expensive".
5. **Redesign three items.** Pick the three items furthest from their targets. For each, change one lever (chance, time per attempt, or a rate limit) to hit the target. Recompute price and tail. If a redesign makes the 95th-percentile wait more than 3 times the mean, propose a pity rule (for example, a guaranteed drop after `k` attempts) and estimate its effect on the mean.
6. **Wage shock.** A patch adds a zone that raises the farming wage to 700 gold per hour. Recompute all long-run prices. Write which items you would retune and which you would leave to inflate.

## Deliverable

The spreadsheet or script, the Ember staff histogram, and a memo of about 300 words to your design lead. The memo must give the before-and-after numbers for your three redesigns, name one item where you chose to accept a long tail and why, and state your response to the wage shock.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Hours and prices | All items correct, units converted, soulbound case explained | One or two errors | Three or more errors | 20% |
| Tail and calendar time | Median, 95th percentile and calendar waits correct | Tails correct, calendar time missing | Missing or wrong | 15% |
| Simulation | Seeded, 1,000 farmers, sample statistics within a few percent of theory, histogram labelled | Runs but unseeded or unlabelled | Missing | 20% |
| Redesigns | Three items on target, levers justified, tail checked, pity rule where needed | On target but tail ignored | Fewer than three or off target | 25% |
| Memo | Numbers from the sheet, a deliberate tail trade-off, a clear wage-shock plan | Recommendations without enough numbers | Opinion without numbers | 20% |

<details>
<summary>Instructor check values</summary>

- Linen scrap: `T = (25/3600)/0.4 = 0.01736` h, `P ≈ 7.8`. Median 2 attempts, 95th percentile 6.
- Iron ore: `T = 40/3600 = 0.0111` h, `P = 5.0`. No tail (every attempt succeeds).
- Wolf-fang charm: `T = (75/3600)/0.04 = 0.521` h, `P ≈ 234`. Median 17, 95th percentile 74. Too cheap against 600.
- Ember staff: `T = (25/60)/0.08 = 5.21` h, `P ≈ 2,344`. Median 9, 95th percentile 36 (15 h). Too cheap against 3,000 by 22%.
- Stormglass ring: `T = 0.25/0.02 = 12.5` h, `P = 5,625`. Median 35 attempts, 95th percentile 149 attempts, which at one attempt a day is 35 and 149 days. Too cheap against 20,000. Note the calendar tail is already long, so lowering `p` makes it worse; raising `t` (a longer fight) or adding a key item cost is a better lever.
- Warden's crest: `T = 3/0.15 = 20` h, mean 6.7 weeks, 95th percentile 19 weeks.
- Wage shock at 700: every tradeable price scales by `700/450 = 1.556`, for example the Ember staff to about 3,646.

</details>

# MMO403 · Week 09 — Whales and Spending Distributions

**Why this matters:** In a free-to-play game, a few percent of players pay, and a few percent of those pay most of the money. That shape decides how risky your revenue is, how noisy your tests are, what a spending limit would cost, and whose wellbeing your business depends on. This week you learn to draw the shape, to read one number off it without being fooled, and to price a protection before you argue about it.

**You will be able to:**
- Draw the Lorenz curve of player spend from a list of spends, and compute the Gini coefficient and top-share figures from it.
- Derive why a Gini over all players is almost fixed by the payer rate, and use the payer-only curve instead.
- Compute the revenue cost and the share of payers affected by a monthly spending cap under a Pareto model.
- Critique claims about "whales" against the research, stating what the evidence does and does not show.

**Before class:** Close, J., Spicer, S. G., Nicklin, L. L., Uther, M., Lloyd, J. & Lloyd, H. (2021), "Secondary analysis of loot box data: Are high-spending 'whales' wealthy gamers or problem gamblers?", *Addictive Behaviors* 117, 106851 (short; the preprint is free on PsyArXiv). Reread section 2, "The second view: who actually pays", of GS101 week 11. Fields & Cotton, *Social Game Design: Monetization Methods and Mechanics* (Morgan Kaufmann, 2011), the material on paying players and high spenders.

**Prerequisites from earlier courses:** [GS101 week 11, free-to-play, mobile and live service](../../GS101-history-and-critical-study-of-games/lectures/w11-free-to-play-mobile-and-live-service.md) (the whale, dolphin and minnow terms; the Pareto shape `α` and the top-share rule `q^(1 − 1/α)`; the Swrve 2014 figures; this lecture builds on all of them and does not repeat the fit). [MA102 week 12, descriptive statistics](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md) (why mean and median part ways in skewed data). [MMO308 week 6, A/B testing statistics](../../MMO308-live-operations-analytics-and-experimentation/lectures/w06-ab-testing-statistics-and-pitfalls.md) (whales as a source of noise, and capping spend in tests). [MMO308 week 7, segmentation](../../MMO308-live-operations-analytics-and-experimentation/lectures/w07-segmentation.md). If you are taking it alongside, [MMO401 week 2](../../MMO401-virtual-economies-ii-markets-governance-and-macr/lectures/w02-agent-based-modeling-i.md) derives the Gini coefficient for gold balances; we apply the same formula to spending. From this course, [week 2, unit economics](w02-unit-economics-ltv-cac-arppu.md) and [week 6, loot boxes and disclosure](w06-loot-boxes-and-probability-disclosure.md) (the evidence on harm).

**Interactive:** [Spending Lorenz curve](../examples/w09-spend-lorenz.html). Keep it open during section 2.

---

## 1. Three numbers for one shape

Any month of spending in a live game is a list: one amount per active player, most of them zero. Three summaries of that list come up again and again.

- The **payer rate** `p` is the share of players who spent anything. Week 2 used it as a factor of ARPDAU.
- A **top share** is the share of revenue from the top fraction of spenders, such as "the top 10% of payers produced half of revenue". Always ask whether the fraction is of players or of payers. They differ by a factor of `1/p`.
- The **Gini coefficient** `G` is a single number from 0 (everyone spends the same) to 1 (one player spends everything). MMO401 week 2 computes it for gold balances. For a sorted list `x_1 ≤ x_2 ≤ ... ≤ x_n` with total `X`, it is

```
G = Σ (2i − n − 1) × x_i  /  (n × X)        (i = 1 ... n)
```

All three are read off one picture, the Lorenz curve.

The **Lorenz curve** sorts players from the smallest spender to the largest. The horizontal axis is the cumulative share of players, the vertical axis the cumulative share of revenue. If everyone spent the same, the curve would be the diagonal. The more concentrated the spending, the more the curve sags below it. The Gini coefficient is twice the area between the diagonal and the curve. A top share is read from the right-hand end: the top 10% of players hold `1 − L(0.9)` of revenue, where `L(F)` is the curve's height at `F`.

Economists draw Lorenz curves of income and wealth. For a game, spending is the natural choice, because spending is what the business model runs on and what the harm research measures.

## 2. Worked example: the curve that hides the whales

### The hook

Industry lore says the biggest spenders in free-to-play games are wealthy hobbyists who can afford it. In 2021 James Close and colleagues put that to a test. They pooled six open survey datasets covering 7,767 loot box buyers, with self-reported monthly spend and a problem gambling score (PGSI), and self-reported earnings for 5,933 of them.

Two results. First, spending was very concentrated. About 5% of buyers, those spending over $100 a month, produced about half of loot box revenue, and about 2% produced about 30%. Second, spending tracked problem gambling scores (Spearman's ρ = 0.34), while it did not track earnings (ρ = 0.02, not significant). In their figure, buyers spending under $100 a month had a mean PGSI of 1.3 (low risk), and those spending $500 or more had a mean of about 9.75, in the problem-gambling range.

Both results come from one shape. To reason about it, you need to draw it correctly, and the obvious way to draw it hides almost everything.

### The model

Split players into non-payers (a share `1 − p`, spending zero) and payers (a share `p`). Let `L_pay(F)` be the Lorenz curve of payers alone. The curve for all players is flat along the bottom axis for the first `1 − p` of players, then follows the payers' curve squeezed into the last `p`:

```
L_all(F) = 0                             for F ≤ 1 − p
L_all(F) = L_pay( (F − (1 − p)) / p )    for F > 1 − p
```

The area under `L_all` is therefore `p` times the area under `L_pay`. Since `G = 1 − 2 × (area under the curve)`,

```
G_all = 1 − p × (1 − G_pay) = (1 − p) + p × G_pay
```

This is the key identity of the week. **The all-player Gini is the non-payer share plus a small correction.** With `p = 4%`, `G_all` must lie between 0.96 and 1.00 whatever the payers do.

For the payers, use GS101's Pareto model with shape `α`. Its Lorenz curve and Gini are

```
L_pay(F) = 1 − (1 − F)^(1 − 1/α)
G_pay    = 1 / (2α − 1)
```

and the top fraction `q` of payers holds `q^(1 − 1/α)` of revenue, as in GS101. Smaller `α` means more concentration.

### Numbers you can check

**A server of 20 players.** Fifteen spend nothing this month. Five spend $1, $2, $5, $12 and $80, a total of $100. Here is the code, which you can run as shown:

```python
def gini(xs):
    xs = sorted(xs)
    n, total = len(xs), sum(xs)
    return sum((2 * i - n - 1) * x for i, x in enumerate(xs, start=1)) / (n * total)

spend = [0] * 15 + [1, 2, 5, 12, 80]
payers = [x for x in spend if x > 0]
p = len(payers) / len(spend)

print(f"payer rate {p:.2f}")
print(f"G_pay {gini(payers):.3f}  G_all {gini(spend):.3f}  identity {(1 - p) + p * gini(payers):.3f}")
running = 0
for k, x in enumerate(sorted(spend), start=1):
    running += x
    if k >= 15:
        print(f"F = {k / 20:.2f}  L = {running / sum(spend):.2f}")
```

It prints:

```
payer rate 0.25
G_pay 0.672  G_all 0.918  identity 0.918
F = 0.75  L = 0.00
F = 0.80  L = 0.01
F = 0.85  L = 0.03
F = 0.90  L = 0.08
F = 0.95  L = 0.20
F = 1.00  L = 1.00
```

The top player (5% of the server) holds `1 − 0.20 = 80%` of revenue. The top two (10%) hold 92%. The identity checks: `0.75 + 0.25 × 0.672 = 0.918`.

**Pareto payers at a 4% payer rate.** Now vary the payers' shape and watch the two Gini numbers.

| Shape `α` | `G_pay` | `G_all` (p = 4%) | Top 1% of players' share | Top 10% of payers' share |
|---|---|---|---|---|
| 1.16 | 0.758 | 0.990 | 82.6% | 72.8% |
| 1.43 | 0.538 | 0.982 | 65.9% | 50.0% |
| 2 | 0.333 | 0.973 | 50.0% | 31.6% |
| 3 | 0.200 | 0.968 | 39.7% | 21.5% |

(The top 1% of players is the top 25% of payers when `p = 4%`, so its share is `0.25^(1 − 1/α)`.)

Read the columns side by side. Across the four rows, the top 1% of players goes from holding 40% of revenue to holding 83%. Those are very different businesses. `G_all` moves from 0.968 to 0.990, a change you would round away on a dashboard. `G_pay` moves from 0.20 to 0.76 and tells the story.

### The visual

Open `examples/w09-spend-lorenz.html`. The left chart is the all-player Lorenz curve. At a 4% payer rate it runs along the bottom axis for 96% of the width and then shoots up the right edge. Drag `α` from 3 to 1.16. The left chart barely moves. The right chart is the payer-only Lorenz curve, and it sags deeper as you drag. Both charts show the same data. The left one is what you get if you plot "all players" by reflex, and it hides the whale structure behind the non-payers. Drag `p` next and watch `G_all` follow it almost one for one.

### Cross-game recognition

Rewrite each published figure as a point on a Lorenz curve, then ask which `α` it implies.

**Swrve's mobile network (January 2014, via GS101 week 11).** 1.5% of players paid, and 0.15% of players produced half of revenue. In payer terms, the top 10% of payers held 50%, which fits `α ≈ 1.43`. The all-player Gini would be about `0.985 + 0.015 × 0.538 ≈ 0.993`, which tells you nothing the payer rate didn't.

**Close and colleagues' loot box buyers (surveys up to March 2020, published 2021).** Here the population is buyers, so it is already a payer-only curve. Top 5% holding half fits `0.05^(1 − 1/α) = 0.5`, so `α ≈ 1.30` and `G_pay ≈ 0.62`. But the same `α` predicts the top 2% should hold about 40%, and the paper reports about 30%. The Pareto shape overstates the very top of this dataset. Part of the reason is the method: the authors removed 24 respondents reporting over $1,000 a month as outliers, which trims exactly the top tail. One point is not enough to fit a shape. Check a second.

**A mobile puzzle game (Sifa and colleagues, AIIDE 2015).** Tracking over 100,000 new players of a Wooga free-to-play puzzle game for 30 days, the authors found that fewer than 2% became paying players. With `p < 2%`, `G_all > 0.98` before you know anything about how those payers spent. The paper's whole method (oversampling the rare payers to train a classifier) exists because of that shape.

**Gold in an MMO economy (MMO401 week 2).** A random-exchange economy settles at a wealth Gini of about 0.5. Spending Ginis among payers in the table above run from 0.2 to 0.76, and all-player spending Ginis are near 1. Same formula, different quantity: a spending distribution with non-payers is far more concentrated than any wealth distribution a fair trading game produces.

Four sources, one curve. When someone quotes a concentration number, locate it on the curve: which population, what fraction, which month.

### Eyes-open design judgment

- **Plot payers separately.** An all-player Gini or Lorenz curve mostly measures `p`. Report `p` and the payer-only curve (or `G_pay` and two top shares) instead.
- **Two points, not one.** A single top share fits any Pareto `α`. Quote two (for example top 1% and top 10% of payers) and check they agree with one shape before you model with it.
- **Concentration is a risk measure.** If a quarter of revenue comes from a few hundred accounts, a change that annoys them, a competitor that courts them, or a law that caps them moves your revenue by that quarter. Week 14 asks you to state this number in a pitch.
- **Concentration is also a harm signal.** Close and colleagues' data link the steep end of the curve with high problem gambling scores, not high incomes. That is a correlation from self-reports, but it is the part of the curve where your design choices matter most.

### Check this example

1. A game has 50,000 monthly players, 3% of them payers, and a payer Gini of 0.60. What is the all-player Gini?
2. A payer population follows a Pareto shape with `α = 2`. What share of revenue comes from the top 20% of payers? From the top 5%?
3. A dashboard shows "spending Gini fell from 0.985 to 0.975 this month; spending is more equal". The payer rate rose from 2% to 3% in the same month after a starter pack. Is the claim right?

<details>
<summary>Answers</summary>

1. `G_all = 0.97 + 0.03 × 0.60 = 0.988`.
2. `1 − 1/α = 0.5`, so the top 20% hold `0.2^0.5 = 44.7%` and the top 5% hold `0.05^0.5 = 22.4%`.
3. Not necessarily. With `p = 2%`, `G_all ≥ 0.98`, and with `p = 3%`, `G_all ≥ 0.97`. The fall is about the size you'd expect from the payer rate alone, so it says almost nothing about how payers spend. Solve for `G_pay` in each month: `(0.985 − 0.98)/0.02 = 0.25` and `(0.975 − 0.97)/0.03 = 0.17`. Payers' spending did become somewhat more equal, probably because many new payers bought the same cheap pack. Look at the payer curve and a top share to see whether the big spenders changed at all.

</details>

## 3. What a spending cap costs

The concentration that makes whales valuable also makes protecting them expensive. You can put a number on that before the argument starts.

Suppose a game caps each account's spending at `C` per month. Under the Pareto model with minimum spend `x_m` and shape `α`, two quantities follow from integrating the tail:

```
share of payers above the cap      = (x_m / C)^α
share of revenue lost to the cap   = (x_m / C)^(α − 1) / α
```

(The revenue lost is the spending above `C` by those over it. It assumes they don't move that money into anything else.) The minimum spend comes from the mean: `x_m = A × (α − 1) / α`, where `A` is ARPPU.

Use GS101's figures, `A = $17.32` a month and `α = 1.43` (the Swrve fit), so `x_m = 17.32 × 0.43 / 1.43 = $5.21`.

| Monthly cap `C` | Payers affected | Revenue lost |
|---|---|---|
| $50 | 3.94% | 26.4% |
| $100 | 1.46% | 19.6% |
| $200 | 0.54% | 14.6% |
| $500 | 0.15% | 9.8% |

Check the $100 row. `x_m / C = 0.0521`. `0.0521^1.43 = 0.0146`, so 1.46% of payers are affected. `0.0521^0.43 = 0.281`, and `0.281 / 1.43 = 0.196`, so 19.6% of revenue is lost.

A cap that touches one payer in seventy removes a fifth of the revenue. That single row explains both sides of the whale debate. To a business, the top of the curve is where the money is, so any protection there is expensive. To a critic, a business that loses a fifth of its revenue by limiting 1.5% of payers to $100 a month depends heavily on those few accounts, and the research in section 2 says some of them are the players at most risk.

Neither conclusion follows from the model alone. The model tells you what the choice costs. Some facts to weigh when you make it:

- **What protections exist.** China capped minors' monthly spending at 200 to 400 yuan by age from 2019 (week 7). The UK industry guidance of 2023 asks for spending controls for all players. The EU CPC principles (week 3) ask studios to avoid business models aimed at players willing to spend excessive amounts. A player-set limit with a cooling-off period costs less than a hard cap, because most high spenders never set one, and it helps the ones who want help.
- **What the evidence says, and doesn't.** The Close study is cross-sectional and self-reported, drawn from surveys of people who chose to answer. It shows that high spend goes with high problem gambling scores and not with income. It does not show that spending causes gambling problems, and it cannot tell you about any one player. Week 6 covers the wider literature, including a Chinese sample where the correlation did not replicate.
- **Why many high spenders are fine.** Some players spend a lot because they love the game, play it for years and have the means. The model can't tell them apart from players in trouble. Your telemetry can help (sudden jumps in spend, late-night sessions, chasing after losses on random items), but acting on those signals raises its own privacy questions (MMO402 week 12).

## 4. Living with a concentrated curve

A concentrated curve changes several everyday practices.

**Testing.** Revenue per player has enormous variance when a few players carry most of it. MMO308 week 6 showed how one extra whale can flip an A/B result, and how capping each player's spend in the analysis (winsorizing) tames the noise. Note that capping in the analysis is not the same as capping in the game. The first is a statistical choice, the second a design choice.

**Segmentation and targeting.** Sorting payers into spend bands is ordinary analytics (MMO308 week 7). What you do with the bands is an ethical choice. Week 10 will argue against targeting price rises at predicted big spenders. The same logic applies to targeting offers, personal "account managers" and exclusive events at the top band: the players most responsive to them are, on the evidence of section 2, disproportionately those at risk.

**Forecasting.** If 20% of revenue comes from 1.5% of payers, a forecast built on average ARPPU is fragile. Week 2's LTV works on averages. Report the share of revenue from the top 1% of spenders next to it, so readers see how much of the average rests on a few accounts.

**Design direction.** Products with a price ceiling push the curve toward the diagonal. A battle pass caps what most payers spend on it each season (week 5). A subscription token (week 11) sells a fixed price per unit. Direct-purchase cosmetics at a range of price points widen the paying base. None of these removes the top of the curve, but each raises `p` and flattens the payer curve, which lowers the business's dependence on it.

## In-class activity (25 minutes)

Groups of three. The instructor hands each group a printed month of spending for an invented game (60 accounts, about 5% payers).

1. (7 min) Sort the list and plot the Lorenz curve by hand on the grid provided, for all players and for payers only.
2. (6 min) Compute `p`, `G_pay` with the sorted formula, and `G_all` with the identity. Check `G_all` directly for one group member.
3. (6 min) Pick a monthly cap. Compute, from the list (not the Pareto formula), the share of payers affected and the share of revenue lost. Compare with the Pareto table.
4. (6 min) Write a three-sentence recommendation: a cap, a player-set limit, or neither, with the numbers and one piece of evidence from section 3.

Expected output: two curves, three numbers, the cap calculation from the data, and the recommendation.

## Common misconceptions

- **"A Gini of 0.98 means our whales are extreme."** At a 2-4% payer rate it means mostly that most players don't pay. Use the payer-only Gini.
- **"Whales are rich players who can afford it."** In the one pooled dataset that tested this, loot box spend tracked problem gambling scores, not earnings. That is a correlation in self-reports, but it is the best evidence available, and it points the other way from the lore.
- **"A spending cap only affects a handful of people, so it can't cost much."** In the section 3 model, a $100 cap affects 1.46% of payers and removes 19.6% of revenue. Few people, much money.
- **"One top-share figure pins down the distribution."** Any single top share fits a Pareto curve. The Close data show how a second point can disagree with the first fit.

## Check yourself

1. A month's spend list has 1,000 players. 960 spend nothing, and the 40 payers have a Gini of 0.55. What is the all-player Gini? What would it be if the payer rate doubled to 8% with the same payer Gini?
2. The top 10% of payers produce 60% of revenue. Find `α` for a Pareto fit and predict the top 1% share. Then compute `G_pay`.
3. With `A = $17.32` and `α = 1.43`, what monthly cap removes 10% of revenue? Roughly what share of payers does it touch?
4. A producer says, "Our revenue is safe; the top 1% of spenders only account for 1% of our players." Explain why the statement is empty and name the number the producer should report instead.

<details>
<summary>Answers</summary>

1. `G_all = 0.96 + 0.04 × 0.55 = 0.982`. At `p = 8%`: `0.92 + 0.08 × 0.55 = 0.964`.
2. `0.1^(1 − 1/α) = 0.6` gives `1 − 1/α = ln 0.6 / ln 0.1 = 0.2218`, so `α ≈ 1.285`. The top 1% share is `0.01^0.2218 ≈ 36%`. `G_pay = 1 / (2 × 1.285 − 1) ≈ 0.64`.
3. Solve `(5.21 / C)^0.43 / 1.43 = 0.10`: `(5.21 / C)^0.43 = 0.143`, so `5.21 / C = 0.143^(1/0.43) ≈ 0.0109` and `C ≈ $480`. It touches `0.0109^1.43 ≈ 0.16%` of payers. This matches the $500 row (9.8%, 0.15%).
4. The top 1% of spenders are 1% of players by definition. The number that measures dependence is their share of revenue (and, better, two top shares or `G_pay`), which could be anywhere from about 10% to over 80%.

</details>

## Lab / assignment hook

[Lab 09, the spending curve of a live game](../labs/lab09.md). You implement the Lorenz curve, the Gini coefficient, the identity and the cap calculation, run them on a synthetic month of 20,000 accounts, fit a Pareto shape from one top share and check it against the others, and write a 400-word memo recommending a spending protection with its measured cost. The model results feed the models component (40%).

## Sources

- Close, J., Spicer, S. G., Nicklin, L. L., Uther, M., Lloyd, J. & Lloyd, H. (2021). "Secondary analysis of loot box data: Are high-spending 'whales' wealthy gamers or problem gamblers?" *Addictive Behaviors* 117, 106851. doi:10.1016/j.addbeh.2021.106851. Preprint doi:10.31234/osf.io/fvdrx (checked). 7,767 loot box purchasers from six open datasets (searches to 28 March 2020); 5,933 with earnings; 24 respondents over $1,000 a month removed; top ~5% (over $100 a month) about half of revenue, top ~2% about 30%; ρ = 0.34 with PGSI; ρ = 0.02 with earnings, not significant; mean PGSI 1.3 under $100 a month and about 9.75 at $500 or more.
- Sifa, R., Hadiji, F., Runge, J., Drachen, A., Kersting, K. & Bauckhage, C. (2015). "Predicting Purchase Decisions in Mobile Free-to-Play Games." *Proceedings of AIIDE 2015*, 79-85. doi:10.1609/aiide.v11i1.12788. Over 100,000 players of a Wooga free-to-play puzzle game over 30 days; premium players below 2%; oversampling of the minority class.
- Johnson, E. (26 February 2014). "A Long Tail of Whales: Half of Mobile Games Money Comes From 0.15 Percent of Players." *Recode*. Swrve's January 2014 figures, as used in GS101 week 11.
- King Digital Entertainment plc, Form F-1/A (25 March 2014), via GS101 week 11. ARPPU of US$17.32 per month (Q4 2013), used here as `A`.
- National Press and Publication Administration (China) and Wikipedia, "Loot box" (accessed 28 September 2026), for minors' spending limits from November 2019; UK DCMS (18 July 2023) for the industry guidance on spending controls; CPC Network key principles (21 March 2025) as summarized in week 3.
- Fields, T. & Cotton, B. (2011). *Social Game Design: Monetization Methods and Mechanics*. Morgan Kaufmann.
- The Pareto Lorenz curve `1 − (1 − F)^(1 − 1/α)`, Gini `1/(2α − 1)` and the cap formulas are standard results for the Pareto distribution. The 20-player server and all table values were computed by the author with the code shown.

## Interactive spec: examples/w09-spend-lorenz.html

**Purpose.** Show that the Lorenz curve of all players is dominated by non-payers, so the payer-only curve is the one that reveals concentration, and that a spending cap's cost follows from that concentration. Insight on first load: *with 4% payers, dragging α from 3 to 1.16 barely changes the left chart (Gini 0.968 to 0.990) while the right chart sags from Gini 0.20 to 0.76.*

**Layout.** Two square charts side by side on desktop, stacked on mobile. Left, "All players": `L_all(F)` with the diagonal. Right, "Payers only": `L_pay(F)` with the diagonal. Both axes 0 to 100%, gridlines every 10%. Under the charts, a cap panel and a numbers table. Generic lines only; no game names in the charts.

**Formulas.**
- `L_pay(F) = 1 − (1 − F)^(1 − 1/α)`; `G_pay = 1/(2α − 1)`.
- `L_all(F) = 0` for `F ≤ 1 − p`, else `L_pay((F − (1 − p))/p)`; `G_all = (1 − p) + p × G_pay`.
- Top fraction `q` of payers: `q^(1 − 1/α)`. Top fraction `t` of players (for `t ≤ p`): `(t/p)^(1 − 1/α)`; for `t > p`: 100%.
- Cap: `x_m = A(α − 1)/α`; payers above `C`: `(x_m/C)^α` (100% if `C ≤ x_m`); revenue lost: `(x_m/C)^(α − 1)/α` (if `C ≤ x_m`, lost = `1 − C/A`). Draw the capped payer curve as a dashed line on the right chart: capped spend `min(x, C)`, computed numerically on 2,000 quantiles.

**Controls.**
- `p` payer rate: 0.5% to 30%, step 0.1%, default 4%.
- `α`: 1.05 to 4.00, step 0.01, default 1.43.
- `A` ARPPU: $1 to $100, step 0.01, default 17.32.
- Cap `C`: toggle (default off) and slider $10 to $2,000 on a log scale, default $100.
- Presets: "Swrve 2014" (p 1.5%, α 1.43), "Close et al. fit" (α 1.30 in a "buyers only" mode that sets p to 100%, outside the slider range; the p slider parks at its 30% end and the readout shows "100% (buyers only)"; moving the p slider leaves the mode), "Toy server" (switch to data mode: plot the step Lorenz curve of 0×15, 1, 2, 5, 12, 80).
- All controls keyboard operable; charts redraw on input.

**Numbers table.** `p`, `G_pay`, `G_all`, top 1% / 10% of players' share, top 1% / 10% / 20% of payers' share, `x_m`, and with the cap on: payers affected, revenue lost, and capped `G_pay`.

**Test values.**
- p 4%, α 1.43: `G_pay` 0.538, `G_all` 0.982, top 1% of players 65.9%, top 10% of payers 50.0%.
- α 1.16: `G_pay` 0.758, `G_all` 0.990, top 1% of players 82.6%. α 2: 0.333, 0.973, 50.0%. α 3: 0.200, 0.968, 39.7%.
- Swrve preset: `G_all` ≈ 0.993.
- Toy server: `G_pay` 0.672, `G_all` 0.918; Lorenz points (0.75, 0), (0.80, 0.01), (0.85, 0.03), (0.90, 0.08), (0.95, 0.20), (1, 1).
- Cap with A 17.32, α 1.43 (`x_m` 5.21): C $50 → 3.94% of payers, 26.4% lost; $100 → 1.46%, 19.6%; $200 → 0.54%, 14.6%; $500 → 0.15%, 9.8%.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. The two curves differ by colour and line style; the diagonal is dotted and labelled "equal spending". Provide a text summary that updates ("Payers only: Gini 0.54; top 10% of payers hold 50%"). Respect `prefers-reduced-motion` and `prefers-color-scheme`.

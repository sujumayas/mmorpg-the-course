# MMO403 · Week 10 — Pricing Experiments

**Why this matters:** Every price in your store is a guess until you test it, and the first number you will look at, conversion, points the wrong way. Raise a price and fewer people buy, so the dashboard turns red, even when the studio earns more. This week you learn what a price test should measure, why that measure needs far more players than a normal A/B test, and how to run one in a world where players compare notes and the law cares about what they see.

**You will be able to:**
- Compute revenue per exposed player, the break-even conversion and the arc elasticity for a price change, and say from those numbers whether the change raised revenue.
- Calculate the players per arm a price test needs for a conversion metric and for a revenue metric, and explain why the second is larger and explodes near the best price.
- Choose a test design (player split, region, time switchback, offer test or survey) for a given price question in a shared world, and name the fairness and legal constraints that apply.
- Critique a price-change announcement or readout that reports conversion without revenue, or revenue without a horizon.

**Before class:** Fields, T. & Cotton, B., *Social Game Design: Monetization Methods and Mechanics* (Morgan Kaufmann, 2011), the chapter on pricing and the sections on testing store offers. Kohavi, R., Tang, D. & Xu, Y. (2020), *Trustworthy Online Controlled Experiments*, chapter 7 (metrics and the overall evaluation criterion); reread the section on revenue metrics. Reread your notes from MMO308 weeks 5 and 6.

**Prerequisites from earlier courses:** [MA102 week 14, hypothesis testing and A/B](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w14-intro-to-hypothesis-testing-ab.md) (the two-proportion z-test, power and the sample-size formula; its SimCity pre-order example is a store test you should recall, not a new one). [MMO308 week 5, A/B testing design](../../MMO308-live-operations-analytics-and-experimentation/lectures/w05-ab-testing-design.md) (the experiment plan, the randomization unit, and its section 6 on testing prices on people who talk to each other). [MMO308 week 6, A/B statistics and pitfalls](../../MMO308-live-operations-analytics-and-experimentation/lectures/w06-ab-testing-statistics-and-pitfalls.md) (peeking, and its section 5 on whale-driven revenue noise, capping and splitting the metric). [MMO308 week 2, KPIs](../../MMO308-live-operations-analytics-and-experimentation/lectures/w02-kpis-dau-mau-stickiness-arpdau.md) (the KPI tree with payer rate and ARPPU). From this course, [week 2, unit economics](w02-unit-economics-ltv-cac-arppu.md) (LTV), [week 8, dark patterns](w08-dark-patterns.md) and [week 9, whales and spending distributions](w09-whales-and-spending-distributions.md).

**Interactive:** [Price test](../examples/w10-price-test.html). Keep it open during section 2.

---

## 1. What a price test is for

A **price test** is an experiment in which the thing that changes between arms is what a player pays, or how the price is presented. It can change the list price, the size of a bundle at a fixed price, a discount, or the order in which offers appear. Everything you learned about experiments in MA102 and MMO308 still applies. What changes is the metric.

Some terms, used the same way all week:

- **Exposed player.** A player who saw the offer in the test window. Only exposed players count, which is MMO308 week 5's triggering rule.
- **Conversion** `c`. The share of exposed players who bought.
- **ARPPU** (average revenue per paying user). Revenue divided by buyers. For a single item at one price, ARPPU is just the price `p`.
- **Revenue per exposed player** `RPE`. Revenue divided by exposed players. For a single item, `RPE = p × c`.
- **Demand curve.** Conversion as a function of price, `c(p)`. It slopes down. Higher prices lose buyers.
- **Elasticity** `ε`. The percentage change in conversion caused by a 1% change in price. It is negative for normal goods. When `|ε| < 1`, demand is **inelastic** and a price rise increases revenue. When `|ε| > 1`, demand is **elastic** and a price rise loses revenue.

MMO308 week 2 split revenue into payer rate times ARPPU. A price test pushes those two factors in opposite directions on purpose. The whole skill this week is to read the product, not either factor alone.

## 2. Worked example: the price test that turned the dashboard red

### The hook

World of Warcraft launched in 2004 with a US subscription of US$15 a month. In 2026 the one-month plan still costs US$15. Prices in the US economy did not stand still. The US consumer price index averaged 188.9 in 2004 and 321.9 in 2025, so the 2004 price is worth about US$25.56 in 2025 dollars. In real terms, a month of WoW has become about 41% cheaper.

In a PC Gamer interview at GDC in March 2024, Blizzard's John Hight explained why the price had not moved. He said, in effect, that he would rather keep a large, healthy audience than risk driving players away with an increase. Is that leaving money on the table, or wise? You cannot answer from the price alone. You need to know how many players a higher price would lose. That number is what a price test measures, and it is also why Blizzard cannot simply A/B test it. A subscription price in a shared world is visible, and every subscriber would learn that someone else pays less.

Start with a test you *can* run. Your MMO sells a starter bundle to new players. It costs US$4.99, and 5.0% of the new players who see it buy it. The monetization team tests US$6.99 against it. After two weeks, conversion in the new arm is 4.0%. The dashboard shows a 20% drop in purchases in red. Someone asks for the test to be killed.

### The model

For one item at one price:

```
RPE(p)          = p × c(p)                    revenue per exposed player
break-even c1   = c0 × p0 / p1                conversion the new price must keep to tie
arc elasticity  ε = [(c1 − c0) / c̄] / [(p1 − p0) / p̄]      with c̄, p̄ the midpoints
```

- `p0` and `c0` are the old price and its conversion. `p1` and `c1` are the new ones.
- `RPE` is what the studio earns per player who saw the offer. It is the number that decides the test.
- The break-even line comes from setting `p1 × c1 = p0 × c0`. Any result above it earns more than the old price.
- The **arc elasticity** uses midpoints, so going from A to B gives the same answer as going from B to A.

For this week's numbers, suppose the true demand is a straight line. Conversion falls half a percentage point for every dollar above US$4.99.

```
c(p) = 0.05 − 0.005 × (p − 4.99)
```

Straight-line demand is a teaching simplification. Real curves bend. But it has one property every downward demand curve shares. Revenue rises, peaks and falls. For a straight line the peak sits exactly where `|ε| = 1`, at `p* = 7.495` here.

### Numbers you can check

The script below computes the demand line, revenue per 1,000 exposed players, and the players per arm a test against US$4.99 needs. The two sample-size functions use MA102 week 14's formula at `α = 0.05` two-sided and 80% power. The first detects a change in conversion. The second detects a change in revenue per exposed player, where each player's revenue is `p` with probability `c` and 0 otherwise, so its variance is `p² × c × (1 − c)`.

```python
Z = 1.96 + 0.8416          # two-sided 5% test, 80% power (MA102 week 14)

def conversion(p):         # the week's demand line: 5% at $4.99, minus 0.5 points per dollar
    return 0.05 - 0.005 * (p - 4.99)

def n_rate(c0, c1):        # players per arm to detect a change in conversion
    return Z**2 * (c0 * (1 - c0) + c1 * (1 - c1)) / (c1 - c0) ** 2

def n_revenue(p0, p1):     # players per arm to detect a change in revenue per exposed player
    c0, c1 = conversion(p0), conversion(p1)
    var = p0**2 * c0 * (1 - c0) + p1**2 * c1 * (1 - c1)
    return Z**2 * var / (p1 * c1 - p0 * c0) ** 2

base = 4.99
for p in (3.99, 4.99, 5.99, 6.99, 7.99, 8.99, 9.99):
    c = conversion(p)
    line = f"${p:.2f}  conv {c:.2%}  per 1,000 exposed ${1000 * p * c:7.2f}"
    if p != base:
        line += f"  n(conv) {n_rate(conversion(base), c):>7,.0f}  n(rev) {n_revenue(base, p):>9,.0f}"
    print(line)
```

Output:

```
$3.99  conv 5.50%  per 1,000 exposed $ 219.45  n(conv)  31,231  n(rev)    17,473
$4.99  conv 5.00%  per 1,000 exposed $ 249.50
$5.99  conv 4.50%  per 1,000 exposed $ 269.55  n(conv)  28,405  n(rev)    53,199
$6.99  conv 4.00%  per 1,000 exposed $ 279.60  n(conv)   6,742  n(rev)    26,501
$7.99  conv 3.50%  per 1,000 exposed $ 279.65  n(conv)   2,835  n(rev)    28,830
$8.99  conv 3.00%  per 1,000 exposed $ 269.70  n(conv)   1,503  n(rev)    67,991
$9.99  conv 2.50%  per 1,000 exposed $ 249.75  n(conv)     903  n(rev) 454,031,991
```

Check the US$6.99 row by hand. `RPE = 6.99 × 0.04 = 0.2796`, so US$279.60 per 1,000 exposed players against US$249.50. That is a 12.1% gain, with 20% fewer buyers. The break-even conversion is `0.05 × 4.99 / 6.99 = 3.57%`. The test observed 4.0%, comfortably above it. The arc elasticity is `(−0.01 / 0.045) / (2 / 5.99) = −0.222 / 0.334 = −0.67`. Its size is below 1, so demand is inelastic in this range and the price rise pays.

Read the table as three lessons.

1. **Conversion always falls. Revenue does not.** Every row above US$4.99 has lower conversion. Revenue climbs to about US$281 per 1,000 at US$7.49, then falls. The red dashboard was measuring the wrong thing.
2. **The top of the curve is flat.** US$6.99 and US$7.99 earn within 5 cents per 1,000 players of each other. Near the best price, getting the price exactly right is worth almost nothing, and the table's last column shows it is very expensive to find.
3. **Equal revenue can hide very different games.** US$9.99 earns the same as US$4.99 (US$249.75 against US$249.50) from half as many buyers. A test cannot tell them apart. Only a decision about who you want paying can. You will return to this below.

Now the sample-size columns. Detecting the conversion drop from US$4.99 to US$6.99 takes about 6,700 new players per arm. Detecting the revenue gain takes about 26,500, roughly four times as many. The revenue metric carries the price's variance on top of the purchase's, and the gain in `RPE` is a small difference of two products. Near the top of the curve it is worse. The US$5.99 comparison needs 53,000 per arm, and US$9.99 against US$4.99 would need hundreds of millions, because their true revenues are nearly equal. A team that powers its price test for conversion, the familiar metric, will stop long before it can say anything about revenue.

This is before whales. A single bundle has one price, so every buyer spends the same. A store where players can buy many things has MMO308 week 6's heavy tail on top, and capping or splitting the metric, as that lecture showed, becomes necessary.

### A visual you can move

Open the interactive. The left view plots conversion against price with the demand line and, through the base price, a dashed **iso-revenue curve** `c = RPE0 / p`. Every point on that curve earns the same as the base price. The test arm is a dot. Drag it along the demand line and watch whether it sits above the curve (earns more) or below it (earns less), while its conversion falls the whole time. The right view plots revenue per 1,000 exposed players against price. The hump is visible at once, and the flat top is where the two sample-size bars under the chart grow tall. Press "run one test" to draw one noisy result at your chosen sample size. At 5,000 players per arm, the conversion result is usually significant and the revenue result usually is not.

### Cross-game recognition

Every one of these is `RPE = p × c(p)`, with its break-even line `c1 / c0 = p0 / p1`.

**World of Warcraft subscription (US$15 a month since 2004).** For a subscription, `c` is the share of players who keep paying, and revenue is price times subscribers. A rise to US$20 breaks even if at least `15 / 20 = 75%` of subscribers stay. Put differently, the game could lose up to a quarter of its subscribers and earn the same. Hight's stated reason for not raising the price is about what the break-even line leaves out. Subscribers who leave also stop grouping, trading and filling raids, and the players who stay feel that loss. MMO305's social capital is not in `RPE`.

**Old School RuneScape membership and bonds (Jagex, 2022 to 2026).** Jagex has raised the price of bonds, its sanctioned token for membership, several times, on 4 May 2022, 25 June 2024 and 10 March 2026, each alongside membership price changes. In September 2026 a bond costs US$9.99 and one month of membership costs US$14.99. Each rise applies to every player at once. In the language of MMO308 that is a whole-game switch with no control group, so its effect can only be read as a before-and-after comparison, and anything else that changed in those months (new content, seasons, a rival's launch) is mixed into it. The formula is the same. The evidence is weaker.

**Steam sales (any Steam game, current Steamworks rules).** A discount is a price test run backwards. At a discount `d`, the break-even line says units must rise by a factor `1 / (1 − d)`. A 50% sale must double units to tie, a 75% sale must quadruple them. Valve's partner rules add a constraint that shapes sequential tests. Raising a price in any currency starts a 30-day cooldown before you may submit a discount. You cannot raise a price on Monday and "discount" it back on Tuesday.

**The SimCity pre-order page (EA/Maxis, 2013).** MA102 week 14 used this case, in which removing a pre-order discount banner raised purchases. It is a reminder that presentation is part of price. The offer changed where the buy button sat, and that mattered more than the money.

One idea underneath all four. A price change trades buyers for revenue per buyer. The break-even line says how many buyers you can afford to lose. Whether you *want* to lose them is a separate decision.

### Eyes-open design judgment

- **Decide the metric before the test, and make it revenue per exposed player over a fixed horizon.** Conversion is a guardrail, not the goal. Write both into the plan from MMO308 week 5.
- **Size the test for revenue, not conversion.** Estimate the revenue variance from last month's data. If the required sample exceeds your traffic, test bigger price gaps or accept that you are choosing on judgment.
- **Stop optimizing at the flat top.** Once two prices are within a few percent of each other in revenue, pick on other grounds. Those grounds include price points players recognize, parity across regions, and how many players you want owning the item.
- **Fewer buyers is a cost you cannot see in RPE.** An item that half as many players own changes the game. A starter bundle that fewer new players buy may mean fewer who reach the social hook of week 2's LTV curve. A cosmetic that fewer players wear is less visible advertising for itself (MMO305 week 7 on conspicuous display). Estimate these effects or at least name them.
- **Test prices on items that are new to everyone when you can.** A player who sees a price change on a familiar item compares it with what they paid. A player who sees a new item has no reference.

## 3. Running a price test in a shared world

MMO308 week 5, section 6 warned that visible differences get noticed and suggested test servers or switchbacks for prices. Here is the full menu, with what each one costs.

| Design | What varies | Strength | Weakness |
|---|---|---|---|
| Player-level split | Each player sees one price | Most statistical power | Players compare prices; fairness complaints; legal disclosure in some places |
| Region or server split | Price differs by market or shard | No player sees two prices on the same server | Few units, so a large design effect (MMO308 week 5); regions differ in more than price |
| Time switchback | Everyone gets price A, then B, then A | Everyone is treated the same at any moment | Weekday and event effects; players delay purchases to wait for the cheaper period |
| Offer test | Same list price, a randomized discount or bundle | List price stays public and identical | Measures response to offers, not to the list price |
| Survey | Stated willingness to pay | No revenue at risk | People say one thing and pay another |

Three notes on the table.

**Offer tests are the workhorse.** Most live teams hold the list price fixed and test what goes around it. That includes bundle sizes, bonus currency, which items share a bundle, and first-purchase offers for new accounts only. These are easier to defend because no player pays more than the posted price. They still carry week 8's warnings. A "limited-time" offer that is always available is a false urgency claim, whatever the test says it earns.

**Surveys still have a use.** The **Van Westendorp price sensitivity meter** asks four questions. At what price would this be so cheap you would doubt its quality? A bargain? Getting expensive? Too expensive to consider? Plotting the answers gives a range of acceptable prices. It is cheap and quick, and it cannot measure the real `c(p)`, because nobody pays. Use it to pick which two or three prices to test, then test them.

**Regional pricing is price discrimination players usually accept.** Steam's pricing tools offer three ways to convert a base price into other currencies. They are exchange rate only, purchasing power only, and a multi-variable conversion that also considers the cost of comparable entertainment. Charging less where incomes are lower increases access and revenue at the same time. Players accept it because the rule is visible and ties price to a market, not to them personally. A price set for one player, from their own data, is a different thing.

### The law and the player

Two rules from the European Union's 2019 "Omnibus" directive, Directive (EU) 2019/2161, apply to price tests aimed at EU consumers. Member states had to apply them from 28 May 2022.

- **Reference prices.** When a trader announces a price reduction, it must show the prior price, defined as the lowest price it applied in a period of at least 30 days before the reduction. A test arm that shows "was US$9.99, now US$6.99" to players who never saw US$9.99 as a price in force is exactly what this rule targets.
- **Personalised prices.** Before a distance contract, the trader must tell the consumer, where applicable, that the price was personalised on the basis of automated decision-making. A price test that assigns prices by hashing account ids is automated. Whether a random split counts as "personalised" is a question for your legal team, not for you. Raise it before launch.

The ethics sit alongside the law. Testing a lower price on some players is rarely a harm. Testing a higher price on players your model marks as big spenders is a different act. It uses what you know about a player's spending, often including compulsive spending, to charge them more. Weeks 8 and 9 of this course cover why the top of the spending curve is where vulnerable players concentrate, and [MMO402 week 12](../../MMO402-emergent-society-governance-and-ethics/lectures/w12-research-ethics-in-online-worlds.md) covers consent in research on players. A defensible rule many studios follow is to randomize prices only across players, never to target price rises by predicted spend, and to refund or honor the lower price for any player who can show they were charged more in a test.

## 4. Beyond one purchase

A single bundle is the clean case. Real stores make three complications you must plan for.

**Cannibalization.** A cheaper bundle may pull buyers away from another item. Measure `RPE` across the whole store for exposed players, not only for the item under test. A 12% gain on the starter bundle that comes entirely out of the next bundle is a zero.

**Horizon.** A higher price may lose a purchase today and gain it next week, or a lower price may pull purchases forward from next month. Measure revenue per exposed player over a fixed window, 14 or 30 days after first exposure, and check whether the gap is still moving at the end (MMO308 week 6's novelty section applies to prices too).

**Subscriptions and LTV.** For a subscription, the right comparison is lifetime value, which week 2 builds. In its simplest form, week 2's retention-times-revenue sum with a constant monthly churn `m` (so monthly retention `1 − m`), a subscriber pays `p` for an average of `1 / m` months, so `LTV = p / m`. A price rise pays only if `p1 / m1 > p0 / m0`. Suppose a game raises its price from US$15 to US$18 and monthly churn rises from 8% to 10%. Then LTV goes from `15 / 0.08 = 187.50` to `18 / 0.10 = 180.00`. The rise loses money per subscriber, even though each month earns 20% more. The break-even churn is `0.08 × 18 / 15 = 9.6%`. A churn change that small, 1.6 points, is hard to measure quickly. Churn also reacts slowly, so a subscription price test needs months, not weeks. That is one more reason Blizzard's choice is harder to second-guess than it looks.

## In-class activity (25 minutes)

In groups of three, you run pricing for a new MMO's first cosmetic mount, currently planned at US$14.99. Your store sees about 40,000 exposed players a week, and last month's mount sold to 3% of exposed players.

1. Pick one design from the table in section 3 and justify it in two sentences, including how players could find out.
2. Choose a second price to test. Using a straight-line demand guess of your own (write it down), compute `RPE` for both prices and the break-even conversion for your test price.
3. Compute the players per arm needed to detect the revenue difference with the script from section 2 (edit `conversion` and the prices). Convert it to weeks of traffic.
4. If the test would take longer than six weeks, redesign it. Options include a bigger price gap, a different metric, or an offer test.
5. Write the one-line EU disclosure question you would send to legal.

Expected output: a design choice, your demand guess, two `RPE` values, a break-even conversion, a test length in weeks, and your redesign if needed.

## Common misconceptions

- **"Conversion went down, so the price rise failed."** Conversion always falls when price rises. Check revenue per exposed player against the break-even line `c1 = c0 × p0 / p1`.
- **"If the test isn't significant, the prices earn the same."** Near the best price the revenue difference is small and the test needs enormous samples. "Not significant" there means the test could not tell, as MA102 week 14 warned.
- **"The revenue-maximizing price is the right price."** It is the price that maximizes one number. At the flat top, a lower price with more owners may cost almost nothing and be better for the game.
- **"A price test is just another A/B test."** It needs a revenue metric with larger variance, a fixed horizon, a store-wide view, and attention to fairness and consumer law that a button-color test does not.

## Check yourself

1. A bundle at US$9.99 converts 2.0% of exposed players. A test at US$7.99 converts 2.4%. Compute `RPE` for both, the break-even conversion for US$7.99, and the arc elasticity. Did the cut pay?
2. A Steam game at US$20 runs a 40% discount. By what factor must unit sales rise to earn the same revenue? What if the discount is 60%?
3. A subscription costs US$12 with 6% monthly churn. Management proposes US$15. What is the highest churn at which the new price still has the higher `p / m`?
4. With the section 2 script, why does comparing US$9.99 with US$4.99 need hundreds of millions of players per arm? What would you do instead if you really wanted to choose between them?

<details>
<summary>Answers</summary>

1. `RPE` at US$9.99 is `9.99 × 0.020 = 0.1998`. At US$7.99 it is `7.99 × 0.024 = 0.1918`. Break-even for US$7.99 is `0.02 × 9.99 / 7.99 = 2.50%`. Observed 2.4% is below it, so the cut lost about 4% of revenue. Arc elasticity: `(0.004 / 0.022) / (−2 / 8.99) = 0.182 / −0.222 = −0.82`. The size is below 1, so demand is inelastic here, which is why the cut did not pay.
2. `1 / (1 − 0.4) = 1.67`, so units must rise 67%. At 60% off, `1 / 0.4 = 2.5`, so units must rise 150%.
3. Solve `15 / m1 = 12 / 0.06 = 200`, so `m1 = 0.075`. Churn can rise to 7.5% a month and the new price still ties. Above that, it loses.
4. Their true revenues per exposed player are almost identical (US$249.75 against US$249.50), so the difference to detect is tiny and the required sample is huge. Revenue cannot choose between them. Choose on the other difference, that US$4.99 has twice as many buyers, and decide which you want for the game.

</details>

## Lab / assignment hook

[Lab 10, reading a three-arm price test](../labs/lab10.md). You get player-level results of a three-price test for a bundle. You compute conversion, `RPE`, break-even lines, elasticities and confidence intervals, find out why the conversion readout and the revenue readout disagree, and write a one-page recommendation. It counts toward the models component (40%).

## Sources

- Warcraft Wiki, "Game time" (accessed September 2026). One-month price US$15 unchanged since launch in 2004; 3-month, 6-month and 12-month plans; cites Colp, T., "Against all odds, World of Warcraft's subscription price hasn't changed in 20 years", PC Gamer, 22 March 2024, reporting John Hight's remarks in an interview at GDC 2024; the article was read directly (published 22 March 2024). Paraphrased here.
- US Bureau of Labor Statistics, CPI-U, US city average, all items, series CUUR0000SA0, annual averages 188.9 (2004) and 321.943 (2025), retrieved from the BLS public API, September 2026.
- Old School RuneScape Wiki, "Old school bond" (accessed September 2026). Bond prices by currency (US$9.99 for one bond), 14 days of membership per bond, and the change history listing bond price increases on 4 May 2022, 25 June 2024 and 10 March 2026. "Membership" (accessed September 2026). One-month membership US$14.99.
- Valve, Steamworks Documentation, "Pricing" (accessed September 2026). Three currency conversion methods for recommended regional prices, and the rule that raising a price starts a 30-day cooldown on submitting discounts.
- Directive (EU) 2019/2161 of the European Parliament and of the Council of 27 November 2019 (the "Omnibus" directive), as adopted. Article 2 inserts Article 6a into Directive 98/6/EC (prior price is the lowest in at least 30 days); Article 4 inserts point (ea) into Article 6(1) of Directive 2011/83/EU (disclosure of prices personalised by automated decision-making); Article 7 sets transposition by 28 November 2021 and application from 28 May 2022. Read from the legislation.gov.uk copy of the adopted text.
- Optimizely, SimCity pre-order case study (2013), as used in MA102 week 14.
- Van Westendorp, P. (1976). "NSS Price Sensitivity Meter: A new approach to study consumer perception of prices." Proceedings of the ESOMAR Congress, Venice.
- Fields, T. & Cotton, B. (2011). *Social Game Design: Monetization Methods and Mechanics*. Morgan Kaufmann.
- Kohavi, R., Tang, D. & Xu, Y. (2020). *Trustworthy Online Controlled Experiments*. Cambridge University Press.

## Interactive spec: examples/w10-price-test.html

**The one insight:** when a price rises, conversion always falls, but revenue per exposed player rises and then falls. A result is a win only if it lies above the iso-revenue curve through the old price. Near the top of the revenue curve, the revenue difference is so small that the test needs enormous samples, while the conversion difference stays easy to detect.

**Layout.** Two linked charts side by side on desktop, stacked on mobile (conversion chart first). A readout table and two sample-size bars below.

**Left chart: conversion against price.** x-axis price from US$0.99 to US$14.99. y-axis conversion 0% to 10%. Draw the demand line `c(p) = c0 − β × (p − p0)`, clipped at 0. Draw the iso-revenue curve `c = p0 × c0 / p` as a dashed line, labelled "earns the same as the base price". Shade the region above the dashed curve lightly and label it "earns more". Base point at `(p0, c0)`, fixed. Test point at `(p1, c(p1))`, draggable along the demand line and set by a slider.

**Right chart: revenue per 1,000 exposed against price.** Same x-axis. y = `1000 × p × c(p)`. Mark the base and test points, and the peak at `p* = (c0 + β p0) / (2β)` with a vertical dotted line and label "best price".

**Controls.**
- Base price `p0`: US$0.99 to US$19.99, step 1.00, default 4.99.
- Base conversion `c0`: 0.5% to 10%, step 0.1%, default 5.0%.
- Slope `β`: 0.1 to 2.0 percentage points per dollar, step 0.1, default 0.5.
- Test price `p1`: US$0.99 to US$19.99, step 0.50 (also by dragging), default 6.99.
- Players per arm `n`: 1,000 to 200,000, log slider, default 5,000.
- Button "run one test": draws `k0 ~ Binomial(n, c0)` and `k1 ~ Binomial(n, c(p1))` (normal approximation is fine for `n × c ≥ 10`, otherwise exact with a seeded generator), and shows observed conversions, observed `RPE`, and the z statistic for conversion and for `RPE`. Each gets a verdict "significant" or "not significant" at 1.96.

**Readout table** (copyable). `p`, `c`, `RPE`, revenue per 1,000 for both arms. Change in conversion (%). Change in `RPE` (%). Break-even conversion `c0 p0 / p1`. Arc elasticity. Players per arm for conversion, `n_c = 7.849 × (c0(1−c0) + c1(1−c1)) / (c1 − c0)²`. Players per arm for revenue, `n_r = 7.849 × (p0² c0(1−c0) + p1² c1(1−c1)) / (p1 c1 − p0 c0)²`, where `7.849 = (1.96 + 0.8416)²`. Show "more than 10 million" when `n_r` exceeds 10 million.

**Sample-size bars.** Two horizontal bars on a log scale for `n_c` and `n_r`, with a marker at the current `n`. Each bar is labelled with its number.

**Test values (defaults except `p1`).**
- `p1 = 6.99`: `c1 = 4.00%`, `RPE` 0.2495 against 0.2796 (+12.1%), conversion −20.0%, break-even 3.57%, arc elasticity −0.67, `n_c ≈ 6,742`, `n_r ≈ 26,501`.
- `p1 = 7.99`: `c1 = 3.50%`, revenue per 1,000 US$279.65, `n_c ≈ 2,835`, `n_r ≈ 28,830`.
- `p1 = 9.99`: `c1 = 2.50%`, revenue per 1,000 US$249.75, `n_r` shown as "more than 10 million".
- `p1 = 3.99`: `c1 = 5.50%`, revenue per 1,000 US$219.45, `n_r ≈ 17,473`.
- Peak at defaults: `p* = 7.495`, revenue per 1,000 about US$280.88.

**Accessibility.** All controls keyboard-operable with visible focus; the draggable point also moves with arrow keys. The shaded "earns more" region has a text label, not only color. Demand and iso-revenue lines are distinguished by dash pattern. No animation under `prefers-reduced-motion`. Uses the shared palette tokens.

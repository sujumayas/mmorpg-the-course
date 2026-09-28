# MMO401 · Week 01 — The in-house economist role

**Why this matters:** Every live MMO eventually hits a meeting where someone says "prices are up, players are angry, what do we change?" The person who can turn that complaint into a measured number, a cause and a costed option is the in-house economist. This course trains you to be that person.

**You will be able to:**
- Describe the four jobs of an in-house economist (measure, diagnose, advise, publish) and name the deliverable each one produces.
- Compute Laspeyres, Paasche and Fisher price indices from a small basket and explain why they disagree.
- Read a published game economic report and separate stocks (money supply) from flows (faucets and sinks).
- Critique a single-number "inflation" claim by naming the basket behind it.

**Before class:** Read CCP's EVE Online Monthly Economic Report for October 2024 (eveonline.com, news section) and look at every chart once. Skim the course text, Lehdonvirta & Castronova, *Virtual Economies* (2014), the first of the assigned chapters 9-12. Read the US Bureau of Labor Statistics page "Chained CPI questions and answers" (about 10 minutes).

**Prerequisites from earlier courses:** [MMO304 week 3, faucets, sinks and transformations](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md). [MMO304 week 4, money supply per capita and inflation](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w04-money-supply-per-capita-and-inflation.md). [MMO304 week 12, economic telemetry and dashboards](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w12-economic-telemetry-and-dashboards.md). [MA102 week 12, descriptive statistics for playtests](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md) (means, medians and why one summary number hides the shape).

**Interactive:** [Price index basket](../examples/w01-price-index-basket.html). Keep it open during section 2.

---

## 1. A job that did not exist before 2007

In 2007 CCP Games, the studio behind EVE Online, hired an academic economist to look after the game's economy. Eyjólfur Guðmundsson had been dean of business and science at the University of Akureyri in Iceland. Wikipedia's history of EVE describes CCP as the first game developer to make that kind of hire. He stayed until 2014, when he went back to Akureyri as the university's rector. In June 2012 Valve hired the economist Yanis Varoufakis to study the economies of its games and the Steam platform. By 2024, CCP's economic reports carried the byline "EVE Online Economic Council," a team rather than one person.

Why would a game studio pay for an economist? Three reasons, all of which you met in MMO304.

- **Players treat currency as real.** In 2001, Edward Castronova estimated the output of EverQuest's world, Norrath, from auction-site prices. His working paper put its GNP per capita between Russia's and Bulgaria's. Once players can swap game currency for money, legally (a subscription token) or not (gold selling), every design change moves somebody's savings.
- **The designers are the central bank.** Every faucet (a source of new currency, like a quest reward) and every sink (something that destroys currency, like a repair bill) is a number in a design file. MMO304 week 3 taught you to draw that map. Someone has to watch what happens when those numbers meet millions of player decisions.
- **Economies fail slowly and then all at once.** Inflation from an unbalanced faucet takes months to show up in prices. By the time the forum notices, fixing it hurts players who did nothing wrong.

### The four jobs

An in-house economist does four things. Each has a concrete output you can put on a desk.

| Job | Question it answers | Deliverable |
|---|---|---|
| Measure | What is happening? | Indicators computed the same way every month: money supply, faucet and sink totals, price indices |
| Diagnose | Why is it happening? | A causal story tested against the data, often with a model (weeks 2-3) |
| Advise | What should we change? | A policy memo with options, predicted effects and a recommendation (weeks 4, 7, 14) |
| Publish | What do we tell players? | A public report, or a decision not to publish, with the reasons written down |

Most of this course is about the middle two jobs. This week is about the first one, because every later argument stands on a number someone chose how to compute. If you choose badly, your diagnosis and your advice inherit the error.

### What the economist has that a real one does not

A national statistics office samples prices from shops and guesses at the money supply from bank reports. You have the full ledger. Every coin a quest paid out and every coin a repair bill destroyed sits in a log table. You can compute the exact money supply for any second of the game's life.

You also have three problems a national economist rarely has:

1. **Your goal is not welfare.** A real economy exists so people can live well. A game economy exists so the game is fun and the studio stays open. Sometimes scarcity, loss and grind are the point.
2. **Your players read your reports and act on them fast.** Announce a sink change on Tuesday and the affected item's price moves on Tuesday, weeks before the patch ships.
3. **You work for the company that sells the currency.** If the studio sells a premium currency or token (week 11), your advice about exchange rates is also advice about revenue. Name that conflict out loud.

## 2. Worked example: which inflation? Building a price index

### The hook

CCP's Monthly Economic Report for October 2024 said two things in the same breath. The Mineral Price Index, which tracks the raw materials ships are built from, had reached a record 287. The Ship Index had fallen about 4.5% over the previous twelve months. The raw data CCP released with that report shows the total ISK (EVE's currency) held by players rose from about 1.89 quadrillion on 1 October 2023 to about 2.21 quadrillion on 1 October 2024. That is 16.8% more money in a year.

So, was EVE in inflation or not? A miner would say yes, loudly. A pilot shopping for a new hull would say prices were falling. Both are right. The answer depends on whose shopping list you price. That shopping list is called a **basket**, and choosing it is the first real decision of an economist's job.

### The model

A **price index** compares what a fixed set of goods costs now with what it cost in a base period, scaled so the base period equals 100. There are three standard ways to do it. Every symbol below is per good `i`.

```
p0_i, p1_i   price of good i in the base period (0) and the current period (1)
q0_i, q1_i   quantity of good i traded in period 0 and period 1

Laspeyres  L = 100 × Σ p1_i × q0_i  /  Σ p0_i × q0_i
Paasche    P = 100 × Σ p1_i × q1_i  /  Σ p0_i × q1_i
Fisher     F = sqrt(L × P)
```

- **Laspeyres** asks "what would last month's shopping cost at today's prices?" It holds quantities at the base period.
- **Paasche** asks "what would today's shopping have cost at last month's prices?" It uses current quantities.
- **Fisher** is the geometric mean of the two. It sits between them. Statisticians call it a *superlative* index because it handles substitution well.

The gap between Laspeyres and Paasche has a name, **substitution bias**. When a good gets expensive, players buy less of it. Laspeyres ignores that and overstates the price rise. Paasche uses the new, smaller quantities and tends to understate it.

### Numbers you can check

Take an invented fantasy MMO with four traded goods. The auction house logs give these monthly prices and volumes.

| Good | Price month 0 | Price month 1 | Change | Units sold month 0 | Units sold month 1 |
|---|---|---|---|---|---|
| Ore (per unit) | 10 | 15 | +50% | 1,000 | 700 |
| Health potion | 20 | 22 | +10% | 300 | 320 |
| Mid-tier sword | 500 | 400 | −20% | 20 | 30 |
| Mount | 5,000 | 4,000 | −20% | 2 | 3 |

Now the four sums. Each is a price column times a quantity column, added over goods.

| Sum | Ore | Potion | Sword | Mount | Total |
|---|---|---|---|---|---|
| `p0 × q0` | 10,000 | 6,000 | 10,000 | 10,000 | 36,000 |
| `p1 × q0` | 15,000 | 6,600 | 8,000 | 8,000 | 37,600 |
| `p0 × q1` | 7,000 | 6,400 | 15,000 | 15,000 | 43,400 |
| `p1 × q1` | 10,500 | 7,040 | 12,000 | 12,000 | 41,540 |

So:

```
L = 100 × 37,600 / 36,000 = 104.4     (prices up 4.4%)
P = 100 × 41,540 / 43,400 =  95.7     (prices down 4.3%)
F = sqrt(104.4 × 95.7)    = 100.0     (flat)
```

Same prices, same month. One standard formula reports 4.4% inflation, another reports 4.3% deflation, and the compromise says nothing happened. The formulas disagree this much because players moved sharply. They bought 30% less of the good that rose 50%, and 50% more of the goods that fell.

Now change the basket instead of the formula. Price only what a new player buys (ore and potions) or only what a veteran buys (swords and mounts), with Laspeyres weights:

| Basket | Base cost | Cost at month-1 prices | Index |
|---|---|---|---|
| New player (ore, potions) | 16,000 | 21,600 | 135.0 |
| Veteran (swords, mounts) | 20,000 | 16,000 | 80.0 |
| Everything | 36,000 | 37,600 | 104.4 |

The new player's cost of living rose 35%. The veteran's fell 20%. The "whole economy" number of +4.4% describes nobody. This is the most common way a single inflation figure misleads a design team.

### Move it yourself

Open the interactive. The left view shows each good's price change as a bar, from −50% to +100%. The right view shows the index under the basket you pick, with a line at 100. Drag the quantity sliders for month 1 and watch Laspeyres stay put while Paasche moves. Then switch the basket preset between "new player," "veteran" and "all." The price bars on the left never change. The verdict on the right flips from inflation to deflation. Same data, two views, opposite headlines.

### Cross-game recognition

**EVE Online (monthly reports, 2024).** CCP does not publish one inflation number. The October 2024 report splits prices into a Consumer Price Index, a Mineral Price Index, a primary and a secondary Producer Price Index, and a ship-and-module index. Each is a different basket. The raw data file lists every item's index and sub-index (skill injectors sit in the consumer index under "Accessories," for example) and gives each sub-index a monthly price change and a traded value. That is exactly our model with value weights. The report itself does not document how the headline index values are chained together. Treat that as a lesson in what to publish, not only what to compute.

**World of Warcraft (WoW Token, patch 6.1.2, 2015).** The WoW Token is a single good with a fixed real-money value. It redeems for 30 days of game time, and Blizzard sets its gold price by supply and demand. At launch in the Americas region it cost 30,000 gold. Its gold price is a price index with a one-item basket. Because the token's value in dollars is fixed, its gold price is also an exchange rate between gold and money. If the token costs more gold each month, gold is losing value against real money. Week 11 returns to this.

**Real-world statistics (United States).** The Bureau of Labor Statistics publishes the CPI-U, a fixed-basket index whose weights update once a year. Since the July 2002 data it has also published the Chained CPI (C-CPI-U), which uses a superlative formula to capture consumers switching between item categories. The BLS explains the difference with meat. If pork gets dearer and beef does not, shoppers move to beef, and the chained index rises less. That is our ore-and-sword table with groceries.

Three settings, one idea. A price index is a basket plus a weighting rule. When someone quotes you a number, your first move is to ask *whose basket, and whose quantities?*

### Eyes-open design judgment

- **Pick the basket from the question.** "Can new players afford to start?" needs a starter basket. "Is money losing value?" needs broad coverage or a fixed-value anchor like a token. "Are raw materials scarce?" needs a materials basket. EVE's split into five indices is the right instinct.
- **Report more than one formula when players are moving.** If Laspeyres and Paasche differ by more than a point or two, say so. The size of the gap is itself a finding: it tells you how hard players are substituting.
- **Watch for quality change.** When a new tier of swords ships, a "mid-tier sword" in month 12 is not the same item as in month 0. If you keep pricing the old item, your index reports deflation that is really obsolescence. Either drop superseded items or link the new tier in at an overlapping month.
- **Publish your method.** An index nobody can reproduce invites conspiracy theories. The cost of writing down the method is one page.
- **Do not let the index become the goal.** A team told to "keep the CPI flat" will find a way to do it (subsidize the basket items) that leaves the economy worse. The index is a thermometer, not the patient.

## 3. The ledger: stocks and flows you can read exactly

MMO304 week 3 separated **stocks** (quantities at a moment, like money held) from **flows** (quantities per unit of time, like gold paid out per day by quests). The one identity that holds in every closed economy is:

```
change in money supply over a period = faucets − sinks   (over that period)
```

A real central bank can only estimate both sides. You can read both from logs. EVE's October 2024 raw data gives a sense of scale.

| Quantity (EVE, October 2024) | Value | Share |
|---|---|---|
| Total ISK held, 1 Oct 2024 | about 2,206 trillion | — |
| All faucets, October | about 170.8 trillion | 7.7% of the stock |
| All sinks, October | about 95.9 trillion | 4.3% of the stock |
| Largest faucets | commodity sales to the NPC market (27.8%), NPC bounty prizes (26.8%), ESS main-bank payouts (13.3%) | of faucets |
| Largest sinks | transaction tax (21.3%), LP store purchases (16.3%), broker fees (11.3%), skill purchases (10.6%) | of sinks |

The net flow is about +74.9 trillion for the month. But the money-supply series in the same download grew by about 129.9 trillion between 1 October and 31 October. The two do not match. Maybe some flows are not in the faucet and sink table, maybe the stock and flow series are sampled at different times of day, maybe the categories are defined differently. Lab 01 asks you to investigate this gap. It is the most realistic thing in the lab. Most of an in-house economist's week is spent reconciling two numbers that should agree and do not.

Two habits from this table carry through the course.

- **Express flows as a share of the stock.** "170.8 trillion" means nothing to a designer. "Faucets add 7.7% of the money supply every month, sinks remove 4.3%" is a sentence anyone can reason with. It also tells you that, with no change, the money supply grows about 3.4% a month.
- **Group flows by their shape, not their name.** A bounty pays in proportion to how fast you kill. A transaction tax takes a share of what you trade. A skill book costs the same for everyone. Week 3 shows that faucets and sinks with the same total but different shapes produce very different worlds.

## 4. Advising: from a number to a decision

Measurement only matters if it changes a decision. The standard output of the advise job is a one-page **policy memo**. Every memo in this course uses the same five parts.

1. **Observation.** One number, with its basket, period and source. "The new-player basket rose 35% month on month (Laspeyres, auction-house data, month 0 to 1)."
2. **Diagnosis.** The mechanism you believe causes it and the evidence. "Ore volume fell 30% after the gathering nerf in patch X. Ore is 62.5% of the new-player basket by value."
3. **Options.** Two to four interventions with predicted effects on the observed number and on at least one other number you care about. Each option names its cost.
4. **Recommendation.** One option, and why.
5. **What we will measure.** The indicator, the threshold that would make you reverse course, and when you will look.

The fifth part is the one most memos leave out, and the one that makes the memo honest. If you cannot say what result would prove you wrong, you are guessing. Weeks 4 (monetary tools), 7 (taxes) and 14 (intervention design) each end with a memo in this format.

Notice what the index example did to the memo. "Inflation is 4.4%" would have led the team to add a general sink. "The new-player basket is up 35% and the veteran basket is down 20%" points at ore supply, a completely different fix. The measurement chose the policy.

## 5. Ethics: the economist knows too much

The economist sees data that players would pay for. Upcoming patch notes, drop-rate changes and the exact size of every faucet are all market-moving information.

EVE learned this early. In 2007 a CCP developer, known by the name t20, was found to have given six valuable blueprints to the player corporation he belonged to. CCP responded by setting up an internal affairs team to watch staff and privileged accounts in the game. The controversy is one of the reasons CCP invited players to elect the first Council of Stellar Management in 2008, a player body that advises the studio. MMO402 week 3 studies that council.

Three working rules follow for the economist.

- **Staff do not trade on unreleased changes.** Write it into the team's rules, and audit it.
- **Publish data after the fact, on a fixed schedule.** A monthly report with a fixed release date gives every player the same information at the same time.
- **Announce changes with enough notice that the price move happens before the patch, in the open.** Players who read patch notes get an edge, but it is an edge anyone can have.

## In-class activity (25 minutes)

Work in groups of three. Each group gets the invented four-good table from section 2 plus a fifth good that your instructor assigns (for example, "dungeon key, price 50 then 80, volume 100 then 60").

1. Recompute L, P and F with five goods. (8 min)
2. Define one basket for a player type your group chooses (crafter, raider, new player, gold farmer). Justify each item in one line. Compute its Laspeyres index. (8 min)
3. Write the *observation* and *options* parts of a policy memo, at most 120 words, for the player type you chose. (9 min)

Expected output: three index values, one custom basket with its index, and the memo draft. Two groups read their observations aloud. The class decides whether the two memos could both be true.

## Common misconceptions

- **"There is one true inflation rate."** There are as many rates as there are baskets. The honest report names the basket and gives more than one.
- **"More money in the economy means prices rise."** Only if the money chases the same goods at the same speed. EVE's ISK supply rose 16.8% in a year while its Ship Index fell. Production, substitution and where the new money sits all matter. MMO304 week 4 gives the quantity-equation view, and week 4 of this course adds the policy tools.
- **"Laspeyres is wrong and Paasche is right."** Each answers a different question. Laspeyres prices last month's life, Paasche prices this month's. Their gap measures substitution, which is information.
- **"The in-house economist sets the drop rates."** Designers own the content. The economist measures, models and advises, and a good one makes it easy for designers to say no with reasons.

## Check yourself

1. In the section 2 table, the mount's month-1 price rises back to 5,000 and everything else stays the same. Recompute the Laspeyres index.
2. An economy has two goods. Bread goes from 10 to 12 and sales fall from 100 to 80. Cloth stays at 50 with sales of 20 in both months. Compute L and P. Why are they this close to each other?
3. EVE's October 2024 faucets were about 7.7% of the money supply and sinks about 4.3%. If those rates held for a year and nothing else changed, roughly how much larger would the money supply be after 12 months? (Assume the rates apply to the current stock each month.)
4. A designer proposes to cut the "inflation" by adding a 10% auction-house fee on all goods. Using the new-player and veteran baskets from section 2, argue whether that fixes the problem the numbers show.

<details>
<summary>Answers</summary>

1. `p1 × q0` becomes 15,000 + 6,600 + 8,000 + 10,000 = 39,600, so `L = 100 × 39,600 / 36,000 = 110.0`.
2. Base `p0 q0 = 1,000 + 1,000 = 2,000`. `p1 q0 = 1,200 + 1,000 = 2,200`, so `L = 110.0`. `p0 q1 = 800 + 1,000 = 1,800`, `p1 q1 = 960 + 1,000 = 1,960`, so `P = 108.9`. They are close because only one good changed and its quantity moved only 20%. Little substitution, little gap.
3. Net growth is about 3.4% a month. `1.034^12 ≈ 1.49`, so about 49% larger. (Real growth over October 2023 to October 2024 was 16.8%, which tells you the October 2024 rates were not typical of the whole year.)
4. The numbers say ore is scarce (+50%) while finished goods are cheap. A flat fee raises everyone's costs, hits the new-player basket (which is already up 35%) and does nothing about ore supply. A better first option targets ore supply, for example reverting part of a gathering nerf, and measures the new-player basket afterwards.

</details>

## Lab / assignment hook

[Lab 01, reading a real economic report](../labs/lab01.md). You download the raw data behind CCP's October 2024 report, rebuild the money-supply and faucet-sink numbers from section 3, investigate the gap between the flows and the stock, and compute three indices on a provided basket. Deliverable: a notebook or spreadsheet and a one-page memo in the section 4 format.

## Sources

- Wikipedia, "Eve Online" (accessed 2026). CCP hired Eyjólfur Guðmundsson in 2007 as the first economist employed by a game developer; he left in 2014 to become rector of the University of Akureyri. The 2007 t20 blueprint incident, CCP's internal affairs response, and the first Council of Stellar Management election in 2008.
- Wikipedia, "Yanis Varoufakis" and "Valve Corporation" (accessed 2026). Varoufakis joined Valve in June 2012 to study the economies of its games and Steam.
- Castronova, E. (2001). "Virtual Worlds: A First-Hand Account of Market and Society on the Cyberian Frontier." CESifo Working Paper No. 618. Norrath GNP per capita between Russia and Bulgaria (as summarized on Wikipedia, "Edward Castronova").
- CCP Games, "Monthly Economic Report, October 2024," EVE Online Economic Council, eveonline.com, published 8 November 2024. Mineral Price Index record of 287, Ship Index down about 4.5% over 12 months, the five indices, and the faucet and sink charts.
- CCP Games, raw data for the October 2024 report (`EVEOnline_MER_Oct2024.zip`, files `money_supply.csv`, `sinks_and_faucets_history.csv`, `index_baskets.csv`, `economy_indices_details.csv`). Money supply values, October 2024 faucet and sink totals and shares, and the index basket structure were computed by the author from these files.
- Warcraft Wiki, "WoW Token." Introduced with patch 6.1.2 (2015), redeems for 30 days of game time, price set by supply and demand, 30,000 gold at launch in the Americas.
- US Bureau of Labor Statistics, "Chained CPI questions and answers." CPI-U fixed-weight formula with annual weight updates; C-CPI-U from July 2002 data using a superlative formula; the pork and beef substitution example.
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press.

## Interactive spec: examples/w01-price-index-basket.html

**Insight the visual must make obvious:** the same price changes produce opposite inflation verdicts depending on the basket and on which period's quantities you use.

**Layout.** Two linked panels, side by side at 1280px and stacked at 390px.

1. **Left panel, "What prices did."** Horizontal bar chart, one bar per good (Ore, Health potion, Mid-tier sword, Mount). Bar length is the price change `p1/p0 − 1` on an axis from −50% to +100%, zero line marked. Positive bars in the "warm" token colour, negative in the "cool" token colour. Each bar shows its exact percentage.
2. **Right panel, "What the index says."** Three vertical bars for Laspeyres, Paasche and Fisher, on an axis from 60 to 150, with a dashed reference line at 100 labelled "no change." Each bar prints its value to one decimal. Above the bars, a one-line verdict computed from the selected formula: "Inflation +4.4%" or "Deflation −4.3%" or "Flat" when within ±0.5.

**Controls (all keyboard accessible, labelled).**
- Basket preset (segmented control): "All goods" (default), "New player" (ore, potion), "Veteran" (sword, mount), "Custom." Custom shows four checkboxes, one per good.
- Four sliders for month-1 prices (ore 5-30, potion 10-40, sword 200-800, mount 2,000-8,000) and four sliders for month-1 quantities (ore 200-1,500, potion 100-500, sword 5-60, mount 0-8). Month-0 values are fixed and shown as tick marks on each slider.
- "Highlighted formula" radio (Laspeyres / Paasche / Fisher) that drives the verdict line.
- Reset button restoring the defaults.

**Data table** under the panels with the four sums `Σp0q0`, `Σp1q0`, `Σp0q1`, `Σp1q1` for the selected basket and the three index values, formatted exactly as in the lecture so students can copy them.

**Formulas.** For the selected set of goods S: `L = 100 × Σ_S p1 q0 / Σ_S p0 q0`, `P = 100 × Σ_S p1 q1 / Σ_S p0 q1`, `F = sqrt(L × P)`. If a denominator is zero (for example mount quantity 0 in a mount-only basket), show "n/a" and the message "No trades in this basket in that period."

**Defaults.** p0 = (10, 20, 500, 5,000), p1 = (15, 22, 400, 4,000), q0 = (1,000, 300, 20, 2), q1 = (700, 320, 30, 3).

**Test values.**
- Defaults, all goods: sums 36,000 / 37,600 / 43,400 / 41,540; L = 104.4, P = 95.7, F = 100.0.
- New player preset: L = 135.0, P = 130.9.
- Veteran preset: L = 80.0, P = 80.0.
- Mount p1 set to 5,000, everything else default, all goods: L = 110.0.
- Set q1 equal to q0 for every good: L and P must be identical (104.4).

**Accessibility and style.** Uses `templates/interactive-tokens.css` inline, respects `prefers-color-scheme` and `prefers-reduced-motion` (bars update without animation when reduced motion is set). All goods drawn as generic labelled bars; no game art.

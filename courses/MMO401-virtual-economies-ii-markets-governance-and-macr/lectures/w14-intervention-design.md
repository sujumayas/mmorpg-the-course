# MMO401 · Week 14 — Intervention Design

**Why this matters:** Every lever in a live economy moves more than one thing. Raise a tax and you drain money, but you may also kill the trading that the tax was collecting from. This week you learn to predict where an intervention settles, how long it takes, and who pays for it, before you ship it.

**You will be able to:**
- Compute the equilibrium money stock and the half-life of adjustment after a change to a proportional sink.
- Predict how a behavioural response (the elasticity of trade to the tax) splits an intervention's effect between lower prices and lower trade volume.
- Compare interventions (faucet cuts, sink raises, item sinks, market rules) by incidence, speed and reversibility.
- Write an intervention spec with a diagnosis, a sized lever, a pre-registered prediction and kill criteria.

**Before class:** Lehdonvirta & Castronova, *Virtual Economies: Design and Analysis* (MIT Press, 2014), from the course reading list ch. 9-12, reread the material on economic policy and managing a virtual economy. EVE University Wiki, "Sales tax" (the change history). Old School RuneScape Wiki, "Grand Exchange tax". Your Lab 13 results.

**Prerequisites from earlier courses:** [GD102 week 4, negative feedback loops](../../GD102-systems-design-and-game-mechanics/lectures/w04-negative-feedback-loops-rubber-banding.md) (a loop that pulls a stock toward a target). [MA101 week 4, exponentials](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md) and [MA101 week 5, logarithms](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md) (repeated multiplication and solving for the number of steps). [MA102 week 14, hypothesis testing and A/B tests](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w14-intro-to-hypothesis-testing-ab.md). [MMO304 week 10, market design](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w10-market-design-auction-houses-vendors-barter.md) (fees as a band around the price). From this course, [week 13, reading an economic report](w13-reading-an-economic-report.md), [week 4, monetary policy tools](w04-monetary-policy-tools-in-games.md), [week 7, taxes and fees as policy](w07-taxes-and-fees-as-policy.md), and week 12 on exploits and rollbacks (see the [MMO401 syllabus](../syllabus.md)).

**Interactive:** [Tax change simulator](../examples/w14-tax-change-simulator.html) (spec at the end of this lecture). Keep it open during section 2.

---

## 1. What counts as an intervention

An intervention is any change the developer makes to shift the economy's state on purpose. Last week you learned to read the state. This week you learn to change it without surprising yourself.

Most interventions pull one of a few levers:

| Lever | Example | Acts on |
|---|---|---|
| Cut a faucet | Lower NPC bounties or quest gold | Money inflow `F` |
| Raise a proportional sink | Higher sales tax or broker fee | Money outflow, scaled by trade |
| Add a flat sink | A new repair cost, a cosmetic sold by an NPC | Money outflow, per player |
| Item sink | Buy items from players and delete them | Item supply, the `Q` side |
| Market rule | Price bands, binding, closing a market | Who can trade what |
| One-off correction | A rollback or a targeted deletion after an exploit | The stock directly |

Week 4 introduced these as tools. Week 7 looked at taxes in the order book. This week's question is different. Given a diagnosis, how do you choose one lever, size it, and know in advance what "working" will look like?

Every intervention spec answers five questions:

1. **Diagnosis.** What is wrong, in numbers, from the identities of week 13? "Money per active player is rising 3% a month with flat velocity and volume, so prices are rising about 3% a month."
2. **Target.** What number should change, to what value, by when?
3. **Lever and size.** Which lever, and how far do you pull it?
4. **Prediction.** Where does the economy settle, how fast, and what else moves? Who pays?
5. **Measurement and reversal.** Which metric tells you it is working, what result would make you roll it back, and can you roll it back?

Question 4 is where most interventions fail. Designers pull a lever, see the first week's numbers, and declare victory or panic. The first week tells you very little. The worked example shows why.

## 2. Worked example: doubling the sales tax

### The hook

In 2025 two of the largest player markets nearly doubled their main transaction tax within three months of each other. EVE Online raised its base sales tax from 4% to 7.5% in release 22.02 on March 12, 2025, a factor of 1.875. Old School RuneScape raised its Grand Exchange tax from 1% to 2% on May 29, 2025, a factor of 2.

A natural reading of either change is that the sink now removes twice the money, so the money supply will shrink twice as fast, forever. That reading is wrong in two separate ways. A proportional sink does not drain money forever. It moves the money stock to a new resting level. And how far the stock moves depends on something neither patch note can tell you, which is how much players cut back their trading because of the tax.

We will not claim what happened to EVE's or RuneScape's money supply after their changes. We will build the model you would use to predict it, run it on an invented economy with EVE-like rates, and see what the prediction depends on.

### The model

Use a daily time step. Let

- `M_t` be the money stock on day `t`.
- `F` be the net daily faucet: all money created minus all sinks other than the tax. Treat it as constant.
- `v` be the daily velocity, the fraction of the money stock that changes hands on the market each day. Trade value per day is `v × M_t`.
- `τ` (tau) be the tax rate on trade value.

Then

```
M_{t+1} = M_t + F − τ × v × M_t
```

The sink is a rate times a base, and the base is proportional to the stock. That makes this a negative feedback loop (GD102 week 4). When the stock is high, the sink is big and pulls it down. When the stock is low, the sink is small and faucets push it up.

**Equilibrium.** Set `M_{t+1} = M_t`:

```
M* = F / (τ × v)
```

**Speed.** Write `r = τ × v`. The gap to equilibrium shrinks by the factor `(1 − r)` each day, so after `t` days it is `(M_0 − M*)(1 − r)^t` (MA101 week 4). The half-life, the time to close half the gap, is about

```
half-life ≈ ln 2 / r   days
```

**The behavioural response.** Players who pay more tax per trade trade less. Model that with an elasticity `ε` (epsilon):

```
v = v_0 × (τ / τ_0)^(−ε)
```

With `ε = 0`, players ignore the tax. With `ε = 1`, trade value falls in exact proportion to the tax rise, so the tax collects the same revenue from less trade. Real values are unknown until you measure them, which is the point of the whole example.

**Where the effect lands.** Assume the money-stock change shows up as prices (fewer crowns chasing the same goods) and the velocity change shows up as fewer trades at unchanged prices. Using `P × Q = M × v` from week 13, the new equilibrium has

```
price level factor  = M* / M_0      = (τ_0 / τ)^(1 − ε)
trade volume factor = v / v_0       = (τ_0 / τ)^ε
```

The two factors multiply to `τ_0 / τ`. The intervention always takes the same total bite out of nominal trade. The elasticity decides how that bite splits between lower prices, which is usually what you wanted, and less trade, which usually is not.

### Numbers you can check

Invented economy: `F = 10` billion crowns per day, `v_0 = 0.1` per day, `τ_0 = 4%`. The starting equilibrium is `M_0 = 10 / (0.04 × 0.1) = 2,500` billion. The tax sink collects `0.04 × 0.1 × 2,500 = 10` per day, exactly matching the faucet. Now raise the tax to 7.5%.

| Elasticity `ε` | New `v` | New `M*` | Half-life (days) | Tax sink on day 0 | `M` on day 90 | Price factor | Volume factor |
|---|---|---|---|---|---|---|---|
| 0 | 0.1000 | 1,333 | 92 | 18.75 | 1,926 | 0.533 | 1.000 |
| 0.5 | 0.0730 | 1,826 | 127 | 13.69 | 2,237 | 0.730 | 0.730 |
| 1 | 0.0533 | 2,500 | — | 10.00 | 2,500 | 1.000 | 0.533 |

Check the first row. `r = 0.075 × 0.1 = 0.0075`. `M* = 10 / 0.0075 = 1,333`. Half-life `0.693 / 0.0075 = 92` days. On day 90 the gap is `1,167 × 0.9925^90 = 1,167 × 0.508 = 593`, so `M = 1,333 + 593 = 1,926`.

Check the second. `v = 0.1 × 1.875^(−0.5) = 0.1 × 0.730 = 0.0730`. `r = 0.075 × 0.0730 = 0.00548`. `M* = 10 / 0.00548 = 1,826`.

Three things stand out.

**The first day misleads.** With `ε = 0` the tax sink jumps from 10 to 18.75 per day, nearly doubling as the naive reading predicted. That is the number the team will see in the first week's telemetry. It is not the long-run number. As the stock falls, the sink falls with it, and at the new equilibrium the sink collects exactly 10 per day again. **In the long run a proportional sink collects exactly what the faucets pour in, whatever the rate.** The rate only decides the stock level at which that happens.

**The change is slow.** Even with no behavioural response, half the adjustment takes three months. A team that checks the money supply after two weeks sees it down by about 5% and may conclude the tax is too weak. It is working exactly as designed.

**Elasticity decides whether the tax does anything useful.** At `ε = 1` the money stock does not move at all. Trade value drops 47% on day one and stays there. Prices do not fall. The tax has become pure friction: players pay more per trade, trade less, and the sink collects the same 10 per day it always did. From the money supply chart alone, you could not tell `ε = 1` from a tax change that never shipped.

### The visual

Open the interactive. The left panel plots the money stock over 365 days, with the old equilibrium as a flat line and the new path falling from it. The right panel plots the price index and the trade volume index on the same axes, both starting at 1.

Set the new tax to 7.5% and slide `ε` from 0 to 1. On the left, the money curve rises toward the old line and flattens against it. On the right, the price and volume curves swap roles. At `ε = 0`, prices fall and volume holds. At `ε = 1`, volume drops on day one and prices hold. The nominal trade value readout at the bottom settles at 133 per day in every case, which is `F / τ = 10 / 0.075`. A dashboard that only shows nominal trade value cannot tell these worlds apart. You need the price index and the volume index side by side, the week 13 decomposition again.

### Cross-game recognition

**EVE Online (release 22.02, March 12, 2025).** The base sales tax went from 4% to 7.5%, cut by the Accounting skill. On top of it, orders placed at NPC stations pay a broker fee with a 3% base. Both are the `τ` in our model, and they stack. EVE has two features that make `ε` hard to guess. Players can shift trade to player-owned structures, where broker fees are set by the owner plus a small fixed surcharge, so part of the response is substitution between markets rather than less trade. And much of EVE's value moves in direct contracts and hauling, which the market tax does not touch. The lesson for your spec is that `ε` includes every escape route players have, not just their willingness to trade.

**Old School RuneScape (Grand Exchange tax, 1% from December 9, 2021, 2% from May 29, 2025).** Rewrite the tax as `τ = 2%` below 250 million coins per item and a flat 5 million above it. The cap means `τ` falls for the most expensive items. A flat amount on a 1 billion coin item is 0.5%. So the tax bites hardest on the middle of the market and least on the top. Jagex also spends a small part of the revenue buying selected high-value items from players and deleting them, and reported in May 2025 that this item sink had removed about 5.7 trillion coins' worth of items since launch. That is a second lever working on the goods side. Removing items raises their prices directly, where the coin tax lowers the price level through the money stock. The two push individual prices in opposite directions, and a designer running both has to say which prices each is for.

**Diablo III (auction houses, closed March 18, 2014).** Closing a market is the limit of raising `τ` without bound, where trade value on that market goes to zero. Blizzard announced the closure of both the gold and real-money auction houses on September 17, 2013, and closed them six months later. Former game director Jay Wilson said in 2022 that legal questions, partly because the feature had been advertised on the box, caused much of the delay. For our purposes the six months matter because they were an announced future change, and announced changes produce behaviour before they take effect. Section 4 returns to that.

**Guild Wars 2 (Trading Post, current).** A fixed 15% total fee, split into a 5% listing fee paid up front and a 10% exchange fee on sale. A high `τ` from the start sets a low `M*` for a given faucet and a wide no-trade band around each price (MMO304 week 10). A game that launches with a high rate never has to pull this lever later, which avoids the transition problem entirely. The cost is less flipping and more price noise from day one.

Four games, one equation. Each rewrite asks what `τ` is, what base it applies to, what escape routes set `ε`, and whether the change was announced before it arrived.

### Eyes-open design judgment

- **Use a proportional sink when you want a floor on stability, not a drain.** It stabilises the money stock at `F / (τ v)`. If the faucet keeps growing, for example because the player base grows, the equilibrium grows with it. A sink raise is a one-time level shift, not a cure for a faucet that keeps rising. For that, cut the faucet or tie it to something that does not grow.
- **Estimate `ε` before you ship, or ship in a way that measures it.** Look at past fee changes in your own game, at how trade responded to event taxes, or at how much trade already moves through untaxed channels. If you cannot estimate it, ship a smaller change first. A 4% to 5% step tells you `ε` with much less damage than 4% to 7.5%.
- **Judge on the half-life, not on week one.** Write down the expected money stock at 30, 90 and 180 days before the change ships. Compare the actual path with that curve, not with the starting value.
- **Watch the price index and the volume index, never the sink revenue alone.** Sink revenue returns to `F` whatever happens, so it tells you nothing about success.
- **Prefer faucet cuts when the problem is income, and sinks when the problem is concentration of trade.** A faucet cut hits whoever earns from that faucet, often newer players doing PvE content. A sales tax hits whoever trades most, often the richest players. Choose based on who you want to pay, which is section 3.

## 3. Who pays: incidence

Every intervention has an incidence, the group that ends up bearing its cost. The group that pays the fee at the counter is often not the group that bears it.

Take a sales tax charged to the seller. Sellers fall into two groups in most MMOs. Gatherers sell raw goods they farmed and need the crowns to play. Traders buy low and sell high. After the tax rises, traders keep buying only if their margin still covers the new fee (MMO304 week 10). So they bid less for gatherers' goods. Part of the tax passes back to gatherers as lower buy prices, even though the gatherers never see a tax line. The share that passes back depends on how easily each side can walk away. Gatherers who must sell to fund repairs cannot walk away, so they bear more of it.

A faucet cut has a different incidence. Lowering bounties by 20% takes income from players who earn from bounties. In most games those are players who have not yet built a trading or crafting business, which often means newer players. The money stock falls either way, but the people who feel it are different.

A flat sink, such as a repair cost or a fixed-price cosmetic, charges the same crowns to everyone who uses it. Week 13 showed that money per player is a mean over a skewed distribution. A flat sink sized to matter to the mean player can be a large share of the median player's wealth.

A useful habit is to write one line per player group in every spec:

| Group | Faucet cut 20% | Sales tax 4% to 7.5% | New flat sink |
|---|---|---|---|
| New players | Income falls 20% | Little effect, they trade little | Large share of wealth |
| Gatherers | Some income loss | Lower buy prices from traders | Moderate |
| Traders | Little effect | Margins squeezed, some stop flipping | Negligible |
| Richest 1% | Negligible | Pay most of the tax in crowns | Negligible |

No column is right in general. The table makes you pick on purpose.

## 4. Announcements, pilots and reversal

### Announced changes act early

Lab 13's month 11 showed velocity dropping 9% after the team announced a tax rise for month 13. Traders had a reason to wait, or to sell early at the old rate and then pause. Anything announced ahead of time creates a window where players act on the future rule. The Diablo III closure had a six-month window. A patch note two weeks before a tax change has a two-week window.

That is not a reason to surprise players. Surprise changes to rules people plan around cost trust, and the governance weeks of [MMO402](../../MMO402-emergent-society-governance-and-ethics/syllabus.md) deal with that cost. It is a reason to include the announcement window in your prediction. Your 30-day forecast should start on the announcement date, not the ship date, and your baseline for measuring the effect should come from before the announcement.

### Pilots are harder than in other features

MA102 week 14 taught A/B testing: split players randomly, change one group, compare. Economies break that method because the groups trade with each other. If half the players pay 7.5% tax and half pay 4%, the 7.5% group sells through the 4% group, and you measure the escape route, not the tax. Statisticians call this interference between units.

Workable options, each with a cost:

- **Split by market, not by player.** Change the tax in one region's market and compare with others. EVE's regional markets make this possible. The cost is that trade shifts toward the untaxed regions, which inflates `ε`.
- **Step in stages.** Raise the rate in two or three steps across weeks and estimate `ε` from each step's response. The cost is a longer announcement window.
- **Simulate first.** Run the change in the agent-based model from [weeks 2](w02-agent-based-modeling-i.md) and [3](w03-agent-based-modeling-ii.md), with agents who can choose between trading, holding and using escape routes. The cost is that your agents only know the escape routes you gave them.

### Plan the reversal before you ship

Some levers reverse cleanly. A tax rate can go back down, and the stock returns to its old equilibrium with the same half-life. Others do not. Items deleted by an item sink are gone. A closed market takes years of player habit with it. A rollback after an exploit (week 12) erases legitimate play along with the exploit.

Write kill criteria into the spec. Make them numbers with dates, for example: "If the volume index is down more than 25% at day 30 while the price index is down less than 5%, `ε` is near 1 and the tax is friction. Revert to 5% and reassess." A kill criterion written after launch is a rationalisation.

## 5. The intervention spec

Your final project's policy memo is an intervention spec. One page, in this order:

1. **Diagnosis** from the week 13 identities, with the three numbers that justify acting.
2. **Target**, one metric and one value by one date.
3. **Lever and size**, with the alternatives you rejected and why.
4. **Prediction**, the equilibrium, the half-life, and the path at 30, 90 and 180 days, under at least two values of the behavioural parameter.
5. **Incidence**, one line per player group.
6. **Rollout**, announcement date, ship date, stages if any.
7. **Measurement and kill criteria**, the dashboard panels to watch and the numbers that trigger reversal.

The spec is short because the model does the work. If you cannot fill section 4, you are not ready to ship.

## In-class activity (25 minutes)

Groups of three. Use the Lab 13 economy at month 12, converted to a monthly model: `M = 1,271`, net faucet after non-tax sinks `F = 149 − 35 = 114` per month, monthly velocity `V = 4.2`, tax `τ = 2%`.

1. (5 min) Compute the current equilibrium `M* = F / (τ V)` and say whether money is still rising.
2. (8 min) The producer wants the planned rise to 4%. Compute the new `M*` and the half-life in months for `ε = 0` and `ε = 0.5`.
3. (7 min) Propose one alternative lever with a size that reaches a similar `M*` at `ε = 0`. Fill in the incidence table for both options.
4. (5 min) Write two kill criteria for your preferred option.

Expected output: two equilibria, two half-lives, one alternative and a four-row incidence table. Check: at 2%, `τV = 0.084` and `M* ≈ 1,357`.

## Common misconceptions

- **"Doubling a sink doubles the money it removes."** Only on day one. At the new equilibrium a proportional sink removes exactly the net faucet, the same as before. What changes is the stock level.
- **"The first two weeks show whether the tax worked."** With a half-life of months, two weeks shows a few percent of the adjustment. Compare against the predicted path, not the starting point.
- **"If trade volume falls after a tax rise, the tax is working."** Falling volume with stable prices is the sign of high elasticity, where the tax adds friction and removes little money relative to the damage.
- **"We can A/B test the tax on half the players."** Players on different rates trade with each other. Split by market or stage the change instead.

## Check yourself

1. A game has `F = 6` per day, `v = 0.08` per day and a 3% sales tax. Compute `M*` and the half-life. The tax rises to 5% with `ε = 0`. What is the new `M*`?
2. In question 1 the tax rises to 5% with `ε = 0.5`. Compute the new `v`, the new `M*`, and the equilibrium price and volume factors.
3. A designer wants the money stock 20% lower in the long run and assumes `ε = 0`. By what factor must the tax rise? What happens to that plan if `ε` turns out to be 0.5?
4. A tax change goes live on day 0. On day 14 the money stock is down 4% and sink revenue is up 70%. The designer says the tax is too weak and wants to raise it again. Using the model, write a two-sentence reply.
5. Explain in terms of incidence why raising a seller-paid sales tax can lower gatherers' income even if gatherers rarely list items themselves.

<details>
<summary>Answers</summary>

1. `r = 0.03 × 0.08 = 0.0024`, `M* = 6 / 0.0024 = 2,500`, half-life `0.693 / 0.0024 ≈ 289` days. At 5%, `r = 0.004`, `M* = 1,500`.
2. `v = 0.08 × (5/3)^(−0.5) = 0.08 × 0.775 = 0.0620`. `r = 0.05 × 0.0620 = 0.0031`, `M* = 6 / 0.0031 ≈ 1,936`. Price factor `(3/5)^0.5 = 0.775`, volume factor `0.775`.
3. `M*` scales with `1/τ` when `ε = 0`, so the tax must rise by `1/0.8 = 1.25`. With `ε = 0.5`, the price factor is `(1/1.25)^0.5 = 0.894`, so the stock falls only about 11%, and trade volume also falls about 11%.
4. With a half-life of months, a 4% drop in two weeks is on track. Compare it with the predicted day-14 value before changing anything, and remember that sink revenue will drift back down toward the faucet total as the stock falls.
5. Traders who buy from gatherers must now clear a higher fee on resale, so they bid less. Gatherers who sell to traders or accept buy orders get lower prices, bearing part of the tax without paying it directly.

</details>

## Lab / assignment hook

[Lab 14, sizing an intervention](../labs/lab14.md). You calibrate the stock-flow model to your Lab 13 results, forecast the planned tax rise under three elasticities, compare it with a faucet cut, and write a one-page intervention spec in the section 5 format. That spec is a draft of the policy memo for the final project (week 15).

## Sources

- EVE University Wiki, "Sales tax" (accessed September 2026). Base sales tax raised from 4% to 7.5% in version 22.02, released March 12, 2025; reduced by the Accounting skill; NPC station broker fee base 3%, reduced by Broker Relations and standings; player-owned structures charge an owner-set fee plus a fixed surcharge.
- Old School RuneScape Wiki, "Grand Exchange tax" (accessed September 2026). 1% from December 9, 2021; 2% from May 29, 2025; cap of 5 million coins per item; most revenue removed, part used to buy and delete selected items; Jagex's May 29, 2025 figure of about 5.7 trillion coins' worth of items removed by the item sink since launch.
- Wikipedia, "Diablo III" (accessed September 2026). Closure of both auction houses announced September 17, 2013, effective March 18, 2014; Jay Wilson's 2022 remarks on legal issues and retail packaging as a cause of the delay.
- Guild Wars 2 Wiki, "Trading Post" (accessed September 2026). 5% listing fee and 10% exchange fee, 15% total.
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press.

## Interactive spec: examples/w14-tax-change-simulator.html

**Purpose.** Show that raising a proportional sink moves the money stock to a new level, not to zero, and that the behavioural elasticity decides whether the effect lands on prices or on trade volume.

**Layout.** Controls on top. Two panels side by side at desktop width, stacked on mobile (left first). A readout strip underneath.

**Controls.**
- Old tax `τ_0`: slider 0.5% to 10%, step 0.5, default 4%.
- New tax `τ`: slider 0.5% to 20%, step 0.5, default 7.5%.
- Elasticity `ε`: slider 0 to 1.5, step 0.05, default 0. Labels at 0 ("players ignore the tax"), 1 ("trade falls as fast as the tax rises").
- Net faucet `F`: slider 1 to 30 per day, step 1, default 10.
- Base velocity `v_0`: slider 0.02 to 0.3 per day, step 0.01, default 0.1.
- Day marker: slider 0 to 365, default 90. Drives the readout.
- Preset buttons: "EVE-like 4% to 7.5%" (sets `τ_0 = 4%`, `τ = 7.5%`), "OSRS-like 1% to 2%" (sets `τ_0 = 1%`, `τ = 2%`, `v_0 = 0.1`).

**Computation.**
- `M_0 = F / (τ_0 v_0)`. `v = v_0 (τ/τ_0)^(−ε)`. `r = τ v`. `M* = F / r`.
- Iterate daily from `M_0` for 365 days: `M_{t+1} = M_t + F − r M_t`.
- Price index `P_t = M_t / M_0`. Volume index `Q_t = v / v_0` (a step at day 0, constant after). Nominal trade value `T_t = v M_t`. Tax sink `S_t = τ v M_t`.
- Half-life `ln 2 / r`. Equilibrium price factor `(τ_0/τ)^(1−ε)`, volume factor `(τ_0/τ)^ε`.

**Left panel, money stock.** x axis days 0 to 365. y axis money stock from 0 to `1.1 × max(M_0, M*)`. Dashed horizontal line at `M_0` labelled "old equilibrium", dotted line at `M*` labelled "new equilibrium", solid path `M_t`. Mark the half-life day with a small tick if it is inside the range.

**Right panel, prices and volume.** x axis days 0 to 365. y axis index 0 to 1.2. Two lines, price index (solid) and volume index (dashed), both 1 before day 0. Caption: "The tax takes the same bite from nominal trade. Elasticity decides whether it comes from prices or from trade."

**Readout at the day marker.** `M_t`, `M*`, gap closed as a percentage, half-life, tax sink `S_t` and `F` side by side, nominal trade `T_t` and its limit `F/τ`, price index, volume index.

**The one insight.** Sliding `ε` from 0 to 1 at the EVE-like preset makes the money path flatten onto the old equilibrium while the price and volume lines swap places, and the nominal trade readout converges to 133.3 in every case.

**Test values (defaults `F = 10`, `v_0 = 0.1`, `τ_0 = 4%`, `τ = 7.5%`).**
- `M_0 = 2,500`, nominal trade at day 0 before the change 250, sink 10.
- `ε = 0`: `M* = 1,333.3`, half-life 92.4 days, `S_0 = 18.75`, `M_30 = 2,264.1`, `M_90 = 1,925.8`, `M_180 = 1,634.2`, `M_365 = 1,408.1`, price factor at equilibrium 0.533, volume 1.
- `ε = 0.5`: `v = 0.07303`, `M* = 1,825.7`, half-life 126.6 days, `S_0 = 13.69`, `M_90 = 2,237.0`, `M_365 = 1,916.6`, both equilibrium factors 0.730.
- `ε = 1`: `v = 0.05333`, `M* = 2,500`, `M_t = 2,500` for all `t`, `S_t = 10`, volume index 0.533 from day 0.
- `τ = τ_0`: nothing changes at any `ε`.

**Accessibility.** Lines differ by dash pattern as well as colour. Every slider shows its value as text and works from the keyboard. Colours from `templates/interactive-tokens.css`. No animated transitions when `prefers-reduced-motion` is set.

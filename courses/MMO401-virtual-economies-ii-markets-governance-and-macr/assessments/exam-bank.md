# MMO401 · Exam bank: practice, quiz and viva questions

MMO401 has no written exam. The grade comes from the ABM labs (40%) and the final agent-based model and policy memo (60%). This bank does three other jobs.

- **Practice.** Work a week's questions before its lab is due. If you can answer them without the lecture open, the lab will go quickly.
- **Weekly quizzes.** Each week opens with an ungraded 10-minute quiz of two or three questions from this bank. Usually one is a compute question with new numbers and one is an explain or critique question.
- **Viva.** The final project ends with a 15-minute oral defense ([final-model-and-memo-brief.md](final-model-and-memo-brief.md)). Examiners draw viva questions in the style of this bank and rewrite them with numbers from your own model. The lab code reviews in the [ABM labs brief](abm-labs-brief.md) use the same style.

Every question is tagged with the week or weeks it draws on and a type.

- **compute**: apply a lecture model to numbers you have not seen before.
- **explain**: say why a model behaves the way it does, with a number as evidence.
- **design**: choose values that meet a stated goal and show that they meet it.
- **critique**: find what is wrong with a claim or a proposal and say how to fix it.

All numbers are invented unless a question names a game. Every game fact used here comes from the lecture of the tagged week, which cites its source and version. Every answer was recomputed in Python. Where rounding matters, the solution says how it was rounded. Write your own answer before you open the solution.

---

## Week 1: The in-house economist role

1. *Week 1 · compute.* An invented MMO has three traded goods. Ore goes from 8 to 12 gold while units sold fall from 500 to 350. Potions go from 30 to 27 while sales rise from 200 to 260. Bows go from 400 to 360 while sales rise from 10 to 14. Compute the Laspeyres, Paasche and Fisher indices for month 1 against month 0.

<details>
<summary>Answer and worked solution</summary>

**Answer:** L = 107.1, P = 100.4, F = 103.7.

The four sums, goods in the order ore, potion, bow:

- `Σ p0 q0 = 8×500 + 30×200 + 400×10 = 4,000 + 6,000 + 4,000 = 14,000`
- `Σ p1 q0 = 12×500 + 27×200 + 360×10 = 6,000 + 5,400 + 3,600 = 15,000`
- `Σ p0 q1 = 8×350 + 30×260 + 400×14 = 2,800 + 7,800 + 5,600 = 16,200`
- `Σ p1 q1 = 12×350 + 27×260 + 360×14 = 4,200 + 7,020 + 5,040 = 16,260`

`L = 100 × 15,000 / 14,000 = 107.1`. `P = 100 × 16,260 / 16,200 = 100.4`. `F = sqrt(107.1 × 100.4) = 103.7`.

The 6.8-point gap between L and P is substitution bias. Players bought 30% less of the good that rose 50%.
</details>

2. *Week 1 · compute.* Use the data from question 1. A new player buys ore and potions. A veteran buys bows. Compute each basket's Laspeyres index and write the observation line of a policy memo in the week 1 format.

<details>
<summary>Answer and worked solution</summary>

**Answer:** new-player basket 114.0, veteran basket 90.0.

New player: base cost `8×500 + 30×200 = 10,000`, cost at month-1 prices `12×500 + 27×200 = 11,400`, index 114.0.

Veteran: base cost `400×10 = 4,000`, at month-1 prices `360×10 = 3,600`, index 90.0.

Observation line: "The new-player basket (ore and potions, Laspeyres, auction-house data, month 0 to 1) rose 14.0%, while the veteran basket (bows) fell 10.0%." The whole-economy +7.1% describes neither group, and the memo should say so.
</details>

3. *Week 1 · compute.* An economy holds 40,000 million gold. Last month faucets paid 3,200 million and sinks removed 2,000 million. Express both flows as a share of the stock. If those shares held for a year and applied to the current stock each month, how much larger would the money supply be after 12 months?

<details>
<summary>Answer and worked solution</summary>

**Answer:** faucets 8.0%, sinks 5.0%, net +3.0% a month, about 42.6% larger after a year.

`3,200 / 40,000 = 8%`. `2,000 / 40,000 = 5%`. Net growth 3% a month compounds to `1.03^12 = 1.426`.

The share form is the one a designer can reason with. "3,200 million" means nothing on its own. "Faucets add 8% of the money supply every month" tells a designer the money supply will grow by about 43% this year if nothing changes.
</details>

4. *Week 1 · critique.* A colleague's memo reads, in full: "Inflation is 2.1% this month. We recommend a 5% auction-house fee." List what is missing against the five-part memo format, and name the first number you would compute before accepting the recommendation.

<details>
<summary>Answer and worked solution</summary>

**Answer:** it has a number and a recommendation, and nothing that connects them.

- **Observation** lacks a basket, a formula and a period. "2.1%" of whose shopping, Laspeyres or Paasche, which months?
- **Diagnosis** is missing. No mechanism explains why prices moved.
- **Options** are missing. One option with no predicted effect and no cost is not a choice.
- The **recommendation** has no reason.
- **What we will measure** is missing. Nothing says which result would reverse the fee.

First number to compute: the index for at least two baskets (new player and veteran), and the Laspeyres against Paasche gap. Week 1's example shows a whole-economy +4.4% hiding a +35% starter basket and a −20% veteran basket. A flat fee would hit the group that is already worse off.
</details>

## Week 2: Agent-based modeling I

5. *Week 2 · compute.* A random-exchange server has an average balance `T = 40` gold and trades of `d = 2` gold. Predict the median balance, the share of players below the mean, the top-10% share, the Gini coefficient and the share of broke players once the model settles.

<details>
<summary>Answer and worked solution</summary>

**Answer:** median about 27.7 gold, 63.2% below the mean, top 10% hold 33.0%, Gini 0.50, about 4.8% broke.

- Median `T × ln 2 = 40 × 0.693 = 27.7`.
- Below the mean `1 − e^(−1) = 63.2%`, whatever `T` is.
- Top-10% share `0.1 × (1 + ln 10) = 33.0%`.
- Gini of an exponential distribution: exactly 0.5.
- Broke share with discrete chunks: `1 / (T/d + 1) = 1 / 21 = 4.8%`.

Four of these five numbers do not depend on `T`. The shape is the same on every server. Only the scale changes.
</details>

6. *Week 2 · compute.* Server A has five players with 0, 10, 20, 30 and 40 gold. Server B has five players with 10, 10, 10, 10 and 60 gold. Compute each Gini coefficient with the double-sum formula. What does the result tell you about reporting a Gini alone?

<details>
<summary>Answer and worked solution</summary>

**Answer:** both are 0.40.

Both servers have `n = 5` and mean `μ = 20`, so the denominator is `2 × 25 × 20 = 1,000`.

Server A: the pairwise differences are 10 (four pairs), 20 (three), 30 (two) and 40 (one), which sum to `40 + 60 + 60 + 40 = 200`. The double sum counts each pair twice, so 400. `G = 0.40`.

Server B: only the four pairs with the 60-gold player differ, each by 50, so the sum is 200 and the double sum 400. `G = 0.40`.

The Gini is one number for a whole shape. A has a steady ladder with one broke player. B has four identical players and one rich one. Players in those worlds have different experiences. Report the Gini with the median, the share below an affordability line and the top-10% share.
</details>

7. *Week 2 · compute.* Four players share 3 identical coins. How many arrangements are there? In how many does player A hold 0, 1, 2 and 3 coins? What share of the time does A hold less than the average?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 20 arrangements. A holds 0, 1, 2, 3 coins in 10, 6, 3 and 1 of them. A is below the average 50% of the time.

Coins into players: `C(3 + 4 − 1, 3) = C(6, 3) = 20`. If A holds `a` coins, the other `3 − a` coins go to three players in `C(3 − a + 2, 2)` ways: 10, 6, 3, 1.

The average is 0.75 coins, so "below average" means holding 0, which is `10/20 = 50%`. The probabilities fall steadily with wealth, 50%, 30%, 15%, 5%, the start of the exponential staircase. Fair random trade wanders over these 20 arrangements equally, and the equal-ish ones are rare.
</details>

8. *Week 2 · compute.* Four buyers value a potion at 40, 32, 25 and 18 gold. Four sellers can make one for 12, 20, 28 and 35 gold. What is the maximum total surplus, and which prices clear the market? A zero-intelligence market pairs the 40-buyer with the 20-seller and the 25-buyer with the 12-seller. What is its allocative efficiency?

<details>
<summary>Answer and worked solution</summary>

**Answer:** maximum surplus 40 gold, from two trades. Any price above 25 and below 28 clears. The zero-intelligence pairing reaches 82.5%.

Sort buyers high to low and sellers low to high. Pair 1: `40 − 12 = 28`. Pair 2: `32 − 20 = 12`. Pair 3: `25 − 28 = −3`, which should not trade. Maximum surplus `28 + 12 = 40`.

At a price above 25 only two buyers want to buy. Below 28 only two sellers want to sell. So the clearing range is 25 to 28, exclusive.

The zero-intelligence pairing gives `(40 − 20) + (25 − 12) = 20 + 13 = 33`. Efficiency `33 / 40 = 82.5%`. The loss comes from the wrong buyer (25 instead of 32) getting a unit, the exact failure the lecture names.
</details>

9. *Week 2 · critique.* An analyst reports: "Our server's wallet Gini is 0.53. That is proof that gold farmers are hoarding." Critique the claim and say what you would compute before believing it.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 0.53 is close to what pure chance produces, so it proves nothing on its own.

The random-exchange baseline with identical players settles near 0.5, and 0.51 to 0.52 with chunky trades (week 2 table: 0.512 at 1,000 trades per player). A measured 0.53 is within a few hundredths of a world with no farmers at all.

Before believing it:

1. Run the random-exchange model with the server's real player count and money supply, several seeds, and compare the settled Gini.
2. Add one real rule at a time (income from play, flat and proportional sinks) and see which one moves the baseline.
3. Look at concentration directly. What share of gold sits in the top 1% of accounts, and are those accounts linked?

A pattern that would appear with random players is a baseline, not a discovery.
</details>

## Week 3: Agent-based modeling II

10. *Week 3 · compute.* Four players hold 60, 120, 180 and 240 gold. With trading switched off, apply one tick of policies A, B and C with `f = 15` and `r = 10%`. Give the new balances, the totals and each Gini. What is the balance point?

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Policy | Balances | Total | Gini |
|---|---|---|---|
| Start | 60, 120, 180, 240 | 600 | 0.250 |
| A: `0.9x + 15` | 69, 123, 177, 231 | 600 | 0.225 |
| B: `0.9x + 60 × x / 600` | 60, 120, 180, 240 | 600 | 0.250 |
| C: `1.1x − 15` | 51, 117, 183, 249 | 600 | 0.275 |

The balance point is `f / r = 150`, the mean. Gaps from 150 were −90, −30, +30, +90. Policy A shrinks them by 10% to −81, −27, +27, +81. Policy C grows them by 10%. In B each player's faucet `0.1x` cancels the sink `0.1x`, so nothing moves. Three identical money totals, three directions for the Gini.
</details>

11. *Week 3 · compute.* Under policy C with `r = 4%` and `f = 8`, a player holds 170 gold and trading is off. How many ticks until the player is broke? What happens to the money supply after that?

<details>
<summary>Answer and worked solution</summary>

**Answer:** the player hits zero during tick 49. After that the money supply starts to grow.

Balance point `f / r = 8 / 0.04 = 200`. The player is 30 below it, and policy C multiplies the gap by 1.04 each tick. They reach 0 when the gap reaches 200: `30 × 1.04^t = 200`, so `t = ln(6.667) / ln(1.04) = 48.4`. Stepping the rule tick by tick confirms that the floor binds on tick 49.

From then on the flat sink under-collects. The broke player owes 8 a tick and pays nothing, while the proportional faucet keeps paying the rich players. Less money leaves than enters, so the total climbs, as in the lecture's tick-6 row.
</details>

12. *Week 3 · compute.* Policy X gives a mean Gini of 0.284 with sample standard deviation 0.018 over 16 replications. Policy Y gives 0.262 with standard deviation 0.024 over 16 replications, using the same seeds. Give each 95% interval and decide whether the policies differ.

<details>
<summary>Answer and worked solution</summary>

**Answer:** X is 0.284 ± 0.009 (0.275 to 0.293). Y is 0.262 ± 0.012 (0.250 to 0.274). They differ, just.

`SE_X = 0.018 / 4 = 0.0045`, times 1.96 is 0.0088. `SE_Y = 0.024 / 4 = 0.006`, times 1.96 is 0.0118.

The intervals do not overlap, though they nearly touch. A sharper test uses the difference: `0.022 / sqrt(0.0045² + 0.006²) = 0.022 / 0.0075 = 2.9` standard errors, which is past 1.96. Because the runs share seeds (common random numbers), a paired test on the 16 per-seed differences would be sharper still. Then ask whether a 0.022 Gini difference changes any player's experience. Statistics cannot answer that part.
</details>

13. *Week 3 · critique.* A classmate implements policy A with `r = 5%` and `f = 5` on 1,000 players starting at 100 gold. Their settled money supply is 95,000, not 100,000. They conclude that policy A leaks money. What went wrong, and which test would have caught it?

<details>
<summary>Answer and worked solution</summary>

**Answer:** they applied the faucet before the sink. Policy A is balanced. Their code is not.

The specification is sink first, `x → x − r·x + f`, with steady state `f / r = 100` per player. Faucet first gives `x → (x + f)(1 − r)`, with steady state `f(1 − r) / r = 5 × 0.95 / 0.05 = 95` per player, so 95,000 in total.

This is a verification bug, not a finding about the policy. The four-player unit test from section 5 of the week 3 lecture catches it. With trading off, one tick must turn a known input into a known output. With the wrong order the numbers come out lower on every player.
</details>

14. *Week 3 · explain.* Classify each rule as a flat or proportional faucet or sink, and predict whether it compresses or spreads the wealth distribution. (a) A daily login chest of 50 gold. (b) Housing upkeep of 500 gold a week. (c) Boss loot whose value rises with the player's gear. (d) A 3% auction-house cut. (e) Repairs costing 10% of item value. Which one should you model with a floor, and why?

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Rule | Shape | Effect |
|---|---|---|
| (a) Login chest | Flat faucet | Compresses |
| (b) Housing upkeep | Flat sink | Spreads |
| (c) Gear-scaled loot | Proportional faucet | Spreads |
| (d) Auction cut | Proportional sink (on trade, roughly on wealth) | Compresses |
| (e) Repairs | Roughly proportional sink (scales with the gear players own) | Compresses |

The upkeep needs a floor in the model. A player who cannot pay 500 gold pays what they have or loses the house. Either way the sink under-collects, like policy C in week 3, and the money supply drifts up. Model the leak and cap or exempt the poorest players on purpose.
</details>

## Week 4: Monetary policy tools in games

15. *Week 4 · compute.* A closed server has `g = 30` gold per player per day, velocity `v = 6%` and a trade tax `τ = 3%`. Players start at `m(0) = 8,000`. Compute `σ`, the steady state, the half-life, and `m` at days 365 and 730.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `σ = 0.0018`, `m* = 16,667`, half-life about 385 days, `m(365) ≈ 12,176`, `m(730) ≈ 14,340`.

`σ = 0.03 × 0.06 = 0.0018`. `m* = 30 / 0.0018 = 16,667`. Half-life `ln 2 / −ln(0.9982) = 384.7`, and the shortcut `0.693 / 0.0018` gives 385.

`m(365) = 16,667 + (8,000 − 16,667) × 0.9982^365 = 16,667 − 8,667 × 0.5195 = 12,176`.
`m(730) = 16,667 − 8,667 × 0.2699 = 14,340`.

Two years in, the server has closed only 73% of the gap to its ceiling.
</details>

16. *Week 4 · compute.* A server has `g = 50`, `v = 5%` and `m(0) = 12,000`. You can cut `g` to 40, or add a 1% trade tax and leave `g` at 50. Which gives lower money per player at day 365? At day 730? At about which day do they cross, and why is it later than the day the tax first removes more per day?

<details>
<summary>Answer and worked solution</summary>

**Answer:** the faucet cut is lower at day 365 (26,600 against 26,683). The tax is lower at day 730 (38,916 against 41,200). They cross at day 389.

Faucet cut: `m(t) = 12,000 + 40t`, so 26,600 and 41,200.

Tax: `σ = 0.01 × 0.05 = 0.0005`, `m* = 50 / 0.0005 = 100,000`, `m(t) = 100,000 − 88,000 × 0.9995^t`. That gives 26,683 at day 365 and 38,916 at day 730.

The cut removes 10 gold a day from day 1. The tax removes `0.0005 × m`, which is only 6 gold at `m = 12,000` and passes 10 gold once `m` exceeds 20,000. By then the cut has built a lead. The tax needs extra days to win that lead back, so the paths cross at day 389, not on the day the daily removals match.
</details>

17. *Week 4 · compute.* A feedback rule has `g = 45`, `v = 5%` and target `m = 18,000`, with `k = 0.3`. What is the neutral rate? What tax does the rule set when it observes 21,600? When it observes 13,500? What risk does the second case carry with a 60-day data lag?

<details>
<summary>Answer and worked solution</summary>

**Answer:** neutral rate 5%. At 21,600 the rule sets 11%. At 13,500 it wants −2.5% and clamps to 0%.

`τ_n = g / (v × m_target) = 45 / (0.05 × 18,000) = 5%`.

At 21,600: `5% + 0.3 × (21,600/18,000 − 1) = 5% + 0.3 × 0.2 = 11%`.

At 13,500: `5% + 0.3 × (0.75 − 1) = 5% − 7.5% = −2.5%`, clamped to 0.

With a 60-day lag the rule keeps seeing the old low values after money has already recovered. It holds the tax at 0 too long and overshoots above target. Week 4's table shows the same `k`-and-lag pattern turning a smooth rule into a swinging one. Cut the lag or lower `k`.
</details>

18. *Week 4 · compute.* A server sits under a proportional sink with `σ = 0.002` per day. On day 0 a luxury item removes 4,000 gold per player. How much of that 4,000 gap to the no-sink path remains after 365 days? After 693 days? What would remain after 693 days on a server with no proportional sink?

<details>
<summary>Answer and worked solution</summary>

**Answer:** about 1,926 after 365 days and about 999 after 693 days. With no proportional sink, all 4,000 remain.

With a ceiling, the one-off gap closes like any other gap: `4,000 × 0.998^t`. At `t = 365` that is `4,000 × 0.4816 = 1,926`. At `t = 693`, one half-life (`0.693 / 0.002 ≈ 347` days) twice over, `4,000 × 0.2497 ≈ 999`.

With no ceiling, money grows by `g` a day on both paths and the 4,000 difference never closes. Either way the one-off sink changed the level once. It changed neither the slope nor the ceiling.
</details>

19. *Week 4 · critique.* Prices rose 6% this quarter. A producer proposes raising the trade tax from 2% to 4% "to stop inflation this quarter." Velocity is 4% a day. Critique the proposal with the model and propose a package.

<details>
<summary>Answer and worked solution</summary>

**Answer:** the tax is the right lever for year three and the wrong one for this quarter.

`σ` goes from `0.02 × 0.04 = 0.0008` to `0.0016`. The half-life goes from about 866 days to about 433 days. Doubling the rate halves the ceiling `m*`, but even at the new rate the server closes only about 13% of the gap to that ceiling in a quarter (`1 − 0.9984^90 = 0.134`).

A package that acts this quarter:

- A faucet cut, which bends the slope from the next day.
- The tax rise, announced as a long-run ceiling, with the half-life stated in the patch notes so players do not read next month's price rise as failure.
- A measurement line: money per active player at 30, 90 and 180 days against the predicted path.

Also check velocity. If `v` falls when the tax rises, `σ` rises by less than the factor of 2.
</details>

## Week 5: Market microstructure, order books and spreads

20. *Week 5 · compute.* The ask side of a book is 50 × 20, 52 × 30, 55 × 50 and 60 × 100 (price × quantity). For market buy orders of 90 and 150 units, give the total cost, average price, marginal price and slippage.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| `Q` | Total cost | Average | Marginal | Slippage |
|---|---|---|---|---|
| 90 | 4,760 | 52.89 | 55 | 5.8% |
| 150 | 8,310 | 55.40 | 60 | 10.8% |

90 units: `20×50 + 30×52 + 40×55 = 1,000 + 1,560 + 2,200 = 4,760`. Average `4,760 / 90 = 52.89`, slippage `52.89 / 50 − 1 = 5.8%`.

150 units: `1,000 + 1,560 + 50×55 + 50×60 = 1,000 + 1,560 + 2,750 + 3,000 = 8,310`. Average 55.40, slippage 10.8%.

The marginal price after the 150-unit order is 60, 20% above the old best ask, while the buyer's average is only 10.8% above it. The average trails the marginal, as the linear model predicts.
</details>

21. *Week 5 · compute.* A book has best ask 30 and a linear depth of `d = 40` units per gold. For a 160-unit buy, give the marginal price, average price and slippage. What happens to the slippage if a server merge doubles depth?

<details>
<summary>Answer and worked solution</summary>

**Answer:** marginal 34, average 32, slippage 6.7%. Doubling depth halves the slippage to 3.3%.

`marginal = a + Q/d = 30 + 160/40 = 34`. `avg = a + Q/(2d) = 30 + 2 = 32`. `32 / 30 − 1 = 6.7%`.

With `d = 80`: `avg = 30 + 160/160 = 31`, slippage 3.3%. Slippage scales with `Q / d`, which is why pooling books across realms, as World of Warcraft did for commodities in patch 9.2.7, helps large buyers most.
</details>

22. *Week 5 · compute.* (a) A game charges a 2% broker fee on every placed order and a 4% sales tax on every sale. What is the break-even spread for a market maker? (b) Using the EVE fee rules from the lecture (broker fee 3% base minus 0.3 points per Broker Relations level, sales tax 7.5% base minus 11% of it per Accounting level, standings ignored), what is the break-even spread for a trader with Broker Relations III and Accounting IV?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 8.5%. (b) about 9.0%.

(a) `A / B = (1 + b) / (1 − b − t) = 1.02 / 0.94 = 1.0851`.

(b) `b = 3% − 3 × 0.3% = 2.1%`. `t = 7.5% × (1 − 4 × 0.11) = 7.5% × 0.56 = 4.2%`. `A / B = 1.021 / (1 − 0.021 − 0.042) = 1.021 / 0.937 = 1.0896`.

The partly skilled trader sits between the lecture's 15.1% (no skills) and 6.7% (both at V). In an item where fully skilled traders compete spreads down toward 6.7%, this trader cannot profit.
</details>

23. *Week 5 · design.* You want market makers to be able to profit on any spread above 4%. You will charge the same rate `b` as a broker fee on placed orders and as a sales tax. What rate do you need? Check it.

<details>
<summary>Answer and worked solution</summary>

**Answer:** about 1.30% for each fee.

Set `(1 + b) / (1 − 2b) = 1.04`. Then `1 + b = 1.04 − 2.08b`, so `3.08b = 0.04` and `b = 0.01299`.

Check: `1.01299 / (1 − 0.02597) = 1.01299 / 0.97403 = 1.0400`.

A designer who wants a merchant profession would pick a higher floor. One who wants tight spreads for casual players would pick a lower one. The formula turns that choice into a rate.
</details>

24. *Week 5 · critique.* A game prices items to the nearest 0.01 gold. Rare items sell for about 2,000,000 gold, and there is no fee to modify an order. Players complain that their listings are undercut within seconds. A designer proposes a 10-minute cooldown on price changes. Critique the diagnosis and compare two levers.

<details>
<summary>Answer and worked solution</summary>

**Answer:** the root cause is that one tick costs nothing. On a 2,000,000-gold item a 0.01 tick is 0.0000005% of the price, so undercutting is free and the queue becomes a reaction-time race that rewards automation.

The cooldown limits how often each player can reprice. It does not make undercutting cost anything, and it slows honest responses to real news.

A relative tick (for example 0.1% of price) makes each undercut give up margin. A modification fee as a share of order value, like EVE's relist fee, makes each undercut cost gold, so it pays only when the expected fill is worth more than the fee. Either one attacks the cause. Say which cost your players will notice least and pick that one.
</details>

## Week 6: Manipulation, cornering and cartels

25. *Week 6 · compute.* A reagent's normal price is `P_0 = 20`. Its ask side holds 100 units at each of 20, 21, 22, 23 and 24. Demand is `D(P) = 300 − 10P` per day. Compute the cost of the float, the premium, the best hold price, the maximum daily markup income and the break-even lag. What is the cornerer's profit if supply returns after 6 days? After 12 days?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `C = 11,000`, premium 1,000, best price 25, daily markup 250, `L* = 4` days. Profit +500 at 6 days and about +1,917 at 12 days.

`C = 100 × (20 + 21 + 22 + 23 + 24) = 11,000`. `F = 500`. Premium `11,000 − 500 × 20 = 1,000`.

Demand is zero at 30, so `P* = (20 + 30)/2 = 25`. Players buy `300 − 250 = 50` a day at a markup of 5, so 250 a day. `L* = 1,000 / 250 = 4` days.

At `L = 6`: sales `50 × 6 = 300` fit in the float. Profit `250 × 6 − 1,000 = 500`.

At `L = 12`: 50 a day would need 600 units, more than the float. The cornerer raises the price until `D(P) × 12 = 500`, so `P = 30 − 500/120 = 25.83`. Profit `25.83 × 500 − 11,000 = 1,917`.
</details>

26. *Week 6 · compute.* Use the corner from question 25. Compute the break-even lag under (a) an NPC vendor selling the reagent at 22, and (b) a second source that supplies 30 units a day whatever the price.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 6.25 days. (b) about 8.2 days.

(a) The ceiling caps the hold price at 22. Daily income `(22 − 20) × (300 − 220) = 2 × 80 = 160`. `L* = 1,000 / 160 = 6.25`.

(b) The cornerer sells only `300 − 10P − 30 = 270 − 10P`, zero at 27. Best price `(20 + 27)/2 = 23.5`, daily income `3.5 × 35 = 122.5`. `L* = 1,000 / 122.5 = 8.2`.

A 6-day supply lag makes the corner pay in the baseline (`L* = 4`) and lose under either lever. Neither lever bans anything.
</details>

27. *Week 6 · design.* The supply lag for the reagent in question 25 is 6 days. What is the highest NPC vendor price that makes the corner unprofitable? What does that price cost gatherers?

<details>
<summary>Answer and worked solution</summary>

**Answer:** any vendor price below about 22.11.

With a ceiling `c` below 25, the best hold price is `c`. The corner loses when `(c − 20)(300 − 10c) × 6 < 1,000`. Put `x = c − 20`. Then `x(100 − 10x) < 166.7`, which gives `10x² − 100x + 166.7 > 0`. The smaller root is `x = (100 − sqrt(10,000 − 6,667)) / 20 = 2.113`. So `c < 22.11`.

Cost: gatherers can never sell above about 22.1, only 10.6% above normal, however scarce the reagent gets. The vendor price also loses meaning as the price level drifts (week 4), so index it to a price index if you ship it.
</details>

28. *Week 6 · compute.* Two producers face `P = 120 − Q` with a unit cost of 20. Compute each producer's profit as a cartel, under Cournot competition, and when one cheats on the cartel quota. What patience `δ` holds the cartel together? Compare with the lecture's threshold for `A = 100`, `c = 10`, and explain the result.

<details>
<summary>Answer and worked solution</summary>

**Answer:** cartel 1,250 each, Cournot 1,111.1 each, cheater 1,406.25 and loyal member 937.5. `δ ≥ 0.53`, the same as the lecture.

- Cartel: monopoly output `(120 − 20)/2 = 50`, 25 each, price 70, profit `50 × 25 = 1,250`.
- Cournot: each makes `100/3 = 33.33`, price 53.33, profit `33.33² = 1,111.1`.
- Cheat: best response to 25 is `(100 − 25)/2 = 37.5`. Total 62.5, price 57.5. Cheater `37.5 × 37.5 = 1,406.25`, loyal `37.5 × 25 = 937.5`.

`δ ≥ (1,406.25 − 1,250) / (1,406.25 − 1,111.1) = 156.25 / 295.1 = 0.529`.

In a linear Cournot market every profit scales with `(A − c)²`. The ratio that sets `δ` cancels that factor, so the threshold for two firms is 0.53 whatever the demand level or cost. It depends on the number of firms (0.57 for three), not on the size of the market.
</details>

29. *Week 6 · critique.* An alert fires. In one hour, four accounts bought an herb with shares of 60%, 20%, 10% and 10%. Compute the buyer HHI and compare it with four equal buyers. The on-call designer wants to suspend the top account. What would you check first?

<details>
<summary>Answer and worked solution</summary>

**Answer:** HHI 4,200 against 2,500 for four equal buyers.

`60² + 20² + 10² + 10² = 3,600 + 400 + 100 + 100 = 4,200`. Four equal buyers give `4 × 25² = 2,500`.

Concentration is a reason to look, not proof. Check first:

- Whether the top account relisted the herb at a higher price soon after. That is the corner signature.
- Whether it belongs to a guild whose raid starts tonight. Forty raiders' flasks look like a corner.
- Whether the purchases came before a patch note that raises the herb's demand, which would point to leaked information.

Then compute `L*` for this herb. If new supply returns faster than `L*`, the corner fails on its own and a suspension punishes a trader the market is already punishing.
</details>

## Week 7: Taxes and fees as policy

30. *Week 7 · compute.* Use the lecture's market (demand `Q = 100 − P_b`, supply `Q = P_s`, tax `t` on the seller). At `t = 8%`, give `P_b`, `P_s`, `Q`, the sink `R`, the deadweight loss and the number of trades on the discrete 100-bid, 100-ask book.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `P_b = 52.08`, `P_s = 47.92`, `Q = 47.92`, `R = 199.7`, deadweight loss 4.3, 48 trades on the discrete book.

`P_b = 100 / 1.92 = 52.08`. `P_s = 0.92 × 52.08 = 47.92`. `Q = 100 − 52.08 = 47.92`.

`R = 0.08 × 52.08 × 47.92 = 199.7`. `DWL = 2,500 − (100 × 47.92 − 47.92²) = 2,500 − 2,495.7 = 4.3`.

Discrete book: count `k` with `101 − k ≥ k / 0.92`. At `k = 48`: `53 ≥ 52.17`, true. At `k = 49`: `52 ≥ 53.26`, false. So 48.

The tax deletes almost 200 gold a day and destroys about 4 gold of trade value. At single-digit rates a tax is a cheap sink.
</details>

31. *Week 7 · compute.* Add the bypass channel with maximum bypass cost `E = 30`. At `t = 10%`, what share of trades leaves the market, how many stay, and what is the sink `R_m`? At which rate does `R_m` peak, and how big is the peak?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 17.5% bypass, 39.06 trades stay, `R_m = 205.6`. The peak is at about 24.1%, with about 321 gold a day.

At 10%, `P_b = 52.63` and `Q = 47.37`. Tax per trade `0.1 × 52.63 = 5.26`. `b = 5.26 / 30 = 17.5%`. `Q_m = 47.37 × 0.825 = 39.06`. `R_m = 5.26 × 39.06 = 205.6`.

The peak comes from scanning `t` in steps of 0.0001: 24.1%, 321.2. It sits between the lecture's 17.3% at `E = 20` and 29.9% at `E = 40`, as it should. Harder bypass lets you tax more.
</details>

32. *Week 7 · design.* The monetary team needs 200 gold a day from this market, and you want to keep the rate at 10%. What maximum bypass cost `E` do you need? Name one rule that could raise `E` and the player group that pays for it.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `E` of about 26.6.

Without bypass, `R(0.10) = 249.3`. With bypass, `R_m = R × (1 − b)` and `b = 5.263 / E`. Solve `249.3 × (1 − 5.263/E) = 200`. Then `1 − 5.263/E = 0.8023`, so `E = 5.263 / 0.1977 = 26.6`.

Rules that raise `E`: a fee on mail that carries gold, binding some items on trade, or removing the trade window for high-value goods. Each one lands on players who trade face to face for good reasons, such as guild members supplying each other. Remember week 7's warning as well: trades pushed off the market lose escrow and carry scam risk.
</details>

33. *Week 7 · compute.* Demand for a potion is `Q = 120 − 2P` and supply is `Q = 4P − 60`. A per-unit tax of 6 is charged to sellers. Find the buyer price, the seller price, and each side's share of the tax. Which side can walk away more easily?

<details>
<summary>Answer and worked solution</summary>

**Answer:** buyers pay 34 and sellers keep 28. Buyers bear 4 (two thirds) and sellers bear 2 (one third).

Before the tax, `120 − 2P = 4P − 60` gives `P = 30`, `Q = 60`.

With the tax, `120 − 2P_b = 4(P_b − 6) − 60`, so `6P_b = 204` and `P_b = 34`. `P_s = 28`.

Buyer share `d / (b + d) = 4 / (2 + 4) = 2/3`. Supply is steeper in quantity per gold (4 against 2), so sellers respond more to price and can walk away more easily. The side that cannot walk away pays more, whoever hands over the tax.
</details>

34. *Week 7 · design.* Your market has listing spam. Players post items at silly prices and relist every hour. The current rule is a 6% sale tax and nothing else. Propose a fee schedule that targets the spam, and compute the minimum profitable spread for a flipper under a Guild Wars 2 style schedule (5% listing fee, 10% exchange fee on sale, no buy-side fee).

<details>
<summary>Answer and worked solution</summary>

**Answer:** move part of the charge from success to attempts. For example, a 2% listing fee that is kept whether or not the item sells, and a 4% sale tax. The GW2-style floor is about 17.6%.

A sale tax only charges trades that happen, so it does nothing to an order that never fills. A listing fee charges every attempt, so each hourly relist costs 2% of the listed value, and absurd prices become expensive to hold.

Flipper under 5% + 10%: they buy at `B` with no fee and sell at `A`, paying 15% of `A`. Break-even `A × 0.85 = B`, so `A / B = 1 / 0.85 = 1.176`, a minimum spread of 17.6%. High listing fees also squeeze merchants out, so choose the size from the spam you want to stop.
</details>

## Week 8: Player banks, loans and scams

35. *Week 8 · compute.* A banker earns a net spread `s = 1.2%` a week on lent money. Lending demand is `L = 80` billion, the weekly quit chance is `δ = 0.8%`, and the expected penalty for theft is `K = 10` billion. Compute the honesty ceiling. Deposits start at 25 billion and grow 8% a week. In which week does the bank pass the ceiling? What is the ceiling if the banker's quit chance rises to 1.5%?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `D* = 130` billion. Deposits pass it in week 22. At `δ = 1.5%`, `D*` drops to 50 billion.

`s ≥ δ` (1.2% against 0.8%), so the first branch applies. `D* = s × L / δ + K = 0.012 × 80 / 0.008 + 10 = 120 + 10 = 130`.

`25 × 1.08^w > 130` needs `w > ln(5.2) / ln(1.08) = 21.4`, so week 22.

At `δ = 1.5%` the spread is below the quit chance, so the second branch applies. Honest value grows as `(0.012 / 0.015) × D = 0.8 × D` and theft as `D − 10`. They meet at `D = K / (1 − s/δ) = 10 / 0.2 = 50`, which is below `L = 80`, so `D* = 50`. Deposits pass 50 billion in week 10 (`25 × 1.08^w > 50` needs `w > ln 2 / ln 1.08 = 9.0`; `25 × 1.08^9 = 49.97`). A tired banker meets the ceiling twelve weeks sooner. Students who apply the first-branch formula and get 74 have missed that `s < δ`.
</details>

36. *Week 8 · compute.* A second banker has `s = 1%`, `δ = 2%`, `L = 60` billion and `K = 15` billion, and holds 40 billion, all lent. Is honesty their best move? What is their ceiling?

<details>
<summary>Answer and worked solution</summary>

**Answer:** no. Stealing pays at 40 billion. The ceiling is 30 billion.

`V = s × D / δ = 0.01 × 40 / 0.02 = 20`. `S = D − K = 40 − 15 = 25`. Since `S > V`, theft pays.

Here `s < δ`, so the second branch applies. Honest value grows as `0.5 × D` while theft grows as `D − 15`. They meet at `D = K / (1 − s/δ) = 15 / 0.5 = 30`, which is below `L`, so `D* = 30`. Only the penalty keeps this banker honest, and only for small banks.
</details>

37. *Week 8 · compute.* A lender's safe alternative earns 0.8% a week. A borrower defaults 6% of the time. What is the break-even weekly loan rate with collateral that recovers half the loan? With no collateral?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 4.0% a week with collateral, 7.2% a week without.

`r = (1 + r_0 − p × c) / (1 − p) − 1`.

With `c = 0.5`: `(1.008 − 0.03) / 0.94 − 1 = 0.978 / 0.94 − 1 = 4.04%`.

With `c = 0`: `1.008 / 0.94 − 1 = 7.23%`.

At 7.2% a week, honest borrowers walk away and the ones who stay are more likely to default. That is adverse selection pushing `p` up, and it is why unsecured player lending stays tiny.
</details>

38. *Week 8 · design.* Using the numbers of question 37, your guild-bank feature must let lenders break even at no more than 3% a week. What collateral recovery `c` must the server guarantee?

<details>
<summary>Answer and worked solution</summary>

**Answer:** at least about 66% of the loan.

Solve `(1.008 − 0.06c) / 0.94 ≤ 1.03`. Then `1.008 − 0.06c ≤ 0.9682`, so `c ≥ 0.0398 / 0.06 = 0.663`.

In practice the server holds an item worth at least two thirds of the loan in a collateral slot. It releases the item to the borrower on repayment and to the lender on default. That turns a trust exchange into something close to an atomic one, which matters far more than the interest calculator.
</details>

39. *Week 8 · compute.* A scheme promises 2% a week, earns nothing and takes 20 units of new deposits every week. After 30 weeks, what does it hold, what does it owe, and what is its reserve ratio?

<details>
<summary>Answer and worked solution</summary>

**Answer:** it holds 600, owes about 811, and its reserve ratio is about 74%.

Cash is everything deposited: `20 × 30 = 600`.

Owed: `20 × (1.02^30 − 1) / 0.02 = 20 × 40.57 = 811.4`.

Reserve ratio `600 / 811.4 = 74%`. A scheme like this looks healthy for months. It pays small withdrawals easily and fails the day many depositors withdraw at once.
</details>

40. *Week 8 · critique.* A designer proposes a "loan board." Players post loan requests with an interest rate, other players fill them, and repayment is on trust. Classify the trust gap, predict what the board looks like after a month, and propose one fix.

<details>
<summary>Answer and worked solution</summary>

**Answer:** it is a time gap. One half of the exchange happens now and the other half depends on a person later.

With anonymous borrowers and no collateral, `p` is high. Break-even rates at a 10% default chance are above 12% a week (week 8 table). Honest borrowers refuse those rates. The ones who remain are more likely to default, so lenders raise rates further. Within a month the board is mostly scams and a few very expensive loans.

Fix: a server-held collateral slot, released automatically on repayment or to the lender on default. It closes the time gap by construction. Expect the scam to move to presentation, for example collateral items with names close to valuable ones. Pair the fix with a confirmation screen that states the item's market value.
</details>

## Week 9: Regional economies and logistics

41. *Week 9 · compute.* In the lecture's two-region model (`P_A = 60 − τ/2`, `P_B = 60 + τ/2`, `F = 20 − τ`), a route has hauler wage `w = 800` gold per hour, round trip `h = 0.75` hours, capacity `k = 150` units, a toll `f = 2` per unit and a loss chance `λ = 5%`. Compute `τ`, both prices, the flow, the gains from trade and the expected loss per unit.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `τ = 8.78`, `P_A = 55.61`, `P_B = 64.39`, `F = 11.22`, `G = 62.9`, expected loss 2.78 per unit.

Time and toll: `t0 = 800 × 0.75 / 150 + 2 = 4 + 2 = 6`.

`τ = (t0 + 60λ) / (1 + λ/2) = (6 + 3) / 1.025 = 8.78`.

`P_A = 60 − 4.39 = 55.61`. `P_B = 64.39`. `F = 20 − 8.78 = 11.22`. `G = 11.22² / 2 = 62.9`.

Check the loss term: `0.05 × 55.61 = 2.78`, and `6 + 2.78 = 8.78`. The price gap equals the transport cost exactly.
</details>

42. *Week 9 · design.* Your lead wants a price gap of 12 between hub and frontier on a safe route (`λ = 0`) with `w = 600` and a 1-hour round trip. What cargo capacity gives that gap with no toll? With a toll of 4?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 50 units with no toll, 75 units with a toll of 4.

With `λ = 0`, `τ = w × h / k + f`.

No toll: `600 / k = 12`, so `k = 50`.

Toll of 4: `600 / k = 8`, so `k = 75`.

Both routes give the same prices, the same flow (`20 − 12 = 8`) and the same gains from trade (32). Players feel them differently. The first means more trips. The second sends 4 gold per unit to whoever collects the toll, a sink if it goes to an NPC and a transfer if it goes to a player.
</details>

43. *Week 9 · critique.* Using the route from question 41, the monetization team proposes a "caravan teleport" that sets `h = 0` and `λ = 0` for players who own it. The toll of 2 still applies. Compute the new `τ`, prices, flow and gains, and critique the proposal.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `τ = 2`, `P_A = 59`, `P_B = 61`, `F = 18`, `G = 162`.

Only the toll remains, so the gap falls from 8.78 to 2. Gains from trade rise from 62.9 to 162, which frontier buyers will like.

The costs: hauling stops paying for anyone without the teleport, so the profession collapses. Frontier producers lose about 3.4 gold of price protection per unit. Places start to feel the same. The world's geography becomes a paid feature.

A restriction that keeps `τ` near its designed value: the teleport carries the player but not a full cargo hold, or it charges a per-unit fee that restores most of `τ`. Many games let players teleport without cargo for exactly this reason.
</details>

44. *Week 9 · explain.* Two trade hubs start with 60% and 40% of traders. Explain why the larger one tends to take over, and state the condition under which a second hub survives.

<details>
<summary>Answer and worked solution</summary>

**Answer:** a market is more useful the more people use it, so each new trader picks the busier hub and makes it busier still.

Expected sale time falls with the number of counterparties. A trader choosing where to list prefers the hub with more buyers, which is a positive feedback loop (agglomeration). In the lecture's example every newcomer joins the 60% hub, and after 1,000 newcomers it holds 80% of 2,000 traders.

A second hub survives when it is far enough away that the transport cost to reach the main hub is larger than the cost of slower sales at home. That is a rule you can compute with the `τ` formula, and a designer can use it to place hubs on purpose.
</details>

## Week 10: Scarcity by design, full loot and destruction

45. *Week 10 · compute.* An armor set class has `F = 400` sets built per day, a loss hazard `h = 0.025` per day and recovery `r = 0.2`. Players hold `A = 30` million gold in the class. Compute `δ`, the mean life, `S*`, `p*` and daily crafting revenue. What happens to each if crafters double production?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `δ = 0.02`, mean life 50 days, `S* = 20,000`, `p* = 1,500`, revenue 600,000 gold a day. Doubling output doubles the stock to 40,000, halves the price to 750, and leaves revenue at 600,000.

`δ = 0.025 × 0.8 = 0.02`. `S* = 400 / 0.02 = 20,000`. `p* = 30,000,000 / 20,000 = 1,500`. Revenue `1,500 × 400 = 600,000 = A × δ`.

At 800 a day: `S* = 40,000`, `p* = 750`, revenue `750 × 800 = 600,000`. Under unit-elastic demand, the crafting industry's income is set by how fast the world destroys the item, not by how much crafters build.
</details>

46. *Week 10 · compute.* The class in question 45 gains NPC insurance of 100 gold per lost set, and replacement purchases pay a 5% sales tax. At the steady state, how much gold does insurance create per day, how much does the tax remove, and what is the net?

<details>
<summary>Answer and worked solution</summary>

**Answer:** insurance creates 50,000 gold a day, the tax removes 30,000, and the net is a faucet of 20,000 a day.

Sets lost per day: `h × S* = 0.025 × 20,000 = 500`. Insurance `500 × 100 = 50,000`.

Tax: `τ × A × δ = 0.05 × 30,000,000 × 0.02 = 30,000`.

Net +20,000 gold a day. Losses destroy items but no gold, so this loss system inflates the currency while it deflates the item stock.
</details>

47. *Week 10 · compute.* A fleet of 500 ships dies. Each hull is worth 2,000,000 and carries fittings worth 1,500,000. Hulls are always destroyed. Fittings drop half the time (`r = 0.5`). Insurance pays 800,000 per hull from an NPC. Fill in the ledger: headline value destroyed, items removed from the world, items transferred to the winners, currency destroyed, currency created.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Ledger line | Amount |
|---|---|
| Headline "value destroyed" | 1.75 billion |
| Items removed from the world | 1.375 billion |
| Items transferred to the winners | 0.375 billion |
| Currency destroyed by the battle | 0 |
| Currency created by insurance | +0.4 billion |

Headline: `500 × (2.0M + 1.5M) = 1.75B`. Removed: hulls `1.0B` plus half the fittings `0.375B`. Transferred: the other half, `0.375B`. Insurance `500 × 800,000 = 0.4B`.

The headline counts the victims' ledger. The world lost 1.375 billion of goods and gained 0.4 billion of currency, so the battle pushed prices up from both sides.
</details>

48. *Week 10 · compute.* A player carries six items worth 12, 8, 5, 2, 1 and 1 million. How much is at risk under a keep-3 rule, a keep-4 rule and when skulled (keep 0)? With a 15% chance of dying on an outing, what is the expected loss per outing under keep-3 and when skulled?

<details>
<summary>Answer and worked solution</summary>

**Answer:** at risk 4 million (keep 3), 2 million (keep 4), 29 million (skulled). Expected loss 0.6 million per outing under keep-3 and 4.35 million when skulled.

Total value `12 + 8 + 5 + 2 + 1 + 1 = 29`. Keep-3 protects 25, so 4 is at risk. Keep-4 protects 27, so 2. Skulled protects nothing.

Expected loss: `0.15 × 4 = 0.6` and `0.15 × 29 = 4.35`.

The protection rule sets the risk budget almost on its own. Players will carry three valuable items and little else, which also keeps the most valuable items out of the item sink.
</details>

49. *Week 10 · critique.* Players hate losing gear in the open-PvP zone. A designer proposes: "Lower `r` from 0.5 to 0.2, so killers get less loot and victims feel less punished." Critique it with the ledger.

<details>
<summary>Answer and worked solution</summary>

**Answer:** lowering `r` changes what the killer gets, not what the victim loses. The victim loses their whole kit either way.

What the change does: `δ = h(1 − r)` rises from `0.5h` to `0.8h`, a 60% increase in item destruction. That shrinks the steady stock and raises prices and crafting revenue. It may be a good change for crafters. It will not reduce frustration, and killers get less reward for PvP.

To reduce the victim's pain, lower `h` (safer routes, consent), add insurance (a faucet, so size it), or protect items (keep-N rules). Name which of those the designer actually wants.
</details>

## Week 11: Premium currencies and exchange rates

50. *Week 11 · compute.* An MMO launches a token. Players who buy tokens with gold spend 48 billion gold a month on them, and 240,000 tokens a month are sold for gold. The token costs $15 in the store and redeems for a month of play. A typical farmer earns 10,000 gold an hour. Compute the token's gold price, gold per dollar, hours of farming per month of play, and the implied wage. What happens to the price if a store sale adds 80,000 tokens in one month?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 200,000 gold per token, about 13,333 gold per dollar, 20 hours per month, $0.75 an hour. The sale month drops the price to 150,000 gold.

`P = B / Q = 48,000,000,000 / 240,000 = 200,000`. `e = 200,000 / 15 = 13,333` gold per dollar. `H = 200,000 / 10,000 = 20` hours. `W = 15 / 20 = $0.75` an hour.

Sale month: `48B / 320,000 = 150,000`, a 25% drop, with `e = 10,000` gold per dollar. The business team's sale is also a monetary event.
</details>

51. *Week 11 · compute.* Over a quarter, the gold incomes of token buyers rise 10%, token supply falls 8%, and a new token use raises the share of income spent on tokens by 25%. By what factor does the token's gold price change? How much of that change would you call inflation?

<details>
<summary>Answer and worked solution</summary>

**Answer:** the price rises by a factor of about 1.495, a 49.5% rise. Only the 10% income rise is an inflation signal.

`P = s × Y / Q`, so the factor is `1.10 × 1.25 / 0.92 = 1.495`.

The income rise is money growth. The supply fall and the new use move the price without creating any gold. A team that reads the token price as an inflation gauge would report about five times the real signal. Track a basket of ordinary goods as well (weeks 1 and 13).
</details>

52. *Week 11 · compute.* A two-way gold and gem exchange charges 12% on each leg. What share of value does a round trip lose? Your economist wants a round trip to lose at least 25%. What fee per leg does that need?

<details>
<summary>Answer and worked solution</summary>

**Answer:** a round trip loses 22.6%. A 25% loss needs about 13.4% per leg.

`1 − 0.88² = 1 − 0.7744 = 0.2256`.

For 25%: `(1 − f)² = 0.75`, so `1 − f = 0.866` and `f = 13.4%`.

Pick the fee from the round-trip loss you want, since that is what damps the feedback loop from gold inflation to gem demand.
</details>

53. *Week 11 · explain.* Studio P sells gold directly at a fixed 100 gems per 10,000 gold. Studio T sells a token that players trade to each other for gold. Each studio sells $1 million of premium currency this month. Which one created gold, and who carries the monetary risk in each?

<details>
<summary>Answer and worked solution</summary>

**Answer:** studio P created gold. Studio T created none.

The peg is a faucet with a cash register. Every gem converted to gold creates gold from nothing. If the studio's other faucets inflate gold, the peg makes gold cheaper in real terms, players buy more, and inflation feeds on itself. The studio carries the monetary risk.

The token moves gold from the buyer to the seller. That is a transfer, so the money supply does not change. The floating price absorbs shocks, and players carry the rate risk as volatility. The only gold the token trade removes is whatever fee the market charges.
</details>

## Week 12: Economic shocks, exploits and rollbacks

54. *Week 12 · compute.* A server ledger shows these four days, in millions of gold. Compute each day's residual. When does a daily alert with a threshold of 1% of `M` fire, and how big is the shock?

| Day | `M` start | Faucets | Sinks | `M` end |
|---|---|---|---|---|
| 1 | 2,000 | 60 | 55 | 2,005 |
| 2 | 2,005 | 61 | 56 | 2,010 |
| 3 | 2,010 | 60 | 57 | 2,051 |
| 4 | 2,051 | 62 | 58 | 2,078 |

<details>
<summary>Answer and worked solution</summary>

**Answer:** residuals 0, 0, +38 and +23. The alert fires on day 3. The shock is 61 million, about 3.0% of `M`.

`residual = M_end − M_start − (faucets − sinks)`.

- Day 3: `2,051 − 2,010 − 3 = 38`.
- Day 4: `2,078 − 2,051 − 4 = 23`.

The threshold is about 20 million, so day 3 trips it. Money appeared with no recorded faucet. That points to an exploit or an unlogged faucet. Break the residual down by account next.
</details>

55. *Week 12 · compute.* A dupe creates 5% of a 2 billion money supply (`ΔM = 100` million). Exploiters pass on `q = 0.5` of what they still hold each day. Players average 1.5 hours a day and the team's `λ` is 30,000 player-hours per point of inflation. The dupe is found after 1 day. Compare clawback and rollback for a server with 40,000 players and one with 80,000.

<details>
<summary>Answer and worked solution</summary>

**Answer:** with 40,000 players, rollback wins (60,000 against 75,000 player-hours). With 80,000 players, clawback wins (75,000 against 120,000).

Leaked after 1 day: `100M × (1 − 0.5) = 50M`, so `L / M = 2.5%`. Clawback harm `30,000 × 2.5 = 75,000` on both servers.

Rollback harm `N × h × t`: `40,000 × 1.5 × 1 = 60,000` and `80,000 × 1.5 × 1 = 120,000`.

For the smaller server the crossover is at about 1.77 days. After that, clawback wins there too. A bigger player base makes rollbacks expensive sooner.
</details>

56. *Week 12 · explain.* In question 55, the 80,000-player server never has a delay at which rollback beats clawback. Derive the condition for a crossover to exist and check it for both servers.

<details>
<summary>Answer and worked solution</summary>

**Answer:** a crossover exists only if, at very small delays, clawback harm grows faster than rollback harm. That needs `λ × 100 × (ΔM/M) × (−ln(1 − q)) > N × h`.

Leakage `L(t) = ΔM(1 − (1 − q)^t)` rises fastest at `t = 0`, with slope `ΔM × (−ln(1 − q))` per day. So clawback harm starts rising at `λ × 100 × (ΔM/M) × (−ln(1 − q))` per day, then slows. Rollback harm rises at a constant `N × h` per day. If rollback is already steeper at the start, clawback stays below it forever.

Here the left side is `30,000 × 100 × 0.05 × 0.693 = 103,972` per day.

- 40,000 players: `N × h = 60,000`. The left side is bigger, so rollback is cheaper at first and a crossover exists.
- 80,000 players: `N × h = 120,000`. The left side is smaller, so clawback is cheaper at every delay.

This matches the lecture's small-`t` argument, which used `q` in place of `−ln(1 − q)`.
</details>

57. *Week 12 · compute.* After a clawback, 45 million gold of leaked currency remains. Daily sinks remove 50 million. By how much must you raise sinks to clear the leak in 9 days? The team also wants to give 80,000 players 2,000 gold each as compensation for a short trade freeze. Critique that plan.

<details>
<summary>Answer and worked solution</summary>

**Answer:** raise sinks by 5 million a day, a 10% increase. The compensation creates 160 million gold, more than three times the leak.

`45M / 9 = 5M` extra a day, `5 / 50 = 10%`. Choose a luxury or wealth-scaled sink, because leaked gold tends to sit with traders who sold to the exploiters.

Compensation: `80,000 × 2,000 = 160M`. That is a faucet 3.6 times the size of the leak you just spent nine days removing. Compensate in something that is not currency (an experience boost, a cosmetic), or price it against the shock.
</details>

## Week 13: Reading an economic report

58. *Week 13 · compute.* A monthly report shows `M` going from 2,000 to 2,060 (billions), faucets of 260 and sinks of 190. Trade value `T` fell from 9,000 to 8,700 and the volume index fell from 100 to 97. Reconcile the stock, then decompose the price change, exactly and by the growth form.

<details>
<summary>Answer and worked solution</summary>

**Answer:** residual −10, which is 14% of net flow. `gM = +3.0%`, `gV = −6.1%`, `gQ = −3.0%`, exact `gP = −0.34%`, approximate `gP = −0.15%`.

Stock: `2,000 + 260 − 190 = 2,070` predicted, 2,060 reported, so `R = −10`, and `−10 / 70 = −14%` of net flow.

`V` goes from `9,000 / 2,000 = 4.500` to `8,700 / 2,060 = 4.223`, a change of −6.15%. `P` goes from `9,000 / 100 = 90.0` to `8,700 / 97 = 89.69`, a change of −0.34%.

Growth form: `3.00 − 6.15 − (−3.00) = −0.15%`.

Reading: money grew 3%, but the average coin changed hands 6% less often, and fewer goods traded, which on its own pushes prices up. Prices ended flat. The residual share is above 10%. Churn under an active-money definition is the first thing to check.
</details>

59. *Week 13 · compute.* In an exploit month, money grows 50%, velocity falls 30% and volume rises 5%. Compare the growth-form estimate with the exact price change.

<details>
<summary>Answer and worked solution</summary>

**Answer:** the growth form says +15%. The exact answer is 0%.

Growth form: `50 − 30 − 5 = +15%`.

Exact: `1.50 × 0.70 / 1.05 = 1.00`, no change at all.

The additive form is fine for monthly moves of a few percent. For event months, use the exact ratio. Here the approximation invents a 15% inflation that did not happen.
</details>

60. *Week 13 · compute.* Using the Old School RuneScape Grand Exchange rule from the lecture (2% per item, capped at 5 million coins per item), a month's trades are 1,000 items at 1 million coins each and 10 items at 1 billion coins each. What is the tax collected and the effective rate? A colleague says the drop from 2% proves players are evading the tax. Respond.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 70 million coins of tax on 11 billion of trade, an effective rate of about 0.64%.

Cheap items: `1,000 × 0.02 × 1,000,000 = 20M`. Expensive items: 2% of 1 billion would be 20 million, above the cap, so each pays 5 million, `10 × 5M = 50M`. Total 70 million. Value `1B + 10B = 11B`. Rate `70 / 11,000 = 0.64%`.

No evasion is needed to explain it. The cap makes the tax flat above 250 million coins per item, so the effective rate falls whenever the mix shifts toward expensive items. Check the trade mix before blaming evasion.
</details>

61. *Weeks 2 and 13 · explain.* In question 58's game, active players rose from 80,000 to 92,000. Compute money per active player in both months. If wealth follows the random-exchange baseline, what does the median player hold in the second month? Why does that matter for a flat sink?

<details>
<summary>Answer and worked solution</summary>

**Answer:** money per player fell from 25.0 million to about 22.4 million, down 10.4%. Under the exponential baseline, the median player holds about 15.5 million.

`2,000B / 80,000 = 25.0M`. `2,060B / 92,000 = 22.4M`.

Median `= mean × ln 2 = 22.4 × 0.693 = 15.5M`. Real game wealth is usually more skewed than the baseline, so the true median is probably lower still.

A flat sink sized to matter to the mean player takes a larger share from the median player, and much more from new players, who hold the least. Ask for balance percentiles before you size it.
</details>

## Week 14: Intervention design

62. *Week 14 · compute.* A game has net faucet `F = 8` per day and base velocity `v_0 = 0.12` per day. The tax rises from 2.5% to 4%, and players respond with elasticity `ε = 0.3`. Compute the old equilibrium, the new velocity, the new `M*`, the half-life, and the equilibrium price and volume factors. What does nominal trade settle at?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `M_0 = 2,667`, `v = 0.1042`, `M* = 1,919`, half-life about 166 days, price factor 0.720, volume factor 0.868. Nominal trade settles at 200 per day.

`M_0 = 8 / (0.025 × 0.12) = 2,667`.

`v = 0.12 × (0.04/0.025)^(−0.3) = 0.12 × 1.6^(−0.3) = 0.1042`. `r = 0.04 × 0.1042 = 0.004169`. `M* = 8 / 0.004169 = 1,919`. Half-life `0.693 / 0.004169 = 166` days.

Price factor `(0.025/0.04)^0.7 = 0.720`. Volume factor `(0.025/0.04)^0.3 = 0.868`. Their product is `0.625 = τ_0 / τ`.

Nominal trade `v × M* = F / τ = 8 / 0.04 = 200`.
</details>

63. *Week 14 · compute.* Use the game from question 62. Predict the money stock on day 30 for `ε = 0` and for `ε = 0.3`, and the tax sink on day 0 in each case. Write one kill criterion that tells the two worlds apart.

<details>
<summary>Answer and worked solution</summary>

**Answer:** day 30 money stock about 2,532 (`ε = 0`) and about 2,579 (`ε = 0.3`). Day-0 sink 12.8 and 11.1, against a faucet of 8.

Iterate `M_{t+1} = M_t + 8 − r M_t` from 2,667 for 30 days. With `ε = 0`, `r = 0.04 × 0.12 = 0.0048` gives 2,532. With `ε = 0.3`, `r = 0.004169` gives 2,579.

Sink on day 0: `0.0048 × 2,667 = 12.8` and `0.004169 × 2,667 = 11.1`.

The money paths differ by less than 2% at day 30, so money alone cannot tell the worlds apart early. The volume index can, because it steps down on day 0 (to 0.868 when `ε = 0.3`). By day 90 the predicted price index is 0.868 for `ε = 0` and 0.912 for `ε = 0.3`. Kill criterion: "If the volume index is below 0.85 at day 30 and the price index is above 0.95 at day 90, `ε` is well above 0.3 and the tax is mostly friction. Revert to 3% and reassess."
</details>

64. *Week 14 · design.* You want the long-run money stock 30% lower. By what factor must the tax rise if `ε = 0`? If `ε = 0.4`? Starting from a 2.5% tax, what rates are those?

<details>
<summary>Answer and worked solution</summary>

**Answer:** a factor of 1.43 (to about 3.57%) if `ε = 0`, and 1.81 (to about 4.53%) if `ε = 0.4`.

The price factor is `(τ_0 / τ)^(1 − ε) = 0.7`.

`ε = 0`: `τ / τ_0 = 1 / 0.7 = 1.43`, so 3.57%.

`ε = 0.4`: `τ / τ_0 = 0.7^(−1/0.6) = 1.81`, so 4.53%. Volume then falls to `(1/1.81)^0.4 = 0.79` of its old level.

The same target needs a much bigger lever when players respond, and it costs about a fifth of market volume. This is why the spec must forecast under at least two values of `ε`.
</details>

65. *Week 14 · critique.* A producer proposes testing the tax rise by charging 7.5% to a random half of players and 4% to the other half for a month. Critique the test and propose one that works.

<details>
<summary>Answer and worked solution</summary>

**Answer:** the groups trade with each other, so the test measures the escape route, not the tax.

A 7.5% seller lists nothing and sells through a 4% friend, or buys from 4% sellers. The treated group's volume falls because trade moves, not because trade disappears. Statisticians call this interference between units. The estimated `ε` comes out far too high.

Workable designs:

- Split by market, for example one region's book against the others. Trade will shift toward the untaxed regions, so treat the estimate as an upper bound.
- Step the rate in stages (4% to 5% to 6.5% to 7.5%) and estimate `ε` from each step's volume response.
- Simulate first in the agent-based model, with agents who can choose to hold, trade or use escape routes.
</details>

66. *Week 14 · explain.* Two weeks after a tax rise, a designer says: "Sink revenue is up 70%, so the tax is working. Let's announce success." Explain why sink revenue is the wrong metric.

<details>
<summary>Answer and worked solution</summary>

**Answer:** at the new equilibrium a proportional sink collects exactly the net faucet, whatever the rate. Revenue jumps on day one and then drifts back down to `F`.

`S_t = τ × v × M_t`. When the rate rises, `S` jumps because `M` has not moved yet. As `M` falls toward `M* = F / (τ v)`, `S` falls toward `F`. After a few half-lives, revenue is back where it started even if the intervention worked perfectly. It also comes back to `F` if `ε = 1` and the tax did nothing but add friction.

Judge the change on the price index and the volume index against the pre-registered path at 30, 90 and 180 days.
</details>

## Across weeks

67. *Weeks 4 and 7 · compute.* Use the week 7 market with bypass cost `E = 20`. The tax rises from 5% to 10%. Trade volume on the market is the week 4 velocity. By what factor does the sink rate `σ = τ × v` rise, and how far does the money ceiling `m*` fall? Compare with the naive answer.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `σ` rises by a factor of about 1.64, so `m*` falls to about 61% of its old value, not to 50%.

Market volume `Q_m = Q × (1 − b)`:

- At 5%: `Q = 48.72`, `b = 2.56 / 20 = 12.8%`, `Q_m = 42.47`.
- At 10%: `Q = 47.37`, `b = 26.3%`, `Q_m = 34.90`.

`σ` scales with `τ × Q_m`: `(0.10 × 34.90) / (0.05 × 42.47) = 1.64`. Since `m* = g / σ`, the ceiling falls to `1 / 1.64 = 0.61` of its old value.

The naive reading doubles `σ` and halves `m*`. Players trading around the market take back more than a third of the intended effect. That is week 4's warning that `v` responds to `τ`, measured with week 7's model.
</details>

68. *Weeks 8, 10, 11 and 12 · explain.* For each event, say which ledger it touches (currency or items), whether it is a faucet, a sink or a transfer, and for which currency. (a) An NPC insurance payout for a destroyed hull. (b) A player buys a subscription token from another player for gold. (c) That token is redeemed for game time. (d) A duplication bug copies 1 million gold. (e) A player bank's founder walks off with deposits. (f) A fee on a two-way gem exchange.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Event | Ledger | Kind |
|---|---|---|
| (a) Insurance payout | Currency | Faucet (gold created by an NPC) |
| (b) Token bought for gold | Currency and premium | Transfer of gold between players, transfer of the token |
| (c) Token redeemed | Premium | Sink of the premium currency, no gold effect |
| (d) Duplicated gold | Currency | Unintended faucet, visible only as a ledger residual |
| (e) Bank theft | Currency | Transfer (the money supply is unchanged; ownership moves) |
| (f) Exchange fee | Currency or premium | Sink on whichever leg the fee is charged |

The pattern to notice: many dramatic events, such as the bank theft or the token trade, do not change the money supply at all. The quiet ones, the insurance payout and the dupe, do.
</details>

69. *Weeks 1, 13 and 14 · critique.* Critique this intervention memo line by line: "Money supply rose 4% last month, so we have 4% inflation. We will double the auction cut from 3% to 6%. We expect the money supply to shrink by 4% a month from next month. We will check the sink revenue in two weeks."

<details>
<summary>Answer and worked solution</summary>

**Answer:** every line has a model error.

- **"Money up 4% means 4% inflation."** Only if velocity and volume held still (week 13). Decompose `gP = gM + gV − gQ` first, and name the basket (week 1).
- **"Double the cut."** No alternatives, no incidence line, no reason this lever beats a faucet cut (week 14 spec, sections 3 and 5).
- **"Shrink by 4% a month."** A proportional sink moves the stock to a new level `F / (τ v)` along a half-life. It does not drain at a fixed rate. And `v` may fall when the cut rises (weeks 7 and 14).
- **"Check sink revenue in two weeks."** Revenue jumps on day one and returns to `F`, so it says nothing about success. Two weeks is a small fraction of a half-life measured in months.

A fixed version: diagnosis from the identities, a target metric and date, the lever with rejected alternatives, a forecast at 30, 90 and 180 days under two elasticities, an incidence table, and numeric kill criteria on the price and volume indices.
</details>

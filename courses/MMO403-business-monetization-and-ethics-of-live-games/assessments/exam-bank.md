# MMO403 · Exam bank: quiz, practice and viva questions

MMO403 has no written exam. The grade comes from the models strand (40%, see [models-brief.md](models-brief.md)), the ethics analysis (20%, see [ethics-analysis-brief.md](ethics-analysis-brief.md)) and the business plan (40%, see [business-plan-brief.md](business-plan-brief.md)). This bank has three other jobs.

- **Practice.** Work a week's questions before its lab is due. If you can answer them with the lecture closed, the lab will go quickly.
- **Lab quizzes.** Each lab session opens with a 10-minute ungraded quiz of two or three questions from this bank, usually one compute question and one explain or critique question.
- **Checks and viva.** The models strand adds two questions from this bank to each model set, issued with new numbers. The week 15 business plan viva asks questions in this style, rewritten with your own plan's numbers.

Every question is tagged with the week it draws on and one type.

- **compute**: apply a lecture model (contribution, LTV curve, cheapest cover, paid edge, pass finish line, set completion, rule table, friction for sale, Lorenz and cap, price test, token revenue, store take, burn and runway, stage gate) to values you have not seen.
- **code**: predict what a piece of Python prints, or find the bug in it.
- **explain**: say why something behaves as it does, with a number as evidence.
- **design**: choose a setting or a rule for a stated situation and justify it.
- **critique**: find what is wrong with a claim, a plan or a readout, and fix it.
- **ethics** and **regulation**: weigh a monetization choice or state where the law stands. Model answers give both sides and use the lectures' dated status (28 September 2026). Rules change, so a viva answer that cites a later, sourced change is also correct.

All numbers are invented unless a question names a game. Every real-game fact comes from the lecture of the tagged week, which cites its source and era. Every code snippet runs as shown with `.venv/bin/python`, and every number was recomputed in Python from the lectures' own models. Write your answer before you open the solution.

Week 15 has no lecture. Its viva draws on all fourteen weeks.

---

## Week 1: Business models

Lecture: [w01](../lectures/w01-business-models-box-subscription-f2p-hybrid.md). Unless a question says otherwise, use the lecture's four rows (box 0.20 / $60 / $0, subscription 0.10 / $40 / $15, free-to-play 1.00 / $0 / $2.00, hybrid 0.25 / $30 / $3.50), an audience of 1,000,000 and `c = $0.50`.

1. *Week 1 · compute.* Monthly retention is 0.75. Compute `S(24)` and the 24-month contribution of each of the four models. Which model ranks first, and why does the subscription come third?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `S(24) = 3.996`. Box $11.60M, hybrid $10.50M, subscription $9.79M, free-to-play $5.99M. The box ranks first.

`S(24) = (1 − 0.75^24) / 0.25 = 3.996`, close to the long-run lifetime of 4 months.

- Box: `200,000 × (60 − 0.5 × 3.996) = $11.60M`.
- Subscription: `100,000 × (40 + 14.5 × 3.996) = $9.79M`.
- Free-to-play: `1,000,000 × 1.5 × 3.996 = $5.99M`.
- Hybrid: `250,000 × (30 + 3.0 × 3.996) = $10.50M`.

The subscription needs more than 5.16 active months to beat the box. At `r = 0.75` a player's expected lifetime is only 4 months, so the subscription cannot catch up however long you wait.
</details>

2. *Week 1 · compute.* Derive the break-even `S*` at which the hybrid's contribution equals the box's. What long-run monthly retention does that require? At `r = 0.85`, in which month does the hybrid's cumulative contribution first pass the box's?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `S* = 5.29` active months, which needs `r > 0.811` in the long run. At `r = 0.85` the hybrid passes the box in month 10.

Set `0.25 × (30 + 3.0 S) = 0.20 × (60 − 0.5 S)`. That is `7.5 + 0.75 S = 12 − 0.1 S`, so `0.85 S = 4.5` and `S* = 5.294`. Since `S` approaches `1 / (1 − r)`, the hybrid can only win if `1 / (1 − r) > 5.294`, that is `r > 0.811`. At `r = 0.85`, `S(T)` first exceeds 5.294 at `T = 10` (`S(9) = 5.12`, `S(10) = 5.35`).
</details>

3. *Week 1 · compute.* Estimate the value of one extra point of monthly retention (from 0.85 to 0.86) for the hybrid, first with the long-run derivative and then exactly over 36 months. Why is the exact figure larger?

<details>
<summary>Answer and worked solution</summary>

**Answer:** About $333,000 from the derivative; $348,000 exactly over 36 months.

The long-run approximation is `A × d × (m − c) × 0.01 / (1 − r)² = 1,000,000 × 0.25 × 3.0 × 0.01 / 0.0225 = $333,333`. The exact value is the 36-month contribution at 0.86 minus the one at 0.85, `$12.834M − $12.486M = $348,000`. The exact figure is larger because the step from 0.85 to 0.86 is not infinitesimal, and `1 / (1 − r)` is convex, so the gain grows as `r` rises. The lecture's own r = 0.80 example shows the same gap ($375,000 by the derivative, $393,000 exact for free-to-play).
</details>

4. *Week 1 · explain.* A cloud price rise lifts the cost to serve `c` from $0.50 to $2.00 per active month. For each model, say what happens to the value of one extra retained month, and say which team at a free-to-play studio would now struggle to get budget.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The margin per retained month `m − c` falls by $1.50 for every model. Free-to-play goes to exactly zero, so retention earns it nothing.

- Box: `m − c` falls from −$0.50 to −$2.00. Each retained month now costs four times as much.
- Subscription: from $14.50 to $13.00. Still strongly positive, so retention stays valuable.
- Free-to-play: from $1.50 to $0.00. With `U = 0`, every month's contribution is zero, and the value of one point of retention is zero.
- Hybrid: from $3.00 to $1.50. Retention is worth half what it was.

The retention and live-ops team at the free-to-play studio loses its budget argument, since section 3 of the lecture values its work at `A × d × (m − c) × ...`, and `m − c` is now zero. The fix is on the cost side or the meter, not the team.
</details>

## Week 2: Unit economics

Lecture: [w02](../lectures/w02-unit-economics-ltv-cac-arppu.md).

5. *Week 2 · compute.* A cohort has `w = 0.30`, `qs = 0.97`, `qt = 0.45`, gross ARPDAU $0.15 and a 30% platform fee. Compute `R(1)`, the expected active days `L`, lifetime net LTV, and the share of LTV that comes from stayers.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `R(1) = 0.606`, `L = 11.27` days, lifetime net LTV $1.184, stayers 88.7%.

`R(1) = 0.30 × 0.97 + 0.70 × 0.45 = 0.291 + 0.315 = 0.606`. `L = 0.30 / 0.03 + 0.70 / 0.55 = 10 + 1.273 = 11.27`. Net ARPDAU is `0.15 × 0.70 = $0.105`, so lifetime LTV is `11.27 × 0.105 = $1.184`. Stayers give 10 of the 11.27 active days, 88.7%.
</details>

6. *Week 2 · code.* This is the lecture's LTV code with question 5's cohort. Predict the four lines it prints before you run it.

```python
w, qs, qt = 0.30, 0.97, 0.45      # stayer share, stayer and tourist daily survival
arpdau, fee = 0.15, 0.30          # gross revenue per DAU; platform fee
net = arpdau * (1 - fee)

def R(d):
    return w * qs**d + (1 - w) * qt**d

def ltv(T):                        # net revenue per install over days 0 .. T-1
    return net * sum(R(d) for d in range(T))

def payback_day(cac, horizon=3650):
    return next((d for d in range(horizon) if ltv(d + 1) >= cac), None)

lifetime = net * (w / (1 - qs) + (1 - w) / (1 - qt))
print(f"LTV d30 {ltv(31):.3f}  d90 {ltv(91):.3f}  lifetime {lifetime:.3f}")
for cac in (0.50, 1.00, 1.50):
    print(f"CAC {cac:.2f}: payback day {payback_day(cac)}")
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
LTV d30 0.775  d90 1.118  lifetime 1.184
CAC 0.50: payback day 14
CAC 1.00: payback day 57
CAC 1.50: payback day None
```

A CAC of $1.50 is above the lifetime LTV of $1.184, so the curve never reaches it. At $1.00 the LTV/CAC ratio is only 1.18, so payback comes late, on day 57, because the last 15% of value sits in a slow stayer tail.
</details>

7. *Week 2 · compute.* A game installs 12,000 players a day at steady state. Its net lifetime LTV per install is the lecture's $1.925. What is its daily net revenue at the plateau? Its gross ARPDAU is $0.20 with a 2.5% daily payer rate. What is its daily ARPPU?

<details>
<summary>Answer and worked solution</summary>

**Answer:** $23,100 a day; ARPPU $8.00.

By the plateau identity, daily revenue at steady state equals daily installs times lifetime LTV: `12,000 × 1.925 = $23,100` net a day. From `ARPDAU = payer rate × ARPPU`, `ARPPU = 0.20 / 0.025 = $8.00` gross per paying user per day.
</details>

8. *Week 2 · critique.* A marketing slide reads: "LTV $4.00. Blended CAC $2.50. LTV/CAC 1.6. Recommendation: double paid spend." List what is missing or misleading, and rewrite the claim so that a finance lead could act on it.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The LTV has no fee basis, horizon, cohort or measured-versus-predicted label, and the CAC is blended.

- Gross or net of the platform fee? A 30% fee alone separates the two by a factor of 1.43.
- Which horizon? Day 30 and lifetime can differ by a factor of two, as in the lecture's example ($0.99 against $1.93).
- Which cohort? An average over organic and paid players overstates the paid ones.
- Measured or predicted? How many days of data sit behind $4.00?
- Blended CAC includes free organic installs, so it understates what the next paid install costs. Doubling paid spend needs paid CAC per channel.
- A ratio of 1.6 leaves little room for development, overheads and forecast error, even if both numbers were right.

A usable version: "Net LTV at day 180 for paid video-ad installs in North America, March to May cohorts, measured: $3.10; predicted lifetime $4.00. Paid CAC for that channel $2.80; payback on day 150."
</details>

## Week 3: Premium currencies

Lecture: [w03](../lectures/w03-premium-currencies.md). The Emberfall store sells 1,000 coins for $9.99, 2,800 for $24.99, 5,000 for $39.99 and 13,500 for $99.99.

9. *Week 3 · compute.* From a zero balance, find the cheapest cash outlay, the leftover, the reference price and the markup for an Emberfall item priced at 2,300 coins, and for one priced at 3,500 coins.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 2,300 coins: one medium pack, $24.99, leftover 500, reference $22.98, markup 1.09. 3,500 coins: one small plus one medium, $34.98, leftover 300, reference $34.97, markup 1.00.

For 2,300: three small packs give 3,000 for $29.97, one medium gives 2,800 for $24.99, so the medium wins. Reference `2,300 × 9.99 / 1,000 = $22.977`, rounded half up to $22.98. Markup `24.99 / 22.98 = 1.09`.

For 3,500: one large gives 5,000 for $39.99; one small plus one medium gives 3,800 for $34.98; four smalls give 4,000 for $39.96. The mix wins. Reference `3,500 × 9.99 / 1,000 = $34.965`, rounded half up to $34.97. Markup `34.98 / 34.97 ≈ 1.00`. A mixed purchase can land almost exactly on the reference price, which a player choosing one big pack by instinct would miss.
</details>

10. *Week 3 · compute.* Fortnite's V-Bucks packs from 19 March 2026 are 800 for $8.99, 2,400 for $22.99, 4,500 for $36.99 and 12,500 for $89.99. What does a hypothetical 1,500 V-Buck item cost from zero, with what leftover, and what is its markup at the smallest pack's rate?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Two 800 packs for $17.98, leftover 100, reference $16.86, markup 1.07.

Two small packs give 1,600 for $17.98. One 2,400 pack costs $22.99. The reference price is `1,500 × 8.99 / 800 = $16.856`, which rounds to $16.86, so the markup is `17.98 / 16.86 = 1.07`. Compare the lecture's 1,200 V-Buck example, which costs the same $17.98 but leaves 400. Leftover depends on where the price sits relative to multiples of the 800 step.
</details>

11. *Week 3 · compute.* Guild Wars 2 sells gems at a flat 80 per dollar in packs of 400, 800, 1,600, 2,800, 4,000 and 8,000 (September 2026). An item costs 1,000 gems. What is the cheapest purchase from zero, the leftover and the markup? Explain why a flat rate did not remove the leftover.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 400 plus 800 gems for $15.00, leftover 200, markup 1.20.

Reference `1,000 / 80 = $12.50`. Nothing smaller than 1,200 gems covers 1,000, so the player pays $15.00 and keeps 200. Markup `15.00 / 12.50 = 1.20`. A flat rate means no bulk discount, so every gem costs the same. Leftovers come from step size, and the smallest step is 400 gems. Any item price that is not a multiple of 400 leaves a remainder. GW2's gold-to-gem exchange softens this, since a player can top up with gold.
</details>

12. *Week 3 · compute.* A new Emberfall player buys three items in order, 800, then 1,200, then 1,500 coins, each time taking the cheapest cover for the shortfall. Give the cash paid at each step, the final balance and the total. How much would the same three items cost if each were bought from a zero balance, discarding leftovers?

<details>
<summary>Answer and worked solution</summary>

**Answer:** $9.99 (balance 200), $9.99 (balance 0), $19.98 (balance 500). Total $39.96 with 500 coins left. From zero each time: $49.95.

For 1,200 with 200 held, the player needs 1,000 more, which is one small pack, and ends at 0. For 1,500 from 0, two small packs, ending at 500. Bought separately from zero, the three cost `9.99 + 19.98 + 19.98 = $49.95`. The leftover is prepayment: across a sequence the average cost per coin approaches the pack rate, and whatever remains when the player quits is breakage.
</details>

13. *Week 3 · regulation.* A producer says: "The EU's 2025 principles on in-game currencies are just guidance, so we can ignore them." How much force do they have, which of them does a store with a 1,000-coin minimum pack and items at 1,200 coins touch, and what would you change?

<details>
<summary>Answer and worked solution</summary>

**Answer:** They are not binding in themselves, but they state how the enforcers read EU consumer law, which does bind. The store touches principles 1 and 3, and probably 2 if more than one currency is involved.

The CPC Network published the key principles on 21 March 2025. The document says it is non-exhaustive and binds neither national authorities nor the Commission. It sets out how authorities read the Unfair Commercial Practices Directive, the Consumer Rights Directive and the Unfair Contract Terms Directive, which do bind. The same Commission page records a coordinated action against Star Stable Online that included unclear currency information, so the reading is being applied.

For this store, principle 1 asks for the real-money price of every item, without quantity discounts. Principle 3 asks studios not to force players to buy currency they do not need, naming bundles that mismatch item prices. A 1,200-coin item behind a 1,000-coin step forces an 800-coin leftover. Fixes: show "≈ $11.99" beside the coin price, and either price items on multiples of the smallest pack or add a smaller pack.

The other side: currencies unify prices across markets, let players earn store credit and allow bulk pricing. The principles do not ban currencies. They ask that the real price be visible and that players can buy what they need.
</details>

## Week 4: Cosmetics vs power

Lecture: [w04](../lectures/w04-cosmetics-vs-power.md). Use `Φ` for the standard normal CDF and the lecture's ladder model (skill spread `s = 200`).

14. *Week 4 · compute.* In a game with fight noise `σ = 0.20`, a store item gives +6% damage. Compute the `z` value, the duel win chance against an equal player and the rating value `Δ`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `z = 0.206`, win chance 58.2%, `Δ ≈ 57` rating points.

`ln(1.06) = 0.0583`. `σ√2 = 0.283`. `z = 0.0583 / 0.283 = 0.206`. `Φ(0.206) = 0.582`. `Δ = 400 × log10(0.582 / 0.418) = 400 × 0.143 = 57.2`.
</details>

15. *Week 4 · compute.* The item in question 14 is owned by 25% of players. In an unranked mode with random opponents, what are owners' and non-owners' win rates? What would they be in a ranked mode with matchmaking, once ratings settle?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Unranked: owners 56.1%, non-owners 48.0%. Ranked: both 50%.

Owners meet owners 25% of the time and non-owners 75%: `0.25 × 0.5 + 0.75 × 0.582 = 0.561`. Non-owners meet non-owners 75% and owners 25%: `0.75 × 0.5 + 0.25 × 0.418 = 0.480`. Under matchmaking, owners' ratings rise by `Δ` until they meet opponents that much stronger, and their win rate returns to 50%. The edge moves from win rates into rank.
</details>

16. *Week 4 · compute.* Your studio's policy says no purchasable item may be worth more than 10 rating points in ranked play. What is the largest damage edge you may sell if fight noise is `σ = 0.25`? If `σ = 0.10`? (`Φ⁻¹(0.5144) = 0.0361`.)

<details>
<summary>Answer and worked solution</summary>

**Answer:** About +1.3% at `σ = 0.25`, about +0.5% at `σ = 0.10`.

Invert the chain. `Δ = 10` means `p / (1 − p) = 10^(10/400) = 1.0593`, so `p = 0.5144`. Then `z = 0.0361`, and `ln(1 + b) = z × σ√2`. At `σ = 0.25`, `ln(1 + b) = 0.0361 × 0.354 = 0.01276`, so `b = 1.28%`. At `σ = 0.10`, `ln(1 + b) = 0.0361 × 0.141 = 0.0051`, so `b = 0.51%`. A policy written in rating points gives a much stricter percentage limit in a precise, skill-heavy game.
</details>

17. *Week 4 · critique.* A producer reports: "Only 10% of our ranked players own the +X% item, it is worth about 50 rating points, and owners win 50.3% of matches. The item is fair." Using the ladder model (`f = 0.10`, `Δ = 50`), say what owners' share of the top 10% and top 1% will be, and rewrite the producer's conclusion.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Owners hold about 14.5% of the top 10% and 17.5% of the top 1%, against 10% of the population.

Solve for the cut-off `t` where `0.9 × (1 − Φ(t/200)) + 0.1 × (1 − Φ((t − 50)/200)) = 0.10`, then take `0.1 × (1 − Φ((t − 50)/200)) / 0.10`. The lecture's `payer_share_on_top(50, 0.1)` returns 0.145, and with `top=0.01` returns 0.175. The 50.3% win rate is what matchmaking always produces. A better conclusion: "Owners are over-represented at the top of the ladder by about 45% in the top 10% and 75% in the top 1%. The item buys rank. We will track owner share of the top 1% each season and remove the item from ranked play if it stays above 15%."
</details>

## Week 5: Battle passes

Lecture: [w05](../lectures/w05-battle-passes.md). Owners' play time is lognormal with median `m` and spread `s`, so `P(H ≥ h) = 1 − Φ(ln(h/m) / s)`.

18. *Week 5 · compute.* A pass needs `H* = 45` hours. Owners play a median of 35 hours with `s = 0.6`. What share finish?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 33.8%.

`ln(45/35) = 0.2513`, and `0.2513 / 0.6 = 0.419`. `Φ(0.419) = 0.662`, so `1 − 0.662 = 0.338` of owners finish.
</details>

19. *Week 5 · compute.* With the lecture's owners (`m = 40`, `s = 0.7`), what `H*` gives a 60% finish share? (`Φ(−0.253) = 0.40`.) An owner plays 25 hours in a season with `H* = 40` and 100 tiers. Which tier do they reach?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `H* ≈ 33.5` hours. The 25-hour owner reaches tier 62.

A 60% finish share needs `P(H ≥ H*) = 0.6`, so `ln(H*/40) / 0.7 = −0.253`, `H* = 40 × e^(−0.177) = 40 × 0.838 = 33.5`. For the owner, `T = floor(100 × 25 / 40) = floor(62.5) = 62`.
</details>

20. *Week 5 · compute.* A pass costs 800 coins and returns a 1,000-coin rebate. With the lecture's owners and `H* = 50` (finish share 37.5%, mean tier 73.1), what does the average owner get back if the rebate is spread evenly? If it all sits on the final tier? Which placement makes the pass "pay for itself" for more owners?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Evenly: 731 coins on average. Final tier: 375 coins on average. Neither returns the 800-coin price to the average owner. Spread evenly, an owner breaks even at tier 80 instead of tier 100.

Evenly: `1,000 × 73.1 / 100 = 731`. Final tier: `1,000 × 0.375 = 375`. With an even spread, an owner has received 800 coins at tier 80, which needs `0.8 × 50 = 40` hours, the median, so about half of owners get their price back. With all the rebate at tier 100, only the 37.5% who finish get anything, and they get 200 coins more than the price. The even spread makes the pass pay for itself for more owners; the final-tier placement rewards play time and gives the median owner a reason to buy tiers.
</details>

21. *Week 5 · design.* Your producer asks you to set the lecture's pass at its tier-revenue peak (43 hours, 45.9% finish, 15,086 coins per 1,000 owners). You prefer `H* = 30` (65.9% finish, 13,259 coins). Write the trade-off in numbers and a recommendation.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `H* = 30` gives up about 1,827 coins of tier sales per 1,000 owners, 12.1% of the peak, and lets 20 more owners in 100 finish by playing.

`15,086 − 13,259 = 1,827`, and `1,827 / 15,086 = 12.1%`. Finish share rises from 45.9% to 65.9%. Tier sales are a small part of pass revenue next to the pass price, and the peak setting leaves more than half of paying owners short of the list they bought. A defensible recommendation is `H* = 30`, published to players, with catch-up XP in the final weeks. The case for the peak is revenue. The case against is trust among the players who play most, which the lecture's rebate section shows are the ones who renew. Either answer is acceptable if the numbers and the trade-off are stated.
</details>

## Week 6: Loot boxes and probability disclosure

Lecture: [w06](../lectures/w06-loot-boxes-and-probability-disclosure.md).

22. *Week 6 · compute.* A set has 8 items, each at 12.5% per box. Compute the expected boxes to complete it, the expected boxes to collect the first 4 items, and the expected boxes for the last item alone.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 21.74 boxes in all; 5.08 for the first half; 8 for the last item.

`H_8 = 2.718`, so `E[T] = 8 × 2.718 = 21.74`. The first 4 items take `8 × (1/8 + 1/7 + 1/6 + 1/5) = 8 × 0.6345 = 5.08` boxes. The last item has a 1-in-8 chance per box, so it takes 8 boxes on average. Half the set costs under a quarter of the whole.
</details>

23. *Week 6 · compute.* The in-class mount set has 8 Commons at 9%, 3 Rares at 8% and 1 Mythic at 4%. Using the lecture's inclusion-exclusion code, what are the mean, median and 90th-percentile boxes to complete the set? What are the median and 90th percentile for the Mythic alone? A box costs 150 gems and the common bundle sells 1,000 gems for $9.99. Convert the set's 90th percentile to dollars.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Set: mean 41.91, median 37, 90th percentile 65 boxes. Mythic alone: median 17, 90th percentile 57. The set's 90th percentile costs $97.40.

The odds sum to `0.72 + 0.24 + 0.04 = 1`. Set `SET = [(8, 0.09), (3, 0.08), (1, 0.04)]` in the lecture code. For the Mythic alone, the median is the smallest `n` with `1 − 0.96^n ≥ 0.5`, which is 17, and the 90th percentile needs `0.96^n ≤ 0.1`, which is 57. One box costs `150 × 9.99 / 1,000 = $1.4985`, so 65 boxes cost $97.40. Here the set's tail (65) is longer than the Mythic's (57), unlike the lecture's 15/4/1 set, because the Commons and Rares at 8 to 9% are slow enough to matter too.
</details>

24. *Week 6 · compute.* A 3% Legendary gets a hard pity at 30 boxes. What is the chance a buyer reaches the pity box, and what is the new expected number of boxes for the Legendary? (Use `E = (1 − (1 − p)^H) / p`.)

<details>
<summary>Answer and worked solution</summary>

**Answer:** 41.3% reach the pity box. The expected wait falls from 33.3 to 20.0 boxes.

Reaching box 30 needs 29 misses: `0.97^29 = 0.413`. `E = (1 − 0.97^30) / 0.03 = (1 − 0.401) / 0.03 = 19.97`. Without pity, `E = 1 / 0.03 = 33.3`. Pity helps the tail most: no buyer now waits more than 30 boxes.
</details>

25. *Week 6 · design.* For question 23's box, choose one rule that brings the 90th-percentile cost of the Mythic below $60, and explain why duplicate protection alone would not do it.

<details>
<summary>Answer and worked solution</summary>

**Answer:** A hard Mythic pity at 40 boxes. The Mythic's 90th percentile becomes 40 boxes, $59.94.

$60 buys `60 / 1.4985 = 40.04` boxes, so the pity must fall at box 40 or earlier. With pity at 40, every buyer has the Mythic by box 40, so the 90th percentile is at most 40 (it was 57). Duplicate protection only helps when there is more than one missing item in a rarity to choose from. The Mythic is a single item, so protection cannot shorten its wait at all. Protection moves the middle of the cost curve; pity moves the tail.
</details>

26. *Week 6 · ethics.* One colleague says research proves loot boxes cause problem gambling. Another says the research shows nothing. Write a short, balanced statement of what the evidence in the lecture supports, with its numbers.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The evidence shows a consistent association in many Western samples, a weaker or absent one in at least one Chinese sample, and no established direction of cause.

Zendle and Cairns (2018) surveyed 7,422 gamers and found loot box spending related to problem gambling severity (η² = 0.054), much more than other in-game spending (η² = 0.004). A cross-sectional survey cannot say whether loot boxes lead to gambling problems or whether people with gambling problems spend more on loot boxes, and the authors said so. A preregistered survey of 879 players in mainland China did not replicate the link to problem gambling. The UK government's 2022 response accepted an association with harms. For design, that supports treating paid random rewards as a product with a known risk for a minority of buyers, and choosing protections (pity, spending limits, age gates, real-money pricing, fuller disclosure) with that minority in mind. It does not support claiming every buyer is harmed, or that loot boxes are harmless because most buyers spend little.
</details>

## Week 7: Regulation

Lecture: [w07](../lectures/w07-regulation-belgium-netherlands-china-others.md). Status as of 28 September 2026. Use the lecture's five facts `P`, `C`, `T`, `S`, `M` and its eight markets.

27. *Week 7 · regulation.* A collectible card MMO sells random card packs for premium currency that players can buy with money. Cards trade on the in-game auction house for gold, with no official or tolerated cash-out. The game's ranked mode uses the cards, but packs are mainly bought outside it and the studio does not argue skill-embedding. It is rated for teenagers. Encode the facts and give the outcome in each of the eight markets.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `P = yes`, `C = yes`, `T = trade`, `S = no`, `M = yes`. Must remove in 3 of 8 markets (Belgium, Netherlands, Brazil).

- Belgium: `P and C`, so a licence is needed, which means removal.
- Netherlands: `P and C and T ≠ none and not S`, so a licence is needed.
- UK: not licensable gambling (no cash-out); the July 2023 industry guidance applies.
- China and South Korea: publish the odds.
- Brazil: `P and C and M`, so prohibited under Law 15.211, article 20, in force since 17 March 2026.
- Australia: minimum rating M.
- PEGI: default 16 for games submitted from June 2026.

This is the lecture's design D. If the studio argued `S = yes`, only the Netherlands would change, and the lecture warns that `S` is a court's judgment on the facts, not a toggle.
</details>

28. *Week 7 · compute.* For question 27's game, find every single fact change that clears all "must remove" cells, and show why "stop marketing to teenagers" (`M` off) is not one of them.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Only `P` off (packs can no longer be bought with money, directly or through currency) or `C` off (fixed contents).

With `P` off or `C` off, every rule that needs `P and C` fails, so all eight markets clear. With `M` off, Brazil clears but Belgium (`P and C`) and the Netherlands (`T = trade`) remain. With `T = none`, the Netherlands clears but Belgium and Brazil remain. No other single change clears Belgium, which is why its row decides a global build.
</details>

29. *Week 7 · compute.* Question 27's game earns $30 million a year, 35% of it from packs in every market. Belgium is 0.5% of revenue, the Netherlands 2% and Brazil 3%. When packs go, players move 40% of that spending to other products (`k = 0.4`). Compute the cost of a regional switch-off in the three markets and of removing paid randomness everywhere.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Regional: $346,500 a year. Global: $6,300,000 a year, about 18 times as much.

Regional: `30,000,000 × (0.005 + 0.02 + 0.03) × 0.35 × 0.6 = 30,000,000 × 0.055 × 0.21 = $346,500`. Global: `30,000,000 × 0.35 × 0.6 = $6,300,000`. The regional figure leaves out store variants, geolocation, support and exposure to the next market that tightens. The global option costs nothing extra when that happens.
</details>

30. *Week 7 · regulation.* The same FIFA Ultimate Team packs were a game of chance in Belgium (2018) and not in the Netherlands (2022). Name the element of each legal test that differs and the decision that settled the Dutch case.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Belgium's test is `P and C`. The Dutch test, as read by the Council of State on 9 March 2022, adds transfer and "not skill-embedded", and the court found the packs skill-embedded.

The Belgian Gaming Commission's April 2018 report reads the 1999 Gaming and Betting Act as four cumulative elements (game, stake, win or loss, chance), counts purchasable in-game currency as a stake and counts a win "of any type", including cosmetics players value. EA stopped selling FIFA Points for packs in Belgium in early 2019. In the Netherlands, the KSA ordered EA in October 2019 to stop selling packs, and a district court agreed in October 2020. The Council of State overturned the order on 9 March 2022, holding that the packs were part of a larger game of skill (FUT). The difference is one legal judgment about what the packs are for, not a difference in the product.
</details>

31. *Week 7 · regulation.* A colleague says: "Loot boxes are banned across the EU now, and the Digital Fairness Act makes all paid random items illegal from 2026." Correct the statement as of 28 September 2026.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Both parts are wrong as of 28 September 2026.

- There is no EU-wide loot box law. Belgium's position comes from its own national gambling law. The Netherlands treats a paid random item as gambling only if prizes are transferable and the box is not part of a skill game.
- The Digital Fairness Act is a planned proposal. Its public consultation closed on 24 October 2025 and the Commission's planning page lists the proposal for the fourth quarter of 2026. It had not been published on 28 September 2026, so nothing in it binds yet.
- What does apply across the EU is consumer law, as the CPC Network's March 2025 key principles on in-game currencies read it (non-binding in themselves), and PEGI's criteria for games submitted from June 2026, which give paid random items a default PEGI 16 rating. A rating is not a ban, though it can move a game away from a teen audience.
- Even national bans are unevenly enforced. Xiao found 82 of the 100 highest-grossing iPhone games in Belgium still sold loot boxes in July 2022.
</details>

32. *Week 7 · regulation.* A studio's game is rated 12 and sells to Brazilian players. It offers (a) chests earned only by playing, (b) a direct-purchase cosmetic shop, and (c) a paid random chest. Which of these does Brazil's Law 15.211 prohibit, and what else in the PEGI 2026 criteria should the studio check for (b)?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Only (c). For (b), check whether offers are time-limited or quantity-limited, which PEGI now rates at 12.

Article 20 prohibits loot boxes in games aimed at or likely to be accessed by children and adolescents, judged by the age rating, and the law's definition requires payment, so the earned chest (a) is outside it. The direct shop (b) has no chance element. The paid chest (c) in a 12-rated game is prohibited since the law took effect on 17 March 2026. For the shop, PEGI's criteria for games submitted from June 2026 rate time-limited or quantity-limited offers at 12, daily return rewards at 7 and punishment for not returning at 12. A shop full of countdowns does not raise the rating above 12 on that criterion alone, but it should be designed knowing the criterion exists.
</details>

## Week 8: Dark patterns

Lecture: [w08](../lectures/w08-dark-patterns.md). Unless stated, use the lecture's defaults: `A0 = $0.50`, `n = 20`, `s = $1.00`, `m = 10%`, `a = 2`, `r0 = 90%`, `d = 0.20`, `b = 8`.

33. *Week 8 · compute.* A game places more walls: `n = 30` a month, everything else at the defaults. Compute LTV at `w = 0` and `w = 6`. The LTV-maximizing wait is now exactly 4 hours. Compute LTV and lifetime there, and the lifetime lost against no wall.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `LTV(0) = $5.00`, `LTV(6) = $14.81`. At `w = 4`: LTV $15.00, lifetime 6.0 months, 40% of lifetime lost.

At `w = 6`: `π = 0.10 × 6/8 = 7.5%`, `ARPU = 0.50 + 30 × 0.075 = $2.75`, `r = 0.90 − 0.20 × 6/14 = 81.43%`, `L = 5.385`, `LTV = 2.75 × 5.385 = $14.81`. At `w = 4`: `π = 6.67%`, `ARPU = 0.50 + 30 × 0.0667 = $2.50`, `r = 0.90 − 0.20 × 4/12 = 83.33%`, `L = 6.0`, `LTV = $15.00`. Lifetime lost is `1 − 6.0 / 10.0 = 40%`. More walls make the skip a larger share of ARPU, so each extra minute of wait raises ARPU by a larger percentage, and the optimum moves from 3.46 to 4 hours.
</details>

34. *Week 8 · compute.* A studio rule says no wall may cut modelled lifetime by more than 10% against no wall. Under the defaults, what is the longest wait allowed, what LTV does it give, and what share of the peak LTV ($11.02) does the rule give up?

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 0.47 hours (28 minutes), LTV $7.93, giving up 28% of the peak.

A 10% cut means `L(w) ≥ 9` months, so `r(w) ≥ 1 − 1/9 = 0.8889` and `0.20 × w / (w + 8) ≤ 0.0111`. Then `w / (w + 8) ≤ 0.0556`, which gives `w ≤ 0.0556 × 8 / 0.9444 = 0.47`. At `w = 0.47`, `π = 1.90%`, `ARPU = $0.88`, `L = 9.00`, `LTV = $7.93`. `1 − 7.93 / 11.02 = 28%`. The rule still earns 59% more than no wall ($5.00) while keeping lifetime within 10%.
</details>

35. *Week 8 · compute.* A subscription starts in 1 step and cancels in 5. Each step is completed by 90% of those who start it. Compute both completion rates and the asymmetry ratio. Separately, 3% of 2,000 store visits contain an accidental buy press. How many accidental purchases does a one-step buy flow produce, and how many with a confirmation that catches 90% of mistakes? What does the confirmation cost in intended purchases?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Start 90%, cancel 59.0%, ratio 1.52. Accidental purchases fall from 60 to 6. Intended buy completion falls from 90% to 81%.

`0.9^5 = 0.590`. The ratio is `0.9^(1 − 5) = 1.52`. Accidental presses: `0.03 × 2,000 = 60`. With the confirmation, `60 × 0.1 = 6`. The confirmation adds a step, so intended completion becomes `0.9² = 81%`. A tenfold cut in mistakes for a 9-point drop in completion is the trade the studio chooses when it decides whether to confirm.
</details>

36. *Week 8 · ethics.* Classify each feature with the Zagal taxonomy and the disclosure test, and say whether it is pacing, grey or dark. (a) A daily login streak that resets to zero if the player misses a day, in a game submitted to PEGI in July 2026. (b) A bundle labelled "leaves the store on Sunday, returns in spring". (c) A checkout that pre-selects the largest currency pack. (d) A 12-hour crafting timer with no skip in an adult MMO.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) playing by appointment, grey to dark, with a PEGI 12 rating cost; (b) honest limited-time offer, acceptable; (c) interface misdirection, dark; (d) pacing, not dark.

(a) The streak punishes not returning, which PEGI's 2026 criteria rate at 12 for games submitted from June 2026. It works by loss rather than reward, so it fails the interest test for players who would rather skip a day. A version that rewards returning without resetting (PEGI 7) keeps the habit without the penalty.

(b) Time pressure exists, but the statement is true and says the item returns, so it passes the disclosure test. It becomes dark only if "leaves on Sunday" is false urgency. PEGI still rates time-limited offers at 12, which matters for a young audience.

(c) It makes the studio's preferred choice easier than the player's, the asymmetric friction the FTC's Epic complaint described. It would not survive the store saying plainly "we pre-selected the most expensive pack".

(d) No paid skip means `π = 0`, so the timer is not for sale. An adult audience and a clear purpose make it ordinary pacing.
</details>

## Week 9: Whales and spending distributions

Lecture: [w09](../lectures/w09-whales-and-spending-distributions.md).

37. *Week 9 · compute.* A server of 10 players spends, this month, $0 (six players), $2, $4, $10 and $24. Compute the payer rate, `G_pay`, `G_all` directly and by the identity, and the share of revenue held by the top 10% and top 20% of players.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `p = 0.40`, `G_pay = 0.45`, `G_all = 0.78` both ways. The top 10% hold 60% and the top 20% hold 85%.

Payers sorted: 2, 4, 10, 24, total 40, `n = 4`. `Σ(2i − 5)x = −3 × 2 − 1 × 4 + 1 × 10 + 3 × 24 = 72`, so `G_pay = 72 / (4 × 40) = 0.45`. For all ten players, `Σ(2i − 11)x = 3 × 2 + 5 × 4 + 7 × 10 + 9 × 24 = 312`, so `G_all = 312 / (10 × 40) = 0.78`. The identity gives `0.60 + 0.40 × 0.45 = 0.78`. The Lorenz curve reaches 0.40 at `F = 0.9` and 0.15 at `F = 0.8`, so the top player holds `1 − 0.40 = 60%` and the top two hold `1 − 0.15 = 85%`.
</details>

38. *Week 9 · code.* A teammate's Gini function prints 0.580 for question 37's server. Find the bug and explain why the error is exactly 0.2.

```python
def gini(xs):
    xs = sorted(xs)
    n, total = len(xs), sum(xs)
    return sum((2 * i - n - 1) * x for i, x in enumerate(xs)) / (n * total)

spend = [0] * 6 + [2, 4, 10, 24]
print(f"{gini(spend):.3f}")
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** `enumerate(xs)` starts at 0, but the formula's rank `i` starts at 1. Use `enumerate(xs, start=1)`.

Starting at 0 lowers every rank by 1, so every weight `2i − n − 1` falls by 2. The numerator falls by `2 × total`, and the result falls by `2 × total / (n × total) = 2 / n`. With `n = 10`, that is 0.2, so the function prints `0.78 − 0.20 = 0.580`. The bug is invisible on large lists (where `2/n` is tiny) and large on small test lists, which is a reason to test with a hand-checked small case.
</details>

39. *Week 9 · compute.* Payers follow a Pareto shape with `α = 1.5`, and 5% of players pay. Compute `G_pay`, `G_all`, the top 10% of payers' share of revenue and the top 1% of players' share.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `G_pay = 0.50`, `G_all = 0.975`, top 10% of payers 46.4%, top 1% of players 58.5%.

`G_pay = 1 / (2 × 1.5 − 1) = 0.50`. `G_all = 0.95 + 0.05 × 0.50 = 0.975`. `1 − 1/α = 1/3`, so the top 10% of payers hold `0.1^(1/3) = 46.4%`. The top 1% of players is the top 20% of payers when `p = 5%`, so its share is `0.2^(1/3) = 58.5%`. `G_all` would read 0.975 whatever the payers did between 0.95 and 1, which is why the payer curve is the one to report.
</details>

40. *Week 9 · compute.* ARPPU is $20 a month and payers follow a Pareto shape with `α = 1.6`. A monthly cap of $150 is proposed. Compute the minimum spend `x_m`, the share of payers affected and the share of revenue lost.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `x_m = $7.50`, 0.83% of payers affected, 10.4% of revenue lost.

`x_m = 20 × 0.6 / 1.6 = $7.50`. `x_m / C = 0.05`. Payers above the cap: `0.05^1.6 = 0.0083`. Revenue lost: `0.05^0.6 / 1.6 = 0.1657 / 1.6 = 0.104`. The cap touches fewer than one payer in a hundred and removes a tenth of revenue, which is the same "few people, much money" shape as the lecture's $100 row.
</details>

41. *Week 9 · ethics.* A studio director says: "Our whales are wealthy adults who choose to spend. Spending caps are paternalism." Give a balanced reply that uses the evidence from the lecture, its limits, and at least one protection other than a hard cap.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The best available evidence does not support the claim, but it also cannot identify any single player, so the reply should favour protections that help those at risk without assuming everyone is.

Close and colleagues (2021) pooled six survey datasets of 7,767 loot box buyers. Spending tracked problem gambling scores (ρ = 0.34) and not earnings (ρ = 0.02, not significant), and buyers spending $500 or more a month had a mean PGSI of about 9.75, in the problem range. The data are self-reported and cross-sectional, and the authors removed 24 respondents over $1,000 a month, so they show an association, not cause, and say nothing about a given player. Some high spenders are long-term fans with the means to pay. Options short of a hard cap include player-set limits with a cooling-off period, spending controls for all players (asked for in the UK's 2023 industry guidance), and not targeting offers or price rises at the top spend band. The EU CPC principles of March 2025 also ask studios to avoid business models built on players willing to spend excessive amounts. Report the revenue cost of each option, from the cap model, beside the decision.
</details>

## Week 10: Pricing experiments

Lecture: [w10](../lectures/w10-pricing-experiments.md). Sample sizes use `α = 0.05` two-sided and 80% power, `Z = 1.96 + 0.8416`.

42. *Week 10 · compute.* A bundle at $2.99 converts 8.0% of exposed players. A test arm at $3.99 converts 6.5%. Compute `RPE` for both, the change in `RPE`, the break-even conversion for $3.99 and the arc elasticity. Did the rise pay?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `RPE` $0.2392 against $0.2594 (+8.4%). Break-even 6.0%. Arc elasticity −0.72. Yes, the rise paid.

`RPE0 = 2.99 × 0.08 = 0.2392`, `RPE1 = 3.99 × 0.065 = 0.2594`, a gain of 8.4%. Break-even is `0.08 × 2.99 / 3.99 = 5.99%`, and 6.5% is above it. Arc elasticity: `(−0.015 / 0.0725) / (1.00 / 3.49) = −0.207 / 0.287 = −0.72`. Demand is inelastic in this range, so the price rise gained revenue while losing about one buyer in five.
</details>

43. *Week 10 · compute.* For question 42's test, how many exposed players per arm are needed to detect the change in conversion, and to detect the change in `RPE`? The store shows the offer to 10,000 players a week in total, split evenly. How many weeks does each take?

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 4,688 per arm for conversion (under a week) and 31,424 per arm for `RPE` (about 6.3 weeks).

Conversion: `7.849 × (0.08 × 0.92 + 0.065 × 0.935) / 0.015² = 7.849 × 0.1344 / 0.000225 = 4,688`. Revenue: `7.849 × (2.99² × 0.0736 + 3.99² × 0.0608) / (0.2594 − 0.2392)² = 31,424`. At 5,000 players per arm per week, that is 0.94 weeks against 6.3 weeks. A test powered for conversion would stop long before it could say anything about revenue.
</details>

44. *Week 10 · compute.* World of Warcraft's one-month plan has cost US$15 since 2004. Using the lecture's CPI figures (188.9 in 2004, 321.9 in 2025), what is the 2004 price in 2025 dollars? If the price rose to US$18, what share of subscribers would have to stay for revenue to break even? Separately, a subscription at $10 with 5% monthly churn moves to $12 and churn rises to 6.5%. Compare `p / m` before and after, and give the break-even churn.

<details>
<summary>Answer and worked solution</summary>

**Answer:** About US$25.56 in 2025 dollars. At US$18, 83.3% must stay. For the second game, `p / m` falls from $200 to $184.62, and the break-even churn is 6.0%.

`15 × 321.9 / 188.9 = 25.56`. Break-even retention for the rise is `15 / 18 = 83.3%`. For the second game, `10 / 0.05 = 200` and `12 / 0.065 = 184.62`, so the rise loses lifetime value per subscriber even though each month earns 20% more. Break-even churn is `0.05 × 12 / 10 = 6.0%`. The lecture's point about Blizzard applies: a subscription price in a shared world cannot be A/B tested cleanly, and churn reacts over months.
</details>

45. *Week 10 · regulation.* A test arm shows "was $9.99, now $6.99" to EU players who never saw $9.99 in force, and prices are assigned by hashing account ids. Which EU rules does this touch, and what is a defensible studio policy on who gets tested at which price?

<details>
<summary>Answer and worked solution</summary>

**Answer:** The Omnibus directive's prior-price rule and its disclosure rule for personalised prices, both applied from 28 May 2022.

Directive (EU) 2019/2161 requires that an announced price reduction show the prior price, the lowest applied in at least the 30 days before. A "was $9.99" that was never a price in force is what the rule targets. It also requires traders to say, where applicable, that a price was personalised by automated decision-making. Whether a random hash-based split counts is a question for legal before launch. A defensible policy randomizes price arms across players, never targets price rises at players a model predicts will spend heavily (the top band is where week 9's evidence places players at risk), prefers offer tests around a public list price, and refunds or honours the lower price for any player shown to have paid more in a test.
</details>

## Week 11: Subscription tokens

Lecture: [w11](../lectures/w11-subscription-tokens.md). `ΔR = T × (c × (1 − σ) − k × s)` and `σ* = 1 − k × s / c`.

46. *Week 11 · compute.* A subscription costs $12 and a token $16. Each month 50,000 game-time months are paid with tokens. 60% of token players would have paid cash anyway, and 20% of token dollars displace other store spending. Compute `ΔR`, the break-even `σ` and the number of players kept who would otherwise have left.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `ΔR = $280,000` a month, `σ* = 0.55`, 20,000 players kept.

`16 × 0.8 − 0.6 × 12 = 12.8 − 7.2 = 5.6` per token month, and `50,000 × 5.6 = $280,000`. `σ* = 1 − 0.6 × 12 / 16 = 1 − 0.45 = 0.55`. Kept players are `T × (1 − k) = 50,000 × 0.4 = 20,000`, whose social value the formula does not count.
</details>

47. *Week 11 · compute.* A studio sells tokens at $18 only through a console store that keeps 30%, and subscriptions at $15 on its own site with a 3% payment cost. Compute the net prices. At `σ = 0`, above what share `k` of cannibalized subscribers does the token lose money?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Net token $12.60, net subscription $14.55. The token loses money when `k > 0.866`.

`0.7 × 18 = 12.60`. `0.97 × 15 = 14.55`. At `σ = 0` the gain per token month is `12.60 − k × 14.55`, which is negative for `k > 12.60 / 14.55 = 0.866`. The $3 premium in list prices became a $1.95 discount in net dollars. Compare token and subscription revenue net of each one's channel costs.
</details>

48. *Week 11 · compute.* Using the prices the lecture reports for September 2026, compute the token premium of the WoW Token against the 12-month plan (US$13 a month) and of 20 OSRS bonds (US$192.99 for 12 months) against the 12-month membership (US$131.88). Why does a premium protect game-time revenue?

<details>
<summary>Answer and worked solution</summary>

**Answer:** WoW `20 / 13 = 1.54`. OSRS `192.99 / 131.88 = 1.46`.

With `σ = 0`, the token's gain per month is `c − k × s`. Because `k ≤ 1`, the worst case is `c − s`, which is positive whenever `c > s`. Even if every token player would have paid cash anyway, each token month earns the premium. A premium cannot protect against `σ` or against a platform fee that pushes the net token price below the net subscription, which is why questions 46 and 47 matter.
</details>

49. *Week 11 · ethics.* A token is proposed for an MMO whose auction house sells the best raid gear. Name what changes for players, one item or service gold should never buy once the token exists, and one argument in the token's favour.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The token puts a dollar price on everything gold can buy, so gear bought for gold becomes power bought for money through a sanctioned channel.

Week 4's line between cosmetics and power moves for every item on the market at once. Items gold should not buy might include ranked-mode advantages, account-bound progression shortcuts or anything a PvP ladder depends on. Gold spending also becomes money spending, so it should sit under the same spending limits and parental controls as cash. In the token's favour: it gives time-rich, cash-poor players access to a subscription game, lets busy players skip a grind through a channel the studio controls, and draws demand away from third-party gold sellers and the account theft that feeds them. The design question is what gold can buy once it has a price, not whether tokens are acceptable in general.
</details>

## Week 12: Publishing, platforms and fees

Lecture: [w12](../lectures/w12-publishing-platforms-and-fees.md). Steam since October 2018: 30% to US$10M, 25% to US$50M, 20% above. Epic from June 2025: 0% on the first US$1M per product per year, 12% after.

50. *Week 12 · code.* Predict the three lines this prints, then state the marginal and average rate at US$25 million.

```python
STEAM = [(0, 0.30), (10e6, 0.25), (50e6, 0.20)]

def take(gross, brackets):
    total = 0.0
    for i, (start, rate) in enumerate(brackets):
        end = brackets[i + 1][0] if i + 1 < len(brackets) else float("inf")
        if gross > start:
            total += rate * (min(gross, end) - start)
    return total

for g in (25e6, 26e6):
    print(f"${g/1e6:.0f}M  take ${take(g, STEAM)/1e6:.2f}M  average {take(g, STEAM)/g:.1%}")
print(f"extra on the 26th million: ${(take(26e6, STEAM) - take(25e6, STEAM))/1e6:.2f}M")
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
$25M  take $6.75M  average 27.0%
$26M  take $7.00M  average 26.9%
extra on the 26th million: $0.25M
```

`0.30 × 10M + 0.25 × 15M = 3M + 3.75M = 6.75M`. The marginal rate at US$25M is 25%, the take on the next million. The average is 27.0% and approaches 20% only as revenue grows without limit. Budget with the average, decide with the marginal.
</details>

51. *Week 12 · compute.* A developer eligible for Apple's Small Business Program earns US$2.5 million this year. What does Apple take this year, and what would it take on the same revenue next year? An Epic Games Store game earns US$3 million. What is Epic's take and average rate?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Apple: US$0.60M (24%) this year, US$0.75M (30%) next year. Epic: US$0.24M (8%).

Apple this year: `0.15 × 1M + 0.30 × 1.5M = 0.15M + 0.45M = 0.60M`. Next year the developer made more than US$1M last year, so it pays 30% on everything: `0.30 × 2.5M = 0.75M`. That is a status rule: crossing the threshold costs more in the following year. Epic: `0.12 × (3M − 1M) = 0.24M`, `0.24 / 3 = 8%`.
</details>

52. *Week 12 · compute.* Players spend US$5.5 million on a Steam game in its first year, including tax at a blended 10% of the pre-tax price. Refunds and chargebacks are 5% of pre-tax revenue. A publisher advanced US$1.5 million, splits Steam payouts 60/40 in its own favour, and recoups the advance from the studio's 40%. Build the waterfall to the studio's royalty. Then recompute if the publisher instead recoups from 100% of payouts before the same split.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Studio royalty US$0, with US$170,000 still unrecouped. Under "recoup from all payouts first", the studio receives US$730,000.

| Step | Amount | Left |
|---|---|---|
| Consumer spend | 5,500,000 | 5,500,000 |
| Tax (`5.5M × 0.10 / 1.10`) | −500,000 | 5,000,000 |
| Refunds (5%) | −250,000 | 4,750,000 |
| Steam (30%, first bracket) | −1,425,000 | 3,325,000 payout |
| Publisher's 60% | −1,995,000 | 1,330,000 studio's 40% |
| Recoupment | −1,330,000 | 0 royalty, 170,000 unrecouped |

With recoupment from all payouts: `3,325,000 − 1,500,000 = 1,825,000`, and the studio's 40% is `$730,000`. The clause, not the split, decides whether the studio sees any money in year one.
</details>

53. *Week 12 · compute.* A direct store's card processor charges 2.9% plus 30 cents. At what basket size is the fee exactly 10% of the purchase? What share does it take from a US$2.99 purchase? Why do premium currencies exist partly because of this?

<details>
<summary>Answer and worked solution</summary>

**Answer:** US$4.23. It takes 12.9% of a US$2.99 purchase.

`0.029 b + 0.30 = 0.10 b` gives `0.071 b = 0.30`, `b = US$4.23`. On US$2.99: `0.029 × 2.99 + 0.30 = 0.387`, and `0.387 / 2.99 = 12.9%`. A fixed per-purchase charge punishes small baskets. Selling currency in packs turns many small purchases into one large one, which cuts processing cost, and week 3 showed the price the player pays for that in leftovers.
</details>

54. *Week 12 · compute.* A game expects US$3 million on the Epic Games Store. How many times as many buyers must Steam (30% at that size) bring to leave the studio the same net revenue? How does that compare with the lecture's headline 1.26?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Steam must bring about 1.31 times as many buyers.

Epic's average rate at US$3M is 8%, so it leaves 92 cents a dollar. Steam leaves 70. `0.92 / 0.70 = 1.31`. The lecture's 1.26 uses Epic's 12% marginal rate (`0.88 / 0.70`). For a game this size, the first-million rule makes Epic's average lower, so the reach gap Steam must close is larger. Compare channels by average rate at your forecast revenue.
</details>

## Week 13: Team and budget planning

Lecture: [w13](../lectures/w13-team-and-budget-planning.md).

55. *Week 13 · compute.* A plan has pre-production 8 months at 10 people, production 20 months at 35 and beta 8 months at 50. Loaded cost is $9,000 per head-month and fixed costs $40,000 a month. Compute each phase's burn and cost, the total, and the cost of a 2-month slip in each phase. The studio has raised $12.8 million. Which slips does it survive?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Burns $130,000, $355,000 and $490,000. Phase costs $1.04M, $7.10M and $3.92M; total $12.06M. Two-month slips cost $260,000, $710,000 and $980,000. It survives the first two; a beta slip runs out of cash in month 38, the last month.

`10 × 9,000 + 40,000 = 130,000`; `35 × 9,000 + 40,000 = 355,000`; `50 × 9,000 + 40,000 = 490,000`. Totals with a slip: $12.32M (pre-production, $480,000 left), $12.77M (production, $30,000 left) and $13.04M (beta). The beta version passes $12.8M during its 38th and final month. The same two months cost almost four times as much late as early.
</details>

56. *Week 13 · compute.* A studio has $5 million, 25 people at $8,000 per head-month and $30,000 of fixed monthly costs. What is its runway?

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 21.7 months.

Burn is `25 × 8,000 + 30,000 = $230,000` a month. `5,000,000 / 230,000 = 21.7` months.
</details>

57. *Week 13 · compute.* At the end of month 12 of a 22-month production phase, a 40-person team is two months behind (80 head-months). Loaded cost is $10,000 and fixed costs $50,000. The producer proposes hiring 10 people now. Each works at 50% for three months and costs an existing member 20% of their time for those months. Does the hire recover the slip, and what does it cost against simply slipping?

<details>
<summary>Answer and worked solution</summary>

**Answer:** No. Net extra output is 79 head-months against 80 needed. The hire costs $1.0 million against $900,000 for the slip.

Output from hires: `10 × (3 × 0.5 + 7 × 1.0) = 85` head-months. Mentoring: `10 × 3 × 0.2 = 6`. Net 79, one short. Hiring costs `10 × 10 × 10,000 = $1,000,000`. Slipping two months costs `2 × (40 × 10,000 + 50,000) = $900,000`. The hire costs more and still misses the date, which is Brooks's point: the later you add people, the less of the remaining time they spend at full speed.
</details>

58. *Week 13 · compute.* The question 55 plan holds a 15% contingency on its $12.06 million build cost. How many months of production burn and of beta burn does it cover?

<details>
<summary>Answer and worked solution</summary>

**Answer:** $1.809 million, about 5.1 months of production or 3.7 months of beta.

`0.15 × 12,060,000 = 1,809,000`. `1,809,000 / 355,000 = 5.10`. `1,809,000 / 490,000 = 3.69`. The same reserve buys fewer months the later it is spent, so put the largest contingency where burn is highest and risks are least tested.
</details>

## Week 14: Pitching to publishers and investors

Lecture: [w14](../lectures/w14-pitching-to-publishers-and-investors.md). `EV_all = pV − C1 − C2` and `EV_gate = −C1 + max(0, p·s·(V − C2) − (1 − p)·f·C2)`.

59. *Week 14 · compute.* A pitch has `p = 0.30`, `V = 50`, `C1 = 3` and `C2 = 15` ($ millions). The gate has `s = 0.85` and `f = 0.25`. Compute the all-in EV, the perfect-gate EV, the gated EV, the kill rate, `P(hit | go)` and the break-even false-go rate `f*`. Should the funder continue after a "go"?

<details>
<summary>Answer and worked solution</summary>

**Answer:** All in −3.0. Perfect gate +7.5. Gated +3.3. Kill rate 57%. `P(hit | go) = 0.593`. `f* = 0.564`. Yes, continue after a "go".

All in: `0.3 × 50 − 3 − 15 = −3`. Perfect: `−3 + 0.3 × 35 = 7.5`, a gate value of `(1 − 0.3) × 15 = 10.5`. Gated: `0.3 × 0.85 × 35 = 8.925`, `0.7 × 0.25 × 15 = 2.625`, `−3 + 8.925 − 2.625 = 3.3`. Kill rate: `1 − (0.255 + 0.175) = 0.57`. Posterior: `0.255 / 0.43 = 0.593`, and `0.593 × 50 = 29.7 > 15`. Break-even: `(8.925 − 3) / (0.7 × 15) = 0.564`.
</details>

60. *Week 14 · compute.* A studio sells 15% for $3 million in a seed round, then 25% for $20 million in a Series A after a passed gate. Compute each round's pre-money and post-money valuation and the founders' final share.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Seed: post-money $20M, pre-money $17M. Series A: post-money $80M, pre-money $60M. Founders own 63.75%.

`3 / 0.15 = 20`, `20 − 3 = 17`. `20 / 0.25 = 80`, `80 − 20 = 60`. Founders: `0.85 × 0.75 = 0.6375`. The step from $20M post-money to $60M pre-money is the price of the evidence the gate produced.
</details>

61. *Week 14 · critique.* A student pitch says: "We have already spent $4 million, so stopping would waste it. Comparable MMOs succeed 40% of the time. We ask for the full $20 million now." Identify three problems and rewrite the ask.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Sunk cost, survivorship bias in the comps, and an all-in ask that forces the funder to accept the all-in EV.

The $4 million already spent appears in both branches of the decision, so it cannot justify continuing. Comps are games that shipped. Cancelled projects (about half of Blizzard's starts, by Morhaime's 2019 account) never appear in a comp list, so 40% overstates `p`. Asking for everything removes the funder's option to stop, which the lecture shows is where a gate's value comes from, `(1 − p) × C2` with a perfect gate. A better ask: "$2 million for a vertical slice with a closed playtest. Go/no-go on day-30 retention of at least X% in a test of N players, measured on date D, decided by the funder. If the gate says stop, we keep the tools, refund testers' purchases, and help the team move to other projects."
</details>

## Week 15: Integration

These draw on several weeks and suit the business plan viva.

62. *Weeks 2, 9, 14 · critique.* A business plan forecasts ARPPU of $17.32 a month with Pareto payers at `α = 1.43`, and says "revenue risk is low because only 1.5% of payers spend over $100 a month". Using week 9's cap model, how much revenue sits above $100 a month, and what should the plan's risk slide say instead?

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 19.6% of revenue is spending above $100 a month by those 1.46% of payers. The risk slide should state that share, not the payer count.

With `x_m = $5.21`, `(5.21/100)^1.43 = 1.46%` of payers exceed $100, and `(5.21/100)^0.43 / 1.43 = 19.6%` of revenue is their spending above the line. A law, a competitor or a design change that affects those accounts moves a fifth of revenue. The slide should give that share, a second top share (top 1% and top 10% of payers) to show the shape, and the plan's position on spending limits, which funders will read as regulatory and reputation risk.
</details>

63. *Weeks 1, 3, 7, 12 · design.* Your plan sells a hybrid MMO on Steam and mobile, with a premium currency, an optional subscription and cosmetic chests. List the decisions from this course that change the plan's net revenue per player and name the week that gives each one a number.

<details>
<summary>Answer and worked solution</summary>

**Answer:** At least these, each with its model.

- Door, upfront price and monthly meter, and the retention needed to beat the alternatives (week 1, contribution and break-even `S*`).
- The horizon, fee basis and cohort of every LTV, and payback against CAC by channel (week 2).
- Pack grid and item prices, the markup and leftover they force, and whether the store shows real prices (week 3).
- What the store sells in ranked modes, in rating points (week 4).
- Pass finish line and rebate placement (week 5).
- Chest odds, pity, the full cost disclosure (week 6), and which markets require removal or a rating change, with the regional switch-off cost (week 7).
- Walls and flows reviewed for dark patterns, with lifetime reported beside LTV (week 8).
- Revenue concentration and the cost of any spending protection (week 9).
- The price test plan and its sample size (week 10), and a token only if its net premium survives the platform fee (week 11).
- Store take by channel at forecast revenue, payment fees and the publishing waterfall (week 12).
</details>

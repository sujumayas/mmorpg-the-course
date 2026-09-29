# MMO403 · Week 02 — Unit Economics: LTV, CAC, ARPPU

**Why this matters:** Free games pay to be installed. A studio that buys players for more than they will ever bring in grows its player count and loses money on every one, and it can do this for a long time before anyone notices. Unit economics is the arithmetic that tells you what a player is worth, what you can pay to get one, and when that money comes back.

**You will be able to:**
- Compute a lifetime value (LTV) curve by summing a retention curve times net ARPDAU, and read the payback day where it crosses the cost to acquire a player (CAC).
- Decompose ARPDAU into payer rate and ARPPU and predict how each moves LTV.
- Explain why most of a game's LTV comes from the few players who stay, and why an LTV measured at day 30 can understate the lifetime figure by half.
- Critique an acquisition plan that states an LTV without its horizon, its fee basis or the channel its players came from.

**Before class:** Fields & Cotton, *Social Game Design: Monetization Methods and Mechanics* (Morgan Kaufmann, 2011), the chapters on metrics and on acquiring and retaining players (the course reader lists the pages). Skim David Skok, "SaaS Metrics 2.0: A Guide to Measuring and Improving What Matters" (forEntrepreneurs.com), the sections on LTV to CAC and months to recover CAC.

**Prerequisites from earlier courses:** [MMO308 week 1, what live ops is](../../MMO308-live-operations-analytics-and-experimentation/lectures/w01-what-live-ops-is.md) (the two-type retention curve `R(a) = w × qs^a + (1 − w) × qt^a` and the lifetime `L`; this lecture uses both without re-deriving them). [MMO308 week 2, KPIs](../../MMO308-live-operations-analytics-and-experimentation/lectures/w02-kpis-dau-mau-stickiness-arpdau.md) (the KPI tree, `ARPDAU = payer rate × ARPPU`, and why units hide in "per user" KPIs). [GS101 week 11](../../GS101-history-and-critical-study-of-games/lectures/w11-free-to-play-mobile-and-live-service.md) (LTV under constant retention, `ARPU × 1 / (1 − r)`). From this course, [week 1, business models](w01-business-models-box-subscription-f2p-hybrid.md) (contribution and cost to serve).

**Interactive:** [The LTV curve](../examples/w02-ltv-curve.html), built from the spec at the end of this lecture. Keep it open during section 2.

---

## 1. The player as the unit

Week 1 looked at a whole audience. Unit economics looks at one player, the **unit**, and asks three questions about them.

- **What does a player bring in?** Their **lifetime value (LTV)**: the revenue one install produces over its whole life, net of the costs that scale with that revenue. In this course LTV means *net of platform fees* unless stated otherwise. Some teams also subtract cost to serve, which gives a **contribution LTV**. Always say which one you mean.
- **What does a player cost to get?** The **cost to acquire a customer (CAC)**: marketing spend divided by the installs it produced. Mobile teams often call the per-install price **CPI** (cost per install). **Paid CAC** divides paid spend by paid installs only. **Blended CAC** divides all spend by all installs, including organic ones that cost nothing, and is always lower.
- **When does the money come back?** The **payback day** is the day on which the cumulative LTV of a cohort first reaches its CAC. Before it, the studio is funding the player. After it, the player is funding the studio.

Two KPIs from MMO308 week 2 feed LTV directly. **ARPDAU** (average revenue per daily active user) is revenue on a day divided by that day's DAU. **ARPPU** (average revenue per paying user) is revenue divided by the number of payers in the same period. They are linked by the payer rate, `ARPDAU = payer rate × ARPPU`. Keep the time unit attached. In this lecture all three are daily.

## 2. Worked example: the LTV curve

### The hook

In 2013 King Digital Entertainment, the maker of Candy Crush Saga, had revenue of $1,884 million. When it filed to list its shares in the US in 2014, its prospectus showed that its sales and marketing expenses had grown from $55 million in 2012 to $377 million in 2013, most of it performance marketing to acquire players. The same document said about 4% of its monthly users paid anything in December 2013, and described running thousands of acquisition campaigns every 24 hours, all held to "the same target return parameters."

So King spent roughly one dollar in five of its revenue buying players for a free game, knowing that about 96 in 100 of them would pay nothing in a given month. Why is that rational? And what is a "target return parameter"? The answer is a curve.

### The model

Take one install cohort. Let `R(d)` be the share still active on day `d` after install, with day 0 the install day. Use the two-type curve from MMO308 week 1, now in days:

```
R(d)     = w × qs^d + (1 − w) × qt^d
LTV(T)   = a × (1 − f) × [ R(0) + R(1) + ... + R(T − 1) ]
LTV(∞)   = a × (1 − f) × [ w / (1 − qs) + (1 − w) / (1 − qt) ]
payback  = the first day D with LTV(D + 1) ≥ CAC
```

- `w` is the share of **stayers**, `qs` their daily survival, `qt` the daily survival of **tourists**.
- `a` is gross ARPDAU, assumed the same for every active day (section 3 relaxes this).
- `f` is the platform fee as a fraction. King's prospectus says its platforms (Apple, Google, Amazon, Facebook) typically charged about 30% of after-tax payments. Apple's standard App Store commission is 30% today, and 15% for developers in its Small Business Program.
- `LTV(T)` is net revenue per install over the first `T` days. It is the area under the retention curve up to day `T`, times net ARPDAU.

That last sentence is the signature idea of this week. **LTV is retention times ARPDAU integrated over time.** The retention curve says how many active days an install produces. ARPDAU says what each active day is worth. Multiply and add.

### Numbers you can check

Use `w = 0.25`, `qs = 0.98`, `qt = 0.40`, `a = $0.20` and `f = 0.30`, so net ARPDAU is `0.20 × 0.70 = $0.14`. These are invented values in a plausible range for a mid-sized online game, not any studio's data. Check day 1 by hand: `R(1) = 0.25 × 0.98 + 0.75 × 0.40 = 0.245 + 0.300 = 0.545`.

| Day `d` | `R(d)` | Cumulative LTV through day `d` |
|---|---|---|
| 0 | 1.000 | $0.140 |
| 1 | 0.545 | $0.216 |
| 7 | 0.218 | $0.436 |
| 30 | 0.136 | $0.989 |
| 60 | 0.074 | $1.415 |
| 90 | 0.041 | $1.647 |
| 180 | 0.007 | $1.880 |
| ∞ | 0 | $1.925 |

The lifetime figure comes from the closed form. The expected number of active days per install is `L = 0.25 / 0.02 + 0.75 / 0.60 = 12.5 + 1.25 = 13.75`, and `13.75 × 0.14 = $1.925`.

Now add a CAC. Suppose the studio pays $1.50 per install:

| CAC | LTV / CAC | Payback day |
|---|---|---|
| $0.50 | 3.85 | 10 |
| $1.00 | 1.93 | 31 |
| $1.50 | 1.28 | 70 |
| $1.75 | 1.10 | 113 |
| $2.00 | 0.96 | never |

At $1.50 the average install pays for itself on day 70, and returns 28% more than it cost over its whole life. At $2.00 it never pays back. That is King's "target return parameter" in its simplest form: bid for installs only while the predicted LTV curve clears the price by the margin you require, within the time you are willing to wait.

Look at the split inside `L`. Stayers contribute 12.5 of the 13.75 active days, so **91% of lifetime value comes from the quarter of installs who stay**. The tourists, three quarters of the cohort, are worth about 23 cents each on average (`1 / 0.60 = 1.67` active days at $0.14), or 17.5 cents of each install's $1.925. That is why the retention curve on the left looks like a disaster (half the cohort gone on day 1) while the LTV curve still climbs for months.

This code reproduces the tables. It runs as shown with `.venv/bin/python`:

```python
w, qs, qt = 0.25, 0.98, 0.40      # stayer share, stayer and tourist daily survival
arpdau, fee = 0.20, 0.30          # gross revenue per DAU; platform fee
net = arpdau * (1 - fee)

def R(d):
    return w * qs**d + (1 - w) * qt**d

def ltv(T):                        # net revenue per install over days 0 .. T-1
    return net * sum(R(d) for d in range(T))

def payback_day(cac, horizon=3650):
    return next((d for d in range(horizon) if ltv(d + 1) >= cac), None)

lifetime = net * (w / (1 - qs) + (1 - w) / (1 - qt))
print(f"LTV d30 {ltv(31):.3f}  d90 {ltv(91):.3f}  lifetime {lifetime:.3f}")
for cac in (1.00, 1.50, 2.00):
    print(f"CAC {cac:.2f}: payback day {payback_day(cac)}")
```

It prints `LTV d30 0.989  d90 1.647  lifetime 1.925`, then payback days 31, 70 and `None`.

### The visual

Open `examples/w02-ltv-curve.html`. The left view is the retention curve `R(d)` as a filled area, with the stayer and tourist parts shaded differently. It drops by half in a day and looks like a leak. The right view is `LTV(T)`, the running total of that area times net ARPDAU, with a horizontal line at CAC. The height of the right curve on any day equals the shaded area to the left of that day on the left view.

Drag `qs` from 0.98 to 0.97. The left curve barely changes in the first week. The right curve's plateau drops from $1.93 to $1.34 and the payback line moves from day 70 to never. Now drag `qt` from 0.40 to 0.60, a big improvement that lifts day-1 retention from 55% to 70%. The left curve jumps visibly, and the right plateau rises by only about 9 cents. The picture to take away is that the first days of retention are the most visible and the least valuable, and the tail you can hardly see on the left is most of the money on the right.

### Cross-game recognition

**King (2013), read backwards.** Sales and marketing of $377 million against revenue of $1,884 million is a spend ratio of 20%. King booked platform fees as a cost of revenue, so its reported revenue is gross, like our `a`. If every dollar of that spend bought installs whose net LTV exceeded their CAC by a comfortable margin, the spend was an investment, not a cost. The prospectus is the company's own description and shows only totals, so you cannot compute King's LTV from it. You can see the rule it describes, which is our payback inequality applied thousands of times a day.

**A subscription MMO.** Replace days with months and ARPDAU with the fee. For World of Warcraft's $15 one-month price, LTV is `15 × [R(0) + R(1) + ...]` in months. With an invented monthly curve `w = 0.4, qs = 0.9, qt = 0.3`, the expected lifetime is `0.4 / 0.1 + 0.6 / 0.7 = 4.86` months and the gross LTV is about $73. The model is identical. Only the meter changed, and a subscription's meter charges every active month the same amount, so its ARPDAU does not vary by player.

**The live-ops plateau (MMO308 week 1).** There, steady weekly installs `I` produce a plateau of `I × L` active players. Multiply both sides by net revenue per active period and you get **daily revenue at the plateau = installs per day × lifetime LTV.** A game at steady state earns, every day, exactly the lifetime value of one day's installs. So a studio that knows its LTV and its daily installs can predict its long-run revenue, and a change to LTV shows up in revenue only as fast as old cohorts are replaced.

**Software subscriptions.** Skok's rules of thumb for software-as-a-service businesses say LTV should exceed three times CAC, and months to recover CAC should be under 12, a figure he notes came from 2011 when capital was scarce. Our example at $1.50 passes the second rule easily (payback in about 2.3 months) and fails the first (1.28). The two rules measure different things. Payback measures how long your cash is tied up. The ratio measures how much margin is left for everything LTV does not count, such as development, overheads and the error in your LTV forecast.

Four contexts, one integral. In every case, value per unit is the area under a survival curve times the rate the meter charges.

### Eyes-open design judgment

- **Always state the horizon.** In the example, day-30 LTV is $0.99 and lifetime LTV is $1.93. A team that bids up to "LTV" using the lifetime number is betting on a tail it has not yet observed. A team using the day-30 number is leaving growth on the table. Pick a horizon deliberately and write it next to the number.
- **Predicted LTV is a forecast of the tail from the head.** Nobody waits a year to price installs. Teams fit a curve to the first days of a cohort and extrapolate. Section 2's sensitivity says the parameter that matters most (`qs`) is the one the first week shows least. Keep a margin, and re-fit as cohorts age.
- **LTV differs by channel.** Players bought through different ads are different people. An LTV averaged over organic and paid players overstates what the paid ones are worth. Lab 02 gives you four channels to price separately.
- **Discount money that arrives late.** A dollar in month 12 is worth less than a dollar today, if only because you could have spent today's dollar on more installs. For long tails, multiply each day's revenue by a discount factor. With the short lifetimes in this example the effect is small. For a subscription MMO whose players stay for years, it is not.
- **LTV is an upper bound for all spending on a player, not only ads.** Support, community management, events and anti-cheat are also paid out of it. A studio that spends its whole LTV on acquisition has nothing left to run the game.
- **Maximizing LTV is not the same as serving players.** Because the tail holds the money, an LTV-maximizing team is tempted to design for the heaviest, longest-staying spenders and to treat the rest as cost. The EU Consumer Protection Cooperation Network's 2025 principles on in-game currencies (week 3) explicitly warn against business models built on players willing to spend excessive amounts. Decide which parts of LTV you refuse to chase.

## 3. ARPPU, payer rate, and where the value sits

Section 2 held ARPDAU constant. It is a product, and each factor behaves differently.

```
ARPDAU = payer rate × ARPPU
$0.20  = 2%         × $10
```

Two ways to raise ARPDAU by 10%:

| Change | Payer rate | ARPPU | ARPDAU | Lifetime LTV |
|---|---|---|---|---|
| Baseline | 2.0% | $10.00 | $0.200 | $1.925 |
| More payers | 2.2% | $10.00 | $0.220 | $2.118 |
| Bigger baskets | 2.0% | $11.00 | $0.220 | $2.118 |

On paper they are identical. In practice they are not, for two reasons you will meet again in weeks 9 and 10. First, they reach different people. More payers spreads spending across more players, while bigger baskets concentrates it on those already paying. Second, they interact. Raising prices often lowers the payer rate, so a 10% price rise rarely produces a 10% ARPPU rise at a constant payer rate. Week 10 tests this with experiments.

ARPDAU also changes with player age. Tourists rarely pay. Stayers do. Suppose tourists' active days are worth $0.05 gross and stayers' $0.215, chosen so the lifetime average is still $0.20 per active day. Lifetime LTV is unchanged at $1.925, because it depends only on the total active days of each type. But the early curve is lower, because the first days are mostly tourists:

| Horizon | LTV, flat ARPDAU | LTV, ARPDAU by type |
|---|---|---|
| Day 0 | $0.140 | $0.064 |
| Days 0-7 | $0.436 | $0.324 |
| Days 0-30 | $0.989 | $0.919 |
| Days 0-90 | $1.647 | $1.626 |

Payback at a $1.50 CAC moves from day 70 to day 73. That is small here. It is large when you judge a campaign on its day-7 revenue, where the flat assumption overstates value by a third. The general rule is to estimate ARPDAU separately for the kinds of players in your cohort, and to be suspicious of any early LTV built on an all-player average.

## 4. Reading an LTV claim

When someone shows you an LTV, or you present one, check four things before you trust it.

1. **Gross or net?** Net of platform fees, net of refunds and chargebacks, and whether cost to serve is subtracted. A 30% fee alone separates gross from net by a factor of 1.43.
2. **Which horizon?** Day 30, day 180, 3 years, or "lifetime" extrapolated from a fitted curve. In the example these differ by a factor of two.
3. **Which cohort?** Organic, paid, a single channel, a single country, a launch week. Launch cohorts are unusual, as MMO308 week 1 showed.
4. **Measured or predicted?** How many days of data sit behind it, and what model filled in the rest.

A slide that says "LTV $4" answers none of these. "Net LTV at day 180 for paid installs from video ads in North America, cohorts of March to May, measured: $3.10; predicted lifetime: $4.00" answers all four.

## In-class activity (25 minutes)

In pairs. Materials: the interactive and the four-channel table in `labs/lab02-starter/channels.csv`.

1. (5 min) Enter the "video ads" row into the interactive. Record lifetime LTV, LTV/CAC, and the payback day.
2. (8 min) Do the same for the other three channels. Rank the channels by LTV/CAC and, separately, by payback day. Do the rankings agree?
3. (7 min) Your studio can spend $100,000 this month and needs every channel it funds to pay back within 120 days. Allocate the budget. Assume each channel's CAC stays fixed as you spend (it doesn't in reality; note one reason why).
4. (5 min) Write one sentence on the channel you refused to fund and why.

Expected output: a table of four channels with LTV, ratio and payback, your allocation, and the one-sentence refusal.

## Common misconceptions

- **"LTV is ARPU times lifetime."** Only when ARPU is constant over a player's life and retention is geometric. With a two-type curve and ARPDAU that grows with age, the early LTV is lower than that product suggests, and the horizon matters.
- **"A high day-1 retention means a high LTV."** Day-1 retention mostly measures tourists. In the example, raising `qt` from 0.40 to 0.60 adds about 9 cents to lifetime LTV, while lowering `qs` from 0.98 to 0.97 removes 58 cents.
- **"Blended CAC is what an install costs."** Blended CAC divides spend over all installs, including free organic ones, so it understates what the next paid install costs. Bid with paid CAC per channel.
- **"If LTV exceeds CAC, the business is profitable."** LTV net of fees does not include development, overheads, or the forecast error. That is why rules of thumb ask for a ratio well above 1.

## Check yourself

1. With the lecture's parameters, what is lifetime net LTV if the platform fee is 15% instead of 30%? What CAC now has a payback of exactly "never" (lifetime LTV equal to CAC)?
2. A game has `w = 0.20`, `qs = 0.99`, `qt = 0.50` and net ARPDAU of $0.10. Compute the expected active days per install and the lifetime LTV. What share of LTV comes from stayers?
3. Using the plateau identity, a game earns $50,000 a day at steady state and installs 20,000 players a day. What is its lifetime LTV? If a feature raises LTV by 10%, why won't daily revenue rise by 10% the next day?
4. Two campaigns cost $2.00 per install. Campaign A: lifetime LTV $3.00, payback day 150. Campaign B: lifetime LTV $2.60, payback day 45. Which would you fund if cash is tight, and which if it is not? Explain in one sentence each.

<details>
<summary>Answers</summary>

1. Net ARPDAU becomes `0.20 × 0.85 = $0.17`, and lifetime LTV `0.17 × 13.75 = $2.3375`. Any CAC above about $2.34 never pays back.
2. `L = 0.20 / 0.01 + 0.80 / 0.50 = 20 + 1.6 = 21.6` active days. LTV `= 21.6 × 0.10 = $2.16`. Stayers contribute `20 / 21.6 ≈ 93%`.
3. `LTV = 50,000 / 20,000 = $2.50`. Revenue rises only as new cohorts, which carry the higher LTV, replace old ones. The existing layers of the cake keep producing at the old rate until they wear away.
4. Cash tight: B, because the money comes back in 45 days and can be reinvested. Cash not tight: A, because it returns $1.00 per install over its life against B's $0.60, provided you trust the tail forecast behind day 150.

</details>

## Lab / assignment hook

[Lab 02, LTV curve and payback](../labs/lab02.md). You implement the LTV curve and payback day from a starter with tests, price four acquisition channels, and write a one-page acquisition plan that states horizon, fee basis and cohort for every LTV it uses. The LTV code is reused in the course's final business plan.

## Sources

- King Digital Entertainment plc, Form F-1/A, Amendment No. 3, filed with the US SEC on 25 March 2014 (file 333-193984). Revenue of $1,884.3 million in 2013 and $164.4 million in 2012; sales and marketing expenses of $376.9 million in 2013 and $55.2 million in 2012, primarily performance marketing for player acquisition; approximately 12 million monthly unique payers, about 4% of monthly unique users, as of 31 December 2013; thousands of campaigns every 24 hours subject to "the same target return parameters"; platforms typically charging about 30% of after-tax payments, recorded as cost of revenue.
- Apple Developer, "App Store Small Business Program" (developer.apple.com, accessed September 2026). Reduced commission of 15% for developers with up to $1 million in proceeds in the prior calendar year; standard rate 30%.
- Skok, D. "SaaS Metrics 2.0: A Guide to Measuring and Improving What Matters" (forEntrepreneurs.com, accessed September 2026). Guideline LTV to CAC above 3; months to recover CAC under 12, with his note that the 12-month guideline dates from 2011.
- GS101 week 11 and its sources. World of Warcraft's US one-month price of $15.
- MMO308 weeks 1 and 2. Two-type retention curve, the plateau `I × L`, and the KPI tree.
- Consumer Protection Cooperation Network, "Key Principles on In-game Virtual Currencies" (European Commission, published 21 March 2025). Principle 7 on business models targeting players who spend excessive amounts; see week 3.
- Fields, T. & Cotton, B. (2011). *Social Game Design: Monetization Methods and Mechanics*. Morgan Kaufmann.

## Interactive spec: examples/w02-ltv-curve.html

**Purpose.** Make visible that LTV is the area under the retention curve times net ARPDAU, and that the tail holds most of the value. Insight on first load: *the left curve loses half the cohort on day 1, while the right curve keeps climbing for months and crosses the CAC line on day 70.*

**Layout.** Two linked charts side by side on desktop, stacked on mobile (retention first). Controls below, then a numbers table. Generic visuals only.

**Left chart, retention.** x: day 0 to horizon `H` (default 180; a toggle for 365). y: `R(d)` from 0 to 1. Draw as a stacked filled area: stayer part `w × qs^d` (bottom) and tourist part `(1 − w) × qt^d` (top), in two colors with a hatch on the tourist part. A vertical cursor follows the pointer or keyboard focus; the area to the left of the cursor is highlighted.

**Right chart, cumulative LTV.** Same x. y: `LTV(T) = a (1 − f) Σ_{d=0}^{T−1} R(d)` in dollars, plotted at `T = d + 1` for each day `d`. A dashed horizontal line at CAC and a dotted horizontal line at lifetime LTV `a (1 − f) (w / (1 − qs) + (1 − w) / (1 − qt))`. Mark the payback day (first `d` with `LTV(d + 1) ≥ CAC`) with a vertical line and label "payback day N", or "no payback" if lifetime LTV < CAC. The cursor is shared: at day `d` the right chart shows a dot at `LTV(d + 1)` with the value, and the left chart's highlighted area.

**Controls.**
- `w` stayer share: 0.05 to 0.60, step 0.01, default 0.25.
- `qs` stayer daily survival: 0.90 to 0.995, step 0.001, default 0.980.
- `qt` tourist daily survival: 0.10 to 0.80, step 0.01, default 0.40.
- Gross ARPDAU `a`: 0.02 to 1.00, step 0.01, default 0.20.
- Platform fee `f`: 0 to 0.30, step 0.01, default 0.30 (presets 0.30, 0.15, 0).
- CAC: 0 to 5.00, step 0.05, default 1.50.
- Optional toggle "ARPDAU by type": when on, reveals tourist ARPDAU `t` (default 0.05) and computes stayer ARPDAU `s` so that the lifetime average per active day equals `a`: `s = (a L − t (1 − w) / (1 − qt)) × (1 − qs) / w`, where `L` is expected active days. The LTV curve then uses `(1 − f)(s w qs^d + t (1 − w) qt^d)`.

**Numbers panel.** `R(1)`, `R(7)`, `R(30)`; expected active days `L` and the stayer share of it; net ARPDAU; LTV at days 0-7, 0-30, 0-90, 0-180 (that is, `LTV(8)`, `LTV(31)`, `LTV(91)`, `LTV(181)`); lifetime LTV; LTV/CAC; payback day.

**Test values** (defaults unless stated).
- `R(1) = 0.545`, `R(7) = 0.2183`, `R(30) = 0.1364`. `L = 13.75`, stayer share 90.9%. Net ARPDAU $0.14.
- LTV: day 0 only $0.140; 0-7 $0.436; 0-30 $0.989; 0-90 $1.647; 0-180 $1.880; lifetime $1.925.
- Payback: CAC 0.50 → day 10; 1.00 → 31; 1.50 → 70; 1.75 → 113; 2.00 → no payback.
- `qs = 0.97`: lifetime LTV $1.342; CAC 1.50 → no payback. `qt = 0.60` (others default): `R(1) = 0.695`, lifetime $2.0125.
- Fee 0: lifetime $2.750. Fee 0.15: $2.3375.
- ARPDAU by type on, `t = 0.05`: `s = 0.215`; LTV day 0 $0.064, 0-7 $0.324, 0-30 $0.919, 0-90 $1.626; lifetime $1.925; payback at CAC 1.50 → day 73.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. Stayer and tourist areas differ by color and hatch. The cursor moves with arrow keys when a chart has focus, and the current day's values are announced in a live region. Respect reduced motion.

# MMO403 · Week 05 — Battle Passes

**Why this matters:** The battle pass is the most common way live games sell content today, and it is often praised as the fair alternative to loot boxes, because the player sees every reward before paying. What the player cannot see is the one number that decides how the pass feels and how much it earns: how many hours it takes to finish. This week you learn to set that number deliberately, and to see what each choice does to completion, tier sales and trust.

**You will be able to:**
- Compute the share of pass owners who finish, and the distribution of the tiers they reach, from a play-time distribution and the hours a pass requires.
- Derive where tier-purchase revenue peaks, and explain why that point leaves about half of paying players short.
- Compute the expected premium-currency rebate a pass returns and compare "pays for itself" claims across pass designs.
- Critique deadline, expiry and reward-return policies using the model.

**Before class:** Fields & Cotton, *Social Game Design: Monetization Methods and Mechanics* (Morgan Kaufmann, 2011), the chapters on retention and on time-limited offers. Wikipedia, "Battle pass" (read the history and criticism sections, about 1,500 words). Reread MMO308 week 8 on event pull-forward.

**Prerequisites from earlier courses:** [MMO308 week 8, event design and calendars](../../MMO308-live-operations-analytics-and-experimentation/lectures/w08-event-design-and-calendars.md) (deadlines pull play forward; we do not repeat the pull-forward model). [MMO308 week 3, cohorts and retention curves](../../MMO308-live-operations-analytics-and-experimentation/lectures/w03-cohorts-and-retention-curves.md). [MA102 week 12, descriptive statistics for playtests](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md) (skewed distributions, and why the median beats the mean for play time). [MA102 week 8, dice sums and the normal curve](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w08-dice-sums-and-the-normal-curve.md) (the normal CDF). From this course, [week 4, cosmetics vs power](w04-cosmetics-vs-power.md) (Overwatch 2's heroes on the pass) and [week 3, premium currencies](w03-premium-currencies.md).

**Interactive:** [The pass finish line](../examples/w05-pass-finish-line.html). Keep it open during section 2.

---

## 1. What a battle pass sells

A **battle pass** is a seasonal track of rewards. The player earns experience points (XP) by playing and completing challenges. Every fixed amount of XP unlocks the next **tier**, and each tier carries a reward. Most passes have two tracks. The **free track** gives a few rewards to everyone. The **premium track**, bought for a fixed price at any time in the season, unlocks the rest, including tiers already earned. When the season ends, most passes close and a new one begins.

The idea is older than its name. For The International 2013, Valve sold an in-game Compendium for *Dota 2* that unlocked content as players engaged with the tournament. A quarter of all Compendium revenue went into the tournament's prize pool, which grew from a base of $1.6 million to over $2.8 million. *Fortnite Battle Royale* adopted the name "Battle Pass" in its second season and made the format the standard for free-to-play games from 2018 onward.

Compare the pass with the products from weeks 3 and 6. A loot box sells a random draw. A store sells a fixed item. A pass sells something different: **a list of rewards, fully visible, whose delivery depends on how much you play before a deadline.** The price is fixed. What varies is how much of the list each player receives. That variation is the design question, and it is set by two numbers:

- `H*`, the **hours to finish**: how much play the full track requires, given the XP per tier and the XP a typical hour of play earns.
- The distribution of how many hours each pass owner will actually play this season.

The rest of this lecture is about the relationship between those two.

## 2. Worked example: where to put the finish line

### The hook

For years, a *Fortnite* Battle Pass bought for 950 V-Bucks (1,000 from Chapter 6 Season 1, December 2024) returned up to 1,500 V-Bucks to a player who worked through it. Players summed that up as "the pass pays for itself". On 19 March 2026, with Chapter 7 Season 2, Epic raised the real-money price of V-Bucks, cut the pass to 800 V-Bucks, and cut the V-Bucks it returns to 800. A finisher now breaks even instead of coming out ahead.

That change raises a question the old slogan hid. "Pays for itself" was only ever true for players who reached the tiers where the V-Bucks sat. How many of them was that? And who decides? Epic's players can also buy levels directly, at 150 V-Bucks each, which means every player who ends the season a few tiers short is a potential sale. The designer who sets `H*` is setting the number of such players.

### The model

We need a distribution of play time and a rule for tiers.

**Play time.** Let `H` be the hours a pass owner plays during the season. Play time is always skewed: most players play a moderate amount, a few play enormously. A good first model is the **lognormal** distribution, where `ln H` is normal. It has two parameters:

- `m`, the median play time. Half of owners play less, half play more.
- `s`, the spread of `ln H`. `s = 0.7` means the middle two-thirds of owners play between about half and double the median.

The share of owners who play at least `h` hours is

```
P(H ≥ h) = 1 − Φ( ln(h / m) / s )
```

where `Φ` is the standard normal CDF.

**Tiers.** The track has `N` tiers. The whole track needs `H*` hours, so each tier takes `H* / N` hours. An owner who plays `H` hours ends on tier

```
T = min( N, floor( N × H / H* ) )
```

So the **finish share**, the fraction of owners who complete the track, is `P(H ≥ H*)`. It is exactly 50% when `H* = m`.

**Tier sales.** Suppose owners who end 1 to `G` tiers short consider buying the rest, and a share `q` of them do, at price `c` per tier. The coins earned per 1,000 owners are

```
tier revenue = 1000 × q × c × Σ_{k=N−G}^{N−1} (N − k) × P(T = k)
```

**Rebate.** If the pass returns `R` coins of premium currency spread evenly over the track, an owner on tier `T` has received `R × T / N`. The expected rebate is `R × E[T] / N`.

For the example we use `N = 100` tiers, median play time `m = 40` hours, spread `s = 0.7`, near-miss window `G = 10` tiers, purchase share `q = 30%` and tier price `c = 150` coins. These are teaching assumptions, not any game's data. The code below runs as shown with `.venv/bin/python`.

```python
from math import erf, log, sqrt

MEDIAN_HOURS, SPREAD = 40.0, 0.7   # pass owners' season play time, lognormal
TIERS, GAP, BUY_SHARE, TIER_PRICE = 100, 10, 0.3, 150

def share_playing_at_least(h):
    """Fraction of pass owners who play at least h hours this season."""
    return 1.0 if h <= 0 else 0.5 * (1 - erf(log(h / MEDIAN_HOURS) / (SPREAD * sqrt(2))))

def season(hours_to_finish, rebate=1500):
    step = hours_to_finish / TIERS                      # hours per tier
    reach = [share_playing_at_least(k * step) for k in range(TIERS + 1)]
    ends_at = [reach[k] - reach[k + 1] for k in range(TIERS)]   # P(final tier = k)
    finish = reach[TIERS]
    mean_tier = sum(k * p for k, p in enumerate(ends_at)) + TIERS * finish
    near = sum(ends_at[TIERS - GAP:])                   # 1 to 10 tiers short
    tiers_short = sum((TIERS - k) * ends_at[k] for k in range(TIERS - GAP, TIERS))
    skip_coins = 1000 * BUY_SHARE * TIER_PRICE * tiers_short   # per 1,000 owners
    returned = rebate * mean_tier / TIERS               # rebate spread evenly
    return finish, mean_tier, near, skip_coins, returned

print("hours  finish  mean tier  near miss  skip coins/1000  rebate back")
for h in (20, 30, 40, 50, 60, 80, 100):
    f, t, n, s, r = season(h)
    print(f"{h:5}  {f:6.1%}  {t:9.1f}  {n:9.1%}  {s:15,.0f}  {r:11.0f}")
```

### Numbers you can check

Output:

```
hours  finish  mean tier  near miss  skip coins/1000  rebate back
   20   83.9%       95.4       3.4%            8,357         1432
   30   65.9%       88.5       5.3%           13,259         1327
   40   50.0%       80.7       6.0%           15,015         1210
   50   37.5%       73.1       5.8%           14,722         1097
   60   28.1%       66.3       5.3%           13,435          994
   80   16.1%       54.9       4.0%           10,133          824
  100    9.5%       46.3       2.8%            7,249          695
```

Check one row by hand. At `H* = 60`, `ln(60/40) = 0.405`, divided by `0.7` gives `z = 0.579`. `Φ(0.579) = 0.719`, so 28.1% of owners finish. At `H* = 40`, `z = 0` and exactly half finish.

Now read the table as a designer.

**Completion falls fast, then slowly.** Moving the finish line from 20 to 40 hours drops completion from 84% to 50%. From 60 to 100 hours it drops from 28% to 9.5%. The steepest part is around the median, because that is where most players are.

**Tier sales peak at the median.** The skip-revenue column rises from 8,357 coins at 20 hours to about 15,000 at 40, then falls again. Search every whole hour and the peak is at 43 hours, where 46% of owners finish. Anywhere from 37 to 50 hours earns within 3% of the peak. The reason is simple once you see the chart. Tier sales come from owners who end the season just short. The most owners end just short when the finish line sits where the most owners are, which for a skewed distribution is close to the median on the log scale.

That is the uncomfortable result. **The finish line that sells the most tiers is the one that leaves about half of paying players unable to finish by playing.** A designer who tunes the pass purely for tier revenue will land there without ever deciding to.

**The rebate goes to the players who play.** With a 1,500-coin rebate spread evenly, an owner at `H* = 40` receives 1,210 coins on average, more than a 950-coin price. But the median owner reaches tier 100 only at exactly 40 hours, and an owner who plays 20 hours gets 750. Cut the rebate to 800, as Fortnite did in 2026, and the average owner receives 645 at `H* = 40` (run `season(40, 800)`). "Pays for itself" is a claim about finishers, and the table tells you what share of owners that is.

### Move it yourself

Open `examples/w05-pass-finish-line.html`. The left view is the player's view: a histogram of the tier each pass owner ends the season on, with a spike at tier 100 for finishers and a shaded band for the near-miss owners. The right view is the business view: tier revenue and finish share plotted against `H*`, with a marker at your current setting. Drag `H*` from 20 to 100 hours. On the left the spike at tier 100 shrinks and the near-miss band first grows, then empties. On the right the revenue curve peaks just as the finish share crosses the 50% line. Change the median play time, and the peak moves with it.

### Cross-game recognition

**Dota 2, The International Compendium (2013 onward).** The Compendium was the first pass, and its rewards unlocked by level. Because a quarter of revenue went to the prize pool, players who bought levels were also funding a tournament they watched. In our model the tier purchases (`q × c`) had a second, public purpose, which made buying the gap feel like support rather than a shortfall. The structure is the same. The framing changed how players read it.

**Halo Infinite (2021 onward).** The multiplayer launched with a pass whose progress was widely criticized as too slow, and 343 Industries adjusted it soon after. Its passes also **do not expire**. Players can keep earning through a pass they own after its season ends, with one pass active at a time. In our model, removing the deadline removes the season length from `H`. Every owner who keeps playing will eventually finish, so the near-miss band never forms and tier purchases lose their deadline. What is left is a sale of speed. Wikipedia's survey of battle passes lists Helldivers 2 and Marvel Rivals as taking the same approach.

**Fortnite (2018 onward).** Beyond the rebate change, Fortnite announced in August 2024 that battle pass cosmetics from Chapter 5 Season 4 onward may return to the Item Shop at least 18 months after their pass ends. That softens the other half of the deadline, the fear that an item missed now is gone forever. It does not change `H*` or the tier distribution. It changes what a near-miss costs the player.

Three games, one model. The designer controls `H*`, the deadline, and what happens to the unfinished part.

### Design judgment

- **Set a completion target before you set XP values.** Decide what share of owners should finish by playing, then compute `H*` from your play-time data. If you pick 50%, pick it knowing it is also the revenue peak, and say so in the design review.
- **Measure play time on pass owners, not all players.** Owners play more than non-owners. Using the whole population's median will set `H*` too low for owners and change every number in the table. Segment exactly as MMO308 week 7 taught.
- **Put the rebate where it helps the players you want to keep.** Currency placed early in the track reaches almost every owner. Currency placed at tier 100 reaches only finishers and makes the rebate a reward for play time. Both are defensible. The second is also a reason for the median owner to buy tiers.
- **Expiry is a separate lever from difficulty.** A long track with no expiry is a sale of speed. A short track with expiry is a sale of time pressure. Pick the combination on purpose, and read week 8 before you add countdown timers.

### Check this example

1. With `m = 40` and `s = 0.7`, what `H*` gives an 80% finish share? (Use `Φ(−0.842) = 0.20`.)
2. An owner plays 30 hours in a season with `H* = 50`. Which tier do they reach, and how many 150-coin tiers would they need to buy?

<details>
<summary>Answers</summary>

1. Need `P(H ≥ H*) = 0.8`, so `ln(H*/40) / 0.7 = −0.842`, `H* = 40 × e^(−0.589) = 40 × 0.555 = 22.2` hours.
2. `T = floor(100 × 30 / 50) = 60`. They are 40 tiers short, 6,000 coins. That is far outside a 10-tier near-miss window, which is why owners that far behind rarely buy.

</details>

## 3. The rebate and the next season

A pass that returns premium currency does more than make the price feel smaller. It changes what happens next season.

Suppose the rebate equals or exceeds the next pass's price. A finisher can buy the next pass without spending money. That sounds like lost revenue, and for that player it is. But the player's decision next season becomes "keep playing" rather than "pay again", which is a much easier decision. The pass turns a repeat purchase into a retention mechanic. MMO308 week 3's cohort curves are where you would see the effect: owners who finish one pass start the next at a higher rate.

Three things follow.

**The rebate is a loan against next season's play.** A finisher who returns spends nothing and keeps playing, and the studio earns on their other purchases and on the players they bring along. A finisher who does not return has taken currency and left. The value of the rebate depends on the return rate, which you should measure per finisher cohort.

**Cutting a rebate changes the deal for the most engaged players.** Fortnite's 2026 change moved a finisher from 500 V-Bucks ahead (at the 1,000-coin price) to exactly even. Those are the players who play most. Before cutting a rebate, forecast the change in their return rate and their store spending as well as the currency saved.

**Rebates are often the real price of the next pass.** If a player finishes most seasons, the pass costs them nothing after the first. If they finish some, each season is a gamble on their own play time. The model gives the probability, and in the lab you compute the expected cost of a year of passes for owners with different play times.

## 4. Deadlines, FOMO and what players read as fair

**Fear of missing out (FOMO)** is the worry that a reward available now will be unavailable later. Battle passes rely on it by design: the deadline is what makes the season a season. The criticism, summarized in the Wikipedia survey of passes, is that the deadline pushes players to play past the point of enjoyment and to buy tiers to avoid losing what they have already paid for.

Both parts of that criticism map onto the model.

- **Playing past enjoyment** is the owners just below `H*` who push to finish. You can see them in the data as a bulge of play time in the last week of a season, the same pull-forward MMO308 week 8 measured for events.
- **Buying to avoid loss** is the near-miss band. The model shows it is largest when `H*` sits at the median.

Neither is a reason to abandon passes. A pass with a clear list of rewards, a fixed price, a finish line most owners reach and no hidden odds is one of the more transparent products a live game can sell. Players also value the structure: a season gives them goals and a reason to return with friends. The design question is the size of the pressure, not its existence.

Practical ways to set it:

1. **Publish `H*`.** Tell players roughly how many hours the track takes. Some studios show expected completion at a given play rate. Players who know the size of the commitment can decide whether to buy.
2. **Put catch-up XP in the last weeks.** Bonus XP for players behind the expected pace narrows the near-miss band without cutting the finish line for everyone.
3. **Choose expiry deliberately.** Non-expiring passes (Halo Infinite) remove deadline pressure. Returning items later (Fortnite's 18-month policy) removes permanent loss. Both cost some urgency.
4. **Keep power off the pass,** or keep it earnable on the free track at a pace that does not matter competitively. Week 4 covered what happened when Overwatch 2 put new heroes on its pass.

## In-class activity (25 minutes)

Work in pairs. Your MMO's pass has 80 tiers. Telemetry from last season shows pass owners played a median of 32 hours with spread `s = 0.8`. Tier purchases cost 120 coins; assume `G = 8` and `q = 30%`.

1. Edit the code's constants and find the `H*` that maximizes tier revenue. Report the finish share there.
2. Find the `H*` that gives a 70% finish share. How much tier revenue per 1,000 owners do you give up compared with step 1?
3. Your producer asks for the revenue-maximizing setting. Write a four-sentence reply that states the trade-off in numbers and recommends one setting.
4. Propose one change from section 4 and predict, qualitatively, which column of the table it moves.

Expected output: two rows of the table, the reply, and one change with its predicted effect.

## Common misconceptions

- **"A battle pass pays for itself."** Only for players who reach the tiers holding the currency. With `H*` at the median, half of owners do not finish.
- **"Longer passes earn more from tier sales."** Tier revenue peaks near the median owner's play time. Past that, fewer owners are close enough to buy.
- **"Set `H*` from average play time."** Play time is skewed, so the mean sits above the median and overstates the typical owner. Use the median, measured on pass owners.
- **"Visible rewards make a pass immune to pressure tactics."** The rewards are visible. The pressure comes from the deadline and the finish line, which the player cannot see unless you publish them.

## Check yourself

1. A pass needs `H* = 50` hours. Owners' play time has median 40 hours and `s = 0.5`. What share finish? Compare with the `s = 0.7` row of the table and explain the difference.
2. A pass returns 1,000 coins spread evenly over 100 tiers and costs 950. What is the smallest tier at which an owner has received more than the price? If `H* = 60` with `m = 40` and `s = 0.7`, what share of owners reach that tier? (Use `Φ(0.521) = 0.699`.)
3. Your team switches to a non-expiring pass. Which terms in the tier-revenue formula change, and why does the near-miss band disappear?
4. Explain, with the model, why tier revenue peaks close to the median play time and not at a very long `H*` where nearly every owner is short.

<details>
<summary>Answers</summary>

1. `z = ln(50/40) / 0.5 = 0.223 / 0.5 = 0.446`, `Φ(0.446) = 0.672`, so 32.8% finish, versus 37.5% with `s = 0.7`. A narrower spread means fewer owners far above the median, so when the finish line is above the median, fewer clear it.
2. `1000 × T / 100 > 950` needs `T ≥ 96`. Reaching tier 96 needs `0.96 × 60 = 57.6` hours. `ln(57.6/40) / 0.7 = 0.365 / 0.7 = 0.521`, and `1 − Φ(0.521) = 1 − 0.699`, so 30.1% of owners reach it.
3. With no season end, `H` is no longer capped by the season, so every owner who keeps playing eventually reaches tier `N`. `P(T = k)` for `k < N` falls toward zero over time and the sum over the near-miss window shrinks. Tier purchases then buy speed, not rescue from a deadline.
4. Tier sales come only from owners who end 1 to `G` tiers short. That band is a thin slice of play time just below `H*`. The number of owners in a thin slice is largest where the distribution is densest, which for a lognormal on the log scale is the median. At a very long `H*`, most owners are short by far more than `G` tiers and do not buy.

</details>

## Lab / assignment hook

[Lab 05, tune a battle pass](../labs/lab05.md). You implement the finish-share, tier-distribution, tier-revenue and rebate functions, fit them to a generated season of pass-owner play time, and then choose `H*`, rebate placement and one pressure-reducing rule for a pass. Your memo states the trade-off in numbers. The model feeds the models assignment (40%).

## Sources

- Wikipedia, "Battle pass" (accessed September 2026). Origin in the Dota 2 Compendium for The International 2013; Fortnite's adoption from its second season; criticism on FOMO and sunk cost; Halo Infinite's slow-progression criticism and adjustment; non-expiring passes in Halo Infinite, Helldivers 2 and Marvel Rivals; Fortnite's August 2024 18-month return policy.
- Wikipedia, "The International 2013" and "The International (esports)"; Liquipedia Dota 2, "The International/2013" (accessed September 2026). Base prize pool $1.6 million; 25% of Compendium sales added; final pool over $2.8 million.
- Fortnite Wiki (fortnite.fandom.com), "Battle Pass" (accessed September 2026, current season Chapter 7 Season 4). Price history 950, then 1,000 V-Bucks (Chapter 6 Season 1, from 1 December 2024), then 800 (Chapter 7 Season 2); total V-Bucks obtainable reduced from 1,500 to 800 in Chapter 7 Season 2; levels purchasable at 150 V-Bucks each.
- Fortnite Wiki, "Chapter 7: Season 2" and "V-Bucks" (accessed September 2026). Season ran 19 March to 5 June 2026; V-Bucks real-money price raised on 19 March 2026 (citing Epic's news post "Fortnite V-Bucks price increase"); current 800 V-Bucks bundle at $8.99 USD.
- Epic Games, "Fortnite V-Bucks price increase" (fortnite.com news, March 2026, read via the Internet Archive copy of 10 March 2026). From 19 March 2026 the Battle Pass costs 800 V-Bucks and awards 800 V-Bucks on completion; previously it cost 1,000 and paid 1,000 plus 500 in bonus rewards; the $8.99 pack now gives 800 V-Bucks.
- Wikipedia, "Halo Infinite" (accessed September 2026). Criticism of slow battle pass progression in 2021 and 343 Industries' adjustment.
- Fields, T. & Cotton, B. (2011). *Social Game Design: Monetization Methods and Mechanics*. Morgan Kaufmann.
- The lognormal play-time distribution, its parameters, the near-miss window and the purchase share are teaching assumptions, not measurements from any game.

## Interactive spec: examples/w05-pass-finish-line.html

**The one insight.** Tier-purchase revenue peaks when the finish line sits near the median owner's play time, which is exactly where about half of paying owners fail to finish by playing.

**Layout.** Two linked views side by side at 1280px, stacked at 390px. Left: "Where owners end the season", a histogram of final tier `T` (0 to `N`) as a share of owners, bins of 5 tiers plus a separate bar for tier `N` (finishers), with the near-miss band `N − G ≤ T < N` shaded and hatched. Right: "What the finish line earns", two curves against `H*` from 10 to 150 hours: tier revenue per 1,000 owners (left axis) and finish share (right axis, 0 to 100%), a horizontal dashed line at 50% finish share, a vertical marker at the current `H*`, and a small dot at the revenue peak.

**Controls (all update instantly).**
- Hours to finish `H*`, 10 to 150, step 1, default 40.
- Median play time `m`, 10 to 100 hours, step 1, default 40.
- Spread `s`, 0.3 to 1.2, step 0.05, default 0.7.
- Tiers `N`, 50 to 150, step 10, default 100.
- Near-miss window `G`, 1 to 20, default 10. Purchase share `q`, 0% to 100%, default 30%. Tier price `c`, default 150.
- Rebate `R`, 0 to 2,000, step 50, default 1,500; pass price, default 950. Rebate placement toggle: "spread evenly" (default) or "all at the final tier".
- Reset button.

**Formulas.**
- `P(H ≥ h) = 0.5 × (1 − erf( ln(h/m) / (s √2) ))`, with `P(H ≥ 0) = 1`.
- `reach_k = P(H ≥ k × H*/N)` for `k = 0..N`; `P(T = k) = reach_k − reach_{k+1}` for `k < N`; `P(T = N) = reach_N`.
- Finish share `= reach_N`. Mean tier `= Σ k P(T = k) + N × reach_N`. Near-miss share `= Σ_{k=N−G}^{N−1} P(T = k)`.
- Tier revenue per 1,000 owners `= 1000 × q × c × Σ_{k=N−G}^{N−1} (N − k) P(T = k)`.
- Rebate, evenly spread: `R × mean tier / N`. All at the final tier: `R × reach_N`. Net cost to the average owner = price − rebate.
- Peak: evaluate tier revenue at every whole `H*` from 10 to 150 and mark the maximum.

**Readouts.** Finish share, mean tier (one decimal), near-miss share, tier revenue per 1,000 owners (whole coins), revenue-peak `H*` and the finish share there, average rebate and net cost. When `H*` is within 3% of peak revenue, print "Near the revenue peak: X% of owners finish by playing."

**Test values.**
- Defaults: finish 50.0%, mean tier 80.7, near miss 6.0%, tier revenue 15,015, rebate back 1,210, net cost −260. Peak at `H* = 43`, finish share 45.9%, revenue 15,086.
- `H* = 20`: finish 83.9%, mean tier 95.4, revenue 8,357.
- `H* = 60`: finish 28.1%, mean tier 66.3, revenue 13,435.
- `H* = 100`: finish 9.5%, mean tier 46.3, revenue 7,249.
- Defaults with `R = 800`: rebate back 645. With `R = 1,500` at the final tier: rebate back 750.

**Accessibility and style.** Native range inputs with visible labels and numeric outputs; the near-miss band is hatched as well as colored; both curves have direct labels. Colors from `templates/interactive-tokens.css`. No game art or logos.

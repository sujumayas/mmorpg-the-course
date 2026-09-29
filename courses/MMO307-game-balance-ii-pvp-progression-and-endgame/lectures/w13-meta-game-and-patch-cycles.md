# MMO307 · Week 13 — Meta-Game and Patch Cycles

**Why this matters:** Every competitive game solves itself. Players share what wins, the population piles onto it, and a game with forty viable builds starts to feel like a game with four. Your patch calendar is how you fight that, and every patch costs players time to relearn. This week gives you a model for deciding how often to patch, and for recognizing when patching is the wrong tool.

**You will be able to:**
- Compute the average meta diversity over a patch cycle from a settling model, and the share of the cycle a meta spends settled.
- Estimate a meta's settling time from post-patch pick data, by hand from two points and by least squares in code.
- Compare patch cadence against scheduled perturbations and a healthier settled meta as ways to keep a game varied, using numbers.
- Critique a patch calendar by naming the settling time it assumes and the cost it puts on players.

**Before class:** Schreiber & Romero, *Game Balance* (2021), the chapter on the balance process after launch. Reread [MMO303 week 9, section 2](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w09-intransitivity-and-counters.md) ("How the population gets there") and [MMO303 week 10, section 4](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w10-game-theory-payoff-matrices-and-nash-equilibria.md) (the meta as a population). About 40 minutes in total.

**Prerequisites from earlier courses:** [MMO303 week 1](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w01-what-balanced-means.md) (the effective number of classes, `N_eff = 1 / Σ p²`, which this week uses as its measure of diversity). [MMO303 week 9](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w09-intransitivity-and-counters.md) and [week 10](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w10-game-theory-payoff-matrices-and-nash-equilibria.md) (replicator drift and why the population moves after a patch). [MMO303 week 14](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w14-communicating-balance-changes.md) (how a patch is communicated). From this course, [week 7](w07-pvp-vs-pve-split-tuning.md) (split tuning) and [week 11](w11-seasonal-structures-and-resets.md) (seasons and resets).

**Interactive:** [`examples/w13-patch-cadence.html`](../examples/w13-patch-cadence.html). Open it for section 2.

---

## 1. What a meta is, and why it solves itself

The **meta** (short for metagame) is two things at once. It is the set of strategies players believe are best right now, and it is the shares of play those strategies actually receive. The belief drives the shares. A tier list on a website is a statement of belief. The pick-rate table in your telemetry is the shares.

In MMO303 you studied the meta as a population that drifts toward an equilibrium. Week 9 moved shares week by week with the replicator rule `share × (1 + η × E)`. Week 10 showed that in a pure counter triangle the population orbits the equilibrium, and that friction (players who stick with a favorite) damps the orbit. This week takes that population and asks a live-operations question. The equilibrium itself is often narrow, so reaching it is the problem. How fast does the population get there, and what should you do about it?

Watch any competitive game across one patch and you see the same four phases.

1. **Shock.** The patch lands. Nobody knows what is best. Players try old favorites, new buffs and whatever a streamer played last night. Diversity is high.
2. **Discovery.** Win-rate sites, guides and forum threads start to agree. A few builds pull ahead in the data.
3. **Convergence.** Players copy what the data says wins. Shares of the top builds climb. Diversity falls fast.
4. **Settled.** The population sits near the equilibrium of the current numbers. Diversity is low and stable. Players describe this as "solved" or "stale."

A settled meta is not necessarily unbalanced. MMO303 week 1 separated fairness, viability and diversity, and showed that they come apart. A settled meta can be perfectly fair, with every played option winning about half its games, while offering only four options that anyone plays. Staleness is a diversity problem, and it gets worse with time even when nothing about the numbers changes.

The speed of phases 2 and 3 is not a property of your design alone. It depends on how many players there are, how much each one plays, how complex the choice space is, and above all how fast information moves. A game with public win-rate sites, in-client build imports and a large streaming audience converges in days. The same game in 2005, with forum posts as the only data, took weeks. You do not control that speed, but you can measure it.

## 2. Worked example: how often should you patch?

### The hook

In 2026, Riot Games scheduled 24 patches for League of Legends, from 26.01 on January 8 to 26.24 on December 9, and most of them landed two weeks apart. Valve's Dota 2 moves at a very different pace. Its numbered gameplay updates from 7.34 (August 8, 2023) to 7.40 (December 15, 2025) arrived 70 to 208 days apart. Smaller lettered patches land in between. For example, 7.35 on December 14, 2023 was followed by 7.35b a week later, 7.35c in February and 7.35d in March 2024.

Both are large, long-running competitive games. One patches every fortnight and the other makes its big changes two or three times a year. They can't both be following one "correct" cadence, unless the correct cadence depends on something that differs between the games. It does. The number it depends on is how fast the meta settles.

### The model

Measure diversity with MMO303 week 1's effective number of strategies, `N_eff = 1 / Σ p_i²`, computed from pick shares each day. Call it `D(t)` for day `t` after a patch. Model the settling as exponential decay toward the settled value:

```
D(t) = D_s + (D_0 − D_s) × e^(−t/τ)
```

- `D_0` is the diversity on the day of the patch (the shock).
- `D_s` is the settled diversity, where the population ends up if nobody patches again. It is a property of the game's equilibrium.
- `τ` (tau) is the **settling time** in days. After `τ` days, 63% of the gap between `D_0` and `D_s` has closed. After `2τ`, 86%. After `3τ`, 95%. The half-life is `τ × ln 2 ≈ 0.69τ`.
- `D_0 − D_s` is the **gap**, the diversity a patch buys you.

Why exponential? Near the equilibrium, the replicator drift from MMO303 week 9 shrinks each class's distance from its equilibrium share by roughly the same fraction every day. A fixed fraction per step is exponential decay. Friction and imitation change the rate, and they change `τ`, but not the shape. Treat this as a fitted model, not a law. Section 3 shows how to check the fit.

Now patch every `T` days, and assume each patch resets diversity to `D_0`. Diversity then traces a sawtooth: a spike at every patch, then decay. The number that matters to players is the average diversity they experience across the whole cycle. Integrate `D(t)` from 0 to `T` and divide by `T`:

```
D̄(T) = D_s + (D_0 − D_s) × (τ/T) × (1 − e^(−T/τ))
```

Two limits make sense of it. When you patch far more often than the meta settles (`T` much smaller than `τ`), the bracket `(τ/T)(1 − e^(−T/τ))` approaches 1 and the average approaches `D_0`, since players never leave the shock phase. When you patch rarely (`T` much larger than `τ`), the bracket approaches `τ/T` and the average sinks toward `D_s`.

One more quantity is useful. Call the meta **settled** once 90% of the gap has closed. That happens at `t = τ × ln 10 ≈ 2.3τ`. The share of each cycle spent settled is `(T − 2.3τ) / T`, or zero if `T` is shorter than `2.3τ`.

### Numbers you can check

Take an invented eight-class PvP ladder, the one your lab uses. On patch day `D_0 = 12` (players try more than the eight classes, because specs and builds count as strategies). It settles to `D_s = 4`, and it settles with `τ = 7` days.

First, the decay within one cycle:

| Day after patch | `D(t) = 4 + 8e^(−t/7)` |
|---|---|
| 0 | 12.00 |
| 3 | 9.21 |
| 7 | 6.94 |
| 14 | 5.08 |
| 21 | 4.40 |
| 28 | 4.15 |

Now the cycle average for different patch intervals:

| Patch every `T` days | Patches per year | `D̄(T)` | Share of cycle settled |
|---|---|---|---|
| 1.75 | 209 | 11.08 | 0% |
| 3.5 | 104 | 10.30 | 0% |
| 7 | 52 | 9.06 | 0% |
| 14 | 26 | 7.46 | 0% |
| 28 | 13 | 5.96 | 42% |
| 56 | 6.5 | 5.00 | 71% |
| 90 | 4.1 | 4.62 | 82% |
| 180 | 2.0 | 4.31 | 91% |

Check one row by hand. For `T = 14`, `T/τ = 2`, so `D̄ = 4 + 8 × 0.5 × (1 − e^(−2)) = 4 + 4 × 0.8647 = 7.46`. For the settled share at `T = 28`, `2.3τ = 16.1` days, so `(28 − 16.1) / 28 = 42%`.

Read the table from the bottom up. Going from 2 patches a year to 4 buys 0.31 effective strategies. Going from 6.5 to 13 buys 0.96. Going from 13 to 26 buys 1.50. Doubling again from 26 to 52 patches a year buys 1.60, the biggest step in the table, but it takes 26 extra patches to buy it, so each patch buys about half as much as in the step before. Doubling from 52 to 104 buys only 1.24, and the returns keep falling. The curve is steepest when `T` is between about `τ` and `3τ`. Much faster than `τ`, you pay for patches that interrupt a meta that has not moved yet. Much slower than `3τ`, the game spends most of its life settled.

### A visual you can move

Open [`examples/w13-patch-cadence.html`](../examples/w13-patch-cadence.html). The left view shows the sawtooth `D(t)` over 180 days for your chosen patch interval. The right view plots `D̄(T)` against `T`, with a marker at your current setting. Drag the interval slider from 90 days down to 3. The sawtooth on the left gets busier and busier and looks healthier every time. The curve on the right shows that past the knee near `T = τ`, all that extra motion buys little average diversity. Then change `τ`. The whole right-hand curve slides sideways, and the knee moves with it.

### Why only `T/τ` matters

Look at the formula again. `T` and `τ` appear only as the ratio `T/τ`. So a game with `τ = 7` patched every 28 days has exactly the same average diversity as a game with `τ = 3.5` patched every 14 days. Both have `T/τ = 4` and `D̄ = 5.96`.

This is the answer to the hook. A cadence is not fast or slow in days. It is fast or slow relative to the settling time. A studio that patches every two weeks is betting that its meta settles in about a week. A studio that makes big changes every three to six months is betting on a much longer `τ`, or on a small gap (a settled meta that stays diverse), or it accepts long settled stretches in exchange for stability. Those are different bets, and neither is wrong until you know the numbers.

It also predicts a trend. Better information tools shorten `τ`. If a new stat site halves your game's settling time, then to keep the same average diversity you must halve `T`, which means patching twice as often. Studios feel this as pressure to patch more often as their community's tools improve.

### Cross-game recognition

**League of Legends (2026 schedule).** Twenty-four patches, most of them two weeks apart, under the `YEAR.PATCH` naming Riot uses, so 26.01 is the first patch of 2026. In model terms, `T = 14` days. If the model holds, Riot is working with a `τ` of a week or less. That is plausible for a game with a very large ranked population and many public statistics sites.

**Dota 2 (7.34 to 7.40, August 2023 to December 2025).** Numbered updates arrived 128, 160, 70, 203, 91 and 208 days apart. The lettered patches in between (7.35b to 7.35d, 7.36a to 7.36c and so on) arrived every few weeks. This is a **two-level cadence**, and the model separates the two levels cleanly. A numbered update is a large shock that raises `D_0` a long way. A lettered patch is a small adjustment that mostly nudges which classes sit in the settled mix, so it changes `D_s` without resetting the cycle. Valve's calendar only makes sense if large shocks are expensive for players to absorb, and if the long settling time of a large update is part of the design.

**World of Warcraft Mythic+ (since patch 7.0.3, Legion, 2016).** Mythic+ dungeons carry **affixes**, modifiers that change enemy behavior or dungeon mechanics. The affixes are the same for all players in a given week and rotate on a schedule. That rotation is a patch without a patch. Each week the best group composition and route shift, so the settled state rotates. In model terms it is a scheduled perturbation with a period of seven days and almost no development cost per cycle. The affix list and the keystone levels at which affixes switch on have changed many times since Legion, so cite the season when you use a specific one. The catch is that a rotation repeats, and players eventually solve the whole rotation as well as each week.

**MMO303 week 9's counter triangle.** A pure counter triangle keeps cycling without any patch. That is a meta whose settled state is a moving orbit, not a point. Designing counters into a game is a way to raise `D_s` itself, which section 4 comes back to.

Four cases, one idea. Each one sets a period of disruption against a settling speed.

### Eyes-open design judgment

- **Patching is not free, and the model hides the cost.** Every patch makes players relearn, makes guides and videos go stale and adds bug risk. It also invites the "chasing the meta" error from MMO303 week 10, where you nerf a class during its post-patch surge and move the equilibrium again before the population has settled. Plot `D̄(T)` next to the number of patches per year, and ask what the last doubling actually bought.
- **The gap `D_0 − D_s` is a design choice.** A bigger shake-up buys more diversity per patch, and it costs players more to absorb. Small patches keep `D_0` modest and are easier to live with.
- **Raising `D_s` beats patching faster.** Compare two options for the lecture's game. Patching every 28 days with `D_s = 4` gives `D̄ = 5.96`. Patching every 90 days with a better equilibrium, `D_s = 6`, gives `D̄ = 6.47`, and the second option needs a third as many patches. A healthier equilibrium, built from counters (MMO303 weeks 9 and 10) and horizontal options ([GD203 week 14](../../GD203-combat-and-progression-design/lectures/w14-horizontal-vs-vertical-progression.md)), works every day of the cycle.
- **Scheduled perturbation is cheap diversity.** Map rotations, weekly affixes and seasonal modifiers change the optimum without a balance pass. They are best for PvE and for modes where players accept that the rules change. In a ranked mode, players may read them as noise.
- **Measure `τ`. Don't assume it.** It changes over a game's life as the audience and its tools change. Refit it every few patches.

## 3. Measuring the settling time

You can estimate `τ` from any two days of post-patch data if you know `D_s`. Rearrange the model:

```
τ = (t_2 − t_1) / ln( (D(t_1) − D_s) / (D(t_2) − D_s) )
```

From the table in section 2, take day 3 (`D = 9.21`) and day 14 (`D = 5.08`) with `D_s = 4`. Then `τ = 11 / ln(5.21 / 1.08) = 11 / 1.57 = 7.0` days, as expected.

Real data is noisy, so use every day instead of two. Take logs of the model:

```
ln(D(t) − D_s) = ln(D_0 − D_s) − t/τ
```

This is a straight line in `t` with slope `−1/τ`. Fit it by least squares and read off `τ`. The short script below checks the method on data generated from the model, then prints the lecture's cycle averages.

```python
import math

def diversity_at(t, d0, ds, tau):
    return ds + (d0 - ds) * math.exp(-t / tau)

def fit_tau(days, diversity, ds):
    pts = [(t, math.log(d - ds)) for t, d in zip(days, diversity) if d > ds]
    mx = sum(t for t, _ in pts) / len(pts)
    my = sum(y for _, y in pts) / len(pts)
    slope = (sum((t - mx) * (y - my) for t, y in pts)
             / sum((t - mx) ** 2 for t, _ in pts))
    return -1 / slope

def cycle_average(d0, ds, tau, period):
    return ds + (d0 - ds) * (tau / period) * (1 - math.exp(-period / tau))

days = [0, 3, 7, 14, 21, 28]
obs = [diversity_at(t, 12, 4, 7) for t in days]
print(f"fitted tau = {fit_tau(days, obs, 4):.2f} days")
for period in (7, 14, 28, 90):
    print(period, round(cycle_average(12, 4, 7, period), 2))
```

It prints:

```
fitted tau = 7.00 days
7 9.06
14 7.46
28 5.96
90 4.62
```

Three practical cautions.

- **You need `D_s` first.** Estimate it from the last week of a long cycle, or from the previous cycle's tail. If `D_s` is too high, points near the end fall below it and drop out of the fit. If it is too low, the fitted `τ` comes out too long. Lab 13 has you try both.
- **Check the fit as well as the number.** Plot `ln(D − D_s)` against `t`. If the points bend, the population is not settling exponentially. The usual cause is a second wave, where a new build is discovered on day 10 and diversity dips, spikes and dips again. Report that as two events, not one `τ`.
- **Measure in the audience you are tuning for.** The top of a ladder converges faster than the whole population, as MMO303 week 1 noted for diversity by bracket. A professional scene may be settled while casual players are still in discovery. Fit `τ` per bracket.

### When to judge a change

The same model tells you when a patch's effect is readable. On day `τ`, 37% of the gap is still open. The data shows a population on the move, and any class looks stronger or weaker than it will be. By `2τ` the remaining gap is 14%, and by `3τ` it is 5%. A good rule is to wait at least `2τ` before you judge a balance change from pick data, and to write that date into your patch plan. With `τ = 7`, that is two weeks. With a two-week patch cycle, that is the day of the next patch. Section 4 deals with what that means.

## 4. Designing the patch calendar

A patch calendar is a set of cadences layered on top of each other, each doing a different job.

| Layer | Typical job | Effect in the model |
|---|---|---|
| Hotfix | Remove a clear outlier or exploit within days | Stops one strategy crushing `D_s`, no reset |
| Balance patch | Tune numbers on a regular schedule | Small reset to `D_0`, shifts `D_s` |
| Content patch or new season | New options, systems or rules | Large reset, often raises the ceiling of `D_0` |
| Scheduled perturbation | Weekly affixes, map or mode rotation | Rotates the settled state without a patch |

The rule from section 3 creates a real conflict for fast cadences. If `2τ` equals `T`, you judge each patch on the day you ship the next one. You cannot learn from patch *n* before writing patch *n + 1*, so you are always tuning on half-settled data. Studios on short cadences handle this in a few ways. They lock the contents of a patch before the previous patch's data is complete and accept a one-patch lag. They also keep some patches deliberately small, which makes the next reading cleaner. And they reserve hotfixes for outliers so obvious that they show in two days of data. The measurement tools for that call are the subject of [week 14](w14-measuring-balance-with-win-rates-and-pick-rates.md).

Slow cadences have the opposite problem. With `T = 90` and `τ = 7`, the game spends 82% of each cycle settled. Players who dislike the current settled meta have nothing to wait for. Slow-cadence designs therefore lean on the other tools: a high `D_s` from counter design, a two-level cadence with small interim patches, and seasonal events.

Seasons are the natural outer layer. A season is a large planned shock tied to rating resets and rewards, and [week 11](w11-seasonal-structures-and-resets.md) covers its design. The patch cadence sits inside the season. A reasonable planning exercise is to draw one season on a calendar and mark every layer. That is the in-class activity.

The process side of patches, including hotfix procedure, rollbacks and deployment, belongs to live operations. See [MMO308 week 9](../../MMO308-live-operations-analytics-and-experimentation/lectures/w09-patch-management-and-hotfixes.md). How to write the notes is [MMO303 week 14](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w14-communicating-balance-changes.md).

## 5. The meta beyond numbers

Two effects fall outside the model, and designers who ignore them get surprised.

**Players choose for reasons other than power.** A class with a striking fantasy or a new cosmetic set draws players regardless of its win rate. Those players raise `D_s`, because they are friction that keeps the population from collapsing onto the strongest options. That is healthy, and it is one reason cosmetic and identity design matters to balance. It also makes pick rate a poor measure of power, which is a theme of next week.

**The meta is a social agreement as well as a population.** Once a build is "the build," groups demand it in matchmaking and raid invitations. The pressure outlasts the numbers. A class buffed back to strength can stay unpopular for a whole cycle because nobody invites it. In model terms, social pressure shortens `τ` on the way down and lengthens it on the way back up. When you buff a neglected option, expect the recovery to be slower than the fall, and say so in the notes.

## In-class activity (25 minutes)

Groups of three or four. Materials: the interactive, a calendar grid for one 16-week season (printed or on screen) and this data from an invented game. Daily `N_eff` after its last patch:

| Day | 0 | 2 | 5 | 9 | 14 | 21 | 28 |
|---|---|---|---|---|---|---|---|
| `N_eff` | 10.0 | 8.4 | 6.7 | 5.4 | 4.6 | 4.2 | 4.1 |

1. Estimate `D_s` from the tail and `τ` from two points (5 minutes). Check your `τ` with a third point.
2. Your team can ship 10 balance patches this season. Place them on the calendar. Use the interactive to find your season's average `N_eff`, and compare it with evenly spaced patches (10 minutes).
3. Propose one scheduled perturbation or one change that would raise `D_s`, and estimate how much it would move the average (5 minutes).
4. Write the day on which you would first judge each patch, and flag any patch you must write before its predecessor's data is readable (5 minutes).

Expected output: `D_s` and `τ` with working, a marked calendar, two average-diversity numbers and one paragraph arguing for your calendar. (For reference, with `D_s = 4` the pairs of points from days 0 to 14 give `τ` between about 5.9 and 6.5 days, and a least-squares fit over those five days gives 6.07. Days 21 and 28 sit only 0.1 to 0.2 above `D_s`, so any pair that uses them swings widely. That spread is the noise, and it is why the lab fits all the points at once.)

## Common misconceptions

- **"More patches always means a healthier meta."** Only up to about `T ≈ τ`. Past that, each extra patch buys less average diversity and costs players the same relearning.
- **"The patch worked, look how diverse the first week was."** A diverse first week is the shock phase, and every patch has one. Judge after `2τ`, against `D_s`.
- **"A stale meta means the game is unbalanced."** A settled meta can be perfectly fair and still narrow. Staleness is a diversity problem. It needs a diversity fix: better counters, more horizontal options or scheduled rotation, not necessarily number changes.
- **"Players solve the meta at a fixed speed."** `τ` depends on population, complexity and information tools, and it shrinks over a game's life. Refit it.

## Check yourself

1. A game settles from `D_0 = 10` to `D_s = 3` with `τ = 5` days. What is the average diversity if you patch every 10 days? What share of each cycle is settled?
2. Your dashboard shows `N_eff = 8.0` on day 2 after a patch and `5.0` on day 9. You believe `D_s = 4`. Estimate `τ`. On which day will 90% of the gap have closed?
3. A popular new statistics site halves your game's settling time. You currently patch every 28 days. What cadence restores your old average diversity, and why does the model say that exactly?
4. With `D_0 = 12` and `τ = 7`, compare option A, 12 evenly spaced patches a year with `D_s = 4`, and option B, 4 patches a year after a redesign that raises `D_s` to 5.5. Which gives the higher average diversity, and what does the comparison leave out?

<details>
<summary>Answers</summary>

1. `T/τ = 2`, so `D̄ = 3 + 7 × 0.5 × (1 − e^(−2)) = 3 + 3.5 × 0.8647 = 6.03`. Settled from `2.3τ = 11.5` days, which is after the next patch, so 0% of the cycle is settled.
2. `τ = (9 − 2) / ln((8 − 4)/(5 − 4)) = 7 / ln 4 = 7 / 1.386 = 5.05` days. 90% closed at `τ ln 10 = 11.6` days after the patch.
3. Every 14 days. The average depends only on `T/τ`. Halving `τ` doubles `T/τ` from 4 to 8 unless `T` halves too.
4. A: `T = 365/12 = 30.4` days, `D̄ = 4 + 8 × (7/30.4)(1 − e^(−4.34)) = 4 + 8 × 0.230 × 0.987 = 5.82`. B: `T = 91.25` days, `D̄ = 5.5 + 6.5 × (7/91.25)(1 − e^(−13.0)) = 5.5 + 0.50 = 6.00`. B wins slightly with a third of the patches. The comparison leaves out the cost of the redesign, and whether `D_0` stays at 12 after it. It also leaves out the fact that a player who dislikes B's settled meta waits three months for change.

</details>

## Lab hook

[Lab 13, settling time and patch cadence](../labs/lab13.md). You compute `N_eff` from 29 days of pick counts for an invented eight-class ladder, fit `τ`, test how sensitive the fit is to your `D_s`, and recommend a patch calendar for one season with its average diversity and its judgment dates. Its measurement output feeds the season design in the final assessment.

## Sources

- Riot Games, "League of Legends 2026 Patch Schedule," Riot Games Support (support.riotgames.com, accessed September 2026). Patches 26.01 (January 8, 2026) to 26.24 (December 9, 2026). Most patches ship every two weeks. Naming format `YEAR.PATCH`.
- Liquipedia Dota 2 Wiki, pages "Version 7.34" through "Version 7.40", and "Version 7.35b", "7.35c", "7.35d", "7.36a", "7.36b", "7.36c" (accessed September 2026). Release dates: 7.34 August 8, 2023; 7.35 December 14, 2023; 7.35b December 21, 2023; 7.35c February 21, 2024; 7.35d March 21, 2024; 7.36 May 22, 2024; 7.36a May 26, 2024; 7.36b June 5, 2024; 7.36c June 24, 2024; 7.37 July 31, 2024; 7.38 February 19, 2025; 7.39 May 21, 2025; 7.40 December 15, 2025. Intervals computed from these dates.
- Warcraft Wiki, "Mythic+" and "Affix" (warcraft.wiki.gg, accessed September 2026). Mythic+ introduced in patch 7.0.3 (Legion) with weekly-rotating affixes, standardized across all players each week. Affix levels and lists have changed across seasons.
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press. The chapter on the balance process after launch.
- Settling model, cycle-average formula and all numbers for the invented ladder are this course's own and are computed in the lecture's code.

## Interactive spec: examples/w13-patch-cadence.html

**The one insight:** a faster patch cadence makes the meta look busier every time, but average diversity saturates once the patch interval drops below the settling time `τ`. What matters is the ratio `T/τ`, not the number of days.

**Layout.** Two linked views side by side at 1280px, stacked at 390px (sawtooth first). Controls above, number panel below. The first screen shows both views at the default values with the marker on the right-hand curve.

**Left view: sawtooth over one season.**
- x axis: days 0 to 180. y axis: `N_eff` from 0 to `max(D_0) + 1`.
- Plot `D(t)` where `t` is days since the most recent patch: `D(t) = D_s + (D_0 − D_s) e^(−(t mod T)/τ)`. Draw at least 2 samples per day, and more when `T < 5`.
- Thin vertical tick at each patch day.
- Dashed horizontal line at `D̄(T)` labeled "average", and a dotted line at `D_s` labeled "settled".
- Shade in a muted color the parts of each cycle where the meta is settled, i.e. `(t mod T) ≥ τ ln 10`.

**Right view: average diversity against patch interval.**
- x axis: `T` from 1 to 180 days on a logarithmic scale, with ticks at 1, 2, 3.5, 7, 14, 28, 56, 90, 180. A secondary label under each tick shows patches per year, `365/T`, to one decimal.
- Plot `D̄(T)` as a smooth curve. Horizontal reference lines at `D_0` and `D_s`.
- A vertical guide at `T = τ` labeled "T = τ", and a filled marker at the current `T`.
- Optional overlay toggle "compare": freezes the current curve as a grey ghost so the student can change `τ` or `D_s` and see the shift.

**Controls.**
- Patch interval `T`: slider 1 to 180 days, step 0.25 below 7 and step 1 above (or a log slider), default 28. Also buttons "League-like (14)", "Quarterly (90)".
- Settling time `τ`: slider 1 to 30 days, step 0.5, default 7.
- `D_0`: slider 2 to 20, step 0.5, default 12. `D_s`: slider 1 to `D_0`, step 0.5, default 4 (clamp `D_s ≤ D_0`).
- Keyboard: every slider works with arrow keys; Page Up and Page Down move `T` by 7 days.

**Formulas.**
- `D̄(T) = D_s + (D_0 − D_s)(τ/T)(1 − e^(−T/τ))`.
- Settled share of cycle `= max(0, T − τ ln 10) / T`.
- Patches per year `= 365 / T`.

**Number panel.** `T`, `τ`, `T/τ` (two decimals), patches per year (one decimal), `D̄` (two decimals), settled share (whole percent), and "gain from halving T" `= D̄(T/2) − D̄(T)` (two decimals). That last number makes the diminishing return explicit.

**Test values** (with `D_0 = 12`, `D_s = 4`, `τ = 7`).
- `T = 7`: `D̄ = 9.06`, settled 0%, 52.1 patches per year.
- `T = 14`: `D̄ = 7.46`, settled 0%, gain from halving 1.60.
- `T = 28`: `D̄ = 5.96`, settled 42%, gain from halving 1.50.
- `T = 90`: `D̄ = 4.62`, settled 82%.
- `τ = 3.5`, `T = 14`: `D̄ = 5.96` (same as `τ = 7`, `T = 28`).
- `D_s = 6`, `T = 90`: `D̄ = 6.47`.
- Sawtooth at `T = 28`: value 6.94 at day 7 and 12.00 at day 28 (the next patch).

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`, copied inline. Lines differ by dash pattern as well as color. Respect `prefers-reduced-motion` (no animated transitions) and `prefers-color-scheme`. Numbers in the panel use tabular figures. No game names, logos or art in the graphic; the text labels may say "two-week cadence" and "quarterly".

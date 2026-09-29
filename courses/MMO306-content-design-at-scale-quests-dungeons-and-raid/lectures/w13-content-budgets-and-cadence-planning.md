# MMO306 · Week 13 — Content Budgets and Cadence Planning

**Why this matters:** Week 1 told you how long players take to run out of a drop. This week answers the question your producer will ask next. How many teams do we need to ship a drop every N days, and how often will we actually hit the date? If you plan with the average build time, you will be late about half the time, and players will feel every late day as a drought.

**You will be able to:**
- Compute a drop's mean build time and spread from a three-point estimate, and the chance that it is ready by its release date.
- Derive the number of staggered teams a cadence needs for a target on-time rate, and the fastest cadence a given number of teams can promise.
- Compare slipping a late drop with cutting its scope, and say which players each option costs.
- Design a one-page roadmap that places major and minor drops against the drought your population will feel.

**Before class:** Final Fantasy XIV Online Wiki, "Patches" (10 minutes, note the dates of the Dawntrail patches). Wikipedia, "Program evaluation and review technique", the sections on terminology and on the three time estimates (15 minutes). Reread the model and table of [week 1](w01-the-content-treadmill-production-vs-consumption.md), section 2.

**Prerequisites from earlier courses:** [MMO306 week 1, the content treadmill](w01-the-content-treadmill-production-vs-consumption.md) gave you exhaustion time `T`, cadence `P` and drought. This week reuses them and does not re-derive them. [MA102 week 8, dice sums and the normal curve](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w08-dice-sums-and-the-normal-curve.md) gave you `Φ` and z-scores. [MA102 week 11, Monte Carlo simulation](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w11-monte-carlo-simulation.md) is the method of this week's lab. PR101 week 6, estimation and why it fails ([syllabus](../../PR101-game-production-i-teams-scope-and-the-game-jam/syllabus.md)), met the cone of uncertainty on a jam game. Here the same uncertainty meets a release calendar.

**Interactive:** [`examples/w13-cadence-promise.html`](../examples/w13-cadence-promise.html). Keep it open during section 2.

---

## 1. Budgets in team-days, cadence in calendar days

A **content budget** is the production capacity you spend on a drop. Studios count it in people and time. This lecture uses **team-days**. One team working for one day is one team-day. A team here is a fixed group (designers, artists, engineers, testers) that can build a whole drop on its own.

A **cadence** `P` is the promise you make to players, the number of calendar days between drops (week 1). The two are linked by one fact from week 1, section 4. A team cannot build a raid in half the time by doubling its size. So when a studio wants drops more often than one team can build them, it **staggers** teams. With `n` teams, each team builds every `n`th drop. Team A builds drops 1, 4 and 7, team B builds 2, 5 and 8, and so on. Each team then has a **build window** of `W = n × P` days per drop.

The trouble is that nobody knows the **build time** `D` of a drop before it is built. It depends on bugs, on hiring, on the feature that turned out to need a new tool. So producers ask for three numbers instead of one.

- The **optimistic** time `a`: everything goes right.
- The **most likely** time `m`: the one you would bet on.
- The **pessimistic** time `b`: several things go wrong, but nothing catastrophic.

This is a **three-point estimate**. Its most useful property is that it is lopsided. A drop can come in a few weeks early. It can come in months late. Most teams give a `b` that is much further from `m` than `a` is, and they are right to.

A **buffer** is the gap between the build window and the time you expect the build to take. It is the insurance you buy with team-days. The rest of this lecture is about how much buffer a promise needs, and what happens when the buffer runs out.

## 2. Worked example: the date you can promise

### The hook

Final Fantasy XIV's expansion Dawntrail launched with patch 7.0 on 2 July 2024. Then came 7.1 on 12 November 2024, 7.2 on 25 March 2025, 7.3 on 5 August 2025, 7.4 on 16 December 2025 and 7.5 on 28 April 2026. Count the days between them. Every gap is 133 days, five times in a row. That is exactly 19 weeks, the interval the game's community wiki gives for major patches since Endwalker. Even in Endwalker the gaps were 126, 133, 140, 133 and 133 days.

Compare two other games in the same years.

- World of Warcraft's patch 6.2.0, the last major content patch of Warlords of Draenor, came out on 22 June 2015. The next expansion, Legion, opened its new continent on 30 August 2016. That is 435 days between content drops.
- Bungie planned Destiny 2: The Final Shape for 27 February 2024. On 27 November 2023, 92 days before that date, Bungie announced a delay to 4 June 2024, saying it needed more time to deliver its vision for the expansion. The drop arrived 98 days after the promised date.

Nobody outside these studios knows their internal schedules, and this lecture will not guess. But the pattern raises a question every live team faces. What does it take to promise a date, and hit it, drop after drop? The answer is a single probability, and it depends far more on the slow end of your estimate than on its middle.

### The model

Turn the three-point estimate into a mean and a spread with the formulas of **PERT**, the Program Evaluation and Review Technique, which the US Navy's Special Projects Office developed with Lockheed and Booz Allen Hamilton for the Polaris missile programme in 1958:

```
mean build time      μ = (a + 4m + b) / 6
spread               σ = (b − a) / 6
build window         W = n × P
z-score              z = (W − μ) / σ
on-time chance       q = Φ(z)
```

- `a`, `m` and `b` are the optimistic, most likely and pessimistic build times, in days.
- `μ` is the expected build time. The weight of 4 on `m` pulls it toward the most likely value, and a long pessimistic tail pulls it to the right of `m`.
- `σ` is the standard deviation of the build time. Six spreads cover the range from `a` to `b`, which is the PERT convention.
- `n` is the number of staggered teams and `P` the cadence, so `W` is the time each team has for its drop.
- `Φ` is the standard normal cumulative distribution (MA102 week 8). We approximate the build time as normal with mean `μ` and spread `σ`, which is how PERT is usually applied.
- `q` is the chance a drop is ready by its date.

Two useful rearrangements follow. To reach a target on-time rate `q*`, with `z*` the value where `Φ(z*) = q*`:

```
teams needed          n = ceil((μ + z* × σ) / P)
fastest cadence       P_min = (μ + z* × σ) / n
```

For `q* = 90%`, `z* = 1.28`. For 50%, `z* = 0`, which is the plan "divide the average build time by the number of teams." Hold on to that. It is the plan most teams make first.

### Numbers you can check

Take a raid-tier drop estimated at `a = 240`, `m = 300`, `b = 480` days. The pessimistic case is three times further from the most likely case than the optimistic one. These figures are invented for teaching, but a raid tier with its zone, dungeons and systems plausibly takes most of a year to build.

```
μ = (240 + 4 × 300 + 480) / 6 = 1,920 / 6 = 320 days
σ = (480 − 240) / 6 = 40 days
```

Note that `μ` is 20 days later than `m`. The lopsided estimate has already told you something. The time you would bet on is not the time to plan on.

| Teams `n` | Cadence `P` (days) | Window `W` | `z` | On-time chance `q` | Average days late |
|---|---|---|---|---|---|
| 1 | 365 | 365 | 1.13 | 87.0% | 2.6 |
| 2 | 160 | 320 | 0.00 | 50.0% | 16.0 |
| 2 | 175 | 350 | 0.75 | 77.3% | 5.2 |
| 2 | 200 | 400 | 2.00 | 97.7% | 0.3 |
| 3 | 120 | 360 | 1.00 | 84.1% | 3.3 |
| 3 | 133 | 399 | 1.98 | 97.6% | 0.4 |

Check one row by hand. Two teams on a 175-day cadence each have `W = 350` days. `z = (350 − 320) / 40 = 0.75`, and `Φ(0.75) = 0.773`. Roughly one drop in four will not be ready on its date.

The last column is the average number of days a drop misses its date by, counting on-time drops as zero. It is `σ × (φ(z) − z × (1 − Φ(z)))`, where `φ` is the normal density. You don't need to derive it. Read it as "what a slip costs players on average, per drop."

Now read the second row carefully. Two teams, and `2 × 160 = 320`, exactly the mean build time. On paper the plan fits. In practice it is on time half the time, and the average drop is 16 days late. **A plan built on the mean is a coin flip.**

The teams-needed formula makes the same point from the other side. For a 90% on-time rate you need `μ + 1.28 σ = 371` days of window per drop.

| Cadence `P` | Teams for 90% on time | Fastest cadence those teams can promise at 90% |
|---|---|---|
| 365 | 2 | 186 |
| 200 | 2 | 186 |
| 175 | 3 | 124 |
| 133 | 3 | 124 |
| 120 | 4 | 93 |

Team counts are whole numbers, so the cost of a cadence is a staircase. Going from 200 to 175 days needs a third team. Going from 175 to 133 needs nothing more. A studio that pays for three teams and ships every 175 days is holding about 154 days of spare window per drop (`3 × 175 − 371`), or 51 days of cadence it could have promised and didn't. That spare time is not waste. It is either reliability (on time 99.9% of the time) or scope (a bigger drop). But you should choose which one on purpose.

The same numbers from code:

```python
from statistics import NormalDist

PHI = NormalDist()                      # standard normal: PHI.cdf, PHI.pdf, PHI.inv_cdf

def pert(a, m, b):
    """Mean and spread of a build time from a three-point estimate (days)."""
    return (a + 4 * m + b) / 6, (b - a) / 6

def on_time(n, P, mu, sigma):
    """Chance a drop is ready by its date when n staggered teams share cadence P."""
    return PHI.cdf((n * P - mu) / sigma)

def mean_late(n, P, mu, sigma):
    """Average days late per drop (zero for drops that are ready in time)."""
    z = (n * P - mu) / sigma
    return sigma * (PHI.pdf(z) - z * (1 - PHI.cdf(z)))

mu, sigma = pert(240, 300, 480)
print(f"mu = {mu:.0f} days, sigma = {sigma:.0f} days")
for n, P in ((1, 365), (2, 160), (2, 175), (2, 200), (3, 120), (3, 133)):
    print(f"n={n} P={P:3d}  window {n * P:3d}  on time {on_time(n, P, mu, sigma):6.1%}"
          f"  mean late {mean_late(n, P, mu, sigma):4.1f} d")
```

It prints:

```
mu = 320 days, sigma = 40 days
n=1 P=365  window 365  on time  87.0%  mean late  2.6 d
n=2 P=160  window 320  on time  50.0%  mean late 16.0 d
n=2 P=175  window 350  on time  77.3%  mean late  5.2 d
n=2 P=200  window 400  on time  97.7%  mean late  0.3 d
n=3 P=120  window 360  on time  84.1%  mean late  3.3 d
n=3 P=133  window 399  on time  97.6%  mean late  0.4 d
```

### A visual you can move

Open the interactive. The left view is a two-year calendar. Each team is a row, and each drop is a bar from the day its team starts it to its release date. At the end of each bar sits a small bell curve, the build-time distribution, with the part that runs past the release date shaded. The right view plots the on-time chance `q` against the cadence `P`, one S-shaped curve for each team count from 1 to 5, with your current plan as a dot and a dashed line at your target.

Start with two teams at 160 days. Half of every bell hangs past its date. Drag `P` to 175 and the shaded tails shrink, but the dot on the right is still well under the 90% line. Now add a third team. The dot jumps to a different curve, and you can drag `P` down to about 124 days before it falls below 90% again.

Then leave `n` and `P` alone and drag the pessimistic estimate `b` from 480 to 600. The mean moves 20 days, but the spread moves 20 days too, and every curve on the right slides to the right. The slow end of the estimate, not the likely case, sets what you can promise.

### Cross-game recognition

The model needs three numbers a studio rarely publishes, the build window, the mean and the spread. So what you can recognize from outside is the output of the model, the release pattern.

**Final Fantasy XIV (Endwalker and Dawntrail, 2021-2026).** Inside the two expansions there are ten gaps between major patches. All ten are within a week of 133 days, and eight are exactly 133. The one long gap, 273 days from 6.5 to 7.0, is the expansion itself, a different kind of drop. In model terms, this is a plan that sits far up an S-curve, with `W` many spreads above `μ`. A release history like that is what `q` near 100% looks like from the player's side. Whatever the internal arrangement, the published cadence is long enough, relative to the effort in each patch, that a bad month does not move the date.

**Destiny 2: The Final Shape (2023-2024).** A single drop whose date moved by 98 days, announced 92 days ahead. In model terms, the studio learned partway through the build that `D` would land far out in the tail, and chose to move the date rather than ship less. Section 3 puts a number on that choice. Wikipedia's article also records that Bungie made layoffs in October 2023, the month before the delay was announced. Losing people mid-build is exactly the kind of event that turns a pessimistic estimate into the actual one.

**World of Warcraft, Warlords of Draenor to Legion (2015-2016).** A 435-day gap after the last major patch. Whatever the cause, week 1's drought formula does not care. For every player who exhausted patch 6.2, the drought was the gap minus their `T`. A long gap is the model's output when no finished drop is waiting in the pipeline.

**Guild Wars 2, Living World Season 1 (January 2013 to March 2014).** ArenaNet shipped the season's story in bi-weekly installments for 414 days. Apply the teams-needed formula in reverse. If one installment took even three months to build, a 14-day cadence needs `n ≥ 90 / 14`, so at least 7 builds in flight at once. That is a model inference, not a report of ArenaNet's staffing. It shows what a very short cadence commits a studio to, whether the parallel work is whole teams or overlapping stages of one pipeline.

**Outside games, the Polaris programme (1958).** PERT was built for exactly this problem, a large project with thousands of uncertain tasks and a date the whole organisation depended on. The three-point estimate and the `(a + 4m + b) / 6` weighting come from there. Studios use the same arithmetic, whether or not they call it PERT.

### Eyes-open design judgment

- **Never plan on the most likely time.** It is the most common single outcome, but not the average, when the estimate is lopsided. Plan on `μ`, and then decide how far above it the window must sit.
- **Pick the on-time rate as a design decision.** 50% means the community learns that your dates are guesses. 90% means one late drop in ten, roughly one every three years at a 4-month cadence. 99% costs about one extra spread per drop. Say which you are buying.
- **The staircase makes some cadences free.** Once you pay for a team, the fastest cadence it allows at your target rate is `(μ + z* σ) / n`. Anything slower is spare window. Spend it on purpose, on scope or on reliability.
- **Shortening `P` has a player cost too.** Week 1 showed that `T` does not change with cadence. A shorter `P` shrinks the drought of heavy players and floods light players with content they have not finished. A 133-day cadence with a 140-day median `T` means the median player is still busy when the next patch lands.
- **Estimates are the weak link.** The whole calculation rests on `b`. Teams that have never shipped a drop underestimate it. Use the history of your own drops, not your hopes. Week 7's point about small samples applies to production data too.

### Check yourself (worked example)

1. An estimate is `a = 90`, `m = 120`, `b = 210` days. Compute `μ` and `σ`. With one team and a 150-day cadence, what is the on-time chance?
2. For the same estimate, how many staggered teams does a 60-day cadence need for a 90% on-time rate?

<details>
<summary>Answers</summary>

1. `μ = (90 + 480 + 210) / 6 = 130` days, `σ = 120 / 6 = 20` days. `z = (150 − 130) / 20 = 1`, so `q = Φ(1) = 84.1%`.
2. `μ + 1.28 σ = 130 + 25.6 = 155.6` days of window per drop. `n = ceil(155.6 / 60) = ceil(2.59) = 3` teams. With three teams the window is 180 days, `z = 2.5`, and `q ≈ 99.4%`.

</details>

## 3. Slip or cut: who pays for a late drop

Sooner or later a drop is not ready on its date. You have two pure options. You can **slip**, shipping the whole drop late. Or you can **cut**, shipping on the date with part of the drop removed. Real studios often mix them, by cutting a feature and shipping it in a later, smaller patch. The pure options are worth separating, because they cost different players.

Use week 1's exhaustion time `T` for each player. The late drop is `X` days late, or it ships on time with a share `s` of its content hours removed.

- A **slip** lengthens the current cycle from `P` to `P + X`. Every player who had run out of the current drop waits `X` more days. The extra drought is `min(X, max(0, P + X − T))`. It is the same `X` for every player with `T ≤ P`.
- A **cut** leaves the date alone and shrinks the next drop. Its `T` falls to `(1 − s) × T`, because `T` is proportional to content hours `C`. The extra drought, at the end of the next cycle, is `max(0, P − (1 − s)T) − max(0, P − T)`. For players who run out anyway, it is `s × T`, proportional to their own `T`.

So a slip charges everyone who runs out the same amount, and a cut charges each player in proportion to how long the drop would have lasted them. Take week 1's design B (`C = 20`, `r = 6`, `P = 175`), a drop 21 days late, and a cut of 15%, which is the cut that would roughly recover 21 days of a 140-day build:

```python
P, X, s = 175, 21, 0.15                 # cadence, days late, share of content cut
C, r = 20, 6                            # week 1, design B

for h in (3, 5, 6, 10, 16, 34, 60):     # hours per week; 6 to 60 are week 1's p50 to p99.9
    T = 7 * C * r / h                                    # week 1's exhaustion time
    slip = min(X, max(0, P + X - T))                     # extra drought if the drop ships X days late
    cut = max(0, P - (1 - s) * T) - max(0, P - T)        # extra drought if it ships on time, cut by s
    print(f"{h:2d} h/wk  T={T:6.1f}  slip +{slip:4.1f} d  cut +{cut:4.1f} d")
```

It prints:

```
 3 h/wk  T= 280.0  slip + 0.0 d  cut + 0.0 d
 5 h/wk  T= 168.0  slip +21.0 d  cut +25.2 d
 6 h/wk  T= 140.0  slip +21.0 d  cut +21.0 d
10 h/wk  T=  84.0  slip +21.0 d  cut +12.6 d
16 h/wk  T=  52.5  slip +21.0 d  cut + 7.9 d
34 h/wk  T=  24.7  slip +21.0 d  cut + 3.7 d
60 h/wk  T=  14.0  slip +21.0 d  cut + 2.1 d
```

The median player is indifferent. Everyone heavier would rather you cut. The 60-hour player barely notices a 15% cut, but waits three extra weeks through a slip. The 5-hour player, who was almost keeping up, is hurt more by the cut, because it takes away a larger slice of a longer `T` and pushes them into a real drought. The 3-hour player is not affected by either, because they never run out.

This matters for who complains. Heavy players are the loudest voices after a delay, and the table says they are right that a delay hurts them most. Light players rarely complain about a cut, because they don't notice it until months later. A designer should weigh both, not only the one that shows up on forums.

Two refinements change the answer in practice.

- **What gets cut matters.** Cutting a repeatable system lowers `r`, which shrinks `T` for everyone in proportion, as above. Cutting a one-time story chapter mostly hurts light players, who play it, and barely touches heavy players, who finish it in the first evening. Cutting the hardest tier (week 6) hurts only the top percentiles.
- **A cut can come back.** If the cut content ships in a small follow-up patch before light players run out, most of their extra drought disappears. This is one reason studios plan minor patches between major ones, the subject of section 4.

## 4. The roadmap on one page

A **roadmap** is the calendar of drops for the next year or two. For a content team, it is the place where production (section 2) meets consumption (week 1). You can draw the whole thing on one page.

1. **Major drops.** Place them at your cadence `P`. Each has a build window `n × P`, a three-point estimate and an on-time chance. Write the chance on the roadmap next to the date.
2. **The drought line.** For each major drop, mark the day each percentile runs out, `T_p50`, `T_p90` and so on (week 1). These are the days players start to leave.
3. **Minor drops.** Put small, cheap drops where the drought line says players will need them. A good first rule is to land a minor drop just before `T_p50`, the day half your players run out. Events (week 11), rotations (week 8) and procedural content (week 9) are the natural fillers, because their cost per hour of play is low.
4. **The live team.** Minor drops need people too. Budget them separately from the major-drop teams. If a major-drop team has to stop and build an event, its window shrinks and its on-time chance falls.

Here is a worked budget. A studio has 3 major-drop teams and a live team. The major cadence is 175 days, and the drop from section 2 (`μ = 320`, `σ = 40`) gets a window of 525 days, `z = 5.1`, on time essentially always. The studio could spend the spare window on a bigger drop, but it decides instead to shorten the cadence to 133 days (`W = 399`, `q = 97.6%`). It now ships about 2.7 major drops a year instead of 2.1.

Week 1's design B gives the median player `T = 140` days. With `P = 133`, the median player is never in drought. The p90 player (`T = 52.5`) runs out 80 days before each drop. So the live team's job is a minor drop around day 50 to 60 of each cycle, aimed at the top percentiles. That tells you what kind of minor drop to build. It should be something with high replay, like a new rotation or a harder tier, not 10 hours of story that the median player has no time to reach.

Compare the plan with the one the studio started from, 2 teams at 160 days. That plan was on time half the time, its average drop was 16 days late, and the live team would have spent its effort patching droughts caused by slips, not planned ones.

### When one late drop becomes three

The model in section 2 treats each drop on its own. In a real schedule, a late drop has two knock-on effects.

- **The team starts its next drop late.** If team A's drop 1 is 30 days late, team A starts drop 4 30 days late too, unless it cuts. Its window for drop 4 shrinks from `n × P` to `n × P − 30`, and its on-time chance falls.
- **Drops ship in order.** Drop 2 cannot sensibly ship before drop 1, even if team B is ready. So one team's slip can hold up another team's finished drop.

With these rules the on-time chance of a whole roadmap is lower than `q` for any one drop, and the gap grows the tighter the plan is. There is no neat formula for it. That is why this week's lab simulates the roadmap instead, with MA102 week 11's Monte Carlo method.

## In-class activity (25 minutes)

Work in groups of three. Your studio has a raid-tier drop estimated at `a = 200`, `m = 260`, `b = 440` days, and wants a cadence between 100 and 200 days.

1. **(5 min)** Compute `μ` and `σ`. Using the interactive or a z-table, find the on-time chance for 2 teams at 160 days and 3 teams at 120 days.
2. **(8 min)** Your producer can fund at most 3 teams and wants 90% on time. Find the fastest cadence. Then find the on-time chance of the "average plan" (`P = μ / 3`).
3. **(7 min)** A drop is 28 days late. Using week 1's design B population (`C = 20`, `r = 6`) and your cadence, fill a slip-or-cut table for the 5, 6, 16 and 60 hours-a-week players with a 20% cut. Decide which you would choose and write the one sentence you would post to players.
4. **(5 min)** Sketch the one-page roadmap for your first year, with the drought line for p50 and p90 and one minor drop. Say which percentile the minor drop is for.

Expected output: `μ`, `σ`, three on-time chances, the fastest cadence, a four-row slip-or-cut table with your decision, and a sketched roadmap.

## Common misconceptions

- **"If the build takes 320 days and we have two teams, we can ship every 160 days."** That plan is on time 50% of the time, and the average drop is 16 days late. The window must sit above the mean by as many spreads as your target rate needs.
- **"The most likely estimate is the one to plan with."** With a lopsided estimate, the mean is later than the most likely time. In the section 2 example it is 20 days later.
- **"A delay is always better than a cut, because players get the whole drop."** A slip costs every exhausted player the full delay. A cut costs each player in proportion to their own `T`. For heavy players a cut is much cheaper. For players who barely run out, it is the other way round.
- **"More teams always means more reliable drops."** More teams at the same cadence mean a bigger window. More teams used to shorten the cadence can leave reliability exactly where it was. The staircase shows that a third team can buy either a faster cadence or a safer one, not both.

## Check yourself

1. A dungeon drop is estimated at `a = 60`, `m = 75`, `b = 120` days. One team builds it and the cadence is 90 days. Compute `μ`, `σ` and the on-time chance.
2. For the estimate in section 2 (`μ = 320`, `σ = 40`), what cadence can 4 teams promise at 97.7% on time (`z = 2`)?
3. A drop is 30 days late with `P = 150`. A player has `T = 60` days. What extra drought does a slip cause? What does a 25% cut cause? Which does this player prefer?
4. A studio runs 3 teams on a 175-day cadence with the section 2 estimate. Its producer proposes moving to 150 days "because we have the people." Compute the on-time chance before and after, and say what the studio gives up.
5. Two teams share a 160-day cadence (section 2 estimate). Drop 1 comes in 30 days late and team A does not cut. What is team A's window for drop 3, and its on-time chance?

<details>
<summary>Answers</summary>

1. `μ = (60 + 300 + 120) / 6 = 80` days, `σ = 60 / 6 = 10` days. `z = (90 − 80) / 10 = 1`, so `q = 84.1%`.
2. `P = (μ + 2σ) / 4 = 400 / 4 = 100` days.
3. Slip: `T ≤ P`, so the full 30 days. Cut: `s × T = 0.25 × 60 = 15` days. This player prefers the cut, by half.
4. Before: `W = 525`, `z = 5.1`, on time essentially always. After: `W = 450`, `z = 3.25`, `q = 99.94%`. The studio still ships on time almost always. What it gives up is 75 days of window per drop that it could have spent on a bigger drop. That is a scope decision, not a reliability one.
5. Team A starts drop 3 thirty days late, so its window is `2 × 160 − 30 = 290` days. `z = (290 − 320) / 40 = −0.75`, and `q = Φ(−0.75) = 22.7%`. One late drop has turned a coin-flip plan into a probably-late one. This is the cascade of section 4.

</details>

## Lab / assignment hook

[Lab 13, a roadmap simulator](../labs/lab13.md). You implement the PERT mean and spread, the on-time chance and the teams-needed rule, then write a release simulator in which late teams start their next drop late and drops ship in order. You run it over a two-year roadmap and choose a team count and cadence for your final dungeon's studio. The roadmap you produce goes into the final dungeon's content budget.

## Sources

- Final Fantasy XIV Online Wiki (consolegameswiki), "Patches" (retrieved September 2026). Release dates: 6.0 on 7 December 2021, 6.1 on 12 April 2022, 6.2 on 23 August 2022, 6.3 on 10 January 2023, 6.4 on 23 May 2023, 6.5 on 3 October 2023, 7.0 on 2 July 2024, 7.1 on 12 November 2024, 7.2 on 25 March 2025, 7.3 on 5 August 2025, 7.4 on 16 December 2025, 7.5 on 28 April 2026. Major patches on a 4.5-month (19-week) interval since Endwalker. Day counts between patches computed from these dates. https://ffxiv.consolegameswiki.com/wiki/Patches
- Warcraft Wiki, "Patch 6.2.0" (Warlords of Draenor). Released 22 June 2015; the last major content patch of the expansion. https://warcraft.wiki.gg/wiki/Patch_6.2.0
- Warcraft Wiki, "Patch 7.0.3" (Legion pre-expansion patch, 19 July 2016). The Broken Isles became available on 30 August 2016. https://warcraft.wiki.gg/wiki/Patch_7.0.3
- Wikipedia, "Destiny 2: The Final Shape" (retrieved September 2026). Originally planned for 27 February 2024; delay to June announced 27 November 2023; released 4 June 2024; Bungie layoffs in October 2023. https://en.wikipedia.org/wiki/Destiny_2:_The_Final_Shape
- Guild Wars 2 Wiki, "Living World Season 1". Ran from 28 January 2013 (Flame and Frost: Prelude) to 18 March 2014 (Battle for Lion's Arch: Aftermath), released in temporary bi-weekly installments. https://wiki.guildwars2.com/wiki/Living_World_Season_1
- Wikipedia, "Program evaluation and review technique". Developed in 1958 by the US Navy Special Projects Office, Lockheed and Booz Allen Hamilton for the Polaris programme; expected time `(o + 4m + p) / 6` and standard deviation `(p − o) / 6`. https://en.wikipedia.org/wiki/Program_evaluation_and_review_technique
- The three-point estimates, team counts, player population and cut shares are invented for teaching. The player population and design B come from week 1 of this course.

## Interactive spec: examples/w13-cadence-promise.html

**The one insight.** A cadence planned on the mean build time is on time only half the time. What a studio can promise is set by the slow tail of its estimate and by a whole number of staggered teams, so the cost of a cadence is a staircase. The student must see the bell curves hang past their release dates at `n = 2, P = 160`, and see the plan's dot jump between S-curves when `n` changes.

**Layout.** Two linked views side by side on wide screens, stacked on phones (calendar first). A second tab, "Slip or cut", holds the section 3 table.

- **Left view, "Two-year calendar".** One row per team (up to 5). Drop `k` (from 1) is built by team `(k − 1) mod n`, starts at day `(k − n) × P` (negative days are drawn as pre-launch, clipped at the left edge with an arrow), and is due at day `k × P`. Draw each drop as a bar from start to due date, labelled "Drop k". At the due date draw a small normal density of the build time, centred at `start + μ`, width ±3σ, with the part beyond the due date hatched and labelled with its probability `1 − q`. Show days 0 to 730 on the x axis. A vertical line at "today" = day 0.
- **Right view, "On time vs cadence".** x axis `P` from 30 to 400 days, y axis `q` from 0 to 100%. One curve per `n` from 1 to 5, `q(P) = Φ((nP − μ) / σ)`, each labelled "n = 1" to "n = 5" at its right end. The current plan is a large dot on the curve for the current `n`. A dashed horizontal line at the target rate, with its value. For each `n`, a small tick on the target line at `P_min = (μ + z* σ) / n`.
- **Readout under both views.** `μ`, `σ`, `W`, `z`, `q` (one decimal percent), average days late (one decimal), teams needed for the target at the current `P`, and fastest cadence at the target for the current `n`. Copyable as text.

**Controls.**
- Optimistic `a`: slider 30 to 400 days, step 5, default 240.
- Most likely `m`: slider 30 to 500 days, step 5, default 300. Constrain `a ≤ m ≤ b`.
- Pessimistic `b`: slider 60 to 800 days, step 5, default 480.
- Teams `n`: stepper 1 to 5, default 2.
- Cadence `P`: slider 30 to 400 days, step 1, default 160.
- Target on-time rate: select 50%, 75%, 90%, 95%, 99%; default 90%.
- Preset buttons: "Mean plan" (`n = 2, P = 160`), "Two teams, 175" (`n = 2, P = 175`), "Three teams, 133" (`n = 3, P = 133`).
- Slip or cut tab: days late `X` slider 0 to 90, step 1, default 21; cut share `s` slider 0 to 50%, step 1, default 15%; cadence `P` shared with the main view but default 175 in this tab; content `C = 20` and replay `r = 6` fixed and shown.

**Formulas.**
- `μ = (a + 4m + b) / 6`, `σ = (b − a) / 6`, `W = nP`, `z = (W − μ) / σ`, `q = Φ(z)`.
- Average days late `= σ × (φ(z) − z × (1 − Φ(z)))`, with `φ` the standard normal density.
- Teams needed `= ceil((μ + z* σ) / P)`, `z*` from the target (0, 0.674, 1.2816, 1.6449, 2.3263).
- Fastest cadence `= (μ + z* σ) / n`.
- Slip or cut, for `h` in 3, 5, 6, 10, 16, 34, 60 hours a week: `T = 7 × C × r / h`; slip `= min(X, max(0, P + X − T))`; cut `= max(0, P − (1 − s)T) − max(0, P − T)`. Show as paired horizontal bars per row (slip solid, cut hatched) with values.

**Test values** (`a = 240, m = 300, b = 480`, so `μ = 320`, `σ = 40`).
- `n = 1, P = 365`: `q = 87.0%`, late 2.6 d.
- `n = 2, P = 160`: `q = 50.0%`, late 16.0 d. `n = 2, P = 175`: `q = 77.3%`, late 5.2 d. `n = 2, P = 200`: `q = 97.7%`, late 0.3 d.
- `n = 3, P = 120`: `q = 84.1%`, late 3.3 d. `n = 3, P = 133`: `q = 97.6%`, late 0.4 d.
- Target 90%: fastest cadence 371.3, 185.6, 123.8, 92.8 days for `n` = 1 to 4. Teams needed at `P = 175`: 3; at `P = 200`: 2; at `P = 120`: 4.
- Slip or cut (`X = 21, s = 15%, P = 175`): slip 0, 21, 21, 21, 21, 21, 21; cut 0, 25.2, 21.0, 12.6, 7.9, 3.7, 2.1 days for 3, 5, 6, 10, 16, 34, 60 h/week.
- Check-yourself answer 5: `n = 2, P = 160`, window reduced by 30 gives `q = 22.7%`. Offer a "Late start (days)" field in the readout, default 0, that subtracts from `W` for the highlighted drop.

**First screen.** The "Mean plan" preset, so the student sees every bell curve half-hatched and the dot sitting on the 50% line far below the 90% target.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. Team rows and S-curves are distinguished by dash pattern and direct labels, not colour alone. Late tails use a hatch pattern. All sliders, the stepper and preset buttons keyboard operable with visible values; readouts in an `aria-live="polite"` region. Transitions off under `prefers-reduced-motion`.

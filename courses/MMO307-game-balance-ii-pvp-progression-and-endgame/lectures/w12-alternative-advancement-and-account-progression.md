# MMO307 · Week 12 — Alternative Advancement and Account Progression

**Why this matters:** At the level cap, experience stops meaning anything unless you give it somewhere to go. Most MMOs answer with a second, often endless, progression track. The cost curve you choose for that track decides whether a player with a job can ever stand next to a player without one, and whether anyone still gets a reward after the first year.

**You will be able to:**
- Compute points earned and the power gap between a light and a heavy player under flat, linear and geometric point-cost schedules.
- Derive the long-run gap for each schedule (hours ratio, square root, constant difference) and explain why.
- Compare bounding the gap on the cost side with bounding it on the value side, and predict each design's reward cadence.
- Decide which progress should belong to the account rather than the character, and estimate what that does to the cost of an alternate character.

**Before class:** Schreiber & Romero, *Game Balance* (2021), the chapter on progression in PvE games, the part on endgame and post-cap progression. Reread GD203 week 7, section 5 (caps and what happens after them), and GD203 week 14, section 2 (the power gap `G` and the band `F`).

**Prerequisites from earlier courses:** [GD203 week 7, XP curves](../../GD203-combat-and-progression-design/lectures/w07-xp-curves.md), for cost tables and play-time targets. [GD203 week 14, horizontal vs vertical progression](../../GD203-combat-and-progression-design/lectures/w14-horizontal-vs-vertical-progression.md), for the power gap `G`, the band `F` and masteries as horizontal tools. [MA101 week 5, logarithms](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md). In this course, [week 2, vertical progression and power creep](w02-vertical-progression-and-power-creep.md), [week 3, horizontal progression](w03-horizontal-progression.md) and [week 11, seasonal structures and resets](w11-seasonal-structures-and-resets.md).

**Interactive:** [`examples/w12-aa-gap.html`](../examples/w12-aa-gap.html). Keep it open during section 2.

---

## 1. Where experience goes after the cap

A character's level stops at the cap, but the player keeps killing monsters and finishing quests. That experience has three possible fates.

- **It vanishes.** The bar fills and nothing happens. Players notice quickly, and a whole class of activity loses its reward.
- **It converts into something else**, such as gold or a currency. That feeds the economy and can inflate it.
- **It feeds a second progression track.** This is **alternative advancement** (AA). Post-cap experience earns points, and points buy small, permanent bonuses.

EverQuest shipped one of the first AA systems with its Shadows of Luclin expansion in December 2001. Past level 50, a player could divert a percentage of their experience to a separate bar that granted abilities, stats and even crafting bonuses. The slider mattered. Players chose, experience point by experience point, between levelling and AA.

Diablo III's **Paragon** system is the best-known modern version. Since patch 2.0.1 (early 2014, the pre-patch for Reaper of Souls), Paragon levels have had no cap, and they are shared across the account.

That second fact introduces the other half of this week. **Account progression** is progress that belongs to the player's account, so every character they own benefits. Character progression belongs to one character. The split decides how expensive a second character is, and so how many players will play one.

Both halves raise the same balance question from GD203 week 14. Does this track widen the gap between players who share content? A power track with no cap looks like a vertical treadmill that never stops. This lecture shows that whether it does depends almost entirely on one design choice, the cost of each successive point.

## 2. Worked example: the cost curve decides the gap

### The hook

Diablo III's Paragon 2.0 is uncapped. Yet points go into four categories in rotation (Core, Offensive, Defensive, Utility), and every stat in the last three is capped at 50 points. Once a player passes Paragon 800, all three are full, and every further point goes to Core, which means primary stat or vitality at +5 per point. So the "endless" system is mostly finite, with a narrow endless tail.

Why build an infinite progression track and then cap three quarters of it? Because an uncapped track with a constant reward per point makes the most active players pull away from everyone else without limit. The designers had to bound it somewhere. There are two places to do it, on the cost of points or on their value. This example is about the cost side. Section 3 does the value side.

### The model

Measure everything in post-cap hours. Assume a player earns experience at a steady rate, so the cost of a point can be written in hours.

- `c(n)` is the **cost** of point number `n`, in hours.
- `T(n) = c(1) + c(2) + … + c(n)` is the total cost of the first `n` points.
- A player with `h` post-cap hours holds `n(h)` points, the largest `n` with `T(n) ≤ h`.
- Each point adds `v` to a power multiplier, so `P = 1 + v × n`. We use `v = 1%`.

Two players share the endgame. The **light** player plays 5 post-cap hours a week, the **heavy** player 20. Their power gap is

```
G = P_heavy / P_light
```

which is exactly GD203 week 14's `G`. If `G` grows past the band `F` that an encounter can serve, the two players can no longer share it.

Three cost schedules cover most shipped designs.

| Schedule | Cost of point `n` | Total for `n` points | Points after `h` hours |
|---|---|---|---|
| Flat | `a` | `a × n` | `h / a` |
| Linear | `a × n` | `a × n (n + 1) / 2` | about `√(2h / a)` |
| Geometric | `a × r^(n−1)` | `a (r^n − 1) / (r − 1)` | `log_r(1 + h (r − 1) / a)` |

The last column predicts the long-run gap, before any numbers. Give the heavy player `k` times the hours of the light player (here `k = 4`).

- **Flat.** Points are proportional to hours, so the heavy player ends with `k` times the points. The ratio of points tends to `k = 4`.
- **Linear.** Points grow like the square root of hours, so the ratio tends to `√k = 2`.
- **Geometric.** Points grow like the logarithm of hours. Multiplying hours by `k` *adds* a fixed number of points, `log_r k` (MA101 week 5). The ratio of points tends to 1, and the difference stops growing at `log_r 4`.

For a geometric schedule with `r = 1.05`, that ceiling is `ln 4 / ln 1.05 ≈ 28.4` points. However long both players play, the heavy one ends up about 28 points ahead, and not further.

### Numbers you can check

Take these three schedules with 1% per point: flat at 10 hours per point, linear at `c(n) = 2n` hours, and geometric at `c(n) = 2 × 1.05^(n−1)` hours. The script below prints the table.

```python
from math import log, floor

VALUE = 0.01          # each point adds 1% power

def points_flat(hours, cost=10):
    return floor(hours / cost)

def points_linear(hours, step=2):
    # point n costs step * n hours, so n points cost step * n (n + 1) / 2
    n = 0
    while step * (n + 1) * (n + 2) / 2 <= hours:
        n += 1
    return n

def points_geometric(hours, first=2, ratio=1.05):
    # point n costs first * ratio ** (n - 1); n points cost first (ratio^n - 1)/(ratio - 1)
    return floor(log(1 + hours * (ratio - 1) / first) / log(ratio) + 1e-9)

schedules = {"flat": points_flat, "linear": points_linear, "geometric": points_geometric}
light, heavy = 5, 20   # post-cap hours per week
for weeks in (10, 52, 156):
    print(f"after {weeks} weeks ({light * weeks} h vs {heavy * weeks} h)")
    for name, f in schedules.items():
        nl, nh = f(light * weeks), f(heavy * weeks)
        pl, ph = 1 + VALUE * nl, 1 + VALUE * nh
        print(f"  {name:9} light {nl:4d}  heavy {nh:4d}  power ratio {ph / pl:.3f}")
```

| After | Schedule | Light points | Heavy points | Gap `G` |
|---|---|---|---|---|
| 10 weeks (50 h vs 200 h) | Flat | 5 | 20 | 1.143 |
| | Linear | 6 | 13 | 1.066 |
| | Geometric | 16 | 36 | 1.172 |
| 1 year (260 h vs 1,040 h) | Flat | 26 | 104 | 1.619 |
| | Linear | 15 | 31 | 1.139 |
| | Geometric | 41 | 67 | 1.184 |
| 3 years (780 h vs 3,120 h) | Flat | 78 | 312 | 2.315 |
| | Linear | 27 | 55 | 1.220 |
| | Geometric | 61 | 89 | 1.174 |

Check one row by hand. Flat at one year: `260 / 10 = 26` and `1,040 / 10 = 104`, so `G = 2.04 / 1.26 = 1.619`. Check the geometric ceiling. At three years the heavy player leads by `89 − 61 = 28` points, right at the `log_1.05 4 ≈ 28.4` limit.

Now read the table as a designer would.

1. **Early on, geometric is the most unequal.** After 10 weeks it has the largest gap, because its first points are cheap and the heavy player grabs many of them. Players who compare notes in the first month will think the geometric system is the harsh one.
2. **By year three the order has flipped completely.** Flat has passed `G = 2.3` and is still climbing toward 4. Suppose your encounters can serve a band of `F = 1.5`. Under flat costs, a light and a heavy player drift out of shared content within a year. Under geometric costs they never do.
3. **Linear is a slow version of flat.** Its gap keeps growing, toward 2, but slowly enough that three years only reach 1.22.

### The price: the reward stops arriving

The geometric schedule bounds the gap by making points expensive. Look at what the next point costs each player after three years.

| Schedule | Light player's next point | Weeks at 5 h/week | Heavy player's next point | Weeks at 20 h/week |
|---|---|---|---|---|
| Flat | 10 h | 2.0 | 10 h | 0.5 |
| Linear | 56 h | 11.2 | 112 h | 5.6 |
| Geometric | 39.2 h | 7.8 | 153.8 h | 7.7 |

The geometric row holds the surprise. After three years, both players wait almost exactly the same number of *weeks* for their next point, about 7.7. That is no coincidence. Under a geometric schedule, a player's next point costs roughly `(r − 1)` times everything they have played so far, so every player waits a fixed share of their own history. The schedule is fair in weeks and stingy for everyone. A point every two months is not a reward loop. It is a rounding error.

This is the real design tension. **The cost curve that keeps players together also starves them of rewards.** Flat costs feed the heavy player a point twice a week and split the population apart. Geometric costs hold the population together and turn the bar into wallpaper.

### A visual you can move

Open the interactive. The left panel plots points against weeks for both players under the schedule you choose. The right panel plots the gap `G` against weeks, with a dashed line at the band `F`. Switch between flat, linear and geometric without changing anything else. On the left, flat looks generous and geometric looks mean. On the right, the flat line crosses `F` and keeps going, while the geometric line rises fast, peaks and settles. Then open the "Next point" readout and slide to week 156 to see the cadence cost.

Drag the heavy player's hours from 20 up to 40. Under flat costs the long-run gap doubles. Under geometric costs the ceiling rises only from `log_r 4` to `log_r 8` points, from 28 to 43.

### Cross-game recognition

**Diablo III, Paragon 2.0 (patch 2.0.1, 2014, to the current game).** Paragon bounds the gap mainly on the value side. Three of the four categories stop giving anything after 50 points each. In our form, most of `v` is capped, and only the Core stats keep a constant `v` forever. Points keep arriving and keep being spendable, so the reward loop survives, while most of their power stops accumulating. It also keeps separate Paragon tallies for seasonal and non-seasonal play, which is week 11's reset applied to an account track. A new season starts everyone's seasonal Paragon from zero, so the season race is not decided by years of banked hours.

**Diablo Immortal, Paragon and the server level (launch in 2022 onward).** Diablo Immortal ties the cost of a point to a moving target. Each server has a World Paragon Level that rises by 10 levels a week. A player far below it earns experience at up to 15 times the normal rate. A player above it earns less and less, down to 1% of the normal rate once they are 19 or more levels ahead. In our form, the cost of the next point depends on the player's distance from a line that moves with the calendar. A heavy player can get only a few levels ahead of it before each level costs a hundred times more. The gap in levels is held to a narrow band around the server line. That is the geometric idea with the growth tied to the calendar instead of to the player's own history, and it is also a catch-up mechanic (week 6) for anyone below the line.

**EverQuest, AA experience (The Shadows of Luclin, December 2001).** EverQuest's AA split experience between levels and AA by a slider the player set. It makes the opportunity cost explicit. Every hour on AA was an hour not spent on levels, so AA's power competed with level power instead of simply adding to it. In our model the AA cost of a point includes the levels a player gave up.

Three designs, three ways to answer the same question. Diablo III bounds value per point. Diablo Immortal bounds how far anyone can pull ahead of the calendar. EverQuest makes the player pay for AA in the other currency. When you meet an endless track in a new game, ask the question in our terms. Is the long-run gap set by cost, by value, or by a moving cap?

### Eyes-open design judgment

- **Do not judge a schedule by its first month.** Early gaps and long-run gaps are ordered differently. Plot three years before you ship.
- **Decide your band first.** If your content assumes `F = 1.5`, a flat schedule with `v = 1%` and a 4-to-1 hours ratio breaks that band inside a year. Either change the schedule or lower `v`.
- **Separate the reward loop from the power loop.** The geometric row shows you cannot bound power and keep a steady reward cadence with one number per point. Keep points coming at a steady pace, and bound their power by capping or decaying value (section 3). Or hand out non-power rewards, such as cosmetics, titles or horizontal tools (week 3), on the steady clock.
- **Tie growth to the calendar when you can.** A moving target like Diablo Immortal's lets the whole population progress together, gives everyone behind it a catch-up bonus ([week 6](w06-catch-up-mechanics.md) covers these), and never lets the leaders run away. The price is that heavy players feel throttled, and some will say so loudly.

### Check yourself (worked example)

1. A flat schedule costs 8 hours per point at 0.5% each. The light player plays 5 hours a week, the heavy player 15. What is `G` after two years (104 weeks)? What value does `G` approach in the long run?
2. A geometric schedule has `a = 1` hour and `r = 1.1`. How many points ahead does a player with four times the hours end up, in the long run? After 1,040 hours, how many points does a player hold, and how long does their next point take?

<details>
<summary>Answers</summary>

1. Light: `520 / 8 = 65` points, `P = 1.325`. Heavy: `1,560 / 8 = 195` points, `P = 1.975`. `G = 1.975 / 1.325 ≈ 1.49`. Points tend to the hours ratio, 3, so `G` tends to 3 as `v × n` swamps the 1.
2. `log_1.1 4 = ln 4 / ln 1.1 ≈ 1.386 / 0.0953 ≈ 14.5` points. After 1,040 hours, `1.1^n ≤ 1 + 1,040 × 0.1 = 105`, so `n = floor(ln 105 / ln 1.1) = floor(48.8) = 48`. The next point costs `1.1^48 ≈ 97` hours, almost five weeks at 20 hours a week.

</details>

## 3. Bounding the value instead

The other place to bound the gap is the value of each point. Keep the cost flat, so points arrive at a steady pace, and make each point worth a little less than the last:

```
value of point k = v₀ × d^(k−1)
P(n) = 1 + v₀ × (1 − d^n) / (1 − d)
```

This is a geometric series, so total power can never exceed `1 + v₀ / (1 − d)`. With `v₀ = 2%` and `d = 0.98`, the ceiling is `1 + 0.02 / 0.02 = 2.0`. Half of the total bonus is earned by point `ln 0.5 / ln 0.98 ≈ 34`.

With flat costs of 10 hours per point, the same two players give:

| After | Light points | Heavy points | Light `P` | Heavy `P` | Gap `G` | Heavy player's next point is worth |
|---|---|---|---|---|---|---|
| 10 weeks | 5 | 20 | 1.096 | 1.332 | 1.216 | 1.34% |
| 1 year | 26 | 104 | 1.409 | 1.878 | 1.333 | 0.24% |
| 3 years | 78 | 312 | 1.793 | 1.998 | 1.114 | 0.004% |

The gap peaks at about 1.36 around week 35 and then shrinks, because the heavy player has hit the ceiling and the light player is still climbing toward it. Both players get a point every 10 hours forever. That is the cadence the geometric cost schedule could not give.

The cost is the last column. After three years, the heavy player's next point is worth four thousandths of a percent. The bar still fills and the number still goes up, but the reward is empty, and players who do the arithmetic know it. This is where Diablo III's design sits. After Paragon 800 the Core points are the only ones left. They keep a small, real value, but it is small next to what gear provides.

So neither side is free.

- **Bound the cost** and rewards dry up in real time.
- **Bound the value** and rewards keep arriving, but they empty out.

Most shipped games combine both with something outside power. A steady track of points whose power is capped or decaying, plus cosmetics, titles or horizontal tools on milestones, lets the bar keep meaning something after the power has stopped. Week 3 showed how to make horizontal rewards worth chasing. This is where you spend them.

## 4. Account progression: what belongs to the player

So far "the player" had one character. Most MMO players have several. Some want a character in each role (MMO303 week 5 showed why a queue needs them). Others want to try another class without giving up the first.

Every piece of progress belongs either to the account or to one character. The split decides what an alternate character, an **alt**, costs. A simple model makes the decision concrete. Let `T_c` be the hours to bring a character from the cap to endgame-ready, and let `s` be the share of that progress that is account-wide. Then:

```
first character   = T_c
each later alt    = (1 − s) × T_c
k characters      = T_c × (1 + (k − 1)(1 − s))
```

Take `T_c = 40` hours and four characters.

| Account-wide share `s` | First character | Each alt | Four characters |
|---|---|---|---|
| 0% | 40 h | 40 h | 160 h |
| 30% | 40 h | 28 h | 124 h |
| 60% | 40 h | 16 h | 88 h |
| 90% | 40 h | 4 h | 52 h |

Raising `s` from 0 to 60% nearly halves the cost of a full roster. That is a strong lever for a game that needs players to fill scarce roles, because the cheapest tank to recruit is the one already playing a damage dealer who would try tanking if it cost 16 hours instead of 40.

Shipped games move this lever deliberately.

- **Diablo III (patch 2.0.1 onward).** Paragon experience is shared by every character of the same type on the account (normal, hardcore, seasonal and so on). If a hardcore character dies, the Paragon experience it earned is not lost. A new character of the same type arrives with the account's full Paragon level. In the table's terms, Paragon has `s = 100%`.
- **World of Warcraft, Warbands (patch 11.0.0, July 2024, The War Within).** Blizzard made many reputations account-wide, added a shared Warband bank, shared flight-path knowledge and map exploration, and let any character collect transmog appearances regardless of armour type. Every one of these raises `s`. What stayed per character, such as gear and character level, is the part Blizzard chose to keep as `1 − s`.

### What account progression costs

A high `s` is not free.

- **Identity.** If everything is shared, a character is a skin on the account, and the pride of "my paladin earned this" fades. Players who play one character notice nothing. Players who played many alts under the old rules may feel their earlier effort was devalued.
- **Power gap on new characters.** Account-wide *power* reaches every new character at once. A returning veteran's fresh alt starts far above a new player's first character. If your band `F` matters in that content, account power should be capped or, as in Diablo III's seasons, kept in a separate tally.
- **Chores become one-time tasks.** When a reputation is shared, the grind is done once. That is kind to players and bad for any content that depended on being repeated. Plan to replace the hours you removed, or accept that players will spend fewer of them.

A good default is to share **access and convenience** (unlocks, maps, collections, storage) and keep **power earned in play** per character or capped. Then alts are cheap and the gap between characters stays inside the band.

## In-class activity (25 minutes)

Groups of three. Your MMO's encounters serve a band of `F = 1.35`. Post-cap players range from 4 to 24 hours a week. You must design one AA track.

1. Choose a cost schedule and a value rule. Use the interactive to check `G` over three years for a 4-hour and a 24-hour player. It must stay under `F` throughout.
2. Report the 24-hour player's weeks per point in year 3 and the value of their next point.
3. Add one non-power reward track that keeps a steady cadence for that player. Name what it gives and how often.
4. Decide your account-wide share `s` for the AA track and one other system. Justify each in one sentence.

Expected output: a short spec (schedule, parameters, value rule, reward track, `s` values) and the three numbers from steps 1 and 2.

## Common misconceptions

- **"An uncapped track means the gap grows forever."** Only if the cost per point is flat and the value per point is constant. A geometric cost holds the point gap at `log_r k`. A decaying value holds power under a ceiling.
- **"Steeper costs are always fairer."** They are fairer in the long run and less fair early on, because early points are cheap and heavy players grab them first. Check the first three months as well as the third year.
- **"If every point still counts, the reward loop is healthy."** A point every two months, or a point worth 0.004%, is not a reward. Measure cadence in weeks and value in real power.
- **"Account-wide progression removes the power gap problem."** It removes the gap between a player's own characters. It widens the gap between a veteran's fresh alt and a new player's first character.

## Check yourself

1. A game's AA track uses flat costs of 12 hours and 0.8% per point. Its content serves `F = 1.5`. A light player plays 6 hours a week and a heavy player 24. In which week does `G` first exceed 1.5? (Treat points as continuous to keep the arithmetic short.)
2. Under a geometric schedule with `r = 1.05`, the heavy player doubles their hours from 20 to 40 a week. By how many points does the long-run lead over a 5-hour player grow?
3. A decaying-value track has `v₀ = 3%` and `d = 0.97`. What is the power ceiling? How many points earn 90% of it?
4. A designer wants alts to cost at most a quarter of the first character. What account-wide share `s` does that need? Name one system you would keep per character anyway, and why.

<details>
<summary>Answers</summary>

1. After `w` weeks the light player holds `6w / 12 = 0.5w` points and the heavy player `2w`. `G = (1 + 0.008 × 2w) / (1 + 0.008 × 0.5w) = (1 + 0.016w) / (1 + 0.004w)`. Setting this to 1.5 gives `1 + 0.016w = 1.5 + 0.006w`, so `0.01w = 0.5` and `w = 50`. Just under a year.
2. The lead grows from `log_1.05 4 ≈ 28.4` to `log_1.05 8 ≈ 42.6` points, by about 14.2, which is `log_1.05 2`.
3. Ceiling `1 + 0.03 / 0.03 = 2.0`. For 90%, `1 − 0.97^n = 0.9`, so `n = ln 0.1 / ln 0.97 ≈ 75.6`, about 76 points.
4. `(1 − s) ≤ 0.25`, so `s ≥ 75%`. A reasonable answer keeps gear, or any power earned in rated play, per character, so a veteran's new alt does not start with power the band cannot absorb.

</details>

## Lab hook

[Lab 12, designing an AA track](../labs/lab12.md). You implement the three cost schedules and three value rules, evaluate a light and a heavy player over three years, and search for a design that meets five targets at once (gap, peak gap, early points, heavy cadence and a minimum value for late points). You will find that three of them cannot hold together. Your report chooses which to relax and defends it with numbers. The lab feeds the progression analysis assessment.

## Sources

- EverQuest Wiki, "The Shadows of Luclin" and "Alternate Advancement" (expansion released 4 December 2001). Alternate Advancement introduced with Luclin; past level 50, players allocate a percentage of experience to a separate bar for abilities, stats and tradeskill bonuses.
- Diablo Wiki, "Paragon", Diablo III section (Paragon 2.0, patch 2.0.1, 2014, pre-patch for Reaper of Souls). No level cap; account-wide per game type, with separate normal, hardcore and seasonal tallies; one point per level, rotating through Core, Offensive, Defensive and Utility; all stats except primary stat and vitality capped at 50 points; after Paragon 800 all further points go to Core; primary stat and vitality +5 per point; Paragon experience kept if a character dies.
- Diablo Wiki, "Paragon", Diablo Immortal section (launch 2022 onward, accessed September 2026). Server World Paragon Level rising 10 levels per week; experience rate from 1,500% far below the server level to 1% at 19 or more levels above.
- Diablo Wiki, "Season" (Diablo III, patch 2.1.0, August 2014). Seasonal characters have their own Paragon experience, merged into the non-seasonal pool when the season ends.
- Warcraft Wiki, "Warband" (patch 11.0.0, 23 July 2024, The War Within). Account-wide reputations, Warband bank, shared flight paths and map exploration, transmog appearances collectable regardless of armour type. https://warcraft.wiki.gg/wiki/Warband
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press. Progression in PvE games.

## Interactive spec: examples/w12-aa-gap.html

**The one insight.** The cost curve of an endless track decides the long-run gap between a light and a heavy player. Flat costs let the gap grow toward the ratio of hours, linear toward its square root, and geometric costs stop the lead at a fixed number of points. The schedule that holds players together also slows every player's rewards to the same crawl.

**Layout.** Two linked charts, side by side from 900px, stacked on mobile, with a readout table below.

**Left chart, "Points over time".** x-axis weeks 0 to 156. y-axis points (auto scale). Two step lines, light and heavy player, for the selected design. Optional toggle to overlay the other two schedules in muted colors.

**Right chart, "Power gap G".** x-axis weeks 0 to 156. y-axis `G` from 1.0 to 3.0. The selected design's `G(w)` as a line. A dashed horizontal line at the band `F`. Shade the region above `F`. Mark the first week `G > F`, if any.

**Controls.**
- Schedule: flat / linear / geometric (segmented control).
- Flat cost `a`: 2 to 40 h, default 10. Linear step: 0.5 to 10 h, default 2. Geometric first cost: 0.5 to 10 h, default 2; ratio `r`: 1.01 to 1.20, step 0.01, default 1.05.
- Value rule: constant (`v`, 0.1% to 3%, default 1%) or decaying (`v₀` default 2%, `d` 0.90 to 0.999, default 0.98).
- Light hours per week: 1 to 20, default 5. Heavy hours per week: 5 to 60, default 20.
- Band `F`: 1.1 to 3.0, step 0.05, default 1.5.
- Week slider for the readout: 1 to 156, default 156.

**Formulas.**
- Cost of point `n`: flat `a`; linear `step × n`; geometric `first × r^(n−1)`.
- Points after `h` hours: largest `n` with the cumulative cost ≤ `h` (loop, with a 1e-9 tolerance).
- Power: constant `1 + v × n`; decaying `1 + v₀ (1 − d^n)/(1 − d)`.
- `G(w) = P(points(heavy × w)) / P(points(light × w))`.
- Next point, in weeks, for each player at the readout week: `cost(n + 1) / hours per week`. Value of the next point: `v` or `v₀ × d^n`.
- Long-run note shown under the chart: flat "points ratio → hours ratio", linear "→ √(hours ratio)", geometric "lead → log_r(hours ratio) points".

**Readout table (at the selected week).** Light and heavy points, light and heavy `P`, `G`, max `G` so far, weeks to next point for each player, value of each player's next point.

**Test values (must match the lecture).** Defaults (light 5, heavy 20, `v = 1%`):
- Flat 10 h: week 52 → 26 and 104 points, `G = 1.619`; week 156 → 78 and 312, `G = 2.315`.
- Linear step 2: week 156 → 27 and 55, `G = 1.220`.
- Geometric 2 h, `r = 1.05`: week 10 → 16 and 36, `G = 1.172`; week 156 → 61 and 89, `G = 1.174`; next point 39.2 h (7.8 weeks) light, 153.8 h (7.7 weeks) heavy.
- Flat 10 h with decaying `v₀ = 2%`, `d = 0.98`: week 52 → `G = 1.333`; week 156 → `G = 1.114`, heavy next point worth 0.004%.

**First screen.** Geometric and flat both drawn on the right chart (flat muted), readout at week 156, so the student sees flat crossing `F = 1.5` and geometric staying under it, and the cadence cells showing 7.7 weeks.

**Accessibility.** All controls keyboard operable, with labels and live values. An `aria-live` sentence summarises the readout ("Week 156, geometric: heavy leads by 28 points, G = 1.17, next point in 7.7 weeks"). No animation under `prefers-reduced-motion`.

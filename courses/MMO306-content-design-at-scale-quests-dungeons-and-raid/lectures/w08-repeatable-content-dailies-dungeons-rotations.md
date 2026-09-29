# MMO306 · Week 08 — Repeatable Content: Dailies, Dungeons, Rotations

**Why this matters:** You can't author content as fast as players finish it, so most of what an MMO player does in a given week is something they have done before. Repeatable content works only if you control two things: how soon it starts to feel the same, and how fast players earn from it. Both are numbers. The first decides when "today's quests" turns into "these quests again." The second decides what happens to a player who misses a week.

**You will be able to:**
- Compute how quickly a daily or weekly rotation exposes its pool, and how much of yesterday's offer repeats today.
- Size a rotation pool for a freshness target, and compare random draws with a fixed cycle.
- Compare hard weekly caps with accumulating caps and predict what each does for a player who misses weeks.
- Compute the reward-per-hour curve of a first-run bonus, and critique the chore any reset-based reward creates.

**Before class:** Warcraft Wiki, "Daily quest" (the history section, about 10 minutes). Final Fantasy XIV wiki (consolegameswiki), "Allagan Tomestones" (the two caps, 5 minutes). Reread [UX201 week 5](../../UX201-game-ux-and-player-psychology/lectures/w05-reinforcement-schedules-and-ethics.md), section 3, on when a reward schedule becomes a problem.

**Prerequisites from earlier courses:** [GD202 week 7, quest types and the drop-rate tax](../../GD202-narrative-and-quest-design/lectures/w07-quest-types-and-redeeming-them.md) (why a single repeated quest goes stale, and how to fix it). [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md). [MA102 week 10, pseudo-random distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w10-pseudo-random-distribution-and-pity-timers.md) (shuffled decks versus independent rolls). [GD102 week 2, stocks and flows](../../GD102-systems-design-and-game-mechanics/lectures/w02-stocks-and-flows.md). From this course, [week 1, the content treadmill](w01-the-content-treadmill-production-vs-consumption.md) (the replay multiplier and the weekly gate `g`) and [week 2, quest hubs](w02-quest-hubs-and-zone-pacing.md) (hub layout for one-time quests).

**Interactive:** [`examples/w08-rotation-wear.html`](../examples/w08-rotation-wear.html). Keep it open during section 2.

---

## 1. Why games repeat themselves

Week 1 set the problem. A drop that took a team months is exhausted by its fastest players in days, and the replay multiplier `r` is how a studio stretches authored hours. **Repeatable content** is content designed to be played many times: daily quests, dungeons run for gear, weekly raid bosses, rotating activities. It turns a fixed stock of authored content into a flow of play hours.

Repeatable content is built from four parts. The rest of the lecture uses these words exactly.

- A **reset** is the moment a repeatable becomes available again. World of Warcraft resets daily quests at a fixed time per region (for example 15:00 UTC for the US region) and raids once a week.
- A **lockout** limits how often a player can earn from one piece of content between resets. In World of Warcraft, raids, world bosses and Mythic dungeons have weekly lockouts, and Heroic dungeons entered directly have daily ones. A boss you killed this week stays dead for you until the reset.
- A **cap** limits how much of a currency a player can earn in a period, however many activities they do. Final Fantasy XIV's newest tomestone currency usually has a weekly limit of 450.
- A **rotation** changes which repeatables are on offer each day or week, so a fixed pool of authored content feels less repetitive.

Week 1 already showed the most important fact about caps and gates: a weekly gate slows only the players above it and leaves everyone below untouched. This week does not repeat that. It adds the two questions week 1 left open. How fast does a rotation wear out (section 2)? And what should happen to a player who misses a week (section 4)?

## 2. Worked example: how fast a rotation wears out

### The hook

World of Warcraft has tried three daily-quest designs that are easy to compare.

- In The Burning Crusade (patch 2.4), the Shattered Sun Offensive offered up to 19 daily quests, the same ones every day.
- In Cataclysm, the Tol Barad Peninsula quest givers offered 6 quests a day from a pool of 22.
- In patch 4.2, the Firelands Invasion hubs offered up to 18 quests a day from a pool of 55.

Which of the last two feels fresher the next morning? It is tempting to pick Firelands, whose pool is two and a half times larger. The numbers say the opposite. On a typical morning, a larger share of the Firelands offer is a repeat of yesterday's, and a Firelands player also runs through the whole pool sooner. The pool's size is not what decides freshness.

### The model

A rotation has a pool of `S` repeatables and offers `a` of them each period (a day for dailies, a week for weekly content). Assume each period's offer is a fresh random draw of `a` from the pool. The letters differ from week 2's hub model on purpose: `S` is the size of a repeatable pool, `a` is what the board offers each period.

The key quantity is the **draw share**, `p = a / S`, the fraction of the pool on offer at once. Two things follow from it.

**Repeat share.** Each quest on today's board has a chance `p` of having been on yesterday's board. So

```
expected repeats from yesterday = a × p = a² / S
repeat share                    = p
```

**Exposure.** The share of the pool a player has been offered at least once after `d` periods. A given quest is left off one board with probability `1 − p`, so by the complement rule (MA102 week 3)

```
exposure  X(d) = 1 − (1 − p)^d
```

Turn it around to find how many periods it takes to reach an exposure `x`, or how big a pool you need to hold exposure below `x` for `d` periods:

```
periods to reach x    d = ln(1 − x) / ln(1 − p)
pool size needed      S = a / (1 − (1 − x)^(1/d))
```

Every symbol:

- `S`, the number of repeatables in the pool.
- `a`, the number offered per period.
- `p = a / S`, the draw share.
- `d`, the number of periods (days or weeks) a player has played.
- `X(d)`, the share of the pool the player has seen by then.

Exposure is not the same as staleness. A great quest can be seen ten times. But when `X` nears 100%, every new board is assembled from things the player has already seen, and the only remaining novelty is the combination.

### Numbers you can check

| Rotation | `S` | `a` | `p` | Repeats from yesterday | `X(1)` | `X(3)` | `X(7)` | Periods to 90% |
|---|---|---|---|---|---|---|---|---|
| Shattered Sun (fixed) | 19 | 19 | 1.000 | 19 of 19 | 100% | 100% | 100% | 1 |
| Tol Barad | 22 | 6 | 0.273 | 1.6 of 6 | 27.3% | 61.5% | 89.2% | 7.2 |
| Firelands Invasion | 55 | 18 | 0.327 | 5.9 of 18 | 32.7% | 69.6% | 93.8% | 5.8 |
| Tol Barad with pool doubled | 44 | 6 | 0.136 | 0.8 of 6 | 13.6% | 35.6% | 64.2% | 15.7 |

The rotation columns assume a fresh random draw each day. That is a modeling assumption, not a documented rule of those hubs.

Check one row by hand. Tol Barad, day 3: `1 − (16/22)^3 = 1 − 0.3847 = 0.615`. Periods to 90%: `ln 0.1 / ln(16/22) = −2.303 / −0.318 = 7.2`.

Now the hook's answer. Firelands has `p = 0.327` and Tol Barad has `p = 0.273`. The larger pool offers a larger share of itself each day, so it repeats more of yesterday's board (33% against 27%) and reaches 90% exposure more than a day sooner. **Freshness is set by the draw share `p`, not by the pool size.** Two rotations with the same `p` wear out along the same curve, however large they are.

The last row shows the price of freshness. Doubling Tol Barad's pool to 44 while keeping 6 a day halves `p`, and the days to reach 90% exposure more than double, from 7.2 to 15.7. Every one of those 22 extra quests has to be written, built and tested. You buy freshness with authored content, at a rate the formula tells you in advance.

### Random draw or fixed cycle

A rotation doesn't have to be random. A **fixed cycle** deals the pool out like a deck: each period takes the next `a` quests, and the cycle restarts only when all `S` have been shown. MA102 week 10 compared the same two options for crits and drops, independent rolls against a shuffled deck.

| Tol Barad pool (`S = 22`, `a = 6`) | Repeats from yesterday | Exposure day 3 | Day on which the whole pool has been seen |
|---|---|---|---|
| Random draw each day | 1.6 on average | 61.5% | Uncertain; 89.2% by day 7 |
| Fixed cycle | 0 | 81.8% (18 of 22) | Day 4 |

A fixed cycle never repeats within a cycle and exposes the pool at the fastest possible rate, `min(1, d × a / S)`. A random draw repeats quests but exposes the pool more slowly, and a player can never be sure when a particular quest will come back. Neither is better. A fixed cycle is predictable, so players can plan ("the good quest is back on Thursday"), and it guarantees every authored quest is seen. A random draw spreads exposure over more days, at the cost of occasional runs of the same quests on consecutive days.

### A visual you can move

Open the interactive. The left panel is the quest board: `S` small cards in a grid. Each day, `a` cards light up as today's offer, cards that were also on yesterday's board get a repeat marker, and cards the player has ever been offered turn solid. A "next day" button and an autoplay control step through the days. The right panel plots exposure `X(d)` against days for the current settings, with the reference curves for Tol Barad and Firelands drawn faintly.

Set `S = 22` and `a = 6`, then step through a week. Now set `S = 44` and `a = 12`. The board is twice as large, yet the curve on the right lies exactly on top of the Tol Barad curve, because `p` is the same. Switch to "fixed cycle" and the curve becomes a straight ramp that hits 100% on day 4, with no repeat markers on the board.

### Cross-game recognition

**World of Warcraft, Island Expeditions (Battle for Azeroth, patch 8.2).** By 8.2 there were 11 islands in rotation, with 3 available each week. That is `p = 3/11 = 0.273`, exactly Tol Barad's draw share, on a weekly clock instead of a daily one. The same curve applies: about 61.5% of the islands seen after three weeks, 89.2% after seven, if each week's three were a fresh random draw. The expeditions also randomize the enemies on each island, which adds variety inside each run. Week 9 measures that second kind of variety.

**World of Warcraft, daily quest limits (The Burning Crusade to Mists of Pandaria).** Daily quests arrived in patch 2.1 with a limit of 10 completions a day. Patch 2.4 raised it to 25, because the Shattered Sun quests alone added up to 19 more a day. Patch 5.0.4 removed the limit. In Cataclysm, rotating hubs such as Tol Barad replaced fixed sets. In this lecture's terms, early designs had `p = 1` and relied entirely on the quality of each quest. Later designs lowered `p` and paid for it with larger pools.

**Final Fantasy XIV, Duty Roulette (introduced patch 2.1).** A roulette sends a player into a randomly chosen duty from a category and pays a daily bonus for doing so. Here `a = 1` per run and `S` is the number of duties in the category, so every run is a draw with `p = 1/S`. The design goal differs from a quest board. The roulette also spreads players across old duties that would otherwise have empty queues. Section 5 models its daily bonus.

Three games, three clocks, one curve. When you meet a rotation, find `S`, `a` and the period, and compute `p`.

### Eyes-open design judgment

- **Set a freshness target, then size the pool.** Write the target as an exposure: "a player who does every daily should not have seen more than 75% of the pool in the first week." With `a = 6` that needs `S = 6 / (1 − 0.25^(1/7)) ≈ 33.4`, so 34 quests. Now you know the authoring cost before you start.
- **A bigger board is not a fresher board.** If you raise `a` to give players more to do each day, raise `S` in proportion or `p` goes up and the rotation wears out faster.
- **Choose random or cycle for the player, not the spreadsheet.** Cycles suit content players plan around (a weekly rotation of raids or bosses). Random draws suit small tasks where surprise is part of the appeal. Randomness with no memory will sometimes offer the same quest four days in a row. If that would feel broken, add a rule such as "not offered yesterday," which is a small step toward a cycle.
- **Exposure is a floor on staleness, not a measure of fun.** A pool at 100% exposure can stay enjoyable if each quest plays differently every time. GD202 week 7 covered how to redesign a single quest for that. Rotation math tells you when you start depending on it.

## 3. Caps and lockouts: what week 1 already showed

Week 1 modeled a weekly gate `g` in hours of useful play and showed that it collapses the top of the distribution onto one value while leaving the median alone. A currency cap is the same thing measured in rewards. If repeatables pay `r_c` currency per hour and the weekly cap is `C`, the cap binds above

```
h* = C / r_c
```

hours a week, and `h*` plays the role of week 1's `g`. (This lecture writes the earning rate as `r_c` so it doesn't clash with week 1's replay multiplier `r`.)

A real example makes the size of the effect concrete. In Final Fantasy XIV's Dawntrail expansion, the capped tomestone of patches 7.05 and 7.1 was the Allagan Tomestone of Heliometry, which bought item level 720 gear. Head, hands and feet cost 495 each, body and legs 825 each, and each of five accessories 375:

```
3 × 495 + 2 × 825 + 5 × 375 = 5,010 tomestones
```

Under the usual weekly limit of 450, the full set took at least `5,010 / 450 ≈ 11.1`, so 12 weeks, for anyone whose play time earned the 450. A player who fills the cap in an evening and one who needs all week finish the same day.

The same shape appears in other forms:

- **Raid lockouts (World of Warcraft, current).** One kill per boss per difficulty per week, so loot chances per week are `min(kills attempted, 1)`. A cap with `C = 1`.
- **The Great Vault (World of Warcraft, Shadowlands onward).** Up to 9 item options each week based on the previous week's raid bosses, dungeons and world activities, of which the player claims one. More activity buys more choice, while the reward stays capped at one item.
- **FFXIV's cap raise.** Near the end of each expansion's final patch cycle, the weekly tomestone limit has been raised to 900 (for example in patches 3.56, 4.56, 5.57 and 6.57). In week 1's terms, the gate opens late, when the content is oldest, which helps anyone still behind.

## 4. Hard caps and accumulating caps: forgiving a missed week

A **hard weekly cap** resets every week, and anything not earned is lost. An **accumulating cap** grows every week, and the player may earn up to the running total:

```
hard cap:         earned in week w ≤ C
accumulating cap: total earned by week w ≤ C × w
```

They differ only for a player who misses weeks. Take an invented game with `r_c = 60` currency per hour, `C = 450` and a goal of `G = 3,600`. A player with 30 hours a week earns 1,800 uncapped, far above the cap. They are away for weeks 1 to 3 and play normally from week 4.

| Week | Hard cap: earned that week | Hard cap: total | Accumulating cap: allowed total | Accumulating cap: earned that week | Accumulating cap: total |
|---|---|---|---|---|---|
| 1 to 3 | 0 | 0 | 1,350 | 0 | 0 |
| 4 | 450 | 450 | 1,800 | 1,800 | 1,800 |
| 5 | 450 | 900 | 2,250 | 450 | 2,250 |
| 6 | 450 | 1,350 | 2,700 | 450 | 2,700 |
| 7 | 450 | 1,800 | 3,150 | 450 | 3,150 |
| 8 | 450 | 2,250 | 3,600 | 450 | 3,600 |

Under the hard cap this player reaches 3,600 in week 11. Under the accumulating cap they reach it in week 8, the same week as a player who never missed. In week 4 they earned four weeks' worth, because their hours were enough to fill the backlog.

Now take a player with 8 hours a week (480 uncapped) and the same three missed weeks. Under the accumulating cap, week 4 allows 1,800 but they can earn only 480. They never catch up to the allowance, because 480 is barely above 450, and they finish in week 11 either way. **An accumulating cap forgives missed weeks only for players with spare hours.** It still removes the "log in or lose it" pressure for everyone, which is reason enough to prefer it for most currencies. It does not rescue players whose hours sit close to `h*`.

The design decision is what a missed week should cost. Under a hard cap, a missed week is lost for good, and players feel that as an obligation to log in. Under an accumulating cap, a missed week is postponed. FFXIV's late cap raise is a third answer: missed weeks cost you until the raise, then much less.

## 5. Repeatable dungeons: the first-run bonus

Dungeons repeat differently from quests. Players can often run them without limit, so you shape the flow through reward per run rather than through a lockout. A common tool is the **first-run bonus**, an extra reward for the first completion each day. Final Fantasy XIV's Duty Roulette pays one on top of the duty's normal reward.

Model it. Each run takes `t` hours and pays a base reward `b`. The first run of the day also pays a bonus `B`. After `n` runs in a day, the average reward per hour is

```
reward per hour = (B + n × b) / (n × t)
```

With `t = 0.5`, `b = 40` and `B = 100`:

| Runs today `n` | Total reward | Reward per hour |
|---|---|---|
| 1 | 140 | 280 |
| 2 | 180 | 180 |
| 3 | 220 | 147 |
| 6 | 340 | 113 |

The first run pays 280 per hour, and every later run pays only 80 per hour. A bonus this large relative to `b` teaches players to do exactly one run a day and log off. That can be what you want. It spreads play across days and fills queues with a steady mix of players, and when the duty is picked at random it sends players into old content that would otherwise have empty queues.

The cost is the chore. A daily bonus is a daily hard cap in disguise: its value is lost if not claimed, so it carries the same obligation to log in. Make `B` too large and the daily run feels like a tax on the player's time. UX201 week 5 gave you the checklist for deciding when that pressure has gone too far.

## In-class activity (25 minutes)

In groups of three. Materials: the interactive.

1. Design a daily hub where a player sees at most 60% of the pool in the first 5 days, with 5 quests on offer each day. Give `S`. Then compute the expected repeats from yesterday.
2. Your producer can fund only 20 quests. Keep `a = 5` and compare random draw with a fixed cycle on three numbers: repeats from yesterday, exposure on day 3, and the day the pool is fully seen. Recommend one and give a reason a player would notice.
3. A weekly currency has a hard cap of 500. Players complain about losing progress over holidays. Redesign it as an accumulating cap and compute when a player with 20 hours a week at 50 per hour, who misses two weeks, reaches a goal of 4,000.
4. Name the chore each of your three designs creates, in one line each.

Expected output: a pool size with its repeat count, a random-versus-cycle recommendation, a week number, and three one-line chores.

## Common misconceptions

- **"A bigger pool is always fresher."** Freshness depends on the draw share `p = a / S`. A pool of 55 that offers 18 a day repeats more of yesterday's board than a pool of 22 that offers 6.
- **"Random rotations expose content faster than fixed ones."** The reverse. A fixed cycle shows every item before repeating any. Randomness wastes some draws on repeats.
- **"An accumulating cap means nobody falls behind."** Only players with spare hours can fill the backlog. Players near `h*` finish no sooner.
- **"A daily bonus is free extra reward."** It is reward that expires daily, so it acts like a daily cap and carries the same pressure to log in.

## Check yourself

1. A weekly rotation offers 2 of 8 bosses each week, drawn at random. What share of the bosses has a player been offered after 4 weeks? How many weeks until 90%? How would a fixed cycle change both answers?
2. A designer doubles a hub's daily offer from 6 to 12 quests to "give players more to do," keeping the pool at 22. Compute `p`, the repeats from yesterday, and the exposure on day 2. What should they have done with the pool?
3. Final Fantasy XIV raises the weekly tomestone limit from 450 to 900 late in an expansion. A capped player has 1,000 of the 5,010 tomestones needed for the Heliometry set in section 3. How many more weeks do they need before and after the raise?
4. In section 4's example, the 30-hour player misses 5 weeks instead of 3. In which week do they reach 3,600 under each cap?
5. Using section 5's numbers (`t = 0.5`, `b = 40`), what bonus `B` makes the first run of the day pay three times the reward per hour of every later run? With that `B`, what is the average reward per hour after two runs?

<details>
<summary>Answers</summary>

1. `p = 2/8 = 0.25`. `X(4) = 1 − 0.75^4 = 1 − 0.316 = 68.4%`. Weeks to 90%: `ln 0.1 / ln 0.75 = 8.0`. A fixed cycle shows all 8 by week 4 (100%), with no repeats until week 5.
2. `p = 12/22 = 0.545`. Repeats from yesterday: `12 × 0.545 = 6.5` of 12. `X(2) = 1 − 0.455^2 = 79.3%`. To keep Tol Barad's `p = 0.273`, the pool should double to 44.
3. They need `5,010 − 1,000 = 4,010`. At 450 a week, `4,010 / 450 ≈ 8.9`, so 9 weeks. At 900 a week, `4,010 / 900 ≈ 4.5`, so 5 weeks.
4. Hard cap: 8 weeks of 450 starting in week 6, so week 13. Accumulating cap: in week 6 the allowance is `450 × 6 = 2,700`, and they earn 1,800 (their full week). Week 7 allows 3,150 and they reach it. Week 8 allows 3,600, so they finish in week 8, again with no delay.
5. Later runs pay `b / t = 40 / 0.5 = 80` per hour. The first run pays `(B + 40) / 0.5`. Setting that to `3 × 80 = 240` gives `B + 40 = 120`, so `B = 80`. After two runs the average is `(80 + 80) / 1.0 = 160` per hour.

</details>

## Lab / assignment hook

[Lab 08, rotations and caps](../labs/lab08.md). You implement rotation exposure (random draw and fixed cycle) and check it against a simulation, size a pool for a freshness target, then run hard and accumulating caps against 16 weeks of play logs for 400 invented players to see who each cap delays. Your final dungeon (60%) must state its repeat structure (rotation, lockout, cap or bonus) with the numbers from this lab.

## Sources

- Warcraft Wiki, "Daily quest" (history and patch changes). Limit of 10 in patch 2.1, 25 in patch 2.4, removed in patch 5.0.4; the fixed Shattered Sun set of 19; Tol Barad's 6 of 22 in Cataclysm; Firelands Invasion's up to 18 of 55 in patch 4.2; regional reset times. https://warcraft.wiki.gg/wiki/Daily_quest
- Warcraft Wiki, "Island Expedition" (Battle for Azeroth; islands added in patches 8.1 and 8.2). 11 islands in rotation with 3 available each week; enemies on each island are randomized. https://warcraft.wiki.gg/wiki/Island_Expedition
- Warcraft Wiki, "Lockout" (current). Weekly lockouts for raids, world bosses and Mythic dungeons; daily lockouts for Heroic dungeons. https://warcraft.wiki.gg/wiki/Lockout
- Warcraft Wiki, "Great Vault" (Shadowlands to Midnight). Up to 9 options each week from the previous week's activity; one item may be claimed. https://warcraft.wiki.gg/wiki/Great_Vault
- Final Fantasy XIV Online wiki (consolegameswiki), "Allagan Tomestones" (current). The newest tomestone usually has a weekly limit of 450, originally 300 in patch 2.1; the limit is raised to 900 near the end of an expansion's final patch cycle (patches 3.56, 4.56, 5.57, 6.57); at most 2,000 of each tomestone held. https://ffxiv.consolegameswiki.com/wiki/Allagan_Tomestones
- Final Fantasy XIV Online wiki, "Allagan Tomestone of Heliometry" (Dawntrail, introduced patch 7.05). Item level 720 gear prices: head, hands and feet 495; body and legs 825; each accessory 375. https://ffxiv.consolegameswiki.com/wiki/Allagan_Tomestone_of_Heliometry
- Final Fantasy XIV Online wiki, "Duty Roulette" (introduced patch 2.1). A randomly selected duty from a category, with daily bonus rewards. https://ffxiv.consolegameswiki.com/wiki/Duty_Roulette

## Interactive spec: examples/w08-rotation-wear.html

**The one insight.** Rotation freshness is set by the draw share `p = a / S`, not by pool size. Two boards with the same `p` wear out along the same curve, and a fixed cycle wears out fastest but never repeats.

**Layout.** Two linked panels, side by side on desktop, stacked on mobile (board first).

- **Left panel, "The quest board."** A grid of `S` small cards (numbered, generic icons, no game art). State per card: never offered (outline, `--grid`), offered before (solid `--steel` at low opacity), on today's board (solid `--ochre`), and on today's board *and* yesterday's (today's style plus a small `--blood` corner marker and the text "repeat" for screen readers). Above the grid: "Day d", "today: a quests, R repeats from yesterday", "seen: k of S (X%)".
- **Right panel, "Exposure over time."** x-axis: day 0 to 20. y-axis: exposure 0% to 100%. Plot the expected curve `X(d) = 1 − (1 − p)^d` for the current settings in `--ochre`, and for "fixed cycle" mode the ramp `min(1, d × a / S)`. Faint reference curves for Tol Barad (22, 6) and Firelands (55, 18), labeled. Plot the simulated player's actual exposure as dots on the current curve's color. A horizontal dashed line at 90% with the label "90% at day D" where `D = ln 0.1 / ln(1 − p)` (one decimal; in cycle mode `ceil(0.9 × S / a)`).

**Controls.**

- Pool size `S`: slider 5 to 80, step 1, default 22.
- Offer per day `a`: slider 1 to 30, step 1, default 6, clamped to `a ≤ S`.
- Mode: radio "Random draw each day" / "Fixed cycle" / "Random, not offered yesterday" (draw `a` from the items not on yesterday's board; if fewer than `a` remain, fill from the rest).
- Buttons: "Next day", "Autoplay" (one day per 0.7 s; disabled when `prefers-reduced-motion` is set, then "Next day" only), "Reset", "New seed".
- Preset buttons: Shattered Sun (19, 19), Tol Barad (22, 6), Firelands (55, 18), Island Expeditions (11, 3, relabel days as weeks), Tol Barad doubled (44, 6).

**Formulas.** `p = a / S`. Expected repeats from yesterday `= a × p` (random) or 0 (cycle, except on the day the cycle restarts). `X(d) = 1 − (1 − p)^d`. Simulation uses a seeded PRNG (for example mulberry32) so "Reset" replays the same days. The "not offered yesterday" mode has no closed form. Its expected curve is the average of 400 seeded runs (seeds 9001 to 9400), its expected repeats are `max(0, 2a − S)`, and its 90% mark is the first whole day whose averaged exposure reaches 90%. A footer note must say the curve is simulated.

**Test values** (expected, not simulated):

| `S` | `a` | Mode | `p` | Repeats | `X(1)` | `X(3)` | `X(7)` | 90% day |
|---|---|---|---|---|---|---|---|---|
| 22 | 6 | random | 0.273 | 1.64 | 27.3% | 61.5% | 89.2% | 7.2 |
| 55 | 18 | random | 0.327 | 5.89 | 32.7% | 69.6% | 93.8% | 5.8 |
| 44 | 12 | random | 0.273 | 3.27 | 27.3% | 61.5% | 89.2% | 7.2 |
| 44 | 6 | random | 0.136 | 0.82 | 13.6% | 35.6% | 64.2% | 15.7 |
| 22 | 6 | cycle | — | 0 | 27.3% | 81.8% | 100% | 4 |
| 8 | 2 | random | 0.250 | 0.50 | 25.0% | 57.8% | 86.7% | 8.0 |
| 22 | 6 | not yesterday | 0.273 | 0 | 27.3% | ≈71.6% | ≈95.6% | 6 |
| 55 | 18 | not yesterday | 0.327 | 0 | 32.7% | ≈82.2% | ≈98.8% | 4 |

The two "not yesterday" rows come from 40,000 simulated runs; the 400-run average in the page may differ by about half a point.

**First screen.** Tol Barad preset on day 3 of a fixed seed, with the right panel showing the Tol Barad and Firelands curves and a note under the chart: "Firelands has the bigger pool, and the steeper curve." Caption under the title: "Change the pool. Watch the curve, not the board."

**Accessibility.** Cards are not focusable individually; the board has a text summary in an `aria-live="polite"` region. All controls keyboard operable with visible focus. Card states use fill, outline and the corner marker, not color alone.

# MMO306 · Week 01 — The Content Treadmill: Production vs Consumption

**Why this matters:** A team spends half a year building a raid, and some players finish it in an afternoon. If you plan content by asking "how long does it take to play?", you will always lose that race. The useful question is how long each kind of player takes to run out, and what you can build so that the answer is "later than the next patch."

**You will be able to:**
- Compute the exhaustion time `T` and the locust ratio `P / T` for players at different percentiles of weekly play time.
- Derive how a replay multiplier and a weekly gate change `T`, and explain why a gate compresses the spread between percentiles.
- Critique a content plan from a shipped MMO (World of Warcraft, Final Fantasy XIV, Destiny 2) by naming which lever it pulls: cadence, replay or gate.
- Design a content drop whose median player still has something new to do when the next drop arrives.

**Before class:** Browse the Raider.IO hall of fame for the World of Warcraft raid Nerub-ar Palace (15 minutes, raider.io). Look at the kill dates and kill counts for the last boss on each difficulty. Final Fantasy XIV Online Wiki, "Patches" (10 minutes, note the gap between major patches). Reread your notes on the treadmill from MMO301 week 4.

**Prerequisites from earlier courses:** [MMO301 week 4, EverQuest, the treadmill and the raid](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w04-everquest-the-treadmill-and-the-raid.md) defined the progression treadmill. This week measures how fast players run on it. [GD203 week 7, XP curves](../../GD203-combat-and-progression-design/lectures/w07-xp-curves.md) designed a level curve backwards from a play-time target. Here the target is calendar days, not hours. [MA102 week 12, descriptive statistics](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md) covered percentiles, which we use to describe the player population.

**Interactive:** [`examples/w01-content-locust.html`](../examples/w01-content-locust.html). Keep it open during section 2.

---

## 1. Two clocks

Every online game with a live team runs on two clocks at once.

The **production clock** is the team's. It measures how long it takes to design, build, test and ship a **content drop**, a batch of new things to do released together. A drop can be a patch with one raid, an expansion with ten zones, or a season with a new dungeon rotation. The time from one drop to the next is the **cadence**, which we write `P` and measure in days.

The **consumption clock** is the player's. It measures how long a player takes to exhaust a drop, meaning to finish everything in it that still gives them something they want. That time depends on the player. Some play 5 hours a week, some play 50. We write it `T`, also in days.

Players and developers have a name for the fast end of the consumption clock: **content locusts**, players who strip a new release bare and then ask what's next. The name is unfair to the players. They are doing what the game rewards. It is also a good description of the design problem. Production is slow and serial. Consumption is fast and happens for every player at once.

A few more terms carry this week.

- **Content hours** `C` is how many hours of play a drop holds for a player who plays it once, start to finish, at the difficulty they choose. It is a first-pass number. It counts the first clear, not the tenth.
- **Replay multiplier** `r` is the number of hours players actually spend per hour of first-pass content, because they repeat it. Repeatable dungeons, higher difficulty tiers, random loot and alternative characters all raise `r`. A story you read once has `r = 1`.
- A **gate** is any rule that limits how much of a drop a player can use per week: a weekly loot lockout, a weekly currency cap, a quest that unlocks on Tuesday. We model it as `g`, the most hours per week that still move a player toward exhausting the drop. Hours beyond `g` are still played, but they don't bring the end any closer.
- A **drought** is the stretch between a player exhausting a drop and the next drop arriving. Players in a drought log in less, and some leave. MMO308 treats retention with real telemetry. This week treats the drought as a number of days you can see coming.

## 2. Worked example: content locust math

### The hook

World of Warcraft's raid Nerub-ar Palace opened in the Americas on 10 September 2024. It stayed the current raid until the next one, Liberation of Undermine, opened on 4 March 2025. That is a cadence of 175 days, almost exactly six months.

Here is what the fastest players did with those six months, according to Raider.IO's hall of fame for the raid.

- The first guild to kill the final boss, Queen Ansurek, on Normal difficulty did it at 18:51 UTC on opening day. The raid had been open for under four hours.
- The first Heroic kill came about 25 hours after opening.
- Liquid killed her on Mythic, the hardest difficulty, on 29 September, 19 days after the raid opened.

So one guild saw everything the raid offered in under three weeks of a 25-week season. Yet by the end of the season, Raider.IO lists 22,403 guilds with a Normal kill of the final boss, 17,625 with a Heroic kill, and only 2,777 with a Mythic kill. For about seven in eight of the guilds that finished Normal, the Mythic version of the same boss was still unbeaten when the season ended.

Two facts sit side by side. The raid was exhausted in hours by some, and never exhausted by most. Which one is "the" consumption time? Neither. Consumption time is a distribution, and a content plan is only as good as its worst-served percentile.

### The model

Take one content drop and one player.

```
exhaustion time    T = 7 × C × r / min(h, g)     (days)
locust ratio       L = P / T
drought            D = max(0, P − T)              (days)
drought share      D / P
```

- `C` is the drop's content hours for one pass.
- `r` is the replay multiplier, so `C × r` is the total hours the drop can hold this player.
- `h` is the player's hours of play per week.
- `g` is the weekly gate in hours. Without a gate, `min(h, g) = h`.
- The 7 turns weeks into days.
- `P` is the cadence, days until the next drop.

Read `L` as "how many times could this player have consumed the drop while the team built the next one." `L = 1` is the break-even line. At `L = 1` the player finishes exactly as the next drop lands. At `L = 4` they finished in a quarter of the cycle and spent three quarters of it in drought.

Players differ mainly in `h`. So describe the population by percentiles of weekly play time. The **pth percentile** `h_p` is the weekly hours that a share `p` of players play at or below (MA102 week 12). The median player is `p50`. The top one in a thousand is `p99.9`.

### Numbers you can check

Take a drop of `C = 20` content hours and a cadence of `P = 175` days, the length of the Nerub-ar Palace season. Use this invented population of weekly play times:

| Percentile | `h` (hours/week) |
|---|---|
| p50 | 6 |
| p75 | 10 |
| p90 | 16 |
| p99 | 34 |
| p99.9 | 60 |

The numbers are shaped like real play-time data (a long tail of heavy players) but they are chosen for teaching, not measured from any game.

Now three designs for the same 20 hours of content.

| Percentile | A: `r = 1`, no gate: `T` (days) | `L` | B: `r = 6`, no gate: `T` | `L` | C: `r = 6`, `g = 12`: `T` | `L` |
|---|---|---|---|---|---|---|
| p50 | 23.3 | 7.50 | 140.0 | 1.25 | 140.0 | 1.25 |
| p75 | 14.0 | 12.50 | 84.0 | 2.08 | 84.0 | 2.08 |
| p90 | 8.8 | 20.00 | 52.5 | 3.33 | 70.0 | 2.50 |
| p99 | 4.1 | 42.50 | 24.7 | 7.08 | 70.0 | 2.50 |
| p99.9 | 2.3 | 75.00 | 14.0 | 12.50 | 70.0 | 2.50 |

Check one cell by hand. Design A, median player. `T = 7 × 20 × 1 / 6 = 23.3` days, and `L = 175 / 23.3 = 7.5`. The median player finishes a six-month drop in about three weeks and spends the other five months in drought.

Design B keeps the same 20 hours of authored content and makes it worth playing six times, through difficulty tiers and repeatable rewards. Every `T` grows sixfold and every `L` shrinks sixfold. The median player now nearly makes it (`L = 1.25`, drought 35 days). The p99.9 player still burns through it in two weeks.

Design C adds a gate of 12 useful hours per week. Look at what it does and doesn't do. It leaves the p50 and p75 rows alone, because those players play under 12 hours anyway. It changes nothing about how much content exists. It only stops the heaviest players from converting extra hours into progress, so the top three rows collapse onto one value, 70 days. The spread between the median and the top one-in-a-thousand player falls from `75 / 7.5 = 10×` to `2.5 / 1.25 = 2×`.

That is the lesson of this worked example. **Content volume moves every percentile by the same factor. A gate moves only the top.** They solve different problems, and a plan needs to say which problem it is solving.

The same table from code:

```python
def exhaust_days(C, r, h, gate=None):
    """Days until a player who plays h hours a week runs out of new content."""
    rate = h if gate is None else min(h, gate)
    return 7 * C * r / rate

P, C = 175, 20                       # days between drops, content hours per drop
players = {"p50": 6, "p75": 10, "p90": 16, "p99": 34, "p99.9": 60}

for r, gate in ((1, None), (6, None), (6, 12)):
    row = []
    for name, h in players.items():
        T = exhaust_days(C, r, h, gate)
        row.append(f"{name} {T:5.1f}d x{P / T:5.2f}")
    print(f"r={r} gate={gate}:", " | ".join(row))
```

It prints:

```
r=1 gate=None: p50  23.3d x 7.50 | p75  14.0d x12.50 | p90   8.8d x20.00 | p99   4.1d x42.50 | p99.9   2.3d x75.00
r=6 gate=None: p50 140.0d x 1.25 | p75  84.0d x 2.08 | p90  52.5d x 3.33 | p99  24.7d x 7.08 | p99.9  14.0d x12.50
r=6 gate=12: p50 140.0d x 1.25 | p75  84.0d x 2.08 | p90  70.0d x 2.50 | p99  70.0d x 2.50 | p99.9  70.0d x 2.50
```

### A visual you can move

Open the interactive. The left view is a bar for each percentile, with length `T` in days, drawn against a vertical line at the cadence `P`. Any bar that stops short of the line leaves a shaded drought after it. The right view shows the whole population at once, as a curve of the share of players who still have something new to do on each day of the cycle.

Start on design A. The right-hand curve falls off a cliff in the first month. Drag the replay slider to 6. Every bar stretches and the curve slides to the right, keeping its shape. Now drag the gate slider down from "none" to 12. The long bars at the top don't move, while the short ones lengthen until they meet. On the right the curve changes shape. It stays flat at 100% for 70 days and then drops, because everyone above 12 hours a week now runs out on the same day.

That drop is the gate's hidden cost, and section 3 comes back to it.

### Cross-game recognition

Every live MMO pulls the same three levers: cadence `P`, replay `r` and gate `g`. The mix is what differs.

**World of Warcraft (The War Within, 2024-2026).** One raid per season, with four difficulties. Raider.IO's kill counts for Nerub-ar Palace show what difficulty tiers do in model terms. The same eight bosses are authored once and exhausted at very different times by different percentiles, which raises `r` for the players who move up a tier. On top of that, the game gates. Raids and Mythic dungeons have **weekly lockouts** (a character can loot each boss once per week per difficulty), and the Great Vault gives one extra choice of reward per week. Mythic+ dungeons have no lockout at all. They are the high-`r` repeatable that absorbs hours the raid gate refuses.

**Final Fantasy XIV (Endwalker onward, 2021-2026).** Square Enix shortens `P` instead. Since Endwalker, major patches have arrived on a roughly 19-week (4.5-month) cycle, and earlier expansions ran closer to 16 weeks. Current-tier raids limit how much loot a player can take per week, and the strongest tomestone gear is bought with a weekly-capped currency. Both are gates in our sense. When a raid tier ages, the wiki notes, those weekly limits are lifted so that players can catch up. That is a gate being opened on purpose once the top percentile no longer needs holding back.

**Destiny 2 (The Final Shape, June 2024).** Bungie's raid Salvation's Edge launched on 7 June 2024. According to Destinypedia, the first team took 18 hours, 59 minutes and 41 seconds to clear it, the longest first clear of any Destiny 2 raid, and only one team finished in the first 24 hours. An emblem rewarded anyone who cleared it within the first 48 hours. In our terms, Bungie tuned the launch difficulty to stretch `T` for the p99.9 player from hours to days, and turned that race into an event. Most players met the raid later, at a lower difficulty, on a longer clock.

Three games, one equation. WoW gates hard and adds a repeatable. FFXIV runs a shorter cadence. Destiny stretches the top of the distribution with difficulty at launch. Each is a choice about which rows of the table to fix.

### Eyes-open design judgment

- **Pick the percentile you're designing for, and write it down.** "The content lasts until the next patch" is meaningless without a percentile. A drop that holds the median player for the full cycle will leave the p99 player in drought for most of it, unless you gate them. Decide which rows you will accept as `L > 1`.
- **Replay beats volume, up to a point.** Building six times the content costs six times the production. Making the same content worth playing six times costs systems work, tuning and loot design, which is usually far cheaper per hour. The price is that replayed hours are thinner. The sixth run of a dungeon is not the first, and players know it.
- **Gates compress, and compression synchronizes.** A gate makes the top percentiles run out together. That is good for social play (friends stay in step) and bad for a live service, because everyone above the gate hits the drought on the same day. The right-hand view shows the cliff.
- **Gates feel like a tax to the people they bind.** The heaviest players are also the most vocal. They experience a gate as "the game won't let me play." FFXIV's habit of lifting weekly limits as a tier ages is one way to spend that goodwill back.
- **Droughts aren't always failures.** A player who finishes and takes a break before the next drop may return happily. Subscription games and free games price droughts differently (MMO403). Decide whether your model's drought is a churn risk or a planned rest.

### Check yourself (worked example)

1. A drop holds `C = 12` hours with `r = 4`. The cadence is 120 days. How many hours per week can a player play before `L > 1`?
2. In design C above, what gate value would make the p90 player's `T` exactly equal to `P`?

<details>
<summary>Answers</summary>

1. `L = 1` when `T = P`, so `7 × 12 × 4 / h = 120` and `h = 2.8` hours per week. Any player above 2.8 hours a week, which is most players, runs out before the next drop. This drop needs more replay, a shorter cadence, or both.
2. `T = 7 × 20 × 6 / g = 175` gives `g = 4.8` hours per week. A gate that low binds almost everyone, including the median player, which is why real gates sit above the median and accept some drought at the top.

</details>

## 3. Where replay comes from

The replay multiplier `r` is not one feature. It is the product of several decisions, and it helps to split it.

```
r ≈ tiers × runs per tier × characters
```

- **Tiers.** The same encounter at several difficulties. Each tier is a new first clear for players who move up. The Nerub-ar Palace kill counts show how tiers split the population. Everyone who beats Heroic has already beaten Normal, and fewer than one in six guilds with a Heroic kill ever gets the Mythic one.
- **Runs per tier.** How many times a player repeats a cleared tier because it still pays. Random loot is the classic reason. MA102 week 7 showed how long a single drop can take. Here, that long wait is the replay.
- **Characters.** A second character replays everything. Account-wide unlocks reduce this multiplier on purpose, because players asked for it.

Each factor has a cost the table doesn't show. Tiers need tuning at every level, and the week 6 lecture on raid difficulty tiers covers that work. Runs per tier depend on loot, and loot that keeps players returning also makes them feel they are grinding. Characters multiply replay only for players who enjoy alts.

### Tiers target percentiles

Think of each difficulty as a separate drop aimed at a different part of the population. A Normal tier sized for the median player at `L ≈ 1` would be trivial for the p99 player. A Mythic tier sized for the p99 player would never be finished by the median player, and the kill counts suggest that's fine. The median guild's drop is Normal and Heroic. Mythic is the p99 drop that happens to reuse the same art, bosses and story.

That reuse is where tiers earn their keep. The expensive parts of a raid (the environment, the models, the encounter scripting) are built once. The cheap part (numbers and a few extra mechanics) is built per tier.

## 4. The production side: why the ratio isn't about efficiency

It is tempting to measure the locust problem as cost per hour. Suppose a team of 60 builds a drop in six months (invented, but the right order of magnitude for a raid tier plus its surrounding systems). That is roughly `60 × 26 weeks × 40 hours = 62,400` developer hours for 20 content hours, about 3,100 developer hours per hour of play.

That sounds ruinous until you remember that content is shared. If a million players each play those 20 hours six times, the drop delivers `1,000,000 × 20 × 6 = 120,000,000` player hours. That's about 0.0005 developer hours per player hour. By cost per hour of fun, MMO content is cheap.

So the problem is not efficiency. It is **calendar time**. Production runs in series (one team, one drop at a time) while consumption runs in parallel (every player at once). Hiring more people does not halve `P`, because a team twice the size doesn't build a raid in half the time. What you can change quickly is `r` and `g`, which is why live games lean on them so heavily. Week 13 turns this into a cadence plan with a budget. For now, carry one rule. When a drop is consumed too fast, the first question is "what makes the second hour of this content worth playing?", not "how do we build more?"

### Two production strategies

Studios usually combine two ways of attacking `P`.

- **Parallel teams.** Two or three teams work on staggered drops, so each drop gets a full year of development while players see a new one every six months. This shortens `P` without shortening any one team's schedule. It costs coordination, since drops must fit together.
- **Cheaper content types.** Some content is cheaper per hour than a raid. Repeatable dungeons with rotating modifiers, systemic events and procedurally varied content (weeks 8 and 9) all have high `r` for their production cost. They pay for their cheapness in freshness. Players can tell a remix from a new place.

## In-class activity (25 minutes)

Work in groups of three. You are planning a drop for a fictional MMO with a cadence of 140 days and the population table from section 2.

1. **(5 min)** Your lead says the drop has 30 content hours and no replay. Compute `T` and `L` for all five percentiles.
2. **(10 min)** You may spend a budget of "10 points". Each point buys either 3 more content hours, or +1 to `r`, or lowers the gate by 5 hours per week from an initial "no gate" (the first point sets `g = 40`). Choose a spend that gets the p50 and p75 players to `L ≤ 1` and keeps the p99.9 player at `L ≤ 3`. Record `T` and `L` for every row.
3. **(5 min)** Check your plan in the interactive. Read the share of players with something to do on day 70 and day 120.
4. **(5 min)** Swap plans with another group. Name the percentile their plan serves worst and say which single change you would make.

Expected output: a spend list, a filled table, two shares read from the interactive, and one critique.

## Common misconceptions

- **"Locusts are a player problem."** They are a scheduling fact. Any player with enough hours reaches `L > 1`. The heavy players simply reach it first, and a design that works for the median fails for them by construction.
- **"More content fixes the treadmill."** More content multiplies every `T` by the same factor, so it helps everyone equally in ratio terms. It cannot close the tenfold gap between p50 and p99.9, and it is the most expensive lever you have.
- **"A weekly lockout reduces how much content the game has."** A gate changes how fast players can use content, not how much exists. It affects only the players above it.
- **"The fastest clear tells you how long the content lasts."** A 19-day world first and a season where most guilds never beat Mythic describe the same raid. Always ask "for which percentile?"

## Check yourself

1. A drop holds 15 content hours with `r = 5`. The cadence is 150 days. Compute `T` and `L` for a player who plays 8 hours a week and for one who plays 40.
2. The same drop adds a gate of 10 hours per week. Recompute both rows. By what factor did the gap between the two players shrink?
3. A designer proposes doubling `C` instead of adding the gate. Compute the new `L` for both players and say which proposal serves the 40-hour player better, and which serves the 8-hour player better.
4. In the Nerub-ar Palace figures, 2,777 guilds killed the final boss on Mythic and 17,625 on Heroic. What share of Heroic-clearing guilds ever finished Mythic? What does that say about the Mythic tier's `L` for a typical Heroic guild?

<details>
<summary>Answers</summary>

1. 8 h: `T = 7 × 15 × 5 / 8 = 65.6` days, `L = 150 / 65.6 ≈ 2.29`. 40 h: `T = 525 / 40 = 13.1` days, `L ≈ 11.4`.
2. 8 h is under the gate, so it is unchanged (`L ≈ 2.29`). 40 h becomes `min(40, 10) = 10`, so `T = 52.5` days and `L ≈ 2.86`. The gap between the two `L` values shrank from `11.4 / 2.29 = 5×` to `2.86 / 2.29 = 1.25×`, a factor of 4.
3. Doubling `C` doubles every `T` and halves every `L`. 8 h: `L ≈ 1.14`. 40 h: `L ≈ 5.71`. The 8-hour player gains more from doubling (1.14 against 2.29 with the gate). The 40-hour player gains more from the gate (2.86 against 5.71). This is the section 2 lesson in numbers.
4. `2,777 / 17,625 ≈ 16%`. For the other 84% the Mythic tier was never exhausted, so for them `T > P` on that tier, and `L < 1`. The tier gave them something to work on all season, even if they never finished it.

</details>

## Lab / assignment hook

[Lab 01, locust math on a player population](../labs/lab01.md). You implement `T`, `L` and the share of players with something to do, run them on a sample of 2,000 players' weekly hours, and search for the cheapest plan that meets a target for the median and the p99 player. You will reuse the functions in week 13's cadence plan and in the final dungeon's content budget.

## Sources

- Raider.IO, hall of fame and raid static data for Nerub-ar Palace (World of Warcraft: The War Within, season 1), retrieved from the public Raider.IO API in September 2026. Raid opened 10 September 2024 (Americas, 15:00 UTC) and was current until 4 March 2025. First Normal kill of Queen Ansurek 10 September 2024 18:51 UTC; first Heroic kill 11 September 2024 15:46 UTC; first Mythic kill by Liquid 29 September 2024 07:02 UTC. End-of-season counts of guilds with a final-boss kill: Normal 22,403, Heroic 17,625, Mythic 2,777. https://raider.io/nerubar-palace
- Warcraft Wiki, "Patch 11.1.0" and "Liberation of Undermine" (The War Within). Patch released 25 February 2025; the raid opened 4 March 2025. https://warcraft.wiki.gg/wiki/Liberation_of_Undermine
- Warcraft Wiki, "Lockout" (as of the Midnight era, 2026). Raids, world bosses and Mythic dungeons have weekly lockouts; Mythic+ keystones have none; loot-based lockouts allow one loot per boss per difficulty per week. https://warcraft.wiki.gg/wiki/Lockout
- Warcraft Wiki, "Great Vault" (Shadowlands onward). Weekly reward choice for raid, dungeon and world activities. https://warcraft.wiki.gg/wiki/Great_Vault
- Final Fantasy XIV Online Wiki (consolegameswiki), "Patches" (as of 2026). Major patches on a 4.5-month (19-week) interval since Endwalker; earlier gaps of about 112 days. https://ffxiv.consolegameswiki.com/wiki/Patches
- Final Fantasy XIV Online Wiki, "Raids" (Dawntrail era, 2026). Current-tier raids limit loot per week and the limits are removed as raids age to help catch-up; weekly-capped tomestone gear. https://ffxiv.consolegameswiki.com/wiki/Raids
- Destinypedia, "Salvation's Edge" (Destiny 2: The Final Shape). Released 7 June 2024; first clear 18 h 59 min 41 s, longest of any Destiny 2 raid; one clear in the first 24 hours; emblem for completion within 48 hours. https://www.destinypedia.com/Salvation%27s_Edge
- The population table, content hours, team size and replay values are invented for teaching.

## Interactive spec: examples/w01-content-locust.html

**The one insight.** Adding content or replay stretches every player's exhaustion time by the same factor, but a weekly gate only shortens the fast end. The student must see bars stretch in proportion when `r` moves, and the long-tail bars merge when `g` moves.

**Layout.** Two linked views, side by side on wide screens, stacked on phones (bars first).

- **Left view, "Days until they run out".** Horizontal bars, one per percentile row (p50, p75, p90, p99, p99.9), length `T` in days. A vertical line at `P`, labeled "next drop". The part of the cycle after a bar ends and before `P` is shaded and labeled "drought, N days". Bars longer than `P` are clipped at the axis end with an arrow and the label "outlasts the cycle". Each bar shows `T` and `L = P / T` at its end, to one decimal for `T` and two for `L`.
- **Right view, "Share of players with something new".** Line chart, x axis day 0 to `P` (plus 10%), y axis 0 to 100%. The curve is `S(t)` below. Mark the day each table percentile runs out with a small tick on the curve. A dashed horizontal guide at 50%.
- **Readout under both views.** A copyable table with the five rows: `h`, `T`, `L`, drought days, drought share.

**Controls.**
- Content hours `C`: slider 2 to 80, step 1, default 20.
- Replay `r`: slider 1 to 12, step 0.5, default 1.
- Gate `g`: slider "none", then 40 down to 2 hours per week in steps of 1. Default "none".
- Cadence `P`: slider 30 to 365 days, step 5, default 175.
- Preset buttons: "A: raw content" (`C = 20, r = 1`, no gate), "B: replay" (`r = 6`), "C: replay + gate" (`r = 6, g = 12`).
- Population toggle: "table" (the five fixed rows: 6, 10, 16, 34, 60 hours) or "curve only".

**Formulas.**
- `T = 7 × C × r / min(h, g)`, with `min(h, g) = h` when there is no gate.
- `L = P / T`, drought `D = max(0, P − T)`, drought share `D / P`.
- Population curve. Weekly hours are lognormal with median 6 and `σ = 0.75` (so p75 ≈ 10.0, p90 ≈ 15.7, p99 ≈ 34.3, p99.9 ≈ 60.9). A player still has content on day `t` when `T > t`. Let `limit = 7 × C × r / t`. If a gate is set and `g ≤ limit`, then `S(t) = 1` (gated players have `T = 7Cr/g`, so at `t = 7Cr/g` exactly they count as still having content, matching the `t ≤ 70` test below). Otherwise `S(t) = Φ((ln(limit) − ln 6) / 0.75)`, where Φ is the standard normal CDF. `S(0) = 1`.

**Test values** (`C = 20`, `P = 175`).
- Preset A: `T` = 23.3, 14.0, 8.8, 4.1, 2.3 days; `L` = 7.50, 12.50, 20.00, 42.50, 75.00. Curve: `S(30) ≈ 37%`, `S(90) ≈ 4%`.
- Preset B: `T` = 140.0, 84.0, 52.5, 24.7, 14.0; `L` = 1.25, 2.08, 3.33, 7.08, 12.50. `S(30) ≈ 98%`, `S(90) ≈ 72%`.
- Preset C: `T` = 140.0, 84.0, 70.0, 70.0, 70.0; `L` = 1.25, 2.08, 2.50, 2.50, 2.50. `S(t) = 100%` for `t ≤ 70`, `S(90) ≈ 72%`.
- Check-yourself Q1 of section 2: `C = 12, r = 4, P = 120` gives `L = 1` at `h = 2.8`.

**First screen.** Preset A, so the student sees five short bars far from the "next drop" line and a curve that collapses within a month. The replay and gate sliders sit directly under the bars.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. Bars carry text labels, not colour alone. Drought shading has a hatch pattern. All sliders keyboard operable with visible values. Curve animation off under `prefers-reduced-motion`.

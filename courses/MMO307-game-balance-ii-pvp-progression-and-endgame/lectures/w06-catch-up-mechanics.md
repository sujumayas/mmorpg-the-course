# MMO307 · Week 06 — Catch-Up Mechanics

**Why this matters:** Every week of a season, some players arrive late: returning subscribers, new players, alts, people back from exams. A vertical game leaves them behind by default. The rule you choose for them decides whether they can play with their friends by week 10, and also whether your most committed players still see a reason to log in during week 1.

**You will be able to:**
- Compute the week a late player catches up under a rolling cap, and show that a plain weekly cap never lets them catch up.
- Derive the free lateness window, the number of weeks a fast player can skip at no cost, and explain what it does to early-season engagement.
- Model mid-season levers (raising the cap, removing it, converting old currency, account-wide discounts) as changes to one allowance function, and compute their effect on the gap.
- Critique a shipped catch-up system by rewriting its rules in this model and naming who it helps and who it costs.

**Before class:** Warcraft Wiki, "Conquest" and "Valor" (the Shadowlands sections, 10 minutes). Final Fantasy XIV Online Wiki, "Allagan Tomestone" (the two caps, 5 minutes).

**Prerequisites from earlier courses:** [GD203 week 14, horizontal vs vertical progression](../../GD203-combat-and-progression-design/lectures/w14-horizontal-vs-vertical-progression.md) (the power gap `G`, the sharing band `F`, and catch-up as one of three tools against a growing gap). [MA101 week 7, piecewise functions, caps and floors](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w07-piecewise-caps-and-floors.md) (`min` and `max` as caps). This course's [week 1](w01-the-endgame-problem.md) (weekly caps turn runs into calendar weeks) and [week 4](w04-gear-treadmills-and-item-level.md) (the patch-day gap between veterans and newcomers).

**Interactive:** [`examples/w06-rolling-cap.html`](../examples/w06-rolling-cap.html). Keep it open during section 2.

---

## 1. The late player's problem

GD203 week 14 named the problem. In a vertical game the power gap between a veteran and a newcomer grows with every tier, and three tools stop it: a cap on growth, a reset, and a **catch-up mechanic**, which raises the newcomer directly. Week 4 of this course measured the reset side, the gap left on patch day when old gear lands a third of the way up the new ladder.

This week is about the third tool, inside a single season. The season has already started. A player joins in week 7. What rule lets them close the distance, and how fast?

Most endgame progress in modern MMOs is paced by a **capped currency**. The player earns points (Valor, Conquest, crests, tomestones) by playing, spends them on gear or upgrades, and cannot earn more than a set amount per week. Week 1 showed why designers use caps: a cap turns "how many hours can you play" into "how many weeks have you played", which compresses the spread between light and heavy players.

That compression is exactly the late player's problem. If progress is paced by weeks, the player who missed six weeks is six weeks behind, and no amount of play fixes it. Every catch-up mechanic in this lecture is a way to loosen that one sentence.

## 2. Worked example: the rolling cap

### The hook

In World of Warcraft's Shadowlands, the PvP currency Conquest had a weekly cap of 550. Warcraft Wiki adds the detail that made it unusual. The cap increased every week by another 550, "allowing players to earn any missed Conquest at any point". Valor, the dungeon upgrade currency added in patch 9.0.5 (9 March 2021), used the same rule with 750 per week.

A player who skipped the first six weeks of a season could come back and earn six weeks of Valor in their first week back, if they played enough. Then, in April 2022, Blizzard doubled Conquest's weekly increase to 1,100, and in May 2022 it removed both caps entirely.

Three changes to one number in a single season. Each one moved a different group of players. Here is a model that shows which.

### The model

A **capped currency** has an allowance, the most a player can have earned by the end of week `w`. Two shapes are common.

```
weekly cap:   each week, earn at most L
rolling cap:  by the end of week w, have earned at most L × w in total
```

With a weekly cap, a week you miss is gone. With a rolling cap, the allowance you did not use carries forward.

Now model two players.

- A **veteran** plays from week 1 and always reaches the allowance. By the end of week `w` they have `L × w`.
- A **late player** misses the first `j` weeks, then plays at a **speed** `v`, the amount they would earn per week with no cap at all. The speed depends on how many hours they put in.

Under a **weekly cap**, the late player earns `min(v, L)` per week. Even if they play twice as much as the veteran, they earn `L`. Their total is `L × (w − j)`, so the gap is

```
veteran − late player = L × j        (constant, forever)
```

Under a **rolling cap**, the late player earns `v` per week until they hit the allowance. Their total is `min(v × (w − j), L × w)`. They reach the allowance, and so catch the veteran, when `v × (w − j) = L × w`:

```
catch-up week  w* = v × j / (v − L)      (needs v > L)
```

Finally, the season has a finish line. Say a full set of upgrades costs `N`. The veteran finishes in week `N / L`. The late player finishes in week `max(j + N / v, N / L)`: either when their own speed gets them there, or when the allowance lets them, whichever is later.

Symbols, once more: `L` weekly allowance, `j` weeks missed, `v` late player's speed per week, `w` week number, `w*` catch-up week, `N` currency needed to finish.

### Numbers you can check

Use Shadowlands Valor's `L = 750`. Invent a finish line of `N = 9,000`, so a veteran finishes in week 12. A late player misses 6 weeks and then plays at `v = 1,500`, twice the allowance.

| End of week w | Veteran | Late player, rolling cap | Late player, weekly cap | Gap, rolling | Gap, weekly |
|---|---|---|---|---|---|
| 6 | 4,500 | 0 | 0 | 4,500 | 4,500 |
| 7 | 5,250 | 1,500 | 750 | 3,750 | 4,500 |
| 8 | 6,000 | 3,000 | 1,500 | 3,000 | 4,500 |
| 10 | 7,500 | 6,000 | 3,000 | 1,500 | 4,500 |
| 12 | 9,000 (done) | 9,000 (done) | 4,500 | 0 | 4,500 |
| 14 | 9,000 | 9,000 | 6,000 | 0 | 3,000 |
| 18 | 9,000 | 9,000 | 9,000 (done) | 0 | 0 |

Under the weekly cap, the gap sits at `750 × 6 = 4,500` until the veteran stops earning at the finish line, and the late player finishes six weeks after the veteran, in week 18. Under the rolling cap, the gap shrinks by `v − L = 750` every week and hits zero at `w* = 1,500 × 6 / 750 = 12`. The late player finishes on the same day as the veteran, having played only six weeks.

Now vary the late player's speed, keeping `j = 6`.

| Speed v | Catch-up week w* = 6v / (v − 750) | Late player finishes (week) |
|---|---|---|
| 1,000 | 24 | 15 |
| 1,125 | 18 | 14 |
| 1,500 | 12 | 12 |
| 2,250 | 9 | 12 |
| 3,000 | 8 | 12 |

At `v = 1,000` the formula says week 24, but the late player finishes in week 15 anyway. The catch-up week is where their total meets the allowance, and for slow players the finish line comes first. The column that matters for play is the last one. Everyone at `v ≥ 1,500` finishes in week 12, on the veteran's day, because the allowance, not speed, is what stops them.

You can reproduce both tables with a short script.

```python
N, L, j = 9_000, 750, 6

def rolling(w, v):
    return min(N, max(0, min(v * (w - j), L * w)))

def weekly(w, v):
    return min(N, max(0, min(v, L) * (w - j)))

for w in (7, 10, 12, 18):
    print(w, min(N, L * w), rolling(w, 1_500), weekly(w, 1_500))
for v in (1_000, 1_500, 3_000):
    print(v, v * j / (v - L), max(j + N / v, N / L))
```

It prints:

```
7 5250 1500 750
10 7500 6000 3000
12 9000 9000 4500
18 9000 9000 9000
1000 24.0 15.0
1500 12.0 12.0
3000 8.0 12.0
```

### A visual you can move

Open the interactive. The left panel plots cumulative currency against weeks: the veteran's staircase at `L` per week, the late player's line starting at week `j`, and the allowance `L × w` as a dashed line. Under the rolling rule the late player's line is steep and meets the dashed line. Under the weekly rule it runs parallel to the veteran's, six weeks behind. On this panel the two rules look like a steeper or shallower line, a matter of degree.

The right panel plots the gap, veteran minus late player, for both rules at once. Now the difference is qualitative. The weekly-cap gap is a flat shelf at `L × j` that only drains after the veteran finishes. The rolling-cap gap is a ramp that hits zero at `w*`. Drag `v` down toward `L` and watch the ramp flatten until, at `v = L`, it becomes the shelf. Drag `j` to 10 and watch `w*` move to 20 at `v = 1,500`. Turn on "cap removed at week U" and a third line appears that behaves like the rolling line from week `U` on.

### Cross-game recognition

**World of Warcraft, Dragonflight Season 1 (2022 to 2023).** Warcraft Wiki records that Valor in that season started with a cap of 1,500 and increased by 750 per week. That is a rolling cap with a head start, allowance `750 + 750 × w`. In our model the head start does not change `w*`'s formula for the gap. It gives everyone, veteran and late player alike, one free week of allowance on day one, which matters mostly for players who arrive in week 1 with a lot of time.

**Final Fantasy XIV (A Realm Reborn to Dawntrail).** The Allagan tomestone that buys the newest gear is capped at 450 per week, and the cap does not roll. A missed week is gone, so a late player sits a fixed `450 × j` behind. The game's catch-up comes later and all at once. The wiki records that when a new tomestone is introduced, the previously capped one becomes uncapped. It also records that the weekly limit is typically raised to 900 towards the end of an expansion's final patch cycle. In our model, FFXIV runs a weekly cap with a shelf-shaped gap, then removes the cap on the old currency at the next rotation (`U` = the next even patch) and doubles `L` at the very end of an expansion.

**World of Warcraft, Midnight Season 1 (2026).** The upgrade crests had a cap of 100 per type per week. The wiki records that Blizzard removed the cap for every crest type by hotfix on 19 May 2026, nine weeks into a 21-week season. After that week, every player earned at their own speed `v`. A cap removal is the extreme of a rolling cap: the allowance jumps to infinity at week `U`.

Three games, the same allowance function in different shapes. For any capped currency, ask four questions. What is `L`? Does unused allowance roll forward? Does `L` change during the season? And when, if ever, does the cap come off?

### Eyes-open design judgment

- **A weekly cap is fair week by week and harsh to late players.** It gives light and heavy players the same pace, which is its purpose. It also freezes the late player's gap at `L × j` until the veterans stop earning. Use it when you want the calendar to be the only thing that matters, and pair it with a later catch-up event.
- **A rolling cap makes progress depend on total time, not on which weeks you played.** Late players catch up if they can play faster than `L`. Players who cannot (`v ≤ L`) get nothing from it, and they are often the same players who arrived late because they have little time.
- **Raising `L` mid-season helps everyone who was capped.** Shadowlands' Conquest change in April 2022, from 550 to 1,100 per week, helped late players and heavy veterans alike. It does not close a gap between those two groups. It moves the finish line closer for both.
- **Removing the cap ends the pacing.** After week `U` the gap between players is set by speed, `(v_1 − v_2)` per week, so heavy players pull ahead of light ones as fast as they like. That is the reverse of what the cap was for. It is a good trade late in a season, when the heavy players are already done.

Pick the shape for the player you most want to protect, and say in the design document who pays for it.

## 3. The free lateness window

The rolling cap has a side effect that designers often miss. Go back to the finish-line formula. The late player finishes in week `max(j + N / v, N / L)`. As long as `j + N / v ≤ N / L`, joining late costs them nothing at all. Solve for `j`:

```
free lateness window   J_free = N / L − N / v = N × (v − L) / (v × L)
```

With `N = 9,000` and `L = 750`:

| Speed v | J_free (weeks) |
|---|---|
| 750 | 0 |
| 1,000 | 3 |
| 1,500 | 6 |
| 2,250 | 8 |
| 3,000 | 9 |

A player who can play twice the allowance's worth each week can skip the first six weeks of a twelve-week chase and finish on the same day as someone who logged in every week. A player at four times the allowance can skip nine.

That is catch-up working as designed, and it has a cost. The players with the highest `v` are your most committed players. A rolling cap tells them, correctly, that the early weeks don't matter. If your season's first weeks are also when raids open, when guilds form and when the community is busiest, the rolling cap is quietly asking your most active players to be absent for them.

Two fixes are common.

- **Keep a weekly-only source alongside the rolling one.** A weekly reward whose missed weeks cannot be made up keeps early weeks worth something, while the rolling currency handles catch-up.
- **Shorten the window.** Since `J_free = N (v − L) / (v L)`, a larger `L` or a smaller `N` shrinks it. So does a head start on the allowance (Dragonflight's 1,500), which moves `N / L` earlier for everyone.

## 4. Mid-season levers as changes to the allowance

Every mid-season catch-up change is a change to the allowance function `A(w)`. Writing each one down in that form lets you compare them.

| Lever | Allowance after the change at week U | Who it helps | Shipped example |
|---|---|---|---|
| Raise `L` | `L × U + L' × (w − U)` with `L' > L` | Anyone whose speed exceeds `L` | Shadowlands Conquest, 550 to 1,100 per week (hotfix 12 April 2022) |
| Remove the cap | unlimited from `U` | Anyone with time; heavy players most | Shadowlands Conquest and Valor (9 May 2022); Midnight crests (19 May 2026) |
| Uncap the old currency when a new one arrives | old currency unlimited from the next rotation | Players still collecting the previous tier | Final Fantasy XIV tomestones |
| Account-wide discount | cost `N × (1 − δ)` for alts once any character has reached a level | Players with several characters | Dragonflight Flightstones, 50% off to a slot's highest level on any character |

The last row is catch-up for alternate characters. Warcraft Wiki records that from Dragonflight Season 2 on, once one character on an account had upgraded an item to a given level in a slot, other characters paid half the Flightstones up to that level. In The War Within the same discount applied to Valorstones account-wide, while the crest discount stayed per character. In our model it scales `N` down for the second character, which shrinks its finish time and its free lateness window together.

### Raising L, worked

Suppose that at week `U = 10` of our example the allowance increase doubles to `L' = 1,500`. The veteran who always reached the old allowance (speed exactly 750) gains nothing, because their own speed now binds. A late player with `j = 8` and `v = 1,500` would, under the old rule, catch up at `w* = 1,500 × 8 / 750 = 16`. But they finish before week 16, at `j + N / v = 8 + 6 = 14`, so the allowance never binds for them. Their own speed is the limit under the old rule and the new one, and they finish in week 14 either way. Raising `L` helped nobody in this pair.

Now take a heavy veteran with `v = 1,500` who has been capped at 750 all season. After week 10 their allowance grows by 1,500 a week, and so do they. They had `7,500` at the end of week 10 and finish during week 11 instead of week 12. Raising `L` is a gift to capped players, and late players are only one kind of capped player.

The lesson generalises. Before shipping a catch-up change, list which players were limited by the cap and which by their own speed. A cap change helps only the first group.

## 5. What catch-up does to the gap in power

Currency is not power. Week 4 converted item levels into power with `(1 + g)` per level. Crest-style currencies make the conversion concrete. In Midnight Season 1, Warcraft Wiki lists 20 crests per upgrade rank and ranks 3 or 4 item levels apart, about 3.4 on average. So a currency gap `Δ` crests is a gap of about `Δ / 20 × 3.4` item levels in the slot being upgraded, and at week 4's `g = 1%` per item level, a power ratio of `1.01^(Δ × 3.4 / 20)` in that slot.

Suppose a character has 16 slots and each needs five ranks. The full set is then `16 × 5 × 20 = 1,600` crests. At 100 crests per week, the veteran completes a track in 16 weeks. A player who missed 6 weeks under a pure weekly cap is 600 crests behind. That is 30 ranks, about 1.9 per slot, or about `1.01^(1.9 × 3.4) ≈ 1.07` in power.

That is small. It is well inside any sharing band `F` from GD203 week 14. So why catch up at all? Because players compare item levels on the character sheet and in group-finder requirements, not power ratios, and because the gap compounds with week 4's patch-day gap and with every tier the player missed before this one. A 7% gap does not stop anyone from playing. A gate on average item level can, and so can the feeling of starting a season 30 ranks behind.

Catch-up therefore has two jobs. One is closing a power gap that would stop players from sharing content. The other is closing a visible gap that would stop them from trying. The second job is often the bigger one, and it is the one a rolling cap does well.

## In-class activity (25 minutes)

In groups of three, design the catch-up rules for a 16-week season whose upgrades cost `N = 4,800` of a currency.

1. Choose `L` so that a player who plays every week finishes in week 12. Compute it.
2. Decide weekly or rolling. For a player who misses 5 weeks and plays at `v = 1.5 L`, compute when they finish under each rule.
3. Compute the free lateness window for `v = 1.5 L` and `v = 3 L` under your rule. Is it acceptable for your season's first weeks? If not, add one lever from section 4 and recompute.
4. Swap with another group. Name the player their rules serve worst and propose one change.

Expected output: `L`, the rule, a finish-week table for three kinds of player, the free lateness window, and a one-paragraph critique.

## Common misconceptions

- **"A weekly cap lets late players catch up if they play more."** It doesn't. They earn `min(v, L)` per week, so extra hours are wasted and the gap stays at `L × j` until the veterans stop.
- **"A rolling cap helps everyone who is behind."** Only players faster than `L`. A late player with little time (`v ≤ L`) gets nothing from it.
- **"Raising the cap is catch-up."** It helps every capped player, veterans included. It does not close the gap between a capped veteran and a capped late player.
- **"Catch-up only affects late players."** The free lateness window changes when committed players choose to play. A generous rolling cap makes early weeks optional for them.

## Check yourself

1. A rolling cap grows by 600 per week. A player misses 4 weeks and then plays at 1,000 per week. In which week do they catch the allowance?
2. The same season has `N = 7,200`. When does the veteran finish, and when does the late player from question 1 finish?
3. With `N = 7,200` and `L = 600`, what is the free lateness window for a player at `v = 1,800`?
4. A game uses a weekly (non-rolling) cap of 450, like FFXIV's tomestones. A player misses 5 weeks. How far behind are they after 10 more weeks, and what single change would let them close the gap?
5. At week 8 of the section 2 example (`L = 750`, `N = 9,000`), the designers remove the cap. A heavy veteran plays at `v = 3,000` and had earned 6,000 by the end of week 8. A light veteran plays at exactly 750. When does each finish?

<details>
<summary>Answers</summary>

1. `w* = 1,000 × 4 / (1,000 − 600) = 10`. At the end of week 10 they have `1,000 × 6 = 6,000 = 600 × 10`.
2. The veteran finishes in week `7,200 / 600 = 12`. The late player finishes in week `max(4 + 7,200 / 1,000, 12) = max(11.2, 12) = 12`, on the same day as the veteran.
3. `J_free = 7,200 / 600 − 7,200 / 1,800 = 12 − 4 = 8` weeks.
4. `450 × 5 = 2,250` behind, and still 2,250 behind after 10 more weeks. Changing to a rolling cap (or removing the cap) lets a player faster than 450 per week close it.
5. The heavy veteran needs 3,000 more at 3,000 per week, so they finish at the end of week 9. The light veteran is unaffected by the removal and finishes in week 12, as before.

</details>

## Lab / assignment hook

[Lab 06, catch-up simulator](../labs/lab06.md). You implement weekly, rolling, raised and removed caps as allowance functions, simulate a population of players who join at different weeks with different speeds, and tune a season's rules so that 90% of players who join by week 8 finish before the season ends while the free lateness window for heavy players stays under a limit you set. The results feed the progression analysis assignment (30%).

## Sources

- Warcraft Wiki, "Conquest" (Shadowlands section, accessed September 2026). Cap of 550 per week, increasing by 550 each week so missed Conquest can be earned later; hotfix of 12 April 2022 raising the weekly increase to 1,100; caps removed by hotfix on 9 May 2022. https://warcraft.wiki.gg/wiki/Conquest
- Warcraft Wiki, "Valor" (accessed September 2026). Re-added in patch 9.0.5 with a rolling seasonal cap increasing by 750 per week; Dragonflight Season 1 cap starting at 1,500 and increasing by 750 per week; caps removed 9 May 2022. https://warcraft.wiki.gg/wiki/Valor
- Warcraft Wiki, "Patch 9.0.5" (released 9 March 2021). Valor earnable in Mythic Keystone dungeons. https://warcraft.wiki.gg/wiki/Patch_9.0.5
- Warcraft Wiki, "Midnight Season 1" and "Hero Dawncrest" (accessed September 2026). Season from 17 March to 11 August 2026; 20 crests per upgrade; cap of 100 crests per type per week; seasonal cap removed by hotfix on 19 May 2026. https://warcraft.wiki.gg/wiki/Midnight_Season_1
- Warcraft Wiki, "Item upgrade" and "Valorstones" (accessed September 2026). Dragonflight Season 2 onward: 50% Flightstone discount for other characters on the account up to a slot's reached item level; The War Within: Valorstone discount account-wide, crest discount per character. https://warcraft.wiki.gg/wiki/Item_upgrade
- Final Fantasy XIV Online Wiki (consolegameswiki), "Allagan Tomestone" (accessed September 2026). Weekly limit of 450 for the newest tomestone, typically raised to 900 towards the end of an expansion's final patch cycle; the previous capped tomestone becomes uncapped when a new one is introduced. https://ffxiv.consolegameswiki.com/wiki/Allagan_Tomestone
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press.

## Interactive spec: examples/w06-rolling-cap.html

**Insight the visual must make obvious:** under a weekly cap the late player's gap is a flat shelf that no amount of play can shrink; under a rolling cap the same gap is a ramp that reaches zero at `w* = v j / (v − L)`, and only if the player is faster than `L`.

**Layout.** Two linked panels, side by side on desktop, stacked on mobile (left first).

- **Left panel, "Currency earned".** x-axis weeks 0 to 24, y-axis currency 0 to `N`. Lines: veteran `min(N, L w)`; late player under the selected rule; the allowance `L w` dashed (rolling) or the weekly steps (weekly). A horizontal line at `N` labelled "finish". Mark each player's finish week with a dot and its value.
- **Right panel, "Gap: veteran minus late player".** Three lines on one chart, always all drawn: weekly cap (`min(N, L w) − min(N, max(0, min(v, L)(w − j)))`), rolling cap (`min(N, L w) − min(N, max(0, min(v (w − j), L w)))`), and, when the toggle is on, cap removed at `U` (late player earns `min(v, L)` per week of play before week `U` under the selected base rule and `v` per week from week `U + 1`, all capped at `N`). Mark `w*` on the rolling line with its value, or print "never (v ≤ L)".

**Controls (keyboard accessible, values shown).**
- `L`: slider 100 to 2,000, step 50, default 750.
- `j` weeks missed: slider 0 to 16, step 1, default 6.
- `v` late player's speed: slider 0 to 4,000, step 50, default 1,500.
- `N`: number input, default 9,000.
- Rule for the left panel: weekly or rolling (default rolling).
- Toggle "cap removed at week U" with slider `U` 1 to 20, default 9.
- Readouts: `w*`, late player's finish week, veteran's finish week `N / L`, free lateness window `J_free = N/L − N/v` (0 when `v ≤ L`).

**Exact test values.**
- Defaults (`L = 750, j = 6, v = 1,500, N = 9,000`, rolling): `w* = 12`, both finish in week 12, `J_free = 6`. Right panel at `w = 10`: rolling gap 1,500, weekly gap 4,500.
- `v = 1,000`: `w* = 24`, late player finishes week 15, `J_free = 3`.
- `v = 750`: `w*` "never", rolling and weekly lines coincide, `J_free = 0`.
- `j = 10, v = 1,500`: `w* = 20`, late player finishes week 16.
- Weekly rule, defaults: late player finishes week 18; gap 4,500 from week 6 to week 12, then 3,000 at week 14 and 0 at week 18.
- Cap removed at `U = 8`, weekly base rule, defaults: the late player has 1,500 at the end of week 8 (two weeks at 750), then earns 1,500 per week, so 3,000 at week 9 and the finish (`1,500 + 1,500 (w − 8) ≥ 9,000`) in week 13.

**First screen:** defaults, rolling rule, with both gap lines visible on the right so the shelf and the ramp are side by side. Caption: "Missing six weeks costs 4,500 forever under a weekly cap, and nothing by week 12 under a rolling one."

# MMO301 · Week 04 — EverQuest: the Treadmill and the Raid

**Why this matters:** EverQuest made the raid the goal of a whole game and made its players wait in line for it. Two of its choices, a fixed number of bosses in a shared world and a level curve that grows much faster than your power, still shape how MMO endgames are built and how players judge them. If you design an endgame, you are choosing between the problems EverQuest had and the problems its fixes created.

**You will be able to:**
- Compute the loot rate per raider for a contested world boss and for an instanced one, given spawn timer, lockout, guild count, raid size and drops per kill.
- Explain with numbers why contested content gets worse for each player as a server gets more popular, and why instancing removes that link.
- Define a progression treadmill and identify its parts in EverQuest's level curve and raid loop.
- Critique an endgame design by naming which of its rewards are rival (one player's gain is another's loss) and which are not.

**Before class:** Bartle, *Designing Virtual Worlds* (2003), chapter 5, "Advancement" and "Levels" (pp. 466-474). Castronova, *Synthetic Worlds* (2005), chapter 4, on the rules and scarcity of synthetic worlds. Skim the Project 1999 Wiki page "Experience" (about 15 minutes).

**Prerequisites from earlier courses:** [GS101 week 9, graphical MMOs](../../GS101-history-and-critical-study-of-games/lectures/w09-graphical-mmos-meridian-59-ultima-online-everquest.md) covers EverQuest's launch, subscriber history and the flat monthly fee. This lecture does not repeat that history. [GD203 week 7, XP curves](../../GD203-combat-and-progression-design/lectures/w07-xp-curves.md) covers curve families and where the XP lives. [MA101 week 4, exponentials and the XP curve](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md) covers growth rates. [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md) is used for loot rates. This course: [week 3 on Ultima Online](w03-ultima-online-the-simulation-dream-and-its-limits.md) set up the shared-world problem this week continues.

**Interactive:** [w04-contested-spawn.html](../examples/w04-contested-spawn.html). Keep it open during section 2.

---

## 1. What EverQuest bet on

GS101 told the business story. EverQuest launched on 16 March 1999, passed Ultima Online in subscriptions within the year and peaked at about 550,000 subscribers at the end of 2004. This week is about the design bet underneath those numbers.

Ultima Online, which you studied last week, tried to be a world that ran by its own rules and let players do almost anything in it. EverQuest took a narrower path. Its center of play was killing monsters in groups to gain levels and items. Player-versus-player combat was limited to dedicated servers, arenas and agreed duels. The hardest monsters were beyond any single group. You needed many groups together, organized by a guild. In 2011 the Game Developers Choice Online Awards gave EverQuest a Hall of Fame award, citing it as the first MMORPG to feature a guild system and raiding.

Two structures come out of that bet, and they are this week's subject.

- **The treadmill.** A progression loop where the reward for effort is the ability to take on more effort of the same kind, and where the finish line keeps moving. Levels, then items, then harder raids that need those items.
- **The raid.** A fight that needs a large, coordinated group, gives rare items, and happens on a schedule set by the world rather than by the players.

Neither is bad in itself. Both have a precise mathematical shape, and the shape tells you what they will do to a population of players.

### A few terms

A **spawn** is the moment a monster appears in the world. A **respawn timer** is the time between the monster's death and its next appearance. A **named** monster is a unique one with its own loot table. In a **shared** (or **open-world**) encounter, every player on the server sees the same monster, so only one group can kill each spawn. In an **instanced** encounter, the game makes a private copy of the area for each group, so every group can kill its own copy. A **lockout** is the rule that stops a character from killing the same instanced boss again until a timer resets.

## 2. Worked example: one dragon, many guilds

### The hook

In classic EverQuest, the original raid bosses were two dragons and a sea creature: Lord Nagafen in Nagafen's Lair, Lady Vox in Permafrost, and Phinigel Autropos in Kedge Keep. The Project 1999 Wiki, which documents a fan-run recreation of the game's classic era, lists Nagafen and Vox as level 55 with a respawn time of 7 days, plus or minus 8 hours. Phinigel respawns every 12 hours.

So on a whole server, one Nagafen appeared per week. It did not matter whether that server had one guild able to kill him or ten. A shared weekly spawn forces guilds either to race each other to the lair or to agree on who takes which spawn. Why did the endgame feel better on a quiet server than on a busy one? The model gives the answer in one line.

### The model

Let:

- `T` be the respawn timer in days. Spawns per week are `s = 7 / T`.
- `G` be the number of guilds that can kill the boss and want it.
- `R` be the raid size, the number of players who share one kill's loot.
- `d` be the number of items that drop per kill.
- `L` be the lockout in days, for an instanced version.

For a **contested** boss shared fairly among guilds (each guild gets an equal share of kills over time):

```
kills per guild per week      k = s / G
items per raider per week     i = s × d / (G × R)
weeks until one item          W = G × R / (s × d)
```

For an **instanced** boss with lockout `L`:

```
kills per guild per week      k = 7 / L
items per raider per week     i = 7 × d / (L × R)
weeks until one item          W = L × R / (7 × d)
```

The whole lesson sits in one symbol. `G` appears in the contested formulas and not in the instanced ones. In a contested world, the server's total supply of this boss's items is `s × d` per week, fixed by the designer, and every new guild divides it further. In an instanced world, each guild gets its own supply.

`W` is an expected value from MA102 week 4. It assumes every drop is equally useful to every raider. Real loot tables have class-specific items, so a real raider waits longer. The model gives the best case.

### Numbers you can check

Use Nagafen's timer from the wiki, `T = 7`, so `s = 1` spawn per week. The drop count and raid size are assumptions for the example, not documented figures: `d = 3` items per kill, `R = 40` raiders.

| Guilds `G` | Kills per guild per week | Items per raider per week | Weeks until one item |
|---|---|---|---|
| 1 | 1.00 | 0.075 | 13.3 |
| 2 | 0.50 | 0.0375 | 26.7 |
| 4 | 0.25 | 0.01875 | 53.3 |
| 8 | 0.125 | 0.009375 | 106.7 |
| Instanced, `L = 7`, any `G` | 1.00 | 0.075 | 13.3 |

Check the `G = 4` row by hand. `i = 1 × 3 / (4 × 40) = 3 / 160 = 0.01875`. Its reciprocal is `160 / 3 ≈ 53.3` weeks, about a year for one item.

Now change the timer. Phinigel respawns every 12 hours, so `T = 0.5` and `s = 14`. The wiki says a few players can kill him, so try `R = 6`. With eight guilds and the same `d = 3`:

```
i = 14 × 3 / (8 × 6) = 42 / 48 = 0.875 items per raider per week
W = 1 / 0.875 ≈ 1.1 weeks
```

Same number of competing guilds, a hundred times shorter wait. The spawn timer and the raid size are design dials, and they matter as much as the competition does.

### Rotation or race

The formulas above assume guilds share kills evenly. That happens only if players agree to a rotation. Without one, the fastest guild wins most spawns. Model that with one more number, `q`, the share of spawns the strongest guild takes. The others split `1 − q` evenly.

With `G = 4`, `q = 0.7`, `s = 1`, `d = 3`, `R = 40`:

| Guild | Kills per week | Weeks until one item |
|---|---|---|
| Strongest guild | 0.70 | 19.0 |
| Each of the other three | 0.10 | 133.3 |

Check the second row. Each other guild gets `0.3 / 3 = 0.1` kills per week, so `i = 0.1 × 3 / 40 = 0.0075` and `W ≈ 133.3` weeks. That is more than two and a half years.

The server's total supply did not change. Only its distribution did. A race concentrates rewards in one guild, which then gets stronger and wins more races. That is a positive feedback loop (GD102 week 3) built from nothing more than a respawn timer.

### A visual you can move

Open `examples/w04-contested-spawn.html`. The left panel plots weeks until one item against the number of guilds, 1 to 12. The contested curve rises in a straight line, because `W` is proportional to `G`. The instanced line stays flat. The right panel is a 26-week calendar. Each column is one spawn, colored by the guild that got it. Move the `q` slider from "rotation" to "race" and watch the calendar fill with one color while the other guilds' bars on the left climb off the chart. The number panel under the chart shows `s`, `i` and `W` for every guild, to the same precision as the tables above.

Then set `G` back to 1. The two lines touch. Contested and instanced content are the same when only one guild wants the boss. The difference exists only because the world is shared.

### Cross-game recognition

**World of Warcraft, classic era (2004 to 2006).** WoW shipped its main raids as instances. Molten Core holds 40 players and has a one-week lockout. In the model that is `L = 7`, and `G` disappears. WoW also kept a few open-world bosses, and Warcraft Wiki records what contention did to one of them. During the Gates of Ahn'Qiraj event, a quest step required players to talk to the dragon Azuregos, but he was usually killed within a few hours of spawning. Blizzard added an unkillable Spirit of Azuregos so the quest could be completed. A shared boss with a high `G` is not only slow loot. It can block content for everyone who lost the race.

**EverQuest itself, 2003 to 2004.** EverQuest changed its own model. Lost Dungeons of Norrath (9 September 2003) introduced broad instanced dungeons for groups. Gates of Discord (10 February 2004) shipped with nine raid zones and instances. The game that made the contested raid famous moved toward the lockout formula five years after launch.

**The Sleeper, a boss with `s` close to zero.** The Scars of Velious expansion (5 December 2000) added Sleeper's Tomb. Killing the four dragons guarding it woke Kerafyrm, the Sleeper, in what Wikipedia calls the game's first world-changing event. The Project 1999 Wiki says the event can run only once per server. On that project's servers it was triggered on 31 January 2016 on one server and 13 April 2022 on another. With one spawn per server, ever, `i` is effectively zero for everyone except the guild that wins. That makes it a story for the whole server, not a reward. Designers still use once-per-world events this way, as history rather than loot.

**Shared tagging.** MMO303 week 10 analyzes how WoW changed who gets loot from an open-world kill, first to everyone of the tapping faction (patch 5.1.0) and then to up to five groups (patch 7.0.3). In this model those changes make `d` scale with the number of participants. The boss stays shared, but the reward stops being rival. See [MMO303 week 10](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w10-game-theory-payoff-matrices-and-nash-equilibria.md) for the game theory of guilds meeting at one spawn.

Four cases, one question. When you see an endgame reward, ask whether one group's gain removes it from another group. If it does, `G` is in the formula.

### Eyes-open design judgment

Contested content is not a mistake. It is a set of trade-offs.

- **What contention buys.** Other guilds matter. A server has a history of who killed what first, rivalries, rotation agreements, and a reason to watch the world. Ultima Online wanted players to affect each other. EverQuest's contested bosses did that without player-versus-player combat.
- **What contention costs.** The loot rate per player falls as the population rises, which punishes your own success. Rewards concentrate in the fastest guild. Players organize their lives around spawn windows, and the press was already calling the game "EverCrack" in 2000 (USA Today).
- **What instancing buys.** Rewards per player become independent of population. You can tune `L` and `d` once and trust them on every server. Schedules move from the world's clock to the guild's.
- **What instancing costs.** Other guilds stop mattering to your progress. The world becomes a lobby between instances. Week 7's themepark lecture returns to this cost.
- **What to decide on purpose.** For each reward, decide whether it should be rival. Put rival rewards where you want competition and stories, and non-rival rewards where you want predictable progress. Then choose `T`, `L`, `d` and `R` from the target `W` you want a typical raider to feel.

### Check yourself (worked example)

1. A contested boss spawns every 3 days, drops 4 items and is killed by raids of 50. Six guilds share it evenly. How many weeks does a raider wait for one item?
2. You want that wait to be 20 weeks with the same six guilds and raid size. Keeping `T = 3`, what `d` do you need? Keeping `d = 4`, what `T`?
3. Under the same boss, the strongest of the six guilds takes 60% of the spawns. How long does a raider in one of the other five guilds wait?

<details>
<summary>Answers</summary>

1. `s = 7 / 3 ≈ 2.333`. `i = 2.333 × 4 / (6 × 50) ≈ 0.0311`, so `W ≈ 32.1` weeks.
2. `W = G × R / (s × d)`, so `d = 6 × 50 / (2.333 × 20) ≈ 6.4` items per kill. Or `s = 6 × 50 / (4 × 20) = 3.75` spawns per week, so `T = 7 / 3.75 ≈ 1.87` days.
3. The others share `0.4 × 2.333 = 0.933` kills per week, so each gets `0.187`. `i = 0.187 × 4 / 50 ≈ 0.0149`, and `W ≈ 67` weeks.

</details>

## 3. The level treadmill

The raid is the end of the treadmill. The levels are the belt.

### What EverQuest's curve looks like

The Project 1999 Wiki gives the classic-era formula for the total experience needed to finish level `L`:

```
total XP at end of level L = L³ × C × R × H
```

`C` and `R` are class and race multipliers. Some combinations needed 68% more experience than others. `H` is a level multiplier that is 1.0 up to level 29, then rises in steps: 1.1 at level 30, 1.2 at 35, 1.3 at 40, 1.4 at 45, and higher in the 50s, up to 3.0 at level 59 and 3.1 at 60.

The `L³` part alone means experience per level grows roughly with `L²`. That is a polynomial curve in GD203 week 7's families. The step changes in `H` created what players called **hell levels**. The wiki's example is that level 39 to 40 needs about 5.3 million experience, 40 to 41 about 12.0 million, and 41 to 42 about 6.4 million. The level that crosses a step in `H` pays for the whole step. The wiki also reproduces a September 2002 patch note that smoothed levels 50 to 60 for later eras while keeping their total cost the same.

### Why it is a treadmill

A monster's experience grows too. The wiki gives about `L² × ZEM` for a solo kill of a monster of level `L`, where ZEM is a zone modifier. If a level needs about `L²` more experience and each kill gives about `L²` more, the number of kills per level stays roughly flat. You are running at the same pace on a longer belt that moves under you. That is the treadmill shape. Power grows, and so does the price of the next step, and the ratio between them barely changes.

Two more rules make the belt dangerous. From level 5, death costs experience, and enough deaths can take you down a level. A cleric's Resurrection spell returns 90% of the lost experience if it is cast within 3 hours of death. Your corpse keeps your items for 7 days, and you have to go back and get it. Week 5 turns these rules into a model. For now, note that the treadmill has a way to push you backward.

### Why a subscription wants a treadmill

GS101 week 9 showed that a flat monthly fee rewards goals that take months. A treadmill produces goals that take months at every level of play. A raid with a `W` of 50 weeks produces goals that take a year. Put them together and a player's next reward is always ahead, and always far enough away to justify another month. This is a business reading of the design, and it is not the only one. Plenty of players loved the long climb because it made each level feel earned. Your job is to see the mechanism, then decide what you want it to do.

## 4. The raid as a social machine

EverQuest's raids needed dozens of players online at once, at a time the world chose. That requirement built institutions.

- **Guilds became organizations.** Scheduling, attendance and recruitment are what a guild does when its members' rewards depend on showing up together.
- **Loot needed rules.** When 40 players share 3 items, someone must decide who gets them. Guilds invented systems for it, such as points earned for attendance and spent on items. MMO304's economy courses treat these as currencies inside a guild.
- **Servers had politics.** Contested bosses made guilds negotiate with each other, keep records of who had which spawn, and sometimes break agreements.

This is the same result Ultima Online produced with open player combat, a society that the designers did not script, but built from a different pressure. Ultima Online pushed players against each other through danger. EverQuest pushed them together through scarcity and pushed guilds against each other through contention. When you design a world, ask which pressure your rules apply, and what institution players will build to cope with it.

The cost falls on the players who cannot fit the schedule. A raid that needs 40 people at 8 p.m. on a Tuesday excludes everyone who works that shift. Week 5 shows how World of Warcraft answered that problem, and what it lost by doing so.

## In-class activity (25 minutes)

In groups of three, design the endgame for a server of 3,000 active players at the level cap, of whom about 400 raid seriously in 10 guilds.

1. (8 min) Pick one boss to be contested and one to be instanced. For each, choose `T` or `L`, `d` and `R`.
2. (7 min) Compute `W` for a raider in a mid-ranked guild under rotation, and under a race with `q = 0.5`.
3. (5 min) The server grows to 16 raiding guilds. Recompute. Which of your bosses breaks, and at what `G` does the contested wait pass one year?
4. (5 min) Write two sentences on what the contested boss gives the server that the instanced one cannot.

Expected output: a small table of your parameters and `W` values, the `G` at which the contested boss fails, and the two sentences. Keep it for Lab 04.

## Common misconceptions

- **"More players means more loot."** For contested content the server's supply is fixed at `s × d` per week. More players means less loot each.
- **"Instancing made raids easier."** Instancing changes who can attempt a boss and how often. It says nothing about the difficulty of the fight itself.
- **"Hell levels were a bug."** They follow directly from the step changes in the level multiplier `H`. A step in a multiplier lands entirely on the level that crosses it. Any curve built from stepped multipliers has them unless the designer smooths them.
- **"The treadmill is a trick to keep people paying."** It is a curve shape, power and cost rising together. It has business effects, and many players also valued it. Name the mechanism before you judge it.

## Check yourself

1. A contested boss has `T = 7`, `d = 5`, `R = 30` and `G = 5` guilds in rotation. Compute `i` and `W`. The server adds three guilds. What happens to `W`?
2. The same boss becomes instanced with a 7-day lockout. What is `W` now, and does it depend on the number of guilds?
3. Using the classic multipliers from section 3, explain why level 40 to 41 costs more than 41 to 42, even though 41 to 42 is the higher level.
4. A designer proposes a world boss that spawns once a day and drops one item for the whole server, "so that it feels special." Using the model, predict what a server with 20 competing guilds will experience. Suggest one change that keeps the boss rival but fixes the worst effect.
5. Explain in two sentences how a respawn timer can create a positive feedback loop between guilds.

<details>
<summary>Answers</summary>

1. `s = 1`. `i = 1 × 5 / (5 × 30) ≈ 0.0333`, so `W = 30` weeks. With 8 guilds, `W = 8 × 30 / 5 = 48` weeks. `W` is proportional to `G`.
2. `W = L × R / (7 × d) = 7 × 30 / 35 = 6` weeks per item. It does not depend on `G`.
3. `H` steps from 1.2 to 1.3 at level 40. The experience needed for a level is the difference between two totals, so the level that crosses the step pays for the whole jump in `H` applied to `L³`. The next level has the same `H` as the one before it, so it pays only for the growth in `L³`.
4. `s = 7`, `d = 1`, so 7 items per week for the whole server. With 20 guilds of, say, 40 raiders, that is 7 items for 800 people, about one item per raider every 114 weeks. Most guilds will never see it, and the fastest guild will take most kills. Keep it rival but give every guild that participates a smaller guaranteed reward (a token), or scale `d` with participants as WoW's later tapping rules did.
5. The guild that wins a spawn gets items that make it stronger, and a stronger guild reaches and kills the next spawn faster. So winning raises the chance of winning again, which is a positive feedback loop.

</details>

## Lab / assignment hook

[Lab 04, contested versus instanced loot](../labs/lab04.md). You build a spreadsheet that simulates 52 weeks of a server with one contested and one instanced boss, measure the loot each guild receives under rotation and race, and write a 400-word endgame policy memo. The analysis feeds the EverQuest case study in the case-studies assignment (40%).

## Sources

- Project 1999 Wiki, "Lord Nagafen" and "Lady Vox" (classic-era pages, accessed September 2026). Level 55, respawn time 7 days plus or minus 8 hours, one of the original three raid bosses. Project 1999 is a fan-run recreation of classic EverQuest (1999 to 2001 rules), so treat its timers as documentation of that recreation.
- Project 1999 Wiki, "Phinigel Autropos" (classic era). 12-hour respawn; can be killed by a few players.
- Project 1999 Wiki, "Kerafyrm" (Velious era). The event runs only once per server; woken on the Blue server on 31 January 2016 and on the Green server on 13 April 2022.
- Project 1999 Wiki, "Experience" (classic era). Total experience `L³ × C × R × H`; class and race multipliers up to a 68% penalty; the level multiplier table from 1.0 to 3.1; the 39-40, 40-41 and 41-42 example; the September 2002 smoothing patch note; solo experience about `L² × ZEM`; experience loss on death from level 5, with level loss possible.
- Project 1999 Wiki, "Resurrection" (spell restoring 90% of lost experience) and "Corpse" (player corpses decay after 7 days; resurrection possible within 3 hours).
- Wikipedia, "EverQuest" (accessed September 2026). Release on 16 March 1999; PvP only on PvP servers, arenas and duels; 2011 Game Developers Choice Online Hall of Fame citation for guilds and raiding; the "EverCrack" nickname (USA Today, 8 September 2000).
- Wikipedia, "EverQuest expansions" (accessed September 2026). Scars of Velious released 5 December 2000 with Sleeper's Tomb and the first world-changing event; Lost Dungeons of Norrath released 9 September 2003 with broad instanced dungeons; Gates of Discord released 10 February 2004 with nine raid zones and instances.
- Warcraft Wiki, "Molten Core" (40 players, one-week lockout, classic) and "Azuregos" (killed within hours of spawning; the Spirit of Azuregos added during the Gates of Ahn'Qiraj event).
- Bartle, R. (2003). *Designing Virtual Worlds*. New Riders.
- Castronova, E. (2005). *Synthetic Worlds: The Business and Culture of Online Games*. University of Chicago Press.

## Interactive spec: examples/w04-contested-spawn.html

**Insight the visual must make obvious:** in contested content, the wait for loot grows in a straight line with the number of competing guilds, while instanced content stays flat. The two are identical at one guild. A race makes the average worse for everyone except the winner.

**Layout.** Two linked panels side by side at 1280px, stacked at 390px. Left: "Weeks until one item" against number of guilds. Right: a 26-week spawn calendar. A number panel below both. A data table toggle at the bottom.

**Left panel.**
- x axis: guilds `G`, integers 1 to 12. y axis: weeks until one item `W`, 0 to 150 (clip values above, with an arrow marker and the value printed).
- Series 1 "Contested, rotation": `W = G × R / (s × d)` for each `G`. Solid line with circle markers.
- Series 2 "Instanced": `W = L × R / (7 × d)`, constant. Dashed line.
- Series 3 (only when `q > 1/G`) "Contested, race, other guilds": `W_other = R × (G − 1) / ((1 − q) × s × d)`, and series 4 "Contested, race, strongest guild": `W_top = R / (q × s × d)`. Distinct marker shapes (triangle, square), not only colors.
- A vertical cursor at the current `G`.

**Right panel.** A grid of `ceil(26 × s)` columns (cap at 182 columns and switch to a density strip if more), one per spawn in 26 weeks, grouped by week. Each cell is filled with the pattern and color of the guild that got that spawn. Rotation mode assigns spawns round-robin. Race mode assigns each spawn with a seeded pseudo-random draw: guild 1 with probability `q`, else uniformly among guilds 2 to `G`. Seed fixed at 42 and a "reroll" button. Beside the grid, a bar per guild with its kill count over the 26 weeks.

**Controls.**
- Respawn timer `T`: 0.5 to 14 days, step 0.5, default 7.
- Lockout `L`: 1 to 14 days, step 1, default 7.
- Drops per kill `d`: 1 to 10, default 3.
- Raid size `R`: 6 to 72, default 40.
- Guilds `G`: 1 to 12, default 4.
- Strongest guild's share `q`: from `1/G` (labelled "rotation") to 1.0, step 0.05, default `1/G`. When `G` changes, clamp `q` to at least `1/G`.
- Presets: "Nagafen" (`T = 7`, `d = 3`, `R = 40`), "Phinigel" (`T = 0.5`, `d = 3`, `R = 6`), "Molten Core style" (`L = 7`, `d = 3`, `R = 40`). Label the drop counts in presets as "assumed".

**Number panel (always visible).** `s = 7 / T`; server supply `s × d` items per week; for the current `G`: contested `i` and `W` (rotation), instanced `i` and `W`, and in race mode `W_top` and `W_other`. Values to 4 significant figures for `i` and 1 decimal for `W`.

**Formulas.** `s = 7 / T`. Rotation: `i = s × d / (G × R)`, `W = 1 / i`. Instanced: `i = 7 × d / (L × R)`, `W = 1 / i`. Race: top guild kills `q × s`, others `(1 − q) × s / (G − 1)` each.

**Test values.**
- `T = 7, d = 3, R = 40`: `G = 1, 2, 4, 8` give `W = 13.3, 26.7, 53.3, 106.7`. Instanced `L = 7`: `W = 13.3` at every `G`.
- `T = 0.5, d = 3, R = 6, G = 8`: `i = 0.875`, `W = 1.1`.
- `T = 7, d = 3, R = 40, G = 4, q = 0.7`: `W_top = 19.0`, `W_other = 133.3`.
- `T = 3, d = 4, R = 50, G = 6`: `W = 32.1`.

**Style and accessibility.** Tokens from `templates/interactive-tokens.css`. Up to 12 guild colors from the categorical palette plus a distinct fill pattern per guild so the calendar reads without color. All sliders keyboard operable with visible values. Respect `prefers-reduced-motion` (no calendar fill animation). No game art or logos; guilds are "Guild 1" to "Guild 12".

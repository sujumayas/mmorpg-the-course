# MMO301 · Week 07 — Themepark vs sandbox

**Why this matters:** Every MMO team argues about "themepark" and "sandbox" sooner or later, usually as a matter of taste. This week you turn the argument into a question about supply. Where does a player's next new experience come from, how much does it cost, and what happens to that supply when your population shrinks or your most devoted players play twice as much?

**You will be able to:**
- Define themepark and sandbox structures by who sets goals and who produces the content, and place a real game on that map with evidence.
- Compute a player's novelty share under an authored-content model and a player-driven model, and find the population where they cross.
- Predict how play time, sharding and population decline change which structure delivers more new experiences.
- Critique a hybrid design by naming what each half depends on and what it costs to run.

**Before class:** Reread your notes on Juul, "The Open and the Closed: Games of Emergence and Games of Progression" (2002), from GD102 week 10. Castronova, *Synthetic Worlds* (2005), chapters 1 to 4 (course reading list). Skim your notes from MMO301 weeks 3 to 6 (Ultima Online, EverQuest, World of Warcraft, EVE Online).

**Prerequisites from earlier courses:** [GD102 week 10, emergence vs progression](../../GD102-systems-design-and-game-mechanics/lectures/w10-emergence-vs-progression.md) (the single-player version of this week's argument; not re-taught here). [MA101 week 6, rational functions and asymptotes](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w06-rational-functions-and-asymptotes.md) (the shape `N / (N + K)`). [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) (combining two independent sources). [GS101 week 9, graphical MMOs](../../GS101-history-and-critical-study-of-games/lectures/w09-graphical-mmos-meridian-59-ultima-online-everquest.md) and [GS101 week 10, World of Warcraft](../../GS101-history-and-critical-study-of-games/lectures/w10-world-of-warcraft-and-the-mass-market-mmo.md) (the history this lecture assumes). From this course, [week 4, EverQuest and the treadmill](w04-everquest-the-treadmill-and-the-raid.md), [week 5, World of Warcraft and the themepark](w05-world-of-warcraft-accessibility-and-the-themepark.md) and [week 6, EVE Online and the single-shard sandbox](w06-eve-online-the-single-shard-sandbox.md). Also [week 3, Ultima Online](w03-ultima-online-the-simulation-dream-and-its-limits.md).

**Interactive:** [Where the next new thing comes from](../examples/w07-novelty-crossover.html). Keep it open during section 2.

---

## 1. Two answers to "what do I do tonight?"

Log into any MMO after dinner and the game has to answer one question. What will you do for the next two hours that you have not already done?

Week 5 introduced the first answer and week 6 the second. A **themepark** answers with content the developers made. Quest chains, dungeons, raids, scripted events and story. Each piece was built, placed, tested and tuned by the team. You ride the rides. When you have ridden them all, you wait for the next patch or ride them again for better loot.

A **sandbox** answers with systems and other people. It gives you tools (crafting, building, trading, territory, open combat) and a shared space. The next new thing that happens to you comes mostly from what other players decided to do. Nobody on the team wrote it.

Both words are industry shorthand, not formal terms, and people use them loosely. To make them usable, split them along two questions:

| | Designer produces the content | Players produce the content |
|---|---|---|
| **Designer sets the goals** | Classic themepark: quest hubs, dungeon ladders, raid tiers | Player-made content inside designer goals: a player-run market in a quest-driven game, user-made dungeons |
| **Players set the goals** | Open world full of authored places with no required path | Classic sandbox: player cities, territorial wars, player-run economies |

The top-left and bottom-right cells are the pure types. Most shipped games have pieces in all four cells, and the interesting design work is deciding how much of each.

In GD102 week 10 you met Juul's split between games of **progression** (the designer lays out challenges in sequence) and games of **emergence** (a few rules combine into many situations). A themepark is progression built at the scale of a world. A sandbox is emergence with one extra ingredient. The rules combine with each other, and they also combine with thousands of human beings who each have their own goals. That extra ingredient is what this lecture is about, because it behaves very differently from rules alone.

### Where you met this already

You have seen both structures in this course's history weeks. Ultima Online (1997) launched as a simulation-heavy world where players could kill each other almost anywhere and build houses in the open world. EverQuest (1999) organized play around camps, groups and raids placed by designers. World of Warcraft (2004) made the quest chain the spine of levelling. EVE Online (2003) put its whole player base in one universe and let players own space. GS101 week 9 and week 10 cover the history. Here you will look at the machinery underneath.

## 2. Worked example: where the next new thing comes from

### The hook

On 27 January 2014, a player corporation in EVE Online failed to make a routine sovereignty payment for a star system called B-R5RB. The payment was an in-game upkeep fee, the kind of chore nobody thinks about. Because it lapsed, the system lost its protective timers. A rival coalition noticed, and within hours both sides were pouring fleets into one star system.

The fight lasted about 21 hours. By CCP's count, more than 7,500 characters took part across the battle and its side fights, with a peak of 2,670 in the system at once. Around 11 trillion ISK (EVE's currency) of ships were destroyed, including 75 titans, the largest ship class. CCP, the developer, later put a monument in the system.

Nobody at CCP designed that battle. There was no quest, no raid boss, no scheduled event. The most famous night in the game's history came from a missed bill and the players who reacted to it.

Now compare the other structure. Suppose a themepark studio spends six months building a raid, and a dedicated guild playing every night finishes it in two weeks. The numbers are invented, but the ratio is the point. Themepark content is expensive to produce and cheap to consume. Sandbox content costs the studio almost nothing per event, but it depends entirely on who else is online.

So which structure gives a player more new experiences per hour? The answer depends on a number you can compute.

### One model, stated once

Define a player's **novelty share** as the fraction of their play time spent on situations they have not already experienced. It runs from 0 (everything is a repeat) to 1 (everything is new). This is a teaching model. It leaves out quality and taste on purpose, so you can see the supply side clearly.

**Authored content (themepark):**

```
s_T = min(1, p / h)
```

- `p` is the hours of new authored content the team ships per month, measured as the time a typical player takes to finish it once.
- `h` is the hours the player plays per month.
- The `min` caps the share at 1. If the team ships more than you can play, everything you play is new.

This assumes the player has already finished the launch content, which for an MMO player past the first months is the normal case. After that, the only new authored hours are the ones the team keeps shipping.

**Player-driven content (sandbox):**

```
s_S = N / (N + K)
```

- `N` is the number of other players within reach, meaning online in the same shard and close enough in the world or the social graph to affect you.
- `K` is the **half-novelty population**, the number of players in reach at which half your play time involves situations other players created. It depends on the tools the game gives players. Rich tools for conflict, trade and building make `K` smaller.

You have seen this shape before. It is `A / (A + K)` from MA101 week 6 and the armor formula from MMO303. It starts at 0, climbs fast, and flattens toward 1 without ever reaching it. An empty sandbox gives you nothing. A crowded one gives you a lot, and each extra player adds a little less.

**The crossover.** The sandbox delivers more novelty than the themepark when `s_S > s_T`. Solve `N / (N + K) = s_T` for `N`:

```
N* = K × s_T / (1 − s_T)
```

Below `N*` players in reach, the themepark wins on novelty. Above it, the sandbox wins.

**Hybrid.** A game can have both sources. If you treat them as independent chances that a given hour is new, the complement rule from MA102 week 3 gives

```
s_H = 1 − (1 − s_T) × (1 − s_S)
```

### Numbers you can check

Take a studio that ships `p = 10` hours of new authored content per month, and a player who plays `h = 40` hours per month (about ten hours a week). Then `s_T = 10 / 40 = 0.25`. A quarter of this player's time is new authored content, whatever the population.

For the sandbox, take `K = 300`.

| Players in reach `N` | Sandbox `s_S = N/(N+300)` | Themepark `s_T` | Hybrid `s_H` |
|---|---|---|---|
| 0 | 0% | 25% | 25% |
| 50 | 14.3% | 25% | 35.7% |
| 100 | 25.0% | 25% | 43.8% |
| 300 | 50.0% | 25% | 62.5% |
| 900 | 75.0% | 25% | 81.3% |
| 2,700 | 90.0% | 25% | 92.5% |

Check the crossover with the formula: `N* = 300 × 0.25 / 0.75 = 100`. The table agrees. At 100 players in reach, both sources give 25%.

Now change the player. A devoted player at `h = 160` hours per month (about five hours a day) gets `s_T = 10 / 160 = 6.25%` from the same patch schedule. Their crossover drops to

```
N* = 300 × 0.0625 / 0.9375 = 20
```

Twenty players in reach are enough for the sandbox to out-supply the themepark for this person. The heaviest players are the first to run out of authored content, and they are also the ones who most need other people.

To give that 160-hour player back a 25% authored share, the team would need `p = 0.25 × 160 = 40` hours of new content per month, four times the output. That is the arithmetic behind the content treadmill from [week 4](w04-everquest-the-treadmill-and-the-raid.md). Authored supply has to scale with play time. Player-driven supply scales with population.

### A visual you can move

Open the interactive. The left panel plots novelty share against players in reach on a log axis, with the flat themepark line, the rising sandbox curve and the hybrid curve above both. A marker shows `N*`. The right panel shows the same player's month as a bar of 40 (or `h`) hours, split into "new authored", "new player-made" and "repeat".

Drag `h` from 40 to 160. The themepark line drops and the crossover marker slides left toward 20. Then drag the population slider down, the way an MMO population falls after its launch year. The sandbox curve does not move, but your position on it slides toward zero, and the repeat share in the bar grows. The themepark bar does not care about population at all. That contrast is the whole lesson. One structure is fragile to play time, the other is fragile to population.

### Cross-game recognition

**EVE Online (2003 to now).** EVE runs one main universe, Tranquility, for nearly all players outside China, where many other MMOs run many parallel copies of their world. In this model, a single shard is a decision to maximize `N` for everyone. CCP's player count once peaked at 65,303 accounts logged in at the same time, on 5 May 2013. The B-R5RB battle needed thousands of players to be able to reach one star system. You cannot build that event in a game with a few thousand players per server copy.

**World of Warcraft, patch 3.3.0 (8 December 2009).** WoW is the standard themepark, but its group content still depends on other people. You need four others to run a five-player dungeon. Patch 3.3.0 added the cross-server Dungeon Finder, which built groups from players across every server in a battlegroup and teleported them to the dungeon. In this model, Blizzard raised `N` for the player-dependent part of the game without merging its servers. It is the same fix EVE made with one shard, applied to one activity instead of the whole world.

**Star Wars Galaxies (2003 to 2011).** Galaxies launched on 26 June 2003 as a sandbox. It had 34 professions at launch, a crafting-driven economy, and player cities with elected mayors. Reviewers praised the sandbox approach and criticized the lack of quest content. The May 2005 expansion added Kashyyyk, a planet split into a small open area plus instanced dungeons. In November 2005 the New Game Enhancements cut the professions to nine, and SOE's president defended the change as a response to a shrinking subscriber base. Read it through the model. A sandbox losing players watches its `s_S` fall, so the team moved toward authored content, whose novelty does not depend on population. The cost was that the players who had stayed for the sandbox lost what they came for, and many left. The servers closed on 15 December 2011.

Three games, one trade. EVE pushed `N` up for everyone. WoW pushed `N` up for one activity. Galaxies tried to swap one supply for the other in the middle of the game's life.

### Eyes-open design judgment

Neither structure is "better". Each fails in a predictable way, and you should choose which failure you can afford.

- **Themepark strength.** Novelty does not depend on population. A quiet server at 3 a.m. still has every quest. Content quality is controlled, so you can tell a story and tune a difficulty curve.
- **Themepark cost.** Supply is capped by your team's output, and demand grows with play time. Your most devoted players outrun you first. You will reach for repeatable content (daily quests, lockouts, random loot) to stretch hours, which trades novelty for repetition. MMO303 and MMO306 cover how to tune that stretch.
- **Sandbox strength.** Supply grows with players. A healthy population produces events no studio could afford to script, and it keeps producing them for years.
- **Sandbox cost.** Novelty needs density. At launch, in a declining year, or on a small shard, the sandbox is thin and the repeat share climbs. Player-made content is also uneven. Some of it is war, betrayal and griefing, which some players love and others quit over (week 8 looks at this with Bartle's population model).
- **Hybrids buy both curves.** The hybrid column in the table is always above both. But each half keeps its own weakness. You still pay the authored treadmill, and you still need density.

The decision to make on purpose is where your target population sits relative to `N*`. If you expect a few hundred concurrent players in reach, a sandbox-first design is a bet that `K` is small. If you expect tens of thousands in one space, a themepark-only design leaves most of your supply unused.

### Check yourself (worked example)

1. A studio ships 15 hours of new content per month. With `K = 400`, find `N*` for a player who plays 60 hours per month.
2. A sandbox has 8,000 players online spread over 20 shards of equal size, with everyone on a shard in reach. With `K = 300`, what is `s_S` per player? What would it be with one shard?
3. A hybrid game has `s_T = 0.2` and a player has 300 players in reach with `K = 300`. What is `s_H`? What share of their time is a repeat?

<details>
<summary>Answers</summary>

1. `s_T = 15/60 = 0.25`, so `N* = 400 × 0.25 / 0.75 ≈ 133` players.
2. 400 per shard, `s_S = 400/700 ≈ 57.1%`. With one shard, `N = 8,000`, `s_S = 8,000/8,300 ≈ 96.4%`. In practice not all 8,000 are in reach, which is why `N` is "in reach", not "online".
3. `s_S = 0.5`, so `s_H = 1 − 0.8 × 0.5 = 0.6`. Repeat share is 40%.

</details>

## 3. What "in reach" hides

The model's weakest symbol is `N`. Two games with the same number of players online can give very different `N`.

**Sharding.** A shard (also called a server or realm) is a full copy of the world. Players on different shards cannot meet. Splitting 30,000 players into ten shards gives each player at most 3,000 others in reach. Themeparks shard freely because authored content does not care. Sandboxes shard at a cost, because every split divides `N`.

**Geography.** Even on one shard, a player in a remote region has few others nearby. A large map spreads players thin. Travel time, fast travel and chokepoints all change how many players are really in reach. World design decides `N` as much as server count does.

**Instancing.** An instance is a private copy of an area for one group. A themepark raid instance sets `N` to the raid group by design. That protects the authored experience from interference, and it also switches off the player-driven supply inside it.

**Social reach.** Guilds, chat channels, markets and matchmaking tools put people in reach without putting them in the same place. WoW's Dungeon Finder is one example. A global auction house is another. It makes every trader in the game part of your market.

When you evaluate a design, do not ask "how many players do we have?" Ask "how many players can affect a given player tonight, and through which systems?"

## 4. The spectrum in practice

Most MMOs sit between the pure types, and they often move along the spectrum during their lives. Three patterns recur.

**The sandbox that adds rides.** Launch as a sandbox, find that new players do not know what to do, and add authored guidance such as tutorials, starter quest chains and scripted events. This usually works when the authored layer leads players into the sandbox instead of replacing it.

**The themepark that adds tools.** Launch as a themepark, run into the treadmill, and add systems that let players create repeatable variety for each other: player housing, player markets, structured player-versus-player modes, user-built content. This works when the new tools have enough players to feed them.

**The conversion.** Change the core structure after launch. Star Wars Galaxies is the case you should remember. A conversion changes which players the game is for. The players who chose you for the old structure lose what they came for, and the players the new structure would suit are already playing a game built for them from the start.

### A diagnostic you can run on any MMO

Pick a game and log a typical two-hour session. For each 15-minute block, write down where the new experience (if any) came from.

- **A**, authored and new to you.
- **P**, created by other players (a trade, a fight, a conversation, a player-built place, a group you would not have met otherwise).
- **R**, repeat.

Count the blocks. The shares estimate `s_T`, `s_S` and the repeat share for that player on that night. They are not a measurement of the game. Log a quiet night and a busy night and the `P` count will change. That is the model saying the sandbox part depends on `N`.

## In-class activity (25 minutes)

In groups of three. Materials: the interactive, a sheet with the three studio briefs below, and a calculator.

- **Studio 1.** A team of 12 can ship 6 hours of new authored content per month. Target players play 30 hours per month. They expect 400 concurrent players per region.
- **Studio 2.** A team of 80 can ship 25 hours per month. Target players play 50 hours per month. They expect 20,000 concurrent players across 10 shards, with about 1,500 in reach for a typical player.
- **Studio 3.** A team of 30 ships 8 hours per month. Target players are devoted and play 120 hours per month. They plan a single shard with an estimated 5,000 players in reach.

Steps:

1. For each studio, compute `s_T`. Assume `K = 300` and compute `s_S` and `N*`.
2. Recommend themepark-first, sandbox-first or hybrid, in two sentences each.
3. Name the event that would break your recommendation (a population drop, a jump in play time, a server split) and how far it would have to go.

Expected output: a table of three rows (`s_T`, `s_S`, `N*`, recommendation) and three break conditions. Studio 1, for example, has `s_T = 0.2`, `N* = 75` and `s_S ≈ 57%` at 400 in reach. It is sandbox-leaning on paper, but its population would have to stay above 75 in reach, and a team of 12 cannot also run heavy moderation.

## Common misconceptions

- **"Sandbox means no content."** A sandbox has plenty of content. The players make it, and the studio makes the tools. The cost moves from content production to systems, moderation and balance.
- **"Themeparks are for casual players."** The model says the opposite about who suffers. Themepark supply runs out fastest for the players who play the most.
- **"More players always helps a sandbox."** Each extra player adds less novelty than the last (the curve flattens), and past some density, servers and social systems break. B-R5RB itself ran under EVE's time-dilation system, which slows the game to as little as 10% speed to keep the server alive.
- **"Adding a sandbox layer to a themepark is free variety."** The layer only produces novelty if enough players use it. A player market with ten sellers is not a market.

## Check yourself

1. A themepark ships 20 hours per month. Its players average 50 hours per month. What is `s_T`? How many hours per month would it need to ship to reach 50%?
2. Why does sharding hurt a sandbox more than a themepark? Answer with the two formulas.
3. A sandbox has `K = 500`. What `N` gives `s_S = 80%`?
4. Using the diagnostic in section 4, a student logs 8 blocks as `A, A, R, P, P, R, P, A`. Estimate `s_T`, `s_S` and the repeat share. What would you log next to test whether the `P` count depends on population?
5. A hybrid game currently gives a player `s_T = 0.3` and `s_S = 0.4`. The team can either double authored output or double the players in reach (from 200 to 400 with `K = 300`). Which raises `s_H` more?

<details>
<summary>Answers</summary>

1. `s_T = 20/50 = 0.4`. For 50% it needs `0.5 × 50 = 25` hours per month.
2. `s_T = p/h` contains no `N`, so splitting players across shards changes nothing. `s_S = N/(N+K)` falls when `N` is divided by the number of shards.
3. `N / (N + 500) = 0.8`, so `N = 0.8N + 400`, `N = 2,000`.
4. `A` 3 of 8 (37.5%), `P` 3 of 8 (37.5%), `R` 2 of 8 (25%). Log a second session at a different time of day with a noticeably different population, and compare the `P` counts.
5. Doubling authored output gives `s_T = 0.6` (if `h` is unchanged), so `s_H = 1 − 0.4 × 0.6 = 0.76`. Doubling reach from 200 to 400 gives `s_S = 400/700 ≈ 0.571`, so `s_H = 1 − 0.7 × 0.429 ≈ 0.70`. Doubling authored output wins here, but it costs a second content team every month. Current `s_H` is `1 − 0.7 × 0.6 = 0.58`.

</details>

## Lab / assignment hook

[Lab 07, content supply model](../labs/lab07.md). You build the novelty model in a spreadsheet, add sharding and population decline, run it on three game profiles and write a 400-word structure recommendation for a studio brief. The same memo format returns in the world design bible (week 15).

## Sources

- Juul, J. (2002). "The Open and the Closed: Games of Emergence and Games of Progression." *Computer Games and Digital Cultures Conference Proceedings*. Summarized in GD102 week 10.
- Wikipedia, "Battle of B-R5RB" (accessed September 2026, a Good Article citing CCP's official report and press coverage). Date 27 to 28 January 2014; missed sovereignty payment by a Nulli Secunda member corporation; about 21 hours; over 7,548 characters overall, peak 2,670 in system; 75 titans lost; estimated 11 trillion ISK destroyed; time dilation slowing the game to 10% speed; the Titanomachy monument.
- Wikipedia, "Eve Online" (accessed September 2026). Release May 2003; single main universe on the Tranquility server, with the separate Chinese server Serenity; record of 65,303 concurrent accounts on 5 May 2013.
- Warcraft Wiki, "Patch 3.3.0" and "Dungeon Finder" (accessed September 2026). Patch 3.3.0 released 8 December 2009 with cross-server Dungeon Finder; groups formed across the servers of a battlegroup, with teleport to the dungeon.
- Wikipedia, "Star Wars Galaxies" (accessed September 2026). Release 26 June 2003; 34 professions at launch; player cities and elections; reviews praising the sandbox approach and criticizing the lack of quest content; Kashyyyk with instanced dungeons in the May 2005 expansion; New Game Enhancements in November 2005 reducing professions to nine; SOE president John Smedley's defence of the change as a response to subscriber decline; shutdown on 15 December 2011.
- Castronova, E. (2005). *Synthetic Worlds: The Business and Culture of Online Games*. University of Chicago Press. Chapters 1 to 4.
- The novelty-share model, the value `K = 300` and all studio figures in this lecture are teaching constructions, not measurements from any game.

## Interactive spec: examples/w07-novelty-crossover.html

**The one insight.** Authored novelty is flat in population and falls with play time. Player-driven novelty is zero in an empty world and rises with population. The student must see the crossover point move left when play time rises, and see their own position slide down the sandbox curve when population falls, while the themepark share does not move.

**Layout.** Two panels, stacked on mobile, side by side at 1024 px and wider. Controls above.

**Controls.**
- Slider `h`, hours played per month, 10 to 200, step 5, default 40.
- Slider `p`, new authored hours shipped per month, 0 to 60, step 1, default 10.
- Slider `K`, half-novelty population, 50 to 2,000, step 50, default 300.
- Slider `N`, players in reach, logarithmic, 0 to 10,000 (map the slider to 0 then 10, 20, 50, 100, 200, 300, 500, 1,000, 2,000, 3,000, 5,000, 10,000 using fine steps between these anchors), default 300.
- Checkbox "Split into shards" with a number input `shards` 1 to 50, default 1. When on, the effective `N` is `N / shards` (label it "in reach per shard").
- Button "Launch year to year three": animates `N` from its current value down to 20% of that value over 4 seconds (skip animation, jump to end, when `prefers-reduced-motion` is set).
- All sliders keyboard operable, with visible numeric values.

**Formulas.**
- `s_T = min(1, p / h)`.
- `s_S = N_eff / (N_eff + K)`, with `N_eff = N` or `N / shards`.
- `s_H = 1 − (1 − s_T)(1 − s_S)`.
- Crossover `N* = K × s_T / (1 − s_T)`; show "never" if `s_T = 1` and "0" if `s_T = 0`.

**Left panel.** x axis players in reach, log scale from 1 to 10,000 (plot `N = 0` as a separate point at the left edge labelled "0"). y axis novelty share 0 to 100%. Flat line `s_T`, rising curve `s_S`, curve `s_H` on top. Vertical dashed marker at `N*` labelled with its value. A dot on each curve at the current `N_eff`.

**Right panel.** One horizontal bar of length `h` hours, split into three segments. Use the hybrid split: new authored `h × s_T`, new player-made `h × (s_H − s_T)`, repeat `h × (1 − s_H)`. Numeric hours and percentages next to each segment. Beneath, a second, thinner bar for "themepark only" (`s_T`, repeat `1 − s_T`) and a third for "sandbox only" (`s_S`, repeat `1 − s_S`).

**Readout.** `s_T`, `s_S`, `s_H`, `N*`, all to one decimal place in percent or whole players.

**Test values.**

| h | p | K | N (shards) | s_T | s_S | s_H | N* |
|---|---|---|---|---|---|---|---|
| 40 | 10 | 300 | 0 | 25.0% | 0.0% | 25.0% | 100 |
| 40 | 10 | 300 | 100 | 25.0% | 25.0% | 43.8% | 100 |
| 40 | 10 | 300 | 300 | 25.0% | 50.0% | 62.5% | 100 |
| 40 | 10 | 300 | 2,700 | 25.0% | 90.0% | 92.5% | 100 |
| 160 | 10 | 300 | 300 | 6.3% | 50.0% | 53.1% | 20 |
| 60 | 15 | 400 | 133 | 25.0% | 25.0% | 43.7% | 133 |
| 40 | 10 | 300 | 3,000 (10 shards) | 25.0% | 50.0% | 62.5% | 100 |
| 40 | 60 | 300 | 300 | 100% | 50.0% | 100% | never |

**Style.** Shared palette from `templates/interactive-tokens.css`. Three distinct series colors for authored, player-made and repeat, also distinguished by pattern or label so the chart reads in grayscale. No game logos or art. Game names appear only in a caption: "EVE Online keeps one shard to raise N. World of Warcraft's Dungeon Finder raised N for dungeons only."

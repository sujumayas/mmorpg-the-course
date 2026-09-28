# MMO301 · Week 13 — Worlds that died: shutdowns and their lessons

**Why this matters:** Most online worlds ever launched are now switched off. The ones that closed were rarely empty on the last day, and several closed while people were still paying. If you design a persistent world, you are also designing how it will fade, whether you plan for it or not. This week you learn to read the warning signs in the numbers, to see which of them a designer controls, and to plan an ending that respects the people who lived there.

**You will be able to:**
- Classify a shutdown by its main cause (empty-world spiral, business decision, licence or partner, platform) and name the evidence for it.
- Compute monthly population, churn and break-even for a sharded world with the density-churn model, and predict what a server merge does to them.
- Critique a real shutdown (Tabula Rasa, The Matrix Online, Star Wars Galaxies, City of Heroes, WildStar) against the design levers that were available.
- Design a sunset plan for a world, with dates, a final event and a preservation decision.

**Before class:** Bartle, *Designing Virtual Worlds* (2003), chapter 3, "Levels of Community" through "Influence Through Design" (pp. 288-302), which ends with "Churn, Sink, and Drift" on why newbies leave. Read the Wikipedia articles "Tabula Rasa (video game)" and "City of Heroes", the sections on closure only (about 15 minutes). Note every date and who announced what.

**Prerequisites from earlier courses:** [GD102 week 2, stocks and flows](../../GD102-systems-design-and-game-mechanics/lectures/w02-stocks-and-flows.md) (a population is a stock with an inflow and an outflow). [GD102 week 3, positive feedback loops](../../GD102-systems-design-and-game-mechanics/lectures/w03-positive-feedback-loops-snowballing.md) (a spiral is a loop that feeds itself). [MA101 week 6, rational functions and asymptotes](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w06-rational-functions-and-asymptotes.md) (the `H / (H + d)` shape in this week's churn term). [GS101 week 9, graphical MMOs](../../GS101-history-and-critical-study-of-games/lectures/w09-graphical-mmos-meridian-59-ultima-online-everquest.md) (subscribers versus players per shard). Within this course, [week 6 on EVE Online's single shard](w06-eve-online-the-single-shard-sandbox.md) and [week 12 on persistence](w12-persistence-and-time-what-should-last.md).

**Interactive:** [examples/w13-shard-spiral.html](../examples/w13-shard-spiral.html). Keep it open during section 2.

---

## 1. How a world dies

A shutdown looks like one event: the servers go dark on a named date. Behind the date there is almost always a longer story, and the story usually has one main cause. Learning to name the cause is the first skill of this week, because each cause points to different design lessons.

Here are five worlds that closed, with the facts we can check.

| World | Launched | Closure announced | Servers off | Reason given or recorded |
|---|---|---|---|---|
| The Matrix Online | March 2005 (NA) | June 2009 | 31 July 2009 | Fewer than 500 active players reported near the end |
| Tabula Rasa | November 2007 | 21 November 2008 | 28 February 2009 | Lower than expected population, per the developers |
| Star Wars Galaxies | June 2003 (NA) | 24 June 2011 | 15 December 2011 | SOE and LucasArts agreed to close it |
| City of Heroes | April 2004 (NA) | 31 August 2012 | 30 November 2012 | NCSoft cited a realignment of company focus |
| WildStar | June 2014 | 6 September 2018 | 28 November 2018 | NCSoft closed the studio, then set the date |

Read the last column carefully. Only two entries mention population. The others name a business decision or a partner agreement. That split gives us four families of cause.

**The empty-world spiral.** Players leave because the world feels empty, which makes it feel emptier, which makes more players leave. Tabula Rasa's developers named "lower than expected" population as the main factor. The Matrix Online's final numbers were tiny. This is the family a designer can influence most directly, and section 2 models it.

**The business decision.** The world may still have a paying community, but the owner decides the money and staff are better spent elsewhere. City of Heroes is the standard example. NCSoft closed Paragon Studios and gave "a realignment of company focus and publishing support" as the reason. More than 21,000 players signed a petition against the closure. The lesson is uncomfortable. A world can be healthy by its own measure and still be switched off, because the owner compares it with other uses of the same budget, not with zero.

**The licence or partner.** Star Wars Galaxies ran on a licence. The closure was announced as a mutual agreement between Sony Online Entertainment and LucasArts. When a world depends on someone else's intellectual property, its end date can be set by a contract you never see.

**The platform.** A world can die because its hardware, operating system, store or middleware goes away. EverQuest's Mac-only server, Al'Kabor, closed in November 2013 while the main game continued. Nothing about the design had failed. The platform around it had.

Most real closures mix causes. A spiral lowers revenue, which makes the business decision easy. A licence renewal comes up during a slump. When you write a post-mortem, name the main cause and the contributing ones, and say which evidence supports each. "The game died because it was bad" is not an analysis.

### Stock and flow, again

In GD102 week 2 you modelled resources as stocks with inflows and outflows. A world's population is the same kind of thing. The stock is the number of active players. The inflow is new and returning players per month. The outflow is churn, the fraction of current players who leave each month. A world grows when inflow beats outflow and shrinks when it does not.

What makes online worlds special is that the outflow depends on the stock. Other players are the content. A dungeon needs a group, a market needs sellers, a city needs a crowd, a guild needs members online tonight. When fewer people are around, each remaining player gets less from the world, so more of them leave. That is a positive feedback loop in exactly the GD102 week 3 sense, and it is why population problems accelerate once they start.

## 2. Worked example: the empty-shard spiral

### The hook

Tabula Rasa's developers blamed population. Blizzard, running the most successful subscription MMO of its era, built a whole feature called connected realms in World of Warcraft patch 5.4 (September 2013), and described its goal as giving players on lower-population realms more chances to group up, compete and connect. Neither statement is about the total number of players in the game. Both are about how many players you meet.

Here is the puzzle. Two worlds have the same 90,000 subscribers. One feels busy and keeps its players. The other feels like a ghost town and bleeds them. The difference is not in the total. It is in how the total is divided.

### The model

We split the world into `S` shards (also called servers or realms). Each shard is a separate copy of the world, and players on different shards cannot meet. Time runs in months.

```
d  = N / S                           players per shard (the density a player feels)
c  = c0 + c1 × H / (H + d)           monthly churn rate
N' = N × (1 − c) + A                 next month's population
```

- `N` is the number of active players (subscribers) this month.
- `S` is the number of shards.
- `d` is players per shard. This is the population a player can actually meet.
- `c0` is the base churn, the fraction who leave each month even in a busy world (life happens, other games launch).
- `c1` is the extra churn caused by emptiness. It is fully felt when a shard is empty and fades as the shard fills.
- `H` is the half-social density, the players per shard at which the emptiness penalty is half of `c1`.
- `A` is the number of new or returning players arriving each month.

The term `H / (H + d)` is the rational shape from MA101 week 6, turned around. At `d = 0` it equals 1, at `d = H` it equals ½, and as `d` grows it falls toward 0 without reaching it. So churn is highest in an empty shard and approaches `c0` in a crowded one.

We also need money. Each player pays `p` per month. Running the world costs a fixed `F` per month (the team, the office, the licence) plus `k` per shard (hardware, bandwidth, the people who watch it).

```
revenue   = p × N
cost      = F + k × S
break-even population  N_be = (F + k × S) / p
```

All numbers below are invented for teaching. Real studios do not publish them, and you should not treat them as industry figures. The values are `c0 = 0.03`, `c1 = 0.20`, `H = 2,000`, `A = 6,000` per month, `p = $15`, `F = $900,000` per month and `k = $10,000` per shard per month. The world launches with `N = 200,000` players on `S = 40` shards, because the launch team planned for a crowd.

### Numbers you can check

Start at launch. There are 200,000 players on 40 shards, so `d = 5,000`. The emptiness factor is `2,000 / 7,000 = 0.2857`. Churn is `0.03 + 0.20 × 0.2857 = 0.0871`, so 8.71% leave this month. That is 17,429 players. Add 6,000 arrivals and next month starts with 188,571.

| Month | N | d = N/40 | H/(H+d) | Churn c | Players lost | Next N |
|---|---|---|---|---|---|---|
| 0 | 200,000 | 5,000 | 0.2857 | 8.71% | 17,429 | 188,571 |
| 1 | 188,571 | 4,714 | 0.2979 | 8.96% | 16,891 | 177,680 |
| 2 | 177,680 | 4,442 | 0.3105 | 9.21% | 16,363 | 167,317 |
| 3 | 167,317 | 4,183 | 0.3235 | 9.47% | 15,844 | 157,473 |

Look at the churn column. It rises every month. The world is shrinking, so each shard is emptier, so churn goes up, so the world shrinks faster than it would at a fixed rate. That is the spiral, and you can compute each step by hand.

Where does it stop? The population settles when outflow equals inflow, `N × c = A`. Because `c` depends on `N / S`, the resting population depends on the number of shards. Solving numerically:

| Shards S | Resting population N* | Players per shard | Churn at rest | Break-even N_be | Verdict |
|---|---|---|---|---|---|
| 40 | 35,637 | 891 | 16.8% | 86,667 | Loses money forever |
| 20 | 50,803 | 2,540 | 11.8% | 73,333 | Loses money forever |
| 10 | 90,746 | 9,075 | 6.6% | 66,667 | Profitable |
| 5 | 137,843 | 27,569 | 4.4% | 63,333 | Profitable |
| 1 | 186,808 | 186,808 | 3.2% | 60,667 | Profitable |

Same arrivals, same players, same game. The only change is how the population is divided, and the resting population differs by a factor of five between 40 shards and one. You can check any row. Take `S = 10`. Then `d = 9,075`, `H / (H + d) = 2,000 / 11,075 = 0.1806`, `c = 0.03 + 0.0361 = 0.0661`, and `90,746 × 0.0661 ≈ 6,000`, which equals `A`. The world is in balance.

The one-shard row is not a free lunch. The model has no crowding term, so it cannot see lag, queues, camped spawns or a market that one guild controls. Week 6 looks at what EVE Online pays in engineering to run one shard. Treat the bottom row as "what density alone would give you."

### Merging: when you act matters

The launch team built 40 shards. Suppose the operations team decides to merge them into 10. The model says the world will end up near 90,746 players whenever they merge, because there is only one resting point for `S = 10`. So does timing matter? It matters for the money.

Without a merge, the 40-shard world first drops below its break-even of 86,667 in month 14 (85,407 players). Now try merging at different months:

| Merge at month | N at merge | Months spent below break-even | N at month 60 |
|---|---|---|---|
| 6 | 139,306 | 0 | 97,646 |
| 12 | 96,249 | 0 | 91,675 |
| 18 | 68,308 | 4 (months 14-17, before the merge) | 86,198 |
| 24 | 52,011 | 22 (months 14-35) | 81,190 |
| never | n/a | every month from 14 on (47 months to 60) | 35,783 (still sinking toward 35,637) |

A merge at month 24 still ends in a profitable world, eventually. But it spends almost two years losing money first. In the real world, a publisher looking at 22 months of losses does not wait for the curve to turn. It announces a closure date. The designer's lever (shard count) worked. It was pulled too late for the business to see the result.

Open the interactive now. The left panel shows total players over 60 months, with the break-even line. At 40 shards the total curve bends gently and looks survivable for a year. The right panel shows players per shard against `H`, and it falls through the half-social line much sooner. Press the merge button at different months and watch the right panel jump while the left panel barely moves at first. Players feel the right panel. Accountants see the left one.

### Cross-game recognition

The model has one design knob that real games have turned many times: `S`, the number of places the population is divided into. Rewrite each case as "what did they do to `S`?"

**World of Warcraft, patch 5.4 (September 2013 onward).** Connected realms merge the databases of two or more realms so their players share guilds, trading and one auction house. The first US connections went live on 25 September 2013. In our terms, Blizzard lowered `S` for low-population realms without asking players to move. The stated goal, more chances to group and compete, is the `H / (H + d)` term in plain words.

**EverQuest (Sony Online Entertainment era).** EverQuest has merged servers repeatedly over its life. In Europe, Kane Bayle was merged into Antonius Bayle, and three promotional servers were later folded into Antonius Bayle as well. Each merge is a step down in `S`. EverQuest is still running under Daybreak Game Company, with expansions announced in 2024 and 2025. A world that manages `S` can outlive its peak by decades.

**Guild Wars 2 (megaserver system, completed 21 April 2014).** ArenaNet removed the fixed link between players and a home server for most open-world maps. When you enter a map, the game places you in a copy chosen by rules that consider your party, guild, language and home world. In our terms, `S` is no longer a number the launch team picks once. The game creates as many copies of each map as demand needs, so `d` stays near a target at every hour.

**EVE Online (Tranquility server).** EVE is the limiting case, `S = 1` for the whole player base. Its record of 65,303 accounts logged in at once (5 May 2013) was on a single server. Week 6 looks at the engineering cost of that choice. For this week, notice that a single shard makes the spiral much harder to start, because no player is ever stranded on the quiet copy of the world.

Four games, four mechanisms, one idea. Players experience density, not totals. When you read about any MMO's population trouble, ask how the players were divided and whether the division changed.

### Eyes-open design judgment

Fewer shards is not always better. Each lever has costs.

- **Merging breaks identity.** Players attach to server names, rival guilds and their own spot in a player-run market. A merge can create name clashes, flood a market with a second economy's gold, and turn two stable political scenes into one unstable one. Plan the merge like a content release, with a date, name-conflict rules and economy checks. MMO304 covers what happens when two money supplies meet.
- **Dynamic copies weaken place.** A megaserver keeps maps busy, but the stranger you helped today may never be in your copy again. Recognition over time, the thing that turns strangers into a community, needs stable groupings. That is why Guild Wars 2's rules try to keep guilds and parties together.
- **Launch shard counts are a guess.** Teams add shards for the launch crowd, then face exactly the table above a few months later. A design that can add and remove copies cheaply (instancing, connected databases, cross-server grouping) is insurance against your own launch success.
- **The model's parameters are unknown.** You will never know `H` for your game in advance. You can estimate it from telemetry by comparing churn on busy and quiet shards, which is what live-ops analytics (MMO308) is for. Decide in advance which density number triggers a merge, so the decision does not wait for a crisis.

## 3. Lessons from the case files

The spiral model explains one family of deaths. The other families teach different lessons. Take each case in turn and ask what a designer could have changed.

### Star Wars Galaxies: redesigning away your players

Star Wars Galaxies launched in North America in June 2003 as a sandbox with a deep crafting and profession system. In 2005 it went through two large redesigns. The Combat Upgrade arrived in May 2005, and subscription cancellations rose after it. The New Game Enhancements (usually called the NGE) followed in November 2005 and cut the profession system down to a small set of fixed roles. Contemporary reviews criticised the loss of depth and complexity.

The servers closed six years later, on 15 December 2011, by agreement between SOE and LucasArts. You cannot draw a straight line from the NGE to the closure, and you should not. What you can say is this. A redesign that replaces the thing your existing players came for is a bet that new arrivals will outnumber departures. In the model's language, it raised `c0` for the current population in the hope of raising `A`. If `A` does not rise enough, the resting population falls.

The coda matters too. In 2004, before the redesigns, fans founded SWGEmu to recreate the pre-Combat Upgrade version of the game from scratch. Players did not only miss the world. They missed a specific version of its rules, and they spent years rebuilding it.

### City of Heroes: closed with a community still inside

City of Heroes launched in North America on 28 April 2004 and closed on 30 November 2012, three months after NCSoft closed its developer, Paragon Studios. The stated reason was a company realignment. Players organised, petitioned and gathered in game for farewells. None of it changed the date.

What happened next is why the case is taught. A private server built from the game's code had been running quietly for years. It became public in April 2019, the code spread, and several fan-run servers appeared. On 4 January 2024, NCSoft granted one of them, Homecoming Servers LLC, an official licence to host the game.

Two lessons. First, a world's community can outlive its operator, and a publisher can later decide to work with it. Second, the legal path to that outcome ran through years of unlicensed servers. A designer who plans a sunset can offer a cleaner path from the start: server software released on closure, or a licence for community hosting.

### Tabula Rasa: an ending as content

Tabula Rasa launched in November 2007 and lasted about sixteen months. The team announced the closure on 21 November 2008, citing lower than expected population. From 10 January 2009 the game was free to play until the servers closed on 28 February 2009. The day before, the official site asked players to join a final assault, which ended with the mutual destruction of the two sides.

Star Wars Galaxies did something similar in its last week, with a final player-versus-player battle between the two factions. These events do not save a world. They change how its players remember the end. A world that ends mid-sentence, with a login error, leaves players with nothing to point at. A world that ends with a story beat gives them a last shared memory.

### The Matrix Online: the end kept outside the world

The Matrix Online closed on 31 July 2009 with fewer than 500 active players reported. Its story never got an in-game conclusion. Instead, the official website posted a memory book with story summaries after the servers went down. That is a cheap and respectable ending when the population is too small for a live event. Notice the order, though. Players who were logged in on the last day got no ending in the place they had spent their time.

### WildStar: when the studio goes first

WildStar launched on 3 June 2014 with a subscription and switched to free-to-play on 29 September 2015. On 6 September 2018, NCSoft closed Carbine Studios immediately and said it would begin winding the game down. The shutdown date of 28 November 2018 came later. Once the team that knows the code is gone, every option (a final event, a merge, a server-software release) becomes harder. Sunset plans have to be written while the team still exists.

## 4. Designing the ending

A world that will close someday should have an ending designed while it is healthy. This is not pessimism. Buildings have fire exits, and nobody calls the architect gloomy.

A sunset plan answers five questions.

1. **Trigger.** What measured condition starts the sunset? A players-per-shard floor, a revenue line, a licence date. Write it down with a number.
2. **Notice period.** How long between the announcement and the last day? The cases above range from under two months (The Matrix Online, announced in June for 31 July) through about twelve weeks (WildStar) and thirteen weeks (City of Heroes) to nearly six months (Star Wars Galaxies). Longer notice lets players say goodbye and export what they can.
3. **Final content.** Is there a last event, a story conclusion, or a memory book? Who will build it if the studio is already closed?
4. **What players keep.** Character data exports, screenshots of their houses, guild rosters, chat logs. Even a static web page of character sheets gives people something to keep.
5. **Preservation.** Will the server software, a single-player mode, or a community hosting licence be released? What legal and licensing work does that need, and who signs it off?

There is now public pressure on the fifth question. The Stop Killing Games campaign, started in 2024 by the YouTuber Ross Scott after Ubisoft switched off The Crew, ran a European Citizens' Initiative asking for games to stay playable after support ends. It closed on 31 July 2025, and verification in January 2026 confirmed 1,294,188 valid signatures. On 16 June 2026 the European Commission replied that it would not propose a legal obligation to keep games playable. It said it would work with stakeholders toward industry standards and a voluntary code of conduct instead. For a designer, the practical reading is simple. Nothing requires an end-of-life plan today, and players and regulators are watching whether studios make one anyway.

Persistence was the subject of week 12. A sunset plan is the last persistence decision. It asks what should last after the world itself stops.

## In-class activity (25 minutes)

Groups of three. Each group gets one case from section 3 (City of Heroes, Star Wars Galaxies, Tabula Rasa or WildStar).

1. (5 min) Name the main cause and up to two contributing causes, using the four families in section 1. For each, write one piece of evidence and its source.
2. (10 min) Set up the interactive to tell your case's story as well as the model can. Choose `S`, `A` and a merge month (or none). Write down the parameter values and the month the world first falls below break-even. If your case's main cause is not population, say which part of the story the model cannot show.
3. (10 min) Write a five-line sunset plan for your world as if you were the lead designer one year before its closure, answering the five questions in section 4.

Expected output: a half-page sheet with the cause analysis, the parameters and one screenshot from the interactive, and the five-line plan. Two groups present; the class checks each other's evidence.

## Common misconceptions

- **"Worlds close because nobody plays them."** Some do. City of Heroes and Star Wars Galaxies closed with active communities and petitions. Always ask who made the decision and what they compared the world against.
- **"More servers means more capacity, so more servers is safer."** At launch, maybe. After the launch crowd leaves, extra shards spread players thin, raise churn and raise per-shard cost at once. In the model, 40 shards rest at a fifth of the one-shard population.
- **"Total subscribers tell you whether a world feels alive."** Players meet the people on their shard, in their zone, at their hour. The same total can feel busy or empty depending on how it is divided.
- **"Once the servers are off, the world is gone."** SWGEmu and City of Heroes Homecoming show that communities can rebuild or rehost a world. A sunset plan decides whether that happens legally and easily or illegally and slowly.

## Check yourself

1. A world has 60,000 players on 20 shards, with the lecture's parameters (`c0 = 0.03`, `c1 = 0.20`, `H = 2,000`, `A = 6,000`). Compute this month's churn rate and next month's population.
2. Using the same world, what is the break-even population with `p = $15`, `F = $900,000` and `k = $10,000` per shard? Is the world profitable this month? What happens to the break-even if it merges to 10 shards?
3. At rest, `N × c = A`. Show that if `c1 = 0` (emptiness does not matter), the resting population no longer depends on `S`. What is it?
4. A publisher cites "realignment of company focus" for a closure. Which of the four families does this belong to, and what evidence would you look for to test whether a spiral contributed?
5. Your team is launching with 30 shards. Write the merge trigger you would put in the design document, as a rule with a number, and justify the number with the model.

<details>
<summary>Answers</summary>

1. `d = 60,000 / 20 = 3,000`. `H / (H + d) = 2,000 / 5,000 = 0.4`. `c = 0.03 + 0.20 × 0.4 = 0.11`. Players lost `= 6,600`. Next month `N = 60,000 − 6,600 + 6,000 = 59,400`.
2. `N_be = (900,000 + 10,000 × 20) / 15 = 73,333`. With 60,000 players, revenue is $900,000 against $1,100,000 cost, so it loses $200,000 this month. At 10 shards, `N_be = 1,000,000 / 15 = 66,667`, still above 60,000, but density doubles to 6,000 per shard, churn falls to `0.03 + 0.20 × 0.25 = 0.08`, and the resting population rises toward 90,746, above break-even.
3. With `c1 = 0`, `c = c0` for every `S`, so `N* = A / c0 = 6,000 / 0.03 = 200,000` regardless of shard count. The number of shards only matters because emptiness raises churn.
4. A business decision. Evidence of a contributing spiral would be falling players per shard, rising churn, recent merges or server closures, a switch to free-to-play, and statements that name population. Evidence against would be stable or growing numbers and petitions or protests from a large active community.
5. One reasonable answer: "Merge when median players per shard stays below `H` for four consecutive weeks." With the lecture's `H = 2,000`, churn in a shard at `d = H` is already 13%, well above the 6.6% of a healthy 10-shard world, and the merge table shows that acting before the world falls below break-even avoids months of losses. A good answer states `H` as an estimate from telemetry and says how it will be measured.

</details>

## Lab / assignment hook

[Lab 13, sunset simulation and closure post-mortem](../labs/lab13.md). You run the density-churn model in the starter script, fit it to one real shutdown's public timeline, and write a 600-word post-mortem with a sunset plan. The post-mortem counts toward the case-studies assessment (40%).

## Sources

- Wikipedia, "City of Heroes" (closure and later history sections, accessed September 2026). North American launch 28 April 2004; closure announced 31 August 2012, servers off 30 November 2012; "realignment of company focus and publishing support" as the stated reason; private server revealed April 2019; official licence to Homecoming Servers LLC on 4 January 2024.
- Wikipedia, "Paragon Studios" (accessed September 2026). Studio liquidated 31 August 2012; more than 21,000 players signed a petition against the closure.
- Wikipedia, "Star Wars Galaxies" (accessed September 2026). North American launch 26 June 2003; Combat Upgrade May 2005 and rising cancellations; NGE November 2005; closure announced 24 June 2011; servers off 15 December 2011; final PvP event; SWGEmu founded 2004.
- Wikipedia, "Tabula Rasa (video game)" (accessed September 2026). Launch November 2007; closure announced 21 November 2008 citing lower than expected population; free play from 10 January 2009; final assault event 27 February 2009; closure 28 February 2009.
- Wikipedia, "The Matrix Online" (accessed September 2026). Launch March 2005; closure 31 July 2009; fewer than 500 active players; post-closure memory book.
- Wikipedia, "WildStar (video game)" (accessed September 2026). Launch 3 June 2014; free-to-play 29 September 2015; studio closure 6 September 2018; shutdown 28 November 2018.
- Wikipedia, "EverQuest" (accessed September 2026). European server merges into Antonius Bayle; Al'Kabor closed November 2013; operated by Daybreak Game Company; expansions in December 2024 and December 2025.
- Warcraft Wiki, "Connected realms" (accessed September 2026). Introduced in patch 5.4 (September 2013); first US connections 25 September 2013; stated goal for low-population realms; shared guilds, trading and auction house.
- Guild Wars 2 Wiki, "Megaserver" (accessed September 2026). System completed 21 April 2014 after the 15 April 2014 update; placement rules use party, guild, language and home world.
- Wikipedia, "EVE Online" (accessed September 2026). Record of 65,303 concurrent accounts on 5 May 2013; single-universe design on the Tranquility cluster.
- Wikipedia, "Stop Killing Games" (accessed September 2026). Founded by Ross Scott in 2024 after The Crew's shutdown; ECI closed 31 July 2025; 1,294,188 valid signatures confirmed 26 January 2026; Commission response 16 June 2026. The European Citizens' Initiative register, ECI(2024)000007 "Stop Destroying Videogames" (register.eci.ec.europa.eu, checked September 2026), lists the initiative as answered on 16 June 2026.
- Bartle, R. (2003). *Designing Virtual Worlds*. New Riders. Chapter 3, "Churn, Sink, and Drift" (pp. 300-302): churn as the rate people leave a community, and most churn happening in a newbie's first days.
- The density-churn model, its parameters and all population and money figures in section 2 are invented for teaching and do not describe any real game.

## Interactive spec: examples/w13-shard-spiral.html

**The one insight.** Total population and players per shard tell different stories. At high shard counts the total curve looks survivable while the per-shard curve has already dropped through the half-social line, and merging changes the per-shard picture instantly while the total and the money respond slowly.

**Layout.** Two linked line charts side by side on desktop, stacked on mobile.

- Left, "Total players and break-even." x-axis month 0-60. y-axis players 0-220,000. Line: `N_t`. Dashed horizontal step line: `N_be(t) = (F + k × S_t) / p` (it steps down at the merge month). Shade months where `N_t < N_be(t)` in the palette's warning tint. Label the first month below break-even.
- Right, "Players per shard." Same x-axis. y-axis 0-12,000 (clip higher values and mark the clip). Line: `d_t = N_t / S_t`. Dashed horizontal line at `H`, labelled "half-social density." A vertical marker at the merge month on both charts.

**Model (monthly, t = 0..60).**
```
S_t = S_start if (merge is off or t < m) else S_after
d_t = N_t / S_t
c_t = c0 + c1 × H / (H + d_t)
N_{t+1} = N_t × (1 − c_t) + A
N_be(t) = (F + k × S_t) / p
```

**Controls.**
- Starting shards `S_start`, slider 1-60, default 40.
- Arrivals per month `A`, slider 0-20,000 step 500, default 6,000.
- Merge toggle (default off), merge month `m` slider 1-48 default 12, shards after merge `S_after` slider 1-60 default 10.
- "Advanced" disclosure with `c0` (0-0.10, default 0.03), `c1` (0-0.40, default 0.20), `H` (100-10,000, default 2,000), `p` (default 15), `F` (default 900,000), `k` (default 10,000), `N_0` (default 200,000).
- Buttons for presets: "Launch plan (40 shards, no merge)", "Merge early (month 6 to 10)", "Merge late (month 24 to 10)".

**Readouts beside the charts.** Current month under a hover or keyboard cursor with `N`, `d`, churn %, revenue, cost, profit. Summary: resting population `N*` for the final shard count (solve `N × c(N/S) = A` by bisection on [0, 10^7]), months below break-even (count over 0-60), first month below break-even.

**Test values (defaults unless stated).**
- No merge, S = 40: month 1 `N = 188,571`, month 3 `N = 167,317`, month 6 `N = 139,306`, month 12 `N = 96,249`; first month below break-even is 14 with `N = 85,407`; `N_be = 86,667`; 47 months below break-even in 0-60; `N_60 ≈ 35,783`; resting `N* = 35,637`.
- Merge at 6 to 10: zero months below break-even; `N_60 ≈ 97,646`; resting `N* = 90,746`; `N_be = 66,667` after the merge.
- Merge at 24 to 10: 22 months below break-even (14-35 in the full run to month 120; in the 0-60 window also 22); `N_60 ≈ 81,190`.
- Resting populations: S = 20 gives 50,803; S = 5 gives 137,843; S = 1 gives 186,808.

**Accessibility and style.** Keyboard cursor moves month by month on both charts together. Shared palette tokens from `templates/interactive-tokens.css`. No game art or logos. State on screen that all parameters are invented for teaching.

# MMO302 · Week 02 — Shards, realms, zones, instances, layers

**Why this matters:** Week 1 showed that a crowd costs the square of its size. Every MMO answers that with some mix of five tools: shards, zones, instances, layers and phases. Players use these words loosely and so do many developers. Each tool splits either the map or the population, and each split has a price that players pay in queues, empty streets or lost friends. This week you learn to name the split, compute its price, and choose on purpose.

**You will be able to:**
- Classify a game's world structure by what it copies (the population) and what it partitions (the map), using the five terms consistently.
- Compute, for a crowded zone split into `L` layers, the quest completion time under spawn contention, the number of players each person can meet, and the server cost, and find the `L` that balances them.
- Compute how many layers a launch-day zone needs as its population falls, and compare a policy that retires layers at restart with one that retires them on demand.
- Critique a real game's split (WoW Classic layering, Guild Wars 2 megaservers, WoW cross-realm zones, EVE's single shard) in terms of the same model.

**Before class:** Warcraft Wiki, "Layering" and "Cross-realm zones" (read both in full, they are short). Guild Wars 2 Wiki, "Megaserver". Reread MMO301 week 6 on what a single shard changes for players.

**Prerequisites from earlier courses:** [MMO302 week 1](w01-scale-targets-ccu-messages-and-n-squared.md) (deliveries `D = u × Σ g(g − 1)`, the crowd ceiling). [MMO301 week 6, EVE Online as a single shard](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w06-eve-online-the-single-shard-sandbox.md) (why one world matters socially). [MMO301 week 5, World of Warcraft](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w05-world-of-warcraft-accessibility-and-the-themepark.md) (instances as a design tool). [MA102 week 2, independent events](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w02-independent-events-and-the-gamblers-fallacy.md) (multiplying probabilities for friends landing together).

**Interactive:** [examples/w02-layer-split.html](../examples/w02-layer-split.html). Keep it open during section 2.

---

## 1. Two ways to cut a world

There are only two ways to make a crowd smaller. You can **copy** the world and put some players in each copy. Or you can **partition** the world, cutting the map into pieces that different server processes run. Copies divide the population, so players in different copies cannot meet. Partitions divide the map, so players can meet anywhere but the servers must pass them from piece to piece.

Every term players use is one of these two cuts, applied at some scale.

| Term | Cut | What is copied or split | Who chooses | Can players cross? | Example |
|---|---|---|---|---|---|
| **Shard** or **realm** | Copy | The whole world, with its own characters, economy and history | The player, at character creation | Only by transfer, often paid | World of Warcraft realms. EVE's Serenity server for China, separate from Tranquility |
| **Zone** | Partition | A region of the map, run by one server process | The map designer | Yes, by walking or a loading screen | A continent's regions on different machines. EVE's star systems on nodes |
| **Instance** | Copy | A small area (a dungeon, a raid, a house), one copy per group | The group, by entering | No. Each group has its own | WoW dungeons and raids |
| **Layer** or **megaserver copy** | Copy | Open-world zones, copied on demand | The server | Yes, by joining a party | WoW Classic layers (2019). Guild Wars 2 megaserver map copies (2014) |
| **Phase** | Neither | A player's view of world state, by story progress | The quest script | Not a capacity tool | WoW phasing. Warcraft Wiki warns that it is often confused with sharding |

Two words need care. **Shard** means a full copy of the world in most MMO writing, and that is how this course uses it. Blizzard also uses "sharding" for the dynamic zone copies that later became layers. When you read a source, check which one it means. **Phasing** changes what a player sees (the village burned or not) and has nothing to do with load.

The table has a pattern. The larger the thing you copy, the more community you split. A shard splits everything forever. An instance splits five people for half an hour. A layer sits in between. It splits the open world, but only for a while and only for players who are not grouped.

Partitions keep the community whole but move the cost to engineering. When a player walks from one zone server to another, the two servers must hand the player over without losing or duplicating them. That is week 4. When a crowd gathers in one partition, the partition cannot help, because the whole crowd is in one piece. That is why partitioned worlds such as EVE still need week 1's other lever, slowing time.

## 2. Worked example: launch day in the starting zone

### The hook

World of Warcraft Classic launched on 26 August 2019, a recreation of the game as it stood in patch 1.12.1 in 2006. On launch day every character on a realm was level 1, so each realm's whole population started in the same few zones at the same time. Blizzard's answer was **layering**. The Warcraft Wiki describes each layer as a copy of the outdoor world with its own NPCs, its own rare spawns and its own herbs and ore. Players only see players in their own layer. Joining a party with someone on another layer moves you to theirs. And layering was temporary. Blizzard said it would merge each realm's layers before content Phase 2, and by 13 November 2019 every realm was down to a single layer.

Why build a whole system only to switch it off after 11 weeks? Because layers solve one problem and create another, and the balance between them changes as the launch crowd spreads out.

### The model

One zone has `Z` players at the peak. The server splits them evenly over `L` layers, so each layer has `Z / L`.

**Contention.** Quests ask players to kill monsters that respawn on a timer. A fraction `f` of the zone's players are on the same kill quest at once. The zone has `S` spawn points for the quest monster, each respawning `R` seconds after a kill. Each player could kill `q` monsters per minute if nobody else were competing, and needs `k` kills.

```
kill supply per layer   = S × 60 / R                  (kills per minute)
demand per layer        = f × (Z / L) × q             (kills per minute)
each player's kill rate = min(q, supply / (f × Z / L))
quest time              = k / kill rate               (minutes)
```

When demand is below supply, everyone kills at their own pace `q`. Above it, the supply is shared, and each player gets a fraction of it.

**Community.** A player can meet the other players on their layer, `Z / L − 1` of them. A friend who logs in without grouping lands on the same layer with probability `1 / L`. A group of five friends who log in separately all land together with probability `(1 / L)^4`, because each of the other four independently matches the first.

**Server cost.** From week 1, if a layer's zone were one group, its deliveries are `u × (Z / L) × (Z / L − 1)`. Over `L` layers that totals about `u × Z² / L`. Each layer also needs its own copy of the zone's NPCs and objects, so it costs a base amount of memory and CPU even when nearly empty.

### Numbers you can check

Use invented but plausible numbers. `Z = 3,000` players in the starting zone. `f = 10%` of them, so 300, are on the same boar-hunting quest. `S = 30` spawn points, `R = 60` s respawn, `q = 2` kills per minute uncontested, `k = 10` kills. Supply per layer is `30 × 60 / 60 = 30` kills per minute. Updates per player `u = 5`.

| Layers `L` | Players per layer | Quest time (min) | Players you can meet | Chance an ungrouped friend is with you | Chance a 5-friend group lands together | Deliveries/s, all layers |
|---|---|---|---|---|---|---|
| 1 | 3,000 | 100 | 2,999 | 100% | 100% | 44,985,000 |
| 2 | 1,500 | 50 | 1,499 | 50% | 6.25% | 22,485,000 |
| 4 | 750 | 25 | 749 | 25% | 0.39% | 11,235,000 |
| 5 | 600 | 20 | 599 | 20% | 0.16% | 8,985,000 |
| 10 | 300 | 10 | 299 | 10% | 0.01% | 4,485,000 |
| 20 | 150 | 5 | 149 | 5% | 0.0006% | 2,235,000 |
| 30 | 100 | 5 | 99 | 3.3% | 0.0001% | 1,485,000 |

Check the `L = 4` row by hand. Each layer has 750 players, 10% of them are questing, so 75 share 30 kills a minute. Each gets `30 / 75 = 0.4` kills a minute, and 10 kills take 25 minutes. The friend chance is `1/4`. The group chance is `(1/4)^4 = 1/256 ≈ 0.39%`. Deliveries are `4 × 5 × 750 × 749 = 11,235,000`.

Three things stand out.

- **Contention falls in proportion to `L` until it hits the floor.** At `L = 20`, demand per layer equals supply and every player kills at their own pace. More layers after that buy nothing. Quest time at `L = 30` is still 5 minutes.
- **Community falls in proportion to `L` from the first split.** There is no floor. Every layer you add shrinks the crowd each player sees.
- **The server's cost falls as `1 / L`**, exactly as week 1 predicted. Twenty layers cost a twentieth of one layer in deliveries.

So the model gives a clear target. Use the smallest `L` at which contention stops. Here that is `L = 20`, where supply equals demand. Any fewer and players wait for boars. Any more and you split the community for nothing.

The friend columns are why party-joining matters. Without it, a 5-friend group has one chance in 160,000 of landing together at `L = 20`. With it, the chance is 100%, because the game moves the group to the leader's layer. Party-joining turns the worst social cost of layering into a minor one, and WoW Classic had it from the start.

### The crowd moves on

The starting zone does not stay crowded. Players level up and leave. Say the zone's population halves every two days, `Z(d) = 3,000 × 0.5^((d − 1) / 2)` on day `d` of launch. The layers needed to keep contention at or below supply is `ceil(f × Z × q / supply) = ceil(Z / 150)`.

| Launch day | Players in zone | Layers needed | Players per layer, if layers follow demand | Players per layer, if the 20 layers stay |
|---|---|---|---|---|
| 1 | 3,000 | 20 | 150 | 150 |
| 3 | 1,500 | 10 | 150 | 75 |
| 5 | 750 | 5 | 150 | 37.5 |
| 7 | 375 | 3 | 125 | 18.75 |
| 9 | 188 | 2 | 94 | 9.4 |
| 11 | 94 | 1 | 94 | 4.7 |

The last two columns are the design decision. If layers follow demand, every layer stays busy at about 150 players, then 125, then 94. If layers created on day 1 stay until someone retires them, by day 7 each of the 20 copies holds fewer than 19 people. The zone is a ghost town, twenty times over, and players who log in see an empty world even though 375 people are in it.

Retiring layers on demand sounds better. But retiring a layer means moving everyone on it to another copy of the world, mid-fight, mid-trade, mid-conversation. Players see enemies vanish and monsters reset. The cost of merging has to be weighed against the cost of emptiness.

### Move it yourself

Open `examples/w02-layer-split.html`. The left chart plots quest time against `L` from 1 to 40. The right chart plots players you can meet against the same `L`. A vertical line marks your chosen `L` in both. Drag `L` from 1 upward. The left curve falls steeply, then goes flat at `L = 20`. The right curve falls from the first step and never flattens. Now drag the day slider below the charts from 1 to 11. The layers-needed marker moves left as the crowd shrinks. Switch the policy toggle from "retire on demand" to "keep until restart" and watch the players-per-layer readout drop into single digits.

### The same idea in other games

**WoW Classic layering (2019) and Season of Discovery (2023 to 2024).** Blizzard's first policy for WoW Classic created layers on demand and did not collapse them until the realm restarted. That is our "keep" policy, bounded by the restart schedule. For Season of Discovery, launched 30 November 2023, Blizzard tried the other policy. The Warcraft Wiki reports that layers were collapsed dynamically in off-peak hours to push players together, and that this broke the Battle for Ashenvale world event, whose progress depended on a crowd staying put. Blizzard went back to retiring layers only at restarts. The model predicted both halves. Dynamic retirement fixes emptiness and costs stability.

**Guild Wars 2 megaserver (ArenaNet, April 2014).** Guild Wars 2 put all players of a region (North America, Europe, China) into shared copies of each map, creating a new copy when a map fills. That is layering with `L` chosen per map. What ArenaNet changed is the assignment. The Guild Wars 2 Wiki lists the heuristics used to place a player, including party, guild, language and home world. In our model this raises the "friend is with you" column above `1 / L`. The assignment function is a design lever as strong as `L` itself. In April 2023 ArenaNet added a queue for joining a full copy where your party is, which shows the other side of a capacity cap.

**WoW cross-realm zones (patch 5.0.4, 2012).** This is the model run backwards. Blizzard's problem was not too many players in a zone but too few, with low-level zones empty because most players were at the level cap. Cross-realm zones put players from several realms into the same copy of a zone. In our terms, `L` fell below 1 per realm. Several realms' zone populations were added together so `Z / L` rose to a lively number. A September 2012 hotfix limited the pooling to realms within three time zones, which recognises that players in different time zones do not overlap enough to meet.

**EVE Online (CCP, single shard).** EVE refuses copies. Tranquility runs one world for everyone outside China, split into nodes that host parts of space. That is `L = 1` forever and all the scaling done by partition. The model says EVE should suffer the worst contention and crowding, and it does. It answers with a huge map (thousands of star systems, so `Z` per system is usually small) and, when players gather anyway, with time dilation from week 1. EVE's players get a world where every encounter counts because nobody is ever in a different copy. MMO301 week 6 covers what that means for play.

**Dungeon instances.** An instance is the extreme of this model, one copy per group. For a 5-player dungeon, `L = Z / 5`. Contention is zero, and the players you can meet are your four companions. Games use instances exactly where contention would be intolerable (a boss that drops loot once) and meeting strangers adds nothing.

### Design judgment

- **Split only as far as contention requires.** The right `L` is the smallest one where supply meets demand. Past that point, every extra copy costs community and buys nothing. Compute it from spawn counts, respawn times and the share of players on each objective.
- **Always ship party-joining with any copy system.** Without it, the chance of friends meeting falls as `(1/L)` to the power of the group size minus one. With it, the social cost falls on strangers only.
- **Decide your retirement policy before launch.** Keeping layers until restart is stable and empties the world. Retiring on demand keeps the world full and breaks events and fights. Season of Discovery shows that you can pick wrong, and that players notice quickly.
- **Prefer raising supply to adding copies when you can.** If 300 players hunt 30 boars, a designer can double the spawn points or halve the respawn time and cut `L` in half. That keeps players together. The trade is that the world feels less scarce, and an economy built on scarce drops will inflate.
- **Remember what a copy costs to run.** Each layer carries its own NPCs, respawn timers and objects. Twenty layers of a mostly empty zone cost twenty times the base CPU and memory for the same 375 players.

### Check this example

1. With the same zone and quest, the designers double the spawn points to `S = 60`. How many layers are needed on day 1 now? What is the quest time at `L = 10`?
2. A group of three friends logs in separately to a zone with 8 layers and no party-joining. What is the chance they all land together?
3. On day 5, with the "keep 20 layers" policy, how many players can each person meet? With "retire on demand"?

<details>
<summary>Answers</summary>

1. Supply per layer is 60 kills per minute. Demand is `300 × 2 = 600` in total, so `L = 600 / 60 = 10` layers. At `L = 10`, 30 questers share 60 kills per minute, which is 2 each, the uncontested rate. Quest time is `10 / 2 = 5` minutes.
2. `(1/8)^2 = 1/64 ≈ 1.6%`.
3. With 20 layers, `750 / 20 = 37.5` per layer, so about 36 others. With 5 layers, 150 per layer, so 149 others.

</details>

## 3. Shards: the copy you cannot undo

A **shard** (or **realm**) is the biggest copy. Players choose one at character creation. Their characters, items, guild and reputation live there. A shard has its own database, and a shard's economy and politics develop apart from the others.

Sizing shards starts from week 1's numbers. If the whole game peaks at 60,000 PCU and one shard's hardware is planned for 4,000, you need 15 shards on day 1. The harder question is what happens over time. Shards do not shrink evenly. Players follow friends and guilds to the busiest shards, and the quiet ones empty out. Suppose you believe a shard needs at least 1,500 players online at the evening peak for its markets, groups and guilds to work. With 15 shards of 4,000 at launch, a 50% drop in total population leaves an average of 2,000 per shard. That average hides the spread. If the busiest five hold 3,000 each, the other ten average 1,500, right at your floor, and several are below it.

Then you must merge, and a merge is worse than a layer merge because shards carry permanent state. Two characters named the same. Two guilds with the same name. Two economies with different prices for the same item. Two histories of who conquered what. Games handle this with renames, transfers and connected realms. In September 2025 Blizzard offered free character transfers to consolidate its Mists of Pandaria Classic players onto regional "Mega Realms", citing the benefits of higher player concentration it had seen after earlier transfers. The model's lesson is the same as for layers. Split late, merge early, and plan the merge before launch.

A single shard avoids all of this and pays for it in engineering. EVE's architecture must survive every crowd players can gather in one world. Week 12 takes EVE's architecture apart in detail.

## 4. Choosing a structure

Put the options side by side with the question each one answers.

| Your problem | First choice | Why | Price |
|---|---|---|---|
| Too many players for one machine in total | Partition into zones (week 4) | Keeps one community | Handoff engineering, crowds still possible in one zone |
| A predictable crowd at launch or an event | Layers with party-joining | Divides `g` for a while, then merges | Community splits, merge disruption |
| Competition for a boss or a dungeon's loot | Instances | Removes contention entirely | Players meet only their group |
| Too few players in old content | Cross-realm pooling | Raises `Z / L` by merging copies | Players meet strangers they will never see again |
| Too many players for one world, forever | Shards | Hard limit on everything | Permanent social split, merges later |
| Players must share one world at any cost | Single shard plus partitions and time dilation | One history, one economy | The hardest engineering in the field |

Most successful MMOs use several at once. WoW uses realms, zones, instances and cross-realm zones together, and Classic added layers. The skill is to use each where its price is lowest.

## In-class activity (25 minutes)

Pairs. Your studio is launching a fantasy MMO. The design has one starting zone per faction and expects 6,000 players per faction in that zone on day 1. A key quest asks for 8 kills. Designers propose 40 spawn points with a 90 s respawn. Assume 15% of the zone's players are on that quest at once and each can kill 3 per minute uncontested.

1. Compute kill supply per layer and the layers needed on day 1.
2. Propose one design change to the quest (spawns, respawn, kills needed) that halves the layers needed. Show the numbers.
3. Choose a retirement policy and write the rule precisely (when is a layer retired, where do its players go).
4. Name one event in your game that your policy would break, and how you would protect it.

Expected output: the layer counts before and after your change, your retirement rule in two sentences, and the protected event.

## Common misconceptions

- **"Sharding and layering are the same thing."** A shard is a permanent copy with its own characters and economy. A layer is a temporary copy of open-world zones on one realm, and players move between layers by grouping.
- **"More layers is always safer."** Contention stops falling once supply meets demand, and community keeps falling. Past that point, each layer is pure cost.
- **"Phasing reduces server load."** Phasing changes what a player sees by quest progress. It can even raise load, because the server tracks several versions of the same place.
- **"A single-shard game has no crowding problems."** It has the worst ones, because a crowd can never be split into copies. It must be handled by partitioning, time dilation or design.

## Check yourself

1. A zone has 4,800 players at peak. 5% are on a kill quest needing 12 kills. There are 24 spawn points with a 120 s respawn, and players kill 2 per minute uncontested. How many layers are needed? What is the quest time with one layer?
2. A game uses 12 layers in a hub city. A guild of 6 logs in without grouping. What is the chance that all 6 land on the same layer? What does party-joining change?
3. Classify each as copy or partition: a raid instance, EVE's star systems, a WoW realm, a Guild Wars 2 map copy.
4. Using week 1's formula, by what factor do total deliveries fall when a 3,000-player zone is split into 6 layers? Why is the real saving smaller?

<details>
<summary>Answers</summary>

1. Supply per layer `= 24 × 60 / 120 = 12` kills per minute. Demand `= 0.05 × 4,800 × 2 = 480` kills per minute. Layers needed `= 480 / 12 = 40`. With one layer, 240 questers share 12 kills per minute, `0.05` each, so 12 kills take 240 minutes.
2. `(1/12)^5 = 1 / 248,832 ≈ 0.0004%`. Party-joining moves the whole group to the leader's layer, so the chance becomes 100% for anyone who groups.
3. Raid instance, copy. EVE's star systems, partition. WoW realm, copy. Guild Wars 2 map copy, copy.
4. `u × Z(Z − 1)` becomes `u × 6 × 500 × 499`. The ratio is `(3,000 × 2,999) / (6 × 500 × 499) = 6.01`, about 6. The real saving is smaller because each layer carries its own NPCs, timers and objects, and because the zone is rarely one single group in practice. Week 3's interest management already splits it.

</details>

## Lab / assignment hook

[Lab 02, layer assignment](../labs/lab02.md). You simulate 3,000 players, many in guilds, arriving at a zone with 20 layers. You implement a random assignment and a guild-aware one with a capacity cap, and measure the largest layer, the share of guildmates who share a layer, and quest contention. Deliverable: the finished `layers.py`, a comparison table, and a one-page layering policy for the in-class game.

## Sources

- Warcraft Wiki, "Layering" (accessed September 2026). Each layer a copy of the outdoor world with its own NPCs, rares and gathering nodes; players see only their layer; moving layers by joining a party; layers created with demand and collapsed only at realm restart; merge planned before Phase 2 and all realms on one layer from 13 November 2019; Season of Discovery's dynamic collapsing and its problems with the Battle for Ashenvale event, reverted to retirement at restarts. Warcraft Wiki cites Blizzard forum posts and Wowhead news (2019, December 2023).
- Wikipedia, "World of Warcraft Classic" (accessed September 2026). Release 26 August 2019 recreating patch 1.12.1; Season of Discovery launched 30 November 2023; free transfers to consolidate Mists of Pandaria Classic players onto Mega Realms in September 2025.
- Warcraft Wiki, "Cross-realm zones" (accessed September 2026). Added in patch 5.0.4 (2012) to fill low-level zones; hotfix of 20 September 2012 limiting pooling to realms within three time zones; group phasing rules.
- Guild Wars 2 Wiki, "Megaserver" (accessed September 2026). Region-wide map copies created when a map fills; placement heuristics including party, guild, language and home world; roll-out completed April 2014; map queue beta added in the 18 April 2023 update.
- EVE University Wiki, "Tranquility" (accessed September 2026), and Wikipedia, "Eve Online" (accessed September 2026). One persistent world split into nodes hosting parts of New Eden; Serenity as the separate Chinese server.

## Interactive spec: examples/w02-layer-split.html

**The one insight.** Adding layers cuts contention only until supply meets demand, and then it flattens. The number of players you can meet falls from the very first split and never flattens. The right number of layers is the knee of the first curve, and it moves as the launch crowd leaves.

**Model (exact).**
- Inputs with defaults and ranges: zone population on day 1 `Z0` (3,000; 500 to 10,000 step 100), share on the quest `f` (10%; 1% to 50%), spawn points `S` (30; 5 to 100), respawn `R` seconds (60; 10 to 300), uncontested kill rate `q` per minute (2; 0.5 to 5 step 0.5), kills needed `k` (10; 1 to 30), layers `L` (4; 1 to 40 integer), launch day `d` (1; 1 to 14 integer), halving time `h` days (2; 1 to 7), policy toggle "manual L", "retire on demand" or "keep until restart" (default manual L, so the first screen shows `L = 4`), group size `G` for the friends readout (5; 2 to 10), updates per player `u` (5, fixed).
- `Z(d) = Z0 × 0.5^((d − 1) / h)`.
- `supply = S × 60 / R` kills per minute per layer.
- `questers per layer = f × Z(d) / L`.
- `rate = min(q, supply / questers per layer)`; `quest time = k / rate` minutes.
- `meet = Z(d) / L − 1` (floor at 0).
- `friend = 1 / L`; `group = (1 / L)^(G − 1)`.
- `deliveries = u × L × (Z(d) / L) × (Z(d) / L − 1)`.
- `L_needed(d) = max(1, ceil(f × Z(d) × q / supply))`.
- Under "keep until restart", the layer count on day `d` is `L_needed(1)` (layers from day 1 persist). Under "retire on demand", it is `L_needed(d)`. The `L` slider is overridden by the policy when the policy toggle is active; show a "manual L" option to free it.

**Layout.** Two linked charts side by side (stacked below 700 px). Left: quest time (y, minutes, 0 to 110) against `L` (x, 1 to 40), a line with a marker at the current `L` and a dashed vertical line at `L_needed(d)`. Right: players you can meet (y, log scale) against the same `L`, with the same markers. Below the charts, a strip chart of `Z(d)` for days 1 to 14 with a marker on day `d`, and the layer count each policy gives that day. Readout row: `Z(d)`, `L` in use, players per layer, quest time, meet, friend %, group %, deliveries/s.

**First screen.** Day 1, manual `L = 4`, so both charts show the current marker well to the left of the knee at 20, with quest time 25 minutes and meet 749.

**Test values** (defaults, day 1):
- `L = 1`: quest 100 min, meet 2,999, deliveries 44,985,000.
- `L = 4`: quest 25 min, meet 749, friend 25%, group (G = 5) 0.39%, deliveries 11,235,000.
- `L = 10`: quest 10 min, meet 299, deliveries 4,485,000.
- `L = 20`: quest 5 min, meet 149, deliveries 2,235,000. `L_needed(1) = 20`.
- `L = 30`: quest 5 min, meet 99.
- Days with `h = 2`: `L_needed` is 20, 10, 5, 3, 2, 1 on days 1, 3, 5, 7, 9, 11; `Z` is 3,000, 1,500, 750, 375, 187.5, 93.75. Under "keep until restart" players per layer on day 7 is 18.75.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. All controls are native inputs with labels; charts have text summaries in an `aria-live` region. No game art; label the scenario "starting zone" generically.

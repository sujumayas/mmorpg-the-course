# MMO306 · Week 02 — Quest Hubs and Zone Pacing

**Why this matters:** A levelling zone is built in order, hub by hub, but players leave it the moment it stops paying. Anything that speeds up their levelling, from a dungeon queue to a bonus for logging out at an inn, quietly deletes the end of your zone for them. If you can compute how many quests a player actually does before moving on, you can decide where to spend a quest team's months instead of discovering after launch that a third of the zone is empty.

**You will be able to:**
- Compute a zone's XP demand, the number of quests a player needs to clear it, and its coverage ratio `c`.
- Predict how much of each hub a player sees when XP arrives from outside the quests, and identify the hub that is cut first.
- Compare fixed-level zones with level-scaled zones (World of Warcraft, The Elder Scrolls Online, Final Fantasy XIV, Guild Wars 2) and name what scaling changes in the model.
- Design a zone's hub layout and coverage target so that the content you author is the content players see.

**Before class:** Warcraft Wiki, "Zone scaling" and "Rest" (15 minutes together). UESP, "Online:One Tamriel" (5 minutes). Reread GD203 week 7, section 4, on designing an XP curve backwards from a play-time target.

**Prerequisites from earlier courses:** [GD203 week 7, XP curves](../../GD203-combat-and-progression-design/lectures/w07-xp-curves.md) gave you the XP table and income curves. This week reads them per zone. [GD203 week 8, power curves and level scaling](../../GD203-combat-and-progression-design/lectures/w08-power-curves-and-level-scaling.md) compared ways of scaling enemies to the player. We use its vocabulary and do not repeat its model. [GD202 week 6, quest anatomy](../../GD202-narrative-and-quest-design/lectures/w06-quest-anatomy-hook-objective-complication-reward.md) priced one quest against grinding and showed how quest XP decays when a player outlevels it. [GD202 week 8, quest chains and zone storytelling](../../GD202-narrative-and-quest-design/lectures/w08-quest-chains-and-zone-storytelling.md) measured a zone's trips, width and order control. [GD201 week 10, hubs, spokes and gating](../../GD201-level-and-world-design/lectures/w10-hubs-spokes-and-gating.md) computed errand costs and gate slack. This lecture assumes all three and adds the question they left open: how much of the zone does a player reach at all? From this course, [week 1](w01-the-content-treadmill-production-vs-consumption.md) gave you the production side.

**Interactive:** [`examples/w02-zone-xp-budget.html`](../examples/w02-zone-xp-budget.html). Keep it open during section 2.

---

## 1. Zones, hubs and the XP budget

A **levelling zone** is a region of the world built for characters in a level range, say 10 to 15. Its quests are grouped into **quest hubs**, small towns or camps with a cluster of quest givers, a place to rest and usually a flight point. Players work through a zone hub by hub. They finish most of the first hub's quests, follow a quest or a road to the second hub, and so on.

GD202 and GD201 looked at hubs and chains from the inside: the order of quests, the walk back to turn them in, the gates between spokes. This course looks at the zone from the production side. Every quest costs a writer, a designer, a scripter and a tester some days. A zone of 30 quests is several months of a small team. So a production question sits under all of the design questions. **Of the quests you build, how many will the average player do?**

In a zone with fixed levels, the answer comes from an XP budget. Three terms.

- **XP demand** `X` is the experience a character needs to cross the zone's level range. If the zone takes players from level 10 to 15, it is the sum of the XP-to-next-level values for levels 10 through 14. You built such tables in GD203 week 7.
- **XP supply** is what the zone's content hands out. Most of it comes from quests. Some comes from monsters killed along the way.
- **Outside XP** is experience from anywhere else while the player is nominally in the zone: dungeons, gathering, player-versus-player, bonuses.

When supply plus outside XP reaches the demand, the character reaches the top of the zone's range. The zone's monsters and quests turn low-level. GD202 week 6 showed that quest XP then shrinks with the level gap, so the player's best move is to leave for the next zone. Whatever quests remain are unplayed.

## 2. Worked example: the last hub dies first

### The hook

On 16 January 2018, World of Warcraft patch 7.3.5 brought **zone scaling** to every zone in Kalimdor, the Eastern Kingdoms, Outland, Northrend, Pandaria and Draenor. Monsters, quests and rewards in each zone now scale to the player's level across a range, as they already did in Legion's Broken Isles. The patch notes pitched it as a big increase in the options players have when deciding where to quest and when to move on to the next zone. Two and a half years later, patch 9.0.1 (October 2020) added Chromie Time, which lets a character level through any one earlier expansion's zones with everything scaled.

Rebuilding the maths of fourteen years of zones is a large engineering job. Why would a studio do it, rather than build more zones? Because in a fixed-level world, a player's experience rate decides how much of each zone they see, and faster levelling had been cutting whole hubs out of the player's path. You can see why with one line of arithmetic.

### The model

A zone spans a level range with XP demand `X`. It holds `N` quests, split into hubs that players do in order.

```
quests needed      n = X × (1 − o) / (q × (1 + k))
coverage ratio     c = N / n
share of zone seen = min(1, 1 / c)
```

- `X` is the zone's XP demand, summed from the XP table.
- `q` is the XP one quest pays to a character at the zone's level.
- `k` is the kill XP a player earns while doing one quest, as a share of `q`. If the monsters on the way give 100 XP for a 400 XP quest, `k = 0.25`.
- `o` is the share of `X` that arrives from outside the zone's quests: dungeons, gathering, and so on.
- `n` is how many quests the player does before they outlevel the zone.
- `c` is how many quests you built for each one they need. It is GD201's gate slack, `available / required`, measured in XP instead of tokens.

Hubs come in order, so the player fills them front to back. With hubs of sizes `s₁, s₂, …`, the player finishes all of hub 1 if `n ≥ s₁`, then puts what's left of `n` into hub 2, and so on. The last hub gets whatever remains, which may be nothing.

The model assumes the player does quests in hub order and does every quest they meet. Real players skip some, and section 3 adds that.

### Numbers you can check

An invented zone for levels 10 to 15:

| Level | XP to next level |
|---|---|
| 10 | 2,000 |
| 11 | 2,200 |
| 12 | 2,400 |
| 13 | 2,600 |
| 14 | 2,800 |
| **Zone demand `X`** | **12,000** |

Each quest pays `q = 400` XP, and the kills along the way add a quarter of that (`k = 0.25`), so a quest is worth 500 XP in total. The team builds `N = 30` quests in three hubs of 10.

Now four players.

| Player | `k` | `o` | Quests needed `n` | Coverage `c` | Hub 1 seen | Hub 2 seen | Hub 3 seen |
|---|---|---|---|---|---|---|---|
| Solo quester | 0.25 | 0 | 24.0 | 1.25 | 100% | 100% | 40% |
| Arrives fully rested | 0.50 | 0 | 20.0 | 1.50 | 100% | 100% | 0% |
| Some dungeons | 0.25 | 0.2 | 19.2 | 1.56 | 100% | 92% | 0% |
| Dungeon heavy | 0.25 | 0.5 | 12.0 | 2.50 | 100% | 20% | 0% |

Check the first row by hand. `n = 12,000 / 500 = 24`. Hubs 1 and 2 take 20 of those quests. The last 4 fall in hub 3, which is 40% of it. For this player the team built 6 quests too many, and all 6 are in hub 3.

The second row uses a real World of Warcraft mechanic. A **rested** character earns double experience from kills, but the bonus does not apply to quest XP, per the Warcraft Wiki. Rest builds up while the character is logged out, about 5% of a level for every 8 hours in an inn or city, up to 150% of a level. So a player who logs in twice a week often arrives rested. Their kill XP doubles, `k` goes from 0.25 to 0.5, each quest is worth 600 XP, and they need only 20 quests. They leave the zone the moment they finish hub 2. The feature that exists to help part-time players catch up also means they never see hub 3.

Rows 3 and 4 add a dungeon queue. With one fifth of the XP from dungeons, hub 3 is gone and hub 2 is nearly done. With half, the player leaves after two quests of hub 2.

Read down the "Hub 3" column. **The last hub is the first to die.** Every source of XP outside the quests is paid for entirely out of the end of the zone. The team spent a third of its budget on hub 3, and only the slowest player in the table sees any of it.

Here is the table from code:

```python
XP_TO_NEXT = {10: 2000, 11: 2200, 12: 2400, 13: 2600, 14: 2800}   # zone runs 10 -> 15
HUBS = [10, 10, 10]                                              # quests per hub, in order
Q = 400                                                          # quest XP at zone level

def quests_needed(X, q, k, o):
    return X * (1 - o) / (q * (1 + k))

def hub_seen(n_done, hubs):
    seen, left = [], n_done
    for size in hubs:
        seen.append(min(size, max(0, left)) / size)
        left -= size
    return seen

X = sum(XP_TO_NEXT.values())
for label, k, o in (("solo", 0.25, 0), ("rested", 0.5, 0),
                    ("some dungeons", 0.25, 0.2), ("dungeon heavy", 0.25, 0.5)):
    n = quests_needed(X, Q, k, o)
    c = sum(HUBS) / n
    hubs = " ".join(f"{s:4.0%}" for s in hub_seen(n, HUBS))
    print(f"{label:14s} need {n:4.1f}  c={c:.2f}  hubs {hubs}")
```

It prints:

```
solo           need 24.0  c=1.25  hubs 100% 100%  40%
rested         need 20.0  c=1.50  hubs 100% 100%   0%
some dungeons  need 19.2  c=1.56  hubs 100%  92%   0%
dungeon heavy  need 12.0  c=2.50  hubs 100%  20%   0%
```

### A visual you can move

Open the interactive. The left view is the zone as the player walks it: 30 quest markers in three coloured hub bands, left to right, with an XP bar filling along them. A vertical "outlevelled" line marks the quest at which the bar reaches `X`. Quests to the right of it are greyed out.

The right view is the production side. It shows three columns, one per hub, each as tall as the team's cost for that hub (equal here), filled to the share of it the player sees. The unfilled part is labelled "built, not played".

Drag the outside-XP slider `o` from 0 to 0.5. The line on the left slides toward the start, and on the right the third column empties first, then the second. Now tick "zone scaling". The line disappears, every quest pays full XP regardless of level, and all three columns fill. The player's level at the end of the zone now reads above 15. Section 4 discusses that trade.

### Cross-game recognition

Each of these games changed one term of the model, and each change has a cost.

**World of Warcraft, zone scaling (Legion onward, all older continents from patch 7.3.5, January 2018).** Scaled zones pay quest XP at the player's current level within the zone's range, so the "outlevelled" line moves to the top of that range, well past the level where the old fixed zone used to end. `c` stops deciding what players see, because the zone keeps paying. Chromie Time (patch 9.0.1, October 2020) went further. A player picks one earlier expansion and levels through all of its zones, scaled, until the level at which the campaign ends. Several expansions' worth of zones now compete for the same level range, and each player sees mostly one.

**The Elder Scrolls Online, One Tamriel (Update 12, October 2016).** ZeniMax applied its battle-levelling system to every zone and removed most alliance restrictions, so players of any level could quest anywhere and be scaled to the zone's content. Rewards stay appropriate to the character's real level. In model terms, `c` became irrelevant everywhere at once. The zone's story, not its XP, decides when the player is done.

**Final Fantasy XIV (FATEs, A Realm Reborn onward).** FATEs, the game's open-world events, use level sync. A player more than five levels above a FATE's level can't take part until they sync down. The game scales the player down rather than the content up. Old zones stay fixed-level, with their XP budgets intact, but high-level players can still join low-level players there.

**Guild Wars 2 (2012 onward).** A character in a lower-level area is scaled down to that area's maximum level plus one, as GD201 week 10 described. Like FFXIV, it scales the player down to keep old content challenging, which keeps high-level players in low zones alongside newcomers.

Four games, two directions. Scaling content up (WoW, ESO) removes the XP budget as a constraint, so players see more of every zone. Scaling players down (FFXIV, GW2) keeps the budget and keeps old zones populated. Neither is free, and section 4 is about the price.

### Eyes-open design judgment

- **Author to a coverage target, not to a level range.** A zone with `c = 1.0` for your slowest intended player gives every player a wall of quests with no slack. A zone with `c = 2.5` for your typical player wastes 60% of it. A target of about 1.2 to 1.5 for the typical player lets players skip quests they dislike (GD201's slack argument) without building hubs nobody sees. Pick the target for the player who uses the most outside XP you intend to support.
- **Put the zone's story climax where players still are.** If hub 3 carries the zone's resolution (the finale of GD202 week 8's spine), most players will never see it. Either move the climax into hub 2 or make hub 3 a destination players go to for other reasons, such as a dungeon entrance.
- **Every outside XP source is a design decision about zone endings.** Adding a dungeon queue, a rested bonus or an XP potion removes the end of every fixed-level zone for the players who use it. That may be fine, but decide it on purpose, with this table in front of you.
- **Scaling fixes the budget and breaks the sense of growth.** In a scaled zone, the monsters that were hard at level 10 are just as hard at level 20. GD203 week 8 called this the flattening of the power curve. Players lose the moment of returning to an old zone and crushing it.

### Check yourself (worked example)

1. The same zone adds a fourth hub of 8 quests. What coverage does the solo quester have now, and how much of hub 4 do they see?
2. A designer wants the "some dungeons" player (`o = 0.2`) to finish hub 3 exactly. What must `q` be, keeping `k = 0.25`?

<details>
<summary>Answers</summary>

1. `N = 38`, `n = 24`, so `c = 38 / 24 ≈ 1.58`. Hubs 1 and 2 take 20 quests and hub 3 takes the last 4. Hub 4 sees nothing.
2. Finishing hub 3 means `n = 30`. `30 = 12,000 × 0.8 / (q × 1.25)` gives `q = 9,600 / 37.5 = 256` XP. Lowering quest XP stretches the zone. It also makes every quest less rewarding compared with grinding, which is GD202 week 6's detour test.

</details>

## 3. Pacing inside the zone

The XP budget says how far players get. Pacing says what it feels like on the way. Three clocks run in a zone.

**The level clock.** Minutes per level-up is `XP to next level / XP per minute`. With 500 XP per quest and 6 minutes per quest (travel included), a player earns about 83 XP per minute, so level 10 takes 24 minutes and level 14 takes about 34. Players feel a level-up as a reward beat, so a zone with 30-minute levels gives a beat every half hour. GD203 week 7 built the whole curve. Here you only need to check that the zone's levels land at a rate you like.

**The hub clock.** Minutes between arriving at new hubs is `quests per hub × minutes per quest`, plus the walk to the next hub. With 10 quests at 6 minutes, that's an hour per hub. A new hub means new faces, a new vendor and a new flight point, so the hub clock is the zone's main source of novelty. Short hubs feel brisk and thin. Long hubs feel like home, then like a chore.

**The story clock.** GD202 week 8 gave the zone a spine of bottleneck quests. Place them against the other two clocks. A spine beat that lands just after a level-up competes with it. One that lands in a long stretch without either gives the player a reason to keep going.

Now combine the clocks with section 2. A player with `o = 0.2` reaches the "outlevelled" line after 19 quests, about 115 minutes of questing. If the zone's big story beat sits at minute 150, they never see it. When you plan a zone, draw all three clocks on one timeline and mark where each player type in your table leaves.

### Skipping and parallel hubs

Two refinements make the model closer to real play.

**Skipping.** Players don't do every quest. If a player does a share `s` of the quests they meet, they walk past `n / s` quests to complete `n`. The "outlevelled" line moves further into the zone as `s` falls, which means more of the zone is walked through (seen) but less of it is played. A zone with `c = 1.25` and `s = 0.8` is exactly used up, with the player walking through all 30 quests and doing 24.

**Parallel hubs.** If hub 2 and hub 3 both open after hub 1 and the player chooses one, the "last hub dies first" problem turns into "the less popular hub dies." You have traded a predictable loss for an unpredictable one, and you can measure which hub players pick. GD202 week 8's order-control number `C` drops, and the story must work in either order.

## 4. Scaling, and what it costs at scale

Scaling changes the production maths as much as the design.

In a fixed-level world, each level range needs at least one zone, and extra zones for the same range split the players. In a scaled world, every zone can serve every level in its range, so you can build fewer, richer zones, or let players choose among many. Chromie Time is the extreme case: several expansions' zones serve the same levels, and each player's path uses only a fraction of them. The content already exists, so the production cost is zero. The cost is that a new player's route through fourteen years of world is now a menu rather than a journey.

Scaling also changes what players experience.

- **The world stops getting smaller.** In a fixed-level world, a level-40 player walking through a level-10 zone feels powerful. In a scaled zone, nothing changes. Many players valued that feeling, and GD203 week 8 showed how to keep some of it by scaling enemies more slowly than players.
- **Groups of mixed level work.** ESO and GW2 both scale to let friends of different levels quest together. In a fixed-level world, one of them is either useless or the other is carried.
- **Old content stays populated.** FFXIV's sync and GW2's downscaling bring high-level players back to low zones, which keeps them busy for newcomers. GD201 week 11 showed why a zone with no one in it feels dead.

The model suggests a middle path many games take. Scale the zone within a range (so outside XP doesn't cut the ending), but end the range where the next zone begins (so players still move on and still outgrow places). The zone then needs `c ≥ 1` only for its own range, and the last hub survives.

## In-class activity (25 minutes)

Groups of three, with the interactive and a spreadsheet.

1. **(5 min)** Your zone spans levels 20 to 24 with XP to next level of 4,000, 4,300, 4,600 and 4,900. Quests pay 600 XP with `k = 0.2`. Compute `X` and `n` for a solo quester.
2. **(10 min)** The team can build 36 quests. Split them into hubs (any number, any sizes) so that a player with `o = 0.25` sees at least half of the last hub. Record your split and the hub-seen shares for `o = 0` and `o = 0.25`.
3. **(5 min)** Place the zone's story climax in a hub. Say which of your player types misses it.
4. **(5 min)** Swap with another group. Find the player type their design serves worst, and propose one change: a hub split, a `q` change, or scaling within a range.

Expected output: `X`, `n`, a hub split, two rows of hub-seen shares, and the other group's proposed change.

## Common misconceptions

- **"More quests make a better zone."** Past `c ≈ 1.5` for your typical player, extra quests land in hubs that few players reach. Spend the budget on making the quests players do reach better.
- **"Players skip the end of the zone because it's worse."** Often they skip it because their XP bar is full. Check `c` before blaming the content.
- **"Rested XP just speeds everyone up equally."** It speeds up only kill XP and only for players who were away. It shortens zones most for the part-time players it is meant to help.
- **"Level scaling removes the need to budget XP."** It removes the ceiling within the scaled range. You still need to budget play time, story order and the point where the player leaves for the next zone.

## Check yourself

1. A zone for levels 30 to 33 needs 6,000, 6,500 and 7,000 XP to next level. Quests pay 700 XP with `k = 0.3`. How many quests does a solo quester need?
2. The zone has three hubs of 10, 8 and 8 quests. For the player in question 1, what share of each hub do they see? Now give them `o = 0.3` and recompute.
3. A designer proposes cutting hub 3 and adding its 8 quests' worth of XP (at 700 each) as a dungeon at the end of hub 2. Which players does this help and which does it hurt?
4. In a scaled zone, `q` is paid at the player's level and the zone's range tops out at level 40. What limits how many of the zone's quests a player does now?

<details>
<summary>Answers</summary>

1. `X = 19,500`. Each quest is worth `700 × 1.3 = 910` XP, so `n = 19,500 / 910 ≈ 21.4` quests.
2. Solo: hub 1 100%, hub 2 100% (18 quests used), hub 3 `3.4 / 8 ≈ 43%`. With `o = 0.3`: `n = 19,500 × 0.7 / 910 = 15.0`. Hub 1 100%, hub 2 `5 / 8 ≈ 63%`, hub 3 0%.
3. It helps players who like dungeons, who now get the zone's last 8 quests' worth of XP in one run. It hurts solo players and anyone who avoids groups, who now have `N = 18` quests against a need of 21.4, so `c ≈ 0.84 < 1` and they must grind or go elsewhere for the last few thousand XP.
4. Quests keep paying until the player reaches level 40, so the XP budget no longer ends the zone early for most players. What limits them is the zone's content and story (they run out of quests) and the time they are willing to spend there. The designer now budgets minutes, not XP.

</details>

## Lab / assignment hook

[Lab 02, zone XP budget](../labs/lab02.md). You implement the XP demand, quests-needed and hub-coverage functions, extend them with skipping and parallel hubs, and use them to lay out the quest hubs for your final project's approach zone so that each player type you support reaches the zone's climax. The layout feeds the final dungeon brief, whose entrance sits in that zone.

## Sources

- Warcraft Wiki, "Patch 7.3.5" (released 16 January 2018). Every zone in Kalimdor, Eastern Kingdoms, Outland, Northrend, Pandaria and Draenor now uses the level scaling system introduced in Legion; the patch notes describe more options for where to quest and when to move on. https://warcraft.wiki.gg/wiki/Patch_7.3.5
- Warcraft Wiki, "Zone scaling" (as of the Midnight era, 2026). Mobs, quests and loot scale with the character's level over a range; first introduced for the Broken Isles in Legion; end-game content excluded. https://warcraft.wiki.gg/wiki/Zone_scaling
- Warcraft Wiki, "Timewalking Campaigns" (Chromie Time). Added in patch 9.0.1 (13 October 2020); level ranges per era, 10-60 in Shadowlands, 10-71 from The War Within, 10-81 from Midnight. https://warcraft.wiki.gg/wiki/Chromie_Time
- Warcraft Wiki, "Rest" (current retail). Double XP from kills and gathering while rested; quest and exploration XP do not use the bonus; accrual in inns and cities about four times faster than outside; maximum 150% of a level. https://warcraft.wiki.gg/wiki/Rest
- UESP, "Online:One Tamriel". Released with Update 12 on 5 October 2016 (PC/Mac); battle levelling applied to every zone; rewards appropriate to character level. https://en.uesp.net/wiki/Online:One_Tamriel
- Final Fantasy XIV Online Wiki (consolegameswiki), "Level Sync" (as of 2026). FATEs cannot be joined when more than 5 levels above the recommended level without syncing down; duties sync down automatically. https://ffxiv.consolegameswiki.com/wiki/Level_Sync
- Guild Wars 2 Wiki, "Dynamic level adjustment" (game version as of 2026, as cited in GD201 week 10). A character is scaled down to the area's maximum level plus one. https://wiki.guildwars2.com/wiki/Dynamic_level_adjustment
- The zone, its XP table, quest rewards and hub sizes are invented for teaching.

## Interactive spec: examples/w02-zone-xp-budget.html

**The one insight.** Outside XP is paid for out of the end of the zone. As the outside-XP slider rises, the last hub empties before any other hub loses a single quest, while the production cost of every hub stays the same.

**Layout.** Two linked views, side by side on wide screens, stacked on phones (zone first).

- **Left view, "The zone as played".** A horizontal track of `N` quest markers (circles), grouped into hub bands with labels "Hub 1", "Hub 2", and so on. Above the track, an XP bar that fills from left to right as quests are done, with tick marks at each level-up (label the level). A vertical line labelled "outlevelled" at the fractional quest index `n`. Markers left of the line are filled; markers right of it are hollow and greyed. The spine beat (a star marker, draggable to any quest) is labelled "zone climax"; its label turns to "missed" when it lies right of the line.
- **Right view, "Built vs played".** One column per hub, height proportional to that hub's quest count (the production cost), filled to the hub-seen share. Label each column with the share and the count "k of s quests played". A total line under the chart: "built N, played n, unused N − n (x%)".
- **Readout.** `X`, `n`, `c`, share of zone seen, minutes in zone (`n × t_q`), and minutes per level for each level in the table.

**Controls.**
- Presets: "Solo", "Rested", "Some dungeons", "Dungeon heavy" (the four rows of the lecture table).
- Quest XP `q`: slider 100 to 1,000, step 10, default 400.
- Kill share `k`: slider 0 to 1, step 0.05, default 0.25.
- Outside XP `o`: slider 0 to 0.8, step 0.05, default 0.
- Hub sizes: three number fields (1 to 20 each, default 10, 10, 10) and a button to add a fourth hub.
- Minutes per quest `t_q`: slider 2 to 15, default 6.
- Checkbox "Zone scaling (within range)". When on, the XP bar shows level-ups continuing past 15, the outlevelled line is removed, and every hub fills to 100%. Show the end level reached, computed by walking the XP table extended by +200 XP per level beyond 14 (15: 3,000, 16: 3,200, and so on).

**Formulas.**
- `X = Σ XP_to_next` for levels 10 to 14 (2,000, 2,200, 2,400, 2,600, 2,800).
- `n = X × (1 − o) / (q × (1 + k))`, `c = N / n`, share seen `= min(1, 1 / c)`.
- Hub seen: walk hubs in order, each takes `min(size, remaining)`; share `= taken / size`.
- XP per minute `= q × (1 + k) / t_q`; minutes for level L `= XP_to_next(L) / XP per minute`, with outside XP adding `o / (1 − o)` of the quest rate.

**Test values** (hubs 10, 10, 10, `q = 400`).
- Solo (`k = 0.25`, `o = 0`): `n = 24.0`, `c = 1.25`, hubs 100%, 100%, 40%.
- Rested (`k = 0.5`, `o = 0`): `n = 20.0`, `c = 1.50`, hubs 100%, 100%, 0%.
- Some dungeons (`k = 0.25`, `o = 0.2`): `n = 19.2`, `c = 1.56`, hubs 100%, 92%, 0%.
- Dungeon heavy (`k = 0.25`, `o = 0.5`): `n = 12.0`, `c = 2.50`, hubs 100%, 20%, 0%.
- Solo with a fourth hub of 8: `c ≈ 1.58`, hub 4 at 0% (check yourself Q1).
- Solo, `t_q = 6`: 83.3 XP per minute; level 10 takes 24.0 minutes, level 14 takes 33.6 minutes; minutes in zone 144.

**First screen.** The "Solo" preset with the climax star placed in hub 3, quest 26, showing "missed" already, so the student sees that even the slowest player in the table misses it, then drags `o`.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. Hub bands differ by pattern as well as colour. Markers reachable by Tab when dragging the climax star; arrow keys move it. Numbers in tabular figures.

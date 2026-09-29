# GD201 · Week 11 — Shared spaces: designing for many players at once

**Why this matters:** A zone you tested alone will be played by hundreds of people at once, and by three people on a quiet Tuesday a year later. The same geometry can feel dead, lively or unplayable depending only on how many players stand in it and where they stand. If you can predict how many other players each person will see, you can size a zone, place its camps and choose a server technology on purpose instead of finding out on launch day.

**You will be able to:**
- Compute the expected number of other players a person sees at a camp and in open ground, from population, camp count, the share of players at camps and view radius.
- Derive a zone's comfortable population range from target neighbour counts, and the number of zone copies a launch needs.
- Compare sharding, layering, megaserver instancing and time dilation as answers to the same density problem, and say what each one costs.
- Critique a zone layout and its reward rules for whether a crowd helps or hurts the players in it.

**Before class:** Christopher Totten, *An Architectural Approach to Level Design* (2nd ed., CRC Press, 2019). Use the index entries for "multiplayer" and read the passages on designing spaces for several players (about 15 pages). Guild Wars 2 Wiki, "Megaserver" and the "Event scaling" section of "Dynamic event" (15 minutes). EVE University Wiki, "Time dilation" (5 minutes).

**Prerequisites from earlier courses:** [MA101 week 14, distances and ranges](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w14-distances-ranges-and-squared-distance.md) (the area of a range circle, `π r²`, and who counts as "in range"). Looking ahead to year 3, [MMO305 week 2, playing alone together](../../MMO305-social-systems-and-online-behaviour/lectures/w02-playing-alone-together.md) covers co-presence versus co-activity, and why seeing other players matters even when you don't group with them. [MMO301 week 6, EVE Online, the single-shard sandbox](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w06-eve-online-the-single-shard-sandbox.md), also in year 3, covers what a single shard changes. From this course, [week 10, hubs, spokes, and gating](w10-hubs-spokes-and-gating.md) (why every errand passes through the hub).

**Interactive:** [`examples/w11-crowd-capacity.html`](../examples/w11-crowd-capacity.html). Keep it open during section 2.

---

## 1. Designing for a number you don't control

In a single-player level you know exactly how many players are in the room: one. In a multiplayer match you know it within a small range: 12, or 64, or 100, set by matchmaking. In a persistent world you don't know it at all. The number of players in a zone rises when a zone launches or an event starts, falls at night, and falls again as the player base moves on to newer content. A zone lives through all of these numbers, often in its first month.

Three terms for this lecture.

**Population `P`** is the number of players in one copy of a zone at one moment.

**Density** is players per unit of area. It is what players feel. A 100-player zone of one square kilometre and a 400-player zone of four square kilometres have the same density on average, but only on average, as you will see.

**Neighbours** are the other players a person can see and interact with. We'll count someone as a neighbour if they stand within a **view radius `r`**. It is the distance at which you notice another player, can read what they're doing, and can compete or cooperate with them. It is a design value, not the draw distance of the engine. In a dense forest `r` might be 25 metres; on open plains, 60.

The number of neighbours decides the experience. Zero neighbours for a long time feels like an empty, dead world. A few neighbours is the classic appeal of an MMO: other people doing their own thing nearby, who might help or might become friends. Dozens of neighbours at the same monster camp means waiting in line for every kill.

## 2. Worked example: the camp that is always crowded

### The hook

When World of Warcraft Classic launched in 2019, Blizzard ran it with **layering**, a system that splits the outdoor world into several separate copies, each with its own monsters, objects and players. The original game of 2004 had nothing like it. Blizzard disabled layering before the game's second content phase, on 13 November 2019, once the population had spread out.

So the same world, with the same map and the same number of monsters, was judged unplayable at one population and fine at another. And it wasn't the whole zone that broke. A starting zone has plenty of empty hillside. What breaks is the handful of places every player needs: the quest-giver's camp, the cave with the quest monsters, the path between them. The average density of the zone hides this completely. You need a model that separates where players stand.

### The model

Split the players in a zone into two groups.

- A share `f` of them stand at **camps**: the quest hubs, monster camps and resource spots that the zone's content points at. There are `H` camps, and a camp is small enough that everyone at it can see everyone else there.
- The rest, `1 − f`, are in the **open**: travelling, exploring, fighting in the spaces between camps. The open ground has area `A`, and players are spread across it evenly.

The number of neighbours a player sees is the number of other people in the place they stand, within view:

```
at a camp:     N_camp = f × P / H − 1
in the open:   N_open = (1 − f) × P × π r² / A
```

- `P` is the zone's population.
- `H` is the number of camps, and `f` the share of players at camps.
- `r` is the view radius, so `π r²` is the area a player can see (MA101 week 14).
- `A` is the open ground's area.
- The `− 1` at the camp removes the player themselves.

Both lines say the same thing: **neighbours = local density × the area you can see.** At a camp, the local density is so high that the whole camp is in view, so the count is simply the number of other people there. In the open, only the circle around you counts.

The model assumes players are spread evenly across camps and across the open ground. Real players bunch up more than that (section 3 of the lab measures by how much), so treat these numbers as the minimum crowding you will get.

### Numbers you can check

A teaching zone: `A = 1,000,000` m² of open ground (one square kilometre), `H = 8` camps, `f = 0.6`, and `r = 40` m, so `π r² ≈ 5,027` m², about 0.5% of the open ground.

| Population `P` | At a camp `N_camp` | In the open `N_open` |
|---|---|---|
| 25 | 0.88 | 0.05 |
| 50 | 2.75 | 0.10 |
| 100 | 6.50 | 0.20 |
| 200 | 14.00 | 0.40 |
| 400 | 29.00 | 0.80 |
| 1,000 | 74.00 | 2.01 |

Check the row for 100 by hand. Sixty players are at camps, 7.5 per camp, so each sees 6.5 others. Forty are in the open, and each sees `40 × 0.005027 ≈ 0.20`.

Two things stand out. First, at 100 players a player at a camp sees about 32 times as many people as a player in the open, and the gap widens as `P` grows (37 times at 1,000). With 100 players, the camps are busy and the open ground is empty. A player who complains the zone is "dead" and another who complains it's "packed" can be in the same zone at the same moment. Second, crowding at camps grows in step with population. Double `P` and `N_camp` roughly doubles.

The code that produced the table:

```python
import math

A = 1_000_000   # open ground outside the camps, m² (1 km²)
H = 8           # camps
f = 0.6         # share of players standing at a camp
r = 40          # view radius, m

def camp_neighbours(P):
    return f * P / H - 1

def wild_neighbours(P):
    return (1 - f) * P * math.pi * r**2 / A

for P in (25, 50, 100, 200, 400, 1000):
    print(f"{P:5d} {camp_neighbours(P):6.2f} {wild_neighbours(P):5.2f}")

n_min, n_max = 2, 10
print("P_min", H * (n_min + 1) / f, "P_max", math.floor(H * (n_max + 1) / f))
```

It prints:

```
   25   0.88  0.05
   50   2.75  0.10
  100   6.50  0.20
  200  14.00  0.40
  400  29.00  0.80
 1000  74.00  2.01
P_min 40.0 P_max 146
```

### From neighbours to capacity

Now turn the model around. Decide what a good camp feels like, as a range of neighbours, and solve for the population that produces it. Say you want at least `n_min = 2` other players at a camp (so the world feels inhabited) and at most `n_max = 10` (so nobody waits long for a kill). Solving `f × P / H − 1 = n` for `P`:

```
P_min = H × (n_min + 1) / f
P_max = H × (n_max + 1) / f
```

For the teaching zone, `P_min = 8 × 3 / 0.6 = 40` and `P_max = 8 × 11 / 0.6 = 146.7`, so 146 players (round down to stay under 10). That is the zone's **comfortable range**: 40 to 146 players per copy.

The last line of the code printed exactly that. Notice what isn't in the formula: the zone's area. Capacity is set by the camps, not by the square kilometres. Doubling the map's size without adding camps changes nothing for the players standing at them.

What if 3,000 players arrive in the zone on launch day? One copy would put 225 players at every camp, each seeing 224 others. The server must split them into copies:

```
copies = ceiling(P / P_max) = ceiling(3,000 / 146) = 21
```

With 21 copies of about 143 players each, every camp holds 10.7 players and each sees 9.7 others. Three months later, 60 players remain across the whole server. Twenty-one copies would give each copy about 3, and `N_camp` becomes negative in the model, which means most camps are empty. Now the server must merge copies, not split them.

Open the interactive. The left panel draws the zone from above, with eight camps as rings and each player as a dot. The right panel plots `N_camp` and `N_open` against `P`, with a shaded band between `n_min` and `n_max`. Drag the population slider from 20 to 3,000. The camp line leaves the band at 146 and the dots pile up at the camps while the open ground stays sparse. Then switch on "split into copies" and watch the camp line fold back into the band as the server adds copies.

### Cross-game recognition

Every persistent world has to answer the question "what do we do when `P` leaves the comfortable range?" The answers look different, but each one changes a term of the model.

**World of Warcraft, sharding (patch 6.0.2, October 2014) and cross-realm zones.** When too many players occupy an outdoor area, sharding creates duplicate copies of it, each with its own monsters, objects and players. That caps `P` per copy, which is our `copies = ceiling(P / P_max)`. The opposite problem, too few players, is handled by cross-realm zones, which merge players from several realms into one shared copy. Warcraft Wiki's article describes the two as solving overcrowding and undercrowding. They are the two ends of the comfortable range.

**World of Warcraft Classic, layering (2019).** Layering is the same idea applied to the whole world at once: each layer is a full copy of the outdoor world. Blizzard used it for the launch rush and removed it once `P` per realm dropped, because separate copies also split the community a realm is meant to share.

**Guild Wars 2, the megaserver (roll-out completed April 2014).** Guild Wars 2 stopped tying players to a home server's copy of each map. All players in a region are placed into shared copies of a map, and the game opens a new copy when a map is getting full. When it chooses which copy you join, it weighs your party, guild, language and home world. In the model's terms, the megaserver adjusts the number of copies continuously in both directions, keeping `P` per copy inside the range, and it tries to make your neighbours people you know.

**EVE Online, time dilation (dev blog, April 2011).** EVE runs almost its whole player base in one universe and does not make copies of a star system (MMO301 week 6). When thousands of players gather in one system, the server cannot keep up, so it slows the simulation there. Time dilation can slow in-space time down to 10% of normal, so one game second takes ten real seconds. EVE refuses to cut `P`, so it pays for density with time instead. The battle stays whole, and everyone in it plays in slow motion.

Four systems, one model. Sharding and layering cap `P` from above. Cross-realm zones and the megaserver raise `P` from below. EVE keeps `P` and changes the speed of the world.

### Design judgment, eyes open

Copies are a server's answer. A level designer has earlier, cheaper levers, and each has a cost.

- **Add camps (raise `H`).** Doubling `H` from 8 to 16 doubles `P_max` to 293. It costs content: more quest areas, more monster camps. It also doubles `P_min`, from 40 to 80, because more camps need more people to feel alive. A zone with many camps is lively at launch and empty sooner.
- **Spread the players (lower `f`).** Objectives that live in the open ground (roaming monsters, gathering spread over the map, exploration goals) pull players out of the camps. Halving `f` to 0.3 also doubles `P_max` to 293. The cost is the social side: people in the open rarely meet, because `N_open` stays below 1 until `P` is very high.
- **Change the view radius.** A forest with short sightlines (small `r`) makes the open ground feel quieter at the same density. Open plains make it feel busier. It doesn't change the camps, where everyone is in view anyway.
- **Split into copies.** Solves crowding at any scale, but each copy is a separate world. Friends end up in different copies, and the "everyone was there" moment disappears. That is the price WoW Classic's community paid for layering, and the reason the megaserver's placement rules exist.

The deliberate choice is the band. How many neighbours do you want at a camp? That number follows from what the camp is for. A quest-giver's camp can hold 30 people without harm, because talking to an NPC doesn't use anything up. A camp with six monsters that four players are trying to kill cannot. Section 3 is about changing the rules so that the second camp behaves more like the first.

## 3. When a crowd helps and when it hurts

Neighbours are only a problem if they compete with you. Whether they do depends on the rules for who gets credit for a kill, who gets the loot, and whether a resource is used up when someone takes it. Change those rules and the same `N_camp` means something else.

**Exclusive credit (tagging).** In many MMOs, the first player or group to damage a monster owns it: only they get experience, loot and quest credit. This is called tagging. Under exclusive credit, every neighbour at a camp is a competitor for the same spawns, and `N_camp = 10` means ten people racing for each monster. Week 12 turns this into wait times.

**Shared credit.** Guild Wars 2 gives every player who contributes enough to a kill their own loot, calculated as if they were the only participant, so one enemy can drop the same rare item for several players. Participation counts damage and also support, such as healing or reviving an ally. Under shared credit, a neighbour who attacks the same monster speeds up your kill instead of stealing it. The crowd is now help.

**Scaling encounters.** Guild Wars 2's dynamic events scale up and down with the number of players currently taking part. A crowd doesn't trivialize the event, and a lone player isn't blocked by it. Scaling bends the model's band. If the event scales, the top of the band (`n_max`) can move much higher before a camp feels bad.

**Per-player resources.** Guild Wars 2 lets every character on an account gather each resource node, with the node resetting for that character a few hours later. Nobody takes a node away from anyone else. Week 12 compares this with shared nodes.

The pattern is simple. Where a resource is used up and credit is exclusive, the top of the band is low, and your capacity is small. Where credit is shared and encounters scale, the top of the band is high, and a crowd becomes the social moment MMO305 week 2 describes: strangers working toward one goal without forming a group. Before you tune `H` and `f`, decide which camps are competitive and which are cooperative. The numbers only mean something after that choice.

## 4. Laying out the shared space

The model gives you capacity. The layout decides whether players can actually move and act in it.

**Make hubs wide, and camps wider than they look.** Week 10 showed every errand passes through the hub, so the hub is the densest place in the zone. Paths into it, doorways and the space in front of quest-givers must fit the peak `N_camp` without players blocking each other's view or clicks. A doorway a single player finds generous is a bottleneck for thirty.

**Separate the camps.** If two camps sit within `r` of each other, their players see each other and the two camps merge in players' minds into one crowded place. Keep camps at least `2r` apart, or split them with terrain that blocks sight.

**Spread the objectives within a camp.** A camp where the six quest monsters stand in one clump concentrates everyone on one spot. Spread across a larger area, the same six monsters let players work side by side without contesting the same target.

**Design the quiet days too.** At the bottom of the range, `N_camp` is below 1 and group content fails because nobody is around. Solo-able versions, scaling, and merging copies protect the zone's second year. Before you ship, compute `N_camp` at 20% of your launch population, and play the zone at that density.

## In-class activity (25 minutes)

In groups of three, with the interactive and one zone from your final-project blockout (or the teaching zone if yours isn't ready).

1. **(5 min)** Count your zone's camps `H`. Estimate `f` by listing every quest or objective and marking whether it is done at a camp or in the open.
2. **(5 min)** For each camp, decide whether it is competitive (exclusive credit, used-up resources) or cooperative (shared credit, nothing used up). Choose `n_max` separately for the two kinds.
3. **(10 min)** Compute `P_min` and `P_max` using the competitive camps only. Then find one change (camps, objectives, or rules) that raises `P_max` by at least 50% without raising `P_min` above 30. Check it in the interactive.
4. **(5 min)** Report your change to another group, who must name what it costs.

Expected output: `H`, `f`, the two `n_max` values, `P_min` and `P_max` before and after your change, and the cost the other group names.

## Common misconceptions

- **"Bigger zones hold more players."** Capacity comes from camps, not area. A bigger map with the same eight camps crowds at the same population. Area only changes how empty the open ground feels.
- **"Average density tells you if a zone is crowded."** At 100 players the teaching zone's camps are about 32 times as crowded as its open ground. Always compute density where players stand, not across the whole map.
- **"More copies are always better."** Each copy splits the players who could have met. Copies solve the top of the band and make the bottom worse, which is why games that split also merge.
- **"Crowding is a server problem."** The server decides how many copies exist. The designer decides `H`, `f`, `r` and the credit rules, and those decide where the crowding happens and whether it hurts.

## Check yourself

1. A zone has `H = 10` camps, `f = 0.5` and 300 players. How many others does a player at a camp see? With `A = 2,000,000` m² and `r = 50` m, how many does a player in the open see?
2. For the zone in question 1, you want between 3 and 12 others at each camp. What is the comfortable range of `P`? How many copies does a launch population of 2,500 need?
3. A designer doubles the teaching zone's open ground to 2 km² to "make room for launch". What happens to `P_max` and to `N_open` at `P = 100`?
4. The teaching zone's camps use exclusive credit and `n_max = 10`. The team switches them to shared credit with scaling and decides a camp is fine up to 40 others. What is the new `P_max`, and how many copies would the 3,000-player launch need now?

<details>
<summary>Answers</summary>

1. `N_camp = 0.5 × 300 / 10 − 1 = 14`. `N_open = 150 × π × 50² / 2,000,000 = 150 × 7,854 / 2,000,000 ≈ 0.59`.
2. `P_min = 10 × 4 / 0.5 = 80`. `P_max = 10 × 13 / 0.5 = 260`. Copies `= ceiling(2,500 / 260) = 10`.
3. `P_max` doesn't change (146), because it depends only on `H`, `f` and `n_max`. `N_open` halves, from 0.20 to 0.10. The open ground gets emptier and the camps stay exactly as crowded.
4. `P_max = 8 × 41 / 0.6 ≈ 546.7`, so 546. Copies `= ceiling(3,000 / 546) = 6` instead of 21. Changing the rules cut the number of copies by more than two thirds, so players are split into far fewer separate worlds.

</details>

## Lab / assignment hook

[Lab 11, zone population planner](../labs/lab11.md). You implement the neighbour model and a Monte Carlo placement that tests it, measure how much uneven camp choice adds to crowding, and write a population plan for your final zone: its comfortable range, its competitive and cooperative camps, and what happens at launch and a year later. This feeds the final zone's design document.

## Sources

- Warcraft Wiki, "Sharding (term)" (accessed September 2026). Sharding added in patch 6.0.2 (14 October 2014, Warlords of Draenor) to prevent outdoor overcrowding by creating duplicate copies of an area; cross-realm zones serve the opposite purpose of preventing undercrowding.
- Warcraft Wiki, "Layering" (accessed September 2026). Layering used at the 2019 launch of WoW Classic, each layer a separate copy of the outdoor world, later disabled; Blizzard said it intended to merge each realm's layers before Phase 2 (November 2019).
- Guild Wars 2 Wiki, "Megaserver" (accessed September 2026). Players in a region share map copies, a new copy opens when a map is getting full; placement weighs party, guild, language and home world; roll-out completed 21 April 2014.
- Guild Wars 2 Wiki, "Dynamic event" (accessed September 2026). Events scale up and down with the number of participating players; each participant gets experience and loot as if they were the only participant.
- Guild Wars 2 Wiki, "Loot" (accessed September 2026). Each player who contributes enough to a kill can loot it, loot is unique to each player, and supporting allies counts toward participation.
- Guild Wars 2 Wiki, "Gathering" (accessed September 2026). Most resource nodes can be used by each character and reset for that character a few hours after gathering.
- EVE University Wiki, "Time dilation" (accessed September 2026), citing CCP's dev blog "Introducing Time Dilation (TiDi)" (22 April 2011). Time dilation slows in-space actions on overloaded nodes, down to a minimum of 10% speed.
- Totten, C. (2019). *An Architectural Approach to Level Design* (2nd ed.). CRC Press.

## Interactive spec: examples/w11-crowd-capacity.html

**Purpose.** Make the student see that crowding is local (camps are about 30 times as dense as the open ground), that capacity is set by camps rather than map area, and that splitting into copies folds the camp line back into the comfortable band.

**Layout.** Two linked panels, side by side on desktop, stacked on mobile (map first).

- **Left panel, the zone from above.** A square representing the open ground (drawn at fixed size regardless of `A`; label its side length in metres). `H` camps drawn as small rings evenly spaced on a grid inside the square, each with a count badge. Dots for players: `round(f × P / copies)` dots split evenly across camps (random positions inside each ring), and the rest scattered uniformly in the open. If `P / copies > 400`, draw one dot per 5 players and say so in a note. One highlighted "you" dot in the open with a dashed circle of radius `r` (scaled to the square). When copies > 1, show a row of small tabs "Copy 1 … Copy k" and draw copy 1.
- **Right panel, neighbours against population.** x-axis `P` from 20 to 3,000 (log scale, labelled). y-axis neighbours (log scale, 0.01 to 300; clamp values below 0.01 to the axis). Two lines: `N_camp` and `N_open`. A shaded horizontal band from `n_min` to `n_max`. Vertical markers at `P_min` and `P_max`. A marker dot at the current `P` on each line. When "split into copies" is on, draw the lines using the per-copy population `P / ceiling(P / P_max)` (the camp line becomes a sawtooth that stays in the band above `P_max`).
- **Readout.** `N_camp`, `N_open`, their ratio, `P_min`, `P_max`, copies `= ceiling(P / P_max)` (show "1" when splitting is off), and per-copy population.

**Controls.**
- `P` slider, 20 to 3,000, logarithmic steps, default 100. Numeric input beside it.
- `H` slider 1 to 30, default 8.
- `f` slider 0.1 to 0.9, step 0.05, default 0.6.
- `r` slider 10 to 100 m, step 5, default 40.
- `A` slider 0.25 to 4 km², step 0.25, default 1 (convert to m²).
- `n_min` and `n_max` number inputs, defaults 2 and 10.
- "Split into copies" toggle, default off.
- Preset buttons: "Teaching zone" (defaults), "Launch day" (`P = 3,000`, split on), "One year later" (`P = 60`, split on), "Shared credit" (`n_max = 40`).

**Formulas.**
- `N_camp = f × P / H − 1` (per copy: replace `P` with `P / copies`). Display negative values as "0 (camp usually empty)".
- `N_open = (1 − f) × P × π r² / A`.
- `P_min = H × (n_min + 1) / f`, `P_max = floor(H × (n_max + 1) / f)`, copies `= ceiling(P / P_max)`.

**Test values** (`A = 1` km², `H = 8`, `f = 0.6`, `r = 40`):
- `P = 100`: `N_camp = 6.50`, `N_open = 0.20`, ratio about 32.
- `P = 400`: `N_camp = 29.00`, `N_open = 0.80`.
- `P = 1,000`: `N_camp = 74.00`, `N_open = 2.01`.
- `n_min = 2`, `n_max = 10`: `P_min = 40`, `P_max = 146`.
- `P = 3,000`, split on: 21 copies, 142.9 per copy, `N_camp = 9.71`.
- `n_max = 40`: `P_max = 546`; `P = 3,000` split gives 6 copies.
- `H = 16`: `P_max = 293`. Changing `A` to 2 km² leaves `P_max` at 146 and halves `N_open`.

**The one insight.** On first load, the map must already show dense camp rings and a nearly empty open ground at `P = 100`, and dragging `P` up must push the camp line out of the band while changing `A` leaves `P_max` unmoved.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. Camp and open lines differ in colour and dash pattern. Dot animation (re-scatter on change) disabled under `prefers-reduced-motion`. All controls keyboard reachable with visible focus.

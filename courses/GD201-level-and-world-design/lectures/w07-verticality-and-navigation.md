# GD201 · Week 07 — Verticality and navigation

**Why this matters:** The moment a level has height in it, the way down stops being the way back up. Players feel this as "I jumped down and now I'm stuck", as a thrilling shortcut, or as a map they can't read. Each of those comes from choices you made about ledges, ladders and drops, and you can compute most of them before anyone plays.

**You will be able to:**
- Compute the traversal time of climbs, drops and slopes, and the up-down asymmetry ratio of a vertical edge.
- Model a level with height as a directed graph with timed edges, and compute out and back times and the return ratio with a shortest-path search.
- Design step-down ledges and rest platforms from a safe drop height and a maximum climb, and place a shortcut that brings the return ratio under a target.
- Critique a vertical space for orientation problems (stacked floors, lost landmarks, one-way commitment) and propose fixes.

**Before class:** Christopher Totten, *An Architectural Approach to Level Design* (2nd ed., CRC Press, 2019), chapter 4 "Basic Gamespaces" and chapter 6 "Building Exciting Levels with Dangerous Architecture". Reread CS102 week 8, section 3, on directed graphs and asymmetric distance.

**Prerequisites from earlier courses:** [CS102 week 8, graphs, maps and dialogue](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w08-graphs-maps-and-dialogue.md) (directed edges, breadth-first search, and why distance in a directed graph is not symmetric). [MA101 week 2, linear functions and rates](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w02-linear-functions-and-rates.md) (time equals distance over speed, and unit conversion). [GD201 week 1, level design as teaching](w01-level-design-as-teaching.md) (recovery time `r` and the cost of sending a player back). Free fall under gravity is treated properly in [MA201 week 6](../../MA201-linear-algebra-and-physics-for-games/lectures/w06-kinematics-position-velocity-acceleration.md) (kinematics); here you need only one formula from it.

**Interactive:** [`examples/w07-drop-and-climb.html`](../examples/w07-drop-and-climb.html). Keep it open during section 2.

---

## 1. What height changes

A flat level is mostly symmetric. If a corridor takes 5 seconds to walk from A to B, it takes 5 seconds from B to A. The level can still be confusing, but the cost of a mistake is a walk you have already seen.

Add height and three things stop being symmetric.

**Time.** Going down is fast and going up is slow. A player can step off a 6 metre ledge and land in under a second. Climbing back up a ladder of the same height takes several seconds. Walking up a hill is slower than walking down it. Some drops can't be reversed at all.

**Information.** From high ground you see more of the level, and you see it laid out like a map. From low ground you see walls and the undersides of things. A player on a balcony can plan. A player in a pit can only react.

**Risk.** Height is the most readable danger in games. Every player knows a long drop can hurt. That makes height a cheap way to create tension, and a cheap way to create frustration when the fall sends you a long way back.

This week is mostly about the first asymmetry, because it is the one that changes how a level is connected. We treat a level as a **graph**: places are **nodes**, and the ways between them are **edges**. You met this in CS102 week 8, where an edge had a direction and a trapdoor could drop you into a room you couldn't climb out of. This week each edge also gets a **cost in seconds**, and the vertical edges get different costs in each direction.

Three terms you will use all week:

- A **vertical edge** is a connection whose main job is to change height: a ladder, a climbable wall, a lift, a drop off a ledge.
- A **one-way edge** is one the player can use in one direction only. The usual one-way edge in a 3D game is a drop that's too high to climb back.
- A **shortcut** is an edge added (often unlocked later) that makes a return trip much shorter than the route the player first took.

## 2. Worked example: the drop is free, the climb is not

### The hook

In Dark Souls (FromSoftware, 2011), you work your way up to the Undead Parish, a church high above the starting area, through a long run of fights. At the top you find an elevator. Ride it and you are back at Firelink Shrine, the hub where you started. The elevator only becomes usable from the Firelink end after you activate it from the Parish end. The game's world is one interconnected space, and it is linked by shortcuts like this one that open from the far side.

Players remember these moments as some of the best in the game. Nothing new was added to the world. What changed is a single edge in the graph, and it changed the return trip from minutes to seconds. This section puts numbers on that feeling.

### The model

Give every edge a time. For the four kinds of edge in this lecture:

```
walk or run:   t = d / v            d = path length (m), v = speed on that surface (m/s)
climb:         t = h / v_climb      h = height gained (m)
drop:          t = sqrt(2h / g)     g = the game's gravity (m/s²), only if h ≤ h_safe
slope:         use a different v for uphill and downhill
```

A drop higher than `h_safe`, the **safe drop height**, is not an edge at all in this model. It either kills or injures the player, and your level shouldn't route people through it. (Section 3 covers games that price a drop in health instead.)

For one vertical edge of height `h`, divide the climb time by the drop time. Call it the **asymmetry ratio**:

```
asymmetry = (h / v_climb) / sqrt(2h / g) = sqrt(g × h / 2) / v_climb
```

It grows with the square root of the height. Taller edges are more one-sided, even before they become too tall to drop.

For a whole trip from a start `S` to a goal `X`, the time is the **shortest path** through the graph: the route whose edge times add up to the least. The out time `T(S→X)` and the back time `T(X→S)` can be different, because the edges are directed. Define the **return ratio**:

```
return ratio = T(X → S) / T(S → X)
```

A return ratio of 1 means the way back costs the same as the way out. A return ratio of 7 means that after a quick trip out, the player faces a trip home seven times as long. That is what "stranded" feels like, as a number.

### Numbers you can check

Use these values for a teaching level (they are invented, not measured from any shipped game). The run speed matches week 1.

| Symbol | Meaning | Value |
|---|---|---|
| `v` | run speed on flat ground and downhill | 6 m/s |
| `v_up` | walking speed on the uphill trail | 4 m/s |
| `v_climb` | ladder climbing speed | 1.5 m/s |
| `g` | gravity | 20 m/s² |
| `h_safe` | highest harmless drop | 8 m |

Many games use gravity stronger than Earth's 9.8 m/s², because falls at real gravity feel floaty at game scale. 20 is a round number in that range.

First, one vertical edge at a time:

| Height `h` | Drop time `sqrt(2h/g)` | Climb time `h / 1.5` | Asymmetry ratio |
|---|---|---|---|
| 2 m | 0.45 s | 1.33 s | 2.98 |
| 4 m | 0.63 s | 2.67 s | 4.22 |
| 6 m | 0.77 s | 4.00 s | 5.16 |
| 8 m | 0.89 s | 5.33 s | 5.96 |
| 12 m | 1.10 s (unsafe) | 8.00 s | 7.30 |

Check the 6 m row: `2 × 6 / 20 = 0.6`, `sqrt(0.6) = 0.775`. Climb `6 / 1.5 = 4`. Ratio `4 / 0.775 = 5.16`. Or with the one-line form, `sqrt(20 × 6 / 2) / 1.5 = sqrt(60) / 1.5 = 7.746 / 1.5 = 5.16`.

Now the whole level. The **Cliff Ruin** has five places. The Camp and the Overlook sit on a clifftop 12 m up. The Ruin and the Gate are on the valley floor. Halfway down the cliff face is a Ledge at 6 m.

| Edge | Kind | Time |
|---|---|---|
| Camp ↔ Overlook | run 30 m | 5.0 s each way |
| Overlook → Ledge | drop 6 m | 0.77 s (one way) |
| Ledge → Ruin | drop 6 m | 0.77 s (one way) |
| Overlook → Ruin | drop 12 m | not an edge (over `h_safe`) |
| Ruin ↔ Gate | run 60 m | 10.0 s each way |
| Camp → Gate | trail down 150 m at 6 m/s | 25.0 s |
| Gate → Camp | trail up 150 m at 4 m/s | 37.5 s |
| Ruin → Overlook | ladder 12 m (shortcut, locked at first) | 8.0 s |

Trace the out trip from Camp to Ruin. Via the cliff: `5.0 + 0.775 + 0.775 = 6.55` s, which the code below prints as 6.5. Via the trail: `25 + 10 = 35` s. The cliff wins by a lot.

Trace the back trip. The drops only go down, so the cliff route doesn't exist in this direction. The only way home is `Ruin → Gate → Camp = 10 + 37.5 = 47.5` s. Return ratio `47.5 / 6.55 = 7.25`.

Unlock the ladder: `Ruin → Overlook → Camp = 8 + 5 = 13` s. Return ratio `13 / 6.55 = 1.98`.

Here is the same calculation in code. It is Dijkstra's algorithm, which is breadth-first search from CS102 week 8 with one change: the queue is ordered by total time so far instead of number of steps. [CS203 week 3, graphs and Dijkstra](../../CS203-artificial-intelligence-for-games/lectures/w03-graphs-and-dijkstra.md) covers it properly. For level-sized graphs you only need to trust that it returns the shortest total time.

```python
import heapq
from math import sqrt

V_RUN, V_UPHILL, V_CLIMB = 6.0, 4.0, 1.5   # metres per second
G, H_SAFE = 20.0, 8.0                        # m/s^2, highest harmless drop in metres

def walk(d, v=V_RUN): return d / v
def climb(h): return h / V_CLIMB
def drop(h): return sqrt(2 * h / G) if h <= H_SAFE else None   # None: not a safe edge

def cliff_ruin(ledge=True, ladder=False):
    edges = [("Camp", "Overlook", walk(30)), ("Overlook", "Camp", walk(30)),
             ("Ruin", "Gate", walk(60)), ("Gate", "Ruin", walk(60)),
             ("Camp", "Gate", walk(150)), ("Gate", "Camp", walk(150, V_UPHILL)),
             ("Overlook", "Ruin", drop(12))]
    if ledge:
        edges += [("Overlook", "Ledge", drop(6)), ("Ledge", "Ruin", drop(6))]
    if ladder:
        edges += [("Ruin", "Overlook", climb(12))]
    graph = {}
    for a, b, t in edges:
        if t is not None:                      # unsafe drops are not edges
            graph.setdefault(a, []).append((b, t))
    return graph

def shortest(graph, start, goal):
    best, queue = {start: 0.0}, [(0.0, start)]
    while queue:
        t, node = heapq.heappop(queue)
        if node == goal:
            return t
        if t > best[node]:
            continue
        for nxt, cost in graph.get(node, []):
            if t + cost < best.get(nxt, float("inf")):
                best[nxt] = t + cost
                heapq.heappush(queue, (t + cost, nxt))
    return float("inf")

for label, g in [("no ledge", cliff_ruin(ledge=False)), ("ledge", cliff_ruin()),
                 ("ledge + ladder", cliff_ruin(ladder=True))]:
    out, back = shortest(g, "Camp", "Ruin"), shortest(g, "Ruin", "Camp")
    print(f"{label:15} out {out:5.1f} s  back {back:5.1f} s  ratio {back / out:4.2f}")
```

Output:

```
no ledge        out  35.0 s  back  47.5 s  ratio 1.36
ledge           out   6.5 s  back  47.5 s  ratio 7.25
ledge + ladder  out   6.5 s  back  13.0 s  ratio 1.98
```

Read the three rows as three versions of the same level.

- **No ledge.** The 12 m drop is unsafe, so everybody takes the trail. Slow both ways, but fair: the return ratio is 1.36, and it only exceeds 1 because the trail is uphill on the way back.
- **Ledge.** One small platform halfway down turns an unsafe 12 m drop into two safe 6 m drops. The out trip gets more than five times faster. The back trip doesn't change at all. You have built a trap: a fun, fast descent into a place the player can only leave the long way.
- **Ledge and ladder.** One edge added at the bottom. The descent stays fast and the return drops from 47.5 s to 13 s.

Open the interactive. The left view is the cliff in side section with the five nodes. The right view shows two bars, out and back. Toggle the ledge on and watch the out bar collapse while the back bar stays put. Then unlock the ladder. Drag the climb speed slider down to 0.5 m/s and see how slow a climb has to get before the ladder stops being a good shortcut (at 0.5 m/s it takes 24 s, and the trip home is `24 + 5 = 29` s, still better than 47.5).

### Cross-game recognition

**Dark Souls (2011).** The Undead Parish elevator is the ladder in our model. Before activation, the edge between Firelink Shrine and the Parish doesn't exist in either direction. The first trip goes the long way through the Undead Burg. Activating the lift at the far end adds a fast two-way edge. The design pattern is to make the player earn the short edge by reaching its far end first, so the long route has already been learned and the shortcut arrives as a reward.

**Minecraft (Java Edition, 1.21 era).** Minecraft prices drops in health instead of forbidding them. A player takes no fall damage for the first 3 blocks, then 1 health point (half a heart) per block beyond that, rounded down, out of 20. Write it in our form: `h_safe = 3` blocks, and a drop of `h` costs `floor(h − 3)` health. A 12-block drop costs 9 health, almost half your bar, so it is an edge you can take once but not repeat. Ladders go the other way: the wiki gives about 2.35 blocks per second up and about 3 blocks per second down. A ladder's asymmetry ratio is only `3 / 2.35 = 1.28`. That is why the ladder is the standard Minecraft "shortcut": it is the one vertical edge that is nearly symmetric. Players who dig down into a cave and can't get back up are living in the "ledge" row of our table.

**The Legend of Zelda: Breath of the Wild (2017).** Here you can climb almost any surface, but climbing drains the stamina wheel, and when it runs out you let go. In our model that gives climbing its own limit, a **maximum continuous climb** `h_max = v_climb × (stamina seconds)`. Breath of the Wild's 15 Sheikah Towers are built for this. Their walls are climbable, with platforms between sections where Link can rest. The platforms do for the climb what our Ledge did for the drop. They cut one edge too long to use into shorter ones that fit the player's limit. And the reward at the top is information, not items. Activating a tower gives you the detailed map of the area around it, which is the "high ground sees more" asymmetry from section 1 turned into a game system.

Three games, one idea. Every vertical edge has a price in each direction (seconds, health or stamina), and the designer decides which direction is cheap.

### Design judgment, eyes open

A high return ratio is not a bug by itself. It is a commitment device.

- **Use one-way drops when you want commitment.** A drop into a boss arena, a pit you enter to find a secret, the one-way descent into the final dungeon. The player knows there is no going back, and that raises the stakes. Signal it. Players should be able to see it's one-way before they jump.
- **Don't use them where players need to go back.** Quest-givers, vendors, the corpse you need to reach after dying. A 7× return ratio on a route the player will walk ten times is ten small punishments. Week 1's recovery time `r` includes this walk. A one-way drop between a checkpoint and a hard fight multiplies the penalty ratio.
- **Unlock the return from the far side.** It guarantees the player has seen the long route once, turns the shortcut into a reward, and gives you a moment to show the hub from a new angle.
- **Watch accidental ledges.** The Ledge in our level could be a rock you placed for decoration. Any foothold within `h_safe` of the level below is a potential one-way edge. Your level has more of them than you drew. Week 13 builds the metrics (jump height, step height, `h_safe`) that let you find them on purpose.

The alternatives each have a cost. Make every drop reversible (ladders everywhere) and height stops being exciting. Kill players on every drop over `h_safe` and they stop exploring edges. Price drops in health, the way Minecraft does, and players will make the trade you didn't expect, taking a painful drop to save a long walk. None of these is correct. Pick one per region and apply it the same way everywhere, so players can learn it.

## 3. Breaking height into steps

Section 2 gives you two limits. Players can safely drop `h_safe`, and they can climb at most `h_max` without resting (for games with stamina) or at most one ladder per edge. Any vertical gap larger than the limit needs intermediate footholds.

For a gap of total height `H`, the number of footholds needed is:

```
drops:   footholds = ceil(H / h_safe) − 1
climbs:  rests     = ceil(H / h_max) − 1
```

With `h_safe = 8`, a 12 m cliff needs `ceil(1.5) − 1 = 1` ledge. A 30 m cliff needs `ceil(3.75) − 1 = 3`. If climbing stamina lasts 10 seconds at 1.5 m/s, then `h_max = 15` m, and a 40 m tower needs `ceil(2.67) − 1 = 2` rest platforms.

This formula is a design tool in both directions:

- **To allow a route**, place footholds at intervals at or below the limit. Players read a staircase of ledges as an invitation.
- **To forbid a route**, make sure no gap fits the limit. If you want a cliff to be a wall, check there's no stray rock, crate or roof edge that splits it into legal steps. Players find these. Speedrunners find them faster.

The same gap can be one-way in one direction and blocked in the other. A 7 m wall with `h_safe = 8` and no ladder can be dropped down and not climbed. That is the most common one-way edge in 3D games, and you now know how to spot it on a greybox.

## 4. Navigating in three dimensions

Height also makes levels harder to read. Four problems come up again and again, each with a standard fix.

**Stacked spaces hide each other.** A top-down map shows one floor at a time. Two rooms directly above each other look like one room. The fix is to break the map into floors, show the current floor strongly and the others faintly, and mark vertical connections (stairs, lifts, holes) with the same icon on both floors. Test it by asking a playtester to point, on the map, to the room directly below them.

**Landmarks vanish when you drop.** A landmark visible from the clifftop may be hidden behind the cliff once you're at its foot. [Week 4](w04-guiding-the-player-landmarks-light-weenies.md) treats landmarks in depth. For vertical levels, check each landmark from both the high and low positions. A good vertical landmark is tall enough to be seen over the cliff edge from below, so a player at the Ruin can still point toward the Camp.

**The view from above is a preview.** An overlook where the player can see the space below before descending does the same job as a map. Put the overlook just before the one-way drop. The player sees the Ruin, the Gate and the trail home before committing, so the return route is known before it is needed. This is also where you show the locked end of the future shortcut, so the player will recognise it from below.

**Vertical sightlines change combat.** A player above can see and shoot down more easily than a player below can see up. Week 6 covered cover and lanes on a flat plan. In section it is the same analysis. The high position sees over low cover, the low position doesn't. If a high point overlooks a respawn or a chokepoint, it will be camped. Week 12 measures that with sightline heatmaps.

## In-class activity (25 minutes)

Work in pairs with squared paper and the interactive.

1. (5 min) Draw a side section of a two-level space: a town on a plateau 20 m up and a mine entrance on the valley floor. Use `h_safe = 8` m, climb 1.5 m/s, gravity 20 m/s², run 6 m/s.
2. (10 min) Design the descent so the fastest out trip is under 15 s. Place ledges using the foothold formula. Then design the long way home, and compute the return ratio with no shortcut.
3. (5 min) Add one shortcut, unlocked from the mine end. Choose its type (ladder, lift at a speed you pick, climbable wall) and compute the new return ratio. Target: under 2.
4. (5 min) Swap sheets with another pair. Find one accidental ledge or one gap that fits the limit and makes an unintended route.

Expected output: a side section with times on every edge, three numbers (out time, return ratio before, return ratio after), and the accidental route your partners found.

## Common misconceptions

- **"Distance on the map is travel time."** Only on flat ground. A 12 m cliff is 12 m on the section and zero metres on the plan, and it costs 1.1 s one way (if the drop were safe) and 8 s the other.
- **"A shortcut should make the out trip faster."** The shortcuts players remember make the return faster. The out trip was already the one they chose.
- **"If players can't climb it, it's a wall."** Only if no gap in it fits within `h_safe`. Otherwise it's a one-way door, downward.
- **"Taller ladders are just longer ladders."** Asymmetry grows with the square root of height. The ratio for 12 m is about 7.3, compared with 5.2 for 6 m, so taller edges are more one-sided, and with stamina they may need rest points.

## Check yourself

1. With `g = 20` and `v_climb = 1.5`, what is the asymmetry ratio of a 10 m edge? What climb speed would bring it down to 3?
2. In the Cliff Ruin with the ledge, the trail up is regraded so uphill speed is 5 m/s. What is the new return ratio with no ladder?
3. A designer wants a 36 m cliff to be descendable by ledges with `h_safe = 8`. How many ledges are needed? If one ledge is removed, what happens to the route?
4. In Minecraft, a player drops down 15 blocks into a cave instead of placing a ladder. How much health do they lose? How many such drops can they take in a row from full health without healing?

<details>
<summary>Answers</summary>

1. `sqrt(20 × 10 / 2) / 1.5 = sqrt(100) / 1.5 = 10 / 1.5 = 6.67`. For a ratio of 3: `v_climb = 10 / 3 = 3.33` m/s.
2. The trail up takes `150 / 5 = 30` s, so the back trip is `10 + 30 = 40` s. The out trip is still 6.55 s. Return ratio `40 / 6.55 ≈ 6.11`. Regrading the trail helps a little. It doesn't fix the stranding. Only a new edge does.
3. `ceil(36 / 8) − 1 = ceil(4.5) − 1 = 4` ledges, which split it into five drops of 7.2 m each. Remove one and two of the steps merge into a 14.4 m gap, which is over `h_safe`, so that step is no longer an edge. The whole descent route stops existing, unless a player accepts the damage.
4. `floor(15 − 3) = 12` health. From 20, one drop leaves 8. A second drop would need 12 more, so it kills. Only one.

</details>

## Lab / assignment hook

[Lab 07, return ratios in a vertical level](../labs/lab07.md). You implement the edge-time functions and the shortest-path search, load a larger level (the Quarry, eight nodes and four levels of height), find which of its places strand the player, test four candidate shortcuts, and then design your own fix, because no single candidate brings every return ratio under 2. It counts toward the blockouts component. Keep your code, because return ratios come back in week 10, when hubs and spokes are gated and unlocked.

## Sources

- FromSoftware, *Dark Souls* (2011). The world is described as a single interconnected space linked by unlockable shortcuts in Wikipedia, "Dark Souls (video game)" (accessed September 2026). The Undead Parish to Firelink Shrine elevator, which becomes operational after it is activated from the Parish, is documented on the Dark Souls Wiki (Fandom), "Undead Parish".
- Minecraft Wiki, "Damage" (Java Edition, 1.21 era, fall damage section). Fall damage is `max(0, floor((fall distance − safe_fall_distance) × fall_damage_multiplier))`, with a 3-block safe distance and 1 health per block for players, and a 20-health player needing a drop of about 23.5 blocks to die.
- Minecraft Wiki, "Ladder" (Java Edition). Climbing speed about 2.35 blocks per second, descending speed about 3 blocks per second.
- Zelda Wiki, "Sheikah Tower" and "Stamina Wheel" (*Breath of the Wild*, 2017). Fifteen towers; climbable walls with platforms between sections for resting; activating a tower gives the detailed map of the surrounding area; climbing drains stamina.
- Wikipedia, "The Legend of Zelda: Breath of the Wild" (accessed September 2026). Activating towers reveals map territory.
- Totten, C. (2019). *An Architectural Approach to Level Design* (2nd ed.). A K Peters/CRC Press. Chapters 4 and 6 (doi:10.1201/9781351116305-4 and -6; titles checked on Crossref, September 2026).
- Dijkstra, E. W. (1959). "A note on two problems in connexion with graphs." *Numerische Mathematik* 1, 269-271. The shortest-path method used in section 2.

## Interactive spec: examples/w07-drop-and-climb.html

**The one insight.** A single ledge can make the trip down five times faster without changing the trip back at all. The return ratio, not the out time, tells you whether a vertical route strands players, and one shortcut at the bottom fixes it.

**Layout.** Two linked views. On narrow screens they stack, section on top.

- **Left: side section of the Cliff Ruin.** Horizontal axis is plan distance (not to scale is fine, but keep order: Gate at left on the valley floor, Ruin right of it, cliff face, Camp and Overlook on the clifftop at 12 m). Draw the Ledge at 6 m on the cliff face when enabled. Nodes are labelled circles. Edges are arrows; one-way edges have a single arrowhead, two-way edges have two. Unsafe drops (height over `h_safe`) are drawn as a dashed red line with an "unsafe" label and are not usable. The shortest out route (Camp to Ruin) is highlighted in the accent colour; the shortest back route (Ruin to Camp) in the second colour.
- **Right: two horizontal bars**, "Out: Camp to Ruin" and "Back: Ruin to Camp", on a shared axis 0 to 60 s. Under them, large text "Return ratio 7.25" with a colour band: under 2 green, 2 to 4 amber, over 4 red (use palette tokens, and also show the band as a word, "fair", "long", "stranded", so colour is not the only cue).
- Under the bars, a table listing every usable edge with its time to two decimals, updated live.

**Controls.**
- Toggle "Ledge at 6 m" (default on).
- Toggle "Ladder Ruin → Overlook unlocked" (default off).
- Slider climb speed `v_climb`, 0.5 to 3.0 m/s, step 0.1, default 1.5.
- Slider gravity `g`, 10 to 40 m/s², step 1, default 20.
- Slider safe drop height `h_safe`, 4 to 14 m, step 0.5, default 8.
- Slider uphill trail speed `v_up`, 2 to 6 m/s, step 0.5, default 4.
- Reset button.

**Formulas.** Run `v = 6` fixed. Edges: Camp↔Overlook `30/6`; Ruin↔Gate `60/6`; Camp→Gate `150/6`; Gate→Camp `150/v_up`; Overlook→Ledge and Ledge→Ruin `sqrt(2·6/g)` if `6 ≤ h_safe`, else not an edge; Overlook→Ruin `sqrt(2·12/g)` if `12 ≤ h_safe`, else not an edge; Ruin→Overlook `12/v_climb` if ladder unlocked. Shortest paths by Dijkstra over the directed graph (5 nodes, so any correct method works). Return ratio = back / out.

**Test values** (check to one decimal):
- Defaults, ledge on, ladder off: out 6.5, back 47.5, ratio 7.25.
- Ledge off, ladder off: out 35.0, back 47.5, ratio 1.36.
- Ledge on, ladder on: out 6.5, back 13.0, ratio 1.98.
- Ledge on, ladder on, `v_climb = 0.5`: out 6.5, back 29.0, ratio 4.43.
- Ledge off, `h_safe = 12`: out `5 + sqrt(1.2) = 6.1`, back 47.5, ratio 7.79.
- Ledge on, `h_safe = 5`: drops unsafe, out 35.0, back 47.5.

**Accessibility.** All controls keyboard operable with visible focus. Route highlights use both colour and line style (solid out, dotted back). Numbers in text next to the bars. Respect `prefers-reduced-motion` (no animated route tracing when set; otherwise a short dot animation along each route is fine) and `prefers-color-scheme`.

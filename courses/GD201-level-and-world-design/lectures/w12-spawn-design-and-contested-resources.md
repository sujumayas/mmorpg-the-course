# GD201 · Week 12 — Spawn design and contested resources

**Why this matters:** A spawn point is the one place on your map where you know a player will appear, and so does everyone who wants to kill them. A resource node is the one place where players who want the same thing are forced to meet. Both are geometry problems before they are balance problems. If you can measure how exposed a spawn is and how fast a resource refills, you can stop spawn camping and resource fights at the blockout stage instead of patching them after launch.

**You will be able to:**
- Compute the sightline exposure of any cell on a grid map, and read a whole-map exposure heatmap to find where a spawn is safe.
- Compute the number of camp positions that cover every exit of a spawn, and redesign a spawn room to bring it down.
- Compute the time a contested kill quest or gathering task takes from spawn count, respawn time and the number of competing players, and find the population at which supply, not skill, sets the pace.
- Critique spawn and resource rules in shipped games (respawn waves, moving spawns, per-player nodes) by the term of the model each one changes.

**Before class:** Christopher Totten, *An Architectural Approach to Level Design* (2nd ed., CRC Press, 2019). Use the index entries for "spawn" and "sightline" and read those passages (about 10 pages). Team Fortress 2 Wiki, "Respawn" (10 minutes; note the wave rules). Old School RuneScape Wiki, "Runite rocks" (5 minutes).

**Prerequisites from earlier courses:** [MA101 week 14, distances and ranges](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w14-distances-ranges-and-squared-distance.md) (the squared-distance range test used here). [MA101 week 13, dot product and vision cones](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w13-dot-product-facing-and-vision-cones.md) (a cone decides *where* someone looks; this week decides whether walls let them see at all). Looking ahead, [MMO305 week 8, griefing](../../MMO305-social-systems-and-online-behaviour/lectures/w08-griefing-typology-and-design-responses.md) (year 3) treats spawn and corpse camping as grief play and sorts design responses by the parameter they change. [GD102 week 7, internal economies](../../GD102-systems-design-and-game-mechanics/lectures/w07-internal-economies-sources-drains-converters.md) (a respawning node is a source with a fixed rate). From this course, [week 11, shared spaces](w11-shared-spaces-designing-for-many-players.md) (neighbours at a camp and competitive versus cooperative camps). [Week 6, combat spaces: cover, lanes and chokepoints](w06-combat-spaces-cover-lanes-chokepoints.md), covered cover in a fight. This week asks where the fight should never start.

**Interactive:** [`examples/w12-spawn-sightlines.html`](../examples/w12-spawn-sightlines.html). Keep it open during section 2.

---

## 1. The two places everyone knows about

Most of a level is uncertain for a hunter. The prey could be anywhere. Two kinds of place remove that uncertainty.

A **spawn point** is where a player enters or re-enters the world: at the start of a match, after death, or after a loading screen. In an MMO the equivalent is the **graveyard** or respawn point where a dead character comes back. A spawn is a promise that someone will appear here soon.

A **contested resource** is anything that several players want and that runs out when one of them takes it: a monster whose kill counts for only one player, an ore node that disappears when mined, a rare boss that appears once an hour. A resource location is a promise that other players will be here too.

**Spawn camping** is waiting at or near an enemy spawn and killing players as they appear, before they can act. It is one of the oldest complaints in multiplayer games. The Team Fortress 2 Wiki describes spawn camping as a kind of camping that ruins the game's enjoyment. It is also a form of grief play (MMO305 week 8) when the camper's main gain is the victim's frustration. Resource fights are its slower cousin. Nobody dies, but players wait, and waiting feels like being punished for showing up.

Both problems come down to numbers you can compute from a map: how many places can see this spot, and how fast does this spot refill?

## 2. Worked example: spawn camping as geometry

### The hook

In Team Fortress 2 (Valve, 2007), you don't come back the moment you die. Players respawn in **waves**. Most official maps use a 10-second wave, and a dead player joins the wave after the next one, so they return between 10 and 20 seconds after death. Everyone who died at about the same time walks out of the spawn room together. Capture-the-flag maps often use spawn rooms whose doors open only from the inside. On control-point maps, which spawn room your team uses often depends on which points it holds, so the spawn moves forward as the team advances.

Each rule answers the same threat. A spawn is a target that everyone knows about. The wave means campers face a group, not one player at a time. The one-way door keeps the enemy out. The moving spawn keeps the fight from settling on the same doorway all game. But none of those rules help if the spawn room's exit can be watched from half the map. That part is geometry, and it is your job.

### The model

Lay the map on a grid (week 2's blockout grid is ideal). Every cell is either open floor or wall. Two cells **see** each other if the straight line between their centres crosses no wall cell, and they are within range `R` (the distance at which a weapon or a threat matters, in cells).

The **exposure** of a cell `p` is the number of open cells that see it:

```
E(p) = number of open cells c ≠ p  with  |c − p| ≤ R  and  line of sight from c to p
```

- `R` is the threat range in cells.
- `|c − p|` is the ordinary distance between cell centres. Test it as `dx² + dy² ≤ R²` (MA101 week 14).
- Line of sight means no wall cell lies on the segment from the centre of `c` to the centre of `p`.

Line of sight is symmetric. If `c` can see `p`, then `p` can see `c`. So `E(p)` is also the number of places a camper could stand to shoot a player standing at `p`.

Compute `E` for every open cell and colour the map by it, and you have an **exposure heatmap**: bright where many places can see you, dark where few can. A spawn belongs in the dark.

One number for the spawn cell isn't enough, because players don't stay on the spawn cell. They leave through **exits**, the cells where the spawn area meets the shared map. A camper who can see every exit at once doesn't need to see the spawn. So the second number is:

```
K = number of open cells outside the spawn area that see every exit
```

`K` is the number of **camp positions**: places where one enemy covers every way out. A good spawn has a low `E` at the spawn cell and a low `K`.

For the line-of-sight test, walk along the segment from one centre to the other in quarter-cell steps and check which cell each step lands in. It is simple and good enough for a blockout grid. Your engine will use raycasts against real geometry, but the numbers behave the same way.

### Numbers you can check

Start with a map you can count by hand. An open 9 × 9 arena with no inner walls, spawn in the centre, `R = 4`. Every cell within 4 of the centre can see it. That is every grid point inside a circle of radius 4, which is 49 points, minus the spawn itself: `E = 48`. If you place the spawn next to a wall, cells behind the wall drop out, and `E` falls.

Now the teaching map for this week. It is 17 cells wide and 13 tall, with `x` counted from 0 at the left and `y` from 0 at the top. It has a large plaza at the top, a lower courtyard, a side room on the left and a closet at the end of a corridor on the right. Three spawn candidates are marked:

```
#################
#...............#
#...............#
#.......A.......#
#...............#
#...##.....##...#
#...#.......#...#
#...#.......#...#
##.##..###..#####
#B..#.......#..C#
#...........#.###
#...#...........#
#################
```

- **A** stands in the middle of the plaza, at (8, 3).
- **B** stands in the corner of the side room, at (1, 9). The room has two exits: a door to the east at (4, 10) and a gap to the north at (2, 8).
- **C** stands at the end of the closet, at (15, 9). Its only way out is round two corners to the door at (12, 11).

With `R = 8`:

| Spawn | `E` at the spawn | Exits | `E` at each exit | Camp positions `K` |
|---|---|---|---|---|
| A, plaza | 90 | none (already in the open) | 90 | 90 |
| B, side room, two exits | 16 | 2 | 38 and 34 | 2 |
| B, north gap walled up | 14 | 1 | 36 | 28 |
| C, closet | 2 | 1 | 25 | 21 |

Read the table in order.

**A is the worst spawn on the map.** Ninety cells can see it. Anyone who walks into the plaza can shoot a player who has just appeared. The heatmap shows the plaza as the hottest area. Nobody should spawn there.

**C looks like the best, and it isn't.** Only 2 cells can see the spawn itself, the lowest on the map. But C has one exit, and 21 cells can see that exit. One camper on any of them catches every player who leaves, one after another. A spawn with one exit is a spawn with a queue.

**B with two exits is the best spawn.** Its spawn cell is almost as hidden as C's (16), and its two exits face different parts of the map. Only 2 cells outside the room see both exits at once, at (1, 7) and (5, 11). They sit on a diagonal that happens to run through both doorways. Wall up the north gap and B becomes a one-exit spawn like C: `K` jumps from 2 to 28.

That last row is the lesson. **What makes a spawn campable is the number of places that cover every way out, not how hidden the spawn point is.** A spawn cell in a dark corner is useless if its only door is bright.

The code that produced the table:

```python
import math

MAP = """
#################
#...............#
#...............#
#.......A.......#
#...............#
#...##.....##...#
#...#.......#...#
#...#.......#...#
##.##..###..#####
#B..#.......#..C#
#...........#.###
#...#...........#
#################
""".split()

WALL = {(x, y) for y, row in enumerate(MAP) for x, ch in enumerate(row) if ch == "#"}
OPEN = [(x, y) for y, row in enumerate(MAP) for x, ch in enumerate(row) if ch != "#"]

def los(a, b):
    """Walk the segment between cell centres in quarter-cell steps; any wall blocks it."""
    (x0, y0), (x1, y1) = a, b
    n = max(1, 4 * max(abs(x1 - x0), abs(y1 - y0)))
    for i in range(n + 1):
        t = i / n
        cell = (math.floor(x0 + (x1 - x0) * t + 0.5), math.floor(y0 + (y1 - y0) * t + 0.5))
        if cell in WALL:
            return False
    return True

def sees(c, p, R):
    return c != p and (c[0] - p[0])**2 + (c[1] - p[1])**2 <= R * R and los(c, p)

def exposure(p, R=8):
    """E(p): open cells within range R that have line of sight to p."""
    return sum(sees(c, p, R) for c in OPEN)

def camp_cells(exits, room, R=8):
    """K: cells outside the spawn room that see every exit at once."""
    return sum(all(sees(c, e, R) for e in exits) for c in OPEN if c not in room)

room_B = {(x, y) for x in (1, 2, 3) for y in (9, 10, 11)}
room_C = {(13, 9), (14, 9), (15, 9), (13, 10), (13, 11), (14, 11), (15, 11)}
print("A", exposure((8, 3)), camp_cells([(8, 3)], set()))
print("B", exposure((1, 9)), exposure((4, 10)), exposure((2, 8)),
      camp_cells([(4, 10), (2, 8)], room_B))
print("C", exposure((15, 9)), exposure((12, 11)), camp_cells([(12, 11)], room_C))
```

It prints:

```
A 90 90
B 16 38 34 2
C 2 25 21
```

The letters A, B and C are open cells too (the code treats anything that isn't `#` as floor).

Open the interactive. The left panel is the map with the chosen spawn, its exits, and every cell that sees the spawn highlighted. The right panel is the exposure heatmap for the whole map. Click A, B and C in turn and watch `E` and `K` change. Then click the north gap of B's room to wall it up. The two camp cells on the left panel become 28, spread across the lower courtyard. Drag the range slider from 4 to 16 and notice that the plaza gets hotter while the closet stays dark. Long range punishes open spawns most.

### Cross-game recognition

**Team Fortress 2 (Valve, 2007 onward).** Its answers each attack a different term. Respawn waves (10 seconds on most official maps, 10 to 20 seconds from death to return) send players out together, so the camper faces a group. Doors that open only from the inside keep the enemy out of the spawn room, so every camp position must be outside it, which is exactly how `K` is defined. On control-point maps, the spawn room in use depends on which points a team holds. The designer changes which exits exist as the match progresses, so no set of camp positions stays useful for long.

**World of Warcraft battlegrounds (2005 onward).** In battlegrounds, dead players return at graveyards, where a Spirit Guide resurrects everyone nearby every 30 seconds with full health and mana. Some battlegrounds have graveyards that either side can capture, and when one changes hands, the ghosts waiting there move to another of their faction's graveyards. The 30-second wave works like TF2's: a group comes out together, on a timer both teams can see. Capturable graveyards make the spawn itself an objective, which turns camping a graveyard into a legitimate strategy with a counter, rather than a trap with none.

**World of Warcraft open world.** Outside battlegrounds, a dead player can accept resurrection from a Spirit Healer at the graveyard, at the price of resurrection sickness, a debuff that cuts attributes and damage dealt by 75% for a time. The graveyard is a spawn with a known location, and the sickness makes a player who spawns there briefly weaker than normal, which is the opposite of spawn protection. It discourages players from using the graveyard casually, and it leaves them exposed to anyone waiting nearby. A world that wants open-world PvP to stay fair needs graveyards with low `E` and several exits.

Three games, one principle. Every rule either lowers exposure (hidden rooms, one-way doors), spreads the targets in time (waves) or moves the exits (moving spawns and capturable graveyards).

### Design judgment, eyes open

- **Measure the exits, not only the spawn.** `E` at the spawn is the number most people check. `K` is the one that decides whether camping works. Two exits that face different areas usually beat any amount of hiding.
- **Don't make the spawn a fortress.** A spawn with `E = 0` and `K = 0` is safe but may be so far from the action that players walk for a minute after every death. Week 1's recovery time `r` applies. Spawn safety and walk-back time trade against each other, and the designer picks the point.
- **Waves help the victims and the campers.** A 30-second wave means defenders come out together, but it also tells campers exactly when to look. Randomized spawn points (TF2 picks among the points in the active spawn area) make the timing less useful.
- **Hard rules are a last resort.** Invulnerability on spawn, damage zones around spawn doors and one-way doors all work, and all tell the player the level couldn't protect them by itself. Get `E` and `K` right first and use hard rules to cover what is left.
- **In an MMO, graveyards are in the shared world.** The same graveyard serves questers and PvP players. A graveyard in an open field is a death trap on a PvP server and harmless on a PvE one. Decide which kind of server the zone will run on before you place it.

## 3. Contested resources: when supply sets the pace

Spawns bring players back. Resources bring players together. Last week you counted neighbours at a camp. This week you put a price on each neighbour at a competitive camp.

### The model

A camp has `M` spawns of the monster a quest needs. Each respawns `T` seconds after it dies. A player needs `k` kills and, with no competition, kills one every `t_k` seconds. `P` players are at the camp, all needing the same monster, with exclusive credit (week 11).

The camp produces at most `M / T` monsters per second in steady state, whatever the players do. Split evenly, each player gets `M / (T × P)` per second. A player can use at most `1 / t_k`. The time to finish is set by whichever rate is smaller:

```
time = k × max(t_k, T × P / M)
```

- When `t_k` is larger, the player's kill speed sets the pace, and more players cost nothing.
- When `T × P / M` is larger, supply sets the pace, and every extra player adds time to everyone's quest.

The crossover is at `P* = M × t_k / T`. Below it, the camp is **skill-limited**. Above it, the camp is **supply-limited**.

This is a source with a fixed rate (GD102 week 7) shared by `P` drains. The model ignores the monsters standing at the camp when the first players arrive, so it describes a camp that has been busy for a while.

### Numbers you can check

A quest needs `k = 10` kills. The camp has `M = 6` spawns, each respawning after `T = 60` seconds. Alone, a player kills one every `t_k = 20` seconds. Then `P* = 6 × 20 / 60 = 2`.

| Players at the camp `P` | `T × P / M` (s per kill from supply) | Limited by | Time for 10 kills |
|---|---|---|---|
| 1 | 10 | skill | 200 s |
| 2 | 20 | either | 200 s |
| 4 | 40 | supply | 400 s |
| 11 | 110 | supply | 1,100 s (18.3 min) |
| 30 | 300 | supply | 3,000 s (50 min) |

The row for 11 is the week 11 teaching zone at its comfortable maximum: each player sees 10 others at the camp. At that population, a 3-minute quest takes over 18 minutes. The camp the population model called "comfortable" is a queue under exclusive credit. That is why week 11 asked you to set `n_max` separately for competitive camps.

The levers are in the formula. To keep the quest at 5 minutes (300 s) for 11 players, you need `T × 11 / M ≤ 30`. With 60-second respawns, that means `M ≥ 22` spawns. With 6 spawns, it means `T ≤ 16.4` seconds. Or change the rules so that `P` no longer divides the supply: shared credit (week 11) lets every player who helps with a kill count it, so the camp stops being a race.

### Cross-game recognition

**Old School RuneScape, mining (current game).** Rocks deplete when mined and respawn after a fixed time, so each rock is a source with rate `1 / T`. An iron rock respawns after 5.4 seconds (2.4 seconds in the members' part of the Mining Guild). A runite rock takes 12 minutes (6 minutes in the Mining Guild). One runite rock can supply at most 5 ore per hour per world, whoever mines it. The Old School RuneScape Wiki notes that the long respawn makes switching between game worlds practically mandatory for collecting any useful amount, and that players and bots compete for the rocks. Players respond to a supply-limited camp exactly as the model predicts. They leave for a copy of the world where `P` is lower. Some keep a timer for when each rock returns, and others mine at rocks behind quest requirements, where fewer players can reach them.

**Guild Wars 2, gathering (current game).** Most resource nodes can be gathered by each character, and each resets for that character a few hours later. In the model, every player has their own `M`, so `P` drops out of the formula. Nobody competes, and the crowd from week 11 costs nothing at a node. The price is that nodes can't create the tension, trade or player-to-player conflict that a scarce shared rock does.

Two games, the same formula, opposite choices. Old School RuneScape keeps `P` in the denominator and lets scarcity push players around the world. Guild Wars 2 removes it and keeps the world friendly.

### Design judgment, eyes open

- **Decide which resources are meant to be fought over.** A rare node that everyone wants creates stories, trade and conflict. The same rule on a quest monster that every new player needs creates only waiting. Keep scarcity for things that are optional and valuable.
- **Compute `P*` for every quest camp.** If the expected `N_camp + 1` from week 11 is above `P*`, the camp is supply-limited at normal population. Add spawns, cut respawn time, spread the monsters, or share credit.
- **Scaling respawn helps and has costs.** Respawn time that falls as more players arrive (`T` proportional to `1 / P`) keeps the quest time flat, but it also creates an endless stream of monsters that suits farming bots. Cap it.
- **Remember the spawn geometry.** A resource camp is a spawn for monsters. Monsters that respawn inside a player's view appear out of nothing. Place spawn points where `E` is low, behind terrain or buildings, so the camp refills where players can't watch it happen.

## In-class activity (25 minutes)

In pairs, with squared paper and the interactive.

1. **(8 min)** Draw a 15 × 11 grid map with a spawn room that has one exit. Using the interactive's edit mode, copy it in and record `E` at the spawn, `E` at the exit and `K`.
2. **(8 min)** Add one wall piece and move one door (no more) to bring `K` below 5 without raising `E` at the spawn above 20. Record the new numbers.
3. **(6 min)** Place a quest camp on the same map with 5 monster spawns in cells where `E ≤ 10`. With `T = 45` s and `t_k = 15` s, compute `P*`. If the zone expects 8 players at this camp, how long does a 12-kill quest take?
4. **(3 min)** Swap maps with another pair and find the best camp position on theirs.

Expected output: the before-and-after table, `P*` and the quest time, and the camp position the other pair found.

## Common misconceptions

- **"A hidden spawn is a safe spawn."** Hiding the spawn cell lowers `E` at the spawn but does nothing for its exits. The closet spawn C has the lowest `E` on the map and 21 camp positions.
- **"More spawn points at a camp are always better."** More spawns raise `M` and shorten supply-limited quests, but each spawn placed in view of players pops into existence in front of them, and a denser camp is harder for a new player to pull one monster from. Place them by `E` as well as by count.
- **"Spawn invulnerability solves camping."** It delays the first shot by a second or two. If `K` is high, the camper is still there when protection ends.
- **"Scarcity is always the economy's job."** The respawn time and the number of nodes are level-design values. Where you place nodes and how many exist decides how many players compete for each one before any economist touches a price.

## Check yourself

1. In an open arena with no inner walls, a spawn sits far from any edge, and `R = 3`. What is `E` at the spawn? Why does `E` drop if you move the spawn next to the arena's wall?
2. On the teaching map, walling up B's north gap raises `K` from 2 to 28, although `E` at the spawn falls from 16 to 14. Explain both changes in terms of which cells see what.
3. A quest needs 8 kills at a camp with 4 spawns that respawn every 90 seconds. Alone, a player kills one every 15 seconds. Is a single player skill-limited or supply-limited? How long does the quest take for 5 players? What respawn time brings it to 5 minutes?
4. A world has 3 runite rocks, each respawning every 12 minutes, and 4 players mining them full time. How many ore per hour does each get? If a second world has the same rocks and 1 player, how many does that player get, and what does the model predict the 4 players will do?

<details>
<summary>Answers</summary>

1. Every grid point within radius 3 of the centre counts: 29 points, minus the spawn itself, so `E = 28`. Next to a wall, the cells beyond the wall are not open floor, so about half the circle is gone and `E` drops to about half.
2. With the gap open, the north gap is a second exit facing the plaza's left alcove, and the east door faces the lower courtyard. Only 2 cells lie on a line through both openings, so `K = 2`. Walled up, the east door is the only exit, and every cell that sees it (28 outside the room) covers every way out. `E` at the spawn falls because the cells in the alcove could see B through the gap, and now they can't.
3. Supply gives `M / T = 4 / 90 ≈ 0.044` monsters per second, less than the `1 / 15 ≈ 0.067` a lone player can kill, so even one player is supply-limited (`P* = 4 × 15 / 90 ≈ 0.67`). For 5 players, `time = 8 × 90 × 5 / 4 = 900` s, 15 minutes. For 300 s: `8 × T × 5 / 4 ≤ 300` gives `T ≤ 30` seconds (check that skill doesn't bind: `8 × 15 = 120` s, so it doesn't).
4. Three rocks at 5 ore per hour each supply 15 ore per hour. Split four ways, that is 3.75 each. The lone player on the second world gets all 15. The model predicts that some of the four will move to the second world until the shares are closer to equal, which is the world switching the Old School RuneScape Wiki describes.

</details>

## Lab / assignment hook

[Lab 12, sightline heatmaps and spawn redesign](../labs/lab12.md). You implement line of sight, exposure, the heatmap and camp positions, reproduce this lecture's table, then redesign a badly placed spawn on a lab map until it meets exposure and camp-position targets. You also place a quest camp and check it against `P*`. Your spawn and camp analysis goes into the final zone's design document.

## Sources

- Team Fortress 2 Wiki, "Respawn" (accessed September 2026). Players respawn in waves; most official maps use a 10-second wave; a dead player joins the wave after the next, returning 10 to 20 seconds after death; the minimum is 5 seconds for teams of 3 or fewer; on Capture the Flag maps, doors to the resupply area often open only from the inside; on Control Point maps, the active respawn area often depends on which points a team holds.
- Team Fortress 2 Wiki, "Camping" (accessed September 2026). Spawn camping described as camping that ruins the game's enjoyment, with examples of stickybombs placed at spawn exits.
- Warcraft Wiki, "Spirit Guide" (accessed September 2026). In battlegrounds, Spirit Guides resurrect players every 30 seconds with full health and mana and no penalty.
- Warcraft Wiki, "Battleground" (accessed September 2026). Some battlegrounds have capturable graveyards; when one is captured, waiting ghosts move to another graveyard of their faction.
- Warcraft Wiki, "Spirit Healer" (accessed September 2026). Resurrection at a Spirit Healer outside battlegrounds applies resurrection sickness, which reduces attributes and damage dealt by 75%.
- Old School RuneScape Wiki, "Iron rocks" and "Runite rocks" (accessed September 2026). Iron rocks respawn in 5.4 seconds (2.4 in the members' Mining Guild); runite rocks in 12 minutes (6 in the Mining Guild); world switching described as practically mandatory for runite, with competition from players and bots.
- Guild Wars 2 Wiki, "Gathering" (accessed September 2026). Most nodes can be used by each character and reset for that character a few hours after gathering.
- Totten, C. (2019). *An Architectural Approach to Level Design* (2nd ed.). CRC Press.

## Interactive spec: examples/w12-spawn-sightlines.html

**Purpose.** This is the course's signature example "Spawn camping as geometry". Make the student see that a hidden spawn cell does not make a safe spawn, that the number of places covering every exit (`K`) is what decides camping, and that one wall piece can change `K` by more than a factor of ten.

**Layout.** Two linked grid views of the same map, side by side on desktop, stacked on mobile (sightlines first).

- **Left view, sightlines from the spawn.** The 17 × 13 teaching map (exact layout in the lecture, `#` wall, `.` floor). The selected spawn cell has a marker. Its exits have door markers. Every cell that sees the spawn (within `R`, with line of sight) is tinted. Every camp position (outside the spawn area, sees every exit) gets a strong outline and a crosshair glyph drawn with SVG shapes (no icons from games).
- **Right view, exposure heatmap.** The same map with every open cell coloured by `E(cell)` on a sequential scale (dark = low, bright = high). Legend with the min and max. Hover or keyboard focus on a cell shows its coordinates and `E`.
- **Readout.** Spawn name and coordinates, `E` at the spawn, the list of exits with `E` at each, and `K`. Table of the three preset spawns (A, B, C) with the same columns, updated live when the map or `R` changes.

**Controls.**
- Spawn selector: buttons A, B, C, plus "Pick a cell" mode (click or Enter on a focused cell).
- For custom spawns: "Mark exits" mode (click cells to toggle them as exits) and "Spawn area" mode (click cells to include them in the spawn area excluded from `K`). Presets define these for A, B, C (A: exit = the spawn cell, area empty; B: exits (4, 10) and (2, 8), area x 1-3, y 9-11; C: exit (12, 11), area (13, 9), (14, 9), (15, 9), (13, 10), (13, 11), (14, 11), (15, 11)).
- "Edit walls" mode: click or Enter toggles wall and floor. Outer border cannot be edited.
- Quick toggle button "Wall up B's north gap" (toggles (2, 8)).
- `R` slider 2 to 16, step 1, default 8.
- Map selector: "Teaching map" (default) and "Open arena" (11 × 11, border walls, open 9 × 9 interior, spawn at (5, 5), exit = the spawn cell).
- Reset.

**Formulas.** Cells indexed `(x, y)` from the top-left, `x` to the right, `y` down. Line of sight from `a` to `b`: `n = max(1, 4 × max(|dx|, |dy|))`; for `i = 0 … n`, `t = i / n`, cell `= (floor(x0 + dx t + 0.5), floor(y0 + dy t + 0.5))`; blocked if any such cell is a wall. `sees(c, p) = c ≠ p` and `dx² + dy² ≤ R²` and line of sight. `E(p) = Σ sees(c, p)` over open cells. `K = number of open cells outside the spawn area that see every exit`. Compute the heatmap once per change (221 cells × 221 cells is fine in plain JavaScript).

**Test values** (teaching map, `R = 8`):
- A (8, 3): `E = 90`, `K = 90`.
- B (1, 9): `E = 16`; exits `E(4, 10) = 38`, `E(2, 8) = 34`; `K = 2`, the camp cells are (1, 7) and (5, 11).
- B with (2, 8) walled: `E = 14`, `E(4, 10) = 36`, `K = 28`.
- C (15, 9): `E = 2`, `E(12, 11) = 25`, `K = 21`.
- Heatmap maximum 90 at (8, 2) and (8, 3).
- Open arena, `R = 4`, spawn (5, 5): `E = 48`. With `R = 3`: `E = 28`.

**The one insight.** On first load, show spawn C selected: the left view is almost empty of tint around the spawn (`E = 2`) while the readout shows `K = 21` and the camp cells light up at the corridor mouth. The student should see immediately that "hidden" and "safe" are different numbers, then click B and see `K = 2`.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. The heatmap scale must stay legible in dark mode and not rely on hue alone (use lightness). Camp cells use outline plus glyph, not colour only. All grid cells reachable by arrow keys once the grid has focus. No animation needed; if the heatmap fades in, disable under `prefers-reduced-motion`.

# GD201 · Week 14 — Playtesting levels with heatmaps

**Why this matters:** A heatmap is the most persuasive picture in a level review. One red blob and the room agrees something is wrong there. Often the room is wrong. A plain death map mostly shows where players spend their time, and with a small playtest it also shows where one unlucky tester fell. This week you learn to build a heatmap that points at the real problem, and to tell when a map is too thin to trust.

**You will be able to:**
- Compute death counts, raw death rates and shrunk death rates per cell from position and death events, and explain why they rank cells differently.
- Choose the strength of shrinkage `k` and a cell size for a playtest of a given size, using the standard error of a rate.
- Critique a published or team heatmap for missing denominators, attrition and small samples.
- Plan a telemetry-backed playtest of a level: which events to log, which maps to draw, and what to pair them with to learn why.

**Before class:** Clive Thompson, "Halo 3: How Microsoft Labs Invented a New Science of Play" (Wired 15.09, August 2007), the pages on Bungie's test lab and the Valhalla and Jungle examples. Valve, "Episode Two Stats" (steampowered.com, archived 2008-2009), the page as a whole. Reread GD101 week 7 on observing without explaining.

**Prerequisites from earlier courses:** [GD101 week 7, playtesting](../../GD101-introduction-to-game-design/lectures/w07-playtesting-observe-dont-explain.md) (observe behaviour, don't coach). [MA102 week 12, descriptive statistics for playtests](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md) (section 4, counts need a denominator). [MA102 week 13, sampling and confidence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (standard error of a rate, the Wilson interval). [UX201 week 8, usability testing methods](../../UX201-game-ux-and-player-psychology/lectures/w08-usability-testing-methods.md). [GD201 week 2](w02-blockout-and-greyboxing.md) (test rounds and the discovery rate `f`). [GD201 week 12, spawn design](w12-spawn-design-and-contested-resources.md) computed a sightline heatmap from geometry. This week's heatmaps come from players. Logging the events is covered next semester, in [DB201 week 10, telemetry design](../../DB201-data-persistence-and-telemetry/lectures/w10-telemetry-design-events-and-properties.md).

**Interactive:** [`examples/w14-death-heatmap.html`](../examples/w14-death-heatmap.html). Keep it open during section 2.

---

## 1. What a level heatmap is

A **heatmap** is a top-down map of a level with a colour on each place showing how much of something happened there. The something is an **event**, a record your game writes while someone plays. For level work, the useful events are few:

- **Position samples.** The player's position every second or so. From these you get where players go and how long they stay.
- **Deaths.** Where the player died, what killed them, and ideally where the killer stood.
- **Progress events.** Checkpoints reached, objectives completed, doors opened.
- **Quits.** Where the session ended without finishing.
- **Interactions.** Pickups taken, switches used, secrets found.

Each event carries at least the player, the run (one attempt at the level), the time, the position and the build number. The build number matters more than it looks. A heatmap that mixes last week's layout with this week's shows neither.

There are three common ways to draw events.

1. **Dot plot.** One dot per event. Honest and fast, but a thousand dots on top of each other look like ten.
2. **Binned map.** Divide the floor into square **cells** and count the events in each. This lecture uses binned maps, because every cell has a number you can check.
3. **Smoothed map.** Spread each event over nearby cells with a soft bump and add up the bumps. It looks nicer and hides the numbers. Treat it as a binned map with blurry edges.

A heatmap tells you *where*. It rarely tells you *why*. Keep that in mind through the whole lecture. Section 4 returns to it.

## 2. Worked example: where is the level really dangerous?

### The hook

In October 2007 Valve shipped Half-Life 2: Episode Two with a reporting system that sent anonymous play data back to the company. Valve then published a public stats page. Between October 2007 and September 2008 it recorded over four million play sessions. The page included a **death map** for each of the game's maps, coloured, in Valve's words, by where players died most often. Valve posted the same kind of death maps for eight Team Fortress 2 multiplayer maps on its stats pages.

Look at a death map like that and your eye goes straight to the hottest spot. The natural reading is "this is the most dangerous place in the level." Is it?

Not necessarily. A spot can be hot because it is deadly, or because every player walks through it. The main corridor of a level collects deaths the way the busiest road in a city collects accidents. A side room that kills half the people who enter can stay pale if only a handful ever enter it. A death map without a denominator mixes two questions: where players are, and how dangerous each place is. You want the second.

### The model

Divide the level into cells. For each cell `i`, count:

- `d_i`, the number of **deaths** in the cell.
- `v_i`, the number of **visits**: how many times a player entered the cell during a run. A player who leaves and comes back makes two visits.

The **raw death rate** `d_i / v_i` is the chance of dying per visit. It answers the right question, and it is badly behaved when `v_i` is small. One death in two visits reads as 50%.

The fix is to pull every cell's rate toward the level's average by an amount that depends on how much data the cell has. Let `r̄` be the level-wide rate, total deaths divided by total visits. Then the **shrunk death rate**, the value we colour each cell by, is:

```
heat_i = (d_i + k × r̄) / (v_i + k)
```

- `k` is the **prior strength**, measured in visits. Read it as "pretend every cell already had `k` visits at the level's average rate before the playtest began."
- When `v_i` is much larger than `k`, the pretend visits don't matter and `heat_i` is close to the raw rate.
- When `v_i` is much smaller than `k`, the cell has too little data to move far from `r̄`, and `heat_i` stays near the average.
- `k = 0` gives the raw rate. A very large `k` paints every cell the same colour.

This is the only formula in the lecture. It is a weighted average of the cell's own rate and the level's rate, with weight `v_i / (v_i + k)` on the cell's own data. Statisticians call it shrinkage, or additive smoothing. You met the same problem in MA102 week 13 as the width of a confidence interval. The standard error of a rate `r` measured from `v` visits is `sqrt(r(1 − r) / v)`, so a rate from 4 visits is five times noisier than one from 100.

### Numbers you can check

An invented level, "Quarry", tested by 30 players. It has six zones. Totals are 1,000 visits and 100 deaths, so `r̄ = 0.1`. Use `k = 20`.

| Zone | Visits `v` | Deaths `d` | Rank by count | Raw rate `d/v` | Standard error | Shrunk `(d + 2) / (v + 20)` | Rank by shrunk rate |
|---|---|---|---|---|---|---|---|
| Corridor | 400 | 28 | 2 | 0.070 | 0.013 | 0.071 | 5 |
| Bridge | 250 | 30 | 1 | 0.120 | 0.021 | 0.119 | 4 |
| Sniper yard | 100 | 25 | 3 | 0.250 | 0.043 | 0.225 | 1 |
| Vent | 10 | 4 | 5 | 0.400 | 0.155 | 0.200 | 2 |
| Spawn room | 236 | 11 | 4 | 0.047 | 0.014 | 0.051 | 6 |
| Lift | 4 | 2 | 6 | 0.500 | 0.250 | 0.167 | 3 |

Check the sniper yard by hand. `k × r̄ = 20 × 0.1 = 2`. `(25 + 2) / (100 + 20) = 27 / 120 = 0.225`. And the lift: `(2 + 2) / (4 + 20) = 4 / 24 = 0.167`.

Three maps, three different answers to "where is the problem?"

- **By count**, the bridge is hottest with 30 deaths. But 250 visits pass through it, and its rate of 12% is only a little above the level's 10%. The count map is mostly a traffic map.
- **By raw rate**, the lift is hottest at 50%. That is two deaths in four visits, with a standard error of 25 points. One more safe ride and it drops to 40%. The raw map is mostly a noise map.
- **By shrunk rate**, the sniper yard is hottest. A player who enters it has about a one-in-four chance of dying there, measured over 100 visits. That is the zone to look at first. The vent comes second, flagged as worth a closer look but not yet proven.

You can reproduce the table with this code:

```python
zones = {                  # name: (visits, deaths) from one playtest
    "Corridor":    (400, 28),
    "Bridge":      (250, 30),
    "Sniper yard": (100, 25),
    "Vent":        (10, 4),
    "Spawn room":  (236, 11),
    "Lift":        (4, 2),
}
V = sum(v for v, d in zones.values())
D = sum(d for v, d in zones.values())
r_bar = D / V                                   # level-wide death rate per visit

def heat(v, d, k):
    """Death rate per visit, pulled toward r_bar by k pretend visits."""
    return (d + k * r_bar) / (v + k)

print(f"level rate r_bar = {D}/{V} = {r_bar:.3f}")
for name, (v, d) in zones.items():
    print(f"{name:12s} count {d:3d}  raw {d / v:.3f}  k=20 {heat(v, d, 20):.3f}")
for k in (0, 5, 20, 100):
    order = sorted(zones, key=lambda z: -heat(*zones[z], k))
    print(f"k = {k:3d}: hottest first -> {', '.join(order[:3])}")
```

```
level rate r_bar = 100/1000 = 0.100
Corridor     count  28  raw 0.070  k=20 0.071
Bridge       count  30  raw 0.120  k=20 0.119
Sniper yard  count  25  raw 0.250  k=20 0.225
Vent         count   4  raw 0.400  k=20 0.200
Spawn room   count  11  raw 0.047  k=20 0.051
Lift         count   2  raw 0.500  k=20 0.167
k =   0: hottest first -> Lift, Vent, Sniper yard
k =   5: hottest first -> Vent, Lift, Sniper yard
k =  20: hottest first -> Sniper yard, Vent, Lift
k = 100: hottest first -> Sniper yard, Vent, Lift
```

The last four lines show how the ranking responds to `k`. With no shrinkage the tiny zones win. By `k = 20` the ranking has settled, and raising `k` to 100 doesn't change the top three. When the top of the ranking stops moving as you raise `k`, you can trust it.

### The visual

Open [`examples/w14-death-heatmap.html`](../examples/w14-death-heatmap.html). It shows an invented level from above, with a simulated playtest. The left map is coloured by death count. The right map is coloured by the rate you choose: raw or shrunk. Start with 30 testers and `k = 20`. The left map lights up the main corridor and the bridge. The right map lights up the sniper yard, a side area that a quarter of the testers pass through.

Now set testers to 5 and the right map to raw rate. It breaks into speckles. Its hottest cells are often ones with a death or two in a handful of visits, scattered wherever a few testers happened to die, and on many seeds they are not in the yard at all. Switch to shrunk and the speckles fade toward the average while the yard stays warm. Finally raise testers to 300. All three maps begin to agree on where the danger is, and the count map still shows the corridor, because traffic is still traffic.

### Cross-game recognition

**Halo 3, Valhalla (Bungie, 2007).** Wired's 2007 feature on Bungie's test lab describes a death heatmap of Valhalla, one of Halo 3's multiplayer maps, from testing that April. Deaths skewed toward the base on one side, which told the designers that the team attacking from the other side had a slight advantage. They adjusted the terrain to even it out. Rewrite it in our model and you see why a count map worked there. Valhalla has two mirrored halves, and both teams play equally long matches, so the denominator is roughly the same on both sides by design. When the exposure is equal, counts compare fairly. That is a special case worth recognising. In most levels, exposure is not equal.

**Halo 3, Jungle (Bungie, 2007).** The same article shows the other main kind of map. For the first campaign level, the lab plotted where about 30 testers were after half an hour of play. The dots were scattered all over the terrain. Players were lost. Bungie changed the geography to stop players backtracking, and in a later test the dots, coloured by timestamp, clustered in order along the route. This is a position map, not a death map, and its denominator is time. The question "where are players after 30 minutes?" is answered by the fraction of testers in each area, which is a rate.

**Half-Life 2: Episode Two (Valve, 2007-2008).** Valve's stats page also shows the danger of comparing across maps. It reports that 47.54% of players reached the final map and 44.22% completed the game. So the last map was played by fewer than half as many people as the first. A raw death count on the last map starts at a disadvantage of more than two to one. Valve's page presented deaths per map as an average, which divides by players. That is the right denominator for comparing maps, the same way visits are the right denominator for comparing cells. **Attrition**, players leaving before the end, shrinks every later denominator.

**Rates per head, everywhere.** Public-health maps show illness per 100,000 residents, and road safety compares accidents per vehicle-kilometre, because a raw count mostly measures population and traffic. They face the small-sample problem too. A village with one case in 50 people shows a higher rate than a city, which is why their statisticians also smooth small areas toward the regional average. A level designer's death map is a disease map of a very small country.

Four cases, one model. Before reading any map, ask what the colour is divided by, and how many observations stand behind each cell.

### Design judgment, eyes open

- **Keep all three maps, and read them together.** The count map is still useful. It shows where most of the total frustration happens, weighted by traffic. The corridor with 28 deaths ruins more total minutes than the lift. The shrunk rate shows where a single visit is dangerous. Decide which question you are asking before choosing a map.
- **High danger can be intended.** A sniper yard at 25% may be exactly what the design wanted: a risky shortcut with a reward. Compare the rate with your design intent, not with zero. Week 3's intensity graph gives each area an intended level of threat. The heatmap tells you whether you hit it.
- **`k` is a judgment, so choose it before looking.** If you tune `k` until the map shows what you expected, you have learned nothing. A workable default is `k` near the number of visits you would want before trusting a cell on its own, often 10 to 30 for a class-sized playtest. Then check that the top of the ranking is stable when you double `k`.
- **Shrinkage hides real problems in rare places.** The vent's true rate might be 40%. With 10 visits you can't tell. The right response is a targeted test, sending testers through the vent, not a bigger `k`.
- **Don't use the raw rate map in a meeting.** Its brightest cells are the least reliable ones, and people remember the brightest cells.

## 3. Cell size and noise

Every binned heatmap has a cell size, and it trades detail against noise.

- **Small cells** show detail. A 1 m cell can separate the space behind a crate from the space in front of it. But each cell gets few visits, so its rate is noisy.
- **Large cells** get many visits and steady rates. But an 8 m cell may merge a safe doorway with the deadly room behind it, and the average hides both.

The standard error makes the trade concrete. Take a cell whose true rate is 0.2.

| Visits in the cell | Standard error `sqrt(0.2 × 0.8 / v)` | Roughly, the rate you might measure |
|---|---|---|
| 400 | 0.020 | 0.16 to 0.24 |
| 100 | 0.040 | 0.12 to 0.28 |
| 25 | 0.080 | 0.04 to 0.36 |
| 6 | 0.163 | anything from 0 to 0.5 |

(The last column is about two standard errors each side. MA102 week 13 explains why that simple interval is too narrow at small counts, and how the Wilson interval fixes it.)

Visits per cell fall as cells shrink, though not in a simple way. A cell on a corridor keeps most of its visits when it gets narrower along the corridor, because every player still passes through. A cell in open ground loses visits roughly in proportion to its area. So halving the cell size can double the standard error in open areas while barely changing it on routes.

A practical rule for choosing:

1. Name the smallest feature you need to see. A piece of cover, a doorway, a ledge. The cell should be no larger than half that feature's size.
2. Count the visits per cell on the routes you care about. If most are below your `k`, the cells are too small for this playtest. Use larger cells or test with more players.
3. Look at the map at two cell sizes, for example 2 m and 4 m. A problem that shows up at both is real. A problem that exists only at one size deserves suspicion.

Lab 14 asks you to do exactly this with a simulated playtest, and you will see the hottest shrunk cell move when the cells get too large or too small.

## 4. From heatmap to design change

A heatmap starts a question. It seldom ends one.

### Pair every map with observation

The Wired article has a good example. In Halo 3's Jungle level, players kept running out of rifle ammunition, even though the designers had left plenty around. The telemetry showed the problem. It took the lab's video recordings to explain it. Players were firing at enemies from too far away and wasting bullets. No heatmap of ammunition pickups would have shown that.

So for every hot cell you plan to act on, pull up the recordings or observer notes for a few deaths there. GD101 week 7's method still applies: record what players did, not your guess about what they meant. Ask of each death, did the player see the threat, did they know what to do, could they have done it? Those three answers point to different fixes: sightlines and signposting (weeks 4 and 5), teaching (week 1), or tuning the challenge itself.

### A small menu of maps

Pick maps to match the question. For a level playtest, these five cover most needs:

| Question | Events | Colour each cell by |
|---|---|---|
| Where is a visit dangerous? | deaths, visits | shrunk death rate |
| Where does the frustration add up? | deaths | death count |
| Where do players get lost? | position samples | time spent, or position at fixed times (the Jungle method) |
| Where do sessions end? | quits, visits | shrunk quit rate |
| Who is shooting from where? | death position and killer position | lines from killer to victim, drawn over the level |

The last one connects to week 12. The sightline heatmap you computed from geometry predicts where a respawn point can be seen from. The killer-victim lines show where players actually shot from. When the two disagree, one of them is wrong about your level, and finding out which is a good use of a playtest.

### Before and after

When you change a level because of a heatmap, test it again and compare the same map on the same kind of tester. A new layout tested on experienced players will look safer than the old one tested on beginners, whatever you changed. MA102 week 14 formalises the comparison as an A/B test. For a class playtest, at least keep the tester pool, the build notes and the cell size the same, and report `v` next to every rate you compare.

### Logging responsibly

Position data from real players is personal data in many jurisdictions. Tell testers what you record, keep it tied to an anonymous ID rather than a name, and delete raw logs when the analysis is done. DB201 covers telemetry design in depth. For this course, a consent line on your playtest sheet and an anonymous player column in your CSV are enough.

## In-class activity (25 minutes)

Groups of three. Each group gets a printed top-down plan of a small level (a 6 × 4 grid of 5 m cells) and an event list from a simulated playtest of 20 testers: one line per visit and per death, with the cell label.

1. **(8 min)** Tally visits and deaths per cell on the plan. Colour a copy by death count, darker for more.
2. **(8 min)** Compute `r̄` for the level and the shrunk rate for every cell with `k = 10`. Colour a second copy by shrunk rate.
3. **(5 min)** Circle the top cell on each map. If they differ, write one sentence explaining why, using `v` for each cell.
4. **(4 min)** Pick the cell you would investigate first and write the question you would ask of the video recordings of deaths there.

Expected output: two coloured maps, the calculation for the top three cells, and the one question for the recordings.

## Common misconceptions

- **"The reddest spot on a death map is the most dangerous place."** A count map shows traffic times danger. Divide by visits before you rank cells.
- **"Divide by visits and the problem is solved."** Raw rates in cells with few visits are dominated by chance. Shrink them toward the level's average, or hide cells with too few visits.
- **"A heatmap tells you what to fix."** It tells you where to look. The reason comes from watching players, and different reasons need different fixes.
- **"Smaller cells are always more precise."** They are more detailed and less precise. Each cell's rate rests on fewer visits.

## Check yourself

1. In a playtest, `r̄ = 0.08`. Cell A has 3 deaths in 6 visits. Cell B has 30 deaths in 200 visits. Compute both shrunk rates with `k = 20`. Which do you investigate first, and what would change your mind?
2. A cell's measured rate is 0.25. What is its standard error with 100 visits? With 25? How many visits would halve the error at 25 visits?
3. On a mirrored two-base multiplayer map, one test logged 180 deaths near the left base and 120 near the right. Why is comparing these counts more defensible than on most maps? Which one extra number would you check before concluding that one side has an advantage?
4. A single-player game has 1,000 deaths logged on its first map and 600 on its last. Only 475 of the first map's 1,000 players reached the last map. Compare the danger of the two maps properly. What does the raw comparison get wrong?

<details>
<summary>Answers</summary>

1. `k × r̄ = 1.6`. A: `(3 + 1.6) / (6 + 20) = 4.6 / 26 = 0.177`. B: `(30 + 1.6) / (200 + 20) = 31.6 / 220 = 0.144`. A ranks higher, but its evidence is 6 visits. B is well measured and nearly twice the level rate. A reasonable plan is to investigate B now and send testers through A to get more visits. If a targeted test gave A 30 visits and it kept a rate near 0.5, A would move to the top.
2. `sqrt(0.25 × 0.75 / 100) = sqrt(0.001875) = 0.043`. With 25 visits, `sqrt(0.0075) = 0.087`. The error halves when visits quadruple, so 100 visits.
3. The two halves are mirror images and both teams play the same matches, so the exposure (time spent and visits) near each base is roughly equal by design. That makes the denominator nearly the same on both sides. Still, check time spent or visits near each base. If one team simply spends more time near the left base, more deaths there would be expected and would not show an advantage.
4. Per player who reached the map: first map `1,000 / 1,000 = 1.0` deaths, last map `600 / 475 = 1.26`. The last map is about 26% more deadly per player, though its raw count is 40% lower. The raw comparison ignores attrition, the players who never arrived.

</details>

## Lab / assignment hook

[Lab 14, death heatmaps that don't lie](../labs/lab14.md). You finish a small Python module that turns a telemetry file into count, raw-rate and shrunk-rate maps, find the level's real danger in a simulated playtest, test the effect of `k` and cell size, and then instrument your own blockout, run a playtest, and write a heatmap-based analysis. The analysis counts toward the course's analysis component (20%).

## Sources

- Thompson, C. (2007, August 21). "Halo 3: How Microsoft Labs Invented a New Science of Play." *Wired* 15.09 (web archive of wired.com/gaming/virtualworlds/magazine/15-09/ff_halo). Randy Pagulayan's test lab for Bungie; more than 3,000 hours of Halo 3 play by about 600 players, with where players were killed tracked to the square foot; the Valhalla death heat map from April and the terrain change; the Jungle level position map of about 30 testers after half an hour, the geography change and the timestamp-coloured dots; the Jungle ammunition problem explained from video recordings.
- Valve Corporation, "Episode Two Stats" (steampowered.com/status/ep2/ep2_stats.php, archived January 2009). Data collected 10 October 2007 to 11 September 2008; 4,149,046 sessions; 47.54% of players reached the final map; 44.22% completed the game; average deaths per map; death maps coloured by where players died most often, for each map.
- Valve Corporation, "Team Fortress 2 Stats" (steampowered.com/status/tf2/tf2_stats.php, archived January 2009). Death maps for eight maps (cp_dustbowl, cp_granary, cp_gravelpit, cp_well, ctf_2fort, tc_hydro, cp_badlands, pl_goldrush), data collected 31 December 2008 to 7 January 2009.
- Totten, C. W. (2019). *An Architectural Approach to Level Design* (2nd ed.). CRC Press.
- The Quarry level, its visit and death counts, the choice of `k` and the cell-size rule are teaching models built for this lecture, not data from any game.

## Interactive spec: examples/w14-death-heatmap.html

**Purpose.** Show that a death-count heatmap mostly measures traffic, that a raw death-rate map mostly measures noise when visits are few, and that the shrunk rate `(d + k r̄) / (v + k)` finds the dangerous area.

**The one insight the visual must make obvious.** With defaults (30 testers, `k = 20`, 4 m cells), the count map's hottest cell is on the bridge or main corridor, and the shrunk-rate map's hottest cell is in the sniper yard. With 5 testers the raw-rate map is speckled: its hottest cells rest on a few visits each and often sit outside the yard (a 100% cell appears on only about one playtest in three), while the shrunk map is calm.

**Layout.** Mobile (390px): two maps stacked (count on top, rate below), then controls, then the numbers panel and the zone table. Desktop (1280px): the two maps side by side, controls and numbers below.

**The level.** 40 × 20 m, drawn top-down as plain rectangles with labels: spawn room (0-6, 6-14), corridor (6-26, 8-12), sniper yard (14-26, 12-20), vent (10-30, 0-4), bridge (26-34, 8-12), exit hall (34-40, 6-14). Cells are drawn over it.

**Simulation.** Reproduce Lab 14's generator (`labs/lab14-starter/make_telemetry.py`) in JavaScript. Routes and weights: main 0.70 via (3,10), (26,10), (34,10), (39,10); yard 0.25 via (3,10), (14,10), (18,16), (24,16), (26,10), (34,10), (39,10); vent 0.05 via (3,10), (8,10), (10,2), (30,2), (34,10), (39,10). Speed 2 m/s, one sample per second, jitter uniform ±0.8 m per axis, clamp to the level. Per-second death chance by region: spawn 0.002, corridor 0.012, yard 0.070, vent 0.050, bridge 0.030, exit 0.004, elsewhere 0.010. A run ends at a death or the exit. Each tester plays 4 runs. Use a seeded generator (mulberry32) so a given seed and tester count always give the same data. A "new playtest" button changes the seed. (The JavaScript data need not match the Python CSV exactly. The zone-table mode below carries the exact test values.)

**Counting.** Visits: for each run, a visit starts at the first sample and whenever the sample's cell differs from the previous sample's cell. Deaths: count death events per cell. `r̄ = total deaths / total visits`. Heat per visited cell `= (d + k r̄) / (v + k)`. Unvisited cells are drawn as "no data" (hatched), never as zero.

**Controls.** Testers: 5, 10, 30, 100, 300 (default 30). `k` slider 0 to 100, step 1 (default 20). Cell size: 2, 4, 8 m (default 4). Right map mode: raw rate or shrunk rate (default shrunk). "Hide cells with fewer than N visits" slider 0 to 30 (default 0). "Show true danger" toggle outlines the regions with their per-second death chance. "New playtest" button. Reset.

**Readouts.** Hover or keyboard focus on a cell shows `v`, `d`, raw rate, standard error `sqrt(r(1 − r)/v)` and heat. Numbers panel: total runs, visits, deaths, `r̄`, the top 3 cells on each map with their region names, and a sentence built from the data, for example "Most deaths: bridge (5). Most dangerous per visit: sniper yard, 0.115 from 21 visits."

**Zone-table mode.** A tab that replaces the maps with the lecture's six Quarry zones as bars (count bars on the left, rate bars on the right) with the `k` slider and raw or shrunk switch.

**Test values (zone-table mode).**

| `k` | Corridor | Bridge | Sniper yard | Vent | Spawn room | Lift | Top 3 |
|---|---|---|---|---|---|---|---|
| 0 | 0.070 | 0.120 | 0.250 | 0.400 | 0.047 | 0.500 | Lift, Vent, Sniper yard |
| 5 | 0.070 | 0.120 | 0.243 | 0.300 | 0.048 | 0.278 | Vent, Lift, Sniper yard |
| 20 | 0.071 | 0.119 | 0.225 | 0.200 | 0.051 | 0.167 | Sniper yard, Vent, Lift |
| 100 | 0.076 | 0.114 | 0.175 | 0.127 | 0.0625 | 0.115 | Sniper yard, Vent, Lift |

`r̄ = 0.100` throughout. Counts: 28, 30, 25, 4, 11, 2. Values are rounded to 3 decimals, except exact 4-decimal values such as 21 / 336 = 0.0625, which the page shows in full rather than rounding a tie.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`, light and dark. Use a single-hue sequential scale that works in both themes and for colour-blind readers, with a legend showing numeric values. "No data" is a hatch pattern, distinct from the lowest colour. Cells are keyboard focusable in a grid with arrow-key movement. Respect reduced motion. No game art, logos or screenshots.

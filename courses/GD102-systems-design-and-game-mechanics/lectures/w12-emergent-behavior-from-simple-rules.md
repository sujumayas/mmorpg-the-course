# GD102 · Week 12 — Emergent Behavior from Simple Rules

**Why this matters:** Some of the best things in games, and some of the strangest bugs, come from a few local rules running many times over. You cannot read the result off the rules. You have to run them, and you have to know which numbers in them are dangerous to touch.

**You will be able to:**
- Apply a neighbor-count rule to a grid by hand and predict one step of a cellular automaton.
- Explain how a majority rule turns random noise into cave-like structure, and identify the positive feedback that drives it.
- Measure how a global property (wall share, connectedness) responds to one local parameter, and locate the threshold where it changes fast.
- Trace an emergent bug back to the chain of simple rules that produced it, and choose where to break the chain.

**Before class:** Adams & Dormans, *Game Mechanics: Advanced Game Design* (2012), chapter 3, "Complex Systems and the Structure of Emergence". Gardner, M. (1970), "Mathematical Games: The fantastic combinations of John Conway's new solitaire game 'life'", *Scientific American*, October 1970 (library access). RogueBasin, "Cellular Automata Method for Generating Random Cave-Like Levels" (free online, the first half).

**Prerequisites from earlier courses:** From this course, [week 1, systems thinking](w01-systems-thinking-parts-relationships-emergence.md) (emergence as a property of the whole), [week 3, positive feedback](w03-positive-feedback-loops-snowballing.md), [week 4, negative feedback](w04-negative-feedback-loops-rubber-banding.md), [week 10, emergence vs progression](w10-emergence-vs-progression.md) and [week 11, intransitive mechanics](w11-intransitive-mechanics-rock-paper-scissors.md). Loops over 2D arrays from CS101 (see the [CS101 syllabus](../../CS101-programming-for-games-i/syllabus.md)). Averaging over many random runs, from [MA102 week 11, Monte Carlo simulation](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w11-monte-carlo-simulation.md). GD101 [week 10](../../GD101-introduction-to-game-design/lectures/w10-chance-vs-skill-and-randomness.md) on randomness.

**Interactive:** [Cave automaton threshold](../examples/w12-cave-automaton.html). Keep it open during section 2.

---

## 1. Local rules, global patterns

In December 2015, the developer of *Dwarf Fortress* posted a fix to his development log. Cats had been dying of alcohol poisoning.

Nobody had written a rule that said "cats drink." The log gives only the fix, so the chain below is our reconstruction from that note and the community wiki. The game had several separate rules, each sensible on its own. Dwarves drink in taverns, and drinks spill. Spilled liquid leaves the floor damp and coats anything that walks through it. Cats clean themselves by licking their fur, and cleaning swallows whatever is on the fur. Swallowed alcohol makes a creature drunk. Put a cat in a tavern and run the rules for a few in-game days, and the chain completes. The fix in the log reduced the effect, so a cat that cleans itself after walking over a damp tavern floor no longer dies from it.

Every step in that chain is a **local rule**. A local rule reads only the thing it applies to and what is right next to it. The cat rule does not know about taverns. The spill rule does not know about cats. The result, cats dying in taverns, is a **global pattern**. It is visible only when you look at the whole system over time, and no single rule mentions it.

Week 1 defined **emergence** as behavior of the whole that none of the parts has on its own. Week 10 looked at emergence at the scale of game design, counting how many pairs of rules can meet. This week goes down to the smallest scale. Take one rule, apply it to every cell of a grid at once, repeat, and watch structure appear from nothing. The tool for this is the **cellular automaton**.

### Cellular automata

A **cellular automaton** (CA) has four parts.

1. A **grid** of cells. We use a square grid.
2. A **state** for each cell. We use two states, wall and floor (or alive and dead).
3. A **neighborhood**, the set of cells a cell looks at. We use the **Moore neighborhood**, the 8 cells around a cell, sometimes with the cell itself included to make a 3 × 3 block.
4. An **update rule** that gives each cell's next state from its neighborhood's current state.

Every cell updates at the same time, from a snapshot of the current grid. That detail matters in code. If you update cells one by one in place, cells later in the loop see a mix of old and new states, and you get a different (and direction-biased) automaton. Always read from one grid and write to another.

That is the whole machine. It has no memory beyond the grid, no plan, and no idea what a cave or a glider is. Anything that looks like a plan in its output is emergent.

## 2. Worked example: caves from coin flips

### The hook

Many roguelike developers do not draw their caves. They fill a grid with random noise, then run one short rule over it a few times, and cave systems appear with smooth walls, winding tunnels and open chambers. The method is common enough to have a standard write-up on RogueBasin, the roguelike developers' wiki, where it is called the "4-5 rule".

Here is the surprising part. The rule's main dial is the share of walls in the starting noise. The write-up starts at 45%. Set it to 40% and you get one big open field with a few pillars. Set it to 50% and you get sealed pockets of rock with no way between them. Five percentage points in the noise, and the map goes from "too open to be a cave" to "not one connected level." Why does such a small change flip the whole map?

### The model

Start with a `W × H` grid. The outer border is always wall. Every inner cell starts as wall with probability `p`, and floor otherwise. This is the noise.

Then apply this rule to every cell at once, several times:

```
n = number of walls in the 3 × 3 block centered on the cell
    (the cell itself plus its 8 neighbors; cells off the grid count as walls)

next state = wall   if n ≥ 5
             floor  if n ≤ 4
```

- `p` is the initial wall probability.
- `n` is a count from 0 to 9.
- The threshold 5 is a majority of 9.

RogueBasin states the rule the other way round, and it is the same rule. A wall stays a wall if 4 or more of its 8 neighbors are walls. A floor becomes a wall if 5 or more of its 8 neighbors are walls. If the cell is a wall, it adds 1 to the 3 × 3 count, so "4 neighbors plus itself" is `n = 5`. Both forms say "join the majority of your 3 × 3 block."

That is why it makes caves. It is a **majority vote**, and a majority vote is a positive feedback loop (week 3). A cell surrounded mostly by walls becomes a wall, which makes its neighbors more surrounded by walls, which makes them walls. Scattered walls in mostly-floor areas lose their vote and vanish. Scattered floor cells in mostly-wall areas get filled in. Local majorities grow and harden, and the random speckle turns into smooth blobs.

### Numbers you can check

**One cell at a time.** Apply the rule to these three 3 × 3 blocks. `#` is wall, `.` is floor. The center is the cell being updated.

| Block | Walls counted `n` | Next state of center |
|---|---|---|
| `# . #` / `. # .` / `# . .` | 4 | floor (a lonely wall erodes) |
| `# # .` / `# . #` / `. # .` | 5 | wall (a floor gap is filled) |
| `# # #` / `. # .` / `. . .` | 4 | floor |

Count them yourself. In the first block, walls are the top-left, top-right, center and bottom-left, which gives 4. Four is not a majority, so the center wall becomes floor.

**A whole small grid.** Here is a 5 × 5 grid of noise with 8 walls out of 25 (32%). Cells beyond the edge count as walls.

```
Before       Counts n        After
# . # . .    6 6 5 6 6       # # # # #
. . # . #    5 4 2 3 4       # . . . .
# . . . .    5 3 2 3 5       # . . . #
. # . . #    5 3 2 2 4       # . . . .
. . # . .    6 5 5 5 6       # # # # #
```

Check a few counts. The top-left cell: its 3 × 3 block has 5 off-grid cells (walls), plus itself (wall), plus its three on-grid neighbors (floor, floor, floor), so `n = 6`. The center cell: its block is rows 2 to 4 and columns 2 to 4, which holds `. # .`, `. . .`, `# . .`, so `n = 2`. After one step the grid has 14 walls instead of 8, and they are all on the edges. The off-grid-as-wall choice builds an outer wall, and the interior clears out. On a grid this small, the edge dominates. On a real map, the interior does the interesting work.

**The dial.** Now a full map, 64 × 40 cells, border always wall, five steps of the rule. The table averages 20 random maps for each `p` (seeds 1 to 20, the generator given in the spec). "Largest region" is the biggest connected floor area, as a share of all floor, where cells connect up, down, left and right. The region count is a mean of 20 whole numbers, so it is exact to two decimals and shown that way.

| Initial wall chance `p` | Wall share after 5 steps | Largest region, share of floor | Separate floor regions (mean) |
|---|---|---|---|
| 0.30 | 14.9% | 100.0% | 1.00 |
| 0.35 | 19.5% | 100.0% | 1.00 |
| 0.40 | 28.7% | 99.9% | 1.10 |
| 0.42 | 33.8% | 99.3% | 1.50 |
| 0.44 | 39.3% | 96.1% | 1.85 |
| 0.45 | 42.5% | 90.6% | 2.45 |
| 0.46 | 46.1% | 88.5% | 3.05 |
| 0.48 | 53.3% | 79.2% | 4.55 |
| 0.50 | 61.2% | 63.4% | 7.25 |
| 0.52 | 68.3% | 52.3% | 9.80 |
| 0.55 | 77.9% | 37.5% | 12.50 |

Look at the first two columns together. Below about `p = 0.45`, the rule *removes* walls. Five steps turn 40% noise into 28.7% wall. Above it, the rule *adds* walls. Five steps turn 50% noise into 61.2% wall. The rule amplifies whichever side of the middle you start on, as a majority vote should. (The middle is a little below 50% because the border walls, about 8% of this map, also vote.)

Now the last two columns. From `p = 0.40` to `p = 0.50`, the map goes from one open region to more than seven separate ones, and the largest region falls from almost all the floor to under two thirds of it. A player dropped into the map at 0.50 has roughly a one-in-three chance of starting somewhere that does not connect to the biggest cave. Most of that change happens in the ten points between 0.40 and 0.50, and the steepest part is between 0.44 and 0.50. That band is the **threshold**. Near it, a small change to a local number makes a large change to a global property.

### A visual you can move

Open the interactive. The left panel is the map. The right panel is a chart of the dial table, with `p` on the x-axis and two lines, wall share and largest-region share, averaged over 20 seeds.

Drag `p` slowly from 0.40 to 0.50. On the left, the map looks only a little different at each step. A few more walls, a slightly narrower tunnel. You would not notice any single step. On the right, the marker slides along the chart and crosses the steep part of the largest-region curve, and the "separate regions" readout climbs from 1 to 7. The map view hides the threshold. The chart view shows it. That is the reason to always build the second view when you tune an emergent system.

Then use the step control. Set `p = 0.45` and step from 0 to 5. The largest-region share jumps from about 11% at step 0 (noise has no big regions) to about 92% after one step. Most of the structure appears in the first step or two, and later steps mostly smooth edges. The seed control lets you check that this is typical and not one lucky map.

### Cross-game recognition

**Conway's Game of Life (1970).** Martin Gardner introduced John Conway's game to readers of *Scientific American* in October 1970. It is the same machine as our cave rule with a different threshold. Cells are alive or dead, the neighborhood is the 8 surrounding cells, and the rule reads as follows. A live cell with 2 or 3 live neighbors survives, any other live cell dies, and a dead cell with exactly 3 live neighbors comes alive. Where our rule is a majority vote, which smooths, Life's rule is a narrow band, which neither smooths nor explodes. That band is why Life produces moving and oscillating structures instead of blobs. Section 3 works through two of them.

**Noita (2019 early access, 1.0 in 2020).** Nolla Games built a roguelike in which nearly every pixel is simulated. Sand falls, water flows, fire spreads, and liquids mix. The developers described the approach as a falling-sand simulation, which is a cellular automaton with more states and rules. Each pixel looks only at its neighbors. The global patterns, a burning oil spill that ignites a wooden structure that drops a pool of acid on the player, are chains of local rules just like the cave and the cats. Rewrite a Noita pixel in our form and it is a cell with a state (material), a small neighborhood, and a rule table.

**Boids (1987).** Craig Reynolds's flocking model, presented at SIGGRAPH in 1987, gives each simulated bird three local steering rules. Steer away from flockmates that are too close (separation). Steer toward the average heading of nearby flockmates (alignment). Steer toward their average position (cohesion). No bird knows the shape of the flock. Flocks form, split around obstacles and rejoin. The film *Batman Returns* (1992) used modified boids software for its bat swarms and penguin flocks. Boids are not on a grid, but the structure is the same. Each agent reads only its neighborhood, and the pattern belongs to the whole. Cohesion is our majority vote in continuous form, pulling each agent toward the local crowd.

Three systems, one shape. **Agents or cells, a small neighborhood, a rule that reads only the neighborhood, all applied at once, many times.** When a pattern in a game looks designed but you cannot find where it was designed, look for this shape.

### Eyes-open design judgment

- **Use it for texture, not for guarantees.** A CA gives natural-looking variety for almost no authoring cost. It gives no promise that the map is connected, that the exit is reachable, or that the start room is safe. RogueBasin's own write-up lists disconnected caves and huge open spaces as the method's main problems. Pair the CA with a check (a flood fill that measures connectivity) and a repair (connect the regions with tunnels, or fill in all but the largest one).
- **Tune away from the threshold, or on purpose near it.** Near `p = 0.45`, two maps from the same settings can differ a lot, and a small balance tweak changes every map in the game. If you want consistency, choose `p` on a flat part of the curve. If you want variety, the steep part gives it, and you must then handle the bad maps.
- **Fix the seed for testing.** A seeded generator makes every map reproducible. When a tester reports "map 3,117 trapped me," you can load exactly that map. MA102 week 11 makes the same argument for simulations.
- **Change one rule, re-measure everything.** RogueBasin describes a refined version with a second, wider neighborhood check that adds walls in large open areas. It fixes one problem and changes the whole dial table. Any change to a local rule needs the sweep re-run. Never trust your eyes on one map.
- **The alternatives cost more authoring.** Hand-drawn maps give full control and cost designer time per map (week 10's plan P). Room-and-corridor generators give guaranteed connectivity and look artificial. Noise functions give smooth terrain but need their own thresholds. The CA sits in between. It is cheap, organic and unreliable, and that is the trade you are choosing.

### Check this example

1. A floor cell has 5 walls among its 8 neighbors. What does it become? A wall cell has 3 walls among its 8 neighbors. What does it become?
2. A designer wants maps with about 30% wall and one connected cave, and sets `p = 0.41`. Using the dial table, is this a safe choice? What would you change if the team later wants 45% wall?
3. Why does the table's 0.30 row give fewer walls than 0.30 of the map, even though the border is always wall?

<details>
<summary>Answers</summary>

1. The floor cell's 3 × 3 count is 5 (neighbors) + 0 (itself) = 5, so it becomes wall. The wall cell's count is 3 + 1 = 4, so it becomes floor.
2. Between 0.40 (28.7% wall, 99.9% connected) and 0.42 (33.8%, 99.3%), the curve is still near-flat for connectivity, so 0.41 is safe. For 45% wall, `p` must be about 0.46, which is in the steep part: expect about 3 separate regions on average. Add a connectivity pass (flood fill plus tunnels or fill) rather than relying on `p`.
3. Below the threshold, the majority rule removes walls. Most isolated walls have fewer than 5 walls in their block and erode, so the wall share falls well below the starting noise level. The border adds walls, but the interior loses more.

</details>

## 3. Game of Life: things no rule mentions

Life shows emergence in its most striking form, because its structures seem to have behavior of their own.

**The blinker.** Three live cells in a row. Apply the rule.

```
Step 0      Step 1      Step 2
. . . . .   . . . . .   . . . . .
. . . . .   . . # . .   . . . . .
. # # # .   . . # . .   . # # # .
. . . . .   . . # . .   . . . . .
. . . . .   . . . . .   . . . . .
```

Check it. The middle cell of the row has 2 live neighbors, so it survives. The two end cells each have 1 live neighbor, so they die. The cells directly above and below the middle each have 3 live neighbors (the whole row), so they are born. The row becomes a column. By the same reasoning, the column becomes a row. The blinker has a **period** of 2.

**The glider.** Five cells in this shape:

```
. # .
. . #
# # #
```

Run it for four steps and the same shape appears again, shifted one cell down and one cell right. The glider has period 4 and moves diagonally one cell every four steps, forever, across an empty grid. There is no "move" in Life's rules. The rules only say which cells live and die. Motion is a pattern of births and deaths that repeats in a new place. That is emergence in its purest form, a property (moving at a quarter of a cell per step) that belongs to the pattern, not to any rule or any cell.

Later in 1970, a group led by Bill Gosper found a **glider gun**, a stable structure that emits a new glider every 30 steps. The rules never mention guns either.

**Why the band matters.** Compare three rules on the same random start.

- A majority rule (our caves) smooths. Everything settles into blobs in a few steps.
- A rule with a very wide birth condition fills the grid. Every cell becomes alive and stays alive.
- Life's narrow band (born on exactly 3, survive on 2 or 3) sits between the two. Random starts produce a long period of churning activity, then settle into scattered stable blocks, blinkers and escaping gliders.

For a designer, that sits beside week 3 and week 4. Too much positive feedback and the system locks into one state (all wall, all alive). Too much negative feedback and nothing interesting happens (everything dies). Rich behavior needs the loops balanced against each other. Life's numbers do that, and a small change to them loses it.

## 4. Debugging emergence

Back to the cats. How do you find and fix a bug that no single rule contains?

**Write the chain.** List each rule that fires, in order, with what it reads and what it writes. For the cats, our reconstruction is:

1. Dwarves drink in the tavern (writes: spilled drink on the floor).
2. Spills leave the floor damp (writes: liquid on tile).
3. Walking through liquid coats the walker (reads: liquid on tile; writes: liquid on fur).
4. Cats clean their fur (reads: liquid on fur; writes: liquid swallowed).
5. Swallowed alcohol causes drunkenness, and enough of it kills (reads: amount swallowed).

**Find the link where the amounts are wrong.** Each rule is fine on its own. The problem is usually a quantity passed between rules that no single rule checks. A few drops of beer on a paw should not add up to a lethal drink, so the amount carried from step 3 to step 5 is the suspicious link. The developer's fix, as logged, reduced the effect of alcohol picked up this way. It did not remove any rule in the chain.

**Break the chain at the cheapest link that keeps the good behavior.** Removing rule 4 would stop cats cleaning themselves, which also stops them cleaning off other things, which the game wants. Removing rule 3 would make liquids stop spreading on bodies, which breaks blood, mud and much else. Scaling the quantity at the rule 4 step fixes the cats and keeps every other chain that uses those rules. That is the general lesson. In an emergent system, rules are shared by many chains, so fix quantities before you delete rules.

**Add damping, not special cases.** A special case ("cats cannot get drunk") fixes this chain and leaves the next one open. A general limit ("a creature swallows at most a trace of what is on its fur") damps every chain that passes through that link. In systems language, it adds a small balancing loop where a quantity was flowing unchecked.

This is the same reasoning you would use for the cave generator. If maps come out disconnected, you could hand-edit bad seeds (special cases) or add a connectivity pass that applies to every map (a general limit). Emergent systems reward general fixes.

## In-class activity (25 minutes)

**Paper automaton.** Groups of three, with a sheet of 10 × 10 grid paper per person, a die and two colored pens.

1. Each person fills their grid with noise. Roll a die for each cell. A roll of 1 or 2 is wall (a 33% chance) for one person, 1 to 3 (50%) for another, and 1 to 2 plus a coin flip on 3 (about 42%) for the third. Mark off-grid cells as walls. (6 min)
2. Apply the cave rule once, by hand, writing the next grid on a fresh sheet. Split the grid between the group to go faster, but every cell must read from the old sheet. (10 min)
3. Count the walls and the separate floor regions on each result. (3 min)
4. Put the three results side by side. Which starting share gave one open area, which gave pockets? Where does your group think the threshold is on a 10 × 10 grid? Why might it differ from the 64 × 40 table? (6 min)

Expected output: three before-and-after grids, a wall count and a region count for each, and a one-line answer on why the small grid's threshold moves (hint: the border is a larger share of a small grid).

## Common misconceptions

- **"Complex behavior needs complex rules."** The cave rule is one comparison. Life is two. Complexity in the output comes from repetition and interaction, not from the rule's length.
- **"If each rule is correct, the system is correct."** The cats' rules were each correct. The bug lived in the chain. Test chains and quantities, not only rules.
- **"Emergent means unpredictable, so there is nothing to tune."** You cannot predict one map, but you can measure the distribution of maps. The dial table is a precise, reproducible description of a random system. Tune the distribution.
- **"Updating cells in place is just an optimization."** It changes the automaton. Cells later in the loop read new values, and patterns drift in the loop's direction. Always use two grids.

## Check yourself

1. Apply Life's rule to the 2 × 2 square `##` / `##` (a block) surrounded by dead cells. What happens, and why?
2. A designer changes the cave rule's threshold from 5 to 6 (wall only if `n ≥ 6`). Predict, without running it, the direction of the change in wall share and connectedness for `p = 0.45`. Explain using feedback.
3. In the cat chain, name a second place where you could add a general limit, and one other chain in a game like *Dwarf Fortress* that your limit would also affect.
4. You run the cave generator 100 times at `p = 0.47` and see a mean of 3.8 separate regions. A teammate's tweak drops it to 3.1 in 5 runs. Using MA102's argument about sample size, what should you ask before accepting the tweak?

<details>
<summary>Answers</summary>

1. Each live cell has exactly 3 live neighbors, so all four survive. Each dead cell touching the block has at most 2 live neighbors, so none is born. The block never changes. It is a still life, with period 1.
2. With a higher bar for walls, fewer cells meet it. The rule now favors floor, so the wall share falls and the map opens up, and connectedness rises. In feedback terms, the positive loop that grows walls now needs a stronger local majority to run, so it is weaker, and the floor side of the vote wins more often.
3. For example, at rule 3 (coating). "A walker picks up at most a small amount of liquid from a tile" would limit every chain where creatures carry liquids, including tracking blood, spreading mud, or carrying a poison from one room to another. Any such chain would now move less of the liquid, which is usually what you want, but you must check chains that depended on the old amount.
4. Five runs is a tiny sample of a noisy quantity. Ask for the same number of runs (100) with the same seeds, or at least a standard error for both means. A drop of 0.7 regions could easily be noise at `n = 5`.

</details>

## Lab hook

**Lab 12, cave generator** ([`labs/lab12.md`](../labs/lab12.md)). You run and extend a 40-line Python cellular automaton, reproduce the dial table, add a connectivity measure and a repair pass, then tune the generator for a design target and write a short tuning memo with a chart. The sweep code is reused in week 14's spreadsheet tuning.

## Sources

- Adams, T. (2015). *Dwarf Fortress* development log, bay12games.com/dwarves/dev_2015.html, entry of 12 December 2015. Fix note on cats dying of alcohol poisoning after walking over damp tavern floors and cleaning themselves, with the effect reduced. The chain in section 4 is our reconstruction from that note and the *Dwarf Fortress* Wiki page "Cat" (DF2014), which states that cats with a contaminant on their fur clean themselves with their tongue and are exposed to any ingestion syndrome it carries.
- RogueBasin, "Cellular Automata Method for Generating Random Cave-Like Levels" (roguebasin.com, accessed September 2026). The 4-5 rule, the 45% starting fill, the problems of disconnected maps and huge open spaces, and the refined rule with a wider neighborhood.
- Gardner, M. (1970). "Mathematical Games." *Scientific American*, October 1970. First publication of Conway's Game of Life. Rules, glider period and the 1970 glider gun by Gosper's group confirmed via Wikipedia, "Conway's Game of Life" (accessed September 2026).
- Reynolds, C. W. (1987). "Flocks, Herds, and Schools: A Distributed Behavioral Model." SIGGRAPH '87. The three steering rules and the use of modified boids software in *Batman Returns* (1992), from Reynolds's page red3d.com/cwr/boids (accessed September 2026): bat swarms by VIFX and penguin flocks by Boss Films.
- Wikipedia, "Noita (video game)" (accessed September 2026). Nolla Games; nearly every pixel simulated; falling-sand approach described by the developers as complex cellular automata; early access 24 September 2019, 1.0 on 15 October 2020.
- Adams, E. & Dormans, J. (2012). *Game Mechanics: Advanced Game Design*. New Riders. Chapter 3.
- The dial table and the 5 × 5 example were computed for this lecture with the generator and rule in the interactive spec (seeds 1 to 20).

## Interactive spec: examples/w12-cave-automaton.html

**The one insight:** a cave map looks almost the same from `p = 0.40` to `p = 0.50`, but its connectedness collapses across that band. The map view hides the threshold. The sweep chart shows it.

**Layout.** Two linked panels with controls above. Map left and chart right at 900px and wider; stacked (map first) at 390px. The map canvas scales to the panel width and keeps square cells.

**Left panel, "Map."** A `64 × 40` grid. Walls drawn in the ink token, floor in the surface token. The largest connected floor region is tinted with accent 1. Other floor regions are tinted with accent 2 at lower opacity, so disconnected pockets are visible without relying on hue alone (also add a thin outline around non-largest regions). Readout under the map: wall share, largest region share of floor, separate floor regions, current step.

**Right panel, "Sweep."** Line chart, x-axis `p` from 0.30 to 0.60, y-axis 0% to 100%. Two lines, averaged over seeds 1 to 20 at 5 steps: wall share (accent 1) and largest-region share of floor (accent 2). Precompute on load at `p` steps of 0.01 (31 points; about 620 small runs, fast). A vertical marker at the current `p`. A shaded band marks where the largest-region line drops fastest (the interval between consecutive points with the largest decrease), labeled "threshold".

**Controls.**
- `p`, initial wall chance: range 0.30 to 0.60, step 0.01, default 0.45.
- Steps: range 0 to 8, step 1, default 5. Also Step +1 and Reset buttons.
- Seed: number input 1 to 9999, default 1, plus a "new seed" button.
- Toggle "count off-grid as wall" (default on). Turning it off counts off-grid cells as floor. The sweep recomputes for the current toggle state.
- All keyboard accessible with visible values.

**Generator (must match exactly so the test values reproduce).**
- PRNG mulberry32 with the seed as its 32-bit state:
  ```
  function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;}}
  ```
- Fill in row-major order (y from 0 to 39, x from 0 to 63). Draw one random number for every cell, including border cells, so the sequence is stable. Cell is wall if it is on the border or the draw is `< p`.
- Rule: `n` = walls in the 3 × 3 block including the cell, off-grid counted as wall (when the toggle is on). Next state wall if `n ≥ 5`. Read from the current grid, write to a new one.
- Connectivity: 4-connected flood fill over floor cells.

**Test values (builder must reproduce, toggle on).**
- Seed 1, `p = 0.45`: step 0 wall share 50.5%, largest region 10.8% of floor, 126 regions. Step 1: 48.2%, 91.9%, 14 regions. Step 5: 45.9%, 93.8%, 3 regions.
- Sweep averages at 5 steps over seeds 1 to 20 (wall share, largest region, regions): `p = 0.40`: 28.7%, 99.9%, 1.10. `p = 0.45`: 42.5%, 90.6%, 2.45. `p = 0.50`: 61.2%, 63.4%, 7.25. `p = 0.55`: 77.9%, 37.5%, 12.50. Show the mean region count with two decimals (it is a mean of 20 integers, so two decimals are exact).
- Hand example, available as a "tiny grid" mode that swaps the map for a 5 × 5 grid and shows `n` in each cell: before rows `#.#..`, `..#.#`, `#....`, `.#..#`, `..#..` (8 walls); counts `66566 / 54234 / 53235 / 53224 / 65556`; after one step `##### / #.... / #...# / #.... / #####` (14 walls).

**First screen.** Load at `p = 0.45`, seed 1, 5 steps, so the map shows a cave with a few tinted pockets and the chart marker sits on the steep part of the curve. Caption: "Same rule, same map size. Move p by 0.05 and watch the right panel, not the left."

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`, light and dark themes. Region tints paired with outlines. Readout values in text for screen readers, updated with `aria-live="polite"`. `prefers-reduced-motion` disables step animation (jump to the final step). No game art or logos.

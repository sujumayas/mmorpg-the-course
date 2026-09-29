# GD201 · Week 02 — Blockout and greyboxing

**Why this matters:** Most of what is wrong with a level only shows up when someone plays it. Every problem you find then costs time to fix, and that time depends on how finished the level already looks. Teams that paint too early can afford only a handful of fixes. Teams that never leave grey boxes ship levels nobody could read. This week you learn to price that trade and to build the grey version well.

**You will be able to:**
- Define blockout, greybox, scale figure, footprint and critical path, and list what a first blockout must contain and leave out.
- Compute how many layout problems remain after a fixed budget, from the discovery rate per round and the cost of a round at each level of finish.
- Find the best point to switch from greybox to art for a given budget, including problems that only art can reveal, and explain why that best point exists.
- Lay out a blockout on a grid whose pieces tile, and measure walking times along its critical path.

**Before class:** The Level Design Book, "Blockout" (book.leveldesignbook.com, the process section). Joel Burgess and Nate Purkeypile, "Skyrim's Modular Approach to Level Design" (GDC 2013, transcript on Burgess's blog), read up to the end of the section on the graybox phase. Ken Birdwell, "The Cabal: Valve's Design Process for Creating Half-Life" (Game Developer, December 1999), the sections on the Cabal and on playtesting. Totten, *An Architectural Approach to Level Design* (2nd ed., 2019), chapter 3, "Level Design Workflows".

**Prerequisites from earlier courses:** [GD101 week 6, paper prototyping](../../GD101-introduction-to-game-design/lectures/w06-paper-prototyping-cards-dice-boards.md) (the cheapest prototype that answers a question). [GD101 week 7, playtesting](../../GD101-introduction-to-game-design/lectures/w07-playtesting-observe-dont-explain.md) (the chance that a test reveals a problem, `1 − (1 − p)ⁿ`). [GD101 week 8, iteration loops](../../GD101-introduction-to-game-design/lectures/w08-iteration-loops-and-kill-your-darlings.md) (how many loops fit in a schedule). [MA101 week 4, exponentials](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md) (repeated multiplication by a constant factor). [GD201 week 1](w01-level-design-as-teaching.md) (the lesson plan you are about to build).

**Interactive:** [`examples/w02-greybox-budget.html`](../examples/w02-greybox-budget.html). Keep it open during section 2.

---

## 1. What a blockout is

A **blockout** is a playable draft of a level built from simple shapes: boxes, ramps, cylinders, flat planes. It has the real dimensions, the real routes and the real enemy positions, and none of the final art. The word **greybox** means the same thing and comes from the default grey material most editors give new geometry. You will also hear **blockmesh**, **whitebox** and **graybox**. Some studios draw fine distinctions between them. This course treats them as one idea and says "blockout" for the object and "greyboxing" for the activity.

A blockout exists to answer questions that a drawing can't. How long does it take to cross this room? Can the sniper on the balcony see the door? Does the player notice the side path? Is the fight too cramped for three enemies? You answer these by playing, which is why a blockout has to run in the game with the real player controller, camera and movement speed.

### What goes in, what stays out

The Level Design Book's blockout page gives a practical list, which this course adopts.

- **A gridded floor texture.** It lets you and your testers judge distance at a glance.
- **A scale figure.** A box or capsule the size of the player character, placed in the level, so every doorway and ledge can be compared with it.
- **Walls at 150 to 200% of the figure's height,** tall enough to read as walls without making rooms feel like wells.
- **Doorways and corridors at least twice the figure's width,** because players steer less precisely than designers expect and cameras need room.
- **Enemies, pickups and objectives as placeholders,** labelled boxes in the right places.
- **Leave out** finished meshes, props, decoration, detailed lighting and anything that exists to look good.

The same page names wrong scale as the most common beginner problem. A room that feels right in the editor's free camera feels huge or cramped at the player's eye height. The fix is to play your blockout early and often, in the game, not in the editor.

### What a blockout tests

Two shipped examples from the Level Design Book's case studies show the kind of question a blockout answers.

- For the Castle map in the team shooter Dirty Bomb (8 players per team), designer Anthony Massey's team measured the main paths to keep the run from spawn to objective at 8 to 12 seconds, then checked the numbers by playing. Their rule of thumb was that if it feels long, it is too long. That is a timing question, and only a playable blockout can answer it.
- For World's Edge in Apex Legends, Rodney Reece's blockout changed a lot during the art pass. He described deciding which parts of the layout were precious, meaning they had to survive art, and which could flex.

The **critical path** is the shortest route a player must take from the start of a level to its end, through every required objective. Everything else is optional space. Measuring the critical path in seconds is one of the first things you do in a blockout, because it sets the pace of the whole level (week 3) and the recovery times of every checkpoint (week 1).

## 2. Worked example: why grey first?

### The puzzle

Valve's first Half-Life (1998) went through a restart, the story behind [GD101 week 8's loop clock](../../GD101-introduction-to-game-design/lectures/w08-iteration-loops-and-kill-your-darlings.md). This week looks at what happened next. During that year, a small cross-disciplinary group called the Cabal designed the game in long weekly sessions, and Valve ran over two hundred playtest sessions with outside volunteers. Observers sat behind each player and took notes without helping. A typical session produced around a hundred action items.

Two hundred sessions at about a hundred items each is on the order of twenty thousand things to look at. If each of those took a day of work, the fixes alone would take one person about eighty years. So how does a team afford to act on that much feedback? The answer is that most fixes were cheap when they were made. This section builds a model of why.

### The model

Picture a level with `N` layout problems: a door players miss, a fight that is too cramped, a jump that is too long. Nobody knows `N`. Playtests reveal problems a round at a time.

- `f` is the **discovery rate**: the fraction of the remaining problems that one round of testing finds and fixes. GD101 week 7 showed where a number like this comes from. Five testers who each have a 30% chance of hitting a given problem reveal it with probability `1 − 0.7⁵ ≈ 0.83`.
- `c` is the **round cost**: hours for one round of testing plus the revisions it triggers. It depends on how finished the level is. Moving a wall in a blockout takes minutes. Moving it after the art pass means re-modelling, re-texturing and re-lighting.
- `B` is the **budget** in hours.

After `k` rounds, the expected number of problems left is:

```
remaining after k rounds = N × (1 − f)^k
rounds that fit in the budget, k = floor(B / c)
```

This is exponential decay, the same shape as MA101 week 4 in reverse. Each round removes a fixed fraction of what is left.

So far the model only says "cheaper rounds are better," which you knew. Two facts about real projects make it more interesting.

1. **The level has to get its art at some point.** Call the one-time cost of the art pass `A` hours. After it, every round costs the art-fidelity price `c_a` instead of the greybox price `c_g`.
2. **Some problems can only be found after art.** A pickup that disappears against a busy texture, a path that lighting hides, a landmark that isn't one yet. Call their number `M`. They appear when the art arrives.

Now a plan has one decision in it: the **switch point** `S`, the number of hours you spend greyboxing before starting the art pass. The problems left at ship are:

```
greybox rounds       g = floor(S / c_g)
art rounds           a = floor((B − S − A) / c_a)
problems at ship     R = ( N × (1 − f)^g  +  M ) × (1 − f)^a
```

The first bracket is what survives the greybox, plus the new art-only problems. The last factor is what the art rounds remove.

### Numbers you can check

Use these values, invented for a small level: `N = 40` layout problems, `M = 6` art-only problems, `f = 0.5`, a budget of `B = 80` hours, an art pass of `A = 32` hours, greybox rounds of `c_g = 4` hours and art rounds of `c_a = 16` hours.

| Switch point `S` (h) | Greybox rounds `g` | Left after greybox | Art rounds `a` | Problems at ship `R` |
|---|---|---|---|---|
| 0 (art first) | 0 | 40 + 6 = 46 | 3 | 5.75 |
| 8 | 2 | 10 + 6 = 16 | 2 | 4.00 |
| 16 | 4 | 2.5 + 6 = 8.5 | 2 | 2.13 |
| 24 | 6 | 0.63 + 6 = 6.63 | 1 | 3.31 |
| 32 | 8 | 0.16 + 6 = 6.16 | 1 | 3.08 |
| 48 (grey to the end) | 12 | 0.01 + 6 = 6.01 | 0 | 6.01 |

Check the best row by hand. Four greybox rounds halve 40 four times, leaving 2.5. The art adds 6, for 8.5. The remaining `80 − 16 − 32 = 32` hours buy two art rounds, and `8.5 × 0.25 = 2.125`.

Two things stand out. Both extremes are bad. Art first ships with 5.75 problems because it can afford only three expensive rounds. Grey to the end ships with 6 because it never looks for the art-only problems at all. **The best plan greyboxes until the layout problems are mostly gone, then leaves enough time for at least two rounds on the finished art.**

You can reproduce the table with this code:

```python
def problems_at_ship(S, N=40, M=6, f=0.5, B=80, A=32, c_g=4, c_a=16):
    g = S // c_g                    # greybox rounds
    a = (B - S - A) // c_a          # art rounds after the art pass
    return (N * (1 - f) ** g + M) * (1 - f) ** a

for S in (0, 8, 16, 24, 32, 48):
    print(f"S = {S:2d} h -> {problems_at_ship(S):.2f} problems at ship")
best = min(range(0, 49, 4), key=problems_at_ship)
print("best switch point:", best, "h")
print("with no art-only problems:", [round(problems_at_ship(S, M=0), 2) for S in (16, 32, 48)])
```

```
S =  0 h -> 5.75 problems at ship
S =  8 h -> 4.00 problems at ship
S = 16 h -> 2.12 problems at ship
S = 24 h -> 3.31 problems at ship
S = 32 h -> 3.08 problems at ship
S = 48 h -> 6.01 problems at ship
best switch point: 16 h
with no art-only problems: [0.62, 0.08, 0.01]
```

(Python rounds 2.125 to 2.12 when printing. The exact value is 2.125.)

The last line matters. If art revealed nothing new (`M = 0`), greyboxing to the very end would always win. **The best switch point exists because some problems are invisible in grey.** How early you switch is really a bet on how many of those there are.

Open the interactive. The left view is a timeline of your 80 hours, split into greybox rounds, the art pass and art rounds, with a step curve of problems remaining that drops at each round and jumps up by `M` when the art lands. The right view plots problems at ship against the switch point for every `S` from 0 to 48. Drag `S` and watch the marker slide along the U. Then set `M` to 0 and watch the U flatten into a slope that runs downhill all the way to the right.

### Cross-game recognition

**Half-Life (Valve, 1998).** Birdwell's account describes the regime the model calls high `k` and high `f`. Many rounds, each with silent observation of real players, each producing a long list of fixes. Levels were edited by several designers in turn, one handling geometry, another monsters, another lighting. That split is its own way to keep `c` low, since a lighting pass doesn't reopen the layout. Later in development Valve also recorded where players were and what happened to them, which raises `f` by catching problems the observers missed. Week 14 comes back to that with heatmaps.

**The Elder Scrolls V: Skyrim (Bethesda, 2011).** Burgess and Purkeypile report that the game has more than 300 dungeons and that about ten of the roughly ninety developers were directly responsible for them. Bethesda's answer to the model is to shrink `c_a` itself. Artists build **kits**, sets of modular pieces that snap together on a grid, and the kits go through their own proof and graybox phases (one to three weeks and one to four weeks in their description) before the final art is built. Once a kit exists, level designers lay out dungeons directly with final-art pieces and play them almost at once. Rerun the model with `c_a = 8` instead of 16 and the best plan ships with 0.5 problems instead of 2.1, and the art-first plan drops to 0.72. Kits make art-fidelity rounds nearly as cheap as grey ones. The cost moves elsewhere. The kit constrains shapes, and Burgess names the risk of repetitive-looking spaces, which they call art fatigue.

**Neon White (Angel Matrix, 2022).** The Level Design Book reports, citing Game Informer, that one of its levels went through more than fifty changes over three years. A speedrunning game lives or dies on the timing of every route, so it needs a very large `k`. That many rounds is only affordable if most of them change cheap geometry.

**Dirty Bomb (Splash Damage, 2015).** Massey's 8 to 12 second spawn-to-objective target is a problem of the kind greybox finds well, with `f` close to 1. One playtest shows whether the run feels long. It is also a problem that stays found. Art doesn't change the distance, so it adds nothing to `M`.

Rewrite all four in the model's terms and they are one idea. Raise `k` by keeping `c` low, raise `f` by testing with real players, and don't pretend `M` is zero.

### Design judgment, eyes open

- **Greybox is a price, not a style.** Its value is the low `c_g`. Anything that makes grey rounds slow (waiting for builds, needing an artist to move a wall, perfectionism about grey geometry) erodes the reason to do it.
- **Name your art-only problems in advance.** Readability, lighting-led guidance (week 4) and landmark visibility can't be judged in grey. If your level depends on them, switch earlier or do a rough lighting pass inside the greybox.
- **Art raises the emotional price of change, too.** GD101 week 8 covered the sunk-cost trap. Once a room looks finished, teams defend it. The model counts hours. It doesn't count the reluctance, so the real `c_a` is usually higher than your estimate.
- **Greybox can mislead stakeholders.** People outside design often can't judge a grey level and may reject a good layout or approve a bad one. Show them play footage with a short explanation, not screenshots.
- **Decide what is precious.** Reece's distinction on World's Edge is worth copying. Before the art pass, list the few layout facts that must survive (a sightline, a route length, a cover position), so the art pass can change everything else freely.

## 3. Building the blockout: grids, footprints and the critical path

### Work on a grid, and choose sizes that tile

Blockouts are built on a **grid**: every wall, floor and step snaps to a fixed spacing. The grid keeps pieces aligned and makes distances easy to read. The Level Design Book suggests coarse grids based on player width, for example 32 to 64 units in Doom or Quake, 1 to 2 metres in Unity, and 50 to 128 units in Unreal.

When you build from reusable pieces, whether grey boxes or a kit, every piece has a **footprint**: the full box it occupies on the grid. Burgess and Purkeypile give the rule that footprints must be multiples of each other. A 512-unit room tiles with a 256-unit corridor, because every edge of the room lands on the corridor's grid. A 384-unit room does not. Chain two of them and the second ends at 768, which is fine. Chain one and turn a corner, and the room's far edge sits at 384, halfway between two 256-unit grid lines. Loops that should close leave a 128-unit gap or overlap.

The arithmetic is the least common multiple. Two pieces realign every `lcm(a, b)` units. For 512 and 256 that is 512, one room. For 384 and 256 it is 768, and every junction in between is off-grid. They also recommend a snap size of half the footprint, and building walls inside the footprint rather than on its edge, so two pieces placed side by side don't overlap.

For your blockouts this semester, pick one base unit (1 metre in Unity and Godot, 100 units in Unreal, 64 units in Trenchbroom) and make every room and corridor a whole multiple of it.

### Measure the critical path in seconds

Once the level runs, walk the critical path and time it, then measure its length along the floor. The two should agree: `time ≈ length / speed`. If they don't, something is slowing the player that you didn't plan (a door that needs lining up, a corner the camera fights, a stair the controller catches on). Record the critical path time every round. It is the first number anyone asks about a level.

On a grid you can also compute path lengths before playing. Treat each grid cell as a node and each open neighbour as an edge. The shortest route is a breadth-first search, the same one you meet in the programming courses. Lab 02 gives you a small tool that does this on a text grid, so you can check your blockout's timings against your stopwatch.

### A round, written down

Keep a **revision log** for every blockout. One row per round, with the date, testers, critical path time, problems found (observed behaviour, not your interpretation, as GD101 week 7 insisted), the change made for each, and the hours spent. The log is how you measure your own `f` and `c`, and after two or three levels you will know them well enough to plan a schedule with the model above.

## In-class activity (25 minutes)

In pairs, with squared paper (1 square = 1 metre) and a ruler.

1. **(10 min)** Block out the first three beats of one partner's Lab 01 paper level as a top-down plan. Use a scale figure of 1 × 1 square, doorways at least 2 squares wide, and room sizes that are multiples of 4 squares.
2. **(5 min)** Mark the critical path. Measure it in squares and convert to seconds at 6 m/s.
3. **(5 min)** Swap sheets with another pair. They walk the path with a pencil tip, out loud, and name every place they are unsure where to go. You write down what they say without explaining.
4. **(5 min)** Count the problems found. Estimate `f` for your group from how many of the problems you had already suspected. Decide one change and redraw it.

Expected output: the plan with the critical path, its length and time, the list of problems, and your estimate of `f`.

## Common misconceptions

- **"The greybox is just a rough version of the art."** It is a measuring instrument. Its dimensions, routes and timings are final unless a test says otherwise. Its looks are not.
- **"More time in greybox is always better."** Only if art reveals nothing new. With art-only problems, greyboxing too long leaves no time to find them, which is the right-hand side of the U.
- **"Grid size is cosmetic."** Pieces whose footprints aren't multiples of each other stop lining up the moment a layout loops back on itself.
- **"If it measures right in the editor, it plays right."** The editor camera flies. The player walks at eye height with a real controller. Time it in the game.

## Check yourself

1. A level has `N = 30` problems. Each round finds 40% of what is left. How many are expected to remain after a 30-hour budget with 5-hour rounds? With 15-hour rounds?
2. In the lecture's example (`N = 40`, `M = 6`, `f = 0.5`, `B = 80`, `A = 32`, `c_g = 4`, `c_a = 16`), compute `R` for `S = 12`. Is it better or worse than `S = 16`, and why does the step from 12 to 16 help?
3. A kit reduces `c_a` from 16 to 8 hours and leaves everything else the same. Compute `R` for `S = 0` and `S = 8`. What does this say about Bethesda's choice to lay out dungeons with final-art kits?
4. Your corridor piece is 3 metres long. Which room sizes, 6, 8, 9 or 10 metres, tile with it on a loop? What is the smallest room that tiles with both a 3 m and a 4 m corridor?

<details>
<summary>Answers</summary>

1. 5-hour rounds: `k = 6`, remaining `30 × 0.6⁶ ≈ 1.40`. 15-hour rounds: `k = 2`, `30 × 0.6² = 10.8`. The same budget leaves nearly eight times as many problems.
2. `g = 3`, so `40 × 0.125 = 5`, plus 6 gives 11. Art rounds `a = floor((80 − 12 − 32)/16) = floor(2.25) = 2`, so `R = 11 × 0.25 = 2.75`. Worse than 2.125. The extra greybox round at 16 hours halves 5 to 2.5 before the art, and the budget still covers two art rounds, so it is free.
3. `S = 0`: `a = floor(48/8) = 6`, `R = 46 × 0.5⁶ ≈ 0.72`. `S = 8`: `g = 2`, `a = floor(40/8) = 5`, `R = 16 × 0.5⁵ = 0.5`. With cheap art rounds, art first is almost as good as the best plan. Kits pay for themselves by making the art stage iterable.
4. Multiples of 3: 6 and 9 tile, 8 and 10 do not. The smallest room that tiles with both a 3 m and a 4 m corridor is `lcm(3, 4) = 12` metres.

</details>

## Lab / assignment hook

[Lab 02, blockout and critical path](../labs/lab02.md). You finish a small path-measuring tool for text-grid blockouts, then build your Lab 01 level as a playable blockout in an engine of your choice, run three test rounds, and keep a revision log with critical-path times. This blockout is the first graded blockout of the semester.

## Sources

- The Level Design Book, "Blockout" (book.leveldesignbook.com, accessed September 2026). Definition and synonyms; include and exclude list (gridded floor, scale figure, walls at 150-200% figure height, doorways at least twice figure width); wrong scale as the most common beginner problem; suggested grid sizes by engine; case studies of Dirty Bomb's Castle map (Anthony Massey, 8-12 s spawn to objective, 8v8), Apex Legends' World's Edge (Rodney Reece, precious versus flexible) and Neon White (more than 50 changes to one level over three years, citing Blake Hester in Game Informer #350; the magazine itself was not checked).
- Birdwell, K. (1999, December 10). "The Cabal: Valve's Design Process for Creating Half-Life." Game Developer. Restart in late 1997 and a delay of about a year; the Cabal group; more than 200 playtest sessions with silent observers; about 100 action items per session; several designers working on each level in turn; later automatic recording of player data.
- Burgess, J. & Purkeypile, N. (2013). "Skyrim's Modular Approach to Level Design." Level Design in a Day, GDC 2013. Transcript on blog.joelburgess.com, 19 April 2013. 300+ dungeons, about 10 of about 90 developers responsible for dungeons; kit proof phase of 1-3 weeks and graybox phase of 1-4 weeks; footprints as multiples of each other (512 with 256 tiles, 384 does not); snap at half the footprint; art fatigue.
- Totten, C. W. (2019). *An Architectural Approach to Level Design* (2nd ed.). CRC Press.
- The greybox budget model and all values of `N`, `M`, `f`, `A`, `B`, `c_g` and `c_a` are teaching models built for this lecture, not measurements of any studio's process.

## Interactive spec: examples/w02-greybox-budget.html

**Purpose.** Show that the best time to leave greybox is a trade-off. Cheap grey rounds remove layout problems fast, but some problems only appear once art is in, and those need expensive art rounds.

**The one insight the visual must make obvious.** With the defaults, the right-hand chart is a U with its lowest point at `S = 16`. Setting `M` to 0 turns the U into a downhill slope whose lowest point is at the far right. Lowering `c_a` to 8 flattens the U so art-first is nearly as good as the best plan.

**Layout.** Mobile (390px): timeline on top, U chart below, controls, numbers panel. Desktop (1280px): timeline and U chart side by side, controls and numbers below.

- Left view, "Your 80 hours": x axis hours 0 to `B`. A coloured band under the axis splits it into greybox rounds (one segment each, width `c_g`), the art pass (width `A`, hatched), art rounds (width `c_a` each) and unused hours (pale). Above it, a step curve of expected problems remaining: starts at `N`, multiplies by `1 − f` at the end of each round, jumps up by `M` at the end of the art pass. Label the final value.
- Right view, "Problems at ship vs switch point": x axis `S` from 0 to `B − A` in steps of `c_g`, y axis `R`. Dots joined by a line. The current `S` is a large marker. The minimum is marked with a label "best: S = 16 h, 2.13 problems".

**Controls.** `S` slider 0 to `B − A` (step = `c_g`, default 16). `N` 10 to 100 (default 40). `M` 0 to 20 (default 6). `f` 0.1 to 0.9 (step 0.05, default 0.5). `B` 20 to 200 (step 2, default 80). `A` 0 to 64 (step 4, default 32; 0 lets you model a greybox-only budget, as check question 1 needs). `c_g` 1 to 16 (default 4). `c_a` 4 to 40 (default 16). Presets: "Defaults", "No art-only problems (M = 0)", "Kits (c_a = 8)", "Art first (S = 0)". Reset.

**Formulas.** `g = floor(S / c_g)`, `a = floor((B − S − A) / c_a)` (0 if negative), `R = (N × (1 − f)^g + M) × (1 − f)^a`. Unused hours `= B − S − A − a × c_a` (if `B − S − A < 0`, show "art pass does not fit" and `R = N + M`). The timeline step curve uses the same rounds in order.

**Numbers panel.** `g`, `a`, left after greybox (2 decimals), `R` (2 decimals), unused hours, best `S` and its `R`, and a sentence built from the data, for example "Greyboxing for 16 h leaves 8.50 problems after art; two art rounds bring it to 2.13."

**Test values.**

- Defaults: `R` at `S` = 0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48 is 5.75, 6.50, 4.00, 2.75, 2.13 (2.125), 3.63, 3.31, 3.16, 3.08, 6.08, 6.04, 6.02, 6.01. Best `S = 16`.
- `M = 0`: `R` at 16, 32, 48 is 0.63 (0.625), 0.08 (0.078), 0.01 (0.0098). Best `S = 48`.
- `c_a = 8`: `R` at `S = 0` is 0.72 (0.719), at `S = 8` is 0.50, best `S = 8`.
- Check question 1 via a preset-free setting: `N = 30`, `M = 0`, `f = 0.4`, `A = 0`, `B = 30`, `c_g = 5`, `S = 30` gives 1.40.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`, light and dark. Greybox, art pass and art rounds differ by pattern (solid, hatched, dotted) as well as colour. All sliders are native range inputs with visible numeric values and keyboard steps. Respect reduced motion (no animated step curve). No game art, logos or screenshots.

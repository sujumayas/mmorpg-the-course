# GD201 · Week 03 — Flow, pacing and intensity graphs

**Why this matters:** Two levels can hold exactly the same enemies and still feel completely different. One wears players out and the other keeps them leaning forward, and the difference is the spacing. Pacing is the one part of a level you can draw on paper before anyone plays, and fix cheaply while it is still a line on a chart.

**You will be able to:**
- Write a beat chart for a level and turn its encounter list into an intensity graph.
- Compute an intensity curve with a stock-and-decay rule, and measure its peak time, calm time and number of peaks.
- Explain the pacing cycle of Left 4 Dead's AI Director and rewrite it as a rule on the same curve.
- Critique a level's pacing against a target shape, redesign it without changing its total threat, and say what fixed pacing can't do in a shared world.

**Before class:** Michael Booth, "The AI Systems of Left 4 Dead" (Valve, 2009, slides on Valve's publications page), the section headed "Generate dramatic game pacing" (about 15 slides). Totten, *An Architectural Approach to Level Design* (2nd ed., 2019), the material on pacing and rhythm in level layouts. Reread your notes on flow channels from UX201 week 3.

**Prerequisites from earlier courses:** [GD102 week 2, stocks and flows](../../GD102-systems-design-and-game-mechanics/lectures/w02-stocks-and-flows.md) (a stock with an outflow proportional to its size, and its equilibrium). [GD102 week 4, negative feedback](../../GD102-systems-design-and-game-mechanics/lectures/w04-negative-feedback-loops-rubber-banding.md) (a rule that pushes a value back toward a target). Running alongside this course, [UX201 week 3, flow and difficulty](../../UX201-game-ux-and-player-psychology/lectures/w03-flow-and-difficulty.md) (the psychological meaning of flow). From this course, [week 1](w01-level-design-as-teaching.md) (beats and the lesson matrix) and [week 2](w02-blockout-and-greyboxing.md) (critical-path times, which give each beat its duration).

**Interactive:** [`examples/w03-intensity-graph.html`](../examples/w03-intensity-graph.html). Keep it open during section 2.

---

## 1. Flow and pacing: two words, three meanings

Level designers use "flow" for two different things, and it's worth separating them before we draw anything.

- **Spatial flow** is how players move through a space. Where the routes go, where they merge, where people bunch up or get lost. A level "flows well" when players find their way without stopping to think about it. Weeks 4 to 7 are about spatial flow.
- **Flow as a mental state** is the psychologist Mihaly Csikszentmihalyi's term for full absorption in a task whose challenge matches your skill. UX201 week 3 covers it in detail, including the flow channel between boredom and anxiety.

**Pacing** connects them. It is how the demands a level puts on the player change over time. A level that stays at one level of demand pushes players out of the flow channel eventually, either into boredom or into fatigue. A level that rises and falls can keep them in it for much longer.

We'll use three tools this week.

- A **beat chart** is a table with one row per beat (week 1's unit): its type, its duration, its target intensity and what it introduces. You write it before you build.
- An **intensity graph** is a curve of how intense the level is over time. You can draw one by hand from the beat chart, compute one from the encounter list, or record one from a playtest.
- An **intensity model** is the rule that turns events into a curve. This week's model is simple enough to compute by hand, and it is close to the one a famous shipped game used.

**Intensity** here means how hard the level is pressing on the player right now: threat, damage, noise, time pressure. It is not the same as difficulty. A hard puzzle in a quiet room is high difficulty and low intensity. A crowd of weak enemies rushing at you is low difficulty and high intensity.

## 2. Worked example: the drip, the wave and the Director

### The puzzle

Left 4 Dead (Valve, 2008) is a co-operative shooter in which four survivors cross a map from one safe room to the next while infected attack them. Players who replay the same map notice two things. The fights happen in different places each time. And yet there is always a moment to breathe: after a big rush, the map goes quiet for a while.

That is not an accident. Michael Booth's 2009 talk on the game's AI describes a system called the AI Director that estimates how intense the game currently is for each survivor and shapes the flow of enemies to produce peaks and valleys. Booth says the team took the idea from watching Counter-Strike rounds, whose pacing is spiky: quiet tension broken by sudden fights. His summary of the lesson is that constant combat is fatiguing and long inactivity is boring.

So here is the puzzle. Give a designer 180 "units" of threat to spend over three minutes. Spread evenly, it is the same total as bunched into waves. Why do players experience the two so differently? To answer, we need a model of intensity.

### The model

Treat intensity as a **stock**, in the GD102 week 2 sense. Events pour into it. It drains away on its own over time. Split the level into steps of 10 seconds and write:

```
I[k] = d × I[k − 1] + E[k]
```

- `I[k]` is the **intensity** at the end of step `k`. It starts at 0.
- `E[k]` is the **threat** that arrives during step `k`, in whatever units your team agrees on (for example, one unit per point of expected damage, or per enemy weighted by danger).
- `d` is the **decay factor** per step, between 0 and 1. It says how much of the last step's intensity is still there. This lecture uses `d = 0.5`, so intensity halves every 10 seconds with no new threat. That half-life is a teaching choice, not a value taken from any game.

This is exactly the stock from GD102 week 2 whose outflow is proportional to its size. You met its **equilibrium** there. Feed a constant `E` every step and `I` settles where the inflow equals the outflow:

```
I* = E / (1 − d)
```

With `d = 0.5`, a constant drip of 10 settles at 20.

To read a curve, we need a few measurements. Pick two thresholds, a **peak** threshold (here 35) and a **calm** threshold (here 10).

- **Peak time**: seconds with `I ≥ 35`.
- **Calm time**: seconds with `I < 10`.
- **Peaks**: how many separate times the curve crosses up through 35.
- **Maximum**: the highest value of `I`.

### Numbers you can check

Three designs for the same three-minute stretch (18 steps). Each spends exactly 180 units of threat.

- **A, the drip.** 10 units every step. A steady trickle of enemies.
- **B, the authored wave.** `0, 5, 10, 15, 20, 30, 40, 0, 0, 0, 0, 5, 10, 15, 30, 0, 0, 0`. A build to a big fight, a long quiet stretch, then a second, smaller build.
- **C, the Director rule.** Send a full population of 20 units per step until intensity reaches 35. Then send nothing for 3 steps (30 seconds). Repeat. This is a stripped-down version of Left 4 Dead's cycle, described below.

Here are the first six steps of each, which you can check by hand.

| Step (end, s) | A: `E` | A: `I` | B: `E` | B: `I` | C: `E` | C: `I` |
|---|---|---|---|---|---|---|
| 1 (10) | 10 | 10.0 | 0 | 0.0 | 20 | 20.0 |
| 2 (20) | 10 | 15.0 | 5 | 5.0 | 20 | 30.0 |
| 3 (30) | 10 | 17.5 | 10 | 12.5 | 20 | 35.0 |
| 4 (40) | 10 | 18.8 | 15 | 21.3 | 0 | 17.5 |
| 5 (50) | 10 | 19.4 | 20 | 30.6 | 0 | 8.8 |
| 6 (60) | 10 | 19.7 | 30 | 45.3 | 0 | 4.4 |

Check one cell. Design B, step 6: `0.5 × 30.625 + 30 = 45.3`. Design C, step 4: C crossed 35 at step 3, so step 4 sends nothing and `I = 0.5 × 35 = 17.5`.

Over the whole three minutes:

| Design | Total threat | Maximum | Peak time (`I ≥ 35`) | Calm time (`I < 10`) | Peaks |
|---|---|---|---|---|---|
| A, drip | 180 | 20.0 | 0 s | 0 s | 0 |
| B, authored wave | 180 | 62.7 | 30 s | 60 s | 2 |
| C, Director rule | 180 | 35.6 | 30 s | 60 s | 3 |

The drip never peaks and never rests. It sits at 20, its equilibrium, for the whole three minutes. Nothing about it is dangerous, and nothing about it ever lets up. It is Booth's "constant combat," at a volume too low to be exciting. The wave and the Director rule spend the same threat and produce clear peaks with a full minute of calm in between. The totals are identical. The shape is what players feel.

You can reproduce both tables with this code:

```python
def intensity(E, d=0.5):
    I, curve = 0.0, []
    for e in E:
        I = d * I + e
        curve.append(I)
    return curve

def director(steps, full=20, peak=35, relax=3, d=0.5):
    I, rest, E = 0.0, 0, []
    for _ in range(steps):
        e = 0 if rest > 0 else full
        rest = max(0, rest - 1)
        I = d * I + e
        E.append(e)
        if e > 0 and I >= peak:
            rest = relax
    return E

def measure(curve, peak=35, calm=10):
    peaks = sum(1 for k, x in enumerate(curve) if x >= peak and (k == 0 or curve[k - 1] < peak))
    return max(curve), 10 * sum(x >= peak for x in curve), 10 * sum(x < calm for x in curve), peaks

designs = {
    "A drip": [10] * 18,
    "B wave": [0, 5, 10, 15, 20, 30, 40, 0, 0, 0, 0, 5, 10, 15, 30, 0, 0, 0],
    "C director": director(18),
}
for name, E in designs.items():
    top, hot, quiet, n = measure(intensity(E))
    print(f"{name:10s} total {sum(E)}  max {top:5.1f}  peak {hot:2d} s  calm {quiet:2d} s  peaks {n}")
```

```
A drip     total 180  max  20.0  peak  0 s  calm  0 s  peaks 0
B wave     total 180  max  62.7  peak 30 s  calm 60 s  peaks 2
C director total 180  max  35.6  peak 30 s  calm 60 s  peaks 3
```

Open the interactive. The top view is the encounter list as a bar chart: one bar per 10-second step, showing `E`. The bottom view is the intensity curve with the peak and calm bands shaded. Switch between A, B and C, and notice that the bars' total stays at 180 while the curve changes shape. Then drag bars in B to move threat around. Try to make the curve peak three times without raising the total.

### How Left 4 Dead does it

Booth's slides describe the Director's intensity estimate in words, and it maps onto the model almost term for term.

- Each survivor has an intensity value. It **rises** when the survivor is hurt (in proportion to damage taken), is incapacitated, is pulled or pushed off a ledge, or when an infected dies nearby (more for closer kills). Those are the `E` terms.
- It **decays toward zero** over time. That is `d`. One detail our model skips: it does not decay while infected are actively attacking that survivor.
- The Director tracks the **highest** intensity among the four survivors and runs a cycle of four phases. **Build Up** sends a full population of threats until intensity crosses a peak threshold. **Sustain Peak** keeps the full population for 3 to 5 seconds more. **Peak Fade** switches to a minimal population and waits for intensity to drop out of the peak range, so a fight in progress can finish. **Relax** keeps the population minimal for 30 to 45 seconds, or until the survivors have travelled far enough toward the next safe room, then returns to Build Up.
- Boss infected are **not** controlled by this cycle. Booth notes they change the pacing on their own, which is part of their job.
- Booth's own summary is that the algorithm changes the pacing, not the difficulty. The size of the threat stays the same. The timing moves.

Our design C is that cycle with the sustain and fade phases folded in and the relax set to 30 seconds. In GD102 week 4 terms, it is a negative feedback loop: when intensity gets high, the rule removes inflow until it falls.

### Cross-game recognition

**Left 4 Dead (2008).** The model above, run live, with intensity measured from what actually happens to each player. Structured randomness adds variety on top. Booth gives mob spawns on Normal difficulty a random interval of 90 to 180 seconds, so the timing of peaks differs between runs while the shape stays.

**Counter-Strike (the versions Booth refers to, around 2000 to 2008).** Booth cites its "spiky" pacing as the inspiration. Rewrite a round in our terms. Most of the round is low `E` (moving, listening, holding angles) with intensity near zero. Then a firefight delivers a burst of `E` in a few seconds. The start of each round, before the teams meet, is a calm phase built into the rules. Nobody authored a curve. The rules and the map produced it.

**Resident Evil series (1996 onward).** In the early games, safe rooms hold the typewriter used for saving and the item box, and they have their own music, a separate quiet track in Resident Evil 2 (1998) and its 2019 remake. In our model, a safe room is a place where the space itself sets `E = 0` for as long as the player stays. The designers didn't need a Director to create a valley. They built one out of walls and a soundtrack, and put it where the curve needs it.

**World of Warcraft dungeons (original game and The Burning Crusade era values).** A group clears a dungeon one **pull** at a time: a pack of enemies is a pulse of `E`. Between pulls, casters sit and drink to restore mana. The vendor drinks of that era restore mana over 18 to 30 seconds and require the character to sit. That drink break is a relax phase of 18 to 30 seconds built into the resource system, and the group, not the designer, decides when the next pulse comes. Pacing is still there. Control of it has moved to the players.

Four games, one shape. A pulse of threat, a decay, and a valley that is either computed (Left 4 Dead), emergent from the rules (Counter-Strike), built into the space (Resident Evil) or built into a resource loop (World of Warcraft).

### Design judgment, eyes open

- **Constant intensity is a choice, and usually a bad one.** The drip's problem is not its level but its flatness. If you want sustained pressure (a horde mode, a final escape), make it short and follow it with a long valley.
- **Valleys need content.** Calm doesn't mean empty. The best rests hold a reward, a view, a story beat or a safe place to manage inventory. Resident Evil's safe rooms work because they are useful as well as quiet.
- **The model is crude, and that's fine.** Booth describes the Director's intensity estimate as crude but effective. Your `d` and your threat units are guesses. Choose them once, write them down, and use them the same way across every level so that comparisons mean something.
- **Authored or adaptive?** An authored wave (B) gives you exact control and the same experience every time, which suits a story level. An adaptive rule (C) reacts to the player and varies between runs, which suits replayable co-op. Adaptive pacing also hides the designer's hand. Players rarely notice it, so they can't learn to exploit it, but you can't promise a specific moment to a writer either.
- **Pacing and difficulty are separate dials.** Booth's point that the Director changes timing, not size, is worth copying. When a playtest says "too hard," check whether the real problem is too little calm between peaks before you weaken the enemies.
- **Shared worlds lose the script.** In an open MMO zone, twenty players meet the same camp at different times, with different groups and cooldowns. You can't author one curve for all of them. You can shape the parts of it you control: the spacing of camps along a road, the placement of safe spots and vendors, and the time between points of interest, which week 9 turns into its own worked example.

## 3. Writing a beat chart

A beat chart is a planning table. You write it before the blockout and check the blockout against it after. Here is one for the Flooded Mill from week 1. Durations come from walking the week 2 blockout.

| Beat | Type | Duration (s) | Target intensity (0-5) | New mechanic | Notes |
|---|---|---|---|---|---|
| 1. Dock | Traversal | 40 | 1 | Grapple (introduce) | No enemies. Water under the gap. |
| 2. Water wheel | Traversal and light combat | 60 | 2 | — | Two weak enemies after the grapple. |
| 3. Sluice | Combat | 50 | 3 | Swinging hazard (introduce) | First real fight near the hazard. |
| 4. Mill loft | Rest | 40 | 0 | — | Health pickup, view of the rooftop goal. |
| 5. Gear room | Combat | 70 | 4 | — | Combine grapple and hazard in a fight. |
| 6. Stairwell | Rest | 20 | 1 | — | Short calm before the climax. |
| 7. Rooftop | Combat, climax | 60 | 5 | — | Test of all three verbs. |

A few rules of thumb, each one a statement about the intensity curve.

- **Rest after a peak.** Beats 4 and 6 follow the two big fights. With `d = 0.5` per 10 seconds, 40 seconds of rest takes intensity down to about 6% of its peak. 20 seconds takes it to 25%.
- **Peaks rise toward the climax.** Targets go 3, then 4, then 5. A level whose biggest fight is in the middle feels as if it ends early.
- **Never introduce during a peak.** Match the chart against week 1's lesson matrix. New mechanics sit in beats with intensity 1 to 3, never 4 or 5.
- **Rests point forward.** The loft has a view of the rooftop. A calm beat that shows the player where they are going turns rest into anticipation. Week 4 builds this into landmarks and weenies.
- **Check the total.** Add up the durations (here 340 seconds) and compare with the critical-path time from your blockout plus the expected fight times. If the chart and the blockout disagree, one of them is wrong.

To turn the chart into an intensity graph, draw each beat as a block of its target height and duration, then smooth the edges by eye. Or convert each fight into `E` values per 10-second step and compute the curve with the model, which is what Lab 03 does.

## 4. Pacing lives in space

Pacing is time, but you build it out of space. Some layout choices raise or lower intensity before any enemy is placed.

- **Room size and shape.** A narrow corridor limits how many enemies can reach the player at once and reads as a transition. A large arena lets threat arrive from several directions and reads as a peak. Week 6 covers combat spaces in detail.
- **Sightlines.** A long view of an enemy group lets tension build before the fight. A blind corner delivers the whole pulse at once.
- **Distance.** Walking time between beats is a valley whether you design it or not. In week 2 you measured it. Here you decide whether it is long enough to rest in, or so long that it becomes boredom.
- **Safe spaces.** A closable door, a save point, a vendor. Any place the rules make safe sets `E` to zero, as Resident Evil's safe rooms do.

Your intensity graph and your blockout should tell the same story. If the graph wants a rest and the blockout puts the player in an open field with three patrol routes crossing it, change one of them.

## In-class activity (25 minutes)

In groups of three, with a stopwatch and a shared sheet.

1. **(10 min)** One student plays five minutes of an action game level (or the group watches a five-minute recorded run). One student calls out threat events. One logs, every 10 seconds, a threat score `E` from 0 to 40 using the scale agreed in advance: 5 per weak enemy engaging, 15 per strong one, 10 for taking a big hit.
2. **(5 min)** Compute the intensity curve with `d = 0.5` in a spreadsheet or by hand. Measure maximum, peak time, calm time and number of peaks.
3. **(5 min)** Sketch the beat chart you think the designers wrote. Where is their rest after each peak? Is it in time, in space (a safe area) or missing?
4. **(5 min)** Propose one change that adds a valley without removing any threat. Recompute.

Expected output: the `E` log, the curve with its four measurements, the reconstructed beat chart and the redesigned `E` list with its new measurements.

## Common misconceptions

- **"More action is more exciting."** Past its equilibrium, a steady flow of action only holds intensity flat. Peaks come from contrast, which needs calm around them.
- **"Pacing is the same as difficulty."** The Director changes timing, not size. A level can be easy and badly paced, or hard and well paced.
- **"Rests are wasted time."** A rest is where players recover, take stock and look ahead. Filled with a reward or a view, it is one of the most valuable beats in a level.
- **"The intensity graph is a measurement."** It's a model with a chosen `d` and chosen threat units. It becomes useful when you use the same choices every time and check them against playtests.

## Check yourself

1. With `d = 0.5`, compute `I` for the encounter list `E = 30, 0, 0, 30`. Is the second pulse's peak higher or lower than the first, and why?
2. A designer wants a steady horde section to hold intensity exactly at the peak threshold of 35. With `d = 0.5`, what constant `E` per step does that take? Using design A as a guide, what will players feel after a minute of it?
3. Run the Director rule by hand with `full = 20`, `peak = 35`, `relax = 3` for steps 7 to 9, starting from `I = 4.38` after step 6. Does the second peak arrive at the same step count after the rest as the first did?
4. Left 4 Dead's Relax phase lasts 30 to 45 seconds. In this lecture's model, by what fraction does intensity fall across 30 seconds of relax? Across 45? What would happen to that fraction if the team chose a half-life of 20 seconds instead?

<details>
<summary>Answers</summary>

1. `I = 30, 15, 7.5, 33.75`. The second peak is higher (33.75 against 30) because 3.75 of the first pulse is still there. Pulses spaced closer than the decay can clear stack up. Spaced far apart, they don't.
2. `I* = E / (1 − d)`, so `E = 35 × 0.5 = 17.5` per step. Like the drip, it will rise to the threshold and sit there with no calm and no further peaks. After a minute it reads as noise, not climax. Make it short and give it a valley after.
3. Step 7: `0.5 × 4.38 + 20 = 22.19`. Step 8: `31.09`. Step 9: `35.55`, which crosses 35. The first peak took 3 steps from zero, and this one also takes 3 steps, because the rest left almost nothing behind. Rests of this length reset the curve.
4. 30 seconds is three half-lives: intensity falls to `0.5³ = 12.5%` of its start, a drop of 87.5%. 45 seconds is 4.5 half-lives: `0.5^4.5 ≈ 4.4%`, a drop of about 95.6%. With a 20-second half-life, 30 seconds leaves `0.5^1.5 ≈ 35%`, so the same relax would not reset the curve. The length of rest you need depends on how fast your intensity decays, which is why you choose `d` deliberately.

</details>

## Lab / assignment hook

[Lab 03, intensity graph for your blockout](../labs/lab03.md). You implement the intensity model, the four measurements and the Director rule in Python, then write a beat chart and an encounter list for your Lab 02 blockout, compute its intensity graph, and revise the encounters to hit a target shape without changing the total threat. You play-test the revised version and log what testers did during the valleys.

## Sources

- Booth, M. (2009). "The AI Systems of Left 4 Dead." Valve, slides from a 2009 talk, hosted on Valve's publications page (steamcdn-a.akamaihd.net/apps/valve/2009/ai_systems_of_l4d_mike_booth.pdf). Pacing inspired by Counter-Strike's spiky rounds; constant combat fatiguing and long inactivity boring; survivor intensity raised by damage, incapacitation, ledge pulls and nearby kills and decaying toward zero, with no decay while engaged; Build Up, Sustain Peak (3-5 s), Peak Fade and Relax (30-45 s or until far enough toward the next safe room); bosses excluded from adaptive pacing; mob interval 90-180 s on Normal; the algorithm changes pacing, not difficulty.
- Resident Evil Wiki (residentevil.fandom.com), "Typewriter," "Item Box" and "Save Room" (accessed September 2026). Typewriters as save points and item boxes in safe rooms across the series from Resident Evil (1996); the save room music of Resident Evil 2 (2019), a remix of the 1998 game's theme.
- Warcraft Wiki (warcraft.wiki.gg), "Drink" (accessed September 2026). Mana-restoring drinks consumed while sitting; vendor drinks for levels 1-65 restore mana over 18 to 30 seconds.
- Csikszentmihalyi, M. (1990). *Flow: The Psychology of Optimal Experience*. Harper & Row. As summarised in UX201 week 3.
- Totten, C. W. (2019). *An Architectural Approach to Level Design* (2nd ed.). CRC Press.
- The intensity model, `d = 0.5`, the thresholds, the threat units and designs A, B and C are teaching models built for this lecture. Design C simplifies Booth's published description and is not Valve's code.

## Interactive spec: examples/w03-intensity-graph.html

**Purpose.** Show that the same total threat produces very different experiences depending on its spacing, and that a simple feedback rule (the Director) produces peaks and valleys automatically.

**The one insight the visual must make obvious.** Switching between designs A, B and C leaves the "total threat: 180" counter unchanged while the intensity curve changes from a flat line at 20 (no peaks, no calm) to a shape with clear peaks and a full minute of calm.

**Layout.** Two stacked views sharing one x axis (0 to 180 seconds, 18 steps of 10 s). Mobile (390px): stacked full width, controls and numbers below. Desktop (1280px): views on the left two-thirds, controls and numbers on the right.

- Top view, "Threat per step": 18 bars showing `E[k]`, y axis 0 to 60. In design B and Custom, bars are draggable vertically in steps of 5 (keyboard: focus a bar, up/down arrows change by 5). A counter at top right: "Total threat: 180".
- Bottom view, "Intensity": the curve `I[k]` drawn as points joined by lines (step values at the end of each step), y axis 0 to 80. A shaded band at `I ≥ peak` labelled "peak" and a band at `I < calm` labelled "calm". In design C, shade the relax steps on the x axis.

**Controls.** Design selector: A drip, B authored wave, C Director, Custom (copies the current bars for editing). Decay `d` slider 0.1 to 0.9 (step 0.05, default 0.5), with the half-life shown as `10 × ln 0.5 / ln d` seconds. Peak threshold 20 to 60 (default 35). Calm threshold 0 to 20 (default 10). For C: full population 5 to 40 (default 20), relax steps 0 to 6 (default 3). A "Normalise total" button that scales Custom bars so the total returns to 180 (rounded to multiples of 5; put any remainder on the largest bar). Reset.

**Formulas.**

- `I[0] = 0` before the first step, `I[k] = d × I[k−1] + E[k]`.
- Director (C): `rest = 0`. For each step: `e = 0` if `rest > 0` else `full`; then `rest = max(0, rest − 1)`; `I = d × I + e`; if `e > 0` and `I ≥ peak` then `rest = relax`.
- Peak time `= 10 × count(I ≥ peak)`, calm time `= 10 × count(I < calm)`, peaks = number of steps where `I ≥ peak` and the previous step (or start) was below `peak`, maximum `= max I`.
- Equilibrium line (dashed, toggleable): `E_mean / (1 − d)` where `E_mean` is the mean bar height.

**Numbers panel.** Total threat, maximum (1 decimal), peak time, calm time, peaks, equilibrium for the mean threat, and a sentence such as "Same 180 threat. Design A never peaks and never rests; design B spends 30 s at peak and 60 s calm."

**Test values (defaults `d = 0.5`, peak 35, calm 10).**

- A: `I` = 10, 15, 17.5, 18.75, 19.38, 19.69, ... to 20.00; max 20.0; peak 0 s; calm 0 s; peaks 0.
- B: `E` = 0, 5, 10, 15, 20, 30, 40, 0, 0, 0, 0, 5, 10, 15, 30, 0, 0, 0; `I` = 0, 5, 12.5, 21.25, 30.63, 45.31, 62.66, 31.33, 15.66, 7.83, 3.92, 6.96, 13.48, 21.74, 40.87, 20.43, 10.22, 5.11; max 62.7; peak 30 s; calm 60 s; peaks 2.
- C: `E` = 20, 20, 20, 0, 0, 0 repeated three times; `I` = 20, 30, 35, 17.5, 8.75, 4.38, 22.19, 31.09, 35.55, 17.77, 8.89, 4.44, 22.22, 31.11, 35.56, 17.78, 8.89, 4.44; total 180; max 35.6; peak 30 s; calm 60 s; peaks 3.
- Check question 1: Custom with `E = 30, 0, 0, 30` then zeros gives `I` = 30, 15, 7.5, 33.75.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`, light and dark. Peak and calm bands use a pattern as well as a tint. Bars are focusable buttons with visible values. Respect reduced motion (no animated transitions between designs). No game art or characters; threats are plain bars.

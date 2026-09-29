# GD201 · Week 08 — Environmental storytelling

**Why this matters:** You can spend a week dressing a room so that it tells a story, and most players will walk through it without getting the story. That isn't bad luck. Whether a player gets a story from a space depends on where the clues are, how many there are, and how many the player needs to see. You can compute it, and you can fix it before the playtest instead of after.

**You will be able to:**
- Compute the chance that a player understands a story beat from the notice chances of its clues, for "needs all", "needs any" and "needs at least k" designs.
- Estimate notice chances from playtest counts and explain why small tests and correlated noticing make the prediction too optimistic.
- Design a clue layout that reaches a target understanding rate with the fewest clues, using placement levers (stop points, framing, gating).
- Critique a shipped game's environmental story by naming its clues, their placement and the reading rule it relies on.

**Before class:** Christopher Totten, *An Architectural Approach to Level Design* (2nd ed., CRC Press, 2019), chapter 9 "Storytelling in Gamespaces". Henry Jenkins, "Game Design as Narrative Architecture" (2004), in Wardrip-Fruin and Harrigan (eds.), *First Person*, MIT Press. It is free on the MIT website. Read the sections on evocative spaces and embedded narratives.

**Prerequisites from earlier courses:** [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) (the chance of at least one success). [MA102 week 6, the binomial distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w06-binomial-crits-over-a-fight.md) (exactly `j` successes in `n` tries). [UX201 week 1, perception, attention and memory](../../UX201-game-ux-and-player-psychology/lectures/w01-perception-attention-memory.md) (why players miss what they aren't looking for). [GD101 week 7, playtesting](../../GD101-introduction-to-game-design/lectures/w07-playtesting-observe-dont-explain.md) (how to watch without coaching). Running alongside this course, GD202 covers the writing side of environmental and emergent narrative in [week 9, emergent narrative](../../GD202-narrative-and-quest-design/lectures/w09-emergent-narrative.md) and [week 10, lore delivery without walls of text](../../GD202-narrative-and-quest-design/lectures/w10-lore-delivery-without-walls-of-text.md).

**Interactive:** [`examples/w08-clue-reliability.html`](../examples/w08-clue-reliability.html). Keep it open during section 2.

---

## 1. What a space can tell

**Environmental storytelling** is telling a story through the arrangement of a space and the things in it, instead of through cutscenes, dialogue or text screens. The player reads the story by looking.

Henry Jenkins's 2004 essay "Game Design as Narrative Architecture" gives a useful map. He argues that game spaces carry story in four ways:

- **Evocative spaces** call up a story the player already knows. A haunted house needs no explanation, because the genre has done the work.
- **Enacted stories** happen in the space while you are there. An ambush in a canyon is a story event staged by the level.
- **Embedded narratives** are stories already over, left in the space as evidence. The player arrives after the event and reconstructs it. This is the kind level designers usually mean by environmental storytelling, and it is this week's focus.
- **Emergent narratives** are stories players make themselves from the systems the space gives them. They are a subject for GD202.

Jenkins draws on Don Carson, a theme-park designer who wrote about environmental storytelling for game developers in 2000. Carson's point is that a themed space works when every element obeys one set of story rules, so visitors can infer what happened from what they see. Harvey Smith and Matthias Worch titled their 2010 GDC talk on the subject with the question every embedded narrative asks the player: "What happened here?"

To reason about embedded stories, split them into parts:

- A **story beat** is one fact you want the player to understand. "The garrison abandoned this tower because the well was poisoned" is one beat.
- A **clue** is one object or arrangement in the space that carries evidence for a beat: a skeleton, a note, a barricaded door, a pattern of scorch marks.
- A clue's **notice chance** `p` is the fraction of players who see it and read it the way you intended. It depends on where you put it much more than on how well it's made.
- A beat's **reading rule** says how many of its clues a player needs to get the beat. This is the choice designers most often make without noticing they are making it.

## 2. Worked example: the poisoned well

### The hook

Gone Home (Fullbright, 2013) has no other characters on screen. You explore an empty family house and work out what happened by examining objects, letters and journals. Its developers had worked on BioShock 2's Minerva's Den, where players dug story out of audio logs they had to seek out. Designing Gone Home, they accepted a hard fact: not every player would find every clue. So they made each thread of the story understandable without every piece being found. They also chose a family that had only just moved in. Most things are still in boxes, so the few objects that are unpacked stand out as important.

Those two decisions are exactly the two numbers in this section. The first is about the reading rule. The second raises `p`.

### The model

A beat has `n` clues. Clue `i` is noticed with chance `p_i`. Treat noticing as independent across clues for now (the judgment section comes back to this). Three reading rules:

```
needs all  (chain):      P = p_1 × p_2 × ... × p_n
needs any  (redundant):  P = 1 − (1 − p_1) × (1 − p_2) × ... × (1 − p_n)
needs at least k of n:   P = chance that k or more of the n clues are noticed
```

The first two are special cases of the third: "needs all" is `k = n`, and "needs any" is `k = 1`. When every clue has the same `p`, the third is the binomial tail you met in MA102 week 6:

```
P(at least k) = Σ over j = k..n of C(n, j) × p^j × (1 − p)^(n − j)
```

`P` is the **understanding rate**: the fraction of players who come away with the beat.

Where does `p` come from? From playtests, which section 3 covers. Until you have data, use placement tiers. The values below are invented starting points for this course, not measurements from a shipped game. Replace them with your own as soon as you can test.

| Tier | Placement | Starting `p` |
|---|---|---|
| Gate | On an object the player must use to progress (the door lever, the key) | 0.95 |
| A | On the critical path, in the forward view, at a stop point | 0.8 |
| B | On the critical path, to the side | 0.5 |
| C | In an optional side room or behind cover | 0.25 |
| D | Behind the player's direction of travel | 0.1 |

### Numbers you can check

The level is an abandoned watchtower. The beat is "the garrison fled because the well was poisoned".

**Version 1, the chain.** The designer places three clues, each carrying one link of the argument:

| Clue | Carries | Tier | `p` |
|---|---|---|---|
| Dead crows around the well | "something is wrong with the well" | A | 0.8 |
| A sick bay with rows of empty cots | "people fell ill" | B | 0.5 |
| The captain's half-written order to evacuate | "they left because of it" | C | 0.25 |

A player needs all three to connect well, sickness and flight. `P = 0.8 × 0.5 × 0.25 = 0.10`. One player in ten gets the beat. The other nine see some dead birds and an empty building.

**Version 2, redundant clues.** Same three locations, same three tiers, but each clue is rewritten to carry the whole beat by itself. A skull is scratched into the well cover beside a crossed-out cup. The sick bay's wall tally counts the sick under a drawing of a bucket. The captain's order says "draw no water, abandon the tower". Now any one clue is enough:

```
P = 1 − (1 − 0.8)(1 − 0.5)(1 − 0.25) = 1 − 0.2 × 0.5 × 0.75 = 1 − 0.075 = 0.925
```

Same art budget, same floor plan. The understanding rate goes from 10% to 92.5%. The change was the reading rule, not the placement.

**Between the extremes.** A single clue can be misread. Dead crows might be just dead crows. So you may decide that a player needs at least two clues before the reading is safe. Add a fourth clue, packed bags abandoned at the gate (tier B, `p = 0.5`), and compute the understanding rate for every `k`:

| Clues needed `k` | Four clues at 0.8, 0.5, 0.5, 0.25 | Four clues all at 0.5 |
|---|---|---|
| 1 | 0.9625 | 0.9375 |
| 2 | 0.7250 | 0.6875 |
| 3 | 0.3125 | 0.3125 |
| 4 | 0.0500 | 0.0625 |

Check the right column's `k = 2` cell by hand. The chance of seeing none is `0.5^4 = 0.0625`, the chance of seeing exactly one is `4 × 0.5^4 = 0.25`, so at least two is `1 − 0.0625 − 0.25 = 0.6875`.

Look down the columns. Each extra clue the reader must find costs more than the one before: from `k = 1` to `k = 2` you lose about 24 points, and from 2 to 3 you lose 41. The steepest drop is in the middle. That is where designers most often set the bar without meaning to, by writing a story that makes sense only if you saw "most" of it.

For clues with different chances, compute the distribution one clue at a time. This is the short version you'll finish in the lab:

```python
def p_at_least(ps, k):
    """Chance that at least k of the clues are noticed, clue i with chance ps[i]."""
    dist = [1.0]                      # dist[j] = chance exactly j noticed so far
    for p in ps:
        new = [0.0] * (len(dist) + 1)
        for j, q in enumerate(dist):
            new[j] += q * (1 - p)     # this clue missed
            new[j + 1] += q * p       # this clue noticed
        dist = new
    return sum(dist[k:])

chain = [0.8, 0.5, 0.25]
print(f"chain, need all 3:   {p_at_least(chain, 3):.3f}")
print(f"redundant, need 1:   {p_at_least(chain, 1):.3f}")
for k in range(1, 5):
    print(f"4 clues at 0.5, need {k}: {p_at_least([0.5] * 4, k):.4f}")
well = [0.8, 0.5, 0.5, 0.25]
for k in range(1, 5):
    print(f"well clues, need {k}: {p_at_least(well, k):.4f}")
```

Output:

```
chain, need all 3:   0.100
redundant, need 1:   0.925
4 clues at 0.5, need 1: 0.9375
4 clues at 0.5, need 2: 0.6875
4 clues at 0.5, need 3: 0.3125
4 clues at 0.5, need 4: 0.0625
well clues, need 1: 0.9625
well clues, need 2: 0.7250
well clues, need 3: 0.3125
well clues, need 4: 0.0500
```

Open the interactive. The left view is the watchtower floor plan with the player's path and four clue slots, each set to a tier. The right view is a grid of 100 player icons: each icon is one simulated player, filled if they got the beat. Switch the reading rule between "needs all" and "needs any" and watch the grid go from almost empty to almost full while the floor plan doesn't change at all. That gap, between how complete the room looks to you and how few players get the story, is the lesson. You've seen every clue. They haven't.

### Cross-game recognition

**Gone Home (2013).** Fullbright's decision that each thread must survive missing pieces is a choice of small `k` relative to `n`. The main thread also has a second, louder channel: Sam's journal entries are narrated as audio when you find them. The side stories (the parents' troubles) are allowed to be low `p`. Summaries of the game list them as optional clues that only some players find. The moved-in-recently framing raises `p` for every object by cutting the clutter a player has to search. UX201 week 1's visual search model says why that works: fewer distractors, faster and more reliable finds.

**Portal (Valve, 2007).** The main story beat, that the AI running the tests is lying to you, is delivered by GLaDOS's voice, a gate-tier channel with `p` near 1. The environment repeats it. After the player escapes the test chambers, the route runs through backstage maintenance areas covered in graffiti, including the line "the cake is a lie". The graffiti is on the path you must take, and it carries the same beat as the voice. It is a redundant second clue, not a required link in a chain. Valve also dropped a plan to introduce the graffiti's author as a character, to avoid adding too much narrative. They kept the evidence and cut the explanation.

**BioShock 2: Minerva's Den (2010).** Gone Home's team named the audio logs of their earlier work as a direct influence: narrative pieces the player has to actively seek out. Logs you must go looking for are tier-C clues by design. That is fine as long as nothing essential depends on them. A log that rewards curiosity is allowed a low `p`. A log that explains why the next door is locked is not.

In all three games the same structure appears. The beat the player must get is carried by a high-`p` channel with `k = 1`. The environment repeats it redundantly. Depth that only explorers find is allowed to sit at low `p` or high `k`, because missing it costs nothing.

### Design judgment, eyes open

- **Decide `k` on purpose for every beat.** Write it next to the beat in your design doc. If the beat is essential, aim for `k = 1` with a high-`p` clue in the set. If it's a reward for close readers, a chain is fine. A 5% understanding rate can be exactly right for a secret.
- **One beat per clue, several clues per beat.** The most common failure is a clue that carries two half-beats, so it is needed by two chains at once. Rewrite clues until each one carries a whole beat.
- **Redundancy has costs.** Three clues that all shout "the well is poisoned" can feel patronizing to the players who get it from the first. Vary the channel (an object, a written sign, a sound) and put the loudest clue last, as a confirmation for the players who missed the quiet ones.
- **Independence is optimistic.** Players who notice one clue are more likely to notice the others. They are the attentive ones, or the slow ones. Positive correlation makes "needs any" less reliable than the formula says, and "needs all" more reliable. Your lab data will show this. Treat the formula as an upper bound for redundant designs.
- **Players in groups notice less.** In a shared world a group moving at the speed of its fastest member stops at fewer stop points. [Week 11](w11-shared-spaces-designing-for-many-players.md) looks at shared spaces. For now, assume tier values drop when players aren't alone, and put essential beats on gates.

## 3. Measuring notice chances

The tier table is a guess. Replace it with measurements.

**Observe, don't ask first.** Watch testers play (GD101 week 7). Note, for each clue, whether the camera paused on it. Afterwards, ask an open question ("What happened in the tower?") before any specific one. A tester who says "the water was bad" got the beat. A tester who needed a hint didn't.

**Estimate `p` as a fraction.** If 7 of 12 testers noticed the sick bay, `p̂ = 7/12 ≈ 0.58`. With 12 testers this estimate is rough. MA102 week 13 shows why small samples lie. A 95% confidence interval on 7 of 12 runs from roughly 0.3 to 0.8. Don't redesign a clue because one test moved its `p̂` by 0.1.

**Compare prediction with observation.** Put your estimated `p̂` values into `p_at_least` and compare the predicted understanding rate with the fraction of testers who actually got the beat. If they told you the beat more rarely than predicted for a `k = 1` design, suspect correlation (the same few testers notice everything) or misreading (they saw the clue but read it wrong). Misreading means the clue's `p` was measured wrong. Measure "read correctly", not "looked at".

## 4. Levers that raise p

Once you know which clues are weak, you have a small set of levers, roughly in order of power:

- **Gate it.** Put the clue on the thing the player must use. The order to evacuate is pinned to the door the player must open. `p` near 1, at the cost of feeling staged if you overuse it.
- **Stop points.** Players stop at doors, ladders, loot, save points and the tops of stairs, and their camera settles. Clues placed in the view at a stop point are read far more often than clues passed at running speed.
- **Frame it.** Use the landmark and lighting tools from [week 4](w04-guiding-the-player-landmarks-light-weenies.md). A pool of light, a sightline down a corridor ending on the clue, an arch that frames it. Frame one clue per view. Two framed clues compete.
- **Contrast.** A clean object in a dirty room, one upright chair among overturned ones. Gone Home's half-unpacked house is contrast applied to a whole level.
- **Sound.** A creaking sign or buzzing flies pull the camera around. This is the best lever for tier-D clues behind the player.
- **Repeat the motif.** If the crossed-out cup appears on the well, the sick bay wall and the captain's order, the second sighting reminds the player of the first. That makes the redundant design easier to read as well as more likely to be seen.

Each lever has a budget in art time and in player patience. Spend the most on the beats with `k = 1` that the rest of the level depends on.

## In-class activity (25 minutes)

Pairs, with the interactive and squared paper.

1. (5 min) Pick a beat for a small ruined chapel, one sentence long, and name what the player should understand.
2. (10 min) Draw the floor plan with the player's path. Place four clues and assign each a tier. Write the reading rule (`k`) you intend.
3. (5 min) Compute the understanding rate with the lecture's function or the interactive. If it's under 0.8, move one clue up a tier or rewrite one clue to carry the whole beat, and recompute.
4. (5 min) Swap with another pair. Without looking at their `k`, read their plan and say what story you think it tells. Compare with their beat.

Expected output: a floor plan, a table of four clues with tiers and `p`, the understanding rate before and after your fix, and your partners' reading of your plan.

## Common misconceptions

- **"More clues always helps."** Only if the player needs a fixed number of them. Add a clue to a chain (`k = n` rises with `n`) and the understanding rate falls, because every added link is one more thing to miss.
- **"If I can see it in the editor, players will see it."** You know where everything is. Notice chance is about attention during play, which UX201 week 1 showed is narrow and goal-driven.
- **"A good environmental story needs no words."** Written signs are part of the environment. Portal's graffiti is words on a wall. The rule is to avoid walls of text, not text.
- **"Low understanding rate means a failed beat."** Only for essential beats. A secret that 5% of players find is working as designed if you meant it to be a secret.

## Check yourself

1. A beat has three clues with `p = 0.6` each. What is the understanding rate if the player needs all three? Any one? At least two?
2. A designer's chain has clues at 0.9, 0.8 and 0.3. Which single change raises the understanding rate most: raising the 0.9 clue to 1.0, or raising the 0.3 clue to 0.6? Show the numbers.
3. You want an essential beat understood by at least 95% of players, using clues at tier B (`p = 0.5`) with `k = 1`. How many clues do you need? How many if they are tier A (`p = 0.8`)?
4. In a playtest, 10 testers saw clue X, and those are the same 10 who saw clue Y. The other 10 saw neither. Estimate `p` for each clue, the independence prediction for "needs any", and the observed rate. What went wrong?

<details>
<summary>Answers</summary>

1. All: `0.6³ = 0.216`. Any: `1 − 0.4³ = 1 − 0.064 = 0.936`. At least two: exactly two is `3 × 0.6² × 0.4 = 0.432`, exactly three is `0.216`, total `0.648`.
2. Now `0.9 × 0.8 × 0.3 = 0.216`. Raising the first clue: `1.0 × 0.8 × 0.3 = 0.24`. Raising the third: `0.9 × 0.8 × 0.6 = 0.432`. In a chain, fix the weakest link. It doubles the rate here.
3. Need `1 − 0.5^n ≥ 0.95`, so `0.5^n ≤ 0.05`, which gives `n = 5` (`0.5^5 = 0.031`, while `0.5^4 = 0.0625` is too high). With tier A, `0.2^n ≤ 0.05`, so `n = 2` (`0.2² = 0.04`).
4. `p̂ = 10/20 = 0.5` for both. Independence predicts `1 − 0.5 × 0.5 = 0.75` for "needs any". Observed: 10 of 20, `0.5`. Noticing was perfectly correlated, so the second clue added nothing. Put the two clues where different kinds of player look, for example one on the path and one at a stop point with a sound cue.

</details>

## Lab / assignment hook

[Lab 08, clue reliability from playtest data](../labs/lab08.md). You implement the three reading rules and the general `p_at_least`, estimate `p` from a 24-tester playtest log of the watchtower, compare predicted and observed understanding rates, and write a planner that picks the fewest clue slots to hit a target. Then you dress your week 7 greybox with one beat and test it on three people. It counts toward the analysis component (20%).

## Sources

- Jenkins, H. (2004). "Game Design as Narrative Architecture." In N. Wardrip-Fruin & P. Harrigan (eds.), *First Person: New Media as Story, Performance, and Game*. MIT Press. Online at web.mit.edu/~21fms/People/henry3/games&narrative.html. The four kinds of spatial story (evoke, enact, embed, emergent) and the discussion of Don Carson.
- Carson, D. (2000). "Environmental Storytelling: Creating Immersive 3D Worlds Using Lessons Learned from the Theme Park Industry." *Gamasutra* (now Game Developer). As summarized by Jenkins (2004).
- Smith, H. & Worch, M. (2010). "What Happened Here? Environmental Storytelling." Game Developers Conference 2010, GDC Vault (Arkane Studios and LucasArts). Cited for its title and subject.
- Wikipedia, "Gone Home" (accessed September 2026), development section. No other characters on screen; the team's BioShock 2: Minerva's Den background and its audio logs that players seek out; the recognition that not every player finds every clue, so each thread is understandable without every element; the recently-moved family chosen so key objects stand out.
- Wikipedia, "Portal (video game)" (accessed September 2026). GLaDOS directs and taunts the player; the backstage maintenance areas with graffiti including "the cake is a lie"; the dropped introduction of the Rat Man character to avoid too much narrative.
- Totten, C. (2019). *An Architectural Approach to Level Design* (2nd ed.). A K Peters/CRC Press. Chapter 9 (doi:10.1201/9781351116305-9; title checked on Crossref, September 2026).

## Interactive spec: examples/w08-clue-reliability.html

**The one insight.** The same four clues in the same room can tell the story to 96% of players or to 5%, depending only on how many of them a player needs. The designer sees every clue; the player population doesn't.

**Layout.** Two linked views, stacked on narrow screens.

- **Left: floor plan of the watchtower.** A simple generic plan: gate, courtyard with well, sick bay to the side of the path, captain's room as a side room. The player's path is a dotted line from gate to stairs. Four clue slots are shown as numbered markers: 1 well (default tier A), 2 sick bay (default B), 3 captain's order (default C), 4 bags at the gate (default B). Each marker shows its tier letter and `p`.
- **Right: 100 player icons in a 10 × 10 grid.** Each is one simulated player. Filled means they got the beat, hollow means they didn't. Under the grid: "Exact understanding rate 72.5%" and "This sample: 71 of 100". A "New sample" button draws another 100 players.
- **Below both: a bar chart** of the understanding rate for `k = 1..n` for the current clues, with the selected `k` highlighted.

**Controls.**
- Each clue slot has a tier selector (Gate 0.95, A 0.8, B 0.5, C 0.25, D 0.1, Off). Off removes the clue from `n`.
- Reading rule: segmented control "Needs any" (`k = 1`), "Needs at least k" with a stepper for `k` (1 to `n`), "Needs all" (`k = n`). Default `k = 2`.
- Toggle "Correlated noticing". When on, each simulated player is "attentive" with chance 0.5. An attentive player notices clue `i` with chance `min(1, 1.6·p_i)`; the others notice it with chance `max(0, 2·p_i − min(1, 1.6·p_i))`. This keeps each clue's average notice chance at `p_i` while making noticing positively correlated. When on, show the exact independent rate and the simulated correlated rate side by side, so students see the correlated rate fall below the formula for `k = 1` and rise above it for `k = n`.
- Seeded random generator so the first screen always shows the same sample (seed 8).

**Formulas.** Exact rate by the dynamic program in the lecture (`p_at_least`). Simulation: for each of 100 players and each active clue, draw uniform `u` and notice if `u < p` (independent mode).

**Test values.**
- Clues 0.8, 0.5, 0.5, 0.25: `k = 1` 0.9625, `k = 2` 0.7250, `k = 3` 0.3125, `k = 4` 0.0500 (four decimals, so the exact values need no rounding).
- Clue 4 off (0.8, 0.5, 0.25): `k = 3` 0.100, `k = 1` 0.925.
- All four at B (0.5): `k = 2` 0.6875.
- All four at A (0.8): `k = 4` 0.4096, `k = 1` 0.9984.

**Accessibility.** Tier selectors are native selects or radio groups with labels. Filled and hollow icons differ in shape as well as colour (filled circle vs ring). Text readouts next to the grid. Respect `prefers-reduced-motion` (no icon fill animation) and `prefers-color-scheme`.

# GD201 · Week 01 — Level design as teaching

**Why this matters:** Every level teaches something, whether you planned the lesson or not. Players who fail a lesson pay for it in time, and you set that price when you place a checkpoint, a respawn point or a graveyard. Designers who ignore the price build levels that feel cruel to beginners and trivial to experts at the same time.

**You will be able to:**
- Break a level into a lesson plan (introduce, practise, combine, test) and critique where a shipped level introduces each mechanic.
- Compute the expected time to clear a challenge from its attempt length, its success chance and the recovery time after a failure, and the penalty ratio that recovery creates.
- Compute the expected time to clear a segment of several challenges between checkpoints, and place checkpoints to meet a target.
- Decide where a level should make failure cheap and where it should make it costly, and defend the choice with numbers.

**Before class:** Christopher Totten, *An Architectural Approach to Level Design* (2nd ed., CRC Press, 2019), the opening chapter on what level designers do and where the craft comes from. Watch Eurogamer's video "Miyamoto on World 1-1: How Nintendo made Mario's most iconic level" (September 2015, about 18 minutes). Play the first ten minutes of any 2D platformer and write down, in order, every new thing it asks you to do.

**Prerequisites from earlier courses:** [MA102 week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md) (why a task with success chance `p` takes `1/p` tries on average). [GD101 week 7, playtesting](../../GD101-introduction-to-game-design/lectures/w07-playtesting-observe-dont-explain.md) (how to watch testers without coaching them, which is how you will measure `p`). [GD102 week 8, core loops](../../GD102-systems-design-and-game-mechanics/lectures/w08-core-loops-and-meta-loops.md) (verbs and the loop they sit in). Running alongside this course, [UX201 week 7, onboarding and tutorials](../../UX201-game-ux-and-player-psychology/lectures/w07-onboarding-and-tutorials.md) covers the memory side of teaching. This lecture covers the space side.

**Interactive:** [`examples/w01-retry-cost.html`](../examples/w01-retry-cost.html). Keep it open during section 2.

---

## 1. The level is the teacher

Start the original Super Mario Bros. (NES, 1985) and look at what the first screen of World 1-1 does before you touch anything. Mario stands at the left edge of a flat, open strip of ground. There is nothing to fall into. A few steps to the right, a Goomba walks toward you. You didn't go looking for it. It came to you, so you have to do something: jump over it, jump on it, or touch it and find out what happens. Just above, a `?` block floats in reach of a jump.

Hit the block group that follows and a mushroom appears. It slides along the ground at Mario's walking speed and turns around when it hits a wall. The first pipe stands a short way to the right, so a mushroom that slides right can bounce off it and come back toward you. The game uses its own physics to hand you the power-up, and to make sure you learn that the thing that looks like a Goomba is not one.

None of this is explained in text. The space does the explaining. According to Shigeru Miyamoto, in the 2015 Eurogamer interview, World 1-1 was built late in development. The team made the more exciting courses first and then realised those needed a player who already knew the rules, so they built a first course whose job was to teach them.

That is the idea of this whole course in one level. **A level is a sequence of situations, and each situation either teaches, practises or tests something.** The designer decides the order, the spacing and what failure costs.

### The vocabulary of a lesson

We need a few words, used the same way all semester.

- A **verb** is something the player can do: jump, dash, grapple, block, climb. GD102 used the word for the actions inside a core loop. Here a verb is the thing a level teaches.
- A **challenge** is one situation that asks for a verb and can be failed: a gap to jump, a Goomba to avoid, a ledge to grapple.
- A **beat** is a stretch of level built around one idea. It usually holds one to three challenges.
- A **lesson** is the sequence of beats that takes a verb from unknown to mastered.

Most well-built lessons use four kinds of beat, in this order.

1. **Introduce.** The verb appears in a situation where failure is cheap and the answer is nearly forced. The Goomba on flat ground is an introduction. So is a gap over shallow water that you can climb out of.
2. **Practise.** The same verb again, with small changes: a wider gap, a Goomba on a slope, two in a row.
3. **Combine.** The verb meets something the player already knows. Jump over a Goomba while a pit waits behind it.
4. **Test.** The verb under pressure, where failure costs something. A long jump over a pit, with a moving enemy, near the end of the level.

If this sounds like Koichi Hayashida's "introduce, develop, twist, conclude" structure for Super Mario 3D Land levels, it is the same family of idea. UX201 week 7 covers that structure and the memory research behind it: why a verb needs spaced practice, and why a checklist of "taught" verbs lies about what players can recall. This lecture takes the teaching order as given and asks a different question, one that belongs to level design. **When a player fails a beat, what does it cost them, and who pays most?**

## 2. Worked example: the price of a mistake

### The puzzle

Celeste (2018) is known as a hard platformer. Players die in it constantly. Yet many players describe it as encouraging. Madeline respawns within a couple of seconds, a short way back inside the room where she died. Her wiki calls her de facto immortal.

Dark Souls (2011) is also known as hard. When you die, you return to the last bonfire you rested at. Every ordinary enemy between the bonfire and the place you died is alive again, and the souls you were carrying lie in a bloodstain where you fell. Players describe it as punishing.

Suppose a Celeste room and a Dark Souls boss had the same chance of success per attempt. Would they feel equally hard? The model below says no, and tells you by how much.

### The model

Take one challenge. Define:

- `t`, the **attempt time**: seconds from the start of an attempt to success or failure.
- `p`, the **success chance** per attempt, between 0 and 1.
- `r`, the **recovery time** after a failure: seconds from failing to being ready to try again. It is usually a respawn delay `s` plus the walk back from the respawn point, `d / v`, where `d` is the distance and `v` the player's speed.

From MA102 week 7, attempts until the first success follow a geometric distribution with mean `1/p`. So on average there are `1/p` attempts, and `1/p − 1 = (1 − p)/p` of them are failures. Every attempt costs `t`. Every failure also costs `r`. Add them up:

```
E[T] = t / p  +  r × (1 − p) / p
     = (t + r × (1 − p)) / p
```

`E[T]` is the **expected time to clear** the challenge. The first term is what the challenge itself costs. The second is what your level layout adds.

Divide by the time with instant recovery (`r = 0`) and you get the **penalty ratio**:

```
penalty ratio = 1 + (r / t) × (1 − p)
```

Two things set the penalty. The ratio `r / t` says how long recovery is compared to the challenge. The factor `1 − p` says how often players pay it. Notice that `p` appears in both. **A long recovery hurts most exactly when the success chance is low**, which is when a player is meeting a verb for the first time.

### Numbers you can check

Take a jump challenge with `t = 8` seconds. The respawn delay is `s = 2` seconds and the player runs at `v = 6` metres per second (these are invented values for a teaching level, not measurements of a shipped game). Put the respawn point 0, 60 or 300 metres before the challenge, which gives `r = 2`, `12` and `52` seconds.

Now vary `p`. A value of 0.2 is a first contact with a new verb. A value of 0.5 is a player who half-knows it. A value of 0.9 is a player who has mastered it.

**Expected time to clear, `E[T]` in seconds**

| Respawn distance | `r` | `p = 0.2` | `p = 0.5` | `p = 0.9` |
|---|---|---|---|---|
| 0 m | 2 | 48.0 | 18.0 | 9.1 |
| 60 m | 12 | 88.0 | 28.0 | 10.2 |
| 300 m | 52 | 248.0 | 68.0 | 14.7 |

**Penalty ratio**

| Respawn distance | `p = 0.2` | `p = 0.5` | `p = 0.9` |
|---|---|---|---|
| 0 m | 1.20 | 1.13 | 1.03 |
| 60 m | 2.20 | 1.75 | 1.15 |
| 300 m | 6.20 | 4.25 | 1.65 |

Check one cell by hand. At `p = 0.2` and `r = 52`: `(8 + 52 × 0.8) / 0.2 = (8 + 41.6) / 0.2 = 248` seconds. The same challenge with the respawn point next to it takes 48 seconds.

Read the table across a row. With the far respawn point, a learner (`p = 0.2`) loses 200 extra seconds compared with the near one. A master (`p = 0.9`) loses 5.6 seconds. Moving the checkpoint barely changes the game for the skilled player. It changes it completely for the new one. **Recovery time is a tax paid almost entirely by the players who are still learning.**

Open the interactive now. The left view is a side-on strip of level with a checkpoint flag you can drag and a challenge marker. The right view plots `E[T]` against `p` for your current `r`, with the `r = 0` curve underneath it as a baseline. The gap between the two curves is the time your layout adds. Drag the flag back and watch the gap swell on the left of the chart, where `p` is low, while the right end hardly moves.

### Several challenges between checkpoints

Real levels put more than one challenge between checkpoints. If you fail any of them, you go back to the start of the **segment**, the stretch between two checkpoints. Now the success chance of a whole run is the product of the individual chances, `P = p₁ × p₂ × ... × pₖ`, and that product falls fast.

A run pays for challenge `i` only if it got that far, which happens with chance `p₁ × ... × pᵢ₋₁`. Let `cᵢ` be the time to reach and attempt challenge `i`. The expected time to clear the segment is:

```
E[segment] = ( c₁  +  c₂ p₁  +  c₃ p₁ p₂  + ...  +  s × (1 − P) ) / P
```

For one challenge this is the model above with `r = s`, since the walk-back is now counted inside `c`.

Take three challenges, each with `c = 10` seconds and `p = 0.5`, and a respawn delay `s = 2`. With one checkpoint at the start, `P = 0.125`, so a player needs 8 runs on average. With a checkpoint before each challenge, each one is its own segment. You can check both with this code:

```python
def segment_time(costs, probs, respawn):
    reach, run = 1.0, 0.0
    for c, p in zip(costs, probs):
        run += c * reach        # pay for this challenge only if we got here
        reach *= p              # chance of getting past it
    return (run + respawn * (1 - reach)) / reach

one_checkpoint = segment_time([10, 10, 10], [0.5, 0.5, 0.5], 2)
three_checkpoints = 3 * segment_time([10], [0.5], 2)
print(f"one checkpoint:    {one_checkpoint:.1f} s")
print(f"three checkpoints: {three_checkpoints:.1f} s")
print(f"mastered (p=0.9):  {segment_time([10]*3, [0.9]*3, 2):.1f} s vs {3*segment_time([10], [0.9], 2):.1f} s")
```

```
one checkpoint:    154.0 s
three checkpoints: 66.0 s
mastered (p=0.9):  37.9 s vs 34.0 s
```

The same three jumps take 154 seconds or 66 seconds depending on one design decision. For the skilled player the gap is under 4 seconds. Checkpoint density is a teaching decision far more than a difficulty decision.

The interactive's second tab puts three challenges on the strip. Drag up to three checkpoints and it shows the segment times and the total.

### Cross-game recognition

Every game with failure has some version of `t`, `p` and `r`. The skill is to find them.

**Celeste (2018, all versions).** Madeline respawns within seconds, back inside the current room, so `r` is a few seconds. If an attempt at a room also takes a few seconds, `r / t` is close to 1 and the penalty ratio stays under about 2 even at very low `p`. That is why players can die many times on one screen without quitting. Celeste also shows the other end of the scale. After a player beats the B-side of Chapter 8 (Core), Golden Strawberries appear at the start of completed chapters. Carrying one, any death loses the berry and sends you back to the room where you picked it up. For that run, `r` is the whole chapter. The game offers the huge `r` only to players whose `p` is already high, and only if they choose it.

**Dark Souls (2011, original release).** Dying returns you to the last bonfire you rested at, and resting respawns the ordinary enemies. So the walk back is not a walk. It is a segment of fights with their own success chances, and a player can die on the way back. Your souls wait in a bloodstain at roughly where you died, and dying again before you reach it loses them for good. Here `r` is large, uncertain, and carries a stake that is not time. The design uses that deliberately: every approach to a boss becomes careful, because the cost of failure is high.

**Super Mario, 1985 to 1990.** Super Mario Bros. has unmarked checkpoints. A player who dies part-way through a level resumes from a point they had passed. Super Mario Bros. 3 has none, and the Super Mario Wiki gives the reason as its shorter levels. Super Mario World made the checkpoint a visible object, the Midway Gate. Rewrite all three in our terms and they are the same rule. Keep `d` short, either by making levels short or by cutting a long level into segments. Making the checkpoint visible also lets players know their `r` before they attempt the challenge.

**World of Warcraft (retail, patch 10.0 onward for the numbers).** When you die in the open world and release your spirit, your ghost appears at the nearest graveyard and must run back to your corpse, a "corpse run." The alternative is to resurrect at the graveyard's spirit healer, which costs 50% durability on your gear and, for characters above level 10, a one-minute Resurrection Sickness debuff that cuts attributes and damage by 75%. Low-level characters skip the sickness. That is a lower `r` for players who are most likely still learning. Warcraft Wiki records that players were reluctant to take inexperienced groups to the Blackrock Mountain dungeons while the nearest graveyard was far away across the zone, and that the graveyard was later moved much closer. A long `r` changed which groups players were willing to form.

Four games, one idea. When you meet a new game, ask: when I fail, how long until I can try again, and how much of the level do I have to redo?

### Design judgment, eyes open

The model does not tell you to make failure cheap everywhere. It tells you what each choice costs and who pays.

- **Cheap failure at introductions.** At first contact `p` is low, so every second of `r` is multiplied by up to four or five failures. Put the respawn point next to the challenge, or make the failure non-lethal (fall into shallow water, climb out, try again).
- **Costly failure is a tool for tension.** Stakes make players careful, and careful play is part of what a boss fight or a survival game is for. Dark Souls' long `r` is a deliberate choice. If you want it, place it where `p` is already high, after the lesson, not during it.
- **Recovery is repeated content.** Every second of walk-back replays something the player has already seen. Beyond boredom, it cuts the number of real attempts per hour. Each attempt, failures included, takes `t + r × (1 − p)` seconds on average. At `r = 52`, `t = 8` and `p = 0.2` that is 49.6 seconds, about 73 attempts an hour. At `r = 2` it is 9.6 seconds, about 375 attempts an hour. Practice is how `p` rises, so a long `r` also slows learning.
- **Time is not the only currency.** Souls, durability, experience and a lost Golden Strawberry are all costs of failure. Convert them to time when you can (how long does it take to earn back 50% durability?), and name them when you can't.
- **The average hides the unlucky.** `E[T]` is a mean. As MA102 week 7 showed, a geometric wait has a long tail. Some players at `p = 0.2` will fail ten times in a row. With `r = 52` that is ten minutes on one jump. Design for the tail, not only the mean.

## 3. Writing the lesson plan: the lesson matrix

A lesson plan for a level fits in one table. Rows are verbs. Columns are beats, in the order the player meets them. Each cell holds a letter: `I` (introduce), `P` (practise), `C` (combine), `T` (test), or nothing. Add one more row for the recovery time of each beat.

Here is a plan for an invented level, The Flooded Mill, which teaches a grapple hook to a player who already knows jumping.

| Beat | 1. Dock | 2. Water wheel | 3. Sluice | 4. Gear room | 5. Rooftop |
|---|---|---|---|---|---|
| Jump | P | P | C | C | T |
| Grapple | I | P | P | C | T |
| Swinging hazard | — | — | I | C | T |
| Recovery `r` (s) | 2 | 2 | 4 | 6 | 25 |

Read it as a set of rules you can check.

- **One new thing per beat.** Each column holds at most one `I`. Beat 3 introduces the swinging hazard, so the grapple only needs practice there.
- **No test before practice.** Every `T` has at least one `P` to its left in the same row.
- **Combine before you test the combination.** Beat 5 tests jump, grapple and hazard together. Beat 4 already combined them where failure was cheap.
- **Recovery rises with mastery.** The `r` row stays low while `p` is low and climbs only at the test. By the rooftop, players have had four beats of practice, so a 25-second recovery costs them far less than it would at the dock.

The matrix makes mistakes easy to see. A column with two `I` letters overloads working memory (UX201 week 1 covers that limit). A `T` with no `P` before it is a wall the player hits cold. A high `r` under an `I` is the worst cell in any level: the cost of failure is highest where failure is most likely.

### Measuring `p`

You can't compute anything without `p`, and you can't guess it. You measure it in a playtest. Count attempts and clears for each challenge across your testers. The estimate is `p̂ = clears / attempts`. With five testers who each clear the dock grapple on their first or second try, you might see 5 clears in 8 attempts, so `p̂ ≈ 0.63`. GD101 week 7 explains how to run the session without coaching, which matters here: every hint you give raises `p` in your notes without raising it in your game.

One playtest gives one `p` per challenge for this group of testers at this point in their learning. The numbers change as players improve, which is the point. Re-measure after each revision.

## 4. Teaching in a shared, persistent world

Single-player levels control the order of lessons. An MMO zone mostly can't. Players arrive at different levels of skill, mobs respawn on timers, and someone else may have killed the monster your introduction depended on. Several tools from this lecture still apply, and a few new problems appear.

- **Order by distance, not by script.** A quest hub sits in the safest spot. Danger rises with distance from it. A player who wanders gets harder challenges, but also a longer walk back, so `r` and difficulty rise together in the direction the zone wants you to learn.
- **Starting zones are lesson plans.** Many MMOs put new characters in a separate starting area with its own order of beats. UX201 week 7 looks at one such zone from the memory side.
- **Recovery is shared.** In a five-player group, a wipe costs five people the recovery time. Groups respond to high `r` by refusing to take learners along, as the Blackrock Mountain example showed. Your graveyard placement shapes who plays with whom.
- **Other players are part of the lesson.** A player who sees someone else die to a patrol has learned something at zero cost. Visible failure (corpses, bloodstains, a death animation others can see) turns one player's `r` into another player's free introduction.

Weeks 11 and 12 return to shared spaces and spawn points in detail.

## In-class activity (25 minutes)

In pairs, pick the first level of a game you both know (a platformer, an action game or an MMO starting zone).

1. **(10 min)** Build its lesson matrix: five to eight beats, every verb it teaches, and your best estimate of `r` for each beat.
2. **(5 min)** Choose the three challenges you think have the lowest `p`. Estimate `t`, `p` and `r` for each and compute `E[T]` and the penalty ratio.
3. **(5 min)** Find the worst cell: the highest `r` sitting on a low `p`. Propose one layout change (move a checkpoint, make a failure non-lethal, add a practice beat) and compute the new `E[T]`.
4. **(5 min)** Swap with another pair. Each pair argues whether the other's change removes tension the game needed.

Expected output: the matrix, a three-row table of `t`, `p`, `r`, `E[T]` and penalty ratio, and one proposed change with its before and after times.

## Common misconceptions

- **"A hard game has a harsh penalty."** Difficulty is `p`. Penalty is `r`. Celeste has low `p` and low `r`. A game can have high `p` and huge `r` (a simple jump at the end of a long unskippable sequence). Name which one you mean.
- **"More checkpoints always make a game easier."** They change time, not `p`. For a skilled player at `p = 0.9` the table above moves 14.7 seconds to 9.1. They make the game faster for learners and remove stakes for everyone.
- **"Teaching means tutorial text."** World 1-1 teaches its core verbs with no text at all. Text is one tool, and usually the weakest (UX201 week 7).
- **"If the average time is fine, the level is fine."** The mean hides the tail. At `p = 0.2`, about one player in nine fails ten or more times in a row (`0.8¹⁰ ≈ 0.107`).

## Check yourself

1. A grapple challenge has `t = 6` seconds, `p = 0.25` and `r = 30` seconds. What are `E[T]` and the penalty ratio? What is `E[T]` if you move the respawn point so that `r = 3`?
2. For the same challenge, you want the penalty ratio at `p = 0.25` to be at most 1.5. What is the largest `r` you can allow? With `s = 2` seconds and `v = 6` m/s, how far before the challenge can the checkpoint be?
3. A segment holds two challenges, each with `c = 10` seconds, one with `p = 0.5` and one with `p = 0.8`. The respawn delay is `s = 2`. Compute `E[segment]` with the hard challenge first, then with it second. Which order should a designer prefer, and why?
4. Celeste only offers Golden Strawberries after the player has beaten the Chapter 8 B-side. Use the penalty ratio to explain why that timing makes sense.

<details>
<summary>Answers</summary>

1. `E[T] = (6 + 30 × 0.75) / 0.25 = 28.5 / 0.25 = 114` seconds. Penalty ratio `1 + (30/6) × 0.75 = 4.75`. With `r = 3`: `(6 + 2.25) / 0.25 = 33` seconds.
2. `1 + (r/6) × 0.75 ≤ 1.5` gives `r ≤ 4` seconds. Subtract the 2-second respawn delay and 2 seconds remain for walking, so `d ≤ 2 × 6 = 12` metres.
3. Hard first: `run = 10 + 10 × 0.5 = 15`, `P = 0.4`, `E = (15 + 2 × 0.6) / 0.4 = 40.5` seconds. Hard second: `run = 10 + 10 × 0.8 = 18`, `E = (18 + 1.2) / 0.4 = 48` seconds. Hard first is cheaper, because a failure there wastes less of the run. Put the likeliest failure early in a segment, or give it its own checkpoint.
4. The Golden Strawberry makes `r` a whole chapter, so `r / t` is huge. The penalty ratio is `1 + (r/t)(1 − p)`, so it only stays tolerable when `1 − p` is small. Players who have beaten that B-side have high `p` on the regular chapters, which keeps the product manageable. Offered to a new player, the same rule would multiply their time many times over.

</details>

## Lab / assignment hook

[Lab 01, checkpoint placement and a one-verb lesson](../labs/lab01.md). You implement the retry model and the segment model in Python, find the best checkpoint placement for a sample level, then design a five-beat paper level that teaches one verb, measure `p` for its challenges with three testers, and place its checkpoints with the model. The paper level becomes the starting point for your Lab 02 blockout.

## Sources

- Super Mario Wiki, "World 1-1 (Super Mario Bros.)" (accessed September 2026). Layout of the first screen (flat start, approaching Goomba, first `?` block, first Magic Mushroom in the second `?` block) and Miyamoto's statement that World 1-1 was made late, citing Eurogamer, "Miyamoto on World 1-1: How Nintendo made Mario's most iconic level," YouTube, 7 September 2015.
- Super Mario Wiki, "Super Mushroom" (accessed September 2026). In Super Mario Bros. (NES, 1985) the Magic Mushroom moves at Mario's walking speed and reverses direction on touching a wall.
- Super Mario Wiki, "Checkpoint" (accessed September 2026). Unmarked checkpoints in Super Mario Bros.; none in Super Mario Bros. 3 because of its shorter levels; the Midway Gate in Super Mario World as the series' first checkpoint object.
- Celeste Wiki (celeste.ink), "Madeline," "Strawberries," "Forsaken City" and "Assist Mode" (accessed September 2026). Respawn within seconds; room-based respawn points; Golden Strawberries unlocked after the later B-side chapter, lost on death with a return to the room where they were collected.
- Dark Souls Wiki (darksouls.fandom.com), "Death," "Bonfire (Dark Souls)" and "Bloodstain" (accessed September 2026). Respawn at the last bonfire rested at; resting respawns enemies; souls left in a bloodstain and lost on a second death. Applies to the original Dark Souls (2011).
- Warcraft Wiki (warcraft.wiki.gg), "Death (gameplay)," "Spirit Healer" and "Resurrection Sickness" (accessed September 2026). Ghost spawns at the nearest graveyard; corpse running; Blackrock Mountain graveyard history; spirit healer cost of 50% durability and one minute of Resurrection Sickness since patch 10.0.0, none for characters level 10 and under.
- Nutt, C. (2012, April 13). "The Structure of Fun: Learning from *Super Mario 3D Land*'s Director." Game Developer (then Gamasutra). Hayashida's four-step level structure, as summarised in UX201 week 7.
- Totten, C. W. (2019). *An Architectural Approach to Level Design* (2nd ed.). CRC Press.
- The retry and segment models, the Flooded Mill level and all values of `t`, `p`, `r`, `s` and `v` are teaching models built for this lecture, not measurements of any game.

## Interactive spec: examples/w01-retry-cost.html

**Purpose.** Show that recovery time after failure costs learners far more than experts, because the cost is paid once per failure and learners fail most.

**The one insight the visual must make obvious.** Dragging the checkpoint away from the challenge makes the gap between the `E[T]` curve and the `r = 0` baseline balloon at low `p` while the right end of the chart (high `p`) barely moves.

**Layout.** Two tabs: "One challenge" (default) and "Segment". Mobile (390px): strip on top, chart below, numbers panel below the chart. Desktop (1280px): strip and chart side by side, numbers panel under both.

**Tab 1, One challenge.**

- Left view, "Level strip": a horizontal side-on strip 0 to 320 m. A challenge marker (a plain gap in the ground) fixed at 310 m. A checkpoint flag draggable from 0 to 310 m (snap 10 m). A bracket between flag and gap labelled with `d` and the walk-back time `d / v`.
- Right view, "Expected time to clear": x axis `p` from 0.05 to 1.0, y axis `E[T]` in seconds (auto-scale, cap at 600 with an off-scale arrow). Two curves: current `r` (solid) and `r = 0` (dashed, labelled "instant retry"). Shade the area between them and label it "time added by layout." A vertical marker at the selected `p` with both values labelled.
- Controls: `p` slider 0.05 to 1.0 (step 0.05, default 0.2); `t` slider 2 to 30 s (step 1, default 8); respawn delay `s` 0 to 10 s (step 1, default 2); speed `v` 2 to 12 m/s (step 1, default 6); checkpoint distance `d` via the flag or a numeric input 0 to 310 (default 300). Presets: "Celeste-like (d = 0, s = 1)", "Far checkpoint (d = 300)", "Near checkpoint (d = 60)". Reset.
- Numbers panel: `r = s + d / v`, `E[T]`, `E[T]` at `r = 0`, penalty ratio, attempts per hour `3600 / (t + r × (1 − p))`, and a sentence: "At p = 0.20 this layout adds 208.0 s per clear. At p = 0.90 it adds 5.8 s." (with the defaults `r = 52`; "adds" is measured against the `r = 0` baseline, so it is 8 s larger than the lecture's 200 s near-versus-far comparison, which uses `r = 2`)

**Tab 2, Segment.**

- Strip with three challenges at 100, 200 and 300 m. Each has its own `p` slider (0.05 to 1.0, default 0.5) and `c` (default 10 s, the time to reach and attempt it from the previous challenge or checkpoint). Up to three checkpoint toggles, one before each challenge; the one before challenge 1 is always on.
- A bar chart with one bar per segment showing `E[segment]` and a total bar. A second total drawn as an outline for "checkpoint before every challenge" for comparison.
- A "Swap order" button that reverses the challenge order.

**Formulas.**

- `r = s + d / v`.
- `E[T] = (t + r × (1 − p)) / p`. Baseline `E₀ = t / p`. Penalty ratio `E[T] / E₀ = 1 + (r/t)(1 − p)`.
- Segment with costs `c₁..cₖ` and chances `p₁..pₖ`: `reach₁ = 1`, `reachᵢ₊₁ = reachᵢ × pᵢ`, `run = Σ cᵢ × reachᵢ`, `P = reachₖ₊₁`, `E[segment] = (run + s × (1 − P)) / P`. Total = sum over segments.

**Test values.**

- `t = 8`, `s = 2`, `v = 6`: `d = 0` gives `r = 2`, `E[T]` 48.0 / 18.0 / 9.1 at `p` = 0.2 / 0.5 / 0.9. `d = 60` gives `r = 12`, 88.0 / 28.0 / 10.2. `d = 300` gives `r = 52`, 248.0 / 68.0 / 14.7 (9.1 is 9.11, 10.2 is 10.22, 14.7 is 14.67 before rounding).
- Penalty ratios at `d = 300`: 6.20 / 4.25 / 1.65. At `d = 0`: 1.20 / 1.13 / 1.03 (exact 1.125 and 1.025 round half up; nudge before rounding so binary floats do not turn 1.025 into 1.02).
- `t = 6`, `p = 0.25`, `r = 30`: `E[T] = 114.0`, ratio 4.75.
- Segment tab, `c = 10`, `s = 2`, all `p = 0.5`: one checkpoint 154.0 s; three checkpoints 66.0 s. All `p = 0.9`: 37.9 s vs 34.0 s.
- Segment with two challenges (third disabled or `p = 1`, `c = 0`): `p = 0.5` then `0.8` gives 40.5 s; swapped gives 48.0 s.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`, light and dark. The current curve and the baseline differ by line style as well as colour. The flag is keyboard-draggable (arrow keys move 10 m, Shift+arrow 50 m) and mirrored by the numeric input. Respect reduced motion (no animated transitions of curves). No game art or characters; the strip uses flat shapes only.

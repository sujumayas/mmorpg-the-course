# GD102 · Week 04 — Negative feedback loops (rubber-banding)

**Why this matters:** Last week you saw how a lead feeds itself until the game is decided long before it ends. This week you learn the opposite loop, the one that pulls a leader back toward the pack. Almost every competitive game ships with one, and the strength you give it decides whether early skill matters at all.

**You will be able to:**
- Identify a negative (balancing) feedback loop in a game by naming its goal, its discrepancy and its correcting flow.
- Compute the steady-state gap `d / k` and the approach to it for a simple lead-and-correction model, and predict when a correction overshoots.
- Compare position-based and distance-based catch-up rules and predict what each does to lead stability.
- Critique a rubber-band mechanic by measuring two things at once, how close races are and how often the early leader still wins.

**Before class:** Meadows, *Thinking in Systems: A Primer* (2008), chapter 1 (the sections on balancing feedback loops) and chapter 2 (the thermostat and the inventory-with-delays examples). Adams & Dormans, *Game Mechanics: Advanced Game Design* (2012), chapter 3, the section on feedback loops.

**Prerequisites from earlier courses:** [GD102 week 3, positive feedback loops](w03-positive-feedback-loops-snowballing.md). Formal elements and MDA from GD101 [week 2](../../GD101-introduction-to-game-design/lectures/w02-players-objectives-procedures-rules.md), [week 3](../../GD101-introduction-to-game-design/lectures/w03-resources-conflict-boundaries-outcome.md) and [week 4](../../GD101-introduction-to-game-design/lectures/w04-mda-mechanics-dynamics-aesthetics.md). Geometric shrinking `(1 − k)^t` from [MA101 week 4, exponentials](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md). Running many random trials from [MA102 week 11, Monte Carlo simulation](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w11-monte-carlo-simulation.md).

**Interactive:** [Kart rubber banding](../examples/w04-kart-rubber-band.html). Keep it open during section 2.

---

## 1. The loop that pulls back

A **feedback loop** is a chain of cause and effect that comes back to where it started. A change in some quantity causes other changes that eventually change that same quantity again. Week 3 covered the loop where the return push goes the same way as the original change. More gold buys more workers, more workers mine more gold. That is a **positive** or **reinforcing** loop, and its signature is runaway growth.

A **negative feedback loop** pushes back against the change. Meadows calls it a **balancing loop**, which is the better name, because "negative" sounds like "bad" and it isn't. Every balancing loop has four parts:

1. A **stock**, the quantity being controlled. In a room it is the temperature. In a race it is the gap between first and second place.
2. A **goal**, the value the loop steers toward. For a thermostat it is the set temperature. For a catch-up mechanic it is usually zero gap, "keep the pack together".
3. A **discrepancy**, the difference between the stock and the goal.
4. A **correcting flow**, which changes the stock in the direction that shrinks the discrepancy. Its size usually grows with the discrepancy.

The thermostat is Meadows' standard example. The room is 15 °C, the setting is 20 °C, the discrepancy is 5 °C, so the furnace runs. As the room warms, the discrepancy shrinks and the furnace eventually stops. Heat also leaks out through the walls, so the room never sits exactly at 20 °C. It settles where the furnace's push and the leak balance. Hold that thought. It is the whole lesson in miniature.

### Rubber-banding is a balancing loop on a difference

In a single-player system the stock is often one number, such as health or ammunition. In a competitive game the stock the designer cares about is usually a **difference between players**. That is the lead, the score margin, or the wealth gap. A mechanic that pulls that difference back toward zero is called **rubber-banding** or a **catch-up mechanic**. The image is a rubber band tied between the leader and the pack. The further the leader pulls away, the harder the band pulls back.

Rubber-banding can act in two directions:

- **Help the trailer.** Give players who are behind stronger items, more resources or extra speed.
- **Hinder the leader.** Attack whoever is ahead, slow them, or make them pay more for the same thing.

Both shrink the gap. They feel very different to play, and that difference is a design decision you will make repeatedly.

### Spotting the sign of a loop

Draw the loop as a circle of arrows. Label each arrow `+` if the two quantities move in the same direction ("more gap → more catch-up power" is `+`), and `−` if they move in opposite directions ("more catch-up power → less gap" is `−`). Count the minus signs around the loop.

- An **even** number of minus signs (including zero) gives a reinforcing loop.
- An **odd** number gives a balancing loop.

The rubber band has one `+` and one `−`, so it balances. The worker loop from week 3 has two `+` signs and balances nothing. This counting trick works on loops of any length, and it is how you will read the causal diagrams in weeks 5 and 6.

## 2. Worked example: the item box as a balancing loop

### The hook

The Spiny Shell first appeared in Mario Kart 64 in 1996. Players know it as the blue shell. Once fired, it flies ahead to whoever is in first place and knocks them out of their stride. It is a pure "hinder the leader" correction. The racers behind do not need to aim. The shell does the aiming, and it always aims at the front.

In Mario Kart 8 Deluxe the item boxes themselves carry a second, quieter correction. The item you receive depends on **how far you are from the front-runner**, not only on your position number. Racers well behind the leader get access to the strongest items, and the leader cannot pull a Spiny Shell from a box at all. So the item box is a random draw whose odds are tuned by the gap, a correcting flow that grows with the discrepancy.

Players feel both. A race where you led for two laps and lost on the last straight leaves a mark. The question this worked example answers is how strong that pull can be before leading stops mattering.

We will not reproduce Nintendo's item tables. They differ by game and are known mainly from data mining. Instead we build a small model with the same structure, a correction that grows with the gap, and measure what it does.

### One model, stated once

Take two racers. The leader is slightly faster and gains `d` metres per second of racing on the chaser. The catch-up mechanic hands the chaser extra speed equal to `k` times the current gap. Write `g_t` for the gap after `t` seconds:

```
g_(t+1) = g_t + d − k × g_t
```

- `g_t` is the stock, the gap in metres.
- `d` is the leader's natural edge, metres gained per second from skill or a better kart.
- `k` is the feedback strength, the fraction of the current gap the chaser recovers each second.
- The goal is zero gap, so the discrepancy is `g_t` itself, and `k × g_t` is the correcting flow.

This is the thermostat again. The leader's edge `d` is the leak, a steady push away from the goal. The correction `k × g_t` is the furnace. The gap settles where the two cancel, when `d = k × g`:

```
steady-state gap  g* = d / k
```

Solve the recurrence starting from `g_0 = 0` and you get

```
g_t = (d / k) × (1 − (1 − k)^t)
```

The factor `(1 − k)^t` is the geometric shrink from MA101 week 4. Each second the remaining distance to `g*` is multiplied by `1 − k`.

### Numbers you can check

Let the leader gain `d = 2` metres per second. Compare no feedback, a moderate band and a strong band.

| Second `t` | `k = 0` | `k = 0.25` | `k = 0.5` |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 1 | 2 | 2.00 | 2.00 |
| 2 | 4 | 3.50 | 3.00 |
| 3 | 6 | 4.63 | 3.50 |
| 4 | 8 | 5.47 | 3.75 |
| 5 | 10 | 6.10 | 3.88 |
| 6 | 12 | 6.58 | 3.94 |
| long run | grows without limit | 8 | 4 |

Check one row by hand. At `k = 0.25`, second 2: `2 + 2 − 0.25 × 2 = 3.5`. Second 3: `3.5 + 2 − 0.875 = 4.625`. The closed form agrees: `8 × (1 − 0.75^6) = 8 × 0.822 = 6.58`.

Read the table as a designer:

- **Without feedback the lead grows forever.** A faster racer's lead is a straight line in time. The race is decided by whoever is faster, and the gap at the finish shows by how much.
- **With feedback the lead stops growing.** It levels off at `d / k`. Doubling `k` halves the final gap.
- **The leader still leads.** A balancing loop with a steady push does not erase the lead, it caps it. The faster racer sits 8 metres ahead forever at `k = 0.25`. What erases leads is the combination of a small capped gap and **noise**, random events that can now flip first and second because the gap is so small.

That last point is where the real design question lives, and it needs a simulation.

### A visual you can move

Open `examples/w04-kart-rubber-band.html`. It races eight karts for 120 seconds. Each kart has a base speed of 10 m/s, a skill offset from +0.35 m/s for the best driver down to −0.35 m/s for the worst, and random noise every second (the bumps, the bad corners, the item hits). A single slider sets the **feedback strength** from 0% to 100%, and a toggle chooses how the catch-up bonus is computed:

- **By distance**, like Mario Kart 8 Deluxe. Each kart's bonus is proportional to its distance behind the leader, up to a cap.
- **By position**, the simpler rule. Each kart's bonus depends only on its rank, first gets nothing, last gets the most.

The top view shows one race as eight lines of "metres behind the leader". The bottom view runs 2,000 races and plots two measurements against feedback strength:

- **Closeness**, the average distance from first to last at the finish.
- **Early-lead value**, the share of races won by whoever led at the halfway mark.

Here are the numbers the interactive should reproduce (2,000 races each, so expect a point or two of random wobble):

| Mode | Strength | Spread first to last (m) | Halfway leader wins | Best driver wins | Lead changes per race |
|---|---|---|---|---|---|
| none | 0% | 95 | 67% | 62% | 11 |
| distance | 25% | 33 | 44% | 55% | 17 |
| distance | 50% | 19 | 33% | 47% | 23 |
| distance | 100% | 12 | 24% | 37% | 34 |
| position | 25% | 51 | 53% | 59% | 17 |
| position | 50% | 21 | 34% | 47% | 28 |
| position | 100% | 7 | 16% | 27% | 60 |

With eight karts, a winner picked by coin toss would win 12.5% of the time. Keep that number in mind.

Drag the slider from 0 to 100% and watch the two views disagree. The top view looks better and better. The pack tightens, lines cross, the finish is close. The bottom view tells you what you paid for it. At full position-based strength the halfway leader wins 16% of races, barely above the 12.5% a random draw would give. Leading for a full minute has almost no value. The best driver still wins more than their share, 27% against 12.5%, but a player who races perfectly now loses almost three races in four.

That is the insight this example exists to make visible. **Rubber-banding buys closeness with the currency of early-lead value.** Closeness is what you see on screen. Early-lead value is what a skilled player feels over a season.

Two more things to notice in the interactive:

- **Which rule drains the lead faster depends on strength.** At 25%, distance mode is the harsher one. The halfway leader wins 44% against position mode's 53%, because at low strength the position bonus (at most 0.5 m/s for last place) is too small to close a field that has spread out, while the distance bonus keeps growing with the gap. The two curves cross between 50 and 60%. Above that, distance mode keeps more early-lead value. At 100% the halfway leader wins 24% in distance mode against 16% in position mode, with about half as many lead changes. A distance rule only pulls hard when the gap is large. A strong position rule pulls on the leader of a tight pack exactly as hard as on the leader of a strung-out field, so it churns the order even when nobody is running away.
- **The steady-state formula still holds on average.** In distance mode at 50% strength, `k = 0.05` per second. The best-to-worst skill difference is `0.7` m/s, so `d / k` predicts a 14 m spread from skill alone. The simulation shows 19 m. The extra few metres come from noise. The model you can do by hand gets you most of the way.

### Cross-game recognition

Rewrite each of these into the form "correcting flow = strength × discrepancy" and you will see the same loop.

**League of Legends (bounties, 2026 patches, V26.01 onward).** Killing an enemy champion pays a base bounty of 300 gold at levels 1 to 6, rising to 420 at level 18. A champion who keeps earning gold without dying accumulates extra bounty, and past a threshold they enter a shut-down state where their extra worth is shown on the scoreboard. Killing them pays the base plus the accumulated extra, capped at base plus 700 per kill. A champion who keeps dying loses bounty, down to a floor of 50. The stock is a champion's lead in gold. The correcting flow is the extra gold paid to whoever ends the streak. It grows with the lead, so it is proportional correction, with a cap, exactly like distance mode with its 60 m cap. Riot's recent changes in this system tuned how fast bounty accrues and decays, which is tuning `k`.

**Catan (base game rules, 2015 edition).** When any player rolls a 7, nobody collects resources, and every player holding more than 7 resource cards returns half of them, rounded down. The stock is a player's hand. The goal is "7 or fewer". The correcting flow is zero below the threshold and half the hand above it. This is a balancing loop with a threshold instead of a smooth slope, and it hits whoever is hoarding hardest. The same roll lets the roller move the robber onto any hex and steal a card from a player next to it. That is a "hinder the leader" correction whose strength is chosen by the players, who usually aim it at whoever is winning. The loop is social, run by people instead of code.

**The thermostat (Meadows).** Stock, room temperature. Goal, the setting. Discrepancy, setting minus temperature. Correcting flow, the furnace, pushing against a steady leak. The room settles near the goal but slightly below it, for the same reason the faster racer holds a small lead at `d / k`. A steady push against proportional correction always leaves a residual gap. Meadows makes this point about thermostats, and you just saw it in a kart race.

Three settings, one structure: a discrepancy, a correction that grows with it, and a steady-state gap set by the ratio of the push to the correction strength.

### Eyes-open design judgment

Rubber-banding is neither cheating nor a fix-all. It is a trade you make on purpose.

What it buys you:

- **Games stay live longer.** Trailing players keep making meaningful decisions instead of waiting for a foregone result. In a party game with mixed skill levels, that is often the entire point.
- **Mixed-skill groups can play together.** A strong band lets a newcomer and an expert share a race. The expert still wins more often, just not every time.
- **It caps runaway leads from positive loops.** If your game already has a snowball (week 3), a balancing loop is the standard counterweight.

What it costs you:

- **Early play matters less.** The table shows this plainly. If your game is meant to reward sustained skill, a strong band works against your own goal.
- **Leading can become a trap.** If the leader is punished hard enough, the best strategy is to sit in second and strike late. When players start doing that deliberately, the balancing loop has created a new dominant strategy. GD203 week 13 raises the same worry about adaptive difficulty that players can exploit by playing badly on purpose ([GD203 week 13](../../GD203-combat-and-progression-design/lectures/w13-difficulty-modes-and-scaling.md)).
- **Hidden correction feels unfair when discovered.** A visible bounty on the scoreboard reads as a rule everyone plays by. An invisible speed boost for the computer racers reads as the game lying.

Decisions to make deliberately, not by reflex:

- **What is the discrepancy?** Rank, distance, score or resources. Rank is cheap to compute and noisy. Distance responds to what actually happened.
- **How strong is `k`?** Pick it by deciding what share of races the halfway leader should win, then tune until the simulation agrees.
- **Is there a cap?** A cap on the correction keeps a far-behind player from being launched to the front.
- **Help the trailer or hinder the leader?** Helping feels generous. Hindering feels like being attacked. Both shrink the gap.
- **Is it visible?** If players can read the rule, they can plan around it, and that planning is part of the game.

## 3. When balancing loops overshoot

The recurrence `g_(t+1) = (1 − k) × g_t + d` hides a warning. Look at the factor `1 − k`.

- If `0 < k < 1`, the factor is between 0 and 1. The gap approaches `d / k` smoothly from one side.
- If `1 < k < 2`, the factor is negative. The correction is so strong that it overshoots, and the chaser passes the leader. Next second the roles swap and the correction pulls the other way. The gap flips sign every step while shrinking.
- If `k > 2`, the factor has size greater than 1. The flips grow instead of shrinking and the system shakes itself apart.

Try it with `d = 0` and a starting gap of 10. At `k = 0.5` the gap goes 10, 5, 2.5, 1.25. At `k = 1.5` it goes 10, −5, 2.5, −1.25, the lead changes every second. At `k = 2.5` it goes 10, −15, 22.5, −33.75.

In real games the overshoot usually comes from a **delay** rather than a huge `k`. The correction acts on old information. A blue shell is picked up, carried for a while, then fired at whoever is first *now*, which may not be the racer who was running away when it was picked up. Meadows' inventory example in chapter 2 makes the same point about a car dealer who reorders stock based on last week's sales and ends up with too much, then too little. A balancing loop plus a delay tends to oscillate. If you see the lead swinging back and forth in a playtest, look for a delay before you reach for a smaller `k`.

## 4. Mixing loops: which one dominates?

Real games run several loops at once. A racing game might have a small reinforcing loop (the leader drives on a clean track while the pack fights each other) and a balancing loop (the item box). Which one wins?

Compare their strengths near the current state. Suppose the reinforcing loop adds 3% of the gap per second, and the balancing loop removes 5% of the gap per second. The net effect is `−2%` per second, balancing. If a patch halves the item effect to 2.5%, the net becomes `+0.5%` per second and the same game now snowballs. Nothing about the loops' structure changed. Only their relative strength did.

Meadows calls this **shifting dominance**. It is why balance patches that look small can change the character of a game. It is also why you should never describe a game as simply "having negative feedback". Say which loop dominates, under what conditions, and by how much.

A common pattern in board and video games is to let the reinforcing loop dominate early and the balancing loop dominate late, or the reverse. Building a lead early and defending it late feels like a story. A lead that can never be built or can never be lost does not.

## In-class activity (25 minutes)

Work in pairs. You need the interactive, a sheet of paper and a calculator.

1. **Pick a target.** Decide what share of races the halfway leader should win in a party racer for mixed-skill groups, and a separate target for a competitive racer. Write both numbers down with one sentence of justification each. (5 minutes)
2. **Tune.** Use the interactive to find the feedback strength that hits each target, once in distance mode and once in position mode. Record the strength, the spread and the lead changes per race for all four settings. (10 minutes)
3. **Diagnose.** For your party-racer setting, write the balancing loop in four parts (stock, goal, discrepancy, correcting flow) and sketch it as a two-arrow loop with signs. (5 minutes)
4. **Break it.** Swap sheets with another pair. Describe one way a player could exploit their competitive-racer setting, for example by sandbagging in second place. (5 minutes)

Expected output: a half-page sheet with two targets, a four-row tuning table, one loop diagram and one exploit.

## Common misconceptions

- **"Negative feedback means the game punishes you."** Negative describes the direction of the loop, not its effect on anyone's mood. The thermostat is a negative feedback loop and it keeps you warm.
- **"A strong enough catch-up mechanic makes the game random."** Not quite. In the simulation, even at the strongest setting the best driver wins about twice their fair share. Rubber-banding reduces the value of a lead. It does not erase skill, unless it also rewards being behind so much that skill stops mattering.
- **"Balancing loops remove the lead."** A steady advantage against proportional correction settles at `d / k`, a smaller lead that never quite disappears. What makes leads change hands is that small gap combined with noise.
- **"Position-based and distance-based catch-up are the same thing."** At 100% strength the position rule churns the order almost twice as often (60 lead changes against 34), because it pulls on the leader of a tight pack as hard as on a runaway leader. At 25% the ranking flips and the distance rule drains the lead faster. Which rule is gentler depends on how hard you set it.

## Check yourself

1. A leader gains `d = 3` m/s on a chaser, and the chaser recovers `k = 0.2` of the gap each second. What gap does the race settle at? How big is the gap after 2 seconds, starting from zero?
2. A designer wants the steady-state gap in question 1 to be 6 m. What `k` do they need? What goes wrong if they overshoot and use `k = 1.2`?
3. In a four-player strategy game, each player gets bonus income equal to 10% of the difference between their gold and the richest player's gold. Name the stock, the goal, the discrepancy and the correcting flow. Is this closer to position mode or distance mode?
4. A playtest report says races "feel close but pointless". Which of the interactive's two measurements would you check first, and what would you expect to see?

<details>
<summary>Answers</summary>

1. `g* = d / k = 3 / 0.2 = 15` m. Second 1: `0 + 3 − 0 = 3`. Second 2: `3 + 3 − 0.6 = 5.4` m. Check with the closed form, `15 × (1 − 0.8^2) = 15 × 0.36 = 5.4`.
2. `k = d / g* = 3 / 6 = 0.5`. At `k = 1.2`, the factor `1 − k = −0.2` is negative, so the correction overshoots. The chaser passes the leader, the gap flips sign each second while shrinking, and first place changes hands every step. The steady state is `3 / 1.2 = 2.5` m, reached by oscillating around it.
3. Stock, each player's gold. Goal, the richest player's gold. Discrepancy, richest gold minus own gold. Correcting flow, 10% of that discrepancy as bonus income. It is distance mode, because the bonus depends on how far behind you are, not on your rank.
4. Check early-lead value, the share of games won by the halfway leader. "Close but pointless" suggests a small spread (the close part) with a halfway-leader win rate near the random baseline of one over the number of players (the pointless part). The fix is to lower `k` or cap the correction until the halfway leader wins noticeably more than chance.

</details>

## Lab hook

**Lab 04, rubber-band tuning** ([labs/lab04.md](../labs/lab04.md)). You build the two-racer recurrence and an eight-racer simulation in a spreadsheet, reproduce two rows of the table in section 2, then tune a catch-up rule to hit a stated early-lead target and write a 300-word recommendation.

## Sources

- Meadows, D. H. (2008). *Thinking in Systems: A Primer*. Chelsea Green. Chapter 1 defines balancing and reinforcing loops; chapter 2 works through the thermostat (including the residual gap caused by a steady leak), the inventory system with delays, and shifting dominance between loops. Paraphrased.
- Adams, E. & Dormans, J. (2012). *Game Mechanics: Advanced Game Design*. New Riders. Chapter 3, feedback loops in games.
- Super Mario Wiki, "Spiny Shell (Mario Kart)". The item first appeared in Mario Kart 64 (1996) and targets the racer in first place. The same page describes item distribution in Mario Kart 8 Deluxe as based on distance from the front-runner, and notes the shell can come from any place other than first.
- League of Legends Wiki, "Champion gold bounties" (accessed September 2026; accrual rates last changed in V26.01, base 420 at level 18 since V25.09). Base bounty 300 gold at levels 1 to 6 rising to 420 at level 18, accrual from gold earned, shut-down state, per-kill cap of base plus 700, floor of 50 gold.
- Catan GmbH, *Catan: Game Rules & Almanac*, base game, 2015 edition (downloaded from catan.com). Rolling a 7: no production, players with more than 7 resource cards return half rounded down, the roller moves the robber and steals one card.
- Simulation results in section 2 were computed for this course with the model in the interactive spec (2,000 races per setting, Python, seed 1). They describe the course model, not any shipped game.

## Interactive spec: examples/w04-kart-rubber-band.html

**The one insight.** A catch-up mechanic makes races look closer (top view) while quietly draining the value of leading (bottom view). The student must see both at once, and see that position-based catch-up drains early-lead value faster than distance-based catch-up at high strength (above about 60%), while at low strength the order flips.

**Layout.** Two stacked panels on mobile, side by side at 1024 px and wider. A control bar above them.

**Controls.**
- Slider `strength` from 0 to 100%, step 5, default 50%.
- Segmented toggle `mode`: "By distance" (default) and "By position".
- Button "New race" reseeds the single race in the top panel only.
- Button "Run 2,000 races" (runs automatically on load and whenever `mode` changes; the curve is precomputed for strength 0, 10, ..., 100 so dragging the slider only moves a marker). Show a progress indicator if the run exceeds 200 ms; use chunked work or a Web Worker so the page never freezes.
- Keyboard: slider responds to arrow keys; toggle and buttons reachable by Tab.

**Model (per race).**
- `N = 8` karts, `T = 120` steps of one second. All positions start at 0.
- Skill `s_i = 0.35 − 0.1 × i` for `i = 0..7` (so +0.35 down to −0.35 m/s). Kart 0 is "best driver".
- Each step, compute `lead = max(x)` and every kart's bonus `b_i` from positions **before** the move:
  - Distance mode: `b_i = 0.1 × f × min(lead − x_i, 60)`, where `f = strength / 100`.
  - Position mode: `rank_i` = 0 for first up to 7 for last (ties broken by index), `b_i = 2.0 × f × rank_i / 7`.
- Move: `x_i ← x_i + 10 + s_i + noise_i + b_i`, with `noise_i` drawn from a normal distribution with mean 0 and standard deviation 1.5 (Box-Muller on a seeded PRNG such as mulberry32).
- After each step record the leader (index of max `x`). A lead change is counted when the leader differs from the previous step's leader. The halfway leader is the leader after step 60.
- Winner is the index of max `x` after step 120.

**Top panel (one race).** Eight lines, x axis time 0 to 120 s, y axis "metres behind leader" (0 at the top, growing downward), clamp display at 120 m. Best driver's line drawn thicker and labelled "best driver". Mark t = 60 with a dashed vertical line labelled "halfway". Beneath, text readout: winner, halfway leader, lead changes, final spread.

**Bottom panel (2,000 races).** x axis strength 0 to 100%. Two lines on a shared 0 to 100% y axis: "Halfway leader wins" and "Best driver wins". A horizontal dashed reference at 12.5% labelled "random winner". A third series, final spread in metres, on a right-hand axis (0 to 100 m) drawn lighter. A vertical marker at the current slider value with a numeric readout of all four metrics (spread, halfway leader wins, best driver wins, lead changes per race) so students can copy them into the lecture table.

**Test values (2,000 races; accept ± 3 percentage points and ± 10% on spread and lead changes).**

| Mode | Strength | Spread (m) | Halfway leader wins | Best driver wins | Lead changes |
|---|---|---|---|---|---|
| any | 0% | 95 | 67% | 62% | 11 |
| distance | 25% | 33 | 44% | 55% | 17 |
| distance | 50% | 19 | 33% | 47% | 23 |
| distance | 100% | 12 | 24% | 37% | 34 |
| position | 25% | 51 | 53% | 59% | 17 |
| position | 50% | 21 | 34% | 47% | 28 |
| position | 100% | 7 | 16% | 27% | 60 |

**Secondary readout (hand-check panel, collapsible).** The two-racer recurrence `g_(t+1) = g_t + d − k × g_t` with inputs `d` (default 2) and `k` (default 0.25), showing the first 7 values and `d / k`. Test: `d = 2, k = 0.25` gives 0, 2, 3.5, 4.625, 5.469, 6.102, 6.576 and steady state 8. With `k = 1.5` and `d = 0`, start 10, the values alternate 10, −5, 2.5, −1.25.

**Style.** Shared palette from `templates/interactive-tokens.css`. Karts are coloured lines only, no characters, logos or game art. Name Mario Kart only in the caption text ("distance mode resembles the rule Mario Kart 8 Deluxe uses").

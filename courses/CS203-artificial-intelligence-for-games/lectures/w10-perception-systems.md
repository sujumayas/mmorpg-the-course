# CS203 · Week 10 — Perception Systems

**Why this matters:** Every NPC decision you built in weeks 6 to 9 starts from what the NPC believes about the world. If that belief is "the player is exactly here, always", your guards cheat. If it is a yes-or-no cone test, your guards snap from asleep to shooting in one frame. A perception system decides what an NPC knows and when it learns it, and in a stealth game that timing is the game.

**You will be able to:**
- Compute how long an NPC takes to detect a player from distance, light and a fill-and-drain awareness meter, by hand and in Python.
- Derive the largest share of time a player can stay exposed without ever being detected, and use it to tune a guard.
- Order a sensing pipeline from cheap tests to expensive ones and estimate its raycast cost.
- Critique a perception design for fairness, using hearing through walls and off-screen guards as test cases.

**Before class:** Martin Walsh, "Modeling Perception and Awareness in Tom Clancy's Splinter Cell Blacklist", *Game AI Pro 2* (2015), chapter 28, sections 28.1, 28.2 and 28.4 (free online). Rich Welsh, "Crytek's Target Tracks Perception System", *Game AI Pro* (2013), chapter 31, sections 31.3 to 31.7. Brook Miles, "How to Catch a Ninja: NPC Awareness in a 2D Stealth Platformer", *Game AI Pro* (2013), chapter 32. Millington, *AI for Games* (3rd ed.), the section on sense management in the chapter on world interfacing.

**Prerequisites from earlier courses:** [MA101 week 13, dot product and vision cones](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w13-dot-product-facing-and-vision-cones.md) (the cone test `f̂ · d̂ ≥ cos(h)` and the graded "focus" value; this week uses both and does not re-teach them). [MA101 week 8, interpolation and remap](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w08-interpolation-lerp-inverse-lerp-remap.md) (turning a distance into a 0-to-1 factor). [CS102 week 10, observer and events](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w10-observer-and-events.md) (polling versus events). [CS203 week 1](w01-game-ai-vs-academic-ai.md) (human reaction time and cheating that players can catch). [CS203 week 4](w04-a-star-and-heuristics.md) (A*, used here to measure how far a sound travels).

**Interactive:** [`examples/w10-detection-meter.html`](../examples/w10-detection-meter.html). Keep it open during section 2.

---

## 1. Sensing is a filter on the truth

Your game already knows everything. The player's position is a variable. So is whether they are crouching, whether the lights are on and which door they just opened. The simplest NPC reads those variables directly. Welsh opens his chapter on Crytek's perception system with exactly this temptation. One function call can tell an agent where the player is. He then points out that once players realize the AI is cheating, they feel cheated.

A **perception system** is the code that sits between the true game state and an NPC's decisions and deliberately withholds information. It answers two questions for every NPC and every thing it might notice:

1. **Can it sense this at all?** Is the player in range, inside a vision shape, lit, and not behind a wall? Is the sound loud enough to reach this guard?
2. **What does it believe, and how sure is it?** Has it just glimpsed movement, or does it know for certain the player is there? Where does it think the player is now?

Three terms will be used all week.

- A **stimulus** (Crytek shortens it to **stim**) is a perceivable event: a footstep, a gunshot, the player standing in view, a door left open. It has a type, a position, a source and a radius within which it can be sensed.
- **Awareness** is the NPC's internal state about a stimulus source. Walsh defines it for Splinter Cell as a set of discrete mental states reached progressively over time through perception. You first notice "something over there", and only later know it is an enemy.
- **Memory** is what the NPC keeps once the stimulus stops, usually a last known position and a timer.

The split between sensing and awareness is the idea to hold on to. Sensing is a filter, a set of yes-or-no tests. Awareness is a quantity that changes over time. Most perception bugs come from collapsing the two, so that the moment a test passes the NPC knows everything.

### The sense pipeline

Sight in most games is a chain of tests. You met the first two in MA101.

1. **Range.** Is the target within the sight radius? Compare squared distances, no square root needed.
2. **Shape.** Is it inside the vision cone (`f̂ · d̂ ≥ cos(h)`), or inside a peripheral or long-range shape?
3. **Light and stance.** Is the target lit? Is it crouched in cover? These scale or gate the result.
4. **Line of sight.** Does a ray from the NPC's eyes to the target hit a wall? This is the expensive test.

Put them in this order because each test is cheaper than the next and rejects most candidates. Range and shape are a few multiplications. A raycast walks the collision geometry. Walsh reports that Blacklist cast rays to eight different bones on the player's body, and that the player's stance set how many visible bones it took to start detection. That is eight raycasts per guard per check, so you want as few guards as possible reaching step 4.

## 2. Worked example: the meter that gives you time

### The hook

In Splinter Cell Blacklist (Ubisoft Toronto, 2013), a guard can look straight at you and not react. A small marker grows on your screen instead. If you duck back into cover before it fills, the guard shrugs and goes on patrolling. If you stay, it fills and he opens fire.

Walsh explains what is happening. When the player is inside one of the guard's vision shapes, unobstructed and lit, a timer starts. The timer's full length is set by which shape the player is in, and within that range it scales linearly with distance. The growing HUD element shows the timer. It is, in Walsh's words, the player's window of opportunity to break line of sight or deal with the guard. Some games, Splinter Cell included, add an intermediate state partway along the bar, where the guard knows he saw something and goes to investigate.

So the guard "sees" you in the sense-pipeline meaning at once, but becomes aware of you only after a delay. Here is the puzzle. Players quickly learn to peek: lean out, look, lean back. Does peeking ever get you caught? If the meter resets the instant you hide, never. If it never drains, always, eventually. Neither is what a designer wants. The answer sits in one number most teams tune by feel.

### The model

Keep one number per NPC per target, the **awareness meter** `a`, between 0 and 1. Every AI tick of length `Δt`:

```
while the target passes the sense pipeline:   a ← a + Δt / T(d, ℓ)
otherwise:                                    a ← max(0, a − Δt / F)

T(d, ℓ) = [T_near + (T_far − T_near) × min(d, R) / R] / ℓ
```

- `a` is awareness. At `a ≥ 0.5` the NPC is **suspicious** and investigates. At `a ≥ 1` it is **alert** and treats the target as an enemy. The thresholds are design choices.
- `T(d, ℓ)` is the **fill time**, the seconds of unbroken sight needed to go from 0 to 1.
- `d` is distance to the target and `R` the sight range. `T_near` is the fill time at point-blank range, `T_far` the fill time at the edge of range.
- `ℓ` is the light level on the target, from 0 (dark) to 1 (fully lit). Dim light stretches the fill time. `ℓ = 0` means never.
- `F` is the **forget time**, the seconds an unseen NPC takes to drain a full meter back to zero.

The fill part is Blacklist's rule, a timer whose length grows linearly with distance. The drain part is the piece this lecture adds, and it is what the hook's question is about.

This week's numbers: `T_near = 1 s`, `T_far = 4 s`, `R = 20 m`, `F = 6 s`, `Δt = 0.1 s`. They are invented for teaching. Blacklist's tuned values are not published.

Now the peeking question. Suppose the player repeats a cycle: exposed for `e` seconds, hidden for `h` seconds. Each exposure adds `e / T`. Each hiding removes up to `h / F`. The meter climbs over many cycles only if it gains more than it loses:

```
e / T > h / F
```

Rearrange for the share of time spent exposed, `f = e / (e + h)`:

```
never detected  if  f ≤ f* = T / (T + F)
```

`f*` is the **break-even exposure**. It depends on distance and light through `T`, and on the designer's choice of `F`. It tells you exactly how much peeking your guard tolerates.

Here is the model in Python. The meter runs in integer ticks so that comparisons do not drift.

```python
T_NEAR, T_FAR, RANGE = 1.0, 4.0, 20.0   # seconds to fill at 0 m and at 20 m
FORGET = 6.0                            # seconds for a full meter to drain
DT = 0.1                                # one AI tick

def detect_time(d, light=1.0):
    """Seconds of unbroken sight needed to fill the meter from empty."""
    t = T_NEAR + (T_FAR - T_NEAR) * min(d, RANGE) / RANGE
    return t / light

def first_detection(pattern, d, light=1.0, forget=FORGET, limit=60.0):
    """pattern: list of (seconds, seen) repeated. Time the meter fills, or None."""
    meter, ticks = 0.0, 0
    while ticks * DT < limit:
        for seconds, seen in pattern:
            for _ in range(round(seconds / DT)):
                ticks += 1
                if seen:
                    meter += DT / detect_time(d, light)
                else:
                    meter = max(0.0, meter - DT / forget)
                if meter >= 1 - 1e-9:
                    return round(ticks * DT, 1)
    return None

for d in (0, 5, 10, 15, 20):
    print(f"{d:>2} m: fill {detect_time(d):.2f} s")
print("stand in view at 10 m:", first_detection([(1.0, True)], 10))
print("peek 1.5 s, hide 2 s: ", first_detection([(1.5, True), (2.0, False)], 10))
print("peek 1.0 s, hide 3 s: ", first_detection([(1.0, True), (3.0, False)], 10))
print("half light, in view:  ", first_detection([(1.0, True)], 10, light=0.5))
```

Output:

```
 0 m: fill 1.00 s
 5 m: fill 1.75 s
10 m: fill 2.50 s
15 m: fill 3.25 s
20 m: fill 4.00 s
stand in view at 10 m: 2.5
peek 1.5 s, hide 2 s:  8.2
peek 1.0 s, hide 3 s:  None
half light, in view:   5.0
```

### Numbers you can check

Break-even exposure with `F = 6 s`, in full light:

| Distance | Fill time `T` | Break-even `f* = T / (T + 6)` | Longest safe peek if you hide 3 s |
|---|---|---|---|
| 0 m | 1.00 s | 1 / 7 = 14.3% | 0.50 s |
| 5 m | 1.75 s | 1.75 / 7.75 = 22.6% | 0.88 s |
| 10 m | 2.50 s | 2.5 / 8.5 = 29.4% | 1.25 s |
| 15 m | 3.25 s | 3.25 / 9.25 = 35.1% | 1.63 s |
| 20 m | 4.00 s | 4 / 10 = 40.0% | 2.00 s |

The last column comes from `e / T = h / F`, so `e = h × T / F`. At 10 m with a 3 s hide, `e = 3 × 2.5 / 6 = 1.25 s`.

Now trace the two peeking runs at 10 m by hand, where `T = 2.5 s` and each second of sight adds 0.4.

**Peek 1 s, hide 3 s.** Each peek adds `1 / 2.5 = 0.4`. Each hide can remove `3 / 6 = 0.5`. The meter goes 0 → 0.4 → 0 → 0.4 → 0, forever. Exposure share is 25%, under the 29.4% break-even. Never detected.

**Peek 1.5 s, hide 2 s.** Each peek adds `0.6`. Each hide removes `2 / 6 = 0.333`. Exposure share is `1.5 / 3.5 = 42.9%`, over break-even. The meter:

| Moment | Meter |
|---|---|
| end of peek 1 (1.5 s) | 0.600 |
| end of hide 1 (3.5 s) | 0.267 |
| end of peek 2 (5.0 s) | 0.867 |
| end of hide 2 (7.0 s) | 0.533 |
| during peek 3 | needs 0.467 more, which takes `0.467 × 2.5 = 1.17 s` |

Detection comes at `7.0 + 1.17 = 8.17 s`. The code reports 8.2 because it works in whole 0.1 s ticks and the meter crosses 1 during the twelfth tick of the third peek.

Compare that with standing still in view at 10 m: 2.5 s. Peeking over the break-even line still gets you caught, but it takes more than three times as long, and every cycle the HUD shows you the meter climbing. That is the window Walsh describes, stretched over several attempts.

Half light doubles the fill time to 5 s and raises break-even at 10 m to `5 / 11 = 45.5%`. Light is a multiplier on the whole table, which is why stealth games make shadows the main resource.

### Move it yourself

Open [the interactive](../examples/w10-detection-meter.html). The left view is a top-down room with a guard, his vision cone and a player marker you can drag. The right view plots the meter against time, with the 0.5 and 1.0 lines drawn across it.

The first screen runs the 1.5 s peek, 2 s hide pattern at 10 m. Its exposure share, 42.9%, is over the 29.4% break-even, so the teeth step upward and the guard catches you at 8.2 s. Drag the forget-time slider down from 6 s. A shorter memory drains faster, so the break-even readout rises. Once `F` drops below about 3.3 s, break-even passes 42.9% and the same pattern is safe forever.

Now set the pattern to 1 s exposed and 3 s hidden. At `F = 6` the meter saws between 0 and 0.4 and never reaches the top line. Drag `F` up. Past `F = 7.5 s` the break-even readout falls below the pattern's 25% share, and the teeth start stepping upward. At `F = 10` each cycle adds 0.1 and the guard catches you at 25.0 s. Nothing about the guard's eyes changed. Only his memory did.

Then switch the model selector. "Instant" is the plain cone test. The meter jumps to 1 the first tick you are seen, and every peek is a detection. "Never forgets" sets `F` to infinity, so the meter only climbs and every pattern is caught eventually. "Reset on hide" drains to 0 instantly, so peeking is always safe. The fill-and-drain meter is the only one of the four where the player's timing matters, and the drain rate is where you set how much it matters.

### Cross-game recognition

**Crysis 2 and later CryENGINE 3 games, the Target Tracks Perception System.** Welsh describes each stimulus as an envelope borrowed from music synthesizers, with **attack, decay, sustain and release** phases. In the attack phase the perception value rises from 0 to a peak over a set time. While the stimulus stays valid it holds at a sustain level. When it stops, for sight usually because line of sight broke, the release phase lowers the value toward 0. The chapter's example configuration for primary vision uses an attack of 2, a peak of 100, sustain 1.0 and a release of 40, and defines three threat levels at 25%, 62.5% and 100% of the peak, named Interesting, Threatening and Aggressive. Peripheral vision uses a lower peak and a longer attack, so a target at the edge of view takes longer to identify.

Rewrite it in this week's form. Attack time is `T`. Release time is `F`. The threat levels are the meter's thresholds, with one extra rung. A release twenty times the attack means `f* = 2 / 42 ≈ 4.8%` for a target that stays in the primary view. This configuration is much less forgiving of peeking than our guard, and Welsh notes the matching design lever, that a longer visual attack gives the player more time to lean out and look or dash between covers. There is also one real difference. Crytek applies distance as a **multiplier on the value** (1 at 0 m falling linearly to 0 at 50 m) rather than stretching the time. In our meter, that would mean a distant target lowers the ceiling instead of slowing the climb. A designer choosing between the two is choosing whether far-away players are "slow to notice" or "never fully noticed".

**Splinter Cell Blacklist, vision shapes.** Walsh describes three shapes: a standard cone in front of the NPC where detection should be fast, a peripheral shape, and a long "coffin-shaped" box that widens like a cone and then narrows again with distance. The shape the player is in sets the timer's range. In our model, each shape is its own pair `T_near`, `T_far`. The coffin exists because a cone keeps widening, so a guard would eventually notice someone far away and far to the side. Walsh is also frank about the cost of any shape. One centimeter outside it, the guard never sees you. One centimeter inside, you are detected within a couple of seconds at most. The meter softens the time axis. It does not soften the space axis, and your shapes still need tuning by playtest.

**Mark of the Ninja (Klei Entertainment, 2012).** Miles lists the sight test as a chain: inside one of the agent's vision cones, the target lit by a light source (unless the agent has night vision), and no collision blocking the line from the agent's eyes. In our form, light is a gate, so `ℓ` is either 0 or 1. That fits a 2D game where the player can always see which areas are lit. A continuous `ℓ` would be harder to read in that art style, so Klei made it binary.

Three games, one model. Each keeps a per-target number that climbs while the target is sensed and falls when it is not, with thresholds that change the NPC's behavior. The differences are all in how `T`, `F`, the thresholds and the shapes are chosen.

### Eyes-open design judgment

- **The forget time is a difficulty knob.** A short `F` makes guards forgiving and peeking a strong tactic. A long `F` makes the whole level tense after one mistake. Compute `f*` for your common distances before a playtest, not after.
- **Show the meter, or show the guard.** Walsh lists good feedback as one of four requirements, with fairness, consistency and intelligence. A meter nobody can see feels like random detection. Blacklist shows it on the HUD. A game with no HUD needs animation and barks to show the same states: a head turn at 0.5, a weapon raised at 1.
- **Consistency beats realism.** Walsh warns that real humans vary in what they notice, and that NPCs must not. Use the same `T` and `F` every time for the same situation, and put the variety in animations and lines.
- **Mind the floor.** With `T_near = 1 s`, a player who steps out right in front of a guard gets one second. Week 1's reaction-time figures (about 0.2 s for a simple reaction, about 0.4 s when a decision is needed) say one second is enough to react. Drop `T_near` to 0.2 s and you have built the instant cone again.
- **Thresholds need a way down.** An NPC at `a = 0.5` investigates. If the meter hovers at 0.5, the guard flips between patrol and investigate every tick. Use two thresholds (enter suspicious at 0.5, leave only below 0.3) or commit to the investigate state for a minimum time. This is the same hysteresis you will use for threat in week 12.

## 3. Hearing: distance is a path, not a line

Sound is the second sense almost every game models. The naive rule is "an NPC hears a sound if it is within the sound's radius." It fails at the first wall.

Take a player running at `S = (0, 0)` whose footsteps have a 10 m radius. A guard stands at `G = (6, 0)` on the other side of a wall. The only gap in the wall is a doorway at `D = (3, 5)`.

- Straight-line distance: `|G − S| = 6 m`. Inside the radius. Heard.
- Path distance: `|D − S| + |G − D| = √(9 + 25) + √(9 + 25) = 5.83 + 5.83 = 11.66 m`. Outside the radius. Not heard.

The straight line lets guards hear through walls, which players read as cheating. Both games from this week's readings measure along a path instead. Mark of the Ninja builds a triangle mesh of all the empty space in a level, a "sound mesh", and runs A* from the sound to each guard's head; a guard with no path cannot hear the sound at all. Blacklist found a full path search too costly and too fragile. It used a graph of rooms joined by choke points (doors and windows), and summed the distances from the source to the nearest choke, from choke to choke, and from the last choke to the listener. Walsh calls it a rough approximation that proved accurate enough that the team never went back. That is week 3 and week 4 again. The nodes are rooms and doors, and the edge weights are distances.

### Fairness beats accuracy

Walsh reports a problem you will meet in every playtest. His creative director kept getting detected by guards he could not see, heard running footsteps from around a corner. The detections were correct. They felt unfair, because the player cannot pause and look around the corner. Walsh's conclusion is that what matters is what the player thinks the NPC can see and hear.

Blacklist's fix was specific. Guards that were off-screen, and far enough away that not hearing would be plausible, had their hearing radius halved for certain events. Walsh reports the game became more fun at once. They did not halve it for all off-screen guards, because a guard one step around a corner who fails to hear you sprinting looks broken when you round the corner.

In the example above, a 10 m footstep radius becomes 5 m for an off-screen guard. Treat that as a rule of the form `radius × (0.5 if off-screen and far else 1)`. It is a deliberate cheat in the player's favor. Week 1 said cheat in the player's favor as often as against them, and never where they can catch you. This is that rule applied to hearing.

## 4. Events, polling and cost

How does a guard find out a footstep happened? Two designs from CS102 week 10 apply.

**Polling.** Every tick, every guard loops over every possible stimulus and runs the pipeline. Simple, and cost grows with guards times stimuli.

**Events.** When something perceivable happens, the game creates a stim and hands it to a perception manager. The manager filters it cheaply before any guard does work. Welsh lists three filters in Crytek's system: agents subscribe only to stim types they care about, a stim is dropped for agents outside its radius, and types can be flagged hostile-only so that friendly agents' own footsteps are ignored. Mark of the Ninja goes further and drives the test from the stim's side. Each interest source finds the agents that can detect it. That turns out to be useful for groups, as week 11 will show.

Sight is the expensive case because it needs raycasts. Welsh gives the arithmetic. With 16 active agents, each can potentially see 15 others, which is up to `16 × 15 / 2 = 120` raycasts just to check agent-to-agent visibility, before the player is considered. Crytek's answers were to test only targets an agent cares about and to request raycasts **asynchronously**, getting the result a frame or two later. A 33 ms delay is invisible next to a 1 s fill time. That is one more argument for the meter. It hides latency that a one-frame boolean would expose.

Cost at MMO scale, thousands of mobs rather than sixteen guards, is a separate problem. [MMO404 week 12, AI at scale](../../MMO404-advanced-networked-simulation/lectures/w12-ai-at-scale.md) covers it, and week 14 of this course covers AI level of detail.

## 5. Memory: what the NPC keeps

When the meter is above zero but the target is no longer sensed, the NPC needs somewhere to go. The standard answer is a **last known position**: the target's position at the last tick it was sensed. A suspicious guard walks there and searches. An alert guard fires at it or flanks toward it. The player learns that breaking line of sight and moving is how to escape, because the guard hunts where you were.

Two design rules from Mark of the Ninja are worth copying.

- **One interest at a time, with priorities.** Each agent holds a single current interest. A new interest replaces it only if its priority is at least as high. Klei found that corpses, noises and several other types worked best at *equal* priority with newest-first. If you are examining a body and hear footsteps behind you, the footsteps should win. The final game had around 60 interest source types.
- **Merge repeats.** Running produces a stream of footsteps. Treating each as a new interest makes the guard twitch. Klei's fix was simple. If an incoming interest has the same sense, type and priority as the current one and is close to it, update the current interest's position and timers instead of replacing it.

Both are forms of the same principle as the meter. Perception should change an NPC's state smoothly and readably, not jump every time a stimulus arrives.

## In-class activity (25 minutes)

Pairs. Each pair gets a printed floor plan (a 20 m × 20 m warehouse with three shelving rows, two doors and one guard on a fixed post facing north) and the parameter card from section 2.

1. **Sight (8 min).** Mark five player positions along a route from the south door to the north door. For each, compute distance to the guard, fill time `T` in full light, and whether the position is inside a 30° half-angle cone.
2. **Peeking (7 min).** The route has one spot where the player must wait 6 s behind a shelf that hides them for 4 of every 6 seconds as the guard's gaze sweeps. At the distance of that spot, is the player ever detected? Compute `f*` and compare with `2 / 6`.
3. **Retune (7 min).** The level designer wants that spot to be tense but safe for a player who waits, and fatal for one who stands up. Choose `F` so that the 2-in-6 exposure is just under break-even. Write one sentence on what this does to every other spot on the map.
4. **Hearing (3 min).** The player drops a crate (radius 12 m) at the south door. Using straight-line distance, does the guard hear it? Using a path through the nearest door, does he?

Expected output: a five-row table, a yes/no with `f*`, one chosen `F` with the sentence, and two hearing answers.

## Common misconceptions

- **"If the NPC can see you, it knows you are there."** Seeing is a test. Knowing is a meter. Blacklist separates them on purpose, and the gap between them is where stealth gameplay lives.
- **"Longer fill times make stealth easier, full stop."** Fill time sets how long a single exposure is safe. Forget time sets whether repeated exposures add up. A guard with slow fill and very slow drain still catches a player who peeks too often.
- **"Hearing through walls is realistic, so it is fair."** Players judge by what they can see. Walsh's team halved some off-screen hearing radii because correct detections still felt unfair.
- **"Raycasting everyone every frame is the accurate approach."** It is the expensive approach. Order tests cheap-first, raycast only survivors, and let results arrive a frame late. The meter hides the delay.

## Check yourself

1. Using this week's parameters, how long does a player standing still in full view at 16 m take to fill a guard's meter? At the same distance in 25% light?
2. A guard uses `T = 2 s` at a certain distance. The designer wants a player who is exposed 1 s out of every 4 s to be safe forever, but a player exposed 1 s out of every 3 s to be caught eventually. Find the range of forget times `F` that does this.
3. In the Crytek-style configuration (attack 2 s, release 40 s), what is the break-even exposure? What does this suggest about how that system treats a player who peeks from cover every few seconds?
4. A sound with a 9 m radius is made at `(0, 0)`. A listener is at `(8, 0)` behind a wall whose only gap is at `(4, 3)`. Is the sound heard with straight-line distance? With path distance?
5. A colleague proposes removing the suspicious state and going straight from unaware to alert at `a = 1`. Name one of week 1's five tests this hurts, and explain why using the meter.

<details>
<summary>Answers</summary>

1. `T = 1 + 3 × 16 / 20 = 3.4 s` in full light. At 25% light, `3.4 / 0.25 = 13.6 s`.
2. Safe forever needs `f ≤ T / (T + F)`. With `f = 1/4`: `1/4 ≤ 2 / (2 + F)` gives `2 + F ≤ 8`, so `F ≤ 6`. Caught eventually needs `1/3 > 2 / (2 + F)`, so `2 + F > 6`, `F > 4`. Any `F` with `4 < F ≤ 6` works. Check `F = 5`: 1-in-4 gains 0.5 per peek and loses 0.6 per hide, safe; 1-in-3 gains 0.5 and loses 0.4, climbs.
3. `f* = 2 / (2 + 40) ≈ 4.8%`. Almost any peeking pattern adds up, because the value drains twenty times more slowly than it rises. Such a system relies on long attack times and cover, not on the player's rhythm, to give the player room.
4. Straight line: 8 m, heard. Path: `√(16 + 9) + √(16 + 9) = 5 + 5 = 10 m`, not heard.
5. "Readable" (or "beatable"). Without the intermediate state, the only visible change is at `a = 1`, when the guard attacks. The player gets no warning while the meter climbs through 0.5, so detection looks sudden, and the player cannot learn the timing. A head turn or bark at 0.5 is the telegraph.

</details>

## Lab / assignment hook

[Lab 10, the awareness meter](../labs/lab10.md). Implement the fill-and-drain meter, the suspicious and alert states with hysteresis, break-even exposure, and path-based hearing with the off-screen rule, until the provided checker passes. Then tune one guard for a given room so that a scripted peeking route is safe and a careless one is not. Deliverable: the passing code, a tuning table and a 300-word note.

## Sources

- Walsh, M. (2015). "Modeling Perception and Awareness in Tom Clancy's Splinter Cell Blacklist." In S. Rabin (ed.), *Game AI Pro 2*, chapter 28. CRC Press. Free at gameaipro.com. Splinter Cell Blacklist (2013): raycasts to eight bones with a stance-dependent count; a detection timer whose range is set by the vision shape and scaled linearly by distance; the HUD element as the player's window; the intermediate investigate state; cone, peripheral and coffin-shaped vision shapes (boxes in Splinter Cell Conviction); the 1 cm threshold remark; fairness, consistency, feedback and intelligence as goals; sound distance via rooms and choke points; halved hearing for some events from off-screen, distant NPCs.
- Welsh, R. (2013). "Crytek's Target Tracks Perception System." In S. Rabin (ed.), *Game AI Pro*, chapter 31. CRC Press. Free at gameaipro.com. Written for Crysis 2 by Kevin Kirst and used in CryENGINE 3 projects: stims and their filters; the 16-agent, 120-raycast example; deferred raycasts; ADSR envelopes; peripheral vision with lower peak and longer attack; example configuration with attack 2, peak 100, sustain 1.0, release 40 and threat levels at 0.25, 0.625 and 1; distance multiplier from 1 at 0 m to 0 at 50 m.
- Miles, B. (2013). "How to Catch a Ninja: NPC Awareness in a 2D Stealth Platformer." In S. Rabin (ed.), *Game AI Pro*, chapter 32. CRC Press. Free at gameaipro.com. Mark of the Ninja (Klei Entertainment, 2012): the sight test chain with the lit-or-night-vision condition; hearing by A* over a sound mesh; about 60 interest source types; one interest per agent, priorities with newest-first at equal priority; merging repeated footstep interests.
- Rabin, S. (2017). "The Illusion of Intelligence." In S. Rabin (ed.), *Game AI Pro 3*, chapter 1. Reaction times of about 0.2 s and 0.4 s, as cited in CS203 week 1.
- Millington, I. (2019). *AI for Games*, 3rd ed. CRC Press. Sense management.
- The detection parameters (`T_near = 1 s`, `T_far = 4 s`, `R = 20 m`, `F = 6 s`), the thresholds 0.5 and 1, the wall-and-doorway geometry and the warehouse activity are invented for teaching.

## Interactive spec: examples/w10-detection-meter.html

**The one insight:** a guard's forget time decides whether peeking adds up. With a fill-and-drain meter, a peeking pattern is safe exactly when its exposure share is at most `f* = T / (T + F)`; dragging `F` moves that line and the sawtooth either stays flat or climbs to detection. The "instant", "never forgets" and "reset on hide" models make the contrast obvious: in all three the player's timing stops mattering.

**Layout.** Two linked views, side by side at 1280 px, stacked at 390 px (map on top).

- **Left, "Room":** a 24 m × 24 m top-down room drawn at a fixed scale, guard at `(12, 4)` facing +y (down the screen is +y). Draw the vision cone (half-angle 30°, range 20 m) as a translucent wedge, with range rings at 5, 10, 15 and 20 m labelled. One rectangular cover block, 3 m × 1 m, centered at `(12, 14.5)`. The player is a draggable circle. When the player is inside the cone, in range, and not behind the cover block (segment from guard to player does not intersect the block), draw a line from guard to player and label it "sensed". A light-level shading control dims the room.
- **Right, "Awareness":** meter `a` from 0 to 1 against time, a scrolling 30 s window. Horizontal lines at 0.5 ("suspicious") and 1.0 ("alert"). Background bands shaded where the player was sensed. Readouts: distance `d`, fill time `T`, forget time `F`, break-even `f*` as a percentage, current exposure share of the auto-peek pattern, and "first detection at X s" or "never (safe)".

**Controls (keyboard accessible, labelled):**

1. Drag the player, or move with arrow keys (0.5 m per press) when the map has focus.
2. Light level slider `ℓ` from 0.1 to 1.0, step 0.05, default 1.0.
3. Forget time `F` slider from 1 to 40 s, step 0.5, default 6.
4. Auto-peek toggle with two number inputs, exposed seconds `e` (0.1 to 5, default 1.5) and hidden seconds `h` (0.1 to 10, default 2). When on, the player alternates between the current position (exposed) and "behind cover" (not sensed) on this schedule, and the meter runs from 0.
5. Model select: "Fill and drain" (default), "Instant" (a = 1 on the first sensed tick), "Never forgets" (F = ∞), "Reset on hide" (a = 0 on the first unsensed tick).
6. Play/Pause, Reset, speed (1×, 2×, 4×).

**Formulas.** Tick `Δt = 0.1 s`. `T(d, ℓ) = (1 + 3 × min(d, 20) / 20) / ℓ`. Sensed: `a ← min(1, a + Δt / T)`. Not sensed: `a ← max(0, a − Δt / F)`. Detection when `a ≥ 1 − 1e−9`. `f* = T / (T + F)`. Exposure share `e / (e + h)`. The state label reads "unaware" below 0.5, "suspicious" from 0.5, "alert" at 1; once alert, stay alert until Reset.

**Test values (must match `first_detection` in the lecture).**

- Fill times at `d` = 0, 5, 10, 15, 20 m (ℓ = 1): 1.00, 1.75, 2.50, 3.25, 4.00 s.
- Standing in view at 10 m: detected at 2.5 s. At 10 m with ℓ = 0.5: 5.0 s.
- Auto-peek at 10 m, `e = 1.5`, `h = 2`, `F = 6`: detected at 8.2 s; meter 0.600 at 1.5 s, 0.267 at 3.5 s, 0.867 at 5.0 s, 0.533 at 7.0 s.
- Auto-peek at 10 m, `e = 1`, `h = 3`, `F = 6`: never; meter peaks at 0.400 each cycle.
- Break-even at 10 m, `F = 6`: 29.4%. At 20 m: 40.0%. At 0 m: 14.3%.
- Same `e = 1`, `h = 3` pattern at 10 m with `F = 3.5`: exposure 25% vs `f* = 2.5 / 6 = 41.7%`, still safe; with `F = 10`: `f* = 20%`, detected (meter climbs by 0.1 per cycle).
- Check yourself 1: at 16 m, fill 3.4 s; at 25% light, 13.6 s.

**First screen.** Fill-and-drain model, player at `(12, 14)` (10 m in front of the guard) with auto-peek on at `e = 1.5`, `h = 2`, meter already running so the climbing sawtooth is visible with the "first detection at 8.2 s" readout. Caption: "Same guard, same eyes. His memory decides whether peeking works."

**Accessibility.** All controls reachable by Tab with visible focus. A live region announces state changes ("suspicious at 5.0 s", "alert at 8.2 s"). Respects `prefers-reduced-motion` (the plot updates in 1 s steps, no scrolling animation) and `prefers-color-scheme`. Palette from `templates/interactive-tokens.css`. No game art: a circle for the player, a triangle for the guard.

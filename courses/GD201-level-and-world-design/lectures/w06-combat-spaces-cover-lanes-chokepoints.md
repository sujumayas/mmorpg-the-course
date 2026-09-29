# GD201 · Week 06 — Combat spaces: cover, lanes, chokepoints

**Why this matters:** The geometry of a fight decides who wins it long before anyone fires. A doorway can let ten defenders beat thirty attackers, and a missing flank route can make a map one-sided for years. If you can put numbers on what a doorway, a wall or a third lane is worth, you can tune a combat space on paper instead of discovering its problems in a playtest.

**You will be able to:**
- Compute the outcome of an open-field fight with Lanchester's square law, and the attacker's cost to break a chokepoint of a given width.
- Derive the chokepoint cost formula `b D² / (2 a w)` and use it to compare the effect of defenders, width, cover and area damage.
- Convert a cover bonus into a change in kill rate and predict how cover and flanking change a fight.
- Design a three-lane layout and critique how it splits defenders and depends on rotation time.

**Before class:** Christopher Totten, *An Architectural Approach to Level Design* (2nd ed., CRC Press, 2019), chapter 6, the sections on prospect and refuge. The Level Design Book (book.leveldesignbook.com), the pages "Cover" and "Map balance," in the section on combat.

**Prerequisites from earlier courses:** [GD203 week 4, time-to-kill](../../GD203-combat-and-progression-design/lectures/w04-time-to-kill-and-time-to-die.md) (a kill rate is the inverse of time-to-kill). [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md) (hit chance times damage gives average damage). From this course, [week 4, landmarks and sightlines](w04-guiding-the-player-landmarks-light-weenies.md). Week 12 of this course returns to sightlines around spawn points.

**Interactive:** [`examples/w06-chokepoint-law.html`](../examples/w06-chokepoint-law.html). Keep it open during section 2.

---

## 1. Three tools for shaping a fight

A combat space is any area built for fighting. Level designers shape one with three main tools.

**Cover** is any object that blocks a sightline or shields someone from attack. The Level Design Book traces it back to Space Invaders (1978), whose destructible bunkers are cover. Kill Switch (2003) is generally recognized as the first shooter with a formal cover system, where the character snaps to an object and fights from it. Gears of War (2006) popularized that system and defined the modern cover shooter. Cover comes in two heights. **Half cover** (waist high) protects a crouching character and lets them shoot over it. **Full cover** (head high or more) protects completely but forces the character to step out to shoot.

A **lane** is a route between the two sides of a combat space, usually bounded by walls or terrain so that fighters in one lane can't easily shoot into another. Many competitive maps have three.

A **chokepoint** is a narrow place that fighters must pass through, typically with open space on either side. The Team Fortress 2 Wiki defines it as any enclosed space, corridor or area that large numbers of players are forced through with no alternate route. The key property of a chokepoint is its **width** `w`, the number of fighters who can pass through, or fight from it, at the same time.

The three tools interact. Cover changes how fast each side kills the other. Chokepoints change how many fighters can take part. Lanes decide how many chokepoints there are and how the defenders must split up to hold them. One model captures all three.

## 2. Worked example: the chokepoint law

### The hook

Alterac Valley is a large battleground in World of Warcraft, with up to 40 players on each team. Near the Horde's base, Frostwolf Keep has inner gates. Wowpedia's player-written tactical overview, written during patches 1.10 to 2.4 (2006 to 2008), calls those gates a very tight choke point that easily holds back greater numbers of Alliance players. Its note on the Alliance side makes the matching point from the other direction. A narrow approach corrals attackers and leaves them open to area attacks.

Players had learned this by losing at those gates. But "a choke point holds back greater numbers" is vague. How much greater? If ten defenders hold a gate, do the attackers need twelve, twenty, or fifty? And what happens if you widen the gate by one person? The numbers turn out to be larger than intuition suggests.

### The model, part 1: an open field

Start without a chokepoint. Define:

- `A` is the number of attackers alive, starting at `A₀`.
- `D` is the number of defenders alive, starting at `D₀`.
- `a` is the attacker **kill rate**, the number of enemies one attacker removes per second. If one attacker needs 10 seconds on average to kill one defender, then `a = 1/10 = 0.1`. That is the time-to-kill from GD203 week 4, inverted.
- `b` is the defender kill rate, defined the same way.

In an open field, everyone who is alive can shoot. Each second, the attackers remove `a × A` defenders and the defenders remove `b × D` attackers. The engineer Frederick Lanchester worked out in 1916 what this implies, and the Russian officer M. Osipov independently reached the same result. The fighting strength of each side is proportional to its kill rate times the **square** of its numbers. This is **Lanchester's square law**:

```
attackers win if  a × A₀²  >  b × D₀²
attackers left  = sqrt(A₀² − (b/a) × D₀²)
```

With equal fighters (`a = b = 0.1`), 30 attackers against 10 defenders is `900` against `100`. The attackers win with `sqrt(900 − 100) = 28.3` left. They lose fewer than two people. Numbers are squared because a bigger side both deals more damage and spreads the incoming damage over more bodies.

### The model, part 2: add a chokepoint

Now the defenders stand behind a gate that only `w` attackers can fight through at once. The defenders, spread in an arc on the far side, can all shoot at the gate. So:

- The attackers remove `a × w` defenders per second, as long as at least `w` attackers are alive to fill the gap.
- The defenders still remove `b × D` attackers per second.

The first line is the whole change. The attackers' killing speed no longer depends on how many of them there are. It depends only on the width of the gate.

You can now compute the attackers' losses without calculus. Defenders fall at a steady `a × w` per second, so `D` falls in a straight line from `D₀` to 0 over

```
T = D₀ / (a × w)   seconds.
```

During that time, the defenders kill `b × D` attackers per second. `D` falls in a straight line, so its average over the fight is `D₀ / 2`. The attackers' total loss is the defenders' average kill speed times the time:

```
attacker losses = b × (D₀ / 2) × T = b × D₀² / (2 × a × w)
```

Call this the **chokepoint law**. It holds while at least `w` attackers are alive, that is, when the attackers have at least `losses + w` fighters at the start. If they start with fewer, the last few seconds turn into an open-field fight among the survivors, and a simulation (below) handles that part.

Read the formula term by term. It is the whole lecture in one line.

- **`D₀²`.** Defenders still count squared. Double the defenders and the gate costs four times as much to break.
- **`w` in the denominator.** Halve the gate's width and the cost doubles.
- **`A₀` is missing.** The number of attackers doesn't appear. At a chokepoint, extra attackers don't fight faster. They only form a queue. Their numbers become a budget of bodies to spend, not a force multiplier.
- **`b / a`.** Anything that changes the kill-rate ratio, like cover, height or area damage, multiplies the cost directly.

### Numbers you can check

Take 30 attackers and 10 defenders, all equal fighters with a 10-second time-to-kill (`a = b = 0.1`).

| Situation | Attacker losses (formula) | Attackers left | Defenders left | Fight length |
|---|---|---|---|---|
| Open field | — | 28.3 | 0 | 3.5 s |
| Gate, `w = 10` | 5.0 | 25.0 | 0 | 10.0 s |
| Gate, `w = 4` | 12.5 | 17.5 | 0 | 25.0 s |
| Gate, `w = 2` | 25.0 | 5.0 | 0 | 50.0 s |
| Gate, `w = 1` | 50.0 (more than 30) | 0 | 6.4 | 36.7 s |

The open field costs the attackers under two fighters. A gate two wide costs them 25. A gate one wide wipes them out, and 6.4 defenders are still standing. The same 30 people against the same 10 people, and the only change is a wall with a gap in it. That is how ten defenders "easily hold back greater numbers."

The `w = 1` row is past the formula's limit, because the attackers run out before the defenders do. The simulation below computes it directly. Each tick is one thousandth of a second, fighters are allowed to be fractional (think of it as a fraction of total health), and the tick loop applies the two rates above. It prints the rows of the table.

```python
import math

def fight(attackers, defenders, a, b, width=None, dt=0.001):
    """Tick simulation. a, b: kills per second per fighter. width=None means open field."""
    t = 0.0
    while attackers > 1e-9 and defenders > 1e-9:
        firing = attackers if width is None else min(attackers, width)
        attackers, defenders = attackers - b * defenders * dt, defenders - a * firing * dt
        t += dt
    return max(attackers, 0.0), max(defenders, 0.0), t

A0, D0, a, b = 30, 10, 0.1, 0.1
print(f"open field: square law {math.sqrt(A0**2 - (b / a) * D0**2):.2f} attackers left")
for w in (1, 2, 4, 10):
    left_a, left_d, t = fight(A0, D0, a, b, width=w)
    print(f"width {w:>2}: closed form loses {b * D0**2 / (2 * a * w):5.1f} | "
          f"sim: {left_a:5.2f} attackers, {left_d:4.2f} defenders left after {t:5.1f} s")
```

It prints `open field: square law 28.28 attackers left`, then for widths 1, 2, 4 and 10 the losses 50.0, 25.0, 12.5 and 5.0 beside the simulated survivors: 0.00 attackers and 6.40 defenders after 36.7 s, then 5.00, 17.50 and 25.00 attackers left after 50.0, 25.0 and 10.0 s.

Two more rows to check by hand. Double the defenders to 20 at `w = 2`, and the losses become `0.1 × 400 / (2 × 0.1 × 2) = 100`. The gate now needs more than 100 attackers. And if the attackers want the `w = 2` gate to cost them only what the `w = 4` gate did, 12.5 fighters, they must thin the defenders first. Solve `D₀² / 4 = 12.5` to get `D₀ = 7.1`, so about three defenders must be picked off before the push.

### The visual

Open [`examples/w06-chokepoint-law.html`](../examples/w06-chokepoint-law.html). The left view is a top-down sketch of a gate with attackers queued on one side and defenders in an arc on the other. The right view plots both sides' numbers over time, with a second chart comparing the attackers' losses in the open field and at the gate.

Drag the gate width from 10 down to 1. On the left, the queue grows and only `w` attackers are ever engaged. On the right, the defender line becomes straight (a steady fall of `a × w` per second), the fight stretches out, and the attackers' loss bar climbs as `1/w`. Now drag the number of attackers from 30 to 60. The loss bar doesn't move. Only the queue gets longer. That is the missing `A₀` in the formula, made visible. Finally, drag defenders from 10 to 20 and watch the loss bar quadruple.

### Cross-game recognition

The same law appears whenever a space limits how many attackers can fight at once. What changes is which term the design touches.

**World of Warcraft, Alterac Valley (patches 1.10 to 2.4).** Frostwolf Keep's inner gates are a small `w`. The tactical overview's second observation, that a narrow approach leaves attackers open to area attacks, touches `b`, which the next case explains.

**Team Fortress 2, Dustbowl and payload maps.** The Team Fortress 2 wiki lists turns in payload tracks, the spaces between capture points and the corridors of maps like Dustbowl as common chokepoints. It notes that chokepoints invite explosive spam and area denial, and that the Soldier and Demoman gain the most there. Rewrite it in the model. An explosive that hits `k` bunched attackers at once multiplies the defenders' kill rate `b` by `k`. A chokepoint bunches attackers, so area damage raises the cost of the gate by the same factor `k`. Two targets per blast doubles the cost. In a wide-open field, attackers spread out and `k` falls back toward 1.

**XCOM: Enemy Unknown (2012) and XCOM 2 (2016).** Here the lever is the kill rate `a`. A shot's hit chance is the shooter's aim minus the target's defense, plus a range modifier. A rookie has 65 aim. Half cover gives +20 defense and full cover +40. So against a rookie, a target in half cover is hit 45% of the time and a target in full cover 25%, compared with 65% in the open. In model terms, full cover multiplies the attacker's kill rate by `25/65 = 0.38`, and the chokepoint cost by `65/25 = 2.6`. **Flanking**, shooting from a side where the cover doesn't block, ignores the cover bonus entirely, which restores `a`.

**Counter-Strike, de_cache.** The Level Design Book's page on map balance uses this map as its example. Each of three lanes (A, mid and B) ends in chokepoints, and it recommends three or four chokepoints across a map, one per lane, placed so that no single spot covers them all. Section 4 shows why that rule falls straight out of the `D²` term.

Four games and one line of algebra. When you meet a combat space, ask which term it changes: the defenders' numbers `D`, the width `w`, or the kill-rate ratio `b / a`.

### Eyes-open design judgment

The chokepoint law is a strong model of a specific situation, attrition through a gap. Use it knowingly.

- **A chokepoint is a stalemate generator.** Because cost grows with `D²/w`, a well-held narrow choke can make attacking pointless, and a match that stalls there stops being fun for both sides. Give attackers a way to change a term. Grenades or area damage reduce `D` before the push, a second route adds width, or a flank removes cover.
- **Numbers stop mattering at a choke, and players feel it.** The missing `A₀` means that bringing more players doesn't help. In an MMO battleground that can be good, because it lets smaller groups hold ground. It can also be deeply frustrating for the bigger side, who see their numbers wasted in a queue. Decide which feeling you want.
- **Area damage and chokepoints multiply.** If your game has strong area damage, every narrow space you build becomes much stronger for the defender than the width alone suggests. Measure `k` in playtests (how many targets a typical blast hits at the choke) and budget for it.
- **The model ignores movement and respawns.** Real fights have healing, respawning, retreats and pushes. Use the model to compare layouts and to find the order of magnitude, then playtest. It will not predict an exact score.
- **Width is a design knob, so write it down.** "The gate is narrow" is not a spec. "The gate lets two characters fight abreast" is, and you can check it with the character's collision width from week 13's metrics.

### Check yourself on the chokepoint

1. Eight defenders hold a gate two fighters wide. All fighters have a 10-second time-to-kill. How many attackers do the defenders kill before they fall, and how long does the fight last? Do 25 attackers win cleanly?
2. A designer wants a gate to be twice as costly to break without changing its width. By what factor must the number of defenders grow?
3. The defenders at a `w = 4` gate (30 attackers, 10 defenders, equal fighters) get half cover in XCOM terms (rookie aim 65, +20 defense). What are the attackers' losses now?

<details>
<summary>Answers</summary>

1. `a = b = 0.1`. Losses `= 0.1 × 64 / (2 × 0.1 × 2) = 16`. Fight length `T = 8 / (0.1 × 2) = 40` s. With 25 attackers, 9 are left, which is more than `w = 2`, so the formula holds and they win cleanly.
2. Cost grows with `D²`, so defenders must grow by `sqrt(2) = 1.41`, about 41% more.
3. Half cover multiplies the attackers' kill rate by `45/65`, so the cost is multiplied by `65/45 = 1.44`. Losses `= 12.5 × 1.44 = 18.1`, leaving about 11.9 attackers.

</details>

## 3. Cover in numbers

The XCOM translation generalizes. For any game, cover changes the attacker's expected damage per second by some factor `c` between 0 and 1. The factor can come from a lower hit chance (XCOM), from less of the body being exposed to hitscan weapons (most shooters), or from damage reduction. Whatever its source, cover multiplies the defender's staying power by `1/c` in both the open-field and the chokepoint formulas.

That gives you a way to compare cover types in a design document. If playtests show that players in half cover take about 60% of the damage they would take in the open, then `c = 0.6` and half cover is worth a 1.67× kill-rate advantage. You can then ask whether a spot with half cover and one approach is stronger than a spot in the open with three approaches. Section 4 answers exactly that kind of question.

Cover design has a few rules that follow from the model.

- **Every cover position needs a flank.** Flanking restores `a` (XCOM makes this explicit). A cover spot with no way to flank it has a permanent `1/c` advantage, and players will camp it. Place cover so that each position can be shot from at least one angle it doesn't protect.
- **Cover height sets the rhythm.** The Level Design Book distinguishes cover as a **maneuver** (you pass it while moving, as in Doom), a **tactic** (you duck behind it and pop out, as in Counter-Strike) and a **system** (being in cover is a distinct state, as in Gears of War). Half cover lets defenders shoot without moving and suits the tactic style. Full cover forces a peek, which creates a moment of exposure and suits the system style.
- **Prospect and refuge.** Totten's reading describes spaces where a player can see without being seen (a **refuge** with a view of a **prospect**, such as an open area). A good cover position is a refuge facing a prospect. The attacker's matching need is a route into that prospect that has refuges of its own. A prospect with no refuges for the attacker is a killing field. Sometimes you want one, but make it deliberate.
- **Destructible cover moves `c` over time.** XCOM's cover can be damaged or destroyed by explosives and some missed shots. A defender's advantage erodes as a fight goes on, which is one answer to the stalemate problem above.

## 4. Lanes: why three, and why rotation time matters

Suppose a map has one chokepoint, and 10 defenders hold it at `w = 2` with equal fighters. The cost to break it is `100 / 4 = 25` attackers. Now give the map three lanes, each with its own `w = 2` choke. The defenders don't know which lane the attack will come down, so they spread out, say 4, 3 and 3. The attackers pick the lane with 3 defenders. Its cost is `9 / 4 = 2.25` attackers. Splitting 10 defenders across three lanes cut the cost of the weakest lane by a factor of 11.

This is why the Level Design Book recommends one chokepoint per lane, three or four in all, placed so no one spot covers them all. The `D²` term punishes splitting. A defender team spread evenly over `n` lanes faces a cost per lane of about `1/n²` of the single-choke cost. Three lanes make each one about nine times cheaper to attack.

The defenders' answer is **rotation**. They leave a small watch in each lane and move the rest to whichever lane is attacked. Rotation creates a race. The defenders in the attacked lane must survive long enough for help to arrive. From section 2, a lane with `D` defenders at width `w` falls in `T = D / (a w)` seconds. The 3-defender lane at `w = 2` and `a = 0.1` falls in `3 / 0.2 = 15` seconds. If a rotation takes 20 seconds, the lane is lost before help arrives. If it takes 10 seconds, the defenders arrive in time and the fight becomes a much more expensive one.

Rotation time is walking distance divided by movement speed. Now the geometry of the whole map matters as well as the geometry of each choke. The de_cache example in the Level Design Book says exactly this. The defending team has a safe rotation from mid to A, while rotating away from B takes longer. Lane length, rotation routes and movement speed are all level-design decisions. Week 9 of this course turns walking speed into seconds between points of interest, and week 13 fixes the movement metrics you will use.

A good three-lane layout does these things.

- Each lane has a chokepoint, and no one position covers two chokes.
- The defenders' rotation routes are shorter than the attackers' routes between lanes, but not so short that defenders can hold every lane at full strength.
- At least one lane offers cover that suits each play style (close, mid and long range), so the lanes play differently rather than being three copies.

## 5. Combat spaces in persistent worlds

MMOs add three wrinkles to everything above.

**Scale.** A 40-player side is a large `A₀`, which the chokepoint law says is wasted at a narrow gate. That is why large battlegrounds tend to be built around several objectives spread over a large area, where numbers can be split and used. A single narrow choke between two 40-player sides tends to produce long, static fights.

**Mixed roles.** Healers effectively lower the opposing side's kill rate, and tanks absorb damage. Both enter the model as changes to `a` or `b`. A healer who restores health as fast as one attacker can remove it cancels that attacker in the model. A chokepoint makes healing more valuable, because the small number of engaged attackers means the healer only has to keep up with `w` of them.

**Shared PvE spaces.** Even without player-versus-player combat, the chokepoint law shows up. Groups fighting computer-controlled enemies often pull them back to a doorway or corridor so that only a few can reach the group at once. That is the group choosing a small `w` for the enemies. If you design a dungeon room, decide whether you want that tactic to work. If not, give enemies ranged attacks or alternate paths so a doorway doesn't neutralize them.

## In-class activity (25 minutes)

Work in groups of three with paper, the interactive and a greybox of any small arena.

1. **Measure the space (8 minutes).** On your arena, mark every chokepoint and estimate its width `w` in characters abreast. Mark every cover position as half or full, and draw one flank route for each.
2. **Price the chokes (10 minutes).** For a 6-versus-6 fight with a 10-second time-to-kill, compute the cost to break each choke if all six defenders hold it, then if the defenders split evenly across the chokes. Add half cover at your strongest choke with `c = 0.6`.
3. **Rotation race (7 minutes).** Measure the walking distance between the two farthest chokes, and assume a movement speed of 6 meters per second. Is a rotation faster than the time it takes one lane's split defenders to fall? Adjust one wall so the answer is "just barely."

Expected output: an annotated arena sketch, a table of choke costs (all-in and split), the rotation time against lane fall time, and your one wall change.

## Common misconceptions

- **"More attackers always help."** In the open field, yes, and quadratically. At a chokepoint, the number of attackers drops out of the kill-rate term. Extra attackers only lengthen the queue.
- **"A chokepoint twice as narrow is twice as good for the defender."** It doubles the cost only while the defender count stays fixed. Adding defenders is the stronger lever, because cost grows with their square.
- **"Cover is binary."** Cover is a multiplier on the enemy's kill rate. Half cover, full cover, partial exposure and destructible cover all sit on the same scale.
- **"Three lanes make a map fair."** Three lanes split defenders, which makes attacking easier, and they make rotation time decisive. Fairness depends on route lengths and cover in each lane, not on the count.

## Check yourself

1. In an open field, 20 attackers fight 12 defenders. Each defender kills twice as fast as each attacker. Who wins, and how many are left?
2. Twelve defenders hold a single `w = 3` gate with equal fighters and `a = b = 0.1`. The map designer adds two more lanes with `w = 3` gates, and the defenders spread 4, 4 and 4. What is the cost of attacking one lane? By what factor did it fall?
3. At the 4-defender lane from question 2, how long does the lane survive an attack? If rotation takes 12 seconds, do the reinforcements arrive in time?
4. A game's grenade hits an average of 2.5 attackers when thrown into a choke. How does that change the cost of breaking the choke? What layout change would reduce it?

<details>
<summary>Answers</summary>

1. Square law with `b = 2a`. Attackers' strength `a × 400`, defenders' `2a × 144 = 288a`. Attackers win with `sqrt(400 − 2 × 144) = sqrt(112) = 10.6` left.
2. One gate, all 12 defenders: `0.1 × 144 / (2 × 0.1 × 3) = 24`. One lane with 4 defenders: `16 / 6 = 2.67`. The cost fell by a factor of 9, which is `3²`.
3. `T = 4 / (0.1 × 3) = 13.3` seconds. A 12-second rotation arrives with 1.3 seconds to spare.
4. The defenders' kill rate `b` rises by a factor of 2.5 when attackers are bunched, so the cost rises by 2.5 as well. Widening the space in front of the choke, or adding a second entrance so attackers can spread out, lowers the number of targets per blast.

</details>

## Lab / assignment hook

[Lab 06, chokepoint simulator and three-lane arena](../labs/lab06.md). You build a tick simulator for open-field, chokepoint and multi-lane fights, confirm it against the closed forms, and use it to tune a three-lane greybox arena so that a coordinated attack on one lane succeeds only if the defenders rotate late. The arena feeds the blockouts assessment (40%).

## Sources

- Lanchester, F. W. (1916). *Aircraft in Warfare*. The square law, derived independently by M. Osipov during 1915 and 1916. Checked against Wikipedia, "Lanchester's laws."
- Wowpedia, "Alterac Valley tactical overview" (player-written; references patches 1.10 to 2.4, 2006 to 2008). Frostwolf Keep's inner gates described as a very tight choke point that holds back greater numbers; narrow approaches that leave attackers open to area attacks. Wowpedia, "Alterac Valley" (current), up to 40 players on each team.
- Team Fortress 2 Wiki, "Chokepoint" (current). Definition; chokepoints on payload turns, between control points and on Dustbowl; explosive spam and area denial; Soldier and Demoman advantages.
- XCOM Wiki (Fandom), "Cover" and "Aim (XCOM: Enemy Unknown)" for XCOM: Enemy Unknown (2012) and Enemy Within; "Cover (XCOM 2)" for XCOM 2 (2016). Chance to hit is aim minus defense plus a range modifier; rookie aim 65; half cover +20 and full cover +40 defense; flanking ignores the cover bonus; cover can be damaged or destroyed.
- The Level Design Book (Robert Yang and contributors, book.leveldesignbook.com, accessed September 2026). "Cover": Space Invaders (1978), Kill Switch (2003) as the first recognized cover shooter, Gears of War (2006) popularizing the cover system; cover as maneuver, tactic and system. "Map balance": three or four chokepoints, one per lane; the Counter-Strike map de_cache as an example, including its rotation asymmetry.
- Totten, C. W. (2019). *An Architectural Approach to Level Design* (2nd ed.). CRC Press. Chapter 6, "Prospect and Refuge Spatial Design."

## Interactive spec: examples/w06-chokepoint-law.html

**The one insight.** At a chokepoint, the attackers' losses are `b D² / (2 a w)`. They grow with the square of the defenders and with one over the width, and they don't depend on the number of attackers at all. More attackers only lengthen the queue.

**Layout.** Two linked views, map left and charts right on desktop, stacked on mobile with the map on top. Readout panel under both.

**View A, "The gate" (top-down).** A wall across the middle of the view with a gap `w` characters wide (draw character slots as small squares so the width is countable). Attackers are generic circles queued on the left in rows, with exactly `min(A, w)` of them in the gap, highlighted as "engaged." Defenders are generic diamonds in an arc on the right. In open-field mode, remove the wall and spread both sides in lines. During playback, remove shapes as their side's count drops by whole numbers (round the fractional count down for drawing). Draw a small shield icon next to defenders when cover is on (half or full) and a burst icon at the gap when splash `k > 1`.

**View B, charts.**
- Top chart, "Fighters alive": x-axis time 0 to the fight's end (auto), y-axis 0 to `max(A₀, D₀)`. Two lines, attackers and defenders, from the tick simulation. In chokepoint mode, overlay the closed-form defender line `D₀ − a_eff w t` as a dashed line.
- Bottom chart, "Attacker losses": two horizontal bars, "open field" (`A₀ − sqrt(A₀² − (b_eff/a_eff) D₀²)` or "all" if the attackers lose) and "gate" (closed form `b_eff D₀² / (2 a_eff w)`, with the simulated value printed beside it). Mark `A₀` on the axis so students see when losses exceed the whole force.

**Controls.**
- Attackers `A₀`: 1 to 100, step 1, default 30.
- Defenders `D₀`: 1 to 40, step 1, default 10.
- Attacker time-to-kill: 2 to 30 s, step 1, default 10 (so `a = 1/TTK`). Defender time-to-kill likewise, default 10.
- Mode: open field / chokepoint (default chokepoint).
- Gate width `w`: 1 to 12, step 1, default 2.
- Defender cover: none (`c = 1`), half (`c = 45/65`), full (`c = 25/65`), custom `c` slider 0.2 to 1, step 0.05.
- Splash targets per defender hit `k`: 1 to 4, step 0.5, default 1. Applies only in chokepoint mode.
- Lanes: 1 to 4 (default 1) with a defender split input (comma-separated, default even split rounded, must sum to `D₀`). When lanes > 1, the charts show the lane with the fewest defenders, and a readout shows its fall time `T = D_lane / (a_eff w)` next to a "rotation time" input (seconds, default 20) with "help arrives in time" or "lane falls first."
- Buttons: Play (animate the tick simulation over 3 seconds of real time), presets "Lecture (30 v 10, w = 2)", "Wide gate (w = 10)", "One-wide gate (w = 1)", "Double defenders", "Full cover", "Three lanes 4/3/3".

**Readouts (monospace).** `a_eff`, `b_eff`, closed-form losses and fight length `T = D₀ / (a_eff w)`, simulated attackers and defenders left and fight length, open-field square-law survivors, a validity note "formula valid (A₀ ≥ losses + w)" or "formula past its limit, see simulation."

**Exact formulas.**
- `a = 1 / attacker TTK`, `b = 1 / defender TTK`.
- `a_eff = a × c` (cover), `b_eff = b × k` (splash, chokepoint mode only).
- Open field: winner by `a_eff A₀²` vs `b_eff D₀²` (with `k = 1`); attacker survivors `sqrt(A₀² − (b_eff / a_eff) D₀²)` if positive.
- Chokepoint closed form: losses `b_eff D₀² / (2 a_eff w)`, `T = D₀ / (a_eff w)`.
- Tick simulation, `dt = 0.001` s: `firing = A` (open) or `min(A, w)` (gate); `A ← A − b_eff D dt`; `D ← D − a_eff firing dt`; stop when either side reaches 0.

**Test values (the build must reproduce these, equal fighters with TTK 10 s unless noted).**
- 30 v 10, open field: 28.28 attackers left, about 3.5 s.
- 30 v 10, gate `w = 10`: losses 5.0, 25.0 left, 10.0 s. `w = 4`: 12.5, 17.5 left, 25.0 s. `w = 2`: 25.0, 5.0 left, 50.0 s. `w = 1`: attackers wiped, 6.40 defenders left, 36.7 s.
- 20 defenders, `w = 2`: closed-form losses 100.
- 25 v 8, `w = 2`: losses 16, 9 left, 40 s.
- 30 v 10, `w = 4`, half cover: losses 18.06, 11.94 left, 36.1 s. Full cover: losses 32.5, attackers wiped.
- Three lanes 4/3/3, `w = 2`: cheapest lane cost 2.25, fall time 15 s; with rotation 20 s "lane falls first," with 10 s "help arrives in time."

**First screen.** The lecture preset (30 v 10, `w = 2`) with the fight already played, the defender line straight, and the loss bars showing about 1.7 (open) against 25 (gate). Caption: "Same 30 against the same 10. The wall costs the attackers 25 fighters instead of 2. Try adding attackers."

**Accessibility and motion.** All controls are native labeled inputs, keyboard reachable. Sides are distinguished by shape (circles and diamonds) as well as color. Under `prefers-reduced-motion`, Play jumps to the final state. Palette from `templates/interactive-tokens.css`, light and dark.

# CS203 · Week 06 — Finite state machines

**Why this matters:** Most NPCs you have ever fought were state machines: patrol, notice, chase, attack, search, give up. You already know how to build one. What you have not met yet is what happens when the inputs come from a noisy world instead of a keyboard. The player steps behind a pillar for a fifth of a second, two enemies take turns shooting the same monster, a distance hovers right at the attack range. A machine that answers every flicker looks broken to players, and the fix is a design decision about commitment, not a bug fix.

**You will be able to:**
- Write an NPC's behavior as a transition table with guards, priorities and minimum dwell times, and trace it tick by tick.
- Compute, for a retargeting rule with a commitment time `L` and a switch cost `T`, how often the NPC switches and what fraction of its time it spends attacking.
- Recognize commitment rules in shipped games (Doom, Metal Gear Solid, World of Warcraft) and rewrite each as a guard plus a timer or a margin.
- Critique an NPC state machine for dithering, unresponsiveness and transition growth, and say when to move to a behavior tree.

**Before class:** Graham, D. "Rez", "A Reusable, Light-Weight Finite-State Machine", *Game AI Pro 3* (2017), chapter 12 (free at gameaipro.com). Orkin, J., "Three States and a Plan: The A.I. of F.E.A.R.", Game Developers Conference 2006, pages 1-3. Millington, *AI for Games* (3rd ed., 2019), chapter 5, the section on state machines.

**Prerequisites from earlier courses:** [CS101 week 11, game state machines](../../CS101-programming-for-games-i/lectures/w11-game-state-machines.md) (states, events, enter and exit actions, Pac-Man's ghost modes). [CS102 week 11, the State pattern and state machines](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w11-state-and-state-machines.md) (guards, timers, hierarchical, pushdown and concurrent machines). [MA101 week 14, distances and ranges](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w14-distances-ranges-and-squared-distance.md) (the two-radius aggro and leash rule, which is hysteresis on distance). This lecture does not re-teach FSM basics; reread the CS102 notes if "guard" or "enter action" is unfamiliar.

**Interactive:** [`examples/w06-target-commitment.html`](../examples/w06-target-commitment.html). Keep it open during section 2.

---

## 1. An NPC is a state machine fed by a noisy world

In CS101 the inputs to your state machine were button presses: Start, Pause, Quit. They arrive rarely and mean exactly one thing. In CS102 you added guards and timers for a character the player controls. An NPC's machine is different in three ways.

- **Inputs are continuous and noisy.** "Can I see the player?" flips every time the player passes a pillar. "Is the player in range?" is a distance that wobbles around your threshold while the player strafes.
- **Nobody presses a button.** The machine is **polled**: the AI asks its questions every think tick (often 5 to 30 times a second, not every frame) and fires whichever transition's guard is true. Some inputs arrive as **events** instead (took damage, heard a noise), and the machine must handle both.
- **The player reads the state.** A guard who switches from "attack" to "search" and back in half a second looks stupid, even if each switch was locally correct. Every transition is visible behavior.

### A shipped example: Doom's monsters are data

Doom (1993) is a good place to see a real NPC machine, because id Software released its source code. Every monster's behavior is a table of states in `info.c`. Each state names a sprite frame, a duration in **tics** (Doom runs at 35 tics per second), an action function to call on entry, and the next state. Each monster type then names its entry states: where it spawns, where it goes on seeing the player, when hurt, when attacking, when dying.

Here is the zombieman (`MT_POSSESSED`) from the released source, `linuxdoom-1.10`:

| State | Tics | Action on entry | Next state |
|---|---|---|---|
| `S_POSS_STND` | 10 | `A_Look` (look for a player) | `S_POSS_STND2` |
| `S_POSS_STND2` | 10 | `A_Look` | `S_POSS_STND` |
| `S_POSS_RUN1` ... `RUN8` | 4 each | `A_Chase` (move, maybe attack) | next run frame, `RUN8` loops to `RUN1` |
| `S_POSS_ATK1` | 10 | `A_FaceTarget` | `S_POSS_ATK2` |
| `S_POSS_ATK2` | 8 | `A_PosAttack` (fire) | `S_POSS_ATK3` |
| `S_POSS_ATK3` | 8 | none | `S_POSS_RUN1` |
| `S_POSS_PAIN`, `PAIN2` | 3 each | `A_Pain` on the second | `S_POSS_RUN1` |

The loops are the "stand" and "run" behaviors, and the action functions are the guards. `A_Look` jumps to the see-state (`S_POSS_RUN1`) when it finds a target. `A_Chase` jumps to the missile state when an attack check passes. Taking damage can jump from any state to the pain state, with a per-monster chance (the zombieman's `painchance` is 200 out of 256). It is a state machine written as data, with the timing built into each state's tic count. You will meet the same idea, states and transitions as data a designer can edit, in every engine's animation and AI tools.

### The guard's transition table

For the rest of this lecture we use a guard with four states: PATROL, CHASE, ATTACK and SEARCH. Written as a table, with the first matching row winning:

| From | To | Guard | Notes |
|---|---|---|---|
| PATROL | CHASE | sees player | |
| CHASE | ATTACK | sees player and distance ≤ 2 m | |
| CHASE | SEARCH | player unseen | |
| ATTACK | SEARCH | player unseen | listed first: losing sight beats range |
| ATTACK | CHASE | distance > 2 m | |
| SEARCH | CHASE | sees player | |
| SEARCH | PATROL | searched long enough | |

Every guard here uses one threshold, and that is the problem this week is about. Lab 06 gives you exactly this table and three traces of player behavior. On the "strafe" trace, where the player circles at about 2 m and ducks behind a pillar for 0.2 s out of every 1.7 s, this table makes 127 transitions in 30 seconds and spends only 42% of its time attacking.

MA101 week 14 already fixed one version of this with **hysteresis**: two thresholds instead of one, so "start chasing at 10 m" and "give up at 30 m" leave a band where the current state decides. That handles a wobbling *distance*. It does not handle the case where the reasons to switch are real, distinct events that keep arriving, such as being shot by two different enemies. For that you need commitment in time.

## 2. Worked example: the monster that can't pick a target

### The hook

In Doom, monsters fight each other. If an imp's fireball hits a demon, the demon turns on the imp. Players learn to exploit this infighting, luring monsters into each other's line of fire. Look at how the source handles it and you find one number doing a lot of work.

When a monster takes damage from some source, `P_DamageMobj` in `p_inter.c` checks a counter called `threshold`. If it is zero, the monster makes the source its new target and sets `threshold = BASETHRESHOLD`, which is 100. While the counter is above zero, further damage from anyone else does not change the target. The counter drops by one each time the monster runs its chase routine `A_Chase`, and resets to zero if the target dies.

Put the numbers together. A zombieman's run states each last 4 tics and call `A_Chase` once, so 100 calls take at least 400 tics, or 400 / 35 = 11.4 seconds of chasing. A revenant's run states last 2 tics, so its lock is at least 200 tics, 5.7 seconds. Same constant, different commitment, because the timer counts think calls, not seconds. (The count only drops while the monster is chasing. Time spent attacking or in pain does not count, so the real lock lasts longer.)

Why would id bother? Imagine the demon without the counter, standing between the imp and you. Every fireball in its back and every bullet in its face would swing it around. It would spend the fight turning.

### The model

Strip the situation down to one NPC and two attackers, A and B, who take turns hitting it.

- The **retargeting rule**: switch to whoever hit you last.
- The **commitment time** `L`: after switching, ignore reasons to switch until you have held the current target for at least `L` seconds. This is Doom's threshold, in seconds instead of chase calls.
- The **switch cost** `T`: each switch spends `T` seconds turning and re-pathing, during which the NPC does not attack.
- The **gap** between reasons to switch. Here A hits at `t = 0, 1, 2, ...` seconds and B at `t = 0.5, 1.5, 2.5, ...`.

After a switch, the NPC ignores hits until `L` has passed, then switches on the next hit from the other attacker. Call the time between switches the **switch period** `P`. With this hit pattern, the next hit from the other attacker comes 0.5, 1.5, 2.5, ... seconds after a switch, so `P` is the first of those values that is at least `L`:

```
P = 0.5                   if L ≤ 0.5
P = ceil(L − 0.5) + 0.5   otherwise
fraction of time attacking = 1 − T / P   (and 0 if T ≥ P)
worst-case time before reacting to the other attacker ≈ P
```

The third line is the payoff. Every period, the NPC loses `T` seconds to the switch and attacks for the rest. The fourth line is the price. For up to `P` seconds, it ignores whoever is hitting it hardest right now.

### The code

This simulation runs the rule at 10 AI ticks per second for 1,000 seconds, long enough that the start-up does not matter, with `T = 0.6 s`.

```python
TICK = 0.1        # seconds per AI think
TURN = 6          # ticks spent turning and re-pathing after a switch (0.6 s)

def simulate(lock, hits, ticks):
    """Retarget to whoever hit us last, but only if we have held the
    current target for at least `lock` ticks. Returns (switches, attacking)."""
    target, held, turning = None, 0, 0
    switches = attacking = 0
    for t in range(ticks):
        for attacker in hits.get(t, []):
            if target is None:
                target, held = attacker, 0
            elif attacker != target and held >= lock:
                target, held, turning = attacker, 0, TURN
                switches += 1
        if turning > 0:
            turning -= 1          # still turning: no attack this tick
        elif target is not None:
            attacking += 1
        held += 1
    return switches, attacking

TICKS = 10_000                    # 1,000 seconds, long enough to hide start-up
hits = {}
for t in range(0, TICKS, 10):     # attacker A hits every 1.0 s from t = 0
    hits.setdefault(t, []).append("A")
for t in range(5, TICKS, 10):     # attacker B hits every 1.0 s from t = 0.5
    hits.setdefault(t, []).append("B")

print("lock (s)  switches/min  time attacking")
for lock in (0, 10, 20, 30, 60, 100):
    s, a = simulate(lock, hits, TICKS)
    per_min = s / (TICKS * TICK / 60)
    print(f"{lock * TICK:8.1f}  {per_min:12.1f}  {100 * a / TICKS:13.1f}%")
```

Output:

```
lock (s)  switches/min  time attacking
     0.0         119.9            0.1%
     1.0          40.0           60.0%
     2.0          23.9           76.1%
     3.0          17.1           82.9%
     6.0           9.2           90.8%
    10.0           5.7           94.3%
```

### Numbers you can check

Compute each row from the model, then compare with the simulation.

| L (s) | P (s) | Switches per minute = 60 / P | Attacking = 1 − 0.6 / P | Simulated | Worst reaction delay ≈ P |
|---|---|---|---|---|---|
| 0 | 0.5 | 120 | 0% (T > P) | 0.1% | 0.5 s |
| 1 | 1.5 | 40 | 60.0% | 60.0% | 1.5 s |
| 2 | 2.5 | 24 | 76.0% | 76.1% | 2.5 s |
| 3 | 3.5 | 17.1 | 82.9% | 82.9% | 3.5 s |
| 6 | 6.5 | 9.2 | 90.8% | 90.8% | 6.5 s |
| 10 | 10.5 | 5.7 | 94.3% | 94.3% | 10.5 s |

Look at the first row. With no commitment, the NPC switches every half second, and each switch costs 0.6 s. It never finishes turning. It is hit 120 times a minute and fires back almost never. That is the demon in the middle, and it is what players mean by "the AI is broken".

Look at the shape of the attack column. The first second of commitment buys 60 points. The next two buy 23 more. After that, each extra second buys less and less, while the reaction delay keeps growing one-for-one. The curve `1 − T/P` bends over hard. Most of the benefit arrives by `P ≈ 5T` (80% attacking), and past that you are mostly buying slowness.

### The visual

Open [`w06-target-commitment.html`](../examples/w06-target-commitment.html). The top panel is a timeline: A's hits as marks on one row, B's on another, and under them a strip showing the NPC's target (colored A or B) with the turning time hatched. The bottom panel plots attack fraction against `L`, with the model's curve `1 − T/P` and a dot for the current setting. Drag `L` from 0 to 3 seconds and watch the strip change from a hatched blur into long solid runs. Then drag `T` up to 1.5 s. The curve drops and the knee moves right: a slower-turning monster needs a longer commitment. Finally, switch B to "heavy hitter" (three times A's damage). A new readout shows damage taken from B while the NPC was locked on A. That number grows with `L`, and it is the reason you cannot just set `L` to 30 seconds.

### Cross-game recognition

**Doom (1993, released source `linuxdoom-1.10`).** Commitment in think calls: `threshold = 100`, decremented once per `A_Chase`. Rewritten in our form, `L = 100 × (tics per run state) / 35` seconds, at least. Zombieman 11.4 s, revenant 5.7 s. The switch rule is "whoever damaged me", and there are two extra lines in our table for the arch-vile. A damaged arch-vile ignores its own threshold and always turns on whoever hurt it, and damage dealt *by* an arch-vile never makes another monster retarget.

**Metal Gear Solid (1998) and Metal Gear Solid 2 (2001).** Enemy soldiers go through alert phases. Per the Metal Gear Wiki, in the first game, losing sight of Snake during Alert moves the guards to Evasion, and they return to normal only if he stays hidden until an on-screen counter reaches zero. Being spotted again sends them straight back to Alert. Metal Gear Solid 2 adds a Caution phase after Evasion, in which patrols stay more watchful. This is commitment on the way *out* of a state. The countdown is `L` for the SEARCH-to-PATROL transition, and the game shows it to the player, which turns the lock from a hidden rule into a readable one.

**World of Warcraft (classic era onward).** A monster switches to a new target only when that player's threat exceeds the current target's by 10% in melee range, or by 30% at range (Warcraft Wiki, "Threat"; in year 3, [MMO303 week 6](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w06-threat-aggro-and-control.md) derives the timing). That is commitment by **margin** instead of time. Doom asks "have I held this target long enough?" WoW asks "is the new reason big enough?" Both stop the monster from flipping on every small change. The margin version also scales with the fight: a 10% lead is a small number early and a large one late.

**MA101's aggro and leash radii.** Two distances, 10 m to start chasing and 30 m to give up, are commitment by margin applied to distance. The band plays the same role as WoW's 10% or Doom's 100 chase calls.

Four games or rules, one idea. A transition that fires on a noisy or frequently changing input needs a buffer, either in time (`L`) or in size (a margin or band), and the size of that buffer trades stability against responsiveness.

### Eyes-open design judgment

- **Pick `L` from `T`, not from taste.** If a switch costs `T`, commitment below `T` wastes most of the NPC's time, and commitment past about `5T` mostly adds delay. Measure `T` in your game (turn speed, re-path time, animation lock) before tuning `L`.
- **Time or margin?** A time lock is simple and predictable, and players can learn and exploit it (Doom players do). A margin lock ties behavior to what is happening in the fight, but players cannot see it without a threat meter, which is why WoW players use threat addons. If you want players to plan around the rule, show it: Metal Gear's countdown is the model.
- **Interrupts break commitment on purpose.** Some events should always win: the NPC is about to die, the player uses a taunt, a scripted moment starts. Mark those transitions as interrupts that ignore the lock. Doom's arch-vile exception is one. Keep the list short, or you are back to dithering.
- **Commitment has a cost players feel.** In the heavy-hitter setting of the interactive, a 6-second lock lets B deal six seconds of free damage. For a monster, that may be good design (the player can exploit it). For a companion NPC who ignores the enemy shooting the player, it reads as betrayal. Decide which side of that line each NPC is on.

## 3. Building the machine so it stays readable

### Guards, priorities and dwell in one table

Lab 06 uses one small engine for all of this. Each transition has a source, a destination, a guard function and an interrupt flag. Each state may have a minimum dwell time. Each tick the machine tries the current state's transitions in the order listed, fires the first whose guard is true and whose dwell has passed (or that is an interrupt), and runs exit then enter actions. The fixed guard table, after this lecture's ideas, looks like this:

| From | To | Guard | Idea used |
|---|---|---|---|
| PATROL | CHASE | sees player | |
| CHASE | ATTACK | sees player and distance ≤ 2 m | |
| CHASE | SEARCH | unseen for ≥ 0.5 s | commitment in time (grace period) |
| ATTACK | SEARCH | unseen for ≥ 0.5 s | commitment in time |
| ATTACK | CHASE | distance > 3 m | margin (band 2 to 3 m) |
| SEARCH | CHASE | sees player | |
| SEARCH | PATROL | in SEARCH for ≥ 5 s | Metal Gear's countdown |
| (dwell) ATTACK | | at least 1 s once entered | Doom's lock |

On the strafe trace this version makes 2 transitions instead of 127 and attacks 99% of the time. It still enters ATTACK on the tick the player first comes within 2 m on the approach trace. Responsiveness to the first real change is kept. Only the flicker is filtered.

### Transitions grow faster than states

A machine with `N` states can have up to `N(N − 1)` transitions. Four states allow 12, which is a table you can read. Ten allow 90. And each new state must be checked against every old one: can a stunned guard be taunted? Can a fleeing guard hear a noise? The number of questions grows with the square of the number of states.

CS102 week 11 showed the standard remedies. Hierarchical machines put shared transitions (death, stun) on a superstate so they are written once. Concurrent machines split independent concerns (movement and weapon) into separate small machines. Both help. Neither changes the basic fact that someone has to write every guard by hand.

Monolith's F.E.A.R. (2005) took a more radical approach. In his 2006 GDC paper, Jeff Orkin describes a character state machine with only three states, Goto, Animate and UseSmartObject, and argues that the last is really a data-driven version of Animate. All the decisions about which state to enter and with what parameters moved into a planner. His stated reason was that the combination and interaction of behaviors, not any single behavior, had become too complex to manage by hand. You will build that kind of planner in week 9 (GOAP). Next week's behavior trees are the more common middle path: keep hand-authored behavior, but organize it as a tree of reusable pieces instead of a web of transitions.

### Debugging the machine you cannot see

An NPC's state is invisible unless you make it visible. Three habits pay off every time.

- **Draw the state over the NPC's head** in debug builds, with the time in state. Most "the AI is dumb" reports become obvious within a minute of watching the labels.
- **Log transitions with the reason**: tick, from, to, and which guard fired with its inputs. `(412, ATTACK, CHASE, dist=3.1)` tells you the band is working. A log with 127 lines in 30 seconds tells you it is not.
- **Replay traces.** Record the inputs (sees, distance, damage events) for a few seconds of play and feed them back to the machine offline, as the lab's traces do. You can then change a guard and see the new behavior on exactly the same situation.

## In-class activity (25 minutes)

Groups of three. You are tuning a tower-defense enemy that retargets to the nearest tower whenever a closer one appears.

1. Each group gets a printed timeline of 20 seconds. Towers A and B alternate being nearest every 0.8 seconds as the enemy walks a zig-zag path. The enemy's turret turn costs `T = 0.5 s`.
2. With no commitment, count the switches and compute the fraction of time the turret is firing.
3. Choose a commitment time `L` that gets firing above 75%. Show the calculation with `P` and `1 − T/P`, using the fact that reasons to switch arrive every 0.8 s.
4. Now propose a margin rule instead ("switch only if the new tower is at least X m closer"). Describe one situation where your margin rule behaves better than your time rule, and one where it behaves worse.
5. One member from each group reads their `L` and margin aloud. The class compares.

Expected output: the switch count and firing fraction at `L = 0`, a chosen `L` with its calculation, and a margin rule with one strength and one weakness.

## Common misconceptions

- **"If each transition is correct, the machine is correct."** Each switch in the `L = 0` row is locally correct: the NPC always targets whoever hit it last. Together they produce an NPC that never attacks. Judge the machine by its behavior over time.
- **"Hysteresis and commitment are the same thing."** Hysteresis (a band on one input) stops wobble in a continuous value. It does nothing about a stream of separate, real reasons to switch, like hits from two attackers. For that you need a time lock or a margin between options.
- **"A longer lock is always safer."** Past about `5T`, a longer lock barely raises attack time and keeps adding reaction delay. The heavy-hitter case shows the damage it costs.
- **"FSMs are obsolete, use behavior trees."** Many shipped games ship with FSMs, and behavior trees often contain small state machines inside them. The question is how many transitions you are willing to maintain by hand, not which technique is modern.

## Check yourself

1. Two attackers alternate hits every 0.5 s, exactly as in the worked example. The NPC's switch cost is `T = 0.8 s`. What is the smallest whole-second `L` that keeps it attacking at least 75% of the time? What is its worst-case reaction delay?
2. A Doom mod adds a monster whose run states last 3 tics each. At minimum, how many seconds does its infighting lock last? Why is the true lock usually longer?
3. Rewrite World of Warcraft's melee rule as a guard in the lecture's table: from ATTACK(current target) to ATTACK(new target). What happens to the rule when the tank's threat is 0?
4. In the fixed guard table of section 3, suppose the player stands still at exactly 2.5 m. Which state is the guard in, and does it depend on history? Give both cases.
5. A designer adds a FLEE state to the four-state guard, reachable from every other state and able to return to CHASE or PATROL. How many transitions can the machine now have at most? How many new guards must be written if FLEE connects as described?

<details>
<summary>Answers</summary>

1. Need `1 − 0.8/P ≥ 0.75`, so `P ≥ 3.2 s`. The possible periods are 0.5, 1.5, 2.5, 3.5, ... so `P = 3.5`, which needs `L > 2.5`. The smallest whole second is `L = 3`. Attacking `1 − 0.8/3.5 = 77.1%`. Worst reaction delay about 3.5 s.
2. `100 × 3 / 35 = 8.6` seconds of chasing. The counter only drops during `A_Chase`, so time spent in attack and pain states adds to the real duration.
3. Guard: `threat(new) > 1.1 × threat(current)` and new is in melee range. If the current target has 0 threat, any positive threat exceeds it, so the monster switches immediately. A margin rule gives no commitment at zero. (That is one reason WoW taunts copy the top threat rather than relying on the margin.)
4. The band is 2 to 3 m. If the guard arrived from farther away, it is in CHASE: 2.5 m is not ≤ 2, so CHASE-to-ATTACK does not fire. If it was already attacking (the player backed off from 1.5 m to 2.5 m), it stays in ATTACK: 2.5 m is not > 3. Same input, two states, decided by history. That is hysteresis.
5. Five states allow `5 × 4 = 20` transitions. FLEE adds 4 incoming (from PATROL, CHASE, ATTACK, SEARCH) and 2 outgoing (to CHASE, PATROL): 6 new guards, taking the machine from 7 transitions to 13. A hierarchical machine could write the 4 incoming as one transition on a superstate.

</details>

## Lab / assignment hook

[Lab 06, a guard that commits](../labs/lab06.md). You finish a table-driven state machine engine (guards, priorities, dwell, interrupts, enter and exit hooks), then fix a designer's first-draft guard table so it passes four behavior traces: strafing at the edge of range, a straight approach, an escape, and a short juke out of melee. The checks in `check_lab06.py` fail on the starter and pass when you are done.

## Sources

- id Software, DOOM source code, `linuxdoom-1.10` (released 1997; GitHub id-Software/DOOM). `info.c`: zombieman and revenant state tables with tic counts and action functions; `info.h`: `state_t` fields; `p_local.h`: `BASETHRESHOLD 100`; `doomdef.h`: `TICRATE 35`; `p_inter.c` `P_DamageMobj`: pain chance, retarget and set threshold, arch-vile exceptions; `p_enemy.c` `A_Chase`: threshold decrement and reset. https://github.com/id-Software/DOOM
- Metal Gear Wiki (Fandom), "Enemy status". Normal, Alert and Evasion modes in Metal Gear Solid (1998), with the Evasion counter; Caution mode added in Metal Gear Solid 2: Sons of Liberty (2001).
- Warcraft Wiki, "Threat". Target switch when a unit exceeds the current target's threat by 10% in melee range or 30% outside it. The page is marked partly outdated; the rule is the long-standing one from the classic era.
- Orkin, J. (2006). "Three States and a Plan: The A.I. of F.E.A.R." Game Developers Conference 2006. The three-state FSM (Goto, Animate, UseSmartObject) and the move of transition logic into a planner.
- Graham, D. (2017). "A Reusable, Light-Weight Finite-State Machine." In S. Rabin (ed.), *Game AI Pro 3*, chapter 12. CRC Press. Free at gameaipro.com.
- Millington, I. (2019). *AI for Games*, 3rd ed., chapter 5. CRC Press.

## Interactive spec: examples/w06-target-commitment.html

**Purpose.** Make the stability-versus-responsiveness trade of a commitment lock visible and numeric.

**The one insight.** A short lock turns a dithering NPC into one that fights, and most of that gain comes early: attack fraction follows `1 − T/P`, which bends over fast, while the reaction delay keeps growing with `P`. The first screen, with `L = 0`, should show a timeline that is almost all hatched (turning), next to the number 0%. The student should then drag `L` and see the strip turn solid.

**Layout.** Two linked panels.
1. Timeline (top, full width): 20 seconds. Row "A hits": marks at the hit times. Row "B hits": marks. Row "Target": a strip colored A (steel) or B (ochre), with turning periods hatched in red. Vertical thin lines at each switch. Under the strip: "switches in 20 s: N", "attacking: X%".
2. Curve (bottom): x axis `L` from 0 to 10 s, y axis attack fraction 0 to 100%. Draw the model curve `max(0, 1 − T/P(L))` as a step curve (P jumps at L = 0.5, 1.5, 2.5, ...). A dot at the current `L` with the steady-state simulated value. A second y axis (right) or a second line for worst-case reaction delay ≈ P, in a muted color.

**Controls.**
- `L` commitment, 0 to 10 s, step 0.1, default 0.
- `T` switch cost, 0.1 to 1.5 s, step 0.1, default 0.6.
- Hit gap for each attacker, 0.5 to 3 s, step 0.1, default 1.0 for both; B's offset 0 to gap, default 0.5.
- Mode toggle: "Commit by time" (default) or "Commit by margin" (margin mode is a teaser: switch only if the new attacker's damage in the last 3 s exceeds the current target's by the margin slider, 0% to 100%, default 10%).
- "B is a heavy hitter" checkbox: B's hits deal 3 damage, A's deal 1. Adds readout "damage from B while locked on A".
- All controls keyboard operable; values shown next to sliders.

**Simulation (must match the lecture).** Tick = 0.1 s. Integer ticks throughout. Per tick: process hits in order A then B; if no target, take the hitter (held = 0); else if hitter ≠ target and held ≥ L_ticks, switch (held = 0, turning = T_ticks, switches += 1). Then if turning > 0, turning −= 1, else if target exists, attacking += 1. Then held += 1. The timeline panel shows the first 200 ticks. The dot on the curve uses 10,000 ticks.

**Test values (T = 0.6 s, gaps 1.0 s, B offset 0.5 s, 10,000 ticks).** L = 0: 0.1% attacking, 119.9 switches/min. L = 1: 60.0%, 40.0/min. L = 2: 76.1%, 23.9/min. L = 3: 82.9%, 17.1/min. L = 6: 90.8%, 9.2/min. L = 10: 94.3%, 5.7/min. Model curve at those L: 0%, 60.0%, 76.0%, 82.9%, 90.8%, 94.3%.

**Accessibility and motion.** Readouts in an `aria-live="polite"` region. No animation needed; the timeline redraws on input. Respect `prefers-reduced-motion` for any transitions. Hatch patterns must also differ by pattern, not only color.

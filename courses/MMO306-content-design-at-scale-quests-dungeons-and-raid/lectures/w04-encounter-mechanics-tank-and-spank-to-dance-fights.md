# MMO306 · Week 04 — Encounter Mechanics: Tank-and-Spank to Dance Fights

**Why this matters:** Every mechanic you add to a boss costs the raid damage, because players who are dodging, stacking or running are not attacking. If you add mechanics without paying for them somewhere else, the fight quietly turns into a gear check that the best players fail. If you pay for them on purpose, you can decide exactly what the enrage timer tests.

**You will be able to:**
- Compute a group's uptime from a list of mechanics and turn it into a kill time and a pass or fail against an enrage timer.
- Convert a mechanic into its "hidden health": the extra boss health it is worth for a given group.
- Design two encounters with the same enrage timer, one that tests gear and one that tests execution, and predict which of two groups clears each.
- Critique a boss design by naming what each mechanic costs (uptime, healing, attention or lives) and who pays it.

**Before class:** Schreiber & Romero, *Game Balance* (2021), the chapter on PvE balance and encounter pacing. Skim the Warcraft Wiki pages for Patchwerk and Heigan the Unclean (classic Naxxramas) listed in Sources.

**Prerequisites from earlier courses:** [GD203 week 4, time-to-kill and time-to-die](../../GD203-combat-and-progression-design/lectures/w04-time-to-kill-and-time-to-die.md) (why `H / DPS` is exact for long fights, and the Patchwerk DPS check). [MMO303 week 5, the holy trinity](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w05-the-holy-trinity-tank-healer-dps.md) (the damage, healing and spike checks, `H / T`). [MMO303 week 3, effective HP and effective DPS](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w03-effective-hp-and-effective-dps.md) (paper DPS versus what lands). [GD201 week 3, intensity graphs](../../GD201-level-and-world-design/lectures/w03-flow-pacing-and-intensity-graphs.md) (for the phase pacing in section 4). From this course, [week 3, dungeon design](w03-dungeon-design-trash-bosses-loot.md) (dungeon bosses).

**Interactive:** [`examples/w04-enrage-line.html`](../examples/w04-enrage-line.html). Keep it open during section 2.

---

## 1. What a mechanic is

A **boss encounter** is a fight against a scripted enemy that sets the group a set of tests. In MMO303 week 5 you met three of them as numbers: a damage check (deal `H` health before a deadline `T`), a healing check and a spike check. Those three are about stats. Gear and class tuning decide them.

A **mechanic** is any rule of the encounter that asks players to do something other than their normal rotation. "Move out of the fire." "Stand together when the marker appears." "Kill the add before it reaches the boss." "Interrupt this cast." Mechanics are the part of a fight that players learn, practise and talk about. They are also the part designers spend most of their time building.

Two words for the ends of the spectrum:

- A **tank-and-spank** fight has almost no mechanics. The tank holds the boss, the healers heal, the damage dealers run their rotation. Success depends on numbers the group brought into the room.
- A **dance fight** is dominated by movement mechanics. The name comes from players' description of the classic Naxxramas boss Heigan the Unclean, where the raid moves across the room in a fixed pattern to avoid eruptions from the floor.

Most bosses sit between the two. The question for this week is how to place a fight on that spectrum on purpose.

### Four things a mechanic can cost

Every mechanic spends one or more of four currencies. Naming the currency is the first step in tuning.

1. **Uptime.** The fraction of the fight a player spends doing their job. A damage dealer running out of a fire circle for three seconds deals no damage for those three seconds (unless their class can attack while moving). This is the currency the worked example is about.
2. **Healing.** A mechanic that deals damage to players who resolve it correctly (a "soak", where players share a hit by standing in it) spends healer throughput. MMO303 weeks 5 and 7 give you the tools for this one.
3. **Attention.** A mechanic that must be noticed spends the player's reaction budget. [GD101 week 12](../../GD101-introduction-to-game-design/lectures/w12-feedback-juice-clarity-readability.md) priced a single warning in milliseconds. Next week scales that up to a raid.
4. **Lives.** A mechanic that kills on failure spends the raid's margin for error. A dead player deals no damage for the rest of the fight, which turns into an uptime cost, as section 3 shows.

The **enrage timer** is the deadline `T`. A **hard enrage** kills the group at `T` (the boss gains a huge damage buff, or casts an unsurvivable spell). A **soft enrage** makes the fight steadily harder as time goes on, for example a stacking damage buff on the boss, until the healers can't keep up. MMO303 week 7 showed a third kind, the hidden enrage set by healer mana. This week uses hard enrages because they make the arithmetic clean, and the result carries over to the soft kind.

## 2. Worked example: the enrage line

### The hook

Classic World of Warcraft's Naxxramas (patch 1.12 era) put two famous bosses a few rooms apart.

Patchwerk has about 3,850,000 health and a 7-minute enrage. He has almost nothing to dodge. His signature attack, Hateful Strike, hits one of the high-health melee players every 1.2 seconds or so, and the healers keep them alive. The raid stands still and attacks. GD203 week 4 used him to show that `H / T` sets a raid's minimum DPS, about 9,170 here.

Heigan the Unclean has exactly 1,780,000 health. His fight runs on a 135-second cycle: 90 seconds with Heigan in the room, then 45 seconds on his platform while the floor erupts faster. The eruptions follow a fixed order across four zones, deal 3,500 to 4,500 unresistable nature damage to anyone standing in them, and the raid survives by moving from zone to zone in the right rhythm. The Warcraft Wiki lists no enrage timer for him.

Same raid, same gear, same players. One fight tests only the numbers the raid brought. The other tests only whether the raid can move together. Most bosses you design will be a mix, and the question is: **if a fight has both an enrage timer and mechanics, what is the timer actually testing?**

### The model

Plot the boss's health pool as a horizontal line at height `H`. Plot the raid's **cumulative damage** `D(t)`, the total damage dealt since the pull, as a line rising from zero. The raid wins if its line crosses the pool before the enrage time `T`.

With no mechanics, the line is straight:

```
D(t) = P × t
kill time  T_kill = H / P
pass if    T_kill ≤ T
```

- `H` is the boss's health.
- `P` is the raid's **paper DPS**: total damage per second when every player is attacking. It comes from gear and rotation.
- `T` is the enrage time in seconds.

Now add mechanics. Mechanic `j` happens every `c_j` seconds (its **cycle**) and costs each damage dealer `d_j` seconds of attacking (its **cost**). A group's **execution factor** `x` scales that cost: `x = 1` for a group that resolves each mechanic in the minimum time the design allows, `x = 1.6` for a group that takes 60% longer (hesitates, runs the long way, stops casting early). Averaged over the fight, the fraction of time spent attacking is the **uptime**:

```
tax  = Σ d_j / c_j          (the mechanic tax, a property of the fight)
u    = 1 − x × tax          (uptime, a property of fight and group together)
T_kill = H / (P × u)
required paper DPS  P_req = H / (u × T)
```

The mechanic line is no longer straight. It rises during attack windows and goes flat during each mechanic, and its average slope is `P × u`. The model assumes the mechanics don't overlap and that the fight covers many cycles. Section 3's simulation relaxes both.

One rearrangement is the whole lesson. Write the kill time as

```
T_kill = (H / u) / P
```

A fight with mechanics is a tank-and-spank fight against a boss with **hidden health** `H / u`. The hidden part, `H / u − H`, is what the mechanics are worth in boss health. And because `u` depends on `x`, **the hidden health is different for every group.**

### Numbers you can check

Two invented raids, both with 14 damage dealers.

- **Group A, "geared and sloppy":** paper DPS `P = 24,000`, execution `x = 1.6`.
- **Group B, "crisp":** paper DPS `P = 22,000`, execution `x = 1.0`.

Two invented bosses, both with a 300-second enrage.

- **Stitchgut**, a tank-and-spank: `H = 6,900,000`, no mechanics, tax 0.
- **Quakemaw**, a dance fight: `H = 5,000,000`. A spread mechanic every 20 seconds costs 2 seconds, and an eruption every 30 seconds costs 3 seconds. Tax `= 2/20 + 3/30 = 0.2`.

| Fight | Group | Uptime `u` | Effective DPS `P × u` | Kill time | Result |
|---|---|---|---|---|---|
| Stitchgut | A | 1.00 | 24,000 | 287.5 s | Pass, 12.5 s spare |
| Stitchgut | B | 1.00 | 22,000 | 313.6 s | Enrage |
| Quakemaw | A | 1 − 1.6 × 0.2 = 0.68 | 16,320 | 306.4 s | Enrage |
| Quakemaw | B | 1 − 1.0 × 0.2 = 0.80 | 17,600 | 284.1 s | Pass, 15.9 s spare |

Check one row by hand. Group A on Quakemaw: `u = 1 − 0.32 = 0.68`, effective DPS `24,000 × 0.68 = 16,320`, kill time `5,000,000 / 16,320 = 306.4` seconds. Six seconds too slow.

The same enrage timer, 300 seconds, tested gear on Stitchgut and execution on Quakemaw. Group A has 9% more paper DPS than group B, and it still loses Quakemaw by six seconds. In hidden-health terms, Quakemaw is a 6,250,000-health tank-and-spank for group B (`5,000,000 / 0.8`) and a 7,350,000-health one for group A (`5,000,000 / 0.68`). The mechanics added 1.25 million health for the crisp group and 2.35 million for the sloppy one.

Now fix the boss and vary the tax, to see how fast the requirement climbs. Quakemaw's 5,000,000 health and 300-second enrage, with `P_req = H / (u × T)`:

| Mechanic tax | `u` at `x = 1.0` | Required paper DPS at `x = 1.0` | `u` at `x = 1.6` | Required paper DPS at `x = 1.6` |
|---|---|---|---|---|
| 0.00 | 1.00 | 16,667 | 1.00 | 16,667 |
| 0.10 | 0.90 | 18,519 | 0.84 | 19,841 |
| 0.20 | 0.80 | 20,833 | 0.68 | 24,510 |
| 0.30 | 0.70 | 23,810 | 0.52 | 32,051 |

At zero tax the two groups face the same requirement. At a tax of 0.3 the sloppy group needs 35% more paper DPS than the crisp one for the same boss. The gap between the two right-hand columns is the part of the fight that tests execution. The designer sets it with one number, the tax.

### A visual you can move

Open [`examples/w04-enrage-line.html`](../examples/w04-enrage-line.html). The left view is the enrage line itself: time across, cumulative damage up, a horizontal band at the boss's health and a vertical wall at the enrage time. Each group's damage line rises in steps, flat during every mechanic. The right view plots required paper DPS against mechanic tax for both groups, with each group's actual paper DPS as a horizontal line.

Start on the Stitchgut preset. Group A's line crosses the health band first. Now drag the tax slider from 0 to 0.2 and lower health to 5,000,000 (the Quakemaw preset). Watch group A's line grow long flat steps and slide past the enrage wall, while group B's shorter steps still cross in time. On the right, the two required-DPS curves fan apart as the tax rises, and the point where group A's curve crosses its own DPS line is the tax at which A stops clearing. That fan is the one thing to take away: **mechanics don't make a fight harder evenly. They make it harder for the groups that execute worse.**

### Cross-game recognition

**World of Warcraft, classic Naxxramas (patch 1.12).** Patchwerk is the tax-zero corner: his fight is `H / T` and nothing else, which is why GD203 could use him as a clean DPS check. Heigan sits at the other corner. With no enrage timer, his fight has no damage line to cross at all. Everything the encounter tests is the dance. In this week's model, Heigan's check moved entirely from "can you deal `H` before `T`" to "can everyone survive the cycle", so his health matters only for how many cycles the raid must survive.

**Final Fantasy XIV, Savage raids (current design, Stormblood onward).** Each normal-difficulty raid boss has a Savage version that uses the same boss with more difficult mechanics, more health and higher damage, and every Savage boss has a time limit after which it wipes the party with an enrage ability. Rewrite that in this week's terms. Savage raises `H` (the damage line has further to go), raises the tax (the line is flatter for everyone) and keeps a hard `T`. So Savage tests gear and execution at once, and a group short on either fails the same way, by hitting the wall.

**Final Fantasy XIV, Ultimate raids.** The wiki's summary of Ultimate is that failing a mechanic usually means death or a severe Damage Down debuff. Both are the same thing in this model: a failed mechanic removes a share of `P` for the rest of the fight (death) or for the debuff's duration (Damage Down). Section 3 computes what one death costs, and it is usually far more than the seconds a mechanic takes. Ultimate also uses a strict item level sync, which fixes `P` for everyone. With gear fixed, the only way to move the line is `x`.

Three games, one picture: a line rising toward a health band, flattened by mechanics, racing a wall. When you meet a new boss, ask what flattens the line, by how much, and for whom.

### Eyes-open design judgment

- **Decide what the enrage tests, then tune `H` to match.** If you want a gear check, keep the tax low and the enrage tight. If you want an execution check, raise the tax and lower `H` so a crisp group at your target gear clears with a margin you choose. The mistake to avoid is adding mechanics to a boss that was tuned as a tank-and-spank. You then have a fight that only well-geared, well-executing groups clear, which is usually far fewer groups than you intended.
- **The tax isn't the same for every role.** Ranged casters in many games can't cast while moving, melee must follow a boss that moves, and some classes have instant attacks they can use on the run. A spread mechanic that costs a caster 3 seconds may cost a hunter 0. If your tax differs by class, your enrage check differs by class, and some specs will be invited less. Compute the tax per role, not per raid.
- **Hidden health rewards learning.** Because `x` falls as a group learns a fight, a dance fight gets easier week by week without any change in gear. That is a feature for progression content (players feel their own improvement) and a problem for content you want to stay hard. A tank-and-spank does not get easier with practice once the rotation is learned, so it only yields to gear.
- **Execution checks punish the slowest player, not the average one.** A group's `x` in practice is set by whoever resolves the mechanic last, because the boss often can't be attacked by the group until everyone is safe, or the healers must cover the late player. Next week turns this into numbers.
- **Tank-and-spank is not a failure of design.** A low-tax fight is a good first boss, a good gear gate and a relief between two hard fights. Patchwerk was a deliberate DPS check placed among movement-heavy bosses. Vary the tax across a raid so different groups shine on different bosses.

### Check yourself (worked example)

1. A boss has `H = 8,000,000` and `T = 360` s. Its mechanics: every 24 s, 3 s of lost attacking; every 40 s, 4 s. What is the tax? What paper DPS does a group with `x = 1.2` need?
2. Group A from the example learns Quakemaw and drops to `x = 1.3`. Does it clear now? By how many seconds?
3. A designer wants Quakemaw to be cleared by group A (`x = 1.6`) but not by group B. Is that possible by changing only `H`? Explain using hidden health.

<details>
<summary>Answers</summary>

1. Tax `= 3/24 + 4/40 = 0.125 + 0.1 = 0.225`. `u = 1 − 1.2 × 0.225 = 0.73`. `P_req = 8,000,000 / (0.73 × 360) ≈ 30,441`.
2. `u = 1 − 1.3 × 0.2 = 0.74`, effective DPS `24,000 × 0.74 = 17,760`, kill time `5,000,000 / 17,760 ≈ 281.5` s. It clears with about 18.5 s spare, slightly faster than group B.
3. No. At tax 0.2, group A's effective DPS is 16,320 and group B's is 17,600, so B kills any `H` faster than A. Changing `H` moves the health band for both lines equally. To make A clear and B fail you must lower the tax until A's effective DPS exceeds B's: `24,000 (1 − 1.6 tax) > 22,000 (1 − tax)`, which holds for `tax < 2,000 / 16,400 ≈ 0.122`.

</details>

## 3. Deaths, overlap and the real line

The average model is a planning estimate. A real fight differs from it in three ways, and each teaches you something about where to put mechanics.

**Mechanics that overlap cost less.** If a 2-second spread and a 3-second eruption happen at the same moment, players lose 3 seconds, not 5. Stacking mechanics on purpose trades a lower tax for a higher attention cost at one moment.

**The last cycle is partial.** The kill often lands in the middle of a cycle, so the fight's actual uptime near the end depends on where the mechanics fall. On short fights this shifts the kill time by several seconds. Boss logs in week 7 will show it.

**A death costs its share for the rest of the fight.** If one of 14 damage dealers dies, the raid loses about 1/14 of its paper DPS from that moment on. A player who dies 60 seconds into a 300-second fight costs about `240 × P × u / 14` damage. For group B that is `240 × 17,600 / 14 ≈ 302,000` damage, or 17 seconds of the whole raid's effective damage. Compare that with the 2 or 3 seconds the mechanic itself would have cost. **A failed mechanic is usually far more expensive than a resolved one.** That is why tuning a fight "with no deaths" and tuning it "with one death" give such different health values, and why the Ultimate design (failure means death or Damage Down) makes the enrage timer so unforgiving.

This short simulation steps through the fight in tenths of a second, with each mechanic given its first cast time so that they never overlap. It uses whole-number ticks to avoid rounding drift.

```python
def kill_time(H, P, mechanics, x=1.0, deaths=(), limit_s=600):
    """Step through the fight in tenths of a second. Return the kill time in seconds."""
    done = 0.0
    for tick in range(limit_s * 10):          # tick 0 covers 0.0-0.1 s
        busy = any(tick >= first * 10 and (tick - first * 10) % (every * 10) < x * cost * 10
                   for first, every, cost in mechanics)
        alive = 1 - sum(share for when, share in deaths if tick >= when * 10)
        if not busy:
            done += P * alive / 10
        if done >= H:
            return (tick + 1) / 10
    return None                               # enrage reached first

quakemaw = [(10, 20, 2), (15, 30, 3)]         # (first cast s, every s, costs s)
print(kill_time(5_000_000, 22_000, quakemaw, x=1.0))   # group B
print(kill_time(5_000_000, 24_000, quakemaw, x=1.6))   # group A
print(kill_time(5_000_000, 22_000, quakemaw, x=1.0, deaths=[(60, 1 / 14)]))
```

It prints:

```
282.3
305.4
301.1
```

The first two lines agree with the average model to within two seconds (284.1 and 306.4). The simulation is slightly faster because the first mechanics don't arrive until 10 and 15 seconds in. The third line is the lesson. Group B, the crisp group that cleared with 16 seconds to spare, hits the enrage after a single death at the one-minute mark. Its margin was real, but it was smaller than one mistake.

The interactive simulates a simpler schedule, one mechanic every 20 s costing `tax × 20` s, so its "simulated" column reads 283.3 s (B) and 304.4 s (A), a second off these numbers.

This gives you a tuning rule you can write into a design document: **state how many deaths a target group may suffer and still clear, and tune `H` to that number.** A first-week normal boss might allow two or three. A top-difficulty boss might allow none. Whatever you choose, choose it, because the difference between those two targets is several hundred thousand health.

## 4. Composing a fight from mechanics

Knowing the cost of mechanics lets you build a fight as a sequence of demands instead of a pile of ideas.

### A mechanic menu

Most MMO boss mechanics fall into a handful of families. The table names what each tests and what it spends. Use it to check that a boss isn't testing the same thing five ways.

| Family | Example instruction | Tests | Main currency spent |
|---|---|---|---|
| Avoid | "Move out of the circle" | Individual reaction | Uptime, lives on failure |
| Position | "Stand behind the boss", "face away" | Knowledge | Little, lives on failure |
| Spread | "Stay apart when marked" | Individual spacing | Uptime |
| Stack or soak | "Share the hit" | Group coordination | Healing, lives if too few soak |
| Add | "Kill the adds before they reach the boss" | Target switching | Boss damage (a target switch is a tax on boss DPS) |
| Interrupt | "Stop this cast" | Assignment and timing | Attention, small uptime |
| Tank swap | "Change tanks at 3 stacks" | Tank coordination | Tank attention, healing on failure |
| Burn | "Boss takes 50% more damage for 20 s" | Cooldown planning | Nothing: it gives damage back |

A burn window is a negative tax. It raises effective DPS for its duration and rewards groups that save cooldowns, so a high-tax fight can still reward gear and preparation.

### Phases and pacing

A **phase** is a section of the fight with its own set of mechanics, usually triggered by the boss's health (at 60%, the boss takes off) or by time. Phases let you vary the tax during the fight. Heigan's 90-and-45-second cycle is a two-phase fight: a low-intensity phase and a high-intensity one, repeated.

GD201 week 3 taught you to draw a level's intensity over time as an **intensity graph** and to shape it into rises and rests. A boss fight has the same kind of graph, and you can read intensity straight off this week's model: the local tax (how much of each minute is spent on mechanics) and the attention demand. Draw the fight's tax over time before you script it. A good boss graph usually has:

- **A teaching opening.** The first mechanic appears alone, at low tax, so the group learns it before it combines with anything else.
- **Rising combinations.** Later phases combine mechanics the group already knows. A new mechanic introduced at the peak of the fight is one the group will learn by wiping at 20% health, which is the most expensive place to learn anything.
- **A final phase that tests the whole fight.** Often with a soft enrage, so the damage line matters at the end even if it didn't before.

### Where the enrage goes

With phases, the enrage becomes a budget spent across the fight. If phase 1 has a tax of 0.1 and phase 2 a tax of 0.3, groups with spare DPS push through phase 1 fast to buy time for phase 2, and groups without it enter phase 2 already behind. If you want the last phase to decide the fight, compute how many seconds your target group has left when it enters that phase, and compare that with the time the phase needs at its tax.

## 5. Who pays: roles and the mechanic tax

The tax in section 2 was one number for the whole raid. In practice each role pays differently, and that decides who enjoys the fight.

- **Damage dealers** pay in uptime, as modelled.
- **Healers** pay in healing throughput when mechanics deal damage (soaks, raid-wide pulses) and in uptime when they must move. A healer who is moving and can't cast is a hole in the healing check from MMO303 week 5.
- **Tanks** pay in attention on swap mechanics and in survival on spike mechanics.

You can compute a per-role tax the same way: sum `d_j / c_j` over the mechanics that role must respond to. If one role's tax is much higher than the others', that role carries the fight. That can be deliberate (a boss that is "the healers' fight") but it should be a choice, and it should move from boss to boss so no role carries every fight.

A second consequence concerns the damage dealers themselves. Suppose a raid has melee and ranged damage dealers, and a boss moves every 30 seconds with 4 seconds of travel for melee and 0 for ranged. Melee tax from that mechanic is `4/30 ≈ 0.13`. If the ranged and melee specs are balanced on a stationary target dummy (MMO303 week 1's viability target), melee now brings 13% less to this boss. Across a whole raid of bosses with movement like this, raid leaders will bring more ranged players. The class balance team did nothing wrong. The content did it. Content design and class balance must share numbers.

## In-class activity (25 minutes)

In groups of three, design a boss for a 20-player raid with 14 damage dealers. Assume the target group has paper DPS 30,000 and execution `x = 1.2`.

1. (5 min) Choose three mechanics from the section 4 menu. For each, write the cycle `c`, the cost `d` for damage dealers, and one sentence on what it tests.
2. (5 min) Compute the tax, the target group's uptime and effective DPS.
3. (5 min) Choose an enrage time between 300 and 480 seconds. Set `H` so the target group clears with exactly one death allowed at the halfway point. Show your arithmetic (use section 3's rule: a death costs its share for the rest of the fight).
4. (10 min) Swap designs with another group. Find the execution factor at which the other group's boss becomes impossible for the target gear level, and the paper DPS at which it becomes a tank-and-spank for a group with `x = 2`.

Expected output: a half-page sheet with the mechanic table, tax, `H`, `T`, and the two numbers from step 4.

## Common misconceptions

- **"More mechanics make a fight harder for everyone equally."** They make it harder in proportion to `x`. A crisp group barely notices a mechanic that costs a sloppy group a full enrage's worth of damage. The fan of curves in the interactive is this misconception made visible.
- **"The enrage timer is a DPS check."** It checks effective DPS, `P × u`. How much of that is gear and how much is execution depends on the tax, which you choose.
- **"A mechanic costs the seconds it takes to resolve."** A resolved mechanic does. A failed one usually costs a death, and a death costs a share of the raid's damage for the rest of the fight, which is far larger.
- **"Tank-and-spank fights are lazy design."** They are the zero-tax corner of the design space. The problem is only a raid made entirely of them.

## Check yourself

1. A boss has 12,000,000 health and a 420-second enrage. Group C has paper DPS 36,000 and `x = 1.4`. The boss's mechanics: every 30 s, 3 s of lost attacking; every 45 s, 6 s. Does group C clear? What is its hidden health?
2. Same boss. Group D has paper DPS 45,000 and `x = 1.0`. Does it clear? If one of its 15 damage dealers dies at the 2-minute mark, when does the boss die now?
3. A designer halves the cycle of every mechanic on Quakemaw to make a "heroic" version and keeps `H` at 5,000,000. Which of groups A and B still clear? What `H` would restore group B's 284-second kill time?
4. On a boss where ranged players lose no uptime and melee lose 0.15, a spec that deals 10% more damage than a ranged spec on a target dummy is melee. On this boss, which contributes more? By how much?
5. Explain, using hidden health, why a dance fight gets easier each week a guild practises it even if nobody's gear improves.

<details>
<summary>Answers</summary>

1. Tax `= 3/30 + 6/45 = 0.1 + 0.133 = 0.233`. `u = 1 − 1.4 × 0.233 ≈ 0.673`. Effective DPS `36,000 × 0.673 ≈ 24,240`. Kill time `12,000,000 / 24,240 ≈ 495` s. Enrage. Hidden health `12,000,000 / 0.673 ≈ 17.8` million.
2. `u = 1 − 0.233 ≈ 0.767`, effective DPS `45,000 × 0.767 = 34,500`, kill time `12,000,000 / 34,500 ≈ 347.8` s, a clear with 72 s spare. With the death: by 120 s the raid has dealt `34,500 × 120 = 4,140,000`. The remaining 14 deal `34,500 × 14/15 = 32,200` per second, so the other 7,860,000 take about 244.1 s. The boss dies at about 364.1 s, 16 s later, still inside the enrage.
3. Halving each cycle doubles the tax to 0.4. Group A: `u = 1 − 0.64 = 0.36`, 8,640 DPS, 579 s, fails. Group B: `u = 0.6`, 13,200 DPS, 379 s, fails. To restore 284.1 s for group B: `H = 13,200 × 284.1 ≈ 3,750,000`.
4. Melee effective: `1.10 × (1 − 0.15) = 0.935` of the ranged spec's dummy damage. Ranged contributes more, by about 7% (`1 / 0.935 ≈ 1.07`).
5. Practice lowers `x`, which raises `u = 1 − x × tax`, which lowers the hidden health `H / u`. The boss's real health never changes, but the group faces a smaller effective pool each week.

</details>

## Lab / assignment hook

[Lab 04, the enrage line](../labs/lab04.md). You finish a Python encounter calculator (average model and tick simulation), then tune three bosses to three stated design goals: a pure gear check, an execution check that a lower-geared crisp group clears, and a fight that allows exactly one death. The encounter designs you produce here are the first entries in the course's encounter-design portfolio (40% of the grade).

## Sources

- Warcraft Wiki, "Patchwerk (Classic)" (40-player Naxxramas, patch 1.12). About 3,850,000 health, 7-minute berserk (the wiki also lists a later 7:30 Slime Bolt timer, which this lecture ignores) with about 9,500 raid DPS recommended, Hateful Strike roughly every 1.2 seconds on high-health melee. https://warcraft.wiki.gg/wiki/Patchwerk_(Classic)
- Warcraft Wiki, "Heigan the Unclean (Classic)" (40-player Naxxramas, patch 1.12). Exactly 1,780,000 health, 135-second cycle of 90 seconds in the room and 45 seconds on the platform, eruptions in a fixed four-zone order dealing 3,500 to 4,500 unresistable nature damage; no enrage timer listed. https://warcraft.wiki.gg/wiki/Heigan_the_Unclean_(Classic)
- Final Fantasy XIV Online Wiki (consolegameswiki), "Raids" (accessed September 2026, covering Stormblood through Dawntrail). Savage versions use the same boss with harder mechanics, more health and higher damage, and every Savage boss has an enrage time limit; in Ultimate raids a failed mechanic usually means death or Damage Down, and each Ultimate has a strict item level sync. https://ffxiv.consolegameswiki.com/wiki/Raids
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press.
- The bosses Stitchgut and Quakemaw, groups A and B, and all their numbers are invented for teaching.

## Interactive spec: examples/w04-enrage-line.html

**Purpose.** Make visible that an enrage timer tests effective DPS `P × u`, and that raising the mechanic tax separates groups by execution, not gear. The first screen must show the Quakemaw preset with group A's line hitting the enrage wall and group B's line crossing the health band before it.

**Model (exact).** For each group `g` in {A, B}: `u_g = max(0, 1 − x_g × tax)`. Average-model kill time `T_kill = H / (P_g × u_g)` (show "never" if `u_g = 0`). Required paper DPS curve `P_req(tax) = H / ((1 − x_g × tax) × T)` for `tax` where `1 − x_g × tax > 0.05`; stop drawing beyond.

For the left chart use the tick simulation from section 3, with the mechanic schedule generated from tax so the picture has visible steps: one mechanic with cycle `c = 20` s, first cast at 10 s, and base cost `d = tax × 20` s; the group's flat window is `x_g × d` seconds, clipped to at most 19.9 s. Ticks of 0.1 s. Optional death: if the "one death" toggle is on, group `g` loses share `1/14` of `P_g` from `t = 60` s onward. Simulate to `1.5 × T` at most.

**Left view, "The enrage line."** x axis time 0 to `1.5 × T`; y axis cumulative damage 0 to `1.3 × H`. Horizontal band at `H` (ochre, labelled "Boss health"). Vertical wall at `T` (blood red, labelled "Enrage"). Group A line in steel, group B line in moss, each a stepped line (flat during mechanics). Mark each crossing of `H` with a dot and label "A kills at 287.5 s" or "A: enrage". Draw each group's average-model line as a thin dashed line of slope `P × u` for comparison.

**Right view, "Required paper DPS vs mechanic tax."** x axis tax 0 to 0.4; y axis paper DPS 0 to 40,000. Two curves `P_req(tax)` for A (steel) and B (moss). Horizontal lines at each group's `P_g` in the same colours, dashed. A vertical cursor at the current tax. Where each curve crosses its group's `P_g` line, drop a marker labelled "A stops clearing at tax 0.X".

**Controls.** Sliders: boss health `H` 2,000,000 to 10,000,000 step 100,000; enrage `T` 180 to 600 s step 10; tax 0 to 0.4 step 0.01; `P_A` and `P_B` 10,000 to 40,000 step 500; `x_A` and `x_B` 1.0 to 2.0 step 0.05. Toggle "one death at 60 s". Preset buttons "Stitchgut" (H 6,900,000, T 300, tax 0) and "Quakemaw" (H 5,000,000, T 300, tax 0.2); both presets set `P_A = 24,000, x_A = 1.6, P_B = 22,000, x_B = 1.0`. All controls keyboard operable with visible labels and values.

**Readout table** (updates live). Rows A and B; columns `u`, effective DPS, hidden health `H / u`, average-model kill time, simulated kill time, result (Pass with seconds spare / Enrage).

**Test values.** Stitchgut: A `u = 1`, 24,000, 287.5 s pass; B 22,000, 313.6 s enrage. Quakemaw average model: A `u = 0.68`, 16,320, hidden health 7,352,941, 306.4 s enrage; B `u = 0.80`, 17,600, hidden health 6,250,000, 284.1 s pass. Right view at Quakemaw settings: A's curve crosses 24,000 at tax ≈ 0.19 (solve `5,000,000 / ((1 − 1.6 t) × 300) = 24,000`, `t = (1 − 0.6944) / 1.6 ≈ 0.191`); B's crosses 22,000 at tax ≈ 0.242 (`t = 1 − 0.7576 ≈ 0.242`). Simulated kill times at Quakemaw (one-mechanic schedule): B 283.3 s pass, A 304.4 s enrage, B with one death 301.1 s enrage. These differ by about 1 s from the two-mechanic code in section 3 (282.3 and 305.4), which is expected.

**The one insight.** Dragging tax up from 0 must visibly fan the two required-DPS curves apart and make the geared group's stepped line fall behind the crisp group's. Caption under the charts: "Same boss, same enrage. The mechanics decide whether it tests gear or execution."

**Style and accessibility.** Program tokens inline (steel, moss, ochre, blood). Lines distinguishable by dash pattern as well as colour (A solid with square markers, B solid with circle markers). Respect `prefers-reduced-motion` (no animated drawing) and `prefers-color-scheme`. Works at 390 px wide with the two charts stacked.

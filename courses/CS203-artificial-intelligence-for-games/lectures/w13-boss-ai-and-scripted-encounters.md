# CS203 · Week 13 — Boss AI and scripted encounters

**Why this matters:** A boss is the one enemy players study, rehearse and talk about afterwards, so its AI is mostly a script that has to hold up when players get stronger. The rule you choose for moving from one phase to the next decides which parts of your fight a well-geared group will ever see. Pick it by reflex and your best mechanic may vanish the week players get better gear.

**You will be able to:**
- Model a boss encounter as a phase state machine plus a per-phase ability timeline, and write it as data.
- Compute, for a given damage per second, how long each phase lasts and how many times each ability fires under HP-gated and time-gated phase rules.
- Derive the skip threshold of an ability, the damage per second at which its first cast never happens, and the minimum damage per second an enrage timer demands.
- Choose between HP gates, time gates and hybrid gates for a given design goal, and defend the choice with numbers.

**Before class:** Millington, *AI for Games* (3rd ed., 2019), chapter 5 "Decision making", the sections on state machines and hierarchical state machines. Reread your notes on telegraphs from GD101 week 12. Watch one full kill video of any raid or action-game boss with at least two phases, and write down the time at which each phase starts.

**Prerequisites from earlier courses:** [CS102 week 11, state and state machines](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w11-state-and-state-machines.md) (states, transitions and guards; this lecture uses them without re-teaching). [GD101 week 12, feedback and readability](../../GD101-introduction-to-game-design/lectures/w12-feedback-juice-clarity-readability.md) (how long a telegraph must be to be fair). [CS203 week 6, finite state machines](w06-finite-state-machines.md) and [CS203 week 12, MMO mob AI](w12-mmo-mob-ai-leashing-aggro-threat-tables.md). Week 12 decides *who* the boss hits. This week decides *what* the boss does and *when*. If you take GD203 alongside this course, its [week 4 on time-to-kill](../../GD203-combat-and-progression-design/lectures/w04-time-to-kill-and-time-to-die.md) and [week 10 on enemy design](../../GD203-combat-and-progression-design/lectures/w10-enemy-design-by-the-numbers.md) look at fight length from the designer's side; this lecture defines everything it uses.

**Interactive:** [`examples/w13-phase-gates.html`](../examples/w13-phase-gates.html). Keep it open during section 2.

---

## 1. What makes a boss different from a mob

The mobs of weeks 10 to 12 react. They perceive a player, pick a target, chase and attack. A good mob is readable because its rules are simple and the same every time.

A boss is built the other way round. Players fight it dozens of times, often as a group of 5 to 40, and the fight is meant to be learned. Learning needs something stable to learn. So most boss AI is not a decision maker at all. It is a **script**, a list of what the boss does and when, with just enough reaction to the players to feel alive.

Three pieces make up nearly every scripted encounter.

1. **Phases.** A **phase** is a section of the fight with its own set of abilities, and often its own arena layout or music. The boss moves between phases through **transitions**, which are the edges of a state machine. You met this structure in CS102 week 11 and built general versions of it in [CS203 week 6](w06-finite-state-machines.md).
2. **Timelines.** Inside a phase, abilities fire on a schedule. The simplest schedule gives each ability a **first cast** time and a **period**: cast at `first`, `first + period`, `first + 2 × period`, and so on, counted from the start of the phase. That is a timeline, and it is the reason add-ons such as Deadly Boss Mods can draw countdown bars for World of Warcraft bosses. The script is regular enough to predict.
3. **Global clocks.** An **enrage timer** is a clock that runs from the pull (the moment the fight starts). When it expires, the boss becomes far stronger and the group almost always dies. Designers call it a **DPS check**, because it sets the minimum damage per second (DPS) the group must deal.

The interesting design question sits in piece 1. What fires a transition? There are two main answers.

- An **HP gate** moves the boss to the next phase when its health drops below a threshold, such as 65%.
- A **time gate** moves the boss to the next phase when a clock reaches a value, such as 3 minutes after the pull.

Both look reasonable on paper. They behave very differently once players get stronger, and that difference is this week's worked example.

## 2. Worked example: the phase that faster raids never see

### The hook

Two bosses from the same raid tier of classic World of Warcraft (2004 to 2006) use opposite rules.

Onyxia, in the level-60 version of Onyxia's Lair, is HP-gated. The Warcraft Wiki's classic tactics page puts the transitions at 65% and 40% health. Between them, Onyxia flies above the room, throws fireballs and breathes fire across the floor, and whelps pour out of the eggs along the walls. When she reaches 40% she lands and adds an area fear.

Ragnaros, the last boss of Molten Core, is time-gated. The Warcraft Wiki records that after 3 minutes of combat he summons 8 Sons of Flame and submerges. He comes back after 90 seconds, or earlier if the players kill all eight adds. His health never triggers a phase.

So here is the puzzle. A group that deals twice as much damage spends half as long dodging Onyxia's air phase. A group that deals twice as much damage to Ragnaros still waits exactly 3 minutes for his submerge, and may kill him before it ever happens. Which boss did the designer actually control? And which of their mechanics will a strong group never see?

### The model

Describe a boss with total health `H` and a list of phases. Phase `i` covers `H_i` points of health, so the `H_i` add up to `H`. Each phase has abilities, and each ability has a first cast `a` and a period `p` in seconds, counted from the start of its phase. The group deals a constant `D` damage per second. That is a simplification, and section 3 returns to it.

**HP-gated phases.** Phase `i` ends when the group has dealt its `H_i` damage, so it lasts

```
t_i = H_i / D
```

An ability with first cast `a` and period `p` fires at `a`, `a + p`, `a + 2p`, ... and a cast counts only if it happens before the phase ends. The number of casts is

```
n = number of k ≥ 0 with a + k × p < t_i
  = 0                          if a ≥ t_i
  = floor((t_i − a) / p) + 1   when (t_i − a) / p is not a whole number
```

The first cast is lost entirely when `a ≥ H_i / D`. Rearranged, that gives the **skip threshold** of the ability:

```
D_skip = H_i / a
```

At or above `D_skip`, the phase is over before the ability's first cast. The players never see it.

**Time-gated phases.** Phase `i` starts at a fixed time `s_i` and lasts a fixed `T_i` seconds, except the last phase, which runs until the fight ends. The abilities fire at `s_i + a`, `s_i + a + p`, ... as long as they are inside the phase window. But the fight ends when the boss dies, at `H / D`, whatever phase it is in. A cast counts only if it happens before the kill. Here high DPS does not shorten phases. It deletes the phases at the end.

**Enrage.** With an enrage timer at `E` seconds, the group must kill the boss before `E`:

```
D_min = H / E
```

Every symbol, once more. `H` is boss health, `H_i` the health covered by phase `i`, `D` the group's DPS, `t_i` the length of an HP-gated phase, `s_i` and `T_i` the start and length of a time-gated phase, `a` and `p` an ability's first cast and period, and `E` the enrage time.

### A boss to test it on

We will use an invented boss, the Warden, so every number is ours to check. The Warden has `H = 600,000` and an enrage at `E = 360` s. It was designed for a group dealing 2,000 DPS, which gives a 300 s fight.

| Phase | HP range | `H_i` | Length at 2,000 DPS | Ability | First cast `a` | Period `p` |
|---|---|---|---|---|---|---|
| P1, ground | 100% to 60% | 240,000 | 120 s | Summon adds | 20 s | 45 s |
| P2, sky | 60% to 30% | 180,000 | 90 s | Meteor | 40 s | 40 s |
| P3, burn | 30% to 0% | 180,000 | 90 s | Firestorm | 15 s | 25 s |

Meteor is the fight's signature mechanic. It is the one the art team built a sky phase for, the one on the trailer.

For the time-gated version, the designer takes the lengths at design DPS and fixes them: P1 runs from 0 to 120 s, P2 from 120 to 210 s, P3 from 210 s until the kill.

### The code

This program computes the number of casts of each ability under both rules. It uses whole numbers only. A cast at time `t` inside a phase happens if `t < H_i / D`, which is the same as `t × D < H_i`, so no division and no floating-point edge cases. Both functions also stop at the enrage, since a cast after 360 s never happens either.

```python
HP = 600_000                        # the Warden's health
ENRAGE = 360                        # seconds from the pull
PHASES = [                          # (name, HP the phase covers, seconds at design DPS, ability)
    ("P1", 240_000, 120, ("Summon adds", 20, 45)),
    ("P2", 180_000,  90, ("Meteor",      40, 40)),
    ("P3", 180_000,  90, ("Firestorm",   15, 25)),
]

def hp_gated(dps):
    """Phase i ends when its HP is gone. Timers restart at each phase."""
    counts, done = [], 0                    # done: HP dealt before this phase began
    for _, phase_hp, _, (_, first, period) in PHASES:
        n, t = 0, first
        while t * dps < phase_hp and done + t * dps < ENRAGE * dps:
            n, t = n + 1, t + period        # before the phase's HP is gone and before the enrage
        counts.append(n)
        done += phase_hp
    return counts

def time_gated(dps):
    """Phase i starts at a fixed time; the last phase runs until the fight ends.
    Every cast must land before the kill (t * dps < HP) and before the enrage."""
    counts, start = [], 0
    for i, (_, _, seconds, (_, first, period)) in enumerate(PHASES):
        end = start + seconds if i < len(PHASES) - 1 else ENRAGE   # P3 is open-ended
        n, t = 0, start + first
        while t < end and t < ENRAGE and t * dps < HP:
            n, t = n + 1, t + period
        counts.append(n)
        start += seconds
    return counts

print(f"minimum DPS to beat the enrage: {HP / ENRAGE:,.1f}")
print(f"{'DPS':>6} {'kill (s)':>9}   HP-gated   time-gated")
for dps in (2_000, 3_200, 4_400, 4_600, 6_000):
    print(f"{dps:>6,} {HP / dps:>9.1f}   {str(hp_gated(dps)):>9}   {str(time_gated(dps)):>9}")
```

Output:

```
minimum DPS to beat the enrage: 1,666.7
   DPS  kill (s)   HP-gated   time-gated
 2,000     300.0   [3, 2, 3]   [3, 2, 3]
 3,200     187.5   [2, 1, 2]   [3, 1, 0]
 4,400     136.4   [1, 1, 2]   [3, 0, 0]
 4,600     130.4   [1, 0, 1]   [3, 0, 0]
 6,000     100.0   [1, 0, 1]   [2, 0, 0]
```

Each list is `[Summon adds, Meteor, Firestorm]`.

### Numbers you can check

Work the 4,400 and 4,600 rows by hand for the HP-gated boss.

| Quantity | 4,400 DPS | 4,600 DPS |
|---|---|---|
| P1 length `240,000 / D` | 54.5 s | 52.2 s |
| Summon adds at 20, 65, ... | 20 only: 1 cast | 20 only: 1 cast |
| P2 length `180,000 / D` | 40.9 s | 39.1 s |
| Meteor at 40, 80, ... | 40 < 40.9: 1 cast | 40 > 39.1: 0 casts |
| P3 length `180,000 / D` | 40.9 s | 39.1 s |
| Firestorm at 15, 40, 65, ... | 15 and 40: 2 casts | 15 only: 1 cast |
| Total mechanics seen | 4 | 2 |

A group that is 4.5% stronger sees half as many mechanics, and loses the signature one completely. The skip threshold says exactly where the cliff is: `D_skip = H_i / a = 180,000 / 40 = 4,500` DPS for Meteor. Firestorm's second cast falls at 40 s into P3, which has the same `H_i`, so it disappears at the same 4,500 DPS. Summon's second cast, at 65 s into P1, goes at `240,000 / 65 = 3,692` DPS.

Now the time-gated boss at 4,400 DPS. The kill comes at `600,000 / 4,400 = 136.4` s. P1 runs its full 120 s, so Summon fires three times, at 20, 65 and 110 s. P2 starts at 120 s and Meteor would first fire at 160 s, after the kill. P3 never starts. The time-gated boss shows the group every one of P1's casts and nothing else.

Both designs agree exactly at the design DPS of 2,000. That is not luck. The time gates were copied from the HP-gated lengths at that DPS. They only disagree about what a *faster* group skips.

- The **HP-gated** Warden keeps every phase but shrinks each one. Stronger groups see every phase and fewer casts in each, and whole abilities vanish at their skip thresholds.
- The **time-gated** Warden keeps every phase the same length but ends early. Stronger groups see the opening in full and never reach the end.

### The visual

Open [`w13-phase-gates.html`](../examples/w13-phase-gates.html). It shows the Warden twice, one timeline above the other, with a shared DPS slider. The top timeline is HP-gated. Its phase bands stretch and shrink as you drag, and each cast is a tick mark. The bottom timeline is time-gated. Its bands never move, but a red kill line slides left as DPS rises and greys out everything after it.

Start at 2,000 DPS, where the two timelines are identical. Drag slowly to the right. In the top view, watch the Meteor tick slide toward the end of the sky band and drop off it at 4,500. In the bottom view, watch the kill line swallow the first Firestorm at 2,667 DPS, the whole of P3 at 2,857, and the first Meteor at 3,750. Drag left below 1,667 and both timelines turn red at 360 s, the enrage. The numbers panel lists every cast time, so you can copy them into the table above.

### Cross-game recognition

**World of Warcraft, Onyxia (classic, level 60).** Onyxia's transitions at 65% and 40% are HP gates. In our notation, P2 covers `H_2 = 0.25 × H`, and the air phase lasts `0.25 × H / D`. In the model, every mechanic tied to the air phase, including the Deep Breath runs and the whelp waves, gets less time to happen as the raid gets stronger. A raid strong enough would pass through the whole air phase in seconds. The same page says developer Jeff Kaplan described the timing of Deep Breath as random. That is a design choice too. A random ability inside an HP-gated phase has no fixed skip threshold, only a probability of being skipped that grows with DPS.

**World of Warcraft, Ragnaros (classic Molten Core).** Ragnaros is time-gated, with a hybrid exit. His submerge starts at a fixed `s = 180` s. It ends at 90 s *or* when all 8 Sons of Flame die, whichever comes first. That second condition is an **event gate**, a transition that fires on something the players do. In our model a strong raid shortens the submerged phase by killing adds quickly, and a raid strong enough to kill Ragnaros in under 3 minutes never sees the submerge at all, exactly like the Warden's time-gated P2.

**World of Warcraft, Patchwerk (classic Naxxramas).** Patchwerk has almost no phases, which makes his clocks easy to see. The Warcraft Wiki records a berserk after 7 minutes that multiplies his damage and is effectively a wipe, and a separate enrage at 5% health. The first is our `E = 420` s, giving `D_min = H / 420`. The second is an HP gate into a last, short phase. One boss, both kinds of gate.

**Cuphead (2017), Cagney Carnation.** The same model works outside MMOs. The Cuphead Wiki lists Cagney's health on Regular difficulty as 1,300, split into 702 for the first phase and 598 for the second, so the transition is an HP gate at `702 / 1,300 = 54%` of total damage dealt. On Simple difficulty the wiki lists 1,000 health and the fight ends after the first phase. In our terms, the easy mode deletes the last phase outright rather than shrinking it. That is a third answer to "what should weaker or stronger players skip?"

Four bosses, four presentations, one model. When you study a boss, write it down as phases, gates and timelines, then ask: *what fires each transition, and what does a group twice as strong never see?*

### Eyes-open design judgment

- **HP gates reward damage with a shorter fight, and charge for it in content.** That is often exactly what you want. Gear progress should feel like power, and "we skipped the air phase" feels great. But you must know which abilities have skip thresholds inside the DPS range you expect. Compute `H_i / a` for every signature ability and compare it to the DPS your best groups will have at the end of the tier, not at launch.
- **Time gates protect the script, and make the ending the fragile part.** Time-gated fights are identical for every group until the kill, so they are easier to teach, to tune for fairness, and to predict with timers. But a strong group kills the boss before the final phase, which is usually the climax. Time gates also make DPS nearly irrelevant except through the enrage, which some players find flat.
- **Hybrid gates buy guarantees.** Common patches include casting a phase's signature ability immediately on entering the phase (set `a` close to 0, so `D_skip` becomes huge), or holding the boss's health at the threshold until the mechanic resolves (the boss cannot drop below 30% while Meteor is in the air). Each guarantee costs something. The first removes the build-up. The second wastes the group's damage and can feel like the game is cheating. Lab 13 measures the second.
- **An enrage is the only rule that sets a floor.** Nothing else in the model punishes low DPS. A fight with no enrage can be won by a group that survives long enough, which is sometimes the right experience (a story boss) and sometimes an exploit (a healer-only group grinding for an hour).
- **Keep the telegraph fair at every DPS.** GD101 week 12 gives the minimum telegraph time. HP gating can push two abilities from different phases close together at high DPS, because phases shrink and the next phase's first cast arrives sooner. Check the shortest gap between any two dangerous casts across your DPS range, not only at design DPS.

## 3. Scripting the fight as data

The Warden fits in six lines of data. That is the point. A boss script should be data that a designer edits, not code a programmer rewrites. [CS102 week 13](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w13-data-driven-design-stats-in-json-and-csv.md) argued this for item stats, and it matters more here because boss scripts are tuned constantly during testing.

A workable encounter format has four parts.

1. **Phases**, each with an entry condition (HP below a threshold, time since pull, an event such as "all adds dead", or any combination), and an optional entry action (a line of dialogue, a knockback, an arena change).
2. **Abilities per phase**, each with first cast, period, a telegraph time, and optionally a random window (fire somewhere between 30 and 40 s rather than at exactly 35).
3. **Global rules**, such as the enrage timer, soft enrages at low health, and the guarantees from section 2.
4. **Targeting**, which hands off to the threat table and targeting rules of week 12. The script says "cast Meteor"; week 12's system says at whom.

At run time, the boss's AI is a small loop that runs every server tick. It checks the current phase's exit conditions, advances the phase if one fires, then fires every ability whose next cast time has arrived. Written this way, the phase logic is a state machine with guarded transitions, and each state owns a timeline. Nothing about it is clever. That is correct for a boss. The cleverness is in the numbers.

### Randomness inside a script

Fully fixed timelines are learnable, which is good, until they become a solved sequence that players execute from a timer bar. Designers add controlled randomness in three places.

- **Jitter.** Each cast lands in a window, `a ± j`. Players still learn the rhythm but must watch the telegraph. The skip threshold becomes a range, from `H_i / (a + j)` to `H_i / (a − j)`.
- **Choice.** The boss picks one ability from a small set at each slot, perhaps weighted ([MA102 week 9](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w09-weighted-tables-and-loot-table-design.md) covers weighted tables). Players learn the set and must read which one is coming.
- **Order.** The same abilities fire in a shuffled order each cycle, like a bag of tiles drawn without replacement. Every ability still appears once per cycle, so no group gets unlucky with three Meteors in a row.

Each form of randomness makes timers less exact and telegraphs more important. Decide which one you use by asking what you want players to practice, executing a known sequence or reading and reacting.

### Adds and the second clock

Many fights add a second source of pressure, **adds** (extra enemies the boss summons). Adds turn DPS into a split decision. Every second the group spends on adds is a second not spent on the boss, so the boss's effective `D` drops. With an HP-gated boss, that lengthens the current phase and adds casts. That is a feedback loop. Ignoring adds speeds up the boss but lets adds pile up. Killing adds slows the boss and gives it more casts. Ragnaros's event gate is the reverse design. Killing adds *shortens* the phase. When you design adds, decide which way the loop runs.

## 4. Readable bosses

A boss that the group cannot read is not hard. It is unfair. Three habits keep a scripted fight readable.

- **Telegraph every lethal ability.** A cast bar, an animation wind-up, a ground marker. Length from GD101 week 12. Keep the telegraph length fixed across difficulties even when damage changes, so learning carries over.
- **Mark every transition.** Phase changes should be impossible to miss: a line of dialogue, a pause in attacks, a change in arena or music. Players reason about the fight as phases, so show them the phase.
- **Keep one new idea per phase.** Players can hold only a few new rules at once ([UX201 week 2](../../UX201-game-ux-and-player-psychology/lectures/w02-cognitive-load-and-ui.md) covers cognitive load). The classic structure teaches one mechanic per phase, then combines them in the last phase, which is why the final phase is often the hardest, and why skipping it under a time gate loses the payoff.

## In-class activity (25 minutes)

In groups of three, design a three-phase boss for a five-player dungeon. The designers expect groups to deal between 1,500 and 3,000 DPS over the life of the content.

1. (8 min) Write your boss as a table like the Warden's: `H`, `H_i`, one ability per phase with `a` and `p`, and an enrage `E`. Pick HP gates, time gates or a hybrid for each transition.
2. (7 min) Compute `D_min` and the skip threshold of every ability. Are any of them inside the 1,500 to 3,000 range? Use the interactive's custom mode to check.
3. (5 min) Change one number or one gate so that the signature ability is seen at least once by every group in the range, without letting the weakest group win after the enrage.
4. (5 min) Swap with another group. Find the DPS in their range at which the fight shows the fewest mechanics, and say which ones.

Expected output: your table, the list of thresholds, the one change you made and why, and the weak point your partners found.

## Common misconceptions

- **"HP-gated fights are the same for everyone, just faster."** Phase lengths scale with `1 / D`, but cast times do not, so the *number* of casts changes in steps and abilities disappear entirely past `H_i / a`. Faster is a different fight.
- **"Time gates stop players from skipping content."** They stop players from shortening a phase. A strong group skips the phases at the end instead.
- **"The enrage is what makes a boss hard."** The enrage sets a minimum DPS and nothing else. Difficulty comes from what the group must do while dealing that damage: the casts per phase, the telegraphs and the overlaps.
- **"A boss script is an AI problem."** Most of a boss is authoring and tuning. The AI parts are the targeting (week 12) and any reactive rules. Treat the script as content with numbers you can check.

## Check yourself

1. The Warden's P2 Meteor first cast moves from 40 s to 25 s, period unchanged. What is its new skip threshold? How many Meteors does an HP-gated group at 4,600 DPS now see?
2. A boss has 900,000 health and an enrage at 6 minutes. A group deals 2,400 DPS. Do they beat the enrage, and with how many seconds to spare?
3. In the time-gated Warden, at what DPS does the group stop seeing any Firestorm at all? At what DPS do they stop seeing any Meteor?
4. A designer wants the Warden's Meteor to be seen by every group up to 8,000 DPS, keeping P2 at 30% of health and the first cast at 40 s. How much health must the Warden have? What happens to `D_min` if the enrage stays at 360 s?
5. Ragnaros's submerge ends after 90 s or when all 8 adds die. A raid kills one add every 8 s. How long does the submerged phase last? Which rule fired?

<details>
<summary>Answers</summary>

1. `D_skip = 180,000 / 25 = 7,200` DPS. At 4,600 DPS, P2 lasts 39.1 s, and Meteor fires at 25 s only (the next would be at 65), so 1 cast.
2. `D_min = 900,000 / 360 = 2,500` DPS. At 2,400 DPS the kill would come at 375 s, 15 s after the enrage. They fail.
3. Firestorm first fires at `210 + 15 = 225` s, so the group sees none when the kill comes at or before 225 s: `600,000 / D ≤ 225`, so `D ≥ 2,667` DPS. Meteor first fires at `120 + 40 = 160` s, so none at `D ≥ 600,000 / 160 = 3,750` DPS.
4. The first cast is lost when `40 × D ≥ 0.3 × H`, so to keep it up to 8,000 DPS we need `0.3 × H > 40 × 8,000 = 320,000`, so `H > 1,066,667`. With `H = 1,066,667` and `E = 360`, `D_min` rises from 1,667 to about 2,963 DPS. Buffing health to protect a mechanic also raises the DPS floor, so the enrage must move too, to at least `1,066,667 / 1,500 ≈ 711` s if 1,500-DPS groups must still win.
5. Eight adds at one per 8 s die by 64 s, before the 90 s timer. The event gate fired, and the phase lasted 64 s.

</details>

## Lab / assignment hook

[Lab 13, encounter scripts and skip thresholds](../labs/lab13.md). You write an encounter runner that reads a boss from data, produces the full timeline of casts under HP gates, time gates and a guarded hybrid, and checks it against the Warden's numbers from this lecture. Then you design your own boss so that no signature ability has a skip threshold inside a given DPS range, and write a one-page tuning note.

## Sources

- Warcraft Wiki, "Onyxia (Classic)" (classic level-60 encounter, accessed September 2026). Phase 2 at 65% health, phase 3 at 40%; air-phase fireballs, whelps and Deep Breath; the page's report that Jeff Kaplan described Deep Breath timing as random.
- Warcraft Wiki, "Ragnaros (tactics)" (original Molten Core encounter, accessed September 2026). Submerge after 3 minutes of combat with 8 Sons of Flame; returns after 90 seconds or when the adds are dead, whichever is first; no health-based phase in the original version.
- Warcraft Wiki, "Patchwerk (Classic)" (classic Naxxramas, accessed September 2026). Berserk after 7 minutes; enrage at 5% health.
- Cuphead Wiki (Fandom), "Cagney Carnation" (Cuphead, 2017 release, accessed September 2026). Health 1,000 / 1,300 / 1,500 on Simple / Regular / Expert; Regular phase 1 at 702 and phase 2 at 598; Simple ends after the first phase.
- Deadly Boss Mods, project page on CurseForge (World of Warcraft add-on, current). Timers, warnings and alerts for boss abilities.
- Millington, I. (2019). *AI for Games*, 3rd ed., chapter 5 (state machines, hierarchical state machines). CRC Press.

## Interactive spec: examples/w13-phase-gates.html

**Purpose.** Show one boss under two phase rules at the same DPS, so the student sees that HP gates shrink phases and delete abilities at thresholds, while time gates keep phases fixed and delete the ending.

**The one insight.** At the design DPS both timelines are identical. As DPS rises, the top (HP-gated) timeline loses the Meteor tick abruptly at exactly 4,500 DPS, while the bottom (time-gated) timeline keeps every early tick and loses whole phases from the right. The student should see this within ten seconds of dragging the slider.

**Layout.** Two horizontal timelines stacked, sharing one time axis from 0 to 400 s. Top label "HP gates (phase ends when its HP is gone)", bottom label "Time gates (phase starts at a fixed time)". Under them, a numbers panel with one row per ability and two columns (HP-gated, time-gated), each listing cast times in seconds with one decimal and the count. Above them, the controls. Under 700 px width, the axis compresses to fit and the numbers panel becomes one column per mode stacked.

**Model (must match the lecture exactly).**
- Defaults: `H = 600,000`, `E = 360`. Phases P1, P2, P3 with `H_i = 240,000, 180,000, 180,000`. Time-gated lengths 120, 90 s, P3 open-ended. Abilities: P1 Summon adds `a = 20, p = 45`; P2 Meteor `a = 40, p = 40` (signature, drawn larger); P3 Firestorm `a = 15, p = 25`.
- HP-gated: phase `i` starts at the sum of earlier `H_j / D` and lasts `H_i / D`. A cast at phase time `t` exists if `t < H_i / D`.
- Time-gated: phase starts 0, 120, 210. A cast at absolute time `T` exists if `T` is inside its phase window and `T < H / D`.
- Both: the fight ends at `min(H / D, E)`. If `H / D > E`, draw a red "ENRAGE" marker at `E`, grey out everything after it, and state "wipe at 360 s".
- Use exact comparisons as in the lecture (compare `t × D < H_i`, integers), so thresholds land exactly.

**Controls.**
- DPS slider 1,000 to 8,000, step 100, default 2,000; a number input beside it accepts any integer in range. Keyboard: arrow keys step 100, Page Up/Down step 1,000.
- Toggle "Guard Meteor" (HP-gated view only): P2 cannot end before `40 + 5 = 45` s of phase time; damage in the locked time is wasted. Show the extra seconds and the new kill time.
- "Custom" mode: editable table of `H`, `E`, three phase `H_i` (percent inputs that must sum to 100), time-gated lengths, and one ability per phase (`a`, `p`). Validation messages inline.
- Reset button.

**Drawing.** Phase bands in three tones from the palette; cast ticks as vertical marks with the ability's initial; the signature ability as a larger diamond. A vertical kill line (red) on both timelines at `H / D`. Hovering or focusing a tick shows "Meteor, phase time 40.0 s, absolute 94.5 s". A small badge next to each ability's name shows its skip threshold `H_i / a` for the HP-gated view.

**Test values (defaults, no guard).**
- 2,000 DPS: kill 300.0 s. HP-gated counts [3, 2, 3], time-gated [3, 2, 3]. Meteor at absolute 160.0 and 200.0 in both.
- 3,200 DPS: kill 187.5 s. HP [2, 1, 2], time [3, 1, 0].
- 4,400 DPS: kill 136.4 s. HP [1, 1, 2], time [3, 0, 0]. HP Meteor at absolute 94.5 s.
- 4,500 DPS: HP Meteor count 0 (threshold is inclusive of the skip).
- 4,600 DPS: kill 130.4 s. HP [1, 0, 1], time [3, 0, 0].
- 6,000 DPS: kill 100.0 s. HP [1, 0, 1], time [2, 0, 0]. With guard: P2 lasts 45 s instead of 30 s, Meteor count 1, kill 115.0 s.
- 1,600 DPS: ENRAGE at 360 s on both; HP-gated P3 cut at 360 s.
- Skip thresholds shown: Summon adds 12,000 (first cast), Meteor 4,500, Firestorm 12,000.

**First screen.** 2,000 DPS with both timelines identical and a caption "Same boss, same DPS. Drag DPS up and watch what each rule takes away."

**Accessibility.** All controls keyboard operable with visible focus. The numbers panel is a real table. Announce the counts in an `aria-live="polite"` region at most once per 500 ms while dragging. Colors from `templates/interactive-tokens.css` in light and dark; ticks differ by shape as well as color. With `prefers-reduced-motion`, no animated transitions between states.

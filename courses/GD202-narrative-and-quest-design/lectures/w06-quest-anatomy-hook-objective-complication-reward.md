# GD202 · Week 06 — Quest Anatomy: Hook, Objective, Complication, Reward

**Why this matters:** A quest is a small contract. The hook makes a promise, the objective states the terms, the complication tests them, and the reward pays out. Players read every quest this way, and they also run a quick sum you rarely see written down: is this worth my time compared with what else I could be doing? This week you learn to build each part on purpose and to check that sum before players do.

**You will be able to:**
- Break any quest into hook, objective, complication and reward, and critique each part against the player's question it must answer.
- Compute a quest's reward rate, including travel and level-based reward decay, and decide whether a given player will take it.
- Compute how much reward a complication must add to keep a quest worth doing, and choose a non-XP reward when XP cannot pay for it.
- Design a reward that pays off the promise its hook made.

**Before class:** Bateman (ed.), *Game Writing: Narrative Skills for Videogames* (2nd ed., 2021), the chapter on structure. Reread [GD203 week 7, XP curves](../../GD203-combat-and-progression-design/lectures/w07-xp-curves.md), section 3, on income curves.

**Prerequisites from earlier courses:** [GD101 week 2, players, objectives, procedures, rules](../../GD101-introduction-to-game-design/lectures/w02-players-objectives-procedures-rules.md) (what an objective is). Looking ahead, [GD203 week 7, XP curves](../../GD203-combat-and-progression-design/lectures/w07-xp-curves.md) (next semester) covers XP income per hour and why time per level is what players feel. [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md). [UX201 week 5, reinforcement schedules and ethics](../../UX201-game-ux-and-player-psychology/lectures/w05-reinforcement-schedules-and-ethics.md). [GD202 week 4, dialogue systems and state flags](w04-dialogue-systems-and-state-flags.md) (quest stages). [GD202 week 5, characters and companions](w05-characters-and-companions.md) (approval as a reward).

**Interactive:** [`examples/w06-quest-detour.html`](../examples/w06-quest-detour.html). Keep it open during section 2.

---

## 1. Four parts, four questions

Every quest, from a one-line bounty to a ten-hour story arc, has four parts. Each part answers one question the player is asking, whether or not they would put it in words.

| Part | The player's question | What a good one does |
|---|---|---|
| **Hook** | Why should I care? | Gives a person, a problem and a stake in one or two lines. |
| **Objective** | What exactly do I do, and where? | States a verb, a target, a count and a place that the quest log can show. |
| **Complication** | What changed? | Breaks the plan the player formed at the hook, and gives them something new to decide or do. |
| **Reward** | Was it worth it? | Pays off the hook's promise, in a currency the player values at that moment. |

### Hook

The **hook** is the first contact. It is usually a line of dialogue, a notice board, an item that starts a quest when picked up, or something the player sees. A hook works when it names a person with a problem and makes the stake concrete. "Help the village" is not a hook. "The miller's daughter went to check the traps at dawn and her dog came back alone" is a hook. It has a person, a problem, a clock and an image.

Hooks also make a promise about what kind of quest this is. The miller's hook promises a search, some danger and an emotional payoff. If the quest turns out to be "collect eight wolf pelts", the promise is broken, and the player notices even if they could not tell you why.

### Objective

The **objective** is the part the game can check. Write it so it fits in a quest log line. The test is four slots: a **verb**, a **target**, a **count** and a **place**. "Find Mira (1) at the trapping grounds east of the mill." "Recover 3 stolen crates from the Smuggler's Cave." If any slot is missing, players get lost or stuck. A missing place sends them to a wiki. A missing count leaves them unsure when to go back.

The objective is also where the story state from week 4 lives. Each objective step is a quest stage (10: find Mira, 20: follow the tracks, 30: return her home), and the dialogue reads those stages.

### Complication

The **complication** is the moment the plan changes. The player forms a plan at the hook ("go east, find the girl, come back"), and the complication breaks it. The standard types are:

- **Reversal.** A fact the player relied on turns out false. The client lied, or the bandits are the victims.
- **Escalation.** The task is bigger than stated. The cave has a second level, or the wolves have a leader.
- **Dilemma.** The player must choose between two things they want. Save the girl or catch the smuggler before he escapes.
- **Obstacle.** A new thing is in the way. The bridge is out, so find another route.

The first three change what the quest means. The obstacle only changes how long it takes. Obstacles are the cheapest to write and the most likely to feel like padding, and section 2 shows why in numbers.

### Reward

The **reward** is what the player gets when the quest ends. Players value several currencies:

- **Power.** XP, gear, abilities.
- **Wealth.** Gold and tradeable items.
- **Access.** New areas, vendors, quests or features.
- **Story.** A resolution, a revelation, a character's fate.
- **Relationship.** Approval or reputation with a companion or faction (week 5).

A reward is well chosen when it pays off the hook's promise and is worth something to the player at that moment. Both halves matter, and the second half is the one designers can measure.

## 2. Worked example: the detour test

### The hook

In classic-era World of Warcraft, a quest you completed long after outlevelling it paid a fraction of its listed XP. Players who documented the rewards on the Warcraft Wiki found a clean pattern. Full XP up to 5 levels above the quest's level, then 80%, 60%, 40% and 20% for 6, 7, 8 and 9 levels above, and 10% from 10 levels above onward, rounded to the nearest 5 XP. That cut-off gives the pattern players complained about. A quest line you left for later is paying 10% by the time you come back.

Whatever Blizzard's intent, the decay is a reward-logic decision in effect. It tells players, in the currency they care about, that this content is no longer for them and the next zone is. To see why it works, and to see how every quest you design is judged, you need the sum players run in their heads.

### The model

A player choosing whether to take a quest compares it with the best alternative use of the same time. In an MMO the alternative is usually grinding: killing monsters where you stand, which pays a steady **baseline rate** `r₀` in XP per minute.

```
reward paid  R  = R_full × m(Δ)
time cost    t  = t_travel + t_task
reward rate  v  = R / t

take the quest  if  v ≥ r₀
```

- `R_full` is the quest's listed reward.
- `Δ` is the player's level minus the quest's level, and `m(Δ)` is the decay multiplier. For the classic-era WoW pattern, `m` is 1 for `Δ ≤ 5`, then 0.8, 0.6, 0.4, 0.2, and 0.1 for `Δ ≥ 10`.
- `t_travel` is the time to reach the quest area and return. `t_task` is the time to do the objective there.
- `r₀` is what the player earns per minute doing something else.

This is the income idea from GD203 week 7, turned around. There you asked how fast XP flows in. Here the player asks whether one particular source beats the flow they already have.

### Numbers you can check

A level-20 character faces an invented quest board. Grinding nearby pays `r₀ = 200` XP per minute. Travel and task times are what a playtest measured.

| Quest | Quest level | Listed XP | Travel (min) | Task (min) |
|---|---|---|---|---|
| Wolves at the mill | 19 | 1,800 | 2 | 6 |
| The ogre's tithe | 22 | 4,200 | 9 | 14 |
| Letter to the ferryman | 18 | 900 | 1 | 3 |
| Old bones | 12 | 2,000 | 3 | 5 |
| Smuggler's cave | 20 | 3,000 | 5 | 9 |

Here is the detour test in Python, with the quests sorted by listed XP, the order a quest log or a notice board tends to suggest.

```python
PERCENT = {6: 80, 7: 60, 8: 40, 9: 20}   # player level minus quest level -> % of XP

def quest_xp(full_xp, delta):
    """Original-era WoW quest XP (community-measured): full up to 5 levels over,
    then 80/60/40/20%, then 10% from 10 levels over, rounded to the nearest 5."""
    if delta <= 5:
        return full_xp
    pct = PERCENT.get(delta, 10)
    return (full_xp * pct + 250) // 500 * 5

PLAYER_LEVEL, BASELINE = 20, 200   # baseline: XP per minute from grinding mobs

BOARD = [  # name, quest level, full XP, travel minutes, task minutes
    ("Wolves at the mill",     19, 1800, 2,  6),
    ("The ogre's tithe",       22, 4200, 9, 14),
    ("Letter to the ferryman", 18,  900, 1,  3),
    ("Old bones",              12, 2000, 3,  5),
    ("Smuggler's cave",        20, 3000, 5,  9),
]

print(f"{'quest':24} {'XP paid':>7} {'min':>4} {'XP/min':>7}  take it?")
for name, qlvl, full, travel, task in sorted(BOARD, key=lambda q: -q[2]):
    xp = quest_xp(full, PLAYER_LEVEL - qlvl)
    minutes = travel + task
    rate = xp / minutes
    print(f"{name:24} {xp:7} {minutes:4} {rate:7.1f}  {'yes' if rate >= BASELINE else 'no'}")
```

It prints:

```
quest                    XP paid  min  XP/min  take it?
The ogre's tithe            4200   23   182.6  no
Smuggler's cave             3000   14   214.3  yes
Old bones                    800    8   100.0  no
Wolves at the mill          1800    8   225.0  yes
Letter to the ferryman       900    4   225.0  yes
```

Check two by hand. Old bones is 8 levels below the player, so it pays 40% of 2,000, which is 800 XP over 8 minutes, 100 per minute. The ogre's tithe pays its full 4,200, but 9 minutes of travel plus 14 of fighting makes 23 minutes, and `4,200 / 23 ≈ 182.6`, below the baseline.

### What the table tells you

The quest with the biggest number fails the test. The two smallest quests pass it best. A notice board that shows only the listed reward is showing players the wrong column, and players who have done the sum once will skip the ogre and pick up the letter.

Travel is part of the price. Give the player a mount that halves travel time and the ogre's tithe becomes `4,200 / (4.5 + 14) ≈ 227` per minute, which beats the baseline. Faster travel does not change the quest at all. It changes which quests are worth doing. When an MMO adds faster travel, the whole quest board gets re-priced.

Decay moves quests off the board over time. At level 17, Old bones pays full XP and earns 250 per minute, the best on the board. By level 20 it pays 100. The quest did not change. The player did. That is what the WoW decay is for. It prices old content out of the player's plan without removing it from the world.

### The complication tax

Now add a complication to the Smuggler's cave. Halfway through, the tunnel collapses and the player must dig through a side passage, which a playtest times at 4 extra minutes. The quest now takes 18 minutes.

```
v = 3,000 / 18 ≈ 166.7 per minute   (below r₀ = 200)
```

A quest that passed now fails. To keep it at the baseline, the reward must rise to at least `r₀ × t = 200 × 18 = 3,600`. The complication costs 600 XP. In general, each minute a complication adds costs `r₀` in reward, and the full requirement is:

```
R_full × m(Δ) ≥ r₀ × (t_travel + t_task + t_complication)
```

That is the **complication tax**. An obstacle that adds time and nothing else must be paid for, or it pushes the quest below the line. A reversal or a dilemma can pay for itself in a currency that is not XP. The player learns something, chooses something, or gets a scene they will remember. Players will spend minutes on meaning. They resent spending them on a collapsed tunnel.

Open the interactive now. The left panel is the board sorted by listed XP, as a notice board shows it. The right panel is the same quests as bars of XP per minute, with the baseline drawn across. Drag the player level from 17 to 30 and watch quests fall below the line one by one as decay bites. Toggle the mount, then the tunnel collapse. The left panel barely changes. The right panel reorders.

### Cross-game recognition

The same test runs whenever a player weighs a quest against the alternatives. What changes is the currency.

**World of Warcraft (classic era).** The decay `m(Δ)` above, measured by players rather than published by Blizzard. It prices old quests out of a player's plan. The Warcraft Wiki records the same era's total of 4,084,700 XP to reach level 60, which is the scale these rewards are measured against. Once a player reaches the level cap, quests convert their XP into extra gold, so `R` stays positive in a new currency.

**Old School RuneScape (2013 onward, updated through 2025).** Every quest awards **quest points**, from 1 to 6 per quest in most cases, alongside any XP. Quest points are an access currency. For example, 32 are needed to enter the Champions' Guild and start Dragon Slayer I, and 55 to start Heroes' Quest. In our model, part of `R` is not XP at all. It is a ticket, and its value to the player is the value of what it opens. That lets a quest with poor XP per minute pass the detour test, because the player is buying access, and access has no substitute from grinding.

**The Elder Scrolls V: Skyrim (2011).** The Radiant system generates quests from parts (a location, an enemy type, a reward), producing a near-endless supply. The UESP wiki notes two things. Radiant quests are not built to be large or particularly interesting, and the system tries to send the player to locations they have not yet discovered. In our model the generator holds `R` modest and makes the destination part of the reward. Discovery of a new place is the currency. For a player who has seen every cave, that currency is gone, and the model predicts radiant quests start to fail the test late in a playthrough.

Three games, one sum. When you look at any quest, ask what it pays, in which currency, what it costs in minutes including travel and complications, and what the player's best alternative is.

### Design judgment

- **Decide who the rate-maximizer is and whether you care.** Some players run this sum constantly. Others never do. Story-led single-player games can ignore it more safely than MMOs, where the fastest route to the cap spreads through guides quickly.
- **Do not let story quests fail the test by accident.** If the main story pays less per minute than grinding, efficiency-minded players skip it, and you have paid writers for scenes nobody watches. Pay story quests at or above the baseline, or pay them in a currency grinding cannot give (access, relationship).
- **Decay is a steering tool.** A decay curve like WoW's pushes players forward. If you want players to return to old zones (a world that grows with them), use level scaling or non-XP rewards instead, because decay tells them the opposite.
- **Price complications before writing them.** For every complication, write down the minutes it adds and what it pays back. An obstacle that pays nothing is the first thing to cut in the edit.
- **Show the right column when you can.** You cannot show XP per minute on a notice board, but you can show honest time estimates or difficulty, and you can make travel short. Players who trust your board stop reading guides.

## 3. The promise ledger

Section 2 treats the reward as a number. Players also judge it as a payoff. The hook made a promise, and the reward must keep it.

Keep a **promise ledger** for each quest. It is a two-column list: what the hook implies on the left, what the reward delivers on the right.

| The hook implies | The reward delivers | Kept? |
|---|---|---|
| Mira is in danger | Mira is found alive (or her fate is shown) | Yes |
| The miller is desperate and poor | 300 gold from the miller | Broken. A poor miller paying a fortune reads false. |
| Something is hunting near the mill | The wolf leader is killed and the trappers return | Yes |

The broken row is common. Designers set rewards from a table (quest level times a constant) and writers set hooks from the story, and nobody checks that the two agree. The fix is to pay in the currency the fiction supports. The miller cannot pay 300 gold, but he can offer free milling (a vendor discount, which is access), his late wife's ring (an item with story), or a standing welcome (reputation). The XP still comes from the game, which players accept as outside the fiction. The gold should come from someone who could plausibly have it.

### Reward timing

When the reward arrives matters as much as what it is. UX201 week 5 covered reinforcement schedules. Quests are fixed-ratio schedules by design: do the steps, get the payout. Two timing choices are worth making on purpose.

- **Pay at the complication, not only at the end.** A small reward at the moment the plan changes (a clue, a key, a companion reaction) turns the complication from a tax into a beat.
- **Keep the final reward where the story ends.** If the emotional resolution is at the cave but the reward is back in town, the player walks back through a finished story to collect it. Some games let the quest complete remotely for this reason. Others use the return walk on purpose, for a scene with the quest-giver. Choose one; do not get the walk by accident.

## 4. Anatomy under pressure: scaling to many quests

A single quest is easy to get right. An MMO zone has dozens, and a live game adds more every patch. Two habits keep the anatomy intact at scale.

**Write the four lines first.** Before any dialogue, write each quest as four lines: hook, objective, complication, reward. A zone of 30 quests is then 120 lines you can read in ten minutes. Duplicated complications and broken promises jump out at that density. [Week 8](w08-quest-chains-and-zone-storytelling.md) builds chains and zones from this format, and [week 7](w07-quest-types-and-redeeming-them.md) looks at what happens inside the objective for each quest type.

**Run the detour test on the whole board.** Put every quest in a zone into the model from section 2, at the level a player is expected to be when they arrive. Look for quests below the baseline with no non-XP reward, which players will skip. Look also for quests far above the baseline, which will dominate and make the rest look bad. Then fix the outliers by moving travel, task time or reward. This is the same spreadsheet discipline as GD203's balancing workshop, applied to content.

## In-class activity (25 minutes)

In pairs, take one quest from a game you have played recently (describe it in your own words; do not copy its text).

1. Write its four lines: hook, objective, complication, reward. If it has no complication, say so.
2. Estimate travel and task minutes from memory, and the reward. Pick a baseline for that game (what you would otherwise have been doing, in the same currency). Does it pass the detour test?
3. Write its promise ledger with at least three rows.
4. Redesign one part to fix the weakest point you found. If you add a complication, price it: minutes added, and what it pays back.
5. Swap with another pair and try to break their redesign. Find a player type for whom it now fails.

Expected output: the four lines, the detour numbers, the ledger, the redesign with its price, and the failure your partners found.

## Common misconceptions

- **"Bigger rewards make better quests."** Players compare rate, not size. The ogre's tithe paid the most XP and failed the test.
- **"Complications make quests more interesting."** Reversals and dilemmas do. Obstacles that only add minutes are a tax, and they need paying back.
- **"Reward decay punishes players for exploring."** It steers them, and it is the designer's decision. If you want old content revisited, use a different reward logic.
- **"The reward is just numbers from a table."** The reward is also the end of a story. A payout that contradicts the hook breaks the fiction even when the numbers are fine.

## Check yourself

1. A level-27 player looks at the Smuggler's cave (quest level 20, 3,000 listed XP, 14 minutes). What XP does it pay, what is its rate, and does it pass at `r₀ = 200`?
2. The designers want the ogre's tithe to pass at level 20 without adding a mount. Travel is fixed at 9 minutes. How short must the task be, to the nearest minute?
3. A complication adds 6 minutes to the Wolves at the mill quest. What listed XP does it now need to stay at `r₀ = 200`? If the designers refuse to raise XP, name a reward currency that could keep players taking the quest, and say which kind of player it will not work for.
4. In Old School RuneScape a player has 30 quest points and wants to enter the Champions' Guild. Quest A pays 1 quest point and takes 10 minutes. Quest B pays 2 quest points and takes 35 minutes. Compare them in quest points per minute. Which one gets the player into the Guild, and why is XP per minute the wrong measure here?

<details>
<summary>Answers</summary>

1. `Δ = 7`, so it pays 60% of 3,000, which is 1,800 XP. Rate `1,800 / 14 ≈ 128.6` per minute. It fails.
2. Need `4,200 / (9 + t) ≥ 200`, so `9 + t ≤ 21` and `t ≤ 12` minutes. The task must drop from 14 to 12 minutes.
3. Time becomes `8 + 6 = 14` minutes, so it needs `200 × 14 = 2,800` XP, up from 1,800. A non-XP currency such as access (the miller's discount), story (Mira's rescue shown on screen) or relationship (companion approval) could carry it. It will not work for a pure rate-maximizer who values only XP, and in an MMO those players are the ones writing the guides.
4. Quest A pays `1 / 10 = 0.1` points per minute and quest B pays `2 / 35 ≈ 0.057`, so A is the better rate. But the player needs 32, so A alone leaves them at 31 and only B gets them in. Quests are done once, so the real comparison is B (35 minutes) against A plus the shortest other 1-point quest. If that quest takes under 25 minutes, the pair wins. The reward is access, so the right measure is the cheapest route to 32 points, and XP per minute does not enter into it.

</details>

## Lab / assignment hook

[Lab 06, quest spec and board audit](../labs/lab06.md). You implement the detour test for a whole quest board, including decay, travel modifiers and complications, then write three quests for one zone in four-line form with promise ledgers and tune them so each passes the test for its intended player. The quests are the first draft of the final quest chain (60% of the grade), which [week 7](w07-quest-types-and-redeeming-them.md) and [week 8](w08-quest-chains-and-zone-storytelling.md) extend.

## Sources

- Warcraft Wiki, "Experience point", sections "Quest XP" and "Experience to level" (classic-era World of Warcraft; the Quest XP section is community-derived and does not name a patch). Quest XP decay: full to 5 levels above quest level, then 80/60/40/20%, 10% from 10 levels above, rounded to 5 XP; 4,084,700 XP to reach level 60 in Classic; XP converted to gold at the level cap.
- Old School RuneScape Wiki, "Quest points" (read September 2026, after the 22 October 2025 update). 1 to 6 quest points per quest in most cases; 32 needed for the Champions' Guild and Dragon Slayer I; 55 for Heroes' Quest.
- UESP Wiki, "Skyrim:Radiant" (The Elder Scrolls V: Skyrim, 2011). Radiant quests built from components such as location, enemy and reward; not designed for large or complex quests; aims to send the player to undiscovered locations.
- Bateman, C. (ed.) (2021). *Game Writing: Narrative Skills for Videogames*, 2nd ed. Bloomsbury Academic.

## Interactive spec: examples/w06-quest-detour.html

**Purpose.** Show that the order a notice board suggests (by listed reward) is not the order players should act in (by reward per minute against their baseline), and that player level, travel speed and complications reshuffle it.

**Layout.** Two linked panels, stacked on mobile, side by side from 900px. Controls above.

- **Left panel, "What the board shows".** Horizontal bars of listed XP for the five quests, sorted descending. Each bar is labelled with quest name and listed XP. A small grey sub-bar inside each shows XP actually paid after decay, labelled "paid: 800" etc.
- **Right panel, "What it's worth to you".** Horizontal bars of XP per minute, sorted descending, with a vertical dashed line at `r₀` labelled "baseline 200/min". Bars at or above the line use the accent colour and a check icon; bars below use neutral with a cross icon. Each bar shows its value to one decimal.
- **Table under both panels.** Columns: quest, quest level, `Δ`, `m(Δ)`, XP paid, travel, task, complication, total minutes, XP/min, pass. This is the numbers view students copy into their notes.

**Controls.**
1. Player level slider 10 to 32, default 20.
2. Baseline `r₀` slider 50 to 400 XP/min, step 10, default 200.
3. Toggle "Mount (travel × 0.5)".
4. Toggle "Tunnel collapse in Smuggler's cave (+4 min)".
5. A "Required reward" readout for the selected quest (click or Enter on a bar selects it): the smallest listed XP, a multiple of 5, whose paid XP (after decay and rounding) is at least `r₀ × total minutes`. Shown next to the listed XP. Find it by stepping upward in 5s from `ceil(r₀ × minutes / m / 5) × 5 − 10`.

**The one insight.** At default settings the ogre's tithe is first on the left and fails on the right, while the letter to the ferryman is last on the left and ties for first on the right.

**Model.** `m(Δ) = 1` for `Δ ≤ 5`; 0.8, 0.6, 0.4, 0.2 for `Δ = 6, 7, 8, 9`; 0.1 for `Δ ≥ 10`. Paid XP rounds `R_full × m` to the nearest 5 (half up). Rate = paid / (travel × mountFactor + task + complication).

**Exact test values.**

| Settings | Wolves | Ogre | Letter | Old bones | Smuggler |
|---|---|---|---|---|---|
| Level 20, no mount, no collapse | 1,800 / 225.0 | 4,200 / 182.6 | 900 / 225.0 | 800 / 100.0 | 3,000 / 214.3 |
| Level 17 | 1,800 / 225.0 | 4,200 / 182.6 | 900 / 225.0 | 2,000 / 250.0 | 3,000 / 214.3 |
| Level 25 | 1,440 / 180.0 | 4,200 / 182.6 | 540 / 135.0 | 200 / 25.0 | 3,000 / 214.3 |
| Level 30 | 180 / 22.5 | 1,680 / 73.0 | 90 / 22.5 | 200 / 25.0 | 300 / 21.4 |
| Level 20, mount | 257.1 | 227.0 | 257.1 | 123.1 | 260.9 |
| Level 20, collapse | — | — | — | — | 3,000 / 166.7 |

(Cells are "XP paid / XP per minute" or just XP per minute.)

- Required reward for the Smuggler's cave with collapse at level 20, `r₀ = 200`: 3,600.
- Required reward for the ogre's tithe at level 20: `200 × 23 = 4,600`.
- Required reward for the Smuggler's cave at level 27 (no collapse): 4,665, because 4,665 × 0.6 = 2,799 rounds to 2,800 = 200 × 14.

**Accessibility.** All controls native and labelled; bars are focusable buttons with `aria-label` such as "Old bones, paid 800 XP, 100 XP per minute, below baseline". Pass or fail uses an icon and text as well as colour. Sorting changes animate over 300 ms, disabled under `prefers-reduced-motion`.

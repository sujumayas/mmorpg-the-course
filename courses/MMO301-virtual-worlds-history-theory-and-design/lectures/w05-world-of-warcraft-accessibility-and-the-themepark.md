# MMO301 · Week 05 — World of Warcraft: Accessibility and the Themepark

**Why this matters:** World of Warcraft took EverQuest's structure, levels then groups then raids, and removed most of the ways it could hurt or stall a player. The result reached millions of people who had never played an MMO. Every accessibility decision also removed something that had made the older worlds feel dangerous and social. When you design a world you will make the same trades, so you need to see exactly what each one costs.

**You will be able to:**
- Compute net progress per hour under a death penalty, and the death rate at which a player stops progressing or goes backward.
- Rewrite the death rules of EverQuest, World of Warcraft, Final Fantasy XI and Old School RuneScape into one time-and-experience form and compare them.
- Explain how World of Warcraft's instances, group finders and lockouts lowered the coordination cost of group play, and what each removed.
- Define the themepark model and critique a design by naming which barriers it removes and what those barriers were doing.

**Before class:** Bartle, *Designing Virtual Worlds* (2003), chapter 5, "Advancement" (pp. 466-470) and "Consequences" through "Alternatives to Permanent Death" (pp. 549-563). Warcraft Wiki, "Death (gameplay)" and "Patch 1.1.0" (the general changes list), about 15 minutes together.

**Prerequisites from earlier courses:** [GS101 week 10, World of Warcraft and the mass-market MMO](../../GS101-history-and-critical-study-of-games/lectures/w10-world-of-warcraft-and-the-mass-market-mmo.md) covers WoW's release, its subscriber curve, quests as the levelling path and the rested system as history. This lecture does not repeat them. [GD102 week 2, stocks and flows](../../GD102-systems-design-and-game-mechanics/lectures/w02-stocks-and-flows.md) models the rested pool. [GD102 week 10, emergence vs progression](../../GD102-systems-design-and-game-mechanics/lectures/w10-emergence-vs-progression.md) gives the vocabulary for authored and systemic content. [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md) is used throughout. This course: [week 4, EverQuest](w04-everquest-the-treadmill-and-the-raid.md), for the treadmill, contested spawns and EverQuest's death rules.

**Interactive:** [The price of dying](../examples/w05-death-penalty.html). Keep it open during section 2.

---

## 1. Accessibility as barrier removal

"Accessible" is used loosely. In this course it has a narrow meaning. A design is more **accessible** when fewer players are stopped, slowed or pushed backward by things other than their own choices. Every MMO has barriers of four kinds.

- **Entry barriers.** Hardware, price, learning the interface, finding out what to do next.
- **Risk barriers.** What you can lose. Experience, items, time, a character.
- **Coordination barriers.** What you need other people for, and how hard it is to get them together at the right time.
- **Contention barriers.** What other players can take from you, as in week 4's contested spawns.

GS101 week 10 covered WoW's entry barriers, the quest path, modest hardware and the rested bonus that turned a pacing limit into a reward. This lecture takes the other three. The worked example is about risk, because it is the one where a small rule change has the biggest effect, and because WoW changed it a few weeks before launch.

### A term: the themepark

Players and designers call WoW's model a **themepark**. The world is a set of authored rides. Quests lead you from zone to zone in a planned order, dungeons are private copies built for a group of a fixed size, and raids reset on a timer. The designer controls the experience of each ride. The opposite model, the **sandbox**, gives players systems and lets them make their own goals. Week 6 studies EVE Online as a sandbox, and week 7 compares the two directly. For now, notice that "themepark" describes where content comes from (the designer, authored in advance), not whether it is easy.

## 2. Worked example: the price of dying

### The hook

In EverQuest's classic era, dying from level 5 onward cost experience, and enough deaths could take you down a level. Your items stayed on your corpse, and you had to go back to it, often through the monsters that had just killed you. A cleric's Resurrection spell returned 90% of the lost experience, if one was available within 3 hours.

World of Warcraft went through the beta with a softer rule. If you chose to be revived at a spirit healer instead of walking back to your body, you lost experience. Then, in patch 1.1.0, the North American release version dated 7 November 2004, Blizzard removed that experience loss. From then on, death in WoW cost time and gold, never progress. On death your equipped items lose 10% durability, and you run back to your body as a ghost. The spirit healer shortcut added more durability loss and a short weakness called resurrection sickness.

That sounds like a small change to a single rule. Model it and you find it is the difference between a world where you can go backward and a world where you cannot.

### The model

Let:

- `g` be your progress rate while playing, in levels per hour.
- `λ` (lambda) be your death rate, in deaths per hour.
- `t` be the time a death costs you, in hours (running back, recovering a corpse, resting to full health).
- `x` be the experience a death costs you, in levels.

In one hour you lose `λ × t` hours to deaths, so you play for `1 − λ × t` hours and lose `λ × x` levels. Net progress per hour is:

```
P = g × (1 − λ × t) − λ × x
```

Set `P = 0` to find the **break-even death rate**, the rate at which a player stops making progress:

```
λ* = g / (g × t + x)
```

And the share of your play time that deaths erase is:

```
waste = 1 − P / g = λ × (t + x / g)
```

Look at the case `x = 0`. Then `λ* = 1 / t`. With a 3-minute runback, `t = 0.05` hours, so you would need to die 20 times an hour, spending every minute running back, before you stopped progressing. And `P` can never go below zero. A time-only penalty slows you down. It cannot push you back.

With `x > 0`, the second term subtracts directly from progress, and `λ*` can be a rate a real player reaches on a bad evening. Above it, `P` is negative. You end the session behind where you started.

### Numbers you can check

The rules above are documented. The parameter values in this table are assumptions chosen for the example, so you can check the arithmetic. Take `g = 0.25` levels per hour (a level every four hours).

- **Time-only penalty (WoW after patch 1.1.0):** `t = 0.05` hours (3 minutes of runback), `x = 0`.
- **Time and experience (EverQuest classic):** `t = 1/3` hour (20 minutes to recover a corpse and rest), `x = 0.1` level per death. The Project 1999 Wiki describes the loss as a share of the previous level's experience without giving a fixed figure, so 0.1 is illustrative.

| Deaths per hour `λ` | `P`, time only | `P`, time and experience | Waste, time and experience |
|---|---|---|---|
| 0 | 0.250 | 0.250 | 0% |
| 0.25 | 0.247 | 0.204 | 18% |
| 0.5 | 0.244 | 0.158 | 37% |
| 1 | 0.238 | 0.067 | 73% |
| 2 | 0.225 | −0.117 | 147% |

Check the `λ = 1` row for the experience penalty by hand. `0.25 × (1 − 1/3) − 1 × 0.1 = 0.1667 − 0.1 = 0.0667`. Waste is `1 × (1/3 + 0.1/0.25) = 0.333 + 0.4 = 0.733`.

The break-even rates are:

```
time only:            λ* = 1 / 0.05 = 20 deaths per hour
time and experience:  λ* = 0.25 / (0.25 × 1/3 + 0.1) = 0.25 / 0.1833 ≈ 1.36 deaths per hour
```

One death an hour costs the WoW player 5% of their session. It costs the EverQuest player nearly three quarters. Two deaths an hour and the EverQuest player is going backward.

Now add a cleric. Resurrection returns 90% of the loss, so `x` falls to 0.01, and the corpse run disappears, so `t` falls to, say, 0.1 hours. At `λ = 1`, `P = 0.25 × 0.9 − 0.01 = 0.215`. The penalty almost vanishes, but only if someone in your group can cast the spell. EverQuest's harsh rule made the healer a person you needed, not a convenience. That is the social half of the design.

### A visual you can move

Open `examples/w05-death-penalty.html`. The left panel plots net progress `P` against death rate `λ` from 0 to 3. The time-only line slopes gently and never crosses zero on the chart. The experience line crosses zero at `λ*`, marked with a vertical rule, and the region below zero is shaded "going backward." The right panel simulates a three-hour session with deaths arriving at random at rate `λ`. It draws your level over time for both rules on the same seed. The time-only trace is a staircase with short flat steps. The experience trace is a saw, with drops at each death. Push `λ` past `λ*` and the saw ends lower than it started.

Toggle "resurrection available" to see the cleric's effect. Move `x` to zero and the two lines merge.

### Cross-game recognition

Every death rule in an MMO can be written as a pair `(t, x)`, plus any items or currency lost. Rewrite each case below into that form.

**Final Fantasy XI (current rules).** BG Wiki says death costs experience, that no experience is lost at level 30 or lower or when knocked out inside a city, that repeated losses can take a character down a level, and that a Raise spell restores part of the loss. So `x = 0` for the first 30 levels, then `x > 0`. The rule protects new players and applies the risk only once they know the game. In the model, `λ*` is infinite early and finite later.

**Old School RuneScape (current rules).** Dying to a monster puts most of your unprotected items in a grave at the death location. You can reclaim them for a fee within 15 minutes, after which they go to an NPC and cost more to recover. Your 3 most valuable items are kept. Experience is never lost, so `x = 0`. The penalty is `t` (the run back) plus a coin fee, and the risk of losing items if you do not get back in time. MMO401 week 10 treats this as an economic sink; see [MMO401 week 10](../../MMO401-virtual-economies-ii-markets-governance-and-macr/lectures/w10-scarcity-by-design-full-loot-and-destruction.md).

**Hardcore modes.** Old School RuneScape's Hardcore Ironman accounts lose that status after one unsafe death, as GD101 week 3 describes. Here `x` is the whole character's special status, and `λ*` is effectively zero. Players who choose these modes are choosing the far end of the same line on purpose. See [GD101 week 3](../../GD101-introduction-to-game-design/lectures/w03-resources-conflict-boundaries-outcome.md).

**World of Warcraft over time.** Patch 1.1.1 (17 November 2004) cut spirit healer durability loss to 25% and limited resurrection sickness to ten minutes. Patch 10.0.0 set resurrection sickness to one minute and spirit healer durability loss to 50%. Each change moves cost between `t` (sickness is time) and gold (durability is a repair bill). None puts experience back.

Four games, one form. Name `t` and `x` before arguing about whether a death penalty is "harsh."

### Eyes-open design judgment

- **What an experience penalty buys.** Caution, and the social ties that caution creates. If death can push you backward, you group up, you value a healer, you learn an area before you push into it. EverQuest's world felt dangerous because it was, in the only currency players cared about.
- **What it costs.** Players who die more, usually new or less skilled ones, lose the most. A bad evening can erase a good one. Players with less time feel it most, because the same `x` is a bigger share of a short week.
- **What a time-only penalty buys.** Progress is monotonic. You can always log off ahead of where you logged on. That is a strong promise to a player with 45 minutes, and it is the promise WoW's other decisions support.
- **What it costs.** Death stops mattering much. Designers then need another source of tension, often difficulty in instanced content, where the penalty is a failed attempt instead of lost progress.
- **Decide on purpose.** Choose `λ*` for the players you want. If you want new players never to go backward, set `x = 0` for early levels, as Final Fantasy XI does. If you want danger to shape behavior, make sure a player can see `x` before they risk it.

### Check yourself (worked example)

1. A player progresses at `g = 0.5` levels per hour. Deaths cost `t = 0.1` hours and `x = 0.05` levels. Compute `λ*`. What is `P` at two deaths per hour?
2. A designer wants an experience penalty in which a player who dies once an hour still keeps at least half their progress, with `g = 0.25` and `t = 0.1`. What is the largest `x` allowed?
3. Rewrite this rule into `(t, x)` form. "On death you respawn instantly at the zone entrance, lose 5% of your current level's experience and keep all items. Experience loss applies only at level 20 and above."

<details>
<summary>Answers</summary>

1. `λ* = 0.5 / (0.5 × 0.1 + 0.05) = 0.5 / 0.1 = 5` deaths per hour. At `λ = 2`, `P = 0.5 × (1 − 0.2) − 2 × 0.05 = 0.4 − 0.1 = 0.3` levels per hour.
2. Need `P ≥ 0.125`. `0.25 × (1 − 0.1) − x ≥ 0.125`, so `0.225 − x ≥ 0.125` and `x ≤ 0.1` level per death.
3. `t` is the walk back from the zone entrance to where you were (plus any recovery), not zero even with an instant respawn. `x = 0.05` levels at level 20 and above, `x = 0` below. No item loss.

</details>

## 3. Lowering the coordination cost

EverQuest's group content assumed players would find each other in the world, travel to the same place and wait for the right monster. WoW kept group content and attacked each of those steps.

**Instanced dungeons.** A five-player dungeon in WoW is a private copy of the area for your group. In week 4's language, the dungeon's bosses have `G = 1` for every group. Nobody else can take your kill, camp your monster or interrupt your run. That removes contention for group content entirely.

**Raids with lockouts.** Molten Core and Onyxia's Lair, the raids available at release, held 40 players and reset on a timer. Week 4 showed that the lockout formula removes the number of competing guilds from the loot rate. A 40-player raid still needs 40 people at the same hour, so the coordination barrier remained at the top.

**The Dungeon Finder (patch 3.3.0, 8 December 2009).** A queue that builds a five-player group from players across all the realms in a battlegroup and teleports them into the dungeon. Warcraft Wiki describes it as cross-realm matchmaking. Finding four other people, agreeing on a destination and travelling there all collapse into a queue.

**The Raid Finder (patch 4.3.0, November 2011).** The same idea for raids, at a new lowest difficulty that always uses 25 players. The top of the coordination barrier came down too.

Each step made group content available to more players, more often. Each step also removed a reason to know anyone. A group formed by a queue across realms dissolves when the dungeon ends. You will probably never see those players again, so there is little reason to be polite to them or to build a reputation with them. Week 4 showed EverQuest building guilds and server politics out of scarcity and contention. WoW's finders removed the scarcity and contention for everyone who used them.

A useful way to phrase this trade is as a loss of **dependence**. A world where you depend on specific other players, a healer you know, a guild that holds a spawn rotation, has high barriers and strong ties. A world where any other player will do has low barriers and weak ties. You cannot have the lowest barriers and the strongest ties at once. You can choose where each piece of content sits.

## 4. The themepark and what it asks of the designer

Put the pieces together and you get the themepark.

- A quest path that tells every player what to do next (GS101 week 10).
- A death rule that never takes progress away (section 2).
- Group content in private copies, reached through queues (section 3).
- An endgame of raids that reset on a timer (week 4).
- A rested bonus that rewards short sessions (GD102 week 2).

Each piece removes a barrier. Together they make a world in which a player's progress depends almost entirely on their own time and skill, not on who else is online, who got there first, or bad luck at the wrong moment.

That has a cost the business can see. Authored content is consumed faster than it can be made. In GD102 week 10's terms, a themepark is mostly progression content. Each quest and dungeon is a planned sequence that a player finishes and does not need to repeat, so the designer has to keep building more of it. The treadmill from week 4 returns in a new form. Where EverQuest slowed players with scarcity, the themepark has to keep feeding them new rides. WoW answered with expansions and with raid tiers that replace each other's rewards.

It also has a cost players can feel. A world in which nothing can go wrong because of other players is also a world in which other players matter less. The players who valued EverQuest and Ultima Online for their danger and their politics noticed. When Blizzard released WoW Classic in August 2019, a recreation of the game at patch 1.12, GS101 notes that a large audience wanted the older, slower version. Patch 1.12 is still the post-1.1.0 death rule, but it predates the Dungeon Finder, the Raid Finder and most of the queues, and those barriers may be part of what those players wanted back.

## In-class activity (25 minutes)

In pairs. Materials: the model from section 2 and a calculator or spreadsheet.

1. (8 min) Design a death rule for a new MMO with levels 1 to 50. Write it as `(t, x)` for three level bands (1-10, 11-30, 31-50), plus any item or currency loss.
2. (7 min) With `g = 0.3` levels per hour, compute `λ*` for each band. Plot `P` against `λ` for the three bands on one sketch.
3. (5 min) Decide one piece of content that should depend on specific other players, and one that should use a queue. Write one sentence each on why.
4. (5 min) Swap with another pair. Find the player your partners' rule hurts most, and describe them in one sentence.

Expected output: the three-band rule, three `λ*` values, the sketch, the two content decisions, and the critique you received. Keep it for Lab 05.

## Common misconceptions

- **"WoW has no death penalty."** It has a time penalty and a gold penalty (repairs). It has had no experience penalty since the release version. The difference is that its penalty cannot push you backward.
- **"Harsher penalties make better players."** They make more cautious players, and they drive away players who die more. Whether that is "better" depends on who you want to keep.
- **"Group finders made players antisocial."** They removed the need to know the people you group with. Players then behaved as that structure rewarded. The design choice came first.
- **"Themepark means easy."** Themepark describes authored, resettable content. WoW's hardest raids at the time were very demanding. What the themepark removes is risk from other players and from bad luck, not difficulty.

## Check yourself

1. At `g = 0.25`, `t = 0.05`, `x = 0`, how many deaths per hour cut a player's progress in half?
2. EverQuest's resurrection returns 90% of lost experience. If `x = 0.12` without resurrection, what is the effective `x` with it? Using `t = 0.1` and `g = 0.25`, compute `λ*` with and without resurrection (use `t = 1/3` without).
3. A proposal says: "Remove the Dungeon Finder so players make friends." Using section 3, give one outcome the designer would get and one they probably would not want.
4. Give one reason a designer might want `x > 0` only above a certain level, with a game that does it.
5. Explain why week 4's instanced raid and this week's time-only death rule both have the same effect on the kind of promise a game can make to a player with little time.

<details>
<summary>Answers</summary>

1. `P = 0.25 × (1 − 0.05λ) = 0.125` needs `0.05λ = 0.5`, so `λ = 10` deaths per hour.
2. With resurrection, `x = 0.012`. Without: `λ* = 0.25 / (0.25/3 + 0.12) = 0.25 / 0.2033 ≈ 1.23`. With: `λ* = 0.25 / (0.025 + 0.012) = 0.25 / 0.037 ≈ 6.8` deaths per hour.
3. Players would need to know others to run dungeons, so friend lists, guilds and reputation would matter more. Players with little time, or on quiet realms and at quiet hours, would struggle to find a group and would see less content.
4. So that new players learn the game without going backward, and the risk arrives once they are invested and skilled. Final Fantasy XI loses no experience at level 30 or lower.
5. Both remove other players and bad luck from the player's progress. An instanced raid's loot rate does not depend on other guilds, and a time-only death rule never takes progress away, so the game can promise that time spent always moves you forward.

</details>

## Lab / assignment hook

[Lab 05, auditing a death rule](../labs/lab05.md). You write the death rules of three MMOs (one from this lecture, two of your choice) in `(t, x)` form with sources, simulate sessions for three player profiles, and recommend a rule for your world concept. It feeds the WoW case study in the case-studies assignment (40%) and the risk section of the world design bible.

## Sources

- Warcraft Wiki, "Patch 1.1.0" (release date 7 November 2004, listed as the North American release version). Spirit healer experience loss removed and replaced by durability loss and resurrection sickness; 10% durability loss on death.
- Warcraft Wiki, "Patch 1.1.1" (17 November 2004) and "Resurrection Sickness" (patch history: limited to ten minutes and durability loss reduced to 25% in 1.1.1; one minute and 50% in 10.0.0).
- Warcraft Wiki, "Death (gameplay)" (current). Ghost form at the nearest graveyard; automatic spirit release after 6 minutes; 10% durability loss on equipped items per death.
- Warcraft Wiki, "Spirit Healer" (current). 50% durability loss to all items; one minute of resurrection sickness at level 11 and above.
- Warcraft Wiki, "Dungeon Finder" and "Patch 3.3.0" (8 December 2009). Cross-realm matchmaking for five-player dungeons within a battlegroup.
- Warcraft Wiki, "Raid Finder" and "Patch 4.3.0" (November 2011). Introduced with Dragon Soul; always 25 players; lowest raid difficulty.
- Warcraft Wiki, "Molten Core" and "Onyxia's Lair (Classic)". 40-player raids available at release; Molten Core one-week lockout.
- Project 1999 Wiki, "Experience", "Corpse" and "Resurrection" (classic-era recreation of EverQuest, 1999 to 2001 rules). Experience loss from level 5 with level loss possible; corpse decay after 7 days; resurrection window of 3 hours; Resurrection restores 90% of lost experience.
- BG Wiki, "Experience Points" (Final Fantasy XI, current). No experience lost at level 30 or lower or inside cities; level loss possible; Raise restores part of the loss.
- Old School RuneScape Wiki, "Items Kept on Death" (current). Three most valuable items kept; unprotected items go to a grave reclaimable for a fee within 15 minutes, then held by an NPC at a higher fee.
- Wikipedia, "World of Warcraft Classic" (accessed September 2026). Released 26 August 2019, recreating patch 1.12.
- Bartle, R. (2003). *Designing Virtual Worlds*. New Riders.

## Interactive spec: examples/w05-death-penalty.html

**Insight the visual must make obvious:** a death penalty paid only in time slows progress but can never make it negative; any experience penalty creates a death rate above which the player goes backward, and that rate can be low enough for a real player to hit.

**Layout.** Two panels side by side at 1280px, stacked at 390px. Left: "Net progress per hour" line chart. Right: "A three-hour session" trace. Controls above at 1280px, between the panels at 390px. Number panel below.

**Left panel.**
- x axis: deaths per hour `λ`, 0 to 3. y axis: `P` in levels per hour, from `−g` to `g`.
- Line A "Time only": `P = g × (1 − λ × t_A)` with `x = 0`.
- Line B "Time and experience": `P = g × (1 − λ × t_B) − λ × x_B`, where resurrection (when on) sets `x_B_eff = x_B × (1 − 0.9)` and `t_B_eff = t_res`.
- Shade `P < 0` and label it "going backward". Vertical rule at `λ*_B = g / (g × t_B_eff + x_B_eff)` with its value printed. If `λ*_A` is within the axis, mark it too; otherwise print "λ* = 1 / t_A = N (off chart)".
- A draggable or keyboard-movable cursor at the current `λ` that sets the right panel's rate.

**Right panel.** Simulate 180 minutes in 1-minute steps. Deaths arrive as a Poisson process at rate `λ` per hour (probability `λ / 60` per minute), using a seeded generator (seed 7; "new seed" button). Both rules use the same death times. While alive, level rises by `g / 60` per minute. At each death, rule A pauses progress for `t_A × 60` minutes; rule B subtracts `x_B_eff` immediately and pauses for `t_B_eff × 60` minutes. Deaths that fall during a pause are skipped. Plot level (starting at 10.0) against minutes for both rules. Print the end level of each and the number of deaths.

**Controls.**
- `g`: 0.05 to 1.0 levels per hour, step 0.05, default 0.25.
- `λ`: 0 to 3 deaths per hour, step 0.05, default 1.
- `t_A`: 0 to 0.5 hours, step 0.01, default 0.05.
- `t_B`: 0 to 1 hour, step 0.01, default 0.33.
- `x_B`: 0 to 0.3 levels, step 0.01, default 0.10.
- "Resurrection available" toggle (default off). When on, `x_B_eff = 0.1 × x_B` and `t_B_eff = t_res`, with `t_res` slider 0 to 0.5, default 0.1.
- Presets: "WoW after 1.1.0 vs EverQuest classic" (defaults), "With a cleric" (resurrection on), "FFXI below level 30" (`x_B = 0`). Label parameter values as assumptions; only the rule structure is sourced.

**Number panel.** `P_A`, `P_B`, `λ*_A`, `λ*_B`, waste `λ × (t + x / g)` for both, all to 3 decimals, plus the one-line formula for each.

**Test values.**
- Defaults (`g = 0.25`, `t_A = 0.05`, `t_B = 1/3`, `x_B = 0.1`): at `λ = 0, 0.25, 0.5, 1, 2`, `P_A = 0.250, 0.247, 0.244, 0.238, 0.225` and `P_B = 0.250, 0.204, 0.158, 0.067, −0.117`. `λ*_A = 20`, `λ*_B = 1.364`. Waste at `λ = 1`: A 5.0%, B 73.3%.
- Resurrection on, `t_res = 0.1`: `x_eff = 0.01`; at `λ = 1`, `P_B = 0.215`.
- `g = 0.5`, `t = 0.1`, `x = 0.05`: `λ* = 5`; `P` at `λ = 2` is 0.300.

**Style and accessibility.** Tokens from `templates/interactive-tokens.css`. Line A solid, line B dashed, so they differ without color. The session traces carry direct text labels. All controls keyboard operable; the λ cursor moves with arrow keys. Respect `prefers-reduced-motion` (draw the session trace at once instead of animating). No game art or logos.

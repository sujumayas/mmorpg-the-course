# MMO303 · Week 08 — Crowd Control and Diminishing Returns

**Why this matters:** Crowd control takes away the other player's turn. Used once, it is a tactic. Chained without limit, it is a loss the victim watches from the floor. The rule that stops chains, diminishing returns, is a small formula with a large effect on which classes and team compositions are viable in PvP.

**You will be able to:**
- Compute the total control time of a chain of crowd control effects under a diminishing-returns (DR) rule, and the maximum control uptime a DR rule allows.
- Order a chain of effects to maximize (or, as the victim, minimize) total control, and prove the ordering rule.
- Compare DR, tenacity-style duration reduction and break bars, and predict what each does to class design.
- Design a DR rule for a new game and state the uptime ceiling it implies.

**Before class:** Schreiber & Romero, *Game Balance* (2021), chapter 10 (Combat) and the chapter on situational balance; skim Warcraft Wiki's "Diminishing returns" article, including its patch history.

**Prerequisites from earlier courses:** [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md) and the geometric series from [MA101 week 4, exponentials](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md). [GD203 week 4, time-to-kill](../../GD203-combat-and-progression-design/lectures/w04-time-to-kill-and-time-to-die.md). From this course, [week 2](w02-armor-and-damage-mitigation.md) (multiplicative layers), [week 4](w04-stacking-mitigation-multiplicative-layers.md) (stacking mitigation) and [week 6](w06-threat-aggro-and-control.md) (threat, aggro and control).

**Interactive:** [CC diminishing returns](../examples/w08-cc-diminishing-returns.html). Keep it open during section 2.

---

## 1. What crowd control is, and why it needs a brake

**Crowd control (CC)** is any effect that stops or limits a target's actions for a time. The common kinds:

- **Stun**: the target can do nothing.
- **Incapacitate** or **sleep**: the target can do nothing, but damage usually breaks the effect.
- **Disorient** or **fear**: the target moves without control.
- **Root**: the target cannot move but can still act.
- **Silence**: the target cannot cast spells.
- **Slow**: the target moves more slowly.

Last week you measured healing as a rate. CC is also a rate, but of something scarcer. It removes the target's **agency**, their ability to make choices. Damage lowers a health bar the target can respond to. A stun lowers a clock the target can only watch.

Week 6 used CC as a PvE tool: sheep one enemy, fight the rest. In PvE the target is a script and nobody minds that it stood still. In PvP the target is a person. A rogue who can stun you for ten seconds, and then again, and then again, has turned a fight into a cutscene.

Three things make CC hard to balance.

1. **CC multiplies damage.** A stunned healer does not heal, so every second of stun on a healer is a second of full enemy DPS against an unhealed team. CC's value depends on who you use it on.
2. **CC is binary per second.** You are either stunned or not. There is no "20% stunned". Small duration changes flip outcomes, such as whether you survive until your cooldown comes back.
3. **CC chains.** Several players, or one player with several abilities, can apply effects back to back. Chain length grows with team size, not with the power of any single ability.

The third problem is what diminishing returns solve.

## 2. Worked example: 100%, 50%, 25%, immune

### The hook

In World of Warcraft PvP, from a 2015 Warlords of Draenor hotfix through The War Within expansion, getting stunned three times in a row gave you a full-length stun, then a half-length stun, then a quarter-length stun. A fourth stun did nothing. The target was immune. Eighteen seconds after the last stun wore off, the counter reset and the next stun was full length again.

Players call this "DR" and many think of it as "stuns get weaker". That reading misses the point. DR is a cap on total control, and the cap has a size you can compute. Once you know it, you can say exactly how much of a fight one team can spend controlling one enemy.

### The model

Group CC effects into **DR categories**. In the WoW era above, all stuns share one category, all roots another, and there are separate categories for incapacitates, disorients, silences and a few others. Effects in different categories do not affect each other's DR.

Within one category, the `k`-th application of CC on the same target lasts

```
duration_k = m_k × d_k
```

- `d_k` is the base duration of the `k`-th effect (what the tooltip says).
- `m_k` is the DR multiplier for the `k`-th application. In the WoW era above, `m = (1, 0.5, 0.25, 0)`. The zero means immune.
- The counter `k` resets to 1 when `R` seconds pass after the last effect in the category ends. In that era, `R = 18`.

If every effect has the same base duration `d` and the chain stays inside the reset window, total control before immunity is

```
total = d × (1 + 0.5 + 0.25) = 1.75 × d
```

The maximum uptime, the fraction of time a target can spend controlled by one category, comes from a cycle. The attackers spend `1.75 d` seconds controlling. Then the target is immune until `R` seconds pass after the last effect ends. Then the cycle repeats:

```
uptime ≤ 1.75 d / (1.75 d + R)
```

Without DR, uptime is limited only by cooldowns and could reach 100%. With DR it has a ceiling set by two numbers, the multiplier sum and the reset window.

### Numbers you can check

Take a generic 6-second stun (base duration `d = 6`) and the WoW-era rule, `m = (1, 0.5, 0.25, 0)`, `R = 18`.

| Application | Multiplier | Duration | Total control so far |
|---|---|---|---|
| 1st | 1.00 | 6.0 s | 6.0 s |
| 2nd | 0.50 | 3.0 s | 9.0 s |
| 3rd | 0.25 | 1.5 s | 10.5 s |
| 4th | 0 (immune) | 0.0 s | 10.5 s |
| 5th and later, within R | 0 | 0.0 s | 10.5 s |

Uptime ceiling: `10.5 / (10.5 + 18) = 10.5 / 28.5 = 36.8%`.

Now do the same for other base durations:

| Base duration d | Total before immune (1.75 d) | Uptime ceiling, R = 18 |
|---|---|---|
| 2 s | 3.5 s | 16.3% |
| 4 s | 7.0 s | 28.0% |
| 6 s | 10.5 s | 36.8% |
| 8 s | 14.0 s | 43.8% |

Longer effects raise the ceiling, but slowly, because the reset window `R` is a fixed tax on every cycle. That is what `R` is for. A designer who wants less CC in PvP can shorten durations, or lengthen `R`, and the second hits every ability at once.

### Chain-stun math: order matters

Now give the attacking team three different stuns in one category. Call them Stun A (6 s), Stun B (4 s) and Stun C (3 s). All three land inside the reset window. The total depends on the order:

| Order | 1st (×1) | 2nd (×0.5) | 3rd (×0.25) | Total |
|---|---|---|---|---|
| A, B, C (longest first) | 6.0 | 2.0 | 0.75 | 8.75 s |
| A, C, B | 6.0 | 1.5 | 1.0 | 8.5 s |
| B, A, C | 4.0 | 3.0 | 0.75 | 7.75 s |
| B, C, A | 4.0 | 1.5 | 1.5 | 7.0 s |
| C, A, B | 3.0 | 3.0 | 1.0 | 7.0 s |
| C, B, A (shortest first) | 3.0 | 2.0 | 1.5 | 6.5 s |

Longest first beats shortest first by 2.25 seconds, about a third more control from the same three buttons. The rule is general. The multipliers fall, so you want the biggest durations paired with the biggest multipliers. This is the **rearrangement inequality**: a sum of products `Σ m_k × d_k` is largest when both lists are sorted the same way and smallest when they are sorted in opposite ways. The victim's side follows too. If you can choose when to take a stun (for example, by using an immunity or a CC-break ability on the long one), spend it on the effect that would land at multiplier 1.

A second chain question: what if the team has a stun, a disorient and an incapacitate, each 6 seconds? They sit in separate categories, so each has its own DR counter:

```
total = 3 × 1.75 × 6 = 31.5 s
```

Across categories, DR does not stop chains. It stops them within a category. This is why PvP team compositions care about having CC in many categories, and why designers are careful about which category a new ability belongs to. Moving one ability from "incapacitate" to "stun" can remove a whole comp from the game.

### A visual the student can move

Open the [CC diminishing returns interactive](../examples/w08-cc-diminishing-returns.html). The top view is a 60-second timeline. Each CC application is a bar whose length is its actual duration, colored by its DR step (full, half, quarter, immune). The shaded band after each bar is the reset window. Drag the cast times or change the base durations and the bars recompute.

The bottom view plots total control time against the number of applications. It climbs, bends and goes flat at `1.75 d`. Next to it, the uptime gauge shows the ceiling for the current `d` and `R`.

Try three things. First, press "Longest first" and "Shortest first" and watch the total change. Second, slide the gap between casts past `R` and watch the fourth bar jump back to full length. Third, switch the era preset from "WoW, 2015 to The War Within" to "No DR" and watch the flat line in the bottom view become a straight climb. The timeline looks almost the same in both presets. The totals do not.

### Cross-game recognition

**World of Warcraft, across eras.** The same model covers every version with different parameters. According to Warcraft Wiki, Classic servers reset DR dynamically somewhere between 15 and 20 seconds instead of a fixed 18. The Midnight expansion changed it twice. Patch 12.0.0 (January 20, 2026) made players in PvP immune after two applications in a category instead of three and cut the reset window from 18 to 16 seconds. Patch 12.1.0 (August 11, 2026) raised the window to 20 seconds, which is the current value as of September 2026. Blizzard's stated reason was to keep reducing the time players spend out of control of their characters. Plug those in. With `m = (1, 0.5, 0)` and `R = 16`, a 6-second stun gives 9 seconds of control and a ceiling of `9 / 25 = 36%`. With `R = 20` the ceiling is `9 / 29 = 31.0%`. Warcraft Wiki also notes that DR against NPCs usually applies only to stuns and taunts, and a Midnight PvE change keeps halving stun durations on NPCs down to one sixteenth of the base length instead of granting immunity. This rule changed twice in 2026, so check the current patch notes before you quote it.

**League of Legends: tenacity.** League has no DR in this sense. Instead a champion stat called **tenacity** shortens incoming CC by a percentage. It is `duration × (1 − tenacity)`. Tenacity sources are sorted into groups. Within a group they stack multiplicatively. Two item sources of 30% and 20% give `1 − 0.7 × 0.8 = 44%`, not 50%. Groups add together, tenacity caps at 100%, and no disable can be shortened below 0.3 seconds. Some effects (airborne knock-ups, suppression, stasis and a few others) ignore tenacity entirely. In our form, tenacity is a DR multiplier that is the same for every application, `m_k = 1 − tenacity` for all `k`, with no immunity step. It shortens every stun, including the first, and does nothing to stop a chain. The multiplicative stacking inside a group is the same idea as the mitigation layers from week 2, with the same result: layers never reach 100%.

**Guild Wars 2: the defiance bar.** Guild Wars 2 bosses mostly ignore CC durations. Instead, a boss with an active defiance bar takes "break damage" from CC. The wiki gives hard CC (stuns, knockdowns) break damage of 100 per second of the effect's duration, with a minimum of 25. When the group empties the bar, the boss is interrupted and usually stunned, and it gains an "Exposed" state that raises the damage it takes. Then the bar recharges, and the boss is immune to CC while it does. Rewrite it in our form. Each CC's duration is converted into a shared pool, and the pool pays out one fixed-length control window, followed by an immunity window. That is DR taken to its limit. The first several applications give zero control on their own, and the chain as a whole buys one burst of control. The design goal is the same, a ceiling on control uptime, but the rule turns CC from a solo button into a group project.

Three games, three presentations, one question. What is the most control time a group can put on one target per minute, and what sets that ceiling?

### Eyes-open design judgment

- **DR caps control, it does not balance CC.** A class whose only strength is CC still gets 1.75 d per category per cycle, and a class with CC in four categories gets four times that. Balance the number of categories a class touches, not just durations.
- **The immunity step is a design statement.** A multiplier list ending in 0 guarantees the victim a window to act. A list that halves forever (as in the Midnight PvE stun change) never grants immunity. Its first five steps total `1.9375 d`, and after that each extra application adds only `d / 16`. Immunity is cleaner for players to read. Endless halving avoids "wasted" abilities in PvE, where a boss becoming immune feels like a bug.
- **R is the most powerful knob you have.** It applies to every ability in the category at once. Changing it is a global change to PvP pacing. Blizzard changed it twice within 2026 alone, which tells you how sensitive it is.
- **DR is invisible unless you show it.** The victim cannot see which step they are on unless the interface tells them, and neither can the attacker planning a chain. Hidden state feels like randomness. Show DR state on nameplates or debuff icons, and expect competitive players to install addons if you do not.
- **Tenacity rewards investment, DR rewards timing.** Tenacity is a stat players buy, so it can be a build choice and a counter-pick. DR is a rule everyone lives under, so it shapes team play. Many games use both.
- **Categories are balance levers.** When one team comp dominates, look at whether its CC spans more categories than its rivals before you touch any durations.

## 3. The geometric series behind DR

The WoW-era multipliers `1, 0.5, 0.25` are the first three terms of a geometric series with ratio one half. If DR kept halving forever, the total would be

```
d × (1 + 1/2 + 1/4 + 1/8 + ...) = d × 1 / (1 − 1/2) = 2 d
```

So stopping at the third step and making the fourth zero only costs the attacker `0.25 d` compared with infinite halving. The immunity step is not mainly about total control. It is about the number of button presses. With halving forever, a team could spend 20 abilities to gain almost nothing, and the victim would be locked in a flicker of tiny stuns. The immunity step says "stop", and players can read it.

Change the ratio and the ceiling changes. With ratio `q`, infinite halving totals `d / (1 − q)`. A game using `q = 0.65` (duration cut by 35% per step) reaches a ceiling of `d / 0.35 ≈ 2.86 d`, much higher. Warcraft Wiki records that for taunts, patch 3.3.0 used a 35% reduction per application with immunity only after five taunts. A taunt is a CC aimed at a script, and designers were willing to let tanks stack a lot of it.

## 4. CC and time-to-kill

CC matters because of what happens during it. Put the numbers from GD203 week 4 to work. Say the attacking team deals 1,500 DPS to a target with 20,000 EHP. Time-to-kill is 13.3 seconds. If the target can heal themselves at 600 HPS whenever they are not controlled, their effective damage intake during free time is `1,500 − 600 = 900`, and the TTK depends on how much of the fight they spend controlled.

Let `u` be the fraction of time controlled. Average net damage is `1,500 × u + 900 × (1 − u) = 900 + 600 u`. At `u = 0` the TTK is 22.2 seconds. At the WoW-era ceiling for a 6-second stun, `u = 0.368`, it is `20,000 / 1,120.8 = 17.8` seconds. With stun plus disorient plus incapacitate chained, `u` can approach 1 for the first 31.5 seconds, and the target dies in 13.3 seconds with no chance to act.

This connects CC to the healer model from week 7. A stunned healer is a healer whose HPS is zero, and CC on healers is an attack on the other team's mana and time budget at once. It is why PvP designers care more about CC on healers than on anyone else, and why many games give healers extra ways to break or resist CC.

## 5. Designing a DR rule

When you design DR for a new game, decide these explicitly:

1. **Categories.** How many, and which abilities go where. Fewer categories mean tighter caps. More mean more interesting chains and more compositions to balance.
2. **Multiplier list.** How fast it falls, and whether it ends in immunity.
3. **Reset window `R`.** Its length, and whether it starts when the CC is applied or when it ends. Starting at the end (as WoW does) keeps long effects from resetting themselves.
4. **Scope.** PvP only, PvE too, or players only. Most games spare NPC encounters from most DR because bosses are balanced around separate CC immunity rules.
5. **Presentation.** How the victim and the attacker see the current DR step.

Then compute the uptime ceiling for each category and for the whole chain, and compare them to your TTK. If a coordinated team can control a target for longer than the target's TTK, the target's class choices do not matter in that fight. That may be fine in a raid. It is not fine in a 3v3 arena.

## In-class activity (25 minutes)

In groups of three, design the DR rule for a small arena game with three classes, each with one stun (4 s), one root (5 s) and one silence (3 s).

1. Choose the categories. Put each ability in one. Justify each placement in a sentence.
2. Choose a multiplier list and `R`. Compute total control before immunity for each category, and the uptime ceiling.
3. A 2v2 team uses both players' stuns and silences on one target inside one window. What is the best order, and how long is the target unable to cast?
4. Your target TTK is 12 seconds. Does any combination let a team kill a target who never acts? If yes, change one parameter to stop it, and show the new numbers.

Expected output: one table per group of categories, multipliers, `R`, per-category ceiling, and the worst-case chain.

## Common misconceptions

- **"DR makes CC weaker."** It leaves the first application untouched. It caps the total per category per cycle, which is `1.75 d` in the WoW-era rule, and it sets an uptime ceiling that is well below 100%.
- **"Two 50% duration reductions make you immune."** Tenacity sources in the same group multiply. Two 50% sources give 75%, not 100%, just like the mitigation layers in week 2.
- **"The order of CC does not matter, it all adds up the same."** Under DR, the order changes the total. Longest first gives the most control, by the rearrangement inequality.
- **"Once immune, you are immune for 18 seconds."** In WoW the reset window starts when the last effect ends. If the last effect was a 1.5-second quarter stun, the immunity lasts about 18 seconds after that stun, not after the first stun.

## Check yourself

1. Under the WoW-era rule, a target takes a 5-second stun, then a 4-second stun, then an 8-second stun, all in one window. What is the total stun time? What order of the same three stuns would give the attackers the most, and what total?
2. A game uses `m = (1, 0.5, 0.25, 0)` and `R = 18`. What base duration `d` would give an uptime ceiling of exactly 40%?
3. A League champion builds two tenacity items from the same group, 30% and 20%, and is hit by a 2-second stun and later by a 0.5-second stun. How long does each last?
4. A designer wants to cut the maximum stun control in arena by one third without changing any ability's tooltip. Propose two ways using only the DR rule, and give the new uptime ceiling for a 6-second stun in each.

<details>
<summary>Answers</summary>

1. In the given order: `5 × 1 + 4 × 0.5 + 8 × 0.25 = 5 + 2 + 2 = 9` seconds. Longest first (8, 5, 4): `8 + 2.5 + 1 = 11.5` seconds.
2. Solve `1.75 d / (1.75 d + 18) = 0.4`. Then `1.75 d = 0.4 × 1.75 d + 7.2`, so `1.05 d = 7.2` and `d = 6.86` seconds.
3. Group tenacity is `1 − 0.7 × 0.8 = 0.44`. The 2-second stun lasts `2 × 0.56 = 1.12` seconds. The 0.5-second stun would last 0.28 seconds, but the 0.3-second floor applies, so it lasts 0.3 seconds.
4. The WoW-era ceiling for `d = 6` is 36.8%, and the target is about 24.5%. One way is to make immunity come after two applications, `m = (1, 0.5, 0)`. Total per cycle falls from 10.5 to 9 seconds, which alone gives `9 / 27 = 33.3%`. Adding a longer window reaches the target: `9 / (9 + R) = 0.245` gives `R ≈ 27.7` seconds. A second way keeps the multipliers and lengthens `R`: `10.5 / (10.5 + R) = 0.245` gives `R ≈ 32.4` seconds. Either change works. The first makes each chain shorter, the second makes cycles rarer.

</details>

## Lab hook

**Lab 08 (Chain CC planner).** Build a spreadsheet or small script that takes a list of CC abilities with categories, durations and cooldowns, applies a DR rule, and finds the chain order that maximizes control on one target in a 60-second window. Test it under three DR rules and write a 300-word recommendation. See [`labs/lab08.md`](../labs/lab08.md).

## Sources

- Warcraft Wiki, "Diminishing returns" (accessed September 2026). Full, half, quarter, then immune within one category; the window counts from the end of the effect; 18 seconds from a Warlords of Draenor hotfix in 2015; Classic resets dynamically between 15 and 20 seconds; stuns and taunts are the usual DR categories against NPCs; patch 6.0.2 merged stuns and roots into single categories; patch 3.3.0 taunt rule (35% per application, immune after five); patch 12.0.0 (2026-01-20) immunity after two applications and a 16-second window; patch 12.1.0 (2026-08-11) window of 20 seconds, quoting the patch notes; retail maximum PvP CC duration of 6 seconds.
- Maxroll, "Crowd Control Diminishing Returns 12.0.7" (accessed September 2026). Describes the Midnight PvE stun change (halving to one sixteenth instead of immunity). Its 12.0.x reset figures predate patch 12.1.0.
- League of Legends Wiki, "Tenacity" (accessed September 2026). Duration reduction, grouped multiplicative stacking, 100% cap, 0.3-second minimum, list of effects tenacity does not affect.
- Guild Wars 2 Wiki, "Defiance bar" (accessed September 2026). Break damage of 100 per second of hard CC with a minimum of 25; break interrupts and applies Exposed; recharge with CC immunity.
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press. Chapter 10 (Combat).
- All ability names and durations in the worked example (Stun A, B, C) are invented for teaching.

## Interactive spec: examples/w08-cc-diminishing-returns.html

**The one insight:** diminishing returns turn "more CC" into a ceiling. Total control in one category flattens at `(Σ m_k) × d`, and the order of a chain changes the total. The timeline looks almost the same with and without DR, and the cumulative plot shows the difference.

**Layout.** Two stacked views (timeline on top, cumulative plot below), with controls on the right on desktop and below on mobile. Number panel under the plots.

**Top view: 60-second timeline.**
- x-axis time 0 to 60 s. One lane for the target.
- Up to 6 CC applications, each drawn as a bar from cast time to cast time plus actual duration. Fill the bar by DR step: step 1 full color, step 2 medium, step 3 light, immune as an outlined zero-width marker with the label "immune".
- After each bar, a hatched band of length `R` showing the reset window. When a new cast lands after the band ends, its step resets to 1.
- Bars cannot overlap. If a cast time falls inside the previous bar, the app moves it to the moment the previous bar ends (a chain) and shows a small note.

**Bottom view: cumulative control.**
- x-axis number of applications (1 to 6), y-axis total control seconds.
- Bars for the current chain. A dashed horizontal line at the ceiling `(Σ m_k) × d_max`, labeled.
- A ghost line for the "No DR" total (sum of base durations) so the gap is visible.
- An uptime gauge showing `(Σ m_k × d) / ((Σ m_k × d) + R)` for the first effect's base duration, as a percentage.

**Controls.**
- Era preset (radio buttons):
  - "WoW, 2015 to The War Within": `m = (1, 0.5, 0.25, 0)`, `R = 18`.
  - "WoW Midnight 12.0 (per Warcraft Wiki)": `m = (1, 0.5, 0)`, `R = 16`.
  - "WoW Midnight 12.1 (per Warcraft Wiki)": `m = (1, 0.5, 0)`, `R = 20`.
  - "Halve forever": `m_k = 0.5^(k−1)` with no immunity, floor `1/16`, `R = 16`.
  - "No DR": all `m_k = 1`.
  - "Custom": editable multiplier list (up to 6 values) and `R` slider 0 to 40 s.
- For each of up to 6 applications: base duration slider (0.5 to 10 s, step 0.5) and cast time slider (0 to 60 s, step 0.5). Add and remove buttons.
- Buttons "Chain now" (each cast at the end of the previous), "Longest first", "Shortest first".
- Tenacity slider 0 to 90%, step 5, default 0. Applies `duration × (1 − tenacity)` before DR. Show a floor of 0.3 s when a "League-style floor" checkbox is on.

**Formulas.**
- For each application in cast-time order: if its cast time is later than `(end of previous application in category) + R`, reset step `k = 1`; otherwise `k = previous k + 1`.
- `actual_k = m_k × d_k × (1 − tenacity)`, with `m_k = 0` beyond the list (immune) unless the preset is "Halve forever" (then `max(0.5^(k−1), 1/16)`).
- Floor: when the checkbox is on and `actual_k > 0`, `actual_k = max(actual_k, 0.3)`.
- Total control = sum of `actual_k`.

**Number panel.** For each application: step, multiplier, actual duration, running total. Also: total control, "No DR" total, ceiling, uptime ceiling, and the best and worst ordering totals for the current durations.

**Test values.**
- WoW 2015 preset, three chained 6 s stuns: 6.0, 3.0, 1.5, total 10.5 s. Fourth application immune. Uptime ceiling 36.8%.
- Durations 6, 4, 3 chained: longest first 8.75 s, shortest first 6.5 s.
- Base 2, 4, 8 s: uptime ceilings 16.3%, 28.0%, 43.8%.
- Midnight 12.0 preset, 6 s: 6.0, 3.0, immune, total 9.0 s, ceiling 36.0%. Midnight 12.1: ceiling 31.0%.
- Chained 6 s stuns, fourth cast placed 18.5 s after the third ends: its step resets to 1 and it lasts 6.0 s.
- Tenacity 44% with a 2 s stun: 1.12 s. With the floor on, a 0.5 s stun at 44% lasts 0.3 s.

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`. DR steps must be distinguishable without color (use fill pattern or step labels "1", "½", "¼", "0"). Respect reduced motion (no animated bar growth). No game art, class icons or logos.

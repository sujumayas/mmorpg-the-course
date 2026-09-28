# MMO402 · Week 10 — Addiction, Wellbeing and Responsible Design

**Why this matters:** Every pacing system in an MMO (rested bonuses, daily quests, login rewards, energy timers) is a rule about when and how long people play. You will write those rules. Whether your world is a good place to spend time depends less on how many hours people play and more on why they feel they have to.

**You will be able to:**
- Compute the weekly reward that four pacing rules (flat, rested, fatigue, daily reward) give to players with different schedules.
- Identify which part of a player's schedule a pacing rule actually regulates: total hours, session length, or presence on a given day.
- Distinguish the clinical definitions of gaming disorder (ICD-11, DSM-5) from the everyday word "addictive", and state what the telemetry evidence says about time played and wellbeing.
- Critique a live game's pacing and reminder features against the question "can a player move their hours without losing anything?"

**Before class:** Vuorre, Johannes, Magnusson and Przybylski, "Time spent playing video games is unlikely to impact well-being," *Royal Society Open Science* 9(7), 2022, the abstract, introduction and discussion (about 25 minutes). World Health Organization, ICD-11 entry 6C51 "Gaming disorder" (one page). Reread [GD102 week 2](../../GD102-systems-design-and-game-mechanics/lectures/w02-stocks-and-flows.md), section 3, on the rested pool as a stock.

**Prerequisites from earlier courses:** [GD102 week 2, stocks and flows](../../GD102-systems-design-and-game-mechanics/lectures/w02-stocks-and-flows.md) (the rested pool as a stock with an inflow, an outflow and a cap). [GD102 week 8, core loops and meta loops](../../GD102-systems-design-and-game-mechanics/lectures/w08-core-loops-and-meta-loops.md) (daily loops sit on top of the core loop). [UX201 week 4, self-determination theory](../../UX201-game-ux-and-player-psychology/lectures/w04-self-determination-theory.md) (autonomy, and why controlling rewards feel different from informational ones). [UX201 week 5, reinforcement schedules and their ethics](../../UX201-game-ux-and-player-psychology/lectures/w05-reinforcement-schedules-and-ethics.md). [GS101 week 11, free-to-play, mobile and live service](../../GS101-history-and-critical-study-of-games/lectures/w11-free-to-play-mobile-and-live-service.md). [MMO402 week 1, worlds as polities](w01-worlds-as-polities.md) (you are the sovereign who writes these rules).

**Interactive:** [Pacing rules read different clocks](../examples/w10-pacing-rules.html)

---

## 1. What "addictive" means, and what it does not

Players, journalists and designers all call games "addictive." Most of the time they mean "I kept playing longer than I planned." That is a real experience and worth designing for, but it is not a diagnosis. Before you argue about responsibility you need the clinical terms straight, because the two meanings lead to very different design questions.

### Two clinical definitions

The **World Health Organization** added "gaming disorder" to the 11th revision of its International Classification of Diseases (ICD-11). The revision was released in June 2018, approved by the World Health Assembly in May 2019, and came into effect on 1 January 2022. The ICD-11 definition has three parts: impaired control over gaming, gaming taking priority over other interests and daily activities, and continuing despite negative consequences. The pattern must be severe enough to cause significant impairment in personal, family, social, educational or work life, and would normally have been evident for at least 12 months.

The **American Psychiatric Association** took a more cautious route. The DSM-5 (2013) lists "Internet Gaming Disorder" in Section III, as a condition requiring further study, not as an official diagnosis. It proposes nine criteria, including preoccupation with games, withdrawal when gaming is taken away, tolerance (needing more time to feel the same), failed attempts to cut down, giving up other activities, continuing despite problems, deceiving others about play, playing to escape bad moods, and risking relationships or opportunities.

Notice what neither definition contains: a number of hours. A player who raids 25 hours a week with friends, sleeps enough and keeps their job does not meet either definition. A player who plays 8 hours a week but hides it, fails at school and cannot stop might. Time is a symptom at most. The core of both definitions is loss of control and harm.

### What the telemetry says

For years most research on games and wellbeing relied on players estimating their own play time, which people do badly. In 2022, Matti Vuorre, Niklas Johannes, Kristoffer Magnusson and Andrew Przybylski linked six weeks of actual play data from 38,935 players, supplied by seven game publishers, with three waves of wellbeing surveys. They found little to no evidence that time spent playing affected wellbeing. They did find that players' motivations were associated with wellbeing. In plain terms, playing because you want to and playing because you feel you have to are different experiences, even at the same number of hours.

That finding lines up with self-determination theory from UX201 week 4. Rewards that feel like control ("log in or lose your streak") undermine autonomy. Rewards that feel like information ("you got better") support it. It also gives you, the designer, a sharper question than "is my game too engaging?" Ask instead: **which of my rules create obligation?** Obligation is something you build on purpose or by accident, and you can measure it.

### Why this is a governance question

In week 1 you saw that the developer is the sovereign of its world. Pacing rules are that sovereign's labor law. They decide how the world rewards a long shift against a short one, a daily visit against a weekly one, a player who takes a vacation against one who never leaves. Real governments have also written these rules directly. China's regulators have imposed play-time rules on online games since 2007, and you will study the version aimed at minors in week 11. Whether you like those rules or not, they show that "how long should people play" is treated as public policy, and that developers who do not decide will be told.

## 2. Worked example: rested, tired, or on time?

### The hook

In the World of Warcraft beta, according to the Warcraft Wiki's account of the rest system, experience was designed to stop players from playing more than a few hours in a row: after a few hours, experience gains were cut by half. Testers hated it. The developers flipped the framing. Normal gain became the "tired" rate, and the old full rate became a 200% "rested" bonus that builds up while you are offline. The wiki describes it as the same numbers seen from the opposite point of view. Players loved it, and rested experience has been in the game ever since.

Here is the surprise. The two versions are not actually the same rule. One of them regulates how long you play in a sitting. The other barely does. By the end of this example you will be able to say which, and by how much.

### The model

Measure all experience in percent of a level. Assume a level takes 10 hours of play at the normal rate, so the **base rate** is `b = 10%` of a level per hour. (This base rate is invented to keep the arithmetic clean. The rested numbers that follow are World of Warcraft's.)

Compare four pacing rules. Each takes a player's weekly schedule and returns the experience they earn.

1. **Flat.** Every hour earns `b`. No pacing at all.
2. **Rested (World of Warcraft, current retail).** While logged off in an inn or capital city, a character builds a rested pool at one "bubble" (10% of a level) per 16 hours, which is 5% of a level per 8 hours, or `a = 0.625%` of a level per hour. The pool caps at 150% of a level. While the pool is above zero, kill experience is doubled, and the bonus is taken out of the pool. So an hour of play earns `b + min(pool, b)`.
3. **Fatigue (modeled on China's 2007 system).** Within one day, the first 3 hours earn `b`, hours 3 to 5 earn `b/2`, and hours after 5 earn nothing. (The real system counted cumulative online time. Resetting it each day is our simplification.)
4. **Daily reward.** Every hour earns `b`, plus a one-time bonus `d = 10%` of a level the first time you log in each day. This stands in for daily quests, login calendars and first-win-of-the-day bonuses.

The weekly total for a rested player has a closed form, as long as the pool never hits its cap and is used up by the end of each session. Let `H` be hours played per week. The pool fills during the `168 − H` hours offline and empties into bonus experience:

```
weekly rested bonus = min( a × (168 − H),  b × H )
                    = min( 0.625 × (168 − H),  10 × H )
```

The first term is how much rest you can bank in a week. The second is how much bonus you can spend, since the bonus can never exceed your base gain. The two are equal at `H ≈ 9.9` hours. Below that, every hour you play is doubled. Above it, the bonus is capped by the bank and actually shrinks slowly as you play more, because you spend fewer hours offline.

### Numbers you can check

Four players. Three of them play the same 14 hours a week, arranged differently. The fourth is a light player.

- **Light:** 2 hours on Saturday and Sunday (4 hours a week).
- **Daily:** 2 hours every evening (14 hours).
- **Weekend:** 7 hours on Saturday and Sunday (14 hours).
- **Binge:** one 14-hour session on Sunday (14 hours).

Weekly experience, in percent of a level:

| Schedule | Hours | Flat | Rested | Fatigue | Daily reward |
|---|---|---|---|---|---|
| Light, 2 h × 2 days | 4 | 40 | 80 | 40 | 60 |
| Daily, 2 h × 7 days | 14 | 140 | 236.25 | 140 | 210 |
| Weekend, 7 h × 2 days | 14 | 140 | 236.25 | 80 | 160 |
| Binge, 14 h × 1 day | 14 | 140 | 236.25 | 40 | 150 |

Check three cells by hand.

**Rested, daily.** Between sessions the player is offline 22 hours and banks `22 × 0.625 = 13.75`. Each 2-hour session earns 20 base plus 13.75 bonus. Over 7 days that is `7 × 33.75 = 236.25`.

**Rested, binge.** The player is offline 154 hours and banks `154 × 0.625 = 96.25`, under the 150 cap. The session earns 140 base, and the first 96.25 of that is matched by bonus. Total `140 + 96.25 = 236.25`. Identical to the daily player. The closed form agrees: `min(0.625 × 154, 10 × 14) = 96.25`.

**Fatigue, weekend.** Each 7-hour day earns 3 full hours (30), 2 half hours (10) and 2 empty hours (0), so 40 a day and 80 a week.

### What each rule regulates

Read the table by columns, not rows.

- **Rested does not care how you arrange your hours.** The three 14-hour players get exactly the same total. What rested experience regulates is *total* play. The light player gets double the flat rate (80 against 40), while the 14-hour players get 1.69 times the flat rate. Rested experience is a catch-up mechanism: it compresses the gap between light and heavy players. It is not a session-length limit, and it never was, even though it grew out of one.
- **Fatigue punishes long sessions hard.** The binge player earns 40, less than a third of the daily player's 140, for the same hours. Fatigue regulates *session length* and nothing else.
- **Daily rewards regulate presence.** The daily player earns 210, 40% more than the binge player's 150 for the same time. The rule does not care how long you play. It cares whether you showed up today.

So the beta story is half right. The fatigue version and the rested version do use "the same numbers" in the sense that one is the other with the labels swapped: normal-and-halved against doubled-and-normal. But the pool in the rested version fills from time offline, not from time since your session started. That one change turned a rule about session length into a rule about total hours. Players did not only prefer the friendlier label. They got a different rule.

### The obligation test

Now apply this lecture's question: which rule creates obligation? A simple test is to ask what happens when a player's life gets in the way.

The daily player skips Wednesday and plays 4 hours on Thursday instead. Same total hours, one day moved. What does it cost?

| Rule | Loss from moving Wednesday's hours to Thursday | Can the player avoid the loss without adding a day? |
|---|---|---|
| Flat | 0 | Nothing to avoid |
| Rested | 0 (Thursday's pool is 28.75 instead of 13.75, and it all gets spent) | Nothing to avoid |
| Fatigue | 5 (Thursday's 4th hour is half rate) | Yes, by playing 3 h Thursday and 3 h Friday |
| Daily reward | 10 (Wednesday's bonus is gone) | No. Only by logging in on Wednesday |

Check the rested row. Offline from Tuesday's session end to Thursday's start is `22 + 24 = 46` hours, which banks 28.75. Thursday's 4 hours earn 40 base plus 28.75 bonus. Friday's pool is smaller than usual, because only 20 hours pass between Thursday's session end and Friday's start (12.5 instead of 13.75). Add Wednesday to Friday together and you get `0 + 68.75 + 32.5 = 101.25`, exactly what three normal days give (`3 × 33.75`).

The daily reward is the only rule of the four whose loss you cannot avoid by rearranging the same hours. That is the mechanical signature of obligation. It is small here, 10 out of 210, about 5% of the week. Stack a streak multiplier on top (rewards that grow for each consecutive day and reset when you miss one) and the cost of a missed day can grow without limit. Players describe this as feeling they "have to" log in, and the 2022 telemetry study suggests that feeling, not the hours, is what tracks with lower wellbeing.

Open the interactive. The left view shows the reward rate for each hour of the week as a strip, colored by rule. The right view plots weekly experience against total hours for all four rules, with a dot for the current schedule. Drag the session-length slider with the weekly hours locked at 14. The rested line on the right does not move. The fatigue dot falls. Then drag "days per week" and watch the daily-reward dot climb while every other rule holds still.

### Cross-game recognition

**Final Fantasy XIV (current).** Rested experience accrues while the character is in a sanctuary (cities, inns and areas around aetherytes) or logged out there. It gives a 50% bonus to experience from enemies, FATEs, crafting and gathering, and a full bar takes 7 days to fill. Rewrite it in our model: the multiplier is 1.5 instead of 2, and the bank fills over a week instead of about ten days. It is the same rule shape, so it has the same property. It regulates total hours and compresses the gap between light and heavy players, and it says nothing about session length.

**China's online game fatigue system (2007).** Once a player reached a cumulative three to five hours of play, rewards were cut by 50%, and beyond five hours no rewards were given. This is our fatigue column exactly, run by a regulator rather than a designer. Our table predicts what it does: it leaves players who play 2 hours a day untouched and cuts a 14-hour binge to less than a third of its reward. It also shows the weakness. It only works if the player cannot simply switch to a second account. Later Chinese rules tied play to real names, and from September 2020 the government ran its own name-based authentication system for publishers to use (week 11).

**World of Warcraft beta to launch.** The same designers ran both rules on the same game. They kept the one that tested better with players, and in doing so moved from regulating session length to regulating total hours. Whether that was the right trade depends on what you wanted the rule to do. If the goal was "players should not grind for 12 hours," the shipped rule does not achieve it.

Three contexts, one model: a reward multiplier that depends on either time offline, time in session, or presence on the day. When you meet a new pacing system, ask which of the three clocks it reads.

### Design judgment

- **Name the clock before you tune the numbers.** Decide whether you want to shape total hours, session length or daily presence. Most arguments about "addictive" pacing are really disagreements about which clock should matter.
- **Rested systems are gentle and mostly harmless.** They reward coming back, they never punish an absence shorter than the cap (240 hours in WoW, about ten days), and they narrow the gap between casual and heavy players. Their cost is that they do not stop marathons, and a cap reached during a long absence wastes rest, which GD102 week 2 showed as the shaded area on the stock chart.
- **Fatigue systems work and feel bad.** They do limit sessions. They also punish exactly the players who play in long weekend blocks because that is when they have time, and they invite workarounds (alternate accounts, account sharing). If you use one, frame it as a pool that empties, and tell the player how much is left.
- **Daily rewards buy retention with obligation.** Daily active user numbers go up. The same mechanism makes the game into a chore for players with irregular lives. If you use them, let players bank missed days (a weekly cap instead of a daily one), and never let a streak reset to zero.
- **Framing is design, but it is not the whole design.** The WoW story is usually told as "framing beats substance." Look at the table again. The substance changed too.

## 3. A responsible-design toolkit

The worked example gave you one test, the obligation test. Here is the rest of the kit, grouped by what each tool acts on.

### Tools that act on time

- **Session reminders.** A clock or a gentle "you have been playing for 2 hours" message. Cheap, respectful of autonomy, and weak on its own. Put it where it does not interrupt combat.
- **Natural stopping points.** A dungeon that takes 40 minutes gives a player a place to stop. An endless queue of 5-minute tasks does not. This is level and content design, and it matters more than any reminder.
- **Weekly instead of daily caps.** A weekly cap on a reward lets players fit it around their lives. A daily cap asks them to arrange their lives around it. The total reward can be identical.
- **Catch-up mechanics.** Rested experience is one. Others raise reward rates for players behind the current content. They reduce the fear that a week off means falling behind forever.

### Tools that act on money

Spending is the other place where "I did more than I meant to" causes harm. Loot boxes, randomized purchases with a price, are regulated differently across countries. China's Ministry of Culture required publishers to disclose item drop probabilities from May 2017. In April 2018, Belgium's Gaming Commission found that loot boxes in FIFA 18, Overwatch and Counter-Strike: Global Offensive broke its gambling laws. In the Netherlands, a 2020 fine against Electronic Arts over FIFA packs was overturned by the country's highest administrative court in March 2022. The United Kingdom decided in July 2022 not to legislate and asked the industry for voluntary protections instead. MMO403 weeks 6 to 8 cover this in depth; see the [MMO403 syllabus](../../MMO403-business-monetization-and-ethics-of-live-games/syllabus.md). For this course, the governance point is enough. The same mechanism is gambling in one country and a game feature in the next, so a global game ends up with the strictest rule by default or with regional versions of the same world.

Tools here include spending limits the player sets, a visible monthly total, disclosed odds, and pity timers that put a ceiling on how much bad luck can cost (MA102 week 10).

### Tools that act on obligation

- **Remove the penalty for absence.** Missed events come back. Seasonal rewards can be earned later at a cost in time, not gone forever.
- **Make social commitments visible and negotiable.** Raid schedules are the strongest obligation in most MMOs, and they come from players, not from your reward tables. You can still help. Lockouts that allow a raid on any night of the week remove the need to all be online on Tuesday.
- **Watch the right metric.** Session length is easy to log and tells you little. Ask about obligation directly, with a validated survey item on why people play, and look at how much of your daily activity is players doing only the daily task and leaving. A high share of logins that last under 10 minutes and touch only the daily reward is a signal of obligation, not engagement. MMO308 week 3 teaches cohort and retention analysis; see the [MMO308 syllabus](../../MMO308-live-operations-analytics-and-experimentation/syllabus.md).

### Where responsibility sits

You will hear two extreme positions. One says players are adults and how long they play is their business. The other says any design that increases play time is exploitation. Neither survives the evidence. The first ignores that you choose the reward structure, and structure shapes behavior (that is why you build it). The second ignores that most players at most play times are fine, and that the 2022 telemetry found time itself was not the problem.

A defensible middle position for a studio is this. You are responsible for the incentives you create, not for every hour anyone spends in your world. So audit your incentives. Every rule that makes an absence costly, or makes stopping costly, needs a reason you would say out loud to your players. Week 14's debate will test whether you can defend that position against both extremes.

## In-class activity (25 minutes)

Work in groups of three. Each group gets one real or invented pacing system: WoW rested experience, FFXIV rested experience, a 7-day login calendar with a streak that resets on a miss, a daily quest cap, or a stamina/energy bar that refills at 1 point every 6 minutes up to 120.

1. Rewrite your system in the lecture's model. Which clock does it read: time offline, time in session, or presence on the day? Give the multiplier or bonus and any cap. (8 min)
2. Run the obligation test. The player moves one day's play to the next day with the same total hours. What do they lose, and can they avoid it without adding a login? (7 min)
3. Propose one change that keeps the system's retention purpose and lowers the obligation cost. State the new number. (7 min)
4. One-minute report to the room.

Expected output: a one-line model, a loss figure from step 2, and a before-and-after for your change.

## Common misconceptions

- **"More hours means more addiction."** Neither ICD-11 nor DSM-5 uses hours as a criterion, and the 2022 telemetry study found little link between play time and wellbeing. Loss of control, harm, and playing out of felt obligation are what matter.
- **"Rested experience limits grinding."** It regulates total hours and helps light players catch up. A 14-hour binge earns the same rested total as seven 2-hour evenings.
- **"Framing is all that changed when WoW flipped fatigue into rest."** The pool now fills from time offline, not from time since the session started. That changes which schedules it rewards.
- **"Daily rewards are harmless because they are small."** Their size per day is small. Their cost of absence cannot be avoided by rearranging your hours, which is what makes them feel mandatory, and streaks make that cost grow.

## Check yourself

1. Using the lecture's rested model (`b = 10`, `a = 0.625`, cap 150), what weekly rested bonus does a player get who plays 20 hours a week? What is their total weekly experience?
2. A player plays 3 sessions of 5 hours each week under the fatigue rule. What do they earn? How could they earn more with the same 15 hours?
3. A game replaces its daily reward (10% of a level per login day) with a weekly one (70% of a level, earned by logging in on any 3 days). For the light, daily and binge players in the table, what does each earn from the new reward?
4. At what weekly play time `H` does the rested bonus stop being limited by base gain and start being limited by the bank? Show the equation.
5. A designer says: "Our streak bonus is fine; the average player never misses a day." Using the obligation test, explain what that statistic hides.

<details>
<summary>Answers</summary>

1. `min(0.625 × 148, 10 × 20) = min(92.5, 200) = 92.5`. Total `200 + 92.5 = 292.5` percent of a level.
2. Each 5-hour day earns `30 + 10 = 40`, so 120 a week. Five sessions of 3 hours earn `5 × 30 = 150`. The rule rewards spreading play across more days.
3. Light (2 days) gets 0, since they do not reach 3 days. Daily gets 70. Binge (1 day) gets 0. The weekly version removes the daily penalty for the daily player's missed day, but it still excludes the light and binge players. A threshold of 1 or 2 days would include the weekend player.
4. Set `0.625 × (168 − H) = 10 × H`, so `105 = 10.625 H` and `H ≈ 9.88` hours.
5. Players who would miss days may already have left, so the survivors look perfectly regular (survivorship). And "never misses" can be the result of obligation: the players may be logging in because missing costs them, which is the effect you should worry about. Measure short logins that only claim the reward, and ask players why they log in.

</details>

## Lab / assignment hook

[Lab 10, pacing audit](../labs/lab10.md). Run the four pacing rules over a synthetic population of 500 player schedules, compute who gains and loses under each, and write a 400-word recommendation for a studio choosing between a daily reward and a weekly one. Your analysis feeds the case-analysis portfolio (30% of the course grade).

## Sources

- Warcraft Wiki, "Rest" (retail World of Warcraft, accessed September 2026). One bubble (10% of a level) per 16 hours logged off in an inn or capital, per 64 hours elsewhere; cap of 15 bubbles (150% of a level); doubled experience from kills and several gathering activities while rested; account of the beta rule that halved experience after a few hours and its reframing as a 200% bonus. https://warcraft.wiki.gg/wiki/Rest
- Final Fantasy XIV Online Wiki (consolegameswiki), "Rested EXP" (current version, accessed September 2026). 50% bonus to experience from enemies, FATEs, crafting and gathering; accrues in sanctuaries; 7 days to fill the bar. https://ffxiv.consolegameswiki.com/wiki/Rested_EXP
- Wikipedia, "Shutdown law" (accessed September 2026). China's 2007 Online Game Addiction Prevention System (fatigue system): rewards cut by 50% after a cumulative three to five hours of play and to zero beyond five hours. South Korea's shutdown law (2011 to 2021) for under-16s.
- Wikipedia, "Video game addiction in China" (accessed September 2026). Government name-based authentication system made available to companies in September 2020.
- Wikipedia, "Digital media use and mental health" (accessed September 2026). Notes that the 2007 anti-addiction system was implemented for minors.
- World Health Organization, ICD-11, 6C51 "Gaming disorder." Dates (released June 2018, approved May 2019, in effect 1 January 2022) and the 12-month and impairment criteria as summarized in Wikipedia, "Video game addiction" (accessed September 2026).
- American Psychiatric Association (2013). *Diagnostic and Statistical Manual of Mental Disorders*, 5th ed. Internet Gaming Disorder in Section III as a condition for further study, nine proposed criteria. Summary from Wikipedia, "Video game addiction" and "Internet gaming disorder" (accessed September 2026).
- Vuorre, M., Johannes, N., Magnusson, K. & Przybylski, A. K. (2022). "Time spent playing video games is unlikely to impact well-being." *Royal Society Open Science* 9(7). 38,935 players, six weeks of publisher-supplied play data from seven publishers, three survey waves. https://doi.org/10.1098/rsos.220411
- Wikipedia, "Loot box" (accessed September 2026). China's probability disclosure rule (May 2017); Belgian Gaming Commission findings on FIFA 18, Overwatch and CS:GO (April 2018); Dutch court reversal of the EA fine (March 2022); UK DCMS response (July 2022).
- The base rate `b = 10%` per hour, the daily reward `d = 10%`, and the four player schedules are invented for teaching.

## Interactive spec: examples/w10-pacing-rules.html

**The one insight.** Pacing rules read different clocks. Rested experience reads time offline, so it gives the same weekly total to every arrangement of the same hours. Fatigue reads time in session and punishes long sessions. Daily rewards read presence on the day and punish missing a day in a way no rearrangement can avoid.

**Layout.** A control strip on top. Two linked panels below, side by side at 1280px, stacked at 390px (week strip first). A numbers table under both panels.

**Controls (keyboard operable, numeric readouts).**
- Sessions per week `n`: 1 to 7, step 1, default 7. Sessions are placed on the last `n` days of the week (Sunday back to Monday), each starting at 18:00; if a session is longer than 6 hours it starts at 10:00 instead.
- Hours per session `h`: 1 to 14, step 1, default 2.
- Lock toggle "keep weekly hours at 14": when on, changing `n` sets `h = round(14 / n)` and changing `h` sets `n = round(14 / h)` clamped to 1..7. Off by default.
- Base rate `b`: 5 to 20, step 1, default 10 (percent of a level per hour).
- Rested accrual `a`: 0.1 to 2, step 0.025, default 0.625 (percent per offline hour); rested multiplier `m_r`: 1.5 or 2 (radio), default 2; cap: 50 to 300, step 10, default 150.
- Fatigue thresholds: full-rate hours `t1` (1 to 6, default 3), half-rate end `t2` (t1 to 10, default 5).
- Daily bonus `d`: 0 to 30, step 1, default 10.
- Preset buttons: Light (n 2, h 2), Daily (7, 2), Weekend (2, 7), Binge (1, 14), and "Skip Wednesday" (daily schedule with Wednesday removed and Thursday set to 4 hours).
- Buttons to switch rested multiplier to "FFXIV-like" (m_r 1.5, accrual set so the cap fills in 168 hours: `a = cap / 168`).

**Simulation.** Hour-by-hour over 6 weeks, report the 6th week (steady state). For each hour: if playing, flat gain `b`; rested gain `b + min(pool, (m_r − 1) × b)` and subtract the bonus from the pool; fatigue gain `b × (1 if hoursToday < t1, 0.5 if < t2, else 0)`; daily gain `b` plus `d` on the first played hour of the day. If not playing, `pool = min(cap, pool + a)`. `hoursToday` resets at midnight.

**Left panel, the week strip.** 7 rows (days) by 24 columns (hours) for the selected rule (tabs: Flat, Rested, Fatigue, Daily). Each played cell is shaded by its gain relative to `b` (0, 0.5, 1, 1 + bonus). Offline cells show the rested pool level as a thin bar when the Rested tab is active. Label each row with that day's total.

**Right panel, weekly total against hours.** Horizontal axis weekly hours 0 to 40, vertical axis weekly experience. For the current session length `h`, plot each rule's weekly total as `n` varies (so hours = `n × h`), four lines, labeled at the end. Also draw the closed-form rested curve `b × H + min(a × (168 − H), (m_r − 1) × b × H)` as a thin dashed line. Mark the current schedule with a dot on each line.

**Numbers table.** For the current schedule: hours per week, and weekly totals for Flat, Rested, Fatigue, Daily, plus "loss if one day's hours move to the next day" for each rule (computed by moving the hours of the middle played day onto the next played day and rerunning; show "n/a" when there is only one session).

**Test values (the builder must check these).**
- Light (2, 2): 40, 80, 40, 60.
- Daily (7, 2): 140, 236.25, 140, 210.
- Weekend (2, 7): 140, 236.25, 80, 160.
- Binge (1, 14): 140, 236.25, 40, 150.
- Skip Wednesday: flat loss 0, rested loss 0, fatigue loss 5, daily loss 10.
- Closed form at 20 hours: rested bonus 92.5.

**Accessibility and style.** Use `templates/interactive-tokens.css`. Rule lines differ by dash pattern and direct labels, not color alone. Week-strip cells get a text readout on focus/hover. Respect reduced motion. No game logos or art.

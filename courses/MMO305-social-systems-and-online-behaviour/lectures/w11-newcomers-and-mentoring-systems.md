# MMO305 · Week 11 — Newcomers and Mentoring Systems

**Why this matters:** Every MMO loses most of its new players in the first weeks, and teams usually respond by polishing the tutorial. The evidence from games and from other online communities points somewhere else: newcomers stay when they connect with people. This week gives you a model that shows why, and why the usual early metrics cannot see it.

**You will be able to:**
- Compute day-by-day newcomer retention with a two-state model (unattached and attached) and read the share of survivors who are attached.
- Explain why a mentoring change can leave day-1 and day-7 retention almost unchanged while nearly doubling day-30 retention.
- Compare a mentoring intervention with a tutorial intervention by the model, and state which metric and time horizon would detect each.
- Design a newcomer channel and mentor program, including mentor eligibility, capacity and protection against abuse, and critique a shipped one.

**Before class:** Halfaker, Geiger, Morgan & Riedl (2013), "The Rise and Decline of an Open Collaboration System", *American Behavioral Scientist* 57(5), sections on newcomer rejection. Morgan & Halfaker, "Evaluating the impact of the Wikipedia Teahouse on newcomer socialization and retention" (OpenSym 2018), or the Teahouse retention summary on Meta-Wiki. Skim the Final Fantasy XIV Online Wiki pages "Novice Network" and "Mentor".

**Prerequisites from earlier courses:** [GD102 week 2, stocks and flows](../../GD102-systems-design-and-game-mechanics/lectures/w02-stocks-and-flows.md) (the update rule `S[t+1] = S[t] + inflow − outflow`, which this week's model uses twice). [MA101 week 4, exponentials](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md) (repeated multiplication by a daily survival rate). [MA102 week 14, hypothesis testing and A/B](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w14-intro-to-hypothesis-testing-ab.md) (how to test a mentoring change). [UX201 week 7, onboarding and tutorials](../../UX201-game-ux-and-player-psychology/lectures/w07-onboarding-and-tutorials.md). From this course, [week 1 on bonding social capital](w01-mmos-as-societies-social-capital.md), [week 3 on forced grouping](w03-forced-vs-voluntary-grouping.md), [week 4 on guilds](w04-guilds-formation-lifecycle-leadership.md), [week 7 on status](w07-status-prestige-and-conspicuous-display.md), [week 8 on griefing](w08-griefing-typology-and-design-responses.md), and [week 10 on channels](w10-communication-design-chat-emotes-pings.md).

**Interactive:** [examples/w11-newcomer-retention.html](../examples/w11-newcomer-retention.html). Use it during section 2.

---

## 1. The newcomer problem

A **newcomer** is a player in their first days or weeks in a game. Newcomers differ from veterans in three ways that matter for design.

1. **They lack knowledge.** They do not know the controls, the map, the jargon, or which quests are worth doing. This is the problem tutorials solve, and UX201 week 7 covers it.
2. **They lack ties.** They know nobody. Nobody will notice if they stop logging in. This is the problem that social systems solve, and it is this week's subject.
3. **They lack standing.** Veterans may treat them as a nuisance, a target or a source of mistakes in group content. Newcomers who are rejected early often leave for good.

Designers often treat the first problem as the whole problem, because knowledge gaps are visible in playtests and fixable with better UI. The second and third problems are harder to see. They show up in retention curves weeks later, when nobody connects them to the design of the starting zone.

### Evidence from an open community

The clearest large-scale evidence comes from outside games, from Wikipedia, where every edit is logged. Halfaker and colleagues (2013) studied why the number of active English Wikipedia editors began falling after 2007. The obvious explanation was that fewer good people were joining. The data said otherwise. The share of newcomers who arrived with good-faith, useful first edits stayed roughly stable. What changed was how they were received. Good-faith newcomers had their first edits reverted more and more often, frequently by semi-automated tools whose users rarely explained the revert. Those rejected newcomers were much less likely to stay.

The Wikimedia Foundation then tested a fix. The **Teahouse** is a friendly question-and-answer space where experienced editors host newcomers. In a controlled study, Morgan and Halfaker invited a random sample of new editors to the Teahouse and compared them with a control group that received no invitation. The invited group was more than 10% more likely to still be editing at 3 to 4 weeks and again at 2 to 6 months. One invitation to a welcoming space changed long-run retention measurably.

Two lessons carry over to games. Newcomers leave because of how they are treated as much as because of what they know. And the effect of a welcome is a long-run effect, visible weeks later, which is the part of the curve most teams stop watching.

## 2. Worked example: the connection clock

### The hook

Final Fantasy XIV runs a dedicated chat channel for newcomers, the **Novice Network**, introduced in patch 3.2 (2016) together with a **Mentor** system. New players carry a "New Adventurer" status (players call it the sprout, after its icon) until they have 300 hours of play time and have completed a named main-story quest ("The Coming Dawn" at the time of writing), or until they switch it off. Mentors must earn it. A battle mentor needs 1,000 completed dungeons, raids or trials, 1,500 commendations from other players, and the tank and healer role quests. Each Novice Network instance holds up to 100 mentors and 412 new adventurers.

World of Warcraft added a similar **Newcomer Chat** in patch 9.0.1 (2020), with volunteer **Guides** who must have completed 3,000 quests.

Two big studios have built channels, eligibility rules and capacity limits for newcomers, at a real cost in moderation. Their players still arrive through tutorials that were polished for years. Why spend on people rather than on more tutorial? The model below shows what a mentor channel buys that a tutorial cannot, and why you would not see it in your first week of data.

### The model

Split active newcomers into two groups.

- **Unattached (`U`)**: playing, but with no social tie in the game. No guild, no friend they play with, no mentor who knows their name.
- **Attached (`A`)**: has at least one tie.

Each day:

- An unattached newcomer quits with probability `a`, becomes attached with probability `p`, and otherwise stays unattached.
- An attached newcomer quits with probability `b`, with `b` much smaller than `a`.

Start with the whole cohort unattached, `U₀ = 1` and `A₀ = 0`. Then, as a pair of stock-and-flow updates (GD102 week 2):

```
U[t+1] = U[t] × (1 − a − p)
A[t+1] = A[t] × (1 − b) + U[t] × p
retention R[t] = U[t] + A[t]
```

Every symbol:

- `a`, the **solo churn**: daily chance an unattached player quits. Tutorials, quest clarity and performance mostly act on `a`.
- `b`, the **tied churn**: daily chance an attached player quits.
- `p`, the **connection rate**: daily chance an unattached player forms a tie. Mentor channels, guild recruitment tools and group content mostly act on `p`.
- `R[t]`, the share of the starting cohort still playing on day `t`.

The model has a closed form if you want it. Write `q = 1 − a − p`:

```
U[t] = qᵗ
A[t] = p × ((1 − b)ᵗ − qᵗ) / (a + p − b)
```

You will not need it for the table below; iterating the update by hand or in a spreadsheet is enough. The closed form tells you one more thing. The share of newcomers who **ever** attach is `p / (a + p)`, because each day an unattached player either leaves (`a`) or attaches (`p`), and those are the two exits from `U`.

### Numbers you can check

Use `a = 0.10` (an unattached newcomer has a 10% chance of quitting each day), `b = 0.02`, and compare three designs.

- **Baseline:** `p = 0.02`.
- **Mentoring:** a newcomer channel and mentor program triples the connection rate, `p = 0.06`.
- **Tutorial:** a much better tutorial cuts solo churn by 30%, `a = 0.07`, with `p = 0.02`.

| Design | Day 1 | Day 7 | Day 14 | Day 30 | Attached share of day-30 survivors | Ever attach `p/(a+p)` |
|---|---|---|---|---|---|---|
| Baseline (`a` 0.10, `p` 0.02) | 90.0% | 50.1% | 28.4% | 12.6% | 83% | 16.7% |
| Mentoring (`a` 0.10, `p` 0.06) | 90.0% | 54.1% | 37.3% | 23.7% | 98% | 37.5% |
| Tutorial (`a` 0.07, `p` 0.02) | 93.0% | 61.7% | 40.6% | 19.8% | 70% | 22.2% |

Check day 1 by hand. Baseline: `U₁ = 1 × 0.88 = 0.88` and `A₁ = 0 + 1 × 0.02 = 0.02`, so `R₁ = 0.90`. Mentoring: `U₁ = 0.84`, `A₁ = 0.06`, and `R₁ = 0.90` again. On day 1 the two designs are identical, because a newcomer who attaches today has not yet had a chance to benefit from it. Only the split between `U` and `A` differs.

Check day 2 for mentoring. `U₂ = 0.84 × 0.84 = 0.7056`. `A₂ = 0.06 × 0.98 + 0.84 × 0.06 = 0.0588 + 0.0504 = 0.1092`. `R₂ = 0.8148`, against baseline `0.7744 + 0.0372 = 0.8116`. A gap of 0.3 percentage points.

### What the table says

Read the rows at different horizons.

- **Day 1:** tutorial wins (93% against 90%), and mentoring is indistinguishable from baseline.
- **Day 7:** tutorial still wins clearly (61.7% against 54.1%). A team that ships both changes and reads day-7 retention will conclude the tutorial was the better investment.
- **Day 30:** mentoring wins (23.7% against 19.8%), and it has nearly doubled the baseline.

The two interventions act on different parts of the curve. Lowering `a` slows the initial fall of everyone. Raising `p` moves people into the slow-decay group, and that pays off only after the unattached group has mostly drained away. After a month, almost every survivor is someone with a tie. In the mentoring design, 98% of day-30 players are attached. **Long-run retention is a connection problem, measured with a delay.**

This is the connection clock of the title. Each unattached newcomer is on a timer with expected length `1 / (a + p)` days, about 8.3 days at baseline. The timer ends either with a tie or with a quit. A tutorial makes the timer run slower. A mentor program makes the good ending more likely. Both help. Only one of them changes who is left a month later.

### A visual the student can move

Open `examples/w11-newcomer-retention.html`. The left panel shows the day-1 and day-7 retention bars for the three designs, and the tutorial looks like the clear winner. The right panel shows the full 60-day curves, stacked into attached and unattached layers, and the mentoring curve crosses the tutorial curve around day 20. Drag `p` and watch the left panel barely move while the right panel's tail lifts. Then drag `a` and see the reverse. The crossover day is printed under the chart.

### Cross-game and cross-context recognition

Each system below is a way of raising `p`, lowering `a` for a specific cause, or lowering the rejection that pushes newcomers out.

**Final Fantasy XIV, Novice Network and Mentors (introduced in patch 3.2; current rules as of the Dawntrail era, 2024-2026).** The Novice Network raises `p` by giving every new adventurer a channel where people are paid in status to answer. The mentor requirements (1,000 duties, 1,500 commendations) filter for players who have played with strangers many times and been thanked for it. The channel's capacity of 100 mentors to 412 new adventurers, about 4.1 newcomers per mentor slot, is a staffing ratio. It caps the number of newcomers who can be in a conversation with experienced players at once.

**World of Warcraft, Newcomer Chat and Guides (patch 9.0.1, October 2020, with the Guide level requirement raised in 11.0.2 and 12.0.1).** The same structure, with a lower bar for helpers (a quest count and a level) and an automatic exit for newcomers after 40 hours played and a level threshold. The exit rule matters: it keeps the channel a newcomer space rather than a general chat that veterans take over, which would recreate the saturation problem from week 10.

**Wikipedia, the Teahouse (study period 2014-2015).** A randomised invitation to a host-staffed space, with a retention gain visible at weeks and months. In model terms, the invitation raised `p` for the invited group. The gain showed up in the long windows, as the model predicts.

**Wikipedia, reverts of good-faith newcomers (2007 onward).** The Halfaker study describes the opposite intervention. Rejection raised `a` for newcomers who had done nothing wrong. Automated quality control that rarely explained itself increased churn among exactly the people the community needed. The game equivalents are vote-kicks of new players from group content, and veterans in a dungeon group who expect newcomers to know the route. Week 3's forced grouping discussion applies here: a grouping system that throws newcomers into groups of impatient veterans can raise `a` and lower `p` at the same time.

### Eyes-open design judgment

Mentoring systems are not free, and the model does not tell you everything.

- **Mentor supply is a stock.** Mentors burn out, get bored and quit. If your newcomer inflow grows faster than your mentor pool, the ratio falls and `p` falls with it. Treat mentors as a stock with its own inflow (recruitment) and outflow (burnout), and watch the ratio as a live-ops metric.
- **Eligibility is a filter with two errors.** A high bar (FFXIV's) keeps out bad mentors and keeps out many good ones. A low bar (a quest count) fills the channel fast and lets in players who want an audience, including some who will mislead or recruit newcomers into scams. Decide which error you can moderate more cheaply.
- **Status is the mentor's pay.** Mentors in both games get a visible icon. That is a status reward (week 7), and it attracts people who want status. Some of them are the best helpers you have. Some will use the channel to show off. Tie the icon to continued good conduct, and make it removable.
- **Ties to bad actors count as ties.** The model rewards any attachment. A newcomer recruited into a guild of griefers is "attached" and retained. Your metric for `p` should count ties that survive, and your moderation must reach newcomer spaces first.
- **Correlation is not the intervention.** Attached players churn less, but some of that is because players who were going to stay anyway are the ones who join guilds. The Teahouse study is valuable because it randomised the invitation. Test your mentoring change the same way (MA102 week 14), and read the result at day 30, not day 7.

### Check yourself (worked example)

1. With `a = 0.10`, `b = 0.02` and `p = 0.04`, compute `R₁` and `R₂` by hand.
2. What share of newcomers ever attach at `a = 0.10` and `p = 0.04`? At `a = 0.07` and `p = 0.06`?
3. A studio measures only day-7 retention in an A/B test of a mentor program and finds a gain of 4 percentage points. Using the model's table, what do you expect at day 30, and what would you tell the studio about its metric?

<details>
<summary>Answers</summary>

1. `U₁ = 0.86`, `A₁ = 0.04`, `R₁ = 0.90`. `U₂ = 0.86 × 0.86 = 0.7396`. `A₂ = 0.04 × 0.98 + 0.86 × 0.04 = 0.0392 + 0.0344 = 0.0736`. `R₂ = 0.8132`.
2. `0.04 / 0.14 ≈ 28.6%`. `0.06 / 0.13 ≈ 46.2%`.
3. The table's mentoring row gains 4.0 points at day 7 (54.1% against 50.1%) and 11.1 points at day 30 (23.7% against 12.6%), almost double the baseline. A day-7 metric understates a connection intervention, so the studio should report day-30 retention, or better, the share of day-30 survivors who are attached.

</details>

## 3. Designing the newcomer space

The model says to raise `p` and to avoid raising `a` through rejection. The rest of this lecture turns that into design choices.

### Make newcomers visible

A mentor cannot help someone they cannot see. FFXIV's sprout icon and WoW's newcomer flag both mark newcomers publicly, which lets veterans adjust (explain a mechanic, slow down) and lets group finders place them with care. Visibility has a cost. A visible newcomer is also a visible target for scammers and griefers (week 8). FFXIV lets a new adventurer turn the status off at any time, which gives the player control over that trade-off.

### Give the space a purpose and an exit

A newcomer channel that anyone can join becomes a general chat. The week 10 model tells you what happens next: `L` grows, veterans post jokes, and the newcomers' questions scroll away. Both games solve this with membership rules. Newcomers join by status and leave automatically after a threshold. Helpers join by eligibility. A capacity limit per channel instance keeps `L` below saturation, and it is the same lever as splitting a channel.

### Build repeated contact

A single helpful answer is not a tie. Ties form through repeated contact with the same people (week 3). Designs that turn one answer into repeated contact:

- **Mentor-newcomer group content** where the veteran is rewarded for completing a dungeon with a first-timer. A bonus of this kind pays veterans to group with newcomers rather than avoid them, which counters the vote-kick incentive described below. Price it so that it does not attract veterans who farm newcomers for the bonus and then abandon them.
- **Guild recruitment tools** that suggest guilds whose members play at the newcomer's times and level range.
- **Starting-area social hubs** where the same people meet daily because the quests send them back.

### Protect the first rejection

The Wikipedia evidence says the first rejection is the most expensive. In games the first rejection is often a vote-kick, a harsh message after a wipe, or an unexplained ban from a group. Designs that reduce it:

- Vote-kick rules that require a reason and prevent kicking a flagged newcomer in the first minutes of a dungeon.
- Group finders that match newcomers with groups that opted in to teaching.
- Automated moderation that explains itself. Halfaker's finding was that automated tools rarely started a conversation after a revert. An automatic chat mute that says why, and how to appeal, rejects the behaviour without rejecting the person.

### Measure it

Instrument the model directly. You need, per newcomer and per day, whether they played and whether they had a tie (guild membership, a repeated group partner, a friend-list entry used for play). From that you can estimate `a`, `b` and `p` for each cohort (lab 11 does exactly this). A mentoring change should show up as a higher `p`, long before it shows up clearly in day-30 retention.

## In-class activity (25 minutes)

Groups of three or four. Each group gets one of these newcomer problems.

- **A.** A sandbox MMO where veterans can attack anyone outside safe zones. Newcomers who are killed in their first hour quit at twice the normal rate.
- **B.** A themepark MMO where the fastest way to level is solo questing, and the first group dungeon unlocks at hour 12.
- **C.** A cozy life-sim MMO where newcomers join fine but report that "everyone already has their friends."

Steps:

1. **Diagnose (5 min).** Which parameter does your problem hurt: `a`, `p`, `b`, or rejection that raises `a`?
2. **Design (12 min).** Propose one change that raises `p` and one that protects against early rejection. Name the channel, the eligibility rule for helpers, and the exit rule.
3. **Predict (5 min).** Estimate your change as a new parameter value and use the table's baseline (`a` 0.10, `b` 0.02, `p` 0.02) to predict day-7 and day-30 retention. Iterate the update rule for a few days to check your direction.
4. **Report (3 min).** One sentence each: the change, the parameter, the predicted day-30 number.

Expected output: a short design card with the parameter change and the prediction.

## Common misconceptions

- **"If day-7 retention didn't move, the mentor program failed."** Connection changes pay off late. The model's mentoring design gains 4 points at day 7 and 11 at day 30. Read long horizons, or measure `p` directly.
- **"A better tutorial is always the safe investment."** It lowers `a` and wins the early metrics. It changes little about who is left after a month, because survivors are mostly attached players.
- **"Any newcomer chat helps."** A newcomer channel without membership and exit rules saturates like any other channel, and one without moderation can raise churn by exposing newcomers to scams and abuse.
- **"Attached players stay because of the tie."** Some would have stayed anyway. Only a randomised test, like the Teahouse invitation, separates the effect of the tie from the kind of player who forms ties.

## Check yourself

1. At `a = 0.10`, `b = 0.02`, what connection rate `p` makes half of all newcomers eventually attach?
2. A studio can either cut `a` from 0.10 to 0.08 or raise `p` from 0.02 to 0.04. Using the closed form or iteration, which gives higher day-30 retention? (Use `b = 0.02`.)
3. FFXIV's Novice Network holds 100 mentors and 412 new adventurers per instance. If a busy evening brings 2,000 new adventurers online, how many instances are needed, and how many mentors must be online to fill every mentor slot?
4. Your mentor channel's eligibility rule is "reached max level." Name two ways this rule could lower `p` or raise `a` for newcomers, and propose a better rule.

<details>
<summary>Answers</summary>

1. `p / (0.10 + p) = 0.5` gives `p = 0.10`.
2. Cut `a` to 0.08: `q = 0.90`, `R₃₀ = 0.9³⁰ + 0.02 × (0.98³⁰ − 0.9³⁰) / 0.08 ≈ 0.0424 + 0.25 × (0.5455 − 0.0424) ≈ 0.0424 + 0.1258 = 0.168`. Raise `p` to 0.04: `q = 0.86`, `R₃₀ = 0.86³⁰ + 0.04 × (0.5455 − 0.0108) / 0.12 ≈ 0.0108 + 0.1782 = 0.189`. Raising `p` wins at day 30 (18.9% against 16.8%).
3. `2,000 / 412 ≈ 4.85`, so 5 instances. Filling every mentor slot takes `5 × 100 = 500` mentors online. If only 200 are online, the ratio falls from about 4 newcomers per mentor to 10.
4. Max level says nothing about helpfulness or patience, so it admits players who answer rudely (raising `a`) or who use the channel to show off, which buries questions (lowering `p`). A better rule combines a play-with-others record (group content completed with strangers), a thanks record (commendations), and a clean conduct history, like FFXIV's, with removal for reports that are upheld.

</details>

## Lab / assignment hook

[Lab 11, newcomer cohort analysis](../labs/lab11.md). You fit the two-state model to a synthetic cohort log, estimate `a`, `b` and `p` for a control group and a mentored group, and write a one-page recommendation with the right retention horizon. The lab's data generator is included in the lab file.

## Sources

- Final Fantasy XIV Online Wiki (consolegameswiki), "Novice Network" (accessed September 2026, Dawntrail era). Introduced with the Mentor system in patch 3.2; New Adventurer status removed at 300 hours played plus completion of the quest "The Coming Dawn", or manually; capacity of 100 mentors and 412 new adventurers per network; returner eligibility.
- Final Fantasy XIV Online Wiki (consolegameswiki), "Mentor" (accessed September 2026). Battle mentor requirements: 1,000 instanced duties, 1,500 player commendations, tank and healer role quests and one DPS role quest; trade mentor requirements.
- Warcraft Wiki, "Newcomer Chat" (accessed September 2026). Added in patch 9.0.1 (October 13, 2020); Guides need 3,000 quests completed and a level requirement raised in patches 11.0.2 and 12.0.1; newcomers leave after 40 hours played and a level threshold.
- Halfaker, A., Geiger, R. S., Morgan, J. T. & Riedl, J. (2013). "The rise and decline of an open collaboration system: How Wikipedia's reaction to popularity is causing its decline." *American Behavioral Scientist*, 57(5), 664-688. Summarised on Meta-Wiki, "Research:The Rise and Decline".
- Morgan, J. & Halfaker, A. Teahouse long-term new editor retention study, Wikimedia Foundation (Meta-Wiki, "Research:Teahouse long term new editor retention"; data October 2014 to January 2015). Invitees more than 10% more likely to meet the survival threshold at 3-4 weeks and 2-6 months.
- Ducheneaut, N., Yee, N., Nickell, E. & Moore, R. J. (2006). "Alone Together? Exploring the Social Dynamics of Massively Multiplayer Online Games." *CHI 2006*. Course reading from week 2, on how much players play with others.

## Interactive spec: examples/w11-newcomer-retention.html

**The one insight:** a change to the connection rate `p` is almost invisible at day 1 and day 7 and large at day 30, while a change to solo churn `a` looks best early. The left panel must make the tutorial look like the winner and the right panel must show the curves cross.

**Layout (mobile first):** left panel above right panel on phones, side by side at 900px and wider. Number table below.

**Model (iterate daily, t = 0..60):**
```
U[0] = 1, A[0] = 0
U[t+1] = U[t] × (1 − a − p)
A[t+1] = A[t] × (1 − b) + U[t] × p
R[t] = U[t] + A[t]
ever attach = p / (a + p)
```
Guard `a + p ≤ 1` (disable values that break it and show a note).

**Three designs, each with its own parameter set, all editable:**
- Baseline: `a = 0.10, b = 0.02, p = 0.02` (grey).
- Mentoring: `a = 0.10, b = 0.02, p = 0.06` (accent colour 1).
- Tutorial: `a = 0.07, b = 0.02, p = 0.02` (accent colour 2).
A segmented control picks which design the sliders edit. Sliders: `a` 0.01 to 0.30 step 0.01, `b` 0.00 to 0.10 step 0.005, `p` 0.00 to 0.20 step 0.01. A "reset" button restores defaults.

**Left panel, "What the dashboard shows":** grouped bars for day 1 and day 7 retention for the three designs, with percentages printed on the bars (1 decimal).

**Right panel, "What happens by day 60":** line chart, x days 0 to 60, y retention 0 to 100%. One line per design. For the design currently being edited, draw the area under its line split into two stacked layers, attached (solid) and unattached (hatched), so the student sees the unattached layer drain. Vertical markers at day 7 and day 30. Print the first day on which Mentoring's `R` exceeds Tutorial's `R` ("curves cross on day N"), or "no crossing" if none.

**Number table:** for each design, `R` at days 1, 7, 14, 30, 60; attached share of survivors at day 30; ever-attach share.

**Test values (defaults, must match to 1 decimal):**
- Baseline: 90.0, 50.1, 28.4, 12.6; attached share at day 30 83%; ever attach 16.7%.
- Mentoring: 90.0, 54.1, 37.3, 23.7; 98%; 37.5%.
- Tutorial: 93.0, 61.7, 40.6, 19.8; 70%; 22.2%.
- Day 2 Mentoring `R = 81.5%`, Baseline `81.2%`.
- Mentoring first exceeds Tutorial on day 20 with defaults (30.4% against 29.9%); compute it, do not hard-code.

**Accessibility:** bars and lines distinguished by pattern or marker shape as well as colour; `aria-live` summary ("Day 30: Baseline 12.6%, Mentoring 23.7%, Tutorial 19.8%"); reduced motion disables curve animation.

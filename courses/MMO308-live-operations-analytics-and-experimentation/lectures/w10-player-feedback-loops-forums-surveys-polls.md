# MMO308 · Week 10 — Player Feedback Loops: Forums, Surveys, Polls

**Why this matters:** A live team hears from players every day, through forums, Discord, support tickets, bug reports, in-game surveys and polls. Each channel reaches a different slice of the player base, and the slice depends on how you ask as much as on who cares. If your in-game survey pops up for "whoever is online now", your most devoted players will answer it several times over, and a feature most players like can look like a failure.

**You will be able to:**
- Compute the chance that each player is reached by a survey trigger (random account, online now, at login) and predict the bias in the raw result.
- Correct a survey with inverse-probability weights computed from each respondent's own telemetry, and compute the effective sample size those weights leave you.
- Estimate how many players hit a problem from two overlapping report channels with the capture-recapture formula, and state when it undercounts.
- Design a feedback loop for a live game, with a channel for each question, a unit of analysis, and a published response time.

**Before class:** Seif El-Nasr, Drachen & Canossa (eds.), *Game Analytics* (2013), chapter 8, "Sampling for Game User Research" (Drachen, Gagné & Seif El-Nasr, pp. 143-167), and chapter 25, "Game Metrics Through Questionnaires" (Weedon, pp. 515-537).

**Prerequisites from earlier courses:** [UX201 week 12, surveys and interviews](../../UX201-game-ux-and-player-psychology/lectures/w12-surveys-and-interviews.md) (response bias in odds form, weighting by known groups, writing survey items). [MMO305 week 12, community management](../../MMO305-social-systems-and-online-behaviour/lectures/w12-community-management.md) (the voice ratio `ρ` that makes a forum louder than the player base). [MA102 week 13, sampling and confidence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (standard error, sample size, bias that `n` cannot fix). [DB201 week 10, telemetry design](../../DB201-data-persistence-and-telemetry/lectures/w10-telemetry-design-events-and-properties.md) (the session and account events you will join survey answers to). From this course, [week 7 on segmentation](w07-segmentation.md).

**Interactive:** [Who gets asked](../examples/w10-who-gets-asked.html). Keep it open during section 2.

---

## 1. The feedback loop in a live game

A **feedback loop** in live operations is the cycle that turns what players say and do into changes, and those changes into new things players say and do. It has five steps.

1. **Collect** signals from players.
2. **Estimate** what share of players hold a view or hit a problem.
3. **Decide** what to change, if anything.
4. **Ship** the change and tell players what you did.
5. **Measure** again, with the same instruments, to see whether it worked.

Two earlier courses gave you the hardest parts of step 2. MMO305 week 12 showed that a forum over-represents unhappy players by a voice ratio `ρ`, so forum sentiment needs a correction before it means anything. UX201 week 12 showed that people who answer a survey differ from people who don't, and that you can weight respondents to match group shares you know from telemetry. This week does not repeat those models. It adds the two questions a live team faces next. *Who did our own trigger put in front of the survey?* And *how many players does this problem really touch?*

### Channels and what each one sees

Every channel measures something different, reaches different players, and arrives at a different speed. Put them side by side before you trust any of them.

| Channel | What it measures | Who it reaches | Speed | Main distortion |
|---|---|---|---|---|
| Telemetry | What players did | Everyone who played | Minutes | Says nothing about why |
| Forums, Reddit, Discord | What engaged players say | Self-selected posters | Hours | Voice ratio `ρ` (MMO305) |
| Support tickets | Problems bad enough to report | Players who hit a blocker | Hours to days | Only the frustrated write in |
| In-game bug reporter | Problems seen while playing | Players in the affected content | Minutes | Reporting rate varies by player type |
| In-game survey | Stated opinion | Whoever the trigger reaches | Days | Trigger sampling (section 2) and nonresponse (UX201) |
| Email survey to an account sample | Stated opinion | A random list of accounts | A week | Nonresponse, lapsed players ignore it |
| Poll that decides content | Preference, with consequences | Eligible players who choose to vote | A week | Turnout and eligibility (week 11) |

Read the "Main distortion" column as a to-do list. Each distortion has a correction, and each correction needs a number you have to measure. A team that runs one channel and skips its correction is guessing.

### Say and do

The most useful habit in the loop is to pair every stated opinion with a behaviour. Players who say a dungeon is too long should also show longer clear times or more abandons in telemetry. Players who say they love a new daily quest should complete it on more days. When the two agree, act with confidence. When they disagree, the disagreement is the finding. Sometimes players dislike something they keep doing (a grind that works), and sometimes they praise something they have stopped doing (nostalgia for a mode nobody queues for). You need both to see either.

## 2. Worked example: ask the players who are online now

### The hook

In 2005, Ducheneaut, Yee, Nickell and Moore ran a census of World of Warcraft characters on several US servers by logging who was online every few minutes. Among other things, they measured guild sizes. The median guild had 6 members. The mean was 14.5. The largest had 257.

Now ask the question two ways. Pick a guild at random and ask how big it is, and the typical answer is 6. Pick a guilded *player* at random and ask how big their guild is, and the average answer must be above 14.5. It is the same census. The only change is the sampling unit. A 257-member guild is one guild, but it is 257 players, so a player-level sample hits it 257 times as often as it hits a one-person guild.

A live team makes this mistake every time it pops up an in-game survey for "players who are online". The unit it wants is a player. The unit it samples is a moment of play. The two are not the same, and the gap can reverse a decision.

### The model

Give each player `i` a number of hours played per week, `h_i`. A survey trigger decides the chance `π_i` that player `i` is asked. Three common triggers:

- **Random account.** Draw accounts from the list of active players. Every player has the same chance, `π_i ∝ 1`.
- **Online now.** Ask players who are logged in at random moments. A player online 25 hours a week is present at 12.5 times as many moments as a player online 2 hours, so `π_i ∝ h_i`.
- **At login.** Ask at the start of a session. The chance grows with the number of sessions per week, `π_i ∝ s_i`.

If player `i` answers `y_i` (1 for "approve", 0 for "don't"), the raw survey average estimates

```
raw = Σ π_i × y_i / Σ π_i
```

which is the approval of *playtime*, not of players. To get the approval of players, weight each respondent by the inverse of their chance of being asked:

```
w_i = 1 / π_i
estimate = Σ w_i × y_i / Σ w_i        (summed over respondents)
```

This is an **inverse-probability weighted** estimate. Statisticians call this version the Hájek estimator. You don't need group shares to use it. Each respondent's weight comes from their own telemetry: their hours, or their session count, for the week the survey ran. That is the difference from the post-stratification weights in UX201. Those correct for who *chose* to answer, using groups you know about. These correct for who your trigger *put in front* of the question, using a probability you set yourself.

Weights have a price. A survey whose weights vary a lot carries less information than its count suggests. Kish's **effective sample size** measures how much:

```
n_eff = (Σ w_i)² / Σ w_i²
```

When all weights are equal, `n_eff = n`. The more they vary, the smaller `n_eff` gets, and the wider your confidence interval (MA102 week 13) should be.

One identity explains the hook and the survey in one line. If you sample in proportion to `h`, the average `h` you see is

```
mean of h in the sample = mean(h) + variance(h) / mean(h)
```

The sample overstates the mean by the variance divided by the mean. The more unequal playtime is, the larger the overstatement. For the WoW guilds, the variance of guild size is positive, so the player-weighted mean must be above 14.5.

### Numbers you can check

An MMO has 10,000 active players in three segments. It has just capped daily quests at three per day, and asks "Do you approve of the new daily quest cap?"

| Segment | Players | Hours per week `h` | Player share | Share of online time | Approve |
|---|---|---|---|---|---|
| Casual | 6,000 | 2 | 60% | 19.7% | 70% |
| Regular | 3,000 | 8 | 30% | 39.3% | 50% |
| Hardcore | 1,000 | 25 | 10% | 41.0% | 20% |
| Total | 10,000 | mean 6.1 | 100% | 100% | |

The online time column comes from `players × h`. That is 12,000, 24,000 and 25,000 hours, 61,000 in all, so casual players supply `12,000 / 61,000 = 19.7%` of online time.

**The truth.** Approval among players is `0.6 × 0.70 + 0.3 × 0.50 + 0.1 × 0.20 = 0.59`. Most players like the cap. Casual players, who could never do more than three dailies anyway, now fall behind less.

**The online-now survey.** Weight by online time instead: `0.197 × 0.70 + 0.393 × 0.50 + 0.410 × 0.20 = 0.416`. The survey reports 41.6% approval. A producer reading it sees a feature that most players reject. It is the same player base.

**The playtime it thinks it sees.** The survey's respondents play `Σ h² / Σ h = 841,000 / 61,000 = 13.8` hours a week on average. The real average is 6.1. Check it against the identity. The variance of `h` is `(6,000 × 4 + 3,000 × 64 + 1,000 × 625) / 10,000 − 6.1² = 84.1 − 37.21 = 46.89`, and `6.1 + 46.89 / 6.1 = 13.8`.

**The fix.** Suppose 1,000 players answer, in proportion to online time: 197 casual, 393 regular and 410 hardcore. Give each a weight of `1 / h`. The segment weight totals are `197 / 2 = 98.5`, `393 / 8 = 49.1` and `410 / 25 = 16.4`, which is 60%, 30% and 10% of the total 164.0. The weighted player mix is back to the real one, and the weighted approval is 59.0%.

**The price.** `Σ w = 164.0` and `Σ w² = 197 / 4 + 393 / 64 + 410 / 625 = 56.05`, so `n_eff = 164.0² / 56.05 = 480`. Your 1,000 answers carry the information of 480 random players. The hardcore segment was over-sampled, so its extra answers add little. The casual segment was under-sampled, so each casual answer counts for a lot.

The same arithmetic in Python:

```python
segments = {  # name: (players, hours per week, share who approve)
    "casual": (6000, 2, 0.70),
    "regular": (3000, 8, 0.50),
    "hardcore": (1000, 25, 0.20),
}
players = sum(n for n, h, y in segments.values())
hours = sum(n * h for n, h, y in segments.values())
truth = sum(n * y for n, h, y in segments.values()) / players
online = sum(n * h * y for n, h, y in segments.values()) / hours
print(f"true approval {truth:.1%}, online-now survey {online:.1%}")

answered = {"casual": 197, "regular": 393, "hardcore": 410}
w = {s: answered[s] / segments[s][1] for s in segments}  # total weight per segment
estimate = sum(w[s] * segments[s][2] for s in segments) / sum(w.values())
sum_w2 = sum(answered[s] / segments[s][1] ** 2 for s in segments)
print(f"weighted {estimate:.1%}, effective sample {sum(w.values()) ** 2 / sum_w2:.0f}")
```

It prints `true approval 59.0%, online-now survey 41.6%` and then `weighted 59.0%, effective sample 480`.

### A visual you can move

Open `examples/w10-who-gets-asked.html`. The left view, "Who the survey sees", shows respondents as a stacked bar coloured by segment, with the raw approval printed above it. The right view, "Who the players are", shows the player base with the true approval. Switch the trigger between random account, at login and online now, and watch the left bar change while the right bar stays still. Then drag the hardcore hours slider from 8 to 40. The raw approval slides downward while the truth does not move at all. Tick "weight by 1/π" and the left view snaps back to the truth, while the `n_eff` counter drops. That counter is the cost of the repair, and it is the number to watch when you choose a trigger.

### Cross-game recognition

**The class size paradox (Feld and Grofman, 1977).** A university reports an average class size of 30. Its students report an average of 60. Both are right. The university averages over classes, and students average over seats, so a class of 200 counts once for the university and 200 times for students. Feld and Grofman showed that the student-side average equals the class average plus the variance over the mean, which is our identity with `h` replaced by class size. Your online-now survey is a student survey of a university that wanted to know about classes.

**The friendship paradox (Feld, 1991).** On average, your friends have more friends than you do. Pick a person and look at their friends, and you are sampling people in proportion to how many friendships they have. The most connected people show up in many friend lists. Same formula, with `h` replaced by number of friends. Guild rosters, friend lists and group finders in MMOs all have this shape. The players you meet in content are sampled in proportion to how much content they run.

**Matchmaking queues in any online game.** "Everyone in ranked is a try-hard" is the same effect. You meet opponents in proportion to how many matches they play, so the players who play ten times as many matches appear in ten times as many of your games. No fact about the game is needed to predict this, only the sampling rule. A studio that surveys players at the end of a ranked match is surveying the queue, not the ladder.

**Old School RuneScape polls (current).** OSRS runs its content votes in-game. When a poll is live, players who log in and haven't voted get a chat message pointing them to it. That puts the trigger at login, so a player who logs in every day will almost certainly see the poll during its week, while a player who logs in once a fortnight may not. Week 11 studies that system in full. For now, notice that "who votes" starts with "who was reached".

In all four, the question is the same. *In proportion to what was each person included?* Once you know `π`, you know the bias and the weight.

### Eyes-open design judgment

- **Choose the unit to match the question.** "Was your queue time acceptable today?" is a question about sessions, and an online-now survey samples sessions correctly. "Do you approve of the daily cap?" is a question about players, and needs player weights. Write down the unit before you write the trigger.
- **Prefer a trigger with equal chances.** Drawing from the account list gives every player the same `π`, so there is nothing to correct and nothing lost to `n_eff`. It costs more, because you need a way to reach players who aren't online (email, a message waiting at their next login, a launcher prompt). A message at next login is still a login trigger, so log who saw it.
- **Log `π` at the moment you ask.** You can only weight what you recorded. Store each respondent's hours and sessions for the survey week alongside the answer, from the same pipeline that feeds your KPIs (DB201 week 10). Reconstructing it later from a different table invites mistakes.
- **Weights fix reach, not willingness.** After you weight by `1/π`, the players who were asked but didn't answer are still missing. Combine this correction with UX201's nonresponse checks. They are separate problems and both are usually present.
- **Watch `n_eff`, not `n`.** An online-now survey with 5,000 answers can carry less information than a random-account survey with 2,000. Report the interval with `n_eff` in the formula, and your team will stop over-reading small moves.
- **Frequency caps change `π` too.** A rule like "don't show a player more than one survey a month" sounds neutral. It caps the chance for heavy players and raises the relative chance for light ones. That's often helpful, but it's still a sampling rule, so log it.

### Check yourself (worked example)

1. In the example, the team switches to an at-login trigger. Casual players log in 2 times a week, regular players 5 and hardcore players 12. What approval does the raw survey show?
2. A random-account survey of the same game gets 1,000 answers, and an online-now survey gets 2,000. Which has the larger effective sample size, assuming everyone asked answers?
3. Give one survey question for which the online-now trigger is the right design, and say why.

<details>
<summary>Answers</summary>

1. Login shares are `6,000 × 2 = 12,000`, `3,000 × 5 = 15,000` and `1,000 × 12 = 12,000`, 39,000 in total. Approval is `(12,000 × 0.7 + 15,000 × 0.5 + 12,000 × 0.2) / 39,000 = 18,300 / 39,000 = 46.9%`. Better than 41.6%, still well short of 59%.
2. The random-account survey has `n_eff = 1,000`. For the online-now survey, `n_eff / n = 480 / 1,000`, so 2,000 answers give about 960. The random survey is slightly better despite having half the answers.
3. Any question about the experience of a session, such as "Did you find a group in under five minutes just now?" The unit you care about is the session, and online-now samples sessions in proportion to how often they happen.

</details>

## 3. Counting the silent: how many players hit this bug?

A new patch ships. The bug forum has a thread about a quest that won't complete, and the in-game bug reporter has a stack of tickets about the same quest. The producer asks the question every live team hears: *how many players does this affect?* Adding the two channels double-counts players who used both. Using the larger one ignores everyone who used neither. There is a better answer, borrowed from ecology.

### Capture-recapture

Ecologists estimate how many fish live in a lake by catching some, tagging them, releasing them, and catching again. If the second catch contains tagged fish in the same proportion as the lake does, then

```
N ≈ n1 × n2 / m
```

- `n1` is the number caught and tagged the first time.
- `n2` is the number caught the second time.
- `m` is the number in the second catch that were already tagged.
- `N` is the estimated population.

This is the Lincoln-Petersen estimate. For bug reports, the two "catches" are two channels, and the tag is the account ID. Suppose 240 distinct accounts posted in the forum thread, 600 distinct accounts filed an in-game report, and 48 accounts appear in both. Then `N ≈ 240 × 600 / 48 = 3,000` affected players. Only 792 distinct players spoke up, so about three in four affected players said nothing anywhere.

The reasoning is simple. Among the 600 in-game reporters, 48 also posted, which is 8%. If posting is independent of using the in-game reporter, then about 8% of *all* affected players post. 240 posters is 8% of 3,000.

For small overlaps, a corrected form is less biased: `N ≈ (n1 + 1)(n2 + 1) / (m + 1) − 1`. Here that gives 2,955. Use it when `m` is below about 20, and don't trust either form when `m` is below about 7.

### Where it breaks

The formula assumes the two channels catch players independently. In games they rarely do. Engaged players both post and file reports, so the overlap `m` is larger than independence predicts, and `N` comes out **too small**. Treat the estimate as a floor. If you can, check it against telemetry. When a bug writes an error event or leaves a quest in a stuck state, count the accounts in that state directly, and use capture-recapture only for problems telemetry can't see, such as a confusing reward or a misleading tooltip.

Software engineering borrowed the same method decades ago. Eick and colleagues (1992) used it to estimate how many faults a design document still held, from how many faults two independent reviewers found and how many they both found. The lake, the design document and your quest have the same structure.

## 4. Closing the loop

Collecting feedback is the easy half. Players judge the loop by what comes back.

### Measure the loop itself

A feedback loop has a speed, and you can put numbers on it. Three are worth tracking every week.

| Measure | Definition | A reasonable target for a live MMO |
|---|---|---|
| Time to acknowledge | From the first report of a top issue to the first official reply that names it | Under 24 hours |
| Time to decision | From acknowledgement to a public "we will", "we won't" or "we need data until date X" | Under 2 weeks |
| Coverage | Share of the week's top 10 issues (by estimated players affected) with a public status | 100% |

The targets are a starting point, not an industry standard. Set your own and publish them. MMO305 week 12 explained why kept promises build trust. These measures turn "we listen" into something a producer can check on a dashboard.

### Rank issues by players, not by volume

A thread with 2,000 replies and a bug that 30,000 players hit silently are not comparable by reply count. For each issue, keep three numbers.

- **Reach**, the estimated number of players affected. Use telemetry, a weighted survey or capture-recapture, in that order of preference.
- **Severity**, what it costs each affected player: a blocked quest, lost items, a cosmetic glitch. A four-level scale is enough.
- **Confidence**, how good your reach estimate is. A floor from two correlated channels deserves less trust than a count from an error event.

Sort by reach times severity, and show confidence next to it. The loudest issue will often come out near the top. When it doesn't, you will have a number to show the community team when they ask why.

### Tell players what happened

Every change that came from feedback should say so. "You told us the daily cap hurt players who log in late in the day. We moved the reset to your local time." That sentence closes one loop and makes players more willing to use the next one. A change you made against the feedback deserves the same treatment, with the number that decided it. "The forum was strongly against the cap, but a survey of 2,000 randomly chosen players found 59% approve, so we are keeping it." Players can disagree with a number. They can't check a feeling.

## 5. From surveys to polls

Every channel in this lecture is **advisory**. The team listens, weighs, and decides. A **binding** poll is different. The team commits in advance to do what the vote says. That changes three things. Players who would never answer a survey will vote, because the vote has consequences. Organised groups will mobilise to swing it, so the voting rule matters as much as the question. And the team gives up the option to overrule a result it thinks is wrong.

Old School RuneScape is the best-known game that runs on binding polls, and in 2025 it split its polls into types. "Opinion surveys" gauge attitudes and have no pass mark, "greenlight" polls approve a concept for more design work, and "lock-in" polls commit the team to ship. That is this lecture's advisory channel and next week's binding one, living side by side in the same interface. Week 11 works through the pass threshold, who is allowed to vote, and what a supermajority does to the content that gets made.

## In-class activity (25 minutes)

Pairs. Your team runs a mid-sized MMO. A new crafting system launched two weeks ago. You have three sources:

- A forum thread: 1,100 posts, 68% negative, 310 distinct posting accounts.
- An end-of-session survey (shown when a player logs out, at most once per player): 2,400 answers, 44% satisfied.
- Telemetry: 40,000 weekly active players. Crafting sessions per week by segment: casual players (65% of players) average 1, regulars (25%) average 4, crafters (10%) average 15. Satisfaction is unknown.

1. Name the unit the end-of-session survey samples. Is it sessions, crafting sessions or players? What does the "at most once per player" cap do to `π`?
2. Suppose `π` is proportional to sessions per week, capped at one ask, and that asked players always answer. The raw survey mix is then equal to the session shares. Compute those shares. If satisfaction is 60% (casual), 45% (regular) and 30% (crafters), what does the raw survey show and what is the player-weighted truth?
3. The bug reporter shows 520 accounts reporting a crafting bug, of which 65 also posted in the forum thread. Estimate the number of affected players. Is it a floor or a ceiling, and why?
4. Write the two-sentence public reply that closes the loop, using one number from step 2 and one from step 3.

Expected output: answers to steps 1 to 3 with the arithmetic shown, and the reply.

## Common misconceptions

- **"A bigger survey is a better survey."** Only if everyone had the same chance of being asked. An online-now survey with 5,000 answers can carry less information than a random-account survey with 2,000. Compare `n_eff`, not `n`.
- **"Weighting fixes all survey bias."** Weighting by `1/π` fixes the bias from your trigger. It doesn't fix who declined to answer (UX201) or who is louder (MMO305). Those need their own corrections.
- **"Players who report a bug are the players who have it."** Most affected players never report. Capture-recapture gives you a floor on the rest, and telemetry gives you the count when the bug leaves a trace.
- **"Online-now surveys are always wrong."** They are right for questions about sessions. They are wrong for questions about players. Pick the unit first.

## Check yourself

1. A survey pops up for players online now. Segment A (80% of players) plays 3 hours a week and 50% of them like a change. Segment B (20% of players) plays 27 hours a week and 90% of them like it. What does the raw survey show, and what is the truth?
2. In question 1, 1,000 players answer in proportion to online time. Compute `n_eff` for the `1/h`-weighted estimate.
3. Two bug channels catch 150 and 400 distinct accounts, with 30 in both. Estimate the number of affected players with both formulas from section 3. Would you expect the true number to be higher or lower, and why?
4. A designer wants to know "how long do players wait for a dungeon group?" Should the answer be averaged per session or per player? Give a case where the two differ a lot.
5. A team shows every player one survey per month at login, and logs nothing else. Months later they want to weight the answers. What have they lost, and what should they have stored?

<details>
<summary>Answers</summary>

1. Online time is `0.8 × 3 = 2.4` and `0.2 × 27 = 5.4`, so B supplies `5.4 / 7.8 = 69.2%` of respondents. Raw: `0.308 × 0.5 + 0.692 × 0.9 = 77.7%`. Truth: `0.8 × 0.5 + 0.2 × 0.9 = 58%`. Here the heavy players like the change, so the survey overstates approval.
2. Respondents: 308 in A, 692 in B. Weights `1/3` and `1/27`. `Σ w = 102.7 + 25.6 = 128.3`. `Σ w² = 308 / 9 + 692 / 729 = 34.2 + 0.95 = 35.2`. `n_eff = 128.3² / 35.2 ≈ 468`.
3. Lincoln-Petersen: `150 × 400 / 30 = 2,000`. Corrected: `151 × 401 / 31 − 1 ≈ 1,952`. The true number is probably higher, because engaged players tend to use both channels, which inflates `m` and shrinks the estimate.
4. Both are legitimate, but they answer different questions. Per session tells you what a typical queue feels like. Per player tells you what a typical player experiences across their week. If casual players queue at off-peak hours and wait 20 minutes while heavy players queue at peak and wait 2, the per-session average is dominated by the heavy players' many short waits, and the per-player average is dominated by the casual players' few long ones.
5. They lost `π`. Each player's chance of being asked depended on how often they logged in, and the survey didn't record it. They should have stored each respondent's sessions and hours for the survey month, plus the frequency-cap state, with the answer.

</details>

## Lab / assignment hook

[Lab 10, who answered the survey?](../labs/lab10.md) You get an in-game survey export with 3,000 answers, the telemetry for every respondent, and the account lists from two bug-report channels. You implement the raw, inverse-probability weighted and effective-sample-size calculations, estimate the affected players for a bug with capture-recapture, compare with the telemetry count, and write a one-page note to a producer. This lab counts toward the analytics labs (40%).

## Sources

- Ducheneaut, N., Yee, N., Nickell, E. & Moore, R. J. (2006). "'Alone Together?' Exploring the Social Dynamics of Massively Multiplayer Online Games." *Proceedings of CHI 2006*, 407-416. doi:10.1145/1124772.1124834. World of Warcraft census data from 2005, US servers. Mean guild size 14.5, median 6, largest 257. Checked against the author-hosted PDF, September 2026.
- Feld, S. L. & Grofman, B. (1977). "Variation in class size, the class size paradox, and some consequences for students." *Research in Higher Education* 6(3), 215-222. doi:10.1007/BF00991287.
- Feld, S. L. (1991). "Why Your Friends Have More Friends Than You Do." *American Journal of Sociology* 96(6), 1464-1477. doi:10.1086/229693.
- Eick, S. G., Loader, C. R., Long, M. D., Votta, L. G. & Vander Wiel, S. (1992). "Estimating software fault content before coding." *Proceedings of the 14th International Conference on Software Engineering*, 59-65. doi:10.1145/143062.143090.
- Old School RuneScape Wiki, "Polls" (accessed September 2026). In-game voting with a login chat message during live polls; poll types after the 2025 poll system improvements (lock-in, greenlight, opinion surveys).
- Seif El-Nasr, M., Drachen, A. & Canossa, A. (eds.) (2013). *Game Analytics: Maximizing the Value of Player Data*. Springer. Chapter 8 (Drachen, Gagné & Seif El-Nasr, "Sampling for Game User Research") and chapter 25 (Weedon, "Game Metrics Through Questionnaires").
- Kish, L. (1965). *Survey Sampling*. Wiley. The effective sample size formula for weighted samples.

## Interactive spec: examples/w10-who-gets-asked.html

**Insight the visual must make obvious:** the survey trigger decides who gets asked. An online-now survey over-counts heavy players by their playtime and can reverse the answer, and weighting each respondent by `1/π` restores the truth at a cost in effective sample size.

**Layout.** Two linked horizontal stacked bars, one above the other on mobile and side by side on desktop, each 100% wide and coloured by segment (casual, regular, hardcore; use three categorical tokens from the shared palette). Above each bar, a large approval percentage.

- **Left, "Who the survey sees".** Segment shares of respondents under the chosen trigger. When "weight by 1/π" is ticked, the bar shows the weighted shares and the label changes to "Who the survey sees, weighted".
- **Right, "Who the players are".** Segment shares of players. Never changes with the trigger.
- **Under the bars.** A readout row: raw approval, weighted approval, true approval, gap (raw minus true, in points, signed), `n` and `n_eff`.
- **Below.** A small table of the three segments with columns players, hours per week, logins per week, approve, share of players, share of respondents, weight per respondent.

**Controls.**
- Trigger: radio buttons "Random account" (`π ∝ 1`), "At login" (`π ∝ s`), "Online now" (`π ∝ h`). Default "Online now".
- Sliders per segment: players (0 to 10,000, step 100), hours per week `h` (1 to 40, step 1), logins per week `s` (1 to 21, step 1), approve (0 to 100%, step 1).
- Respondents `n`: slider 100 to 5,000, step 100, default 1,000.
- Checkbox "Weight by 1/π", default off.
- Reset button.

**Formulas.** For segment `k` with `N_k` players, `h_k`, `s_k`, approval `y_k`, and trigger value `t_k` (1, `s_k` or `h_k`):
- Share of respondents: `q_k = N_k t_k / Σ_j N_j t_j`. Respondent counts are `n_k = n × q_k`, unrounded.
- Raw approval: `Σ q_k y_k`.
- True approval: `Σ N_k y_k / Σ N_k`.
- Weighted approval: `Σ (n_k / t_k) y_k / Σ (n_k / t_k)`. With exact `n_k` this equals the true approval.
- Effective sample size: `n_eff = (Σ n_k / t_k)² / Σ (n_k / t_k²)`.
- Also show "average hours of respondents" `Σ q_k h_k` next to "average hours of players" `Σ N_k h_k / Σ N_k`.

**Defaults and test values.** Casual 6,000 players, `h = 2`, `s = 2`, 70%. Regular 3,000, `h = 8`, `s = 5`, 50%. Hardcore 1,000, `h = 25`, `s = 12`, 20%. `n = 1,000`.
- Online now: respondent shares 19.7% / 39.3% / 41.0%; raw 41.6%; true 59.0%; weighted 59.0%; `n_eff = 480`; respondent hours 13.8 vs player hours 6.1.
- At login: shares 30.8% / 38.5% / 30.8%; raw 46.9%; `n_eff = 696`.
- Random account: shares 60% / 30% / 10%; raw 59.0%; `n_eff = 1,000`.
- Online now with hardcore `h = 40`: raw falls to 37.4%, true stays 59.0%.

**Behaviour.** Every control updates both bars and the readouts immediately. The approval numbers animate with a short tween unless `prefers-reduced-motion` is set. When the gap exceeds 10 points, the left percentage turns the warning colour. When raw and true fall on opposite sides of 50%, show a one-line note, "The survey and the players disagree on the majority."

**Accessibility.** All controls keyboard operable with visible focus. Bars have text equivalents (segment share percentages in the table). Colour is never the only cue: each bar segment is labelled with its share when wide enough.

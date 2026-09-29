# MMO308 · Week 11 — Community-Voted Design: Old School RuneScape Polls

**Why this matters:** A few live games let players vote on what gets built, and commit to the result. Old School RuneScape has run that way since 2013. A binding vote needs a rule, and the rule decides which content exists. The pass mark sets how many "no" votes it takes to cancel a "yes", who can vote sets whose "no" counts, and the wording of the ballot sets what a "yes" means. Change any of the three and a different game gets made.

**You will be able to:**
- Compute whether a poll question passes at a threshold, how many "no" votes it takes to block it, and what share of the active player base that is at a given turnout.
- Use a real archive of 3,304 poll questions to measure how many decisions a change of threshold actually flips.
- Critique a poll's design for eligibility, turnout, skip handling, hidden results and question bundling.
- Design a voting rule for a live game, choosing between advisory, greenlight and binding votes, with a threshold you can defend in numbers.

**Before class:** Jagex, "Polling Changes" (Old School RuneScape news, 27 October 2022), and the "Polling Charter" linked from it. Skim the Old School RuneScape Wiki's "Polls" page, including the list of past polls. Reread MMO402 week 3 if you have taken it.

**Prerequisites from earlier courses:** [MMO308 week 10, player feedback loops](w10-player-feedback-loops-forums-surveys-polls.md) (who a trigger reaches; advisory versus binding channels). [MA102 week 13, sampling and confidence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (why a huge self-selected sample can still be biased). [MMO305 week 12, community management](../../MMO305-social-systems-and-online-behaviour/lectures/w12-community-management.md) (voice, exit and closing the loop). Optional for year-4 students: [MMO402 week 3, EVE's Council of Stellar Management](../../MMO402-emergent-society-governance-and-ethics/lectures/w03-eves-council-of-stellar-management.md), which studies an elected advisory council and its voting rule.

**Interactive:** [Poll threshold](../examples/w11-poll-threshold.html). Keep it open during section 2.

---

## 1. A game that asks before it changes

Old School RuneScape (OSRS) began as a vote. In February 2013 Jagex asked players whether it should reopen a copy of RuneScape as it had been in August 2007, with promises that grew with turnout. At 50,000 votes, a bare server with a separate fee. At 500,000, the game would come free with membership and get content updates. At 750,000, regular polls on new content. The poll closed on 1 March 2013 with 449,351 votes, short of the third tier. Jagex launched the game anyway, and in June 2013 said it would stay with no extra fee.

The promise of player polls stuck. From March 2013 onward, Jagex has put proposed content to players in polls, and committed not to add polled content that fails. Three rules define the system as it stands in 2026, according to the OSRS Wiki.

1. **Who votes.** Members with a total level of at least 300 and at least 25 hours of play time. Voting happens in-game at poll booths. A player who logs in during a live poll and hasn't voted gets a chat message about it.
2. **What counts.** Each question offers "Yes", "No" and, since 11 February 2016, "Skip question". Skips are left out of the count. Since 12 April 2019, results are hidden until the poll closes.
3. **What passes.** A question passes if "Yes" reaches the threshold of the votes cast for "Yes" and "No". The threshold was 75% until 27 October 2022, when Jagex lowered it to 70%.

A **supermajority** rule like this one needs more than half the votes. It is the central design choice in any binding vote, so it gets its own model.

## 2. Worked example: the 70% line

### The hook

In August 2023, OSRS players voted on whether to add Sailing, the game's first new skill since the 2013 relaunch. The result was 112,976 "Yes", 44,153 "No" and 4,252 skips, so Yes had 71.9% of the votes that count. Sailing passed and was released on 19 November 2025.

Four years earlier, a different new skill, Warding, went to a vote. It got 82,633 "Yes" and 41,726 "No", 66.4%. Jagex's results post said it had failed to reach the 75% approval mark, and Warding was dropped.

Two skills, both with clear majorities. One is in the game and one is not. Sailing at 71.9% would also have failed under the rule that sank Warding. The difference between the two outcomes is partly the content and partly a line that moved by five points in October 2022. Why did Jagex move it, and what does five points buy?

### The model

Let `Y` and `N` be the "Yes" and "No" votes on a question. Skips are ignored. The **yes share** is

```
s = Y / (Y + N)
```

and the question passes if `s ≥ T`, where `T` is the threshold.

Rearrange the pass condition and a second, more useful reading appears. The question passes if

```
N ≤ Y × (1 − T) / T
```

So each "No" vote cancels `T / (1 − T)` "Yes" votes. At a simple majority, `T = 50%`, one cancels one. At 75%, one "No" cancels three "Yes". At 70%, one cancels 2.33.

Turn it around once more. To block a question, opponents need more than a share `1 − T` of the votes cast. Now bring in **turnout** `τ`, the share of eligible players who vote. If opponents all vote and the rest of the voters split any way at all, the smallest group of eligible players that can block anything is

```
blocking share of the player base = τ × (1 − T)
```

- `s` is what the poll reports.
- `T` is the rule.
- `T / (1 − T)` is the exchange rate between a "No" and a "Yes".
- `τ × (1 − T)` is how small a group can stop a change.

### Numbers you can check

Jagex said in its 2022 announcement that fewer than 6% of active members vote in polls. Set `τ = 6%`.

| Threshold `T` | "No" share that blocks | "Yes" votes one "No" cancels | Blocking share of active members at `τ = 6%` |
|---|---|---|---|
| 50% | over 50% | 1 | 3.0% |
| 60% | over 40% | 1.5 | 2.4% |
| 66.7% (two thirds) | over 33.3% | 2 | 2.0% |
| 70% | over 30% | 2.33 | 1.8% |
| 75% | over 25% | 3 | 1.5% |
| 80% | over 20% | 4 | 1.2% |

Check the 75% row against the source. Jagex wrote that with a 75% pass rate, it took only 1.5% of active members voting "No" to stop content. That is `6% × 25%`, the model's last column. The company's own reason for lowering the threshold is this formula.

Now apply the model to Sailing. At 70%, the question passes while `N ≤ 112,976 × 0.3 / 0.7 = 48,418.3`. It got 44,153 "No" votes. Another 4,266 "No" votes would have sunk it, about 2.6% of the 161,381 ballots cast. Or, if 2,986 "Yes" voters had switched to "No", 2.6% of them, it would have failed. At 75%, the limit is `112,976 / 3 = 37,658.7`, and it already had 6,494 more "No" votes than that.

Warding, by contrast, was not close to either line. At 70% it could survive at most 35,414 "No" votes against its 41,726. Lowering the threshold would not have saved it. A threshold change moves only the questions near the line.

The same calculation in Python, with exact fractions so the boundary case can't be decided by floating-point error:

```python
from fractions import Fraction


def passes(yes, no, t):
    """True if the yes share of yes + no votes reaches threshold t. Skips don't count."""
    return Fraction(yes, yes + no) >= t


def no_votes_to_block(yes, t):
    """Smallest number of 'no' votes that makes `yes` fail at threshold t."""
    allowed = yes * (1 - t) / t  # the most 'no' votes that still let it pass
    return int(allowed) + 1


yes, no = 112_976, 44_153  # Sailing, Summer Summit 2023 Giga Poll
print(f"yes share {yes / (yes + no):.1%}")
for t in (Fraction(70, 100), Fraction(75, 100)):
    need = no_votes_to_block(yes, t)
    print(f"T = {float(t):.0%}: passes {passes(yes, no, t)}, "
          f"blocking needs {need:,} no votes ({need - no:+,} against the actual count)")
```

It prints:

```
yes share 71.9%
T = 70%: passes True, blocking needs 48,419 no votes (+4,266 against the actual count)
T = 75%: passes False, blocking needs 37,659 no votes (-6,494 against the actual count)
```

### What the line does across 3,304 questions

One poll is an anecdote. The OSRS Wiki keeps an archive of every poll with its vote counts. For this lecture, every question with a "Yes" and "No" answer was tallied from that archive, from the first poll on 14 March 2013 to one that opened on 21 September 2026. That gives 3,304 questions. Treat the tally as this course's own count. It includes a few survey-style questions that were never meant to decide content, and it doesn't know which questions carried special voting restrictions.

| Period | Questions | Median yes share | Passed at the rule in force | Between 70% and 75% |
|---|---|---|---|---|
| Before 27 Oct 2022 (75% rule) | 2,647 | 86.1% | 2,069 (78.2%) | 177 (6.7%) |
| From 27 Oct 2022 (70% rule) | 657 | 89.7% | 633 (96.3%) | 21 (3.2%) |
| All | 3,304 | 86.9% | | 198 (6.0%) |

Three things stand out.

1. **Most questions aren't close.** The median question got about 87% "Yes". That matches Jagex's own remark in 2022 that most polled content passes with 80% or more. A threshold matters only for the contested minority.
2. **The five points that moved would have changed 177 earlier results.** Under a 70% rule, 6.7% of the questions that failed or passed before October 2022 would have gone the other way. Since the change, 21 questions, Sailing among them, have passed only because the line moved.
3. **The pass rate rose for another reason too.** Even judged at 75%, 93.2% of questions after October 2022 would have passed, against 78.2% before. The threshold can't explain that. What changed is *what gets polled*. The Polling Charter published at the same time took bug fixes, quality-of-life changes, integrity changes and more off the ballot. From August 2023 the team also ran greenlight polls on concepts before writing full proposals. A lower threshold and better-screened proposals both push the pass rate up. You can only separate them with data like this.

### A visual you can move

Open `examples/w11-poll-threshold.html`. The left view is one ballot, a bar split into "Yes" and "No", with the threshold as a vertical line and a marker showing how many more "No" votes would block it. It starts on Sailing. The right view is a histogram of all 3,304 yes shares from the archive, with bars left of the threshold in the "fail" colour. Drag the threshold from 75% to 70%. On the left, Sailing flips from fail to pass. On the right, a thin band of bars changes colour while the tall mass above 80% doesn't move at all. The readout counts the flipped questions. Then drag the turnout slider and watch the "smallest blocking group" figure, `τ × (1 − T)`, shrink as fewer players vote.

### Cross-game recognition

**The US Constitution (Article V, since 1789).** An amendment needs two thirds of both houses of Congress to propose it and three fourths of the states to ratify it. With 50 states, ratification needs 38, so any 13 states can block. Rewritten in our form, `T = 75%` counted in states, and the blocking share is just over 25% of states. It is the same rule OSRS used until 2022, applied to a different unit. Both make the status quo win whenever opinion is split, which is the point of a rule for changing a foundation.

**Minecraft's Mob Vote (2017 to 2023).** Each year Mojang put three or four candidate mobs or biome updates to a public vote, added the winner, and shelved the rest. That is a **plurality** vote with no status-quo option. Something always gets added, and the winner needs only more votes than each rival, which in a three-way race can be well under half. In our model, there is no `T` at all, and no blocking group exists. Mojang discontinued the vote on 9 September 2024. Plurality settles which of several options to build, and a supermajority settles whether to change anything at all. A designer should pick the rule that answers the question actually being asked.

**The 2013 OSRS founding poll.** The first OSRS vote had a threshold of a different kind. Its tiers were set by **turnout**, not by yes share: 250,000 votes for one level of service, 500,000 for the next. At 449,351, it fell short of the tier that promised content updates. A turnout threshold asks "do enough people care?" A share threshold asks "do enough of those who care agree?" The same studio used both, for different questions.

**EVE Online's Council of Stellar Management (2008 onward).** CCP's elected player council is **advisory**. It advises the developers and has no vote on what ships. The voting rule there decides who sits on the council, and MMO402 week 3 works through it. Compare it with OSRS, where the vote decides the content directly and nobody stands between the ballot and the patch notes.

Four systems, one question. What share of the votes can stop a change, and what share of the people is that?

### Eyes-open design judgment

- **A supermajority protects the status quo.** That is its purpose. In a long-running game, the existing design is something players have invested years in, and a high `T` makes that investment hard to take away. The cost is that popular content can fail. At 75%, a question with 74% support fails, which is a result many players find absurd.
- **The threshold and turnout multiply.** A high threshold with low turnout hands the veto to a very small group. Jagex's 1.5% figure is `τ × (1 − T)`. If you can't raise turnout, a lower threshold is the only way to widen the group needed to block. If you can raise turnout, you may keep a high threshold with a broader base.
- **Only the contested band moves.** Lowering `T` by five points flipped about 6% of historical questions in OSRS. Before you change a threshold, count the questions in the band. If there are almost none, the change is symbolic. If there are many, look at them one by one. They are the content your rule is deciding about.
- **What you put on the ballot matters as much as the line.** The post-2022 pass rate rose mostly because of screening. A team that polls only well-tested proposals will see high pass rates at any threshold, and a team that polls rough ideas will see failures at any threshold.
- **A vote is also a promise.** Jagex's 2022 post described the risk of polls offering "an illusion of choice" when proposals arrive so fully designed that a "No" only wastes work. A binding vote is most useful early, on a concept, before the work is sunk.

### Check yourself (worked example)

1. A question gets 30,000 "Yes", 12,000 "No" and 5,000 skips. What is the yes share? Does it pass at 70%? How many extra "No" votes would block it?
2. A game with 400,000 eligible players uses `T = 2/3` and sees 10% turnout. What is the smallest group of eligible players that can block any question?
3. A designer proposes counting skips as "No" votes. What does that do to the pass condition? Use the numbers from question 1.

<details>
<summary>Answers</summary>

1. `30,000 / 42,000 = 71.4%`. It passes at 70%. The limit is `30,000 × 0.3 / 0.7 = 12,857.1`, so 12,858 "No" votes block it, 858 more than it got.
2. `10% × (1 − 2/3) = 3.3%` of eligible players, about 13,334 players (just over one third of the 40,000 voters).
3. The yes share becomes `Y / (Y + N + skips) = 30,000 / 47,000 = 63.8%`, and the question fails. Counting skips as "No" turns indifference into opposition, so every question with many skips gets harder to pass. OSRS introduced skip precisely so indifferent players wouldn't have to pick a side.

</details>

## 3. Who votes

A binding vote is still a sample, and week 10's first question applies. *In proportion to what was each player included?*

### Eligibility

OSRS requires membership, a total level of 300 and 25 hours of play. Each rule has a job. Membership ties a vote to a paying account, which makes buying votes with throwaway accounts expensive. The level and hours rules stop new accounts made for a single poll. The side effect is that free players and brand-new players have no voice, even on content aimed at them. The Polling Charter's answer is to take content for new players off the ballot entirely. The Polling Changes post gave the reason plainly. The new players that content is for aren't able to vote.

Eligibility is a design decision with the same shape as a survey trigger. It sets a chance of inclusion `π` for each player type. Write it down, and ask whose opinion the rule leaves out.

### Turnout and reach

Voting happens in-game, and a login message reminds players who haven't voted. That is a login trigger in week 10's terms. A player who logs in daily almost certainly sees the poll during its week. A player who logs in once a month may miss it. So even among eligible players, the voters lean toward the most active. When Jagex says fewer than 6% of active members vote, those 6% are not a random 6%.

Low turnout is not automatically a flaw. Players who don't care about a mining change can reasonably not vote on it. The problem arises when a group that cares a lot, and plays a lot, is outvoted or out-vetoed on content that also affects players who didn't vote. The 2022 change to 70% was an attempt to fix that by moving `T`. Summits followed by one large poll on everything announced, which Jagex proposed in the same announcement, were an attempt to raise `τ`. The Summer Summit 2023 poll that passed Sailing drew 161,381 ballots, more than the Warding poll's 125,147, which Jagex had called the largest content poll in the game's history at the time.

### Skips and hidden results

Two quieter rules shape the count.

- **Skip question.** Before February 2016, a player who didn't care still had to pick "Yes" or "No" on every question. Indifferent votes are noise, and they tend to pull shares toward the middle. With skip, `Y + N` counts only players with an opinion. In the archive, the median question since skip was introduced drew about 7% skips.
- **Hidden results.** Since April 2019, running totals stay hidden until the poll closes. A visible total invites strategic voting. A group sees a question sitting at 76% and mobilises "No" votes to push it under the line, or a close result draws bandwagon votes. Hiding the count removes that feedback during the vote.

## 4. Designing the ballot

The model assumes each question is a clean yes or no. Real ballots are written by people, and the writing changes the result.

### Bundling and conditional questions

The Warding poll asked first whether to add the skill, then asked a series of follow-ups beginning "If question 1 passes, should we…" about specific parts of it. The first question got 66.4%. Eleven of the fifteen follow-ups got between 70% and 74%, and one, a Warding Guild, reached 73.8%. A player who opposed the skill could still vote "Yes" on the parts they'd want if it came anyway, or skip. So a conditional question measures a different thing from the main question, and its share can't be compared with it directly.

Bundling works the other way. Put two changes in one question, one popular and one not, and the popular one can carry the other over the line, or the unpopular one can sink both. The general rule is one decision per question. Break that rule only when two changes truly can't exist apart, and say so on the ballot.

### Greenlight, lock-in and opinion

OSRS now labels its polls by commitment. Since August 2023 the interface has shown "greenlight", "lock-in" and "opinion" categories, and the 2025 poll-system update formalised them. A greenlight poll that passes 70% means a fuller design will be developed and polled again. A lock-in poll that passes 70% commits the team to ship, as long as delivery stays reasonably possible. An opinion survey has no pass mark. That is the week 10 distinction between advisory and binding channels, built into the ballot.

Two-stage voting has a clear benefit. Players can reject a concept before the team spends months on it, which answers the "illusion of choice" worry directly. The cost is time. Sailing passed its poll in August 2023 and launched in November 2025, more than two years later. In between, two Sailing polls in June and August 2025 decided its islands, quests, resources and potions question by question.

### What not to poll

The Polling Charter lists changes that don't need a vote. It includes bug fixes, quality-of-life improvements, graphical updates, temporary events, new game modes, content for new players, membership and bond prices, accessibility changes, and changes made for game integrity and balance. The list has a logic you can reuse.

- **Changes that fix what players already agreed to** (bugs, integrity). Voting on whether a bug should be fixed invites the players who profit from it to vote.
- **Changes whose audience can't vote** (new-player content, accessibility for players who may find the poll booth itself hard to use).
- **Changes the business must control** (prices).
- **Changes that are temporary or separate from the main game** (events, other game modes).

## In-class activity (25 minutes)

Groups of three. Your studio runs a mid-sized MMO with 120,000 monthly active players and wants to let players vote on content. Past surveys suggest 8% of players will vote in a well-promoted poll.

1. Pick a threshold between 50% and 80%. Compute `T / (1 − T)` and the smallest blocking group as a share of monthly actives and as a number of players.
2. Write eligibility rules. For each rule, name one group it leaves out and say whether that is acceptable.
3. List three kinds of change you won't poll, with a one-line reason each, and one kind you will always poll.
4. Here are last year's advisory survey results on ten proposals, as yes shares: 58, 64, 68, 71, 73, 77, 82, 86, 90, 94. How many pass at your threshold? How many would flip if you moved it five points either way?
5. Swap with another group and find the proposal type their rule handles worst.

Expected output: the threshold with its two numbers, eligibility rules, the not-polled list, the answer to step 4, and the weakness your partners found.

## Common misconceptions

- **"A 70% threshold means 70% of players want it."** It means 70% of the players who voted "Yes" or "No" did. With 6% turnout, that can be about 4% of active players.
- **"Raising the threshold makes decisions more democratic."** It makes them more conservative. A higher threshold gives a smaller group the power to block, so it concentrates veto power.
- **"Lowering the threshold changes many results."** In OSRS, moving from 75% to 70% flipped about 6% of historical questions. Most questions weren't close.
- **"Skips are just abstentions, so they don't matter."** Whether skips count decides the denominator. Counting them as "No" would have sunk many questions that pass today.

## Check yourself

1. A question receives 64,000 "Yes" and 26,000 "No". Does it pass at 70%? At 75%? How many voters would have to switch from "No" to "Yes" to pass at 75%?
2. A game lowers its threshold from 80% to 70% and keeps turnout at 5%. By what factor does the smallest blocking group grow?
3. Using the archive table, what share of all 3,304 questions pass at 70% but fail at 75%? Why is that share larger before October 2022 than after?
4. A studio polls a popular new zone and an unpopular currency change in one question. Explain two ways this can go wrong, and propose a better ballot.
5. Minecraft's Mob Vote let the community choose one of three mobs. Rewrite it as a set of OSRS-style yes/no questions. What new outcome becomes possible that the original vote could never produce?

<details>
<summary>Answers</summary>

1. `64,000 / 90,000 = 71.1%`. Passes at 70%, fails at 75%. At 75%, it needs `Y ≥ 0.75 × 90,000 = 67,500`, so 3,500 voters must switch.
2. From `5% × 20% = 1%` to `5% × 30% = 1.5%`, a factor of 1.5.
3. 198 of 3,304, or 6.0%. Before October 2022 the share was 6.7%, after it 3.2%. After the change, the team screened proposals harder and polled fewer contested ideas, so fewer questions landed near the line.
4. The popular zone can carry the currency change through, so players get something most of them opposed. Or the currency change can sink the zone, so players lose something most of them wanted. Either way, the result doesn't say which part players rejected. Split it into two questions, and if the zone truly needs the currency change, say why on the ballot.
5. Three questions, "Should we add mob A?", and the same for B and C, each at a threshold. Now all three can fail, and the game adds nothing. Several could also pass. The plurality vote always added exactly one.

</details>

## Lab / assignment hook

[Lab 11, the poll archive](../labs/lab11.md). You get the 3,304 OSRS poll questions as a CSV. You implement the pass and blocking functions, draw the pass-rate-by-threshold curve, find the questions that a threshold change flips, test whether skips and conditional questions behave differently, and write a one-page voting rule for a game of your own. This lab counts toward the analytics labs (40%).

## Sources

- Old School RuneScape Wiki, "Polls" (accessed September 2026). Eligibility (members with total level 300 and 25 hours of play), in-game poll booths and the login chat message; skip option from 11 February 2016; results hidden from 12 April 2019; threshold changed from 75% to 70% on 27 October 2022; Polling Charter (October 2022) list of unpolled changes; greenlight, lock-in and opinion categories (16 August 2023) and the 2025 poll-system improvements.
- Jagex, "Polling Changes", Old School RuneScape news, 27 October 2022 (via the OSRS Wiki's copy, "Update:Polling Changes"). Fewer than 6% of active members vote; 1.5% of active members could block at 75%; most polled content passes with 80% or more; threshold lowered to 70%; the "illusion of choice" concern; plans for summits followed by large polls; new-player content not polled because its audience can't vote.
- Old School RuneScape Wiki, "Poll:Summer Summit 2023 - Giga Poll" (poll open 19 to 25 August 2023). Sailing: 112,976 Yes, 44,153 No, 4,252 skips, 161,381 total ballots.
- Old School RuneScape Wiki, "Sailing" (accessed September 2026). Passed with 71.9%; released 19 November 2025.
- Jagex, "Warding Poll Results", Old School RuneScape news, 24 July 2019 (via the OSRS Wiki's "Update:Warding Poll Results"). 82,633 Yes (66.4%), 41,726 No; failed the 75% mark; 125,147 votes, the largest content poll to that date. Follow-up question results from "Poll:Warding Skill" in the same wiki.
- Old School RuneScape Wiki, "Old School RuneScape" (accessed September 2026). The February 2013 poll, its vote tiers (50,000, 250,000, 500,000, 750,000), the final count of 449,351 on 1 March 2013, the August 2007 backup, and the June 2013 announcement of no extra fee.
- Archive tally: this course's own count of all yes/no questions on the pages listed under "List of polls" on the OSRS Wiki "Polls" page, 14 March 2013 to 21 September 2026, fetched September 2026 through the wiki's API. 3,304 questions. The data file is in the lab 11 starter.
- Minecraft Wiki, "Community Vote" (accessed September 2026). Mob and biome votes from MINECON Earth 2017 to Minecraft Live 2023; winner added, others shelved; discontinued 9 September 2024, citing Mojang's "The future of Minecraft's development".
- US National Archives, "The Constitution of the United States: A Transcription", Article V. Two thirds of both houses to propose; ratification by three fourths of the states.

## Interactive spec: examples/w11-poll-threshold.html

**Insight the visual must make obvious:** a supermajority threshold only decides the contested questions. Moving it from 75% to 70% flips a thin band of results (Sailing among them) while most questions sit far above both lines, and at low turnout a very small group can block anything.

**Data.** Embed the 3,304 yes shares from `labs/lab11-starter/osrs_polls.csv` (yes share = `yes / (yes + no)`), as integers in hundredths of a percent, floored (`floor(10000 × yes / (yes + no))`, so a share never rounds up past a threshold), plus a parallel array of opened dates (ISO) so the era toggle works.

**Layout.** Two linked views, side by side on desktop, stacked on mobile.

- **Left, "One ballot".** A horizontal bar split into Yes (left) and No (right), proportional to `Y` and `N`. A vertical line at `T`. A dashed marker at the "No" count that would block the question, labelled "blocked at N = …". Above the bar, the yes share and "PASSES" or "FAILS". A dropdown picks the ballot: Sailing 2023 (112,976 / 44,153), Warding 2019 (82,633 / 41,726), or "Custom" with two number inputs for Yes and No.
- **Right, "Every question since 2013".** A histogram of yes shares, 1-point bins from 0% to 100%. Bars below `T` in the fail colour, at or above in the pass colour, and bars between 70% and 75% outlined so the historic band is always visible. A vertical line at `T`.
- **Readouts under the views.** Questions passing at `T`, share passing, questions whose result differs between `T` and the comparison threshold (default 70%, so the first screen shows the 198 questions in the historic band), yes votes cancelled by one no (`T / (1 − T)`), and smallest blocking group `τ × (1 − T)` as a percentage of eligible players.

**Controls.**
- Threshold `T`: slider 50% to 90%, step 0.5, default 75%. Buttons "75% (2013-2022)" and "70% (since Oct 2022)" set it directly.
- Comparison threshold: 70% by default, editable.
- Turnout `τ`: slider 1% to 50%, step 0.5, default 6%.
- Era: "All", "Before 27 Oct 2022", "From 27 Oct 2022".

**Formulas.** Pass if `Y / (Y + N) ≥ T`. Blocking "No" count `floor(Y × (1 − T) / T) + 1` (use integer arithmetic on tenths of a percent to avoid float error at the boundary). Exchange rate `T / (1 − T)`. Blocking group `τ × (1 − T)`.

**Test values.**
- Sailing at 70%: passes; blocks at 48,419 No. At 75%: fails; would need at most 37,658 No.
- Warding at 70%: fails; allowed at most 35,414 No against 41,726.
- All questions passing at 50%, 60%, 66.7%, 70%, 75%, 80%, 90%: 3,204; 3,121; 2,975; 2,879; 2,681; 2,404; 1,065.
- Questions with yes share in [70%, 75%): 198 in all, 177 before 27 Oct 2022, 21 from that date.
- Median yes share: 86.9% all, 86.1% before, 89.7% after.
- `τ = 6%`, `T = 75%`: blocking group 1.5%. `T = 70%`: 1.8%.

**Behaviour.** Dragging `T` recolours the histogram and moves both lines immediately. When the selected ballot flips between pass and fail, flash its label once (no flash under `prefers-reduced-motion`). Clicking a histogram bar lists the count in that bin in a tooltip and a live region.

**Accessibility.** All controls keyboard operable. The histogram has a text summary ("2,681 of 3,304 questions pass at 75%") in an `aria-live` region. Pass and fail are distinguished by pattern or outline as well as colour.

# PR101 · Peer review brief: team process and contribution

**Weight:** 10% of the course grade.
**Team process labs:** [lab 01](../labs/lab01.md) (week 1), [lab 05](../labs/lab05.md) (week 5) and [lab 11](../labs/lab11.md) (week 11). **Peer assessment round 1:** end of week 9, covering weeks 1 to 9 and the jam. **Round 2:** within three days of your final release in week 15, covering weeks 10 to 15.
**Work mode:** the labs are team work with a shared mark. The peer ratings you receive and the reviews you write are individual.
**Lectures:** [week 1, roles on a game team](../lectures/w01-roles-on-a-game-team.md), [week 5, standups and retrospectives](../lectures/w05-agile-and-scrum-adapted-for-games.md) and [week 11, communication and conflict](../lectures/w11-communication-and-conflict-in-teams.md).

## What this component is for

The other 90% of the course grade is shared. Week 11 showed what a shared grade does. Each hour you put in returns only `m / n` of its value to you, so for a team of four with `m = 2` it takes individual credit of at least `k* = 1 − 2/4 = 0.5` per hour before contributing pays on its own. Peer review is one of the individual-credit mechanisms your working agreement relies on. It only works if it rewards what the record shows, not who is popular or loud. So this component marks three things: the team documents that make contribution visible, what your teammates say about your contribution, and how well you review theirs.

## Part A: team process labs (50 points)

Each lab is marked on its own rubric in its week. Its percentage counts here.

| Lab | What it sets up | Points |
|---|---|---|
| [Lab 01, team charter and RACI](../labs/lab01.md) | Roles with one A per row, bus factors, tie-break rule, lateness rule | 15 |
| [Lab 05, one sprint, measured](../labs/lab05.md) | Standups, a review with outside players, a retrospective with one owned change | 15 |
| [Lab 11, working agreement and contribution record](../labs/lab11.md) | Channels, decision log, contribution record with evidence links, escalation ladder, `k*` argument | 20 |

## Part B: peer assessment (40 points)

### The form

In each round, you rate every teammate, not yourself, on five criteria, 0 to 4 each. Every rating needs at least one piece of evidence: a contribution record entry, a card id, a commit, a pull request review, a tracker id or a decision log line. A rating with no evidence is removed before scoring.

| Criterion | What a 4 looks like | What a 0 looks like |
|---|---|---|
| Delivery | Closed the cards they committed to, meeting the definition of done, or re-planned early and visibly | Committed cards stayed open with no warning |
| Reliability | Did what they said by when they said it, under the charter's "what counts as late" rule | Repeatedly late without warning |
| Communication | Replied within the agreement's response times; logged decisions; raised blockers at standups | Unreachable for days; decisions made in private |
| Shared work | Reviewed pull requests, triaged bugs, fixed builds they didn't break, ran playtests | Only worked on their own visible cards |
| Team conduct | Kept task conflict about the task; raised problems early through the ladder; wrote blameless | Personal attacks, or problems raised only in the peer review |

Each rating also takes two sentences for the teammate: one thing to keep doing, and one thing to change. Write them as observation, impact and request (week 11 section 3).

You also rate yourself on the same form. Self-ratings are not scored. The instructor uses them to find gaps between how members see their own work and how others see it.

### Scoring

Your score in a round is the mean, over the teammates who rated you, of their five ratings added together, out of 20.

- Round 1 is worth 10 points: `points = mean total / 20 × 10`.
- Round 2 is worth 30 points: `points = mean total / 20 × 30`.

Example. In round 2, Ana's three teammates give her totals of 17, 18 and 16. The mean is 17, so she scores `17 / 20 × 30 = 25.5` points.

Round 1 is weighted less on purpose. It gives every member feedback while there is still time to act on it, before the final project.

### Moderation

The instructor reviews every round before scores are released.

- **Evidence.** Ratings are compared with the contribution record, the board, the Git history and the tracker. Ratings without evidence are removed.
- **Outliers.** If one rater's score for a criterion differs from the other raters' mean by more than 1.5, the instructor reads that rater's evidence. It stands if the evidence supports it.
- **Blanket ratings.** If a team gives everyone 4 on everything while the record shows large differences in contribution, those ratings are set aside, and the instructor scores that round from the record.
- **Meetings.** Any student may ask for a meeting about their result. The instructor may also call one. A meeting never reveals who gave which rating.

### Confidentiality

Ratings and comments are confidential. After moderation, each student sees their own mean for each criterion and the comments written about them, without names. Nobody sees a teammate's ratings. Peer review is about contribution. The post-mortem is about the project, and it is no place to settle contribution disputes (week 14 section 3).

## Part C: the reviews you write (10 points)

The instructor marks the reviews you wrote across both rounds. Good reviews cite evidence for every rating, say something specific enough to act on, and describe behaviour and its effect rather than character. Reviews that are all 4s with "great teammate!" score low here, and so do reviews that use the form to attack someone.

## Rubric

The peer review mark is the total below, out of 100, multiplied by 0.10.

| Criterion | Excellent | Good | Adequate | Weak or missing | Points |
|---|---|---|---|---|---|
| Lab 01, charter and RACI | Lab rubric percentage × 15 | | | | 15 |
| Lab 05, one sprint, measured | Lab rubric percentage × 15 | | | | 15 |
| Lab 11, working agreement and record | Lab rubric percentage × 20 | | | | 20 |
| Round 1 peer rating | Mean total received / 20 × 10, after moderation | | | | 10 |
| Round 2 peer rating | Mean total received / 20 × 30, after moderation | | | | 30 |
| Reviews you write | 9 to 10: every rating has specific evidence; keep and change sentences in observation-impact-request form; blameless; both rounds on time | 6 to 8: evidence for most ratings; comments general | 3 to 5: few citations; ratings look uniform | 0 to 2: late, missing or abusive | 10 |
| **Total** | | | | | **100** |

## Rules

- **Submit both rounds.** A student who doesn't submit a round's form by its deadline scores 0 in Part C for that round, and their own ratings of others are not used.
- **Honesty.** Agreeing with teammates to give each other top ratings is collusion and is handled under the university's misconduct policy.
- **Low contribution with a reason.** A teammate with an illness, a job or a family emergency has fewer hours (`H`), which is different from free riding. Rate what they did against what the team agreed with them, and tell the instructor privately if their circumstances affected the team. The week 11 ladder, not the rating form, is the place to deal with it while the project is running.
- **Safety.** Harassment or safety concerns go straight to the instructor and the university's reporting route, never only into a peer review form.

## Advice

- **Keep the contribution record every day.** It takes five minutes. It is your evidence when you rate others and the evidence others will use when they rate you.
- **Read your round 1 comments as a retrospective.** Pick one change, give it a check, and see whether round 2 notices.
- **Rate what happened, not how you feel today.** Open the record before you open the form.

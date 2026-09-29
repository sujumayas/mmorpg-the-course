# PR101 · Week 11 — Communication and conflict in teams

**Why this matters:** The most common complaint in student game teams is some version of "I did all the work." It is rarely about one bad person. A shared grade creates a situation where every hour you put in helps you only a little and helps everyone else a lot. Once you can compute how little, you can design your team's rules so that contributing pays. Then you can argue about the game instead of about each other.

**You will be able to:**
- Compute a team member's return on one hour of project work from team size, the value an hour creates and any individual credit, and decide whether a team faces a free-rider problem.
- Derive the minimum individual credit that makes contributing worth it, and explain why it grows with team size.
- Distinguish task conflict from relationship conflict, name the five Thomas-Kilmann conflict modes, and choose one for a given team situation with a reason.
- Write a working agreement for your final project covering communication channels, decision records, contribution tracking and a conflict escalation ladder.

**Before class:** Clinton Keith, *Agile Game Development: Build, Play, Repeat* (2nd ed., 2020), chapter 5, "Great Teams", and chapter 20, "Self-Organization and Leadership". Latané, Williams and Harkins (1979), "Many hands make light the work", *Journal of Personality and Social Psychology* 37(6), 822-832, the introduction and the discussion (about 6 pages). Reread your team charter from lab 01.

**Prerequisites from earlier courses:** From this course, [week 1, roles on a game team](w01-roles-on-a-game-team.md) (communication channels and team charters; this week does not repeat the channel model) and [week 9, jam post-mortem](w09-jam-post-mortem.md). Looking ahead to year 3, [MMO303 week 10, payoff matrices and Nash equilibria](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w10-game-theory-payoff-matrices-and-nash-equilibria.md) develops best responses and equilibria in full, and [MMO305 week 5, raiding as organization](../../MMO305-social-systems-and-online-behaviour/lectures/w05-raiding-as-organization-dkp.md) shows a player-built answer to this week's problem.

**Interactive:** [`examples/w11-free-rider.html`](../examples/w11-free-rider.html). Keep it open during section 2.

---

## 1. Communication is a production tool

Week 1 counted communication channels and showed that each one costs hours. This week asks what goes through those channels and what happens when it goes wrong.

Most team communication problems in game projects fall into three kinds.

**Lost decisions.** Two people agree on Tuesday that enemies should respawn after 30 seconds. On Friday the designer remembers 20. Nobody wrote it down, so the argument is about memory, not design. The fix is a **decision log**: one shared page, one line per decision, with the date, the decision, who decided and why. It costs a minute per decision. It ends every "but we agreed" argument, because the log says what was agreed.

**Wrong channel.** A question that blocks someone's work ("which sprite sheet format does the importer expect?") sits in a chat channel with 200 unread messages. A long design debate happens in a thread that half the team muted. Match the channel to the message:

| Message | Channel | Expected reply |
|---|---|---|
| Blocking question | Direct message or a call, tagged "blocking" | Within a few hours in working time |
| Status update | The task board, not chat | None |
| Design decision | Short call, then one line in the decision log | Everyone reads the log line |
| Heads-up ("I'm renaming the player scene") | Team channel | An emoji acknowledging it |
| Feedback on someone's work | In person or a call first, written summary after | Discussion |

Write your team's version of this table into your working agreement. The response-time column matters most. "Reply within four working hours" is a promise people can keep and check. "Stay responsive" is not.

**Tone without faces.** Text strips out voice and expression, and a tired reader fills the gap with the worst interpretation. "Did you test this?" can be a question or an accusation. Two habits help. Say what you observed and what you need, not what you think of the person: "The build crashes on level 2 since your last commit. Can you look before tonight's merge?" And move anything heated to a call, then write a neutral summary afterwards.

### Synchronous and asynchronous

**Synchronous** communication happens at the same time for everyone (meetings, calls, the daily standup from week 5). **Asynchronous** communication waits for the reader (messages, the task board, the decision log, commit messages). Student teams have very little overlapping time, because four people have four different timetables. So default to asynchronous, and spend synchronous time only on things that need back-and-forth, such as decisions with trade-offs, conflict and planning. The Agile Manifesto's principles call face-to-face conversation the most efficient way to convey information within a team. That is true for rich, uncertain topics. It is a poor way to record anything, which is why every call ends with one written line.

## 2. Worked example: why "I did all the work" is predictable

### The hook

In 1979, Bibb Latané, Kipling Williams and Stephen Harkins asked people to clap and shout as loudly as they could, alone and in groups. People made less noise per person in groups, and the loss was larger than poor coordination alone could explain. People put in less effort when their contribution disappears into a group total. The authors called this **social loafing**.

Every team game you have played has the same shape. In an MMO raid, the boss dies for all 40 people at once, whether you pulled your weight or stood in the fire. Raiding guilds, first in EverQuest in 1999 and later in World of Warcraft, built systems like DKP ("dragon kill points"), covered in MMO305 week 5, to tie each person's loot to their own attendance. Player-run guilds invented rules to solve a problem your team has too. The question is why the problem arises so reliably, and how big a fix it needs.

### The model

This is the linear **public goods game** from experimental economics, set in a student team.

Each of the `n` members has `H` hours this week. Each person chooses `x_i` hours to put into the team project and spends the rest, `H − x_i`, on other things (another course, a job, sleep).

- Every hour on the project creates `m` units of value for the team. The team's result is shared equally, because everyone gets the same team grade. So each member receives `m / n` units per project hour, whoever worked it.
- Every hour spent elsewhere is worth 1 unit, to you alone.
- Some team rules give a person **individual credit** for their own project hours: peer review marks, named ownership of a feature, a demo slot. Call that `k` units per project hour, paid only to the person who worked it.

A member's payoff is:

```
u_i = (m / n) × X + k × x_i + (H − x_i)
X = x_1 + x_2 + ... + x_n    (total project hours)
```

Now ask what one extra project hour does for the person who works it. They gain `m / n` from the shared result and `k` in individual credit. They lose the 1 unit that hour was worth elsewhere. So the **individual return per project hour** is:

```
return = m / n + k − 1
```

Economists call `m / n` the marginal per capita return. For the team as a whole, one project hour produces `m` units of value (plus `k` of credit) and costs 1. A **free-rider problem** exists when the hour is good for the team (`m > 1`) and bad for the person who works it (`m / n + k < 1`).

Set the individual return to zero and you get the smallest individual credit that makes contributing pay:

```
k* = 1 − m / n
```

That formula is the whole lesson. The credit you need grows with team size. In a pair, a shared grade already gives each person half of every hour's value. In a team of six, each person gets a sixth.

### Numbers you can check

Take your final-project team: `n = 4` people, `H = 10` hours each this week, and project hours worth `m = 2` units (an hour on the game moves the shared grade twice as much as an hour elsewhere moves your own results). Start with no individual credit, `k = 0`.

**Everyone contributes 10 hours.** `X = 40`. Each person gets `(2/4) × 40 = 20` units.

**Nobody contributes.** `X = 0`. Each person keeps their 10 hours for other things, 10 units each. Everyone is worse off than when all contribute.

**Three contribute, one does nothing.** `X = 30`. The shared result gives everyone `(2/4) × 30 = 15`. The contributors have nothing else, so they get 15. The free rider adds their 10 other hours and gets 25.

Now add individual credit `k = 0.6` (a peer review that tracks each person's logged hours, for example). Contributors earn 0.6 per hour of their own, so 6 units for 10 hours.

| Scenario | Payoff with `k = 0` | Payoff with `k = 0.6` |
|---|---|---|
| All four contribute 10 h | 20 each | 26 each |
| One free rides: the free rider | 25 | 25 |
| One free rides: each contributor | 15 | 21 |
| Nobody contributes | 10 each | 10 each |

Read the `k = 0` column as the free rider would. If the other three contribute, doing nothing earns 25 instead of 20. Free riding pays, even though everyone together prefers the all-contribute row. In the language of MMO303 week 10, not contributing is each player's best response whatever the others do, so "nobody contributes" is the equilibrium of the one-shot game.

Now read the `k = 0.6` column. Free riding earns 25, contributing earns 26. It no longer pays. Check with the formula: `m / n + k − 1 = 0.5 + 0.6 − 1 = 0.1` per hour, times 10 hours, is the 1-unit difference. The threshold is `k* = 1 − 2/4 = 0.5`.

How the threshold grows with team size, still at `m = 2`:

| Team size `n` | Your share of each hour, `m / n` | Credit needed, `k* = 1 − m / n` |
|---|---|---|
| 2 | 1.00 | 0 |
| 3 | 0.67 | 0.33 |
| 4 | 0.50 | 0.50 |
| 6 | 0.33 | 0.67 |
| 8 | 0.25 | 0.75 |

A pair needs no individual credit at all. A team of eight needs credit worth three quarters of an hour's outside value before contributing pays. This is why jam pairs rarely argue about effort and eight-person projects almost always do.

The table comes from this code. Run it with `.venv/bin/python`:

```python
def payoff(hours, i, m=2, k=0.0, H=10):
    n, X = len(hours), sum(hours)
    return m / n * X + k * hours[i] + (H - hours[i])

for k in (0.0, 0.6):
    team = [10, 10, 10, 0]
    print(f"k={k}: all={payoff([10] * 4, 0, k=k):g}",
          f"rider={payoff(team, 3, k=k):g}",
          f"contributor={payoff(team, 0, k=k):g}")

for n in (2, 3, 4, 6, 8):
    print(n, round(2 / n, 2), round(1 - 2 / n, 2))
```

It prints:

```
k=0.0: all=20 rider=25 contributor=15
k=0.6: all=26 rider=25 contributor=21
2 1.0 0.0
3 0.67 0.33
4 0.5 0.5
6 0.33 0.67
8 0.25 0.75
```

Open the interactive. The left chart shows each member's payoff as a bar, with one hours slider per member. The right chart plots your return per project hour, `m / n + k`, against team size, with a line at 1. Where the curve sits below the line, free riding pays. Drag `n` from 2 to 8 and watch the curve fall under the line. Then raise `k` and watch the whole curve lift until it clears the line at your team size.

### Where the conflict comes from

Look at the contributors in the `k = 0` column. They earn 15 while the free rider earns 25, and they can see it. Ernst Fehr and Simon Gächter (2000) ran public goods games in the lab and gave players a chance to punish others at a cost to themselves. Many cooperators paid to punish free riders, even when they could not expect anything in return. The authors link this to people's strong aversion to being the "sucker". Contributions were generally higher when punishment was possible than when it was not.

In a student team, "punishment" is the angry message at 2 a.m., the silent treatment, or the brutal peer review. Those reactions are predictable, and they cost the team more than the free-riding did. A team that builds individual credit into its rules in week 1 gets the benefit of punishment (people contribute) without the fight.

### Cross-game recognition

**MMO raids and DKP.** A raid kill is a public good for the raid. Loot is the private reward. DKP systems pay points for attendance and let members spend them on items, so each person's reward depends on their own contribution. In this model DKP is `k`. MMO305 week 5 shows the side effects, such as inflation and newcomers who wait for items, which is a reminder that every `k` mechanism has its own design problems.

**Valve's peer-ranked pay.** Valve's *Handbook for New Employees* (first edition, March 2012) describes a flat organization in which employees rank one another once a year, and the stack ranking is used mainly to adjust each person's pay. That is a large `k` made from peer judgment. In January 2023 the documentary channel People Make Games published a report arguing that the flat structure and the stack-ranking pay system contributed to a slow release record and a lack of diversity. Read it as the warning that comes with any peer-based `k`. When credit depends on what colleagues see and remember, it can reward visibility and social standing as much as work. Your team's `k` should rest on records (commits, closed tasks, the decision log), with peer judgment on top.

**Lab public goods games.** Across many experiments, reviewed by John Ledyard (1995), people start by contributing a substantial share of their endowment but contribute less as rounds repeat, once they see others giving less. Your team goes through the same slide over a semester. Enthusiasm in week 2 is not a contribution plan for week 12.

### Eyes-open judgment

- **`k` is not free.** Every individual-credit rule costs time to record and can be gamed. Counting commits rewards many tiny commits. Counting hours rewards slow work. Pick measures that are hard to inflate, such as closed tasks that met the definition of done from week 7.
- **Too much `k` breaks teamwork.** If `k` is much larger than `m / n`, people optimize their own visible tasks and nobody takes the unglamorous shared work: merging, build fixes, the bug triage from week 10. Make those shared tasks count too.
- **Not all low contribution is free riding.** A teammate with a job, an illness or a family emergency has a smaller `H`, not a different choice. The model helps you talk about hours without talking about character. "You logged 2 hours this week and we planned 10, what happened?" is a question. "You're lazy" starts a relationship conflict.
- **The one-shot game is the worst case.** Your team plays the game every week for a semester, and people remember. Repetition and reputation let cooperation hold even without formal `k`, as long as contributions are visible. Visibility is therefore the cheapest `k` there is. A task board where every card has a name on it is already individual credit.

## 3. Conflict: which kind, and what to do

Conflict is not a sign that a team is failing. Bruce Tuckman's 1965 model of group development names a **storming** stage, after forming and before norming and performing, in which members clash over roles, power and direction. Most teams pass through it. Your jam in week 8 probably felt like one.

### Task conflict and relationship conflict

Researchers separate two kinds.

**Task conflict** is disagreement about the work. Should the jump be floaty or tight? Should we cut the second level or the boss? It is about ideas.

**Relationship conflict** is friction between people. Irritation, distrust, "she always ignores my ideas". It is about the person.

For years the textbook advice held that task conflict helps teams by testing ideas while relationship conflict hurts them. Karen Jehn's 1995 study was part of that picture. Then Carsten De Dreu and Laurie Weingart (2003) pooled the research in a meta-analysis. Relationship conflict was strongly negatively related to team performance and satisfaction, as expected. But task conflict was *also* negatively related to both, not positively. It hurt less when the two kinds of conflict were not tangled together, and it hurt more on complex tasks like projects than on simple production work.

The lesson for a game team is not "avoid disagreement about the game". You must disagree about the game to make good decisions. The lesson is to keep task conflict from turning into relationship conflict, and to settle it quickly. Every task conflict should end in a decision, logged, and not stay open for weeks.

### Five ways to handle a conflict

Kenneth Thomas and Ralph Kilmann (1974) describe conflict behaviour on two dimensions: **assertiveness** (how hard you push for your own concerns) and **cooperativeness** (how hard you try to satisfy the other person's). The combinations give five modes:

| Mode | Assertive | Cooperative | Good for | Bad for |
|---|---|---|---|---|
| Competing | High | Low | Emergencies, a clear owner deciding within their area | Anything the others must commit to |
| Collaborating | High | High | Core design choices that everyone must believe in | Small calls; it takes the most time |
| Compromising | Medium | Medium | Splitting time or scope when both sides have a point | Design choices where half of each idea is worse than either |
| Avoiding | Low | Low | Trivial issues, or letting a heated moment cool for a day | Anything that will come back bigger |
| Accommodating | Low | High | Issues that matter more to the other person than to you | Repeatedly, by the same person, which builds resentment |

No mode is right every time. The skill is choosing on purpose. The owner of the audio (from your week 1 RACI) can reasonably compete on the choice of footstep sounds. The whole team must collaborate on the core loop. And "we'll compromise and make the jump medium-floaty" is often the worst option in game design, because a blend of two feels can be worse than either. In that case, prototype both and let a playtest decide, as in GD101 week 7.

### An escalation ladder

Decide in advance what happens when a conflict does not resolve. A ladder for a student team:

1. **Direct.** The two people talk, in person or on a call, within two days of noticing the problem. Use observation, impact and request: "In the last two sprints, three of your tasks moved to the next sprint (observation). Level 3 is blocked on them (impact). Can we split them smaller or move one to me (request)?"
2. **Team.** If that fails, raise it at the next retrospective (week 5) as a team problem, with the numbers from the task board. The team decides a change and writes it in the decision log.
3. **Facilitator.** If it continues, the team asks the teaching assistant to sit in on one meeting.
4. **Instructor.** Last, the instructor, who can change roles, adjust peer review weight, or in rare cases split the team.

Two rules make the ladder work. Nobody skips a rung, except for harassment or safety issues, which go straight to the instructor and the university's reporting route. And the numbers come first, feelings second. Your task board, commit log and decision log are the evidence. That is why section 2 matters for conflict. A team that already tracks individual contributions has the facts ready before tempers rise.

## 4. Your working agreement

Your week 1 charter answered who owns what. After a jam and a post-mortem you know where it was thin. This week you turn it into a **working agreement** for the final project, with four additions:

- **Channels.** Your version of the channel table in section 1, with response times.
- **Decision log.** Where it lives, who writes the line after each call.
- **Contribution record and `k`.** What counts as a contribution (closed tasks meeting the definition of done, reviewed merges, triaged bugs), where it is recorded, and how it feeds the course's peer review. Compute `k*` for your team and check your rule is at least that strong.
- **Conflict ladder.** The four rungs above, adapted, with names and deadlines.

Everyone signs it. It takes about an hour to write and will save you far more than that.

## In-class activity (25 min)

In your final-project team, with your jam task board and commit log open.

1. **Measure (8 min).** For the jam weekend, count each member's closed tasks and merged commits. Estimate each person's hours. Do not discuss yet. Just write the numbers.
2. **Model (7 min).** Using `n = 4` and a value of `m` your team agrees on, compute `k*`. List every mechanism in your current charter that works as individual credit. Is its combined strength above `k*`?
3. **Scenario (7 min).** The instructor hands each team one written conflict scenario (for example, "the artist redraws the player sprite for the third time, and the programmer says the animation system cannot take another change"). Classify it as task or relationship conflict, pick a Thomas-Kilmann mode, and write the first sentence the person should say, in observation-impact-request form.
4. **Report (3 min).** One person reads your scenario answer to the neighbouring team, who must guess which mode you chose.

Expected output: the contribution table from step 1, your `k*` with the list from step 2, and a card with the scenario answer. The table starts lab 11.

## Common misconceptions

- **"Free riders are bad people."** The model shows free riding is the individually rational choice whenever `m / n + k < 1`. Change the rules and most people change their behaviour. Save judgments of character for the rare case where the rules are fair and someone still takes advantage.
- **"Task conflict is healthy, only personal conflict hurts."** The meta-analysis by De Dreu and Weingart found task conflict also hurts performance on average, especially on complex work. Disagree, then decide quickly and record it.
- **"Compromise is always fair."** Splitting the difference between two design ideas often produces something worse than either. Prototype and test instead.
- **"Bigger teams share the load, so there's less stress."** Each member's share of their own hour's value falls as `1/n`. Bigger teams need stronger individual credit, and week 1 showed they also need more coordination.

## Check yourself

1. A team of five works on a project where an hour creates `m = 3` units of shared value. There is no individual credit. Does a free-rider problem exist? What is `k*`?
2. In the four-person example (`m = 2`, `H = 10`), set `k = 0.3`. Compute the payoff of a free rider and of each contributor when the other three contribute 10 hours. Does free riding pay?
3. A team adds a rule that each person's peer review score is their share of closed tasks. A member responds by splitting every task into five tiny cards. Which eyes-open point does this illustrate, and how would you change the measure?
4. Two teammates argue for a week about whether combat should use stamina. It has started to include comments like "you never listen". Classify the conflict, and describe the two steps you would take, naming a Thomas-Kilmann mode.

<details>
<summary>Answers</summary>

1. `m / n = 3/5 = 0.6 < 1` and `m = 3 > 1`, so yes. `k* = 1 − 0.6 = 0.4`.
2. Shared result: `X = 30`, so `(2/4) × 30 = 15` each. Free rider: `15 + 0.3 × 0 + 10 = 25`. Contributor: `15 + 0.3 × 10 + 0 = 18`. If the free rider contributed instead, they would get `(2/4) × 40 + 3 + 0 = 23`. Since 25 > 23, free riding still pays, because `k = 0.3 < k* = 0.5`.
3. `k` can be gamed; a measure that is easy to inflate rewards inflating it. Count closed tasks weighted by estimate, or tasks that met the definition of done and were reviewed, so splitting gains nothing.
4. It began as task conflict and is turning into relationship conflict. First, stop the thread and move to a call, so tone does not make it worse. Second, collaborate or, better for a design question with a testable answer, agree to prototype both versions and decide by a playtest by a fixed date, then log the decision. Avoiding would let it grow. Competing would leave one person without commitment to the result.

</details>

## Lab / assignment hook

[Lab 11, working agreement and contribution record](../labs/lab11.md). Your team turns the week 1 charter into a signed working agreement with a channel table, a decision log, a contribution record and an escalation ladder, computes `k*` for your team, and runs a scripted conflict role-play. Deliverable: the agreement, the first two weeks of the contribution record, and a 300-word role-play debrief.

## Sources

- Latané, B., Williams, K. & Harkins, S. (1979). "Many hands make light the work: The causes and consequences of social loafing". *Journal of Personality and Social Psychology* 37(6), 822-832. Clapping and shouting experiments; reduced individual effort in groups beyond coordination losses.
- Fehr, E. & Gächter, S. (2000). "Cooperation and Punishment in Public Goods Experiments". *American Economic Review* 90(4), 980-994. Cooperators willing to pay to punish free riders; aversion to being the "sucker"; higher contributions with punishment available.
- Ledyard, J. (1995). "Public Goods: A Survey of Experimental Research". In Kagel & Roth (eds.), *The Handbook of Experimental Economics*, 111-194. Princeton University Press. Contribution levels and their decline over repeated rounds.
- Wikipedia, "Public goods game" (accessed September 2026). The payoff form and the condition under which contributing is socially good but individually costly.
- De Dreu, C. K. W. & Weingart, L. R. (2003). "Task versus relationship conflict, team performance, and team member satisfaction: a meta-analysis". *Journal of Applied Psychology* 88(4), 741-749. Both conflict types negatively related to performance; stronger on complex tasks.
- Jehn, K. A. (1995). "A Multimethod Examination of the Benefits and Detriments of Intragroup Conflict". *Administrative Science Quarterly* 40(2).
- Tuckman, B. W. (1965). "Developmental sequence in small groups". *Psychological Bulletin* 63(6). Forming, storming, norming, performing; adjourning added by Tuckman and Jensen (1977). Summarized in Wikipedia, "Tuckman's stages of group development".
- Thomas, K. W. & Kilmann, R. H. (1974). *Thomas-Kilmann Conflict Mode Instrument*. The five modes on the assertiveness and cooperativeness dimensions. Summarized in Wikipedia, "Thomas-Kilmann Conflict Mode Instrument".
- Wikipedia, "Valve Corporation" (accessed September 2026). Flat organization with open allocation; the January 2023 People Make Games report on the flat structure and stack-ranking compensation.
- Valve Corporation (2012). *Handbook for New Employees*, first edition, March 2012, Part 3, "Your Peers and Your Performance". Annual peer stack ranking used primarily to adjust compensation.
- Warcraft Wiki, "Dragon kill points", as cited in MMO305 week 5. DKP created for the EverQuest guild Afterlife in 1999 and later used in World of Warcraft raids.
- Beck, K. et al. (2001). "Principles behind the Agile Manifesto", agilemanifesto.org. Face-to-face conversation as the most efficient way to convey information within a team.
- Keith, C. (2020). *Agile Game Development: Build, Play, Repeat* (2nd ed.). Addison-Wesley. Chapters 5 and 20.
- The values of `m`, `H` and `k` in section 2 are teaching values chosen for round numbers, not measurements.

## Interactive spec: examples/w11-free-rider.html

**The one insight.** Your return on one hour of team work is `m / n + k`. As the team grows it falls under 1, and free riding starts to pay. Individual credit `k` lifts the curve, and the lift needed grows with team size.

**Layout.** Two linked views side by side on desktop, stacked on mobile. Left, "Who comes out ahead": one bar per member. Right, "Your return per project hour": a curve over team size. Controls below on mobile, right column on desktop. A one-line verdict above both views.

**Model (exact).**
- `X = Σ x_i`.
- `u_i = (m / n) × X + k × x_i + (H − x_i)`.
- Individual return per hour `R(n) = m / n + k`; free riding pays when `R < 1`. Show `k* = max(0, 1 − m / n)`.
- "Best response" for member i: contribute `H` if `R > 1`, contribute 0 if `R < 1`, indifferent if `R = 1` (use a tolerance of 1e-9).

**Left chart.** One vertical bar per member (n bars). Each bar is split into three stacked segments: shared share `(m/n) × X` (primary color), individual credit `k × x_i` (accent), outside value `H − x_i` (neutral). Numeric total above each bar. A dashed horizontal line at the "all contribute" payoff `m × H + k × H` labelled "if everyone contributes". Under each bar, a vertical slider for that member's hours `x_i`, 0 to `H`, step 1, default `H`.

**Right chart.** x = team size 2 to 12. y = return per hour, 0 to 2. Curve `R(n) = m / n + k` drawn as connected points. Horizontal line at 1, labelled "break-even". Shade the region under 1 and label it "free riding pays". Marker on the current `n`. A second, faint curve for `k = 0` so the lift from `k` stays visible.

**Controls.**
- Team size `n`: slider 2 to 8, step 1, default 4. Changing `n` adds or removes member sliders; new members default to `H`.
- Value per project hour `m`: slider 1.0 to 4.0, step 0.1, default 2.0.
- Individual credit `k`: slider 0 to 1.0, step 0.05, default 0.
- Hours available `H`: slider 4 to 20, step 1, default 10.
- Preset buttons: "All contribute", "One free rider" (last member 0, others `H`), "Nobody contributes".
- Reset.

**Verdict line.** Text such as: "With 4 members, each hour you work returns 0.50 to you. Free riding pays. Individual credit of at least 0.50 would fix it." When `R ≥ 1`: "Contributing pays for everyone. Return per hour: 1.10."

**Test values (must match exactly).**
- `n = 4, m = 2, H = 10, k = 0`, all contribute: every bar 20. One free rider: rider 25, contributors 15. Nobody: 10 each. `k* = 0.50`.
- Same with `k = 0.6`: all contribute 26 each; one free rider: rider 25, contributors 21. Return per hour 1.10.
- `n = 5, m = 3, k = 0`: return 0.60, `k* = 0.40`.
- `n = 4, m = 2, k = 0.3`, one free rider: rider 25, contributors 18.
- `k*` at `m = 2` for `n = 2, 3, 4, 6, 8`: `0, 0.33, 0.50, 0.67, 0.75`.

**Accessibility and behaviour.** Every slider keyboard operable with a visible numeric value; member sliders labelled "Member 1 hours" and so on. The verdict line is an ARIA live region. Respect `prefers-reduced-motion` and `prefers-color-scheme`. Use `templates/interactive-tokens.css` inline. Members are drawn as plain numbered bars; no game characters or logos.

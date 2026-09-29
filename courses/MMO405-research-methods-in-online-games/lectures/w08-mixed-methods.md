# MMO405 · Week 08 — Mixed Methods

**Why this matters:** Telemetry tells you what players did, and interviews and field notes tell you what it meant. Most good questions about online worlds need both. Putting a chart and three quotes in the same report does not make a mixed-methods study. The value comes from the point where one kind of evidence changes how you read the other, and you have to design for that point before you collect anything.

**You will be able to:**
- Name the three core mixed-methods designs and the four ways of integrating data (connecting, building, merging, embedding), and pick one for a research question.
- Decompose a group difference in self-reports into the true difference plus a difference in reporting bias, using linked survey and log records.
- Select qualitative cases from quantitative results in a way you can defend in a methods section.
- Build a joint display and classify each meta-inference as confirmation, expansion or discordance.

**Before class:** Fetters, Curry and Creswell, "Achieving Integration in Mixed Methods Designs: Principles and Practices" (2013), the whole article (open access). Williams, Consalvo, Caplan and Yee, "Looking for Gender" (2009), the method section and the results on self-reported hours (pp. 707-713). Skim Williams, Ducheneaut, Xiong, Zhang, Yee and Nickell, "From Tree House to Barracks" (2006), pp. 342-344, the three-step method.

**Prerequisites from earlier courses:** [MMO308 week 10, player feedback loops](../../MMO308-live-operations-analytics-and-experimentation/lectures/w10-player-feedback-loops-forums-surveys-polls.md) (say and do, and who gets asked). [UX201 week 12, surveys and interviews](../../UX201-game-ux-and-player-psychology/lectures/w12-surveys-and-interviews.md) (response bias, thematic analysis, how many interviews). [MA102 week 12, descriptive statistics for playtests](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md) (means and spread). [MMO305 week 2, playing alone together](../../MMO305-social-systems-and-online-behaviour/lectures/w02-playing-alone-together.md) (the census study used below). [MMO405 week 2, quantitative methods overview](w02-quantitative-methods-overview.md) (the EverQuest II logged hours by gender). [MMO405 week 3, telemetry as research data](w03-telemetry-as-research-data.md) (self-report as logged time plus bias plus noise, and differential error). [MMO405 week 6, interviews](w06-qualitative-methods-interviews.md) (coding and codebooks). [MMO405 week 7, ethnography and participant observation](w07-ethnography-and-participant-observation.md).

**Interactive:** [examples/w08-say-and-log.html](../examples/w08-say-and-log.html). Keep it open during section 2.

---

## 1. What makes a study "mixed"

A **mixed-methods study** collects both quantitative data (numbers you count or measure) and qualitative data (text, observation, talk you interpret), and it **integrates** them. Integration means that one strand shapes how the other is collected, analysed or read. Fetters, Curry and Creswell (2013) put integration at the centre of the definition, and it is the part most student projects leave out. A report with a retention curve in chapter 3 and interview quotes in chapter 4, never brought together, is two studies stapled together.

Why mix at all? Greene, Caracelli and Graham (1989) reviewed mixed-method evaluations and found five purposes. They still cover almost every reason you will give.

- **Triangulation.** Two methods measure the same thing, and agreement increases confidence. Logs and field notes both say the raid spent most of the night waiting.
- **Complementarity.** Each method covers a different facet. Logs show how often players leave guilds, and interviews show why.
- **Development.** One method's results shape the next. Field notes from a guild give you the categories for a survey.
- **Initiation.** You look for contradictions on purpose, because a contradiction is a new question. Players say they want harder raids and then stop queueing for them.
- **Expansion.** You widen a study's range by using different methods for different parts of it.

State your purpose in the proposal. It decides the design. Triangulation needs both strands to measure the same construct. Development needs one strand to finish before the other starts. Initiation needs linked data, so that you can see who says one thing and does another.

## 2. Worked example: when the survey and the server disagree

### The hook

In the mid-2000s Sony Online Entertainment let a research team led by Dmitri Williams survey EverQuest II players and match each answer to the player's own account in the game's databases. Players on four servers (one each of the PvP, PvE, role-play and Exchange types) were invited when they logged in. About 7,000 answered in just over two days, drawn in by a rare in-game staff made for the study. For the first time, researchers could compare what players said about their play with what the servers recorded.

You have met this dataset twice already. Week 2 used its logged hours by gender to separate a significant difference from a meaningful one. Week 3 used linked self-reports to show that recall is noisy, that noise hides correlations, and that error which depends on another variable is the dangerous kind. This week asks the next question. When two strands of evidence disagree, what does the disagreement do to a comparison, and how do you design the study that explains it?

One of the survey questions asked how many hours a week they played. The servers had logged every second each account was online. Men reported 24.10 hours a week and the servers logged 25.03. Women reported 26.03 hours a week and the servers logged 29.32.

Both groups under-reported, and women under-reported about three and a half times as much. Now look at the comparison a survey-only study would have made. The survey says women play about 1.9 hours a week more than men. The servers say the difference is 4.3 hours. **The survey shows less than half of the real gap.** Before this study, researchers had routinely taken self-reported hours on faith. The authors said as much, and warned that earlier findings built on self-reported play time might need to be re-examined.

### The model

Link each player's survey answer to their log. For player `i`:

```
d_i = r_i − ℓ_i                       (discrepancy: reported minus logged hours)
b_g = mean of d_i over group g        (the group's reporting bias)

Δ_r = r̄_A − r̄_B                       (the gap a survey shows)
Δ_ℓ = ℓ̄_A − ℓ̄_B                       (the gap the logs show)

Δ_r = Δ_ℓ + (b_A − b_B)
```

- `r_i` is what player `i` reported, and `ℓ_i` is what the server logged.
- `r̄` and `ℓ̄` are group means. A and B are the two groups being compared.
- A negative `d_i` means under-reporting.

This is week 3's `S = X + b + e` summarised by group. Week 3 held `b` constant. Here `b` is allowed to differ between groups, which is differential error in its simplest form. The last line is an identity, not an assumption. It follows because the mean of a difference is the difference of the means. It says that **any group comparison made with self-reports equals the true comparison plus the difference in how the two groups report.** If the groups report equally badly, their biases cancel and the survey gap is right even though every answer is wrong. If they report differently, the survey gap is wrong by exactly `b_A − b_B`.

That second term is where the qualitative strand enters. Linked records tell you *that* two groups report differently and *by how much*. They cannot tell you *why*. Williams and colleagues offered an explanation drawn from gender role theory. On their reading, women who play a game seen as male-oriented may play down how much they play, even on an anonymous survey. They supported it with one further quantitative check, described below. The linked data could not observe the reasons directly. Interviews could.

### Numbers you can check

First, the published figures (EverQuest II, Williams et al. 2009):

| Group | Reported `r̄` | Logged `ℓ̄` | Bias `b` |
|---|---|---|---|
| Men | 24.10 | 25.03 | −0.93 |
| Women | 26.03 | 29.32 | −3.29 |
| Women − men | `Δ_r` = 1.93 | `Δ_ℓ` = 4.29 | `b_A − b_B` = −2.36 |

Check the identity. `4.29 + (−2.36) = 1.93`. The survey shows `1.93 / 4.29 = 45%` of the logged gap. (Week 2 quoted women's logged hours as 29.31, from the team's 2008 paper on the same data. The 2009 paper, which reports the self-reports, gives 29.32. The one-hundredth difference is rounding between the two papers and changes none of the conclusions.)

Now a small invented dataset that you can work through completely. Ten players from a fictional MMO's survey are linked to their logs. The study wants to follow up with interviews. This is the **connecting** form of integration, in which the quantitative results choose the qualitative sample.

| Player | Group | Reported | Logged | `d` |
|---|---|---|---|---|
| F1 | F | 30 | 33 | −3 |
| F2 | F | 20 | 27 | −7 |
| F3 | F | 12 | 13 | −1 |
| F4 | F | 40 | 42 | −2 |
| F5 | F | 25 | 32 | −7 |
| M1 | M | 22 | 24 | −2 |
| M2 | M | 35 | 34 | +1 |
| M3 | M | 15 | 18 | −3 |
| M4 | M | 28 | 29 | −1 |
| M5 | M | 10 | 10 | 0 |

The selection rule, written down before looking at any names, is the two largest under-reporters in each group plus the most accurate reporter in each group as a contrast case. Ties are broken by player id. The code below runs as shown with `.venv/bin/python`.

```python
# Linked records: survey answer and server log for the same account (hours per week).
PLAYERS = [  # (id, group, reported, logged)
    ("F1", "F", 30, 33), ("F2", "F", 20, 27), ("F3", "F", 12, 13),
    ("F4", "F", 40, 42), ("F5", "F", 25, 32),
    ("M1", "M", 22, 24), ("M2", "M", 35, 34), ("M3", "M", 15, 18),
    ("M4", "M", 28, 29), ("M5", "M", 10, 10),
]

def mean(xs):
    return sum(xs) / len(xs)

stats = {}
for g in ("F", "M"):
    rows = [p for p in PLAYERS if p[1] == g]
    stats[g] = (mean([r for _, _, r, _ in rows]), mean([l for _, _, _, l in rows]))
    print(f"{g}: reported {stats[g][0]:.1f}  logged {stats[g][1]:.1f}  bias {stats[g][0] - stats[g][1]:+.1f}")

gap_r = stats["F"][0] - stats["M"][0]
gap_l = stats["F"][1] - stats["M"][1]
print(f"survey gap {gap_r:.1f} = log gap {gap_l:.1f} + bias gap {gap_r - gap_l:+.1f}")
print(f"the survey shows {gap_r / gap_l:.0%} of the logged gap")

# Connect: pick interviewees from the discrepancy d = reported - logged.
for g in ("F", "M"):
    rows = sorted((p for p in PLAYERS if p[1] == g), key=lambda p: (p[2] - p[3], p[0]))
    under = [p[0] for p in rows[:2]]
    accurate = min(rows, key=lambda p: (abs(p[2] - p[3]), p[0]))[0]
    print(f"{g}: interview under-reporters {under} and accurate reporter {accurate}")
```

```
F: reported 25.4  logged 29.4  bias -4.0
M: reported 22.0  logged 23.0  bias -1.0
survey gap 3.4 = log gap 6.4 + bias gap -3.0
the survey shows 53% of the logged gap
F: interview under-reporters ['F2', 'F5'] and accurate reporter F3
M: interview under-reporters ['M3', 'M1'] and accurate reporter M5
```

Check group F by hand. Reported `(30 + 20 + 12 + 40 + 25)/5 = 25.4`. Logged `(33 + 27 + 13 + 42 + 32)/5 = 29.4`. Bias `−4.0`. The identity holds, since `6.4 + (−3.0) = 3.4`.

The contrast cases matter. If you interview only the under-reporters, every theme you find will look like an explanation of under-reporting. You cannot tell whether accurate reporters say the same things. F3 and M5 let you check.

### A visual you can move

Open the interactive. The left panel is a scatter of reported against logged hours for every player, with the line `reported = logged` drawn across it. Points below the line are under-reporters. Each group has its own colour and marker shape. The right panel shows two pairs of bars, the gap between groups in the survey and the gap in the logs, with the bias difference drawn as the piece that separates them. Drag group F's bias slider from 0 toward −6 hours. The logged bars do not move. The survey gap shrinks, reaches zero at a bias difference of −6.4, and then reverses. A survey-only study at that point would report that group M plays more. Toggle "select interviewees" to see the connecting rule highlight its cases.

### Cross-game recognition

In each study below, name the strands, the form of integration, and the fit between them.

**EverQuest II survey linked to server logs (Williams, Yee and Caplan 2008; Williams et al. 2009).** Strands: a survey and server logs, joined by account id. Integration: merging. Fit: discordance on hours played, which became a finding in its own right. The authors' follow-up check stayed quantitative. Women who identified as bisexual reported 29.28 hours against 29.83 logged, a difference that was not statistically significant, and the authors read this as support for the gender-role explanation. That is a quantitative test of a qualitative idea. The natural next step, interviews sampled on `d_i`, is an explanatory sequential design.

**World of Warcraft guild interviews (Tree House, Williams et al. 2006).** Strands: a census of three servers in January 2006, social network measures built from who grouped with whom, and 48 interviews in February and March 2006. Integration: connecting. The census built a sampling frame stratified by server type, faction, guild size and each player's network centrality, and interviewees were drawn at random from its cells. Fit: expansion and some discordance. The team had assumed that high-centrality players were the social hubs of their guilds. The interviews showed that this assumption did not entirely hold. Week 9 picks up exactly this finding.

**World of Warcraft census (Ducheneaut et al. 2006, 2007).** Strands: the authors' own play and guild membership since the game's launch, then an automated census. Integration: building, because the fieldwork told them which variables to record and how to read them, for example why cities had to be excluded from co-location measures. Fit: expansion. The census showed that grouping was a minority activity. The field experience explained that players valued playing among others without playing with them. MMO305 week 2 has the numbers.

**Live-operations feedback (MMO308 week 10).** Strands: survey or forum opinion, and telemetry of the same players. Integration: merging on player id. Fit: whichever it turns out to be. The live-ops rule that "the disagreement is the finding" is the initiation purpose from section 1, applied every week.

Four studies, one structure. Two strands, a named point of contact, and a judgment about fit. When you read any study that claims to combine methods, find those three things. If you cannot find the point of contact, the study was not integrated.

### Eyes-open design judgment

- **Logs are not the truth either.** Williams and colleagues computed hours per week as all seconds online across an account's characters, divided by the weeks since first login. That counts time spent AFK in a city, and it averages over a period that may not match the "typical week" a respondent had in mind. Part of `d_i` is a mismatch between two definitions of play. Say which construct each strand measures before you call a difference "bias".
- **A small bias difference can move a big conclusion.** In the EQ2 data the bias difference was about 2.4 hours a week, small against standard deviations of about 17 to 20 hours. It still hid more than half of the group difference, because the difference itself was small. Check `b_A − b_B` against `Δ_ℓ`, not against the spread.
- **Linked data raises the ethics stakes.** Matching survey answers to account records turns an anonymous survey into an identified one. The EQ2 study asked for consent before the survey and matched through an account number the researchers could not see. Week 10 covers what an ethics board will ask.
- **Choose the qualitative sample on the quantitative result, but write the rule first.** Selecting "interesting" players after browsing the data invites you to pick the cases that fit your story. A written rule, including contrast cases, is your protection.
- **Do not turn the interviews back into percentages.** Ten interviews that find a theme in seven people do not mean that 70% of players think so. The survey's job is to estimate prevalence. The interviews' job is to explain mechanisms.

### Check yourself (worked example)

1. In a survey linked to logs, group A reports 15.0 hours and logs 18.0. Group B reports 17.0 and logs 17.5. What gap does the survey show, what gap do the logs show, and what is the bias difference? Which group "plays more" according to each source?
2. Two groups each under-report by exactly 20% of their logged hours. Is the survey's group difference right? Use the identity to explain.
3. Why does the connecting rule in the example include one accurate reporter per group?

<details>
<summary>Answers</summary>

1. Survey gap `Δ_r = 15.0 − 17.0 = −2.0`, so B looks 2 hours ahead. Log gap `Δ_ℓ = 18.0 − 17.5 = +0.5`, so A actually plays more. Biases are `b_A = −3.0` and `b_B = −0.5`, so `b_A − b_B = −2.5`, and `0.5 + (−2.5) = −2.0`. The survey reverses the direction.
2. No, unless the groups play the same amount. Each bias is `−0.2 × ℓ̄`, so `b_A − b_B = −0.2 × Δ_ℓ` and `Δ_r = 0.8 × Δ_ℓ`. The survey shows 80% of the true gap. Proportional misreporting shrinks every difference toward zero.
3. Without contrast cases, you cannot tell whether a reason given by under-reporters (for example "I don't count time idling in town") is special to them. If accurate reporters say the same thing, it does not explain the discrepancy.

</details>

## 3. Three core designs

Almost every mixed study in game research is one of three basic designs, or a combination of them. Fetters, Curry and Creswell (2013) describe them, and Creswell and Plano Clark's textbook builds on the same set.

| Design | Order | Typical purpose | Game research example |
|---|---|---|---|
| **Convergent** | Both strands at once, merged at analysis | Triangulation, complementarity | Field notes on a raid night and the same night's combat logs, compared event by event |
| **Explanatory sequential** | Quantitative first, then qualitative to explain it | Explaining a surprising result | EQ2 hours discrepancy, then interviews with players selected on `d_i` |
| **Exploratory sequential** | Qualitative first, then quantitative to test or measure it | Development | Fieldwork in guilds finds "carry culture", and a survey then measures how common it is |

A short notation from the nursing researcher Janice Morse is used in many methods sections. Upper case marks the strand with priority, an arrow marks sequence, and a plus sign marks concurrency. `QUAN → qual` is an explanatory sequential study in which the numbers carry most of the weight. `QUAL + quan` is a convergent study led by fieldwork with a small quantitative component. Write your design in this notation in your proposal. It forces you to decide priority and timing.

### Four ways the strands meet

Fetters and colleagues list four integration methods. Every design needs at least one.

- **Connecting.** One strand chooses the sample for the other. The EQ2 follow-up and Tree House's centrality-stratified interviews both do this.
- **Building.** One strand shapes the instrument of the other. Interview themes become survey items, or field notes decide which events to log.
- **Merging.** The two datasets are brought together for analysis, as with linked survey and log records, or a joint display.
- **Embedding.** Collection and analysis link at several points, for example short interviews run inside an A/B test (MMO308 week 5) to explain why the variant changed behaviour.

### Integration at the reporting stage

At the end you still have to write one argument, not two. The three tools are a **narrative** that weaves findings theme by theme, **data transformation** (turning qualitative codes into counts, called quantitizing, or turning numeric groups into profiles, called qualitizing), and the **joint display**.

## 4. Joint displays and meta-inferences

A **joint display** is a table or figure that puts the two strands side by side, organised around the same units, so that a reader can see where they agree. Guetterman, Fetters and Creswell (2015) analysed published joint displays and found two common types. One is **statistics-by-themes**, where each row is a quantitative group and each column a qualitative theme. The other is the **side-by-side comparison**, where each row is a topic with the quantitative result, the qualitative result and the conclusion drawn from both.

The conclusion drawn from both is called a **meta-inference**. Fetters and colleagues classify its fit in three ways.

- **Confirmation.** Both strands lead to the same conclusion, and credibility goes up.
- **Expansion.** The strands diverge but address different aspects, so together they cover more.
- **Discordance.** The strands contradict each other. You report it, look for the source (a sampling difference, a measurement mismatch, a real contradiction), and do not hide it.

Here is a side-by-side joint display for a hypothetical follow-up to the EQ2 finding. The quantitative column uses the published figures. **The qualitative column is invented for teaching.** It shows what such a study might find, not what anyone found.

| Topic | Quantitative (linked records) | Qualitative (hypothetical interviews, n = 12) | Fit | Meta-inference |
|---|---|---|---|---|
| Size of under-reporting | Women −3.29 h, men −0.93 h | Most interviewees estimate "a normal week", not the heaviest ones | Expansion | Part of the gap may be a definition mismatch, not concealment |
| Reason for the gender difference | Bisexual women showed no significant discrepancy | Several women describe downplaying play hours to family | Confirmation | Supports a social-desirability account for some players |
| Idle time | Logs count every second online | Many players leave characters logged in while doing other things | Discordance with "logs = play" | Separate active from idle time before calling `d_i` misreporting |

Each row names its fit. A reader can challenge any row and trace it back to evidence in each strand.

### Quantitizing with care

Counting how many interviewees mentioned a theme is useful inside a joint display. It shows whether a theme came from one talkative person or from most of the sample. As UX201 week 12 put it, count participants, not mentions. Never report those counts as prevalence in the player base. If you need prevalence, the qualitative themes should build a survey item (exploratory sequential design), and the survey then measures it.

## 5. Planning a mixed study

Four decisions belong in your proposal, and each has a common failure.

- **Priority.** Which strand carries the main claim? Failure: a qualitative strand added at the end "for colour", with no power to change the conclusion.
- **Timing.** Concurrent or sequential? Sequential designs take longer, because the second strand cannot start until the first is analysed. Failure: planning an explanatory sequential study and leaving two weeks for interviews after the survey closes.
- **Sampling.** In a sequential design, is the second sample drawn from the first (nested), or separately? Nested samples allow linking and connecting. Failure: interviewing whoever answers a Discord post, then trying to connect their stories to survey groups they were never sampled from.
- **The point of integration.** Name the step where the strands meet (connecting, building, merging or embedding) and the joint display you will produce. Failure: no named point, which leaves you with two studies stapled together.

A useful test for any plan is to ask what result in one strand would change what you do in the other. If no possible result would change anything, the strands are not integrated.

## In-class activity (25 minutes)

Work in pairs. Each pair receives one research question from the list below.

- Why do players leave guilds within their first two weeks?
- Does a new "looking for group" tool change who players group with?
- What does "casual" mean to players on a hardcore raiding server?
- Do players who report high social motivation actually group more?

1. (5 min) Choose a design. Write it in Morse notation and name the purpose from Greene and colleagues' list.
2. (8 min) Specify each strand in one line (data source, sample, analysis). Name the integration method and the exact step at which it happens.
3. (7 min) Draw an empty joint display with the rows and columns you will fill.
4. (5 min) Write one result from the quantitative strand that would change your qualitative sampling or questions. If you cannot, revise the design.

Expected output: a half-page plan with notation, the two strands, the integration step, an empty joint display and the "what would change" sentence.

## Common misconceptions

- **"Any study with numbers and quotes is mixed methods."** Only if the strands are integrated at a named step. Otherwise it is two studies in one report.
- **"Logs are the truth, and surveys are the error."** Logs measure a defined construct, such as seconds online per account. If the survey asked about a different construct, part of the disagreement is definitional. Name both constructs.
- **"If everyone misreports, the comparison is ruined."** The identity `Δ_r = Δ_ℓ + (b_A − b_B)` shows that equal biases cancel in a comparison. The trouble comes when groups misreport differently, and that difference is itself worth explaining.
- **"Qualitative follow-up should target the most interesting cases."** Write a selection rule before you look, and include contrast cases. Otherwise you have picked the cases that fit your explanation.

## Check yourself

1. A studio finds that players who rate a new quest line highly complete it less often than players who rate it poorly. Name Greene and colleagues' purpose this result serves, a design that follows from it, and the integration method you would use.
2. Write `QUAL → quan` in words. Give a game research question it would suit.
3. Linked records show `Δ_ℓ = 3.0` hours and `Δ_r = 4.5` hours between veterans and new players. Compute `b_veterans − b_new`, taking veterans as group A. What might explain the sign?
4. A student's joint display row reads "Survey: 62% want harder raids. Interviews: 9 of 12 want harder raids. Fit: confirmation." What would you ask before accepting the fit?
5. Tree House stratified its interview sample by network centrality. Name the integration method and describe one way the interviews changed how the centrality measure should be read.

<details>
<summary>Answers</summary>

1. Initiation, because the contradiction is a new question. An explanatory sequential design (`QUAN → qual`) fits, with connecting integration, interviewing players sampled from the high-rating/low-completion and low-rating/high-completion cells.
2. A qualitatively led, exploratory sequential study with a small quantitative follow-up. Example: fieldwork in several guilds to learn how players define "carrying", followed by a short survey to measure how often players report being carried.
3. `b_A − b_B = Δ_r − Δ_ℓ = 4.5 − 3.0 = +1.5`. Veterans over-report relative to new players. One possibility is that veterans count time on the game's forums, Discord or theorycrafting as "playing", which the logs do not see. Another is that new players under-report.
4. Who each sample reached. If the interviewees were raiders recruited from the guild's Discord and the survey was shown at login, the two strands measure different populations. Also ask whether the survey and interview questions asked about the same construct.
5. Connecting. The interviews showed that high centrality did not always mean sociability or formal authority, and that low centrality could reflect a guild that had gone inactive rather than a peripheral player. So centrality should be read as "time grouped with guildmates", not as "social hub" or "leader".

</details>

## Lab / assignment hook

[Lab 08, linking a survey to logs](../labs/lab08.md). You link a supplied survey file to a supplied telemetry file by account id, compute discrepancies and the bias decomposition, apply a written connecting rule to choose interviewees, and build a joint display from a set of short supplied interview summaries. The lab's design memo is the mixed-methods section of your research proposal.

## Sources

- Williams, D., Consalvo, M., Caplan, S. & Yee, N. (2009). "Looking for Gender: Gender Roles and Behaviors Among Online Gamers." *Journal of Communication* 59(4), 700-725. https://doi.org/10.1111/j.1460-2466.2009.01453.x. EverQuest II, one server of each of four types; 7,129 respondents (5,719 men, 1,406 women) in just over two days; server hours computed as seconds played per account across characters divided by the window since first login; men reported 24.10 and logged 25.03 hours per week, women reported 26.03 and logged 29.32; bisexual women reported 29.28 and logged 29.83 (not significantly different); SDs 17.47 to 20.14. Author's copy (dmitriwilliams.com, LFGpaperfinal.pdf) rechecked in review, September 2026. The 2008 JCMC paper gives women's logged hours as 29.31.
- Williams, D., Yee, N. & Caplan, S. E. (2008). "Who Plays, How Much, and Why? Debunking the Stereotypical Gamer Profile." *Journal of Computer-Mediated Communication* 13(4), 993-1018. https://doi.org/10.1111/j.1083-6101.2008.00428.x. First linkage of survey data to operator-collected play data; about 7,000 EQ2 players; the in-game item incentive; informed consent before the survey.
- Williams, D., Ducheneaut, N., Xiong, L., Zhang, Y., Yee, N. & Nickell, E. (2006). "From Tree House to Barracks: The Social Life of Guilds in World of Warcraft." *Games and Culture* 1(4), 338-361. https://doi.org/10.1177/1555412006292616. Three-step method: participant observation, a census of three servers in January 2006 used to build a sampling frame stratified by server type, faction, guild size and centrality, then 48 interviews in February and March 2006; the finding that the centrality assumption "did not entirely bear out".
- Ducheneaut, N., Yee, N., Nickell, E. & Moore, R. J. (2007). "The Life and Death of Online Gaming Communities." *Proceedings of CHI 2007*, 839-848. https://doi.org/10.1145/1240624.1240750. The authors' play since the November 2004 launch framed the analysis; cities excluded from co-location ties because characters idle there.
- Fetters, M. D., Curry, L. A. & Creswell, J. W. (2013). "Achieving Integration in Mixed Methods Designs: Principles and Practices." *Health Services Research* 48(6 pt 2), 2134-2156. https://doi.org/10.1111/1475-6773.12117. Three basic designs; connecting, building, merging, embedding; narrative, data transformation and joint display; fit as confirmation, expansion or discordance.
- Greene, J. C., Caracelli, V. J. & Graham, W. F. (1989). "Toward a Conceptual Framework for Mixed-Method Evaluation Designs." *Educational Evaluation and Policy Analysis* 11(3), 255-274. https://doi.org/10.3102/01623737011003255. The five purposes.
- Guetterman, T. C., Fetters, M. D. & Creswell, J. W. (2015). "Integrating Quantitative and Qualitative Results in Health Science Mixed Methods Research Through Joint Displays." *Annals of Family Medicine* 13(6), 554-561. https://doi.org/10.1370/afm.1865. Statistics-by-themes and side-by-side displays as the most common types.
- Creswell, J. W. & Plano Clark, V. L. (2018). *Designing and Conducting Mixed Methods Research* (3rd ed.). SAGE.
- Morse, J. M. (1991). "Approaches to Qualitative-Quantitative Methodological Triangulation." *Nursing Research* 40(2), 120-123. https://doi.org/10.1097/00006199-199103000-00014. The priority and sequence notation.

## Interactive spec: examples/w08-say-and-log.html

**The one insight:** a group comparison made with self-reports equals the true comparison plus the difference in reporting bias, so a bias gap that is small against the spread can shrink, erase or reverse a real difference, while the logged bars never move.

**Layout.** Two linked panels side by side at 1280px, stacked at 390px (scatter first).

- **Left panel, scatter.** x-axis logged hours per week 0 to 50, y-axis reported hours 0 to 50. The line `reported = logged` drawn and labelled. Group F as filled circles, group M as open squares (shape and colour both differ). A small horizontal tick on each group's side shows its mean. When "select interviewees" is on, the selected points get a ring and a label.
- **Right panel, gaps.** Two horizontal bar pairs, "Survey gap `Δ_r`" and "Log gap `Δ_ℓ`", on a shared axis from −8 to +8 hours with zero marked. Between them, a bracket labelled `b_F − b_M` with its value. When `Δ_r` changes sign, the survey bar changes colour and a note appears, "The survey now reverses the direction."

**Data.** Two datasets, chosen by a toggle.

- "Lecture ten": the ten players of section 2 (F1 30/33, F2 20/27, F3 12/13, F4 40/42, F5 25/32, M1 22/24, M2 35/34, M3 15/18, M4 28/29, M5 10/10, reported/logged).
- "EQ2 published means": show only the four group means as large markers (men 24.10/25.03, women 26.03/29.32) with no individual points and no interviewee toggle.

**Controls** (keyboard accessible, with numeric readouts):

- Extra bias for group F, `e_F`, −6.0 to +3.0 hours, step 0.1, default 0. It shifts every F point's reported value by `e_F` (logged values unchanged).
- Extra bias for group M, `e_M`, same range, default 0.
- Toggle "select interviewees" (lecture ten only).
- Reset button.

**Formulas.**

```
r_i' = r_i + e_g          for player i in group g
d_i  = r_i' − ℓ_i
b_g  = mean(d_i in g)
Δ_r  = mean(r' in F) − mean(r' in M)
Δ_ℓ  = mean(ℓ in F) − mean(ℓ in M)
check: Δ_r = Δ_ℓ + (b_F − b_M)   (display both sides)
share shown = Δ_r / Δ_ℓ          (show "n/a" if Δ_ℓ = 0)
selection per group: sort by (d_i, id) ascending, take first two; add the player with smallest |d_i| (ties by id) if not already chosen
```

**Readouts:** each group's reported mean, logged mean and bias (one decimal), `Δ_r`, `Δ_ℓ`, `b_F − b_M`, and the share `Δ_r / Δ_ℓ` as a percentage.

**Test values.**

| Dataset | `e_F` | `e_M` | `Δ_r` | `Δ_ℓ` | `b_F − b_M` | Share | Selected |
|---|---|---|---|---|---|---|---|
| Lecture ten | 0 | 0 | 3.4 | 6.4 | −3.0 | 53% | F2, F5, F3; M3, M1, M5 |
| Lecture ten | −3.4 | 0 | 0.0 | 6.4 | −6.4 | 0% | — |
| Lecture ten | −5.0 | 0 | −1.6 | 6.4 | −8.0 | −25% | — |
| EQ2 means | 0 | 0 | 1.93 | 4.29 | −2.36 | 45% | — |

For the EQ2 dataset show two decimals. With the lecture ten at `e_F = −3.4`, the survey bars sit at zero and the note reads "The survey shows no difference."

**Accessibility and style.** Palette from `templates/interactive-tokens.css`, inline. Screen-reader summary states `Δ_r`, `Δ_ℓ` and the bias gap after every change (polite live region). Respect `prefers-reduced-motion`. No game art or logos; label the EQ2 dataset in text only.

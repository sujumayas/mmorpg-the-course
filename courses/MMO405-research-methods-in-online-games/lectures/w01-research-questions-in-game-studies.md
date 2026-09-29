# MMO405 · Week 01 — Research Questions in Game Studies

**Why this matters:** Every studio has a dashboard that says guild members stay longer. Half the design meetings you will sit in treat that as proof that guilds keep players. It isn't, and the reason is a question-writing problem before it is a statistics problem. This week you learn to write questions that say what kind of claim they make, so you pick a method that can support it.

**You will be able to:**
- Classify a research question as descriptive, associational, causal or interpretive, and name the kind of evidence each one needs.
- Compute the selection term that separates an observed group gap from a causal effect, and recover the effect by stratifying.
- Rewrite a vague topic into a question card with population, unit, construct, measure, comparison and time frame, and score it with the FINER criteria.
- Critique a published or studio claim by naming the question it answered and the question it implies.

**Before class:** Boellstorff, Nardi, Pearce and Taylor, *Ethnography and Virtual Worlds* (2012), chapter "Research Design and Preparation" (pp. 52-64). Castronova, Ross and Knowles, "Designer, Analyst, Tinker: How Game Analytics Will Contribute to Science," in Seif El-Nasr, Drachen and Canossa (eds.), *Game Analytics* (2013), pp. 665-687. Skim the abstract and figure 1 of Egami et al. (2024), listed in Sources.

**Prerequisites from earlier courses:** [MMO305 week 2, playing alone together](../../MMO305-social-systems-and-online-behaviour/lectures/w02-playing-alone-together.md) (three ways of counting togetherness from one log). [MMO301 week 9, motivation research beyond Bartle](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w09-motivation-research-beyond-bartle-yee.md) (how a construct becomes a scale). [MMO308 week 5, A/B testing design](../../MMO308-live-operations-analytics-and-experimentation/lectures/w05-ab-testing-design.md) (randomizing players). [MA102 week 12, descriptive statistics for playtests](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md) (rates and fair comparisons).

**Interactive:** [examples/w01-selection-gap.html](../examples/w01-selection-gap.html). Keep it open during section 2.

---

## 1. From a topic to a question

A topic is something you are curious about. "Guilds." "Toxicity in ranked play." "Gold sellers." A research question is a sentence that could be answered wrong. It names who you are studying, what you will measure and what you will compare. Until you have one, you cannot choose a method, estimate how much data you need, or tell an ethics board what you plan to do.

This course treats a question as having a **claim type**. The claim type is the strongest sentence your answer will be allowed to say. There are four you will use all semester.

| Claim type | Template | Guild example | Evidence that can answer it |
|---|---|---|---|
| Descriptive | How much, how many, how often? | What share of players still active after 30 days belong to a guild? | A census or a well-drawn sample, clear definitions |
| Associational | Does X go with Y? | Are guild members retained at a higher rate than non-members? | Descriptive data on both X and Y for the same units |
| Causal | Does X change Y? | Does joining a guild raise a player's chance of staying 30 days? | Randomization, a natural experiment, or strong assumptions you must defend |
| Interpretive | What does X mean to the people involved, and how does it work? | How do players decide a guild is worth staying for? | Interviews, fieldwork, documents, close reading |

The first three are quantitative in style and the fourth is qualitative. You will meet all four families of method in this course. Weeks 2 to 5 cover the numbers, weeks 6 and 7 the interpretive work, and week 8 how to combine them.

Two rules follow from the table. First, a method can only answer questions at or below its claim type. A server log can answer the descriptive and associational guild questions perfectly and cannot, by itself, answer the causal one. Second, the claim type belongs in the question. If your question says "does joining a guild raise retention," your paper had better contain a design that separates joining from everything that comes with it. If you only have logs, ask the associational question and say so.

### Constructs and measures

The words in a question are usually **constructs**, ideas that cannot be counted directly: sociability, commitment, well-being, toxicity. To answer the question you **operationalize** each construct, meaning you choose a concrete measure that stands in for it.

You have already seen how much this choice matters. In MMO305 week 2 you counted "playing together" three ways from the same census of World of Warcraft characters and got answers that disagreed by a factor of five or more. In MMO301 week 9 you saw how Yee turned "motivation" into factor scores. Debeauvais, Nardi, Schiano, Ducheneaut and Yee (2011) studied what keeps World of Warcraft players committed, using a questionnaire answered by 2,865 players in North America, Europe, Taiwan and Hong Kong. They measured commitment three ways: weekly play time, stop rate and the number of years a respondent had played. Those three measures do not have to agree. A player who logs 30 hours a week for a single year and a player who has logged 5 hours a week for six years are both "committed," in different senses. A question that says "commitment" without saying which one is two or three questions pretending to be one.

### Population, unit and time frame

Three more choices sit inside every question.

- The **population** is everyone the answer is meant to be about. "Players of this game" is too loose. Is it everyone who ever created an account, everyone who logged in last month, or everyone who reached the level cap?
- The **unit of analysis** is the thing each row of your data describes. In an MMO this is rarely obvious. One person can own several accounts, one account can hold many characters, and one guild holds many accounts. Week 3 shows how Williams, Yee and Caplan (2008) handled this for EverQuest II.
- The **time frame** says when. Retention after 7 days and after 90 days are different quantities. A finding from a game's launch month may not hold two expansions later.

Name all three and a reader can tell whether your study says anything about their game.

## 2. Worked example: do guilds keep players?

### The hook: the same survey, opposite signs

Between 2020 and 2022, Nintendo Switch and PlayStation 5 consoles were in short supply in Japan, and many retailers sold them by lottery. Egami, Rahman, Yamamoto, Egami and Wakabayashi (2024) surveyed 97,602 people aged 10 to 69, of whom 8,192 had entered a console lottery. Before running their main analysis, they did what most studies do: they regressed well-being on how much people played, adjusting for a long list of background variables. In two of five estimates, more gaming went with **more** psychological distress.

Then they compared lottery winners with lottery losers. Winning is close to random, so winners and losers should differ only in their luck. Winners played about half an hour more per day. Winning a Switch lottery **reduced** psychological distress by roughly 0.2 standard deviations, and winning a PS5 lottery reduced it by roughly 0.1 and raised life satisfaction by roughly 0.2.

Same people, same survey, opposite conclusions. The difference is the question each analysis could answer. The first analysis answered an associational question: do people who play more feel worse? The lottery answered a causal one: does getting to play more change how you feel? Many people who play a lot are different in other ways, and those other differences leaked into the first answer. The rest of this section gives you a model for that leak. [MMO308 week 7](../../MMO308-live-operations-analytics-and-experimentation/lectures/w07-segmentation.md) flagged guild-joining as likely selection. The model below measures it.

### The model

Split players into two groups by whether they did something (joined a guild, bought a console, used the group finder). Call the doers the **treated** group, a word borrowed from medicine that means "got X," not "got medicine." Measure an outcome in each group, such as the 30-day retention rate. Then:

```
observed gap = causal effect + selection term
```

- The **observed gap** is the outcome rate among the treated minus the rate among the untreated. It is what the dashboard shows.
- The **causal effect** `δ` (delta) is how much the outcome would change for the same players if they were treated instead of untreated.
- The **selection term** is the part of the gap caused by the treated group being made of different people.

When players come in two kinds, say high-commitment `H` and low-commitment `L`, and the effect `δ` is the same for both kinds, the selection term has a simple form:

```
selection term = (r_H − r_L) × (s_T − s_U)
```

- `r_H` and `r_L` are the outcome rates of each kind **without** treatment.
- `s_T` is the share of high-commitment players among the treated. `s_U` is their share among the untreated.

Read it as two questions. Do the kinds of players differ in the outcome (`r_H − r_L`)? Do they differ in how often they get treated (`s_T − s_U`)? If either answer is "no," the selection term is zero and the observed gap is the causal effect. If both are "yes," the gap contains a bias you did not ask for.

### Numbers you can check

The following server is invented so the arithmetic is easy to follow. It has 1,000 new players. 400 are high-commitment and 600 are low-commitment. High-commitment players join guilds 75% of the time and low-commitment players 20% of the time. Without a guild, 70% of high-commitment and 30% of low-commitment players are still playing after 30 days. Set the causal effect of a guild to **zero**. Guilds do nothing in this world.

| Group | High-commitment | Low-commitment | Retained | 30-day retention |
|---|---|---|---|---|
| In a guild | 300 | 120 | 210 + 36 = 246 | 246 / 420 = 58.6% |
| No guild | 100 | 480 | 70 + 144 = 214 | 214 / 580 = 36.9% |
| Gap | | | | **+21.7 points** |

The dashboard reports a 21.7-point retention advantage for guild members, and the guilds did nothing. Check it against the model. `r_H − r_L = 0.70 − 0.30 = 0.40`. The share of high-commitment players is `300/420 = 0.714` among guild members and `100/580 = 0.172` among the rest, a difference of 0.542. The selection term is `0.40 × 0.542 = 0.217`, which is the whole gap.

Now look inside each kind of player separately:

| Stratum | Retention in a guild | Retention without | Gap |
|---|---|---|---|
| High-commitment | 70% | 70% | 0 |
| Low-commitment | 30% | 30% | 0 |

Comparing like with like makes the gap vanish. This is **stratification**: split the data by the variable that drives selection and compare within each slice. Give guilds a real effect of +5 points and each stratum shows a 5-point gap while the pooled gap grows to 26.7 points. The dashboard would say 26.7, and 21.7 of it would still be selection.

The code below reproduces both tables. It runs as shown with `.venv/bin/python`.

```python
# Observed gap versus causal effect for an invented 1,000-player server.
def server(delta, n_h=400, n_l=600, g_h=0.75, g_l=0.20, r_h=0.70, r_l=0.30):
    gh, gl = n_h * g_h, n_l * g_l           # guild members by kind
    uh, ul = n_h - gh, n_l - gl             # non-members by kind
    in_guild = (gh * (r_h + delta) + gl * (r_l + delta)) / (gh + gl)
    no_guild = (uh * r_h + ul * r_l) / (uh + ul)
    selection = (r_h - r_l) * (gh / (gh + gl) - uh / (uh + ul))
    return in_guild, no_guild, selection

for delta in (0.0, 0.05):
    a, b, sel = server(delta)
    print(f"delta={delta:.2f}  guild={a:.1%}  no guild={b:.1%}  "
          f"gap={a - b:+.1%}  selection={sel:+.1%}  gap-selection={a - b - sel:+.1%}")
```

Output:

```
delta=0.00  guild=58.6%  no guild=36.9%  gap=+21.7%  selection=+21.7%  gap-selection=+0.0%
delta=0.05  guild=63.6%  no guild=36.9%  gap=+26.7%  selection=+21.7%  gap-selection=+5.0%
```

### A visual you can move

Open [`examples/w01-selection-gap.html`](../examples/w01-selection-gap.html). The left view is the dashboard: two bars, retention with and without a guild, and the gap between them. The right view splits the same players into high- and low-commitment and draws each pair of bars side by side. Start with the causal effect at zero. The left view shows a big gap and the right view shows two pairs of equal bars.

Now drag the "high-commitment players who join" slider down toward the "low-commitment players who join" value. The left gap shrinks to nothing, though you have not touched the guilds at all. Push it the other way and the gap grows. Then set the causal effect to a negative number, say a guild that burns people out, and find a setting where the dashboard still shows guild members retaining better. The left view answers the associational question. Only the right view answers the causal one, and only because the simulation lets you see commitment. Real logs do not.

### Cross-context recognition

The same equation sits under every study that compares people who chose something with people who didn't. Learn to rewrite each one as `observed gap = effect + selection` and ask what drives the selection.

**Game time and well-being, correlational (2021).** Johannes, Vuorre and Przybylski (2021) linked surveys with play logs from Electronic Arts (*Plants vs. Zombies: Battle for Neighborville*) and Nintendo of America (*Animal Crossing: New Horizons*). Logged play time had a small positive association with affective well-being. The authors said plainly that their data do not allow causal claims. In our terms they measured the observed gap and could not size the selection term. People who feel well may simply have more time and energy to play.

**Game time and well-being, longitudinal (2022).** Vuorre, Johannes, Magnusson and Przybylski (2022) followed 38,935 players of seven games, including *EVE Online* and *Apex Legends*, for six weeks with three survey waves and logged play from each publisher. Instead of comparing heavy players with light ones, they asked whether a player's own change in play predicted that same player's later change in well-being. Comparing each player with themselves removes every stable difference between players, such as personality, job or free time, from the selection term. It cannot remove differences that change during the study, which the authors discuss as a limit. They found little to no evidence that play time affected well-being.

**Game time and well-being, natural experiment (2024).** The console lotteries of Egami et al. are the cleanest version. Winning is close to random, so `s_T − s_U` is close to zero for every background trait, measured or not. The authors checked 30 background variables and found winners and losers alike on almost all of them. Their covariate-adjusted regression pointed the wrong way for distress in two of five estimates. Selection can hide an effect or reverse it, as well as inflate it.

**A/B tests in live games.** When a studio randomizes which players see a feature, as in MMO308 week 5, it forces `s_T − s_U` to zero in expectation. That is the whole reason randomization works. Anything that breaks randomization, such as letting players opt in, brings the selection term back.

When you read "players who did X did better at Y," first ask what kind of player chooses X, and whether they would have done better at Y anyway.

### Eyes-open design judgment

- **Ask the question your data can answer.** An associational question answered well is worth more than a causal question answered badly. "Guild members are retained at 58.6% against 36.9%, and we have not separated selection from effect" is honest and useful to a designer deciding where to look next.
- **Stratification only fixes what you measured.** It worked above because the simulation tells you each player's commitment. In a real game you would stratify on proxies such as week-one play time or prior purchases, and whatever the proxy misses stays in the selection term. The Egami covariate-adjusted regression adjusted for many covariates and still got a misleading answer.
- **You often cannot randomize the thing you care about.** You cannot assign players to guilds. You can randomize an encouragement, such as which players get a guild-finder invitation, and study that. Week 5 covers these designs, and week 10 covers when even that needs ethics review.
- **Descriptive questions are not second-class.** Williams, Yee and Caplan (2008) mostly answered "who plays and how much" for EverQuest II. The answers contradicted the stereotype of the teenage male player (week 3 has the numbers) and changed what later researchers thought they needed to sample.

### Check yourself (worked example)

1. In the invented server, high-commitment players join guilds at 40% instead of 75%, and nothing else changes. Compute the new observed gap with `δ = 0`.
2. A dashboard shows players who bought a cosmetic are retained 15 points better than those who didn't. Name the two quantities in the selection term and say what you would expect each to be.
3. Why did comparing each player with themselves over time (Vuorre et al.) remove some but not all of the selection term?

<details>
<summary>Answers</summary>

1. Guild members are 160 high and 120 low, so `s_T = 160/280 = 0.571`. Non-members are 240 high and 480 low, so `s_U = 240/720 = 0.333`. Selection is `0.40 × 0.238 = 0.095`, so the observed gap is about 9.5 points, all selection.
2. `r_H − r_L`: engaged players retain better anyway, so positive. `s_T − s_U`: engaged players buy cosmetics more often, so also positive. Expect a large positive selection term. The 15 points could be mostly or entirely selection.
3. Stable differences between players cancel when each player is compared with themselves. Differences that change during the study, such as a new job that cuts both play time and mood, still bias the estimate.

</details>

## 3. Writing a good question

### The question card

A **question card** is one page that forces every choice from section 1 into the open. You will write one for your course proposal, and the lab this week makes you write two. Its fields:

| Field | What you write | Example |
|---|---|---|
| Topic | One phrase | Guilds and retention |
| Question | One sentence ending in a question mark | Among players who created their first character in March, are those in a guild on day 7 still active on day 30 at a higher rate than those not in a guild? |
| Claim type | Descriptive, associational, causal or interpretive | Associational |
| Population | Who the answer is about | New accounts on the game's EU servers, March |
| Unit | What one row is | Account (all characters merged) |
| Construct → measure | Each construct and its operational measure | "In a guild" → guild ID not null on day 7. "Retained" → at least one session between day 28 and day 30 |
| Comparison | What is compared with what | Retention of guild vs no-guild accounts |
| Time frame | When | Days 0-30 after account creation |
| Data source | Where the numbers come from | Server logs via the studio's analytics warehouse |
| Known threats | What could make the answer wrong | Selection by commitment. Accounts shared between people. Bots in guilds |
| Ethics flag | What needs review | Pseudonymized log data; no contact with players |

Notice what the example does. It says "associational" because it only has logs. It defines "in a guild" at a fixed day, because a player who joins on day 25 is not the same as one who joined on day 3. It lists selection as a threat instead of hoping nobody notices.

### Scoring a question with FINER

Hulley, Cummings and colleagues, in *Designing Clinical Research*, proposed five tests for a research question. The acronym is FINER, and it carries over to game research with little change.

- **Feasible.** Can you get the data, the players and the time? A causal question about guilds needs a studio willing to randomize something. A question about players' private chat needs access you probably won't get.
- **Interesting.** Does the answer matter to someone, a designer, a researcher, or the players? Would either answer be worth knowing?
- **Novel.** Does it confirm, extend or overturn something known? A replication counts (week 13 is devoted to it). A question already answered for your game does not.
- **Ethical.** Can you answer it without harming players, deceiving them beyond what an ethics board would approve, or exposing their data? [MMO402 week 12](../../MMO402-emergent-society-governance-and-ethics/lectures/w12-research-ethics-in-online-worlds.md) covers the principles, and this course's week 10 covers the review process.
- **Relevant.** Does it connect to theory or practice beyond your one dataset?

Score each from 1 to 3. A question that scores 1 on Feasible is dead whatever else it scores. A question that scores 1 on Interesting is alive but not worth your semester.

### Rewrites

Most first drafts fail in the same few ways. Here are four, with fixes.

| Draft | Problem | Rewrite |
|---|---|---|
| "Are MMOs addictive?" | Construct undefined; claim type hidden; population unbounded | "Among adult players of game G who log over 30 hours a week, what share meet the criteria of a validated problematic-play scale?" (descriptive) |
| "Does the new LFG tool make players more social?" | Causal claim with no design; "social" unmeasured | "In the two weeks after launch, did players randomly shown the tool form more repeat groups (the same two players grouped on at least two days) than players not shown it?" (causal, needs an A/B test) |
| "How do players feel about the economy?" | Fine as interpretive, but the population and setting are missing | "How do traders on one EVE-style market hub describe the risks they take, and what practices do they use to manage them?" (interpretive) |
| "What is the average level of players?" | Descriptive but the unit and time are missing, so the answer changes with every choice | "On 1 March, what was the median level of each account's highest-level character among accounts active in the previous 7 days?" (descriptive) |

The last one looks fussy. Answer the draft with real data and you will find several defensible answers. The rewrite has one.

## 4. Where questions come from in game studies

Game research grew out of several traditions that ask different kinds of questions. Knowing which one a paper comes from tells you what it will count as an answer.

**Media effects.** Psychology and communication research long asked what games do to players: aggression, well-being, addiction. The questions are causal, the methods are experiments and surveys, and the classic weakness is the one in section 2. Williams, Yee and Caplan (2008) argued that this "what are games doing to us" framing misses how actively players choose and shape their play. They also warned that effects research based on young male student samples would not generalize to the real, older, more mixed MMO population they had found.

**Game analytics and design research.** Studios and analytics researchers ask what players do and what a designer could change to make it different. The questions are descriptive and causal, the data are logs and A/B tests, and the answers feed decisions. The difference is the target. A studio wants to know what is true for its game next month. A researcher wants to know what is true of games or people in general.

**Interpretive and ethnographic research.** Anthropology and sociology ask what a world means to the people who live in it and how its social life works. The questions are interpretive and the methods are fieldwork, interviews and close observation. Boellstorff, Nardi, Pearce and Taylor's handbook, this course's second main text, argues for treating a virtual world as a real field site. You met the classic studies in MMO305 week 13, and you will do this work in weeks 6 and 7.

**Social science using games as a window.** Economists, network scientists and sociologists sometimes study MMOs because they offer complete records of a society. The question is about people, markets or networks in general, and the game is the dataset. Week 9's guild network analysis belongs here.

No tradition is the right one, and good projects often combine two (week 8). Know which question you are asking, so you judge your answer by the right standard.

### Studio questions and research questions

Studio questions differ from academic ones in four ways.

- A studio question has a **decision** attached. "Should we ship the guild finder?" The answer only needs to be good enough to choose.
- A research question has a **generalization** attached. "Do structured group-finding tools increase repeat play across games?" The answer must hold beyond one dataset.
- A studio has **access** and a researcher usually doesn't. Every telemetry study in this lecture exists because a company shared data: Sony Online Entertainment for Williams et al., Electronic Arts and Nintendo of America for Johannes et al., seven publishers for Vuorre et al. Week 3 looks at what such partnerships require.
- A studio can **randomize** its own game, but as MMO402 week 12 argued, the moment it wants to publish the result, it has moved from product testing to research, and research has rules.

## In-class activity (25 minutes)

Pairs. Each pair draws one topic card: gold sellers, raid difficulty, new-player mentoring, voice chat, housing, or cross-server grouping.

1. **Four questions (10 min).** Write one question of each claim type about your topic. Each must name a population and a measure.
2. **Selection audit (5 min).** For your associational question, name the most likely variable driving selection. Write the two brackets of the selection term for it and guess the sign of each.
3. **FINER (5 min).** Score all four questions. Circle the one you would choose for a one-semester project.
4. **Swap (5 min).** Give your circled question to another pair. They must name one way it could be answered wrongly.

Expected output: four questions with claim types, a selection-term sketch, FINER scores, and the other pair's objection written under your chosen question.

## Common misconceptions

- **"More data will fix selection."** A bigger log gives a more precise estimate of the observed gap, including its selection term. In the invented server, a million players would show the same 21.7-point gap with a tiny margin of error.
- **"If I control for enough variables, the association becomes causal."** Adjustment removes selection only through what you measured. The Egami observational analysis controlled for many covariates and still found more gaming going with more distress in two of five estimates, the opposite of the lottery result.
- **"Qualitative questions are just early versions of quantitative ones."** Interpretive questions ask about meaning and process. "How do players decide a guild is worth staying for?" has an answer that no retention rate contains.
- **"A descriptive study is not real research."** Descriptive findings overturned the stereotype of who plays MMOs and set the sampling for a decade of later work. A descriptive answer fails only when it is imprecise or the definitions are vague.

## Check yourself

1. Classify each by claim type: (a) "What share of raid attempts on the final boss end in a wipe?" (b) "Do players who read quest text complete more quests?" (c) "Does showing quest text in voiced cutscenes raise completion?" (d) "How do roleplayers negotiate what counts as in-character?"
2. In an invented game, 1,000 players are 50% high-commitment. High-commitment players use the group finder 60% of the time and low-commitment ones 20%. Without the finder, 30-day retention is 80% and 40%. The finder has a true effect of +3 points. What gap will the dashboard show?
3. Rewrite "Does PvP make players toxic?" into a question card's Question, Claim type, Unit and Construct → measure fields, using only data a studio could have.
4. A paper reports that players of an MMO who joined a voice-chat channel in week one had 20% higher 90-day retention. The authors conclude voice chat "drives retention." Name the claim type they measured and the one they concluded, and one design that could close the gap.

<details>
<summary>Answers</summary>

1. (a) Descriptive. (b) Associational. (c) Causal. (d) Interpretive.
2. Finder users are 300 high and 100 low, so `s_T = 0.75`. Non-users are 200 high and 400 low, so `s_U = 0.333`. Selection is `(0.80 − 0.40) × 0.417 = 0.167`. The gap is `0.03 + 0.167 ≈ 0.197`, about 19.7 points, of which 3 are the finder.
3. One answer: Question, "Among ranked-PvP players in season S, is the number of chat reports received per 100 matches higher for accounts that play more PvP?" Claim type, associational. Unit, account. Construct → measure, "toxic" → upheld chat reports per 100 matches; "PvP play" → PvP matches per week. Better answers also say that reports measure being reported, not being toxic, and list that as a threat.
4. Measured associational, concluded causal. A randomized encouragement (inviting a random half of new players to a voice channel) or a natural experiment (a region where voice chat launched later) could separate effect from selection.

</details>

## Lab / assignment hook

[Lab 01, question cards and a selection audit](../labs/lab01.md). You compute observed and stratified gaps on an invented 2,000-player log, then write two question cards for your own course proposal. The better card becomes page 1 of the proposal (20% of the grade).

## Sources

- Egami, H., Rahman, M. S., Yamamoto, T., Egami, C. & Wakabayashi, T. (2024). "Causal effect of video gaming on mental well-being in Japan 2020-2022." *Nature Human Behaviour* 8(10), 1943-1956. https://doi.org/10.1038/s41562-024-01948-y. Console lotteries for Nintendo Switch and PlayStation 5 in Japan; 97,602 respondents, 8,192 lottery participants; covariate-adjusted regression (two of five distress estimates positive); effects of about 0.2 s.d. (Switch, distress), about 0.1 s.d. (PS5, distress) and about 0.2 s.d. (PS5, life satisfaction); about 0.5 h more daily play; balance on 30 variables.
- Johannes, N., Vuorre, M. & Przybylski, A. K. (2021). "Video game play is positively correlated with well-being." *Royal Society Open Science* 8(2), 202049. https://doi.org/10.1098/rsos.202049. Telemetry from Electronic Arts and Nintendo of America linked to surveys (autumn 2020); small positive association; the authors' statement that the data do not allow causal claims.
- Vuorre, M., Johannes, N., Magnusson, K. & Przybylski, A. K. (2022). "Time spent playing video games is unlikely to impact well-being." *Royal Society Open Science* 9(7), 220411. https://doi.org/10.1098/rsos.220411. 38,935 players, seven games and publishers, six weeks, three waves (data collected May to September 2021); within-person design and its stated limits.
- Debeauvais, T., Nardi, B., Schiano, D. J., Ducheneaut, N. & Yee, N. (2011). "If you build it they might stay: retention mechanisms in World of Warcraft." *Proceedings of the 6th International Conference on Foundations of Digital Games*, 180-187. https://doi.org/10.1145/2159365.2159390. Sample of 2,865 players and the three commitment measures, as stated in the abstract.
- Williams, D., Yee, N. & Caplan, S. E. (2008). "Who plays, how much, and why? Debunking the stereotypical gamer profile." *Journal of Computer-Mediated Communication* 13(4), 993-1018. https://doi.org/10.1111/j.1083-6101.2008.00428.x. Data shared by Sony Online Entertainment; the critique of effects-only framing and of student samples (discussion section).
- Hulley, S. B., Cummings, S. R., Browner, W. S., Grady, D. G. & Newman, T. B. (2007). *Designing Clinical Research* (3rd ed.). Lippincott Williams & Wilkins. The FINER criteria, as attributed in later literature, e.g. Farrugia et al. (2010), "Practical tips for surgical research: Research questions, hypotheses and objectives," *Canadian Journal of Surgery* 53(4), 278-281.
- Boellstorff, T., Nardi, B., Pearce, C. & Taylor, T. L. (2012). *Ethnography and Virtual Worlds: A Handbook of Method*. Princeton University Press. Chapter "Research Design and Preparation," pp. 52-64.
- Castronova, E., Ross, T. L. & Knowles, I. (2013). "Designer, Analyst, Tinker: How Game Analytics Will Contribute to Science." In Seif El-Nasr, M., Drachen, A. & Canossa, A. (eds.), *Game Analytics: Maximizing the Value of Player Data*, pp. 665-687. Springer. https://doi.org/10.1007/978-1-4471-4769-5_29.

## Interactive spec: examples/w01-selection-gap.html

**The one insight.** A large retention gap between guild members and non-members can appear with zero causal effect. Inside each commitment group the bars are equal, so the whole gap is who joins, not what the guild does.

**Layout.** Two linked views side by side on desktop, stacked on mobile (dashboard view on top).

- **Left view, "What the dashboard shows."** Two vertical bars: 30-day retention of guild members and of non-members, labelled with percentages to one decimal. A bracket between the bar tops shows the observed gap in points. Under the bars, a stacked strip splits the gap into "causal effect" and "selection" segments with their values; the selection segment may be negative and then extends in the opposite direction, with the label "selection (hides effect)".
- **Right view, "Inside each kind of player."** Two pairs of bars, high-commitment and low-commitment, each pair showing guild vs no guild retention. Bar width proportional to the number of players in that cell, with the count printed on the bar. Each pair labelled with its within-stratum gap (always equal to δ).

**Controls** (all sliders, keyboard accessible, with numeric readouts):

| Control | Symbol | Range | Step | Default |
|---|---|---|---|---|
| Share of high-commitment players | `p_H` | 0.05-0.95 | 0.05 | 0.40 |
| High-commitment players who join | `g_H` | 0-1 | 0.05 | 0.75 |
| Low-commitment players who join | `g_L` | 0-1 | 0.05 | 0.20 |
| Retention without guild, high | `r_H` | 0-1 | 0.05 | 0.70 |
| Retention without guild, low | `r_L` | 0-1 | 0.05 | 0.30 |
| Causal effect of a guild | `δ` | −0.20 to +0.20 | 0.01 | 0.00 |

Retention with guild is clamped to [0, 1] per stratum. Total players fixed at 1,000; display counts rounded to whole players but compute with exact fractions. A "Randomize joining" button sets `g_H = g_L` to their mean, showing the selection term go to zero. A "Reset" button restores defaults.

**Formulas.**

```
H = 1000·p_H, L = 1000 − H
GH = H·g_H, GL = L·g_L, UH = H − GH, UL = L − GL
ret_guild = (GH·clamp(r_H+δ) + GL·clamp(r_L+δ)) / (GH+GL)
ret_none  = (UH·r_H + UL·r_L) / (UH+UL)
gap = ret_guild − ret_none
s_T = GH/(GH+GL), s_U = UH/(UH+UL)
selection = (r_H − r_L)·(s_T − s_U)          (exact when no clamping)
effect shown = gap − selection
```

If a group is empty (GH+GL = 0 or UH+UL = 0), show "no players in this group" instead of a bar.

**Test values.**

| p_H | g_H | g_L | r_H | r_L | δ | guild | none | gap | selection |
|---|---|---|---|---|---|---|---|---|---|
| 0.40 | 0.75 | 0.20 | 0.70 | 0.30 | 0.00 | 58.6% | 36.9% | +21.7 | +21.7 |
| 0.40 | 0.75 | 0.20 | 0.70 | 0.30 | 0.05 | 63.6% | 36.9% | +26.7 | +21.7 |
| 0.40 | 0.40 | 0.20 | 0.70 | 0.30 | 0.00 | 52.9% | 43.3% | +9.5 | +9.5 |
| 0.50 | 0.60 | 0.20 | 0.80 | 0.40 | 0.03 | 73.0% | 53.3% | +19.7 | +16.7 |
| 0.40 | 0.75 | 0.20 | 0.70 | 0.30 | −0.10 | 48.6% | 36.9% | +11.7 | +21.7 |

The last row is the one to point students to: guilds hurt retention by 10 points, and the dashboard still shows members retaining 11.7 points better.

**Accessibility and style.** Use the shared tokens from `templates/interactive-tokens.css`. Guild and no-guild bars use two palette colors plus a pattern (hatched for no guild) so the views work without color. All numbers also appear in a visually hidden live region updated on change. No game art; bars and labels only.

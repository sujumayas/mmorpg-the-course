# MMO405 · Week 03 — Telemetry as Research Data

**Why this matters:** For decades, research on games and players rested on asking people how much they played. When researchers finally got the server logs, the answers people gave turned out to track their real play only loosely, and effects that should have been visible were washed out. Telemetry fixes that problem and brings new ones: someone else decided what to log, one person is many rows, and every cleaning rule changes the answer. This week you learn to treat logs as evidence instead of truth.

**You will be able to:**
- Compute how measurement noise in a self-report attenuates a correlation, and correct an observed correlation for it.
- Choose and defend a unit of analysis (event, session, character, account, person) and a sessionization rule, and show how each changes a measured quantity.
- Write the cleaning and exclusion rules for a telemetry dataset and predict which way each one biases the result.
- Plan lawful, ethical access to linked telemetry: consent for linkage, pseudonymization, Article 89 safeguards and ethics review.

**Before class:** Ducheneaut and Yee, "Data Collection in Massively Multiplayer Online Games: Methods, Analytic Obstacles, and Case Studies," in *Game Analytics* (2013), pp. 641-664. Johannes, Vuorre and Przybylski (2021), sections 2 and 3 and figure 3. Boellstorff, Nardi, Pearce and Taylor (2012), chapter "Human Subjects Clearance and Institutional Review Boards" (pp. 151-158).

**Prerequisites from earlier courses:** [DB201 week 10, telemetry design](../../DB201-data-persistence-and-telemetry/lectures/w10-telemetry-design-events-and-properties.md) (events and properties). [DB201 week 11, pipelines](../../DB201-data-persistence-and-telemetry/lectures/w11-pipelines-collect-store-query.md) (duplicates, late events, clocks). [DB201 week 13, privacy and GDPR](../../DB201-data-persistence-and-telemetry/lectures/w13-privacy-gdpr-and-data-retention.md) (personal data, pseudonyms, retention). [MMO402 week 12, research ethics in online worlds](../../MMO402-emergent-society-governance-and-ethics/lectures/w12-research-ethics-in-online-worlds.md) (Belmont principles, re-identification). [Week 2 of this course](w02-quantitative-methods-overview.md) (effect sizes, Fisher's `z`).

**Interactive:** [examples/w03-self-report-vs-logs.html](../examples/w03-self-report-vs-logs.html). Keep it open during section 2.

---

## 1. Found data

A survey is **designed data**. You wrote every question for your study. Telemetry is **found data**. A studio logged it for its own reasons, such as billing, balancing, fraud detection or crash reports, and you are reusing it. Social scientists also call it **trace data**, because it is the trace that behaviour leaves in a system rather than a report of the behaviour.

That changes what you must check. With a survey, you worry about whether people understood and answered honestly. With telemetry, you worry about three other things.

- **Construct gap.** The log records what the system needed, not what you want. "Session length" is the time between a login and a logout event. It is not "time spent playing," because players idle, alt-tab, and sit in queues. It is not "time spent in the game world" if the logout event fires only on a clean exit.
- **Coverage.** The log covers one game, on the platforms that report to that server, for the period the studio kept. A player who plays four games shows up as a light player of yours.
- **Its own errors.** Johannes, Vuorre and Przybylski (2021) point out that session logging carries measurement error of its own. Vuorre, Johannes, Magnusson and Przybylski (2022) dropped sessions shorter than zero (0.5% of sessions) or longer than ten hours (1.9%), since impossible values like these come from logging errors.

None of this makes telemetry worse than self-report. For **behaviour**, it is usually much better, as the next section shows. It means telemetry is a measurement with a known procedure, and you must know that procedure.

## 2. Worked example: ask players how long they played

### The hook

In late 2020, Johannes and colleagues asked players of *Plants vs. Zombies: Battle for Neighborville* and *Animal Crossing: New Horizons* how many hours they had played in the past two weeks. Electronic Arts and Nintendo of America then supplied the logged play for the same accounts.

The two numbers matched poorly. Regressing each player's estimate on their logged time explained 15% of the variance in *Plants vs. Zombies* and 16% in *Animal Crossing* (`R² = 0.15` and `0.16`). That means a correlation of about 0.4 between what players said and what they did. On average, players overestimated by between half an hour and 1.6 hours. The spread was far larger, with a standard deviation of the error of 11.8 and 15.8 hours over the fortnight.

Then the part that matters for research. Logged play time was associated with well-being in both games. In *Plants vs. Zombies*, self-reported play time was not. Its 95% interval ran from −0.04 to +0.14 and included zero, while the logged-time interval ran from +0.02 to +0.18. The authors noted that with self-reports alone they could have missed an association entirely. Most earlier research on play time and well-being relied on self-reports.

### The model

Let `X` be the true quantity (logged hours, treated for now as correct), `S` the self-report and `Y` an outcome such as well-being.

```
S = X + b + e
reliability  ρ = var(X) / (var(X) + var(e))
r(S, X) = sqrt(ρ)
r(S, Y) = r(X, Y) × r(S, X)          (if e is unrelated to Y)
corrected r(X, Y) = r(S, Y) / r(S, X)
```

- `b` is **bias**, a constant offset such as "everyone adds an hour." It shifts means and does not change any correlation.
- `e` is **noise**, a random error that differs from player to player. It is what shrinks correlations.
- `ρ` (rho) is the **reliability** of `S` as a measure of `X`: the share of the variance in `S` that is real signal.
- The fourth line is **attenuation**. The correlation you observe with a noisy measure is the true correlation multiplied by `r(S, X)`, which is always at most 1. Spearman described it in 1904, together with the correction on the last line.

If the outcome `Y` is also measured with error, the full correction divides by `sqrt(ρ_S × ρ_Y)`. Week 4 shows how to estimate `ρ_Y` for a survey scale.

### Numbers you can check

Take a true correlation between play time and well-being of `r(X, Y) = 0.10`, the order of size in the studies above. The table shows what a study that uses self-reports would see, and how many players it would need for 80% power at the 5% level, using `n = ((1.96 + 0.8416) / atanh(r))² + 3`, rounded to the nearest player. Here 1.96 and 0.8416 are the standard normal values for a two-sided 5% test and 80% power.

| r(S, X) | Reliability ρ | Observed r(S, Y) | Players needed |
|---|---|---|---|
| 1.00 (logs) | 1.00 | 0.100 | 783 |
| 0.80 | 0.64 | 0.080 | 1,224 |
| 0.60 | 0.36 | 0.060 | 2,178 |
| 0.40 | 0.16 | 0.040 | 4,903 |
| 0.39 (Johannes et al., `R² = 0.15`) | 0.15 | 0.039 | 5,158 |

At the reliability found in these studies, a self-report study needs about six and a half times as many players as a log study to detect the same effect. Most of the self-report studies in the literature were far smaller than 5,000 players.

The simulation below builds the whole chain, with a one-hour bias and increasing noise. It runs as shown with `.venv/bin/python`.

```python
# Self-reported play time as logged time plus bias plus noise, and what it does to r.
import random
from statistics import correlation  # Python 3.10+

rng = random.Random(3)
n = 20_000
logged = [rng.gauss(20, 8) for _ in range(n)]                    # hours in two weeks
wellbeing = [0.10 * (x - 20) / 8 + rng.gauss(0, 1) for x in logged]  # true r close to 0.10
for noise_sd in (0, 8, 16, 18.3):
    said = [x + 1.0 + rng.gauss(0, noise_sd) for x in logged]    # +1 h bias, plus noise
    r_sx = correlation(said, logged)
    r_sy = correlation(said, wellbeing)
    print(f"noise SD {noise_sd:>4} h   r(self, logs)={r_sx:.2f}   "
          f"r(logs, wellbeing)={correlation(logged, wellbeing):.2f}   "
          f"r(self, wellbeing)={r_sy:.3f}   corrected={r_sy / r_sx:.2f}")
```

Output:

```
noise SD    0 h   r(self, logs)=1.00   r(logs, wellbeing)=0.11   r(self, wellbeing)=0.110   corrected=0.11
noise SD    8 h   r(self, logs)=0.72   r(logs, wellbeing)=0.11   r(self, wellbeing)=0.084   corrected=0.12
noise SD   16 h   r(self, logs)=0.46   r(logs, wellbeing)=0.11   r(self, wellbeing)=0.048   corrected=0.10
noise SD 18.3 h   r(self, logs)=0.40   r(logs, wellbeing)=0.11   r(self, wellbeing)=0.045   corrected=0.11
```

The theoretical values are `r(S, X)` = 1.00, 0.71, 0.45 and 0.40, and the true `r(X, Y)` is 0.0995. The simulated ones differ in the second decimal because 20,000 players still leave sampling noise of about ±0.007 in each correlation. Notice that the one-hour bias did nothing to any correlation, and that the corrected values land back on the sample's `r(logs, wellbeing)` of about 0.11, within sampling noise.

### A visual you can move

Open [`examples/w03-self-report-vs-logs.html`](../examples/w03-self-report-vs-logs.html). The left view is a scatter of logged hours against well-being for 500 simulated players, with the fitted line and `r`. The right view plots the same players' **self-reported** hours against the same well-being scores. Drag the "recall noise" slider up. The right cloud smears sideways, the line flattens, and `r` falls. The left view never changes, because the players' real behaviour and real well-being haven't changed. Only your ruler has.

Then drag the "bias" slider. Both clouds keep their shape and the right one slides along the x-axis. Bias moves means. Noise hides relationships. Last, switch on "error depends on well-being." In the demo this makes unhappier players over-report and happier ones under-report. Kahn and colleagues (below) found the opposite direction for enjoyment in EverQuest II, and either direction is a problem. Now the right view can show a correlation with the wrong size, or even a correlation when the left view has none. That is **differential error**, and no reliability correction fixes it.

### Cross-context recognition

**Digital media in general (Parry et al. 2021).** A preregistered meta-analysis of studies that measured both self-reported and logged use of phones, internet and social media combined 106 effect sizes. The average correlation between self-report and logs was `r = 0.38`, with a 95% interval of 0.33 to 0.42. Self-reports were rarely an accurate reflection of logged use. Games are not special here. Recall of screen time is poor across the board.

**EverQuest II, errors with a pattern (Kahn, Ratan and Williams 2014).** Comparing self-reported weekly play with Sony Online Entertainment's logs, this study found that errors were not random. Age, education, lower enjoyment of the game and a weaker sense of online community predicted greater under-reporting. Under-reporting that depends on enjoyment is differential error. A study relating self-reported play to enjoyment would inherit a built-in association that has nothing to do with how much people play.

**EverQuest II, the first linked census (Williams, Yee and Caplan 2008).** Sony supplied each respondent's logged play, averaged over the survey window and summed over all characters on the account. The mean was 25.86 hours per week (SD 19.06), compared with 7.5 hours per week of play for adults in an industry survey the authors cited. The log turned "how much do people play?" from a recall question into a measurement.

**Your own lab data.** In MMO308 week 10 you saw that forum posters and survey answerers are not the player base. This week's point is the within-person version. Even the players who answer will misremember, and the error is large enough to hide effects.

In every case, rewrite the situation as `S = X + b + e` and ask two questions. How large is `var(e)` compared with `var(X)`? Does `e` depend on the outcome?

### Eyes-open design judgment

- **Use logs for behaviour and self-report for experience.** Nobody can log how enjoyable a raid felt, why a player quit, or how many hours they spent on other games. Vuorre et al. took play time from logs and well-being and motivation from surveys. That split is the default for good reason.
- **Correction needs a reliability you trust.** Dividing by `r(S, X)` only works if you measured `r(S, X)` in a comparable sample. If you did, you probably had the logs and should use them. Report corrected values next to raw ones, never instead of them.
- **Don't correct your way to significance.** Correction inflates the point estimate and its interval together. It does not add information.
- **Logs are not free of error.** They drift when the client changes, drop events under load (DB201 week 11), and measure the account, not the person. Treat them as a better ruler, not a perfect one.

### Check yourself (worked example)

1. Self-reports correlate with logs at `r = 0.5`, and self-reported play correlates with a loneliness score at `r = 0.06`. Assuming random error in the self-report and a perfectly reliable loneliness score, estimate the log-based correlation.
2. Every player in a survey doubles their real play time when reporting it. What happens to `r(S, X)` and to `r(S, Y)`?
3. Why does the Kahn et al. finding make the correction in question 1 unsafe for a study of enjoyment?

<details>
<summary>Answers</summary>

1. `0.06 / 0.5 = 0.12`.
2. Nothing. Doubling is a linear rescaling, and correlations do not change under rescaling. Means and totals are wrong by a factor of two.
3. Under-reporting depends on enjoyment, so the error `e` is related to the outcome. The attenuation formula assumes it is not, and the correction can push the estimate in the wrong direction.

</details>

## 3. The unit problem

Every telemetry question hides a choice of **unit**, the thing one row describes. In an MMO there are at least five candidates.

| Unit | What it is | Typical trap |
|---|---|---|
| Event | One logged action: a kill, a trade, a chat line | Events are not independent; a raid produces thousands per minute |
| Session | A span of continuous play | Depends entirely on the sessionization rule |
| Character | One avatar | One person may have ten; many studies want the person |
| Account | One login and one bill | May be shared by a household, or one person may run several |
| Person | The human | Usually not observable from logs at all |

Williams, Yee and Caplan (2008) show how careful researchers handled this in EverQuest II. They made the player the unit of analysis while noting that one player can hold several characters across servers. To build the sampling frame, they took each account's most-played character over the prior year, its "main," and used that character's server as the player's home server. Play time was then summed over all the characters on the account. Each choice answers a different question. A character-level study of "time per character" would have given a smaller number and treated one person's alts as independent people.

### Sessionization

To turn a stream of events into "hours played," you need a **sessionization rule**: when does a gap in activity end a session? Here is one invented player's evening.

| Time | Event |
|---|---|
| 19:00 | Login |
| 19:00-19:40 | Combat and quest events every minute or two |
| 19:40-20:05 | No events (25 minutes) |
| 20:05-20:50 | Dungeon events every minute or two |
| 20:50-21:30 | No events (idle in town, 40 minutes) |
| 21:30 | Logout |

Three defensible rules give three answers.

| Rule | Sessions | Hours played |
|---|---|---|
| Login to logout | 19:00-21:30 | 2.50 |
| Activity, gaps over 30 min end a session | 19:00-20:50 | 1.83 |
| Activity, gaps over 10 min end a session | 19:00-19:40 and 20:05-20:50 | 1.42 |

The same evening is 1.42 or 2.50 hours, a factor of 1.76. If you compare two games whose logs use different rules, or one game before and after a patch changed the idle timeout, you are comparing rulers. Choose the rule from the construct: "time with the game running" suggests login to logout, and "time actively playing" suggests an activity rule. Then report it and test whether your conclusions survive the other rules. That check is called a **sensitivity analysis**.

## 4. Cleaning decides answers

Every telemetry study has a cleaning step. Write each rule down, give the reason, and say which way it pushes the result.

- **Impossible values.** Negative or over-long sessions, as in Vuorre et al. Dropping them is usually right. Capping them instead (setting any session over ten hours to ten) keeps the player in the data.
- **Bots and farmers.** Accounts that play 20 hours a day are real rows and fake players. Removing them lowers mean play time and may remove the heaviest "players" from an analysis of heavy play. Use the studio's own bot flags where they exist (MMO309 covers detection), and report how many accounts you removed.
- **Zeros and missing values.** A player who did not log in during the window has zero play time, not missing play time. Vuorre et al. studied active players: of 108,880 consenting players, 85% answered at least one well-being item, and of those, 42% had played during the study, leaving 38,935. The finding is about people who play, and the method section says so.
- **Changes across patches.** A new client version may start or stop logging an event, rename a property, or change the idle timeout. Line up your study window against the patch notes and the studio's tracking-plan history (DB201 week 10), and split the analysis at any change.
- **Survivorship.** A retention study that samples current players will miss everyone who left. A study of "veterans" measured today learns about the people who stayed, not about what made people stay.

A good rule of thumb is to write your cleaning rules before you look at the outcome variable, the same way you set the SESOI before the effect in week 2. Rules chosen after seeing results tend to be the ones that help.

## 5. Access, consent and data protection

### Getting the data

Almost every linked telemetry study you will read exists because a company agreed to share data. Sony Online Entertainment worked with Williams and colleagues. Electronic Arts and Nintendo of America worked with Johannes and colleagues. Seven publishers (Nintendo of America, Electronic Arts, CCP Games, Microsoft, Sony Interactive Entertainment, Square Enix and Ubisoft) worked with Vuorre and colleagues. Other routes include public APIs that some games offer, your own game or server, and collecting public pages. For each route, read the terms of service and ask your ethics board early, because "publicly visible" does not mean "free to collect and republish" (MMO305 week 13 introduced the Association of Internet Researchers' guidance on this).

A partnership agreement should settle at least what data is shared, at what level of aggregation, who holds the key that links IDs to accounts, how long the data is kept, and **who controls publication**. MMO402 week 12 explains why the last point must be in writing before the study starts.

### Consent for linkage

Linking a survey answer to a player's logs is the moment a study learns something new about a person. Current practice treats it as needing its own consent.

Vuorre et al. show the modern form. Participants read the study's purposes and procedures and agreed both to take part and to have their game-play data provided by the publisher. The study had approval from the University of Oxford's Central University Research Ethics Committee. Publishers created a hashed ID for each account, the survey URL carried that hashed ID, and the researchers joined surveys to logs through it without receiving names or emails.

Williams et al. (2008) show an earlier form. Players gave informed consent to the survey, but the paper reports that the log calculations were done separately, and that participants were unaware that their time online, server and character use were part of the research. Most ethics committees today would expect the consent form to say that logged play will be linked to the answers. The comparison is not a judgment on the earlier study. It shows how the norm moved, and which of the two designs your protocol should copy.

### Data protection in the EU and UK

If players are in the EU (or the UK, whose law keeps the same structure), the General Data Protection Regulation applies to their log data. DB201 week 13 covered the basics. Four points matter specifically for research.

- **Pseudonymized is still personal.** Recital 26 of the GDPR says data that could be attributed to a person with additional information remains personal data. A hashed account ID is pseudonymous while the publisher holds the mapping. Anonymous data falls outside the regulation, but the bar is that no one can re-identify the person by means reasonably likely to be used. MMO402 week 12 showed how few attributes it takes to single out a player.
- **Research reuse is allowed, with safeguards.** Article 5(1)(b) says further processing for scientific research is not incompatible with the original purpose, provided it follows Article 89(1). Article 89(1) requires appropriate safeguards, including data minimization, and pseudonymization where the research can still be done that way. Where the research can be done without identifying anyone, it should be.
- **Two meanings of consent.** The European Data Protection Board's consent guidelines (05/2020, section 7.2) separate consent as a GDPR legal basis from the informed consent that research ethics requires. A study can rely on another legal basis for processing, such as public interest or legitimate interests, with Article 89 safeguards, and still need participants' ethical informed consent. Your ethics application and your data protection notice are two different documents.
- **Keep it no longer than needed.** Article 5(1)(e) allows longer storage for research purposes, again under Article 89(1) safeguards. It does not allow indefinite storage by default. Put a deletion date in your data management plan.

These points are the structure of the law, not legal advice for a specific study. Universities have data protection officers, and a real study should talk to one.

### Ethics review

Research with human participants at a university goes to an ethics board before any data is collected. In the United States this is an Institutional Review Board operating under the Common Rule (MMO402 week 12). In the UK and much of Europe it is a university research ethics committee, like the Oxford committee that approved Vuorre et al. Boellstorff and colleagues' chapter describes what these boards look for in virtual-world research. Week 10 of this course walks through an application. For now, know that the application needs your question, your data sources, your consent and linkage procedure, your pseudonymization and storage plan, and what you will do if you find something that harms a player.

## In-class activity (25 minutes)

Groups of three. Each group gets a printed extract of an invented one-week event log for 12 accounts (about 400 rows) and a two-question survey the same accounts answered ("hours played this week"; "how satisfied are you with the game, 1 to 7").

1. **Sessionize (10 min).** Compute each account's hours under the login-to-logout rule and under a 15-minute activity rule. Mark the three accounts whose hours change most.
2. **Compare (5 min).** Plot self-reported hours against each version of logged hours (by eye, on the grid provided). Estimate which version the self-reports resemble more, and why.
3. **Clean (5 min).** Two accounts log over 100 hours in the week. Decide whether to keep, cap or drop them, write the rule, and say which way it moves the mean.
4. **Consent (5 min).** Write the one sentence your consent form needs so that linking these survey answers to this log is disclosed.

Expected output: a 12-row table with two hours columns, one cleaning rule with its direction of bias, and the consent sentence.

## Common misconceptions

- **"Logs are ground truth."** Logs are a better ruler for behaviour, with their own errors, rules and gaps. Vuorre et al. dropped about 2.4% of sessions as impossible.
- **"If players overestimate, the correlation is too high."** A constant overestimate changes means, not correlations. Random recall noise pulls correlations toward zero. Only error that depends on the outcome can push them in either direction.
- **"Hashed IDs make the data anonymous."** A hash the publisher can reverse, or that stays the same across datasets, is a pseudonym. Under Recital 26 the data are still personal data.
- **"The terms of service cover research."** They may give the studio a legal basis for processing. They are not the informed consent a research ethics board expects, and they rarely mention linkage to a survey (MMO402 week 12 makes the same point for experiments).

## Check yourself

1. A study finds `r = 0.05` between self-reported weekly play and a depression score among 600 players. The self-report correlates with logs at `r = 0.4` in similar samples. What is the corrected estimate? Would the original study have had 80% power to detect the corrected value's attenuated form?
2. Rewrite the sessionization example with a 45-minute idle rule. How many hours does the evening contain?
3. A studio shares character-level data: 30,000 characters from 11,000 accounts. A student reports a correlation between character level and weekly play with `n = 30,000`. Name two problems.
4. Your study links a survey to logs through a hashed account ID. The publisher keeps the mapping for 30 days to handle withdrawals and then deletes it. Before and after day 30, is your dataset pseudonymous or anonymous under the GDPR? What else would you have to check to call it anonymous?

<details>
<summary>Answers</summary>

1. `0.05 / 0.4 = 0.125`. The attenuated value is 0.05. Detecting `r = 0.05` with 80% power needs about `((1.96 + 0.8416) / atanh(0.05))² + 3 ≈ 3,137` players, so 600 was far too few.
2. Both gaps (25 and 40 minutes) are under 45 minutes, so the session runs from 19:00 to the last activity at 20:50: 1.83 hours, the same as the 30-minute rule. It becomes 2.50 only if the logout counts as activity, which is another rule to write down.
3. The unit is wrong for a player-level claim: 11,000 accounts, not 30,000 independent observations, so the standard error is too small. Also, weekly play per character splits one person's play across their alts, so a player with three characters looks like three light players.
4. While the mapping exists, pseudonymous and therefore personal data. After deletion it may be anonymous, but only if the remaining attributes (server, play pattern, rare items, timestamps) cannot single out a person by means reasonably likely to be used. MMO402 week 12's uniqueness calculation is the check.

</details>

## Lab / assignment hook

[Lab 03, sessionizing a log and auditing self-report](../labs/lab03.md). You sessionize an invented event log for 300 accounts under three rules, clean it, compare it with the same players' self-reported hours, and write the data management and consent section your course proposal will need.

## Sources

- Johannes, N., Vuorre, M. & Przybylski, A. K. (2021). "Video game play is positively correlated with well-being." *Royal Society Open Science* 8(2), 202049. https://doi.org/10.1098/rsos.202049. Surveys fielded in autumn 2020; self-estimates regressed on logs, `R² = 0.15` (PvZ) and `0.16` (AC:NH); mean overestimate 1.6 h (SD 11.8) and 0.5 h (SD 15.8); PvZ associations with well-being, logged β = 0.10 [0.02, 0.18], self-reported β = 0.05 [−0.04, 0.14]; note on telemetry's own error.
- Vuorre, M., Johannes, N., Magnusson, K. & Przybylski, A. K. (2022). "Time spent playing video games is unlikely to impact well-being." *Royal Society Open Science* 9(7), 220411. https://doi.org/10.1098/rsos.220411. Session exclusions (below 0 h, 0.5%; above 10 h, 1.9%); 108,880 consented, 85% answered, 42% of those active, 38,935 analysed; consent to publisher data sharing; hashed IDs; approval by Oxford's Central University Research Ethics Committee (SSH_OII_CIA_21_011); the seven publishers.
- Parry, D. A., Davidson, B. I., Sewall, C. J. R., Fisher, J. T., Mieczkowski, H. & Quintana, D. S. (2021). "A systematic review and meta-analysis of discrepancies between logged and self-reported digital media use." *Nature Human Behaviour* 5(11), 1535-1547. https://doi.org/10.1038/s41562-021-01117-5. 106 effect sizes; `r = 0.38` [0.33, 0.42].
- Kahn, A. S., Ratan, R. & Williams, D. (2014). "Why we distort in self-report: Predictors of self-report errors in video game play." *Journal of Computer-Mediated Communication* 19(4), 1010-1023. https://doi.org/10.1111/jcc4.12056. EverQuest II; predictors of under-reporting (from the abstract).
- Williams, D., Yee, N. & Caplan, S. E. (2008). "Who plays, how much, and why? Debunking the stereotypical gamer profile." *Journal of Computer-Mediated Communication* 13(4), 993-1018. https://doi.org/10.1111/j.1083-6101.2008.00428.x. Sampling by "main" character; play summed per account; 25.86 h/week (SD 19.06); the 7.5 h industry comparison; informed consent to the survey and participants' unawareness of the log linkage (method section).
- Spearman, C. (1904). "The proof and measurement of association between two things." *American Journal of Psychology* 15(1), 72-101. https://doi.org/10.2307/1412159. Attenuation and its correction.
- Regulation (EU) 2016/679 (General Data Protection Regulation), Recital 26, Article 5(1)(b) and (e), Article 89(1)-(2). Text via EUR-Lex and gdpr-info.eu (accessed September 2026).
- European Data Protection Board (2020). *Guidelines 05/2020 on consent under Regulation 2016/679*, version 1.1, section 7.2, paragraphs 153-161.
- Ducheneaut, N. & Yee, N. (2013). "Data Collection in Massively Multiplayer Online Games: Methods, Analytic Obstacles, and Case Studies." In Seif El-Nasr, M., Drachen, A. & Canossa, A. (eds.), *Game Analytics*, pp. 641-664. Springer. https://doi.org/10.1007/978-1-4471-4769-5_28.
- Boellstorff, T., Nardi, B., Pearce, C. & Taylor, T. L. (2012). *Ethnography and Virtual Worlds: A Handbook of Method*. Princeton University Press. Chapter "Human Subjects Clearance and Institutional Review Boards," pp. 151-158.

## Interactive spec: examples/w03-self-report-vs-logs.html

**The one insight.** Recall noise in self-reported play time flattens the relationship you are looking for while the players' real behaviour stays the same. Bias moves the cloud and leaves the correlation alone. Error that depends on the outcome can manufacture or reverse a relationship.

**Layout.** Two scatter plots side by side on desktop, stacked on mobile (logs first), sharing the y-axis scale.

- **Left view, "Logged hours."** x = logged hours in two weeks (0 to 60), y = well-being (standardized, −3.5 to 3.5). 500 points, least-squares line, and `r` printed to three decimals.
- **Right view, "What players said."** x = self-reported hours (same axis range; points outside are clamped to the edge and drawn hollow), same y values. Line and `r` printed. Below: `r(self, logs)`, reliability `ρ = r(self, logs)²`, corrected `r = r(self, wellbeing) / r(self, logs)`, and "players needed for 80% power at this r" using `n = ((1.96 + 0.8416) / atanh(|r|))² + 3`, rounded to the nearest whole player (show "∞" when `r = 0`).

**Data generation.** Seeded PRNG (mulberry32, seed 405) so a given slider state always shows the same points. Draw once per seed: `x_i ~ N(20, 8)` hours, `u_i ~ N(0, 1)`, `v_i ~ N(0, 1)`, `w_i ~ N(0, 1)`. Then

```
y_i  = ρxy · (x_i − 20)/8 + sqrt(1 − ρxy²) · u_i
s_i  = x_i + b + σ_e · v_i + k · σ_e · y_i
```

where `k` is 0 unless "error depends on well-being" is on, in which case `k = −0.5` (unhappier players over-report, happier ones under-report; the sign is a design choice for the demo and the label says so). `w_i` is reserved for a "draw new players" button that reseeds.

**Controls.**

| Control | Symbol | Range | Step | Default |
|---|---|---|---|---|
| True correlation, logs and well-being | `ρxy` | −0.5 to 0.5 | 0.01 | 0.10 |
| Recall noise SD (hours) | `σ_e` | 0 to 30 | 0.1 | 18.3 |
| Bias (hours) | `b` | −10 to 10 | 0.5 | 1.0 |
| Error depends on well-being | toggle | off/on | — | off |
| Draw new players | button | — | — | — |
| Noise presets | buttons | 0, 8, 16, 18.3 | — | — |
| Differential error demo | button | sets `ρxy = 0`, `σ_e = 10`, toggle on | — | — |

**Theoretical readout** (shown in small type under the sample values so students can compare): `r(S, X) = 8 / sqrt(64 + σ_e²)` and `r(S, Y) = ρxy · r(S, X)` when `k = 0`.

**Test values** (theoretical, `k = 0`, `ρxy = 0.10`).

| σ_e | r(S, X) | ρ | r(S, Y) | n needed at r(S, Y) |
|---|---|---|---|---|
| 0 | 1.000 | 1.000 | 0.100 | 783 |
| 8 | 0.707 | 0.500 | 0.071 | 1,568 |
| 16 | 0.447 | 0.200 | 0.045 | 3,922 |
| 18.3 | 0.401 | 0.160 | 0.040 | 4,890 |

With the toggle on, `ρxy = 0`, `σ_e = 10`: the right view should show a clearly negative `r` (theoretical `cov(S, Y) = −0.5 · 10 = −5`, `sd(S) = sqrt(64 + 100 + 25) ≈ 13.7`, `r ≈ −0.36`) while the left view shows `r ≈ 0`.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. Points drawn at 50% opacity so density shows; both lines use the accent color with distinct dash patterns. A visually hidden live region reports the two `r` values after each change. Reduced motion: points jump to new positions without animation.

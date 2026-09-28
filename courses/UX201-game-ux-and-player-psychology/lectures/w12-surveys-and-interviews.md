# UX201 · Week 12 — Surveys and Interviews

**Why this matters:** Telemetry tells you what players did. Surveys and interviews are how you find out what they felt and why. They are also the easiest research methods to run badly, because a survey with a thousand answers feels solid even when the thousand people who answered are not the players you care about. This week you learn to write questions that measure what you mean, to talk to players without leading them, and to ask of every result, "who answered?"

**You will be able to:**
- Compute how unequal response rates shift an observed survey result, using the odds form of response bias, and show why a larger sample does not remove the shift.
- Correct a survey result by weighting respondents to match known player groups from telemetry.
- Write and critique survey items, spotting double-barrelled, leading and hypothetical questions, and choose between a validated scale and a custom item.
- Plan a semi-structured interview study, estimate how many interviews you need to hear a problem at least once, and code the results into themes.

**Before class:** Ryan, Rigby and Przybylski (2006), "The Motivational Pull of Video Games: A Self-Determination Theory Approach", *Motivation and Emotion* 30(4), read the method section of Study 1 (how PENS was built and scored). Nick Yee (2006), "Motivations of Play in MMORPGs", the introduction and method (pages 1-3). Hodent, *The Gamer's Brain* (CRC Press, 2017), reread the chapter "Usability" (pp. 109-134).

**Prerequisites from earlier courses:** [MA102 week 13, sampling, confidence and why n=5 lies](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md), for the Wilson interval and section 5 on bias. This week does not re-teach intervals; it builds on them. [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md), for "at least once in n tries", which we reuse for interviews. [MA102 week 12, descriptive statistics for playtests](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md). [GD101 week 7, playtesting](../../GD101-introduction-to-game-design/lectures/w07-playtesting-observe-dont-explain.md), for the "observe, don't explain" rule, which applies to interviews too. Looking ahead, [MMO304 week 12, economic telemetry and dashboards](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w12-economic-telemetry-and-dashboards.md) (year 3) builds the kind of telemetry this week uses to check who answered. Here, telemetry just means counts of players by group that the game already logs.

**Interactive:** [examples/w12-who-answers.html](../examples/w12-who-answers.html). Use it during section 2.

---

## 1. Asking instead of watching

[Week 8](w08-usability-testing-methods.md) and [week 9](w09-heuristic-evaluation-for-games.md) were about watching players and inspecting the game. This week is about asking. Asking has one great strength and one great weakness.

The strength is access to the inside. No log file records that a player felt cheated by a boss, that they quit because their friend quit, or that they didn't know the crafting menu existed. Only the player can tell you.

The weakness is that people are poor witnesses to their own behaviour. They forget, they rationalise, they tell you what they think you want to hear, and they predict their future behaviour badly. So researchers follow a rule that runs through this whole lecture. **Ask about experiences and recent specific events. Measure behaviour with telemetry or observation.** "How did you feel when the boss one-shot you?" is a good question. "How often do you use the map?" is a question telemetry answers better.

Two methods do most of the asking.

- A **survey** asks many people the same fixed questions, usually with fixed answer options. It gives you numbers you can compare across groups and over time.
- An **interview** asks a few people open questions and follows up on their answers. It gives you reasons, stories and vocabulary.

They work best together. Interviews find out what to ask. Surveys find out how common it is. Interviews then explain the surprising numbers.

## 2. Worked example: who answered?

### The hook

Between 2016 and 2019, Valve changed how the Steam review score is computed several times, and none of the changes altered a single review. In May 2016 Steam started showing a separate score for reviews from the last 30 days next to the all-time score. In September 2016 it stopped counting reviews from players who activated the game with a product key rather than buying it on Steam. In 2017 it added a histogram of reviews over time, so buyers could spot short bursts. In March 2019 it began detecting bursts of off-topic reviews, such as protests about something outside the game, and excluding every review from those periods from the score.

A game on Steam can have hundreds of thousands of reviews. With that many answers, sampling error is tiny. So why keep changing the rules? Because every one of those changes is about **who counts**, not how many. More answers never fixed who answered. Your post-playtest survey has the same problem at a smaller scale, and you can put a number on it.

### The model

Suppose a fraction `p` of your players are satisfied. Satisfied players answer your survey at rate `r₁`, and unsatisfied players at rate `r₀`. Among the people who answer, the observed fraction satisfied is

```
p_obs = p × r₁ / (p × r₁ + (1 − p) × r₀)
```

This looks messy, and it becomes clean in **odds**. The odds of an event are `p / (1 − p)`, the chance it happens divided by the chance it doesn't. Divide the top and bottom of `p_obs` by `(1 − p) × r₀`:

```
odds_obs = odds_true × k        where   k = r₁ / r₀
```

- `odds_true = p / (1 − p)`, the odds in the population you care about.
- `odds_obs = p_obs / (1 − p_obs)`, the odds among the people who answered.
- `k` is the **response-rate ratio**. `k = 1` means both groups answer equally often. `k = 0.5` means unhappy players are twice as likely to answer. `k = 2` means happy players are.

In words: **unequal response rates multiply the odds by k**. Sample size does not appear anywhere in this equation. That is the whole lesson.

To convert back from odds to a fraction, use `p = odds / (1 + odds)`.

### Numbers you can check

Let the true satisfaction be `p = 0.70`. Then `odds_true = 0.70 / 0.30 = 2.33`.

| Who answers more? | k | odds_obs | p_obs | Error |
|---|---|---|---|---|
| Nobody (equal rates) | 1 | 2.33 | 70.0% | 0 |
| Unhappy players, 2× | 0.5 | 1.17 | 53.8% | −16.2 points |
| Unhappy players, 3× | 0.33 | 0.78 | 43.8% | −26.2 points |
| Happy players, 2× | 2 | 4.67 | 82.4% | +12.4 points |
| Happy players, 3× | 3 | 7.00 | 87.5% | +17.5 points |

Check the second row by hand. `odds_obs = 2.33 × 0.5 = 1.17`, and `p_obs = 1.17 / 2.17 = 0.538`.

Now add sample size. Take the `k = 0.5` row and use the Wilson 95% interval from MA102 week 13.

| Respondents | Satisfied | Wilson 95% interval | Contains the true 70%? |
|---|---|---|---|
| 100 | 54 | 44.3% to 63.4% | No |
| 1,000 | 538 | 50.7% to 56.9% | No |
| 10,000 | 5,385 | 52.9% to 54.8% | No |

The interval narrows by a factor of ten as responses grow by a factor of a hundred. It narrows around 53.8%, a number that is 16 points wrong. The larger survey is more precise and no more accurate. It will also convince more people.

Three things stand out.

1. **Moderate differences in who answers make large errors.** A factor of two in response rate moves a 70% result by 12 to 16 points. Factors of two are common. Players who just rage-quit a match and players who just won it are both more likely to answer than players who felt nothing much.
2. **The error is not symmetric in points.** `k = 0.5` and `k = 2` are equal and opposite in odds, but they move `p` by −16 and +12 points, because odds stretch near 0% and 100%.
3. **The fix is not more answers.** The fix is to know `k`, or to change who you ask.

### A visual you can move

Open `examples/w12-who-answers.html`. The left view shows what the survey reports, the Wilson interval as a horizontal bar. It draws no true value, because the team running the survey doesn't know it. Drag the respondents slider from 50 to 10,000 and the bar tightens. The right view shows the same bar with the true satisfaction added as a dashed line. At `k = 1` the bar tightens onto that line. Drag `k` away from 1 and the whole bar slides off the line, while the respondents slider only makes it thinner. The chart below plots the reported satisfaction against `k`, and the number of respondents doesn't appear in it at all.

The one thing to notice: with `k = 0.5` and 10,000 respondents, the left view looks like a very confident result. The right view shows that it is confidently wrong. Toggle "weight by known groups" to see the correction from section 3 pull the bar back.

### Cross-game recognition

**Steam reviews (2016-2019).** Each of Valve's changes is a decision about `k`. Players who got a key for free, or from the developer, may review at a different rate and with a different lean from buyers, so they were removed from the score. Players caught up in a protest review at a much higher rate for a short time, so those periods were removed. The "recent" score limits the sample to people who played the current version. None of these changes made the sample bigger. All of them changed who is in it.

**The Literary Digest poll of 1936.** The magazine mailed about 10 million ballots, received 2.38 million back, and predicted that Alf Landon would win with 57% of the popular vote. Franklin Roosevelt won in a landslide. The mailing list came from magazine subscribers, car owners and telephone users, groups that were richer than average during the Depression. Later analysis found that non-response, with Roosevelt's opponents more eager to reply, was the biggest source of the error. George Gallup's poll of about 50,000 people called the result correctly. Same equation, no game: `k` far from 1 and a huge `n` that didn't help.

**Yee's motivations survey (2006).** Yee's factor analysis of why people play MMORPGs used 3,200 respondents to an online survey of 39 items. That is a large sample, and his component model is still widely used, including in this course in week 6. The worked example tells you what question to ask of it. Who fills in a 39-item online survey about their MMO motivations, and who doesn't? The answer doesn't make the model wrong. It tells you which population the percentages describe.

**Your own in-game survey (invented but typical).** A studio shows a one-question satisfaction survey at the end of a match. Players who alt-F4 out of a loss never see it. That is `r₀` pushed toward zero for the angriest players, and it inflates `p_obs`. Showing the survey on the next launch instead, or to a random sample by email, changes `k`.

In all four cases, write the result as `odds_obs = odds_true × k` and ask what `k` is. If you can't estimate it, you can't read the number.

### Eyes-open design judgment

- **Estimate `k`, don't assume it.** Send the survey to a random sample of players (drawn from your account list, not from those who happen to be online), then compare the telemetry of those who answered with those who didn't: playtime, level, spending, whether they are still playing a week later. Big differences mean `k` is far from 1 for anything related to those variables.
- **Change who you ask.** A random invitation, a short survey, a reminder, and asking at a neutral moment (not straight after a win or a loss) all bring `k` closer to 1. None of them gets it to exactly 1.
- **Weighting helps only for what you can see.** Section 3 shows how to weight respondents to match known groups. It fixes the part of the bias that runs through those groups. It cannot fix a bias in something telemetry doesn't see, such as mood.
- **Self-selected feedback is still useful.** Reviews, forums and support tickets are biased samples, and they are also early warnings. Use them to find problems, then measure how common the problems are with a sample you control.
- **Report who answered.** Every survey result in a UX report (week 14) should state the invitation method, the response rate and how respondents differed from the player base. A reader who knows `k` can judge the number. A reader who doesn't will trust `n`.

### Check yourself (worked example)

1. True satisfaction is 60%. Happy players answer at 4% and unhappy players at 10%. What satisfaction does your survey show?
2. A survey shows 80% of respondents want a harder mode. You learn from telemetry that players who finished the game answered at three times the rate of those who didn't, and you suspect finishers want a harder mode more. If finishing and wanting a harder mode go together, which way is 80% wrong?
3. A team's survey reports 45% satisfied with a margin of error of ±1 point from 9,000 responses. You suspect unhappy players were 1.5 times as likely to answer. What is your best estimate of the true satisfaction?

<details>
<summary>Answers</summary>

1. `k = 0.04 / 0.10 = 0.4`. `odds_true = 1.5`, `odds_obs = 0.6`, `p_obs = 0.6 / 1.6 = 37.5%`.
2. Too high. The group more likely to answer is also the group more likely to want the harder mode, so `k > 1` for "wants harder mode" and the observed share overstates it.
3. `k = 1 / 1.5 = 0.667`. `odds_obs = 0.45 / 0.55 = 0.818`. `odds_true = 0.818 / 0.667 = 1.23`, so `p ≈ 55%`. The ±1 point margin describes only sampling error. The bias is ten times larger.

</details>

## 3. Weighting by known groups

When you know how respondents differ from the player base on something telemetry measures, you can **weight** the answers. This is called post-stratification. Each group's answers count in proportion to its share of the players, not its share of the respondents.

A worked case, with invented numbers. A survey asks lapsed and active players whether they liked the new crafting system.

| Group | Share of players (telemetry) | Share of respondents | Satisfied within group |
|---|---|---|---|
| Active | 50% | 80% | 80% |
| Lapsed | 50% | 20% | 30% |

Raw result: `0.8 × 0.80 + 0.2 × 0.30 = 70%` satisfied. Weighted result: `0.5 × 0.80 + 0.5 × 0.30 = 55%` satisfied. The raw survey overstated satisfaction by 15 points because active players, who like the system more, answered four times as often.

Weighting has limits you should state in your report.

- It corrects only through the groups you weight on. If lapsed players who answered are happier than lapsed players who didn't, the weighted number is still too high.
- Small groups get large weights, which makes the result noisier. A group with 5 respondents standing in for 30% of players is a thin foundation.
- You need the true group shares, which is where telemetry comes in. Surveys and telemetry are partners here, not rivals.

## 4. Writing survey questions

A survey item is a measuring instrument, and a bad item measures the wrong thing precisely. Five common faults, with a fix for each.

| Fault | Bad item | Why it fails | Better item |
|---|---|---|---|
| Double-barrelled | "The combat was fun and fair." | Two questions, one answer. A player who found it fun but unfair can't answer. | Two items, one for fun and one for fairness. |
| Leading | "How much did you enjoy the new raid?" | Assumes enjoyment. | "How would you rate the new raid?" with a balanced scale. |
| Hypothetical | "Would you buy a season pass?" | People predict their future behaviour poorly. | Ask about past behaviour, or measure it in telemetry. |
| Jargon | "Was the TTK appropriate?" | Many players don't know the term, or read it differently. | "How long did enemies take to defeat?" (too short, about right, too long). |
| Vague frequency | "Do you often use the map?" | "Often" means different things to different people. And telemetry knows. | Drop it, or ask about a specific recent session. |

Most game surveys use **Likert-type items**: a statement and an ordered set of answers, such as "strongly disagree" to "strongly agree" on 5 or 7 points. Some practical rules for them:

- **Balance the scale.** As many positive as negative options, with a neutral middle unless you have a reason to force a choice.
- **Label every point, or at least the ends.** Players read unlabelled middles differently.
- **Watch for acquiescence.** Many respondents tend to agree with statements regardless of content. Mixing in **reverse-coded** items, statements where agreeing means the opposite, helps detect and reduce it.
- **Keep it short.** Completion falls as surveys grow, and the people who finish a long survey are a more selected group (section 2 again).
- **Pilot it.** Have three people answer it aloud and explain each answer. Misread items show up at once.

### Validated scales

A **validated scale** is a set of items that researchers have tested to show they measure a construct reliably and that the construct predicts what it should. Using one saves you from inventing items and lets you compare your results with published ones.

The best-known example in games is the **PENS** (Player Experience of Need Satisfaction), from this term's reading. Ryan, Rigby and Przybylski built it from Self-Determination Theory (week 4). In their first study, run with Super Mario 64, they measured in-game competence (5 items), in-game autonomy (5 items), presence (9 items across physical, emotional and narrative presence) and intuitive controls (3 items), all on 7-point Likert-type scales. The autonomy scale includes a reverse-coded item, where agreeing that you felt pressured counts against autonomy. The paper reports each scale's internal consistency (Cronbach's alpha): .79 for competence, .66 for autonomy and .85 for both presence and intuitive controls.

Alpha measures how well items in a scale agree with one another. Values around .7 or above are usually treated as acceptable for research. So the autonomy scale in that first study was weaker than the others, which the reader should keep in mind. Two lessons for your own work follow.

- **Several items per construct beat one.** A single item mixes the construct with the noise of its wording. Averaging several items cancels some of that noise, which is why validated scales ask similar things more than once.
- **Use a validated scale as published.** Changing its wording or dropping items breaks the validation. If you need a custom question, add it separately and report it as a single item.

## 5. Interviews

A **semi-structured interview** follows a written guide of open questions and planned follow-ups, and lets the interviewer depart from the guide when the player says something worth exploring. It is the default for game UX research because it balances comparability (everyone gets the same core questions) with discovery.

### Running one

- **Ask about specific, recent episodes.** "Tell me about the last time you died to the second boss" gets a story. "What do you think of the difficulty?" gets an opinion.
- **Ask open questions.** Start with how, what, tell me about. Avoid questions answerable with yes or no.
- **Don't lead, don't defend.** GD101 week 7's rule for playtests applies. You are not there to explain the design. If the player is wrong about how a system works, that is a finding.
- **Use silence.** After an answer, wait three or four seconds. Players often add the most useful part after a pause.
- **Probe.** "What did you expect to happen?", "What made you decide that?", "Can you show me?" If the game is in front of you, a short **retrospective think-aloud**, replaying a recording of their session and asking them to talk through it, anchors memory in what actually happened.
- **Record, with consent.** Get informed consent for recording and explain how the data will be stored and used. With minors, follow your institution's ethics rules and get guardian consent.

### How many interviews?

You can't compute a margin of error for interviews, but you can ask a different question. **If a fraction `p` of your players have a particular problem, how likely are you to hear about it at least once in `n` interviews?** That is MA102 week 3's complement rule:

```
P(heard at least once) = 1 − (1 − p)^n
```

| Share of players with the problem `p` | n = 3 | n = 5 | n = 8 | n = 12 | n = 24 |
|---|---|---|---|---|---|
| 10% | 27% | 41% | 57% | 72% | 92% |
| 20% | 49% | 67% | 83% | 93% | 99.5% |
| 30% | 66% | 83% | 94% | 99% | ~100% |

The table assumes you interview a random sample of the affected population and that anyone who has the problem mentions it, which is generous. Even so, 5 interviews give a 41% chance of hearing about a problem that one player in ten has. Twelve give 72%.

This matches what qualitative researchers find in practice. Guest, Bunce and Johnson (2006) coded 60 in-depth interviews with women in two West African countries, in order, and tracked when new codes stopped appearing. In their data, saturation came within the first 12 interviews, and the basic elements of the main themes were present after 6. That is one fairly homogeneous group on one topic, so treat 12 as a planning figure, not a law. Later work argues that a deeper understanding of each issue, sometimes called meaning saturation, takes more interviews. For a student project, 8 to 12 interviews per player group is a sensible plan. Stop early only if the last several interviews produced nothing new.

### From transcripts to themes

**Thematic analysis**, as described by Braun and Clarke (2006), gives a standard process in six phases.

1. Become familiar with the data. Read every transcript through.
2. Generate codes. Tag short segments with labels ("didn't see the crafting tab", "felt the boss was unfair").
3. Generate initial themes. Group codes into candidate patterns.
4. Review themes. Check each theme against the data. Split, merge or drop.
5. Define and name themes. Write one or two sentences saying what each theme is.
6. Produce the report. Use short quotes as evidence and count how many participants each theme came from.

Count participants, not mentions. One player who complained about the camera eight times is one participant. And don't turn counts from 10 interviews into percentages of your player base. That is the survey's job.

## In-class activity (25 minutes)

Groups of three.

1. **Fix the survey (10 min).** Your instructor hands out a 10-item post-playtest survey with at least five faults from section 4. Find them, name each fault, and rewrite each item.
2. **Estimate `k` (5 min).** The survey was shown at the end of each match to 2,000 players, and 300 answered. Telemetry says 40% of answers came from players who had just lost, while losses are 50% of matches. Estimate the response-rate ratio between players after a win and after a loss, and say which way it biases "the matchmaking feels fair."
3. **Interview guide (10 min).** Write a six-question semi-structured guide to find out why players stop playing after the tutorial. Include at least one question about a specific recent episode and two probes. Swap with another group and mark any leading or hypothetical questions.

Expected output: a corrected survey, one value of `k` with its direction of bias, and a peer-reviewed interview guide.

## Common misconceptions

- **"A big sample means a reliable result."** A big sample shrinks sampling error. It does nothing about who answered. The Literary Digest had 2.38 million answers and was wrong by a landslide.
- **"Players know what they want, so ask them."** Players are good at reporting experiences and poor at predicting their own behaviour or designing solutions. Ask what happened and how it felt; design the fix yourself.
- **"One good question is enough."** Single items are noisy. Validated scales use several items per construct for a reason.
- **"Interviews are too small to mean anything."** They are too small to estimate how common something is, and they are the best tool for finding what exists and why. Use them for that, and use surveys to count.

## Check yourself

1. A survey of 400 players finds 30% satisfied with matchmaking. Unhappy players were twice as likely to answer. Estimate the true satisfaction.
2. Rewrite this item and name its faults: "Don't you agree the new UI is faster and easier to use?"
3. You plan interviews to find problems in a new guild interface. You want at least an 80% chance of hearing about any problem that 15% of guild leaders have. How many guild leaders should you interview?
4. A PENS-style autonomy scale in your study has an alpha of .55. What does that tell you, and what would you do?

<details>
<summary>Answers</summary>

1. `k = 0.5`. `odds_obs = 0.3 / 0.7 = 0.429`. `odds_true = 0.429 / 0.5 = 0.857`. `p = 0.857 / 1.857 ≈ 46%`.
2. It is leading ("Don't you agree") and double-barrelled (faster, easier). Better: two items, "The new UI lets me do what I want quickly" and "The new UI is easy to use", each rated on a balanced 5- or 7-point agreement scale. Better still, measure speed with task timing (week 2) and ask only about ease.
3. Solve `1 − 0.85^n ≥ 0.80`. `0.85^n ≤ 0.20`, so `n ≥ ln 0.20 / ln 0.85 = 9.9`. Interview 10.
4. The items don't agree with one another well, so the averaged score is noisy, and it may be measuring more than one thing. Check whether you changed the published wording, look for an item that correlates poorly with the rest, and report the alpha alongside any result. Don't draw strong conclusions from that scale alone.

</details>

## Lab hook

[Lab 12, survey and interview study](../labs/lab12.md). You run a short survey and four interviews about one feature of a game your classmates play, estimate the response bias against a known group split, weight the result, and code the interviews into themes. Deliverable: the survey, the analysis sheet from the starter script, a theme table and a two-page memo.

## Sources

- Wikipedia, "Steam (service)" (accessed September 2026). User reviews from 2013; separate recent (last 30 days) and overall scores from May 2016; from September 2016, review scores discount reviews from key activations rather than Steam purchases; March 2019 announcement that off-topic reviews would be excluded from summary scores.
- Wikipedia, "Review bomb" (accessed September 2026). Steam histograms added in 2017; from 2019 all reviews in a detected off-topic period are excluded from the displayed rating; first applied to Borderlands titles in April 2019.
- Steamworks documentation, "User Reviews" (partner.steamgames.com, accessed September 2026). Only purchases made by the reviewing account count toward the review score.
- Wikipedia, "The Literary Digest" (accessed September 2026). 1936 poll: about 10 million ballots mailed, 2.38 million returned, predicted Landon 57.08%; sources were subscribers, car owners and telephone users; non-response bias identified as the primary contributor to the error; Gallup's poll of about 50,000 was close to the result.
- Ryan, R. M., Rigby, C. S. & Przybylski, A. (2006). "The Motivational Pull of Video Games: A Self-Determination Theory Approach." *Motivation and Emotion*, 30(4), 344-360. Study 1 with Super Mario 64; PENS subscales, item counts, 7-point Likert-type scale, alphas .79 (competence), .66 (autonomy), .85 (presence), .85 (intuitive controls).
- Yee, N. (2006). "Motivations of Play in MMORPGs: Results from a Factor Analytic Approach." Online survey; 3,200 respondents completed 39 items; 5-point importance scale.
- Guest, G., Bunce, A. & Johnson, L. (2006). "How Many Interviews Are Enough? An Experiment with Data Saturation and Variability." *Field Methods*, 18(1), 59-82. doi:10.1177/1525822X05279903. Abstract checked via Crossref (September 2026). Sixty interviews in two West African countries; saturation within the first 12 interviews; basic elements of metathemes by 6. The meaning-saturation point is from Wikipedia, "Thematic analysis" (accessed September 2026).
- Braun, V. & Clarke, V. (2006). "Using thematic analysis in psychology." *Qualitative Research in Psychology*, 3(2), 77-101. Six phases as listed in Wikipedia, "Thematic analysis."
- Wikipedia, "Binomial proportion confidence interval" (accessed September 2026), for the Wilson interval used in the numbers table.
- Hodent, C. (2017). *The Gamer's Brain*. CRC Press.
- The satisfaction values, response rates, crafting-system groups, in-game survey scenario and survey items are invented for teaching.

## Interactive spec: examples/w12-who-answers.html

**Purpose.** Show that sample size narrows a survey's interval while response bias moves it, so a large biased survey is confidently wrong.

**The one insight the visual must make obvious.** With `k = 0.5`, raising respondents from 100 to 10,000 shrinks the interval bar to a sliver that sits well away from the true-value line.

**Layout.** Two linked views side by side at 1280px, stacked at 390px. Controls below. Numbers panel under the controls.

- **Left, "What the survey reports".** A horizontal axis from 0% to 100%. The Wilson 95% interval for `p_obs` with the current respondent count, drawn as a thick bar with a dot at `p_obs`. No true-value line on this view. Caption shows "n = …, reported p = …, ± …".
- **Right, "What is true".** The same axis and the same bar, plus a vertical line at the true `p`, plus (when weighting is on) a second bar for the weighted estimate. Shade the gap between `p_obs` and true `p` and label it "bias: … points".
- Below both views, a small line chart of `p_obs` against `k` on a log axis from 0.2 to 5, with the true `p` as a horizontal line and the current `k` marked.

**Controls.**

- True satisfaction `p`: slider 5-95%, step 1, default 70.
- Response-rate ratio `k = r₁/r₀`: log slider 0.2 to 5, default 1. Show presets "unhappy 3× (0.33)", "unhappy 2× (0.5)", "equal (1)", "happy 2× (2)", "happy 3× (3)".
- Respondents `n`: log slider 20 to 20,000, default 100. Use `k_obs = round(n × p_obs)` satisfied answers for the interval.
- Toggle "Weight by known groups". When on, show the section 3 example: two groups (active, lapsed), with sliders for each group's share of players (default 50/50), share of respondents (default 80/20) and satisfaction within the group (defaults 80% and 30%). The right view then shows raw and weighted estimates side by side. In this mode the `k` slider is disabled.
- Reset.

**Formulas.**

- `odds_true = p/(1−p)`; `odds_obs = odds_true × k`; `p_obs = odds_obs/(1 + odds_obs)`.
- Wilson interval with `z = 1.96`, `p̂ = k_obs/n`: centre `(p̂ + z²/2n)/(1 + z²/n)`, half-width `z √(p̂(1−p̂)/n + z²/4n²)/(1 + z²/n)`.
- Weighted estimate: `Σ share_players_g × sat_g`. Raw: `Σ share_resp_g × sat_g`.

**Numbers panel.** `p`, `k`, `odds_true`, `odds_obs`, `p_obs`, bias in points, `n`, Wilson low and high, and whether the interval contains the true `p`.

**Test values.**

| p | k | p_obs |
|---|---|---|
| 0.70 | 1 | 0.700 |
| 0.70 | 0.5 | 0.5385 |
| 0.70 | 1/3 | 0.4375 |
| 0.70 | 2 | 0.8235 |
| 0.70 | 3 | 0.875 |
| 0.60 | 0.4 | 0.375 |

| Satisfied / n | Wilson low | Wilson high |
|---|---|---|
| 54 / 100 | 0.443 | 0.634 |
| 538 / 1000 | 0.507 | 0.569 |
| 5385 / 10000 | 0.529 | 0.548 |
| 70 / 100 | 0.604 | 0.781 |

- Weighting defaults: raw 70%, weighted 55%.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`, light and dark. True-value line differs from the interval by line style (dashed) as well as colour. All values printed as text. Controls keyboard operable with visible focus. Respect `prefers-reduced-motion`. No game art or logos.

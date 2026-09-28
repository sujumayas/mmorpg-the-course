# UX201 · Lab 12: Survey and interview study

Assigned in week 12 ([lecture](../lectures/w12-surveys-and-interviews.md)). Due at the start of week 13. Groups of three; each group submits one report.

## Objective

Run a small mixed-method study of one feature in a game that people around you play: a short survey to count, and interviews to explain. Estimate how unequal response rates bias the survey, correct for it where you can, and code the interviews into themes. The point is to practise the week 12 habit of asking "who answered?" before reading any number.

## Starter materials

Everything is in [`lab12-starter/`](lab12-starter/) and this file.

**1. `survey_analysis.py`.** A dependency-free Python script. It reads survey responses (one row per respondent, a `group` column and Likert items scored 1-7) and group sizes, flips reverse-coded items (names ending in `_r`), and prints per-group response rates and satisfaction, the raw share satisfied (scores 5-7) with its Wilson 95% interval, the weighted share, and the response-rate ratio between groups. It also prints how many interviews give an 80% chance of hearing a problem held by 10-30% of players.

**2. `responses.csv` and `population.csv`.** A synthetic data set built to match section 3 of the lecture: 200 respondents about an invented crafting system, 160 active and 40 lapsed, from a player base of 5,000 active and 5,000 lapsed. Three items: `crafting_satisfied`, `crafting_fair` and a reverse-coded `felt_pressured_r`. Run the script on it first. You should see raw 70.0% (Wilson 63.3% to 75.9%), weighted 55.0%, and a response-rate ratio of 4.00.

**3. Survey template** (adapt the wording to your feature; keep the structure).

- Screening: which game, how many hours in the last two weeks (0, 1-5, 6-20, more than 20), still playing (yes, no, taking a break).
- Four to six Likert items on a 7-point agreement scale, one construct each, at least one reverse-coded.
- One open question: "Tell us about the last time you used [feature]."
- No hypothetical questions ("Would you...?") and no double-barrelled items.

**4. Interview guide skeleton.**

1. Warm-up: how they started playing, what they play it for.
2. "Tell me about the last time you used [feature]." Probes: what were you trying to do, what happened, what did you expect.
3. "Was there a moment it annoyed or surprised you?" Probe: can you show me, or walk me through it.
4. "What do you do instead when you don't use it?"
5. Close: anything we should have asked.

**5. Theme table** (copy into your report).

| Theme (one-sentence definition) | Codes grouped under it | Participants (of N) | Short evidence quote (paraphrase if long) | Survey item it relates to |
|---|---|---|---|---|

## Steps

1. **Pick a feature and a question.** One feature in one game that at least 20 people you can reach play (a class channel, a club, a Discord server you are a member of). Write one research question, for example "Do players who stopped playing find the crafting system harder to use than those still playing?"
2. **Define the groups and their sizes.** Choose a split you can count independently of the survey, such as still playing versus stopped, or members of two class sections. Record the size of each group in the pool you invite. This is your `population.csv`.
3. **Pilot the survey** with two people who answer aloud. Fix any item they misread.
4. **Invite everyone in the pool in the same way** and record how many you invited from each group. Collect at least 20 responses. Get consent at the start of the survey and collect no names.
5. **Analyse.** Export to the `responses.csv` format and run `survey_analysis.py`. Report raw and weighted results and the response-rate ratio. Say which way you think the remaining bias runs, and why.
6. **Interview four people**, at least one from each group, for 15-20 minutes each, using the guide. Record with consent, and take notes if they decline.
7. **Code and theme.** Follow the six phases from the lecture. Count participants per theme.
8. **Combine.** For each theme, say whether the survey supports it, contradicts it, or says nothing. Use the starter's interview table to state how likely four interviews were to miss a problem held by 20% of players.

## Deliverable

A PDF with a memo of at most two pages plus appendices.

- The research question, the groups and the invitation method, with the response rate for each group.
- Raw and weighted results with the Wilson interval, the response-rate ratio, and a one-paragraph judgment of remaining bias.
- The theme table.
- Two or three findings that combine survey and interviews, each with one recommended design change.
- Appendices: the survey, the interview guide, anonymised responses CSV, script output, consent text.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Instrument design | Items single-barrelled, balanced, piloted; one reverse-coded; open question about a specific episode | Minor wording faults | Leading, hypothetical or double-barrelled items | 20% |
| Sampling and bias | Invitation counts per group, response rates, `k` computed, weighting done, remaining bias argued | Weighting done, bias discussion thin | Raw numbers only | 25% |
| Interviews | Four interviews, guide followed with probes, no leading, consent recorded | Fewer probes or some leading | Fewer than three interviews or no guide | 20% |
| Analysis and themes | Codes and themes traceable, participants counted, links to survey clear | Themes plausible, weak traceability | List of opinions | 25% |
| Writing | Numbers first, plain, within length | Readable, some padding | Hard to follow | 10% |

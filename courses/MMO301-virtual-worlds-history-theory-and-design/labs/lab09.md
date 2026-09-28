# MMO301 · Lab 09: A motivation survey study

**Assigned:** week 9 ([lecture](../lectures/w09-motivation-research-beyond-bartle-yee.md)). **Due:** start of week 10. **Feeds:** the player-type critique (20%), together with lab 08.

## Objective

Run a small motivation study from start to finish. Write your own survey items, collect answers, score components, apply a primary-motivation rule, and test the assumptions behind type models. You will end with evidence, from real respondents, for or against using player types in a design document, and a clear sense of what a sample of 20 can and cannot show.

## Starter materials

Everything is in this file.

**1. Item-writing rules.** Write 12 items, four for each of three components: Achievement, Social, Immersion (Yee's main components). Write them yourself. Do not copy items from Yee, the Bartle Test or any other published instrument.

- One idea per item. "I like to explore and collect things" is two items.
- Behaviour or preference, not identity. "I plan my progress several sessions ahead", not "I am an achiever".
- At least one item per component should be reverse-worded, for example "I would rather play alone than in a group" for Social. Reverse its score before averaging (`6 − answer` on a 1 to 5 scale).
- Five-point agreement scale, 1 strongly disagree to 5 strongly agree.

**2. Consent text (show before the first item).** "This is a class exercise on why people play online games. It takes about four minutes. Answers are anonymous and only used in a class report. You can stop at any time. Continuing means you agree."

**3. Scoring sheet layout.** One row per respondent, columns: `id`, twelve item answers, three component scores, `top`, `second`, `ratio = second / top`, `primary_c75`, `forced_label`.

- Component score `= (mean of its four items after reversal − 1) / 4`, which gives 0 to 1.
- `primary_c75` is the top component if `second < 0.75 × top`, else "none".
- `forced_label` is always the top component.
- If `top = 0`, write "none" for both labels.

**4. Test file.** Before collecting data, type these three rows (items already reversed where needed) and check your formulas.

| id | Achievement items | Social items | Immersion items | Expected scores (A, S, I) | Expected `primary_c75` |
|---|---|---|---|---|---|
| T1 | 5, 5, 4, 4 | 2, 2, 1, 3 | 2, 1, 2, 1 | 0.875, 0.25, 0.125 | Achievement |
| T2 | 4, 4, 4, 4 | 4, 4, 3, 4 | 1, 2, 1, 2 | 0.75, 0.6875, 0.125 | none |
| T3 | 3, 3, 3, 3 | 3, 3, 3, 4 | 3, 3, 3, 3 | 0.5, 0.5625, 0.5 | none |

## Steps

1. **Write items** following item 1. Get one classmate to read them and flag any item that holds two ideas. Revise.
2. **Pilot.** Take your own survey and time it. Enter the three test rows and confirm your scoring matches item 4.
3. **Collect at least 20 responses** from people who play online games. At least 10 must be from outside this course. Use any free form tool. Record no names or contact details.
4. **Score** every respondent. Report the mean and standard deviation of each component (MA102 week 12).
5. **Label.** Count `primary_c75` labels, including "none". Repeat with `c = 0.6` and `c = 0.9`. Compare each labelled share with the model value `c²` for three independent components.
6. **Test independence.** Compute the three correlations between components. Are any negative, as Bartle's graph predicts for achievement and social? How large is each compared with Yee's roughly 0.10?
7. **Forced versus measured.** Tabulate `forced_label`. Find the two respondents with the closest scores who received different forced labels, and the two with the most different scores who received the same one.
8. **Sample honesty.** Using MA102 week 13, estimate the margin of error on your unlabelled share (treat it as a proportion with your `n`). Say whether your result can distinguish your class from Yee's 43%.

## Deliverable

A PDF of at most five pages, the survey as sent (appendix), and the scoring spreadsheet.

- The 12 items with the component each measures and which are reversed.
- Component summary statistics and the three correlations.
- The labelled-share table for `c = 0.6, 0.75, 0.9`, beside the model values.
- The step 7 pairs, shown as rows.
- A 600-word critique of one type-based persona. Find a published or course-provided design persona built on a player type, or write one in the style studios use, and use your data and Yee's to say what it hides. End with a replacement that uses component scores.
- A limitations paragraph: sample, self-report, item wording, and the margin of error from step 8.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Survey design | 12 original single-idea items, reverse items present, consent shown | Minor wording problems | Copied or double-barreled items, no consent | 20% |
| Scoring and labels | Test rows match; labels correct at three values of `c`; compared with `c²` | Small scoring errors | Test rows do not match | 20% |
| Independence and forced labels | Correlations computed and compared with Yee; step 7 pairs chosen well and explained | Present but thinly explained | Missing | 20% |
| Persona critique | Uses own data and Yee's findings; replacement uses component scores | Critique present, weak use of data | Opinion only | 25% |
| Limitations and writing | Margin of error computed; limits named plainly; within length | Limits listed without numbers | No limitations section | 15% |

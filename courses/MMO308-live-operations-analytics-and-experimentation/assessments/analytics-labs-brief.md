# MMO308 · Analytics labs brief

**Weight:** 40% of the course grade.
**What counts:** all 14 labs are set. Labs 03, 05, 06 and 14 always count. Of the other ten, your best eight count. Two labs can be dropped.
**When:** each lab is assigned in its week's session and is due at the start of the next week's lab session, unless the lab says otherwise. Lab 14 is due at the start of week 15, before the live-ops plan is presented.
**Work mode:** as each lab states. Labs 04 to 13 are done in pairs. Labs 01, 02, 03 and 14 are individual.

## What this component is for

The labs turn each lecture model into code you ran and a number you measured on data. The week 3 lecture says an onboarding break hides inside a rising DAU line. Lab 03 hands you 284,000 rows of activity with three planted changes and makes you find the break, date it and size it before you read the answer. The course outcome "define and compute core live-game KPIs" is assessed mostly here, because it can only be shown with functions that pass a check and numbers that match the lecture's model.

Four labs cannot be dropped, because other assessments build on them or because they carry the course's two signature worked examples.

| Compulsory lab | Why it always counts |
|---|---|
| [03](../labs/lab03.md), the retention triangle | the signature example "spot the patch that broke onboarding"; the cohort table is reused in the live-ops plan |
| [05](../labs/lab05.md), design an experiment | its plan is the design half of the [A/B report](ab-report-brief.md) |
| [06](../labs/lab06.md), peeking and a broken split | the signature example "peeking inflates false positives"; its write-up is the analysis half of the A/B report |
| [14](../labs/lab14.md), sunset forecast | its memo is the end-of-life section of the [live-ops plan](live-ops-plan-brief.md) |

## The labs and how much each is worth

The component is marked out of 100 and then multiplied by 0.40.

| Lab | Week | Title | Work | Automatic check | Points |
|---|---|---|---|---|---|
| [01](../labs/lab01.md) | 1 | The layer cake | individual | `test_layercake.py` | 7.5 if in best 8 |
| [02](../labs/lab02.md) | 2 | Touches and play | individual | `test_kpis.py` | 7.5 if in best 8 |
| [03](../labs/lab03.md) | 3 | The retention triangle | individual | `test_retention.py` | **10, compulsory** |
| [04](../labs/lab04.md) | 4 | Funnels and churn from an event log | pair | `check_lab04.py` | 7.5 if in best 8 |
| [05](../labs/lab05.md) | 5 | Design an experiment for a shared world | pair | `check_lab05.py` | **10, compulsory** |
| [06](../labs/lab06.md) | 6 | Peeking, boundaries and a broken split | pair | `check_lab06.py` | **10, compulsory** |
| [07](../labs/lab07.md) | 7 | Segment the retention drop | pair | `test_segments.py` (7 tests) | 7.5 if in best 8 |
| [08](../labs/lab08.md) | 8 | Measure an event and plan a calendar | pair | `test_event_lift.py` (7 tests) | 7.5 if in best 8 |
| [09](../labs/lab09.md) | 9 | Rollout planner | pair | `test_rollout.py` (8 tests) | 7.5 if in best 8 |
| [10](../labs/lab10.md) | 10 | Who answered the survey? | pair | `test_lab10.py` (5 tests) | 7.5 if in best 8 |
| [11](../labs/lab11.md) | 11 | The poll archive | pair | `test_lab11.py` (5 tests) | 7.5 if in best 8 |
| [12](../labs/lab12.md) | 12 | Faucet alarms | pair | `test_lab12.py` (4 tests) | 7.5 if in best 8 |
| [13](../labs/lab13.md) | 13 | Incident analysis and a blameless postmortem | pair | `lab13-starter.py` (9 tests) | 7.5 if in best 8 |
| [14](../labs/lab14.md) | 14 | Sunset forecast and recommendation | individual | `lab14-starter.py` (8 tests) | **10, compulsory** |
| | | | | **Total** | **4 × 10 + 8 × 7.5 = 100** |

A compulsory lab is worth 4% of the course grade. Each of the eight best other labs is worth 3%. Dropping a lab removes its mark, not the knowledge. If you drop Lab 12, the live-ops plan still needs an alarm specification.

## How each lab is marked

Every lab has its own rubric, and that rubric decides the lab's mark out of 100. The lab mark is then scaled to the lab's points above. A lab marked 84 is worth `0.84 × 7.5 = 6.3` points, or `0.84 × 10 = 8.4` for a compulsory lab. The lab rubrics come in three formats, and each converts to 100 the same way every time.

| Labs | Rubric format | Conversion to a mark out of 100 |
|---|---|---|
| 01, 02, 03, 07, 08, 09, 10, 11, 12 | Weighted criteria, each scored in bands 0 to 4 | A criterion earns `weight × band ÷ 4`. A criterion weighted 25% and marked 3 earns 18.75. |
| 04, 05, 06 | Points out of 20, each criterion full, half or zero | Multiply the total by 5. |
| 13, 14 | Points out of 100, each criterion full, half or zero | Used as is. |

In the band labs, "Adequate (2-3)" means band 3 when one piece of evidence or explanation is missing and band 2 when the work is right in outline but thin. In the full, half or zero labs, a marker may give a quarter or three quarters of a criterion's points when the work sits clearly between two levels, and writes one line saying why.

### The common rubric behind every lab

The fourteen lab rubrics are specializations of one rubric. When a lab rubric is silent on something (a lab that runs but skips a step, a report in an unexpected format), or when a spot check leads to a re-mark, the marker uses this table.

| Criterion | What earns full marks | Points |
|---|---|---|
| Working code | The lab's automatic check passes on a clean copy with `.venv/bin/python`; the tests are unchanged; the code does what the lab asks and not only what the check tests | 25 |
| Model against data | Every measured number sits next to the lecture model's prediction, and gaps are explained in the model's own terms (for example `I × L`, `q / (q + h)`, `1 + (m − 1)ρ`, `τ × (1 − T)`, `R / (r/p + F)`) | 25 |
| The trap named | The lab's central misreading (MAU as players, a snapshot funnel as a cohort funnel, a peeked win, a mix shift as a regression, a spike as the lift, a raw survey as the truth) is shown with a number, not only described | 20 |
| Written recommendation | The memo, note, policy or specification makes a clear choice, uses at least three of your own numbers, and names what the choice costs | 25 |
| Reproducibility and honesty | Seeds, settings and the command that produced each number are stated; predictions written before results where the lab asks; help and AI assistance acknowledged in one line | 5 |
| **Total** | | **100** |

### Automatic checks

Markers run each lab's check on a clean copy of your folder with the course interpreter, `.venv/bin/python`. Code that only runs on your machine because of an absolute path or a missing file counts as failing. If the check fails, the code criterion of the lab rubric cannot score above band 1, or above half its points in the full, half or zero labs. Simulation checks in Labs 06, 09 and 13 accept a range, so any correct seeded implementation passes. Do not try seed after seed until one passes. Pick a seed before you run, and state it.

### Predictions and hidden answers

Several labs ask you to commit before you look.

- Lab 03 step 3 asks for your guesses from the pictures before you compute, and the `SECRET` block in `gen_cohorts.py` stays closed until step 6.
- Lab 06 keeps `gen_experiment.py` closed until step 5.
- Lab 10 step 1 asks you to predict the direction of the survey bias, and `stuck_accounts.txt` stays closed until step 6.
- Lab 12's `make_faucet.py` stays closed until you submit.

A prediction written after the run, or edited to match it, earns the lowest band for the criterion it belongs to. A wrong prediction with honest working loses nothing, as long as you then explain the difference with the model. Answers that match a hidden file you were told not to open, with no path from the data to the answer, are treated as unexplained work (see spot checks).

## Pairs

In pair labs both partners submit the same folder and receive the same mark, plus a two-line contribution statement signed by both. Swap the keyboard at least once per step. If a spot check shows one partner cannot explain the work, that partner's mark is re-marked alone, as described below.

## Spot checks

In each lab session from week 2 on, a marker picks a few students and asks two short questions about their previous lab, in the style of the [exam bank](exam-bank.md), rewritten with the student's own data and code. Typical questions are "Your D7 series steps at install day 20. Point to the cells in your triangle that show it is a cohort effect and not an outage" or "Your weighted approval is 60.8% with `n_eff` 1,248. Which respondents carry most of the weight, and why?"

A spot check never lowers a mark for a slip. It exists to confirm the work is yours. If you cannot explain your own code at all, the lab is re-marked after a 10-minute conversation with the instructor, using this table.

| Result | Share of the lab mark kept | What the student shows |
|---|---|---|
| Full | 100% | Explains each function they wrote, traces one input through it, and says why the lab's key number came out as it did |
| Partial | 70% | Explains the main function and the key number, but cannot answer a "what if the cohorts were half as big" change |
| Weak | 40% | Recognizes the code and can run it, but cannot say what it does or where a number came from |
| None | 0% | Cannot explain the submitted work |

## Late work

- A droppable lab submitted up to 48 hours late is marked out of 80. After 48 hours it is marked for feedback only and counts as 0, which usually makes it one of your two drops.
- A compulsory lab (03, 05, 06 or 14) is accepted up to 7 days late and marked out of 50, because later assessments need it. After 7 days it is marked for feedback only and counts as 0. Talk to the instructor before the deadline if one of these is at risk.
- Extensions for illness or other documented reasons follow the university policy and do not use up a drop.
- Lab 14 cannot be late past the live-ops plan deadline, because the plan ships its end-of-life section.

## Data and ethics rules

- Generated or published data only. Every lab builds its data from a fixed seed or ships a public file (the Steam averages in Lab 01, the OSRS poll archive in Lab 11). Do not load real player data, scraped account data or another student's output into a lab.
- The OSRS poll archive comes from the Old School RuneScape Wiki under CC BY-NC-SA 3.0. Credit the wiki if you publish anything built on it.
- Do not commit generated files. Submit the code that makes them and the seed.

## Academic integrity

You may use any code from the lectures and starter files. You may use documentation, forums and AI assistants to understand an error or an API, and you must say so in one line in the lab report ("used the Python docs for `random.binomialvariate`; asked an assistant why my CUSUM never reset"). You may not submit code you cannot explain, and you may not copy another pair's measurements. A table of simulated rates or fitted parameters must come from runs you did yourself, with the seed and settings recorded. The spot checks are designed around these rules.

# MMO405 · Lab 07: Recording rules and a field observation

**Week:** 7 ([Ethnography and participant observation](../lectures/w07-ethnography-and-participant-observation.md))
**Time:** 2 hours in lab, plus a 60-minute field session and about 2 hours of write-up at home
**Counts toward:** methods labs (30%); the recording plan and reflexive paragraph are reused in the methods section of your proposal (20%)
**Work:** code and analysis in pairs; the field session and notes individually

## Objective

You will implement the three recording rules from the lecture (continuous, instantaneous scan, one-zero), run them on a supplied focal-observation log, and test when the one-zero bias factor `1 + T/b` predicts what you observe and when it breaks. Then you will plan and carry out one hour of open-role observation in a public space of an MMO, using a scan rule and open field notes together, and write a reflexive methods paragraph about it.

## Starter materials

All in [`lab07-starter/`](lab07-starter/README.md). Python 3.10 or later, standard library only.

- `gen_focal.py` writes `focal_log.csv` from seed 707. It holds six focal characters observed for 180 minutes each in a city hub, with one row per bout of "in conversation".
- `recording.py` holds six functions to write: `continuous_share`, `scan_share`, `scan_average`, `one_zero_share`, `one_zero_expected` and `bias_factor`. Each docstring gives the exact rule. `main()` prints a comparison table once they work.
- `check_lab07.py` prints PASS, FAIL or TODO per function, plus one check on the generated log.
- `recording-plan-template.md` and `fieldnotes-template.md`, which you fill in for part B.

```
python gen_focal.py
python recording.py
python check_lab07.py
```

## Steps

### Part A, in lab (pairs)

1. **Implement the rules (30 min).** Write the six functions until `check_lab07.py` passes. Reproduce the lecture's evening (`T = 5` and `T = 15`) in a scratch script and confirm your numbers match the lecture's table.
2. **Run the log (15 min).** Run `recording.py`. Copy the table into `RESULTS.md`. For each focal character, compare the observed one-zero bias (`obs x`) with the predicted factor (`pred x`).
3. **Find where the formula breaks (20 min).** For at least two characters the formula overshoots badly. Explain why, using the assumption stated in the lecture. Check it directly by counting, for one of those characters, how many 15-minute blocks contain more than one bout.
4. **Interval sweep (15 min).** For character C6, compute the scan average and the one-zero score for every `T` from 1 to 30. Plot or tabulate both against `T` with the true share. In two sentences, say what a reader should conclude from a one-zero "time in conversation" figure reported without its interval.
5. **Choose rules for a question (10 min).** For each of these, name the recording rule you would use and why: (a) the share of an evening a raid spends waiting; (b) how many loot disputes happen per raid night; (c) whether anyone mentioned a new patch during each hour of a stream.

### Part B, field session (individual)

6. **Plan (before you log in).** Fill in `recording-plan-template.md`. Your site must be a public space, such as a city hub, a public event or an open-world zone. Your role must be open. Add a short note to your character's profile or bio if the game allows one, saying you are a student observing public spaces for a course. Get the instructor's sign-off on item 9 before the session.
7. **Observe (60 min).** Choose one focal character at random from those in view at the start. Scan every 2 minutes for your focal behaviour and log all occurrences of the events you listed. Keep jottings throughout. Do not start conversations for research purposes, do not join private channels, and do not record names. If your focal character leaves, pick the next one by the same rule and note the switch.
8. **Write up (same day).** Expand your jottings into field notes. Write two events thin and thick. Compute the scan estimate for your focal behaviour and, from your jottings, the one-zero score you would have got with 10-minute blocks. Report both.
9. **Reflexive paragraph.** In 200 to 250 words, write the paragraph your proposal's methods section would contain. Give your role, what you told whom, your recording rules, where your own presence or play habits may have shaped what you saw, and what your structured and open records could and could not support.

## Deliverable

One folder per pair named `lab07-<name1>-<name2>` containing `recording.py` (passing `check_lab07.py`) and `RESULTS.md` with steps 2 to 5. Each student adds a subfolder with their signed recording plan, field notes and the reflexive paragraph. Screenshots are not required. If you include any, blur every name and chat line.

## Rubric (20 points)

| Criterion | Excellent (full) | Adequate (half) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Code passes the checker | All seven checks PASS | Five or six PASS | Four or fewer | 4 |
| Formula check (steps 2 and 3) | Observed and predicted factors compared for all six; breakdown explained by shared blocks, with a direct block count | Comparison made, explanation vague | Missing | 4 |
| Interval sweep and rule choice (steps 4 and 5) | Sweep shown; conclusion about unreported intervals is specific; each rule choice matches the question | Sweep or choices incomplete | Missing | 4 |
| Field plan and notes (steps 6 to 8) | Plan signed before the session; scan table complete; thin and thick versions clearly different; both estimates reported | Notes present but plan late or scan table patchy | Missing, or names recorded | 4 |
| Reflexive paragraph (step 9) | Role, disclosure, rules and limits all stated; names a specific way the observer shaped the data | Generic reflection | Missing | 4 |

Any submission that records real character names, quotes chat verbatim, or observes a non-public space without approval scores 0 for the field components.

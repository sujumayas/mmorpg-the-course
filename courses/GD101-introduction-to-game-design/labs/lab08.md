# GD101 · Lab 08: Two-loop iteration sprint

Assigned in week 8 ([lecture](../lectures/w08-iteration-loops-and-kill-your-darlings.md)). Due at the start of week 9. This is playtest report 2 of 3. Your iteration log carries forward to the final paper prototype.

## Objective

Run two complete, short iteration loops on your paper prototype, each with written kill criteria set before testing, and make an honest keep, change or kill decision at the end of each. You will also measure your own loop length and use it to plan the rest of the semester.

## Starter materials

Everything below is included in this file.

- Your lab 07 findings list. If you missed lab 07, first run two silent sessions with the lab 07 protocol and build a short findings list from them before starting loop 1.
- The week 8 interactive, [the iteration clock](../examples/w08-iteration-clock.html), for the planning step (the formulas in lecture section 2 give the same numbers).

**Iteration log template (one entry per loop).**

| Field | Entry |
|---|---|
| Loop number and dates (start, decision) | |
| Question this loop answers | |
| Change from last version, and the finding that motivated it | |
| Kill criteria (written and dated before testing) | Keep if ... / Change if ... / Kill if ... |
| Testers (count, profile) | |
| Result (findings with counts, k of n) | |
| Decision and reason | |
| Hours spent: build / test / analyse | |

**Kill criteria checklist.** Each criterion must be (1) observable in a silent playtest, (2) a count, "k of n testers," (3) written before the test, and (4) include a limit on change loops ("kill after two change loops without meeting keep").

**Sunk cost check.** Before each decision, answer in one sentence: "If we had built this feature in ten minutes, would we keep it given these results?" If the answer differs from your decision, explain why in the log.

## Steps

1. **Choose the target.** From your lab 07 list, pick the highest-ranked finding that your team can address in under three hours of prototype changes.
2. **Loop 1: plan.** Write the question, the change, and the kill criteria in the log. Get a timestamp on them (a dated message to your lab instructor or a commit to your team's shared folder counts).
3. **Loop 1: build and test.** Make the change on paper. Run silent sessions with at least three new testers using the lab 07 protocol. Keep observation logs.
4. **Loop 1: decide.** Compare results against the criteria, fill in the decision, and complete the sunk cost check.
5. **Loop 2.** Repeat steps 2 to 4 with the next question. It can continue the same feature (a change decision) or move to a new finding (after keep or kill). Use at least two testers who did not see loop 1.
6. **Measure your loop.** Record the calendar time and hours of each loop. Compute your average loop length `c` in days.
7. **Plan the semester.** With the days left until the week 15 showcase as `T`, compute how many loops fit, and the chance of at least one keeper for hit rates of 0.1 and 0.2. Then propose one concrete way to cut your loop length in half, and recompute.

## Deliverable

A PDF of at most four pages plus raw logs as an appendix.

- The two completed iteration log entries.
- One photo of the prototype before loop 1 and after loop 2, with changes marked.
- The loop-length measurement and the semester plan from step 7, with working.
- A short paragraph: which of your decisions was hardest, and did the sunk cost check change anything?

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Kill criteria | Observable, count-based, timestamped before testing, with a limit on change loops | Present but vague or partly unobservable | Written after testing or missing | 25% |
| Loop execution | Two complete loops, new testers each loop, lab 07 protocol followed | Two loops with shortcuts (reused testers, thin logs) | Fewer than two loops | 25% |
| Decisions | Each decision follows from criteria and evidence; sunk cost check done honestly | Decisions plausible but loosely tied to criteria | Decisions contradict evidence or ignore criteria | 20% |
| Loop measurement and plan | Correct loop length, correct loop count and probabilities, credible plan to shorten the loop | Minor errors | Missing or wrong | 20% |
| Writing | Clear, numbers first, at most four pages | Readable but padded | Hard to follow | 10% |

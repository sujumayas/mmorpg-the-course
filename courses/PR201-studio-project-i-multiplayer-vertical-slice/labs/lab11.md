# PR201 Lab 11: Playtest evidence table and count checks

**Week:** 11 (Playtest and telemetry review). **Guide:** [week 11](../lectures/w11-playtest-and-telemetry-review.md). **Team lab**, submitted once per team.

## Objective

Turn your alpha playtest into a table of decisions that the data can actually support. You will check your telemetry counts, compute a Wilson interval for every rate at its correct unit, compare it with a threshold you set in advance, and produce a ranked sprint 4 input list. The checker script tells you whether every verdict follows from its numbers.

## Starter materials

In [`labs/lab11-starter/`](lab11-starter/):

- `check_evidence.py`. Standard library only. Run it with `.venv/bin/python check_evidence.py evidence.csv counts.csv`. It prints the Wilson interval and the model's verdict for every row, then `PASS` or `NOT READY`, and exits with code 1 when anything is missing or inconsistent.
- `evidence.csv`. Four example rows from the week 11 guide with the verdicts left blank and one rule missing. Replace them with your own rows when you have done the warm-up.
- `counts.csv`. The four count checks from section 4 of the guide, with values left blank.

Rule format: `above:0.05` means "act if the rate is above 5%". `below:0.70` means "act if the rate is below 70%". Verdicts are `act`, `leave` or `cant_decide`.

## Steps

1. **Warm-up (15 minutes).** Fill in the blank verdicts in the starter `evidence.csv` and give row E3 the rule `above:0.70` (the boss is too hard if more than 70% of parties wipe). Fill `cluster_note` for every `act` row. Run the checker until E1 to E4 pass. Your verdicts should match the guide's table.
2. **Thresholds.** Copy the questions and thresholds from your week 10 alpha plan into a new `evidence.csv`. If a question had no threshold, write one now and add "set after data" to the question text. Honesty is marked; a late threshold is not.
3. **Count checks.** Run the four checks from guide section 4 against your raw export and enter both numbers for each in `counts.csv`. Any mismatch needs a note that explains it or names the fix.
4. **Evidence rows.** Add at least six rows. At least one must be a party-level or session-level outcome with `n` equal to the number of parties or sessions. For every `act` row, check which sessions the events came from and say so in `cluster_note`.
5. **Clustering row.** For at least one event that could depend on a session (disconnects, desyncs, server errors), add a second row for the same event at the session level. Compare the two verdicts.
6. **Run the checker** until it prints `PASS`.
7. **Sprint 4 input list.** Write `input-list.md` with one line per finding: the finding in UX201 week 14 form, its evidence (row IDs and observation note references), its type (bug, design change, polish item, needs a targeted test) and its size. Rank the list using the lower end of each interval. File every bug in your tracker and paste the ticket IDs.

## Deliverable

In `production/week11/` in the team repository:

- `evidence.csv` and `counts.csv` that pass `check_evidence.py`, with the checker output saved as `check-output.txt`.
- `input-list.md`, ranked, with ticket IDs for every bug.

**Checkable output:** the instructor reruns `check_evidence.py` on your two CSV files. It must print `PASS` and exit with code 0.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun, output file matches |
| Units | 4 | Every row has the right unit; party outcomes use parties as `n`; at least one session-level row |
| Thresholds | 3 | Set before the playtest, or honestly marked as set after |
| Count checks | 3 | All four run on real data; every mismatch explained |
| Clustering | 2 | Every `act` row says where its events came from; the session-level comparison is discussed in one or two sentences |
| Input list | 4 | Ranked by the stated rule; every line traceable to evidence; bugs have ticket IDs; "needs a targeted test" items have an owner and a date |

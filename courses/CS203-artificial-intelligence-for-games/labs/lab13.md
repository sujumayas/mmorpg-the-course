# CS203 · Lab 13: Encounter scripts and skip thresholds

**Week:** 13 ([Boss AI and scripted encounters](../lectures/w13-boss-ai-and-scripted-encounters.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually; swap bosses with a neighbor in step 7

## Objective

Build a small encounter runner that reads a boss from data and produces every cast of every ability for a given group DPS, under HP gates, time gates and a guarded hybrid. Check it against the Warden from the lecture, then use it to design a boss whose signature mechanics survive across the DPS range your players will actually have. By the end you should be able to hand a designer a table that says "at this DPS, this rule shows the group these casts, and this is what the guarantee costs in fight length."

## Starter materials

- Python 3.10 or later, standard library only. In this repository, `.venv/bin/python`.
- [`lab13-starter/encounter.py`](lab13-starter/encounter.py). It holds two bosses as data, `WARDEN` (the lecture's boss) and `FOUNDRY` (two phases, two abilities each, two signature abilities), a helper `counts()` and a `table()` printer. You write four functions: `phase_windows()`, `cast_times()`, `run()` and `skip_threshold()`. All times are `fractions.Fraction`, so thresholds land exactly and there are no floating-point edge cases. Run `python encounter.py` to print comparison tables for both bosses; cells for unwritten functions show a dash.
- [`lab13-starter/test_encounter.py`](lab13-starter/test_encounter.py). Run `python test_encounter.py` from inside the starter folder. It prints PASS or FAIL for seven checks and exits with status 1 until all pass. On the untouched starter all seven fail.
- The interactive [`examples/w13-phase-gates.html`](../examples/w13-phase-gates.html), to spot-check timelines by eye.

## Steps

### Part A: the runner (60 minutes)

1. Write `phase_windows(enc, dps, mode)`. For `"hp"`, each phase lasts `phase_hp / dps` and starts where the previous one ended. For `"time"`, phases start at the running sum of `seconds`, and the last phase has end `None`. For `"guard"`, start from the HP rule, then push the end of any phase with a signature ability out to at least `start + first + resolve`. Check by hand that the Warden's guarded windows at 6,000 DPS are `(0, 40)`, `(40, 85)`, `(85, 115)` before running the tests.
2. Write `cast_times(start, end, first, period, stop)`. Every cast must be strictly before the phase end and strictly before `stop`. The strict inequalities are what make the skip threshold exact. Run the tests until step 2 passes.
3. Write `run(enc, dps, mode)`. Work out the kill time (`kill_time()` in the hp and time modes, the end of the last window in guard mode), cut everything at `min(kill, enrage)`, collect `(time, phase, ability)` for every cast, and sort by time. Break ties by phase order, then by ability order in the data. The two step 3 checks compare your counts with the lecture's table and test the enrage at 1,600 DPS.
4. Write `skip_threshold(enc, phase_name, ability_name)` as `phase_hp / first`. The step 4 check also confirms that the Warden's Meteor fires once at 4,499 DPS and never at 4,500.
5. Run the full test file. The two step 5 checks test guard mode on the Warden and your runner on the Foundry Twins. When all seven pass, run `python encounter.py` and paste both tables into your report.

### Part B: measure (30 minutes)

6. For the Warden, sweep DPS from 1,500 to 8,000 in steps of 100 in all three modes. Plot or tabulate, for each mode, the total number of casts and the fight length against DPS. Mark the enrage floor and every skip threshold on the plot. Answer in two or three sentences each:
   - Between which DPS values does each mode show the group the fewest casts?
   - Guard mode keeps one Meteor for every group. How many seconds does that add to the fight at 4,600 and at 8,000 DPS, and what fraction of the group's damage is wasted while the boss is held at 30%?

### Part C: design (at home)

7. Copy `WARDEN` into a new boss of your own with three phases and at least one signature ability per phase. Your players will deal between 1,500 and 3,500 DPS over the life of the content. Constraints:
   - Every group in that range beats the enrage, with the weakest finishing between 300 and 360 s.
   - No signature ability has a skip threshold inside the range under the rule you pick for each transition. You may mix HP gates, time gates and guards.
   - At no DPS in the range do two signature casts from different phases land less than 6 s apart. Add a small function that checks this from `run()`'s event list.
   Swap bosses with a neighbor. Try to find a DPS in the range that breaks one of their constraints, and report what you found.
8. Write a tuning note of at most 300 words for the encounter designer. State the rule you chose for each transition and why, list the skip thresholds and the enrage floor, name the DPS in the range that shows the fewest mechanics and how many it shows, and describe one thing your design gives up compared with pure HP gates.

## Deliverable

Your completed `encounter.py` with your boss added, and `test_encounter.py` passing (paste its output). Also a PDF with the two tables from step 5, the step 6 plot and answers, your boss table and constraint checks from step 7 (including your neighbor's finding), and the tuning note.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Correct runner (30%) | All seven checks pass; code reads the data generically with no boss names hard-wired; strict inequalities explained in a comment | All checks pass, code hard to follow | Hp and time modes correct, guard or enrage fails | Runner missing or counts wrong |
| DPS sweep (20%) | All three modes plotted with thresholds and enrage marked; both questions answered with numbers from the sweep | Plot present, one answer vague | Only one or two modes | Missing |
| Boss design (25%) | All three constraints met and shown by code; neighbor's attack reported; gate choice per transition justified | Constraints met, justification thin | One constraint fails and is acknowledged | Missing |
| Tuning note (25%) | Every requested number present; clear trade-off stated against pure HP gates; readable by a designer without the code | Numbers present, trade-off vague | Few numbers | Missing |

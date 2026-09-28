# DB201 · SQL labs brief

**Weight:** 40% of the course grade.
**What counts:** all 14 labs are set. Labs 05, 06, 13 and 14 always count. Of the other ten, your best eight count. Two labs can be dropped.
**When:** each lab is assigned in its week's session and is due at the start of the next week's lab session, unless the lab says otherwise. Lab 14 is due at the start of week 15, before the final service demo.
**Work mode:** individual, except Lab 03 and Lab 14, which are done in pairs, and the incident note in Lab 06 step 12, which you write with a partner.

## What this component is for

The labs turn each lecture model into code you ran and a number you measured. The week 6 lecture says a naive trade handler dupes in 18 of 20 interleavings. Lab 06 makes you run all 20 against a real database, watch the stale copy appear, and then write three handlers that make it impossible. The course outcome "model game entities relationally and query them with SQL" is assessed mostly here, and so is most of "use transactions to prevent item duplication", because both can only be shown with queries and handlers that pass a check.

Four labs build parts that the [final service](final-service-brief.md) reuses directly, so they cannot be dropped.

| Compulsory lab | What the final service takes from it |
|---|---|
| [05](../labs/lab05.md), transactions | the trade as one transaction, and the persistence policy per game action |
| [06](../labs/lab06.md), the dupe | the conditional, locked and versioned trade handlers, and the stress harness |
| [13](../labs/lab13.md), retention and erasure | the erasure path and the retention schedule |
| [14](../labs/lab14.md), disaster recovery | the backup script, the verification check and the restore runbook |

## The labs and how much each is worth

The component is marked out of 100 and then multiplied by 0.40.

| Lab | Week | Title | Work | Automatic check | Points |
|---|---|---|---|---|---|
| [01](../labs/lab01.md) | 1 | Save intervals and a crash-proof save | individual | `save_sim.py --check` | 7.5 if in best 8 |
| [02](../labs/lab02.md) | 2 | An inventory schema that enforces the rules | individual | `check_schema.py` (12 tests) | 7.5 if in best 8 |
| [03](../labs/lab03.md) | 3 | Eight questions about a generated world | pair | `run_queries.py` (8 queries) | 7.5 if in best 8 |
| [04](../labs/lab04.md) | 4 | Scans, indexes and query plans | individual | none; the printed plans are the evidence | 7.5 if in best 8 |
| [05](../labs/lab05.md) | 5 | Split saves, real crashes and commit cost | individual | `acid_lab.py` output and your `audit` | **10, compulsory** |
| [06](../labs/lab06.md) | 6 | Reproduce the dupe, then make it impossible | individual, pair note | `dupe_lab.py` (0 of 20, and `--stress 2000`) | **10, compulsory** |
| [07](../labs/lab07.md) | 7 | Ranks at scale | individual | `rank_lab.py --check` | 7.5 if in best 8 |
| [08](../labs/lab08.md) | 8 | The write-behind flusher | individual | `writebehind_lab.py --check` | 7.5 if in best 8 |
| [09](../labs/lab09.md) | 9 | A migration under load | individual | `migration_lab.py --check` | 7.5 if in best 8 |
| [10](../labs/lab10.md) | 10 | Tracking plan and event validator | individual | `validate_events.py` ("plan OK") | 7.5 if in best 8 |
| [11](../labs/lab11.md) | 11 | A telemetry pipeline in SQLite | individual | `check_lab11.py` | 7.5 if in best 8 |
| [12](../labs/lab12.md) | 12 | KPIs in SQL | individual | `check_lab12.py` (7 queries) | 7.5 if in best 8 |
| [13](../labs/lab13.md) | 13 | Retention and erasure | individual | `privacy_lab.py --check` | **10, compulsory** |
| [14](../labs/lab14.md) | 14 | Disaster-recovery drill | pair | `dr_drill.py --check` | **10, compulsory** |
| | | | | **Total** | **4 × 10 + 8 × 7.5 = 100** |

A compulsory lab is worth 4% of the course grade. Each of the eight best other labs is worth 3%. Dropping a lab removes its mark, not the work. If you drop Lab 08, you still need a write-behind flusher in the final service.

## How each lab is marked

Every lab has its own rubric, and that rubric decides the lab's mark out of 100. The lab mark is then scaled to the lab's points above (a lab marked 84 is worth `0.84 × 7.5 = 6.3` points, or `0.84 × 10 = 8.4` for a compulsory lab).

Labs 01 to 12 use weighted criteria scored in bands from 0 to 4. A criterion earns `weight × band ÷ 4`. A criterion weighted 25% and marked 3 earns 18.75 points.

| Band | Label in the lab rubric | Share of the criterion's weight | What the marker sees |
|---|---|---|---|
| 4 | Excellent | 100% | Everything the Excellent cell asks for, with numbers that match the check or the lecture's model |
| 3 | Good, or Adequate (strong) | 75% | Correct, with one piece of evidence or explanation missing |
| 2 | Partial, or Adequate (weak) | 50% | Works in outline, explanations thin or one number off |
| 1 | Missing or wrong, attempted | 25% | Attempted, but fails the check or reasons from the wrong model |
| 0 | Missing | 0% | Not submitted, or unrelated to the lab |

Labs 13 and 14 list points per criterion with three levels. Excellent earns the full points, Adequate earns half, and Missing earns zero. A marker may give a quarter or three quarters of a criterion's points when the work sits clearly between two levels, and writes one line saying why.

### The common rubric behind every lab

The fourteen lab rubrics are specializations of one rubric. When a lab rubric is silent on something (a lab that runs but ignores a step, a report in an unexpected format), or when a spot check leads to a re-mark, the marker uses this table.

| Criterion | What earns full marks | Points |
|---|---|---|
| Working code or queries | The lab's automatic check passes on a clean copy with `.venv/bin/python`; the harness and tests are unchanged; the code does what the lab asks and not only what the check tests | 30 |
| Model against measurement | Every measured number sits next to the lecture model's prediction; gaps are explained with the model's own terms (for example `b / r`, `m₁ × m₂`, `1 − e^(−uT)`) | 25 |
| Reasoning in the lecture's terms | Explanations name the mechanism (grain, selectivity, stale copy, dirty set, commit point, watermark) and would convince a teammate who missed the lecture | 20 |
| Written recommendation | The memo, policy, plan or runbook makes a clear choice, uses at least three of your own numbers, and names what the choice costs | 20 |
| Reproducibility and honesty | Seeds, settings and machine stated; predictions written before results where the lab asks; help and AI assistance acknowledged in one line | 5 |
| **Total** | | **100** |

### Automatic checks

Markers run each lab's check on a clean copy of your folder with the course interpreter, `.venv/bin/python`. Code that only runs on your machine because of an absolute path or a missing file counts as failing. If the check fails, the code criterion of the lab rubric (usually the first row) cannot score above band 1, or above half its points in Labs 13 and 14. Lab 04 has no check script, so its plan lines and timings are the evidence. Lab 06 is checked twice, with the 20-interleaving table and with `--stress 2000`. One dupe in 2,000 attempts means the fix is wrong.

### Predictions before results

Several labs ask you to predict before you run: Lab 06 step 4 (dupe rates for new `work_ms` values), Lab 09 step 1 (the worst wait during the one-statement backfill), Lab 11 step 5 (scan time for 1,000 players) and Lab 13 Part A (row counts and rows examined). A prediction written after the run, or edited to match it, earns the lowest band for that criterion. A wrong prediction with honest working loses nothing, as long as you then explain the difference with the model.

## Pairs

In Labs 03 and 14 both partners submit the same files and receive the same mark, plus a two-line contribution statement signed by both. Lab 03 asks you to swap the keyboard every query. If a spot check shows one partner cannot explain the work, that partner's mark is re-marked alone, as described below. The Lab 06 incident note is written with a partner, and each partner submits it with their own lab.

## Spot checks

In each lab session from week 2 on, a marker picks a few students and asks two short questions about their previous lab, in the style of the [exam bank](exam-bank.md), rewritten with the student's own schema, queries and numbers. Typical questions are "Your q06 naive join reported 240 times the true warrior gold. Which two match counts multiply to give that, for one character?" or "Point to the line in your `versioned_trade` that makes trade 2 give nothing in `121122`, and say what happens if you delete it."

A spot check never lowers a mark for a slip. It exists to confirm the work is yours. If you cannot explain your own code at all, the lab is re-marked after a 10-minute conversation with the instructor, using this table.

| Result | Share of the lab mark kept | What the student shows |
|---|---|---|
| Full | 100% | Explains each function or query they wrote, traces one input through it, and says why the lab's key number came out as it did |
| Partial | 70% | Explains the main function and the key number, but cannot answer a "what if the table were ten times bigger" change |
| Weak | 40% | Recognizes the code and can run it, but cannot say what it does or where a number came from |
| None | 0% | Cannot explain the submitted work |

## Late work

- A droppable lab submitted up to 48 hours late is marked out of 80. After 48 hours it is marked for feedback only and counts as 0, which usually makes it one of your two drops.
- A compulsory lab (05, 06, 13 or 14) is accepted up to 7 days late, marked out of 50, because the final service needs it. After 7 days it is marked for feedback only and counts as 0. Talk to the instructor before the deadline if one of these is at risk.
- Extensions for illness or other documented reasons follow the university policy and do not use up a drop.
- Lab 14 cannot be late past the final service deadline, because the service ships its backup script and runbook.

## Data and safety rules

- Generated data only. Every lab builds its own world from a fixed seed. Do not load real player data, scraped data or another student's database into a lab.
- Do not commit generated files (`events.ndjson` in Lab 11 is about 135 MB). Submit the code that makes them and the seed.
- Destructive steps (Lab 05's `os._exit`, Lab 13's `DROP TABLE`, Lab 14's disaster) run against files in a temporary folder. Never point them at a database you care about.

## Academic integrity

You may use any code from the lectures and starter files. You may use documentation, forums and AI assistants to understand an error or an API, and you must say so in one line in the lab report ("used the SQLite docs for `INSERT OR IGNORE`; asked an assistant why `BEGIN IMMEDIATE` raised"). You may not submit code you cannot explain, and you may not copy measurements. A timing table or a stress-test rate must come from runs you did yourself, with the seed and settings recorded. The spot checks are designed around these rules.

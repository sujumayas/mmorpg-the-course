# CS202 · Labs brief

**Weight:** 40% of the course grade.
**What counts:** 13 labs. Lab 09 covers weeks 8 and 9 and counts twice, so there are 14 lab slots. Your best 12 slots count, and labs 02, 09, 13 and 14 always count.
**When:** each lab is assigned in its week's session and is due before the next lecture, unless the lab says otherwise. Lab 07 is due before week 8, Lab 09 before week 10, and Lab 14 before the final prototype review. Week 8 has no separate lab. You start Lab 09 that week.

## What this component is for

The labs turn each lecture model into Python you can run and a number you measured. A lecture says a lost packet costs TCP `4Δ + RTT`. The lab makes you write the simulator, reproduce the table and then point the tool at your own network. The course outcome "explain latency, jitter, packet loss and bandwidth effects on gameplay" is assessed mostly here, because it can only be shown with numbers you produced.

Four labs also build tools the [final prototype](final-prototype-brief.md) reuses. Lab 02's ping and analysis give your latency report. Lab 09's prediction and reconciliation are the core of your client. Lab 13's budget model gives your bandwidth report, and Lab 14's conditioner and test matrix give your bad-network report. That is why those four cannot be dropped.

## The labs

| Lab | Week | Title | Slots | Feeds the final prototype | Can be dropped? |
|---|---|---|---|---|---|
| [01](../labs/lab01.md) | 1 | Sockets and the cost of order | 1 | transport choice, framing | yes |
| [02](../labs/lab02.md) | 2 | Measure your own connection | 1 | latency report (ping, `analyze.py`) | **no** |
| [03](../labs/lab03.md) | 3 | The topology calculator | 1 | topology decision | yes |
| [04](../labs/lab04.md) | 4 | Policing movement | 1 | server validation, tick budget | yes |
| [05](../labs/lab05.md) | 5 | 108 bits | 1 | packet format, fuzzed reader | yes |
| [06](../labs/lab06.md) | 6 | Acks and copies | 1 | acks, input redundancy | yes |
| [07](../labs/lab07.md) | 7 | A snapshot codec | 1 | snapshots and deltas | yes |
| [09](../labs/lab09.md) | 8 and 9 | Prediction and reconciliation | 2 | client prediction and reconciliation | **no** |
| [10](../labs/lab10.md) | 10 | The interpolation buffer | 1 | remote players | yes |
| [11](../labs/lab11.md) | 11 | Rewind hit detection | 1 | lag compensation | yes |
| [12](../labs/lab12.md) | 12 | Lockstep timing and the desync hunt | 1 | seeded replay, checksums | yes |
| [13](../labs/lab13.md) | 13 | Bandwidth budget | 1 | bandwidth report | **no** |
| [14](../labs/lab14.md) | 14 | Break it on purpose | 1 | bad-network test report | **no** |

All labs are individual. You may talk through ideas with anyone, but the code and the report you submit must be your own. If you drop a lab whose work the prototype needs (Lab 10 or Lab 11, for example), you still need that code for the prototype. Dropping a lab removes its mark, not the work.

## How each lab is marked

Every lab has a rubric with four to six criteria. Each criterion has a weight and is scored in bands from 0 to 4. Excellent is 4, Adequate is 2 or 3, and Missing or wrong is 0 or 1. A criterion earns `weight × band ÷ 4`, so a criterion weighted 25% and marked 3 earns 18.75 points. The lab's mark is the sum, out of 100.

| Band | Label in the lab rubric | Share of the criterion's weight | What the marker sees |
|---|---|---|---|
| 4 | Excellent | 100% | Everything the Excellent cell asks for, with numbers that match the lecture or the check |
| 3 | Adequate, strong | 75% | Correct, one piece of evidence or explanation missing |
| 2 | Adequate, weak | 50% | Works in outline, explanations thin or a number off |
| 1 | Missing or wrong, partial | 25% | Attempted, but fails the check or reasons from the wrong model |
| 0 | Missing or wrong | 0% | Not submitted, or unrelated to the lab |

Your labs component is the mean of the 12 slots that count, multiplied by 0.40. A single lab is worth about 3.3% of the course, and Lab 09 about 6.7%.

### Automatic checks

Most labs have a `--check` mode (`hol_sim.py --table`, `analyze.py --check`, `topology.py --check`, `movement_check.py --check`, `bitpack.py --check`, `reliability.py --check`, `snapcodec.py --check`, `netsim.py --check`, `interp_lab.py --check`, `rewind.py --check`, `lockstep.py --check`, `budget.py --check`, and `conditioner.py`). Markers run it on a clean copy of your folder with the course interpreter, `.venv/bin/python`. The code criterion (usually the first row of the rubric) cannot score above band 1 if the check fails there. Code that only runs on your machine because of an absolute path or a missing file is treated as failing.

### Predictions before results

Many labs ask you to predict a number before you run the code (Lab 02 steps 3 and 4, Lab 07 step 1, Lab 13 step 1, Lab 14 step 2). A prediction written after the run, or changed to match it, earns the lowest band for that criterion. A wrong prediction with honest working does not lose marks, as long as you then explain the difference.

## Spot checks

In each lab session from week 2 on, a marker picks a few students and asks two short questions about their previous lab, in the style of the [exam bank](exam-bank.md), rewritten with the student's own code and numbers. Typical questions are "Your log had a P95 of 23 ms above the minimum. What `B` does that give for a 5% target, and what does it cost in felt latency?" or "Point to the line in `on_snapshot` that drops acknowledged inputs, and say what the client does if you delete it."

A spot check never lowers a mark for a slip. It exists to confirm the work is yours. If you cannot explain your own code at all, the lab is re-marked after a 10-minute conversation with the instructor, using this rubric.

| Band | Points kept from the lab mark | What the student shows |
|---|---|---|
| Full | 100 | Explains each function they wrote, traces one input through it, and says why the lab's key number came out as it did |
| Partial | 70 | Explains the main function and the key number, but cannot trace a second function or answer a "what if the RTT doubled" change |
| Weak | 40 | Recognizes the code and can run it, but cannot say what it does or where a number came from |
| None | 0 | Cannot explain the submitted work |

## Late work

A lab submitted up to 48 hours late is marked out of 80. After 48 hours it is marked for feedback only and counts as 0, which usually makes it one of your two dropped slots. Labs 02, 09, 13 and 14 cannot be dropped, so talk to the instructor before the deadline if one of them is at risk. Extensions for illness or other documented reasons follow the university policy and do not use up a drop.

## Network rules for lab work

Several labs send real packets. Run servers on `127.0.0.1` unless a step tells you to use the lab network. Only point Lab 02's ping, Lab 14's conditioner or netem at machines you own or a classmate's machine with their agreement. Always remove a netem rule when you finish (`sudo tc qdisc del dev lo root`), and say in your report which directions a conditioner setting applied to.

## Academic integrity

You may use any code from the lectures and starter files. You may use documentation, forums and AI assistants to understand an error or an API, and you must say so in one line in the lab report ("used the Python docs for `struct.unpack_from`; asked an assistant why `recvfrom` blocked"). You may not submit code you cannot explain, and you may not copy measurements. A latency log or a test-matrix table must come from runs you did yourself, with the seeds and settings recorded. The spot checks are designed around these rules.

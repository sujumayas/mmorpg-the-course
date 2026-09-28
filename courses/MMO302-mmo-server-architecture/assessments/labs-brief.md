# MMO302 · Labs brief

**Weight:** 40% of the course grade.
**What counts:** 14 labs, one per lecture week. Labs 03, 08, 11 and 14 always count. Of the other ten, your best eight count. The rubric at the end of this brief shows how the 12 counted labs add up to 100.
**When:** each lab is assigned in its week's session and is due before the next lecture, unless the lab says otherwise. Lab 13 is due at the start of week 14 and Lab 14 at the start of week 15.
**Work mode:** labs 01 to 06 are individual. Labs 07 to 12 are done in pairs, as each lab says. Labs 13 and 14 are individual.

## What this component is for

Each lecture gives you a model: `D = u × Σ g(g − 1)` for crowds, `(2/π) ρ v L` for handoffs, `c = a + d·n + e·n·k` for a tick, `C / L` for a login queue, `1 / (μ − λ)` for a knee. The labs make you turn each model into code, reproduce the lecture's numbers from your own code, then point the code at something the lecture did not cover, such as your own machine, a messier population or a crash you inject on purpose.

The labs assess the three course outcomes piece by piece.

- "Design a server topology for a target concurrency" is assessed in labs 01, 02, 04, 05, 12 and 13, which each end with a plan backed by numbers.
- "Implement area-of-interest management" is assessed in lab 03, which is why it cannot be dropped.
- "Build a persistent, authoritative world server with safe item transactions" is assessed in labs 06 to 10, and then in the [final server](final-server-brief.md).

Four labs also produce parts that later assessments reuse. Lab 03's grid is the interest manager in your final server. Lab 08's transfer and audit become its item service. Lab 11's open-loop fleet drives the [week 15 load test](load-test-brief.md), and lab 14's histogram and stall alert produce the per-zone numbers that report needs. That is why those four always count.

## The labs

| Lab | Week | Title | Mode | Reused in | Can be dropped? |
|---|---|---|---|---|---|
| [01](../labs/lab01.md) | 1 | The crowd cost model | individual | capacity plan in the final design document | yes |
| [02](../labs/lab02.md) | 2 | Layer assignment | individual | layering policy (optional in the final server) | yes |
| [03](../labs/lab03.md) | 3 | Build interest management | individual | the final server's AOI | **no** |
| [04](../labs/lab04.md) | 4 | Zone handoff simulator | individual | the final server's handoff protocol | yes |
| [05](../labs/lab05.md) | 5 | Tick budget profiler | individual | tick-rate choice, load-test prediction | yes |
| [06](../labs/lab06.md) | 6 | Movement validators | individual | the final server's movement check | yes |
| [07](../labs/lab07.md) | 7 | Persistence strategies under crash | pairs | the final server's event log | yes |
| [08](../labs/lab08.md) | 8 | A dupe-proof item service | pairs | the final server's item service and audit | **no** |
| [09](../labs/lab09.md) | 9 | Login queue and session tickets | pairs | the final server's login path | yes |
| [10](../labs/lab10.md) | 10 | Chat router under load | pairs | the final server's chat | yes |
| [11](../labs/lab11.md) | 11 | Ramp test with an open-loop bot fleet | pairs | the week 15 load test | **no** |
| [12](../labs/lab12.md) | 12 | A time-dilation governor | pairs | overrun policy (optional in the final server) | yes |
| [13](../labs/lab13.md) | 13 | An autoscaler for a zone-server fleet | individual | the deployment section of the final design document | yes |
| [14](../labs/lab14.md) | 14 | Tick telemetry and a stall alert | individual | the week 15 load-test report | **no** |

Dropping a lab removes its mark, not the work. If you drop lab 09 you still need a login path for the final server.

## How each lab is marked

Every lab ends with its own rubric, and that rubric decides the lab's mark out of 100. The labs use two formats, and both come out of 100.

- **Labs 01 to 06** score each criterion in bands. Excellent is 4, Adequate is 2 or 3, Missing or wrong is 0 or 1. A criterion earns `weight × band ÷ 4`. A criterion weighted 25% and marked 3 earns 18.75 points.
- **Labs 07 to 14** give full, half or zero marks per criterion, with the points or weight shown in the lab.

| Band (labs 01 to 06) | Share of the criterion | What the marker sees |
|---|---|---|
| 4 | 100% | Everything the Excellent cell asks for, with numbers that match the lecture or the tests |
| 3 | 75% | Correct, with one piece of evidence or explanation missing |
| 2 | 50% | Works in outline, explanation thin or one number off |
| 1 | 25% | Attempted, but fails the tests or reasons from the wrong model |
| 0 | 0% | Not submitted, or unrelated to the lab |

### Tests first

Every lab ships with a test file that fails on the starter and passes on a correct solution. Markers run it on a clean copy of your folder with the course interpreter, `.venv/bin/python`. The code criterion (usually the first row of the lab rubric) cannot score above band 1, or above zero in the full-or-half labs, if the tests fail on the marker's machine. Code that only runs on your machine because of an absolute path or a missing file counts as failing.

### Predictions before results

Several labs ask you to predict a number before you run the code: lab 08 step 2 (drift), lab 11 step 13 (the new knee), lab 13 step 3 (servers at minute 1). A prediction written after the run, or changed to match it, earns nothing for that criterion. A wrong prediction with honest working loses nothing, as long as you then explain the difference with the lecture's model.

### Numbers from your own machine

Labs 01, 03, 05 and 11 measure timings on your hardware. Your numbers will differ from the lecture's and from your classmates'. State the CPU model, the core count, and whether anything else was running (the bots, a browser, a video call). Markers check that your numbers are consistent with each other and with the model, not that they match a reference.

## Spot checks

In each lab session from week 2 on, a marker picks a few students and asks two short questions about their previous lab, in the style of the [exam bank](exam-bank.md), rewritten with the student's own code and numbers. Typical questions are "Your fit gave `e = 0.31` µs. What `T_max` does that give for the siege?" or "Point to the line in `transfer_gold` that makes a retry safe, and say what happens if the client makes a new operation ID for each retry."

A spot check never lowers a mark for a slip. It confirms the work is yours. If you cannot explain your own code at all, the lab is re-marked after a 10-minute conversation with the instructor.

| Result | Share of the lab mark kept | What the student shows |
|---|---|---|
| Full | 100% | Explains each function they wrote, traces one input through it, and says why the lab's key number came out as it did |
| Partial | 70% | Explains the main function and the key number, but cannot trace a second function or answer a "what if `L` doubled" change |
| Weak | 40% | Recognizes the code and can run it, but cannot say where a number came from |
| None | 0% | Cannot explain the submitted work |

In pair labs, either partner may be asked about any part of the lab.

## Late work

A lab submitted up to 48 hours late is marked out of 80. After 48 hours it is marked for feedback only and counts as 0, which usually makes it one of your two dropped labs. Labs 03, 08, 11 and 14 cannot be dropped, so talk to the instructor before the deadline if one of them is at risk. Extensions for illness or other documented reasons follow the university policy and do not use up a drop.

## Academic integrity

You may use any code from the lectures and starter files. You may use documentation, forums and AI assistants to understand an error or an API, and you must say so in one line in the lab report ("used the Python docs for `sqlite3` isolation levels; asked an assistant why `BEGIN` failed"). You may not submit code you cannot explain, and you may not copy measurements. A timing table, a ramp test or a crash run must come from runs you did yourself, with the seeds and settings recorded. In pair labs, add one line saying who wrote which function.

## Rubric: how the labs make up this component

Each lab is first marked out of 100 with its own rubric. The component mark out of 100 is then built from the 12 labs that count.

| Part of the component | Labs | Weight of each lab | Points |
|---|---|---|---|
| Labs that always count | 03, 08, 11, 14 | 10 | 40 |
| Best eight of the other ten | 01, 02, 04, 05, 06, 07, 09, 10, 12, 13 | 7.5 | 60 |
| **Total** | 12 labs | | **100** |

A lab marked 80 out of 100 in the "always count" group adds `0.80 × 10 = 8` points. Your component mark is multiplied by 0.40 for the course grade, so each always-counted lab is worth 4% of the course and each of the best-eight labs 3%.

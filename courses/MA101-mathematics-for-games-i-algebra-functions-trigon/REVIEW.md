# MA101 review notes (course-reviewer, 2026-09-28)

These are the open items the reviewer did not fix directly. The small fixes are already applied in the files.

| File | Problem | Proposed fix |
|---|---|---|
| lectures/w11, w13, w14 | These link the CS203, MMO302 and MA201 syllabi, because those courses have no lectures yet. | Upgrade the links to the target lectures once CS203 w10/w12, MMO302 w03 and MA201 w11 exist. |
| lectures/w01, w10 (title lines) | The titles use Title Case ("Functions as Machines: ...", "Angles, Radians, Sin and Cos: ..."), while the other weeks use sentence case. | Align with curriculum.yaml when the orchestrator finishes the syllabus. |
| tools/check_examples.py | `page.goto` waits for Google Fonts and times out offline (it hung at w04). With external requests blocked, all 14 examples pass. | Add `page.route("http*://**", lambda r: r.abort())` or `wait_until="domcontentloaded"` to the tool. |
| assessments/exam-bank.md | Broken link to `midterm-and-final-brief.md`. The briefs are not written yet. | Owned by the assessments agent. |
| labs/starter/ | Starter data (path.csv, mobs.csv, chase.csv, stick_log.csv) is generated. Reference answers: lab13 first-seen times sentry_a 10.3 s, sentry_b 7.8 s, patrol_c 16.4 s, tower_d 1.8 s; the 30° meter never fills (max 0.63), 45° spots at 11.9 s. Lab14 zones safe 576 / random 1,530 / despawn 2,894; box keeps 163; int32 overflow wrongs 1,070 from 463.5 blocks; chase state changes 3 (two radii) vs 9 (one radius). | Copy these into the grading key when the assessments agent writes it. |

## Fact sweep (2026-09-29)

No open real-world fact items. The lectures, labs and assessments have no "(verify" markers. Verified 0, hedged 0, removed 0.

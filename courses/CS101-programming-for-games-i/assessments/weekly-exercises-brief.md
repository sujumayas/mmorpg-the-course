# CS101 · Weekly exercises brief

**Weight:** 40% of the course grade.
**Work mode:** individual submission. You may sit with a partner in the lab, talk through ideas and swap laptops where a lab sheet tells you to, but the code, the log and the numbers you hand in are your own.

## What counts

The weekly exercises are the 14 labs. Each lab has its own sheet with an objective, starter files, steps, a deliverable and a rubric. Your **best 12 of 14** lab scores count, at equal weight, so each counted lab is worth `40 / 12 = 3.33%` of the course grade. The two dropped labs cover illness, a bad week or a lab you started late. You do not need to apply for them.

| Lab | Week | Topic | Automated check you must reach | Feeds |
|---|---|---|---|---|
| [Lab 01](../labs/lab01.md) | 1 | State of a text adventure | `4/4 parts pass` | |
| [Lab 02](../labs/lab02.md) | 2 | A cave with a way out | `3/3 parts pass` | |
| [Lab 03](../labs/lab03.md) | 3 | Loop it | `4/4 parts pass` | Mini-game 1 (turn structure) |
| [Lab 04](../labs/lab04.md) | 4 | Refactoring the combat turn | `7/7 tests passed` | Lab 05 |
| [Lab 05](../labs/lab05.md) | 5 | A stacking inventory | `8/8 tests passed` | Lab 06 |
| [Lab 06](../labs/lab06.md) | 6 | The item database | `7/7 tests passed` | Final (data files) |
| [Lab 07](../labs/lab07.md) | 7 | A scene tree you can test | `10/10 tests passed` | Mini-game 1 |
| [Lab 08](../labs/lab08.md) | 8 | Input you can trust | `10/10 tests passed` | Mini-game 1 (jump) |
| [Lab 09](../labs/lab09.md) | 9 | One game, every frame rate | `9/9 tests passed` | Mini-game 1 (30 and 144 fps check) |
| [Lab 10](../labs/lab10.md) | 10 | Collision toolkit | `8/8 tests passed` | Mini-game 2 (collision) |
| [Lab 11](../labs/lab11.md) | 11 | The game-flow machine | `10/10 tests passed` | Mini-game 2 (menu and pause) |
| [Lab 12](../labs/lab12.md) | 12 | Bug hunt | `7/7 tests passed` | Final (bug journal) |
| [Lab 13](../labs/lab13.md) | 13 | Seeded randomizers and a fair spawner | `9/9 tests passed` | Final (spawner, run seed) |
| [Lab 14](../labs/lab14.md) | 14 | Headless juice | `8/8 tests passed` | Final (shake, particles, polish table) |

A lab's grade and the mini-game or final that reuses its code are marked separately. You earn the lab mark for the lab, and the later project mark for how well the code works inside a game.

## How a lab is scored

Each lab rubric scores every criterion on 0 to 4 and gives it a weight. The lab score out of 100 is

```
lab score = sum over criteria of (points / 4) × weight
```

For example, lab 01 with 4/4 on the checker (40%), 3 on types (15%), 4 on predictions (20%), 2 on the log (15%) and 3 on readability (10%) scores `40 + 11.25 + 20 + 7.5 + 7.5 = 86.25`.

Your weekly exercises mark is the mean of your best 12 lab scores. Your tutor reruns the checker or the test file on your submitted code. The number that counts is the one the tutor sees, not a pasted screenshot.

## Deliverables and milestones

| When | What |
|---|---|
| Each week, in the 2-hour lab | Work through the lab sheet with a tutor in the room. The first 10 minutes are a short quiz drawn from the [exam bank](exam-bank.md) for the week just taught. The quiz is feedback only. |
| Start of the next week's lab | Submit the week's lab: the edited starter files and the note, log or journal the sheet asks for, zipped, on the course page. |
| Weeks 4, 8 and 12 | Checkpoint. Your tutor returns your running mean and flags any lab whose tests still fail, so you can fix it before the dropped-lab rule has to cover it. |
| Start of week 15 | Lab 14 is due. It is the last lab, and its outputs go into your final release. |

Labs 07, 08, 09, 11, 13 and 14 have Godot steps. Hand in the Godot evidence each deliverable names, such as a log excerpt, a screenshot or a short recording.

## Rules that protect the tests

- **Do not edit checker or test files.** They are the specification. A submission whose test file differs from the starter gets 0 on that lab's "tests pass" criterion.
- **Write predictions before you run.** Several labs (01, 03, 05, 07, 09, 10, 13, 14) ask you to predict a number first. Write the prediction in your log with the arithmetic, then run the code and write the result next to it. A wrong prediction with honest working scores better than a right one written afterwards.
- **Keep the given names and outputs.** Checkers read exact function names and printed lines, such as the `STATUS` line in lab 01.
- **Late work.** Up to three days late loses 10 points per day from the lab score. After three days the lab scores 0 but still gets feedback, and it counts as one of your two dropped labs if you have any left.

## Rubric (every lab, out of 100)

The lab sheet's own rubric is the detailed marking guide. This table shows what each band looks like across all 14 labs, so you know what an 80 means before you start.

| Criterion (typical weight) | Excellent | Good | Weak | Missing |
|---|---|---|---|---|
| **Tests and checker** (30 to 40) | 30 to 40: every provided test or checker part passes when the tutor reruns it | 20 to 29: all but one or two pass | 8 to 19: about half pass | 0 to 7: few or none pass, or test files were edited |
| **Predictions and measurements** (15 to 25) | 20 to 25: predictions written before running, with working, and compared with measured values; any gap is explained with the lecture's model | 13 to 19: predictions and measurements present, comparison thin | 5 to 12: measured values only, or predictions clearly written afterwards | 0 to 4: missing |
| **Explanations** (15 to 25) | 20 to 25: each explanation names the mechanism and a number from your own output (for example "lost remainder of 0.4 frames per cooldown") | 13 to 19: right idea, no numbers | 5 to 12: vague or partly wrong | 0 to 4: missing |
| **Engine or integration step** (0 to 30, where the lab has one) | 25 to 30: the Godot or cross-lab step works and the evidence the sheet asks for is included | 15 to 24: works with one visible gap, or evidence incomplete | 5 to 14: attempted, does not work | 0 to 4: not attempted |
| **Code quality** (10) | 9 to 10: clear names, docstrings kept, no global game state, no leftover debug prints | 6 to 8: minor clutter | 3 to 5: hard to follow | 0 to 2: unreadable or does not run |

Weights differ by lab. Lab 01 has no engine step, so its tests and predictions carry more. Lab 11 gives 30% to the Godot port. Always read the sheet's own table.

## Getting help

Bring a failing test to the lab, not a finished-looking file. Your tutor will ask you the week 12 questions first. Can you reproduce it? What is the smallest case? What did you observe? A lab that you could not finish, with an honest log of what you tried and where you got stuck, earns marks on the predictions and explanation rows even when the tests fail.

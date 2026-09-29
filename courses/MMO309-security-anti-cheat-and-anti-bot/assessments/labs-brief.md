# MMO309 · Labs brief

**Weight:** 30% of the course grade.
**What counts:** 11 labs. Your best 9 count, and Labs 01, 03, 08 and 12 always count.
**When:** each lab is assigned in its week's session and is due at the start of the next week's lecture, unless the lab sheet says otherwise. Lab 01 is due before the week 3 lecture, because its Part D uses the week 2 model.

## What this component is for

The labs turn each lecture model into Python you can run and a decision you can defend. A lecture says that a rate check turns every forgiven lag spike into free speed. The lab makes you write both checks, reproduce the table, and then tune a ban threshold on a log of 10,000 players. The course outcomes "prevent classes of exploits by server design" and "detect bots with behavioral analytics" are assessed mostly here, because both can only be shown with code that works and numbers you produced.

Four labs build pieces the other components reuse. Lab 01 is the first draft of your [threat model](threat-model-brief.md). Lab 03's detector, Lab 08's triage policy and Lab 12's sanction ladder are the starting points for the [final prototype](final-prototype-brief.md) and the threat model's section 9. That is why those four cannot be dropped.

## The labs

| Lab | Week | Title | Checker | Feeds | Can be dropped? |
|---|---|---|---|---|---|
| [01](../labs/lab01.md) | 1 | The threat ledger | `threat_ledger.py --check` | threat model draft | **no** |
| [03](../labs/lab03.md) | 3 | The lag-tolerant movement validator | `movement_validator.py --check` | prototype (movement track) | **no** |
| [04](../labs/lab04.md) | 4 | The mailbox under fire | `check_lab04.py` | value-path inventory | yes |
| [06](../labs/lab06.md) | 6 | The bot farm ledger | `check_lab06.py` | bot economics section | yes |
| [07](../labs/lab07.md) | 7 | Behavioral features for bot detection | `check_lab07.py` | prototype (bot track) | yes |
| [08](../labs/lab08.md) | 8 | From detector scores to decisions | `check_lab08.py` | prototype decision policy | **no** |
| [10](../labs/lab10.md) | 10 | Follow the gold | `test_lab10.py` | prototype (RMT track) | yes |
| [11](../labs/lab11.md) | 11 | Dupe response: rollback, trace or ban | `test_lab11.py` | incident response section | yes |
| [12](../labs/lab12.md) | 12 | A sanction policy with an error budget | `test_lab12.py` | sanction ladder | **no** |
| [13](../labs/lab13.md) | 13 | Pricing a bounty table | `test_bounty.py` | disclosure section | yes |
| [14](../labs/lab14.md) | 14 | Response scorecard | `test_scorecard.py` | case lesson, optional appendix | yes |

Weeks 2, 5 and 9 have no lab. Their lecture hooks ask you to add rows to your Lab 01 ledger instead, and that work is marked in the threat model.

Labs 01 and 03 are done in pairs. The other labs are individual. You may talk through ideas with anyone, but the code and the report you submit must be your own. If you drop a lab whose code your prototype needs (Lab 07 or Lab 10, for example), you still need that code. Dropping a lab removes its mark, not the work.

## How each lab is marked

Each lab sheet has its own rubric, and that rubric is the one used. Labs 01 and 03 award points directly (full, half or zero per criterion, out of 100). The other labs use weighted criteria scored in bands from 0 to 4. A criterion earns `weight × band ÷ 4`, so a criterion weighted 25% and marked 3 earns 18.75 points. Every lab's mark is out of 100.

| Band | Label in the lab rubric | Share of the criterion's weight | What the marker sees |
|---|---|---|---|
| 4 | Excellent | 100% | Everything the Excellent cell asks for, with numbers that match the lecture or the checker |
| 3 | Adequate, strong | 75% | Correct, one piece of evidence or explanation missing |
| 2 | Adequate, weak | 50% | Works in outline, explanations thin or a number off |
| 1 | Weak, partial | 25% | Attempted, but fails the check or reasons from the wrong model |
| 0 | Weak or missing | 0% | Not submitted, or unrelated to the lab |

Your labs component is the mean of the 9 labs that count, multiplied by 0.30. One lab is worth about 3.3% of the course.

### Default rubric

If a lab sheet is revised during the term and its rubric is missing or unclear, the marker uses this one, scored in the bands above. It also shows what every lab rubric in this course rewards.

| Criterion | Weight | Excellent (band 4) |
|---|---|---|
| Correctness | 30 | The checker passes on a clean copy with `.venv/bin/python`, without edits to the checker or the seeded generator |
| Lecture numbers reproduced | 20 | The lab's link to the lecture (a table, a hand check or a closed form) matches, with the hand working shown where asked |
| Analysis | 25 | Every "explain" and "compare" step answered with a number from your own run and the right model |
| Written deliverable | 15 | Memo or note within its length, numbers first, readable by the named audience (producer, live-ops lead, community manager) |
| Code quality | 10 | Readable, runs first time, no absolute paths, starter code and your code clearly separated |
| **Total** | **100** | |

### Automatic checks

Every lab has a checker or a `--check` mode, listed in the table above. Markers run it on a clean copy of your folder with the course interpreter, `.venv/bin/python`, from inside the starter folder. The correctness criterion cannot score above band 1 if the check fails there. Code that only runs on your machine because of an absolute path or a missing file is treated as failing. Never edit a checker or a seeded generator to make a check pass. Several labs say so, and a marker compares both against the originals.

### Predictions before results

Several labs ask you to predict or work by hand before you run the code (Lab 04 step 1, Lab 06 step 2, Lab 07 step 1, Lab 08 step 1, Lab 10 step 1). A prediction written after the run, or changed to match it, earns the lowest band for that criterion. A wrong prediction with honest working does not lose marks, as long as you then explain the difference.

## Spot checks

In each lab session from week 3 on, a marker picks a few students and asks two short questions about their previous lab, in the style of the [exam bank](exam-bank.md), rewritten with the student's own code and numbers. Typical questions are "Your best 7-day `k` at `L = 250` was 12. What happens to precision if you drop it to 10, and why?" or "Point to the line in `send_mail` that makes a retry safe, and say what happens if you delete it."

A spot check never lowers a mark for a slip. It exists to confirm the work is yours. If you cannot explain your own code at all, the lab is re-marked after a 10-minute conversation with the instructor.

| Result | Share of the lab mark kept | What the student shows |
|---|---|---|
| Full | 100% | Explains each function they wrote, traces one input through it, and says why the lab's key number came out as it did |
| Partial | 70% | Explains the main function and the key number, but cannot trace a second function or answer a "what if the base rate halved" change |
| Weak | 40% | Recognizes the code and can run it, but cannot say what it does or where a number came from |
| None | 0% | Cannot explain the submitted work |

## Late work

A lab submitted up to 48 hours late is marked out of 80. After 48 hours it is marked for feedback only and counts as 0, which usually makes it one of your two dropped labs. Labs 01, 03, 08 and 12 cannot be dropped, so talk to the instructor before the deadline if one of them is at risk. Extensions for illness or other documented reasons follow the university policy and do not use up a drop. The same rules apply to the milestones of the threat model and the final prototype.

## Safety rules for lab work

This is a defensive course. Every lab runs on starter code and seeded synthetic data in this repository.

- Run all lab code locally. None of it needs the network.
- Steps that ask you to "attack your own code" (Lab 04 step 7, Lab 07 step 6) or to stress a detector mean changes to the lab's own simulator, data or handlers. They never mean trying anything against a real game, a real service or another person's account, including your own game accounts.
- Do not bring real player data into a lab, including logs from a game you play or run, unless the instructor has approved it and it is anonymized.
- If you believe you have found a vulnerability in a real game while studying, stop, report it through that studio's published disclosure channel (week 13), and tell the instructor. Do not include it in a lab report.

Breaking these rules is a conduct matter under university policy, whatever the lab mark.

## Academic integrity

You may use any code from the lectures and starter files. You may use documentation, forums and AI assistants to understand an error or an API, and you must say so in one line in the lab report ("used the Python docs for `sqlite3` isolation levels; asked an assistant why `rowcount` was −1"). You may not submit code you cannot explain, and you may not copy measurements. A precision table or a seed summary must come from runs you did yourself, with the seeds and settings recorded. The spot checks are designed around these rules.

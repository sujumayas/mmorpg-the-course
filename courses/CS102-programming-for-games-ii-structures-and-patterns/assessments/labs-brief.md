# CS102 · Labs brief

**Weight:** 40% of the course grade.
**What counts:** your best 12 of the 14 weekly labs, with labs 12, 13 and 14 always counted.
**When:** each lab is assigned in its week's session and due at the start of the next week's session, unless the lab says otherwise.

## What this component is for

The labs are where the course's ideas become code you can run and measure. Each one turns a lecture model into a working Python file, then asks you to check the model against your own machine or your own trace. The course outcome "pick data structures by access pattern and cost" is assessed almost entirely here, in labs 4, 5, 8 and 9, because it can only be shown with numbers you measured.

Three labs also build parts you reuse. Lab 12's recorder and bisect tool go into the [pattern project](pattern-project-brief.md). Lab 13's loader becomes the data layer of the [final module](final-module-brief.md), and lab 14's test suite runs against it. That is why those three cannot be dropped.

## The labs

| Lab | Week | Title | Work mode | Feeds into | Can be dropped? |
|---|---|---|---|---|---|
| [01](../labs/lab01.md) | 1 | Gated stats | individual | | yes |
| [02](../labs/lab02.md) | 2 | Breaking up the blob | individual | | yes |
| [03](../labs/lab03.md) | 3 | The chemistry engine | individual | | yes |
| [04](../labs/lab04.md) | 4 | The proximity budget | individual | | yes |
| [05](../labs/lab05.md) | 5 | The item database | individual | | yes |
| [06](../labs/lab06.md) | 6 | Undo and the input buffer | pairs | pattern project (undo) | yes |
| [07](../labs/lab07.md) | 7 | Scene graph and skill tree | individual | | yes |
| [08](../labs/lab08.md) | 8 | Dialogue linter | individual | | yes |
| [09](../labs/lab09.md) | 9 | A world with a component index | individual | pattern project (world) | yes |
| [10](../labs/lab10.md) | 10 | Build and instrument an event bus | individual | pattern project milestone 1 (event table) | yes |
| [11](../labs/lab11.md) | 11 | Table-driven state machines | individual | pattern project (`FSM` class) | yes |
| [12](../labs/lab12.md) | 12 | Record, replay and find the desync | individual | pattern project (recorder, bisect tool) | **no** |
| [13](../labs/lab13.md) | 13 | A validated data loader | pairs | final module (data layer) | **no** |
| [14](../labs/lab14.md) | 14 | A test suite for the combat module | pairs | final module (test suite) | **no** |

Where a lab says "individual, pair discussion allowed", you may talk through ideas with anyone, but the code and the report you submit must be your own. In pair labs both names go on one submission and both partners receive the same mark, unless the spot check below shows one partner cannot explain the work.

If you drop lab 9, 10 or 11 you still need its code for the pattern project. Dropping a lab removes its mark, not the work.

## How each lab is marked

Every lab is marked out of 100 with the rubric printed in the lab.

- **Labs 1 to 12** score each criterion in bands from 0 to 4 (Excellent is 4, the lowest band is 0 to 1; the band names differ slightly between labs) and give each criterion a weight. A criterion earns `weight × band ÷ 4`. A criterion weighted 25% and marked 3 earns 18.75 points.
- **Labs 13 and 14** give points directly (full, half or zero per criterion), totalling 100.

Your labs component is the mean of the 12 lab marks that count, multiplied by 0.40. Each lab that counts is worth about 3.3% of the course.

Where a lab has hidden or automatic checks (lab 13's `check_lab13.py`, lab 14's hidden broken versions of `rules.py`), the markers run them on a clean copy of your folder with Python 3.13. Code that only runs on your machine because of an absolute path or a missing file earns the "does not run" band for that criterion.

## Spot checks

In each lab session from week 2 on, a marker picks a few students and asks two short questions about their previous lab, in the style of the [exam bank](exam-bank.md), rewritten with the student's own code and numbers. Typical questions: "Your `c_pair` was 38 ns. What `n_max` does that give for 8 ms?" or "Point to the line that clears the redo stack and say what breaks without it."

A spot check never lowers a mark for a slip. It exists to confirm the work is yours. If you cannot explain your own code at all, the lab is re-marked after a 10-minute conversation with the instructor, and in a pair lab the mark can then differ between partners.

## Rubric used for spot checks and pair splits

This rubric applies only when a spot check or a pair dispute triggers a re-mark. The lab's own rubric sets the starting mark.

| Band | Points kept from the lab mark | What the student shows |
|---|---|---|
| Full | 100% | Explains what each function they wrote does, traces one input through it, and says why the lab's key number came out as it did |
| Partial | 70% | Explains the main function and the key number, but cannot trace a second function or answer a "what if" change |
| Weak | 40% | Recognises the code and can run it, but cannot say what it does or where a number came from |
| None | 0% | Cannot explain the submitted work |

## Late work

A lab submitted up to 48 hours late is marked out of 80. After 48 hours it is marked for feedback only and counts as 0, which usually makes it one of your two dropped labs. Labs 12, 13 and 14 cannot be dropped, so talk to the instructor before a deadline if one of them is at risk. Extensions for illness or other documented reasons follow the university policy and do not use up a drop.

## Academic integrity

You may use any code from the lectures and starter files. You may use documentation, forums and AI assistants to understand an error or an API, and you must say so in the lab's report in one line ("used the Python docs for `deque`; asked an assistant why `dict` iteration raised"). You may not submit code you cannot explain. The spot checks are designed around that rule.

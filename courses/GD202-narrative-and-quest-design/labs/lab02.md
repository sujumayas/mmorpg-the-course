# GD202 · Lab 02: The remembered choice

**Week:** 2, the player as co-author ([lecture](../lectures/w02-the-player-as-co-author.md)).
**Time:** 2 hours in lab, plus up to 4 hours at home.
**Weight:** dialogue exercises (40% of the course, shared across the exercise labs).

## Objective

Write a short scene sequence in which one binary choice is honored mostly through acknowledgement, not branching. Track every flag in a ledger, measure the cost with the week 2 model, and playtest whether players felt the choice mattered. The point is to find out, with real readers, how few extra words a choice needs before it feels real.

## Starter materials

All in [`lab02-starter/`](lab02-starter/).

- [`scene_template.md`](lab02-starter/scene_template.md), a plain-text format for scenes, choices, `SET` lines and conditional blocks. You may use Twine or ink instead if you already know one of them. The format is only there so the lab needs no tool.
- [`flag_ledger.csv`](lab02-starter/flag_ledger.csv), a sample ledger with one row per flag write or read. It contains two deliberate mistakes.
- [`ledger_check.py`](lab02-starter/ledger_check.py), a finished helper. It reads a ledger and your base word count and prints `W`, `V`, `V/W`, extra words, `R` (with the number of heavy acknowledgements) and extra words per acknowledgement. It also flags written-but-never-read flags, read-but-never-written flags and reads that come before the write.
- The [interactive](../examples/w02-choice-cost.html), to compare your scene against pure branching with the same parameters.

Run the helper from inside the starter folder:

```
cd courses/GD202-narrative-and-quest-design/labs/lab02-starter
../../../../.venv/bin/python ledger_check.py flag_ledger.csv 3000
```

On the sample it prints `W = 4,005`, `R = 3 (heavy 1)` and two problems. Find both in the CSV before you start (5 minutes).

## Steps

1. **Premise (15 min).** Choose an original premise: a small location, the player character and at most two others. No existing characters or settings. Write one sentence for each character's want.
2. **Design the choice (15 min).** Write a binary content choice (it changes what happens, not only how the player says something) at the end of scene 2. Both options must be discernable: the option text tells the player what they are choosing. Name the flag.
3. **Plan the acknowledgements (15 min).** Plan a sequence of 6 to 8 scenes. Mark at least four acknowledgements after the choice, with at least one on the critical path and at least one heavy. Fill in your ledger before you write any prose.
4. **Write (in lab and at home).** Write the scenes in the template format. Target 250 to 500 words per scene. Add one tone choice somewhere that needs only a different next line.
5. **Measure.** Count the words one player reads on option A (shared text plus the A versions). Run `ledger_check.py` with that count. Fix every reported problem. Record `W`, `V/W`, `R` and extra words per acknowledgement.
6. **Compare.** Enter your `N`, `s`, average scene length and `b = 2` into the interactive. Record what full branching would have cost.
7. **Playtest (at home).** Give the scene to two readers, one per option, without telling them about the acknowledgements. Afterwards ask each: "Did your choice matter? Where did you notice it?" Record which acknowledgements they mentioned without prompting.
8. **Revise.** Cut or move any acknowledgement no reader noticed. Strengthen the choice if a reader said it did not matter. Rerun the checker.

## Deliverable

- The scene file (template format, Twine export or ink source).
- Your final `flag_ledger.csv` and the checker's output with no problems.
- A report of at most 600 words: the numbers from step 5, the branching comparison from step 6, a table of which acknowledgements each reader noticed, and what you changed in step 8 and why.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Choice design | Content choice, both options discernable, stakes clear from the text | Choice is clear but one option is obviously right, or mostly a tone choice | Options unclear or choice has no stakes | 20% |
| Acknowledgement plan | 4+ acknowledgements, one heavy, one on the critical path, spaced across the scenes | Meets the count but clustered, or no heavy one | Fewer than 4, or all optional | 20% |
| Ledger and numbers | Checker runs clean; `W`, `V/W`, `R` correct and compared with branching | Numbers present with minor errors | Ledger missing or checker reports problems | 20% |
| Writing quality | Characters' wants drive the scene; lines work in both versions; original setting | Readable, some variant lines feel bolted on | Hard to follow, or uses existing IP | 20% |
| Playtest and revision | Reader evidence drives specific changes | Playtest done, changes loosely linked to it | No playtest | 20% |

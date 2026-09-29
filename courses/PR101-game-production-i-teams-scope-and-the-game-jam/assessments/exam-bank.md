# PR101 · Exam bank: quiz, practice and viva questions

PR101 has no written exam. The grade comes from the jam game (30%, see [jam-game-brief.md](jam-game-brief.md)), the final team game (40%, see [final-team-game-brief.md](final-team-game-brief.md)), the post-mortem (20%, see [post-mortem-brief.md](post-mortem-brief.md)) and peer review (10%, see [peer-review-brief.md](peer-review-brief.md)). This bank has three other jobs.

- **Practice.** Work a week's questions before its lab. If you can answer them with the lecture closed, the lab will go quickly.
- **Lab quizzes.** Most lab sessions open with a 10-minute ungraded quiz of two or three questions from this bank. Usually one applies a lecture model to new numbers and one asks you to explain or critique.
- **Release review and post-mortem viva.** In week 15 each team member answers questions in this style, rewritten with your own team's numbers: your jam log, your bug forecast, your release checklist, your coded post-mortem.

Every question is tagged with its week and one type.

- **compute**: apply a lecture model to numbers you have not seen before.
- **analysis**: compare two options, derive a rule or read a result off a model.
- **code**: trace what a piece of Python prints.
- **explain**: say why something behaves as it does, with a number as evidence.
- **critique**: find what is wrong with a plan, a sentence or a document and fix it.

All numbers are invented unless a question names a game. Every game fact used here comes from the lecture of the tagged week, which cites its source and era. Every number was recomputed in Python from the lecture's own model, and every code snippet runs as shown with `.venv/bin/python` (Python 3.13). Write your own answer before you open the solution.

---

## Week 1: Roles on a game team

1. *Week 1 · compute.* A team of 9 works as a full mesh. How many communication channels does it have, and how many does a tenth person add? With `H = 12` hours per person per week and `c = 0.75` hours per channel per person, compute `n*` and the useful capacity at `n = 7, 8, 9, 10`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 36 channels; a tenth person adds 9. `n* = 8.5`. Capacity 52.5, 54, 54, 52.5 hours.

Channels are `9 × 8 / 2 = 36`. The tenth person needs a channel to each of the nine people already there, so 9 new channels and 45 in total.

`n* = (H + c) / (2c) = 12.75 / 1.5 = 8.5`. Capacity is `n × H − c × n × (n − 1)`.

| n | Total hours | Coordination hours | Capacity |
|---|---|---|---|
| 7 | 84 | 0.75 × 7 × 6 = 31.5 | 52.5 |
| 8 | 96 | 42 | 54 |
| 9 | 108 | 54 | 54 |
| 10 | 120 | 67.5 | 52.5 |

8 and 9 tie, which matches `n* = 8.5`. The top is flat: going from 7 to 9 people adds 24 hours of work time and only 1.5 hours of useful capacity.
</details>

2. *Week 1 · compute.* A 15-person semester team has `H = 10` and `c = 0.5`. Compare the useful capacity of a full mesh, three sub-teams of 5 whose leads talk, and five sub-teams of 3 whose leads talk.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Full mesh 45 hours, three teams of 5 give 117 hours, five teams of 3 give 125 hours.

Total hours are `15 × 10 = 150`, and each channel costs `2c = 1` hour a week.

- Full mesh: `15 × 14 / 2 = 105` channels, capacity `150 − 105 = 45`.
- Three sub-teams of 5: inside, `3 × (5 × 4 / 2) = 30`; between leads, `3 × 2 / 2 = 3`. Total 33, capacity 117.
- Five sub-teams of 3: inside, `5 × 3 = 15`; between leads, `5 × 4 / 2 = 10`. Total 25, capacity 125.

Smaller sub-teams win here, but the lead layer grows as the pair count of `k`. With 15 teams of 1 you are back to 105 channels among "leads". The lecture's catch also applies. The saving is real only if the sub-teams can finish work without talking across the boundary.
</details>

3. *Week 1 · analysis.* Show that the `n`th person adds `H − 2c(n − 1)` hours of useful capacity. Use it to say what the fifth, sixth and seventh jam teammates add at `H = 30`, `c = 3`, and explain how this matches `n* = (H + c) / (2c) = 5.5`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Fifth adds 6 hours, sixth adds 0, seventh loses 6.

`capacity(n) − capacity(n − 1) = H − c[n(n − 1) − (n − 1)(n − 2)] = H − c × (n − 1) × 2`. The new person brings `H` hours and opens `n − 1` channels, each costing `2c`.

At `H = 30`, `c = 3`: the fifth person adds `30 − 6 × 4 = 6`, the sixth adds `30 − 6 × 5 = 0`, the seventh adds `30 − 6 × 6 = −6`. So capacity peaks at 5 and 6 (both 90 hours in the lecture's table), which is exactly where the continuous formula puts the peak, halfway between them at 5.5. This is the lecture's misconception "more people means faster" in one line.
</details>

4. *Week 1 · analysis.* A jam team runs a short check-in every two hours and posts every decision in one channel, and it measures `c = 2` instead of the lecture's `c = 3`. Recompute `n*` with `H = 30` and the capacity of a team of four. What does this say about how to improve a team?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `n* = 8`. Four people now have 96 useful hours instead of 84.

`n* = (30 + 2) / 4 = 8`. Capacity at `n = 4` is `120 − 2 × 4 × 3 = 96`. Cutting coordination cost by a third gives the same four people 12 more useful hours, the output of almost half an extra person with no new channels. The lecture's judgment point was "lower `c` before you add people". This is that point with numbers.
</details>

5. *Week 1 · critique.* A four-person team's RACI matrix has these rows. Find every problem and fix each with the smallest change.

| Deliverable | Ana | Ben | Chen | Dee |
|---|---|---|---|---|
| Player movement | C | A/R | I | I |
| Enemy AI | A | A | R | I |
| Title screen | C | C | C | C |
| Export a build | I | A/R | I | I |

Their coverage matrix shows that only Ben can export a build.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Enemy AI has two A's. Title screen has no A and no R, and it is all C. Export has bus factor 1.

- **Enemy AI.** Two A's means two people think they have the final say, and Chen gets conflicting instructions. Keep one A (for example Ben, if he owns gameplay code) and make the other a C.
- **Title screen.** Nobody owns the outcome and nobody does the work, so it slips. Every row also being C makes it a full mesh for that task. Name one A and one R (for example Chen A/R for the art and layout, Ben C), and move the others to I.
- **Export a build.** The row is valid, but a skill with bus factor 1 is the one the lecture says a jam cannot live with. Pair Dee with Ben for one hour on day one, and write a five-line export note in the repository.
</details>

## Week 2: Git fundamentals and branching

6. *Week 2 · compute.* Two programmers share `F = 120` files. Each touches `r = 3` new files a day, and they merge every `d = 2` days. Compute the exact and approximate P(overlap) for the pair. If the team grows to four people, each on a branch, what is P(any overlap) per merge, with pairs treated as independent?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Exact 27.0%, approximate 25.9%. With four people, about 84.9%.

`k = r × d = 6`. Exact: `1 − C(114, 6) / C(120, 6) = 27.0%`. Approximate: `1 − e^(−36/120) = 1 − e^(−0.3) = 25.9%`.

Four people give `4 × 3 / 2 = 6` pairs, so `1 − (1 − 0.270)^6 = 84.9%`. The pair count from week 1 turns a one-in-four risk into a near certainty.
</details>

7. *Week 2 · compute.* A team of four with `F = 200` and `r = 2` wants P(any overlap) below 20% per merge. What per-pair overlap chance does that allow, and which merge interval meets it? Use the lecture's exact values (2.0% at one day, 7.8% at two days).

<details>
<summary>Answer and worked solution</summary>

**Answer:** Each pair must stay below about 3.65%. Only daily merges meet it (11.4% for the team).

Six pairs, so `1 − (1 − p)^6 < 0.20` gives `(1 − p)^6 > 0.8` and `p < 1 − 0.8^(1/6) = 3.65%`.

At `d = 1`, `p = 2.0%` and the team's risk is `1 − 0.98^6 = 11.4%`. At `d = 2`, `p = 7.8%` and the team's risk is `1 − 0.922^6 = 38.7%`. Merging every two days fails the target by almost a factor of two.
</details>

8. *Week 2 · code.* What does this print? A team with `k = 12` files per branch is choosing between halving its merge interval (so `k = 6`) and splitting its scenes so `F` doubles from 200 to 400. Which lever does more, and why does the exponent predict it?

```python
from math import comb

def p_overlap(F, k):
    if 2 * k > F:
        return 1.0
    return 1 - comb(F - k, k) / comb(F, k)

for F, k in [(200, 12), (200, 6), (400, 12)]:
    print(F, k, f"{p_overlap(F, k):.1%}")
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** It prints

```
200 12 53.4%
200 6 16.9%
400 12 31.0%
```

Halving the interval wins, 16.9% against 31.0%. The exponent is `k² / F`. Halving `d` halves `k` and so divides the exponent by 4 (144/200 to 36/200). Doubling `F` only divides it by 2 (144/200 to 144/400). Both levers are worth pulling, but the `d²` term makes merge frequency the cheaper one.
</details>

9. *Week 2 · explain.* Unreal Engine 5's One File Per Actor and Unity's UnityYAMLMerge both respond to merge collisions in level files. Say which variable or cost in the week 2 model each one changes, and why neither would be needed for a team where only one person ever edits levels.

<details>
<summary>Answer and worked solution</summary>

**Answer:** One File Per Actor raises `F`. Smart Merge lowers the cost of an overlap, not its chance.

A level saved as one binary file is `F = 1` for level work, so any two people editing it at once always overlap, whatever `d` is. Saving each placed actor in its own file makes `F` roughly the number of actors, which drives `k² / F` toward zero. Unity keeps scenes as text and ships a merge tool that understands scene and prefab files, so an overlap becomes a merge a person can resolve instead of lost work.

With one level editor there is no second branch touching level files, so there are no pairs. The model's risk comes from pairs, which is why clear ownership (the week 1 RACI) also works as a merge-conflict tool.
</details>

10. *Week 2 · critique.* A teammate's merge leaves `balance.cfg` like this, and they propose to "just keep both lines so nothing is lost". What goes wrong, and what are the correct steps?

```
<<<<<<< HEAD
jump = 420
=======
jump = 380
>>>>>>> tuning-pass
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** Keeping both lines leaves either marker lines or a duplicate key in a config file, which crashes the game or loads silently as garbage.

A conflict is a decision handed to a human. Read both sides and both commit messages (`git log -1 tuning-pass`) to find why each value changed. Ask the owner of tuning numbers (the designer, per the RACI) which value is right. Edit the file to that one value, delete all three marker lines, run the game, then `git add balance.cfg` and commit with a message that states the decision.
</details>

## Week 3: Asset workflows and large files (LFS)

11. *Week 3 · compute.* A project has 150 binary assets averaging 6 MB. Each asset is re-saved twice a week. At week 10, how big is a fresh clone without LFS and with LFS, and how long does each take on a 100 Mbps connection? How much does the LFS server store? Use 132-byte pointers and decimal MB.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Without LFS 18,900 MB (25.2 minutes). With LFS about 900.4 MB (1.2 minutes). LFS server 18,900 MB.

Versions `v = 1 + 2 × 10 = 21`.

- Without LFS: `150 × 6 × 21 = 18,900 MB`. Time `18,900 × 8 / 100 = 1,512 s = 25.2 min`.
- With LFS: current files `150 × 6 = 900 MB`, plus pointers `150 × 21 × 132 = 415,800` bytes (0.42 MB). Time `900.4 × 8 / 100 ≈ 72 s = 1.2 min`.
- LFS server: every version is still kept, `150 × 6 × 21 = 18,900 MB`.

LFS moves the cost from every clone to the server. It does not remove it.
</details>

12. *Week 3 · compute.* Three artists share 40 binary files, and each opens 4 of them per day. An overlap costs the loser 1.5 hours of redone work. Estimate the hours lost per 5-day week with no locking.

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 8.0 hours a week.

Per pair per day, `P = 1 − C(36, 4) / C(40, 4) = 1 − 58,905 / 91,390 = 35.5%`. Expected loss per pair per week is `0.355 × 1.5 × 5 = 2.67` hours. Three artists form 3 pairs, so about 8.0 hours, a full working day, thrown away each week. Mark these patterns lockable. The overlaps still happen, but the second person finds out before starting instead of after finishing.
</details>

13. *Week 3 · explain.* A team turned on LFS in week 6 after committing art without it for five weeks. Their new clones are still slow. Explain why, and what fixing it costs the whole team.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Tracking patterns only affect new commits, so five weeks of full binary versions are still in history, and a clone downloads all of history.

The fix is `git lfs migrate import`, which rewrites every commit so the old binaries become pointers. Rewriting history means every teammate must re-clone, and any branch based on the old history must be rebased or recreated. That is why the lecture says to turn LFS on before the first binary commit: one command on day one against a painful afternoon later.
</details>

14. *Week 3 · critique.* A team's `.gitattributes` and `.gitignore` are below. Their project has Aseprite sources, PNG exports, OGG music and Godot 4 text scenes. Name every problem.

```
# .gitattributes
*.png filter=lfs diff=lfs merge=lfs -text
*.tscn filter=lfs diff=lfs merge=lfs -text
# .gitignore
*.import
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** Four problems.

- `*.tscn` should not be in LFS. Scenes are text, and in LFS they can't be diffed or merged on the host.
- `*.import` should not be ignored. Godot's import settings files are small text and are meant to be committed.
- `.godot/` is missing from `.gitignore`, so the derived cache will be committed and cause conflicts in files nobody edited.
- `*.aseprite` and `*.ogg` are not tracked. The sources should be LFS and lockable (`git lfs track --lockable "*.aseprite"`), and the OGG exports should be in LFS.
</details>

## Week 4: Scope, MVP, vertical slice, cut lists

15. *Week 4 · compute.* A team of three has `H = 30` and `c = 2` for the jam and chooses `b = 0.2`. Its task list in build order is below. Compute `C`, `P`, the cut line, `S_MVP` and `m_max`.

| Task | A | B | C | D | E | F | G | H | I | J |
|---|---|---|---|---|---|---|---|---|---|---|
| Tier | MVP | MVP | Slice | MVP | Slice | MVP | Slice | Polish | Polish | Polish |
| Estimate (h) | 5 | 6 | 8 | 4 | 6 | 5 | 7 | 6 | 12 | 4 |

<details>
<summary>Answer and worked solution</summary>

**Answer:** `C = 78`, `P = 62.4`, cut line after task I at 59 hours, `S_MVP = 34`, `m_max = 2.29`.

`C = n × H − c × n × (n − 1) = 90 − 2 × 3 × 2 = 78`. `P = 0.8 × 78 = 62.4`.

Running totals are 5, 11, 19, 23, 29, 34, 41, 47, 59, 63. The total passes 62.4 at task J, so the line falls after task I and J (4 hours) is the cut list.

The last MVP task, F, is sixth in this order, so `S_MVP = 34` and `m_max = 78 / 34 = 2.29`.
</details>

16. *Week 4 · analysis.* Reorder question 15's list so the four MVP tasks come first (A, B, D, F), then the rest in the same order. What happens to the cut line, `S_MVP` and `m_max`? Then let every task take 2.5 times its estimate. What is finished when the 78 real hours run out, in each order, and which order has a playable game?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Same cut line (after I, 59 hours). `S_MVP = 20`, `m_max = 3.9`. At `m = 2.5`, only the MVP-first order is playable.

New running totals: 5, 11, 15, 20, 28, 34, 41, 47, 59, 63. Nothing about the plan's size changed, so the line is where it was. `S_MVP = 5 + 6 + 4 + 5 = 20`, so `m_max = 78 / 20 = 3.9`. The MVP is `20 / 62.4 = 32%` of `P`, inside the lecture's 40% guide.

At `m = 2.5`, 78 real hours buy `78 / 2.5 = 31.2` estimated hours.

- Original order: A, B, C, D and E finish (29 hours). F would reach 34, so the last MVP task is unfinished. Not playable.
- MVP first: A, B, D, F and C finish (28 hours). E would reach 34. Playable.

Same tasks, same estimates. The order decides whether a long overrun costs polish or costs the game.
</details>

17. *Week 4 · compute.* In the lecture's *Lantern* plan, the team wants the moth swarm (task 12, 8 hours) in the plan and moves it to position 6, straight after the MVP, keeping everything else in order. With `P = 63`, where is the new cut line, and which tasks fall below it? What is `m_max`?

<details>
<summary>Answer and worked solution</summary>

**Answer:** The line falls after task 10 at 61 hours. Task 11 (oil pickups) and tasks 13 to 16 are cut. `m_max` stays 3.5.

Running totals: MVP 24, then task 12 gives 32, task 6 gives 40, 7 gives 45, 8 gives 49, 9 gives 54, 10 gives 61. Task 11 would take it to 65, over 63, so the line falls there. The whole slice survives and the moth swarm is in. The MVP is still done at 24 hours, so `m_max = 84 / 24 = 3.5`. The price is the oil pickups, which is a real design cost if the lantern mechanic needs a refill to be interesting.
</details>

18. *Week 4 · critique.* At hour 20 of a jam a teammate says, "the music loop is only 6 hours and we have 6 hours of buffer left, so let's add it and also keep the second level." The second level is above the cut line. What do the cut-line rules and one-in-one-out say?

<details>
<summary>Answer and worked solution</summary>

**Answer:** The buffer is not free hours for a new task. A new task gets an estimate and a tier, and if it goes above the line, tasks at least as large drop below it.

The buffer exists to absorb overruns and forgotten work, which week 6 shows is the normal case. Unused buffer pulls tasks back from the cut list in order, not by what fits. If the team decides music is worth it now, it goes into the ordered list at its priority, and something of at least 6 hours leaves the plan. Keeping both the level and the music with no removal is scope creep.
</details>

## Week 5: Agile and Scrum adapted for games

19. *Week 5 · compute.* A team has `W = 30` useful team-hours per week, a fixed sprint overhead `h = 4.8` team-hours and a wrong-turn rate `λ = 0.4` per week. Compute `L*` and `C(L*)`, and the weekly cost at `L = 0.5, 1, 2, 4` weeks.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `L* = 0.89` weeks, `C(L*) = 10.7` team-hours per week. Costs 12.6, 10.8, 14.4 and 25.2.

`L* = √(2 × 4.8 / (0.4 × 30)) = √0.8 = 0.894`. `C(L*) = √(2hλW) = √115.2 = 10.73`.

| L | Overhead h/L | Waste λWL/2 | Total |
|---|---|---|---|
| 0.5 | 9.6 | 3.0 | 12.6 |
| 1 | 4.8 | 6.0 | 10.8 |
| 2 | 2.4 | 12.0 | 14.4 |
| 4 | 1.2 | 24.0 | 25.2 |

One-week sprints cost almost nothing more than the optimum. Monthly sprints spend 84% of the team's capacity on overhead and rework.
</details>

20. *Week 5 · compute.* A jam team of five (`W = 5` team-hours per working hour) takes 15 minutes each to make and play a build. Wrong turns come about once every four working hours. How often should they build and play?

<details>
<summary>Answer and worked solution</summary>

**Answer:** About every 1.4 working hours.

`h = 5 × 0.25 = 1.25` team-hours, `λ = 0.25` per hour. `L* = √(2 × 1.25 / (0.25 × 5)) = √2 = 1.41` hours. At that length the cost is `√(2 × 1.25 × 0.25 × 5) = 1.77` team-hours per hour, about 35% of the team's time on builds and rework combined, which is the price of pre-production at jam speed.
</details>

21. *Week 5 · analysis.* Show that running sprints `a` times the optimal length costs `(a + 1/a) / 2` times the optimal cost. Use it to check the lecture's pre-production numbers (`L* = 0.84`, `C(L*) = 14.28`, `C(4) = 35.5`), and say what it means for a team that is only "a bit off" its best length.

<details>
<summary>Answer and worked solution</summary>

**Answer:** At `L*` the two terms are equal, each `C*/2`. Scaling `L` by `a` divides overhead by `a` and multiplies waste by `a`, so `C(aL*) = (C*/2)(1/a + a)`.

For the lecture: `a = 4 / 0.840 = 4.76`, so the ratio is `(4.76 + 0.21) / 2 = 2.49`, and `35.5 / 14.28 = 2.49`. It checks.

Being off by a factor of 2 either way costs only 25% more (`(2 + 0.5) / 2 = 1.25`). Being off by 4 costs 2.1 times as much. The curve is flat near the bottom, so a team can round `L*` to a convenient number of days, but not to a month.
</details>

22. *Week 5 · analysis.* The lecture's semester team has `W = 34` and `h = 6`. At what wrong-turn rate `λ` are two-week sprints optimal? Explain what that number means for when a team should switch from one-week to two-week sprints.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `λ ≈ 0.088` per week, about one wrong turn every 11 weeks.

Solve `2 = √(2h / (λW))` for `λ`: `λ = 2h / (W × 4) = 12 / 136 = 0.088`. Two-week sprints pay only once playtests overturn work rarely, which is the lecture's production phase. A team that is still finding its fun (the lecture used `λ = 0.5`) should stay near one-week sprints. The switch is triggered by the count of redone work at reviews, not by the calendar.
</details>

23. *Week 5 · critique.* A team's pre-production sprint goal is "Finish the combat system." Its Sprint Review is a slide deck shown to the instructor. Rewrite the goal, and say what the review does to the team's effective `L`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** A pre-production goal is a question, for example "Find out whether a parry or a dodge makes the first fight more fun, by testing both with three players." Done means the playtest happened and the decision and evidence are written down.

A review where nobody plays the build does not catch wrong turns, so it does not reset the waste clock. The effective `L` is the gap between real play-and-decide moments. If the last one was three sprints ago, `L` is three sprints, however many meetings happened.
</details>

## Week 6: Estimation and why it fails

24. *Week 6 · compute.* A team's eight tasks have estimates 4, 2, 3, 1, 5, 2, 6, 3 hours and actuals 3, 2, 6, 1, 4, 5, 6, 9. Compute each ratio, the median, the mean ratio, the plan ratio `R`, the hours saved by early tasks and lost to late ones, and the buffer `b` that would have absorbed `R`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Ratios 0.75, 1.0, 2.0, 1.0, 0.8, 2.5, 1.0, 3.0. Median 1.0, mean 1.51, `R = 1.38`. Saved 2 hours, lost 12. `b = 0.28`.

Sorted: 0.75, 0.8, 1.0, 1.0, 1.0, 2.0, 2.5, 3.0. The median is the average of the fourth and fifth, `(1.0 + 1.0) / 2 = 1.0`. Five of eight tasks were on time or early. The mean is `12.05 / 8 = 1.51`. `R = 36 / 26 = 1.38`.

Early tasks saved `1 + 1 = 2` hours. Late tasks lost `3 + 3 + 6 = 12`. `b = 1 − 1/1.385 = 0.278`, more than week 4's default of 0.25.
</details>

25. *Week 6 · code.* What does this print for question 24's ratios? Check the p10 by hand with the lecture's rule.

```python
from math import floor

def percentile(values, p):
    s = sorted(values)
    h = (len(s) - 1) * p
    f = floor(h)
    if f == len(s) - 1:
        return s[f]
    return s[f] + (h - f) * (s[f + 1] - s[f])

r = [0.75, 1.0, 2.0, 1.0, 0.8, 2.5, 1.0, 3.0]
print([round(percentile(r, p), 3) for p in (0.1, 0.5, 0.9)])
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** It prints `[0.785, 1.0, 2.65]`.

For p10, `h = 7 × 0.1 = 0.7`. Positions 0 and 1 of the sorted list hold 0.75 and 0.8, so the value is `0.75 + 0.7 × 0.05 = 0.785`. For p90, `h = 6.3`, between 2.5 and 3.0, giving `2.5 + 0.3 × 0.5 = 2.65`. A 4-hour task written under this team's history is honestly "about 3 to 11 hours, most likely 4".
</details>

26. *Week 6 · compute.* The logs of a team's ratios have `σ = 0.5` and a geometric mean `G = 1.1`. Estimate the mean ratio and the buffer it needs. With `C = 84`, what is `P`? If splitting tasks brought `σ` down to 0.2 with the same `G`, what buffer would they need?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Mean about 1.25, `b ≈ 0.20`, `P ≈ 67.4`. At `σ = 0.2`, mean about 1.12 and `b ≈ 0.11`.

Skew penalty `e^(0.25/2) = e^0.125 = 1.133`, so the mean is `1.1 × 1.133 = 1.246`. `b = 1 − 1/1.246 = 0.198`, and `P = 0.802 × 84 = 67.4`.

At `σ = 0.2`, the penalty is `e^0.02 = 1.020`, the mean `1.1 × 1.020 = 1.122`, and `b = 1 − 1/1.122 = 0.109`. The median bias (`G = 1.1`) is still there. Splitting only removed the tail, and that alone nearly halved the buffer.
</details>

27. *Week 6 · compute.* The export can start only when three tasks are all finished. Each has a 30% chance of running late, independently. What is the chance the export starts late? How does that compare with a single task, and what does it suggest about the build order in week 4?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 65.7%, more than twice the single-task risk.

`1 − 0.7³ = 1 − 0.343 = 0.657`. Each dependency is another coin flip the export must win. Tasks that many others wait on belong early in the build order, where their lateness has time to be absorbed, and they are the first ones to split so their spread shrinks.
</details>

28. *Week 6 · critique.* A producer says, "Our median ratio was 1.0, so we'll plan the final project with no buffer. And to be safe, everyone pads their own tasks by 25%." Give two problems with this plan, using the lecture's model.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The median says nothing about the plan total, and padding each task gets spent inside the task.

First, the plan ratio tracks the mean, which sits above the median by the skew penalty `e^(σ²/2)`. The lecture's no-rule teams had a median of exactly 1.0 and a plan ratio of 1.48. Second, people work to the time they are given, so padding disappears into every task instead of protecting the deadline. A shared buffer at the end of the plan, sized from the team's own `R` (`b = 1 − 1/R`), and smaller tasks to shrink `σ` do the job the padding pretends to do.
</details>

## Week 7: Task tracking and definitions of done

29. *Week 7 · compute.* A board averages 15 cards in Doing, and the team finishes 3 cards an hour. What is the average cycle time? The producer sets a WIP limit of 6, and the team's throughput stays the same. What is the new cycle time, and what did the limit not change?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 5 hours, then 2 hours. The limit did not change throughput.

Little's law: `W = L / λ = 15 / 3 = 5` hours. With `L = 6`, `W = 6 / 3 = 2` hours. Throughput is set by people and speed. Cutting WIP changes when cards become done, not how many get done per hour. With switching costs, throughput would even rise slightly.
</details>

30. *Week 7 · compute.* Five people (`n = 5`) have 15 cards of 2 person-hours each, with switching overhead `c = 0.1`. Using the lecture's batch model, list the finish times for WIP limits 5, 10 and 15. How many cards are done at a playtest at hour 3, and at hour 5?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `w = 5`: batches finish at 2, 4, 6. `w = 10`: 10 cards at 4.4, then 5 at 6.4. `w = 15`: all at 7.2. At hour 3: 5, 0, 0. At hour 5: 10, 10, 0.

- `w = 5`: `k = 1`, each batch takes 2 hours.
- `w = 10`: the first batch has `k = 2`, so `d = 2 × 2 × 1.1 = 4.4`. The last 5 cards have `k = 1` and take 2 more hours, ending at 6.4.
- `w = 15`: `k = 3`, `d = 2 × 3 × 1.2 = 7.2`.

At hour 3 only the `w = n` board has anything to play. By hour 5, `w = 10` has caught up in count but finishes the whole list 0.4 hours later than `w = 5`, because of switching.
</details>

31. *Week 7 · analysis.* For question 30's `w = 10` case, compute average WIP `L`, throughput `λ` and average cycle time `W`, and show that Little's law holds.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `L = 8.44` cards, `λ = 2.34` cards per hour, `W = 3.6` hours, and `L / λ = 3.6`.

Makespan is 6.4 hours. Average WIP is the card-hours in progress divided by the time: `(10 × 4.4 + 5 × 2) / 6.4 = 54 / 6.4 = 8.44`. Throughput is `15 / 6.4 = 2.34`. Average cycle time is `(10 × 4.4 + 5 × 2) / 15 = 3.6`. And `8.44 / 2.34 = 3.6`. Both averages divide the same 54 card-hours, which is why the law holds whatever the schedule.
</details>

32. *Week 7 · analysis.* Many teams set `w = n + 1`. In question 30 (`n = 5`, `c = 0.1`) with no blocked cards, compute the finish time of the whole list at `w = 6` and compare it with `w = 5`. Then explain when the extra card is worth its cost.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `w = 6` finishes at 6.9 hours against 6.0. It costs about 0.9 hours when nothing is blocked.

Two batches of 6 have `k = 1.2`, so `d = 2 × 1.2 × (1 + 0.1 × 0.2) = 2.448` each, and the last 3 cards take 2 hours: `2.448 + 2.448 + 2 = 6.9`. The extra card is insurance. When one card is blocked on an asset, a strict `w = n` leaves one person idle for the whole wait, which can easily cost more than 0.9 hours. Mark blocked cards visibly so the slack is used for them, not for starting new work.
</details>

33. *Week 7 · compute.* At hour 43 of a jam, 28 of 35 cards are in Done. The 7 cards in To do average 2.5 person-hours. Applying the definition of done, the producer finds 7 "done" cards that fail it, each needing 1.5 person-hours. The team has 4 people and 5 hours left. What share of the real remaining work was hidden, and what must happen?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 10.5 of 28 remaining person-hours were hidden, 37.5%. Cards in To do must be cut now.

Believed remaining: `7 × 2.5 = 17.5`. Hidden: `7 × 1.5 = 10.5`. Real: 28. The team has `4 × 5 = 20` person-hours, less than 28, and hour 42 was content lock anyway. Fix the failing done cards first, since those features are already in the game, and cut the To do cards from the bottom of the list.
</details>

## Week 8: The 48-hour game jam

34. *Week 8 · compute.* A jam game has 6 working features and it is one hour before the deadline, with `q = 0.15` per late change. With no tagged last-good build, should the team make one more change? Give the threshold and the expected value with 0 and 1 changes.

<details>
<summary>Answer and worked solution</summary>

**Answer:** No. The threshold is 5.67, and `F = 6` is already above it. Expected features 6.00 with no change, 5.95 with one.

Threshold `(1 − q) / q = 0.85 / 0.15 = 5.67`. The rule says make a change only if `F + k < 5.67`, and `6 + 0 = 6` fails. `E(0) = 6`, `E(1) = 7 × 0.85 = 5.95`. The one change also creates a 15% chance of shipping nothing.
</details>

35. *Week 8 · compute.* A small game has `F = 4` and `q = 0.1`, with no net. How many late changes maximize expected features, and what is the chance of a broken build at that point? Build the table for `k = 0` to 7.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 5 or 6 changes (they tie at 5.31 expected features). At 5 changes there is a 41.0% chance the build is broken.

| k | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| `(4 + k) × 0.9^k` | 4.00 | 4.50 | 4.86 | 5.10 | 5.25 | 5.31 | 5.31 | 5.26 |
| `1 − 0.9^k` | 0% | 10.0% | 19.0% | 27.1% | 34.4% | 41.0% | 46.9% | 52.2% |

Threshold `0.9 / 0.1 = 9`. Change `k + 1` pays while `4 + k < 9`, so changes 1 to 5 pay and the sixth (`4 + 5 = 9`) is break-even. A game with few features has little to lose, so late changes pay for longer. But "maximum expected value" here means a 41% chance of shipping nothing, which is why the lecture says a graded jam should choose finished.
</details>

36. *Week 8 · compute.* A team with 10 features makes 8 late changes at `q = 0.25`. Compare expected features and the chance of a broken submission with and without a tagged last-good build.

<details>
<summary>Answer and worked solution</summary>

**Answer:** With the net, 16 expected features and 0% broken. Without it, 1.80 expected features and a 90.0% chance of a broken build.

Net: `10 + 8 × 0.75 = 16`. No net: `18 × 0.75^8 = 18 × 0.1001 = 1.80`, and `1 − 0.1001 = 90.0%`. The net only works if someone plays each build before tagging it. An untested tag is a tag of an unknown build.
</details>

37. *Week 8 · analysis.* Derive the rule "make one more change only if `F + k < (1 − q) / q`" from `E(k) = (F + k)(1 − q)^k`. Then explain why the rule's real answer is "stop earlier" when late changes are not independent.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `E(k + 1) > E(k)` means `(F + k + 1)(1 − q)^(k+1) > (F + k)(1 − q)^k`. Divide by `(1 − q)^k` to get `(F + k + 1)(1 − q) > F + k`. Expand: `(F + k)(1 − q) + (1 − q) > F + k`, so `1 − q > q(F + k)`, and `F + k < (1 − q) / q`.

The formula assumes each change breaks the build independently. Late changes pile onto each other, so the third change can break the second, and a tired team raises `q` for all of them at once. The real chance of a clean build falls faster than `(1 − q)^k`, so the break-even point arrives sooner than the rule says. That makes the freeze more valuable, not less.
</details>

38. *Week 8 · explain.* Since version 1.16 (2020), Mojang has published release candidates for Minecraft: Java Edition, and the full release is often identical to the last candidate apart from version numbers. Explain this with the week 8 model, and name the one practice in it that a jam team can copy for free.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Minecraft's `F` is in the thousands, so `F + k` is far above `(1 − q) / q` for any realistic `q`, and every change that isn't fixing a game-breaking bug lowers expected value. A release candidate is the freeze made formal.

The practice to copy is the tagged known-good build. Tag every build that works, after someone has played it. That turns a late mistake from "lose the game" into "lose one feature", which is the difference between the model's two formulas.
</details>

## Week 9: Jam post-mortem

39. *Week 9 · compute.* A task finished with actual effort `A = 10` person-hours. The log shows (spent, remaining estimate) of (0, 4), (3, 3), (6, 2) and (8, 1). Compute `x`, the total ratio and the remaining ratio at each checkpoint. What does each column suggest about the owner's estimating?

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Spent | Remaining est. | `x` | Total ratio | Remaining ratio |
|---|---|---|---|---|
| 0 | 4 | 0.0 | 2.50 | 2.50 |
| 3 | 3 | 0.3 | 1.67 | 2.33 |
| 6 | 2 | 0.6 | 1.25 | 2.00 |
| 8 | 1 | 0.8 | 1.11 | 2.00 |

For example, at the third row the estimated total is `6 + 2 = 8`, so the total ratio is `10 / 8 = 1.25`, and the real remaining work was `10 − 6 = 4` against an estimate of 2, a remaining ratio of 2.0.

The total view marches toward 1 and looks like learning. The remaining view shows the owner was about twice too optimistic about what was left at every checkpoint. The total view narrows because the spent hours are known exactly, not because the estimates improved.
</details>

40. *Week 9 · compute.* One `x` bin of a pooled class log holds six remaining-view ratios: 0.8, 1.0, 1.2, 1.5, 2.0, 3.0. Compute p10, p50 and p90 with the inclusive rule and the spread. Compare the spread with Todd Little's factor of 3 to 4.

<details>
<summary>Answer and worked solution</summary>

**Answer:** p10 0.90, p50 1.35, p90 2.50, spread 2.78.

With `n = 6`, positions are `h = 5p`. p10: `h = 0.5`, halfway between 0.8 and 1.0, so 0.90. p50: `h = 2.5`, halfway between 1.2 and 1.5, so 1.35. p90: `h = 4.5`, halfway between 2.0 and 3.0, so 2.50. Spread `2.50 / 0.90 = 2.78`.

That is a little narrower than Little's 3 to 4 between p10 and p90, but six points is a tiny sample, and one extra bad task would move the p90 a long way (MA102 week 13).
</details>

41. *Week 9 · compute.* A team's finished tasks have ratios (actual ÷ original estimate) of 0.9, 1.1, 1.25, 1.5 and 2.0. It also cut two tasks, each estimated at 4 hours, after spending 6 and 9 hours on them. What is the median with and without the cut tasks, and why is one of them only a lower bound?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 1.25 without the cut tasks. At least 1.5 with them.

The cut tasks' ratios are at least `6 / 4 = 1.5` and `9 / 4 = 2.25`, because they were unfinished when cut. Seven values, sorted: 0.9, 1.1, 1.25, 1.5, 1.5, 2.0, 2.25. The median is the fourth, 1.5. The true ratios of the cut tasks could only be higher, so the true median is at least 1.5. Leaving the cut tasks out hides exactly the worst overruns. That is survivorship.
</details>

42. *Week 9 · critique.* A team's post-mortem says: "Our cone narrowed from a spread of 3.0 to 1.2, so we got much better at estimating during the jam. Also, Sam's levels were late." Rewrite both claims.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The first claim needs the view named. The second needs to be about the process.

If the 3.0 to 1.2 is the total view, it narrows by arithmetic, because the total ratio is a weighted average of 1 (weight `s`) and the remaining ratio (weight `R̂`), and `s` grows. Report the remaining view's spread in the first and last bins too, and claim improvement only if that narrowed.

Blameless version of the second: "Level cards were estimated at hour 0 before anyone had built a level in the engine; the first took 7 hours against 3 (log rows L01 at hours 6 to 18). Change: build one graybox level before estimating level cards. Owner: level lead. Check: level cards in the final project's log are created after that commit."
</details>

## Week 10: Bug tracking and QA basics

43. *Week 10 · compute.* After feature lock a team has `B[0] = 20` open bugs. Testers find `f0 = 12` on day 1, decaying with `d = 0.75` and half-up rounding. The team fixes `c = 6` a day with no regressions. List the finds for days 1 to 6, the open count for days 1 to 6, the peak and the day the backlog reaches zero.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Finds 12, 9, 7, 5, 4, 3. Open 26, 29, 30, 29, 27, 24. Peak 30 on day 3. Zero on day 12.

Day 3 finds `round(12 × 0.75²) = round(6.75) = 7`. Open counts: `20 + 12 − 6 = 26`, `26 + 9 − 6 = 29`, `29 + 7 − 6 = 30`, `30 + 5 − 6 = 29`, and so on. The peak sits on the last day where finds exceed fixes (7 > 6 on day 3, 5 < 6 on day 4). Later finds are 2, 2, 1, 1, 1, 1, 0, so the backlog continues 20, 16, 11, 6, 1 and reaches 0 on day 12.
</details>

44. *Week 10 · code.* Using the lecture's functions, what do the last two lines print? Compare the two changes to question 43's team.

```python
import math

def find_rates(f0, d, days):
    return [math.floor(f0 * d ** (t - 1) + 0.5) for t in range(1, days + 1)]

def backlog(b0, found, c, r=0.0):
    b, regress, rows = b0, 0.0, []
    for f in found:
        arrivals = f + regress
        fixed = min(c, b + arrivals)
        b = b + arrivals - fixed
        regress = r * fixed
        rows.append(b)
    return rows

found = find_rates(12, 0.75, 20)
more = backlog(20, found, 8)
careless = backlog(20, found, 6, r=0.2)
print("c=8:", max(more), more.index(0) + 1)
print("r=0.2:", round(max(careless), 1), careless.index(0) + 1)
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** It prints

```
c=8: 25.0 8
r=0.2: 32.6 14
```

Raising capacity from 6 to 8 lowers the peak from 30 to 25 and pulls the zero day in from 12 to 8. A 20% regression rate at the old capacity raises the peak to 32.6 and pushes the zero day out to 14. Every careless fix both uses capacity and creates new work, so the real drain is `c × (1 − r) = 4.8` a day, not 6.
</details>

45. *Week 10 · compute.* Classify with the lecture's matrix, `P = S + F − 1` clamped to 1 to 4, where always = 0, often = 1, rare = 2: (a) the game crashes when a controller is unplugged during a boss fight, about 1 attempt in 20; (b) the pause menu's volume slider does nothing, every time; (c) a tree's shadow flickers on one level, often.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) P2, (b) P1, (c) P4.

(a) A crash is S1; rare. `1 + 2 − 1 = 2`, P2. (b) A feature that does not work but lets the player carry on is S2; always. `2 + 0 − 1 = 1`, P1. (c) Cosmetic, S4; often. `4 + 1 − 1 = 4`, P4.

The rare crash ranks below the broken slider because every player meets the slider. Priority spends fixing hours. Severity only describes the damage.
</details>

46. *Week 10 · compute.* Two testers test the same build separately. Tester A files 40 bugs and tester B files 25, with 10 on both lists. Estimate the total, the number still unfound, and say which way the estimate is biased.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `N ≈ 100`. They found 55 distinct bugs, so at least about 45 remain.

`N ≈ a × b / m = 40 × 25 / 10 = 100`. Distinct found `40 + 25 − 10 = 55`. The estimate assumes every bug is equally easy to find. Easy bugs on the main path inflate the overlap, and a large overlap makes `N` look small, so the true count is probably higher. Treat 45 as a floor.
</details>

47. *Week 10 · analysis.* A tracker averaged 36 open bugs last month, and the team closed 4 a day. How long does the average bug wait? A teammate proposes "prioritizing better" to cut the wait. Using Little's law, say what that changes and what it doesn't, and give one change that would cut the average wait.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `W = 36 / 4 = 9` days.

Reordering the queue changes which bugs wait, not the average wait, because `L` and `λ` are unchanged. To cut the average you need a shorter list or more real throughput. Closing P4s as won't-fix at the release candidate shrinks `L`. Cutting regressions raises the real `λ`, because fewer fixes create new bugs.
</details>

## Week 11: Communication and conflict in teams

48. *Week 11 · compute.* A team of five has `H = 8` hours each this week and `m = 2.5`. With no individual credit, compute the payoff of each member when all contribute, and of the free rider and each contributor when one member contributes nothing. What is `k*`? Does `k = 0.4` fix it? Does `k = 0.6`?

<details>
<summary>Answer and worked solution</summary>

**Answer:** All contribute 20 each. One free rider: rider 24, contributors 16. `k* = 0.5`. At `k = 0.4` free riding still pays (24 against 23.2). At `k = 0.6` it doesn't (24 against 24.8).

All contribute: `X = 40`, each gets `(2.5 / 5) × 40 = 20`. One rider: `X = 32`, shared part `0.5 × 32 = 16`. The rider adds 8 outside hours, 24. Contributors get 16.

`k* = 1 − m/n = 1 − 0.5 = 0.5`. With `k = 0.4`, contributing when the others do earns `20 + 0.4 × 8 = 23.2`, less than 24. With `k = 0.6`, it earns `20 + 4.8 = 24.8`, more than 24. The return per project hour, `m/n + k − 1`, is −0.1 and +0.1 in the two cases.
</details>

49. *Week 11 · compute.* A studio estimates `m = 3` for project hours. Compute `k*` for teams of 3, 4, 6 and 8. A four-person team's only individual credit is worth `k = 0.3`. What `m` would it need for contributing to pay?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `k*` is 0, 0.25, 0.5 and 0.625. The team needs `m ≥ 2.8`.

`k* = max(0, 1 − 3/n)`: `n = 3` gives 0, `n = 4` gives 0.25, `n = 6` gives 0.5, `n = 8` gives 0.625. For the team with `k = 0.3` and `n = 4`, contributing pays when `m/4 + 0.3 ≥ 1`, so `m ≥ 2.8`. Either the work has to matter more to the shared grade, or the team needs a stronger individual credit.
</details>

50. *Week 11 · analysis.* A team decides that peer review marks will be proportional to each member's number of commits. Give two ways this `k` can be gamed or can hurt the team, and propose a measure that avoids both.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Commits can be inflated by splitting work into tiny commits, and a commit count ignores shared, unglamorous work such as reviewing merges, triaging bugs or fixing someone else's build.

If `k` rewards only visible solo output, nobody takes the shared tasks, which the lecture warns about when `k` is much larger than `m/n`. A better measure counts closed cards that met the definition of done, weighted by estimate, plus reviewed merges and triage duties from the contribution record, each with an evidence link. Splitting a card then gains nothing, and the shared work counts.
</details>

51. *Week 11 · analysis.* Two teammates have argued for a week about whether the jump should be floaty or tight, and messages now include "you never listen". Classify the conflict, choose a Thomas-Kilmann mode, and say why "let's compromise on medium-floaty" is a poor choice here.

<details>
<summary>Answer and worked solution</summary>

**Answer:** It began as task conflict and is turning into relationship conflict. Move it to a call, then collaborate on a test: prototype both jumps, playtest by a fixed date, and log the decision.

De Dreu and Weingart's meta-analysis found that task conflict also hurts performance on complex work, so the aim is to settle it quickly and keep it from becoming personal. Compromise splits the difference, and a blend of two feels can be worse than either, so the design gets worse while both people feel half-heard. A playtest gives a decision both can accept, and the log stops the argument from reopening.
</details>

## Week 12: Crunch, causes, costs, alternatives

52. *Week 12 · compute.* A team plans three weeks at 70 hours, then 40-hour weeks. Using `f = 0.005`, `g = 0.10`, `e_min = 0.3`, compute output for weeks 1 to 8, the lead over a 40-hour team at week 3 and at week 12, and the return per extra hour worked.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Outputs 70, 59.5, 49, 22, 26, 30, 34, 38. Lead +58.5 at week 3 and +8.5 at week 12. Return 0.09 per extra hour.

Each 70-hour week drains `0.005 × 30 = 0.15`, so efficiency runs 1.0, 0.85, 0.70 and starts week 4 at 0.55. Week 4 at 40 hours produces `40 × 0.55 = 22`, then recovery adds 0.10 a week: 26, 30, 34, 38, and 40 from week 9.

Cumulative at week 3 is `70 + 59.5 + 49 = 178.5`, against 120, so +58.5. Weeks 4 to 8 fall short of 40 by `18 + 14 + 10 + 6 + 2 = 50`, leaving +8.5 from week 8 on. Each person worked `3 × 30 = 90` extra hours for 8.5 fresh hours, `8.5 / 90 = 0.094` per extra hour.
</details>

53. *Week 12 · compute.* A team works 50-hour weeks with `f = 0.005`. In which week does weekly output first fall below a rested 40-hour week? Which week produces exactly 40?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Week 6 (37.5 fresh hours). Week 5 produces exactly 40.

Each 50-hour week drains `0.005 × 10 = 0.05`, so week `w` starts at `e = 1 − 0.05(w − 1)`. Output `50e < 40` needs `e < 0.8`, so `w − 1 > 4`, `w = 6`. Week 5 has `e = 0.80` and produces 40, the same as a rested week for 10 more hours. Week 6 has `e = 0.75` and produces 37.5.
</details>

54. *Week 12 · analysis.* Rerun the lecture's four weeks at 60 hours with slower recovery, `g = 0.05`, over 12 weeks. What is the lead at the deadline (week 4), in which week does crunch fall behind, and what is the lead at week 12? What does this say about how much the lecture's conclusion depends on `g`?

<details>
<summary>Answer and worked solution</summary>

**Answer:** +44 at week 4, behind from week 8 (−8), −28 at week 12.

The crunch weeks are unchanged (60, 54, 48, 42), so the deadline lead is +44. Efficiency starts week 5 at 0.6 and now climbs 0.05 a week, giving outputs 24, 26, 28, 30, 32, 34, 36, 38. The lead goes 28, 14, 2, −8, −16, −22, −26, −28. With the lecture's `g = 0.10` the crunch team ended 4 ahead. Halving recovery turns that into 28 behind. The shape (ahead at the deadline, behind later) survives. The week it crosses depends heavily on `g`, which the lecture flags as a teaching value, not a measurement.
</details>

55. *Week 12 · critique.* A student producer writes: "We're 60 hours short with three weeks left, so all four of us will do three 55-hour weeks. That's 180 extra hours, three times what we need." Critique the arithmetic with the ledger and propose a plan that follows the lecture's four-part policy.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The 180 extra hours are clock hours, not fresh hours. Each 55-hour week drains 0.075 of efficiency, so the three weeks produce `55 + 50.9 + 46.8 = 152.6` fresh hours per person against 120, about 32.6 extra per person, and the next weeks pay it back (the following 40-hour week produces only `40 × 0.775 = 31`).

On paper the team still covers 60 hours, but it spends its exam period in recovery and raises its regression rate while fixing bugs. A plan in the lecture's form cuts first from the bottom of the cut list until the gap is small, allows at most one 50-hour week per person (worth about 40 fresh hours for four people), never two in a row, plans a light week after the deadline, and logs overtime in the contribution record.
</details>

## Week 13: Builds and release checklists

56. *Week 13 · compute.* A release has 25 failure items at 4% each. Compute `P(clean)` and the expected escaped defects with no checks, and with every item checked at a catch rate of 0.75.

<details>
<summary>Answer and worked solution</summary>

**Answer:** No checks: 36.0% clean, 1.0 expected escapes. Full coverage at 0.75: 77.8% clean, 0.25 expected escapes.

`0.96^25 = 0.360`. Expected escapes `25 × 0.04 = 1.0`. With checks each item escapes with `0.04 × 0.25 = 0.01`, so `0.99^25 = 0.778` and expected escapes `25 × 0.01 = 0.25`. Without a checklist, almost two releases in three ship with something wrong.
</details>

57. *Week 13 · code.* A team with question 56's list checks 15 of its 25 items at `c = 0.9`. It can spend its next hour on one of three things. What does this print, and which option should it choose?

```python
def p_clean(n, p, coverage=1.0, catch=0.0):
    checked = round(n * coverage)
    unchecked = n - checked
    return (1 - p * (1 - catch)) ** checked * (1 - p) ** unchecked

print(f"now:              {p_clean(25, 0.04, 0.6, 0.9):.1%}")
print(f"perfect checks:   {p_clean(25, 0.04, 0.6, 1.0):.1%}")
print(f"delete 5 items:   {p_clean(20, 0.04, 0.75, 0.9):.1%}")
rest = (1 - 0.04 * 0.1) ** 15 * (1 - 0.04 * 0.5) ** 10
print(f"cover rest at .5: {rest:.1%}")
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** It prints

```
now:              62.6%
perfect checks:   66.5%
delete 5 items:   76.8%
cover rest at .5: 76.9%
```

Making the existing 15 checks perfect gains only 3.9 points, because the 10 unchecked items still carry their full 4% each. Deleting 5 of the unchecked items (a script or pinned engine version makes them impossible) and adding quick checks to all 10 unchecked items both gain about 14 points. Deleting is better in the long run, because it helps every future release without anyone doing the check. Coverage first, rigor second.
</details>

58. *Week 13 · compute.* Put these in SemVer 2.0.0 precedence order, and say which two are equal in precedence: `1.10.0`, `2.0.0-rc.12`, `1.9.3`, `2.0.0`, `1.10.0+b7c1a2`, `2.0.0-rc.3`, `2.0.0-rc.1`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `1.9.3 < 1.10.0 = 1.10.0+b7c1a2 < 2.0.0-rc.1 < 2.0.0-rc.3 < 2.0.0-rc.12 < 2.0.0`.

Each part compares as a number, so 10 beats 9 in the minor version. Build metadata after `+` is ignored when comparing, so `1.10.0` and `1.10.0+b7c1a2` have equal precedence. Numeric pre-release identifiers compare as numbers (12 after 3), and any pre-release sorts before its release.
</details>

59. *Week 13 · analysis.* Suppose a release checklist, run on every build, cut shipped problems from 8.0% of builds to 5.0%. Treating the checklist as one combined catch rate, what is `c`? Relate this to the WHO surgical checklist result in the lecture and to the "all, quick" row of the lecture's table.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `c = 1 − 5.0 / 8.0 = 0.375`.

From `8.0% × (1 − c) = 5.0%`. The lecture's surgical case gave `c ≈ 0.36` (complications 11.0% to 7.0%), a loose check that still cut problems by about a third because it ran on every operation. That is the "all, quick" row. Full coverage at a modest catch rate (78.5%) beat half coverage at a high one (71.6%). A short check on everything beats a careful check on some things.
</details>

60. *Week 13 · critique.* A team's release checklist has these lines: "Check audio", "Make sure the build works", "Version OK". Rewrite each as a line with an owner and a pass condition someone else could verify, and mark which could be automated.

<details>
<summary>Answer and worked solution</summary>

**Answer:** For example:

- "Web build plays music and effects after the first click. Owner: QA owner. Pass: sound heard in two browsers on a machine that isn't the build machine." Human check.
- "Release candidate built from a clean clone of the tagged commit and started on another machine. Owner: build owner. Pass: title screen in under 10 s, new game to first checkpoint with no errors." The clean-clone build is scripted. The play test is human.
- "Version is valid SemVer, newer than the last release, has a changelog heading and matches the title screen. Owner: build owner. Pass: `release_check.py` passes and the title screen shows the same string." Automated, except the title-screen glance.
</details>

## Week 14: Post-mortems as a practice

61. *Week 14 · compute.* A team codes 40 problems across its projects: scope 10, planning 8, tools 7, communication 5, testing 4, bugs 3, audio 2, art 1. Build the Pareto table (share and cumulative share), give `k_80`, and say what the top 20% of categories cover.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Cumulative 25.0, 45.0, 62.5, 75.0, 85.0, 92.5, 97.5, 100%. `k_80 = 5` of 8. The top 20% of categories (`ceil(1.6) = 2`) cover 45.0%.

| Rank | Category | n | Share | Cumulative |
|---|---|---|---|---|
| 1 | Scope | 10 | 25.0% | 25.0% |
| 2 | Planning | 8 | 20.0% | 45.0% |
| 3 | Tools | 7 | 17.5% | 62.5% |
| 4 | Communication | 5 | 12.5% | 75.0% |
| 5 | Testing | 4 | 10.0% | 85.0% |
| 6 | Bugs | 3 | 7.5% | 92.5% |
| 7 | Audio | 2 | 5.0% | 97.5% |
| 8 | Art | 1 | 2.5% | 100.0% |

Five of eight categories (63%) are needed to pass 80%, so the 80/20 rule doesn't hold here.
</details>

62. *Week 14 · code.* What does this print? Explain the order of the two categories with 3 problems each.

```python
counts = {"tools": 3, "scope": 3, "communication": 2, "testing": 1, "bugs": 1}
total = sum(counts.values())
running = 0
for name, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
    running += n
    print(f"{name:13} {n} {running / total:.0%}")
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** It prints

```
scope         3 30%
tools         3 60%
communication 2 80%
bugs          1 90%
testing       1 100%
```

The sort key is (negative count, name), so larger counts come first and ties break alphabetically. "scope" sorts before "tools", and "bugs" before "testing". `k_80 = 3`, since the running total reaches exactly 80% at communication. Without a fixed tie rule, two people would draw different charts from the same data.
</details>

63. *Week 14 · compute.* A team's jam post-mortem listed six categories: scope, planning, communication, bugs, tools, art. Its final-project post-mortem lists planning, testing, communication and audio. Of the jam's six action items, four were done. Compute the recurrence rate and the closure rate, and say what you would check before calling the result good or bad.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `R = 2 / 6 = 33%` (planning and communication came back). Closure `4 / 6 = 67%`.

Check whether the two recurring categories were the ones whose action items were not done. In the lecture's example, every open item came back and every closed one stayed away. Also check whether the final project was much larger, which gives problems more chances to recur, and remember that six categories prove nothing statistically. Testing and audio are new problems, inputs to the next post-mortem rather than failures of this one.
</details>

64. *Week 14 · analysis.* In Politowski and colleagues' 200 Gamasutra post-mortems, "technical" is the largest problem type (116 of 927), yet the largest root causes are insufficient workforce (49) and environment problems (48). Explain how both can be true, and what a producer should do before acting on the top bar of any Pareto chart.

<details>
<summary>Answer and worked solution</summary>

**Answer:** "Technical" is a wide bucket of 18 root causes, the largest only 24. "Team" is a narrow bucket where two root causes dominate, each about twice the largest technical one.

Coarse grouping makes technology look biggest. Grouping by root cause makes people look biggest. Before acting, open the top bar and count how many different causes it holds. A useful category is narrow enough that one kind of action could fix it. Also weigh counts by rough cost, since the table counts mentions, not damage.
</details>

65. *Week 14 · critique.* Rewrite this post-mortem line as blameless, with an action item that has an owner, a change and a check: "Priya didn't tell anyone the save system was broken until the day before release."

<details>
<summary>Answer and worked solution</summary>

**Answer:** For example: "The save system failed on the web build from 3 May, but the first report reached the team channel on 13 May. Our board showed the save card as Done, and we had no smoke test that loaded a save on the web build, so nothing made the failure visible. Action item: add 'save, quit, reload on the web build' to the week 13 smoke test. Owner: QA owner. Check: the next release candidate's checklist shows the line passed."

The rewrite keeps the dates and the effect, points at what the process let happen, and gives one change the team can check. It does not say anything about Priya that the team cannot act on.
</details>

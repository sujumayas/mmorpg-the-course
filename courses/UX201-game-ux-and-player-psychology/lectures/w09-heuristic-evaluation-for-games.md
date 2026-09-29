# UX201 · Week 09 — Heuristic Evaluation for Games

**Why this matters:** You won't always have testers. Sometimes you have a mock-up, two days and three colleagues. A heuristic evaluation turns those colleagues into a structured inspection that finds the obvious problems before a tester has to trip over them. Done alone it misses most of what's there. Done well, with several evaluators, it can also estimate how much it missed, which is the number your producer actually needs.

**You will be able to:**
- Run a heuristic evaluation of a game screen with independent evaluators, Nielsen's ten heuristics and a game-specific set, and consolidate the findings into one list with mean severity ratings.
- Predict how many problems one to ten evaluators will find with the Nielsen-Landauer model, and estimate the problems nobody found with the Lincoln-Petersen and Chao estimators.
- Explain why those two estimators disagree when problems differ in how easy they are to find, and use them as a range rather than a single number.
- Decide which findings are usability problems and which are deliberate challenge, and say what a heuristic evaluation cannot find that a usability test can.

**Before class:** Jakob Nielsen, "How to Conduct a Heuristic Evaluation" and "10 Usability Heuristics for User Interface Design" (Nielsen Norman Group, current versions online), and "The Theory Behind Heuristic Evaluations" (Nielsen, 1994, on the same site). Pinelle, Wong and Stach, "Heuristic evaluation for games: usability principles for video game design," *CHI 2008*, pp. 1453-1462, the introduction and the section presenting the heuristics.

**Prerequisites from earlier courses:** [GD101 week 7, playtesting](../../GD101-introduction-to-game-design/lectures/w07-playtesting-observe-dont-explain.md), for the discovery formula `1 − (1 − p)^n`, which this week applies to evaluators instead of testers. [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md), section 3, for chances that differ. [MA102 week 13, sampling](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md), on why small samples find things but measure badly. From this course, [week 1](w01-perception-attention-memory.md) for "recognition rather than recall" and knowledge in the world, [week 2](w02-cognitive-load-and-ui.md) for intrinsic and extraneous load, and [week 8](w08-usability-testing-methods.md) for usability testing, reach and severity in the report.

**Interactive:** [examples/w09-evaluator-grid.html](../examples/w09-evaluator-grid.html). Use it during section 2.

---

## 1. What a heuristic evaluation is

A **heuristic evaluation** is an inspection method. Instead of watching players, a small group of **evaluators** (designers, UX researchers, anyone trained in the method) examine the interface and judge it against a short list of principles called **heuristics**. Jakob Nielsen and Rolf Molich introduced the method in 1990. Nielsen calls the principles heuristics because they are broad rules of thumb, not precise guidelines.

The method has a fixed shape, and each step exists for a reason.

1. **Scope.** Pick the screen, flow or task to inspect, and the player it is for. "The raid interface, for a player in their first raid." A narrow scope gives a detailed evaluation.
2. **Evaluate independently.** Each evaluator works alone, for about one to two hours. The first pass learns the interface. The second pass looks for violations and records each one against the heuristic it breaks. Evaluators must not see each other's notes until they finish, because the method's power comes from their differences.
3. **Consolidate.** Merge the lists into one, removing duplicates and writing a clear description of each problem.
4. **Rate severity.** Afterwards, send the consolidated list to every evaluator and ask each to rate every problem, including those they didn't find. Take the mean. Nielsen reports that one person's severity ratings are too unreliable to trust, and that the mean of three evaluators is good enough for most purposes.

Nielsen's severity scale combines three factors. **Frequency** is how often the problem occurs. **Impact** is how hard it is to overcome. **Persistence** is whether it bothers users once or every time. The ratings run from 0 to 4.

| Rating | Meaning |
|---|---|
| 0 | Not a usability problem |
| 1 | Cosmetic; fix only if time allows |
| 2 | Minor; low priority |
| 3 | Major; high priority |
| 4 | Catastrophe; must fix before release |

### Nielsen's ten, translated for games

Nielsen's ten heuristics were written for general software. Every one has a game translation.

| # | Heuristic | In a game |
|---|---|---|
| 1 | Visibility of system status | The player can see their health, cooldowns, what the boss is about to do and whether their action worked |
| 2 | Match between system and the real world | Words and icons players already know; "Train" versus "Create" in week 8 |
| 3 | User control and freedom | Cancel a cast, back out of a menu, undo an accidental sale |
| 4 | Consistency and standards | The same role icon everywhere; genre conventions for keys and buttons |
| 5 | Error prevention | Confirm before deleting a character or leaving a raid in progress |
| 6 | Recognition rather than recall | Show the options instead of making players remember them; week 1's knowledge in the world |
| 7 | Flexibility and efficiency of use | Hotkeys, movable frames and quick slots for experts, hidden from beginners (week 2's Skyrim favourites) |
| 8 | Aesthetic and minimalist design | Every HUD element earns its place; nothing important is buried under decoration |
| 9 | Help users recognise, diagnose and recover from errors | "Out of range" appears where the player is looking, in time to act |
| 10 | Help and documentation | A searchable, in-context help for the systems players forget (week 7) |

### Heuristics made for games

General heuristics don't cover play. A game is supposed to be hard in places, and "the enemy is hard to see" might be the point of a stealth level. Researchers have written game-specific sets to fill the gap.

- **HEP (2004).** Heather Desurvire, Martin Caplan and Jozsef Toth assembled Heuristic Evaluation for Playability from usability and playtesting literature, for video, computer and board games. They tested it on a game design in development and compared it with user testing. Their conclusion was that HEP suited early phases and general issues, and worked best combined with user studies. Desurvire and Charlotte Wiberg revised the set as PLAY in 2009.
- **Mobile playability heuristics (2006).** Hannu Korhonen and Elina Koivisto organised their set into three modules: game usability, mobility and gameplay. Evaluating five mobile games with it, they found that usability and mobility problems were easy to identify, and gameplay problems were harder.
- **Pinelle, Wong and Stach (2008).** They built their heuristics from evidence. They analysed PC game reviews from a popular gaming website, covering 108 games, 18 from each of six genres. They sorted the usability complaints into twelve classes of common problems and wrote ten heuristics to avoid them. An early evaluation suggested the heuristics helped find game-specific problems that are easy to overlook.

Use Nielsen's ten plus one game set. Treat both as prompts that make evaluators look at the right things, not as laws. The worked example's last judgment point is about what to do when a heuristic and the game's challenge disagree.

## 2. Worked example: five evaluators, one raid screen

### The hook

In January 2026, World of Warcraft's pre-expansion patch for Midnight (12.0.0) restricted what add-ons can do in combat. Add-ons could no longer register the combat log events, and a new "secret values" system limited the logic add-ons could run on combat information. The API documentation for the patch describes the aim as limiting add-ons' ability to perform complex logic and decision-making from combat information, while keeping customisation of how the interface looks.

In the same patch, Blizzard added features to the default interface. There was a built-in damage meter, and a set called Boss Warnings, with a Boss Timeline showing a boss's upcoming casts in order and centre-screen text alerts graded minor, medium and critical. Before this, raid players who wanted timers and warnings installed add-ons such as Deadly Boss Mods, which is built from one module per raid boss, each triggering alert messages and timer bars.

Read that in this course's terms. Players had been evaluating the default raid interface against heuristic 1, visibility of system status, and fixing the gaps themselves. When the fixes were switched off, the team had to supply the missing status. A studio preparing a new interface doesn't have millions of players inspecting it. It has three to five evaluators and a deadline. How many problems will they find? And since nobody knows the true total, how do they know how many they missed?

### The model

**Discovery across evaluators.** Nielsen and Landauer (1993) modelled the problems found by `i` independent evaluators as

```
found(i) = N × (1 − (1 − λ)^i)
```

- `N` is the total number of problems in the interface, which nobody knows.
- `λ` (lambda) is the share of all problems one evaluator finds.
- `found(i)` is the expected number found by the union of `i` evaluators.

It is GD101 week 7's discovery formula, with evaluators in place of testers. Across six of Nielsen's case studies, `λ` ranged from 19% to 51% with a mean of 34%. Averaged over those projects, a single evaluator found 35% of the problems. That is why Nielsen recommends about five evaluators, and at least three.

**Estimating what nobody found.** Split the evaluators into two independent groups, A and B.

- `n_A` is the number of distinct problems group A found, and `n_B` is the number group B found.
- `m` is the number found by *both* groups.

If every problem were equally easy to find, the share of B's problems that A also found, `m / n_B`, would estimate the share of *all* problems that A found, `n_A / N`. Setting them equal gives the **Lincoln-Petersen estimator**.

```
N̂ = n_A × n_B / m
```

Ecologists use exactly this to count fish in a lake. They catch and mark some, release them, catch again, and see what share of the second catch is marked. A small-sample variant with less bias is the **Chapman estimator**, `N̂ = (n_A + 1)(n_B + 1) / (m + 1) − 1`.

Problems are not equally easy to find, though. Some are found by almost everyone, and those are precisely the ones both groups share, which inflates `m` and pulls `N̂` down. A second estimator, due to Anne Chao (1984), looks at the rare end instead. Let `f₁` be the number of problems found by exactly one evaluator, and `f₂` the number found by exactly two. Then

```
N̂_Chao = S + f₁² / (2 × f₂)
```

where `S` is the number of distinct problems found so far. Many problems seen only once means many more that nobody saw.

### Numbers you can check

An invented MMO, Tidefall, has a new raid interface: group frames, boss warnings, a ready check and a loot roll window. Five evaluators inspect it independently. Because the example is invented, we can tell you what they couldn't know. The screen has 14 problems.

| # | Problem | Heuristic | Mean severity (3 raters) |
|---|---|---|---|
| 1 | Boss warning text uses the same yellow as quest text | 1, 4 | 3.0 |
| 2 | Raid frames show health as numbers only, no bar | 1, 8 | 2.7 |
| 3 | Loot roll window opens over the boss warning area | 8 | 3.3 |
| 4 | Need, Greed and Pass are icons with no labels | 6 | 2.0 |
| 5 | Dispellable debuffs look like all other debuffs | 1 | 3.0 |
| 6 | Leaving the raid needs no confirmation | 5 | 3.3 |
| 7 | Role icons differ from the group finder's icons | 4 | 1.3 |
| 8 | Raid frames can't be moved or resized | 7 | 2.3 |
| 9 | "Target not in line of sight" appears late, at the top edge | 9 | 2.0 |
| 10 | Raid marker names don't appear in chat | 2 | 1.0 |
| 11 | No way to review a boss warning after it fades | 6 | 2.3 |
| 12 | Ready check makes no sound when the game window is in the background | 1 | 2.7 |
| 13 | Loot setting silently resets after the leader disconnects | 1 | 3.7 |
| 14 | In range and out of range shown only by a red or green tint | 1, 4 | 3.0 |

What each evaluator found:

| Evaluator | Problems found | Count |
|---|---|---|
| E1 | 1, 2, 3, 5, 7, 10 | 6 |
| E2 | 1, 2, 4, 6, 8 | 5 |
| E3 | 1, 3, 4, 5, 11 | 5 |
| E4 | 2, 3, 6, 9 | 4 |
| E5 | 1, 2, 7, 12 | 4 |

**One evaluator.** The mean is `24 / 5 = 4.8` problems, so `λ = 4.8 / 14 = 0.34`. That's Nielsen's average almost exactly. Each evaluator on their own found about a third of the problems.

**The union grows.** Add evaluators in order and count distinct problems. E1 gives 6. E2 adds 4, 6 and 8, making 9. E3 adds 11 (10), E4 adds 9 (11), and E5 adds 12 (12). Compare that with the model, `14 × (1 − 0.66^i)`.

| Evaluators `i` | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Found (union, in this order) | 6 | 9 | 10 | 11 | 12 |
| Model `14 × (1 − 0.657^i)` | 4.8 | 8.0 | 10.0 | 11.4 | 12.3 |

Five evaluators found 12 of 14, or 86%. Problems 13 and 14 were found by nobody.

**Lincoln-Petersen.** Split them into A = {E1, E2} and B = {E3, E4, E5}. Group A found {1, 2, 3, 4, 5, 6, 7, 8, 10}, so `n_A = 9`. Group B found {1, 2, 3, 4, 5, 6, 7, 9, 11, 12}, so `n_B = 10`. Both found {1, 2, 3, 4, 5, 6, 7}, so `m = 7`.

```
N̂ = 9 × 10 / 7 = 12.9        Chapman: 10 × 11 / 8 − 1 = 12.75
```

The estimate says about one problem is still hidden. The truth is two.

**Chao.** Count how many evaluators found each problem. Problems 1 and 2 were found by four evaluators, problem 3 by three, problems 4 to 7 by two each, and problems 8 to 12 by one each. So `f₁ = 5` and `f₂ = 4`.

```
N̂_Chao = 12 + 5² / (2 × 4) = 12 + 3.1 = 15.1
```

This estimate says about three problems are still hidden. The truth, 14, sits between the two estimates.

**Why they disagree.** Problems 1 and 2 are obvious. Almost everyone finds them, so they appear in both groups' lists and push `m` up. Lincoln-Petersen reads a high overlap as "we've found nearly everything." Chao looks at the five problems found only once and reads them as the visible tip of a group of hard-to-find problems. When problems differ in difficulty, as they always do, Lincoln-Petersen tends to underestimate. Report both numbers as a range, "between 1 and 3 problems we haven't found," rather than pretending to know.

**Pairs are too small.** Try the estimator on single pairs. E1 and E2 share 2 problems, giving `6 × 5 / 2 = 15`. E1 and E5 share 3, giving `6 × 4 / 3 = 8`, which is fewer problems than the team already found. E3 and E4 share only one, giving 20. With small lists, one shared problem more or less swings the estimate by a factor of two. Use groups, not pairs.

**Severity.** The two missed problems have mean severity 3.7 and 3.0, higher than the average of the twelve found (2.4). By count, the evaluation found 86% of the problems. Weighted by severity, it found `28.9 / 35.6 = 81%`. The problems an inspection misses are not a random sample. Problem 13 appears only after a leader disconnects, a state no evaluator created. Problem 14 is invisible to an evaluator with typical colour vision. An inspection finds what the evaluators can reach and see, which is week 8's reach problem again.

### A visual you can move

Open `examples/w09-evaluator-grid.html`. The left view is Nielsen's grid. Evaluators are rows, problems are columns, and a filled square means "found." Sort the columns by how many evaluators found each problem and the grid forms a staircase. A few columns are almost full, and a long tail has one square each. Two blank columns are shown faded with a "?" and the label "not found," hidden until you turn on "reveal truth."

The right view shows the numbers. There is a curve of problems found against evaluators, with the Nielsen-Landauer model line and the union actually found. Horizontal lines mark the Lincoln-Petersen and Chao estimates. The gap between the union and the estimates is the "still hidden" band.

Drag evaluators into group A or B and watch the Lincoln-Petersen estimate move. Then switch to "simulate." Each problem gets its own chance of being found, drawn from a spread you control. Set the spread to zero (all problems equally findable) and Lincoln-Petersen lands on the truth on average. Widen it and Lincoln-Petersen sinks below the truth while Chao stays closer, often above.

### Cross-game recognition

**Ecology, where the method comes from.** To estimate fish in a pond, catch 10, mark them and release them. Later catch 15, and if 5 of those are marked, the estimate is `10 × 15 / 5 = 30`. Rewrite it in our terms. The first catch is evaluator group A, the second catch is group B, marked fish are shared problems, and the pond is your interface. Ecologists state the same assumption we broke above, that every animal is equally likely to be caught. Trap-shy fish play the part of hard-to-find problems.

**Software inspection.** Eick, Loader, Long, Votta and Vander Wiel (1992) applied the capture-recapture idea to estimate the faults remaining in software design documents from the overlap between reviewers' findings, before any code was written. That is a heuristic evaluation of a design, estimated the same way.

**MMO bot detection (a design application).** Suppose an MMO runs two independent bot detectors, one based on movement patterns and one on trade behaviour. In a week, the first flags 400 accounts, the second flags 300, and 120 are flagged by both. Lincoln-Petersen estimates `400 × 300 / 120 = 1,000` bot accounts, so about 420 bots that neither detector caught. Bots that behave like humans are the trap-shy fish, so treat 1,000 as a floor. This example is illustrative, not a report from a real game. MMO309 covers detection in depth (see its [week 7 lecture](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w07-bot-detection-behavioral-features.md)).

**World of Warcraft, again.** Every widely installed interface add-on is a finding from a very large, very unequal evaluation team. Popular add-ons mark problems many players found. They don't tell you what nobody found, and they over-represent the concerns of players who install add-ons, which is the evaluator selection problem in section 4.

Four contexts, one idea. When two independent searches overlap heavily, most of what exists has probably been found. When they barely overlap, a lot remains hidden. That holds only as far as everything is equally findable.

### Eyes-open design judgment

- **Heuristics flag. Designers decide.** A boss timeline satisfies heuristic 1. Hiding upcoming casts can also be the challenge, because reading the boss is intrinsic load (week 2), the part of the fight you designed on purpose. Blizzard's 12.0 changes show that the line moves, and that the call belongs to design, not to the checklist. Record such findings, then mark them "deliberate challenge" with a reason, or fix them.
- **More evaluators, fewer returns.** The model says evaluator six adds `14 × 0.34 × 0.657⁵ = 0.6` problems. Evaluators cost hours, and a usability test (week 8) finds a different kind of problem. Nielsen puts the sweet spot at three to five. For a critical screen, spend extra effort on different *kinds* of evaluator, not more of the same.
- **Choose evaluators for reach.** The two missed problems needed a disconnect and atypical colour vision. Give evaluators scenarios that create unusual states ("the leader disconnects mid-pull"), and include a colour-vision simulator or an evaluator with the relevant experience. [Week 11](w11-accessibility-guidelines.md) covers accessibility guidelines.
- **Estimates are a range, and a floor.** Report "12 found; estimated 13 to 15 in total," and say that both estimators assume the evaluators worked independently. If they talked during the evaluation, `m` rises and both estimates fall.
- **Heuristic evaluation finds candidates, not verdicts.** Some findings won't bother real players. Others that evaluators rate as minor will stop half your testers. Use the evaluation to decide what to test, then test it.

### Check yourself (worked example)

1. Using `λ = 0.34`, how many evaluators does a team need to expect to find 90% of the problems?
2. A different split is A = {E1, E4} and B = {E2, E3, E5}. Compute `n_A`, `n_B`, `m` and the Lincoln-Petersen estimate.
3. A sixth evaluator joins and finds problems 1, 2, 8 and 13. Recompute `S`, `f₁`, `f₂` and the Chao estimate.

<details>
<summary>Answers</summary>

1. `1 − 0.66^i ≥ 0.9` gives `i ≥ ln 0.1 / ln 0.66 = 5.55`, so six evaluators. For 75%, `ln 0.25 / ln 0.66 = 3.3`, so four.
2. A = {1, 2, 3, 5, 6, 7, 9, 10}, `n_A = 8`. B = {1, 2, 3, 4, 5, 6, 7, 8, 11, 12}, `n_B = 10`. Shared {1, 2, 3, 5, 6, 7}, `m = 6`. `N̂ = 8 × 10 / 6 = 13.3`. A different split gives a different number, which is another reason to report a range.
3. `S = 13` (problem 13 is new). Counts now: problems 1 and 2 by five evaluators, 3 by three, 4, 5, 6, 7 and 8 by two, and 9, 10, 11, 12 and 13 by one. So `f₁ = 5` and `f₂ = 5`. `N̂_Chao = 13 + 25 / 10 = 15.5`. The estimate barely moves, because the new evaluator found one new problem and turned one singleton into a doubleton.

</details>

## 3. Writing up the findings

A heuristic evaluation report has one table and a few paragraphs. Each row of the table is one consolidated problem.

| Field | Content |
|---|---|
| ID and location | "RF-03, raid frames" |
| Description | What the player sees and what goes wrong, in one or two sentences |
| Heuristics violated | Numbers from Nielsen's ten and your game set |
| Found by | Which evaluators (shows how obvious it is) |
| Mean severity | Mean of at least three raters, one decimal |
| Evidence | Screenshot or mock-up with the problem marked |
| Recommendation | A specific change, or "deliberate challenge" with a reason |

Sort by severity, then by how many evaluators found it. Add a short summary at the top. Give the number found, the estimated range still hidden, the count at severity 3 or above, and what you recommend testing next. A reader who stops after the summary should know whether the screen can ship.

Three writing rules keep the report useful.

- **Describe the problem, not the heuristic.** "Players can't tell which debuffs they can dispel" is a finding. "Violates heuristic 1" is a label.
- **One problem per row.** A row that bundles colour, size and position of the same icon hides which part the team fixed.
- **Separate observation from inference.** Evaluators predict player behaviour. Write "a new player may not notice the warning," not "players miss the warning," until a test shows it.

## 4. Heuristic evaluation and usability testing together

The two methods find overlapping but different sets of problems. Desurvire and colleagues found similarities and differences between HEP and user testing on the same game. Their conclusion was that heuristic evaluation fits early phases and general issues, and that the two together make a more usable and playable game. The practical division of labour looks like this.

| | Heuristic evaluation | Usability test (week 8) |
|---|---|---|
| Needs players | No | Yes |
| Earliest use | Paper mock-up | Playable or paper prototype with a "computer" |
| Cost per round | A few evaluator-hours each | Recruiting, sessions, analysis |
| Finds well | Consistency, labels, missing feedback, violations of convention | Wrong mental models, blockers, terminology, what players actually try |
| Misses | States evaluators don't create; player-specific problems; real frequencies | Rare problems at small n; problems behind blockers |
| Output | Candidate problems with predicted severity | Observed problems with evidence and frequency |

A sensible sequence for a new screen is a heuristic evaluation on the mock-up, fixes for the obvious problems, a usability test on the fixed build (so testers don't spend their sessions on problems an evaluator could have spotted), then another evaluation of anything the test changed. Each method clears the ground for the other.

Evaluators also carry biases a test doesn't. They know the game too well, or they know UX principles and see violations everywhere. Their severity guesses reflect their own play. If your evaluators are all experienced raiders, the raid interface will be judged for experienced raiders. That's the week 3 problem again. Pick evaluators who can take the perspective of the player in your scope, and say in the report who they were.

## In-class activity (25 minutes)

Groups of four. The instructor projects a mock-up of the Tidefall crafting screen, or a screen from a game of your choice captured by one group member.

1. **Evaluate alone (10 min).** Each person lists problems with the heuristic number, without talking. Aim for a second pass after five minutes.
2. **Consolidate (7 min).** Merge the four lists. Number the distinct problems and mark who found each.
3. **Estimate (5 min).** Split into two pairs. Compute Lincoln-Petersen and Chao. Report a range for problems not found.
4. **Rate (3 min).** Each person rates severity for the top five problems. Report the means.

Expected output: a consolidated list with a found-by column, two estimates, and mean severities for five problems.

## Common misconceptions

- **"One expert evaluator is enough."** On average one evaluator finds about a third of the problems, and even the best miss problems that weaker evaluators find. The method is built on several independent evaluators.
- **"If our evaluators all found the same problems, we found everything."** High overlap can mean the problems were all obvious. Look at the singletons (Chao) before concluding.
- **"Every heuristic violation should be fixed."** Some violations are the game's challenge. Mark them as deliberate, with a reason.
- **"Heuristic evaluation replaces testing."** It predicts problems without players. Use it to decide what to test and to clear obvious problems before testers arrive.

## Check yourself

1. Two evaluator groups find 12 and 15 problems, with 9 in common. Estimate the total with Lincoln-Petersen and Chapman.
2. A consolidated list has 20 problems, of which 8 were found by exactly one evaluator and 6 by exactly two. What is the Chao estimate?
3. Three evaluators rate a problem 4, 2 and 3. A fourth, who found it, rates it 4. What mean do you report, and why does Nielsen advise collecting ratings after the evaluation rather than during it?
4. A heuristic evaluation of a stealth game flags "guards are hard to see in shadows (heuristic 1)." How do you decide whether to fix it, and what would you write in the report?

<details>
<summary>Answers</summary>

1. `12 × 15 / 9 = 20`. Chapman `13 × 16 / 10 − 1 = 19.8`. About 20 in total, so about 2 not yet found, from a union of `12 + 15 − 9 = 18`.
2. `20 + 8² / (2 × 6) = 20 + 5.3 = 25.3`. About five more problems not yet found.
3. The mean of all four ratings, `13 / 4 = 3.25`, reported as 3.3. Nielsen notes that evaluators rate poorly while they are busy finding problems, and that each has seen only some of the problems. Rating the full consolidated list afterwards means everyone rates everything from the same descriptions.
4. Ask whether seeing guards is part of the intended challenge. If the level is designed around reading the dark, the finding may describe intrinsic load, so record it as "deliberate challenge" with the design reason. Then check in a usability test that players understand *that* guards can hide and *how* to find them (sound cues, a light meter). If players can't tell hidden from absent, the challenge has become extraneous load, and you should fix the feedback without removing the darkness.

</details>

## Lab hook

[Lab 09, heuristic evaluation of a game interface](../labs/lab09.md). In groups of four or five, you inspect one screen or flow of a shipped game independently with Nielsen's ten and one game set, consolidate the findings, collect severity ratings, estimate the problems not found with the starter script, and write a findings report. Deliverable: individual lists, the consolidated table, the script output and a two-page report. The graded heuristic evaluation assignment (20%) follows the same method.

## Sources

- Nielsen, J. & Molich, R. (1990). "Heuristic evaluation of user interfaces." *Proceedings of CHI '90*, pp. 249-256.
- Nielsen Norman Group, "10 Usability Heuristics for User Interface Design" (current version, accessed September 2026). Names and descriptions of the ten heuristics.
- Nielsen Norman Group, "How to Conduct a Heuristic Evaluation" (Moran and Gordon, accessed September 2026). Three to five independent evaluators, no sharing until finished, one to two hours, two passes.
- Nielsen, J. (1994). "The Theory Behind Heuristic Evaluations." Nielsen Norman Group. Single evaluators found 35% of problems averaged over six projects; recommendation of about five evaluators and at least three; the model `N(1 − (1 − λ)^i)`; `λ` from 19% to 51%, mean 34%; `N` from 16 to 50, mean 33; the grid of 19 evaluators and 16 problems for a banking voice-response system.
- Nielsen, J. "How to Rate the Severity of Usability Problems." Nielsen Norman Group (accessed September 2026). Frequency, impact and persistence; the 0 to 4 scale; ratings collected after the evaluation; one rater unreliable, the mean of three satisfactory.
- Nielsen, J. & Landauer, T. K. (1993). "A mathematical model of the finding of usability problems." *Proceedings of INTERCHI '93*, pp. 206-213.
- Desurvire, H., Caplan, M. & Toth, J. A. (2004). "Using heuristics to evaluate the playability of games." *CHI '04 Extended Abstracts*. HEP, tested against user testing on a game in development.
- Desurvire, H. & Wiberg, C. (2009). "Game usability heuristics (PLAY) for evaluating and designing better games: the next iteration." In *Online Communities and Social Computing*, Springer LNCS.
- Korhonen, H. & Koivisto, E. M. I. (2006). "Playability heuristics for mobile games." *MobileHCI '06*. Three modules; five games evaluated; gameplay problems harder to find.
- Pinelle, D., Wong, N. & Stach, T. (2008). "Heuristic evaluation for games: usability principles for video game design." *CHI '08*, pp. 1453-1462. Reviews of 108 PC games, 18 from each of six genres; twelve problem classes; ten heuristics.
- Warcraft Wiki (warcraft.wiki.gg), "Patch 12.0.0" and "Patch 12.0.0/API changes" (accessed September 2026). World of Warcraft Midnight pre-expansion patch, January 2026: combat log events blocked for add-ons, secret values, the stated aim, built-in Damage Meter and Boss Warnings (Boss Timeline and graded text alerts). "World of Warcraft: Midnight": release 2 March 2026. "Deadly Boss Mods": boss modules triggering alert messages and timer bars.
- Wikipedia, "Mark and recapture" (accessed September 2026). Lincoln-Petersen estimator, the equal-catchability assumption, the Chapman estimator, the 10, 15, 5 example.
- Chao, A. (1984). "Nonparametric estimation of the number of classes in a population." *Scandinavian Journal of Statistics*, 11(4), 265-270.
- Eick, S. G., Loader, C. R., Long, M. D., Votta, L. G. & Vander Wiel, S. (1992). "Estimating software fault content before coding." *Proceedings of ICSE '92*, pp. 59-65.
- Tidefall, its 14 problems, the evaluators' findings and the severity ratings are fictional, built for this lecture. The bot-detection numbers are illustrative.

## Interactive spec: examples/w09-evaluator-grid.html

**Purpose.** Show that each evaluator finds about a third of the problems while the union of five finds most of them, and that the overlap between evaluator groups estimates how many remain hidden, with a bias that depends on how unequal the problems are.

**The one insight the visual must make obvious.** On first load, the grid shows five sparse rows (4 to 6 squares each) whose union covers 12 columns, next to a numbers panel reading "Found 12. Estimated total: 12.9 (Lincoln-Petersen) to 15.1 (Chao)." Turning on "reveal truth" shows the two faded columns and "True total 14," which sits between the estimates.

**Layout.** Grid on the left, chart on the right at 1280px. Stacked at 390px, grid first, scrollable horizontally inside its own container only (the page must not scroll sideways). Controls and numbers panel below.

- Grid: rows E1 to E5 (up to 10 in simulate mode), columns problems 1 to 14. A filled square means found. Column headers show problem number and mean severity; hovering or focusing a header shows the description. A final row "found by" shows counts. Hidden columns (found by nobody) are drawn faded with "?" until "reveal truth" is on. Each row has an A/B group toggle.
- Chart: x axis evaluators 1 to 10, y axis problems 0 to 20. Dots for the union found as evaluators are added in grid order; the model line `N × (1 − (1 − λ)^i)` using the true `N` and the observed `λ`. Horizontal dashed lines for the Lincoln-Petersen estimate (from the current A/B split) and the Chao estimate. Shade the band between the union and the higher estimate, labelled "estimated still hidden." With "reveal truth" on, add a solid line at the true `N`.

**Data (defaults).** 14 problems with severities [3.0, 2.7, 3.3, 2.0, 3.0, 3.3, 1.3, 2.3, 2.0, 1.0, 2.3, 2.7, 3.7, 3.0] and the descriptions from the lecture table. Finds: E1 {1, 2, 3, 5, 7, 10}, E2 {1, 2, 4, 6, 8}, E3 {1, 3, 4, 5, 11}, E4 {2, 3, 6, 9}, E5 {1, 2, 7, 12}. Default split A = {E1, E2}, B = {E3, E4, E5}.

**Controls.**

- Group toggles per evaluator (A, B, or excluded).
- Sort columns: by problem number, by found-by count (default after first interaction; initial load by count), by severity.
- Toggle "reveal truth."
- Toggle "weight by severity": the numbers panel shows severity-weighted coverage.
- Simulate mode: true `N` slider (5 to 40, default 14); mean findability slider (0.1 to 0.7, default 0.34); spread slider (0 to 1, default 0.5), where each problem's findability is drawn from a Beta distribution with the given mean and a concentration set by spread (spread 0 means every problem has exactly the mean); evaluators 2 to 10; "run once" redraws one team; "run 1,000" shows histograms of Lincoln-Petersen and Chao estimates with the true `N` marked and the mean of each.
- Presets: "Lecture data", "Equal findability (spread 0)", "Very unequal (spread 0.9)", "Three evaluators only".
- Reset.

**Formulas.**

- `S` = number of problems found by at least one included evaluator.
- `λ̂` = mean over included evaluators of (problems found ÷ true `N`) for the model line; in the numbers panel also show `λ̂` = mean found ÷ `N̂` (Lincoln-Petersen) as "estimated λ".
- `n_A`, `n_B` = distinct problems found by groups A and B; `m` = size of their intersection. Lincoln-Petersen `n_A × n_B / m` (show "undefined, no overlap" if `m = 0`). Chapman `(n_A + 1)(n_B + 1)/(m + 1) − 1`.
- `f_k` = number of problems found by exactly `k` included evaluators. Chao `S + f₁² / (2 f₂)`; if `f₂ = 0`, use the bias-corrected form `S + f₁(f₁ − 1)/2` and label it.
- Severity-weighted coverage = sum of severities of found problems ÷ sum of all severities (only with "reveal truth" on, since the total is otherwise unknown).

**Numbers panel.** Per evaluator: found count. Totals: `S`, Lincoln-Petersen, Chapman, Chao, `f₁`, `f₂`, and a sentence built from the data, for example "5 evaluators found 12 problems. Between 1 and 3 more are probably hidden." With truth revealed: true `N`, coverage by count and by severity.

**Test values.**

- Lecture data, default split: `n_A = 9`, `n_B = 10`, `m = 7`, Lincoln-Petersen 12.86, Chapman 12.75; `f₁ = 5`, `f₂ = 4`, `S = 12`, Chao 15.125.
- Union in order E1..E5: 6, 9, 10, 11, 12. Model with `N = 14`, `λ = 0.3429`: 4.80, 7.95, 10.03, 11.39, 12.28.
- Split A = {E1, E4}, B = {E2, E3, E5}: `n_A = 8`, `n_B = 10`, `m = 6`, Lincoln-Petersen 13.33.
- Pairs: E1 with E2 gives 15.0; E1 with E5 gives 8.0; E3 with E4 gives 20.0.
- Coverage with truth revealed: 12/14 = 85.7% by count; 28.9/35.6 = 81.2% by severity.
- Simulate, spread 0, `N = 14`, mean 0.34, 5 evaluators, 1,000 runs: mean Lincoln-Petersen (runs with `m > 0`) within about 1 of 14.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`, light and dark. Found squares use a fill and a check glyph so they don't rely on colour; group A and B rows are marked by letter as well as tint. The grid is navigable by keyboard (arrow keys move focus between cells; the focused cell announces evaluator, problem and found state). Respect reduced motion. No game art, logos or screenshots; the Tidefall interface is described in text only.

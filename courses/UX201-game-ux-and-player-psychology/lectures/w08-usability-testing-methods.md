# UX201 · Week 08 — Usability Testing Methods

**Why this matters:** A usability test is the cheapest way to watch your game fail for someone who isn't you. Run it badly and you get a list of problems nobody fixes, or a clean report on a build whose worst problems were hiding behind the first one. This week you learn to pick a method, write tasks, measure what matters, and read a result that looks like things got worse after a fix.

**You will be able to:**
- Write a usability test plan for a game sequence with tasks, success criteria and zero-tolerance items, and choose the measures (success, time, errors, failures, assists, SUS) that answer the team's question.
- Compute the effective chance that a tester meets a problem hidden behind a blocking problem, and predict how fixing the blocker changes the error count per tester.
- Compare a batch test with a RITE test by the problems each is expected to find and the fixes each can verify, and choose between them for a given team.
- Compute how many further testers a fix needs before you can trust it, and score a System Usability Scale questionnaire.

**Before class:** Medlock, Wixon, Terrano, Romero and Fulton, "Using the RITE method to improve products: a definition and a case study" (Usability Professionals Association, 2002), all seven pages; it is free online and it is this week's hook. Jakob Nielsen, "Thinking Aloud: The #1 Usability Tool" (Nielsen Norman Group, January 2012). Celia Hodent, *The Gamer's Brain* (CRC Press, 2017), reread the chapter "Usability" (pp. 109-134).

**Prerequisites from earlier courses:** [GD101 week 7, playtesting](../../GD101-introduction-to-game-design/lectures/w07-playtesting-observe-dont-explain.md). This week reuses its discovery formula `P(seen) = 1 − (1 − p)^n`, its session protocol and its rule of silence without re-teaching them. [GD101 week 8, iteration loops](../../GD101-introduction-to-game-design/lectures/w08-iteration-loops-and-kill-your-darlings.md), for loop length and fixing between testers. [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md), section 3, for "at least one" when chances differ. [MA102 week 13, sampling and why n = 5 lies](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md), for why a five-person test finds problems but can't measure rates. From this course, [week 2](w02-cognitive-load-and-ui.md) for task timing and [week 7](w07-onboarding-and-tutorials.md) for the onboarding sequence you will test.

**Interactive:** [RITE and the error spike](../examples/w08-rite-masking.html). Use it during section 2.

---

## 1. What a usability test measures

A **usability test** puts a representative player in front of your game, gives them tasks, and records whether and how they manage. In GD101 week 7 you ran a **playtest**, which asks whether the game produces the experience you wanted. A usability test asks a narrower question. **Can players do what the game needs them to do, without help?** Can they find the crafting station, read the cooldown, equip the new sword, join a group? A game can be fun and fail that test, or pass it and be dull. You need both answers, and they need different sessions.

The method has four parts you write down before the first tester arrives.

**Target players.** Who is this for? The Age of Empires II tutorial team recruited 16 people aged 25 to 44 who had never played a real-time strategy game but wanted to try one, and who had played at least one PC game in the past year. That is a precise definition, and it excludes the team's friends, who were all RTS players.

**Tasks.** Concrete things the tester is asked to do, in the tester's words, not the designer's. "Make a sword" rather than "Use the crafting interface." Each task has a **success criterion** that an observer can judge without arguing, such as "sword in inventory within five minutes, without a hint."

**Zero-tolerance items.** Before the test, the Age of Empires II team listed things every player had to manage after the tutorial, with no errors allowed. The list included moving units, gathering resources, selecting several units, scrolling the map with the mouse, using the mini-map, understanding the fog of war, and building and repairing buildings. Last week you called these moments of need. A zero-tolerance list turns an argument about "is that a real problem?" into a quick yes, because the team agreed in advance.

**Measures.** Choose the ones that answer the team's question.

| Measure | What it is | Good for |
|---|---|---|
| Task success | Did the tester meet the success criterion? | Every test; the headline for each task |
| Time on task | Minutes from task start to success | Comparing designs (week 2's keystroke-level model predicts it) |
| Errors | Mistakes that caused confusion but not failure | Finding friction |
| Failures | Mistakes that stopped the tester continuing without help | Finding blockers |
| Assists | Times the moderator had to step in | Honest reporting of what the game couldn't do alone |
| Think-aloud remarks | What the tester said while acting | The *why* behind every other number |
| SUS | A ten-item questionnaire after the session | Tracking perceived usability across builds |

The Age of Empires II study used exactly two of these, and defined them carefully. A **failure** was an error that stopped the tester continuing with the tutorial. An **error** was a mistake that caused confusion. Keep that distinction. It is the difference between a player who is slowed down and one who is gone.

### Think-aloud

The core technique of most usability tests is **thinking aloud**. The tester narrates what they're doing, looking for and expecting while they play. Nielsen reduces a basic think-aloud study to three steps. Recruit representative users, give them representative tasks, and then stop talking and let them talk. He calls it the most valuable usability method, because you hear the tester's wrong ideas about your design as they form. Those wrong ideas usually tell you what to change.

Games add a complication. Talking uses working memory (week 1), and a player in a fast fight can't narrate and dodge at the same time. Two adjustments are standard. Let testers go quiet during intense moments and prompt them afterwards ("What were you thinking there?"). Or run a **retrospective think-aloud**, where you replay the recording to the tester after the session and ask them to narrate it. Retrospective accounts are cleaner for action but less reliable, because people fill memory gaps with plausible stories.

### The System Usability Scale

The **System Usability Scale (SUS)** is a ten-item questionnaire developed by John Brooke at Digital Equipment Corporation in 1986. Each item is rated from 1 (strongly disagree) to 5 (strongly agree). The odd-numbered items are positive statements ("I thought the system was easy to use"), and the even-numbered items are negative ones ("I found the system unnecessarily complex"). The score is

```
SUS = 2.5 × (20 + sum of odd items − sum of even items)
```

which runs from 0 to 100. A tester who answers 4 to every odd item and 2 to every even item scores `2.5 × (20 + 20 − 10) = 75`. Treat SUS as a thermometer for comparing your own builds, not a grade. With five testers its uncertainty is large, as MA102 week 13 showed for any rate from a small sample. For games, word the items about the part you tested ("the crafting screen"), not the whole game, or testers will answer about how much fun they had.

## 2. Worked example: the fix that raised the error count

### The hook

Before Age of Empires II shipped in 1999, the user testing team at Microsoft Games Studios, working with Ensemble Studios designer Mark Terrano, tested its tutorial with 16 new players, one at a time. After each tester, the team met with the usability engineer and decided what to change before the next one. They changed the build after testers 1, 2, 5, 8, 9 and 10.

The first change fixed a simple problem. The tutorial told players to gather wood, but no trees were on screen, and the first tester spent a long time confused. The team placed trees in view and taught players to explore for more. The problem never appeared again in the next 15 testers.

Then the error count went *up*. The paper shows the per-tester counts only as a chart (its Figure 1) and calls these rises "spikes" after a revision. After later rounds of changes the counts fell, and after the final change only 1 error remained. The authors explain the spike. Once the wood problem was gone, testers got further into the tutorial and met problems that had been there all along.

A fix that makes the numbers worse is a strange thing to show your producer. This section gives you the model that predicts it, and shows why it is good news.

### The model

Order a tutorial's problems by where they occur. Some problems are **blockers**, which stop a tester progressing within the session. Others are **non-blocking**. They cause an error, and the tester carries on.

- `p_j` is the chance that a tester who *reaches* problem `j` meets it.
- `b_k` is the chance that a tester who reaches blocker `k` is stopped by it. For a blocker, `b_k = p_k`.
- The **reach** of problem `j` is the chance a tester gets that far:
  ```
  reach_j = product of (1 − b_k) over every unfixed blocker k before j
  ```
- The **effective chance** that a tester meets problem `j` is
  ```
  p_eff_j = reach_j × p_j
  ```
- Over `n` independent testers on the same build, problem `j` is seen at least once with probability `1 − (1 − p_eff_j)^n`. That is GD101 week 7's formula with `p_eff` in place of `p`. When the build changes between testers, multiply the per-tester "not seen" chances instead: `P(seen) = 1 − Π (1 − p_eff_j,t)` over testers `t`.
- The **expected errors per tester** on a build is the sum of `p_eff` over all unfixed problems.

A fixed problem has `p = 0`, and fixing a blocker raises the reach of everything after it. A tester in a session typically has a moderator who rescues them after a time limit, but the session also has an end time. Our model assumes that a blocked tester uses up the session and doesn't reach later sections. That's a simplification you should check against your own sessions.

### Numbers you can check

An invented MMO tutorial, the Harbor, has five sections and seven problems. The team doesn't know these values. We do, so that you can see what the tests reveal.

| # | Section | Problem | Blocker? | `p` |
|---|---|---|---|---|
| P1 | 1 Movement | Doesn't discover mouse-look; turns with keys only | No | 0.3 |
| B1 | 2 Fishing | No fishing spot visible when the task starts | Yes | 0.6 |
| P2 | 3 Crafting | Craft button greyed out with no reason shown | No | 0.5 |
| B2 | 3 Crafting | Recipe is on a second tab the tester never opens | Yes | 0.4 |
| P3 | 4 Combat | Doesn't read the cooldown swirl; spams the button | No | 0.4 |
| P4 | 4 Combat | Loot window closes on movement; reward lost | No | 0.2 |
| P5 | 5 Group finder | Role icons have no labels | No | 0.3 |

**Reach on the original build.** Everything in section 3 is behind B1, so its reach is `1 − 0.6 = 0.4`. Sections 4 and 5 are behind B1 and B2, so their reach is `0.4 × (1 − 0.4) = 0.24`.

| Problem | `p` | Reach | `p_eff` | Seen in 8 testers, one build |
|---|---|---|---|---|
| P1 | 0.3 | 1 | 0.300 | 0.942 |
| B1 | 0.6 | 1 | 0.600 | 0.999 |
| P2 | 0.5 | 0.4 | 0.200 | 0.832 |
| B2 | 0.4 | 0.4 | 0.160 | 0.752 |
| P3 | 0.4 | 0.24 | 0.096 | 0.554 |
| P4 | 0.2 | 0.24 | 0.048 | 0.325 |
| P5 | 0.3 | 0.24 | 0.072 | 0.450 |
| **Total** | | | **1.476 errors per tester** | **4.85 problems expected seen** |

Check one row by hand. P3 has `p_eff = 0.24 × 0.4 = 0.096`, and `1 − 0.904⁸ = 1 − 0.446 = 0.554`.

Problem P3 is a common problem. Four in ten players who reach combat will meet it. On the original build, a batch test of eight testers has only a 55% chance of showing it at all, because three quarters of testers never reach combat.

**Now run it the RITE way.** Suppose the first tester hits B1, as the first Age of Empires II tester hit the missing trees. The cause and the fix are obvious (put a fishing spot in view), so the team fixes it before tester 2. B2 turns up by tester 3 and is fixed before tester 4. P2 is a one-line text change ("Requires: Copper Ingot") made before tester 6.

Expected errors per tester on each build:

| Testers | Unfixed | `p_eff` for P1, B1, P2, B2, P3, P4, P5 | Errors per tester |
|---|---|---|---|
| 1 | all | 0.30, 0.60, 0.20, 0.16, 0.096, 0.048, 0.072 | 1.48 |
| 2-3 | all but B1 | 0.30, 0, 0.50, 0.40, 0.24, 0.12, 0.18 | **1.74** |
| 4-5 | all but B1, B2 | 0.30, 0, 0.50, 0, 0.40, 0.20, 0.30 | 1.70 |
| 6-8 | P1, P3, P4, P5 | 0.30, 0, 0, 0, 0.40, 0.20, 0.30 | 1.20 |

The first fix *raised* expected errors per tester from 1.48 to 1.74. That is the Age of Empires II spike, produced by nothing more than reach. Fixing B1 cut one problem, but it more than doubled the number of testers who reached sections 3 to 5.

Now compare what each approach knows at the end of eight testers.

| Problem | Batch: seen | RITE: status |
|---|---|---|
| P1 | 0.942 | seen 0.942 |
| B1 | 0.999 | fixed after tester 1, then 7 testers without it |
| P2 | 0.832 | fixed after tester 5, then 3 testers without it |
| B2 | 0.752 | fixed after tester 3, then 5 testers without it |
| P3 | 0.554 | seen 0.959 |
| P4 | 0.325 | seen 0.758 |
| P5 | 0.450 | seen 0.895 |

Check P3 under RITE by hand. Tester 1 meets it with chance 0.096, testers 2 and 3 with 0.24, and testers 4 to 8 with 0.4. The chance nobody sees it is `0.904 × 0.76² × 0.6⁵ = 0.904 × 0.578 × 0.078 = 0.041`, so it is seen with probability 0.959.

The batch test expects to leave `7 − 4.85 = 2.15` problems unknown, and none of its fixes have been tried. The RITE test expects to leave `(1 − 0.942) + (1 − 0.959) + (1 − 0.758) + (1 − 0.895) = 0.445` problems unknown (0.4447 from unrounded values). It has also already watched three fixes survive contact with new testers. Same eight people, same week.

### A visual you can move

Open `examples/w08-rite-masking.html`. The left chart is "errors per tester," a bar per tester, with vertical lines where the build changed. It is the chart from the Age of Empires II paper, and in RITE mode it shows the spike after the first fix. The right chart is "problems still in the build," a falling staircase, with each step labelled by the fix. The two views look like opposite stories. The left one says the build got worse. The right one says it got better at every step.

Switch between "batch" and "RITE." In batch mode the left chart is flat and the right chart doesn't move until the end. Then turn on "simulate," which runs 1,000 random test weeks with the rule "fix a blocker right after its first sighting, fix P2 after its second." Read the distribution of problems left unknown for each approach. Finally, raise B1's `p` to 0.9 and watch the batch test go almost blind to sections 3 to 5.

### Cross-game recognition

**Age of Empires II (1999), the original case.** Rewritten in our terms, the missing trees were a blocker in section 2 of the tutorial. Fixing it raised the reach of everything after, and testers 2 and later found problems that tester 1 never reached. The authors say this directly. Fixing errors early let later participants move further into the tutorial and find more problems. They also used the discovery formula in reverse to verify fixes, which is section 4 of this lecture.

**Valve's Half-Life (1998), from GD101 week 7.** Valve logged position and events for every playtester. A plot of where players went and where they stopped is a reach map. A room nobody reaches is a room whose problems can't be seen, however many testers you run. The logging tells you where to fix a blocker before testing the content behind it.

**Your onboarding from week 7.** A tutorial's steps are a chain of blockers by design. Each step waits for the player to succeed. If step 2's instruction confuses half your testers, your data on steps 3 to 8 comes from half the sample. In the week 7 timeline, a blocker also delays every practice use after it, so forgetting gaps grow for the testers who get stuck.

The rule across all three is the same. Your test sees only the parts of the game that testers reach. Fix what stops them early, and you buy sight of everything behind it.

### Eyes-open design judgment

- **RITE needs the decision-makers in the room.** The Age of Empires II paper lists its conditions. A developer attended every session, the team agreed before testing to fix what it found, the usability engineer knew the domain, and the scenario editor let them change the tutorial between testers. Without those, "fix after each tester" becomes "argue after each tester."
- **Fixing fast means fixing wrong sometimes.** Of the 36 changes in the Age of Empires II test, 6 needed a second fix, a re-fix ratio of 20%. The team first thought testers failed to "train" swordsmen because the interface mixed the words "train" and "create." They made it all "train," the next tester failed the same way, and they switched everything to "create." RITE catches bad fixes because the next tester tests them. A batch test ships them.
- **Small samples between changes miss rare problems.** The paper says so itself. A problem with `p = 0.05` will slip past any three-tester stretch of the same build. RITE is for the frequent problems that block learning. Rare ones need larger samples or telemetry.
- **Don't fix what you don't understand.** The paper's categories are the safeguard. Fix now if the cause and solution are obvious and quick. Start a fix if they are obvious but slow. Collect more data if the cause is unclear or might be your test setup. Most issues in their test were not obvious and waited for more testers.
- **Error counts are not a quality score.** In a RITE test, errors per tester rise when you remove blockers and fall when you remove common problems. Report the right-hand chart, problems remaining, and explain the left one.

### Check yourself (worked example)

1. On the original Harbor build, a batch team runs 12 testers instead of 8. What is the chance they see P4 at least once?
2. After B1 is fixed, what is the reach of section 4? What is `p_eff` for P5?
3. The team fixes B2 first, before B1. What are the errors per tester on that build, and why did the number drop instead of rising?

<details>
<summary>Answers</summary>

1. `p_eff = 0.048`, so `1 − 0.952¹² = 1 − 0.554 = 0.446`. Still worse than a coin flip, because 76% of testers never reach combat.
2. Reach of section 4 is `1 − 0.4 = 0.6` (only B2 still blocks). `p_eff` for P5 is `0.6 × 0.3 = 0.18`.
3. With B2 fixed and B1 in place, reach is 0.4 for sections 3 to 5. Values are P1 0.3, B1 0.6, P2 0.2, B2 0, P3 0.16, P4 0.08, P5 0.12, total 1.46. It drops slightly from 1.48, because B2 was itself met by 16% of testers, and removing it opens sections 4 and 5 only for the 40% who got past B1. Fixing the *first* blocker opens the most game, which is why it causes the biggest spike.

</details>

## 3. Choosing a method

Usability testing is a family of methods. Pick by the question the team needs answered and what the team can change.

| Method | How it runs | Use it when | Watch out for |
|---|---|---|---|
| Moderated think-aloud, rounds | 5 or so testers on one build, fix, repeat | Early builds; team can change things between rounds | Blockers hide later problems within a round |
| RITE | Fix between testers when cause and fix are clear | Tutorials and onboarding; decision-makers attend; fast builds | Needs rapid builds and domain expertise; rare problems slip through |
| Retrospective think-aloud | Tester plays silently, then narrates the replay | Fast action where talking disrupts play | Accounts are reconstructed; takes twice the time |
| Unmoderated remote | Testers record themselves at home with a task script | Many testers cheaply; natural setting | Nobody to probe "why?"; weak recruits; no rescue |
| Benchmark (summative) test | Larger sample, fixed build, measured tasks | Comparing builds or competitors on time and success | Needs 20 or more testers per condition to say anything about rates (MA102 week 13) |

Two rules cover most choices. Test early and small to *find* problems, and test late and large to *measure* them. And never run a test whose results the team has not agreed in advance to act on. The Age of Empires II paper opens with four reasons usability findings go unfixed. Teams don't believe the findings, fixing costs time, feedback arrives too late, and nobody is sure a fix will work. Every method choice should answer at least one of those.

### A test plan in one page

Write this before recruiting anyone.

1. **Question.** What decision will this test inform? ("Can new players finish the Harbor tutorial without help, and where do they get stuck?")
2. **Players.** Recruitment criteria and exclusions. ("Has played an online game in the past year; has never played an MMO; not a friend of the team.")
3. **Tasks.** Each with its success criterion and time limit.
4. **Zero-tolerance items.** What every player must manage afterwards.
5. **Measures.** Which rows of the section 1 table, and how each is logged.
6. **Script.** The words you will say, including the think-aloud instruction and the rescue rule from GD101 week 7.
7. **Change policy.** RITE or rounds, who decides, and how fast a build can change.
8. **Report.** Who gets it, when, and in what form.

## 4. Verifying a fix, and reporting the week

### How many testers does a fix need?

A fix removes a problem, or it doesn't. If it didn't, the problem still appears with its old chance `p`. The chance that `m` further testers all miss a problem that is still there is `(1 − p)^m`. So after `m` testers with no sighting, your confidence that a real problem of frequency `p` would have shown itself is

```
confidence = 1 − (1 − p)^m
```

This is the discovery formula again, read the other way. The Age of Empires II team ran six extra testers after the final build with no fixed problem returning. At `p = 0.3`, `1 − 0.7⁶ = 0.88`, so they were at least 88% confident for problems that common. At `p = 0.1`, `1 − 0.9⁶ = 0.47`, less than even. Their wood fix, seen by 15 testers after the change, reached `1 − 0.9¹⁵ = 0.79` even at `p = 0.1`. These are the figures the paper reports.

| Testers since fix `m` | Confidence at `p = 0.1` | at `p = 0.3` | at `p = 0.6` |
|---|---|---|---|
| 3 | 0.271 | 0.657 | 0.936 |
| 5 | 0.410 | 0.832 | 0.990 |
| 7 | 0.522 | 0.918 | 0.998 |
| 15 | 0.794 | 0.995 | 1.000 |

Blockers with high `p` are verified almost at once. Fixes to rarer problems need many testers, which is one more reason to fix those early in a RITE week, so later testers can verify them.

### Two ratios for the report

The Age of Empires II paper reports two ratios you can reuse.

- **Impact ratio** = problems that received a fix ÷ problems found. Theirs was 30 of 31, or 97%. It measures whether the test changed the game.
- **Re-fix ratio** = fixes that needed redoing ÷ all fixes. Theirs was 6 of 36, or 17%, which the paper rounds to 20%. It measures how often the team's first idea was wrong.

A test with a low impact ratio was wasted, however well it was run. Report both, next to the list of problems still open with their severity. Week 9 covers how to rate severity.

## In-class activity (25 minutes)

Groups of three: a moderator, a tester and an observer. Use the Harbor tutorial as a paper prototype (the instructor provides five printed screens), or any short menu flow in a game on a group member's phone.

1. **Plan (8 min).** Write three tasks with success criteria, one zero-tolerance item and the think-aloud instruction.
2. **Test (10 min).** Run the tester through the tasks. The observer logs errors, failures, assists and remarks with the minute.
3. **Decide (7 min).** Sort every issue into the four RITE categories from the paper (obvious and quick, obvious and slow, unclear cause, might be the test). Choose the one fix you would make before the next tester, and say which later sections it opens up.

Expected output: a half-page plan, an observation log and a one-line RITE decision with its category.

## Common misconceptions

- **"The error count went up, so the fix broke something."** It may have, but the first thing to check is reach. Removing a blocker sends testers into content they never saw before.
- **"Five testers find 85% of problems."** Only of problems that five testers *reach* and meet with about a 31% chance each. Problems behind a blocker have a much lower effective chance until the blocker is fixed.
- **"Think-aloud slows the player, so it ruins game testing."** It changes behaviour in fast sequences. Let testers go quiet during intense moments, prompt afterwards, or use retrospective think-aloud.
- **"A high SUS score means the game is good."** SUS measures perceived usability of what you tested. With five testers it is a rough reading. It says nothing about fun.

## Check yourself

1. A tester answers the ten SUS items 5, 1, 4, 2, 4, 2, 5, 1, 3, 3. What is their score?
2. A problem sits behind two blockers with `b = 0.5` each and has `p = 0.6`. What is its effective chance per tester, and how many testers does a batch test need for a 90% chance of seeing it?
3. After a fix, how many testers without a sighting do you need for 90% confidence that a problem with `p = 0.2` is gone?
4. Your producer says "we can't change builds during the test week; the build pipeline takes two days." Which method do you recommend, and what do you do about blockers?

<details>
<summary>Answers</summary>

1. Odd items sum `5 + 4 + 4 + 5 + 3 = 21`. Even items sum `1 + 2 + 2 + 1 + 3 = 9`. `SUS = 2.5 × (20 + 21 − 9) = 80`.
2. `p_eff = 0.5 × 0.5 × 0.6 = 0.15`. Need `1 − 0.85^n ≥ 0.9`, so `n ≥ ln 0.1 / ln 0.85 = 14.2`, which is 15 testers. Without the blockers, `p = 0.6` needs only 3.
3. `1 − 0.8^m ≥ 0.9` gives `m ≥ ln 0.1 / ln 0.8 = 10.3`, so 11 testers.
4. Rounds, with the rounds matched to the pipeline: for example, five testers, a two-day gap, five more. Within a round, let the moderator rescue a tester at a known blocker after a fixed time limit (logged as an assist), so testers still reach later sections. Report the blocker as found, and don't count problems behind it as absent.

</details>

## Lab hook

[Lab 08, RITE usability test of an onboarding sequence](../labs/lab08.md). In groups, you write a one-page test plan for a short onboarding flow you can change quickly (your own prototype or a modifiable game), run six to eight testers with think-aloud, fix between testers where the cause is clear, and report errors per tester, problems remaining, verification confidence, impact ratio and re-fix ratio. Deliverable: the plan, the logs, the build change list and a three-page report. The graded usability test assignment builds on this lab.

## Sources

- Medlock, M. C., Wixon, D., Terrano, M., Romero, R. L. & Fulton, B. (2002). "Using the RITE method to improve products: a definition and a case study." Usability Professionals Association annual conference, Orlando, July 2002. Free PDF via CiteSeerX. Source for the Age of Empires II (1999) tutorial test: 16 participants (5 women, 11 men, aged 25 to 44, new to RTS games); failures and errors defined; the zero-tolerance list; build changes after participants 1, 2, 5, 8, 9 and 10; the missing-trees fix and its absence in the next 15 participants; the error spike explained by removal of blocking issues; 88% (p = 0.30) and 47% (p = 0.10) verification after six further participants, 79% at p = 0.10 for the wood fix; impact ratio 30 of 31 (97%); 36 fixes including 6 re-fixes, reported as a 20% re-fix ratio; the "train" and "create" re-fix; the four issue categories; the risk of missing rare problems. The spike after the first fix and the single error after the final iteration are stated in the text; per-tester counts appear only in Figure 1 and are not quoted here. Checked against the authors' September 2002 Word version (Microsoft download, Wayback Machine copy of 27 August 2010), September 2026.
- Wikipedia, "RITE Method" (accessed September 2026). Authors, the definition and the two-part philosophy.
- Nielsen, J. (2012, January 15). "Thinking Aloud: The #1 Usability Tool." Nielsen Norman Group. The three steps of a basic think-aloud study and its benefits.
- Brooke, J. The System Usability Scale, developed at Digital Equipment Corporation in 1986; ten items and the scoring formula, via Wikipedia, "System usability scale" (accessed September 2026).
- Birdwell, K. (1999). "The Cabal: Valve's Design Process for Creating Half-Life." Game Developer. Logged player data, as summarised in GD101 week 7.
- Hodent, C. (2017). *The Gamer's Brain*. CRC Press. Chapter "Usability."
- The Harbor tutorial, its seven problems, their values of `p` and the fix schedule are fictional, built for this lecture.

## Interactive spec: examples/w08-rite-masking.html

**Purpose.** Show that fixing a blocker raises the number of errors each later tester makes, because more testers reach the content behind it, and that this is progress. Compare a batch test with a RITE test by problems found and fixes verified.

**The one insight the visual must make obvious.** In RITE mode, the left chart (errors per tester) jumps from 1.48 to 1.74 right after the first fix, while the right chart (problems still in the build) steps down at the same moment.

**Layout.** Two charts side by side at 1280px, stacked at 390px (right chart first on mobile, because it carries the true story). A problem table and controls below, and a numbers panel beside them.

- Left, "Errors per tester": x axis testers 1 to `n` (default 8), y axis 0 to 3. One bar per tester showing expected errors on that tester's build (sum of `p_eff`). Stacked by problem, each segment coloured and labelled on hover or focus. Vertical dashed lines between testers where the build changed, labelled with the fix.
- Right, "Problems still in the build": same x axis, y axis 0 to 7. A step line of unfixed problems after each tester, plus a second line "unfixed and not yet seen (expected)". The second is the sum over unfixed problems of the probability that nobody has seen it so far.
- Problem table: one row per problem with section, blocker flag, `p`, current reach, `p_eff`, P(seen so far) and status (open, fixed after tester k).

**Data (defaults).** Problems in order: P1 section 1, non-blocker, 0.3; B1 section 2, blocker, 0.6; P2 section 3, non-blocker, 0.5; B2 section 3 (after P2), blocker, 0.4; P3 section 4, 0.4; P4 section 4, 0.2; P5 section 5, 0.3. `n = 8`. RITE schedule: B1 fixed after tester 1, B2 after tester 3, P2 after tester 5.

**Controls.**

- Mode: Batch (no fixes during the test) / RITE (scheduled fixes) / Simulate.
- For each problem: `p` slider 0 to 1 (step 0.05), blocker toggle, and "fix after tester" select (never, 1 to `n − 1`), enabled in RITE mode.
- Testers `n`: 3 to 16.
- Simulate: runs 1,000 random test weeks. For each tester, walk the problems in order; a tester meets each unfixed reached problem with chance `p`; meeting a blocker ends the tester's walk. Fix rule, selectable: "fix blockers after first sighting and non-blockers after second sighting" (default) or "never fix during the test" (batch). Show a histogram of problems never seen for each mode, with means.
- Presets: "Default RITE", "Batch", "Fix B2 first", "B1 almost always blocks (p = 0.9)", "No blockers".
- Reset.

**Formulas.**

- For tester `t`, let `F_t` be the set of problems fixed before tester `t`. Walk problems in order with `reach = 1`. For each problem `j`: if `j ∈ F_t`, `p_eff = 0`; else `p_eff = reach × p_j`, and if `j` is a blocker, `reach ← reach × (1 − p_j)` after computing its `p_eff`.
- Errors per tester `t` = `Σ_j p_eff_{j,t}`.
- P(seen by tester `t`) for problem `j` = `1 − Π_{u ≤ t} (1 − p_eff_{j,u})`.
- Unfixed after tester `t` = count of problems not in `F_{t+1}`.
- Unfixed and not yet seen (expected) = `Σ` over unfixed `j` of `Π_{u ≤ t} (1 − p_eff_{j,u})`.
- Verification confidence for a fixed problem `j` with `m` testers after the fix: `1 − (1 − p_j)^m`, shown in the table as "verified: x% at its old p".

**Numbers panel.** Errors per tester for each distinct build; expected problems seen by the end; expected problems unknown by the end; per-fix verification confidence. A sentence built from the data, for example "Fixing B1 raised errors per tester from 1.48 to 1.74. It also raised the chance of seeing P3 from 55% to 96%."

**Test values.**

- Batch, `n = 8`: errors per tester 1.476 for every tester. P(seen): P1 0.942, B1 0.999, P2 0.832, B2 0.752, P3 0.554, P4 0.325, P5 0.450; sum 4.855; unknown 2.145.
- RITE default: errors per tester 1.476, 1.74, 1.74, 1.70, 1.70, 1.20, 1.20, 1.20. P(seen) for unfixed problems: P1 0.942, P3 0.959, P4 0.758, P5 0.895; expected unknown among unfixed 0.445 (0.4447 unrounded). Verification at old `p`: B1 (7 testers) 0.998, B2 (5 testers) 0.922, P2 (3 testers) 0.875.
- Fix B2 first (B2 after tester 1, nothing else): tester 2 errors 1.46.
- Batch, `n = 12`: P(seen) for P4 = 0.446.
- Verification table: `m = 6` gives 0.469 at `p = 0.1` and 0.882 at `p = 0.3`; `m = 15` gives 0.794 at `p = 0.1`.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`, light and dark. Problems differ by colour and by a text label on each bar segment (or a pattern where labels don't fit). Build-change lines are labelled in text. All controls are keyboard operable, and the problem table is a real table. Respect reduced motion (no animated bar growth when set). No game art, logos or screenshots.

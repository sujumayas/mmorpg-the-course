# PR101 · Week 10 — Bug tracking and QA basics

**Why this matters:** Your jam game shipped with bugs, and you probably fixed some of them in the last hour by memory and luck. Your final team game in week 15 is bigger, lasts longer and has more people touching it. Without a shared list of what is broken, and a rule for what gets fixed first, the team will fix easy bugs, forget hard ones and discover on release day that the build is not stable. This week gives you the list, the rule and a model that tells you when the list will be short enough to ship.

**You will be able to:**
- Write a bug report that another person can reproduce on the first try, and assign it a severity and a priority using a written matrix.
- Compute the open-bug backlog day by day from find and fix rates with the rule `B[t] = B[t−1] + found[t] − fixed[t]`, and predict its peak day and the day it reaches zero.
- Explain, with numbers, why a fix that breaks something else costs more than it seems, and why adding fix capacity moves the zero day less than cutting regressions does.
- Estimate how many bugs are still unfound from two testers' overlapping lists, and state the assumption that makes the estimate too low.

**Before class:** Clinton Keith, *Agile Game Development: Build, Play, Repeat* (2nd ed., 2020), chapter 15, "Agile QA and Production". Browse two post-mortems of your choice in the Game Developer (formerly Gamasutra) post-mortem archive and note every sentence that mentions bugs, testing or stability.

**Prerequisites from earlier courses:** [CS101 week 12, debugging](../../CS101-programming-for-games-i/lectures/w12-debugging-breakpoints-logging-rubber-ducking.md) (the reproduce, shrink, observe loop; you will ask testers to do the first two steps for you). [CS102 week 14, unit testing gameplay rules](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w14-unit-testing-gameplay-rules.md) (regression tests). [GD101 week 7, playtesting](../../GD101-introduction-to-game-design/lectures/w07-playtesting-observe-dont-explain.md) (how a playtest differs from a test pass). [GD102 week 2, stocks and flows](../../GD102-systems-design-and-game-mechanics/lectures/w02-stocks-and-flows.md) (the bathtub rule, which this week applies to bugs). From this course, [week 7, task tracking and definitions of done](w07-task-tracking-and-definitions-of-done.md) and [week 9, jam post-mortem](w09-jam-post-mortem.md).

**Interactive:** [`examples/w10-bug-backlog.html`](../examples/w10-bug-backlog.html). Keep it open during section 2.

---

## 1. What QA is, and what a bug is

**Quality assurance (QA)** is the work of finding out, on purpose and with a method, where the game does not do what the team intended. It is different from playtesting. A playtest, as you learned in GD101 week 7, asks whether the design works on a fresh player. Is it fun, is it clear, where do people get lost? A **test pass** asks whether the build works as specified. Does the door open, does the save load, does the game survive alt-tabbing during a cutscene? A playtester who gets lost has found a design problem. A tester who falls through the floor has found a bug. Both matter, and they go to different lists.

A **bug** (or defect) is a difference between what the build does and what the team agreed it should do. That definition has a useful consequence. If nobody wrote down what the game should do, nobody can say whether a behaviour is a bug. This is why week 7's definition of done matters here. "The inventory is done when items stack to 99, the stack count is visible, and dropping a stack drops all of it" gives a tester three things to check. "The inventory is done" gives them nothing.

### The kinds of testing you will do this term

You do not need a QA department to test well. You need to know which kind of test answers which question.

- **Smoke test.** Five minutes after every new build. Does it launch, can you start a game, can you reach the main loop, can you quit? If a smoke test fails, nobody else should waste time on that build.
- **Functional test.** Walk through one feature against its definition of done. The inventory checklist above is a functional test.
- **Regression test.** Recheck things that used to work. Every fixed bug becomes a regression check, by hand in a checklist or automated as in CS102 week 14. Bugs come back more often than beginners expect, because the same fragile code gets touched again.
- **Exploratory test.** A tester with a goal ("try to get stuck in the level geometry") and no script. Exploratory testing finds the bugs nobody imagined.
- **Soak test.** Leave the game running for hours, or repeat a loop a hundred times. It finds memory leaks, timers that overflow and saves that grow without limit.

### Anatomy of a bug report

A bug report is a message to a stranger, possibly yourself in three weeks. Its job is to let that person see the bug on the first try. Every report in your tracker needs these fields:

| Field | Good example | Why it matters |
|---|---|---|
| Title | "Crash when dropping a full stack of arrows while the shop is open" | Searchable, says what and where. Not "game broke". |
| Build | `jam-final 0.4.2`, commit `a3f9c1e` | A bug in an old build may already be fixed. |
| Steps to reproduce | 1. Open shop in town. 2. Open inventory. 3. Drag 99 arrows onto the ground. | The fixer follows these exactly. Number them. |
| Expected result | Arrows drop, shop stays open. | Tells the fixer what "fixed" means. |
| Actual result | Game freezes, then closes. Log attached. | What went wrong, in observable terms. |
| Frequency | 5 of 5 attempts | A bug seen once in twenty tries needs different handling from one seen every time. |
| Severity | S1 (crash) | See below. |
| Attachments | Log file, a 10-second clip | Evidence beats description. |

The steps are the hard part. In CS101 week 12 you learned to shrink a failing case to the smallest input that still fails. A tester who does that shrinking before filing ("it only happens when the shop is open") saves the programmer most of the debugging work. A report that says "sometimes crashes in town" costs the fixer an hour before they even start.

### Severity is not priority

Two different questions hide in "how bad is this bug?"

**Severity** describes the damage the bug does when it happens. It is a fact about the bug, and a tester can judge it. This course uses four levels:

- **S1, blocker.** Crash, hang, lost save, or a player cannot continue.
- **S2, major.** A feature does not work, but the player can carry on.
- **S3, minor.** A feature works wrongly in a way players notice, such as a wrong number on a tooltip.
- **S4, cosmetic.** A texture seam, a typo, a sound that plays slightly late.

Notice that S1 is the worst. GD101 week 7 ranked playtest findings on a scale where the higher number was worse. Studios use both conventions. Pick one, write it at the top of your tracker, and never mix them.

**Priority** describes when the team will fix it. It is a decision, not a fact, and it depends on how often players will meet the bug, how close the deadline is and what else is broken. A tester can suggest a priority, but the team decides it in triage.

To make that decision quick and consistent, write the rule down as a matrix. This course uses frequency bands of **always** (every attempt), **often** (roughly half the attempts or a common path) and **rare** (once in many attempts, or only on an unusual path):

| Severity \ Frequency | Always | Often | Rare |
|---|---|---|---|
| S1 blocker | P1 | P1 | P2 |
| S2 major | P1 | P2 | P3 |
| S3 minor | P2 | P3 | P4 |
| S4 cosmetic | P3 | P4 | P4 |

The matrix follows one rule you can compute. Give the frequency bands the numbers 0, 1 and 2. Then `P = S + F − 1`, clamped to the range 1 to 4. S2 rare is `2 + 2 − 1 = 3`, so P3. You will implement this in lab 10.

What the priorities mean for your final project:

- **P1.** Fix before the next build goes to anyone. A P1 open on release day blocks release.
- **P2.** Fix before release.
- **P3.** Fix if time allows. Otherwise it ships as a **known issue**, listed in the release notes.
- **P4.** Probably never. Close it as "won't fix" when the release candidate is cut, so the list shows what you actually intend to do.

A rare crash is P2, not P1. That feels wrong to beginners, because crashes are the worst thing. But a crash that needs three unusual steps will reach fewer players than a common S2 bug in the main menu, and the team has only so many fixing hours. Priority spends those hours. Severity only describes the damage.

### The life of a bug

Every tracker, from a shared spreadsheet to Jira, GitHub Issues or a board in your task tool, moves bugs through the same states:

```
New → Triaged → Assigned → Fixed → Verified → Closed
                               ↑        |
                               └────────┘  Reopened
```

Two rules keep the list honest. First, the person who fixed a bug does not close it. Someone else, usually the reporter, **verifies** the fix in a new build, following the original steps. Second, a bug that fails verification is **reopened**, not filed again, so the history stays in one place. **Triage** is the short, regular meeting (daily near a deadline, twice a week otherwise) where the team reads every New bug, sets its priority and assigns it.

## 2. Worked example: when will the build be stable?

### The hook

Cyberpunk 2077 launched on 10 December 2020 on PlayStation 4, Xbox One, PC and Stadia. The last-generation console versions had so many bugs and performance problems that Sony removed the game from the PlayStation Store on 18 December 2020, eight days after launch. It did not return to that store until June 2021, and when it did, the store page carried a warning that players still experienced performance issues. In December 2021 CD Projekt agreed to pay US$1.85 million to settle a class action over the release.

We do not know CD Projekt's internal bug counts, and nothing below depends on them. What we know is the outcome. A large, experienced studio shipped builds whose list of serious bugs had not come down far enough. Every team near a date asks the question that decides this. **When will the bug list be short enough to ship?** Most teams answer by gut feeling. You can do better with one line of arithmetic.

### The model

Your open bugs are a **stock**, exactly like the gold stock in GD102 week 2. Testing pours bugs in. Fixing drains them out. The bathtub rule applies unchanged:

```
B[t] = B[t−1] + found[t] + regressions[t] − fixed[t]
fixed[t] = min(c, B[t−1] + found[t] + regressions[t])
regressions[t] = r × fixed[t−1]
```

- `B[t]` is the number of open bugs at the end of day `t`. `B[0]` is the number open when you start.
- `found[t]` is the number of new bugs testers file on day `t`.
- `c` is the team's fix capacity, in bugs per day. You cannot fix more bugs than exist, hence the `min`.
- `r` is the **regression rate**, the fraction of fixes that break something else. Those new bugs show up the day after the fix.

One more fact from experience goes into `found[t]`. After **feature lock**, the point where the team stops adding features, the find rate falls, because testers exhaust the easy bugs first. A simple way to write that is a daily decay:

```
found[t] = round(f0 × d^(t−1))
```

where `f0` is the find rate on day 1 and `d` is the fraction of the previous day's rate that survives (0.8 means each day finds about 80% as many new bugs as the day before). Rounding is half up, so 6.55 becomes 7.

### Numbers you can check

Take a team two weeks from their release. They have just locked features and have `B[0] = 30` open bugs. Testers find `f0 = 20` new bugs on day 1, with `d = 0.8`. The programmers can fix `c = 8` bugs a day. Start with no regressions, `r = 0`.

| Day | Found | Fixed | Open at end of day |
|---|---|---|---|
| 0 | — | — | 30 |
| 1 | 20 | 8 | 42 |
| 2 | 16 | 8 | 50 |
| 3 | 13 | 8 | 55 |
| 4 | 10 | 8 | 57 |
| 5 | 8 | 8 | 57 |
| 6 | 7 | 8 | 56 |
| 7 | 5 | 8 | 53 |
| 8 | 4 | 8 | 49 |
| 9 | 3 | 8 | 44 |
| 10 | 3 | 8 | 39 |

Check a row. Day 3 starts with 50 open. Testers find `round(20 × 0.8²) = round(12.8) = 13`. The team fixes 8. `50 + 13 − 8 = 55`.

Three things in this table surprise almost every team the first time.

**The backlog grows for four days after feature lock, while everyone is fixing at full speed.** On every day where more bugs arrive than leave, the stock rises. The team is working hard and the number on the board goes up. Teams who don't expect this panic and start adding people or hours. The model says wait. The peak comes exactly when the find rate falls to the fix rate, here on day 5, when `found = 8 = c`.

**After the peak, the backlog drains at `c − found`, not at `c`.** On day 7 the team fixes 8 bugs, but 5 new ones arrive, so the list shrinks by only 3. Ten days in, 89 bugs have been found and 80 fixed, and 39 remain open. Run the rule forward and the backlog reaches zero on day 16.

**The bugs you have not found yet are part of the problem.** On day 1 the board showed 30 open bugs. The real amount of work was 30 plus everything testers had not found yet.

This short program reproduces the table. Run it with `.venv/bin/python`:

```python
import math

def find_rates(f0, d, days):
    return [math.floor(f0 * d ** (t - 1) + 0.5) for t in range(1, days + 1)]

def backlog(b0, found, c, r=0.0):
    b, regress, rows = b0, 0.0, []
    for t, f in enumerate(found, start=1):
        arrivals = f + regress
        fixed = min(c, b + arrivals)
        b = b + arrivals - fixed
        regress = r * fixed
        rows.append(b)
    return rows

found = find_rates(20, 0.8, 20)
base = backlog(30, found, 8)
print(found[:10])
print([int(b) for b in base[:10]])
print("zero on day", base.index(0) + 1)
print("r = 0.25:", backlog(30, found, 8, r=0.25)[:20:4])
print("c = 10 zero on day", backlog(30, found, 10).index(0) + 1)
```

It prints:

```
[20, 16, 13, 10, 8, 7, 5, 4, 3, 3]
[42, 50, 55, 57, 57, 56, 53, 49, 44, 39]
zero on day 16
r = 0.25: [42.0, 65.0, 60.0, 44.0, 24.0]
c = 10 zero on day 13
```

### Regressions: the hidden tax

Now suppose a quarter of fixes break something else, `r = 0.25`. With `c = 8`, that is 2 new bugs a day, created by the fixing itself. The team's real net drain is no longer 8 bugs a day. It is `c × (1 − r) = 6`.

| Setting | Peak open | Peak day | Open on day 10 | Day open reaches 0 |
|---|---|---|---|---|
| `c = 8`, `r = 0` | 57 | 4 and 5 | 39 | 16 |
| `c = 8`, `r = 0.25` | 66 | 6 | 57 | 21 |
| `c = 10`, `r = 0` | 49 | 3 and 4 | 19 | 13 |

Compare the rows. Adding 25% more fix capacity (8 to 10) pulls the zero day in by 3 days. A 25% regression rate pushes it out by 5 days. Careless fixing costs more than slow fixing, because each careless fix both uses capacity and creates new work. This is the numerical argument for the regression tests in CS102 week 14, and for the rule that a fix is verified by someone else.

Open the interactive. The left chart shows the daily flows as bars (found plus regressions) against a horizontal line at the fix capacity `c`. The right chart shows the open backlog. Drag `d` or `c` and watch the backlog's peak slide so that it always sits above the day where the bars drop under the line. Then drag `r` up and watch the fix line effectively sink.

### Cross-game recognition

The same stock-and-flow rule shows up wherever work arrives and leaves.

**The economy stock from GD102.** In GD102 week 2 a player's gold followed `S[t+1] = S[t] + inflow − outflow`, and the stock rose whenever the faucet ran faster than the drain. Replace gold with open bugs, faucet with testers, drain with programmers, and you have this week's model. The stock's peak sits where inflow falls to outflow in both cases. It is one idea.

**Little's law, from queueing theory.** In 1961 John Little proved a rule for any stable queue. The average number of items waiting equals the average arrival rate times the average time each item waits, `L = λW`. (These are [week 7](w07-task-tracking-and-definitions-of-done.md)'s queue symbols, not week 5's sprint length, wrong-turn rate and capacity.) It holds regardless of order or arrival pattern, as long as the system runs in a steady state. For bugs, if your team closes 8 bugs a day and the list hovers around 50, the average bug waits `W = L / λ = 50 / 8 ≈ 6` days from filing to fix. A support desk, a restaurant kitchen and a build farm obey the same rule. The useful consequence is that you cannot make bugs wait less without either a shorter list or faster throughput. Asking people to "prioritize better" changes which bugs wait, not how long the average bug waits.

**Cyberpunk 2077 and the release decision (December 2020).** The model does not say how CD Projekt's backlog looked. It says what any team faces near a fixed date. If the date arrives before the backlog has drained, the only choices are to ship with known issues, delay, or cut the platforms or features that generate the most bugs. CD Projekt had already moved the release date three times, from April 2020 to September, then November, then December. Shipping on the last date with the last-generation versions in poor shape led to the store removal. The fourth choice, adding hours, is week 12's topic. This week's model already hints at its limit, because tired programmers raise `r`.

### Eyes-open judgment

The model is a planning tool, and it has blind spots. Use it knowing them.

- **Not every bug must reach zero.** "Zero open bugs" is almost never the release bar. The bar is zero open P1 and P2 bugs, with P3s listed as known issues. Run the model on the must-fix bugs only, and the zero day comes sooner. Triage is how you control which stock you are draining.
- **Bug counts are not equal units.** Eight cosmetic typos are not eight crashes. If your P1 bugs take a day each, measure capacity in P1 fixes per day, not bugs per day.
- **The find rate depends on testing effort.** If testers stop testing, the find rate falls to zero and the backlog looks wonderful. That is a measurement failure, not stability. Keep the test effort constant when you read the curve.
- **Fitting `d` needs a few days of data.** On day 1 you cannot know `d`. After three or four days, divide each day's finds by the previous day's and average. The interactive lets you type in your own daily counts instead of the decay.
- **Watch `r` more than `c`.** A team that tracks reopened and new-from-fix bugs knows its `r`. A team that does not will misread a rising backlog as "testers found more" when it is really "we are breaking things".

## 3. How many bugs have we not found yet?

The worked example exposed a gap. The board shows bugs you have found. The work includes bugs you have not. Ecologists face the same problem counting fish in a lake, and their answer, **capture-recapture**, has been used in software inspection to estimate latent defects (Schofield, 2007).

Two testers test the same build independently, without comparing notes. Tester A files `a` bugs, tester B files `b` bugs, and `m` bugs appear on both lists. The **Lincoln-Petersen estimate** of the total number of bugs that either could find is:

```
N ≈ a × b / m
```

Here is the logic. B's list is a sample of all bugs. The fraction of B's bugs that A also found, `m / b`, estimates the fraction of all bugs that A found, `a / N`. Set them equal and solve.

Example. A finds 24, B finds 18, and 12 are on both lists. `N ≈ 24 × 18 / 12 = 36`. Together they found `24 + 18 − 12 = 30` distinct bugs, so roughly 6 remain for this kind of testing.

If the overlap is small, the news is bad. With the same 24 and 18 but only 4 shared, `N ≈ 108`, and the two testers have seen about a third of what is there.

The estimate assumes every bug is equally easy to find. That is false. Some bugs sit on the main path and everyone trips over them, while others hide behind a rare sequence. Easy bugs inflate the overlap, and a large overlap makes `N` look small. So capture-recapture **underestimates** the true count. Treat its answer as a floor, and use it to compare builds or areas ("the crafting system has far more unfound bugs than combat") rather than as an exact number. The same equal-chance assumption was behind GD101 week 7's `1 − (1 − p)^n` for playtesters, and it fails in the same direction.

## 4. Running QA on a student team

You do not have testers on payroll. You have five busy people and a deadline. What works:

- **One tracker, one owner.** Pick a single place (GitHub Issues if your repo is there, a board column in your task tool, or a shared sheet) and name one person as the **triage owner** each sprint. That person runs triage and keeps the list clean. The role rotates.
- **Everyone files, nobody fixes silently.** If you find and fix a bug in the same minute, still file it, closed, with one line. It is how you learn your `r` and how the post-mortem in week 14 knows what happened.
- **Test someone else's feature.** Authors test the path they built. Others find the paths the author never imagined. Swap features for one exploratory session per week.
- **Smoke-test every build that leaves your machine.** Week 13 will turn this into a release checklist. For now, a five-line checklist in the repo is enough.
- **Keep a known-issues list.** The honest alternative to hiding bugs is listing them. Players and graders both forgive a listed issue more readily than a surprise.

## In-class activity (25 min)

Work in your final-project teams. You need your jam game build and a timer.

1. **Test pass (10 min).** Split the team in two halves. Each half plays the jam build independently for 10 minutes and files every bug on a shared sheet using the report fields from section 1. Do not talk across halves.
2. **Triage (8 min).** Merge the lists. Mark duplicates. Assign severity and frequency, and compute priority with the matrix.
3. **Estimate (4 min).** Count `a`, `b` and `m` and compute the Lincoln-Petersen estimate. How many bugs are still unfound?
4. **Plan (3 min).** Assume your team can fix 4 bugs a day in the final project. Using only your P1 and P2 count, how many days would draining them take if no new bugs were found? What does section 2 say about that answer?

Expected output: one merged, triaged bug sheet; the estimate `N` with its three inputs; and a two-sentence answer to step 4. Hand in the sheet. It is the starting data for lab 10.

## Common misconceptions

- **"A rising bug count means the team is getting worse."** Right after feature lock, a rising count usually means testing is working. The count peaks when the find rate falls to the net fix rate. Judge the trend after the peak.
- **"Severity and priority are the same thing."** Severity is the damage when it happens. Priority is when you fix it, and it also depends on frequency and the deadline. A rare S1 can be a lower priority than a common S2.
- **"We will ship when there are zero bugs."** Almost no shipped game had zero known bugs. The release bar is zero open bugs at or above a chosen priority, with the rest listed as known issues.
- **"Adding programmers is the fastest way to drain the list."** The table shows cutting the regression rate from 25% to 0 saves more days than adding 25% capacity. Careful fixing and regression tests are cheaper than more hands, and PR101 week 11 shows why more hands have their own cost.

## Check yourself

1. A team starts with `B[0] = 12` open bugs, finds 10, 8, 6 and 4 bugs on days 1 to 4, and fixes 7 a day with no regressions. Compute the open count at the end of each day. On which day does it peak?
2. Classify with the matrix: (a) a typo in the credits that every player sees; (b) a save file corrupts if the player quits during an autosave, about 1 attempt in 30; (c) the map screen shows the wrong region name on the main quest path.
3. A team fixes 12 bugs a day and a third of fixes create a new bug. What is their net drain rate? How many bugs a day must testers be finding, at most, for the backlog to shrink?
4. Two testers find 30 and 20 bugs with 15 in common. Estimate the total. A teammate says, "so there are exactly 5 left." What is wrong with that sentence?
5. Your tracker's average open count over the last month was 40 and the team closed 5 bugs a day. How long does the average bug wait? Name one change that would shorten it and one that would not.

<details>
<summary>Answers</summary>

1. Day 1: `12 + 10 − 7 = 15`. Day 2: `15 + 8 − 7 = 16`. Day 3: `16 + 6 − 7 = 15`. Day 4: `15 + 4 − 7 = 12`. Peak on day 2, the last day where finds (8) exceeded fixes (7).
2. (a) S4, always: `4 + 0 − 1 = 3`, P3. (b) S1 (lost save), rare: `1 + 2 − 1 = 2`, P2. (c) S3, always: `3 + 0 − 1 = 2`, P2. "Often" is also defensible for (c) if the screen is rarely opened, which would give P3. Say which band you chose and why.
3. Net drain `12 × (1 − 1/3) = 8` bugs a day. Testers must be finding fewer than 8 new bugs a day for the list to shrink.
4. `N ≈ 30 × 20 / 15 = 40`. Distinct bugs found: `30 + 20 − 15 = 35`, so about 5 remain for this style of testing. The estimate assumes all bugs are equally findable, which makes it a floor. Some bugs neither tester's approach would reach are not counted at all.
5. Little's law: `W = L / λ = 40 / 5 = 8` days. Raising throughput (fixing more per day, or fewer regressions so throughput is real) or shrinking the list (closing P4s as won't-fix) shortens the average wait. Reordering the queue without changing either does not change the average; it changes which bugs wait.

</details>

## Lab / assignment hook

[Lab 10, bug triage and the backlog model](../labs/lab10.md). You implement the priority matrix, the backlog rule and the capture-recapture estimate in Python against provided tests, then run them on your own team's triaged bug sheet from the in-class activity. Deliverable: passing code, five full bug reports and a one-page stability forecast for your final project.

## Sources

- Wikipedia, "Cyberpunk 2077" and "CD Projekt" (accessed September 2026). Release on 10 December 2020 for PlayStation 4, Stadia, Windows and Xbox One; removal from the PlayStation Store on 18 December 2020 over console technical problems; return in June 2021 with a performance warning; the 2020 delays; the US$1.85 million class-action settlement agreed in December 2021.
- Little, J. D. C. (1961). "A Proof for the Queuing Formula L = λW". *Operations Research* 9(3). Summarized in Wikipedia, "Little's law": the relation holds for stationary systems regardless of arrival or service distribution or service order.
- Schofield, J. R. (2007). "Beyond Defect Removal: Latent Defect Estimation With Capture-Recapture Method". *CrossTalk*, August 2007, 27-29. Use of capture-recapture to estimate remaining software defects.
- Wikipedia, "Mark and recapture". The Lincoln-Petersen estimator `N = nK/k`.
- Keith, C. (2020). *Agile Game Development: Build, Play, Repeat* (2nd ed.). Addison-Wesley. Chapter 15, "Agile QA and Production" (table of contents verified on the publisher's page).
- Meadows, D. (2008). *Thinking in Systems: A Primer*. Chelsea Green. The bathtub model of stocks and flows, as used in GD102 week 2.
- The priority matrix, the S1-S4 scale and the backlog parameters in section 2 are this course's teaching conventions, not a standard from any studio.

## Interactive spec: examples/w10-bug-backlog.html

**The one insight.** The open-bug backlog keeps rising after feature lock while the team fixes at full speed, and it peaks exactly on the day the incoming bars drop below the fix-capacity line. Regressions lower that line more than extra capacity raises it.

**Layout.** Two linked charts side by side on desktop (left "Bugs arriving per day", right "Open bugs"), stacked on mobile with the flows chart first. Controls below the charts on mobile, in a right column on desktop. A day-by-day readout table under the charts.

**Model (exact).** Days `t = 1..T`, `T` default 20.
- `found[t] = floor(f0 × d^(t−1) + 0.5)` in decay mode.
- `regressions[1] = 0`; `regressions[t] = r × fixed[t−1]` (not rounded; display to one decimal).
- `arrivals[t] = found[t] + regressions[t]`.
- `fixed[t] = min(c, B[t−1] + arrivals[t])`.
- `B[t] = B[t−1] + arrivals[t] − fixed[t]`, with `B[0] = B0`.
- Peak day = the day(s) with the maximum `B[t]` (list all ties). Zero day = first `t` with `B[t] = 0` (display "after day T" if none).
- Must-fix mode (checkbox "Only P1 and P2 bugs"): multiply `B0` and every `found[t]` by the must-fix share `s` before rounding (`found_s[t] = floor(s × found[t] + 0.5)`, `B0_s = floor(s × B0 + 0.5)`), everything else unchanged.

**Left chart.** x = day 1..T. Stacked bars per day: `found[t]` (primary color) and `regressions[t]` on top (warning color, labelled "caused by fixes"). A horizontal line at `c` labelled "fix capacity" and a dashed line at `c × (1 − r)` labelled "net drain" (only when `r > 0`). Shade the bars in days where `arrivals[t] > fixed[t]` a slightly darker tone.

**Right chart.** x = day 0..T. Line of `B[t]`. A marker and label at the peak ("Peak: 57 on day 4"). A vertical guide at the ship day `S`, with the value `B[S]` labelled. A vertical guide on the left chart at the same peak day, so the student sees the two align.

**Controls.**
- Starting open bugs `B0`: slider 0 to 100, step 1, default 30.
- Day-1 find rate `f0`: slider 0 to 40, step 1, default 20.
- Daily decay `d`: slider 0.50 to 1.00, step 0.01, default 0.80.
- Fix capacity `c`: slider 1 to 20, step 1, default 8.
- Regression rate `r`: slider 0 to 0.50, step 0.05, default 0.
- Ship day `S`: slider 1 to T, default 10.
- Horizon `T`: segmented 10 / 20 / 30, default 20.
- Must-fix share `s`: slider 0.1 to 1.0, step 0.05, default 0.4, enabled only when the must-fix checkbox is on.
- "Enter my own counts" disclosure: a text field accepting comma-separated daily finds (up to 30 integers). When filled and valid, it replaces the decay formula and disables `f0` and `d`.
- Reset button.

**Readouts (live, above the table).** Peak open and peak day; open on ship day; zero day; total found; total fixed; net drain `c × (1 − r)`.

**Table.** Columns Day, Found, Regressions, Fixed, Open. Rows 0..T. Highlight the peak row and the ship-day row.

**Test values (must match exactly).**
- Defaults (`B0 = 30, f0 = 20, d = 0.8, c = 8, r = 0`): found days 1-10 `20, 16, 13, 10, 8, 7, 5, 4, 3, 3`; open days 1-10 `42, 50, 55, 57, 57, 56, 53, 49, 44, 39`; peak 57 on days 4 and 5; zero day 16.
- `r = 0.25`, rest default: open on days 4, 8, 12, 16, 20 = `63, 63, 49, 29, 6`; peak 66 on day 6; zero day 21 when `T = 30`.
- `c = 10`, rest default: peak 49 on days 3 and 4; open on day 10 = 19; zero day 13.
- Custom counts `10,8,6,4` with `B0 = 12, c = 7, T = 10`: open days 1-4 `15, 16, 15, 12`.

**Accessibility and behaviour.** All sliders keyboard operable with visible value labels. Charts have text alternatives: the readout line states peak, ship-day value and zero day in words. Respect `prefers-reduced-motion` (no animated transitions) and `prefers-color-scheme`. Use `templates/interactive-tokens.css` inline. No game art or logos.

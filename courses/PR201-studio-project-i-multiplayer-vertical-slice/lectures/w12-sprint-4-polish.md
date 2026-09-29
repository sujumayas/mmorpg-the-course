# PR201 · Week 12 — Sprint 4: Polish

**Why this matters:** Sprint 4 is the last sprint in which your team may change anything other than bugs. Every team arrives at it with a long list of things that would make the slice feel better, and every team overestimates how much of that list it will get to. The beta build at the week 13 meeting has to clear a bug bar first. This week you compute how many hours are really left for polish once that bar is paid for, then spend them on the items your playtest evidence ranks highest.

**You will be able to:**
- Compute the fix load for sprint 4 from your open bugs, your find rate, your regression rate and your average hours per fix, converted to estimated hours.
- Derive the polish budget that remains of the sprint forecast `f × U`, and fill it from a ranked list using value per estimated hour.
- Explain with numbers why lowering the regression rate is a cheaper lever than working longer hours, and why extra hours buy less polish than they seem to.
- Write a definition of done for a polish item that a tester who didn't make it can check.

**Before class:** Bring your week 11 sprint 4 input list, your tracker export (open bugs with severity and priority, plus bugs found and fixed since the week 7 playtest with the hours logged on each), your focus `f` over sprints 1 to 3 and your sprint 3 estimate ratio. Watch Martin Jonasson and Petri Purho, "Juice it or lose it" (Nordic Game Indie Night, 2012, about 15 minutes on YouTube). Reread PR101 week 10, section 2 on the backlog model (15 minutes).

**Prerequisites from earlier courses:** [PR101 week 10, bug tracking and QA basics](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md) (the backlog model and the regression rate `r`, used here without re-deriving). [PR101 week 6, estimation and why it fails](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md) (estimate ratios). [PR101 week 4, scope and cut lists](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md). [PR101 week 12, crunch](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w12-crunch-causes-costs-alternatives.md). [CS202 week 10, entity interpolation](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w10-entity-interpolation.md) (the main lever for how smooth other players look). [MA101 week 9, easing curves](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w09-easing-curves-for-animation-feel.md) (the tweens behind most "juice"). From this course, [week 6, sprint 2](w06-sprint-2-core-combat.md) (yesterday's weather) and [week 11, playtest and telemetry review](w11-playtest-and-telemetry-review.md) (the input list).

**Interactive:** [Polish budget and cut line](../examples/w12-polish-budget.html)

---

## 1. What polish means in a multiplayer slice

**Polish** is work that changes how the game feels or reads without adding a feature. It is not a synonym for "the stuff we didn't finish". In a networked vertical slice it falls into five kinds.

- **Feedback.** The game answers the player's input. Hit flashes, hit-stop (freezing both attacker and target for a few frames on impact), screen shake, impact sounds, damage numbers.
- **Clarity.** The player can tell what is happening. Telegraphs before a boss attack, a visible prompt over a downed ally, readable UI text, one colour meaning one thing.
- **Network smoothness.** Other players move without jitter or snapping. This is mostly interpolation delay and buffer tuning (CS202 week 10) and correction smoothing for your own prediction errors (CS202 week 9).
- **Audio mix.** Sounds sit at the right levels relative to each other, important cues cut through, nothing clips.
- **Consistency.** The art and UI look like one game. Placeholder assets are gone or deliberately styled.

All five share one property. Each item is small, and there is no natural end to the list. That is why polish needs a budget, not a wish list.

Sprint 4 starts under a **feature freeze**. From this meeting on, nothing new enters the game. If an item on your list adds a mechanic ("let's add a dodge roll, it would feel great"), it is a feature, and it goes on the cut list with a note for the post-mortem. The freeze is what lets next week's beta mean something.

## 2. Where polish items come from

Your sprint 4 candidates are the week 11 input list, not new ideas from this morning. Each item already has evidence, a type and a rough size. For this sprint you add three more fields.

- **Value.** A score from 1 to 10 that the team agrees in triage, anchored on the week 11 evidence. Rank first by how many players the problem touched (using the low end of the interval), then by how badly. Write the anchor down, for example "9 = touched more than a quarter of players at the low end and blocked a core action".
- **Estimate.** Hours, from the person who will do it.
- **Definition of done.** What a tester who didn't make the change will see. "Revive prompt added" is not a definition of done. "In a three-player test, a player who has never seen the game revives a downed ally within 10 seconds of the prompt appearing, without being told" is.

The last field matters more for polish than for features. A feature either works or it doesn't. A polish item can be done and change nothing a player notices. Record a short before-and-after capture for every polish item. The capture is also the best material you will have for the showcase and the post-mortem.

## 3. Worked example: the polish budget

### The hook

In 2012 Martin Jonasson and Petri Purho gave a short talk at Nordic Game Indie Night called "Juice it or lose it". They started from a plain Breakout clone and switched on small effects one at a time, such as tweened blocks (MA101 week 9), until the same game felt alive. Their project's README describes a juicy game as one that answers each small input with a cascade of responses. The talk made polish look cheap, and item by item it is.

The trap is the phrase "item by item". Tom Cargill of Bell Labs is credited with a joke that Jon Bentley printed in *Communications of the ACM* in 1985. The first 90% of the code takes the first 90% of the time, and the remaining 10% takes the other 90%. Polish lives in that second 90%, and in a team project it competes with the bug fixes that the beta bar demands. The question for sprint 4 is not "what polish would help?" It is "how many hours of polish do we actually have?"

### The model

Plan in the unit every sprint in this course has used, the estimated hour. Start from the sprint forecast, then subtract what must happen before any polish.

```
E      = f × U
F      = (B + N) / (1 − r)
H_fix  = F × h / q
H_pol  = E − O − H_fix
```

- `U` is **useful hours** for the sprint, measured the way weeks 4 and 6 did it: available hours after known absences, minus coordination.
- `f` is the team's **focus** over sprints 1 to 3, estimated hours done per useful hour (week 5). `E` is the **forecast**, the estimated hours the sprint will finish.
- `O` is **overhead tasks** at their estimates: the beta build and its checklist, the playtest you run on the build. Meetings are already in the coordination cost.
- `B` is the number of **open bugs** that must be closed before beta. In this course that is every P1 and P2 (PR101 week 10's priority scale).
- `N` is the number of **new** P1 and P2 bugs you expect testers to find during the sprint. Estimate it from recent sprints: bugs found per sprint times the share that were P1 or P2.
- `r` is the **regression rate**, the fraction of fixes that break something else (PR101 week 10). Every fix you make adds `r` new bugs on average, and those need fixing too, which is where `1 / (1 − r)` comes from: `B + N + r(B + N) + r²(B + N) + ...`.
- `h` is the average **logged hours per fix** from your tracker. Nobody estimates bug fixes in advance, so the tracker holds actual hours.
- `q` is your **estimate ratio**, actual hours over estimated hours in sprint 3. Dividing by it converts the logged fix hours into estimated hours, the unit of `E`. This is the one conversion on the sheet.
- `H_pol` is the **polish budget**, in estimated hours.

Then fill the budget. Polish items go on the sheet at their raw estimates, because `f` already carries the team's overrun. Sort by value per estimated hour, highest first. Take items in that order while they fit. Skip any item that doesn't fit and keep going, since a smaller item further down may still fit.

### Numbers you can check

The Hollowmarch team (the six-person sample team since week 1) plans sprint 4.

| Input | Value | Where it comes from |
|---|---|---|
| Useful hours `U` | 75 | 6 people × 2 weeks × 8 h = 96, minus one member's 6 h conference trip, minus 15 h coordination |
| Focus `f` | 0.532 | Sprints 1 to 3: 126 estimated hours done in 237 useful hours (weeks 5, 6 and 9) |
| Overhead tasks `O` | 5 | Beta build and checklist 3, one internal playtest 2 |
| Open P1 and P2 bugs `B` | 7 | Tracker, after week 11 triage |
| New P1 and P2 bugs `N` | 4 | 10 bugs found per sprint since week 7, 40% of them P1 or P2 |
| Regression rate `r` | 0.2 | 3 of the 15 fixes since week 7 were reopened or caused a new ticket |
| Logged hours per fix `h` | 2.4 | Mean of logged hours on those 15 fixes |
| Estimate ratio `q` | 1.3 | Sprint 3 actual hours ÷ estimated hours |

Compute. `E = 0.532 × 75 = 39.9` estimated hours. `F = (7 + 4) / 0.8 = 13.75` fixes. `H_fix = 13.75 × 2.4 / 1.3 = 25.4` estimated hours. `H_pol = 39.9 − 5 − 25.4 = 9.5`.

Nine and a half hours. The team had called sprint 4 "the polish sprint" and pictured 90 hours of it, one for every hour on the calendar. Focus takes 90 down to a forecast of 40, and fixing takes almost two thirds of that whether anyone plans it or not. A team that plans 90 hours of polish will either miss the beta bar or ship half-finished polish items, and usually both.

Now fill the 9.5 hours from the week 11 list.

| Polish item | Estimate (h) | Value | Value per hour | Running total | Decision |
|---|---|---|---|---|---|
| Revive prompt over a downed ally | 4 | 9 | 2.25 | 4 | In |
| Tutorial step 3 rewrite | 3 | 5 | 1.67 | 7 | In |
| Loot pickup sparkle and sound | 2 | 3 | 1.50 | 9 | In |
| Hit feedback: hit-stop, flash, sound | 6 | 8 | 1.33 | — | Cut, doesn't fit |
| Boss telegraph audio mix | 3 | 4 | 1.33 | — | Cut, doesn't fit |
| Remote player smoothing | 5 | 6 | 1.20 | — | Cut |
| Title music loop seam | 1 | 1 | 1.00 | — | Cut, doesn't fit |
| Menu transition tweens | 4 | 2 | 0.50 | — | Cut |

Three items, 9 estimated hours. Check two rows. Loot sparkle has value 3 and estimate 2, so `3 / 2 = 1.50`, and `7 + 2 = 9` fits in 9.5. Hit feedback has the second highest value on the list, but `9 + 6 = 15` does not fit, and neither does the title music seam at `9 + 1 = 10`. The hit feedback falls out on hours, not on value, which is the kind of result the team should argue about before accepting (see the judgment section).

A common mistake is to multiply each estimate by 1.3 "because things take longer". Then the list would need `9 × 1.3 = 11.7` hours and nothing after the revive prompt and tutorial would fit. That counts the overrun twice, once in `f` and once in the multiplier. The budget is in estimated hours, so the items go on at their estimates.

The lever that changes the answer is `r`. Rerun with other regression rates.

| Regression rate `r` | Fixes `F` | Fix estimate-hours | Polish budget | Items that fit |
|---|---|---|---|---|
| 0.1 | 12.2 | 22.6 | 12.3 | Revive prompt, tutorial, loot sparkle, boss telegraph mix |
| 0.2 | 13.8 | 25.4 | 9.5 | Revive prompt, tutorial, loot sparkle |
| 0.3 | 15.7 | 29.0 | 5.9 | Revive prompt, title music seam |

Halving `r` from 0.2 to 0.1 buys 2.8 estimated hours of polish, one more item. Raising it to 0.3 costs the tutorial and the loot sparkle. Now compare the other lever. Ten more hours of everyone's time raise `U` from 75 to 85, and the forecast by only `0.532 × 10 = 5.3` estimated hours, because extra hours land at the same focus as the rest, and tired hours at a worse one. Lowering `r` by 0.1 buys more than half of that without anyone working longer, and it keeps paying in week 14. How do you lower `r`? The same way PR101 week 10 said: someone other than the fixer verifies each fix, fixes come with a regression check, and nobody commits a fix to code they have never opened without a review. None of that is extra hours. It is how the fix hours get spent.

This script reproduces both tables. Run it with `.venv/bin/python` and replace the numbers with your team's.

```python
def polish_budget(useful, focus, overhead, known, new, r, h_logged, ratio):
    forecast = focus * useful                 # estimate-hours the sprint will finish
    fixes = (known + new) / (1 - r)
    fix_est = fixes * h_logged / ratio        # logged hours per fix, converted to estimate-hours
    return fixes, fix_est, forecast - overhead - fix_est

def fill(items, budget):
    total, plan = 0.0, []
    for name, est, value in sorted(items, key=lambda i: -i[2] / i[1]):
        keep = total + est <= budget
        total += est if keep else 0
        plan.append((name, est, keep))
    return plan, total

items = [("Revive prompt", 4, 9), ("Hit feedback", 6, 8), ("Remote smoothing", 5, 6),
         ("Tutorial step 3", 3, 5), ("Boss telegraph mix", 3, 4), ("Loot sparkle", 2, 3),
         ("Menu tweens", 4, 2), ("Title music seam", 1, 1)]
for r in (0.1, 0.2, 0.3):
    fixes, fix_est, budget = polish_budget(75, 0.532, 5, 7, 10 * 0.4, r, 2.4, 1.3)
    plan, used = fill(items, budget)
    kept = [n for n, h, k in plan if k]
    print(f"r={r}: fixes {fixes:.1f}, fix {fix_est:.1f} h, polish budget {budget:.1f} h, used {used:.1f} h")
    print("   ", ", ".join(kept))
```

It prints:

```
r=0.1: fixes 12.2, fix 22.6 h, polish budget 12.3 h, used 12.0 h
    Revive prompt, Tutorial step 3, Loot sparkle, Boss telegraph mix
r=0.2: fixes 13.8, fix 25.4 h, polish budget 9.5 h, used 9.0 h
    Revive prompt, Tutorial step 3, Loot sparkle
r=0.3: fixes 15.7, fix 29.0 h, polish budget 5.9 h, used 5.0 h
    Revive prompt, Title music seam
```

### Move it yourself

In the interactive, the top bar shows the sprint's useful hours, the part focus removes, and the forecast split into overhead, fixing and polish. The list below it shows the polish items in value-per-hour order with the cut line drawn where the budget runs out. Drag `r` from 0.1 to 0.3 and watch the fixing segment grow and the cut line climb the list. Then drag useful hours up by 10 (a teammate "finds time") and compare that with dragging `r` down by 0.1. The extra hours buy 5.3, lowering `r` buys 2.8, and only one of them costs the team sleep.

### Cross-game recognition

**The backlog model in PR101 week 10.** That model showed a team's open bug count peaking days after feature lock, and a 25% regression rate pushing the zero-bug day out further than 25% more fix capacity pulled it in. The polish budget is the same arithmetic viewed from the other side. There, regressions delayed the ship date. Here, with the date fixed, they eat the polish.

**Yesterday's weather in week 6.** Sprint 2 forecast its capacity from sprint 1's measured rate. Here `f`, `N`, `r`, `h` and the estimate ratio are all yesterday's weather. They come from the tracker and the sprint log, not from hope. If your tracker has no logged hours on fixes, `h` is a guess, and so is your polish budget.

**The ninety-ninety rule.** Cargill's joke describes the whole industry's experience that the last stretch of a project costs as much as everything before it. The formula shows one reason why. Near the end, most hours go to fixing, and every careless fix creates more.

### Eyes-open design judgment

- **Fix first, polish second, and say so in the plan.** The beta bar is not optional. Put the fix hours on the board as a block, owned by named people, before any polish item is assigned.
- **Check what the fill drops, not only what it keeps.** Hit feedback, value 8, fell out on hours. If the team believes it matters more than the loot sparkle and the tutorial rewrite together, the honest move is to raise its value against the written anchors, or to drop a lower item by hand and write down why, not to squeeze it in.
- **Low value per hour can still be right.** Remote player smoothing was cut here because the week 11 evidence gave it value 6. If your slice's players complained about other characters stuttering, it would score higher. Value comes from evidence, and the formula is only as good as the evidence behind the scores.
- **Don't split items to squeeze them in.** Half a hit-feedback pass (flash but no sound) often feels worse than none. If an item doesn't fit, cut it whole, or redefine it as a smaller item with its own definition of done.
- **More hours is the expensive lever.** Adding hours works once, lands at the team's focus or worse, and costs the team's other courses and sleep (PR101 week 12). Lowering `r` works for every remaining week, including the release candidate in week 14.

### Check this example

1. A team has `U = 70`, `f = 0.6`, `O = 4`, `B = 6`, `N = 3`, `r = 0.25`, `h = 3` logged hours and an estimate ratio of 1.5. What is the polish budget?
2. The same team gets `r` down to 0.1 by requiring a second person to verify every fix, which adds 3 estimated hours of overhead. Is it worth it?
3. A teammate says hit feedback, estimated at 6 hours, "really takes 7.8", so it needs 7.8 hours of Hollowmarch's 9.5. Is that right?

<details>
<summary>Answers</summary>

1. `E = 0.6 × 70 = 42`. `F = 9 / 0.75 = 12` fixes, `H_fix = 12 × 3 / 1.5 = 24` estimated hours, `H_pol = 42 − 4 − 24 = 14` hours.
2. `F = 9 / 0.9 = 10`, `H_fix = 20`, `H_pol = 42 − 7 − 20 = 15` hours. The 3 hours of verification buy 4 hours of fixing back, a net gain of 1 over the 14 before. Yes, narrowly this sprint, and it also lowers the number of bugs that reach beta and keeps paying in week 14.
3. No. The budget is in estimated hours, and `f` already carries the overrun. The item needs 6 of the 9.5. Charging 7.8 counts the overrun twice.

</details>

## 4. Integrating art and audio in the last sprint

Sprint 4 is often the first sprint in which final art and audio arrive in quantity, and the pipeline problems your team postponed arrive with them. Three habits keep the build stable.

- **Assets go through the same gate as code.** Every asset lands through a branch and a review, with the naming and import settings your technical design document fixed in week 3. Large binaries go through LFS as PR101 week 3 set up. A texture imported at the wrong size can cost more frame time than any bug on your list.
- **One audio mix pass, owned by one person.** Individual sounds added by different people are never balanced against each other. Schedule a single mix pass late in the sprint, after the feedback sounds are in, with the audio student setting the levels and the rest of the team testing on the same headphones.
- **Polish the networked view, not only the local one.** Every feedback item must be checked from a second client. A hit flash that plays on the attacker's screen but not on the target's is half an item. Run each check under the "campus Wi-Fi" conditions from week 6 (CS202 week 14), because feedback timed perfectly at 0 ms can arrive after the enemy has already died at 120 ms.

## 5. Running the sprint

- **Daily triage.** Fifteen minutes each working day, reading every new bug and setting its priority (PR101 week 10). New P1 and P2 bugs come out of the fix block. If the fix block runs out, the lowest polish item above the cut line moves below it. Decide that rule now, so it is not argued about on day 9.
- **Polish pairs.** Most polish items need two disciplines, a programmer and an artist for hit feedback, a designer and an audio student for telegraphs. Assign pairs, not individuals, and have the pair sign off the before-and-after capture together.
- **Freeze the list at planning.** New polish ideas that appear during the sprint go into a "post-beta" column. Some of them become known issues, some become post-mortem notes. None of them enter sprint 4.
- **Watch the burn of the fix block.** If after half the sprint more than half the fix hours are spent with fewer than half the bugs closed, your `h` or `r` was optimistic. Recompute the budget that day and move the cut line, rather than finding out at the beta review.

## Studio session plan

Week 12 meeting, 3 hours.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:15 | Briefing: feature freeze, the polish budget model, the definition of done for polish | — |
| 0:15-0:45 | Teams pull their numbers from the tracker and sprint log: `U`, `f`, `N`, `r`, `h`, estimate ratio (lab 12, part A) | Inputs in `sprint4.csv` |
| 0:45-1:10 | Compute the fix load and polish budget; run `plan_polish.py` | Budget and cut line |
| 1:10-1:20 | Break | — |
| 1:20-1:55 | Score value against the week 11 anchors; write a definition of done for every item above the line; assign pairs | Polish backlog on the board |
| 1:55-2:15 | Neighbour-team audit: the other team picks two items above the line and asks for the evidence and the done test | Audit notes |
| 2:15-2:40 | Instructor round: 5 minutes per team on the budget and the top item | Sign-off |
| 2:40-3:00 | Start the fix block: every P1 has an owner before anyone leaves | Tracker updated |

## Deliverables

Due at the end of the week 12 meeting, in `production/week12/`:

1. **Sprint 4 plan** in the lab 12 format ([`labs/lab12.md`](../labs/lab12.md)): the eight inputs with their source, the fix load, the polish budget, and the ranked polish list with the cut line. Checked by running `plan_polish.py`. It must print `PASS`.
2. **Definitions of done** for every item above the line, each one checkable by a tester who didn't make the change.

Due at the start of the week 13 meeting: the beta candidate build, tagged, plus a before-and-after capture for every completed polish item. Week 13 describes how the build is reviewed.

## Common failure modes

- **Planning 90 hours of polish.** Calendar hours are not forecast hours, and the fix block is invisible until beta week. Start from `f × U` and put the fix block on the board first.
- **Mixing units.** Logged fix hours next to estimated polish hours, or polish estimates multiplied by the ratio. Convert the fix hours once, by dividing by `q`, and leave the estimates alone.
- **Inventing `r` and `h`.** If the tracker has no logged hours, say the numbers are guesses and plan a larger margin. Better, start logging today, so week 14 has real numbers.
- **Features wearing a polish label.** "A better camera" that adds a new camera mode is a feature. The freeze applies.
- **Polish checked on one client.** Networked feedback must be checked from both sides, under latency.
- **Late assets breaking the build.** An asset that skips review is a regression waiting to happen, and it counts toward `r` like any code change.
- **Crunching the last two days.** Hours worked tired raise `r`, which the model shows is the most expensive variable. See PR101 week 12.

## Review checklist

The instructor checks, at the end of the week 12 meeting and again at beta:

- [ ] `plan_polish.py` prints `PASS` on the team's `sprint4.csv` and `polish.csv`.
- [ ] Each of `U`, `f`, `N`, `r`, `h` and the estimate ratio cites a tracker query or sprint record, or is marked as a guess.
- [ ] The fix block is on the board with named owners before any polish item.
- [ ] Every polish item above the line traces to a week 11 finding and has a checkable definition of done.
- [ ] No item above the line adds a mechanic.
- [ ] At beta: every completed polish item has a before-and-after capture; items that did not finish are listed, not half-merged.

## Sources

- Jonasson, M. & Purho, P. (2012). "Juice it or lose it." Talk at Nordic Game Indie Night, 2012. Recording on YouTube (video Fy0aCDmgnxg, uploaded by grapefrukt); the example project is the public GitHub repository grapefrukt/juicy-breakout, created May 2012, whose README says it was made for that talk.
- Bentley, J. (1985). "Programming pearls: Bumper-sticker computer science." *Communications of the ACM* 28(9), 896-901. Prints the ninety-ninety rule, attributed to Tom Cargill of Bell Labs. Attribution as summarised by Wikipedia, "Ninety-ninety rule" (read September 2026).
- The Hollowmarch sprint 4 numbers are a constructed teaching example continuing the sample team from week 1. They are not data from a real team.

## Interactive spec: examples/w12-polish-budget.html

**The one insight.** In the last sprint before beta, most of the forecast goes to fixing, and the forecast is far smaller than the calendar. Ten extra useful hours buy only `f × 10` estimated hours of polish (5.3 at the defaults), while lowering the regression rate `r` by 0.1 buys 2.8 without anyone working longer.

**Layout.** Two linked views, stacked on mobile, side by side on desktop.

1. **Hours bar (top or left).** One horizontal bar of length `U` (useful hours). Its right part, `U − E`, is drawn hatched and labelled "lost to focus". The rest, of length `E = f × U`, is split into three segments: overhead `O`, fix estimate-hours `H_fix`, polish budget `H_pol`. Label each segment with its hours. If `H_pol ≤ 0`, the polish segment disappears and a warning reads "No polish budget. The beta bar alone needs X estimated hours more than the forecast."
2. **Polish list (bottom or right).** The eight items, sorted by value per estimated hour, each as a row with a bar proportional to its estimate. Rows above the cut are filled, rows below are outlined. Draw a horizontal cut line after the last row that fits the greedy fill. A row that is skipped because it doesn't fit but has items below it that fit is marked "skipped, too big".

Above both views, large text: "Forecast: 39.9 · Fixes needed: 13.8 · Fix estimate-hours: 25.4 · Polish budget: 9.5 h · Planned: 9.0 h".

**Controls** (keyboard operable, value shown beside each, every change redraws both views immediately).

- Useful hours `U`: slider 40 to 150, step 1, default 75.
- Focus `f`: slider 0.30 to 1.00, step 0.001, default 0.532.
- Overhead tasks `O`: slider 0 to 20, step 1, default 5.
- Open P1/P2 bugs `B`: slider 0 to 40, step 1, default 7.
- New P1/P2 bugs expected `N`: slider 0 to 30, step 1, default 4.
- Regression rate `r`: slider 0 to 0.5, step 0.05, default 0.2.
- Logged hours per fix `h`: slider 0.5 to 6, step 0.1, default 2.4.
- Estimate ratio `q`: slider 1.0 to 2.0, step 0.05, default 1.3.
- Button "Compare levers": shows two ghost markers on the hours bar, the polish budget at `U + 10` and at `r − 0.1` (minimum 0), with their values printed.
- Button "Reset".
- Editable item table (collapsible) with name, estimate and value for the eight default items, so teams can enter their own list.

**Formulas.**

```
E      = f × U
F      = (B + N) / (1 − r)
H_fix  = F × h / q
H_pol  = E − O − H_fix
order: sort by value_i / estimate_i descending (stable for ties, keep table order)
greedy: running = 0; for each item in order: if running + estimate_i ≤ H_pol then keep, running += estimate_i
```

**Default items** (name, estimate h, value): Revive prompt 4, 9; Hit feedback 6, 8; Remote smoothing 5, 6; Tutorial step 3, 3, 5; Boss telegraph mix 3, 4; Loot sparkle 2, 3; Menu tweens 4, 2; Title music seam 1, 1. Ties on value per hour keep this table order, so Hit feedback sorts before Boss telegraph mix.

**Test values** (must match the guide to one decimal).

- Defaults: `E = 39.9`, `F = 13.8`, `H_fix = 25.4`, `H_pol = 9.5`, planned 9.0, kept Revive prompt, Tutorial step 3, Loot sparkle.
- `r = 0.1`: `F = 12.2`, `H_fix = 22.6`, `H_pol = 12.3`, planned 12.0, kept adds Boss telegraph mix.
- `r = 0.3`: `F = 15.7`, `H_fix = 29.0`, `H_pol = 5.9`, planned 5.0, kept Revive prompt, Title music seam.
- `U = 85`, others default: `E = 45.2`, `H_pol = 14.8`.
- Check-yourself case `U = 70, f = 0.6, O = 4, B = 6, N = 3, r = 0.25, h = 3, q = 1.5`: `H_pol = 14.0`.

**Behaviour.** The first screen shows the defaults, so the focus loss and the fix segment visibly dominate the bar. Segment widths animate over 150 ms, not at all under `prefers-reduced-motion`. Colours from `templates/interactive-tokens.css`. No game art.

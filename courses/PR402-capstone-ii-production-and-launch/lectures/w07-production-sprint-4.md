# PR402 · Week 07 — Production Sprint 4

**Why this matters:** This is the last sprint before strangers can download your game. Everything you commit to this week either works at the open-beta doors next week or becomes a known issue in front of the public. Two things make this sprint different from sprints 1 to 3. Your closed-beta server is still generating bug reports, which eat capacity you did not plan for. And this sprint ends with content lock, so anything that does not fit waits until after launch. Teams that plan sprint 4 like sprint 1 finish it with a third of the work undone and a broken open beta.

**You will be able to:**
- Compute sprint capacity from measured velocity and this week's availability, with a planning value and a conservative value.
- Reserve an interrupt buffer for incoming bug fixes, sized from the bug arrival rate you measured in the closed beta.
- Draw a cut line through a ranked backlog so the committed work fits the capacity left after the buffer.
- Read a mid-sprint burn-down that includes arriving bugs and decide on day 3 whether to cut.
- Write open-beta readiness as a sprint goal with pass or fail criteria.

**Before class:** Bring your sprint 1 to 3 velocity (points completed, not points planned), the closed-beta bug list with the date each bug was filed and whether it had to be fixed before open beta, the week 6 change log and open-beta test list, and every person's availability for this week. Re-read [PR101 week 5](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w05-agile-and-scrum-adapted-for-games.md), section 3, and [PR101 week 4](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md), section 5, on cut lists and cut triggers (20 minutes).

**Prerequisites from earlier courses:** [PR101 week 4, scope and cut lists](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md). [PR101 week 5, agile and Scrum adapted for games](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w05-agile-and-scrum-adapted-for-games.md). [PR101 week 6, estimation and why it fails](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md) (why the plan is late even when most tasks are on time). [PR101 week 7, task tracking and definitions of done](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w07-task-tracking-and-definitions-of-done.md). [PR101 week 10, bug tracking and QA basics](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md) (severity and priority). [MMO407 week 3, beta strategies](../../MMO407-launch-scaling-and-post-mortems/lectures/w03-beta-strategies.md) (what the open beta you are preparing is for). PR401 week 11, production plan, holds your original sprint plan and cut list (see the [PR401 week 11 lecture](../../PR401-capstone-i-pre-production/lectures/w11-production-plan.md)).

**Interactive:** [Sprint burn-down with an interrupt buffer](../examples/w07-sprint-buffer-burndown.html)

---

## 1. What sprint 4 is for

Sprint 4 has one goal, and you should write it down in one sentence before planning anything: **the build that opens to the public next week is stable, measurable and safe to run for a weekend.** Every item in the sprint either serves that goal or is a balance change from week 6 that must be in the open-beta build to be tested there.

That goal rules out most new features. A feature started this week gets one week of testing by your team and then meets hundreds of strangers. The Scrum Guide (2020) describes the sprint goal as the single objective of the sprint, and says scope may be clarified and renegotiated with the product owner as more is learned. Sprint 4 uses both halves of that. The goal is fixed. The list of items that serve it will shrink during the week, and that is the plan working, not failing.

Typical sprint 4 items, in rough priority order:

1. Must-fix bugs from the closed beta: every gate bug by the [week 4](w04-alpha-review-and-bug-triage.md) rule (data loss, value-path exploits, widespread S1s), then the highest impact per fix hour.
2. Open-beta readiness: sign-up and login rate limits, a login queue or cap, the load test from MMO302 week 11 at the open-beta target, a kill switch for trading, a bug report path players can find.
3. Week 6 balance changes, run through the simulator, in the build.
4. Instrumentation for the targeted tests on the week 6 open-beta test list.
5. Onboarding fixes from the closed-beta funnel.

Items 1 and 2 decide whether open beta happens. Items 3 and 4 decide whether it teaches you anything.

## 2. Capacity from what you actually finished

Your velocity is the number of points you **completed** per sprint, not the number you planned. Take the three production sprints so far and compute two numbers.

- **Planning velocity**: the mean of the three.
- **Conservative velocity**: the lowest of the three.

If you measured your ops tax each sprint ([week 1](w01-production-sprint-1-the-ops-tax.md), section 5), divide each sprint's completed points by `1 − t` first. That gives the untaxed velocity, the rate the team builds at when nothing interrupts it. The interrupt buffer in section 3 then carries this sprint's tax, so nothing is counted twice.

Then adjust both for availability. Count person-days this sprint and divide by the person-days in a normal sprint. A team of seven working a five-day sprint has 35 person-days; if one person is away for two days, availability is 33 / 35. Capacity is velocity times availability. Do not round up. PR101 week 6 showed why: estimates are skewed, so a plan that uses every point of a mean capacity is late more often than it is early.

## 3. The interrupt buffer

During sprints 1 to 3, nobody outside the team was filing bugs. Now the closed-beta server is still running, your testers are still playing, and must-fix bugs arrive while you work. Each one displaces planned work. If you plan as though they will not arrive, the sprint fails by exactly the amount of bug work that arrived.

Size the buffer from data you already have.

```
buffer = expected must-fix bugs this sprint × mean points per must-fix bug
```

Take the expected count from the closed-beta week: how many bugs filed per day were marked must-fix, times the days in this sprint, adjusted for the lower tester activity after the beta formally ended. Take the mean size from the bugs you already fixed. Then:

```
commitment = capacity − buffer
```

This is the ops tax `t` from [week 1](w01-production-sprint-1-the-ops-tax.md), measured from beta data instead of assumed: a 12-point buffer on 27 points of capacity is `t ≈ 0.44`. The buffer is not slack. If bugs arrive at the expected rate, the buffer is spent on them and the committed work still finishes. If fewer arrive, pull the next item from above the stretch line. If more arrive, section 5 tells you when to cut.

## 4. The cut line and content lock

Rank the whole candidate backlog in one list. Then walk down it, adding up points, and draw a line where the total reaches your commitment. Items above the line are the sprint. The next few items below it are the stretch list, pulled in only if the buffer is not spent. Everything else goes to one of two places:

- **Post-launch list**: work you still want, scheduled for live-ops weeks or the week 12 patch.
- **Cut list**: work you have decided not to do in this course, with one line saying why. PR101 week 4 argued that a cut list you write down is a decision, and a feature that quietly never ships is an accident.

Your feature list closed at the week 3 feature-complete gate, and anything that missed it was cut or put on a trigger list. Sprint 4 ends in **content lock**, set in [week 1](w01-production-sprint-1-the-ops-tax.md), which closes the content list too. After it, the build only receives bug fixes, balance values and polish until launch. Items that still look like features at this point (a shop screen, a new bank) are leftovers from before alpha, and they belong on the post-launch or cut list. Write the lock into your definition of done for the week (PR101 week 7). Content lock is what makes the open-beta and launch builds testable: every week you add a system is a week that system has not been tested by the public.

## 5. Worked example: capacity, buffer and cut line for sprint 4

### The hook

Amazon's New World ran its final open beta from 9 to 12 September 2021 and released on 28 September. That left 16 days between the last big test and the launch, and players were still going to arrive in numbers no beta had seen. Your gap is shorter. The closed beta ended last week, open beta is next week, and this sprint is the only one between them. The arithmetic below is how you decide what fits in it.

### The model

```
capacity    = velocity × (person-days this sprint / person-days in a normal sprint)
buffer      = expected must-fix bugs × mean points per bug
commitment  = capacity − buffer
cut line    = where the ranked backlog's running total first exceeds commitment
```

Compute it twice, with planning velocity (the mean) and conservative velocity (the minimum). Items that fit the conservative commitment are the sprint's core. Items that fit only the planning commitment are its planned edge. Items beyond it are stretch or cut.

### Numbers you can check

Emberfall, the seven-person team used as the running example in this course, completed 27, 26 and 20 story points in sprints 1 to 3, with measured ops taxes of 0.10, 0.15 and 0.25. (It sizes stories in points for planning and logs estimated and actual hours per task; [week 12](w12-patch.md) and [week 14](w14-post-mortem.md) use the hours.) One member is away for two of the five days. In the closed-beta week, testers filed 22 bugs, of which 9 were must-fix; the team expects about 8 more must-fix bugs this sprint at a mean of 1.5 points each. All values are invented teaching values.

```
untaxed velocities     = 27 / 0.90, 26 / 0.85, 20 / 0.75 = 30.0, 30.6, 26.7
planning velocity      = (30.0 + 30.6 + 26.7) / 3 = 29.1
conservative velocity  = 26.7
availability           = 33 / 35 = 0.943
planning capacity      = 29.1 × 0.943 = 27.4     → 27 points (round down)
conservative capacity  = 26.7 × 0.943 = 25.2     → 25 points
buffer                 = 8 × 1.5 = 12 points
planning commitment    = 27 − 12 = 15 points
conservative commitment = 25 − 12 = 13 points
```

The planning velocity of 29.1 is close to the 29.2 that week 1 forecast from the PR401 slice, which is a good sign for the method. The buffer works out as an ops tax of `12 / 27.4 = 0.44`, against the 0.45 week 1 planned for this week, and the commitment of 15 points sits just under week 1's 16.1. Week 1 guessed; this week measured, and the guess held.

The ranked candidate backlog, with running totals:

| Rank | Item | Points | Running total | Where it lands |
|---|---|---|---|---|
| 1 | C: crash on zone hand-off (SEV2) | 3 | 3 | core |
| 2 | B: login rate limit and queue at the cap | 5 | 8 | core |
| 3 | I: load test at 1.5 × open-beta peak target | 3 | 11 | core |
| 4 | A: Hexer damage to 77%, simulator run | 1 | 12 | core (conservative line) |
| 5 | E: in-client bug report button | 2 | 14 | planned edge |
| 6 | F: Warden and Mender kill-time instrumentation | 1 | 15 | planned edge (planning line) |
| 7 | D: tutorial step 3 rewrite | 3 | 18 | stretch |
| 8 | H: fast travel between towns | 5 | 23 | post-launch list |
| 9 | G: guild bank | 8 | 31 | post-launch list |
| 10 | J: cosmetic shop UI | 5 | 36 | cut list |

The 36 points of candidates are more than double the planning commitment. The team commits to 15 points (items C, B, I, A, E, F), holds D as stretch, and moves H, G and J off the sprint. Fast travel and the guild bank missed the week 3 feature-complete gate but still have a player case, so they go to the post-launch list; both come back as candidates for the week 12 patch. The cosmetic shop has no player case before the showcase, so it goes to the cut list with that reason. On the tracker, the six committed stories split into 14 items, and week 14's delivery record counts those 14.

Now check the buffer with a burn-down. Completion runs at `27.42 / 5 = 5.485` points a day. Bugs arrive at `8 / 5 = 1.6` a day, which is `2.4` points of new work a day. Remaining work at the end of day `d` is:

```
R(d) = commitment + 2.4 × d − 5.485 × d
```

| Commitment | Day 1 | Day 2 | Day 3 | Day 4 | Day 5 |
|---|---|---|---|---|---|
| 27 points, no buffer | 23.9 | 20.8 | 17.7 | 14.7 | **11.6** left |
| 15 points, 12-point buffer | 11.9 | 8.8 | 5.7 | 2.7 | done on day 4.86 |

Check the first row's day 5 by hand: `27 + 12 − 27.4 = 11.6`. The team that committed its full capacity ends the sprint with 11.6 points unfinished, which is 43% of its plan, even though everyone worked at their normal pace and the bugs arrived exactly as predicted. The buffered team finishes just inside the sprint. It has no spare time for stretch item D unless fewer bugs arrive than expected, which is why D is stretch and not planned.

The mid-sprint rule follows from the same line. The ideal line for a 15-point commitment falls 3 points a day, so on the evening of day 3 it sits at 6.0 points, and the model predicts 5.7. Set the cut threshold at the ideal value plus one average item, `6.0 + 3 = 9.0`. If the burn-down shows more than 9 points left on day 3, cut the lowest committed item now, while cutting it still frees time. Waiting until day 5 to cut frees nothing.

### Move it yourself

Open the [burn-down interactive](../examples/w07-sprint-buffer-burndown.html). Set the commitment to 27 and the bug arrival to 8. The line misses zero by 12 points. Drag the commitment down until the line hits zero on day 5: it lands at about 15, which is capacity minus the buffer. Then press the button, raise bug arrivals to 14 and watch the day-3 check turn red, which is the signal to cut.

### Cross-game recognition

The buffer is the sprint-sized version of ideas you have met at larger scale. PR101 week 10 modelled a bug backlog that shrinks only when the fix rate beats the arrival rate; the burn-down here is that model with planned work stacked on top. MMO308 week 1 describes live teams splitting capacity between planned content and live issues, and the same split will run your live-ops weeks. MMO302 week 13 sizes server headroom to cover the time it takes to react to load; the interrupt buffer is headroom for the team.

### Eyes-open design judgment

A buffer based on one week of closed-beta data is a guess with a number attached. It is still much better than zero, which is also a guess. Revisit it at the day-3 check. Guard against two abuses. First, a buffer is not a place to hide feature work. If nobody files bugs, pull the stretch list, not the guild bank. Second, the conservative line is not pessimism. It is the set of items that must survive any cut, so rank the list so that open-beta readiness sits above it. If the load test ranks below a cosmetic shop, the ranking is wrong, not the arithmetic.

### Check yourself

1. The away teammate is back and available all five days. Recompute planning capacity and commitment. Does stretch item D now fit?
2. By the evening of day 3, 14 must-fix bugs have arrived instead of about 5. Using the model, how many points are left, and what do you cut?
3. A teammate argues for committing 27 points "because we can always cut later". Use the burn-down to explain what cutting on day 5 costs compared with day 3.

## Studio session plan

The studio meeting runs 180 minutes with one break.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:15 | Instructor briefing: sprint goal, buffer, cut line, content lock | — |
| 0:15-0:40 | Compute capacity and buffer from your own velocity and closed-beta bug data (lab 7, part A) | Capacity sheet |
| 0:40-1:15 | Rank the full candidate backlog in one list; draw the conservative and planning lines | Ranked backlog with lines |
| 1:15-1:25 | Break | — |
| 1:25-1:50 | Write the post-launch list and the cut list with one reason each | Two lists |
| 1:50-2:20 | Write the open-beta readiness criteria as the sprint goal's pass or fail tests | Readiness checklist draft |
| 2:20-2:40 | Pair review: another team tries to find one item above your line that does not serve the goal | Review notes |
| 2:40-3:00 | Instructor walk-round and sign-off; set the day-3 cut threshold | Signed sprint plan |

## Deliverables

Due before the week 8 studio meeting, in `production/week07/`.

1. **Sprint plan** (lab 7): capacity at both velocities, buffer with its data source, commitment, ranked backlog with both lines. Checked by recomputing capacity and commitment.
2. **Daily burn-down** with arriving bugs shown as separate additions, and the day-3 check result. Checked against the tracker's history.
3. **Post-launch list and cut list**, each item with a reason.
4. **Open-beta readiness checklist**, every line a pass or fail test with the evidence attached by the end of the sprint (load-test report, rate-limit test log, kill-switch test).
5. **Content-lock statement** in the repository's `CHANGELOG` or release notes, dated.

## Common failure modes

- **Planning with planned points.** Velocity is what you finished. A team that planned 40 and finished 31 has a velocity of 31.
- **No buffer.** The sprint fails by the amount of bug work that arrived, as the worked example shows.
- **A buffer used for features.** The stretch list exists so the buffer's spare time goes to ranked work.
- **Cutting on the last day.** Cut at the day-3 check, while cutting frees time.
- **Readiness below the line.** If the load test or the login cap is not in the conservative set, the ranking is wrong.
- **Sneaking a system or a quest past the lock.** A "small" new system or quest in the week 8 build has had no testing at all.
- **Everybody on bugs.** Assign one person as the bug triager each day, so bug work flows through one queue and does not stop every task at once (PR101 week 7 on work in progress).

## Review checklist

The instructor checks, at the week 8 meeting:

- [ ] Velocity uses completed points from sprints 1 to 3, and both capacities are computed and rounded down.
- [ ] The buffer names its data source (closed-beta bug dates and sizes) and the arithmetic is correct.
- [ ] The ranked backlog puts every open-beta readiness item above the conservative line.
- [ ] The burn-down shows arriving bugs separately, and the day-3 check was run and recorded.
- [ ] Any cut made during the sprint is recorded with its day and reason.
- [ ] The cut list and post-launch list exist and every item has a reason.
- [ ] The readiness checklist has evidence for every line, or an explicit fail with a plan.
- [ ] Content lock is dated and no new system or content item appears in the week 8 build.

## Sources

- Schwaber, K. and Sutherland, J. *The Scrum Guide*, November 2020 edition (scrumguides.org, read September 2026). Sprints of one month or less; the sprint goal as the single objective of the sprint; scope clarified and renegotiated with the product owner as more is learned.
- Keith, C. (2010). *Agile Game Development with Scrum*. Addison-Wesley. Scrum practice adapted to game teams, as covered in PR101 week 5.
- Wikipedia, "New World (video game)" (read September 2026; "New World: Aeternum" redirects there). Final open beta from 9 to 12 September 2021; global release on 28 September 2021.
- Velocities, availability, bug counts and backlog items in section 5 are invented teaching values.

## Interactive spec: examples/w07-sprint-buffer-burndown.html

**Purpose.** Show that a sprint committed at full capacity fails by the amount of bug work that arrives, and that committing capacity minus the buffer finishes on time.

**The one insight.** When must-fix bugs arrive during a sprint, the remaining-work line falls at (completion rate minus bug rate), not at the completion rate. The commitment that reaches zero on the last day is capacity minus the expected bug work.

**Layout.** One chart, x axis days 0 to 5 (sprint length control can extend it to 10), y axis points remaining (0 to 45). Below it, a row of controls and a result panel. On phones the controls stack under the chart.

**Plotted series.**
- **Ideal line** (dashed, neutral): from `commitment` at day 0 to 0 at the last day.
- **Remaining work** (solid, primary): `R(d) = commitment + b × s × d / D − v_eff × d / D`, clipped at 0, where `D` is sprint length in days.
- **Bug work added** (stacked thin bars, secondary colour): cumulative `b × s × d / D` per day, so the student sees where the extra work came from.
- **Day-3 check marker**: a vertical line at `d = 3` (scaled as `round(0.6 × D)` if `D` changes) with the threshold `ideal(3) + mean item size` shown, where `ideal(3)` is the ideal line's value on day 3, as a short horizontal tick. The marker turns red when `R(3)` exceeds the threshold.

**Controls.**
- Untaxed velocity `v` (points per sprint), slider 10 to 50 step 0.1, default 29.1.
- Availability, a slider in whole person-days from 18 to 35 over a normal 35 (seven people, five days), default 33, which is 0.943.
- Commitment (points), slider 0 to 45, default 27.
- Expected must-fix bugs per sprint `b`, slider 0 to 20, default 8.
- Mean points per bug `s`, slider 0.5 to 4 step 0.5, default 1.5.
- Mean item size for the day-3 threshold, slider 1 to 8, default 3.
- Sprint length `D` in working days, select 5 or 10, default 5.
- Button "Set commitment to capacity − buffer" that sets commitment to `floor(v × availability) − b × s`.

**Derived values.** `v_eff = v × availability` (capacity). `buffer = b × s`. End-of-sprint leftover `max(0, commitment + buffer − v_eff)`. Finish day `commitment / ((v_eff − b × s) / D)` when positive, else "never".

**Result panel.** Capacity, buffer, recommended commitment `floor(v_eff) − buffer`, leftover at sprint end, finish day, and the day-3 check status (green "on track" or red "cut the lowest committed item now").

**Test values.**
- Defaults (v 29.1, availability 33/35 = 0.943, commitment 27, b 8, s 1.5, D 5): capacity 27.44, buffer 12, leftover 11.6 points, `R(3) = 17.7`, day-3 status red (ideal line at day 3 is 10.8; threshold 13.8).
- Commitment 15, other defaults: leftover 0, finish day 4.86, `R(3) = 5.7`, ideal line at day 3 is 6.0, threshold 9.0, status green.
- Button pressed with defaults: commitment becomes `27 − 12 = 15`, the same as the previous case.
- b 0: remaining line equals `commitment − 5.49 × d`; commitment 27 finishes at day 4.92.
- b 14, commitment 15: `R(3) = 15 + 12.6 − 16.5 = 11.1`; ideal line at day 3 is 6.0, threshold 9.0, status red.

**Accessibility.** All sliders keyboard operable with visible labels and current values. Status conveyed by text as well as colour. Chart has a text summary that updates with the leftover and finish day.

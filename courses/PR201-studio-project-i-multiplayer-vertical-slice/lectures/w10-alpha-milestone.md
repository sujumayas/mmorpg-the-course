# PR201 · Week 10 — Alpha Milestone

**Why this matters:** Alpha is the first milestone where the question changes from "what else can we add?" to "does what we have actually work?" A team that treats alpha as a date on the calendar arrives with a build that plays in the editor and a bug list nobody has counted. A team that treats it as a gate, with written criteria and a forecast, can tell a week in advance whether it will pass, and still has time to do something about it.

**You will be able to:**
- State alpha exit criteria for a networked slice, each with an owner and a pass condition someone else can check.
- Triage an open bug list into gate and non-gate bugs with the PR101 priority matrix.
- Forecast whether the gate bugs reach zero by the review day, and test the forecast against changes in capacity and regression rate.
- Choose between adding capacity, cutting a feature behind a flag and moving the gate, and defend the choice with numbers.

**Before class:** Reread [PR101 week 10, sections 1 and 2](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md) on the priority matrix and the backlog model, and [PR101 week 13, section 4](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w13-builds-and-release-checklists.md) on stage checklists. Bring your bug tracker export and your team's week 9 cut list.

**Prerequisites from earlier courses:** [PR101 week 10](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md) (severity, priority, the bug backlog as a stock). [PR101 week 13](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w13-builds-and-release-checklists.md) (reproducible builds, checklists with owners). [CS202 week 14](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w14-testing-under-bad-networks-netem-clumsy.md) (the network test matrix). [DB201 week 10](../../DB201-data-persistence-and-telemetry/lectures/w10-telemetry-design-events-and-properties.md) (events and the tracking plan, which week 11 will read).

---

## 1. What "alpha" means in this course

Studios use "alpha" for different things. For some it means feature complete. For others it means the whole game is playable from start to end with placeholder content. For others it is a contract milestone whose meaning is whatever the contract says. The word matters less than having written criteria before the date, so that "are we at alpha?" has an answer that does not depend on who you ask.

For PR201, alpha is reached when all seven criteria below hold on the review day.

| # | Criterion | Pass condition |
|---|---|---|
| A1 | Feature complete | Every story above the week 9 line meets the definition of done; cut stories are marked cut |
| A2 | End to end | On three machines, fresh accounts log in, play from entrance to boss kill, log out and back in with level and XP intact |
| A3 | Reproducible build | The build is made by a script from a clean checkout of a tagged commit, on a machine that is not a developer's |
| A4 | No gate bugs | Zero open P1 and P2 bugs (section 3) |
| A5 | Network matrix | All checks pass on the LAN, Good broadband and Evening Wi-Fi profiles; Mobile results recorded |
| A6 | Telemetry | Every event in the tracking plan fires at least once in an A2 run and lands where week 11 will query it |
| A7 | Content marked | Placeholder art and audio are listed, so the week 11 playtest does not report them as bugs |

Content does not have to be final. Polish is sprint 4's job. What alpha does require is that everything that will ship exists and works. After this week, the only changes are fixes, tuning and polish.

A4 is strict. Many studios allow some P2 bugs at alpha. The slice is small and beta is only three weeks away, so this course asks for zero. That makes the alpha week a **hardening sprint**, where the whole team fixes, verifies and tests instead of building.

## 2. The network matrix at alpha

A5 uses the matrix from [CS202 week 14](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w14-testing-under-bad-networks-netem-clumsy.md), applied to the whole slice instead of a toy client. You need a scripted session that three bot clients can run without a human. Join, walk to the first pack, fight, have one client disconnect and reconnect, gain a level, log out. Each run applies the checks: no crash or disconnect, health and XP agree between client and server within a second of any change, the reconnecting client sees the same world state, and bandwidth stays under your budget.

Size it before you run it. Four profiles, five seeds each, eight minutes per run:

```
runs = 4 profiles × 5 seeds = 20
time = 20 × 8 min = 160 min on one machine
```

That fits in one overnight run. It also has a limit you already know from week 7. Five seeds catch a failure that hits one run in ten with probability `1 − 0.9^5 = 0.41`. The matrix at alpha is a check for common failures. Rare ones need the longer soak run you planned in week 7, started now and read at beta.

## 3. Gate bugs and non-gate bugs

Use the priority matrix from [PR101 week 10](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md) without changes. Severity S1 to S4, frequency bands always (0), often (1) and rare (2), and

```
P = S + F − 1,  clamped to 1..4
```

For alpha, P1 and P2 bugs are **gate bugs**. They block the milestone. P3 and P4 bugs are not gate bugs. They go into sprint 4's polish backlog or the known-issues list.

The frequency band should come from evidence where you have it. The week 7 playtest gave observed frequencies for some bugs. The network matrix gives others (failed seeds divided by seeds). A bug seen once by one developer is "rare" until someone reproduces it more often.

Triage runs daily in the alpha week, 15 minutes, first thing. Read every new bug, set severity and frequency, compute priority, assign an owner. Verified fixes are closed by someone other than the fixer, as PR101 requires.

## 4. Worked example: will the gate bugs reach zero by Friday?

### The hook

*Final Fantasy XIV* ran its first closed alpha test from 11 March 2010. Its open beta, planned for 31 August, was postponed because critical bugs were found, and started on 2 September. The game went live on 30 September 2010, four weeks later. Critics praised its graphics and music and panned its interface, its pace and its many bugs. Square Enix later said more time should have been given to fixing bugs during beta. In December 2010 the producer and director were replaced, subscription fees were suspended, and the new team eventually rebuilt the game from the ground up as *A Realm Reborn* (2013).

We cannot see Square Enix's bug counts, and nothing below needs them. The pattern is the lesson. The milestone dates held while the evidence said the build was not ready. A written gate and a forecast of the bug count make that evidence hard to ignore, a week before the date instead of a month after it.

### The model

The gate bugs are a stock, as in PR101 week 10. Each day testers find new ones, some fixes cause regressions, and the team fixes as many as its capacity allows.

```
found[t]       = round( f0 × d^(t − 1) )          (half up)
regressions[t] = round( r × fixed[t − 1] )
fixed[t]       = min( c, B[t − 1] + found[t] + regressions[t] )
B[t]           = B[t − 1] + found[t] + regressions[t] − fixed[t]
```

`B[0]` is the open gate bugs on Monday morning. `f0` is the gate bugs found on day 1, and `d` is how much of each day's find rate survives to the next. `c` is gate bugs fixed per day. `r` is the share of fixes that cause a new gate bug the next day. The review is at the end of day 5. The gate passes if `B[5] = 0`.

### Numbers you can check

The *Hollowmarch* team's open bugs on the Monday of week 10:

| Bug | Summary | S | Frequency | P |
|---|---|---|---|---|
| B-31 | Server crashes when a ranged bolt hits a grunt on the tick it dies | 1 | rare (2) | 2 |
| B-32 | Client cannot rejoin after disconnecting during the boss | 1 | often (1) | 1 |
| B-33 | Boss does not reset after a party wipe | 2 | always (0) | 1 |
| B-34 | Quest XP granted twice when two players turn in on the same tick | 2 | often (1) | 2 |
| B-35 | Ranged bolt passes through grunts above 120 ms RTT | 2 | often (1) | 2 |
| B-36 | Damage number shows on a ranged miss | 3 | always (0) | 2 |
| B-37 | Level lost if the player logs out within 2 s of levelling up | 1 | rare (2) | 2 |
| B-38 | Third party member's health bar freezes after respawn | 2 | often (1) | 2 |
| B-39 | Lobby hangs when the host's window loses focus | 2 | always (0) | 1 |
| B-40 | Footstep sound late on stairs | 4 | always (0) | 3 |
| B-41 | Texture seam in room 2 | 4 | often (1) | 4 |
| B-42 | Tooltip shows old damage value | 3 | often (1) | 3 |

Check B-31. `1 + 2 − 1 = 2`, so P2. Check B-36. `3 + 0 − 1 = 2`, also P2, a minor bug that everyone sees. Nine bugs are P1 or P2, so `B[0] = 9`. B-40 to B-42 are not gate bugs.

The other inputs come from the team's records. Sprint 3's playtest and matrix runs found gate bugs at about 4 per day at first, falling fast, so `f0 = 4` and `d = 0.7`. Of sprint 3's fixes, about one in five was reopened or caused a new bug, so `r = 0.2`. In sprint 3 the team closed 12 bugs in 10 working days while spending about a third of its hours on bugs. Full time, that is `12 / 10 × 3 = 3.6` per day. The team plans with `c = 4`, and knows that is slightly optimistic.

Day by day with `c = 4`:

| Day | Found | Regressions | Fixed | Open `B` |
|---|---|---|---|---|
| 0 | | | | 9 |
| 1 | 4 | 0 | 4 | 9 |
| 2 | 3 | 1 | 4 | 9 |
| 3 | 2 | 1 | 4 | 8 |
| 4 | 1 | 1 | 4 | 6 |
| 5 | 1 | 1 | 4 | 4 |
| 6 | 1 | 1 | 4 | 2 |
| 7 | 0 | 1 | 3 | 0 |

Check day 2. Found `round(4 × 0.7) = round(2.8) = 3`, regressions `round(0.2 × 4) = round(0.8) = 1`, fixed `min(4, 9 + 3 + 1) = 4`, open `9 + 3 + 1 − 4 = 9`.

On Friday, four gate bugs are still open. The gate fails. The list reaches zero on day 7, two days late. Nobody was lazy. The team fixed four bugs every day. New bugs and regressions kept pace for the first two days.

Now test the forecast and the options. Each row changes one thing from the base case.

| Scenario | `B[0]` | `f0` | `c` | `r` | Open on day 5 | Zero on day |
|---|---|---|---|---|---|---|
| Base | 9 | 4 | 4 | 0.2 | 4 | 7 |
| Capacity is really 3.6, say 3 | 9 | 4 | 3 | 0.2 | 9 | after 8 |
| Regressions double | 9 | 4 | 4 | 0.4 | 8 | after 8 |
| One more fixer, `c = 5` | 9 | 4 | 5 | 0.2 | 0 | 5 |
| Ranged ability cut behind a flag | 6 | 3 | 4 | 0.2 | 0 | 4 |

The base case misses by four, and the forecast is fragile. If capacity is really 3 or regressions run at 0.4, the list barely shrinks all week.

Two options pass. Raising `c` from 4 to 5 means a quarter more fixing every day. The team can only find that by pulling someone off week 11's playtest preparation. It also passes on day 5 exactly, with no margin.

The second option removes the ranged ability behind a feature flag. Three gate bugs (B-31, B-35, B-36) belong to it, so `B[0]` drops to 6. With less new surface to test, the find rate drops too, estimated at `f0 = 3`. The list reaches zero on day 4, with a day of margin. The cost is design, not hours. The slice ships with melee only. The team records the ranged ability as a cut feature with its three bugs attached, to be reconsidered in PR301.

| Day | Found | Regressions | Fixed | Open `B` (ranged cut) |
|---|---|---|---|---|
| 0 | | | | 6 |
| 1 | 3 | 0 | 4 | 5 |
| 2 | 2 | 1 | 4 | 4 |
| 3 | 1 | 1 | 4 | 2 |
| 4 | 1 | 1 | 4 | 0 |

The team takes the flag, and writes down one more thing. If on Wednesday evening `B` is above 3, it asks the instructor to move its alpha review to the following Monday, and says so on Monday of week 10, not on Friday.

### Cross-game recognition

The same gate logic appears outside this course. In PR101 week 10, the stock model answered the question "when will the build be stable?" for a jam game, with *Cyberpunk 2077*'s December 2020 console launch as the hook. Here it answers a narrower question, the count of one priority class by one date. In PR101 week 13, the surgical safety checklist study (Haynes and colleagues, 2009) showed deaths falling from 1.5% to 0.8% across eight hospitals once a written checklist with a named owner for each item was used. Alpha's criteria table is the same device, applied to a build. And CS202 week 14's test matrix is a gate for netcode. A profile passes or fails on seeds, not on how the game felt in the last session someone played.

### Eyes-open judgment

The model is a forecast, not a promise. Real bugs are not all the same size. One P1 can take two days while three P2s take an hour. If one gate bug dominates, pull it out and schedule it by hand. Then model the rest.

Cutting behind a flag is cheap, but it is not free. Flagged code still compiles, still loads and can still break. Test the build with the flag off in the matrix, and remove the code before release if the feature will not return. And a cut that removes the pitch's central verb is not a bug fix. If the ranged ability were the reason the game exists, the right answer would be to move the gate and protect the feature, and to say so early.

Finally, moving the gate is a legitimate choice if it is made early and in the open. What fails is the *Final Fantasy XIV* pattern, a date held while the evidence says no.

## 5. Running the alpha week

**Monday.** Triage everything. Compute `B[0]`. Run the forecast. Decide on cuts or capacity changes that day. Start the overnight matrix.

**Tuesday to Thursday.** Daily triage at the start. Fix, verify and close. Update the forecast each evening with the real numbers, and compare against the plan.

**Wednesday evening.** The checkpoint. If `B` is above the value your forecast allows, act now. Cut, re-assign or ask to move the review.

**Thursday.** Code freeze at the end of the day. Tag the alpha candidate. Build it by script from a clean checkout. Run the A2 session on three machines and the matrix overnight.

**Friday.** The alpha review.

## Studio session plan

Week 10 meeting, 3 hours. This is the alpha review itself. Each team has 20 minutes with the instructor and a reviewer from another team.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:10 | Briefing: review order, criteria A1 to A7 on screen | |
| 0:10-2:30 | Alpha reviews, 20 minutes per team: A3 build made in front of the reviewer from the tag (5 min, started first), A2 run on three lab machines (8 min), matrix report and telemetry query (3 min), bug tracker and forecast against actuals (4 min) | Signed criteria sheet per team: pass, conditional pass or fail |
| 2:30-2:45 | Teams not reviewing: run the lab 10 checker on another team's export and compare with its claim | Cross-check notes |
| 2:45-3:00 | Instructor summary; conditional passes get their conditions and date | Conditions list |

Seven teams at 20 minutes fill 140 minutes on one station. Larger cohorts need a second station and a second reviewer.

## Deliverables

Due at the start of the week 10 review:

1. **Alpha criteria sheet** in the lab 10 format ([`labs/lab10.md`](../labs/lab10.md)): A1 to A7, each with owner, evidence and pass or fail.
2. **Bug tracker export** as CSV with severity, frequency, priority, status and owner, and the **alpha forecast**: inputs, the day-by-day table and the actual counts for each day of the week. Checked with `check_alpha.py`, which recomputes priorities, counts gate bugs and reruns the forecast.
3. **Alpha candidate build**: tagged, built by script, with the build log.
4. **Network matrix report** from the overnight run, in CS202 week 14's format.
5. **Placeholder list** for the week 11 playtest.
6. **Alpha playtest plan** for the sessions run between the alpha review and week 11. List each question the team wants answered (for example tutorial completion, disconnect rate, use of a key ability), its unit of analysis (player, party or session), the tracked event that answers it, and the threshold at which the team will act. Date the plan before any session runs. [Week 11](w11-playtest-and-telemetry-review.md) reads these thresholds and holds you to them.

A conditional pass lists the failed criteria and a date within one week to meet them. Two failed criteria, or any failed A2 or A3, is a fail. The milestone rubric in `assessments/` gives the marks.

## Common failure modes

- **Alpha as a date.** The team arrives with whatever it has. Write criteria first, and forecast them.
- **Uncounted bugs.** The tracker has 40 items, none prioritized. Triage on Monday, with the matrix.
- **Everything is P1.** When every bug is urgent, none is. Use the matrix, with frequencies from evidence.
- **Features during the hardening week.** "Just one small thing" adds surface and bugs. The week 9 freeze still holds.
- **The fixer closes the bug.** Unverified fixes come back as regressions. Someone else verifies.
- **Editor-only success.** A2 works in the editor, fails in the built game. Only the scripted build counts.
- **Late honesty.** The team knows on Wednesday that the gate will fail and says so on Friday. Say it at the checkpoint.

## Review checklist

The instructor and the reviewer check at the alpha review:

- [ ] A3: the build is produced from the tag by script during the review, on a non-developer machine.
- [ ] A2: three fresh accounts reach the boss kill and keep level and XP across logout, on three machines.
- [ ] A1: every story above the week 9 line is done; cut stories are marked.
- [ ] A4: the tracker shows zero open P1 and P2 bugs, with priorities that match the matrix; the checker agrees.
- [ ] The forecast was made on Monday, updated daily, and compared with actual counts.
- [ ] A5: the matrix report covers four profiles with at least five seeds each, and the three required profiles pass.
- [ ] A6: a query shows every tracked event from the A2 run.
- [ ] A7: placeholder assets are listed.
- [ ] The alpha playtest plan names questions, units, events and thresholds, and is dated.
- [ ] Any cut made this week is recorded with its bugs and the reason.

## Sources

- Wikipedia, "Final Fantasy XIV (2010 video game)" (accessed September 2026). First closed alpha test from 11 March 2010; open beta planned for 31 August postponed over critical bugs and started 2 September; release on 30 September 2010; critical reception; the later statement that more time should have been given to bug fixing during beta; removal of the producer and director in December 2010 and suspension of subscriptions; rebuild as *A Realm Reborn* and closure of the original servers on 11 November 2012.
- Haynes, A. B., Weiser, T. G., Berry, W. R., et al. (2009). "A surgical safety checklist to reduce morbidity and mortality in a global population." *New England Journal of Medicine* 360(5), 491-499. As cited in PR101 week 13.
- Wikipedia, "Cyberpunk 2077" (accessed September 2026), as cited in PR101 week 10. Release on 10 December 2020 and removal from the PlayStation Store on 18 December 2020.
- Keith, C. (2020). *Agile Game Development: Build, Play, Repeat* (2nd ed.). Addison-Wesley. Chapter 15, "Agile QA and Production", as cited in PR101 week 10.
- The alpha criteria, the zero-gate-bug rule and the *Hollowmarch* bug list and forecast inputs are this course's teaching conventions and invented data.

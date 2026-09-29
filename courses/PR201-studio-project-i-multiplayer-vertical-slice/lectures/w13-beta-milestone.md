# PR201 · Week 13 — Beta Milestone

**Why this matters:** Beta is the milestone where your slice stops growing. From here to the showcase you may only fix and remove things. The instructor will review your beta build from a clean download, with other people's hands on the controls. The question that decides most beta reviews is short. Will this build survive the showcase? This week turns "it didn't crash when we tried it" into a number you can defend, and shows why a one-hour playtest can't give you that number.

**You will be able to:**
- Apply your team's beta exit criteria to a build and record the evidence for each one.
- Convert a showcase reliability target into the maximum crash rate your server may have.
- Compute how many crash-free soak hours are needed to show that rate at 95% confidence, and how the answer changes after one crash.
- Plan a bot-driven soak test that runs long enough before week 15, and say what it cannot prove.

**Before class:** Your team's beta candidate build, tagged, built from a clean checkout, uploaded where the instructor can download it. Your sprint 4 before-and-after captures. Reread MA102 week 13, section 3, the part on zero events and the rule of three (10 minutes) and CS202 week 14, section 4 on a nightly network test matrix (10 minutes). NIST/SEMATECH *e-Handbook of Statistical Methods*, section 8.3.1.1, "Exponential life distribution (or HPP model) tests", the first two paragraphs and the test length table (10 minutes).

**Prerequisites from earlier courses:** [MA102 week 13, sampling](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (the rule of three for zero events). [CS202 week 13, tick rate and bandwidth budgets](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w13-tick-rate-and-bandwidth-budgets.md) and [CS202 week 14, testing under bad networks](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w14-testing-under-bad-networks-netem-clumsy.md). [PR101 week 10, bug tracking and QA basics](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md) (priority scale). [PR101 week 13, builds and release checklists](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w13-builds-and-release-checklists.md) (clean-checkout builds and coverage). [DB201 week 12, dashboards and KPIs](../../DB201-data-persistence-and-telemetry/lectures/w12-dashboards-and-kpis.md). From this course, [week 12, sprint 4](w12-sprint-4-polish.md).

**Interactive:** [Soak test planner](../examples/w13-soak-planner.html)

---

## 1. What beta means in this course

Studios define beta differently. In PR201 it means three things, and all three must hold.

- **Feature and content complete.** Everything the showcase will contain is in the build and reachable by a player. Nothing is behind a debug key.
- **No open P1 bugs, and every open P2 has an owner and a plan.** P3 and P4 bugs may remain. They go on a known issues list that the release candidate in week 14 will carry.
- **Stable enough to survive the showcase.** This is the one teams argue about, and the one this guide puts a number on.

After beta, the rules change. Every change is a fix or a removal. A fix that needs a new feature to work is a sign the feature should be removed instead. Next week, at the release candidate, the rules tighten again to fixes for blockers only.

## 2. Exit criteria, written before the review

**Exit criteria** are the conditions a build must meet to count as beta. You write them before the review, and each one names the evidence that shows it. A criterion without evidence is an opinion. Here is the course's minimum set. Your team adds rows for its own slice.

| Area | Criterion | Evidence |
|---|---|---|
| Content | Every showcase area, enemy and quest step reachable in a normal playthrough | Route checklist signed by a tester who didn't build it |
| Bugs | Zero open P1; every P2 has an owner and a target build | Tracker filter, exported with the date |
| Build | Built from a clean checkout of the tag with the export script (PR101 week 13) | Script log |
| Network | Plays through the "campus Wi-Fi" row of the week 6 conditions table with the full party | Recorded session and a note from the tester |
| Performance | Server tick time under budget at full party size (CS202 week 13); client frame time under budget on the lab machines | Profiler capture, one line per measure |
| Telemetry | The week 11 count checks still balance on the beta build | Query output |
| Stability | Showcase reliability target met, per section 3 | Soak log |

Two warnings. First, coverage beats rigor, as PR101 week 13 showed with release checklists. Seven rough checks beat three perfect ones. Second, the evidence must be from the beta build. A profiler capture from sprint 3 says nothing about the build with sprint 4's hit feedback in it.

## 3. Worked example: how long must the server run without crashing?

### The hook

Diablo III's open beta ran from 20 April to 1 May 2012. The game launched on 15 May 2012, and many players who tried to log in that night got error 37, a message that the servers were busy and they should try later. MMO407 week 1, in year 4, takes that launch apart. The part that matters here is simple. A beta tells you about what it exercised. Blizzard's open beta had real players two weeks before launch, and launch night still brought a load the servers could not take.

Your problem is a smaller version. Your team played the beta build for an hour on Tuesday, and nothing crashed. The showcase in week 15 will run your server for about two hours with strangers playing. What did Tuesday's hour tell you about the showcase?

### The model

Treat server crashes as random events that happen at a constant rate `λ` per server-hour. (This is the **Poisson process** model. MMO407 week 3 will use the same model for bugs per player-hour in a beta.) Then:

```
P(no crash in S hours) = e^(−λ × S)
```

Set a **reliability target** `R` for the showcase, the chance you want of getting through it with no server crash. Solve for the largest crash rate that meets it:

```
λ_max = −ln(R) / S
```

Now the evidence side. If you run the server for `T` hours and see zero crashes, the rule of three (MA102 week 13) says that at 95% confidence the true rate is below about `3 / T`. The exact factor is `−ln(0.05) = 2.996`, which the rule rounds to 3. To show that `λ` is below `λ_max`, you need `2.996 / T ≤ λ_max`, so:

```
T_needed = 2.996 / λ_max = 2.996 × S / (−ln R)
```

If you saw `k` crashes, replace 2.996 with the 95% upper bound for a Poisson count of `k`. The first four values are:

| Crashes seen `k` | Factor (95%) |
|---|---|
| 0 | 2.996 |
| 1 | 4.744 |
| 2 | 6.296 |
| 3 | 7.754 |

This guide, the lab script and the interactive all use these exact factors.

Every symbol again. `S` is the showcase's server-hours. `R` is your reliability target. `λ_max` is the most crashes per hour you can tolerate. `T` is the soak test's server-hours, where a **soak test** is a long run under steady load, meant to find failures that only appear with time.

### Numbers you can check

Hollowmarch's showcase runs four 30-minute sessions on one server, so `S = 2` server-hours. The team wants `R = 0.9`, a 90% chance of no server crash.

`λ_max = −ln(0.9) / 2 = 0.10536 / 2 = 0.0527` crashes per hour, about one crash per 19 hours.

`T_needed = 2.996 / 0.0527 = 56.9` crash-free server-hours.

Now read Tuesday's hour against that. One crash-free hour bounds the rate below `2.996 / 1 = 2.996` crashes per hour. At that rate, the chance of a crash-free two-hour showcase could be as low as `e^(−2.996 × 2) = 0.25%`. One quiet hour is consistent with a server that almost certainly crashes during the showcase. It proves nearly nothing.

| Crash-free hours `T` | 95% upper bound on `λ` | Worst-case `P(no crash in 2 h)` |
|---|---|---|
| 1 | 2.996 per h | 0.25% |
| 10 | 0.300 per h | 54.93% |
| 30 | 0.100 per h | 81.90% |
| 57 | 0.053 per h | 90.02% |

And the targets side by side, with zero crashes or one:

| Target `R` | `λ_max` per hour | Hours needed, 0 crashes | Hours needed, 1 crash |
|---|---|---|---|
| 0.80 | 0.1116 | 26.9 | 42.5 |
| 0.90 | 0.0527 | 56.9 | 90.1 |
| 0.95 | 0.0256 | 116.8 | 185.0 |

Check a row. For `R = 0.8`, `−ln(0.8) = 0.2231`, divided by 2 gives 0.1116. Then `2.996 / 0.1116 = 26.9` hours, and `4.744 / 0.1116 = 42.5` hours.

Fifty-seven hours sounds impossible for a student team, and with humans it is. With bots it is not. A **bot client** is a headless build of your client that logs in, joins a party, walks a scripted route, attacks and uses abilities, then does it again. Three bot clients on one lab machine, pointed at your server overnight, give about 10 server-hours a night. Six nights between now and week 15 reach 60. That is why the lab this week asks for a bot soak, not more human playtests.

This script reproduces both tables. Run it with `.venv/bin/python`.

```python
from math import exp, factorial, log

def poisson_cdf(k, mu):
    return sum(exp(-mu) * mu ** i / factorial(i) for i in range(k + 1))

def upper_count(k, conf=0.95):
    lo, hi = 0.0, 50.0
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if poisson_cdf(k, mid) > 1 - conf else (lo, mid)
    return lo

print("factors:", [round(upper_count(k), 3) for k in range(4)])
f0 = upper_count(0)
for t in (1, 10, 30, 57):
    print(f"T={t:2}  bound {f0 / t:.3f}/h  worst P(clean 2 h) {exp(-f0 / t * 2):.2%}")
for target in (0.8, 0.9, 0.95):
    lam = -log(target) / 2
    print(f"R={target}  lam_max {lam:.4f}  T0 {upper_count(0) / lam:.1f}  T1 {upper_count(1) / lam:.1f}")
```

It prints:

```
factors: [2.996, 4.744, 6.296, 7.754]
T= 1  bound 2.996/h  worst P(clean 2 h) 0.25%
T=10  bound 0.300/h  worst P(clean 2 h) 54.93%
T=30  bound 0.100/h  worst P(clean 2 h) 81.90%
T=57  bound 0.053/h  worst P(clean 2 h) 90.02%
R=0.8  lam_max 0.1116  T0 26.9  T1 42.5
R=0.9  lam_max 0.0527  T0 56.9  T1 90.1
R=0.95  lam_max 0.0256  T0 116.8  T1 185.0
```

### Move it yourself

In the interactive, the left view shows your soak evidence as a bar of crash-free hours with the 95% upper bound on the crash rate printed above it. The right view shows the showcase: 100 simulated two-hour showcases run at that worst-case rate, each a square that turns red if the server crashed. Start at one hour and watch nearly every square go red, even though your hour was clean. Drag the soak hours to 57 and watch about 90 squares turn green. Then add one crash and watch the hours needed jump to 90.

### Cross-game recognition

**Diablo III (2012).** The open beta ran with real players and still did not show that the servers could take launch night, because launch night was a different load. In the model, a soak test proves a crash rate under the load it ran. If your bots never open the inventory, the soak says nothing about inventory crashes.

**MMO betas, MMO407 week 3 (year 4).** The same rule of three will bound bug rates from a beta's player-hours, and the same catch applies. Exposure has a shape. Paths the beta rarely visits stay unbounded. Your bot route is your beta's shape, so write it to cover every system the showcase will use.

**Factory equipment acceptance.** The NIST/SEMATECH engineering statistics handbook describes reliability acceptance tests in which new equipment runs for a fixed period and passes if it fails no more than an agreed number of times. Its test-length table gives factors of 3.00, 4.74, 6.30 and 7.75 at 95% confidence for 0 to 3 allowed failures, the table above rounded to two decimals, multiplied by the mean time between failures you need to show. A 19-hour required mean time between crashes times 3 is your 57 hours. Game servers and factory tools are held to the same arithmetic.

### Eyes-open design judgment

- **Choose `R` before you soak.** A team that sees 30 clean hours and then decides 80% was the goal all along has not tested anything.
- **A crash resets more than the count.** If the soak crashes and you fix the cause, the new build is a different server. Hours on the old build say little about the new one. Restart the count on the fix build, or keep the old hours with `k = 1` only if the fix was in code the soak never exercised.
- **Bots test the bot route.** The model assumes the showcase load looks like the soak load. Add showcase actions to the route (party wipe and respawn, reconnect, the boss) and run a short human session on the same build to catch what bots can't do.
- **Client crashes count too.** The same formula applies per client-hour. Three clients for two hours is six client-hours of showcase, so client stability needs about three times the soak hours of the server at the same `R`.
- **The target is a choice, not a law.** Some teams will accept `R = 0.8` and plan a fast restart procedure for the showcase instead. That is a legitimate trade, as long as it is written down and rehearsed.

### Check this example

1. A team's showcase is one 90-minute session. For `R = 0.9`, what is `λ_max` and how many crash-free soak hours do they need?
2. A team has 40 crash-free hours. What reliability can it claim for a two-hour showcase at 95% confidence?
3. The same team's soak crashes once, at hour 25, in code a bug fix has since changed. Should they count 40 hours with `k = 1`?

<details>
<summary>Answers</summary>

1. `λ_max = 0.10536 / 1.5 = 0.0702` per hour. `T = 2.996 / 0.0702 = 42.6` hours.
2. The bound is `2.996 / 40 = 0.0749` per hour. `e^(−0.0749 × 2) = e^(−0.150) = 0.861`, so about 86%.
3. No. The crash happened in code that has changed, so the hours before the fix measured a different server. Restart the count on the fix build. If they must, they can report both numbers, but the claim for the showcase rests on the new build's hours.

</details>

## 4. The beta review

The instructor reviews every beta the same way, and your team can rehearse it.

1. **Clean download.** The instructor downloads the build from where you uploaded it, on a lab machine, and starts it without your help. If it needs a step that isn't in the README, that is a finding.
2. **Full party playthrough.** Three people, at least one from another team, play the showcase route under the "campus Wi-Fi" conditions. A team member watches in silence and takes notes as in UX201 week 8.
3. **Exit criteria walk.** The producer shows the evidence for each criterion. The instructor picks two and asks to see the raw data.
4. **Bug bash.** Fifteen minutes in which the other team tries to break the build. Every bug they find is filed in your tracker before the meeting ends, with a priority set on the spot.

A beta passes if every criterion has evidence and the playthrough reaches the end. It passes with conditions if a criterion is short but has a dated plan, for example a soak that is at 30 of 57 hours with nights booked. It fails if a P1 is open, if content is missing, or if the build can't be started from a clean download.

## Studio session plan

Week 13 meeting, 3 hours.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:15 | Briefing: exit criteria, the soak model, how the review runs | — |
| 0:15-1:15 | Beta reviews, two teams at a time in parallel with the instructor and a TA (each team 30 minutes: clean download, playthrough, criteria walk) | Review sheet per team |
| 1:15-1:25 | Break | — |
| 1:25-1:55 | Cross-team bug bash, 15 minutes each way; file every bug before swapping | Tracker updated |
| 1:55-2:25 | Soak planning (lab 13): choose `R`, compute `T_needed`, write the bot route, book machines and nights | `soak_plan.csv` passing `soak_target.py` |
| 2:25-2:50 | Triage the bug bash: set priorities, decide fix, remove or known issue | Updated known issues list |
| 2:50-3:00 | Start the first overnight soak | First soak log entry |

## Deliverables

Due at the week 13 meeting:

1. **Beta build**, tagged `v0.9.0-beta` or your team's equivalent, built from a clean checkout, uploaded before the meeting.
2. **Exit criteria sheet** with evidence for each row (lab 13, part A).

Due at the start of the week 14 meeting, in `production/week13/`:

3. **Soak plan and log** in the lab 13 format ([`labs/lab13.md`](../labs/lab13.md)). Checked by running `soak_target.py`, which must print `PASS` or `ON TRACK`.
4. **Known issues list** with every open P2, P3 and P4 bug and its planned outcome (fix in RC, leave as known issue, remove the feature).

## Common failure modes

- **"It never crashed on us."** Without hours, that sentence has no content. Log the hours.
- **Soaking the menu.** A server idling with nobody connected, or bots standing still, exposes almost nothing. The route must exercise combat, parties and the boss.
- **Evidence from an older build.** Every criterion's evidence must come from the tagged beta build or later.
- **Adding a feature to fix a bug.** After beta, a bug whose fix needs a new feature is fixed by removing the broken feature, or is shipped as a known issue.
- **Criteria written during the review.** If the criteria were not in the repository before the meeting, the review treats them as missing.
- **Skipping the clean download.** Teams that test only from the editor find out in the review that the build depends on a file that isn't in Git.

## Review checklist

The instructor checks at the week 13 review:

- [ ] The build starts from a clean download on a lab machine, following only the README.
- [ ] A full party, including a player from another team, reaches the end of the showcase route under the "campus Wi-Fi" conditions.
- [ ] Every exit criterion has evidence from the beta build; two spot-checked against raw data.
- [ ] Zero open P1 bugs in the tracker export; every P2 has an owner and a target build.
- [ ] `soak_target.py` prints `PASS` or `ON TRACK` on the team's soak plan, with `R` recorded before the first soak.
- [ ] The bot route covers every system the showcase uses, or the gaps are listed with a human test planned.
- [ ] Bug bash findings are all in the tracker with priorities.

## Sources

- Wikipedia, "Diablo III" (read September 2026). Open beta from 20 April to 1 May 2012; release on 15 May 2012; error 37 at launch with the message that the servers were busy; connection errors through May 2012.
- Hanley, J. A. & Lippman-Hand, A. (1983). "If nothing goes wrong, is everything all right? Interpreting zero numerators." *JAMA* 249(13), 1743-1745. The rule of three, via Wikipedia, "Rule of three (statistics)" (read September 2026).
- NIST/SEMATECH *e-Handbook of Statistical Methods*, section 8.3.1.1, "Exponential life distribution (or HPP model) tests" (read September 2026). Reliability acceptance tests for equipment; test-length factors 3.00, 4.74, 6.30 and 7.75 at 95% confidence for 0 to 3 allowed failures. https://www.itl.nist.gov/div898/handbook/apr/section3/apr311.htm
- The Hollowmarch showcase schedule and soak numbers are a constructed teaching example. They are not data from a real team.

## Interactive spec: examples/w13-soak-planner.html

**The one insight.** A short crash-free test proves almost nothing about a longer event. The hours of clean running you need grow with the event length and the reliability you want, and a single crash raises them by more than half.

**Layout.** Two linked views, stacked on mobile (showcase grid first), side by side on desktop.

1. **Evidence (left).** A horizontal bar showing crash-free soak hours `T` against a marker at `T_needed`. Above it, large text: "Soak: 1 h, 0 crashes. 95% bound on crash rate: 2.996 per hour." Below, "Hours needed for your target: 56.9. You have 1.8% of it."
2. **Showcase (right).** A 10 × 10 grid of squares. Each square is one simulated showcase of `S` hours run at the worst-case rate `λ_upper = factor(k) / T`. Green if no crash, red if at least one. Above it, "Worst-case P(no crash) = 0.25% (model) · 0 of 100 in this sample".

**Controls** (keyboard operable, values shown, every change redraws both views immediately).

- Soak hours `T`: slider 1 to 200, step 1, default 1.
- Crashes seen `k`: stepper 0 to 3, default 0.
- Showcase server-hours `S`: slider 0.5 to 6, step 0.5, default 2.
- Reliability target `R`: slider 0.5 to 0.99, step 0.01, default 0.90.
- Button "Jump to needed": sets `T` to `ceil(T_needed)`.
- Button "New sample": reseeds the grid simulation.
- Button "Reset".

**Formulas.**

```
factor(k)   = 2.996, 4.744, 6.296, 7.754 for k = 0..3 (exact 95% Poisson upper bound; compute by bisection or hard-code to 4 decimals)
lambda_up   = factor(k) / T
P_clean     = exp(−lambda_up × S)
lambda_max  = −ln(R) / S
T_needed    = factor(k) / lambda_max
```

Simulation: for each of 100 showcases, draw one uniform number and mark it crashed if the draw is above `P_clean`. Use a seeded PRNG (mulberry32, default seed 13). Always show the model value beside the sample count.

**Readout table** under both views: rows for `R` = 0.80, 0.90, 0.95 with columns `λ_max`, hours needed at `k = 0`, hours needed at `k = 1`, computed for the current `S`. Highlight the row nearest the current `R`.

**Test values** (must match the guide to one decimal).

- `S = 2`, `R = 0.9`: `λ_max = 0.0527`, `T_needed` 56.9 at `k = 0`, 90.1 at `k = 1`.
- `S = 2`, `R = 0.8`: 26.9 and 42.5. `R = 0.95`: 116.8 and 185.0.
- `S = 2`, `k = 0`: `T = 1` gives `P_clean` 0.25%; `T = 10` gives 54.9%; `T = 30` gives 81.9%; `T = 57` gives 90.0%.
- `S = 1.5`, `R = 0.9`, `k = 0`: `T_needed = 42.6`.
- `S = 2`, `T = 40`, `k = 0`: `P_clean` 86.1%.

**Behaviour.** The first screen shows `T = 1`, so the grid is almost all red while the evidence bar says "0 crashes". Squares fade over 150 ms, none under `prefers-reduced-motion`. Colours from `templates/interactive-tokens.css`. No game art or logos.

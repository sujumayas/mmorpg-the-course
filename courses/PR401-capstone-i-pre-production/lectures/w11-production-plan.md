# PR401 · Week 11 — Production Plan

**Why this matters:** Next semester, in PR402, your team builds and launches the game you have been designing. The production plan is the document that says who builds what, in which weeks, and what gets cut when the weeks run out. Most capstone plans add up in total and fail in one discipline. This week you find the discipline that sets your finish date before PR402 finds it for you.

**You will be able to:**
- Compute the capacity of each discipline on your team from people, weekly hours and the focus factor, and its demand from estimates and the plan ratio.
- Compute each discipline's load and identify the constraint that sets the finish date.
- Compare the four ways of relieving a constraint (move work, cut, buy, reorder) and pick the one whose cost your team can pay.
- Write a production plan for PR402 that maps every backlog item to an owner, a discipline and a milestone.

**Before class:** Bring your week 7 technical design, your week 9 content plan and your week 10 social systems plan, each with its hours estimates. Bring your week 6 fit sheet with your measured focus factor `f` and plan ratio `R`. Read the [PR402 syllabus](../../PR402-capstone-ii-production-and-launch/syllabus.md) schedule (5 minutes). Reread [PR101 week 4, section 5](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md) on ordered cut lists (15 minutes).

**Prerequisites from earlier courses:** [PR101 week 6, estimation and why it fails](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md) (the plan ratio `R`, used here without re-deriving). From this course, [week 6, greenlight review](w06-greenlight-review.md) (capacity `C = N × H × f`, demand `D = S × R` and the *Emberfall* team, all used here per discipline). [PR101 week 4, scope and cut lists](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md). [PR101 week 12, crunch](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w12-crunch-causes-costs-alternatives.md). [PR201 week 9, sprint 3 review](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w09-sprint-3-review.md) (burn-up forecasts, which you will run every PR402 sprint). [MMO403 week 13, team and budget planning](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w13-team-and-budget-planning.md) (the same plan in people-months and money). [MMO306 week 13, content budgets and cadence planning](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w13-content-budgets-and-cadence-planning.md). Your own PR301 project, whose sprint records are your best evidence of how your disciplines really perform; [PR301 week 3](../../PR301-mmo-studio-project-i-persistent-world-prototype/lectures/w03-sprint-1-world-server-and-login.md) planned by person rather than by team total, which is the same move this week makes by discipline. Looking ahead, [MMO407 week 13, launch plan workshop](../../MMO407-launch-scaling-and-post-mortems/lectures/w13-launch-plan-workshop.md) (next semester) returns to risk registers and triggers.

**Interactive:** [Discipline load model](../examples/w11-discipline-load.html). Use it during section 3.

---

## 1. What the production plan is for

A **production plan** answers one question from whoever funds the next stage. If we say go, what happens every week until launch? In this program the funder is the week 14 review panel, and the next stage is PR402. The plan has five parts.

- **The calendar.** PR402's schedule is fixed. Production sprints 1 to 3 run in weeks 1 to 3, alpha is week 4, closed beta week 5, a telemetry review week 6, sprint 4 week 7, open beta week 8 and launch week 9. After launch come about four weeks of live operation. Week 1 of this course set the production window before launch at `W = 8` weeks, PR402 weeks 1 to 8.
- **Milestone definitions.** For each milestone, a short list of what must be true, written so a tester who didn't build it can check it. "Alpha: every system in the build, every zone reachable, placeholder art allowed" is a definition. "Alpha: mostly done" is not.
- **The staffed backlog.** Every item from your technical design, content plan and social systems plan, with an hours estimate, a discipline, an owner and the milestone it belongs to.
- **The capacity check.** Proof that each discipline can do its share in the weeks it has. This is this week's worked example.
- **The cut list and the risk register.** What goes first when you are late (PR101 week 4), and the ten or so risks with a trigger and a response for each (MMO407 week 13).

The plan is not a promise that nothing will change. It is a baseline, so that when something changes in PR402 you can see what it costs.

## 2. Capacity comes from people, not from the backlog

Teams usually start a plan from the backlog. "Here is everything we want. How long will it take?" Start from the other end. Your team has a fixed number of people, each with a fixed number of hours a week for this course, and a fixed number of weeks. That is the most you can build. The backlog has to fit inside it.

Week 6 turned raw hours into real capacity with two measured numbers.

- **The focus factor `f`.** The share of scheduled hours that turns into work on estimated tasks. Meetings, reviews, builds, playtests, illness and other courses take the rest. Week 6 measured it from your PR301 log. *Emberfall*'s is 0.75.
- **The plan ratio `R`.** Estimates run over by this factor (PR101 week 6), so demand is the sum of estimates times `R`. *Emberfall*'s is 1.30.

With the PR402 convention of `H = 12` hours a week from week 1, each *Emberfall* member contributes `12 × 8 × 0.75 = 72` hours of real work before launch. Subtract known absences per person, such as a conference or a resit week, before you multiply.

Now the step that most plans skip. **Do these sums per discipline, not for the whole team.** A programmer's free hour can't model a creature, and an artist's free hour can't fix the server. If your team has three programmers, two designers, one artist and one audio and technical-art student, you have four separate capacities. The next section shows why the total hides the one that matters.

## 3. Worked example: the plan that fits in total and fails in art

### The hook

In World of Warcraft's Dungeon Finder, a five-player group needs one tank, one healer and three damage dealers. By early 2011 players who queued as damage dealers were waiting far longer than tanks and healers. The queue held plenty of players. It was short of one kind. In patch 4.1.0 (26 April 2011) Blizzard added **Call to Arms**, which gives extra rewards to whichever role is currently scarcest, usually tanks or healers. Blizzard's community manager explained the reasoning as reducing the "unacceptable" wait for damage dealers by paying the players whose role carried more responsibility to queue more often.

Notice what Blizzard did not do. It did not try to attract more damage dealers. The queue's throughput was set by the scarcest role, so the only change that shortened everyone's wait was adding capacity to that role. Your production plan works the same way. The team finishes when its most overloaded discipline finishes, however much slack the others have.

### The model

For each discipline `d`:

```
C_d = n_d × H × W × f                    capacity, hours of real work
D_d = S_d × R                            demand, estimates scaled by the plan ratio
L_d = D_d / C_d                          load
T_d = L_d × W                            weeks that discipline needs
T   = max over d of T_d                  weeks the plan needs
```

- `n_d` is the number of people in discipline `d`. A person who splits time between two disciplines counts as a fraction in each.
- `H` is hours per person per week (12 in PR402), `W` is production weeks (8), and `f` is the focus factor from week 6.
- `S_d` is the sum of estimated hours of every backlog item assigned to `d`, and `R` is the plan ratio from week 6.
- `L_d` is the **load**. At 1.0 the discipline is exactly full. Above 1.0 it is over.
- `T_d` is how many weeks the discipline needs at its capacity, and `T` is the plan's real length. The discipline with the largest load is the **constraint**.

The whole-team load is `ΣD / ΣC`, week 6's fit ratio without the risk reserve. It is the number most teams compute, and at this stage it tells you almost nothing, because it assumes any hour can do any job.

### Numbers you can check

The *Emberfall* team from week 6 has seven members: three programmers (server, gameplay, tools and UI), two designers (systems and economy, content), one artist and one student who covers audio and technical art. Week 6 already flagged the risk "art pipeline stalls (one artist, custom shaders)". Their production backlog after the greenlight cuts and the vertical slice has 310 estimated hours.

| Discipline | People `n_d` | Capacity `C_d` | Estimates `S_d` | Demand `D_d = S_d × 1.30` | Load `L_d` | Weeks needed `T_d` |
|---|---|---|---|---|---|---|
| Programming | 3 | 216 | 130 | 169 | 0.78 | 6.3 |
| Design | 2 | 144 | 80 | 104 | 0.72 | 5.8 |
| Art | 1 | 72 | 80 | 104 | 1.44 | 11.6 |
| Audio and tech art | 1 | 72 | 20 | 26 | 0.36 | 2.9 |
| **Team** | **7** | **504** | **310** | **403** | **0.80** | |

Check the art row. `C = 1 × 12 × 8 × 0.75 = 72`. `D = 80 × 1.30 = 104`. `L = 104 / 72 = 1.44`. `T = 1.44 × 8 = 11.6` weeks.

The team total says 403 hours of work in 504 hours of capacity, 80%, and even with week 6's 54-hour risk reserve on top it is 0.91. The art row says the art backlog needs almost twelve weeks and there are eight. Launch is in PR402 week 9. On this plan the towns the players fight over are grey boxes at alpha, and some are still grey at launch. Meanwhile the audio and tech-art student is at 0.36 and the programmers have about 47 hours to spare between them.

The art estimates break down like this. Three more towns at 5 hours each (15), for the four towns week 10's social plan needs (the slice town and three more), the dungeon interior (30), and class gear and creature variants (35). The town figure is a guess from the grey-box towns in the prototypes. Most of it comes from the week 9 content plan.

### Relieving the constraint

Four kinds of move bring `L_art` down. Each has a price, paid by someone else. The table works in estimated hours and multiplies by `R = 1.30` at the end.

| Move | Art estimate change | Who pays | New art load |
|---|---|---|---|
| Start | | | 1.44 (80 × 1.3 / 72) |
| **Move work.** The tech-art student takes imports, LODs and VFX for the dungeon and gear, 20 h of art estimates, at 1.5 times the artist's estimate because it is outside their main skill | −20 | Audio and tech art +30 h of estimates, load 0.36 → 0.90 | 1.08 (60 × 1.3 / 72) |
| **Buy.** A licensed modular prop kit replaces 10 h of dungeon prop modelling; integrating it costs the artist 2 h | −8 | Money, and some visual consistency | 0.94 (52 × 1.3 / 72) |
| **Cut.** Held in reserve: the second boss variant reuses the first boss's model with a new material | (−4) | The pillar that each fight reads differently now rests on animation and colour | would give 0.87 |
| **Reorder.** Put towns before creature variants, so what is late is the least visible | 0 | Nothing now; it changes what is missing if art still runs late | 0.94 |

After two moves the art load is 0.94 and audio and tech art is at 0.90. The team keeps the boss cut on the cut list instead of taking it now, because art at 0.94 has a margin of about 4 hours and the cut is the first thing to use if that margin goes. It writes "art load above 1.0 at the end of sprint 2" as the first trigger in its risk register, with the response already chosen. Take the boss cut, then re-dress an existing town instead of building the third.

Two moves are missing from the table on purpose.

- **"The artist will work more hours."** That is crunch, and PR101 week 12 put numbers on what it costs. It also doesn't scale. At 1.44 the one artist would need 44% more hours every week for eight weeks.
- **"Recruit another artist."** Fred Brooks's law, from *The Mythical Man-Month* (1975), says adding people to a late software project makes it later, because the newcomer needs teaching and every extra person adds communication paths. For a student team in week 1 of PR402 it is almost always true. A new member costs your artist hours in onboarding exactly where you have none.

### Move it yourself

In the interactive, the left view is one bar, the whole team's demand against the whole team's capacity. At the defaults it reads 80% and is coloured green. The right view has one bar per discipline, with a line at 1.0. The art bar pokes through the line to 1.44 and turns red, and a calendar strip below shows the art track ending in week 11.6 while the others end by week 7. Drag the "move work" slider and watch art fall while audio and tech art rises. Then drag it to 30 hours and watch audio and tech art become the new constraint. The left bar barely moves the whole time. Only the right view tells you anything.

### Cross-game recognition

**The Dungeon Finder, rewritten.** Groups formed per hour are `min(tanks, healers, damage dealers / 3)`, the same `max` of loads turned around. Adding damage dealers to the queue raises the whole-queue count and forms no extra groups. Call to Arms added capacity to the constraint. Your "move work" row does the same thing.

**Goldratt's theory of constraints.** Eliyahu Goldratt's business novel *The Goal* (1984) argued that every production system has at least one constraint that limits its throughput, and that improving anything else is wasted. His five focusing steps are identify the constraint, exploit it, subordinate everything else to it, elevate it, and repeat. Your table follows them. You identified art, exploited it by keeping the artist on work nobody else can do, subordinated the others by giving the tech-art student art work, elevated it by buying a kit, and would repeat if audio and tech art became the constraint.

**Your raid composition in MMO courses.** A raid that needs two tanks can't start with one, however many damage dealers are online. Guild rosters are planned per role for the same reason a production plan is planned per discipline.

Three settings, one rule. Throughput is set by the scarcest capacity, and the average hides it.

### Eyes-open design judgment

- **Plan per discipline, and per person when a discipline has one person.** If your art capacity is one student, as on *Emberfall*, their illness is a discipline outage. Name a backup for the design work that can't wait, even if the backup is slower.
- **Moving work has a conversion cost.** The 1.5 factor above is a guess. Use your own evidence. If the tech-art student did art tasks in PR301, compute their ratio on those.
- **Leave the non-constraint disciplines some slack.** A plan with every load at 1.00 has no room for the bug fixes that land on programmers after alpha (PR201 week 12 showed they eat most of the last sprint). Programming at 0.78 is not waste.
- **Cuts protect pillars or they are the wrong cuts.** Before each cut, read your pillars from week 3 aloud. If a cut removes the thing a pillar promises, find a different cut.

### Check this example

1. A team with one artist has `H = 12`, `W = 8` and a measured `f = 0.7`. What is the artist's capacity?
2. The same team's art estimates total 70 hours and its plan ratio is 1.4. What is the art load, and how many weeks does art need?
3. In *Emberfall*'s start position, the tech-art student takes 30 h of art estimates at a 1.5 conversion factor instead of 20. What happens?

<details>
<summary>Answers</summary>

1. `C = 1 × 12 × 8 × 0.7 = 67.2` hours.
2. `D = 70 × 1.4 = 98`. `L = 98 / 67.2 = 1.46`. `T = 1.46 × 8 = 11.7` weeks.
3. Art falls to `50 × 1.3 / 72 = 0.90`. Audio and tech art rises to `(20 + 45) × 1.3 / 72 = 1.17`. The constraint has moved, and the team is no better off than after the 20-hour move plus the kit. More moving is not always better.

</details>

## 4. Mapping the backlog to PR402 milestones

A plan can have every load at 1.0 or below and still fail if the work lands in the wrong order. Two checks catch that.

- **Every alpha item is in sprints 1 to 3.** Alpha in PR402 week 4 is where the whole system first runs together. Anything the alpha definition names must be scheduled in the first three sprints. Content that alpha does not need, such as the third zone's dressing or cosmetic variants, belongs in sprint 4.
- **Dependencies point backwards.** For each item, list the items it needs. The guild UI needs the guild service. A town needs the terrain export presets. If an item depends on something scheduled later, one of them moves. PR201 week 6 showed that a chain of `k` items that must all finish, each with probability `q`, finishes with probability `q^k`. Long chains across disciplines inside one sprint are the plan's weak point. Break them up with stubs, such as the client talking to a fake guild service until the real one lands.

Run the discipline load per milestone as well as for the whole production window. A discipline at 0.9 overall can be at 1.6 by the end of sprint 1 and comfortable by launch. If that happens, the sprint 1 overload is where you move or reorder work.

## 5. The plan as a document

The production plan in the pre-production package is short and mostly tables. The review panel will read it in ten minutes and question it for twenty. Include:

- The calendar mapped to PR402 weeks, with milestone definitions.
- The capacity table, with every input sourced: hours per person from your team charter, `f` and `R` from the week 6 fit sheet.
- The load table per discipline, whole window and per milestone.
- The staffed backlog as a linked spreadsheet or tracker export, not pasted in full.
- The cut list, ordered, with the hours each cut frees and the pillar it touches.
- The risk register, with a trigger and a pre-chosen response for each risk (MMO407 week 13). "Art load above 1.0 at the end of sprint 2" is a trigger. "If art falls behind" is not.

MMO403 week 13 shows how the same plan reads in money and months to an outside funder. Your panel reads hours, but it asks the same question. If one discipline slips two weeks, what does the plan do?

## Studio session plan

Week 11 meeting, 3 hours.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:15 | Briefing: the PR402 calendar, capacity per discipline, the load table | |
| 0:15-0:45 | Teams fill `team.csv`: people per discipline, hours, absences, `f` and `R` from week 6 (lab 11, part A) | Capacities |
| 0:45-1:20 | Teams merge the week 7, 9 and 10 estimates into `backlog.csv` with discipline, owner and milestone; run `check_plan.py` | First load table |
| 1:20-1:30 | Break | |
| 1:30-2:05 | Relieve the constraint: try move, buy, cut and reorder, recording each move and who pays; rerun the checker | Loads at or below 1.0 |
| 2:05-2:25 | Neighbour-team audit: the other team checks three estimates against their evidence and one dependency chain | Audit notes |
| 2:25-2:50 | Instructor round, 5 minutes per team, on the constraint and the first risk trigger | Sign-off or rework list |
| 2:50-3:00 | Assign owners for the vertical slice sprint 1 backlog (week 12) | Sprint 1 draft |

## Deliverables

Due at the start of the week 12 meeting, in `preproduction/week11/`:

1. **Production plan** (`production-plan.md`), with the five parts in section 5.
2. **`team.csv` and `backlog.csv`** in the lab 11 format ([`labs/lab11.md`](../labs/lab11.md)). Checked by running `check_plan.py`. It must print `PASS`, which means every item has an owner, a discipline and a milestone, every discipline's load is at or below 1.0 for the window and for each milestone, and no item depends on one scheduled later.
3. **Constraint log** (half a page): the starting load table, each move you made, who paid for it, and the final table.

This plan becomes part of the pre-production package reviewed in week 14 and handed in at week 15. It will change after the vertical slice sprints, and week 14 shows how.

## Common failure modes

- **Only the team total.** A plan at 80% overall with art at 144%. Compute per discipline.
- **Capacity from the calendar, not from people.** "We have eight weeks" is not a capacity. Seven people, 12 hours, eight weeks, times the focus factor, per discipline, is.
- **Estimates without the plan ratio.** Multiply by your measured `R` from week 6. Raw estimates are the plan you wish you had.
- **Moving work without a conversion cost.** The tech-art student does not model at the artist's speed.
- **Every discipline at exactly 1.00.** The first post-alpha bug wave has nowhere to go. Leave the programmers room.
- **Cutting the pillar.** The cheapest cut is often the thing that makes the game yours. Check each cut against the week 3 pillars.
- **A risk register with no triggers.** Risks with no observable trigger are never acted on.

## Review checklist

The instructor checks, at the end of the week 11 meeting and again at the week 14 review:

- [ ] `check_plan.py` prints `PASS` on the team's `team.csv` and `backlog.csv`.
- [ ] Every capacity input cites its source (charter, week 6 fit sheet, or marked assumption).
- [ ] `f` and `R` are the measured week 6 values, or the plan says why not.
- [ ] The constraint log shows the starting loads and every move, with who paid.
- [ ] No discipline is above 1.0 for the window or for any milestone.
- [ ] Every alpha-definition item is scheduled in PR402 sprints 1 to 3.
- [ ] The cut list is ordered, with hours freed and the pillar each cut touches.
- [ ] Each risk has an observable trigger and a pre-chosen response.

## Sources

- Warcraft Wiki, "Call to Arms (dungeon)" (read September 2026). Added in World of Warcraft patch 4.1.0 (26 April 2011); extra rewards to the currently least represented Dungeon Finder role, usually tanks and healers; the community manager Bashiok's explanation that it addresses the unacceptable queue times of players queueing as damage dealers. Paraphrased.
- Wikipedia, "Theory of constraints" (read September 2026). Introduced by Eliyahu M. Goldratt in *The Goal* (1984); the five focusing steps.
- Wikipedia, "Brooks's law" (read September 2026). From Fred Brooks, *The Mythical Man-Month* (1975); ramp-up time and communication overhead.
- The PR402 calendar is from this program's `curriculum.yaml`; `H = 12` and `W = 8` are the course conventions from week 1. The *Emberfall* team, its `f` and `R` (from week 6), its discipline split, estimates, conversion factor and moves are a constructed teaching example, not data from a real team.

## Interactive spec: examples/w11-discipline-load.html

**The one insight.** A plan that fits in total can fail in one discipline, and the whole-team number hides it. Moving work to relieve the constraint can create a new one.

**Layout.** Two linked views, stacked on mobile, side by side on desktop, plus a calendar strip under the right view.

1. **Team bar (left).** One horizontal bar showing `ΣD / ΣC` as a percentage, with a line at 100%. Coloured with the "ok" token below 100% and the "warning" token above.
2. **Discipline bars (right).** Four bars, one per discipline, showing `L_d`, with a vertical line at 1.0. Bars above 1.0 use the "danger" token. The constraint (largest `L_d`) is labelled "constraint".
3. **Calendar strip.** For each discipline, a bar from week 0 to `T_d`, with a vertical line at `W`. Labels show `T_d` to one decimal.

Above both, large text: "Team load 80% · Constraint: Art at 1.44 · Plan needs 11.6 weeks of 8".

**Controls** (keyboard operable, value shown beside each, every change redraws all views immediately).

- Hours per person per week `H`: slider 6 to 16, step 1, default 12.
- Weeks `W`: slider 4 to 10, step 1, default 8.
- Focus factor `f`: slider 0.5 to 1.0, step 0.05, default 0.75.
- Plan ratio `R`: slider 1.0 to 2.0, step 0.05, default 1.30.
- For each discipline, people `n_d` (0 to 4, step 0.5) and estimates `S_d` (0 to 250, step 5). Defaults: Programming 3, 130; Design 2, 80; Art 1, 80; Audio and tech art 1, 20.
- Move work: slider 0 to 40 h, step 2, default 0, with a conversion factor slider 1.0 to 2.0, step 0.1, default 1.5. Moves `x` estimated hours from Art to Audio and tech art as `x × factor`.
- Buy: checkbox "prop kit", removes 10 h of Art estimates and adds 2 h back (net −8).
- Cut: checkbox "reuse boss model", removes 4 h of Art estimates.
- Button "Reset".

**Formulas.**

```
C_d  = n_d × H × W × f
S_art   = 80 − x − (kit ? 8 : 0) − (cut ? 4 : 0)
S_audio = 20 + x × factor
D_d  = S_d × R
L_d  = D_d / C_d        (show "no capacity" if C_d = 0 and D_d > 0)
T_d  = L_d × W
team = ΣD / ΣC
```

**Test values** (must match the guide to two decimals).

- Defaults: capacity per person 72; loads 0.78, 0.72, 1.44, 0.36; `T_art = 11.56`; team 0.80.
- `x = 20`, factor 1.5: art 1.08, audio and tech art 0.90.
- Plus kit: art 0.94. Plus cut: art 0.87.
- `x = 30`, factor 1.5, no kit, no cut: art 0.90, audio and tech art 1.17, constraint label moves to Audio and tech art.
- Check-yourself case: one person, `H = 12`, `W = 8`, `f = 0.7`, `R = 1.4`, `S = 70`: `C = 67.20`, `L = 1.46`, `T = 11.67`.

**Behaviour.** The first screen shows the defaults, so the green team bar sits beside a red art bar. Bar changes animate over 150 ms, not at all under `prefers-reduced-motion`. Colours from `templates/interactive-tokens.css`. No game art or logos; disciplines are labelled in text.

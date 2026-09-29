# PR401 · Week 06 — Greenlight Review

**Why this matters:** This week a panel decides whether your capstone goes into full pre-production as pitched, goes ahead with named cuts, or goes back to the drawing board. Teams that bring enthusiasm get a vague "go" and discover in PR402 that the game never fit the team. Teams that bring a capacity calculation, a risk register and two playable prototypes get a decision they can plan against.

**You will be able to:**
- Compute your team's capacity in hours for the build window from team size, weekly hours and a measured focus factor.
- Compute a fit ratio from your feature estimates, your measured plan ratio and the expected cost of your top risks, and turn it into a go, conditional go or no-go.
- Find the plan ratio at which your plan stops fitting, and state it as a tripwire the team will watch.
- Prepare and defend a greenlight package in front of a panel, and record the decision with its conditions.

**Before class:** Reread [PR101 week 6, estimation and why it fails](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md), section 2 (the plan ratio `R` and the buffer `b = 1 − 1/R`), 20 minutes. Reread [MMO403 week 14](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w14-pitching-to-publishers-and-investors.md), section 2, on why gates that can say stop are worth money, 15 minutes. Pull every sprint's estimated and actual hours from your PR301 tracker into one sheet. Bring the prototype 1 and 2 builds and their playtest notes from weeks 4 and 5.

**Interactive:** [Greenlight fit model](../examples/w06-greenlight-fit.html). Use it during section 4.

**Prerequisites from earlier courses:** [PR101 week 4](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md) (MVP, cut lists and cut triggers). [PR101 week 6](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md) (plan ratio and buffer). [MMO403 week 13](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w13-team-and-budget-planning.md) (budgets as people-months). [MMO403 week 14](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w14-pitching-to-publishers-and-investors.md) (stage gates and kill rates). Your PR301 sprint history, sprints 1 to 5 in PR301 weeks 3 to 12, and [PR301 week 4](../../PR301-mmo-studio-project-i-persistent-world-prototype/lectures/w04-sprint-1-review.md), where you replaced a borrowed focus factor with a measured one. Looking ahead, [MMO407 week 4](../../MMO407-launch-scaling-and-post-mortems/lectures/w04-case-ffxiv-1-0-to-a-realm-reborn.md) (next semester) asks when a rebuild beats patching.

---

## 1. What a greenlight gate decides

A **greenlight** is a funding decision taken at a fixed point, called a **gate**, by people who are not on the team. In a studio the panel is a publisher, a studio head or an internal committee. In this course it is the instructor, one guest from industry when we can get one, and one member of another capstone team.

The gate has four possible outcomes. Know them before you walk in, because the panel will use exactly these words.

- **Go.** The pitch, the prototypes and the plan agree. The team starts technical design in week 7 against the pitched scope.
- **Conditional go.** The game is worth making but the plan does not fit. The team goes ahead only with named cuts or named proofs, each with a date. If a condition is not met by its date, the decision reverts to no-go on that feature.
- **Pivot.** The prototypes found something better than the pitch. The team re-pitches a changed concept in week 7 and carries on. A pivot is not a failure grade.
- **No-go.** The concept does not survive contact with the prototypes, or the plan cannot be made to fit. The team gets one week to bring a reduced pitch built from what did work.

MMO403 week 14 showed why a gate that can say stop is worth money. The stage-2 spend you save on games that were going to fail pays for the games that get through. For a student team the currency is hours, not dollars, and stage 2 is PR402. A plan that does not fit costs you the launch in week 9 of PR402, which is worth far more to your grade than any feature.

## 2. What goes in the greenlight package

The package is short. Panels read the numbers first and the prose second.

1. **The pitch on one page.** Title, one-sentence premise, the two to four pillars from week 3, target player, and the one thing a player will tell a friend. Reuse week 1 to 3 material; do not rewrite it.
2. **Prototype evidence.** For each of prototypes 1 and 2, the question it asked, what you measured, and the answer. "Prototype 1 asked whether players repeat the craft and trade loop without being told to. 5 of 8 testers made at least two voluntary craft-and-sell cycles in session 2, against a threshold of half." A prototype without a question is a demo.
3. **Market position.** Two comparable games and the one reason a player would try yours instead, from week 2.
4. **The feature list with estimates.** Every feature the pitch promises, estimated in hours at the level of detail you can defend today. Mark the MVP line from PR101 week 4.
5. **The capacity and fit calculation** from section 4, with your measured plan ratio and where it came from.
6. **The risk register.** The five biggest risks, each with a probability, a cost in hours if it happens, an owner and a trigger that says it is happening.
7. **The ordered cut list.** What goes first if the fit ratio is over 1, with the hours each cut saves.

Keep it to six pages plus the builds. Lab 06 gives the template.

## 3. How the panel scores it

The panel scores six criteria from 0 to 4. The weights are fixed for the course so that teams can see what matters.

| Criterion | Weight | A 4 looks like |
|---|---|---|
| Prototype evidence answers the pitch's riskiest question | 25% | A measured answer, with the number of testers and what would have counted as failure |
| Plan fits the team (fit ratio) | 25% | `F ≤ 1` at the team's own measured plan ratio, with the source of that ratio shown |
| Risks are named, costed and owned | 15% | Five risks, each with probability, hours, owner and a trigger that can be observed |
| Pillars drive the feature list | 15% | Every must-have feature traces to a pillar; features that trace to none are on the cut list |
| MMO scope is real | 10% | Something persists between sessions and players meet other players in a way the design depends on |
| Market position | 10% | Two named comparables and a reason to switch that a player would say out loud |

Two rules override the weighted total. A 0 on "plan fits the team" is a no-go regardless of the total, because nothing else can recover it. A 0 on "MMO scope is real" is a pivot, because the course requires it.

## 4. Worked example: does the pitch fit the team?

### The hook

Blizzard began its next MMO, codenamed Titan, around 2007. By 2013 the team had grown to about 140 people. In May 2013 Blizzard announced a reset and moved about seventy percent of the team to other projects. In September 2014 it announced that Titan was cancelled. About forty of the remaining developers had already built a prototype for a much smaller game from Titan's pieces, which shipped in May 2016 as Overwatch.

MMO403 week 14 reads this as a gate that worked: a studio that can cancel saves stage-2 money. Read it here from the team's side. The same people who could not ship Titan shipped Overwatch, with fewer of them, in about three years. The talent did not change. The fit between scope and team did. Your greenlight asks one version of that question: does the game you pitched fit the seven of you and the weeks you have?

### The model

```
hours per person H = Σ_w H_w                        scheduled hours in the build window
capacity         C = N × H × f                      hours of real work available
planned demand   D = S × R                          estimates scaled by your plan ratio
risk reserve     E = Σ p_i × L_i                    expected hours lost to risks
fit ratio        F = (D + E) / C
tripwire         R* = (C − E) / S                   the plan ratio at which F = 1
```

- `N` is the number of people on the team.
- The **build window** runs from vertical slice sprint 1 to the date strangers play the game: PR401 weeks 12 and 13 plus PR402 weeks 1 to 8.
- `H_w` is the project hours each person has in week `w`. The course convention from week 1 is 8 in PR401 and 12 in PR402, so `H = 2 × 8 + 8 × 12 = 112` hours per person. Change it only if your team agreement says otherwise, and subtract known absences.
- `f` is the **focus factor**, the share of scheduled hours that turns into work on estimated tasks. Meetings, reviews, builds, playtests, illness and other courses take the rest. Measure it from PR301: hours logged against tasks divided by hours scheduled.
- `S` is the sum of the feature estimates in hours, including the foundation work that week 3 left out of the pillar shares.
- `R` is the **plan ratio** from PR101 week 6, total actual hours over total estimated hours. Use your team's measured value from PR301 sprints. A plan ratio you did not measure is a guess, and the panel will treat it as one.
- `p_i` and `L_i` are the probability that risk `i` happens and the hours of rework it costs if it does, as in week 4. `E` is the expected rework still open after your prototypes.
- `F` above 1 means the plan does not fit. `R*` tells you how bad your estimating can get before it stops fitting.

Week 1 sized pitches with the PR201 convention: a coordination cost per channel and a flat buffer `b = 0.3`. At greenlight you replace both guesses with measurements. The focus factor `f` replaces the coordination cost, and your measured `R` replaces the buffer. The two are linked by PR101's `b = 1 − 1/R`, so week 1's buffer is the same as assuming `R = 1.43`.

The course's decision rule: `F ≤ 1.00` is a go on fit. `1.00 < F ≤ 1.15` is a conditional go, with cuts from the cut list that bring `F` to 1.00 or below, named at the meeting. `F > 1.15` is a no-go on this scope, because that much overrun cannot be recovered by trimming.

### Numbers you can check

The sample team is the seven students building *Emberfall*, the small co-op world from weeks 1 to 5, with two classes, one dungeon and a crafting and trade loop in which players hold towns. There are three programmers (server, gameplay, tools and UI), two designers (systems and economy, content), one artist, and one student who covers audio and technical art. Across their PR301 sprints they logged 1,470 task hours against 1,960 scheduled (`f = 0.75`) and spent 1,470 actual hours on tasks estimated at 1,131 (`R = 1.30`).

```
H = 2 × 8 + 8 × 12 = 112 hours per person
C = 7 × 112 × 0.75 = 588 hours
```

Their feature list is week 3's revised list plus the foundation work, which week 3 set aside:

| Feature | Pillar | Estimate (h) | After cuts (h) |
|---|---|---|---|
| Port the PR301 server: login, save, movement | foundation | 50 | 50 |
| Combat for two classes, death, and the dungeon instance | foundation | 30 | 30 |
| Gathering nodes and tools | P1 | 60 | 40 (fewer node types) |
| Crafting stations and recipes | P1 | 90 | 60 (two tiers, not three) |
| Town market stall | P1, P2 | 70 | 45 (sell only, no buy orders) |
| Town claim and shared storage | P2 | 80 | 60 (one town type, one shared chest) |
| Town siege event | P2, P3 | 60 | 30 (the smaller town raid from week 4) |
| Death drop and insurance | P3 | 40 | 25 (one insurance tier) |
| Bounty board | P3 | 45 | 30 (post and claim only) |
| Tutorial chain | P1 | 25 | 25 |
| Character customization | orphan | 20 | cut |
| **Total `S`** | | **570** | **395** |

The risk register after both prototypes, re-rated from week 4's burn-down:

| Risk | `p` | `L` (h) | `p × L` |
|---|---|---|---|
| R1 Players do not repeat the craft and trade loop | 0.1 | 200 | 20 |
| R7 Art pipeline stalls (one artist) | 0.3 | 40 | 12 |
| R3 The town raid is not fun (scoped down from the siege) | 0.2 | 40 | 8 |
| R2 Town storage fails under 60 players' writes | 0.04 | 150 | 6 |
| R5 Market UI not learnable without a tutorial | 0.2 | 30 | 6 |
| R4 Art style does not read at play distance | 0.05 | 40 | 2 |
| **`E`** | | | **54** |

Week 4 forecast that 104 hours of exposure would remain after both prototypes. The re-rated register holds 54, and the difference has causes you can name. R1's test came back clearer than planned (40 down to 20). The siege was scoped down to a town raid, so R3's loss fell to 40 hours and its exposure from 32 to 8. R2 was partly tested by prototype 2's small bot run, and R4 and R5 were re-rated from the week 5 art and UI work (9, 8 and 9 down to 6, 2 and 6). R6 left the register (6 down to 0), and R7 is new (+12). That is `104 − 20 − 24 − 3 − 6 − 3 − 6 + 12 = 54`.

R6, the claim that the team authors one play hour in 20 team hours, is closed. Its week 4 test measured 30 for a quest area, so the team re-estimated its content at the measured rate (week 9 does this for every content type), and the risk became a fact in the estimates. R7 is new: with one artist, a week of illness stops all art.

Now the fit, for the pitched scope and the cut scope, at several plan ratios:

| Plan ratio `R` | `D + E` pitched | `F` pitched | `D + E` cut | `F` cut |
|---|---|---|---|---|
| 1.00 | 624.0 | 1.06 | 449.0 | 0.76 |
| 1.20 | 738.0 | 1.26 | 528.0 | 0.90 |
| **1.30 (measured)** | **795.0** | **1.35** | **567.5** | **0.97** |
| 1.43 (week 1's `b = 0.3`) | 869.1 | 1.48 | 618.9 | 1.05 |
| 1.48 | 897.6 | 1.53 | 638.6 | 1.09 |

Check one row by hand. At `R = 1.30`, pitched: `570 × 1.30 = 741`, plus 54 is 795, and `795 / 588 = 1.352`. Cut: `395 × 1.30 = 513.5`, plus 54 is 567.5, and `567.5 / 588 = 0.965`.

And the tripwires:

```
R* pitched = (588 − 54) / 570 = 0.94
R* cut     = (588 − 54) / 395 = 1.35
```

Read it as the panel does.

- **The pitch as written cannot fit.** At the team's measured `R`, `F = 1.35`. Its tripwire is below 1, so it would not fit even if every estimate were exact. No trimming saves this plan. It needs real cuts.
- **The cut plan is a go, just.** The cuts save 175 hours and bring `F` to 0.97. The team keeps about 20 hours of capacity spare.
- **The tripwire is the condition.** The cut plan survives up to `R = 1.35`. It would fail at week 1's assumed buffer, and the 1.48 row is the no-size-rule plan ratio from PR101 week 6's cohort. If the team stops splitting tasks to 4 hours or less, it will land near that row and miss. So the panel writes the decision as a conditional go: cuts as listed, and a measured plan ratio at or below 1.35 at the end of vertical slice sprint 1 in week 12, or the next item on the cut list goes.

Notice what the panel did not do. It did not argue about whether customization is fun. The fit ratio made the conversation about which 175 hours to give back, and the pillars from week 3 decided which ones. Every cut shrinks a feature and keeps its pillar funded, except the orphan, which goes.

### Cross-game recognition

The same ratio appears whenever a team's capacity meets a promised scope.

- **Titan and Overwatch.** A reset that removes seventy percent of the people cuts `C` by seventy percent. The remaining team could only get `F` under 1 by cutting `S` far harder, to a much smaller game built from Titan's pieces. MMO403 week 14 has the gate economics.
- **Final Fantasy XIV 1.0.** MMO407 week 4 models the choice between patching the 2010 launch and rebuilding. Rewritten in this week's terms, the old code's penalty on structural fixes raised the effective `R` of every patch task so far that the rebuild was the plan with the lower `F`.
- **Your PR101 jam.** The cut line in PR101 week 4 was `P = (1 − b) × C`, planned hours at most capacity minus buffer. With `b = 1 − 1/R` that is the same statement as `S × R ≤ C`, which is `F ≤ 1` with no risk register. This week adds `E`, because a ten-week plan has room for things to go wrong that a 48-hour jam does not.

### Eyes-open judgment

`E` is an expected value, and expected values lie about single events. R1 carries 20 hours of expected rework, but its real cost is 200 hours or nothing: it is the claim that players repeat the craft and trade loop. If it fires, the cut plan's `F` becomes `(513.5 + 54 − 20 + 200) / 588 = 1.27`, and no cut list can absorb that. So R1 is not a cut-list risk. It is a pivot risk, and the decision record should say what the team pivots to if vertical slice testing shows the loop does not hold. For each large risk, check the plan against its full cost and decide whether the answer is a cut or a pivot.

The focus factor is the number teams fudge most. A team that logged 0.75 in PR301 and claims 0.9 for PR402 because "we'll be more focused" has added 20% capacity by assertion. Use the measured value, and if you believe a change will raise it, name the change.

Finally, a fit ratio says nothing about whether the game is good. A plan that fits with a pillar-free feature list is a go on fit and a pivot on design. The weights in section 3 keep the two questions apart on purpose.

## 5. Running the review

Each team gets 25 minutes. The panel has read the package in advance.

- **5 minutes: play.** A panelist plays prototype 2 while the team is silent. Do not narrate.
- **5 minutes: the numbers.** One slide with `C`, `S`, `R` and its source, `E`, `F` and the tripwire. One slide with the cut list.
- **12 minutes: questions.** Expect questions about where `R` came from, what the riskiest assumption is and what prototype 2 would have looked like if the answer had been no.
- **3 minutes: decision.** The panel confers and states the outcome, the conditions and their dates. The producer writes them into the decision record before leaving the room.

Disagree with the decision in writing within 48 hours if you have new evidence. Do not argue in the room.

## Studio session plan

Week 6 meeting, 3 hours. Four teams per room, each on the panel for one other team.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:15 | Builds installed on panel machines, packages printed, panel roles assigned | Every build starts from a clean install |
| 0:15-0:40 | Review, team 1 | Decision record 1 |
| 0:40-1:05 | Review, team 2 | Decision record 2 |
| 1:05-1:15 | Break | |
| 1:15-1:40 | Review, team 3 | Decision record 3 |
| 1:40-2:05 | Review, team 4 | Decision record 4 |
| 2:05-2:35 | Each team alone: apply the conditions, update the cut list, recompute `F` and the tripwire | Updated lab 06 sheet |
| 2:35-3:00 | Instructor round: each producer states the decision and the first date that could reverse it | Dates entered in the course calendar |

## Deliverables

Due 48 hours after the meeting, in `preproduction/week06/` in the team repository:

1. **Greenlight package** (six pages at most), with the pitch page, prototype evidence, market position, feature list, fit calculation, risk register and cut list.
2. **Fit sheet** in the [lab 06](../labs/lab06.md) format. The checker `greenlight_fit.py` must print `PASS` on your files.
3. **Decision record**: outcome, conditions, dates, and the tripwire value of `R` that reverses the decision.
4. **Updated cut list** reflecting the decision, ordered, with hours per item.

The instructor reruns the checker and compares the decision record with the panel's notes.

## Common failure modes

- **Borrowed plan ratio.** The team uses 1.0, or the textbook value, instead of its own PR301 history. The fit looks fine and fails in week 12. Show the source.
- **Capacity by optimism.** Twelve hours a week at a focus factor of 1.0 for ten weeks, with exams in the middle. Use the measured `f` and subtract known absences.
- **Risks with no cost.** "Networking might be hard" is not a risk entry. Give it a probability, hours, an owner and a trigger you can observe, like "persistence p95 write time above 50 ms at 100 bots".
- **Cut list in random order.** The first item cut should be the one furthest from the pillars, not the one the loudest person dislikes least.
- **Prototype as trailer.** The prototypes look good and answer no question. The panel scores evidence, not polish.
- **Arguing the decision in the room.** It burns the 3 minutes you need to hear the conditions.

## Review checklist

The instructor checks at the meeting and in the submission:

- [ ] The package fits in six pages and every section in section 2 is present.
- [ ] `C` uses the team's size, `H = 112` (or a stated alternative), and a focus factor with a source.
- [ ] `R` is measured from PR301 sprint data, and the sheet shows the totals it came from.
- [ ] The risk register has at least five risks, each with probability, hours, owner and trigger.
- [ ] `F` and the tripwire `R*` are computed correctly and `greenlight_fit.py` prints `PASS`.
- [ ] The largest risk's full cost is covered by the cut list.
- [ ] Each prototype states its question and a measured answer.
- [ ] The decision record lists every condition with a date and an owner.

## Sources

- Wikipedia, "Titan (cancelled video game)" (accessed September 2026). Development from about 2007, a team of about 140 by 2013, reset announced 28 May 2013 with about seventy percent of the team reassigned, cancellation disclosed by Mike Morhaime to Polygon on 23 September 2014, about forty developers building the prototype that became Overwatch (released 24 May 2016). https://en.wikipedia.org/wiki/Titan_(cancelled_video_game)
- MMO403 week 14 of this program, for Morhaime's 2019 Gamelab remark on cancellation rates and the stage-gate model.
- MMO407 week 4 of this program, for the Final Fantasy XIV 1.0 rebuild decision and its sources.
- Keith, C. (2020). *Agile Game Development: Build, Play, Repeat* (2nd ed.). Addison-Wesley. Background on stage gates and release planning in game teams.
- The *Emberfall* team, its PR301 history, foundation estimates and cuts are invented for teaching and continue weeks 1 to 5. The build window, the panel weights and the 1.15 threshold are this course's conventions, not industry standards.

## Interactive spec: examples/w06-greenlight-fit.html

**The one insight:** a plan that fits at a plan ratio of 1.0 can fail badly at the team's real ratio, and the tripwire `R*` shows how much estimating error the plan can absorb.

**Layout.** Two linked views, side by side at 1280px, stacked at 390px.

- **Left: the stacked bar.** One horizontal bar for capacity `C`. Below it, a stacked bar for demand: `S` (estimates, solid), the extra `S × (R − 1)` from the plan ratio (hatched), and `E` (a third tone). A vertical line marks `C`. When the stack passes the line, the overflow is shaded in the warning color and labelled with the hours.
- **Right: F against R.** x-axis `R` from 1.0 to 2.0. y-axis `F` from 0.5 to 2.0. Two lines: pitched scope and cut scope. Horizontal bands at 1.00 (go) and 1.15 (conditional limit). A vertical marker at the current `R`. The x-intercepts with `F = 1` are labelled as `R*` for each line.

**Controls.** Sliders for `N` (3 to 9), `H` (60 to 160 hours per person, default 112 from 2 weeks at 8 and 8 weeks at 12), `f` (0.5 to 1.0, step 0.05) and `R` (1.0 to 2.0, step 0.01). A feature table with an editable estimate and a keep checkbox per row, preloaded with the *Emberfall* list from section 4 (pitched values, with the "after cuts" values one click away). A risk table with `p` and `L` per row, preloaded with the six risks from section 4, and a "fire" toggle per risk that replaces its `p × L` with `L`.

**Readouts.** `C`, `S` kept, `D`, `E`, `F` to two decimals, `R*` to two decimals, and the verdict word (go, conditional go, no-go).

**Formulas.** `C = N × H × f`, `D = S × R`, `E = Σ p × L`, `F = (D + E) / C`, `R* = (C − E) / S`. Verdict: go if `F ≤ 1.00`, conditional go if `F ≤ 1.15`, otherwise no-go.

**Test values.** Defaults `N = 7`, `H = 112`, `f = 0.75`, `R = 1.30`, pitched list: `C = 588`, `S = 570`, `E = 54`, `F = 1.35`, `R* = 0.94`, verdict no-go. Apply the cuts: `S = 395`, `F = 0.97`, `R* = 1.35`, verdict go. Then fire R1: `E = 234`, `F = (513.5 + 234) / 588 = 1.27`, verdict no-go. Unfire R1 and set `R = 1.43`: `F = 1.05`, verdict conditional go.

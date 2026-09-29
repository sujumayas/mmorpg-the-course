# PR401 · Week 04 — Prototype 1

**Why this matters:** You have two prototype weeks before greenlight, about 45 team hours each. Teams usually spend the first one building the part of the game they are most excited about. The greenlight panel then asks about the claim the pitch depends on, and the team has no evidence. This week you choose what to prototype by how much risk each prototype removes per hour, build the first one, and bring back a result.

**You will be able to:**
- Turn load-bearing claims into a risk list with probability, cost if discovered late, and exposure.
- Compute the exposure a prototype removes per hour spent, and choose prototypes within a fixed hour budget.
- Design a prototype around one question, at the lowest fidelity that can answer it, with a kill criterion set in advance.
- Report a prototype result as evidence for or against a claim, and update the claims sheet.

**Before class:** Reread [MMO403 week 14](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w14-pitching-to-publishers-and-investors.md), section 2 (why good studios cancel half their games, 20 minutes). Reread [PR101 week 4](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md), section 4 (the vertical slice, 10 minutes), because a prototype is not one. Bring your claims sheet and your committed pillar test lines from week 3.

**Interactive:** [Prototype picker](../examples/w04-prototype-picker.html). Use it during section 2.

**Prerequisites from earlier courses:** [MMO403 week 14](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w14-pitching-to-publishers-and-investors.md) for the value of a gate, which this guide applies at the scale of one prototype. [PR101 week 6](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md) for why hour estimates run long. [UX201 week 8](../../UX201-game-ux-and-player-psychology/lectures/w08-usability-testing-methods.md) for think-aloud testing, which is how you will run most prototype sessions. [MMO302 week 11](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md) for the bot load test behind R2, and [PR301 week 3](../../PR301-mmo-studio-project-i-persistent-world-prototype/lectures/w03-sprint-1-world-server-and-login.md) for the world server code you can reuse. From this course, [week 1](w01-pitch-development.md) (claims) and [week 3](w03-pillars-and-vision.md) (pillar test lines).

---

## 1. What a prototype is for

A **prototype** is the cheapest thing you can build that answers one question about your game. It is not an early version of the game. It is an experiment, and its product is a result: evidence that a claim is true, false, or still unknown.

That definition has three consequences.

- **One question per prototype.** A prototype that tests the economy loop, the art style and the siege at once will give you three muddy answers. If you need three answers, build three small things.
- **Lowest fidelity that can answer.** Paper, a spreadsheet, a grey-box level in last year's engine, a script that spawns bots. Fidelity costs hours, and hours spent on polish are hours not spent on the next question.
- **Throwaway by default.** Prototype code skips the tests, the error handling and the architecture from your technical design. Assume none of it enters the production codebase in PR402. If some of it does, it is rewritten first.

A **vertical slice** is the opposite. It is a thin, finished strip of the real game (PR101 week 4). This course builds the slice in weeks 12 and 13, after greenlight and technical design. Building the slice now means building on claims you have not tested.

## 2. Worked example: which prototype first?

### The hook

In 2007, while Double Fine was making *Brütal Legend*, the studio started what it called Amnesia Fortnight: two weeks in which the staff stopped regular work and built game prototypes in small teams. Two prototypes from the 2009 round became *Costume Quest* (2010) and *Stacking* (2011). Tim Schafer later credited the practice with keeping the company viable through difficult publishing years.

Two weeks is also the prototype budget in this course. Double Fine's prototypes answered "is this a game we should make?" Yours must answer "which of our claims is false?" With two weeks, you cannot test every claim. You need a way to choose.

### The model

For each load-bearing claim, write a **risk** `i`:

```
E_i      = p_i × L_i                exposure: expected hours of rework
V_i      = q_i × E_i                exposure a prototype removes
ratio_i  = V_i / c_i                exposure removed per prototype hour
prototype when ratio_i ≥ 1, highest ratio first, within budget B
```

- `p_i` is the team's estimate of the probability that the claim is false.
- `L_i` is the cost in team hours if the claim turns out false during PR402 production: redesign, rework and cut content.
- `c_i` is the prototype's cost in team hours, including running the test.
- `q_i` is the share of the exposure the prototype removes. A prototype that can only answer part of the question, or whose result is noisy, has `q < 1`.
- `B` is the prototype budget. A team of seven at `H = 8` with the channel cost has `7 × (8 − 0.25 × 6) = 45.5` hours in a week. Prototype weeks are timeboxed, so no buffer is held back.

`E_i` is what Barry Boehm called **risk exposure** in his 1991 paper on software risk management. `ratio_i` has the same form as his risk reduction leverage: exposure before minus exposure after, divided by the cost of the reduction. A ratio below 1 means the prototype costs more hours than it is expected to save. For that risk, choose another response: accept it, cut the feature, or deal with it during production.

### Numbers you can check

*Emberfall*'s six load-bearing risks after week 3. The probabilities and costs are the team's estimates, argued in class for ten minutes each.

| Risk | Claim at stake | `p` | `L` (h) | `E` (h) | Prototype | `c` (h) | `q` | `V` (h) | ratio |
|---|---|---|---|---|---|---|---|---|---|
| R1 | Players repeat the craft and trade loop 3.9 times per pass | 0.5 | 200 | 100 | Spreadsheet economy run live by 8 players over 3 short sessions | 24 | 0.6 | 60 | **2.50** |
| R6 | The team authors one play hour in 20 team hours | 0.5 | 60 | 30 | Build one 15-minute quest area and time it | 10 | 0.8 | 24 | **2.40** |
| R2 | Town storage holds 60 players' writes | 0.3 | 150 | 45 | Bot load test on the PR301 server | 30 | 0.8 | 36 | **1.20** |
| R4 | The art style reads at play distance | 0.2 | 40 | 8 | Paint-over test of three screenshots | 12 | 0.9 | 7.2 | 0.60 |
| R3 | A 10 against 10 siege is fun | 0.4 | 80 | 32 | Grey-box siege with 20 testers | 40 | 0.7 | 22.4 | 0.56 |
| R5 | The market UI is learnable without a tutorial | 0.3 | 30 | 9 | Clickable mock, five think-aloud users | 16 | 0.8 | 7.2 | 0.45 |

Check R1 by hand. `E = 0.5 × 200 = 100` hours. The prototype removes `0.6 × 100 = 60` of them for 24 hours of work, so the ratio is `60 / 24 = 2.5`. Every hour spent on it is expected to save two and a half hours of PR402 rework.

**Prototype 1 (this week, `B = 45.5`).** Take R1 (24 hours) and R6 (10 hours), 34 hours in all. R2 is next in line, but it costs 30 hours and only 11.5 remain. Rather than start R2 and leave it half done, spend the spare hours on running the R1 test well, and move R2 to prototype 2.

**Prototype 2 (week 5).** R2's 30-hour bot test, plus whatever R1's result demands. Week 5 shows that a clean answer on R1 may cost more testers than the team expects.

**Not prototyped.** R3, R4 and R5 have ratios below 1. The siege is the most fun thing to build, and its prototype costs 40 hours to remove about 22 hours of expected rework. The team scopes the siege down to a smaller "town raid" in the content plan (week 9), handles R4 inside normal art work, and tests R5 with RITE usability sessions in PR402.

**The burn-down.** Total exposure starts at `100 + 30 + 45 + 8 + 32 + 9 = 224` hours. Prototype 1 is expected to remove `60 + 24 = 84`, leaving 140. Prototype 2 is expected to remove 36 more, leaving 104. The 104 is a forecast made before any prototype has run. Week 6 re-rates every risk with the actual results and carries the remaining expected rework into the greenlight fit as the risk reserve `E`. For *Emberfall* that re-rated register comes to 54 hours, and week 11 reserves the same 54 hours in the production plan. Whatever the number, it does not go away. The greenlight panel sees it as the size of the bet it is taking.

The lab 04 checker computes the table, picks prototypes within the budget, and prints the burn-down.

### The same idea elsewhere

**MMO403 week 14, the stage gate.** A gate is worth the stage-2 money a funder does not spend on games that were going to fail. A prototype is a small gate on one claim. `q` plays the part of the gate's accuracy: a noisy prototype lets bad claims through, just as a gate with a high false-go rate lets bad games through.

**Amnesia Fortnight.** Double Fine's rounds produced many prototypes and few shipped games. By the same logic, a prototype that kills a claim has done its job. The team that finds out in week 4 that its replay claim is false has saved a year of the wrong game.

**PR201 week 1.** There the constraint was discipline hours. Here it is prototype hours. In both cases the rule is to spend the scarce resource where it changes the most, and to write down what you chose not to do.

### Eyes-open judgment

Every input except `c` is a guess, and `c` itself runs long (PR101 week 6). Use the ratio to rank risks, not as a precise value. If two risks have ratios of 2.5 and 2.4, either order is fine. If one is 2.5 and another 0.5, the ranking is robust even if both are off by half.

Teams game the model in two predictable ways. They inflate `p` for the prototype they want to build, and they deflate `L` for claims they would rather not test. The fix is social, not mathematical. Each discipline's primary estimates `p` and `L` for the others' risks, not their own, and the numbers are written down before prototype choices are discussed.

The model also ignores learning. A prototype that fails in an interesting way can reveal a risk nobody listed. Leave 10 to 25% of the budget unallocated for that, as the *Emberfall* team did.

### Check yourself

1. The *Emberfall* designer argues that `p` for R3 (the siege) should be 0.8, not 0.4. Recompute its exposure and ratio. Does the siege prototype make the cut now?
2. The engineer finds a way to test R2 with 20 bots in 15 hours, which removes half its exposure (`q = 0.5`). What is the new ratio, and could it fit in prototype 1 alongside R1 and R6?

<details><summary>Answers</summary>

1. `E = 0.8 × 80 = 64`, `V = 0.7 × 64 = 44.8`, ratio `44.8 / 40 = 1.12`. It passes the ratio test, but it is still below R2 and costs 40 hours. It would not fit in prototype 1 and would compete with R2 for prototype 2. Before accepting the change, ask a different team member for their `p`.
2. `V = 0.5 × 45 = 22.5`, ratio `22.5 / 15 = 1.5`. R1 + R6 + small R2 is 49 hours, over the 45.5 budget. Either cut the R1 test to 20 hours (risking a lower `q` for R1) or keep the small R2 test for week 5.

</details>

## 3. Designing the prototype

Write a one-page **prototype brief** before anyone builds anything:

1. **The question**, copied from the claim. "Do players repeat the gather, craft and trade loop at least 3.9 times per content pass?"
2. **What you will observe.** For R1: the number of craft-and-sell cycles each player completes by choice after the scripted first one, per session.
3. **The kill criterion**, set now. "If the median player completes fewer than 2 voluntary cycles in session 2, the claim is false." This is the pillar threshold from week 3 or derived from it.
4. **Fidelity.** The lowest level that can produce the observation. R1 needs real people making real choices about prices, so it needs players. It does not need 3D art. A shared spreadsheet as the market, dice or a script for gathering, and players in the same room can run it.
5. **Cost and owner.** Hours by discipline, and one person who owns the result.
6. **What you will not build.** The list is as long as the list of what you will build.

Then build to the brief. At the midpoint, the owner asks one question: will this answer the question by the deadline? If not, cut fidelity, not the test.

## 4. Running and reporting the test

Run prototype sessions the way UX201 week 8 taught: a script, a facilitator who does not help, an observer who writes down what happens, and a short debrief. For a multiplayer prototype, observe the group as well as the individuals. Who traded with whom, who waited, who left.

Report each prototype on one page:

- **Claim and kill criterion**, as set before the test.
- **What you ran:** testers, sessions, dates, and anything that went differently from the brief.
- **Result:** the observed numbers against the criterion. Supported, refuted, or unclear.
- **What you learned that you did not ask:** new risks, surprises.
- **Claims sheet change:** which claims move from assumed to tested, and which new ones appear.

"Unclear" is a legitimate result. Eight testers can rarely settle a question about rates. Week 5 is about what to do next.

## Studio session plan

This is a build week. The studio session starts the prototype. Most of the work happens between sessions.

| Time | Activity | Output |
|---|---|---|
| 0:00 to 0:15 | Brief: prototype versus slice, the risk model, the budget | Questions answered |
| 0:15 to 0:55 | Risk estimates. Each team turns load-bearing claims into risks. Each primary estimates `p` and `L` for another discipline's risks. Numbers are written before discussion | Draft `risks.csv` |
| 0:55 to 1:15 | Ranking. Teams run the lab 04 checker and use the picker interactive to try other budgets and estimates | Prototype 1 and 2 plan |
| 1:15 to 1:25 | Break | |
| 1:25 to 2:05 | Briefs. One brief per prototype 1 item, with a kill criterion. Another team reads each brief and tries to find a result that would not clearly pass or fail | Briefs, revised |
| 2:05 to 2:50 | Build start. Teams start building. Instructor holds five-minute check-ins with each prototype owner | First build running |
| 2:50 to 3:00 | Test booking. Each team books its tester sessions for the coming week | Session calendar |

## Deliverables

Due before next week's studio session, in `preproduction/week04/` in your team repository.

- **Risk sheet** (`risks.csv`) and the checker output with the chosen prototypes and the burn-down.
- **Prototype briefs**, one per item, committed before the build started.
- **Prototype build** (or paper materials) in `prototypes/p1/`, runnable or usable by the instructor, with a README.
- **Result reports**, one page each, with raw observation notes attached.
- **Claims sheet update** with evidence levels changed.
- **Time log**: actual hours per prototype against `c`. You will need it for week 11.

See [lab 04](../labs/lab04.md).

## Common failure modes

- **Building the favourite.** The team prototypes the siege because it is fun. Fix: numbers first, written before discussion, estimated by someone other than the feature's owner.
- **Prototype as slice.** The build has menus, a login and a title screen. Fix: cut everything the question does not need. The README says what was faked.
- **No kill criterion.** The result is "players seemed to enjoy it." Fix: commit the criterion in the brief, and report the number against it.
- **The test at the end.** Building takes all 45 hours and the test is squeezed into one rushed session. Fix: book tester sessions on day one and count the test inside `c`.
- **Code carried forward.** Prototype code slides into the PR402 repository. Fix: separate directory, and a rule in the charter that prototype code is rewritten before reuse.

## Review checklist

The instructor checks prototype 1 when:

- [ ] Every load-bearing claim from the claims sheet appears in `risks.csv`.
- [ ] `p` and `L` were estimated by someone other than the risk's owner, and the file history shows numbers before choices.
- [ ] `check_risks.py` prints `PASS`, and the prototypes built match its choice or the deviation is justified in writing.
- [ ] Each brief states one question, an observable and a kill criterion, committed before the build.
- [ ] Each result report states supported, refuted or unclear against the criterion, with raw notes attached.
- [ ] The claims sheet has changed as a result.
- [ ] Actual hours are logged against `c`.

## Sources

- Wikipedia, "Amnesia Fortnight" (accessed September 2026). Double Fine; started around 2007 during the development of *Brütal Legend*; two-week prototyping in small teams; *Costume Quest* (2010) and *Stacking* (2011) prototyped in the 2009 round; Tim Schafer's remarks on keeping the company viable.
- Wikipedia, "Stacking (video game)" (read 29 September 2026). Published by THQ in February 2011 for Xbox 360 and PlayStation 3.
- Boehm, B. W. (1991). "Software risk management: principles and practices." *IEEE Software* 8(1), 32 to 41. doi:10.1109/52.62930. Risk exposure as probability times loss, and risk reduction leverage.
- MMO403 week 14 and PR101 weeks 4 and 6 in this repository.
- *Emberfall*, its risks, probabilities, costs and `q` values are invented for teaching. The prototype budget follows the course convention `H = 8` for PR401.

## Interactive spec

**File:** `examples/w04-prototype-picker.html`

**The one insight the visual must make obvious:** the prototype you most want to build is often below the break-even line, and the right choice is set by exposure removed per hour, not by exposure alone.

**Left view: risk scatter.** x axis prototype cost `c` in hours (0 to 60). y axis exposure removed `V = q × p × L` in hours (0 to 120). One labelled circle per risk, area proportional to `E = p × L`. Draw the break-even line `V = c` (ratio 1) as a dashed diagonal, labelled "saves as much as it costs". Shade the region below it lightly. Circles chosen for prototype 1 are filled with the accent colour, prototype 2 with a second colour, unchosen are outlined only.

**Right view: exposure burn-down.** Three stacked bars: "now", "after P1", "after P2". Each bar stacks the remaining exposure per risk (`E_i` now; `E_i − V_i` for prototyped risks after their prototype). Print the total above each bar.

**Controls.**
- Budget per prototype week `B`: slider 20 to 80 hours, step 0.5, default 45.5.
- For the selected risk (click a circle or choose from a list): sliders for `p` (0 to 1, step 0.05), `L` (0 to 300, step 5), `c` (1 to 80, step 1), `q` (0 to 1, step 0.05).
- Toggle "spare hours rule": when on, a risk that does not fit the remaining budget is not started (as in the guide). When off, the picker skips it and tries the next.
- Reset to the guide's values.

**Selection algorithm.** Sort risks with ratio ≥ 1 by ratio, descending. Fill prototype 1 in that order while the cumulative `c` ≤ `B`. With the spare hours rule on, stop at the first risk that does not fit and send it and the rest to prototype 2. With it off, continue down the list. Fill prototype 2 the same way with a fresh budget `B`. Risks with ratio < 1 are never selected.

**Readout table** under the views, with the columns of the guide's table (`p`, `L`, `E`, `c`, `q`, `V`, ratio, assigned to P1, P2 or none), plus the three burn-down totals.

**Test values (defaults must reproduce these).** Risks: R1 (0.5, 200, 24, 0.6), R6 (0.5, 60, 10, 0.8), R2 (0.3, 150, 30, 0.8), R4 (0.2, 40, 12, 0.9), R3 (0.4, 80, 40, 0.7), R5 (0.3, 30, 16, 0.8), given as (`p`, `L`, `c`, `q`). Ratios 2.50, 2.40, 1.20, 0.60, 0.56, 0.45. With `B = 45.5` and the spare hours rule on: P1 = R1, R6 (34 h); P2 = R2 (30 h). Burn-down totals 224, 140, 104. Setting R3 `p = 0.8` gives ratio 1.12. At `B = 45.5` with the spare hours rule on, R3 stays unassigned (P2 = R2, 30 h, and R3's 40 h do not fit in the 15.5 h left). At `B = 70`, P1 = R1, R6, R2 (64 h) and P2 = R3 (40 h).

**Accessibility.** Circles are keyboard focusable, and arrow keys move between them. Every visual state has a text equivalent in the readout table. Respect `prefers-reduced-motion` by disabling transitions.

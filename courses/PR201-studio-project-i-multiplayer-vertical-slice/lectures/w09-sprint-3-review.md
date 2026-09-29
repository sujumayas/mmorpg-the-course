# PR201 · Week 09 — Sprint 3 Review

**Why this matters:** This is the last review before the alpha milestone and the first with three sprints of data behind it. For the first time you can forecast the rest of the project from evidence instead of hope. Most teams find that the forecast and the beta date do not meet. The review is where you decide what to cut, while the cut is still a choice and not an accident.

**You will be able to:**
- Read a burn-up chart and separate the two causes of lateness, slow progress and growing scope.
- Forecast the finish of the remaining backlog as a range from three sprints of velocity and scope data.
- Compute the scope cut that makes the plan fit at a chosen confidence, and write it as an ordered cut list.
- Declare a feature freeze and explain what it changes in the forecast.

**Before class:** Export your board's history for sprints 1 to 3: for each sprint, estimated hours done and total backlog size in estimated hours at the end of the sprint. Reread [PR101 week 4, section 5](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md) on cut lists and cut triggers, and [PR101 week 9](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w09-jam-post-mortem.md) on the cone of uncertainty.

**Prerequisites from earlier courses:** [PR201 week 4](w04-sprint-1-networking-skeleton.md) (burn-up inside a sprint) and week 5 (the first forecast to a milestone, with a ±20% band). [PR101 week 5](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w05-agile-and-scrum-adapted-for-games.md) (sprint review and velocity). [PR101 week 6](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md) (why estimates run late and how skew compounds). [PR101 week 12](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w12-crunch-causes-costs-alternatives.md) (why working longer is not the fix). [GD203 week 11](../../GD203-combat-and-progression-design/lectures/w11-spreadsheet-balancing-workshop.md) (spreadsheet practice for the forecast sheet).

**Interactive:** [Release burn-up forecast and scope cut](../examples/w09-burnup-forecast.html). Use it during section 4.

---

## 1. What this review has to settle

The week 9 review has the usual jobs. Play the increment, answer the sprint goal yes or no, count the estimated hours that met the definition of done, and change the backlog. It also has one job the earlier reviews did not. It must settle the scope for alpha and beyond.

Alpha is in week 10. Week 10's guide defines it for this course, but the short version is that every feature in the slice exists and works end to end in a networked build, content may still be rough, and no known blocker bug is open. After alpha, the calendar leaves weeks 11 and 12 for playtesting, telemetry and sprint 4's polish, then beta in week 13. That is about two sprints of work time. Anything not built by then does not ship.

So the question for this review is concrete. **Does the remaining backlog fit into about two sprints, and if not, what comes out?** Three sprints of history are enough to answer it with numbers.

## 2. The release burn-up

[Week 4](w04-sprint-1-networking-skeleton.md) introduced the burn-up inside a sprint, one point per day, and showed why it can tell a slow team from a moving target when a burn-down cannot. This week you draw the same chart at release scale, one point per sprint, from week 3's plan to today. The unit is the estimated hour, as it has been all term.

- The **done line** is cumulative estimated hours of work that met the definition of done.
- The **scope line** is the total size of the backlog, done plus remaining, including everything added since week 3.

Cuts and additions are drawn differently. A cut comes off the starting point, restated back to week 3, so the scope line's slope measures only what was added. That keeps `g` in section 3 an honest growth rate, which is what a freeze stops. A cut made in week 6 that lowered the line in week 6 would look like negative growth and hide the stream of additions.

The project finishes where the lines meet. Slow progress shows as a shallow done line. Scope growth shows as a climbing scope line. Each needs a different fix. A shallow done line calls for a smaller plan or removing a blocker. A climbing scope line calls for a freeze.

Scope growth in a student studio is rarely one big addition. It is a stream of small, reasonable stories. A bug found in playtest, a missing UI screen, "the boss needs a second phase". Each is fine on its own. Together they climb at a steady rate, and after three sprints that rate is as measurable as velocity.

## 3. Forecasting with ranges

In week 5 you forecast to a milestone from one sprint, with an assumed band of ±20% around it. In week 6 you forecast one sprint with yesterday's weather. With three sprints you can replace the assumed band with a measured one. You can say how fast the team goes on a bad sprint, a typical one and a good one, and how fast scope grows.

```
v_min, v_mean, v_max = lowest, mean and highest velocity so far
g                    = (scope now − scope at first plan) / sprints so far
remaining            = scope now − done so far
capacity(N)          = N × (v − g)          for N sprints left
sprints needed       = remaining / (v − g)
cut needed           = remaining − capacity(N), if positive
```

Three data points make a thin range. Do not dress it up with decimals or false precision. The point of the range is that a plan built on `v_mean` has about even odds of fitting, and a plan built on `v_min` has much better odds. You choose which risk to take, and you write the choice down.

[PR101 week 6](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md) explained why errors in estimates are skewed toward late. The same skew applies here. The chance of a sprint much slower than `v_min` is higher than the chance of one much faster than `v_max`, because illness, exams and a broken build can all take a sprint down, and nothing takes one up by the same amount.

## 4. Worked example: the burn-up that never meets

### The hook

At E3 in June 2019, CD Projekt Red announced a release date of 16 April 2020 for *Cyberpunk 2077*. In January 2020 the studio moved it to 17 September. In June 2020 it moved to 19 November, and in October 2020 to 10 December, when the game finally shipped. Each announcement was a new forecast, and each was later than the one before.

We don't have CD Projekt's burn-up charts, and nothing below depends on them. But the pattern of three forecasts, each a little late, is exactly what a burn-up produces when a team forecasts from its done line and ignores its scope line. Every sprint, the finish looks a couple of sprints away, and every sprint it moves. Your team can see the same pattern in its own data after three sprints, and act on it in week 9 instead of week 13.

### The model

The model is the forecast from section 3, drawn on the burn-up. Extend the done line forward at velocity `v`. Extend the scope line forward at growth `g`. They meet after `remaining / (v − g)` sprints. If that is more than `N`, the sprints left, then the plan does not fit and the gap at sprint `N` is the cut.

A **feature freeze** sets `g = 0` from now on. Only bugs found in testing and stories already on the list may be worked. It is the only lever that changes the scope line's slope, which is why it belongs in this review and not in week 13.

### Numbers you can check

First, where the scope line starts. Week 2 locked 311 estimate-hours. Every cut made since then comes off that figure:

| Week | Change | Estimate-hours | Scope |
|---|---|---|---|
| 2 | Scope sheet locked: must tier 150, should tier 161 | | 311 |
| 5 | Term check at the measured focus: tank taunt (F1) and the boss's second phase leave the slice | −33 | 278 |
| 5 | Term check: talent choice (F6) becomes fixed stat gains, 35 to 10 | −25 | 253 |
| 6 | Lag compensation for the ranged bolt (C8) cut | −16 | 237 |
| 8 | Zone content: plan A's four new rooms and boss room (39) become plan B (24) | −15 | 222 |
| 8 | Ranged bolt re-estimated for its thin version, 10 to 5 | −5 | **217** |

Two things add nothing here. The week 3 spikes test must-tier decisions and were paid from the must tier's 150 hours. The relay was added in sprint 1 and cut in week 6, so it nets to zero. Everything else added since week 3 is growth and shows in the scope column below.

The *Hollowmarch* team's board history. Sprint 1's 43 hours are week 5's measured figure, and sprint 2's 46 are the whole week 6 commitment, finished:

| End of | Velocity (estimated h done) | Done, cumulative | Scope, total |
|---|---|---|---|
| Week 3 (TDD plan, restated after cuts) | | 0 | 217 |
| Sprint 1 | 43 | 43 | 236 |
| Sprint 2 | 46 | 89 | 252 |
| Sprint 3 | 37 | 126 | 262 |

From the table:

```
v_min = 37,  v_mean = (43 + 46 + 37) / 3 = 42,  v_max = 46
g         = (262 − 217) / 3 = 15 hours per sprint
remaining = 262 − 126 = 136 hours
N         = 2 sprints before beta
```

At the current pace, `v_mean − g = 42 − 15 = 27` hours per sprint of net progress. `136 / 27 = 5.0` sprints. The team needs about five sprints and has two. That is the burn-up that never meets in time. Ask the team when they will be done and they will say "two or three more sprints". They said the same thing after sprint 1 and after sprint 2.

Now the four scenarios for the two sprints left:

| Scenario | `v` | `g` | Capacity, 2 sprints | Cut needed |
|---|---|---|---|---|
| Good sprints, freeze | 46 | 0 | 92 | 44 |
| Typical sprints, freeze | 42 | 0 | 84 | 52 |
| Typical sprints, no freeze | 42 | 15 | 54 | 82 |
| Bad sprints, no freeze | 37 | 15 | 44 | 92 |

Check a row, typical sprints with a freeze. `2 × (42 − 0) = 84`, and `136 − 84 = 52` hours to cut.

Three decisions follow from the table.

1. **Freeze now.** Without a freeze, even a typical pair of sprints needs an 82-hour cut. With it, 52. The freeze is worth 30 hours, about two thirds of a sprint, and costs only the discipline of saying no.
2. **Cut to the typical-with-freeze line, 52 hours, at this review.** Take stories from the bottom of the ordered cut list until at least 52 estimated hours are gone, and check each cut against the dependency column so nothing kept depends on something cut.
3. **Pre-agree the next cut.** If sprint 4's velocity comes in at 37 or below, a bad sprint, cut a further 10 hours (the difference between 84 and `2 × 37 = 74`) at the sprint 4 midpoint. Name the stories now.

Here is the team's cut, taken from the bottom of its list. The tank taunt and the boss's second phase are not on it, because the week 5 term check already took them out. The first four lines are left over from the week 2 sheet and the early sprints. The last three are growth added since week 3:

| Cut story | Estimate (h) | Player loses | Depends on it |
|---|---|---|---|
| Loot rarity colors and drop beams (part of F5; the week 5 trigger never fired) | 10 | Excitement on drops | Nothing |
| Ground decals under grunt attacks (part of F3; the boss keeps its telegraphs) | 8 | A warning before a grunt swings | Nothing |
| Combat particle pass (C9, below the line since week 6) | 6 | Final sparks and trails; placeholders stay | Nothing |
| Enemy state packing and the R6 export spike (below the line since week 8) | 6 | Nothing visible with one grunt type and a windowed lab server | Nothing |
| Party chat UI | 10 | Typed chat (voice outside the game still works) | Nothing |
| Death recap screen | 8 | A summary of what killed you | Nothing |
| Key rebinding | 4 | Custom controls | Nothing |
| **Total** | **52** | | |
| *Pre-agreed next cut:* lobby ready-check | 10 | A ready button; host starts manually | Nothing |

Everything cut is a feature players would enjoy. Nothing cut is on the path from login to boss kill. That is what a good cut looks like.

### Cross-game recognition

The same shape shows up in data from outside games. Todd Little's study of 106 software projects at Landmark Graphics (published 2006) found the ratio of actual to initially estimated duration had a median of about 1.8. The spread of remaining-time estimates stayed about as wide late in projects as early on, unlike the neat narrowing that the textbook cone of uncertainty suggests. His teams, like *Cyberpunk*'s dates, kept re-forecasting late. In PR101 week 10, the bug backlog was a stock with an inflow and an outflow, and it only fell when fixing beat finding. A burn-up is the same bathtub. The remaining work is the stock, velocity drains it and scope growth fills it. And in week 6 of this course, the chain rule `q^k` warned that plans with many must-finish pieces rarely finish together. A cut list that removes leaves, not links, is how you shorten the chain without breaking the loop.

### Eyes-open judgment

Three sprints of velocity is a small sample, and it is not stationary. Sprint 1 was mostly code, sprint 3 was mostly content, and sprint 4 will be mostly polish and bugs. The range is a guide, not a law. Update it after every sprint.

Estimated hours are also not actual hours, and the burn-up only works if every number on it is in one unit. Week 8 planned sprint 3 in estimate-hours against `f × U`, with content scaled by `k = 1.33 / 1.28`, so its plan and this chart agree. Sprint 3 still came in at 37 against a forecast of 46. Content-heavy sprints often do, because a new pipeline hides more work than `k` from one room can show.

And a freeze has costs. Some growth is legitimate. A P1 bug from playtest must be fixed, and it adds scope. The freeze rule is that new work enters only by pushing something of equal size below the line, PR101's one-in-one-out. The burn-up then shows the scope line flat while the list's contents change.

Finally, the tempting alternative is to keep the scope and work longer. [PR101 week 12](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w12-crunch-causes-costs-alternatives.md) showed that extra hours lose most of their value within weeks, and your team also has other courses. A 52-hour cut decided in week 9 is cheaper than 52 hours of crunch in week 12.

## 5. Running the review

Structure the meeting around the numbers.

**Before the review,** the producer role updates the burn-up with sprint 3's data and fills the scenario table. Nobody needs to argue about the forecast in the meeting if it is on screen when the meeting starts.

**During the review,** play first. The increment is the evidence that the done line is real. Then show the burn-up and the table. Then walk the cut list from the bottom up, reading each story's "player loses" column aloud, until the cut total reaches the chosen scenario.

**After the review,** mark the cut stories as cut, not deleted. They are the start of your post-mortem list and, for a few, your wishlist for PR301. Record the feature freeze date in the team agreement.

## Studio session plan

Week 9 meeting, 3 hours. Teams present to the instructor and one other team.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:15 | Briefing: burn-up versus burn-down, the scenario table | |
| 0:15-0:45 | Teams fill lab 09: history, scenarios, required cut; run `burnup_forecast.py` | Forecast table and required cut |
| 0:45-1:30 | Reviews, round 1: half the teams, 12 minutes each (5 play, 3 burn-up, 4 cut list) | Review record per team |
| 1:30-1:40 | Break | |
| 1:40-2:25 | Reviews, round 2: the other half | Review record per team |
| 2:25-2:45 | Teams finalize the cut list and pre-agreed next cut; declare the freeze | Signed cut list |
| 2:45-3:00 | Alpha preparation: read the week 10 alpha criteria, assign owners for each | Alpha owner list |

## Deliverables

Due at the end of the meeting:

1. **Burn-up forecast** in the lab 09 format ([`labs/lab09.md`](../labs/lab09.md)): the board history, the burn-up chart, the four-scenario table, the chosen scenario with a one-line reason, and the required cut. Checked with `burnup_forecast.py`, which recomputes the table and confirms the cut list reaches the required total.
2. **Ordered cut list**, with estimates, what the player loses and dependencies, marked "cut now" or "pre-agreed next cut" with its trigger.
3. **Feature freeze declaration**: the date and the one-in-one-out rule, added to the team agreement.
4. **Sprint 3 review record**: goal met (yes or no), velocity, and the backlog changes.

## Common failure modes

- **Forecasting from the done line only.** The finish looks two sprints away every sprint. Draw the scope line.
- **Using the best sprint as the plan.** Sprint 2 went well, so the team plans at 46. Choose the scenario deliberately and name it.
- **Cutting links instead of leaves.** The cut removes something the boss fight needs. Check the dependency column before cutting.
- **Freezing without one-in-one-out.** The freeze is declared, then every playtest finding goes in on top. Equal-size work leaves when new work enters.
- **Deleting cut stories.** They vanish from the record and come back as scope growth in sprint 4. Mark them cut.
- **"We'll just work harder."** The cut is replaced by a promise of extra hours. PR101 week 12 explains why that fails.

## Review checklist

The instructor checks at the review:

- [ ] The increment plays in a tagged networked build, and the sprint goal is answered yes or no.
- [ ] The burn-up shows both lines for weeks 3 to 9 from the board's real history, and the starting scope traces to the week 2 sheet through a table of dated cuts.
- [ ] `v_min`, `v_mean`, `v_max`, `g` and the remaining work are computed, and the scenario table matches the checker.
- [ ] The chosen scenario is named with a reason, and the cut list reaches at least the required cut.
- [ ] No cut story is a dependency of a kept story, and nothing on the login-to-boss path is cut.
- [ ] A pre-agreed next cut exists with a numeric trigger.
- [ ] The feature freeze date and one-in-one-out rule are in the team agreement.
- [ ] Every alpha criterion from week 10 has an owner.

## Sources

- Wikipedia, "Cyberpunk 2077" (accessed September 2026), as cited in PR101 week 9. Release date of 16 April 2020 announced at E3 2019; delays announced in January 2020 (to 17 September), June 2020 (to 19 November) and October 2020 (to 10 December); release on 10 December 2020.
- Little, T. (2006). "Schedule Estimation and Uncertainty Surrounding the Cone of Uncertainty." *IEEE Software* 23(3), 48-54. doi:10.1109/MS.2006.82. Landmark Graphics data, 106 projects; median ratio of actual to initial estimate about 1.8; remaining-duration uncertainty about as wide late as early.
- Fowler, M. "Yesterdays Weather." martinfowler.com, 12 May 2004.
- Schwaber, K. and Sutherland, J. (2020). *The Scrum Guide*, November 2020 edition. Sprint review and product backlog adaptation.
- Cohn, M. (2005). *Agile Estimating and Planning*. Prentice Hall. Velocity ranges and release burn charts.
- The *Hollowmarch* board history, cut list and scenario table are invented for teaching.

## Interactive spec

**File:** `examples/w09-burnup-forecast.html`

**The one insight:** a project can look "two sprints from done" every sprint while never getting closer, because the scope line climbs almost as fast as the done line. Freezing scope changes the forecast more than any plausible change in velocity.

**What is plotted.** One chart, x axis in sprints (0 to 10), y axis in estimated hours (0 to 400).

- Scope line: solid, through the history points (sprint 0 to the current sprint), then dashed forward at slope `g`.
- Done line: solid through history, then a shaded fan forward between slope `v_min` and slope `v_max`, with a dashed center line at `v_mean`.
- A vertical line at the beta sprint (`current + N`), labeled "beta".
- A marker where the `v_mean` done projection meets the scope projection, labeled with the sprint number (or "never" if `v_mean ≤ g`).
- At the beta line, a bracket showing the gap between the scope projection and the done fan, labeled "cut needed: X to Y hours".

A second panel, beside the chart on wide screens and below it on phones, shows the four-scenario table from section 4, recomputed live, with the row matching the current slider settings highlighted.

**Controls.**

- Editable history table: up to 6 rows of (velocity, scope at end of sprint). Defaults are the *Hollowmarch* history: initial scope 217; velocities 43, 46, 37; scope 236, 252, 262.
- Slider `N`, sprints left before beta: 1 to 5, default 2.
- Slider `g` override: 0 to 30 hours per sprint, default "measured" (15 for the defaults). A "freeze" toggle sets `g = 0`.
- Radio choice for the planning scenario: `v_min`, `v_mean`, `v_max`.
- A "replay history" button that steps the chart one sprint at a time and shows, at each step, the forecast finish the team would have computed from the done line alone (ignoring scope growth). For the defaults this shows the finish sliding later every sprint, which is the hook.

**Formulas.**

```
v_min, v_mean, v_max from the velocity column
g = (scope_last − scope_0) / sprints        (unless overridden or frozen)
remaining = scope_last − Σ velocities
capacity  = N × (v − g)
cut       = max(0, remaining − capacity)
meet      = current + remaining / (v − g)   if v > g, else "never"
done-line-only forecast at sprint s = s + (scope_s − done_s) / v_mean_to_s
```

**Test values (defaults).** `v_min = 37`, `v_mean = 42`, `v_max = 46`, `g = 15`, remaining 136. With `N = 2`: cut 44 (`v_max`, freeze), 52 (`v_mean`, freeze), 82 (`v_mean`, `g = 15`), 92 (`v_min`, `g = 15`). Meeting point at `v_mean`, `g = 15`: sprint `3 + 136 / 27 = 8.0`. With freeze at `v_mean`: `3 + 136 / 42 = 6.2`. Done-line-only forecasts during replay: after sprint 1, `1 + 193 / 43 = 5.5`; after sprint 2, `2 + 163 / 44.5 = 5.7`; after sprint 3, `3 + 136 / 42 = 6.2`. The finish moves later each sprint, though each forecast said the team was only three to five sprints from done.

**Accessibility.** Keyboard control of every slider and the table, text summary of the current forecast under the chart ("At 42 hours per sprint with scope growing 15 per sprint, you finish in sprint 8.0. Beta is sprint 5. Cut 82 hours."), respects reduced motion (replay steps without animation) and both color schemes. Scope and done lines differ by dash pattern and label as well as color.

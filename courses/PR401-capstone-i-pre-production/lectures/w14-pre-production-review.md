# PR401 · Week 14 — Pre-production Review

**Why this matters:** This is the meeting where your project is allowed into production, sent back, or changed before it goes. The panel plays your slice, reads your plan and asks one question in many forms. Does what you measured in the slice support what you plan to build in PR402? Teams that bring the week 11 plan unchanged are answering a question from week 11. This week you replan production from the slice's measured costs, bring the plan and the evidence to the panel, and leave with a decision.

**You will be able to:**
- Project the production cost of a content type from the slice's measured first-unit cost, with and without a learning curve.
- Compute how far that projection moves each discipline's load, and choose a replan that fits.
- Defend the learning rate you planned with, and say what evidence would change it.
- Present the pre-production package to a review panel and record the decision and its conditions.

**Before class:** Bring the tagged time log from labs 12 and 13, the stability report from lab 13, the lab 11 plan files, and the tagged review build installed and tested on the review machines. Read [MMO403 week 14, pitching to publishers and investors](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w14-pitching-to-publishers-and-investors.md), section 2, on stage gates and kill rules (20 minutes).

**Prerequisites from earlier courses:** [MMO403 week 14](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w14-pitching-to-publishers-and-investors.md) (why funders fund stages, and how a gate is priced). [MMO403 week 13, team and budget planning](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w13-team-and-budget-planning.md) (what a slip costs). [PR101 week 4, scope and cut lists](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md). [PR101 week 14, post-mortems as a practice](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w14-post-mortems-as-a-practice.md) (checkable action items). [MMO306 week 13, content budgets and cadence planning](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w13-content-budgets-and-cadence-planning.md). From this course, [week 11](w11-production-plan.md) (discipline loads), [week 12](w12-vertical-slice-sprint-1.md) (one-time and per-unit hours) and [week 13](w13-vertical-slice-sprint-2.md) (stability evidence). Looking ahead, [MMO407 week 13, launch plan workshop](../../MMO407-launch-scaling-and-post-mortems/lectures/w13-launch-plan-workshop.md) (next semester) covers the risk register the panel will read, and [MMO405 week 2, quantitative methods overview](../../MMO405-research-methods-in-online-games/lectures/w02-quantitative-methods-overview.md) covers deciding in advance what result would change your mind.

**Interactive:** [Slice to production model](../examples/w14-slice-to-production.html). Use it during section 3.

---

## 1. What the review decides

The review is a **stage gate**. MMO403 week 14 showed why careful funders pay for a project one stage at a time. Each stage is cheaper than the next and produces evidence that changes the odds. Pre-production was the cheap stage. Production in PR402 is the expensive one, fifteen weeks of seven people. The panel's job is to decide whether the evidence justifies spending it on this plan.

The panel returns one of four decisions.

- **Go.** The slice meets its quality bar, the plan fits the measured costs, and the risks have triggers. Production starts in PR402 week 1 on this plan.
- **Go with conditions.** The project goes into production, but with named changes that must be in the week 15 package, such as "cut the fourth town" or "server soak of 20 hours before PR402 sprint 1". Most good teams get this result.
- **Rework.** Something central is unproven, such as the core loop not reading as fun in the slice, or the plan not fitting by a wide margin. The team returns in week 15 with a revised slice element or plan. It is not a failure grade. It is the gate working.
- **Pivot.** The evidence says the game as pitched won't work in the time available. The team keeps its technology and changes the design, with a narrower plan, before PR402.

Say this aloud in your team before the review. A panel that says "rework" has saved you from spending PR402 on a plan that couldn't finish.

## 2. The pre-production package

The week 15 final hands in the whole package. The review sees the draft. It contains, from this semester:

- **The greenlit pitch** from week 6, updated with anything the slice changed.
- **Pillars and vision** from week 3.
- **Technical design** from week 7, updated with what the slice taught you about the server and data.
- **Economy and balance design** from week 8.
- **Content plan** from week 9, with unit counts.
- **Social systems plan** from week 10.
- **Production plan** from week 11, **replanned** with the slice's measured costs. This week's worked example.
- **The vertical slice**, the tagged build, the stability statement from week 13, and the tagged time log.
- **Risk register** with triggers and responses (MMO407 week 13).

The panel will not read all of it in the meeting. It will read the replanned production plan, play the slice, and use the rest to check answers.

## 3. Worked example: from one measured unit to a production plan

### The hook

When Naoki Yoshida explained at GDC 2014 what had gone wrong with the original *Final Fantasy XIV* (2010), he showed a flowerpot outside an inn. It had over 1,000 polygons and 150 lines of shader code, so it cost as much to draw as a player character. To afford that level of detail, the original team had limited the number of player characters on screen at once to 20. Polygon's report of the talk says the result looked slightly better than the rebuilt game but its areas were empty.

Detail per unit and number of units trade against each other. That is true of the draw budget on a player's machine, and it is true of the hours budget on your team. A world where each prop or zone costs more than planned is a world with fewer of them. Your slice has just measured what one unit of your world costs at the quality you promised. The question for this review is what that measurement does to the plan.

### The model

The slice gives you one number per content type, the per-unit cost of the first unit at final quality, `u_1`, with one-time work removed (week 12). Production will make more units of the same type. Two models project their cost.

```
Flat:            u_n = u_1                         every unit costs the same
Learning curve:  u_n = u_1 × n^(log2 LR)           each doubling of units multiplies cost by LR
Total for units a to z:  T = Σ u_n for n = a..z
```

- `n` counts units of the same type from the first one made, so the slice's unit is `n = 1` and production's next units are `n = 2, 3, ...`.
- `LR` is the **learning rate**, the cost multiplier per doubling of cumulative units. At `LR = 0.8` the second unit costs 80% of the first, the fourth 64%, the eighth 51%. `LR = 1.0` is the flat model.
- `log2 LR` is negative when `LR < 1`, so costs fall as `n` grows.

This is **Wright's law**. Theodore Wright reported in 1936 that in aircraft manufacture, the labour to build one airplane fell by about 20% each time cumulative production doubled, which is `LR = 0.8`.

### Numbers you can check

The *Emberfall* artist logged 14 hours on the slice town, of which 4 were one-time (material library, export presets, learning the foliage painter). So `u_1 = 10` hours. That is an actual, so it is not multiplied by the plan ratio. The week 11 plan carried three more towns at 5 estimated hours each, which at `R = 1.30` is 6.5 planned hours per town and 19.5 for the three. The rest of the art plan was 48.1 planned hours, and art capacity is 72.

The three production towns are units 2, 3 and 4. With `LR = 0.9`, `log2 0.9 = −0.152`:

- `u_2 = 10 × 2^−0.152 = 10 × 0.900 = 9.0`
- `u_3 = 10 × 3^−0.152 = 10 × 0.846 = 8.5`
- `u_4 = 10 × 4^−0.152 = 10 × 0.810 = 8.1`
- Total `25.6` hours, against 19.5 planned.

| Learning rate | Units 2-4 (three towns) | Art load with three | Units 2-3 (two towns) | Art load with two |
|---|---|---|---|---|
| 1.00 (flat) | 30.0 | 1.08 | 20.0 | 0.95 |
| 0.95 | 27.7 | 1.05 | 18.7 | 0.93 |
| 0.90 | 25.6 | 1.02 | 17.5 | 0.91 |
| 0.85 | 23.5 | 0.99 | 16.2 | 0.89 |
| 0.80 | 21.4 | 0.97 | 15.0 | 0.88 |

The art load is `(48.1 + T) / 72`, the week 11 art plan with the town line replaced. Check the flat row with three towns: `(48.1 + 30.0) / 72 = 1.08`.

Two things stand out. First, the week 11 guess of 6.5 planned hours per town was not slightly optimistic. The measured first unit is 1.5 times it, even after the plan ratio. Second, three towns fit only if the artist learns at a rate of about 0.86 or better, close to Wright's aircraft. Two towns fit at any rate in the table.

### Which learning rate to plan with

This is the judgment the panel will probe, so decide it on evidence.

- **You have one unit.** A learning rate is a slope, and one point has no slope. Any `LR` you plan with is an assumption until you have built at least two units of the same type at the same quality bar.
- **Small teams learn less than factories.** Wright's 0.8 came from repeated assembly of the same airplane. A town is not the same object built again. Much of what makes it cheaper next time (the material library, the presets) you already removed as one-time work in week 12. What is left is per-unit work that improves more slowly.
- **Plan at 0.95, hope for 0.85.** At 0.95, three towns put art at 1.05. The team could make that fit by spending the boss-model cut it held in reserve in week 11 (5.2 planned hours), which brings art to 0.98. It decides not to, because that would leave the one artist with no reserve at all. It plans two more towns, art at 0.93, and keeps the boss cut in reserve.
- **The fourth town goes on the cut list with a trigger.** Trigger: town 2 (unit 2) comes in at 8.5 hours or less, the `LR = 0.85` line. Response: reinstate the fourth town, and art stays at or below 0.99. If town 2 takes more than 9.5 hours (the `LR = 0.95` line), the response runs the other way: take the boss cut to protect the two towns.

The replanned game has three towns where the pitch promised four. For a game whose vision is small groups holding towns, that is a design change as well as a production one. Fewer towns means more groups competing for each, and the designers check that against the week 8 economy before the review. They also rerun the week 10 liquidity sheet. Ninety players in three towns make towns of 30, which field four defenders on 96% of evenings without the militia, so the militia may no longer be needed. The team says all this on the first slide of the plan presentation, before the panel finds it.

### Move it yourself

In the interactive, the left view plots cost per unit against unit number for the chosen `u_1` and `LR`, with the week 11 estimate as a flat dashed line well below. The right view plots cumulative hours for the planned units against the hours the art plan has room for. Drag `LR` from 1.0 down to 0.8 and watch the cumulative curve bend, and only cross under the line near 0.86. Then set the unit count to two and watch it fit at every rate. The left view makes each unit look nearly affordable. The right view shows whether the plan does.

### Cross-game recognition

**Final Fantasy XIV, rewritten.** The flowerpot is a `u_1` far above budget. Once one prop costs as much as a character, the budget allows fewer props and fewer characters, and the world empties. The rebuilt game moved to a fixed rhythm of content, with a major patch roughly every three months in the *A Realm Reborn* era (week 9 notes a longer interval since *Endwalker*). Same-shaped units on a steady cadence are the conditions under which a learning curve can appear. Whether Square Enix's per-unit costs fell is not public, and nothing here depends on it.

**Wright's aircraft.** The original setting of the model. The 20% per doubling came from building many identical airframes, where each worker repeats the same steps. That is why it is an upper bound on how fast a capstone team learns, not a default.

**Content cadence in MMO306.** MMO306 week 13 planned a content drop every N days from team-days per drop and showed that planning with the average makes you late half the time. A learning rate is one more average. If you plan with a hopeful one, you inherit the same late-half-the-time problem, which is why the *Emberfall* team attached a trigger to it.

### Eyes-open design judgment

- **Measure before you believe a curve.** One slice unit tells you `u_1`. The second unit tells you whether learning is happening. Schedule the second unit of your costliest content type early in PR402 so the evidence arrives while you can still act on it.
- **The flat model is not pessimistic, it is a baseline.** Planning flat protects you, but for content you really will make ten or twenty times (quests, items), it overstates cost. Use the flat model for units you make two or three times and a modest curve for units you make many times, and say which is which.
- **Cut units, not quality, unless the quality bar was wrong.** The slice quality bar is what the panel is approving. Lowering it for production units to make the plan fit is a different game. If you think the bar was set too high, say that to the panel as a decision, with a sample.
- **Every replan belongs in the risk register.** A learning rate, a tool's `u_t` and a crash-rate bound are all assumptions. Each one gets a trigger that tells you in PR402 when it has failed.

### Check this example

1. A slice dungeon room took 40 per-unit hours. The plan wants five more rooms. What is the flat total, and the total at `LR = 0.8`? (`log2 0.8 = −0.322`)
2. The *Emberfall* bounty tool made the slice's three bounties at 1.2 hours each (1.1 designer, 0.1 programmer) instead of the estimated 0.5. Eighteen bounties remain. Is the tool still worth using, and what is the new design load if the week 12 plan had design at 114.9 of 144 hours with 21 bounties at 0.52 planned designer hours each?
3. Town 2 comes in at 8.5 hours. What learning rate does that imply, and what does the team do?

<details>
<summary>Answers</summary>

1. Flat: `5 × 40 = 200` hours. At 0.8, units 2 to 6 cost `40 × (0.800 + 0.702 + 0.640 + 0.596 + 0.562) = 40 × 3.300 = 132` hours.
2. Its cost `F` is spent, so compare per unit only: 1.2 hours with the tool against 1.5 by hand. It still saves 0.3 hours per bounty, 5.4 in all. Design demand becomes `114.9 − 21 × 0.52 + 18 × 1.1 = 114.9 − 10.9 + 19.8 = 123.8`, a load of `123.8 / 144 = 0.86`. Still under 1.0, but design's slack falls from 0.20 to 0.14, and the tool's measured `u_t` goes in the risk register.
3. `8.5 = 10 × 2^b`, so `2^b = 0.85` and `LR = 0.85`. The trigger fires. The team reinstates the fourth town, with art at 0.99, and keeps watching. If town 3 comes in above the 0.85 line, the boss cut is the response.

</details>

## 4. Presenting to the panel

The review lasts 45 minutes per team.

- **Play first (15 minutes).** Two panel members per party, on the review machines, following your demo script loosely. The team does not narrate the controls. Watch where the panel gets stuck, and note it.
- **The plan (10 minutes).** Start with what changed since week 11 and why. Show the replanned load table, the learning rate you planned with and its trigger, the stability statement, and the three highest risks. Don't read the package aloud.
- **Questions (15 minutes).** The panel asks. Answer with the number or say you don't have it. "We didn't measure that" followed by how you will is a good answer. A confident guess is a bad one.
- **Decision (5 minutes).** The panel confers and states the decision and any conditions. The producer writes them down and reads them back before the team leaves.

The conditions become checkable action items in the week 15 package, in the form PR101 week 14 taught: an owner, a date and an observable result.

## Studio session plan

Week 14 meeting, 3 hours plus review slots. Reviews run in 45-minute slots across the meeting; teams not under review work through the agenda below.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:10 | Briefing: the four decisions, the review format, how conditions are recorded | |
| 0:10-0:50 | Replan: fill `replan.csv` from the time log, run `reconcile.py` at the planned learning rate and at 1.0 (lab 14) | Replanned loads |
| 0:50-1:20 | Choose cuts or moves until the plan fits; add each assumption to the risk register with a trigger | Replanned plan |
| 1:20-1:30 | Break | |
| 1:30-2:00 | Rehearse: demo script run-through on the review machines, one 10-minute plan talk, a mock question round from a neighbour team | Rehearsed |
| 2:00-2:45 | Peer panel: sit in on another team's review and write two questions the real panel didn't ask | Peer notes |
| 2:45-3:00 | Record the decision and conditions; convert each condition into an action item | `review-decision.md` |

## Deliverables

Due at the end of the week 14 meeting, in `preproduction/week14/`:

1. **Replanned production plan**: `replan.csv` and the output of `reconcile.py` in the lab 14 format ([`labs/lab14.md`](../labs/lab14.md)), which must print `PASS`, plus the updated `production-plan.md`.
2. **Review decision record** (`review-decision.md`): the panel's decision, each condition as an action item with owner, date and observable result, and the peer panel's questions with your answers.

Due at week 15: the full pre-production package, with every condition addressed.

## Common failure modes

- **Bringing the week 11 plan unchanged.** The slice measured things. Use them.
- **Extrapolating the slice total.** One-time hours in the first unit inflate every projection. Use the week 12 split.
- **A heroic learning rate.** Planning at 0.8 because it makes the plan fit. One unit gives you no slope. Plan cautiously and put the hope in a trigger.
- **Cutting quality to fit.** The panel approved the slice at its quality bar. Cut units first.
- **Hiding the cut.** Panels find them. Lead with what changed.
- **Arguing with the decision.** Ask what evidence would change it, write that down, and bring it in week 15.

## Review checklist

The panel and the instructor check:

- [ ] The slice build plays on the review machines from the tag, following the demo script, and meets its quality bar.
- [ ] The stability statement reports exposures and upper bounds (week 13).
- [ ] `reconcile.py` prints `PASS`; per-unit costs come from the tagged time log with one-time hours removed.
- [ ] The planned learning rate is 0.9 or higher, or is supported by at least two measured units of that type.
- [ ] The replanned loads are at or below 1.0 for every discipline at every milestone.
- [ ] Every changed assumption (learning rate, tool `u_t`, crash bound) is in the risk register with a trigger and response.
- [ ] Every safety minimum from week 10 section 3 (code of conduct, report, block and mute, chat filter, moderation rota, sanctions, age policy, data and consent) is in the slice build or scheduled in the replanned backlog before PR402's closed beta, with an owner, and `social_check.py` still prints `PASS`.
- [ ] The presentation states what changed since week 11 before the panel asks.
- [ ] The decision and conditions are recorded, read back and converted into action items.

## Sources

- Kollar, P. "Final Fantasy 14 killed by Square Enix's stubbornness, reborn by a new approach." Polygon, 20 March 2014 (read via the Internet Archive copy of 21 March 2015). Report of Naoki Yoshida's GDC 2014 talk: the original version's areas looked slightly better but were empty; the flowerpot with over 1,000 polygons and 150 lines of shader code, as many resources as one player character; player characters on screen limited to 20. Paraphrased; one short phrase quoted in MMO306 week 12 is not repeated here.
- Wikipedia, "Final Fantasy XIV" (read September 2026). The development team schedules a major update approximately every three months.
- Wikipedia, "Experience curve effects" (read September 2026). Wright, T. P. (1936), "Factors Affecting the Cost of Airplanes," *Journal of the Aeronautical Sciences*: labour per airplane fell by about 20% with each doubling of total production; the power-law form `C_x = C_1 x^(log2 b)`.
- The *Emberfall* hours, learning-rate plan, triggers and review format are a constructed teaching example continuing weeks 6, 11, 12 and 13. They are not data from a real team.

## Interactive spec: examples/w14-slice-to-production.html

**The one insight.** A per-unit cost curve can look affordable unit by unit while the cumulative total stays above the room in the plan, and only a hopeful learning rate rescues a plan whose per-unit estimate was well below the measured first unit.

**Layout.** Two linked views, stacked on mobile, side by side on desktop.

1. **Cost per unit (left).** Points and a line for `u_n` at `n = 1 .. N + 1`, where `n = 1` is the slice unit (drawn hollow, labelled "slice, measured"). A dashed horizontal line at the old planned cost per unit `e` (default 6.5), labelled "week 11 plan". Y axis from 0 to `u_1 × 1.1`.
2. **Cumulative hours (right).** A step line of cumulative production hours `Σ u_n` for `n = 2 .. N + 1`, and a horizontal line at the room the plan has for these units, `H = C − O` (default 72 − 48.1 = 23.9), labelled "room in the art plan". The region above `H` is shaded with the "danger" token. Label the final total and the resulting discipline load.

Above both, large text: "Three towns at LR 0.90: 25.6 h against 23.9 h of room · Art load 1.02".

**Controls** (keyboard operable, value shown beside each, every change redraws both views immediately).

- Measured first unit `u_1`: slider 2 to 60 h, step 0.5, default 10.
- Old planned cost per unit `e`: slider 1 to 60, step 0.5, default 6.5 (display only).
- Production units `N`: slider 1 to 12, step 1, default 3.
- Learning rate `LR`: slider 0.70 to 1.00, step 0.01, default 0.90. Show `log2 LR` beside it.
- Other demand in the discipline `O`: number input, default 48.1. Capacity `C`: number input, default 72.
- Buttons "Flat (LR 1.0)", "Wright (LR 0.8)", "Reset".
- Readout "LR needed to fit": the largest `LR` in [0.50, 1.00] at which `Σ u_n ≤ C − O`, found by bisection to 0.001, or "no LR ≥ 0.5 fits".

**Formulas.**

```
b    = log2(LR)
u_n  = u_1 × n^b
T    = Σ_{n=2}^{N+1} u_n
load = (O + T) / C
```

**Test values** (must match the guide to one decimal, loads to two).

- Defaults (`u_1 = 10`, `N = 3`, `LR = 0.90`): `u_2 = 9.0`, `u_3 = 8.5`, `u_4 = 8.1`, `T = 25.6`, load 1.02.
- `LR = 1.00`, `N = 3`: `T = 30.0`, load 1.08. `LR = 0.80`, `N = 3`: `T = 21.4`, load 0.97.
- `N = 2`: `LR = 1.00` gives 20.0 (0.95); 0.95 gives 18.7 (0.93); 0.90 gives 17.5 (0.91); 0.80 gives 15.0 (0.88).
- `N = 3`: LR needed to fit ≈ 0.861.
- Check-yourself case `u_1 = 40`, `N = 5`, `LR = 0.8`: `T = 132.0`.

**Behaviour.** First screen shows the defaults, so the dashed estimate line sits far below every point on the left and the cumulative line ends in the shaded region on the right. Transitions 150 ms, none under `prefers-reduced-motion`. Colours from `templates/interactive-tokens.css`. No game art, logos or screenshots.

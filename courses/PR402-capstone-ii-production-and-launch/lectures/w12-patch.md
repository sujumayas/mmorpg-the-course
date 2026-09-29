# PR402 · Week 12 — Patch: Sizing, Freezing and Shipping Your First Live Update

**Why this matters:** This week you ship your first planned update to a game that real players are using. A patch is the first time your team has to hit a date that players can see while the game keeps running. If you fill it the way you filled your sprints, with estimates that add up to the hours you have, it will be late, and a late patch in a live game means a week of the bugs it was meant to fix. This week you size the patch from your own track record, fix the date, and decide in advance what you drop if something goes wrong.

**You will be able to:**
- Compute the hours available for patch items after interrupts and release work, and convert them into an estimate budget using your team's measured plan ratio.
- Select patch items by rule (must-fix first, then value per estimated hour) and state the expected actual hours and slack.
- Write a cut order and go/no-go criteria for release day before the code freeze.
- Run a release through the checklist and staged rollout from earlier courses, and record what the patch changed for players.

**Before class:** Bring lab 11 (your planned hours for weeks 11 and 12) and your sprint 1 to 4 estimate and actual hours. Reread PR101 week 6, sections 1 and 2, on estimate ratios and the plan ratio `R` (20 minutes). Reread MMO308 week 9, sections 2 and 3, on staged rollouts and hotfix versus wait (20 minutes). Skim PR101 week 13, section 4, the release checklist (10 minutes).

**Prerequisites from earlier courses:** [PR101 week 6, estimation and why it fails](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md) (the ratio `actual / estimate`, the plan ratio `R` and the buffer `b = 1 − 1/R`, used here without re-deriving). [PR101 week 4, scope and cut lists](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md) (cut lists). [PR101 week 13, builds and release checklists](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w13-builds-and-release-checklists.md) (build identity and the checklist). [MMO308 week 9, patch management and hotfixes](../../MMO308-live-operations-analytics-and-experimentation/lectures/w09-patch-management-and-hotfixes.md) (staged rollout, when to hotfix, versions and rollback). [MMO308 week 10, player feedback loops](../../MMO308-live-operations-analytics-and-experimentation/lectures/w10-player-feedback-loops-forums-surveys-polls.md) (patch notes as a conversation). From this course, [week 7, production sprint 4](w07-production-sprint-4.md) (capacity, the interrupt buffer and the cut line, here restated in hours), [week 10, live-ops week 1](w10-live-ops-week-1.md) (what went into the hotfixes) and [week 11](w11-live-ops-week-2-operating-rhythm.md) (planned hours after interrupts).

---

## 1. What a patch is, for your team

A **patch** is a planned, versioned update to the live game. It has a date, a build number, a list of changes and patch notes. A **hotfix** is an unplanned change pushed between patches to stop an ongoing harm. MMO308 week 9 gave you the rule for choosing between them. Week 10 used that rule for your first hotfixes. This week is about the planned kind.

For a student team the first patch usually carries three sorts of item.

- **Must-fix bugs.** SEV1 and SEV2 bugs found since launch (week 4's mapping), including anything you stopped with a kill switch or a hotfix that needs a proper fix.
- **Toil removers.** The fixes from week 11 that cut interrupt hours. Several may already be done; the patch is where they reach players.
- **Player-facing improvements.** Quality-of-life changes, a balance pass, perhaps a small event.

A patch is also a promise. Once you announce a date, players plan around it. Moving the date is possible but costs trust, which MMO407 week 10 treats as the slowest thing to rebuild.

## 2. Fixed date, variable scope

There are two ways to plan a release. **Fixed scope** says "these items ship, whenever they are done". **Fixed date** says "we ship on this day with whatever is done and tested". Live games almost always choose the second, and so will you. Your course has a fixed end, your players need a predictable rhythm, and the bugs in the current build do harm every day the patch waits.

Fixed date only works if you plan the scope so that it fits with room to spare, and decide in advance what leaves first. That is the worked example.

## 3. Worked example: the patch that fits

### The hook

Riot Games publishes the patch schedule for League of Legends a year at a time. The 2026 schedule on Riot's support site lists 24 patches, 26.01 on 8 January to 26.24 on 9 December. Most are exactly 14 days apart, with a few three-week gaps around holidays. Patches release on a Wednesday, Pacific time, unless the page marks them otherwise, and four 2026 dates are marked as Thursdays.

What the schedule does not list is what each patch will contain. The dates are fixed months ahead. The contents are decided much later. A game with that many players and that much content ships on a calendar and lets scope move, because the other way round would leave players never knowing when the next change is coming. Your patch runs on the same principle with far fewer hours. The question is how much to put in it.

### The model

Week 7 sized sprint 4 in points from velocity. A patch mixes bug fixes and features whose points were never calibrated against each other, so this week works in hours and corrects them with your ratio. Start from the hours, not the wish list.

```
H = planned hours from now until code freeze          (from lab 11)
X = hours reserved for release work                   (regression pass, checklist, staged deploy)
A = H − X                                             hours available for patch items
R = Σ actual / Σ estimate over past sprints           your plan ratio (PR101 week 6)
E = A / R                                             estimate budget
```

`E` is the number you compare with the sum of your estimates. If your estimates were perfect, `R` would be 1 and `E` would equal `A`. They are not, and your own sprints tell you by how much.

Then choose items by rule.

1. Must-fix items go in first, whatever their value.
2. Rank the rest by value per estimated hour, where value is the number of weekly active players the item affects, from telemetry or tickets.
3. Add items in that order while the running estimate stays within `E`. Skip any item that does not fit and try the next.
4. Record the expected actual hours `R × Σ estimate` and the slack `A − R × Σ estimate`.

The items that go in, read from the bottom up, are also your **cut order**. If something goes wrong, the last item added is the first to leave.

### Numbers you can check

The Emberfall team from week 11 has these inputs.

**Hours.** Week 11 leaves 16.3 planned hours after the buy-back work, and week 12 has 52. So `H = 16.3 + 52 = 68.3`. Their launch build took about 10 hours of release work (a full regression pass, the checklist, a staged deploy to one zone first), so `X = 10` and `A = 58.3`.

**Plan ratio.** From their sprint records. Each sprint is one week ([week 1](w01-production-sprint-1-the-ops-tax.md)), and the hours are those logged on committed items, so they sit well under the 84 team hours once the ops tax and meetings are out:

| Sprint | Estimated hours | Actual hours | Ratio |
|---|---|---|---|
| 1 | 36 | 54 | 1.50 |
| 2 | 39 | 54 | 1.38 |
| 3 | 35.5 | 46 | 1.30 |
| 4 | 33.5 | 40.5 | 1.21 |
| Total | 144 | 194.5 | `R` = 1.35 |

`R = 194.5 / 144 = 1.3507`, so `E = 58.3 / 1.35 = 43.2` estimated hours. Equivalently, the team needs a buffer of `b = 1 − 1/1.35 = 26%` of the hours it has.

**Candidates.**

| Item | Type | Estimate (h) | Players affected per week | Players per estimated hour |
|---|---|---|---|---|
| Party loot desync | Must-fix, SEV2 | 6 | | |
| Crafting duplication exploit (kill switch on since week 10) | Must-fix, SEV1 | 4 | | |
| Tutorial quest marker points at the wrong town gate | Improvement | 3 | 60 | 20.0 |
| Ranger balance pass | Improvement | 4 | 70 | 17.5 |
| Fast travel between towns | Improvement | 8 | 90 | 11.3 |
| Ash-storm event (PR401 week 9) | Improvement | 14 | 120 | 8.6 |
| UI scale option | Improvement | 5 | 25 | 5.0 |
| Guild bank | Improvement | 20 | 45 | 2.3 |

Walk the rule. Must-fix items take 10 estimated hours. Then tutorial marker (13), ranger pass (17), fast travel (25), ash storm (39). The UI scale option would take the total to 44, over 43.2, so it is skipped. The guild bank would take it to 59. Also skipped.

The plan is 39 estimated hours. Expected actual hours are `39 × 1.35 = 52.7`, leaving `58.3 − 52.7 = 5.6` hours of slack. The cut order, from first to leave, is ash storm, fast travel, ranger pass, tutorial marker. Dropping the ash storm alone frees `14 × 1.35 = 18.9` hours.

Now the plan the team nearly made. The first draft put every item in, because the estimates add up to `10 + 3 + 4 + 8 + 14 + 5 + 20 = 64` hours, which fits under `H = 68.3`. At the team's own ratio, 64 estimated hours means `64 × 1.35 = 86.4` actual hours. That is 28.1 hours over `A`, about 0.54 of a week at 52 hours. The patch would have shipped halfway through week 13, or on time without its regression pass. The draft made two errors at once. It compared estimates with hours as though `R` were 1, and it forgot the 10 hours of release work.

This script reproduces the plan. Run it with `.venv/bin/python`.

```python
est, act = [36, 39, 35.5, 33.5], [54, 54, 46, 40.5]
R = sum(act) / sum(est)
A = (16.3 + 52) - 10
E = A / R
must = 6 + 4
items = [("tutorial marker", 3, 60), ("ranger pass", 4, 70), ("fast travel", 8, 90),
         ("ash storm", 14, 120), ("UI scale", 5, 25), ("guild bank", 20, 45)]
items.sort(key=lambda x: -x[2] / x[1])
total, plan = must, []
for name, e, players in items:
    if total + e <= E:
        total += e
        plan.append(name)
print(f"R={R:.3f}  A={A:.1f}  E={E:.1f}")
print(f"plan={plan}  estimate={total}  expected={total * R:.1f}  slack={A - total * R:.1f}")
naive = must + sum(e for _, e, _ in items)
print(f"all items: estimate={naive}  expected={naive * R:.1f}  over by {naive * R - A:.1f} h")
```

It prints:

```
R=1.351  A=58.3  E=43.2
plan=['tutorial marker', 'ranger pass', 'fast travel', 'ash storm']  estimate=39  expected=52.7  slack=5.6
all items: estimate=64  expected=86.4  over by 28.1 h
```

### Cross-game recognition

**League of Legends (2026 schedule).** The public calendar fixes dates a year out and leaves contents open. The same logic as your patch, with a two-week cycle and a whole studio behind it.

**The Last Guardian and Duke Nukem Forever.** PR101 week 6 scored their announced release dates as ratios of about 2.9 and 10. Those are fixed-scope projects that let the date move. In a live game, the date cannot move that way without players leaving, so the ratio has to be absorbed by scope instead.

**Your own sprints.** Your plan ratio fell from 1.50 to 1.21 over four sprints. Using the four-sprint `R` of 1.35 rather than the last sprint's 1.21 is a choice. Patch work is mostly fixing live bugs, which is harder to estimate than feature work, so the older, higher ratio is the safer one. Week 14 checks whether that was right.

### Eyes-open design judgment

- **Value per hour is a heuristic.** It ignores dependencies, risk and fun. Keep the rule, then argue openly for an exception and write it down. Moving the guild bank ahead of the ash storm because your guild players are your most loyal is a legitimate choice; doing it silently is not.
- **Players affected is not the same as value.** A fix that touches 60 new players in the tutorial may matter more than an event for 120 regulars, because new players are the ones deciding whether to stay (MMO308 week 3). Use the number, then look at who the players are.
- **Slack is not a gift.** The 5.6 hours of slack will almost certainly be spent on the next incident. Do not fill it with the UI scale option.
- **An event is the riskiest item.** It has content, a schedule and an announcement. If it slips, players notice. Put it last in the cut order unless it is the reason for the patch.

### Check this example

1. Another team has `H = 50`, `X = 8` and `R = 1.6`. What is its estimate budget?
2. Emberfall's SEV1 exploit fix turns out to need 12 estimated hours, not 4. Rerun the rule. What is cut?
3. Why is it wrong to plan with `E = H / R` and treat release work as part of the slack?

<details>
<summary>Answers</summary>

1. `A = 42`, `E = 42 / 1.6 = 26.3` estimated hours.
2. Must-fix items now take 18. Tutorial (21), ranger (25), fast travel (33) fit. The ash storm would make 47, over 43.2, so it is cut. UI scale fits at 38. The guild bank would make 58, so it is cut. The plan is 38 estimated hours, 51.3 expected actual, with 7.0 hours of slack. Cutting the ash storm is the right call even though it has the most players, and it is the item the cut order put first.
3. Release work is not uncertain in the same way. It has to happen, and it happens at the end, when overruns have already eaten the time. Slack exists for surprises. If release work lives inside it, the first surprise removes your regression pass.

</details>

## 4. Freeze, go/no-go and cut order

Three dates and one list make the plan hold.

- **Feature freeze.** After this, no new items enter the patch. Set it at least three days before release.
- **Code freeze.** After this, only fixes for bugs found in the release candidate go in, each approved by the producer. Set it at least one day before release, so the regression pass runs on the build you ship.
- **Release day.** Pick a day and time when at least two team members are online for four hours after the deploy. Not Friday evening.
- **Go/no-go criteria.** Write them down before code freeze. A typical set is zero open SEV1 issues, no SEV2 issues introduced by the patch, the regression checklist passed, and the rollback tested on the staging server. If any criterion fails on release day, the patch waits or the failing item is cut, following the cut order.

Ship it the way MMO308 week 9 described. Deploy to a small share of players or one zone first, watch the crash rate and the error log for a fixed time, then expand. Keep the previous build ready to restore.

## 5. Patch notes and the week after

Patch notes are for players. Write them in player terms ("Items are no longer lost if you disconnect while trading"), group them by what players do, and credit players who reported bugs if they agreed. MMO308 week 10 shows how the notes also start the next round of feedback.

Then measure. For every item in the patch, write the number you expect to move and check it a week later: tickets for item loss, D1 for the tutorial fix, ranger pick rate for the balance pass. An item with no expected number is an item you cannot learn from. Week 14's post-mortem uses these numbers.

## Studio session plan

The studio meeting runs 180 minutes with one break.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:15 | Instructor briefing: fixed date, `A`, `R`, `E`, cut order | Notes |
| 0:15-0:40 | Compute `H`, `X`, `A` and `R` from lab 11 and sprint records (lab 12, part A) | Budget sheet |
| 0:40-1:20 | Build the candidate list with estimates and players affected; run the selection rule (part B) | Patch plan and cut order |
| 1:20-1:30 | Break | |
| 1:30-2:00 | Write freeze dates, go/no-go criteria and rollout steps (part C) | Release plan |
| 2:00-2:30 | Pair review: another team tries to break your plan by adding one surprise (a new SEV1 bug, a sick teammate). Apply your cut order live | Revised plan |
| 2:30-3:00 | Draft patch notes and the expected-number list (part D); instructor sign-off | Sign-off |

## Deliverables

Due at the end of week 12, in `production/week12/` in the team repository.

1. **Lab 12 worksheet**, parts A to D. Checked by recomputing `A`, `R`, `E`, the expected actual hours and the slack.
2. **The patch itself**, tagged with a version and build number, live for all players by the end of week 12 or held by a recorded no-go decision. Checked by the build tag and the deploy log.
3. **Release record.** The go/no-go decision with each criterion marked, rollout steps with times, and any cut made with the reason. Checked against the plan.
4. **Patch notes** as published to players, and the expected-number list.

## Common failure modes

- **Comparing raw estimates with hours.** This assumes `R = 1`. Your own sprints say otherwise.
- **Forgetting release work.** The regression pass is the first thing a late patch skips, and the thing that would have caught the bug that causes the hotfix.
- **Treating the cut order as a failure plan.** It is part of the plan. Cutting the ash storm on schedule is success.
- **Adding items after feature freeze because "it's tiny".** Tiny items have ratios too.
- **Friday deploys with no one online.** A patch that breaks at 23:00 with nobody watching becomes a weekend outage.
- **Patch notes written for the team.** "Refactored inventory sync" means nothing to a player. Say what changes for them.

## Review checklist

The instructor checks, at the week 13 meeting:

- [ ] `A`, `R`, `E` are computed from lab 11 and the sprint records and recompute correctly.
- [ ] Every must-fix SEV1 or SEV2 bug is in the patch or has a written reason and a hotfix plan.
- [ ] The selection follows the stated rule, or each exception is written down with its reason.
- [ ] Expected actual hours and slack are stated, and the cut order exists in writing before feature freeze.
- [ ] Freeze dates, go/no-go criteria and a tested rollback were written before code freeze.
- [ ] The patch shipped with a version tag and a staged rollout, or a no-go decision is recorded against a criterion.
- [ ] Patch notes are in player terms, and each item has an expected number to check in week 13.

## Sources

- Riot Games Player Support, "Patch Schedule: League of Legends" (support.riotgames.com, read September 2026). The 2026 schedule of 24 patches from 26.01 (8 January 2026) to 26.24 (9 December 2026); the statement that patches release on a Wednesday, Pacific time, unless otherwise indicated; four dates marked Thursday (26.01, 26.02, 26.04, 26.18).
- The Emberfall team, its sprint records, patch candidates and player counts are a constructed example for teaching. They are not data from any real team.

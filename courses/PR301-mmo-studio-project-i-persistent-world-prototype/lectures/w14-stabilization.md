# PR301 · Week 14 — Stabilization

**Why this matters:** The beta found more bugs than your team can fix before the showcase. That is normal, and it is the reason this week exists. From today no new features go in. The question is which bugs you fix, which you remove by flipping a kill switch, and which you ship with and say so. You ran the same kind of review in week 8 before the alpha. Two things are different now. There is no "next sprint" after this one, so a fix that breaks something else has nowhere to go. And the showcase build is the one that gets marked, so the release itself (branch, candidate, backup, install) needs hours of its own. This week you budget the must-fix list with regressions counted, close the gap without touching the data rules, and freeze a candidate you can show, back up and restore.

**You will be able to:**
- Triage beta bugs with the week 8 persistent-world scale and justify every S2 and S3 with beta frequency from telemetry.
- Extend the week 8 fix budget with a measured reopen rate, and compare the result with the hours the team has after reserving release work.
- Close a gap between demand and capacity by flipping a tested kill switch or reclassifying with evidence, and know which bugs may never be reclassified.
- Freeze a release candidate on a release branch, with a release checklist, a tested backup and restore, a clean install and a soak test.

**Before class:** Bring the beta telemetry export, observer notes and restart drill record from week 13. Export the tracker's closed bugs from sprints 1 to 5 with severity, hours logged and whether each was reopened. Re-read [week 8](w08-sprint-3-review.md), sections 2 to 4 (20 minutes) and PR101 week 13, section 4 on the release checklist (15 minutes). Skim MMO308 week 9, section 3 on hotfix decisions (10 minutes).

**Prerequisites from earlier courses:** [PR101 week 10, bug tracking and QA basics](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md) (severity, priority and the find-and-fix backlog model). [PR101 week 2, git branching](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w02-git-fundamentals-and-branching.md) and [PR101 week 13, builds and release checklists](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w13-builds-and-release-checklists.md). [PR101 week 12, crunch](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w12-crunch-causes-costs-alternatives.md). [PR101 week 14, post-mortems as a practice](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w14-post-mortems-as-a-practice.md) (for next week). [MMO407 week 12, writing a post-mortem](../../MMO407-launch-scaling-and-post-mortems/lectures/w12-writing-a-post-mortem.md) returns to post-mortems in year 4. [MMO308 week 9, patch management and hotfixes](../../MMO308-live-operations-analytics-and-experimentation/lectures/w09-patch-management-and-hotfixes.md). [MMO302 week 8, item ownership and transactional integrity](../../MMO302-mmo-server-architecture/lectures/w08-item-ownership-and-transactional-integrity.md). From this course, [week 8](w08-sprint-3-review.md) (severity, the fix budget and kill switches), [week 13](w13-beta-open-class-playtest.md) (the beta evidence) and the [syllabus](../syllabus.md).

---

## 1. What stabilization means

Stabilization is a period in which the team changes the game only to make it more reliable. Three rules start at the beginning of the week 14 studio meeting.

- **Feature freeze.** No new features, no new content, no "small" additions. A change that adds something a player could notice is a feature.
- **Every merge names a bug.** Each commit on the release branch references a tracker ID. No bug, no merge.
- **A release branch.** Cut it from main at the freeze (PR101 week 2). Fixes go to the release branch first and are merged back to main. Anyone who wants to keep building after the course does it on main, where it can't reach the showcase build.

The rules feel slow, and that is the point. PR101 week 10 shows the arithmetic: every fix carries a chance of a regression, and every feature carries more. Late changes are where final builds break, including at studios that know better (section 6).

## 2. Triage with the week 8 scale

Use the persistent-world scale from week 8 without changes. S1 is anything that crashes the server, corrupts saved state, loses progress, or creates or destroys value, at any frequency. S2 blocks a feature the showcase needs with no workaround. S3 is wrong but survivable. S4 is cosmetic.

Two rules matter more now than in week 8.

- **Never downgrade a data bug to make the list fit.** A duplication seen once in the beta is still S1. Its cost is not how often it happened. It is that it can be repeated on purpose once someone finds the steps. The same holds for a crafted item lost at a save.
- **Frequency comes from evidence.** Every S2 and S3 in the triage table carries how many beta sessions or players hit it, from the telemetry export, as in the week 10 review. "Happened once to one tester" and "8 of 57 players" are different bugs, and only evidence lets you tell them apart.

## 3. The fix budget, with regressions

Week 8 gave the model: must-fix bugs are the open ones plus the expected arrivals minus the ones you may leave open, each multiplied by the mean hours to fix its severity. Stabilization adds one term, because there is no later sprint to absorb rework.

```
must_fix work    = Σ over S1 and S2 of (B + λ·T) × h           (week 8, with allowed = 0)
reopen rate      q = fixes reopened / fixes closed, from sprints 1 to 5
effective demand = must_fix work / (1 − q) + kill-switch checks
fix capacity     = team hours to the showcase − hours reserved for release work
```

Dividing by `1 − q` counts rework. If 15% of fixes come back, each hour of fixing produces 0.85 hours of lasting progress. Take `λ`, the arrival rate, from your own internal testing in sprint 5, not from the beta. Fifty strangers found bugs faster than your team will this week.

The release work you reserve hours for is not optional: the release checklist, the backup and restore drill, the soak test, the showcase build and rehearsal, and collecting the post-mortem evidence. A team that spends those hours on bugs arrives at the showcase with a build nobody has installed from scratch.

## 4. Kill switches and reclassification

Week 8 had you build and test a kill switch for every system that can create or destroy value: player trade, the market, mail attachments, crafting stations. Now they earn their keep. A system behind a switch can be turned off for the showcase, which removes all of its bugs from the must-fix list at the cost of re-checking the switch on the release candidate. Three conditions make it the right call:

- The system holds an S1 or several S2 bugs.
- The world still meets the course brief without it. Check the brief, not your pillars. You can't switch off the encounter.
- The switch is already built and tested. If it isn't, building it now is a feature and falls under the freeze.

Reclassification is the other tool. An S2 in content the showcase route never touches can move to S3 if you close that content off and your beta telemetry shows how few players reached it. Reclassification is never allowed for S1 bugs, for anything that loses data, or for anything that crashes.

Write every switched-off system and every reclassification into the showcase notes and the post-mortem. A system you switched off with a reason is a production decision. A system that corrupts the database during the showcase is a failure.

## 5. Freezing the release candidate

By the end of the week you tag a release candidate on the release branch and run the PR101 week 13 release checklist against it, with three additions for a persistent world:

- **Backup and restore.** Back up the world database, restore it into a clean environment, start the server against it and log in as three named characters. The week 9 drill proved the procedure. This proves it on the build you will show.
- **Clean install.** A teammate who did not build the candidate installs the client from the release artifact on a machine that has never run the game.
- **Soak.** Run the candidate for two hours at 50 bots and watch memory and p99 tick for slow growth that a ten-minute test never shows.

Tag the candidate with a version and changelog (PR101 week 13, section 3). Any change after the tag produces a new candidate and a new pass of the checklist. The showcase build in week 15 is the last candidate that passed.

Collect the post-mortem evidence while it exists: the beta exports, the triage table, the sprint 4 and 5 burn-downs, and your capacity and turnout numbers. PR101 week 14 and MMO407 week 12 describe what the post-mortem does with them.

## 6. Worked example: can the *Saltmarsh* team close its must-fix list?

### The hook

CCP released EVE Online's Trinity expansion at 22:04 GMT on Wednesday 5 December 2007. Players who took the optional graphics content upgrade soon reported that it deleted `C:\boot.ini`, a Windows start-up file, and some computers would not boot until it was repaired. CCP's own account explains how. Late in development the team switched the upgrade from its patching tool to an installer with better compression, which shrank the download from about 866 MB to 584 MB. The installer script was committed on 30 November and tested on the Singularity test server from 2 December. It told the installer to delete `boot.ini` without a full path, and the installer took that to mean the root of the drive. The faulty upgrade was pulled a few hours after the problem was found, the fix was made at 06:08 GMT on 6 December, and fewer than 215 players contacted CCP as affected. The change was sensible, and it ran on the test server first. It still reached players five days after it was written, on a path that no earlier release had used. The freeze and the release checklist exist for changes like that one.

### The list after the beta

After triage with the week 8 scale, the *Saltmarsh* team has:

| Severity | Open `B` | Notes |
|---|---|---|
| S1 | 3 | Crafted item lost if made seconds before a save (the week 13 restart drill); item duplication when a market listing is bought during the save that precedes a restart; guild roster entry lost when two members leave at once |
| S2 | 9 | Four in the market; a client crash when leaving the cistern during loot; three visual bugs in the north reed beds, one of which hides a mob's health bar; one in guild chat |
| S3 | 24 | |
| S4 | 18 | |

The showcase bar is every S1 and every S2.

### The team's own history

From the tracker, sprints 1 to 5, and sprint 5's internal testing:

```
mean hours to fix    h(S1) = 6.0     h(S2) = 3.0
closed fixes 60, reopened 9          q = 9 / 60 = 0.15
arrivals in internal testing          about 4 S2 a week, none S1, so λ·T = 4 S2 over the period
```

### Demand

```
S1          3 × 6.0                          = 18.0 h
S2          (9 + 4) × 3.0                    = 39.0 h
must_fix work                                = 57.0 h
effective   57.0 / (1 − 0.15)                = 67.1 h
```

### Capacity

The team has seven people at the week 3 figure of 6.5 available hours a week each, after coordination.

```
week 14      7 × 6.5                         = 45.5 h
reserved     release checklist 3, backup and restore 2, soak setup 1,
             post-mortem evidence 3, showcase build and rehearsal 5    = 14.0 h
week 14 fix hours                            = 31.5 h
week 15      two working days before the showcase, fix share           = 14.0 h
fix capacity                                 = 45.5 h
```

Demand is 67.1 hours against 45.5. The gap is 21.6 hours, nearly half of capacity. Working weekends would close it on paper. PR101 week 12 explains why that plan fails: tired fixes regress more, which raises `q`, and `q` sits in the denominator.

### Option A: flip the market kill switch

The market holds one S1 (the duplication) and four S2 bugs. Its kill switch was built and tested in week 8. The world still meets the brief without it: players can still trade face to face, sell to vendors and buy from them, and the crafting chain works. Re-checking the switch on the release candidate takes half an hour, the week 8 figure.

```
removed      1 × 6.0 + 4 × 3.0 = 18.0 h of work, 18.0 / 0.85 = 21.2 h effective
added        0.5 h to re-check the switch
new demand   67.1 − 21.2 + 0.5 = 46.4 h
```

That is 46.4 hours against 45.5, still 0.9 hours over, with no margin for anything going wrong.

### Option B: reclassify with evidence

The three visual bugs in the north reed beds are S2 only because one of them hides a mob's health bar. The beta telemetry shows that 2 of 57 players went there, and the showcase route doesn't. The team closes the reed beds to the showcase path with a gate and moves the three bugs to S3, with the telemetry numbers in the triage note. None of them touches stored data or crashes anything, so section 4 allows it. The gate is a closed door placed in the level, inside the 5 hours reserved for the showcase build.

```
removed      3 × 3.0 = 9.0 h of work, 9.0 / 0.85 = 10.6 h effective
```

### Options A and B together

```
remaining must-fix   S1: 2 × 6.0 = 12.0 h     S2: (2 + 4 arrivals) × 3.0 = 18.0 h
effective            30.0 / 0.85             = 35.3 h
plus the switch check                         0.5 h
demand                                       = 35.8 h against 45.5 h
margin                                       = 9.7 h, 21% of capacity
```

The team takes both. It writes the market into the showcase notes as "disabled for the showcase after a duplication bug found in the beta". It keeps the duplication bug open at S1 on main, because the switch hides the bug and doesn't fix it.

What the team did not do matters as much. It did not downgrade the item lost at a save, though it needs a window of seconds to happen. It did not reclassify the client crash, though it only happens when leaving the cistern during loot. It did not cut the backup and restore drill to win 2 hours. And nobody worked the weekend.

### Checking during the week

The model gives a plan, not a result. The team tracks one number each evening: open must-fix bugs, including any found that day. With 35.8 hours of demand spread over seven working days, the list should be a little under half done by Wednesday of week 14. If it isn't, the next candidate is the second S1, the guild-leave race. A kill switch doesn't exist for it, so the fallback is to disable the "leave guild" button, which the freeze allows only as a fix for a tracked S1, reviewed by a second person.

### What the example shows

A must-fix list that doesn't fit is not a reason to work longer. Measure demand from your own history, with regressions and arrivals counted. Close the gap with the tool that removes the most bugs per hour. The week 8 kill switch removed five bugs for half an hour of checking. Reclassification removed three, with evidence. Nothing about the data rules was relaxed.

### Check this example

1. If the team's reopen rate had been 25% instead of 15%, what would the demand be with options A and B?
2. A teammate proposes closing the market duplication bug as "won't fix, feature disabled". Why does the team keep it open?
3. Why use the sprint 5 internal-testing arrival rate rather than the beta's?

<details>
<summary>Answers</summary>

1. `30.0 / 0.75 + 0.5 = 40.0 + 0.5 = 40.5 h` against 45.5. The margin falls to 5.0 hours, 11% of capacity. The team should name its next switch-off or reclassification before the week starts.
2. The switch stops new duplicated items during the showcase, but the code is still wrong. Anyone who turns the market back on after the course reintroduces the exploit. The bug stays open on main with a note about the switch.
3. This week the testers are the team, at the team's pace, not 57 strangers at once. The beta rate would overstate arrivals. The team's own rate from the same kind of testing is the closer match.

</details>

## Studio session plan

The studio meeting runs 180 minutes with one break. The feature freeze starts when it begins.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:10 | Instructor briefing: freeze rules, the reopen term, kill switches and reclassification | Freeze announced |
| 0:10-0:25 | Cut the release branch; protect it so every merge needs a bug ID | Release branch |
| 0:25-1:10 | Triage the beta bugs with the week 8 scale; beta frequency from telemetry for every S2 and S3 | Triage table (lab 14) |
| 1:10-1:20 | Break | None |
| 1:20-1:50 | Compute demand and capacity from tracker history; run the lab 14 checker | Budget that passes, or a gap |
| 1:50-2:25 | Close the gap: kill switches and reclassifications, checked against the course brief. Pair with another team to challenge each reclassification | Decisions with evidence |
| 2:25-3:00 | Assign the must-fix list; schedule the backup and restore drill and the soak test; instructor walk-round signs off each budget | Assigned list, dates |

## Deliverables

Due at the start of the week 15 studio meeting, in the team repository under `production/week14/`.

1. **Triage table and fix budget** (lab 14) that pass `check_stabilization.py`. Checked by rerunning the checker and tracing two severities to beta evidence.
2. **Release branch** with every merge since the freeze referencing a bug ID. Checked by reading the branch log.
3. **Release candidate** tagged with version and changelog, with the PR101 week 13 checklist completed against it. Checked by installing from the release artifact.
4. **Backup and restore record** on the candidate, with three characters checked after the restore.
5. **Soak test**: two hours at 50 bots on the candidate, with memory and p99 tick exports. Checked for slow growth.
6. **Daily must-fix count** from freeze to candidate, and the showcase notes for any switched-off system.
7. **Post-mortem evidence folder**: beta exports, triage table, sprint 4 and 5 burn-downs, capacity and turnout numbers.

## Common failure modes

- **"One small feature" after the freeze.** It is how final builds break. Put it on main for after the course.
- **Downgrading a data bug because it was rare.** A duplication that happened once can happen a thousand times once someone finds the steps.
- **Estimating fixes in the meeting.** Use tracker history. Deadline estimates are the most optimistic a team makes.
- **Leaving out regressions and arrivals.** A plan that assumes every fix sticks and nothing new turns up is short by a fifth or more.
- **Closing the gap with overtime.** Tired fixes regress more, and the gap grows.
- **Building a kill switch during the freeze.** An untested switch is a new feature. Use the ones from week 8, or fix the bug.
- **Closing a bug because its system is switched off.** The switch hides it. Keep it open on main.
- **A backup nobody restored.** Until it has been restored and logged into on this build, you don't know that it works.
- **Spending the reserved hours on bugs.** The checklist and the rehearsal are what get the fixed build to the showcase.

## Review checklist

The instructor checks, at the week 15 meeting:

- [ ] Every S1 is a server crash or a stored-state bug under the week 8 scale, and none was downgraded.
- [ ] Every S2 and S3 has beta frequency from telemetry in its triage note.
- [ ] Fix hours and the reopen rate come from the tracker, and demand includes expected arrivals.
- [ ] Demand is at or below capacity after the team's decisions, with the margin stated.
- [ ] Each switched-off system uses a week 8 kill switch re-checked on the candidate, has a showcase note, and keeps its bugs open on main.
- [ ] Each reclassification is supported by telemetry and touches no stored data and no crash.
- [ ] The release branch log shows a bug ID on every merge since the freeze.
- [ ] The candidate passed the release checklist, a clean install, a two-hour soak and a restore test.
- [ ] The post-mortem evidence folder is complete.

## Sources

- CCP Explorer (Erlendur S. Thorsteinsson), "About the boot.ini issue", EVE Online dev blog, 11 December 2007. Trinity released at 22:04 GMT on 5 December 2007; the Classic to Premium graphics content upgrade deleted `C:\boot.ini`; late switch from patching to installer technology, shrinking the download from about 866 MB to 584 MB; installer script committed 30 November 2007, first released on Singularity on 2 December; `Delete` without a full path defaults to the drive root; fix at 06:08 GMT on 6 December; faulty upgrade pulled a few hours after discovery; fewer than 215 users (170 by petition, 45 by phone) reported being affected. https://www.eveonline.com/news/view/about-the-boot.ini-issue
- NWDB, "All Forms of Trading Disabled Due to Coin Duplication Exploits" (2 November 2021), reporting Amazon Games' statement for New World. Trading post, player trading, coin transfer and guild treasury disabled while a gold duplication exploit was fixed. Cited in week 8 as the model for kill switches. https://nwdb.info/news/all-forms-of-trading-disabled-due-to-coin-duplication-exploits
- PR101 weeks 2, 10, 12, 13 and 14, MMO308 week 9, MMO302 week 8 and MMO407 week 12 (this program) for branching, severity and backlog models, crunch, release checklists, post-mortems, hotfixes and transactional integrity, with their sources.
- The *Saltmarsh* team's bug counts, fix times, reopen rate and hours are a constructed teaching example, not data from any real team.

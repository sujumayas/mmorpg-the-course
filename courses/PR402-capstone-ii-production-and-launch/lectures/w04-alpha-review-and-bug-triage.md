# PR402 · Week 04 — Alpha: the review, the bug bar and triage by reach

**Why this matters:** Alpha is the first time people outside your team play your game on your servers. They will find more bugs in two hours than you can fix in a week, and next week's closed beta testers will meet whatever you leave open. Which bugs you fix this week decides whether closed beta produces useful data or a Discord full of the same complaint.

**You will be able to:**
- Run an alpha review against your exit criteria and log findings in a form that supports triage.
- Estimate each bug's reach and compute its expected impact on next week's testers.
- Separate gate bugs, which must be fixed whatever they cost, from bugs ranked by impact per fix hour.
- Fill a week's fix capacity and state whether the build meets the closed beta bug bar.

**Before class:** Your alpha build is tagged and deployed (week 3 deliverable). Print your alpha exit criteria. Reread [PR101 week 10, sections 1 and 4](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md) on bug reports and running QA. Read Microsoft's "SDL Security Bug Bar (Sample)" on learn.microsoft.com, the definitions section only (10 minutes).

**Prerequisites from earlier courses:** [PR101 week 10, bug tracking and QA basics](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md) (bug stock, find and fix rates). [MMO407 week 6, duplication exploits after launch](../../MMO407-launch-scaling-and-post-mortems/lectures/w06-case-duplication-exploits-after-launch-new-world-2021.md). [MMO308 week 13, incident response](../../MMO308-live-operations-analytics-and-experimentation/lectures/w13-incident-response.md). [MMO302 week 8, item ownership and transactional integrity](../../MMO302-mmo-server-architecture/lectures/w08-item-ownership-and-transactional-integrity.md). [PR402 week 3](w03-production-sprint-3-feature-complete-and-server-budget.md) (alpha exit criteria).

---

## 1. What alpha is for

Alpha has two jobs, and they pull in different directions.

The first job is a **gate**. The instructor and a partner team check your build against the exit criteria you wrote in week 3. A criterion either passes or it does not, and the result goes into your milestone grade.

The second job is **discovery**. Strangers play your game and break it in ways you did not imagine. You want as many of those breaks as possible, written down well enough to reproduce.

The gate rewards a smooth demo. Discovery rewards letting testers go wherever they like. Run them as two separate blocks in the session plan below. First the scripted criteria check, then an hour of free play with everyone logging bugs.

## 2. A bug report that supports triage

[PR101 week 10](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md) set out the basic report: title, steps, expected, actual, build. For a live game add three fields, because triage needs them:

- **Severity.** How bad it is for one player who hits it. Use this scale all semester:

| Level | Meaning | Examples |
|---|---|---|
| S1 | Crash, data loss, progress blocked, security or economy exploit | Client crash, lost character, gold duplication |
| S2 | A feature fails, a workaround exists | Quest cannot complete if the party changes; login takes a minute |
| S3 | Works, but wrong or confusing | Mob walks through a wall; chat drops a message |
| S4 | Cosmetic | Typo, clipping, misaligned icon |

- **Reach.** The share of play sessions in which a player meets the bug. Estimate it from the report ("happened every time I entered the market" suggests high reach) and correct it later with telemetry.
- **Fix estimate.** Hours to fix and verify, from the person who will fix it.

From closed beta on, your game is live to outsiders, and a live problem also gets an incident level from the severity table in [MMO308 week 13](../../MMO308-live-operations-analytics-and-experimentation/lectures/w13-incident-response.md), SEV1 to SEV3. The two scales answer different questions. S1 to S4 say how bad a bug is for one player who meets it, and they stay on every tracker ticket. SEV1 to SEV3 say how urgently the live service needs a response. Every later guide maps one to the other with this rule:

| Bug | Incident level |
|---|---|
| Data loss or a value-path exploit (the gate classes in section 3), or most players unable to log in or play | SEV1 |
| Any other S1 (crash, progress blocked), or an S2 that most sessions meet | SEV2 |
| Every other S2, and every S3 and S4 | SEV3 |

Severity alone is what most teams sort by. It answers "how bad is this for the player who hits it?" It does not answer "how many players will hit it?" That second question is what decides where a week of fixing does the most good.

## 3. Gates, impact and the bug bar

Triage splits bugs into two groups.

**Gate bugs** are fixed this week whatever the arithmetic says. In this course three kinds of bug are gates:

- anything that loses or corrupts player data;
- any exploit on a value path (items, currency, experience), however rare, because exploits are found deliberately and spread by word of mouth ([MMO407 week 6](../../MMO407-launch-scaling-and-post-mortems/lectures/w06-case-duplication-exploits-after-launch-new-world-2021.md));
- any S1 with reach of 1% of sessions or more.

**Everything else** is ranked by expected impact per fix hour:

```
impact    I = sessions × reach × weight(severity)
priority  p = I / fix hours
```

- `sessions` is the number of play sessions expected next week.
- `weight` turns severity into a number: S1 = 10, S2 = 4, S3 = 1, S4 = 0.2. The weights say an S1 hurts a player about ten times as much as an S3. They are a team choice, and you should argue about them once, now, rather than for each bug.
- `I` is weighted sessions harmed per week.

The **bug bar** is the rule for entering closed beta. For this course it is: every gate bug fixed and verified, and the remaining open impact written down with a plan for each item. A build that misses the bar goes to closed beta a day late, not with a known data-loss bug.

## 4. Worked example: the login that nobody filed as S1

### The hook

On 13 September 2005 World of Warcraft added Zul'Gurub, a raid whose final boss cast a debuff called Corrupted Blood. It drained health and jumped between nearby characters, and it was meant to end when players left the raid. Hunters' pets could carry it out, because a pet dismissed while infected kept the debuff when summoned again. Within days it was spreading through the capital cities, killing low-level characters in crowds. Blizzard tried quarantines and rolling restarts. The outbreak ended on 8 October 2005, after hard resets of the servers and a change that made pets immune.

Read that as a triage report. The severity was obvious once people were dying in Ironforge. What anyone would have got wrong in advance was the reach. A debuff inside one raid, meant for a few dozen players at a time, looks like a low-reach bug. The mechanism that carried it out, pets leaving and returning, touched every hunter in the game. Reach is a guess about how far a bug travels, and it is the number triage most often gets wrong.

### The model

Section 3's model, applied to a week of fix capacity:

```
I_b  = sessions × reach_b × weight(sev_b)
p_b  = I_b / hours_b
plan = all gates, then remaining bugs in descending p_b while hours fit
open = Σ I_b over bugs not in the plan
```

Filling a fixed budget in order of value per hour is the greedy approach to a knapsack problem. It is not always optimal, and the check at the end of the example shows how to catch the case where it fails.

### Numbers you can check

Emberfall's alpha produced nine bugs worth triaging. Closed beta next week plans for 150 active testers (week 5) playing about three sessions each, so `sessions = 450`. The week 4 ops tax from lab 01 is `84 × 0.45 = 37.8` hours. Not all of it is fixing. The team estimates 6.3 hours for deploys, the tester FAQ and closed beta accounts, which leaves 31.5 hours of fix capacity.

| Bug | Summary | Sev | Reach | Hours | Impact `I` | `I` per hour | Gate |
|---|---|---|---|---|---|---|---|
| B1 | Client crash when two players loot one chest at once | S1 | 2.0% | 6 | 90.0 | 15.00 | S1, reach ≥ 1% |
| B2 | Character lost if the zone server restarts during a trade | S1 | 0.2% | 12 | 9.0 | 0.75 | Data loss |
| B3 | Town-hold contract cannot complete if a party member leaves | S2 | 6.0% | 5 | 108.0 | 21.60 | |
| B4 | Login takes over 60 seconds with 30 or more players online | S2 | 25.0% | 8 | 450.0 | 56.25 | |
| B5 | Ash hound walks through the town wall | S3 | 15.0% | 3 | 67.5 | 22.50 | |
| B6 | Splitting a mark stack in town storage duplicates marks | S1 | 0.1% | 4 | 4.5 | 1.12 | Exploit |
| B7 | Zone server memory leak, crash after about 9 hours | S2 | 4.0% | 10 | 72.0 | 7.20 | |
| B8 | Typo in the town crier's greeting | S4 | 40.0% | 0.5 | 36.0 | 72.00 | |
| B9 | Guild chat drops messages after a zone change | S3 | 10.0% | 4 | 45.0 | 11.25 | |

Check one row. B4: `450 × 0.25 × 4 = 450`, and `450 / 8 = 56.25` per hour.

Total impact if nothing is fixed: 882.

**Severity first.** The usual habit: fix all S1s, then S2s in the order they were filed, and so on, while hours remain.

- S1s: B1, B2, B6, 22 hours.
- S2s: B3 fits (27 hours). B4 needs 8 and only 4.5 are left. B7 needs 10. Skipped.
- S3s: B5 fits (30). B9 does not.
- S4: B8 fits (30.5).

Open impact: `882 − (90 + 9 + 108 + 4.5 + 67.5 + 36) = 567`.

**Gates, then impact per hour.**

- Gates: B1, B2, B6, 22 hours.
- Then by `I` per hour: B8 (72.00) fits, 22.5 hours. B4 (56.25) fits, 30.5 hours. B5 (22.50) needs 3, only 1 left. Nothing else fits.

Open impact: `882 − (90 + 9 + 4.5 + 36 + 450) = 292.5`.

| Plan | Fixed | Hours | Open impact |
|---|---|---|---|
| Severity first | B1, B2, B6, B3, B5, B8 | 30.5 | 567.0 |
| Gates, then impact per hour | B1, B2, B6, B8, B4 | 30.5 | 292.5 |

Same hours, same gate bugs fixed, and the second plan leaves about half the harm. The difference is almost all B4, a slow login that nobody would call S1 and that a quarter of all sessions meet first thing.

Now the check on greedy. After the gates there are 9.5 hours. Could a different set of non-gate bugs beat B8 plus B4 (486 impact in 8.5 hours)? B4 plus B5 would be 517.5 in 11 hours, too many. B3 plus B5 plus B8 is 211.5. Nothing beats 486 inside 9.5 hours. When the leftover hours are small next to the bugs' sizes, try the two or three nearest alternatives by hand, as here.

This program reproduces both plans:

```python
SESSIONS = 450                      # closed beta sessions next week: 150 testers x 3
CAPACITY = round(84 * 0.45 - 6.3, 1)   # week 4 ops-tax hours minus non-fix ops work
WEIGHT = {1: 10, 2: 4, 3: 1, 4: 0.2}

# id: (severity, reach per session, fix hours, gate reason)
bugs = {
    "B1": (1, 0.020, 6, "S1 reach >= 1%"), "B2": (1, 0.002, 12, "data loss"),
    "B3": (2, 0.060, 5, ""), "B4": (2, 0.250, 8, ""), "B5": (3, 0.150, 3, ""),
    "B6": (1, 0.001, 4, "exploit"), "B7": (2, 0.040, 10, ""),
    "B8": (4, 0.400, 0.5, ""), "B9": (3, 0.100, 4, ""),
}
impact = {b: SESSIONS * r * WEIGHT[s] for b, (s, r, h, g) in bugs.items()}


def fill(order):
    used, fixed = 0.0, []
    for b in order:
        if used + bugs[b][2] <= CAPACITY:
            used += bugs[b][2]
            fixed.append(b)
    return fixed, used, sum(impact[b] for b in bugs if b not in fixed)


by_severity = sorted(bugs, key=lambda b: bugs[b][0])    # filing order within a severity
gates = [b for b in bugs if bugs[b][3]]
rest = sorted((b for b in bugs if b not in gates), key=lambda b: -impact[b] / bugs[b][2])
print("capacity", CAPACITY, "total impact", sum(impact.values()))
for name, order in (("severity first", by_severity), ("gates then per hour", gates + rest)):
    fixed, used, left = fill(order)
    print(f"{name}: {fixed} {used}h open {left:.1f}")
```

It prints:

```
capacity 31.5 total impact 882.0
severity first: ['B1', 'B2', 'B6', 'B3', 'B5', 'B8'] 30.5h open 567.0
gates then per hour: ['B1', 'B2', 'B6', 'B8', 'B4'] 30.5h open 292.5
```

### Cross-game recognition

- **START triage, 1983.** Staff at Hoag Hospital and the Newport Beach Fire Department in California designed Simple Triage and Rapid Treatment for incidents with many casualties. Responders sort by a few fast checks (can the person walk, breathing rate, pulse, following commands) into immediate, delayed, minor and expectant. They do not sort in arrival order or by how dramatic an injury looks. Your gates are "immediate". Your per-hour ranking is how you spend the time left.
- **Microsoft's SDL bug bar.** Microsoft's sample security bug bar rates severity partly by exposure. It separates "default or common" scenarios, defined as features active out of the box or reaching more than 10% of users, from narrower ones, and the same flaw can rate higher when it sits in the common path. That is reach built into the severity label rather than kept as a separate column.
- **New World, November 2021.** On 2 November Amazon turned off trading, coin transfers and the guild treasury to stop a coin duplication exploit ([MMO407 week 6](../../MMO407-launch-scaling-and-post-mortems/lectures/w06-case-duplication-exploits-after-launch-new-world-2021.md) has the timeline). The accidental reach of a dupe is tiny. Its real reach is everyone who hears about it. That is why exploits are gates here and never go through the impact formula.

### Eyes-open judgment

The model is only as good as the reach estimates, and alpha reach estimates are guesses from a few hours of play by a few people. Two habits limit the damage. First, when reach is uncertain, write a range and triage on the high end for S1 and S2 bugs. Second, add a telemetry event for each open S2 so closed beta measures its real reach, which week 6 will use.

Workarounds change reach, sometimes in both directions. Emberfall could avoid fixing B7 by restarting zone servers every six hours, which costs half an hour of setup. That drops B7's reach to near zero. It also makes restarts routine, and B2 loses characters when a restart hits a trade. A workaround for one bug can raise the reach of another. Check the list for interactions before you adopt one.

The weights are value judgments. A team whose pillar is "your home is safe" may weight data loss far above 10, and a competitive game may treat any unfairness as S1. Change the weights if your pillars demand it, write down why, and then apply them consistently.

Finally, do not let the formula bury a bug that is small today but grows. A memory leak that crashes after nine hours of uptime with 30 players may crash after two hours with 100. Scale the reach to the load you expect at launch, not the load you saw at alpha.

## 5. The closed beta go or no-go

At the end of the week, one decision: does the build meet the bar?

- **Go** if every gate bug is fixed and verified on staging, and the open list has an owner and a plan for each S1 and S2.
- **No-go** otherwise. Move the closed beta start by a day, tell testers, and fix the gate. A day's delay costs one day. A data-loss bug in closed beta costs the testers' trust, and they are the players you want at launch.

Record the decision and the open impact number in the milestone log. Week 5 starts from it.

A no-go is survivable. Emberfall's own record, reviewed in [week 14](w14-post-mortem.md), shows a no-go on the B6 fix and its closed beta starting a day late in week 5, with every later milestone on its planned week.

## Studio session plan

Week 4 meeting, alpha review, 3 hours.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:10 | Brief: severity scale, report fields, the two blocks | |
| 0:10-0:55 | Block 1, the gate: instructor and partner team run your exit criteria on the production build | Criteria marked pass or fail, signed |
| 0:55-1:45 | Block 2, discovery: partner team plays freely for 50 minutes; your team observes and logs | Bug reports with severity, reach guess, repro steps |
| 1:45-1:55 | Break | |
| 1:55-2:30 | Triage (lab 04): merge duplicates, estimate hours, mark gates, run `check_triage.py` | `bugs.csv` passing the checker |
| 2:30-2:50 | Instructor round, 4 minutes per team: gates, top three by impact per hour, one reach estimate defended | Notes on the board |
| 2:50-3:00 | Plan the fix week; schedule the go or no-go check | Fix board live |

## Deliverables

Due at the end of the week 4 meeting:

1. **Signed alpha criteria sheet**, with every criterion marked pass or fail by the instructor or the partner team.
2. **Triage sheet** in the lab 04 format ([`labs/lab04.md`](../labs/lab04.md)). The instructor reruns `check_triage.py`. It must print `PASS`.
3. **Fix plan** on the board: gate bugs first, then the ranked list to capacity.

Due at the start of week 5: the go or no-go record, with every gate bug verified on staging and the open impact number stated.

## Common failure modes

- **Triage by severity alone.** Everything S1 first, then filing order. The high-reach S2 that every tester meets on login waits until after launch.
- **Treating an exploit as rare.** Accidental reach is small. Deliberate reach is everyone who reads the forum. Exploits are gates.
- **Demo mode at alpha.** The team drives the partner team through a safe path and finds nothing. Run the gate check, then let them roam.
- **Reports without repro steps.** "Crashed near the market" costs an hour to find. Fill the template during play, not after.
- **Workarounds without a check.** Scheduled restarts hide a leak and make the restart-during-trade bug routine.
- **Filling the week with S4s because they are quick.** One typo with high reach is worth a half hour. Ten of them are not worth a gate bug slipping.

## Review checklist

The instructor checks at the alpha review and at the start of week 5:

- [ ] Every exit criterion from week 3 is marked pass or fail and signed.
- [ ] Failed criteria have a story in the fix plan or a written cut.
- [ ] Every bug has severity, reach, hours and repro steps; duplicates are merged.
- [ ] Gate bugs are marked by the course rules and all fit in the week's capacity.
- [ ] Non-gate bugs are planned in descending impact per hour, or a departure is explained.
- [ ] Planned hours do not exceed the week 4 ops-tax hours from lab 01 less the non-fix ops work.
- [ ] Open S2 bugs have a telemetry event planned to measure real reach.
- [ ] At the start of week 5: go or no-go recorded, gate bugs verified on staging.

## Sources

- Wikipedia, "Corrupted Blood incident" (read September 2026). Zul'Gurub added on 13 September 2005; Hakkar's Corrupted Blood debuff meant to expire at the end of the fight; carried out by hunters' pets dismissed while infected; spread in capital cities; quarantine zones and rolling restarts failed; hard resets and pet immunity on 8 October 2005.
- Wikipedia, "Simple triage and rapid treatment" (read September 2026). Developed in 1983 by staff of Hoag Hospital and the Newport Beach Fire Department; categories immediate, delayed, minor and expectant; checks for walking, respiration, perfusion and mental status.
- Microsoft, "SDL Security Bug Bar (Sample)", learn.microsoft.com (page dated March 2025, read September 2026). Severity levels Critical, Important, Moderate and Low; "default/common" defined as features active out of the box or reaching more than 10 percent of users.
- NWDB, "All Forms of Trading Disabled Due to Coin Duplication Exploits", 2 November 2021, as cited in MMO407 week 6. Trading post, player trading, coin transfers and guild treasury disabled.
- The Emberfall bugs, reach estimates, fix hours, severity weights and session counts are invented for teaching.

# PR402 · Milestone 2 brief: alpha

**Weight:** 8% of the course grade, inside the milestones component (40%).
**Assigned:** week 3. **Due:** the alpha review in the week 4 meeting. The go or no-go record is due at the start of week 5.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guides:** [week 3](../lectures/w03-production-sprint-3-feature-complete-and-server-budget.md) (exit criteria) and [week 4, alpha review and bug triage](../lectures/w04-alpha-review-and-bug-triage.md). **Lab:** [04](../labs/lab04.md).

## What this milestone proves

That every system in the game exists, works with the others and runs where testers will run it, and that the team can decide which bugs to fix before strangers arrive. "Feature complete" in this course has the four meanings set in [week 3, section 1](../lectures/w03-production-sprint-3-feature-complete-and-server-budget.md): every kept system in and connected, no placeholder rules, server authority on every value path, and a build from the release pipeline on production.

Alpha has two jobs, a gate and discovery ([week 4, section 1](../lectures/w04-alpha-review-and-bug-triage.md)). This brief marks both. The gate is your exit criteria, run by the instructor and a partner team. Discovery is the quality of what you log during free play and what you do with it in the fix week.

## Gates

A build that fails a gate at the review has its rubric capped at 50 until the gate passes, and it must pass before the closed beta starts.

- **G1. Reachable.** The tagged alpha build is on production and a partner team joins it from outside the team's network.
- **G2. Server authority.** A reviewer tries one value-path cheat from the client (a modified loot, gold or XP message) and the server rejects it ([MMO302 week 8](../../MMO302-mmo-server-architecture/lectures/w08-item-ownership-and-transactional-integrity.md)).
- **G3. No known data loss at go.** At the go or no-go check, no gate bug in the data-loss or exploit class is open.

## Deliverables

1. **Signed alpha criteria sheet.** Every criterion from week 3 marked pass or fail by the instructor or partner team during block 1 of the review.
2. **Bug reports from block 2.** Title, steps, expected, actual, build, severity (S1 to S4), reach estimate and fix estimate, as in [week 4, section 2](../lectures/w04-alpha-review-and-bug-triage.md).
3. **Triage sheet** in the lab 04 format, passing `check_triage.py` with the sessions and capacity stated at the top of `check-output.txt`.
4. **Fix plan** on the board: gates first, then the ranked list to capacity.
5. **`telemetry.md`**: one reach event per open S2.
6. **`go-no-go.md`**: the decision, the date, the staging verification of each gate fix and the open impact number.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Build | Tag, release pipeline log, production deploy log | Confirms the reviewed build matches the tag and was not rebuilt by hand |
| Criteria | Signed sheet | Reruns two criteria live during the review |
| Playtest data | Block 2 bug reports with repro steps | Reproduces one S1 or S2 from its steps alone |
| Triage | `bugs.csv` and checker output | Reruns `check_triage.py`; recomputes one bug's impact per hour by hand |
| Capacity | Week 4 ops-tax hours from lab 01 less non-fix ops work | Checks the capacity passed to the checker matches lab 01 |
| Telemetry | Event names in `telemetry.md` and the build | Opens the code for one event and checks it fires on staging |
| Staging verification | Commit or deploy log for each gate fix, test notes | Checks every gate fix was verified on staging before the go decision |

## How it is marked

The alpha review follows the week 4 session plan. The instructor and the partner team run block 1 (the gate) from your criteria sheet, and nobody on your team drives. Block 2 is 50 minutes of free play by the partner team while your team observes and logs. Triage happens in the room. The instructor scores the review on the day and the go or no-go record at the start of week 5.

A criterion that fails at the review but passes within the fix week earns half its points in row 1. The lab 04 rubric is the detailed scoring guide for rows 3 to 5.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Exit criteria pass | 25 | All criteria pass at the review; each line is a test a stranger ran | Several fail, or lines were rewritten on the day to pass |
| Placeholder rules and authority | 10 | No placeholder logic; every value path decided on the server | A hard-coded table or client-decided loot found |
| Discovery quality | 15 | Reports have repro steps, severity and a reach guess written during play; duplicates merged | Reports written from memory after the session; "crashed near the market" |
| Triage (lab 04) | 20 | Gates marked by course rules; the rest ranked by impact per fix hour; departures explained; checker `PASS` | Severity-first ordering with no reason, or capacity exceeds lab 01 |
| Reach telemetry | 10 | One event per open S2, placed and firing | Events named but not in the build |
| Go or no-go | 15 | Decision recorded against the bar, gate fixes verified on staging, open impact stated; a no-go moves the date by a day and tells testers | Go with an open data-loss bug, or no record |
| Team conduct at review | 5 | Partner team given free play; no demo mode; the team logs rather than explains | The team steers testers down a safe path |
| **Total** | **100** | | |

## Builds on

- [PR401 week 7, technical design](../../PR401-capstone-i-pre-production/lectures/w07-technical-design.md) (the systems your criteria cover) and [PR401 week 11](../../PR401-capstone-i-pre-production/lectures/w11-production-plan.md), section 4 (every alpha item in sprints 1 to 3).
- [PR101 week 10, bug tracking and QA basics](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md) and [week 13, builds and release checklists](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w13-builds-and-release-checklists.md).
- [MMO302 week 8, item ownership and transactional integrity](../../MMO302-mmo-server-architecture/lectures/w08-item-ownership-and-transactional-integrity.md).
- [MMO308 week 13, incident response](../../MMO308-live-operations-analytics-and-experimentation/lectures/w13-incident-response.md) (why exploits are gates).
- [MMO407 week 6, duplication exploits after launch](../../MMO407-launch-scaling-and-post-mortems/lectures/w06-case-duplication-exploits-after-launch-new-world-2021.md).

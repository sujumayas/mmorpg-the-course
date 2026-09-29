# PR201 · Exam bank: viva and reflection questions

PR201 has no written exam. Each student sits a 15-minute viva in week 15 or the exam period, which is 30 of the 100 points in the [post-mortem and viva brief](post-mortem-brief.md). The same questions are prompts for the individual reflection and for sprint retrospectives.

## How the bank is used

- **In the viva.** Two examiners pick five or six questions and rewrite them with the team's own numbers: its fit sheet, velocity, message catalogue, telemetry and bug list. At least two questions must be about a part of the slice the student did not build. The repository and the build are open, and the student may look things up. Knowing where to look is part of the answer.
- **For practice.** Answer each question for your own slice before week 15. If you need a teammate to answer, ask them now, not in the viva.
- **Types.** Each question is tagged **explain** (say why, with a number from your project), **compute** (redo a calculation with your data), **critique** (find the weakness in a decision) or **reflect** (what you would do differently, as a checkable change).

## Marking scale for every question

Each question is marked 0 to 5. The viva row is `total / (5 × questions asked) × 30`.

| Mark | Meaning |
|---|---|
| 5 | Correct concept, applied with the team's real numbers or artefacts, trade-off stated, limits of the evidence acknowledged |
| 4 | Correct and specific, but one of numbers, trade-off or limits is missing |
| 3 | Correct in general terms; could be about any project |
| 2 | Partly correct, or correct only for the part the student built |
| 1 | Vague, or relies on a teammate's explanation the student cannot extend |
| 0 | Wrong, or no answer |

The guidance under each question lists what a 5 contains and what usually drags an answer down. Model numbers use the course's invented example teams unless the question says otherwise.

---

## A. Pitch, team and scope

Links: [PR201 week 1](../lectures/w01-pitch-and-team-formation.md), [PR101 week 1](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w01-roles-on-a-game-team.md), [PR101 week 4](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md), [PR101 week 6](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md).

1. *Explain.* What was the largest discipline load in your week 1 fit sheet, and which decision brought it to 1 or below? Show where that decision is visible in the final slice.

<details>
<summary>Marking guidance</summary>

A 5 names the discipline, the load before and after (for example art 1.35 to 0.92), the decision as written ("all enemies share one rig") and points to it in the build or asset list. It also says whether the decision held until week 15. A 3 describes the fit test correctly but not the team's numbers. Drop to 2 or below if the student confuses the total load with the worst discipline load, which is the main error the week 1 guide warns about.

</details>

2. *Compute.* Recompute one member's plannable hours using your team's `n`, `H`, `c`, `W` and `b`. How far was that from the hours they actually logged?

<details>
<summary>Marking guidance</summary>

Formula: `p_i = (1 − b) × (H_i − c × (n − 1)) × W`. For the week 1 example (`n = 6`, `H = 8`, `c = 0.25`, `W = 11`, `b = 0.3`) the answer is `0.7 × 6.75 × 11 = 51.975`, about 52 hours. A 5 gets the arithmetic right, compares it with the hours log and explains the gap (illness, deadlines in other courses, coordination costing more than `c`). A 3 has the right formula but no comparison. Anyone who says the buffer `b` was "extra time" rather than hours held back against estimates running long scores at most 2.

</details>

3. *Critique.* Where in your slice does one player need another? Would the slice still work with one player, and what did the network layer cost you to support that moment?

<details>
<summary>Marking guidance</summary>

A 5 describes a concrete interdependence (roles, shared resources or simultaneous actions), says honestly whether a solo player can finish, and estimates the networking share of code hours. If the answer is "you can play with friends", the maximum is 2. The week 1 guide warns that a game that works the same alone pays about 30% of code hours for networking players do not feel.

</details>

4. *Explain.* Name one feature below your cut line. What cut trigger fired, when, and what did the team do in the hours it saved?

<details>
<summary>Marking guidance</summary>

A 5 names the trigger condition and date from the milestone 1 scope sheet, the date it fired and where the hours went, with a board reference. If the team never used its triggers, a strong answer says so and explains the cost. Cuts made silently or late (after beta) are a legitimate answer if the student can say what the trigger should have been.

</details>

5. *Reflect.* Your team's backup for one discipline was never used. Was the bus factor of that discipline really 2? How would you know before it mattered?

<details>
<summary>Marking guidance</summary>

Looks for the difference between a name in a table and a person who has built that discipline's work in this project. A 5 proposes a check, for example the backup completes one small ticket in each sprint, or rebuilds the art export once. A 3 restates the definition of bus factor from PR101 week 1.

</details>

6. *Critique.* A classmate says "our pitch fit because total demand was below total supply." Using your own fit sheet, explain what that check misses.

<details>
<summary>Marking guidance</summary>

The total check is necessary but not sufficient. A 5 shows a discipline in the student's own sheet whose load exceeded or came close to 1 while the total passed, or explains why their team never had that problem. Mentions the theory of constraints idea from the week 1 guide (output is set by the slowest discipline).

</details>

## B. Planning, sprints and process

Links: [PR201 week 6](../lectures/w06-sprint-2-core-combat.md), [PR201 week 8](../lectures/w08-sprint-3-content-and-progression.md), [PR101 week 5](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w05-agile-and-scrum-adapted-for-games.md), [PR101 week 7](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w07-task-tracking-and-definitions-of-done.md), [PR101 week 12](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w12-crunch-causes-costs-alternatives.md).

7. *Compute.* Show how your team forecast sprint 2 from sprint 1. What did it commit, and what did it finish?

<details>
<summary>Marking guidance</summary>

`f = estimated hours done / useful hours`, then `forecast = f × next sprint's useful hours`. In the week 6 example, `43 / 75 × 81 = 46.4`, so commit 46. A 5 uses the team's own numbers, states that half-finished stories counted zero, and compares forecast with outcome. A student who counts partly done stories in velocity scores at most 2.

</details>

8. *Explain.* Your sprint 2 goal needed a chain of dependent stories. How many were in the chain, what did you estimate for each one's chance of finishing, and what did you change to raise it?

<details>
<summary>Marking guidance</summary>

`P(chain) = q^k`. In the week 6 example, five stories at `q = 14 / 18 = 0.78` give 0.28; raising `q` to 0.9 gives 0.59. A 5 uses the team's `k` and `q`, notes that the independence assumption is optimistic, and names a concrete change (splitting a story, pairing, doing the riskiest link first). A 3 recites the formula without the team's chain.

</details>

9. *Critique.* Pick one story your team called done that later reopened. Which line of your definition of done should have caught it?

<details>
<summary>Marking guidance</summary>

A 5 names the ticket, the reopening cause, the missing or ignored line (for example "tested on two machines outside the editor") and whether the team added it afterwards. A student who says nothing ever reopened must show the bug list that proves it, or scores at most 3.

</details>

10. *Compute.* Take your sprint 3 content budget. State the XP, time and hours balances with numbers. Which failed first, and which lever did you pull?

<details>
<summary>Marking guidance</summary>

The three balances from week 8: content XP at least the XP to the target level, content minutes within ± 10% of target, content build hours within capacity. A 5 quotes all three and names the lever (cut, remix, retune) with its cost. The week 8 example's plan B holds on hours (25.0 of 26 estimate-hours, against a forecast of `f × U = 46`) and time (22 min against 20) but is 15 XP short, fixed by a curve retune. A 5 also states the unit: estimate-hours against `f × U`, not estimates times the ratio against all useful hours, which week 8 shows would have let plan A through. A 3 explains the method with the example's numbers instead of the team's.

</details>

11. *Explain.* How did you measure the unit cost of one room or area, and how wrong were your original content estimates?

<details>
<summary>Marking guidance</summary>

A 5 gives the measured hours per discipline for one unit from the sprint 2 log, the content estimate ratio (actual over estimate), and compares it with the team ratio already inside `f`: `k = r_content / r_team` (week 8: `1.33 / 1.28 = 1.04`). A student who multiplied content estimates by the full ratio and also planned against `f × U` has counted the overrun twice and scores at most 3. Mentions that estimates run long more often than short, per PR101 week 6. A 2 says "we guessed" with no ratio.

</details>

12. *Reflect.* Did your team crunch at any point? Use your hours log to say when, how much, and what decision earlier in the project made it likely.

<details>
<summary>Marking guidance</summary>

PR101 week 12 argues crunch is decided early. A 5 finds the spike in the log, traces it to a scope or estimate decision weeks earlier, and names the alternative the team had (cut, move, delay). An answer that treats crunch as dedication scores at most 2.

</details>

13. *Critique.* Read one of your retrospective actions. Was it checkable? Rewrite it with an owner, a change and a check.

<details>
<summary>Marking guidance</summary>

A 5 quotes the real action item, identifies what was missing and rewrites it in the PR101 week 14 form. "Communicate better" rewritten as "each standup names one blocker; owner X; checked at next retro by counting blockers reported more than a day late" is the model.

</details>

14. *Explain.* Who was your product owner, and describe one scope tie they broke. What evidence did they use?

<details>
<summary>Marking guidance</summary>

A 5 names the decision, the options, the evidence (a playtest note, a load, a velocity number) and where it is logged. A 3 describes the role in general. If the team had no working product owner, a strong answer says so and explains the effect on the backlog.

</details>

## C. Networking architecture

Links: [CS202 week 3](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w03-topologies-peer-to-peer-client-server-relay.md), [week 4](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w04-server-authority-never-trust-the-client.md), [week 5](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w05-serialization-and-bit-packing.md), [week 6](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w06-reliability-over-udp.md), [week 7](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w07-snapshots-and-delta-compression.md), [week 8](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w08-client-side-prediction.md), [week 9](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w09-server-reconciliation.md), [week 10](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w10-entity-interpolation.md), [week 11](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w11-lag-compensation-rewind-hit-detection.md), [week 13](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w13-tick-rate-and-bandwidth-budgets.md), [week 14](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w14-testing-under-bad-networks-netem-clumsy.md).

15. *Explain.* Walk through what happens, message by message, when a player attacks an enemy in your slice, from key press to the damage number on a second player's screen.

<details>
<summary>Marking guidance</summary>

A 5 traces input message (with its channel), server validation, the server's damage decision, the replicated result, and what each client shows while waiting. It names which parts are predicted and which are interpolated, using the team's message catalogue. Examiners should ask about the path the student did not code. A 3 describes the general pattern; a 1 cannot say where damage is decided.

</details>

16. *Compute.* Using your tick rate and a measured RTT from a playtest, what is the average and worst input-to-confirmation delay for a server-decided action?

<details>
<summary>Marking guidance</summary>

`delay ≈ RTT + wait for next tick`, average wait `T/2`, worst `T`. At 60 ms RTT and 20 Hz (`T = 50 ms`) the average is 85 ms and the worst 110 ms, before rendering and interpolation delay. A 5 uses a measured RTT, not a guess, and says what the team did about actions where that delay was too long to feel good.

</details>

17. *Explain.* Name one action your client predicts and one it does not. Why is each on its side of the line?

<details>
<summary>Marking guidance</summary>

A 5 links the choice to cost of a wrong guess: movement and attack animation are cheap to correct, damage, death and loot are not. Refers to the team's feedback table from week 6. Loses marks if the student says the client predicts damage values that the server may overturn without explaining the correction.

</details>

18. *Compute.* From your message catalogue, compute the bytes per second the server sends each client at your maximum player count. How much margin did you have?

<details>
<summary>Marking guidance</summary>

Model: 20 snapshots per second, 28 bytes of IP and UDP headers, an 8-byte game header, 10 entities at 24 bytes each gives `20 × (28 + 8 + 240) = 5,520 B/s`, about 44 kbit/s per client and 22 KB/s upstream from the server for four clients. A 5 reproduces the team's own figure, includes packet headers, and states the limit it compared against. A 3 forgets headers or computes for one player.

</details>

19. *Critique.* Which messages did you send reliably and which unreliably? Pick one you would now move to the other channel, and justify it.

<details>
<summary>Marking guidance</summary>

A 5 explains that state which is superseded by the next snapshot (position) should not wait for resends, while one-off events (loot granted, level up) must arrive once. It names a real case from the slice where the choice caused a bug or a stall. Answers claiming "everything is reliable to be safe" should be probed on head-of-line blocking.

</details>

20. *Explain.* What stops a modified client in your slice from dealing ten times its damage? Show the line of code or the design decision.

<details>
<summary>Marking guidance</summary>

Clients send intent (attack target X), and the server computes damage from its own state. A 5 points to the server function and names what it validates (range, cooldown, target alive). If the client sends a damage value that the server accepts, the student should recognise that as a defect and say how to fix it.

</details>

21. *Explain.* How do other players' characters move smoothly on your screen when snapshots arrive 20 times a second? What delay does that add?

<details>
<summary>Marking guidance</summary>

Entity interpolation renders remote entities between two past snapshots, adding about one to two snapshot intervals of delay (50 to 100 ms at 20 Hz). A 5 states the team's buffer and what they saw when a snapshot was lost. A 3 describes interpolation without the team's numbers.

</details>

22. *Critique.* Did your slice need lag compensation for hit detection? Argue from your combat design.

<details>
<summary>Marking guidance</summary>

Lag compensation matters for fast, aimed attacks where the target moves between the shot and the server's check. A targeted RPG attack with a lock-on may not need rewind. A 5 decides for the team's own combat, and names what a player at 120 ms RTT would experience either way. Saying "yes, all games need it" or "no, it is only for shooters" without the reasoning scores 2.

</details>

23. *Explain.* Describe one bug that only appeared under packet loss or latency. How did you reproduce it, and which network profile found it?

<details>
<summary>Marking guidance</summary>

A 5 names the profile (delay, jitter, loss), the reproduction rate, the root cause and the fix, and says whether it was found by a human test or a soak run. CS202 week 14's point is that bursty loss finds bugs that independent loss hides. A student who never tested under a conditioner scores at most 2 and should say what they would test now.

</details>

24. *Critique.* Why did you pick your server tick rate? What would doubling it cost in CPU and bandwidth?

<details>
<summary>Marking guidance</summary>

A 5 quotes the rate, the measured server frame time, and shows that doubling it doubles snapshot bandwidth if the snapshot rate follows, and halves the time budget per tick. It also says what players would gain (average wait falls by `T/4`). A 3 says "higher is smoother" only.

</details>

25. *Explain.* What happens in your slice when a client disconnects in the middle of the encounter and reconnects 30 seconds later?

<details>
<summary>Marking guidance</summary>

A 5 describes the server's behaviour (character kept or removed, timeout), how state is resent on rejoin (full snapshot, then deltas), and what the persistence layer saves. It should mention the telemetry event that records it. If reconnection does not work, a strong answer says so and gives the cost of fixing it.

</details>

26. *Explain.* Did your team use a client-server model with a dedicated server or a player host? What would have changed with the other?

<details>
<summary>Marking guidance</summary>

A 5 names the choice from the milestone 2 TDD, its reason, and at least two consequences (host advantage, host leaving ends the session, NAT traversal, cost of running a server). References CS202 week 3. A 3 describes the topologies without linking them to the slice.

</details>

27. *Compute.* If you added a fifth player and six more enemies to your slice, would your bandwidth budget still hold?

<details>
<summary>Marking guidance</summary>

In the model from question 18, going from 10 to 16 entities raises the per-client rate to `20 × (28 + 8 + 384) = 8,400 B/s`, about 67 kbit/s, and the server sends that to five clients instead of four. A 5 does this with the team's numbers, notes the growth is roughly players × entities, and names the mitigation (delta compression, interest management, lower rate for distant entities). CS202 week 13 is the reference.

</details>

## D. Persistence and telemetry

Links: [DB201 week 1](../../DB201-data-persistence-and-telemetry/lectures/w01-why-persistence-is-hard-in-games.md), [week 2](../../DB201-data-persistence-and-telemetry/lectures/w02-relational-modeling-characters-inventories-items.md), [week 5](../../DB201-data-persistence-and-telemetry/lectures/w05-transactions-and-acid.md), [week 6](../../DB201-data-persistence-and-telemetry/lectures/w06-race-conditions-and-the-duplication-bug.md), [week 10](../../DB201-data-persistence-and-telemetry/lectures/w10-telemetry-design-events-and-properties.md), [week 11](../../DB201-data-persistence-and-telemetry/lectures/w11-pipelines-collect-store-query.md), [week 12](../../DB201-data-persistence-and-telemetry/lectures/w12-dashboards-and-kpis.md), [week 13](../../DB201-data-persistence-and-telemetry/lectures/w13-privacy-gdpr-and-data-retention.md), [week 14](../../DB201-data-persistence-and-telemetry/lectures/w14-backups-and-disaster-recovery.md).

28. *Explain.* Show your schema for characters, inventory and progression. Why is each table shaped the way it is?

<details>
<summary>Marking guidance</summary>

A 5 walks through keys and relations, explains one normalisation choice and one place the team denormalised on purpose. A 2 cannot say where an item's owner is stored.

</details>

29. *Explain.* What happens in your database when a character levels up? Which steps are inside one transaction, and what breaks if the server crashes halfway?

<details>
<summary>Marking guidance</summary>

A 5 lists the writes (XP, level, stat changes, reward grant), shows they commit together, and describes the half-applied state that the transaction prevents. References DB201 week 5 and the week 8 acceptance criteria "level-up as one transaction".

</details>

30. *Critique.* Could a player in your slice receive the same boss reward twice? Explain how your design prevents it, or how it could happen.

<details>
<summary>Marking guidance</summary>

The expected mechanism is an idempotent grant: a unique grant id, so a retried message or a double click inserts nothing the second time. A 5 shows the constraint or check and names the race (two requests in flight, a retry after a timeout) from DB201 week 6. A student who says "the button is disabled after one click" scores 2, since the server must not trust that.

</details>

31. *Explain.* Name three telemetry events your server logs and the question each one answered at the alpha playtest.

<details>
<summary>Marking guidance</summary>

A 5 gives event names, key properties, the question and the threshold, and explains why they are server-side rather than client-side (DB201 week 10). A 3 lists events without questions.

</details>

32. *Compute.* Your count checks at week 11 compared two numbers that should match. Give one pair from your data. Did they match, and if not, why?

<details>
<summary>Marking guidance</summary>

For example sessions started against sessions ended plus disconnects, or deaths against revives plus wipes. A 5 quotes both counts, explains any mismatch (lost events, test sessions, clock issues) and says what the team changed. The week 11 guide's point is to trust the counts before the chart.

</details>

33. *Critique.* What personal data does your telemetry store, how long do you keep it, and could you delete one player's data on request?

<details>
<summary>Marking guidance</summary>

A 5 lists the identifiers stored (player id, IP address if logged), the retention period, and the deletion route, with reference to DB201 week 13. It notices if playtest consent forms did not cover telemetry. "We don't store personal data" is only acceptable if the student has checked the schema for IP addresses and free-text fields.

</details>

34. *Explain.* Describe your backup and restore test from the release candidate. What was the recovery point, and how long did the restore take?

<details>
<summary>Marking guidance</summary>

A 5 gives the backup method, the row counts before and after, the time taken, and how much play would be lost if the server failed just before the next backup. A backup that was never restored scores at most 2, because an untested backup is the DB201 week 14 warning.

</details>

## E. Playtests and evidence

Links: [PR201 week 7](../lectures/w07-sprint-2-review-and-playtest.md), [PR201 week 11](../lectures/w11-playtest-and-telemetry-review.md), [lab 11](../labs/lab11.md), [UX201 week 8](../../UX201-game-ux-and-player-psychology/lectures/w08-usability-testing-methods.md), [UX201 week 12](../../UX201-game-ux-and-player-psychology/lectures/w12-surveys-and-interviews.md), [UX201 week 14](../../UX201-game-ux-and-player-psychology/lectures/w14-ux-research-reporting.md).

35. *Compute.* How many matches did your week 7 playtest hold, and what was the smallest problem frequency you could expect to have seen with 90% confidence?

<details>
<summary>Marking guidance</summary>

`P(seen) = 1 − (1 − p)^n` and `n = ceil(ln(1 − c) / ln(1 − p))`. With 12 matches, a per-match problem at `p = 0.10` is seen with probability 0.72, and 90% confidence needs 22 matches; at `p = 0.05` it needs 45. A 5 uses the team's own `n`, separates per-match and first-time problems, and states the reach sentence. A 3 has the formula but the examiner's numbers.

</details>

36. *Compute.* Pick one rate from your alpha evidence table. What was `k/n`, what was its unit, and what did the Wilson interval say about acting on it?

<details>
<summary>Marking guidance</summary>

A 5 gives `k`, `n`, the unit (player, party or session), the interval and the pre-set threshold, and says act, leave or can't decide. For example 4 of 12 players gives about [13.8%, 60.9%]. Party-level outcomes must use parties as `n`: 3 of 4 parties gives [30.1%, 95.4%], which rarely decides anything. Students who use players as `n` for a party outcome score at most 2.

</details>

37. *Critique.* Name one change made after the alpha that was not supported by evidence. Was it the right call?

<details>
<summary>Marking guidance</summary>

The beta brief allows judgment calls if they are labelled. A 5 names one, explains why the team made it anyway, and says what evidence would have confirmed or refuted it. A student who claims every change was evidence-based should be asked to trace one; if they can't, cap at 2.

</details>

38. *Explain.* What did your observation notes show that telemetry could not, and the other way round?

<details>
<summary>Marking guidance</summary>

A 5 gives one concrete example each way: observation explains why (a player never found the revive prompt), telemetry says how often and in which sessions. Uses the UX201 week 14 finding format for the example.

</details>

39. *Explain.* A problem showed up in three disconnects out of fifteen players. Why might that be one problem, not three, and how did you check in your own data?

<details>
<summary>Marking guidance</summary>

Clustering. If all three came from one session (one bad host or network), the session-level rate is 1 of 5, whose interval, [3.6%, 62.4%], can't decide. A 5 shows the team's clustering row from lab 11 and what it changed about their decision.

</details>

## F. Builds, release and pipelines

Links: [PR101 week 3](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w03-asset-workflows-and-large-files-lfs.md), [PR101 week 10](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md), [PR101 week 13](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w13-builds-and-release-checklists.md), [UX201 week 11](../../UX201-game-ux-and-player-psychology/lectures/w11-accessibility-guidelines.md).

40. *Explain.* Follow one art asset and one audio asset from source file to the release build. Who touched them, and what checks ran?

<details>
<summary>Marking guidance</summary>

This tests the outcome "integrate design, code, art and audio pipelines". A 5 describes file formats, storage (LFS, lockable files), import settings, naming, the build step and a check (a missing-asset test, a size budget). Programmers should be able to answer for art and artists for code, at least at the level of "where does it enter the build".

</details>

41. *Explain.* Could a teammate who is not the build owner produce your release candidate from the tag today? Show how.

<details>
<summary>Marking guidance</summary>

A 5 names the build script, its inputs, the version stamping and where the artifact goes, and refers to the RC milestone's rebuild test. A student who says "only X knows how" is describing a bus factor of 1 and should say what they would change.

</details>

42. *Critique.* Name one bug you shipped as a known issue. Why was it waived, and was that the right severity?

<details>
<summary>Marking guidance</summary>

A 5 gives the bug, severity and priority per PR101 week 10, the product owner's reasoning and whether it appeared at the showcase. Recognises the difference between severity (how bad) and priority (how soon).

</details>

43. *Explain.* Which accessibility item from your beta checklist did you implement, which did you decide against, and why?

<details>
<summary>Marking guidance</summary>

A 5 names two items from UX201 week 11 (for example remappable controls, subtitles for audio cues, colour-independent status), what it cost, and who it helps. "Not applicable" needs a reason.

</details>

## G. Team and reflection

Links: [PR101 week 11](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w11-communication-and-conflict-in-teams.md), [PR101 week 14](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w14-post-mortems-as-a-practice.md), [peer assessment brief](peer-assessment-brief.md).

44. *Reflect.* Describe a disagreement on your team. Was it a task, process or relationship conflict, and what settled it?

<details>
<summary>Marking guidance</summary>

A 5 classifies the conflict per PR101 week 11, describes behaviour not character, and names the rule or decision that settled it (charter, product owner, evidence). An answer that blames a named teammate scores at most 2; the viva is not the place to settle it, and the post-mortem brief requires blameless writing.

</details>

45. *Compute.* Using PR101 week 11's model, explain why individual credit mattered more in your team of `n` than it would in a pair. What was the peer adjustment `F` for a score of 0.7, and for 1.3?

<details>
<summary>Marking guidance</summary>

`k* = 1 − m/n`, so the credit needed grows with `n`; at `m = 2` it is 0 for a pair and 0.6 for a team of five. With `w = 0.5`, `F = 1 + 0.5 × (s − 1)`, so 0.7 gives 0.85 and 1.3 gives 1.15, clamped to 1.10. A 5 does both and explains why the scheme normalises each rater's points. The student is not asked about their own ratings.

</details>

46. *Reflect.* What is the one action item from your post-mortem that the next PR301 team should adopt, and how would they check it worked?

<details>
<summary>Marking guidance</summary>

A 5 gives an owner, a change and a check that a different team can run, and ties it to a coded "what went wrong" category and its recurrence from the PR101 jam. Generic advice ("start early") scores 2.

</details>

47. *Reflect.* Compare your planned and logged hours over the semester. Which week had the biggest gap, and what did you learn about your own estimates?

<details>
<summary>Marking guidance</summary>

A 5 quotes the hours log, identifies the week and cause, and computes a personal estimate ratio. It says how the ratio will change the student's next plan. Answers without numbers score at most 3.

</details>

48. *Reflect.* If your team restarted at week 4 with what you know now, what single decision would you change, and what would it have cost?

<details>
<summary>Marking guidance</summary>

A 5 picks one decision (scope, topology, a tool, a process rule), traces its effects through the milestones with evidence, and names the price of the alternative. Lists of several changes without a priority score at most 3.

</details>

# PR301 · Week 04 — Sprint 1 Review

**Why this matters:** "Fifty bots logged in fine" is the sentence most sprint 1 reviews hear, and it proves much less than it sounds. A login path that fails one time in twenty will pass that test more often than not, then fail a dozen times during the alpha weekend. This week you learn how many clean attempts it takes to back a claim, and you replace the focus factor you borrowed from PR201 with your own.

**You will be able to:**
- Rehearse the sprint review at the sprint's midpoint, then run it at the start of week 5, answering the goal with yes or no from the definition of done, the test host and a restart.
- Compute the 95% upper bound on a failure rate from a soak test with zero failures (the rule of three) and with some failures (the Wilson interval).
- Choose a failure-rate threshold from the exposure of the next playtest, and size a soak test that can prove it.
- Measure sprint 1's focus factor and forecast sprint 2 from it.

**Before class:** Reread [PR201 week 7](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w07-sprint-2-review-and-playtest.md) section 4 (the discovery formula for playtests) and [PR201 week 11](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w11-playtest-and-telemetry-review.md) (Wilson intervals at the right unit). Skim [MMO302 week 11](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md) section 4 (bots that behave like players). Bring the midpoint build deployed on the test host, the soak script, its first logs, and the sprint board.

**Prerequisites from earlier courses:** [PR101 week 5](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w05-agile-and-scrum-adapted-for-games.md) for the review and retrospective. [PR101 week 10](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md) for writing and triaging a bug. [PR201 week 6](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w06-sprint-2-core-combat.md) for yesterday's weather. [MMO302 week 9](../../MMO302-mmo-server-architecture/lectures/w09-login-character-select-gateway-services.md) for the login pipeline and reconnect storms. [DB201 week 6](../../DB201-data-persistence-and-telemetry/lectures/w06-race-conditions-and-the-duplication-bug.md) for races that only appear under concurrency.

---

## 1. The review inspects the goal, on the host, under load

Sprint 1 runs from the week 3 session to the week 5 session, and its review takes the first part of week 5. This week's session sits at the midpoint. It is a stand-up, a soak test and a restart on the test host, and a burn-down check, run exactly as the review will run them. Whatever fails today still has a week to be fixed. Whatever fails at the review counts.

The sprint 1 review follows the PR201 pattern with three changes.

**The demo runs on the test host.** Not on the laptop of the person who wrote the server. The build is the tagged one, deployed by the build script. If the build script does not work, the demo does not happen and the goal is answered "no". That sounds harsh. It is also the cheapest time this semester to find out that deploying the world takes one person and a secret.

**The demo includes a restart.** The reviewer picks a moment, and a team member kills the server process. After the restart the bots log back in, and the team checks their positions against the persistence map from week 2. Position may lose up to a minute. Anything marked "None" must match exactly.

**The goal is answered by the definition of done.** Week 3 wrote three server lines into it: runs on the test host, survives a restart, has a bot check. A story whose bot check fails its threshold is not done, however well it demos. Section 2 is about what that threshold should be.

Then count what met the definition of done, record the sprint's focus factor (section 3), and hold the retrospective. The retrospective's first question for sprint 1 is always the same. When did the first real message pass between two programmers' code? If the answer is "day eight", that is the topic.

## 2. Worked example: what does a clean soak test prove?

### The hook

Blizzard released Diablo III on 15 May 2012. The game required an online connection even for solo play, and at launch the servers could not keep up. Many players could not get in. They met "Error 37", with a message telling them the servers were busy and to try again later. Connection problems continued through the rest of May, easing as Blizzard added capacity and demand settled.

Large launches are tested before release. The trouble is that a test says less than it seems to. A test that passes tells you the failure rate is probably below some number. Which number depends on how many attempts you made, and teams almost never compute it.

### The model

Suppose each login attempt fails independently with an unknown probability `p`. You run `n` attempts and see `x` failures. You want an upper bound, a value that `p` is below with 95% confidence.

**Zero failures.** If `p` were large, seeing `n` clean attempts in a row would be unlikely. The largest `p` that still gives a clean run with probability at least 5% solves `(1 − p)^n = 0.05`. For small `p`, `(1 − p)^n ≈ e^(−pn)`, so

```
upper bound ≈ −ln(0.05) / n = 2.996 / n ≈ 3 / n
```

This is the **rule of three**, from medical statistics. If no adverse event appears in `n` patients, the rate is below `3 / n` with 95% confidence.

**Some failures.** When `x > 0`, use the **Wilson interval** from PR201 week 11. With `p̂ = x / n` and `z = 1.96`:

```
upper = ( p̂ + z²/(2n) + z × √( p̂(1 − p̂)/n + z²/(4n²) ) ) / (1 + z²/n)
```

**The threshold.** Pick it from the next event, not from a feeling. If the alpha weekend has `E` login attempts and you can tolerate `k` failures on average, the threshold is `p* = k / E`. The attempts needed for a clean soak to prove it are

```
n_needed = ⌈ 2.996 / p* ⌉
```

### Numbers you can check

The *Saltmarsh* team's alpha weekend expects 50 players, each logging in about four times: `E = 200`. They can live with two failed logins over the weekend if a retry works, so `p* = 2 / 200 = 1%`. A clean soak needs `2.996 / 0.01 = 299.6`, so 300 attempts.

What different clean runs prove:

| Clean attempts `n` | 95% upper bound on `p` | Expected failures in 200 alpha logins at that bound |
|---|---|---|
| 50 | 5.99% | 12.0 |
| 100 | 3.00% | 6.0 |
| 300 | 1.00% | 2.0 |
| 400 | 0.75% | 1.5 |
| 1,000 | 0.30% | 0.6 |

Check the first row: `2.996 / 50 = 0.0599`. The sprint 1 demo, "50 bots logged in fine", cannot rule out a login that fails 6% of the time. At 6%, the weekend's 200 logins would fail about 12 times, and the chance of at least one failure would be `1 − 0.94^200`, which is above 0.9999.

The team ran three conditions in the week 4 mid-sprint session, on the midpoint build:

| Condition | Attempts | Failures | Upper bound | Verdict |
|---|---|---|---|---|
| One-shot: 50 bots log in once | 50 | 0 | 5.99% | Not done |
| Cycled: 50 bots log in and out 8 times | 400 | 2 | 1.80% | Not done |
| Burst: all 50 at once, 4 times | 200 | 0 | 1.50% | Not done |

Check the cycled row. `p̂ = 2/400 = 0.005` and `z² = 3.8416`. The denominator is `1 + 3.8416/400 = 1.0096`. The centre is `(0.005 + 0.0048) / 1.0096 = 0.00971`. The half-width is `1.96 × √(0.0000124 + 0.0000060) / 1.0096 = 0.00834`. The upper bound is `0.00971 + 0.00834 = 0.0180`, or 1.80%.

The login story is not done. The two failures in the cycled run gave the team a lead. Both happened when a bot logged back in within a second of logging out. The old session row had not been deleted yet, and the login service refused a second session for the same account. That is a race, the kind [DB201 week 6](../../DB201-data-persistence-and-telemetry/lectures/w06-race-conditions-and-the-duplication-bug.md) taught you to look for, and a one-shot test can never trigger it.

The fix (the login replaces an old session inside one transaction instead of refusing) was harder than it looked and missed the tagged review build, so at the sprint 1 review the login story was still not done. The team merged the fix on the first day of sprint 2 and reran both conditions. Cycled: 400 attempts, 0 failures, bound 0.75%. Burst: 300 attempts, 0 failures, bound `2.996 / 300 = 0.999%`. Both are at or below 1%. The story is done, and it counts as sprint 2's first finished story, not in sprint 1's velocity.

Run `check_soak.py` from [lab 04](../labs/lab04.md) on the starter file to reproduce the three verdicts. Replace the rows with the rerun and it prints `PASS`.

### The same idea elsewhere

**Playtest discovery, PR201 week 7.** There you asked how many matches it takes to see a problem of frequency `p` at least once: `1 − (1 − p)^n`. Set that to 95% and solve: `n = ln(0.05) / ln(1 − p) ≈ 3 / p`. It is the same equation read the other way. PR201 asked "will we see it?". The rule of three asks "we didn't see it, so how rare must it be?"

**Medical trials.** The rule of three comes from clinicians asking what a trial with no adverse events proves. Hanley and Lippman-Hand's 1983 paper had the title "If nothing goes wrong, is everything all right?" The answer is the same for patients and for logins: only up to `3 / n`.

**WoW Classic's stress tests.** Blizzard ran three public stress tests in 2019 with the level cap at five, which packed players into the starting zones. Each test exposed the servers to far more logins and crowding than internal testing could. In the model's terms, public tests are the cheapest way to make `n` large.

### Eyes-open judgment

The model assumes attempts are independent. They are not. A bug that depends on timing, like the session race, fails in bursts under some conditions and never under others. That is why the conditions stay separate. Never add the one-shot, cycled and burst runs into one big `n`. Each condition tests different causes, and a large clean total from the easy condition hides a failing hard one.

Bots are also not players. Real players reconnect on bad networks, close the client mid-login and click "log in" twice. [MMO302 week 9](../../MMO302-mmo-server-architecture/lectures/w09-login-character-select-gateway-services.md) described the reconnect storm after a server restart, when every client retries at once. The burst condition is a crude version of it. Add a "restart, then all 50 reconnect" condition before the alpha.

Finally, the threshold is a product decision. One percent was right for a class alpha where a retry costs a few seconds. For the item-trade path, where a failure could mean a lost item, the threshold is much lower and the soak much longer. Set it per path, write it in the definition of done, and don't let the soak script's author choose it after seeing the result.

### Check yourself

1. The beta in week 13 expects 120 players logging in five times each, and the team still tolerates two failures. What threshold and what clean soak size does that give?
2. A team reports "1,000 logins, 0 failures" from 20 bots cycling 50 times, all in one sequential loop. What does the rule of three say, and what would you ask before accepting it?
3. A soak run gives 1 failure in 600 attempts. Is the 1% threshold met? Use the Wilson formula.

<details><summary>Answers</summary>

1. `E = 600`, so `p* = 2 / 600 = 0.33%`. The soak needs `⌈2.996 / 0.00333⌉ = 899` clean attempts per condition.
2. The rule says the rate is below 0.3%. But a sequential loop never runs two logins at once, so it cannot trigger a concurrency bug. Ask for a burst condition and a cycled condition with overlap, each counted separately.
3. `p̂ = 0.00167`, `z²/n = 0.0064`. Denominator `1.0064`. Centre `(0.00167 + 0.0032) / 1.0064 = 0.00484`. Half-width `1.96 × √(0.00000277 + 0.00000267) / 1.0064 = 0.00454`. Upper bound about 0.94%. Yes, the threshold is met, with little to spare.

</details>

## 3. Your own focus factor

Week 3 borrowed `f = 0.62` from PR201. At the sprint 1 review, at the start of week 5, measure sprint 1's own. Today, check the burn-down against it so the number is no surprise.

```
f = estimated hours of stories that met the definition of done / hours actually available
```

For *Saltmarsh*: the plan charged 50.5 hours. S12 (the character model) was dropped by the drop order on day seven. S3 (login) did not meet its threshold. Done stories charged `50.5 − 8 − 3 = 39.5` hours. Chen lost 5 hours to illness, so available hours were `7 × 13 − 5 = 86`.

```
f = 39.5 / 86 = 0.46
```

That is well below PR201's 0.62, and typical for a first server sprint. Most of the gap was integration. Now forecast sprint 2 with PR201 week 6's yesterday's weather. Two people have midterms and lose 4 hours each, so sprint 2 has `91 − 8 = 83` available hours:

```
sprint 2 capacity = 0.46 × 83 = 38.2 hours
```

Per person, with 13 available hours, capacity is `0.46 × 13 = 6.0` hours. The sprint 2 plan, made in the rest of the week 5 session, uses 6.0, not 8.06. The login fix is nearly done and gets no extra room in sprint 2's forecast, but the stories stubbed in sprint 1 (real authentication, the client login screen, chat) are waiting in the backlog and will compete with combat for those 38 hours.

Keep a small table of `f` per sprint in the repository. After three sprints you have a range, and PR201 week 9 showed how to forecast from one.

## 4. Turning the review into the sprint 2 backlog

The review produces three kinds of backlog item. Tag each one as you write it.

- **Defects** from the soak or the restart check. Each has a failing bot condition that reproduces it. Its fix is done when that condition passes the threshold.
- **Stubs coming due.** Dev-token login, a missing client screen. They were planned; confirm the sprint.
- **Discoveries.** Things the demo showed that nobody planned, like a restart that takes three minutes because the server loads every character at startup. Estimate them now, and let the product owner rank them against sprint 2's combat and mob stories.

Draft the list today from the midpoint soak and restart, and finish it at the review. Sprint 2's goal is combat and mobs. A team that enters sprint 2 with a failing login path will spend its combat sprint on login. Fix defects on the goal's path first.

## Studio session plan

This is a mid-sprint session: sprint 1 is one week in, and its review opens the week 5 session. The studio meets for 3 hours. Teams are paired, and each team runs the other's restart.

| Time | Activity | Output |
|---|---|---|
| 0:00 to 0:15 | Stand-up by goal-chain story; briefing on the rule of three, thresholds from exposure and separate conditions | Chain status on the board |
| 0:15 to 0:55 | Midpoint check, team A: midpoint build on the test host; team B kills the server; bots reconnect; soak conditions run and read from the log | Soak table, restart result |
| 0:55 to 1:35 | Midpoint check, team B, the other way round | Same |
| 1:35 to 1:45 | Break | |
| 1:45 to 2:15 | Each team runs `check_soak.py`, files a defect for every failure, and checks the goal-chain burn-down against the drop order | Checker output; defects; burn-down decision |
| 2:15 to 2:45 | Playtest: the paired team plays the midpoint build by hand and logs issues | Issue log |
| 2:45 to 3:00 | Draft the sprint 2 input list: defects, stubs coming due, discoveries | Draft input list |

At the sprint 1 review (first part of the week 5 session): goal read aloud and answered yes or no on the tagged build, another team's restart, the final soak, `f` computed, the sprint 2 forecast and the retrospective (when did the first real message pass?).

## Deliverables

In `production/sprint1/` in the team repository.

At the end of this session:

- **Midpoint soak results** (`soak.csv`) with at least the cycled and burst conditions, the saved `check_soak.py` output, and the threshold with its exposure calculation.
- **Defects** for every soak or restart failure, each linked to the bot condition that reproduces it.

At the sprint 1 review, start of week 5:

- **Review record**: goal answered yes or no, stories done and not done, and the restart result against the persistence map.
- **Final soak results** on the tagged build, with the checker output.
- **Focus factor**: `f` for sprint 1 with its inputs, and the sprint 2 forecast.
- **Retrospective note** with one action, an owner and a check date.
- **Tagged sprint 2 input list**.

The instructor reruns `check_soak.py` on your file. See [lab 04](../labs/lab04.md).

## Common failure modes

- **One-shot proof.** Fifty bots log in once and the story is closed. Fix: set the threshold from exposure and run the soak it needs.
- **Pooling conditions.** The team adds cycled, burst and one-shot into one clean total. Fix: one row per condition, each at the threshold.
- **Threshold after the fact.** The failure rate comes back at 1.8% and the threshold becomes 2%. Fix: the threshold is in the definition of done before the soak runs.
- **Laptop demo.** The build works on the author's machine and the review watches that. Fix: test host or no demo.
- **Velocity inflation.** The login fix, merged after the review build was tagged, counts toward sprint 1. Fix: a story counts in the sprint in which it met the definition of done.

## Review checklist

The instructor checks the midpoint soak in this session and signs off the sprint 1 milestone at the review, at the start of week 5, when:

- [ ] The goal was answered yes or no on the test host, with a restart performed by another team.
- [ ] Persistent state after the restart matched the persistence map.
- [ ] `check_soak.py` output is saved, with separate cycled and burst conditions.
- [ ] The login threshold was set from the alpha's exposure before the soak ran.
- [ ] Sprint 1 `f` is computed from done stories and actual available hours, and the sprint 2 forecast uses it.
- [ ] Every defect in the sprint 2 input list has a reproducing bot condition.

## Sources

- Wikipedia, "Diablo III" (read September 2026). Released 15 May 2012; always-online requirement; severe server overload at launch; "Error 37" telling players the servers were busy; problems eased as capacity was added and demand settled.
- Hanley, J. A., & Lippman-Hand, A. (1983). "If nothing goes wrong, is everything all right?" *JAMA*, 249(13), 1743-1745.
- Eypasch, E., et al. (1995). "Probability of adverse events that have not yet occurred: a statistical reminder." *BMJ*, 311(7005), 619-620.
- Wikipedia, "Rule of three (statistics)" (read September 2026). The bound `3 / n` at 95% confidence and the general form `−ln(α) / n`.
- Wilson, E. B. (1927). "Probable inference, the law of succession, and statistical inference." *Journal of the American Statistical Association*, 22(158), 209-212.
- Warcraft Wiki, "Stress test" (read September 2026). WoW Classic stress tests in May, June and July 2019 with a level cap of five.
- The *Saltmarsh* team, its soak results, the session race and all hour figures are invented for teaching. The 1% threshold is an example of a product decision, not a standard.

# PR201 · Week 11 — Playtest and Telemetry Review

**Why this matters:** Your alpha build has now been played by people who are not on your team, and you have two kinds of evidence from it. You have notes from watching them, and you have event logs from your server. Next week's polish sprint has room for only a handful of changes, so this week decides which ones. Teams that skip the review spend sprint 4 polishing what the loudest teammate noticed. Teams that do it spend it on what players actually hit.

**You will be able to:**
- Sort alpha evidence by its unit of analysis (player, party, session) and state the sample size each claim really rests on.
- Compute a Wilson 95% interval for each telemetry rate and decide whether the data supports acting, not acting, or neither.
- Reconcile your event counts against each other and against the server log before trusting any chart.
- Turn the review into a ranked sprint 4 input list in which every item names its evidence.

**Before class:** Re-read your own alpha playtest notes and export your telemetry tables (session, player, party and death events at minimum). Read MA102 week 13, section 3 on the Wilson interval (15 minutes), and DB201 week 10, section 5 on client versus server events (10 minutes). Skim UX201 week 14, section 3 on writing one finding (10 minutes). Bring the alpha milestone feedback sheet from week 10.

**Prerequisites from earlier courses:** [UX201 week 8, usability testing methods](../../UX201-game-ux-and-player-psychology/lectures/w08-usability-testing-methods.md) (how the observation notes were collected). [UX201 week 14, UX research reporting](../../UX201-game-ux-and-player-psychology/lectures/w14-ux-research-reporting.md) (the finding format used in the lab). [DB201 week 10, telemetry design](../../DB201-data-persistence-and-telemetry/lectures/w10-telemetry-design-events-and-properties.md) and [DB201 week 12, dashboards and KPIs](../../DB201-data-persistence-and-telemetry/lectures/w12-dashboards-and-kpis.md) (your events and how to count them). [MA102 week 13, sampling and why n = 5 lies](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (the Wilson interval, which this guide uses without re-deriving). [PR101 week 10, bug tracking and QA basics](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md) (severity, priority and triage). From this course, the alpha milestone in week 10 (see the [syllabus](../syllabus.md)).

---

## 1. What you have after the alpha

By now every team has run at least one external playtest of the alpha build. The evidence from it comes in five piles, and each pile answers a different question.

- **Observation notes.** What testers did and said while you watched in silence (UX201 week 8). These answer "does this problem exist, and why does it happen?"
- **Survey answers.** What testers said afterwards (UX201 week 12). These answer "how did it feel?", with all the bias of a question asked after the fact.
- **Telemetry events.** What your code recorded: session start and end, party formed, ability used, death, disconnect. These answer "how often?", if you have enough of them.
- **Server logs.** Errors, warnings, tick overruns and disconnect reasons. These answer "what broke under the hood?"
- **The bug tracker.** Everything your team and your testers filed.

The review's job is to put the piles side by side. A good finding usually has two kinds of evidence. Observation says a problem exists and suggests why. Telemetry says how many people it touched. Neither alone is enough for a decision you will spend a sprint on.

## 2. The unit of analysis in a multiplayer test

Single-player playtests have one natural unit, the player. Your game has at least three.

- **Player.** One person's experience. "Did this player finish the tutorial?"
- **Party.** The group that played together. "Did this party beat the boss?"
- **Session.** One run of the server from start to shutdown, often one party, sometimes several. "Did this server session have a disconnect?"

Why it matters is simple and costly to forget. Fifteen testers in five parties of three give you fifteen observations of anything personal, but only five observations of anything the party does together. Boss difficulty, party wipes, loot disputes and pacing are all party-level outcomes. So is anything caused by the host's network or the server build that session ran. When you write "80% of players wiped at the boss", check the unit. If all three players in a party wipe together, you have one observation, not three.

A second trap follows from the first. Players in the same party are not independent of each other. If one tester's home connection drops packets, everyone who shares a session with them sees rubber-banding. If one party has an experienced player who explains revive, all three "discover" it. When events cluster inside sessions, the effective sample size sits somewhere between the number of sessions and the number of players. You can't compute it exactly with this little data. You can check for it, as the worked example does.

## 3. Worked example: fifteen players, five parties

### The hook

In August 2007 Wired described the user research lab that Microsoft ran for Bungie's Halo 3. By the time of the article, Randy Pagulayan's team had analysed more than 3,000 hours of play from about 600 players, tracking where and how players died down to small patches of floor. The article also shows the other half of the method. Watching one tester through a one-way mirror, Pagulayan saw her charge into a fight again and again and ignore the grenades on the floor, because the grenades were not visible enough. Telemetry told Bungie where people died. Watching told them why.

The Hollowmarch team ran its alpha playtest with 15 players in five parties of three, for about 45 minutes each. That is about 11 player-hours, under 0.4% of Halo 3's 3,000. You have the same two tools and far less data. This example shows what that amount of data can and cannot decide.

### The model

For a rate measured as `k` events out of `n` units, use the Wilson 95% interval from MA102 week 13, section 3:

```
p̂        = k / n
center    = (p̂ + z²/(2n)) / (1 + z²/n)
halfwidth = z × sqrt(p̂(1 − p̂)/n + z²/(4n²)) / (1 + z²/n)
interval  = center ± halfwidth,    z = 1.96
```

Then compare the interval with a **threshold**, the value at which your team would change something. Write the threshold down before you look at the data. Three outcomes are possible.

- The whole interval is on the "act" side of the threshold. The data supports acting.
- The whole interval is on the "leave it" side. The data supports leaving it alone.
- The interval straddles the threshold. The data can't decide. Use another kind of evidence, or collect more.

### Numbers you can check

Here is Hollowmarch's alpha. Five sessions, one party of three per session, 15 players in all. Thresholds were set in the week 10 alpha plan.

| Question | Unit | `k / n` | `p̂` | Wilson 95% | Threshold | Verdict |
|---|---|---|---|---|---|---|
| Tutorial completed | player | 12 / 15 | 80.0% | 54.8% to 93.0% | act if below 70% | Can't decide |
| Disconnected at least once | player | 3 / 15 | 20.0% | 7.0% to 45.2% | act if above 5% | Act |
| Party wiped at the boss at least once | party | 4 / 5 | 80.0% | 37.6% to 96.4% | tune if above 70% | Can't decide |
| Never used the revive ability when a teammate went down | player | 6 / 15 | 40.0% | 19.8% to 64.3% | act if above 10% | Act |

Check the disconnect row by hand. `p̂ = 0.2`, `z² = 3.8416`. The center is `(0.2 + 3.8416/30) / (1 + 3.8416/15) = 0.3281 / 1.2561 = 0.2612`. The halfwidth is `1.96 × sqrt(0.2 × 0.8/15 + 3.8416/900) / 1.2561 = 1.96 × sqrt(0.010667 + 0.004268) / 1.2561 = 1.96 × 0.12221 / 1.2561 = 0.1907`. So `0.2612 ± 0.1907`, which is 7.0% to 45.2%.

Read the verdicts.

**Tutorial.** 80% looks healthy, but the data is consistent with a true rate as low as 55%, which is below the 70% threshold. Telemetry alone can't clear the tutorial. Look at the three players who didn't finish in the observation notes. If they all stopped at the same step for the same reason, that is a real problem regardless of the rate.

**Disconnects.** Even the low end, 7.0%, is above the 5% threshold. Act. But check the clustering first. The server log shows all three disconnects happened in session 2. At the session level, that is 1 of 5 sessions, with a Wilson interval of 3.6% to 62.4%. The evidence now points at one session's conditions (a tester on hotel wifi, say, or one server build) rather than a problem every player meets. You still act, but the action changes. Instead of rewriting the reconnect flow, reproduce session 2's conditions with a network conditioner (CS202 week 14) and find out which of your timeouts fired.

**Boss wipes.** Four wipes out of five parties could come from a boss that 38% of parties wipe on or one that 96% do. You can't tune difficulty from this. How many parties would you need? Turn the margin formula around (MA102 week 13, section 4) for a ±15-point margin at the worst case `p = 0.5`: `n = 1.96² × 0.25 / 0.15² ≈ 43` parties, which is 129 players. For ±10 points, 96 parties, or 288 players. No student team gets that before beta. So boss tuning in this course runs on observation (did parties understand the mechanic, did they die to it or to confusion?) and on your combat model from GD203, not on a wipe rate.

**Revive.** 40% of players never used revive when they could have. Even the low end of the interval, 19.8%, is above the threshold. And observation explains it. Four of the six said they didn't know they could revive a downed teammate. This is the Halo 3 grenade problem in your game. Act, and the fix is almost certainly visibility, not balance.

This script reproduces the table and the clustering check. Run it with `.venv/bin/python`.

```python
from math import sqrt

def wilson(k, n, z=1.96):
    p = k / n
    center = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return max(0.0, center - half), min(1.0, center + half)

def verdict(lo, hi, act_below=None, act_above=None):
    if act_above is not None:
        return "act" if lo > act_above else "leave" if hi <= act_above else "can't decide"
    return "act" if hi < act_below else "leave" if lo >= act_below else "can't decide"

rows = [("tutorial completed", 12, 15, dict(act_below=0.70)),
        ("disconnected", 3, 15, dict(act_above=0.05)),
        ("sessions with a disconnect", 1, 5, dict(act_above=0.05)),
        ("parties wiped at the boss", 4, 5, dict(act_above=0.70)),
        ("never revived", 6, 15, dict(act_above=0.10))]
for name, k, n, rule in rows:
    lo, hi = wilson(k, n)
    print(f"{name:27} {k:2}/{n:<2} [{lo:5.1%}, {hi:5.1%}]  {verdict(lo, hi, **rule)}")
for m in (0.15, 0.10):
    print(f"parties for +/-{m:.0%}: {round(1.96 ** 2 * 0.25 / m ** 2)}")
```

It prints:

```
tutorial completed          12/15 [54.8%, 93.0%]  can't decide
disconnected                 3/15 [ 7.0%, 45.2%]  act
sessions with a disconnect   1/5  [ 3.6%, 62.4%]  can't decide
parties wiped at the boss    4/5  [37.6%, 96.4%]  can't decide
never revived                6/15 [19.8%, 64.3%]  act
parties for +/-15%: 43
parties for +/-10%: 96
```

Notice the third line. At the session level, the disconnect data can't decide either. That is the numerical version of "check the clustering before you rewrite the netcode".

### Cross-game recognition

**Halo 3 (2007).** At 3,000 hours from 600 players, Bungie's team could measure rates per area of a map and still needed a researcher behind the glass to explain them. Your study is a few hundred times smaller, so the balance moves further toward observation. The method is the same.

**MMO beta tests.** In year 4, MMO407 week 3 applies the same reasoning to betas with many thousands of player-hours, where the question becomes which content paths got enough exposure. Rates for the popular starting zone are sharp. Rates for the endgame, which few beta players reach, are as vague as your boss wipe rate. Large studios hit the small-sample wall too. They just hit it further into the game.

**Opinion polls.** A national poll of about 1,000 people carries a margin of about ±3 points, as MA102 week 13 shows. A poll whose respondents were chosen as whole households would need a larger sample for the same precision, because people in one household answer alike. Your parties are households.

### Eyes-open design judgment

- **Set thresholds before you look.** A threshold chosen after you see 81% will be chosen to make 81% look fine or bad, whichever the person choosing already believed.
- **Use telemetry for existence and ordering, observation for cause.** With 15 players you can say "disconnects happen and cluster" and "the revive problem touches more players than the tutorial problem". You can't say "the boss is 12% too hard".
- **A "can't decide" row is not a "leave it" row.** It means this evidence is silent. Decide from other evidence, or schedule a targeted test next week.
- **Beware the one bad session.** In a five-session test, one unusual session can produce most of a rate. Always check which sessions an event came from.

### Check this example

1. Another team saw 2 of 12 players disconnect, in two different sessions out of four. Compute the player-level Wilson interval. Against a 5% threshold, what is the verdict?
2. A designer says "the boss is too hard, 5 of 5 parties wiped." What interval does that give, and what would you ask to see instead?
3. Why is "3 of 15 players disconnected, all in session 2" weaker evidence of a netcode bug than "3 of 15, one in each of three sessions"?

<details>
<summary>Answers</summary>

1. `p̂ = 0.167`, Wilson about 4.7% to 44.8%. The low end is just under 5%, so the verdict is "can't decide" at the strict rule, though very close to "act". Because the disconnects are spread over two sessions, clustering is less of a worry. Most teams would act, and should say the evidence is borderline.
2. 5 of 5 gives about 56.6% to 100%. That rules out an easy boss but can't tell "hard" from "impossible". Ask for the observation notes on how each wipe happened and for the death events per mechanic, so you know whether parties died to the design or to confusion.
3. In the clustered case, one cause specific to that session (one tester's connection, one server build) can explain all three. The effective sample is closer to one session than to three players. Spread across sessions, a shared cause in the code is more likely.

</details>

## 4. Trust the counts before you trust the chart

Before any rate goes into the table above, check that your telemetry adds up. Student pipelines lose and duplicate events more often than they get anything subtle wrong. Four checks catch most problems, and each takes one query (DB201 week 11).

- **Starts and ends balance.** Every `session_start` should have a matching `session_end` or a logged crash or disconnect. If 15 players started and 11 ended, five sessions ended in a way your code didn't record.
- **Server and client agree.** If the client sends `player_died` and the server also logs deaths, the counts should match within the handful lost to disconnects. A large gap means one side double-sends or drops. For anything that matters to balance, trust the server, as DB201 week 10 argues.
- **No duplicate event IDs.** A retry loop that resends a batch doubles its counts silently. Count distinct event IDs against total rows.
- **Timestamps fall inside the playtest window.** Events stamped in 1970 or tomorrow come from a client clock or a default value.

Write down what each check found, even when it found nothing. When the instructor asks why you trust a number, "the start and end counts balance, 15 and 15" is an answer. "The dashboard says so" is not.

## 5. From findings to the sprint 4 input list

The review ends with one list, ranked, that becomes next week's polish sprint input. Each line is one finding, written in the UX201 week 14 format, plus three production fields.

- **Evidence.** Which piles support it, with the numbers. "Observation 4 of 6 non-revivers said they didn't know; telemetry 6 of 15, Wilson 19.8% to 64.3%."
- **Type.** Bug (goes to the tracker with a severity, PR101 week 10), design change, polish item, or "needs a targeted test".
- **Rough size.** Estimated hours, the unit your team has planned in since week 4.

Rank by how many players the problem touched and how badly, using the interval's low end when you compare rates, so that a noisy estimate doesn't jump the queue. Anything typed "needs a targeted test" gets a named owner and a test date before beta, or it gets dropped explicitly.

## Studio session plan

Week 11 meeting, 3 hours.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:15 | Instructor briefing: units of analysis, the threshold rule, the four count checks | — |
| 0:15-0:45 | Teams run the four count checks on their telemetry export | Check log with numbers |
| 0:45-1:25 | Fill the evidence table (lab 11): one row per question from the alpha plan, Wilson interval, verdict, clustering check | Evidence table |
| 1:25-1:35 | Break | — |
| 1:35-2:05 | Pair with another team. Each team presents its three strongest findings; the other team challenges the unit and the verdict | Challenge notes |
| 2:05-2:40 | Write and rank the sprint 4 input list; file every bug in the tracker | Ranked list, tracker updated |
| 2:40-3:00 | Instructor walk-round: each team shows its top three items and their evidence | Sign-off on the list |

## Deliverables

Due before the week 12 studio meeting, in the team repository under `production/week11/`.

1. **Evidence table** (lab 11 template), every row with `k`, `n`, unit, interval, threshold and verdict. Checked by recomputing two random rows.
2. **Count-check log** with the four checks and their numbers. Checked by comparing one count against the raw export.
3. **Sprint 4 input list**, ranked, every line with evidence, type and size. Checked by tracing three lines back to the evidence table or the observation notes.
4. **Tracker updated.** Every finding typed "bug" exists in the tracker with severity and priority.

## Common failure modes

- **Counting players when the outcome belongs to the party.** "12 of 15 players wiped" is 4 of 5 parties. Recount at the right unit.
- **Treating the average as the answer.** "80% finished the tutorial" with no interval invites the team to argue from a number it can't defend.
- **Moving the threshold after seeing the data.** If a threshold changes, write down why, and write it before the table is filled.
- **Dropping the "can't decide" rows.** They are the list of targeted tests you still need.
- **Trusting a chart built on unbalanced counts.** If starts and ends don't match, every rate that uses "sessions" as its denominator is wrong.
- **Letting the most senior voice rank the list.** The ranking rule is written down. Use it, then argue about the exceptions.

## Review checklist

The instructor checks, at the week 12 meeting:

- [ ] Every rate in the evidence table states its unit, and party-level outcomes use parties as `n`.
- [ ] Two recomputed Wilson intervals match the table to one decimal place.
- [ ] Thresholds are dated before the playtest, or any change is explained.
- [ ] At least one clustering check is shown for an event that could depend on a session.
- [ ] The four count checks are logged with numbers, and any imbalance is explained or fixed.
- [ ] The top three items on the sprint 4 list each cite both observation and telemetry, or say why one is missing.
- [ ] Every "needs a targeted test" item has an owner and a date, or is marked dropped.

## Sources

- Thompson, C. "Halo 3: How Microsoft Labs Invented a New Science of Play." *Wired*, issue 15.09, 21 August 2007 (read via the Internet Archive copy of 17 March 2014). More than 3,000 hours of Halo 3 play from about 600 players analysed by Randy Pagulayan's team; tracking of where players were killed; the observed tester who missed the grenades because they were not visible enough; Halo 3 release date of 25 September 2007.
- Wilson, E. B. (1927). "Probable inference, the law of succession, and statistical inference." *Journal of the American Statistical Association* 22(158), 209-212. The score interval used in section 3, as taught in MA102 week 13.
- The alpha playtest numbers in section 3 are a constructed example for teaching. They are not data from any real team.

# MMO308 · Week 13 — Incident Response

**Why this matters:** Every live game breaks. What players remember is how long it stayed broken and what you told them while it was. The first hour of an incident is spent making choices under uncertainty. Teams that practise those choices are down for minutes, and teams that improvise are down for days.

**You will be able to:**
- Compute the expected outage and the chance of still being down after `t` minutes for a revert-first and a fix-forward response, and find the break-even confidence at which reverting pays.
- Measure an incident's cost in player-hours from telemetry against a same-hour-last-week baseline, including rebound.
- Design a severity table, an incident role list and a player-communication cadence for a small MMO team.
- Write a blameless postmortem whose action items change the numbers in the model.

**Before class:** Beyer, Jones, Petoff and Murphy (eds.), *Site Reliability Engineering* (O'Reilly, 2016), chapter 14 "Managing Incidents" and chapter 15 "Postmortem Culture" (free at sre.google, about 40 minutes). Roblox, "Roblox Return to Service 10/28-10/31/2021" (January 2022), the sections on the timeline and the root causes (about 20 minutes).

**Prerequisites from earlier courses:** [MMO302 week 14, observability](../../MMO302-mmo-server-architecture/lectures/w14-observability-logs-metrics-traces.md) (which alerts page a person; this week starts at the page). [MA102 week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md) (mean `1/p` and the dry curve `(1 − p)^n`). [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md). [DB201 week 12, dashboards and KPIs](../../DB201-data-persistence-and-telemetry/lectures/w12-dashboards-and-kpis.md) (concurrent users and fair comparisons). [DB201 week 9, schema migrations](../../DB201-data-persistence-and-telemetry/lectures/w09-schema-migrations-in-a-live-game.md) (expand and contract). Data restores are [DB201 week 14](../../DB201-data-persistence-and-telemetry/lectures/w14-backups-and-disaster-recovery.md), and the choice between rolling back, tracing and banning after a dupe is [MMO309 week 11](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w11-exploit-response-rollback-vs-ban.md). This lecture uses both without repeating them.

**Interactive:** [`examples/w13-revert-or-fix.html`](../examples/w13-revert-or-fix.html). Keep it open during section 2.

---

## 1. What an incident is

An **incident** is an unplanned event that hurts players now and needs a coordinated response. The word "coordinated" matters. A crash that one engineer fixes in five minutes, alone, is a bug. A login outage that needs the server team, the database owner and the community manager at once is an incident, because now three people can make conflicting changes and nobody is telling players anything.

Google's SRE book gives three triggers for declaring one. Declare an incident if a second team is needed, if the problem is visible to customers, or if an hour of focused work has not solved it. All three are about coordination cost, not about how clever the bug is. Adopt them as written. Most game teams declare too late, because declaring feels like admitting the problem is big.

Four clocks describe every incident. You met the first in MMO302 week 14.

- **Time to detect.** From the moment players are hurt until someone is paged.
- **Time to mitigate.** From the page until players stop being hurt. The bug may still exist.
- **Time to resolve.** Until the real fix ships and any temporary measure is removed.
- **Time to learn.** Until the postmortem's action items are done.

Players feel only the first two. This lecture is mostly about the second, because it is the clock your decisions control most directly. The priority order the SRE workbook gives is the one to memorise. Stop the bleeding, restore service, and keep the evidence so you can find the root cause later. In that order.

### Mitigation is not a fix

A **mitigation** stops the harm without explaining it. Reverting the last deploy, switching off a feature, draining a bad server, pausing the auction house, and closing the store to new sign-ups are all mitigations. Google's workbook calls them **generic mitigations**, blunt tools you prepare before any incident so you can use them before you understand the problem.

A **fix** removes the cause. It needs a diagnosis, then code, then testing, then a deploy. A fix is always better in the end. The question this week is what to do first.

## 2. Worked example: revert first or fix forward?

### The hook

On 28 October 2021 Roblox went down, and it stayed down for 73 hours. Roblox's own postmortem lists what the team tried in order. First they suspected failing hardware and replaced machines, then upgraded the whole cluster to bigger servers. Then they reset the cluster from a snapshot. Then they cut load by switching off non-essential services. Then they moved back to the older, smaller servers. About 54 hours in, they found two causes working together. One was a streaming feature in Consul, the service-discovery system every Roblox service used, which had been enabled on 27 October, the day before the outage. The other was a storage-layer problem that turned small writes into huge ones. Switching the streaming feature off brought write times back to normal, and full service returned on 31 October.

Hindsight is cheap, and the storage problem was real and hard to see. But the feature that was switched on the day before was part of the cause, and turning it off was part of the cure. So ask the question every on-call engineer faces in the first ten minutes. When something new went out recently, should you undo it before you know whether it is to blame?

### The model

Two strategies, each described by a few numbers you can estimate before any incident happens.

**Fix forward.** You diagnose. Diagnosis runs in rounds of `r` minutes: form a hypothesis, test it, read the result. Each round finds the cause with probability `p`, independent of the others. Once found, the fix takes `F` minutes to write, test and deploy.

**Revert first.** You immediately undo the most recent change (roll back the deploy or flip its kill switch). That takes `R` minutes. With probability `q` the recent change was the cause and the game recovers. With probability `1 − q` it was not, and you fall back to fixing forward, starting at minute `R`.

The number of diagnosis rounds is geometric, exactly the "kills until the drop" count from MA102 week 7, with a round in place of a kill. So its mean is `1/p` and the chance it takes more than `k` rounds is `(1 − p)^k`. That gives:

```
fix forward:   E[outage] = r/p + F
               P(still down at t) = (1 − p)^floor((t − F)/r)      for t ≥ F + r, else 1

revert first:  E[outage] = R + (1 − q) × (r/p + F)
               P(still down at t) = (1 − q) × [fix-forward curve at t − R]   for t ≥ R, else 1

revert pays off when  q > q* = R / (r/p + F)
```

- `r` is the length of one diagnosis round, in minutes.
- `p` is the chance one round finds the cause. Hard bugs have small `p`.
- `F` is the minutes from "we know the cause" to "the fix is live".
- `R` is the minutes to revert the last change.
- `q` is your honest belief that the last change is the cause.
- `q*` is the break-even belief. Above it, reverting first lowers the expected outage.

The last line comes from setting the two expectations equal: `R + (1 − q)(r/p + F) = r/p + F` gives `R = q (r/p + F)`.

Multiply any outage length by the number of affected players, `N`, to turn minutes into player-minutes. Every result below scales with `N`, so the choice between strategies does not depend on it. Only the size of the stakes does.

### Numbers you can check

The numbers are invented for teaching, sized like a mid-sized MMO's evening peak. A round takes `r = 30` minutes and finds the cause with `p = 0.25`. A fix takes `F = 45` minutes to ship. A revert takes `R = 20` minutes. The on-call engineer thinks the patch that went out this afternoon has a `q = 0.6` chance of being the cause. `N = 40,000` players are affected.

```python
import math

r, p, F = 30, 0.25, 45   # minutes per diagnosis round, chance a round finds the cause, minutes to ship the fix
R, q = 20, 0.6           # minutes to revert the last change, chance the last change is the cause
N = 40_000               # players affected while the incident lasts

def fix_forward():
    """Expected outage in minutes if you diagnose, then fix."""
    return r / p + F

def revert_first():
    """Expected outage if you revert first and diagnose only if the revert fails."""
    return R + (1 - q) * fix_forward()

def still_down(t, first):
    """Chance the game is still down t minutes after the page."""
    def ff(t):                      # fix forward, starting at time 0
        if t < F + r:
            return 1.0
        rounds = math.floor((t - F) / r)   # rounds that must have failed
        return (1 - p) ** rounds
    if first == "fix":
        return ff(t)
    if t < R:
        return 1.0
    return (1 - q) * ff(t - R)

ea, eb = fix_forward(), revert_first()
print(f"fix forward:  {ea:5.0f} min expected, {ea * N / 60:9,.0f} player-hours")
print(f"revert first: {eb:5.0f} min expected, {eb * N / 60:9,.0f} player-hours")
print(f"revert pays off when q > R / (r/p + F) = {R / ea:.3f}")
print(" t(h)  P(down) fix  P(down) revert")
for h in (1, 2, 4, 6, 8):
    print(f"{h:4d}  {still_down(60*h, 'fix'):11.3f}  {still_down(60*h, 'revert'):14.3f}")
print(" p     E[fix]  q*")
for pp in (0.5, 0.25, 0.1, 0.05):
    e = r / pp + F
    print(f"{pp:4.2f} {e:7.0f}  {R / e:.3f}")
```

It prints:

```
fix forward:    165 min expected,   110,000 player-hours
revert first:    86 min expected,    57,333 player-hours
revert pays off when q > R / (r/p + F) = 0.121
 t(h)  P(down) fix  P(down) revert
   1        1.000           0.400
   2        0.562           0.300
   4        0.178           0.095
   6        0.056           0.030
   8        0.018           0.010
 p     E[fix]  q*
0.50     105  0.190
0.25     165  0.121
0.10     345  0.058
0.05     645  0.031
```

Check the first lines by hand. Fixing forward, the mean number of rounds is `1/0.25 = 4`, so diagnosis takes 120 minutes, plus 45 to ship, which is 165. Reverting first costs 20 minutes for sure, and 40% of the time you then pay the full 165 as well: `20 + 0.4 × 165 = 86`. At 40,000 affected players, the difference is about 52,700 player-hours.

Read the middle table next. Two hours after the page, a team fixing forward is still down 56% of the time. To be back by minute 120 it must have found the cause by the end of round two (minute 60, plus 45 to ship), and `0.75² = 0.5625` is the chance it did not. At four hours, almost one incident in five is still open.

Now the most useful table, the bottom one. The break-even belief `q*` is small. With these numbers, if you think there is even a 12% chance the recent change is to blame, reverting first is the better bet. And look at how `q*` moves with `p`. When the bug is hard (`p = 0.05`, a 1-in-20 chance per round), `q*` drops to about 3%.

That is the counterintuitive part. Engineers hesitate to revert when they are unsure the change caused the problem. They want to understand first. The model says the opposite. The less you understand, the lower `p` is, the longer diagnosis will take, and the more a cheap revert is worth even when you doubt it will work. Being confused is a reason to revert, not a reason to wait.

### Seeing it move

Open the interactive. The left panel shows the two expected outages as bars, with `q*` marked on a belief slider. The right panel shows the two "still down" curves over eight hours, the fix-forward curve as a staircase that starts at 1 and falls one step per failed round, and the revert-first curve with a cliff at minute `R`.

Drag `p` down from 0.5 to 0.05. On the left, both bars grow, but the revert-first bar grows more slowly. On the right, the fix-forward staircase stretches toward the right edge, while the revert-first curve drops to `1 − q` at minute 20 and stays low. Then drag `R` up to 120 minutes, a slow revert that needs a full server restart. The cliff moves right, `q*` climbs, and at low `q` fixing forward wins again. That is the lever you control between incidents: make `R` small.

### Cross-game recognition

Real teams rarely publish their `p` and `q`. What they do publish is which lever they pulled, and each lever maps onto `R` and `q`.

**Roblox, October 2021.** The hook, rewritten. The team spent over two days in rounds with small `p`: hardware, snapshot, load, server size. Each was a reasonable hypothesis and each took hours to test. The change from the day before was a candidate with a real `q`, and the eventual cure included switching it off. The storage problem meant that switching streaming off on day one might not have been enough by itself, so `q` for "disable streaming alone" was below 1. The model still says a cheap revert of a recent change belongs early in the list, not at hour 54.

**New World (Amazon Games, 2 November 2021).** A coin duplication exploit was spreading. Amazon disabled the trading post, player-to-player trading, coin transfers and guild treasuries, said trades would stay off overnight while a fix was built and tested, and said exploiters would be banned. In model terms this is a revert with small `R` (a server-side switch) and `q` close to 1 for the harm, because no transfers means no duped coins moving. It did not fix the bug. It stopped the bleeding while fixing forward ran in parallel, and it had a price. Every honest player lost trading for the night. What happens to the duped coins afterward is MMO309 week 11's problem.

**Old School RuneScape (1 October 2024).** A potion storage glitch let players duplicate potions. Jagex started a 15-minute countdown during which Grand Exchange trading, shops and ground items were blocked, then took the game down, rolled back to before the countdown (complete at 09:45 UTC), and brought servers back at 13:00 UTC after testing a fix. That is revert first twice over. The trade block is a kill switch on the spread, and the rollback is a revert of the world state. The three hours after the rollback are the `F` of the fix-forward branch, run with players offline, where a mistake could not spread.

**Final Fantasy XIV: A Realm Reborn (August 2013).** At relaunch the servers could not hold the number of concurrent players, and Square Enix temporarily suspended digital sales. Here the "change" being reverted is the flow of new players. Stopping sales has a tiny `R`, and it attacks the cause (load) directly. It costs revenue, which is the price of this particular switch.

Four incidents, one move. Find the cheapest thing that undoes the most recent change to the system, whether that change is code, a feature, a transfer channel or a wave of new players, and ask whether its `q` beats `R / (r/p + F)`.

### Eyes-open design judgment

Revert first is a default, not a law. Know when it fails.

- **Some changes cannot be reverted.** A patch that ran a data migration, such as rewriting item stats or converting a currency, cannot be undone by redeploying old code, because the old code does not understand the new data. `R` for that patch is a database restore (DB201 week 14), which may be hours and may lose progress. The fix is at design time. Ship migrations in the expand and contract order from DB201 week 9, so that the previous server version still runs against the new schema and `R` stays small.
- **A revert has its own risk.** Rolling back a client-server pair where clients already updated can split versions. If the revert needs a forced client patch, `R` includes every player's download.
- **Mitigations cost honest players.** New World's trade shutdown and the RuneScape trade block both took something from everyone. The model treats the outage as the only harm. When the mitigation itself hurts, weigh its harm rate against the harm rate of the incident. Turning off trading to stop a dupe is usually worth it. Turning off all logins to stop a cosmetic bug is not.
- **Kill switches are a design task.** `R` is small only if someone built the switch before the incident. Each risky feature in a patch (a new trade path, a new currency faucet, a new instance type) should ship behind a flag that operations can turn off without a deploy. Budget this in the patch plan. [Week 9 on patch management](w09-patch-management-and-hotfixes.md) covers flags in the release process.
- **Beliefs should be honest.** If the team always says `q = 0.9` because it wants to revert, or `q = 0.05` because it is proud of the patch, the rule breaks. A simple habit is to write `q` in the incident log before acting, and check it in the postmortem.

### Check yourself on the worked example

1. With the lecture's numbers, what `R` makes the two strategies equal when `q = 0.6`?
2. A team's revert takes 90 minutes because it needs a full cluster restart. With `r = 30`, `p = 0.25`, `F = 45`, what is `q*`? Would you revert at `q = 0.4`?
3. Why does `N`, the number of affected players, not change which strategy is better?

<details>
<summary>Answers</summary>

1. Set `R = q (r/p + F) = 0.6 × 165 = 99` minutes.
2. `q* = 90/165 ≈ 0.545`. At `q = 0.4` fixing forward has the lower expected outage (165 against `90 + 0.6 × 165 = 189`). The real lesson is to make the revert faster.
3. Both expected costs are `N` times an expected duration. Multiplying both sides of an inequality by the same positive number does not change which side is bigger. `N` changes how much is at stake, not the ranking.

</details>

## 3. Measuring the damage

After the incident, someone will ask how bad it was. "Down for 90 minutes" is not an answer, because 90 minutes at 04:00 and 90 minutes at 20:00 on a Saturday are very different events. The analyst's answer is **lost player-hours**: the play that would have happened and did not.

You cannot observe what would have happened, so you estimate it with a **baseline**. The standard choice for games is the same time last week. Daily and weekly cycles dominate concurrent-user curves (DB201 week 12), and last week's curve at the same hour already contains them. Scale the baseline by the ratio of today's to last week's concurrent users in the hour before the incident, so a generally busier week does not count as "loss".

```
lost player-hours = Σ over samples of (scaled baseline − observed) × sample length in hours
```

Here is an invented incident sampled every 30 minutes. The patch went out at 19:15. Pre-incident scale factor `51,500 / 52,000 = 0.990`.

| Time | Last week | Scaled baseline | Today | Gap |
|---|---|---|---|---|
| 19:00 | 52,000 | 51,500 | 51,500 | 0 |
| 19:30 | 54,000 | 53,481 | 21,000 | 32,481 |
| 20:00 | 55,000 | 54,471 | 14,000 | 40,471 |
| 20:30 | 55,500 | 54,966 | 15,000 | 39,966 |
| 21:00 | 55,000 | 54,471 | 49,000 | 5,471 |
| 21:30 | 53,000 | 52,490 | 55,500 | −3,010 |
| 22:00 | 50,000 | 49,519 | 51,000 | −1,481 |

The gross loss from 19:30 to 21:00 is `(32,481 + 40,471 + 39,966 + 5,471) × 0.5 = 59,195` player-hours. From 21:30 the game is above its baseline. That is **rebound**, players coming back to finish what they meant to do. Subtract it and the net loss is about `59,195 − (3,010 + 1,481) × 0.5 ≈ 56,950` player-hours.

Report both numbers. The gross figure is what players experienced as frustration. The net figure is what the incident cost in play. A large rebound means players shifted their evening. A missing rebound means they gave up, and that is the number that predicts churn. To check for it, compare next week's retention for players who tried to log in during the outage with players who did not. Retention curves are week 3's tool, and the method for comparing two groups fairly is weeks [5](w05-ab-testing-design.md) and [6](w06-ab-testing-statistics-and-pitfalls.md).

Two cautions. First, last week may itself have been unusual (a holiday, a big update, another incident). Use the median of the last three or four same-weekday curves when you can. Second, concurrent users undercount the harm for players who could not log in at all, since they never show up in the curve. Add failed login attempts from the gateway logs (MMO302 week 9) as a separate line.

## 4. Running the response

### Severity is decided in advance

A **severity table** says, before any incident, how big a problem must be to wake whom. Write it in terms of player impact, which you can measure, not in terms of the technical cause, which you do not know yet. A workable table for a small MMO:

| Severity | Player impact | Response |
|---|---|---|
| SEV1 | Most players cannot log in or play, or data or economy integrity is at risk (dupes, item loss) | Page on-call and a lead now, any hour. Status update every 30 minutes. |
| SEV2 | A major system is down (instances, trading, one region) or a large group is affected | Page on-call now. Status update every hour. |
| SEV3 | A minor feature is broken, workaround exists | Ticket for business hours. Known-issues post. |

Economy integrity sits at SEV1 even when the servers are healthy. A dupe grows every minute it runs, which is why New World and RuneScape both treated trading as the thing to switch off first. [Week 12](w12-economy-monitoring.md) covers the alarms that detect it.

### Roles, not heroes

The SRE book describes four roles in an incident, and they apply unchanged to games.

- The **incident commander** owns the state of the incident and assigns work. They do not debug.
- **Operations** makes changes to the live system. Only this group touches production during the incident.
- **Communications** writes updates for players and for the rest of the studio.
- **Planning** handles the longer tail: filing bugs, arranging hand-offs, tracking temporary changes that must be undone later.

On a five-person live team, one person may hold two roles, but never commander and operations together. The person with their hands in the database cannot also see the whole picture. The commander also keeps a **live incident document**: a timeline, the current hypothesis, what has been tried, the current `q`, and who holds which role. It becomes the postmortem's raw material. Hand-offs are explicit. The book suggests saying "you are now the incident commander" and waiting for a clear yes.

### Talking to players

Players can forgive an outage. Silence makes it worse. Communication has three rules.

1. **Acknowledge fast.** Post within 15 minutes of declaring a SEV1, even if all you can say is that you know and are working on it.
2. **Promise the next update, then keep the promise.** "Next update at 20:30 UTC" gives players a reason to stop refreshing. An update that arrives late costs more trust than an update with no news.
3. **Never promise the fix time.** You do not know it. Look at the fix-forward curve in section 2. Even the median is hard to call, and the 90th percentile is hours away. Promise update times, not fix times.

Put status posts where players already look (launcher, website, social accounts), and on infrastructure that does not share a failure with the game, as MMO302 week 14 argued for monitoring.

### Compensation

After a large outage, many games compensate. Final Fantasy XIV gave all players a week of free play time after its 2013 relaunch congestion. Compensation is a design decision with an analytics side.

- **Size it from the measurement.** Section 3 gives lost player-hours. A comp worth roughly what an affected player lost reads as fair. A comp worth ten times that teaches players to hope for outages.
- **Target it.** Telemetry says who was online or tried to log in during the window. Give them the comp, not the whole account base, when your data supports it.
- **Watch the economy.** Comp paid in currency or tradeable items is a faucet (MMO304 week 3). A generous comp to every account after a big outage can move prices. Prefer subscription time, cosmetics or account-bound boosts.

## 5. The postmortem

A **postmortem** is a written record of an incident: its impact, what was done to mitigate and resolve it, the causes, and follow-up actions to stop it happening again. The SRE book's triggers for writing one include user-visible downtime above a threshold, any data loss, an on-call engineer having to intervene (a rollback, rerouting traffic), resolution taking longer than a threshold, and a monitoring failure that meant a person found the problem first. Add one for games: any event that created or destroyed currency or items outside the rules.

Postmortems must be **blameless**. They look for contributing causes without accusing any person or team, and assume everyone acted in good faith on what they knew at the time. If the engineer who ran the bad migration expects punishment, the next one will hide the mistake for an hour. That hour is time to detect, and you just paid for it in player-hours.

A good postmortem's action items change the numbers in section 2. Read each proposed item and ask which parameter it moves.

| Action item | Parameter it moves |
|---|---|
| Put the new trade path behind a kill switch | `R` down for next time, `q` targeted |
| Make deploys revertible without a restart | `R` down |
| Add per-feature error metrics to the dashboard | `p` up (each round tests a sharper hypothesis) |
| Pre-written runbook for "logins failing after a patch" | `r` down, `p` up |
| Canary the patch to one realm for an hour first | `N` down for the next bad patch |
| Automated alert on the currency ledger | time to detect down |

An action item that moves none of them ("be more careful") is not an action item. Also watch the cost column. Each item costs engineering time, and a postmortem with 30 action items will ship none of them. Rank them by player-hours saved per engineer-day, using the model, and do the top three.

## In-class activity (25 minutes)

Groups of four run a tabletop incident. One person is the incident commander, one is operations, one is communications, and one is the "world", who holds a card with the hidden cause.

1. The world reads the opening. "19:20 UTC, Saturday. Login failures at 38%. Patch 4.2 shipped at 19:05. It adds a new guild bank and changes the login token format."
2. The commander asks the team for `q` for "revert patch 4.2" and writes it down. Operations estimates `R`, `r`, `p` and `F` from the class's shared assumptions (`R = 20`, `r = 30`, `F = 45`, and a `p` the team argues for).
3. Decide, using `q*`. The world reveals whether the revert worked. The cause card may say the patch was innocent (a certificate expired at 19:00).
4. Communications drafts the first two status posts, with next-update times.
5. Afterwards, write three postmortem action items and name the parameter each one moves.

Expected output: the decision with its `q` and `q*`, two status posts, and three action items mapped to parameters. Groups compare. Did any group revert with `q` below `q*`, or refuse to revert above it?

## Common misconceptions

- **"Don't revert until you know it's the patch."** The model says the less you know, the more reverting is worth. With a hard bug, a revert beats waiting at beliefs as low as 3 to 12%.
- **"The outage lasted 90 minutes, so the cost is 90 minutes times our player count."** Cost depends on when it happened and how many players were really affected. Measure it against a same-hour baseline, and separate gross loss from rebound.
- **"A rollback and a revert are the same thing."** A revert undoes a code or configuration change. A rollback restores world data to an earlier time and erases players' progress. The first is cheap and routine. The second is a SEV1 decision with its own trade-offs (MMO309 week 11).
- **"The postmortem should find who made the mistake."** Blame makes people hide problems, which raises time to detect. Postmortems find contributing causes and change the system.

## Check yourself

1. A team has `r = 20`, `p = 0.2`, `F = 60` and `R = 15`. Compute the expected outage for each strategy at `q = 0.3`, and `q*`.
2. Using the fix-forward formula with `r = 30`, `p = 0.25`, `F = 45`, what is the chance the game is still down 4 hours and 15 minutes after the page? Explain the floor in the formula.
3. An incident's gap to baseline, sampled every 15 minutes, is 8,000, 20,000, 20,000, 12,000 and then −2,000 players. Compute gross and net lost player-hours.
4. A studio's postmortem lists "engineers must test patches more thoroughly" as its only action item. Rewrite it as two items that move named parameters in the model.
5. A designer proposes compensating every account with 5,000 gold after a two-hour outage. Give two reasons to push back, using this week's material.

<details>
<summary>Answers</summary>

1. Fix forward `20/0.2 + 60 = 160` minutes. Revert first `15 + 0.7 × 160 = 127` minutes. `q* = 15/160 ≈ 0.094`, so at `q = 0.3` reverting first wins.
2. `t = 255` minutes. `floor((255 − 45)/30) = 7` rounds must have failed, so `0.75^7 ≈ 0.133`. The floor is there because a round only ends in whole steps. Partway through round eight, you have seven failures, not seven and a half.
3. Gross `(8,000 + 20,000 + 20,000 + 12,000) × 0.25 = 15,000` player-hours. Net `15,000 − 2,000 × 0.25 = 14,500`.
4. For example, "canary each patch on one realm for an hour before the rest" (lowers `N` for the next bad patch) and "ship the new feature behind a kill switch" (lowers `R`). Other valid answers name `p`, `r` or time to detect.
5. It is untargeted: most accounts were not online and lost nothing, so measure who was affected and give them the comp. And gold is a faucet, so a flat grant to every account adds currency to the economy and can raise prices. Prefer account-bound or time-based comp, sized from the lost player-hours.

</details>

## Lab / assignment hook

[Lab 13, incident analysis](../labs/lab13.md). You measure a synthetic incident against its baseline, implement the section 2 model with its tail, check it with a simulation, and write a blameless postmortem whose action items are ranked by player-hours saved. Counts toward the analytics labs (40%).

## Sources

- Roblox, "Roblox Return to Service 10/28-10/31/2021", Roblox newsroom, January 2022. 73-hour outage; the sequence of hypotheses (hardware, snapshot reset, load reduction, server size); causes found about 54 hours in; the Consul streaming feature enabled on 27 October; disabling streaming restored write latency; full service on 31 October.
- Beyer, B., Jones, C., Petoff, J. and Murphy, N. R. (eds.) *Site Reliability Engineering*. O'Reilly, 2016. Chapter 14, "Managing Incidents": the incident command, operations, communication and planning roles; the live incident document; explicit hand-off; the three triggers for declaring an incident; the priority to stop the bleeding and restore service while preserving evidence. Chapter 15, "Postmortem Culture": postmortem triggers, the definition of blameless, and the contents of a postmortem.
- Beyer, B., Murphy, N. R., Rensin, D. K., Kawahara, K. and Thorne, S. (eds.) *The Site Reliability Workbook*. O'Reilly, 2018. Chapter "Incident Response": mitigate before root cause, the "3Cs" (coordinate, communicate, control) and generic mitigations such as rolling back releases.
- NWDB, "All Forms of Trading Disabled Due to Coin Duplication Exploits", 2 November 2021, reporting Amazon Games' statement for New World. Trading post, player trading, coin transfer and guild treasury disabled overnight while a fix was tested; exploiters to be banned.
- Old School RuneScape Wiki, "Potion storage glitch" (retrieved September 2026). 1 October 2024; 15-minute restriction on the Grand Exchange, shops and ground items; rollback completed at 09:45 UTC; servers back at 13:00 UTC after testing.
- Wikipedia, "Final Fantasy XIV" (retrieved September 2026). A Realm Reborn relaunch, August 2013: servers unable to handle concurrent players, temporary suspension of digital sales, a week of free play time for all players.
- All model parameters (`r`, `p`, `F`, `R`, `q`, `N`), the concurrent-user series in section 3 and the severity table are teaching assumptions, not figures from any studio.

## Interactive spec: examples/w13-revert-or-fix.html

**Purpose.** Make visible that reverting first shortens both the expected outage and the long tail, and that the break-even belief `q*` falls as the bug gets harder.

**Layout.** Two linked panels side by side on desktop, stacked on mobile (left panel first). Controls in a strip above both.

**Controls (sliders, each with a numeric readout and keyboard steps):**
- `q`, belief the last change is the cause: 0 to 1, step 0.01, default 0.6.
- `p`, chance a diagnosis round finds the cause: 0.02 to 0.8, step 0.01, default 0.25.
- `r`, minutes per round: 10 to 60, step 5, default 30.
- `F`, minutes to ship a fix: 10 to 120, step 5, default 45.
- `R`, minutes to revert: 1 to 180, step 1, default 20.
- `N`, affected players: 1,000 to 200,000, step 1,000, default 40,000 (affects only the player-hours readouts).
- A "Presets" select: "Lecture default", "Hard bug (p = 0.05)", "Slow revert (R = 90)", "Kill switch (R = 2, q = 0.9)".

**Left panel: expected outage.** Two horizontal bars, "Fix forward" and "Revert first", length in minutes, with the value in minutes and in player-hours (`minutes × N / 60`) printed at the end of each bar. Under the bars, a horizontal 0-to-1 belief axis with a marker at the current `q` and a vertical line at `q* = R / (r/p + F)`. The region of the axis right of `q*` is shaded and labelled "revert first wins". The label "q* = 0.121" updates live.

**Right panel: still down after t.** x axis 0 to 480 minutes (labelled in hours), y axis 0 to 1. Two step curves:
- Fix forward: `S_A(t) = 1` for `t < F + r`, otherwise `(1 − p)^floor((t − F)/r)`.
- Revert first: `S_B(t) = 1` for `t < R`, otherwise `(1 − q) × S_A(t − R)`.
Draw both as step functions (no smoothing). Vertical guide lines at 1, 2, 4, 6 and 8 hours. A small table beneath lists `S_A` and `S_B` at those five times with three decimals.

**Formulas.** `E_A = r/p + F`. `E_B = R + (1 − q) × E_A`. `q* = R / E_A` (clamp the displayed marker to [0, 1]; if `q* > 1`, show "revert never wins in expectation").

**Test values (defaults).** `E_A = 165` min, 110,000 player-hours. `E_B = 86` min, 57,333 player-hours. `q* = 0.121`. Table: 1 h 1.000 / 0.400; 2 h 0.562 / 0.300; 4 h 0.178 / 0.095; 6 h 0.056 / 0.030; 8 h 0.018 / 0.010. With `p = 0.05` (others default): `E_A = 645`, `q* = 0.031`. With `R = 90`: `q* = 0.545`.

**Optional simulate button.** Runs 2,000 simulated incidents per strategy using the model (geometric rounds drawn with a seeded random generator) and overlays the empirical survival curves as faint dots, showing they match the formulas.

**The one insight.** When the user drags `p` downward, the fix-forward staircase stretches to the right while the revert-first curve keeps its early cliff, and the `q*` line slides left. The less you understand the bug, the more a revert is worth.

**Accessibility and style.** Shared palette tokens from `templates/interactive-tokens.css`. Fix forward and revert first use two palette colors plus different line dash patterns so they differ without color. All numbers also appear as text. No game names or art in the visual.

# PR301 · Week 08 — Sprint 3 Review and the Alpha Go/No-Go

**Why this matters:** Next Friday your world goes live for 48 hours and you will be asleep for some of them. This mid-sprint session, halfway through sprint 3, sets the criteria that decide whether it is safe to leave running, and the sprint 3 review at the start of week 9 checks them. In a persistent world, bugs that create or destroy value do not go away when the session ends. They stay in the database, spread through trade, and have to be cleaned up by hand.

**You will be able to:**
- Check the economy increment against the ledger at the midpoint and at the sprint 3 review, not only on screen.
- Apply a severity scale for persistent worlds, in which anything that corrupts saved state or creates value is S1 however rare it is.
- Forecast the bug work between now and the alpha freeze from open counts, arrival rates and fix times, and compare it with team capacity.
- Close the gap with explicit cuts and pre-tested kill switches, and write go/no-go criteria the team can check on Thursday.

**Before class:** Reread [PR101 week 10](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md) (severity, priority and bug reports) and [MMO309 week 4](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w04-duplication-exploits-and-transactional-design.md) (why a rare dupe is certain for an attacker). Skim [MMO308 week 9](../../MMO308-live-operations-analytics-and-experimentation/lectures/w09-patch-management-and-hotfixes.md) on hotfixes. Bring the tracker export (every bug with severity, opened date, closed date and hours logged), the ledger queries from sprint 3 and a midpoint build.

**Prerequisites from earlier courses:** [DB201 week 6](../../DB201-data-persistence-and-telemetry/lectures/w06-race-conditions-and-the-duplication-bug.md) (race conditions and the dupe). [DB201 week 14](../../DB201-data-persistence-and-telemetry/lectures/w14-backups-and-disaster-recovery.md) (restores you have actually tested). [MMO302 week 7](../../MMO302-mmo-server-architecture/lectures/w07-persistence-strategies-write-through-periodic-event-sourcing.md) (persistence strategies and what a crash loses). [MMO309 week 11](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w11-exploit-response-rollback-vs-ban.md) (rollback or ban). [PR201 week 9](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w09-sprint-3-review.md) (scope cuts and the feature freeze).

---

## 1. What this review has to settle

Sprint 3 runs from the week 7 session to the week 9 session, and its review opens week 9, two days before the freeze. This week's session sits at the midpoint, so it asks two questions, in this order.

**Is sprint 3 on track to meet its goal?** The week 7 goal had a ledger clause, so check it the way week 10 will, today on the midpoint build and again at the review on the tagged build. Start a fresh world and run bots for an hour, with trading and crafting. Then run the two queries from sprint 3: money supply, and the ledger summed by reason code. The ledger equation from [week 7](w07-sprint-3-economy-and-crafting.md) must hold exactly:

```
M_end − M_start = Σ faucets − Σ sinks
```

If it is off by even one copper, the economy stories are not done. Something changes a balance without going through the logging function. It is far cheaper to find that now, with bots and one hour of data, than after a weekend with humans.

**Can the world run unattended from Friday 18:00 to Sunday 18:00?** You will not answer this today. Today you agree the criteria and the plan to meet them. The decision is made at the freeze on Thursday of week 9, against the list in section 5.

## 2. Severity in a persistent world

The S1 to S4 scale from [PR101 week 10](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md) still applies, with one change. In a session game, severity is about the player's experience in that session. In a persistent world, add a question: **does the damage outlive the session?**

| Severity | Persistent-world rule | Examples |
|---|---|---|
| S1 | Crashes the server, corrupts saved state, loses progress, or creates or destroys value. Any frequency. | Trade dupe on disconnect; inventory lost when two saves overlap; mail copper saved on one side only |
| S2 | Blocks a feature the alpha is meant to test, with no workaround | Market listings never expire; party loot goes to the wrong member |
| S3 | Wrong but survivable, or has a workaround | Quest tracker shows stale counts; repair cost shown before discount |
| S4 | Cosmetic | Typo in an item name |

"Any frequency" matters. [MMO309 week 4](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w04-duplication-exploits-and-transactional-design.md) showed that a dupe which almost never fires by accident fires within a handful of tries for a player who knows how to trigger it. Your testers are game development students. Assume they will look.

## 3. Reading the tracker

Pull three numbers per severity from the tracker for the last two weeks.

- **Open now**, `B`.
- **Arrival rate**, `λ`: bugs opened per week. Use the last two weeks, not the whole project, because the rate follows how much new code is landing.
- **Mean fix time**, `h`: hours logged per closed bug. If your team does not log hours, estimate from the last ten closed bugs and say so.

A tracker that cannot give you these numbers has told you something too. Fix the process before the weekend, because the alpha will produce more bugs than any sprint so far.

## 4. Worked example: will the bugs fit before the freeze?

### The hook

On 2 November 2021, five weeks after New World launched, Amazon Games turned off every way for players to move wealth to each other. That meant the trading post, player-to-player trades, currency sending and the guild treasury. The community team's posts, collected by the NWDB news site, said they were aware of a possible gold duplication exploit, would ban the people using it, and would keep trading off while they built and tested a fix. A studio with a live game and a large team chose to switch off its entire economy rather than ship with a known dupe.

*Saltmarsh* has seven people, ten days and a list of open bugs. The question is the same as Amazon's. What must be fixed, what can be switched off, and does the remaining work fit?

### The model

For each severity, the bugs you must close before the freeze are the open ones, plus the ones that will arrive in the meantime, minus the number you are allowed to leave open:

```
must_fix = B + λ·T − allowed
work     = Σ over severities of must_fix × h  +  unfinished features
capacity = people × available hours per week × T × f − reserved
gap      = work − capacity
```

where `T` is the time to the freeze in weeks, `f` is the focus factor and `reserved` is time already committed to the alpha operations work from week 9 (runbook, backup drill, on-call setup). Fix times come from hours logged on tickets, the same unit as your estimates, so the focus factor applies to them as it does to stories.

### Numbers you can check

This session is on Tuesday of week 8. The freeze is Thursday of week 9 at 18:00, so `T = 1.5` weeks. *Saltmarsh* has seven people with 6.5 available hours a week each (week 3), and plans with `f = 0.5`, the middle of its measured 0.46 and 0.54.

| Severity | Open `B` | Arrivals per week `λ` | Mean fix hours `h` | Allowed open at freeze |
|---|---|---|---|---|
| S1 | 2 | 2 | 3 | 0 |
| S2 | 9 | 4 | 1.5 | 3 |
| S3 | 15 | 6 | 1 | no limit |

```
capacity  = 7 × 6.5 × 1.5 × 0.5 − 5 (alpha ops)   = 34.1 − 5 = 29.1 h

S1 must_fix = 2 + 2 × 1.5 − 0                      = 5    → 5 × 3    = 15 h
S2 must_fix = 9 + 4 × 1.5 − 3                      = 12   → 12 × 1.5 = 18 h
bug work                                                               = 33 h
unfinished feature: crafting window UI                                 = 8 h
total                                                                  = 41 h
gap = 41 − 29.1                                                        = 11.9 h over
```

The team is about 12 hours over, 41% of its capacity. Wishful thinking would say "we'll work harder." The review instead looks for cuts that change the scope, not the effort.

**Cut 1: a plain crafting menu.** The alpha asks whether the crafting economy works, not whether the crafting window looks good. A text list of recipes with a Craft button is 1 hour, not 8. Saves 7 h.

**Cut 2: flag off features the alpha is not testing.** Six of the twelve S2 fixes are in the guild bank and the emote wheel, which the alpha does not need. Hide both behind feature flags at a quarter of an hour each. The S2 fixes drop from 12 to 6, saving `6 × 1.5 = 9` h, at a cost of `6 × 0.25 = 1.5` h. Net saving 7.5 h.

```
total after cuts = 41 − 7 − 7.5 = 26.5 h
slack            = 29.1 − 26.5  = 2.6 h  (9% of capacity)
```

It fits, with 2.6 hours of slack. Now test the plan against the number you trust least, the arrival rate. If bugs arrive 50% faster than last fortnight, that is 1.5 more S1s and 3 more S2s:

```
extra = 1.5 × 3 + 3 × 1.5 = 4.5 + 4.5 = 9 h
total = 26.5 + 9          = 35.5 h   → 6.4 h over
```

So the plan is safe in the expected case and fails in a bad but plausible one. That is normal. The answer is not more padding. It is a decision, made today, about what happens if the bad case arrives.

**The kill-switch list.** For each system that can create or destroy value, the team builds and tests a flag that turns it off at runtime without a restart: player trade, the market, mail attachments and crafting stations. If an S1 in one of those systems is open at the freeze, the world launches with that system switched off instead of with the bug. That is what New World did. It costs a slice of the alpha's data, and it never costs the economy.

**The go/no-go rule.** On Thursday at 18:00, the world launches if every open S1 is either fixed or behind a tested kill switch, and at most three alpha-relevant S2s are open. If an S1 that cannot be switched off is still open, for example a crash on login or a save corruption, the weekend shrinks to Saturday only and that day goes on the fix.

### A visual you can move

No separate interactive ships this week. The model is a sum, and lab 08's checker recomputes it from your tracker export. Change the arrival multiplier in `plan.txt` from 1.0 to 1.5 and watch the slack go negative. If you want a picture, [PR201 week 9](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w09-sprint-3-review.md) has a burn-up interactive that shows the same thing as two lines that do or do not meet.

### Cross-game recognition

Two more live games made the same trade in the same form. Something that creates value is open, and the fix is not ready. Remove the feature's reach instead of hoping.

- **Old School RuneScape, 1 October 2024.** Players found that potion storage and a new consumable device could be combined to duplicate potions. According to the OSRS Wiki, Jagex put the worlds on a 15-minute shutdown timer and blocked trading on the Grand Exchange, in shops and on the ground during it. It then rolled the game back and kept it offline for testing until 13:00 UTC. In our terms, an S1 with no fix, handled by a kill switch on every transfer path, then a restore to a known-good state.
- **New World, November 2021.** The hook. Every wealth transfer went behind one switch while the fix was built.

Your version is smaller, and it has one advantage over both studios. You can build and test the switches before the weekend, not during it.

### Eyes-open judgment

- **Arrival rates are not constant.** They rise when new code lands and fall after a freeze. Your last fortnight was a feature sprint, so the forecast is probably pessimistic after Thursday, and optimistic for the first day of the alpha, when humans find what bots did not.
- **Fix times are skewed.** A mean of 3 hours for S1s might be three 1-hour fixes and one 9-hour fix. When one S1 looks deep, estimate it separately.
- **Flagging off is not free.** Each flag adds a code path, and a feature hidden from players can still run on the server. Test the flag in both states.
- **Do not downgrade to fit.** Moving a bug from S1 to S2 because the numbers are tight is the most common way teams "close" a gap. Severity follows the table in section 2, and the instructor checks it.

### Check yourself

1. Dee wants to keep a 1.5-hour quest-log polish story. With the cuts in place and expected arrivals, what is the slack?
2. How many S1s above forecast can the plan absorb before it goes over, if S2 arrivals stay as forecast?
3. Why does the go/no-go rule treat an open mail dupe differently from an open login crash?

<details>
<summary>Answers</summary>

1. `29.1 − (26.5 + 1.5) = 1.1` hours, 4% of capacity. One S2 would use most of it. The story should wait for sprint 4.
2. The slack is 2.6 h and each S1 costs 3 h, so it cannot absorb even one. A single extra S1 puts the plan 0.4 h over. That is why the kill-switch list exists.
3. A mail dupe lives in a system that can be switched off, so the world can run safely without it. A login crash cannot be switched off without closing the world. There is no reduced version of the alpha that avoids it.

</details>

## 5. The go/no-go list

Agree this list at the review and check it on Thursday. Each item is yes or no, with evidence.

1. No open S1, or every open S1 is behind a tested kill switch.
2. At most three open S2s in features the alpha tests.
3. The ledger reconciles to zero on a one-hour bot run of the freeze build.
4. The tick rule from [week 6](w06-sprint-2-review.md) (mean at or under 60 ms, p99 at or under 80 ms) passes at 100 bots in the market-square layout on the freeze build, and a 100-bot spread-layout run is recorded beside it.
5. The server survives `kill -9` and restarts with every character's last saved state, and the loss window matches your persistence design ([MMO302 week 7](../../MMO302-mmo-server-architecture/lectures/w07-persistence-strategies-write-through-periodic-event-sourcing.md)).
6. Last night's backup has been restored on a second machine and a character logged in on it ([DB201 week 14](../../DB201-data-persistence-and-telemetry/lectures/w14-backups-and-disaster-recovery.md)).
7. Every kill switch has been flipped on the freeze build, both ways, while players were online.
8. The on-call rota and runbook from lab 09 are complete.

Items 5 to 8 are week 9's work, but agree them now so that the 5 reserved hours are spent on them.

## Studio session plan

Week 8 meeting, 3 hours, in the middle of sprint 3. Two teams are paired, as in week 6. The sprint 3 review opens the week 9 session.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:10 | Both midpoint builds started on fresh worlds; one-hour bot runs with trade and crafting begin | Bots running |
| 0:10-0:30 | Team A stand-up and burn-down check: goal-chain status, hours done so far, drop order | Burn-down decision |
| 0:30-1:00 | Playtest: team B tries to break team A's economy by hand (trade during disconnect, craft with a full bag, list and cancel quickly) | Issue log with severities |
| 1:00-1:10 | Break | |
| 1:10-1:30 | Team B stand-up and burn-down check | Burn-down decision |
| 1:30-2:00 | Team A tries to break team B's economy | Issue log with severities |
| 2:00-2:15 | Both bot runs end; each team runs its ledger queries | Residual per team, zero or not |
| 2:15-2:45 | Each team alone: tracker export, bug forecast, cuts, kill-switch list | Lab 08 passing |
| 2:45-3:00 | Go/no-go list agreed with the instructor | Signed go/no-go list |

At the sprint 3 review (first part of the week 9 session): goal answered yes or no on the tagged build, done hours, the sprint 3 focus factor, a one-hour ledger reconciliation on that build, and the retrospective.

## Deliverables

In `production/week08/`.

Due 48 hours after this meeting:

1. **Freeze plan** in the lab 08 format ([`labs/lab08.md`](../labs/lab08.md)), passing `check_gonogo.py`: tracker numbers, forecast, cuts, slack, and the pessimistic case.
2. **Kill-switch list**: each system, its flag name, who can flip it, and the date it was tested.
3. **Go/no-go list** signed by the team and the instructor.
4. **Midpoint reconciliation**: the one-hour ledger run on the midpoint build, with its residual.

Due at the sprint 3 review, start of week 9:

5. **Sprint 3 review record**: goal met (yes or no), hours committed and done, the sprint 3 focus factor, burn-down, and the one-hour ledger reconciliation on the tagged build with its residual.

## Common failure modes

- **Reviewing the economy by looking at it.** Copper goes up when you kill wolves, so it looks right. Only the reconciliation shows whether some path skips the ledger.
- **Severity by frequency.** "It only happened once" is how a dupe ends up as S3. Anything that creates value is S1.
- **Planning at 100% of capacity.** Zero slack in the expected case means certain failure in the bad case. Aim for about 10% slack and a written plan for the rest.
- **Kill switches that need a restart.** A restart on Saturday night drops every player and may lose unsaved state. Read flags at runtime.
- **Switches never tested.** A flag that was never flipped with players online is a hope, not a switch.
- **Adding features after the freeze.** The freeze exists so that arrival rates fall. Every late feature raises them again.

## Review checklist

The instructor checks at this meeting, in the submission, and at the sprint 3 review at the start of week 9:

- [ ] The one-hour ledger reconciliation was run on the midpoint build, with its residual reported, and again on the tagged build at the review, where the sprint goal was answered yes or no.
- [ ] Every bug that creates or destroys value, corrupts state or crashes the server is S1.
- [ ] The forecast uses measured open counts, two-week arrival rates and fix times, and `check_gonogo.py` agrees.
- [ ] Cuts change scope, not effort, and each is recorded in the backlog as cut or flagged.
- [ ] The pessimistic case (arrivals × 1.5) was computed and a response is written down.
- [ ] A kill switch exists for each value-moving system, read at runtime, with a test date.
- [ ] The go/no-go list is signed and every item is checkable on Thursday.
- [ ] The sprint 3 review's retrospective produced one owned change.

## Sources

- NWDB, "All Forms of Trading Disabled Due to Coin Duplication Exploits" (2 November 2021), quoting New World community managers. Trading post, player-to-player trading, coin transfer and guild treasury disabled while a fix was built and tested; users of the exploit to be banned. https://nwdb.info/news/all-forms-of-trading-disabled-due-to-coin-duplication-exploits
- Wikipedia, "New World (video game)" (accessed September 2026, as cited in DB201 week 6). Worldwide release on 28 September 2021.
- Old School RuneScape Wiki, "Potion storage glitch" (accessed September 2026). 1 October 2024; the chugging barrel and potion storage; a 15-minute timer with Grand Exchange, shop and ground-item restrictions; rollback completed at 09:45 UTC; worlds back online at 13:00 UTC. https://oldschool.runescape.wiki/w/Potion_storage_glitch
- Schwaber, K. and Sutherland, J. (2020). *The Scrum Guide*, November 2020 edition.
- The bug counts, rates, fix times and capacity are invented for teaching. The persistent-world severity table and the go/no-go list are this course's conventions.

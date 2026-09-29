# PR301 · Week 10 — Telemetry Review

**Why this matters:** Your world ran for a weekend and wrote down everything. Now you find out which of your plans held. The tick budget, the sign-up model and the money budget were all predictions. This week you put the measurements beside them. The hardest finding is usually in the economy, because a bug there leaves no crash and no error, only gold that should not exist.

**You will be able to:**
- Check the weekend's telemetry for completeness before drawing conclusions from it.
- Compare measured sign-ups, show rate, sessions, session length and event attendance with the week 9 plan, and feed them to the week 13 beta plan.
- Reconcile the money supply against the ledger, and decompose the residual by time and by character to find its causes.
- Compare actual faucets and sinks with the week 7 budget per player-hour and turn every large gap into a ranked sprint 4 input.

**Before class:** Reread [PR201 week 11](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w11-playtest-and-telemetry-review.md) (units of analysis, Wilson intervals, count checks) and [MMO308 week 12](../../MMO308-live-operations-analytics-and-experimentation/lectures/w12-economy-monitoring.md) (economy monitoring). Skim [MMO309 week 11](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w11-exploit-response-rollback-vs-ban.md) on exploit response. Bring the weekend's exports, untouched: telemetry events, the ledger, the final database backup, the tick log and the incident log.

**Prerequisites from earlier courses:** [DB201 week 11](../../DB201-data-persistence-and-telemetry/lectures/w11-pipelines-collect-store-query.md) (pipelines and where events get lost). [DB201 week 12](../../DB201-data-persistence-and-telemetry/lectures/w12-dashboards-and-kpis.md) (dashboards and KPIs). [MMO304 week 12](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w12-economic-telemetry-and-dashboards.md) (economic telemetry). [MMO308 week 3](../../MMO308-live-operations-analytics-and-experimentation/lectures/w03-cohorts-and-retention-curves.md) (retention). [MMO302 week 7](../../MMO302-mmo-server-architecture/lectures/w07-persistence-strategies-write-through-periodic-event-sourcing.md) (what a crash loses under periodic saves).

---

## 1. Trust the counts first

Before any chart, check that the data is whole. [PR201 week 11](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w11-playtest-and-telemetry-review.md) listed count checks for a playtest. A persistent weekend adds three.

- **Sequence gaps.** Every server numbers its events (`server_seq` from [week 7](w07-sprint-3-economy-and-crafting.md)). Count the gaps. Events lost around each crash are expected, and you should know how many. Gaps at other times mean the pipeline drops events under load.
- **Sessions that never end.** A crash leaves logins without logouts. Close them at the crash time, or session length and player-hours come out too large.
- **Humans and bots.** Filter bots out before computing any player number or economy total. Check the filter by counting bot accounts against the bot plan.

Write the results at the top of your report. "Two crashes, 96 events lost in total, all within 5 seconds of a crash; 14 sessions closed at crash time; 81 bot accounts excluded, with their ledger lines" is a finding, and it tells the reader what the rest can be trusted for.

## 2. Stability and concurrency

**Stability.** List every restart with its cause, the loss window players saw, and whether the runbook worked. Plot p99 tick by hour against the week 6 limits. On the *Saltmarsh* weekend, the server crashed twice, at 03:12 and 04:40 on Saturday. Both crashes came from the same bug, crafting with a full bag, first reported in the bug channel at 23:30 on Friday. Fay, on call, flipped the crafting kill switch at 05:05, and a hotfix went out at 11:00. With 19 humans and 81 bots at the event, p99 tick peaked at 74 ms, inside the 80 ms trigger now that the grid was in.

**Concurrency.** Measure the rates from the week 9 model and set them beside the plan.

| Rate | Plan | Measured | From |
|---|---|---|---|
| Sign-ups `I` | 60 | 40 | the sign-up form |
| Show rate `s` | 0.55 | 26 / 40 = 0.65 | logins ÷ sign-ups |
| Sessions per player `k` | 2.5 | 70 / 26 = 2.69 | sessions ÷ players |
| Session length `W` | 1.5 h | 147 / 70 = 2.1 h | player-hours ÷ sessions |
| Event attendance `e` | 0.6 | 17 / 26 = 0.65 | players who joined the Saturday hunt ÷ players |

Recruiting fell short, and the players who came stayed longer and showed up more reliably than planned. Put the measured rates back into the model. `L/P = 2.69 × 0.0472 × 2.1 = 0.267`, and online per sign-up is `0.65 × (0.654 + 0.346 × 0.267) = 0.485`. That predicts `40 × 0.485 = 19.4` humans at the event, the 17 who joined the hunt plus about two others online in that hour. The team saw 19. The expected-value answer for 50 at the beta is now `50 / 0.485 = 104` sign-ups. [Week 13](w13-beta-open-class-playtest.md) adds the uncertainty on top, because 40 sign-ups is a small sample.

**Return rate.** Of the 26 players, 17 played on a second day, 65%. With `n = 26`, the Wilson 95% interval from PR201 week 11 is 46% to 81%. That is too wide to compare with any shipped game's retention, and it should not be compared anyway. Your testers were recruited friends on a free weekend. Report it as a baseline for the beta, not as a verdict.

## 3. Worked example: where did 8,177 copper come from?

### The hook

In August 2005, Sony Online Entertainment said that a group of EverQuest II players had used a duplication bug to create so much platinum that the game's money supply rose by about a fifth in roughly 24 hours. SOE's spokesman told CNET that the company had many alarms for this kind of event and that they all went off. The economy was restored to its state before the exploit. The detail that matters for you is how they knew. Someone was measuring the total amount of money in the world and comparing it with what the game's own rules could produce.

Your world has the same equation from week 7, and a weekend of data to test it.

### The model

```
residual = (M_end − M_start) − (Σ faucets − Σ sinks)
```

`M` is money supply, the currency in every place it can live. The faucets and sinks are the ledger's totals by reason code. If every balance change went through the logging function and was saved, the residual is zero. A non-zero residual is currency that the rules did not create, or did not destroy, and each cause leaves a different fingerprint:

- **In time.** A steady drift points to a routine path that is not logged. A step points to an event, such as a crash or a patch.
- **By character.** For each character, compare their final balance with the sum of their own ledger deltas. An unlogged faucet shows up on every character. A dupe shows up on a few.

### Numbers you can check

The world started empty, so `M_start = 0`. Human player-hours, from section 2: 147. Bot characters and their ledger lines are excluded.

The ledger against the week 7 budget, after option A (wolves drop 4 copper):

| Code | Budget per player-hour | Actual total | Actual per player-hour | Actual ÷ budget |
|---|---|---|---|---|
| `F_LOOT` | 192 | 26,900 | 183.0 | 0.95 |
| `F_QUEST` | 60 | 7,700 | 52.4 | 0.87 |
| `F_VENDOR` | 50 | 15,950 | 108.5 | **2.17** |
| Faucets | 302 | 50,550 | 343.9 | 1.14 |
| `S_REPAIR` | 50 | 6,600 | 44.9 | 0.90 |
| `S_CONSUMABLE` | 60 | 7,350 | 50.0 | 0.83 |
| `S_CRAFT_FEE` | 40 | 11,040 | 75.1 | **1.88** |
| `S_TRAINING` | 30 | 3,800 | 25.9 | 0.86 |
| `S_MARKET_CUT` | 15 | 1,300 | 8.8 | **0.59** |
| Sinks | 195 | 30,090 | 204.7 | 1.05 |
| Net | 107 | 20,460 | 139.2 | 1.30 |

Money supply from the final backup: 27,937 in character balances, plus 700 in unopened mail. Market listings hold items, not copper, so escrow is zero. `M_end = 28,637`.

```
residual = (28,637 − 0) − (50,550 − 30,090) = 28,637 − 20,460 = 8,177 copper
```

That is 29% of all the money in the world, unexplained. Now decompose it.

**By time.** Chen recomputes the residual at hour marks from the ledger and hourly balance snapshots:

| Time | Characters created | Residual | Starter copper (20 each) | Left over |
|---|---|---|---|---|
| Fri 21:00 | 14 | 280 | 280 | 0 |
| Sat 03:00 | 24 | 490 | 480 | 10 |
| Sat 04:00 | 24 | 1,990 | 480 | 1,510 |
| Sat 05:00 | 25 | 8,010 | 500 | 7,510 |
| Sun 18:00 | 31 | 8,177 | 620 | 7,557 |

Two causes are visible. A smooth drift of exactly 20 per new character is starter copper, which never got a reason code in the code. Lab 07's starter file flagged exactly this line, and the team fixed it in the sheet but not in the server. And there are two steps, of 1,500 by 04:00 and 6,000 by 05:00, which line up with the crashes at 03:12 and 04:40.

**By character.** For each character, the final balance minus the sum of their own ledger deltas, after taking off the 20 starter copper:

- 28 characters are at zero, or within a copper or two for market sellers, 57 in total.
- 3 characters are at +1,500, +3,000 and +3,000. Each ledger shows a large `T_MAIL` out a few minutes before a crash, to an alt that collected the mail and logged out.

The dupe works like this. The week 2 persistence map says currency is write-through. Collecting mail was built that way. Sending mail was not. To fit sprint 3, the send changed the sender's balance in memory and left it for the next periodic save. The alt collects, which saves its new balance at once. Then the server crashes, and the sender is restored from the last periodic save, from before the send. The ledger is right. The saved balances are not. [MMO302 week 7](../../MMO302-mmo-server-architecture/lectures/w07-persistence-strategies-write-through-periodic-event-sourcing.md) called this risk the loss window. Here it became a gain window, and the crafting crash gave players a way to open it.

**The last 57.** The market cut is logged as `0.05 × price` but applied as `floor(0.05 × price)`. The ledger shows 120 market sales, and the mean fractional part of the cut lost to rounding is about 0.475 copper, so `120 × 0.475 = 57`. That is the week 7 rule "log the amount actually applied," broken.

```
starter copper    620   (31 × 20)
mail dupe       7,500   (1,500 + 3,000 + 3,000)
rounding           57
total           8,177   = residual
```

The residual is fully explained. Now the per-hour gaps in the budget table:

- **`F_VENDOR` at 2.17 and `S_CRAFT_FEE` at 1.88 move together.** The excess faucet is `15,950 − 7,350 = 8,600`. The excess crafting fee is `11,040 − 5,880 = 5,160`. Their ratio is 0.6, which is exactly 12 ÷ 20, the fee and vendor price of the reed mat. Reeds are gathered and count as zero, so each mat made 8 copper from nothing: 430 mats, 3,440 copper. This is the arbitrage inequality from week 7, section 5. Lab 07's starter file flagged exactly this recipe, and the team lowered its price in the sheet, but the server's item table still sold the mat for 20. It is the starter-copper failure again, fixed in the plan and not in the build.
- **`S_MARKET_CUT` at 0.59.** Players traded less than the 300 copper per hour the budget guessed. That is not a bug, but it was the weakest part of the week 7 estimate, and it now has a measurement.

Two things are left. The mail dupe comes on top of the 1.30 net ratio: `(20,460 + 7,500) / 147 = 190` copper per player-hour actually reached players, not 139. And the hourly residual alarm from week 9 did not fire at 04:00, because Gus had muted it on Friday at 21:00. It had gone off every hour because of the starter copper. An alarm that fires on a known, harmless cause gets muted, and then it misses the real one.

### A visual you can move

No separate interactive ships this week. The two tables are the picture, and the lab 10 checker recomputes them from your exports. If you want a chart, plot the residual by hour with the crash times marked. The steps are unmistakable.

### Cross-game recognition

- **Old School RuneScape, November 2019.** The OSRS Wiki's page on the "server crash glitch" describes the same mechanism. After a crash, players reverted to their save from up to 15 minutes before, or their last logout. So a player could trade coins away, have the receiver log out, and force a crash, and keep both copies. Jagex said that tip-offs and its own system monitoring found it quickly, and it removed a large amount of gold rather than rolling back. That is our dupe at scale, through trade instead of mail, and the targeted correction *Saltmarsh* will also choose.
- **Old School RuneScape, 12 July 2018.** A change to death handling for the new coin pouch turned some players' items into stacks of 2,147,483,647 coins, the largest 32-bit signed integer. Jagex took the servers offline about 20 minutes after the update and rolled back. This is a faucet with no reason code at all, which is the starter-copper failure at its most extreme.
- **EVE Online's Monthly Economic Report** publishes the faucet and sink totals by source every month. It is the public version of the table above.

### Eyes-open judgment

- **Reconcile per character, not only in total.** A world total can net a dupe against a leak and come out near zero. The per-character check cannot be fooled that way.
- **Correct, or roll back?** The ledger says exactly which copper is duplicated, so the team resets the three senders' balances to their ledger sums. Nobody else loses a weekend of play. Without a trustworthy ledger, a rollback is the only safe tool ([MMO309 week 11](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w11-exploit-response-rollback-vs-ban.md)). What happens to the players is a separate decision, made under the policy you published in week 9.
- **Fix the class of bug, not the instance.** Stop the crafting crash, yes. But the dupe needs no crash bug, only any crash. The fix is to save both sides of every transfer in one transaction when it completes, as the persistence map promised, and as the TrinityCore server does for World of Warcraft 3.3.5a-era trades ([MMO302 week 7](../../MMO302-mmo-server-architecture/lectures/w07-persistence-strategies-write-through-periodic-event-sourcing.md) sources).
- **Budget misses are information.** `S_MARKET_CUT` at 0.59 is a measurement replacing a guess. Update the budget, and do not "fix" the players.

### Check yourself

1. Suppose the team had logged starter copper from the start. What would the residual alarm have shown at 03:00, 04:00 and 05:00 on Saturday?
2. The team fixes the reed mat by setting its vendor price to 10. For the same 430 crafts, how would the mats' vendor income compare with their fees, and would players still make the loop?
3. A world total shows a residual of +300. Per-character checks show 20 characters at −600 each and 3 characters at +4,100 each. What might be going on?

<details>
<summary>Answers</summary>

1. The residual would have held only the rounding and the dupe: +10 at 03:00, +1,510 at 04:00, +7,510 at 05:00. An alarm at "any residual above 100" would have fired at 04:00, forty minutes before the second, larger dupe.
2. Vendor income from mats falls from `430 × 20 = 8,600` to `4,300`, while fees stay `430 × 12 = 5,160`. Each craft now loses 2 copper, so players would stop, and `F_VENDOR` and `S_CRAFT_FEE` would fall back towards budget.
3. Negative per-character residuals mean balances lower than the ledger says: currency destroyed without a sink event, 12,000 in total (for example, a lost save). Three characters hold 12,300 that the ledger does not explain, a probable dupe. The world total, +300, hides both.

</details>

## 4. From findings to sprint 4

List every finding with its evidence, type and size, and rank them as in [PR201 week 11](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w11-playtest-and-telemetry-review.md). For *Saltmarsh* the top of the list is:

1. Write-through for both sides of every transfer: mail send, trade and market completion, each in one transaction. S1, the class of bug behind the dupe.
2. Correct the three senders' balances to their ledger sums, and log the correction as an `S_GM_CORRECTION` sink.
3. Starter copper gets `F_STARTER` in the server, not only in the sheet. Rounding is logged as applied. Unmute the residual alarm and set its threshold.
4. Reed mat vendor price below fee plus inputs. Add the lab 07 recipe check to the build pipeline, reading the server's item table, so the build and the sheet cannot drift apart again.
5. The crafting station with a full bag: the 11:00 hotfix stops the crash by refusing to start a craft when the bag is full, so no reagents are lost now. The proper fix, sending the output to mail, is an S3 for the week 14 triage.
6. Budget update: `S_MARKET_CUT` basis changed to measured, and the other lines re-estimated from the weekend.
7. Beta sign-ups: 104 as the expected value from measured rates, with the event kept. Week 13 sets the final target.

Sprint 4 is social systems. Items 1 to 4 are small and go first, as the sprint 4 bug reserve, before any guild feature can move copper. [Week 11](w11-sprint-4-social-systems.md) sizes them at 4 hours.

## Studio session plan

Week 10 meeting, 3 hours. Teams work mostly alone, with a cross-team readout at the end.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:25 | Count checks: sequence gaps, open sessions, bot filter | Data-quality paragraph |
| 0:25-0:55 | Stability and concurrency tables; measured rates into the week 9 model | Beta sign-up estimate |
| 0:55-1:05 | Break | |
| 1:05-1:50 | Ledger reconciliation: total residual, by hour, by character (lab 10) | Residual fully decomposed or open items named |
| 1:50-2:15 | Budget against actuals per player-hour; every line outside 0.75 to 1.25 explained | Budget table with findings |
| 2:15-2:35 | Ranked sprint 4 input list | Input list with ticket IDs |
| 2:35-3:00 | Readout: each team shows its residual table and its top finding in three minutes | Shared list of failure patterns across the course |

## Deliverables

Due 48 hours after the meeting, in `production/week10/`:

1. **Telemetry review report**: data quality, stability, concurrency with measured rates and the beta sign-up estimate, return rate with its interval, and the economy section.
2. **Ledger reconciliation** in the lab 10 format ([`labs/lab10.md`](../labs/lab10.md)), passing `check_ledger.py`.
3. **Sprint 4 input list**, ranked, with ticket IDs, evidence and sizes.
4. **Exploit response record**: what was found, what was corrected, and what happened to the players involved under the week 9 policy.

## Common failure modes

- **Charts before counts.** A retention figure computed with crashed sessions left open, or with bots included, is wrong in a way nobody sees.
- **Only the world total.** A total residual near zero is reported as "economy clean" while a dupe and a leak cancel out. Reconcile per character.
- **Explaining the residual by guessing.** "Probably rounding" is a hypothesis. Rounding predicts a size, `sales × 0.475`. Check it.
- **Treating budget misses as player error.** Players traded less than you guessed. Update the guess.
- **Muted alarms.** An alarm that fires on a known cause gets muted. Remove the cause, then keep the alarm.
- **Wiping the weekend.** Once the world is reset, nobody can recheck the numbers. Keep the final backup until the course ends.

## Review checklist

The instructor checks in the report and the lab:

- [ ] Count checks are reported first: sequence gaps, closed sessions, bots excluded.
- [ ] Measured sign-ups, `s`, `k`, `W` and `e` are computed from telemetry, and the beta sign-up estimate follows from them.
- [ ] The return rate is reported with its interval and without comparison to shipped games.
- [ ] Money supply includes every place currency lives, and `check_ledger.py` prints `PASS`.
- [ ] The residual is decomposed by time and by character, and every explanation predicts its own size.
- [ ] Every budget line outside 0.75 to 1.25 of plan has a finding.
- [ ] The sprint 4 list ranks the class-of-bug fix above the instance fix, with ticket IDs.
- [ ] The exploit response follows the policy published before the weekend.

## Sources

- Terdiman, D. "Cheaters slam 'Everquest II' economy." CNET News.com via ZDNet, 11 August 2005 (Internet Archive copy, read September 2026). A duplication bug raised EverQuest II's money supply by about a fifth in about 24 hours; SOE's alarms went off; the economy was restored. https://web.archive.org/web/2006/http://news.zdnet.com/2100-1040_22-5829403.html
- Old School RuneScape Wiki, "Server crash glitch" (accessed September 2026). Disclosed 26 November 2019; players reverted to their save from 15 minutes before or their last logout, so trading, logging out the receiver and forcing a crash duplicated items; found through tip-offs and system monitoring; gold removed; no rollback. https://oldschool.runescape.wiki/w/Server_crash_glitch
- Old School RuneScape Wiki, "Coin pouch glitch" (accessed September 2026). 12 July 2018; faulty death handling turned items into stacks of 2,147,483,647 coins; servers taken offline at 11:54 UTC, about 20 minutes after the update; rollback. https://oldschool.runescape.wiki/w/Coin_pouch_glitch
- EVE Online, "Monthly Economic Reports" news category (eveonline.com, accessed September 2026). https://www.eveonline.com/news/t/monthly-economic-report
- TrinityCore, `TradeHandler.cpp` (branch 3.3.5, World of Warcraft 3.3.5a client era), as cited in MMO302 week 7: completed trades save both players' inventory and gold in one database transaction.
- Wilson, E. B. (1927). "Probable Inference, the Law of Succession, and Statistical Inference." *Journal of the American Statistical Association* 22(158), 209-212.
- The *Saltmarsh* weekend's sign-ups, sessions, ledger totals, balances, crash times and character counts are invented for teaching and chosen to be consistent with the week 1 to 9 examples.

# MMO407 · Week 13 — Launch plan workshop

**Why this matters:** Your launch plan is half of this course's grade, and in a studio it is the document a producer reads the night before the doors open. Most launch plans list risks and sort them by expected cost. That sort is right for a year of steady operation and wrong for a single launch week, because a launch is judged once, by how bad it got. This week you learn to judge a plan by its tail, spend a small contingency budget where it removes disasters, and write the triggers that tell a tired war room when to act.

**You will be able to:**
- Compute the expected loss and the chance of a disaster week for a launch risk register, by listing every combination of risks.
- Explain, with numbers, why buying the fixes with the largest expected saving can leave the chance of a disaster unchanged.
- Choose a set of mitigations under a budget with an explicit rule (expected loss, expected loss plus a disaster penalty, or a hard limit on disaster chance) and state the penalty at which your choice changes.
- Write contingency triggers with a signal, a threshold, an action, an owner and a lead time, and check that each trigger fires early enough to help.

**Before class:** Read Klein, G. (2007), "Performing a Project Premortem", *Harvard Business Review* 85(9), 18-19. Read Stone, L. (2016), "Bringing Pokémon GO to life on Google Cloud", Google Cloud blog, 29 September 2016 (10 minutes). Bring your group's drafts from labs 1 to 3 and your [week 12](w12-writing-a-post-mortem.md) post-mortem notes.

**Prerequisites from earlier courses:** [MMO309 week 1, threat modeling](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w01-threat-modeling-for-games.md) (expected annual loss, `f × I`, and the loss ledger; this lecture starts from it and does not re-teach it). [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md) and [MA102 week 5, variance and swingy designs](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w05-variance-and-swingy-designs.md) (two designs with the same average and different spread). [MMO308 week 13, incident response](../../MMO308-live-operations-analytics-and-experimentation/lectures/w13-incident-response.md) (lost player-hours, kill switches, the revert-first decision). [DB201 week 14, backups and disaster recovery](../../DB201-data-persistence-and-telemetry/lectures/w14-backups-and-disaster-recovery.md) (what a tested restore buys you). In this course, [week 1](w01-launch-day-anatomy.md) (the launch timeline and go/no-go criteria), [week 2](w02-capacity-planning-and-login-queues.md) (the capacity plan and layers) and [week 3](w03-beta-strategies.md) (which risks a beta cannot see).

**Interactive:** [examples/w13-risk-register-tail.html](../examples/w13-risk-register-tail.html). Keep it open during section 2.

---

## 1. What a launch plan is

A **launch plan** is the document that says how your game will open, what can go wrong in the first week, what you have bought to stop each thing going wrong, and who does what when it happens anyway. Weeks 1 to 12 gave you its parts. This week you put them together and test the whole.

The course's launch plan has seven sections. Each one comes from a week you have already done, so the workshop is mostly assembly.

| Section | What it contains | Built in |
|---|---|---|
| 1. Launch shape | Preload, head start, unlock time and region order | Week 1 |
| 2. Capacity | World count, caps, layers, queue forecast as a range | Week 2, lab 2 |
| 3. Test evidence | Beta exposure per risk, what the beta could not see | Week 3, lab 3 |
| 4. Risk register | Every launch-week risk with a probability and an impact | This week |
| 5. Mitigations | What you bought, what it cost, which risk it moves | This week |
| 6. Triggers and war room | If-then rules, owners, lead times, roles | This week, week 1 |
| 7. Communication | Status cadence, first message drafts, compensation rule | [Week 9](w09-communication-during-crises.md) |

Sections 4 to 6 are new, and they are where most student plans (and many studio plans) go wrong. A plan can have a perfect capacity model and still fail because its risk register was sorted by the wrong number.

### Risks, from the future backwards

The hardest part of a risk register is listing the risks. Teams list the ones they have worked on, because those are on their minds. Gary Klein's **premortem** is a cheap fix. Before the plan is final, the team imagines that the launch has already happened and was a disaster. Each person writes, alone and for a few minutes, every reason it failed. Then the lead collects one reason from each person in turn until the list is empty. The method builds on an older idea that psychologists call **prospective hindsight**, described by Mitchell, Russo and Pennington in 1989. People look back from an imagined future to find problems before they occur.

Two rules make a premortem work. People write alone first, so the most senior voice does not set the list. And the question is "why did it fail?", not "what might go wrong?". The first question gives permission to name the thing everyone is quietly worried about.

You will run a premortem in the in-class activity. The rest of this section is what you do with the list.

## 2. Worked example: the fix that leaves the disaster in place

### The hook

Pokémon GO launched in Australia and New Zealand on 6 July 2016. Engineers at Google, whose cloud hosted the game, later wrote that Niantic had planned for a target amount of player traffic and a worst case of about five times that target. Within 15 minutes of the launch, traffic passed the target. It eventually reached fifty times the target, ten times the worst case. Players saw crashes and login errors for days, and Niantic's chief executive paused the release in other countries until the service was stable.

The team had a worst case. It was written down and planned for. The launch still went far past it. Here is the question for your plan. When you sort your risks and spend your budget, are you planning for the likely week or for the week that becomes the story? They are different weeks, and the fixes that help one often do nothing for the other.

### The model

MMO309 week 1 gave you **expected loss**, the probability of a risk times its impact, and taught you to rank threats by it over a year. A launch week is one draw, not a year of draws. So you need two numbers for a plan.

Name the parts.

- Risk `i` fires in launch week with probability `pᵢ`, and if it fires it costs `Iᵢ`, its impact. Here impact is lost player-hours in thousands (k ph), the unit MMO308 week 13 measured incidents in.
- The week's total loss `L` is the sum of the impacts of the risks that fired.
- `D` is the **disaster line**, the loss at which the launch becomes the story: press coverage, refunds, a wave of players who never come back. You set it with your producer before you look at the risks.

Then:

```
expected loss        E[L] = Σ pᵢ × Iᵢ
disaster chance      P(L > D) = the sum of the probabilities of every combination of risks whose impacts add to more than D
```

With `n` independent risks there are `2ⁿ` combinations. Each has probability equal to the product of `pᵢ` for the risks that fired and `1 − pᵢ` for the ones that did not. With four risks that is 16 rows, few enough to list by hand.

A **mitigation** is anything you buy before launch that changes one risk's numbers. It can lower `pᵢ` (the risk fires less often) or lower `Iᵢ` (it costs less when it fires). The first kind is **prevention**. The second kind is **containment**. The whole lesson of this section is that the two kinds move the two numbers very differently.

### Numbers you can check

Take one invented launch week with four risks. All values are teaching values.

| Risk | `p` | `I` (k ph) | `p × I` |
|---|---|---|---|
| R1 Login queues over 2 hours at the evening peak | 0.80 | 50 | 40 |
| R2 Authentication outage for half a day | 0.40 | 75 | 30 |
| R3 Duplication exploit found in week 1 | 0.05 | 500 | 25 |
| R4 Character data loss that forces a rollback | 0.02 | 1,000 | 20 |
| **Total** | | | **115** |

The team and the producer set the disaster line at `D = 300` k ph.

Which combinations cross the line? R1 and R2 together cost 125, far below 300. R3 alone costs 500 and R4 alone 1,000. So the week is a disaster exactly when R3 or R4 fires, whatever R1 and R2 do. By the complement rule:

```
P(L > 300) = 1 − P(no R3) × P(no R4) = 1 − 0.95 × 0.98 = 1 − 0.931 = 0.069
```

About one launch in fifteen with this register is a disaster.

Now the budget. The team can afford two of four mitigations. Each costs about the same, three engineer-weeks.

| Mitigation | Kind | Changes | Expected saving |
|---|---|---|---|
| M1 Launch-week layers (week 2) | prevention | R1: `p` 0.80 → 0.20 | 0.6 × 50 = 30 |
| M2 Failover authentication provider | prevention | R2: `p` 0.40 → 0.10 | 0.3 × 75 = 22.5 |
| M3 Trade kill switch plus a currency ledger alarm | containment | R3: `I` 500 → 60 | 0.05 × 440 = 22 |
| M4 Tested restore with five-minute recovery points | containment | R4: `I` 1,000 → 100 | 0.02 × 900 = 18 |

Rank by expected saving, the MMO309 ledger habit, and you buy M1 and M2. The expected loss falls from 115 to 62.5. That looks like the best plan, and by that measure it is.

Now compute the disaster chance for every pair. This code lists all 16 combinations for each plan.

```python
from itertools import combinations, product

# Loss in thousands of player-hours (k ph). Invented teaching values.
RISKS = {"queues": (0.80, 50), "auth": (0.40, 75), "dupe": (0.05, 500), "data loss": (0.02, 1000)}
FIXES = {"M1": ("queues", (0.20, 50)), "M2": ("auth", (0.10, 75)),
         "M3": ("dupe", (0.05, 60)), "M4": ("data loss", (0.02, 100))}
DISASTER = 300

def summary(risks):
    """Expected loss and P(loss > DISASTER), by listing every combination of risks firing."""
    mean = tail = 0.0
    for fired in product((0, 1), repeat=len(risks)):
        prob, loss = 1.0, 0
        for f, (p, impact) in zip(fired, risks.values()):
            prob *= p if f else 1 - p
            loss += impact * f
        mean += prob * loss
        tail += prob if loss > DISASTER else 0
    return mean, tail

print("plan      E[loss]  P(>300)  cost at B=100  cost at B=1000")
for plan in [()] + list(combinations(FIXES, 2)):
    risks = dict(RISKS)
    for m in plan:
        name, new = FIXES[m]
        risks[name] = new
    mean, tail = summary(risks)
    label = "+".join(plan) or "none"
    print(f"{label:9} {mean:7.1f}  {tail:7.3f}  {mean + 100 * tail:13.1f}  {mean + 1000 * tail:14.1f}")
```

It prints:

```
plan      E[loss]  P(>300)  cost at B=100  cost at B=1000
none        115.0    0.069          121.9           184.0
M1+M2        62.5    0.069           69.4           131.5
M1+M3        63.0    0.020           65.0            83.0
M1+M4        67.0    0.050           72.0           117.0
M2+M3        70.5    0.020           72.5            90.5
M2+M4        74.5    0.050           79.5           124.5
M3+M4        75.0    0.000           75.0            75.0
```

Read the first two rows together. The plan the expected-loss ranking chose, M1 and M2, cuts the average by more than half and leaves the disaster chance at exactly 6.9%. It fixed the two risks that could never cause a disaster on their own. Read the last row. M3 and M4 give the worst average of any pair, 75, and a disaster chance of zero. With both, the worst possible week is `50 + 75 + 60 + 100 = 285`, under the line.

Check one middle row by hand. With M1 and M3, only R4 can still cross 300 (R3 now costs 60). So `P(L > 300) = 0.02`. The expected loss is `0.2 × 50 + 0.4 × 75 + 0.05 × 60 + 0.02 × 1,000 = 10 + 30 + 3 + 20 = 63`.

### Pricing the disaster

The last two columns add a **disaster penalty** `B`, the extra cost of a disaster week beyond its direct loss. It stands for the players who leave for good, the refunds and the months of "is it fixed yet?" in every review. The cost of a plan is then

```
cost = E[L] + B × P(L > D)
```

Two plans swap places when their costs are equal. M1+M3 overtakes M1+M2 when `62.5 + 0.069B = 63 + 0.020B`, so at `B ≈ 10`. M3+M4 overtakes M1+M3 when `63 + 0.020B = 75`, so at `B = 600`.

| Your rule | Plan you buy |
|---|---|
| Expected loss only (`B` below 10) | M1+M2 |
| A disaster costs 10 to 600 k ph extra | M1+M3 |
| A disaster costs more than 600 k ph extra, or is not allowed at all | M3+M4 |

Almost any honest penalty moves you off M1+M2. A disaster only has to cost ten thousand player-hours beyond its direct loss, a rounding error for a real launch. Whether you go all the way to M3+M4 depends on how bad a disaster is for your game. That is a business judgment about your players and your studio, and the plan should say which rule you used and why.

### Move it yourself

Open the interactive. The left view is the risk register as the MMO309 ledger shows it: one bar per risk, sorted by `p × I`, with the chosen mitigations shaded where they cut the bar. With M1 and M2 ticked, the two biggest bars shrink and the total drops from 115 to 62.5. It looks like the job is done. The right view is the **exceedance curve**, the chance that the week's loss is above `x`, for every `x`. The disaster line sits at 300. Tick M1 and M2 and the curve drops everywhere left of 125, then crosses the line at exactly the same height as before, 6.9%. Untick them, tick M3 and M4, and the right-hand part of the curve falls to zero while the left-hand bars barely move. Then drag the disaster line down to 100. Now R1 and R2 together cross it, and the prevention fixes start to matter for the tail too.

### Cross-game recognition

Every containment fix in a real launch is a decision to cut the right-hand end of the curve, usually at the cost of the average.

**Pokémon GO (July 2016).** Pausing the rollout to other countries is containment. It does not lower the chance that the service fails. It caps how many players are exposed while it does, so a bad week in three countries does not become a bad week in thirty. The pause cost Niantic players it could have had, which raised the expected loss, and it bounded the worst case.

**New World (November 2021).** When a coin duplication exploit spread, Amazon turned off every form of wealth transfer between players (the trading post, trades, coin transfers and guild treasuries) while it built a fix. MMO308 week 13 analyses that decision as an incident response, and [week 6 of this course](w06-case-duplication-exploits-after-launch-new-world-2021.md) studies the dupes. In this week's terms, the switch was M3. It turned an impact that grows every hour an exploit runs into a fixed cost of one night without trading. The switch had to exist before the exploit did.

**Old School RuneScape (1 October 2024).** A glitch let players duplicate potions through the potion storage interface. Jagex restricted the Grand Exchange, shops and ground items, rolled the game back to a point before the shutdown timer, and brought servers back at 13:00 UTC after testing a fix. That is M4, a rollback you can run in hours because the recovery point exists and the restore has been done before. DB201 week 14 shows how to size those recovery points.

**Outside games: aircraft certification.** The US Federal Aviation Administration's guidance for airliner systems (Advisory Circular 25.1309-1A, 1988) says each failure condition should have a probability inversely related to its severity. Minor failures may be probable. Catastrophic ones must be extremely improbable, defined as not expected to happen in the whole service life of every aircraft of the type. That is a hard limit on the tail. No saving in the average buys you out of it. Engineers do not average a catastrophic failure against a thousand smooth flights.

Four settings, one idea. Prevention moves the average. Containment moves the tail. A plan needs to know which of the two it is buying.

### Eyes-open design judgment

- **Set the disaster line before you look at the fixes.** If you choose `D` after you see which plan is cheapest, you will choose the `D` that agrees with you. Agree it with the producer in the first meeting, in writing.
- **Containment is usually the cheaper tail cut.** You rarely know `p` for a rare risk well (week 3 showed a beta cannot measure it). You often know `I` well, because you design it. A kill switch, a rollback, a trade delay or a regional pause bounds `I` whatever `p` turns out to be. That is why the prevention fixes in this example had to guess `p` and the containment fixes did not.
- **Do not throw away the average.** A plan that ignores R1 accepts long queues in four launches out of five. Players remember those too. The rule is not "always buy containment". It is "know which number each fix moves, and choose with a stated rule".
- **The register is only as good as its list.** A risk you never wrote down has `p × I = 0` in every column. Pokémon GO's worst case was a real number, and the week lived beyond it. The premortem is the defence, and the next section's correlated risks are the second.

### Check this example

1. With no mitigations, what is the chance of a week with no risks firing at all? What is the chance that the loss is above 100 k ph?
2. The budget grows to three fixes. Which three give zero disaster chance, and which of those has the lowest expected loss?
3. The team finds that M3 only cuts R3's impact from 500 to 350. Recompute the disaster chance and expected loss for M3+M4.

<details>
<summary>Answers</summary>

1. No risk fires: `0.2 × 0.6 × 0.95 × 0.98 = 0.1117`. Loss above 100 needs R1 and R2 together (125), or R3, or R4. `P(not above 100) = (1 − 0.8 × 0.4) × 0.95 × 0.98 = 0.68 × 0.931 = 0.633`, so `P(L > 100) ≈ 0.367`.
2. Any set containing M3 and M4 keeps the worst week at or below 285. Add M1 or M2. M1+M3+M4 has `E = 10 + 30 + 3 + 2 = 45`. M2+M3+M4 has `E = 40 + 7.5 + 3 + 2 = 52.5`. Buy M1+M3+M4.
3. R3 now costs 350 and crosses the line on its own. `P(L > 300) = 0.05`, and `E = 40 + 30 + 0.05 × 350 + 0.02 × 100 = 89.5`. A containment fix that does not get the impact under the line buys very little tail.

</details>

## 3. When risks move together

The model above treats the four risks as independent. At a launch they often are not. Pokémon GO's traffic did not cause one problem. It caused crashes, login errors and slow responses at once, because one cause sat behind all of them. When one hidden cause can fire several risks together, the independent model understates the chance that several fire in the same week.

You handle this with a **scenario row**. Instead of guessing how R1 and R2 are correlated, add a named cause with its own probability and write down what each risk does under it. For example, "demand is three times the forecast" might have probability 0.1, and under it R1 and R2 both fire for certain. Outside that scenario, lower their probabilities so the overall rates stay what you believed (for R1, `(0.8 − 0.1) / 0.9 ≈ 0.78`). The expected loss is unchanged. The chance that both fire together rises, and if your disaster line sits where that pair crosses it, so does your disaster chance. Lab 13 asks you to measure how much.

Scenario rows also give your premortem somewhere to put its best answers. "Everyone came at once", "a streamer found the exploit on day 2" and "the patch that fixed the queue broke the saves" are causes, not risks. Each one fires several rows of your register.

## 4. Triggers: deciding in advance

A mitigation you bought is only useful if someone turns it on at the right time. Week 1 gave the war room go/no-go criteria for the unlock. A launch plan extends the same idea to the whole first week with **contingency triggers**, rules written before launch in a fixed form:

| Part | Meaning | Example |
|---|---|---|
| Signal | A number the war room can see on a dashboard | Queue length per world |
| Threshold | The value that fires the trigger | Above 2,000 per world and still growing |
| Action | What happens, in one line | Open launch layers on every full world |
| Owner | One named role who acts without a meeting | Operations lead |
| Lead time | Minutes from decision to effect | 20 minutes |
| Stand-down | When to reverse it | Queue below 200 for 2 hours |

The lead time is the part teams forget. A trigger helps only if it fires early enough for its action to land before the harm it prevents. In symbols, if the signal crosses the threshold at time `t_s`, the action takes `T` minutes, and the harm starts at `t_h`, you need

```
t_s + T ≤ t_h
```

Use week 2's 10-world launch. The queue passes 2,000 per world at about minute 53 and keeps growing until hour 3. A layering trigger at that threshold with a 20-minute lead time lands at minute 73, early enough to cut the shoulder that builds the hour-3 queue. A trigger that adds whole new worlds, with a lead time of a day, lands after the night is over. It is still worth having, but for day 2, and the plan should say so.

Three habits keep triggers honest.

- **One trigger, one owner.** A trigger that says "the team decides" is a meeting, not a trigger. Name the role (MMO308 week 13 gives the roles).
- **Write the stand-down.** Layers, trade switches and sales pauses all cost something while they run. A trigger without a stand-down rule stays on until someone remembers.
- **Rehearse the containment triggers.** A kill switch that has never been flipped in a test is a guess. The restore behind M4 is only worth its 100 k ph if DB201 week 14's drill has actually been run.

## In-class activity (30 minutes)

Work in your launch plan groups.

1. **Premortem (10 minutes).** It is one week after your launch, and the launch is being called a disaster. Each person writes, alone, every reason why. Then go round the group one reason at a time until no one has any left.
2. **Register (10 minutes).** Turn the list into at least six risks and one scenario row. Give each risk a `p` and an `I` in k ph, and write one sentence on where each number comes from (lab 2, lab 3, a case from weeks 4 to 8, or a guess you label as a guess). Agree the disaster line `D` before step 3.
3. **Budget (10 minutes).** You can afford three mitigations from a list you write. Compute, by hand or with the lab code, the expected loss and disaster chance of the plan the expected-loss ranking picks and of the plan with the lowest disaster chance. Write the penalty `B` at which you would switch.

Expected output: a one-page register with `D` stated, the two candidate plans with both numbers, your chosen plan and the rule you used, and two triggers in the table form of section 4. Groups swap pages at the end and each names the one risk they think the other group is missing.

## Common misconceptions

- **"Sort by expected loss and fund from the top."** That ranks fixes by the average they save. It says nothing about the chance of a disaster, and in the worked example it left that chance exactly where it was.
- **"A 2% risk is too unlikely to plan for."** Across the four risks, rare ones supplied the entire 6.9% disaster chance. Many rare risks add up. So do many launches: a studio that ships fifteen games with this register should expect about one disaster.
- **"Containment is admitting defeat."** A kill switch or a rollback does not mean you expect the exploit. It means you know you cannot measure its probability, and you would rather bound its cost than bet on it.
- **"We have a worst case, so we are covered."** A worst case is only as wide as your imagination. Pokémon GO's was a factor of ten too narrow. Plans need triggers and containment that work beyond the worst case, not just up to it.

## Check yourself

1. A register has three risks: R1 `p = 0.5`, `I = 100`; R2 `p = 0.1`, `I = 200`; R3 `p = 0.03`, `I = 600`. With `D = 250`, compute `E[L]` and `P(L > 250)`.
2. For the register in question 1, you can buy one fix: cut R1's `p` to 0.1, or cut R3's `I` to 150. Which lowers `E[L]` more? Which lowers `P(L > 250)` more? At what penalty `B` are they equal in cost?
3. A trigger opens emergency servers when authentication errors pass 5% for 10 minutes. The servers take 45 minutes to come online, and the evening peak, when errors will do the most harm, starts 30 minutes after the error rate usually passes 5%. What is wrong with the trigger, and how would you fix it?
4. Your producer sets `D` at 1,200 k ph for the worked example. Which pair of mitigations would you buy now, and why does the choice of `D` matter so much?

<details>
<summary>Answers</summary>

1. `E = 50 + 20 + 18 = 88`. Losses above 250 need R3 (600), or R1 and R2 together (300). `P(not above 250) = (1 − 0.5 × 0.1) × 0.97 = 0.95 × 0.97 = 0.9215`, so `P(L > 250) ≈ 0.0785`.
2. Cutting R1's `p` saves `0.4 × 100 = 40` in expectation (`E = 48`); cutting R3's `I` saves `0.03 × 450 = 13.5` (`E = 74.5`). For the tail, fixing R1 leaves two ways to cross 250: R3 alone, or R1 with R2. `P = 1 − (1 − 0.1 × 0.1) × 0.97 = 1 − 0.99 × 0.97 ≈ 0.040`. Fixing R3 at 150 leaves R1 with R2 (300) and R2 with R3 (350) crossing, while R1 with R3 is exactly 250 and does not. Both need R2, so `P = 0.1 × (1 − 0.5 × 0.97) = 0.1 × 0.515 ≈ 0.052`. The R1 fix wins on both numbers. Their costs are `48 + 0.040B` and `74.5 + 0.052B`, so the R1 fix is cheaper at every `B` and they never tie. Prevention cuts the tail when the prevented risk sits inside the combinations that cross the line.
3. The lead time (45 minutes) is longer than the gap to the harm (30 minutes), so `t_s + T > t_h` and the servers arrive after the peak has started. Lower the threshold (for example, 2% errors for 5 minutes), or pre-warm the servers so the action takes minutes, or schedule them before the peak regardless of the signal.
4. With `D = 1,200`, only R4 together with R3 crosses the line (1,500). R4 with R1 and R2 is 1,125, still under it. So the disaster chance with no fixes is `0.02 × 0.05 = 0.001`, and M1+M2 is now the sensible pair, because the tail is already tiny and M1+M2 has the lowest expected loss. The line decides which risks count as disaster risks, so moving it changes the answer. That is why it must be agreed before the plan is costed.

</details>

## Lab / assignment hook

[Lab 13, launch risk register](../labs/lab13.md). You implement the exact loss distribution, the exceedance curve and a budgeted mitigation chooser with three rules, reproduce this lecture's table, add scenario rows for correlated risks, and apply it to your own group's register. The output is sections 4 to 6 of your final launch plan, which you present in [week 14](w14-presentations.md).

## Sources

- Stone, L. (29 September 2016), "Bringing Pokémon GO to life on Google Cloud", Google Cloud blog. Launch traffic reached 50 times Niantic's target, ten times the worst-case estimate of about five times the target; the target was passed within 15 minutes of the Australia and New Zealand launch.
- Wikipedia, "Pokémon Go" (read September 2026). Release on 6 July 2016 in Australia, New Zealand and the United States; crashes and authentication errors for several days; John Hanke's pause of releases in other regions.
- Klein, G. (2007), "Performing a Project Premortem", *Harvard Business Review* 85(9), 18-19. The premortem method: assume the project has failed and ask what did go wrong.
- Wikipedia, "Pre-mortem" (read September 2026). The premortem as a formalization of prospective hindsight (Mitchell, Russo and Pennington, 1989).
- NWDB, "All Forms of Trading Disabled Due to Coin Duplication Exploits", 2 November 2021, reporting Amazon Games' statement for New World. Trading post, player trading, coin transfers and guild treasury disabled while a fix was prepared.
- Old School RuneScape Wiki, "Potion storage glitch" (read September 2026). 1 October 2024; restrictions on the Grand Exchange, shops and ground items during the shutdown timer; rollback to before the timer; servers back at 13:00 UTC after a fix was tested.
- US Federal Aviation Administration, Advisory Circular 25.1309-1A, "System Design and Analysis", 21 June 1988. Probability inversely related to severity; minor failure conditions may be probable, catastrophic ones must be extremely improbable (not anticipated in the entire operational life of all airplanes of one type).
- MMO309 week 1, MMO308 week 13 and DB201 week 14 (this program) for expected annual loss, incident response and restore drills, with their sources.
- All risk probabilities, impacts, mitigation effects, the disaster line and penalties in sections 2 to 4 and the activity are invented teaching values.

## Interactive spec: examples/w13-risk-register-tail.html

**The one insight:** fixes ranked by expected saving can cut the average loss in half and leave the chance of a disaster week exactly where it was. Prevention moves the average; containment moves the tail. The ledger view looks solved while the exceedance curve still crosses the disaster line at the same height.

**Layout (two linked views, stacked on mobile, side by side at 900px and wider):**

- View A, "the ledger": horizontal bars, one per risk, length `p × I`, sorted longest first, labelled with `p`, `I` and `p × I`. When a mitigation is ticked, draw the original bar as an outline and the new bar solid, so the cut is visible. A total bar below: `E[L]` before and after. Colour risks by kind of fix available: prevention in `--steel`, containment in `--moss`.
- View B, "the tail": an exceedance curve, x = loss in k ph from 0 to 1,700 (log-free, linear), y = `P(L > x)` from 0 to 1 as a step function. Draw the no-mitigation curve as a faint dashed line and the current plan's curve solid. A vertical line at the disaster threshold `D` in `--blood`, with the crossing height labelled "P(disaster) = 6.9%". Mark the maximum possible loss of the current plan with a small tick.
- Below both, a plan table listing all six pairs of mitigations (and "none") with `E[L]`, `P(L > D)` and `E[L] + B × P(L > D)`. Highlight the row with the lowest cost at the current `B`.

**Controls:**

- Four mitigation checkboxes M1 to M4 (default M1 and M2 ticked). A "budget" readout shows how many are ticked; more than 2 is allowed but flagged "over budget".
- Disaster line `D`, 50 to 1,500 k ph, step 25 (default 300).
- Penalty `B`, 0 to 2,000 k ph, step 10 (default 100).
- For each risk: `p` slider (0 to 1, step 0.01) and `I` slider (0 to 1,500, step 5), in a collapsible "edit register" panel. Defaults from the lecture.
- Scenario toggle "demand three times forecast": probability `s` slider 0 to 0.3 (default 0.1). When on, R1 and R2 fire for certain inside the scenario; outside it their probabilities become `(p − s) / (1 − s)` (clamped at 0), so marginals stay the same.
- Preset buttons: "expected-loss pick" (M1+M2), "lowest cost at B" (computed), "no disaster" (M3+M4).

**Readout (always visible, `aria-live="polite"`):** `E[L]`, `P(L > D)`, worst possible week, cost at `B`, and the two break-even penalties between the cheapest three plans.

**Formulas:**

```
risks i = 1..4 with (pᵢ, Iᵢ); mitigation replaces (pᵢ, Iᵢ) for its risk
M1: R1 p → 0.20      M2: R2 p → 0.10      M3: R3 I → 60      M4: R4 I → 100
for each of the 2^4 outcomes f ∈ {0,1}^4:
    prob(f) = Π (fᵢ ? pᵢ : 1 − pᵢ);  loss(f) = Σ fᵢ Iᵢ
E[L] = Σ prob(f) loss(f)
P(L > x) = Σ over f with loss(f) > x of prob(f)
cost = E[L] + B × P(L > D)
scenario on: with prob s, R1 and R2 fire (R3, R4 unchanged); with prob 1 − s use p₁' = (p₁ − s)/(1 − s), p₂' = (p₂ − s)/(1 − s); mix the two outcome sets
```

**Test values (must match, defaults unless stated):**

- No mitigations: `E = 115.0`, `P(L > 300) = 0.069`, worst week 1,625.
- M1+M2: `E = 62.5`, `P = 0.069`. M1+M3: 63.0, 0.020. M1+M4: 67.0, 0.050. M2+M3: 70.5, 0.020. M2+M4: 74.5, 0.050. M3+M4: 75.0, 0.000, worst week 285.
- Cost at `B = 100`: none 121.9, M1+M2 69.4, M1+M3 65.0 (lowest), M3+M4 75.0. At `B = 1,000`: M3+M4 75.0 (lowest), M1+M3 83.0.
- Break-even penalties: M1+M2 vs M1+M3 at `B ≈ 10.2`; M1+M3 vs M3+M4 at `B = 600`.
- No mitigations, `P(L > 100) ≈ 0.367`; probability no risk fires `0.1117`.
- `D = 1,200`, no mitigations: `P(L > D) = 0.001`.
- Scenario on with `s = 0.1`, no mitigations: `E` still 115.0; `P(R1 and R2 both fire) = 0.1 + 0.9 × (0.7/0.9) × (0.3/0.9) ≈ 0.333` (independent: 0.320). With `D = 100`, `P(L > 100)` rises from 0.367 to about 0.379.

**First screen:** defaults with M1 and M2 ticked. Caption: "The ledger says you halved the loss. The tail says the disaster chance did not move: 6.9%. Try M3 and M4."

**Accessibility:** all controls keyboard operable with visible focus; checkboxes and sliders labelled; readout in `aria-live="polite"`; the exceedance curve has a text table alternative behind a "show numbers" toggle; respects `prefers-reduced-motion` and `prefers-color-scheme`; tokens from `templates/interactive-tokens.css` inline. Generic shapes only, no game art or logos.

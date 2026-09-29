# MMO309 · Week 13 — Bug Bounties and Disclosure

**Why this matters:** Every live MMO ships with exploits nobody on the team has found yet. Players will find them. Whether a finder files a ticket, sells the method, farms it quietly or posts a video depends on rules and prices that you set long before the bug exists. This week turns "should we run a bug bounty?" into a calculation you can defend in a budget meeting.

**You will be able to:**
- Compute the bounty a rational finder needs before reporting beats exploiting, from five measurable inputs.
- Explain why faster detection makes bounties cheaper, and put a number on how much cheaper.
- Compare full, coordinated and private disclosure for gameplay exploits and security vulnerabilities, and choose a disclosure window for each.
- Draft a vulnerability disclosure policy for an MMO with scope, safe harbor, severity tiers and payouts.

**Before class:** Hoglund, G. & McGraw, G. (2007), *Exploiting Online Games*, chapter 5 ("Infested with Bugs") and chapter 10 ("Software Security Über Alles"). Read the Old School RuneScape Wiki page "Server crash glitch" (10 minutes) and Google Project Zero's published disclosure policy (10 minutes).

**Prerequisites from earlier courses:** [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md) (the finder's choice is an expected-value comparison). [MA102 week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md) (why an exploit with daily patch chance `h` lives `1/h` days on average). [MMO304 week 11, real-money trade](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w11-real-money-trade-and-gold-farming.md) (where exploited gold is sold). In year 4, [MMO401 week 12, economic shocks, exploits and rollbacks](../../MMO401-virtual-economies-ii-markets-governance-and-macr/lectures/w12-economic-shocks-exploits-and-rollbacks.md) prices a dupe's hourly cost, and [MMO402 week 5, rules, EULAs and terms of service](../../MMO402-emergent-society-governance-and-ethics/lectures/w05-rules-eulas-and-terms-of-service.md) covers the contract side. In this course, [week 1, threat modeling for games](w01-threat-modeling-for-games.md), [week 4, duplication exploits and transactional design](w04-duplication-exploits-and-transactional-design.md), [week 11, exploit response, rollback versus ban](w11-exploit-response-rollback-vs-ban.md), and [week 6, botting economics](w06-botting-economics.md).

**Interactive:** [examples/w13-bounty-vs-black-market.html](../examples/w13-bounty-vs-black-market.html). Keep it open during section 2.

---

## 1. Who finds your bugs, and what they do next

Your QA team plays the game for a few thousand hours before launch. Your players log millions of hours in the first week. Most exploits are found by players, and the valuable ones by players who hunt for them.

Once someone finds a bug, they have roughly four choices:

1. **Report it privately** to the studio and wait for a fix.
2. **Use it quietly**, for in-game advantage or for gold they sell for real money.
3. **Sell or share it** with a group that will use it at scale.
4. **Publish it**, in a video, forum post or stream, often to force the studio's hand or for attention.

A disclosure program is the set of rules and rewards that tries to make choice 1 the best one for the finder. It has three parts:

- A **vulnerability disclosure policy** (VDP). A public page that says what to report, how, what the studio promises in return, and what the studio will not do (for example, sue or ban a finder who follows the rules). The legal promise is called **safe harbor**.
- A **bug bounty**. Money paid for valid reports, usually on a severity scale. The first widely known program was Netscape's, for the Navigator 2.0 beta in 1995. Platforms such as HackerOne and Bugcrowd now run triage and payment for many companies.
- A **disclosure timeline**. When, if ever, the details become public.

### Two kinds of bug, two kinds of program

Games have a split that most software does not. Keep these apart from the first minute.

A **security vulnerability** lets someone break the confidentiality, integrity or availability of a system outside the game's rules. Examples are account takeover, payment tampering, remote code execution on a player's machine through the chat client, and leaking other players' personal data. These look like ordinary software bugs and the standard security industry practice applies.

A **gameplay exploit** lets someone gain an advantage inside the game's rules as implemented, but against the rules as designed. Duplication ("dupes"), invulnerability, walking through walls, and a quest that pays out twice are all gameplay exploits. The damage is to the economy and to fairness, not to anyone's computer.

Many studios run a paid bounty for the first kind and a report-it-or-be-banned rule for the second. Riot Games' Vanguard program pays up to US$100,000 for vulnerabilities in the anti-cheat driver and states that gameplay bugs do not qualify. Old School RuneScape's rules make "exploiting a bug" a bannable offense and tell players to report bugs to Jagex immediately. You will see in section 2 that these two policies are the same model with different numbers plugged in.

Why the split? Three reasons, each a number you can estimate:

- **Volume.** A live MMO may get hundreds of gameplay bug reports a week. Paying for each would swamp the budget and the triage team.
- **Outside value.** An anti-cheat driver bug sells to cheat makers and malware authors. A clipping bug sells to nobody. The bounty only has to beat the outside option.
- **Blast radius.** A security bug can hurt people outside the game, through stolen payment details or a compromised PC.

## 2. Worked example: outbidding the black market for a gold dupe

### The hook

In August 2021 a researcher reported to Valve, through HackerOne, a way to add money to a Steam wallet without paying for it, by tampering with data sent to one of Steam's payment providers. Valve paid US$7,500. The report was filed on 9 August and publicly disclosed on 10 August, after the fix.

Think about what the finder gave up. Unlimited Steam wallet funds could buy games, and Steam Community Market items that sell for real money. Why would anyone take $7,500 instead?

Part of the answer is ethics, and many finders are honest. But you cannot design a program around the assumption that every finder is honest. You design it so that an honest finder is well paid and a merely rational one reaches the same decision. That requires a model of the finder's alternatives.

### The model

A finder holds a working gold duplication exploit in your MMO. Define:

- `v`, the real-money value per day the finder can extract by using the exploit quietly (duping gold and selling it through real-money trade). In dollars per day.
- `h`, the daily probability that your team detects and patches the exploit on its own. This is a **hazard rate**. From MA102 week 7, if each day independently has chance `h` of ending the exploit, the expected number of days it lives is `1/h`.
- `q`, the probability that, once you detect it, you also identify this finder and act against them (ban, clawback).
- `L`, what the finder loses if identified. The account's value, items, time invested, and any legal risk, in dollars.
- `a`, the probability a report is accepted and paid. Below 1 because of duplicate reports (someone else reported it first), scope disputes and slow triage.
- `B`, the bounty.

The finder's expected value from each choice:

```
exploit:  E_x = v / h − q × L
report:   E_r = a × B
```

A rational finder reports when `E_r ≥ E_x`. The smallest bounty that achieves this is

```
B* = max(0, (v / h − q × L) / a)
```

Now the studio's side. Let `d` be the harm per day the exploit runs (inflation, support tickets, players quitting, cleanup labor) and `R` a one-time incident cost when you finally discover it (rollback, clawback investigation, communication). The expected cost of an exploit that is used until detected is

```
C_x = d / h + R
```

If the finder reports instead, you pay `B` and fix the bug. You pay the fix cost in both cases, so it drops out. The program pays for itself whenever `B* < C_x`.

One symbol does most of the work. Both `B*` and `C_x` have `1/h` in them. Detection speed sets the price of honesty.

### Numbers you can check

Take a mid-sized MMO. The finder can sell $150 of duped gold per day (`v = 150`). You catch 60% of exploiters when you detect a dupe (`q = 0.6`), and the finder's account is worth $300 to them (`L = 300`). Four out of five reports are accepted and paid (`a = 0.8`). On the studio side, each day the dupe runs costs $4,000 in harm (`d = 4,000`), and the incident costs $20,000 to clean up (`R = 20,000`).

With a daily detection chance of 10%, the exploit lives 10 days on average. Work it through by hand:

```
E_x = 150 / 0.10 − 0.6 × 300 = 1,500 − 180 = 1,320
B*  = 1,320 / 0.8 = 1,650
C_x = 4,000 / 0.10 + 20,000 = 60,000
```

A $1,650 bounty saves an expected $60,000. Now vary `h`. This block runs as shown with `.venv/bin/python`.

```python
def exploit_value(v, h, q, L):
    """Expected dollars from quietly using the exploit until it is patched."""
    return v / h - q * L

def bounty_needed(v, h, q, L, a):
    """Smallest bounty that makes reporting worth at least as much as exploiting."""
    return max(0.0, exploit_value(v, h, q, L) / a)

def studio_cost(d, h, R):
    """Expected cost to the studio if the exploit is used until detection."""
    return d / h + R

v, q, L, a = 150, 0.6, 300, 0.8   # finder: $/day, P(caught), loss if caught, P(report accepted)
d, R = 4000, 20000                # studio: harm $/day, incident cost at discovery

print(f"{'h':>5} {'days':>5} {'exploit EV':>11} {'bounty B*':>10} {'studio cost':>12}")
for h in [0.02, 0.05, 0.10, 0.25, 0.50]:
    print(f"{h:>5.2f} {1/h:>5.0f} {exploit_value(v, h, q, L):>11,.0f} "
          f"{bounty_needed(v, h, q, L, a):>10,.0f} {studio_cost(d, h, R):>12,.0f}")
```

Output:

```
    h  days  exploit EV  bounty B*  studio cost
 0.02    50       7,320      9,150      220,000
 0.05    20       2,820      3,525      100,000
 0.10    10       1,320      1,650       60,000
 0.25     4         420        525       36,000
 0.50     2         120        150       28,000
```

Read down the bounty column. When your team takes 50 days on average to notice a dupe, you need $9,150 to win the finder. When you notice in 2 days, $150 does it. The bounty needed scales with `1/h`, so every time you halve detection time you roughly halve the bounty you need (the `q × L` term makes it a little better than half).

Read across any row. `B* / C_x` runs from 4.2% at 50 days down to 0.5% at 2 days. That ratio holds for a bounty set to each row's own `B*`. One fixed bounty sized for 50-day detection, $9,150, is a third of the $28,000 harm at `h = 0.5`. Still a bargain, but fast detection lets you pay far less.

### The visual: two views of the same `1/h`

Open the interactive. The left panel plots the bounty needed `B*` against mean detection time `1/h`, with a horizontal line at your current bounty. Where the curve sits above your line, a rational finder exploits. The right panel plots the studio's expected cost `C_x` on the same horizontal axis, with the bounty drawn in for scale.

Drag the detection slider from 50 days to 2 days. The left curve falls toward zero and crosses under your bounty line. The right panel's cost falls too, but it stays far above the bounty at every setting. The two panels together make the lecture's claim visible. **Detection and bounties are complements, not substitutes.** Money spent on detection lowers the price of every future bounty, and a bounty converts some exploits you would have detected late into reports you receive on day one.

Then drag `q` (the chance you catch the exploiter). Watch the left curve drop by a constant amount. The penalty term `q × L` shifts the whole curve down, but it cannot beat `v / h` when detection is slow. A $300 account at risk does nothing against a 50-day exploit worth $7,500.

### Cross-game recognition

The same model explains policies that look unrelated. Rewrite each one as a choice of `B`, `q`, `L` and `h`.

**Valve on HackerOne (2018 and 2021).** Valve paid $7,500 for a persistent cross-site scripting bug in the Steam chat client (reported September 2018, disclosed January 2019) and $7,500 for the 2021 wallet-funding bug. The wallet bug's outside value `v / h` looks enormous, but consider `q`. Every fraudulent top-up passes through a payment provider and lands in a named Steam account. Once Valve reconciles payments, `q` is close to 1 and `L` includes criminal fraud exposure. The finder's real exploit value was far smaller than "unlimited money," which is why a four-figure bounty works.

**Riot Vanguard (current program, figures as of May 2026).** Up to $100,000 for anti-cheat driver vulnerabilities, gameplay bugs excluded. A kernel-level driver runs with the highest privileges on the player's PC. A vulnerability there has a large `v` for cheat makers (it can hide cheats from the anti-cheat itself) and for malware authors, and `q` is low because using it quietly leaves few traces the studio can see. The model says `B*` must be large, and it is.

**Old School RuneScape (rules as documented in 2024 to 2026).** The Code of Conduct makes bug abuse a bannable offense and asks players to report bugs immediately, and major abuse may bring a permanent ban. In model terms the rule sets `B` near zero for most gameplay bugs and relies on `q × L`. A long-lived OSRS account with years of progress can be worth a great deal to its owner, and Jagex's economy monitoring keeps `h` high. For low-value exploits this works. For a high-value dupe, the model predicts some finders will not report, and in November 2019 one did not (section 4).

**Ultima Online beta (1997).** During the beta a tester killed Lord British, the supposedly invincible avatar of the game's creator, after an oversight around a server crash. The tester was banned, and the reason usually given was not the kill but that he had not reported the bugs he found. That is the same lever as OSRS, `q × L` with `B = 0`, applied in a test where reporting was the tester's job.

Four programs, one inequality, `a × B ≥ v / h − q × L`. For any new policy, ask which term it pulls on.

### Design judgment, eyes open

The model is a floor for your bounty, not a price list. Things it leaves out, and what you should decide deliberately:

- **Most finders are not purely rational.** Many report for free out of goodwill, reputation or curiosity. The model sets the price for the finder you need most, the one who could sell the exploit. Underpaying the honest majority teaches them that the studio does not value their time.
- **`v` is not yours to observe.** You estimate it from real-money trade prices and the exploit's rate. Estimate it high. Underestimating `v` is the error that sends a dupe to a gold seller.
- **Raising `L` has side effects.** Bigger penalties (lifetime bans, lawsuits) make honest finders afraid to report anything that required them to use the bug even once. This is why safe harbor exists. A policy that says "report within 24 hours of discovery and do not use it beyond what you need to show it works, and we will not ban you" keeps `L` high for abusers and near zero for reporters.
- **`a` is the cheapest lever.** Fast triage, a clear duplicate rule, and paying partial bounties for duplicates filed within a short window all raise `a`. A program where a third of valid reports are rejected as "duplicates" without explanation needs a 50% higher headline bounty to compete.
- **Detection is still the main defense.** Every row of the table says so. A studio with slow economy monitoring cannot buy its way to safety with bounties alone, because the bounty it would need grows with `1/h`.

## 3. Disclosure: who learns what, and when

After a report arrives, the next question is who else finds out. The security field uses three broad models.

**Full disclosure.** The finder publishes everything immediately. The argument for it is that vendors fix faster under public pressure. The cost is that attackers learn the details at the same moment as defenders.

**Coordinated disclosure** (older name, "responsible disclosure"). The finder tells the vendor privately and the details become public after a fix or a deadline, whichever comes first. Google Project Zero uses a 90-day deadline from notification. Trend Micro's Zero Day Initiative uses 120 days from the vendor's response. Two ISO standards describe the vendor side: ISO/IEC 29147 for receiving reports and publishing advisories, and ISO/IEC 30111 for handling them internally.

**Private or non-disclosure.** The details are never published. Some bounty programs require this as a condition of payment.

### Why games need a different clock

A 90-day deadline assumes two things that often fail in an MMO:

1. **A fix takes weeks.** For a gameplay exploit that lives on the server, a hotfix can take hours. There is no reason to hold details for 90 days.
2. **Publication mostly helps defenders.** For a gold dupe, publication mostly helps attackers. The number that matters is how many players start exploiting per hour after a video goes up, and for a dupe that pays in tradable gold the answer is "thousands."

Put the second point in the section 2 model. Publication multiplies the number of exploiters, so the daily harm `d` jumps by orders of magnitude, while `h` stays where it was until your team reacts. The expected cost `d / h + R` explodes. This is why, for gameplay exploits, the right window is usually **no public detail until the fix is live on every server**, and often no technical detail even then. What you publish instead is the effect: "we fixed an issue that allowed items to be duplicated, removed the duplicated items, and actioned the accounts involved."

For security vulnerabilities in the client, launcher, anti-cheat or web services, the standard coordinated window applies. Your players' PCs need patches, their security teams need to know what to look for, and the public advisory is part of the fix.

A practical policy therefore has two tracks:

| | Security vulnerability | Gameplay exploit |
|---|---|---|
| Channel | Security inbox or bounty platform | In-game report or support form, with an "exploit" category |
| Reward | Paid on a severity scale | Usually unpaid, or small rewards for high-severity dupes |
| Safe harbor | Written legal promise | Written promise not to ban for proof-of-concept use |
| Public detail | Advisory after fix, standard deadline | Effect only, after fix is live everywhere |
| Deadline if studio stalls | 90 days is common | Negotiate; public detail rarely helps players |

## 4. A disclosure that went public: the OSRS server crash glitch

On 26 November 2019 an Old School RuneScape content creator disclosed a way to duplicate coins and items. Here is the mechanism at the level a defender needs. When a game world crashed, each player's state reverted to their last save, which could be up to 15 minutes old or their last logout. A trade between two players was therefore not saved as one unit. If one side logged out after the trade and the world then crashed, one account kept the traded items while the other reverted to before the trade and got them back. The crash itself was forced by overloading a world.

In week 4 you studied this class of bug as a failure of transactional design. The trade should succeed or fail as a whole on both accounts. Here the save system let half of it be undone.

What happened next is the part for this week. Jagex's Mod Sween said the team learned of the method very quickly through a combination of tip-offs from the content creator and its own system monitoring. Support and anti-cheating teams removed a large amount of gold and investigated accounts, while engine and system administration teams worked on preventing recurrence. There was no rollback. The creator was not banned at first. In January 2021 Jagex published a notice about new reports of item duplication through server crashes, and on 9 July 2021 it announced bans for bug abuse through deliberate server crashes, including the creator's account.

Read it through the model.

- **Detection `h` was high.** Monitoring plus tip-offs meant days of exploitation, not weeks. That kept `C_x` down and made a rollback unnecessary.
- **Disclosure raised `d`.** A public explanation spread the method to anyone who watched, which is the risk section 3 describes.
- **The penalty `q × L` arrived late.** The ban came some 19 months after the first disclosure. Late enforcement tells future finders that the penalty is uncertain, which lowers the `q` they will use in their own calculation.
- **The root cause was structural.** Saving each account on its own timer creates a whole class of dupes. Fixing that class, not just the crash trigger, is what lowers `v` for the next finder to zero.

The lesson is about the program, not one person. With no clear, paid, fast channel for a high-value exploit, the report-it path was not obviously the finder's best move.

## 5. Designing the program

Here is what a minimum program for a mid-sized MMO contains. Each item maps to a term in the model.

**Scope.** List what is in (game servers, client, launcher, web shop, account system, anti-cheat) and what is out (third-party services, social engineering of staff, denial-of-service testing against live servers). A tight scope keeps `a` high, since finders know in advance whether they will be paid.

**Rules of engagement.** Test on your own accounts. Use an exploit only as far as needed to show it works. Do not transfer the results to other accounts or sell them. Report within a fixed time of discovery (24 or 48 hours is common for gameplay exploits). Offer a public test realm and test accounts for security research, so finders do not need to touch the live economy at all.

**Safe harbor.** A written promise that you will not pursue legal action or bans against good-faith research that follows the rules. Standard wording exists (the disclose.io project publishes templates). Without it, your `L` term scares away the reporters and not the abusers.

**Severity tiers and payouts.** Security bugs are often scored with CVSS (the Common Vulnerability Scoring System), which rates impact and ease of exploitation. For gameplay exploits, build your own table using the section 2 model. Estimate `v` for each class of exploit, set a target `h` from your monitoring, and price each tier at or above `B*`. For example:

| Tier | Example | Rough `v` ($/day) | Payout |
|---|---|---|---|
| Critical, economy | Currency or item duplication | 100 to 1,000 | Model's `B*` at your real `h`, with a floor |
| High, account | Taking over another player's account | Varies | Standard security scale |
| Medium, fairness | Invulnerability, out-of-bounds in PvP | Small real-money value | Fixed small reward or in-game recognition |
| Low | Visual glitches, text errors | 0 | Thanks, credit in patch notes |

**Triage.** Commit to a first response time (for example two business days) and a severity decision time. Pay duplicates filed within a short window a partial bounty. Publish the duplicate rule. All of this raises `a`.

**The double dip.** A finder can exploit for `k` days and then report, collecting both. Suppose your server logs let you detect prior use with probability `p`. If you catch it, you void the bounty and apply the penalty. The double-dipper's expected value is

```
E_dd = v × k + (1 − p) × a × B − p × L
```

With the section 2 numbers (`v = 150`, `a × B = 1,320`, `L = 300`) and `k = 5` days, a studio with no audit (`p = 0`) offers the double-dipper $750 + $1,320 = $2,070, beating an honest report's $1,320. The double dip stops paying when `v × k ≤ p × (a × B + L)`, which here is `p ≥ 750 / 1,620 ≈ 0.46`. Good logs are therefore part of the bounty program. If you cannot tell whether a reporter used the bug, your real bounty is lower than your advertised one, because you are paying abusers too.

**Budget.** At 400 reports a month and 30 minutes of triage each, you spend 200 staff hours a month before paying any bounty. The bounties are cheap next to `C_x`. Triage labor is often the larger line.

## 6. Ethics and law for the finder and the studio

[Week 12](w12-legal-and-ethical-considerations.md) covered the legal background. Two points matter here.

First, **the studio's terms of service usually forbid what a researcher does.** Reverse engineering the client, automated testing and using bugs are banned in most EULAs (MMO402 week 5). A bounty program is a contract that carves out an exception for good-faith research. If your program does not carve it out in writing, you have asked finders to break your own rules to help you.

Second, **the finder has duties too.** A good finder stops when the bug is demonstrated, keeps no gains, stays out of other players' data, reports quickly, and publishes nothing before the fix. A finder who follows these rules and still gets banned has been failed by the program. A finder who dupes a billion coins "to test it" has not followed them.

## In-class activity (25 minutes)

In groups of three, draft a one-page vulnerability disclosure policy for a mid-sized MMO with a player-driven economy and real-money trade.

1. Write the scope list (in and out) and three rules of engagement.
2. Estimate `v` for a currency dupe. Use a real-money trade price of $8 per million gold and a dupe that can produce 20 million gold a day without drawing attention. Your monitoring detects dupes in 5 days on average. Take `q = 0.5`, `L = 200` and `a = 0.9`. Compute `B*`.
3. Set the payout for your "critical, economy" tier. Justify the gap between your payout and `B*`.
4. Decide what you publish after a dupe is fixed, and when.
5. Swap with another group. Find one rule in their policy that would make an honest finder hesitate to report.

Expected output: the one-page policy, the `B*` calculation from step 2, and the weakness your partner group found. (For step 2, `v = 160`, `v / h = 800`, `E_x = 800 − 100 = 700`, `B* ≈ 778`.)

## Common misconceptions

- **"A bug bounty replaces detection."** The bounty you need grows with `1/h`. Without detection, the required bounty is unaffordable for valuable exploits. The two work together.
- **"Harsher bans make everyone report."** Harsh penalties with no safe harbor deter reporters, because most reports require at least one use of the bug. They also do little against slow detection, since `v / h` grows faster than any account's value.
- **"Coordinated disclosure means 90 days for everything."** The 90-day convention was built for software where fixes take weeks and publication helps defenders. For a server-side gameplay exploit, the fix can take hours and publication mainly helps attackers.
- **"If we pay for bugs, people will create bugs to report."** Finders cannot create a bug in your server code. What they can do is report the same bug many times or exploit before reporting. A duplicate rule and log audits handle both.

## Check yourself

1. An exploit yields `v = $400` per day. Your team detects such exploits in 8 days on average. You catch the exploiter 70% of the time, and they lose `L = $500`. Reports are accepted 90% of the time. What is `B*`?
2. For the exploit in question 1, your team invests in monitoring and cuts mean detection time to 4 days. By how much does `B*` fall? Why is the answer a little more than half?
3. A studio says: "We don't need a bounty, our accounts are so valuable nobody would risk them." Using the model, describe the exploit for which this is true and the exploit for which it is false.
4. Your triage team rejects 30% of valid reports as duplicates. Your headline bounty for a dupe is $2,000. What bounty would a rival program with `a = 0.95` need to match your program's expected payout to a finder?
5. A double-dipper can use a bug for 3 days at $200 per day before reporting a bug that pays `a × B = $1,000`. The penalty if caught is $400. What audit probability `p` makes the double dip no better than an honest report?

<details>
<summary>Answers</summary>

1. `v / h = 400 × 8 = 3,200`. `q × L = 0.7 × 500 = 350`. `E_x = 2,850`. `B* = 2,850 / 0.9 ≈ $3,167`.
2. `v / h = 1,600`, `E_x = 1,250`, `B* ≈ $1,389`. It falls by about $1,778, a little more than half of $3,167. The penalty term `q × L` does not shrink when detection speeds up, so it takes a larger share of a smaller `v / h`.
3. The penalty only works when `q × L ≥ v / h`. It is true for low-value or short-lived exploits (small `v`, or high `h`). It is false for a high-value dupe with slow detection. With `v = $500` per day and 30-day detection, `v / h = $15,000`, which exceeds almost any account's value.
4. Your expected payout is `0.7 × 2,000 = $1,400`. The rival needs `1,400 / 0.95 ≈ $1,474`. They can advertise about 26% less and still match you, which is the cost of your duplicate rule.
5. Double dip: `600 + (1 − p) × 1,000 − 400p`. Honest report: `1,000`. Setting them equal gives `600 = 1,400p`, so `p ≈ 0.43`. With audits catching prior use at least 43% of the time, the double dip stops paying.

</details>

## Lab hook

[Lab 13, pricing a bounty table](../labs/lab13.md). You will implement the section 2 model, price a five-tier bounty table from a file of exploit classes, and find the detection time at which your budget covers every tier. Deliverable: the passing script, the table, and a 300-word memo to your producer.

## Sources

- Valve, HackerOne report #1295844, "Modify in-flight data to payment provider Smart2Pay" (filed 9 August 2021, disclosed 10 August 2021, bounty US$7,500). https://hackerone.com/reports/1295844
- Valve, HackerOne report #409850, "XSS in steam react chat client" (filed 14 September 2018, disclosed 7 January 2019, bounty US$7,500). https://hackerone.com/reports/409850
- K. Orland, "Riot addresses 'kernel-level driver' concerns with expanded bug bounties", Ars Technica, 20 April 2020. Bounties of up to US$100,000 for practical exploits of the Vanguard kernel driver. Wikipedia, "Valorant" (accessed September 2026), citing Riot's HackerOne page, gives the same ceiling as of May 2026, gameplay bugs excluded. Wikipedia, "Riot Vanguard" (accessed September 2026). Kernel-level anti-cheat, released with Valorant on 7 April 2020 and added to League of Legends in April 2024.
- Old School RuneScape Wiki, "Server crash glitch" (accessed September 2026), citing Mod Sween on Reddit (27 November 2019) and Jagex news posts "Item Duplication Reports" (11 January 2021) and "A Message Regarding Bug Abuse" (9 July 2021). Disclosure on 26 November 2019, the 15-minute save state, no rollback, detection through tip-offs and monitoring, later bans.
- Old School RuneScape Wiki, "Code of Conduct" and "Glitch" (accessed September 2026). Bug abuse as a rule; the instruction to report bugs immediately; punishment up to a permanent ban for major abuse.
- Wikipedia, "Video game exploit" (accessed September 2026). The Ultima Online beta tester banned for not reporting the bugs used to kill Lord British. Wikipedia, "Lord British" (accessed September 2026). The 1997 beta killing linked to a server crash.
- Wikipedia, "Bug bounty program" (accessed September 2026). Netscape's 1995 program for the Navigator 2.0 beta; HackerOne and Bugcrowd as platforms.
- Wikipedia, "Coordinated vulnerability disclosure" (accessed September 2026). Project Zero's 90-day deadline, the Zero Day Initiative's 120-day deadline, ISO/IEC 29147 and ISO/IEC 30111, safe-harbor language.
- Hoglund, G. & McGraw, G. (2007). *Exploiting Online Games: Cheating Massively Distributed Systems*. Addison-Wesley. Chapter titles as listed by Open Library.

## Interactive spec: examples/w13-bounty-vs-black-market.html

**Purpose.** Make visible that the bounty needed to win a rational finder scales with mean detection time `1/h`, and that the studio's expected cost scales the same way but is far larger, so detection and bounties are complements.

**Layout.** Two linked panels side by side on desktop, stacked on mobile.

- Left panel, "What the finder needs." X axis: mean detection time `1/h` in days, 1 to 60 (log scale is not needed; use linear). Y axis: dollars. Plot `B*(1/h) = max(0, (v × (1/h) − q × L) / a)` as a line. Draw a horizontal line at the current bounty `B`. Shade the region where `B* > B` in a warning color with the label "finder exploits" and the region below in a calm color with "finder reports". Mark the current detection time with a vertical line and a dot on the curve.
- Right panel, "What the studio loses." Same X axis. Plot `C_x = d × (1/h) + R`. Draw the current bounty `B` as a thin horizontal line for scale. Mark the current detection time with a dot. Show the ratio `B / C_x` as a percentage next to the dot.

**Controls** (sliders with numeric readouts, keyboard accessible):
- Mean detection time `1/h`: 1 to 60 days, step 1, default 10.
- `v`, finder's value per day: $0 to $1,000, step 10, default 150.
- `q`, chance you catch the exploiter: 0 to 1, step 0.05, default 0.6.
- `L`, finder's loss if caught: $0 to $5,000, step 50, default 300.
- `a`, chance a report is paid: 0.1 to 1, step 0.05, default 0.8.
- `B`, your bounty: $0 to $20,000, step 50, default 1,650.
- `d`, studio harm per day: $0 to $20,000, step 100, default 4,000.
- `R`, incident cost: $0 to $100,000, step 1,000, default 20,000.

**Readouts** next to the panels: exploit EV `E_x`, report EV `a × B`, `B*`, `C_x`, and a verdict line: "At N days, a rational finder reports" or "...exploits".

**The one insight.** Dragging detection time from 60 days to 2 days drives `B*` under the bounty line while the studio's cost stays far above the bounty in every position.

**Test values** (must match exactly, rounded to whole dollars):

| `1/h` (days) | `E_x` | `B*` | `C_x` |
|---|---|---|---|
| 50 | 7,320 | 9,150 | 220,000 |
| 20 | 2,820 | 3,525 | 100,000 |
| 10 | 1,320 | 1,650 | 60,000 |
| 4 | 420 | 525 | 36,000 |
| 2 | 120 | 150 | 28,000 |

with all other sliders at defaults. At defaults, the verdict reads "reports" (tie goes to reporting since `a × B = E_x = 1,320`). With `1/h = 1`, `E_x = 150 − 180 = −30`, so `B* = 0`, and the curve touches zero.

**Accessibility and style.** Use the shared tokens from `templates/interactive-tokens.css`. Both panels have text alternatives listing the current numbers. Respect reduced motion (no animated transitions). No game logos or art.

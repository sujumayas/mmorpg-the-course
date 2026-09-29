# MMO309 · Week 09 — Account Security and Takeovers

**Why this matters:** Once items in your game are worth money, every account holding them is a target, and most of the people who lose them did nothing unusual. You can't stop every stolen password. You can decide how much a thief gets away with, and that decision lives in your game design (trade rules, delays, recovery flows) as much as in your login screen.

**You will be able to:**
- Model an account takeover as a chain of steps and name a defense that breaks each link.
- Compute the share of stolen value a trade hold lets you recover, given how long victims take to notice, and find where a longer hold stops paying.
- Estimate how two-factor adoption and new-device challenges change the yield of a credential-stuffing campaign.
- Critique an account recovery flow as the attacker's easiest way in, and design time delays around security changes.

**Before class:** NIST Special Publication 800-63B-4, *Authentication and Authenticator Management* (final, August 2025), sections 3.1.1 (passwords) and 3.2.2 (rate limiting), about 20 minutes. Skim [MMO402 week 9 on virtual property](../../MMO402-emergent-society-governance-and-ethics/lectures/w09-virtual-property-and-law.md) for why stolen items raise legal as well as design questions.

**Prerequisites from earlier courses:** [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md). [MA101 week 5, logarithms](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md) (you will solve `1 − e^(−H/m) = r` for `H`). [DB201 week 6, race conditions and the duplication bug](../../DB201-data-persistence-and-telemetry/lectures/w06-race-conditions-and-the-duplication-bug.md) (restoring stolen items can create duplicates). [MMO304 week 11, real-money trade](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w11-real-money-trade-and-gold-farming.md) (stolen accounts feed the gold market). From this course, [week 1 on threat modeling](w01-threat-modeling-for-games.md), [week 4 on duplication](w04-duplication-exploits-and-transactional-design.md) and [week 8 on detection](w08-machine-learning-for-detection-overview.md).

**Interactive:** [examples/w09-trade-hold.html](../examples/w09-trade-hold.html). Use it during section 2.

---

## 1. Why game accounts are stolen, and how

### The value on the account

An MMO account can hold currency, tradable items, characters with hundreds of hours of progress, and sometimes a stored payment method. Each of those has a price on some market. In December 2015 Valve wrote that "essentially all Steam accounts are now targets" because trading cards and items gave nearly every active account enough value to be worth a thief's time. Valve also reported that account theft had grown twenty-fold as the top complaint from its users since Steam Trading launched, and that it saw around 77,000 accounts hijacked each month.

In [week 1](w01-threat-modeling-for-games.md)'s threat-modeling terms, the **asset** is everything the account can transfer or sell, the **threat actors** range from opportunists with a leaked password list to professionals who steal items as their job, and the **impact** lands on the player, on your support team, and on your economy.

### The takeover chain

An **account takeover (ATO)** is any case where someone other than the owner gains control of the account. It is easier to defend when you break it into steps, because each step has its own defenses and a thief must pass all of them.

| Step | What the attacker needs | Main defenses |
|---|---|---|
| 1. Get a credential | The password, a session token or a recovery path | Breached-password checks, phishing-resistant sign-in, education |
| 2. Log in | Pass whatever the login asks | Two-factor authentication, new-device challenges, rate limits, login anomaly detection |
| 3. Take control | Change password, email or 2FA so the owner is locked out | Confirmations to the old email, delays on security changes |
| 4. Strip value | Move items and currency to accounts the attacker controls | Trade holds, trade limits for new devices, detection of "empty the inventory" patterns |
| 5. Cash out | Sell items, gold or the account | Economy monitoring, RMT enforcement ([week 10](w10-gold-sellers-and-rmt-networks.md)) |

At the level a defender needs, the ways step 1 happens are few. **Credential stuffing** tries email and password pairs leaked from other websites, betting that people reuse passwords. **Phishing** tricks the player into typing credentials into a fake login page, often advertised as free items or a trade offer. **Malware** on the player's machine records keystrokes or copies session cookies. **Recovery abuse** persuades your support staff or your automated "forgot password" flow to hand over the account. Each has a different fix, and no single fix covers all four.

Notice where most of the value is lost. Steps 1 and 2 are about identity, and the security industry has standard answers for them (section 3). Steps 3 to 5 are about your game's rules, and nobody but your design team can fix them. The worked example is about step 4.

## 2. Worked example: the trade hold

### The hook

Valve's first response to the theft wave, in late 2015, was a **trade hold**. Items leaving an account in a trade are held for a period before they arrive, unless the account uses the Steam Guard Mobile Authenticator. By December 2015 the rules had been softened, with a three-day hold only when the person giving up the item had no authenticator and a one-day hold between players who had been Steam friends for a year. Valve tightened trading security again in early March 2016 (Rock Paper Shotgun reported it on 3 March). Wikipedia, citing a GameSpot report of 2 March 2016, says the new rule put a 15-day hold on items traded from accounts without the mobile authenticator. We could not reach GameSpot or a Valve page to confirm the 15 days, so treat that figure as reported, not confirmed.

Players complained. A hold punishes every honest trade to slow down a minority of thieves. So why would a designer accept that cost, and why 15 days rather than 3 or 60?

### The model

A thief who strips an account starts a race. The owner has to notice the theft and report it before the stolen items become final. If the hold lasts `H` hours, any theft reported within `H` hours is **recoverable**. The items are still in transit, so support can cancel the trade without taking anything from a third party.

Let `T` be the time from the theft to the owner's report. Assume, as a first model, that `T` is exponentially distributed with mean `m` hours. The exponential is the continuous version of the geometric wait you met in MA102 week 7, the model for "some constant chance each hour that the owner logs in and looks." Then

```
recoverable share   r(H) = P(T ≤ H) = 1 − e^(−H / m)
thief keeps               1 − r(H) = e^(−H / m)
```

To reach a target recovery `r`, solve for `H` (MA101 week 5):

```
H = −m × ln(1 − r)
```

### Numbers you can check

With `m = 48` hours (a mean of two days to notice, invented for teaching):

```python
import math

def recoverable(hold_hours, mean_notice_hours):
    """Share of thefts reported while the stolen items are still on hold."""
    return 1 - math.exp(-hold_hours / mean_notice_hours)

m = 48  # mean hours until a victim notices (invented for teaching)
for days in [0, 1, 3, 7, 15]:
    r = recoverable(24 * days, m)
    print(f"hold {days:2d} days: recoverable {r:6.1%}, thief keeps {1 - r:6.1%}")
```

Output:

```
hold  0 days: recoverable   0.0%, thief keeps 100.0%
hold  1 days: recoverable  39.3%, thief keeps  60.7%
hold  3 days: recoverable  77.7%, thief keeps  22.3%
hold  7 days: recoverable  97.0%, thief keeps   3.0%
hold 15 days: recoverable  99.9%, thief keeps   0.1%
```

Check row 3 by hand: `72 / 48 = 1.5`, `e^(−1.5) = 0.223`. A hold one and a half times the mean noticing time lets you recover more than three quarters of stolen value. For 95% recovery you need `H = −48 × ln(0.05) = 48 × 3.0 = 144` hours, six days.

The thief's side of the table is the design lever. A thief's expected take per stolen account is the account's value times `e^(−H/m)`. Going from no hold to a three-day hold cuts it to 22%. If stealing accounts was a business at 100%, it may not be one at 22%.

### When victims are not all alike

The single exponential says every victim notices at the same average rate. Real victims fall into groups. Players who log in daily notice within hours. Players who have stopped playing may not look for weeks. Model victims as a mix: 70% active players with `m = 12` hours, 30% lapsed players with `m = 480` hours (20 days). Both values are invented for teaching.

```python
import math

def recoverable_mix(hold_hours, groups):
    """groups: list of (share of victims, mean hours until they notice)."""
    return sum(share * (1 - math.exp(-hold_hours / mean)) for share, mean in groups)

victims = [(0.7, 12), (0.3, 480)]   # active players, lapsed players (invented)
for days in [1, 3, 7, 15, 30]:
    print(f"hold {days:2d} days: recoverable {recoverable_mix(24 * days, victims):6.1%}")
```

Output:

```
hold  1 days: recoverable  62.0%
hold  3 days: recoverable  74.0%
hold  7 days: recoverable  78.9%
hold 15 days: recoverable  85.8%
hold 30 days: recoverable  93.3%
```

The shape changes. The active group is almost fully recovered after one day (`0.7 × (1 − e^(−2)) = 60.5%` of all victims). After that the curve crawls, because the remaining thefts belong to people who are not looking. Going from 3 to 15 days buys about 12 points of recovery, all from lapsed accounts.

This is also how thieves choose targets. An account that has been idle for months has a large `m`. Valve noted that thieves can wait months for a payoff, and an idle account is the one where waiting works. So the mix model points to a second defense. Treat the first trades after a long absence, or after a login from a new device, as higher risk, and give them a longer hold than an active player's routine trades.

Open the interactive. The left view plots the recovery curve `r(H)` with a shaded hold window. The right view shows the other side of the ledger, honest trade-days of delay per day of trading. Drag the hold from 0 to 30 days. On the left, the gain flattens after a few multiples of `m`. On the right, the cost keeps growing in a straight line. Then raise 2FA adoption, which exempts those players from the hold. The right-hand line tilts down while the left-hand curve does not move, because the exemption applies to accounts where theft is much harder in the first place.

### The cost side

The hold's cost falls on honest traders. If `D` trades happen per day, a share `a` of traders use an authenticator and are exempt, and the hold is `H` days, the waiting you impose each day is

```
delay cost = (1 − a) × D × H   trade-days
```

With 200,000 trades a day, `a = 40%` and a 3-day hold, that is `0.6 × 200,000 × 3 = 360,000` trade-days of waiting per day of trading. Raise adoption to 70% and it drops to 180,000. A 15-day hold at 40% adoption is 1.8 million trade-days. This is the number players feel, and it explains why the hold is tied to the authenticator. Exempting authenticated accounts sends the cost only to accounts that are easier to steal, and gives everyone a reason to enable the authenticator.

### Cross-game recognition

The same idea is to delay the irreversible action long enough for the owner to notice. It shows up in many places, rewritten into `r(H) = 1 − e^(−H/m)` form.

**Steam (trade holds, December 2015 and March 2016).** The hold is on items leaving the account. `H` is 15 days without the mobile authenticator, as reported for March 2016, and zero with it. The one-day hold between long-time friends is a second exemption based on trust: a trade between two accounts with a year-long history is unlikely to be a thief emptying a stranger's inventory.

**RuneScape and Old School RuneScape (Bank PIN, introduced 19 September 2005, current in Old School).** Here the hold protects the *security setting* rather than the items. A new Bank PIN takes 7 days to become active. Deleting a PIN takes 3 or 7 days, as the player chooses. A thief who gets the password cannot delete the PIN and then empty the bank the same evening. The owner has days to notice the pending change. The PIN also re-locks immediately when the account logs in from a different IP address or computer, the "new device" signal again. The RuneScape Authenticator applies the same logic to removal, which goes through a link sent to the account's registered email.

**World of Warcraft (Battle.net Authenticator, current).** Blizzard attacks the `a` term instead of `H`. Attaching the authenticator and phone notifications gives a Core Hound Pup companion pet, and since patch 7.3.5 four extra slots in the default backpack. Removing the authenticator takes the rewards away. RuneScape does the same with 20 extra bank spaces. Paying players, in game currency, to raise adoption is cheaper than supporting stolen accounts.

**Outside games: banking.** Many banks delay or limit the first payments to a newly added payee. It is the same structure: the risky action is the first transfer to a new destination, and a short delay gives the owner time to notice.

Four systems, one variable each. Steam and banks set `H` on transfers, RuneScape sets `H` on security changes, and WoW and RuneScape raise `a`.

### Eyes-open design judgment

- **Size the hold to how fast victims notice, not to a round number.** Past about three times the typical noticing time, extra days buy little recovery and cost the same friction every day. Measure `m` from your own support tickets: time from the theft event in your logs to the owner's report.
- **Put the delay where irreversibility is.** A hold matters only if your team can reverse the transfer during it. If items leave the account instantly and the hold is only on display, you've added friction without adding recovery.
- **Exempt what is already safe, and say why.** Authenticated accounts, long-standing trade partners and routine small trades can go through faster. Every exemption is also a target, so watch for thieves who enable 2FA on a stolen account before trading. Pair exemptions with a hold after any security change.
- **Recovery can break your economy.** Valve noted that its old method of restoring stolen items created duplicates, which devalued rare items for everyone. If you restore by creating a new copy instead of reversing the original transfer, you are running a duplication exploit yourself (DB201 week 6, week 4 of this course). A hold is attractive partly because it lets you cancel the transfer instead of copying the item.
- **Communicate the reason.** Players accept friction they understand. Valve's December 2015 post explained the numbers. Players who know that the alternative is a 77,000-a-month theft rate complain less.

### Check yourself (worked example)

1. With `m = 36` hours, what share of stolen value does a 2-day hold recover? How long a hold gives 90%?
2. In the mixed model, what share of thefts is still unrecoverable after an infinitely long hold? Why is this model wrong about that, and what happens in real systems?
3. Your game has 50,000 trades a day and 25% authenticator adoption. How many trade-days of waiting does a 5-day hold impose per day? What adoption would halve that?

<details>
<summary>Answers</summary>

1. `1 − e^(−48/36) = 1 − e^(−1.33) = 1 − 0.264 = 73.6%`. For 90%, `H = −36 × ln(0.1) = 36 × 2.303 = 82.9` hours, about 3.5 days.
2. None. Every exponential term goes to 1 as `H` grows, so recovery goes to 100%. The model is wrong because some victims never return to the game and never report, and because a very long hold makes trading useless, so the game would have to allow other ways to move value, which thieves would use.
3. `0.75 × 50,000 × 5 = 187,500` trade-days. Halving needs `1 − a = 0.375`, so `a = 62.5%`.

</details>

## 3. Stopping the login

Holds limit the damage after a login succeeds. The standard defenses reduce how often it succeeds.

### Passwords, per current guidance

NIST SP 800-63B-4 (final, August 2025) is the United States federal guideline for authentication, and much of it is good practice for any online service. Several of its password rules surprise people who learned older advice.

- Check new passwords against a **blocklist** of common, expected or compromised values, and refuse matches.
- Do **not** impose composition rules such as "one digit and one symbol."
- Do **not** force periodic password changes. Force a change only when there is evidence of compromise.
- Limit consecutive failed attempts on one account to no more than 100. The guideline explains the number by comparison with a six-digit one-time code, where 100 guesses succeed with probability `100 / 1,000,000 = 0.01%`.

The blocklist is the rule that matters most against credential stuffing, because stuffing depends on passwords that already appear in leaked lists.

### Why per-account limits do not stop stuffing

A credential-stuffing campaign tries each leaked pair once or twice. It never comes close to 100 failures on any single account. What it does produce is a jump in failed logins across many accounts at once, often from infrastructure that also sends little ordinary traffic: many accounts from one network, login attempts with no prior game session, clients that skip normal launcher steps. Those are detection features in the week 7 sense, measured across accounts instead of within one. The week 8 base-rate warning applies in full, since most logins are honest.

### Two factors and challenges

**Two-factor authentication (2FA)** asks for something besides the password, commonly a six-digit code from an authenticator app or a push confirmation. A stuffed password alone no longer works. A **new-device challenge** is a lighter version applied only when a login looks unusual: a code sent to the registered email, for example, when the device or location is new.

Here is a model of one stuffing campaign against a million accounts. Every rate is invented for teaching. Suppose 1.5% of your accounts have a password that still works in the attacker's list.

```python
def takeovers(accounts, reuse, adoption, challenge_catch):
    """Expected takeovers from one credential-stuffing campaign."""
    working = accounts * reuse                  # leaked password still works
    no_2fa = working * (1 - adoption)           # 2FA stops the rest
    return no_2fa * (1 - challenge_catch)       # new-device challenge stops some

for adoption in [0.0, 0.4, 0.7]:
    for catch in [0.0, 0.8]:
        n = takeovers(1_000_000, 0.015, adoption, catch)
        print(f"2FA adoption {adoption:4.0%}  challenge catches {catch:4.0%}  takeovers {n:7,.0f}")
```

Output:

```
2FA adoption   0%  challenge catches   0%  takeovers  15,000
2FA adoption   0%  challenge catches  80%  takeovers   3,000
2FA adoption  40%  challenge catches   0%  takeovers   9,000
2FA adoption  40%  challenge catches  80%  takeovers   1,800
2FA adoption  70%  challenge catches   0%  takeovers   4,500
2FA adoption  70%  challenge catches  80%  takeovers     900
```

The layers multiply, like the damage-reduction layers in MMO303 week 2. Each one removes a share of what is left. Two observations follow. First, a challenge on unusual logins protects the accounts that never enable 2FA, which is most of them in many games. Second, the incentives in section 2's cross-game list (a pet, bag slots, bank space) are worth their cost if they move adoption by tens of points.

### What 2FA does not stop

A phishing page can ask for the one-time code as well as the password and use both within seconds. Malware that steals a logged-in session cookie skips the login entirely. NIST's current guideline requires services at its second assurance level to offer a **phishing-resistant** option, meaning an authenticator bound to the real site's identity, such as a passkey, which a fake page cannot use. For a game, the practical lessons are to keep the trade hold even for 2FA users on new devices and after security changes, and to end every session when the password changes.

## 4. Recovery is the back door

Every account system needs a way back in for owners who lose their password or their phone. That path is also a way in for thieves. A recovery flow is only as strong as its weakest accepted proof.

- **Email-only recovery** makes the email account the real key. Encourage 2FA on the email, as the RuneScape Wiki's guidance does for the RuneScape Authenticator.
- **Support-desk recovery** depends on staff judgment under pressure from a convincing caller. Give staff a written list of acceptable proofs (past purchase details, account creation data) and forbid exceptions for urgency or status.
- **Security changes should be slow and loud.** A change of email, password or 2FA device should notify the old email and phone, and should start a hold on trades and on further security changes. That is the Bank PIN design applied to the whole account.

A useful exercise is to write your recovery flow as a sequence of steps and ask which one a stranger with the player's email address and a convincing story could pass. Week 1's method of listing assets, attackers and entry points works well here.

## In-class activity (25 minutes)

Groups of three. You design account security for a mid-sized MMO with a player market. Numbers from last quarter (invented): 800,000 active accounts, 60,000 trades per day, 30% of accounts with 2FA, 1,200 confirmed takeovers per month, and a median of 20 hours from theft to report, with a long tail of lapsed accounts.

1. Draw the five-step takeover chain for your game and put one defense on each step. (8 minutes)
2. Treat the median as coming from an exponential. What `m` does a 20-hour median imply? (Hint: the median of an exponential is `m × ln 2`.) Pick a hold `H` that recovers 90% for active players. (7 minutes)
3. Compute the daily delay cost of your hold at 30% adoption and propose one incentive to raise adoption. (5 minutes)
4. Name the easiest step in your recovery flow for a thief, and one change that makes it harder. (5 minutes)

Expected output: the annotated chain, `m`, `H`, the delay cost, the incentive, and the recovery change.

## Common misconceptions

- **"Players who get hacked were careless."** Valve's post described professional players, community contributors and traders among its victims. Password reuse is very common, and phishing pages imitate official ones closely. Design for ordinary behavior.
- **"Forcing strong passwords and regular changes is best practice."** Current NIST guidance says the opposite about composition rules and periodic changes, and asks for blocklist checks instead.
- **"With 2FA, a trade hold is unnecessary."** 2FA stops stuffed passwords, not phishing of codes or stolen sessions. Keep holds after new-device logins and security changes.
- **"Restoring stolen items is free."** If restoration creates a copy instead of reversing the transfer, it adds items to the economy. Valve noted that its old restorations created duplicates and devalued rare items.

## Check yourself

1. A hold of 4 days recovers 86.5% of stolen value under the single-exponential model. What is `m`?
2. In the stuffing model, 2% of accounts have working leaked passwords, adoption is 50%, and a new-device challenge catches 60% of the rest. How many takeovers per 500,000 accounts? Which lever would you pull first, and why?
3. A designer proposes removing the Bank-PIN-style delay "because it annoys players who forget their PIN." Describe the attack this reopens in two sentences and suggest a design that keeps most of the protection.
4. Why does per-account rate limiting at 100 failures do little against credential stuffing, and what signal would you watch instead?

<details>
<summary>Answers</summary>

1. `e^(−96/m) = 0.135`, so `96/m = −ln(0.135) = 2.0` and `m = 48` hours.
2. `500,000 × 0.02 × 0.5 × 0.4 = 2,000`. The challenge is often the fastest lever, because it applies to everyone without asking players to act. Adoption incentives take longer but also protect against phishing of passwords alone.
3. A thief with the password could delete the PIN and empty the bank in one session, before the owner notices. Keep the delay on deletion, and let players reset a forgotten PIN through a verified channel (authenticator or email with 2FA) that notifies the owner.
4. Stuffing tries each account once or twice, so no account reaches the limit. Watch failure rates across many accounts, logins from networks with many distinct accounts, and logins with no normal game-client behavior.

</details>

## Lab / assignment hook

There is no lab for this week. The week 9 model feeds the course's threat-model assignment (30% of the grade, see the [threat model brief](../assessments/threat-model-brief.md)). Your threat model must include the takeover chain for your game, a hold length justified with the recovery formula and your chosen `m`, and the expected delay cost. [Lab 08](../labs/lab08.md)'s triage method applies unchanged to login-anomaly scores if you choose to add detection.

## Sources

- Valve, "Security and Trading", Steam news post, 9 December 2015 (archived by the Internet Archive). The primary source for the 77,000 hijackings a month, the twenty-fold rise, "essentially all Steam accounts are now targets", the 3-day and 1-day holds, and the duplicates created by old restorations.
- O'Connor, A. (10 December 2015). "77,000 Steam Accounts Hijacked Each Month For Items." *Rock Paper Shotgun*. Reports and quotes Valve's post on trade holds: around 77,000 accounts hijacked each month; theft grown twenty-fold as the top complaint since Steam Trading; "essentially all Steam accounts are now targets"; victims include professional CS:GO players and traders; thieves can wait months; restorations created duplicates; three-day hold only when the giver lacks the authenticator; one-day hold for friends of a year.
- O'Connor, A. (3 March 2016). "Valve Tighten Steam Trading Security Again." *Rock Paper Shotgun* (read via the Steam news feed, September 2026). Confirms a further tightening in March 2016, including holds on the Steam Market; the excerpt read does not give the hold length.
- Steam (service), Wikipedia (accessed September 2026), security section, citing E. Makuch, "New Steam Security Updates Coming Next Week", GameSpot (2 March 2016), which sits behind a bot check. 15-day holds from March 2016 on traded items unless the account uses the Steam Guard Mobile Authenticator. Steam Guard launched March 2011; mobile authenticator added 2015.
- Old School RuneScape Wiki, "Bank PIN" and "Authenticator" (current). Bank PIN introduced 19 September 2005; 7 days to activate; removal after 3 or 7 days; re-lock on new IP or computer; 20 extra bank spaces; authenticator uses RFC 6238 time-based codes; removal through an emailed link; advice to protect the email with 2FA.
- Warcraft Wiki, "Battle.net Authenticator", "Core Hound Pup" and "Backpack" (current retail). Rewards for authenticator plus phone notifications: Core Hound Pup, four extra backpack slots (added in patch 7.3.5), higher Battle.net Balance limit; rewards removed when the authenticator is removed.
- National Institute of Standards and Technology (2025). *SP 800-63B-4, Authentication and Authenticator Management* (final). Blocklist checks; no composition rules; no forced periodic changes; at most 100 consecutive failed attempts, justified by six-digit OTP guessing odds; phishing-resistant option required at AAL2.
- All values of `m`, victim mixes, trade volumes, adoption rates, reuse rates and challenge catch rates in sections 2 and 3, the activity and the questions are invented for teaching.

## Interactive spec: examples/w09-trade-hold.html

**The one insight:** recovery from a trade hold rises fast and then saturates at a few multiples of the mean noticing time, while the delay cost to honest traders keeps rising in a straight line. Exempting authenticated accounts lowers the cost without lowering recovery.

**Layout.** Two charts side by side on desktop, stacked on mobile.

- **Left chart, "Thefts you can reverse."** x-axis hold `H` in days, 0 to 30. y-axis recoverable share 0 to 100%. Plot `r(H) = Σ sᵢ (1 − e^(−24H / mᵢ))` for the current victim mix. Vertical marker at the chosen `H`, with the area under the curve left of it lightly shaded. Dashed horizontal lines at 90% and 95%. Readouts: recoverable share at `H` (1 decimal), thief keeps `1 − r`, and marginal gain of one more day `r(H+1) − r(H)` in points.
- **Right chart, "What honest traders pay."** Same x-axis. y-axis trade-days of delay per day, `(1 − a) × D × H`. Draw the current line solid and the line for `a = 0` faint, so the saving from adoption is visible. Readout: delay cost at `H` (thousands, 0 decimals).
- **Efficiency readout** under both charts: "recovery points per million trade-days" at `H`, `100 × r(H) / ((1 − a) × D × H / 10⁶)`, shown as a small number (hidden at `H = 0`).

**Controls.**
- Hold `H` slider, 0 to 30 days, step 0.5, default 3.
- Victim model toggle: "One group" (single `m` slider, 2 to 240 hours, default 48) or "Active + lapsed" (active share slider 0 to 100%, default 70%; active `m` default 12 h; lapsed `m` default 480 h; each `m` slider 2 to 1,000 h).
- 2FA adoption `a` slider, 0 to 95%, default 40%.
- Trades per day `D` numeric input, default 200,000.
- Button "Hold for 90% recovery": sets `H` to the smallest half-day value with `r(H) ≥ 0.9`, or shows "not reachable within 30 days."

**Test values.** One group, `m = 48`: `H = 1` gives 39.3%, `H = 3` gives 77.7%, `H = 7` gives 97.0%, `H = 15` gives 99.9%; "Hold for 90%" returns 5.0 days (`r = 1 − e^(−2.5) = 91.8%`), because 4.5 days gives only `1 − e^(−2.25) = 89.5%`. Active + lapsed at 70%/12 h/480 h: `H = 1` gives 62.0%, `H = 3` gives 74.0%, `H = 7` gives 78.9%, `H = 15` gives 85.8%, `H = 30` gives 93.3%. Delay cost at `a = 40%`, `D = 200,000`, `H = 3`: 360,000; at `a = 70%`: 180,000.

**First screen.** Active + lapsed mix, `H = 3`, `a = 40%`. The left curve is already flattening at the marker while the right line keeps climbing.

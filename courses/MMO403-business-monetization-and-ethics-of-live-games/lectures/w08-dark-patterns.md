# MMO403 · Week 08 — Dark Patterns

**Why this matters:** Some of the most profitable designs in live games work by creating a problem and selling its end: a wait you can skip, a fear of missing out you can calm, a purchase that is easier to make than to undo. None of them looks wrong on a revenue dashboard. This week you learn to name these patterns, to compute why the metrics you were taught reward them, and to tell a legitimate timer or offer from a dark one before a regulator or your players do it for you.

**You will be able to:**
- Classify a monetization feature with Zagal, Björk and Lewis's categories (temporal, monetary, social) and the interface patterns named in recent enforcement.
- Compute the lifetime value of a paid-skip wall as a function of wait length, find the wait that maximizes it, and state the player lifetime it costs.
- Compute the asymmetry between a do-flow and an undo-flow and explain why it predicts unwanted charges.
- Critique a store or progression system with a written dark-pattern review that separates pacing from friction for sale.

**Before class:** Zagal, J. P., Björk, S. & Lewis, C. (2013), "Dark Patterns in the Design of Games", *Foundations of Digital Games 2013* (6 pages, free online). Read all of it. US Federal Trade Commission press release on Epic Games (19 December 2022), the section "Illegal dark patterns", about 5 minutes. Fields & Cotton, *Social Game Design: Monetization Methods and Mechanics* (Morgan Kaufmann, 2011), the material on energy systems and paid acceleration.

**Prerequisites from earlier courses:** [UX201 week 5, reinforcement schedules and their ethics](../../UX201-game-ux-and-player-psychology/lectures/w05-reinforcement-schedules-and-ethics.md) (stopping points and its seven-question ethics checklist, which this week extends to money and interfaces). [MMO402 week 10, addiction, wellbeing and responsible design](../../MMO402-emergent-society-governance-and-ethics/lectures/w10-addiction-wellbeing-and-responsible-design.md) (pacing rules and the obligation test; its rested-versus-fatigue model is about play time, ours is about selling time). [MA101 week 6, rational functions](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w06-rational-functions-and-asymptotes.md) (the saturating curve `w / (w + a)`). [GS101 week 11](../../GS101-history-and-critical-study-of-games/lectures/w11-free-to-play-mobile-and-live-service.md) (monthly lifetime `1 / (1 − r)` and `LTV = ARPU × lifetime`). [MMO308 week 4, funnels and churn](../../MMO308-live-operations-analytics-and-experimentation/lectures/w04-funnels-and-churn.md) (step-by-step completion). From this course, [week 3, premium currencies](w03-premium-currencies.md), [week 5, battle passes](w05-battle-passes.md) (deadlines and FOMO) and [week 7, regulation](w07-regulation-belgium-netherlands-china-others.md).

**Interactive:** [Friction for sale](../examples/w08-friction-for-sale.html). Keep it open during section 2.

---

## 1. What makes a pattern dark

The UX designer Harry Brignull coined "dark patterns" on 28 July 2010, when he registered darkpatterns.org (now deceptive.design) to catalogue interfaces built to trick users: a pre-ticked box that adds insurance, a cancel link hidden in grey text. Games inherited the term and widened it.

In 2013 José Zagal, Staffan Björk and Chris Lewis asked what a dark pattern would mean for gameplay rather than for web forms. Their answer went through three drafts, and the drafts teach the idea better than the final wording.

1. First draft: a pattern a designer uses on purpose to cause a negative experience. Too broad. Horror games and hard games do that, and players choose them for it.
2. Second draft: add "without the player's consent". Closer. But some tricks players don't consent to are in their interest, such as racing games that quietly help the player who falls behind.
3. Final version, in paraphrase: a pattern a game's creator uses on purpose to cause negative experiences that go **against the player's best interests** and happen **without their consent**.

The final version has two tests, interest and consent. Keep both. A daily quest is not dark because it brings players back. It becomes dark if it works by making players act against their interests (playing when they don't want to, spending more than they meant to) in a way they didn't agree to and may not notice.

### A taxonomy

Zagal and colleagues sorted the patterns by what the player is manipulated into spending. Brignull's catalogue and recent enforcement add a fourth group about the interface itself.

| Category | Pattern | What the player loses | Example the authors or regulators give |
|---|---|---|---|
| Temporal | Grinding | Time on repetitive tasks, beyond what they expected | Level grinds in MMOs and in shooters with unlock trees |
| Temporal | Playing by appointment | Control over when they play | FarmVille crops that wither if not harvested in time |
| Monetary | Pay to skip | Money to remove an obstacle the game placed | SimCity Social energy that runs out faster as the city grows |
| Monetary | Pre-delivered content | Money for content already on the disc or in the download | Street Fighter X Tekken's on-disc characters sold separately |
| Monetary | Monetized rivalries | Money to keep up with other players | Paid boosts in games with public leaderboards |
| Social | Social pyramid schemes | Friendships, used to recruit | FarmVille's need for in-game neighbours |
| Social | Impersonation | Reputation, when the game speaks as the player | "Your friend sent you a gift" when the friend did nothing |
| Interface | Misdirection and asymmetric friction | Money, through purchases they didn't intend | Fortnite's button layout (FTC complaint, 2022) |

Two notes on the table. First, the authors left gambling out of their list on purpose, arguing that a player who bets knows the odds are against them. Week 6 and week 7 showed why regulators have not accepted that argument for paid random rewards, especially when odds are hidden or the buyer is a child. Second, the authors spend a whole section on "shades of grey". The same mechanic can be light or dark depending on implementation and audience. A timer that gates a crafting queue in a game for adults with no paid skip is pacing. The same timer with a paid skip, placed where the player is most eager, is something else. The worked example measures that difference.

## 2. Worked example: friction for sale

### The hook

In Candy Crush Saga you hold at most five lives. Failing a level costs one. Lives come back at one every 30 minutes, so an empty bar takes two and a half hours to refill. When you run out, the game offers three ways forward: wait, pay for a refill, or ask friends to send lives. That one screen holds three of the patterns in the table: playing by appointment, pay to skip, and a social request.

Nothing about the level itself required the wait. The studio built the wall and then sold its removal. Why would a business make its own game harder to play? Because the metric it is taught to maximize, lifetime value, often goes up when it does.

### The model

Take a game where each player hits a wall `n` times a month. At each wall they can wait `w` hours for free or pay `s` to continue at once. The designer chooses `w`.

```
pay share per wall     π(w) = m × w / (w + a)
monthly retention      r(w) = r0 − d × w / (w + b)
ARPU per month         ARPU(w) = A0 + n × s × π(w)
lifetime in months     L(w) = 1 / (1 − r(w))
lifetime value         LTV(w) = ARPU(w) × L(w)
```

- `π(w)` is the share of wall encounters where the player pays. It starts at zero (nobody pays to skip no wait), rises with `w`, and levels off at `m`, the most that will ever pay. `a` is the wait at which half of that ceiling pays.
- `r(w)` is the share of players still playing next month. It starts at `r0` with no wall and falls toward `r0 − d` as the wall grows. `b` is the wait at which half of that loss has happened.
- `A0` is the rest of the player's monthly spending (cosmetics, passes), which the wall doesn't affect.
- `L(w)` and `LTV(w)` are GS101 week 11's lifetime and lifetime value. Week 2 of this course built LTV day by day. The monthly form is enough here.

Both curves have the saturating shape `w / (w + a)` from MA101 week 6. The parameter values below are invented for teaching. They are not any studio's data.

### Numbers you can check

Use `A0 = $0.50`, `n = 20` walls a month, `s = $1.00`, `m = 10%`, `a = 2` hours, `r0 = 90%`, `d = 20` points and `b = 8` hours.

```python
A0, n, s = 0.50, 20, 1.00   # other spending per month, walls per month, skip price
m, a = 0.10, 2.0            # pay share ceiling, wait (hours) where half of it pays
r0, d, b = 0.90, 0.20, 8.0  # retention with no wall, churn ceiling, half-churn wait

def pay(w):      return m * w / (w + a)
def retention(w): return r0 - d * w / (w + b)
def arpu(w):     return A0 + n * s * pay(w)
def lifetime(w): return 1 / (1 - retention(w))
def ltv(w):      return arpu(w) * lifetime(w)

for w in [0, 1, 2, 3.5, 6, 12, 24]:
    print(f"w={w:>4} h  pay {pay(w):6.2%}  ARPU ${arpu(w):.2f}  "
          f"r {retention(w):6.2%}  lifetime {lifetime(w):5.2f} mo  LTV ${ltv(w):5.2f}")

best = max((ltv(t / 100), t / 100) for t in range(0, 4801))
print(f"best wait {best[1]:.2f} h, LTV ${best[0]:.2f}, lifetime {lifetime(best[1]):.2f} mo")
```

It prints:

```
w=   0 h  pay  0.00%  ARPU $0.50  r 90.00%  lifetime 10.00 mo  LTV $ 5.00
w=   1 h  pay  3.33%  ARPU $1.17  r 87.78%  lifetime  8.18 mo  LTV $ 9.55
w=   2 h  pay  5.00%  ARPU $1.50  r 86.00%  lifetime  7.14 mo  LTV $10.71
w= 3.5 h  pay  6.36%  ARPU $1.77  r 83.91%  lifetime  6.22 mo  LTV $11.02
w=   6 h  pay  7.50%  ARPU $2.00  r 81.43%  lifetime  5.38 mo  LTV $10.77
w=  12 h  pay  8.57%  ARPU $2.21  r 78.00%  lifetime  4.55 mo  LTV $10.06
w=  24 h  pay  9.23%  ARPU $2.35  r 75.00%  lifetime  4.00 mo  LTV $ 9.38
```

and `best wait 3.46 h, LTV $11.02, lifetime 6.24 mo`.

Check one row by hand. At `w = 2`: `π = 0.10 × 2/4 = 5%`, `ARPU = 0.50 + 20 × 1 × 0.05 = $1.50`, `r = 0.90 − 0.20 × 2/10 = 86%`, `L = 1/0.14 = 7.14` months, `LTV = 1.50 × 7.14 = $10.71`.

Read the table as a studio would, then as a player would.

- **The studio's view.** A wall of about three and a half hours more than doubles lifetime value, from $5.00 to $11.02. Any A/B test that compares LTV (week 10) will pick the wall.
- **The player's view.** The same wall cuts the average player's time in the game from 10 months to about 6.2, a loss of 38%. The players who leave are not in the LTV figure at all. They simply stop contributing.

Both numbers are true at once. The wall creates revenue by making the game worse for most players and selling relief to the few who pay. That is Zagal's "against the player's interests" in numbers.

### Where the peak sits

Why is there a best wait at all? Write churn as `c(w) = 1 − r(w)`. Then `LTV = ARPU / c`, and its slope is zero where

```
ARPU'(w) / ARPU(w)  =  c'(w) / c(w)
```

In words: the metric keeps adding wait until one more minute raises ARPU by the same percentage as it raises churn. At `w = 3.46` both sides equal about 7.6% per hour. The rule tells you which way the peak moves when the world changes:

- **More patient players** (smaller `d`) make churn rise more slowly, so the metric wants a longer wall. Halve `d` to 0.10 and the best wait doubles to about 6.9 hours.
- **Better other products** (larger `A0`) make the skip a smaller share of ARPU, so each extra minute raises ARPU by a smaller percentage. Raise `A0` to $1.00 and the best wait falls to about 2.3 hours.

The second point is the business case for good cosmetics and passes. They weaken the incentive to build friction.

### A visual you can move

Open `examples/w08-friction-for-sale.html`. The top chart plots `LTV(w)` with its peak marked. The bottom chart plots lifetime `L(w)` on the same wait axis, with a shaded band from `w = 0` to the LTV peak labelled "lifetime lost". Drag the wait slider and watch the two readouts. Then drag `d` down and watch the LTV peak slide right while the shaded band widens. The top chart looks like good news. The bottom chart shows who pays for it.

### Cross-game recognition

Rewrite each case as a wall with a wait `w`, a skip price `s`, and a ceiling `m`.

**Candy Crush Saga (lives, as documented on the fan wiki in 2026).** Five lives, one back every 30 minutes, so `w` runs from 30 minutes to 2.5 hours depending on how many you have lost. Skips are sold as refills. The social route (ask a friend) replaces `s` with a favour, which is Zagal's social pyramid logic in miniature.

**SimCity Social (2012, as described by Zagal and colleagues).** Energy spent on actions ran short as the city grew, because the city's needs outgrew the energy cap. In our model that is a wall whose `w` rises with progress. The player meets the steepest part of the curve exactly when they are most invested.

**FarmVille (2009-2010 era, same source).** Crops wither if not harvested in time. This is playing by appointment. The model's wall is the reverse: instead of waiting to continue, the player loses progress for not coming back. PEGI's 2026 criteria draw the same line, rating a game 7 when it rewards returning and 12 when it punishes not returning.

**Battlefield 3 (2011, same source).** The game sold "shortcut" packs that unlocked weapons players would otherwise earn by playing. The grind is the wall and the pack is `s`. The wall was already there for pacing, which is exactly why this case sits in the grey zone.

Four games, one model. When you review a feature, find the wall, ask who sets `w`, and ask whether `w` was chosen for the game or for the curve.

### Eyes-open design judgment

- **Timers are not dark by default.** A wait can pace content, protect an economy from bots, give players a stopping point (UX201 week 5), and let a small team ship content no faster than players consume it. With no paid skip, the model's `π` is zero and none of the pressure in this section exists.
- **The paid skip changes the question.** Once you sell the end of a wait, every choice of `w` is also a price decision. Decide `w` with the skip turned off, then add the skip, and never retune `w` upward using LTV alone.
- **Report both views.** Any test of a wall should report LTV and lifetime (or D30 retention) side by side. A win that cuts lifetime by a third should need a named person to sign it off.
- **Prefer levers that raise `A0`.** The optimum rule shows that better products make friction less profitable. A good cosmetic line is an ethical lever as well as a revenue one.

### Check this example

1. With the lecture's parameters, compute `LTV` at `w = 4` hours by hand.
2. A designer halves `d` because "our players are loyal". Where does the metric's best wait move, and what does that say about loyal audiences?
3. The studio doubles the skip price to $2.00 with nothing else changed. The best wait moves to about 4.3 hours and LTV to about $19.01. Why does a higher price push the wall longer?

<details>
<summary>Answers</summary>

1. `π = 0.10 × 4/6 = 6.67%`, `ARPU = 0.50 + 20 × 0.0667 = $1.83`, `r = 0.90 − 0.20 × 4/12 = 83.33%`, `L = 1/0.1667 = 6.0` months, `LTV = 1.83 × 6.0 = $11.00`.
2. To about 6.9 hours. Churn rises more slowly with the wait, so the percentage condition is met further out. Loyal players are the ones the metric will ask you to squeeze hardest, which is a reason for extra care, not less.
3. With `s` doubled, the skip is a larger share of ARPU, so each extra minute of wait raises ARPU by a larger percentage. The ARPU side of the condition grows while the churn side is unchanged, so the balance point moves right.

</details>

## 3. Interface patterns: making "yes" easier than "undo"

The Zagal categories are about game systems. Most enforcement so far has been about interfaces. The clearest case is the US Federal Trade Commission's action against Epic Games, announced 19 December 2022. Under a separate administrative order from its children's privacy penalty, Epic agreed to pay $245 million in refunds for what the FTC called dark patterns and billing practices. The complaint alleged that Fortnite's "counterintuitive, inconsistent, and confusing" button layout charged players with a single press. Players could be charged while waking the game from sleep mode, during a loading screen, or by pressing a button next to the one that previewed an item. Until 2018, children could buy V-Bucks by pressing buttons without any card-holder action. The complaint also alleged Epic locked the accounts of players who disputed charges with their card company.

A simple model shows why these designs produce unwanted charges. Suppose each step in a flow is completed by a fraction `c` of the players who start it. A flow with `k` steps is finished by

```
completion = c^k
```

(MMO308 week 4 builds this for funnels.) Now compare the flow a studio wants (buy) with the flow a player needs (undo, refund, turn off auto-renew).

| Steps to buy | Steps to undo | `c` | Buy completion | Undo completion | Ratio |
|---|---|---|---|---|---|
| 1 | 1 | 0.85 | 85.0% | 85.0% | 1.0 |
| 1 | 3 | 0.85 | 85.0% | 61.4% | 1.4 |
| 1 | 6 | 0.85 | 85.0% | 37.7% | 2.3 |
| 2 (with confirm) | 6 | 0.85 | 72.3% | 37.7% | 1.9 |

The ratio is `c^(k_buy − k_undo)`. It measures **asymmetric friction**: how much easier the studio has made its preferred choice. Now add mistakes. If 2% of store visits contain an accidental press on the buy button, then 1,000 visits produce 20 accidental purchases with a one-step flow. A confirmation step that catches 90% of mistakes cuts that to 2. The confirmation costs the studio some intended purchases (buy completion falls from 85% to 72%), which is exactly why the one-step flow is tempting and why regulators treat its absence as a choice.

The FTC's January 2025 order against Cognosphere (HoYoverse, Genshin Impact) targeted a different interface, the currency system. The complaint said players had to exchange dollars for one currency and then re-exchange it, sometimes several times, at "unusual denominations" before opening a loot box, and that limited-time event banners and influencer campaigns suggested better odds than players had. The order requires disclosure of odds and exchange rates and an option to buy with real money (week 3 covers the currency arithmetic). One detail matters for balance: two of the five commissioners concurred only on the privacy counts and dissented on the counts that called the loot box practices unfair. What counts as "unfair" in a game store is contested inside the regulator itself.

## 4. Writing a dark-pattern review

A review is a short document a designer writes before a feature ships. Here is a format that uses this week's tools.

1. **Name the pattern.** Place the feature in the taxonomy. If it fits two rows, name both.
2. **Find the wall or the asymmetry.** For a timer or grind, state `w`, the skip price and who chose `w`. For a flow, count `k_buy` and `k_undo`.
3. **Run the two views.** Report the revenue metric and a player metric (lifetime, D30 retention, share of sessions ending at the wall).
4. **Apply the disclosure test.** Zagal and colleagues cite Berdichevsky and Neuenschwander's principle that the makers of persuasive technology should disclose their methods. Ask: would this feature still work if the store said plainly how it works? "Wait 3 hours or pay $1" passes. A button placed where players press by accident fails.
5. **Check the audience.** Children change every answer (MMO402 week 11). The PEGI criteria for games submitted from June 2026 now rate time-limited or quantity-limited offers at 12, and punishing players for not returning at 12. If your game targets younger players, these features have a rating cost.
6. **Decide and sign.** State what you ship, what you changed and who accepted the remaining risk.

The review does not ban anything. It makes the trade-off visible and puts a name on it. Many features pass. Limited-time offers can be honest ("this bundle leaves the store on Sunday and will return in the spring"). Daily rewards can be generous without penalties for missing a day. Confirmations can be quick. The point is to choose these versions on purpose.

## In-class activity (25 minutes)

Pairs. Each pair picks one free-to-play game they have played in the past year and opens its store or progression screen on a phone, or works from memory with screenshots taken beforehand (no copyrighted art in your submission; describe the screens in words).

1. (6 min) List every wait, energy bar, timer, limited-time offer and purchase flow you can find. Place each in the taxonomy table.
2. (8 min) For one wall, estimate `w`, `s` and a plausible `m`. Using the interactive with the lecture's other defaults, find where your `w` sits relative to the LTV peak.
3. (6 min) For one purchase flow, count `k_buy` and `k_undo` (for example, the steps to request a refund or cancel a subscription). Compute the asymmetry ratio at `c = 0.85`.
4. (5 min) Write a two-sentence verdict with the disclosure test: pacing, grey, or dark, and why.

Expected output: the placed list, one model estimate, one ratio, one verdict.

## Common misconceptions

- **"Energy systems are dark patterns."** Only when they work against the player's interest without consent. With no paid skip and a clear purpose (pacing, server load, stopping points), a timer is ordinary design.
- **"If the A/B test won, players must like it."** An LTV test measures revenue from those who stay and pay. The section 2 wall wins on LTV while cutting average lifetime by 38%.
- **"Dark patterns are illegal."** Some are. The FTC's Epic case turned on unauthorized charges, and the EU's consumer principles address currency. Many dark patterns in Zagal's list break no law. Legality is the floor, not the standard.
- **"Adding a confirmation step is just friction."** It is friction placed on purpose on the studio's side of the flow. In the section 3 numbers, it cuts accidental purchases tenfold for a 13-point drop in completion of intended ones.

## Check yourself

1. Using the lecture's parameters, compute LTV and lifetime at `w = 1` hour. Compare with `w = 0` and state both changes in percent.
2. A studio says "our new cosmetics line raised `A0` from $0.50 to $1.00, so we can now afford a longer wall". Use the optimum rule to explain why the metric actually points the other way.
3. A subscription can be started in 2 steps and cancelled in 7. With `c = 0.9`, what are the two completion rates and the asymmetry ratio?
4. Classify each feature with the taxonomy and the disclosure test: (a) a 12-hour crafting timer with no skip in an adult MMO; (b) the same timer with a gem skip whose price rises as the timer gets longer, in a game rated 12; (c) a "your friend is waiting for you" notification the friend never sent.

<details>
<summary>Answers</summary>

1. At `w = 1`, LTV is $9.55 against $5.00 (up 91%), and lifetime is 8.18 months against 10.00 (down 18%).
2. With more spending that the wall doesn't touch, each extra minute raises ARPU by a smaller percentage, so the balance with churn is reached at a shorter wait (about 2.3 hours instead of 3.5). The metric now wants a shorter wall. If the studio lengthens it anyway, that is a choice the metric does not support.
3. Start: `0.9² = 81%`. Cancel: `0.9⁷ = 47.8%`. Ratio `0.81 / 0.478 ≈ 1.7`, which is `0.9^(2 − 7)`.
4. (a) Temporal pacing, not dark: no skip, adult audience, passes the disclosure test. (b) Pay to skip, grey to dark: the skip turns `w` into a price, and the audience includes young players; it needs a review, and the PEGI rules may apply if other criteria are met. (c) Impersonation: dark, since the game speaks for a friend who did nothing, and it fails the disclosure test outright.

</details>

## Lab / assignment hook

[Lab 08, a dark-pattern review](../labs/lab08.md). You implement the friction model and the asymmetry calculation, reproduce the lecture's table and optimum, run a sensitivity sweep, and write a dark-pattern review of one real game's store or progression system using section 4's format. The review is the third input to the ethics analysis (20%).

## Sources

- Zagal, J. P., Björk, S. & Lewis, C. (2013). "Dark Patterns in the Design of Games." *Foundations of Digital Games 2013*, Chania. The three proto-definitions and the final definition; the temporal, monetary and social-capital categories; grinding, playing by appointment (FarmVille withering), pay to skip (SimCity Social energy, Battlefield 3 shortcut items), pre-delivered content (Street Fighter X Tekken), monetized rivalries, social pyramid schemes, impersonation; the decision to exclude gambling; the disclosure principle from Berdichevsky and Neuenschwander. http://www.fdg2013.org/program/papers/paper06_zagal_etal.pdf
- Wikipedia, "Dark pattern" (accessed 28 September 2026). Harry Brignull coined the term on 28 July 2010 with the registration of darkpatterns.org; the site later moved to deceptive.design.
- Candy Crush Wiki (Fandom), "Lives" (accessed 28 September 2026). Maximum five lives outside events; one life regenerates every 30 minutes; refills from the shop or requests to friends.
- US Federal Trade Commission, "Fortnite Video Game Maker Epic Games to Pay More Than Half a Billion Dollars over FTC Allegations of Privacy Violations and Unwanted Charges" (19 December 2022). $245 million refunds under a separate administrative order; button configuration charging on a single press, including while waking from sleep mode, on loading screens and next to the preview button; V-Bucks purchases by children without card-holder action until 2018; account locking after disputed charges.
- US Federal Trade Commission, "Genshin Impact Game Developer Will be Banned from Selling Lootboxes to Teens Under 16 without Parental Consent, Pay a $20 Million Fine to Settle FTC Charges" (17 January 2025). Multi-step currency exchanges in unusual denominations; event banners and influencer campaigns; order terms; Commissioners Ferguson and Holyoak concurring on Counts I-II and dissenting on Counts III-V.
- PEGI, "PEGI expands age rating criteria with interactive risk categories" (12 March 2026). Time- or quantity-limited offers PEGI 12; rewards for returning PEGI 7; punishment for not returning PEGI 12; applies to games submitted from June 2026.
- Fields, T. & Cotton, B. (2011). *Social Game Design: Monetization Methods and Mechanics*. Morgan Kaufmann.
- The friction model's parameters (`A0`, `n`, `s`, `m`, `a`, `r0`, `d`, `b`) are invented for teaching. All table values were computed by the author with the code shown.

## Interactive spec: examples/w08-friction-for-sale.html

**Purpose.** Show that lifetime value can rise while player lifetime falls, when a studio sells the end of a wait it created. Insight on first load: *the LTV curve peaks at about 3.5 hours, and the shaded band under the lifetime curve shows that the same wait costs the average player about 38% of their time in the game.*

**Layout.** Two charts stacked, sharing one horizontal axis (wait `w` in hours, 0 to 24, linear). Top chart "What the dashboard sees": `LTV(w)` in dollars, with a dot and label at the maximum. Bottom chart "What players live through": lifetime `L(w)` in months, with a shaded band between `L(0)` and `L(w*)` labelled "lifetime lost at the LTV peak". A vertical cursor line at the current slider value crosses both charts. On mobile, charts stack full width with the controls below. Numbers panel to the right on desktop, below on mobile. Generic shapes only; no game art, no heart icons from any game.

**Formulas.**
- `π(w) = m × w / (w + a)`
- `r(w) = r0 − d × w / (w + b)`
- `ARPU(w) = A0 + n × s × π(w)`
- `L(w) = 1 / (1 − r(w))`
- `LTV(w) = ARPU(w) × L(w)`
- `w*` = argmax of `LTV` on a grid of 0.01 hours from 0 to 48.

**Controls.** Sliders, each with a number field and keyboard support:
- Wait `w`: 0 to 24 h, step 0.1, default 3.5.
- `A0`: 0 to 3.00, step 0.05, default 0.50.
- `n`: 1 to 60, step 1, default 20.
- `s`: 0.25 to 5.00, step 0.25, default 1.00.
- `m`: 1% to 30%, step 1%, default 10%.
- `a`: 0.25 to 12 h, step 0.25, default 2.
- `r0`: 50% to 98%, step 1%, default 90%.
- `d`: 0 to 0.40, step 0.01, default 0.20 (show as points of retention).
- `b`: 1 to 48 h, step 1, default 8.
- Buttons: "Reset", "Patient players" (d = 0.10), "Better cosmetics" (A0 = 1.00), "Pricier skip" (s = 2.00).

**Numbers panel.** At the current `w`: `π`, ARPU, `r`, `L`, `LTV`. At the peak: `w*`, `LTV(w*)`, `L(w*)`, and "lifetime lost = 1 − L(w*)/L(0)" as a percent. Also the two sides of the optimum rule at the current `w`: `ARPU'/ARPU` and `c'/c` in percent per hour, where `c = 1 − r`, `ARPU' = n s m a / (w + a)²`, `c' = d b / (w + b)²`.

**Test values (defaults).**
- `w = 0`: π 0.00%, ARPU $0.50, r 90.00%, L 10.00, LTV $5.00.
- `w = 2`: π 5.00%, ARPU $1.50, r 86.00%, L 7.14, LTV $10.71.
- `w = 3.5`: π 6.36%, ARPU $1.77, r 83.91%, L 6.22, LTV $11.02.
- `w = 24`: π 9.23%, ARPU $2.35, r 75.00%, L 4.00, LTV $9.38.
- Peak: `w*` = 3.46 h, LTV $11.02, L 6.24 months, lifetime lost 37.6%. Both sides of the rule ≈ 7.6% per hour at `w*`.
- "Patient players" (d = 0.10): `w*` ≈ 6.90 h, LTV ≈ $14.02, L ≈ 6.83.
- "Better cosmetics" (A0 = 1.00): `w*` ≈ 2.31 h, LTV ≈ $14.31, L ≈ 6.91; LTV(0) = $10.00.
- "Pricier skip" (s = 2.00): `w*` ≈ 4.32 h, LTV ≈ $19.01, L ≈ 5.88.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. The peak marker and the shaded band have text labels. Charts have an accessible text summary updated on change ("LTV peaks at 3.46 hours; lifetime there is 6.24 months, 37.6% below no wall"). Respect `prefers-reduced-motion` and `prefers-color-scheme`. Caption: "Invented parameters for teaching; not any studio's data."

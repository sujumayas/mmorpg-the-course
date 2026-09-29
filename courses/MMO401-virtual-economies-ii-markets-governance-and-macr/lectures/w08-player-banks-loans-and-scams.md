# MMO401 · Week 08 — Player Banks, Loans and Scams

**Why this matters:** Give players a currency and a chat channel and some of them will start a bank. Many of those banks end with the founder walking off with the deposits. Whether that happens is not random. It follows from what your game enforces and what it leaves to trust, so you can predict it and design around it.

**You will be able to:**
- Compute the deposit level above which an unenforced banker gains more by stealing than by staying honest, and how it moves with spread, lending demand and the banker's horizon.
- Price a player loan from its default probability and collateral, and explain why unsecured lending barely exists in most games.
- Classify a scam by the trust gap it exploits and name the game-enforced tool that closes it.
- Critique a proposal for in-game banking or lending features against the cases of EVE Online, Second Life and Old School RuneScape.

**Before class:** Lehdonvirta & Castronova, *Virtual Economies: Design and Analysis* (MIT Press, 2014), the chapters 9-12 block, reading for institutions, trust and contract enforcement (about 30 pages). EVE University Wiki, "Scams" (about 15 minutes). Reread MMO303 week 10 on payoff matrices.

**Prerequisites from earlier courses:** [MA102 week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md) (a weekly chance `δ` gives an expected wait of `1/δ`). [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md). [MMO303 week 10, payoff matrices and Nash equilibria](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w10-game-theory-payoff-matrices-and-nash-equilibria.md). [MMO304 week 13, case studies](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w13-case-studies-eve-diablo-runescape-grand-exchange.md) (EVE's economy and its published data). [MMO304 week 11, real-money trade and gold farming](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w11-real-money-trade-and-gold-farming.md). This course: [week 7, taxes and fees](w07-taxes-and-fees-as-policy.md) (trades pushed off the market lose escrow), and [week 4, monetary policy tools](w04-monetary-policy-tools-in-games.md). Later: [week 11, premium currencies](w11-premium-currencies-and-exchange-rates.md).

**Interactive:** [The honest banker's ceiling](../examples/w08-honest-banker.html)

---

## 1. What a game enforces, and what it doesn't

A real bank rests on things no game provides by default: courts, deposit insurance, regulators and a banker who can be found and sued. Take those away and a bank is a promise. A depositor hands over money now for a promise of money later, and nothing but the banker's choice turns that promise into a payment.

Start by sorting every exchange in your game by one question: **does the server guarantee both halves?**

- An **atomic exchange** completes both halves at once or neither. A trade window where both players confirm, an auction house purchase, a buy order filled from escrow. Nobody needs to trust anybody.
- A **trust exchange** completes one half now and relies on a person for the other half later. "Give me your sword and I'll pay you tomorrow." "Deposit with my bank at 2% a week." "Lend me the materials and I'll give you the crafted item."

Every loan and every bank is a trust exchange, because time passes between the halves. And every scam in this lecture lives in a trust exchange or in a gap in how an atomic exchange is presented. That gives you the lecture's organizing idea. **A scam is what fills the gap between what players promise and what the server enforces.**

Two terms before the worked example. **Collateral** is property a borrower pledges that the lender gets if the borrower fails to pay. **Escrow** is money or items held by a neutral party (in games, the server) until conditions are met. Both turn trust exchanges back into something closer to atomic ones.

## 2. Worked example: when does an honest banker become a thief?

### The hook

In 2009 the CEO of EBank, a player-run bank in EVE Online, withdrew 200 billion ISK from its funds. He sold the ISK for real money, reported at about 6,100 Australian dollars (about US$4,590), and used it toward a house down payment and medical bills. CCP did not step in to undo the theft. In EVE, theft and fraud inside the game are treated as part of the world, and the EVE University Wiki's advice on player banks is blunt. Most of them have ended with someone walking off with the money.

So two questions. Why did EBank run honestly long enough to collect 200 billion ISK? And why did it stop? "The banker was a bad person" doesn't help you design anything. A model does.

### The model

A banker takes deposits `D`, measured in billions of ISK. They lend the money to players who need it (for ships, for trading stock), charge more interest than they pay depositors, and keep the difference.

- `s` is the banker's net spread per week on money that is lent out, after paying depositors and absorbing defaults. A spread of 2% means 1 billion lent earns the banker 0.02 billion a week.
- `L` is lending demand, the most that creditworthy borrowers will take at the bank's rate. Deposits above `L` sit idle and earn nothing.
- `δ` (delta) is the chance each week that the banker leaves the game for good: quits, burns out, or loses interest. From MA102 week 7, the expected number of weeks they have left is `1/δ`.
- `K` is the expected penalty for stealing: a ban, lost reputation that has in-game value, or legal risk. In EVE, for a purely in-game theft, `K` is close to 0.

Honest profit per week is `s × min(D, L)`. Over an expected `1/δ` weeks, the value of staying honest is

```
V = s × min(D, L) / δ
```

The value of stealing is everything in the vault now, less the penalty:

```
S = D − K
```

The banker stays honest while `V ≥ S`. Look at the two cases.

- While `D ≤ L`, every deposit is lent, so `V = s × D / δ`. Honesty holds when `s / δ ≥ 1 − K/D`. With `K = 0` that is simply `s ≥ δ`. The size of the bank doesn't matter.
- Once `D > L`, extra deposits add to `S` but not to `V`. Honesty holds only while

```
D ≤ D* = s × L / δ + K
```

`D*` is the **honesty ceiling**. Above it, the vault is worth more than the business.

### Numbers you can check

Take `s = 2%` a week, `δ = 1%` a week (an expected 100 weeks, about two years, left in the game), `L = 100` billion and `K = 0`.

| Deposits `D` (bn) | Lent out `min(D, L)` | Honest value `V = s × min(D, L) / δ` | Theft value `S = D` | `V − S` | Banker's best move |
|---|---|---|---|---|---|
| 20 | 20 | 40 | 20 | +20 | Honest |
| 50 | 50 | 100 | 50 | +50 | Honest |
| 100 | 100 | 200 | 100 | +100 | Honest |
| 150 | 100 | 200 | 150 | +50 | Honest |
| 200 | 100 | 200 | 200 | 0 | Indifferent |
| 300 | 100 | 200 | 300 | −100 | Steal |

`D* = 0.02 × 100 / 0.01 = 200` billion. The bank is safe until deposits pass twice the lending demand.

Now let the banker's horizon shrink. Nobody plays forever, and interest fades. Keep `s` and `L`, change `δ`:

| Weekly quit chance `δ` | Expected weeks left `1/δ` | Honesty ceiling `D*` (bn) |
|---|---|---|
| 1% | 100 | 200 |
| 2% | 50 | 100 |
| 3% | 33 | 0 (stealing pays at every size) |
| 4% | 25 | 0 (stealing pays at every size) |

At `δ = 2%` the spread exactly matches the quit chance, so the ceiling is `L` itself. Push `δ` past `s` and, with `K = 0`, the ceiling collapses to zero. Below `L` both `V = s × D / δ` and `S = D` grow in step, and `s / δ < 1` means the vault always wins, whatever the bank's size. A bank holding 150 billion is safe with a keen banker and unsafe with a tired one. Nothing about the deposits changed.

Finally, add growth. Successful banks attract deposits. Start at `D = 20` billion and let deposits grow 10% a week. Deposits reach `D* = 200` after `ln 10 / ln 1.1 ≈ 24` weeks. If the banker's `δ` drifts up to 2% on the way, the ceiling drops to 100 and the crossing comes at `ln 5 / ln 1.1 ≈ 17` weeks.

### The insight

The model says three things, and all three match the EBank story.

1. **A young, small bank can be honest for purely selfish reasons.** While its deposits are lent out and the banker plans to stay, the business is worth more than the vault. That is why player banks exist at all and why depositors are not simply fools.
2. **Success creates the theft.** Deposits keep arriving because the bank is trusted. Lending demand doesn't grow as fast. Past `D*`, the growth that looks like success is building a prize.
3. **The end of a player's career is the most dangerous week.** As `δ` rises, `D*` falls. A banker who is about to quit anyway has an expected future of nearly zero and a vault of everything. Exit scams cluster at the end of a career for the same reason.

Put the pieces together and "EBank ran honestly and then its CEO took 200 billion" needs no villain. It is the predicted path of an unenforced bank that grew.

### The visual

Open the interactive. The left panel plots deposits on the x-axis and value on the y-axis. The theft line `S = D − K` is a straight 45-degree line. The honest-value curve `V` rises along a steeper line until `D = L`, then goes flat. The region where `V ≥ S` is shaded as "honest", and the crossing point `D*` is labelled. The right panel plots deposits over time, growing at rate `g`, with a horizontal line at `D*` and a marker at the week they meet.

Drag `δ` up. On the left, nothing about the theft line changes, but the flat part of `V` drops and `D*` slides toward the origin. On the right, the week of the likely scam jumps closer. Now raise `K`, the enforcement penalty. The theft line drops and `D*` moves out. That is the designer's lever, and next you'll see three games that pulled it in different ways.

### Cross-game recognition

Rewrite each case into `V`, `S`, `D*` and `K`.

**EVE Online, EBank (2009).** `K ≈ 0` for theft inside the game, because CCP treats scams as part of the world and leaves them to players. The payoff `S` was larger than the in-game value of `D`, because the ISK could be sold for real money. That raises `S` for any bank whose currency has a cash price, which is a reason the real-money trade you studied in MMO304 week 11 makes every trust institution less stable. The model predicts that EVE's banks live until they outgrow their lending business or their founder's interest. The EVE University Wiki's observation that most of them end in theft fits.

**Second Life, Ginko Financial (2007).** Ginko offered Linden-dollar accounts at interest rates that at one point reached 0.145% a day, about 69.7% a year, funded by investments that were never disclosed. In our terms, the bank promised depositors more than any honest lending could earn, so its true `s` was negative and `V` was never positive. Nothing but new deposits could pay the interest. That is a **Ponzi scheme**: old depositors are paid with new depositors' money. After Linden Lab restricted in-world gambling in 2007, a run on Ginko followed and it failed, with remaining balances of about 200 million Linden dollars turned into bonds that were never going to be repaid. In January 2008 Linden Lab ruled that only organizations holding a real-world banking licence could offer interest-paying accounts. That rule is a very large `K`. It moved banking out of the game's trust layer and into real-world law.

**Old School RuneScape, "doubling money" and trust trades (current).** A player offers to double any coins you give them. To build credibility they double a small stake first, for example 20,000 to 50,000 coins, often with accomplices posing as happy customers, and then keep a large one. In model terms this is a bank with `L = 0` (no lending business at all) and `δ` near 1 (the scammer will vanish from this relationship immediately), so `V ≈ 0` and `D* ≈ K`. The small honest doubling is a cheap purchase of reputation to raise `D`. The difference from EVE is `K`. Old School RuneScape's Code of Conduct prohibits scamming, punishable by a mute or ban if reported, so `K` is the value of the account times the chance of being reported and caught. The Old School RuneScape Wiki's own advice is the design principle of this lecture. If a trade can be done in a single atomic trade, never split it into two.

**EVE Online, courier contracts (current).** Here the game itself turns a trust exchange into an enforced one. A player who wants cargo hauled posts a contract with a reward and a **collateral**. The hauler must place the collateral in escrow on accepting. If the package is opened, destroyed, or not delivered in time, the contract fails and the collateral is paid to the issuer. For the hauler, `S = cargo value − collateral`. Set collateral above the cargo's value and `S < 0`, so stealing never pays, whatever the hauler's `δ`. Notice that the tool creates a new scam in the other direction. An issuer sets collateral far above the cargo's value, sends it through dangerous space, and has the hauler destroyed to collect. Every enforcement tool you add moves the trust gap somewhere else.

### Eyes-open design judgment

- **Decide which exchanges the server guarantees.** Anything you leave to trust will develop scams in proportion to its value. Doing nothing is also a decision.
- **Enforcement raises `K`, and you have several ways to raise it.** Collateral and escrow (EVE contracts) make stealing unprofitable by construction. Rules and bans (Old School RuneScape) make it risky. Moving the activity under real law (Second Life after January 2008) makes it expensive. Each costs something: engineering time, support staff, or the freedom that makes EVE's political game possible.
- **A world where scams are legal can be a feature.** EVE's reputation for heists and betrayals draws players. That works because the game is built around risk and players accept it. Borrowing that stance for a casual game would produce angry players, not stories.
- **Cash-convertible currencies raise `S`.** When in-game money has a real price, every vault is worth more to a thief than its in-game use. Premium currencies and tokens (week 11) make this sharper.
- **Watch deposits relative to lending, not deposits alone.** If you allow player banks, a telemetry alert on "deposits held by one character far above anything they lend or spend" is a cheap early warning.

## 3. Pricing a loan

A player lending money faces two risks: the borrower may not pay, and the lender could have done something else with the money. Say the lender's alternative earns `r_0` per week (the best safe use of the money). The borrower defaults with probability `p`. If they default, the lender recovers `c` per unit lent from collateral. The loan rate `r` that makes lending break even in expectation solves

```
(1 − p) × (1 + r) + p × c = 1 + r_0
r = (1 + r_0 − p × c) / (1 − p) − 1
```

With `r_0 = 1%` a week:

| Default chance `p` | Collateral recovered `c` | Break-even weekly rate `r` |
|---|---|---|
| 2% | 0 | 3.1% |
| 5% | 0 | 6.3% |
| 5% | 0.8 | 2.1% |
| 10% | 0 | 12.2% |
| 10% | 0.8 | 3.3% |

Two things follow. First, unsecured loans in a game with anonymous players and a high `p` need weekly rates that look outrageous. At 10% default risk, 12% a week is the break-even, before any profit. Borrowers who accept such rates are more likely to be the ones planning to default, which pushes `p` higher still. Economists call this **adverse selection**, and it is why unsecured lending markets in games stay tiny.

Second, collateral does most of the work. Recovering 80% on default cuts the break-even rate from 12.2% to 3.3%. That is why the loans that do exist between players are almost always secured by something the lender can hold: an item left with them, a courier-style escrow, or a guild's reputation.

If you want lending in your game, the feature that matters is not an interest calculator. It is a way to hold collateral that the server releases automatically.

## 4. How a bank fails: runs and Ponzi arithmetic

A banker who is honest can still fail, because lent-out money can't be returned on demand. Suppose a bank keeps a **reserve ratio** `ρ` (rho), the share of deposits held as cash, and lends the rest. If depositors try to withdraw more than `ρ × D` in a short time, the bank can't pay. That is a **bank run**. Fear of a run can cause one, because depositors who think others will withdraw have a reason to withdraw first.

A Ponzi scheme is a bank that is always one run away from failing, and gets further from safety each week. Say it promises `r` per week on deposits, earns nothing, and takes 10 units of new deposits every week. Cash is everything ever deposited, `10t`. What it owes grows with compound interest, `10 × ((1 + r)^t − 1) / r`. The ratio of cash to what it owes is its effective reserve ratio.

| Weeks | Cash held | Owed at `r` = 1%/week | Reserve ratio | Owed at `r` = 5%/week | Reserve ratio |
|---|---|---|---|---|---|
| 10 | 100 | 104.6 | 96% | 125.8 | 80% |
| 20 | 200 | 220.2 | 91% | 330.7 | 60% |
| 40 | 400 | 488.9 | 82% | 1,208.0 | 33% |
| 52 | 520 | 677.7 | 77% | 2,328.6 | 22% |
| 104 | 1,040 | 1,814.6 | 57% | 31,768.1 | 3% |

Ginko's advertised 0.145% a day compounds to about 1.02% a week, close to the left-hand columns. At that rate a scheme with steady inflows looks healthy for months. The reserve ratio is still 77% after a year, so a few withdrawals are easy to pay. Any event that makes many depositors withdraw at once breaks it. In Ginko's case the trigger was the gambling restriction. The lesson for a designer is that a rule change aimed at something else can trigger a run on a player institution you never approved. Before a change, ask what player institutions depend on the activity you are restricting.

## 5. A taxonomy of scams by trust gap

Scams sort cleanly by the gap they exploit. The EVE University Wiki's scam list and Old School RuneScape's scam guide give plenty of cases. Group them by what the server did not guarantee.

| Trust gap | Examples | What closes it |
|---|---|---|
| Time: one half now, one later | Banks, loans, "doubling money", trust trades | Collateral, escrow, contracts the server settles |
| Presentation: the atomic exchange is real but misread | EVE contract tricks where the title or price looks different from the terms, items with similar names, a fitted ship listed without the ship | Clear UI, confirmation screens that restate the terms, warnings when the price is far from market |
| Identity: who am I dealing with | Impersonation of trusted players or staff | Verified names, rules against impersonation (EVE forbids it even though it allows most scams) |
| Institution: the organization holds shared assets | Corporation or guild theft after long infiltration | Role permissions and withdrawal limits on shared storage |

The table tells you where to spend. Engineering fixes (escrow, clear confirmation screens, withdrawal limits) close whole rows. Rules and bans close individual cases after the harm is done and need reports and staff.

## In-class activity (25 minutes)

Pairs. Your cooperative MMO wants a guild-bank lending feature so that veterans can fund new members' first crafting gear.

1. Choose what the server enforces: collateral, repayment schedule, what happens on default. One sentence each.
2. Using the loan table, set a maximum interest rate for your feature that still lets lenders break even at a 5% default rate with your collateral rule.
3. Write the honesty condition for the guild officer who controls the bank. What is `L`, what is `K`, and what is `D*` if the guild bank holds 20 times what members borrow in a week?
4. Name the new scam your feature enables.

Expected output: a four-line feature spec, a rate, a `D*` estimate, and one scam with a counter.

## Common misconceptions

- **"Bank scams happen because scammers are drawn to banking."** Honest founders become thieves when the vault outgrows the business or their interest in the game fades. The model predicts theft without assuming anyone started dishonest.
- **"High interest rates attract depositors, so they show a strong bank."** A rate above anything lending can earn means the interest is paid from new deposits. That is the Ponzi signature, as in Ginko's 0.145% a day.
- **"Adding collateral ends scams."** It removes one and creates another, as EVE's collateral gank scam shows.
- **"Banning scams makes a game safer at no cost."** It raises `K` but needs reports, investigation and staff, and it rules out the betrayal stories that some games rely on.

## Check yourself

1. A banker earns `s = 1.5%` a week on lent money, lending demand is 60 billion, and their weekly quit chance is 1%. What is `D*` with `K = 0`? With `K = 20` billion?
2. A different banker has the same spread and lending demand but a weekly quit chance of 3%. Their bank holds 40 billion, all lent. Is the banker honest with `K = 0`? With `K = 20` billion? Does the first answer depend on `D`?
3. A lender's safe alternative earns 0.5% a week. A borrower defaults 8% of the time and pledges collateral worth half the loan. What is the break-even weekly rate?
4. A scheme promises 3% a week, earns nothing and takes 10 units of deposits each week. What is its reserve ratio after 20 weeks?
5. A designer proposes letting players post "loan requests" that other players fill, with repayment on trust. Using the loan table and section 5, predict what the feature's default rate and interest rates will look like after a month, and propose one change.

<details>
<summary>Answers</summary>

1. `s ≥ δ`, so the bank is safe up to `L` and beyond. `D* = 0.015 × 60 / 0.01 = 90` billion. With `K = 20`, `D* = 110` billion.
2. With `D = 40 ≤ L = 60`, honesty needs `s / δ ≥ 1 − K / D`. With `K = 0`, `0.015 / 0.03 = 0.5 < 1`, so stealing pays. `V = 0.015 × 40 / 0.03 = 20` against `S = 40`. With `K = 20`, `S = 20 = V`, so the banker is exactly indifferent; the ceiling is `K / (1 − s/δ) = 20 / 0.5 = 40`. With `K = 0` the answer does not depend on `D`, because both `V` and `S` grow in proportion to `D` below `L`.
3. `r = (1.005 − 0.08 × 0.5) / 0.92 − 1 = 0.965 / 0.92 − 1 ≈ 4.9%` a week.
4. Owed `10 × (1.03^20 − 1) / 0.03 = 10 × 0.8061 / 0.03 ≈ 268.7`. Cash 200. Reserve ratio about 74%.
5. With no collateral and anonymous borrowers, `p` will be high. Break-even rates at 10% default are above 12% a week, which honest borrowers refuse, so the remaining borrowers are the ones least likely to repay. Rates rise, honest use collapses, and the feature becomes a scam channel. A server-held collateral slot, released on repayment or to the lender on default, fixes most of it.

</details>

## Lab / assignment hook

[Lab 08, the honesty ceiling](../labs/lab08.md). You will build a week-by-week spreadsheet or script of a player bank with random deposits, lending demand and a rising quit chance, find when the banker's best move flips, and test three enforcement rules. It counts toward the ABM labs (40%).

## Sources

- Wikipedia, "Eve Online" (checked September 2026). The 2009 EBank case: its CEO withdrew 200 billion ISK and converted it to about A$6,100 (US$4,590); the article notes such dangers are part of the virtual economy and are not dealt with by the developers.
- EVE University Wiki, "Scams" (current). Scam categories, including banks ("most banks in EVE have ended with someone walking off with the money"), Ponzi schemes, contract tricks and corporate theft; CCP permits most scams but forbids a listed set, including impersonation and scams involving real-life assets.
- EVE University Wiki, "Contracts" (current). Courier contracts: reward, collateral held in escrow, failure paying collateral to the issuer, advice to set collateral above cargo value, and the high-collateral gank scam.
- Wikipedia, "Ginko Financial" (checked September 2026). Second Life bank; rates reaching 0.145% a day (69.7% a year); failure in 2007 after in-world gambling was restricted; about 200 million Linden dollars converted to bonds; Linden Lab's January 2008 rule limiting interest-paying accounts to organizations with real-world banking licences.
- Old School RuneScape Wiki, "Scams" (current). Rule 2 of the Code of Conduct prohibits scamming (mute or ban if reported); doubling-money scheme with small initial doublings of 20,000 to 50,000 coins; trust trading; advice to never split a single trade into two.
- Lehdonvirta, V. & Castronova, E. (2014). *Virtual Economies: Design and Analysis*. MIT Press. Chapters 9-12: 9 "Institutions and Nonmarket Allocation", 10 "Money", 11 "Macroeconomic Design", 12 "Macroeconomic Management" (titles and order from the MIT Press chapter DOIs 10.7551/mitpress/9525.003.0010 to .0013 on Crossref, checked September 2026).

## Interactive spec: examples/w08-honest-banker.html

**The one insight:** a banker's honesty has a ceiling. Honest value stops growing once deposits exceed lending demand, while the value of stealing keeps growing, so a successful bank walks itself into theft, and the ceiling falls as the banker's interest fades.

**Layout.** Two linked panels, side by side on desktop, stacked on mobile (temptation chart first).

- Left panel, "Business against vault": x-axis deposits `D` from 0 to `max(3 × L, 1.5 × D*)` billion. Plot `S(D) = D − K` (solid straight line, labelled "Steal") and `V(D) = s × min(D, L) / δ` (solid, second style, labelled "Stay honest"). Shade where `V ≥ S` and label it "Honest is better". Vertical dashed line and label at `D*` when it exists. If `s ≥ δ` is false and `K = 0`, show the note "Stealing pays at every size" and shade nothing.
- Right panel, "Deposits over time": x-axis weeks 0 to 60. Deposits `D(w) = D0 × (1 + g)^w`. Horizontal line at `D*`. Marker and label at the first whole week where `D(w) > D*`. If "Fading interest" is on, `δ(w) = δ0 + Δδ × w` (capped at 1) and `D*(w)` is drawn as a falling curve instead of a line.

**Formulas.**

```
V(D)  = s × min(D, L) / δ
S(D)  = D − K
if s ≥ δ or K / (1 − s/δ) ≥ L:   D* = s × L / δ + K
otherwise:                         D* = K / (1 − s/δ)
week* = first w with D(w) > D*(w)
```

The second branch covers a banker whose spread is below their quit chance. They are honest only while the penalty outweighs the vault, even before deposits pass `L`. If `s < δ` and `K = 0`, `D* = 0`.

**Controls.**

- Spread `s`: 0% to 5% per week, step 0.1%, default 2%.
- Quit chance `δ0`: 0.5% to 10% per week, step 0.1%, default 1%.
- Lending demand `L`: 10 to 300 billion, default 100.
- Enforcement penalty `K`: 0 to 200 billion, default 0.
- Starting deposits `D0`: 1 to 100 billion, default 20. Growth `g`: 0% to 20% per week, default 10%.
- Toggle "Fading interest" with `Δδ`: 0 to 0.2 points per week, default 0.05.
- Presets: "EVE bank (no enforcement)" (defaults), "Tired banker" (`δ0` 4%), "Second Life after 2008" (`K` 200), "Doubling scam" (`L` 0, `δ0` 10%, `K` 1).

**Readout table** (copyable): `V` and `S` at the current `D0`, `D*`, `1/δ` in weeks, week*.

**Test values.**

- Defaults: `D*` = 200.0; at `D` = 150, `V` = 200, `S` = 150; at `D` = 300, `V` = 200, `S` = 300; week* = 25 (first whole week with `20 × 1.1^w > 200`; `w` = 24.16).
- `δ0` = 2%: `D*` = 100, week* = 17. `δ0` = 4% (preset "Tired banker"): `s < δ` and `K = 0`, so "Stealing pays at every size", `D*` = 0, week* = 0.
- `s` = 1.5%, `δ0` = 1%, `L` = 60, `K` = 0: `D*` = 90. With `K` = 20: `D*` = 110.
- `s` = 1.5%, `δ0` = 3%, `L` = 60, `K` = 0: "Stealing pays at every size". With `K` = 20: `D*` = 40 (second branch, `20 / (1 − 0.5)`).

**Accessibility.** Keyboard-operable sliders with visible focus, line styles and direct labels instead of colour alone, `prefers-reduced-motion` disables animated growth. No game logos or art.

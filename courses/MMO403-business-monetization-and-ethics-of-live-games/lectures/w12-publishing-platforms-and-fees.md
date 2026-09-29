# MMO403 · Week 12 — Publishing, Platforms and Fees

**Why this matters:** A player pays US$20 for your expansion. Before a dollar reaches your studio, a tax authority, a payment network, a store and possibly a publisher each take their share, in an order written into contracts you will sign. Headline rates like "30%" hide how those shares actually work, and a studio that plans its budget on the wrong base can be short by a third. This week you learn to trace the money from the player's wallet to your bank and to compare channels by what they actually leave you.

**You will be able to:**
- Compute a store's take under a tiered revenue share, and distinguish its marginal rate from its average rate.
- Build a revenue waterfall from consumer spend to studio receipts, including tax, refunds, store share, payment fees and a publisher's recoupment.
- Compare Steam, the Epic Games Store, the App Store, Google Play and a direct store with a card processor by writing each fee schedule in the same form, with the date it applied.
- Critique a channel or publishing proposal by computing the reach a lower-fee or lower-share option must make up, and name the non-fee rules (payments, pricing, exclusivity) that come with each platform.

**Before class:** Fields, T. & Cotton, B., *Social Game Design: Monetization Methods and Mechanics* (Morgan Kaufmann, 2011), the chapter on platforms and distribution. Read Valve's Steamworks announcement "New Revenue Share Tiers and other updates to the Steam Distribution Agreement" (30 November 2018, on the Steamworks Steam Community group), and skim Apple's "App Store Small Business Program" page.

**Prerequisites from earlier courses:** [MMO308 week 1, what live ops is](../../MMO308-live-operations-analytics-and-experimentation/lectures/w01-what-live-ops-is.md) (the live team as a running cost that fees must cover). [GS101 week 11, free-to-play, mobile and live service](../../GS101-history-and-critical-study-of-games/lectures/w11-free-to-play-mobile-and-live-service.md) (how stores and microtransactions changed the business). From this course, [week 1, business models](w01-business-models-box-subscription-f2p-hybrid.md), [week 10, pricing experiments](w10-pricing-experiments.md) (break-even lines, and Steam's discount cooldown), [week 11, subscription tokens](w11-subscription-tokens.md) (why a platform fee on the token changes its sign), [week 13, team and budget planning](w13-team-and-budget-planning.md) (which lists platform and payment fees as a budget line from this week), [week 2, unit economics](w02-unit-economics-ltv-cac-arppu.md), and [week 3, premium currencies](w03-premium-currencies.md) (currency packs).

**Interactive:** [w12-store-take.html](../examples/w12-store-take.html). Keep it open during section 2.

---

## 1. The money chain

Between a player's purchase and your studio's receipts there is a chain of parties. Name them before you model them.

- **Consumer spend** (or **gross bookings**). What players paid, including any tax in the price.
- **Tax.** Value-added tax (VAT) or sales tax. In many markets the store collects it and pays it to the government. In the UK, for example, the standard VAT rate is 20% and is included in the displayed price, so a £24.00 price contains `24 × 0.20 / 1.20 = £4.00` of VAT.
- **Refunds and chargebacks.** Money returned to players, either by the store's refund policy or by a card network after a dispute.
- **Net revenue.** Consumer spend after tax, refunds and chargebacks. Most store revenue shares are computed on some version of this. Valve, for example, pays on its monthly report, which it says includes deductions such as refunds, chargebacks and taxes. Always check the exact base in your agreement.
- **Store share** (or **platform fee**, **commission**). The store's percentage of net revenue.
- **Payment processing.** If you sell directly, a card processor charges per transaction. Stripe's standard US price, for example, is 2.9% plus 30 cents for a domestic card.
- **Publisher share.** If a publisher funded or marketed the game, it takes a share of what the store pays out.
- **Advance and recoupment.** An **advance** is money a publisher pays the studio before launch. **Recoupment** means the publisher keeps the studio's share of revenue until the advance, and often marketing costs, have been paid back. A **royalty** is what the studio receives after that.
- **Marginal and average rate.** The **marginal rate** is the share taken from the next dollar. The **average rate** is the total taken divided by the total earned. Tiered fee schedules make them differ, as income tax brackets do.

## 2. Worked example: what "30%" really means on Steam

### The hook

"Steam takes 30%" is the most repeated number in PC games business. It was true for every game until 2018. On 30 November 2018 Valve announced new revenue share tiers. From 1 October 2018, once a game makes more than US$10 million on Steam, the share becomes 75/25 on earnings beyond US$10 million, and 80/20 beyond US$50 million. The revenue that counts includes the game itself, DLC, in-game sales and Community Market fees.

So a big live game pays 20%? Take one that has earned US$30 million on Steam since the tiers began. It pays 25% on its next dollar. Its average, over all that revenue, is 26.7%. A game at US$100 million averages 23%. No game ever averages 20%, however large it grows. Two numbers are hiding behind "the rate", and budgets built on the wrong one are wrong by millions.

### The model

A **tiered (bracket) fee schedule** lists thresholds `b_1 < b_2 < …` and a rate `r_i` for the revenue inside each bracket, from `b_i` up to `b_(i+1)`.

```
take(G)       = Σ  r_i × max(0, min(G, b_(i+1)) − b_i)     summed over brackets i
average rate  = take(G) / G
marginal rate = r_i for the bracket that contains G
```

- `G` is the game's cumulative revenue on the store that counts toward the thresholds.
- `take(G)` is the store's total share.
- Steam, since October 2018: `b = 0, 10M, 50M` with `r = 30%, 25%, 20%`.

The average rate always lies between the first rate and the marginal rate, and it approaches the top rate only as `G` grows without limit. The same structure applies wherever a schedule says "X% up to a threshold, Y% after".

Some schedules are not brackets. They are **status rules**, where last year's revenue decides this year's rate for all revenue. Keep the two apart. A bracket never punishes you for crossing a threshold. A status rule can.

### Numbers you can check

The script computes Steam's take and the Epic Games Store's (0% on a game's first US$1 million, 12% after, from June 2025; see the cross-platform section) at several revenue levels. It also shows a card processor's fee on a direct store, which has its own shape: a percentage plus a fixed amount per purchase.

```python
STEAM = [(0, 0.30), (10e6, 0.25), (50e6, 0.20)]      # (bracket starts at, rate on revenue above it)
EPIC = [(0, 0.00), (1e6, 0.12)]

def take(gross, brackets):
    """Store's share when each rate applies only to revenue inside its bracket."""
    total = 0.0
    for i, (start, rate) in enumerate(brackets):
        end = brackets[i + 1][0] if i + 1 < len(brackets) else float("inf")
        if gross > start:
            total += rate * (min(gross, end) - start)
    return total

def card_fee(basket):
    """A typical card processor on your own store: 2.9% plus 30 cents per purchase."""
    return 0.029 * basket + 0.30

for g in (1e6, 5e6, 10e6, 30e6, 50e6, 100e6):
    s, e = take(g, STEAM), take(g, EPIC)
    print(f"gross ${g/1e6:>5.0f}M  Steam ${s/1e6:6.2f}M ({s/g:5.1%})  Epic ${e/1e6:5.2f}M ({e/g:5.1%})")
for b in (0.99, 4.99, 19.99, 99.99):
    print(f"basket ${b:6.2f}  card fee ${card_fee(b):.3f} ({card_fee(b)/b:5.1%})")
```

Output:

```
gross $    1M  Steam $  0.30M (30.0%)  Epic $ 0.00M ( 0.0%)
gross $    5M  Steam $  1.50M (30.0%)  Epic $ 0.48M ( 9.6%)
gross $   10M  Steam $  3.00M (30.0%)  Epic $ 1.08M (10.8%)
gross $   30M  Steam $  8.00M (26.7%)  Epic $ 3.48M (11.6%)
gross $   50M  Steam $ 13.00M (26.0%)  Epic $ 5.88M (11.8%)
gross $  100M  Steam $ 23.00M (23.0%)  Epic $11.88M (11.9%)
basket $  0.99  card fee $0.329 (33.2%)
basket $  4.99  card fee $0.445 ( 8.9%)
basket $ 19.99  card fee $0.880 ( 4.4%)
basket $ 99.99  card fee $3.200 ( 3.2%)
```

Check the US$30 million row by hand. The first US$10 million pays 30%, which is US$3 million. The next US$20 million pays 25%, which is US$5 million. The total is US$8 million, and `8 / 30 = 26.7%`. The marginal rate is 25%.

Three lessons.

1. **Budget with the average, decide with the marginal.** Your forecast of what Steam will keep uses the average rate at your forecast revenue. That average is the fee `f` in week 2's net ARPDAU, `a × (1 − f)`, so a game that will clear US$10 million should not plug in a flat 30% for its whole life. A decision about one more DLC or one more sale uses the marginal rate, because that is the rate on the extra revenue.
2. **Most games never leave the first bracket.** Below US$10 million, Steam's rate is 30% on every dollar. The tiers were announced as a way to reward, in Valve's words, the network effects of big games. They change nothing for small ones, and many smaller developers objected at the time for that reason.
3. **A fixed per-purchase fee punishes small baskets.** A 30-cent fixed charge takes a third of a US$0.99 purchase and 3% of a US$99.99 one. This is one reason games sell premium currency in bundles (week 3) rather than charging cards for every small item. The bundle turns many small purchases into one large one, and that bundle has its own ethical costs, which week 8 covers.

### A visual you can move

Open the interactive. The left chart plots the average take rate against lifetime revenue on a log axis from US$100,000 to US$500 million, with one line per store schedule. Steam's line is flat at 30% to US$10 million and then bends down toward 20% without reaching it. Epic's rises from 0% toward 12%. Epic's and Google's brackets restart each year, so read their lines as one year's revenue; Steam's tiers count a game's lifetime revenue. Apple's small-business line jumps when you toggle "eligible last year" off. The right chart is a waterfall for the revenue and channel you select. It shows consumer spend, then tax, refunds, store share, payment fees and publisher recoupment as steps down to "reaches the studio". Slide revenue across US$10 million and watch the marginal-rate marker on the left drop to 25% while the average barely moves.

### Cross-platform recognition

Each schedule below, written as brackets or as a status rule, with the date it applied. Platform terms change often. The dates are part of the fact.

**Epic Games Store (12% since launch in December 2018; 0% on the first US$1 million from June 2025).** Epic launched its store with a 12% share against Steam's 30%. From 1 June 2025 it takes no share of a product's first US$1 million of net revenue and 12% after. From 2026 the threshold resets every 1 January, so, like Google's, this is a bracket that restarts each year: `b = 0, 1M` with `r = 0%, 12%` on one year's revenue. The average rate on US$5 million in a year is 9.6%. A game that earns US$5 million a year for four years pays `4 × 0.48 = US$1.92M`, not the US$2.28M a lifetime bracket would give. Epic has also used its share as a bargaining tool. Its First Run program, announced 23 August 2023, waived Epic's share for six months in exchange for six months of store exclusivity.

**Google Play (help page as of September 2026).** In the markets Google lists as "remaining" (outside the EEA, UK and US), developers enrolled in the 15% tier pay 15% on the first US$1 million of annual earnings and 30% above. That is a bracket that resets each year: `b = 0, 1M` with `r = 15%, 30%`. From 30 June 2026 Google applies a different structure in the EEA, the UK and the US, a service fee plus a separate 5% billing fee when a purchase uses Google Play Billing, with rates that depend on whether the install is new or existing. Two schedules for one store, split by region and date, is now normal.

**Apple App Store Small Business Program (announced December 2020; page as of September 2026).** Developers whose total proceeds were no more than US$1 million in the prior calendar year pay 15%. If they pass US$1 million during the current year, the standard rate applies to future sales. The standard rate is 30%. This is a status rule with a bracket inside it. For an eligible developer earning US$3 million this year, the take is `0.15 × 1M + 0.30 × 2M = US$0.75M`, an average of 25%. The next year that developer is no longer eligible and pays 30% on everything, `US$0.90M` on the same US$3 million. Crossing the threshold costs more in the following year than in the year you cross it.

**A direct store with a card processor.** Stripe's standard US pricing is 2.9% plus 30 cents per successful domestic card charge, with 1.5% more for international cards and 1% more when currency conversion is needed. The shape is a straight line with a fixed intercept, not a bracket. The average rate depends on basket size rather than lifetime revenue. A direct store keeps far more per purchase than any platform. It also has to bring its own players, handle tax registration in every market, and run its own fraud and refund handling.

Four schedules, two shapes, plus a straight line. When you meet a new store's terms, write them in this form and compute the average rate at your forecast revenue and basket size before comparing headline percentages.

### Eyes-open design judgment

- **Compare channels by net per player and players reached, not by rate.** Net revenue is `reach × conversion × price × (1 − average rate)`. A store at 30% leaves 70 cents per dollar, and one at 12% leaves 88. The higher-fee store ties if it brings `0.88 / 0.70 = 1.26` times as many buyers. It is week 10's break-even line with the fee in place of the price.
- **Model the threshold you will actually cross.** A schedule that resets yearly (Google), counts lifetime revenue since a date (Steam), or depends on last year (Apple) rewards different launch and DLC timing. Put your revenue forecast by month into each schedule, not just the annual total.
- **Price small items knowing the fixed fee.** On a direct store, anything under about US$5 loses a large share to per-transaction fees. Bundle, or accept the loss knowingly.
- **Headline terms are only part of the deal.** Exclusivity, payment rules, pricing rules and featuring all come with the rate. The next sections treat them.

## 3. The full waterfall

Put the chain from section 1 in order for one year of an invented game. It sells on Steam, and a publisher funded it with a US$2.0 million advance and spent US$1.0 million on marketing. The publishing deal splits store receipts 50/50. The publisher recoups the US$3.0 million from the studio's half before paying the studio anything.

| Step | Amount (US$) | Left |
|---|---|---|
| Consumer spend, including tax | 11,000,000 | 11,000,000 |
| Tax (blended 10% of the pre-tax price) | −1,000,000 | 10,000,000 |
| Refunds and chargebacks (4%) | −400,000 | 9,600,000 |
| Steam share (30%, below US$10M) | −2,880,000 | 6,720,000 paid out to the publisher |
| Publisher's 50% | −3,360,000 | 3,360,000 studio's half |
| Recoupment of advance and marketing | −3,000,000 | 360,000 royalty paid to the studio |

The tax rate, refund rate and deal terms are invented for teaching. The Steam rate is the real first-bracket rate.

Read the table as a studio. Players spent US$11 million. The studio's royalty cheque for the year is US$360,000, about 3.3% of consumer spend. That looks brutal, but it leaves out the US$2 million advance the studio received before launch, which paid for development. Counting the advance, the studio has received US$2.36 million, about 21% of consumer spend. From the publisher's side, it spent US$3 million and received US$6.36 million, US$3.36 million of profit before its own costs.

Three details decide who comes out well.

**What recoups from what.** Here the advance recouped only from the studio's half. Some deals recoup from 100% of receipts before any split, which pays the publisher back faster and delays the studio's royalty. Some recoup marketing, some do not. On these numbers, recouping US$3 million from all receipts and then splitting the remaining US$3.72 million 50/50 would give the studio US$1.86 million instead of US$0.36 million. The contract clause matters more than the headline split.

**The base of each percentage.** "30%" and "50%" are both percentages of something. A share of consumer spend, of net revenue after tax and refunds, or of store payouts are three different amounts. Ask for the base in writing.

**Timing.** Valve pays about 30 days after the sales month. A publisher may pay quarterly, and royalties arrive only after recoupment. Week 13's runway model needs the dates, not only the totals.

## 4. What else comes with a platform

A store sells distribution, discovery, payments and trust. It also sets rules. Three kinds matter for live games.

**Payment rules.** Mobile stores have long required in-app purchases of digital goods to use the store's own billing. That is why the 30% applies to microtransactions, not only to the initial sale. The rules are under legal pressure and now differ by country. In the US, the Epic v. Apple case led to an injunction requiring Apple to let apps link to outside payment options. When Apple responded with a 27% commission on those linked purchases, the district court ruled in April 2025 that Apple had wilfully violated the injunction and barred it from charging on such purchases. Fortnite returned to the US App Store in May 2025. As of September 2026 the matter is not closed. The Supreme Court has agreed to hear Apple's appeal in its 2026 term, limited to the contempt question. Google Play's June 2026 structure, described above, is likewise a response to legal and regulatory change. Treat any payment-rule assumption in a business plan as "as of" a date and name the risk.

**Pricing rules.** Stores constrain prices as well as taking a share of them. Week 10 met Steam's 30-day discount cooldown after a price increase. Stores set minimum prices and price tiers, and in the EU the 30-day prior-price rule governs any announced reduction. A live game planning weekly offers across three stores has to satisfy three rulebooks.

**Premium currency across platforms.** A cross-platform MMO faces a specific question. If a player buys premium currency on one platform, can they spend it on another? Every platform wants its share of purchases made in its store, and players want one wallet. Whatever you decide, the currency's dollar value per unit now differs by where it was bought, because the net after fees differs. Record the purchase channel on every unit of premium currency, or you will not be able to compute revenue per player by channel.

**Exclusivity and publishing deals.** A store or publisher may pay you, lower its share, or fund marketing in exchange for exclusivity or a share of revenue. Evaluate it with the same waterfall. Estimate the net you would earn without the deal, the net with it (including the lost reach during exclusivity), and the money that arrives earlier. A publisher's advance is also insurance. If the game fails, a studio usually keeps the advance, because advances are typically recoupable only from revenue and not repayable. That risk transfer is what the publisher's share pays for, and it is worth a lot to a small studio with three months of runway.

## In-class activity (25 minutes)

In groups of three, you plan distribution for a PC MMO expansion priced at US$29.99. Forecast: 400,000 copies in year one if sold on Steam alone.

1. Compute Steam's take and average rate on the forecast (ignore tax and refunds). Is the game in the first bracket for all of it?
2. The Epic Games Store offers the same 12% schedule with the June 2025 first-million rule. How many copies must sell there to earn the same net as 400,000 copies on Steam, if Epic were the only store?
3. Your own launcher charges cards 2.9% plus 30 cents. How many direct sales equal the same net? What else would the launcher cost you?
4. A publisher offers a US$1.5 million advance, 50/50 split of store receipts, recoupment from the studio's half. Compute the studio's year-one royalty on the Steam-only forecast.

Expected output: a short table with gross, take, average rate and net for each option, the break-even copy counts, the royalty, and a one-paragraph recommendation. (Check: 400,000 × US$29.99 = US$11.996 million; Steam takes US$3.499 million, an average of about 29.2%, leaving US$8.497 million.)

## Common misconceptions

- **"Big games pay Steam 20%."** They pay 20% on revenue above US$50 million. The average rate stays above 20% at any size, 23% at US$100 million.
- **"A lower store fee always means more money."** Net depends on reach. A store at 30% ties with one at 12% if it brings 1.26 times as many buyers.
- **"The studio gets the publisher's split of revenue."** It gets its split minus recoupment, and the recoupment clause can move the studio's year-one receipts by a factor of five, as section 3 showed.
- **"Platform terms are fixed facts."** They changed for Steam in 2018, Epic in 2025, Google in 2026 and Apple's US link-out rules in 2025. Always cite the date of the terms you use.

## Check yourself

1. A game has earned US$60 million on Steam since October 2018. What is Steam's total take, the average rate, and the marginal rate?
2. A developer eligible for Apple's Small Business Program earns US$1.8 million this year. What does Apple take this year? What would it take on the same revenue next year?
3. On a direct store with a 2.9% plus 30-cent card fee, at what basket size does the fee reach exactly 5% of the purchase?
4. In section 3's waterfall, the publisher offers to recoup from 100% of Steam payouts before a 60/40 split in the studio's favor. Compute the studio's royalty and compare it with the original deal.

<details>
<summary>Answers</summary>

1. `0.30 × 10M + 0.25 × 40M + 0.20 × 10M = 3M + 10M + 2M = US$15M`. Average `15 / 60 = 25%`. Marginal 20%.
2. This year: `0.15 × 1M + 0.30 × 0.8M = US$0.39M` (21.7%). Next year, not eligible: `0.30 × 1.8M = US$0.54M` (30%).
3. Solve `0.029 × b + 0.30 = 0.05 × b`, so `0.021 × b = 0.30` and `b = US$14.29`.
4. Payouts US$6.72M, minus US$3.0M recouped first, leaves US$3.72M. The studio's 60% is US$2.232M, against US$0.36M in the original deal. The publisher receives US$3.0M plus US$1.488M. The new deal is far better for the studio in year one.

</details>

## Lab / assignment hook

[Lab 12, the revenue waterfall](../labs/lab12.md). You code the bracket and status fee schedules from this lecture into a small library, run a year of an invented game's monthly sales through four channels and two publishing deals, and write a channel recommendation. The waterfall feeds the business plan in week 15 (40%) and counts toward the models component (40%).

## Sources

- Valve, "New Revenue Share Tiers and other updates to the Steam Distribution Agreement", Steamworks Steam Community group announcement, 30 November 2018. Tiers from 1 October 2018: 75/25 on earnings beyond US$10M and 80/20 beyond US$50M; revenue includes packages, DLC, in-game sales and Community Market game fees; the network-effects rationale.
- Valve, Steamworks Documentation, "Reporting and Payments" (accessed September 2026). Payment about 30 days after the sales month; the monthly report includes deductions such as refunds, chargebacks and taxes; US$100 minimum payout.
- Wikipedia, "Steam (service)" (accessed September 2026). Flat 30% before the tiers; reaction from smaller developers to the 2018 change.
- Epic Games, "Epic Games Store Updates Revenue Share: Keep 100% of the First $1M Per Product, Per Year" (store.epicgames.com news, June 2025, read via the Internet Archive copy of 4 June 2025). 100% to the developer on the first US$1 million of net revenue per product per year, retroactive from 1 June 2025, 88/12 after; the threshold resets on 1 January each year from 2026.
- Wikipedia, "Epic Games Store" (accessed September 2026). 12% share at launch (December 2018); First Run exclusivity program announced 23 August 2023.
- Google, Play Console Help, "Service fees" (answer 112622, accessed September 2026). 15% on the first US$1M of annual earnings and 30% above for enrolled developers in remaining markets; from 30 June 2026 a service fee plus a 5% billing fee in the EEA, UK and US, differing for new and existing installs.
- Apple, "App Store Small Business Program", developer.apple.com (accessed September 2026). 15% for developers with no more than US$1M in proceeds in the prior calendar year; standard rate on future sales after passing US$1M; re-qualification rule. Wikipedia, "App Store (Apple)" (accessed September 2026). Standard 30% commission; program announced December 2020.
- Wikipedia, "Epic Games v. Apple" (accessed September 2026). April 2025 contempt ruling barring commission on linked purchases; Fortnite's return to the US App Store in May 2025; Supreme Court certiorari for the 2026 term limited to the contempt question.
- Stripe, "Pricing" (accessed September 2026). 2.9% plus 30 cents per successful domestic card charge; plus 1.5% for international cards and 1% for currency conversion.
- GOV.UK, "VAT rates" (accessed September 2026). Standard rate 20%.
- Fields, T. & Cotton, B. (2011). *Social Game Design: Monetization Methods and Mechanics*. Morgan Kaufmann.

## Interactive spec: examples/w12-store-take.html

**The one insight:** a tiered fee schedule has a marginal rate and an average rate, and the average stays well above the headline top rate. A fixed per-purchase fee makes the rate depend on basket size instead. Laid out as a waterfall, the store fee is often not the largest deduction between the player's wallet and the studio.

**Layout.** Two panels side by side on desktop, stacked on mobile (rate chart first). Readout table below.

**Left panel: average take rate against revenue.** x-axis lifetime (or annual) revenue on a log scale from US$100,000 to US$500 million. y-axis 0% to 35%. One line per schedule:
- Steam: brackets `0, 10M, 50M` at `30%, 25%, 20%`.
- Epic: brackets `0, 1M` at `0%, 12%`.
- Google Play, remaining markets: brackets `0, 1M` at `15%, 30%`.
- Apple Small Business Program: if "eligible last year" is on, brackets `0, 1M` at `15%, 30%`; if off, flat `30%`.
- Direct store: flat `2.9% + 0.30 / basket`, using the basket slider.
A vertical marker at the selected revenue shows each line's average rate. A second, dashed marker set shows each schedule's marginal rate at that revenue.

**Right panel: waterfall.** Bars for consumer spend, tax, refunds and chargebacks, store share (for the selected channel, computed with that channel's schedule on net revenue), payment fees (direct store only), publisher share, recoupment, and "reaches the studio". Each bar is labelled with its dollar amount and its share of consumer spend.

**Controls.**
- Revenue (net of tax and refunds) `G`: US$100,000 to US$500 million, log slider, default US$9.6 million.
- Channel: Steam, Epic, Google Play (remaining markets), Apple (eligible last year: toggle), Direct store.
- Basket size: US$0.99 to US$99.99, default US$19.99 (direct store only).
- Tax rate: 0% to 27%, default 10% (applied as `spend = G_pre_refund × (1 + tax)`).
- Refund and chargeback rate: 0% to 15%, default 4%.
- Publisher: toggle, split to studio 0% to 100% (default 50%), recoupable amount US$0 to US$10 million (default US$3 million), recoup base "studio's half" or "all receipts".

**Readout table** (copyable). Consumer spend, tax, refunds, net revenue `G`, store take, average and marginal store rate, payment fees, publisher share, recoupment, studio receipts, and studio receipts as a share of consumer spend.

**Test values.**
- Steam, `G = 30M`: take US$8.00M, average 26.7%, marginal 25%. `G = 100M`: take US$23.00M, 23.0%.
- Epic, `G = 5M`: take US$0.48M, 9.6%.
- Apple eligible, `G = 3M`: take US$0.75M, 25.0%. Not eligible: US$0.90M, 30.0%.
- Direct, basket US$0.99: 33.2%. Basket US$19.99: 4.4%.
- Section 3 waterfall (Steam, tax 10%, refunds 4%, `G` = US$9.6M, publisher 50%, recoup US$3M from the studio's half): consumer spend US$11.0M, store take US$2.88M, studio receipts US$0.36M (3.3%). Switch the recoup base to "all receipts": studio receipts US$1.86M.

**Accessibility.** Keyboard-operable controls with visible focus. Lines are distinguished by dash pattern and direct labels, not only color. Waterfall bars carry text labels. No animation under `prefers-reduced-motion`. Uses the shared palette tokens.

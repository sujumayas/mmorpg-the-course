# MMO403 · Week 13 — Team and Budget Planning

**Why this matters:** Every monetization model you built this term pays for one thing, a team of people working month after month. If you cannot say what that team costs per month, how long your money lasts and what a two-month slip does to the total, you cannot tell a funder (or yourself) whether your business model works. Most MMO projects that die in development run out of months before they run out of ideas.

**You will be able to:**
- Compute a monthly burn rate from a staffing plan, a loaded cost per head-month and fixed costs, and turn it into a total budget and a runway.
- Compute the cost of a schedule slip in each phase and explain why late slips cost several times more than early ones.
- Rewrite published studio figures (Cloud Imperium Games 2024, Camelot Unchained's Kickstarter) into the same burn model and state what they do and do not tell you.
- Design a phased team plan with a contingency and a cut list, and defend it against a slip scenario.

**Before class:** Fields & Cotton, *Social Game Design: Monetization Methods and Mechanics* (Morgan Kaufmann, 2011), skim the book's material on metrics and running a game as a business. Cloud Imperium Games, "CFO comment on the 2024 accounting" (cloudimperiumgames.com, about 15 minutes; read the cost and headcount sections). Reread [PR101 week 1, roles on a game team](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w01-roles-on-a-game-team.md), section 2.

**Prerequisites from earlier courses:** [MMO308 week 1, what live ops is](../../MMO308-live-operations-analytics-and-experimentation/lectures/w01-what-live-ops-is.md) (the live team and its levers). [MMO308 week 14, sunsetting](../../MMO308-live-operations-analytics-and-experimentation/lectures/w14-sunsetting-content-and-servers.md) (the month a live game stops covering its costs; this week builds the cost side of that crossing). [PR101 week 4, scope and cut lists](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md). [MMO302 week 13, cloud deployment](../../MMO302-mmo-server-architecture/lectures/w13-cloud-deployment-and-autoscaling.md) (where the server line of the budget comes from). [MMO403 week 1, business models](w01-business-models-box-subscription-f2p-hybrid.md) (contribution and cost to serve). [MMO403 week 2, unit economics](w02-unit-economics-ltv-cac-arppu.md) (LTV and CAC, the revenue side of this week's plan).

**Interactive:** [w13-burn-and-runway.html](../examples/w13-burn-and-runway.html). Keep it open during section 2.

---

## 1. A game budget is mostly people-months

Ask a producer what an MMO costs and the honest first answer is "how many people, for how many months?" Almost everything else in the budget either scales with the team (desks, laptops, software seats, payroll taxes) or is small next to it until launch (servers, marketing). So the budget starts with four terms.

- **Headcount** is the number of people on the team in a given month. It changes by phase.
- **Loaded cost** is what one person costs the studio per month, not what they are paid. It adds employer taxes, pensions or health insurance, equipment, software licences, office space and a share of management and support staff. In most studios the loaded cost is well above the salary. Use a figure for your region and say where it came from.
- **Burn rate** (or just "burn") is total spending per month: headcount times loaded cost, plus fixed costs that do not depend on headcount.
- **Runway** is how many months of burn your cash covers: cash divided by burn.

A **head-month** is one person working for one month. It is the unit producers budget in, because it makes teams of different sizes comparable. Twelve people for six months is 72 head-months, and so is six people for twelve months (though, as section 3 shows, the two plans do not finish at the same time).

This course uses round, invented numbers so you can check them by hand. We assume a loaded cost of $10,000 per head-month and $50,000 a month of fixed costs (build servers, tools, licences, rent that does not grow with the team). These are teaching assumptions, not market rates. Your lab asks you to replace them with numbers you can source.

## 2. Worked example: the phase budget and the price of a slip

### The hook

In April 2013, City State Entertainment put Camelot Unchained, a realm-versus-realm MMO, on Kickstarter with a $2,000,000 goal. By the close on 2 May 2013 it had raised $2,232,933 from 14,873 backers. Alpha testing started in March 2015. A planned 2015 beta slipped by about three years after the team decided to rebuild the ability system, and Beta 1 opened on 31 July 2018. The game entered Steam Early Access on 2 June 2026, thirteen years after the campaign.

Backers lived that wait. The puzzle for a business student is a different one. How long does $2.2 million last on an MMO team? And why does a delay in the middle of a project hurt so much more than one at the start?

### The model

Split the project into phases. Each phase `p` has a length `m_p` in months and a headcount `n_p`. Then:

```
burn in phase p:        B_p = n_p × c + F
total budget:           S   = Σ_p  m_p × B_p
runway at any moment:   R   = cash remaining / B_now
cost of a slip:         ΔS  = Δ × B_p     (Δ extra months in phase p)
```

- `c` is the loaded cost per head-month.
- `F` is the fixed monthly cost.
- `B_now` is the burn of the phase you are in.
- `Δ` is the length of the slip in months.

The last line is the one to remember. **A month of delay costs the burn of the month in which it happens.** A slip in a phase with 12 people costs the burn of 12 people. The same slip when 60 people are on the team costs the burn of 60.

### Numbers you can check

Take a 30-month plan for a mid-sized MMO, with `c = $10,000` and `F = $50,000`.

| Phase | Months | Headcount | Burn per month | Phase cost | Spent by end of phase |
|---|---|---|---|---|---|
| Pre-production | 6 | 12 | $170,000 | $1,020,000 | $1,020,000 |
| Production | 18 | 45 | $500,000 | $9,000,000 | $10,020,000 |
| Beta and launch | 6 | 60 | $650,000 | $3,900,000 | $13,920,000 |

Check one row by hand. Production burn is `45 × 10,000 + 50,000 = 500,000`, and 18 months of it is $9.0 million.

Now suppose the studio raised $15 million. The plan leaves $1.08 million unspent, which looks like a safe margin. Add a three-month slip to each phase in turn:

| 3-month slip in | Extra cost | New total | Cash runs out in month |
|---|---|---|---|
| Pre-production | $510,000 | $14,430,000 | never (plan finishes in month 33) |
| Production | $1,500,000 | $15,420,000 | 33 (the last month) |
| Beta and launch | $1,950,000 | $15,870,000 | 32 (one month before the plan ends) |

The same three months cost almost four times as much in beta as in pre-production. A slip in pre-production fits inside the margin. A slip in beta sinks the plan two months short of launch. Nothing about the team's skill changed between those rows. Only the phase did.

Here is the same calculation in Python. It runs as shown with `.venv/bin/python` and prints the rows above.

```python
PLAN = [  # (phase, months, headcount)
    ("pre-production", 6, 12),
    ("production", 18, 45),
    ("beta and launch", 6, 60),
]
COST = 10_000    # loaded cost per head-month, dollars
FIXED = 50_000   # servers, tools, licences, rent per month, dollars


def burn_series(plan, cost=COST, fixed=FIXED):
    """Monthly burn, one entry per month of the plan."""
    series = []
    for phase, months, heads in plan:
        series += [heads * cost + fixed] * months
    return series


def cash_out_month(series, cash):
    """First month in which cumulative spend exceeds cash, or None."""
    spent = 0
    for month, burn in enumerate(series, start=1):
        spent += burn
        if spent > cash:
            return month
    return None


def slip(plan, phase_name, extra):
    """The same plan with `extra` months added to one phase."""
    return [(p, m + extra if p == phase_name else m, h) for p, m, h in plan]


base = burn_series(PLAN)
print(f"total {sum(base):,}  months {len(base)}  cash-out at $15M: {cash_out_month(base, 15_000_000)}")
for phase, _, _ in PLAN:
    s = burn_series(slip(PLAN, phase, 3))
    print(f"3-month slip in {phase:16s} extra {sum(s) - sum(base):>9,}  cash-out: {cash_out_month(s, 15_000_000)}")
```

Output:

```
total 13,920,000  months 30  cash-out at $15M: None
3-month slip in pre-production   extra   510,000  cash-out: None
3-month slip in production       extra 1,500,000  cash-out: 33
3-month slip in beta and launch  extra 1,950,000  cash-out: 32
```

### Back to the hook

Now read Camelot Unchained's Kickstarter through the model. At our pre-production burn of $170,000 a month, $2,232,933 lasts about 13 months. At our production burn of $500,000 it lasts under five. Put another way, at $10,000 per head-month it buys about 223 head-months, roughly 18 people for one year.

The campaign was never the whole budget. The studio kept taking pledges on its own site after Kickstarter closed, and public summaries of the project (Wikipedia, September 2026) report about $4.5 million in total crowdfunding, $5 million from founder Mark Jacobs and $7.5 million from an investor in 2018, about $17 million in all. Treat those as reported figures, not audited ones. Spread $17 million over the thirteen years from campaign to Early Access and you get about $109,000 a month. At $10,000 per head-month that pays for about eleven people with nothing left for fixed costs, or about six once you set aside our $50,000 a month of fixed costs. That is an implied average under our assumptions, not the studio's actual headcount, which we do not know. It does explain the shape of what backers saw. A small team takes many years to build an MMO, and a three-year rework in the middle (the ability system) adds three years of burn without adding any revenue.

### Move it yourself

Open the interactive. The left panel is the staffing plan, a stacked area of headcount by month, coloured by phase. The right panel is cumulative spend against a horizontal line for cash raised. Drag the slip slider and move the slip between phases. On the left, the plan just gets wider. On the right, the spend line steepens in the late phases, so the same slip pushes it through the cash line only when it lands late. Turn on the contingency toggle to see how much slip a 20% reserve absorbs in each phase.

### Cross-game recognition

**Cloud Imperium Games, 2024 accounts (Star Citizen and Squadron 42).** The studio publishes a yearly cost summary. For 2024 it reported total trading costs of $152.9 million, of which salaries and related on-costs were $71.4 million, publishing, community and marketing $37.5 million, and other overheads $36.7 million. Year-end headcount was 1,031 (the company notes this is a year-end count, not an average). Rewrite it into the model:

- Monthly burn `B = 152.9 / 12 ≈ $12.7 million`.
- All-in cost per head-month `≈ 152,900,000 / 1,031 / 12 ≈ $12,400`.
- Salaries are only 47% of trading costs. The other 53% is the "F" and the non-salary part of "c" in our model.

Two lessons carry over to your own plans. First, a budget built from salaries alone would miss about half of this studio's spending. Second, a burn figure with no cash figure does not give you runway. The CFO report gives income ($146.6 million) and a loss of $14.3 million after capital spending (an EBITDA loss of $6.3 million), which tells you the gap per year, about $1.2 million a month, but not how many months of cash remain. Separately, the company's crowdfunding tracker passed $1.04 billion in lifetime pledges by September 2026.

**Final Fantasy XIV, 2010 to 2013.** The original game launched on 30 September 2010 to a poor reception. Square Enix suspended subscription fees, and from December 2010 Naoki Yoshida's team kept patching the live game while rebuilding a replacement from scratch. The original servers closed on 11 November 2012, and A Realm Reborn launched in August 2013. In our model this is the most expensive shape a project can take. There are two burns at once, `B = B_live + B_rebuild`, and for a long stretch revenue from subscriptions was switched off. MMO407 week 4 works through this case and the patch-or-rebuild decision in depth ([MMO407 week 4](../../MMO407-launch-scaling-and-post-mortems/lectures/w04-case-ffxiv-1-0-to-a-realm-reborn.md)). Here you only need the budget reading. A rebuild doubles burn for its whole length.

**Hytale, 2025.** Riot Games cancelled Hytale in June 2025. On 17 November 2025 the original co-founders announced they had bought it back, rehired more than 30 developers and committed personal funding for the next ten years. That is the runway equation run backwards. If you know the months you want (`R = 120`) and the burn of your team, the cash you need is `R × B`. A 30-person team at our assumed rates is `30 × 10,000 + 50,000 = $350,000` a month, so ten years is $42 million before any revenue. The studio did not publish its costs, so this is a check on scale, not a claim about Hytale's real budget. The game reached Early Access on 13 January 2026, which gave it revenue two months after the buyback.

Three very different studios, one equation. When you read any studio's funding news, rewrite it as cash, burn and months, and ask which of the three is missing.

### Eyes-open design judgment

The phase model is a planning tool, not a forecast. Use it with these trade-offs in view.

- **Its strength is that it makes timing visible.** A spreadsheet total hides the fact that the last third of the schedule carries half the cost. Always show the cumulative curve next to the total.
- **Flat phases are a simplification.** Real teams ramp up over months, and people roll off one by one. A ramp spreads the cost of a slip, but it does not change the main lesson. Late months are expensive months.
- **Slips are not independent of phase.** Problems found late (performance at scale, server load, a broken economy) take longer to fix than problems found early. Your model should put its largest contingency where the burn is highest and the unknowns are the least tested.
- **The model has no revenue.** For a live game, a slip also moves the first revenue month back. MMO403 week 2 gives you the lifetime value of a player, and a late launch loses those months of every cohort's value too. Include both costs when you argue about a delay.

## 3. Shaping the team

### Why not hire 60 people on day one?

If late slips are so expensive, why not staff up early and finish sooner? Three reasons.

First, a large team with no settled design produces work that gets thrown away. Pre-production exists to answer the questions (core loop, tech risks, art direction) that decide what 45 people will build. PR101 week 4 called the answer to those questions a vertical slice. It is cheaper to find the answers with 12 people.

Second, hiring takes months, and new people are not at full output on arrival. They need onboarding, and someone on the team has to mentor them.

Third, communication cost grows faster than headcount. PR101 week 1 showed that a team of `n` people has `n(n − 1)/2` possible pairs to keep in sync. Going from 12 to 45 people multiplies those channels by about 15. Studios manage this by splitting into sub-teams with clear owners, which adds leads and producers to the headcount.

### Buying back a slip costs more than the slip

Frederick Brooks argued in *The Mythical Man-Month* (1975) that adding people to a late software project makes it later. The claim is strongest near the end of a project. Earlier on, adding people can help, but at a price. Work it through with the plan from section 2.

At the end of month 12 of production, the team finds it is three months behind. That is `3 × 45 = 135` head-months of missing work, with 12 months left in the phase. The producer proposes hiring 15 people now. Assume each new hire works at 50% for their first three months, and each one costs an existing team member 20% of their time for those three months.

```
output from new hires   = 15 × (3 × 0.5 + 9 × 1.0) = 157.5 head-months
mentoring cost          = 15 × 3 × 0.2           =   9.0 head-months
net extra output        = 148.5 head-months   (enough to cover 135)
cost of the new hires   = 15 × 12 × $10,000      = $1,800,000
cost of just slipping   = 3 × $500,000           = $1,500,000
```

Under these assumptions, hiring keeps the date but costs $300,000 more than accepting the slip. It is worth it only if the launch date carries value, such as a marketing window, a platform feature slot or revenue three months sooner. With worse assumptions (hiring takes two months, new hires reach full speed after six) the hires never catch up. That is Brooks's point.

### The live team

After launch, the team does not go to zero. A live MMO keeps content designers, live-ops and economy staff, engineers on call, community managers and customer support. MMO308 week 1 described what that team does. For budgeting, the live team is a new phase with its own `n` and a burn that must be covered by revenue. MMO308 week 14 showed how to find the month when revenue falls below that burn. The lower you can make the live burn, the longer the game lives.

## 4. What else goes in the budget

Headcount is the largest line but not the only one. A complete MMO budget also has these lines. Each is either part of `F` or a one-off cost in a particular month.

| Line | Scales with | Where you learned to size it |
|---|---|---|
| Servers and hosting | players (after launch), builds and tests (before) | MMO302 week 13 |
| Platform and payment fees | revenue | MMO403 week 12 |
| Customer support and community | players | MMO308 weeks 1 and 10 |
| Marketing and user acquisition | the launch plan | MMO403 week 2 (CAC) |
| External services (localisation, motion capture, audio, QA vendors) | content volume | this week |
| Age ratings, legal review, payment and consumer-law compliance | markets you sell in | MMO403 weeks 6 and 7 |
| Contingency | risk | this week |

**Contingency** is a reserve kept out of the phase plan for things you know will go wrong but cannot name yet. It is not padding. Padding hides inside estimates, where nobody can see or manage it. A contingency is a visible line with an owner and a rule for spending it. A common practice is to hold 10 to 25% of the build budget, set by how many untested risks remain. That range is a planning convention, not a law. On the section 2 plan, 20% of $13.92 million is $2.78 million, about 5.6 months of production burn or 4.3 months of beta burn. Note how the same reserve buys fewer months the later you spend it.

**A cut list** is the other half of contingency. It is the list of features you will drop, in order, if the money or the months run short. PR101 week 4 introduced it for jams. For an MMO it might read "housing to post-launch, second starting zone cut, crafting tier 5 cut, one fewer raid at launch". A cut list turns a funding shortfall into a smaller game instead of a dead one.

### Crunch is an unbudgeted line

When a plan is short of months, teams are often pushed to work longer hours instead of cutting scope or moving the date. In budget terms, crunch is borrowing head-months from the team without paying for them, and the loan is repaid in mistakes, sick leave and people quitting after launch. That last cost lands in the live phase, exactly when you need experienced people most. PR101 week 12 covers the causes and the evidence ([PR101 week 12, crunch](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w12-crunch-causes-costs-alternatives.md)). As a business planner, the defensible position is simple. If your plan works only with sustained overtime, the plan is wrong. Fix it with the cut list, the contingency or the date.

## In-class activity (25 minutes)

In groups of three, you are the producer, finance lead and design lead of a studio pitching a small sandbox MMO. You have $8 million.

1. Draft three phases with months and headcount. Use `c = $10,000` and `F = $40,000`. Your plan must spend no more than $6.5 million, leaving the rest as contingency. (8 min)
2. Compute burn per phase, total, and the contingency as months of production burn. (5 min)
3. The instructor draws a card: "server tech needs a rewrite, 4 months, found in month 14". Decide which phase absorbs it, compute the extra cost, and state whether you spend contingency, cut features (name them), hire, or move the date. (8 min)
4. Swap sheets with another group and find the one assumption in their plan most likely to be wrong. (4 min)

Expected output: a one-page table of phases and burns, the slip cost, your decision with numbers, and the other group's weak assumption.

## Common misconceptions

- **"The budget is the salaries."** Salaries were 47% of Cloud Imperium's 2024 trading costs. Loaded cost, overheads, marketing and publishing operations make up the rest, and a plan built from salaries alone runs out of money early.
- **"A three-month delay costs three months of average spend."** It costs three months of the burn in the phase where it happens. Late slips in the section 2 plan cost almost four times early ones.
- **"If we're late, add people."** Adding people costs more than the slip and helps only if they arrive early enough to reach full speed. Near the end it makes things later.
- **"The crowdfunding total is the budget."** Camelot Unchained's Kickstarter was about 13% of its reported total funding. Always ask where the rest of the money comes from, and how many months the headline number buys.

## Check yourself

1. A studio has $6 million, 20 people at $9,000 per head-month and $40,000 of fixed monthly costs. What is its runway? It plans to hire 10 more people in month 6. What is the runway then, counted from month 1?
2. In the section 2 plan, which costs more, a two-month slip in pre-production or a one-month slip in beta? By how much?
3. Using Cloud Imperium's 2024 figures, if costs and income both stayed flat, how much would the company need to raise or borrow per month to cover the gap, including capital spending?
4. A plan's total build cost is $20 million, and 60% of that is spent in the final 12 months at a flat burn. The studio holds 15% contingency. How many months of final-phase slip does the contingency cover?

<details>
<summary>Answers</summary>

1. Burn is `20 × 9,000 + 40,000 = $220,000`, so the runway is `6,000,000 / 220,000 ≈ 27.3` months. After hiring, burn becomes `30 × 9,000 + 40,000 = $310,000`. Five months at $220,000 spend $1.1 million, leaving $4.9 million, which lasts `4,900,000 / 310,000 ≈ 15.8` months. Total runway is about 5 + 15.8 = 20.8 months, so the hire costs about 6.5 months of runway.
2. Two months in pre-production cost `2 × 170,000 = $340,000`. One month in beta costs $650,000. The beta month costs $310,000 more, nearly twice as much, although it is half as long.
3. Costs including capital spending were `152.9 + 8.0 = $160.9` million against income of $146.6 million, a gap of $14.3 million a year, or about $1.19 million a month.
4. Final-phase burn is `0.6 × 20,000,000 / 12 = $1,000,000` a month. Contingency is `0.15 × 20,000,000 = $3,000,000`, which covers three months of final-phase slip.

</details>

## Lab / assignment hook

[Lab 13, phase budget and slip analysis](../labs/lab13.md). You implement the burn model with ramps and a contingency rule, test it against the numbers in this lecture, then build a sourced budget for your own final-project MMO and stress it with three slip scenarios. The budget and memo feed straight into the final business plan (week 15), and next week's pitch asks for the first stage of it.

## Sources

- Kickstarter, "Camelot Unchained" project page (campaign 2 April to 2 May 2013; archived snapshot 15 April 2026). $2,232,933 pledged of a $2,000,000 goal by 14,873 backers.
- Camelot Unchained official site, news posts "Steam Early Access Announcement" (30 May 2026) and "Live NOW on Steam Early Access" (2 June 2026).
- Wikipedia, "Camelot Unchained" (accessed September 2026). Alpha 1 on 3 March 2015, the ability-system rebuild and Beta 1 on 31 July 2018, and the reported funding totals ($4.5M crowdfunding, $5M from Mark Jacobs, $7.5M investment in 2018). The funding totals are reported, not audited.
- Cloud Imperium Games, "CFO comment on the 2024 accounting" (cloudimperiumgames.com, 2026). Trading costs, cost categories, capex, income, EBITDA loss ($6.3 million), loss after capex ($14.3 million) and year-end headcount (1,031) for 2024; read directly, September 2026.
- Roberts Space Industries, crowdfunding statistics endpoint (read 28 September 2026). Lifetime funds of about $1.048 billion.
- Kollar, P., "Final Fantasy 14 killed by Square Enix's stubbornness, reborn by a new approach", Polygon, 20 March 2014. Report of Naoki Yoshida's GDC 2014 talk, including the decision to rebuild while continuing to update the original game.
- Wikipedia, "Final Fantasy XIV (2010 video game)" and "Final Fantasy XIV" (accessed September 2026). Launch on 30 September 2010, suspended fees, Yoshida taking over in December 2010, shutdown on 11 November 2012, relaunch in August 2013.
- Hypixel Studios, "Hytale is saved!" (hytale.com, 17 November 2025), and Chalk, A., PC Gamer, 17 November 2025. Buyback from Riot, 30+ developers rehired, ten-year personal funding commitment. Hytale news, early access launch post (13 January 2026).
- Brooks, F. P. (1975). *The Mythical Man-Month*. Addison-Wesley. The argument about adding people to late projects, paraphrased.
- Fields, T. & Cotton, B. (2011). *Social Game Design: Monetization Methods and Mechanics*. Morgan Kaufmann.

## Interactive spec: examples/w13-burn-and-runway.html

**The one insight:** a month of delay costs the burn of the month it happens in, so the same slip is cheap early and fatal late.

**Layout.** Two linked panels side by side at 1280px, stacked at 390px.

- **Left panel, "Team plan".** Stacked area chart. X axis is month (1 to 48). Y axis is headcount. Each phase is one colour block of height `n_p` and width `m_p`. A slip widens the chosen phase by Δ months and shifts later phases right.
- **Right panel, "Money".** Line chart of cumulative spend `S(t)` in $M against month, same x axis. A horizontal line for cash raised. A dashed horizontal line for "cash minus contingency" when the contingency toggle is on. A vertical red marker and label "cash runs out in month N" where `S(t)` first exceeds cash. If it never does, show a green label "funded, ends month N with $X left".

**Controls.**
- Three phase rows, each with months (1 to 24, step 1) and headcount (1 to 120, step 1). Defaults 6/12, 18/45, 6/60.
- Loaded cost `c` ($5,000 to $20,000 per head-month, step $500, default $10,000). Fixed cost `F` ($0 to $200,000, step $10,000, default $50,000).
- Cash raised ($5M to $30M, step $0.5M, default $15M).
- Slip: phase selector (pre-production, production, beta and launch) and Δ (0 to 6 months, default 0).
- Contingency toggle with percentage (0 to 30%, default 20%). When on, show "contingency covers X months of this phase's burn" for the selected slip phase.
- A "compare phases" button that shows a small table of the slip cost and cash-out month for the current Δ applied to each phase in turn.

**Formulas.** `B_p = n_p × c + F`. Monthly series is each `B_p` repeated `m_p` times (slip adds Δ to the chosen `m_p`). `S(t)` is the running sum. Cash-out month is the first `t` with `S(t) > cash`, with integer dollars to avoid float error. Slip cost `= Δ × B_p`.

**Numbers panel** (always visible, copyable): burn per phase, phase cost, total, total with slip, slip cost, cash-out month, contingency in dollars and in months of the selected phase.

**Test values** (defaults, Δ = 3, cash $15M):
- No slip: total $13,920,000, 30 months, never runs out, $1,080,000 left.
- Slip in pre-production: extra $510,000, total $14,430,000, never runs out.
- Slip in production: extra $1,500,000, total $15,420,000, cash runs out in month 33.
- Slip in beta and launch: extra $1,950,000, total $15,870,000, cash runs out in month 32.
- Contingency 20% of $13,920,000 = $2,784,000, which covers 5.57 months of production burn and 4.28 months of beta burn.

**First screen.** Defaults with Δ = 3 in beta and launch, so the red "cash runs out in month 32" marker is visible on load. No game art or logos; generic shapes only.

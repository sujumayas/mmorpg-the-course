# MMO403 · Week 14 — Pitching to Publishers and Investors

**Why this matters:** Nobody funds a whole MMO on a slide deck. Publishers and investors fund the next stage, then decide again. If your pitch asks for everything at once, a careful funder has to say no even to a good idea. If it asks for a cheap first stage with a clear test and an honest kill rule, the same idea can become a good bet. This week you learn to see your pitch the way the person across the table does.

**You will be able to:**
- Compute the expected value of funding a game all at once and in two stages with a go/no-go gate, and explain where the gate's value comes from.
- Compute how a gate's false-go rate and its cost change that value, and choose between stage-1 designs by the numbers.
- Compute pre-money and post-money valuation, ownership and dilution across funding rounds, and explain why a de-risked second round costs founders less.
- Design and critique a pitch that asks for one stage, names its go/no-go metric in advance, and states its risks honestly.

**Before class:** Your lab 13 budget, printed. Reread [MA102 week 4, section 4](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md) (expected value of a decision) and [MA102 week 14, section 3](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w14-intro-to-hypothesis-testing-ab.md) (false positives and false negatives). Supercell, "Rush Wars Closing" (supercell.com, 5 November 2019), 3 minutes.

**Prerequisites from earlier courses:** [MMO403 week 13, team and budget planning](w13-team-and-budget-planning.md) (the phase costs this week's stages are built from). [MMO403 week 1, business models](w01-business-models-box-subscription-f2p-hybrid.md). [PR101 week 4, scope, MVP and vertical slice](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md) (what a first stage usually builds). [MMO308 week 5, A/B test design](../../MMO308-live-operations-analytics-and-experimentation/lectures/w05-ab-testing-design.md) (choosing one metric before you look). Looking ahead, [MMO407 week 3, beta strategies](../../MMO407-launch-scaling-and-post-mortems/lectures/w03-beta-strategies.md) (next semester) treats soft launches and tests as sources of evidence.

**Interactive:** [w14-stage-gate.html](../examples/w14-stage-gate.html). Keep it open during section 2.

---

## 1. What a funder is buying

A pitch is an argument about four numbers, whether or not it shows them.

- **Cost.** How much money the game needs, and when. You built this in week 13 as a phase plan.
- **Value if it works.** What the funder gets back if the game reaches its target audience. For a publisher, that is its share of net revenue. For an equity investor, it is the value of their shares when they sell. Call it `V`.
- **Chance it works.** Call it `p`. Nobody knows it, and every funder has seen many confident pitches that failed. A funder's estimate of `p` for a new MMO from an unproven team is low, and it should be.
- **What happens after bad news.** Can the funder stop paying if the first months go badly, and how much will they have spent by then?

Students tend to spend their pitch on the first two numbers. Experienced funders listen hardest to the last two. This lecture shows why, with one model.

### Who funds games, and what they get

| Funder | Gives | Gets | Decides again at |
|---|---|---|---|
| Publisher | Development money (an advance), marketing, distribution | A share of revenue, often recouping its advance first; sometimes the IP | Contract milestones |
| Venture or strategic investor | Cash | Shares in the studio | Each funding round |
| Platform holder | Money or marketing for exclusivity or a launch window | Exclusive content, time or players | Contract milestones |
| Rewards crowdfunding (Kickstarter) | Pledges | Rewards (game access, items), no ownership | Never; backers pay once |
| Equity crowdfunding | Small investments from many people | Shares; regulated as securities | Each round |

Week 12 covered publishing contracts, platform fees and revenue splits, so this week does not repeat them. Notice the last column. Every funder except rewards crowdfunding gets to decide again, and that is where the money is made.

## 2. Worked example: why good studios cancel half their games

### The hook

At the Gamelab conference in June 2019, Blizzard's former president Mike Morhaime said that about half of the games Blizzard started were never released, some 14 cancelled titles over the company's history. The best known is Titan, a next-generation MMO in development from about 2007. Blizzard announced its cancellation in September 2014. About forty of its developers went on to build Overwatch, released in 2016.

Players heard years of rumours about Titan and then nothing. It is tempting to read a 50% cancellation rate as a studio failing half the time. The model below says the opposite. The ability to cancel is part of what makes the other half worth funding.

### The model

Split funding into two stages.

```
Stage 1: spend C1 on a prototype, vertical slice or soft launch.
         It returns a signal: "go" or "stop".
Stage 2: spend C2 on full production and launch, only after a "go".

p  = probability the game is a hit (worth V); otherwise it is worth 0
s  = P(go | hit)     the gate's sensitivity: hits it lets through
f  = P(go | miss)    the gate's false-go rate: misses it lets through

All in (no gate):  EV_all = p × V − C1 − C2
Gated:             EV_gate = −C1 + max(0, p × s × (V − C2) − (1 − p) × f × C2)
Kill rate:         k = 1 − (p × s + (1 − p) × f)
```

- `V` is the value to the funder if the game is a hit, before counting `C1` and `C2`.
- The `max(0, ...)` says a funder never pays `C2` when continuing is worth less than stopping.
- The kill rate `k` is the share of projects stopped after stage 1.

With a perfect gate (`s = 1`, `f = 0`) the gated value simplifies to `p × V − C1 − p × C2`. Compare it with the all-in value and the difference is exactly `(1 − p) × C2`. **A gate is worth the stage-2 money you do not spend on games that were going to fail.** Every other feature of the model comes from how far a real gate falls short of that.

### Numbers you can check

Take an invented MMO pitch in $ millions. Stage 1 costs `C1 = 2` (about a year of the pre-production team from week 13). Stage 2 costs `C2 = 18`. A hit is worth `V = 60` to the funder. The funder rates the chance of a hit at `p = 0.25`.

**All in.** `0.25 × 60 − 2 − 18 = −5`. The funder expects to lose $5 million. A careful funder says no.

**Perfect gate.** `−2 + 0.25 × (60 − 18) = +8.5`. The same game, the same odds, is now worth $8.5 million. The gain is `(1 − 0.25) × 18 = 13.5`, the stage-2 money saved on the three games in four that miss.

**Realistic gates.** Stage-1 evidence is noisy. Hold `s = 0.8` (the gate catches 80% of hits) and vary the false-go rate.

| False-go rate `f` | EV of the gated plan | Killed after stage 1 |
|---|---|---|
| 0.0 | +6.40 | 80% |
| 0.2 | +3.70 | 65% |
| 0.4 | +1.00 | 50% |
| 0.6 | −1.70 | 35% |
| No gate: always continue | −5.00 | 0% |

Check the second row by hand. `0.25 × 0.8 × 42 = 8.4`, `0.75 × 0.2 × 18 = 2.7`, and `−2 + 8.4 − 2.7 = 3.7`.

Read the table from the bottom. A studio that always continues has no gate at all, and its value is the all-in value. (If the signal says "go" every time, `s = f = 1`, it carries no information. The model then tells a rational funder to stop before stage 2 whatever happens, for an EV of −2. That is the model's way of saying the project should not have been funded.) As the gate gets stricter, the funder kills more projects and earns more. At `f = 0.4`, half the projects die after stage 1 and the portfolio still makes money. That is Blizzard's reported rate. A 50% cancellation rate is what a working gate looks like from outside, not a sign of failure.

The Python below reproduces the table. It runs as shown with `.venv/bin/python`.

```python
def ev_all_in(p, V, C1, C2):
    """Fund everything up front: pay C1 + C2, win V with probability p."""
    return p * V - C1 - C2


def ev_gated(p, V, C1, C2, s, f):
    """Pay C1, look at the signal, pay C2 only after a 'go'.
    s = P(go | hit), f = P(go | miss)."""
    go_hit, go_miss = p * s, (1 - p) * f
    continue_value = go_hit * (V - C2) - go_miss * C2
    return -C1 + max(0.0, continue_value)   # a funder never continues at a loss


p, V, C1, C2 = 0.25, 60, 2, 18              # money in $ millions
print(f"all in:          {ev_all_in(p, V, C1, C2):+.2f}")
print(f"perfect gate:    {ev_gated(p, V, C1, C2, s=1.0, f=0.0):+.2f}")
for f in (0.0, 0.2, 0.4, 0.6):
    s = 0.8
    kill = 1 - (p * s + (1 - p) * f)
    print(f"s=0.8 f={f:.1f}:     {ev_gated(p, V, C1, C2, s, f):+.2f}   killed after stage 1: {kill:.0%}")
```

Output:

```
all in:          -5.00
perfect gate:    +8.50
s=0.8 f=0.0:     +6.40   killed after stage 1: 80%
s=0.8 f=0.2:     +3.70   killed after stage 1: 65%
s=0.8 f=0.4:     +1.00   killed after stage 1: 50%
s=0.8 f=0.6:     -1.70   killed after stage 1: 35%
```

### Is it worth continuing after a "go"?

After a "go", the funder's estimate of `p` rises. By Bayes' rule, `P(hit | go) = p × s / (p × s + (1 − p) × f)`. With `s = 0.8` and `f = 0.2` that is `0.2 / 0.35 ≈ 0.571`. Continuing is worth it when `P(hit | go) × V > C2`, and `0.571 × 60 ≈ 34.3 > 18`, so the funder continues. This is the same arithmetic as MA102 week 14, where a "significant" test result raised your belief that a change worked. A stage-1 gate is a hypothesis test on the whole game, with a false-positive rate `f` and a power `s`.

### Paying more for a better gate

The studio can design stage 1. Compare three options for the same pitch.

| Stage 1 design | `C1` | `s` | `f` | EV | `P(hit | go)` |
|---|---|---|---|---|---|
| Paper design and a combat prototype | 1 | 0.70 | 0.35 | +1.63 | 0.40 |
| Vertical slice with a closed playtest | 2 | 0.80 | 0.20 | +3.70 | 0.57 |
| Vertical slice plus a regional soft launch | 4 | 0.90 | 0.10 | +4.10 | 0.75 |

The most expensive stage 1 wins here, because it cuts false-go spending by more than it costs. That is not a general rule. Raise `C1` to $6 million and the soft launch drops to +2.10, below the vertical slice. The point is that a pitch should justify its stage 1 by the quality of the evidence it buys, not by how much of the game it builds.

### Move it yourself

Open the interactive. The left panel, "100 projects", is a 10 × 10 grid of squares, one per imagined project, coloured by where each ends up after the gate: "hit, funded", "miss, funded", "hit, killed" or "miss, killed". A small table under the grid gives the money on each branch. The right panel plots expected value against the false-go rate `f`, with a flat line for the all-in plan. Drag `f` from 0 to 1 and watch the red "miss, funded" pile grow on the left while the curve on the right falls through zero and flattens at `−C1`, where a rational funder would stop paying after stage 1 whatever the signal says. Then lower `p` to 0.15. The all-in plan falls to −11. The gated plan at `f = 0.2` sits just below zero (−0.02), but tighten the gate to `f = 0.05` and it is worth about +2.3. The riskier the project, the stricter the gate has to be, and the more the gate is worth. That describes most MMO pitches.

### Cross-game recognition

**Supercell (mobile, 2010s to 2020s).** Supercell builds games in small teams it calls cells, typically five to seven people. A game that passes internal playtesting is released in a few test markets (the Canadian App Store has been its usual first stop), and only a game whose numbers hold up goes global. The company is known for killing games at that stage. It cancelled Smash Land in 2015 after a test release, about ten months of work by four or five people. In November 2019 it closed the Rush Wars beta, switched off in-app purchases the day it announced the decision, and kept the servers running until 30 November. Its first new global release in over five years, Squad Busters, came on 29 May 2024. In our model, a cell makes `C1` tiny compared with `C2` (global launch and years of live operations), and a soft launch buys low `f`. That is the cheapest possible version of the gate.

**Hytale (2018 to 2026).** Riot Games invested in Hypixel Studios in 2018 and bought it in 2020. A planned 2021 early-access release did not happen, and after an engine reboot and a rising bar, Riot cancelled the game in June 2025. In November 2025 the original co-founders bought it back, returned to the older engine, rehired more than 30 developers and committed personal funding for ten years. Early Access opened on 13 January 2026. In our model, the same project got two different verdicts because the two funders had different numbers. For Riot, the remaining `C2` on a new engine was large next to its estimate of `V`. For the founders, returning to an existing engine and a smaller team cut `C2`, and they valued the game differently. A gate is a decision by a particular funder with particular costs, not a verdict on the idea.

**Blizzard's Titan (2007 to 2014).** Titan is the case where the gate came late. PC Gamer reported in 2012 that the team had grown past 100 people, years before the project was stopped, so much of `C2` had already been spent. Even so, the stop was worth something. About forty people and the work they had done went into Overwatch. Real projects have a salvage value that the basic model sets to zero. You can add it as a term `+ (1 − p) × f × L` for the value recovered from a funded miss, or `+ k × L1` for what a killed project leaves behind (tools, tech, a team that has worked together).

Three companies, three sizes of stage 1, one equation. When you read a cancellation announcement, ask which stage the project had reached, what the next stage would have cost, and who was deciding.

### Eyes-open design judgment

- **A gate is only as good as the metric chosen before you look.** If the team picks its "go" metric after seeing the data, `f` rises toward 1 and the gate is worth nothing. Write the metric and threshold into the pitch, the way MMO308 week 5 wrote the primary metric into a test plan.
- **Sunk cost is invisible to the model, on purpose.** Once `C1` is spent it appears in both branches, so it cannot affect the decision. Teams that argue "we've spent too much to stop" are asking the funder to ignore this.
- **Gates have human costs.** Killing a game ends work people cared about and can end jobs. Studios that gate well tend to plan for it. They keep teams together after a kill, as Blizzard did with Titan's team, and they are open with players who joined a test. Supercell's Rush Wars notice, which turned off purchases immediately and gave players weeks of notice, is a reasonable standard to copy.
- **Not every project can gate cheaply.** An MMO's server technology, economy and social systems are hard to test with a small team. The honest pitch says which risks stage 1 retires and which ones it cannot reach.

## 3. Valuation and dilution

When the funder is an investor rather than a publisher, the "value" they receive is shares. Three terms cover most conversations.

```
post-money valuation = investment / share bought
pre-money valuation  = post-money − investment
founders' share after a round = share before × (1 − share sold)
```

**A published example.** In December 2018, Cloud Imperium Games (Star Citizen) announced a $46 million investment from the family office of Clive Calder for a 10% stake. That puts the post-money valuation at `46 / 0.10 = $460` million and the pre-money valuation at $414 million. Press coverage described it as "nearly $500 million". The company said the money was meant for marketing the eventual launch, while development continued to be funded by players, whose pledges passed $1 billion in 2026. Pledges bought game access and ships, not shares. Only the investors own part of the company.

### Why staging protects founders

Return to the section 2 pitch, now as an equity raise. Suppose that before any evidence exists, an investor values the studio at $6 million pre-money. The founders can raise all $20 million now at that price, or raise stage 1 ($2 million) at that price and the rest after a "go".

| Plan | Round | Investment | Post-money | Share sold | Founders own after |
|---|---|---|---|---|---|
| All at once | Single round | $20M | $26M | 76.9% | 23.1% |
| Staged | Seed (stage 1) | $2M | $8M | 25% | 75% |
| Staged | Series A after a "go" | $18M | $72M | 25% | 56.25% |

The staged founders own more than twice as much. The reason is that the "go" signal changed the price. After a passed gate, the funder's `P(hit | go)` rose from 0.25 to 0.57 (section 2), and the company is worth more, so the same share buys more money. The numbers in this table are invented, but the direction is general. Every risk you retire before you raise makes the next raise cheaper.

### Rewards, equity and the law

Rewards crowdfunding and equity crowdfunding are legally different things. Backers on Kickstarter pay for rewards and get no ownership. Selling shares to the public is regulated as a securities offering. In the United States, for example, Regulation Crowdfunding lets a company raise at most $5 million in a 12-month period through an SEC-registered intermediary, with limits on how much non-accredited investors can put in and required disclosures. Other countries have their own rules. If your plan includes selling shares to players, you need a lawyer before you need a deck.

## 4. The pitch itself

A pitch deck for a funder is ten to fifteen slides. Every slide should help the funder estimate one of the four numbers from section 1, or reduce their risk.

1. **The game in one sentence and one image.** The fantasy the player buys into. Use your own art or placeholder shapes, never another game's assets.
2. **Who plays it, and how many.** The audience and its size, with comparable titles ("comps"). Choose comps honestly. You can only see the games that shipped. Blizzard's cancelled half never appears in a list of comps, so comps overstate `p`. Say so.
3. **Why now.** What has changed (a platform, a technology, an audience that current games serve badly).
4. **What exists.** The prototype or vertical slice, ideally playable in the meeting.
5. **How it makes money.** The business model from week 1 and the unit economics from week 2, as ranges. Include how much revenue depends on the top 1% of spenders (week 9), and your position on loot boxes and paid randomness given the rules in the markets you plan to sell in (weeks 6 and 7). Funders price regulatory risk, and players and journalists will read your store.
6. **The plan and the money.** Your week 13 phases, total cost, and runway.
7. **The ask.** How much for which stage, what it buys, and when you will come back.
8. **The gate.** The metric, the threshold and the date for the go/no-go decision, and what you will do after a "stop". This is the slide that most student pitches leave out.
9. **The team.** Who has shipped what, and which roles you still need to hire.
10. **Risks.** The three biggest, and which ones stage 1 retires.

### Honest numbers are a strategy, not only a duty

A funder's first job in the meeting is to find out which of your numbers are wishful. A pitch that shows day-30 retention from a friendly closed test as if it were a launch forecast, or that hides that the model depends on a few very heavy spenders, loses credibility on every other slide once one number fails. Give ranges, say where each number came from, and show what happens to your plan at the low end. This is also where monetization ethics meets business. A plan that only works with manipulative design (weeks 8 and 9) carries legal and reputation risk that a careful funder will count against you, and a plan that works without it is easier to fund.

Crowdfunding raises a particular version of this duty. Backers carry the risk of a project without the gate that professional funders have. Camelot Unchained's 2013 backers (week 13) waited thirteen years for Early Access. If you ask players for money before stage 1 is proven, tell them plainly what stage the project is in, what the money buys, and what happens if it stops.

## In-class activity (30 minutes)

Groups of four. Two students are the studio, two are the funder. Swap roles halfway.

1. The studio has 5 minutes to pitch from its lab 13 budget. The ask must be for stage 1 only, with a named go/no-go metric, threshold and date. (5 min)
2. The funders question the studio for 5 minutes, then privately write their estimates of `p`, `V`, `s` and `f`. (5 min)
3. Both sides compute `EV_all` and `EV_gate` with the funder's numbers, using the interactive. (3 min)
4. The funders decide to fund stage 1 or not, and give one change to the pitch that would move their numbers. (2 min)
5. Swap roles and repeat. (15 min)

Expected output: for each pitch, the funder's four estimates, both EVs, the decision, and the one suggested change.

## Common misconceptions

- **"A studio that cancels half its games is failing half the time."** A strict gate cancels most projects and earns more than a lax one (section 2 table). Cancelling cheaply is the business model.
- **"Asking for the whole budget shows confidence."** It forces the funder to accept the all-in value, which is often negative for a risky game that would be positive with a gate.
- **"We've spent too much to stop."** Money already spent is the same in both branches of the decision, so it cannot justify continuing.
- **"Backers own part of the game."** Rewards backers own their rewards. Only equity investors own shares, and selling shares to the public is regulated.

## Check yourself

1. A pitch has `p = 0.2`, `V = 80`, `C1 = 3`, `C2 = 20` ($ millions). Compute the all-in EV and the EV with a perfect gate. How much is the gate worth?
2. With the same numbers and `s = 0.75`, find the largest false-go rate `f` for which the gated plan is still worth more than zero.
3. A studio sells 20% for $5 million in a seed round, then 30% for $30 million in a later round. What were the post-money valuations, and what share do the founders own at the end?
4. A funder's gate has `s = 0.8`, `f = 0.2` and `p = 0.25`, as in section 2. A new analytics tool would cut `f` to 0.1 but add $1 million to `C1`. Should the funder use it?

<details>
<summary>Answers</summary>

1. All in: `0.2 × 80 − 3 − 20 = −7`. Perfect gate: `−3 + 0.2 × (80 − 20) = +9`. The gate is worth `9 − (−7) = 16`, which equals `(1 − 0.2) × 20`.
2. Set `−3 + 0.2 × 0.75 × 60 − 0.8 × f × 20 = 0`. That gives `9 − 3 − 16f = 0`, so `f = 0.375`. Any gate that lets through more than 37.5% of misses loses money.
3. Seed post-money is `5 / 0.20 = $25` million. The later post-money is `30 / 0.30 = $100` million. Founders own `0.8 × 0.7 = 0.56`, or 56%.
4. With the tool, `EV = −3 + 0.25 × 0.8 × 42 − 0.75 × 0.1 × 18 = −3 + 8.4 − 1.35 = 4.05`. Without it the EV is 3.70. The tool adds $0.35 million of expected value, so yes, narrowly. Check how sure you are that `f` really falls to 0.1 before paying for it.

</details>

## Lab / assignment hook

[Lab 14, stage-gate funding plan and pitch](../labs/lab14.md). You implement the gate model, dilution across rounds and a stage-1 design chooser, test them against this lecture, then turn your lab 13 budget into a staged funding plan and a ten-slide pitch with a written gate. The deck and plan are the funding section of your final business plan (week 15).

## Sources

- Eurogamer, report of Mike Morhaime's talk at Gamelab, Barcelona (26 June 2019). About half of the games Blizzard started were never released, some 14 titles.
- Wikipedia, "Titan (cancelled video game)" (accessed September 2026), citing Polygon (23 September 2014) and Eurogamer (14 March 2017, Jeff Kaplan interview). Development from about 2007, public cancellation in September 2014, about forty team members moving to what became Overwatch (2016).
- PC Gamer, "Titan's team is over 100 people" (28 September 2012).
- Supercell, "Rush Wars Closing" (supercell.com, 5 November 2019). Beta ended, in-app purchases switched off, servers kept running until 30 November 2019.
- Wikipedia, "Supercell (company)" (accessed September 2026). Cells of five to seven people, test releases in the Canadian App Store before global launch, Smash Land (four to five people, ten months), Squad Busters global launch on 29 May 2024.
- Hypixel Studios, "Hytale is saved!" (hytale.com, 17 November 2025), and the early access launch post (13 January 2026). Buyback, return to the legacy engine, 30+ developers rehired, ten-year personal funding.
- Chalk, A., "'Hytale is saved'", PC Gamer, 17 November 2025. Riot's 2020 acquisition, the missed 2021 early access plan, the engine reboot and cancellation.
- TechCrunch, "Crowdfunded developer of space sim Star Citizen takes on $46M in funding at nearly $500M valuation" (21 December 2018). $46 million for 10%, from Clive Calder's family office, intended for marketing.
- Roberts Space Industries, crowdfunding statistics endpoint (read 28 September 2026). Lifetime pledges above $1.04 billion.
- U.S. Securities and Exchange Commission, "Regulation Crowdfunding" (sec.gov, accessed September 2026). $5 million maximum per 12 months, SEC-registered intermediary, investor limits and disclosure.
- Kickstarter, "Camelot Unchained" project page (archived 15 April 2026). Campaign of April to May 2013.
- Fields, T. & Cotton, B. (2011). *Social Game Design: Monetization Methods and Mechanics*. Morgan Kaufmann.

## Interactive spec: examples/w14-stage-gate.html

**The one insight:** the same game, with the same odds, goes from a losing bet to a winning one when the funder can stop after a cheap first stage, and a studio that always continues gets the all-in value.

**Layout.** Two linked panels side by side at 1280px, stacked at 390px.

- **Left panel, "100 projects".** A 10 × 10 grid of squares, one per imagined project. Colour by outcome: hit and funded (green), miss and funded (red), hit and killed (amber, a lost hit), miss and killed (grey). Counts come from rounding `100 × p × s`, `100 × (1 − p) × f`, `100 × p × (1 − s)`, `100 × (1 − p) × (1 − f)` so they sum to 100 (adjust the largest group for rounding). Under the grid, money per branch: stage-1 spend `100 × C1`, stage-2 spend on hits and on misses, value returned.
- **Right panel, "Expected value".** X axis is the false-go rate `f` from 0 to 1. Y axis is EV in $M. Curve for `EV_gate(f)` at the current `s`. Flat dashed line for `EV_all`. Zero line. A dot marks the current `f`. Label the `f` where the curve crosses zero.

**Controls.** `p` (0.05 to 0.60, step 0.01, default 0.25). `V` ($10M to $200M, step 5, default 60). `C1` ($0.5M to $10M, step 0.5, default 2). `C2` ($5M to $60M, step 1, default 18). `s` (0.5 to 1.0, step 0.05, default 0.8). `f` (0 to 1, step 0.05, default 0.2). A preset row with three stage-1 designs from the lecture: "prototype" (C1 1, s 0.70, f 0.35), "vertical slice" (2, 0.80, 0.20), "soft launch" (4, 0.90, 0.10).

**Formulas.** `EV_all = pV − C1 − C2`. `EV_gate = −C1 + max(0, p·s·(V − C2) − (1 − p)·f·C2)`. Kill rate `k = 1 − (p·s + (1 − p)·f)`. `P(hit | go) = p·s / (p·s + (1 − p)·f)` (show "n/a" when the denominator is 0). Break-even false-go rate `f* = (p·s·(V − C2) − C1) / ((1 − p)·C2)`, clamped to [0, 1].

**Numbers panel** (always visible, copyable): `EV_all`, `EV_gate`, value of the gate `EV_gate − EV_all`, kill rate, `P(hit | go)`, `f*`.

**Test values** (money in $M):
- Defaults: `EV_all = −5.00`, `EV_gate = +3.70`, kill rate 65%, `P(hit | go) = 0.571`.
- `s = 1`, `f = 0`: `EV_gate = +8.50`, gate value 13.50.
- `s = 0.8`, `f = 0.4`: `EV_gate = +1.00`, kill rate 50%. `f = 0.6`: `EV_gate = −1.70`.
- Presets: prototype +1.625 (kill rate 56.25%), vertical slice +3.70 (65%), soft launch +4.10 (70%).
- Break-even at defaults: `f* = (8.4 − 2) / 13.5 ≈ 0.474`.
- `s = 1`, `f = 1` (a signal that always says go): continuing is worth `10.5 − 13.5 < 0`, so `EV_gate = −2.00`. Show a note: "this signal carries no information; a rational funder stops before stage 2". Add an "always continue" toggle that forces stage 2 after any signal; with it on, `EV = p·V − C1 − C2 = −5.00` at defaults, whatever `s` and `f` are.

**First screen.** Defaults, so the right panel shows the gated curve well above the negative all-in line at `f = 0.2`. No game art or logos; generic shapes only.

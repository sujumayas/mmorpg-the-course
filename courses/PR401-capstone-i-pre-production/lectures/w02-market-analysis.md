# PR401 · Week 02 — Market Analysis

**Why this matters:** You are not raising money for the capstone, so it is tempting to skip market analysis. But PR402 ends with strangers deciding whether to play your game, and they already play something else. Market analysis tells you who those players are, what they already play, what they complain about, and how many of them you would need to fill a server. The last number is usually far larger than a student team expects.

**You will be able to:**
- Estimate owners and revenue ranges for comparable games from public Steam review counts, and state when the method does not apply.
- Compute the daily players needed to reach a target peak concurrency from session length and a peak-to-average ratio.
- Code a sample of comparable-game reviews into complaint categories and turn the counts into a positioning statement.
- Critique a comparables table for survivorship bias, business-model mismatch and false precision.

**Before class:** Read GameDiscoverCo, "How that game sold on Steam, using the 'NB number'" (Simon Carless, 3 August 2020), 10 minutes. Reread [MMO403 week 2, unit economics](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w02-unit-economics-ltv-cac-arppu.md), section 1, and [MMO403 week 12, publishing platforms and fees](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w12-publishing-platforms-and-fees.md), section 2 (what "30%" means on Steam). Bring your week 1 pitch draft and its list of comparables.

**Prerequisites from earlier courses:** [MMO403 week 12](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w12-publishing-platforms-and-fees.md) for store revenue shares, which this guide uses at a flat 30% for a first pass. Looking ahead, [MMO405 week 6, interviews and coding](../../MMO405-research-methods-in-online-games/lectures/w06-qualitative-methods-interviews.md) (next semester) covers building a codebook and checking agreement between coders. [MMO308 week 3, cohorts and retention curves](../../MMO308-live-operations-analytics-and-experimentation/lectures/w03-cohorts-and-retention-curves.md) for why a launch audience shrinks. [PR101 week 6](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md) for reporting an estimate as a range. From this course, [week 1](w01-pitch-development.md) for the pitch and its claims sheet.

---

## 1. What market analysis is for in a capstone

A studio does market analysis to answer "will enough people pay for this to cover its cost?" MMO403 week 14 showed how funders use that answer. Your capstone is free to play for a few weeks and has no budget to recover, so the question changes. You need four answers:

1. **Who is the player?** Name them by what they play now, not by age or gender. "Plays small sandbox MMOs with full-loot PvP, has quit two of them" is a player. "Males 18 to 34" is not.
2. **What are they missing?** What do players of your comparables complain about that your pitch fixes? This is your positioning.
3. **How big is that group?** Rough, as a range, from public data. It tells you whether the niche exists at all.
4. **How many do you need?** The daily players it takes to make your world feel inhabited at launch. Section 4 computes it.

A **comparable** (or "comp") is a shipped game whose players are the players you want. Pick two to four. They should be close in what the player does, not just in genre label, and at least one should be small enough to be honest about your scale. Comparing your capstone to the largest MMOs tells you nothing you can use.

## 2. Worked example: how many people bought the comparables?

### The hook

Every game on Steam shows how many reviews it has. Sales figures are private. Since at least the mid-2010s, analysts have estimated sales by multiplying the review count by a fixed number. The idea is credited to Mike Boxleiter, and Jake Birkett updated it in 2018. In August 2020 Simon Carless of GameDiscoverCo checked it against games whose real sales were known. The multiplier had fallen. Games released before 2017 averaged about 81 sales per review. Games released in 2020 averaged about 41, with a median of 38. The reason was a change in Steam itself. From October 2019 Steam began prompting players to leave a review, so more buyers reviewed. The same number of reviews now meant fewer sales.

A market estimate is only as good as its multiplier, and the multiplier moves when the platform does.

### The model

```
owners  ≈ R × m                    R = total Steam reviews, m = sales per review
gross   ≈ owners × price × φ       price = current list price, φ = realized-price factor
net     ≈ gross × (1 − f)          f = store fee, 0.30 for a first pass
```

- `R` is the review count from the store page or the Steam reviews endpoint, on a stated date.
- `m` is the multiplier. This guide uses a range from 38 (the 2020-launch median) to 58 (the median across all games in the 2020 sample). Always report both ends.
- `φ` (phi) covers discounts, regional pricing and refunds. This guide sets `φ = 0.5` as a teaching assumption. It is not a measured value, and it is the least reliable number in the model.
- `f = 0.30` ignores Valve's lower tiers above US$10 million (MMO403 week 12).

The model applies only to games that are **paid on Steam**. It breaks for free-to-play games, games that also sell accounts or pledges off Steam, and games whose review count comes mostly from a relaunch.

### Numbers you can check

Three paid, small-studio MMOs in the *Emberfall* niche (sandbox, player economy, group play). Review counts and US list prices from the Steam store, 29 September 2026.

| Game (developer) | Steam release listed | `R` | Price | Owners at `m = 38` | at `m = 58` | Net at 38 ($M) | at 58 ($M) |
|---|---|---|---|---|---|---|---|
| *Mortal Online 2* (Star Vault) | 25 Jan 2022 | 13,925 | $39.99 | 529,150 | 807,650 | 7.41 | 11.30 |
| *Pantheon: Rise of the Fallen* (Visionary Realms) | 13 Dec 2024, early access | 5,108 | $39.99 | 194,104 | 296,264 | 2.72 | 4.15 |
| *Project: Gorgon* (Elder Game) | 28 Jan 2026 | 5,080 | $24.99 | 193,040 | 294,640 | 1.69 | 2.58 |

Check one row by hand. *Pantheon* at `m = 38`: `5,108 × 38 = 194,104` owners. Gross is `194,104 × 39.99 × 0.5 = 3.88` million dollars. Net is `3.88 × 0.7 = 2.72` million.

Now read the table as a market analyst, not as an accountant.

- **The range is wide on purpose.** Each row spans a factor of about 1.5 from `m` alone, before any doubt about `φ`. A report that gives "*Mortal Online 2* made $9.4 million" has hidden that range, and anyone who checks will stop trusting the rest of the analysis.
- **Two rows break the model's conditions.** *Pantheon* is in early access, and its Steam page tells earlier pledge holders how to link their accounts, so some buyers paid outside Steam and are missing from its reviews. *Project: Gorgon* lists a 2026 release date, but its Steam page has posted update notes since April 2018, so it was on sale for years before that and not always at today's price. Its row is the least reliable. Say so in a footnote rather than dropping it.
- **Check the business model of every row, even the clean-looking one.** On 29 September 2026 the *Mortal Online 2* store page shows a one-time price and no subscription. This guide did not check whether Star Vault also sells the game outside Steam. If it does, treat that row as a lower bound too.
- **What the table does tell you.** Paid sandbox MMOs from small studios have reached somewhere between about two hundred thousand and eight hundred thousand buyers on Steam. That is a niche in the hundreds of thousands, not in the millions and not in the thousands. For the capstone, this is the answer to question 3 in section 1: the players exist.

The lab 02 checker computes these ranges from a comparables sheet and refuses rows whose business model breaks the method.

### The same idea elsewhere

**Free-to-play breaks the multiplier.** *Albion Online* is free to play on Steam and had 94,048 reviews on 29 September 2026. The same arithmetic would give 3.6 to 5.5 million "owners", but an owner of a free game is anyone who clicked install, and many reviewers never paid anything. For a free game you need a different proxy, such as concurrent players, and a different multiplier. The shape of the method stays the same: a public count, times a ratio that someone has checked against private data.

**Concurrent players are the same move.** The *New World* figures in week 1 came from concurrent-player counts, not sales. Turning concurrency into a player count needs a ratio too, and section 4 derives it. In October 2021 *New World*'s peak concurrency was about 2.2 times its average, which is the kind of ratio section 4 uses.

**Estimation in PR101.** PR101 week 6 said an estimate is a range with a stated confidence, and that the midpoint alone misleads. A review-multiplier estimate is a task estimate for someone else's game.

### Eyes-open judgment

Use review multipliers to answer "is this niche tens of thousands, hundreds of thousands or millions?" They are good at that. Do not use them to make claims about a specific studio's finances. You do not know their costs, their off-Steam sales or their refund rate, and the studio can read what you write.

Choose comparables before you look at their numbers. If you pick comps after seeing which ones sold well, your table shows only the survivors and your niche looks larger than it is. Include at least one comparable that did poorly or closed, if one exists. A market analysis that finds only successes has usually been written backwards.

### Check yourself

1. A comparable has 2,000 reviews and costs $19.99. Give the owner and net revenue range with this guide's defaults.
2. Your team finds a fourth comp, released in 2016, with 8,000 reviews. Why might 38 to 58 underestimate its owners? What multiplier range would you defend, and from which source?

<details><summary>Answers</summary>

1. Owners: `2,000 × 38 = 76,000` to `2,000 × 58 = 116,000`. Net: `76,000 × 19.99 × 0.5 × 0.7 = 0.53` million to `116,000 × 19.99 × 0.5 × 0.7 = 0.81` million dollars.
2. Most of its reviews came before Steam's October 2019 review prompt, when fewer buyers reviewed. The 2020 GameDiscoverCo sample found pre-2017 games averaged about 81 sales per review with a median of 74. A range of about 58 to 81 is defensible, with the source cited. Its reviews after 2019 still pull the true value down, so say that too.

</details>

## 3. Reading what the comparables' players say

Numbers say the niche exists. Reviews say what it lacks. Negative reviews of a comparable are a free, public list of unmet needs, written by exactly the players you want.

Use the qualitative method from MMO405 week 6, cut down to fit one studio session:

1. **Sample.** Take the 40 most recent negative reviews of each comparable, in English, longer than two sentences. Recent matters because games change.
2. **Codebook.** Start with six to eight codes, such as *empty world*, *grind*, *griefing*, *economy broken*, *performance*, *onboarding*, *price*. Allow one "other" code and add to the book when "other" passes 15%.
3. **Code twice.** Two people code the same 20 reviews independently and compare. Where they disagree, tighten the code's definition. MMO405 week 6 shows why simple percent agreement flatters you.
4. **Count.** Tally codes per comparable. A review can carry more than one code.
5. **Position.** Pick the one or two complaints that recur across comparables and that your pitch addresses directly. That is your positioning statement: "For players who left sandbox MMOs because towns felt empty, *Emberfall* ..."

Do not quote reviews at length in your documents. Paraphrase and count. The reviewers did not write for your pitch deck.

## 4. How many players does your launch need?

PR301 asked for a world that supports 50 or more concurrent test players. A world with 5 people online feels dead, however good it is. So set a **target peak concurrency** for PR402 launch and work backward to daily players.

Average concurrency is players per day times the hours each plays per day, spread over 24 hours:

```
CCU_avg  = D × h_day / 24
CCU_peak = CCU_avg × q
D        = 24 × CCU_peak / (q × h_day)
```

- `D` is daily active players, `h_day` is average hours played per player per day, and `q` is the peak-to-average ratio.
- *New World* in October 2021 had a peak of 913,027 and an average of about 410,171 on SteamCharts, so `q ≈ 2.2`. A small game with players in few time zones will have a larger `q`, because everyone logs in in the same evening.

For a peak of 50 with `q = 2.2` and 1.5 hours a day, `CCU_avg = 22.7` and `D = 24 × 50 / (2.2 × 1.5) = 364` daily players. If players average only 1 hour, `D = 545`.

Then remember MMO308 week 3. Daily players are a fraction of the people who tried the game, and the fraction falls week by week. If one in three players who try the game are still playing on a given day of launch week, you need over a thousand people to try it. That is a marketing plan, not a hope, and it goes into your week 11 production plan. Put the number in the pitch now so the greenlight panel sees it.

## Studio session plan

The studio meets for 3 hours.

| Time | Activity | Output |
|---|---|---|
| 0:00 to 0:15 | Brief: the four questions, the review multiplier and its limits | Questions answered |
| 0:15 to 0:45 | Comparables. Each team lists candidates and fixes its two to four comps before looking up any numbers. At least one comp must be small or have failed | Locked comps list with reasons |
| 0:45 to 1:15 | Numbers. Teams pull review counts and prices with the date, fill `comps.csv` and run the lab 02 checker | Owner and net ranges |
| 1:15 to 1:25 | Break | |
| 1:25 to 2:15 | Review coding. Pairs sample and code negative reviews. The first 20 are coded by two people independently, then compared | Codebook and counts |
| 2:15 to 2:35 | Launch audience. Teams set a target peak CCU and compute `D` | `audience.csv` |
| 2:35 to 3:00 | Positioning round. Each team states its player, its positioning sentence and its `D` in 90 seconds. Another team names the weakest comparable | Named concern per team |

## Deliverables

Due before next week's studio session, in `preproduction/week02/` in your team repository. The one-page market section goes in `docs/market.md`, beside the pitch.

- **Comparables sheet** (`comps.csv`) with review counts, prices and access dates, and the checker output.
- **Review coding** (`codebook.md` and `codes.csv`) with the double-coded sample and the agreement you measured.
- **Launch audience** (`audience.csv`) with target peak CCU, `q`, `h_day` and the resulting `D`.
- **Market section** of the pitch (one page) answering the four questions in section 1, with the positioning sentence.
- **Claims sheet update.** Move at least one claim from assumed to estimated, and add the `D` target as a claim.

See [lab 02](../labs/lab02.md).

## Common failure modes

- **Comps chosen by fame.** The comps are the biggest MMOs the team has heard of. Fix: pick games your player would recognise, at a scale that says something about yours.
- **One number, no range.** The table reports a single owner figure. Fix: always report `m` low and high, and say where `φ` came from.
- **Free games run through the multiplier.** Fix: mark the business model of every comp. The checker refuses free-to-play rows.
- **Positioning by feature list.** "We have crafting, PvP and housing." Fix: position against a complaint that recurs in the reviews.
- **No audience target.** The team plans a launch without knowing it needs hundreds of daily players. Fix: compute `D`, and add the recruitment plan to the production risks.

## Review checklist

The instructor checks the market section when:

- [ ] Comps were locked before numbers were gathered, and the reasons are written down.
- [ ] At least one comp is small or unsuccessful.
- [ ] `check_comps.py` prints `PASS` on the submitted files, with dated review counts.
- [ ] Every estimate is a range, and `φ` is marked as an assumption.
- [ ] The review sample was double-coded on at least 20 reviews and the agreement is reported.
- [ ] The positioning sentence names a complaint found in more than one comparable.
- [ ] `D` for the target peak is computed and appears as a claim with an owner.

## Sources

- Carless, S. (3 August 2020). "How that game sold on Steam, using the 'NB number'." GameDiscoverCo newsletter. Credits the method to Mike Boxleiter and a 2018 update by Jake Birkett; reports average and median sales per review by launch year (pre-2017 average 81, median 74; 2019 average 57, median 51; 2020 average 41, median 38; whole sample average 63, median 58) and links the fall to Steam's October 2019 review prompt.
- Steam store and Steam reviews endpoint, app pages for *Mortal Online 2* (1170950), *Pantheon: Rise of the Fallen* (3107230), *Project: Gorgon* (342940) and *Albion Online* (761890). Review totals (Steam reviews endpoint, all languages and purchase types), US list prices, developers and listed release dates, accessed 29 September 2026; the *Pantheon* page's early access notes on pledge holders; *Project: Gorgon* Steam announcements dated from April 2018. These values change daily.
- SteamCharts, "New World: Aeternum" (app 1063730), October 2021 average and peak concurrent players (accessed September 2026).
- Valve revenue share tiers as covered in [MMO403 week 12](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w12-publishing-platforms-and-fees.md), with its sources.
- The realized-price factor `φ = 0.5`, the `Emberfall` pitch and the one-in-three launch-week ratio are teaching assumptions, not measurements. Owner and revenue figures in section 2 are estimates made with a public method and are not reported figures from the studios.

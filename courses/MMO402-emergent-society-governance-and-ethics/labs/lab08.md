# MMO402 · Lab 08: A player charter

**Week:** 8 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the case analyses (30%); the charter is reused in the final governance design paper

## Objective

Turn Koster's 2000 declaration into something a studio could actually publish and be held to. You write a one-page charter of commitments for a fictional MMO, each one checkable, each with a named cost and a named collision with another right, and you set an exploit policy using the retroactive-risk model from [week 8](../lectures/w08-rights-of-avatars-koster-2000.md).

## Starter materials

**The fictional world.** *Saltmarch* is a subscription sandbox MMO with 120,000 monthly players on one shard. It has open-world PvP outside cities, player-run guilds with shared vaults, a player-driven market, a sanctioned real-money token, text and voice chat, and a volunteer review team of 40 players plus 6 staff moderators. Its terms of service currently say only: "We may suspend or terminate any account at any time for any reason." Its analytics team estimates that 3% of players are heavy explorers who try about 40 novel techniques a year, and everyone else tries about 3. Historically about 2% of novel techniques were later declared exploits, and the studio's logs detect about 60% of past uses once an exploit is declared.

**Reference texts.**
- Koster, "Declaring the Rights of Players" (raphkoster.com, 2000): all 19 articles.
- The article clusters table in section 1 of the week 8 lecture.
- The commitments table in section 5 of the week 8 lecture, as a model of the format.
- The week 8 interactive, `examples/w08-retroactive-risk.html`. If it is not yet built, use the formulas in section 3 of the lecture in a spreadsheet.

**Charter template (copy it).**

| # | Koster article(s) | Commitment ("We will ... within ..., and publish ...") | Measure and target | Cost to the studio | Collides with |
|---|---|---|---|---|---|
| 1 | | | | | |

## Steps

1. **Choose (15 minutes).** Pick eight articles, at least one from each cluster (equality, rule of law, liberty, accountability). Article 8 is compulsory.
2. **Draft commitments (30 minutes).** Write each as a checkable commitment in the template. "Players have the right to X" is not accepted. A commitment names an action, a time limit and something you publish.
3. **Measure (15 minutes).** Give each commitment a measure and a target, for example "95% of appeals answered within 72 hours, reported quarterly."
4. **Exploit policy (20 minutes).** Using Saltmarch's numbers, compute `r = q × d`, then the one-year and three-year ban risk for a heavy explorer and a typical player under retroactive, warn-first and notice-first policies. Compute the explorers' share of exploit bans in year one for the first two policies. Choose a policy for ambiguous exploits and a separate rule for obvious ones, and write your "obvious" test in one sentence.
5. **Collide (15 minutes).** For each commitment, name the right or interest it collides with and one realistic situation where keeping it hurts someone. Say which way you resolve it.
6. **Watch the watchers (15 minutes).** Write two commitments about staff conduct (articles 12, 14 or 15) that would have caught or deterred the 2007 EVE t20 incident described in the lecture. Say who monitors, and how a player reports a suspected breach safely.

## Deliverable

- The charter: one page, eight to ten rows in the template, plus the exploit policy in a short paragraph.
- A calculation sheet for step 4.
- A 400-word commentary explaining which article you found hardest to turn into a commitment and why, and which of your commitments you expect the studio's lawyers to resist.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Commitments are checkable | Every row names an action, a time limit and a published measure | Most rows checkable, some vague | Rights restated as slogans | 25% |
| Coverage | Eight or more articles, all four clusters, article 8 included | One cluster missing | Fewer than six articles | 10% |
| Exploit policy calculations | All risks and ban shares correct; policy follows from the numbers; clear obviousness test | Minor calculation error or vague test | Wrong model or no numbers | 25% |
| Costs and collisions | Every row has a realistic cost and collision, with a stated resolution | Some rows missing or generic | Missing | 20% |
| Staff accountability | Two commitments that would plausibly have caught the t20 case, with a safe reporting route | One weak commitment | Missing | 10% |
| Commentary | About 400 words, specific, argued | Generic | Missing | 10% |

<details>
<summary>Instructor check values</summary>

- `r = 0.02 × 0.6 = 0.012`.
- Heavy explorer, retroactive: one year (`N = 40`) `1 − 0.988^40 = 38.3%`; three years (`N = 120`) `1 − 0.988^120 = 76.5%`.
- Heavy explorer, warn first: one year `0.383 − 40 × 0.012 × 0.988^39 = 0.383 − 0.300 = 8.3%`; three years about 42.3%.
- Typical player, retroactive: one year (`N = 3`) 3.56%; three years (`N = 9`) 10.3%. Warn first: one year 0.04%; three years 0.49%.
- Year-one bans, retroactive: explorers `3,600 × 0.383 ≈ 1,379`, others `116,400 × 0.0356 ≈ 4,140`, explorers' share about 25%. Warn first: explorers `3,600 × 0.0833 ≈ 300`, others `116,400 × 0.00043 ≈ 50`, explorers' share about 86%.

</details>

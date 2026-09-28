# MMO402 · Lab 04: The allowed-play brief

**Week:** 4 ([lecture](../lectures/w04-wars-betrayals-and-meta-gaming.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish.
**Work mode:** individual (the in-lab calibration round is in pairs).
**Counts toward:** case analyses (30% of the course grade).

## Objective

Write a two-page case analysis of one documented betrayal, scam or heist from an online game. Apply the four-part allowed-play test from week 4, put a sourced real-money shadow on the loss, compare your model's verdict with what the operator actually did, and propose one policy change with its cost.

## Starter materials

**The test** (from the lecture, section 2):

```
allowed = M × S × T × N
M  means    only mechanics every player has (no exploit, bot, hacked client, stolen account)
S  stakes   everything taken and gained stays in the game's asset layer
T  target   aimed at characters, not at the person or at the operator's authority
N  notice   the victim could fairly have known this was possible
shadow = L × P     (loss in game currency × real price per unit at the time)
```

**Calibration cases** (used in Part A; the answer key is in the instructor block below). Each is a short constructed scenario in a fictional sandbox MMO whose rules match EVE Online's published scam policy.

1. A player sells a "rare blueprint" through the in-game contract system. The contract title says "Blueprint Original", but the item is a copy. The buyer did not read the contract details.
2. A corporation director gives a new recruit hangar access after two weeks. The recruit empties it and joins a rival.
3. A player finds that a crafting menu duplicates items when two players click at once, and uses it to fund a "bank" that pays generous interest.
4. A player runs a lottery with in-game currency, pays out honestly for a month, then keeps the last pot.
5. A player sends private messages signed "GM Tessel, Customer Support" asking for items "for verification".
6. A player in a voice server shares the real workplace of a rival alliance leader during a war.

**Case bank** (pick one for Part B, or propose another with the instructor's approval). Each has at least one reliable public source. You must find and cite your own sources, with dates.

- EVE Online: the Guiding Hand Social Club heist on Ubiqua Seraph (2005).
- EVE Online: the 700 billion ISK bank theft (2006).
- EVE Online: the Band of Brothers disbandment (2009).
- EVE Online: EBank (2009).
- Second Life: Ginko Financial (2007). Start from MMO401 week 8.
- Old School RuneScape: any documented scam wave the Jagex news pages or the Old School RuneScape Wiki describe, with a date.
- Any other online game, if you can find two independent sources that give dates and the operator's response.

**Template for the brief** (two pages, about 1,000 words, plus a table):

| Section | Content | Length |
|---|---|---|
| 1. Facts | What happened, when, the game's version or era, the operator's response, all cited | 200 words |
| 2. Test table | `M`, `S`, `T`, `N`, each with a 0 or 1 and one sentence of evidence | table |
| 3. Shadow | `L`, `P`, the source of `P` and its date, the result, and one sentence on what the shadow does and does not mean | 100 words |
| 4. Model versus ruling | Does the model's verdict match what the operator did? If not, which test explains the gap, or what does the model miss? | 250 words |
| 5. Policy change | One change to the operator's line, restoration rule or interface, and who gains and loses | 300 words |
| 6. Sources | Every factual claim, with dates | as needed |

## Steps

### Part A: calibration (30 min, pairs)

1. Score calibration cases 1 to 6 on `M`, `S`, `T`, `N` independently, then compare with your partner.
2. For every case where you disagree, write one sentence on which test caused it and why. Disagreements are expected on case 4 (was the lottery a scam or a gambling service?) and case 6 (is the voice server part of the operator's world?).
3. Check against the instructor key and note where your reading differed.

### Part B: research (60 min)

4. Pick a case from the case bank and collect at least two sources. Prefer the operator's own statements, then major news outlets, then maintained wikis. Record the access date for each.
5. Find a price `P` for the game's currency at the time of the event. Acceptable sources include an official exchange route (such as PLEX market history), a report that quotes a real-money value for a known in-game amount, or a published study. Record where the price came from. If you cannot find one, say so and give the shadow as a range at two defensible prices.

### Part C: write the brief (at home)

6. Fill the template.
7. In section 5, state your change as a rule a support agent could apply in under a minute. Then name one historical case, from the lecture or your research, whose verdict it would change.

## Deliverable

A PDF of two pages plus sources, named `lab04-<surname>.pdf`, and your Part A calibration sheet.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Facts and sourcing | Dated, versioned, at least two independent sources, operator response documented | One source, or dates missing | Unsourced claims | 20% |
| Test table | All four tests scored with specific evidence; borderline tests discussed | Scores given, evidence thin | Tests misapplied | 20% |
| Real-money shadow | Correct arithmetic, sourced `P` with date, limits of the shadow stated | Arithmetic right, `P` weakly sourced | Missing or wrong | 15% |
| Model versus ruling | Gap explained through a named test or a named limit of the model | Comparison made, explanation vague | No comparison | 20% |
| Policy change | Rule is concrete and quick to apply, winners and losers named, one case whose verdict changes | Change proposed, costs partly named | Opinion without a rule | 20% |
| Calibration sheet | All six cases scored, disagreements explained | Scored without explanations | Missing | 5% |

<details>
<summary>Instructor key for the calibration cases</summary>

1. `M = 1`, `S = 1`, `T = 1`, `N = 1`. Allowed play under an EVE-style policy. It is a presentation scam; the fix is interface friction (show "copy" in the title), not a verdict.
2. All pass. Allowed play. Corporate theft after infiltration is the standard EVE case.
3. `M = 0`. Duplication is an exploit, so the bank is a violation, whatever it does next. Expect some students to score the later bank default separately; the exploit alone decides the verdict.
4. All four pass in an EVE-style world, so it is allowed play. Discuss whether the operator has a separate gambling rule. Old School RuneScape's Code of Conduct bans player-run games of chance (Rule 13), which would fail it before the scam question arises.
5. `T = 0`. Impersonating staff. Violation.
6. `T = 0`. The target is the person. Discuss whether the operator's code of conduct reaches a voice server it does not run; a policy that says "no" leaves the victim without a remedy.

</details>

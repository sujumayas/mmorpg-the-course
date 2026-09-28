# GS101 · Lab 11: Free-to-play teardown

**Week:** 11 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** formative, feeds the timeline project (25%) and the close readings (40%)

## Objective

Take one free-to-play game apart as a business and as a design. You will list what its store sells, connect each item to a term of the revenue model from [week 11](../lectures/w11-free-to-play-mobile-and-live-service.md), estimate the model's numbers with honest ranges, and write a short critique of whose experience the store is built around.

The model you use:

```
monthly revenue R = N × p × A        ARPU = p × A
share of revenue from the top fraction q of payers = q^(1 − 1/α)
expected lifetime L = 1 / (1 − r)    LTV = ARPU × L
```

## Starter materials

- A spreadsheet (Google Sheets, Excel or LibreOffice Calc).
- A free-to-play game you can open during the lab, on phone or PC. It must have been live for at least a year. You may not choose Candy Crush Saga, because the reference row below already uses King's figures.
- The reference row, which everyone enters first to check their formulas:

| Row | N (monthly players) | p | A (US$ per payer per month) | R per month | ARPU |
|---|---|---|---|---|---|
| King, Q4 2013 (F-1/A, March 2014) | 304,000,000 | 0.040 | 17.32 | ≈ 210,611,200 | ≈ 0.69 |

- A blank store inventory table with these columns: item name, price (real currency, converting premium currency at the best-value bundle rate), type (cosmetic, convenience, content, power, random), is it time-limited (yes/no), which model term it targets (`N`, `p`, `A`, `r`), one-line reason.
- A blank sensitivity table: rows for `p` = 1%, 2%, 4%, 8%; columns for three values of `A` you choose.

## Steps

1. **Formula check (15 min).** Enter the King reference row with formulas, not typed results. Your R must come to about US$210.6 million per month and about US$632 million per quarter. Add a cell for players needed per subscriber at US$15, World of Warcraft's monthly price (it should read about 21.7).
2. **Store inventory (30 min).** Open your game's store and record at least 12 items or bundles. Convert premium-currency prices to real money and show the conversion rate in a cell. Classify each item and name the term it targets.
3. **Context and history (15 min).** Record the game's release date, platform, developer, region and business-model history (did it launch free, or switch?). Cite a source for each. Add one row to your course timeline.
4. **Estimate N, p and A (20 min).** Search for published figures (company reports, filings, official announcements). Where there are none, give a low and a high estimate and explain the basis in one sentence each. Never present a guess as a fact.
5. **Sensitivity (15 min).** Fill the sensitivity table with your N and the `p` and `A` values. Highlight the cells consistent with any revenue figure you found.
6. **Spending shape (15 min).** Choose `α` for your game's payers, using the week 11 interactive. Justify it from the store: a store full of expensive random items suggests a small `α`; a store built around one fixed-price pass suggests a larger one. Compute the top 10% share and the median payer's spend at your `A`.
7. **Retention (10 min).** Pick a plausible monthly retention `r` and compute LTV. Name two features in the game that exist to raise `r`.
8. **Critique (at home).** Write the memo described below.

## Deliverable

The spreadsheet, and a memo of about 600 words that:

- names the player the store is designed around, using at least three items from your inventory as evidence;
- states your `p`, `A` and `α` estimates and what they imply for the median payer versus the average;
- describes what the game is like for a player who never pays;
- ends with one claim a reader could disagree with, in the form "This store is built for X, so Y."

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Formula check | King row reproduces US$210.6 million a month and 21.7 players per subscriber from formulas | Right values but typed in, or one formula wrong | Wrong or missing | 10% |
| Store inventory | 12+ items, prices converted correctly, every item classified with a plausible target term | Fewer items or some misclassified | Incomplete | 25% |
| Sourcing and estimates | Every fact cited with date; estimates given as ranges with stated basis | Some unsourced figures, or guesses presented as facts | Numbers without sources | 20% |
| Sensitivity, shape and retention | All three computed correctly and tied back to store evidence | Computed but not connected to the store | Missing or wrong | 20% |
| Memo | Clear, arguable claim supported by inventory and numbers; the non-paying player described | Claim present but thinly supported | Description with no claim | 25% |

<details>
<summary>Instructor check values</summary>

- King row: `304,000,000 × 0.04 × 17.32 = 210,611,200` a month; quarter ≈ 631.8 million; ARPU 0.6928; 15 / 0.6928 ≈ 21.65.
- With `α = 1.43`, top 10% share = 0.1^(1 − 1/1.43) ≈ 0.50. With `A = 17.32`, the median = `17.32 × 0.43/1.43 × 2^(1/1.43)` ≈ 8.46.
- With ARPU 0.69 and `r = 0.9`, LTV = 6.90.
- Watch for students converting premium currency at the smallest bundle's rate, which overstates prices. Accept either rate if it is stated.

</details>

# MMO301 · Lab 10: The crowd audit

Assigned in week 10 ([lecture](../lectures/w10-immersion-identity-and-the-avatar.md)). Due at the start of week 12. Marked with the rubric below; it feeds the identity chapter of your world design bible.

## Objective

Measure how many distinct looks a character creator really gives a crowd. You will compute `M`, `c`, `M_eff` and the chance of twins from a sample of characters, compare the independent-categories estimate with the twins actually observed, and write a redesign memo that raises `M_eff` for a stated cost. The skill you are practising is turning "players feel like clones" into a number you can change.

## Starter materials

Everything below is included in this file. The game, "Harbourlight," is invented.

**1. Harbourlight's creator.** Four categories: Face (8 options, F1 is the default), Hairstyle (10 options, H1 default), Hair colour (12 options, C1 default), Skin tone (6 options, S1 default). `M = 5,760`.

**2. Sample of 120 characters seen in Harbourlight's main plaza, one evening.** Counts of each option, listed from most to least common. The first option in each row is the default.

| Category | Counts per option (default first) | Total |
|---|---|---|
| Face | 44, 14, 12, 11, 10, 10, 10, 9 | 120 |
| Hairstyle | 50, 12, 10, 9, 8, 8, 7, 6, 5, 5 | 120 |
| Hair colour | 38, 16, 12, 10, 8, 8, 7, 6, 5, 4, 3, 3 | 120 |
| Skin tone | 42, 26, 20, 14, 10, 8 | 120 |

**3. Exact looks observed.** In the same sample, grouping characters whose four choices all match:

| Look | Characters |
|---|---|
| F1 H1 C1 S1 (all defaults) | 9 |
| F1 H1 C2 S1 | 3 |
| F1 H1 C1 S2 | 2 |
| F2 H1 C1 S1 | 2 |
| F1 H2 C1 S3 | 2 |
| Every other look | 1 each (102 characters) |

**4. Spreadsheet layout.** One sheet per category with columns `option`, `count`, `share p = count / total`, `p²`, and a cell for `c_j = Σ p²`. A summary sheet with `c = Π c_j`, `M_eff = 1/c`, a table of `n` from 2 to 200 with pairs `n(n−1)/2`, `E = pairs × c` and `P = 1 − EXP(−E)`, and a line chart of P against `n`.

## Steps

1. Build the four category sheets and compute each `c_j`. Check: the face category gives `c_j ≈ 0.193`.
2. On the summary sheet, compute `c` and `M_eff` assuming independent categories. Find the crowd size at which P(twin) reaches 50%, using `n ≈ ½ + √(¼ + 2 ln 2 / c)`, and check it against your P column.
3. Compute the observed collision rate from table 3. Count twin pairs within each group (`g(g − 1)/2` for a group of `g`), add them up, and divide by the total number of pairs among 120 characters (7,140). Its inverse is the observed `M_eff`.
4. Compare the independent estimate with the observed value. Explain the gap in two or three sentences. (Hint: are players who keep one default more likely to keep the others?)
5. Also compute the expected number of all-default characters under independence (`120 × Π (default share)`) and compare with the 9 observed.
6. Design two changes to the creator. For each, rebuild the category sheets with your predicted new counts (state your assumptions) and compute the new `M_eff` under independence. At least one change must address the correlation you found in step 4.
7. Write the memo.

## Deliverable

- The spreadsheet with all sheets and the chart.
- A 400-word memo to the Harbourlight art director that states the current `M_eff` (both estimates), the crowd size for even odds of twins in the plaza, your two changes with their predicted `M_eff`, and the cost of each (art time, player time at creation, or player dissatisfaction). End with one recommendation.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Computation | `c_j`, `c`, `M_eff`, P curve and 50% crowd size all correct and traceable in the sheet | Minor arithmetic errors, method right | Method wrong or values hard-coded | 30% |
| Observed vs independent | Observed `M_eff` correct; gap explained by correlated default-keeping with evidence from table 3 | Gap noted, explanation vague | Not attempted or misread | 20% |
| Redesign | Two changes, predicted counts justified, one targets correlation, new `M_eff` computed | Two changes with weak justification | One change or no numbers | 25% |
| Memo | Clear numbers, honest costs, a single recommendation a director could act on | Numbers present, costs thin | Restates the method, no recommendation | 25% |

Instructor check values: `c_j` ≈ 0.193, 0.214, 0.154, 0.222; independent `c ≈ 0.00141`, `M_eff ≈ 707`, even odds at about 32 players; observed twin pairs 42, observed `c ≈ 0.00588`, observed `M_eff ≈ 170`; expected all-default characters under independence ≈ 2.0 against 9 observed.

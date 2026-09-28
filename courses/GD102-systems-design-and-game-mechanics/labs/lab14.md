# GD102 · Lab 14: Tune an idle economy

**Assigned:** week 14 ([lecture](../lectures/w14-tuning-with-spreadsheets.md)). **Due:** start of week 15 (final). **Feeds:** the tuning appendix of the final system design document (40%).

## Objective

Build a spreadsheet model of a rising-price economy with a greedy buyer, then hit three design targets by tuning inputs. For each target you will name the knob you changed, show with a sensitivity table why you chose it over the alternatives, and record what else it moved. The point of the lab is the judgment, not the arithmetic: two knobs can hit the same target and do very different things to the rest of the game.

## Starter materials

Build the workbook from the description below in Excel, LibreOffice Calc or Google Sheets. The numbers are the base values of Cookie Clicker's first four buildings (Cookie Clicker Wiki, current web version), renamed so you design your own game rather than copy theirs.

### Tab 1: Inputs

| Name | Base price | Base output (per second) | Notes |
|---|---|---|---|
| Tapper | 15 | 0.1 | Cookie Clicker's Cursor |
| Helper | 100 | 1 | Cookie Clicker's Grandma |
| Field | 1,100 | 8 | Cookie Clicker's Farm |
| Quarry | 12,000 | 47 | Cookie Clicker's Mine |
| Foundry | (you design) | (you design) | New building, target B |

| Name | Value | Notes |
|---|---|---|
| `growth` | 1.15 | Price multiplier per purchase of the same building |
| `purchases` | 150 | Rows in the Sim tab |

Color every input cell pale yellow. Define a named range for each (for example `helper_price`, `helper_output`, `growth`).

### Tab 2: Sim (one row per purchase)

Columns, left to right:

| Column | Header | Formula idea (row 3 onward) |
|---|---|---|
| A | Purchase # | `=A2+1` (row 2 holds 1) |
| B to F | Owned before this purchase: Tapper, Helper, Field, Quarry, Foundry | Row 2 is all 0. Each later row: previous row, plus 1 if the previous row bought this building. `=B2+($L2="Tapper")` |
| G to K | Payback of the next purchase, one per building | `=tapper_price*growth^B2/tapper_output` and so on |
| L | Buys | `=INDEX($G$1:$K$1, MATCH(MIN(G2:K2), G2:K2, 0))`, with row 1 of G to K holding the building names |
| M | Payback of this purchase | `=MIN(G2:K2)` |

If you have not designed the Foundry yet, give it a base price of 10^12 so it is never bought.

### Tab 3: Checks

| Check | Formula idea | Pass condition |
|---|---|---|
| Helpers owned at first Quarry | Find the first row where L = "Quarry", read column C | Target A |
| Settled gap Helper minus Foundry | Row 150: C minus F | Target B |
| Settled gap Helper minus Tapper | Row 150: C minus B | Target C |
| Largest jump in payback between consecutive purchases, rows 20 to 150 | `MAX` of `M(n+1)/M(n)` | below 1.20 |

Use conditional formatting so each check cell is green when it passes and red when it fails.

### Baseline check values

Before tuning anything, your sheet must reproduce these (from the week 14 lecture):

- First five purchases: Helper, Helper, Helper, Field, Tapper.
- First Quarry at purchase 17, with 7 Helpers owned.
- After 40 purchases: Tapper 10, Helper 13, Field 11, Quarry 6.

If any of these differ, fix the sheet before going on. The usual causes are a relative reference that shifted when filled down, or "owned" counting after the purchase instead of before it.

## Steps

1. **Build and verify (40 min).** Build the three tabs. Reproduce the baseline check values. Add a chart of column M (payback of each purchase) against purchase number, colored by building if your program allows.
2. **Target A: the first Quarry arrives at exactly 10 Helpers (25 min).** First, predict the range of Quarry base prices that achieves it using the lecture's boundary method (payback of the 10th and 11th Helper). Then confirm in the sheet by stepping the price. Pick a value with margin on both sides and justify it.
3. **Target B: design the Foundry (30 min).** The Foundry must settle 10 ± 0.5 purchases behind the Helper. Use the gap formula `ln(payback ratio) / ln(growth)` to find the base payback it needs. Choose an output (per second) that fits your game's fiction, then the price. Check the settled gap at row 150. Also report the purchase number of the first Foundry.
4. **Target C: the Tapper stays 4 ± 0.25 purchases behind the Helper (30 min).** There are at least two ways to do this: change `growth`, or change the Tapper's price or output. Do both, in two copies of the workbook. For each, record all four checks. One of them will break target A or B. Say which and why.
5. **Sensitivity table (25 min).** On a new tab, build a one-at-a-time sensitivity table. Inputs: `growth` at 1.10, 1.12, 1.15, 1.18, 1.20; Quarry price at −20%, −10%, 0, +10%, +20%; Tapper output at −20%, −10%, 0, +10%, +20%. Outputs: the three target checks. Draw it as a tornado chart for "Helpers owned at first Quarry."
6. **Memo (30 min).** Write the tuning memo described below.

## Deliverable

- The workbook with all tabs and the final tuned inputs, every check green.
- The second workbook copy from step 4 (the alternative you rejected).
- A tuning memo of 400 to 600 words that, for each target, states: the knob you changed, its old and new value, the range that would also work, what else the change moved (with numbers from your checks or sensitivity table), and why you rejected the alternative. End with one paragraph on what the greedy model leaves out and how that could change your numbers in a real game.
- A change log with one line per input change, in the format from the week 13 lecture.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Weight |
|---|---|---|---|---|
| Model correctness | All baseline values reproduced; inputs referenced by name; no typed numbers in formulas | Baseline reproduced, some hard-coded values | Baseline not reproduced | 20% |
| Targets A and B | Predicted ranges derived by formula and confirmed in the sheet; chosen values have margin | Targets met by trial and error, no prediction | A target not met | 20% |
| Target C and knob comparison | Both approaches built; the broken target identified and explained with numbers | Both built, explanation thin | One approach only | 20% |
| Sensitivity and tornado | Table complete, chart sorted by swing, most sensitive input named | Table present, chart missing or unsorted | Missing | 15% |
| Tuning memo | Every target has knob, range, side effects and a rejected alternative, all with numbers; limits of the greedy model discussed | Memo covers targets without side effects or ranges | Missing or restates the steps | 20% |
| Change log | One dated line per change with a reason | Partial | Missing | 5% |

## Instructor check values

- Target A at `growth = 1.15`: Quarry base price between 16,534 and 19,014 (output 47). The boundary values are ties.
- Target B at `growth = 1.15`: Foundry base payback about `100 × 1.15^10 ≈ 404.6` s. For example output 260 and price 105,000 give 403.8 s and a settled gap of 10 at row 150 (Helper 35, Foundry 25, with Quarry at 17,500).
- Target C by `growth`: gap `ln 1.5 / ln g` between 3.75 and 4.25 needs `g` between about 1.100 and 1.114. At `g = 1.11` the gap is 3.89, and target A then needs a Quarry price between about 12,023 and 13,345, so a Quarry tuned for 1.15 breaks target A.

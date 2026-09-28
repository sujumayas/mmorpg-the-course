# GS101 · Lab 04: The crash spreadsheet

**Week:** 4 · **Time:** 2 hours in the lab plus up to 3 hours at home · **Weight:** part of the timeline project (the 1982 to 1985 entries)

**Lecture:** [Week 04, home consoles and the 1983 crash](../lectures/w04-home-consoles-and-the-1983-crash.md)

## Objective

Build the lecture's shelf model in a spreadsheet, reproduce its table, and use it to test three competing explanations of the 1983 crash. Then write a short, sourced argument about which cause mattered most. You will practise the difference between what a model shows (a mechanism) and what the historical record shows (evidence), and you will need both.

## Starter materials

Everything below is described here. There is nothing to download.

- **Software.** Google Sheets, LibreOffice Calc or Excel. Python is allowed if you also hand in a table and a chart.
- **Parameter block.** Put these in named cells at the top of your sheet so every formula refers to them:

| Name | Meaning | Default |
|---|---|---|
| `D1`, `S1` | Year-1 demand and shipments (thousand cartridges) | 100, 100 |
| `dg` | Year-2 demand growth | 100% |
| `sg` | Year-2 supply growth | 175% |
| `later` | Demand change per year from year 3 | 0% |
| `c` | Bargain share of demand the bin can capture | 0.5 |
| `P`, `b` | Full price and bin price | $35, $5 |
| `shock_year`, `shock_size` | Year and size of a one-time demand drop | off (use year 4, 50% when on) |
| `gate` | Licensing gate headroom, shipments capped at `gate × D` | off (use 1.00 when on) |

- **Row layout.** One row per year, 1 to 5, with columns Year, D, S, S_eff, bin_sold, new_sold, U_after, Revenue. Units are thousand cartridges, so Revenue is in $ thousands, as in the lecture. The formulas are exactly those in section 2 of the lecture:

```
bin_sold  = MIN(U_before, c × D)
new_sold  = MIN(S_eff, D − bin_sold)
U_after   = U_before − bin_sold + (S_eff − new_sold)
Revenue   = P × new_sold + b × bin_sold
```

- **Fact sheet.** Use only these facts, each from the lecture's Sources, plus any you find and cite yourself:
  1. Atari games on the market went from about 100 (June 1982) to over 400 (December 1982).
  2. A 1983 Goldman Sachs analyst estimated demand +100% and manufacturing output +175% year on year.
  3. Launch prices of about $35 fell to about $5 in discount bins after returns failed.
  4. Commodore cut the C64 to $300 in June 1983, and some stores sold it for $199.
  5. US home video game sales fell from about $3 billion at the 1982 peak to about $100 million (1985).
  6. E.T. sold over 2.6 million copies in 1982, and at least 669,000 were returned in 1983. Ray Kassar later said about 3.5 million of 4 million produced came back.
  7. Nintendo's third-party terms included at most five games per year and a minimum order of 10,000 cartridges.

## Steps

1. **Reproduce.** Build the model with the default parameters. Your years 1 to 5 must match the lecture's table exactly (year 3 revenue $4,750, year 5 unsold stock 300). Do not continue until they do.
2. **Sensitivity to `c`.** Copy the sheet and vary `c` from 0 to 1 in steps of 0.25. Record year-5 revenue and year-5 unsold stock for each value. Check: `c = 1` gives year-5 revenue $1,000.
3. **Scenario A, supply only.** Defaults. This is "the market flooded."
4. **Scenario B, demand only.** Set `sg` equal to `dg` (both 100%), then turn on the demand shock (year 4, 50%). This is "home computers took the buyers."
5. **Scenario C, both.** Defaults plus the demand shock. Check: year-4 revenue $2,000, year-5 unsold stock 500.
6. **The gate.** Turn on the gate in scenario C. Find the loosest headroom (step 0.01) that keeps `U_after < 0.5 × D` every year. Record the year-5 revenue at that value. Check: 1.08, with year-5 revenue $2,300.
7. **Chart.** One chart with revenue by year for scenarios A, B, C and C-with-gate. Label each line. A second chart with unsold stock by year for the same four.
8. **Argue.** Write 400 words answering this question. Which cause did the most damage between 1982 and 1985, the supply flood or the loss of demand? Use your scenario results as the mechanism and at least three items from the fact sheet (or your own cited sources) as evidence. Include one sentence on what the model cannot tell you.

## Deliverable

The spreadsheet (parameter block, four scenario sheets, `c` sensitivity table, both charts) and the 400-word argument with a source list. Name the file `GS101-lab04-<surname>`.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Model reproduction | All five years match the lecture; formulas use named parameters | One value off, or hard-coded numbers in formulas | Table does not match | 25% |
| Scenarios and gate | A, B, C correct with check values; gate value found and justified | One scenario or the gate missing | Several scenarios wrong or missing | 20% |
| Charts | Both charts labeled, all four scenarios readable | One chart missing or unlabeled | No charts | 10% |
| Argument | Clear claim; mechanism from the model and evidence from sources both used; states a limit of the model | Claim supported by model or by sources, not both | No clear claim | 30% |
| Source handling | Every fact cited; the E.T. disagreement handled honestly if used | Most facts cited | Uncited or legend repeated as fact | 15% |

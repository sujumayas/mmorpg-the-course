# MMO401 · Lab 13: Reading a year of reports

**Assigned:** week 13. **Due:** start of week 14. **Weight:** part of the ABM labs component (40%).
**Lecture:** [Week 13, reading an economic report](../lectures/w13-reading-an-economic-report.md).

## Objective

Read twelve months of economic reports for one invented MMO the way an in-house economist would. You will reconcile every month with the stock-flow identity, decompose every price change with the equation of exchange, find the month with an exploit, and write short readings a producer could act on. The code you write here is the diagnostic step of your final policy memo.

## Starter materials

Python 3 with the standard library, or any spreadsheet. Save the data below as `mmo401_reports.csv`. Money is in billions of crowns. `sink_sales_tax` is 2% of `trade_value`, rounded to one decimal. `volume_index` is real trade volume at fixed prices.

```
month,active_players,money_start,faucet_bounties,faucet_quests,faucet_npc_sales,sink_sales_tax,sink_repairs,sink_other,money_end,trade_value,volume_index
1,50000,1000.0,85,35,20,81.8,20,12,1023.2,4092.4,100
2,50500,1023.2,86,35,20,84.1,20,12,1046.1,4205.3,100.5
3,51000,1046.1,87,36,20,86.0,21,12,1067.1,4300.4,101
4,51000,1067.1,87,36,21,88.1,21,12,1088.0,4406.4,101.5
5,58000,1088.0,98,44,22,85.5,22,13,1125.5,4276.9,102
6,57000,1125.5,96,42,22,88.7,23,13,1151.8,4434.4,103
7,56000,1151.8,94,40,22,92.6,23,13,1172.2,4630.2,104
8,56000,1172.2,95,40,22,102.7,23,13,1252.5,5135.2,104
9,55500,1252.5,93,39,22,108.1,23,13,1257.4,5406.8,104.5
10,55000,1257.4,92,39,21,110.8,23,13,1258.6,5537.8,105
11,54500,1258.6,91,38,21,101.4,22,13,1268.2,5072.4,103
12,54000,1268.2,90,38,21,106.8,22,13,1271.4,5339.9,104
```

Context the producer gave you, as it would arrive in real life (some of it is irrelevant):

- Month 5 shipped an expansion with a free trial.
- Month 8 had a server crash and a hotfix. Nobody filed an economy ticket.
- Month 10 the team announced that the sales tax rises to 4% at the start of month 13.
- Months 9 and 10 had a seasonal event with cosmetic rewards bought with crowns from an NPC vendor. That vendor's income is booked under `sink_other`.

A starter script, `read_reports.py`:

```python
import csv

def load(path="mmo401_reports.csv"):
    with open(path) as f:
        return [{k: float(v) for k, v in row.items()} for row in csv.DictReader(f)]

def month_stats(r, prev=None):
    F = r["faucet_bounties"] + r["faucet_quests"] + r["faucet_npc_sales"]
    S = r["sink_sales_tax"] + r["sink_repairs"] + r["sink_other"]
    out = {"month": int(r["month"]), "F": F, "S": S}
    out["R"] = r["money_end"] - (r["money_start"] + F - S)
    # TODO: residual share, sink coverage, V, P, money per player,
    #       effective tax rate, and growth rates gM, gV, gQ, gP vs prev
    return out

if __name__ == "__main__":
    rows = load()
    prev = None
    for r in rows:
        print(month_stats(r, prev))
        prev = r
```

## Steps

1. **Reconcile.** For every month compute `F`, `S`, `R = M_end − (M_start + F − S)`, the residual share `R / (F − S)`, and sink coverage `S / F`. Plot `R` by month.
2. **Check the tax rule.** Compute the effective rate `sink_sales_tax / trade_value` each month. It should be 2.0% within rounding. Say in one sentence what you would suspect if it were not.
3. **Decompose.** Compute `V = trade_value / money_end` and `P = trade_value / volume_index`. For months 2-12, compute `gM`, `gV`, `gQ` and exact `gP`, and the approximation `gM + gV − gQ`. Plot the three components as stacked bars with exact `gP` as a line.
4. **Per capita.** Compute money per active player in millions. Plot it next to total money. Mark the months where they move in opposite directions.
5. **Find the exploit.** One month has a residual far outside the others. Name it, give the residual and its share of net flow, and estimate how much of that month's price rise it explains. (Hint: recompute `gM` as if the residual had been −4, keep `gV` and `gQ` as reported, and compare `gP`.)
6. **Explain month 11.** Prices fell sharply while money grew. Use the decomposition and the producer's context to give the most likely cause, and say what data cut would confirm it.
7. **Write three readings.** Five lines each, following the lecture's format, for months 5, 8 and 11.
8. **One recommendation.** In 150 words, say whether the planned tax rise to 4% should go ahead, using sink coverage and money per player from the last three months. You will test this properly with a model in [week 14](../lectures/w14-intervention-design.md).

Checkpoints so you know you are on track: month 1 has `R = −3.0` and coverage 0.813. Month 5 has `gV ≈ −6.2%` and exact `gP ≈ −3.4%`. The exploit month's residual share is above 3.

## Deliverable

A zip with your finished `read_reports.py` (or the spreadsheet), a results CSV with one row per month and every computed column, three plots (residual, decomposition, per capita) as PNG, and a Markdown or PDF file with the step 5 and 6 answers, the three readings and the recommendation.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) |
|---|---|---|---|
| Reconciliation and tax check (steps 1-2) | All months correct; residual plot clear; tax suspicion stated precisely | Minor arithmetic slips or unclear plot | Identity not applied or many months wrong |
| Decomposition (steps 3-4) | Exact and approximate `gP` for every month; plots readable; opposite-direction months marked | Decomposition done but plots or marks incomplete | No decomposition, or velocity computed from the wrong money figure |
| Exploit and month 11 (steps 5-6) | Correct month, residual and counterfactual `gP`; month 11 cause tied to the announcement with a confirming data cut | Right month found, counterfactual or data cut missing | Wrong month or cause asserted without numbers |
| Readings (step 7) | Five lines each, every line with a number, action sized or explicitly "none" | Readings present but vague or overlong | Missing or restate the charts without explaining them |
| Recommendation (step 8) | Uses coverage and per-player money from months 10-12; names who pays | Recommendation without numbers | Missing |

Total 20 points, scaled to the lab weight.

<details>
<summary>Instructor key (remove before handing out)</summary>

- Residuals are between −2 and −9 every month except month 8, where `R = +62.0`, share 3.39 of net flow. Month 8: `gM = +6.85%`, `gV = +3.80%`, `gQ = 0`, exact `gP = +10.9%`. With `R = −4` instead, `M_end = 1,186.5`, `gM ≈ +1.22%`, and exact `gP ≈ +5.1%`, so the exploit explains a bit more than half of that month's price rise. Month 8 context points to the crash and hotfix as a possible duplication window.
- Month 5: `gM = +3.45%`, `gV = −6.17%`, `gQ = +0.49%`, `gP = −3.41%`. Money per player fell from 21.33M to 19.41M while total money rose.
- Month 11: `gV = −9.10%`, `gQ = −1.90%`, `gP = −6.63%`. Traders waiting for, or reacting to, the announced tax change is the expected answer; a velocity cut by account type (traders versus others) would confirm it. The event in months 9-10 is a distractor. The context says its vendor income is booked under `sink_other`, yet `sink_other` stays at 13 in those months. Give credit to a student who spots that the event revenue does not appear and asks where it went, because that is a reporting gap worth a ticket.
- Coverage rises from 0.81 to about 0.95 by month 12 and money per player growth slows to about 1% a month. A strong answer argues the tax rise is less urgent than it looked in month 8 and asks whether it is aimed at the exploit's money, which a rollback would handle better.

</details>

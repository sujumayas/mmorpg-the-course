# MMO401 · Lab 10: Loss rules in an agent-based economy

**Week:** 10 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** part of the ABM labs (40%)

## Objective

Take a small agent-based economy of pilots, ships and a crafter, and make its loss rules explicit in the `(h, r, insurance)` form from [week 10](../lectures/w10-scarcity-by-design-full-loot-and-destruction.md). Then run three loss policies for a simulated year and show, with numbers from both ledgers, which one you would ship and why.

The lab tests one idea from the lecture above all: the victim feels `h`, the item stock feels `h × (1 − r)`, and insurance moves only the currency ledger.

## Starter materials

- [`lab10-starter.py`](lab10-starter.py), a standard-library Python 3 script (no packages needed). It simulates 2,000 pilots for 365 days. Each day pilots earn 50,000 gold, every ship owner flies, a flying ship is lost with chance `H_OUTING`, and a lost ship's 4 fittings each survive to the killer with chance `R`. A crafting sector builds 40 ships a day and sells them at a price that moves 3% a day toward clearing. A 5% sales tax on each ship sale is destroyed. The script prints the stock, price and a ledger of flows.
- The parameters live at the top of the file. The places you must edit are marked `TODO`.
- Your week 10 notes, especially the item ledger (`S* = F / δ`) and the currency ledger (insurance in, tax out).

Run it once as given with `python3 lab10-starter.py` and keep the output. With the default seed of 401, the final line should report 13,660 hulls destroyed and 14,586 ships sold. If yours differs, check your Python version with the instructor before continuing.

## Steps

1. **Read the model.** In a short table, map each part of the script to the lecture's symbols: which line is `h`, which is `r`, which is `F`, which is `I`, which is `τ`. Note one way the script differs from the lecture's model (for example, the price rule).
2. **Make `r` matter.** In the starter, looted fittings pile up in hangars and nothing uses them. Add a fittings market. Each new ship needs 4 fittings. A buyer who owns spare fittings uses those first and buys only the rest from a second crafter that builds 150 fittings a day at a posted price with the same 3% adjustment rule. Now a high `r` should mean fewer fittings bought.
3. **Build the currency ledger.** Record the money supply `M` (total pilot gold plus crafter gold, once you model the crafters as holders of gold) at the start and end of every day. Check the identity `M(end) = M(start) + faucets − sinks` every day and assert that the residual is zero. If it is not, you have a leak in your own code, and finding it is part of the lab.
4. **Run three policies,** each with the same seed and for 365 days:
   - A. Full-loot transfer: `R = 1.0` for fittings, no insurance.
   - B. EVE-like: `R = 0.5`, `INSURANCE = 100,000` per hull.
   - C. Destroy everything: `R = 0.0`, no insurance.
   For each, report at day 365: ships in the world, ship price, fittings in the world (including spares), fittings price, fittings crafted per day over the last 30 days, total insurance paid, total tax destroyed, and the net change in `M`.
5. **One battle.** In policy B, add a battle on day 180 that destroys 300 ships at once under the same rules. Plot ship price and `M` for days 150 to 250. Describe what happened on each ledger in two sentences each.
6. **Sensitivity.** For policy B only, run 5 seeds and report the mean and range of the day-365 ship price. Say whether the differences between policies in step 4 are larger than the seed-to-seed spread.

## Deliverable

1. Your modified script, runnable with `python3`.
2. A results table for step 4 and the plot from step 5.
3. A memo of about 400 words to a lead designer recommending one of the three policies for a game whose crafting players are 20% of the population. The memo must cite at least four numbers from your runs, separate what the victim loses from what the world loses, and state the net currency effect of your chosen policy per simulated month.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Model mapping (step 1) | Every symbol mapped correctly, one real difference from the lecture named | Most symbols mapped | Missing or mostly wrong | 10% |
| Fittings market (step 2) | Spares used before buying, second crafter with price rule, `r` visibly changes fittings demand | Market added but spares ignored or price fixed | Not done | 20% |
| Ledger identity (step 3) | Daily residual asserted zero, any leak found and explained | Ledger kept but not checked every day | Missing | 20% |
| Policy runs and battle (steps 4-5) | All figures reported for three policies, battle plotted and explained on both ledgers | One policy or the battle incomplete | Two or more missing | 25% |
| Sensitivity (step 6) | Five seeds, spread compared with policy differences | Seeds run, no comparison | Missing | 10% |
| Memo | Recommendation argued from the numbers, victim and world separated, net currency effect stated | Recommendation made, numbers thin | Opinion without numbers | 15% |

<details>
<summary>Instructor check values</summary>

- Unmodified starter, seed 401 (tested on Python 3.13): day 365 has 1,952 ships in the world, a price of 1,673,964 gold, 13,660 hulls destroyed, 14,586 ships sold, 27,306 fittings destroyed and 27,334 looted, and 842,963,699 gold of tax.
- Unmodified starter with `R = 1.0` or `R = 0.0` gives the same ship count and price as the default, because nothing uses fittings yet. That is the point of step 2. Students who report different ship prices across A and C before step 2 have changed something else.
- Unmodified starter with `R = 0.5` and `INSURANCE = 100,000` pays 1,366,300,000 gold of insurance, about 1.5 times the 886,524,436 gold of tax taken in that run. Expect students to find policy B a net faucet relative to A and C.
- The income faucet (36.5 billion over the year) dwarfs both insurance and tax, so ship prices rise under every policy. Good memos notice this and say that loss rules cannot fix an economy whose main faucet is out of balance.

</details>

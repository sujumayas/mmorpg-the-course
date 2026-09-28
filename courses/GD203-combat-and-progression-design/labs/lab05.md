# GD203 · Lab 05: Burst, sustain and the crossover

**Assigned:** week 5. **Due:** start of week 6. **Weight:** part of the spreadsheet labs (40% of the course).
**Lecture:** [Week 5, DPS, burst and sustain](../lectures/w05-dps-burst-and-sustain.md). **Interactive:** [Burst vs sustain](../examples/w05-burst-vs-sustain.html), for checking your numbers.

## Objective

Build a time-step spreadsheet that computes cumulative damage for three weapons, finds where each pair of weapons swaps the lead, and computes time-to-kill against targets that regenerate. Then tune one weapon so it wins a stated band of fight lengths and loses outside it.

## Starter materials

Create these yourself in any spreadsheet tool. All numbers are fictional.

**Weapons.** `n = ∞` means the weapon never reloads.

| Weapon | d | n | Δ (s) | R (s) |
|---|---|---|---|---|
| Blunderbuss | 120 | 2 | 0.6 | 3.0 |
| Carbine | 30 | 8 | 0.4 | 2.0 |
| Wand | 14 | ∞ | 0.25 | 0 |

**Targets.** Health 100, 240, 400, 800 and 2,000. Regeneration 0, 20 and 50 per second.

**Check values.** One blunderbuss cycle lasts `2 × 0.6 + 3.0 = 4.2` s and deals 240, so its sustained DPS is about 57.1. The wand's sustained DPS is 56.

## Steps

1. **Summary table.** For each weapon compute alpha, burst DPS `d / Δ`, clip damage `n × d` and sustained DPS `n × d / (n × Δ + R)`.
2. **Hit schedule.** On a new tab, make a time column from 0 to 60 s in steps of 0.05 s. For each weapon, add a column that is 1 when a hit lands at that time and 0 otherwise. Use the cycle rule from lecture section 2: hits at `c × L + k × Δ` for `k = 0 .. n − 1`, with `L = n × Δ + R`. Hint: `MOD(t, L)` tells you where you are in the cycle. Round times to avoid floating-point misses.
3. **Cumulative damage.** Add a running total `D(t)` for each weapon. Chart all three on one line chart from 0 to 30 s.
4. **Crossovers.** For each pair of weapons, list every time at which the leader changes. Write the pair's "final" crossover, after which the lead no longer changes within 60 s.
5. **TTK without regeneration.** For each weapon and each target health, find the first time `D(t) ≥ H`. Build a 3 × 5 table and mark the fastest weapon in each column.
6. **TTK with regeneration.** Add a target-health column per weapon that starts at `H`, rises by `r × 0.05` each step (capped at `H`) and drops by `d` on each hit. Record the kill time, or "never" if there is none by 60 s. Fill a table for all targets at `r = 20` and `r = 50`.
7. **Tune.** Change exactly one parameter of the carbine so that it is the fastest weapon against the 800-health target and not the fastest against either 100 or 240. Then say what your change did to the carbine's rank against 2,000 health, and explain why no single-parameter change makes the carbine fastest at 400 health without also making it fastest at 2,000. Record the parameter, its old and new value, and the new TTK table.
8. **Explain one cliff.** Find the largest single jump in any weapon's TTK between two neighbouring target health values in your step 5 table. Explain it in terms of clip damage.

## Deliverable

The spreadsheet file (or a share link), the cumulative damage chart, and a design note of about 350 words. The note must say, for each weapon, the band of fight lengths it wins, what regeneration did to that band, and why your carbine change worked.

## Rubric

| Criterion | Points | Full marks | Partial | Minimal |
|---|---|---|---|---|
| Summary table | 10 | All four numbers correct for all weapons | One weapon wrong | Missing |
| Hit schedule and D(t) | 25 | Correct schedule for clip and no-reload weapons; chart readable | Clip timing off by one interval | Continuous DPS used instead of hits |
| Crossovers | 15 | All lead changes found, final crossover stated | Only first crossover | None |
| TTK tables | 20 | Correct with and without regeneration; "never" handled | One table wrong | Only smooth estimates |
| Tuning | 15 | One parameter changed, goal met, evidence shown | Goal partly met | No tuning |
| Design note | 15 | Bands and regeneration effect explained with numbers | Explanation thin | Restates the lab |

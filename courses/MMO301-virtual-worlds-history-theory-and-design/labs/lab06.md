# MMO301 · Lab 06: Pricing aggression

**Week:** 6 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the world design bible (40%)

## Objective

Build a gank calculator from week 6's model, reproduce EVE's high security table, and use the calculator to design and stress-test a three-zone risk gradient for your own world.

This lab uses [week 6](../lectures/w06-eve-online-the-single-shard-sandbox.md): `n = ceil(H / (a × T))`, `C = n × c`, `V* = C / p`, expected profit `p × V − C`.

## Starter materials

- A blank spreadsheet.
- CONCORD response times from week 6's Sources (EVE University Wiki, "CONCORD", current): 1.0: 6 s, 0.9: 6 s, 0.8: 7 s, 0.7: 10 s, 0.6: 14 s, 0.5: 19 s. Add 6 s for the "CONCORD pulled" case.
- The assumed ship values from the lecture: `a = 500` damage per second, `c = 12M`, `p = 0.5`.
- A hauler table, the same for everyone:

| Hauler | EHP `H` | Typical cargo `V` |
|---|---|---|
| Starter hauler | 15,000 | 20M |
| Mid hauler | 60,000 | 150M |
| Tanked hauler | 120,000 | 400M |
| Freighter | 400,000 | 2,000M |

## Steps

1. **Calculator.** One row per security level (1.0 to 0.5), one column block per hauler. Compute `n`, `C`, `V*`, `V* / H` and expected profit at the typical cargo. Mark every cell where the gank pays.
2. **Check against the lecture.** For the mid hauler, confirm the lecture's table (20, 20, 18, 12, 9, 7 ships).
3. **Pulled CONCORD.** Repeat step 1 with 6 s added. Report, for each hauler, the security levels where pulling CONCORD turns a losing gank into a paying one.
4. **Sensitivity.** Halve `c`. Then double `a`. For each change, report how `V* / H` at 0.5 moves and compare with the 3,000 ISK per EHP rule of thumb.
5. **Your gradient.** Take the three-region world from the week 6 in-class activity (capital, frontier, wilderness). For each region, define the price rule (an NPC response time, a reputation cost, a fee, or none) and translate it into the calculator's terms. A reputation or fee cost can be added to `C` as a flat amount per attacker.
6. **New-player test.** Using your own starter hauler equivalent (the most valuable thing a new player carries), show that attacking it does not pay in your capital with your assumed attacker. Then find the cheapest attacker (lowest `c`) that would make it pay.

## Deliverable

The calculator and a one-page zone table for your world design bible: region, price rule, the number that sets it, the best resource there, and `V*` for a new player and for a veteran hauler. Add 250 words on the one exploit you expect players to use to lower your capital's price, and whether you will allow it.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Calculator | All haulers and levels correct, gank-pays cells marked, lecture table reproduced | One block wrong or unmarked | Two or more wrong | 25% |
| Pulled CONCORD and sensitivity | Both analyses complete with the direction and size of each change | One analysis missing or vague | Missing | 20% |
| Zone design | Three regions with numeric price rules, risk and reward rising together | Rules given but not numeric, or reward not considered | Missing | 20% |
| New-player test | Shown with arithmetic, the breaking attacker found | Shown without the breaking case | Missing | 15% |
| Exploit note | A concrete exploit, its effect on `V*` computed, a decision argued | Exploit named, effect not computed | Missing | 20% |

<details>
<summary>Instructor check values</summary>

- Starter hauler (`H = 15,000`, `V = 20M`): at 1.0, `n = 5`, `V* = 120M`; at 0.5, `n = 2`, `V* = 48M`. The gank never pays at 20M.
- Mid hauler (`H = 60,000`, `V = 150M`): pays at no level with fresh CONCORD (lowest `V*` is 168M at 0.5). Pulled at 0.5: `n = 5`, `V* = 120M`, so it pays (expected profit `75M − 60M = 15M`).
- Tanked hauler (`H = 120,000`, `V = 400M`): at 0.5, `n = 13`, `V* = 312M`, pays (profit `200M − 156M = 44M`); at 0.6, `n = 18`, `V* = 432M`, does not pay.
- Freighter (`H = 400,000`, `V = 2,000M`): at 0.5, `n = 43`, `V* = 1,032M`, pays; at 1.0, `n = 134`, `V* = 3,216M`, does not pay.
- Halving `c` halves `V* / H`; doubling `a` roughly halves it (exactly, before rounding in `n`).

</details>

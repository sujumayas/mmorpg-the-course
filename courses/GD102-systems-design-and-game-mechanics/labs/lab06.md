# GD102 · Lab 06: Pricing a converter

**Assigned:** week 6. **Due:** start of week 7. **Weight:** part of the Machinations models component (30% of the course).
**Lecture:** [Week 6, converters, traders, gates](../lectures/w06-machinations-diagrams-ii-converters-traders-gates.md). **Interactive:** [w06-catan-converter.html](../examples/w06-catan-converter.html), for checking your numbers.

## Objective

Rebuild the worked example's diagram, reproduce two rows of its table, then set a converter ratio and a hand-limit rule for a new game so that trading for a resource is slower than producing it by an amount you choose on purpose. By the end you should be able to state a converter ratio as a price and show, with numbers, what else in the system changes that price.

## Starter materials

**Part A, the diagram.** Build the diagram from lecture section 5 in machinations.io: an interactive roll node, a random gate with the 2d6 weights, four resource pools, a converter, an all-or-nothing city drain, and a discard drain with a trigger from the 7 output and an activator `hand > 7`. A screenshot is part of the deliverable.

**Part B, simulation script.** Machinations' batch runner is slow for thousands of games, so the measurements use this script. Save it as `converter_sim.py`. It uses only the Python standard library and matches the interactive spec. Both players use the bank: the ore player's spare grain, lumber and brick also convert 4:1 (that is why `ORE_PLAYER` is measured with `"4:1"`).

```python
import random, statistics

def ratio_for(res, harbor):
    if harbor == "3:1":
        return 3
    if harbor == "2:1 wool" and res == "wool":
        return 2
    return 4

def game(hexes, harbor, discard, rng, limit=7, cap=500):
    need = {"grain": 2, "ore": 3}
    hand = {"grain": 0, "wool": 0, "lumber": 0, "brick": 0, "ore": 0}
    for roll_no in range(1, cap + 1):
        roll = rng.randint(1, 6) + rng.randint(1, 6)
        if roll == 7:
            if discard and sum(hand.values()) > limit:
                for _ in range(sum(hand.values()) // 2):
                    surplus = {r: hand[r] - need.get(r, 0) for r in hand}
                    worst = max(hand, key=lambda r: (surplus[r], hand[r]))
                    hand[worst] -= 1
        else:
            for res, token in hexes.items():
                if token == roll:
                    hand[res] += 1
        changed = True
        while hand["ore"] < 3 and changed:
            changed = False
            for res in ("wool", "lumber", "brick", "grain"):
                q = ratio_for(res, harbor)
                if hand[res] - need.get(res, 0) >= q and hand["ore"] < 3:
                    hand[res] -= q
                    hand["ore"] += 1
                    changed = True
        if hand["grain"] >= 2 and hand["ore"] >= 3:
            return roll_no
    return cap

def measure(hexes, harbor, discard, games=20000, seed=7, limit=7):
    rng = random.Random(seed)
    xs = sorted(game(hexes, harbor, discard, rng, limit) for _ in range(games))
    return statistics.mean(xs), xs[len(xs) // 2], xs[int(0.9 * len(xs))]

ORE_PLAYER = {"grain": 6, "ore": 8, "lumber": 9, "brick": 10}
NO_ORE = {"grain": 6, "wool": 8, "lumber": 9, "brick": 10}

if __name__ == "__main__":
    print("ore player, discard:", measure(ORE_PLAYER, "4:1", True))
    print("no ore, bank, discard:", measure(NO_ORE, "4:1", True))
```

**Design brief for Part C.** A fictional island game, *Saltmarsh*, uses the same dice and the same hex layout as the no-ore player above. A new building, the Lighthouse, costs 3 ore and 2 grain, exactly like a city. The lead designer wants:

- A player without ore should reach a Lighthouse in between 1.3 and 1.6 times the mean rolls of the ore player.
- No more than 10% of no-ore games should take longer than 80 rolls.
- There must still be a rule that punishes large hands.

You may change the bank ratio (any whole number from 2 to 6), the hand limit that activates the discard (any whole number from 5 to 12), and the share discarded (a half or a third, rounded down).

## Steps

1. **Diagram.** Build Part A in Machinations and run it by hand for 5 games for the no-ore player with the bank. Record rolls to city for each.
2. **Reproduce.** Run the script. Your two printed rows must match the lecture table within 1 roll on the mean. If they do not, find the difference before going on.
3. **Flow estimates.** In a spreadsheet, compute the flow estimate for the no-ore player at bank ratios 2 to 6. Plot flow estimate against ratio next to the simulated means (discard off) and label the batching gap.
4. **Exposure.** Add the `limit` parameter to your runs and plot mean rolls for the no-ore bank path against the hand limit from 5 to 12 with the discard on. Mark the ore player's mean on the same chart.
5. **Share discarded.** Change the script so the discard can take a third of the hand instead of half. Report the effect on both players at the default limit.
6. **Design.** Search the three knobs in the brief for every combination that meets all three conditions. Present the qualifying combinations in a table. If none qualify, report the closest and the condition it fails.
7. **Pick one.** Choose one combination and argue for it on grounds other than the brief, for example which is easiest to explain on a rules card, or which keeps harbors valuable.

## Deliverable

The Machinations screenshot, the modified script, the spreadsheet with the two charts, and a memo of about 400 words. The memo states your chosen ratio, hand limit and discard share, gives the resulting mean, 90th percentile and ratio to the ore player's mean, explains the batching gap and the exposure gap in your own words using your own numbers, and says how your choice changes the value of a harbor.

## Rubric

| Criterion | Points | Full marks | Partial | Minimal |
|---|---|---|---|---|
| Machinations diagram | 15 | All nodes present with correct modes, all-or-nothing pulls, trigger and activator | One element wrong or missing | Diagram does not run |
| Reproduction | 10 | Both rows within tolerance | One row within tolerance | Not run |
| Flow estimates and batching chart | 15 | Estimates correct for all five ratios; gap labelled | Minor errors | Missing |
| Exposure analysis | 20 | Limit sweep and discard-share change both measured for both players | One of the two measured | Missing |
| Design search | 20 | Every qualifying combination found and tabled, or closest with failing condition | Partial search | Guess without data |
| Memo | 20 | Choice justified with numbers; both gaps explained; harbor value discussed | Some numbers, weak explanation | Restates the lab |

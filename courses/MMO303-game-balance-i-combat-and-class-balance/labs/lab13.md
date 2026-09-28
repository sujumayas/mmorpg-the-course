# MMO303 · Lab 13: Build a combat simulator

**Assigned:** week 13 ([lecture](../lectures/w13-combat-simulators.md)). **Due:** start of week 14 class. **Feeds:** the simulator assessment (30%) and [Lab 14](lab14.md).

## Objective

Write a small event-driven Monte Carlo combat simulator, prove it is correct on cases you can compute by hand, then use it to measure the balance of four DPS classes with error bars. By the end you should be able to defend every number in your balance table with its standard error, its policy and its fight style.

## Starter materials

Your instructor provides a folder `lab13-starter/` with:

- `sim.py`, a skeleton with an event queue (Python's `heapq`), an `Actor` class, and empty functions `choose_action`, `apply_action` and `run_fight`. It runs, but every class deals zero damage.
- `classes.yaml`, the four class definitions you will simulate (below).
- `test_sim.py`, two example tests using `pytest`, one of which fails until you implement hits.
- `report_template.md`, the headings for your write-up.

If you prefer another language, you may port the skeleton, but your simulator must accept a seed and a number of iterations from the command line.

The core loop you are completing looks like this:

```python
def run_fight(actors, fight_length, rng):
    queue = [(0.0, i, "ready") for i in range(len(actors))]
    heapq.heapify(queue)
    while queue:
        t, i, kind = heapq.heappop(queue)
        if t >= fight_length:
            break
        actor = actors[i]
        if kind == "ready":
            action = choose_action(actor, t)
            apply_action(actor, action, t, rng)
            heapq.heappush(queue, (t + action.cast_time, i, "ready"))
        # TODO: handle buff expiry, proc cooldowns
    return {a.name: a.damage / fight_length for a in actors}
```

### The four classes (from `classes.yaml`)

All classes act every 1.5 seconds and crit for 2× damage unless stated.

| Class | Base hit | Crit chance | Special rule |
|---|---|---|---|
| Duelist | 100 | 25% | none |
| Marksman | 110 | 10% | none |
| Berserker | 95 | 15% | **Frenzy proc:** each hit has a 20% chance to grant Frenzy for 6 s (+30% damage). Frenzy cannot trigger again for 10 s after it triggers (internal cooldown). |
| Ritualist | 80 | 20% | **Builder/spender:** each hit grants 1 charge. At 4 charges, the next action is Rite instead: 400 damage, crits as normal, consumes all charges, 1.5 s like any action. |

## Steps

1. **Implement plain hits (30 min).** Complete `apply_action` for base damage and crits. Use one `random.Random(seed)` instance per actor so that actors do not share a random stream.
2. **Validate against the closed form (45 min).** For the Duelist and the Marksman, run 10,000 fights of 60 seconds. Report `μ̂`, sample SD and SE. Compare with the lecture values (Duelist `μ = 83.33`, `σ = 4.56`; Marksman `μ = 80.67`, `σ = 3.48`). Add a test to `test_sim.py` that fails if `μ̂` is outside `μ ± 4 SE`. Also add deterministic tests: crit chance 0% gives exactly `40 × D / 60`; crit chance 100% gives exactly twice that.
3. **Implement the Berserker (45 min).** Add buff state and the internal cooldown to the event queue. Before running it, estimate its mean by hand with a rough argument (what fraction of time is Frenzy up?) and write your estimate down. Then run 10,000 fights and compare. Explain any difference in two or three sentences.
4. **Implement the Ritualist (30 min).** Add the charge counter and the priority list: "if charges = 4, use Rite; else use Hit." Compute its exact mean for a 60-second fight by hand (how many Rites fit in 40 actions?) and check the simulator against it.
5. **Build the balance matrix (45 min).** Run all four classes on three fight lengths: 30 s, 60 s and 300 s. Fill a 4 × 3 table where every cell is `μ̂ ± 1.96 SE`. Choose N per cell so that every half-width is under 0.5% of the cell's mean, and state the N you used.
6. **Common random numbers (30 min).** Compare the Duelist with a Duelist buffed to 102 base damage. Do it twice, with independent streams and with the same seed for both versions. Report the SE of the difference both ways and the ratio.
7. **Write it up.** Fill in `report_template.md`.

## Deliverable

A zip or repository link containing:

- Your completed `sim.py` and `test_sim.py`, with all tests passing (`pytest` output pasted in the report).
- `report.md` (800 to 1,200 words) with: the validation table from step 2; your Berserker estimate versus the simulated value and the explanation; the Ritualist hand calculation; the balance matrix with error bars; the common-random-numbers result; and a closing paragraph naming the one class you would change first and why, citing a specific cell of the matrix.
- The seed and command line for every table, so a reviewer can reproduce it.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Weight |
|---|---|---|---|---|
| Correctness of the simulator | All validation checks pass; means within 4 SE of hand values; deterministic tests exact | Plain hits correct, one special class has an unexplained discrepancy | Plain hits fail validation | 25% |
| Stateful mechanics | Frenzy internal cooldown and Ritualist charges both correct, matched to hand estimates with reasoning | One mechanic correct, or both correct without hand checks | Neither implemented correctly | 20% |
| Statistical reporting | Every number has SE or a 95% interval; N chosen from the 0.5% target and justified | Error bars present on most numbers; N chosen by guess | Point estimates only | 20% |
| Common random numbers | Both SEs reported, ratio computed and explained | Run done, no explanation | Not attempted | 10% |
| Reproducibility | Seeds and commands given; reviewer can rerun and match | Seeds given, commands incomplete | Cannot be rerun | 10% |
| Balance judgment | Recommendation cites a specific cell and its error bar, considers fight length | Recommendation given, loosely tied to data | No recommendation | 15% |

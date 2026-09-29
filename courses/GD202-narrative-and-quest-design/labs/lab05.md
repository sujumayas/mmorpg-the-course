# GD202 · Lab 05: Approval tuning

**Week:** 5, characters and companions ([lecture](../lectures/w05-characters-and-companions.md)).
**Time:** 2 hours in lab, plus about 3 hours at home.
**Weight:** part of the dialogue exercises (40%).

## Objective

Compute exact approval distributions for a companion whose events have different step sizes, with and without a clamped meter. Then design a companion of your own and tune the steps and thresholds so that three player personas get the outcomes you intend.

## Starter materials

All in [`lab05-starter/`](lab05-starter/). Standard-library Python, run with `.venv/bin/python`.

- [`approval.py`](lab05-starter/approval.py) has an `Event` dataclass (name, `agree_step`, `disagree_step`), the lecture's `closed_form` function, Oda's ten events from lecture section 1, and three empty functions: `walk_distribution`, `prob_at_least` and `mean`.
- [`test_approval.py`](lab05-starter/test_approval.py) holds the test values. Twenty ±5 events at `p = 1/2` give exactly `21,700 / 1,048,576` for approval of 50 or more. The walk must match the closed form for `p` from 0.6 to 0.9. Three ±50 steps clamped to ±100 give `{100: 1/8, 50: 3/8, −50: 3/8, −100: 1/8}`. With a cap of 100, the order `+60, +60, −20` ends at 80 and `−20, +60, +60` ends at 100. A persona with per-event probabilities works. Oda's mean at `p = 1/2` is −5.
- The [interactive](../examples/w05-approval-walk.html), whose clamp toggle uses the same step-by-step method.

Run the tests from the repository root:

```
.venv/bin/python courses/GD202-narrative-and-quest-design/labs/lab05-starter/test_approval.py
```

On the starter all eight tests report `TODO` and the script exits with status 1.

## Steps

1. **Walk.** Implement `walk_distribution(events, p, start, lo, hi)` as a step-by-step dynamic program: a dict from approval value to probability, updated once per event, clamped after each step when `lo` or `hi` is set. Test it with `fractions.Fraction` so results are exact.
2. **Read it.** Implement `prob_at_least` and `mean`. Run `approval.py` and confirm Oda at `p = 0.5` has mean −5.0 and a 4.6% chance of reaching 30.
3. **Why is Oda negative?** Explain in two sentences why an indifferent player loses approval with Oda even though half the choices please her. Use the asymmetric steps in her event list.
4. **Your companion.** Write a values sheet (three approvals, three disapprovals, one-line reasons in voice) and 12 to 16 events with steps. Use at least two step sizes. At least three events must have a disagree step of a different size from the agree step.
5. **Three personas.** Define three players as per-event probability lists: a *devotee* who shares the companion's values, a *wanderer* who chooses on a whim (0.5 everywhere unless your events make that silly), and a *rival* whose values oppose the companion's. Write one sentence per persona saying what you want to happen to them.
6. **Tune.** Pick a friendship threshold and a walk-out wall. Adjust steps (not personas) until the devotee reaches the threshold at least 80% of the time, the wanderer reaches it between 10% and 30% of the time, and the rival hits the wall at least 50% of the time. Report the final numbers with and without a ±100 clamp.
7. **Order test.** Reverse your event list and rerun with the clamp on. Report any persona whose chance changes by more than one percentage point and explain which events cause it.

## Deliverable

`approval.py` with all tests passing, a `my_companion.py` with your events and personas, and a report of at most 600 words: the values sheet, the event table, the three persona results before and after tuning, the step 7 result, and a paragraph on what kind of player your tuning rewards.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Walk correctness | All eight tests pass with exact fractions | Six or seven pass | Fewer than six | 30% |
| Values sheet and voice | Values pull against each other; reasons read as one character | Values listed, voice generic | Missing or copied | 20% |
| Tuning targets | All three persona targets met, numbers shown with and without clamp | Two targets met | One or none | 25% |
| Order and asymmetry analysis | Step 3 and step 7 explained with the specific events responsible | Explained vaguely | Missing | 15% |
| Design reflection | Clear statement of which player the system rewards and why that fits the game | Statement without reasoning | Missing | 10% |

<details>
<summary>Instructor check values</summary>

- Oda, uniform `p`, no clamp, `P(A ≥ 30)`: 4.6% at 0.5, 13.2% at 0.6, 29.8% at 0.7, 55.2% at 0.8, 84.1% at 0.9. Means: −5.0, +6.4, +17.8, +29.2, +40.6.
- Oda's maximum possible approval is +52 (all agreements), so a threshold above 52 is unreachable; students who set one should notice.
- Step 3 answer: three events cost more on disagreement than they pay on agreement (informant and magistrate, +5 or −10; toll bridge, +1 or −5), and one pays more than it costs (side door, +5 or −1). At `p = 0.5` each event contributes the average of its two steps, and these sum to −5.
- Thirty ±10 events clamped at ±100, `p = 0.7`: `P(A ≥ 50)` is 91.45% against 91.55% unclamped.

</details>

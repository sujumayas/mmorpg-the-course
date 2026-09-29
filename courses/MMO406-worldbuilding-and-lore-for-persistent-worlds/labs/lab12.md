# MMO406 · Lab 12: The transmedia plan

**Week:** 12, transmedia ([lecture](../lectures/w12-transmedia.md), [interactive](../examples/w12-required-vs-optional.html)).
**Time:** 2 hours in lab, plus about 3 hours at home.
**Weight:** part of the exercises (40%). The plan and brief you write here become the "beyond the game" chapter of your world bible.

## Objective

This is a design and writing lab. There is no code to write. You audit a *Thornmere* transmedia plan with a provided calculator, fix it with retell lines until the game's story stands on its own, then write a transmedia plan for your own world and a licensee brief for one tie-in. The calculator makes the result checkable. Your plan passes when every beat the game needs is carried in the game, so the share of players who can follow the story is 100%.

## Starter materials

All in [`lab12-starter/`](lab12-starter/). Standard-library Python, run with `.venv/bin/python`.

- [`transmedia.py`](lab12-starter/transmedia.py) is a complete calculator. It reads a plan, decides which media are required (a medium is required when a beat comes from it and the game has no retell line for that beat), and prints `n`, `C` and `X` with their bounds for any overlap. `--selftest` reproduces the lecture's numbers.
- [`thornmere_transmedia.json`](lab12-starter/thornmere_transmedia.json) is the in-class plan for "The Heir's Road": four outside pieces with reach estimates, and four story beats. Only one beat has a retell line.

### The plan file format

```json
{
  "media": [
    {"id": "novel", "name": "Prequel novel: Adelmar's Last Year", "reach": 0.12,
     "tier": "tie-in", "frozen": true, "timing": "before"}
  ],
  "beats": [
    {"beat": "How Queen Adelmar died", "source": "novel", "retell": null}
  ]
}
```

`reach` is the share of active players who consume the medium. `retell` is the in-game line, scene or item that carries the beat to players who never saw the medium, or `null` if there is none yet.

Run it from the repository root:

```
.venv/bin/python courses/MMO406-worldbuilding-and-lore-for-persistent-worlds/labs/lab12-starter/transmedia.py --selftest
.venv/bin/python courses/MMO406-worldbuilding-and-lore-for-persistent-worlds/labs/lab12-starter/transmedia.py courses/MMO406-worldbuilding-and-lore-for-persistent-worlds/labs/lab12-starter/thornmere_transmedia.json
```

On the shipped plan it reports three required media, `C = 2.1%` (0% to 12% for any overlap) and `X = 55.0%`.

## Steps

1. **Audit Thornmere (15 min).** Run the calculator on the shipped plan. Check `C` and `X` by hand and show the arithmetic.
2. **Write the retell lines (35 min).** For each of the three beats with no retell line, write one in-game line, scene or item that carries the essential fact. For each, state where it lives (main story, side quest, item, zone text) and why a player cannot miss it. Keep each to at most two sentences of player-facing text, following GD202 week 10. Save the result as `thornmere_transmedia_v2.json` and rerun. The target is `C = 100%`. Record the new `X` and explain why it rose.
3. **Check the lines against the lecture's three properties (10 min).** For each retell line, say in one sentence how it rewards a reader of the outside piece without punishing a non-reader.
4. **Your transmedia plan (60 min, at home).** For your own world, plan the outside media for one expansion: at least four pieces in at least three different media, with reach estimates and a sentence justifying each estimate (where the piece is published, whether it is free, whether it is in the client). Mix timing: at least one lead-in and one follow-up. List at least five story beats the expansion relies on, each with its source. Write a retell line for every beat that comes from outside the game. Run the calculator until `C = 100%`.
5. **Stress the plan (15 min, at home).** Set your least-reached medium's reach to half your estimate and rerun. Then delete one retell line and rerun. Report both results in one table and one paragraph: which change hurts more, and why?
6. **Licensee brief (45 min, at home).** Write a one-page brief for one of your tie-ins, using every row of the table in lecture section 4. The "allowed facts" and "forbidden facts" rows must use fact ids from your lab 11 canon graph, and the forbidden list must include at least one open hook from your lab 10 plan.

## Deliverable

A zip or repository link containing:

- `thornmere_transmedia_v2.json` and your own plan file.
- `lab12.md`, 900 to 1,300 words, with: the Thornmere audit before and after, with hand checks; the retell lines with their locations and the step 3 sentences; your plan's calculator output; the stress table and paragraph; and the licensee brief.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Thornmere audit | Hand checks correct; v2 reaches `C = 100%`; new `X` computed and explained | Checks correct, explanation thin | Numbers not checked or wrong | 15% |
| Retell lines | Each carries exactly the needed fact, lives on the main path, and meets all three properties | Lines work but some sit in optional content or say too much | Lines missing or restate the whole story | 25% |
| Own plan | Four or more pieces across three media, reasoned reach estimates, mixed timing, `C = 100%` | Meets counts, estimates unjustified | Under counts or `C < 100%` | 25% |
| Stress test | Both changes run and compared, conclusion ties to the AND/OR rule | Run but not interpreted | Missing | 10% |
| Licensee brief | Every row filled; allowed and forbidden facts use real ids; an open hook protected; timing and after-release duties clear | Brief complete but generic | Missing rows or no ids | 25% |

<details>
<summary>Instructor check values</summary>

- Shipped plan: required media novel, comic, story; `C = 0.12 × 0.25 × 0.70 = 0.021`; bounds 0% to 12%; optional media short only, `X = 55.0%`; `n = 1.62`.
- After all three retell lines are added: no required media, `C = 100%`; `X = 1 − 0.88 × 0.45 × 0.75 × 0.30 = 1 − 0.0891 = 91.1%`, bounds 70% to 100%.
- Stress test pattern to expect: halving an optional medium's reach lowers `X` a little. Deleting one retell line makes that medium required and caps `C` at its reach, which is much larger damage. Students who halve a medium that is already required (in a plan that still has one) see `C` halve.
- Weak retell lines to flag: lines placed in optional side content (catch-up reach far below 1, week 7), lines that summarize the whole novel, and lines that tell non-readers they "should have read" something.

</details>

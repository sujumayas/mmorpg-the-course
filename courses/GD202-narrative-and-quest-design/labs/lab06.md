# GD202 · Lab 06: Quest spec and board audit

**Week:** 6, quest anatomy ([lecture](../lectures/w06-quest-anatomy-hook-objective-complication-reward.md)).
**Time:** 2 hours in lab, plus about 3 hours at home.
**Weight:** first draft toward the quest chain (60%). The three quests you write here are the seed of the final quest chain.

## Objective

Implement the detour test from the week 6 lecture for a whole quest board, including reward decay, travel speed and complications. Then write three quests for one zone in four-line form, give each a promise ledger, and tune them so each passes the test for the player it is meant for.

## Starter materials

All in [`lab06-starter/`](lab06-starter/). Standard-library Python, run with `.venv/bin/python`.

- [`quest_board.py`](lab06-starter/quest_board.py) has a `Quest` dataclass (name, level, listed XP, travel, task and complication minutes), a CSV loader, a given `audit` printer and five empty functions: `decay_percent`, `paid_xp`, `minutes`, `rate` and `required_listed_xp`.
- [`board.csv`](lab06-starter/board.csv) is the lecture's five-quest board.
- [`test_quest_board.py`](lab06-starter/test_quest_board.py) holds the lecture values. At level 20 the board pays 1,800, 4,200, 900, 800 and 3,000 XP. The ogre's tithe runs at 182.6 XP per minute, 227.0 with a mount. The collapsed Smuggler's cave runs at 166.7 and needs 3,600 listed XP to reach 200. Rounding goes to the nearest 5 with halves up, so 1,225 XP at 10% pays 125.
- The [interactive](../examples/w06-quest-detour.html) for spot checks.

Run the tests from the repository root:

```
.venv/bin/python courses/GD202-narrative-and-quest-design/labs/lab06-starter/test_quest_board.py
```

On the starter all eight tests report `TODO` and the script exits with status 1.

## Steps

1. **Implement the model.** Fill in the five functions. Use integer percent for decay so that rounding matches the tests. Run `quest_board.py` and check that it prints the lecture's table.
2. **Stress the board.** Using `audit`, find the lowest player level at which no quest on the lecture board passes at `r₀ = 200`. Then find the smallest `r₀` at which every quest passes at level 20. Report both.
3. **Choose a zone.** Pick a zone for a level range (for example, levels 14 to 18) and a fantasy for it in two sentences. Set a baseline `r₀` for that level range and justify it in one sentence.
4. **Write three quests in four lines each.** Hook, objective (verb, target, count, place), complication, reward. Use three different complication types from lecture section 1. At least one quest must pay part of its reward in a non-XP currency (access, story, relationship).
5. **Promise ledgers.** Write a ledger of at least three rows for each quest. Fix any broken promise before going on.
6. **Price and tune.** Add the three quests to `board.csv` with playtest-style time estimates (time yourself describing a walkthrough aloud if you have nothing better). Tune listed XP, travel and task so that each quest passes at the level you expect players to arrive. For each complication, report its minutes and its tax in XP (`r₀ × minutes`), and say what pays that tax back.
7. **Decay check.** Report each quest's rate at arrival level + 3 and + 7. Decide whether you want players to still take it then, and if not, say what tells them to move on.

## Deliverable

`quest_board.py` with all tests passing, your extended `board.csv`, and a quest spec of at most 900 words: the zone description, the three quests in four-line form, their promise ledgers, the audit table at the arrival level, the complication tax table, and the step 2 and step 7 results.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Model correctness | All eight tests pass; step 2 answers correct | Six or seven pass | Fewer than six | 25% |
| Four-line quests | Every part answers its player question; objectives have all four slots; three different complication types | One part weak or one slot missing | Parts missing or indistinct | 25% |
| Promise ledgers | Three rows each, broken promises found and fixed with a fiction-appropriate currency | Ledgers present but shallow | Missing | 15% |
| Tuning and tax | Every quest passes for its intended player; each complication priced and paid back | One quest fails or one tax unexplained | No numbers | 25% |
| Decay reasoning | Clear intent at +3 and +7 with a signal to move on | Numbers without intent | Missing | 10% |

<details>
<summary>Instructor check values</summary>

- Step 2, lowest level where nothing passes at `r₀ = 200`: at level 25 the only pass is the Smuggler's cave (214.3, still 5 levels over and paying in full). At level 26 it is 6 levels over and pays 2,400 (171.4), and the best remaining quest is the ogre's tithe at 182.6. The answer is level 26.
- Step 2, smallest `r₀` where every quest passes at level 20: the slowest is Old bones at 100.0, so `r₀ = 100`.
- Required listed XP at level 20, `r₀ = 200`: ogre's tithe 4,600; collapsed Smuggler's cave 3,600.
- Smuggler's cave at level 27, `r₀ = 200`: 4,665 listed XP (4,665 × 0.6 = 2,799, which rounds to 2,800).

</details>

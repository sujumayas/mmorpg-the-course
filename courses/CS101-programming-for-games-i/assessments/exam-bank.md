# CS101 · Exam bank

CS101 has no written exam. The grade comes from the weekly exercises (40%), two mini-games (30%) and the final arcade game (30%). This bank has three other jobs.

- **Weekly quizzes.** At the start of each lab, your tutor sets two or three questions from the week just taught as a 10-minute check. The score is feedback for you and for the tutor. It does not count toward the grade. See [weekly-exercises-brief.md](weekly-exercises-brief.md).
- **Practice.** Work through a week's questions before you start its lab. Every answer has a full working, so when you get a different number you can find the step where your method went wrong.
- **Code viva.** Both mini-games and the final arcade game end with a short viva. The assessor picks questions tagged **apply**, swaps the question's values for your game's own values (your jump window, your bullet speed, your spawn radius) and asks you to answer about your code. The viva pattern at the end of this file shows how. See [mini-games-brief.md](mini-games-brief.md) and [final-arcade-game-brief.md](final-arcade-game-brief.md).

**How to read the tags.** Each question starts with `[Weeks · type · mode]`.

- Type is **code** (trace a snippet or write one), **compute** (produce a number with a lecture model), **explain** (state a concept and use it on a case), **design** (propose code or data that meets a stated goal) or **critique** (judge someone else's code, claim or design).
- Mode is **apply** when the question gives values or code the lecture did not work through, so you must carry a model or a habit to a new case. Mode is **recall** when it checks a definition or a result from the lecture itself. 67 of the 68 questions are apply. The 20 code questions and 31 compute questions, 51 in all, ask you to trace or write code or to put new values through a lecture model.

Games in the questions are either invented for this bank or are games the lectures already discuss, used only with the facts the lectures cite. Every Python snippet was run with Python 3.13 and every number was recomputed for this bank. GDScript lines are short and mirror Python the lectures already run.

**Coverage.**

| Week | Topic | Questions |
|---|---|---|
| 1 | Programs, variables, types | 1 to 4 |
| 2 | Conditionals | 5 to 8 |
| 3 | Loops and the game loop | 9 to 12 |
| 4 | Functions and decomposition | 13 to 17 |
| 5 | Lists and inventories | 18 to 22 |
| 6 | Dictionaries and item databases | 23 to 27 |
| 7 | Godot scenes, nodes, scripts | 28 to 31 |
| 8 | Input handling and movement | 32 to 36 |
| 9 | Delta time and fixed timestep | 37 to 42 |
| 10 | Collision: AABB and circles | 43 to 47 |
| 11 | Game state machines | 48 to 52 |
| 12 | Debugging | 53 to 56 |
| 13 | Randomness and spawning | 57 to 62 |
| 14 | Polish: shake, particles, sound | 63 to 66 |
| Several | Integrated cases | 67 to 68 |

---

## Week 1 · Programs, variables and types

Lecture: [w01-programs-variables-and-types.md](../lectures/w01-programs-variables-and-types.md)

1. **[1 · code · apply]** Predict every value this line prints, then say which of the five values is a `float`.

   ```python
   gold = "25"
   found = 7
   lamp = 100.0
   print(gold * 2, int(gold) + found, lamp - 2.5 * 4, 9 // 4, 9 / 4)
   ```

   <details>
   <summary>Answer</summary>

   It prints `2525 32 90.0 2 2.25`.

   - `gold * 2` repeats the string `"25"`, giving `2525`.
   - `int(gold) + found` is `25 + 7 = 32`, an `int`.
   - `2.5 * 4 = 10.0` is worked out first (multiplication before subtraction), then `100.0 − 10.0 = 90.0`, a `float`.
   - `9 // 4` rounds down to the `int` 2.
   - `9 / 4` always gives a `float`, 2.25.

   The floats are the third and fifth values. `/` gives a float even when the division is exact, so `9 / 3` is `3.0`.

   </details>

2. **[1 · compute · apply]** Use `stored = true_value mod 2^n` for unsigned values and the signed range `−2^(n−1)` to `2^(n−1) − 1`. (a) A 16-bit unsigned turn counter reads 65,530 and 10 turns pass. What does it hold? (b) A signed 8-bit armor value is 100 and a buff adds 40. What does it hold? (c) An unsigned 8-bit ammo count is 3 and a bug subtracts 5. What does the player see?

   <details>
   <summary>Answer</summary>

   (a) `(65,530 + 10) mod 65,536 = 65,540 − 65,536 = 4`. The counter shows 4.

   (b) The true value 140 is above the signed maximum 127. The byte keeps `140 mod 256 = 140`, which as a signed byte is `140 − 256 = −116`. The character now has negative armor.

   (c) `(3 − 5) mod 256 = −2 mod 256 = 254`. The player suddenly has 254 bullets. That is underflow, the same wrap in the other direction.

   </details>

3. **[1 · compute · apply]** A character in a big open world stands at `x = 5,000,000` in a 32-bit float position and walks right by adding a constant step every frame. Use `gap(x) = 2^(floor(log2 x) − 23)`. (a) What is the gap between neighbouring floats here? (b) With a step of 0.3, where does the character land after one frame, and how far does it travel in 100 frames? (c) With a step of 0.2?

   <details>
   <summary>Answer</summary>

   (a) `2^22 = 4,194,304` and `2^23 = 8,388,608`, so `floor(log2 5,000,000) = 22`. The gap is `2^(22 − 23) = 2^−1 = 0.5`. Only multiples of 0.5 exist here.

   (b) `5,000,000.3` is not a float. The nearest floats are `5,000,000.0` (0.3 away) and `5,000,000.5` (0.2 away), so it rounds to `5,000,000.5`. Every step rounds up the same way, so the character moves 0.5 per frame instead of 0.3. After 100 frames it has gone 50 units instead of 30, 67% too fast.

   (c) `5,000,000.2` is 0.2 from `5,000,000.0` and 0.3 from `5,000,000.5`, so it rounds back to where it started. The character never moves. You can check both with the lecture's `as_float32` helper applied after every addition.

   Same code, two different bugs, depending only on the step size. The lecture's design judgment gives the fix. Keep positions near zero, or use 64-bit positions.

   </details>

4. **[1 · design · apply]** A game caps gold at 9,999 and stores the level in one unsigned byte. Write one line of Python for each rule, then give the results for (a) 9,990 gold plus 25, (b) level 250 plus 7 levels. Say which rule a player expects and why.

   <details>
   <summary>Answer</summary>

   ```python
   gold = min(gold + loot, 9_999)       # clamp
   level = (level + gained) % 256       # 8-bit wrap
   ```

   (a) `min(10,015, 9,999) = 9,999`. (b) `257 mod 256 = 1`. The player on level 250 is sent to level 1.

   Players expect the clamp. A clamp at a visible cap reads as a rule ("the purse is full"). A wrap reads as a bug, because the value jumps from the top of its range to the bottom. Use a wrap only when the design wants a cycle, such as a day counter or an angle.

   </details>

## Week 2 · Conditionals

Lecture: [w02-conditionals-room-transitions-and-win-lose.md](../lectures/w02-conditionals-room-transitions-and-win-lose.md)

5. **[2 · code · apply]** What does this function return for `(0, True)`, `(-3, False)`, `(5, True)` and `(5, False)`?

   ```python
   def outcome(hp, shield):
       if hp <= 0 and not shield:
           return "dead"
       elif hp <= 0:
           return "saved by shield"
       elif shield:
           return "shielded"
       else:
           return "fine"
   ```

   <details>
   <summary>Answer</summary>

   | Call | First true branch | Result |
   |---|---|---|
   | `(0, True)` | `hp <= 0` (the `and not shield` part is False) | `saved by shield` |
   | `(-3, False)` | `hp <= 0 and not shield` | `dead` |
   | `(5, True)` | `shield` | `shielded` |
   | `(5, False)` | none | `fine` |

   The chain is in the right order. The most specific case (out of health and no shield) is tested first, and `<=` catches the overkill value −3.

   </details>

6. **[2 · compute · apply]** Evaluate both expressions for `has_key = True`, `door_open = False`, `trapped = True`. Then find one set of values for the three variables where the two lines give the same answer.

   ```python
   has_key or door_open and not trapped
   (has_key or door_open) and not trapped
   ```

   <details>
   <summary>Answer</summary>

   Python evaluates `not`, then `and`, then `or`. The first line means `has_key or (door_open and not trapped)`, which is `True or (False and False) = True`. The second is `(True or False) and not True = True and False = False`.

   So the brackets change the answer. With `has_key = False`, `door_open = True`, `trapped = False`, both lines are `True`, which is why a test with only "normal" values would never notice the difference. When the intent is "any way in, and no trap", write the brackets.

   </details>

7. **[2 · critique · apply]** A health bar shows a status word. Test it with `hp` of 100, 60, 20 and −5 (maximum 100). What is wrong, and what is the fix?

   ```python
   if hp < max_hp:
       status = "hurt"
   elif hp <= max_hp * 0.2:
       status = "critical"
   else:
       status = "full"
   ```

   <details>
   <summary>Answer</summary>

   | `hp` | Result | Intended |
   |---|---|---|
   | 100 | full | full |
   | 60 | hurt | hurt |
   | 20 | hurt | critical |
   | −5 | hurt | critical |

   Every value at or below 20 is also below 100, so the `hurt` branch fires first and `critical` can never be reached. It is the locked-door bug from lecture section 2. Put the more specific test first:

   ```python
   if hp <= max_hp * 0.2:
       status = "critical"
   elif hp < max_hp:
       status = "hurt"
   else:
       status = "full"
   ```

   </details>

8. **[2 · design · apply]** A co-op game ends when the boss dies (win), the base is destroyed (lose) or the timer runs out (lose). The current chain checks `base_destroyed`, then `boss_dead`, then `time_up`. (a) How many cases exist? (b) List every case in which the boss dies but the team still loses. (c) The designer wants "killing the boss on the same frame the base falls" to be a win, while "boss dies as time runs out" stays a win. Rewrite the chain.

   <details>
   <summary>Answer</summary>

   (a) Three booleans give `2^3 = 8` cases.

   (b) With the current order, `base_destroyed` wins every tie. The boss dies and the team loses in two cases: boss dead and base destroyed, and boss dead, base destroyed and time up.

   (c) Put the win first, so it beats both lose conditions:

   ```python
   if boss_dead:
       result = "win"
   elif base_destroyed or time_up:
       result = "lose"
   else:
       result = "keep playing"
   ```

   Run the eight rows to check. The four rows with `boss_dead` give win, the three others with a lose condition give lose, and all False gives keep playing. Write the tie policy in the design notes, as the lecture advises, so the next programmer does not "fix" the order back.

   </details>

## Week 3 · Loops and the game loop

Lecture: [w03-loops-and-the-game-loop.md](../lectures/w03-loops-and-the-game-loop.md)

9. **[3 · code · apply]** Trace this loop in a table with columns for `turns`, the `continue` decision and `oil`. What does it print?

   ```python
   oil = 20
   turns = 0
   while oil > 0:
       turns += 1
       if turns % 3 == 0:
           continue
       oil -= 6
   print(turns, oil)
   ```

   <details>
   <summary>Answer</summary>

   | `oil` at check | `turns` after `+= 1` | `turns % 3 == 0`? | `oil` after |
   |---|---|---|---|
   | 20 | 1 | no | 14 |
   | 14 | 2 | no | 8 |
   | 8 | 3 | yes, `continue` | 8 |
   | 8 | 4 | no | 2 |
   | 2 | 5 | no | −4 |
   | −4 | loop ends | | |

   It prints `5 -4`. `continue` skips the rest of turn 3 but still goes back to the condition, so turn 3 costs no oil. A condition of `oil != 0` would never end, because oil jumps from 2 to −4.

   </details>

10. **[3 · compute · apply]** A tribute to Space Invaders uses the lecture's model. One alien moves per frame, and the formation moves `d = 2` px per step. It starts with 36 aliens. (a) At `F = 60`, give steps per second, speed and time per step for 36, 12 and 3 aliens. (b) How many aliens can remain before the formation first moves at 20 px/s or faster? (c) What happens to all three speeds if the game runs its loop at 30 per second?

    <details>
    <summary>Answer</summary>

    Speed is `d × F / N` and time per step is `N / F`.

    | `N` | Steps per second `60/N` | Speed (px/s) | Time per step |
    |---|---|---|---|
    | 36 | 1.67 | 3.33 | 0.600 s |
    | 12 | 5 | 10 | 0.200 s |
    | 3 | 20 | 40 | 0.050 s |

    (b) `120 / N ≥ 20` needs `N ≤ 6`. The formation reaches 20 px/s when 6 aliens are left.

    (c) Every speed halves (1.67, 5 and 20 px/s), because speed is proportional to `F`. The curve keeps its shape. The whole game is half as fast, which is the turbo-button problem with `F` falling instead of rising.

    </details>

11. **[3 · code · apply]** (a) What does `for i in range(10, 0, -3): total += i` add to `total`, and how many times does the body run? (b) A turret fires when `frame % 45 == 0`. How many shots per second is that at 60 fps and at 144 fps? Is this "every k-th" pattern safe on a PC?

    <details>
    <summary>Answer</summary>

    (a) The range gives 10, 7, 4, 1 and stops before 0, so the body runs 4 times and adds 22.

    (b) At 60 fps, `60 / 45 = 1.33` shots per second. At 144 fps, `144 / 45 = 3.2` shots per second, 2.4 times as many. The pattern counts frames, so its rate follows the frame rate. It is safe only where the frame rate is fixed and guaranteed, as on an arcade board. On a PC, time the turret in seconds (week 9).

    </details>

12. **[3 · code · apply]** A variant moves up to three aliens per frame. A formation step always ends the frame's work. The model says `N / 3` frames per step. What does this loop measure for 55, 20 and 2 aliens, and why does it differ from the model?

    ```python
    def frames_per_step(alive, k, steps=3):
        cursor, frame, done = 0, 0, 0
        while done < steps:
            for _ in range(k):          # move up to k aliens this frame
                cursor += 1
                if cursor == alive:     # formation step complete
                    cursor = 0
                    done += 1
                    break               # rest of this frame's moves skipped
            frame += 1
        return frame / steps
    ```

    <details>
    <summary>Answer</summary>

    | Aliens | Model `N / 3` | Measured |
    |---|---|---|
    | 55 | 18.33 | 19 |
    | 20 | 6.67 | 7 |
    | 2 | 0.67 | 1 |

    A frame cannot be split. The last frame of each step moves the one or two aliens that are left and then stops, so the measured value is `N / 3` rounded up. With 2 aliens the model predicts more than one step per frame, which this loop cannot do. It is the same effect as the lecture's two-per-frame activity (28, 6 and 1 frames for 55, 11 and 1 aliens).

    </details>

## Week 4 · Functions and decomposition

Lecture: [w04-functions-and-decomposition.md](../lectures/w04-functions-and-decomposition.md)

13. **[4 · code · apply]** What are the three printed values?

    ```python
    def heal(hp, amount, max_hp=30):
        hp = hp + amount
        if hp > max_hp:
            hp = max_hp
        return hp

    hp = 12
    heal(hp, 10)
    print(hp)
    hp = heal(hp, 25)
    print(hp)
    print(heal(5, 5, max_hp=8))
    ```

    <details>
    <summary>Answer</summary>

    It prints 12, 30 and 8.

    - The first call returns 22, but nobody stores it. The function changed its own local `hp`, not the caller's, so `hp` is still 12.
    - The second call computes `12 + 25 = 37`, clamps to the default `max_hp` of 30, and the caller stores it.
    - The keyword argument `max_hp=8` replaces the default. `5 + 5 = 10` clamps to 8.

    </details>

14. **[4 · compute · apply]** Use the lecture's Generation I model: `byte = percent × 255 // 100`, and a move hits when `roll < byte` for a roll from 0 to 255. Compute the stored byte and the real hit chance for moves listed at 95%, 90% and 75%. Then give each chance if the check were `roll <= byte`.

    <details>
    <summary>Answer</summary>

    | Listed | Byte | Rolls that hit with `<` | Chance with `<` | Chance with `<=` |
    |---|---|---|---|---|
    | 95% | `24,225 // 100 = 242` | 242 | 94.53% | 94.92% |
    | 90% | `22,950 // 100 = 229` | 229 | 89.45% | 89.84% |
    | 75% | `19,125 // 100 = 191` | 191 | 74.61% | 75.00% |

    With `<`, rolls 0 to `byte − 1` hit, which is `byte` rolls out of 256. With `<=`, one more roll hits. Every move is under its listing with `<`. With `<=`, the 75% move lands exactly on its listing and the others stay a little under.

    </details>

15. **[4 · compute · apply]** Using the lecture's two `hits()` functions: (a) D&D 5e, bonus +4. What is the hit chance against Armor Class 15, 26 and 3? (b) Diablo II, chance `2 × AR / (AR + DR) × alvl / (alvl + dlvl)` clamped to 5% to 95%. Compute it for AR 600, DR 400, levels 20 against 30, and for AR 2,000, DR 100, levels 40 against 10.

    <details>
    <summary>Answer</summary>

    (a) A normal roll hits when `roll + 4 >= AC`.

    - AC 15 needs 11 or more. Rolls 11 to 19 (9 rolls) plus the natural 20 make 10 of 20, so 50%.
    - AC 26 needs 22, which no normal roll reaches. Only the natural 20 hits, 5%.
    - AC 3 is met by every roll from 2 to 19, plus the natural 20. Only the natural 1 misses, 95%.

    (b) First case: `2 × 600 / 1,000 × 20 / 50 = 1.2 × 0.4 = 0.48`, so 48%, inside the band. Second case: `2 × 2,000 / 2,100 × 40 / 50 = 1.905 × 0.8 = 1.524`, a raw 152%, clamped to 95%.

    Both games end up with the same 5% to 95% band, written two different ways (early returns and a `min(max(...))` clamp).

    </details>

16. **[4 · code · apply]** The spec says "a target at exactly the weapon's reach is in range." The code is `def in_range(distance, reach): return distance < reach`. Write the three `assert` lines that test it at its edge for `reach = 64`, say which one fails, and fix the function.

    <details>
    <summary>Answer</summary>

    ```python
    assert in_range(63, 64) is True    # just inside
    assert in_range(64, 64) is True    # exactly at reach: fails with <
    assert in_range(65, 64) is False   # just outside
    ```

    With `<`, `in_range(64, 64)` returns False, so the second assert fails. The fix is `return distance <= reach`. The other two pass either way, which is why the lecture says to test each side of every comparison, not a typical value.

    </details>

17. **[4 · design · apply]** Decompose one purchase in a text-adventure shop ("buy potion") into four or five functions. For each, give its parameters, what it returns, and whether it can be pure.

    <details>
    <summary>Answer</summary>

    One good split:

    - `parse(text)` returns `(verb, noun)`. Pure.
    - `price_of(item, prices)` returns the price, or raises `KeyError` for an unknown item. Pure.
    - `can_afford(gold, price)` returns `gold >= price`. Pure, and it has a boundary to test (gold exactly equal to the price).
    - `buy(gold, inventory, item, price)` returns the new gold and a new inventory list. Pure if it builds a new list instead of changing the one it was given.
    - `shop_turn()` reads input, calls the four above, and prints the result. Not pure. This is the only function that talks to the player.

    Input and output stay at the edge, as in lecture section 3, so the rules can be tested with `assert` without typing into the game.

    </details>

## Week 5 · Arrays and lists: inventories

Lecture: [w05-arrays-and-lists-inventories.md](../lectures/w05-arrays-and-lists-inventories.md)

18. **[5 · code · apply]** What does the last line print?

    ```python
    bag = ["rope", "torch", "key"]
    bag.append("map")
    bag.insert(1, "gem")
    x = bag.pop()
    bag.remove("torch")
    print(bag, x, bag[-1], len(bag), bag[1:3])
    ```

    <details>
    <summary>Answer</summary>

    `['rope', 'gem', 'key'] map key 3 ['gem', 'key']`

    After `append`: rope, torch, key, map. After `insert(1, ...)`: rope, gem, torch, key, map. `pop()` removes and returns the last item, map. `remove("torch")` leaves rope, gem, key. The slice `[1:3]` takes indexes 1 and 2 and excludes 3.

    </details>

19. **[5 · code · apply]** Trace the lecture's two-pass `add_item` on `[("coin", 90), None, ("coin", 40), ("gem", 3)]` with stack size 99, adding 150 coins. Give the list and the return value. Then add 30 more coins to the result.

    <details>
    <summary>Answer</summary>

    | Pass | Slot | Before | Moved | After | Still to place |
    |---|---|---|---|---|---|
    | 1 | 0 | `("coin", 90)` | `min(9, 150) = 9` | `("coin", 99)` | 141 |
    | 1 | 2 | `("coin", 40)` | `min(59, 141) = 59` | `("coin", 99)` | 82 |
    | 2 | 1 | `None` | `min(99, 82) = 82` | `("coin", 82)` | 0 |

    Result `[("coin", 99), ("coin", 82), ("coin", 99), ("gem", 3)]`, return 0.

    Adding 30 more: pass 1 tops slot 1 up by 17 to 99, leaving 13. Pass 2 finds no `None`. The function returns 13, and those coins stay on the ground. The list has no empty slot and still took 17 coins, which is the lecture's "full, except it isn't."

    </details>

20. **[5 · compute · apply]** An invented game has 20 slots. Arrows stack to 50, potions to 10, swords to 1. (a) How many arrows fit in an empty inventory? (b) The inventory holds 3 swords, arrow stacks of 35 and 50, a potion stack of 7 and 14 empty slots. What is the room for arrows and for potions? (c) How many slots do 230 arrows need, and 230 potions?

    <details>
    <summary>Answer</summary>

    (a) `20 × 50 = 1,000` arrows.

    (b) Room is free space in matching stacks plus a full stack per empty slot. Arrows: `(50 − 35) + (50 − 50) + 14 × 50 = 15 + 0 + 700 = 715`. Potions: `(10 − 7) + 14 × 10 = 143`.

    (c) `ceil(230 / 50) = 5` slots for arrows. `ceil(230 / 10) = 23` slots for potions, more than the inventory has, so 230 potions never fit. The stack size, not the slot count, is what makes potions the scarce item here.

    </details>

21. **[5 · code · apply]** What does this print? Name each list that is an alias.

    ```python
    base = [10, 20]
    a = base
    b = base.copy()
    a.append(30)
    b[0] = 99
    grid = [[0] * 2] * 2
    grid[1][0] = 7
    print(base, b, grid)
    ```

    <details>
    <summary>Answer</summary>

    `[10, 20, 30] [99, 20] [[7, 0], [7, 0]]`

    `a` is a second name for `base`, so appending through `a` changes `base`. `b` is a real copy, so changing it leaves `base` alone. `[[0] * 2] * 2` puts the same inner list in both rows, so writing to row 1 shows up in row 0 too. Build the grid with `[[0] * 2 for _ in range(2)]`.

    </details>

22. **[5 · critique · apply]** A cleanup loop is meant to drop every broken item. What is left after it runs, and why? Rewrite it so it works.

    ```python
    items = ["broken_a", "broken_b", "sword", "broken_c"]
    for item in items:
        if item.startswith("broken"):
            items.remove(item)
    ```

    <details>
    <summary>Answer</summary>

    It leaves `["broken_b", "sword"]`. The loop looks at index 0 and removes `broken_a`, which shifts `broken_b` into index 0. The loop moves on to index 1 (`sword`), so `broken_b` is never checked. At index 2 it finds `broken_c` and removes it. Then the list has only two items and the loop ends.

    Build a new list instead of changing the one you are walking:

    ```python
    items = [item for item in items if not item.startswith("broken")]
    ```

    </details>

## Week 6 · Dictionaries: item databases

Lecture: [w06-dictionaries-item-databases.md](../lectures/w06-dictionaries-item-databases.md)

23. **[6 · code · apply]** What do the two `print` lines show? Is anything in the result a bug?

    ```python
    stock = {"arrow": 20, "potion": 2}
    for item in ["potion", "bomb", "potion", "arrow"]:
        stock[item] = stock.get(item, 0) - 1
    print(stock)
    print(stock.get("shield", "none"), "bomb" in stock, len(stock))
    ```

    <details>
    <summary>Answer</summary>

    ```
    {'arrow': 19, 'potion': 0, 'bomb': -1}
    none True 3
    ```

    Potions go 2, 1, 0. `bomb` did not exist, so `.get` gives 0 and the new entry is −1. Arrows go to 19. Keys keep insertion order, so `bomb` comes last.

    The −1 bomb is a bug. The code spends an item the player never had, and `.get` with a default hid that. A "use item" rule should check `stock.get(item, 0) > 0` first and refuse otherwise. `.get` is right for "how many do I have?", not for "take one away."

    </details>

24. **[6 · compute · apply]** (a) A list database has 750 items. How many comparisons does a linear search need on average for an item that exists, and for one that does not? (b) Another game stores items in a list with `ID = 500 + index` for 60 items. A patch inserts a new item at index 20. How many old items change ID? What ID does the item that used to be 530 have now, and what does an old save that says "530" load?

    <details>
    <summary>Answer</summary>

    (a) Present: `(750 + 1) / 2 = 375.5` on average. Missing: all 750. A dictionary needs about one hash and one comparison either way.

    (b) Items at old indexes 20 to 59 all move up one place, so 40 items change ID. The item at index 30 (ID 530) moves to index 31, so its ID becomes 531. ID 530 now points at index 30, which holds the item that used to be at index 29 (old ID 529). The save loads the wrong item without any error.

    </details>

25. **[6 · code · apply]** Using the lecture's `ITEM_DB` (wooden sword 10 gold, iron sword 60, potion 15, arrow 1), write `total_value(inventory, db)` and compute it for `[("arrow", 64), ("potion", 4), None, ("iron_sword", 1), ("arrow", 12)]`. Then write one comprehension that lists the keys of items whose `damage` is above 4, without crashing on items that have no damage.

    <details>
    <summary>Answer</summary>

    ```python
    def total_value(inventory, db):
        return sum(db[slot[0]]["price"] * slot[1]
                   for slot in inventory if slot is not None)
    ```

    `64 × 1 + 4 × 15 + 1 × 60 + 12 × 1 = 64 + 60 + 60 + 12 = 196`.

    ```python
    strong = [k for k, v in ITEM_DB.items() if v.get("damage", 0) > 4]   # ['iron_sword']
    ```

    Here `.get("damage", 0)` is the right tool. `damage` is an optional field, and "no damage" really means 0. In `total_value`, `db[slot[0]]` should stay a plain lookup. An inventory key missing from the database is a data bug that should fail loudly.

    </details>

26. **[6 · critique · apply]** A teammate writes `dmg = ITEM_DB.get(key, {}).get("damage", 0)` "so the game never crashes." A quest script gives the player the key `"iron_sowrd"`. What happens in play, and what should the code do instead?

    <details>
    <summary>Answer</summary>

    The outer `.get` returns `{}` for the misspelt key, and the inner `.get` returns 0. The player equips a sword that does 0 damage, with no error anywhere. Someone finds it hours later in a bug report ("my sword does nothing").

    `ITEM_DB[key]["damage"]` would raise `KeyError: 'iron_sowrd'` the first time the script ran. Better still, validate every key a quest or save refers to when the game starts, as the lecture's `validate` does for fields. Use `.get` only where missing has a real meaning.

    </details>

27. **[6 · design · apply]** Version 1.0 of your game stored inventory slots as list positions (`ID = index`). Version 1.1 switches to string keys and also renames `"short_sword"` to `"iron_dagger"`. Design the load path for an old save in four or five steps.

    <details>
    <summary>Answer</summary>

    1. Read the save's version field. A save with no version field is treated as version 1.
    2. For a version 1 save, convert each numeric slot to a key with the frozen version 1 ID list (the list exactly as 1.0 shipped it, kept in the code forever).
    3. Pass every key through an alias table, `ALIASES = {"short_sword": "iron_dagger"}`, so renamed items resolve to their new key.
    4. Check that every resulting key exists in `ITEM_DB`, and fail loudly with the slot number if one does not.
    5. Write the save back as version 2 with string keys, and return a new dictionary rather than editing the old one.

    Lab 06 builds steps 2, 3 and 5.

    </details>

## Week 7 · Engine intro: scenes, nodes and scripts (Godot)

Lecture: [w07-engine-intro-scenes-nodes-scripts.md](../lectures/w07-engine-intro-scenes-nodes-scripts.md)

28. **[7 · compute · apply]** A scene tree is `Game` with children `Camera`, `Level` and `HUD`. `Level` has children `Player` and `Enemies`. `Player` has child `Gun`. `Enemies` has children `Bat` and `Rat`. (a) Give the `_enter_tree`, `_ready` and `_process` orders. (b) `Camera` gets `process_priority = 10` and every other node keeps 0. What is the new `_process` order?

    <details>
    <summary>Answer</summary>

    (a) `_enter_tree` and `_process` are pre-order: Game, Camera, Level, Player, Gun, Enemies, Bat, Rat, HUD.

    `_ready` is post-order, children before parents: Camera, Gun, Player, Bat, Rat, Enemies, Level, HUD, Game.

    (b) Lower priority runs first, and ties keep tree order. Everything except `Camera` has 0, so they run in pre-order and `Camera` runs last: Game, Level, Player, Gun, Enemies, Bat, Rat, HUD, Camera. That is the usual reason to raise a camera's priority, so it reads the player's position after the player has moved.

    </details>

29. **[7 · compute · apply]** A boss moves at 800 px/s. A `Bar` copies the boss's x each frame, and a `Label` copies the bar's x. (a) Tree order `Bar`, `Label`, `Boss`. What is each follower's lag in frames, and the label's gap at 60 fps and at 30 fps? (b) Tree order `Label`, `Bar`, `Boss`. What is the label's gap at 144 fps?

    <details>
    <summary>Answer</summary>

    Count the links that run in the wrong order, then use `gap = lag_frames × v / fps`.

    (a) `Bar` runs before `Boss`, which is wrong, so the bar lags 1 frame. `Label` runs after `Bar`, which is right, so the label adds nothing and also lags 1 frame in total. The label's gap is `800 / 60 = 13.33` px at 60 fps and `800 / 30 = 26.67` px at 30 fps.

    (b) Both links are now wrong. `Label` runs before `Bar`, and `Bar` before `Boss`, so the label lags 2 frames, and its gap is `2 × 800 / 144 = 11.11` px. That is almost the same gap as (a) at 60 fps, on a much faster screen.

    </details>

30. **[7 · critique · apply]** The boss in question 29 spins while it attacks. A teammate fixes the bar by making it a child of the boss. Is that the right fix here? Compare it with the other two fixes from the lecture.

    <details>
    <summary>Answer</summary>

    Parenting removes the lag at every speed, but the bar inherits the boss's rotation and scale, so it spins with the boss. That makes it the wrong fix for a spinning boss.

    The better fix is `process_priority`. Give the bar and label a higher priority than the boss so they always run after it. The order is then written in the node's settings and survives a teammate reordering the Scene panel. Reordering the tree also works today, but nothing records why the order matters, so it is the easiest fix to break. Add a one-line comment on the bar script whichever you choose.

    </details>

31. **[7 · explain · apply]** A scene is `Main` with children `HUD` and `Player`, in that order. `HUD._ready()` reads `$"../Player".max_hp` to size its health bar, and `Player._ready()` sets `max_hp = 120`. The bar comes out sized for 0. Explain with the traversal order and give two fixes.

    <details>
    <summary>Answer</summary>

    `_ready` runs in post-order: HUD, then Player, then Main. When `HUD._ready()` runs, `Player._ready()` has not run yet, so `max_hp` still has its default of 0. Siblings are not guaranteed ready in `_ready`. Only your own children are.

    Fixes: (1) give `max_hp` its value in the declaration (`var max_hp := 120`), so it is set before any `_ready` runs; or (2) do the wiring in `Main._ready()`, which runs after both children are ready, for example by calling `hud.set_max_hp(player.max_hp)` there. A third option is to let the player emit a signal when its health is set up and have the HUD connect to it.

    </details>

## Week 8 · Input handling and movement

Lecture: [w08-input-handling-and-movement.md](../lectures/w08-input-handling-and-movement.md)

32. **[8 · compute · apply]** A key's held state over eight frames is `no, yes, yes, no, yes, no, no, yes`. On which frames is `just_pressed` true, and on which is `just_released` true? A character that jumps on `held` instead would jump on how many of these frames if it were grounded throughout?

    <details>
    <summary>Answer</summary>

    `just_pressed` is `held and not was_held`, true on frames 2, 5 and 8. `just_released` is `was_held and not held`, true on frames 4 and 6.

    Jumping on `held` would try to jump on frames 2, 3, 5 and 8, four frames. Frame 3 is the extra one. In play the character is airborne by frame 3, so the bug shows as a bunny hop on the first grounded frame while the key is still down.

    </details>

33. **[8 · compute · apply]** A runner moves at 90 px/s. (a) At 75 fps with a coyote window `C = 0.13` s, what is the last airborne frame on which a jump still works, and how far past the edge is the runner? (b) The programmer changes the window to "6 frames". How long is that window at 75 fps and at 40 fps, and how far past the edge can the runner jump at each?

    <details>
    <summary>Answer</summary>

    (a) The last allowed frame is the largest whole `k` with `k / 75 ≤ 0.13`. `0.13 × 75 = 9.75`, so `k = 9`, at `9 / 75 = 0.12` s. Distance `90 × 0.12 = 10.8` px.

    (b) Six frames last `6 / 75 = 0.08` s at 75 fps (7.2 px) and `6 / 40 = 0.15` s at 40 fps (13.5 px). The slow machine gets almost twice the forgiveness of the fast one. Store the window in seconds.

    </details>

34. **[8 · code · apply]** Run the lecture's `JumpInput` at 60 fps with `C = 0.1` and `B = 0.1`. The player is grounded on frames 1 to 3, airborne on frames 4 to 20, and grounded again from frame 21. Jump is held on frames 16 to 25 and released after. (a) On which frame does a jump fire? (b) Which frame fires with `B = 0.05`? (c) Which frame fires with `B = 0.1` and `C = 0`?

    <details>
    <summary>Answer</summary>

    The press edge is on frame 16, in the air. `since_ground` there is 13 frames, `13 / 60 = 0.217` s, above `C`, so no jump. On frame 21 the player lands, so `since_ground = 0`. `since_press` has grown for 5 frames, `5 / 60 = 0.083` s.

    (a) `0.083 ≤ 0.1`, so the jump fires on frame 21, the landing frame. Both timers reset, so the key still held on frames 22 to 25 does nothing.

    (b) `0.083 > 0.05`, so frame 21 does not fire. The key is still held, so no new edge arrives, and the jump never fires. The player pressed and was ignored.

    (c) The same as (a), frame 21. On the landing frame `since_ground` is 0, which passes `C = 0`. The buffer does the work here, not coyote time.

    </details>

35. **[8 · compute · apply]** A character uses `velocity.x = move_toward(velocity.x, target, accel × mult × delta)` with a top speed of 130 px/s, a ground acceleration of 1,000 px/s² and an air multiplier of 0.5. How long does it take to reach top speed on the ground and in the air, and how many physics ticks is that at 60 Hz?

    <details>
    <summary>Answer</summary>

    Time is `max / (accel × mult)`.

    - Ground: `130 / 1,000 = 0.13` s. Each tick adds `1,000 / 60 = 16.67` px/s, and `130 / 16.67 = 7.8`, so it reaches 130 on tick 8 (the last step is clamped by `move_toward`).
    - Air: `130 / 500 = 0.26` s. Each tick adds 8.33 px/s, and `130 / 8.33 = 15.6`, so tick 16.

    Because the step is `accel × delta`, the time in seconds is the same at any tick rate. Only the tick count changes.

    </details>

36. **[8 · explain · apply]** For each action, say whether to read `held`, `just_pressed` or `just_released`, and whether it belongs in `_unhandled_input` or `_physics_process`: (a) walking left and right, (b) opening the pause menu, (c) a charged shot that fires when you let go, (d) an automatic rifle with a cooldown.

    <details>
    <summary>Answer</summary>

    (a) `held`, polled in `_physics_process`, because walking is continuous and uses physics.

    (b) A pressed event, in `_unhandled_input` with `event.is_action_pressed("pause")`. It is a one-off action, and menus should be able to take the event first.

    (c) Charge while `held` and fire on `just_released`, both polled in `_physics_process`, where the shot is created.

    (d) `held` plus a cooldown timer in seconds, in `_physics_process`. The cooldown sets the fire rate. With `just_pressed` it would become semi-automatic, which is a different design.

    </details>

## Week 9 · Delta time and frame-rate independence

Lecture: [w09-delta-time-and-frame-rate-independence.md](../lectures/w09-delta-time-and-frame-rate-independence.md)

37. **[9 · compute · apply]** A game was tuned on a 75 Hz monitor and moves the player 4 px per frame. How fast is the player, and how long does a 1,200 px screen take to cross, at 50, 75 and 165 fps? What single line fixes it?

    <details>
    <summary>Answer</summary>

    Speed is `s × fps`.

    | fps | Speed (px/s) | Time to cross 1,200 px |
    |---|---|---|
    | 50 | 200 | 6.00 s |
    | 75 | 300 | 4.00 s |
    | 165 | 660 | 1.82 s |

    The fix states the speed the designer meant, 300 px/s, and multiplies by the frame time: `position.x += 300.0 * delta`.

    </details>

38. **[9 · code · apply]** This `_process` body was written for 60 fps. Classify each line as correct, needs `dt`, or needs a power, and rewrite it. `cooldown` starts at 30 and means "half a second".

    ```python
    x += 3                 # drift right
    speed *= 0.95          # friction
    cooldown -= 1          # counts down to the next shot
    vy = -400              # jump impulse, set once when jump fires
    ```

    <details>
    <summary>Answer</summary>

    ```python
    x += 180 * dt                  # needs dt: 3 px per frame at 60 fps is 180 px/s
    speed *= 0.95 ** (dt * 60)     # needs a power: same loss per second as at 60 fps
    cooldown -= dt                 # needs dt: start it at 0.5 s instead of 30
    vy = -400                      # correct: a one-off impulse in px/s, no dt
    ```

    Additions per frame become rate × `dt`. Multiplications per frame become a power of `dt`. Values that are set once, like an impulse, need nothing. A cooldown that ends should add 0.5 back rather than reset to 0.5, so the leftover fraction of a frame is kept (lab 09 step 3).

    </details>

39. **[9 · compute · apply]** Friction applies `speed *= 0.95` every frame. What fraction of the speed is left after one second at 30, 60 and 144 fps? What is it at every rate with `speed *= 0.95 ** (dt * 60)`?

    <details>
    <summary>Answer</summary>

    Per frame, `0.95^fps` is left after one second: 0.2146 at 30 fps, 0.0461 at 60 fps and 0.00062 at 144 fps. The 30 fps player slides almost five times as far into the second as the 60 fps player. The 144 fps player stops almost dead.

    With the power form, each frame multiplies by `0.95^(dt × 60)`. Over one second that is `0.95^(60 × dt × fps) = 0.95^60 = 0.0461` at every frame rate, the value the designer tuned at 60 fps.

    </details>

40. **[9 · code · apply]** Run the lecture's `jump_apex` with `v0 = 300` px/s and `g = 900` px/s² at 30, 60 and 120 fps. What is the exact apex, what does semi-implicit Euler give, and does the error estimate `v0 × dt / 2` match? A ledge is 47 px high. Who can reach it?

    <details>
    <summary>Answer</summary>

    Exact apex `v0² / (2g) = 90,000 / 1,800 = 50` px.

    | fps | Semi-implicit Euler | Estimate `50 − 300 × dt / 2` | Explicit Euler (lines swapped) |
    |---|---|---|---|
    | 30 | 45.00 px | 45.00 | 55.00 px |
    | 60 | 47.50 px | 47.50 | 52.50 px |
    | 120 | 48.75 px | 48.75 | 51.25 px |

    The estimate matches exactly here. A 47 px ledge is reachable at 60 and 120 fps and not at 30 fps, even though every line uses `dt` correctly. With a fixed 60 Hz step every player gets 47.50 px, so everyone can reach it.

    </details>

41. **[9 · compute · apply]** Trace Fiedler's accumulator with a 60 Hz simulation (`SIM_DT = 16.67` ms) on a 75 fps display, starting empty. Give steps, leftover and `alpha` for five frames. Then give the pattern for a 50 Hz simulation on a 60 fps display over six frames.

    <details>
    <summary>Answer</summary>

    75 fps deposits `1000 / 75 = 13.33` ms per frame.

    | Frame | Accumulator before steps | Steps | Leftover | alpha |
    |---|---|---|---|---|
    | 1 | 13.33 | 0 | 13.33 ms | 0.800 |
    | 2 | 26.67 | 1 | 10.00 ms | 0.600 |
    | 3 | 23.33 | 1 | 6.67 ms | 0.400 |
    | 4 | 20.00 | 1 | 3.33 ms | 0.200 |
    | 5 | 16.67 | 1 | 0.00 ms | 0.000 |

    Four steps in five frames, `4 / 5 = 60 / 75`. (Without a tolerance, floats can leave the accumulator a hair under 16.67 ms on frame 5, which shows 0 steps and alpha 1.000 and moves the step a frame later. The lecture's `run_accumulator` compares with `sim_dt - EPS` to avoid exactly this.)

    50 Hz simulation on 60 fps: each frame deposits 16.67 ms and each step withdraws 20 ms. Steps 0, 1, 1, 1, 1, 1. Leftovers 16.67, 13.33, 10.00, 6.67, 3.33, 0.00 ms. Five steps per six frames, which is 50 per 60.

    </details>

42. **[9 · compute · apply]** A game uses a 50 Hz simulation and clamps frame time at 0.25 s. The player drags the window and one frame lasts 0.6 s. How many steps run in that frame with the clamp and without it, and how much game time is lost with the clamp? What is the most game time Godot's default settings will simulate in one frame?

    <details>
    <summary>Answer</summary>

    With the clamp, 0.25 s is deposited. `0.25 / 0.02 = 12.5`, so 12 steps run and 10 ms stays in the accumulator (alpha 0.5). The game loses `0.6 − 0.25 = 0.35` s of simulated time. Without the clamp, `0.6 / 0.02 = 30` steps run in one frame.

    Godot runs at most `max_physics_steps_per_frame = 8` steps at the default 60 ticks per second, so at most `8 / 60 = 0.133` s of game time per frame.

    </details>

## Week 10 · Collision basics: AABB and circles

Lecture: [w10-collision-basics-aabb-and-circles.md](../lectures/w10-collision-basics-aabb-and-circles.md)

43. **[10 · compute · apply]** The player box is `a = (40, 60, 24, 32)` as `(x, y, w, h)`, with y pointing down. For each box, fill in the four comparisons from the lecture, say whether they overlap, and give `(ox, oy)` and the push-out when they do: `b1 = (60, 80, 20, 20)`, `b2 = (64, 70, 10, 10)`, `b3 = (20, 20, 16, 16)`, `b4 = (30, 90, 40, 6)`.

    <details>
    <summary>Answer</summary>

    Edges of `a`: left 40, right 64, top 60, bottom 92.

    | Box | 1. `40 < b.right` | 2. `64 > b.left` | 3. `60 < b.bottom` | 4. `92 > b.top` | Overlap? |
    |---|---|---|---|---|---|
    | b1 (60 to 80, 80 to 100) | 40 < 80 ✓ | 64 > 60 ✓ | 60 < 100 ✓ | 92 > 80 ✓ | yes |
    | b2 (64 to 74, 70 to 80) | 40 < 74 ✓ | 64 > 64 ✗ | 60 < 80 ✓ | 92 > 70 ✓ | no, touching |
    | b3 (20 to 36, 20 to 36) | 40 < 36 ✗ | 64 > 20 ✓ | 60 < 36 ✗ | 92 > 20 ✓ | no |
    | b4 (30 to 70, 90 to 96) | 40 < 70 ✓ | 64 > 30 ✓ | 60 < 96 ✓ | 92 > 90 ✓ | yes |

    b1: `ox = min(64, 80) − max(40, 60) = 4`, `oy = min(92, 100) − max(60, 80) = 12`. Push on x by 4. The player's center x (52) is left of b1's (70), so push left, `a.x = 36`.

    b3 fails comparisons 1 and 3, so it lies up and to the left. b2 shares the line x = 64 and no area.

    b4: `ox = min(64, 70) − max(40, 30) = 24`, `oy = min(92, 96) − max(60, 90) = 2`. Push on y by 2. The player's center y (76) is above b4's (93), so push up, `a.y = 58`. The player now stands on the platform.

    </details>

44. **[10 · code · apply]** Two circles have radii 12 and 20. Circle 1 is at `(0, 0)`. Use the squared-distance test to decide overlap when circle 2 is at `(24, 20)` and when it is at `(26, 21)`. Write the test as a one-line Python expression with no square root.

    <details>
    <summary>Answer</summary>

    ```python
    dx * dx + dy * dy < (r1 + r2) * (r1 + r2)
    ```

    Reach squared is `32² = 1,024`.

    - `(24, 20)`: `576 + 400 = 976 < 1,024`, overlap. The true distance is about 31.24.
    - `(26, 21)`: `676 + 441 = 1,117`, not less than 1,024, no overlap. The true distance is about 33.42.

    You never needed the square roots to decide.

    </details>

45. **[10 · compute · apply]** A round bullet of radius 5 meets the player box `(40, 60, 24, 32)` (left 40, right 64, top 60, bottom 92). Use the lecture's nearest-point method for bullet centers `(68, 56)`, `(67, 62)` and `(52, 76)`. For the first one, what would a box test on the bullet's own 10 × 10 bounding square say?

    <details>
    <summary>Answer</summary>

    Clamp the center into the box on each axis, then compare the squared distance with `5² = 25`.

    | Center | Nearest point | Offset | Squared distance | Hit? |
    |---|---|---|---|---|
    | (68, 56) | (64, 60), the top-right corner | (4, −4) | 32 | no |
    | (67, 62) | (64, 62), on the right edge | (3, 0) | 9 | yes |
    | (52, 76) | (52, 76), inside the box | (0, 0) | 0 | yes |

    The first bullet's bounding square runs from 63 to 73 on x and 51 to 61 on y. It pokes 1 px into the box on both axes, so a box test says hit while the round bullet misses the corner by about 0.66 px (`√32 ≈ 5.66` against a radius of 5). That is the corner problem from the lecture, seen from the bullet's side. The third case shows the method also works when the center is already inside the box.

    </details>

46. **[10 · compute · apply]** A 3 px bullet flies at 1,800 px/s. The thinnest wall is 20 px. (a) Below what frame rate can it tunnel? (b) At 60 fps, how many substeps per frame make it safe? (c) At 30 fps with no substeps, how thick must walls be?

    <details>
    <summary>Answer</summary>

    Tunneling is possible when `v / f > t + s`, here `1,800 / f > 23`.

    (a) `f < 1,800 / 23 = 78.3` fps. At 60 fps the step is 30 px, so it can tunnel.

    (b) With `n` substeps the step is `30 / n`. It must be at most 23, so `n ≥ 1.3` and `n = 2` (15 px steps).

    (c) At 30 fps the step is 60 px. Walls need `t > v / f − s = 60 − 3 = 57` px.

    </details>

47. **[10 · critique · apply]** A student tests box overlap with "is any corner of `a` inside `b`, or any corner of `b` inside `a`?" Give a pair of boxes where this says no and the boxes overlap. Then say how many pair checks a brute-force loop does per frame for 60 objects, and one way to cut that without changing the overlap test.

    <details>
    <summary>Answer</summary>

    A plus sign. A tall thin box `a = (110, 80, 10, 90)` and a wide flat box `b = (90, 110, 60, 20)` cross in the middle. No corner of either lies inside the other, yet their x intervals (110 to 120 against 90 to 150) and y intervals (80 to 170 against 110 to 130) both overlap, so the four comparisons say yes.

    Brute force needs `60 × 59 / 2 = 1,770` pair checks per frame. Skip pairs that can never matter (the player's bullets against the player, pickups against walls) with Godot's collision layers and masks. That is the cheap first step before any broad phase.

    </details>

## Week 11 · Game state machines

Lecture: [w11-game-state-machines.md](../lectures/w11-game-state-machines.md)

48. **[11 · compute · apply]** Use the level 1 ghost schedule (scatter 7, chase 20, scatter 7, chase 20, scatter 5, chase 20, scatter 5, then chase) with 6 s of fright that pauses the schedule clock. Power pellets are eaten at 3 s and at 15 s. (a) List every transition time. (b) What mode are the ghosts in at 40 s? (c) How many reversals have happened by 45 s? (d) When does the endless chase begin?

    <details>
    <summary>Answer</summary>

    (a) At 3 s the ghosts are 3 s into scatter. Fright runs 3 to 9 and the clock is frozen, so scatter resumes at 9 with 4 s left and ends at 13. Chase starts at 13. The pellet at 15 s comes 2 s into chase, so fright runs 15 to 21 and chase resumes with 18 s left, ending at 39. Every later boundary is 12 s late: scatter 39 to 46, chase 46 to 66, scatter 66 to 71, chase 71 to 91, scatter 91 to 96, then chase.

    Transitions: 3 (scatter to frightened), 9 (frightened to scatter), 13 (scatter to chase), 15 (chase to frightened), 21 (frightened to chase), 39, 46, 66, 71, 91, 96.

    (b) Scatter (phase 3, 39 to 46).

    (c) Reversals happen on every transition except the exit from frightened. By 45 s: 3, 13, 15 and 39, so 4. The changes at 9 and 21 do not reverse.

    (d) 96 s, the same as `84 + 6 + 6`. A frame-stepped simulation prints times up to one frame late, such as 3.02 and 13.03.

    </details>

49. **[11 · compute · apply]** (a) A game tracks its mode with six booleans and has seven legal modes. How many illegal combinations can the flags represent? (b) Run this event list through the lecture's seven-row transition table, starting in `MENU`: `start, pause, start, resume, out_of_lives, pause, retry, quit`. Which events are ignored, what is the final state, and how many times are score and lives reset?

    <details>
    <summary>Answer</summary>

    (a) `2^6 = 64` combinations, 7 legal, so 57 illegal.

    (b)

    | Event | Pair in table? | State after |
    |---|---|---|
    | start | yes | PLAY (reset) |
    | pause | yes | PAUSE |
    | start | no, ignored | PAUSE |
    | resume | yes | PLAY |
    | out_of_lives | yes | GAME_OVER |
    | pause | no, ignored | GAME_OVER |
    | retry | yes | PLAY (reset) |
    | quit | no, ignored | PLAY |

    Three events are ignored, five are handled, and the final state is PLAY. Score and lives reset twice, on `start` and on `retry`, never on `resume`. `(PLAY, quit)` is not in the table, so quitting from play needs a pause first. Whether that is right is a design question worth asking.

    </details>

50. **[11 · critique · apply]** A student puts `$Music.play()` (start the level music from the beginning) in the enter action for `PLAY`. What does a player hear when they pause and resume? Where should the line go, and what should the enter and exit actions of `PAUSE` do instead?

    <details>
    <summary>Answer</summary>

    Entering `PLAY` from `PAUSE` is still entering `PLAY`, so the music restarts from the beginning every time the player unpauses. It is the same mistake as resetting the score in `on_enter(PLAY)`.

    Starting the music belongs to the transitions that start a run, `start` and `retry`, next to the score reset. The pause can lower or stop the music in its enter action and bring it back in its exit action. Because the enter and exit actions belong to `PAUSE`, they fire on every path into and out of it, which is what you want there.

    </details>

51. **[11 · design · apply]** Add a `GET_READY` state that shows "3, 2, 1" for 2 seconds before play, both on a new game and on retry. Write the changed and new rows of the transition table and the enter action and update for `GET_READY`. Where do the score and lives reset now?

    <details>
    <summary>Answer</summary>

    | Current state | Event | Next state | Transition action |
    |---|---|---|---|
    | MENU | `start` | GET_READY | reset score and lives |
    | GAME_OVER | `retry` | GET_READY | reset score and lives |
    | GET_READY | `ready_done` | PLAY | — |

    ```python
    def on_enter_get_ready(game):
        game["countdown"] = 2.0

    def update_get_ready(game, dt):
        game["countdown"] -= dt
        if game["countdown"] <= 0:
            handle(game, "ready_done")
    ```

    The reset stays on the `start` and `retry` transitions. Moving it to `on_enter(GET_READY)` would also work today, because pause never leads into `GET_READY`, but it is fragile. The day someone adds "resume via countdown", the unpause bug returns. The countdown clock only runs while the state is `GET_READY`, so pause needs no special code.

    </details>

52. **[11 · explain · recall]** In the lecture's ghost machine, why does `update` subtract the phase duration (`phase_time -= duration`) instead of setting `phase_time = 0`, and why is the reversal written inside `change_mode` rather than in the scatter and chase code?

    <details>
    <summary>Answer</summary>

    A phase usually ends partway through a frame. Subtracting keeps the leftover part of that frame and carries it into the next phase. Setting it to 0 throws that leftover away, so each phase runs up to a frame long and the error adds up over the schedule (lab 11 step 3 measures it at a slow frame rate).

    The reversal belongs to the transition, not to either state. `change_mode` is the only place that assigns `mode`, so every path into a new mode passes through it and the reversal cannot be forgotten on one path. It also knows the old mode, which is what the "no reversal when leaving frightened" exception needs.

    </details>

## Week 12 · Debugging: breakpoints, logging, rubber-ducking

Lecture: [w12-debugging-breakpoints-logging-rubber-ducking.md](../lectures/w12-debugging-breakpoints-logging-rubber-ducking.md)

53. **[12 · compute · apply]** An endless mode breaks somewhere in levels 1 to 5,000. A script plays to any chosen level in about 45 seconds. How many runs does bisecting need, and how long does it take? How does that compare with testing every level in order?

    <details>
    <summary>Answer</summary>

    `2^12 = 4,096 < 5,000 ≤ 8,192 = 2^13`, so 13 runs. `13 × 45 s = 585 s`, just under 10 minutes. Testing every level in order could take up to 5,000 runs, about 62 hours. Bisecting needs a yes-or-no check ("is level N broken?") and a bug that stays broken once it starts.

    </details>

54. **[12 · code · apply]** An invented game computes each level's time limit in one byte: `time_limit = (100 + 10 * level) % 256`. (a) What limits do levels 15, 16 and 17 get? (b) Write a regression test that would have caught this before release. (c) What is the fix if the save file must still store the limit in one byte?

    <details>
    <summary>Answer</summary>

    (a) Level 15: 250. Level 16: `260 mod 256 = 4`. Level 17: 14. The player gets 4 seconds on level 16, a kill screen of the same shape as the lecture's Donkey Kong example.

    (b) State the designer's story for every level, in the style of the lecture's fruit-row test:

    ```python
    def test_time_limit_never_drops():
        for level in range(1, 100):
            assert time_limit(level) >= time_limit(level - 1), level
    ```

    It fails and reports 16.

    (c) Do the arithmetic in full-size integers and clamp before storing, `min(100 + 10 * level, 255)`. Levels 16 and later then keep 255, the largest value a byte holds. If the design needs larger limits, store the level (or seconds in larger units) and compute the limit on load.

    </details>

55. **[12 · critique · apply]** A student gets this traceback and starts editing `apply_hit`. Read it from the bottom up. Where is the bug, and what is the one-line fix?

    ```
    Traceback (most recent call last):
      File "game.py", line 16, in <module>
        fight()
      File "game.py", line 12, in fight
        hp = apply_hit(hp, 12, 4)
      File "game.py", line 7, in apply_hit
        return hp - damage(attack, armor)
    TypeError: unsupported operand type(s) for -: 'int' and 'NoneType'
    ```

    ```python
    def damage(attack, armor):
        result = max(1, attack - armor)
        print(result)

    def apply_hit(hp, attack, armor):
        return hp - damage(attack, armor)
    ```

    <details>
    <summary>Answer</summary>

    The last line says an `int` minus `None` failed. The line above shows the subtraction in `apply_hit`, and the right-hand value comes from `damage`. The error appears where the bad value is used, but the bug is where it was made. `damage` prints its result and never returns it, so it returns `None`. The program also printed 8 just before the crash, which is the clue.

    Fix `damage` with `return result` in place of the `print`. `apply_hit` is correct and should not change. Python 3.13 also underlines the failing expression with `~` and `^` marks, which point at the same subtraction.

    </details>

56. **[12 · explain · apply]** Pick the first tool (log, conditional breakpoint or rubber duck) for each report and say what you would observe. (a) "About once a minute a coin can't be picked up." (b) "The score is wrong right after the third wave starts." (c) "I rewrote the enemy AI and now nothing moves, and I don't know where to start." (d) "Bullets pass through walls on my old laptop but never on my desktop."

    <details>
    <summary>Answer</summary>

    (a) A log. The bug is rare and you need history. Log each pickup test with the frame number, both positions and the result, and read the lines around a failure.

    (b) A conditional breakpoint, `if wave == 3 and state == "PLAY": breakpoint()`, at the top of the score update. You need one moment in full detail. Inspect the score and whatever feeds it, then step forward.

    (c) The rubber duck. You do not yet know what to observe. Explain the new AI's update line by line and note every "always" and "never". Those are the claims to test.

    (d) A log, not a breakpoint. Pausing changes the timing, and the bug depends on large frame steps. Log `delta` and each bullet's step with the frame number, only when the step exceeds the wall thickness (week 10's tunneling condition).

    </details>

## Week 13 · Randomness: spawning and procedural variety

Lecture: [w13-randomness-spawning-and-procedural-variety.md](../lectures/w13-randomness-spawning-and-procedural-variety.md)

57. **[13 · compute · apply]** A designer changes the NES-style randomizer. The first roll is now 0 to 9 for seven pieces, so there are three dummy values (7, 8 and 9). A dummy or a repeat triggers one reroll from 0 to 6, which is always dealt. What is the chance that the next piece repeats the current one? Compare it with `1/28`.

    <details>
    <summary>Answer</summary>

    A repeat needs the first roll rejected and the second roll to hit the same piece. The first roll is rejected on any of the 3 dummies or on the one matching piece, `4/10`. The reroll repeats with chance `1/7`. So `4/10 × 1/7 = 4/70 = 2/35 ≈ 5.7%`.

    That is higher than the original `1/28 ≈ 3.6%`. More dummy values means more rerolls, and every reroll is a fresh chance to repeat. A 200,000-piece simulation of this rule gives 5.72%.

    </details>

58. **[13 · compute · apply]** A shooter deals one of five enemy types per spawn. (a) With a 5-bag, what is the longest possible gap between two spawns of the same type, and the chance that two spawns in a row are the same type? (b) With pure random picks, what is the chance of 10 or more spawns in a row without a given type?

    <details>
    <summary>Answer</summary>

    (a) The worst case puts the type first in one bag and last in the next. The other 4 of the first bag and the first 4 of the next lie between them, `4 + 4 = 8`. A repeat can only happen at a bag boundary, one position in five, with chance `1/5` there, so `1/5 × 1/5 = 1/25 = 4%`. Checking every pair of bag orders by brute force confirms the maximum of 8.

    (b) Each pick misses the type with chance `4/5`, so `(4/5)^10 ≈ 0.107`, about 10.7%. There is no maximum.

    </details>

59. **[13 · compute · apply]** A spawner uses rejection sampling in a 1,000 × 600 arena with the player at the center and a 180 px safe radius (the circle fits inside the arena). Compute the share of the arena allowed, the mean number of tries, and the chance that all 20 tries fail.

    <details>
    <summary>Answer</summary>

    The circle covers `π × 180² = 101,788` of `600,000` square pixels, 16.96%. So `p = 1 − 0.1696 = 0.830`. Mean tries `1 / p = 1.20`. All 20 fail with chance `0.1696^20 ≈ 3.9 × 10⁻¹⁶`, which never happens in practice. A 20,000-call simulation gives a mean of 1.20 tries.

    </details>

60. **[13 · code · apply]** What do the two `print` lines show, and why? What does this tell you about sharing one generator between spawning and sparks?

    ```python
    import random
    a = random.Random(7)
    b = random.Random(7)
    b.random()
    xs = [a.randint(1, 100) for _ in range(3)]
    ys = [b.randint(1, 100) for _ in range(3)]
    print(xs == ys)
    c = random.Random(7)
    print(xs == [c.randint(1, 100) for _ in range(3)])
    ```

    <details>
    <summary>Answer</summary>

    It prints `False` then `True`. Same seed, same sequence, so `c` reproduces `xs` exactly. `b` made one extra call first, so its whole sequence is shifted. With Python 3.13 the values are `xs = [42, 20, 51]` and `ys = [20, 51, 84]`, the same numbers one position later.

    One extra call anywhere moves every later result. If sparks draw from the spawn generator, the number of sparks (or whether particles are switched on) moves every later spawn, and a seed from a bug report stops reproducing. Give gameplay its own generator.

    </details>

61. **[13 · compute · apply]** A spawn table has grunt 60, runner 30, brute 10. A designer adds elite with weight 20 and changes nothing else. What share of spawns is each type before and after? Did the designer mean to make brutes rarer?

    <details>
    <summary>Answer</summary>

    Before, the total is 100, so grunt 60%, runner 30%, brute 10%. After, the total is 120, so grunt 50%, runner 25%, brute 8.33% and elite 16.67%.

    Weights are relative, so adding an entry lowers every other entry's share. Brutes fell from 10% to 8.3% even though nobody touched their line. If the designer wanted brutes to stay at 10%, they must scale the other weights or state the table in percentages that sum to 100.

    </details>

62. **[13 · critique · apply]** A teammate's Fisher-Yates shuffle uses `j = rng.randint(0, i - 1)` instead of `rng.randint(0, i)`. Shuffle `["A", "B", "C"]` many times. Which of the six orders can appear? Why is this a bug for a bag randomizer?

    <details>
    <summary>Answer</summary>

    Only `BCA` and `CAB` appear. With `i − 1`, a slot can never swap with itself, so every item is always moved away from where it started. For three items only the two "rotations" have no item in its original place. A 60,000-shuffle run confirms it, while the correct version produces all six orders.

    In a 7-bag this means the piece at each position can never be the one the unshuffled list had there, so some deals never happen and a sharp player can learn what can't come next. The lecture's GDScript `shuffle_with` uses `randi_range(0, i)` for exactly this reason.

    </details>

## Week 14 · Polish pass: sound, particles, screen shake

Lecture: [w14-polish-pass-sound-particles-screen-shake.md](../lectures/w14-polish-pass-sound-particles-screen-shake.md)

63. **[14 · compute · apply]** A hit adds 0.7 trauma. Decay is 1.4 per second, the exponent is 2 and the maximum offset is 24 px. (a) What is the peak offset? (b) When does the camera stop shaking? (c) When does the shake drop below 1 px? (d) The camera already has trauma 0.3 when hits of 0.4 and 0.5 land in the same frame. With exponent 3, what is the shake after each hit?

    <details>
    <summary>Answer</summary>

    (a) `0.7² × 24 = 0.49 × 24 = 11.76` px.

    (b) Trauma falls linearly, so it reaches 0 at `0.7 / 1.4 = 0.5` s.

    (c) The offset is below 1 px when `24 × T² < 1`, that is `T < 0.204`. Trauma is `0.7 − 1.4t`, so `t > (0.7 − 0.204) / 1.4 = 0.354` s. Most of the visible shake happens in the first third of a second, the ease-out.

    (d) Before the hits the shake is `0.3³ = 0.027`. After 0.4: trauma 0.7, shake `0.343`. After 0.5: `min(1.2, 1) = 1.0`, shake 1.0, the full 24 px.

    </details>

64. **[14 · compute · apply]** The naive shake code subtracts a fixed `d / 60` per frame. A hit adds 0.6 with `d = 1.2`. How long does the shake last at 30, 60 and 144 fps with the bug, and with `d × dt`?

    <details>
    <summary>Answer</summary>

    With the bug, each frame removes `1.2 / 60 = 0.02`, so 0.6 lasts 30 frames at any rate. That is 1.0 s at 30 fps, 0.5 s at 60 fps and 0.21 s at 144 fps.

    With `d × dt`, trauma reaches 0 after `0.6 / 1.2 = 0.5` s at every rate (15 frames at 30 fps, 30 at 60, 72 at 144). The 144 Hz player with the bug gets less than half the shake the designer tuned.

    </details>

65. **[14 · code · apply]** (a) An emitter runs at 50 particles per second at 144 fps with the lecture's accumulator. How many particles are emitted in the first 10 frames, and what is left in `to_emit`? (b) A game has a thruster at 40 particles per second living 2 s, and death bursts of 30 sparks living 0.5 s at 4 kills per second. How many particles are alive on average, and what `amount` do you give the thruster's `GPUParticles2D` with `lifetime = 2`?

    ```python
    to_emit, emitted = 0.0, 0
    for frame in range(10):
        to_emit += 50 * (1 / 144)
        while to_emit >= 1.0:
            emitted += 1
            to_emit -= 1.0
    print(emitted, round(to_emit, 3))
    ```

    <details>
    <summary>Answer</summary>

    (a) It prints `3 0.472`. Each frame adds `50 / 144 = 0.347`. Ten frames add 3.47, three whole particles leave, and 0.47 carries into the next frame. Emitting one per frame instead would give 144 per second at 144 fps and 30 at 30 fps.

    (b) Alive is `rate × lifetime`. Thruster `40 × 2 = 80`. Sparks `30 × 4 = 120` per second, times 0.5 s, is 60. Total 140. Godot's `amount` is the number alive at once, so the thruster gets `amount = 80`, and the engine's rate `amount / lifetime = 40` per second follows.

    </details>

66. **[14 · compute · apply]** (a) What `pitch_scale` values give −3 and +3 semitones? (b) A sound is raised by 3 dB. By what factor does its amplitude change? (c) `AudioStreamRandomizer.random_pitch` is set to 1.12. About how many semitones of variation is that? Is it a good choice for a gun that fires ten times a second?

    <details>
    <summary>Answer</summary>

    (a) `2^(−3/12) = 0.841` and `2^(3/12) = 1.189`.

    (b) Amplitude scales by `10^(3/20) = 1.41`. (6 dB is about double, so 3 dB is about the square root of 2.)

    (c) `12 × log2(1.12) = 1.96`, about ±2 semitones, the lecture's "about ±2" figure. For a rapid-fire gun that is on the edge. The lecture suggests ±1 to ±2 semitones, and at ten shots a second a smaller range (±1, `random_pitch` about 1.06) keeps it sounding like one gun.

    </details>

## Integrated cases

67. **[9, 10 · compute · apply]** Your final game moves a 4 px bullet at 1,500 px/s with correct `delta`, and your thinnest wall is 16 px. Physics runs in `_physics_process` at Godot's default rate. (a) Can the bullet tunnel? (b) What is the lowest physics tick rate that makes it safe with no other change? (c) Why is a fixed tick rate a better place for this fix than raising the player's frame rate?

    <details>
    <summary>Answer</summary>

    (a) The default is 60 ticks per second, so the step is `1,500 / 60 = 25` px. That is above `t + s = 20`, so yes.

    (b) `1,500 / f ≤ 20` needs `f ≥ 75` ticks per second. At 75 Hz the step is exactly 20 px, which the lecture's condition `v / f > t + s` counts as safe. Many teams would pick 120 Hz for a margin, at twice the CPU cost of 60.

    (c) Collision runs once per physics tick, so the step size depends only on the tick rate. With a fixed tick rate the answer is the same on every machine. If the check ran in `_process`, a player at 30 fps would take 50 px steps no matter how fast your own machine is. Substeps or thicker walls are the other fixes from week 10.

    </details>

68. **[4, 5, 6 · code · apply]** Change the lecture's `add_item` so it takes the item database instead of a stack size, `add_item(inventory, item, count, db)`. With potions stacking to 16 and arrows to 64, what does it return, and what does the inventory hold, for `[("potion", 10), None, ("arrow", 60)]` after adding 20 potions and then 9 arrows? What should happen for the misspelt key `"potoin"`?

    <details>
    <summary>Answer</summary>

    Replace the parameter with one lookup at the top. The two passes are unchanged.

    ```python
    def add_item(inventory, item, count, db):
        stack_size = db[item]["stack"]
        # pass 1 and pass 2 exactly as in the week 5 lecture
    ```

    20 potions: pass 1 tops slot 0 up from 10 to 16 (6 moved, 14 left), pass 2 puts 14 in slot 1. Returns 0, inventory `[("potion", 16), ("potion", 14), ("arrow", 60)]`.

    9 arrows: pass 1 tops slot 2 up to 64 (4 moved, 5 left), no empty slot remains, so it returns 5.

    `"potoin"` raises `KeyError: 'potoin'` on the first line, before the inventory is touched. That is the behavior you want. Using `db.get(item, {}).get("stack", 1)` would quietly create a slot of a non-existent item.

    </details>

---

## Viva pattern

In each viva the assessor takes one or two **apply** questions and replaces the numbers with values from your project. You answer from your own code, with the project open. Three examples:

- From question 33: "Your jump has `C = 0.12` s and your character runs at 140 px/s. At 30 fps, what is the last frame a late jump works, and how far past the edge is the character? Show me the line that stores the window."
- From question 46: "Your fastest projectile is 6 px wide and moves at 1,100 px/s, and your thinnest wall is 12 px. Can it tunnel at your physics tick rate? Show me the numbers, then show me the wall in the editor."
- From question 49: "Here is your transition table. Which state and event pairs are ignored? Press the keys for two of them in the running game and show me that nothing happens."

A good viva answer names the model, puts your numbers into it, and points at the line of code that implements it.

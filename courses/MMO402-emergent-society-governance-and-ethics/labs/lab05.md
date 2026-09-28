# MMO402 · Lab 05: Terms-of-service audit

**Week:** 5 ([lecture](../lectures/w05-rules-eulas-and-terms-of-service.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish.
**Work mode:** pairs.
**Counts toward:** case analyses (30% of the course grade).

## Objective

Measure one live game's full legal stack, find where its key clauses sit, compute what a 51-second reader meets, and redesign the stack as a four-layer rule set (code, just-in-time notice, summary, full contract) so that every rule a reasonable player would be surprised by is met before it matters.

## Starter materials

**Your document stack.** Choose one game not used in the lecture (so not Blizzard or Riot). Collect every document a new player accepts or is pointed to at sign-up: EULA, terms of service, code of conduct or rules, privacy policy or notice, and any separate virtual-currency or purchase terms. Save each as plain text, and record its URL, its "last updated" date and the date you saved it.

**The model** (from the lecture):

```
T = W / R            required reading time, R = 250 words per minute
w = t × R            words covered; use t = 0.85 min (51 seconds)
coverage = min(1, w / W)
a clause at word x is met if x ≤ w (counting through the stack in order)
```

**Word and position counter.** Save this as `lab05_count.py` and run it with Python 3 (standard library only).

```python
import re
import sys

WORD = re.compile(r"[A-Za-z0-9][\w'’.-]*")

def count(path, patterns):
    text = open(path, encoding="utf-8").read()
    words = [m.start() for m in WORD.finditer(text)]
    print(f"{path}: {len(words)} words, {len(words) / 250:.1f} min at 250 wpm")
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if not m:
            print(f"  not found: {pat}")
            continue
        x = sum(1 for s in words if s < m.start())
        print(f"  {pat!r}: word {x} ({x / len(words):.1%} through)")

if __name__ == "__main__":
    count(sys.argv[1], sys.argv[2:])
```

Example: `python3 lab05_count.py tos.txt "arbitration" "virtual (items|currency|goods)" "terminat" "cheat|bot"`. The first match of each pattern is reported, so check that it is the clause itself and not a table of contents entry. If it is not, use a more specific phrase from the clause.

**Clause checklist.** Find each of these in your stack and record the document, the position `x` and a one-sentence paraphrase (no long quotations).

| # | Clause | Why a player would care |
|---|---|---|
| 1 | Licence versus ownership of the game and of virtual items | Whether items can be taken away or sold |
| 2 | Ban on selling items, currency or accounts for real money | The rule behind most bans in item-trading games |
| 3 | Ban on cheats, bots and exploits | What counts as `M` in week 4's test |
| 4 | Scamming and deception between players (allowed, banned or silent) | What counts as allowed play |
| 5 | Account suspension and termination, and what happens to purchases | What a ban costs the player |
| 6 | How the operator can change the terms, and how you are told | Whether version 1 still binds you |
| 7 | Dispute resolution: arbitration, class-action waiver, opt-out | Whether you can sue |
| 8 | Conduct outside the game (forums, voice, social media) that the rules cover | Where week 4's `T` test reaches |

## Steps

### Part A: measure (40 min)

1. Count each document and the whole stack. Record `W`, `T` and the 51-second coverage for each.
2. Locate clauses 1 to 8. Record `x` within its document and its position through the whole stack, reading the documents in the order the sign-up flow presents them.
3. Mark each clause "met" or "missed" for a 51-second reader and for a 10-minute reader.

### Part B: score (20 min)

4. Rate each clause on surprise: would a reasonable new player be surprised to learn it? Use 0 (no), 1 (somewhat) or 2 (yes). Write one sentence of reasoning per clause.
5. Compute the **surprise gap**, the number of clauses with surprise 2 that a 10-minute reader misses. The lecture's floor says this should be zero.

### Part C: redesign (at home)

6. Assign every clause to one of the four layers (code, just-in-time, summary, full contract). Each clause lives in the full contract; the question is which other layer it also needs.
7. Write at least three just-in-time notices, each at most 25 words, each naming the exact screen and moment it appears.
8. Write a summary of at most 200 words (it must fit inside a 51-second reading budget at 250 words per minute) that covers every clause with surprise 2.
9. Name one rule you would move into code instead of text, and describe the mechanic that enforces it.

## Deliverable

One PDF, named `lab05-<surname1>-<surname2>.pdf`, containing: the measurement table (Part A), the scored checklist with the surprise gap (Part B), the layer assignment, three or more notices, the 200-word summary and the code rule (Part C). Attach your plain-text copies of the documents and the counter's output.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Measurement | All documents counted, versions and dates recorded, positions correct within 2% | One document or date missing | Counts missing or unverifiable | 20% |
| Clause location | All eight clauses found or shown absent, paraphrased accurately | Six or seven found | Five or fewer | 20% |
| Surprise scoring and gap | Every score reasoned; gap computed correctly | Scores given with thin reasons | Missing | 15% |
| Just-in-time notices | Three or more, each at most 25 words, tied to a specific screen and moment, consistent with the contract | Notices vague about timing or too long | Fewer than two | 20% |
| Summary | At most 200 words, covers every surprise-2 clause, plain language, accurate | Over length or misses one clause | Missing or inaccurate | 15% |
| Code rule | A concrete mechanic that removes the need for a text rule, with its cost named | Mechanic named, cost missing | Missing | 10% |

<details>
<summary>Instructor check values</summary>

- Counter sanity check: for a text of exactly 12,800 words, the script prints 51.2 minutes; a pattern at the 137th word prints "word 137 (1.1% through)".
- For any stack, 51-second coverage is `212.5 / W`, so a 10,000-word document gives 2.1% and a 25,000-word stack gives 0.85%.
- A 10-minute reader covers 2,500 words. A stack in which the arbitration or item-ownership clause sits beyond word 2,500 and has no summary or notice has a surprise gap of at least 1.
- A 200-word summary is within the 212.5-word budget, so a 51-second reader who starts with it covers all of it.

</details>

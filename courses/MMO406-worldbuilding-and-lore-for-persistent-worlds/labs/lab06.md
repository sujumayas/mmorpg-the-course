# MMO406 · Lab 06: A pantheon, a ledger and four accounts

**Week:** 6, religion and myth in fiction ([lecture](../lectures/w06-religion-and-myth-in-fiction.md)).
**Time:** 2 hours in lab, plus about 4 hours at home (most of it writing).
**Weight:** part of the exercises (40%). The pantheon and myths become the religion chapter of your world bible.

## Objective

Implement the week 6 outcome model and an auditor for fact matrices. Then write a pantheon, a hidden canon ledger for one origin myth, and four in-world accounts of it, placed on a fact matrix that hits a target split of settled, answerable and unrecoverable facts. The auditor checks the matrix; your classmates check the writing.

## Starter materials

All in [`lab06-starter/`](lab06-starter/). Standard-library Python, run with `.venv/bin/python`.

- [`myth.py`](lab06-starter/myth.py) has the model and the matrix format in its docstring, finished `load_matrix` and `summary` helpers, and three empty functions: `outcomes`, `classify_row` and `audit`.
- [`sample_matrix.csv`](lab06-starter/sample_matrix.csv) is an eight-fact matrix for a flood myth told by four accounts. The fourth account is a translation of the third, so it repeats the third account's distortions.
- [`test_myth.py`](lab06-starter/test_myth.py) holds the test values. The lecture table at `p = 0.4`, `q = 0.2` for `k = 2, 3, 6`. The three shares always add to 1. Check-yourself question 1 (25%, 0%, 75%). Six hand-made rows covering every class, including a shared distortion label (false consensus). The sample matrix as written gives 2 settled, 2 answerable, 2 unrecoverable and 2 false consensus. With the translation removed it gives 2, 2, 4 and 0.
- The [interactive](../examples/w06-myth-triangulation.html), for choosing parameters before you write.

Run the tests from the repository root:

```
.venv/bin/python courses/MMO406-worldbuilding-and-lore-for-persistent-worlds/labs/lab06-starter/test_myth.py
```

On the starter all six tests report `TODO` and the script exits with status 1.

## Steps

1. **Model.** Implement `outcomes`. Check it against the lecture table with `myth.py`.
2. **Auditor.** Implement `classify_row` and `audit`. Run `myth.py` and explain in two sentences why removing the translation changes two false-consensus facts into unrecoverable ones rather than settled ones.
3. **Pantheon.** Write three to six gods. For each: domain, what they want, whom they favour, and their rung on the lecture's ladder of mechanical presence. Write one paragraph stating your answer to the active god problem and the rule it relies on.
4. **Ledger.** Write 12 to 16 core facts about one origin event, in plain sentences. Mark two or three as "must stay unrecoverable".
5. **Target and budget.** Choose a target split (for example 5 settled, 4 answerable, 4 unrecoverable of 13). Use `outcomes` or the interactive to find the `p` and `q` at `k = 4` whose expected split comes closest. Record how far chance would miss your target.
6. **Matrix.** Now author deliberately. Name four accounts (culture, institution, audience, motive). Fill a CSV in the sample's format that hits your target exactly under `audit`, with no false consensus unless you intend one and explain it. Every "must stay unrecoverable" fact must audit as unrecoverable.
7. **Accounts.** Write the four accounts, 250 to 400 words each, in four different in-world forms (for example a hymn, a scholar's summary, a children's rhyme, a heretic's letter). Each must read as a complete story on its own. Every distortion must serve its teller's motive.
8. **Peer reconstruction.** Give a classmate only the four accounts. They have 30 minutes to write down every fact they think is true. Score their list against your ledger and compare it with your audit: did they recover the settled facts, argue about the answerable ones, and miss the unrecoverable ones?

## Deliverable

`myth.py` with all tests passing; your matrix CSV; and a document of at most 2,500 words containing the pantheon, the active-god paragraph, the ledger with unrecoverable facts marked, the target and step 5 comparison, the audit output, the four accounts, and the peer-reconstruction results with a short paragraph on where the reader's reconstruction differed from the audit and why.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Model and auditor correctness | All six tests pass; step 2 explanation correct | Four or five pass | Three or fewer | 20% |
| Pantheon and active-god answer | Gods want things; rungs chosen and consistent; the active-god rule is specific and usable across expansions | Gods defined by domain only, or rule vague | Missing or generic | 20% |
| Ledger and matrix | Matrix hits the target exactly; protected facts unrecoverable; any false consensus is intended and explained | Target missed by one fact, or motives thin | Matrix missing or inconsistent with accounts | 20% |
| Accounts | Four distinct forms and voices; each stands alone; distortions serve motives; no long quotes from real scripture or game lore | Voices similar or one account weak | Accounts are summaries of the ledger | 25% |
| Peer reconstruction | Clean test; results compared with the audit; differences explained (for example, a reader trusting one voice) | Test run, comparison thin | No test | 15% |

<details>
<summary>Instructor check values</summary>

- `outcomes(4, 0.4, 0.2)` is about (0.282, 0.243, 0.475); `outcomes(6, 0.4, 0.2)` is (0.233472, 0.533248, 0.23328).
- Sample matrix as written: settled F01, F07; answerable F03, F05; unrecoverable F04, F08; false consensus F02, F06. With `codex_translation` removed, F02 and F06 become unrecoverable because the only remaining support is one true telling (F02) or none (F06). Neither becomes settled, because the false version was never evidence for the true one.
- Common bug: counting distinct distortion labels instead of checking for repeats, which misses false consensus. Another: `audit` deleting keys from the caller's rows; the last test catches it.
- In step 5, a target with at most 25% unrecoverable needs `p` of about 0.55 or more at `k = 4` (`U = 24.1%` at `p = 0.55`), whatever `q` is, since `U` depends only on `p`. Even at the best parameters, chance lands a random matrix a fact or two off the target in most draws, which is the lecture's argument for authoring the matrix deliberately.
- Check the accounts for copied real-world scripture or long passages of published game lore. Short allusions are fine; quotations beyond a phrase are not.

</details>

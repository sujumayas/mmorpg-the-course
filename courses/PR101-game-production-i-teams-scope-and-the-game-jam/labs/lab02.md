# PR101 · Lab 02: Branching drill and team repository

**Week:** 2, Git fundamentals and branching ([lecture](../lectures/w02-git-fundamentals-and-branching.md)).
**Time:** 2 hours in lab, plus up to 1 hour at home with your team.
**Weight:** part of the jam game component (30%), since the team repository you set up here is the one you jam in.

## Objective

Practice the everyday loop and a real conflict on a small game repository until a checker passes. Then set up your team's shared repository with the workflow from lecture section 4 and measure your team's merge interval against the overlap model.

## Starter materials

All in [`lab02-starter/`](lab02-starter/). Standard-library Python 3.10 or later and Git 2.28 or later.

- [`setup_lab02.py`](lab02-starter/setup_lab02.py) builds `lab02-repo/`, the config files of a small jam platformer called Slime Hop. It has three branches. `feature/hud` merges cleanly. `balance-pass` conflicts with a later commit on `main`. A `DECISIONS.md` file records what the designer decided. The repository also has a cache folder committed by mistake.
- [`check_lab02.py`](lab02-starter/check_lab02.py) runs 17 checks on the repository and prints PASS or FAIL for each. On a freshly built repository it prints `4/17 checks passed` and exits with code 1.
- The [interactive](../examples/w02-branch-collisions.html) for part B.

From the `labs/` folder:

```
python lab02-starter/setup_lab02.py
python lab02-starter/check_lab02.py lab02-repo
```

If you get stuck, `python lab02-starter/setup_lab02.py --force` rebuilds the repository from scratch.

## Steps

### Part A, the drill (75 min)

1. **Look before you touch.** `cd lab02-repo`, then run `git log --oneline --graph --all` and `git status`. Draw the commit graph on paper and label each branch. Set your own name and email in this repository with `git config user.name` and `git config user.email`.
2. **Clean merge.** Merge `feature/hud` into `main`. Confirm with `git log --graph` that `main` now contains the HUD commit.
3. **Conflict.** Merge `balance-pass` into `main`. Git stops on `game/enemy.cfg`. Before editing, read both sides, both commit messages (`git log -1 balance-pass`, `git log -2 main`) and `DECISIONS.md`. Resolve the file so it matches the recorded decision. Keep everything else the balance pass changed. Delete every marker line, stage the file and commit with a message that states the decision.
4. **Your feature.** Create a branch named `feature/<yourname>-doublejump` (lowercase, hyphens, for example `feature/ana-doublejump`). Add the line `double_jump = true` to `game/player.cfg`, commit, switch back to `main` and merge it.
5. **Fix the cache mistake.** Create a `.gitignore` with the line `.godot/`. Remove the cache folder from tracking, but not from disk, with `git rm -r --cached .godot`. Commit both changes.
6. **Tag.** Tag the tip of `main` as `v0.1`.
7. **Check.** Run the checker until it prints `17/17 checks passed`. Commit messages from you must start with a capital letter and an imperative verb ("Add", not "Added" or "Adding"), be at most 72 characters and not end with a full stop. The checker rejects "wip", "fix", "update" and "stuff" as first words. If a message is wrong, fix it with `git commit --amend` before it's merged, or make a new, well-named commit. Rewriting a merged commit's message isn't worth it in this lab.
8. **Adjacent lines.** In a scratch folder, repeat the lecture's two experiments: a two-line file where branches change line 1 and line 2, and a four-line file where branches change lines 1 and 4. Record which one conflicts.

### Part B, your team repository (45 min, with your team)

9. **Create the repository** on the hosting service your instructor specifies. Add every teammate. Protect `main` so changes arrive only through pull requests with one approval.
10. **Add the basics.** Commit a README with the game's working title and your lab 01 charter, and the engine-generated `.gitignore` (Godot 4: Project, Version Control, Generate Version Control Metadata).
11. **One PR each.** Each teammate opens a pull request from a short branch that adds their name to the README, and another teammate reviews and merges it. Four PRs, four reviewers.
12. **Your merge interval.** List the files your week 4 prototype will likely have, count `F` (files two people might both edit that week), and estimate `r` per person. In the interactive, find the longest merge interval that keeps P(any overlap) below 20% for your team of four. Write that interval into your charter as a rule.

## Deliverable

- The output of `check_lab02.py` showing `17/17 checks passed`, and the output of `git log --oneline --graph --all` from your `lab02-repo`.
- Your drawing from step 1 (a photo is fine) and one sentence from step 8 on which case conflicted and why.
- A link to your team repository showing four merged pull requests, each reviewed by someone other than its author.
- A short note of at most 200 words with your `F`, `r`, chosen merge interval and its overlap percentage from the interactive, and the rule as written in your charter.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Drill checker | 17/17 checks pass | 14-16 pass | 13 or fewer | 35% |
| Conflict resolution | Resolved to the recorded decision, balance-pass damage kept, merge message states the decision | Correct values, vague message | Wrong values or markers left | 15% |
| Graph and adjacent-lines note | Drawing matches the real graph; adjacent-line result explained in terms of how Git compares lines | Drawing close; explanation vague | Missing | 10% |
| Team repository | `main` protected, four PRs with reviews by someone other than the author, charter and `.gitignore` committed | Repository set up, some PRs self-merged | No shared repository | 25% |
| Merge-interval rule | `F`, `r` and interval justified with the model's numbers and written as a charter rule | Numbers given, rule vague | Missing | 15% |

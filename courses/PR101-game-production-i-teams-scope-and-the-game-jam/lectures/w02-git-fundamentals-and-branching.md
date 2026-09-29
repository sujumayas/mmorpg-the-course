# PR101 · Week 02 — Git Fundamentals and Branching

**Why this matters:** Every team in this course will lose work at least once. The question is whether you lose ten minutes or a weekend. Git turns "who overwrote my level?" into a two-minute fix, and a branching habit that merges early keeps those fixes rare.

**You will be able to:**
- Use the everyday Git loop (status, add, commit, switch, merge, push, pull) and explain what each command changes in the working tree, the staging area and the history.
- Resolve a merge conflict by reading the conflict markers and deciding, not guessing.
- Compute the chance that two branches touch the same file, as a function of files, edit rate and days apart, and use it to choose how often your team merges.
- Design a branching workflow for a four-person game team and justify each rule with the model.

**Before class:** Scott Chacon and Ben Straub, *Pro Git* (2nd ed., 2014, free online at git-scm.com/book), chapter 1 "Getting Started", chapter 2 "Git Basics" and sections 3.1 to 3.3 of "Git Branching" (about 60 short pages). Install Git and set your name and email (`git config --global user.name "..."`). Keith, *Agile Game Development* (2nd ed., 2020), the section on continuous integration.

**Prerequisites from earlier courses:** [PR101 week 1, roles on a game team](w01-roles-on-a-game-team.md) (the pair count `n(n − 1)/2`, which returns here). [CS101 week 12, debugging](../../CS101-programming-for-games-i/lectures/w12-debugging-breakpoints-logging-rubber-ducking.md) (bisecting, which `git bisect` automates over commits). [CS102 week 13, data-driven design](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w13-data-driven-design-stats-in-json-and-csv.md) (tuning data in text files, which merge well). MA102 is running alongside this course. Its [week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md), is the probability tool used in section 3.

**Interactive:** [examples/w02-branch-collisions.html](../examples/w02-branch-collisions.html). Keep it open during section 3.

---

## 1. What version control does for a team

A **version control system** records every saved state of a project, who made it and why, and lets several people change the project at once and combine their work. Git is the one you'll use. Linus Torvalds started writing it in April 2005, after the free license for BitKeeper, the tool the Linux kernel team had used since 2002, was withdrawn. Within weeks Git was managing kernel releases. Junio Hamano took over as maintainer in July 2005 and still maintains it.

You need six terms before anything else makes sense.

- A **repository** (repo) is the project folder plus its complete history, which Git stores in a hidden `.git` folder inside it.
- A **commit** is a saved snapshot of the whole project. It has an author, a message, and a pointer to the commit before it (its **parent**). Commits are named by a hash, a long hexadecimal string such as `41b1bd8...`. You'll usually see the first seven characters.
- The **working tree** is the files you see and edit.
- The **staging area** (also called the index) is the list of changes that will go into your next commit. You choose what goes in with `git add`. This lets you commit the player fix without also committing the half-finished menu you were playing with.
- A **branch** is a name that points at one commit and moves forward each time you commit on it. That's all it is. A branch is not a copy of the project. Creating one is instant.
- **HEAD** is Git's word for "the commit you're on right now", normally the tip of the branch you've switched to.

Two more for teamwork. A **remote** is another copy of the repository, usually on a server such as GitHub or GitLab, that the team shares. **Push** sends your commits to the remote. **Pull** fetches other people's commits and merges them into yours.

### Why games need it more than essays

A shared drive keeps the latest version of each file. Git keeps every version of every file, tied together into snapshots of the whole project. The difference shows the first time a build breaks. With a shared drive you ask around. With Git you run `git log`, find the last commit where the game started, and compare. CS101 week 12 showed that bisecting halves the search each step. `git bisect` does exactly that over your commit history, so finding the one bad commit among 1,000 takes about 10 test runs.

## 2. The everyday loop

Here is a whole session in a terminal. Run it in an empty folder. It uses `printf` to write files so it works the same on macOS, Linux and Git Bash on Windows.

```bash
mkdir jam-demo && cd jam-demo
git init -b main
git config user.name "Ana"
git config user.email "ana@example.com"
printf 'speed = 200\njump = 400\n' > player.cfg
git add player.cfg
git commit -m "Add player tuning file"
git switch -c feature/dash
printf 'speed = 260\njump = 400\n' > player.cfg
git commit -am "Raise run speed for dash feel"
git switch main
printf 'speed = 180\njump = 400\n' > player.cfg
git commit -am "Lower run speed after playtest"
git merge feature/dash
```

Line by line:

- `git init -b main` creates the repository with a first branch called `main`.
- `git add player.cfg` stages the new file. `git commit -m` saves the snapshot with a message.
- `git switch -c feature/dash` creates a branch called `feature/dash` and moves HEAD to it. Your files don't change, because both names point at the same commit.
- `git commit -am` stages every already-tracked file that changed and commits in one step.
- `git switch main` moves back. Git rewrites `player.cfg` to the version on `main`, `speed = 200`.
- Ana then changes the same line on `main` and commits.
- `git merge feature/dash` tries to combine the two lines of work.

The last command prints this:

```
Auto-merging player.cfg
CONFLICT (content): Merge conflict in player.cfg
Automatic merge failed; fix conflicts and then commit the result.
```

And `player.cfg` now reads:

```
<<<<<<< HEAD
speed = 180
=======
speed = 260
>>>>>>> feature/dash
jump = 400
```

### What a conflict is

Git merges line by line. If two branches changed different parts of a file, Git combines them without asking. If they changed the same lines, or lines right next to each other, Git can't know which one you want. It writes both between **conflict markers** and stops. Everything between `<<<<<<< HEAD` and `=======` is your current branch's version. Everything between `=======` and `>>>>>>> feature/dash` is the incoming branch's version.

The "right next to each other" part surprises people. In the two-line file above, if one branch changes `speed` and the other changes `jump`, Git still reports a conflict, because the two edits touch neighbouring lines. Put two untouched lines between them and Git merges cleanly. You can check both cases in the lab.

### Resolving it

A conflict is a decision Git hands back to a human. It is not an error. Resolve it in four steps.

1. **Read both sides and find out why each changed.** `git log -1 feature/dash` shows the message on the other side. Here, one person raised speed for dash feel and the other lowered it after a playtest. Both had reasons.
2. **Decide, with the owner.** Tuning numbers belong to the designer (week 1 RACI). Ask them. Say the answer is 220.
3. **Edit the file to the final state and delete all three marker lines.** A marker left in a config file will crash the game or, worse, load silently as garbage.
4. **Stage and commit.** The message should say what you decided.

```bash
printf 'speed = 220\njump = 400\n' > player.cfg
git add player.cfg
git commit -m "Merge feature/dash: settle speed at 220 after playtest"
git log --oneline --graph --all
```

The graph shows the shape of what happened (your hashes will differ):

```
*   6bcf6a0 Merge feature/dash: settle speed at 220 after playtest
|\
| * 41b1bd8 Raise run speed for dash feel
* | 449dc4a Lower run speed after playtest
|/
* 140a2aa Add player tuning file
```

The merge commit has two parents. That's how Git records that two lines of work joined.

### Commit messages that help

A commit message is written for the teammate who reads `git log` at 2 a.m. during the jam. Three rules:

- First line of 50 to 72 characters, written as a command: "Add double jump", not "added stuff" or "fixes".
- Say why when it isn't obvious: "Lower run speed after playtest" tells the reader a human decided it.
- One idea per commit. If your message needs "and", it's probably two commits. Small commits are easier to review, to revert and to bisect.

## 3. Worked example: why long-lived branches hurt

### The hook

In Unreal Engine, a level used to be one file. If you wanted to move a single lamp, you checked out the whole level, and Epic's documentation notes that this locked everyone else on the team out of that file until you were done. Unreal Engine 5 added **One File Per Actor**. Each object placed in the level is saved in its own small file, and the files are only packed back together when the game is cooked for release. Unity went the other way on the same problem. Its default is to save scenes as text, and it ships a merge tool (UnityYAMLMerge, also called Smart Merge) that understands scene and prefab files.

Why would an engine vendor split one level into thousands of files? Why would another build a special merge tool? Both are answers to one question. How likely is it that two people touch the same file before their work is combined, and what does it cost when they do?

### The model

Take a project with `F` files that people actually edit. Two people work on separate branches. Each touches `r` new files per day, and they merge after `d` days. So each branch touches `k = r × d` different files by merge time. Assume, for now, that files are picked at random.

The chance that the two branches share **no** file is the chance that the second person's `k` files all miss the first person's `k`:

```
P(no shared file) = C(F − k, k) / C(F, k)
P(overlap) = 1 − C(F − k, k) / C(F, k)
```

Here `C(a, b)` is "a choose b", the number of ways to pick `b` things from `a`. The "1 minus" step is the complement rule from MA102 week 3. It's easier to count the ways nothing collides.

For small `k`, a much simpler form is very close:

```
P(overlap) ≈ 1 − e^(−k² / F) = 1 − e^(−r² d² / F)
```

- `F` is the number of files people edit (not the number in the repository).
- `r` is new files touched per branch per day.
- `d` is days between merges.
- `k = r × d` is files touched per branch before the merge.

Look at the exponent. **Overlap risk grows with the square of the time between merges.** Double the branch lifetime and the exponent quadruples.

An overlap is not always a conflict. If both people edited different parts of a text file far apart, Git merges it without asking. But every overlap is a merge someone should look at. For binary files and single-file levels, every overlap is a conflict that Git cannot resolve at all. That's week 3.

### Numbers you can check

This code prints the table for `F = 200` and `r = 2`. Run it with `.venv/bin/python`.

```python
from math import comb, exp

def p_overlap(F, k):
    """Chance that two branches, each touching k different files
    chosen at random from F, share at least one file."""
    if 2 * k > F:
        return 1.0
    return 1 - comb(F - k, k) / comb(F, k)

F, r = 200, 2          # 200 files, each branch touches 2 new files a day
for d in [1, 2, 3, 5, 7, 10]:
    k = r * d
    exact = p_overlap(F, k)
    approx = 1 - exp(-k * k / F)
    print(f"d={d:2}  k={k:2}  exact={exact:6.1%}  approx={approx:6.1%}")
```

Output:

```
d= 1  k= 2  exact=  2.0%  approx=  2.0%
d= 2  k= 4  exact=  7.8%  approx=  7.7%
d= 3  k= 6  exact= 16.9%  approx= 16.5%
d= 5  k=10  exact= 40.9%  approx= 39.3%
d= 7  k=14  exact= 65.1%  approx= 62.5%
d=10  k=20  exact= 89.1%  approx= 86.5%
```

Merge daily and two people overlap 2% of the time. Merge weekly and it's 65%. Leave it ten days and it's close to certain. Going from 1 day to 3 days multiplies the risk by more than 8, because the exponent grows with `d²`.

Now hold the branch lifetime at 3 days (`k = 6`) and change `F`, the number of files the work is spread across.

| Files people edit, F | P(overlap) at k = 6 |
|---|---|
| 20 | 92.3% |
| 50 | 55.6% |
| 200 | 16.9% |
| 1,000 | 3.6% |

This is the Unreal hook in numbers. A level held in one file is `F = 1` for level work. Any two people editing the level collide, every time. Split it into a file per actor and a busy level becomes hundreds of files, and the risk collapses.

### More people, more pairs

Week 1's pair count comes back. With `m` people each on their own branch, there are `m(m − 1)/2` pairs, and any pair can overlap. Treating the pairs as independent (a close enough approximation at these sizes):

```
P(any overlap) ≈ 1 − (1 − p)^(m(m − 1)/2)
```

With `F = 200` and `r = 2`:

| People m | Pairs | Merge every 3 days (p = 16.9%) | Merge daily (p = 2.0%) |
|---|---|---|---|
| 2 | 1 | 16.9% | 2.0% |
| 3 | 3 | 42.6% | 5.9% |
| 4 | 6 | 67.1% | 11.4% |
| 6 | 15 | 93.8% | 26.1% |

A four-person jam team that merges every three days will hit an overlap two times in three. The same team merging daily sees one about once in nine merges.

### Watch it move

Open the interactive. The left view is a grid of `F` squares, one per file. Press "Simulate a sprint" and two colours fill in the files each branch touched. Any square in both colours flashes as an overlap. The right view plots P(overlap) against days between merges. Drag the days slider from 1 to 7. On the left, the grid looks only a little busier each day. On the right, the curve bends sharply upward. Then drag `F` from 200 down to 20 and watch the curve jump. Finally raise the number of people from 2 to 4 and watch the whole curve lift.

### The same idea in other places

**The birthday problem.** In a room of 23 people there's about a 50% chance two share a birthday. Rewrite it in our form. There are `F = 365` days, and among 23 people there are `23 × 22 / 2 = 253` pairs, each colliding with chance `1/365`. So `P ≈ 1 − e^(−253/365) ≈ 1 − e^(−0.693) = 50%`. Pairs times the chance per pair, in an exponent. It's the same shape, and it surprises people for the same reason. They count the people and forget to count the pairs.

**Unreal Engine 4 to 5.** A single level file forces `F = 1` for level work. Unreal's answer for binary level files was locking, where only one person may edit the file at a time (week 3 covers locking). One File Per Actor, added in UE5, attacks the model's other lever and raises `F` by giving every placed object its own file. Epic's documentation gives the reason directly: to stop one person's edit from locking the rest of the team out of the level.

**Unity (current, Unity 6).** Unity's Asset Serialization Mode defaults to Force Text, and its manual says the text format exists to help version control merges. It also ships UnityYAMLMerge for scene and prefab files. Unity is attacking the other side of the problem. It doesn't lower the chance of an overlap. It lowers the cost of one, by making overlaps mergeable.

**Godot 4.** Godot saves scenes as `.tscn` text files. Its documentation says the format is designed to be human-readable and easy for version control to manage. The editor can also generate a `.gitignore` for you, which leaves out the `.godot/` cache folder, as you'll see in section 4.

Four places, two levers. You can lower the chance of an overlap (merge sooner, spread work over more files) or lower the cost of one (text formats, smart merge tools). Every branching policy you'll ever read is a mix of the two.

### Design judgment

- **Merge at least daily.** The `d²` in the exponent makes this the cheapest lever. It costs a few minutes a day. Teams that do it almost never have a painful merge. This is the core of what people call **trunk-based development**. Everyone commits to one main line (the trunk) or to branches that live a day or two.
- **Split hot files on purpose.** If your whole game is one `Main` scene and one `Game.gd` script, your `F` is tiny and your team will collide constantly. Split scenes into sub-scenes, and scripts into one per object. The cost is more files to find your way around.
- **Random is the wrong assumption, in your favour.** Real work isn't random. If Ben owns movement code and Chen owns art, their files barely overlap, so the week 1 RACI is also a merge-conflict tool. The model's numbers are a worst case for a team with clear ownership, and a best case for a team where everyone touches `Game.gd`.
- **Long branches do have a use.** Stabilization is the main one. Epic's public Unreal Engine source keeps a `release` branch, which it describes as tested by QA and matching the current release, alongside a main branch where active development may not even compile. A branch that's meant to change slowly is fine. A feature branch that drifts for two weeks isn't.

## 4. A branching workflow for your team

Here is the workflow for PR101. It's deliberately simple. You'll adapt it after the jam post-mortem in week 9.

1. **`main` always builds and runs.** Anything merged into `main` must open in the engine and start the game. If `main` is broken, fixing it comes before everything else.
2. **One short branch per task.** Name it for the task: `feature/dash`, `fix/menu-crash`, `art/tileset-forest`. It lives two days at most. If the task is bigger, split the task (week 7 shows how).
3. **Update from `main` every day.** Run `git switch main`, `git pull`, `git switch feature/dash`, `git merge main`. Conflicts arrive one at a time, while they're small.
4. **Merge back through a pull request.** A **pull request** (PR, called a merge request on GitLab) is a request on the hosting site to merge your branch. It shows the diff and lets a teammate comment. One teammate reviews it, which takes five minutes for a small PR. The reviewer checks that it runs and that it contains nothing that shouldn't be there.
5. **Tag milestones.** `git tag v0.1-prototype` marks the commit you submitted. You'll always be able to rebuild exactly what the markers saw.
6. **Ignore what the engine regenerates.** A **`.gitignore`** file lists paths Git should never track. For Godot 4.1 and later, use the one the editor generates (Project, Version Control, Generate Version Control Metadata). It excludes the `.godot/` folder of cached imports. Committing cache folders bloats the repository and causes conflicts in files nobody edited by hand.

### When things go wrong

- **"I committed on `main` by accident."** If you haven't pushed, run `git switch -c feature/oops` to put a branch name on your work. Then `git switch main` and `git reset --hard origin/main` to move `main` back to the server's version. Your commits are safe on the new branch.
- **"I want to undo a commit that's already pushed."** Use `git revert <hash>`. It makes a new commit that undoes the old one without rewriting shared history. Never rewrite history that teammates have pulled.
- **"Git says my push was rejected."** Someone pushed first. `git pull`, resolve any conflicts, then push again.
- **"I don't know what state I'm in."** Run `git status`. It tells you your branch, what's staged, what's changed, and usually what to do next.

## In-class activity (25 minutes)

In your lab-1 teams, at one laptop.

1. **Ten minutes.** Run the section 2 session. Then repeat it with a four-line file (`speed`, `gravity`, `friction`, `jump`) where one branch changes `speed` and the other changes `jump`. Record which case conflicts and which merges cleanly.
2. **Ten minutes.** List the files your week 4 prototype will probably have. Count the ones two people might both edit in the same week. That's your `F`. Estimate `r` for each person. Use the interactive to find the merge interval that keeps P(any overlap) for your whole team below 20% per merge.
3. **Five minutes.** Write your team's three branch rules (naming, maximum lifetime, who reviews), each in one sentence, for your charter.

Expected output: the result of the two merge experiments, your `F`, `r`, team size and chosen interval with its overlap percentage, and three rules.

## Common misconceptions

- **"A branch is a copy of the project."** A branch is a name that points at a commit. Creating one copies nothing and takes no time. That's why branching often is cheap. Merging is where the cost lives.
- **"Conflicts mean somebody did something wrong."** A conflict means two people changed the same lines, and Git asks a human to decide. It's normal. What's avoidable is a huge conflict, and merging often avoids it.
- **"Git merges files, so if we edit different lines we're safe."** Edits to neighbouring lines still conflict. Binary files and single-file levels can't be merged at all (week 3).
- **"We'll merge everything at the end, it's quicker."** The overlap risk grows with the square of the days apart. Merging a week of four people's work at once is close to certain to collide, and all the collisions land in the final hours.

## Check yourself

1. Two artists share `F = 300` files. Each touches 3 new files a day. They merge every 4 days. Use the approximation to estimate P(overlap). What happens if they merge every 2 days instead?
2. In the `F = 200`, `r = 2` model, a team merges every 6 days. By roughly what factor does merging every 3 days cut the exponent? Use the exact function to compare the two probabilities.
3. A team of five merges daily with `p = 2%` per pair. Estimate P(any overlap) per merge. How many pairs are there?
4. Your teammate's merge leaves this in `enemy.cfg`: `<<<<<<< HEAD`, `hp = 50`, `=======`, `hp = 80`, `>>>>>>> balance-pass`. List the steps to resolve it correctly, including who you ask.
5. Why does One File Per Actor help more than merging more often for a team of level designers in UE5? Answer with the model's variables.

<details>
<summary>Answers</summary>

1. `k = 3 × 4 = 12`, so `P ≈ 1 − e^(−144/300) = 1 − e^(−0.48) ≈ 38%`. (The exact formula gives 39.3%.) Merging every 2 days makes `k = 6`, so `P ≈ 1 − e^(−36/300) = 1 − e^(−0.12) ≈ 11%`. Halving the interval cuts the exponent by 4.
2. `k` goes from 12 to 6, so `k²` goes from 144 to 36, a factor of 4. Exact: `p_overlap(200, 12) ≈ 53.4%` and `p_overlap(200, 6) ≈ 16.9%`.
3. Pairs `= 5 × 4 / 2 = 10`. `P ≈ 1 − 0.98^10 ≈ 1 − 0.817 ≈ 18%`.
4. Read both versions and the commit messages (`git log -1 balance-pass`) to find why each changed. Ask the owner of balance numbers (the designer, per your RACI) which value is right. Edit the file to the chosen value and delete all three marker lines. Run the game to check it loads. Then `git add enemy.cfg` and commit with a message that states the decision.
5. Level files are binary, and a single level is `F = 1` for level work. With `F = 1`, any two designers editing the level at once always collide, however short `d` is. There's nothing to merge more often, because only one person can hold the lock. OFPA raises `F` to roughly the number of placed actors, which drives `k² / F` toward zero.

</details>

## Lab / assignment hook

[Lab 02, branching drill](../labs/lab02.md). A setup script builds a small game repository with two feature branches, one of which conflicts. You merge both, resolve the conflict by the rule given, add a branch of your own, tag a milestone, and run a checker that fails until the repository is in the right state. Then you set up your team's shared repository with the workflow from section 4.

## Sources

- Wikipedia, "Git" (accessed September 2026). Development started April 2005 after the BitKeeper free license was revoked; self-hosting 7 April 2005; kernel 2.6.12 managed by 16 June 2005; maintenance passed to Junio Hamano on 26 July 2005; version 1.0 on 21 December 2005.
- Chacon, S. & Straub, B. (2014). *Pro Git* (2nd ed.). Apress. Free at git-scm.com/book. Commits, staging, branches as pointers, merging.
- Epic Games, "One File Per Actor in Unreal Engine" (Unreal Engine 5 documentation, 5.8 page, accessed September 2026). Actor data saved in external files; previously editing actors required checking out the whole level, locking out teammates; actors embedded back into levels when cooked.
- Epic Games, "Using Perforce as Source Control for Unreal Engine" (UE5 documentation, accessed September 2026). `.uasset` and `.umap` files are binary and cannot be text-merged; the editor locks (checks out) files being edited.
- Epic Games, "Downloading Source Code in Unreal Engine" (UE5 documentation, accessed September 2026). `release` branch tested by QA and matching the current release; main branch for active development that may not compile.
- Unity Technologies, Unity Manual, "Smart Merge" and "Editor settings" (Unity 6, 6000.x, accessed September 2026). UnityYAMLMerge merges scene and prefab files; Asset Serialization Mode defaults to Force Text to help version control merges.
- Godot Engine documentation, "TSCN file format" (4.7) and "Version control systems" (4.1 and later), accessed September 2026. Text scenes are designed for version control; the editor generates `.gitignore` and `.gitattributes`; exclude `.godot/`.
- Keith, C. (2020). *Agile Game Development* (2nd ed.). Addison-Wesley.

## Interactive spec: examples/w02-branch-collisions.html

**The one insight.** The chance that parallel branches touch the same file grows with the square of the time between merges. A grid that looks only slightly busier each day hides a curve that shoots up.

**Layout.** Two linked views, side by side on desktop, stacked on mobile.

1. **Left view, the file grid.** `F` squares in a near-square grid (for `F` up to 1,000, squares shrink; keep a minimum of 4 px). A "Simulate a sprint" button (also key `S`) draws, for each of `m` people, `k = r × d` distinct random files, using a seeded generator (seed shown, "New seed" button). Colour each person's files with a different palette colour and outline squares chosen by two or more people in a strong accent. Show "Overlaps this sprint: X files, Y pairs affected". A running tally below counts sprints with at least one overlap out of sprints simulated ("Observed: 7 of 20 sprints, 35%"), reset whenever a slider changes.
2. **Right view, the curve.** x-axis days between merges `d` from 1 to 14, y-axis P(any overlap) from 0 to 100%. Plot the exact curve (solid) and the approximation (dashed, lighter). Mark the current `d` with a dot and label its value. Overlay the observed frequency from the left view as a hollow dot with its sprint count.

**Controls** (keyboard operable, values shown).

- Files `F`: slider 1 to 1,000 (log-scaled), default 200. Preset buttons "One level file (F = 1)", "Small jam (F = 40)", "Split scenes (F = 1,000)".
- Files per day `r`: slider 1 to 5, step 1, default 2.
- Days between merges `d`: slider 1 to 14, step 1, default 3.
- People `m`: slider 2 to 6, step 1, default 2.

**Formulas.**

```
k = r × d
p(F, k) = 1 − C(F − k, k) / C(F, k)     (1 when 2k > F; compute with log-gamma or a running product to avoid overflow)
approx(F, k) = 1 − exp(−k² / F)
pairs = m (m − 1) / 2
P_any = 1 − (1 − p)^pairs               (label this "pairs treated as independent")
```

For the exact curve, `p` at `F = 1` and `k ≥ 1` is 1.

**Readout table** under the chart: `d`, `k`, `p` exact, `p` approx, pairs, `P_any`, for `d = 1, 2, 3, 5, 7, 10` at the current `F`, `r`, `m`.

**Test values** (must match the lecture).

- `F = 200`, `r = 2`, `m = 2`: exact `p` at `d = 1, 2, 3, 5, 7, 10` is 2.0%, 7.8%, 16.9%, 40.9%, 65.1%, 89.1%; approx 2.0%, 7.7%, 16.5%, 39.3%, 62.5%, 86.5%.
- `k = 6` (`r = 2`, `d = 3`), `m = 2`: `F = 20, 50, 200, 1,000` gives 92.3%, 55.6%, 16.9%, 3.6%.
- `F = 200`, `r = 2`, `d = 3`: `m = 3, 4, 6` gives 42.6%, 67.1%, 93.8%. With `d = 1`: 5.9%, 11.4%, 26.1%.
- `F = 300`, `r = 3`, `d = 4`, `m = 2`: exact 39.3%.

**Behaviour.** Everything updates on input. With reduced motion, overlaps are outlined without flashing. Colour is never the only signal: overlapped squares also carry a small "x" mark, and the tally is text. Colors from `templates/interactive-tokens.css`. Squares are plain; no file icons or engine logos.

# PR101 · Week 03 — Asset Workflows and Large Files (LFS)

**Why this matters:** Code is small text. Game art and audio are large binary files that Git was never designed for. Get the asset workflow wrong in week 3 and by week 12 a new teammate needs half an hour to clone the project, and two artists will have lost an afternoon each to a file nobody could merge. Get it right and nobody notices it exists.

**You will be able to:**
- Classify project files as source, export or derived, and decide for each whether it belongs in the repository, in LFS, or nowhere.
- Compute how a repository's clone size grows with binary asset saves, with and without Git LFS, and convert it to a download time.
- Compute the expected work lost to binary overlaps and explain why locking replaces merging for binary files.
- Set up LFS tracking, lockable patterns and a folder and naming convention for a team project.

**Before class:** The Git LFS project site (git-lfs.com) and its short tutorial page. *Pro Git* (2nd ed., 2014), section 10.2, "Git Objects", which explains why Git stores whole snapshots (about 10 pages). The Godot documentation page "Version control systems" (Godot 4.1 and later). Reread [AR101 week 14, pipeline](../../AR101-visual-foundations-for-games/lectures/w14-pipeline-export-atlases-import-settings.md) on export and import settings.

**Prerequisites from earlier courses:** [PR101 week 2, Git fundamentals and branching](w02-git-fundamentals-and-branching.md) (commits, merges and the overlap model, which you reuse in section 3). [AR101 week 14, pipeline, export and import settings](../../AR101-visual-foundations-for-games/lectures/w14-pipeline-export-atlases-import-settings.md) (what happens to an image between the paint program and the engine). [CS101 week 7, engine intro](../../CS101-programming-for-games-i/lectures/w07-engine-intro-scenes-nodes-scripts.md) (Godot scenes and resources).

**Interactive:** [examples/w03-repo-growth.html](../examples/w03-repo-growth.html). Keep it open during section 2.

---

## 1. Source, export, derived

Every asset in a game exists in up to three forms. Mixing them up causes most asset-pipeline trouble.

- **Source** is the file an artist or composer works in. It has layers, tracks, undo history and editable effects. Examples are a `.kra` or `.psd` painting, an `.aseprite` sprite with its animation tags, a `.blend` scene or a DAW project. Only the program that made it can open it properly, and it's often big.
- **Export** is what the source program writes for the game: a flat `.png`, a `.wav` or `.ogg`, a `.glb` model. The engine reads these.
- **Derived** (or imported, or cached) files are what the engine makes from the exports. Godot 4 keeps them in the project's `.godot/` folder. Unity keeps them in `Library/`. They're rebuilt automatically whenever an export changes.

Each form gets a different rule.

| Form | Example | In Git? | Why |
|---|---|---|---|
| Source | `hero.aseprite`, `theme.psd` | Yes, through LFS, marked lockable | You need it to change the art later, and nobody can merge two edits to it |
| Export | `hero.png`, `jump.wav` | Yes, through LFS | The game won't run without it |
| Derived | `.godot/imported/...` | No, list in `.gitignore` | Rebuilt on every machine; committing it causes conflicts in files nobody edited |
| Import settings | Godot's `hero.png.import` | Yes, as plain text | Small text files recording how the engine should import the export |

Godot's version control page lists only the `.godot/` folder and generated `*.translation` files as things to exclude. Everything else, including the small `.import` text files Godot writes next to each asset, is meant to be committed. You removed a committed cache folder in lab 2. This is why it mattered.

### Text or binary?

The second question for every file type is whether Git can merge it. A **text** file is lines of characters. Git can show a line-by-line **diff** (what changed) and merge edits to different lines, as you saw last week. A **binary** file is bytes with no line structure. Git can store it and tell you it changed, but it can't show what changed or merge two edits to it. Images, audio, models and most source-program files are binary. Godot `.tscn` scenes, `.tres` resources, config files and scripts are text.

Here's the rule to remember. **For text, an overlap is a merge. For binary, an overlap means one person's work is thrown away.**

## 2. Worked example: why the repository gets heavy

### The hook

GitHub warns you when you push a file larger than 50 MiB and refuses files larger than 100 MiB. Most game assets are well under that, so teams assume they're fine. Then the clone that took 20 seconds in week 2 takes half an hour in week 12.

Epic's own engine avoids this on purpose. The Unreal Engine source code is on GitHub, but the large binary content the engine needs is not in the Git history. After cloning, you run a setup script (`Setup.bat` on Windows) that downloads it separately. Epic's documentation notes that the first download takes a while, and later checkouts only fetch what changed. Why would a company that can afford any server keep its binaries out of Git?

### The model

Git stores the history of the whole project, and **a clone downloads all of it**. Every version of every file that was ever committed comes along. For code that's cheap, since text compresses well and Git stores small changes as small differences (deltas). For binaries it's different. When an artist re-saves a PNG or an OGG after a small edit, the file's compression usually spreads that change across the whole file. Git's delta compression then finds almost nothing to share between versions, so each version costs close to its full size.

Take `A` binary assets of average size `S`, and say each has been saved `v` times in total (its number of versions). Ignore the code, which is small next to the art.

```
Clone without LFS  ≈ A × S × v          every version of every asset
Clone with LFS     ≈ A × S + A × v × p  current version of each asset, plus a pointer per version
LFS server storage ≈ A × S × v          every version is still kept, on the LFS server
```

- `A` is the number of binary assets.
- `S` is the average asset size.
- `v` is the number of versions per asset.
- `p` is the size of one LFS pointer, about 130 bytes.

**Git LFS** (Large File Storage) is a Git extension that changes what goes into history. For every file matching a pattern you choose, Git commits a tiny **pointer file** instead of the content. The pointer records the file's hash and size. The real content goes to a separate LFS server, and your machine downloads only the versions you check out. A pointer looks like this:

```
version https://git-lfs.github.com/spec/v1
oid sha256:cc3b236fd7b5123f6ea8fcfd3c47d9f67efde143c86ffe1cf943d3580cbeb740
size 3000000
```

That's 132 bytes, standing in for a 3 MB file. The ratio between the two clone sizes is roughly `v`. **Without LFS, clone size grows with every save. With LFS, it tracks the current size of the project.**

### Numbers you can check

A semester project has 200 binary assets averaging 4 MB, 800 MB in total. On average each asset is re-saved once a week. A new teammate clones over a 50 Mbps connection. This code prints the clone size and time by week. Run it with `.venv/bin/python`.

```python
POINTER = 132            # bytes in one LFS pointer file for a 4 MB asset
A, S = 200, 4_000_000    # 200 binary assets of 4 MB each
MBPS = 50                # download speed in megabits per second

def clone_mb(versions, lfs):
    if lfs:   # history holds pointers; download only the current files
        total = A * versions * POINTER + A * S
    else:     # history holds every version of every file
        total = A * versions * S
    return total / 1e6

for week in [0, 2, 4, 8, 14]:
    v = week + 1                  # one re-save per asset per week
    git_mb, lfs_mb = clone_mb(v, False), clone_mb(v, True)
    print(f"week {week:2}: git {git_mb:7.0f} MB ({git_mb * 8 / MBPS / 60:4.1f} min)"
          f"   lfs {lfs_mb:5.0f} MB ({lfs_mb * 8 / MBPS / 60:4.1f} min)")
```

Output:

```
week  0: git     800 MB ( 2.1 min)   lfs   800 MB ( 2.1 min)
week  2: git    2400 MB ( 6.4 min)   lfs   800 MB ( 2.1 min)
week  4: git    4000 MB (10.7 min)   lfs   800 MB ( 2.1 min)
week  8: git    7200 MB (19.2 min)   lfs   800 MB ( 2.1 min)
week 14: git   12000 MB (32.0 min)   lfs   800 MB ( 2.1 min)
```

The same numbers as a table:

| Week | Versions v | Clone without LFS | Time at 50 Mbps | Clone with LFS | Time at 50 Mbps |
|---|---|---|---|---|---|
| 0 | 1 | 800 MB | 2.1 min | 800 MB | 2.1 min |
| 2 | 3 | 2,400 MB | 6.4 min | 800 MB | 2.1 min |
| 4 | 5 | 4,000 MB | 10.7 min | 800 MB | 2.1 min |
| 8 | 9 | 7,200 MB | 19.2 min | 800 MB | 2.1 min |
| 14 | 15 | 12,000 MB | 32.0 min | 800 MB | 2.1 min |

The pointers add `200 × 15 × 132` bytes, about 0.4 MB, by week 14. That's too small to show in the table.

Check one row by hand. At week 8 each asset has 9 versions, so `200 × 4 MB × 9 = 7,200 MB`. At 50 megabits per second that's `7,200 × 8 / 50 = 1,152` seconds, 19.2 minutes. Notice that nothing about the game got bigger. The project is still 800 MB of current art. Only its history grew.

### Is the delta claim true? Measure it

Don't take "binaries don't delta-compress" on trust. Lab 3 includes a script that commits six versions of a 2,000,000-byte (1,953 KiB) binary file, packs the repository with `git gc`, and measures it. When each version is completely re-randomized, standing in for a re-saved compressed file, the packed history is about 11,725 KiB, six full copies. When each version changes only 10 bytes in place, the pack is about 1,957 KiB, one copy plus tiny deltas. So Git does try. It just can't help when the whole file changes. A re-exported PNG with a small edit is much closer to the first case than the second.

### Watch it move

Open the interactive. The left view is a stacked bar showing what a new clone downloads today. The segments are code, current binaries, and old binary versions. The right view plots clone size against weeks, with three lines: plain Git, LFS clone, and LFS server storage. Drag the weeks slider to 14 with LFS off and watch the "old versions" segment swallow the bar. Turn LFS on. The bar drops to current files only, and the clone line goes flat, but the server-storage line keeps climbing exactly where plain Git was. Then raise saves per week to 3 and watch plain Git's line steepen while the LFS clone line doesn't move.

### The same idea in other places

**Unreal Engine source (UE5).** Epic keeps large binary dependencies out of the Git history and fetches them with a setup script, so a clone only brings the current binaries. That is LFS's idea done by hand. The history carries a small reference (the script and its manifest), and the content lives elsewhere and is downloaded at the version you need.

**Godot 4's `.godot/` folder.** Godot rebuilds imported assets from exports on each machine and keeps them in `.godot/`, which you don't commit. It's the model's lesson applied to derived files. If a file can be regenerated, keep its history out of the repository entirely. Its versions would count against `v` for no benefit.

**Unreal with Perforce.** Epic's documentation for using Perforce with Unreal notes that `.uasset` and `.umap` files are binary and can't be merged, so the editor checks out, which means locks, a file while you edit it. Perforce is a centralized version control system used widely by larger studios. A Perforce workspace syncs only the current version of each file, so it doesn't carry full history to every machine. The design choice is the same as LFS. Keep the full history on a server, and send each person only what they're working on.

**GitHub's limits.** The 50 MiB warning and 100 MiB block exist because every file in history is copied to every clone and to the host's own storage. The host is protecting itself from the `A × S × v` term.

Four systems, one idea. Keep history of binaries on a server and give each machine only the current versions. The alternative is that every clone pays for every save anyone ever made.

### Design judgment

- **Turn LFS on before the first binary commit.** Tracking patterns only affect new commits. If a PNG was already committed without LFS, its versions stay in history. The fix, `git lfs migrate import`, rewrites history, and every teammate must then re-clone. It's a one-command setup on day one and a painful afternoon in week 10.
- **LFS moves the cost; it doesn't remove it.** Server storage still grows as `A × S × v`. Hosting services meter LFS storage and download bandwidth separately from ordinary repository space, and each has its own free allowance. Check your host's current limits in week 3, not in week 13. Deleting old versions from an LFS server is awkward, so budget for them.
- **Everyone needs LFS installed.** A teammate without it clones pointer files instead of art, and the engine shows 132-byte "images" as broken. Put `git lfs install` in your README's setup steps.
- **Don't LFS what's small and textual.** Scripts, scenes, `.import` files and config stay in plain Git, where diffs and merges work. LFS files can't be diffed on the hosting site.
- **Consider leaving source files out.** Huge source files, such as a 2 GB audio session, may belong on a shared drive with a written naming rule, with only the exports in Git. That's a legitimate choice for a student team if you write down where they live.

## 3. Binary files can't merge, so lock them

Week 2's overlap model applies to binaries with one change. The cost of an overlap is no longer "someone reads a merge". It's "one person's edit is thrown away and redone".

Say two artists share `F = 30` binary files (the tileset, UI sheets, the hero sprite). Each opens `k = 3` of them per day. From week 2:

```
P(overlap per day) = 1 − C(27, 3) / C(30, 3) = 1 − 2,925 / 4,060 ≈ 28%
```

If each overlap costs the loser about 2 hours of redone work, that's `0.28 × 2 ≈ 0.56` hours a day, or roughly 2.8 hours in a five-day week, for one pair. With three artists there are three pairs, so about 8.4 hours a week, a full working day, thrown away.

**Locking** turns a thrown-away edit into a short wait. Before you open a binary file, you lock it. Nobody else can push changes to it until you unlock it. The overlap still happens, but the second person finds out before starting, not after finishing.

Git LFS supports this directly.

- Mark patterns as lockable, for example `git lfs track --lockable "*.psd"`. By default, LFS then makes those files read-only in your working copy until you lock them, so you can't start editing by accident.
- `git lfs lock art/hero.psd` takes the lock, and the LFS server records who holds it.
- `git lfs locks` lists who holds what.
- `git lfs unlock art/hero.psd` releases it after you push.

Locking needs a hosting service whose LFS server supports the locking API. Check yours in the lab before you rely on it. It also needs a team habit: **lock before you open, unlock after you push.** A lock someone forgets to release over a weekend blocks everyone else. Put "who may break a stale lock" in your charter. Usually it's the file's A in the RACI, after a message to the holder.

Unreal's Perforce setup does the same thing under another name, where the editor checks out (locks) a binary asset when you begin editing it. One File Per Actor, from week 2, is Epic's way of making the locked units smaller, so that fewer people ever want the same one.

## 4. Setting up LFS for your team

Run this once, in a fresh repository, before anyone commits an asset.

```bash
git lfs install --local
git lfs track "*.png" "*.wav" "*.ogg"
git lfs track --lockable "*.psd"
cat .gitattributes
```

The last command shows what `track` wrote:

```
*.png filter=lfs diff=lfs merge=lfs -text
*.wav filter=lfs diff=lfs merge=lfs -text
*.ogg filter=lfs diff=lfs merge=lfs -text
*.psd filter=lfs diff=lfs merge=lfs -text lockable
```

The `.gitattributes` file is how Git knows which paths go through LFS. Commit it first, on its own, before any asset. Add patterns for whatever your team's tools produce, such as `*.aseprite`, `*.kra`, `*.blend`, `*.glb` and `*.ttf`.

To check that an asset really went through LFS after committing it, run `git lfs ls-files`. It lists every LFS-tracked file in the current commit. Or run `git show HEAD:path/to/file.png`. If LFS worked, you'll see the three-line pointer, not binary noise.

If you use Godot 4, the editor's "Generate Version Control Metadata" command also writes a `.gitattributes`. Open it, keep what it has, and add your LFS lines.

## 5. Conventions that keep assets findable

A tool doesn't fix a messy folder. Agree on these on day one and write them in your README.

- **Folders by feature, then type.** `characters/hero/hero.png`, `characters/hero/hero_jump.wav`, `levels/forest/forest_tiles.png`. Someone working on the hero finds everything in one place, and two people working on different features rarely share a folder, which lowers overlaps (week 2's "random is the wrong assumption").
- **Names without spaces or capitals, and no version numbers.** Use `hero_idle.png`, not `Hero Idle FINAL v3.png`. Git is the version history, so a `v3` in a file name means the history is being kept in two places.
- **One owner per asset.** The RACI from week 1 names who is A for each asset set. The owner decides on overlaps and breaks stale locks.
- **Export settings written down.** "Sprites export at 1× as PNG, 32 px per tile, no premultiplied alpha." AR101 week 14 covers why each setting matters. Here the point is that a teammate can re-export your file identically when you're asleep.
- **A placeholder rule.** Placeholder art uses the final file name and size, so replacing it is a file swap with no code change. During a jam this is how art and code proceed in parallel.

## In-class activity (25 minutes)

In your teams.

1. **Ten minutes.** List every file type your week 4 prototype will create. Classify each as source, export, derived or import settings. For each, decide plain Git, LFS, LFS lockable, or `.gitignore`. Write your `.gitattributes` and `.gitignore` on paper.
2. **Ten minutes.** Estimate your project at week 14: number of binary assets `A`, average size `S`, saves per week. Use the interactive to find the clone size with and without LFS, and the LFS server storage. Look up your host's LFS allowance and compare.
3. **Five minutes.** Estimate `F` and `k` for your shared binary files and compute P(overlap) per day with the week 2 formula. Decide which patterns must be lockable.

Expected output: your two files written out, the three sizes for week 14, the host allowance, and your lockable list with the overlap number behind it.

## Common misconceptions

- **"Git only stores the latest version, so big files cost once."** Git stores every committed version, and a clone downloads all of them. For binaries that don't delta-compress, each save adds close to the full file size.
- **"LFS makes big files free."** LFS keeps them out of the clone, not off the server. Server storage still grows with every save and counts against your host's LFS allowance.
- **"I'll turn on LFS later if the repo gets big."** Patterns only affect new commits. Moving old commits into LFS rewrites history and forces everyone to re-clone.
- **"Locking is for big studios."** Locking pays off as soon as two people might open the same binary file in a week. The section 3 numbers show a full day per week lost for three artists without it.

## Check yourself

1. A jam team has 60 binary assets averaging 1.5 MB. Over the weekend each is saved 6 times after the first commit. How large is a fresh clone at the end without LFS and with LFS? How long does each take on 10 Mbps venue Wi-Fi?
2. Your semester project is at 5 versions per asset with 1 GB of current binaries and no LFS. A teammate joins at week 8, when there are 9 versions per asset. How much does their clone download, and how much would a new clone download with LFS set up from day one?
3. Two artists share 20 binary files and each opens 4 per day. Compute P(overlap) per day. If an overlap costs 3 hours of redone work, what's the expected loss per 5-day week?
4. A teammate clones the repository and reports that every sprite in Godot is broken and each PNG is 132 bytes. What happened, and what's the fix?
5. Classify these and say where each goes. `boss_theme.ogg`, `.godot/imported/boss.png-3f2a.ctex`, `boss.png.import`, `boss.kra`, `boss.tscn`.

<details>
<summary>Answers</summary>

1. Versions `v = 7`. Without LFS, `60 × 1.5 × 7 = 630 MB`, which takes `630 × 8 / 10 = 504` seconds, 8.4 minutes. With LFS, `60 × 1.5 = 90 MB` (plus about 55 KB of pointers), which takes 72 seconds.
2. Without LFS, `1 GB × 9 = 9 GB`. With LFS from day one, about 1 GB of current files plus pointers. The earlier number (5 versions) doesn't matter. The clone pays for the history at the time of cloning.
3. `P = 1 − C(16, 4) / C(20, 4) = 1 − 1,820 / 4,845 ≈ 62%` per day. Expected loss `0.62 × 3 ≈ 1.9` hours a day, about 9.4 hours in a 5-day week for this pair. Make these patterns lockable.
4. They cloned without Git LFS installed, so they got the pointer files instead of the content. Install LFS (`git lfs install`), then run `git lfs pull` in the repository to download the real files. Add the install step to the README.
5. `boss_theme.ogg` is an export, in LFS. The `.ctex` file under `.godot/imported/` is derived and belongs in `.gitignore` (the whole `.godot/` folder). `boss.png.import` is import settings, plain Git. `boss.kra` is source, LFS and lockable. `boss.tscn` is a text scene, plain Git.

</details>

## Lab / assignment hook

[Lab 03, asset pipeline and LFS](../labs/lab03.md). Part A has you implement the clone-size model in Python until the tests pass, then measure real Git packs with a provided script. Part B has you repair a practice repository where binaries were committed without LFS, by migrating history, adding lockable patterns and passing a checker. You then apply the setup to your team repository.

## Sources

- GitHub Docs, "About large files on GitHub" (accessed September 2026). Warning for files larger than 50 MiB; files larger than 100 MiB blocked; 25 MiB browser upload limit.
- Git LFS, "Git LFS Specification" (`docs/spec.md` in the git-lfs repository, accessed September 2026). Pointer file format with `version`, `oid sha256:` and `size` lines, under 1,024 bytes. Pointer size of 132 bytes measured with git-lfs 3.7.1 for a 3,000,000-byte file.
- Git LFS manual pages `git-lfs-lock` and `git-lfs-config` (accessed September 2026). Locks recorded on the LFS server and checked on push; `lfs.setlockablereadonly` makes lockable files read-only unless locked by the current user, on by default.
- Epic Games, "Downloading Source Code in Unreal Engine" (UE5 documentation, accessed September 2026). Setup script downloads engine binary content after cloning; later checkouts are incremental.
- Epic Games, "Using Perforce as Source Control for Unreal Engine" (UE5 documentation, accessed September 2026). `.uasset` and `.umap` are binary and cannot be text-merged; the editor checks out (locks) files being edited.
- Unity Manual, "Importing assets" (Unity 6.0, accessed September 2026). Unity stores imported asset data in `Library/`, which behaves like a cache, need not be under version control and can be regenerated from `Assets` and `ProjectSettings`.
- Perforce, P4 Command Reference, "p4 sync" (current Helix Core documentation, accessed September 2026). `p4 sync` copies files from the depot into the workspace at the head revision unless another revision is named; the history stays on the server.
- Godot Engine documentation, "Version control systems" (Godot 4.1 and later, accessed September 2026). Exclude `.godot/` and generated `*.translation` files; the editor generates `.gitignore` and `.gitattributes`.
- Chacon, S. & Straub, B. (2014). *Pro Git* (2nd ed.). Apress. Section 10.2 on Git objects and 10.4 on packfiles and deltas.
- Pack-size measurements in section 2 made by the author with Git 2.50.1 and the lab 3 script (six versions of a 2,000,000-byte file, `git gc --aggressive`).

## Interactive spec: examples/w03-repo-growth.html

**The one insight.** Without LFS, clone size grows with every save of every binary. With LFS, the clone tracks the current project size, while server storage keeps growing as before.

**Layout.** Two linked views, side by side on desktop, stacked on mobile.

1. **Left view, "What a new clone downloads today".** One horizontal stacked bar with three segments: code (constant), current binaries (`A × S`), and old binary versions (`A × S × (v − 1)` without LFS; pointer bytes `A × v × 132` with LFS, which renders as a sliver). Label each segment with its size in MB and the total with its download time.
2. **Right view, "Size over the project".** x-axis weeks 0 to 30, y-axis MB. Three lines: plain Git clone, LFS clone, LFS server storage (dashed). Mark the current week with a vertical line and label the three values there.

**Controls** (keyboard operable, values shown).

- Binary assets `A`: slider 10 to 2,000, default 200.
- Average asset size `S`: slider 0.1 to 50 MB, default 4.
- Saves per asset per week: slider 0 to 5, step 0.5, default 1.
- Weeks: slider 0 to 30, default 14.
- Code history: slider 0 to 500 MB, default 0.
- Download speed: slider 5 to 1,000 Mbps (log-scaled), default 50.
- LFS toggle, default off. Presets "Semester project (200, 4 MB, 1/week)" and "Jam weekend (60, 1.5 MB, 6 saves total, 10 Mbps)".

**Formulas.**

```
v = 1 + saves_per_week × weeks          (jam preset: v = 7, shown with "weeks" relabelled as "saves so far")
git_clone   = code + A × S × v
lfs_clone   = code + A × S + A × v × 132 bytes
lfs_server  = A × S × v
minutes     = MB × 8 / Mbps / 60
```

Use decimal MB (1 MB = 1,000,000 bytes) throughout, matching the lecture.

**Readout table** under the chart: week, v, plain Git clone (MB, minutes), LFS clone (MB, minutes), LFS server (MB), for weeks 0, 2, 4, 8, 14 at current settings.

**Test values** (must match the lecture).

- A 200, S 4 MB, 1 save/week, 50 Mbps, code 0: weeks 0, 2, 4, 8, 14 give plain Git 800, 2,400, 4,000, 7,200, 12,000 MB (2.1, 6.4, 10.7, 19.2, 32.0 min). LFS clone 800 MB (2.1 min) at every week, plus 0.03 to 0.40 MB of pointers. LFS server equals the plain Git numbers.
- Jam preset: A 60, S 1.5 MB, v 7, 10 Mbps: plain Git 630 MB (8.4 min), LFS clone 90 MB plus 0.06 MB pointers (1.2 min).

**Behaviour.** The LFS toggle animates the old-versions segment shrinking (instant with reduced motion). A short caption under the left bar states the ratio "plain Git downloads X times more than LFS". Colors from `templates/interactive-tokens.css`. No file icons or engine logos; segments are plain blocks with text labels.

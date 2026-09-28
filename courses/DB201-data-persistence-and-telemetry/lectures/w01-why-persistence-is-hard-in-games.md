# DB201 · Week 01 — Why Persistence Is Hard in Games

**Why this matters:** Every game that remembers anything has to decide how much a crash is allowed to erase. Get it wrong one way and players lose an hour of loot. Get it wrong the other way and your database spends its whole budget saving player positions nobody will miss. This week gives you the model that makes that decision a number instead of a guess.

**You will be able to:**
- Compute the write rate, byte rate and expected progress lost for a periodic save policy, given players online, state size and save interval.
- Explain why halving the progress lost doubles the write load, and design a hybrid policy that escapes the trade-off for the state players care about.
- Write a save routine that survives a crash at any byte, and explain why overwriting a file in place does not.
- Name the four problems that make game persistence harder than saving a document, and say which week of this course handles each.

**Before class:** Kleppmann, *Designing Data-Intensive Applications* (2017), chapter 7, the opening section "The Slippery Concept of a Transaction" up to and including "The Meaning of ACID" (read durability closely). The SQLite documentation page "Atomic Commit In SQLite", sections 1 to 3 (sqlite.org/atomiccommit.html).

**Prerequisites from earlier courses:** Serializing game data to JSON and loading it into objects, [CS102 week 13, data-driven design](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w13-data-driven-design-stats-in-json-and-csv.md). Counting costs by growth rate, [CS102 week 4, Big-O intuition](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w04-big-o-intuition-for-game-developers.md). Expected value of a uniform quantity, [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md). Stocks and flows, which is how you should picture a player's progress between saves, [GD102 week 2](../../GD102-systems-design-and-game-mechanics/lectures/w02-stocks-and-flows.md).

**Interactive:** [Save interval trade-off](../examples/w01-save-interval-tradeoff.html). Keep it open during section 2.

---

## 1. What "persistent" means in a game

A running game keeps its state in memory. Memory is fast and it is volatile, which means its contents vanish when the process stops, the machine loses power, or the operating system kills the program. **Persistence** is the job of copying the state that matters onto storage that survives those events (a disk, usually through a database) and reading it back later.

Not all state is equal. It helps to sort a game's data into four kinds before you decide how to store any of it.

| Kind | Example | Who changes it | How often | Cost of losing it |
|---|---|---|---|---|
| Content data | item definitions, quest text, drop tables | designers, at build or patch time | weekly | none, it ships with the game |
| Player state | level, gold, inventory, quest progress | the player, through play | many times a minute | high, players remember |
| World state | a farm's crops, a guild hall, a player-run market | many players and the simulation | constantly | high, and shared |
| Records | logs, telemetry, purchase receipts | the server | constantly | varies, receipts are legal records |

Content data is what CS102 week 13 loaded from CSV and JSON. It is read-only while the game runs, so persisting it is easy: ship the file. This course is about the other three rows. Player and world state are the "save game" problem. Records are the telemetry problem of weeks 10 to 12.

Two words you will use all semester:

- **Durable** means a change survives a crash once the system has told you it succeeded. If the server says "trade complete" and then loses power, a durable system still has the trade after reboot.
- **Consistent** (in the everyday sense, which week 5 will sharpen) means the saved state is one the game could actually have been in. A save where the sword left your inventory but never arrived in your friend's is durable and wrong.

A save file is a snapshot. The game changes every frame; the snapshot is frozen at one moment. Everything that happens between two snapshots lives only in memory, and that gap is where crashes do their damage.

## 2. Worked example: how much can a crash erase?

### The hook

Stardew Valley saves your game at exactly one moment: when the in-game day ends, because you went to bed, collapsed from exhaustion, or stayed up until 2 a.m. Quit in the middle of the day and everything you did since waking is gone. A full in-game day runs from 6 a.m. to 2 a.m. and takes about 14 minutes of real time, at 0.7 real seconds per in-game minute. So a crash at 1:50 a.m. erases almost 14 minutes of fishing, and players who lose a good day to a power cut remember it.

Why would a shipped, much-loved game accept that? Why not save every minute? The answer is a model that applies to every game you will ever persist, from a farming sim to an MMO shard.

### The model

Picture a server with players online, each with a saved state of some size. The server writes every player's state to the database once per save interval. Name the symbols:

- `N` is the number of players online.
- `S` is the size of one player's saved state, in bytes.
- `T` is the save interval, in seconds.

Then:

```
saves per second   W = N / T
bytes per second   B = N × S / T
worst loss         = T                 (crash just before a save)
average loss       = T / 2             (crash lands anywhere in the interval)
player-time lost   = N × T / 2         (summed over everyone online, per crash)
```

The average-loss line comes from MA102 week 4. A crash has no reason to prefer any moment within the interval, so the time since the last save is uniform between 0 and `T`, and a uniform quantity's expected value is its midpoint.

Now multiply the write rate by the average loss:

```
W × (T / 2) = (N / T) × (T / 2) = N / 2
```

The save interval cancels. **For a fixed number of players, write rate times average loss is a constant.** Halve the progress a crash can erase and you double the writes your database must absorb. Cut loss by ten and you pay ten times the writes. There is no clever choice of `T` that gets both down. The curve relating them is a hyperbola, and every periodic save policy sits somewhere on it.

### Numbers you can check

Take a mid-sized shard: `N = 4,000` players, each with a 24 kB saved state (`S = 24,000` bytes, a reasonable size for a JSON character with a few hundred inventory slots). Compute each row by hand with the formulas above.

| Save interval T | Saves/s W | Write volume B | Average loss | Player-hours lost per crash |
|---|---|---|---|---|
| 1 s | 4,000 | 96 MB/s | 0.5 s | 0.56 |
| 10 s | 400 | 9.6 MB/s | 5 s | 5.6 |
| 60 s | 66.7 | 1.6 MB/s | 30 s | 33.3 |
| 300 s (5 min) | 13.3 | 320 kB/s | 150 s | 166.7 |
| 840 s (one Stardew day) | 4.8 | 114 kB/s | 420 s | 466.7 |

Check the constant. In every row, `W × average loss = 2,000`, which is `N / 2`. For the 60 s row, `66.7 × 30 = 2,000`.

Check one row in full. At `T = 300`, `W = 4,000 / 300 = 13.3` saves per second. `B = 13.3 × 24,000 = 320,000` bytes per second. A crash erases on average 150 seconds per player, and `4,000 × 150 / 3,600 = 166.7` player-hours in total.

Two readings of this table matter. At the top, one-second saves would ask the database for 4,000 durable writes per second from a single shard. That is a heavy load for one database server, and it would be spent mostly on state that barely changed. At the bottom, the Stardew row costs almost nothing, but one crash erases 467 player-hours. A single-player game can live with that because each crash hurts one player. A shard cannot.

### Seeing it move

Open the interactive. The top view is one player's timeline over an hour: save ticks as vertical marks and progress accumulating as a rising line. Drag the crash marker and the shaded area shows what that crash erases. The bottom view plots write rate against average loss on log axes. Drag the save-interval slider and the point slides along the hyperbola. It never leaves the curve, however you set `T`.

Then switch on "save on valuable events." A second point appears that sits below the curve. The next subsection explains how.

### Breaking the curve: not all progress is equal

The model treated all progress as interchangeable, one second of play is one second of loss. Players do not see it that way. Losing 150 seconds of walking is an annoyance. Losing the legendary drop you got 100 seconds ago, or a trade where you already handed over your gold, is a support ticket.

So split the state:

- **Cheap state** changes constantly and is easy to redo: position, facing, mana, the XP from the last few kills. Save it periodically.
- **Valuable state** changes rarely and hurts to lose: rare drops, trades, purchases with real money, quest completions. Save it the moment it changes, as a small write of just that change, before telling the player it succeeded.

Model the hybrid with one more symbol, `e`, the number of valuable events per player per hour:

```
hybrid writes per second = N / T + N × e / 3,600
```

With `T = 300` and `e = 12` (one valuable event every five minutes, a generous figure):

```
4,000 / 300 + 4,000 × 12 / 3,600 = 13.3 + 13.3 = 26.7 writes per second
```

Compare that with `T = 10` for everything, which also keeps loss low: 400 writes per second. The hybrid does **15 times fewer writes**, and for valuable state its loss is zero, not five seconds. Cheap state still loses 150 seconds on average, which is the point: you chose to lose it.

| Policy | Writes/s | Avg loss, cheap state | Avg loss, valuable state |
|---|---|---|---|
| Periodic, T = 300 s | 13.3 | 150 s | 150 s |
| Periodic, T = 10 s | 400 | 5 s | 5 s |
| Hybrid, T = 300 s, e = 12/h | 26.7 | 150 s | 0 |

The event writes are also small. A trade record might be 2 kB against a 24 kB full character, so the byte rate goes up by only `13.3 × 2,000 = 26.7 kB/s`.

### Cross-game recognition

The same trade-off appears everywhere once you know to look for `T`.

**Stardew Valley (1.x).** `T` is one in-game day, about 840 seconds of play. The game gets something in return for that long interval. Night is a natural boundary where no action is half finished, crops grow and shipped items are sold, so the save is always a state the game could really be in. In multiplayer, the day ends only when every player goes to bed, and the host's machine keeps the save file. The long `T` buys a clean, consistent snapshot.

**Minecraft (Java Edition).** The game autosaves every 6,000 ticks, which is 5 minutes, and also whenever the player opens the pause menu. That is `T = 300` plus an event trigger: pausing is the moment a player is most likely to quit, so the game saves exactly then. The world is split into region files of 32 × 32 chunks, and each region file keeps a table of when each chunk was last updated. Only changed chunks need writing. That is the byte-rate half of the model: shrink `S` to what changed, not the whole world.

**PostgreSQL itself.** Databases face the same choice internally. With the default setting `synchronous_commit = on`, a commit waits until its log record is flushed to disk, so a committed change is durable. Turn it off and commits return sooner, at the risk of losing the most recent ones in a crash. The documentation bounds that window at three times `wal_writer_delay`, which defaults to 200 ms, so up to 600 ms. The risk is data loss, not corruption: the database recovers to a consistent earlier state. And the setting can change per transaction. A server can commit position updates asynchronously and trades synchronously, which is the hybrid policy built into the database.

Three contexts, one model: an interval `T` that sets both the loss and the write rate, and an event trigger for the moments that matter.

### Eyes-open design judgment

- **Pick `T` from the cost of loss, not from habit.** Ask what a player loses in `T / 2` seconds of your game. In a fast looter that may be several rare drops. In a farming sim it may be one watered field.
- **Decide which state is valuable, on paper, before writing code.** The list drives the event triggers. Anything involving another player (trades, mail, guild banks) or real money belongs on it, because a loss there creates a second victim or a refund.
- **A natural boundary can be worth a long `T`.** Stardew's end-of-day save is consistent by construction. Saving mid-action risks a snapshot where a fish is half caught. You will spend weeks 5 and 6 learning to get that consistency without waiting for night.
- **Event saves shift the risk, they do not remove it.** If the valuable write succeeds but the periodic save of the rest is 150 seconds old, a crash can restore a character who has the new sword but not the XP from the kill that dropped it. Usually fine. Occasionally it creates a state a designer never imagined, so test it.
- **Tell players the truth.** If you save at the end of the day, say so. Stardew's players tolerate lost days because the rule is simple and visible.

### Check yourself on the worked example

1. A shard of 10,000 players saves a 30 kB state every 120 seconds. What are `W`, `B`, and the player-hours lost per crash?
2. A designer wants average loss under 20 seconds for everything on that shard. What write rate does that force? How does it compare with a hybrid at `T = 120` and `e = 10` events per player-hour?
3. In the table above, what `T` makes the write volume exactly 1 MB/s?

<details>
<summary>Answers</summary>

1. `W = 10,000 / 120 = 83.3` saves/s. `B = 83.3 × 30,000 = 2.5 MB/s`. Player-hours `= 10,000 × 60 / 3,600 = 166.7`.
2. Average loss 20 s means `T = 40`, so `W = 250` saves/s. Hybrid: `83.3 + 10,000 × 10 / 3,600 = 83.3 + 27.8 = 111.1` writes/s, less than half, with zero loss on valuable state.
3. `B = N × S / T`, so `T = 4,000 × 24,000 / 1,000,000 = 96` seconds.

</details>

## 3. Four reasons persistence is hard

The save-interval model is the first problem. Here are all four, each with the week that solves it properly.

### 3.1 Crashes in the middle of a write

A save is not instant. Writing 24 kB is many small operations, and a crash can land between any two of them. Here is the save routine almost everyone writes first:

```python
import json

def naive_save(path, state):
    with open(path, "w") as f:      # truncates the old save to 0 bytes
        f.write(json.dumps(state))   # writes the new one, piece by piece
```

The first line destroys the old save before the second line has written the new one. Crash between them and you have neither. Crash halfway through the write and you have half a JSON document, which the loader rejects. The player's character is not rolled back. It is gone.

The standard fix is to never overwrite in place:

```python
import json, os

def atomic_save(path, state):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        f.write(json.dumps(state))
        f.flush()                    # push Python's buffer to the OS
        os.fsync(f.fileno())         # ask the OS to push it to the disk
    os.replace(tmp, path)            # swap the new file in, in one step
```

`os.replace` renames the temporary file over the real one. On the same file system, the rename is atomic: other readers see either the old file or the new one, never a mix. The `fsync` matters because the operating system otherwise keeps written data in memory for a while, and a power cut would lose it even after `write` returned. (A fully paranoid version also syncs the directory after the rename, so the rename itself is durable. For this course the version above is enough.)

A database does the same job with more care. SQLite, in its default rollback-journal mode, copies the original pages into a separate journal file and flushes it to disk before touching the database file. Then it writes the changes and flushes again. Deleting the journal is the moment of commit. If power fails before that, the journal still exists and SQLite rolls the change back on the next open. PostgreSQL uses a write-ahead log (WAL): every change is first appended to a log and flushed, and the data files are updated later. After a crash it replays the log. Both designs share one idea with `atomic_save`: at every instant there is one complete, valid version on disk.

In Lab 01 you inject a crash at 41 different points during a save. `naive_save` corrupts the file every time; your `atomic_save` must corrupt it zero times.

**Solved properly in:** week 5 (transactions and ACID) and week 14 (backups and recovery).

### 3.2 Two writers at once

A single-player game has one writer, the game. An online game has many. Two players trade. A player sells an item at the same moment a guild officer withdraws it from the guild bank. Two server processes both load the same character, change different fields, and save the whole blob. The second save overwrites the first, and one change silently disappears. That is called a **lost update**.

Worse, some concurrency bugs create value instead of losing it. If a trade removes the item from player A and adds it to player B in two separate saves, and the server crashes between them, the item may exist in both saves or in neither. A duplication bug ("dupe") creates items or gold from nothing, and the extra supply lowers prices for everyone who earned theirs (see [MMO304 week 4](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w04-money-supply-per-capita-and-inflation.md) for what extra money supply does to prices).

**Solved properly in:** week 5 (transactions) and week 6, whose worked example steps through two concurrent trades without a transaction, frame by frame.

### 3.3 Scale

The table in section 2 already showed one kind of scale problem: write rate grows with players and shrinks with `T`. There are others.

- **Reads at login.** When a shard restarts after maintenance, thousands of players log in within minutes, and each login reads a full character. 4,000 logins in 5 minutes is 13 character loads per second, on top of the saves.
- **Queries across players.** "How many Emberfang Swords exist?" is easy for one character's save file and painful for 200,000 of them if each is an opaque blob. Week 2 builds the model for that.
- **Growth.** Characters accumulate items, mail, achievements. A state that is 24 kB at launch can be 200 kB after two years, and `B` grows with it.

**Solved properly in:** weeks 2 to 4 (modeling, SQL, indexes) and weeks [7](w07-nosql-and-key-value-stores-redis.md) and [8](w08-caching-and-write-behind.md) (Redis caching and write-behind, which is the hybrid policy of section 2 turned into an architecture).

### 3.4 Change over time

A game that ships patches changes its data format. You add a "transmog" field to every item. You split "gold" into "gold" and "bound gold." Every save written before the patch must still load after it, possibly years later, when a player returns. In an online game the problem is sharper: you cannot stop the world for a day to rewrite 30 million item rows.

**Solved properly in:** week 9 (schema migrations in a live game).

## 4. Files or a database?

For a single-player game, the atomic save of section 3.1 is often all you need. The file belongs to one player, one process writes it, and nobody queries across saves.

An online game breaks every one of those assumptions, which is why servers use a database. A database gives you, among other things:

- **Atomic, durable commits** without you writing journal logic.
- **Transactions** that change many records together or not at all (week 5).
- **Concurrency control**, so two writers cannot silently overwrite each other (week 6).
- **A query language**, SQL, to ask questions across all players (weeks 3 and 4).
- **Constraints** that reject impossible data, such as a stack of minus three potions (week 2).

This course's reference stack has two parts. **PostgreSQL** is a relational database and the system of record, the place where the truth about characters and items lives. **Redis** is an in-memory key-value store used as a cache and for fast-changing state (weeks 7 and 8). The labs use Python's built-in `sqlite3` module because it needs no server. SQLite and PostgreSQL both speak SQL and both give you atomic commits, and each lecture points out where they differ.

A mental picture for the semester: memory is where the game runs, Redis is where fast-changing state waits, PostgreSQL is where the truth lives, and every design choice is about what moves between them and how often.

## In-class activity (25 minutes)

In groups of three, you are the persistence team for an invented action MMO with these numbers: 6,000 players per shard at peak, a 40 kB character state, and an average player who gets a rare drop every 8 minutes, trades twice an hour and completes a quest every 12 minutes.

1. List every piece of player state you can think of (aim for 12 or more) and mark each one cheap or valuable. Two minutes of arguing per borderline case is fine.
2. Compute `e`, the valuable events per player-hour, from the numbers above.
3. Your database team says the shard can sustain 150 durable writes per second for saves. Find the shortest periodic `T` that fits the budget with the hybrid policy.
4. Compute the average loss of cheap state at that `T`, and write one sentence you would put in the patch notes explaining it to players.

Expected output: the labelled state list, `e = 7.5 + 2 + 5 = 14.5` per hour, a `T` with its arithmetic, and the patch-note sentence. (Check: `6,000 × 14.5 / 3,600 = 24.2` event writes/s leaves 125.8 for periodic saves, so `T = 6,000 / 125.8 ≈ 48` seconds.)

## Common misconceptions

- **"Saving more often is always safer."** It lowers loss and raises write load in exact proportion. Past some point the database falls behind, saves queue up, and loss goes up again. Spend frequent saves only on valuable state.
- **"If `write()` returned, the data is on disk."** It is in the operating system's memory. Without `fsync` (or a database commit that does it for you), a power cut can still lose it.
- **"A crash rolls the player back to the last save."** Only if the last save is intact. With an in-place overwrite, a crash during the save leaves no valid save at all. Rollback is the good outcome.
- **"Persistence is a back-end detail designers don't need to think about."** The choice of which events are valuable, and how much loss is acceptable, is a design decision with player-facing consequences. Stardew's end-of-day rule is a design rule players learn.

## Check yourself

1. Two shards have the same player count. Shard A saves every 30 seconds; shard B every 90 seconds. Without computing absolute numbers, give the ratio of their write rates and the ratio of their average losses.
2. A 2,000-player shard with 50 kB states and `T = 60` s adds event saves of 3 kB at `e = 20` per player-hour. Compute the total writes per second and total bytes per second.
3. A student's save routine opens the real save file with mode `"w"`, writes the JSON, then calls `fsync`. Describe a crash moment that still destroys the save.
4. Why can Minecraft afford to write only the chunks that changed, while a naive character save rewrites the whole blob? What would a character save need to do the same?
5. A server uses `SET LOCAL synchronous_commit TO OFF` for position updates. After a crash, a player's position is 400 ms behind where it was. Is that a bug? What would make it one?

<details>
<summary>Answers</summary>

1. `W = N / T`, so A writes 3 times as often as B. Average loss is `T / 2`, so A loses one third as much. The product is the same for both.
2. Periodic: `2,000 / 60 = 33.3` saves/s at 50,000 bytes, 1.67 MB/s. Events: `2,000 × 20 / 3,600 = 11.1` writes/s at 3,000 bytes, 33.3 kB/s. Total 44.4 writes/s and about 1.70 MB/s.
3. Opening with `"w"` truncates the file to zero bytes immediately. A crash any time before the write finishes (and before `fsync` completes) leaves an empty or partial file. `fsync` at the end does not help, because the old version is already gone.
4. Region files keep a per-chunk offset and timestamp table, so each chunk is addressable on its own. A character save would need the same property: separate records for separately changing parts (inventory rows, quest rows) instead of one blob. That is next week's relational model.
5. Not a bug: position is cheap state, and the documented loss window is up to 600 ms. It becomes a bug if something valuable depended on that position, for example a teleport that charged gold and was committed synchronously while the position change was not, leaving the player charged but not moved.

</details>

## Lab / assignment hook

[Lab 01, save intervals and a crash-proof save](../labs/lab01.md). Run the periodic-save model, confirm the `T / 2` average by simulation, compute the hybrid write rate, and write an `atomic_save` that survives a crash injected at 41 points during the write. Deliverable: the completed `save_sim.py`, the filled tables, and a 250-word save policy for the in-class MMO.

## Sources

- Stardew Valley Wiki, "Saves" (wiki as of September 2026). The game saves when the day ends (going to bed, exhaustion, or 2 a.m.), and quitting mid-day loses the day's progress.
- Stardew Valley Wiki, "Day Cycle" (wiki as of September 2026). 0.7 real seconds per in-game minute; the day runs 6 a.m. to 2 a.m., about 14 minutes of real time; multiplayer does not pause automatically.
- Stardew Valley Wiki, "Multiplayer" (wiki as of September 2026). All players must go to bed to end the day; the host keeps the save file.
- Minecraft Wiki, "Autosave" (Java Edition, current as of 2026). Autosave every 6,000 ticks (5 minutes) and on opening the pause menu.
- Minecraft Wiki, "Region file format" (Java Edition, Beta 1.3 onward; Anvil since 1.2.1). 32 × 32 chunks per region, 4 KiB sectors, a per-chunk location table and a last-modified timestamp table.
- PostgreSQL 18 documentation, "Asynchronous Commit" and "Write Ahead Log" server configuration. `synchronous_commit` defaults to on and can be set per transaction; the loss window is up to three times `wal_writer_delay` (default 200 ms); the risk is loss, not corruption.
- SQLite documentation, "Atomic Commit In SQLite" (sqlite.org/atomiccommit.html). Rollback journal, flush ordering, and deletion of the journal as the commit point.
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly. Chapter 7.

## Interactive spec: examples/w01-save-interval-tradeoff.html

**The one insight:** for periodic saves, write rate times average loss is fixed at `N / 2`, so moving the save interval only slides you along a hyperbola. Saving valuable events immediately is the only move that lands below the curve.

**Layout (two linked views, stacked on mobile, side by side at ≥ 900px):**

- View A, "one player's hour": horizontal timeline from 0 to 3,600 s. Progress is a rising line (1 unit per second of play). Save ticks are vertical marks every `T` seconds. Valuable events appear as diamond markers at fixed pseudo-random times (seeded, `e` per hour). A draggable crash marker (default at 2,000 s). The region from the last save tick before the crash to the crash is shaded in the alert color and labelled "lost: X s". When event saves are on, diamonds before the crash are drawn filled (saved) and the label adds "valuable events lost: 0"; when off, diamonds inside the shaded region are drawn hollow and counted as lost.
- View B, "the trade-off": log-log chart. x-axis average loss in seconds (0.1 to 1,000), y-axis writes per second (1 to 10,000). Draw the curve `W = (N/2) / loss` for the current `N` as a solid line. Draw the current periodic policy as a point on it. When event saves are on, draw a second point for the hybrid at `x = 0` for valuable state (draw it at the left axis edge with a label "valuable: 0 s") and `y = N/T + N·e/3600`, plus a dashed horizontal guide showing how far left on the curve you would have to move to get the same valuable-state loss by periodic saves alone (cap the guide at loss 0.5 s).

**Controls:**

- `T` slider, log scale, snapping to 1, 2, 5, 10, 30, 60, 120, 300, 600, 840, 1,800 s (default 300).
- `N` slider, 100 to 20,000, step 100 (default 4,000).
- `S` input in kB, 1 to 500 (default 24).
- Toggle "save on valuable events" (default off) and `e` slider, 0 to 60 per player-hour (default 12).
- Event save size in kB, 0.5 to 20 (default 2).
- Draggable crash marker in view A, also operable with arrow keys (±10 s, Shift ±100 s).

**Readout panel (exact numbers, always visible):** `W` (1 decimal), `B` in kB/s or MB/s (3 significant figures), average loss `T/2`, worst loss `T`, player-hours lost per crash `N·T/2/3600` (2 decimals), the product `W × T/2` (shows `N/2`), and with events on, hybrid writes/s `N/T + N·e/3600` and hybrid bytes/s `N·S/T + N·e·s_e/3600`.

**Formulas:**

```
W        = N / T
B        = N × S / T
avg_loss = T / 2
worst    = T
p_hours  = N × T / 2 / 3600
W_hybrid = N / T + N × e / 3600
B_hybrid = N × S / T + N × e × s_e / 3600
```

**Test values (must match):** player-hours are shown to two decimals, so the lecture table's 166.7 appears as 166.67.

- `N = 4,000, S = 24 kB, T = 300`: `W = 13.3`, `B = 320 kB/s`, avg loss 150 s, player-hours 166.67, product 2,000.
- `T = 10`: `W = 400`, `B = 9.6 MB/s`, player-hours 5.56.
- `T = 840`: `W = 4.8`, `B = 114 kB/s`, player-hours 466.67.
- Events on, `e = 12`, `s_e = 2 kB`, `T = 300`: `W_hybrid = 26.7`, `B_hybrid = 346.7 kB/s`.
- `N = 10,000, S = 30 kB, T = 120`: `W = 83.3`, `B = 2.5 MB/s`, player-hours 166.67.

**First screen:** defaults above with event saves off, crash marker at 2,000 s (last save at 1,800 s, "lost: 200 s"), the point sitting on the curve, and a one-line caption: "Move T: the point slides along the curve. It never goes below it."

**Accessibility:** all controls keyboard operable with visible focus; readout in an `aria-live="polite"` region; respects `prefers-reduced-motion` (no animated transitions) and `prefers-color-scheme`; tokens from `templates/interactive-tokens.css` inline. Generic shapes only, no game art.

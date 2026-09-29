# DB201 · Week 10 — Telemetry Design: Events and Properties

**Why this matters:** Every question a designer will ask after launch ("where do players die?", "did the patch make the dungeon easier?", "why do people quit on day two?") can only be answered from data you decided to record before launch. A field you forgot is gone for every day it was missing. This week you learn to design the event before you write the code that sends it.

**You will be able to:**
- Decompose a telemetry event into an envelope and event-specific properties, and write both as a table schema.
- Compute bytes per event and storage per day and per year for a given audience, and compare designs by cost.
- Test a tracking plan against a list of design questions and name the missing field for each question it cannot answer.
- Critique an event taxonomy for naming, cardinality and trust (client or server as the source).

**Before class:** Kleppmann, *Designing Data-Intensive Applications* (2017), chapter 2 on data models, and the "Event Sourcing" part of chapter 11 (the idea of an append-only log of facts). Skim the GameAnalytics documentation page "Event types" (collection API). Reread your CS102 notes on the Observer pattern.

**Prerequisites from earlier courses:** [CS102 week 10, Observer and events](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w10-observer-and-events.md) (how game code announces "something happened" without knowing who listens; a telemetry sender is one more listener). [GD101 week 7, playtesting](../../GD101-introduction-to-game-design/lectures/w07-playtesting-observe-dont-explain.md) (observing players before you ask them). [MA102 week 12, descriptive statistics for playtests](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md) (what you will do with the numbers). From this course, [DB201 week 2, relational modeling](w02-relational-modeling-characters-inventories-items.md) (tables and column types) and [DB201 week 4, indexes and query plans](w04-sql-ii-indexes-and-query-plans.md).

**Interactive:** [Event schema designer](../examples/w10-event-schema-designer.html). Keep it open during section 2.

---

## 1. From saving state to recording history

For nine weeks this course has been about **state**: what is true about the world right now. The `characters` table says Aldric is level 12 with 340 gold. When he earns 20 gold you update the row, and the old value is gone. That is correct for a save system. The game only needs the present.

A designer asking "how fast do warriors level?" needs the past. The current row says level 12. It does not say he reached level 11 on Tuesday and level 12 on Friday, or that he died nine times in between. **Telemetry** is the practice of recording what happened, as it happens, so you can answer questions about play later.

The unit of telemetry is the **event**: an immutable record that one thing happened at one moment. Three words in that definition carry weight.

- **Immutable.** You never update an event. If Aldric's death was recorded with the wrong zone, you do not fix the row. You fix the code and, if needed, record a correction. The log is a history, and histories are append-only.
- **One thing.** A death is an event. "Aldric's stats this session" is not. It is a summary, and summaries can always be computed from events, never the reverse.
- **At one moment.** Every event has a timestamp. Without it you cannot order events, join them to sessions, or compare before and after a patch.

Kleppmann calls this style of storage an **event log** and points out that the current state of anything is a function of the log. Game developers use the same idea in replays ([CS102 week 12](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w12-command-pattern-input-replay-undo.md) recorded inputs as commands for exactly this reason). Telemetry applies it to questions instead of playback.

Two terms you will use all week:

- **Event name** (or event type): which kind of thing happened, such as `player_died` or `item_crafted`.
- **Property**: one named value attached to an event, such as `zone_id = 14` or `killer_id = 2101`. Some analytics tools call properties "parameters", "attributes" or "fields". They mean the same thing.

## 2. Worked example: the death event, from counter to heat map

### The hook

In August 2007 Wired published a long feature on how Microsoft's user research group tested Halo 3 before launch. Two details matter for us. First, during Halo 2 the researchers had built tools to extract, for each tester, their location and when and where they fired weapons, rode vehicles, killed enemies and died. Second, in April 2007 they produced a heat map of player deaths on Valhalla, one of Halo 3's multiplayer maps. The deaths skewed toward one base, which meant the team attacking from the other side had a small advantage. The designers changed the terrain to even it out.

Now ask the question that makes this a data design lesson. Suppose the Halo team had recorded only a number, "deaths this match", for each player. Could they have found the Valhalla problem? No. Both teams die about equally often in a close match. The imbalance lived in **where** the deaths happened, and a counter throws "where" away the moment it increments. The fix was possible only because someone had decided, before the test, that a death is an event with a position.

### The model

An event has two parts.

```
event = envelope + properties

envelope   = the fields every event carries, whatever its name
properties = the fields that only this event name carries
```

For this course's reference stack (PostgreSQL), the envelope is:

| Field | Type | Bytes | Why every event needs it |
|---|---|---|---|
| `event_id` | uuid | 16 | Unique id, so a retried send can be recognized as a duplicate (week 11) |
| `event_type` | smallint | 2 | The event name, stored as an id into an `event_types` table |
| `event_time` | timestamptz | 8 | When it happened |
| `player_id` | bigint | 8 | Who it happened to |
| `session_id` | uuid | 16 | Which play session, so events can be grouped and ordered |
| `build_id` | int | 4 | Which game version, so you can compare before and after a patch |
| **Total** | | **54** | |

The cost model is one multiplication:

```
bytes per row  = row_overhead + envelope + properties
bytes per day  = DAU × events per player per day × bytes per row
```

- **DAU** is daily active users, the number of distinct players who play on a given day (week 12 is about defining it properly).
- **row_overhead** is what the database adds to every row. In PostgreSQL each row has a 23-byte header padded to 24 bytes, plus a 4-byte pointer in the page, so 28 bytes.

We ignore alignment padding (PostgreSQL may add a few bytes depending on column order), indexes (which often add 30 to 100% more), and compression. The model is for comparing designs, not for ordering disks.

The second half of the model is the **answerability test**:

```
A design can answer question Q  if and only if  every field Q needs is recorded,
either on the event itself or on another event you can join to it.
```

### Numbers you can check

Take an invented MMO with 40,000 DAU. Each player dies on average 25 times a day, so there are 1,000,000 deaths a day. Here are three designs for recording them.

**Design A, a counter.** One row per player per day: `player_id` (8), `day` (date, 4), `deaths` (int, 4). That is 16 bytes of data plus 28 of overhead, 44 bytes per row, 40,000 rows a day.

**Design B, a lean event.** One row per death: the 54-byte envelope plus `zone_id` (int, 4), `x` and `y` (real, 4 each) and `killer_id` (int, 4). That is 70 bytes of data plus 28, so 98 bytes per row.

**Design C, a rich event.** Design B plus `z` (real, 4), `killer_kind` (smallint, 2: mob, player or environment), `ability_id` (int, 4), `player_level` (smallint, 2), `group_size` (smallint, 2) and `damage_last_5s` (int, 4). That adds 18 bytes, so 116 bytes per row.

| Design | Bytes per row | Rows per day | MB per day | GB per year |
|---|---|---|---|---|
| A, counter | 44 | 40,000 | 1.76 | 0.64 |
| B, lean event | 98 | 1,000,000 | 98 | 35.8 |
| C, rich event | 116 | 1,000,000 | 116 | 42.3 |

Check one line by hand. Design B: 98 bytes × 1,000,000 = 98,000,000 bytes, which is 98 MB. Times 365 is 35,770 MB, or 35.8 GB.

Now the questions a designer will ask about deaths:

| # | Question | Fields needed | A | B | C |
|---|---|---|---|---|---|
| Q1 | How many deaths per day? | any | yes | yes | yes |
| Q2 | Which zone kills the most players? | `zone_id` | no | yes | yes |
| Q3 | Where inside the zone do they die? | `zone_id`, `x`, `y` | no | yes | yes |
| Q4 | Which mob kills the most players? | `killer_id` | no | yes | yes |
| Q5 | Which of that mob's abilities is overtuned? | `killer_id`, `ability_id` | no | no | yes |
| Q6 | Do players quit the session soon after dying? | `event_time`, `session_id`, plus a `session_ended` event | no | yes | yes |
| Q7 | Do solo players die more than grouped players? | `group_size` | no | no | yes |

Read the two tables together.

- Going from A to B multiplies storage by about 56 and turns one answerable question into five. That is the big step, and it is the step from **counting** to **recording**.
- Going from B to C costs 18% more storage and answers the last two questions. Once you pay for the envelope and the row, extra properties are cheap.
- You can compute Design A from Design B with one `GROUP BY`. You can never compute B from A. A counter is a view of events, and a view cannot be un-computed.

For scale, compare with a real pipeline. An AWS case study from about 2015 reports that Supercell, then running three games (Hay Day, Clash of Clans and Boom Beach), handled 45 billion events a day and stored up to 10 TB of event data a day. Divide one by the other and you get roughly 220 bytes per event. The storage format is not stated, so do not read too much into the exact figure, but it tells you that our 100 to 120 byte rows are the right order of magnitude.

### The visual

Open `examples/w10-event-schema-designer.html`. The left panel lists the candidate fields with their byte sizes. Tick and untick them. The middle panel shows bytes per row, MB per day and GB per year for the DAU and deaths-per-player you set with the sliders. The right panel shows the seven questions, each lit or dark.

Watch the two panels move together. Storage grows in small, even steps as you add fields. Questions light up in jumps, and some need two fields at once (Q5 needs `killer_id` and `ability_id`). Now switch the mode to "counter". Storage collapses to under 2 MB a day and six questions go dark at once. That is the picture to remember. **Storage cost is roughly linear in fields, but the value of the data is not.** The first decision, event versus counter, matters far more than any single property.

### Cross-game recognition

The envelope-plus-properties split appears everywhere that games record events, often under other names.

**World of Warcraft's combat log (retail and classic clients, through the 11.x patches).** Every combat log entry starts with the same 11 base parameters: timestamp, subevent name, a hide-caster flag, then GUID, name, flags and raid flags for the source and for the destination. After that come prefix parameters (for a `SPELL_` event, the spell id, name and school) and suffix parameters (for `_DAMAGE`, the amount, overkill, school, resisted, blocked, absorbed, critical and more). That is our model exactly. The base parameters are the envelope, the prefix and suffix parameters are the properties, and the subevent name is built from a prefix and a suffix, so `SPELL_DAMAGE` and `SWING_DAMAGE` share their damage properties. In patch 12.0.0 (2026) Blizzard made addon registration for this event raise an error, as part of restricting what addons can compute in combat, which is a reminder that who may read telemetry is itself a design decision.

**GameAnalytics (collection API documentation, 2025-2026).** This third-party analytics service requires a fixed set of fields on every event, including `user_id`, `session_id`, `session_num`, `client_ts`, the event format version `v` (currently 2), `sdk_version`, `platform`, `os_version`, `device` and `manufacturer`. That is its envelope. It then defines event categories (business, resource, progression, design, error and a few more), each with its own properties. Its design events use an id of one to five colon-separated parts, such as `Boss:Dragon:Phase2:Death`, which is a hierarchical event name. Progression events use two to four parts, starting with `Start`, `Fail` or `Complete`.

**Halo 2 and Halo 3 user research (2004-2007).** The Wired account describes each logged action carrying a player, a time and a position, and the researchers linking those records to video of the session. Microsoft's researchers later described the system, called TRUE, in a CHI 2008 paper. Same split. What happened, plus who, when and where.

Three sources, three vocabularies ("base parameters", "default annotations", "instrumentation"), one structure. When you meet a new analytics tool, find its envelope first. It tells you what every question can be sliced by for free.

### Design judgment

The model tells you what a design costs and what it can answer. It does not tell you what to choose. Here are the decisions to make on purpose.

- **Record events, derive counters.** Unless volume is truly prohibitive, record the event and compute the counter. Storage is the cheapest resource in the pipeline, and the questions you did not think of are the ones that matter after launch.
- **Start from questions, not from code.** Write the questions first, then the fields they need, then the event. An event that answers no question is noise you pay to store. The lab's validator refuses such events.
- **Counts need denominators.** "Which zone kills the most players?" is misleading if zone 7 simply has the most players. A fair question is "deaths per hour played in each zone", and that needs an exposure event such as `zone_entered` and `zone_left`, or a periodic heartbeat. Numerators come free with the event. Denominators have to be designed.
- **Sample the floods.** A footstep or position heartbeat every second would dwarf everything else (40,000 players × 2 hours × 3,600 seconds is 288 million rows a day). Record it every 10 seconds, or for 5% of sessions, and write the sampling rate into the event so analysts can scale back up.
- **Personal data is a liability.** Even `player_id` makes an event personal data, because you can join it to the account table. A free-text `player_name` or chat line makes it worse. [Week 13](w13-privacy-gdpr-and-data-retention.md) replaces `player_id` in the envelope with a random `telemetry_id` held in one mapping table. For now, identify players by id only and never by name.

## 3. Naming events and keeping a tracking plan

A **tracking plan** is the document (often a table or a JSON file under version control) that lists every event, its properties with types, who sends it, and which questions it answers. It is the schema of your telemetry, and it deserves the same review as a database migration.

Naming rules that save pain later:

- **`object_action`, in the past tense, in lower snake case.** `player_died`, `item_crafted`, `quest_completed`, `session_started`. The past tense reminds everyone that an event is a fact that already happened. `object_action` puts related events next to each other when sorted (`item_crafted`, `item_equipped`, `item_sold`).
- **No values in names.** `death_zone_14` is one event with a property baked into its name. With 40 zones you now have 40 event names, and "deaths in any zone" needs 40 queries. Write `player_died` with `zone_id = 14`.
- **One name, one meaning.** If the client sends `player_died` when the death animation ends and the server sends `player_died` when health hits zero, you have two events that disagree by a few seconds and occasionally by a whole death (a heal landing during the animation). Give them different names or pick one source.
- **Version the schema.** When `player_died` gains a property, old rows do not have it. Keep an `event_version` or rely on `build_id`, and document from which build each property exists.

Here is the tracking plan entry for Design C, and the PostgreSQL table it becomes.

```json
{
  "name": "player_died",
  "source": "server",
  "since_build": 1405,
  "answers": ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7"],
  "properties": {
    "zone_id": "int", "x": "real", "y": "real", "z": "real",
    "killer_kind": "smallint", "killer_id": "int", "ability_id": "int",
    "player_level": "smallint", "group_size": "smallint", "damage_last_5s": "int"
  }
}
```

```sql
CREATE TABLE event_types (
  event_type smallint PRIMARY KEY,
  name       text NOT NULL UNIQUE          -- 'player_died'
);

CREATE TABLE ev_player_died (
  event_id       uuid PRIMARY KEY,
  event_type     smallint NOT NULL REFERENCES event_types,
  event_time     timestamptz NOT NULL,
  player_id      bigint NOT NULL,
  session_id     uuid NOT NULL,
  build_id       int NOT NULL,
  zone_id        int NOT NULL,
  x real, y real, z real,
  killer_kind    smallint NOT NULL,
  killer_id      int,
  ability_id     int,
  player_level   smallint NOT NULL,
  group_size     smallint NOT NULL,
  damage_last_5s int
);
```

You have a choice here that the model makes visible. Option one, shown above, is **one typed table per event name**. Every property is a real column with a type, queries are fast and the database rejects a text value in `zone_id`. Adding a property is a migration ([week 9](w09-schema-migrations-in-a-live-game.md)). Option two is **one wide `events` table** with the envelope as columns and all properties in a single `jsonb` column. Adding a property needs no migration, but every read has to extract it (`(properties->>'zone_id')::int`), types are checked by nobody, and the JSON keys are stored in every row (the word `"damage_last_5s"` alone is 16 bytes, repeated a million times a day). Many studios do both. Raw events land in the flexible table, and the events that dashboards read often are copied into typed tables. Week 11 builds exactly that pipeline.

In SQLite, which the labs use, `jsonb` does not exist as a column type. You store JSON as text and read it with `json_extract(properties, '$.zone_id')`. The idea is identical.

## 4. Cardinality: the property that eats your budget

The **cardinality** of a property is the number of distinct values it takes. `killer_kind` has 3. `zone_id` has perhaps 40. `x` stored as a float has, in practice, one distinct value per row.

High cardinality is harmless in a raw event table. A float column costs 4 bytes whatever its value. It becomes a problem when a tool **pre-aggregates** by that property, because every distinct combination of values becomes a row or a counter somewhere. GameAnalytics states this openly. Its documentation sets daily limits on unique event-id combinations (15,000 for design events, 8,000 for progression, 4,000 for resource) and explains that too many unique combinations produce many rows with one or two hits each and slow its dashboards down. From 1 October 2025, ids over the limit are recorded as null in its aggregated metrics, while the raw export keeps them.

Work the numbers for a heat map. Your zones are 800 m by 800 m and you have 40 of them.

| Grid for the heat map | Cells per zone | Cells across 40 zones | Fits a 15,000 limit? |
|---|---|---|---|
| Raw float `x`, `y` | about 1 per death | about 1,000,000 a day | no |
| 10 m cells | 80 × 80 = 6,400 | 256,000 | no |
| 25 m cells | 32 × 32 = 1,024 | 40,960 | no |
| 50 m cells | 16 × 16 = 256 | 10,240 | yes |

The rule that falls out: **keep raw values in the raw event, and bucket only where you aggregate.** Store `x` and `y` as floats. When you build the heat map, compute `floor(x / 50)` and `floor(y / 50)` in the query. If the designer later wants 10 m resolution around one boss arena, the raw data still has it.

The same rule explains why values must stay out of event names (section 3). An event name is always a dimension of aggregation. `death_zone_14_x_310_y_402` has the cardinality of a float.

## 5. Who sends the event: client or server?

In an online game, most events could be sent from the player's machine or from your server. The choice decides whether you can trust them.

- **Server events** are generated by code you run. `player_died`, `item_looted`, `gold_changed` and `trade_completed` should come from the server, which is authoritative for them anyway ([CS202 week 4](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w04-server-authority-never-trust-the-client.md) teaches why the server must be the authority for game state). A player cannot forge them, and their `event_time` comes from a clock you control.
- **Client events** describe things only the client knows: frame rate, loading time, which menu the player opened, whether a tutorial tooltip was dismissed. They are useful and untrustworthy. A modified client can send anything, and a phone's clock can be hours wrong.

A practical rule. If a number could ever feed an economic decision, a ban, or a reward, it must come from the server. If it describes the player's experience of the interface, it comes from the client, and you treat it as a measurement with noise.

Client events carry one more problem you will meet next week. They arrive late. A phone in a tunnel queues its events and sends them when it reconnects, maybe the next day. That is why the lab's events carry both `event_time` (when it happened, by the sender's clock) and `received_at` (when your collector got it, by your clock).

## In-class activity (25 minutes)

Work in pairs. Your game is the invented MMO from section 2. The live team has asked four questions about crafting:

1. Which recipes are crafted most, and does that change after patch 1.4.6?
2. How much gold do players spend on crafting materials per day?
3. Do players who craft on their first day come back on their second day more often?
4. Which crafting station is idle most of the time?

Steps:

1. For each question, list the fields it needs. Mark which already exist in the envelope. (8 minutes)
2. Design the event or events (name, properties with types, source client or server). At least one question needs a denominator or a second event. Find it. (10 minutes)
3. Compute bytes per row with the section 2 model, assume 40,000 DAU and 6 crafts per player per day, and give MB per day. (5 minutes)
4. Swap with another pair. Name one question their plan cannot answer. (2 minutes)

Expected output: a tracking-plan table with 2 to 4 events, the storage figure, and the gap your partners found. A typical answer has `item_crafted` (recipe id, station id, quantity, gold spent) from the server, reusing the envelope's `build_id` for question 1 and `player_id` joined to the first `session_started` for question 3. Question 4 cannot be answered from craft events alone. Idle time needs station occupancy, which is a denominator.

## Common misconceptions

- **"We'll add the field later if we need it."** You can add it later, but the history before that build will never have it. A heat map requested in month six covers months six onward. Decide the fields you would regret missing before launch.
- **"Counters are the efficient version of events."** They are the lossy version. At 56 times less storage, Design A answers one question in seven. Store events and compute counters from them.
- **"More properties means much more storage."** Past the envelope and row overhead, each property is 2 to 8 bytes. Adding six properties to Design B cost 18%. The expensive decisions are event frequency and event-versus-counter, not property count.
- **"Telemetry is just logging."** Debug logs are free text for engineers, written in whatever format the programmer liked that day. Telemetry events have a schema, a tracking plan and typed properties, and they are designed to be aggregated by people who never read the code.

## Check yourself

1. Your game has 120,000 DAU, and each player loots 60 items a day. The `item_looted` event carries the 54-byte envelope plus `item_type_id` (int), `quantity` (smallint), `source_kind` (smallint) and `zone_id` (int). Using 28 bytes of row overhead, compute bytes per row, GB per day and GB per year.
2. A designer asks, "Is the Frost Wyrm's breath attack killing more players since build 1406?" Which fields does the event need? Which of Designs A, B and C in section 2 can answer it?
3. Your analytics tool allows 15,000 unique combinations per day. You want a death heat map across 40 zones of 1,200 m by 1,200 m each. What is the smallest square cell size, in whole multiples of 10 m, that fits?
4. A teammate proposes the event names `boss_1_killed`, `boss_2_killed`, ..., `boss_30_killed`. Rewrite them and explain in one sentence what query becomes simpler.
5. Is `gold_changed` a client event or a server event? Is `settings_menu_opened`? Justify each in one sentence.

<details>
<summary>Answers</summary>

1. Properties are 4 + 2 + 2 + 4 = 12 bytes. Bytes per row = 28 + 54 + 12 = 94. Rows per day = 120,000 × 60 = 7,200,000. Bytes per day = 94 × 7,200,000 = 676,800,000, about 0.68 GB. Per year, 0.6768 × 365 ≈ 247 GB.
2. It needs `killer_id` (to pick the Frost Wyrm), `ability_id` (to pick the breath attack) and `build_id` (to split before and after). Only Design C has `ability_id`, so only C can answer it. `build_id` is in the envelope of B and C, but B lacks the ability.
3. Cells per zone must be at most 15,000 / 40 = 375, so at most 19 × 19 = 361 cells (20 × 20 = 400 is too many). Cell size must be at least 1,200 / 19 ≈ 63.2 m. The next multiple of 10 m is 70 m. Then 1,200 / 70 = 17.1, so the grid is 18 × 18 = 324 cells per zone and 12,960 in total, which fits. (60 m gives 20 × 20 = 400 per zone, 16,000 in total, which does not.)
4. `boss_killed` with a property `boss_id`. "How many bosses were killed per day" becomes one `COUNT(*)` with no list of 30 names, and adding boss 31 needs no new event.
5. `gold_changed` is a server event, because it feeds the economy and a client could forge it. `settings_menu_opened` is a client event, because only the client knows about the menu, and a forged value harms nothing but the UI statistics.

</details>

## Lab / assignment hook

[Lab 10, tracking plan and event validator](../labs/lab10.md). You fix and extend a tracking plan for seven design questions, run the validator on a sample event stream full of the mistakes from sections 3 and 4, and produce a storage estimate for your plan. Deliverable: the corrected `tracking_plan.json`, the validator output, and a one-page memo.

## Sources

- Thompson, C. "Halo 3: How Microsoft Labs Invented a New Science of Play." *Wired*, issue 15.09, published online 21 August 2007. Halo 2 tools that extracted player location, weapon fire, vehicle use, kills and deaths; 2,300 hours of Halo 2 play by 400 testers; more than 3,000 hours of Halo 3 by about 600; the April 2007 Valhalla death heat map and the terrain change. Read via the Internet Archive copy of wired.com/2007/08/ff-halo-2.
- Kim, J. H., Gunn, D. V., Schuh, E., Phillips, B., Pagulayan, R. J. & Wixon, D. (2008). "Tracking real-time user experience (TRUE): a comprehensive instrumentation solution for complex systems." *Proceedings of CHI 2008*, pp. 443-452. doi:10.1145/1357054.1357126. Cited for the existence and name of the system; details in this lecture come from the Wired article.
- Warcraft Wiki, "COMBAT_LOG_EVENT" and "Patch 12.0.0/API changes" (accessed September 2026). The 11 base parameters, prefix and suffix parameters, the `SPELL_DAMAGE` example, and the 12.0.0 change (build 65655, 28 January 2026 in the wiki's build list) under which registering `COMBAT_LOG_EVENT` or `COMBAT_LOG_EVENT_UNFILTERED` raises an error. The wiki page links the diff of Blizzard's UI source (Gethe/wow-ui-source, 11.2.7 to 12.0.0).
- GameAnalytics documentation, "Event types" (collection API) and "Event tracking and cardinality limits" (accessed September 2026). Required shared fields, event categories, design and progression id formats, daily cardinality limits of 15,000 (design), 8,000 (progression) and 4,000 (resource), and the rule from 1 October 2025 that events over the limit are still collected with their identifiers set to "null". Required fields checked on the "Event types" page (docs.gameanalytics.com, September 2026), where `v` is the event version, not the game version.
- Amazon Web Services, "Supercell Case Study" (version with these figures first archived by the Internet Archive in January 2016, when Supercell had three games). 45 billion events per day through Amazon Kinesis; up to 10 TB of game event data per day in Amazon S3.
- PostgreSQL 17 documentation, "Database Page Layout" (heap tuple header of 23 bytes, 4-byte item identifier) and "Data Types" (sizes of uuid, timestamptz, bigint, int, smallint, real).
- Kleppmann, M. (2017). *Designing Data-Intensive Applications*. O'Reilly. Chapters 2 and 11.

## Interactive spec: examples/w10-event-schema-designer.html

**The one insight.** Storage grows in small linear steps as you add properties, but answerable questions jump. The big decision is event versus counter, not how many properties you add.

**Layout.** Three linked panels, stacked on phones (fields, then cost, then questions), side by side at 1,000 px and wider.

1. **Fields panel.** A mode switch at the top with two options, "Event (one row per death)" (default) and "Counter (one row per player per day)". Below it, the envelope as a locked, always-on group (54 B, listed field by field as in section 2). Then ten checkboxes for properties with their byte sizes: `zone_id` 4, `x` 4, `y` 4, `z` 4, `killer_kind` 2, `killer_id` 4, `ability_id` 4, `player_level` 2, `group_size` 2, `damage_last_5s` 4. Preset buttons "A counter", "B lean", "C rich" set the mode and checkboxes to section 2's designs. Default state is Design B.
2. **Cost panel.** Two sliders. DAU from 1,000 to 1,000,000, log scale, default 40,000. Deaths per player per day from 1 to 100, default 25. Readouts: bytes per row, rows per day, MB per day, GB per year (365 days), each with the formula shown in small text. A horizontal bar (log scale from 0.1 MB to 100,000 MB per day) shows MB per day, with ghost markers for designs A, B and C at the current sliders so the gap between A and B is visible.
3. **Questions panel.** Seven cards Q1 to Q7 with the text of section 2's table. Each card is lit (answerable) or dim, and a dim card names the missing field(s).

**Formulas.**
- Event mode: `bytesPerRow = 28 + 54 + sum(checked property bytes)`; `rowsPerDay = DAU × deathsPerPlayer`.
- Counter mode: property checkboxes are disabled and greyed; `bytesPerRow = 28 + 16 = 44`; `rowsPerDay = DAU`.
- `MBperDay = bytesPerRow × rowsPerDay / 1e6`; `GBperYear = MBperDay × 365 / 1000`.
- Answerability in event mode: Q1 always; Q2 needs `zone_id`; Q3 needs `zone_id`, `x`, `y`; Q4 needs `killer_id`; Q5 needs `killer_id` and `ability_id`; Q6 is always answerable in event mode (envelope has `event_time` and `session_id`; the card notes it also needs a `session_ended` event); Q7 needs `group_size`. In counter mode only Q1 is lit.

**Test values (DAU 40,000, 25 deaths per player).**
- Preset A: 44 B per row, 40,000 rows, 1.76 MB per day, 0.64 GB per year, 1 of 7 questions.
- Preset B: 98 B, 1,000,000 rows, 98.0 MB per day, 35.8 GB per year, 5 of 7 (Q1, Q2, Q3, Q4, Q6).
- Preset C: 116 B, 116.0 MB per day, 42.3 GB per year, 7 of 7.
- DAU 120,000, deaths 25, preset C: 348.0 MB per day, 127.0 GB per year.

**Secondary readout.** Under the questions, show "Cost of the last property you ticked: +N B per row (+P%)" so the student sees each property costs a few percent. Example from preset B, ticking `ability_id`: +4 B per row (+4.1%).

**Accessibility.** Every checkbox and preset is keyboard reachable; card state is announced as "answerable" or "not answerable, needs killer_id". Use the shared palette from `templates/interactive-tokens.css`. No game art.

"""DB201 Lab 03: build the practice world game.db (deterministic, seed 303).

Run:  python build_db.py            # writes game.db next to this file
The schema matches the Lab 02 reference schema plus a quest_completions table.
"""
import os
import random
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(HERE, "game.db")

SCHEMA = """
CREATE TABLE item_types (
  type_id      INTEGER PRIMARY KEY,
  name         TEXT NOT NULL UNIQUE,
  rarity       TEXT NOT NULL,
  max_stack    INTEGER NOT NULL CHECK (max_stack >= 1),
  vendor_price INTEGER NOT NULL CHECK (vendor_price >= 0)
);
CREATE TABLE characters (
  character_id INTEGER PRIMARY KEY,
  name         TEXT NOT NULL UNIQUE,
  class        TEXT NOT NULL,
  level        INTEGER NOT NULL DEFAULT 1,
  gold         INTEGER NOT NULL DEFAULT 0 CHECK (gold >= 0)
);
CREATE TABLE items (
  item_id    INTEGER PRIMARY KEY,
  type_id    INTEGER NOT NULL REFERENCES item_types(type_id),
  owner_id   INTEGER NOT NULL REFERENCES characters(character_id),
  bag        INTEGER NOT NULL,
  slot       INTEGER NOT NULL,
  quantity   INTEGER NOT NULL CHECK (quantity >= 1),
  durability INTEGER,
  UNIQUE (owner_id, bag, slot)
);
CREATE TABLE quest_completions (
  character_id INTEGER NOT NULL REFERENCES characters(character_id),
  quest_id     INTEGER NOT NULL,
  completed_day INTEGER NOT NULL,
  PRIMARY KEY (character_id, quest_id)
);
"""

CLASSES = ["warrior"] * 4 + ["mage"] * 3 + ["rogue"] * 3 + ["cleric"] * 2
RARITIES = ["common"] * 6 + ["uncommon"] * 3 + ["rare"] * 2 + ["epic"]


def generate(seed=303):
    """Return (types, chars, items, quests) as lists of tuples."""
    rng = random.Random(seed)
    types = []
    for t in range(1, 301):
        rarity = rng.choice(RARITIES)
        cap = 1 if rarity in ("rare", "epic") else rng.choice([1, 20, 50])
        price = {"common": 2, "uncommon": 15, "rare": 120, "epic": 900}[rarity] * rng.randint(1, 5)
        types.append((t, f"Type {t:03d}", rarity, cap, price))
    chars = []
    for c in range(1, 1201):
        lvl = min(60, max(1, int(rng.gauss(28, 14))))
        gold = int(lvl * rng.uniform(20, 180))
        chars.append((c, f"Hero{c:04d}", rng.choice(CLASSES), lvl, gold))
    items, iid = [], 1
    for (c, _, _, lvl, _) in chars:
        n = 0 if rng.random() < 0.05 else rng.randint(1, 20 + lvl)
        for s in range(n):
            t = types[rng.randint(0, len(types) - 1)]
            qty = rng.randint(1, t[3])
            dur = rng.randint(1, 100) if t[3] == 1 else None
            items.append((iid, t[0], c, s // 24, s % 24, qty, dur))
            iid += 1
    quests = []
    for (c, _, _, lvl, _) in chars:
        k = rng.randint(0, lvl // 2)
        for q in rng.sample(range(1, 101), k):
            quests.append((c, q, rng.randint(1, 90)))
    return types, chars, items, quests


def build(path=DB_PATH):
    if os.path.exists(path):
        os.remove(path)
    types, chars, items, quests = generate()
    con = sqlite3.connect(path)
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript(SCHEMA)
    con.executemany("INSERT INTO item_types VALUES (?,?,?,?,?)", types)
    con.executemany("INSERT INTO characters VALUES (?,?,?,?,?)", chars)
    con.executemany("INSERT INTO items VALUES (?,?,?,?,?,?,?)", items)
    con.executemany("INSERT INTO quest_completions VALUES (?,?,?)", quests)
    con.commit()
    con.close()
    print(f"wrote {path}: {len(types)} item types, {len(chars)} characters, "
          f"{len(items)} items, {len(quests)} quest completions")


if __name__ == "__main__":
    build()

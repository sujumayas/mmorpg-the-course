"""MMO306 Lab 12 starter: a content validator.

    python validate_content.py content/zone_clean.json content/zone_seeded.json
    python -m unittest test_lab12.py

A content file (see content/zone_clean.json) has:
    xp_budget     {"level": most XP one quest at that level may give}
    languages     list of shipped languages
    strings       {language: {string_id: text}}
    npcs          [{"id", "name" (a string id)}]
    items         [{"id"}]
    quests        [{"id", "level", "giver", "requires", "xp", "text", "reward_items"}]
    loot_tables   [{"id", "entries": [{"item", "chance"}]}]

validate() returns a list of (code, record_id, message) triples, one per
problem. Use exactly these codes (the tests check them):

    DUP_ID       an id appears twice in npcs, items, quests or loot_tables
                 (report the id once per extra copy)
    REF_NPC      a quest's giver is not an npc id
    REF_ITEM     a quest reward item or a loot entry item is not an item id
                 (record_id is the quest or the loot table)
    REF_STRING   an npc name or quest text id is missing in any shipped language
    REF_QUEST    a quest requires a quest id that doesn't exist
    XP_BUDGET    a quest gives more XP than its level's budget
    LEVEL_ORDER  a quest requires a quest of a higher level
    CYCLE        a quest is part of a prerequisite cycle (one error per quest in it)
    LOOT_SUM     a loot table's chances add to more than 1 (allow float error!)

When an id is duplicated, use its FIRST record for requirement checks.
"""
import json
import sys


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def validate(content):
    """TODO: return every problem as (code, record_id, message)."""
    raise NotImplementedError("TODO: validate")


if __name__ == "__main__":
    for path in sys.argv[1:]:
        try:
            errs = validate(load(path))
        except NotImplementedError as e:
            print("not done yet:", e)
            break
        print(f"{path}: {len(errs)} error(s)")
        for code, rid, msg in errs:
            print(f"  {code:11s} {rid:10s} {msg}")

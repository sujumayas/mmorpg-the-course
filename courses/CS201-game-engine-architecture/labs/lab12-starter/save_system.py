"""CS201 Lab 12: a save system that survives patches.

You write the parts marked TODO. Everything else is finished.
Run `python save_system.py` for a round-trip demo and `python test_save_system.py` for the checks.
Standard library only.

The world is a list of entity dicts. The CURRENT (version 3) layout is:
    {"uid": int, "kind": str, "health": int, "x": int, "y": int,
     "target": uid or None, "items": [template id strings]}
A save is {"version": 3, "next_uid": int, "entities": [...]}.
"""
import json
import os
import struct
import zlib

CURRENT = 3
MAGIC = b"CS2S"
HEADER = struct.Struct("<4sIII")          # magic, version, payload length, CRC-32


# ---------------------------------------------------------------- shipped migrations (finished)

def v1_to_v2(save):
    """Patch 1.1: entity "hp" renamed to "health"."""
    out = dict(save, entities=[])
    for e in save["entities"]:
        e = dict(e)
        e["health"] = e.pop("hp")
        out["entities"].append(e)
    return out


def v2_to_v3(save):
    """Patch 1.2: tile position "pos": [tx, ty] becomes pixels "x", "y" (16 px tiles)."""
    out = dict(save, entities=[])
    for e in save["entities"]:
        e = dict(e)
        tx, ty = e.pop("pos")
        e["x"], e["y"] = tx * 16, ty * 16
        out["entities"].append(e)
    return out


MIGRATIONS = {1: v1_to_v2, 2: v2_to_v3}


# ---------------------------------------------------------------- part 1: the chain

def upgrade(save, migrations=MIGRATIONS, current=CURRENT):
    """Apply migrations[v], migrations[v+1], ... until the save is at `current`.

    - Do not modify the input dict (the migrations already copy; just don't mutate `save`).
    - After each step set the result's "version" to the new version.
    - Raise ValueError if the save's version is newer than `current`,
      or if a needed migration is missing (message must name the version).
    Return the upgraded save.
    """
    # TODO step 1
    raise NotImplementedError


# ---------------------------------------------------------------- part 2: the file format

def pack(save):
    """Return header + payload bytes. Payload is json.dumps(save, sort_keys=True) in UTF-8.
    Header fields: MAGIC, save["version"], len(payload), zlib.crc32(payload)."""
    # TODO step 2
    raise NotImplementedError


def unpack(blob):
    """Inverse of pack. Raise ValueError with a message containing "magic", "truncated"
    or "checksum" for the matching failure (check in that order). Also raise ValueError
    ("truncated") if the blob is shorter than the header. Return the save dict."""
    # TODO step 2
    raise NotImplementedError


# ---------------------------------------------------------------- part 3: references

class Entity:
    """A runtime entity. `target` is another Entity object or None (a live reference)."""

    def __init__(self, uid, kind, health, x, y, items=()):
        self.uid, self.kind, self.health, self.x, self.y = uid, kind, health, x, y
        self.items = list(items)
        self.target = None


def to_save(entities, next_uid):
    """Serialize runtime entities to a CURRENT-version save dict.
    Each reference is stored as the target's uid (or None). Entities in list order."""
    # TODO step 3
    raise NotImplementedError


def from_save(save):
    """Rebuild runtime entities from a CURRENT-version save with a two-pass load.
    Pass 1 creates every Entity; pass 2 links targets by uid. A target uid that does
    not exist becomes None. Return (entities in save order, next_uid)."""
    # TODO step 3
    raise NotImplementedError


# ---------------------------------------------------------------- part 4: writing safely

def write_save(path, blob):
    """Write blob to `path` without ever leaving a half-written file there.

    1. Write to path + ".tmp", flush, os.fsync.
    2. If `path` already exists, keep it as path + ".bak" (replace any older .bak).
    3. os.replace(path + ".tmp", path).
    """
    # TODO step 4
    raise NotImplementedError


def read_save(path):
    """Load `path` (unpack + upgrade). If that fails with ValueError, try path + ".bak".
    Return (save, source) where source is "main" or "backup". If both fail, raise ValueError."""
    # TODO step 4
    raise NotImplementedError


# ---------------------------------------------------------------- demo (finished)

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    try:
        for name in ("v1.json", "v2.json", "v3.json"):
            with open(os.path.join(here, "golden", name)) as f:
                s = upgrade(json.load(f))
            ents, nxt = from_save(s)
            e = ents[0]
            print(f"{name}: {len(ents)} entities, first = {e.kind} health {e.health} at ({e.x}, {e.y}),"
                  f" targets {e.target.kind if e.target else None}")
    except NotImplementedError:
        print("Finish steps 1 and 3 first.")

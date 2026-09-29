"""Checks for Lab 12. Run from inside lab12-starter: python test_save_system.py"""
import copy
import json
import os
import sys
import tempfile

from save_system import (CURRENT, HEADER, MAGIC, Entity, from_save, pack, read_save,
                         to_save, unpack, upgrade, write_save)

HERE = os.path.dirname(os.path.abspath(__file__))
results = []


def golden(name):
    with open(os.path.join(HERE, "golden", name)) as f:
        return json.load(f)


def check(name):
    def wrap(fn):
        try:
            fn()
            results.append((name, True, ""))
        except Exception as e:  # noqa: BLE001
            results.append((name, False, f"{type(e).__name__}: {e}"))
        return fn
    return wrap


@check("step 1a: every golden save upgrades to the current version")
def _():
    v1 = golden("v1.json")
    before = copy.deepcopy(v1)
    s = upgrade(v1)
    assert v1 == before, "upgrade mutated its input"
    assert s["version"] == CURRENT
    assert s["entities"][0] == {"uid": 100, "kind": "player", "health": 35, "x": 48, "y": 64,
                                "target": 101, "items": ["iron_sword", "bread"]}, s["entities"][0]
    assert upgrade(golden("v2.json"))["entities"][1]["y"] == 112
    assert upgrade(golden("v3.json")) == golden("v3.json")


@check("step 1b: future saves and missing migrations are refused")
def _():
    for bad, kwargs in (({"version": 4, "entities": []}, {}),
                        ({"version": 1, "entities": []}, {"migrations": {2: lambda s: s}})):
        try:
            upgrade(bad, **kwargs)
        except ValueError as e:
            assert str(bad["version"]) in str(e), str(e)
            continue
        raise AssertionError(f"accepted {bad}")


@check("step 2: header round-trip and failure detection")
def _():
    s = upgrade(golden("v1.json"))
    blob = pack(s)
    magic, version, length, crc = HEADER.unpack_from(blob)
    assert magic == MAGIC and version == 3 and length == len(blob) - HEADER.size
    assert unpack(blob) == s
    cases = {"magic": b"XXXX" + blob[4:], "truncated": blob[:-3],
             "checksum": blob[:40] + bytes([blob[40] ^ 4]) + blob[41:]}
    for word, bad in cases.items():
        try:
            unpack(bad)
        except ValueError as e:
            assert word in str(e).lower(), (word, str(e))
            continue
        raise AssertionError(f"{word} not detected")
    try:
        unpack(blob[:10])
    except ValueError as e:
        assert "truncated" in str(e).lower()
    else:
        raise AssertionError("short blob accepted")


@check("step 3a: references survive a save/load round trip, cycles included")
def _():
    p = Entity(1, "player", 30, 0, 0, ["bow"])
    w = Entity(2, "wolf", 8, 16, 0)
    c = Entity(3, "chest", 1, 32, 0, ["gem"])
    p.target, w.target = w, p
    s = to_save([p, w, c], next_uid=4)
    assert s["version"] == CURRENT and s["next_uid"] == 4
    assert s["entities"][0]["target"] == 2 and s["entities"][2]["target"] is None
    ents, nxt = from_save(json.loads(json.dumps(s)))
    assert nxt == 4 and [e.uid for e in ents] == [1, 2, 3]
    assert ents[0].target is ents[1] and ents[1].target is ents[0] and ents[2].target is None
    assert ents[0].items == ["bow"]


@check("step 3b: forward references and dangling targets")
def _():
    ents, _ = from_save(upgrade(golden("v3.json")))
    assert ents[0].target is ents[1]
    assert ents[1].target is None
    ents, _ = from_save(upgrade(golden("v2.json")))
    assert ents[1].target is ents[0]


@check("step 4a: write keeps a backup and leaves no temp file")
def _():
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "slot1.sav")
        a = pack(upgrade(golden("v2.json")))
        b = pack(upgrade(golden("v3.json")))
        write_save(path, a)
        assert not os.path.exists(path + ".bak")
        write_save(path, b)
        with open(path, "rb") as f:
            assert f.read() == b
        with open(path + ".bak", "rb") as f:
            assert f.read() == a
        assert not os.path.exists(path + ".tmp")


@check("step 4b: a damaged main file falls back to the backup")
def _():
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "slot1.sav")
        write_save(path, pack(golden("v1.json")))           # old-format file on disk
        s, src = read_save(path)
        assert src == "main" and s["version"] == CURRENT
        write_save(path, pack(upgrade(golden("v3.json"))))
        with open(path, "r+b") as f:                         # simulate a crash mid-write
            f.truncate(30)
        s, src = read_save(path)
        assert src == "backup" and s["entities"][0]["uid"] == 100
        with open(path + ".bak", "wb") as f:
            f.write(b"garbage")
        try:
            read_save(path)
        except ValueError:
            return
        raise AssertionError("both files bad but no ValueError")


passed = 0
for name, ok, msg in results:
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  ({msg})"))
    passed += ok
print(f"{passed}/{len(results)} checks passed")
sys.exit(0 if passed == len(results) else 1)

"""Checks for CS102 Lab 13. Run from this folder:  python check_lab13.py
Each check prints PASS, FAIL (with the reason) or TODO (function not written yet)."""
import os
import shutil
import tempfile
import time

import loader

results = []


def check(name):
    def wrap(fn):
        try:
            fn()
            results.append(("PASS", name, ""))
        except NotImplementedError as e:
            results.append(("TODO", name, str(e)))
        except AssertionError as e:
            results.append(("FAIL", name, str(e)))
        except Exception as e:  # a crash is a failure too, show what it was
            results.append(("FAIL", name, f"{type(e).__name__}: {e}"))
        return fn
    return wrap


def expect_error(fn, *fragments):
    try:
        fn()
    except ValueError as e:
        msg = str(e)
        missing = [f for f in fragments if f not in msg]
        assert not missing, f"error message lacks {missing}. Message was:\n{msg}"
        return msg
    raise AssertionError("expected a ValueError, but the file loaded")


@check("A1 clean weapons.csv loads with the right numbers")
def _():
    w = loader.load_weapons("weapons.csv")
    for wid in ["short_sword", "gladius", "long_sword", "hand_axe", "war_hammer", "dagger"]:
        assert wid in w, f"missing weapon id '{wid}'"
    assert isinstance(w["long_sword"], loader.Weapon), "values must be Weapon objects"
    assert abs(loader.dps(w["long_sword"]) - 13.2) < 1e-9, "long_sword dps should be 13.2"
    assert w["dagger"].req_str == 0, "blank req_str must become 0"
    assert w["gladius"].upgrade is None, "blank upgrade must become None"
    assert w["short_sword"].upgrade == "gladius"


@check("A2 broken_weapons.csv reports all 7 problems with locations")
def _():
    msg = expect_error(lambda: loader.load_weapons("broken_weapons.csv"),
                       "line 3", "4O", "line 4", "line 5", "sowrd", "line 6",
                       "duplicate", "line 7", "polearm", "attacks_per_sec", "gladus")
    assert msg.count("line 7") >= 2, "line 7 has two problems (type and attacks_per_sec); report both"


@check("A3 crossbow moved from combat_hardcoded.py into weapons.csv")
def _():
    w = loader.load_weapons("weapons.csv")
    assert "crossbow" in w, "add a 'crossbow' row (Part A step 3)"
    c = w["crossbow"]
    assert (c.type, c.min_dmg, c.max_dmg, c.attacks_per_sec, c.req_str) == ("bow", 6, 14, 0.7, 40), \
        f"crossbow numbers do not match combat_hardcoded.py: {c}"


@check("B1 resolve: inheritance, zero is not 'missing', cycles caught")
def _():
    flat = loader.resolve({
        "a": {"hp": 10, "armor": 5, "loot": [1]},
        "b": {"parent": "a", "hp": 20},
        "c": {"parent": "b", "armor": 0, "loot": []},
    })
    assert flat["b"] == {"hp": 20, "armor": 5, "loot": [1]}, f"b resolved to {flat['b']}"
    assert flat["c"]["armor"] == 0 and flat["c"]["loot"] == [], "present 0 / [] must not be inherited"
    assert "parent" not in flat["c"], "remove the 'parent' key after resolving"
    expect_error(lambda: loader.resolve({"x": {"parent": "y"}, "y": {"parent": "x"}}), "x", "y")
    expect_error(lambda: loader.resolve({"x": {"parent": "nobody"}}), "nobody")


@check("B2 clean monsters.json loads and inherits correctly")
def _():
    w = loader.load_weapons("weapons.csv")
    m = loader.load_monsters("monsters.json", w)
    assert m["goblin_brute"]["armor"] == 2, "goblin_brute should inherit armor 2 from goblin"
    assert m["goblin_brute"]["hp"] == 55
    assert len(m["goblin_brute"]["loot"]) == 3, "goblin_brute should inherit goblin's loot"
    assert m["goblin_scout"]["armor"] == 0, "goblin_scout sets armor 0 explicitly; do not inherit 2"


@check("B3 broken_monsters.json reports every problem by id and path")
def _():
    w = loader.load_weapons("weapons.csv")
    expect_error(lambda: loader.load_monsters("broken_monsters.json", w),
                 "shortsword", "loot[2]", "goblin_brute", "hp", "ghost", "wraith", "club")


@check("B4 skeleton moved from combat_hardcoded.py into monsters.json")
def _():
    w = loader.load_weapons("weapons.csv")
    m = loader.load_monsters("monsters.json", w)
    assert "skeleton" in m, "add a 'skeleton' monster (Part B step 6)"
    s = m["skeleton"]
    assert (s["hp"], s["armor"], s["weapon"]) == (40, 4, "crossbow"), f"skeleton is {s}"
    assert sorted((e["item"], e["weight"]) for e in s["loot"]) == [("gold", 70), ("nothing", 30)]


@check("C1 LiveTable reloads good edits and keeps the old table on bad ones")
def _():
    tmp = tempfile.mkdtemp(prefix="cs102_lab13_")
    try:
        path = os.path.join(tmp, "w.csv")
        shutil.copy("weapons.csv", path)
        live = loader.LiveTable(path, loader.load_weapons)
        assert live.poll() is None, "poll() with no change should return None"

        def rewrite(old, new, bump):
            with open(path) as f:
                text = f.read()
            with open(path, "w") as f:
                f.write(text.replace(old, new))
            t = time.time() + bump
            os.utime(path, (t, t))   # make sure the modification time really changes

        rewrite("long_sword,Long Sword,sword,3,19", "long_sword,Long Sword,sword,3,25", 5)
        assert live.poll() is True, "a valid edit should reload and return True"
        assert live.table["long_sword"].max_dmg == 25
        rewrite("long_sword,Long Sword,sword,3,25", "long_sword,Long Sword,sword,3,2X", 10)
        assert live.poll() is False, "an invalid edit should return False"
        assert live.table["long_sword"].max_dmg == 25, "keep the last good table"
        assert live.last_error and "2X" in live.last_error, "store the validation message"
    finally:
        shutil.rmtree(tmp)


if __name__ == "__main__":
    for status, name, detail in results:
        print(f"{status:4}  {name}")
        if status == "FAIL":
            for line in detail.splitlines():
                print(f"        {line}")
    done = sum(s == "PASS" for s, _, _ in results)
    print(f"\n{done} of {len(results)} checks pass")

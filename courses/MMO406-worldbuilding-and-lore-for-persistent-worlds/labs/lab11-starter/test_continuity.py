"""Tests for MMO406 Lab 11. Values come from the week 11 lecture and lab11.md.
Run with `.venv/bin/python test_continuity.py` (from any folder) or pytest.
Every test fails on the starter and passes on a correct continuity.py."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from continuity import blast, contradiction_chance, descendants, resolve, validate  # noqa: E402

LECTURE_IDS = {"F1", "F2", "F3", "F4", "Y1", "Q1", "T1", "I1", "D1", "R1", "Y2", "N1"}


def load():
    with open(os.path.join(HERE, "thornmere_canon.json")) as f:
        return json.load(f)


def lecture_graph():
    """The twelve facts of the lecture table, with the lab's extra dependency removed."""
    facts = [dict(f) for f in load()["facts"] if f["id"] in LECTURE_IDS]
    for f in facts:
        f["depends_on"] = [d for d in f["depends_on"] if d in LECTURE_IDS]
    return facts


def test_descendants_lecture():
    g = lecture_graph()
    assert descendants(g, "F2") == {"F4", "Y1", "D1", "I1", "R1", "Y2"}
    assert descendants(g, "I1") == set()
    assert len(descendants(g, "F1")) == 11


def test_blast_lecture_table():
    g = lecture_graph()
    expected = {"F1": (11, 73.5, ["N1"]), "F2": (6, 58.5, []), "F3": (6, 45.5, ["N1"]),
                "F4": (2, 31.5, []), "D1": (1, 45, []), "I1": (0, 0.5, []),
                "Y1": (1, 11, []), "Q1": (1, 8, ["N1"])}
    for fid, (radius, cost, frozen) in expected.items():
        b = blast(g, fid)
        assert (b["radius"], b["frozen"]) == (radius, frozen), fid
        assert abs(b["cost"] - cost) < 1e-9, fid


def test_blast_full_file_terminates_with_cycle():
    canon = load()["facts"]
    assert blast(canon, "L1") == {"radius": 2, "cost": 4, "frozen": []}
    b = blast(canon, "F1")
    assert b["radius"] == 13 and b["frozen"] == ["C1", "N1"]
    assert abs(b["cost"] - 74.0) < 1e-9


def test_validate_finds_planted_problems():
    assert validate(load()["facts"]) == [("L1", "CYCLE"), ("L2", "CYCLE"), ("T1", "UNKNOWN_DEP")]
    assert validate(lecture_graph()) == []


def test_resolve_by_tier():
    data = load()
    r = resolve(data["facts"], data["tiers"])
    assert r["values"]["drowning_year"] == 912
    assert r["values"]["tidewardens_founded"] == 941
    assert r["values"]["archive_flooded"] == 915
    assert r["values"]["harrow_death_year"] == 941
    assert "signet_metal" not in r["values"]
    assert r["overridden"] == [("C1", "archive_flooded"), ("N1", "tidewardens_founded"),
                               ("X1", "drowning_year")]
    assert r["unresolved"] == ["signet_metal"]


def test_resolve_rejects_unknown_tier():
    data = load()
    data["facts"][0]["tier"] = "rumour"
    try:
        resolve(data["facts"], data["tiers"])
    except ValueError:
        return
    raise AssertionError("resolve accepted an unknown tier")


def test_contradiction_chance():
    assert abs(contradiction_chance(0.02, 50) - 0.63583) < 1e-4
    assert abs(contradiction_chance(0.002, 50) - 0.09525) < 1e-4
    assert contradiction_chance(0.0, 100) == 0.0


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"PASS {name}")
            except NotImplementedError as e:
                failed += 1
                print(f"TODO {name}: {e}")
            except AssertionError:
                failed += 1
                print(f"FAIL {name}")
    print(f"\n{failed} test(s) not passing" if failed else "\nAll tests pass.")
    sys.exit(1 if failed else 0)

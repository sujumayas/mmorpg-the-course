"""Tests for CS101 Lab 06. Run: python test_lab06.py (from this folder)."""
import copy
import itemdb as m

ORIGINAL = m.load_json("items_original.json")
IDS_V1 = m.load_json("ids_v1.json")
SAVE_V1 = m.load_json("save_v1.json")


def test_validate_finds_the_three_errors():
    problems = m.validate(ORIGINAL)
    keys = sorted({p.split(":")[0] for p in problems})
    assert keys == ["arrow", "bronze_sword", "leather_cap"], keys
    assert len(problems) == 3, problems


def test_validate_small_cases():
    assert m.validate({}) == []
    ok = {"x": {"name": "X", "type": "tool", "stack": 1, "price": 0}}
    assert m.validate(ok) == []
    assert len(m.validate({"y": {"type": "weapon", "stack": 1, "price": 5}})) == 2   # name, damage


def test_your_items_json_is_fixed():
    assert m.validate(m.load_json("items.json")) == [], "fix the three errors in items.json"


def test_find_and_aliases():
    assert m.find(ORIGINAL, "potion")["heal"] == 12
    assert m.find(ORIGINAL, "short_sword")["name"] == "Wooden Sword"
    try:
        m.find(ORIGINAL, "laser_sword")
    except KeyError:
        pass
    else:
        raise AssertionError("unknown key must raise KeyError")


def test_items_of_type():
    assert m.items_of_type(ORIGINAL, "weapon") == ["bronze_sword", "iron_sword", "wooden_sword"]
    assert m.items_of_type(ORIGINAL, "consumable") == ["bread", "potion"]
    assert m.items_of_type(ORIGINAL, "spell") == []


def test_total_value():
    assert m.total_value([("potion", 3), None, ("iron_sword", 1)], ORIGINAL) == 105
    assert m.total_value([None, None], ORIGINAL) == 0
    assert m.total_value([("arrow", 40), ("bread", 5)], ORIGINAL) == 50


def test_migrate_save():
    before = copy.deepcopy(SAVE_V1)
    new = m.migrate_save(SAVE_V1, IDS_V1)
    assert new["version"] == 2 and new["gold"] == 42
    assert new["slots"] == [["iron_sword", 1], ["potion", 3], None, ["arrow", 40], ["torch", 5]]
    assert SAVE_V1 == before, "migrate_save must not modify the old save"


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
            passed += 1
        except NotImplementedError:
            print(f"FAIL  {t.__name__}: not implemented yet")
        except AssertionError as e:
            print(f"FAIL  {t.__name__}: {e or 'assertion failed'}")
    print(f"\n{passed}/{len(tests)} tests passed")
    raise SystemExit(0 if passed == len(tests) else 1)

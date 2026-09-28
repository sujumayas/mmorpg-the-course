"""Tests for CS101 Lab 05. Run: python test_lab05.py"""
import inventory as m


def full_but_not_full():
    """Slots 0-34 alternate dirt 64 and pickaxe 1; slot 35 holds cobblestone 50."""
    inv = m.make_inventory()
    for i in range(35):
        inv[i] = ("dirt", 64) if i % 2 == 0 else ("pickaxe", 1)
    inv[35] = ("cobblestone", 50)
    return inv


def test_count_item():
    inv = [("gem", 8), None, ("gem", 3), ("coin", 5)]
    before = list(inv)
    assert m.count_item(inv, "gem") == 11
    assert m.count_item(inv, "bone") == 0
    assert inv == before, "count_item must not change the list"


def test_room_for():
    inv = full_but_not_full()
    assert None not in inv
    assert m.room_for(inv, "cobblestone", 64) == 14
    assert m.room_for(inv, "dirt", 64) == 0
    assert m.room_for(m.make_inventory(), "pearl", 16) == 576
    assert m.room_for(m.make_inventory(), "pickaxe", 1) == 36


def test_add_tops_up_before_new_stacks():
    inv = m.make_inventory(12)
    inv[1] = ("arrow", 60)
    inv[3] = ("arrow", 10)
    left = m.add_item(inv, "arrow", 70, 64)
    assert left == 0
    assert inv[1] == ("arrow", 64) and inv[3] == ("arrow", 64)
    assert inv[9] == ("arrow", 12), "pass 2 must use storage (index 9) first"
    assert inv[0] is None


def test_add_hotbar_after_storage():
    inv = m.make_inventory()
    for i in m.STORAGE:
        inv[i] = ("pickaxe", 1)
    left = m.add_item(inv, "sword", 3, 1)
    assert left == 0
    assert inv[0:3] == [("sword", 1)] * 3 and inv[3] is None


def test_full_but_not_full():
    inv = full_but_not_full()
    assert m.add_item(inv, "cobblestone", 20, 64) == 6
    assert inv[35] == ("cobblestone", 64)
    assert m.add_item(inv, "cobblestone", 5, 64) == 5
    assert m.add_item(inv, "dirt", 3, 64) == 3


def test_add_exact_fit_and_zero():
    inv = m.make_inventory(2)
    assert m.add_item(inv, "potion", 32, 16) == 0
    assert inv == [("potion", 16), ("potion", 16)]
    assert m.add_item(inv, "potion", 0, 16) == 0
    assert m.add_item(inv, "potion", 1, 16) == 1


def test_remove_item():
    inv = [("potion", 16), None, ("potion", 5), ("arrow", 3)]
    assert m.remove_item(inv, "potion", 7) == 7
    assert inv == [("potion", 14), None, None, ("arrow", 3)], "take from the highest index first"
    assert m.remove_item(inv, "arrow", 10) == 3
    assert inv[3] is None
    assert m.remove_item(inv, "bone", 1) == 0


def test_sort_returns_new_list():
    inv = [None, ("potion", 2), ("arrow", 5), None, ("arrow", 64)]
    before = list(inv)
    out = m.sort_inventory(inv)
    assert out == [("arrow", 64), ("arrow", 5), ("potion", 2), None, None]
    assert inv == before, "sort_inventory must not change the original"
    assert out is not inv


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

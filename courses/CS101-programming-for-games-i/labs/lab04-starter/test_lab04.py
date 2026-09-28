"""Tests for CS101 Lab 04. Run: python test_lab04.py
Each test prints PASS or FAIL. A NotImplementedError counts as FAIL."""
import combat as c

HERO = {"atk": 9, "bonus": 4, "armor": 2, "def": 12}
RAT = {"atk": 6, "bonus": 2, "armor": 1, "def": 11}


def test_attack_hits_edges():
    assert c.attack_hits(20, -100, 99) is True      # natural 20 always hits
    assert c.attack_hits(1, 100, 0) is False        # natural 1 always misses
    assert c.attack_hits(7, 4, 11) is True          # 7 + 4 == 11, meets defense
    assert c.attack_hits(6, 4, 11) is False         # one short
    assert c.attack_hits(2, 9, 11) is True          # lowest normal roll can hit


def test_damage_floor_and_crit():
    assert c.damage(9, 1) == 8
    assert c.damage(9, 1, crit=True) == 16
    assert c.damage(3, 5) == 1                      # floor at 1
    assert c.damage(3, 5, crit=True) == 2           # floor, then double
    assert c.damage(5, 5) == 1


def test_apply_damage_edges():
    assert c.apply_damage(10, 3) == 7
    assert c.apply_damage(3, 3) == 0
    assert c.apply_damage(2, 9) == 0                # never negative
    assert c.apply_damage(0, 0) == 0


def test_drink_potion():
    assert c.drink_potion(10, 30, 2) == (22, 1)
    assert c.drink_potion(25, 30, 1) == (30, 0)     # capped at max
    assert c.drink_potion(30, 30, 1) == (30, 0)     # wasted but still used
    assert c.drink_potion(10, 30, 0) == (10, 0)     # none left, no change
    assert c.drink_potion(10, 30, 2, heal_amount=5) == (15, 1)


def test_is_defeated_boundary():
    assert c.is_defeated(0) is True                 # the tangled loop gets this wrong
    assert c.is_defeated(1) is False
    assert c.is_defeated(-3) is True


def test_resolve_attack():
    assert c.resolve_attack(1, HERO, RAT) == 0      # natural 1
    assert c.resolve_attack(6, HERO, RAT) == 0      # 6 + 4 = 10 < 11
    assert c.resolve_attack(7, HERO, RAT) == 8      # 9 - 1
    assert c.resolve_attack(20, HERO, RAT) == 16    # crit
    assert c.resolve_attack(10, RAT, HERO) == 4     # 10 + 2 = 12 meets 12, 6 - 2


def test_functions_are_pure():
    import builtins
    real_print, real_input = builtins.print, builtins.input
    calls = []
    builtins.print = lambda *a, **k: calls.append("print")
    builtins.input = lambda *a, **k: calls.append("input") or "a"
    try:
        c.attack_hits(10, 4, 12); c.damage(9, 1); c.apply_damage(5, 2)
        c.drink_potion(5, 30, 1); c.is_defeated(0); c.resolve_attack(10, HERO, RAT)
    finally:
        builtins.print, builtins.input = real_print, real_input
    assert calls == [], f"Part B functions must not print or ask for input: {calls}"


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

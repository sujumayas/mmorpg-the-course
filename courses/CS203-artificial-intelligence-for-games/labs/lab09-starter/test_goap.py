"""Tests for Lab 09. Values come from the week 9 lecture.
Run with `python3 test_goap.py` or `pytest test_goap.py`."""
from goap import (ACTIONS, DOOR_ACTIONS, GOAL, apply, execute, plan, satisfied,
                  unmet, world)


def test_satisfied_and_apply():
    s = {"a": True}
    assert satisfied(s, {"a": True})
    assert satisfied(s, {"b": False})            # missing counts as False
    assert not satisfied(s, {"b": True})
    t = apply(s, {"b": True})
    assert t == {"a": True, "b": True} and s == {"a": True}   # s unchanged


def test_unmet():
    assert unmet({}, {"x": True, "y": True}) == 2
    assert unmet({"x": True}, {"x": True, "y": True}) == 1


def test_lecture_open_world():
    assert plan(world(True, True, True), GOAL) == (4, ["GoToCover", "AttackFromCover"], 2)


def test_all_eight_worlds():
    expected = {
        (1, 1, 1): (4, ["GoToCover", "AttackFromCover"]),
        (1, 1, 0): (6, ["AttackInOpen"]),
        (1, 0, 1): (4, ["GoToCover", "AttackFromCover"]),
        (1, 0, 0): (6, ["AttackInOpen"]),
        (0, 1, 1): (6, ["GoToCover", "Reload", "AttackFromCover"]),
        (0, 1, 0): (7, ["Charge", "Melee"]),
        (0, 0, 1): (7, ["Charge", "Melee"]),
        (0, 0, 0): (7, ["Charge", "Melee"]),
    }
    for (l, a, c), (cost, steps) in expected.items():
        got_cost, got_steps, _ = plan(world(bool(l), bool(a), bool(c)), GOAL)
        assert (got_cost, got_steps) == (cost, steps), (l, a, c)


def test_cost_is_personality():
    reckless = [(n, 3 if n == "AttackInOpen" else c, p, e) for n, c, p, e in ACTIONS]
    assert plan(world(True, True, True), GOAL, reckless)[:2] == (3, ["AttackInOpen"])


def test_no_plan_without_attacks():
    unarmed = [x for x in ACTIONS if x[0] not in ("AttackFromCover", "AttackInOpen", "Melee")]
    assert plan(world(True, True, True), GOAL, unarmed) == (None, [], 4)


def test_orkin_pizza_example():
    alma = [("OrderPizza", 2, {"has_phone_number": True}, {"hungry": False}),
            ("BakePie", 8, {"has_recipe": True}, {"hungry": False})]
    goal = {"hungry": False}
    both = {"hungry": True, "has_phone_number": True, "has_recipe": True}
    assert plan(both, goal, alma)[:2] == (2, ["OrderPizza"])
    assert plan({"hungry": True, "has_recipe": True}, goal, alma)[:2] == (8, ["BakePie"])
    assert plan({"hungry": True}, goal, alma)[:2] == (None, [])


def test_door_replanning():
    fails = {"OpenDoor": {"door_jammed": True}, "KickDoor": {"door_barred": True}}
    attempted, plans, state = execute({}, {"in_room": True}, DOOR_ACTIONS, fails)
    assert attempted == ["OpenDoor", "KickDoor", "DiveThroughWindow"]
    assert plans == 3 and state["in_room"]
    assert execute({}, {"in_room": True}, DOOR_ACTIONS, {})[:2] == (
        ["OpenDoor", "WalkThroughDoor"], 1)


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
    print(f"\n{failed} test(s) not passing" if failed else "\nall tests pass")
    raise SystemExit(1 if failed else 0)

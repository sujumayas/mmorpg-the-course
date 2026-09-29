"""Tests for Lab 08. Values come from the week 8 lecture's table of four zone shapes.
Run with ../../../../.venv/bin/python test_quest_graph.py (or pytest)."""
from quest_graph import layers, load_zones, order_control, trips, width, zone_minutes

Z = load_zones()


def test_layers_small():
    z = {"a": set(), "b": {"a"}, "c": {"a"}, "d": {"b", "c"}}
    assert layers(z) == [["a"], ["b", "c"], ["d"]]


def test_trips_and_width():
    want = {"linear": (9, 1), "strands": (3, 3), "braided": (5, 3), "flat": (1, 9),
            "waves": (3, 3)}
    for name, (t, w) in want.items():
        assert (trips(Z[name]), width(Z[name])) == (t, w), name


def test_order_control():
    want = {"linear": 36 / 36, "strands": 9 / 36, "braided": 30 / 36, "flat": 0.0,
            "waves": 27 / 36}
    for name, c in want.items():
        assert abs(order_control(Z[name]) - c) < 1e-9, name
    assert order_control({"solo": set()}) == 1.0


def test_zone_minutes():
    want = {"linear": 63, "strands": 39, "braided": 47, "flat": 31, "waves": 39}
    for name, m in want.items():
        assert abs(zone_minutes(Z[name], 3, 4) - m) < 1e-9, name


def test_cycle_and_missing():
    for bad in ({"a": {"b"}, "b": {"a"}}, {"a": {"ghost"}}):
        try:
            layers(bad)
        except ValueError:
            continue
        raise AssertionError(f"expected ValueError for {bad}")


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print("PASS", name)
            except Exception as e:  # noqa: BLE001
                failed += 1
                print("FAIL", name, type(e).__name__, e)
    raise SystemExit(1 if failed else 0)

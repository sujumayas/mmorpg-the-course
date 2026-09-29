"""Tests for Lab 07. Values come from the week 7 lecture.
Run with `python3 test_bt.py` or `pytest test_bt.py`."""
from bt import (FAILURE, RUNNING, SUCCESS, Action, Condition, Inverter,
                Selector, Sequence, guard, run)


class Fixed:
    """A leaf that always returns the same status and counts its ticks."""

    def __init__(self, status):
        self.status, self.ticks = status, 0

    def tick(self, bb):
        self.ticks += 1
        return self.status

    def halt(self):
        pass


def test_selector_returns_first_non_failure():
    a, b, c = Fixed(FAILURE), Fixed(SUCCESS), Fixed(SUCCESS)
    assert Selector([a, b, c], "reactive").tick({}) == SUCCESS
    assert (a.ticks, b.ticks, c.ticks) == (1, 1, 0)
    assert Selector([Fixed(FAILURE), Fixed(FAILURE)], "reactive").tick({}) == FAILURE


def test_sequence_returns_first_non_success():
    a, b, c = Fixed(SUCCESS), Fixed(RUNNING), Fixed(SUCCESS)
    assert Sequence([a, b, c], "reactive").tick({}) == RUNNING
    assert (a.ticks, b.ticks, c.ticks) == (1, 1, 0)
    assert Sequence([Fixed(SUCCESS), Fixed(SUCCESS)], "reactive").tick({}) == SUCCESS


def test_memory_sequence_skips_finished_steps():
    first, second = Action("A", 1), Action("B", 3)
    seq = Sequence([first, second], "memory")
    bb = {}
    assert seq.tick(bb) == RUNNING and bb["acted"] == "B"
    seq.tick(bb)
    assert first.done == 0 and second.done == 2        # A was not re-run


def test_hybrid_sequence_rechecks_conditions():
    seq = Sequence([Condition("ok"), Action("Work", 5)], "hybrid")
    assert seq.tick({"ok": True}) == RUNNING
    assert seq.tick({"ok": False}) == FAILURE          # the guard condition wins
    mem = Sequence([Condition("ok"), Action("Work", 5)], "memory")
    mem.tick({"ok": True})
    assert mem.tick({"ok": False}) == RUNNING          # memory mode never looks back


def test_inverter():
    assert Inverter(Fixed(SUCCESS)).tick({}) == FAILURE
    assert Inverter(Fixed(FAILURE)).tick({}) == SUCCESS
    assert Inverter(Fixed(RUNNING)).tick({}) == RUNNING


def test_lecture_trace_reactive():
    acted = [a for a, _ in run(guard("reactive"))]
    assert acted == ["Patrol", "Patrol", "GoToNoise", "LookAround", "GoToNoise",
                     "Chase", "Chase", "Shoot", "Shoot",
                     "RunToSafety", "RunToSafety", "RunToSafety"]


def test_lecture_trace_memory():
    acted = [a for a, _ in run(guard("memory"))]
    assert acted == ["Patrol", "Patrol", "Patrol", "Patrol", "GoToNoise",
                     "LookAround", "LookAround", "Shoot", "Shoot",
                     "Shoot", "Shoot", "Shoot"]


def test_lecture_trace_hybrid():
    acted = [a for a, _ in run(guard("hybrid"))]
    assert acted == ["Patrol", "Patrol", "GoToNoise", "LookAround", "LookAround",
                     "Chase", "Chase", "Shoot", "Shoot",
                     "RunToSafety", "RunToSafety", "RunToSafety"]


def test_lecture_visit_counts():
    assert [v for _, v in run(guard("reactive"))] == [8, 8, 8, 9, 8, 9, 9, 9, 9, 4, 4, 4]
    assert sum(v for _, v in run(guard("memory"))) == 58
    assert sum(v for _, v in run(guard("hybrid"))) == 89


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

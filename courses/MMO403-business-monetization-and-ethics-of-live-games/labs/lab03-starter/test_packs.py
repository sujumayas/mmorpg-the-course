"""Tests for Lab 03. Values come from the week 3 lecture, section 2.
Run with `python3 test_packs.py` or `pytest test_packs.py`."""
import os

from packs import PACKS, audit, cheapest_cover, load_packs, reference_cents, sequence

HERE = os.path.dirname(os.path.abspath(__file__))


def test_lecture_table():
    rows = {r["price"]: r for r in audit(PACKS, [800, 1_200, 1_500, 2_000, 2_800])}
    assert (rows[800]["cents"], rows[800]["leftover"]) == (999, 200)
    assert (rows[1_200]["cents"], rows[1_200]["leftover"]) == (1_998, 800)
    assert (rows[1_500]["cents"], rows[1_500]["leftover"]) == (1_998, 500)
    assert (rows[2_000]["cents"], rows[2_000]["leftover"]) == (1_998, 0)
    assert (rows[2_800]["cents"], rows[2_800]["leftover"]) == (2_499, 0)


def test_reference():
    assert reference_cents(PACKS, 800) == 799
    assert reference_cents(PACKS, 1_200) == 1_199
    assert reference_cents(PACKS, 2_800) == 2_797


def test_counts_and_balance():
    assert cheapest_cover(PACKS, 1_200) == (1_998, (2, 0, 0, 0), 800)
    assert cheapest_cover(PACKS, 800, balance=800) == (0, (0, 0, 0, 0), 0)
    assert cheapest_cover(PACKS, 800, balance=500) == (999, (1, 0, 0, 0), 700)


def test_big_item_uses_bulk():
    cents, counts, left = cheapest_cover(PACKS, 5_000)
    assert cents == 3_999 and counts == (0, 0, 1, 0) and left == 0


def test_tie_prefers_more_currency():
    packs = [(100, 100), (250, 200)]
    # 200 cents buys either 2 x 100 or 1 x 250; both cover 200, prefer 250.
    assert cheapest_cover(packs, 200) == (200, (0, 1), 50)


def test_sequence():
    # 1,200 then 800: the second item is paid from the 800 leftover.
    assert sequence(PACKS, [1_200, 800]) == (1_998, 0)
    # 1,500 then 800: the 500 leftover is not enough, one more pack.
    assert sequence(PACKS, [1_500, 800]) == (2_997, 700)


def test_flat_store():
    flat = load_packs(os.path.join(HERE, "flat_store.csv"))
    rows = audit(flat, [700, 800])
    assert rows[0]["cents"] == 1_000 and rows[0]["leftover"] == 100
    assert abs(rows[1]["markup"] - 1.0) < 1e-9


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

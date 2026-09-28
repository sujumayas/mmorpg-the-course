"""CS101 lab 13 tests. Run: python test_lab13.py

Plain asserts, no packages. Each test prints PASS or FAIL with a reason.
"""
import math
import random

import randomizers as R
import spawner as S


def test_same_seed_same_sequence():
    a = R.take(R.pure_random(random.Random(42)), 50)
    b = R.take(R.pure_random(random.Random(42)), 50)
    c = R.take(R.pure_random(random.Random(43)), 50)
    assert a == b, "same seed gave different sequences"
    assert a != c, "different seeds gave the same sequence"


def test_gaps_between():
    assert R.gaps_between("IJJIOI") == [2, 1], R.gaps_between("IJJIOI")
    assert R.gaps_between("IIJI") == [0, 1], R.gaps_between("IIJI")
    assert R.gaps_between("JJOS") == [], "no I pieces means no gaps"


def test_nes_repeat_rate():
    seq = R.take(R.nes_style(random.Random(1)), 70_000)
    rate = R.repeat_rate(seq)
    # Model: P(repeat) = 2/8 * 1/7 = 1/28 = 0.0357
    assert 0.030 < rate < 0.042, f"repeat rate {rate:.4f}, expected about 0.0357"
    assert set(seq) == set(R.PIECES), "some piece never appeared"


def test_nes_is_seeded():
    a = R.take(R.nes_style(random.Random(5)), 30)
    b = R.take(R.nes_style(random.Random(5)), 30)
    assert a == b, "nes_style is not reproducible from its seed"


def test_bag_blocks_are_permutations():
    seq = R.take(R.seven_bag(random.Random(2)), 7 * 500)
    for i in range(0, len(seq), 7):
        block = seq[i:i + 7]
        assert sorted(block) == sorted(R.PIECES), f"bag {i // 7} is {block}"


def test_bag_max_drought():
    seq = R.take(R.seven_bag(random.Random(3)), 70_000)
    gaps = R.gaps_between(seq)
    assert gaps, "gaps_between returned nothing"
    assert max(gaps) <= 12, f"drought of {max(gaps)} is impossible for a 7-bag"


def test_spawn_respects_safe_radius():
    rng = random.Random(9)
    for _ in range(2000):
        x, y, tries = S.spawn_position(rng, 400, 300)
        assert x is not None, "gave up although most of the arena is safe"
        assert math.hypot(x - 400, y - 300) >= S.SAFE_RADIUS, (x, y)
        assert 1 <= tries <= S.MAX_ATTEMPTS, tries


def test_spawn_gives_up():
    rng = random.Random(9)
    x, y, tries = S.spawn_position(rng, 400, 300, safe=2000, attempts=5)
    assert x is None and y is None, "a 2000 px radius covers the whole arena"
    assert tries == 5, f"should report 5 tries, got {tries}"


def test_spawn_mean_tries():
    rng = random.Random(11)
    tries = [S.spawn_position(rng, 400, 300)[2] for _ in range(20_000)]
    mean = sum(tries) / len(tries)
    # Model: accept chance p = 1 - pi*150^2/(800*600) = 0.8527, mean tries 1/p = 1.173
    assert 1.14 < mean < 1.21, f"mean tries {mean:.3f}, expected about 1.173"


TESTS = [v for k, v in sorted(globals().items()) if k.startswith("test_")]

if __name__ == "__main__":
    passed = 0
    for t in TESTS:
        try:
            t()
            print(f"PASS {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL {t.__name__}: {e}")
    print(f"{passed}/{len(TESTS)} tests passed")

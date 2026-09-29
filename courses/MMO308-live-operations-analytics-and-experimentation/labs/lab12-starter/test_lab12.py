"""Checks for Lab 12. Run from inside lab12-starter/:  ../../../../.venv/bin/python test_lab12.py
Every check fails on the starter and passes on a correct solution."""
import alarms as m

passed = failed = 0


def check(name, fn):
    global passed, failed
    try:
        fn()
        passed += 1
        print("PASS", name)
    except Exception as e:  # noqa: BLE001
        failed += 1
        print("FAIL", name, "-", type(e).__name__, e)


LECTURE_Z = [0.3, -0.5, 0.8, 0.8, 1.4, -0.1, 1.6, 1.2, 0.6, 1.9, 1.1, 0.6, 1.7, 1.5]
LECTURE_S = [0.0, 0.0, 0.3, 0.6, 1.5, 0.9, 2.0, 2.7, 2.8, 4.2, 4.8, 4.9, 6.1, 7.1]


def t_cusum_lecture():
    scores, first = m.cusum(LECTURE_Z, k=0.5, h=5.0)
    assert [round(s, 1) for s in scores] == LECTURE_S, scores
    assert first == 12, first  # day 13


def t_cusum_mirror_and_k():
    _, first = m.cusum([-2.0, -2.0, -2.0, -2.0], k=0.5, h=5.0, direction=-1)
    assert first == 3, first
    _, first = m.cusum([2.0] * 4, k=0.5, h=5.0, direction=-1)
    assert first is None
    _, first = m.cusum(LECTURE_Z, k=1.0, h=5.0)
    assert first is None


def t_baseline():
    v = list(range(1, 36))  # 35 days: values 1..35
    assert m.weekday_baseline(v, 28) == (22 + 15 + 8 + 1) / 4
    assert m.weekday_baseline(v, 28, weeks=2) == (22 + 15) / 2
    assert m.weekday_baseline(v, 28, weeks=2, skip={21}) == (15 + 8) / 2
    assert m.weekday_baseline(v, 10, weeks=4) == 4.0  # only one earlier same weekday exists
    try:
        m.weekday_baseline(v, 3)
    except ValueError:
        pass
    else:
        raise AssertionError("no earlier same weekday must raise ValueError")


def t_sigma_spike_z():
    assert abs(m.robust_sigma([1, 2, 3, 4, 100]) - 1.4826) < 1e-9
    assert m.spike_alarms([0.5, 3.2, 2.9, 3.0, 4.1]) == [1, 4]
    assert m.zscores([10, 12, 7], [10, None, 9], 2.0) == [0.0, None, -1.0]


for name, fn in [("CUSUM reproduces the lecture table", t_cusum_lecture),
                 ("mirror CUSUM and the allowance k", t_cusum_mirror_and_k),
                 ("same-weekday baseline with skips", t_baseline),
                 ("robust sigma, spikes and z-scores", t_sigma_spike_z)]:
    check(name, fn)
print(f"{passed} passed, {failed} failed")
raise SystemExit(1 if failed else 0)

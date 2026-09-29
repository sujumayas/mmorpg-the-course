"""Checks for Lab 12. Run from inside lab12-starter/:  ../../../../.venv/bin/python test_lab12.py
Every check fails on the starter and passes on a correct solution."""
import sys

from make_accounts import make_accounts
import policy as m

passed = failed = 0
rows = make_accounts()


def check(name, fn):
    global passed, failed
    try:
        fn()
        passed += 1
        print("PASS", name)
    except Exception as e:  # noqa: BLE001
        failed += 1
        print("FAIL", name, "-", type(e).__name__, e)


def t_lecture():
    assert abs(m.posterior(0.01, [90]) - 0.4762) < 1e-4
    assert abs(m.posterior(0.01, [90, 10]) - 0.9009) < 1e-4
    assert abs(m.posterior(0.01, [90, 10, 600]) - 0.9998) < 1e-4
    assert abs(m.threshold(20) - 20 / 21) < 1e-12
    ladder = {"24 h trade lock": 1, "7-day suspension": 5, "permanent ban": 20}
    assert m.allowed(0.4762, ladder) == []
    assert m.allowed(0.9009, ladder) == ["24 h trade lock", "7-day suspension"]


def t_rates():
    tpr, fpr = m.rates(rows, "aim")
    assert 0.88 < tpr < 0.92 and 0.008 < fpr < 0.012, (tpr, fpr)
    tpr, fpr = m.rates(rows, "hash")
    assert 0.55 < tpr < 0.65 and 0.0005 < fpr < 0.0015, (tpr, fpr)


def t_dependence():
    h = m.dependence(rows, "aim", "reports", False)
    c = m.dependence(rows, "aim", "reports", True)
    assert 5.0 < h < 7.5, h
    assert 0.9 < c < 1.2, c
    assert 0.5 < m.dependence(rows, "aim", "hash", True) < 1.5


def t_rule_rates():
    tp, fp = m.rule_rates(rows, ["aim"])
    assert 8000 < tp < 9500 and 8500 < fp < 11000, (tp, fp)
    tp, fp = m.rule_rates(rows, ["aim", "reports"])
    assert fp > 4 * 495, fp


for n, f in [("lecture numbers", t_lecture), ("rates", t_rates), ("dependence", t_dependence),
             ("rule_rates", t_rule_rates)]:
    check(n, f)
print(f"{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)

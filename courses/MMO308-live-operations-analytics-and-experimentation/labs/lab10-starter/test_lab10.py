"""Checks for Lab 10. Run from inside lab10-starter/:  ../../../../.venv/bin/python test_lab10.py
Every check fails on the starter and passes on a correct solution."""
import feedback as m

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


def close(a, b, tol=1e-6):
    assert abs(a - b) <= tol, f"{a} != {b}"


TOY = [dict(hours_7d=2.0, sessions_7d=2, approve=1), dict(hours_7d=2.0, sessions_7d=2, approve=0),
       dict(hours_7d=8.0, sessions_7d=5, approve=1), dict(hours_7d=25.0, sessions_7d=12, approve=0)]


def t_raw():
    close(m.raw_share(TOY), 0.5)


def t_ipw_toy():
    # weights 0.5, 0.5, 0.125, 0.04 -> 0.625 / 1.165
    close(m.ipw_share(TOY, "hours_7d"), 0.625 / 1.165)
    # weights 0.5, 0.5, 0.2, 1/12
    close(m.ipw_share(TOY, "sessions_7d"), 0.7 / (1.2 + 1 / 12))


def t_neff_lecture():
    close(m.kish_neff([1.0] * 7), 7.0)
    w = [1 / 2] * 197 + [1 / 8] * 393 + [1 / 25] * 410  # the lecture's 1,000 respondents
    close(round(m.kish_neff(w), 1), 480.0)


def t_capture():
    a = {f"x{i}" for i in range(240)}
    b = {f"x{i}" for i in range(192, 792)}  # 600 accounts, 48 shared with a
    close(m.lincoln_petersen(a, b), 3000.0)
    close(m.chapman(a, b), 241 * 601 / 49 - 1)
    try:
        m.lincoln_petersen({"p"}, {"q"})
    except ValueError:
        pass
    else:
        raise AssertionError("no overlap must raise ValueError")


def t_survey_data():
    rows = m.read_survey()
    raw, ipw = m.raw_share(rows), m.ipw_share(rows, "hours_7d")
    assert 0.40 < raw < 0.48, raw
    assert abs(ipw - 0.6152) < 0.02, f"weighted {ipw:.4f} should be within 2 points of the true 61.5%"


for name, fn in [("raw share", t_raw), ("ipw on toy rows", t_ipw_toy),
                 ("Kish n_eff reproduces the lecture's 480", t_neff_lecture),
                 ("capture-recapture reproduces the lecture's 3,000", t_capture),
                 ("weighted survey recovers the true approval", t_survey_data)]:
    check(name, fn)
print(f"{passed} passed, {failed} failed")
raise SystemExit(1 if failed else 0)

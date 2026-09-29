"""Checks for Lab 11. Run from inside lab11-starter/:  ../../../../.venv/bin/python test_lab11.py
Every check fails on the starter and passes on a correct solution. Random checks use large
samples and tolerances, so any correct implementation passes."""
import random
import statistics as st
import sys

import dupe_response as m
from make_log import T_OBS, incident_log

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


def close(x, y, tol):
    assert abs(x - y) <= tol, f"{x} vs {y}"


def t_closed():
    # (T, rollback hours, trace hours, trace inflation %, ring-only inflation %, trace harm, keeps)
    lecture = [(1 / 3, 1333, 967, 0.26, 0.64, 6127, 3.2e6), (1, 4000, 2719, 0.73, 1.81, 17221, 9.1e6),
               (6, 24000, 10482, 2.80, 6.99, 66387, 34.9e6), (24, 96000, 14877, 3.97, 9.92, 94218, 49.6e6)]
    for T, rh, th, ti, oi, harm, keeps in lecture:
        r, t, o = (m.respond(pol, T) for pol in ("rollback", "trace", "ring_only"))
        close(r["hours"], rh, 1); close(r["inflation"], 0, 1e-9); close(r["harm"], rh, 1); close(r["keeps"], 0, 1e-6)
        close(t["hours"], th, 1); close(t["inflation"], ti, 0.006); close(t["harm"], harm, 1)
        close(t["keeps"], keeps, 0.06e6); close(o["inflation"], oi, 0.006); close(o["hours"], 0, 1e-9)


def t_crossover():
    close(m.crossover(), 23.54, 0.011)
    close(m.crossover(dict(m.PARAMS, k=0.05)), 7.09, 0.011)
    close(m.crossover(dict(m.PARAMS, b=0.8)), 14.11, 0.011)
    assert m.crossover(dict(m.PARAMS, P=100_000)) is not None
    assert m.crossover(dict(m.PARAMS, P=1_000), T_max=48) is None


def t_refund_and_ban():
    r = m.respond("trace_refund", 6, wallet=20e6)
    close(r["hours"], 482, 1); close(r["keeps"], 14.94e6, 0.01e6); close(r["inflation"], 2.80, 0.006)
    close(m.respond("trace_refund", 6, wallet=1e9)["hours"], 0, 1e-6)
    close(m.respond("trace_refund", 6)["hours"], m.respond("trace", 6)["hours"], 1e-6)
    close(m.ring_net("trace", 6, 30e6), 4.94e6, 0.01e6)
    close(m.ring_net("trace_refund", 6, 30e6, wallet=20e6), -15.06e6, 0.01e6)
    assert m.ring_net("rollback", 0.5, 1.0) < 0


def t_simulate():
    rng = random.Random(3)
    runs = [m.simulate(rng, 6) for _ in range(20)]
    moved = 1 - 2.718281828459045 ** -1.2
    for key, share in [("held", 1 - moved), ("bought", 0.6 * moved), ("gone", 0.4 * moved)]:
        close(st.mean(r[key] for r in runs), 50_000 * share, 0.01 * 50_000 * share)
    assert all(r["held"] + r["bought"] + r["gone"] == 50_000 for r in runs)


def t_estimate():
    k, b = m.estimate(incident_log(), T_OBS)
    close(k, 0.15, 0.01); close(b, 0.70, 0.02)
    rows = [(0, 1.0, "bought"), (1, None, None), (2, 3.0, "gone"), (3, None, None)]
    k2, b2 = m.estimate(rows, 4.0)
    close(k2, 2 / 12, 1e-9); close(b2, 0.5, 1e-9)


for n, f in [("respond matches lecture table", t_closed), ("crossover", t_crossover),
             ("refunds and ring_net", t_refund_and_ban), ("simulate agrees with closed form", t_simulate),
             ("estimate recovers k and b", t_estimate)]:
    check(n, f)
print(f"{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)

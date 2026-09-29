"""Checks for Lab 10. Run from inside lab10-starter/:  ../../../../.venv/bin/python test_lab10.py
Every check fails on the starter and passes on a correct solution."""
from make_server import lab_server, toy_server
import rmt_graph as m

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


acc, gifts = toy_server()


def t_index():
    snd, rcv = m.build_index(gifts)
    assert len(snd["mule0"]) == 56, len(snd["mule0"])
    assert len(rcv["mule1"]) == 250
    assert rcv["farm3"] == {"mule3"}


def t_stranger():
    snd, rcv = m.build_index(gifts)
    assert m.stranger_share("bank0", acc, rcv) == 1.0
    assert m.stranger_share("bank7", acc, rcv) == 0.0
    assert m.stranger_share("mule2", acc, rcv) == 1.0
    assert m.stranger_share("p5000", acc, rcv) == 0


def t_hubs_toy():
    snd, rcv = m.build_index(gifts)
    assert m.find_hubs(acc, snd, rcv) == {"mule0", "mule1", "mule2", "mule3", "bank0"}


def t_expand_toy():
    snd, rcv = m.build_index(gifts)
    hubs = m.find_hubs(acc, snd, rcv)
    r4 = m.score(m.expand(hubs, acc, snd, careful=False), acc)
    r5 = m.score(m.expand(hubs, acc, snd), acc)
    assert (r4["tp"], r4["fp"], r4["fn"]) == (204, 27, 0), r4
    assert (r5["tp"], r5["fp"], r5["fn"]) == (204, 1, 0), r5
    assert r5["seized"] == 9_000_000
    assert abs(r5["precision"] - 204 / 205) < 1e-9


def t_no_mutation():
    snd, rcv = m.build_index(gifts)
    hubs = m.find_hubs(acc, snd, rcv)
    before = set(hubs)
    m.expand(hubs, acc, snd, hops=2)
    assert hubs == before


def t_best_rule():
    la, lg = lab_server(10)
    r = m.score(m.best_rule(la, lg), la)
    assert r["precision"] >= 0.95 and r["recall"] >= 0.90, r


for n, f in [("build_index", t_index), ("stranger_share", t_stranger), ("find_hubs on toy", t_hubs_toy),
             ("expand and score on toy (lecture R4, R5)", t_expand_toy), ("expand does not mutate", t_no_mutation),
             ("best_rule on lab server", t_best_rule)]:
    check(n, f)
print(f"{passed} passed, {failed} failed")
import sys
sys.exit(1 if failed else 0)

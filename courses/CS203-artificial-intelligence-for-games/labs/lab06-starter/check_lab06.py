"""Checks for CS203 Lab 06. Run: python check_lab06.py

Part A checks test Machine.step(). Part B checks test the guard's behaviour on
the four traces. Exits 0 only when every check passes. On the untouched starter
every check fails; after Part A alone, the Part B checks still fail.
"""
import sys

import guard as g

results = []
T = g.Transition
YES = lambda i, m: True


def check(name, fn):
    try:
        ok, detail = fn()
    except NotImplementedError as exc:
        ok, detail = False, f"not written yet ({exc})"
    except Exception as exc:
        ok, detail = False, f"{type(exc).__name__}: {exc}"
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + ("" if ok else f"  -> {detail}"))


def steps(machine, n):
    return [machine.step({}) for _ in range(n)]


def a_order():
    m = g.Machine("A", [T("A", "B", YES), T("A", "C", YES)])
    got = steps(m, 1)
    return got == ["B"], f"first listed transition should win, got {got}"


def a_dwell():
    m = g.Machine("A", [T("A", "B", YES)], {"A": 3})
    got = steps(m, 5)
    ok = got == ["A", "A", "A", "B", "B"] and m.log == [(3, "A", "B")]
    return ok, f"with min_dwell 3 the machine should leave A on tick 3; states {got}, log {m.log}"


def a_interrupt():
    m = g.Machine("A", [T("A", "B", YES, interrupt=True)], {"A": 3})
    got = steps(m, 1)
    return got == ["B"], f"an interrupt ignores min_dwell; got {got}"


def a_hooks():
    events = []
    m = g.Machine("A", [T("A", "B", YES)],
                  on_enter=lambda s: events.append(("enter", s)),
                  on_exit=lambda s: events.append(("exit", s)))
    steps(m, 1)
    return events == [("exit", "A"), ("enter", "B")], f"hook calls {events}"


def a_timer():
    m = g.Machine("A", [T("A", "B", lambda i, m: m.tick == 0),
                        T("B", "C", YES),
                        T("C", "A", lambda i, m: m.time_in_state >= 2)])
    got = steps(m, 5)
    want_log = [(0, "A", "B"), (1, "B", "C"), (3, "C", "A")]
    ok = got == ["B", "C", "C", "A", "A"] and m.log == want_log
    return ok, f"one transition per tick and time_in_state from entry; states {got}, log {m.log}"


def stints(states, name):
    out, n = [], 0
    for s in states:
        if s == name:
            n += 1
        elif n:
            out.append(n)
            n = 0
    return out, n


def b_strafe():
    m = g.make_guard()
    states = g.run(m, g.strafe_trace())
    attack = states.count("ATTACK") / len(states)
    ok = len(m.log) <= 6 and attack >= 0.8
    return ok, f"strafe: {len(m.log)} transitions (max 6), {attack:.0%} of ticks attacking (min 80%)"


def b_flicker():
    m = g.make_guard()
    states = g.run(m, g.strafe_trace())
    bad = [t for t, s in enumerate(states) if s in ("SEARCH", "PATROL")]
    return not bad, f"strafe: pillar flicker sent the guard to SEARCH/PATROL at ticks {bad[:5]}"


def b_approach():
    m = g.make_guard()
    states = g.run(m, g.approach_trace())
    ok = states[10] == "CHASE" and "ATTACK" in states[42:45]
    return ok, f"approach: want CHASE at tick 10 and ATTACK by tick 44; log {m.log}"


def b_escape():
    m = g.make_guard()
    states = g.run(m, g.escape_trace())
    search = next((t for t, s in enumerate(states) if s == "SEARCH"), None)
    patrol = next((t for t, s in enumerate(states) if s == "PATROL" and t > 0), None)
    ok = search is not None and 62 <= search <= 70 and patrol is not None and 100 <= patrol <= 140
    return ok, (f"escape: want SEARCH first on a tick in 62-70 (got {search}) and "
                f"PATROL on a tick in 100-140 (got {patrol})")


def b_juke():
    m = g.make_guard()
    g.run(m, g.juke_trace())
    pairs = [(s, d) for _, s, d in m.log]
    ok = (pairs == [("PATROL", "CHASE"), ("CHASE", "ATTACK"), ("ATTACK", "CHASE")]
          and 25 <= m.log[2][0] <= 30)
    return ok, ("juke: the 3-tick dash on ticks 4-6 must not cancel the attack, but "
                f"leaving for good at tick 25 must end it by tick 30; log {m.log}")


check("A1: transitions are tried in list order", a_order)
check("A2: min_dwell holds a state for the given number of ticks", a_dwell)
check("A3: interrupts ignore min_dwell", a_interrupt)
check("A4: on_exit runs before on_enter", a_hooks)
check("A5: one transition per tick; time_in_state counts from entry", a_timer)
check("B1: strafe trace, few transitions and mostly attacking", b_strafe)
check("B2: strafe trace, pillar flicker never ends the fight", b_flicker)
check("B3: approach trace, still responsive", b_approach)
check("B4: escape trace, SEARCH 0.3-1.1 s after losing sight, PATROL on tick 100-140", b_escape)
check("B5: juke trace, a short dash does not cancel the attack, a real exit does", b_juke)

print(f"\n{sum(results)}/{len(results)} checks pass")
sys.exit(0 if all(results) else 1)

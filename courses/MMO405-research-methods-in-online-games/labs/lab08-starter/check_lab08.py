"""MMO405 Lab 08 checker. Run after gen_data.py:  python check_lab08.py"""
import sys

import linkage as k

TOL = 1e-9

SURVEY = [{"account_id": "X1", "cohort": "veteran", "reported_h": "20"},
          {"account_id": "X9", "cohort": "new", "reported_h": "5"},
          {"account_id": "X2", "cohort": "new", "reported_h": "10"},
          {"account_id": "X3", "cohort": "veteran", "reported_h": "30"},
          {"account_id": "X4", "cohort": "new", "reported_h": "12"}]
TELE = [{"account_id": x, "logged_total_h": t, "logged_active_h": a}
        for x, t, a in (("X1", "26", "18"), ("X2", "11", "10"), ("X3", "34", "25"),
                        ("X4", "12", "11"), ("X5", "40", "30"))]


def close(a, b, tol=TOL):
    return abs(a - b) <= tol


def small():
    return k.link(SURVEY, TELE)


def t_link():
    linked, unmatched = small()
    return ([r["account_id"] for r in linked] == ["X1", "X2", "X3", "X4"]
            and unmatched == ["X9"] and linked[0]["logged_active_h"] == 18.0
            and linked[0]["reported_h"] == 20.0)


def t_discrepancy():
    row = small()[0][0]
    return close(k.discrepancy(row), -6.0) and close(k.discrepancy(row, "logged_active_h"), 2.0)


def t_group_summary():
    s = k.group_summary(small()[0])
    v, n = s["veteran"], s["new"]
    return (close(v[0], 25.0) and close(v[1], 30.0) and close(v[2], -5.0) and v[3] == 2
            and close(n[0], 11.0) and close(n[1], 11.5) and close(n[2], -0.5) and n[3] == 2)


def t_decompose():
    g = k.decompose(k.group_summary(small()[0]))
    return close(g[0], 14.0) and close(g[1], 18.5) and close(g[2], -4.5)


def t_select_cases():
    sel = k.select_cases(small()[0], k_under=1, k_accurate=1)
    return sel == {"new": {"under": ["X2"], "accurate": ["X4"]},
                   "veteran": {"under": ["X1"], "accurate": ["X3"]}}


def t_theme_table():
    sel = {"new": {"under": ["X2"], "accurate": ["X4"]},
           "veteran": {"under": ["X1"], "accurate": ["X3"]}}
    iv = [{"account_id": "X1", "themes": "idle;idle;alts"},
          {"account_id": "X2", "themes": "alts"},
          {"account_id": "X7", "themes": "idle"}]
    t = k.theme_table(sel, iv)
    zero = {"new-accurate": 0, "new-under": 0, "veteran-accurate": 0, "veteran-under": 0}
    return (t["idle"] == {**zero, "veteran-under": 1}
            and t["alts"] == {**zero, "veteran-under": 1, "new-under": 1}
            and set(t) == {"idle", "alts"})


def t_generated():
    linked, unmatched = k.link(k.load("survey.csv"), k.load("telemetry.csv"))
    g_tot = k.decompose(k.group_summary(linked))
    g_act = k.decompose(k.group_summary(linked, "logged_active_h"))
    sel = k.select_cases(linked)
    return (len(linked) == 308 and len(unmatched) == 8
            and close(g_tot[1], 4.741798806479112, 1e-6) and close(g_tot[2], -2.4942284739982945, 1e-6)
            and close(g_act[2], 0.8133503836317146, 1e-6)
            and sel["veteran"]["under"] == ["A0185", "A0551", "A1165", "A1172"]
            and sel["new"]["accurate"] == ["A0793", "A1015"]
            and k.theme_table(sel, k.load("interviews.csv"))["idle_not_counted"]["veteran-under"] == 4)


TESTS = {"link": t_link, "discrepancy": t_discrepancy, "group_summary": t_group_summary,
         "decompose": t_decompose, "select_cases": t_select_cases,
         "theme_table": t_theme_table, "generated_data": t_generated}


def main():
    ok = True
    for name, test in TESTS.items():
        try:
            passed = bool(test())
        except NotImplementedError:
            print(f"TODO {name}")
            ok = False
            continue
        except FileNotFoundError:
            print(f"FAIL {name}: run gen_data.py first")
            ok = False
            continue
        except Exception as e:
            print(f"FAIL {name}: {type(e).__name__}: {e}")
            ok = False
            continue
        print(("PASS " if passed else "FAIL ") + name)
        ok = ok and passed
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

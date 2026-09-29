#!/usr/bin/env python3
"""PR301 lab 06: check a tick budget report.

Usage: .venv/bin/python check_tick.py runs.csv claims.txt

runs.csv   columns: run,players,mobs,mean_ms,p99_ms
           Runs A, B, C, D as in the week 6 guide: (0,0), (P,0), (0,M), (P,M).
           Extra rows (for example a spread-layout run E) are printed but not fitted.
claims.txt key=value lines: hz, cpu_budget, p99_limit_ms, planned_mobs, m_max,
           chosen_option, fallback, and option_mean_ms (the mean tick the chosen option is
           modelled to give at the planned mobs; needed when planned_mobs > m_max)

The model t = a + g + c*M + d*P*M is fitted at the load-test crowd P of runs B and D and is
only valid at that crowd size. PASS needs planned_mobs <= M_max, or a chosen option whose
modelled mean (option_mean_ms) meets both limits. Standard library only. Prints PASS or
NOT READY (exit code 1).
"""
import csv
import sys

KEYS = ("hz", "cpu_budget", "p99_limit_ms", "planned_mobs", "m_max", "chosen_option", "fallback")


def load_claims(path):
    out = {}
    for line in open(path):
        line = line.split("#", 1)[0].strip()
        if "=" in line:
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def main(runs_path, claims_path):
    rows = {r["run"].strip().upper(): r for r in csv.DictReader(open(runs_path))}
    claims = load_claims(claims_path)
    problems = [f"missing run {x}" for x in "ABCD" if x not in rows]
    problems += [f"claims.txt: '{k}' is empty" for k in KEYS if not claims.get(k)]
    if problems:
        for p in problems:
            print("  -", p)
        print("NOT READY")
        return 1

    f = lambda r, k: float(rows[r][k])
    P, M0 = f("B", "players"), f("C", "mobs")
    if f("A", "players") or f("A", "mobs") or f("B", "mobs") or f("C", "players"):
        problems.append("runs A, B, C must be (0,0), (P,0), (0,M)")
    if (f("D", "players"), f("D", "mobs")) != (P, M0):
        problems.append("run D must use run B's players and run C's mobs")
    a = f("A", "mean_ms")
    g = f("B", "mean_ms") - a
    c = (f("C", "mean_ms") - a) / M0
    d = (f("D", "mean_ms") - a - g - c * M0) / (P * M0)
    k = f("D", "p99_ms") / f("D", "mean_ms")

    tick = 1000 / float(claims["hz"])
    mean_cpu = float(claims["cpu_budget"]) * tick
    mean_p99 = float(claims["p99_limit_ms"]) / k
    allowed = min(mean_cpu, mean_p99)
    M = float(claims["planned_mobs"])
    mean_plan = a + g + c * M + d * P * M
    m_max = int((allowed - a - g) / (c + d * P))

    print(f"a={a:.2f} ms  g={g:.2f} ms at P={P:.0f}  c={c:.4f} ms/mob  d={d:.6f} ms/pair  k={k:.2f}")
    print(f"tick {tick:.1f} ms; mean limit {mean_cpu:.1f} (CPU budget), {mean_p99:.1f} (p99 limit / k) -> {allowed:.1f} ms")
    print(f"planned {M:.0f} mobs at P={P:.0f}: mean {mean_plan:.1f} ms, p99 est {k * mean_plan:.1f} ms"
          f" ({'passes' if mean_plan <= allowed else 'fails'})")
    print(f"M_max at P={P:.0f}: {m_max}")
    for r, row in rows.items():
        if r not in "ABCD":
            print(f"extra run {r}: P={row['players']} M={row['mobs']} mean={row['mean_ms']} p99={row['p99_ms']}")
    got = int(float(claims["m_max"]))
    if abs(got - m_max) > 2:
        problems.append(f"m_max = {got}, checker computes {m_max}")
    if d < 0:
        problems.append("negative pair cost d: check that run D used the same layout as B and C")
    if M > m_max:
        opt = claims.get("option_mean_ms", "")
        if not opt:
            problems.append(f"planned {M:.0f} mobs exceed M_max {m_max}: model the chosen option "
                            f"and give its mean tick in option_mean_ms")
        else:
            om = float(opt)
            print(f"chosen option modelled: mean {om:.1f} ms, p99 est {k * om:.1f} ms")
            if om > allowed:
                problems.append(f"chosen option's mean {om:.1f} ms is above the {allowed:.1f} ms limit")
    for p in problems:
        print("  -", p)
    print("PASS" if not problems else "NOT READY")
    return 0 if not problems else 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))

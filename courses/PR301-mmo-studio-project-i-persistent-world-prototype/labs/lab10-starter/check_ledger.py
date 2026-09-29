#!/usr/bin/env python3
"""PR301 lab 10: reconcile the money supply against the ledger.

Usage: .venv/bin/python check_ledger.py ledger.csv snapshot.txt explanations.csv findings.csv

ledger.csv        columns: code,kind,budget_per_hour,actual_total   (kind: faucet or sink;
                  humans only, bot lines excluded; budget_per_hour blank for unbudgeted codes)
snapshot.txt      key=value: player_hours, money_start, and one line per place currency lives,
                  written place.<name> = amount (for example place.balances = 27937)
explanations.csv  columns: cause,amount,evidence   (each part of the residual, with its evidence)
findings.csv      columns: code,finding   (one row for every line outside 0.75 to 1.25 of budget)

Standard library only. Prints the budget table, the residual and PASS or NOT READY (exit code 1).
"""
import csv
import sys

LOW, HIGH = 0.75, 1.25


def load_kv(path):
    out = {}
    for line in open(path):
        line = line.split("#", 1)[0].strip()
        if "=" in line:
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def main(ledger_path, snap_path, expl_path, find_path):
    problems = []
    snap = load_kv(snap_path)
    H = float(snap["player_hours"])
    places = {k[6:]: float(v) for k, v in snap.items() if k.startswith("place.")}
    if not places:
        problems.append("snapshot.txt lists no place.<name> lines")
    m_end = sum(places.values())
    m_start = float(snap.get("money_start", 0) or 0)

    findings = {r["code"].strip(): r["finding"].strip() for r in csv.DictReader(open(find_path))}
    faucets = sinks = 0.0
    print(f"{'code':<16}{'budget/h':>10}{'actual':>10}{'actual/h':>10}{'ratio':>8}")
    for r in csv.DictReader(open(ledger_path)):
        code, kind, actual = r["code"].strip(), r["kind"].strip(), float(r["actual_total"])
        if kind == "faucet":
            faucets += actual
        elif kind == "sink":
            sinks += actual
        else:
            problems.append(f"{code}: kind must be faucet or sink")
        per_h = actual / H
        b = r["budget_per_hour"].strip()
        if b:
            ratio = per_h / float(b)
            flag = "" if LOW <= ratio <= HIGH else "  <- outside band"
            print(f"{code:<16}{float(b):>10.0f}{actual:>10,.0f}{per_h:>10.1f}{ratio:>8.2f}{flag}")
            if flag and not findings.get(code):
                problems.append(f"{code}: ratio {ratio:.2f} is outside {LOW}-{HIGH} and has no finding")
        else:
            print(f"{code:<16}{'-':>10}{actual:>10,.0f}{per_h:>10.1f}{'-':>8}")
    net = faucets - sinks
    residual = (m_end - m_start) - net
    print(f"faucets {faucets:,.0f}  sinks {sinks:,.0f}  net {net:,.0f}  ({net / H:.1f} per player-hour)")
    print(f"money supply {m_end:,.0f} = " + " + ".join(f"{k} {v:,.0f}" for k, v in places.items()))
    print(f"residual = {m_end:,.0f} - {m_start:,.0f} - {net:,.0f} = {residual:,.0f}")

    explained = 0.0
    for r in csv.DictReader(open(expl_path)):
        amt = float(r["amount"])
        explained += amt
        if not r.get("evidence", "").strip():
            problems.append(f"explanation '{r['cause']}' has no evidence")
        print(f"  explained: {r['cause']:<28}{amt:>10,.0f}")
    left = residual - explained
    tol = max(10.0, 0.001 * m_end)
    print(f"unexplained: {left:,.0f} (tolerance {tol:,.0f})")
    if abs(left) > tol:
        problems.append(f"{left:,.0f} of the residual is unexplained")
    for p in problems:
        print("  -", p)
    print("PASS" if not problems else "NOT READY")
    return 0 if not problems else 1


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(*sys.argv[1:]))

#!/usr/bin/env python3
"""PR401 lab 06: greenlight fit checker.

Usage: python greenlight_fit.py team.csv plan.csv risks.csv
Recomputes capacity, demand, risk reserve, fit ratio F and tripwire R* from
your files, compares them with the values you declared in team.csv, and
prints PASS or NOT READY. Exit code 0 on PASS, 1 otherwise. Standard library only.
"""
import csv
import sys

GO, CONDITIONAL = 1.00, 1.15
TOL = 0.01


def read_rows(path):
    with open(path, newline="") as f:
        return [{k.strip(): (v or "").strip() for k, v in row.items()} for row in csv.DictReader(f)]


def num(value, label, problems):
    try:
        return float(value)
    except ValueError:
        problems.append(f"{label}: '{value}' is not a number")
        return None


def verdict_for(F):
    if F <= GO:
        return "go"
    if F <= CONDITIONAL:
        return "conditional go"
    return "no-go"


def main(team_path, plan_path, risks_path, min_risks=5):
    problems = []
    team = {r["key"]: r["value"] for r in read_rows(team_path)}
    needed = ["people", "pr401_weeks", "pr401_hours", "pr402_weeks", "pr402_hours",
              "focus_factor", "focus_source",
              "plan_ratio", "plan_ratio_source", "declared_F", "declared_tripwire", "fit_verdict"]
    for k in needed:
        if not team.get(k):
            problems.append(f"team.csv: '{k}' is blank")
    vals = {k: num(team.get(k, ""), f"team.csv {k}", problems)
            for k in ["people", "pr401_weeks", "pr401_hours", "pr402_weeks", "pr402_hours",
                      "focus_factor", "plan_ratio"]}

    plan = read_rows(plan_path)
    S = 0.0
    for r in plan:
        est = num(r["estimate_h"], f"plan.csv {r['feature']}", problems)
        if r["keep"].lower() not in ("yes", "no"):
            problems.append(f"plan.csv {r['feature']}: keep must be yes or no")
        elif r["keep"].lower() == "yes":
            S += est or 0
            if not r.get("pillar"):
                problems.append(f"plan.csv {r['feature']}: kept feature has no pillar (write 'core' for infrastructure)")

    risks = read_rows(risks_path)
    if len(risks) < min_risks:
        problems.append(f"risks.csv: {len(risks)} risks, need at least {min_risks}")
    E, biggest = 0.0, (0.0, 0.0)
    for r in risks:
        p = num(r["probability"], f"risks.csv {r['risk']} probability", problems)
        c = num(r["loss_h"], f"risks.csv {r['risk']} loss_h", problems)
        if p is not None and not 0 < p <= 1:
            problems.append(f"risks.csv {r['risk']}: probability must be in (0, 1]")
        if not r.get("owner") or not r.get("trigger"):
            problems.append(f"risks.csv {r['risk']}: needs an owner and an observable trigger")
        if p is not None and c is not None:
            E += p * c
            if c > biggest[1]:
                biggest = (p, c)

    if None in vals.values():
        return report(problems, None)

    H = vals["pr401_weeks"] * vals["pr401_hours"] + vals["pr402_weeks"] * vals["pr402_hours"]
    C = vals["people"] * H * vals["focus_factor"]
    R = vals["plan_ratio"]
    D = S * R
    F = (D + E) / C
    R_star = (C - E) / S if S else float("inf")
    F_big = (D + E - biggest[0] * biggest[1] + biggest[1]) / C
    lines = [f"H = {H:.0f} h per person", f"C = {C:.1f} h", f"S kept = {S:.1f} h", f"D = S x R = {D:.1f} h", f"E = {E:.1f} h",
             f"F = {F:.3f}", f"R* = {R_star:.3f}", f"F if the biggest risk fires = {F_big:.3f}",
             f"model verdict = {verdict_for(F)}"]

    dF = num(team.get("declared_F", ""), "team.csv declared_F", problems) if team.get("declared_F") else None
    dR = num(team.get("declared_tripwire", ""), "team.csv declared_tripwire", problems) if team.get("declared_tripwire") else None
    if dF is not None and abs(dF - F) > TOL:
        problems.append(f"declared_F {dF} does not match computed {F:.3f}")
    if dR is not None and abs(dR - R_star) > TOL:
        problems.append(f"declared_tripwire {dR} does not match computed {R_star:.3f}")
    if team.get("fit_verdict") and team["fit_verdict"].lower() != verdict_for(F):
        problems.append(f"fit_verdict '{team['fit_verdict']}' does not follow from F = {F:.3f}")
    if R < 1.0:
        lines.append("note: plan ratio below 1.0 is rare; the panel will ask for the data")
    return report(problems, lines)


def report(problems, lines):
    for line in lines or []:
        print(line)
    for p in problems:
        print("  -", p)
    print("PASS" if not problems else "NOT READY")
    return 0 if not problems else 1


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(*sys.argv[1:]))

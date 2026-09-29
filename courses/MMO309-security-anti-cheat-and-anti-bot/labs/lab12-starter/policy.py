"""MMO309 Lab 12: a sanction policy with an error budget.

The model is the week 12 lecture's:
  LR = TPR / FPR ; posterior odds = prior odds x product of LRs of the signals that fired
  P = odds / (1 + odds) ; a sanction with cost ratio C is allowed when P >= C / (C + 1)

Fill in every function marked TODO. Run `python policy.py` for a summary.
"""
from make_accounts import make_accounts

SIGNALS = ("aim", "reports", "hash")


def rates(rows, signal):
    """Return (tpr, fpr) of `signal`: the share of cheaters and of honest accounts where it fired."""
    raise NotImplementedError("TODO")


def dependence(rows, a, b, cheat):
    """Among accounts with r["cheat"] == cheat, return P(a and b) / (P(a) * P(b)).
    1.0 means the two signals look independent in that group."""
    raise NotImplementedError("TODO")


def posterior(prior, lrs):
    """P(cheat) after multiplying the prior odds by every likelihood ratio in `lrs`."""
    raise NotImplementedError("TODO")


def threshold(C):
    """Confidence a sanction with cost ratio C requires."""
    raise NotImplementedError("TODO")


def allowed(p, ladder):
    """Names of the sanctions in `ladder` (dict name -> C) whose threshold p meets, in ladder order."""
    raise NotImplementedError("TODO")


def rule_rates(rows, required):
    """For the rule "sanction if every signal in `required` fired", return
    (cheaters caught per million players, innocents hit per million players), measured on rows."""
    raise NotImplementedError("TODO")


if __name__ == "__main__":
    rows = make_accounts()
    for s in SIGNALS:
        tpr, fpr = rates(rows, s)
        print(f"{s:8} TPR {tpr:.3f} FPR {fpr:.4f} LR {tpr / fpr:.0f}")
    print("aim/reports dependence, honest:", round(dependence(rows, "aim", "reports", False), 2),
          "cheaters:", round(dependence(rows, "aim", "reports", True), 2))
    print("lecture check:", round(posterior(0.01, [90, 10]), 4), allowed(0.9009, {"lock": 1, "susp": 5, "perm": 20}))
    for req in (["aim"], ["aim", "reports"], ["aim", "hash"], ["aim", "reports", "hash"]):
        tp, fp = rule_rates(rows, req)
        print(f"{'+'.join(req):18} caught/M {tp:8.0f} innocents/M {fp:8.1f}")

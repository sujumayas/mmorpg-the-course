"""MMO405 lab 10: randomized response.

Python 3, standard library only. Fill in the five TODOs, then run
    python -m unittest test_rr.py
from inside this folder (from the repository root, .venv/bin/python is the course Python).
Running this file directly prints the report once the TODOs are done.

Design (lecture week 10, section 2): with probability t the respondent answers
truthfully; otherwise a fair coin decides "yes" or "no".
"""
import csv
from math import sqrt, log, ceil
from pathlib import Path

HERE = Path(__file__).parent
Z95 = 1.959963984540054


def load_responses(path=HERE / "responses.csv"):
    """Return {method: (yes_count, n, t)} for each method in the file."""
    out = {}
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            yes, n, _ = out.get(r["method"], (0, 0, None))
            out[r["method"]] = (yes + int(r["answer"]), n + 1, float(r["t"]))
    return out


def p_yes(pi, t):
    """TODO 1. Probability of a "yes" when the true share is pi and the truth probability is t."""
    raise NotImplementedError("TODO 1")


def estimate(yes, n, t):
    """TODO 2. Return (pi_hat, se) from yes answers out of n with truth probability t.

    pi_hat = (q_hat - (1 - t)/2) / t, se = sqrt(q_hat (1 - q_hat) / n) / t,
    where q_hat = yes / n. Do not clip pi_hat to [0, 1]; report it as it is.
    """
    raise NotImplementedError("TODO 2")


def epsilon(t):
    """TODO 3. Privacy level ln((1 + t)/(1 - t)). Return math.inf when t == 1."""
    raise NotImplementedError("TODO 3")


def posterior(prior, t, answer):
    """TODO 4. P(respondent is a buyer | their answer), answer is 1 ("yes") or 0 ("no")."""
    raise NotImplementedError("TODO 4")


def n_for_margin(margin, pi, t):
    """TODO 5. Smallest integer n whose 95% margin Z95 * SE is at most `margin`.

    Use the planning value pi to compute q = p_yes(pi, t). Round up.
    """
    raise NotImplementedError("TODO 5")


def report():
    data = load_responses()
    for method, (yes, n, t) in sorted(data.items()):
        pi_hat, se = estimate(yes, n, t)
        print(f"{method:6s} n={n}  yes={yes}  t={t:.2f}  estimate={pi_hat:.4f}  "
              f"95% CI=({pi_hat - Z95 * se:.4f}, {pi_hat + Z95 * se:.4f})  eps={epsilon(t):.2f}")
    print(f"n for +-2 points at pi=0.12, t=0.5: {n_for_margin(0.02, 0.12, 0.5)}")
    print(f"P(buyer | yes) at prior 0.12, t=0.5: {posterior(0.12, 0.5, 1):.3f}")


if __name__ == "__main__":
    report()

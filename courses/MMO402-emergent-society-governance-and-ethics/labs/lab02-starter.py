"""MMO402 Lab 02 starter: K-of-N approval rules.

Run:  python lab02-starter.py
Pure standard library, Python 3.8+.

Model (week 2, section 2):
  N officers, K approvals needed.
  q = chance an officer is a traitor (independent).
  a = chance an officer is available in time (independent).
  P(hijack) = P(at least K traitors)  = tail(N, K, q)
  P(timely) = P(at least K available) = tail(N, K, a)
  cost      = H * P(hijack) + L * (1 - P(timely))
"""
from math import comb


def tail(n, k, p):
    """P(X >= k) for X ~ Binomial(n, p)."""
    return sum(comb(n, j) * p**j * (1 - p) ** (n - j) for j in range(k, n + 1))


def cost(N, K, q, a, H, L):
    # TODO step 1: return the expected cost of a K-of-N rule.
    raise NotImplementedError


def missed_duty(N, a, days):
    # TODO step 2: chance that no officer does an any-of-N duty on any of `days` days.
    raise NotImplementedError


def table(N, q, a, H, L):
    print(f"N={N} q={q} a={a} H={H} L={L}")
    print(" K  P(hijack)%  P(timely)%    cost")
    for K in range(1, N + 1):
        h, t = tail(N, K, q), tail(N, K, a)
        try:
            c = f"{cost(N, K, q, a, H, L):7.2f}"
        except NotImplementedError:
            c = "   todo"
        print(f"{K:2d}  {100*h:10.3f}  {100*t:10.2f}  {c}")


if __name__ == "__main__":
    table(5, 0.1, 0.6, 100, 10)   # must match the week 2 lecture table
    table(6, 0.03, 0.5, 100, 10)  # the design brief's guild

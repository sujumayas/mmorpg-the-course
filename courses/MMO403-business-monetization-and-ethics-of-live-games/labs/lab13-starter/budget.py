"""MMO403 Lab 13 starter: phase budgets, runway and the price of a slip.
Standard-library Python 3.10 or later.

Fill in every function marked TODO, then run the tests from this folder:

    python3 test_budget.py        (or: pytest test_budget.py)

The model is the one from the week 13 lecture, section 2:

    burn in phase p:       B_p = n_p x c + F
    total budget:          S   = sum over phases of m_p x B_p
    runway:                R   = cash remaining / burn now
    cost of a slip:        dS  = extra months x B_p

A plan is a list of [phase, months, headcount] rows, in order.
c is the loaded cost per head-month and F the fixed cost per month, both in dollars.
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load_plan(path=os.path.join(HERE, "plan.csv")):
    """Return the plan as a list of [phase, months, headcount] rows."""
    with open(path, newline="") as f:
        return [[r["phase"], int(r["months"]), int(r["headcount"])] for r in csv.DictReader(f)]


# ---------------------------------------------------------------- TODO

def phase_burn(heads, cost, fixed):
    """Monthly burn of a phase with `heads` people: heads x cost + fixed."""
    raise NotImplementedError("phase_burn")


def burn_series(plan, cost, fixed, ramp=0):
    """Monthly burn for every month of the plan, in order.

    ramp = 0: every month of a phase has that phase's headcount.
    ramp = r > 0: people join evenly over the first r months of each phase. In month k
    (k = 1..r) of a phase the headcount is prev + (new - prev) x k / r, where prev is the
    headcount of the previous phase (0 before the first phase). From month r on it is
    the phase's own headcount. A phase shorter than r months never reaches it.
    """
    raise NotImplementedError("burn_series")


def cash_out_month(series, cash):
    """First month (1-indexed) in which cumulative spend EXCEEDS cash, or None."""
    raise NotImplementedError("cash_out_month")


def slip(plan, phase_name, extra):
    """A NEW plan with `extra` months added to the named phase. Do not change `plan`."""
    raise NotImplementedError("slip")


def slip_cost(plan, phase_name, extra, cost, fixed):
    """Extra spending caused by `extra` months of slip in the named phase (flat staffing)."""
    raise NotImplementedError("slip_cost")


def contingency_months(total, share, burn):
    """How many months of `burn` a contingency of `share` x `total` pays for."""
    raise NotImplementedError("contingency_months")


def runway(cash, series):
    """Months of the series that `cash` pays for, counting a final partial month as a
    fraction. Example: cash 250, series [100, 100, 100] -> 2.5."""
    raise NotImplementedError("runway")


def crash_vs_slip(hires, months_left, ramp_months, ramp_eff, mentor_share, cost,
                  phase_burn_now, slip_months):
    """Compare hiring to recover a slip with accepting it (lecture section 3).

    Returns (net_extra_head_months, cost_of_hiring, cost_of_slipping) where
      net output  = hires x (ramp_months x ramp_eff + (months_left - ramp_months))
                    - hires x ramp_months x mentor_share
      hiring cost = hires x months_left x cost
      slip cost   = slip_months x phase_burn_now
    """
    raise NotImplementedError("crash_vs_slip")


if __name__ == "__main__":
    plan = load_plan()
    s = burn_series(plan, 10_000, 50_000)
    print(f"total {sum(s):,} over {len(s)} months")

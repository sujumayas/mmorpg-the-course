"""MMO308 Lab 14 starter: forecasting a sunset from a declining MAU series.

Run it with:
    .venv/bin/python courses/MMO308-live-operations-analytics-and-experimentation/labs/lab14-starter.py

Every function marked TODO raises NotImplementedError. The tests at the bottom
print PASS or FAIL for each part and the script exits with status 1 while any
test fails. Do not change the tests or the data generator. Standard library only.
"""
import math
import random
import sys

# ---------------------------------------------------------------------------
# Data: 18 months of noisy MAU for "your" game (do not edit)
# ---------------------------------------------------------------------------


def make_history(seed=14, months=18):
    """Return a list of monthly MAU values for months 0..months-1.

    The hidden truth is a core-plus-casual mixture with about 3% measurement
    noise. You do not get the true parameters; you estimate them.
    """
    rng = random.Random(seed)
    M0, w, hc, hk = 120_000, 0.25, 30, 5
    out = []
    for t in range(months):
        m = M0 * (w * 2 ** (-t / hc) + (1 - w) * 2 ** (-t / hk))
        out.append(round(m * (1 + rng.uniform(-0.03, 0.03))) if t else M0)
    return out


# ---------------------------------------------------------------------------
# Part A. The diagnostic
# ---------------------------------------------------------------------------

def six_month_ratios(series):
    """Return [series[6]/series[0], series[12]/series[6], ...] for every full six-month step."""
    raise NotImplementedError("A1: six-month ratios")


# ---------------------------------------------------------------------------
# Part B. The two models and their fits
# ---------------------------------------------------------------------------

def mixture(t, M0, w, hc, hk):
    """M0 x (w x 2^(-t/hc) + (1 - w) x 2^(-t/hk)); hc and hk are half-lives in months."""
    raise NotImplementedError("B1: mixture model")


def fit_single(series):
    """Least-squares fit of ln(MAU) = ln(M0) - lam x t over all months.

    Return (M0, lam). Use the ordinary least-squares slope and intercept of
    ln(series[t]) against t, then M0 = e^intercept and lam = -slope.
    """
    raise NotImplementedError("B2: single-rate fit")


def fit_mixture(series):
    """Grid-search fit of the mixture with M0 fixed at series[0].

    Search w in 0.05, 0.10, ..., 0.95; hc in 12, 15, ..., 60; hk in 2.0, 2.5, ..., 12.0.
    Minimize the sum over months of (ln(model) - ln(observed))^2.
    Return (w, hc, hk). Round w to 2 decimals.
    """
    raise NotImplementedError("B3: mixture fit")


# ---------------------------------------------------------------------------
# Part C. Forecasts and their errors
# ---------------------------------------------------------------------------

def crossing(model, a, cost, horizon=120):
    """First month on a 0.1-month grid (k/10 for k = 0, 1, 2, ...) where
    a x model(t) <= cost. Return None if it does not happen by `horizon`."""
    raise NotImplementedError("C1: crossing month")


def announce_month(cross, notice):
    """Month by which you must announce: cross - notice, rounded to 1 decimal.
    Return 0.0 if that is already in the past (negative)."""
    raise NotImplementedError("C2: announce month")


def error_costs(single_model, mixture_model, a, cost, t_single, t_mixture):
    """Return (profit_forgone, loss_taken) in dollars.

    profit_forgone: sum of (a x mixture_model(t) - cost) x 0.1 for t = k/10 from
                    t_single up to (not including) t_mixture. The mixture is true
                    and you closed early.
    loss_taken:     minus the same sum computed with single_model. The single
                    rate is true and you ran too long.
    """
    raise NotImplementedError("C3: error costs")


# ---------------------------------------------------------------------------
# Tests (do not edit)
# ---------------------------------------------------------------------------

def _close(a, b, tol):
    return abs(a - b) <= tol


def run_tests():
    results = []

    def check(name, fn):
        try:
            ok = fn()
        except NotImplementedError as e:
            ok, name = False, f"{name} (not written yet: {e})"
        except Exception as e:
            ok, name = False, f"{name} ({type(e).__name__}: {e})"
        results.append(ok)
        print(("PASS  " if ok else "FAIL  ") + name)

    lecture = [100_000 * (0.3 * 2 ** (-t / 36) + 0.7 * 2 ** (-t / 6)) for t in range(25)]

    check("A1 six-month ratios match the lecture",
          lambda: [round(x, 3) for x in six_month_ratios(lecture)] == [0.617, 0.669, 0.725, 0.777])

    check("B1 mixture at month 6 = 61,727",
          lambda: _close(mixture(6, 100_000, 0.3, 36, 6), 61_727, 1))

    def b2():
        M0, lam = fit_single([100_000 * math.exp(-0.05 * t) for t in range(13)])
        return _close(M0, 100_000, 1) and _close(lam, 0.05, 1e-9)
    check("B2 single-rate fit recovers an exact exponential", b2)

    check("B3 mixture fit recovers the lecture's parameters",
          lambda: tuple(fit_mixture(lecture[:19])) == (0.3, 36, 6))

    def b4():
        hist = make_history()
        M0, lam = fit_single(hist)
        w, hc, hk = fit_mixture(hist)
        sse_s = sum((math.log(M0) - lam * t - math.log(m)) ** 2 for t, m in enumerate(hist))
        sse_m = sum((math.log(mixture(t, hist[0], w, hc, hk)) - math.log(m)) ** 2
                    for t, m in enumerate(hist))
        return sse_m < sse_s
    check("B4 on your history, the mixture fits better than one rate", b4)

    lam = math.log(100_000 / lecture[12]) / 12
    single = lambda t: 100_000 * math.exp(-lam * t)
    mix = lambda t: mixture(t, 100_000, 0.3, 36, 6)

    check("C1 crossings at $50,000 are 28.3 and 46.8",
          lambda: _close(crossing(single, 4, 50_000), 28.3, 1e-6)
          and _close(crossing(mix, 4, 50_000), 46.8, 1e-6)
          and crossing(mix, 4, 1_000) is None)

    check("C2 announce months",
          lambda: announce_month(28.3, 6) == 22.3 and announce_month(4.0, 6) == 0.0)

    def c3():
        f, l = error_costs(single, mix, 4, 50_000, 28.3, 46.8)
        return _close(f, 240_883, 5) and _close(l, 420_869, 5)
    check("C3 error costs match the lecture", c3)

    passed = sum(results)
    print(f"\n{passed}/{len(results)} tests passed")
    return passed == len(results)


if __name__ == "__main__":
    sys.exit(0 if run_tests() else 1)

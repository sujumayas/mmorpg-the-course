"""Run: python test_tick_profiler.py   (prints 'all lab 05 tests passed')"""
from tick_profiler import (tick_cost, utilization, t_max, timer_length, same_tick_probability,
                           multirate_cpu_per_second, fit_costs, schedule)


def near(got, want, tol, label):
    assert abs(got - want) <= tol, f"{label}: got {got}, want {want} +- {tol}"


c = tick_cost(1, 0.005, 0.0002, 3000, 50)
near(c, 46.0, 1e-9, "lecture zone")
near(utilization(c, 10), 0.46, 1e-9, "u at 10 Hz")
near(utilization(c, 30), 1.38, 1e-9, "u at 30 Hz")
near(t_max(c), 13.043, 1e-3, "T_max")
near(1 + 0.005 * 3000 + 0.0002 * (800 * 400 + 2200 * 50), 102.0, 1e-9, "siege (arithmetic)")
near(tick_cost(1, 0.005, 0.0002, 10, 9), 1.068, 1e-9, "shooter match")
near(timer_length(1.2, 1), 2.0, 1e-9, "1.2 s at 1 Hz")
near(timer_length(1.2, 1 / 0.6), 1.2, 1e-9, "1.2 s at 0.6 s ticks")
near(timer_length(1.2, 5), 1.2, 1e-9, "1.2 s at 5 Hz")
near(timer_length(1.2, 128), 154 / 128, 1e-9, "1.2 s at 128 Hz")
near(timer_length(1.5, 5), 1.6, 1e-9, "1.5 s at 5 Hz rounds up")
near(same_tick_probability(0.1, 5), 0.5, 1e-9, "100 ms apart at 5 Hz")
near(same_tick_probability(0.1, 10), 0.0, 1e-9, "100 ms apart at 10 Hz")
near(same_tick_probability(0.01, 50), 0.5, 1e-9, "10 ms apart at 50 Hz")
near(multirate_cpu_per_second(1, 0.005, 0.0002, 1400, 50, 1600, 10), 244.0, 1e-9, "multi-rate")
near(multirate_cpu_per_second(1, 0.005, 0.0002, 3000, 50, 0, 10), 460.0, 1e-9, "single rate")

# the fit recovers exact constants from noiseless samples
true = (0.8, 0.004, 0.00025)
samples = [(n, k, tick_cost(*true, n, k)) for n in (100, 500, 2000, 4000) for k in (5, 40, 300)]
fa, fd, fe = fit_costs(samples)
near(fa, 0.8, 1e-6, "fit a")
near(fd, 0.004, 1e-9, "fit d")
near(fe, 0.00025, 1e-10, "fit e")

# overrun policies: 102 ms ticks at 10 Hz
starts, skipped = schedule([102.0] * 10, 10, "stretch")
near(starts[-1] + 102 - 1000, 20.0, 1e-9, "stretch drift after 10 ticks")
assert skipped == 0
starts, skipped = schedule([102.0] * 200, 10, "skip")
assert skipped == 3, f"skip policy skipped {skipped}, want 3"
starts, skipped = schedule([46.0] * 50, 10, "skip")
assert skipped == 0 and starts[49] == 4900.0, "a tick that fits is never late"

print("all lab 05 tests passed")

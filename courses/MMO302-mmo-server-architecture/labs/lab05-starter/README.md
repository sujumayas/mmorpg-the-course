# MMO302 lab 05 starter: tick budget profiler

Standard library Python 3.10 or later. From this folder:

    python test_tick_profiler.py              # fails until you fill in the TODO functions
    python tick_profiler.py --lecture         # the lecture's tables from your functions
    python tick_profiler.py --measure m.csv   # time a toy world at 12 sizes (a few seconds)
    python tick_profiler.py --fit m.csv       # fit a, d, e and print T_max for the lecture zone

Fill in `tick_cost`, `utilization`, `t_max`, `timer_length`, `same_tick_probability`,
`multirate_cpu_per_second`, `fit_costs` and `schedule`. See [lab05.md](../lab05.md).

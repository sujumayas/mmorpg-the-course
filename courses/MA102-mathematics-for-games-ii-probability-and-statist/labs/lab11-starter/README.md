# Lab 11 starter

- `lab11_starter.py`: helpers `load_config`, `simulate(trial, n, seed)`, `estimate(trial, n, seed)` (mean with its 95% margin) and `percentile(values, q)`, plus the stub `trial_raid(rng, config)` you write. The file's docstring lists the order of events in one kill. Run it as a script or paste it into a notebook. Standard library only, using `random.Random(seed)` as in the week 11 lecture.
- `raid_config.json`: the full raid. 10 players, 2 drops per kill from 8 items weighted 20, 20, 15, 15, 10, 10, 5, 5, one needed item per player (items A and C are needed by two players each), pity after 12 kills without the item.
- `validation_config.json`: the step 1 known case. One player, a target item of weight 1 out of 20, one drop per kill, no pity. Set `pity_kills` to 12 for the second half of step 1.

Once `trial_raid` works, `python lab11_starter.py` prints the step 1 validation table with seed 1111.

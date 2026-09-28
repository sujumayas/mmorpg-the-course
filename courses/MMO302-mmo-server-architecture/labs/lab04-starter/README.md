# MMO302 lab 04 starter: zone servers and handoff

Standard library Python 3.10 or later. From this folder:

    python test_zone_sim.py          # fails until you fill in the TODO functions
    python zone_sim.py --table       # the lecture's formula table
    python zone_sim.py --simulate 4  # random-walk shard on a 4 x 4 grid
    python zone_sim.py --idle        # idle crowd on a border, handoffs per hysteresis band

Fill in `handoff_rate`, `ghost_fraction`, `busiest_zone`, `next_owner`, `ZoneServer.start_handoff`
and `ZoneServer.on_message`. Everything else is provided. See [lab04.md](../lab04.md).

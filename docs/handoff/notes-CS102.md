w11 spec: energizer fires at round(e*60) but lecture run() fires one tick later (example follows lecture); align spec. w09: lecture says 95% of budget, spec cost gives 96%; align.
w09 sec 5 BUG: says deferred destruction stops later systems seeing dead entity; code shows doomed entity stays visible until flush(). lab09 step 7 'drawn at 0 hp' when render before burn only happens when burn runs first. Fix lecture and lab (exam Q40 states verified behavior).
w05 spec: '112% of frame' -> 112.5% with B=1000/60 ms.
w04 table: '12x over' at n=2000 uses model, '46x over' at 4000 uses measured (model 50x); use one basis. spec n_max 6,922 -> 6,921.
w12: lecture table uses seed-7 random player ((180,-300), 52/194, 389 changes=1,167 bytes) but spec scripted player gives (0,-900), 44/180, 1,080 bytes; jitter drift 5.31 not '4'. Make lecture and spec use the same scenario.
w13: spec crash text 'randint(6, 1)' vs lecture 'randrange(6, 2)'; align. With validation off the duplicate row overwrites the upgrade so no KeyError appears; fix wording.

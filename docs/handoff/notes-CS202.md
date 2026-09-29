w01-03: WoW transport inferred from 2.3.2 Nagle + TrinityCore; For Honor/Destiny omitted; AoE packet size illustrative.
w04-06: Overwatch, cl_cmdbackup, Unreal rotator compression dropped. MMO309/MMO302 named only.
w07-09: GGPO, Rocket League, Overwatch rollback dropped; QuakeWorld Sept 1996 beta.
w10-12: Riot 141 ms baseline unused; rewind cap unpublished (said); w12 byte sizes assumptions.
w13-14: Unreal emulation presets unchecked (not used); Apex 60 kB/s overall.
DUPLICATE: w09 specs examples/w09-lag-lab.html and w10 specs examples/w10-lag-lab.html (signature). Resolved by FIX agent before building.
FIX: w09 lag-lab duplicate removed; w09 now examples/w09-reconcile-replay.html (spec values from labs/lab09-starter/netsim.py); w10 spec now cites lab09-starter/netsim.py. Reviewer: confirm assessments don't reference old w09 lag lab.
Assessments written in parallel with builders; reviewer must reconcile exam-bank answers with any lecture changes.
w04 spec wording: 'J=40 lead 240 m' test only holds for cheater at full 1+tol=5x; slider max 3.0. Builder labelled line A as cheater at 1+tol. Align spec/lecture wording.
w14 spec first-screen caption says '18 lost, 1 burst of >=3'; seed 14 gives 2 bursts (lengths 3 and 4). Page shows 2. Fix spec caption.
w08: predicted delay = input wait + frame wait = 8.3+8.3 = 16.7 ms avg; lecture table, formula and spec say 8.3 (page shows 16.7). Decide correct model and fix lecture/spec/example together.
w08: dumb client at 0 ms RTT stops 0 ms after release under definition reproducing 83.3/183.3/283.3; lecture table says 16.7. Fix.
w05 "Move it yourself": 1 cm to 50 cm drops bits by five (16 to 11), not three. Fix.
w07: example defaults to seed 2 (seed 1 shows only one stale cell); stale = differs from server state at client's last decoded tick. Align spec wording.
w10 Table 1 dumb client: 'keeps sliding 1.1 m (183 ms)'; model gives 1.0 m drawn after release (183.3 ms correct). Fix. w11: example fires while 6 mm of victim shows (=1 ms at 6 m/s); align spec wording.

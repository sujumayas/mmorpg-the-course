"""MMO402 Lab 07 starter: simulate a report-review-appeal pipeline.

Usage examples:
    python lab07-starter.py
    python lab07-starter.py --n 5 --t 3 --f 0.3
    python lab07-starter.py --n 9 --t 7 --rho 0.3 --appeal --ladder warn,1d,7d,perm

What it simulates (all numbers are synthetic, for teaching):
  * A population of players over a number of weeks. A small share are
    persistent offenders; everyone else offends rarely. Some innocent players
    are also reported (false or mistaken reports).
  * Every reported case goes to a panel of n reviewers. Each reviewer votes
    guilty with probability s if the player is guilty, f if innocent. With
    probability rho the whole panel shares one impression (one draw decides
    for everyone); otherwise reviewers vote independently. The panel convicts
    if at least t reviewers vote guilty.
  * A conviction moves the player one rung up a strike ladder. The last rung
    is a permanent ban; banned players stop generating cases.
  * With --appeal, convicted players may appeal to one independent reviewer
    (appeal rates a_i for innocent, a_g for guilty; appeal reviewer s_a, f_a).
    A successful appeal removes the strike.

Output: a summary of correct and wrongful convictions, missed offences,
players permanently banned (and how many of those had at least one wrongful
strike), and reviewer workload. Pure standard library, Python 3.8+.
"""
import argparse
import random


def panel_convicts(rng, guilty, n, t, s, f, rho):
    p = s if guilty else f
    if rng.random() < rho:
        return rng.random() < p          # shared impression: one draw for all
    votes = sum(1 for _ in range(n) if rng.random() < p)
    return votes >= t


def run(args):
    rng = random.Random(args.seed)
    ladder = [r.strip() for r in args.ladder.split(",") if r.strip()]
    players = []
    for i in range(args.players):
        persistent = rng.random() < args.persistent_share
        players.append({"persistent": persistent, "rung": 0, "banned": False,
                        "strikes": []})   # list of True (rightful) / False (wrongful)
    stats = dict(cases=0, guilty_cases=0, innocent_cases=0,
                 correct_conv=0, wrong_conv=0, missed=0,
                 appeals=0, appeals_from_guilty=0, reversed_wrong=0,
                 released_guilty=0, reviews=0)
    for week in range(args.weeks):
        for p in players:
            if p["banned"]:
                continue
            rate = args.offend_persistent if p["persistent"] else args.offend_other
            events = []
            if rng.random() < rate:
                events.append(True)                       # a real offence, reported
            if rng.random() < args.false_report:
                events.append(False)                      # reported without an offence
            for guilty in events:
                stats["cases"] += 1
                stats["guilty_cases" if guilty else "innocent_cases"] += 1
                stats["reviews"] += args.n
                conv = panel_convicts(rng, guilty, args.n, args.t, args.s, args.f, args.rho)
                if not conv:
                    if guilty:
                        stats["missed"] += 1
                    continue
                if guilty:
                    stats["correct_conv"] += 1
                else:
                    stats["wrong_conv"] += 1
                if args.appeal:
                    appeals = rng.random() < (args.a_g if guilty else args.a_i)
                    if appeals:
                        stats["appeals"] += 1
                        stats["reviews"] += 1
                        if guilty:
                            stats["appeals_from_guilty"] += 1
                            if rng.random() > args.s_a:        # appeal reviewer clears a guilty player
                                stats["released_guilty"] += 1
                                continue
                        else:
                            if rng.random() > args.f_a:        # appeal reviewer clears an innocent player
                                stats["reversed_wrong"] += 1
                                continue
                p["strikes"].append(guilty)
                p["rung"] += 1
                if p["rung"] >= len(ladder):
                    p["banned"] = True
                    break
    banned = [p for p in players if p["banned"]]
    banned_with_wrong = [p for p in banned if not all(p["strikes"])]
    banned_never_guilty = [p for p in banned if not any(p["strikes"])]
    return stats, ladder, banned, banned_with_wrong, banned_never_guilty


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--players", type=int, default=20000)
    ap.add_argument("--weeks", type=int, default=12)
    ap.add_argument("--persistent-share", type=float, default=0.03)
    ap.add_argument("--offend-persistent", type=float, default=0.30, help="weekly chance a persistent offender commits a reported offence")
    ap.add_argument("--offend-other", type=float, default=0.004, help="weekly chance anyone else commits a reported offence")
    ap.add_argument("--false-report", type=float, default=0.002, help="weekly chance any player is reported without an offence")
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--t", type=int, default=2)
    ap.add_argument("--s", type=float, default=0.9)
    ap.add_argument("--f", type=float, default=0.3)
    ap.add_argument("--rho", type=float, default=0.0)
    ap.add_argument("--ladder", default="warn,1d,7d,perm", help="comma-separated rungs; the last is a permanent ban")
    ap.add_argument("--appeal", action="store_true")
    ap.add_argument("--a-i", type=float, default=0.8)
    ap.add_argument("--a-g", type=float, default=0.4)
    ap.add_argument("--s-a", type=float, default=0.9)
    ap.add_argument("--f-a", type=float, default=0.2)
    ap.add_argument("--seed", type=int, default=402)
    args = ap.parse_args()
    if not 1 <= args.t <= args.n:
        ap.error("need 1 <= t <= n")

    stats, ladder, banned, banned_wrong, banned_never = run(args)
    conv = stats["correct_conv"] + stats["wrong_conv"]
    print(f"Panel n={args.n}, t={args.t}, s={args.s}, f={args.f}, rho={args.rho}, "
          f"ladder={'>'.join(ladder)}, appeal={'on' if args.appeal else 'off'}, seed={args.seed}")
    print(f"Cases reviewed:            {stats['cases']:>7}  (guilty {stats['guilty_cases']}, innocent {stats['innocent_cases']})")
    print(f"Conviction rate:           {conv / max(1, stats['cases']):>7.1%}")
    print(f"Correct convictions:       {stats['correct_conv']:>7}")
    print(f"Wrongful convictions:      {stats['wrong_conv']:>7}")
    print(f"Missed offences:           {stats['missed']:>7}")
    if args.appeal:
        print(f"Appeals heard:             {stats['appeals']:>7}  (from guilty players: {stats['appeals_from_guilty']})")
        print(f"Wrongful convictions reversed on appeal: {stats['reversed_wrong']}")
        print(f"Guilty players released on appeal:       {stats['released_guilty']}")
    print(f"Permanent bans:            {len(banned):>7}")
    print(f"  with at least one wrongful strike: {len(banned_wrong)}")
    print(f"  with no rightful strike at all:    {len(banned_never)}")
    print(f"Reviewer workload:         {stats['reviews']:>7} reviews over {args.weeks} weeks "
          f"({stats['reviews'] / args.weeks:.0f} a week)")


if __name__ == "__main__":
    main()

# CS202 · Lab 03: The topology calculator

**Week:** 3 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the labs (40%)

## Objective

Turn the [week 3 lecture](../lectures/w03-topologies-peer-to-peer-client-server-relay.md)'s formulas into a tool, check it against the lecture's tables, and use it to choose a topology for a game of your own. You finish with a one-page recommendation that a producer could act on, backed by bandwidth and latency numbers.

## Starter materials

Folder [`lab03-starter/`](lab03-starter/README.md). Standard library Python only.

- `topology.py`: stubs for `mesh_upload`, `snapshot_bytes`, `server_upload`, `listen_host_upload`, `client_upload`, `pair_latency` and `worst_pair`, plus a report and a `--check` mode.
- `scenario.json`: the lecture's four players, direct latency matrix, and two server sites.

Optional: the latency logs you collected in [Lab 02](lab02.md).

## Steps

1. **Implement the bandwidth functions.** Follow the docstrings. Keep each to one or two lines, matching the lecture's formulas.
2. **Implement latency.** Write `pair_latency` for `mesh`, `server` and `listen`, and `worst_pair` with `itertools.combinations`. Run `python topology.py --check` until it prints `all checks passed`.
3. **Reproduce the lecture.** Run `python topology.py scenario.json --n 8` and `--n 64`. Paste the output and confirm it matches the lecture's tables. Verify two latency cells by hand.
4. **Add a relay.** Extend `pair_latency` with a `relay` topology that reads a `"relays"` block from the scenario (same shape as `"servers"`). Add relay R with A 20, B 18, C 15, D 20. Report the worst pair and compare it with the lecture's answer (40 ms, A-D).
5. **Your own game.** Copy `scenario.json` to `my_scenario.json`. Choose a game concept with 6 to 16 players and set `rate_hz`, `state_bytes` and `input_bytes` with a one-line reason each. Build a latency matrix for at least five players in two or more regions. Use real measurements where you can (Lab 02's tool run between classmates' machines), or public data, and say which cells are measured and which are estimated. Add two candidate server sites.
6. **Stress it.** Find the largest player count at which a listen host with a 10 Mbit/s uplink still fits, and the largest send rate at your chosen player count. Write a short function for each rather than guessing.
7. **Recommend.** Write one page. State the topology and, if relevant, the server site or host-selection rule. Give the upload per machine, the worst-pair latency, and the round trip of the worst-off player. Name one risk the numbers do not capture (cheating, cost, host leaving, NAT, IP exposure) and how you would handle it.

## Deliverable

Your finished `topology.py`, `my_scenario.json`, the outputs from steps 3, 4 and 6, two hand-checked latency cells, and the one-page recommendation. Submit before next week's lecture.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Core functions | `--check` passes; code matches the lecture's formulas line for line | Passes with a workaround or unclear code | Fails the check | 25% |
| Relay extension | Relay reads from JSON, reproduces 40 ms, and the code handles a missing relay block | Works for the example only | Missing | 15% |
| Scenario quality | Every parameter justified; measured and estimated cells marked; at least five players and two regions | Parameters present, justification thin | Copied numbers with no reasoning | 20% |
| Limits (step 6) | Both limits computed by code and checked by hand | One limit, or guessed by trial | Missing | 15% |
| Recommendation | Choice follows from the numbers; worst pair and worst-off player named; a real risk with a mitigation | Choice sensible but numbers or risk thin | Opinion without numbers | 25% |

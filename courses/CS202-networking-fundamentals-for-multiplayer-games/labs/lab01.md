# CS202 · Lab 01: Sockets and the cost of order

**Week:** 1 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the labs (40%)

## Objective

Send real packets between two programs on your own machine, see TCP's byte stream break a naive protocol, fix it with framing, and build the head-of-line model from the [week 1 lecture](../lectures/w01-networks-for-game-devs-tcp-vs-udp.md) so you can predict, in milliseconds, what one lost packet costs each transport. You finish with a transport recommendation backed by numbers.

## Starter materials

Folder [`lab01-starter/`](lab01-starter/README.md). Standard library Python only. Use the course interpreter (`.venv/bin/python` at the repository root) or any Python 3.10 or later.

- `udp_hello.py`: complete UDP echo server and client.
- `tcp_framing.py`: a demo of the byte-stream problem, stubs for `send_msg`, `recv_exact` and `recv_msg`, and a test.
- `hol_sim.py`: the head-of-line model. `udp_delivery` is written. You write `tcp_delivery`.

## Steps

1. **UDP on localhost.** Start `python udp_hello.py server` in one terminal and run `python udp_hello.py client --count 20` in another. Record the round-trip times. Stop the server and run the client again. Write two sentences on what the client can and cannot tell about why a reply did not come.
2. **See the stream.** Run `python tcp_framing.py demo`. Explain in two sentences why one `recv()` returned all three messages, using the words "byte stream" and "message boundary".
3. **Frame it.** Implement `send_msg`, `recv_exact` and `recv_msg` with a 2-byte big-endian length prefix. Run `python tcp_framing.py test` until it prints `framing tests passed`. Then answer this. What would break if you used a 1-byte length instead, and what is the largest message your 2-byte version can carry?
4. **Build the model.** Implement `tcp_delivery` in `hol_sim.py` following its docstring. Run `python hol_sim.py --table`. It must print the lecture's table (20 Hz and RTT 100 ms gives a TCP gap of 300.0 ms, and 60 Hz and RTT 100 ms gives 166.7 ms). Paste the output.
5. **Probe the model.** Run three scenarios of your own choice, including at least one where the timeout path fires instead of fast retransmit (hint: a low send rate) and one with two consecutive losses (`--lost 10 11`). For each, record the send rate, RTT, the UDP gap, the TCP gap, and which TCP path fired. Check one TCP gap by hand with the lecture's formula.
6. **Nagle, measured.** Add `sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)` to the client socket in `tcp_framing.py`'s demo and run it again. On localhost you may see no difference. Explain why in terms of what Nagle waits for, and say what kind of link would show the difference.
7. **Recommend.** Using the in-class dungeon crawler (four players, real-time melee, loot, trade, chat), write a half-page recommendation. Name the transport for each message type, give the send rate for movement, and quote the model's UDP and TCP gaps at RTT 60 ms and 180 ms to justify it.

## Deliverable

A zip or repository link containing your finished `tcp_framing.py` and `hol_sim.py`, and a single PDF or Markdown file with the answers to steps 1, 2, 3 and 6, the outputs from steps 4 and 5, one hand check, and the recommendation from step 7. Submit before next week's lecture.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Framing code | Tests pass; `recv_exact` loops correctly and handles a closed connection; the 1-byte limit explained | Tests pass but edge cases (empty message, long message) not explained | Tests fail or framing absent | 25% |
| Head-of-line model | `--table` output matches the lecture exactly; code follows the docstring | Minor numeric slips or one path wrong | Model missing or unrelated to the lecture | 25% |
| Scenarios and hand check | Three scenarios including timeout and double loss; the hand check matches the program | Scenarios run but timeout case or hand check missing | Fewer than two scenarios | 20% |
| Explanations (steps 1, 2, 6) | Precise, uses the lecture's terms, Nagle reasoning names the unacknowledged-data condition | Correct in outline, vague in places | Incorrect or missing | 10% |
| Recommendation | Every message type assigned with a reason; numbers from the model at both RTTs; a trade-off admitted | Assignments given but numbers thin | Opinion without numbers | 20% |

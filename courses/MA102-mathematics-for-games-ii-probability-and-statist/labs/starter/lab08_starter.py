"""MA102 lab 08 starter: dice by design.

Run it as a script (python lab08_starter.py) or paste the sections into a
notebook. The exact 2d6 outcome table is below as TWO_D6_OUTCOMES and in
lab08_2d6_outcomes.csv next to this file.

What you write:
    die(F)
    dice_sum(N, F, bonus)
    success_curve(values, probs, mode)

Spreadsheet version: build it yourself with the 2d6 table of all 36
outcomes (import lab08_2d6_outcomes.csv), a sheet for 3d6 by repeated
convolution with one column per die, and a chart of the result.
"""
import numpy as np
import matplotlib.pyplot as plt

# All 36 outcomes of 2d6 as (first die, second die, sum).
TWO_D6_OUTCOMES = [(a, b, a + b) for a in range(1, 7) for b in range(1, 7)]


def die(F):
    """One fair F-sided die.

    Return a numpy float array of length F with every entry 1/F.
    Entry i is the chance of rolling i + 1.
    """
    raise NotImplementedError("Write die (step 1).")


def dice_sum(N, F, bonus):
    """Exact distribution of NdF + bonus.

    Return (values, probs), two numpy arrays of the same length.
    values runs from N + bonus to N*F + bonus. probs[i] is P(roll = values[i]).
    Build probs by starting from die(F) and applying np.convolve with
    die(F) until N dice are included.
    """
    raise NotImplementedError("Write dice_sum (step 1).")


def success_curve(values, probs, mode):
    """Success chance for every target t in `values`.

    mode ">=" returns P(roll >= t) for each t.
    mode "<=" returns P(roll <= t) for each t.
    Return a numpy array the same length as `values`.
    """
    raise NotImplementedError("Write success_curve (step 1).")


if __name__ == "__main__":
    sums = [s for _, _, s in TWO_D6_OUTCOMES]
    ways7 = sums.count(7)
    print(f"2d6 table: {len(TWO_D6_OUTCOMES)} outcomes, "
          f"{ways7} ways to roll 7, P(= 7) = {ways7}/36")

    try:
        v, p = dice_sum(2, 6, 0)
        print(f"2d6  P(= 7)  = {p[v == 7][0]:.4f}   (target 6/36 = 0.1667)")
        v, p = dice_sum(3, 6, 0)
        print(f"3d6  P(<= 10) = {success_curve(v, p, '<=')[v == 10][0]:.4f}   (target 0.5)")
        v, p = dice_sum(8, 6, 0)
        mean = (v * p).sum()
        sd = np.sqrt(((v - mean) ** 2 * p).sum())
        print(f"8d6  mean = {mean:.2f}, SD = {sd:.2f}   (targets 28 and 4.83)")
        plt.bar(v, p)
        plt.xlabel("sum")
        plt.ylabel("probability")
        plt.show()
    except NotImplementedError as e:
        print(f"TODO: {e}")

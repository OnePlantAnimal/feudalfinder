# This script prints a table of feudal intervals
# i.e. intervals of form [(a + b phi) / (x + y phi)] 
# where a*y - b*x = +-1 (merciful intervals) OR b = y= 0 (just intervals).
#
# The table can be printed in order of distance (as a ratio or in cents mod 1200) or harmonic entropy (HE),
# and includes the cents%1200, ratio, (a + b phi) / (x + y phi), and entropy. 
#
# Search of intervals is done by radius, i.e. |a|,|b|,|x|,|y| < 1, then < 2, < 3 and so on.
# All subsequently found octave equivalents and sub unison intervals are discarded.
#
#
# Author: Eli Rosenkim
# Jul 8 2026

import math

import numpy as np

# HE lookup table
def _build_harmonic_entropy_table(max_value=200, gaussian_deviation=17, alpha=100):

    x = np.array(range(1201))

    intervals = []
    interval_weights = []
    for i in range(1, max_value):
        for j in range(1, max_value):
            if np.gcd(i, j) == 1 and i >= j and i <= (2*j):
                intervals.append(i / j)
                interval_weights.append(1/np.sqrt(i * j))

    intervals = np.array(intervals)
    interval_weights = np.array(interval_weights)
    intervals_cents = np.rint(1200 * np.log2(intervals)).astype(int)

    K = np.zeros(len(x))  # K will store the strongest harmonic contribution at each cent value
    for i in range(len(intervals)):
        if (K[intervals_cents[i]] < interval_weights[i]):
            K[intervals_cents[i]] = interval_weights[i]

    x_gaussian = np.array(range(100))
    S = np.exp(-0.5 * ((x_gaussian - 50) / gaussian_deviation)**2) #S holds gaussian blur, wider is more tuning uncertainty. note 1/sigma sqrt(2pi) factor left out as it appears in numerator and denominator of following line
    return 1 / (1 - alpha) * np.log( np.convolve(K**alpha, S**alpha, 'same') / np.convolve(K, S, 'same')**alpha)


# Helper function for order of interval search
def _centered_range(radius):
    yield 0
    for i in range(1, radius + 1):
        yield i
        yield -i


# Return dictionary of intervals
def find_feudal(
    bound=7,
    sort_by="cents",
    discard_just=False,
    discard_merciful=False,
    max_value=200,
    gaussian_deviation=17,
    alpha=100,
):
    """
    Find feudal intervals of the form (a + bφ)/(x + yφ).

    Parameters
    ----------
    bound : int
        Searches intervals fulfulling
        |a|, |b|, |x|, |y| <= bound.
    sort_by : str
        Sorting method: "cents", "ratio", or "entropy".
    discard_just : bool
        If True, discard just intervals where b = y = 0.
    discard_merciful : bool
        If True, discard merciful intervals where a*y - b*x = ±1.
    max_value : int
        Maximum numerator and denominator used for harmonic entropy calculation.
    gaussian_deviation : float
        Standard deviation of the Gaussian blur used in harmonic entropy.
    alpha : float
        Weighting parameter for harmonic entropy calculation.

    Returns
    -------
    list of dict
        A list of intervals sorted according to sort_type. Each dictionary contains:
        "cents", "ratio", "a", "b", "x", "y", and "entropy".
    """

    PHI = (1 + math.sqrt(5)) / 2

    HE = _build_harmonic_entropy_table(max_value, gaussian_deviation, alpha)

    unique = {}

    # Populate dictionary of intervals
    for radius in range(1, bound + 1):
        for a in _centered_range(radius):
            for b in _centered_range(radius):
                for x in _centered_range(radius):
                    for y in _centered_range(radius):

                        if max(abs(a), abs(b), abs(x), abs(y)) < radius: # skip combos already fully covered by a smaller radius
                            continue

                        if (abs(a*y - b*x) != 1) and not(b == 0 and y == 0): #discard intervals which are neither just nor merciful
                            continue

                        if discard_just and (b == 0 and y == 0): #discard just intervals
                            continue

                        if discard_merciful and (b != 0 or y != 0): #discard merciful intervals
                            continue

                        num = a + b*PHI
                        den = x + y*PHI

                        if abs(num) < 1e-12 or abs(den) < 1e-12: #discard 0 or 1/0 intervals
                            continue

                        ratio = abs(num / den)

                        if abs(num / den) < 1: #discard intervals < unison
                            continue

                        cents = (1200 * math.log2(ratio)) % 1200 

                        # group by cent value (rounded to 5 digits)
                        key = round(cents, 5)

                        if key not in unique:
                            unique[key] = {
                                "cents": cents,
                                "a": a,
                                "b": b,
                                "x": x,
                                "y": y,
                                "ratio": ratio,
                                "entropy": HE[int(cents)],
                            }

    #Sort dictionary values into a list of dicts
    intervals = sorted(unique.values(), key=lambda r: r[sort_by])
    return intervals

#handles print formatting
def print_intervals(intervals):
    """
    Takes in list of dicts from find_feudal() and prints in collumns of cents%1200, ratio, a+bphi/x+yphi, entropy
    i.e. "1043.61        14.618    12-13φ /1-1φ     2.26178"
    """
    #formatting helper to get rid of phi when not used
    fmt = lambda a, b: str(a) if b == 0 else f"{a}{b:+d}φ"

    #print
    print(
        f"{'cents%1200':>10}    "
        f"{'ratio':>10}    "
        f"{'(a+bφ)/(x+yφ)':<14}"
        f"{'entropy':>10}"
    )
    print("-"*65)
    for i in intervals:
        print(
            f"{i['cents']:>10.6g}    "
            f"{i['ratio']:>10.6g}    "
            f"{fmt(i['a'], i['b']):<7}/{fmt(i['x'], i['y']):<9}"
            f"{i['entropy']:.6g}"
        )


if __name__ == "__main__":
    print_intervals(
        find_feudal(
            bound=7, #max value of |a|,|b|,|x|,|y|
            sort_by="cents", #"cents" (by cents), "ratio", or "entropy".
            discard_just = False, #discards just intervals
            discard_merciful = False, #discards merciful intervals
            max_value = 200, #max value of numerator/denominator for harmonic entropy calculation
            gaussian_deviation = 17, #gaussian blur standard deviation for harmonic entropy calculation
            alpha = 100 #weighting parameter for harmonic entropy calculation
        )
    )
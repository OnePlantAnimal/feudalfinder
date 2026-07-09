# feudalfinder

A Python script for printing sorted tables of feudal intervals, i.e. intervals of the form

$$
\frac{a+b \phi}{x+y \phi}
$$

where either 
$(a*y) - (b*x) = \pm 1$ (we call intervals that satisfy this property *merciful*), or $b = y = 0$ (we call intervals that satisfy this property *just*), and $\phi = \frac{1+\sqrt{5}}{2}$ is the golden ratio.

The script searches intervals is order of radius, i.e. $|a|,|b|,|x|,|y| < 1$, then $< 2$, $< 3$ and so on.
All subsequently found octave equivalents and sub unison intervals are discarded.

Intervals can be sorted by:
- distance from unison in cents modulo 1200
- frequency ratio (this is not modulo 2)
- harmonic entropy

All of the above properties are printed, in addition to the representation ((a+b phi)/(x+y phi)).

One can also discard either merciful or just intervals to examine the other alone.


## Example Usage
```python
from feudalfinder import find_feudal, print_intervals

# Find feudal intervals
intervals = find_feudal(
    bound=7, #max value of |a|,|b|,|x|,|y|
    sort_by="cents", #"cents" (by cents), "ratio", or "entropy".
    discard_just = False, #discards just intervals
    discard_merciful = False, #discards merciful intervals
    max_value = 200, #max value of numerator/denominator for harmonic entropy calculation
    gaussian_deviation = 17, #gaussian blur standard deviation for harmonic entropy calculation
    alpha = 100 #weighting parameter for harmonic entropy calculation
)

# Print a formatted table from a list of dictionaries as returned by find_feudal
print_intervals(intervals)
```

which should print something like:
cents%1200         ratio    (a+bφ)/(x+yφ)    entropy
         0             1    1      /1        0.129036
   128.831       8.61803    6-7φ   /1-1φ     2.69597
   157.894       4.38197    1-5φ   /0+1φ     2.5713
   177.973       2.21654    5-7φ   /2-3φ     2.40088
   213.528       1.13127    6-7φ   /5-6φ     2.34096
     224.1       2.27639    3-5φ   /1-2φ     2.21142
   243.619        1.1511    5-6φ   /4-5φ     2.30806
... (and so on)


## References

See this [forum post by Dave Keenan](https://forum.sagittal.org/viewtopic.php?t=557&sid=6b83f62ed5491a07c717481b6c925ae9&utm_source=chatgpt.com) on Feudal intonation, and the [Xenharmonic wiki explanation of harmonic entropy](
https://en.xen.wiki/w/Harmonic_entropy).

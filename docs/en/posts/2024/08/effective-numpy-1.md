---
title: "Efficient Quant Coding: Mask Arrays and find_runs for Streak Detection"
date: 2024-08-25
slug: en/posts/tools/effective-numpy-1
tags: [Quantitative Trading, NumPy, Mask Arrays, Factor Analysis]
excerpt: "Learn to detect consecutive events like limit-ups or N-day rallies in quantitative trading using NumPy’s find_runs and mask arrays for efficient streak calculation."
lang: en
translation_of: posts/tools/effective-numpy-1
auto_translated: true
source_sha: 87621ca4b73f1e946628decc5b0663831736028c
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/noise-test-title-image.jpg"
---

In many quantitative scenarios, we need to count the number of consecutive occurrences of a specific event, such as consecutive price limits (limit-up/limit-down), N-day winning streaks, or calculating streaks in Connor's RSI.

<!-- more -->

For example, how do we determine the maximum number of consecutive limit-ups or the longest N-day rally from the following closing prices?

```python
a = [15.28, 16.81, 18.49, 20.34, 21.2, 20.5, 22.37, 24.61, 27.07, 29.78, 
     32.76, 36.04]
```

Assuming a 10% threshold, we can transform the above array into:

```python
pct = np.diff(a) / a[:-1]
pct > 0.1
```

This yields the following array:

```
flags = [True, False, True, False, False, False, True, False, True, True, True]
```

While this doesn't directly calculate the maximum consecutive limit-ups, it serves as a fundamental data structure for such problems. By converting raw data into such boolean arrays based on conditions, we can use the following powerful tool:

```python
from numpy.typing import ArrayLike
from typing import Tuple
import numpy as np

def find_runs(x: ArrayLike) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Find runs of consecutive items in an array.

    Args:
        x: the sequence to find runs in

    Returns:
        A tuple of unique values, start indices, and length of runs
    """

    # ensure array
    x = np.asanyarray(x)
    if x.ndim != 1:
        raise ValueError("only 1D array supported")
    n = x.shape[0]

```

---

```python
    # handle empty array
    if n == 0:
        return np.array([]), np.array([]), np.array([])

    else:
        # find run starts
        loc_run_start = np.empty(n, dtype=bool)
        loc_run_start[0] = True
        np.not_equal(x[:-1], x[1:], out=loc_run_start[1:])
        run_starts = np.nonzero(loc_run_start)[0]

        # find run values
        run_values = x[loc_run_start]

        # find run lengths
        run_lengths = np.diff(np.append(run_starts, n))

        return run_values, run_starts, run_lengths


pct = np.diff(a) / a[:-1]
v,s,l = find_runs(pct > 0.099)
(v, s, l)
```

The output is:

```python
(array([ True, False,  True]), array([0, 3, 6]), array([3, 3, 5]))
```

The output is a tuple containing three arrays representing:

- `value`: unique values
- `start`: start indices
- `length`: length of runs

In the output above, `v[0]` is `True`, indicating the start of a series of limit-ups, `s[0]` is the corresponding start index (index 0), and `l[0]` indicates that the consecutive limit-up count is 3. Similarly, we can determine that the longest consecutive limit-up in the original array (corresponding to `v[2]`) is 5 (from `l[2]`), starting at index 6 (`s[2]`).

Therefore, to find the maximum consecutive limit-ups in the original sequence, we simply need to find the maximum value in `l`. However, solving this requires a bit of technique using the **mask array** introduced in Chapter 4.

```python
v_ma = np.ma.array(v, mask = ~v)
pos = np.argmax(v_ma * l)
print(f"Maximum consecutive limit-ups: {l[pos]}, starting from index {s[pos]}: {a[s[pos]]}.")
```

---

Here, the role of the mask array is to exclude data where `v == False` from calculations (in `v_ma * l`) while preserving their order (indices). This ensures that when we call the `argmax` function, the returned index corresponds correctly to the positions in `v`, `s`, and `l`.

The `v_ma` we created is a mask array with the value:

```
masked_array(data=[True, --, True],
            mask=[False,  True, False],
            fill_value=True)
```

When multiplied by another integer array, `True` is converted to the number 1. The result remains a mask array:

```
masked_array(data=[3, --, 5],
             mask=[False,  True, False],
            fill_value=True)
```

When `argmax` is applied to a mask array, it ignores elements where the mask is `True` but preserves their positions. Thus, the final result for `pos` is 2, corresponding to the values in `v`, `s`, and `l` as: `True`, `6`, and `5`, respectively.

What if we want to count the longest N-day rally? This is an easier task than finding limit-ups. However, this time, we will not use a mask array:

```python
v,s,l = find_runs(np.diff(a) > 0)

pos = np.argmax(v * l)
print(f"Longest N-day rally: {l[pos]}, starting from index {s[pos]}: {a[s[pos]]}.")
```

The output is: Longest N-day rally is 6, starting from index 5: 20.5.

The key here is that when NumPy performs multiplication, `True` is treated as 1 and `False` as 0. Consequently, the multiplication result naturally eliminates parts without consecutive rallies, not interfering with the `argmax` calculation.

Of course, using a mask array might be semantically clearer, even though it is slightly slower. Correctness and readability are often more important.

---

### Calculating Streaks in Connor's RSI

Connor's RSI (Connor's Relative Strength Index) is a technical analysis indicator developed by Nirvana Systems as an improved version of the traditional Relative Strength Index (RSI).

The main difference between Connor's RSI and traditional RSI is that it considers the number of consecutive days of price increases or decreases, known as "winning streaks" and "losing streaks." This consideration allows Connor's RSI to better reflect the strength of market trends.

After introducing the `find_runs` function, calculating streaks becomes very simple.

```python
def streaks(close):
    result = []
    conds = [close[1:]>close[:-1], close[1:]<close[:-1]]

    flags = np.select(conds, [1, -1], 0)
    v, _, l = find_runs(flags)
    for i in range(len(v)):
        if v[i] == 0:
            result.extend([0] * l[i])
        else:
            result.extend([v[i] * x for x in range(1, (l[i] + 1))])
            
    return np.insert(result, 0, 0)
```

This code first divides the price series into three sub-series: rising, falling, and flat. It then calculates the number of consecutive days of rising or falling for each sub-series and merges the results into a new array.

In `streaks`, consecutive rising days are represented by positive numbers, and consecutive falling days by negative numbers. In line 5, `np.select` converts the condition array into a sequence of `[1, 0, -1]`. Subsequent multiplication yields the correct number of consecutive rising (or falling) days.

---
title: "Numpy Vectorization for Quant: Counting Consecutive Runs"
date: 2025-03-25
slug: en/articles/python/numpy-pandas/08-numpy应用案例-1
tags: [Numpy, Quantitative Finance, Vectorization, Backtesting]
excerpt: "Learn to use Numpy vectorization to efficiently count consecutive events in quantitative finance, such as limit-ups or streaks, using mask arrays and find_runs for high-performance backtesting."
lang: en
translation_of: articles/python/numpy-pandas/08-numpy应用案例-1
auto_translated: true
source_sha: e51270f8cf82f561cd703664ecab5a18563ba79d
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/mybook/men-wearing-tank.jpg"
---

In many quantitative scenarios, we need to count the number of consecutive occurrences of an event, such as consecutive price limits (limit-ups/limit-downs), N-day winning streaks, or calculating streaks in Connor's RSI. Through Numpy’s vectorized operations, we can quickly implement these requirements efficiently and concisely.

---

## 1. Counting Consecutive Values

In many quantitative scenarios, we need to count how many times an event has occurred consecutively—for example, consecutive price limits, N-day winning streaks, or calculating streaks in Connor's RSI. For instance, given the following closing prices, what is the maximum number of consecutive limit-ups? What is the longest N-day winning streak?

```python
a = [15.28, 16.81, 18.49, 20.34, 21.2, 20.5, 22.37, 24.61, 27.07, 29.78, 
    32.76, 36.04]
```

Assuming we set the threshold at a 10% increase, we can convert the above array into:

```python
pct = np.diff(a) / a[:-1]
pct > 0.1
```

We obtain the following array:

```python
flags = [True, False,  True, False, False, False,  True, False,  True,
        True,  True]
```

This alone does not calculate the maximum number of consecutive limit-ups, but it is a fundamental data structure for many such problems. Once we convert the original data into a similar array based on conditions, we can use the following powerful tool:

---

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

    # handle empty array
    if n == 0:
        return np.array([]), np.array([]), np.array([])

    else:
        # find run starts
        loc_run_start = np.empty(n, dtype=bool)
        loc_run_start[0] = True
        np.not_equal(x[:-1], x[1:], out=loc_run_start[1:])
        run_starts = np.nonzero(loc_run_start)[0]

        run_values = x[loc_run_start]  # find run values
        run_lengths = np.diff(np.append(run_starts, n))  # find run lengths

        return run_values, run_starts, run_lengths
```

---

```python
pct = np.diff(a) / a[:-1]
v,s,l = find_runs(pct > 0.099)
(v, s, l)
```

The output result is:

(array([ True, False,  True]), array([0, 3, 6]), array([3, 3, 5]))

The output is a tuple consisting of three arrays, representing:

- `value`: unique values
- `start`: start indices
- `length`: length of runs

In the output above, `v[0]` is `True`, indicating the start of a series of limit-ups. `s[0]` corresponds to the starting position, which is index 0. `l[0]` indicates that the number of consecutive limit-ups is 3. Similarly, we can determine that the longest consecutive limit-ups in the original array (`v[2]`) is 5 (`l[2]`), starting from index 6 (`s[2]`).

Therefore, to find the maximum number of consecutive limit-ups in the original sequence, we simply need to find the maximum value in `l`. However, solving this problem requires a slight trick: we must use the **mask array** introduced in <ref>Chapter 4</ref>.

```python
v_ma = np.ma.array(v, mask = ~v)
pos = np.argmax(v_ma * l)

print(f"最大连续涨停次数{l[pos]}，从索引{s[pos]}:{a[s[pos]]}开始。")
```

The role of the mask array here is to exclude data where `v == False` from the calculation (i.e., `v_ma * l`) while preserving the order (indices) of these elements. This ensures that when we later call the `argmax` function, the index found corresponds correctly to the positions in `v`, `s`, and `l`.

The mask array `v_ma` we created has the value:

```python
masked_array(data=[True, --, True],
             mask=[False,  True, False],
       fill_value=True)
```

When multiplied by another integer array, `True` is converted to the number 1. Thus, the multiplication result remains a mask array:

```python
masked_array(data=[3, --, 5],
             mask=[False,  True, False],
       fill_value=True)
```

When `argmax` is applied to a mask array, it ignores elements where the mask is `True` but preserves their positions. Consequently, the final result `pos` is 2, corresponding to the element values in `v`, `s`, and `l` as: `True`, `6`, and `5`.

<!-- We introduced mask arrays in the basics section. Through this example, we see how mask arrays function in quantitative scenarios. -->

What if we want to count the longest N-day winning streak? This is an easier task than finding limit-ups. However, this time, we will implement it **without** using a mask array:

```python
v,s,l = find_runs(np.diff(a) > 0)
pos = np.argmax(v * l)

print(f"最长N连涨次数{l[pos]}，从索引{s[pos]}:{a[s[pos]]}开始。")
```

The output result is: The longest N-day winning streak is 6, starting from index 5:20.5.

---

The key here is that when Numpy performs multiplication, `True` is treated as the number 1, and `False` as 0. Thus, the multiplication result naturally eliminates parts without consecutive upward movements, preventing interference with the `argmax` calculation.

Of course, using a mask array might be semantically clearer. Although mask arrays are slightly slower, correctness and readability are often more important.

## 2. Calculating Streaks in Connor's RSI

Connor's RSI (Connor's Relative Strength Index) is a technical analysis indicator developed by Nirvana Systems as an improved version of the traditional Relative Strength Index (RSI). The main difference between Connor's RSI and traditional RSI is that it considers the number of consecutive days of price increases or decreases, known as "winning streaks" and "losing streaks." This consideration allows Connor's RSI to better reflect the strength of market trends.

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

---

This code first divides the stock price series into three sub-series: upward, downward, and flat. It then calculates the number of consecutive upward or downward days for each sub-series and merges the results into a new array. In `streaks`, consecutive upward days are represented by positive numbers, and consecutive downward days by negative numbers. Therefore, in line 5, `np.select` converts the condition array into a sequence of `[1, 0, -1]`. Subsequent multiplication yields the correct number of consecutive upward (or downward) days.

---

<!-- 
This article is part of the series on Numpy and Pandas in quantitative scenarios. This series introduces not only basic Numpy and Pandas but also how to flexibly apply Numpy and Pandas techniques in quantitative scenarios to write concise and efficient code. The example code fully demonstrates this point.
-->

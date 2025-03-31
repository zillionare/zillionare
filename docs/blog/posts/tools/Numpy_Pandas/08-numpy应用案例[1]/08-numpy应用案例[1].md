---
title: Numpy应用案例[1]
series: 量化人的 Numpy 和 Pandas
seq: "08"
fonts:
    sans: 'AlibabaPuHuiTi-Thin, sans-serif'
slug: numpy-pandas-for-quant-trader-08
date: 2025-03-25
category: tools
motto: Hard work beats talent when talent doesn't work hard.
img: https://images.jieyu.ai/images/hot/mybook/men-wearing-tank.jpg
stamp_width: 60%
stamp_height: 60%
tags: 
    - tools
    - programming
    - Numpy
---

“在很多量化场景下，我们都需要统计某个事件连续发生的次数，比如连续涨停、N 连阳等。通过 Numpy 的向量化操作，我们可以快速实现这些需求，既高效又简洁。”

---

## 1. 连续值统计

在很多量化场景下，我们都需要统计某个事件连续发生了多少次，比如，连续涨跌停、N连阳、计算Connor's RSI中的streaks等等。比如，要判断下列收盘价中，最大的连续涨停次数是多少？最长的N连阳数是多少？

```python
a = [15.28, 16.81, 18.49, 20.34, 21.2, 20.5, 22.37, 24.61, 27.07, 29.78, 
    32.76, 36.04]
```

假设我们以10%的涨幅为限，则可以将上述数组转换为：

```python
pct = np.diff(a) / a[:-1]
pct > 0.1
```

我们将得到以下数组：

```python
flags = [True, False,  True, False, False, False,  True, False,  True,
        True,  True]
```

这仍然不能计算出最大连续涨停次数，但它是很多此类问题的一个基本数据结构，我们将原始的数据按条件转换成类似的数组之后，就可以使用下面的神器了：

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

输出结果为：

(array([ True, False,  True]), array([0, 3, 6]), array([3, 3, 5]))

输出结果是一个由三个数组组成的元组，分别表示：

- value: unique values
- start: start indices
- length: length of runs

在上面的输出中，v[0]为True，表示这是一系列涨停的开始，s[0]则是对应的起始位置，此时索引为0; l[0]则表示该连续的涨停次数为3次。同样，我们可以知道，原始数组中，最长连续涨停（v[2]）次数为5（l[2]），从索引6（s[2]）开始起。


所以，要找出原始序列中的最大连续涨停次数，只需要找到l中的最大值即可。但要解决这个问题依然有一点技巧，我们需要使用<ref>第4章</ref>中介绍的 mask array。


```python
v_ma = np.ma.array(v, mask = ~v)
pos = np.argmax(v_ma * l)

print(f"最大连续涨停次数{l[pos]}，从索引{s[pos]}:{a[s[pos]]}开始。")
```

在这里，mask array的作用是，既不让 v == False 的数据参与计算

---

（后面的 v_ma * l），又保留这些元素的次序（索引）不变，以便后面我们调用 argmax 函数时，找到的索引跟v, s, l中的对应位置是一致的。

我们创建的v_ma是一个mask array，它的值为：

```python
masked_array(data=[True, --, True],
             mask=[False,  True, False],
       fill_value=True)
```

当它与另一个整数数组相乘时，True就转化为数字1，这样相乘的结果也仍然是一个mask array:

```python
masked_array(data=[3, --, 5],
             mask=[False,  True, False],
       fill_value=True)
```

当arg_max作用在mask array时，它会忽略掉mask为True的元素，但保留它们的位置，因此，最终pos的结果为2，对应的 v,s,l中的元素值分别为: True, 6, 5。

<!-- 我们在前面的基础篇介绍了mask array，通过这个例子，我们看到了在量化场景下，mask array如何起作用的。-->



如果要统计最长N连涨呢？这是一个比寻找涨停更容易的任务。不过，这一次，我们将不使用mask array来实现：


```python
v,s,l = find_runs(np.diff(a) > 0)
pos = np.argmax(v * l)

print(f"最长N连涨次数{l[pos]}，从索引{s[pos]}:{a[s[pos]]}开始。")
```

输出结果是： 最长N连涨次数6，从索引5:20.5开始。

---

这里的关键是，当Numpy执行乘法时，True会被当成数字1，而False会被当成数字0，于是，乘法结果自然消除了没有连续上涨的部分，从而不干扰argmax的计算。

当然，使用mask array可能在语义上更清楚一些，尽管mask array的速度会慢一点，但正确和易懂常常更重要。

## 2. 计算 Connor's RSI中的streaks

Connor's RSI（Connor's Relative Strength Index）是一种技术分析指标，它是由Nirvana Systems开发的一种改进版的相对强弱指数（RSI）。Connor's RSI与传统RSI的主要区别在于它考虑了价格连续上涨或下跌的天数，也就是所谓的“连胜”（winning streaks）和“连败”（losing streaks）。这种考虑使得Connor's RSI能够更好地反映市场趋势的强度。

在前面介绍了find_runs函数之后，计算streaks就变得非常简单了。

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

这段代码首先将股价序列划分为上涨、下跌和平盘三个子系列，然后对每个子系列计算连续上涨或下跌的天数，并将结果合并成一个新的数组。在streaks中，连续上涨天数要用正数表示，连续下跌天数用负数表示，所以在第5行中，通过np.select将条件数组转换为[1, 0, -1]的序列，后面使用乘法就能得到正确的连续上涨（下跌）天数了。

---

<!-- 
这篇文章是量化场景下的Numpy与Pandas中的一篇。这个系列既介绍基础的Numpy和Pandas，更介绍在量化场景下我们如何灵活运用Numpy和Pandas技巧，写出简洁、高效的代码。示例代码充分证明了这一点。
-->

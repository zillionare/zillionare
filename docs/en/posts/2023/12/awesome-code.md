---
title: "Brilliant Code in Just a Few Lines"
date: 2023-12-19
slug: en/posts/python/awesome-code
tags: [Programming, Algorithms, Quantitative Trading]
excerpt: "From a zero-line project with 50k stars to Quake's fast inverse square root, this tour celebrates tiny code snippets with outsized ingenuity in games and quant trading."
lang: en
translation_of: posts/python/awesome-code
auto_translated: true
source_sha: 392f77c6545c49bee923fb82a668e4d0adc25cda
---

Since indexing in C/Java/Python starts at zero, our roundup also starts with a project that has no lines of code at all.

## 0 Lines: No Code

This project contains zero lines of code, yet boasts lightweight, cross-platform, fully automatic ineffable beauty — and it has earned 50k :star: on GitHub.

<!--more-->

!!! tip
    There's a project on GitHub with 50k stars called [nocode](https://github.com/kelseyhightower/nocode). It truly achieves zero bugs:
    
    _No code is the best way to write secure and reliable applications. Write nothing; deploy nowhere._

    Write no code, and you'll create no bugs. That's pure Zen wisdom: Bodhi is no tree, nor is the mirror a stand; since all is void, where can dust alight? Yet even this project has collected over 3k issues (you file an issue when you think you've found a bug or have a feature request), far above average — that's programmer humor for you.

    <div style="text-align:right"> - From *Python for Big Projects*</div>

To review such a project, you need Confucianism, Buddhism, and Taoism all at once:

!!! quote
    Form is emptiness, emptiness is form.
    The Tao that can be told is not the eternal Tao; the name that can be named is not the eternal name.
    The Tao is beyond words; to speak it is delusion.
    Having read all the code in the world, no code remains in the heart!

## 1 Line: Quake's Magic

This line comes from the game Quake. It's a fast inverse square root algorithm, computing:

$$x^{\frac{-1}{2}}$$

Most people never need this function, but it's essential for light and shadow tracing in games. Rather than explain further, just look at the picture:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/12/quake-vector.png)

I won't elaborate. That picture doesn't look like game development — it looks like a programmer's hairline. The more you study it, the less hair you'll have left.

Anyway, here is that legendary line of code:

```c
i  = 0x5f3759df - ( i >> 1 );
```

It was written by John Carmack. Its brilliance lies in the author's almost Ramanujan-like intuition in discovering the constant 0x5f3759df. The algorithm was even later copied by ChatGPT.

But since this is a quant-focused blog, let's also look at a one-liner used in quant. We mentioned this example when we covered MPT.

## 1 Line: The Dirichlet Distribution

When using Monte Carlo methods to solve for the efficient frontier in MPT, we need to generate countless weight vectors. With n assets, you'd normally write:

```python
import numpy as np

weights = np.array(np.random.random(len(stocks)))
weights = weights/np.sum(weights)  
```

The second line is required to ensure the weights sum to 1. But with a Dirichlet distribution, you can do it in one line:

```python
from numpy.random import dirichlet

w = dirichlet(np.ones(n), n)
```

## 2 Lines: Shuffle

Given n elements, generate a permutation so that every element appears in every position with equal probability. That's the magic of the shuffle algorithm.

```java
for(int i = n - 1; i >= 0 ; i -- )
    // rand(0, i) 生成 [0, i] 之间的随机整数
    swap(arr[i], arr[rand(0, i)]) 
```

Compared with the 0- and 1-line examples, though, this algorithm is far too straightforward. Random number generation and sampling are used everywhere in quant. So here is a more applied example.

Find the max drawdown window in two lines:

```python
import numpy as np
# close是收盘价序列
# 最大回撤结束的位置 最低的那个位置
i = np.argmax((np.maximum.accumulate(close) - close))
# 回撤开始的位置 最高的那个点
j = np.argmax(data['close'][:i])  
```

## ~~4 Lines~~

There's too much room to play here, so we won't give a general example. Instead, here's a time utility often used in quant. When doing feature extraction and backtests, you often need to specify a lookback period. When pulling market data, you need to know the start time — so given an end date, how do you find the timestamp n periods earlier?

For daily bars, the math isn't complicated, but you need a trading calendar to exclude market holidays.

For intraday bars, such as 30-minute bars, it's much trickier. You have to handle both market holidays and overnight gaps. The zillionare quant framework offers a space-for-time approach. It first expands the 30-minute ticks for period n and merges them with dates, turning the calculation into a linear one:

```python
tm = moment.hour * 60 + moment.minute

new_tick_pos = cls.ticks[frame_type].index(tm) + n
days = new_tick_pos // len(cls.ticks[frame_type])
min_part = new_tick_pos % len(cls.ticks[frame_type])

```
---
---
```python
date_part = cls.day_shift(moment.date(), days)
minutes = cls.ticks[frame_type][min_part]
h, m = minutes // 60, minutes % 60

```

The ticks array used in the code looks like this at the 30-minute level:

```
ticks = [600, 630, ..., 900]
```

600 means 10:00 AM. A day_shift function is used here, which simply searches using the trading calendar. As a final optimization, modulo arithmetic replaces the actual expansion of the ticks array, saving memory as well. That's very useful when `n` is large.

Building quant systems involves writing plenty of low-level utility functions. If you don't have time to write your own, take a look at the code in the zillionare quant framework.

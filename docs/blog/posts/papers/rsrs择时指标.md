---
title: "RSRS择时指标"
date: 2025-06-09
category: papers
img: https://images.jieyu.ai/images/2025/05/20250514202750.png
tags: 
    - papers
---

回测表明，RSRS因子在2005年3月到2017年3月的上证50指数上，12年总收益1432.36%，年化24.84%，夏普比1.42。同期指数收益为290.13%。

该指标的大致思想是，将每日最高价与最低价分别视为阻力位与支撑位，把给定周期下线性回归拟合得到的斜率作为因子。斜率越陡，表示市场强度越强。

本文复现了RSRS因子，并附有可运行的完整代码和数据。

<!--more-->

RSRS(Resistance Support Relative Strength)因子是光大证券于2017年起的系列中，提出的一种择时因子。该系列最初发表于2017年，后来又在2019年和2021年对之前的因子构造进行了回顾和优化。这篇notebook将复现这一因子，并对其构造思想进行解读。

这是我们系列研报解读中的一篇。持续跟踪本系列文章，你将掌握复现研报所需要的理论知识、编程技巧、数据获取方案和交易策略经验，换言之，成为一名熟练的策略研究员。

在解读每一篇研报时，我们都会选附上研报原文：

![](https://images.jieyu.ai/images/2025/05/pdf.jpg)

然后才是我们对研报的解读和复现：

![](https://images.jieyu.ai/images/2025/05/rsrs.jpg)

通过对比，你可以发现我们对研报进行了提炼和挖掘，主题思想更明确，也更容易读懂。

该策略的主要思想是：

!!! tip
    1. 最高价与最低价是经当日全体市场参与者的交易行为所认可的阻力与支撑。
    2. 在相邻的两个时间点[T0, T1]之间，最高价High的变化值 $\Delta_H = High(T1) - High(T0)$ 和最低价Low的变化值 $\Delta_L = Low(T1) - Low(T0)$，这两个变化的比值反应了阻力位与支撑位的相对强度，即RSRS指标。
    3. 为了过滤噪声，一般取$T_1, T_2, ...T_n$间的最高价和最低价进行线性回归，此时得到的斜率$\beta$即为RSRS指标，在本质上与定义2相同，即有以下公式：<br>

    $$
    high = alpha + beta * low + epsilon, epsilon ~ N(0, sigma)
    $$


应该说策略的思想非常巧妙，也很符合我们的交易认知：**如果市场投资者认为下面的支撑很强，就敢于向上试探更大的空间，因此最高价的涨幅就变大；如果市场投资者认为上方的压力很大，则更愿意抛售，从而导致最低价格的跌幅变大**。

研报还展示了如何为交易思想建模的一个简单但常用的技巧，即线性回归。线性回归是从简.丁伯格等人开创计量经济学以来，在经济和金融领域广泛使用的一种技巧。在这里，线性回归的引入，让交易思想得到合理的抽象，成为有统计实证支持的一个模型。

这个因子的计算方法如下：

```python
import pandas as pd

def calc_rsrs_factor(df: pd.DataFrame, win: int = 18):
    df = df.copy()

    # 计算滑动窗口的协方差 Cov(low, high)
    rolling_cov = df['low'].rolling(window=N).cov(df['high'])

    # 计算滑动窗口的方差 Var(low)
    rolling_var = df['low'].rolling(window=N).var()

    df['RSRS'] = rolling_cov / rolling_var

    return df
```


!!! tip
    在这里我们使用了一个快速的向量化算法。如果你感到难以理解这个算法，那么，它对应的vanilla版本是这样:

    ```python
    def calc_rsrs_vanilla(df, N):
        df = df.copy()
        temp = [np.nan] * N

        for row in range(len(df) - N):
            y = df['high'][row : row + N]
            x = df['low'][row : row + N]

            # 确保x和y的长度都为N，并且没有NaN值
            if len(x) == N and len(y) == N and not x.isnull().any() and not y.isnull().any():
                beta = np.polyfit(x, y, 1)[0]
                temp.append(beta)
            else:
                temp.append(np.nan)

        df['RSRS'] = temp
        return df
    ```
    
    在对比测试中，vanilla版本的运行时间如果是4.3ms的话，那么向量化版本的运行时间则仅为317us，快了10倍多。


<!-- BEGIN IPYNB STRIPOUT -->
!!! tip
    看了很多研报，但却不知道如何复现？2025年，你应该加入匡醍研究平台，手把手带你复现研报。全年仅360元，即可享有超100份研报、复现代码及运行环境！在该运行环境中，提供了 Tushare 高级账户使用权（官方价格500元），仅此一项，就值回票价！
<!-- END IPYNB STRIPOUT -->

现在，我们通过tushare的数据，来看一下因子计算的结果。

```python
hs300 = pro.index_daily(ts_code = "000300.SH", start_date = "20250101", end_date = "20250601")
hs300.index = pd.to_datetime(hs300["trade_date"])
hs300 = hs300.sort_index(ascending=True)
```

!!! tip
    在使用tushare的行情数据时，请务必按照这里的代码片段，先将trade_date设置为索引，然后进行排序，这样得到的数据的顺序，才会与大多数软件系统中的顺序一致。

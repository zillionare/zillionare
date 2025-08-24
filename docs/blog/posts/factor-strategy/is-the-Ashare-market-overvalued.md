---
title: A股现在被高估了吗？
date: 2024-10-26
category: factor&strategy
slug: is-the-ashare-market-overvalued
motto: "温故而知新"
img: https://images.jieyu.ai/images/2024/10/tushare-pe-plot.png
stamp_width: 60%
stamp_height: 60%
tags: [strategy, pe, tushare]
---

## 温故而知新

在2024年9月，我们曾发表[《节前迎来揪心一幕！谁来告诉我，A股现在有没有低估？》](https://www.zillionare.com/blog/posts/factor-strategy/Is-the-A-share-market-undervalued.html)一文。在那篇文章中，我们使用了`akshare`获取了上证指数的市盈率数据，并通过分位数和趋势分析，探讨了当时A股市场的估值情况。

当时我们的结论是：

> 如果仅从分位数统计来看，当下的A股是低估的。但如果考虑到市盈率总体上一直处在上升的趋势，以及最近一年来PE与指数涨跌的背离情况，判断A股是否已经低估还存有疑问，应该纳入更多维度进行判断。

现在是2025年8月，差不多快一年了。现在数据会是什么状况？

## 使用 Tushare 获取市盈率

Tushare是一个功能强大的金融数据平台，提供了丰富的A股市场数据。我们可以通过它的`daily`接口，获取到每日的市盈率（PE）数据。

首先，我们需要初始化tushare。请确保你已经安装了`tushare`库，并拥有自己的token。

然后，我们就可以获取上证指数的每日市盈率数据了。

```python
import pandas as pd

pro = ts.pro_api()

# 获取上证指数的每日PE数据
df = pro.index_daily(ts_code='000001.SH', fields='trade_date,pe_ttm')
df.rename(columns={'trade_date': 'date', 'pe_ttm': 'pe'}, inplace=True)
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)
df.sort_index(inplace=True)
df.head()
```

## 当前的估值水平

我们同样可以通过分位数来分析当前的估值水平。

```python
percentiles = []
for i in range(1, 4):
    percentiles.append(df["pe"].quantile(i/4))

print(percentiles)
```

我们发现，从tushare获取的数据来看，25%， 50%和75%分位数分别是 12.5, 14.8和 18.9。

接着，我们计算当前（以2024年10月25日为例）的PE在历史数据中所处的分位数。

```python
from datetime import datetime

rank = df.rank().loc[datetime(2024,10,25), "pe"]
percentile = rank / len(df)
print(f"当前PE分位: {percentile:.2%}")

```

结果显示，当前的市盈率处在 **85%** 分位数左右，这是一个相当高的位置。这与我们一个月前使用`akshare`数据得出的结论（10.6%分位数）大相径庭。

## 趋势分析

为了更直观地理解，我们同样将PE的走势绘制出来。

```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

fig, ax = plt.subplots(figsize=(12,6))

color = "tab:red"
ax.plot(df.index, df["pe"], label="PE", color=color)
ax.set_xlabel("Year")
ax.set_ylabel("PE", color=color)
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

for i in range(1, 4):
    quantile = df["pe"].quantile(i/4)
    ax.axhline(quantile, color='gray', linestyle='--', label=f"{i/4:02.0%}")

plt.title("SSE Index PE Ratio (via Tushare)")
plt.legend(loc="upper left")
plt.grid(True)
plt.show()
```

![Tushare PE Plot](https://images.jieyu.ai/images/2024/10/tushare-pe-plot.png)

从图上可以清晰地看到，当前的PE值确实处于一个相对较高的历史位置。

## 结论

通过使用`tushare`的数据进行分析，我们得出了与前文截然不同的结论。`tushare`的数据显示，当前A股市场（以上证指数为例）的市盈率处在历史高位，存在高估的风险。

为什么不同的数据源会给我们带来如此大的差异呢？这可能与数据清洗、计算口径等多种因素有关。这也提醒我们，在进行量化分析时，数据源的选择和交叉验证是何等重要。

那么，A股现在究竟是被高估了还是低估了？或许，真相就在不同的数据源和分析方法的交叉验证之中。作为投资者，我们需要保持警惕，多维度地去审视市场，才能做出更明智的决策。
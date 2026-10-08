---
title: "How to Build Alpha 101: Quant Coding, Overfitting, and Noise Testing"
date: 2024-08-25
slug: en/posts/uncategory/weekly-0825
tags: [Factor Investing, Quant Coding, Overfitting, Noise Testing]
excerpt: "A technical guide to implementing World Quant’s Alpha 101 factors, optimizing quant coding with mask arrays, and detecting overfitting via noise testing and parameter plains."
lang: en
translation_of: posts/uncategory/weekly-0825
auto_translated: true
source_sha: 4da94fa3d56ff8de9fb928ca52ec75a99520cf94
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/kenneth-griffin.jpg"
---

### This Week’s Highlights

* Fed Chair Powell signals that the time for rate cuts has arrived.
* JPMorgan executes massive Hong Kong stock position transfers, involving over HK$1.1 trillion in market cap.

### Next Week’s Watchlist

* Guangfa Fund’s star manager Liu Gesong’s first “three-year holding period” fund matures, with losses exceeding 58%.
* Thursday: A50 index expiration; Friday: Month-end closing.
* Saturday: Release of August official manufacturing PMI.

### This Week’s Selection

* How to Implement Alpha 101?
* Efficient Quant Coding: Mask Arrays and Find Runs
* Beyond In-Sample Testing: Other Methods for Detecting Overfitting

---

## News Details

* **Fed Chair Powell signals rate cut timing:** “Inflation is only half a percentage point above the Fed’s 2% target, and the unemployment rate is rising. The time for policy adjustment has arrived.” <claimer>Cailian Press</claimer>
* **JPMorgan’s massive HK stock position transfer:** JPMorgan recently executed large-scale transfers of its Hong Kong stock positions, involving a market cap exceeding HK$1.1 trillion. After the transfer, its ranking in securities firm holdings dropped from 4th to 14th, with holdings falling below HK$200 billion. One month prior, JPMorgan had also executed transfers exceeding HK$600 billion. <claimer>JRJ Financial</claimer>
* **Guangfa Fund’s “three-year holding period” fund matures with significant losses:** The first “three-year holding period” fund managed by star Guangfa Fund manager Liu Gesong is nearing maturity. Initial fundraising was RMB 14.87 billion. As of August 22 this year, the fund (Class A/C) has lost over 58% since inception. Recently, a batch of three-year holding period funds has matured simultaneously. Looking back, between 2021 and 2022, the public fund industry densely launched at least 73 three-year holding period active equity funds. <remark>After the lock-up period ends, will investors redeem en masse? This is one of the most critical volatility factors next week. Relevant authorities are likely prepared.</remark> <claimer>Sina Finance</claimer>
* **One year since Beijing Business Today’s “Foreign Capital” commentary:** On August 25, Beijing Business Today published “Foreign Capital Ignores A-Shares Today, Will Be Out of Reach Tomorrow” one year ago. The commentary argued that during a period of extremely high investment value in A-shares, some foreign capital flowing out might represent typical technical traders who are hesitant about indices. They will eventually regret it; when they return, they will have to pay higher prices. As the saying goes, “Ignore A-shares today, and they will be out of reach tomorrow.” <remark>The day after this commentary was published, the Shanghai Composite Index opened at 3,219 points. One year later, it closed at 2,854 points.</remark>

---

# How to Implement Alpha 101?

In 2015, World Quant published the report [《101 Formulaic Alphas》](https://arxiv.org/pdf/1601.00991), which contains 101 different stock selection factors. 80% of these factors were already being used in World Quant’s trading at the time. Following the report’s publication, it generated significant interest in the industry.

Currently, factor libraries generated based on Alpha 101 have become essential for most quantitative platforms, data providers, and quant institutions. Furthermore, inspired by this, some institutions have built additional factors, such as Guotai Junan’s [Alpha 191](https://blog.quantide.cn/assets/ebooks/国泰君安－基于短周期价量特征的多因子选股体系.pdf). Both factor libraries have been implemented by institutions. For example, [DolphinDB](https://github.com/dolphindb/DolphinDBModules/tree/master/gtja191Alpha) and [JoinQuant](https://www.joinquant.com/help/api/help#Alpha101:WorldQuant101Alphas%E5%9B%A0%E5%AD%90%E5%87%BD%E6%95%B0%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E) both provide these factor libraries.

This article introduces how to understand and implement 《101 Formulaic Alphas》. The content is excerpted from Lesson 8 of our course, “Factor Analysis and Machine Learning Strategies.” Due to space constraints, some parts are omitted.

## Data and Operators in Alpha 101

Before implementing Alpha 101 factors, we must first understand the data and basic operators used in their formulas.

Alpha 101 factors are primarily constructed based on price and volume. Only a small fraction of Alpha factors use fundamental data, including market-cap data and industry classification data [^fundmental_data].

!!! tip
    In the China A-shares market, due to concerns about the reliability of financial report data [^fraut] and the lack of T+0 trading and short-selling mechanisms, price inefficiencies generated by trading behavior in the short term are very common. Therefore, short-term price-volume factors are currently more effective than fundamental factors.

---

In price-volume data, Alpha 101 relies on the most raw data: OHLC, volume (turnover amount), amount (trading volume), turnover (turnover rate), and from this, calculates returns (daily price change) and vwap (volume-weighted average price).

The calculation methods for returns and vwap are as follows:

```python
# THE NUMPY WAY
vwap = bars["amount"] / bars["volume"] / 100
returns = bars["close"][1:]/bars["close"][:-1] - 1

# THE PANDAS WAY
vwap = df.amount / df.volume / 100
returns = df.close.pct_change()
```

In addition, to understand Alpha 101, it is crucial to understand its common operators. There are approximately 30 operators in Alpha 101. Some, such as `abs`, `log`, `sign`, `min`, `max`, and mathematical operators (`+`, `-`, `*`, `/`), do not require explanation.

Below, we will explain the operators that require clarification one by one.

### Ternary Operator

The ternary operator exists in C programming but not in Python. It can be expressed as: `"x ? y : z"`, which is equivalent to Python’s:

```python
expr_result = None

if x:
    expr_result = y
else:
    expr_result = z
```

### Rank

In Alpha 101, there are two types of `rank`: one is cross-sectional, ranking all stocks in the universe at the same time point; the other is time-series, ranking the same stock over time.

---

The cross-sectional `rank` directly calls DataFrame’s `rank`. For example,

```python
import pandas as pd

data = {
    'asset': ["000001", "000002", "000004", "000005", "000006"],
    'factor': [85, 92, 78, 92, 88],
    'date': [0] * 5
}
df = pd.DataFrame(data).set_index('date').pivot(index=None, columns="asset", values="factor")

def rank(df):
    return df.rank(axis=1, pct=True, method='min')
```

<!-- This code can also be implemented using bottleneck's rank_data
import bottleneck as bn

# Example data
data = [85, 92, 78, 92, 88]

# Calculate rank
ranked_data = bn.rankdata(data)/len(data)

print(ranked_data)

-->

In the code above, `date` is the index, column names are the assets, and `factor` is the value. We can sort the factor values of each asset cross-sectionally using `rank(axis=1)`. When using the `axis=1` parameter, the index is not involved in sorting. `pct=True` indicates returning percentage ranks, while `False` returns integer ranks.

Sometimes we also need to sort in the time series. In Alpha 101, this type of sorting is defined as `ts_rank`, distinguished from cross-sectional `rank` by the `ts_` prefix. Henceforth, when we see the `ts_` prefix, we should understand it similarly.

```python
from bottleneck import move_rank

def ts_rank(df, window=10, min_count=1):
    return move_rank(df, window, axis=0, min_count=min_count)
```

Here we use `move_rank` from `bottleneck`, which is significantly faster than similar implementations in `pandas` and `scipy`. If implemented using `pandas`, the code would be:

```python
def rolling_rank(na):
    return rankdata(na,method='min')[-1]

def ts_rank(df, window=10):
    return df.rolling(window).apply(rolling_rank)
```

Note that `[-1]` on line 3 is mandatory.

---

The usage of `rank` and `ts_rank` is most typical in Alpha 004. This factor is:

```python
# ALPHA#4	 (-1 * TS_RANK(RANK(LOW), 9))
def alpha004(low):
    return -1 * ts_rank(rank(low), 9)
```

Here, the parameter `low` is a wide DataFrame with assets as columns, dates as the index, and the daily low price as the value. Below, we look at the results of calling `rank` and `ts_rank` sequentially on the parameter `low`. After examining a few examples, we can quickly understand the Alpha 101 factor calculation process.

```python
from bottleneck import move_rank
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

df = pd.DataFrame(
       [[6.18, 19.36, 33.13, 14.23,  6.8 ,  6.34],
       [6.55, 20.36, 32.69, 14.52,  6.4,  6.44 ],
       [7.  , 20.79, 32.51, 14.56,  6.0 ,  6.54],
       [7.06, 21.35, 33.13, 14.47,  6.5,  6.64],
       [7.03, 21.56, 33.6 , 14.6 ,  6.5,  6.44]], 
       columns=['000001', '000002', '000063', '000066', '000069', '000100'], 
       index=['2022-01-04', '2022-01-05', '2022-01-06', '2022-01-07', '2022-01-10'])

def rank(df):
    return df.rank(axis=1, pct=True, method='min')

def ts_rank(df, window=10, min_count=1):
    return move_rank(df, window, axis=0, min_count=min_count)

df
rank(df)

-1 * ts_rank(rank(df), 3)
```

Example [](#example-7) outputs three DataFrames sequentially. We see that `rank` is executed on rows, ranking stocks by their lowest price; `ts_rank` is executed on columns, ranking the cross-sectional ranks of each stock, reflecting changes in the lowest position.

For example, stock 000100 was in the 33rd percentile of cross-sectional ranking on January 4, 2022, but dropped to the 16.7th percentile on January 10.

---

After `ts_rank`, its final factor value on January 10 is 1, reflecting the fact that its cross-sectional ranking dropped. Similarly, for stock 000001, its cross-sectional ranking on January 4 was 16.7% (lowest), but on January 5, its ranking rose to 50%. Its final factor value on that day is -1, reflecting the rise in its cross-sectional ranking.

!!! tip
    Through the Alpha 004 factor, we not only learn the usage of `rank` and `ts_rank` but also understand the difference between cross-sectional and time-series operators. Additionally, we learn that to facilitate the calculation of Alpha 101 factors, the optimal data organization method might be to organize basic data (such as OHLC) into wide tables with dates as the index and assets as columns, facilitating calculations in both directions (cross-sectional and time-series).

### ts_*

This group of operators, in addition to `ts_rank` introduced earlier, includes `ts_max`, `ts_argmax`, `ts_argmin`, and `ts_min`. These operators have two parameters: first, the time series (e.g., `close` or `open`), and second, the sliding window length.

Note that these operators must be performed on a sliding window to avoid introducing future data.

In addition, other common statistical functions such as `min`, `max`, `sum`, `product`, `stddev`, etc., although they do not use the `ts_` prefix, are also time-series operators, not cross-sectional operators. Since we have already detailed the usage of time-series operators through `ts_rank`, and everyone is familiar with the roles of these other operators, we will omit them here.

### delay

In Alpha 101, the `delay` operator is used to retrieve data from n days ago. For example,

---

```python
def delay(df, n):
    return df.shift(n)

data = {
    'date': pd.date_range(start='2023-01-01', periods=10),
    'close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]
}
df = pd.DataFrame(data)

delay(df, 5)
```

In this way, when calculating the factor on the 5th day, we use the `close` data from 5 days ago, i.e., the `close` at the original index 0.

### correlation and covariance

`correlation` is the Pearson correlation coefficient of two time series on a sliding window. This operator can be implemented as:

```python
def correlation(x, y, window=10):
    return x.rolling(window).corr(y).fillna(0).replace([np.inf, -np.inf], 0)

def covariance(x, y, window=10):
    return x.rolling(window).cov(y)
```

Note that here, although we only call `rolling` on `x`, when calculating the correlation coefficient, it has been verified that `y` also slides with the same window.

<!-- Exercise:

Compare:

```python
x = pd.Series(np.arange(10))
y = pd.Series([1,2,3,4,5, 4, 3, 2, 1, 0])

x.rolling(5).corr(y)
```

and

```python
for i in range(5, 10):
    xi = x.iloc[i-5:i].values
    yi = y.iloc[i-5:i].values
    print(np.round(np.corrcoef(xi, yi)[0,1], 2))
```

-->

### scale

According to Alpha 101’s explanation, the purpose of this operator is to scale the elements of an array so that `sum(abs(x)) = a`, with the default `a = 1`. It can be implemented as:

```python
def scale(df, k=1):
    return df.mul(k).div(np.abs(df).sum())
```

---

### decay_linear

The purpose of this operator is to linearly weight-decay the elements in a time series of length `d`, so that the sum is 1, with later elements having larger weights.

```python
def decay_linear(df, period=10):
    weights = np.array(range(1, period+1))
    sum_weights = np.sum(weights)
    return df.rolling(period).apply(lambda x: np.sum(weights*x) / sum_weights)
```

### delta

Equivalent to `dataframe.diff()`.

### adv{d}

Simple moving average of trading volume over d days.

### signedpower

`signedpower(x, a)` is equivalent to `x^a`.

## Alpha 101 Factor Interpretation

<claimer>This part is omitted</claimer>

## Open-Source Alpha 101 Factor Analysis Library

The best way to fully explore the factors defined in Alpha 101 is to calculate all these factors based on historical data and backtest them using Alphalens or even backtrader. [popbo](https://github.com/popbo/alphas) has implemented such functionality.

---

Running this library requires installing `alphalens`, `akshare`, `baostock`, and `jupyternotebook`. Before conducting research, you must download data and calculate factors according to its README file. Then, you can open `research.ipynb` to analyze the annual performance of each factor.

In our supplementary materials, we provide the complete source code for this project, which can be run in our course environment.

---

## Efficient Quant Coding: Mask Array and Find Runs

In many quantitative scenarios, we need

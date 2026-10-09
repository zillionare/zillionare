---
title: "Building the Net-High-NL Factor for Sector Trends"
date: 2023-12-24
slug: en/posts/factor-strategy/nh-nl
tags: [Factor Investing, Quantitative Trading, XtQuant, Momentum Factor]
excerpt: "Learn to construct the Net-High-NL (NHNL) factor using anchor effect theory. This guide covers factor definition, signal thresholds, and Python implementation via XtQuant for momentum and reversal strategies."
lang: en
translation_of: posts/factor-strategy/nh-nl
auto_translated: true
source_sha: b15dc8d9e0e8f774c05befd395e2d3e400f3d759
---

Individual stock highs and lows are hard to gauge due to their high randomness. A chairman might flee, or a stock might encounter sudden positive news (e.g., a competitor’s warehouse catches fire). At individual stock peaks and troughs, **emotion dominates, rationality retreats, and technical indicators become钝ated (blunted)**, entering a state where <red>the current situation is indescribable, and anything is possible</red>.

However, industry indices, as superpositions of multiple random variables, exhibit certain regularities (we exclude A4 systemic shocks for now, as they don’t happen daily). This is where **factor analysis** and **technical analysis** can shine.

<!--more-->

Today, we introduce the **Net-High-NL (NHNL)** factor, which can capture sector strength/weakness trends and reversals. Based on this factor, we can construct index-enhancement strategies.

!!! tip TakeAway
    1. How to define the NHNL factor
    2. The anchor effect is the cornerstone of this factor
    3. From factor to strategy implementation
    4. How to use XtQuant to obtain data

## Factor Definition

The Net-High-NL indicator refers to the percentage of stocks in an industry index that have reached their annual high minus those that have reached their annual low, relative to the total number of stocks in the industry:

$$
    (NHNL)\% = (count(HHV) - count(LLV))/N
$$


!!! tip
    As the factor definition shows, it is not uniformly distributed in the [-1, 1] interval. Using this scheme in **machine learning** may cause slight gradient optimization difficulties. Although we could mimic the RSI approach and transform it into:

    $$
        (NHNL)\% = (count(HHV) - count(LLV))/(count(HHV) + count(LLV))
    $$

    Doing so clearly lacks corresponding logic. This is a point to note during **factor analysis**. Do not apply rigid rules where they don’t fit.

## Logic Behind the Factor

The primary financial principle behind this factor is the **anchor effect**. Behavioral finance tells us that most investors have a strong anchor effect. Investors always use the price at which they bought the stock/fund (i.e., the **anchor cost**) as a benchmark, viewing their accounts as either in floating profit or floating loss, to determine their operations.

Stocks reaching annual highs have holders in floating profit. Even if they plan to sell, they hope for further market rises, so their selling pressure is relatively small. Conversely, stocks reaching annual lows have holders in floating loss. Thus, whenever the market rebounds, investors sell, creating larger selling pressure. This creates the pattern of "no bottom in a bear market, no top in a bull market," or the adage that "after a new high, there is another new high; after a new low, there is another new low."

!!! tip
    When does this trend reverse? The above effect is essentially a **momentum factor**. When momentum continues, the power of reversal factors also accumulates. At this time, you can monitor reversal factors such as whether the monthly RSI has reached previous highs. If the monthly RSI reaches previous highs and confirmation signals appear, a quarterly top is likely to emerge.

Based on this principle, the Net-High-NL factor clearly characterizes the strength or weakness of industry indices.


## Signal Construction

Huafu Securities provided the following reference indicators using CITIC Level-1 industry indices as an example:

$$
NHNL = \begin{cases} 
        x \geq 30\% \ 贪婪\\\
        20\% \leq x \lt 30\% \ 乐观\\\
        -20\% \lt x \lt 20\% \ 正常区间\\\
        -30\% \lt x \leq -20\% \ 悲观\\\
        x \leq -30\% \ 恐惧
\end{cases}
$$

To prevent excessive fluctuations caused by too few stocks in Level-1 industry indices, they recommend relaxing the thresholds to ±30%/40% when the number of stocks listed for more than 1 year in a Level-1 industry index is less than 40.

It is recommended to use the indicator as follows (taking one-sided long positions as an example):

1. When NHNL enters the optimistic zone, start building positions; this is a **momentum strategy**.
2. When NHNL enters the greedy zone, watch for potential reversals. The first drop from the greedy zone back to the optimistic zone generates a short signal; sell at the next trading day’s open.
3. When NHNL enters the panic zone, watch for potential reversals. The first rise from the panic zone back to the pessimistic zone generates a buy signal at the next trading day’s open. Note to set stop-loss levels; hold only if the rebound continues.

## Code

The key to the code is obtaining industry index and constituent stock quotes, as calculating highs and lows within a year is straightforward.

We demonstrate using XtQuant. XtQuant is a market data and live trading interface developed by Xuntou. If you activate quantitative trading permissions, you can obtain market data for free, making it another excellent free data source. We detailed its usage in Lesson 24.



```python
sectors = set()

for item in get_sector_list():
    for i in range(6, 1, -1):
        key = item[:i]

        if key.startswith("SW1"):
            sectors.add(key)
            break
print(sectors)

# Display:
'SW1煤炭', 'SW1交通运', 'SW1综合', 'SW1通信' ...
```

We obtain approximately 40 Shenwan Level-1 sector names. Next, we need to obtain the security codes for each constituent stock within the sector:

```python
xt.get_stock_list_in_sector("SW1煤炭")

# Display:

['600121.SH',
 '600123.SH',
 '600157.SH',
 '600188.SH',
 '600348.SH',
 '600395.SH',
 ...
]
```

The method for obtaining individual stock quote data was detailed in recent notes, so we won’t repeat it here.

!!! tip
    Mastering the acquisition of security lists and then iterating through them to obtain quote data is a basic method. It is also the API you must master first when learning a data source. This is something we have introduced to you since Lesson 1.


More code is not demonstrated one by one. We provide an example notebook. Ultimately, we can achieve an effect like this:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/12/nhnl.png)


## Quiz

Please explain why the Net-High-NL factor is not uniformly distributed in the [-1, 1] interval. How many seconds did it take you to reach the conclusion?

<claimer>Refined and rewritten based on Huafu Securities’ "Market Sentiment Indicator Special Report (Part V)". Special thanks!</claimer>

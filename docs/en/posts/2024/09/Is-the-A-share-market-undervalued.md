---
title: "Is China A-Shares Undervalued? PE Trap vs. Opportunity ===EXCUTIVE SUMMARY=== An analysis of Shanghai Composite PE reveals a divergence between price and earnings, warning of a low-PE trap despite statistical undervaluation. ===TAGS=== Factor Investing, Valuation Analysis, China A-Shares, Quantitative Trading ===BODY=== Before the holiday, a heart-stopping scene unfolded as major indices hit their lowest weekly closes of the year. Naturally, we ask: What is the current market state? Are there undervaluation opportunities? This article explores whether we are facing an opportunity or a trap from the perspective of price-to-earnings (PE) ratios.  We use `akshare` to retrieve the Shanghai Composite PE data. Note that this data originates from the Legu Legu website.  ```python import akshare as ak  pe = ak.stock_market_pe_lg(symbol=\"上证\") pe.set_index(\"日期\", inplace=True) pe.index.name = \"date\" pe.rename(columns={\"平均市盈率\": \"pe\", \"指数\": \"price\"}, inplace=True) pe.tail(15) ```  This retrieves all data since 1999, formatted as follows:  ![Table 1 PE vs Index](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/09/pe-vs-index.jpg)  ## Undervalued in August?  We can identify the 25th, 50th, and 75th percentiles of the PE using the `quantile` function:  ```python percentiles = [] for i in range(1, 4):     percentiles.append(pe[\"pe\"].quantile(i/4))  percentiles ```  Since 1999, the 25th, 50th, and 75th percentiles have been 13.9, 17.4, and 33.5, respectively.  So, where does the Shanghai Composite PE stand at the end of last month (August 2024)?  We can calculate this position as follows:  ```python rank = pe.rank().loc[datetime.date(2024,8,30), \"pe\"] percentile = rank / len(pe) percentile ```  The results show that the current PE is at approximately the 10.6th percentile, a relatively low position since 1999.  Based solely on statistical data, it appears the Shanghai Composite was undervalued at the end of August 2024—implying a buying opportunity.  However, **percentiles are static and do not reflect the trend of the data**.  ## PE Trends  If you open the East Money client and view the Shanghai Composite’s profile, you can see its historical PE trend. The chart over the past decade is as follows:  ![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/09/eastmoney-pe-stats.png)  This chart also offers no new insights; it suggests the Shanghai Composite remains undervalued.  Let’s overlay historical price trends onto the PE trends to see if PE peaks and troughs correspond to price peaks and troughs.  ```python import matplotlib.pyplot as plt import matplotlib.dates as mdates  fig, ax1 = plt.subplots(figsize=(60,6))  color = \"tab:blue\" ax1.plot(pe[\"price\"], label=\"Index\", color=color) ax1.set_xlabel(\"Year\") ax1.set_ylabel(\"Index\", color=\"tab:blue\") ax1.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[2, 5, 8, 11])) ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))   color = \"tab:red\" ax2 = ax1.twinx() ax2.plot(pe[\"pe\"], label=\"PE\", color=color) ax2.set_ylabel(\"PE\", color=color)  for i in range(1, 4):     quantile = pe[\"pe\"].quantile(i/4)     ax2.axhline(quantile, color='gray', linestyle='--', label=f\"{i/4:02.0%}\")  plt.title(\"Index vs PE\")  fig.tight_layout() for date in pe.index[::3]:     ax1.axvline(date, color='gray', linestyle=':', linewidth=0.5) plt.gcf().autofmt_xdate()  plt.legend(loc=\"upper left\") plt.show() ```  This generates the following plot:  ![1999-2024](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/09/index-vs-pe-1999-2024.png)  From 1999 to 2024, there is a general trend of rising Shanghai Composite prices alongside falling PE ratios. The rise in index prices likely reflects the long-term trend of GDP growth, while the decline in PE is primarily due to the expansion of asset supply, which continuously squeezes out asset bubbles.  To examine details, we split the above chart into five subplots:  ![Jan 1999 - May 2004](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/09/index-vs-pe-199901-200405.jpg)  ![Jun 2004 - May 2009](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/09/index-vs-pe-200402-2009-05.png)  ![Jun 2009 - Jul 2014](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/09/index-vs-pe-2009-06-2014-08.png)  ![Jun 2014 - Oct 2019](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/09/index-vs-pe-2014-05-2019-11.png)  ![Aug 2019 - Aug 2024](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/09/index-vs-pe-2019-08-2024-08.png)  ## Reflections and Conclusions  *   **Question:** In which periods do PE trends and Shanghai Composite prices move in perfect lockstep? In such movements, which is the dependent variable and which is the independent variable? What phenomenon does this reflect? *   **Answer:** Between 1999–2001, August 2005–May 2008, and May 2014–May 2015, PE trends mirrored the Shanghai Composite exactly. During these periods, intense market speculation meant that changes in corporate earnings were negligible compared to price changes. Consequently, PE trends were entirely driven by stock prices, resulting in highly similar curves for PE and price. The emergence of such phenomena indicates excessive market speculation.  *   **Question:** Since approximately August 2023, it appears the Shanghai Composite has declined faster than PE. For instance, in February 2024, both the index and PE hit阶段性 lows. However, in September 2024, while the index hit a new low, PE did not. What phenomenon does this divergence reflect? Can it be described using a common term? *   **Answer:** In September 2024, the Shanghai Composite hit a new low, but PE did not, creating a divergence. This can also be observed through peak analysis. For example, in June 2024 (see Table 1), PE reached a new high since August 2023, while the index remained below any high point since August 2023. This divergence can be described as a **low-PE trap**. This indicator reminds us that while the index is falling, the profitability of listed companies may also be declining, leading to scenarios where the index rises slightly while PE surges, or the index falls significantly while PE declines only slightly.  Therefore, based solely on percentile statistics, current China A-shares appear undervalued. However, considering the overall downward trend of PE and the recent divergence between PE and index movements over the past year, determining whether A-shares are truly undervalued remains questionable. More dimensions should be incorporated into the judgment.  *This article is derived from the exercises in Lesson 2 of \"Factor Analysis and Machine Learning Strategies.\"*"
date: 2024-09-16
slug: en/posts/factor-strategy/Is-the-A-share-market-undervalued
tags: [Factor Investing, Valuation Analysis, China A-Shares, Quantitative Trading]
excerpt: "上证PE跌至1999年以来10.6%分位，看似低估却是低PE陷阱？本文用akshare数据揭示价格与盈利背离，量化视角拆解估值真相。"
lang: en
translation_of: posts/factor-strategy/Is-the-A-share-market-undervalued
auto_translated: true
source_sha: 41eb867eaa6e60d8be14405cfa66f8c1cb37d655
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/09/eastmoney-pe-stats.png"
---

Before the holiday, a heart-stopping scene unfolded as major indices hit their lowest weekly closes of the year. Naturally, we ask: What is the current market state? Are there undervaluation opportunities? This article explores whether we are facing an opportunity or a trap from the perspective of price-to-earnings (PE) ratios.

We use `akshare` to retrieve the Shanghai Composite PE data. Note that this data originates from the Legu Legu website.

```python
import akshare as ak

pe = ak.stock_market_pe_lg(symbol="上证")
pe.set_index("日期", inplace=True)
pe.index.name = "date"
pe.rename(columns={"平均市盈率": "pe", "指数": "price"}, inplace=True)
pe.tail(15)
```

This retrieves all data since 1999, formatted as follows:

![Table 1 PE vs Index](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/09/pe-vs-index.jpg)

## Undervalued in August?

We can identify the 25th, 50th, and 75th percentiles of the PE using the `quantile` function:

```python
percentiles = []
for i in range(1, 4):
    percentiles.append(pe["pe"].quantile(i/4))

percentiles
```

Since 1999, the 25th, 50th, and 75th percentiles have been 13.9, 17.4, and 33.5, respectively.

So, where does the Shanghai Composite PE stand at the end of last month (August 2024)?

We can calculate this position as follows:

```python
rank = pe.rank().loc[datetime.date(2024,8,30), "pe"]
percentile = rank / len(pe)
percentile
```

The results show that the current PE is at approximately the 10.6th percentile, a relatively low position since 1999.

Based solely on statistical data, it appears the Shanghai Composite was undervalued at the end of August 2024—implying a buying opportunity.

However, **percentiles are static and do not reflect the trend of the data**.

## PE Trends

If you open the East Money client and view the Shanghai Composite’s profile, you can see its historical PE trend. The chart over the past decade is as follows:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/09/eastmoney-pe-stats.png)

This chart also offers no new insights; it suggests the Shanghai Composite remains undervalued.

Let’s overlay historical price trends onto the PE trends to see if PE peaks and troughs correspond to price peaks and troughs.

```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

fig, ax1 = plt.subplots(figsize=(60,6))

color = "tab:blue"
ax1.plot(pe["price"], label="Index", color=color)
ax1.set_xlabel("Year")
ax1.set_ylabel("Index", color="tab:blue")
ax1.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[2, 5, 8, 11]))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m')) 

color = "tab:red"
ax2 = ax1.twinx()
ax2.plot(pe["pe"], label="PE", color=color)
ax2.set_ylabel("PE", color=color)

for i in range(1, 4):
    quantile = pe["pe"].quantile(i/4)
    ax2.axhline(quantile, color='gray', linestyle='--', label=f"{i/4:02.0%}")

plt.title("Index vs PE")

fig.tight_layout()
for date in pe.index[::3]:
    ax1.axvline(date, color='gray', linestyle=':', linewidth=0.5)
plt.gcf().autofmt_xdate()

plt.legend(loc="upper left")
plt.show()
```

This generates the following plot:

![1999-2024](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/09/index-vs-pe-1999-2024.png)

From 1999 to 2024, there is a general trend of rising Shanghai Composite prices alongside falling PE ratios. The rise in index prices likely reflects the long-term trend of GDP growth, while the decline in PE is primarily due to the expansion of asset supply, which continuously squeezes out asset bubbles.

To examine details, we split the above chart into five subplots:

![Jan 1999 - May 2004](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/09/index-vs-pe-199901-200405.jpg)

![Jun 2004 - May 2009](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/09/index-vs-pe-200402-2009-05.png)

![Jun 2009 - Jul 2014](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/09/index-vs-pe-2009-06-2014-08.png)

![Jun 2014 - Oct 2019](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/09/index-vs-pe-2014-05-2019-11.png)

![Aug 2019 - Aug 2024](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/09/index-vs-pe-2019-08-2024-08.png)

## Reflections and Conclusions

*   **Question:** In which periods do PE trends and Shanghai Composite prices move in perfect lockstep? In such movements, which is the dependent variable and which is the independent variable? What phenomenon does this reflect?
*   **Answer:** Between 1999–2001, August 2005–May 2008, and May 2014–May 2015, PE trends mirrored the Shanghai Composite exactly. During these periods, intense market speculation meant that changes in corporate earnings were negligible compared to price changes. Consequently, PE trends were entirely driven by stock prices, resulting in highly similar curves for PE and price. The emergence of such phenomena indicates excessive market speculation.

*   **Question:** Since approximately August 2023, it appears the Shanghai Composite has declined faster than PE. For instance, in February 2024, both the index and PE hit阶段性 lows. However, in September 2024, while the index hit a new low, PE did not. What phenomenon does this divergence reflect? Can it be described using a common term?
*   **Answer:** In September 2024, the Shanghai Composite hit a new low, but PE did not, creating a divergence. This can also be observed through peak analysis. For example, in June 2024 (see Table 1), PE reached a new high since August 2023, while the index remained below any high point since August 2023. This divergence can be described as a **low-PE trap**. This indicator reminds us that while the index is falling, the profitability of listed companies may also be declining, leading to scenarios where the index rises slightly while PE surges, or the index falls significantly while PE declines only slightly.

Therefore, based solely on percentile statistics, current China A-shares appear undervalued. However, considering the overall downward trend of PE and the recent divergence between PE and index movements over the past year, determining whether A-shares are truly undervalued remains questionable. More dimensions should be incorporated into the judgment.

*This article is derived from the exercises in Lesson 2 of "Factor Analysis and Machine Learning Strategies."*

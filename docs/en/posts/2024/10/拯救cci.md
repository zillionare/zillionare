---
title: "Purifying CCI: Validating a High-Alpha Technical Indicator"
date: 2024-10-25
slug: en/posts/factor-strategy/拯救cci
tags: []
excerpt: "Raw CCI fails factor testing due to bimodal distribution. Purifying by discarding negative values reveals a strong, monotonic alpha. This study validates CCI as a potent technical indicator for quantitative trading. ===TAGs=== Factor Testing, CCI, Factor Purification, Quantitative Trading ===BODY=== The Commodity Channel Index (CCI), developed by Donald Lambert and first published in the *Commodities* magazine in 1980, has long been highly regarded by traders. However, using this indicator directly as a factor for **factor testing** nearly obscured its true potential. Ultimately, factor density distribution plots revealed the truth: through **factor purification**, the final testing results align with traditional experience.  The CCI calculation formula is:  $$ CCI=\\frac{Typical Price - MA}{.015 * Mean Deviation} $$  Where,  $$ \\text{Typical Price}_t=(H_t+L_t+C_t)\\div 3 \\\\ MA = Moving Average \\\\ Moving Average = (\\sum_{i=1}^PTypical Price)\\div P \\\\ Mean Deviation = (\\sum_{i=1}^P|Typical Price - MA|)\\div P $$  In simple terms, CCI represents the deviation of price from its moving average.  !!! tip     MACD, PPO, CCI, and BIAS are a group of very similar indicators. Their main differences lie in the price series selected and whether normalization is applied. We will not cover the BIAS indicator in this chapter, but here is a brief mention. Its formula is:      $$     \\text{Bias} = \\frac{\\text{Current Price} - \\text{N-day Moving Average}}{\\text{N-day Moving Average}} \\times 100     $$      This comparison offers a clue for innovating factors.  The idea behind CCI—using the average of the **highest price, lowest price, and closing price** as the price series—is common in many contexts. Essentially, **it is an approximation of VWAP**. Therefore, if VWAP data is available, using it directly might be better, as its博弈 (game-theoretic/strategic) meaning is clearer.  There is a \"magic number\" in the CCI formula: 0.15. Its purpose is to standardize the CCI value to a reasonable range, giving signal significance at the boundaries of -100 and 100. Initially, the formula’s designer, Lambert, believed that when CCI is within the [-100, 100] range, it means prices are fluctuating randomly and are not worth trading. Only when the absolute value of CCI exceeds 100 is a trend considered to have appeared—i.e., buy when CCI crosses above 100, and sell when it crosses below -100.  Let’s first observe this indicator using a simple dual-axis plot.  ```python df = PAYH.copy() df['cci'] = ta.CCI(df.high, df.low, df.close, 14)  axes = df[['close', 'cci']].plot(figsize=(14, 7),                              subplots=True,                              title=['PAYH', 'cci']) axes[1].set_xlabel('') sns.despine() plt.tight_layout() ```  Here is the output:  ![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/10/cci-payh.jpg)   In the output, I marked trading signals at two points where CCI crosses $\\pm 100$ to illustrate CCI’s signaling role. This is merely an observation of a single asset over a short period, which is insufficient to prove anything.  Now, let’s run **factor testing** to evaluate it:  ``` _ = alphatest(2000, start, end,                calc_factor = lambda x: ta.CCI(x.high,                                               x.low,                                               x.close,                                               14)) ```  The **factor testing** results appear unsatisfactory.  However, a slight analysis of CCI’s principles makes it clear that it is not suitable for direct use as a factor. This is because CCI’s trading signal is triggered when CCI crosses $\\pm 100$. It is an event signal, not a factor in the traditional sense.  Below, we explain why from the perspective of factor distribution.  ```python cci = barss.groupby(level=\"asset\")             .apply(lambda x: ta.CCI(x.high,                                      x.low,                                      x.close,                                      timeperiod=14                                     )                 )  with sns.axes_style('white'):     sns.distplot(cci)     sns.despine() ```  From the density distribution plot, we see that the factor distribution is bimodal.  ![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/10/cci-pdf.jpg)  As we discussed in our course, if a factor’s distribution is bimodal, it often contains multiple influences and is not pure. We are currently facing this exact situation. In such cases, performing **factor analysis** requires us to first \"purify\" the factor.  ```python cci = barss.groupby(level=\"asset\")             .apply(lambda x: ta.CCI(x.high,                                      x.low,                                      x.close,                                      timeperiod=14)) with sns.axes_style('white'):     sns.distplot(cci[cci> 0])     sns.despine() ```  The output is as follows:  ![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/10/cci-pdf-pured.jpg)  Now, the distribution of CCI we see is unimodal. Let’s run **factor testing** on it to see the results:  ```python def calc_cci(df, n):     cci = ta.CCI(df.high, df.low, df.close, n)     cci[cci < 0] = np.nan     return cci * -1      alphatest(2000,           start,           end,           calc_factor= calc_cci, args=(14,),           max_loss=0.55, long_short=False) ```  Note that in the third line of this code, we modified the returned CCI by setting negative values to NaN, so they will be discarded during **factor testing**. This is content previously covered when discussing the Alphalens framework.  Because we discarded half of the factor, we need to set the `max_loss` parameter to greater than 0.5 when calling Alphalens (refer to the maxlosserror report for specifics). <!-- rb：How to optimize CCI -->  The returns based on the purified factor are astonishing. It is not as strong as the RSI we tuned previously, but since we obtained these results under a pure **long position** condition, it is particularly attractive.  ![Annual Alpha Chart](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/10/cci-pured-annual-alpha.jpg)  The Alpha reaches an annualized 19%. Moreover, this factor exhibits a good positive monotonicity, as seen in the **layered backtest** returns chart:  ![Factor Layered Returns Mean Chart](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/10/cci-pured-mean-period-wise-return.jpg)  However, its cumulative return performance is not very stable under a pure **long position**. This can also be seen from the beta value in the previous annual returns chart, indicating significant sensitivity to market volatility.  ![Cumulative Returns Chart](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/10/cci-cumulative-return.jpg)  But we don’t necessarily have to stick to a pure **long position**; CCI was originally a futures indicator. Let’s look at the results for a **long-short** portfolio:  ![Alpha for Long-Short Portfolio](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/10/cci-annual-alpha-with-long-short.jpg)  Not only is the Alpha return strong, but the beta is hedged to near zero! With beta at zero, cumulative returns should be steadily upward with low volatility. Let’s see if this holds:  ![Cumulative Returns for Long-Short Portfolio](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/10/cci-long-short-cumulative.jpg)  This may be one reason why CCI is so highly regarded.  However, **factor testing** here is not equivalent to **live trading**, because the operational methods differ. In **factor testing**, we operate with weighted **long-short** positions based on factor values. In **live trading**, we would fix the entry conditions based on whether CCI crosses $\\pm 100$. In **factor testing**, our entry conditions are looser, possessing some adaptive characteristics.  This article includes code and data for reproducibility. Join the community to access the Jupyter Notebook research environment and run the code directly.  ![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/logo/zsxq.png)   In this environment, besides the code for this article, the code from previous paid articles is also available. Furthermore, any future articles that declare they include reproducible code and data can be found in this environment.  ![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/10/quantide-research-env.gif)"
lang: en
translation_of: posts/factor-strategy/拯救cci
auto_translated: true
source_sha: 84c75ce8e9534a26da1dd77e59980eea78eb9385
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/10/quantide-research-env.gif"
---

The Commodity Channel Index (CCI), developed by Donald Lambert and first published in the *Commodities* magazine in 1980, has long been highly regarded by traders. However, using this indicator directly as a factor for **factor testing** nearly obscured its true potential. Ultimately, factor density distribution plots revealed the truth: through **factor purification**, the final testing results align with traditional experience.

The CCI calculation formula is:

$$
CCI=\frac{Typical Price - MA}{.015 * Mean Deviation}
$$

Where,

$$
\text{Typical Price}_t=(H_t+L_t+C_t)\div 3 \\
MA = Moving Average \\
Moving Average = (\sum_{i=1}^PTypical Price)\div P \\
Mean Deviation = (\sum_{i=1}^P|Typical Price - MA|)\div P
$$

In simple terms, CCI represents the deviation of price from its moving average.

!!! tip
    MACD, PPO, CCI, and BIAS are a group of very similar indicators. Their main differences lie in the price series selected and whether normalization is applied. We will not cover the BIAS indicator in this chapter, but here is a brief mention. Its formula is:

    $$
    \text{Bias} = \frac{\text{Current Price} - \text{N-day Moving Average}}{\text{N-day Moving Average}} \times 100
    $$

    This comparison offers a clue for innovating factors.

The idea behind CCI—using the average of the **highest price, lowest price, and closing price** as the price series—is common in many contexts. Essentially, **it is an approximation of VWAP**. Therefore, if VWAP data is available, using it directly might be better, as its博弈 (game-theoretic/strategic) meaning is clearer.

There is a "magic number" in the CCI formula: 0.15. Its purpose is to standardize the CCI value to a reasonable range, giving signal significance at the boundaries of -100 and 100. Initially, the formula’s designer, Lambert, believed that when CCI is within the [-100, 100] range, it means prices are fluctuating randomly and are not worth trading. Only when the absolute value of CCI exceeds 100 is a trend considered to have appeared—i.e., buy when CCI crosses above 100, and sell when it crosses below -100.

Let’s first observe this indicator using a simple dual-axis plot.

```python
df = PAYH.copy()
df['cci'] = ta.CCI(df.high, df.low, df.close, 14)

axes = df[['close', 'cci']].plot(figsize=(14, 7), 
                            subplots=True, 
                            title=['PAYH', 'cci'])
axes[1].set_xlabel('')
sns.despine()
plt.tight_layout()
```

Here is the output:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/10/cci-payh.jpg)


In the output, I marked trading signals at two points where CCI crosses $\pm 100$ to illustrate CCI’s signaling role. This is merely an observation of a single asset over a short period, which is insufficient to prove anything.

Now, let’s run **factor testing** to evaluate it:

```
_ = alphatest(2000, start, end, 
              calc_factor = lambda x: ta.CCI(x.high, 
                                             x.low, 
                                             x.close, 
                                             14))
```

The **factor testing** results appear unsatisfactory.

However, a slight analysis of CCI’s principles makes it clear that it is not suitable for direct use as a factor. This is because CCI’s trading signal is triggered when CCI crosses $\pm 100$. It is an event signal, not a factor in the traditional sense.

Below, we explain why from the perspective of factor distribution.

```python
cci = barss.groupby(level="asset")
            .apply(lambda x: ta.CCI(x.high, 
                                    x.low, 
                                    x.close, 
                                    timeperiod=14
                                    )
                )

with sns.axes_style('white'):
    sns.distplot(cci)
    sns.despine()
```

From the density distribution plot, we see that the factor distribution is bimodal.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/10/cci-pdf.jpg)

As we discussed in our course, if a factor’s distribution is bimodal, it often contains multiple influences and is not pure. We are currently facing this exact situation. In such cases, performing **factor analysis** requires us to first "purify" the factor.

```python
cci = barss.groupby(level="asset")
            .apply(lambda x: ta.CCI(x.high, 
                                    x.low, 
                                    x.close, 
                                    timeperiod=14))
with sns.axes_style('white'):
    sns.distplot(cci[cci> 0])
    sns.despine()
```

The output is as follows:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/10/cci-pdf-pured.jpg)

Now, the distribution of CCI we see is unimodal. Let’s run **factor testing** on it to see the results:

```python
def calc_cci(df, n):
    cci = ta.CCI(df.high, df.low, df.close, n)
    cci[cci < 0] = np.nan
    return cci * -1
    
alphatest(2000, 
         start, 
         end, 
         calc_factor= calc_cci, args=(14,), 
         max_loss=0.55, long_short=False)
```

Note that in the third line of this code, we modified the returned CCI by setting negative values to NaN, so they will be discarded during **factor testing**. This is content previously covered when discussing the Alphalens framework.

Because we discarded half of the factor, we need to set the `max_loss` parameter to greater than 0.5 when calling Alphalens (refer to the maxlosserror report for specifics).
<!-- rb：How to optimize CCI -->

The returns based on the purified factor are astonishing. It is not as strong as the RSI we tuned previously, but since we obtained these results under a pure **long position** condition, it is particularly attractive.

![Annual Alpha Chart](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/10/cci-pured-annual-alpha.jpg)

The Alpha reaches an annualized 19%. Moreover, this factor exhibits a good positive monotonicity, as seen in the **layered backtest** returns chart:

![Factor Layered Returns Mean Chart](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/10/cci-pured-mean-period-wise-return.jpg)

However, its cumulative return performance is not very stable under a pure **long position**. This can also be seen from the beta value in the previous annual returns chart, indicating significant sensitivity to market volatility.

![Cumulative Returns Chart](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/10/cci-cumulative-return.jpg)

But we don’t necessarily have to stick to a pure **long position**; CCI was originally a futures indicator. Let’s look at the results for a **long-short** portfolio:

![Alpha for Long-Short Portfolio](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/10/cci-annual-alpha-with-long-short.jpg)

Not only is the Alpha return strong, but the beta is hedged to near zero! With beta at zero, cumulative returns should be steadily upward with low volatility. Let’s see if this holds:

![Cumulative Returns for Long-Short Portfolio](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/10/cci-long-short-cumulative.jpg)

This may be one reason why CCI is so highly regarded.

However, **factor testing** here is not equivalent to **live trading**, because the operational methods differ. In **factor testing**, we operate with weighted **long-short** positions based on factor values. In **live trading**, we would fix the entry conditions based on whether CCI crosses $\pm 100$. In **factor testing**, our entry conditions are looser, possessing some adaptive characteristics.

This article includes code and data for reproducibility. Join the community to access the Jupyter Notebook research environment and run the code directly.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/logo/zsxq.png)


In this environment, besides the code for this article, the code from previous paid articles is also available. Furthermore, any future articles that declare they include reproducible code and data can be found in this environment.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/10/quantide-research-env.gif)

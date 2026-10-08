---
title: "Beyond Out-of-Sample Testing: Detecting Overfitting in Quant Strategies ===EXCUT=== This article explores advanced overfitting detection methods beyond standard out-of-sample testing, including noise testing and parameter plane analysis, to validate strategy robustness. ===TAGS=== Overfitting, Noise Testing, Parameter Stability, Backtest Validation ===BODY=== I came across a humorous post on Zhihu describing a tactic where strategy sellers implant numerous `if` statements into their code to manipulate backtest results. These statements check if the current date matches specific dates and prevent trading on those days. The trick lies in the fact that trading on those specific dates would result in losses.  While the authenticity of this anecdote is questionable, it serves as a classic example of **overfitting**.  ## Overfitting and Detection Methods  **Overfitting** occurs when a model fits the data so closely that it fails to generalize, rendering it ineffective on new datasets. In trading terms, an overfitted strategy is \"designed\" to perform well on historical data but will inevitably fail on new data.  Overfitting is the primary enemy in backtesting. How can we detect it?  An obvious detection method is **out-of-sample (OOS) testing**. This involves splitting the entire dataset into non-overlapping training and test sets. The model is trained on the training set and validated on the test set. If the model performs well on the test set, we consider it not overfitted.  However, OOS testing becomes difficult when the dataset is small. To address this, extended versions have been developed.  One such extension is **k-fold cross-validation**, a common concept in machine learning.  This method randomly splits the dataset into $K$ subsets of roughly equal size. For each iteration, one subset is selected as the validation set, while the remaining $K-1$ subsets form the training set. The model is trained on the training set and evaluated on the validation set. This process repeats $K$ times, and the final evaluation metric is typically the average of the $K$ validation results.  This process can be simply illustrated in the following diagram:  ![k-fold cross validation, by sklearn](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/k-fold-cross-validation.png)  However, in time series analysis (with securities analysis being a typical example), k-fold is unsuitable because time series data has a strict chronological order. Therefore, a specialized version derived from k-fold cross-validation is called **rolling forecasting**. You can view it as a sequential version of k-fold cross-validation.  It can be simply illustrated in the following diagram:  ![rolling forecasting, by tsfresh](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/walk-forward-optimization.webp)  Comparing the diagrams for k-fold cross-validation and rolling forecasting reveals the key difference: one is unordered, while the other emphasizes chronological order, requiring the training and validation sets to be contiguous.  You may also encounter the term **Walk-Forward Optimization**. It is essentially identical to rolling forecasting.  Recently, however, I discovered a novel method on the BuildAlpha website: **Noise Testing**.  ## New Attempt: Noise Testing  BuildAlpha’s noise testing involves adding a certain ratio of random noise to the backtest data, running the backtest, and comparing the results based on the noisy data with those based on the real data.  The principle is that during backtesting, historical data represents only *one possible* path. If time were to replay, the overall direction of history might remain unchanged, but randomness would alter the steps. A robust strategy should be able to withstand randomness and capture the overall direction of history. Therefore, adding clever noise to a time series may cause an overfitted strategy to fail, while a truly effective strategy will still shine.  BuildAlpha is a platform similar to TradingView. Noise testing can be configured via its graphical user interface.  ![Noise Testing Settings, by buildalpha](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/add-noise.jpg)  Through this dialog box, BuildAlpha modified approximately 20% of the data, keeping the modification amplitude for OHLC (Open, High, Low, Close) within 20% of the ATR (Average True Range). The \"100\" at the bottom indicates that 100 groups of noisy data will be randomly generated.  Let’s compare the real data with the data overlaid with noise.  <div style=\"display:flex\"> <div style=\"width:45%\"> <img src=\"https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/noise-test-real-price.jpg\"/> </div> <div style=\"width: 45%\"><img src=\"https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/noise-test-modified-price.jpg\"/></div> </div>  The left image shows the real data, and the right image shows the data with added noise. After adding noise, randomness is introduced in some details, but the stock price trend remains unchanged (the addition is independent). If the price trend were altered, this method would be invalid or even harmful.  Finally, the backtest results for the same strategy are compared as follows:  ![Noise Testing Results, by buildalpha](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/noise-test-result.jpg)  From the results, it is evident that among the multiple possible paths in history, none of the backtest results outperform the real data. In other words, the excellent performance of the real backtest is purely because the strategy designer had a \"God's-eye view,\" traveling back from the future.  ## Parameter Plains and Noise Testing  Noise testing involves slightly modifying historical data and then smoothing the results. **Parameter plains**, on the other hand, is another method for detecting overfitting. It involves slightly modifying strategy parameters to see if the backtest performance changes drastically. If the performance does not change drastically, the strategy parameters are considered robust.  BuildAlpha provides visual detection of parameter plains.  ![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/params-plaetu-original.jpg)  In this 3D plot, the parameter choices are $X=9$ and $Y=4$, as indicated by the black dot. Clearly, this area is near a sensitive region where strategy performance drops sharply. Following traditional recommendations, we should choose parameters $X=8$ and $Y=8$, where the graph is flatter.  In many cases, the parameter plain hint is correct—because the parameters we choose are essentially functions of price changes; they are not price changes themselves. The most direct approach is that if the strategy’s performance remains on a flat surface even when prices change slightly, it better demonstrates the strategy’s robustness.  However, such plots are difficult to generate. Therefore, BuildAlpha generates 3D plots with parameters as coordinates in an $n$-dimensional space and strategy performance as the values. Crucially, these plots are not based on a single historical dataset but on a set of historical data: real historical data plus data with added noise. In this context, the optimal parameters selected based on the parameter plain are more reliable.  This article references two articles from the BuildAlpha website: [Noise Test Parameter Optimization](https://www.buildalpha.com/noise-test-parameter-optimization/) and [Noise Testing](https://www.buildalpha.com/noise-test/), and thanks Nelson for his assistance."
date: 2024-08-19
slug: en/posts/algo/noise-test
tags: [Overfitting, Noise Testing, Parameter Stability, Backtest Validation]
excerpt: "回测漂亮实盘拉胯？多半是过拟合！本文详解样本外测试、滚动预测之外的新利器：噪音测试与参数平原，教你识破脆弱策略，选出真正稳健的参数。"
lang: en
translation_of: posts/algo/noise-test
auto_translated: true
source_sha: bbe536fd19ea2b8edc0aa623422ffdaeead6c39d
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/noise-test-title-image.jpg"
---

I came across a humorous post on Zhihu describing a tactic where strategy sellers implant numerous `if` statements into their code to manipulate backtest results. These statements check if the current date matches specific dates and prevent trading on those days. The trick lies in the fact that trading on those specific dates would result in losses.

While the authenticity of this anecdote is questionable, it serves as a classic example of **overfitting**.

## Overfitting and Detection Methods

**Overfitting** occurs when a model fits the data so closely that it fails to generalize, rendering it ineffective on new datasets. In trading terms, an overfitted strategy is "designed" to perform well on historical data but will inevitably fail on new data.

Overfitting is the primary enemy in backtesting. How can we detect it?

An obvious detection method is **out-of-sample (OOS) testing**. This involves splitting the entire dataset into non-overlapping training and test sets. The model is trained on the training set and validated on the test set. If the model performs well on the test set, we consider it not overfitted.

However, OOS testing becomes difficult when the dataset is small. To address this, extended versions have been developed.

One such extension is **k-fold cross-validation**, a common concept in machine learning.

This method randomly splits the dataset into $K$ subsets of roughly equal size. For each iteration, one subset is selected as the validation set, while the remaining $K-1$ subsets form the training set. The model is trained on the training set and evaluated on the validation set. This process repeats $K$ times, and the final evaluation metric is typically the average of the $K$ validation results.

This process can be simply illustrated in the following diagram:

![k-fold cross validation, by sklearn](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/k-fold-cross-validation.png)

However, in time series analysis (with securities analysis being a typical example), k-fold is unsuitable because time series data has a strict chronological order. Therefore, a specialized version derived from k-fold cross-validation is called **rolling forecasting**. You can view it as a sequential version of k-fold cross-validation.

It can be simply illustrated in the following diagram:

![rolling forecasting, by tsfresh](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/walk-forward-optimization.webp)

Comparing the diagrams for k-fold cross-validation and rolling forecasting reveals the key difference: one is unordered, while the other emphasizes chronological order, requiring the training and validation sets to be contiguous.

You may also encounter the term **Walk-Forward Optimization**. It is essentially identical to rolling forecasting.

Recently, however, I discovered a novel method on the BuildAlpha website: **Noise Testing**.

## New Attempt: Noise Testing

BuildAlpha’s noise testing involves adding a certain ratio of random noise to the backtest data, running the backtest, and comparing the results based on the noisy data with those based on the real data.

The principle is that during backtesting, historical data represents only *one possible* path. If time were to replay, the overall direction of history might remain unchanged, but randomness would alter the steps. A robust strategy should be able to withstand randomness and capture the overall direction of history. Therefore, adding clever noise to a time series may cause an overfitted strategy to fail, while a truly effective strategy will still shine.

BuildAlpha is a platform similar to TradingView. Noise testing can be configured via its graphical user interface.

![Noise Testing Settings, by buildalpha](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/add-noise.jpg)

Through this dialog box, BuildAlpha modified approximately 20% of the data, keeping the modification amplitude for OHLC (Open, High, Low, Close) within 20% of the ATR (Average True Range). The "100" at the bottom indicates that 100 groups of noisy data will be randomly generated.

Let’s compare the real data with the data overlaid with noise.

<div style="display:flex">
<div style="width:45%">
<img src="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/noise-test-real-price.jpg"/>
</div>
<div style="width: 45%"><img src="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/noise-test-modified-price.jpg"/></div>
</div>

The left image shows the real data, and the right image shows the data with added noise. After adding noise, randomness is introduced in some details, but the stock price trend remains unchanged (the addition is independent). If the price trend were altered, this method would be invalid or even harmful.

Finally, the backtest results for the same strategy are compared as follows:

![Noise Testing Results, by buildalpha](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/noise-test-result.jpg)

From the results, it is evident that among the multiple possible paths in history, none of the backtest results outperform the real data. In other words, the excellent performance of the real backtest is purely because the strategy designer had a "God's-eye view," traveling back from the future.

## Parameter Plains and Noise Testing

Noise testing involves slightly modifying historical data and then smoothing the results. **Parameter plains**, on the other hand, is another method for detecting overfitting. It involves slightly modifying strategy parameters to see if the backtest performance changes drastically. If the performance does not change drastically, the strategy parameters are considered robust.

BuildAlpha provides visual detection of parameter plains.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/params-plaetu-original.jpg)

In this 3D plot, the parameter choices are $X=9$ and $Y=4$, as indicated by the black dot. Clearly, this area is near a sensitive region where strategy performance drops sharply. Following traditional recommendations, we should choose parameters $X=8$ and $Y=8$, where the graph is flatter.

In many cases, the parameter plain hint is correct—because the parameters we choose are essentially functions of price changes; they are not price changes themselves. The most direct approach is that if the strategy’s performance remains on a flat surface even when prices change slightly, it better demonstrates the strategy’s robustness.

However, such plots are difficult to generate. Therefore, BuildAlpha generates 3D plots with parameters as coordinates in an $n$-dimensional space and strategy performance as the values. Crucially, these plots are not based on a single historical dataset but on a set of historical data: real historical data plus data with added noise. In this context, the optimal parameters selected based on the parameter plain are more reliable.

This article references two articles from the BuildAlpha website: [Noise Test Parameter Optimization](https://www.buildalpha.com/noise-test-parameter-optimization/) and [Noise Testing](https://www.buildalpha.com/noise-test/), and thanks Nelson for his assistance.

---
title: "QuanTide Weekly: CSI 300 Total Return Index & Quant Regulation"
date: 2024-07-21
slug: en/posts/uncategory/weekly-0721
tags: [Quantitative Investing, XGBoost, Portfolio Optimization, Market Regulation]
excerpt: "Shanghai Stock Exchange launches total return index; regulators tighten short-selling rules. This week’s deep dive critiques XGBoost regression for portfolio construction, advocating classification and SMAPE loss functions."
lang: en
translation_of: posts/uncategory/weekly-0721
auto_translated: true
source_sha: 99153a97e98faa9a55a271b1d981d57a5882e913
---

## This Week’s Highlights

*   **SSE Launches Total Return Index:** To help investors better track overall market returns, the Shanghai Stock Exchange (SSE) and China Securities Index Co., Ltd. will officially release real-time data for the **Shanghai Composite Total Return Index** starting July 29. The index code and abbreviation have been adjusted to "000888" and "Shanghai Return," respectively.
*   **Quant Giants Speak Out:** DMA (Direct Market Access) holding values dropped by 200 billion RMB this week. Major quantitative funds like High-Flyer and Yanfu issued statements arguing that quantitative investing has long-term advantages and should not be blamed for market downturns. Since 2023, DMA strategies have been highly profitable, becoming a primary revenue source for private funds, which has also drawn market criticism.
*   **Exchanges Tighten Oversight on Abnormal Trading:** The Shenzhen Stock Exchange (SZSE) took self-regulatory measures against 54 instances of abnormal trading this week. The SSE focused monitoring on convertible bonds with high volatility and issued written warnings for 49 cases of abnormal trading, such as price manipulation and false declarations. Meanwhile, the Shanghai Futures Exchange (SHFE) released the revised *Measures for the Administration of Abnormal Trading Behaviors*, effective October 25, 2024.
*   **Bitcoin Breaks $67,000:** Bitcoin surged past $67,000 intraday.
*   **Short-Term Bond Funds Surge:** The total scale of short- and medium-term bond funds has exceeded 800 billion RMB, a 50% increase in six months. Huijin continued to increase its ETF holdings in Q2, with subscription amounts nearing 300 billion RMB. Equity ETF scales grew by over 420 billion RMB year-to-date, with broad-based ETFs driving the growth.
*   **Tesla Hits Blue Screen:** Tesla’s stock dropped nearly 5% intraday on Friday, closing down 4.02%, hit by both Trump-related news and the global Microsoft Windows blue screen incident.

---

## Next Week’s Calendar

*   **Monday:** The People’s Bank of China will announce July LPR quotes. Market expectations suggest a potential window for RRR cuts or rate cuts in Q3 or Q4 to further support steady economic growth.
*   **Monday:** The margin requirement for securities lending will rise to 100%, and for private securities investment funds participating in securities lending, it will rise from 100% to 120%. Notably, after the CSRC’s announcement, A-share securities lending balances have begun to decline continuously. Wind data shows that as of July 18, the securities lending balance dropped to approximately 29.5 billion RMB, hitting a four-year low.
*   **Starting July 24:** Issuance of ultra-long special treasury bonds begins. This tranche consists of 30-year fixed-rate interest-bearing bonds, with a competitive bidding face value total of 55 billion RMB.
*   **This Week:** Three new stocks will be issued: Liju Thermal Energy, Boshi Jie, and Longtu Guangzhao.
*   **This Friday:** The window for refining oil price adjustments opens. Calculations indicate that domestic gasoline and diesel retail prices should be reduced by 50 RMB/ton.

<div style="font-size: 1.8vw;color: #808080;text-align:right;margin: 2em 0 2em 0;">Data sources: Securities Daily, etc., compiled via Tushare.pro API.</div>

## This Week’s Articles

We published five articles this week. Two detailed articles, including *[Portfolio Strategy Based on XGBoost...](https://mp.weixin.qq.com/s?__biz=MzI2MzE3MzY4Ng==&mid=2662262844&idx=1&sn=7c5ffabd30de64b73b1156cf45f2804c&chksm=f1e5ab65c692227306f4d1ce179e619f8de33ba25ad30412821b02ba62a922b5c8f84fb159dd&token=837192034&lang=zh_CN#rd)*, explain the framework and common pitfalls of using machine learning to build portfolio strategies.

---

**Key Takeaways and Conclusions:**

1.  **Two-Stage Framework:** We implement a two-stage approach for multi-factor, multi-asset portfolio construction. Stage one uses XGBoost to build single-asset multi-factor models; stage two uses classic mean-variance optimization for portfolio allocation.
2.  **Classification over Regression:** Machine learning models should be built based on classification rather than regression. Time-series price prediction is largely meaningless because price sequences are non-stationary.
3.  **Labeling Strategy:** Classification models are trained using multi-factors as features and the digitized future one-period return magnitude as labels.
4.  **Factor Standardization:** For XGBoost models, factor standardization is generally unnecessary and may even introduce side effects. However, standardization can also help with regularization penalties.
5.  **Loss vs. Metric:** The key difference is that a loss function must be differentiable to compute gradients. The non-differentiability of MAPE makes it unsuitable as a loss function.
6.  **Relative Error:** In finance, relative error is more meaningful than RMSE. Therefore, we introduce **SMAPE**—a function that can serve as a loss function.

We have compiled these two articles and will publish them at the end of this piece.

In this week’s Quant Tools column, we published *[The Man Who Won the NASA Medal Brings These IPython Tips](https://mp.weixin.qq.com/s?__biz=MzI2MzE3MzY4Ng==&mid=2662262876&idx=1&sn=051401d8d9939884b6ceafc90326b474&chksm=f1e5ab05c6922213ed57c5f0c3effeffac9ef1409ab7d3234963897757890f79ac4024384fef&token=837192034&lang=zh_CN#rd)*. IPython is a very lightweight interactive programming tool. Although all its features can be found in Notebooks, it is lighter and still highly capable, showing great agility.

In *[Don’t Write Books Unless You’re Talking to Your Soul](https://mp.weixin.qq.com/s?__biz=MzI2MzE3MzY4Ng==&mid=2662262895&idx=1&sn=4bac9ced34d4430b7d1ac065c0857d69&chksm=f1e5ab36c69222207a0d9b62cd264f7787b6eae6fc79bbf5c61a3be658d07b8d6102ad4cac8d&token=837192034&lang=zh_CN#rd)*, we revealed some embarrassing moments during the publication of *Python Efficient Programming Practice Guide*. This book will be very helpful for quants building robust trading systems.

---

Right after these words were spoken, the Windows blue screen event occurred on Friday. This happened precisely because CrowdStrike lacked a robust CI/CD pipeline, which is one of the key topics detailed in our book.

In *[Ask with Confidence: The Most Comprehensive Self-Study Roadmap for Quant](https://mp.weixin.qq.com/s?__biz=MzI2MzE3MzY4Ng==&mid=2662262915&idx=1&sn=86cf93d26f811f3c507bd2ce9c7f57a0&chksm=f1e5abdac69222cc9382f524f2c040828e9ed0177ee1d72a9fcd26de47633624639ecabb25d9&token=837192034&lang=zh_CN#rd)*, we introduced the quant self-study outline written by Algos.org.

We will also launch our own quant self-study roadmap by the end of August. In addition to better localization (as some tools, websites, and data sources in the English version do not support the domestic market), we will clearly map out learning paths from beginner to expert, and from novice to different roles.

Until our roadmap is released, you can temporarily refer to this guide:

![75%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/cheese-course-roadmap.png)

---

# Building Multi-Factor Strategies with XGBoost

How can we apply machine learning methods to portfolio strategies? Recently, we reviewed some stored papers and decided to interpret the paper *"A Portfolio Strategy Based on XGBoost Regression and Monte Carlo Method."*

This is a basic framework diagram abstracted from the paper.

![50%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/xgboost-model-framework.jpg)

What problem does this framework solve? In a portfolio strategy, the first key issue is how to select a subset of stocks from a given universe to include in the strategy pool. The second issue is how to allocate positions among these stocks to maximize the risk-return ratio of the portfolio.

---

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/10/portfolio-optimisation.png)

The latter part is most classically addressed using Modern Portfolio Theory (MPT) to find the efficient frontier. This can be solved using convex optimization or Monte Carlo schemes. We have a series of articles on this topic: *[Portfolio Theory and Practice](https://blog.quantide.cn/articles/investment/%E7%AD%96%E7%95%A5%E7%A0%94%E7%A9%B6/mpt-1/)*, which clearly covers basic concepts to practical details, so we won’t elaborate here.

**How to select stocks from the universe into the strategy pool?** This is relatively easy in single-factor models: simply select stocks from the best-performing tier (layer) in factor ranking. Weights for individual assets can be allocated based on factor loadings or using MPT methods.

But how to select stocks for the strategy pool in a **multi-factor model**? This has always been a difficult problem. Even the commonly mentioned Barra model is primarily a risk control model and does not select the optimal stock pool.

---

The paper’s approach is to view stock selection as a **regression problem**: **train with multi-factors to identify stocks that the model can best predict, and include those in the strategy pool.**

The author’s results show that for the top-performing stock portfolios in 2021, 2020, and 2019, the returns were **27.86%, 6.20%, and 23.26%**, respectively. However, the author did not provide benchmark comparisons, nor did they deeply analyze whether any excess returns came from MPT or from XGBoost.

This is where we need to interpret this paper. We hope our interpretation helps you learn how to analyze others’ papers and extract the correct parts.

## The Error of Regression

The paper uses an XGBoost regression model. This is questionable. In asset pricing models, we want to predict **stock strength or weakness in the cross-section, not their time-series trends.**

The author’s method here is to train a regression model to predict next-day (or subsequent period) trends well.

![R50](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/xgboost-prediction-result.jpg)

The right figure shows one of the author’s results. It appears the model predicts next-day trends perfectly.

---

Clearly, since the XGBoost regression model itself lacks the ability to predict stock strength or weakness, finding perfectly fitted stocks through regression is meaningless. A declining stock can also be perfectly fitted. Therefore, the returns mentioned in the paper, even if they show excess returns, likely come from MPT theory.

However, the author still provides a clue on how to use XGBoost to find the best-performing individual stocks in a multi-factor model. We just need to **convert it into a classification model and use the classifier to screen for the best-performing stocks.**

![L50](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/classification_xgboost.png)

The X part of the training set does not need to change, but we need to redefine the labels, i.e., the y part. For given factors $X_i$, the corresponding $y_i$ needs to reflect whether the stock rises or falls. If possible, we can set labels into 5 categories: -2 for significant drops, 2 for significant rises, and so on for the middle parts.

Then, construct a classifier for training. After training, stocks predicted to belong to the "significant rise" label are included in the strategy pool. Weights can be allocated equally or optimized using MPT theory.

## End-to-End Training and New Network Architecture

The framework used by the paper authors is two-stage: first, select stocks into the strategy pool, then optimize weights via MPT.

---

Even in the first stage, **it is still two-stage**. Each time it trains, it only uses multi-factor data for a single asset. Therefore, if the universe contains 1,000 assets, 1,000 models must be trained (this is the method implied in the paper; alternatively, one model trained 1,000 times).

The reason for this is technical limitations. XGBoost only supports **two-dimensional input**. If we want to train multiple assets’ multi-factors simultaneously, we must use **panel format** data or **flatten multiple assets’ multi-factors into one dimension**. However, if the number of assets is too large, training after flattening becomes difficult.

Thus, due to technical constraints, we can either train multiple assets with single factors simultaneously or train single assets with multiple factors.

However, the paper authors provide a method here: you can train models for each asset separately, predict separately, and then evaluate using MAPE. When we convert this to a classification model, we can simply look at classification results or combine classification metrics (in the time-series dimension) to select assets with **both high accuracy and good classification results** to include in the strategy stock pool.

## Loss Functions vs. Metrics

Next, we analyze the use of the MAPE function in the paper. Using this as an opportunity, we will delve slightly deeper into machine learning principles to discuss two key points:

<div style="font-size: 1.5em; padding-left:2.5em">
1. Loss Functions vs. Metrics<br>
2. Whether Factor Data Needs Standardization for XGBoost Models
</div>

---

## Loss Functions vs. Metrics

In machine learning, there are two important types of functions: **objective functions (also called loss functions)** and **metrics**.

![75%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/gradient-descent.jpg)

Loss functions are used for model training. During training, methods like gradient descent are used to continuously reduce the value of the loss function until it can no longer decrease, at which point the model is trained.

---

The trained model is then tested on the test dataset, and the predicted results are compared with the true values. To quantify this comparison process, we introduce **metrics**.

Sklearn provides numerous loss functions and metrics. The figure below lists some loss functions and metrics provided by Sklearn:

---

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/sklearn-loss-metrics.jpg)

As you can see, the number of metrics is far greater than the number of loss functions. Why is this?

---

In the paper, the author did not disclose the specific training process through XGBoost, only stating that the XGBoost database was used directly. This expression is a bit strange; we can understand it as using XGBoost’s default values for parameters.

---

However, the author emphasized the use of MAPE. From the process, it appears MAPE was used as a metric for post-hoc evaluation.

In XGBoost, if no specific objective function is specified, the default is the RMSE (rooted mean square error) function with regularization penalties. RMSE can also serve as a metric. In the paper, the author did not use RMSE as a metric but chose MAPE (mean absolute percentage error). Why? If MAPE is better in this scenario, why not use MAPE as the loss function during training?

It seems that both objective functions and metrics aim to make predicted values closer to true values. Since they share this characteristic, why distinguish between these two types of functions?

To answer these questions, we must understand XGBoost’s training principle: **how it computes gradients.**

### XGBoost: Second-Order Taylor Expansion

XGBoost is a Boosting algorithm that constructs a strong learner by stacking multiple weak learners. In each iteration, a new tree corrects the residuals of the existing model, i.e., the difference between predicted and true values. The magnitude of this difference is calculated by the objective function.

---

In XGBoost, the stacking of multiple weak learners adopts an additive model,

---

meaning the final prediction is the weighted sum of outputs from all weak learners. This model allows us to use Taylor expansion to approximate the loss function, enabling efficient optimization.

XGBoost optimizes the objective function through second-order Taylor expansion and computing the second

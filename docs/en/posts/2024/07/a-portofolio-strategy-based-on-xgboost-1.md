---
title: "XGBoost Portfolio Strategy: Basic Framework Explained"
date: 2024-07-15
slug: en/posts/factor-strategy/a-portofolio-strategy-based-on-xgboost-1
tags: [XGBoost, Portfolio Strategy, Multi-Factor Model]
excerpt: "We review an XGBoost-based portfolio framework from a PhD thesis, explain its two-stage selection and weighting process, and argue why classification outperforms regression for cross-sectional stock picking."
lang: en
translation_of: posts/factor-strategy/a-portofolio-strategy-based-on-xgboost-1
auto_translated: true
source_sha: b5d20395e556d5a25f52dfceac7dab7bf0ea0dbd
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/university/university-college-london-library.jpg"
---

!!! quote
    Indulgence is instinct; discipline is cultivation. What gives you joy in the short term will surely bring you pain. Conversely, what brings you pain will ultimately lead to success. Remember, cheap pleasure needs only indulgence, while higher joy requires restraint. -- Russell

Before we get into the main content, a quick fact-check: this quote is not from Bertrand Russell, but from Mr. Verbose. Some aphorisms only spread by borrowing a famous name — proof that we are swayed not by truth itself, but by the power and prestige attached to authority.

This time we will unpack a PhD thesis with a “novel” idea — but don’t worship a paper just because it’s a paper.

---

How can machine learning be applied in a portfolio strategy? We dug through our saved papers and decided to review *A Portfolio Strategy Based on XGBoost Regression and Monte Carlo Method* [^mingxuan] in three parts:

!!! readmore
    - Basic Framework for an XGBoost-Based Portfolio Strategy
    - Discussion on the Objective Function
    - On Factor Selection

This is part one: the basic XGBoost-based framework built in the thesis.

## Basic Framework

![50%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/xgboost-model-framework.jpg)

[^mingxuan]: [PDF](https://blog.quantide.cn/assets/ebooks/A-Portfolio-Strategy-Based-on-XGBoost-Regression-and-Monte-Carlo-Method.pdf) 


---

This is the basic framework diagram abstracted from the thesis.

What problem does this framework solve? In a portfolio strategy, the first key question is how to select a subset of stocks from a given universe for the strategy pool; the second is how to allocate weights to those stocks to maximize risk-adjusted return on the portfolio.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/10/portfolio-optimisation.png)

For the second part, the classic approach is MPT theory — finding the efficient frontier. This can be solved with convex optimization or with a Monte Carlo approach. We previously covered this in detail, from basic concepts to implementation, in our series [Portfolio Theory and Practice](https://blog.quantide.cn/articles/investment/%E7%AD%96%E7%95%A5%E7%A0%94%E7%A9%B6/mpt-1/), so we won’t repeat it here.

---


**How do you select stocks from the universe into the pool?** In a single-factor model this is easy: pick the stocks in the best-performing tier from the layered backtest. Weights can then be assigned by factor loadings, or optimized with MPT.

But how do you select stocks into the pool in a multi-factor model? That has always been a hard problem. The Barra model we often mention is only a risk model — it cannot pick the optimal stock pool.

The thesis treats inclusion as a regression problem: **train on multiple factors and select the stocks that the model can predict best for the pool**.

The author reports that in 2021, 2020 and 2019, the leader portfolio returned **27.86%, 6.20% and 23.26%** respectively. However, no benchmark comparison is provided, nor any deeper analysis of whether any excess return came from MPT or from XGBoost.

That is exactly why we are reviewing this thesis. Through our review, you can also learn how to read other people’s papers critically and take away what is actually correct.

## The Flawed Regression

The thesis uses an XGBoost regression model. That choice is debatable. In asset pricing, what we want to predict is **cross-sectional strength among stocks, not time-series direction**.

---

The author trains a regression model to predict the next day (or the move over a subsequent window). Below is one of the results reported in the thesis:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/xgboost-prediction-result.jpg)

The model appears to predict the next-day move almost perfectly.

!!! warning
    Even if the next-day prediction looks perfect, there is a big trap here that beginners must remember: this kind of prediction typically has a high win rate but a low payoff, with uncertain overall profit.


---

Clearly, since an XGBoost regression model has no ability to predict relative cross-sectional strength, finding perfectly fitted stocks through regression is meaningless. A stock in a downtrend can also be fitted perfectly. So even if the reported returns contain excess return, it most likely comes from MPT theory.

Still, the author offers a useful clue on how to find the best stocks in a multi-factor model with XGBoost. We just need to **turn it into a classification model, then use the classifier to filter for the best-performing stocks**.

![L50](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/classification_xgboost.png)

The X side of the training set can stay unchanged, but we need to redefine the labels, the y side. For a given factor $X_i$, the corresponding $y_i$ should indicate up or down. If possible, we can use 5 classes, with -2 for a large drop and 2 for a large rally, and so on for the buckets in between.



Then build a classifier and train it. After training, stocks predicted with the strong-rally label go into the stock pool, where they can be equal-weighted or optimized with MPT theory.

Of course, when we construct labels and the training dataset, we must account for the holding period in live trading.

---

## End-to-End Training and New Architectures

The author uses a two-stage framework: first select stocks into the strategy pool, then optimize weights with MPT.

But even the first stage **is itself two-stage**. Each training run uses multi-factor data for only a single ticker. So if the universe has 1,000 tickers, you have to train 1,000 models (the method implied in the thesis; you can also think of it as training one model 1,000 times).

The reason is a technical constraint. XGBoost only supports **2D input**. To train jointly on multiple factors across multiple tickers, you would have to use data in **panel format**, or **flatten the multiple factors of multiple tickers into one dimension**. But with too many tickers, training after flattening becomes very difficult.

In other words, due to the technical constraint, you either train single-factor on multiple tickers at once, or multi-factor on a single ticker.

The author nevertheless suggests a workable method: you can train separate models for multiple tickers, forecast separately, and then evaluate with MAPE. Once we switch to a classification model, we can simply look at the classification outcome, or combine it with classification metrics (along the time dimension), and select tickers with **both good accuracy and favorable predictions** for the strategy pool.


That is the method we should take away from this thesis.

---


!!! hint
    Is a jointly trained model possible here? From what I have found, XGBoost does not support joint training, or multi-task learning. This also points to a research direction for students of AI. In quant, there is still plenty of room to explore end-to-end algorithmic models.

## Conclusion

In this installment we introduced the model construction for an XGBoost-based multi-factor portfolio strategy. It is a two-stage design that achieves multi-factor stock selection by training many single-ticker, multi-factor models. However, the author mistakenly chose a regression model, so the results in the thesis will likely fall short of expectations.

In the next post, we will talk about MAPE as a metric.

![50%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/mybook/mouse-cursion.png)

---
title: "China Private Quant Strategies Roundup: Early 2024"
date: 2024-01-14
slug: en/posts/factor-strategy/review-of-private-equity-quantitative-strategies-in2023
tags: [Private Quant Funds, Factor Mining, Machine Learning]
excerpt: "After reviewing roadshows from a dozen private funds, we summarize the most effective 2023 quant strategies, led by technical trend and reversal factors combined with machine learning models."
lang: en
translation_of: posts/factor-strategy/review-of-private-equity-quantitative-strategies-in2023
auto_translated: true
source_sha: ab55330728d94c56b352d78be5ec87382d22b25a
---

After reviewing roadshow decks from over a dozen private funds, here is our take on the most effective strategies of 2023!

Factor mining is still predominantly manual. The most effective factors (strategies) remain technical trend + reversal, for both CTA and quant longs. Model construction is almost entirely machine learning. Tree models see wider adoption than neural networks, reaching 90% usage at some firms.

<!--more-->
---

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/01/private-equity-strategy-cta.png)

In CTA strategies, broken down by fundamental, technical, and alternative factors, most firms still rely primarily on technicals. **Trend-following strategies were typically the main contributor to returns, while fundamental factors dragged on performance**.

In CTA, Semi-Martingale (半鞅) fields the most layered mix, combining term structure, event-driven, technical factors, calendar effects, volume-price synergy, and reversal. Overall, the focus remains on technicals broadly defined — here classic indicators, calendar effects, volume-price synergy, and reversal all count as technical factors.

Another distinctive feature of Semi-Martingale is its use of **NLP on overseas data** to build an event-driven model.

---

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/01/private-equity-strategy-long.png)

Among quant long strategies, factors are mainly hand-crafted, with an emphasis on interpretability. Volume-price factors still dominate and remain the main contributor to strategy returns. Factor counts are typically in the hundreds, though a few firms focused on automated mining maintain much larger libraries — Shanghai Zhuosheng (上海卓胜), for example, has built a 100K+ feature library.

For factor testing, single-factor IC is still the standard, but for model combination most private funds have upgraded to machine learning (90%), with some starting to use neural networks to achieve nonlinear combination.

---

One noteworthy trend in factor mining is using high-frequency data in lower-frequency settings. Hanhon (翰荣), for example, mines **L2 data** to build factors used in medium-frequency trading. High-frequency data often contains signals that **reveal aggressive institutional intent**, so it is useful not only for high-frequency trading — Hanhon has confirmed its value in medium-frequency trading as well.

Long portfolios typically target CSI 300, CSI 500, and CSI 1000 enhanced indexing, though some, like Cloudrise (云起), run **"air" enhanced indexing** (no benchmark tracking, stock selection across the entire market).

**Neutral strategies** also had highlights. Shanghai Zhuosheng's quant hedge strategy built on CSI 500 enhanced indexing posted a Sharpe ratio of 2.22 last year, which also reflects the year's market action.

**How to iterate on machine learning**? Cloudrise, for example, undertakes a major model overhaul when it hits a larger-than-expected drawdown. They did not elaborate on how they define such a drawdown. One known approach, however, is to infer the probability distribution of max drawdown via Monte Carlo simulation based on the strategy's Sharpe ratio, and then use max drawdown to judge whether conditions are abnormal.

A more idiosyncratic player is Shanghai Shengguanda (上海盛冠达), which focuses on a small-cap quant strategy: a fundamental multi-factor model (quarterly frequency) + technical indicators (monthly frequency). Annual turnover is 10x. Judging by turnover and trading style, it is likely still manual stock picking with manual execution. But performance has been solid.

On risk control, Barra dominates across the board. Almost all quant long strategies use the Barra model.

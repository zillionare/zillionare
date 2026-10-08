---
title: "Numpy & Pandas for Quant: Essential Data Processing"
date: "2026-10-09"
slug: en/articles/course/numpy-pandas/intro
tags: [Numpy, Pandas, Quantitative Finance, Data Science]
excerpt: "Master Numpy and Pandas through real-world quantitative finance scenarios. This course covers core algorithms for factor analysis, backtesting, and data manipulation, tailored for quant developers and researchers."
lang: en
translation_of: articles/course/numpy-pandas/intro
auto_translated: true
source_sha: 007f0a55fbf182d81ccc607bd2f81b1749343b34
---

Just as death and taxes are inevitable, Numpy and Pandas hold an equally indispensable status for quantitative practitioners—every quant will inevitably interact with these two libraries.

If you examine critical quantitative libraries such as Alphalens, empyrical, backtrader, Tushare, AKShare, jqdatasdk, or excellent frameworks like QuantAxis, Zillionare, and VNPy, you will find they all rely on Numpy and Pandas. In fact, any library that depends on Pandas will inevitably have a transitive dependency on Numpy.

Specifically, Numpy and Pandas provide table-like data structures—Numpy Structured Arrays and Pandas DataFrames—which are essential for intermediate storage of various data types, including market data. They also offer numerous foundational algorithms, such as:

- **Correlation Calculation in Pair Trading:** Correlation analysis is a crucial step in pair trading. Both Numpy and Pandas provide functions for calculating correlations.
- **Ranking for Factor Calculation:** Ranking is a fundamental operation in calculating factors like Alpha 101, which serves as the basis for layered backtests. Pandas provides this functionality via the `rank` method.
- **Max Drawdown Calculation:** Max drawdown is a key metric for evaluating strategies. Numpy supports this via `numpy.maximum.accumulate`.

There are many such commonly used algorithms, which we will introduce one by one in this course.

## Course Pricing

To make this course accessible to more readers, we have adopted a tiered pricing strategy:

=== "Plan A"
    !!! tip "Free"
        You can read the course text for free at [Quantide Blog](https://blog.quantide.cn/articles/python/numpy%26pandas/01-introduction/).
=== "Plan B"
    !!! tip "Only 99 RMB!"
        We provide interactive, online-running notebooks. They contain nearly the same content as Plan A, but every code snippet is executable (if you are familiar with notebooks, you will understand). You can modify and run the code without having to copy-paste from our course text or worry about dependency libraries and data sources.

        You can purchase it on [Xiaohongshu](https://www.xiaohongshu.com/goods-detail/67f4d677ab6a3e0001e5bb84?t=1762062506298&xsec_token=ABstLThUDfUaYjgAOEyrahdZ7G6MeNK3ln85SXgObCR88%3D&xsec_source=pc_arkselfshare).

## Course Structure

A key feature of this course is its tight integration with quantitative scenarios. We analyze the source code of important, high-popularity quantitative libraries to identify where Numpy and Pandas are used, then categorize and distill these patterns. We also incorporate frequently asked questions from quantitative communities—often reflecting the difficulties quant practitioners face when using Numpy/Pandas—to structure the curriculum. This ensures a systematic explanation of these critical libraries while guaranteeing that students can immediately apply the learned methods and techniques to their work, rapidly boosting their productivity.

The course is divided into 11 chapters.

We have arranged both demonstration code and exercises within quantitative scenarios as much as possible to enhance your immersion. However, this often requires you to understand these scenarios and the underlying data.

While developing this course, the author read numerous books, blog posts, papers, and open-source project code. For materials closely related to the textbook, we provide reference links as further reading or footnotes. If you have time, you may read these to gain the same depth of perspective as the author. However, if you are short on time, you can entirely skip this content and focus solely on the main course material.

This course is specifically designed for quantitative trading practitioners, such as Quant Developers, Quant Researchers, and Quant Portfolio Managers. If you have basic financial knowledge, this course is also suitable for others needing to learn Numpy and Pandas. The course’s breadth and depth are rare in the current market.

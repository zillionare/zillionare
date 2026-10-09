---
title: "Monopoly Quant: 24-Lesson Curriculum Guide"
date: 2024-01-04
slug: en/articles/course/24lectures/how-the-course-are-composed
tags: [Quantitative Trading, Factor Investing, Backtesting, Python For Finance]
excerpt: "A comprehensive quantitative trading course covering data acquisition, preprocessing, factor analysis, backtesting, and live trading using Python libraries like AkShare, Tushare, and Backtrader."
lang: en
translation_of: articles/course/24lectures/how-the-course-are-composed
auto_translated: true
source_sha: cddd9771daef711fd33d9ba26187986630efb130
---

## 01 Course Content
This course covers the entire quantitative workflow, from data acquisition and preprocessing to factor extraction and analysis, backtesting, visualization, and live trading. It introduces essential quantitative libraries and their applications, including:

### Data Acquisition
We will cover common libraries such as AkShare, Tushare, and JQDataSDK, as well as the databases used by institutional investors.

### Python Financial Data Analysis
- numpy
- pandas
- scipy (focus on `stats` and `signal`)
- scikit-learn (focus on `preprocessing`, `metrics`, etc.)
- statsmodels (ECDF, empirical cumulative distribution function)
- statistics (Python’s built-in statistical library)
- zigzag (peak/trough analysis, machine learning labeling, and pattern detection)
- ckwraps (1D data clustering for platform detection, etc.)
- talib and technical indicators (RSI, ATR, moving averages)

### Factor Analysis Methods
- alphalens
- jqfactor

### Plotting and Visualization
- matplotlib
- plotly
- pyecharts
- seaborn

### Backtesting
- backtrader (backtesting framework)
- Zillionare (backtesting framework)
- empyrical (strategy metrics analysis)
- quantstats (backtesting metrics visualization)

### Live Trading
- easytrader (keyboard/mouse simulation-based)
- ptrade (ptrade live trading interface)
- emt (East Money file interface)
- qmt (QMT live trading interface)

### Others
- sympy (symbolic math operations, ideal for academic papers)
- pyfolio (risk and factor analysis)
- ta (time-series factor library)

The breadth and depth of this content are unparalleled in the market. Upon completion, you will master the entire quantitative trading implementation process, possessing robust data analysis skills, single-factor analysis capabilities, technical pattern analysis skills, foundational machine learning knowledge, and probability/statistics basics. You will also be able to read research reports and academic papers and reproduce their findings.

## Course Features

### Content Characteristics

First, it is highly practical. Although the course has theoretical depth (tracing the theoretical origins of various strategies and factors, involving statistical probability and financial econometrics), after explaining the theoretical background, the focus is on connecting theory to practice. It explains which Python library and method implement the mathematical formulas in papers, what the resulting plots look like, and in which quantitative scenarios they are typically used to solve specific problems.

Technical pattern analysis and market timing are also key practical focuses. The algorithms taught are based on statistical probability and machine learning theories, featuring strong adaptive capabilities, accurate pattern capture, and significant practical value, particularly for the programmatic implementation of Elliott Wave Theory.

Second, the code quality is high, emphasizing standards and documentation, with performance optimized to the extreme (the instructor developed an open-source quantitative framework entirely in Python, achieving high-speed storage and access for 3 billion data records). Most code is ready for direct use.

Third, the instructor has a broad knowledge base and integrates concepts effectively. For example, when introducing the course’s market data, explaining why we use 32-bit floats instead of 64-bit floats to store OHLC data, we connected this to the latest advancements in deep learning performance optimization:

!!! quote
    We use `np.float32` to store OHLC data, reserving `np.float64` only for turnover amount and volume. Using smaller byte sizes for data storage is a key direction in AI performance optimization. Around 2020, academia began using int16 to compress deep learning models, and recent compressions of large models have even started using int8.

For instance, many friends have read our article [How to Implement Normalization in Deep Learning-Based Quantitative Strategies](https://blog.quantide.cn/blog/2023/12/16/%E5%9F%BA%E4%BA%8E%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0%E7%9A%84%E9%87%8F%E5%8C%96%E7%AD%96%E7%95%A5%E5%A6%82%E4%BD%95%E5%AE%9E%E7%8E%B0%E5%BD%92%E4%B8%80%E5%8C%96/). Most readers consider this article quite profound. This article actually originates from Lesson 13 of our course.

### Structural Characteristics
The course generally begins with a mind map outlining the knowledge points for the entire lesson, for example:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/07/lesson13-outline.png)

### Experimental Environment

The online experimental environment for the course is provided by a cluster with 256GB of memory and 192 CPUs. Students do not need to prepare their own experimental environment or data. The online environment provides 3 billion records of market data, real-time market data, and online backtesting capabilities, as well as simulated trading testing.

A good strategy often requires testing through multiple bull and bear cycles. Our experimental environment includes 18 years of data, which is unachievable for courses that rely on CSV-based data preparation.

---
title: "Quantide’s 24-Lesson Quant Course: Architecture & Syllabus"
date: 2024-01-04
slug: en/articles/course/24lectures/how-the-course-are-composed
tags: [Quantitative Trading, Factor Investing, Backtesting, Python]
excerpt: "A comprehensive quantitative trading curriculum covering data acquisition, factor analysis, backtesting, and live trading. Details essential Python libraries, high-performance data handling, and real-world strategy implementation."
lang: en
translation_of: articles/course/24lectures/how-the-course-are-composed
auto_translated: true
source_sha: 5fdd8f807310ccd7aaa286449d34c20ecfc24f76
---

## 01 Course Overview
This course covers the entire quantitative trading workflow—from data acquisition and preprocessing to factor extraction, analysis, backtesting, visualization, and live trading. It introduces essential quantitative libraries and tools, including:

### Data Acquisition
We cover popular libraries like `akshare`, `tushare`, and `jqdatasdk`, as well as the databases used by institutional investors.

### Python Financial Data Analysis
- `numpy`
- `pandas`
- `scipy` (focus on `stats` and `signal`)
- `scikit-learn` (focus on `preprocessing`, `metrics`, etc.)
- `statsmodels` (ECDF, empirical cumulative distribution functions)
- `statistics` (Python’s built-in statistical library)
- `zigzag` (peak/trough analysis, machine learning labeling, and pattern detection)
- `ckwraps` (1D data clustering for platform detection, etc.)
- `talib` and technical indicators (RSI, ATR, moving averages)

### Factor Analysis Methods
- `alphalens`
- `jqfactor`

### Plotting and Visualization
- `matplotlib`
- `plotly`
- `pyecharts`
- `seaborn`

### Backtesting
- `backtrader` (backtesting framework)
- `Zillionare` (backtesting framework)
- `empyrical` (strategy performance metrics)
- `quantstats` (backtest performance visualization)

### Live Trading
- `easytrader` (keyboard/mouse simulation-based trading)
- `ptrade` (Ptrade live trading interface)
- `emt` (East Money file interface)
- `qmt` (QMT live trading interface)

### Other Tools
- `sympy` (symbolic math operations, ideal for academic papers)
- `pyfolio` (risk and factor analysis)
- `ta` (time-series factor library)

The breadth and depth of this content are unmatched in the market. Upon completion, you will master the full implementation process of quantitative trading, possessing robust data analysis skills, single-factor analysis capabilities, technical pattern recognition skills, and foundational knowledge in machine learning and probability/statistics. You will also be able to read research reports and academic papers and reproduce their findings.

## Course Features

### Content Characteristics

First, the course is highly practical. While it maintains theoretical depth—tracing the theoretical origins of various strategies and factors, involving statistical probability, and industry finance—it emphasizes practical application. After explaining the theoretical background, the focus shifts to connecting theory with practice: showing which Python library and method implement the mathematical formulas in papers, what the resulting plots look like, and in which quantitative scenarios they are typically used to solve specific problems.

Technical pattern analysis and market timing are also key practical components. The algorithms taught in the course, based on statistical probability and machine learning theory, offer strong adaptability, accurate pattern capture, and significant practical value, particularly for the programmatic implementation of Elliott Wave Theory.

Second, the code quality is high, emphasizing standards and documentation, with performance optimized to the extreme (the instructor’s open-source quantitative framework, written entirely in Python, achieves high-speed storage and access for 3 billion data records). Most code is ready for direct use.

Third, the instructor possesses a broad knowledge base and integrates concepts seamlessly. For example, when introducing Daifuweng’s market data and explaining why we use 32-bit floats instead of 64-bit floats to store OHLC data, we connect this to the latest advancements in deep learning performance optimization:

!!! quote
    We use `np.float32` to store OHLC data, reserving `np.float64` only for turnover and volume. Using smaller byte sizes for data storage is a critical direction for AI performance optimization. Around 2020, academia began using `int16` to compress deep learning models, and recent compressions of large models have even started using `int8`.

For instance, many friends have read our article [How Deep Learning-Based Quantitative Strategies Implement Normalization](https://blog.quantide.cn/blog/2023/12/16/%E5%9F%BA%E4%BA%8E%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0%E7%9A%84%E9%87%8F%E5%8C%96%E7%AD%96%E7%95%A5%E5%A6%82%E4%BD%95%E5%AE%9E%E7%8E%B0%E5%BD%92%E4%B8%80%E5%8C%96/). Most readers found this article quite profound. In reality, this article originated from Lesson 13 of our course.

### Structural Characteristics
The course typically begins with a mind map outlining the key knowledge points for the entire lesson, such as:

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/07/lesson13-outline.png)

### Experimental Environment

The online experimental environment for the course is provided by a cluster with 256GB of memory and 192 CPUs. Students do not need to prepare their own experimental environments or data. The online environment provides 3 billion records of market data, real-time market data, and online backtesting capabilities, along with simulated trading testing.

A robust strategy often requires testing across several bull and bear market cycles. Our experimental environment includes 18 years of data, which is unattainable for courses that rely on CSV-based data preparation.

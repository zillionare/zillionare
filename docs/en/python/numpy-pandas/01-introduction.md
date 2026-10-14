---
title: "01 - Your Quant Native Tongue: Numpy & Pandas"
date: 2025-03-08
slug: en/articles/python/numpy-pandas/01-introduction
tags: [Quantitative Investing, Numpy, Pandas, Data Science]
excerpt: "Master Numpy and Pandas, the essential native language for quantitative researchers. This course bridges theory with live trading scenarios, covering data structures, performance optimization, and real-world factor analysis workflows."
lang: en
translation_of: articles/python/numpy-pandas/01-introduction
auto_translated: true
source_sha: 7e34ae46fdecf53b65e08061b5573b63829ab400
cover: "https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2025/03/moon-and-sixpence.jpg"
---

<!--
# Course Introduction
## Course Structure
## What is Numpy
## What is Pandas
Pandas Ecosystem
## Numpy vs. Pandas Comparison
-->

Just as death and taxes are inevitable, Numpy and Pandas hold an equally indispensable status for quantitative professionals—every quant will inevitably interact with these two libraries.

If you examine critical quantitative libraries such as `alphalens`, `empyrical`, `backtrader`, `tushare`, `akshare`, `jqdatasdk`, or excellent quantitative frameworks like `quantaxis`, `zillionare`, and `vnpy`, you will find they all rely on Numpy and Pandas. In fact, any library that depends on Pandas will inevitably have a transitive dependency on Numpy.

If quantitative professionals share a common language, it is Numpy and Pandas. They are the native tongue of quants.

---

Specifically, Numpy and Pandas not only provide tabular-like data structures—Numpy structured arrays and Pandas DataFrames—which are essential for intermediate storage of various data types including market data—but they also offer a wide range of fundamental algorithms.

For example:

1. In **pair trading**, calculating correlation is a crucial step. Both Numpy and Pandas provide functions for correlation calculation.
2. In the calculation of **Alpha 101 factors**, ranking is a fundamental operation—the basis for **layered backtest**—which Pandas provides via the `rank` method.
3. **Max drawdown** is a key metric for evaluating strategies. Numpy supports this through `numpy.maximum.accumulate`.

There are many such commonly used algorithms, which we will introduce one by one in this course.

## Course Structure

A defining feature of this course is its tight alignment with quantitative scenarios. We analyze the source code of important, high-popularity quantitative libraries to identify where Numpy and Pandas are used, then categorize and refine these usage patterns. We also integrate common questions from the quantitative community—often reflecting difficulties quants face when using Numpy/Pandas—to structure the curriculum. This ensures a systematic explanation of these critical libraries while guaranteeing that students can immediately apply the learned methods and techniques to their work, rapidly boosting productivity.

Efficient learning requires high-intensity practice. This course includes extensive exercises. Whether in demo code or exercises, we strive to complete them within quantitative scenarios to enhance your immersion. However, this often requires you to understand these scenarios and the underlying data.

While developing this course, the author read numerous books, blog posts, papers, and open-source project code. For materials closely related to the textbook, we provide reference links as extended readings or footnotes. If you have time, you may read these to gain the same depth of perspective as the author. However, if you are short on time, you can safely skip them and focus solely on the main course content.

---

This course is specifically designed for quantitative trading practitioners, such as **quant developers**, **quant researchers**, and **quant portfolio managers**. If you have basic financial knowledge, this course is also suitable for others needing to learn Numpy and Pandas. The content’s breadth and depth are rare in the current market.

## What is Numpy

<div style="position:relative;float:left">
<img src="https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/10/20261005065445-numpylogo.svg" align="left" style="width: 200px;margin:10px">
<p style="font-size:10px;text-align:center">Image source: numpy.org</p>
</div>

Numpy is the foundational package for scientific computing in Python. It is open-source software that allows free use while preserving original copyright notices. Its name derives from **Numeric Programming**, and its predecessors were the `Numeric` and `Numarray` libraries.

Numpy provides multi-dimensional array objects, various derived objects (such as **masked arrays**), and high-performance routines for array operations, including mathematics, logic, shape manipulation, sorting, selection, I/O, discrete Fourier transforms, basic linear algebra, basic statistical operations, random simulation, and more. The following figure provides a more detailed overview:

<div style='width:80%;text-align:center;margin: 0 auto 1rem'>
<img src='https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/04/numpy-features.jpg?1'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>

---

Numpy’s underlying development language is C, with significant optimizations including parallelization support, the use of OpenBLAS, and advanced SIMD instructions to optimize matrix operations. Python’s flexibility as a "glue language" enabled Numpy to be released as a Python library.

!!! tip
    Many believe that to improve the performance of quantitative strategies, one must abandon Python for C/Rust. This statement is partially correct and partially incorrect.<br><br>If a quant does not understand how to leverage OpenBLAS and LAPACK, even algorithms developed in C may struggle to outperform those calling Numpy via Python. In Numpy, a common matrix multiplication can utilize multi-core parallel processing (multithreading) and advanced CPU instructions to achieve fast BLAS/LAPACK computations. These are knowledge and skills that most people find difficult to master.<br><br>You can check whether your Numpy utilizes OpenBLAS/LAPACK and advanced SIMD instructions using the following method:<br><br>
    ```python
    import numpy as np
    np.show_config()
    ```

Numpy is widely used in academia, finance, and industry, characterized by maturity, speed, stability, and an active community. The current stable version is 2.2.0 (released in March 2025), just one quarter ago, demonstrating the high activity of the Numpy development community.

Numpy serves as the underlying dependency for many well-known Python libraries, including Pandas, SciPy, Statsmodels, and Scikit-learn.

## What is Pandas

Pandas is a Python software library for data manipulation and analysis. It is built on top of Numpy, adding features such as indexing and heterogeneous arrays (equivalent to Numpy’s Structure Array—a concept we will explain in detail later in this course), making it a powerful tool for handling tabular data.

---

The name Pandas derives from **Panel Data** (a term in econometrics referring to datasets observing the same individuals over multiple periods) and **Python Data Analysis**.

Since becoming an open-source project in 2010, Pandas has grown into a substantial library, with a developer community exceeding 2,500 distinct contributors.

<!--
```markmap

# pandas
## 数据结构
## IO
### csv
### HDF5
### JSON
### HTML
### sql
## 索引和查找数据
## 多重索引 
## 数据整理
### merge
### join
### concatenate
### reshape/pivot
## 数据分析
### group by
### window function
## 可视化
### 表格可视化
### 可视化图表
```
-->

<div style='width:75%;text-align:center;margin: 0 auto 1rem'>
<img src='https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/04/pandas-features.jpg'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>

Pandas provides two data structures: `Series` and `DataFrame`. It previously offered a three-dimensional structure called `Panel`, but this was eventually discontinued. Compared to Excel, Pandas can analyze larger datasets more quickly (generally under 10 million rows, depending primarily on the machine’s physical memory).

---

## Extended Reading

<div style='width:33%;float:left;padding: 0.5rem 1rem 0 0;text-align:center'>
<img src='https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/04/wes-mckinney.jpg'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'>Source: Github readme project</span>
</div>

If recommending a book on Pandas, undoubtedly, no other book is more authoritative than [《Python for Data Analysis》](https://wesmckinney.com/), because it was written by Pandas’ creator, Wes McKinney! This book is now available for open access online. Readers can also click [this link](https://wesmckinney.com/book/) to read it. After updates in April 2023, it now supports up to Pandas version 2.0.

Wes McKinney is the creator and lifelong Benevolent Dictator for Life (BDFL) of Pandas. He currently resides in Nashville, Tennessee, and is the CEO and co-founder of DataPad.

Wes McKinney graduated from MIT with a bachelor’s degree and holds a Ph.D. in Mathematics and Statistics from Duke University. While working at AQR Capital Management, he learned Python and began building Pandas. He is also a co-creator of Apache Arrow.

From the history of Pandas’ birth, it is undeniable that Pandas was born for finance/quantitative trading. Wes McKinney’s original intent was to solve the inefficiency and繁琐 (tediousness) of using Microsoft Excel for financial data analysis and statistical operations. Today, quantitative giant Two Sigma[^two-sigma] is a major sponsor of this project. Pandas’ success has also promoted the widespread popularity of Python. One could even say that McKinney single-handedly carved out Python’s survival space.

Creating Pandas generated no direct revenue; initially, Wes McKinney relied on savings from his first job and part-time work to make a living. This is a story similar to *The Moon and Sixpence*, with the protagonist’s background being extremely similar—he was also a finance worker. Fortunately, Wes McKinney achieved success. If you are interested in this story, you can read the article [《Sustainable Open Source Projects Will Win the Future》](https://github.com/readme/stories/wes-mckinney).

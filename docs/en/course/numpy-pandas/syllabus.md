---
title: "NumPy & Pandas Syllabus for Quant Data Processing"
date: 2024-08-27
slug: en/articles/course/numpy-pandas/syllabus
tags: [Quantitative Trading, NumPy, Pandas, Data Processing]
excerpt: "Comprehensive course outline covering NumPy and Pandas for quantitative trading, including core syntax, performance optimization, and real-world quant scenarios."
lang: en
translation_of: articles/course/numpy-pandas/syllabus
auto_translated: true
source_sha: 89a19b37fcd8f6b17a5c3d5397d68ae45854637c
---

<style>

.cols {
    column-count: 2;
    column-gap: 2em;
}

h1, h2, h3, h4 {
    font-weight: 400 !important;
}
h4 {
    color: #808080 !important;
}

h5 {
    color: #a0a0a0 !important;
}

.module {
    text-align: center;
    font-size: 2em;
    margin: 2em 0;
}

em {
    font-size: 0.75em;
    font-style: italic;
    color: #808080;
}

 @media only screen and (max-width: 1024px) {
  .md-sidebar-toc {
    display:none;
    width: 0;
  }
  
  .cols {
      column-count: 1;
    }
    
  .markdown-preview {
      left: 0px !important;
      width: 100% !important;
  }
}


</style>

<p>§ NUMPY AND PANDAS IN QUANTITATIVE TRADING</p>
<h1 style="text-align:center">Course Syllabus</h1>

<div class="cols">

## 1. Introduction
## 2. NumPy Core Syntax (1)
<!--https://github.com/yingzk/100_numpy_exercises/blob/master/cn_100_numpy_exercises.md-->
### 2.1. Basic Data Structures
#### 2.1.1. Creating Arrays
_Common methods for creating arrays, along with several built-in arrays frequently used in quantitative finance._
#### 2.1.2. Adding, Deleting, and Modifying Elements
_How to append, insert, delete, and modify elements in an array?_
#### 2.1.3. Indexing, Reading, and Searching
_Introduction to indexing, slicing, searchsorted, etc._
<!--indexing,slicing and mask-->
#### 2.1.4. Inspecting Arrays
### 2.2. Array Operations
#### 2.2.1. Dimensionality Increase
#### 2.2.2. Dimensionality Reduction
#### 2.2.3. Transposition

## 3. NumPy Core Syntax (2)
### 3.1. Structured Arrays
### 3.2. Arithmetic Operations
#### 3.2.1. Logical Operations and Comparisons
#### 3.2.2. Set Operations
#### 3.2.3. Mathematical and Statistical Operations
_Matrix operations and statistical functions such as mean, variance, covariance, and percentiles._
### 3.3. Type Conversion and Typing
_In-depth understanding of NumPy data types and their conversions, along with the `typing` library, to help write robust code._
## 4. NumPy Core Syntax (3)
### 4.1. Handling Data with `np.nan`
_Data obtained from third parties may contain `np.nan`; technical indicator values during the warm-up period are often `np.nan` as well. This section introduces `np.isnan`, `nanmean`, `nanmax`, and other `nan*` functions for calculating mean or maximum values when data contains `None` or `np.nan`._
### 4.2. Random Numbers and Sampling
<!--https://github.com/Kyubyong/numpy_exercises-->
_Random number generation and sampling are high-frequency operations in quantitative finance, particularly useful for synthetic data generation._
### 4.3. I/O Operations
_Introduction to reading and saving CSV files and other I/O operations._
### 4.4. Dates and Times
_How to convert time and date formats from market data obtained via other libraries?_
### 4.5. String Operations
_How to perform string searches and other operations within NumPy arrays?_
## 5. NumPy Quantitative Scenario Applications
### 5.1. Continuous Value Statistics
_Example: Efficiently finding consecutive price limits (up/down), N-day winning/losing streaks, and calculating `streaks` in Connor's RSI._
### 5.2. Cumulative Sum and Intraday Average Price Line
_The intraday average price line is crucial for intraday trading. Generally, two attacks on the average price line that fail to break it signal an intraday buy (or sell). How do we calculate this average price line?_
### 5.3. Moving Average Calculation
_How to quickly calculate moving averages using NumPy? Introduction to a convolution algorithm._
### 5.4. Rational Selection of Adaptive Parameters
_Often, adaptive parameters are required. How to select them? Percentiles are often a good solution._
### 5.5. Calculating Maximum Drawdown
_With experience, you can identify the major rebound on February 7th. On rebound days, you want to target stocks with the largest declines. How to select them?_
### 5.6. Determining Long-Term Trends for Individual Stocks
_Do not buy stocks with long-term bearish trends. The key is how to determine this. This section introduces polynomial regression._
### 5.7. Function Routines in Alpha101
_Alpha101 contains several basic functions upon which factors are built. How to implement them efficiently?_
### 5.8. Finding Similar Candlestick Patterns
_Introduction to `corrcoef` and `correlate`._
### 5.9. Asset Portfolio Return and Volatility Example
_Start by randomly generating several assets, then calculate their expected returns and volatility. This is one of the high-frequency application scenarios._
<!--https://www.quantrocket.com/code/?repo=quant-finance-lectures&path=%2Fcodeload%2Fquant-finance-lectures%2Fquant_finance_lectures%2FLecture03-Introduction-to-NumPy.ipynb.html-->
## 6. NumPy High-Performance Programming Practices
### 6.1. Broadcasting
_In-depth look at NumPy's efficient underlying principles._
### 6.2. Using NumExpr
<!--https://github.com/aialgorithm/Blog/issues/48-->
### 6.3. Enabling Multithreading
### 6.4. Using the Bottleneck Library
### 6.5. Other Alternatives to NumPy

## 7. Pandas Core Syntax (1)
<!--https://github.com/justmarkham/pandas-videos-->
<!--https://bkds.flygon.net/#/docs/pyda-3e/README-->
### 7.1. Basic Data Structures
<!--Understand index, columns, etc.-->
#### 7.1.1. Series
#### 7.1.2. Creating DataFrames
#### 7.1.3. Rapid Exploration of DataFrames
_Index, info, describe, columns, head, tail, etc._
#### 7.1.4. Merging and Joining DataFrames
<!--concat, join, merge-->
#### 7.1.5. Deleting Rows and Columns
#### 7.1.6. Indexing, Reading, and Modifying
_Introduction to indexing and data selection in Pandas._
#### 7.1.7. Transposition
#### 7.1.8. Resampling
_Intraday real-time minute-level data is surprisingly expensive. Therefore, we need to synthesize it from tick-level data ourselves. This is resampling._

## 8. Pandas Core Syntax (2)
### 8.1. Logical Operations and Comparisons
_DataFrames contain the features we extract. How to select the top 30 columns with the highest PE and lowest PB?_
### 8.2. Groupby Operations
_The factor analysis data table contains industry labels and each company's PE value. How to select the top 5 stocks with the strongest PE in each industry?_
### 8.3. Multi-Index and Advanced Indexing
_One of the more difficult concepts in Pandas._
### 8.4. Window Functions
_For calculating sliding window indicators such as moving averages._
### 8.5. Mathematical and Statistical Operations
_Basic quant functions including mean, variance, covariance, percentile, diff, pct_change, rank, etc._
## 9. Pandas Core Syntax (3)
### 9.1. Data Preprocessing
_What to do during factor analysis preprocessing, such as handling missing values, winsorization, and deduplication?_
<!--fillna, clip, winsorize,dropna-->
### 9.2. I/O Operations
_How to read data from CSVs, web pages, databases, Parquet files, etc.?_
#### 9.2.1. CSV
_Beyond basic operations, we will also introduce how to accelerate CSV reading._
#### 9.2.2. PKL and HDF5
#### 9.2.3. Parquet
#### 9.2.4. HTML and MD
<!--Think of it as web scraping from another perspective-->
#### 9.2.5. SQL
### 9.3. Dates and Times
_How to convert time and date formats from market data obtained via other libraries?_
### 9.4. String Operations
_DataFrames store basic security information, such as names and codes. How to exclude stocks from the STAR Market?_
## 10. Pandas Core Syntax (4)
### 10.1. Tables and Styling
_Giving Pandas rich conditional formatting capabilities similar to Excel._
### 10.2. Pandas Built-in Plotting Functions
## 11. Pandas Quantitative Scenario Applications
### 11.1. Implementing TongdaXin Routines via Rolling Methods
_Implementing TongdaXin formula methods such as HHV, LLV, HHVBARS, LAST, etc._
### 11.2. Filling Missing Adjustment Factors for Minute-Level Data
_Introduction to the newly introduced `as-of-join` feature. A must-know scenario for quantitative finance._
### 11.3. Preparing Data for Alphalens
_The most common DataFrame operations when using Alphalens for factor analysis._
## 12. Pandas Performance
### 12.1. Memory Optimization
_Compressing memory usage by using `category` dtype and more compact data types._
### 12.2. Optimizing Iterations
_Use `itertuples` instead of `iterrows`, use `apply` to optimize iterations, and filter before calculating._
### 12.3. Using NumPy and Numba
### 12.4. Using `eval` or `query`
<!--Use isin for filtering https://zhuanlan.zhihu.com/p/97012199-->
### 12.5. Other Alternatives to Pandas
#### 12.5.1. Modin
_One line of code to replace Pandas, gaining multi-core and memory-unlimited computational power._
#### 12.5.2. Polars
_The fastest table solution._
#### 12.5.3. Dask
_Distributed table processing, capable of running on thousands of nodes._

</div>
<!--
rename columns, sort_values
filter rows by column value 
logical operator
change datatype
Pandas Index
pivot_table https://www.joinquant.com/view/community/detail/92d2ccab2d412dbfa7df366369e6373b
-->

<script>
    var sidebarTOCBtn = document.getElementById('sidebar-toc-btn')
    sidebarTOCBtn.addEventListener('click', function (event) {
        event.stopPropagation()
        if (document.body.hasAttribute('html-show-sidebar-toc')) {
            document.body.removeAttribute('html-show-sidebar-toc')
        } else {
            document.body.setAttribute('html-show-sidebar-toc', true)
        }
    })

    var sidebarTOCBtn = document.getElementById('sidebar-toc-btn')
    document.body.setAttribute('html-show-sidebar-toc', true)
    window.addEventListener('load', function () {
        const urlParams = new URLSearchParams(window.location.search);
        // Read the 'level' parameter from the URL
        const level = parseInt(urlParams.get('level'), 10);

        // If 'level' is not specified or is not a number, do nothing.
        if (isNaN(level)) {
            return;
        }

        const h3s = document.querySelectorAll('h3');
        const h4s = document.querySelectorAll('h4');
        const h5s = document.querySelectorAll('h5');

        // Control visibility based on the level
        if (level === 1) {
            // Level 1: Hide h3 and h4
            h3s.forEach(h => h.style.display = 'none');
            h4s.forEach(h => h.style.display = 'none');
            h5s.forEach(h => h.style.display = 'none');
        } else if (level === 2) {
            // Level 2: Hide only h4
            h4s.forEach(h => h.style.display = 'none');
            h5s.forEach(h => h.style.display = 'none');
        }
        // For level 3 or higher, all headings remain visible by default.
    });
</script>

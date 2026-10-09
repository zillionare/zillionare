---
title: "24 Lessons in Quantitative Investing: Complete Syllabus"
date: 2023-05-13
cover: "https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/10/20261009154146-cover-course-24lectures-syllabus.md.jpg"
slug: en/articles/course/24lectures/syllabus
tags: [Quantitative Investing, Factor Analysis, Backtesting, Live Trading]
excerpt: "Comprehensive syllabus for quantitative trading, covering data sources, strategy development, factor analysis, backtesting frameworks, and live trading integration for China A-shares."
lang: en
translation_of: articles/course/24lectures/syllabus
auto_translated: true
source_sha: ccb0857b7b991b558d1fb54935d1f50525306c2a
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

<p>§ 24 Lessons in Quantitative Investing</p>
<h1 style="text-align:center">Course Syllabus</h1>
<div class="module">I. Securities Fundamentals and Data Sources</div>

<em>This section covers the essential securities knowledge required for quantitative trading, such as price adjustment (adjusted prices). Adjusted prices are an unavoidable issue in quantitative trading and will permeate our entire course, yet many answers found online are incorrect. This section also reveals an unexpected issue: Python has problems with rounding.</em>

## 1. Introduction
### 1.1. Development of Securities Investment and Quantitative Trading
### 1.2. Knowledge Framework for Quantitative Trading
### 1.3. Who is Suitable for Quantitative Trading?
### 1.4. Overview of Quantitative Strategies
#### 1.4.1. Alpha Strategies
#### 1.4.2. Market-Neutral Strategies
#### 1.4.3. High-Frequency Arbitrage Strategies
#### 1.4.4. Technical Analysis-Based Strategies
#### 1.4.5. Strategy Research Methods
### 1.5. Course Content Overview
### 1.6. How to Study This Course
#### 1.6.1. Prerequisites
#### 1.6.2. Introduction to Online Quantitative Environments

## 2. Securities Fundamentals and Data Sources: Akshare
### 2.1. Exchanges and Security Codes
### 2.2. Knowledge of Price Adjustment (Adjusted Prices)
### 2.3. Akshare
#### 2.3.1. Installing akshare in the Course Environment
#### 2.3.2. Real-Time Stock Data
#### 2.3.3. Historical Stock Data
#### 2.3.4. Security Lists
#### 2.3.5. Trading Calendars
#### 2.3.6. Encapsulation and Improvement Suggestions
#### 2.3.7. Exercises

## 3. Data Sources: Tushare, JqDataSdk
### 3.1. TUSHARE
#### 3.1.1. Installation and Token Setup in Course Environment
#### 3.1.2. Historical Stock Data
#### 3.1.3. Security Lists
#### 3.1.4. Trading Calendars
### 3.2. JoinQuant Local Data
#### 3.2.1. Account Installation and Setup in Course Environment
#### 3.2.2. Historical Stock Data
#### 3.2.3. Security Lists
#### 3.2.4. Trading Calendars
### 3.3. BAOSTOCK
#### 3.3.1. Historical Stock Data
#### 3.3.2. Security Lists
### 3.4. YFINANCE
<em>The exercises in this section will highlight the linear transformation relationship between forward and backward adjusted prices.</em>
  
## 4. Using Zillionare for Data Retrieval
### 4.1. Omicron
#### 4.1.1. Initializing Omicron
#### 4.1.2. Real-Time Stock Data
#### 4.1.3. Historical Stock Data
#### 4.1.4. Security Lists
#### 4.1.5. Trading Calendars
#### 4.1.6. Sector Data
### 4.2. Interpreting A-Share Data: Relationship Between Investor Count and Market Trends

## 5. Exercise Solutions (Video Only)

<div class="module">
II. Introduction to Strategies
</div>
<em>Lessons 6–8 constitute the second part of the course. We introduce three types of strategies from the perspectives of fundamentals, technicals, and trade execution, along with how to write strategy backtests and build a simple backtesting framework. In the examples, we also provide additional strategies, such as Connor's RSI strategy.</em>

## 6. Small-Cap Strategy
### 6.1. Introduction to Small-Cap Strategy
### 6.2. Strategy Implementation - Manually Implementing the Simplest Backtest
#### 6.2.1. Initialization
#### 6.2.2. Plotting
#### 6.2.3. Main Strategy Code
### 6.3. Strategy Optimization
#### 6.3.1. Timing Optimization
#### 6.3.2. Rule Optimization
#### 6.3.3. Parameter Optimization
  
## 7. Bollinger Bands Strategy
### 7.1. Initialization Using Coursea
### 7.2. Bollinger Bands Strategy Based on Base Class - Frameworking the Backtest
### 7.3. Discussion on Strategy Optimization Directions
#### 7.3.1. Parameter Optimization
#### 7.3.2. Trend Judgment
  
## 8. Grid Trading
### 8.1. Grid Trading - A Strategy Without Timing
### 8.2. Code Implementation
#### 8.2.1. Initialization
#### 8.2.2. Evaluation Function
#### 8.2.3. Strategy Behavior Analysis
### 8.3. Technical Implementation Issues
#### 8.3.1. Order Price and Trading Timing
#### 8.3.2. Stock Split and Bonus Issues
#### 8.3.3. Trading Units
### 8.4. Strategy Optimization: From 1.37% to 79.8%!
#### 8.4.1. Selecting Underlying Assets with "Bounds"
##### 8.4.1.1. Large-Cap Stocks
##### 8.4.1.2. Deeply Oversold Stocks
##### 8.4.1.3. Convertible Bonds
#### 8.4.2. Determining Grid Parameters Based on Historical Data
#### 8.4.3. Improving Capital Efficiency
### 8.5. Trend-Following Grid

<div class="module">III. Data Analysis in Quantitative Trading: Theory and Implementation</div>
<em>Lessons 9–13 cover the fundamentals of quantitative analysis, focusing on the usage of libraries such as Numpy, Pandas, and Talib. The exercises in Chapter 9 provide many clever and commonly used Numpy exercises in quantitative trading.</em>

## 9. Numpy and Pandas
### 9.1. Numpy
#### 9.1.1. Creating Arrays
##### 9.1.1.1. Vanilla Version
##### 9.1.1.2. Pre-defined Special Arrays
##### 9.1.1.3. Conversion from Existing Arrays
#### 9.1.2. Inspecting Array Properties
#### 9.1.3. Array Operations
##### 9.1.3.1. Dimensionality Increase
##### 9.1.3.2. Dimensionality Reduction
##### 9.1.3.3. Transposition
##### 9.1.3.4. Adding/Removing Elements
#### 9.1.4. Logical Operations and Comparisons
#### 9.1.5. Set Operations
#### 9.1.6. Mathematical Operations
##### 9.1.6.1. Dot Product
##### 9.1.6.2. Aggregation Operations and Statistical Functions
#### 9.1.7. Reading, Searching, and Lookup
##### 9.1.7.1. Indexing and Slicing
##### 9.1.7.2. Lookup, Replacement, and Filtering
#### 9.1.8. Type Conversion and typing Module
#### 9.1.9. Structured Arrays
#### 9.1.10. IO
#### 9.1.11. Common Functions in Quantitative Trading
##### 9.1.11.1. REF(close, n)
##### 9.1.11.2. EVERY(cond, n)
##### 9.1.11.3. LAST(cond_list, n, m)
##### 9.1.11.4. BARSLAST
##### 9.1.11.5. CROSS
### 9.2. Pandas
#### 9.2.1. Creation
#### 9.2.2. Data Access
#### 9.2.3. Iterating DataFrames
### 9.3. Pandas vs. Numpy
  
## 10. Ta-Lib
### 10.1. Installing Ta-Lib
#### 10.1.1. Installing the Native Library
##### 10.1.1.1. macOS
##### 10.1.1.2. Linux
##### 10.1.1.3. Windows
##### 10.1.1.4. Using Conda
##### 10.1.1.5. Third-Party Built Wheel Packages
#### 10.1.2. Installing the Python Wrapper
### 10.2. Ta-Lib Overview
#### 10.2.1. About the Documentation
#### 10.2.2. Two Types of Interfaces
#### 10.2.3. Method Overview
### 10.3. Common Indicator Functions
#### 10.3.1. ATR
#### 10.3.2. Moving Averages
##### 10.3.2.1. SMA
##### 10.3.2.2. EMA
##### 10.3.2.3. WMA
#### 10.3.3. Bollinger Bands
#### 10.3.4. MACD
#### 10.3.5. RSI
#### 10.3.6. OBV (On-Balance Volume)
### 10.4. Pattern Recognition Functions
#### 10.4.1. CDL3LINESTRIKE
#### 10.4.2. CDL3WHITESOLDIERS
  
<em>Statistics and probability play a crucial role in quantitative analysis. Lessons 11–12 review the most common statistical and probabilistic knowledge in quantitative trading, including moments from first to fourth, PDF/CDF, and covariance. The examples in this chapter solve problems such as whether to buy the dip when the Shanghai Composite Index drops by 4%.</em>

## 11. Data Analysis and Python Implementation (1)
### 11.1. Examining Data Distribution
#### 11.1.1. Finding the Center of Data
##### 11.1.1.1. Mean and Centroid
##### 11.1.1.2. Median
##### 11.1.1.3. Mode
#### 11.1.2. Measuring Data Dispersion
##### 11.1.2.1. Quantiles
##### 11.1.2.2. Variance and Standard Deviation
##### 11.1.2.3. Frequency, PMF, PDF, CDF, PPF, and Histograms
##### 11.1.2.4. Probability Density and Probability Density Function
##### 11.1.2.5. Cumulative Probability and Cumulative Distribution Function (CDF)
##### 11.1.2.6. CDF Estimation and Applications
##### 11.1.2.7. Relationships Between Concepts
#### 11.1.3. Distribution Shape of Data
#### 11.1.4. Concept of Central Moments
#### 11.1.5. Interpretation and Application of Skewness and Kurtosis in Investment
  
## 12. Data Analysis and Python Implementation (2)
### 12.1. Statistical Inference Methods
#### 12.1.1. Quantile Plots
#### 12.1.2. Hypothesis Testing Methods
### 12.2. Fitting, Regression, and Residuals
#### 12.2.1. Residuals and Their Measurement
##### 12.2.1.1. max_error
##### 12.2.1.2. mean_absolute_error
##### 12.2.1.3. mean_absolute_percentage_error
##### 12.2.1.4. mean_squared_error
##### 12.2.1.5. Rooted Mean Squared Error
#### 12.2.2. Regression Analysis
### 12.3. Correlation
#### 12.3.1. Covariance and Correlation Coefficient
#### 12.3.2. Pearson and Spearman Correlation
#### 12.3.3. Correlation Analysis Examples
### 12.4. Distance and Similarity
#### 12.4.1. Listing Common Distance Definitions
#### 12.4.2. How to Calculate Distance
### 12.5. Normalization
  

## 13. Practical Technical Analysis

<em>Traditional technical analysis lacks strong theoretical support, but it is based on traders' experience and thus has its rationale. After learning Lessons 11–12, we apply our knowledge to technical analysis and discover new insights. Traditional technical analysis, empowered by statistical theory and adaptive parameters, significantly improves algorithm robustness and timing capabilities.</em>

### 13.1. Box Detection
#### 13.1.1. Statistical-Based Methods
#### 13.1.2. Clustering-Based Algorithms
### 13.2. Finding Peaks and Valleys
#### 13.2.1. Implementation in SciPy
#### 13.2.2. Third-Party Library: Zigzag
#### 13.2.3. Smoothing Curves
#### 13.2.4. Double-Top Pattern Detection
#### 13.2.5. Rounding Bottom Detection
### 13.3. Convexity/Concavity Detection

## 14. Factor Analysis

<em>Factors are features with predictive power. Factor analysis and testing are rapid screening methods for their characteristics and are mandatory knowledge for entering quantitative institutions. We manually implement each step of factor analysis step-by-step, then introduce Alphalens, a common factor testing framework.</em>

### 14.1. Factor Classification
### 14.2. Factor Analysis
#### 14.2.1. Preprocessing
##### 14.2.1.1. Outlier Clipping
##### 14.2.1.2. Missing Values Handling
##### 14.2.1.3. Distribution Adjustment
##### 14.2.1.4. Standardization
##### 14.2.1.5. Neutralization
### 14.3. Single-Factor Testing
#### 14.3.1. Regression Method
##### 14.3.1.1. Factor Evaluation via Regression
#### 14.3.2. IC Analysis Method
##### 14.3.2.1. Factor Evaluation via IC Analysis
#### 14.3.3. Layered Backtest Method
#### 14.3.4. Differences and Connections Among the Three Methods
### 14.4. Factor Evaluation System
  
## 15. Alphalens and Others
### 15.1. Alphalens
#### 15.1.1. Alphalens Call Flow
#### 15.1.2. Data Preprocessing
#### 15.1.3. Factor Analysis
#### 15.1.4. Common Alphalens Errors and Warnings
##### 15.1.4.1. Timezone Issues
##### 15.1.4.2. MaxLossExceedError
##### 15.1.4.3. FutureWarning
### 15.2. JQFactor and jqfactor-analyzer
### 15.3. SymPy
### 15.4. Statistics
### 15.5. Statsmodels
#### 15.5.1. OLS (Ordinary Least Squares) Estimation
#### 15.5.2. Comparing OLS with RLM
#### 15.5.3. ARIMA Models and Time Series Forecasting
### 15.6. Zipline
### 15.7. Pyfolio
### 15.8. TA

<div class="module">IV. Data Visualization</div>

<em>Plotting is not just for creating beautiful visualizations but also for unlocking the full potential of data and revealing hidden insights. This holds true in quantitative trading as well. We need the ability to plot candlestick charts and overlay backtest signals for strategy tuning, as well as generate backtest reports.</em>

## 16. Matplotlib Plotting
### 16.1. Introduction to Matplotlib
### 16.2. How Plots Are Constructed
#### 16.2.1. Top-Level Concepts
#### 16.2.2. Relationships Between pyplot, Figure, and Axes
#### 16.2.3. Layout
#### 16.2.4. Figure Anatomy
### 16.3. High-Frequency Usage Objects
#### 16.3.1. Axis
##### 16.3.1.1. Spine Positioning and Hiding
##### 16.3.1.2. Sharing X-Axis
##### 16.3.1.3. Ticks
#### 16.3.2. Text and Chinese Characters
#### 16.3.3. Styles and Colors
##### 16.3.3.1. Colormaps
  
## 17. Plotly Plotting
### 17.1. Basic Concepts in Plotly
### 17.2. Plotly Module Structure
#### 17.2.1. Plotly Express
#### 17.2.2. Graph Objects
#### 17.2.3. Others
### 17.3. Comparing Plotly Express with go.Figure
### 17.4. Plotly Stock Analysis Chart Drawing
#### 17.4.1. Candlestick Chart Drawing
#### 17.4.2. Overlaying Technical Indicators
#### 17.4.3. Subplots
#### 17.4.4. Display Areas
#### 17.4.5. Interactive Tooltips
### 17.5. Colors
#### 17.5.1. Discrete Color Sequences
#### 17.5.2. Continuous Color Scales
### 17.6. Themes and Templates
### 17.7. Introduction to Dash
#### 17.7.1. Hello World
#### 17.7.2. Connecting to Data
#### 17.7.3. Adding Interactive Controls
#### 17.7.4. Beautifying Applications
#### 17.7.5. Deep Dive into Dash
  
## 18. Seaborn and PyEcharts Plotting
### 18.1. Seaborn
#### 18.1.1. Seaborn Plotting Overview
##### 18.1.1.1. Visualizing Statistical Relationships
##### 18.1.1.2. Visualizing Data Distributions
##### 18.1.1.3. Visualizing Bivariate Distributions
##### 18.1.1.4. Joint and Marginal Distributions
##### 18.1.1.5. Regression Fitting
#### 18.1.2. Themes
#### 18.1.3. Using Palettes
##### 18.1.3.1. Qualitative Palettes
##### 18.1.3.2. Continuous Palettes
##### 18.1.3.3. Diverging Palettes
### 18.2. PyEcharts
#### 18.2.1. Running in Notebook/JupyterLab
#### 18.2.2. Calling Conventions
#### 18.2.3. Using Options
#### 18.2.4. Subplots and Layouts
##### 18.2.4.1. Grid Layout
##### 18.2.4.2. Page Layout
##### 18.2.4.3. Tab Layout
##### 18.2.4.4. Timeline
### 18.3. On Colors and Aesthetics

<div class="module">V. Backtesting Framework</div>

<em>Backtrader is the most famous open-source backtesting framework. Many institutions lack the R&D capability for proprietary quantitative investment research systems and often use backtrader internally for backtesting. We dedicate two lessons to explaining backtrader in depth.</em>

## 19. Backtrader Backtesting Framework (1)
### 19.1. Quick Start
### 19.2. Backtrader Syntax Sugar
#### 19.2.1. Time Series (Lines)
#### 19.2.2. Operator Overloading
### 19.3. Data Feeds
#### 19.3.1. GenericCSVData
#### 19.3.2. Pandas Feed
#### 19.3.3. Customizing a Feed
#### 19.3.4. Adding New Data Columns
### 19.4. Multi-Timeframe Data
#### 19.4.1. Comparing Multi-Timeframe Technical Indicators
### 19.5. Indicators
#### 19.5.1. Built-In Indicator Library
#### 19.5.2. Custom Indicators
##### 19.5.2.1. Minimum Period
  
## 20. Backtrader Backtesting Framework (2)
### 20.1. Cerebro
#### 20.1.1. Adding Loggers
#### 20.1.2. Adding Observers
#### 20.1.3. Execution and Plotting
### 20.2. Order
#### 20.2.1. notify_order
### 20.3. Trading Agents
#### 20.3.1. Querying Assets and Positions
#### 20.3.2. Volume Limits
##### 20.3.2.1. FixedSize
##### 20.3.2.2. FixedBarPerc
##### 20.3.2.3. BarPointPerc
#### 20.3.3. Trading Timing - Cheat-On-Open
#### 20.3.4. Trading Timing - Cheat-On-Close
#### 20.3.5. Trading Functions
##### 20.3.5.1. Standard Trading Functions
##### 20.3.5.2. order_target Series
#### 20.3.6. Portfolio Trading
#### 20.3.7. OCO Orders
#### 20.3.8. Slippage and Transaction Costs
##### 20.3.8.1. Fixed Slippage
##### 20.3.8.2. Percentage Slippage
#### 20.3.9. Transaction Fees
### 20.4. Visualization
#### 20.4.1. Observers
##### 20.4.1.1. Broker Observer
##### 20.4.1.2. BuySell Observer
##### 20.4.1.3. Trade Observer
##### 20.4.1.4. TimeReturn Observer
##### 20.4.1.5. DrawDown Observer
##### 20.4.1.6. Benchmark Observer
#### 20.4.2. Custom Plotting
#### 20.4.3. Collecting Backtest Data
### 20.5. Optimization
### 20.6. Summary

## 21. Strategy Backtest Evaluation

<em>How to interpret backtest results? This is a strategy evaluation issue. Here we also answer a question: If your strategy goes live but performs below expectations, under what circumstances should you abort the strategy? This is a common interview question.</em>

### 21.1. Return Rates
#### 21.1.1. Simple Return Rate
#### 21.1.2. Log Return Rate
#### 21.1.3. Cumulative Returns
#### 21.1.4. Aggregate Returns
#### 21.1.5. Annual Return
### 21.2. Risk-Adjusted Returns
#### 21.2.1. Sharpe Ratio
#### 21.2.2. Relationship Between Sharpe Ratio and Asset Curve
#### 21.2.3. Sortino Ratio
#### 21.2.4. Max Drawdown
#### 21.2.5. Relationship Between Sharpe and Max Drawdown
#### 21.2.6. Annualized Volatility
#### 21.2.7. Calmar Ratio
#### 21.2.8. Omega Ratio
### 21.3. Benchmark-Related Metrics
#### 21.3.1. Information Ratio
#### 21.3.2. Alpha/Beta
### 21.4. Visualization of Strategy Evaluation
#### 21.4.1. Metrics
#### 21.4.2. Plots
#### 21.4.3. Basic and Full
#### 21.4.4. HTML
  
## 22. Backtesting Traps

<em>Have you heard of the phenomenon where strategies "feast" during backtesting but "starve" in live trading? How is it caused? This section introduces backtesting traps, using rich practical experience to help you quickly compensate for insufficient live trading experience.</em>

### 22.1. Survivorship Bias
### 22.2. Look-Ahead Bias
#### 22.2.1. Reference Errors
#### 22.2.2. Price Stealing
#### 22.2.3. Look-Ahead Bias Caused by Price Adjustment
#### 22.2.4. PIT (Point-in-Time) Data
### 22.4. Trading Rules
#### 22.4.1. T+1 Trading
#### 22.4.2. Price Limits (Up/Down Limits)
### 22.5. Overfitting
### 22.6. Backtest Duration
### 22.7. Differences Between Backtesting and Live Trading
#### 22.7.1. Signal Flickering
#### 22.7.2. Impact Costs
#### 22.7.3. Impossible Execution Prices
#### 22.7.4. Matching Issues
### 22.8. Monopoly Backtesting Framework
#### 22.8.1. Backtest Function Overview
##### 22.8.1.1. Architecture and Style
#### 22.8.2. Strategy Framework
##### 22.8.2.1. Data and Data Formats
##### 22.8.2.2. Multi-Timeframe Data
##### 22.8.2.3. Drive Mode and Performance
##### 22.8.2.4. Backtest Reports
#### 22.8.3. Complete Strategy Example
#### 22.8.4. Parameter Optimization
### 22.9. References

<div class="module">VI. Integrating with Live Trading</div>

<em>All preparations are ultimately for integrating with live trading. The last two lessons will introduce various integration solutions.</em>

## 23. Live Trading Interfaces (1)
### 23.1. EasyTrader
#### 23.1.1. Installation
#### 23.1.2. Lifecycle
##### 23.1.2.1. Connecting to Client
##### 23.1.2.2. Retrieving Account Information
##### 23.1.2.3. Trading
#### 23.1.3. Server Mode
#### 23.1.4. Automated Copy Trading
### 23.2. East Money EMC Smart Trading Terminal
#### 23.2.1. Installation
##### 23.2.1.1. Single Directory for Configuration Files
#### 23.2.2. Operation and Maintenance
##### 23.2.2.1. Startup
##### 23.2.2.2. Daily Maintenance
#### 23.2.3. Troubleshooting and Help
#### 23.2.4. Matching Configuration Rules
### 23.3. Trader-GM-Adaptor
#### 23.3.1. Smoke Testing
#### 23.3.2. Client-Server Interaction
##### 23.3.2.1. Client Requests
##### 23.3.2.2. Return Results
#### 23.3.3. API Examples
##### 23.3.3.1. Asset Table
##### 23.3.3.2. Position Table
##### 23.3.3.3. Limit Buy
##### 23.3.3.4. Market Buy
##### 23.3.3.5. Limit Sell
##### 23.3.3.6. Market Sell
##### 23.3.3.7. Cancel Order
##### 23.3.3.8. Query Today's Orders
  
## 24. Live Trading Interfaces (2)
### 24.1. PTrade
#### 24.1.1. Application and Installation
#### 24.1.2. Strategy Framework Overview
##### 24.1.2.1. Initialize
##### 24.1.2.2. Before Trading Start
##### 24.1.2.3. Handle Data
##### 24.1.2.4. After Trading End
#### 24.1.3. A Dual-Moving-Average Strategy
#### 24.1.4. Price Adjustment Mechanism
### 24.2. QMT
#### 24.2.1. Installation and Applying for Quantitative Permissions
#### 24.2.2. Feature Overview
##### 24.2.2.1. My Sectors
##### 24.2.2.2. Model Research
##### 24.2.2.3. Model Trading
### 24.3. QMT-Mini
### 24.4. XtData
#### 24.4.1. Retrieving Security Lists
#### 24.4.2. Retrieving Trading Calendars
#### 24.4.3. Retrieving Market Data
### 24.5. XtTrader
#### 24.5.1. Encapsulating as Web Service
  
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

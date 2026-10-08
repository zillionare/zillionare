---
title: "Factor ML Course Syllabus: From Alpha Mining to Live Trading"
date: "2026-10-09"
slug: en/articles/course/factor-ml/syllabus
tags: [Factor Investing, Machine Learning, Quantitative Trading, Alphalens]
excerpt: "A comprehensive syllabus for quantitative researchers covering factor mining, Alphalens analysis, and machine learning strategies using LightGBM and CNNs for systematic trading."
lang: en
translation_of: articles/course/factor-ml/syllabus
auto_translated: true
source_sha: 89146a9a53b84785e892ff282ca2184326052990
---

<style>

.cols {
    column-count: 2;
    column-gap: 2em;
}

h1 {
    font-weight: 400 !important;
}

h2 {
    margin-top: 2em;
}

h3 {
    color: #303030 !important;
    font-weight: 200 !important;
    font-size: 1.2em;
}

h4 {
    color: #808080 !important;
    font-weight: 100 !important;
    font-size: 1em;
    margin-left: 1em;
}

h5 {
    display: none;
}

.module {
    text-align: center;
    font-size: 2em;
    margin: 2em 0;
}

more {
    font-size: 0.75em;
    color: #808080;
    /* border: 1px solid #ccc; */
    margin: 2.5em 0 -1em 0;
    position: relative;
    cursor: pointer;
    /* min-height: 2em; */
    display: inline-block;
}

more::before {
    content: 'Course Highlights >';
    position: absolute;
    /* top: 50%; */
    /* left: 100%; */
    transform: translate(0, -50%);
    width: 5em;
    height: 3em;
    /* background-color: #ccc; */
    transition: transform 0.3s ease;
}

more.expanded::before {
    content: '';
}

more > p {
    display: none;
    transition: height 0.5s ease; /* Smooth transition effect */
}

more.expanded > p {
    display: block;
}

hr {
    height: 1px !important;
    color: #ddd !important;
    border: none;
    background-image: linear-gradient(to right, 
                    rgba(0, 0, 0, 0.2), 
                    rgba(0,0,0,0));
    background-repeat: no-repeat;
    width: 80%;
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

<p>§ Factor Investing & Machine Learning Strategies</p>
<h1 style="text-align:center">Course Syllabus </h1>
<div class="cols">

<a href="#declaration">Syllabus Notes</a>

## 1. Introduction

### 1.1. The Origins of Factor Investing
### 1.2. Hunting for Alpha
### 1.3. From CAPM to Multi-Factor Models
### 1.4. From Factor Analysis to Factor Investing
### 1.5. From Factor Models to Trading Strategies
### 1.6. Course Structure

<more>

This course is designed for professional quantitative researchers, those transitioning into the field, or professionals from other disciplines determined to explore quantitative research with a rigorous, professional attitude.

Upon completing and mastering this course, you will possess proficient factor analysis skills, master state-of-the-art machine learning strategy construction methods, and become a quantitative researcher with innovative research capabilities and a competitive edge.

The curriculum covers the entire process from factor mining and testing to building machine learning models. If you intend to engage in independent trading, you should supplement your learning with "Quantitative Trading 24 Lessons."

</more>

---

## 2. Factor Preprocessing Pipeline
### 2.1. Factor Data Sources
### 2.2. Factor Generation
### 2.3. Factor Preprocessing
#### 2.3.1. Outlier Clipping
#### 2.3.2. Missing Values Handling
#### 2.3.3. Distribution Adjustment
#### 2.3.4. Standardization
#### 2.3.5. Neutralization

<more>

This chapter and the next form the foundation for factor testing. We will introduce the basic principles and technical implementation details of factor testing using extensive example code, laying a solid groundwork for understanding the Alphalens factor analysis framework.

</more>

---

## 3. Factor Testing Methods
### 3.1. Regression Method
### 3.2. IC Analysis
### 3.3. Layered Backtest Method
### 3.4. Code Implementation of Factor Testing
#### 3.4.1. Generating Factors: Further Modularization
#### 3.4.2. Factor Preprocessing: Integrating Real Data
#### 3.4.3. Calculating Forward Returns
#### 3.4.4. Implementing Regression Analysis
#### 3.4.5. Implementing IC Analysis
#### 3.4.6. Implementing Layered Backtest
### 3.5. Differences and Connections Between the Three Methods

<more>

This chapter introduces the principles and implementation code for the regression method, IC method, and layered backtest method. Upon completion, you will be able to implement a simple factor analysis framework yourself, which is highly beneficial for understanding Alphalens.

</more>

---

## 4. Introduction to Alphalens
### 4.1. Slope Factor: Definition and Implementation
### 4.2. How to Calculate Factors and Collect Price Data for Alphalens
### 4.3. How Alphalens Handles Data Preprocessing
### 4.4. Factor Analysis and Report Generation
### 4.5. References

<more>

Alphalens highly abstracts the factor testing process, encapsulating the steps discussed in the previous two chapters into two functions, with extensive customization achieved through parameters. We will introduce the input data format required by Alphalens and how it uses parameters to control layering, missing value handling, and forward return calculation behaviors.

By the end of this chapter, you will master the most basic usage of Alphalens.

</more>

---

## 5. Alphalens Report Analysis
### 5.1. Return Analysis
#### 5.1.1. Alpha and Beta
#### 5.1.2. Layered Return Mean Chart
#### 5.1.3. Layered Return Violin Plot
#### 5.1.4. Factor-Weighted Long-Short Portfolio Cumulative Return Chart
#### 5.1.5. Layered Drivers of Returns
#### 5.1.6. Robustness of Long-Short Portfolio Returns
### 5.2. Event Study
### 5.3. IC Analysis
### 5.4. Turnover Analysis
### 5.5. References

<more>

Alphalens reports are not self-explanatory. For instance, it doesn't specify the units for Alpha and Beta, nor what a basis point (bps) unit represents; it certainly won't tell you what constitutes a "good" Alpha versus one that is "too good to be true." Some reports calculate metrics differently from what you might expect or have heard.

To accurately understand these reports, we employ three approaches: 1. Reading and debugging the source code. Through this, we discovered that bps stands for one ten-thousandth, defined in the `plotting.py` file. 2. Using synthetic data, which helps us understand what theoretical reports for the best factors should look like. 3. Searching through GitHub issues and the Quantopian community Archive documentation to find answers in other users' questions.

This is currently the only tutorial on the internet that thoroughly explains Alphalens.

</more>

---

## 6. Alphalens Advanced Techniques (1)
### 6.1. Excluding Functional Errors
#### 6.1.1. Outdated Alphalens Versions
#### 6.1.2. MaxLossExceedError
#### 6.1.3. Timezone Issues
### 6.2. Factor Monotonicity
### 6.3. Revisiting Price Data Collection
### 6.4. How to Analyze Factors Above Daily Frequency?
### 6.5. Deep Dive into Factor Layering
#### 6.5.1. Factors with Determined Trading Signals
#### 6.5.2. Discrete Value Factors

<more>

In this chapter, we introduce how to troubleshoot potential errors in Alphalens, both programmatic and logical. We also discuss how to conduct factor analysis at frequencies higher than daily. Many online tutorials don't even realize this presents a problem because they have never performed analysis at this level.

We also delve into Alphalens' layering mechanism, including how to handle cases where factor values are discrete.

</more>

---

## 7. Alphalens Advanced Techniques (2)
### 7.1. Refactoring the Factor Testing Process
### 7.2. Parameter Tuning: Saving Your Factors
#### 7.2.1. Correcting Factor Direction
#### 7.2.2. Filtering Non-Linear Layering
#### 7.2.3. Using Optimal Layering Methods
#### 7.2.4. Grid Search
### 7.3. Overfitting Detection Methods
#### 7.3.1. Out-of-Sample Testing
#### 7.3.2. Plotting Parameter Plateaus

<more>

Using Alphalens for factor testing is like an interview; you must expose the factor's potential as much as possible before evaluating its quality. This chapter introduces how to exhaustively挖掘 (mine) a factor's potential while avoiding the deception of overfitting. Besides out-of-sample testing, we will teach you how to assess the degree of overfitting by plotting parameter plateaus.

Visualization is crucial, especially when collaborating with others.

</more>

---

## 8. Alpha101 Factor Introduction
### 8.1. Data and Operators in Alpha101 Factors
### 8.2. Interpreting Alpha101 Factors
### 8.3. How to Implement Alpha101 Factors?

<more>

The Alpha101 factor library is a factor library published by World Quant in 2015. About 80% of the factors in it are officially used by World Quant (at the time of publication). We will introduce how to read the formulas of Alpha101 factors and implement their operators.

There are already good open-source libraries for implementing the entire factor library, which we will also introduce. This will become one of the treasures in your arsenal.

</more>

---

## 9. Talib Technical Factors
<!--Time-series factors are almost the only factor type in CTA and cryptocurrency trading. Meanwhile, they also hold a very important position in China A-shares-->

<!-- Percentage Price Oscillator https://github.com/stefan-jansen/machine-learning-for-trading/blob/main/24_alpha_factor_library/02_common_alpha_factors.ipynb-->
### 9.1. Ta-lib Function Grouping
### 9.2. Warm-up Periods (Unstable Periods)
<!--Stability isn't achieved just by removing NaNs. RSI stabilizes only after about 3 * win-->
### 9.3. Oscillation Indicators
#### 9.3.1. RSI
<!-- RSI Revamped Applications: Intelli RSI, Connor's RSI -->
#### 9.3.2. ADX - Average Directional Movement Index
#### 9.3.3. APO - Absolute Price Oscillator
#### 9.3.4. PPO - Percentage Price Oscillator
#### 9.3.5. Aroon Oscillator
#### 9.3.6. Money Flow Index
#### 9.3.7. Balance of Power
#### 9.3.8. William's R
#### 9.3.9. Stochastic Oscillator
### 9.4. Volume Indicators
#### 9.4.1. Chaikin A/D Line
#### 9.4.2. OBV
### 9.5. Volatility Indicators
#### 9.5.1. ATR and NATR - Average True Range
### 9.6. 8 Types of Moving Averages
### 9.7. Overlap Studies
#### 9.7.1. Bollinger Bands
#### 9.7.2. Hilbert Trendline and Sine Wave Indicator
#### 9.7.3. Parabolic SAR
### 9.8. Momentum Indicators
<more>

Most Alpha101 factors are volume-price factors. For understandable reasons, they do not repeat classic technical factors that have existed for years, but these factors still possess Alpha potential. In this section, we briefly introduce the talib library and explain the warm-up periods of technical indicators -- a potentially niche topic. The warm-up period is not just NaNs; for example, the warm-up period for RSI is quite long, being 3 times the `win` parameter.

There are many Talib technical indicators; we will introduce a few from each category, focusing on how to revamp these factors under new technical conditions. Taking RSI as an example, we will discuss intelli-RSI and Connor's RSI. This way, you not only gain new factors but also enhance your ability for innovative research.

Even experienced practitioners might be hearing about some of the factors we introduce for the first time, such as the Hilbert Sine Wave, which is one of the paid technical indicators sold on platforms like TradingView.

</more>


---

## 10. Other Volume-Price Factors
### 10.1. Low-Probability Events
<!-- Single extreme events, such as the Shanghai Composite's largest single-day drop or longest consecutive drop, are based on mean reversion after low-probability events -->
### 10.2. Max Drawdown
### 10.3. pct_rank
### 10.4. Volatility
### 10.5. Z-Score
### 10.6. Sharpe Ratio
### 10.7. First-Derivative Factors
### 10.8. Second-Derivative Factors
### 10.9. Frequency-Domain Factors
### 10.10. TSFresh Factor Library
### 10.11. Behavioral Finance Factors
#### 10.11.1. Integer Barrier Factors
#### 10.11.2. Breakout Failure Factors
<!-- Failure to break previous highs/lows -->
#### 10.11.3. Gap Factors
<!-- Gaps must be filled -->
#### 10.11.4. Regret Aversion Theory Factors
<!-- Intraday moving average impact, daily dense trading zone impact factors -->

<more>

Some low-probability factors are easy to construct. Perhaps because of this, they lack names and haven't found their way into academic papers. However, their Alpha is real. For example, the index's largest single-day drop or longest consecutive drop. The underlying principle is probability regression after extreme events.

In short, this is a show-off and innovative chapter. We will introduce second-derivative factors, frequency-domain factors, and behavioral finance factors. For instance, frequency-domain factors use Fast Fourier Transform (FFT) or wavelet transforms to identify the operational cycles of main market participants for prediction. While others are still using wavelets to smooth noise, we have already started using them to explore the patterns of main market participants!

</more>

---

## 11. Fundamental and Alternative Factors
### 11.1. Fama-French Five-Factor Model
#### 11.1.1. Market Factor
#### 11.1.2. Size Factor
<!--
Survivorship bias in the small-cap effect: "The Delisting Bias in CRSP's Nasdaq Data and Its Implications for the Size Effect" (by Tyler Shumway and Vincent Warther)

How Rolf Banz missed the low-volatility factor https://www.rolfbanz.ch/2012/09/low-beta-anomaly-some-early-evidence/

Thesis criticized by big shots: https://blog.quantide.cn/blog/2024/09/12/rolf-banz/
-->

#### 11.1.3. Value Factor
#### 11.1.4. Profitability Factor
#### 11.1.5. Investment Factor
### 11.2. Alternative Factors
<!-- Mining niche data https://pdf.dfcfw.com/pdf/H3_AP202204011556464427_1.pdf -->

#### 11.2.1. Social Media Sentiment Factors
<!-- Stock forum rankings, hot searches -->
#### 11.2.2. Web Traffic Factors
#### 11.2.3. Satellite Image Factors
<!-- This is where CNN networks come into play -->
#### 11.2.4. Patent Application Factors
<!-- Including patent approval, drug launch approval, etc., digging further back leads to mid-term clinical trial data -->
### 11.3. Technical Routes for Web Crawling
<!-- request > scrapy > selenium > playwright > extension -->

<more>

This part will focus more on concepts. Because alternative factors are either purchased or crawled, we don't want to dwell on crawling techniques.

</more>

---

## 12. Factor Mining Methods
<!-- New technology development, cross-border integration
Fashion cycles -- many factors are style factors. They may perform poorly for a period, then perform well later.
Entering different trading instruments. Not all factors have been seriously tested in all markets and trading instruments.
Entering different frequencies. Some factors don't work at the macro level but may be effective at high frequencies.
Factors are not everything

Borrowing terms from other fields: Information Fasting https://www.wenxuecity.com/news/2024/09/15/125777979.html
-->
### 12.1. Where Do New Factors Come From?
<!-- Transforming traditional technical indicators, papers, peers, roadshow exchanges -->
<!-- Where to find papers: Financial top journals -->
<!-- From your own or others' trading experiences -->
<!-- From limit-up or strong stocks. The factors introduced earlier are often inapplicable to very strong stocks due to their own technical limitations. You need to construct your own market indicators, such as the number of limit-up stocks or rising stocks -->

<!-- 

Innovation comes from the margins. Innovation comes from "mixing and matching." Russell chose how to explain mathematics with logic, a unique angle that made him a master. We have discussed that there is no such thing as a new technology; innovation comes from inheritance and synthesis. Many philosophy students think Russell's student Wittgenstein is more impressive, and some believe Frege's ideas were earlier than Russell's. Indeed, Russell was like a sponge, constantly absorbing knowledge from others, ready to change his ideas, and heavily influenced by Wittgenstein in his later years. However, Russell's characteristic was synthesis; his integration ability is stronger. Therefore, comprehensively speaking, we should acknowledge that Russell had a greater impact on philosophy.

Especially familiarize yourself with the mathematical logic pioneered by Russell.

Russell believed that our everyday language is chaotic and misleading; arguing for a long time often means people aren't talking about the same thing, which easily leads to bad philosophy. Logic can clarify and eliminate these misunderstandings, better handling abstract concepts.

Secondly, renowned psychologist Kahneman pointed out that our brains have System 1 and System 2. System 2 includes logical reasoning, but this is not something we are naturally familiar with, so it requires postnatal learning and exercise.

New Technical Indicators:

Awesome Oscillator https://www.ifcmarkets.hk/en/ntx-indicators/awesome-oscillator
Relative Volatility Index https://www.tradingview.com/support/solutions/43000594684-relative-volatility-index/ The RVI indicator first appeared in the 1993 issue of the magazine "Technical Analysis of Stocks & Commodities."
Relative Vigor Index: https://www.investopedia.com/terms/r/relative_vigor_index.asp
Average Daily Range: https://tw.tradingview.com/scripts/adr/
Williams Alligator: https://www.investopedia.com/articles/trading/072115/exploring-williams-alligator-indicator.asp
Connors RSI: 
Smoothed Moving Average: https://trendspider.com/learning-center/what-is-the-smoothed-moving-average-sma/
PVT: https://www.tradingview.com/support/solutions/43000502345-price-volume-trend-pvt/

```python https://github.com/TA-Lib/ta-lib-python/issues/622
def PVT(c, v):
    return np.cumsum(v[1:] * np.diff(c) / c[:-1])
```

-->
### 12.2. Online Resources
<!-- JoinQuant Factor Dashboard
[^yzkb]:  [JoinQuant Factor Dashboard](https://www.joinquant.com/view/factorlib/list). Here we can browse some common factor classifications and the performance of various factors in the current market environment.
-->
### 12.3. Factor Orthogonality Testing
<!-- https://github.com/stefan-jansen/machine-learning-for-trading/blob/f652d79ab2f137d75d554af2cc437a5512b16069/24_alpha_factor_library/04_factor_evaluation.ipynb -->
### 12.4. Discussing the Factor Zoo

<more>

This is also a chapter that discusses broad topics, but it is still full of干货 (substance). We will talk about methods for finding resources, such as how to find papers and data. By now, we have introduced hundreds of factors (excluding parameters and cycles), so we also need to see how many factors are truly independent. Therefore, we will introduce orthogonality testing methods.

</more>

---

## 13. Machine Learning Overview
### 13.1. Machine Learning Classification
#### 13.1.1. Machine Learning, Deep Learning, Reinforcement Learning
<!--https://www.showmeai.tech/article-detail/185-->
#### 13.1.2. Supervised, Unsupervised, and Reinforcement Learning
#### 13.1.3. Regression and Classification
### 13.2. Introduction to Machine Learning Models
### 13.3. Three Elements of Machine Learning
### 13.4. Basic Workflow of Machine Learning
<!-- https://scikit-learn.org/1.4/tutorial/basic/tutorial.html -->
### 13.5. Application Scenarios for Machine Learning
<!--
Linear Regression, Generalized Additive (Decision Trees), Ensemble Models (Gradient Boosting), Neural Networks, Reinforcement Learning, Genetic Algorithms, Bayesian Networks, Gaussian Processes
-->
<!-- The essence of regression vs. classification is a classic philosophical question: Is the world continuous or quantized? This question is classic because it is ubiquitous. When we use machine learning to solve a problem, we first encounter it: Is this a regression problem or a classification problem? -->

<!-- Understanding these concepts helps us understand the limitations of machine learning and why Artificial General Intelligence (AGI) is difficult. -->

<more>

A quick introduction to machine learning. Is the world continuous or quantized? This is an ancient philosophical question that also determines the basic models of machine learning -- regression or classification?

</more>

---

## 14. Core Concepts of Machine Learning
<!-- Linear Algebra, Gradient Optimization, Backpropagation, Activation Functions -->
### 14.1. Bias and Variance
### 14.2. Overfitting and Regularization Penalties
### 14.3. Loss Functions, Objective Functions, Metric Functions, and Distance Functions
#### 14.3.1. Loss Functions and Objective Functions
#### 14.3.2. Metric Functions
#### 14.3.3. Distance Functions

<!-- Tongyi Qianwen: Difference between loss functions and distance functions -->
<!-- https://stackoverflow.com/a/47306502/13395693 -->
<!-- Difference between Euclidean Distance and MSE -->

<more>

This course is an applied course and does not intend to involve too much theory. However, if you understand no principles at all, you can only copy examples without being able to extend them. Therefore, we decided to explain basic concepts closely related to the application layer -- only by understanding these concepts can we know how to choose objective functions, evaluate strategies, prevent overfitting, etc.

</more>

---

## 15. SKLearn General Toolkit
### 15.1. Data Preprocessing: preprocessing
<!-- Standardization tools, normalization tools, missing value handling, one-hot encoding -->
### 15.2. metrics
<!-- Some have been introduced earlier; here we introduce their position in sklearn and the parts not previously covered -->
### 15.3. Model Interpretation and Visualization
### 15.4. Built-in Datasets
<!-- load_iris, fetch_openml, make_classification-->
<!-- https://github.com/stefan-jansen/machine-learning-for-trading/tree/main/06_machine_learning_process -->
<more>

<!-- How to read confusion matrices -->
<!-- 1. https://www.v7labs.com/blog/confusion-matrix-guide -->
<!-- 2. Three-class confusion matrix: https://digitalcommons.aaru.edu.jo/cgi/viewcontent.cgi?article=1115&context=erjeng -->
sklearn is a very powerful machine learning library, winning people's love with its rich models and easy-to-use interface. In this chapter, we first introduce sklearn's general toolkit -- used to handle common problems encountered regardless of which algorithm model we adopt, such as data preprocessing, model evaluation, model interpretation and visualization, and built-in datasets.


</more>

---

## 16. Model Optimization
### 16.1. Optimization Overview
<!-- Objectives and Classification:
        First-order optimization: SGD, Momentum, AdaGrad
        Second-order optimization: Gradients and second-order derivatives
        Zero-order optimization methods: Particle Swarm, Genetic Algorithms GA
    -->
### 16.2. k-fold Cross Validation
### 16.3. Parameter Search
#### 16.3.1. Grid Search
#### 16.3.2. Random Search
#### 16.3.3. Bayesian Optimization

### 16.4. Rolling Forecasting
<!-- Used as an explanation tool for models, inspection & visualization -->
<!-- KNN prediction https://github.com/sammanthp007/Stock-Price-Prediction-Using-KNN-Algorithm -->
<more>

Machine learning in the quantitative field has its own特殊性 (special characteristics), such as in cross-validation, where we actually need to use a method called Rolling Forecasting (also known as Walk-Forward Optimization).

</more>

---

## 17. Clustering: Finding Pair Trading Targets
### 17.1. Overview of Clustering Algorithms
<!-- kmeans vs DBSCAN vs HDBSCAN -->
<!-- If there are too many features, reduce dimensions first -->
### 17.2. HDBSCAN Algorithm Principles
<!-- https://scikit-learn.org/stable/modules/clustering.html#hdbscan -->
### 17.3. Finding Pair Trading Targets
#### 17.3.1. HDBSCAN Example
<!-- https://towardsdatascience.com/dbscan-clustering-for-trading-4c48e5ebffc8 -->
#### 17.3.2. Result Evaluation
<!-- Plot stock price trends -->
<!-- ADF Test -->
#### 17.3.3. Pair Selection
<!-- https://github.com/quantrocket-codeload/quant-finance-lectures/blob/master/quant_finance_lectures/Lecture42-Introduction-to-Pairs-Trading.ipynb-->

<more>

In quantitative trading, Pair Trading is an important type of arbitrage strategy, with the prerequisite of finding two targets that can be paired. In this chapter, we will introduce the advanced HDBSCAN clustering method, demonstrate how to implement clustering through it, and then use related methods in statsmodels to perform cointegration pair tests to find targets that can be paired. Finally, we will demonstrate how to assemble all of this into a complete trading strategy.

This will be the first effective machine learning strategy you learn.

</more>

---

## 18. From Decision Trees to LightGBM
<!-- Decision Trees, Random Forests, GBDT, XGBoost\LightGBM -->
### 18.1. Decision Trees
<!-- https://github.com/edyoda/data-science-complete-tutorial/blob/master/6.%20Decision%20Tree.ipynb -->
#### 18.1.1. Decision Tree Classification <!-- https://scikit-learn.org/stable/modules/tree.html#classification -->
#### 18.1.2. Decision Tree Regression
### 18.2. LightGBM
<!-- https://github.com/datacamp/Machine-Learning-With-XGboost-live-training/blob/master/notebooks/Machine-Learning-with-XGBoost-solution.ipynb -->
#### 18.2.1. Familiarizing with Training Data
#### 18.2.2. Building the First Classifier
#### 18.2.3. Visualizing Feature Importance
#### 18.2.4. Viewing Model Trees
#### 18.2.5. Cross-Validation
#### 18.2.6. Tuning
<!-- We will explore the effects of parameters such as max depth, colsample_bytree, subsample, min_child_weight, gamma, alpha, learning_rate, etc., and use grid_search_cv and RandomizedSearchCV for hyperparameter tuning. -->

<!-- Comparison of LightGBM and XGBOOST https://www.showmeai.tech/article-detail/195 -->

<more>

Limited by the high noise in financial data, end-to-end trading strategies are not yet feasible; also limited by the size of labeled data, deep learning and other AI models are not suitable for constructing trading strategies. Among machine learning models, the best model at present is the Gradient Boosting Decision Tree (GBDT) model. Representative implementations are XGBoost and LightGBM.

Since LightGBM surpasses XGBoost in most tasks in terms of both speed and accuracy, our course will focus on introducing LightGBM.

This chapter will comprehensively introduce the LightGBM model and demonstrate through examples how to use it, how to inspect and visualize the generated models, how to perform cross-validation, and how to tune parameters.

</more>

---

## 19. Price Prediction Based on LightGBM Regression Model
### 19.1. Strategy Principles
<!-- 
Linear transformation between moving averages and prices
If the moving average is stable, prices will mean-revert to the moving average
-->
### 19.2. Strategy Implementation
### 19.3. Strategy Optimization Ideas
<!--
1. Use cost moving averages instead of MA for prediction
2. Under what circumstances are moving averages stable? What additional indicators should be added?
-->

<more>

Asset pricing is one of the core issues in quantitative research. If we can provide a reasonable pricing for assets, we can generate trading signals.

Pricing is a regression problem. Although it is difficult to implement end-to-end price prediction models, we have cleverly designed a regression model that can predict future prices (theoretically self-consistent).

We cannot guarantee that this model will always be effective, and there are many improvement plans we haven't had time to explore. However, starting from this point, you already have a leading advantage in building machine learning trading models.

</more>

---

## 20. Trading Strategy Based on LightGBM Classification Model
<!-- Top/Bottom Prediction Model -->
### 20.1. Strategy Implementation
#### 20.1.1. Top/Bottom Finding Algorithm
#### 20.1.2. Labeling Tools
##### 20.1.2.1. Basic Layout
##### 20.1.2.2. Initialization
##### 20.1.2.3. Component Updates
#### 20.1.3. Building the Model
##### 20.1.3.1. Model Base Class
##### 20.1.3.2. V2
##### 20.1.3.3. V3
### 20.2. Algorithm Optimization
#### 20.2.1. Sample Balancing
#### 20.2.2. Multi-Cycle and Micro Data
#### 20.2.3. Market Atmosphere
#### 20.2.4. Using ID as a Feature

<more>

In this chapter, we will build a trading model based on a LightGBM classification model. In other words, it is not responsible for predicting prices but tells you whether to buy or sell. After completing this chapter, you will surely agree that models should be built this way; the rest is just workload: you need to build the system, label data, construct features, and then train the model.

</more>

---

## 21. The Future New World
<!-- Reference Video: https://www.3blue1brown.com/lessons/mlp -->
### 21.1. How to Obtain Free Computing Power <!-- Determined by the amount of labeled data -->

<!-- [Predicting Chinese stock market using XGBoost multi-objective optimization with optimal weighting](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10936758/)
-->

<!-- Are we building a stock selection model or a trading model? Actually, we should build two models: the first is a buy model, which has both stock selection and timing capabilities; the second is a sell model, which has timing capabilities and is only responsible for judging when to sell.
XGBoost is good, but LightGBM may be superior in memory usage and training speed in some scenarios. This chapter will introduce how to use LightGBM. We will provide a complete example but won't delve into too many details. This is the kind of content you often see in other courses.
-->

### 21.2. CNN Price Prediction
#### 21.2.1. How to Provide Data for Training
#### 21.2.2. How to Construct Feature Data
#### 21.2.3. How to Define the Model
#### 21.2.4. Training
#### 21.2.5. Production Deployment
#### 21.2.6. CNN Principles and Performance Optimization
### 21.3. Transformer
<!-- CNNs have fault tolerance and errors in recognizing key points, which is different from facial recognition -->
### 21.4. Reinforcement Learning
### 21.5. Other Important Intelligent Algorithms
#### 21.5.1. Kalman Filter
#### 21.5.2. Genetic Algorithms

<more>

We previously discussed why deep learning is not yet suitable for building quantitative trading models. In the first part of this chapter, we will use a CNN price prediction example to illustrate why. After understanding these limitations, perhaps you can invent a novel model suitable for quantitative trading. This part doesn't teach you portable tools and experiences. However, if you are a research-oriented and innovative person, you will also find this content very valuable.

Reinforcement learning is a direction we are optimistic about, especially in commodity futures and cryptocurrency trading. We will introduce some introductory knowledge and learning resources.

There are two other important intelligent algorithms that are neither machine learning nor deep learning or reinforcement learning, but are indeed commonly used in quantitative finance: Kalman filters and genetic algorithms. However, this part has no code, leaving more exploration space for you.

</more>

</div>

<!-- Machine learning related https://github.com/aialgorithm/Blog -->
<!-- Machine learning metrics average https://stackoverflow.com/questions/52269187/facing-valueerror-target-is-multiclass-but-average-binary -->
<!-- confusion matrix: https://towardsdatascience.com/understanding-confusion-matrix-a9ad42dcfd62-->
<!--
Fourier and Wavelet Analysis: https://cseweb.ucsd.edu/~baden/Doc/wavelets/polikar_wavelets.pdf
-->

<!-- Rewrite the opening remarks of this course, reference Wenquan Luo: https://open.163.com/newview/movie/free?pid=SHK5ITQ33&mid=KHK5ITSBB -->
<hr>

<h2 id="declaration">Notes</h2>
<p>1. This syllabus is not a course textbook directory. For example, many chapters in the course have "Extended Reading" sections, which are not displayed here.</p>
<p>2. The course content also includes exercises, which are not displayed here.</p>
<p>3. The course content also includes supplementary materials, such as complete Alpha101 factor implementation code (from data acquisition, factor extraction, factor testing to backtesting) and other example codes, which are not displayed here.</p>

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

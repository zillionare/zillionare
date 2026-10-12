---
title: "Factor ML Course: Guide to Factor Analysis & ML Strategies"
date: 2024-08-28
slug: en/articles/course/factor-ml/intro
tags: [Factor Investing, Machine Learning, Quantitative Trading, Backtesting]
excerpt: "A professional guide for quants to master factor analysis, machine learning strategy construction, and backtesting using Alphalens, XGBoost, and LightGBM."
lang: en
translation_of: articles/course/factor-ml/intro
auto_translated: true
source_sha: 660366d6cfe94a27597c7ff0e9ef2c1a2008ccfe
---

# Introduction to Factor Analysis and Machine Learning Strategies

This course is designed for professional quantitative researchers, those transitioning into the field, or professionals from other disciplines who are determined to explore quantitative research with a rigorous and professional attitude.

Upon completing this course and mastering its content, you will possess proficient factor analysis skills, master leading methods for constructing machine learning strategies, and become a quantitative researcher with innovative research capabilities and a competitive advantage.

## 1. Course Objectives

After completing this course, you will acquire the following capabilities (or tools):

1. Master the Alphalens factor analysis framework and apply it in your work.
2. Learn how to read Alphalens analysis reports and determine factor validity based on these reports.
3. Understand how to use Alphalens to mine factor value.
4. Introduce six categories of 400+ factors, including over 350 independent factors such as Alpha101 (factors derived from the same algorithm with different parameters and timeframes count as one factor).
5. Master factor mining methodologies, enabling you to discover new factors and improve existing ones.
6. Acquire a Pair Trading neutral strategy, using machine learning models to identify paired assets.
7. Become proficient in the XGBoost model, taking away price prediction and trend trading models based on XGBoost. These will become indispensable tools in your work for a considerable period.

## 2. Prerequisites

Before taking this course, students must have a foundational understanding of Python programming, including:

1. **Python Basics and Common Libraries**: Including dates, strings, file I/O, lists, dictionaries, module imports, typing, etc.
2. **Statistics**: Requires basic university-level statistical knowledge and a preliminary understanding of fundamental concepts. Detailed explanations are provided in *Quantitative 24 Lessons*.
3. **Jupyter Notebook**: We provide *Notebook Introduction* and *Notebook Advanced Techniques* for your study.
4. **Numpy and Pandas**: Introductory knowledge is required. The course uses many advanced Numpy and Pandas techniques; lacking prior knowledge will increase the difficulty of reading example code (including listening to lectures). We recommend taking our free course, *Numpy and Pandas in Quantitative Trading*, concurrently. We will also cover some syntax during lectures, but it is not the focus.
5. **Machine Learning and Neural Networks**: A basic understanding of machine learning and neural networks is helpful to keep pace when we cover core ML theories.

If you do not meet the first two conditions, you may face significant difficulties. If you do not meet the latter three, you can still take the course but will need to invest extra time familiarizing yourself with these topics.

## 3. Course Content

The course content covers three major modules: factor mining, factor testing, and building machine learning models.

### 3.1. Factor Testing Methods

Only by mastering factor testing methods can we determine whether mined factors are effective. Therefore, factor testing is the starting point of this course, spanning from Chapter 2 to Chapter 7, totaling six chapters.

<div style='width:33%;float:left;padding: 0.5rem 1rem 0 0;text-align:center'>
<img src='https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/01/alphalens.jpg'>
<span style='font-size:0.6rem'>Alphalens Logo</span>
</div>

We will begin by introducing the principles of factor testing, manually implementing each step of the process; then, we will introduce the open-source factor analysis framework, Alphalens. We will not only explain how to use Alphalens but also focus on interpreting its reports, performing parameter tuning, and debugging. This section contains extensive industry experience and comparative examples of successes and failures, offering depth and novelty you won't find elsewhere online.

When you understand how to judge factor quality through reports and flexibly use Alphalens to reveal the relationship between factors and returns hidden in large datasets, you will truly grow into a factor analysis expert.

### 3.2. Factor Mining

Chapters 8 through 12 constitute the second part of the course.

Factor mining, or feature engineering, is a crucial component of building trading strategies and the most daily task for quantitative researchers. We will introduce Alpha 101 factors, Ta-lib and technical indicator factors, behavioral finance factors, fundamental factors, and alternative factors.

If mastering these factors is still insufficient, we will introduce factor mining methodologies in Chapter 12. You may have been attracted to us by our published articles on factor and strategy mining; here, we will impart all the resources and methodologies we have mastered.

<div style='width:50%;text-align:center;margin: 0 auto 1rem'>
<img src='https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/08/factor-nav.jpg'>
<span style='font-size:0.8em'>Various Factor Categories</span>
</div>

When introducing Alpha 101 factors, we focus on understanding their data formats and implementing the operators. This is the foundation for understanding Alpha 101; mastering these operators allows you to fully read and implement all Alpha 101 factors. We will then discuss several specific factors, teaching you how to read their complex expressions and understand the authors' logic and intent.

Regarding the implementation of Alpha 101 factors, since many open-source implementations already exist, we do not intend to reinvent the wheel. Instead, we introduce an open-source library we believe is the most complete and accurate, which you can use directly in our appendix. You can then incorporate it into your quantitative toolkit.

<div style='width:50%;text-align:center;margin: 0 auto 1rem'>
<img src='https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/08/better-sing-wave-indicator.jpg'>
<span style='font-size:0.6rem'>Hilbert Sine Wave</span>
</div>

In Chapter 9, we introduce the Ta-lib library and some technical indicators it implements, including moving averages, Overlap, Momentum, volume, and volatility indicators—about 20 in total. Some may be familiar, such as moving averages, while others, like the Hilbert Transform-based trend line and Sine Wave Indicator (as shown in [](#Hilbert Sine Wave)), may be less so. As with other chapters, we maintain sufficient research depth, covering topics such as the warm-up period and how to revitalize old technical indicators (using RSI as an example).

In Chapter 10, we introduce fundamental and alternative factors. Due to difficulties in data acquisition and quality issues, we will focus primarily on principles and may not provide code implementations for all.

In Chapter 11, we introduce factors that do not fit into other categories but remain important, such as low-probability event (Black Swan) factors. We introduce the concept of derivatives to present two effective first-order and second-order momentum factors. We also discuss constructing frequency-domain factors via time-frequency transformation and introduce some behavioral finance factors, a hot topic in current finance, particularly useful for short-term trading.

<div style='width:50%;text-align:center;margin: 0 auto 1rem'>
<img src='https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/08/fft-decomposite.jpg'>
<span style='font-size:0.6rem'>Extracting Frequency-Domain Factors via FFT</span>
</div>

### 3.3. Building Machine Learning-Based Trading Strategies

<!-- ![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/08/machine-learning.jpg?width=500){width="500"} -->

This part begins with a rapid introduction to core machine learning concepts (Chapter 14). We cover loss functions, objective functions, metric functions, distance functions, bias, variance, overfitting, and regularization penalties. These are application-oriented core concepts that we must deal with.

<!-- ![Machine Learning Basic Concepts](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/08/loss-objective-metrics.jpg?width=500) -->

!!! tip
    If you need to deeply understand machine learning and neural networks, or invent new network models and ML algorithms, you will need to supplement your knowledge with linear algebra, gradient optimization, backpropagation, and activation functions. However, for mastering this course and achieving proficient application of known algorithms with tuning and optimization, the concepts we introduce are sufficient.

<div style='width:33%;float:left;padding: 0.5rem 1rem 0 0;text-align:center'>
<img src='https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/08/sklearn-logo.png'>
<span style='font-size:0.6rem'></span>
</div>

The machine learning library chosen for this course is `sklearn`. `sklearn` is a powerful library, beloved for its rich models and easy-to-use interfaces. In Chapter 15, we introduce sklearn’s general toolkit—used to handle common issues regardless of the algorithm model adopted, such as data preprocessing, model evaluation, model interpretation and visualization, and built-in datasets.

<!-- ![Cross Validation](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/08/k-fold-cross-validation.png?width=500) -->
In Chapter 16, we introduce model optimization methods, a core skill for most people engaged in machine learning and AI, and a key to creating excellent machine learning trading models. We demonstrate how to use cross-validation, grid search (GridSearch), and random search (RandomizedSearch).

<!-- ![Rolling Forecasting](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/08/walk-forward-optimization.webp?width=500) -->

Machine learning in the quantitative field has its own特殊性 (special characteristics). For instance, in cross-validation, we actually use a method called Rolling Forecasting (also known as Walk-Forward Optimization). We will detail this method and its implementation in the latter part of Chapter 16.

Next, we introduce a clustering algorithm (Chapter 17). In quantitative trading, Pair Trading is an important arbitrage strategy, the prerequisite for which is identifying two assets that can be paired. This chapter introduces the advanced HDBSCAN clustering method, demonstrating how to implement clustering and then use correlation methods in `statsmodels` to perform cointegration pair tests to find pairable assets. Finally, we demonstrate how to assemble all this into a complete trading strategy.

In Chapter 18, we introduce XGBoost, a gradient boosting decision tree model. Due to the high noise in financial data and the difficulty in obtaining large amounts of effectively labeled data, gradient boosting decision trees remain the most widely applied and effective machine learning model in quantitative trading.

<div style='width:50%;text-align:center;margin: 0 auto 1rem'>
<img src='https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/08/scheme-of-xgbost-model.jpg'>
<span style='font-size:0.6rem'></span>
</div>

We start with decision tree models, introducing the optimization journey of XGBoost. Then, through a detailed example, we show how to use XGBoost to train a model and delve into its internals: we visualize the model’s important features and plot its model tree. Finally, we conclude by introducing cross-validation and optimization within XGBoost.

After extensive theoretical and practical study, we have completed all groundwork. It is now time to learn how to build XGBoost-based quantitative trading strategies. We will abandon the nearly ineffective end-to-end training approach (i.e., inputting prices to predict the next price) and instead adopt exploratory but more effective strategy examples.

In Chapter 19, we introduce how to build a price prediction model based on an XGBoost regression model. We cover strategy principles, implementation, and optimization. Although we build a price prediction model, it is by no means the end-to-end toy-type models you see online!

Another model is introduced in Chapter 20, a trading model built on an XGBoost classification model. In other words, it does not predict prices but tells you whether to buy or sell. In this chapter, we also introduce how to create annotation tools.

These two examples point to the fundamental method for using machine learning to build strategies under current conditions: because financial data is full of noise, we cannot expect end-to-end models to work. However, if we can clearly define the problem and identify effective features, machine learning becomes incredibly powerful! This will be your sharp weapon to outperform others in the market.

In Chapter 21, we delve deeper into questioning the XGBoost model. We introduce another implementation of gradient boosting decision trees: LightGBM, developed by Microsoft. It is generally believed that LightGBM outperforms XGBoost in performance, has lower memory usage, and has its own strengths and weaknesses compared to XGBoost in other metrics.

<div style='width:50%;text-align:center;margin: 0 auto 1rem'>
<img src='https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/08/lightGBM-by-Hossain-medium.jpeg'>
<span style='font-size:0.6rem'>LightGBM, by Hossain@medim</span>
</div>

We have introduced three very practical examples covering arbitrage trading, price prediction, and trading models. However, portfolio management is another important topic in asset management. How do we achieve portfolio management based on machine learning? We will also answer this question in this chapter.

Our course concludes with Lesson 22. We introduce the pioneer of deep learning—the CNN network—and its application in K-line pattern recognition. I do not believe CNN networks have any advantage in K-line pattern recognition, and I will explain why in detail. However, if you are interested in solving this problem, I will still introduce the general approach to using CNNs for K-line recognition.

Compared to deep learning, I am more optimistic about the application of reinforcement learning in trading. In cryptocurrencies and commodity futures, the key is not selecting investment assets but deciding trading timing, positions, and leverage based on market changes—a natural reinforcement learning problem. I will introduce the basic concepts of reinforcement learning and relevant learning resources.

Finally, there are two intelligent algorithms that do not fit into the aforementioned categories—whether machine learning, deep learning, or reinforcement learning—but remain very important: the Kalman Filter and Genetic Algorithms.

The full course syllabus can be viewed [here](https://blog.quantide.cn/articles/course/factor-ml/syllabus.html).

## 4. Course Structure

The course content consists of main text, exercises, and supplementary materials.

The main text focuses on application, covering only the core theories of machine learning necessary for practical application. Almost every chapter provides extensive reading materials and notes for students who wish to delve deeper into specific details or underlying systems. Students without time can skip these parts without affecting the learning outcome.

The course includes numerous exercises. The purpose of these exercises is:

1. To reinforce memory for programming techniques used in some examples that are common in quantitative research.
2. To address topics with open-ended or exploratory conclusions that are not suitable for formal lecture content.

We have carefully prepared a large number of exercises for this course. You should fully utilize them to consolidate and expand your knowledge and skills. Most exercises are auto-graded, allowing you to promptly assess your mastery of the material.

Video, textbook, and exercise content complement each other, equivalent to taking three courses in one!

This course covers only part of quantitative trading knowledge. To engage in independent trading or complete the full stack of quantitative work, we recommend supplementing your learning with [Quantitative 24 Lessons](https://blog.quantide.cn/articles/course/24lectures/intro/). The difference between this course and *Quantitative 24 Lessons* is that this course is more specialized, while *Quantitative 24 Lessons* is broader and more comprehensive.

!!! tip "Enroll Now!"
    Scan the QR code to enroll and lock in the lowest price!

    <img src="https://gcore.jsdelivr.net/gh/zillionare/images@main/images/hot/quantfans.png" style="width: 150px;position:relative;float:right"/>

    * Exclusive in-depth analysis of Alphalens reports, helping you master factor testing and optimization.
    * Over 400 independent factors, categorized and explained in depth; take away implementations for 350+ factors upon completion.
    * Three practical models establishing a future research framework: clustering algorithms for searching pair trading targets (core of neutral strategies), XGBoost-based asset pricing, and trend trading models.
    * Leading teaching methods: SBP (Slidev Based Presentation), INI (In-place Notebook Interaction), and an assignment system based on Nbgrader (used by UC Berkeley).



<!-- 在交易中使用 DSP 技术一点也不奇怪。比如，网格交易法的鼻祖 -- 香农是信息论的发明人，这是现代通讯技术、包括 DSP 的源头；香农的同事，kelly？，发明了 kelly rule, 在赌场大赚特赚 -->


<!--

全网独家精讲 Alphalens 分析报告，助你精通因子检验和调优。
超 400 个独立因子，分类精讲底层逻辑，学完带走 350+ 因子实现。
课程核心价值观：课程核心价值观：Learning without thought is labor lost. Know-How & Know-Why
三大实用模型，奠定未来研究框架：聚类算法搜索配对交易标的（中性策略核心）、基于 XGBoost 的资产定价、趋势交易模型。
领先的教学手段：SBP（Slidev Based Presentation）、INI（In-place Notebook Interaction）和基于 Nbgrader（UCBerkley 使用中）的作业系统。

-->

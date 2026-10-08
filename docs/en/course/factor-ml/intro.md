---
title: "Factor Analysis & ML Strategy: Course Guide"
date: 
slug: en/articles/course/factor-ml/intro
tags: [Factor Investing, Machine Learning, Quantitative Research, Alphalens]
excerpt: "A comprehensive guide to mastering factor analysis and machine learning for quantitative research. Covers Alphalens, XGBoost, and advanced strategy construction."
lang: en
translation_of: articles/course/factor-ml/intro
auto_translated: true
source_sha: 7fe8158da8455972c58990456b4db6ca2baa8e1a
---

# Introduction to Factor Analysis and Machine Learning Strategies

This course is designed for professional quantitative researchers, those transitioning into the field, or professionals from other disciplines who are committed to exploring quantitative research with a professional and rigorous attitude.

Upon completing this course and mastering its content, you will possess proficient factor analysis skills, master leading methods for constructing machine learning strategies, and become a quantitative researcher with innovative research capabilities and a competitive edge.

## 1. Course Objectives

After completing this course, you will acquire the following capabilities (or tools):

1. Master the Alphalens factor analysis framework and apply it in your work.
2. Know how to read Alphalens analysis reports and determine factor effectiveness based on these reports.
3. Understand how to use Alphalens to mine factor value.
4. Introduce six categories of 400+ factors, including 350+ independent factors from Alpha101 (factors with the same algorithm but different parameters and cycles count as one).
5. Master factor mining methodology, enabling you to mine new factors and improve existing ones.
6. Take away a Pair Trading neutral strategy, using machine learning models to identify paired assets.
7. Become proficient in the XGBoost model, taking home price prediction and trend trading models based on XGBoost. These will become essential tools in your work for some time.

## 2. Prerequisites

Before taking this course, students need to master the following Python programming basics:

1. Python basic syntax and common libraries, including time/date handling, strings, file I/O, lists, dictionaries, module imports, typing, etc.
2. Statistical knowledge. You should have foundational university-level statistics knowledge and a preliminary understanding of basic concepts, which are detailed in "Quantitative 24 Lectures."
3. Jupyter Notebook. We provide "Notebook Introduction" and "Advanced Notebook Techniques" for your study.
4. Numpy and Pandas. Foundational knowledge is required. The course uses many advanced Numpy and Pandas techniques; without prior mastery, reading example code (including lectures) will be difficult. We recommend taking our free course, "Numpy and Pandas in Quantitative Trading," concurrently. We will also explain some syntax during lectures, but it is not the focus.
5. A basic understanding of machine learning and neural networks. This will help you keep up when we explain core machine learning theories.

If you do not meet the first two conditions, you may face difficulties. If you do not meet the last three, you can still take the course, but you will need to spend extra time familiarizing yourself with these areas.

## 3. Course Content

The course covers three major modules: factor mining, factor testing, and building machine learning models.

### 3.1. Factor Testing Methods

Only by mastering factor testing methods can we determine if mined factors are effective. Therefore, factor testing is the starting point of this course, spanning from Chapter 2 to Chapter 7, totaling six chapters.

<div style='width:33%;float:left;padding: 0.5rem 1rem 0 0;text-align:center'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/01/alphalens.jpg'>
<span style='font-size:0.6rem'>Alphalens Logo</span>
</div>

We will start by introducing the principles of factor testing and manually implementing each step of the process; then, we will introduce the open-source factor analysis framework, Alphalens. We will not only cover how to use Alphalens but also focus on interpreting its reports, parameter tuning, and debugging. This section contains extensive industry experience, contrasting positive and negative examples, and offers depth and novelty you won't find elsewhere online.

When you understand how to judge factor quality through reports and flexibly use Alphalens to reveal the relationship between factors and returns hidden in massive data, you will truly grow into a factor analysis expert.

### 3.2. Factor Mining

Chapters 8 to 12 constitute the second part of the course.

Factor mining, or feature engineering, is a crucial step in building trading strategies and the most daily task for quantitative researchers. We will introduce Alpha 101 factors, Ta-lib and technical indicator factors, behavioral finance factors, fundamental factors, and alternative factors.

If mastering these factors is not enough, we will also introduce factor mining methodology in Chapter 12. You may have been attracted to us by our various articles on factor and strategy mining published online; here, we will teach you all the resources and methodologies we have mastered.

<div style='width:50%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/factor-nav.jpg'>
<span style='font-size:0.8em'>Various Factor Categories</span>
</div>

When introducing Alpha 101 factors, we focus on understanding their data formats and implementation operators. This is the foundation for understanding Alpha 101; mastering these operators allows you to fully read and implement all Alpha 101 factors. Then, we will introduce several specific factors, teaching you how to read their complex expressions and understand the authors' logic and intent.

Regarding the implementation of Alpha 101 factors, since many open-source implementations already exist, we do not intend to reinvent the wheel. Instead, we will introduce an open-source library we believe is the most complete and accurate, which you can use directly in our appendix. You can then add it to your quantitative arsenal.

<div style='width:50%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/better-sing-wave-indicator.jpg'>
<span style='font-size:0.6rem'>Hilbert Sine Wave</span>
</div>

In Chapter 9, we will introduce the Ta-lib library and some technical indicators it implements, such as Moving Averages, Overlap, Momentum, Volume, and Volatility indicators (about 20 in total). Some you may already be familiar with, like Moving Averages, while others may be less familiar, such as trendlines based on Hilbert Transform and the Sine Wave Indicator (as shown in [](#Hilbert Sine Wave)). Like other chapters, we will maintain sufficient research depth, covering topics like the warm-up period and how to revitalize old technical indicators (using RSI as an example).

In Chapter 10, we will introduce fundamental and alternative factors. Due to the difficulty and quality issues of data acquisition, we will focus on principles and may not provide code implementations for all.

In Chapter 11, we will introduce factors that do not fit into other categories but are still important, such as low-probability event (Black Swan) factors. We will introduce the concept of derivatives to present two effective first-order and second-order momentum factors, construct frequency-domain factors using time-frequency transformation, and introduce some behavioral finance factors, a hot concept in current finance that is very useful in short-term trading.

<div style='width:50%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/fft-decomposite.jpg'>
<span style='font-size:0.6rem'>Extracting Frequency-Domain Factors via FFT</span>
</div>

### 3.3. Building Machine Learning-Based Trading Strategies

<!-- ![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/machine-learning.jpg?width=500){width="500"} -->

This part begins with a rapid introduction to core machine learning concepts (Chapter 14). We will cover loss functions, objective functions, metric functions, distance functions, bias, variance, overfitting, and regularization penalties. These are applied-level concepts within machine learning that we must deal with.

<!-- ![Machine Learning Basic Concepts](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/loss-objective-metrics.jpg?width=500) -->

!!! tip
    If you need to deeply understand machine learning and neural networks, or invent new network models and algorithms, you will need to supplement your knowledge with linear algebra, gradient optimization, backpropagation, and activation functions. However, for mastering this course, achieving proficiency in known algorithm models and tuning, the concepts we introduce are sufficient.

<div style='width:33%;float:left;padding: 0.5rem 1rem 0 0;text-align:center'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/sklearn-logo.png'>
<span style='font-size:0.6rem'></span>
</div>

The machine learning library selected for this course is `sklearn`. `sklearn` is a powerful library, loved for its rich models and easy-to-use interface. In Chapter 15, we introduce `sklearn`'s general toolkit, which handles common issues regardless of the algorithm model used, such as data preprocessing, model evaluation, model interpretation and visualization, and built-in datasets.

<!-- ![Cross Validation](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/k-fold-cross-validation.png?width=500) -->
In Chapter 16, we will introduce model optimization methods, a core skill for most people engaged in machine learning and AI, and a key to creating excellent machine learning trading models. We will demonstrate how to use cross-validation, grid search (GridSearch), random search (RandomizedSearch), and other methods.

<!-- ![Rolling Forecasting](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/walk-forward-optimization.webp?width=500) -->

Machine learning in the quantitative field has its own特殊性 (special characteristics), particularly in cross-validation. We actually need to use a method called Rolling Forecasting (also known as Walk-Forward Optimization). We will detail this method and its implementation in the final part of Chapter 16.

Next, we introduce a clustering algorithm (Chapter 17). In quantitative trading, Pair Trading is an important class of arbitrage strategies, a prerequisite for which is identifying two assets that can be paired. This chapter introduces the advanced HDBSCAN clustering method, demonstrating how to perform clustering via it, and then using correlation methods in `statsmodels` to execute cointegration pair tests to find pairable assets. Finally, we will demonstrate how to assemble all this into a complete trading strategy.

In Chapter 18, we will introduce XGBoost, a gradient boosting decision tree model. Due to the high noise in financial data and the difficulty in obtaining large amounts of effectively labeled data, gradient boosting decision trees remain the most widely applied and effective machine learning model in quantitative trading.

<div style='width:50%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/scheme-of-xgbost-model.jpg'>
<span style='font-size:0.6rem'></span>
</div>

We will start with decision tree models, introducing the optimization journey of XGBoost. Then, through a detailed example, we will show how to use XGBoost to train a model and delve into its internals: we will visualize the model's important features and plot its model tree. Finally, we will conclude by introducing cross-validation and tuning in XGBoost.

After extensive theoretical and practical study, we have completed all the groundwork. It is now time to learn how to build XGBoost-based quantitative trading strategies. We will abandon the nearly ineffective end-to-end training approach (i.e., inputting prices to predict the next price) and instead use exploratory but more effective strategy examples.

In Chapter 19, we will introduce how to build a price prediction model based on an XGBoost regression model. We will cover the strategy principles, implementation, and optimization schemes. Although we are building a price prediction model, it is certainly not the end-to-end toy models you see online!

Another model will be introduced in Chapter 20, a trading model built on an XGBoost classification model. In other words, it does not predict prices but tells you whether to buy or sell. In this chapter, we will also introduce how to create labeling tools.

These two examples point to the fundamental method for using machine learning to build strategies under current conditions: since financial data is full of noise, we cannot expect end-to-end models to work. However, if we can clearly define the problem and identify effective features, machine learning becomes incredibly powerful! This will be your sharp weapon to defeat others in the market.

In Chapter 21, we will delve deeper into XGBoost models. We introduce another implementation of gradient boosting decision trees: LightGBM, developed by Microsoft. It is generally believed to outperform XGBoost in performance, with smaller memory usage, and each has its own advantages compared to XGBoost in other metrics.

<div style='width:50%;text-align:center;margin: 0 auto 1rem'>
<img src='https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/08/lightGBM-by-Hossain-medium.jpeg'>
<span style='font-size:0.6rem'>LightGBM, by Hossain@medim</span>
</div>

We have introduced three very practical examples covering arbitrage trading, price prediction, and trading models. However, portfolio management is another important topic in asset management. How do we achieve portfolio management based on machine learning? We will also answer this question in this chapter.

Our course concludes with Lesson 22. We will introduce the pioneer of deep learning—the CNN network—and its application in K-line pattern recognition. I do not believe CNN networks have any advantage in K-line pattern recognition, and I will explain why in detail. However, if you are interested in solving this problem, I will still introduce the general approach to using CNNs for K-line recognition.

Rather than deep learning, I am more optimistic about the application of reinforcement learning in trading. In cryptocurrencies and commodity futures, the key is not choosing investment varieties, but deciding trading timing, positions, and leverage based on market changes—a natural reinforcement learning problem. I will introduce the basic concepts of reinforcement learning and related learning resources.

Finally, there are two intelligent algorithms that do not fit into the above categories—whether machine learning, deep learning, or reinforcement learning—but are still very important: the Kalman Filter and the Genetic Algorithm.

The full course syllabus can be viewed [here](https://blog.quantide.cn/articles/course/factor-ml/syllabus.html).

## 4. Course Structure

The course content consists of main text, exercises, and supplementary materials.

The main text focuses on application, covering only the core theories of machine learning necessary for application. Almost every chapter provides extensive reading materials and notes for students who wish to delve deeper into specific details or underlying systems. Students without time can skip this part without affecting their learning outcomes.

The course includes numerous exercises. The purpose of these exercises is:

1. Some examples involve programming techniques commonly used in quantitative research, so they are included in exercises to reinforce memory.
2. Some topics have open-ended, exploratory conclusions and are not suitable for formal instruction.

We have carefully prepared a large number of exercises for this course. You should fully utilize these exercises to consolidate and expand your knowledge and skills. Most of these exercises are auto-graded, allowing you to promptly understand your mastery of the knowledge.

Videos, textbooks, and exercises complement each other, equivalent to taking three courses for the price of one!

This course only covers part of the knowledge in quantitative trading. If you wish to engage in independent trading or complete full-stack quantitative work, we recommend supplementing your learning with [Quantitative 24 Lectures](https://blog.quantide.cn/articles/course/24lectures/intro/). The difference between this course and "Quantitative 24 Lectures" is that this course is more specialized, while "Quantitative 24 Lectures" is broader and more comprehensive.

!!! tip "Enroll Now!"
    Scan the code to enroll and lock in the lowest price!

    <img src="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/quantfans.png" style="width: 150px;position:relative;float:right"/>

    * Exclusive in-depth analysis of Alphalens reports, helping you master factor testing and tuning.
    * Over 400 independent factors, categorized and deeply explained; take away 350+ factor implementations upon completion.
    * Three practical models laying the foundation for future research frameworks: clustering algorithms for searching pair trading targets (core of neutral strategies), asset pricing based on XGBoost, and trend trading models.
    * Leading teaching methods: SBP (Slidev Based Presentation), INI (In-place Notebook Interaction), and an assignment system based on Nbgrader (used by UCBerkley).

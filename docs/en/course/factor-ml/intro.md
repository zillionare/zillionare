---
title: "Factor Analysis & ML Strategy Course Guide"
date: 2024-08-28
slug: en/articles/course/factor-ml/intro
tags: [Factor Investing, Machine Learning, Quantitative Research, Model Optimization]
excerpt: "A comprehensive guide for quant researchers to master factor analysis, machine learning strategy construction, and advanced model optimization using Alphalens, XGBoost, and LightGBM."
lang: en
translation_of: articles/course/factor-ml/intro
auto_translated: true
source_sha: 5120b665a7fad7cb4a18cd26eb98e6391f5b6251
---

# Introduction to Factor Analysis and Machine Learning Strategies

This course is designed for professional quantitative researchers, those transitioning into the field, or professionals from other disciplines who are committed to exploring quantitative research with a rigorous and professional attitude.

Upon completing this course and mastering its content, you will possess proficient factor analysis skills, master leading machine learning strategy construction methods, and become a quantitative researcher with innovative research capabilities and a competitive advantage.

## 1. Course Objectives

After completing this course, you will acquire the following capabilities (or tools):

1. Master the Alphalens factor analysis framework and apply it in your work.
2. Understand how to read Alphalens analysis reports and determine factor effectiveness based on these reports.
3. Learn how to leverage Alphalens to uncover factor value.
4. Introduce six categories of 400+ factors, including over 350 independent factors such as Alpha101 (factors with the same algorithm but different parameters and periods count as one).
5. Master factor mining methodologies, enabling you to discover new factors and improve existing ones.
6. Acquire a Pair Trading neutral strategy, using machine learning models to identify paired assets.
7. Become proficient in the XGBoost model, taking home price prediction and trend trading models based on XGBoost. These will become invaluable tools in your work for a considerable period.

## 2. Prerequisites

Before taking this course, students need to master the following Python programming basics:

1. **Python Basics and Common Libraries**: Including time/date handling, strings, file I/O, lists, dictionaries, module imports, typing, etc.
2. **Statistical Knowledge**: You should have foundational university-level statistical knowledge and a preliminary understanding of basic concepts. This content is detailed in *Quantitative 24 Lessons*.
3. **Jupyter Notebook**: We provide *Notebook Basics* and *Advanced Notebook Techniques* for your study.
4. **Numpy and Pandas**: Introductory knowledge is required. The course uses many advanced Numpy and Pandas techniques; lacking prior mastery will increase the difficulty of reading example code (including lectures). We recommend taking our *Numpy and Pandas in Quantitative Trading* course (free) concurrently. We will also explain some syntax during lectures, but it is not the course focus.
5. **Understanding of Machine Learning and Neural Networks**: Having some familiarity with machine learning and neural networks will help you keep pace when we explain core machine learning theories.

If you do not meet the first two conditions, learning this course may be challenging. If you do not meet the last three conditions, you can still take the course, but you will need to spend extra time familiarizing yourself with these topics.

## 3. Course Content

The course content covers three major modules: factor mining, factor testing, and building machine learning models.

### 3.1. Factor Testing Methods

Only by mastering factor testing methods can we determine whether mined factors are effective. Therefore, factor testing is the starting point of this course, spanning from Chapter 2 to Chapter 7, totaling six chapters.

<div style='width:33%;float:left;padding: 0.5rem 1rem 0 0;text-align:center'>
<img src='https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/01/alphalens.jpg'>
<span style='font-size:0.6rem'>Alphalens Logo</span>
</div>

We will begin by introducing the principles of factor testing, manually implementing each step of the process; then introduce the open-source factor analysis framework, Alphalens. We will not only explain how to use Alphalens but also focus on how to interpret its reports, perform parameter tuning, and debug. This section contains extensive industry experience, contrasting positive and negative examples, and the depth and novelty of the content are unmatched by what you can currently find online.

When you understand how to judge the quality of factors through reports and how to flexibly use Alphalens to reveal the relationship between factors and returns hidden in large datasets, you will truly grow into a master of factor analysis.

### 3.2. Factor Mining

Chapters 8 to 12 constitute the second part of the course.

Factor mining, or feature engineering, is a crucial component in building trading strategies and is the most daily task for quantitative researchers. We will introduce Alpha 101 factors, Ta-lib and technical indicator factors, behavioral finance factors, fundamental factors, and alternative factors.

If mastering these factors is still not enough, we will introduce factor mining methodologies in Chapter 12. You may have been attracted to us by our various online articles on factor and strategy mining; here, we will teach you all the resources and methodologies we have mastered.

<div style='width:50%;text-align:center;margin: 0 auto 1rem'>
<img src='https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/08/factor-nav.jpg'>
<span style='font-size:0.8em'>Various Factor Categories</span>
</div>

When introducing Alpha 101 factors, we focus on understanding their data formats and implementing operators. This is the foundation for understanding Alpha 101. Mastering these operators allows you to fully read and implement all Alpha 101 factors. Then, we will introduce several of these factors, explaining how to read their complex expressions and understand the authors' thoughts and intentions.

Regarding the implementation of Alpha 101 factors, since many open-source implementations already exist, we do not intend to reinvent the wheel. Instead, we introduce an open-source library we believe is the most complete and accurate, which you can use directly in our appendix. You can then incorporate it into your quantitative arsenal.

<div style='width:50%;text-align:center;margin: 0 auto 1rem'>
<img src='https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/08/better-sing-wave-indicator.jpg'>
<span style='font-size:0.6rem'>Hilbert Sine Wave</span>
</div>

In Chapter 9, we introduce the Ta-lib library and some technical indicators it implements. We will cover approximately 20 indicators such as moving averages, Overlap, Momentum, volume, and volatility. Some you may already be familiar with, like moving averages, while others may be less familiar, such as trendlines based on Hilbert transforms and the Sine Wave Indicator (as shown in [](#Hilbert Sine Wave)). As with other chapters, we maintain sufficient research depth, covering topics like the warm-up period and how to revitalize old technical indicators (using RSI as an example).

In Chapter 10, we introduce fundamental factors and alternative factors. Due to the difficulty and quality issues of data acquisition, we will focus on principles and may not provide code implementations for all of them.

In Chapter 11, we introduce factors that do not fit into any specific category but are still important, such as low-probability event (Black Swan) factors. We will introduce the concept of derivatives to discuss two effective first-order and second-order momentum factors. We will also cover frequency-domain factors constructed via time-frequency transformation and some behavioral finance factors, which are hot topics in current finance and are very useful in short-term trading.

<div style='width:50%;text-align:center;margin: 0 auto 1rem'>
<img src='https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/08/fft-decomposite.jpg'>
<span style='font-size:0.6rem'>Extracting Frequency-Domain Factors via FFT</span>
</div>

### 3.3. Building Machine Learning-Based Trading Strategies

<!-- ![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/08/machine-learning.jpg?width=500){width="500"} -->

This section begins with a rapid introduction to core machine learning concepts (Chapter 14). We will cover loss functions, objective functions, metric functions, distance functions, bias, variance, overfitting, and regularization penalties. These are application-oriented core concepts in machine learning that we must deal with.

<!-- ![Machine Learning Basic Concepts](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/08/loss-objective-metrics.jpg?width=500) -->

!!! tip
    If you need to deeply understand machine learning and neural networks, or invent new network models and machine learning algorithms, you will need to supplement your knowledge with linear algebra, gradient optimization, backpropagation, and activation functions. However, for mastering this course and achieving proficiency in using known algorithm models and tuning parameters, understanding the concepts we introduce is sufficient.

<div style='width:33%;float:left;padding: 0.5rem 1rem 0 0;text-align:center'>
<img src='https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/08/sklearn-logo.png'>
<span style='font-size:0.6rem'></span>
</div>

The machine learning library chosen for this course is `sklearn`. `sklearn` is a very powerful machine learning library, beloved for its rich models and easy-to-use interfaces. In Chapter 15, we introduce sklearn's general toolkit—used to handle common issues regardless of the algorithm model adopted, such as data preprocessing, model evaluation, model interpretation and visualization, and built-in datasets.

<!-- ![Cross Validation](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/08/k-fold-cross-validation.png?width=500) -->
In Chapter 16, we introduce model optimization methods, which are core skills mastered by most people engaged in machine learning and AI, and one of the keys to creating an excellent machine learning trading model. We will demonstrate how to use cross-validation, grid search (GridSearch), random search (RandomizedSearch), and other methods.

<!-- ![Rolling Forecasting](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/08/walk-forward-optimization.webp?width=500) -->

Machine learning in the quantitative field has its own特殊性 (specific characteristics). For example, regarding cross-validation, we actually use a method called Rolling Forecasting (also known as Walk-Forward Optimization). We will detail this method and its implementation in the final part of Chapter 16.

Next, we introduce a clustering algorithm (Chapter 17). In quantitative trading, Pair Trading is an important type of arbitrage strategy, with the prerequisite of identifying two assets that can be paired. In this chapter, we introduce the advanced HDBSCAN clustering method, demonstrating how to implement clustering through it, and then use correlation methods in `statsmodels` to perform cointegration pair tests to find pairable assets. Finally, we will demonstrate how to assemble all this into a complete trading strategy.

In Chapter 18, we introduce XGBoost, a gradient boosting decision tree model. Due to the high noise characteristics of financial data and the difficulty in obtaining large amounts of effectively labeled data, gradient boosting decision tree models remain the most widely applied and effective machine learning models in the quantitative trading field.

<div style='width:50%;text-align:center;margin: 0 auto 1rem'>
<img src='https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/08/scheme-of-xgbost-model.jpg'>
<span style='font-size:0.6rem'></span>
</div>

We will start with decision tree models, introducing the optimization journey of XGBoost. Then, through a detailed example, we will show how to use XGBoost to train a model and delve into its internals: we will visualize the model's important features and plot its model tree. Finally, we conclude by introducing cross-validation and tuning in XGBoost.

After extensive theoretical and practical study, we have completed all the groundwork. It is now time to learn how to build XGBoost-based quantitative trading strategies. We will abandon the almost ineffective end-to-end training approach (i.e., inputting prices to predict the next price) and instead use exploratory but more effective strategy examples.

In Chapter 19, we introduce how to build a price prediction model based on an XGBoost regression model. We will cover the strategy principles, implementation, and optimization schemes. Although we are building a price prediction model, it is certainly not the end-to-end toy-type models you see online!

Another model is introduced in Chapter 20, a trading model built on an XGBoost classification model. In other words, it does not predict prices but tells you whether to buy or sell. In this chapter, we also introduce how to create annotation tools.

These two examples point to the fundamental method for using machine learning to build strategies under current conditions: since financial data is full of noise, we cannot expect end-to-end models to work. However, if we can clearly define the problem and identify effective features, machine learning becomes extremely powerful! This will be your sharp weapon to outperform others in the market.

In Chapter 21, we probe deeper into the XGBoost model. We introduce another implementation of gradient boosting decision trees: LightGBM, developed by Microsoft. It is generally believed to outperform XGBoost in performance, with smaller memory usage, and each has its own advantages in other metrics compared to XGBoost.

<div style='width:50%;text-align:center;margin: 0 auto 1rem'>
<img src='https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/08/lightGBM-by-Hossain-medium.jpeg'>
<span style='font-size:0.6rem'>LightGBM, by Hossain@medim</span>
</div>

We have introduced three very practical examples, covering arbitrage trading, price prediction, and trading models. However, portfolio management is another important topic in asset management. How do we achieve portfolio management based on machine learning? We will also answer this question in this chapter.

Our course concludes with Lesson 22. We introduce the pioneer of deep learning—the CNN network's application in K-line pattern recognition. I do not believe CNN networks have any advantage in K-line pattern recognition, and I will explain why in detail. However, if you are interested in solving this problem, I will still introduce the general approach of using CNNs for K-line recognition.

Compared to deep learning, I am more optimistic about the application of reinforcement learning in trading. In cryptocurrencies and commodity futures, the key is not selecting investment assets, but deciding trading timing, positions, and leverage based on market changes, which is inherently a reinforcement learning problem. I will introduce the basic concepts of reinforcement learning and related learning resources.

Finally, there are two intelligent algorithms that do not fit into any of the above categories—whether machine learning, deep learning, or reinforcement learning—but are still very important: the Kalman Filter and Genetic Algorithm.

The full course syllabus can be viewed [here](https://blog.quantide.cn/articles/course/factor-ml/syllabus.html).

## 4. Course Structure

The course content consists of three parts: main text, exercises, and supplementary materials.

The main course text focuses on applications, covering only the core theories of machine learning necessary for application. Almost every chapter provides extensive reading materials and notes for students who wish to delve deeper into specific details or underlying systems. Students without time can skip this part without affecting the learning outcome of the course.

The course includes a large number of exercises. The purpose of the exercises is:

1. Some examples involve programming techniques commonly used in quantitative research, so they are included in the exercises to reinforce memory.
2. Some topics have open-ended, exploratory conclusions and are not suitable for formal instruction.

We have carefully prepared a large number of exercises for this course. You should fully utilize these exercises to consolidate and expand your learned knowledge and skills. Most of these exercises are auto-graded, allowing you to timely understand your mastery of the knowledge.

Video, textbook, and exercise content complement each other, equivalent to taking three courses for the price of one!

This course only covers part of the knowledge in quantitative trading. If you wish to engage in independent trading or complete full-stack quantitative work, we recommend supplementing your learning with [Quantitative 24 Lessons](https://blog.quantide.cn/articles/course/24lectures/intro/). The difference between this course and *Quantitative 24 Lessons* is that this course's content is more specialized, while *Quantitative 24 Lessons* is broader and more comprehensive.

!!! tip "Enroll Now!"
    Scan the code to enroll and lock in the lowest price!

    <img src="https://gcore.jsdelivr.net/gh/zillionare/images@main/images/hot/quantfans.png" style="width: 150px;position:relative;float:right"/>

    * Exclusive in-depth analysis of Alphalens reports, helping you master factor testing and optimization.
    * Over 400 independent factors, categorized and explained in depth; take home 350+ factor implementations after completion.
    * Three practical models laying the foundation for future research frameworks: clustering algorithms for searching pair trading targets (core of neutral strategies), asset pricing based on XGBoost, and trend trading models.
    * Leading teaching methods: SBP (Slidev Based Presentation), INI (In-place Notebook Interaction), and an assignment system based on Nbgrader (used by UC Berkeley).

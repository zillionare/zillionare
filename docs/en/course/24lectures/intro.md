---
title: "24-Lecture Quant Trading Course: From Data to Live Trading"
date: 2023-05-13
slug: en/articles/course/24lectures/intro
tags: [Quantitative Trading, Factor Investing, Backtesting, Live Trading]
excerpt: "A comprehensive quantitative trading course for students, developers, and investors. Covers data, factor mining, backtesting, and live deployment with full A-share minute-level data."
lang: en
translation_of: articles/course/24lectures/intro
auto_translated: true
source_sha: e9486c5f2a6a09c01c17024fdb90989da0883062
---

## 1. Introduction

This introductory course on quantitative trading is designed for students, programmers, and institutional or individual investors currently engaged in discretionary trading who wish to enter the field of quantitative investing.

The curriculum covers the entire quantitative trading workflow: acquiring data, analyzing data distribution and correlations, discovering and extracting factors and patterns, writing strategies, conducting backtests, evaluating performance, and finally integrating strategies into live trading.

Upon completing this course, you will gain a comprehensive and systematic understanding of quantitative trading. You will be able to independently develop, debug, backtest, and execute quantitative strategies, as well as evaluate and improve your own approaches. You will also have the capability to reproduce academic papers, classic quantitative strategies, or implement your own strategic ideas. If you already have successful trading experience, this course will significantly enhance your edge.

The course materials include recorded videos, Jupyter Notebook scripts, and private tutoring/Q&A sessions. The text transcripts total approximately 400,000 bytes. The course provides a runnable experimental environment for these Notebooks, featuring:

* 192 CPU cores and 256GB RAM (shared among students)
* Jupyter Lab strategy development environment
* Full-minute-level data for all China A-shares from 2005 to 2023 (over 3 billion records, all commercial-grade licensed data)
* Backtesting services: Write strategies and run backtests immediately
* Simulated trading: Test your strategies in a simulated environment

This is a technically rigorous course. The content is structured sequentially, with progressive depth, internal consistency, and appropriate prioritization. It also includes unique insights rarely found elsewhere, such as:

!!! question
    1. The minimum price tick for China A-shares is 0.01 CNY. In many cases, we must round decimals to the hundredth place. For stocks under 2 CNY, rounding errors can result in a 0.5% loss. If such trades occur daily, the annualized loss could reach a staggering 247%! But is Python’s default rounding method correct in this context?
    2. Some argue that you must use forward-adjusted prices in backtests. Is this conclusion correct? How would you prove it?
    3. A Sharpe ratio of 2 in backtesting generally indicates a good strategy. However, in live trading, it may begin to draw down, and the Sharpe ratio may deteriorate. At what drawdown threshold can you definitively conclude that the strategy’s underlying assumptions no longer hold, necessitating the termination of live trading? (Note: Others may advise that once a quantitative program is running, it must be held through the drawdown.)
    4. If the Shanghai Composite Index drops by 4%, can you use statistical principles based on the past 1,000 trading days to infer the probability of further decline? In other words, is it appropriate to buy the dip at this point?

## 2. Course Syllabus and Structure

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/10/cheese-course-brochure-1.png)

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/10/cheese-course-brochure-2.png)

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/10/cheese-course-brochure-3.png)

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/10/cheese-course-brochure-4.png)

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/10/cheese-course-brochure-5.png)

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/10/cheese-course-brochure-6.png)

!!! tip
    For a more detailed course syllabus, see [here](/articles/course/24lectures/syllabus/)

## 3. Quantitative Knowledge Framework and Course Positioning

Quantitative trading is not only a nascent field in China but also, globally, has only been mainstream on Wall Street for the past two decades. Consequently, systematic frameworks for quantitative trading knowledge are rare.

Drawing from our own experience, combined with insights from similar domestic and international courses, peer exchanges, and reviews of mainstream quantitative frameworks, common libraries, and key academic papers, we have summarized the following learning roadmap:

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/10/cheese-course-roadmap.png)

The bottom layer of this roadmap represents the prerequisites for learning quantitative trading. For Python fundamentals, we recommend a concise English textbook that can be completed quickly and integrates well with our course. Technical tools can be learned hands-on during the course. Mathematical knowledge only needs to meet foundational levels, which we will review throughout the course.

The top layer allows for selective, in-depth study based on your specific goals after entering the industry.

## 4. Course Purchase and Registration Process

<div style="width:150px; position: relative;float:right">
    <img src="https://gcore.jsdelivr.net/gh/zillionare/images@main/images/hot/quantfans.png" style="width: 120px; display:inline-block"/>
    <p style="text-align:center;width:120px"> QuantFans </p>
</div>
<div>

* Contact quantfans_99 (QuantFans) for inquiries and obtain the purchase link
* Purchase the course through the platform
* Upon completion, the teaching assistant (QuantFans) will provision your course environment account and send you the login URL, username, and password
* The teaching assistant will create a course support group, inviting instructors and students
* Students begin learning. Questions can be asked via WeChat groups, with same-day Q&A for private classes and general group Q&A for other classes.
</div>

The course experimental environment is shown below:

 ![66%](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/hot/course/academy.jpg)

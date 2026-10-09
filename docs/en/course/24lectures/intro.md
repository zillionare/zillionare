---
title: "24-Lesson Quantitative Investing: From Data to Live Trading"
date: "2026-10-09"
slug: en/articles/course/24lectures/intro
tags: [Quantitative Investing, Backtesting, Factor Mining, Live Trading]
excerpt: "A comprehensive, hands-on course for quants and developers covering data pipelines, factor mining, backtesting, and live trading execution in China A-shares."
lang: en
translation_of: articles/course/24lectures/intro
auto_translated: true
source_sha: 3076e3921b18b04fc9042a7b061a842e17b34bce
---

## 1. Introduction

This course serves as an entry-level guide to quantitative trading, targeting students, programmers, and institutional or individual investors transitioning from discretionary trading to systematic strategies.

The curriculum covers the entire quantitative trading workflow: acquiring data, analyzing its distribution and correlations, discovering and extracting factors and patterns, writing strategies, conducting backtests, evaluating performance, and finally deploying strategies into live trading.

Upon completion, you will have a comprehensive and systematic understanding of quantitative trading. You will be able to independently develop, debug, backtest, and execute quantitative strategies, as well as evaluate and improve your own models. You will possess the capability to replicate academic papers, reproduce classic quantitative strategies, or implement novel trading ideas. If you already have successful discretionary trading experience, this course will significantly amplify your edge.

The course materials include pre-recorded videos, Jupyter Notebook scripts, and private tutoring/Q&A sessions. The written transcripts total approximately 400,000 characters. We provide learners with a ready-to-run experimental environment featuring:

* 192 CPU cores and 256GB RAM (shared among students)
* Jupyter Lab strategy development environment
* Full minute-level data for China A-shares from 2005 to 2023 (over 3 billion records, all commercial-grade licensed data)
* Backtesting services: write strategies and run backtests immediately
* Simulation trading: test your strategies in a simulated live environment

This is a rigorous, "hardcore" course. The content is structured sequentially, with progressive depth, internal consistency, and careful selection of topics. It includes unique insights rarely found elsewhere, such as:

!!! question
    1. The minimum price tick in China A-shares is 0.01 RMB. In many cases, we must round decimals to the hundredth place. For stocks under 2 RMB, rounding errors can incur a 0.5% loss. If such trades occur daily, the annualized loss could reach a staggering 247%! However, is Python’s built-in rounding method actually correct for this purpose?
    2. Some argue that backtests must use forward-adjusted prices. Is this conclusion valid? How would you prove it?
    3. If your strategy achieves a Sharpe ratio of 2 in backtesting, it is generally considered excellent. However, in live trading, it may begin to draw down, and the Sharpe ratio deteriorates. At what drawdown threshold can we conclusively determine that the strategy’s underlying assumptions have broken down, necessitating the cessation of live trading? (Note: others might tell you that once a quant program is running, you must hold through any drawdown.)
    4. If the Shanghai Composite Index drops by 4%, can you use statistical principles based on the past 1,000 trading days to infer the probability of further decline? In other words, is this an opportune moment to buy the dip?

## 2. Course Syllabus and Structure

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/10/cheese-course-brochure-1.png)

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/10/cheese-course-brochure-2.png)

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/10/cheese-course-brochure-3.png)

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/10/cheese-course-brochure-4.png)

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/10/cheese-course-brochure-5.png)

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/10/cheese-course-brochure-6.png)

!!! tip
    For a more detailed syllabus, see [here](articles/course/24lectures/intro.md)

## 3. Quantitative Knowledge Framework and Course Positioning

Quantitative trading is a relatively new phenomenon not only in China but also globally; it has only dominated Wall Street for the past 20 years or so. Consequently, systematic frameworks for understanding quantitative trading are scarce.

Based on our experience, combined with insights from domestic and international similar courses, peer exchanges, and reviews of mainstream quantitative frameworks, libraries, and key papers, we have summarized the following learning roadmap:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/10/cheese-course-roadmap.png)

The bottom layer of this roadmap represents the prerequisites for learning quantitative trading. For Python basics, we recommend a concise English textbook that can be completed quickly and integrates seamlessly with our course. Tooling skills can be acquired through hands-on practice during the course. Mathematical knowledge only needs to meet foundational levels; we will guide you through reviewing relevant content within the course.

The top layer represents advanced topics that you can selectively pursue in depth after entering the industry, based on your specific goals.

## 4. Enrollment Process

* Contact quantfans_99 (Kuan Fen) for inquiries and obtain the purchase link.
* Purchase the course via the platform.
* On the day of purchase, the teaching assistant (Kuan Fen) will activate your course environment account and send you the login URL, username, and password.
* The teaching assistant will create a course support group and invite instructors and students.
* Students begin learning. Questions can be asked via WeChat groups, with same-day Q&A for private tutoring classes and group-based Q&A for other classes.
* Course videos remain accessible permanently. Server resource allocation depends on the selected package.

The course experimental environment is depicted below:

 ![66%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/course/academy.jpg)

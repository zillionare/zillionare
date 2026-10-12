---
title: "24-Lecture Quant Trading Course: From Data to Live Trading"
date: 2023-05-13
slug: en/articles/course/24lectures/intro
tags: [Quantitative Trading, Factor Investing, Backtesting, Live Trading]
excerpt: "A comprehensive, hands-on quantitative trading course for students, developers, and investors. Covers data pipelines, factor mining, backtesting, and live deployment with real A-share data."
lang: en
translation_of: articles/course/24lectures/intro
auto_translated: true
source_sha: f7549c93d5f2bdd4be1d1c8d5c87c2db146d4ade
---

## 1. Introduction

This course serves as an entry-level guide to quantitative trading, designed for students, programmers, and institutional or individual investors transitioning from discretionary trading.

The curriculum covers the entire quantitative trading workflow: data acquisition, distribution and correlation analysis, factor and pattern discovery, strategy coding, backtesting, evaluation, and finally, live deployment.

Upon completing this course, you will gain a comprehensive and systematic understanding of quantitative trading. You will be able to independently develop, debug, backtest, and execute quantitative strategies, as well as evaluate and improve your own models. You will have the capability to replicate academic papers, classic quantitative strategies, or implement your own trading ideas. If you already have successful discretionary trading experience, this course will significantly amplify your edge.

The course materials include recorded video lectures, Jupyter Notebook scripts, and private tutoring/Q&A sessions. The text transcripts amount to approximately 400,000 bytes. The course provides a ready-to-run experimental environment for these Notebooks, featuring:

* 192 CPU cores and 256GB RAM (shared among students)
* Jupyter Lab strategy development environment
* Full minute-level data for China A-shares from 2005 to 2023 (over 3 billion records, all commercial-grade licensed data)
* Backtesting services: Write and run backtests immediately
* Simulated trading: Test your strategies in a simulated market environment

This is a technically rigorous course. The content is structured sequentially, progressively building complexity, with careful attention to coherence and prioritization. It also covers niche topics rarely found elsewhere, such as:

!!! question
    1. The minimum price tick in China A-shares is 0.01 RMB. In many cases, we must round decimals to the hundredth place. For stocks priced below 2 RMB, rounding errors can result in a 0.5% loss. If such trades occur daily, the annualized loss could reach a staggering 247%! However, is Python’s built-in rounding method actually correct?
    2. Some argue that adjusted prices (forward-adjusted) should be used in backtests. Is this conclusion correct? How would you prove it?
    3. A Sharpe ratio of 2 in backtesting generally indicates a strong strategy. However, in live trading, it begins to draw down, and the Sharpe ratio deteriorates. At what drawdown threshold should you conclude that the strategy’s fundamental assumptions no longer hold and must halt live trading? (Note: Others may advise that once a quantitative program is running, it must be held through all volatility.)
    4. If the Shanghai Composite Index drops 4%, can you use the past 1,000 trading days of data to statistically infer the probability of further decline? In other words, is it now a valid opportunity to buy the dip?

## 2. Course Syllabus and Structure

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/10/cheese-course-brochure-1.png)

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/10/cheese-course-brochure-2.png)

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/10/cheese-course-brochure-3.png)

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/10/cheese-course-brochure-4.png)

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/10/cheese-course-brochure-5.png)

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/10/cheese-course-brochure-6.png)

!!! tip
    For a more detailed syllabus, see [here](articles/course/24lectures/intro.md)

## 3. Quantitative Knowledge Framework and Course Positioning

Quantitative trading is a relatively new phenomenon not only in China but also globally; it has only dominated Wall Street for the past 20+ years. Consequently, systematic frameworks for quantitative trading knowledge are scarce.

Based on our experience, combined with insights from domestic and international similar courses, peer exchanges, and reviews of mainstream quantitative frameworks, libraries, and key papers, we have summarized the following learning roadmap:

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/10/cheese-course-roadmap.png)

In this roadmap, the bottom layer represents prerequisites for learning quantitative finance. For Python fundamentals, we recommend a concise English textbook that can be completed quickly and integrates seamlessly with our course. Tooling skills can be learned hands-on during the course. Mathematical knowledge only needs to meet this baseline; we will review relevant content throughout the course.

The top layer represents advanced topics you can selectively pursue after entering the industry, based on your specific goals.

## 4. Registration Process

* Contact `quantfans_99` (Kuanfen) for inquiries and obtain the purchase link.
* Purchase the course via the platform.
* On the day of purchase, the teaching assistant (Kuanfen) will activate your course environment account and send you the login URL, username, and password.
* The teaching assistant will create a course support group, inviting instructors and students.
* Students begin learning. Questions are addressed via WeChat groups, with same-day Q&A for private classes and group-based Q&A for other cohorts.
* Video lectures remain accessible permanently. Server resources depend on the selected package.

The course experimental environment is shown below:

 ![66%](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/hot/course/academy.jpg)

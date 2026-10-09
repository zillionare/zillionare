---
title: "2025 Quant Investing Course: Timeline, Profitability, and Tech Stack"
date: 2024-01-04
slug: en/articles/course/24lectures/faq
tags: [Quantitative Investing, Backtesting, Factor Mining, Live Trading]
excerpt: "A 30-hour, 24-chapter course with live server access, 4B+ commercial data, and minute-level backtesting. Ideal for Python/math beginners. Learn how to bridge strategy ideas to live trading with professional tools."
lang: en
translation_of: articles/course/24lectures/faq
auto_translated: true
source_sha: 7980de471a3674c7054bf078178b66f6f84a5cbe
---

## Enrollment Process and Learning Environment

!!! abstract "How is the course structured?"
    The course is delivered via videos, Jupyter notebooks, and Q&A sessions. Videos are hosted on Lizhi Weike, and notebooks are hosted on our dedicated servers.<br><br>
    After purchase, add the WeChat account **quantfans_99** to activate your course server account and begin learning.

!!! abstract "How long does it take to complete?"
    The course comprises 24 chapters, totaling approximately 400,000 bytes of text, with video content (edited and accelerated at 1.2x) lasting about 30 hours. We recommend completing it within one month, though this depends on your background and available time.<br><br>
    Video content is available for free indefinitely. The dedicated course server is accessible for six months; after that, you can still log in for two years but will be moved to public servers.<br><br>
    The course server is for learning purposes only and cannot be used as a general-purpose cloud server.

!!! abstract "Who is this course for / What are the prerequisites?"
    Anyone with **basic Python programming knowledge** and **university-level mathematics** can enroll. For specific assessments, contact **quantfans_99** to evaluate if you meet the entry requirements.<br><br>
    If you have some programming experience and are currently learning Python, you may enroll early; instructors can provide free tutoring.

!!! abstract "Do you provide a learning environment?"
    We provide a server cluster with 192 CPU cores and 256GB of RAM for students. By logging in via a browser, you can learn online and run our example code. In this environment, we have purchased over 4 billion rows of commercial data (measured as a time-series database; sponsored by JoinQuant since 2024). The subscription cost for this data alone exceeds 20,000 RMB.

!!! abstract "What are the advantages of your learning environment? Can I build my own?"
    The primary advantage is our integrated backtesting engine (not based on backtrader) and commercial data. Our backtesting executes trades on minute-level bars, automatically implementing T+1 restrictions and price limits, thereby most accurately replicating real trading conditions. The data volume is massive and difficult to replicate. Therefore, building your own environment would require purchasing data to truly replicate trading conditions. **Strategy optimization is only meaningful when based on real data.**

!!! abstract "I want to learn more about the course"
    We offer a preview environment containing partial course materials (videos, notebooks, and exercises). Add the teaching assistant on WeChat at **quantfans_99** to obtain the link.

## Career Planning Questions

!!! tip "Who is taking this course?"
    According to incomplete statistics (not all students are willing to share their backgrounds), more than 2 PhDs from Ivy League universities and nearly 10 fund managers (including private equity heads) are taking this course. One private equity firm has purchased our course for its employees and interns. Other students include professionals from Hong Kong investment banks, private equity staff, engineers from major internet companies, and university students.

!!! tip "Why learn quantitative trading?"
    Financial literacy is key to generating passive income. Learning quantitative trading allows you to stop working for money and instead, let money work for you!

!!! tip "Will I make money after completing this course?"
    Yes and No. This is a comprehensive course focused on solving the problem of how to programatically and scientifically implement a strategy if you already have one. Upon completion, if you are an experienced trader, you will be able to use the methods taught in this course to reorganize your trading experience, filtering out noise to solidify effective experiences into code. This helps avoid emotional volatility, limitations in human computational capacity, and the inability to analyze the full market panorama. If you lack trading experience, you will master scientific quantitative theories and research methods, gaining the key to unlock the strategy vault.<br><br>
    In short, whether comparing yourself to your past self or to other traders, you will make significant progress. However, profitability depends not only on your improved skills but also on market conditions. If the market is in a downtrend and shorting is not allowed, making money will be difficult.

!!! tip "Do you have connections with headhunters to help with job recommendations?"
    Absolutely! Our account [Quant Fans](https://www.xiaohongshu.com/user/profile/5ba12feef7e8b9437f3aca0c) is the #1 account in the quantitative sector on Xiaohongshu (Little Red Book), and headhunting firms actively collaborate with us.

## Quantitative Framework Questions

!!! tip "Your course introduces backtrader in detail. Why also introduce Daifuweng's backtesting features?"
    backtrader has several significant limitations:
    1. It cannot connect to live trading in China A-shares. You must develop your own market data reception and live trading interfaces to deploy strategies live.
   
    2. backtrader does not provide dynamic forward adjustment (forward-adjusted prices). However, this is the only correct adjustment mechanism for accurate backtesting.

    3. While backtrader theoretically supports minute-level matching, data copying issues make it impractical. Matching on daily bars leads to false executions. For example, if a stock’s lowest price during the day is 10.2 RMB, and you place a buy order for 10,000 lots at 10.3 RMB, backtrader might execute the full trade. However, in reality, only one lot might have been traded at 10.3 RMB or below. Thus, the maximum tradable volume should be one lot, but backtrader limits execution by the full day’s volume, allowing false trades. Minute-level fitting largely avoids these false executions.

    4. backtrader is unaware of China A-share trading rules, so it does not enforce T+1 selling restrictions or price limits. This causes significant discrepancies between backtest results and live trading performance.

!!! tip "What are the advantages of the Daifuweng Quantitative Framework?"
    1. Excellent backtesting and strategy systems. Deploying strategies live requires no code modifications; simply change the backtest server address to the live server address. Avoiding code changes reduces errors. Additionally, dynamic forward adjustment and minute-data matching are leading advantages.

    2. Massive data processing capabilities. We were among the first domestic developers to use time-series databases for storing market data.

    3. High-quality code and documentation. Documentation quality is indeed crucial.

    4. Provides many algorithms and common quantitative trading functions. For example, our calendar calculation library, plotting library, and pattern recognition features are exclusive.

!!! tip "Can I use your Daifuweng Quantitative Software after completing the course?"
    Yes, this is one of our advantages. After completing the course, you can use our quantitative software for local deployment and start trading immediately.<br><br>
    Daifuweng Quantitative Software 2.0 is open-source, but we only provide installation packages and guidance to students. Deploying 2.0 requires purchasing JoinQuant data.

!!! tip "What is the future roadmap for Daifuweng Quantitative Software?"
    We are developing version 3.0, expected to launch before the end of 2025. The goal of this version is to allow more people to build their quantitative research environments at lower costs. Therefore, this version will use ClickHouse as the database to provide better performance with lower hardware requirements. For live trading interfaces, we will use QMT, enabling access to live trading with low capital thresholds. Since previous market data sources were unstable, we are still seeking new low-cost (even free) data sources. This version will no longer be open-source; it will be provided exclusively to students to offer them greater value.

## Other Questions

!!! tip "I have a GPU. Can I use it in quantitative trading?"
    If you start directly from price data, end-to-end AI techniques are not yet mature and may never be. Price data contains significant noise, or rather, it is a many-to-many mapping, making effective learning difficult.<br><br>
    Currently, the most mature approach combining quantitative strategies with AI involves manually extracting factors and using machine learning, particularly algorithms like XGBoost/LightGBM, for factor combination. XGBoost/LightGBM can partially utilize GPUs, but using a GPU is not mandatory. Especially since LightGBM’s training speed is already very fast.

!!! tip "How do I apply for quantitative trading permissions? What are the thresholds?"
    Generally, new accounts can simultaneously apply for quantitative trading permissions. Consult with **quantfans_99** to help you find brokers with the lowest thresholds and optimal fees.

!!! tip "Can you introduce the instructor?"
    <div style="width:150px; position: relative;float:right">
        <img src="https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/me.png" style="width: 120px; display:inline-block"/>
        <p style="text-align:center;width:120px"> Aaron </p>
    </div>

    -   Senior Software R&D Manager at IBM/Oracle

    -   Vice President of Dolphin Browser (backed by Sequoia Capital)

    -   Founder of Kuangti Quantitative

    -   Initiator of the Zillionare open-source quantitative framework

    -   Author of *Python Efficient Programming Practice Guide* (published by China Machine Press).

---
title: "2025 Quant Investing Course: FAQ on Learning Time and Profitability"
date: 2024-01-04
slug: en/articles/course/24lectures/faq
tags: [Quantitative Investing, Backtesting, Factor Mining, Live Trading]
excerpt: "A 24-chapter, 30-hour quant course with pre-built servers, 4B+ data points, and minute-level backtesting. Requires basic Python/math. Learn to deploy strategies live with minimal friction."
lang: en
translation_of: articles/course/24lectures/faq
auto_translated: true
source_sha: 55f93fdf1913a488bc46efeb80cdf16d815812d7
---

## Enrollment Process and Learning Environment

!!! abstract "How do I take this course?"
    The course is delivered via videos, Jupyter notebooks, and Q&A sessions. Videos are hosted on Lizhi Microclass, while notebooks are hosted on our provided servers.<br><br>
    After purchase, add our WeChat account (quantfans_99) to activate your course server account and begin learning.

!!! abstract "How long does it take to complete?"
    The course comprises 24 chapters, totaling approximately 400,000 bytes of content, with video duration (edited and accelerated at 1.2x) of about 30 hours. We recommend completing it within one month, though this depends on your background and available time.<br><br>
    Course videos are available for free indefinitely. The dedicated course server is usable for six months; thereafter, you can log in for two more years but will be migrated to public servers.<br><br>
    The course server is for learning purposes only and cannot be used as a general-purpose cloud server.

!!! abstract "Who is this course for / What are the prerequisites?"
    Anyone with **basic Python programming knowledge** and **university-level mathematics** can enroll. For specific assessments, contact quantfans_99 on WeChat to evaluate if you meet the entry requirements.<br><br>
    If you have some programming experience and are currently learning Python, you may enroll first; instructors can provide free tutoring.

!!! abstract "Do you provide a learning environment?"
    We provide a server cluster with 192 CPU cores and 256GB of RAM for students. By logging in via a browser, you can learn online and run our example code. In this environment, we have purchased over 4 billion records of commercial data (measured by time-series database standards; sponsored by JoinQuant since 2024). The subscription fee for this data alone exceeds 20,000 RMB.

!!! abstract "What are the advantages of your learning environment? Can I set up my own?"
    The biggest advantage is our built-in backtesting functionality (not based on backtrader) and commercial data. Our backtesting executes trades on a minute-by-minute basis, automatically enforcing T+1 settlement and price limit rules, thereby most accurately replicating live trading conditions. The data volume is immense and difficult to replicate. Therefore, if you set up your own environment, you would need to purchase data to realistically simulate trading. **Only with real data does strategy optimization make sense.**

!!! abstract "I want to know more about the course"
    We offer a preview environment containing partial course materials (videos, notebooks, and exercises). You can add the teaching assistant on WeChat (quantfans_99) to obtain the link.

## Career Planning Questions

!!! tip "Who is taking this course?"
    According to incomplete statistics (not all students are willing to share their backgrounds), more than two PhDs from Ivy League universities and nearly ten fund managers (including private equity heads) are taking this course. One private equity firm has purchased our course for its employees and interns. Other students include professionals from Hong Kong investment banks, private equity staff, engineers from major internet companies, and university students.

!!! tip "Why learn quantitative trading?"
    Only by mastering financial management can you achieve passive income. Learn quantitative trading so that money works for you, rather than you working for money!

!!! tip "Will I make money after completing this course?"
    Yes, and no. This is a comprehensive course focused on solving the problem of how to program and scientifically validate strategies if you already have a strategic idea. Upon completion, if you are an experienced trader, you will be able to use the methods taught in this course to reorganize your trading experience, filtering out noise and solidifying effective experiences into code. This helps avoid emotional fluctuations, limitations in human computational capacity, and the inability to analyze the full market panorama. If you lack trading experience, you will still master scientific quantitative theories and research methods, gaining the key to unlocking the strategy vault.<br><br>
    In short, whether comparing yourself to your past self or to other traders, you will see significant progress. However, profitability depends not only on your improved skills but also on market conditions. If the market is in a downtrend and shorting is not allowed, making money will be difficult.

!!! tip "Do you have recruiters who can help recommend jobs?"
    Absolutely! Our account [Quant Fans](https://www.xiaohongshu.com/user/profile/5ba12feef7e8b9437f3aca0c) is ranked #1 in the quantitative sector on Xiaohongshu (Little Red Book), and recruitment agencies actively collaborate with us.

## Quantitative Framework Questions

!!! tip "Your course details backtrader. Why introduce Daifangwang’s backtesting features?"
    backtrader has several significant shortcomings:
    1. It cannot connect to live trading in China A-shares. You must develop your own market data reception and live trading interfaces to deploy strategies live.
   
    2. backtrader does not support dynamic forward adjustment (forward-adjusted prices). However, this is the only correct adjustment mechanism.

    3. Theoretically, backtrader can execute trades on 1-minute bars, but due to data copying issues, it is practically impossible. Executing on daily bars leads to false executions. For example, if the lowest price of a target on a given day drops to 10.2 RMB, and you place a buy order for 10,000 lots at 10.3 RMB, backtrader will execute the trade. However, in reality, only one lot might have been traded at 10.3 RMB or below that day. Thus, the maximum tradable volume should be one lot, but backtrader limits execution by the total daily volume, allowing the trade. Minute-by-minute fitting largely avoids such false executions.

    4. backtrader is unaware of China A-share trading rules, so it does not enforce T+1 sell restrictions or price limits. This causes a large discrepancy between backtest and live performance.

!!! tip "What are the advantages of the Daifangwang Quantitative Framework?"
    1. Excellent backtesting and strategy systems. Deploying strategies to live trading requires no code modification; simply change the backtest server address to the live server address. Avoiding code changes reduces errors. Additionally, dynamic forward adjustment and minute-data execution are leading advantages.

    2. Massive data processing capabilities. We were among the first domestic developers to use time-series databases to store market data.

    3. Excellent code and documentation quality. Documentation quality is indeed crucial.

    4. Provides many algorithms and common functions for quantitative trading. For example, our calendar calculation library, plotting library, and pattern recognition features are exclusive functions.

!!! tip "Can I use your Daifangwang Quantitative Software after completing the course?"
    Yes, this is one of our advantages. After completing the course, you can use our quantitative software for local deployment and start trading immediately.<br><br>
    Daifangwang Quantitative Software 2.0 is open-source, but we only provide installation packages and guidance to students. Deploying 2.0 requires purchasing JoinQuant data.

!!! tip "What is the future roadmap for Daifangwang Quantitative Software?"
    We are developing version 3.0, expected to launch before the end of 2025. The goal of this version is to allow more people to build their quantitative research environments at a lower cost. Therefore, this version will use ClickHouse as the database to provide better performance while requiring lower hardware specifications. For live trading interfaces, we will use QMT, allowing users to access live trading with a very low capital threshold. Since the market data sources we previously planned to integrate were unstable, we are still seeking new low-cost (even free) data sources. This version will no longer be open-source and will be available exclusively to students, thereby providing more value to them.

## Other Questions

!!! tip "I have a GPU. Can I use it in quantitative trading?"
    If you start directly from price data, end-to-end AI techniques are currently immature and may never mature. Price data contains significant noise, or rather, it is a many-to-many mapping, making effective learning difficult.<br><br>
    The most mature solution combining quantitative strategies with AI today involves manually extracting factors and using machine learning, particularly algorithms like XGBoost/LightGBM, for factor combination. XGBoost/LightGBM can partially utilize GPUs, but using a GPU is not mandatory. Especially since LightGBM’s training speed is already very fast.

!!! tip "How do I apply for quantitative trading permissions? What are the thresholds?"
    Generally, you can apply for quantitative trading permissions simultaneously when opening a new account. You can consult quantfans_99 on WeChat to help you find the broker with the lowest threshold and optimal fees.

!!! tip "Can you introduce the instructor?"
    <div style="width:150px; position: relative;float:right">
        <img src="https://gcore.jsdelivr.net/gh/zillionare/images@main/images/hot/me.png" style="width: 120px; display:inline-block"/>
        <p style="text-align:center;width:120px"> Aaron </p>
    </div>

    -   Senior Software R&D Manager at IBM/Oracle

    -   Vice President of Dolphin Browser (invested by Sequoia Capital)

    -   Founder of KuangTi Quant

    -   Initiator of the Zillionare open-source quantitative framework

    -   Author of *Python Efficient Programming Practice Guide* (published by Mechanical Industry Press).

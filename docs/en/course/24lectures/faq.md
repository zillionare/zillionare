---
title: "2025 Quant Investing Course FAQ: Study Time and Payoff"
date: 2024-01-04
slug: en/articles/course/24lectures/faq
tags: [Quantitative Investing, Course FAQ, Backtesting, Career Planning]
excerpt: "A 2025 FAQ on our quantitative investing course: 24 chapters, roughly 31 hours of video, a hosted notebook server with 4 billion+ commercial data records, plus straight answers on study time and profitability."
lang: en
translation_of: articles/course/24lectures/faq
auto_translated: true
source_sha: 4bc49182c3309f1eecc5f359a1be2ceb3ad6a19c
---

## Enrollment and Learning Environment

!!! abstract "How is the course delivered?"
    The course is delivered as videos, notebooks, and Q&A support. Videos are sent to you via Baidu Cloud Drive, and the notebooks are hosted on the courseware server we provide.
    Videos are yours to watch permanently; the courseware server is available until June 2027.
    On the courseware server, all data and dependencies are pre-installed, so the code in the notebooks runs out of the box — and you're free to modify and debug it yourself.


!!! abstract "What does the course cost?"
    The current price is 2,099 RMB. Before you buy, we recommend adding our TA Kuanfen on WeChat (quantfans_99) to learn about the purchase process and to get discounted pricing and free gifts.


!!! abstract "How do I buy it?"
    <div style="width:150px; position: relative;float:right">
        <img src="https://gcore.jsdelivr.net/gh/zillionare/images@main/images/hot/quantfans.png" style="width: 120px; display:inline-block"/>
        <p style="text-align:center;width:120px"> 宽粉 </p>
    </div>

    We recommend first adding our TA Kuanfen on WeChat (quantfans_99) to learn about the purchase process and to get discounted pricing and free gifts. You can also order directly on [Lizhi Weike](https://wk.nczzmn.com/channel/1704575?st=sharelink&inviter_id=88872237), but you'll need to contact the TA after purchase so we can activate your online course access.


!!! abstract "How long does the course take?"
    The course has 24 chapters, roughly 400,000 characters of text, and about 31 hours of video. How long it takes depends mainly on your own schedule. At one lesson per day, you should finish within four weeks.<br><br>
    Course videos are free to watch forever. The dedicated courseware server is available until June 30, 2027.<br><br>The courseware server is for study use only and may not be used as a cloud server.


!!! abstract "Who is this course for / what are the prerequisites?"
    Anyone with **basic Python programming knowledge** and **university-level mathematics** can enroll. If you're unsure, ask Kuanfen (quantfans_99) and she'll help you assess whether you meet the entry requirements.<br><br>If you already have some programming background and are currently learning Python, you can also enroll first — the instructor offers free tutoring.


!!! abstract "Do you provide a learning environment?"
    We run a server cluster with 192 CPU cores and 256 GB of RAM for students. Log in through your browser and you can study and run our example code online. In that environment we have purchased more than 4 billion records of commercial data (measured in time-series database terms; sponsored by JoinQuant since 2024) — the subscription for this data alone costs over 20,000 RMB.


!!! abstract "What's the advantage of your environment? Can I just build my own?"
    The biggest advantage is that we provide backtesting (not backtrader-based) together with commercial data. Our backtest matches orders on minute bars and automatically enforces T+1 settlement and price-limit trading restrictions, reproducing real trading conditions as faithfully as possible. The data volume is enormous and cannot be replicated. So if you build your own environment, you would still have to buy the data to faithfully reproduce live trading conditions. **Strategy tuning is only meaningful when it is based on real data.**


!!! abstract "I'd like to know more about the course"
    We offer a preview environment containing selected lessons (videos, notebooks, and exercises). Add the TA on WeChat at quantfans_99 to get the link.


## Career Planning Questions

!!! tip "Who takes this course?"
    Based on informal counts (not every student is willing to share their background), more than two Ivy League PhDs and close to ten fund managers (including heads of private funds) have taken this course, and several private funds have purchased it for their employees and interns. Other students include Hong Kong investment bankers, private fund staff, engineers from major internet companies, and university students.


!!! tip "Why learn quantitative trading?"
    Only by learning to manage your money can you earn while you sleep. Learn quantitative trading and you stop working for money — money starts working for you.


!!! tip "Will I make money once I finish this course?"
    Yes and no. This is a comprehensive course, and its focus is on how to turn a strategy idea into a programmatic, scientific process. If you are an experienced trader, you will be able to use the methods taught here to re-examine your own trading experience, separate what works from what doesn't, and codify the effective parts as programs — freeing yourself from emotional swings, limited mental computation, and the inability to see and analyze the whole market. If you have no trading experience, you will still learn sound quantitative theory and research methods, and gain the key to a treasury of strategies.<br><br>In short, after this course you will have made obvious progress, whether measured against your past self or against other traders. But whether you make money depends not only on your own improvement but also heavily on the market. If the market is falling and you cannot short, making money is difficult.


!!! tip "Do you know any headhunters who could help with referrals?"
    Of course. Our Xiaohongshu account [量化风云](https://www.xiaohongshu.com/user/profile/5ba12feef7e8b9437f3aca0c) (Quant Winds) ranks first in the quantitative finance niche on the platform, and headhunting firms proactively partner with us.


## Other Questions

!!! tip "I have a GPU — can I use it for quant work?"
    If you start directly from price data, end-to-end AI is not mature yet, and may never be. Price data contains a great deal of noise — or rather, it is a many-to-many mapping — so it is hard to learn from effectively.<br><br>
    The most mature way to combine quantitative strategies with AI today is to hand-engineer factors and then use machine learning — especially XGBoost/LightGBM — to combine them into a factor model. Both can make partial use of a GPU, but a GPU is not required. LightGBM in particular already trains very fast.


!!! tip "How do I apply for quantitative trading permissions? What are the requirements?"
    New brokerage accounts can usually apply for quantitative trading permissions at the same time. Ask Kuanfen (quantfans_99) and she'll help you find the broker with the lowest threshold and the best fees.


!!! tip "Can you introduce the instructor?"
    <div style="width:150px; position: relative;float:right">
        <img src="https://gcore.jsdelivr.net/gh/zillionare/images@main/images/hot/me.png" style="width: 120px; display:inline-block"/>
        <p style="text-align:center;width:120px"> Aaron </p>
    </div>

    -   Senior Software R&D Manager at IBM/Oracle
    -   VP at Dolphin Browser (Sequoia Capital–backed)
    -   Founder of Quantide
    -   Initiator of the open-source Zillionare quantitative framework
    -   Author of *Python High-Performance Programming Practices* (China Machine Press)

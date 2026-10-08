---
title: "Top Programming Languages in Finance: SQL, Python Lead"
date: 2024-06-10
slug: en/posts/career-figure/how-to-start-a-hedge-fund-alfonso-peccatiello-story
tags: [Financial Careers, Python, SQL]
excerpt: "Revelio Labs data shows SQL is required in 25% of finance job postings, ahead of Python, Java and R. We break down why SQL and Python dominate finance and what proficiency employers expect."
lang: en
translation_of: posts/career-figure/how-to-start-a-hedge-fund-alfonso-peccatiello-story
auto_translated: true
source_sha: ab1931d92af36d0826a6320b81f0ac0582d11d2d
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/06/fencing.jpg"
---

Over the past couple of days, I've been getting DMs asking: is it hard to break into quant?

The sender didn't share any background or say what role they were targeting. So it's an unanswerable question as asked. Still, I'll keep following up on it and share some useful references.

Today's focus: what programming skills does finance actually need. The data comes from Revelio Labs and eFinancialCareers. The former is a workforce-intelligence analytics firm, the latter is a specialist finance job board.

---

According to Revelio Labs, the top 10 most in-demand programming languages in financial services are:

![Bar chart of the top 10 most popular programming languages in financial services from Revelio Labs, with SQL at No.1](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/06/coding-language-in-finance.png)

You might not expect it, but SQL rules finance. Across tech as a whole, only 18% of postings mention SQL, but in finance hiring it's around 25%.

Of course, many people don't even count SQL as a programming language. Honestly, it's just a database query language — you can't use it for much beyond querying data.

That's why Python is the real king, not just in finance. It still tops the June TIOBE rankings, and its popularity is still climbing.

---

![TIOBE programming language popularity ranking for June 2024, with Python at No.1](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/06/tiobe-ranking-2024-6.png)


But finance doesn't have much demand for internet favorites like C++ and Rust. While both are indispensable in high-frequency trading, HFT is a niche that can't absorb large amounts of capital, so it's not where the industry's center of gravity lies.

The lower the trading frequency, the greater the capacity for capital. That's why a language like Python — poor on performance but fast and flexible to build with — is so widely used across finance. The heavy use of SQL also shows that finance doesn't require extreme big-data processing power; SQL still handles most data workloads. That's entirely understandable, because the fundamental data widely used in low- to mid-frequency trading isn't that large.

Java in the top three is no surprise either. Plenty of transactional systems, including corporate websites, are still built in Java.

---

Javascript likely made the list for the same reason. To maintain a secretive, high-tech image, investment firms often build flashy websites. Millennium's official site, for example, loves to show off with Javascript. Their latest homepage features JS-powered magnetic field lines and various reveal effects.

<div style='width:"75%";text-align:center;margin-bottom:1rem'>
<img alt='Millennium homepage with Javascript-powered magnetic field animation' src='https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/06/millennium.png'>
<span style='font-style:italic;font-size:0.8rem'>Millennium official site</span>
</div>

The design is ugly, admittedly. But it nails the quant-nerd aesthetic. So strong front-end skills can get you into finance too.

R at No.4 is no surprise either. R is widely used in data science, ships with rich statistical modules out of the box, has simple syntax with pipe operators, and is great for ad-hoc analysis. SAS made the list for the same reason. Both SAS and R offer excellent native support for factor analysis. Statistical toolkits and factor analysis are foundational for data analysis in finance.

---

The more surprising entry is VBA. Its presence really means: you must master Excel to work in finance. And mastering Excel doesn't just mean knowing the point-and-click features — it means being able to write VBA scripts when it counts, for complex tasks and for crunching large datasets quickly.

How important are strong programming skills for landing a finance job? Just look at this recent eFinancialCareers posting for a Global Head of Credit and Convertibles — a $500k to $800k a year role:


!!! quote
    A renowned investment firm is looking for an Head of global credit and convertible bonds to report to their CIO function ...

    Experience

    - Fixed income in preferably a sell-side company
    - Front-office
    - Experience with arbitrage
    - Experience with credit, equities, convertibles, CDS
    - **Strong programming skills (Python or R, SQL, Excel or VB)**
    - Strong communication skills and ability to work in a team

---

If you're still in school, you probably know a bit of SQL and Python — but what counts as proficient?

For Python, for engineering craft see my new book *Python High-Performance Programming in Practice* (on sale in July), and for algorithms grind LeetCode and Kaggle problems, or the puzzle columns from Jane Street and Millennium — our column also shares performance-optimization tips from time to time.

![50%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/book-cover-with-bridge.jpg)

For SQL, developers need to understand data partitioning, index optimization, and query tuning, while data analysts just need to build complex queries — mainly window functions, subqueries and self-joins, and complex filtering and grouping.

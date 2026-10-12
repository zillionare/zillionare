---
title: "24-Lesson Quant Trading Course: Full Pipeline & Live Trading"
date: 2024-01-04
slug: en/articles/course/24lectures/detail
tags: [Quantitative Trading, Factor Analysis, Backtesting, Live Trading]
excerpt: "A comprehensive 40,000-word course with 7,000+ lines of code covering the entire quantitative trading lifecycle. From data sourcing and factor analysis to backtesting and live execution, this curriculum bridges the gap between theory and real-world implementation."
lang: en
translation_of: articles/course/24lectures/detail
auto_translated: true
source_sha: 6f41efaab2e66b42edd9fbb391684a0b92504f9a
---

This course comprises 40,000 words and over 7,000 lines of code (excluding bonus strategy code provided as a bonus). In one sentence: it covers the entire quantitative trading workflow, enabling you to transition from learning to live trading immediately upon completion.

The course is divided into six parts and 24 chapters. Below is an overview of the content for each part, reflecting our considerations in topic selection and curriculum design:

## 1. Where Does Data Come From?

The prerequisite for quantitative trading is access to massive, reliable data.

For data sources, institutional investors primarily use financial terminals such as Eastmoney Choice and Wind Info. Data providers include Wind, Hundsun Juyuan, Chaoyang Yongshu, Tianruan, Juchao, Tianxiang, Juling, Guotai An, and Tonglian. Chaoyang Yongshu holds advantages in analyst consensus expectations, earnings forecasts, and private fund data. Tianruan Technology excels in high-frequency market data. The Guotai An database is mainly for academic purposes, with comprehensive corporate finance data.

Individual and small private equity investors mainly use data sources like Tushare, AKShare, jqdatasdk, and QMT. These are the primary subjects of this course section.

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/05/lesson3-outline.png)

This section consists of 5 lessons. We will focus on AKShare, Tushare, jqdatasdk, and Omicron—the data SDK built into the Daifuweng framework. We will also mention YFinance and other sources. We will clarify which are usable and which are obsolete to save you time.

**Saving you time is a key objective of this course.** We believe that even without this course, you might piece together a quantitative tutorial, but it would take much longer to find the right direction, causing you to lose your first-mover advantage.

When introducing each data source, we explain its API style, documentation style, and API categorization, detailing how to retrieve trading calendars, security lists, and market data. Each source offers dozens or more APIs, so **categorized introduction is crucial**. Once you master the API style and documentation of each framework, exploration becomes effortless.

Considering that asking students to purchase data (free data has various limitations) seems unreasonable in a quantitative course, yet many programs cannot be demonstrated without data: to ensure a better experience, we have built a quantitative environment providing real-time and historical market data (approximately 4 billion records) and a backtesting platform for everyone’s use. This is why we introduce Omicron—apologies for naming it so in 2019; while the name went global, we haven’t quite achieved that fame yet.

Furthermore, this section lays the foundation for the entire series. We cover topics closely related to data processing, such as security code encoding, exchange codes, adjustments (forward/backward), and rounding issues in financial data processing. Here, we address seemingly simple but often overlooked or unconsidered issues that are actually critical:

**Is your usual rounding method correct?**

You may never have thought about this. Isn’t it just `math.round`? Could it be wrong? But you surely know the consequences of rounding errors: for low-priced stocks under 2 yuan, rounding can introduce a 0.01 yuan error, equivalent to at least a 0.5 percentage point deviation!

This is not the only impact of rounding errors. In fact, it affects price granularity at the microstructure level, influencing the distribution of buy and sell orders. Interested readers, especially those in high-frequency trading, can refer to the paper [Is Stock Price Rounded for Economic Reasons in the Chinese Markets](http://centerforpbbefr.rutgers.edu/2005/Paper%202005/PBFEA29.pdf) to understand the special role of integer prices and auspicious numbers in A-share pricing, as well as similar patterns in global markets.

Now, let’s tell you: Python’s implementation is indeed flawed!

Some quantitative tutorials suggest avoiding forward-adjusted prices and using backward-adjusted prices instead. We will encourage you to rethink this. When we reveal that forward and backward adjustments are merely linear transformations, you may ponder deeper: since linear transformations generate no new knowledge, what is the actual difference between forward and backward adjustments?

In this section, we also reveal the value of data. We explain how to obtain data such as investor numbers and index PE ratios, and how they correlate with the Shanghai Composite Index’s movements, which is helpful for large-cycle timing.

Some libraries are useful and well-written. But software is a technology full of regrets. We will also provide improvement suggestions for certain open-source software. If you are looking to contribute to open-source quantitative software, you might start with our suggestions to help完善 them.

## 2. Introduction to Strategies

We use three lessons to introduce three strategies from three dimensions. We place strategies in the second part because, after completing the first part, some students may already be eager to try; more importantly, these strategies demonstrate from different angles what skills are required to build a robust strategy, helping you understand the rationale behind the subsequent curriculum arrangement.

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/05/lesson6-outline.png)

Lesson 6 introduces a small-cap strategy, representing the **fundamental dimension**. The small-cap factor is part of the Fama (FF) three-factor model. Its effectiveness has been validated by Wall Street for decades and was highly effective in A-shares before 2017, entering a phase of intermittent effectiveness and ineffectiveness thereafter. This lesson answers several questions:

1. What minimum functionalities must the simplest strategy implement?
2. How to plot asset curves and strategy metrics after backtesting?
3. From which directions should strategy optimization proceed?

The code in this lesson is concise, easy to understand, and lacks tricks. However, we leave an assignment: how to abstract common parts of the strategy and backtest into a reusable framework?

Easy to say, harder to do. Once you have manually constructed one, your understanding of quantitative trading will deepen. By Lesson 19, when we discuss complex backtesting frameworks like Backtrader, you should be able to get up to speed quickly and understand issues like:

**Why does my strategy eat meat in backtests but dirt in live trading?**

This isn’t necessarily your fault. Backtesting frameworks have their own choices and difficulties. Those who haven’t developed a backtesting framework don’t know this, nor can they explain it to you. But if **you don’t understand the flaws of your weapon, how can you ensure it fires reliably on the battlefield**?

Lesson 7 introduces the Bollinger Bands strategy, representing the **technical analysis dimension**. Bollinger Bands use only the simplest statistical theory—properties of the normal distribution. We rarely use it alone now, but as a single strategy, it once shone brightly, founding a startup. Moreover, the normal distribution principle is an unavoidable knowledge point in statistical and financial data analysis.

Technical analysis (broadly defined as excluding fundamental analysis and macroeconomic timing) is the most effective strategy method for **medium and small-scale capital** in A-shares. From the latest Huatai Securities Research report (August 2023), we see that the most effective factors in July were still **reversal factors** and **volatility factors**, with small-cap ranking third. This remains an era where technology reigns supreme.

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/08/factor_performance_202307_1000.png)

These factor performance data reveal the general direction of strategy research. You should have better methods to seek reversals and master volatility. If you are interested in implementing these factors, you can find answers in our *Factor Analysis and Machine Learning Strategies* course.

Lesson 8 introduces grid trading, a strategy that requires no specific strategy, built from the **trading dimension**. It fully embodies the advantages of quantitative trading: avoiding emotional operations, strictly executing discipline, and potentially achieving profitability even without a complex strategy.

**When you have a fishing net, the key is knowing where to cast it.** The premise for grid trading success is that the stock price ranges sideways over the long term. We indicate what conditions or targets are likely to produce long-term sideways movement. These conclusions are based on **behavioral finance** principles and trading rules. After completing the subsequent lessons, you will have the ability to programmatically identify such targets.

## 3. Python Quantitative Trading Data Analysis

Lesson 9 introduces NumPy and Pandas, which generally serve as the foundational data structures for quantitative trading, while we also perform numerous operations using NumPy and Pandas.

Predicting price movements is difficult but possible in extreme scenarios. For example, if the Shanghai Composite Index has risen for seven consecutive days, what is the probability of it rising or falling tomorrow? Predicting a fall would likely be correct. We set aside this probability calculation for now and return to a simpler question: how to programmatically detect if a security has experienced N consecutive days of gains?

Almost anyone who can code and has basic securities knowledge can implement this. But you need to do it better, e.g., without loops, using a single line of code, and finding all N-consecutive-day gains over the past few years at once... Speed is critical. Even if you trade only once daily, rebalancing before market close, you have only about two minutes (14:56 to 14:58) to traverse all market varieties (and perform strategy calculations). Your program must be fast; practice shows this is not easy.

In this lesson, we cover almost all frequently used NumPy functions in common quantitative frameworks. The exercises in this section are also technical; mastering them will quickly make you a NumPy/Pandas expert!

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/06/lesson9-outline.png)

Lesson 10 introduces TA-Lib, one of the most important technical analysis libraries, integrated into many quantitative frameworks.

Lessons 11 and 12 introduce some statistical knowledge. You will soon see its immense power!

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/07/lesson11-outline.png)

In these two lessons, we verify the fundamental question of what probability distribution the Shanghai Composite Index follows, and answer questions like, “If the Shanghai Index drops 4%, can we buy the dip?” We believe that after learning more similar questions, you will naturally be able to explore and answer them.

Many people think probabilistic concepts are difficult to understand, such as PDF (Probability Density Function) / CDF (Cumulative Distribution Function). But we start with histograms, then imagine each bin size approaching zero, yielding the PDF. We believe that with this explanation, plus countless charts and code, probability and statistics are not so hard to understand?

Combining what we have learned previously, we can now perform some relatively difficult K-line pattern detection. This is the main content of Lesson 13—technical pattern analysis.

K-line pattern detection is very useful in a retail-dominated market; it is the basis for programmatic execution of the **Elliott Wave Theory**. The essence of short-term trading is chip distribution; any rise or fall must fall into a limited number of paradigms. Therefore, K-line pattern detection, even if not used for prediction, can be used for post-event confirmation.

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/07/lesson13-outline.png)

In this lesson, we provide a fully adaptive method for detecting tops and bottoms: based on probability distribution theory, with a solid mathematical foundation.

The red dots show the results of our adaptive algorithm detecting tops and bottoms. Based on these tops and bottoms, we calculated support and resistance lines. When the facts are laid before us, you have to admit that **chartists sometimes indeed control the A-share market**:

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/08/lesson12-resist-line.png)

We can certainly use it for more things, such as detecting M-tops and W-bottoms:

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/06/double_top_detected.png)

Or platform breakout detection (here we transplanted a 2D clustering algorithm from machine learning to 1D time series):

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/08/platform-breakout.png)

And the principles and algorithms of smart RSI, etc.

If your goal in taking this course is to change jobs, then the content of Lesson 14—factor analysis—is indispensable. We detail all aspects of factor analysis: regression, IC, and layered backtests, from principles to implementation.

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/06/lesson14_toc.png)

After completing the full process of factor analysis and having a comprehensive view of most details and frameworks, Lesson 15 brings you to Alphalens. Now, learning Alphalens should be much easier, as you already know what it is and what it does.

!!! info
    Alphalens is part of the Pyfolio library developed by Quantopian. Quantopian was once the world’s largest open-source Quant community; its success also drove the development of domestic startups like JoinQuant and BigQuant. Today, Quantopian is history, and Alphalens has become quantitative heritage with no new maintainers. If you are skilled in program development, after completing this course and mastering sufficient domain knowledge, you might even become its maintainer—perhaps this is where you can achieve something!

## 4. Data Visualization

Lessons 16 to 18 focus on visualization.

![L50](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/07/dash.png)

Plotting is not just for creating beautiful visualizations but also to unleash the full potential of data and reveal hidden insights. It is the bridge between digital language and storytelling language, enabling individuals and organizations to make informed decisions and create meaningful change.

In quantitative trading, although we rely mainly on automated programs, we still rely on our intuition for factor exploration, generating backtest reports, and algorithm research. This intuition comes precisely from graphics.

In this course, we introduce superstars in the plotting world: Matplotlib, Plotly, Seaborn, and Pyecharts. Consistent with the course’s philosophy, we dissect the plotting frameworks and partially restore the mechanisms under the hood, ensuring you are never at a loss when facing new frameworks and new problems.

## 5. Strategies and Backtesting

Lessons 19 and 20 introduce Backtrader, currently the most popular pure backtesting framework.

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2023/08/lesson19-outline.png)

In Lesson 21, after becoming proficient in backtesting, we learn how to evaluate our strategies. We introduce the Sharpe ratio, Sortino ratio, annual return, and many other metrics, explaining how they reveal the balance between risk and profitability in a strategy. We also introduce a professional yet easy-to-use strategy evaluation metric plotting library—QuantStats.

Backtesting, like life, is full of traps. Some are brought by the framework itself—for example, some frameworks cannot use true adjusted prices (e.g., Backtrader, if you generate indicators all at once in `__init__`, regardless of which adjusted price data you use, you are using future data!); others stem from your strategy, calculation precision, misuse of look-ahead bias, dividends, trading rules, etc. We will detail these pitfalls in this lesson.

We will also introduce the Daifuweng backtesting framework. This is not to sell private goods, but because frameworks like Backtrader either cannot avoid the aforementioned backtesting traps or require significant effort to modify. Considering that Daifuweng is open-source and its backtesting framework almost supports distributed backtesting—if I were to modify Backtrader, I might as well accept the Daifuweng backtesting framework—if your company is looking for a solution that complies with A-share trading rules, solves adjustment issues, and preferably has distributed capabilities—we recommend you study this lesson carefully.

This is the content of Lesson 22.

## 6. Connecting to Live Trading

Lessons 23 and 24 introduce how to connect to live trading. You will also leave the rehearsal stage and enter live broadcasting from here.

We will introduce EasyTrader, which has no capital threshold, and PTrade, QMT, and the Eastmoney and Huatai quantitative trading platforms, which have certain capital thresholds. QMT is a quantitative platform launched by Xuntou. In addition to built-in strategy editing and backtesting functions, it provides a Python library called XtQuant, which we can use for its data and trading functions. Currently, QMT is the most cost-effective solution for connecting quantitative programs to live trading.

Ten years to sharpen a sword, its edge untried. After so many lessons of learning and practice, I am confident that you are ready to build your own money-printing machine!

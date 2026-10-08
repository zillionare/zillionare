---
title: "QuanTide Weekly: HFT Fees, Olympic Plays, and RSI Mean Reversion"
date: 2024-07-28
slug: en/posts/uncategory/weekly-0728
tags: [Quantitative Trading, Factor Analysis, High-Frequency Trading, Mean Reversion]
excerpt: "Regulators propose 10x HFT fee hikes; Guangdong audits quant funds; Nasdaq drops 3.64%. Deep dive into short-term RSI mean reversion and Alphalens factor analysis limitations."
lang: en
translation_of: posts/uncategory/weekly-0728
auto_translated: true
source_sha: 7689ee3554ca34149549216ee3d62aa7d98bc1d8
---

## This Week’s Highlights

* HFT fees may increase 10-fold
* Paris Olympics open; new "Olympic concept" sector emerges
* Guangdong private equity self-audit focuses on quant trading and fund scale compliance
* Nasdaq drops 3.64%; Nikkei Index records longest consecutive decline since October 2021

## Key Calendar for Next Week

* "Rate cut" wave begins next week
* Global equities face Super Central Bank Week
* Three major indices...

## This Week’s Selections

* The Holy Grin Shines! Mean Reversion Strategy Based on Short-Term RSI
* Visible but Unattainable! 7-Year, 2,500x Long-Short Strategy
* What Are the Top Quantitative Investing Journals? (Part I)

<!--
News indicates regulators are drafting rules to raise HFT transaction fees from 0.1 RMB to 1 RMB per order. Industry sources confirm that some quant private equity firms have received directives to increase traffic fees by 10-fold for those meeting HFT criteria, from 0.1 RMB to 1 RMB per order. One quant firm noted these fees are calculated by the exchange, issued monthly to brokers, and collected quarterly from clients. Some quant firms have already adjusted risk control parameters. Another trader stated that fees exceeding 5x would eliminate alpha for current strategies, effectively limiting high-frequency quant trading. Rumors of such fees circulated as early as July 12, including "bilateral turnover < 4x/month, cancel rate < 40%, 1 RMB per order (excluding cancellations), 5 RMB per cancellation." Quant firms participated in feedback meetings at that time.

[Guangdong CSRC organizes self-audit for private funds; quant trading and fund scale compliance are key] On July 22, the China Securities Regulatory Commission (CSRC) Guangdong Bureau issued the "Notice on Organizing Self-Audit of Private Investment Funds in the Jurisdiction for 2024." The notice requires private fund managers to self-audit compliance in promotion, fundraising, and investment operations; accuracy and timeliness of registration, reporting, and disclosure; internal management and risk control; overdue fund products; engagement in quant trading; off-site operations; and compliance with registration conditions. Journalists noted that Guangdong CSRC has repeatedly organized such audits, covering "fundraising, investment, management, and exit" stages and potential risk areas. (21st Century Business Herald)

According to Shanghai Securities News, A-share companies such as CIMC Group, Shuhua Sports, Absen, Unilumin, and Yuanlong Yatu participate in "gold-winning" efforts related to Paris Olympics facilities, equipment, marketing, and cultural derivatives. East Money and Tonghuashun have launched Olympic concept stocks.

Xinghui Entertainment: Espanyol Club Players Participate in 2024 Paris Olympics] An investor asked if the club has players in the Paris Olympics. Xinghui Entertainment stated on its interactive platform that Espanyol is committed to supplying players to the Spanish Olympic team. Player Joan Garcia has been selected for the Spanish U23 team and will compete in the 2024 Paris Olympics.

Pop Mart: First Store Opens in Indonesia; Overseas Stores Reach 100] On July 22, Pop Mart opened its first Indonesian store in Gandaria City, South Jakarta, marking its 100th overseas and Hong Kong/Macau/Taiwan store. Pop Mart’s globalization is accelerating, with breakthroughs in Vietnam, Italy, and Indonesia. Its Paris Louvre store will open during the Olympics.

Nasdaq 100 Index fell 3%, marking the largest decline since December 2022. Components Tesla dropped over 10%, Arm Holdings fell 7.2%, Nvidia fell 5.7%, Alphabet A fell over 5%, and Meta fell 4.3%.

<!--

A poet is sacred in history but absurd next door. We worship distant gods but ignore miracles nearby.

Life is short. Do not spend your life living someone else’s life.

Hinton

Yitang Zhang

-->

---

## This Week’s Highlights

* According to Cailian Press, regulators are drafting rules to raise HFT fees from 0.1 RMB to 1 RMB per order. A quant trader stated that fees exceeding 5x would eliminate alpha for current strategies, effectively limiting high-frequency quant trading. <remark>Current HFT criteria involve >300 orders per second or total orders/cancellations ≤20,000 per day.</remark>
* Paris Olympics opened. A-share companies in facilities, equipment, marketing, and derivatives participate, including CIMC Group, Shuhua Sports, Absen, Unilumin, and Yuanlong Yatu. East Money and Tonghuashun launched Olympic concept stocks.
* According to 21st Century Business Herald, Guangdong CSRC organized self-audits for private funds. Key areas include compliance in promotion, fundraising, and investment; overdue products; quant trading; off-site operations; and fund scale compliance.
* On July 25, Nasdaq 100 Index fell 3%, largest decline since December 2022. Nikkei Index fell 5.9% this week, 8 consecutive days, longest decline since October 2021. However, US stocks rose on Friday, with Dow Jones recording 4 consecutive weekly gains.
* Northbound capital continues selling. Cumulative net reduction of 30.7 billion RMB over 2 weeks, with monthly net sales of 28.8 billion RMB.
* PBOC conducts rare MLF operation to stabilize month-end liquidity. On July 25, PBOC added a mid-term lending facility (MLF) operation at month-end, with a winning rate of 2.3%, a 20 basis point decrease from the previous rate.
* CSRC studies further comprehensive deepening of capital market reform and opening up. Wu Qing held symposiums with 10 foreign institutions and QFII representatives to gather opinions.

<claimer>Information sources: Cailian Press, etc., compiled via Tushare.pro interface.</claimer>

---

## Key Calendar for Next Week

* Multiple banks will cut rates starting next week. On July 26, China Merchants Bank and Ping An Bank adjusted RMB deposit benchmark rates, with maximum cuts of 30 basis points. Guangfa Bank will also cut deposit rates next week, aligning with the four major banks. Large-denomination certificates of deposit will also be adjusted.
* Global investors face Super Week. Three major central banks will announce rate decisions. The Fed meets on Wednesday. Tech giants Microsoft, META, and Apple will also release earnings.
* On July 31 (Wednesday), the National Bureau of Statistics will release PMI data. Previous value was 49.5. Caixin will release manufacturing PMI on August 1.

<claimer>Information sources: Cailian Press, etc., compiled via Tushare.pro interface.</claimer>
---

# Mean Reversion Based on Short-Term RSI

<claimer>This article was published on Tuesday’s official account, receiving over 4,000 views.</claimer>

## Strategy Overview

Everyone should be familiar with the RSI indicator. The commonly used RSI is calculated based on 6, 12, and 24 periods.

$$
RS = \frac{\text{SMMA}(U,n)}{\text{SMMA}(D,n)}
$$

$$
RSI = 100\cdot\frac{\text{SMMA}(U,n)}{\text{SMMA}(U,n) + \text{SMMA}(D,n)} = 100 - { 100 \over {1 + RS} }
$$

However, Larry Connors believes that a 2-period RSI better reflects market trends, possibly the "Holy Grail" of technical indicators. He published this view in his 2008 book *Top Traders on Wall Street*. In subsequent Connor's RSI indicators, the streak RSI uses a 2-period calculation.

Based on this RSI, Connors proposed the following mean reversion strategy:

1. S&P 500 Index is above its 200-day moving average;
2. S&P 500 Index’s 2-period RSI is below 5;
3. Buy at close when signal is issued;
4. Sell when S&P 500 is above its 5-day moving average.

---

In trader terms, this is a **buy** strategy during **bull markets** (index > 200-day MA) and **short-term pullbacks** (RSI < 5).

## Factor Testing

First, quantitativo conducted single-factor testing. The method involves buying and holding for 5 days all targets where 2-day RSI closes below 5, then calculating returns.

![75%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/factor-rsi-2-buy-and-hold-5.jpg)

This statistic includes over 21,000 targets and over 2.5 million events (S&P 500 closing above 200-day MA). Highlights from the test:

1. Average return for buying any given stock when 2-day RSI < 5 and holding for 5 days in a bull market is 3.3%;
2. 60% of events yield positive returns, with expected return per trade of 9.8%;
3. 40% of trades are negative, with expected return per trade of -6.6%;
4. Distribution is positively skewed.

quantitativo also analyzed the reverse scenario: buying all stocks when 2-day RSI > 5 and holding for 5 days in a bull market. Results:

---

1. Expected return for buying any given stock when 2-day RSI > 5 is 0.3%;
2. Probability of positive trade is 52%, expected return 5.5%;
3. Probability of negative trade is 48%, expected return -5.1%.

quantitativo performed hypothesis testing on whether the two tests belong to the same distribution, with p-values well below 0.05, proving the distributions are significantly different. Thus, the factor in the first test exhibits Alpha.

## Strategy Backtest

Next, quantitativo conducted strategy backtesting. The strategy design is as follows:

1. Use SPY as the test target.
2. Buy SPY at the next open when:
   1. S&P Index RSI(2) closes below 5
   2. SPY is above 200-day MA
3. Exit conditions:
   1. Exit at next open when SPY close > previous day high.
   2. Exit if SPY close < 200-day MA

The backtest strategy differs slightly from Connor’s. Why?

The difference reflects the gap between backtesting and live trading. Connor’s strategy is more idealized, while quantitativo’s verification is closer to live trading. This is a consideration we must always make when developing strategies.

First, while we can backtest using S&P 500, in live trading, it is more practical to buy the corresponding ETF. SPY is an ETF tracking the S&P 500.

---

Second, Connor’s strategy buys at close. If your backtest system is not precise enough, it is better to buy at the next open. Of course, if your backtest system and market data are minute-level, in China, you can calculate signals using the close price one minute before call auction and buy at the call auction.

The difference in exit conditions can be seen as an optimization by quantitativo. However, I do not see the significance of this optimization. It seems to lack any trading principle support. It looks more like overfitting by quantitativo through data.

!!! question
    quantitativo used 25 years of data for this experiment. If performance remains strong after such a long backtest, can we say there is no overfitting? I am interested in your views.

So, what were quantitativo’s experimental results?

Testing on SPY was a disaster. Over the entire backtest period (25 years), trading this strategy with SPY yielded 67% return. The main reason is too few trades, only 157 executed.

![75%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/performance-qqq-tqqq.jpeg)

---

Next, quantitativo switched to Nasdaq 100 Index ETF (QQQ) and 3x leveraged Nasdaq 100 ETF (TQQQ). Results show good performance on TQQQ (see previous chart):

Sharpe ratios reached 2.3 (QQQ) and 1.92 (TQQQ), quite good indicators for index targets (especially compared to China A-shares).

## Improved Strategy: Adding Factors

Building on the previous experiment, quantitativo added an asset portfolio.

They divided funds into ten slots (10 slots) to buy targets where previous day RSI closed below 5; if the universe has >10 targets triggering entry signals, rank by market cap, prioritizing smaller caps. Exit condition changed to close < 200-day MA.

Additionally, they restricted trading only to liquid targets:
1. Only trade targets with no suspension in the past 3 months
2. Exclude targets with median daily volume in past 3 months < 20x fund share

![75%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/new-experiments-1.jpg)

---

!!! tip
    Actually, quantitativo introduced another factor here, the small-cap factor, though with low weight—applied after RSI trigger.

This result was quite good, with overall annual return reaching 17.8%, 3x the benchmark. But there is a problem: all this was achieved in the first 8-9 years. The strategy stopped executing after 2008 and lost to the benchmark since then.

Why? Analyzing 11,380 trades over 25 years, quantitativo found many delistings. The naive approach’s issue is prioritizing small caps (after liquidity filter), which have a +70% delisting probability.

## Second Improvement: Reducing Delisting Risk

![75%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/07/new-experiment-2.jpg)

quantitativo improved the strategy again, this time restricting the universe to large and mega-cap stocks, which have lower delisting probabilities (35% and 9% respectively).

---

This time, the effect was obvious. Strategy annual return reached 23.9%, 4x the benchmark同期, Sharpe 1.23%, max drawdown 32%, almost half of S&P. But a previous problem remains: too frequent trading. Still 461 trades per year.

<!-- quantitativo analyzed 11,380 trades over 25 years, finding many delistings, but this time could have been avoided -->
## Third Improvement: Reducing Slots

Previous experiments used 10 slots, likely causing excessive trading. Thus, quantitativo reduced simultaneous holdings to 2 targets.

Now, trade count drops from 461/year to 90/year, achieving 30.3% annual return, 5x the benchmark.

## Conclusion

This article introduces a mean reversion strategy based on short-term RSI, finally providing an implementation with 30.3% annual return (excluding slippage and trading fees).

The core of this strategy is short-term RSI. Although this indicator was invented over 45 years ago, backtest results show that if you study something deeply enough, success is likely.

!!! quote
    It's not that I'm so smart; it's just that I stay with problems longer. -- Albert Einstein

This solution is worth your reading time, but more importantly, we discussed the general process of strategy discovery and optimization angles.

---

Let’s summarize again as the closing of this article:

1. RSI represents tides and regression, rooted in human nature, so it will never be obsolete.
2. Multi-factor strategies can also focus on one factor, introducing others as constraints during trading.
3. The article provides a method to judge target liquidity strength, which you can also use as a factor.
4. Strategy R&D steps often start with single-factor testing, then simple backtesting, and step-by-step optimization based on results.
5. In optimization, quantitativo first used ETFs, then switched to 10 slots, finally returning to 2 slots.

---

# Visible but Unattainable! 7-Year, 2,500x Growth

This week we continue exploring the use of the Alphalens factor analysis framework. The relationship between factors and returns is rarely linear, but Alphalens itself is a linear analysis framework, excelling at revealing linear relationships between factors and returns. Its three supported analysis methods are:

* Regression
* IC/Rank-IC (Correlation, Rank Correlation)
* Tiered Regression

All based on linear or quasi-linear regression (relative to SVM, NN, etc.). Thus, how to make Alphalens truly reveal the relationship between factors and returns in factor testing is a skilled task.

In our July 26 video account, we explored how to use `plot_quantile_statistics_table` and `mean period wise return by Factor quantile` charts to unravel and reconstruct factors, perfectly revealing linear relationships between factors and returns.

Here we summarize the video content.

In the experiment, we first used 400 tickers, 1,000 days of data. After determining the direction, we expanded to 2,000 tickers, 2,000 days of data to exclude偶然性.

---

The factor we explore is 6-period RSI. As a factor, generally, higher factor value implies higher return; but RSI is exactly reverse, generally believed that higher RSI implies reducing positions. Thus, the factor we actually construct is:

$$

factor = 100 - RSI

$$

## First Experiment

Running Alphalens with default values simply yields the following results:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/202

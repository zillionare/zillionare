---
title: "TCN Postscript: Why High Win Rates Fail in Live Trading"
date: 2025-11-26
cover: "https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/10/20261009154112-cover-posts-2025-11-tcn番外.md.jpg"
slug: en/posts/algo/tcn/tcn番外
tags: [Deep Learning, Factor Investing, Backtesting, Quantitative Trading]
excerpt: "This article explores why deep learning models like TCN and XGBoost often fail in live trading despite excellent backtest results, highlighting issues like non-stationarity, calendar misalignment, and overfitting."
lang: en
translation_of: posts/algo/tcn/tcn番外
auto_translated: true
source_sha: 4e103cb88c26e017c711b6628f62706daf3c33ce
---

After mastering the core principles of Temporal Convolutional Networks (TCN) and applying them to historical data backtests, many researchers achieve remarkably beautiful results: high accuracy on validation sets and smooth simulated portfolio return curves.

However, once the model is connected to live trading in the real market, these seemingly flawless models often fail rapidly, even generating severe consecutive drawdowns.

When I first witnessed this contrast, I was genuinely stunned.

You stare at the backtest curve for so long that you naturally assume the only remaining issues are position sizing and transaction costs. Then, you go live, and the model seems to suddenly change its brain.

**Is this due to flaws in the model itself, or problems in the code implementation?**

Usually, neither.

### Excellent backtest performance does not guarantee live trading effectiveness. Often, the issue is not that the model was written incorrectly, but that the market environment itself is constantly changing.

The core reason lies in the fundamental differences between financial time series and data in Computer Vision (CV) or Natural Language Processing (NLP).

Using a mindset designed for static data to handle a highly dynamic financial market inevitably leads to friction.

I eventually came to accept a hard truth: often, you didn’t write the model wrong; you just thought the market was too much like Kaggle.

The issues below are ones I have mostly encountered myself, or at least seen in others’ drawdowns.

---

## Dilemma 1: Non-Stationarity and Label Ambiguity in Financial Data: Markets Are Alive

In computer vision, labeling a photo of a cat as “cat” remains valid regardless of whether it was taken 100 years ago or 10,000 years ago, or how many people have seen it. It is always a cat.

**This is data certainty.** The label is eternal. This type of data possesses extremely high **certainty**.

But the rules of the financial market evolve dynamically.

Suppose a model learns a “bullish pattern” (such as specific volume-price coordination) with a very high win rate from historical data.

In backtests, this pattern appears 100 times and rises 80 times, leading the model to label it as “bullish (1).”

But in reality tomorrow, when the same pattern appears, if it encounters sudden macro-policy changes (such as a central bank raising interest rates), the market might crash directly.

For identical K-line input features, the correct historical label was “rise,” while today’s correct label becomes “fall.”

This is the most troublesome aspect of finance: the same input, placed in different time periods, may have shifted distributions:

$$
P_t(X, Y) \neq P_{t+\Delta}(X, Y)
$$

In other words, the joint distribution you used to train the model may no longer apply in the next phase.

This **label ambiguity** causes supervised learning models (like TCN) that rely heavily on historical labels to encounter severe fitting difficulties during training. The model cannot understand why identical features correspond to opposite results.

Furthermore, the market exhibits what Soros called **reflexivity**.

When a prediction model is highly accurate, it inevitably attracts more capital to use the same strategy.

When large amounts of capital issue the same trading signals simultaneously, the market’s **microstructure** is disrupted.

Expected profit margins are instantly exhausted, causing the strategy itself to fail. **Model effectiveness diminishes marginally as capital size and user count increase.**

### The same pattern may not hold the same meaning in different time periods. Once the market environment changes, historical experience may immediately become invalid.

---

## Dilemma 2: Model Time Windows vs. Natural Calendars: TCN Cannot Read Human “Calendars”

In TCN architecture, dilated convolution is ingenious, exponentially expanding the receptive field to capture long-range dependencies.

However, this rigorous mathematical design appears too rigid and mechanical in financial practice.

Human economic activities and trading habits follow **natural calendars** (e.g., monthly macroeconomic data releases, quarterly earnings disclosures, weekly fund settlements).

But TCN’s dilation factors increase in powers of 2 (2, 4, 8, 16, 32, 64...).

This means the model can only construct observation windows of 32 days or 64 days, **preventing it from precisely aligning with natural monthly cycles in the real world, such as January 1st to January 31st.**

This may not seem serious on paper, but it becomes awkward in actual trading.

For example, the last trading day before the Spring Festival and the first trading day after are not just two ordinary K-lines in a human trader’s mind; between them lies a complete re-pricing of news, sentiment, and capital expectations.

In the model’s eyes, if you do not handle it additionally, it still sees only “two adjacent points on the time axis.”

A more critical issue lies in handling **non-trading days**.

China A-shares have 5 trading days per week, interspersed with weekends, and may also encounter week-long closures during the Spring Festival.

Traditional human traders analyzing “weekly lines” automatically filter out gaps caused by non-trading days.

However, TCN mechanically traces back a fixed number of historical data points. It often forcibly stitches together pre-holiday sentiment with post-holiday gaps caused by accumulated news, disrupting the true logical structure of the time series.

Additionally, because TCN absorbs all data points within the window, it incorporates a large amount of intraday random fluctuations (retail sentiment, noise from capital博弈) into its calculations.

**In financial markets with extremely low signal-to-noise ratios, valuable trend signals are often drowned out by this massive noise.**

### More financial data is not always better. When windows are filled with too much noise, models are more likely to learn incorrectly.

---

## Dilemma 3: The “Shortcuts” and Feature Dependence of Tree Models (XGBoost)

Due to deep learning’s high requirements for data signal-to-noise ratios, many quantitative researchers turn to tree models (such as XGBoost or LightGBM), which perform excellently on traditional tabular data.

If you take the shortcut of feeding the past 10 days of closing prices directly into XGBoost to predict the 11th day’s price, you will find that the model’s Loss (error) drops significantly, and the prediction curve almost perfectly overlaps with the real curve!

If you look closely, you will see the model playing a very sly little trick: **it simply treats yesterday’s closing price as today’s predicted value.**

Often, what it has learned is actually:

$$
\hat y_t \approx y_{t-1}
$$

This feeling is somewhat like a student cheating on an exam by copying the line before the standard answer. The score looks good, but the brain learned nothing.

Many “suspiciously stable” good results in backtests are essentially of this nature.

Because most stocks fluctuate less than 1% in a single day, predicting “today equals yesterday” is mathematically the solution with the smallest error. But this is useless for trading where you want to make money.

### Low prediction error does not equal strategy profitability. Many “beautiful results” are simply the model learning to take shortcuts, rather than learning to trade.

Therefore, when using tree models, you **must rely on strong feature engineering**.

You need to manually mine factors: momentum factors (past 20-day gains), valuation factors (PE below 10), technical factors (MACD golden cross)... XGBoost’s strength lies in helping you find non-linear combinations of these factors (e.g., win rates are high only when low valuation and high momentum appear simultaneously).

But this still does not break out of the “supervised learning” framework.

It is still afraid of noise and still afraid of sudden speeches from the Federal Reserve.

Crucially, if your features are mined incorrectly (e.g., accidentally including look-ahead bias), even the strongest tree model is useless.

---

## Evolutionary Direction: Reinforcement Learning (RL)

Facing markets full of noise and deception, academia and frontier institutions are now turning their attention to **Reinforcement Learning (RL)**.

Why reinforcement learning? Because its logic resembles that of real traders most closely.

Supervised learning (TCN / XGBoost) is a nerd, constantly obsessing: “Will it rise or fall tomorrow? Give me a definite label!”

But reinforcement learning is a veteran. Its goal is not to guess tomorrow’s direction, but: **“Did my account balance increase after buying and holding for 30 days?”**

It does not need you to tell it whether each day’s operation was right or wrong; it only looks at the final **long-term return (Reward)**.

Even if the stock crashes for a few days in between, as long as the total return after 30 days is positive, the model will remember that “the holding strategy at that time was correct.”

This characteristic gives reinforcement learning strong immunity to short-term noise in the financial market. It does not dig into dead ends but is responsible only for final profits and losses.

This fault-tolerance mechanism makes reinforcement learning more resilient to short-term market noise and random fluctuations. It no longer obsesses over local prediction accuracy but is responsible for the global capital curve.

---

## Real-World Barriers: Capital, Computing Power, and Market Rules

Even if an excellent prediction model is developed, turning it into actual returns involves far more than just “prediction accuracy.”

**The Curse of Capital Size**

   In backtests, you assume your buy orders do not affect stock prices. But if you hold 1 billion in capital, even if you just want to build a base position, your buy orders will instantly pull the stock to the daily price limit.
   
   Your model issues a buy signal, but your capital size personally destroys the profit margin of that signal. This is why many high-frequency strategies have very small capacity: they work with millions, but lose money with tens of millions.

**Can You Compete with Top Institutions’ Computing Power and Talent?**

   Core researchers at OpenAI earn tens of millions of dollars in annual salary plus shares.
   
   Top quantitative hedge funds (such as Renaissance Technologies, Two Sigma) recruit the best mathematicians and physicists in the United States.
   
   As an individual developer, the graphics cards you use and the open-source models you run may be like millet and rifles facing a dimensional strike in front of them.

**The End of Profit-Making Is Often “Rule Arbitrage”**

   Often, large institutions do not make money because their models are smarter, but because they exploit institutional loopholes.
   
   For example, early short-selling rules: institutions could borrow high-quality securities and short-sell them on the day they pulled up the stock price, achieving risk-free T+0 arbitrage; while retail investors could not even borrow securities.
   
   Later, regulators patched this loophole, and such strategies died instantly.
   
   **In this market, those who can make money stably over the long term are often those who understand the rules best, not those who write the best code.**

---

## Summary

This postscript is not meant to dampen your spirits, but to help you avoid some of the detours of “why does the curve look so good, but why does it change face when going live?”

It is not to deny the value of AI in quantitative finance, but to pull expectations back to a more honest position.

Whether TCN, XGBoost, or reinforcement learning, they are excellent tools for processing complex data, but far from a “universal key” for one-and-done success in the financial market.

### What truly determines whether a strategy survives is often not how new the model name is, but how deeply you understand noise, rules, and risk control.

Mastering deep learning algorithm principles gives you the qualification to sit at the quantitative table;

But what determines whether a strategy can survive in the real market and allow you to keep winning at the table is often the handling of data signal-to-noise ratios, the understanding of market microstructure and trading rules, and strict control over risk and capital management.

Start with small capital. Do not rush to add leverage. Models look smart in backtests, but what really leaves a lasting impression is often those unreasonable drawdowns in live trading.

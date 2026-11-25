---
title: "AI Options Trading: Finding Mispriced Skew Without Code"
date: 2025-10-17
slug: en/posts/factor-strategy/mispriced-option
tags: [Options Trading, AI, Volatility Skew, Vertical Spreads]
excerpt: "A no-code workflow for using AI to spot mispriced options through volatility skew, IV/RV mismatch, and momentum, then trade the edge with vertical spreads."
lang: en
translation_of: posts/factor-strategy/mispriced-option
auto_translated: true
source_sha: 0417e533ca8588648957c8517334fcab8d30040c
cover: "https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main/images/slidev/landscape/bakery/17.jpg"
---

This article explains how to use **AI to find mispriced options** and how to trade them. It was published just yesterday and has already received more than 1.1k upvotes. It is well worth reading. The point is not the strategy itself, but how AI can make complex options trading more accessible. Pay attention to the prompts in the screenshots; translating them is not difficult.

!!! attention
    This article is translated from a blog post by PandaMcGee3. You can find the original text and contact the author here: [PandaMcGee3](https://www.reddit.com/r/options/comments/1o7prtk/my_method_on_making_money_trading_mispriced/).

    Reposting does not mean we endorse the views expressed here. All rights to this article belong to the original author. The first person in the text below is the original author.

I have been trading options for about three years. For most of that time, I was essentially gambling. I would see something interesting on Reddit or Twitter, buy cheap calls, and pray for a 10x return. I would lose money, win some back, and lose again. The usual retail-trader cycle.

About six months ago, I got tired of the guesswork and decided to actually learn the math behind option pricing. Slowly, I started building my own strategies, and with the help of **artificial intelligence**, I can confidently say that my profitability is now quite good. More importantly, I finally feel like I have a reasonably deep understanding of the options market.

This is the article I wish I had seen when I started trading options. It covers the strategy I currently use, along with some more basic concepts. If you are more experienced, feel free to skip parts of it.

## What Is Volatility Skew (and Why Does It Exist?)

Think of option pricing as Las Vegas setting odds for the NBA Finals. The sportsbook starts with expert projections, then adjusts the odds as the season progresses and betting volume increases. Options work in much the same way: market makers use the Black-Scholes model as a baseline, then prices adjust to market realities.

The key point: **Black-Scholes assumes implied volatility should be constant across all strike prices**. In theory, a far out-of-the-money call and an at-the-money call should have the same implied volatility because they are claims on the same stock.

**But reality is different.** Out-of-the-money options consistently have higher implied volatility (IV) than at-the-money options. Plot that curve and you get volatility skew. I know what you are thinking: is that not normal? After all, odds should change as the season progresses, right? You are right. This is completely normal market behavior.

**Our opportunity arises when fear or greed pushes that tendency to an extreme.** When market makers mark prices higher because everyone is panic-buying puts or buying calls for fear of missing out, you see an abnormally rich skew. That is exactly what we are looking for.

![Actual volatility skew in SPY versus Black-Scholes. Notice that far OTM options are priced much higher than theory would predict.](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017153712.png)


## How Do You Find Options with Significant Skew?

Not all skew is created equal. As I mentioned, most skew is completely normal and usually fairly priced. The key is to have a system or criteria that helps you identify more significant or abnormal skew consistently.

!!! attention
    Before you start prompting AI, make sure it has real, up-to-date market data. To do this, you can use an AI with built-in market data such as Xynth, or download data from TradingView or Polygon and upload the CSV file to ChatGPT or Claude. Either approach works.


### Skew Z-Score Below -2.0

This compares the current skew with the stock's historical average. A z-score of -2.0 means the skew is two standard deviations away from normal, which is statistically rare and more likely to revert. In short: how mispriced is the current skew relative to its historical average?

![Prompt](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017155026.png)



![Chart report](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017155826.png)


![Detailed analysis](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017155934.png)

### IV/RV Mismatch

Compare current IV with RV—realized volatility—that is, the move the market expects the stock to make versus how the stock has actually behaved recently:

1. OTM strikes: implied volatility (IV) should be significantly higher than realized volatility → overpriced.
2. ATM strikes: IV should be at or below realized volatility → fairly priced.
   
When both conditions hold, you have an expensive option and a cheap option. That is your spread.

![Prompt](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017160140.png)

![Chart report](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017160215.png)


![Detailed analysis](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017160719.png)

### Momentum Confirmation

This tells you the direction of the trade:
1. Positive momentum + call skew → buy a call spread (buy ATM call, sell OTM call).
2. Negative momentum + put skew → buy a put spread (buy ATM put, sell OTM put).

![Prompt](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017160831.png)
![Chart report](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017160917.png)
![Detailed analysis](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017160943.png)

## The Trade: Vertical Spread

Once you have found significant skew, this is how you want to set up the trade. I mostly do bull call spreads because I do not like shorting, but you can presumably try the opposite as well:

1. Buy the ATM option (fairly priced, ~50 delta).
2. Sell the OTM option (overpriced, ~10-25 delta).

![Trade prompt](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017161137.png)

![Backtest](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017161210.png)

![Detailed analysis](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017161335.png)

!!! attention
    These images are examples I saw in a Xynth chat. In this trade, the score was only 68/100, mainly because the ATM option was already overpriced, so the spread did not offer much profit potential. The concept remains the same, though. Feel free to adjust the variables in the prompt and widen your scan, running this scanner on more stocks every day or even every hour.


## Why Use a Vertical Spread?

If you have read this far, you probably realize that the point of this strategy is not pure directionality. It is a relative-value play—a fancy way of saying you are simultaneously buying something cheap and selling something expensive.

You are not just betting that the stock will go up or down; you are betting that the pricing relationship between the two options is out of balance and will eventually normalize.

In addition, if the stock makes a sharp move, your long option also protects you. You are not exposed to unlimited risk on either side.

## Results

I have been running this strategy for about two months, so take these numbers with a grain of salt—it is still early.

Current statistics:
1. Win rate: ~38%
2. Average return per winning trade: ~250%
3. Average loss per losing trade: ~60%
4. Equity curve: net positive overall, despite more losing trades than winners

This strategy is inherently asymmetric. I have had trades return 300-400% in a few weeks, and other trades lose 50-70% just as quickly. But if you win 4 out of 10 trades with a 3-4x return, that easily covers the 6 losses.

<hr>

For more quantitative trading concepts such as skew, the 24-lesson quantitative trading course covers them systematically.

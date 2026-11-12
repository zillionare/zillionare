---
title: "Finding Mispriced Options with AI: No Code Required"
date: 2025-10-17
slug: en/posts/factor-strategy/mispriced-option
tags: [Options Trading, AI, Volatility Skew, Vertical Spreads]
excerpt: "A practitioner's guide to using AI to surface mispriced options — skew z-scores below −2, IV/RV mismatch, momentum confirmation — then a vertical spread to trade the edge."
lang: en
translation_of: posts/factor-strategy/mispriced-option
auto_translated: true
source_sha: 9a2fd578ed96951f8def75d3ff9ca70fcba6df53
cover: "https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main/images/slidev/landscape/bakery/17.jpg"
---

This post covers **using AI to find mispriced options** and how to trade them. It went up just yesterday and already has over 1.1k upvotes. Well worth a read. The point isn't the strategy itself — it's how AI can make options trading, normally a fairly complex thing to participate in, much more accessible. Pay attention to the prompts in the screenshots; translating them isn't hard.

!!! attention
    This article is a translation of a blog post by PandaMcGee3. You can find the original post and contact the author at [PandaMcGee3](https://www.reddit.com/r/options/comments/1o7prtk/my_method_on_making_money_trading_mispriced/).

    Reposting does not mean we endorse the views expressed here. All rights to this article belong to the original author. The first person "I" throughout refers to the original author.

I've been trading options for about three years. For basically all of that time, I was gambling — buying cheap calls because I saw something promising on Reddit or Twitter, then praying for a 10x. Lose money, win it back, lose it again. Standard retail-trader behavior.

About six months ago I got tired of the guessing game and decided to actually learn the math behind option pricing. Slowly I started building my own strategies, and with help from **artificial intelligence** I can now say with confidence that my profitability is pretty solid. More importantly, I finally feel like I have a genuinely deep understanding of the options market.

This is the article I wish I'd had when I started my options journey. It covers the strategy I currently use, plus some more foundational concepts. If you're more experienced, feel free to skip parts.

## What is volatility skew (and why does it exist)?

Think of option pricing like Vegas setting odds on the NBA Finals. The bookmaker starts from expert projections, then adjusts the odds as the season progresses and betting volume builds. Options work much the same way: market makers anchor to Black-Scholes, then prices get adjusted to real-world conditions.

The key point: **Black-Scholes assumes implied volatility should be identical across all strikes.** In theory, a far out-of-the-money call and an at-the-money call should carry the same implied volatility, since they're bets on the same stock.

**Reality disagrees.** Out-of-the-money options consistently trade at higher IV than ATM options. Plot that curve and you get the volatility skew. I know what you're thinking — isn't that just normal? After all, odds should shift as the season goes on, right? You're right, this is entirely normal market behavior.

**Our opportunity appears when fear or greed pushes that tendency to an extreme.** When market makers mark prices up because everyone is panic-buying puts or FOMO-buying calls, you see abnormally rich skew. That's exactly what we're hunting for.

![SPY's actual volatility skew versus Black-Scholes: far OTM options are priced much higher than theory predicts](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017153712.png)


## How do you find options with significant skew?

Not all skew is created equal. As I said, most skew is perfectly normal and usually priced fairly. What you need is a system — a set of criteria — that helps you identify the more extreme, anomalous skew consistently.

!!! attention
    Before you start prompting an AI, make sure it has real, up-to-date market data. You can use an AI with built-in market data like Xynth, or download data from TradingView or Polygon and upload the CSV to ChatGPT or Claude. Either approach works.


### Skew Z-Score Below -2.0

This compares current skew against the stock's historical average. A z-score of -2.0 means skew sits two standard deviations from normal — statistically rare, and more likely to revert. In short: how far off is the option chain's current pricing relative to its historical average?

![Prompt](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017155026.png)



![Chart report](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017155826.png)


![Detailed analysis](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017155934.png)

### IV/RV Mismatch

Compare current IV against RV — realized volatility, i.e. what the market thinks the stock will do versus what it has actually been doing:

1. OTM strikes: IV should be significantly higher than realized volatility → overpriced
2. ATM strikes: IV should be at or below realized volatility → fairly priced
   
When both conditions hold, you're looking at an expensive option and a cheap one. That's your spread.

![Prompt](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017160140.png)

![Chart report](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017160215.png)


![Detailed analysis](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017160719.png)

### Momentum confirmation

This tells you which direction to trade:
1. Positive momentum + call skew → buy a call spread (buy the ATM call, sell the OTM call)
2. Negative momentum + put skew → buy a put spread (buy the ATM put, sell the OTM put)

![Prompt](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017160831.png)
![Chart report](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017160917.png)
![Detailed analysis](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017160943.png)

## The trade: vertical spreads

Once you've found significant skew, here's how to structure it. I mostly run bull spreads only, because I don't like shorting, but presumably you can try the mirror image:

1. Buy the ATM option (fairly priced, ~50 delta)
2. Sell the OTM option (overpriced, ~10-25 delta)

![Trade prompt](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017161137.png)

![Backtest](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017161210.png)

![Detailed analysis](https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251017161335.png)

!!! attention
    These screenshots are examples I saw in the Xynth chat. In this trade the score was only 68/100, mainly because the ATM option was already overpriced, so the spread doesn't leave us much profit potential. The concept is unchanged though. Feel free to tweak the variables in the prompt and widen the scan — run it on more tickers every day, or even every hour.


## Why vertical spreads?

If you've read this far, you've probably realized the point of this strategy isn't pure direction — it's a relative-value play, which is a fancy way of saying you buy something cheap and sell something expensive at the same time.

You're not just betting that the stock goes up or down; you're betting that the pricing relationship between two options is out of whack and will eventually normalize.

On top of that, if the stock moves violently, your long option covers you. You're not carrying unlimited risk on either side.

## Results

I've been running this for about two months, so take these numbers with a grain of salt — it's early.

Current stats:
1. Win rate: ~38%
2. Average return per winning trade: ~250%
3. Average loss per losing trade: ~60%
4. Net equity: still up overall, even though losses outnumber wins

The nature of this strategy is asymmetric. Some trades return 300-400% within a few weeks; others lose 50-70% just as fast. But winning 4 out of 10 trades at 3-4x easily covers the 6 losers.

<hr>

More quantitative trading concepts like skew are covered systematically in 量化24课 (Quantitative 24 Lessons).

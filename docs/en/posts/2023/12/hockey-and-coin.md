---
title: "Teams vs. Coins Factor: Sports Betting Meets Asset Pricing"
date: 2023-12-23
slug: en/posts/factor-strategy/hockey-and-coin
tags: [Behavioral Finance, Factor Investing, Asset Pricing]
excerpt: "The Teams and Coins factor comes from Yale's Tobias Moskowitz and his September 2021 paper 'Asset Pricing and Sports Betting,' linking sports-betting behavior to momentum and reversals in markets."
lang: en
translation_of: posts/factor-strategy/hockey-and-coin
auto_translated: true
source_sha: 2e5c1108b67b6f3edf8d65a405c1f86282bcf93d
---

![R50](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/12/tobias-moskowitz.png)

The Teams and Coins factor traces back to a September 2021 paper by Yale professor Tobias Moskowitz. Since its release, it has earned more than 14 citations. The paper is titled *Asset Pricing and Sports Betting*.

<!--more-->

Moskowitz starts with a simple observation: when people toss a coin and get heads, they tend to call tails next time; yet when a new sports season kicks off, they tend to bet that last season's champion will win again. Why the difference?

It comes down to knowability in behavioral finance. People understand a coin toss quite well — the odds are known and well-defined — so they lean on that knowledge and expect a reversal on the next flip.

When a new season starts, by contrast, asking who will win the championship is a low-knowability question. Fans know little about the new rosters, new players, and how well teams will gel, so they fall back on track records — and naturally pick last season's champion.

!!! tip
    The championship-team effect is very common in fund investing. For example, investors often pile into products run by last year's top-performing public fund manager, whether it's an existing fund or a new launch. That quickly balloons assets under management, the fund becomes too big to maneuver, underperforms the following year, and the champion curse strikes. For star managers, momentum and reversal are just two sides of the same cycle.

Moskowitz argues that if information about an asset is knowable, it is in coin mode — a reversal is likely next; if the information is unknowable, it is in team mode — momentum persists.

How do you judge whether information is knowable? Moskowitz suggests looking at whether a company has issued an earnings pre-announcement: once it does, knowability rises and investors have a much clearer view of where it is headed.

Experienced investors will immediately recognize the China A-shares version of this: **isn't this just "good news exhausted is bad news; bad news exhausted is good news" — the classic sell-on-good-news?** That's exactly what it is, except Moskowitz gave the phenomenon a theoretical framework.

How can you turn it into an investable factor? Under Moskowitz's original definition, you need to extract earnings pre-announcement data. You can get it for free with AKShare:

```python
import akshare as ak

stock_yjyg_em_df = ak.stock_yjyg_em(date="20230930")
print(stock_yjyg_em_df[["股票简称","预测指标","业绩变动幅度"]])
```

Note that the `date` argument follows a strict pattern — you can only use quarter-end dates, i.e., 0331, 0630, 0930 and 1231 prefixed with the year. Any other date will raise an exception.

That gives you sample output like this:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/12/akshare_yjyg.png)

As you can see, each announcement carries its own date, so the data can be considered PIT-compliant.

To build the factor, you can take the return over 1, 3, 5, 8, 10, 13 periods starting the day after the announcement date, and evaluate the factor. Factor evaluation follows the standard workflow — you can use quantpian's Alphalens library, which we covered in detail with examples in Lesson 15, so we won't repeat it here.

### Quiz

This note mentioned the term PIT-compliant — do you know what it means? PIT data is our first line of defense against look-ahead bias at the data source. Leave a comment if you'd like to learn more!

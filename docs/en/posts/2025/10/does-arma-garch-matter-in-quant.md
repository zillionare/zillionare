---
title: "Why ARMA/GARCH Fail in Quant Trading: A Time-Series Reality Check"
date: 2025-10-10
slug: en/posts/career-figure/does-arma-garch-matter-in-quant
tags: [Time Series, Quantitative Trading, ARMA, GARCH]
excerpt: "ARMA and GARCH models require stationarity, which stock prices lack. This article explains why time-series models used in other fields often fail in quantitative trading due to market reflexivity and structural breaks."
lang: en
translation_of: posts/career-figure/does-arma-garch-matter-in-quant
auto_translated: true
source_sha: 38eb821d507976ef07ff0c0bffba6cb84964eb72
cover: "https://fastly.jsdelivr.net/gh/zillionare/imgbed2@main/images/slidev/landscape/bakery/10.jpg"
---

Securities trading data is a classic example of time-series data, and ARMA (AutoRegressive Moving Average) and GARCH (Generalized AutoRegressive Conditional Heteroskedasticity) are two widely used time-series models. But how should we evaluate their actual role in quantitative trading?

**The Bottom Line:** The essence of time-series research is studying "how data evolves over time." Simply knowing ARMA and GARCH is not enough. In fact, these models are only applicable in specific (often artificially constructed) scenarios within quantitative trading.

Time-series data can exhibit trends, seasonality, periodicity, stationarity, and autocorrelation. ARMA and GARCH, however, rely on the premises of **stationarity** and **autocorrelation**. If a time series only shows trends, seasonality, or periodicity without stationarity or autocorrelation, these methods are not suitable for analysis.

## 01 Market Data Often Violates Model Premises

In tradable assets, stocks typically exhibit **trends**. Over the lifespan of a nation, a stock market’s total capitalization tends to grow linearly with GDP—a relationship known as the Buffett Indicator (or market capitalization-to-GDP ratio). Consequently, stock prices are generally **non-stationary**.

Of course, we can construct stationary time series by pairing two stocks—this is the foundation of **pairs trading**.

Additionally, we can approximate asset returns (e.g., stocks, futures) at high frequencies (such as minute-level bars) as stationary and autocorrelated. In such cases, ARMA can be used for short-term price forecasting. This might explain why some believe that simply knowing ARMA/GARCH is sufficient for **high-frequency trading**.

In summary, while ARMA/GARCH have a niche in quantitative trading, they are not a universal solution, nor do they work reliably in all contexts.

## 02 Time-Series Models Are Not Universally Applicable to Securities

Consider another example: Facebook’s popular time-series library, **Prophet**. If you search for time-series tools, you will likely encounter it.

Although Prophet is designed for forecasting, it is generally unsuitable for securities trading. Why?

Prophet is built on an additive model (trend + seasonality + holiday effects). It works well for business scenarios like sales forecasting, web traffic, or user growth, especially for data with strong seasonality, missing values, or outliers.

While stock markets do have seasonal factors, they are not as explicit as the seasonality seen in commodity prices, consumer goods, or sales volumes. Therefore, using Prophet for stock trading is largely ineffective. The seasonal effects in securities trading differ significantly from consumer markets and are much weaker.

Thus, not all time-series models are applicable to securities trading. The same logic applies to ARMA and GARCH.

## 03 Unique Characteristics of Time-Series in Securities Trading

In my view, **time-series** analysis in **quantitative trading** is both similar to and distinct from time-series analysis in other fields. We cannot simply copy algorithms, rules, or function libraries from other domains.

The fundamental reason is that natural time-series patterns, once established, remain fixed and drift-free for long periods. In contrast, in securities markets, prices are determined by traders. Traders predict "patterns," but in the process of exploiting these patterns, they alter them. Therefore, in securities trading, patterns are constantly emerging and being broken (though some fundamental laws remain unchanged).

Coincidentally, the 2025 Nobel Prize in Physics was announced shortly after I wrote this piece. The prize was awarded to three scholars from the University of California and others for their pioneering work on "achieving macroscopic quantum mechanical tunneling and energy quantization in circuits."

<div style='width:66%;text-align:center;margin: 0 auto 1rem'>
<img src='https://fastly.jsdelivr.net/gh/zillionare/imgbed2@main//images/2025/10/20251009230959.png'>
<span style='font-size:0.8em;display:inline-block;width:100%;text-align:center;color:grey'></span>
</div>

In short, we used to believe that quantum mechanics only operated at the microscopic scale. Schrödinger’s cat was a thought experiment questioning the applicability of quantum mechanics. It raised this question through an apparent paradox. However, we can now say:

Quantum mechanics has no clear macro-micro boundary, as superconducting circuits can reach millimeter scales. It may be time to redesign the Schrödinger’s cat experiment.

However, the author believes that the philosophical concepts underlying quantum mechanics also apply to economics and securities research.

When we discuss prices, we are essentially discussing observations of security prices. These observations are fundamentally completed through trades; without trades, there are no prices.

Moreover, trades themselves interfere with price volatility. Here, we encounter a problem analogous to the Planck scale.

In the physical world, most observations are made via light—specifically, through the collision and reflection of photons with the observed object. However, when the observed object’s scale approaches that of a photon, the act of observation alters the object’s motion. At this point, the object no longer has a definite trajectory, which is the root cause of the **uncertainty principle**.

This theory has a small but significant application in securities trading: If you are trading with small capital, you can predict and exploit patterns without significantly interfering with price movements. If your trading volume is far smaller than the company’s market cap, it is like using a single photon to strike a macroscopic object; it only gathers information about the object without altering its motion.

Therefore, quantitative trading is a paradise for small-capital traders. This is a message for all independent quantitative traders currently on the path or preparing to start.

---
title: "Factor Investing FAQ: From CAPM to Multi-Factor Models"
date: 2026-10-08
cover: "https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/10/20261009145545-cover-articles-course-factor-ml-factor-investing-faq.jpg"
slug: en/articles/course/factor-ml/factor-investing-faq
tags: [Factor Investing, Multi-Factor Models, Machine Learning, Quantitative Trading]
excerpt: "Explore 7 key questions on factor investing origins, CAPM, Alpha, and multi-factor evolution. Understand why machine learning is replacing linear models in quantitative trading."
lang: en
translation_of: articles/course/factor-ml/factor-investing-faq
auto_translated: true
source_sha: 1fc19f9c516b12b369ed6f2a064495826d7aaebd
---

Factor investing posits that asset returns can be decomposed into quantifiable, company-specific factors. By identifying effective factors and combining them appropriately, investors can construct robust investment strategies. This article distills seven of the most frequently asked questions from Chapter 1 ("Introduction") of *Factor Analysis and Machine Learning Strategies*.

## Frequently Asked Questions

### What is Factor Investing and What Problem Does It Solve?

Factor investing is an investment methodology asserting that asset returns can be decomposed into a series of quantifiable factors (such as size, value, momentum, and quality). Researchers seek effective factors that explain future returns and combine them into strategies. This approach originated from Harry Markowitz’s Modern Portfolio Theory (MPT, 1952) and William Sharpe’s Capital Asset Pricing Model (CAPM, 1964)—both are among the seven foundational theories of modern finance. Markowitz and Sharpe jointly received the 1990 Nobel Memorial Prize in Economic Sciences for this work.

### What Is the CAPM Formula and How Are Beta, the Risk-Free Rate, and Market Return Determined?

The CAPM formula is `E(Ri) = Rf + β(E(Rm) − Rf)`: Expected Asset Return = Risk-Free Rate + β × (Market Risk Premium). The determination of the three elements is as follows:

- **Risk-Free Rate (Rf):** Typically derived from government bond yields (matched to the expected holding period; for short-term, highly liquid stocks, the one-year government bond yield is often used).
- **Market Return (Rm):** Often proxied by a corresponding index. For instance, a CSI 300 index-enhanced strategy uses the CSI 300 constituent index. Other common A-share indices include the SSE 50, CSI 500, CSI 1000, and CSI 2000.
- **Beta (β):** Calculated as `β = Cov(Ri, Rm) / Var(Rm)`, measuring a stock’s volatility sensitivity relative to the market. The market’s overall β is 1.0; β < 1 indicates defensive stocks, while β > 1 indicates aggressive stocks. For example, with a market return of 12.4%, a risk-free rate of 0%, and a stock β of 1.1, the expected return is approximately 13.7%.

### What Is Alpha and How Does It Relate to "Factors"?

Alpha was originally introduced by Michael Jensen in his 1968 doctoral dissertation as a performance metric (Jensen’s Alpha): the **residual** of a portfolio’s actual return minus its CAPM-expected return, i.e., excess return: `α = Rp − β(E(Rm) − Rf) − Rf`. As usage evolved, WorldQuant defined Alpha as "trading signals that add value to a portfolio" (the Alpha in the Alpha101 factor library reflects this meaning). The name of the Alphalens framework (Alpha + Lens) also implies "finding Alpha (signals)." Therefore, **factor mining is essentially the search for factors with Alpha**. The two are inextricably linked, and in practice, a strict distinction is usually unnecessary.

### How Did Multi-Factor Models Evolve?

Since CAPM includes only one market risk factor, it cannot fully explain asset returns. The resulting "anomalies" have driven the discovery of numerous new factors:

- **1976:** Stephen Ross published the Arbitrage Pricing Theory (APT), proposing for the first time that security returns should be explained by multiple factors, initiating multi-factor research.
- **1981:** Rolf Banz, analyzing 40 years of NYSE data, discovered that small-cap stocks yielded approximately 0.4% higher monthly returns, establishing the **size factor**.
- **1993:** Fama and French proposed the **three-factor model** (market, size, and value; value is measured by book-to-market ratio or similar metrics like P/B).
- **1993:** Jegadeesh and Titman’s research established the **momentum factor** (the existence of a premium for high-momentum stocks).
- **2015:** Fama and French expanded this to the **five-factor model** (adding profitability and investment factors).
- **2017:** Stambaugh and Yuan proposed a four-factor model including two mispricing factors, summarizing 73 anomalies in the appendix as clues for factor mining.

### What Is the "Factor Zoo" Problem?

As anomaly research accumulates, the number of factors grows explosively (referred to in academia as the "factor zoo"). Analysis of 2023 private equity strategy roadshows indicates that mid-frequency quantitative strategies typically use **over 300 factors**, while some high-frequency strategies report using up to 200,000 factors. The core question随之 arises: among so many features, which provide **independent** information, and which are redundant? How can we find appropriate tools to handle this high-dimensional information and achieve denoising and purification? This is precisely why establishing a **systematic factor analysis framework** (this course uses Alphalens as the core framework) is essential.

### Why Is Machine Learning Replacing Linear Multi-Factor Models?

Traditional multi-factor models primarily rely on linear fitting, which has two significant shortcomings:

1. **Overly Strong Linear Assumption:** The true relationship between factors and returns is often non-linear. Machine learning models, such as neural networks, can theoretically fit any linear/non-linear function, essentially learning a set of factor weights (parameters).
2. **Stronger Resistance to Overfitting:** Machine learning offers techniques like regularization and cross-validation, enabling the generation of more robust models.

It is important to note that machine learning is not a panacea. In asset management, particularly price prediction tasks, many scenarios still struggle to surpass classic machine learning algorithms—especially ensemble models like **XGBoost and LightGBM**, which remain the most widely used and effective models in quantitative trading.

### What Steps Are Required to Move From a Single Factor to Live Trading?

1. **Factor Analysis and Testing:** Evaluate a factor’s ability to explain future returns under ideal assumptions (no fees, static prices, unlimited liquidity).
2. **Backtesting:** Introduce real-world constraints such as transaction fees, slippage, T+1 settlement, and price limits to verify if the model can generate profits in live trading.
3. **Position Management and Risk Control:** Determine capital allocation and risk management rules.
4. **Live Trading:** Large capital deployments require custom order-splitting/following algorithms (transaction cost models) to minimize market impact.

## How to Start Factor Investing (Learning Path)

1. **Build Foundations:** Python programming + university-level statistics (systematically covered in *Quantitative 24 Lessons*).
2. **Master Tools:** Numpy/Pandas (recommended alongside the free *Numpy and Pandas in Quantitative Trading*).
3. **Learn Factor Analysis:** From factor generation and preprocessing to single-factor testing (regression, IC analysis, layered backtest). Implement manually first, then use Alphalens.
4. **Learn Machine Learning Modeling:** General sklearn tools → cross-validation and hyperparameter tuning → XGBoost/LightGBM strategy examples.
5. **Expand Factor Libraries:** Alpha101, Ta-lib, fundamental, and alternative factors.

The above content systematically covers Chapter 1 ("Introduction") of the [Factor Analysis and Machine Learning Strategies Course](https://www.quantide.cn/articles/course/factor-ml/intro/). The complete syllabus is available at [Course Syllabus](https://www.quantide.cn/articles/course/factor-ml/syllabus/).

## Further Reading

- [Factor Preprocessing FAQ: How to Handle Outlier Clipping, Missing Values, Standardization, and Neutralization](https://www.quantide.cn/articles/course/factor-ml/factor-preprocessing-faq/)
- Markowitz, *Portfolio Selection* (1952); Sharpe, *Capital Asset Prices* (1964); Ross, *The Arbitrage Theory of Capital Asset Pricing* (1976)

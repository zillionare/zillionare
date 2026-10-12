---
title: "Factor Investing FAQ: From CAPM to Multi-Factor Models"
date: 2026-10-08
slug: en/articles/course/factor-ml/factor-investing-faq
tags: [Factor Investing, Multi-Factor Models, Machine Learning, Quantitative Trading]
excerpt: "Why does factor investing stem from CAPM? How do alpha and factors relate? This FAQ clarifies the origins of factor investing, the evolution of multi-factor models, and why machine learning is replacing linear approaches."
lang: en
translation_of: articles/course/factor-ml/factor-investing-faq
auto_translated: true
source_sha: ee8c4c5a711c33dc33ad0a7177ac9f5bba93f125
cover: "https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/10/20261009145545-cover-articles-course-factor-ml-factor-investing-faq.jpg"
---

Factor investing posits that asset returns can be decomposed into quantifiable, company-specific factors. By identifying effective factors and combining them appropriately, investors can construct robust investment strategies. This article distills seven of the most frequently asked key questions from Chapter 1, "Introduction," of *Factor Analysis and Machine Learning Strategies*.

## Frequently Asked Questions

### What is factor investing, and what problem does it solve?

Factor investing is an investment methodology that assumes asset returns can be decomposed into a series of quantifiable factors (such as size, value, momentum, and quality). Researchers seek effective factors that explain future returns and combine them to form strategies. It originated from Harry Markowitz’s Modern Portfolio Theory (MPT, 1952) and William Sharpe’s Capital Asset Pricing Model (CAPM, 1964)—both are among the seven fundamental theories of modern finance, for which Markowitz and Sharpe jointly received the 1990 Nobel Memorial Prize in Economic Sciences.

### What is the CAPM formula, and how are beta, the risk-free rate, and market return determined?

The CAPM formula is `E(Ri) = Rf + β(E(Rm) − Rf)`: Expected Asset Return = Risk-Free Rate + β × (Market Risk Premium). The determination of these three elements is as follows:

- **Risk-Free Rate (Rf)**: Typically derived from government bond yields (matching the term to the expected holding period; for short-term, highly liquid stocks, a one-year government bond yield is often used);
- **Market Return (Rm)**: Often proxied by a corresponding index. For example, a CSI 300 index-enhanced strategy uses the CSI 300 constituent index. Other common indices in China A-shares include SSE 50, CSI 500, CSI 1000, and CSI 2000;
- **Beta (β)**: `β = Cov(Ri, Rm) / Var(Rm)`, measuring a stock’s volatility sensitivity relative to the market. The market’s overall beta is 1.0; β < 1 indicates a defensive stock, while β > 1 indicates an aggressive one. For instance, if the market return is 12.4%, Rf is 0, and a stock’s β is 1.1, the expected return is approximately 13.7%.

### What is Alpha, and how does it relate to "factors"?

Alpha was initially introduced as a performance metric for strategies in Michael Jensen’s 1968 doctoral thesis (Jensen’s Alpha): the **residual** of a portfolio’s actual return minus its CAPM-expected return, i.e., excess return: `α = Rp − β(E(Rm) − Rf) − Rf`. As usage evolved, WorldQuant defined Alpha as "trading signals that add value to a portfolio" (the Alpha in the Alpha101 factor library carries this meaning). The name of the Alphalens framework (Alpha + Lens) also implies "finding Alpha (signals)." Therefore, **factor mining is essentially finding factors with Alpha**; the two are inseparable, and in practice, a strict distinction is usually unnecessary.

### How did multi-factor models develop?

Since CAPM includes only one market risk factor, it cannot fully explain asset returns. The resulting "anomalies" have driven the discovery of numerous new factors:

- **1976**: Stephen Ross published the Arbitrage Pricing Theory (APT), proposing for the first time that security returns should be explained by multiple factors, launching multi-factor research;
- **1981**: Rolf Banz discovered, based on 40 years of NYSE data, that small-cap stocks yielded approximately 0.4% higher monthly returns, establishing the **size factor**;
- **1993**: Fama and French proposed the **three-factor model** (market, size, and value; value is measured by book-to-market ratio or similar metrics like P/B);
- **1993**: Jegadeesh and Titman’s research established the **momentum factor** (high-momentum stocks exhibit a premium);
- **2015**: Fama and French expanded this into the **five-factor model** (adding profitability and investment factors);
- **2017**: Stambaugh and Yuan proposed a four-factor model containing two mispricing factors, summarizing 73 anomalies in the appendix as clues for factor mining.

### What is the "Factor Zoo" problem?

As anomaly research accumulates, the number of factors grows explosively (referred to in academia as the "factor zoo"). An analysis of 2023 private equity strategy roadshows reveals that mid-frequency quantitative strategies typically use **over 300 factors**; some high-frequency strategies report using up to 200,000 factors. The core question thus arises: among so many features, which provide **independent** information, and which are redundant? How can we find appropriate tools to handle this high-dimensional information and achieve denoising and purification? This is precisely why establishing a **systematic factor analysis methodology** (with Alphalens as the core framework in this course) is essential.

### Why is machine learning replacing linear multi-factor models?

Traditional multi-factor models primarily rely on linear fitting, which has two obvious shortcomings:

1. **Overly strong linear assumptions**: The true relationship between factors and returns is often non-linear. Machine learning models, such as neural networks, can theoretically fit any linear/non-linear function, essentially learning a set of factor weights (parameters);
2. **Stronger resistance to overfitting**: Machine learning offers techniques like regularization and cross-validation, enabling the generation of more robust models.

It is important to note that machine learning is not a panacea: in asset management, particularly in price prediction tasks, many scenarios still struggle to surpass classic machine learning algorithms—especially ensemble models like **XGBoost and LightGBM**, which remain the most widely applied and effective models in quantitative trading.

### What steps are required to move from a single factor to a live trading strategy?

1. **Factor Analysis and Testing**: Evaluate a factor’s ability to explain future returns under ideal assumptions (no fees, static prices, unlimited liquidity);
2. **Backtesting**: Introduce real-world constraints such as transaction fees, slippage, T+1 settlement, and price limits to verify if the model can generate profits in actual trading;
3. **Position Management and Risk Control**: Determine capital allocation and risk management rules;
4. **Live Trading**: Large capital requires custom order-splitting/following algorithms (transaction cost models) to minimize the market impact of orders.

## How to Start with Factor Investing (Learning Path)

1. **Build Foundations**: Python programming + undergraduate statistics (systematically covered in *Quantitative Trading 24 Lessons*);
2. **Master Tools**: Numpy/Pandas (recommended to pair with the free *Numpy and Pandas in Quantitative Trading*);
3. **Learn Factor Analysis**: From factor generation and preprocessing to single-factor testing (regression, IC analysis, layered backtests). Implement manually first, then use Alphalens;
4. **Learn Machine Learning Modeling**: General sklearn tools → cross-validation and hyperparameter tuning → XGBoost/LightGBM strategy examples;
5. **Expand Factor Libraries**: Alpha101, Ta-lib, fundamental, and alternative factors.

The above content systematically covers Chapter 1, "Introduction," in the [Factor Analysis and Machine Learning Strategies Course](https://www.quantide.cn/articles/course/factor-ml/intro/). For the complete syllabus, see [Course Outline](https://www.quantide.cn/articles/course/factor-ml/syllabus/).

## Further Reading

- [Factor Preprocessing FAQ: How to Handle Outlier Clipping, Missing Values, Standardization, and Neutralization](https://www.quantide.cn/articles/course/factor-ml/factor-preprocessing-faq/)
- Markowitz, *Portfolio Selection* (1952); Sharpe, *Capital Asset Prices* (1964); Ross, *The Arbitrage Theory of Capital Asset Pricing* (1976)

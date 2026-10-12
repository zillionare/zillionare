---
title: "Factor Preprocessing FAQ: Outliers, Missing Data, Standardization, Neutralization"
date: 2026-10-08
slug: en/articles/course/factor-ml/factor-preprocessing-faq
tags: [Factor Investing, Factor Testing, Quantitative Trading, Factor Preprocessing]
excerpt: "A practical guide to factor preprocessing: handling outliers (3σ, Winsorize, MAD), missing values, distribution adjustments, standardization, and sector/market-cap neutralization."
lang: en
translation_of: articles/course/factor-ml/factor-preprocessing-faq
auto_translated: true
source_sha: a29636a42c70d1e6dcf31c0aa32f040a6048525a
cover: "https://gcore.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/10/20261009145604-cover-articles-course-factor-ml-factor-preprocessing-faq.jpg"
---

The quality of **factor testing** hinges first on preprocessing. This article distills seven critical questions from Chapter 2, "Factor Preprocessing Workflow," of *Factor Analysis and Machine Learning Strategies*, covering factor data sourcing, generation, and the principles and practical nuances of outlier clipping, missing value handling, distribution adjustment, standardization, and neutralization.

## Common Questions

### Where does raw factor data come from? What data should small-capital funds prioritize?

Raw factor data sources include trading data, financial data, alternative data, announcement events, earnings expectations, industry-specific data, shareholder holdings, public fund positions, news sentiment, index constituents, and derivatives.

A key background concept is **crowding effect**: using the same data with identical technical methods often yields similar factors; as more users adopt them, returns get diluted. This is the value source of alternative data (e.g., global weather data for agricultural products, App Store rankings for gaming companies, search trend indices). However, for individual investors or small institutions with limited capital, alternative data often has a poor cost-performance ratio (cheap alternatives are usually already widely used). **It is recommended to focus primarily on market data and financial data**, discovering new value through algorithmic improvements or cross-domain integration. When Banz discovered the size factor, the data he cited had already existed for over 40 years. In markets with poor data quality, it is even more crucial to focus on price-volume factors, as all information ultimately reflects in prices.

### What is the "warm-up period" for technical indicators?

Technical indicator factors often have a warm-up period due to window calculations: for example, calculating a 6-day RSI results in `NaN` for the first 6 rows. More importantly, however, **the initial `win × 3` records (including `NaN`) of an RSI are often inaccurate**—not just the `NaN` portion. If factor evaluation requires high precision, you should set the entire warm-up period to `NaN` when extracting factors and treat it as missing data.

### What are the methods for correcting outliers, and when should each be used?

Outliers commonly appear in financial data (e.g., net profit growth rate exploding when the denominator approaches zero). Failing to correct them significantly interferes with neutralization regressions and metrics like IC. There are three common methods:

1.  **Mean-Standard Deviation Method (3σ Method)**: Pulls data deviating more than 3 standard deviations from the mean back to the boundary, implemented using `np.clip`. **Note**: With small sample sizes, individual outliers can significantly affect the standard deviation, causing the 3σ rule to fail (all points fall within the boundaries);
2.  **Percentile Method (Winsorization)**: Sorts data and pulls tail data back based on percentiles. `scipy.stats.mstats.winsorize` can implement this directly, supporting symmetric (e.g., `[0.1, 0.1]`) and asymmetric Winsorization, with results stored in the `.data` attribute;
3.  **Median Absolute Deviation Method (MAD Method)**: Pulls values deviating by several times the MAD from the median. The absolute median deviation is `MAD = median(|Xi − median(X)|)`; taking a scaling factor of k ≈ 1.4826 makes MAD consistent with the standard deviation of a normal distribution. At this point, **3×MAD approximates 5×standard deviation**. MAD is more robust to outliers and is a commonly used solution in practice.

### How should missing values be handled? Delete, fill, or exclude?

More than **70%** of fundamental factors across companies have missing values (Bryzgalova et al.'s study on 45 popular characteristic factors in asset pricing). The general practice is to **directly delete rows with missing values**, keeping only valid values; replacement is considered only when retention is necessary:

-   **Financial factors**: **Carry forward the previous period's factor value** (Point-in-Time, PIT, basis);
-   **Other factors**: Replace with cross-sectional median, similar company values, or interpolation (pandas' `fillna` / `ffill` / `bfill` / `interpolate`);
-   If the missing ratio is too high, leading to insufficient coverage, consider excluding that factor or data source.

Two common pitfalls: ① Filling (especially with mean/median) alters the data distribution; **the order of outlier clipping and missing value handling matters, and different orders may yield different final results**; ② The pandas `fillna(method=...)` syntax is deprecated; use `ffill` / `bfill` directly.

### When is distribution adjustment (e.g., log transformation) necessary?

Ideally, factor exposure on the cross-section should approximate a normal distribution. When significantly deviating, you can use **logarithmic or square-root transformations** before use. A typical example is the China A-shares market-cap factor: with many small-cap stocks and a few with huge market caps, the raw distribution is right-skewed, leptokurtic, and fat-tailed. **Taking the logarithm brings it close to normal**. The approach is to first infer the distribution (e.g., plot a histogram) and then decide whether to adjust.

### When is standardization required? Is it needed for single-factor testing?

Standardization (z-score, `Z = (x − μ) / σ`) aims to **eliminate dimensional differences between factors, allowing fair comparison of weights in linear models**. Whether it is needed depends on the downstream model:

-   **Single-factor testing does not require it**: Alphalens does not standardize factors, nor does it require standardization;
-   **Linear regression models must use it**;
-   **Tree models (decision trees, XGBoost, LightGBM) are insensitive to dimensions and do not need it**.

Prerequisite: Standardization assumes factors approximate a normal distribution; if this assumption does not hold, direct standardization is meaningless (use statistical tests to judge). Also note that z-score following N(0,1) means a mean of 0 and standard deviation of 1—not that values are in (0,1), but that the probability of |Z| falling in [1,2] is less than 5%, and greater than 2 is less than 0.3%.

### What is neutralization? How are sector and market-cap neutralization performed?

Many factors have systematic differences due to industry or market cap—these differences do not reflect company quality but rather industry disparities and economic cycles. Without neutralization, "pseudo Alpha" arises: for example, using a low P/E factor for stock selection in 2022 would select almost entirely bank stocks, earning industry beta rather than stock-selection Alpha.

**Two common approaches for sector neutralization**:

1.  **Industry Mean Difference Method (demean)**: `ε = Y − Ȳ_industry`, i.e., subtracting the industry factor mean from the individual stock's factor value;
2.  **Dummy Variable Regression Method**: `Y = β × Industry + α + ε`, performing linear regression using industry dummy variables (0/1), **taking the residual ε as the neutralized factor**; this approach can be combined with market-cap neutralization.

**Market-cap neutralization** uses a regression form: `Y = β × log(market cap) + α + ε`, also taking the residual. Industry dummy variables and log(market cap) can be concatenated into the same design matrix to perform double neutralization in one step (keep `fit_intercept` generally).

Selection advice: Research by Ehsani et al. (2022) suggests that **long-short hedged investors should perform sector neutralization, while pure long investors should avoid it**. Also, distinguish between: market-cap **distribution adjustment** (log transformation) applied to individual market caps, requiring no overall sample; market-cap **neutralization** is the process of subtracting the mean/regressing to take residuals—these are different operations.

## How to Perform Factor Preprocessing (Standard Steps)

Taking a 10-day momentum factor as an example, the recommended preprocessing order is:

1.  **Outlier Clipping**: Use 3×MAD truncation (`mad_clip`)—operate on the cross-section (row) direction, processing within the same day to avoid look-ahead bias;
2.  **Missing Value Handling**: For cross-sections with missing rates below a threshold (e.g., 20%), fill with the cross-sectional median; otherwise, delete that period. Exclude标的 with excessive missing data. **Missing values must be handled first, otherwise subsequent standardization and neutralization cannot be calculated**;
3.  **Distribution Adjustment** (as needed): For factors significantly right-skewed (e.g., market cap), take the logarithm or square root;
4.  **Standardization** (as needed): z-score standardization on the cross-section—required for linear models, not for tree models or single-factor testing;
5.  **Neutralization**: Construct a design matrix of [log(market cap) + industry dummy variables], perform period-by-period regression to take residuals, obtaining the neutralized clean factor.

This workflow corresponds one-to-one with the `get_clean_factor` implementation in Chapter 3's single-factor testing of this course, and is also the foundation for understanding Alphalens' preprocessing logic.

## Further Reading

-   [Factor Testing FAQ: Regression Methods, IC Analysis, and Layered Backtest Selection](https://www.quantide.cn/articles/course/factor-ml/factor-testing-faq/)
-   Bryzgalova et al., *Missing Financial Data* (2022); Ehsani, Harvey, Li, *Is Sector-neutrality in Factor Investing a Mistake?* (2022)

The above content systematically covers Chapter 2, "Factor Preprocessing Workflow," in the [Factor Analysis and Machine Learning Strategies Course](https://www.quantide.cn/articles/course/factor-ml/intro/). The complete syllabus is available at [Course Syllabus](https://www.quantide.cn/articles/course/factor-ml/syllabus/).

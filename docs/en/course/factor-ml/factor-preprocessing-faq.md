---
title: "Factor Preprocessing FAQ: Outliers, Missing Values, Standardization, Neutralization"
date: 2026-10-08
cover: "https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/10/20261009145604-cover-articles-course-factor-ml-factor-preprocessing-faq.jpg"
slug: en/articles/course/factor-ml/factor-preprocessing-faq
tags: [Factor Investing, Factor Testing, Preprocessing, Neutralization]
excerpt: "Learn the correct order for factor preprocessing: outlier clipping, missing value handling, distribution adjustment, standardization, and sector/market-cap neutralization."
lang: en
translation_of: articles/course/factor-ml/factor-preprocessing-faq
auto_translated: true
source_sha: 740b9bf22035076c392980ee376d8a976c21e46b
---

The quality of **factor testing** hinges on preprocessing. This article distills seven critical questions from Chapter 2, "Factor Preprocessing Workflow," of *Factor Analysis and Machine Learning Strategies*, covering data sourcing, generation, and the principles and practicalities of outlier clipping, missing value handling, distribution adjustment, standardization, and neutralization.

## Frequently Asked Questions

### Where does raw factor data come from? What data should small funds prioritize?

Raw factor data sources include: trading data, financial data, alternative data, announcement events, earnings expectations, industry-specific data, shareholder holdings, public fund positions, news sentiment, index constituents, and derivatives.

A key background concept is **crowding**: using identical data with the same technical methods often yields similar factors. As more users adopt them, returns get diluted—this is the value source for alternative data (e.g., global weather data for agricultural products, App Store rankings for gaming companies, search trend rankings). However, for individual investors or small institutions with limited capital, alternative data offers poor cost-performance ratios (cheap alternatives are often already widely used). **We recommend focusing primarily on market data and financial data**, discovering new value through algorithmic improvements or cross-domain integration. When Banz discovered the small-cap factor, the data had already existed for over 40 years. In markets with poor data quality, focusing on **price-volume factors** is even more critical, as all information ultimately reflects in prices.

### What is the "warm-up period" for technical indicators?

Technical indicator factors often suffer from a warm-up period due to window calculations: for example, calculating a 6-day RSI results in `NaN` for the first 6 rows. More importantly, **the first `win × 3` records (including `NaN`) are often inaccurate**—not just the `NaN` portion. If your factor evaluation requirements are high, you should set the entire warm-up period to `NaN` during factor extraction and treat it as a missing value.

### What are the methods for correcting outliers, and when should each be used?

Outliers commonly appear in financial data (e.g., net profit growth rate exploding when the denominator approaches zero). Failing to correct them significantly interferes with neutralization regression and metrics like IC. There are three methods:

1.  **Mean-Standard Deviation Method (3σ Method)**: Pulls data deviating more than 3 standard deviations from the mean back to the boundary, implemented via `np.clip`. **Note**: With small sample sizes, individual outliers can significantly affect the standard deviation, causing the 3σ threshold to fail (all points fall within the boundary);
2.  **Quantile Method (Winsorization)**: Sorts data and pulls head/tail values back based on quantiles. `scipy.stats.mstats.winsorize` implements this directly, supporting symmetric (e.g., `[0.1, 0.1]`) and asymmetric Winsorization, with results in the `.data` attribute;
3.  **Median Absolute Deviation Method (MAD Method)**: Pulls values deviating by a certain multiple of the MAD from the median. The Absolute Median Deviation is `MAD = median(|Xi − median(X)|)`; taking a proportionality factor $k \approx 1.4826$ makes MAD consistent with the standard deviation of a normal distribution. At this point, **3×MAD approximates 5×standard deviation**. MAD is more robust to outliers and is a commonly used practical solution.

### How should missing values be handled? Delete, fill, or exclude?

More than **70%** of fundamental factors for companies have missing values (Bryzgalova et al. studied 45 popular characteristic factors in asset pricing). The general practice is to **delete rows with missing values**, retaining only valid values; replacement is considered only when retention is necessary:

-   **Financial factors**: **Carry forward the previous period's factor value** (Point-in-Time, PIT);
-   **Other factors**: Replace with cross-sectional median, similar company values, or interpolation (pandas' `fillna` / `ffill` / `bfill` / `interpolate`);
-   If the missing ratio is too high, leading to insufficient coverage, consider excluding that factor or data.

Two common pitfalls: ① Filling (especially with mean/median) alters the data distribution; **the order of outlier clipping and missing value handling matters, as different orders may yield different results**; ② The pandas `fillna(method=...)` syntax is deprecated; use `ffill` / `bfill` directly.

### When is distribution adjustment (e.g., log transformation) necessary?

Ideally, factor exposure on the cross-section should approximate a normal distribution. When significantly deviating, you can use **logarithmic or square-root transformations** before use. A typical example is the China A-share market-cap factor: numerous small-cap stocks and a few with huge market caps result in a right-skewed, leptokurtic, heavy-tailed original distribution. **Taking the logarithm brings it close to normal**. The approach is to first infer the distribution (e.g., plot a histogram) and then decide whether to adjust.

### When is standardization required? Is it needed for single-factor testing?

Standardization (z-score, $Z = (x − \mu) / \sigma$) aims to **eliminate dimensional differences between factors, allowing fair comparison of weights in linear models**. Whether it is needed depends on the downstream model:

-   **Single-factor testing does not require it**: Alphalens does not standardize factors, nor does it require standardization;
-   **Linear regression models must do it**;
-   **Tree models (Decision Trees, XGBoost, LightGBM) are insensitive to dimensions and do not need it**.

Prerequisite: Standardization assumes factors approximate a normal distribution; if this assumption does not hold, direct standardization is meaningless (use statistical tests to judge). Also note that $Z \sim N(0,1)$ means mean 0 and standard deviation 1—not that values are in $(0,1)$, but that the probability of $|Z|$ falling in $[1,2]$ is less than 5%, and greater than 2 is less than 0.3%.

### What is neutralization? How are sector and market-cap neutralization performed?

Many factors have systematic differences due to industry or market cap—these differences do not reflect company quality but rather industry disparities and economic cycles. Without neutralization, you encounter "pseudo Alpha": for example, using a low P/E factor in 2022 would select almost exclusively bank stocks, earning industry Beta rather than stock-selection Alpha.

**Two common schemes for sector neutralization**:

1.  **Industry Mean Difference Method (Demean)**: $\epsilon = Y − \bar{Y}_{industry}$, i.e., subtracting the industry factor mean from the individual stock's factor value;
2.  **Dummy Variable Regression Method**: $Y = \beta \times Industry + \alpha + \epsilon$, performing linear regression using industry dummy variables (0/1), **taking the residual $\epsilon$ as the neutralized factor**; this scheme can be combined with market-cap neutralization.

**Market-cap neutralization** uses the regression form: $Y = \beta \times \log(\text{Market Cap}) + \alpha + \epsilon$, also taking the residual. Industry dummies and log market cap can be concatenated into a single design matrix to perform double neutralization in one step (keep `fit_intercept` generally).

Selection advice: Research by Ehsani et al. (2022) suggests that **long-short hedged investors should perform sector neutralization, while pure long investors should avoid it**. Also, distinguish between: market-cap **distribution adjustment** (log transformation) applied to individual market caps, requiring no overall sample; market-cap **neutralization** is the process of subtracting the mean/regressing to take residuals—these are different operations.

## How to Perform Factor Preprocessing (Standard Steps)

Taking a 10-day momentum factor as an example, the recommended preprocessing order is:

1.  **Outlier Clipping**: Use 3×MAD truncation (`mad_clip`)—operate along the cross-section (row) direction, processing within the same day to avoid look-ahead bias;
2.  **Missing Value Handling**: For cross-sections with missing rates below a threshold (e.g., 20%), fill with the cross-sectional median; otherwise, delete that period. Exclude标的 with excessive missing data. **Missing values must be handled first, otherwise subsequent standardization and neutralization cannot be calculated**;
3.  **Distribution Adjustment** (as needed): For factors with obvious right skew (e.g., market cap), take the logarithm or square root;
4.  **Standardization** (as needed): Z-score standardization by cross-section—required for linear models, not for tree models or single-factor testing;
5.  **Neutralization**: Construct a design matrix of [log market cap + industry dummies], perform period-by-period regression to take residuals, obtaining the neutralized clean factor.

This workflow corresponds one-to-one with the `get_clean_factor` implementation in Chapter 3's single-factor testing of this course, and is also the foundation for understanding Alphalens' preprocessing logic.

## Further Reading

-   [Factor Testing FAQ: Regression Methods, IC Analysis, and Layered Backtest Selection](https://www.quantide.cn/articles/course/factor-ml/factor-testing-faq/)
-   Bryzgalova et al., *Missing Financial Data* (2022); Ehsani, Harvey, Li, *Is Sector-neutrality in Factor Investing a Mistake?* (2022)

The above content systematically covers Chapter 2, "Factor Preprocessing Workflow," in the [Factor Analysis and Machine Learning Strategies Course](https://www.quantide.cn/articles/course/factor-ml/intro/). The complete syllabus is available at [Course Syllabus](https://www.quantide.cn/articles/course/factor-ml/syllabus/).

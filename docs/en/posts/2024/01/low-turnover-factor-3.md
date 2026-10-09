---
title: "Alphalens Factor Analysis: Why Your Alpha Calculation Is Wrong"
date: 2024-01-11
slug: en/posts/factor-strategy/low-turnover-factor-3
tags: [Factor Analysis, Alphalens, Alpha]
excerpt: "Alphalens alpha and beta look simple, but hidden weighting assumptions can invalidate them. We explain why factor values must correlate positively with returns, using turnover as an example."
lang: en
translation_of: posts/factor-strategy/low-turnover-factor-3
auto_translated: true
source_sha: 32d99165ce4a11a07fcfe6592793684af62d3485
---

Continuing our walkthrough of Alphalens factor analysis reports. As noted in the previous two posts, running factor analysis with Alphalens is straightforward, but without understanding the mechanics underneath, it is easy to reach plausible-sounding but misleading conclusions.

Alphalens provides alpha and beta analysis via `factor_alpha_beta`:

```python
from alphalens.performance import factor_alpha_beta

alpha, beta = factor_alpha_beta(factor_data)
```

This gives the following output:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/01/alphalens-alpha-beta.jpg)

---

Looks perfect.

The result suggests an annualized alpha of 2.7% with 35% market exposure — the factor appears somewhat driven by the market. We built `factor_data` exactly as Alphalens requires, via `get_clean_factor_and_forward_returns`, then used it to compute alpha and beta. The process is simple and clear, seemingly foolproof.

**But in this example, the alpha and beta we just computed are essentially meaningless.**

!!! warning
    In quant research, never take any number at face value — scrutinize every result, because getting a result and getting a correct result are two completely different things.

In Alphalens, alpha and beta come from an OLS regression of the factor portfolio return on the market portfolio return.

!!! info
    Alphalens borrows the OLS implementation from statsmodels here.

The market portfolio return is simply the equal-weighted average across all assets. Suppose our universe has 4 assets with daily returns of 0.01189, 0.01102, -0.01241 and -0.01898, then the market return for that day is

$$
(0.01189 + 0.01102 -0.01241 -0.01898)/4= -0.00212
$$

---

Calculating the factor portfolio return comes down to how factor weights are assigned. Once the weight $W$ is set, the portfolio return follows:

$$
    r_p = \sum{r_i * W_i}
$$

The key is how $W$ is computed.

Alphalens groups `factor_data` by date, then divides each asset's factor value by the sum of factor values for that day, so the resulting weights sum to 1. It also offers a demeaning option: subtract the median from the factor values, then divide by the group sum, giving weights that sum to zero.

Suppose we have the following `factor_data` (left chart). If we compute weights the Alphalens way, we get the right chart:

![R50](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/01/alphalens-sample-weight.jpg)

![R50](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/01/alphalens-factor-sample.jpg)

There are two issues here:

1. By default, Alphalens produces zero-net weights, which assumes a market where you can go both long and short. If for whatever reason you are restricted to long-only, you must call `factor_alpha_beta` with `demeaned=False` to change how factor weights are computed.

---

2. If the factor is turnover, then under Alphalens weighting (assuming `demeaned=False`), the factor portfolio return is computed by giving the largest long weight to the highest-turnover stocks and the smallest weight to the lowest-turnover stocks — exactly the opposite of what a low-turnover factor is supposed to capture!

So when building factors, we need to transform the factor so that it is positively correlated with returns.

In hindsight this looks obvious, but Alphalens never documents it. And because our earlier analyses used quantile grouping, the results were unaffected, so the issue stayed hidden.

Now let's transform the factor and rerun:

```python
from alphalens.utils import get_clean_factor_and_forward_returns

factor_data = get_clean_factor_and_forward_returns(factor, prices, bins=None, quantiles=10)

# 我们将换手率因子取倒数，从而使得因子逆序
factor_data.factor = 1 / factor_data.factor
factor_alpha_beta(factor_data,demeaned=False)
```

This time we get 4.48% annualized alpha with 80% market exposure, consistent with what we saw in the cumulative returns plot.

Now let's run the `mean_return_by_quantile` analysis again to see the difference:

---

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/01/alphalens-mean-return-revers.jpg)

Visually, this is a horizontal flip of the corresponding chart from yesterday's note. This time quantile 10 performs best and quantile 2 performs worst — otherwise nothing else changed.

!!! tip KEY TAKEAWAY
    1. By default, Alphalens computes returns on a long-short portfolio — long the highest quantile and short the lowest quantile.
    2. Although undocumented, code inspection shows Alphalens effectively requires factor values to be positively correlated with returns.
    3. If factor values are negatively correlated with returns, you can invert the ordering by taking the reciprocal.
    4. If there is no monotonic relationship between factor values and returns, the factor testing fails — but you have to diagnose that yourself.
    5. In Alphalens, factor alpha and beta come from an OLS regression of factor portfolio returns on market returns.

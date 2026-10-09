---
title: "KS Test, Generalized Hyperbolic Fit, and Buying SSE Dip"
date: 2024-01-05
slug: en/posts/algo/ks-test-and-cdf
tags: [K-S Test, Distribution Fitting, Shanghai Index]
excerpt: "When the Shanghai Index drops 4%, should you buy the dip? We run K-S tests to identify its return distribution and use its CDF to estimate the odds of further decline."
lang: en
translation_of: posts/algo/ks-test-and-cdf
auto_translated: true
source_sha: 3d0e608f5424d6d854aeced7f4e13f9358c24893
---

![R50](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/06/sh_histo_pdf.png) In our last note, we asked a question: when the Shanghai Index plunges 4%, can you buy the dip? In this note, we'll use the K-S test to pin down the probability distribution of the Shanghai Index and answer that question. In a later note, we'll answer the same question with a different method.

<!--more-->
## K-S Test

Our first approach is to try our luck with the K-S test and see if Shanghai Index returns happen to match a known distribution. If we find one, we can easily use its cumulative distribution function (CDF) to compute the probability of further decline as:

$$
P = cdf(-0.04)
$$

---

The K-S test is a non-parametric test in statistics. It can be used to test whether a sample comes from a given probability distribution (one-sample K-S test), or whether two samples share the same distribution (two-sample K-S test). The K-S test is named after its two proposers, the Russian statisticians Kolmogorov and Smirnov.

We can run the K-S test via scipy.stats.kstest. Its signature is:

```python
kstest(rvs, cdf, args=(), N=20, alternative='two-sided', method='auto')
```

Here rvs is the random variable sample — in our example below, we'll pass in 1,000 trading days of Shanghai Index returns. In the cdf argument, we pass the name of the candidate distribution to test.

It returns a KstestResult object, which includes key attributes such as statistic and pvalue.

Now let's run a one-sample test with kstest against each distribution implemented in scipy.stats to see if any of them pass:

```python
pct = close[:-1]/close[1:] - 1
dist_names = ['burr12', 'dgamma', 'dweibull', 'fisk', 'genhyperbolic', 
              'genlogistic', 'gennorm', 'hypsecant', 'johnsonsu', 
              'laplace', 'laplace_asymmetric', 'logistic', 'loglaplace',
              'nct', 'norminvgauss']
```

---

```python
xmin, xmax = min(pct), max(pct)
dist_pvalue = []

for name in dist_names:
    dist = getattr(scipy.stats, name)
    if getattr(dist, 'fit'):
        params = dist.fit(pct)
        ks = scipy.stats.kstest(pct, name, args=params)
        dist_pvalue.append(round(ks.pvalue, 2))
        
df = pd.DataFrame({
    "name": dist_names,
    "pvalue": dist_pvalue
})

df.sort_values("pvalue", ascending=False).transpose()
```

This gives the following output:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/06/sh_kstest_result.png)

The figure may be too wide to read clearly on a phone. But all you need to know is that the first row, genhyperbolic — the generalized hyperbolic distribution — has the highest p-value, reaching 0.97.

Note that the p-value in scipy.stats.kstest may differ from what you understand as p-value elsewhere. Per its documentation and examples, **a p-value greater than 0.95 means we accept the null hypothesis at 95% confidence: that rvs comes from the distribution indicated by the CDF**.

---

The output therefore suggests that **genhyperbolic, the generalized hyperbolic distribution**, is the closest fit for the Shanghai Index among all candidates.

We can verify this conclusion visually:

```python
from scipy.stats import genhyperbolic

params = genhyperbolic.fit(pct)
rv = genhyperbolic(*params)

fig, ax = plt.subplots(1,1)
x = np.linspace(rv.ppf(0.01), rv.ppf(0.99), 100)
ax.plot(x, rv.pdf(x), label = 'genhyperbolic pdf', color="#EABFC7")

ax2 = ax.twinx()
_ = ax2.hist(pct, bins=50)
```

![75%](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/06/sh_histo_pdf.png)

---

It's not just similar — it's virtually identical. The PDF curve neatly traces the outer contour of the empirical histogram.

![L50](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/01/sp-pdf.jpg)

In fact, the Shanghai Index is not the only index that follows a generalized hyperbolic distribution. According to Souto's paper, *Distribution Analysis of S&P 500 Financial Turbulence*, published in Financial Mathematics (February 2023), **the S&P 500 is also closest to this distribution**.

<br>

!!! warning
    Satou didn't use the ks-test in scipy.stats, but implemented his own. One clue is that although he also concluded the S&P is close to a GH distribution, his computed p-value was zero, not close to 1. Careful readers should recall what we noted earlier: the p-value in scipy's ks-test may be inconsistent with what you see elsewhere.<br><br>A similar inconsistency shows up in the definition of convex functions. Some people (myself included) always call a function shaped like the Chinese character 凸 convex, while others call it concave because its second derivative is negative. I once lost a colleague who was both beautiful and brilliant, and I'm not sure if it was over this disagreement. Anyway, now that you know, watch out from now on — don't lose big over something small.

Now let's compute the cumulative probability of a drop below -4% under the generalized hyperbolic distribution — that is, the probability of further decline:

---

```python
from scipy.stats import genhyperbolic

params = genhyperbolic.fit(pct)
rv = genhyperbolic(*params)
print(f"继续下跌的概率为：{rv.cdf(-0.04):.2%}")
```

The result shows that **the probability of further decline is only 0.16%**. So, the conclusion is: this answer is based solely on historical data, for demonstrating quantitative methods only, and does not constitute any investment advice!

!!! tip
    Not sure why cdf(-0.04) represents the probability of further decline? Our course starts from histograms and walks you through it until it clicks.

## Revisit Connor's RSI
If you still remember our note on Connor's RSI, you may recall that one of its three components is the ranking (prank) of today's return over the past 20 days. That ranking is essentially a linear mapping of the empirical CDF. It turns out that inventing a great indicator only takes a grasp of simple statistics.

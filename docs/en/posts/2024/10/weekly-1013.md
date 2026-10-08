---
title: "Numpy Vectorization for Quant: MAD Clipping, Rolling MDD, and Adaptive Signals"
date: 2024-10-13
slug: en/posts/uncategory/weekly-1013
tags: [Numpy, Quantitative Trading, Factor Investing, Machine Learning]
excerpt: "This QuanTide Weekly covers Numpy vectorization techniques for quant finance, including MAD-based outlier clipping, rolling max drawdown calculations, and adaptive thresholding for trading signals."
lang: en
translation_of: posts/uncategory/weekly-1013
auto_translated: true
source_sha: b5194061312371419366b9bc017ca532748ab4b4
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/university/toronto.webp"
---

### This Week's Highlights
* Effective Oct 25, existing mortgage rates are uniformly adjusted downward!
* Robotaxi Day ends abruptly; Tesla stock plunges.
* A comprehensive package of incremental fiscal policies exceeds expectations, potentially exceeding 5 trillion RMB.
* Debt-resolution concepts emerge!

### Next Week's Watchlist
* Sunday: September PPI and CPI data release.
* Monday (Oct 14): State Council Information Office press conference on Q3 import/export data.

### This Week's Selection

* Serialization! Essential Numpy Programming for Quants (6)

---

* ICBC released FAQs on existing mortgage rate adjustments, revealing that most existing housing loans can be adjusted to no less than LPR minus 30 basis points (excluding second homes in Beijing, Shanghai, and Shenzhen), with a unified batch adjustment effective October 25. For a 1 million RMB, 25-year loan with equal principal and interest repayments, monthly expenses decrease by 469 RMB, saving a total of 140,600 RMB in interest.
* The "We Robot" event was held, with Musk previously calling it "historic." However, the curtain-raiser featured only a brief 20-minute keynote, with no key technical indicators or parameters disclosed. Tesla subsequently fell 8.78%, while its rival Lyft surged 9.59%.
* The Ministry of Finance held a press conference on Saturday, unveiling a package of incremental fiscal policies. Analysts conservatively estimate the scale at over 5 trillion RMB, focusing on debt resolution and grassroots "three guarantees."
* Following the Ministry's announcement, debt-resolution concepts sparked market热议 (heated discussion). Securities Times Data宝 compiled a list of approximately 37 companies potentially benefiting from AMC, city investment platforms, PPP concepts, and REITs concepts. Despite Friday's market plunge, most of these companies rose counter-trend or outperformed the broader market.

<claimer>Source: Eastmoney</claimer>

---

# Numpy Quantitative Application Cases [3]
## Vectorization Example: Multi-Asset Median-Based Outlier Clipping

Outlier clipping is a common preprocessing step in quantitative analysis and machine learning. Among various clipping methods, median-based pullback is the most robust and adaptable to different data distributions.

We first introduce the concept of Median Absolute Deviation (MAD):

$$MAD = median(|X_i - median(X)|)$$

To treat MAD as an estimator consistent with the standard deviation $\sigma$, i.e.,
$$\hat{\sigma} = k \cdot MAD$$

Here, $k$ is a proportionality constant. If the distribution is normal, we can calculate:
$$
k = \frac{1}{\Phi^{-1}(\frac{3}{4})} \approx 1.4826
$$

---

Based on this $k$ value, taking 3 times MAD approximates to 5 standard deviations.

The code implementation is as follows:

```python
from numpy.typing import ArrayLike

def mad_clip(arr: ArrayLike, k: int = 3):
    med = np.median(arr)
    mad = np.median(np.abs(arr - med))
    
    return np.clip(arr, med - k * mad, med + k * mad)

np.random.seed(78)
arr = np.append(np.random.randint(1, 4, 20), [15, -10])
mad_clip(arr, 3)
```

This code performs `mad_clip` on a single asset. To clip outliers for a specific metric across all A-shares simultaneously, looping 5,000+ times is inefficient. We can use the following method instead:

```python
def mad_clip(df: Union[NDArray, pd.DataFrame], k: int = 3, axis=1):
    """Outlier clipping using 3x MAD truncation"""
    
    med = np.median(df, axis=axis).reshape(df.shape[0], -1)
    mad = np.median(np.abs(df - med), axis=axis)

    magic = 1.4826
    offset = k * magic * mad
    med = med.flatten()
    return np.clip(df.T, med - offset, med + offset).T
```

---

This version of `mad_clip` accepts both numpy ndarray and pandas dataframe as inputs, returning data in the same format as the input.

In our `np.median` call, we pass the `axis` parameter. If `axis=0`, it traverses columns, calculating medians by row; if `axis=1`, it traverses rows, calculating medians by column.

Let's test with real data:

```python
# Load test data
start = datetime.date(2023, 1, 1)
end = datetime.date(2023, 12, 29)
barss = load_bars(start, end, 7)

closes = barss["close"].unstack("asset").iloc[-5:]
closes
```

The output data is:

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>asset/date</th>
      <th>002095.XSHE</th>
      <th>003042.XSHE</th>
      <th>300099.XSHE</th>
      <th>301060.XSHE</th>
      <th>601689.XSHG</th>
      <th>603255.XSHG</th>
      <th>688669.XSHG</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2023-12-25</th>
      <td>23.400000</td>
      <td>18.090000</td>
      <td>6.10</td>
      <td>13.00</td>
      <td>73.910004</td>
      <td>36.799999</td>
      <td>18.080000</td>
    </tr>
    <tr>
      <th>2023-12-26</th>
      <td>21.059999</td>
      <td>17.520000</td>
      <td>5.94</td>
      <td>12.83</td>
      <td>72.879997</td>
      <td>37.000000</td>
      <td>18.080000</td>
    </tr>
    <tr>
      <th>2023-12-27</th>
      <td>20.070000</td>
      <td>17.590000</td>
      <td>6.04</td>
      <td>12.84</td>
      <td>72.000000</td>
      <td>36.840000</td>
      <td>18.049999</td>
    </tr>
    <tr>
      <th>2023-12-28</th>
      <td>20.010000</td>
      <td>18.139999</td>
      <td>6.11</td>
      <td>13.14</td>
      <td>72.199997</td>
      <td>38.150002</td>
      <td>18.440001</td>
    </tr>
    <tr>
      <th>2023-12-29</th>
      <td>20.270000</td>
      <td>18.580000</td>
      <td>6.19</td>
      <td>13.29</td>
      <td>73.500000</td>
      <td>37.299999</td>
      <td>18.740000</td>
    </tr>
  </tbody>
</table>
</div>

---

To test the effect, we set $k$ to a small value:

```python
mad_clip(closes,k=1)
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>asset/date</th>
      <th>002095.XSHE</th>
      <th>003042.XSHE</th>
      <th>300099.XSHE</th>
      <th>301060.XSHE</th>
      <th>601689.XSHG</th>
      <th>603255.XSHG</th>
      <th>688669.XSHG</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2023-12-25</th>
      <td>23.400000</td>
      <td>18.090000</td>
      <td>10.217396</td>
      <td>13.00</td>
      <td>25.962605</td>
      <td>25.962605</td>
      <td>18.080000</td>
    </tr>
    <tr>
      <th>2023-12-26</th>
      <td>21.059999</td>
      <td>17.520000</td>
      <td>10.296350</td>
      <td>12.83</td>
      <td>25.863649</td>
      <td>25.863649</td>
      <td>18.080000</td>
    </tr>
    <tr>
      <th>2023-12-27</th>
      <td>20.070000</td>
      <td>17.590000</td>
      <td>10.325655</td>
      <td>12.84</td>
      <td>25.774343</td>
      <td>25.774343</td>
      <td>18.049999</td>
    </tr>
    <tr>
      <th>2023-12-28</th>
      <td>20.010000</td>
      <td>18.139999</td>
      <td>10.582220</td>
      <td>13.14</td>
      <td>26.297781</td>
      <td>26.297781</td>
      <td>18.440001</td>
    </tr>
    <tr>
      <th>2023-12-29</th>
      <td>20.270000</td>
      <td>18.580000</td>
      <td>10.659830</td>
      <td>13.29</td>
      <td>26.820169</td>
      <td>26.820169</td>
      <td>18.740000</td>
    </tr>
  </tbody>
</table>
</div>

We observe that the original value 73.9 is pulled back to 25.9, and 6.1 is pulled back to 10.2 (using the first row as an example), calculated on a per-row basis.


## min_range: How many periods since the minimum?

This is a common requirement. As the stock proverb goes, "Volume peaks signal price peaks; volume troughs signal price troughs." When prices are high and volume hits a multi-period high, subsequent volume may struggle to sustain, potentially leading to a decline. Conversely, when prices are low and volume hits a multi-period low, market sentiment is extremely weak, making prices susceptible to manipulation and attracting speculative trading.

---

This function exists in TongDaXin formulas, and in MaiYan language, it might correspond to `LOWRANGE`. Below is the implementation of the `LowRange` function in myTT:

```python
def LOWRANGE(S):                       
    # LOWRANGE(LOW) indicates how many periods ago the current lowest price was the minimum among recent lows by jqz1226
    rt = np.zeros(len(S))
    for i in range(1,len(S)):  rt[i] = np.argmin(np.flipud(S[:i]>S[i]))
    return rt.astype('int')
```

This appears simple but is actually difficult to implement correctly. Testing the above function reveals it may not fully meet the requirement (or the author's understanding of the function may be flawed).

```python
s = [ 1, 2, 2, 1, 3, 0]

LOWRANGE(np.array(s))
```

In this test, we expect the output `[1, 1, 1, 3, 1, 6]`, but `LOWRANGE` returns:

```
array([0, 0, 0, 2, 0, 0])
```

Below is the vectorized implementation of this function.

!!! warning
    This function may produce incorrect outputs for the first few elements. Since this does not affect factor analysis, it has not been fixed yet.

---

```python
def min_range(s):
    """Calculate how many periods ago element i in sequence s was the minimum

    This method has bugs for specific numbers.

    Example:
        >>> s = np.array([5, 7, 7, 6, 5, 8, 2])
        >>> min_range(s)
        array([1, 2, 1, 2, 3, 1, 6])
    """
    n = len(s)

    # handle nan
    filled = np.where(np.isnan(s), -np.inf, s)
    diff = filled[:,None] - filled
    mask = np.triu(np.ones((n, n), dtype=bool), k=1)
    masked = np.ma.array(diff, mask=mask)

    rng = np.arange(n)
    ret = rng - np.argmax(np.ma.where(masked > 0, rng, -1), axis=1)
    ret[0] = 1
    if filled[1] <= filled[0]:
        ret[1] = 2
    return ret

s = np.array([5, 7, 7, 6, 5, 8, 2])
min_range(s)
```

The final output is:

```
array([1, 1, 2, 3, 4, 1, 6])
```

At the position of the second 7, the output differs from expectations, but subsequent calculations are correct. This implementation is highly clever, using a triangular matrix mask array to eliminate loops.

---


## Moving Average Calculation: SMA and Intraday VWAP

Calculating moving averages with Numpy is straightforward using `np.convolve()`.

```python
def moving_average(ts: ArrayLike, win: int, padding=True)->np.ndarray:
    kernel = np.ones(win) / win

    arr = np.convolve(ts, kernel, 'valid')
    if padding:
        return np.insert(arr, 0, [np.nan] * (win - 1))
    else:
        return arr

moving_average(np.arange(5), 3)
```

The output is `array([nan, nan,  1.,  2.,  3.])`.

Moving averages consider only price information. The intraday VWAP (Volume-Weighted Average Price) incorporates both volume and price, holding special significance for intraday trading. For example, in a weak market, if a stock's price is below the intraday VWAP and fails to breach it twice, a third failure is generally considered a signal to sell quickly. The reverse also applies.

The calculation for VWAP is as follows:

---

If the current time is $t$, the cumulative average transaction price at that moment is obtained by dividing the cumulative transaction amount from the open until time $t$ by the cumulative volume. Connecting these average prices across all moments forms the intraday VWAP.

This function appears complex,

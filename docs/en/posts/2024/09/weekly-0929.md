---
title: "Arbitrage Pricing Theory in Practice: Quant Trading Cases"
date: 2024-09-29
slug: en/posts/uncategory/weekly-0929
tags: [Arbitrage Pricing Theory, Quantitative Trading, Factor Investing, Portfolio Optimization]
excerpt: "Arbitrage pricing theory (APT) can be put into practice in quantitative trading through factor-exposure estimation, portfolio optimization under cost and capacity constraints, and A-share applications."
lang: en
translation_of: posts/uncategory/weekly-0929
auto_translated: true
source_sha: 4e47cbdfea78163f5f6c61b833e8e9583acab283
cover: "stamp_width: 60%"
---

## Engineering Arbitrage Pricing Theory in Practice: Quantitative Trading Use Cases

Arbitrage pricing theory (APT) holds that asset returns are driven linearly by multiple common factors; as long as a portfolio has no net exposure to those factors, there should be no predictable excess return. Putting APT into practice usually involves three steps:

1. **Factor-exposure estimation**: use regression and rolling windows to estimate the portfolio's exposures to style factors such as size, momentum, volatility, and sector;
2. **Portfolio optimization**: formulate “factor-exposure constraints + return target + turnover and cost constraints” as a convex optimization problem and solve for weights;
3. **Trading and capacity control**: execute under trading constraints and use attribution reviews to confirm that returns do not come from hidden factor exposures.

In China A-shares, common use cases include market-neutral and statistical-arbitrage portfolios (using factor models to strip out beta), the pricing relationship between a basket of stocks and stock index futures, and weight optimization for multi-factor stock selection. To learn factor analysis and regression methods systematically, start with [Factor Machine Learning Course FAQ](/articles/course/factor-ml/faq/); the companion Numpy linear-regression walkthrough appears in the second half of this article.

### This Week's Headlines
* Big rally: the Shanghai Composite surged 12.8% this week, while the CSI 300 rose 15.7%.
* The first market-value management guideline was released, clarifying market-value management requirements for index constituents and stocks trading below book value.
* Changjiang Securities: banks, real estate, construction, and non-bank financials may be more likely to benefit from valuation-recovery plans for below-book companies.


### Next Week's Highlights
* Monday: Caixin releases September PMI data.
* OpenAI hosts its 2024 DevDay starting October 1.
* Market closed Tuesday (October 1) through October 7.

### This Week's Picks

* Series: Numpy Programming Every Quant Must Know (5)

---

* China A-shares rallied across the board this week. On the news front, the State Council Information Office held a press conference on Tuesday to brief on financial support for high-quality economic development. Pre-market RRR cuts and lower existing mortgage rates boosted market confidence; during the session, a raft of major capital-market measures was released: the CSRC is studying and drafting “Six M&A Measures,” launching an initial RMB 300 billion relending facility for share buybacks and increased holdings, and an initial RMB 500 billion swap facility for securities, fund, and insurance companies; it will support Central Huijin and other medium- and long-term capital in entering the market and is studying the creation of a stabilization fund.
<claimer>Source: East Money</claimer>
* Cailian Press, September 28: China A-shares' first market-value management guideline was recently released, setting specific requirements for index constituents and stocks trading below book value. Industry insiders say the new policy can help undervalued quality assets re-rate; central and state-owned enterprises that trade well below book value but have stable profitability may see valuation-recovery room and investment opportunities. Other analysts say stocks that are both below book value and offer high dividend yields deserve even more attention.
* The PBOC adjusted the rate on its 7-day reverse repo operations in the open market to 1.5%. This week it also cut the reserve requirement ratio by 0.5 percentage points.

<claimer>Source: Cailian Press</claimer>

---

# Numpy in Quantitative Finance: A Case Study [2]


Momentum and reversal are among the most important quantitative factors. There are many ways to characterize momentum, but the slope of a fitted line is arguably the most intuitive.

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/05/two-crossed-line.jpg?1)

---

In the chart above, if the two lines represent the moving-average paths of two stocks, you would clearly prefer to buy the orange one because its slope is steeper—it is rising faster.

Human vision is powerful at pattern discovery. It is easy for us to see that the orange points have a stronger upward trend. But to let a computer know which dataset is better, we need to fit a line, find the trend line, and compare slopes. Line fitting, curve fitting, and polynomial fitting are all linear regression problems.

In this chapter, we discuss line-fitting methods, from the most ordinary implementation to a vectorized version that is 100 times faster.

## Linear Regression and Least Squares

How can we find, within a pile of random numbers, the line that best captures the hidden trend? This problem has troubled scientists since the Age of Discovery.


At that time, sailors needed to determine their latitude from the stars (longitude was calculated using sundials), which required accurately describing celestial motion from human observations.

---

While addressing errors in celestial observations, the Frenchman Adrien-Marie Legendre first discovered the method of least squares (1805). Gauss also proposed the method in his 1809 work *Theory of the Motion of Heavenly Bodies*. Finally, in 1829, he provided the theoretical proof that least squares gives the best linear-regression fit. This proof is known as the Gauss-Markov theorem.

!!! info
     Legendre and Gauss fought a priority dispute over the discovery of least squares, no less fierce than the Newton-Leibniz dispute over calculus. However, when Legendre proposed least squares, it was still a conjecture; Gauss completed its theoretical proof. Legendre was a late-18th-century mathematician on par with Lagrange and Laplace; the three were known as the “three Ls” (from their surnames).

Line fitting (or linear regression) means finding, within a set of (x,y) points, the line that minimizes the sum of squared distances from all points to the line. In Numpy, the most common approach is to fit with `Polynomial.fit`:

```python
from numpy.polynomial import Polynomial
import matplotlib.pyplot as plt


x = np.linspace(0, 100, 100)

```

---

```python

rng = np.random.default_rng(seed = 78)
y = 0.05 * x + 2 + rng.normal(scale = 0.3, size=len(x))

# 绘制这些随机点
plt.scatter(np.arange(100), y, s=5)

# 最小二乘法拟合出趋势线
fitted = Polynomial.fit(x, y, deg=1, domain=[])
y_pred = fitted(x)
plt.plot(y_pred)

# 我们关注的斜率
b, a = fitted.coef
print("slope is {a:.3f}")
```

Many tutorials use `polyfit` for polynomial regression in Numpy. But since version 1.4, we should use the classes and methods in the polynomial module. `polyfit` is considered a legacy API. Note that although polynomial was designed to replace `polyfit` and similar functions, its behavior differs significantly.

<!--Polynomial.fit performs least-squares line fitting. It returns a Polynomial object with a __call__ attribute: pass in x-coordinates to get the corresponding y-values.-->

For Polynomial.fit, note that we pass two arguments, `deg=1` and `domain=[]`.

We set `deg=1` because we want to fit the (x,y) point set with a straight line; set `deg=2` for a quadratic curve, and so on for higher-order curves.

---

`domain` is optional. Omitting it does not affect the predicted line we later obtain via fitted(x), but it does affect the slope we need (line 19). If we omit `domain = []` here, the coefficients we get will be [2.47, 4.57], far from the [0.05, 2] used to generate the data. When we specify `domain = []`, the fitted-line coefficients return to the expected [0.05, 2].

!!! tip
    You can also call `fit` like this:
    ```python
    fitted = Polynomial.fit(x, y, deg=1, window=(min(x), max(x)))
    intercept, slope = fitted.coef
    print(f"slope is {slope:.3f}")
    ```

    Or:
    ```python
    fitted =  Polynomial.fit(x, y, deg=1)
    intercept, slope = fitted.convert().coef
    print(f"slope is {slope:.3f}")
    ```

    `convert` is a transformation function that shifts and scales `domain` and `window`.

<!--Polynomial.fit and polyfit behave quite differently. polyfit returns coefficients, residuals, and other data; Polynomial.fit returns an object, and coefficients, residuals, etc. must be retrieved through its attributes. Second, coefficient order differs: polyfit uses descending powers, while Polynomial uses ascending powers. Third, coefficients differ: the object returned by Polynomial.fit automatically shifts and scales the domain and window to the [-1,1] interval.-->


Linear regression is a very common technique, with similar implementations in scipy, sklearn, statsmodels, and other libraries.

---

As a result, computing a slope factor on prices or moving averages is technically trivial.

But what if we need rolling linear regression? That takes a bit more skill.

## Rolling Linear Regression

Rolling linear regression takes a time series $T$ and a rolling window $win$ and computes another time series $S$ such that

$$
S_i = Slope(T_{[i-win+1, i-win+2, ..., i]})
$$

The simplest implementation is a loop:

```python
from numpy.polynomial import Polynomial
import matplotlib.pyplot as plt


x = np.linspace(0, 100, 100)
y = np.sin(x/10) + x/10

# 曲线拐点
flags = np.sign(np.diff(np.diff(y)))
pivots = np.argwhere(flags[1:] != flags[:-1]).flatten()

plt.plot(y)

win = 10
S = []
```

---

```python
for i in range(win, len(y)):
    xi = x[i-win:i]
    yi = y[i-win:i]
    fitted = Polynomial.fit(xi, yi, deg=1, domain=[])
    S.append(fitted.coef[1])

    if i in pivots:
        xj = x[i-win-10:i+10]
        y_pred = fitted(xj)
        plt.plot(xj, y_pred, '--')

print(S)
```

This code computes the slope of the fitted line over the past 10 points starting from the 10th period, and plots tangent lines at turning points. These tangent lines are generated from the parameters of the fitted line.

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/05/xplussinx.jpg)

---

Here we generate the curve using the equation `x + sin(x)`. You will notice that the resulting curve bears some resemblance to stock-price fluctuations. That is not surprising: stock-price fluctuations should be decomposable into a DC component plus a superposition of many sine waves. The DC component reflects the company's ability to operate as a going concern, while the sine waves reflect the traces left by various short-term speculative funds trading the stock.

Back to the main thread. Now let's remove the plotting and measure how long this code takes to run:

```python
x = np.linspace(0, 100, 100)
y = np.sin(x/10) + x/10

def moving_lsq(ts, win: int):
    x = np.arange(len(ts))
    S = []
    for i in range(win, len(ts)):
        xi = x[i-win:i]
        yi = ts[i-win:i]
        fitted = Polynomial.fit(xi, yi, deg=1, domain=[])
        S.append(fitted.coef[1])
    return S

%timeit moving_lsq(y, 10)
```

90 iterations took 25 ms in total. Given that China A-shares have more than 5,000 stocks, a full calculation would take more than 2 minutes.

---

To speed this up, we need vectorization. But this time there is no magic API to call; we have to roll up our sleeves, understand the underlying math, and build our own implementation.

## Vectorization

Consider a linear regression with `m` points. For each point, we have:

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/05/linear-regression-group.jpg)

If all points fall on the same line, the following matrix equation holds:

$$
Y = A\beta + b
$$

Here $A$ is X, and $\beta$ is the coefficient vector to solve for:

$$
\beta = {(A^TA)}^{-1}A^TY
$$

---

For the derivation, see [*Python Programming and Numerical Methods: A Guide for Engineers and Scientists*](https://pythonnumericalmethods.studentorg.berkeley.edu/notebooks/chapter16.04-Least-Squares-Regression-in-Python.html).

We can verify this formula manually:

```python
x = np.linspace(0, 9, 10)
y = x + np.sin(x/10)

win = 10

A = np.arange(win).reshape((win,1))
pinv = np.dot(np.linalg.inv(np.dot(A.T, A)), A.T)
alpha_1 = np.dot(pinv, y[:, np.newaxis]).item()
alpha_2 = Polynomial.fit(x, y, deg=1, domain=[]).coef[1]

np.isclose(alpha_1, alpha_2, atol=1e-2)
```

We solved for the slope using two methods; the results are identical under an absolute error tolerance of `1e-2`.

Note that on line 7 we use the oddly named variable `pinv`. This is because numpy.linalg has a function of the same name that computes ${(A^TA)}^{-1}A^T$.

So far, however, we have only reproduced what Polynomial.fit does. How can we compute the fitted-line slopes for all rolling windows at once?

---

Note that we compute the slope via matrix multiplication. In Numpy, matrix multiplication is naturally vectorized. On line 7, `pinv` is a (1,10) matrix and `y` is a (10,) vector. If we can stack the `pinv` matrices for each rolling window and stack the `y` vectors into a matrix, we can compute all slopes at once with matrix multiplication.

Start with `y`. When we slide over `y = np.arange(5)` with a window of 3, we effectively get this matrix:

$$
\begin{bmatrix}0&1&2\\1&2&3\\2&3&4\\\end{bmatrix}
$$

We can build this matrix using fancy indexing:

```python
y[
    [0, 1, 2],
    [1, 2, 3],
    [2, 3, 4]
]
```

So to build the rolling-window matrix for y, we only need to construct this fancy-index matrix. The good news is that it is highly regular:

---

```python
def extract_windows_vectorized(array, win:int):
    start = 0
    max = len(array) - win + 1
    
    sub_windows = (
        start +
        # expand_dims are used to convert a 1D array to 2D array.
        np.expand_dims(np.arange(win), 0) +
        np.expand_dims(np.arange(max), 0).T
    )

    return array[sub_windows]

arr_1d = np.arange(10, 20)

extract_windows_vectorized(arr_1d, 4)
```

If this method is hard to follow, Numpy provides a function called `as_strided` that does the job in one step and is about twice as fast as the method above:

```python
from numpy.lib.stride_tricks import as_strided

y = np.arange(3, 10)
stride = y.strdies[0]

win = 4
shape = (len(y) - win + 1, win)
strides = (stride, stride)
as_strided(y, shape, strides)
```

The matrix `pinv` is generated from x. If the time series y is 100 periods long, x will range from 0 to 99.

---

where $[x0, x1, ..., x_{win-1}]$ corresponds to $[y0, y1, ..., y_{win-1}]$,
$[x1, x2, ..., x_{win}]$ corresponds to $[y1, y2, ..., y_{win}]$, and $[x_{-win}, x_{-win+1}, ... x_{-1}]$ corresponds to $[y_{-win}, y_{-win+1}, ..., y_{-1}]$.

Therefore, the coefficient matrix $A$ we need to construct is:

```python
A = as_strided(np.arange(len(y)), shape, strides)
pinv = np.linalg.pinv(A)
```

The regression that follows is the same as before:

```python
alpha = pinv.dot(y).sum(axis = 0)
```

The complete code is as follows:

```python
def moving_lsq_vector(ts, win:int):
    stride = ts.strides[0]

    strides = (stride, stride)
    shape = (win,len(ts)-win+1)
    A = as_strided(np.arange(len(ts)), shape= shape, strides=strides)
    pinv = np.linalg.pinv(A)
    y = as_strided(ts, shape=shape, strides = strides)
    
    return pinv.dot(y).sum(axis=0)
```

This version is 100x faster than the previous version using Polynomial.fit plus a loop. As you may have guessed, 100x is roughly the number of loop iterations. That is the cost of looping.

---

Now, can we use this approach to speed up other calculations? Clearly yes. Suppose you want to quickly compute the 5-day average over the past 10 days for 5,000 stocks. After fetching the last 14 days of prices, you have a (5000, 14) matrix $A$. All you need to do is reshape it into a 3D matrix and multiply it by a convolution kernel:

```python
from numpy.typing import NDArray
def batch_move_mean(A: NDArray, win:int)->NDArray:
    """批量计算移动平均线

    Args:
        A: (m*n)的价格矩阵。m为股票支数
        win: 移动平均窗口
    Returns:
        （m * (n-win+1))的矩阵.
    """
    kernel = np.ones(win)/win
    
    s0, s1 = prices.strides
    m, n = prices.shape

    pm = as_strided(prices, shape=(m, n-win + 1, win), strides=(s0, s1, s1))
    return np.dot(pm, kernel.T).squeeze()
```

We test it with the following code:

```python
prices = np.array([
    np.arange(0, 14),
    np.arange(10, 24)
])

batch_move_mean(prices, 5)
```
---

The output is:

```
array([[ 2.,  3.,  4.,  5.,  6.,  7.,  8.,  9., 10., 11.],
       [12., 13., 14., 15., 16., 17., 18., 19., 20., 21.]])
```

Exactly as expected—but lightning fast.

## A Digression

Should a fitted trend line be used as a momentum factor? This deserves deeper discussion. The biggest problem with the slope factor is that not all time series have a clear trend. Mathematically, if the fitting residuals are large, the series has not formed a clear trend, and the slope factor should not be used. Another issue is the old problem of linear regression: a few outliers can heavily influence the fit. Should the fitted line minimize the sum of squared distances from all points, or should it make the distances for most points smaller, even if the total is not the smallest?

## Conclusion

We discussed how to perform linear regression (line fitting) with numpy and introduced the modern polynomial API. Then we showed how to use matrix operations to achieve vectorization.

---

The key idea is to use `as_strided` to add dimensions to an array, then perform matrix operations on the higher-dimensional array to vectorize the computation. We used the same idea to compute moving averages for 5,000 stocks at once. You also saw a practical example of fancy indexing. This chapter packs in many techniques and serves as a recap of earlier chapters.

<about/>

---

## Course Launch: Factor Investing and Machine Learning Strategies

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/hot/course/factor-ml/1.png)

---

## Clear Goals, Strong Sense of Achievement

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/hot/course/factor-ml/2.png)

---

## Why QuanTide's Course Is Worth It

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/hot/course/factor-ml/3.png)

---
title: "Arbitrage Pricing Theory in Practice: Quant Trading Use Cases"
date: 2024-09-29
slug: en/posts/uncategory/weekly-0929
tags: [Arbitrage Pricing Theory, Factor Investing, Quantitative Trading, Numpy]
excerpt: "How does arbitrage pricing theory translate into practice? A walkthrough of factor exposure estimation, portfolio optimization, and cost and capacity constraints, with China A-share use cases."
lang: en
translation_of: posts/uncategory/weekly-0929
auto_translated: true
source_sha: a841b64de4795683a55f3f25e160112a73904c3e
cover: "stamp_width: 60%"
---

## Putting Arbitrage Pricing Theory into Practice: Quantitative Trading Use Cases

Arbitrage Pricing Theory (APT) holds that asset returns are driven linearly by a set of common factors, so a portfolio with no net factor exposure should produce no predictable excess return. Putting it into production usually takes three steps:

1. **Factor exposure estimation**: use regression over rolling windows to estimate the portfolio's exposure to style factors (size, momentum, volatility, sector, etc.);
2. **Portfolio optimization**: frame "factor exposure constraints + return target + turnover and cost constraints" as a convex optimization problem and solve for the weights;
3. **Execution and capacity control**: trade under execution constraints, then use attribution reviews to confirm the return is not coming from hidden factor exposure.

In China A-shares, typical use cases include market-neutral and statistical arbitrage portfolios (stripping out beta with a factor model), the pricing relationship between a basket of stocks and index futures, and weight optimization in multi-factor stock selection. For a systematic treatment of factor analysis and regression methods, start with [the factor machine-learning course FAQ](/articles/course/factor-ml/faq/); the companion Numpy linear regression walkthrough is in the second half of this article.

### This Week's Headlines
* Big rally! The Shanghai Composite surged 12.8% this week, with the CSI 300 up 15.7%.
* The first market-value management guidelines were released, setting out specific requirements for index constituents and stocks trading below book value.
* Changjiang Securities: banks, real estate, construction, and non-bank financials may benefit most from revaluation plans for sub-book-value companies.

### What to Watch Next Week
* Monday: Caixin releases September PMI data.
* OpenAI hosts its 2024 DevDay starting October 1.
* Markets closed Tuesday (October 1) through October 7.

### This Week's Picks

* Serialized! Numpy programming every quant must know (5)

---

* China A-shares rallied across the board this week. On the news front, the State Council Information Office held a press conference on Tuesday detailing financial support for high-quality economic development. Pre-market cuts to the reserve requirement ratio and to existing mortgage rates lifted confidence, and during the session capital markets saw a dense stream of major policy support: the CSRC is drafting the "M&A Six Measures," a first tranche of RMB 300 billion in relending for share buybacks and increases, a first tranche of RMB 500 billion in swap facilities for securities firms, funds, and insurers, support for medium- and long-term capital such as Central Huijin to enter the market, and a stabilization fund is under study.
<claimer>Source: Eastmoney</claimer>
* Cailian Press, September 28: China A-shares' first market-value management guidelines have been released, specifying requirements for index constituents and stocks trading below book value. Industry observers say the new policy helps repriced undervalued quality assets; in particular, deeply sub-book-value central SOEs with stable profitability may offer room for a value re-rating and thus investment opportunities. Other analysts note that stocks that are simultaneously below book value and high-yielding deserve even more attention.
* The PBOC adjusted the rate on its 7-day reverse repurchase operations to 1.5%. It also cut the reserve requirement ratio by 0.5 percentage points this week.

<claimer>Source: Cailian Press</claimer>

---

# Numpy in Quantitative Finance: A Case Study [2]


Momentum and reversal are the most important quantitative factors. There are many ways to characterize momentum, but the slope of a fitted line is surely the most intuitive.

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/05/two-crossed-line.jpg?1)

---

In the chart above, if the two lines were moving averages for two stocks, you would clearly rather buy the orange one — its slope is steeper, meaning it is rising faster.

Human vision is remarkably good at spotting patterns. We can easily see that the upward trend in the orange dots is stronger. But to make a computer recognize which dataset is better, we have to fit a line, find the trend line, and compare slopes. Line fitting — or curve fitting, or polynomial fitting — is a linear regression problem.

In this chapter we discuss line fitting, starting from the most basic implementation and working up to a vectorized version that is a hundred times faster.

## Linear Regression and Least Squares

How do you find, among a pile of random numbers, the straight line that best captures the hidden trend? This question has vexed scientists since the Age of Exploration.

In that era, sailors determined latitude from the stars (longitude was measured with chronometers), which required an accurate description of celestial behavior based on human observations.

---

In tackling the errors induced by celestial observation, the Frenchman Adrien-Marie Legendre was the first to discover the method of least squares (1805). Gauss then presented the method in his 1809 work *Theoria Motus Corporum Coelestium*. Finally, in 1829, he supplied the theoretical proof that least squares is the best fit for linear regression — now known as the Gauss–Markov theorem.

!!! info
      Legendre and Gauss fought over who discovered least squares — a dispute no less bitter than the Newton–Leibniz feud over calculus. But Legendre's least squares was only a conjecture; the theoretical proof came from Gauss. Legendre was a late-18th-century mathematician on par with Lagrange and Laplace; the three were known as the "three Ls" (after their names).

Line fitting (or linear regression) means finding, within a point set of (x, y), the line that minimizes the sum of squared distances from all points to that line. In Numpy, the most common approach is to fit with `Polynomial.fit`:

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

Many tutorials show polynomial regression in Numpy using `polyfit`. But since version 1.4 we should be using the classes and methods in the `polynomial` module; `polyfit` is regarded as a legacy interface. Note that although `polynomial` was designed to replace functions like `polyfit`, its behavior differs considerably.

<!--Polynomial.fit is the method for least-squares line fitting. It returns a Polynomial object with a __call__ attribute, so passing x coordinates gives you the corresponding y values.-->

With `Polynomial.fit`, note that we pass two parameters, `deg=1` and `domain=[]`.

We specify `deg=1` because we want to fit the point set (x, y) with a straight line; specifying `deg=2` fits a quadratic, and higher degrees follow the same pattern.

---

`domain` is an optional parameter. Omitting it does not affect our later use of `fitted(x)` to obtain the predicted line, but it does affect the slope we want (line 19). If we omit `domain = []` here, the coefficients we get are [2.47, 4.57], far from the [0.05, 2] used to generate the data. Once we specify `domain = []`, the fitted coefficients come back as the expected [0.05, 2].

!!! tip
    We can also call `fit` like this:
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

    `convert` is a transform that shifts and rescales the domain and window.


<!--Polynomial.fit differs considerably in behavior from polyfit. polyfit returns coefficients, residuals, and other data; Polynomial.fit returns an object whose attributes you use to retrieve them. Second, coefficient ordering differs: polyfit uses descending powers, Polynomial uses ascending powers. Third, the coefficients themselves differ: the object returned by Polynomial.fit automatically shifts and scales the domain and window to the [-1, 1] interval.-->


Linear regression is an extremely common technique, and scipy, sklearn, and statsmodels all offer similar implementations.

---

That is why computing a slope factor on prices or moving averages is technically trivial.

But what if we want rolling linear regression? That takes a bit more finesse.

## Rolling Linear Regression

Rolling linear regression means that, given a time series $T$ and a sliding window $win$, we compute another time series $S$ such that

$$
S_i = Slope(T_{[i-win+1, i-win+2, ..., i]})
$$

The simplest, most direct implementation uses a loop:

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

This code computes, starting from the 10th period, the slope of the line fitted to the previous 10 points, and draws the tangent at each turning point of the curve. Those tangents are generated directly from the fitted line's parameters.

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/05/xplussinx.jpg)

---

Here we generated the curve with the equation `x + sin(x)`. You will notice that the result looks somewhat like stock price movement. Not surprising: a price series should decompose into a DC component plus a superposition of many sine waves. The DC component reflects the company's ability to keep operating; the sine waves reflect the traces left by short-term traders operating in the name.

Back to the point. Now let's strip out the plotting and time how long this code takes:

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

90 iterations took 25 ms in total. With over 5,000 stocks in China A-shares, a full pass would take more than two minutes.

---

To speed this up we need vectorization. But this time there is no magic API to call — we have to roll up our sleeves, start from the underlying math, and write our own implementation.

## Vectorization

Consider a linear regression over `m` points. For each point we have:

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/2024/05/linear-regression-group.jpg)

If all points lie on the same line, the following matrix equation holds:

$$
Y = A\beta + b
$$

Here $A$ is X, and $\beta$ is the coefficient vector we need to solve for:

$$
\beta = {(A^TA)}^{-1}A^TY
$$

---

For the derivation, see [*Python Programming and Numerical Methods: A Guide for Engineers and Scientists*](https://pythonnumericalmethods.studentorg.berkeley.edu/notebooks/chapter16.04-Least-Squares-Regression-in-Python.html).

We can verify the formula by hand:

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

We solved for the slope two ways, and the results agree to within an absolute error of 1e-2.

Note that in line 7 we use the odd variable name `pinv`, because `numpy.linalg` has a function of that name that computes exactly ${(A^TA)}^{-1}A^T$.

But so far we have only reproduced what `Polynomial.fit` does. How do we compute the fitted slopes for all sliding windows at once?

---

Note that we compute the slope via a matrix multiplication, and in Numpy matrix multiplication is inherently vectorized. In line 7, `pinv` is a (1, 10) matrix and `y` is a (10,) vector. If we can stack the `pinv` for each sliding window and stack the `y` values into a matrix, we can compute all the slopes in a single matrix multiplication.

Start with `y`. Sliding over `y = np.arange(5)` with a window of 3 yields the matrix:

$$
\begin{bmatrix}0&1&2\\1&2&3\\2&3&4\\\end{bmatrix}
$$

We can build it with fancy indexing:

```python
y[
    [0, 1, 2],
    [1, 2, 3],
    [2, 3, 4]
]
```

So to build the matrix of y values across sliding windows, we only need to construct this fancy index matrix. Good news: the fancy index matrix is highly regular:

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

If that feels hard to follow, Numpy already provides a function called `as_strided` that does the job in one step, and about twice as fast as the method above:

```python
from numpy.lib.stride_tricks import as_strided

y = np.arange(3, 10)
stride = y.strdies[0]

win = 4
shape = (len(y) - win + 1, win)
strides = (stride, stride)
as_strided(y, shape, strides)
```

The matrix `pinv` is generated from x. If the time series y is 100 periods long, then x ranges from 0 to 99.

---

Here $[x0, x1, ..., x_{win-1}]$ corresponds to $[y0, y1, ..., y_{win-1}]$,
$[x1, x2, ..., x_{win}]$ corresponds to $[y1, y2, ..., y_{win}]$, and $[x_{-win}, x_{-win+1}, ... x_{-1}]$ corresponds to $[y_{-win}, y_{-win+1}, ..., y_{-1}]$.

Therefore the coefficient matrix $A$ we need to build is:

```python
A = as_strided(np.arange(len(y)), shape, strides)
pinv = np.linalg.pinv(A)
```

The regression then proceeds exactly as before:

```python
alpha = pinv.dot(y).sum(axis = 0)
```

Here is the complete code:

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

This version is 100x faster than the earlier one using `Polynomial.fit` inside a loop. You may have guessed that the 100x roughly matches the number of iterations — that is the price of looping.

---

Now, can we use this approach to speed up other computations? Obviously yes. Suppose you want to compute the 5-day moving average over the past 10 days for 5,000 stocks. After fetching the last 14 days of prices for those stocks, you have a (5000, 14) matrix $A$. All you need to do now is convert it into a 3-D array and multiply by a convolution kernel:

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

Output:

```
array([[ 2.,  3.,  4.,  5.,  6.,  7.,  8.,  9., 10., 11.],
       [12., 13., 14., 15., 16., 17., 18., 19., 20., 21.]])
```

Exactly as expected. But lightning fast.

## A Digression

Should a fitted trend line be used as a momentum factor? That is a topic worth discussing in depth. The biggest problem with the slope factor is that not every time series has a clear trend. Mathematically, if the fit residual is large, the series has not yet formed a clear trend, and the slope factor should not be used. The other problem is the old bugbear of linear regression: individual outliers heavily influence the fit. Should the fitted line minimize the summed distance from all points, or make the distance smaller for most points (smaller than the former)?

## Conclusion

We discussed how to do linear regression (line fitting) in Numpy and introduced the modern polynomial API. Then we showed how to vectorize using matrix operations.

---

The key idea is to use `as_strided` to add dimensions to an array, then perform matrix operations on the expanded array to achieve vectorization. We used the same idea to compute moving averages for 5,000 stocks in one shot. You also saw a practical example of fancy indexing. This chapter is heavy on technique and serves as a wrap-up of the preceding ones.

<about/>

---

## The "Factor Investing and Machine Learning Strategies" Course Is Open!

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/hot/course/factor-ml/1.png)

---

## Clear Objectives, Tangible Results

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/hot/course/factor-ml/2.png)

---

## Why QuanTide's Course Is Worth It

![](https://gcore.jsdelivr.net/gh/zillionare/images@main/images/hot/course/factor-ml/3.png)

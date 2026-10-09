---
title: "Vectorize Linear Regression: 100x Speedup with Numpy"
date: 2025-03-26
slug: en/articles/python/numpy-pandas/09-numpy应用案例-2
tags: [Numpy, Quantitative Analysis, Vectorization, Linear Regression]
excerpt: "Learn to accelerate quantitative factor computation by replacing Python loops with Numpy vectorization. This guide demonstrates how to implement sliding-window linear regression using matrix operations and `as_strided`, achieving a 100x performance boost for large-scale data analysis."
lang: en
translation_of: articles/python/numpy-pandas/09-numpy应用案例-2
auto_translated: true
source_sha: 0a07f43ec36741c47b8ce833a304f8a4d435eb68
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/mybook/iphone-6.jpg"
---

“Linear regression is a common tool in quantitative analysis, but its implementation via loops is inefficient for large-scale data. By leveraging Numpy’s vectorization techniques, we can accelerate calculations by a hundredfold, easily handling complex requirements such as sliding windows and batch processing.”

---

## High-Dimensional Strike: How Extra Dimensions Solve the Vectorization Puzzle

Momentum and reversal are among the most critical factors in quantitative investing. While there are many algorithms to characterize momentum, fitting a line to calculate its slope is undoubtedly the most intuitive approach.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/05/two-crossed-line.jpg?1)

In the graphic above, if the two lines represent the moving average trends of two stocks, you would obviously prefer to buy the orange one because its slope is steeper, indicating a faster upward trend.

---

Human vision has a powerful pattern-recognition capability. We can easily see that the orange points have a stronger upward trend. However, for a computer to determine which dataset is "better," we must fit a line, identify the trend line, and then compare the slopes of these trend lines. Line fitting, curve fitting, or polynomial fitting are all forms of linear regression problems.

In this chapter, we will discuss methods for line fitting, starting from the most basic implementation and progressing to a vectorized implementation that offers a hundredfold speedup.

## Linear Regression and the Least Squares Method

How do we discover the line that best reflects the trend hidden within a set of random numbers? This problem has puzzled scientists since the Age of Discovery. During that era, sailors needed to determine their latitude using star positions (longitude was calculated using solar observations), which required accurately describing celestial behaviors based on human observations.

To address errors arising from celestial observations, the French mathematician Adrien Marie Legendre first discovered the least squares method (1805). Later, Carl Friedrich Gauss proposed this method in his 1809 work *Theoria Motus Corporum Coelestium*. Ultimately, in 1829, he provided the theoretical proof that the least squares method is the optimal fit for linear regression. This proof is known as the Gauss-Markov theorem.

!!! info
     Between Legendre and Gauss, there was a fierce dispute over the discovery of the least squares method. This rivalry was no less intense than the dispute between Newton and Leibniz over the discovery of calculus. However, when Legendre proposed the least squares method, it was merely a conjecture; the theoretical proof was completed by Gauss. Legendre was a prominent mathematician in the late 18th century, ranked alongside Lagrange and Laplace, known as the "Three Ls" (derived from the first letters of their names).

---

Line fitting (or linear regression) involves finding a line within a set of points $(x,y)$ such that the sum of the squared distances from all points to the line is minimized. In Numpy, the most common method for fitting is via `Polynomial.fit`:

```python
from numpy.polynomial import Polynomial
import matplotlib.pyplot as plt


x = np.linspace(0, 100, 100)

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

In many tutorials, you will see `polyfit` used for polynomial regression in Numpy. However, since version 1.4, we should use the classes and methods under the `polynomial` module. `polyfit` is considered a legacy interface. Note that although `polynomial` was designed as a replacement for functions like `polyfit`, there are significant behavioral differences.

<!--Polynomial.fit is the method for performing least-squares line fitting. It returns a Polynomial object, which has a __call__ attribute; passing x-coordinates yields the corresponding y-values.-->

---

Regarding `Polynomial.fit`, note that we passed two parameters: `deg=1` and `domain=[]`. We specify `deg=1` because we want to fit the point set represented by $(x,y)$ into a straight line; if we wish to fit a quadratic curve, we would specify `deg=2`, and so on for higher-order curves.

The `domain` parameter is optional. Omitting it does not affect our subsequent prediction of the fitted line via `fitted(x)`, but it does affect the slope we calculate (line 19). If we omit `domain = []` here, the coefficients we obtain would be [2.47, 4.57], which is far from the [0.05, 2] used when generating the data. However, when we specify `domain = []`, we see that the coefficients of the fitted line revert to our expected [0.05, 2].

!!! tip
    We can also call `fit` as follows:
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

    `convert` is a transformation function that translates and scales the domain and window.


<!--Polynomial.fit and polyfit differ significantly in behavior. polyfit returns coefficients, residuals, and other data directly, whereas Polynomial.fit returns an object; coefficients, residuals, and other data must be accessed via the object's attributes. Second, the order of coefficients differs: polyfit uses descending powers, while Polynomial uses ascending powers. Third, the coefficients differ: the object returned by Polynomial.fit automatically translates and scales the domain and window to the [-1,1] interval.-->


Linear regression is a very common technique, with similar implementations available in libraries such as scipy, sklearn, and statsmodels. Consequently, calculating slope factors for prices or moving averages is technically trivial.

---

However, what if we require *moving* linear regression? This may require some clever techniques.

## Moving Linear Regression

Moving linear regression refers to calculating another time series $S$ from a time series $T$ and a sliding window $win$, such that

$$
S_i = Slope(T_{[i-win+1, i-win+2, ..., i]})
$$

The simplest and most direct implementation is via a loop:

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
for i in range(win, len(y)):
    xi = x[i-win:i]
    yi = y[i-win:i]
    fitted = Polynomial.fit(xi, yi, deg=1, domain=[])
    S.append(fitted.coef[1])
```

---

```python
    if i in pivots:
        xj = x[i-win-10:i+10]
        y_pred = fitted(xj)
        plt.plot(xj, y_pred, '--')

print(S)
```

This code calculates the slope of the fitted line for the past 10 points starting from the 10th period, and at the turning points of the curve, we draw its tangents. These tangents are generated using the parameters of the fitted lines.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/05/xplussinx.jpg)

---

Here, we generated the curve using the equation `x + sin(x)`. You will notice that the resulting curve somewhat resembles stock price fluctuations. This is not surprising, as stock price fluctuations can essentially be decomposed into a DC component and a superposition of many sine waves. The DC component reflects the company's sustainable operating capability, while the sine waves reflect the traces left by short-term speculative capital trading in the asset.

Returning to our main topic. Now, let's remove the plotting functionality and test how long this code takes to execute:

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

90 loops took a total of 25ms. Considering that China A-shares have over 5,000 stocks, calculating this for all of them would take more than 2 minutes.

To accelerate this solution, we must rely on vectorization. However, this time, there is no magical API to call; we must roll up our sleeves, start by understanding the underlying mathematical principles, and implement it ourselves.

---

## Vectorization

Consider a linear regression with `m` points. For each point, we have:

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/05/linear-regression-group.jpg)

If all points lie on the same straight line, the following matrix equation holds:

$$
Y = A\beta + b
$$

Here, $A$ is X, and $\beta$ is the coefficient we need to solve for:

$$
\beta = {(A^TA)}^{-1}A^TY
$$

For the formula derivation, see [《Python programming and Numerical Methods - A Guide for Engineers and Scientists》](https://pythonnumericalmethods.studentorg.berkeley.edu/notebooks/chapter16.04-Least-Squares-Regression-in-Python.html).

We can manually verify this formula:

```python
x = np.linspace(0, 9, 10)
y = x + np.sin(x/10)

win = 10
```

---

```python
A = np.arange(win).reshape((win,1))
pinv = np.dot(np.linalg.inv(np.dot(A.T, A)), A.T)
alpha_1 = np.dot(pinv, y[:, np.newaxis]).item()
alpha_2 = Polynomial.fit(x, y, deg=1, domain=[]).coef[1]

np.isclose(alpha_1, alpha_2, atol=1e-2)
```

We solved for the slope using two methods, and the results show that under an absolute error constraint of 1e-2, they are identical.

Note that in line 7, we used the somewhat unusual variable name `pinv`. This is because `numpy.linalg` contains a function with the same name, which exactly calculates $ {(A^TA)}^{-1}A^T$.

However, so far, we have only accomplished what `Polynomial.fit` does. How do we calculate the slopes of fitted lines for *all* sliding windows at once?

Note that we calculate the slope via matrix multiplication. In Numpy, matrix multiplication is inherently vectorized. In line 7, `pinv` is a (1,10) matrix, and `y` is a (10,) vector. If we can stack the corresponding `pinv` matrices for each sliding window and stack `y` into a matrix as well, we can compute all slopes at once via matrix multiplication.

Let's start with `y`. When we slide `y = np.arange(5)` with a window of 3, we effectively obtain the following matrix:

$$
\begin{bmatrix}0&1&2\\1&2&3\\2&3&4\\\end{bmatrix}
$$

---

To obtain this matrix, we can use fancy indexing:

```python
y[
    [0, 1, 2],
    [1, 2, 3],
    [2, 3, 4]
]
```

Therefore, to implement the matrix for `y` under sliding windows, we only need to construct this fancy index matrix. The good news is that the fancy index matrix is highly regular:

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

<!-- Regarding rolling windows on numpy arrays: https://colab.research.google.com/drive/1Zru_-zzbtylgitbwxbi0eDBNhwr8qYl6#introduction From 1D to multi-dimensional -->
If you find this method difficult to understand, Numpy provides a function named `as_strided` that can achieve our goal in one step and is faster (by a factor of 1) than the above method:

---

```python
from numpy.lib.stride_tricks import as_strided

y = np.arange(3, 10)
stride = y.strdies[0]

win = 4
shape = (len(y) - win + 1, win)
strides = (stride, stride)
as_strided(y, shape, strides)
```

The matrix `pinv` is generated from `x`. If the time series `y` is 100 periods long, the values of `x` will range from 0 to 99. Here, $[x0, x1, ..., x_{win-1}]$ corresponds to $[y0, y1, ..., y_{win-1}]$,
$[x1, x2, ..., x_{win}]$ corresponds to $[y1, y2, ..., y_{win}]$, and $[x_{-win}, x_{-win+1}, ... x_{-1}]$ corresponds to $[y_{-win}, y_{-win+1}, ..., y_{-1}]$.

Therefore, the coefficient matrix $A$ we need to construct is:

```python
A = as_strided(np.arange(len(y)), shape, strides)
pinv = np.linalg.pinv(A)
```

The subsequent regression operations are the same as before:

```python
alpha = pinv.dot(y).sum(axis = 0)
```

The complete code is as follows:

---

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


This version is 100 times faster than the previous one using `Polynomial.fit` plus loops. You might guess that this 100x speedup is approximately equal to the number of loops. This is the cost of looping.

Now, can we use this method to accelerate other calculations? The answer is obvious. If you need to quickly calculate the 5-day moving average for 5,000 stocks over the past 10 days, and after obtaining the recent 14 days of stock prices, you form a (5000, 14) matrix $A$. What you need to do is convert this matrix into a 3D matrix, and then multiply it by a convolution kernel:

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
```

---

```python
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

The output is:

```
array([[ 2.,  3.,  4.,  5.,  6.,  7.,  8.,  9., 10., 11.],
       [12., 13., 14., 15., 16., 17., 18., 19., 20., 21.]])
```

Just as we expected. But lightning fast.

---

## Aside

Should we use fitted trend lines as a momentum factor? This is a topic worth discussing in depth. The biggest problem with slope factors is not that all time series have obvious trends. Mathematically, if the fitting residuals are large, it indicates that the time series has not yet formed a clear trend, and thus the slope factor should not be deployed. Another issue is the classic problem of linear regression: the significant impact of individual outliers on the fit. Should the fitted line minimize the sum of distances from *all* points to the line, or should it minimize the sum of distances for *most* points (which would be smaller than the former)?

## Conclusion

We discussed how to perform linear regression (line fitting) using Numpy and introduced the latest `polynomial` API. We then introduced how to implement vectorization using matrix operations. The core idea is to use the `as_strided` method to elevate the dimension of the array, and then perform matrix operations on the elevated array to achieve vectorization. We also applied the same logic to solve the problem of calculating the moving averages for 5,000 stocks at once. You also saw a practical example of using fancy indexing. This chapter contains many techniques and serves as a summary of the previous chapters.

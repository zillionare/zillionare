---
title: "QuanTide Weekly: PBOC Rate Outlook, Buffett’s Bank Moves, and Numpy Deep Dive"
date: 2024-09-08
slug: en/posts/uncategory/weekly-0908
tags: [Quantitative Investing, Numpy, Factor Mining, Market Analysis]
excerpt: "PBOC notes room for rate cuts amid constraints; Buffett trims Bank of America stake; CSI 300 breaks 2800. Plus, essential quant papers and advanced Numpy techniques for factor development."
lang: en
translation_of: posts/uncategory/weekly-0908
auto_translated: true
source_sha: fbad87c33062f79ffa40a25bc42e94071c87f78c
cover: "stamp_width: 60%"
---

### This Week’s Highlights

* PBOC: Room for Reserve Requirement Ratio (RRR) cuts exists, but further interest rate declines face constraints
* Buffett trims Bank of America stake again—shorting his own country?
* Expectations for existing mortgage rate cuts fade; CSI 300 closes below 2800 for three consecutive days

### Next Week’s Watchlist
* Monday: August CPI/PPI data release
* Monday: Kweichow Moutian earnings briefing; forecasts for the baijiu sector are a key signal

### This Week’s Selections

* Must-Read Quantitative Research Papers
* Series! Essential Numpy Programming for Quants (Part 2)

---

## This Week’s Highlights

* Zou Lan, Director of the Monetary Policy Department at the People’s Bank of China (PBOC), stated on September 5 that decisions on RRR or interest rate cuts depend on economic trends. The policy effects of the initial-year RRR cut are still materializing. Currently, the average statutory reserve requirement ratio for financial institutions is approximately 7%, leaving room for further adjustments. However, factors such as the pace of deposit flows into asset management products and the narrowing net interest margins of banks impose **constraints on further declines in deposit and lending rates**.
* On September 5 (local time), the U.S. Securities and Exchange Commission (SEC) disclosed that Warren Buffett sold approximately $760 million worth of Bank of America shares over three consecutive days around September 4. In July, he had sold Bank of America shares for nine consecutive days. Prior to these sales, Bank of America was his second-largest holding and one of the most profitable companies for Berkshire Hathaway.
* The Shanghai Composite Index (Shanghai 300) fell 2.69% this week, closing below 2800 for three consecutive days. The index’s Price-to-Earnings (PE) ratio is currently around the 12th percentile, a relatively low level. On the news front, last week’s widespread expectations for cuts on existing mortgages failed to materialize.
* New regulations on listed company IPOs for former CSRC employees have taken effect, imposing stricter requirements and broader verification scopes.

<claimer>Source: East Money, Cailian Press</claimer>


---

# Must-Read Quantitative Research Papers

1. **Portfolio Selection, Markowitz, 1952.** In this paper, Markowitz introduced Modern Portfolio Theory (MPT), for which he received the 1990 Nobel Prize in Economics. The paper extended the common risk-return tradeoff by incorporating the correlation between risk and return into calculations.
2. **A New Interpretation of Information Rate, Kelly, 1956.** This paper presents the formal statement of the famous Kelly Criterion. The model is widely used in casino games, particularly for risk management. The author derived a formula to determine optimal allocation sizes to maximize wealth growth over time.
3. **Capital Asset Prices: A Theory of Market Equilibrium under Conditions of Risk (Sharpe, 1964).** Building on Markowitz’s work, CAPM proved that there is only one efficient portfolio: the market portfolio. This paper introduced the famous Beta concept. Sharpe and Markowitz were teacher and student, respectively, and both received the Nobel Prize in Economics in the same year.
4. **Efficient Capital Markets: a Review of Theory and Empirical Work, Fama, 1970.** This paper is the seminal work that first proposed the highly popular "Efficient Market Hypothesis." Although this theory is now heavily questioned, its academic value remains high.
5. **The Pricing of Options and Corporate Liabilities, Black & Scholes, 1973.** The famous Black-Scholes formula uses the heat transfer equation from physics as a starting point for estimating option prices. This is also why hedge funds favor physics graduates.

---

6. **Does the Stock Market Overreact?, Bondt & Thaler, 1985.** This paper challenges the Efficient Market Hypothesis. Bondt and Thaler present statistically significant evidence to the contrary, suggesting that investors often overreact to unexpected news events. This is a classic study in behavioral finance, which has been a major theme for Nobel Prizes in recent years. Its underlying philosophy is subjective value theory and human-centric thinking. Thaler, also a Nobel laureate, played himself in the movie *The Big Short*.
7. **A closed-form GARCH option valuation model, Heston & Nandi, 1997.** This paper proposes a closed-form formula for valuing spot assets and modeling their variance using Generalized Autoregressive Conditional Heteroskedasticity (GARCH) models. Due to their complexity and practicality, GARCH models were widely popular for estimating volatility in the 1990s, and the financial industry actively adopted them.
8. **Optimal Execution of Portfolio Transactions, Almgren & Chriss, 2000.** For any quantitative developer responsible for refining trade execution algorithms, this paper is essential reading. The paper argues that price volatility stems from exogenous factors (market volatility) and endogenous factors (the impact of one’s own orders on the market). It’s a form of quantum effect! The authors formalized a method for executing trades and measuring execution performance by minimizing a combination of transaction costs and volatility risk.
9. **Incorporating Signals into Optimal Trading, Lehalle, 2017.** Very similar to the work of Almgren and Chriss (2000), this paper discusses optimal trade execution. The authors further refined the work in this field by incorporating Markov signals into the optimal trading framework, deriving optimal trading strategies for the special case of assets with drift (Ornstein-Uhlenbeck processes).
10. **The Performance of Mutual Funds in the Period 1945-1964, Michael Jessen.** Sharpe introduced the concept of Beta in his paper, while the concept of Alpha was introduced by Jessen in this paper.

---

11. **Common risk factors in the returns on stocks and bonds, Fama, 1993.** In this paper, Fama proposed the three-factor model.
12. **Review of Financial Studies, Stambaugh & Yuan, 2017.** This paper was published later, allowing it to review previously published, important papers related to factor investing. Thus, it has become a key paper for quickly understanding the industry. Although published late, it has already accumulated 952 citations.
13. **151 Trading Strategies, Kakushadze, 2018.** The author is from WorldQuant and is one of the authors of Alpha101. This paper cites a large number of papers (2000+), making it good material for broad reading.

---

# Essential Numpy Programming for Quants (Part 2) - Core Syntax

## 1. Structured Array

Initially, Numpy arrays could only store homogeneous elements, meaning all elements had to be of the same data type. However, for many tabular datasets, data is often composed of records, which in turn consist of data with different data types. For example, the most common market data must at least include time, security codes, and OHLC (Open, High, Low, Close) data.

To meet this need, Numpy introduced a data format called **Structured Array**. It is a **one-dimensional array** where each element is a named tuple.

We can declare a Structured Array as follows:

```python
import numpy as np
import datetime
dtypes = [
        ("frame", "O"),
        ("code", "O"),
        ("open", "f4"),
        ("high", "f4"),
        ("low", "f4"),
        ("close", "f4")
    ]
secs = np.array(
    [
        (datetime.date(2024, 3, 18), "600000", 8.9, 9.1, 8.8, 9),
        (datetime.date(2024, 3, 19), "600000", 8.9, 9.1, 8.8, 9),
    ], dtype = dtypes
)
```

---

In this data structure, there are 6 fields, with their names and types defined via `dtype`. This is a `List[Tuple]` type. In the initialization data part, it is also a `List[Tuple]`.

!!! warning
    A common mistake for beginners is using `List[List]` to initialize a Numpy Structured Array instead of `List[Tuple]`. This causes Numpy to fail to map to the correct data type during array construction, resulting in strange errors.<br>For example, the following initialization is incorrect:

    ```python
    secs = np.array([
        [datetime.date(2024, 3, 18), "600000", 8.9, 9.1, 8.8, 9],
        [datetime.date(2024, 3, 19), "600000", 8.9, 9.1, 8.8, 9]
    ], dtype=dtypes)
    ```
    This code will report an obscure "Type Error: float() argument must be a string or ..."

We can use the inspection methods learned in the previous section to view some characteristics of the `secs` array:

```python
print(f"secs dimension is {secs.ndim}")
print(f"secs shape is {secs.shape}")
print(f"secs size is {secs.size}")
print(f"secs length is {len(secs)}")

print(f"secs[0] type is {type(secs[0])}")
print(f"secs[0] dimension is {secs[0].ndim}")
print(f"secs[0] shape is {secs[0].shape}")
print(f"secs[0] size is {secs[0].size}")
print(f"secs[0] length is {len(secs[0])}")
```

As shown, the `secs` array is a **one-dimensional array**, and its shape `(2,)` is also the representation of a one-dimensional array's shape. We introduced the relationship between these attributes in the previous section; you can verify if they still hold.

<!--
Here, size still equals the product of the values of each element in shape. Note that for `secs`, its size equals its length, but for `secs[0]`, its size and length are not equal. We encountered a bug related to this when developing Monopoly.
-->
---

However, the element type of `secs` is `numpy.void`, which is essentially a named tuple. Therefore, we can access any field within it as follows:

```python
print(secs[0]["frame"])

# It is also possible to use the index number instead of the column name (field name)
print(secs[0][0])
```

We can also access a "cell" in column-major order:

```python
print(secs["frame"][0])
```

For tabular data, iteration is a common operation. We can iterate as follows:

```python
for (frame, code, opn, high, low, close) in secs:
    print(frame, code, opn, high, low, close)
```

The syntax for Numpy structured arrays in this part is much more user-friendly than Pandas' DataFrame. We will mention this again when introducing Pandas later.

<!--Common Mistake:

When modifying cell values, the following syntax cannot be interchanged:
    ```python
        data = np.array([("aaron", "label")], dtype=[("name", "O"), ("label", "O")])
        filter = data["name"] == "aaron"

        new_label = "blogger"
        data["label"][filter] = new_label

        # this won't change
        data[filter]["label"] = new_label
    ```

-->

## 2. Operations
### 2.1. Comparison and Logical Operations

In the previous section on positioning and searching, we encountered comparisons, such as `arr > 1`. This compares every element in the array with 1 and returns a boolean array.

Now, we will expand the comparison instructions:

---

| Function    | Description                                                                                          |
| ----------- | ---------------------------------------------------------------------------------------------------- |
| all         | Returns True if all elements in the array are true. Used to check if a set of conditions holds simultaneously. |
| any         | Returns True if at least one element in the array is true. Used to check if at least one condition holds.      |
| isclose     | Checks if elements in two arrays are approximately equal element-wise, returning all comparison results.   |
| allclose    | Checks if all elements in two arrays are approximately equal.                                          |
| equal       | Checks if elements in two arrays are equal element-wise, returning all comparison results.               |
| not_equal   | Checks if elements in two arrays are not equal element-wise, returning all comparison results.           |
| isfinite    | Checks if the value is a number and not infinite.                                                      |
| isnan       | Tests if the value is Not a Number.                                                                  |
| isnat       | Tests if the object is not a time type.                                                              |
| isneginf    | Tests if the object is negative infinity.                                                            |
| isposinf    | Tests if the object is positive infinity.                                                            |

```python
# Enable multi-line output mode
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

np.random.seed(78)
returns = np.random.normal(0, 0.03, size=4)
returns
# Check if all are down
np.all(returns <= 0)
np.any(returns <= 0)

# Simulate a price sequence starting at 8 yuan
prices = np.cumprod(1+returns) * 8

# Corresponding price limit prices are as follows
buy_limit_prices = [8.03, 8.1, 8.1, 8.3]

# Check if price limit is hit
np.isclose(prices, buy_limit_prices, atol=1e-2)
```

<!--Why do functions for judging approximate equality exist? This is because numbers are divided into integer and floating-point types. Any number with a decimal point can be considered a floating-point type. Floating-point numbers cannot be expressed exactly, so they are never strictly equal. Instead, we compare the difference between two floating-point numbers. If the absolute value of the difference is less than an acceptable small number, we consider them approximately equal.

Therefore, if we have the closing price and price limit of a stock, to check if the stock has hit the price limit, we must use `isclose` for comparison, not `equal`.

The parameter `atol` represents absolute error, indicating that if the difference between two floating-point numbers is less than this value, they are considered approximately equal.
-->

In addition to checking if all elements in an array are True or if at least one is True, sometimes we want to perform fuzzier judgments. For example, if more than 60% of the past 20 days showed bullish candles (closing above opening), we can use `np.count_nonzero` or `np.sum` to count the number of True values in the array:

---

```python
np.count_nonzero(returns > 0)
np.sum(returns > 0)
```

In the previous section's comparison examples, we only used single conditions. If we need to search based on combinations of multiple conditions, we must rely on logical operations.

In Numpy, logical operations can be performed via functions or operators:

| Function      | Operator | Description             | Python Equivalent |
| ------------- | -------- | ----------------------- | ----------------- |
| logical_and   | &        | Performs logical AND    | and               |
| logical_or    | \|       | Performs logical OR     | or                |
| logical_not   | ~        | Performs logical NOT    | not               |
| logical_xor   | '^'      | Performs logical XOR    | xor               |

<!--

If you are not very familiar with programming languages, you might find it difficult to understand these boolean operations, but they are widely used in quantitative finance, and we will encounter them again when discussing Pandas.

The meaning of logical AND a&b is that the expression holds only when both conditions a and b are true.
The meaning of logical OR a|b is that the expression holds if either a or b is true.
The meaning of logical NOT ~b is that if b is true, the expression does not hold, and vice versa.
The meaning of logical XOR a ^ b is that...
-->

What is the use of logical operations? For example, when stock selection, we have the following tabular data:

| Stock | pe    | mom  |
| ----- | ----- | ---- |
| AAPL  | 30.5  | 0.1  |
| GOOG  | 32.3  | 0.3  |
| TSLA  | 900.1 | 0.5  |
| MSFT  | 35.6  | 0.05 |

The above table can be represented as a Numpy Structured Array:

```
tickers = np.array([
    ("APPL", 30.5, 0.1),
    ("GOOG", 32.3, 0.3),
    ("TSLA", 900.1, 0.5),
    ("MSFT", 35.6, 0.05)
], dtype=[("ticker", "O"), ("pe", "f4"), ("mom", "f4")])
```


Now, we want to find records where PE < 35 and momentum (mom) > 0.2. We can construct the condition expression as follows:

---

```python
(tickers["pe"] < 35) & (tickers["mom"] > 0.2)
```

Numpy will compare all values in the `pe` column with 35, and then perform a logical AND operation with the result of comparing `mom` with 0.2. This is equivalent

# Numpy Data Types & Factor Investing Course Launch

This article introduces Numpy’s core data types and aliases, then promotes an upcoming online course on factor investing and machine learning strategies.

Tags: Numpy, Factor Investing, Quantitative Trading, Machine Learning

## 4. Further Reading

### 4.1. Numpy Data Types

In Numpy, the following common data types are available. Each numeric type has an alias. In most cases, both the full type name and the alias can be used wherever a `dtype` argument is required. However, aliases are better supported for string, time, and date types. For example, `'S5'` is an alias for an ASCII string that specifies both the data type and the string length. Similarly, `datetime64[S]` indicates a datetime type with second-level precision.

---

| Type           | Alias                         | Category    | Alias                                                                                                           |
| -------------- | ----------------------------- | ----------- | -------------------------------------------------------------------------------------------------------------- |
| np.int8        | i1                            | np.float16  | f2                                                                                                             |
| np.int16       | i2                            | np.float32  | f4, with optional byte-order suffixes (e.g., `'<f4'` for little-endian, `'='` for native, `'>f4'` for big-endian). Other float types follow the same convention. |
| np.int32       | i4                            | np.float64  | f8                                                                                                             |
| np.int64       | i8                            | np.float128 | f16                                                                                                            |
| np.uint8       | u1                            | np.bool_    | b1                                                                                                             |
| np.uint16      | u2                            | np.str_     | U (followed by length, e.g., U10)                                                                              |
| np.uint32      | u4                            | np.bytes_   | S (followed by length, e.g., S5)                                                                               |
| np.uint64      | u8                            |             | np.datetime64: M8, M8[D], M8[h], M8[m], M8[s], or datetime64[D], etc.                                          |
| np.timedelta64 | m8, m8[D], m8[h], m8[m], m8[s], etc. |             |                                                                                                                |

---

## Course Launch: Factor Investing and Machine Learning Strategies

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/course/factor-ml/1.png)

---

## Online Live Stream on September 8th. Don’t Miss It

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/course/factor-ml/2.png)

---

## ![Click to Join](https://cdn.jsdelivr.net/gh/zillionare/imgbed2@main/images/2026/10/20261005065435-j6WuV9fNCB9w.jpg)

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/course/factor-ml/3.png)

<about/>

---
title: "Pandas for Quant: Logic, Grouping, Indexing, and Stats"
date: 2025-03-31
slug: en/articles/python/numpy-pandas/14-pandas核心语法-4
tags: [Pandas, Quantitative Finance, Data Analysis, Factor Investing]
excerpt: "Master Pandas for quantitative finance: logical filtering, groupby, MultiIndex, window functions, and statistical operations for factor analysis and data processing."
lang: en
translation_of: articles/python/numpy-pandas/14-pandas核心语法-4
auto_translated: true
source_sha: ffa20392464f80e1a64f74138bf8c40fca969b9e
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/mybook/girl-hold-book-face.jpg"
---

In Pandas, logical and comparison operations are the foundational tools for data filtering. By leveraging operators such as AND (`&`), OR (`|`), and others, you can easily implement complex conditional filtering—for instance, selecting stocks with the highest Price-to-Earnings (PE) ratio and the lowest Price-to-Book (PB) ratio.

---

## 1. Logical and Comparison Operations
<!--_The dataframe contains the extracted features. How do we select the top 30 columns with the highest PE and lowest PB?_-->
In Pandas, logical and comparison operations on DataFrames are commonly used for data processing, primarily for filtering and screening data. The following details and implementation methods are provided:

### 1.1. Logical Operations on DataFrame

Logical operations include AND (`&`), OR (`|`), NOT (`~`), and XOR (`^`), and are typically used in conjunction with comparison operations. Example code:

```python
import pandas as pd

# 创建示例 DataFrame
df = pd.DataFrame({
    'A': [True, False, True],
    'B': [False, True, False]
})

# 与运算
print(df['A'] & df['B'])

# 或运算
print(df['A'] | df['B'])

# 非运算
print(~df['A'])

# 异或运算
print(df['A'] ^ df['B'])
```

---

Output:

```python
0    False
1    False
2    False
dtype: bool
0     True
1     True
2     True
dtype: bool
0    False
1     True
2    False
dtype: bool
0     True
1     True
2     True
dtype: bool
```

### 1.2. Comparison Operations on DataFrame
Comparison operations include `>`, `<`, `==`, `!=`, `>=`, and `<=`, returning a DataFrame or Series composed of boolean values.

Example code:

```python
# 创建示例 DataFrame
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
})
```

---

```python
# 比较运算
print(df['A'] > 1)  # 返回布尔 Series
print(df > 2)       # 返回布尔 DataFrame
```

Output:

```python
0    False
1     True
2     True
Name: A, dtype: bool
       A      B
0  False   True
1  False   True
2   True   True
```

**The DataFrame contains the extracted features. How do we select the top 30 columns with the highest PE and lowest PB?**

Assume the DataFrame contains the following features:
- PE: Price-to-Earnings ratio
- PB: Price-to-Book ratio

```python
import pandas as pd

# 创建示例 DataFrame
data = {
    'PE': [10, 20, 30, 40, 50],
    'PB': [1.5, 1.2, 1.0, 0.8, 0.5]
}
df = pd.DataFrame(data)
```

---

To select the top 30 columns with the highest PE and lowest PB, follow these steps:
1. Calculate the maximum PE and minimum PB.
2. Filter the data based on these conditions.
3. Select the top 30 columns.

```python
# 筛选 PE 最大且 PB 最小的行
filtered_df = df[(df['PE'] == df['PE'].max()) & (df['PB'] == df['PB'].min())]

# 选取前 30 列（假设列数足够）
result = filtered_df.iloc[:, :30]
print(result)
```

Output:
```python
   PE   PB
4  50  0.5
```


## 2. Grouping Operations (groupby)
<!--_The factor analysis data table includes industry labels and each company's PE value. How do we select the top 5 companies with the strongest PE in each industry?_-->
In Pandas, `groupby` is the core method for performing grouped operations on a DataFrame. It follows a "split-apply-combine" logic: first, data is grouped by specified conditions; then, operations are executed on each group; finally, the results are combined. The following details and specific implementation methods are provided:

### 2.1. Basic Syntax of groupby

---

The basic syntax for `groupby` is:

```python
df.groupby(by=分组键)[选择列].聚合函数
```

- **by**: Specifies the column name(s) for grouping.
- **Selection**: Optional; specifies the columns to operate on.
- **Aggregation functions**: Such as `sum()`, `mean()`, `max()`, etc.

Example:
```python
import pandas as pd
# 创建示例 DataFrame
data = {'行业': ['科技', '科技', '金融', '金融', '科技'],
        '公司': ['A', 'B', 'C', 'D', 'E'],
        'PE': [30, 25, 15, 20, 35]}
df = pd.DataFrame(data)
# 按行业分组并计算平均 PE
result = df.groupby('行业')['PE'].mean()
print(result)
```

Output:

```python
行业
科技    30.0
金融    17.5
Name: PE, dtype: float64
```

---

### 2.2. Applications of groupby
Assume your factor analysis data table includes the following columns:
- Industry label: Indicates the industry to which the company belongs.
- PE value: Indicates the company's Price-to-Earnings ratio.

Sample data:
```python
data = {'行业': ['科技', '科技', '金融', '金融', '科技', '金融'],
        '公司': ['A', 'B', 'C', 'D', 'E', 'F'],
        'PE': [30, 25, 15, 20, 35, 10]}
df = pd.DataFrame(data)
```

To select the top 5 companies with the strongest PE in each industry, "strongest PE" can be interpreted as the companies with the highest PE values. The implementation steps are as follows:
1. Group by industry.
2. Sort each group by PE value in descending order.
3. Select the top 5 rows from each group.

```python
# 按行业分组，并对每个分组按 PE 值降序排序
grouped = df.groupby('行业', group_keys=False)

# 选取每个行业 PE 值最高的 5 家公司
result = grouped.apply(lambda x: x.nlargest(5, 'PE'))
print(result)
```

Output:

---

```python
   行业 公司  PE
0  科技  A  30
4  科技  E  35
1  科技  B  25
2  金融  C  15
3  金融  D  20
5  金融  F  10
```

## 3. MultiIndex and Advanced Indexing
<!--_This is one of the more complex topics in Pandas._-->
In Pandas, MultiIndex and advanced indexing on DataFrames are essential tools for handling complex data structures. They allow you to create multiple levels of indexing on a single axis, enabling more flexible organization and access to data. The following details are provided:

### 3.1. MultiIndex

MultiIndex refers to having multiple levels of indexing on a single axis (row or column). It is suitable for handling data with hierarchical structures, such as data classified by region and time.

#### 3.1.1. Creating MultiIndex
Pandas provides various methods to create MultiIndex. The common approaches are:

[Create from arrays]
```python
import pandas as pd
arrays = [['A', 'A', 'B', 'B'], [1, 2, 1, 2]]
multi_index = pd.MultiIndex.from_arrays(arrays, 
                names=('Letter', 'Number'))
```

---

```python
df = pd.DataFrame({'Value': [10, 20, 30, 40]}, index=multi_index)
print(df)
```

[Create from tuples]
```python
tuples = [('A', 1), ('A', 2), ('B', 1), ('B', 2)]
multi_index = pd.MultiIndex.from_tuples(tuples, names=('Letter', 'Number'))
df = pd.DataFrame({'Value': [10, 20, 30, 40]}, index=multi_index)
print(df)
```

[Create from Cartesian product]
```python
letters = ['A', 'B']
numbers = [1, 2]
multi_index = pd.MultiIndex.from_product([letters, numbers], names=('Letter', 'Number'))
df = pd.DataFrame({'Value': [10, 20, 30, 40]}, index=multi_index)
print(df)
```

#### 3.1.2. Accessing MultiIndex Data
Access using `loc`:
```python
print(df.loc[('A', 1)])  # 访问特定行
```

Cross-selection using `xs`:

---

```python
print(df.xs(1, level='Number'))  # 获取第二层级索引为 1 的所有行
```

Using slice objects:
```python
print(df.loc[pd.IndexSlice[:, 2], :])  # 获取第二层级索引为 2 的所有行
```

#### 3.1.3. Operating on MultiIndex
Swap levels:
```python
df_swapped = df.swaplevel(0, 1)
print(df_swapped)
```

Reorder levels:
```python
df_sorted = df.sort_index(level='Number')
print(df_sorted)
```

Reset index:
```python
df_reset = df.reset_index()
print(df_reset)
```

### 3.2. Advanced Indexing

---

Advanced indexing refers to using more flexible methods to select and manipulate data based on MultiIndex.

#### 3.2.1. Reindexing with `reindex`
`reindex` rearranges data according to specified indices and fills missing values:

```python
new_index = [('B', 2), ('A', 1), ('C', 3)]
df_reindexed = df.reindex(new_index)
print(df_reindexed)
```

#### 3.2.2. Aligning Indices with `align`
`align` aligns two DataFrames with different indices:

```python
df1 = pd.DataFrame({'Value': [10, 20]}, index=[('A', 1), ('B', 2)])
df2 = pd.DataFrame({'Value': [30, 40]}, index=[('B', 2), ('C', 3)])
aligned_df1, aligned_df2 = df1.align(df2)
print(aligned_df1)
print(aligned_df2)
```

!!! Notes
    - **MultiIndex**: Create multi-level indices via `MultiIndex`, supporting flexible data organization and access.
    - **Advanced Indexing**: Implement complex data operations via methods such as `reindex`, `align`, and `groupby`.

    By mastering MultiIndex and advanced indexing, you can handle and analyze complex data more efficiently.

---

## 4. Window Functions
<!--_Used to calculate sliding window indicators such as moving averages._-->
Window functions in Pandas are powerful tools for performing sliding window calculations on data. They are typically used for time-series or ordered data, supporting rolling calculations, expanding calculations, and exponential weighted moving operations. The following details the window functions in Pandas.

### 4.1. Basic Concepts of Window Functions

Window functions are a special type of function that calculates data within a fixed-size window and returns results with the same quantity as the original data. Common window functions include:

- **Rolling Window**: Calculates data within a fixed-size window.
- **Expanding Window**: Gradually increases the window size from the first data point until it includes all data points.
- **Exponentially Weighted Moving Window**: Assigns higher weights to recent data and lower weights to distant data.

### 4.2. Rolling Window

Rolling windows are used to calculate data within a fixed-size window. For example, calculating the average or maximum value over the past 5 days.

```python
import pandas as pd

# 创建示例 DataFrame
data = {'value': [1, 2, 3, 4, 5, 6, 7, 8, 9]}
df = pd.DataFrame(data)
```

---


```python
# 计算滚动平均值，窗口大小为 3
df['rolling_mean'] = df['value'].rolling(window=3).mean()
print(df)
```

Parameter description:
- **window**: Window size.
- **min_periods**: Minimum number of data points required in the window; otherwise, the result is `NaN`.
- **center**: Whether to center the window around the current row.


### 4.3. Expanding Window

Expanding windows start from the first data point and gradually increase the window size until all data points are included. They are typically used to calculate cumulative sums, cumulative averages, etc.

```python
# 计算累计和
df['expanding_sum'] = df['value'].expanding().sum()
print(df)
```

### 4.4. Exponentially Weighted Moving Window

Exponentially weighted moving windows assign higher weights to recent data and lower weights to distant data. This is very useful in financial data analysis.

---

```python
# 计算指数加权移动平均
df['ewm_mean'] = df['value'].ewm(span=3).mean()
print(df)
```

Parameter description:
- **span**: Specifies the decay coefficient.
- **alpha**: Directly specifies the decay factor.


!!! Notes
    - **Selection of window size**: Choose the window size based on specific application scenarios and data characteristics. Too small a window may cause significant fluctuations in results, while too large a window may obscure important details.
    - **Handling boundary values**: Use the `min_periods` parameter to control the minimum window size and avoid `NaN` values.
    - **Handling missing data**: Use `fillna()` to fill missing values or `dropna()` to remove them.

## 5. Mathematical and Statistical Operations
<!--_Statistical functions such as mean, variance, covariance, percentile, diff, pct_change, rank, etc., which are fundamental to quantitative finance._-->
In Pandas, DataFrames provide a rich set of mathematical and statistical functions, facilitating convenient data calculation and analysis.

### 5.1. Mathematical Operations

Pandas supports basic mathematical operations on DataFrames, including addition, subtraction, multiplication, and division. These operations can be performed element-wise or on entire columns or rows.
Example code:

---

```python
import pandas as pd

# 创建示例 DataFrame
data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
df = pd.DataFrame(data)

# 加法
df['C'] = df['A'] + df['B']

# 减法
df['D'] = df['A'] - df['B']

# 乘法
df['E'] = df['A'] * df['B']

# 除法
df['F'] = df['A'] / df['B']

print(df)
```

Output:

```python
   A  B  C  D   E    F
0  1  4  5 -3   4  0.25
1  2  5  7 -3  10  0.40
2  3  6  9 -3  18  0.50
```

Other mathematical operations:
- **Power operation**: `df['A'] ** 2`
- **Square root**: `df['A'].pow(0.5)`
- **Logarithmic operation**: `df['A'].apply(np.log)` (requires importing the `numpy` library)

---

### 5.2. Statistical Calculations
Pandas provides various statistical methods for analyzing data in DataFrames.

Common statistical methods:
- **Sum**: `df.sum()`
- **Mean**: `df.mean()`
- **Max**: `df.max()`
- **Min**: `df.min()`
- **Standard deviation**: `df.std()`
- **Variance**: `df.var()`
- **Median**: `df.median()`
- **Mode**: `df.mode()`
- **Quantile**: `df.quantile(q=0.25)` (calculates the 25th percentile)

Example code:

```python
# 计算各列的和
sum_result = df.sum()

# 计算各列的平均值
mean_result = df.mean()

# 计算各列的最大值
max_result = df.max()

# 计算各列的最小值
min_result = df.min()
```

---

```python
# 计算各列的标准差
std_result = df.std()

# 计算描述性统计信息
desc_stats = df.describe()

print(desc_stats)
```

Output:

```python
              A         B         C         D         E         F
count  3.000000  3.000000  3.000000  3.000000  3.000000  3.000000
mean   2.000000  5.000000  7.000000 -3.000000 10.666667  0.383333
std    1.000000  1.000000  2.000000  0.000000  7.023796  0.125833
min    1.000000  4.000000  5.000000 -3.000000  4.000000  0.250000
25%    1.500000  4.500000  6.000000 -3.000000  7.000000  0.325000
50%    2.000000  5.000000  7.000000 -3.000000 10.000000  0.400000
75%    2.500000  5.500000  8.000000 -3.000000 14.000000  0.450000
max    3.000000  6.000000  9.000000 -3.000000 18.000000  0.500000
```

### 5.3. Advanced Statistical Functions

Pandas also supports more complex statistical operations, such as:
- **Cumulative statistics**: `df.cumsum()` (cumulative sum), `df.cummax()` (cumulative maximum)
- **Correlation analysis**: `df.corr()` (calculates the correlation coefficient matrix)
- **Covariance analysis**: `df.cov()` (calculates the covariance matrix)
- **Skewness and kurtosis**: `df.skew()` (skewness), `df.kurtosis()` (kurtosis)


Example code:

---

```python
# 计算累计和
cumsum_result = df.cumsum()

# 计算相关系数矩阵
corr_matrix = df.corr()

# 计算协方差矩阵
cov_matrix = df.cov()

print(corr_matrix)
```

### 5.4. Grouped Statistics
The `groupby` method in Pandas can group data and then perform statistical calculations on each group. Example code:

```python
# 创建示例 DataFrame
data = {'Category': ['A', 'B', 'A', 'B', 'A'], 'Value': [10, 20, 30, 40, 50]}
df = pd.DataFrame(data)

# 按 Category 分组并计算每组的平均值
grouped_stats = df.groupby('Category').mean()
print(grouped_stats)
```
```python
          Value
Category       
A           30.0
B           30.0
```

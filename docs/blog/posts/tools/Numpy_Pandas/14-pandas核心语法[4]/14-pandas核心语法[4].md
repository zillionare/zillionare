---
title: Pandas核心语法[4]
series: 量化人的 Numpy 和 Pandas
seq: "4"
fonts:
    sans: 'AlibabaPuHuiTi-Thin, sans-serif'
slug: numpy-pandas-for-quant-trader-14
date: 2025-03-31
category: tools
motto: The greatest discovery of all time is that a person can change his future by merely changing his attitude.
img: https://images.jieyu.ai/images/hot/mybook/girl-hold-book-face.jpg
stamp_width: 60%
stamp_height: 60%
tags: 
    - tools
    - programming
    - Numpy
    - Pandas
---

“在 Pandas 中，逻辑运算和比较运算是数据筛选的基础工具。通过与（&）、或（|）等操作符，可以轻松实现复杂条件筛选，比如选出市盈率最大且市净率最小的股票。”

---

## 1. 逻辑运算和比较
<!--_dataframe中包含了我们提取的特征。要选取PE最大同时是PB最小的前30列，怎么做？_-->
在 Pandas 中，DataFrame 的逻辑运算和比较是数据处理中常用的操作，主要用于筛选和过滤数据。以下是详细说明和实现方法：
### 1.1. DataFrame 的逻辑运算

逻辑运算包括与（&）、或（|）、非（~）和异或（^），通常与比较运算结合使用。示例代码：

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

输出结果：

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

### 1.2. DataFrame 的比较运算
比较运算包括 >、<、==、!=、>=、<=，返回布尔值组成的 DataFrame 或 Series。

示例代码：

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

输出结果：

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

**Dataframe中包含了我们提取的特征。要选取PE最大同时是PB最小的前30列，怎么做？**

假设 DataFrame 中包含以下特征：
- PE：市盈率
- PB：市净率

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

选取 PE 最大且 PB 最小的前 30 列, 要实现这一需求，可以按照以下步骤操作：
1. 计算 PE 的最大值和 PB 的最小值。
2. 根据条件筛选数据。
3. 选取前 30 列。

```python
# 筛选 PE 最大且 PB 最小的行
filtered_df = df[(df['PE'] == df['PE'].max()) & (df['PB'] == df['PB'].min())]

# 选取前 30 列（假设列数足够）
result = filtered_df.iloc[:, :30]
print(result)
```

输出结果：
```python
   PE   PB
4  50  0.5
```


## 2. 分组运算（groupby）
<!--_因子分析数据表包含了行业标签和各公司的PE值。如何选出每个行业PE最强的5支_-->
在 Pandas 中，groupby 是用于对 DataFrame 进行分组运算的核心方法。它遵循“拆分-应用-合并”的逻辑，即先将数据按指定条件分组，然后对每个分组执行操作，最后将结果合并。以下是详细说明和具体实现方法：

### 2.1. groupby 的基本语法

---

groupby 的基本语法为：

```python
df.groupby(by=分组键)[选择列].聚合函数
```

- ​**by**：指定分组的列名或列名列表。
- ​选择列：可选，指定需要操作的列。
- ​聚合函数：如 sum()、mean()、max() 等。

示例：
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

输出结果：

```python
行业
科技    30.0
金融    17.5
Name: PE, dtype: float64
```

---

### 2.2. groupby 的应用
假设你的因子分析数据表包含以下列：
- ​行业标签：表示公司所属的行业。
- ​PE值：表示公司的市盈率。

示例数据：
```python
data = {'行业': ['科技', '科技', '金融', '金融', '科技', '金融'],
        '公司': ['A', 'B', 'C', 'D', 'E', 'F'],
        'PE': [30, 25, 15, 20, 35, 10]}
df = pd.DataFrame(data)
```

选出每个行业 PE 最强的 5 支, “PE 最强”可以理解为 PE 值最高的公司。以下是实现步骤：
1. 按行业分组。
2. 对每个分组按 PE 值降序排序。
3. 选取每个分组的前 5 行。

```python
# 按行业分组，并对每个分组按 PE 值降序排序
grouped = df.groupby('行业', group_keys=False)

# 选取每个行业 PE 值最高的 5 家公司
result = grouped.apply(lambda x: x.nlargest(5, 'PE'))
print(result)
```

输出结果：

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

## 3. 多重索引和高级索引
<!--_这是pandas中比较难懂的内容之一_-->
在 Pandas 中，DataFrame 的多重索引（MultiIndex）和高级索引是处理复杂数据结构的重要工具。它们允许你在一个轴上创建多个层级的索引，从而更灵活地组织和访问数据。以下是详细说明：

### 3.1. ​多重索引（MultiIndex）​
多重索引是指在一个轴上（行或列）拥有多个层级的索引。它适用于处理具有层次化结构的数据，例如按地区和时间分类的数据。

#### 3.1.1. 创建多重索引
Pandas 提供了多种方法创建多重索引，以下是常见的方式：

[​从数组创建]
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

[从元组创建]
```python
tuples = [('A', 1), ('A', 2), ('B', 1), ('B', 2)]
multi_index = pd.MultiIndex.from_tuples(tuples, names=('Letter', 'Number'))
df = pd.DataFrame({'Value': [10, 20, 30, 40]}, index=multi_index)
print(df)
```

[从笛卡尔积创建]
```python
letters = ['A', 'B']
numbers = [1, 2]
multi_index = pd.MultiIndex.from_product([letters, numbers], names=('Letter', 'Number'))
df = pd.DataFrame({'Value': [10, 20, 30, 40]}, index=multi_index)
print(df)
```

#### 3.1.2. ​访问多重索引数据
使用 loc 访问：
```python
print(df.loc[('A', 1)])  # 访问特定行
```

​使用 xs 交叉选择：

---

```python
print(df.xs(1, level='Number'))  # 获取第二层级索引为 1 的所有行
```

​使用切片器：
```python
print(df.loc[pd.IndexSlice[:, 2], :])  # 获取第二层级索引为 2 的所有行
```

#### 3.1.3 ​操作多重索引
​交换层级：
```python
df_swapped = df.swaplevel(0, 1)
print(df_swapped)
```

​重排序层级：
```python
df_sorted = df.sort_index(level='Number')
print(df_sorted)
```

​重置索引：
```python
df_reset = df.reset_index()
print(df_reset)
```

### 3.2. ​高级索引

---

高级索引是指在多重索引的基础上，使用更灵活的方法选择和操作数据。

#### 3.2.1. ​使用 reindex 重新索引
reindex 可以根据指定的索引重新排列数据，并填充缺失值：

```python
new_index = [('B', 2), ('A', 1), ('C', 3)]
df_reindexed = df.reindex(new_index)
print(df_reindexed)
```

#### 3.2.2. ​使用 align 对齐索引
align 可以将两个具有不同索引的 DataFrame 对齐：

```python
df1 = pd.DataFrame({'Value': [10, 20]}, index=[('A', 1), ('B', 2)])
df2 = pd.DataFrame({'Value': [30, 40]}, index=[('B', 2), ('C', 3)])
aligned_df1, aligned_df2 = df1.align(df2)
print(aligned_df1)
print(aligned_df2)
```

!!! Notes
    - 多重索引：通过 MultiIndex 创建多层级索引，支持灵活的数据组织和访问。
    - ​高级索引：通过 reindex、align、groupby 等方法实现复杂的数据操作。

    通过熟练掌握多重索引和高级索引，可以更高效地处理和分析复杂数据。

---

## 4. 窗口函数
<!--_用以计算移动平均等具有滑动窗口的指标_-->
Pandas 中的窗口函数（Window Functions）是一种强大的工具，用于对数据进行滑动窗口计算。它们通常用于时间序列数据或有序数据，支持滚动计算、扩展计算和指数加权移动等操作。以下是 Pandas 中窗口函数的详细说明。

### 4.1. ​窗口函数的基本概念

窗口函数是一种特殊的函数，它在一个固定大小的窗口内对数据进行计算，并返回与原始数据相同数量的结果。常见的窗口函数包括：

- ​滚动窗口（Rolling Window）​：在一个固定大小的窗口内对数据进行计算。
- ​扩展窗口（Expanding Window）​：从第一个数据点开始，逐步增加窗口大小，直到包含所有数据点。
- ​指数加权移动窗口（Exponentially Weighted Moving Window）​：对较近的数据赋予更高的权重，较远的数据赋予较低的权重。

### 4.2. ​滚动窗口（Rolling Window）​
滚动窗口用于在固定大小的窗口内对数据进行计算。例如，计算过去 5 天的平均值或最大值。

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

参数说明：
- ​**window**：窗口大小。
- ​**min_periods**：窗口中需要的最小数据点数量，否则结果为 NaN。
- ​**center**：是否以当前行为中心划分窗口。


### 4.3. 扩展窗口（Expanding Window）​
扩展窗口从第一个数据点开始，逐步增加窗口大小，直到包含所有数据点。它通常用于计算累计和、累计平均等。

```python
# 计算累计和
df['expanding_sum'] = df['value'].expanding().sum()
print(df)
```

### 4.4. 指数加权移动窗口（Exponentially Weighted Moving Window）​
指数加权移动窗口对较近的数据赋予更高的权重，较远的数据赋予较低的权重。它在金融数据分析中非常有用。

---

```python
# 计算指数加权移动平均
df['ewm_mean'] = df['value'].ewm(span=3).mean()
print(df)
```

参数说明：
- ​**span**：指定衰减系数。
- ​**alpha**：直接指定衰减因子。


!!! Notes
    - 窗口大小的选择：根据具体应用场景和数据特点选择窗口大小，过小可能导致结果波动较大，过大可能掩盖重要细节。
    - ​边界值处理：使用 min_periods 参数控制最小窗口大小，避免 NaN 值。
    - 数据缺失处理：使用 fillna() 填充缺失值或 dropna() 删除缺失值。

## 5. 数学运算和统计
<!--_均值、方差、协方差、percentile,diff,pct_change,rank 等统计函数，量化基础_-->
在 Pandas 中，DataFrame 提供了丰富的数学运算和统计功能，能够方便地对数据进行计算和分析。

### 5.1. ​数学运算

Pandas 支持对 DataFrame 进行基本的数学运算，包括加法、减法、乘法、除法等。这些运算可以逐元素进行，也可以对整列或整行进行操作。
示例代码：

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

输出结果：

```python
   A  B  C  D   E    F
0  1  4  5 -3   4  0.25
1  2  5  7 -3  10  0.40
2  3  6  9 -3  18  0.50
```

其他数学运算：
- ​幂运算：df['A'] ​** 2
- ​平方根：df['A'].pow(0.5)
- ​对数运算：df['A'].apply(np.log)（需导入 numpy 库）

---

### 5.2. ​统计计算
Pandas 提供了多种统计方法，用于对 DataFrame 中的数据进行分析。

常用统计方法：
- ​求和：df.sum()
- ​平均值：df.mean()
- ​最大值：df.max()
- ​最小值：df.min()
- ​标准差：df.std()
- ​方差：df.var()
- ​中位数：df.median()
- ​众数：df.mode()
- ​分位数：df.quantile(q=0.25)（计算 25% 分位数）

示例代码：

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

输出结果：

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

### 5.3. ​高级统计功能

Pandas 还支持更复杂的统计操作，例如：
- ​累计统计：df.cumsum()（累计和）、df.cummax()（累计最大值）
- ​相关性分析：df.corr()（计算相关系数矩阵）
- ​协方差分析：df.cov()（计算协方差矩阵）
- ​偏度和峰度：df.skew()（偏度）、df.kurtosis()（峰度）


示例代码：

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

### 5.4. ​分组统计
Pandas 的 groupby 方法可以对数据进行分组，然后对每个分组进行统计计算。示例代码：

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
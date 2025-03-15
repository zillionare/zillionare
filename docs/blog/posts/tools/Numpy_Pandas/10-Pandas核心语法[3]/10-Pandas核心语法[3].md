---
title: 量化人怎么用Pandas——核心语法[3]
slug: numpy-pandas-for-quant-trader-10
date: 2025-03-15
category: tools
motto: The only way to do great work is to love what you do.
img: https://images.jieyu.ai/images/2024/12/book-of-sun-le.jpg
stamp_width: 60%
stamp_height: 60%
tags: 
    - tools
    - programming
    - Numpy
    - Pandas
---

Pandas在量化交易中，处于核心地位。许多基于Python SDK的数据源返回的数据格式一般是pandas.DataFrame。因子分析库Alphalens、性能评估库empyrical等都依赖于Pandas。

这并不奇怪。因为Pandas的开发者Wes McKinney原本是资管公司AQR Capital Management的研究员。他在处理大量金融分析任务时，发现Python的现有工具（如NumPy）无法高效处理结构化数据分析，于是在2008年开始开发Pandas，并于2009年将其开源。

---

Pandas的成功远远超出了它本身。从技术史角度看，它配合NumPy、SciPy等库，推动了Python在数据科学领域的地位，甚至在某种程度上改变了Python作为一种“胶水语言”的早期定位，使其超越R和Matlab，成为数据分析和科学计算的主流语言之一。

<!--
## 核心数据结构
### DataFrame
### Series
### Index

## DataFrame的增删改查操作

### 增加
### 删除
### 修改
### 查询
#### 像数组一样查询
#### at/loc
#### fancy indexing
#### 像SQL一样查询

## I/O


https://github.com/ZaxR/pandas_multiindex_tutorial/blob/master/Pandas%20MultiIndex%20Tutorial.ipynb
-->

pandas 的核心数据结构是 Series（类似于一维数组）和 DataFrame（矩形的数据表）数据结构。

前面已经介绍过DataFrame，这里简单回顾一下。DataFrame 含有一组有序且有命名的列，每一列可以是不同的数据类型（数值、字符串、布尔值等）。DataFrame 既有行索引也有列索引，可以看作由共用同一个索引的Series组成的字典。虽然DataFrame是二维的，但利用层次化索引，仍然可以用其表示更高维度的表格型数据。如果你使用的是Jupyter notebook，pandas的DataFrame 对象将会展示为对浏览器更为友好的HTML表格。

Series 由一组数据以及一组与之相关的数据标签（即索引）组成。仅由一个数组即可创建最简单的Series。Series以交互式的方法呈现，索引位于左边，值位于右边（一般会自动创建一个从 0 到 N-1 的索引，这里的 N 为数据长度）。与Numpy数组相比，我们可以通过索引的标签选取Series中的单个或一组值。还可以将其看作长度固定的有序字典，在可能使用字典的场景中，也可以使用 Series。对于许多应用而言，Series 最实用的一个功能是它在算术运算中能自动对齐索引标签。


在使用 Numpy 和 Pandas 之前，我们要先安装和导入 Numpy 库和Pandas库：

```bash
# 安装 Numpy 和 Pandas
!pip install numpy
!pip install pandas
```

一般地，我们通过别名`np`来导入和使用numpy，通过别名`pd`来导入和使用pandas：

---

```python
import numpy as np
import pandas as pd
```

为了在 Notebook 中运行这些示例时，能更加醒目地显示结果，我们首先定义一个 `cprint` 函数，它将原样输出提示信息，但对变量使用红色字体来输出，以示区别：

```python
from termcolor import colored


def cprint(formatter: str, *args):
    colorful = [colored(f"{item}", "red") for item in args]
    print(formatter.format(*colorful))


# 测试一下 CPRINT
cprint("这是提示信息，后接红色字体输出的变量值：{}", "hello!")
```


![50%](https://images.jieyu.ai/images/2025/03/002.png)

接下来，我们将介绍 Series 数据结构。



## 2. Series
### 2.1. 创建 Series
因为Series和DataFrame用的次数非常多，所以将其导入到本地命名空间中会更加方便：

```python
from pandas import Series, DataFrame
```

---

#### 2.1.1. 由数组简单创建(默认索引)
```python
obj = Series([1, 3, 5, 7]) 
obj
```

![50%](https://images.jieyu.ai/images/2025/03/003.png)

通过 `pd.Series()` 直接转换 Python 列表，默认生成从 0 开始的整数索引。

#### 2.1.2. 由字典创建(自定义索引)
字典的键自动转为索引，值转为数据：

```python
obj = Series({"a": 4, "b": 3, "c": 2, "d": 1})
obj
```

![50%](https://images.jieyu.ai/images/2025/03/004.png)

---

通过`to_dict`的方法，Series也能转换回字典：

```python
cprint("转换回字典：{}",obj.to_dict())
```

#### 2.1.3. 自定义索引
通过 index 参数指定任意不可变对象作为索引：
```python
obj = Series([90, 85, 92], index=["数学", "英语", "物理"], dtype="float64")
obj
```

![50%](https://images.jieyu.ai/images/2025/03/005.png)

#### 2.1.4 创建带时间戳索引的Series
生成时间序列数据：
```python
dates = pd.date_range("20230308", periods=4)
s = Series([100, 200, 300, 400], index=dates)
s
```

---

![50%](https://images.jieyu.ai/images/2025/03/006.png)

### 2.2. 查询数组值和索引对象
可以通过Series的array和index属性获取其数组值和索引对象：
```python
obj = Series([1, 3, 5, 7], index=["a","b","c","d"]) 
print("数组值：{}", obj.array)
print("索引对象：{}", obj.index)
```


![50%](https://images.jieyu.ai/images/2025/03/007.png)

与Numpy数组相比，可以通过索引的标签选取Series中的单个或一组值：
```python
print(obj["a"])

obj["d"] = 6
print(obj[["a","c","d"]])

print(obj[obj>5])

print(obj * 2)

print(np.exp(obj))
```

---

![50%](https://images.jieyu.ai/images/2025/03/008.png)

构建Series和Pandas时，所用到的任何数组或其他标签序列都会转换为索引对象：
```python
obj = Series(np.arange(3), index=["a","b","c"])
index = obj.index
print("index:",index)
print("index[1:]",index[1:])

# 注意Index对象是不可变的，因此用户不能对其修改
index[1]="d" # TypeError
```

---

由于Index对象的不可变性，可以使索引对象在多个数据结构之前安全共享：
```python
labels = pd.Index(np.arange(3))
print(labels)

obj = Series([1.5,-2.5,0],index=labels)
print(obj)
```

下面总结一下常用的索引的方法和属性：

| **方法/属性**          | ​**描述**                                                                 | ​**示例**                                                                 |
|------------------------|-------------------------------------------------------------------------|-------------------------------------------------------------------------|
| **`append`**           | 连接额外的索引对象，生成一个新的索引。                                      | `new_index = index1.append(index2)`                                     |
| **`diff`**             | 计算索引的差集。                                                         | `diff_index = index1.diff(index2)`                                      |
| **`intersection`**     | 计算索引的交集。                                                         | `common_index = index1.intersection(index2)`                            |
| **`union`**            | 计算索引的并集。                                                         | `union_index = index1.union(index2)`                                    |
| **`isin`**             | 返回一个布尔数组，表示每个值是否包含在传递的集合中。                        | `bool_array = index.isin(['a', 'b'])`                                   |
| **`delete`**           | 删除指定位置的元素，返回新的索引。                                         | `new_index = index.delete(0)`                                           |
| **`drop`**             | 删除传递的值，返回新的索引。                                               | `new_index = index.drop('a')`                                           |
| **`insert`**           | 在指定位置插入元素，返回新的索引。                                         | `new_index = index.insert(1, 'new_value')`                               |
| **`is_monotonic`**     | 返回 `True`，如果索引是单调递增或递减的。                                   | `is_monotonic = index.is_monotonic`                                     |
| **`is_unique`**        | 返回 `True`，如果索引没有重复的值。                                         | `is_unique = index.is_unique`                                           |
| **`unique`**           | 返回索引的唯一值数组。                                                     | `unique_values = index.unique()`                                        |
| **`reindex`**          | 根据新索引重新排列数据，缺失值用 `NaN` 填充。                                | `new_series = series.reindex(new_index)`                                |
| **`reset_index`**      | 重置索引为默认整数索引，原索引变为列。                                       | `df_reset = df.reset_index()`                                           |
| **`set_index`**        | 将某一列设置为索引。                                                      | `df.set_index('column_name', inplace=True)`                              |
| **`sort_values`**      | 对索引进行排序。                                                         | `sorted_index = index.sort_values()`                                    |
| **`to_series`**        | 将索引转换为 `Series`。                                                   | `index_series = index.to_series()`                                      |

---

| **方法/属性**          | ​**描述**                                                                 | ​**示例**                                                                 |
|------------------------|-------------------------------------------------------------------------|-------------------------------------------------------------------------|
| **`values`**           | 返回索引的 NumPy 数组。                                                   | `index_values = index.values`                                           |
| **`name`**             | 获取或设置索引的名称。                                                     | `index_name = index.name`                                               |
| **`shape`**            | 返回索引的形状（长度）。                                                   | `index_shape = index.shape`                                             |
| **`size`**             | 返回索引的长度。                                                         | `index_size = index.size`                                               |

### 2.3. 基本功能
本节，我们将介绍Series的一些数据的基本操作方法。后续将会深入地挖掘pandas在数据分析和处理方面的功能。

#### 2.3.1. 重建索引
重建索引是通过 `reindex()` 方法实现的，它允许用户根据新的索引标签对 Series 进行重排或填充。如果新索引标签在原 Series 中不存在，默认会用 `NaN` 填充。

| **参数**         | **描述**                                                                 | **默认值**       |
|------------------|-------------------------------------------------------------------------|------------------|
| **`index`**      | 新的索引标签列表，可以是 `Index` 实例或其他序列型数据结构。               | `None`           |
| **`method`**     | 填充缺失值的方法，可选值包括：`'backfill'`/`'bfill'`（后向填充）、`'pad'`/`'ffill'`（前向填充）、`'nearest'`（最近填充）。 | `None`           |
| **`fill_value`** | 用于填充缺失值的默认值。                                                 | `NaN`            |
| **`limit`**      | 使用填充方法时的最大填充距离。                                           | `None`           |
| **`tolerance`**  | 最大容差，超出此范围则不填充。                                           | `None`           |
| **`level`**      | 如果索引是 `MultiIndex`，则指定使用哪一级别进行重新索引。                 | `None`           |
| **`copy`**       | 如果为 `True`，即使新旧索引相同也会返回一个新的副本。                     | `True`           |

---

示例 1：基本重建索引
```python
s = Series([1, 2, 3], index=['a', 'b', 'c'])

# 新的索引
new_index = ['a', 'b', 'c', 'd']

# 重建索引
s_reindexed = s.reindex(new_index, fill_value=0)
print(s_reindexed)
```

![50%](https://images.jieyu.ai/images/2025/03/009.png)

示例 2：使用填充方法
对于时间序列这样的有序数据，重建索引时可能需要做一些插值或填值处理。method选项可以达到此目的，例如使用ffill可以实现前向填充。
```python
# 使用前向填充
s_reindexed = s.reindex(new_index, method='ffill')
print(s_reindexed)
```

---

![50%](https://images.jieyu.ai/images/2025/03/010.png)

示例 3：指定填充值
```python
# 指定填充值为 -1
s_reindexed = s.reindex(new_index, fill_value=-1)
print(s_reindexed)
```

![50%](https://images.jieyu.ai/images/2025/03/011.png)

---

#### 2.3.2. 删除指定轴上的项
在 Pandas 中，Series 删除指定轴上的项可以通过 `drop()` 方法实现。Series 是一维数据结构，因此删除操作通常是针对索引（行）进行的。

`drop()` 方法用于删除指定的索引标签，并返回一个新的 Series，不会修改原对象。其语法如下：

```python
Series.drop(labels, axis=0, inplace=False, errors='raise')
```

- **labels**: 要删除的索引标签，可以是单个标签或标签列表。
- **axis**: 指定操作的轴，对于 Series 只能是 0（默认值），表示删除行。
- **inplace**: 如果为 True，则直接在原对象上修改，不返回新对象。
- **errors**: 如果指定标签不存在，`raise` 会抛出错误，`ignore` 会忽略错误。

```python
obj = Series(np.arange(5.),index=["a","b","c","d","e"])
print(obj)

new_obj = obj.drop("c")
print(new_obj)

print(obj.drop(["d","c"]))
```

<!--![50%](https://images.jieyu.ai/images/2025/03/012.png)-->

#### 2.3.3. 索引、选取和过滤
[索引选取]

Series索引的工作方式类似于Numpy数组的索引，只不过Series的索引值可以不仅仅是整数：
```python
s = Series([10, 20, 30, 40], index=['a', 'b', 'c', 'd'])
print(s['b'])
print(s[['a', 'c']])  # 输出：a 10, c 30
```

---

Series 的选取可以通过以下方式实现：

- 基本选取：使用 [] 运算符。
- 属性选取：使用 . 运算符（仅适用于标签为合法变量名的情况）。
- **iloc 和 loc**：分别用于位置索引和标签索引。

```python
# iloc 选取
print(s.iloc[1])  # 输出：20

# loc 选取
print(s.loc['b'])  # 输出：20
```

[索引过滤]
Series 的过滤可以通过以下方式实现：

- 布尔索引：使用布尔条件筛选数据。
- 条件表达式：结合条件表达式进行过滤。
- **isin() 方法**：筛选值是否在指定列表中。
- **where() 和 mask() 方法**：根据条件替换或保留数据。

```python
# 布尔索引
print(s[s > 20])  # 输出：c 30, d 40

# 条件表达式
print(s[s % 20 == 0])  # 输出：b 20, d 40

# isin() 方法
print(s[s.isin([10, 30])])  # 输出：a 10, c 30

# where() 方法
print(s.where(s > 20, -1))  # 输出：a -1, b -1, c 30, d 40

# mask() 方法
print(s.mask(s > 20, -1))  # 输出：a 10, b 20, c -1, d -1
```

---

#### 2.3.4. 算数运算和数据对齐
```python
# 创建两个具有不同索引的 Series
s1 = Series([1, 2, 3], index=['a', 'b', 'c'])
s2 = Series([4, 5, 6], index=['b', 'c', 'd'])

# 自动对齐索引并相加
result = s1 + s2
print(result)
```

![50%](https://images.jieyu.ai/images/2025/03/013.png)

如果你使用过数据库，可以认为这类似于join操作。

如果不想得到 NaN，可以使用 `fill_value` 参数指定一个默认值来填充缺失的索引：

```python
result = s1.add(s2, fill_value=0)
print(result)
```

!!! 
    pandas 的`isnull`和`notnull`函数可以用于检测缺失数据，不妨来试一试！

---

#### 2.3.5. 排序和排名

Series 的排序可以通过以下两种方式实现：(1) 按索引排序：使用 sort_index() 方法。(2) 按值排序：使用 sort_values() 方法。

[按索引排序]

`sort_index()` 方法用于对 Series 的索引进行排序。默认情况下，索引按升序排列。


```python
s = Series([4, 1, 2, 3], index=['d', 'a', 'c', 'b'])

# 按索引升序排序
print(s.sort_index())  # 输出：a 1, b 3, c 2, d 4

# 按索引降序排序
print(s.sort_index(ascending=False))  # 输出：d 4, c 2, b 3, a 1
```

**参数**：
- ascending：是否升序排序，默认为 True。
- inplace：是否在原对象上修改，默认为 False。

[按值排序]

`sort_values()` 方法用于对 Series 的值进行排序。默认情况下，值按升序排列。
```python
# 按值升序排序
print(s.sort_values())  # 输出：a 1, c 2, b 3, d 4

# 按值降序排序
print(s.sort_values(ascending=False))  # 输出：d 4, b 3, c 2, a 1
```

---

**参数**:
- ascending：是否升序排序，默认为 True。
- inplace：是否在原对象上修改，默认为 False。
- na_position：缺失值的位置，默认为 last（排在最后）。

[排名]

Series 的排名通过 `rank()` 方法实现，它为每个值分配一个排名，支持多种排名方式。


```python
s = Series([7, -5, 7, 4, 2, 0, 4])

# 默认排名（平均排名）
print(s.rank())  # 输出：0 6.5, 1 1.0, 2 6.5, 3 4.5, 4 3.0, 5 2.0, 6 4.5

# 最小排名
print(s.rank(method='min'))  # 输出：0 6.0, 1 1.0, 2 6.0, 3 4.0, 4 3.0, 5 2.0, 6 4.0

# 最大排名
print(s.rank(method='max'))  # 输出：0 7.0, 1 1.0, 2 7.0, 3 5.0, 4 3.0, 5 2.0, 6 5.0

# 按出现顺序排名
print(s.rank(method='first'))  # 输出：0 6.0, 1 1.0, 2 7.0, 3 4.0, 4 3.0, 5 2.0, 6 5.0
```



**参数**：
- method：排名方法，可选值包括：
- 'average'（默认）：相同值分配平均排名。
- 'min'：相同值分配最小排名。
- 'max'：相同值分配最大排名。
- 'first'：相同值按出现顺序分配排名。
- 'dense'：相同值分配相同排名，且排名不跳跃。
- ascending：是否升序排名，默认为 True。
- na_option：缺失值的处理方式，可选 'keep'（保留）、'top'（排在最前）、'bottom'（排在最后）。


---


#### 2.3.6. 带有重复标签的轴索引
直到目前为止，几乎所有示例的轴标签（索引值）都是唯一的。虽然许多pandas函数（如reindex）都要求标签唯一，但这并不是强制性的。观察下面这个带有重复索引值的Series：
```python
obj = Series(np.arange(5),index=["a","a","b","b","c"])
obj
```

![50%](https://images.jieyu.ai/images/2025/03/014.png)

索引的is_unique属性可以告诉我们索引值是否唯一：
```python
obj.index.is_unique  # False
```

对于带有重复值的索引，数据选取操作将会有些不同。如果某个标签对应多个项，则返回Series；如果对应于单个项，则返回标量值：

---

```python
print(obj["a"])
print(obj["c"])
```

![50%](https://images.jieyu.ai/images/2025/03/015.png)


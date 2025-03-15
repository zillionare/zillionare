---
title: 量化人怎么用Pandas——核心语法[2]
slug: numpy-pandas-for-quant-trader-09
date: 2025-03-15
category: tools
motto: The future belongs to those who believe in the beauty of their dreams.
img: https://images.jieyu.ai/images/2024/12/book-of-sun-le.jpg
stamp_width: 60%
stamp_height: 60%
tags: 
    - tools
    - programming
    - Numpy
    - Pandas
---

层次化索引是pandas的一项重要功能，它能使你能在一个轴上拥有多个（两个以上）索引层级。用另一种说法，它能以低纬度形式处理高维度数据。先通过Series看一个例子：


```python
import numpy as np
import pandas as pd
data = pd.Series(np.random.uniform(size=9),index=[["a","a","a","b","b","c","c","d","d"],[1,2,3,1,3,1,2,2,3]])
print(data)
print(data.index)
```

![50%](https://images.jieyu.ai/images/2025/03/037.png)

---

看到的结果是MultiIndex作为索引的经过美化的Series视图。索引之间的“间隔”表示“直接使用上面的标签”。

对于层次化索引对象，可以使用部分索引，使用它选取数据子集更为简单：


```python
print(data["b"])
print(data["b":"c"])
print(data.loc[["b","d"]])

# 在“内部”层级中选取数据也是可行的
print(data.loc[:,2])
```

![50%](https://images.jieyu.ai/images/2025/03/038.png)


层次化索引在数据重塑和基于分组的操作下（如生成透视表）中发挥着重要作用。例如：可以通过unstack方法将下面的数据重排到DataFrame中：


```python
data.unstack()
```

![50%](https://images.jieyu.ai/images/2025/03/039.png)

`unstack()` 的逆运算是 `stack()`：


```python
data.unstack().stack()
```

![50%](https://images.jieyu.ai/images/2025/03/040.png)


对于DataFrame，每个轴都可以有分层索引。通过`nlevels`可以知道索引有多少层：


```python
frame = pd.DataFrame(np.arange(12).reshape((4,3)),index=[["a","a","b","b"],[1,2,1,2]],columns=[["Ohio","Ohio","Colorado"],["Green","Red","Blue"]])
frame.index.names = ["key1","key2"]
frame.columns.names = ["state","color"]
frame
frame.index.nlevels  # 2
```

---

可以单独创建MultiIndex，然后复用。前面DataFrame中的列带有层级名称，还可以如下创建：


```python
pd.MultiIndex.from_arrays([["Ohio","Ohio","Colorado"],["Green","Red","Blue"]],names=["state","color"])
```
![50%](https://images.jieyu.ai/images/2025/03/041.png)


## 1. 重排序和层级排序

有时，我们需要重新调整某条轴上各个层级的顺序，或者指定层级上的值对数据进行排序。Swaplevel方法接收两个层级编号或名称，并返回一个层级互换的新对象（但数据不会发生变化）：


```python
frame.swaplevel("key1","key2")
```

![50%](https://images.jieyu.ai/images/2025/03/042.png)


而`sort_index`默认根据所有索引层级中的字母顺序对数据进行排序，但你也可以通过传入level参数只选取单层级或层级的子集。

---

```python
frame.sort_index(level=1)
```

![50%](https://images.jieyu.ai/images/2025/03/043.png)

```python
frame.swaplevel(0,1).sort_index(level=0)
```

![50%](https://images.jieyu.ai/images/2025/03/044.png)

---

## 2. 按照层级进行汇总统计
许多对DataFrame和Series对描述性和汇总性统计都有一个Level选项，用于指定在某条轴的特点层级进行聚合。再以之前的DataFrame为例，我们可以按照行和列上的层级来进行聚合：


```python
frame.groupby(level="key2").sum()
```

![50%](https://images.jieyu.ai/images/2025/03/045.png)

```python
frame.groupby(level="color",axis="columns").sum()
```

![50%](https://images.jieyu.ai/images/2025/03/046.png)


---

这里使用了pandas的groupby功能。



## 3. 使用DataFrame的列进行索引
我们通常不会将DataFrame的单列或多列用作行索引，但是可能将行索引用作DataFrame的列。以下面这个DataFrame为例：


```python
frame = pd.DataFrame({"a":range(7),
                      "b":range(7,0,-1),
                      "c":["one","one","one","two","two","two","two"],
                      "d":[0,1,2,0,1,2,3]})
frame
```

![50%](https://images.jieyu.ai/images/2025/03/047.png)

DataFrame的set_index函数会将单列或多列转换为行索引，并创建一个新的DataFrame：


```python
frame2 = frame.set_index(["c","d"])
frame2
```

![50%](https://images.jieyu.ai/images/2025/03/048.png)

默认情况下，这些列会从DataFrame中移除，但也可以通过传入`drop=False`将其保留下来：


```python
frame.set_index(["c","d"],drop=False)
```

![50%](https://images.jieyu.ai/images/2025/03/049.png)

---


reset_index的功能与set_index相反，它将层次化索引的层级转移到列：


```python
frame2.reset_index()
```

![50%](https://images.jieyu.ai/images/2025/03/050.png)

## 4. 使用query进行数据查询

query 是 pandas 库中的一个函数，它提供了一种简洁、直观的方法来查询 DataFrame 中的数据。使用 query 函数，你可以使用字符串形式的表达式来指定你想要筛选的数据，这类似于在 SQL 数据库中执行 SELECT 查询。

---

```python
data = {
    'A': [1, 2, 3, 4, 5],
    'B': [10, 20, 30, 40, 50],
    'C': ['a', 'b', 'c', 'd', 'e']
}
df = pd.DataFrame(data)

# 使用 query 函数筛选数据
result = df.query('A > 2 and B < 40')
print(result)
```

![50%](https://images.jieyu.ai/images/2025/03/051.png)

注意，在 query 函数的表达式中，你可以使用变量（需要先使用 @ 符号声明）和比较运算符（如 >, <, ==, != 等）。


```python
threshold = 3
result = df.query('@threshold < A < 5')
print(result)
```

![50%](https://images.jieyu.ai/images/2025/03/052.png)

---

!!! 注意事项
    - query 函数在处理大型数据集时可能比直接使用布尔索引慢。
    - 在 query 表达式中，列名应与 DataFrame 中的列名完全匹配，包括大小写。
    - 如果列名包含空格或特殊字符，可以使用反引号 ` 将其括起来。
    - 总之，query 函数提供了一种简洁、直观的方法来查询 pandas DataFrame 中的数据，特别适用于需要编写复杂筛选条件的情况。

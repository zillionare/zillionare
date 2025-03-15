---
title: 量化人怎么用Pandas——核心语法[1]
slug: numpy-pandas-for-quant-trader-08
date: 2025-03-15
category: tools
motto: If you want to fly, give up everything that weighs you down.
img: https://images.jieyu.ai/images/2024/12/book-of-sun-le.jpg
stamp_width: 60%
stamp_height: 60%
tags: 
    - tools
    - programming
    - Numpy
    - Pandas

---

DataFrame是矩形的数据表，它含有一组有序且有命名的列，每一列可以是不同的数据类型（数值、字符串、布尔值等）。DataFrame既有行索引也有列索引，可以看作由共同作用同一个索引的Series组成的字典。

!!! notes
    虽然DataFrame是二维的，但利用层次化索引，仍然可以用其表示为更高维度的表格型数据。层次化索引是高级数据处理特性，我们会在下一章进行讨论。

---

## 1. 创建DataFrame

### 1.1. 传入一个由等长列表或Numpy数组构成的字典


```python
import pandas as pd
data = {"state":["Ohio","Ohio","Ohio","Nevada","Nevada","Nevada"],
       "year":[2000,2001,2002,2003,2004,2005],
       "pop":[1.5,1.7,3.6,2.4,2.9,3.2]}
frame = pd.DataFrame(data)
frame
```

![50%](https://images.jieyu.ai/images/2025/03/016.png)


生成的DataFrame会自动加上索引（和Series一样），且全部列会按照data键（键的顺序取决于在字典中插入的顺序）的顺序有序排列。
（如果你使用的是Jupyter notebook，pandas的DataFrame对象会展示为对浏览器更为友好的HTML表格）

对于特别大的DataFrame，可以使用`head`方法，只展示前5行。相似地，`tail`方法会返回最后5行。

---

```python
print(frame.head())
print(frame.tail())
```

![50%](https://images.jieyu.ai/images/2025/03/017.png)

下面还有几种创建DataFrame的情况：


```python
# 如果指定了列的顺序，则DataFrame的列就会按照指定顺序进行排列
frame1 = pd.DataFrame(data=data,columns=["year","state","pop"])

# 如果字典中不包括传入的列，就会在结果中产生缺失值
frame2 = pd.DataFrame(data=data,columns=["year","state","pop","debt"])
```

### 1.2. 传入嵌套字典
如果将嵌套字典传给DataFrame，pandas就会将外层字典的键解释为列，将内层字典的键解释为行索引。

---


```python
populations = {"Ohio":{2000:1.5,2001:1.7,2002:3.6},"Nevada":{2001:2.4,2002:2.9}}
frame3 = pd.DataFrame(populations)
frame3
```

![50%](https://images.jieyu.ai/images/2025/03/018.png)


使用类似于Numpy数组的方法，可以对 DataFrame 进行转置（交换行和列）：


```python
frame3.T
```

![50%](https://images.jieyu.ai/images/2025/03/019.png)




内层字典的键被合并后形成了结果的索引。如果明确指定了索引，则不会这样：


```python
pd.DataFrame(populations,index=["2001","2002","2003"])
```

---


![50%](https://images.jieyu.ai/images/2025/03/020.png)


由Series组成的字典差不多也是一样的用法：


```python
pdata = {"Ohio":frame3["Ohio"][:-1],"Nevada":frame3["Nevada"][:2]}
pd.DataFrame(pdata)
```

![50%](https://images.jieyu.ai/images/2025/03/021.png)


可以向DataFrame构造器输入的数据：

| 类型                  | 说明                                                                 |
|-----------------------|----------------------------------------------------------------------|
| ​**字典 (Dict)**       | 键为列名，值为列表、NumPy 数组或 Series。每列的长度必须一致。         |
| ​**列表 (List)**       | 列表中的每个元素是一个字典，字典的键为列名，值为对应列的数据。         |
| ​**NumPy 数组**        | 二维数组，每行对应 DataFrame 的一行，每列对应 DataFrame 的一列。      |

---

| 类型                  | 说明                                                                 |
|-----------------------|----------------------------------------------------------------------|
| ​**Series**            | 单个 Series 可以构造单列的 DataFrame，多个 Series 可以构造多列。      |
| ​**结构化数组**        | NumPy 的结构化数组，字段名对应 DataFrame 的列名。                     |
| ​**其他 DataFrame**    | 可以通过复制另一个 DataFrame 来创建新的 DataFrame。                   |
| ​**CSV 文件**          | 通过 `pd.read_csv()` 读取 CSV 文件并转换为 DataFrame。                |
| ​**Excel 文件**        | 通过 `pd.read_excel()` 读取 Excel 文件并转换为 DataFrame。             |
| ​**JSON 数据**         | 通过 `pd.read_json()` 读取 JSON 数据并转换为 DataFrame。               |
| ​**SQL 查询结果**      | 通过 `pd.read_sql()` 读取 SQL 查询结果并转换为 DataFrame。             |
| ​**HTML 表格**         | 通过 `pd.read_html()` 从 HTML 页面中提取表格并转换为 DataFrame。       |
| ​**剪贴板数据**        | 通过 `pd.read_clipboard()` 从剪贴板中读取数据并转换为 DataFrame。     |


如果设置了DataFrame的index和columns的name属性，则这些信息也会显示出来：



```python
frame3.index.name = "year"
frame3.columns.name = "state"
frame3
```


![50%](https://images.jieyu.ai/images/2025/03/022.png)


---

```python
# 二维的ndarray的DataFrame形式返回
frame3.to_numpy()

# 如果DataFrame各列的数据类型不同，则返回数组会选用能兼容所有列的数据类型：
frame2.to_numpy()
```

![50%](https://images.jieyu.ai/images/2025/03/023.png)



## 2. 获取、修改、删除列和行
### 2.1. 获取列
通过类似于字典标记或点属性的方式，可以将DataFrame的列获取为一个Series。

!!! Notes
    有关Series的具体用法，我们会在后面进行讲解。


```python
print(frame2["state"])
print(frame2.year)
```

---

![50%](https://images.jieyu.ai/images/2025/03/024.png)


如果列名包含空格或下划线以外的符号，是不能用点属性的方式访问的。

---

### 2.2. 修改列

```python
import numpy as np
# 通过赋值的方法修改列
frame2["debt"] = 16.5
print(frame2)
frame2["debt"] = np.arange(6.)
print(frame2)

# 将列表和数组赋值给某个列
val = pd.Series([1.2,-1.5,-1.7],index=["two","four","five"])  # 长度必须与DataFrame保持一致
frame2["debt"] = val
print(frame2)
```

![50%](https://images.jieyu.ai/images/2025/03/025.png)

---

### 2.3. 删除列
关键字`del`可以像在字典中那样删除列。


```python
frame2["eastern"] = frame2["state"] = "ohio"
print(frame2)

del frame2["eastern"]
print(frame2.columns)
```

![50%](https://images.jieyu.ai/images/2025/03/026.png)



### 2.4. 获取行（iloc和loc）
通过`iloc`和`loc`属性，也可以通过位置或名称的方式进行获取行。


```python
print(frame2.loc[1])
print(frame2.iloc[2])
```

---

![50%](https://images.jieyu.ai/images/2025/03/027.png)


## 3. 索引对象
pandas的索引对象负责存储轴标签（包括DataFrame的列名）和其他元数据（比如轴名称或标签）。构建Series或DataFrame时，所用到的任何数组或其他标签序列都会转换成索引对象。

```python
import pandas as pd
obj = pd.Series(np.arange(3),index=["a","b","c"])
index = obj.index
index  # Index(['a', 'b', 'c'], dtype='object')
```

Index 对象是不可变的，因此用户不能对其进行修改。

```python
index[1] = "d"  #TypeError
```

不可变性可以使索引对象在多个数据结构之间安全共享：

---

```python
labels = pd.Index(np.arange(3))
labels  # Int64Index([0, 1, 2], dtype='int64')

obj2 = pd.Series([1.5,-2.5,0],index=labels)
obj2
# 0    1.5
# 1   -2.5
# 2    0.0
# dtype: float64
```

虽然用户不需要经常使用索引的功能，但是因为一些操作生成的结果会包含索引化的数据，所以理解它们的工作原理也很重要。

除了类似于数组，索引也类似于一个大小固定的集合，接下来，以`frame3`为例。

![50%](https://images.jieyu.ai/images/2025/03/028.png)


```python
print(frame3.columns)
# Index(['Ohio', 'Nevada'], dtype='object', name='state')

print("Ohio" in frame3.columns)  # True

print(2003 in frame3.index)  # False
```

---

与Python集合不同，pandas的索引可以包含重复的标签：


```python
pd.Index(["foo","foo","bar","bar"])
# Index(['foo', 'foo', 'bar', 'bar'], dtype='object')
```

选择重复的标签，会选取所有对应的结果。

下面总结了索引的方法和属性：


| 方法/属性                  | 说明                                                                 |
|----------------------------|----------------------------------------------------------------------|
| ​`append()`             | 将另一个索引附加到当前索引后，返回新索引。                           |
| ​`difference()`         | 返回当前索引与另一个索引的差集（在当前索引中但不在另一个索引中）。   |
| ​`intersection()`       | 返回当前索引与另一个索引的交集（两个索引共有的部分）。               |
| ​`union()`              | 返回当前索引与另一个索引的并集（两个索引的所有唯一值）。             |
| ​`isin()`               | 检查索引中的值是否在给定的集合中，返回布尔数组。                     |
| ​`delete()`             | 删除指定位置的索引值，返回新索引。                                   |
| ​`drop()`               | 删除指定的索引值，返回新索引。                                       |
| ​`insert()`             | 在指定位置插入一个索引值，返回新索引。                               |
| `is_monotonic()`       | 检查索引是否单调递增或递减，返回布尔值。                             |
| `is_unique()`           | 检查索引中的所有值是否唯一，返回布尔值。                             |
| `unique()`             | 返回索引中的唯一值，结果为一个数组。                                 |


## 4. 基本功能
### 4.1. 重建索引 reindex
借助DataFrame，reindex可以修改（行）索引、列，也可以修改同时修改。

---


```python
# 只传入一个序列时，会重建索引结果中的行
frame = pd.DataFrame(np.arange(9).reshape((3,3)),index=["a","b","c"],columns=["Ohio","Texas","California"])
print(frame)

frame2 = frame.reindex(index=["a","b","c","d"])
frame2
```

![50%](https://images.jieyu.ai/images/2025/03/029.png)


```python
# 列可以通过columns关键字重建索引
states = ["Texas","Utah","California"]
frame.reindex(columns=states)
print(frame)

# 另一种重建索引的方式生活传入新的轴标签作为位置参数，然后用axis关键字对指定轴进行重建索引
frame.reindex(states, axis="columns")
print(frame)
```

---

![50%](https://images.jieyu.ai/images/2025/03/030.png)


下面总结了 `reindex` 函数的参数及说明：

| 参数          | 说明                                                                 |
|---------------|----------------------------------------------------------------------|
| ​`labels`  | 指定新的索引或列标签。可以是一个列表、数组或 Index 对象。           |
| ​`index`   | 指定新的行索引。与 `labels` 类似，但仅用于行索引。                  |
| ​`columns` | 指定新的列索引。与 `labels` 类似，但仅用于列索引。                  |
| ​`axis`    | 指定操作的轴。`0` 或 `'index'` 表示行，`1` 或 `'columns'` 表示列。   |
| ​`method`  | 指定填充缺失值的方法。可选值：`None`、`'backfill'`/`'bfill'`、`'pad'`/`'ffill'`。 |
| ​`fill_value` | 指定用于填充缺失值的标量值。默认是 `NaN`。                       |
| ​`limit`   | 指定填充缺失值的最大连续填充次数。仅当 `method` 不为 `None` 时有效。 |
| ​`tolerance` | 指定填充缺失值的容差范围（与索引值的差值）。仅当 `method` 不为 `None` 时有效。 |
| ​`level`   | 指定在多级索引中操作的级别（索引层级）。                            |
| `copy`    | 是否返回新对象。如果为 `True`，则返回新对象；如果为 `False`，则可能修改原对象。默认是 `True`。 |

还可以用loc运算重建索引，这也是多数人更为常用的方式。只有当新索引的标签在DataFrame中已经存在时，才能这么做（否则，reindex将会给新标签插入缺失值）：


```python
frame.loc[["a","b","c"],["California","Texas"]]
```

---

<!--![50%](https://images.jieyu.ai/images/2025/03/031.png)-->


### 4.2. 删除指定轴上的项
可以使用`drop`删除任意轴上的索引值。为了演示，首先创建一个DataFrame实例：


```python
data = pd.DataFrame(np.arange(16).reshape((4,4)),
                    index=["Ohio","Colorado","Utah","New York"],
                    columns=["one","two","three","four"])
data
```
![50%](https://images.jieyu.ai/images/2025/03/032.png)


```python
# 用标签序列调用drop会从行标签（axis 0）删除值
frame1 = data.drop(index=["Colorado","Ohio"])
print(frame1)

# 通过传入axis=1（类似于Numpy）或axis=“columns”，从列删除值
frame2 = data.drop(["two","four"],axis = "columns")
print(frame2)
```



![50%](https://images.jieyu.ai/images/2025/03/033.png)

---

### 4.3. 索引、选取和过滤

#### 4.3.1. 索引
loc和iloc是新手常犯的错误，正确的方式是用方括号进行索引。方括号不仅用于切片索引，还用于对DataFrame对多个轴进行索引。

用单个值或序列对DataFrame进行索引，以获取单列或多列：

```python
data = pd.DataFrame(np.arange(16).reshape((4,4)),
                    index=["Ohio","Colorado","Utah","New York"],
                    columns=["one","two","three","four"])
data
data["two"]
data[["three","one"]]
```

<!--![50%](https://images.jieyu.ai/images/2025/03/034.png)-->

用切片或布尔数组对DataFrame进行索引：

```python
data[:2]
data[data["three"]>5]
```

![50%](https://images.jieyu.ai/images/2025/03/035.png)

---

用布尔型DataFrame进行索引，看下面的DataFrame，它的所有值都是与一个标量比较得出的布尔值：

```python
data<5
data[data<5] = 0  # 这个DataFrame将0赋值给等于True的位置
```

#### 4.3.2. 选取
- loc：标签索引
- iloc：整数索引

```python
 print(data)

# 通过标签选取一行
print(data.loc["Colorado"])

# 通过标签选取多行
print(data.loc[["Colorado","New York"]])

# 同时选取行和列
print(data.loc["Colorado",["two","three"]])
```

![50%](https://images.jieyu.ai/images/2025/03/036.png)
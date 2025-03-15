---
title: 量化人怎么用Numpy——核心语法[1]
<<<<<<< HEAD
slug: numpy-pandas-for-quant-trader-02
date: 2025-03-09
category: tools
motto: Every single day counts.
img: https://images.jieyu.ai/images/2024/12/book-of-sun-le.jpg
stamp_width: 60%
stamp_height: 60%
tags: 
    - tools
    - programming
    - Numpy
=======
slug: ta-lib-is-reloaded
date: 2025-03-09
category: arsenal
motto: You only live once, but if you do it right, once is enough
img: https://images.jieyu.ai/images/2024/12/book-of-sun-le.jpg
tags: 
    - tools
    - programming
>>>>>>> 420be9aeea2846f7b9efd59bbbefc070dcb01ab9
---

## 1. 基本数据结构

NumPy 的核心数据结构是 ndarray（即 n-dimensional array，多维数组）数据结构。这是一个表示多维度、同质并且大小固定的数组对象。

ndarray 只能存放同质的数组对象，这样使得它无法表达记录类型的数据。因此，numpy 又拓展出了名为 structured array 的数据结构。它用一个 void 类型的元组来表示一条记录，从而使得 numpy 也可以用来表达记录型的数据。因此，在 Numpy 中，实际上跟数组有关的数据类型主要是两种。

---

前一种数组格式广为人知，我们将以它为例介绍多数 Numpy 操作。而后一种数据格式，在量化中也常常用到，比如，通过聚宽[1]的jqdatasdk获得的行情数据，就允许返回这种数据类型，与 DataFrame 相比，在存取上有不少简便之处。我们将在后面专门用一个章节来介绍。

在使用 Numpy 之前，我们要先安装和导入 Numpy 库：
 
```bash
# 安装 NUMPY
pip install numpy
```

一般地，我们通过别名`np`来导入和使用 numpy：

```python
import numpy as np
```


为了在 Notebook 中运行这些示例时，能更加醒目地显示结果，我们首先定义一个 cprint 函数，它将原样输出提示信息，但对变量使用红色字体来输出，以示区别：

```python
from termcolor import colored

def cprint(formatter: str, *args):
    colorful = [colored(f"{item}", 'red') for item in args]
    print(formatter.format(*colorful))

# 测试一下 CPRINT
cprint("这是提示信息，后接红色字体输出的变量值：{}", "hello!")
```

接下来，我们将介绍基本的增删改查操作。

---

### 1.1. 创建数组

#### 1.1.1. 通过 Python List 创建
我们可以通过`np.array`的语法来创建一个简单的数组,在这个语法中，我们可以提供 Python 列表，或者任何具有 Iterable 接口的对象，比如元组。

```python
arr = np.array([1, 2, 3])
cprint("create a simple numpy array: {}", arr)
```

#### 1.1.2. 预置特殊数组
很多时候，我们希望 Numpy 为我们创建一些具有特殊值的数组。Numpy 也的确提供了这样的支持，比如：

| 函数                | 描述                                                                                                             |
| ------------------- | ---------------------------------------------------------------------------------------------------------------- |
| zeros<br>zeros_like | 创建全 0 的数。zeros_like 接受另一个数组，并生成相同形状和数据类型的 zeros 数组。常用于初始化。以下*_like 类推。 |
| ones<br>ones_like   | 创建全 1 的数组                                                                                                  |
| full<br>full_like   | 创建一个所有元素都填充为`n`的数组                                                                                |
| empty<br>empty_like | 创建一个空数组                                                                                                   |
| eye<br>identity     | 创建单位矩阵                                                                                                     |
| random.random       | 创建一个随机数组                                                                                                 |
| random.normal       | 创建一个符合正态分布的随机数组                                                                                   |
| random.dirichlet    | 创建一个符合狄利克雷分布的随机数组                                                                               |
| arange              | 创建一个递增数组                                                                                                 |
| linspace            | 创建一个线性增长数组。与 arange 的区别在于，此方法默认生成全闭区间数组。并且，它的元素之间的间隔可以为浮点数。   |

---

<!--还有一些比较小众的预置函数，比如 np.indices-->

```python
# 创建特殊类型的数组
cprint("全 0 数组：\n{}", np.zeros(3))
cprint("全 1 数组：\n{}", np.ones((2, 3)))
cprint("单位矩阵：\n{}", np.eye(3))
cprint("由数字 5 填充的矩阵：\n{}", np.full((3,2), 5))

cprint("空矩阵：\n{}", np.empty((2, 3)))
cprint("随机矩阵：\n{}",np.random.random(10))
cprint("正态分布的数组：\n{}",np.random.normal(10))
cprint("狄利克雷分布的数组：\n{}",np.random.dirichlet(np.ones(10)))
cprint("顺序增长的数组：\n{}", np.arange(10))
cprint("线性增长数组：\n{}", np.linspace(0, 2, 9))
```

!!! warning
    尽管 empty 函数的名字暗示它应该生成一个空数组，但实际上生成的数组，每个元素都是有值的，只不过这些值既不是 np.nan，也不是 None，而是随机值。我们在使用 empty 生成的数组之前，一定要对它进行初始化，处理掉这些随机值。
<!--
在这里，注意 empty 数组在打印时是有值的，这些值都是随机的。Numpy 提供 empty 函数主要是出于性能考虑。它使得我们可以快速构建一个数组，但可以在后面再来填充它的数值。但我们毕竟 empty 创建的数据存在随机值，所以，我们使用 empty 时一定要小心，很多情况下，我们会宁可使用 zeros，也不是 empty。
-->

生成正态分布数组很有用。我们在做一些研究时，常常需要生成满足某种条件的价格序列，再进一步研究和比较它的特性。

比如，如果我们想研究上升趋势和下降趋势下的某些指标，就需要有能力先构建出符合趋势的价格序列。下面的例子就演示了如何生成这样的序列，并且绘制图形：

```python
import numpy as np
import matplotlib.pyplot as plt

returns = np.random.normal(0, 0.02, size=100)

fig, axes = plt.subplots(1, 3, figsize=(12,4))
c0 = np.random.randint(5, 50)

for i, alpha in enumerate((-0.01, 0, 0.01)):
    r = returns + alpha
    close = np.cumprod(1 + r) * c0
    axes[i].plot(close)
```

---

绘制的图形如下：

![](https://images.jieyu.ai/images/2024/04/same-vol-different-trend.jpg)

<!--
很多情况下我们需要生成正态分布数组。比如，我们想研究股价涨跌幅与波动率之间的关系，比如，股价持续上涨与持续下跌，会有同样的波动率吗？此时，我们可以从下跌-0.1，到上涨 0.1，中间以 0.05 为一档，造出若干个回报序列，再来求它们的波动率。此时就可以用：

```python
import numpy as np
import matplotlib.pyplot as plt

returns = np.random.normal(0, 0.02, size=100)

fig, axes = plt.subplots(1, 3, figsize=(12,4))
c0 = np.random.randint(5, 50)

for i, alpha in enumerate((-0.01, 0, 0.01)):
    r = returns + alpha
    close = np.cumprod(1 + r) * c0
    vol = round(np.std(r), 3)
    axes[i].set_title(f"vol={vol}")
    axes[i].plot(close)
```

这个例子就演示了如何通过收益数组生成价格序列。

结论是，持续上涨、持续下跌和横盘整理的序列，可以有同样的波动率。它的意义是什么呢？我们知道，绩优股常常是低波动率的。这给了我们一个比较好的起点，再加上其它的指标，我们就可以筛选出绩优股出来。当然，知道了波动率与涨跌的关系之后，我们就知道，反过来，低波动率的，不一定是绩优股。
-->

示例中还提到了 Dirichlet（狄利克雷）分布数组。这个数组具有这样的特点，它的所有元素加起来会等于 1。比如，在现代投资组合理论中的有效前沿优化中，我们首先需要初始化各个资产的权重（随机值），并且满足资产权重之和等于 1 的约束（显然！），此时我们就可以使用 Dirichlet[2] 分布。


<!--狄利克雷，德国数学家。他对数论、傅里叶级数理论和其他数学分析学领域有杰出贡献，并被认为是最早给出现代函数定义的数学家之一和解析数论创始人之一。-->
<!--当然我们也可以使用高斯分布，再将其正则化。-->

<!--
arange 数组类似 range 语法，将生成一个整数数组，而 linspace 将生成步幅为浮点数的数组。此外，一个是左闭右开区间，一个是两端闭合区间。linspace 有什么用？

这里举一个例子，判断均线走势。假设均线数组为 ma, 共 10 个数据，则 linspace(ma[0], ma[-1], 10) 为连接两端的弦。用 ma 数组减去弦数组，如果值为正，则均线在向下拐头，否则，均线为凹曲线，是向上拐头，处在加速上涨中。
-->
#### 1.1.3. 通过已有数组转换

我们还可以从已有的数组中，通过复制、切片、重复等方法，创建新的数组：

```python
# 复制一个数组
cprint("通过 np.copy 创建：{}", np.copy(np.arange(5)))

# 复制数组的另一种方法
cprint("通过 arr.copy: {}", np.arange(5).copy())

# 使用切片，提取原数组的一部分
cprint("通过切片：{}", np.arange(5)[:2])

# 合并两个数组
arr = np.concatenate((np.arange(3), np.arange(2)))
cprint("通过 concatenate 合并：{}", arr)
```

---

```python
# 重复一个数组
arr = np.repeat(np.arange(3), 2)
cprint("通过 repeat 重复原数组：{}", arr)

# 重复一个数组，注意与 NP.REPEAT 的差异
# NP.TILE 的语义类似于 PYTHON 的 LIST 乘法
arr = np.tile(np.arange(3), 2)
cprint("通过 tile 重复原数组：{}", arr)
```

!!! question
    np.copy 与 arr.copy 有何不同？在 Numpy 中还有哪些类似函数对，有何规律？

<!--
我们在数组复制时，使用了两种方法。一种是 np.copy，另一种，则是数组对象自身的 copy。这两种方法有何不同？
-->


注意在 concatenate 函数中，axis 的作用：

```python
arr = np.arange(6).reshape((3,2))

# 在 ROW 方向上拼接，相当于增加行，默认行为
cprint("按 axis=0 拼接：\n{}", np.concatenate((arr, arr), axis=0))
# 在 COL 方向上拼接，相当于扩展列
cprint("按 axis=1 拼接：\n{}", np.concatenate((arr, arr), axis=1))
```

### 1.2. 增加/删除和修改元素
Numpy 数组是固定大小的，一般我们不推荐频繁地往数组中增加或者删除元素。但如果确实有这种需求，我们可以使用下面的方法来实现增加或者删除：
<!--
如果要频繁地执行增加和删除数组元素这种会改变数组大小的操作，一般我们会使用 Python 的 list 作为数据结构，而不是使用 numpy 的 array.
-->

| 函数   | 使用说明                                                                                |
| ------ | --------------------------------------------------------------------------------------- |
| append | 将`values`添加到`arr`的末尾。                                                           |
| insert | 向`obj`（可以是下标、slicing）指定的位置处，插入数值`value`（可以是标量，也可以是数组） |
| delete | 删除指定下标处的元素                                                                    |

---

示例如下：

```python
arr = np.arange(6).reshape((3,2))
np.append(arr, [[7,8]], axis=0)
cprint("指定在行的方向上操作、n{}", arr)

arr = np.arange(6).reshape((3,2))
arr = np.insert(arr.reshape((3,2)), 1, -10)
cprint("不指定 axis，数组被扁平化：\n{}", arr)

arr = np.arange(6).reshape((3,2))
arr = np.insert(arr, 1, (-10, -10), axis=0)
cprint("np.insert:\n{}", arr)

arr = np.delete(arr, [1], axis=1)
cprint("deleting col 1:\n{}", arr)
```

<!--
append 默认就是在行的方向上进行操作，这里的 axis=0 可以省略
-->

!!! tip
    请一定运行一下这里的代码，特别是关于 insert 的部分，了解所谓的扁平化是怎么回事。
<!--
第 5~11 行代码对比了 insert 在指定 axis 和不指定 axis 下的不同行为。特别要注意，如果不指定 axis，则执行此操作后，数组将会被扁平化为一维数组，无论之前数组的维度如何。
-->

<!--
第 13 行演示了如何删除一个数组元素。注意第二个参数是要被删除的元素的坐标，它可以是标量、也可以是一个坐标数组或者切片
-->

<!--
注意在 numpy 中，多数操作都不会直接修改原数组，而是返回一个新的数组
-->

有时候我们需要修改个别元素的值，应该这样操作：

```python
arr = np.arange(6).reshape(2,3)

arr[0,2] = 3
```

这里涉及到如何定位一个数组元素的问题，也正是我们下一节的内容。

<!--
!!! warning
    在 Numpy 中，多数操作并不会在原数组上执行，而是会拷贝并返回一个新的数组。下面的例子提醒我们注意由此可能产生的问题：

    ```python
    data = np.array([("aaron", "label")], 
                    dtype=[("name", "O"), ("label", "O")])
    filter = data["name"] == "aaron"

    # AFTER THIS: AARON -> 100
    data["label"][filter] = 100

    # THIS WON'T CHANGE
    data[filter]["label"] = "blogger"
    ```
-->
### 1.3. 定位、读取和搜索

#### 1.3.1. 索引和切片


Numpy 中索引和切片语法大致类似于 Python，主要区别在于对多维数组的支持：

---

```python
arr = np.arange(6).reshape((3,2))
cprint("原始数组：\n{}", arr)

# 切片语法
cprint("按行切片：{}", arr[1, :])
cprint("按列切片：{}", arr[:, -1])
cprint("逆排数组：\n {}", arr[: : -1])

# FANCY INDEXING
cprint("fancy index: 使用下标数组：\n {}", arr[[2, 1, 0]])

```

上述切片语法在 Python 中也存在，但只能支持到一维，因此，对下面的 Python 数组，类似操作会出错：

```python
arr = np.arange(6).reshape((3,2)).tolist()

arr[1, :]
```

提示 list indices must be integers or slices, not tuple。

<!--
在上面的代码中，我们还通过 tolist() 将 numpy 数组转换成为 Python list。在 Numpy 对象与 Python 对象之间的转换会经常发生，特别是时间对象之间的转换，需要熟练掌握。
-->

#### 1.3.2. 查找、筛选和替换

在上一节中，我们是通过索引来定位一个数组元素。但很多时候，我们得先通过条件运算把符合要求的索引找出来。这一节将介绍相关方法。

| 函数            | 使用说明                                                   |
| --------------- | ---------------------------------------------------------- |
| np.searchsorted | 在有序数组中搜索指定的数值，返回索引。                     |
| np.nonzero      | 返回非零元素的索引，用以查找数组中满足条件的元素。         |
| np.flatnonzero  | 同 nonzero，但返回输入数组的展平版本中非零的索引。         |
| np.argwere      | 返回满足条件的元素的索引，相当于 nonzero 的转置版本        |
| np.argmin       | 返回数组中最小元素的索引（注意不是返回满足条件的最小索引） |
| np.argmax       | 返回数组中最大元素的索引                                   |

---

```python
# 查找
arr = [0, 2, 2, 2, 3]
pos = np.searchsorted(arr, 2, 'right')
cprint("在数组 {} 中寻找等于 2 的位置，返回 {}, 数值是 {}", 
        arr, pos, arr[pos - 1])

arr = np.arange(6).reshape((2, 3))
cprint("arr[arr > 1]: {}", arr[arr > 1])

# NONZERO 的用法
mask = np.nonzero(arr > 1)
cprint("nonzero 返回结果是：{}", mask)
cprint("筛选后的数组是：{}", arr[mask])

# ARGWHERE 的用法
mask = np.argwhere(arr > 1)
cprint("argwere 返回的结果是：{}", mask)

# 多维数组不能直接使用 ARGWHERE 结果来筛选
# 下面的语句不能得到正确结果，一般会出现 INDEXERROR
arr[mask]

# 但对一维数组筛选我们可以用：
arr = np.arange(6)
mask = np.argwhere(arr > 1)
arr[mask.flatten()[0]]

# 寻找最大值的索引
arr = [1, 2, 2, 1, 0]
cprint("最大值索引是：{}", np.argmax(arr))
```

使用 searchsorted 要注意，数组本身一定是有序的，不然不会得出正确结果。
<!--
为什么我们要讲这个函数？在熟悉了 Numpy 之后，大家可能会想把所有的数据都使用 numpy 数组来表示。我们通过这个例子提醒大家，numpy 中的搜索，由于没有索引，实际上会比较慢。只有在数据已经有序的情况下，它才能加快。因此，我们也不能把所有数据都用 Numpy 来表示。
-->

第 10 行到第 21 行代码，显示了如何查找一个数组中符合条件的数据，并且返回它的索引。

<!--
很多场景下，我们要关心的是符合条件的数据的位置，而不是它的取值。比如，在通达信公司中，有一个 barssince，就是要求自满足条件以来，经过了多少个 bar。这就是我们只关心索引位置的一例。
-->

argwhere 返回值相当于 nonzero 的转置，在多维数组的情况下，它不能直接用作数组的索引。请自行对比 nonzero 与 argwhere 的用法。

<!--
以 arg 开头的函数，不完全是为了返回索引值。比如 argsort 是用来进行排序的，但它返回的是排序后的索引，类似于 rank。但 rank 返回的是排名，argsort 返回的是索引

```python
import numpy as np

# 创建一个数组
arr = np.array([3, 1, 2])

# 使用 ARGSORT 获取排序后的索引
sorted_indices = np.argsort(arr)

# 再次使用 ARGSORT 获取排名
ranks = np.argsort(sorted_indices) + 1

print("Ranks:", ranks)
```
-->

---

在量化中，有很多情况需要实现筛选功能。比如，在计算上下影线时，我们是用公式$(high - max(open, close))/(high - low)$来进行计算的。如果我们要一次性地计算过去 n 个周期的所有上影线，并且不使用循环的话，那么我们就要使用 np.where, np.select 等筛选功能。

<!--单就这一功能而言，还有更高效地实现方式-->

下面的例子显示了如何使用 np.select 来计算上影线：

```python
import pandas as pd
import numpy as np

bars = pd.DataFrame({
    "open": [10, 10.2, 10.1],
    "high": [11, 10.5, 9.3],
    "low": [9.8, 9.8, 9.25],
    "close": [10.1, 10.2, 10.05]
})

max_oc = np.select([bars.close > bars.open, 
                    bars.close <= bars.open], 
                    [bars.close, bars.open])
print(max_oc)

shadow = (bars.high - max_oc)/(bars.high - bars.low)
print(shadow)

```

np.where 是与 np.select 相近的一个函数，不过它只接受一个条件。

```python
arr = np.arange(6)
cprint("np.where: {}", np.where(arr > 3, 3, arr))
```

这段代码实现了将 3 以上的数字截断为 3 的功能。这种功能被称为 clip，在因子预处理中是非常常用的一个技巧，用来处理异常值 (outlier)。

但它没有办法实现两端截断。此时，但 np.select 能做到，这是 np.where 与 np.select 的主要区别：

---

```python
arr = np.arange(6)
cprint("np.select: {}", np.select([arr<2, arr>4], [2, 4], arr))
```
其结果是，生成的数组，小于 2 的被替换成 2，大于 4 的被替换成 4，其它的保持不变。

<!--
还有一种筛选，是从一个集合中随机筛选出若干样本，我们将在随机数一节中讲到。
-->

<!--
以上介绍的方法，无论是indexing, slicing，最终都引导我们定位到数组的元素。显然，有了这个定位，我们就能修改数组元素。但是，这里也必须强调视图(view)和副本(copy)的概念。因为根据我们定位元素的方法的不同，我们得到的结果，可能是原数组的一个视图，也可能是原数组的一个副本。前者可以修改到原数组元素，后者的修改只能修改副本。

#### 视图和副本

Numpy数组实际上是由两部分组成的，一个是包含实际数据元素的连续数据缓冲区；另一个则是关于数组的元数据。元数据包括数据类型、步幅和其他更容易操作 ndarray 的重要信息，比如shape。

这种组织方式带来了一个好处，即有可能只更改某些元数据（比如数据类型和shape），而不更改数据缓冲区，就可以以不同的方式访问和操作原数组，但看起来象是一个新的数组。这些新数组称为视图。


Numpy中的多数定位操作会返回视图，但有一些则会返回原数组的copy。规则是，基本索引总是创建视图。所以，我们可以这样修改一个数组：

```python
x = np.arange(10)

# 创建了一个视图
y = x[1:3]
x[1:3] = [10, 11]
```

现在y和x[1:3]持有相同的值。因此修改是改在原数据缓冲区上。

另一方面，高级索引总是创建副本，比如：

```python
x = np.arange(9).reshape(3,3)
cprint("原始数组\n{}", x)

y = x[[1, 2]]
cprint("高级索引创建了副本\n{}", y)

# 现在我们修改高级索引副本值
x[[1,2]] = [[10, 11, 12], [13, 14, 15]]
cprint("就地赋值改变了x\n{}", x)

cprint("但y是副本\n{}", y)
cprint("副本的base属性{}", y.base)
cprint("视图的base属性{}", x[1:2].base)
```

上述示例中，比较难以理解的是第8行。我们要记住，这是所谓的in-place分配的一种情况，此时不会创建任何视图或副本。

示例中还给出了判断一个数组究竟是副本还是视图的标准。如果一个数组是视图，那么它的base会指向原数组。而副本的base会指向None。

我们还会在介绍完Structured array之后，再介绍一个常见、但更容易犯错的例子。
-->

### 1.4. 审视 (inspecting) 数组
<!--了解 numpy 的 dtype 类型，shape、ndim、size 和 len 的用法。-->

当我们调用其它人的库时，往往需要与它们交换数据。这时就可能出现数据格式不兼容的问题。为了有能力进行查错，我们必须掌握查看 Numpy 数组特性的一些方法。

我们先如下生成一个简单的数组，再查看它的各种特性：

```python

arr = np.ones((3,2))
cprint("dtype is: {}", arr.dtype)
cprint("shape is: {}", arr.shape)
cprint("ndim is: {}", arr.ndim)
cprint("size is: {}", arr.size)
cprint("'len' is also available: {}", len(arr))

# DTYPE
dt = np.dtype('>i4')
cprint("byteorder is: {}", dt.byteorder)
cprint("name of the type is: {}", dt.name)
cprint('is ">i4" a np.int32?: {}', dt.type is np.int32)

# 复杂的 DTYPE
complex = np.dtype([('name', 'U8'), ('score', 'f4')])
arr = np.array([('Aaron', 85), ('Zoe', 90)], dtype=complex)
cprint("A structured Array: {}", arr)
cprint("Dtype of structured array: {}", arr.dtype)
```

正如 Python 对象都有自己的数据类型一样，Numpy 数组也有自己的数据类型。我们可以通过`arr.dtype`来查看数组的数据类型。

<!--
这里我们是通过 np.ones 生成的数组，数组的各元素都是 1。注意我们得到的 dtype 是 np.float64，这也是 Numpy 中最常见的数据类型。
-->

---

从第 3 行到第 6 行，我们分别输出了数组的 shape, ndim, size 和 len 等属性。ndim 告诉我们数组的维度。shape 告诉我们每个维度的 size 是多少。shape 本身是一个 tuple, 这个 tuple 的 size，也等于 ndim。

size 在不带参数时，返回的是 shape 各元素取值的乘积。len 返回的是第一维的长度。

### 1.5. 数组操作
<!--介绍引起数组形状、size 等改变的相关操作-->

我们在前面的例子中，已经看到过一些引起数组形状改变的例子。比如，要生成一个$3×2$的数组，我们先用 np.arange(6) 来生成一个一维数组，再将它的形状改变为 (2, 3)。

另一个例子是使用 np.concatenate，从而改变了数组的行或者列。

#### 1.5.1. 升维
我们可以通过 reshape, hstack, vstack 来改变数组的维度：
```python

cprint("increase ndim with reshape:\n{}", 
        np.arange(6).reshape((3,2)))

# 将两个一维数组，堆叠为 2*3 的二维数组
cprint("createing from stack: {}", 
        np.vstack((np.arange(3), np.arange(4,7))))

# 将两个 （3，1）数组，堆叠为（3，2）数组
np.hstack((np.array([[1],[2],[3]]), np.array([[4], [5], [6]])))
```

#### 1.5.2. 降维

通过 ravel, flatten, reshape, *split 等操作对数组进行降维。
<!--很多操作，比如像 argwhere，会返回升维的结果，此时我们可能需要在使用前，对其降维-->

---

```python

cprint("ravel: {}", arr.ravel())

cprint("flatten: {}", arr.flatten())

# RESHAPE 也可以用做扁平化
cprint("flatten by reshape: {}", arr.reshape(-1,))

# 使用 HSPLIT, VSPLIT 进行降维
x = np.arange(6).reshape((3, 2))
cprint("split:\n{}", np.hsplit(x, 2))

# RAVEL 与 FLATTEN 的区别：RAVEL 可以操作 PYTHON 的 LIST
np.ravel([[1,2,3],[4, 5, 6]])
```

这里一共介绍了 4 种方法。ravel 与 flatten 用法比较接近。ravel 的行为与 flatten 类似，只不过 ravel 是 np 的一个函数，可作用于 ArrayLike 的数组。

通过 reshape 来进行扁平化也是常用操作。此外，还介绍了 vsplit, hsplit 函数，它们的作用刚好与 vstack，hstack 相反。

#### 1.5.3. 转置

此外，对数组进行转置也是此类例子中的一个。比如，在前面我们提到，np.argwhere 的结果，实际上是 np.nonzero 的转置，我们来验证一下：

```python
x = np.arange(6).reshape(2,3)
cprint("argwhere: {}", np.argwhere(x > 1))

# 我们再来看 NP.NONZERO 的转置
cprint("nonzero: {}", np.array(np.nonzero(x > 1)).T)
```

两次输出结果完全一样。在这里，我们是通过`.T`来实现的转置，它是一个语法糖，正式的函数是`transpose`。

当然，由于 reshape 函数极其强大，我们也可以使用它来完成转置：

---

```python
cprint("transposing array from \n{} to \n{}", 
    np.arange(6).reshape((2,3)),
    np.arange(6).reshape((3,2)))
```

---
***版权声明
本课程全部文字、图片、代码、习题等所有材料，除声明引用外，均由作者本人开发。所有草稿版本均通过第三方 git 服务进行管理，作为拥有版权的证明。未经书面作者授权，请勿引用。***

[^dirichlet]: 狄利克雷，德国数学家。他对数论、傅里叶级数理论和其他数学分析学领域有杰出贡献，并被认为是最早给出现代函数定义的数学家之一和解析数论创始人之一。Dirichlet 数组不仅仅是作为 MPT 求解中的初始值。在 [A selective Portofolio Management Algorithm with Off-Policy Reinforcement Learning Using Dirichlet Distribution](https://www.jieyu.ai/assets/ebooks/off-policy-reinforcement-learning-using-dirichlet-distribution.pdf) 中，作者还提出了一种以狄利克雷分布为策略，计算多个最优投资组合的算法。

[^聚宽]: 聚宽是数据服务商，提供付费的行情数据、因子数据、财务数据等其它数据。他们的网站是www.joinquant.com

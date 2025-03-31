---
<<<<<<< HEAD
title: Numpy核心语法[3]
seq: "04"
series: 量化人的Numpy&Pandas
=======
title: 核心语法[3]
series: 量化人的 Numpy 和 Pandas
seq: "04"
>>>>>>> 2342e9046da59e772aa16e6fc79660fec612df7d
fonts:
    sans: 'AlibabaPuHuiTi-Thin, sans-serif'
slug: numpy-pandas-for-quant-trader-04
date: 2025-03-09
category: tools
motto: Be dazzling! You are qualified.
img: https://images.jieyu.ai/images/hot/mybook/girl-on-sofa.jpg
stamp_width: 60%
stamp_height: 60%
tags: 
    - tools
    - programming
    - Numpy
---

<<<<<<< HEAD

在不同的库之间交换数据，常常会遇到格式问题。比如，我们从第三方数据源拿到的行情数据，它们用的时间字段常常会是字符串。有一些库在存储行情时，对 OHLC 这些字段进行了优化，使用了 4 个字节的浮点数，但如果要传给 talib 进行指标计算，就必须先转换成 8 个字节的浮点数，等等，这就有了类型转换的需求。

---
=======
在不同的库之间交换数据，常常会遇到格式问题。比如，我们从第三方数据源拿到的行情数据，它们用的时间字段常常会是字符串（这是代码少写了几行吗？！）。有一些库在存储行情时，对 OHLC 这些字段进行了优化，使用了 4 个字节的浮点数，但如果要传给 talib 进行指标计算，就必须先转换成 8 个字节的浮点数，等等，这就有了类型转换的需求。
>>>>>>> 2342e9046da59e772aa16e6fc79660fec612df7d

---

此外，我们还会遇到需要将 numpy 数据类型转换为 python 内置类型，比如，将 numpy.float64 转换为 float 的情况。
<<<<<<< HEAD
## 1. 类型转换和 Typing
=======


## 1. 类型转换和 Typing

>>>>>>> 2342e9046da59e772aa16e6fc79660fec612df7d
### 1.1. Numpy 内部类型转换
Numpy 内部类型转换，我们只需要使用 astype 


```python
x = np.array (['2023-04-01', '2023-04-02', '2023-04-03'])
print (x.astype (dtype='datetime64[D]'))

x = np.array (['2014', '2015'])
print (x.astype (np.int32))

x = np.array ([2014, 2015])
print (x.astype (np.str_))
```

<<<<<<< HEAD
!!! tip
=======


!!! tips
>>>>>>> 2342e9046da59e772aa16e6fc79660fec612df7d
    如何将 boolean array 转换成整数类型，特别是，将 True 转为 1，False 转为 - 1？
    在涉及到阴阳线的相关计算中，我们常常需要将 open > close 这样的条件转换为符号 1 和 - 1，以方便后续计算。这个转换可以用：

    ```python
    >>> x = np.array ([True, False])
    >>> x * 2 - 1
    ... array ([ 1, -1])
    ```

---

### 1.2. Numpy 类型与 Python 内置类型转换

如果我们要将 Numpy 数组转换成 Python 数组，可以使用 tolist 函数。

```python
x = np.array ([1, 2, 3])
print (x.tolist ())
```

我们通过 item () 函数，将 Numpy 数组中的元素转换成 Python 内置类型。

```python
x = np.array (['2023-04-01', '2023-04-02'])
y = x.astype ('M8[s]')
y [0].item ()
```

!!! warning
    一个容易忽略的事实是，当我们从 Numpy 数组中取出一个标量时，我们都应该把它转换成为 Python 对象后再使用。否则，会发生一些隐藏的错误，比如下面的例子：

    ```python
    import json
    x = np.arange (5)
    print (json.dumps ([0]))
    print (x [0])

    json.dumps ([x [0]])
    ```

---

!!! warning
    这里最后一行会出错。提示 type int64 is not JSON serializable。把最后一行换成 `json.dumps ([x [0].item ()])` 则可以正常执行。


### 1.3. Typing
从 Python 3.1 起，就开始引入类型注解 (type annotation)，到 Python 3.8，基本上形成了完整的类型注解体系。我们经常看到函数的参数类型注解，比如，下面的代码:

```python
from typing import List
def add (a: List [int], b: int) -> List [int]:
    return [i + b for i in a]
```

从此，Python 代码也就有了静态类型检查支持。

NumPy 的 Typing 模块提供了一系列类型别名（type aliases）和协议（protocols），使得开发者能够在类型注解中更精确地表达 NumPy 数组的类型信息。这有助于静态分析工具、IDE 以及类型检查器提供更准确的代码补全、类型检查和错误提示。

这个模块提供的主要类型是 ArrayLike, NDArray 和 DType。

```python
import numpy
from numpy.typing import ArrayLike, NDArray, DTypeLike
import numpy as np
```

---

```python
def calculate_mean (data: ArrayLike) -> float:
    """计算输入数据的平均值，数据可以是任何 ArrayLike 类型"""
    return np.mean (data)

def add_one_to_array (arr: NDArray [np.float64]) -> NDArray [np.float64]:
    """向一个浮点数数组的每个元素加 1，要求输入和输出都是 np.float64 类型的数组"""
    return arr + 1

def convert_to_int (arr: NDArray, dtype: DTypeLike) -> NDArray:
    """将数组转换为指定的数据类型"""
    return arr.astype (dtype)
```

如果你是在像 vscode 这样的 IDE 中使用上述函数，你就可以看到函数的类型提示。如果传入的参数类型不对，还能在编辑期间，就得到错误提示。

## 2. 拓展阅读

### 2.1. Numpy 的数据类型

在 Numpy 中，有以下常见数据类型。每一个数字类型都有一个别名。在需要传入 dtype 参数的地方，一般两者都可以使用。另外，别名在字符串类型、时间和日期类型上，支持得更好。比如，'S5' 是 Ascii 码字符串别外，它除了指定数据类型之外，还指定了字符串长度。datetime64 [S] 除了表明数据是时间日期类型之外，还表明它的精度到秒。

---

| 类型           | 别名                                                                                                                |
| -------------- | ------------------------------------------------------------------------------------------------------------------- |
| np.int8        | i1                                                                                                                  |
| np.int16       | i2                                                                                                                  |
| np.int32       | i4                                                                                                                  |
| np.int64       | i8                                                                                                                  |
| np.uint8       | u1                                                                                                                  |
| np.uint16      | u2                                                                                                                  |
| np.uint32      | u4                                                                                                                  |
| np.uint64      | u8                                                                                                                  |
| np.float16     | f2                                                                                                                  |
| np.float32     | f4，还可指定结尾方式，比如 '<f4'，表示小端字节序，'=' 表示当前系统字节序，'>f4' 表示大端字节序。其它 float 类型同。 |
| np.float64     | f8                                                                                                                  |
| np.float128    | f16                                                                                                                 |
| np.bool_       | b1                                                                                                                  |
| np.str_        | U (后接长度，例如 U10)                                                                                              |
| np.bytes_      | S (后接长度，例如 S5)                                                                                               |
| np.datetime64  | M8 和 M8[D] M8[h] M8[m] M8[s]，也可写作 datetime64[D] 等                                                            |
| np.timedelta64 | m8 和 m8[D] m8[h] m8[m] m8[s] 等                                                                                    |


## 3. 处理包含 np.nan 的数据

在量化分析中，我们常常会遇到数据为 np.nan 情况。比如，某公司上年利润为负数，今年利润实现正增长，请问要如何表示公司的 YoY 的利润增长呢？

---

!!! info
    np.nan 是 numpy 中的一个特殊值，表示“Not a Number”，即“不是数字”。注意，在 Numpy 中，尽管 np.nan 不是一个数字，但它确实数字类型。确切地说，它是 float 类型。此外，在 float 类型中，还存在 np.inf（正无穷大）和负无穷大 (np.NINF，或者-np.inf)。



又比如，在计算个股的 RSI 或者移动平均线时，最初的几期数据是无法计算出来的（在回测框架 backtrader 中，它把这种现象称之为技术指标的冷启动）。如果不要求返回的技术指标的取值与输入数据长度一致，则会返回短一些、但全部由有效数据组成的数组；否则，此时我们常常使用 np.NaN 或者 None 来进行填充，以确保返回的数据长度与输入数据长度一致。

但是，如果我们要对返回的数组进行统计，比如求均值、最大值、排序，对包含 np.nan 或者 None 的数组，应该如何处理？

### 3.1. 包含 np.nan 和 np.inf 的数组运算

在 numpy 中，提供了对带 np.nan 的数组进行运算的支持。比如有以下数组：

```python
import numpy as np

x = np.array([1, 2, 3, np.nan, 4, 5])
print(x.mean())
```

---

我们将得到一个 nan。实际上，多数情况下，我们希望忽略掉 nan，只对有效数据进行运算，此时得到的结果，我们往往仍然认为是有意义的。

因此，Numpy 提供了许多能处理包含 nan 数据的数组输入的运算函数。下面是一个完整的列表：

_在这里，我们以输入 `np.array([1, 2, 3, np.nan, np.inf, 4, 5])` 为例_



| 函数        | nan 处理 | inf 处理 | 输出 |
| ----------- | -------- | -------- | ---- |
| nanmin      | 忽略     | inf      | 1.0  |
| nanmax      | 忽略     | inf      | inf  |
| nanmean     | 忽略     | inf      | inf  |
| nanmedian   | 忽略     | inf      | 3.5  |
| nanstd      | 传递     | inf      | nan  |
| nanvar      | 传递     | inf      | nan  |
| nansum      | 忽略     | inf      | inf  |
| nanquantile | 忽略     | inf      | 2.25 |
| nancumsum   | 忽略     | inf      | inf  |
| nancumprod  | 忽略     | inf      | inf  |

对 np.nan 的处理中，主要是三类，一类是传递，其结果导致最终结果也是 nan，比如，在计算方差和标准差时；一类是忽略，比如在找最小值时，忽略掉 np.nan，在余下的元素中进行运算；但在计算 cumsum 和 cumprod 时，"忽略"意味着在该元素的位置上，使用前值来填充。我们看一个不包含 np.inf 的示例：

---

```python
x = np.array([1, 2, 3, np.nan, 4, 5])
np.nancumprod(x)
np.nancumsum(x)
```

输出结果是：

```
array([  1.,   2.,   6.,   6.,  24., 120.])

array([ 1.,  3.,  6.,  6., 10., 15.])
```

结果中的第 4 个元素都是由第 3 个元素复制而来的。

如果一个数组中包含 inf，则在任何涉及到排序的操作（比如 max, median, quantile）中，这些元素总是被置于数组的最右侧；如果是代数运算，则结果会被传导为 inf。这些地方，Numpy 的处理方式与我们的直觉是一致的。

除了上述函数，np.isnan 和 np.isinf 函数，也能处理包含 np.nan/np.inf 元素的数组。它们的作用是判断数组中的元素是否为 nan/inf，返回值是一个 bool 数组。

### 3.2. 包含 None 的数组运算
在上一节中，我们介绍的函数能够处理包含 np.nan 和 np.inf 的数组。但是，在 Python 中，None 是任何类型的一个特殊值，如果一个数组包含 None 元素，我们常常仍然会期望能对它进行 sum, mean, max 等运算。但是，Numpy 并没有专门为此准备对应的函数。

---

但是，我们可以通过 astype 将数组转换为 float 类型，在此过程中，所有的 None 元素都转换为 np.nan，然后就可以进行运算了。

```python
x = np.array([3,4,None,55])
x.astype(np.float64)
```

输出为：`array([3., 4., nan, 55.])`

### 3.3. 性能提升

当我们调用 np.nan *函数时，它的性能会比普通的函数慢很多。因此，如果性能是我们关注的问题，我们可以使用 bottleneck 这个库中的同名函数。

```python
from bottleneck import nanstd
import numpy as np
import random

x = np.random.normal(size = 1_000_000)
pos = random.sample(np.arange(1_000_000).tolist(), 5)
x[pos] = np.nan

%timeit nanstd(x)
%timeit np.nanstd(x)
```

---

我们担心数组中 np.nan 元素个数会影响到性能，所以，在上面的示例中，在随机生成数组时，我们只生成了 5 个元素。在随后的一次测试中，我们把 nan 元素的个数增加了 10 倍。实验证明，nan 元素的个数对性能没有什么影响。在所有的测试中，bottlenect 的性能比 Numpy 都要快一倍。

!!! info
    根据 bottleneck 的文档，它的许多函数，要比 Numpy 中的同名函数快 10 倍左右。


---

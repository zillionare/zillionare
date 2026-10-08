---
title: "NumPy Core Syntax: Arrays, Indexing, and Quant Preprocessing"
date: 2025-03-18
slug: en/articles/python/numpy-pandas/02-numpy核心语法-1
tags: [NumPy, Quantitative Trading, Data Preprocessing, Array Manipulation]
excerpt: "A practical guide to NumPy’s ndarray, covering creation, indexing, slicing, and view/copy semantics, with quant-specific examples for factor preprocessing and data manipulation."
lang: en
translation_of: articles/python/numpy-pandas/02-numpy核心语法-1
auto_translated: true
source_sha: 676ba7ed27ffcf59613234b7dc4c3c0f865c0294
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2025/02/grow-with-quantide.jpg"
---

## 1. Basic Data Structures

The core data structure of NumPy is the `ndarray` (n-dimensional array). This is a multi-dimensional, homogeneous, and fixed-size array object.

To handle structured data, NumPy extends this with a data structure called a **Structured Array**.

---

It represents a record using a `void` type tuple, enabling NumPy to express record-type data. Consequently, there are primarily two array-related data types in NumPy.

## 1. Basic Data Structures

The first type is widely known, and we will use it to introduce most NumPy operations. The second type is also frequently used in quantitative finance. For instance, market data obtained via JoinQuant’s `jqdatasdk` allows returning this data type, offering significant convenience in storage and access compared to `DataFrame`. We will dedicate a separate section to this later.

Before using NumPy, we must install and import the library:

```bash
# 安装 NUMPY
pip install numpy
```

Typically, we import and use NumPy using the alias `np`:

```python
import numpy as np
```

To make result outputs more prominent when running these examples in a Notebook, we first define a `cprint` function. It outputs prompt messages verbatim but renders variable values in red font to distinguish them:

---

```python
from termcolor import colored

def cprint(formatter: str, *args):
    colorful = [colored(f"{item}", 'red') for item in args]
    print(formatter.format(*colorful))

# 测试一下 CPRINT
cprint("这是提示信息，后接红色字体输出的变量值：{}", "hello!")
```

Next, we will introduce basic CRUD (Create, Read, Update, Delete) operations.

### 1.1. Creating Arrays

#### 1.1.1. Creating from Python Lists

We can create a simple array using the `np.array` syntax. In this syntax, we can provide a Python list or any object with an `Iterable` interface, such as a tuple.

```python
arr = np.array([1, 2, 3])
cprint("create a simple numpy array: {}", arr)
```

#### 1.1.2. Pre-built Special Arrays

Often, we want NumPy to create arrays with specific values. NumPy provides this support, for example:

---

| Function             | Description                                                                                                             |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `zeros`<br>`zeros_like` | Creates an array of all zeros. `zeros_like` accepts another array and generates a zeros array with the same shape and dtype. Commonly used for initialization. Other `_like` functions follow this pattern. |
| `ones`<br>`ones_like`   | Creates an array of all ones.                                                                                           |
| `full`<br>`full_like`   | Creates an array where all elements are filled with `n`.                                                                |
| `empty`<br>`empty_like` | Creates an empty array.                                                                                                 |
| `eye`<br>`identity`     | Creates an identity matrix.                                                                                             |
| `random.random`       | Creates a random array.                                                                                                 |
| `random.normal`       | Creates a random array following a normal distribution.                                                                 |
| `random.dirichlet`    | Creates a random array following a Dirichlet distribution.                                                              |
| `arange`              | Creates an incrementing array.                                                                                        |
| `linspace`            | Creates a linearly spaced array. Unlike `arange`, this method defaults to a closed interval. The interval between elements can be a float. |

<!--Some less common pre-built functions exist, such as np.indices-->

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

---

!!! warning
    Although the name `empty` suggests it should generate an empty array, the generated array actually contains values. These values are neither `np.nan` nor `None`, but random values. Before using an array generated by `empty`, you must initialize it to handle these random values.
<!--
    Note here that the empty array prints with values, which are random. NumPy provides the `empty` function primarily for performance reasons. It allows us to quickly build an array, which we can then fill with values later. However, since `empty` creates data with random values, we must be cautious. In many cases, we prefer using `zeros` over `empty`.
-->

Generating normal distribution arrays is very useful. In research, we often need to generate price sequences that satisfy certain conditions to further study and compare their characteristics.

For example, if we want to study certain indicators under upward and downward trends, we need the ability to first construct price sequences that conform to these trends. The following example demonstrates how to generate such sequences and plot them:

```python
import numpy as np
import matplotlib.pyplot as plt
```

---

```python
returns = np.random.normal(0, 0.02, size=100)

fig, axes = plt.subplots(1, 3, figsize=(12,4))
c0 = np.random.randint(5, 50)

for i, alpha in enumerate((-0.01, 0, 0.01)):
    r = returns + alpha
    close = np.cumprod(1 + r) * c0
    axes[i].plot(close)
```

The plotted graph is as follows:

---

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/04/same-vol-different-trend.jpg)

<!--
    In many cases, we need to generate normal distribution arrays. For instance, if we want to study the relationship between stock price changes and volatility, such as whether continuous upward and continuous downward movements have the same volatility, we can do so. We can create return sequences from -0.1 (down) to 0.1 (up) in steps of 0.05, and then calculate their volatility. This can be done using:

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

    This example demonstrates how to generate a price sequence from a return array.

    The conclusion is that continuous upward, continuous downward, and sideways sequences can have the same volatility. What is the significance of this? We know that high-quality stocks often have low volatility. This gives us a good starting point. Combined with other indicators, we can screen for high-quality stocks. Of course, knowing the relationship between volatility and price changes, we also know that low volatility does not necessarily imply a high-quality stock.
-->

The example also mentions Dirichlet distribution arrays. These arrays have a characteristic where the sum of all their elements equals 1. For example, in the efficient frontier optimization of Modern Portfolio Theory (MPT), we first need to initialize the weights of various assets (random values) and satisfy the constraint that the sum of asset weights equals 1 (obviously!). In this case, we can use the Dirichlet[2] distribution.

---

<!--Dirichlet, a German mathematician. He made outstanding contributions to number theory, Fourier series theory, and other areas of mathematical analysis, and is considered one of the earliest mathematicians to provide the modern definition of a function and one of the founders of analytic number theory.-->
<!--Of course, we could also use the Gaussian distribution and then normalize it.-->

<!--
    The `arange` array is similar to the `range` syntax, generating an integer array, while `linspace` generates an array with float steps. Additionally, one is a left-closed, right-open interval, while the other is a closed interval on both ends. What is the use of `linspace`?

    Here is an example: judging moving average trends. Assume the moving average array is `ma`, with 10 data points. Then `linspace(ma[0], ma[-1], 10)` represents the chord connecting the two ends. Subtract the chord array from the `ma` array. If the value is positive, the moving average is turning downward; otherwise, it is a concave curve, indicating an upward turn and accelerating rise.
-->
#### 1.1.3. Converting from Existing Arrays

We can also create new arrays from existing ones through copying, slicing, repeating, etc.:

```python
# 复制一个数组
cprint("通过 np.copy 创建：{}", np.copy(np.arange(5)))

# 复制数组的另一种方法
cprint("通过 arr.copy: {}", np.arange(5).copy())

# 使用切片，提取原数组的一部分
cprint("通过切片：{}", np.arange(5)[:2])
```

---

```python
# 合并两个数组
arr = np.concatenate((np.arange(3), np.arange(2)))
cprint("通过 concatenate 合并：{}", arr)

# 重复一个数组
arr = np.repeat(np.arange(3), 2)
cprint("通过 repeat 重复原数组：{}", arr)

# 重复一个数组，注意与 NP.REPEAT 的差异
# NP.TILE 的语义类似于 PYTHON 的 LIST 乘法
arr = np.tile(np.arange(3), 2)
cprint("通过 tile 重复原数组：{}", arr)
```

!!! question
    What is the difference between `np.copy` and `arr.copy`? Are there other similar function pairs in NumPy, and what is the pattern?

<!--
    In array copying, we used two methods: one is `np.copy`, and the other is the `copy` method of the array object itself. What is the difference between these two methods?
-->
---

Note the role of the `axis` parameter in the `concatenate` function:

```python
arr = np.arange(6).reshape((3,2))

# 在 ROW 方向上拼接，相当于增加行，默认行为
cprint("按 axis=0 拼接：\n{}", np.concatenate((arr, arr), axis=0))
# 在 COL 方向上拼接，相当于扩展列
cprint("按 axis=1 拼接：\n{}", np.concatenate((arr, arr), axis=1))
```

### 1.2. Adding/Deleting and Modifying Elements

NumPy arrays are of fixed size. Generally, we do not recommend frequently adding or deleting elements from arrays.

---

However, if such a need arises, we can use the following methods to achieve addition or deletion:
<!--
    If we frequently perform operations that change the array size by adding or deleting elements, we generally use Python's `list` as the data structure instead of NumPy's `array`.
-->

| Function   | Description                                                                                |
| ---------- | ------------------------------------------------------------------------------------------ |
| `append`   | Adds `values` to the end of `arr`.                                                       |
| `insert`   | Inserts the value `value` (scalar or array) at the position specified by `obj` (index or slice). |
| `delete`   | Deletes elements at specified indices.                                                   |

Examples are as follows:

```python
arr = np.arange(6).reshape((3,2))
np.append(arr, [[7,8]], axis=0)
cprint("指定在行的方向上操作、n{}", arr)
```

---

```python
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
    `append` operates along the row direction by default, so `axis=0` can be omitted here.
-->

!!! tip
    Please definitely run the code here, especially the parts regarding `insert`, to understand what "flattening" means.
<!--
    Lines 5–11 compare the different behaviors of `insert` with and without specifying `axis`. Pay special attention: if `axis` is not specified, the array will be flattened into a one-dimensional array after this operation, regardless of its previous dimensions.
-->

<!--
    Line 13 demonstrates how to delete an array element. Note that the second parameter is the coordinate of the element to be deleted; it can be a scalar, a coordinate array, or a slice.
-->

<!--
    Note that in NumPy, most operations do not modify the original array in place but return a new array.
-->

Sometimes we need to modify the values of individual elements. This is how we do it:

---

```python
arr = np.arange(6).reshape(2,3)

arr[0,2] = 3
```

This involves how to locate an array element, which is the content of our next section.

<!--
    !!! warning
        In NumPy, most operations do not execute on the original array but copy and return a new array. The following example reminds us of the potential problems arising from this:

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
### 1.3. Locating, Reading, and Searching

#### 1.3.1. Indexing and Slicing

The indexing and slicing syntax in NumPy is roughly similar to Python, with the main difference being support for multi-dimensional arrays:

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

The above slicing syntax exists in Python but only supports one dimension. Therefore, similar operations on the following Python array will fail:

---

```python
arr = np.arange(6).reshape((3,2)).tolist()

arr[1, :]
```

The error提示 is `list indices must be integers or slices, not tuple`.

<!--
    In the above code, we also converted the NumPy array to a Python list using `tolist()`. Conversions between NumPy objects and Python objects occur frequently, especially conversions between time objects, which require mastery.
-->

#### 1.3.2. Finding, Filtering, and Replacing

In the previous section, we located array elements through indexing. However, in many cases, we first need to find the indices that meet specific conditions through conditional operations. This section introduces related methods.

| Function            | Description                                                   |
| ------------------- | ------------------------------------------------------------- |
| `np.searchsorted` | Searches for a specified value in a sorted array and returns the index. |
| `np.nonzero`      | Returns the indices of non-zero elements, used to find elements in an array that meet conditions. |
| `np.flatnonzero`  | Same as `nonzero`, but returns the indices of non-zero elements in the flattened version of the input array. |
| `np.argwhere`     | Returns the indices of elements that meet conditions, equivalent to the transpose of `nonzero`. |
| `np.argmin`       | Returns the index of the minimum element in the array (note: not the minimum index that meets a condition). |
| `np.argmax`       | Returns the index of the maximum element in the array.        |

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
```

---

```python
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

When using `searchsorted`, note that the array itself must be sorted; otherwise, it will not yield correct results.
<!--
    Why do we discuss this function? After becoming familiar with NumPy, you might want to represent all data using NumPy arrays. This example reminds you that searching in NumPy, due to the lack of indexes, is actually slower. It only speeds up when the data is already sorted. Therefore, we cannot represent all data using NumPy.
-->

Lines 10–21 show how to find data in an array that meets conditions and return their indices.

<!--
    In many scenarios, we care about the position of data that meets conditions, not its value. For example, in Tongda Xin (TDX) software, there is a function `barssince`, which calculates how many bars have passed since a condition was met. This is an example where we only care about the index position.
-->

The return value of `argwhere` is equivalent to the transpose of `nonzero`. In the case of multi-dimensional arrays, it cannot be directly used as an array index. Please compare the usage of `nonzero` and `argwhere` yourself.

<!--
    Functions starting with `arg` are not solely for returning index values. For example, `argsort` is used for sorting, but it returns the indices after sorting, similar to `rank`. However, `rank` returns the ranking, while `argsort` returns the indices.

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

In quantitative finance, there are many situations requiring filtering functionality. For example, when calculating upper shadow lines, we use the formula $(high - max(open, close))/(high - low)$.

---

If we want to calculate the upper shadow lines for the past $n$ periods all at once without using loops, we must use filtering functions like `np.where` and `np.select`.

<!--There are more efficient ways to implement this specific function-->

The following example shows how to use `np.select` to calculate upper shadow lines:

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

`np.where` is a function similar to `np.select`, but it only accepts a single condition.

```python
arr = np.arange(6)
cprint("np.where: {}", np.where(arr > 3, 3, arr))
```

This code implements the functionality of clipping numbers above 3 to 3.

---

This functionality is called `clip`, a very common technique in factor preprocessing used to handle outliers.

However, it cannot perform two-sided clipping. At this point, `np.select` can do this. This is the main difference between `np.where` and `np.select`:

```python
arr = np.arange(6)
cprint("np.select: {}", np.select([arr<2, arr>4], [2, 4], arr))
```
The result is that in the generated array, values less than 2 are replaced with 2, values greater than 4 are replaced with 4, and others remain unchanged.

<!--
    There is another type of filtering: randomly selecting several samples from a set, which we will discuss in the random number section.
-->

<!--
    The methods introduced above, whether indexing or slicing, ultimately lead us to locate array elements. Clearly, with this location, we can modify array elements. However, we must also emphasize the concepts of views and copies. Depending on how we locate elements, the result may be a view of the original array or a copy of the original array. The former can modify the original array's elements, while modifications to the latter only affect the copy.

    #### Views and Copies

    A NumPy array actually consists of two parts: a contiguous data buffer containing the actual data elements, and metadata about the array. Metadata includes data type, strides, and other important information that makes it easier to manipulate `ndarray`, such as `shape`.

    This organization brings a benefit: it is possible to access and operate on the original array in different ways by changing only certain metadata (such as data type and `shape`) without changing the data buffer, making it look like a new array. These new arrays are called views.


    Most location operations in NumPy return views, but some return a copy of the original array. The rule is that basic indexing always creates a view. So, we can modify an array like this:

    ```python
x = np.arange(10)

# 创建了一个视图
y = x[1:3]
x[1:3] = [10, 11]
```

    Now, `y` and `x[1:3]` hold the same values. Therefore, the modification is made on the original data buffer.

    On the other hand, advanced indexing always creates a copy, for example:

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

    In the above example, line 8 is the most difficult to understand. We must remember that this is a case of so-called in-place assignment, where no view or copy is created.

    The example also provides the standard for determining whether an array is a copy or a view. If an array is a view, its `base` points to the original array. The `base` of a copy points to `None`.

    We will introduce another common but error-prone example after introducing the Structured array.
-->

### 1.4. Inspecting Arrays
<!--Understand the usage of numpy's dtype, shape, ndim, size, and len.-->

When we call other people's libraries, we often need to exchange data with them. This may lead to data format incompatibility issues. To be able to debug, we must master some methods for viewing NumPy array properties.

We first generate a simple array as follows, and then view its various properties:

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
```

---

```python
# 复杂的 DTYPE
complex = np.dtype([('name', 'U8'), ('score', 'f4')])
arr = np.array([('Aaron', 85), ('Zoe', 90)], dtype=complex)
cprint("A structured Array: {}", arr)
cprint("Dtype of structured array: {}", arr.dtype)
```

Just as Python objects have their own data types, NumPy arrays have their own data types. We can view the data type of an array using `arr.dtype`.

<!--
    Here, we generated the array using `np.ones`, and all elements of the array are 1. Note that the `dtype` we obtained is `np.float64`, which is also the most common data type in NumPy.
-->

From lines 3 to 6, we output the array's `shape`, `ndim`, `size`, and `len` properties, respectively. `ndim` tells us the dimension of the array. `shape` tells us the size of each dimension. `shape` itself is a tuple, and the size of this tuple is equal to `ndim`.

`size`, when called without arguments, returns the product of the values of the elements in `shape`. `len` returns the length of the first dimension.

## 2. Array Operations
<!--Introduce related operations that change the array's shape, size, etc.-->

In the previous examples, we have already seen some examples that change the array's shape. For example, to generate a $3 \times 2$ array, we first use `np.arange(6)` to generate a one-dimensional array, and then change its shape to $(2, 3)$.

Another example is using `np.concatenate`, which changes the rows or columns of the array.

### 2.1. Increasing Dimensions

We can change the dimension of an array using `reshape`, `hstack`, and `vstack`:

---

```python

cprint("increase ndim with reshape:\n{}", 
        np.arange(6).reshape((3,2)))

# 将两个一维数组，堆叠为 2*3 的二维数组
cprint("createing from stack: {}", 
        np.vstack((np.arange(3), np.arange(4,7))))

# 将两个 （3，1）数组，堆叠为（3，2）数组
np.hstack((np.array([[1],[2],[3]]), np.array([[4], [5], [6]])))
```

### 2.2. Decreasing Dimensions

We can decrease the dimension of an array through operations like `ravel`, `flatten`, `reshape`, and `*split`.
<!--Many operations, such as `argwhere`, return results with increased dimensions, so we may need to decrease the dimension before using them-->


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

This introduces four methods. `ravel` and `flatten` are quite similar in usage. `ravel` behaves similarly to `flatten`, except that `ravel` is a function of `np` and can act on arrays of type `ArrayLike`.

---

Flattening through `reshape` is also a common operation. Additionally, the `vsplit` and `hsplit` functions are introduced, which do the opposite of `vstack` and `hstack`.

### 2.3. Transposition

Furthermore, transposing an array is also an example of such operations. For instance, earlier we mentioned that the result of `np.argwhere` is actually the transpose of `np.nonzero`. Let's verify this:

```python
x = np.arange(6).reshape(2,3)
cprint("argwhere: {}", np.argwhere(x > 1))

# 我们再来看 NP.NONZERO 的转置
cprint("nonzero: {}", np.array(np.nonzero(x > 1)).T)
```

The two output results are exactly the same. Here, we achieved transposition through `.T`, which is a syntax sugar. The formal function is `transpose`.


---

Of course, since the `reshape` function is extremely powerful, we can also use it to complete transposition:


```python
cprint("transposing array from \n{} to \n{}", 
    np.arange(6).reshape((2,3)),
    np.arange(6).reshape((3,2)))
```

<hr>

Dirichlet, a German mathematician. He made outstanding contributions to number theory, Fourier series theory, and other areas of mathematical analysis, and is considered one of the earliest mathematicians to provide the modern definition of a function and one of the founders of analytic number theory. Dirichlet arrays can serve as initial values in MPT solving.

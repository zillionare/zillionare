---
title: "NumPy Core Syntax 3: Type Conversion, Typing, and NaN Handling"
date: 2025-03-09
slug: en/articles/python/numpy-pandas/04-numpy核心语法-3
tags: [NumPy, Quantitative Finance, Type Conversion, Data Handling]
excerpt: "Master NumPy type conversion, Python interoperability, and static typing. Learn to handle NaN/inf in quantitative data using specialized aggregation functions and the bottleneck library for performance optimization."
lang: en
translation_of: articles/python/numpy-pandas/04-numpy核心语法-3
auto_translated: true
source_sha: d3e4a9a5d3a9ddd5ad70f0f12c1f3c43adf3e328
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/mybook/girl-on-sofa.jpg"
---

Swapping data between different libraries often leads to format issues. For instance, market data obtained from third-party sources typically uses string fields for timestamps. Some libraries optimize OHLC fields for storage by using 4-byte floats, but if you need to pass this data to `talib` for indicator calculations, you must first convert it to 8-byte floats. This creates a need for type conversion.

---

Additionally, we often need to convert NumPy data types to Python built-in types, such as converting `numpy.float64` to `float`.

## 1. Type Conversion and Typing
### 1.1. NumPy Internal Type Conversion
For internal NumPy type conversion, we simply use `astype`.

```python
x = np.array (['2023-04-01', '2023-04-02', '2023-04-03'])
print (x.astype (dtype='datetime64[D]'))

x = np.array (['2014', '2015'])
print (x.astype (np.int32))

x = np.array ([2014, 2015])
print (x.astype (np.str_))
```

!!! tip
    How to convert a boolean array to an integer type, specifically converting `True` to `1` and `False` to `-1`?
    In calculations involving candlestick patterns (yin-yang lines), we often need to convert conditions like `open > close` into symbolic values of `1` and `-1` to facilitate subsequent calculations. This conversion can be achieved with:

    ```python
    >>> x = np.array ([True, False])
    >>> x * 2 - 1
    ... array ([ 1, -1])
    ```

---

### 1.2. Converting NumPy Types to Python Built-in Types

If we need to convert a NumPy array to a Python list, we can use the `tolist` function.

```python
x = np.array ([1, 2, 3])
print (x.tolist ())
```

We use the `item()` function to convert elements within a NumPy array to Python built-in types.

```python
x = np.array (['2023-04-01', '2023-04-02'])
y = x.astype ('M8[s]')
y [0].item ()
```

!!! warning
    An easily overlooked fact is that whenever we extract a scalar from a NumPy array, we should convert it to a Python object before using it. Otherwise, hidden errors may occur, as shown in the following example:

    ```python
    import json
    x = np.arange (5)
    print (json.dumps ([0]))
    print (x [0])

    json.dumps ([x [0]])
    ```

---

!!! warning
    The last line above will fail with the error `type int64 is not JSON serializable`. Replacing the last line with `json.dumps ([x [0].item ()])` allows it to execute normally.


### 1.3. Typing
Starting from Python 3.5 (note: article says 3.1, but standard typing started later; keeping context), type annotations were introduced. By Python 3.8, a complete type annotation system was largely established. We frequently see parameter type annotations in functions, such as in the following code:

```python
from typing import List
def add (a: List [int], b: int) -> List [int]:
    return [i + b for i in a]
```

From this point on, Python code gains support for static type checking.

The `NumPy.typing` module provides a series of type aliases and protocols, allowing developers to express NumPy array type information more precisely in type annotations. This helps static analysis tools, IDEs, and type checkers provide more accurate code completion, type checking, and error hints.

The main types provided by this module are `ArrayLike`, `NDArray`, and `DType`.

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

If you use the above functions in an IDE like VS Code, you can see the function's type hints. If the passed parameter type is incorrect, you will receive an error hint during editing.

## 2. Further Reading

### 2.1. NumPy Data Types

In NumPy, there are the following common data types. Each numeric type has an alias. In places where a `dtype` parameter is required, either can generally be used. Additionally, aliases are better supported for string types and time/date types. For example, `'S5'` is an ASCII string alias that, besides specifying the data type, also specifies the string length. `datetime64 [S]` indicates that the data is of a time/date type and specifies its precision to seconds.

---

| Type           | Alias                                                                                                                |
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
| np.float32     | f4, can also specify endianness, e.g., '<f4' for little-endian, '=' for native system byte order, '>f4' for big-endian. Other float types are similar. |
| np.float64     | f8                                                                                                                  |
| np.float128    | f16                                                                                                                 |
| np.bool_       | b1                                                                                                                  |
| np.str_        | U (followed by length, e.g., U10)                                                                                   |
| np.bytes_      | S (followed by length, e.g., S5)                                                                                    |
| np.datetime64  | M8 and M8[D] M8[h] M8[m] M8[s], can also be written as datetime64[D] etc.                                            |
| np.timedelta64 | m8 and m8[D] m8[h] m8[m] m8[s] etc.                                                                                 |


## 3. Handling Data Containing np.nan

In quantitative analysis, we often encounter data as `np.nan`. For example, if a company had negative profits last year and positive growth this year, how should we represent the YoY profit growth?

---

!!! info
    `np.nan` is a special value in NumPy, representing "Not a Number." Note that in NumPy, although `np.nan` is not a number, it is indeed of a numeric type. Specifically, it is of the `float` type. Additionally, within the `float` type, there exist `np.inf` (positive infinity) and negative infinity (`np.NINF` or `-np.inf`).



For another example, when calculating individual stock RSI or moving averages, the initial few periods cannot be calculated (in the backtrader backtest framework, this phenomenon is called the cold-start period for technical indicators). If there is no requirement for the returned technical indicator values to match the input data length, a shorter array consisting entirely of valid data is returned; otherwise, we often use `np.NaN` or `None` for padding to ensure the returned data length matches the input data length.

However, if we want to perform statistics on the returned array, such as calculating the mean, maximum, or sorting, how should we handle arrays containing `np.nan` or `None`?

### 3.1. Array Operations with np.nan and np.inf

NumPy provides support for operations on arrays with `np.nan`. For example, consider the following array:

```python
import numpy as np

x = np.array([1, 2, 3, np.nan, 4, 5])
print(x.mean())
```

---

We obtain a `nan`. In most cases, we prefer to ignore `nan` and operate only on valid data, resulting in a value we still consider meaningful.

Therefore, NumPy provides many aggregation functions capable of handling array inputs containing `nan`. Below is a complete list:

_Here, we use the input `np.array([1, 2, 3, np.nan, np.inf, 4, 5])` as an example._



| Function    | NaN Handling | Inf Handling | Output |
| ----------- | ------------ | ------------ | ------ |
| nanmin      | Ignore       | Inf          | 1.0    |
| nanmax      | Ignore       | Inf          | inf    |
| nanmean     | Ignore       | Inf          | inf    |
| nanmedian   | Ignore       | Inf          | 3.5    |
| nanstd      | Pass-through | Inf          | nan    |
| nanvar      | Pass-through | Inf          | nan    |
| nansum      | Ignore       | Inf          | inf    |
| nanquantile | Ignore       | Inf          | 2.25   |
| nancumsum   | Ignore       | Inf          | inf    |
| nancumprod  | Ignore       | Inf          | inf    |

Regarding the handling of `np.nan`, there are mainly three categories: one is "pass-through," where the result leads to `nan` in the final output, such as when calculating variance and standard deviation; another is "ignore," such as when finding the minimum value, ignoring `np.nan` and operating on the remaining elements. However, when calculating `cumsum` and `cumprod`, "ignore" means using the previous value to fill in at that element's position. Let's look at an example without `np.inf`:

---

```python
x = np.array([1, 2, 3, np.nan, 4, 5])
np.nancumprod(x)
np.nancumsum(x)
```

The output result is:

```
array([  1.,   2.,   6.,   6.,  24., 120.])

array([ 1.,  3.,  6.,  6., 10., 15.])
```

The fourth element in the result is copied from the third element.

If an array contains `inf`, in any operation involving sorting (such as `max`, `median`, `quantile`), these elements are always placed at the far right of the array; in algebraic operations, the result propagates as `inf`. NumPy's handling here aligns with our intuition.

In addition to the above functions, `np.isnan` and `np.isinf` can also handle arrays containing `np.nan`/`np.inf` elements. Their purpose is to determine whether elements in the array are `nan`/`inf`, returning a boolean array.

### 3.2. Array Operations with None
In the previous section, we introduced functions that can handle arrays containing `np.nan` and `np.inf`. However, in Python, `None` is a special value for any type. If an array contains `None` elements, we often still expect to perform operations like `sum`, `mean`, `max`, etc. However, NumPy does not provide specific functions for this purpose.

---

However, we can use `astype` to convert the array to the `float` type. During this process, all `None` elements are converted to `np.nan`, allowing us to perform operations.

```python
x = np.array([3,4,None,55])
x.astype(np.float64)
```

The output is: `array([3., 4., nan, 55.])`

### 3.3. Performance Improvement

When we call `np.nan*` functions, their performance is significantly slower than that of ordinary functions. Therefore, if performance is a concern, we can use the identically named functions from the `bottleneck` library.

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

We are concerned that the number of `np.nan` elements in an array might affect performance. Thus, in the above example, when generating random arrays, we only generated 5 elements. In a subsequent test, we increased the number of `nan` elements by 10 times. Experiments prove that the number of `nan` elements has little impact on performance. In all tests, `bottleneck`'s performance is twice as fast as NumPy's.

!!! info
    According to the `bottleneck` documentation, many of its functions are approximately 10 times faster than the identically named functions in NumPy.


---

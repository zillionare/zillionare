---
title: Numpy核心语法[5]
series: 量化人的 Numpy 和 Pandas
seq: "06"
fonts:
    sans: 'AlibabaPuHuiTi-Thin, sans-serif'
slug: numpy-pandas-for-quant-trader-06
date: 2025-03-23
category: tools
motto: Tough times never last, but tough people do.
img: https://images.jieyu.ai/images/hot/mybook/christmas.jpg
stamp_width: 60%
stamp_height: 60%
tags: 
    - tools
    - programming
    - Numpy
---

“日期和时间的处理从来都不简单。时区、夏令时、闰秒等问题让时间计算变得复杂。Numpy 提供了高效的日期时间处理工具，帮助我们轻松应对这些挑战。”

---

## 1. 日期和时间

一些第三方数据源传递给我们的行情数据，常常会用字符串形式，或者整数（从 unix epoch time 起）格式来表示行情的时间。比如，akshare 和 tushare 许多接口给出的行情数据就是字符串格式；而 QMT 很多时候，会将行情时间用整数表示。掌握这些格式与 Numpy 的日期时间格式转换、以及 Numpy 到 Python 对象的时间日期转换是非常有必要的。

但是在任何编程语言中，日期和时间的处理从来都不简单。

!!! info
    很少有程序员/研究员了解这一点：日期和时间并不是一个数学上或者物理上的一个客观概念。时区的划分、夏令时本身就是一个政治和法律上的概念；一些地方曾经使用过夏令时，后来又取消了这种做法。其次，关于闰秒 [^闰秒] 的决定，也并不是有章可循的，它是由一个委员会开会来临时决定的。这种决定每年做一次。所有这些决定了我们无法通过一个简单的数学公式来计算时间及其变化，特别是在时区之间的转换。

<!--直到 Python 3.9，Python 还在为实现日期和时间努力。Zoneinfo 就是在这一版加入到 Python 中的。-->

关于时间，首先我们要了解有所谓的 timezone aware 时间和 timezone naive 时间。当我们说到晚上 8 时开会时，这个时间实际上默认地包含了时区的概念。如果这是一个跨国会议，但你在通知时不告诉与会方时区，就会导致其它人无法准时出席 -- 他们将会在自己时区的晚上 8 时上线。


如果一个时间对象不包含时区，它就是 timezone naive 的；否则，它是 timezone aware 的。但这只是针对时间对象（比如，Python 中的 datetime.datetime）才有的意义；日期对象（比如，Python 中的 datetime.date）是没有时区的。

---

```python
import pytz
import datetime

# 通过 DATETIME.NOW() 获得的时间没有时区信息
# 返回的是标准时间，即 UTC 时间，等同于调用 UTCNOW()
now = datetime.datetime.now()
print(f"now() without param: {now}, 时区信息{now.tzinfo}")

now = datetime.datetime.utcnow()
print(f"utcnow: {now}, 时区信息{now.tzinfo}")

# 构造 TIMEZONE 对象
cn_tz = pytz.timezone('Asia/Shanghai')
now = datetime.datetime.now(cn_tz)
print(f"现在时间{now}, 时区信息{now.tzinfo}")
print("现在日期：", now.date())

try:
    print(now.date().tzinfo)
except AttributeError:
    print("日期对象没有时区信息")
```

上述代码将依次输出：

```python
now() 不带参数：2024-05-19 11:03:41.550328, 时区信息 None
utcnow: 2024-05-19 11:03:41.550595, 时区信息 None
现在时间 2024-05-19 19:03:41.550865+08:00, 时区信息 Asia/Shanghai
现在日期：2024-05-19
日期对象没有时区信息
```

---

不过，限于篇幅，我们对时间问题的介绍只能浅尝辄止。在这里，我们主要关注在 Numpy 中，日期/时间如何表示，它们彼此之间如何比较、转换，以及如何与 Python 对象进行比较和转换。

<!--类似的问题，我们在 pandas 中也常常遇到-->

在 Numpy 中，日期/时间总是用一个 64 位整数（np.datetime64）来表示，此外，还关联了一个表示其单位（比如，纳秒、秒等）的元数据结构。`np.datetime64`是没有时区概念的。

```python
tm = np.datetime64('1970-01-01T00:00:00')
print(tm)
print(tm.dtype)
```

这将显示为：

```python
1970-01-01T00:00:00
datetime64[s]
```

这里的`[s]`就是我们前面所说的时间单位。其它常见单位还有`[ms]`、`[us]`、`[ns]`等等。
<!--我们也可以用 ISO 格式（1970-01-01T00:00:00+0800) 传入时间。但是，numpy 会给出警告，提示未来版本中，将不允许传入时区信息.-->
除了从字符串解释之外，我们还可以直接将 Python 对象转换成`np.datetime64`，反之亦然：

```python
tm = np.datetimet64(datetime.datetime.now())
print(tm)

print(tm.item())
print(tm.astype(datetime.datetime))
```

---

下面我们来看看如何实现不同格式之间的批量转换。这在处理 akshare, tushare 或者 QMT 等第三方数据源提供的行情数据时，非常常见。

首先我们构造一个时间数组。顺便提一句，这里我们将使用`np.timedelta64`这个时间差分类型：

```python
now = np.datetime64(datetime.datetime.now())
arr = np.array([now + np.timedelta64(i, 'm') for i in range(3)])
arr
```

输出结果如下：

```python
array(['2024-05-19T12:57:47.349178', 
       '2024-05-19T12:58:47.349178',
       '2024-05-19T12:59:47.349178'], 
     dtype='datetime64[us]')
```

<!--这里我们给 timedelta64() 函数传入了参数'm'，表示以分钟为单位。-->

我们可以通过`np.datetime64.astype()`方法将时间数组转换为 Python 的时间对象：

```python
time_arr = arr.astype(datetime.datetime)

# 转换后的数组，每个元素都是 TIMEZONE NAIVE 的 DATETIME 对象
print(type(time_arr[0]))
```

---

```python
# !!! 技巧
# 如何把 NP.DATETIME64 数组转换为 PYTHON DATETIME.DATE 数组？
date_arr = arr.astype('datetime64[D]').astype(datetime.date)
# 或者 -- 两者的容器不一样
date_arr = arr.astype('datetime64[D]').tolist()
print(type(date_arr[0]))
```

<!--第 8 行与第 10 行的区别，前者仍然是一个 numpy 数组，dtype 为'O'；后者则是 Python List-->

这里的关键是，我们之前生成的`arr`数组，其元素类型为`np.datetime64[us]`。它到 Python `datetime.date`的转换将损失精度，所以 Numpy 要求我们显式地指定转换类型。

<!--总结一下，转换 numpy 标量到 Python 对象时，我们可以用 item() 或者 astype 的方法。转换 numpy 数组到 Python 对象时，我们可以用 astype() 方法。-->

如何将以字符串表示的时间数组转换为 Numpy datetime64 对象数组呢？答案仍然是 astype() 方法。

```python
# 将时间数组转换为字符串数组
str_arr_time = arr_time.astype(str)
print(str_arr_time)

# 再将字符串数组转换为 DATETIME64 数组，精度指定为 D
str_arr_time.astype('datetime64[D]')
```

显示结果为：

```python
array(['2024-05-19T12:57:47.349178', 
       '2024-05-19T12:58:47.349178',
       '2024-05-19T12:59:47.349178'], 
       dtype='datetime64[us]')
```

---

```python
array([
    '2024-05-19', 
    '2024-05-19'],               
    dtype='datetime64[D]')
```

最后，我们给一个 QMT 获取交易日历后的格式转换示例。在 QMT 中，我们通过`get_trading_dates`来获取交易日历，该函数返回的是一个整数数组，每个元素的数值，是从 unix epoch 以来的毫秒数。

我们可以通过以下方法对其进行转换：

```python
import numpy as np

days = get_trading_dates('SH', start_time='', end_time='', count=10)
np.array(days, dtype='datetime64[ms]').astype(datetime.date)
```

QMT 官方没有直接给出交易日历转换方案，但给出åå了如何将 unix epoch 时间戳转换为 Python 时间对象（但仍以字符串表示）：

```python
import time

def conv_time(ct):
    # conv_time(1476374400000) --> '20161014000000.000'
    local_time = time.localtime(ct / 1000)
    data_head = time.strftime('%Y%m%d%H%M%S', local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = '%s.%03d' % (data_head, data_secs)
    return time_stamp

conv_time(1693152000000)
```

我们需要对每一个数组元素使用上述解析方法。官方方案的优点是不依赖任何三方库。不过，没有量化程序能离开 Numpy 库，所以，我们的方案并未增加第三方库的依赖。


---


## 2. 字符串操作

你的数据源、或者本地存储方案很可能使用 Numpy Structured Array 或者 Rec Array 返回证券列表。很显然，证券列表中一定会包括字符串，因为它一定会存在证券代码列和证券名称列。有一些还会返回证券的地域属性和其它属性，这也往往是字符串。

<!--如果你使用 clickhouse 来存储证券列表，那么查询时就可能返回这两种数据结构-->

对证券列表，我们常常有以下查询操作：

1. 获取在某个板块上市的股票列表，比如，北交所、科创板和创业板与主板的个股交易规则上有一些不同，因此，我们的策略很可能需要单独为这些板块构建。这就有了按板块过滤证券列表的需要。也可能我们要排除 ST，刚上市新股。这些都可以通过字符串操作来实现。
2. 市场上有时候会出现魔幻的名字炒作。比如龙年炒龙字头（或者含龙的个股）、炒作“东方”、炒作“中”字头。作为量化人，参与这样的炒作固然不可取，但我们要拥有分析市场、看懂市场的能力。

Numpy 中的大多数字符串操作都封装在 numpy.char 这个包下面。它主要提供了一些用于格式化的操作（比如左右填充对齐、大小写转换等）、查找和替换操作。

下面的代码展示了如何从证券列表中过滤创业板：

```python

import numpy as np
import numpy.char as nc
```

---

```python
# 生成 STRUCTURED ARRAY, 字段有 SYMBOL, NAME, IPO DATE
arr = np.array([('600000.SH', '中国平安', '1997-08-19'),
                ('000001.SZ', '平安银行', '1997-08-19'),
                ('301301.SZ', '川宁生物', '2012-01-01')
                ], dtype=[('symbol', 'S10'), ('name', 'S10'), ('ipo_date', 'datetime64[D]')])

def get_cyb(arr):
    mask = np.char.startswith(arr["symbol"], b"30")
    return arr[mask]
```


!!! question
    我们在查找创业板股票时，使用的是 b"30"来进行匹配。为何要用 b"30"而不是"30"?

<!--这是因为，我们定义数组时，symbol 字段的类型是 ascii 型的，也即 bypte 型，而不是 Unicode 型的。所以，回过头来，我们应该在定义时，就使用"U10"来定义-->

注意第 11 行，我们要通过`np.char.startswith()`来使用`startswith`函数。任何一个 numpy array 对象都没有这个方法。

".SZ"是我们的数据源给股票编制的交易所代码。不同的数据源，可能使用不同的交易所代码。比如，聚宽数据源会使用.XSHG 表示上交所，.XSHE 表示深交所。现在，如果我们要将上述代码转换为聚宽的格式，应该如何操作？

```python
# 生成 STRUCTURED ARRAY, 字段有 SYMBOL, NAME, IPO DATE
arr = np.array([('600000.SH', '中国平安', '1997-08-19'),
                ('000001.SZ', '平安银行', '1997-08-19'),
                ('301301.SZ', '川宁生物', '2012-01-01')
                ], dtype=[('symbol', 'U10'), ('name', 'U10'), ('ipo_date', 'datetime64[D]')])
```

---

```python
def translate_exchange_code(arr):
    symbols = np.char.replace(arr["symbol"], ".SH", ".XSHG")
    print(symbols)
    symbols = np.char.replace(symbols, ".SZ", ".XSHE")

    arr["symbol"] = symbols
    return arr

translate_exchange_code(arr)
```

这一次，我们把 symbol 和 name 的定义改为 Unicode 型，以避免我们查找时，要输入像 b"30"这样的字面量。

但输出的结果可能让人意外，因为我们将得到这样的输出：

```python
array([('600000.XSH', '中国平安', '1997-08-19'),
       ('000001.XSH', '平安银行', '1997-08-19'),
       ('301301.XSH', '川宁生物', '2012-01-01')],
      dtype=[('symbol', '<U10'), ('name', '<U10'), ('ipo_date', '<M8[D]')])

```

!!! question
    发生了什么？我们得到了一堆以".XSH"结尾的 symbol，它们本应该是"600000.XSHG"这样的字符串。错在哪里，又该如何修改？

<!--原因是，我们定义的 symbol 只有 10 个字符，替换后，发生溢出了。-->

在上面的示例中，如果我们把替换字符串改为空字符串，就实现了删除操作。这里就不演示了。

char 模块还提供了字符串相等比较函数`equal`:

---

```python
arr = array([('301301.SZ', '川宁生物', '2012-01-01')],
      dtype=[('symbol', '<U10'), ('name', '<U10'), ('ipo_date', '<M8[D]')])

arr[np.char.equal(arr["symbol"], "301301.SZ")]
```

在这个特殊的场景下，我们也可以直接使用以下语法：

```python
arr[arr["symbol"] == "301301.SZ"]
```

!!! tip 
    np.char 下的函数很多，如何记忆？实际上，这些函数多数是 Python 中 str 的方法。如果你熟悉 Pandas，就会发现 Pandas 中也有同样的用法。因此，像`upper`, `lower`, `strip`这样的`str`函数，你可以直接拿过来用。


Numpy 中的字符串函数另一个比较常用的场景，就是执行格式化。你可以通过`ljust`, 'center', `rjust`在显示一个数组前，将它们的各列数据进行左右空格填充，这样，输出时就可以比较整齐。

!!! question
    2024 年 5 月 10 日起，南京化纤走出 7 连板行情，短短 7 日，股价翻倍。市场上还有哪些名字中包含化纤的个股？它们的涨跌是否存在相关性或者跨周期相关性？

---

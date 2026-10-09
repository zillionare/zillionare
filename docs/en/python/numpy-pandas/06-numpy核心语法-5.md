---
title: "NumPy Date/Time and String Ops for Quant Data"
date: 2025-03-23
slug: en/articles/python/numpy-pandas/06-numpy核心语法-5
tags: [NumPy, Quant Data, Datetime, String Processing]
excerpt: "Master NumPy datetime64 conversions and char array operations to handle messy market data from sources like AkShare and QMT efficiently."
lang: en
translation_of: articles/python/numpy-pandas/06-numpy核心语法-5
auto_translated: true
source_sha: f26f76b4ef7cb14ee951898cfd31971a27535864
cover: "https://cdn.jsdelivr.net/gh/zillionare/images@main/images/hot/mybook/christmas.jpg"
---

“Handling dates and times has never been simple. Issues like time zones, daylight saving time, and leap seconds complicate time calculations. NumPy provides efficient datetime tools to help us easily tackle these challenges.”

---

## 1. Dates and Times

Third-party data sources often deliver market data timestamps as strings or integers (Unix epoch time). For instance, many interfaces from AkShare and Tushare return string-formatted data, while QMT frequently represents timestamps as integers. It is essential to master the conversion between these formats and NumPy’s datetime formats, as well as the conversion from NumPy to Python datetime objects.

However, date and time handling remains complex in any programming language.

!!! info
    Few programmers or researchers realize this: dates and times are not objective mathematical or physical concepts. Time zone divisions and daylight saving time (DST) are political and legal constructs; some regions have adopted and later abolished DST. Furthermore, the decision on leap seconds [^leap second] is not governed by a fixed rule but is made ad hoc by a committee meeting annually. These factors prevent us from calculating time and its variations, especially across time zones, using a simple mathematical formula.

<!--Until Python 3.9, Python was still working on date and time implementation. Zoneinfo was added in this version.-->

Regarding time, we must first distinguish between timezone-aware and timezone-naive times. When we say “meet at 8 PM,” this time implicitly includes a time zone concept. If it is a cross-border meeting and you do not specify the time zone to participants, others will join at 8 PM in their respective local time zones, leading to confusion.

If a time object does not contain a time zone, it is timezone-naive; otherwise, it is timezone-aware. This distinction applies only to time objects (e.g., `datetime.datetime` in Python); date objects (e.g., `datetime.date`) do not have time zones.

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

The above code will output sequentially:

```python
now() 不带参数：2024-05-19 11:03:41.550328, 时区信息 None
utcnow: 2024-05-19 11:03:41.550595, 时区信息 None
现在时间 2024-05-19 19:03:41.550865+08:00, 时区信息 Asia/Shanghai
现在日期：2024-05-19
日期对象没有时区信息
```

---

Due to space constraints, our introduction to time issues here is superficial. We primarily focus on how dates/times are represented in NumPy, how they compare and convert to each other, and how they interact with Python objects.

<!--Similar issues are common in pandas as well-->

In NumPy, dates/times are always represented by a 64-bit integer (`np.datetime64`) associated with a metadata structure indicating the unit (e.g., nanoseconds, seconds). `np.datetime64` has no time zone concept.

```python
tm = np.datetime64('1970-01-01T00:00:00')
print(tm)
print(tm.dtype)
```

This will display as:

```python
1970-01-01T00:00:00
datetime64[s]
```

Here, `[s]` represents the time unit mentioned earlier. Other common units include `[ms]`, `[us]`, `[ns]`, etc.
<!--We can also pass time in ISO format (e.g., 1970-01-01T00:00:00+0800), but NumPy will issue a warning that time zone information will not be allowed in future versions.-->

Besides parsing from strings, we can directly convert Python objects to `np.datetime64` and vice versa:

```python
tm = np.datetimet64(datetime.datetime.now())
print(tm)

print(tm.item())
print(tm.astype(datetime.datetime))
```

---

Next, let’s look at how to perform batch conversions between different formats. This is very common when processing market data from third-party sources like AkShare, Tushare, or QMT.

First, we construct a time array. By the way, here we will use the `np.timedelta64` type for time differences:

```python
now = np.datetime64(datetime.datetime.now())
arr = np.array([now + np.timedelta64(i, 'm') for i in range(3)])
arr
```

The output is as follows:

```python
array(['2024-05-19T12:57:47.349178', 
       '2024-05-19T12:58:47.349178',
       '2024-05-19T12:59:47.349178'], 
     dtype='datetime64[us]')
```

<!--Here, we passed the parameter 'm' to timedelta64(), indicating minutes.-->

We can convert the time array to Python time objects using the `np.datetime64.astype()` method:

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

<!--The difference between line 8 and line 10: the former is still a NumPy array with dtype 'O'; the latter is a Python List.-->

The key point here is that the `arr` array we generated earlier has elements of type `np.datetime64[us]`. Converting it to Python `datetime.date` will lose precision, so NumPy requires us to explicitly specify the conversion type.

<!--To summarize, when converting NumPy scalars to Python objects, we can use `item()` or `astype()`. When converting NumPy arrays to Python objects, we can use `astype()`.-->

How do we convert an array of time strings to a NumPy `datetime64` object array? The answer is still the `astype()` method.

```python
# 将时间数组转换为字符串数组
str_arr_time = arr_time.astype(str)
print(str_arr_time)

# 再将字符串数组转换为 DATETIME64 数组，精度指定为 D
str_arr_time.astype('datetime64[D]')
```

The display result is:

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

Finally, we provide an example of format conversion after fetching the trading calendar from QMT. In QMT, we use `get_trading_dates` to retrieve the trading calendar, which returns an integer array where each element represents the number of milliseconds since the Unix epoch.

We can convert it using the following method:

```python
import numpy as np

days = get_trading_dates('SH', start_time='', end_time='', count=10)
np.array(days, dtype='datetime64[ms]').astype(datetime.date)
```

QMT’s official documentation does not directly provide a trading calendar conversion solution but shows how to convert Unix epoch timestamps to Python time objects (still represented as strings):

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

We need to apply the above parsing method to each array element. The advantage of the official solution is that it does not depend on any third-party libraries. However, since no quantitative program can function without NumPy, our solution does not add third-party library dependencies.

---


## 2. String Operations

Your data source or local storage scheme may return security lists using NumPy Structured Arrays or Rec Arrays. Clearly, security lists must include strings, as they will definitely contain columns for security codes and names. Some may also return regional attributes and other properties, which are often strings.

<!--If you use ClickHouse to store security lists, queries may return these two data structures-->

For security lists, we often perform the following query operations:

1. Retrieve lists of stocks listed in specific sectors. For example, the trading rules for stocks on the Beijing Stock Exchange, the Science and Technology Innovation Board (STAR Market), and the ChiNext differ from the Main Board. Therefore, our strategies may need to be built separately for these sectors. This creates a need to filter security lists by sector. We may also need to exclude ST stocks or newly listed IPOs. All of these can be achieved through string operations.
2. The market sometimes experiences magical name-based speculation. For instance, during the Year of the Dragon, speculation focused on stocks with “Dragon” in their names (or containing “Dragon”), “Dongfang” (East), or “Zhong” (China) prefixes. While it is inadvisable for quants to participate in such speculation, we must possess the ability to analyze and understand the market.

Most string operations in NumPy are encapsulated under the `numpy.char` package. It primarily provides formatting operations (e.g., left/right padding, case conversion) and search-and-replace operations.

The following code demonstrates how to filter out ChiNext stocks from a security list:

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
    When searching for ChiNext stocks, we use `b"30"` for matching. Why use `b"30"` instead of `"30"`?

<!--This is because when we defined the array, the `symbol` field type was ASCII (byte) type, not Unicode type. Therefore, we should have used "U10" to define it during definition.-->

Note line 11: we use the `startswith` function via `np.char.startswith()`. No standard NumPy array object has this method.

".SZ" is the exchange code assigned by our data source to stocks. Different data sources may use different exchange codes. For example, JoinQuant data sources use `.XSHG` for the Shanghai Stock Exchange and `.XSHE` for the Shenzhen Stock Exchange. Now, if we want to convert the above code to JoinQuant’s format, how should we proceed?

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

This time, we changed the definition of `symbol` and `name` to Unicode type to avoid entering literals like `b"30"` during searches.

However, the output may be surprising, as we get:

```python
array([('600000.XSH', '中国平安', '1997-08-19'),
       ('000001.XSH', '平安银行', '1997-08-19'),
       ('301301.XSH', '川宁生物', '2012-01-01')],
      dtype=[('symbol', '<U10'), ('name', '<U10'), ('ipo_date', '<M8[D]')])

```

!!! question
    What happened? We obtained a bunch of symbols ending with ".XSH", which should have been strings like "600000.XSHG". Where is the error, and how should it be fixed?

<!--The reason is that our defined `symbol` has only 10 characters, causing overflow after replacement.-->

In the above example, if we change the replacement string to an empty string, we achieve a deletion operation. This is not demonstrated here.

The `char` module also provides a string equality comparison function `equal`:

---

```python
arr = array([('301301.SZ', '川宁生物', '2012-01-01')],
      dtype=[('symbol', '<U10'), ('name', '<U10'), ('ipo_date', '<M8[D]')])

arr[np.char.equal(arr["symbol"], "301301.SZ")]
```

In this specific scenario, we can also directly use the following syntax:

```python
arr[arr["symbol"] == "301301.SZ"]
```

!!! tip 
    There are many functions under `np.char`. How to remember them? In fact, most of these functions are methods of Python’s `str`. If you are familiar with Pandas, you will find similar usage there. Therefore, `str` functions like `upper`, `lower`, and `strip` can be used directly.


Another common scenario for NumPy string functions is formatting. You can use `ljust`, `center`, and `rjust` to pad columns with spaces before displaying an array, ensuring neat output.

!!! question
    Starting May 10, 2024, Nanjing Chemical Fiber experienced a 7-day consecutive limit-up trend, doubling its stock price in just 7 days. Are there other stocks in the market with “Chemical Fiber” in their names? Do their price movements exhibit correlation or cross-period correlation?

---

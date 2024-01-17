---
title: 存了50TB！pyarrow + parquet
slug: pyarrow-plus-parquet
date: 2024-01-03
category: quantlib
motto: time is an arrow, neither stands still or reverses
lunar: 冬月廿二
tags: 
    - quantlib
    - pyarrow
    - parquet
    - 量化数据存储
---

![R50](https://images.jieyu.ai/images/2024/01/apache-arrow.jpg)
在上一篇笔记中，我们指出，如果我们只在日线级别上存储行情数据和因子，HDF5 无论如何都是够用了。即使是在存储了 40 年分钟线的单个股数据集上，查询时间也只花了 0.2 秒 -- 这个速度已经足够快了，如果我们不需要在分钟级别上进行横截面数据查询的话。
<!--more-->
但是，如果个人交易者确实有条件（网速和硬件）做高频交易，处理 tick 级和 level 2 的数据将是必要的。如此一来，我们处理数据的规模就达到了TB级别，但我们还想保持查询时间在毫秒级。或者，您确实需要在分钟级别上进行横截面数据查询，这些场景下，HDF5 就难堪大任了。

---

现在我们得拜托 pyarrow + parquet 了。它们本来就是大数据解决方案之一。本文的标题是存了 50TB。博主并没有这个存储设施进行实验。但这一数字并非杜撰：

![](https://images.jieyu.ai/images/2024/01/parquet-with-50-tb-tick.jpg)

!!! tip level 2 数据有多大？
    据 dolphin（一种高效的时序数据库）的报告，A 股的 level 2 数据达到了一天 10GB 的数据量。

## pyarrow

要介绍 pyarrow，我们先得从 Apache Arrow 说起。Apache Arrow 定义了一种与开发语言无关的列存储（内存中）格式，以便在 CPU/GPU 上高效地执行数据读取和分析任务。

pyarrow 是 Apache Arrow 库的一个 python 实现。Apache Arrow 还有 R， Java 等多种其它实现。但是， Pyarrow 是 Apache Arrow 实现中的头等公民，许多先进的功能都率先在这里实现了，然后才是 R 等其它语言。

---

Pyarrow 支持从 3.8 到 3.11 的 Python 版本。我们使用下面的命令来安装它：

```bash
pip install pyarrow
```

## Parquet
parquet 是一种数据存储格式。在大数据存储语境下，我们还常常看到 feather 这种格式。两者的区别是，parquet 提供了 RLE 压缩，字典编码（与 pandas 中的 category 替换类似）和数据页压缩。因此，在读写速度上要慢于 feather，但更省磁盘空间。

## 基本概念

pyarrow 中最基本的概念主要有：
1. array -- 它是一列同构的数据，但通常允许出现 None。
2. 一系列等长的 arry 实例构成 Record Batch。batch 可以像 array 一样进行切片
3. 在 batch 之上，还有 Table 的概念。table 由一些列构成，每一列都是一个 ChunkedArray。

接下来我们还要接触到 schema 的概念，这将在后面结合示例进行说明。

---

pyarrow 的主要功能：
1. 提供各种 I/O 接口 (memory and IO interfaces)，比如与常见的其它格式，比如 CSV, dataframe, S3, minio，本地文件等之间的读写转换。
2. 为数据提供表格（tabluar datasets）化的视图和相关操作。
3. 提供基础函数 (compute Functions)，如 group, 聚合查询，join 操作，查询操作（表达式，参照 pandas）。

上述功能分类中，括号中的英文也正对应着 Arrow 的文档，以便大家在需要时查询。

## 行情数据存储方案

尽管我们介绍 pyarrow + parquet 是为了存储 level 2 的数据，但我手头并没有相应的 level 2 数据源，所以，也无法做出可实际运行的示例。因此，我们将通过构造 1 分钟行情的数据集来演示如何通过 pyarrow 来写入、增加和查询数据。

我们把每一天所有证券品种的 1 分钟行情放在同一个文件中，所有的分钟线都放在 1m 目录下。这里我们没有使用 partition，但在实际应用中，我们要考虑按年进行分钟线的 patition。对 level 2 的数据，可能要按月或者周进行 partition。

另一方面，每个 parquet 文件的大小最好在 20M 和 2GB 之间，所以，对于分钟线以上级别的数据，可以考虑按周或者更大的尺度写入一个文件。

---

这是磁盘文件结构示例：

```bash
/tmp/pyarrow
├── 1d
├── 1m
│   ├── 2023-12-27.parquet
│   ├── 2023-12-28.parquet
│   └── 2023-12-29.parquet
└── factors
```

首先，我们定义存储字段：

```python
import pyarrow as pa

schema = pa.schema([
        ("symbol", pa.string()),
        ("frame", pa.date64()),
        ("open", pa.float32()),
        ("high", pa.float32()),
        ("low", pa.float32()),
        ("close", pa.float32()),
        ("volume", pa.float64()),
        ("money", pa.float64()),
        ("factor", pa.float64())
])
```

**pyarrow 支持字符串类型和日期类型！**

接下来，我们就实现数据追加和读写部分。由于我们是将每天的分钟线存为一个 parquet 文件，所以代码非常简单：

---

```python
import arrow
import pyarrow.parquet as pq

async def save_1m_bars(codes, dt: datetime.datetime):
    tables = None

    for code in codes:
        bars = await Stock.get_bars(code, 240, FrameType.MIN1, end=dt)
        data = [[code] * len(bars)]

        data.extend([
                    bars[key] for key in bars.dtype.names
                ])
        table = pa.Table.from_arrays(data, schema=schema)
        if tables is None:
            tables = table
        else: # 拼接表
            tables = pa.concat_tables([tables, table])

    # 写入磁盘
    name = arrow.get(dt).format("YYYY-MM-DD")
    pq.write_table(tables, f"/tmp/pyarrow/1m/{name}.parquet")
```

!!! warning 此 Arrow 非彼 Arrow
    注意这段代码开头处，我们引入了 arrow 这个库。它是一个非常好用的 Python 时间库。在这个时间库中， 主要的数据结构也称作 Arrow。

omicron 返回的 bars 是一个 numpy structured array，在转换成 pyarrow Table 时，我们需要先将它拆成 List[array] 的格式，然后通过 from_arrays 来生成一个子 table，它包含了某支个股的 1 分钟行情数据。

---

由于我们要将所有的个股、指数数据存放在同一张大表里，所以，我们还调用了 concat_tables 来实现拼接。**在其它常见的类似数据结构中，无论是 numpy, 还是 pandas 或者 hdf5，这种拼接都有比较昂贵的代价**，但在 pyarrow 中，这种拼接几乎是零成本的！没有数据被拷贝。

接下来，我们就演示一下如何调用 save_1m_bars 来保存数据：


```python
codes = ["000001.XSHE", "600000.XSHG"]
for i in (25, 26, 27, 28, 29):
    dt = datetime.datetime(2023, 12, i, 15)
    await save_1m_bars(codes, dt)
```

## 查询数据

现在，我们把刚刚写进去的数据，再读回来：

```python
import pyarrow.dataset as ds

dataset = ds.dataset("/tmp/pyarrow/1m")
dataset.files
```

dataset 在这里，只是一种元数据。到此为止，它并不会真的从磁盘上加载任何数据。加载数据是从 to_table, 或者某个查询开始的。

---

上述代码将显示该数据集所包含的磁盘文件。

我们可以将 dataset 转换成一张大表：

```python
table = dataset.to_table()
table
```

这将输出 table 的数据字段定义，以及部分数据。

to_table 将会把所有的数据都加载进内存。如果数据量很大，这会导致内存不够用。因此，很多情况下，我们可能使用 RecordBatch:

```python
for rb in dataset.to_batches():
    print(rb.to_pandas())
```

每一个 RecordBatch, 都有一个 to_pandas 方法，这样就进入了你所熟悉的领域。

但更多的时候，我们会通过查询，只加载我们需要的那部分数据。此时，我们需要使用 pyarrow.compute 中的表达式语法，主要是field函数，逻辑运算符和bitwise运算符（此处未演示，即 & | 等）：

---

```python
import pyarrow.compute as pc

filter = (pc.field("frame") > pc.scalar(datetime.datetime(2023, 12, 28, 15)))
dataset.filter(filter).to_table().to_pandas()
```

溺水三千，只取一瓢。这次我们只把其中的 480 条记录加载的了内存中。

![](https://images.jieyu.ai/images/2024/01/pyarrow-filter.jpg)

!!! tip TAKEAWAY
    1. Apache Arrow是一种基于列向量的内存存储格式
    2. Pyarrow是基于Arrow的一个封装库，实现IO，计算和提供表格视图。
    3. 通过from_arrays生成Table, 通过concat_table进行拼接，通过write_table来写入数据到磁盘中。
    4. 通过dataset来加载一组数据集，通过to_table, to_batches或者filter来将数据加载到内存。

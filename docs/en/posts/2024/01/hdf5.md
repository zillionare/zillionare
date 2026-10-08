---
title: "200x Faster: Storing Securities Data with HDF5"
date: 2024-01-02
slug: en/posts/tools/hdf5
tags: [HDF5, Data Storage, Quantitative Trading]
excerpt: "Local market-data storage avoids quota limits and network latency that slow down backtests. This practical guide uses HDF5 and h5py to store, update, and query bars 200x faster than CSV."
lang: en
translation_of: posts/tools/hdf5
auto_translated: true
source_sha: 696935bddd635a8acd6a248a40a73d9a060800e6
---

![R50](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/12/hdf5-book.jpg)

In a note from the 15th of last year, I left a cliffhanger with a tech map for storing quant data and factors. This post starts to fill that gap.

Even if you pay for online data services — for example, a Tushare or JoinQuant account — you still need to build your own local storage. Why?

<!--more-->

Here is why:

1. Online data services usually impose quota limits (JoinQuant, for example). If you run backtests frequently, you will burn through your quota quickly.
2. If your backtest has to fetch data from a remote server, network latency will seriously slow it down.

---

3. Even if an online service provides a factor library (such as Alpha 101 or Alpha 191), **the factors that actually beat the market must come from your own unique research**. So you still have to solve storage for your own factors — which means you still need local storage.

In this post we introduce HDF5, the best starter solution for individual traders. HDF5 can handle quite large datasets.

![L50](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/01/hdf5-national-lab-report.jpg)

According to research by Kesheng Wu and others, when they analyzed futures trading data from 2007 to July 2012 to build a VPIN factor, they processed 3 billion trades, with CSV files totaling 140GB. Computing VPIN on that much data **took 142 seconds with CSV files; after converting to HDF5 format, the same computation took only 0.4 seconds — HDF5 was more than 200x faster!**

HDF (Hierarchical Data Format) is a file format and supporting libraries designed for storing and processing large scientific datasets. It was originally developed by NCSA (the National Center for Supercomputing Applications) and is now maintained by the non-profit HDF Group. The latest format is version 5, hence the name HDF5. HDF originally supported many data types, such as raster images and annotations, while version 5 was simplified to support only scientific datasets (i.e., homogeneous multidimensional arrays) and groups.

The official HDF5 release is based on C/C++, but languages like MATLAB, Java, Python, R, and Julia also have their own HDF5 APIs.

---

As quants, the library we use most is h5py.

![](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2023/12/h5py-logo.jpg)
<cap>h5py logo</cap>

## HDF5 Basics

HDF5 stores data in files. It contains two kinds of objects: datasets (array-like collections) and groups (like folders, which can contain datasets and other groups). You can think of the basic objects in h5py this way:

**Groups work like dictionaries, while datasets work like NumPy arrays.**

The h5py API is fairly low-level and not complicated to use. But to use it as a market-data and factor database, we need to build some functionality ourselves. The code below shows how to store market data and update it daily:

---

```python
codes = ["000001.XSHE", "600000.XSHG"]
h5file = "/tmp/bars.h5"
h5 = h5py.File(h5file, "a")

for name in ("1m", "5m", "10m", "30m", "1d"):
    if name not in h5.keys():
        h5.create_group(f"/{name}")
```

In the code above, we create one group per bar frequency. Market data will then be stored inside these groups under each security code.

```python
def convert_frame(bars):
    # H5 不能处理 NP.DATETIME64，转换成整数
    dtype = bars.dtype.descr
    dtype[0] = ('frame', 'i8')
    
    return bars.astype(dtype)
```

We use omicron to fetch market data. Its bars contain a `frame` field of type np.datetime64, which h5py cannot handle, so we convert it to epoch time for storage. h5py also lets you save time types directly (opaquely), but then some query operations are no longer supported.

We append new data to the existing dataset like this:

---

```python
def append_ds(name: str, bars):
    ds = h5.get(name)
    if ds is None:
        ds = h5.create_dataset(name, data = bars, chunks=True, maxshape=(None,))
    else:
        nold = ds.shape[0]
        nnew = len(bars)
        ds.resize(nold + nnew, axis=0)
        ds[-nnew:] = bars
        
    return ds
```

This also demonstrates `get` for accessing a dataset, `create_dataset` for creating one, and the `resize` method. To support `resize`, we must declare `chunks=True` and `maxshape=(None,)` when creating the dataset.

New data is added with slice syntax. Now let's implement daily appending:

```python
# 每日增加行情数据
async def save_bars(codes:List[str], ft: FrameType):    
    for code in codes:
        bars = await Stock.get_bars(code, 240, ft)
        append_ds(f"/{ft.value}/{code}", convert_frame(bars))
```

Finally, let's write a function to display its structure:

---

```python
# 显示 H5 文件结构

def h5_tree(val, pre=''):
    items = len(val)
    for key, val in val.items():
        items -= 1
        if items == 0:
            # THE LAST ITEM
            if type(val) == h5py._hl.group.Group:
                print(pre + '└── ' + key)
                h5_tree(val, pre+'    ')
            else:
                print(pre + '└── ' + key + ' (%d)' % len(val))
        else:
            if type(val) == h5py._hl.group.Group:
                print(pre + '├── ' + key)
                h5_tree(val, pre+'│   ')
            else:
                print(pre + '├── ' + key + ' (%d)' % len(val))
                
h5_tree(h5)
```

We will get output similar to this:

```
├── 1d
│   ├── 000001.XSHE (240)
│   └── 600000.XSHG (240)
└── 1m
    ├── 000001.XSHE (1200)
    └── 600000.XSHG (1200)
```

That completes the basic structure for storing market data in HDF5. You can query it like this:

---

```python
filter = mbars["close"] > 14.77
mbars[filter]
```

We simulated a 40-year minute-bar dataset, and the query above takes 0.2 seconds to run.

One downside of this layout is that cross-section queries (for example, querying the close price of all stocks at a given point in time) are relatively slow, because looping is hard to avoid. HDF5 offers virtual datasets for this, but they are not suitable for variable-length datasets.

One workaround is to store the security code together with the market data. Of course, to speed up queries, we need to convert string security codes to integers in advance. For example, a code like 000001.XSHE can be converted to 100001, and 600000.XSHG to 2600000 — i.e., using a 7-digit security code where the first non-zero digit is the exchange code.

In that case, however, the dataset becomes larger and queries take longer. So when designing the layout, you need to weigh the relative frequency of the two access patterns.

## Need for speed!
Think h5py is still not fast enough?! Then consider Parallel HDF5. Here are the steps to install it on Ubuntu:

---

```
sudo apt update

# 安装支持并行运算的 HDF5 原生库
sudo apt install libhdf5-mpi-dev

# 检查 HDF5 并行运算是否开启
h5pcc

# 需要这一步以下载 H5PY
sudo apt install -y pkg-config

# 安装支持并行运算的 H5PY
export CC=mpicc
export HDF5_MPI="ON"
pip install --no-binary=h5py h5py
```
In the last step, specifying **-\-no-binary=h5py** in `pip install` is the key point. With this flag, we download the h5py source, compile it locally, and then install h5py, instead of installing h5py directly from a wheel. If you install from a wheel, you will not get parallel HDF5 support.

For how to use the parallel version of h5py, see this [link](https://www.nersc.gov/assets/Uploads/H5py-2017-Feb23.pdf). If you cannot open external links, google 大富翁量化 to find the article of the same title and sample code on the official site.

## Need even more speed!

Although HDF5 provides the ability to store and access massive datasets, its documentation — and no tutorial — will tell you that it cannot provide index-based queries. As your dataset grows, query time will slow down linearly.

---

!!! tip
    When evaluating a technology, we always want a full picture of its strengths and weaknesses. But official docs often cover only the advantages and stay silent on the drawbacks. Oddly, third-party tutorials often gloss over the flaws as well. The reason may be that mentioning the drawbacks could turn readers away and reduce traffic to the tutorial. That may be why you should keep reading my blog — I don't want you to pick the wrong technology because of my articles, waste time on it, and then have to start over with something new.

One solution is to split the data into multiple datasets, with each dataset name tied to time, so time-related queries can be accelerated. Another approach is to use fastquery, which builds a bitmap-based index. However, I have not seen a ready-made Python library for it.

![R50](https://cdn.jsdelivr.net/gh/zillionare/images@main/images/2024/01/modin.jpg)

Another option might be to use HDF5 only as the underlying persistence layer, and route all queries through modin — a pandas replacement that can load files far larger than physical memory — to operate on the datasets.

Of course, based on our testing, if you only need to handle daily-level market data, direct queries without an index are perfectly fine speed-wise. So this is the simplest approach for individual researchers, which is why it is recommended in the first post of this series.

---

If you want to store minute-level data while keeping query speed very high, that is where pyarrow + parquet shines, which we will cover in the next post.

This post comes with sample h5py code. The notebook is available on the [大富翁量化 website](/assets/notebooks/h5py_update.ipynb). If the 🔗 does not display, google 大富翁量化.

!!! tip TAKEAWAY
    1. HDF5 is a file format and libraries for storing and processing large scientific datasets
    2. HDF5 reads and writes hundreds of times faster than CSV. Searching across 240M records takes about 0.2 seconds.
    3. The Python library for reading HDF5 files is h5py
    4. Market data should be organized into groups by bar frequency. Child datasets are keyed by security code.
    5. Covered creating, querying, and appending market data in HDF5 files.
    6. Several ways to boost HDF5 performance.

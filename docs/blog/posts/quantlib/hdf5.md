---
title: 200倍速！基于 HDF5 的证券数据存储
date: 2024-01-02
lunar: 冬月廿一
slug: save-quote-data-with-hdf5
motto: Data Science is 90% data and 10% science<br> and 100% impossible without python.
categories:
    - quantlib
tags:
    - quantlib
    - 量化数据存储
    - hdf5
    - h5py
---

![R50](https://images.jieyu.ai/images/2023/12/hdf5-book.jpg)

去年 15 日的笔记挖了个坑，给出了量化数据和因子的存储方案技术导图。这一篇笔记就开始填坑。

即使我们购买了在线数据服务，比如 tushare, 聚宽的账号，我们仍然要构建自己的本地存储，为什么？

<!--more-->

原因如下：

1. 在线数据服务一般都有 quota 限制（比如聚宽）。如果我们要频繁地进行回测，很容易用尽 quota。
2. 如果我们在回测时，使用的数据要从远程服务器上获取，网络延时会大大影响到回测速度。
   
---

3. 即使在线数据服务提供了因子库（比如 Alpha 101， Alpha 191 因子库），但是，**真正能战胜市场的因子，必然来自于你自己的独特研究**，所以， 我们也要解决自己提取的因子如何存储的问题，这也决定了我们仍然要构建自己的本地存储。

这一篇笔我们介绍 HDF5，这是最适合个人交易者的入门方案。HDF5 可以处理相当大容量的数据。

![L50](https://images.jieyu.ai/images/2024/01/hdf5-national-lab-report.jpg)

根据 Kesheng Wu 等人的研究，他们分析 2007 年到 2012 年 7 月间的期货交易数据，以构建 VPIN 因子时，处理的交易数据达 30 亿条，CSV 文件的大小达到了 140GB。当使用这么多数据进行 VPIN 计算时，**使用 CSV 文件的时间是 142 秒；将其转换成 HDF5 格式后，同样的计算则只花了 0.4 秒，HDF5快了200多倍！**

HDF（Hierarchical Data Format）是一种为存储和处理大容量科学数据设计的文件格式及相应库文件。最早由 NCSA （美国国家超级计算应用中心） 研究开发，现由非盈利组织 HDF Group 维护。最新的格式是第 5 版，因此就被称为 HDF5。HDF 最初提供了多种数据类型，比如光栅图像和注解等，而在第 5 版中，简化到只支持科学数据集（即同质多维数组）和群组两种类型。

HDF5 官方版本是基于 C/C++ 的，但也像 MATLAB、Java、Python、R 和 Julia 这些语言也有自己版本的 HDF5 API。

---

作为量化人，我们使用最多的是 h5py。

![](https://images.jieyu.ai/images/2023/12/h5py-logo.jpg)
<cap>h5py 的 logo</cap>

## HDF5 的基本概念

HDF5 使用文件来存储数据。它包含两种对象，即数据集(这是一种类似于数组的数据集合）和群组（类似于文件夹，其下可包含数据集 datasets 和其它群组）。我们可以这样来理解 h5py 中的基本对象：

**群组象字典一样工作，而数据集则像 Numpy 数组一样工作。**

h5py 的 API 比较基础，用法并不复杂。但作为行情和因子数据库，我们需要自己构建一些功能。下面的代码，将演示我们如何存储行情数据，并实现每日更新：

---

```python
codes = ["000001.XSHE", "600000.XSHG"]
h5file = "/tmp/bars.h5"
h5 = h5py.File(h5file, "a")

for name in ("1m", "5m", "10m", "30m", "1d"):
    if name not in h5.keys():
        h5.create_group(f"/{name}")
```

在上述代码中，我们按行情的周期频率，分别创建了若干个 group。接下来的行情数据
就会以证券代码为 name，存储在这些 group 中。

```python
def convert_frame(bars):
    # H5 不能处理 NP.DATETIME64，转换成整数
    dtype = bars.dtype.descr
    dtype[0] = ('frame', 'i8')
    
    return bars.astype(dtype)
```

我们使用 omicron 来获取行情数据。它返回的行情数据中，有一个 frame 字段，数据类型为 np.datetime64，是 h5py 不能处理的，因此我们将它转换为 epoch 时间来保存。h5py 也允许我们直接保存时间类型（以不透明的方式），但这样一来，就不再支持一些查询操作了。

我们使用下述方法来把新的数据追加到之前的数据集中：

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

这里还展示了获取数据集的方法 get，创建数据集的方法 create_dataset 和 resize 方法。为了支持 resize，我们在创建数据集时，还必须声明 chunks = True 以及 amxshape=(None,)。

添加新的数据是以切片语法来完成的。现在，我们来实现每日追加数据的功能：

```python
# 每日增加行情数据
async def save_bars(codes:List[str], ft: FrameType):    
    for code in codes:
        bars = await Stock.get_bars(code, 240, ft)
        append_ds(f"/{ft.value}/{code}", convert_frame(bars))
```

最后，我们写一个显示其数据结构的函数：

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

我们将得到类似下面的输出：

```
├── 1d
│   ├── 000001.XSHE (240)
│   └── 600000.XSHG (240)
└── 1m
    ├── 000001.XSHE (1200)
    └── 600000.XSHG (1200)
```

这样，使用 hdf5 来存储行情数据的基本结构就完成了。我们可以用下面的方法进行查询：

---

```python
filter = mbars["close"] > 14.77
mbars[filter]
```

我们模拟了一个 40 年分钟线的数据集，在进行上述查询时，需要执行 0.2 秒。

上述存储结构有一个不利之处，就是在查询横截面数据（比如，要查询某个时间点上所有个股的收盘价）时，速度会比较慢，因为循环难以避免。hdf5 提供了 virtual dataset 这一功能，但它并不适合可变长的数据集。

办法之一是，在存储行情数据时，把个股的代码也存储进来。当然，为了加快查询速度，我们需要将以字符串表示的证券代码，事先转换成为整数格式。比如，象 000001.XSHE 这样的代码，我们可以转换成为 100001，600000.XSHG 转换为 2600000：即使用 7 位数证券代码，第 1 位非零，为交易所编码。

但这种情况下，由于数据集变大，我们执行查询的速度也会变长。因此我们在设计时，要综合考虑两种场景的使用占比。

## Need for speed!
觉得 h5py 还不够快？！那么，你可以考虑使用 Parallel HDF5。这是在 ubuntu 上安装它的步骤：

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
最后一步，在 pip install 时指定 **-\-no-binary=h5py** 要划重点。通过这里的指定，我们将下载 h5py 的源码，在本地执行编译，再安装 h5py，而不是直接安装 wheel 格式的 h5py。如果是从 wheel 格式进行安装，我们将无法得到并行计算的 hdf5 功能。

关于并行版本的 h5py 的使用，可以参考这个[链接](https://www.nersc.gov/assets/Uploads/H5py-2017-Feb23.pdf)。无法查看外链的，可以 google 大富翁量化，在官网上查看同名文章和示例代码。

## Need even more speed!

尽管 hdf5 提供了存储和访问海量数据的能力，但是，它的文档、及任何一本教程都不会告诉你，它不能提供基于索引的查询。随着你的数据集越来越大，查询速度将会以线性增加的方式变慢。

---

!!! tip
    当我们进行技术选型时，我们总是希望全面了解一门技术的优势和缺陷。但是，官方文档常常只介绍它的优点，对其缺点则避而不谈。奇怪的是，第三方的教程也往往对它的缺陷也往往闪烁其辞。原因可能是，一旦他们谈及了这门技术的缺陷，就可能导致读者失去学习的兴趣，进而降低该教程的流量。这也许是你应该常读我的博文的原因 -- 我并不希望你因为我的文章，选择了并不恰当的技术，在浪费了一段时间后，不得不从头再来选择新的技术。

解决方案之一是将数据切分为多个dataset，每个 dataset 的名字与时间关联起来，这样在进行与时间相关的查询时，就可以获得较好的加速。另一个方法是使用 fastquery，它建立了一个基于 bitmap 的索引。不过我并没有看到现成的 python 库。

![R50](https://images.jieyu.ai/images/2024/01/modin.jpg)

另一个方案可能是，仅仅将 hdf5 作为基础的持久化设施，而对它的查询操作，全部通过 modin -- 这是 pandas 的平替，可以载入远大于物理内存的文件--来操作数据集。

当然，从我们的测试来看，如果你只需要处理到日线级别的行情数据，那么直接使用无索引的查询，速度上是没有任何问题的。所以，这是对个人研究者而言，最简单的方式，就放在本系列第一篇中进行推荐。

---

如果你希望存储到分钟级的数据，还要保持非常好的查询速度，怎么办？这就 pyarrow + parquet 可以发力的地方，我们将在下一篇里介绍。

本文附有h5py使用示例代码。notebook可以在[大富翁量化网站](/assets/notebooks/h5py_update.ipynb)获得。如果🔗无法显示，可以google大富翁量化。

!!! tip TAKEAWAY
    1. hdf5是一种存储和处理大容量科学数据的文件格式及相应库
    2. hdf5的读写速度是csv的数百倍。在240M记录中进行查找，速度约为0.2秒。
    3. 读取hdf5文件的python库是h5py
    4. 行情数据应该按周期创建群组。子数据集以证券代码为key。
    5. 介绍了创建、查询和追加行情数据到hdf5文件中。
    6. 增强hdf5性能的几种方式。

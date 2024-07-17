---
title: xtquant 中的板块数据
date: 2023-12-27
motto: 见天地 见众生 见自己<br>坚持学习 遇见更好的自己
slug: arsenal
lunar: 冬月十五
category: arsenal
tags:
    - xtquant
    - quantlib
---

![R50](https://images.jieyu.ai/images/2023/12/sector-cloud.jpg?4)

!!! tip 笔记要点

1. xtquant 中有哪些板块和板块分类？
    1. 如何获取板块的成份股？
    2. 如何获取指数的行情数据？

<!--more-->

xtquant 是一个 Python 库，提供了行情数据和实盘接口。只要您的券商支持 QMT，并且您也申请到了量化接口权限，就可以免费使用这些数据和实盘接口，这也是目前性价比较高、门槛较低的接入方式。因此，我们会通过多篇笔记来介绍这个库。

今天要探索的是，xtquant 中的板块是如何组织的。这部分内容，虽然在官方文档有一些介绍，但并没有把 API 的使用串联起来。有一些知识点也是经询问官方才知道的，可能一段时间内，这仍然是**独家资料**，值得收藏。

---

## Xtquant 中有哪些板块

xtquant 中的板块列表通过 get_sector_list 来获取。返回结果是一个字符串列表：

```python
from xtquant import xtdata
sectors = xtdata.get_sector_list()
for i in range(0, len(sectors), 6):
    print(" ".join(sectors[i:i+6]))
```

我们将得到 5000 多个板块名称，摘录其中的部分显示如下：

```
上期所上证 A 股，上证 B 股，上证期权，上证转债，中金所
创业板，大商所，板块加权指数，板块指数，概念指数，沪市 ETF
沪市债券，沪市基金，沪市指数，沪深 A 股，沪深 B 股，沪深 ETF
迅投一级行业板块指数，迅投三级行业板块加权指数，迅投三级行业板块指数
郑商所，香港联交所指数，香港联交所股票，ETF 主题指数，ETF 债券型，ETF 商品型
ETF 股票型，ETF 行业指数，ETF 货币型，ETF 跨境型，TGN3D 打印，TGN5G
TGNMicroLED 概念，TGNMiniLED,TGNMLOps 概念，TGNMR
...
```

板块比较多。下面我们介绍它的几个重要归类：

### 指数类
在名称中出现指数一词的，大约有 80 个。也就是说，这个板块是由指数的代码组成的：

---

![](https://images.jieyu.ai/images/2023/12/xtquant-sector.jpg)

我们看看沪深指数这个板块都由哪些指数组成：

```python
for sector in xtdata.get_stock_list_in_sector('沪深指数'):
    detail = xtdata.get_instrument_detail(sector)
    name = detail["InstrumentName"]
    print(sector, name)
```

这里大约有 600 种指数，比如我们常用的上证指数 (000001.SH), 上证 50，上证 300 等都在这里面。如果你要获取中证 1000 的行情数据，但不知道它的代码是多少，就需要在这里查询：

```python
for sector in xtdata.get_stock_list_in_sector('沪深指数'):
    detail = xtdata.get_instrument_detail(sector)
    name = detail["InstrumentName"]
    if name == "中证 1000":
        print(sector)
```

---

代码是"000852.SH"和"399852.SZ"，它们分别是中证 1000 在沪指和深指中的代码。接下来我们就可以通过上一篇笔记介绍的方法，来获取这个指数的行情：

```python
xtdata.download_history_data("399852.SZ", period="1d")
xtdata.get_market_data(stock_list=["399852.SZ"], period='1d', count=10)
```

## 概念和同花顺概念

注意“概念指数”这个板块，我们通过下面的代码来列出它包含的指数：

```python
for code in xtdata.get_stock_list_in_sector("概念指数"):
    detail = xtdata.get_instrument_detail(code)
    name = detail["InstrumentName"]

    print(sector, name)
```

部分输出如下：

```
102566.BKZS GNoled 材料
101285.BKZS GN 龙虎榜热门
102109.BKZS GN 太阳能
102512.BKZS GN 安邦系
101602.BKZS GN 饲料
101219.BKZS GN 室外经济
```
但是似乎拿不到这些板块的指数。我们将继续咨询官方，得到反馈后再向大家报告。如果您现在就需要这些板块的指数，那么可以**手工计算一个等权指数**出来。

---

以 GNoled 材料为例，我们可以拿到它的成份股构成，进而得到所有成份股的行情：

```python
secs = xtdata.get_stock_list_in_sector('GNoled 材料')
xtdata.download_history_data2(secs, period='1d', start_time="20231220")

barss = xtdata.get_market_data(stock_list=secs, count=10)
barss
```

此时我们得到输出如下：

![](https://images.jieyu.ai/images/2023/12/xtquant-gn-bars.png)

我们通过下面的方法求等权指数，注意这里的转置，以及求均值时，我们传入的 axis=1 的参数。

```python
barss["close"].T.mean(axis=1)
```

此时我们得到的输出如下：

```
20231220    19.030909
20231221    19.072121
20231222    18.880909
20231225    18.978485
```

---

我们看到板块名字中，好多以 T 开头的，比如 TGN，THY 等。官方文档中似乎没有关于它们的说明，猜测可能是**同花顺概念、同花顺行业**。

## 申万行业分类板块

如果你希望得到按申万行业分类的板块，应该用以下代码进行查询：

```python
for code in xtdata.get_stock_list_in_sector("迅投一级行业板块指数"):
    detail = xtdata.get_instrument_detail(code)
    name = detail["InstrumentName"]
    if name.startswith("SW"):
        print(code, name)
```

这样得到的是申万一级行业板块。如果要查询二级、三级，应该分别使用迅投二级行业板块指数和迅投三级行业板块指数。但似乎也无法获取它们的指数。

## 可转债

我们通过以下代码查找所有的可转债，并得到它们的代码和名字：

```
for sector in xtdata.get_sector_list():
    if sector.find("可转债") != -1:
        print(sector)
xtdata.get_stock_list_in_sector("沪深 A 股")
xtdata.get_stock_list_in_sector("可转债等权")
xtdata.get_instrument_detail("110047.SH")
```

---

这将输出 110043SH 无锡转债。我们可以由它的代码，进一步得到它的行情数据。

## 小结

!!! tip
    1. xtquant 中，get_sector_list 会得到一个板块名称列表。通过板块名，可以进一步得到各个板块的成分股构成。<br><br>
    2. 上述返回值中，有一类特殊的板块，它们的名字中带有“指数”这个词。<br><br>
    3. 指数板块中，比如沪深指数，包含了我们最常见、最常用的一些指数，如上证，沪深 300 等，这些指数我们可以获取行情数据<br><br>
    4. 其它板块，即使是名字中包含指数的，比如概念指数，似乎也无法获取到其指数。<br><br>
    5. 对获取不到指数的，我们可以手工计算其等权指数。
